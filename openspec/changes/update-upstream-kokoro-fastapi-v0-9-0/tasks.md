# Tasks

## 1. Upstream merge

- [x] 1.1 Fetch upstream tag `v0.9.0` and merge it into the branch with a
      merge commit (no squash, no cherry-pick)
- [x] 1.2 Resolve `.github/workflows/ci.yml` in favour of the fork
- [x] 1.3 Resolve `AGENTS.md` as upstream content plus the fork's
      OpenSpec managed block
- [x] 1.4 Stop upstream-only workflows (`test_client_image.yml`) from
      publishing images under the fork

## 2. Fork Dockerfiles

- [x] 2.1 Rebuild `Dockerfile.gpu` on upstream `docker/gpu/Dockerfile.optimized`
      with the fork deltas
- [x] 2.2 Rebuild `Dockerfile.cpu` on upstream `docker/cpu/Dockerfile.optimized`
      with the fork deltas
- [x] 2.3 Entrypoint seeds `voices_dir` from `/app/voices-baked`, keeps the
      optional model download, honours `HOST`/`PORT` and launches
      `server_addons.main:app`

## 3. server_addons

- [x] 3.1 Re-check the integration points against v0.9.0 (`get_manager`,
      `load_voice`, `list_voices`, `_voices`, `settings.voices_dir`)
- [x] 3.2 Decide whether `save-combined` reuses the upstream blend helpers
      or keeps its own math, and record the decision in `design.md`
- [x] 3.3 Add tests for `save-combined`, `reload` and `sync-from-minio`
      (MinIO mocked)
- [x] 3.4 Chain the `KOKORO_SYNC_ON_START` hook into the upstream lifespan
      (`on_event` handlers never ran under `lifespan=`)

## 4. Docs

- [x] 4.1 `NOTICE-fork.md` and `README-fork.md` state the upstream base
      version
- [x] 4.2 `.env.example` and `docs/generation-parameters.md` document the
      upstream env knobs relevant to fork operators

## 5. Validation

- [ ] 5.1 `uv run pytest` green on the merged tree
- [ ] 5.2 `docker build` of both Dockerfiles succeeds
- [ ] 5.3 CPU container: `/health` 200, `/v1/audio/voices` lists baked
      voices, `save-combined` persists, weighted `/v1/audio/speech` returns
      audio
- [ ] 5.4 GPU container: `/health` 200 and a speech request returns audio
- [ ] 5.5 `openspec validate update-upstream-kokoro-fastapi-v0-9-0 --strict`
