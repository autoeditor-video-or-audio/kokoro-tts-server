# kokoro-tts-server — Spec delta (CPU flavour)

## MODIFIED Requirements

### Requirement: Single-Flavour GHCR Image
The fork SHALL publish `:gpu` AND `:cpu` image flavours per release
tag, so operators can choose between a CUDA host and a slim Python
CPU host without changing the API contract.

#### Scenario: CI publishes both flavours on release
- **WHEN** the CI release job promotes a new semantic-release tag
  `vX.Y.Z`
- **THEN** GHCR MUST receive both
  `ghcr.io/autoeditor-video-or-audio/kokoro-tts-server:vX.Y.Z-gpu`
  AND `:vX.Y.Z-cpu`, plus the rolling `:latest-gpu` and `:latest-cpu`
  pointers
- **AND** no `:gpu-flash` flavour MUST be published (Kokoro inference
  does not benefit from flash-attn)

#### Scenario: Cleanup preserves both latest tags
- **WHEN** the `cleanup_ghcr` job runs after a release
- **THEN** it MUST preserve `latest-gpu` AND `latest-cpu` while
  keeping at least the 10 most recent versioned tags of either
  flavour

#### Scenario: CPU compose file pairs with `latest-cpu`
- **WHEN** the operator runs
  `docker compose --env-file .env -f docker-compose.cpu.prod.yml up -d`
  on a non-NVIDIA host
- **THEN** the compose definition MUST default
  `KOKORO_IMAGE_TAG=latest-cpu`, omit the `runtime: nvidia` and the
  `deploy.resources.reservations.devices` block, and still expose
  host port 8880 so vibetalker's `/api/tts/*` proxy works without
  edits

#### Scenario: HTTP contract is identical across flavours
- **WHEN** the client posts the same request to `/v1/audio/speech`,
  `/v1/audio/voices`, `/v1/audio/voices/combine`, `/v1/voices/save-combined`,
  or `/v1/voices/sync-from-minio` against the `-gpu` and `-cpu`
  containers
- **THEN** both MUST return the same status code and an equivalent
  response body (audio bytes MAY differ bit-for-bit due to device
  arithmetic, but format + length MUST match)
