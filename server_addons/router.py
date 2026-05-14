"""FastAPI router for the kokoro-tts-server fork add-ons."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import List, Optional

import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .sync import sync_voicepacks

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/voices", tags=["voicepacks"])

_VALID_NAME = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")


class SaveCombinedRequest(BaseModel):
    voices: List[str] = Field(..., min_length=1, description="Base voicepack names to blend")
    name: str = Field(..., description="Filename (without .pt) to persist in voices_dir")
    overwrite: bool = Field(False, description="Allow overwriting an existing voicepack")


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


@router.post("/save-combined")
async def save_combined_voice(req: SaveCombinedRequest) -> dict:
    """Blend `voices` and persist the result as `<name>.pt` in voices_dir.

    Upstream `POST /v1/audio/voices/combine` returns the blended `.pt`
    as a download but writes it only to a tempfile. This fork-only
    endpoint keeps the same blend math but lands the tensor inside the
    voice manager's directory so it shows up in `GET /v1/audio/voices`
    and survives container restarts.
    """
    if not _VALID_NAME.match(req.name):
        raise HTTPException(
            status_code=400,
            detail="name must match [A-Za-z0-9_-]{1,64}",
        )
    target = _voices_dir() / f"{req.name}.pt"
    if target.exists() and not req.overwrite:
        raise HTTPException(
            status_code=409,
            detail=f"voicepack {req.name!r} already exists; pass overwrite=true to replace",
        )

    try:
        from api.src.services.tts_service import TTSService

        tts_service = await TTSService.create()
        available = set(await tts_service.list_voices())
    except Exception as exc:
        logger.exception("upstream tts service init failed")
        raise HTTPException(status_code=500, detail=f"tts service init: {exc}")

    missing = [v for v in req.voices if v.split("(")[0].strip() not in available]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"base voices not found: {missing}",
        )

    try:
        combined = await tts_service.combine_voices(voices=req.voices)
    except Exception as exc:
        logger.exception("combine_voices failed for %s", req.voices)
        raise HTTPException(status_code=500, detail=f"combine failed: {exc}")

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        torch.save(combined, target)
    except Exception as exc:
        logger.exception("torch.save voicepack failed")
        raise HTTPException(status_code=500, detail=f"persist failed: {exc}")

    await _reload_voice_cache()
    return {"name": req.name, "path": str(target), "base_voices": req.voices}


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
