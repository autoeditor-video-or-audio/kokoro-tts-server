# Design

## save-combined keeps its own blend math

Since upstream v0.8.1, `POST /v1/audio/voices/combine` accepts the
weighted syntax (`a(2)+b(1)`) through `process_and_validate_voices` and
`TTSService.get_voices_path`. `save-combined` could delegate to them, but
`get_voices_path` writes the blend to a temp file and returns a generated
name, so persisting would still need a copy into `voices_dir`, and the
route would depend on two more upstream internals instead of the single
`VoiceManager.load_voice` it uses today. The fork keeps its own parse +
normalise + weighted sum (a few lines, covered by
`server_addons/tests/test_router.py`).

## Startup sync is chained into the upstream lifespan

Upstream builds its app with `FastAPI(lifespan=...)`. With a lifespan
set, Starlette never runs `@app.on_event("startup")` handlers (probed on
fastapi 0.141.1 / starlette 1.4.1: only the lifespan ran), so the
fork's `KOKORO_SYNC_ON_START` hook was dead code. `server_addons/main.py`
now wraps `app.router.lifespan_context`: upstream warmup runs first,
then the optional MinIO sync, which still never blocks startup.

## Dockerfiles mirror upstream Dockerfile.optimized

Upstream v0.9.0 deleted the single-stage `docker/{gpu,cpu}/Dockerfile`
the fork layers were copied from. The fork Dockerfiles are now the
upstream `Dockerfile.optimized` files plus a short list of deltas
(listed in each file's header), so the next sync is a diff against
those two files. The appuser uid stays 1001 on both flavours because
existing voices volumes were chowned to it.
