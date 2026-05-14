# kokoro-tts-server (fork)

Drop-in replacement for `remsky/Kokoro-FastAPI` with three operational
deltas that the nifty-star sequencer needs:

1. **`ALLOW_LOCAL_VOICE_SAVING=true` is the new default**, so
   `POST /v1/audio/voices/combine` actually returns 200 + the blended
   `.pt` blob instead of HTTP 403 `permission_denied`.
2. **`POST /v1/voices/save-combined`** — fork-only route that takes
   `{voices, name, overwrite}`, blends the base voicepacks with caller-
   supplied weights, and persists the resulting tensor as
   `<voices_dir>/<name>.pt`. The new voicepack is immediately visible
   in `GET /v1/audio/voices` and survives container restarts.
   Each `voices[]` entry is either `<bare_name>` (weight 1.0) or
   `<bare_name>(<weight>)`; weights are normalised to sum 1.0 before
   the tensor blend.
3. **`POST /v1/voices/sync-from-minio`** pulls every `*.pt` under
   `s3://${MINIO_BUCKET}/voicepacks/` into the local
   `/app/api/src/voices/v1_0/` folder and rebuilds the upstream voice
   cache. `POST /v1/voices/reload` rebuilds the cache without a
   sync. A lifespan hook runs an initial sync if
   `KOKORO_SYNC_ON_START=1`.

Everything else is upstream: `/v1/audio/speech`, `/v1/audio/voices`,
`/v1/audio/voices/combine`, `/v1/models`, etc. Upstream `api/src/` is
never patched — the additions live in `server_addons/` and `ENV`.

## Image flavours

GHCR `ghcr.io/autoeditor-video-or-audio/kokoro-tts-server` publishes two
image flavours per release tag:

| Tag                    | Base image                                          | When to use                                  |
|------------------------|-----------------------------------------------------|----------------------------------------------|
| `:vX.Y.Z-gpu`          | `nvcr.io/nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04` | NVIDIA host (CUDA 12.x driver installed)     |
| `:latest-gpu`          | rolling pointer to the newest `-gpu` semver         | GPU host, no version pinning                  |
| `:vX.Y.Z-cpu`          | `python:3.10-slim`                                  | CPU-only host (no NVIDIA hardware)            |
| `:latest-cpu`          | rolling pointer to the newest `-cpu` semver         | CPU host, no version pinning                  |

The CPU image is wall-clock slower per synthesis but runs on any x86_64
Linux host. Both flavours ship the same upstream `api/src/` + the same
`server_addons/` routes, so the HTTP contract is identical.

## Run on a GPU host

```bash
mkdir -p ~/works/services/kokoro-tts-server && cd $_
curl -O https://raw.githubusercontent.com/autoeditor-video-or-audio/kokoro-tts-server/master/docker-compose.gpu.prod.yml
curl -O https://raw.githubusercontent.com/autoeditor-video-or-audio/kokoro-tts-server/master/.env.example
cp .env.example .env       # edit MinIO creds + KOKORO_IMAGE_TAG=latest-gpu

# IMPORTANT: chown the host voices dir to container uid 1001 BEFORE the
# first start so the baked-voicepack seed step inside the entrypoint can
# write into the bind mount. Without this the container loops on
# 'Permission denied' / 'File not found: af_heart.pt'.
sudo mkdir -p ./voices && sudo chown -R 1001:1001 ./voices

# Free port 8880 if the upstream container was running here:
docker stop kokoro-fastapi-old 2>/dev/null || true
docker rm   kokoro-fastapi-old 2>/dev/null || true

docker compose --env-file .env -f docker-compose.gpu.prod.yml pull
docker compose --env-file .env -f docker-compose.gpu.prod.yml up -d
curl http://<gpu-host>:8880/health
```

## Run on a CPU host

```bash
mkdir -p ~/works/services/kokoro-tts-server && cd $_
curl -O https://raw.githubusercontent.com/autoeditor-video-or-audio/kokoro-tts-server/master/docker-compose.cpu.prod.yml
curl -O https://raw.githubusercontent.com/autoeditor-video-or-audio/kokoro-tts-server/master/.env.example
cp .env.example .env       # set KOKORO_IMAGE_TAG=latest-cpu

sudo mkdir -p ./voices && sudo chown -R 1001:1001 ./voices

docker compose --env-file .env -f docker-compose.cpu.prod.yml pull
docker compose --env-file .env -f docker-compose.cpu.prod.yml up -d
curl http://<cpu-host>:8880/health
```

## Persisting a weighted voice blend

```bash
# Save a weighted blend that the upstream /v1/audio/voices/combine
# route can't persist (upstream only streams the blob to a tempfile).
curl -X POST http://<host>:8880/v1/voices/save-combined \
  -H 'Content-Type: application/json' \
  -d '{
        "voices": ["pf_dora(0.7)", "pm_alex(0.3)"],
        "name":   "ptbr_warm",
        "overwrite": false
      }'
# -> {"name":"ptbr_warm","path":"/app/api/src/voices/v1_0/ptbr_warm.pt","base_voices":[...]}

curl http://<host>:8880/v1/audio/voices            # 'ptbr_warm' is listed

curl -X POST http://<host>:8880/v1/audio/speech \
  -H 'Content-Type: application/json' \
  -d '{"model":"kokoro","input":"Olá","voice":"ptbr_warm","response_format":"mp3"}' \
  --output sample.mp3
```

Validation:
- `name` must match `[A-Za-z0-9_-]{1,64}`.
- `voices[]` requires at least one entry; weights default to 1.0 when
  no `(...)` suffix is present; `weight_sum == 0` returns HTTP 400.
- `overwrite=false` (default) rejects an existing voicepack with HTTP 409.

## Pulling trained voicepacks from MinIO

```bash
# pull every voicepack the tts-trainer fork has uploaded
curl -X POST http://<host>:8880/v1/voices/sync-from-minio
curl http://<host>:8880/v1/audio/voices
```

## Helm / k8s

`helm/` and `k8s/` mirror the omnivoice-tts shape. `helm/values.yaml`
exposes `env.ALLOW_LOCAL_VOICE_SAVING`, `env.MINIO_*`, and a
`persistence.voices` toggle that mounts a PVC at
`/app/api/src/voices/v1_0`. The chart defaults to the `-gpu` image
flavour; override `image.tag` to `latest-cpu` (or a pinned `-cpu`
semver) for a CPU node pool.

## License

Apache 2.0, preserved from upstream. See `NOTICE-fork.md` for the list
of changes layered on top.
