# Tasks

## 1. Dockerfile.cpu

- [x] 1.1 Mirror `Dockerfile.gpu` on a `python:3.10-slim` base
- [x] 1.2 Install Rust under appuser so sudachipy / pyopenjtalk-plus build
- [x] 1.3 `uv sync --extra cpu --no-cache` (CPU PyTorch index)
- [x] 1.4 Apply the same baked-voicepack staging + entrypoint rewrite
      as `Dockerfile.gpu`
- [x] 1.5 ENV defaults: `DEVICE=cpu`, `USE_GPU=false`,
      `ALLOW_LOCAL_VOICE_SAVING=true`, `MINIO_*`

## 2. docker-compose.cpu.prod.yml

- [x] 2.1 Mirror the GPU compose surface (ports, env, bind mount,
      healthcheck) minus the NVIDIA runtime block
- [x] 2.2 Default `KOKORO_IMAGE_TAG=latest-cpu`
- [x] 2.3 Document `chown -R 1001:1001 ./voices` requirement inline

## 3. CI matrix

- [x] 3.1 Add `publish_cpu` job sibling to `publish_gpu`, pushing
      `:vX.Y.Z-cpu` + `:latest-cpu`
- [x] 3.2 `deploy` job waits on both publish jobs
- [x] 3.3 `cleanup_ghcr` waits on both publish jobs and preserves
      `^latest-(gpu|cpu)$`

## 4. Docs

- [x] 4.1 README-fork.md describes both flavours, both compose files,
      and the bind-mount chown caveat
- [x] 4.2 NOTICE-fork.md lists the new save-combined route, the dual
      Dockerfile, and the dual GHCR tags
- [x] 4.3 .env.example documents the KOKORO_IMAGE_TAG=latest-{gpu,cpu}
      switch

## 5. Verification (after CI green)

- [ ] 5.1 Pull `:latest-cpu` on a non-NVIDIA host, `docker compose up -d`,
      `/health` 200
- [ ] 5.2 `POST /v1/voices/save-combined` returns 200 + persists voicepack
- [ ] 5.3 Synth a short PT-BR line with the saved voice; audio plays
