# Fork notice

`autoeditor-video-or-audio/kokoro-tts-server` is a fork of
[`remsky/Kokoro-FastAPI`](https://github.com/remsky/Kokoro-FastAPI)
(Apache License 2.0). Upstream's `api/src/` Python package is shipped
verbatim; this fork adds:

- `server_addons/` — extra FastAPI router mounted on top of the
  upstream `app`. Provides `POST /v1/voices/sync-from-minio` and
  `POST /v1/voices/reload`, plus a lifespan hook that runs an initial
  MinIO sync when `KOKORO_SYNC_ON_START=1`.
- `Dockerfile.gpu` — wraps the upstream GPU Dockerfile stages, installs
  the `minio` SDK, copies `server_addons/`, sets
  `ALLOW_LOCAL_VOICE_SAVING=true` as the new default, and switches the
  uvicorn entrypoint from `api.src.main:app` to `server_addons.main:app`.
- `docker-compose.gpu.prod.yml`, `helm/`, `k8s/`, `.env.example` —
  operational manifests matching the nifty-star sibling-fork pattern.
- `.github/workflows/ci.yml` — semantic-release + a single `gpu`
  matrix that publishes `ghcr.io/autoeditor-video-or-audio/kokoro-tts-server:vX.Y.Z-gpu`
  (no `-flash` variant; Kokoro inference is small enough that flash-attn
  brings no measurable win).
- `openspec/changes/add-kokoro-tts-server/` — proposal / design /
  tasks / strict-validated capability spec.

Upstream `api/src/` is never patched in place. Pydantic-settings reads
the new `ALLOW_LOCAL_VOICE_SAVING=true` env default, so
`POST /v1/audio/voices/combine` persists user blends as
`.pt` voicepacks without code changes. Rebases against
`remsky/Kokoro-FastAPI` only need to verify that
`api.src.main:app` still exists as an importable FastAPI instance.

Apache 2.0 is preserved in `LICENSE`.
