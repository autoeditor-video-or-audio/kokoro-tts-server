# Fork remsky/Kokoro-FastAPI as autoeditor/kokoro-tts-server

## Why
nifty-star's Kokoro voice blending (Phase 9c) is blocked on the upstream
server: `POST /v1/audio/voices/combine` returns HTTP 403
`{error:"permission_denied", message:"Local voice saving is disabled"}`
because the upstream config flag `allow_local_voice_saving` defaults to
`False` and the published image bakes the default in.

Beyond the flag, we also need:

- A MinIO sync endpoint so voicepacks produced by the sibling
  `tts-trainer` fork (Phase 9b) land in the inference container's
  `voices/v1_0/` folder without a manual `docker cp`.
- Operational parity with the other sibling forks (`omnivoice-tts`,
  `tts-trainer`, `qwen3-tts`): helm chart, k8s manifests, CI matrix,
  GHCR publish, OpenSpec change tracking.

Forking under `autoeditor-video-or-audio/kokoro-tts-server` and layering
a minimal `server_addons/` package over the upstream API is the
lowest-cost path. Nothing in `api/src/` is modified, so future
`git pull upstream master` keeps working.

## What Changes
- Set `ALLOW_LOCAL_VOICE_SAVING=true` as the default ENV in
  `Dockerfile.gpu`. Upstream pydantic-settings overrides
  `Settings.allow_local_voice_saving` from this env name automatically.
- Add `server_addons/sync.py` wrapping the MinIO SDK to mirror every
  `*.pt` under `s3://${MINIO_BUCKET}/voicepacks/` into
  `/app/api/src/voices/v1_0/`. Sha256 idempotency.
- Add `server_addons/router.py` exposing:
  - `POST /v1/voices/sync-from-minio` →
    `{synced:[<names>], skipped:[<names>]}`
  - `POST /v1/voices/reload` → triggers the upstream voice-manager
    re-list so a freshly synced `.pt` is immediately visible to
    `/v1/audio/voices`.
- Add `server_addons/main.py` that imports the upstream
  `api.src.main.app`, calls `app.include_router(sync_router, ...)`,
  and (optionally) runs an initial sync on startup if
  `KOKORO_SYNC_ON_START=1`. The Dockerfile entrypoint switches to
  `server_addons.main:app`.
- Add `Dockerfile.gpu` that **inherits the upstream multi-stage build**
  (we keep using `docker/gpu/Dockerfile` as the base; this is a layer
  on top, not a rewrite). Installs `minio` SDK + copies
  `server_addons/`.
- Add `docker-compose.gpu.prod.yml` + `.env.example` (host port 8880,
  NVIDIA runtime, MinIO env, optional bind mount for `voices/v1_0/`).
- Add helm chart + k8s manifests cloned from omnivoice-tts and renamed.
- Add `.github/workflows/ci.yml` with semantic-release + single `gpu`
  matrix publishing to GHCR + helm bump + cleanup keep-10.
- Add `.releaserc.json`, `NOTICE-fork.md`, `README-fork.md`.

## Impact
- NEW capability: `kokoro-tts-server` (this change is its only source
  of truth).
- Drop-in port 8880 replacement: vibetalker's `/api/tts/*` proxy keeps
  working without any client-side change.
- 9c's *Save as voicepack* button (already shipped in vibetalker)
  starts returning 200 the moment this fork's image is pulled on host
  `.4`.

## Sibling work
- `vibetalker/openspec/changes/add-kokoro-voice-blending/` already
  documents the client side; no change required there.
- `autoeditor-video-or-audio/tts-trainer` produces the voicepacks the
  MinIO sync endpoint pulls.

## Pre-flight on the GPU host (`.4`, RTX 4060 8 GB)
1. `docker stop kokoro-fastapi-old || true` — free port 8880.
2. Pull our image (`:latest-gpu`).
3. Run `docker compose --env-file .env -f docker-compose.gpu.prod.yml up -d`.
4. Confirm `/v1/audio/voices` lists `pf_dora`, `pm_alex`, `pm_santa`
   (upstream defaults).
5. Retry **Save as voicepack** from the vibetalker UI.
