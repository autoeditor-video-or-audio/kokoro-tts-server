# Design — kokoro-tts-server (minimal fork layer)

## Context
The upstream `remsky/Kokoro-FastAPI` repo is healthy and well-tested.
We want everything it already provides (OpenAI-compat speech endpoint,
voice blender, models index, Japanese support, Helm chart of its own)
without diverging from upstream. The only structural delta we need is:

1. A flipped default for `allow_local_voice_saving`.
2. A MinIO sync route for voicepacks produced by `tts-trainer`.
3. Operational parity (CI matrix, helm/k8s mirroring our sibling
   forks).

## Decisions
- **Layer, don't rewrite.** Keep `api/src/` byte-identical with
  upstream. Add new code under `server_addons/`. Future
  `git pull upstream master` rebases cleanly.
- **Env-driven flag flip.** Pydantic-settings reads
  `Settings.allow_local_voice_saving` from `ALLOW_LOCAL_VOICE_SAVING`.
  Set this in the Dockerfile ENV layer; operators can override per-env.
- **Module-level mount.** `server_addons/main.py` imports the upstream
  `app` and calls `app.include_router(...)`. Single FastAPI process,
  same lifespan. The Docker `CMD` switches to
  `server_addons.main:app`.
- **MinIO sync is opt-in per request.** We do **not** poll. The
  vibetalker side fires `POST /v1/voices/sync-from-minio` after the
  tts-trainer export completes. Optional lifespan startup sync via
  `KOKORO_SYNC_ON_START=1` for fully-headless flows.
- **Sha256 idempotency.** Before downloading a voicepack, the sync
  routine hashes the local `.pt`; if it matches MinIO's etag, skip.
  Returned response declares `synced` (downloaded) vs `skipped`
  (already current).
- **Reload after sync.** Upstream caches voice metadata. Our
  `POST /v1/voices/reload` clears that cache so the freshly synced
  `.pt` shows up in `/v1/audio/voices` without restart.
- **CI matrix `gpu` only.** Kokoro inference does not benefit from
  flash-attn (small model, low sequence lengths). No `:gpu-flash`
  flavour.

## Alternatives considered
- **Rewrite upstream into our omnivoice-tts shape.** Discarded: weeks
  of work duplicating the OpenAI-compat layer, breaks paridade with
  third-party OpenAI clients, loses Japanese support, makes upstream
  bug fixes painful to absorb.
- **Patch `api/src/core/config.py` directly to flip the default.**
  Discarded: touches upstream tree, complicates rebases. ENV override
  is cleaner.
- **Watcher daemon polling MinIO.** Discarded: extra thread, race
  conditions with the upstream voice manager. The on-demand endpoint
  is sufficient.

## Risks
- **Upstream rename of `api.src.main:app`.** Our
  `server_addons/main.py` is the only import surface. A rename is a
  one-file fix.
- **Sudachi/UniDic 526 MB.** Inherited from upstream. Acceptable for
  now; if image pulls slow on `.4`, follow-up will expose a build
  arg `INCLUDE_JAPANESE=false`.
- **MinIO unreachable on startup.** If `KOKORO_SYNC_ON_START=1` and
  MinIO is down, the lifespan hook logs an error but the FastAPI app
  still starts (upstream voices still serve). The on-demand sync
  endpoint surfaces the error directly to the caller.
