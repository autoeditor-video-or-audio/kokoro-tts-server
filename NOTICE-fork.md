# Fork notice

`autoeditor-video-or-audio/kokoro-tts-server` is a fork of
[`remsky/Kokoro-FastAPI`](https://github.com/remsky/Kokoro-FastAPI)
(Apache License 2.0). Upstream's `api/src/` Python package is shipped
verbatim; this fork adds:

- `server_addons/` — extra FastAPI router mounted on top of the
  upstream `app`. Provides:
    - `POST /v1/voices/save-combined` — persist a weighted blend of
      base voicepacks as a new `.pt` under `Settings.voices_dir`.
      Each entry in `voices[]` is `<name>` (default weight 1.0) or
      `<name>(<weight>)`; weights are normalised to sum 1.0 before
      the tensor blend. Reuses the upstream `VoiceManager.load_voice`
      to fetch base tensors.
    - `POST /v1/voices/sync-from-minio` — pull every `*.pt` under
      `s3://${MINIO_BUCKET}/voicepacks/` into the local `voices_dir`
      (idempotent: sha256-compared against MinIO etag).
    - `POST /v1/voices/reload` — flush the upstream `VoiceManager`
      cache so a fresh `GET /v1/audio/voices` re-scans the directory.
    - Lifespan hook running an initial sync when
      `KOKORO_SYNC_ON_START=1`.
- `Dockerfile.gpu` and `Dockerfile.cpu` — wrap the upstream
  `docker/gpu/Dockerfile` / `docker/cpu/Dockerfile` build steps,
  install the `minio` SDK, copy `server_addons/`, stage the baked
  voicepacks at `/app/voices-baked/` so a runtime bind mount on
  `voices_dir` doesn't mask them, and rewrite the container
  entrypoint to (1) seed the mounted `voices_dir` from the baked
  staging dir, (2) preserve upstream's optional model download, and
  (3) launch `server_addons.main:app` via uv. Both flavours set
  `ALLOW_LOCAL_VOICE_SAVING=true` as the new default via `ENV`.
- `docker-compose.gpu.prod.yml` / `docker-compose.cpu.prod.yml`,
  `helm/`, `k8s/`, `.env.example` — operational manifests matching
  the nifty-star sibling-fork pattern. The shared `.env.example`
  documents the `KOKORO_IMAGE_TAG=latest-{gpu,cpu}` switch.
- `.github/workflows/ci.yml` — semantic-release + a dual matrix that
  publishes `ghcr.io/autoeditor-video-or-audio/kokoro-tts-server:vX.Y.Z-gpu`
  AND `:vX.Y.Z-cpu` (plus the rolling `:latest-gpu` / `:latest-cpu`
  pointers). The cleanup job preserves both `latest-` tags while
  trimming old pinned versions.
- `openspec/changes/2026-05-14-add-kokoro-tts-server/` (archived) and
  `openspec/specs/kokoro-tts-server/spec.md` — strict-validated
  capability spec documenting every delta above.

Upstream `api/src/` is never patched in place. Pydantic-settings reads
the new `ALLOW_LOCAL_VOICE_SAVING=true` env default. Rebases against
`remsky/Kokoro-FastAPI` only need to verify that `api.src.main:app`
still exists as an importable FastAPI instance and that
`VoiceManager.load_voice(name)` still expects a bare voicepack name.

Apache 2.0 is preserved in `LICENSE`.
