# kokoro-tts-server (fork)

Drop-in replacement for `remsky/Kokoro-FastAPI` with two operational
deltas that the nifty-star sequencer needs:

1. **`ALLOW_LOCAL_VOICE_SAVING=true` is the new default**, so
   `POST /v1/audio/voices/combine` actually persists the resulting
   `.pt` voicepack instead of returning HTTP 403 `permission_denied`.
2. **`POST /v1/voices/sync-from-minio`** pulls every `*.pt` under
   `s3://${MINIO_BUCKET}/voicepacks/` into the local
   `/app/api/src/voices/v1_0/` folder and rebuilds the upstream voice
   cache. `POST /v1/voices/reload` rebuilds the cache without a
   sync. A lifespan hook runs an initial sync if
   `KOKORO_SYNC_ON_START=1`.

Everything else is upstream: `/v1/audio/speech`, `/v1/audio/voices`,
`/v1/audio/voices/combine`, `/v1/models`, etc.

## Run on a GPU host

```bash
mkdir -p ~/works/services/kokoro-tts-server && cd $_
curl -O https://raw.githubusercontent.com/autoeditor-video-or-audio/kokoro-tts-server/main/docker-compose.gpu.prod.yml
curl -O https://raw.githubusercontent.com/autoeditor-video-or-audio/kokoro-tts-server/main/.env.example
cp .env.example .env
# Edit .env: set MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY.

# If an old upstream kokoro-fastapi container holds port 8880:
docker stop kokoro-fastapi-old || true
docker rm   kokoro-fastapi-old || true

docker compose --env-file .env -f docker-compose.gpu.prod.yml pull
docker compose --env-file .env -f docker-compose.gpu.prod.yml up -d
curl http://<gpu-host>:8880/health
```

## MinIO sync

```bash
# pull all voicepacks the tts-trainer fork has uploaded
curl -X POST http://<gpu-host>:8880/v1/voices/sync-from-minio
curl http://<gpu-host>:8880/v1/audio/voices
```

## Helm / k8s

`helm/` and `k8s/` mirror the omnivoice-tts shape. `helm/values.yaml`
exposes `env.ALLOW_LOCAL_VOICE_SAVING`, `env.MINIO_*`, and a
`persistence.voices` toggle that mounts a PVC at
`/app/api/src/voices/v1_0`.

## Image tags

GHCR `ghcr.io/autoeditor-video-or-audio/kokoro-tts-server`:

- `:vX.Y.Z-gpu` — pinned semver, NVIDIA CUDA 12.6 base.
- `:latest-gpu` — rolling pointer at the newest semver.

No `-flash` variant — Kokoro inference is small and flash-attn brings
no measurable win.

## License

Apache 2.0, preserved from upstream. See `NOTICE-fork.md` for the list
of changes layered on top.
