"""FastAPI router for the kokoro-tts-server fork add-ons."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

from .sync import sync_voicepacks

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/voices", tags=["voicepacks"])


def _voices_dir() -> Path:
    # Defer the upstream import so this module is importable for unit
    # tests without the full settings tree resolved.
    from api.src.core.config import settings

    return Path(settings.voices_dir)


@router.post("/sync-from-minio")
async def sync_from_minio() -> dict:
    """Pull every voicepack from MinIO into the local voices_dir."""
    try:
        result = sync_voicepacks(_voices_dir())
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        logger.exception("MinIO sync failed")
        raise HTTPException(status_code=500, detail=str(exc))
    # Flush the upstream voice cache so a follow-up GET /v1/audio/voices
    # picks up any new files immediately.
    await _reload_voice_cache()
    return result


@router.post("/reload")
async def reload_voices() -> dict:
    """Clear the upstream voice-manager cache + re-list directory."""
    await _reload_voice_cache()
    from api.src.inference.voice_manager import get_manager

    manager = await get_manager()
    voices = await manager.list_voices()
    return {"voices": voices, "count": len(voices)}


async def _reload_voice_cache() -> None:
    """Drop cached tensors so the next load_voice() re-reads disk."""
    try:
        from api.src.inference.voice_manager import get_manager

        manager = await get_manager()
        # The upstream manager stores loaded tensors keyed by voice
        # name on `_voices`. Clearing the dict forces a re-read on the
        # next request. `list_voices()` itself goes through
        # `paths.list_voices()` which scans the directory, so no cache
        # invalidation is needed there.
        if hasattr(manager, "_voices") and isinstance(manager._voices, dict):
            manager._voices.clear()
    except Exception:
        logger.exception("voice cache reload failed (continuing)")
