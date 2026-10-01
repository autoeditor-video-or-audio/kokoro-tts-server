# Sync the fork with upstream remsky/Kokoro-FastAPI v0.9.0

## Why

The fork's last upstream merge is `75a98b6` (2026-05-11), which predates
upstream `v0.3.0`. Upstream has since released up to `v0.9.0`
(2026-09-10), 194 commits ahead. The gap includes security fixes for a
network-exposed server: a ReDoS in the text normalizer and a path
traversal in `_find_file` (v0.7.0), the `starlette>=1.3.1` CVE bump
(v0.7.2), and input/pause/`volume_multiplier` caps against OOM
(v0.8.1, GHSA-f64g-9jmv-pm22). It also includes audio correctness fixes
(UAX #29 sentence segmentation, stream cleanup on client disconnect,
FLAC/WAV tail fixes). Tracked in issue #1.

## What Changes

- Merge upstream tag `v0.9.0` into the fork. Upstream `api/src/` stays
  unpatched.
- Resolve the two text conflicts: keep the fork's
  `.github/workflows/ci.yml` (semantic-release plus dual GHCR publish),
  and merge upstream `AGENTS.md` with the fork's OpenSpec managed block.
- Rebuild `Dockerfile.gpu` and `Dockerfile.cpu` on upstream's v0.9.0
  multi-stage `docker/{gpu,cpu}/Dockerfile.optimized`, because upstream
  deleted the single-stage `docker/{gpu,cpu}/Dockerfile` the fork layers
  mirrored. This brings in Python 3.12 (uv-managed), `uv sync --frozen`
  against the upstream `uv.lock`, and bytecode compilation. The fork
  deltas stay: `minio` SDK, `server_addons/`, baked-voicepack staging
  plus seed, `ALLOW_LOCAL_VOICE_SAVING=true`, and an entrypoint that
  launches `server_addons.main:app` and honours `HOST`/`PORT` like
  upstream.
- Keep upstream-only workflows from publishing under the fork's name:
  `test_client_image.yml` pushes on `master` to `ghcr.io/${OWNER}` with
  a `remsky` fallback.
- Add tests for `server_addons` (none exist today).
- Document the upstream base version and the new upstream env knobs that
  affect fork operators.

## Impact

- Affected specs: `kokoro-tts-server`. MODIFIED `Inference Surface
  Inherited Verbatim` pins the inherited surface to upstream `v0.9.0`.
- Affected code: everything under upstream ownership (`api/`, `web/`,
  `docker/`, `pyproject.toml`, `uv.lock`, `.python-version`), plus the
  fork's `Dockerfile.gpu`, `Dockerfile.cpu`, `AGENTS.md`,
  `.github/workflows/`, `server_addons/` tests, `.env.example`,
  `docs/generation-parameters.md`, `NOTICE-fork.md` and `README-fork.md`.
- The HTTP contract of the fork-only routes is unchanged. Upstream
  normalizer and segmentation changes can alter the generated audio for
  the same input text.
- Independent of the active change `add-kokoro-tts-server-cpu-flavour`,
  which modifies a different requirement (`Single-Flavour GHCR Image`).
