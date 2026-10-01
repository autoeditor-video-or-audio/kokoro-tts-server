## MODIFIED Requirements

### Requirement: Inference Surface Inherited Verbatim
The fork SHALL serve every OpenAI-compatible route the upstream
`remsky/Kokoro-FastAPI` server exposes at release `v0.9.0`, with no
signature change.

#### Scenario: Upstream base release
- **WHEN** an operator inspects the fork's git history
- **THEN** upstream tag `v0.9.0` MUST be an ancestor of the fork's
  default branch
- **AND** `NOTICE-fork.md` MUST name `v0.9.0` as the upstream base

#### Scenario: Speech synthesis route
- **WHEN** the client posts `POST /v1/audio/speech` with body
  `{model, input, voice, response_format?, speed?}` (including
  blend expressions in the `voice` field)
- **THEN** the server MUST behave identically to the upstream
  `remsky/Kokoro-FastAPI` `v0.9.0` release of that route, including
  its input-length, pause and `volume_multiplier` limits

#### Scenario: Voice list route
- **WHEN** the client `GET`s `/v1/audio/voices`
- **THEN** the response MUST include every `.pt` file under
  `Settings.voices_dir` (default `/app/api/src/voices/v1_0/`)

#### Scenario: Voice combine route returns blob
- **WHEN** the client posts `POST /v1/audio/voices/combine` with a
  body of `Union[str, list[str]]`, including the weighted syntax
  `"voice1(2)+voice2(1)"`
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
