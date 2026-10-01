# Generation parameters (kokoro-tts-server)

Parameters accepted by `POST /v1/audio/speech`. Mirrors the upstream
`remsky/Kokoro-FastAPI` contract; fork only adds env defaults +
`POST /v1/voices/save-combined` for persisting blends. Sibling fork
omnivoice-tts has its own param set documented at
[`omnivoice-tts/docs/generation-parameters.md`](https://github.com/autoeditor-video-or-audio/omnivoice-tts/blob/master/docs/generation-parameters.md);
the cross-provider mapping the nifty-star sequencer uses is in
`vibetalker/docs/generation-parameters.md`.

## Input

| Parameter | Type | Default | Description |
|---|---|---|---|
| `model` | str | `"kokoro"` | Accepts `tts-1`, `tts-1-hd`, `kokoro`, `gpt-4o-mini-tts`. |
| `input` | str | — | Text to synthesize. |
| `voice` | str | `"af_heart"` | Base voice id, persisted blend name, or inline blend expression `"pf_dora(0.7)+pm_alex(0.3)"`. |
| `lang_code` | str? | first letter of `voice` | Override language hint (e.g. `"p"` for PT-BR). |

## Output

| Parameter | Type | Default | Description |
|---|---|---|---|
| `response_format` | enum | `"mp3"` | `mp3`, `opus`, `flac`, `wav`, `pcm`. AAC currently unsupported. PCM is raw 16-bit, no header. |
| `download_format` | enum? | (mirrors `response_format`) | Optional final-download format if different from the streamed format. |
| `stream` | bool | `true` | Stream audio chunk-by-chunk (sentence boundaries) for OpenAI compatibility. Set `false` to receive the full file at once. |
| `return_download_link` | bool | `false` | Surface the rendered file path in the `X-Download-Path` response header (post-stream). |

## Speech control

| Parameter | Type | Default | Description |
|---|---|---|---|
| `speed` | float | `1.0` | Speaking rate (0.25–4.0). > 1 faster, < 1 slower. |
| `volume_multiplier` | float | `1.0` | Linear gain on the output samples. |
| `normalization_options` | object | `{}` (defaults) | Knobs for the upstream text-normaliser (URL stripping, currency, dates, …). See `api/src/structures/normalization.py`. |

## Voice blending (fork-only persistence)

`POST /v1/voices/save-combined`:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `voices` | list[str] | — | Each entry is `<base_voice>` (weight 1.0) or `<base_voice>(<weight>)`. Weights are normalised to sum 1.0 before tensor blend. |
| `name` | str | — | Filename (without `.pt`) under `voices_dir`. Must match `[A-Za-z0-9_-]{1,64}`. |
| `overwrite` | bool | `false` | Allow replacing an existing voicepack. |

The persisted `.pt` is immediately listed by `GET /v1/audio/voices`
and survives container restarts.

## MinIO sync

`POST /v1/voices/sync-from-minio`: pulls every `*.pt` under
`s3://${MINIO_BUCKET}/voicepacks/` into `voices_dir` (idempotent;
sha256 vs MinIO etag).

`POST /v1/voices/reload`: flushes the upstream voice-manager cache
without a sync.

## Defaults you can override at the container level

| ENV var | Default | Effect |
|---|---|---|
| `ALLOW_LOCAL_VOICE_SAVING` | `true` (fork default) | Gate for `/v1/audio/voices/combine` + `/v1/voices/save-combined`. |
| `KOKORO_SYNC_ON_START` | `0` | If `1`/`true`/`yes`, lifespan hook runs MinIO sync once at boot. |
| `MINIO_ENDPOINT`, `MINIO_BUCKET`, `MINIO_VOICEPACK_PREFIX`, `MINIO_SECURE`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` | see `.env.example` | MinIO connection config used by sync + lifespan hook. |

Upstream `v0.9.0` settings that change what a fork operator sees. All
default to the upstream value; the fork does not override them.

| ENV var | Default | Effect |
|---|---|---|
| `ENABLE_DEBUG_ENDPOINTS` | `false` | `/debug/*` introspection routes are off unless enabled (upstream v0.6.0). |
| `ALLOW_DEV_UNLOAD` | `false` | Exposes `/dev/model`, `POST /dev/unload`, `POST /dev/reload`. |
| `MODEL_AUTO_UNLOAD_TIMEOUT_SECONDS` | `0` | Idle seconds before the model leaves VRAM; `0` disables. |
| `ENABLE_INNO_TUNER` | `false` | Exposes `POST /dev/tune` (voice-clone tuner). |
| `ENABLE_SSML` / `ENABLE_VOICE_TAGS` | `true` | Kill switches for SSML and inline `[voice:...]` multi-speaker parsing. |
| `MAX_INPUT_LENGTH` | `1000000` | Characters per speech request. |
| `MAX_PAUSE_DURATION_S` / `MAX_TOTAL_PAUSE_S` | `60` / `300` | Caps on requested silence per pause and per request. |
