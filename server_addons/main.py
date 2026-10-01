"""Entrypoint module: imports the upstream FastAPI app and mounts addons.

The Docker CMD points uvicorn at `server_addons.main:app` instead of the
upstream `api.src.main:app`. Everything upstream still serves; we just
include an extra router and (optionally) run a MinIO sync on startup,
chained after the upstream lifespan.
"""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager

# Importing the upstream module also runs its top-level `app = FastAPI(...)`
# constructor and registers all of its routers + middleware + lifespan.
from api.src.main import app
from server_addons.router import router as addons_router
from server_addons.sync import sync_voicepacks

logger = logging.getLogger(__name__)

app.include_router(addons_router)


async def _sync_on_start() -> None:
    """If KOKORO_SYNC_ON_START is truthy, pull voicepacks from MinIO."""
    if os.environ.get("KOKORO_SYNC_ON_START", "").lower() not in ("1", "true", "yes"):
        return
    try:
        from pathlib import Path

        from api.src.core.config import settings

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, lambda: sync_voicepacks(Path(settings.voices_dir))
        )
        logger.info(
            "startup sync: synced=%d skipped=%d errors=%d",
            len(result.get("synced", [])),
            len(result.get("skipped", [])),
            len(result.get("errors", [])),
        )
    except Exception:
        # Never block startup on a sync failure — log and continue.
        logger.exception("startup MinIO sync failed; continuing without it")


# Upstream passes `lifespan=` to FastAPI, which makes Starlette skip
# `@app.on_event("startup")` handlers, so the sync is chained into the
# upstream lifespan instead.
_upstream_lifespan = app.router.lifespan_context


@asynccontextmanager
async def _lifespan(application):
    async with _upstream_lifespan(application) as state:
        await _sync_on_start()
        yield state


app.router.lifespan_context = _lifespan
