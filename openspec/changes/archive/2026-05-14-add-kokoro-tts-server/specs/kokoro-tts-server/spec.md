# kokoro-tts-server — Spec delta (ADDED capability)

## ADDED Requirements

### Requirement: Inference Surface Inherited Verbatim
The fork SHALL serve every OpenAI-compatible route the upstream
`remsky/Kokoro-FastAPI` server exposes, with no signature change.

#### Scenario: Speech synthesis route
- **WHEN** the client posts `POST /v1/audio/speech` with body
  `{model, input, voice, response_format?, speed?}` (including
  blend expressions in the `voice` field)
- **THEN** the server MUST behave identically to the upstream
  `remsky/Kokoro-FastAPI` release of that route

#### Scenario: Voice list route
- **WHEN** the client `GET`s `/v1/audio/voices`
- **THEN** the response MUST include every `.pt` file under
  `Settings.voices_dir` (default `/app/api/src/voices/v1_0/`)

#### Scenario: Voice combine route returns blob
- **WHEN** the client posts `POST /v1/audio/voices/combine` with a
  body of `Union[str, list[str]]`
- **THEN** the server MUST stream the combined voicepack `.pt` back
  as a `FileResponse` (upstream contract, preserved verbatim) with
  HTTP 200 — the fork enables the upstream permission gate by default
  so the route no longer 403s

#### Scenario: Persisted weighted blend via fork-only save route
- **WHEN** the client posts
  `POST /v1/voices/save-combined` with body
  `{"voices": ["pf_dora(0.7)", "pm_alex(0.3)"], "name": "my_blend", "overwrite": false}`
- **THEN** the server MUST parse each entry as `<name>` or
  `<name>(<weight>)` (bare names default to weight 1.0), normalise
  the weights to sum 1.0, and compute the weighted-sum tensor of
  the loaded voicepacks
- **AND** persist the resulting tensor as `<voices_dir>/<name>.pt`
- **AND** flush the voice-manager cache so a follow-up
  `GET /v1/audio/voices` lists the new voicepack
- **AND** return `{"name": "<name>", "path": "<absolute>", "base_voices": [...]}`
- **AND** reject `weight_sum == 0` with HTTP 400 and unknown base
  voices with HTTP 400

### Requirement: Allow-Local-Voice-Saving Default Enabled
The fork SHALL flip the default of `Settings.allow_local_voice_saving`
to `True` via environment variable so the published image works
out of the box for the nifty-star clone-and-blend workflow.

#### Scenario: Default container env
- **WHEN** the container starts without any operator override
- **THEN** `Settings.allow_local_voice_saving` MUST evaluate to
  `True`
- **AND** `POST /v1/audio/voices/combine` MUST return 200 instead of
  HTTP 403 `Local voice saving is disabled`

### Requirement: MinIO Voicepack Sync
The fork SHALL expose `POST /v1/voices/sync-from-minio` to pull
voicepacks produced by the sibling `tts-trainer` service into the
inference container's voice directory.

#### Scenario: Sync pulls new voicepacks
- **WHEN** the client posts `POST /v1/voices/sync-from-minio`
- **THEN** the server MUST list every object under
  `s3://${MINIO_BUCKET}/voicepacks/` (default bucket `tts-training`)
- **AND** download each `*.pt` whose local sha256 differs from the
  MinIO etag into `Settings.voices_dir`
- **AND** respond with
  `{"synced":[<voicepack_names>], "skipped":[<voicepack_names>]}`

#### Scenario: Reload after sync
- **WHEN** the client posts `POST /v1/voices/reload`
- **THEN** the upstream voice-manager cache MUST be cleared so the
  next `GET /v1/audio/voices` enumerates the directory fresh from
  disk (any voicepacks added since startup become visible)

#### Scenario: Optional startup sync
- **WHEN** the container starts with env `KOKORO_SYNC_ON_START=1`
- **THEN** the lifespan hook MUST run the sync routine once before
  serving the first request
- **AND** any sync error MUST NOT block startup (log + continue)

### Requirement: GPU-Only Deployment with NVIDIA Runtime
The fork's prod compose definition SHALL request a single nvidia GPU.

#### Scenario: docker-compose targets nvidia
- **WHEN** the operator runs
  `docker compose --env-file .env -f docker-compose.gpu.prod.yml up -d`
- **THEN** the compose definition MUST request a single nvidia GPU
  via `deploy.resources.reservations.devices` and export
  `NVIDIA_VISIBLE_DEVICES=all` plus
  `NVIDIA_DRIVER_CAPABILITIES=compute,utility`
- **AND** the host port MUST default to `8880` so vibetalker's
  `/api/tts/*` proxy keeps working without an env edit

### Requirement: Single-Flavour GHCR Image
The fork SHALL publish a single `:gpu` image flavour per release tag.

#### Scenario: CI publish on release
- **WHEN** the CI release job promotes a new semantic-release tag
  `vX.Y.Z`
- **THEN** GHCR MUST receive
  `ghcr.io/autoeditor-video-or-audio/kokoro-tts-server:vX.Y.Z-gpu`
  and `:latest-gpu`
- **AND** no `:gpu-flash` flavour MUST be published (Kokoro inference
  does not benefit from flash-attn)

#### Scenario: Cleanup preserves latest tag
- **WHEN** the `cleanup_ghcr` job runs after a release
- **THEN** it MUST preserve the `latest-gpu` tag while keeping at
  least the 10 most recent versioned tags
