# Add CPU flavour to kokoro-tts-server

## Why

The upstream `remsky/Kokoro-FastAPI` ships both a GPU and a CPU
Dockerfile. Our fork currently only builds and publishes the `-gpu`
image, which forces every operator onto an NVIDIA host even when low-
latency throughput is not a requirement (e.g. dev boxes, lightweight
preview environments, CI smoke tests). The fork should publish both
flavours so the choice of host is configuration, not a binary.

## What Changes

- Add `Dockerfile.cpu` mirroring the existing `Dockerfile.gpu` 1:1 on
  the fork-layer changes (`server_addons/`, baked-voicepack seed,
  `ALLOW_LOCAL_VOICE_SAVING=true` default, `minio` SDK, rewritten
  entrypoint pointing at `server_addons.main:app`).
- Add `docker-compose.cpu.prod.yml` with the same env + bind-mount
  surface as the GPU compose, minus the NVIDIA runtime block.
- Extend `.github/workflows/ci.yml` with a `publish_cpu` job (sibling
  to `publish_gpu`) that pushes `:vX.Y.Z-cpu` and `:latest-cpu`. Wire
  `deploy` and `cleanup_ghcr` to wait on both publish jobs and
  preserve both `latest-` tags.
- Update `.env.example` to document the `KOKORO_IMAGE_TAG=latest-{gpu,cpu}`
  switch and remind operators which compose file pairs with each tag.
- Update `README-fork.md` + `NOTICE-fork.md` to describe both flavours
  and call out the bind-mount chown caveat (`chown -R 1001:1001 ./voices`)
  that surfaced during the GPU deploy.

## Impact

- Affected specs: `kokoro-tts-server` (add Requirement on dual image
  flavours)
- Affected code: `Dockerfile.cpu` (new), `docker-compose.cpu.prod.yml`
  (new), `.github/workflows/ci.yml`, `.env.example`,
  `README-fork.md`, `NOTICE-fork.md`.
- No runtime change to the existing GPU image; CPU image is additive.
