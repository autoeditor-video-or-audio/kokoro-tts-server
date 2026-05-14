# Tasks — kokoro-tts-server fork

## 1. Repo scaffolding
- [x] 1.1 Fork `remsky/Kokoro-FastAPI` to
      `autoeditor-video-or-audio/kokoro-tts-server`
- [x] 1.2 Clone to `/home/vagrant/mvp/editaudiotomovie/kokoro-tts-server`
- [x] 1.3 `openspec init . --tools claude`
- [x] 1.4 Write proposal / design / this tasks file / capability spec

## 2. server_addons
- [ ] 2.1 `server_addons/__init__.py`
- [ ] 2.2 `server_addons/sync.py` — MinIO client, list, fetch, sha256
- [ ] 2.3 `server_addons/router.py` — `/v1/voices/sync-from-minio` +
      `/v1/voices/reload`
- [ ] 2.4 `server_addons/main.py` — import upstream app + include
      router + optional lifespan startup sync

## 3. Docker
- [ ] 3.1 `Dockerfile.gpu` (layer on top of upstream
      `docker/gpu/Dockerfile` base; install `minio` SDK, copy
      `server_addons/`, switch CMD to `server_addons.main:app`)
- [ ] 3.2 `docker-compose.gpu.prod.yml` (host port 8880, MinIO env,
      voices/ bind mount)
- [ ] 3.3 `.env.example` documenting `ALLOW_LOCAL_VOICE_SAVING`,
      `KOKORO_SYNC_ON_START`, `MINIO_*`

## 4. Helm / k8s / CI parity
- [ ] 4.1 `helm/{Chart.yaml,values.yaml,templates/*}` cloned from
      omnivoice-tts and renamed
- [ ] 4.2 `k8s/{configmap,deployment,pvc,service}.yaml` ditto
- [ ] 4.3 `.github/workflows/ci.yml` (semantic-release + single `gpu`
      matrix publishing to GHCR)
- [ ] 4.4 `.releaserc.json`, `NOTICE-fork.md`, `README-fork.md`

## 5. Verification
- [ ] 5.1 `docker build -f Dockerfile.gpu .` smoke-builds locally (or
      via CI)
- [ ] 5.2 Push `main`; CI publishes `:v1.0.0-gpu` + `:latest-gpu`
- [ ] 5.3 Pull + run on host `.4`. `curl /health` 200,
      `curl /v1/audio/voices` lists the upstream defaults
- [ ] 5.4 From vibetalker UI, retry the Blender modal's *Save as
      voicepack* → returns 200
- [ ] 5.5 `curl -X POST /v1/voices/sync-from-minio` returns
      `{synced:[…], skipped:[…]}` matching the bucket contents
- [ ] 5.6 `curl /v1/audio/voices` lists the freshly synced voicepacks
