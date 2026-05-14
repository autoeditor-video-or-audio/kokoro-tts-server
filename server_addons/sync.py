"""MinIO -> /app/api/src/voices/v1_0 sync for the kokoro-tts-server fork.

Pulls every `*.pt` voicepack under `s3://${MINIO_BUCKET}/voicepacks/`
into the local `Settings.voices_dir` (default
`/app/api/src/voices/v1_0/`). Sha256-idempotent: a voicepack whose
local digest matches the MinIO etag is skipped.
"""

from __future__ import annotations

import hashlib
import logging
import os
from datetime import timedelta
from pathlib import Path
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


def _require(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise RuntimeError(f"required env var {name} is empty")
    return val


MINIO_BUCKET = os.environ.get("MINIO_BUCKET", "tts-training")
MINIO_PREFIX = os.environ.get("MINIO_VOICEPACK_PREFIX", "voicepacks/")
MINIO_SECURE = os.environ.get("MINIO_SECURE", "false").lower() in ("1", "true", "yes")


def _client():
    from minio import Minio

    return Minio(
        _require("MINIO_ENDPOINT"),
        access_key=_require("MINIO_ACCESS_KEY"),
        secret_key=_require("MINIO_SECRET_KEY"),
        secure=MINIO_SECURE,
    )


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def list_remote_voicepacks() -> list[dict]:
    client = _client()
    out: list[dict] = []
    for obj in client.list_objects(MINIO_BUCKET, prefix=MINIO_PREFIX, recursive=True):
        key = obj.object_name
        if not key.endswith(".pt"):
            continue
        out.append(
            {
                "key": key,
                "name": Path(key).stem,
                "size": obj.size,
                "etag": (obj.etag or "").strip('"'),
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
            }
        )
    return out


def sync_voicepacks(target_dir: Path) -> dict:
    """Pull every remote voicepack into `target_dir`.

    Returns `{"synced":[<name>], "skipped":[<name>], "errors":[{name,error}]}`.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    client = _client()
    synced: list[str] = []
    skipped: list[str] = []
    errors: list[dict] = []
    for remote in list_remote_voicepacks():
        name = remote["name"]
        local_path = target_dir / f"{name}.pt"
        if local_path.exists() and remote["etag"]:
            try:
                local_hash = _sha256(local_path)
                # MinIO multipart uploads produce composite etags; only
                # single-part uploads compare cleanly. Fall back to size.
                if local_hash == remote["etag"] or local_path.stat().st_size == (remote["size"] or 0):
                    skipped.append(name)
                    continue
            except Exception:
                # If the local file is unreadable, force a re-download.
                pass
        try:
            client.fget_object(MINIO_BUCKET, remote["key"], str(local_path))
            synced.append(name)
            logger.info("synced voicepack %s (%.1f KB)", name, (remote["size"] or 0) / 1024)
        except Exception as exc:
            logger.exception("voicepack %s download failed", name)
            errors.append({"name": name, "error": str(exc)})
    return {"synced": synced, "skipped": skipped, "errors": errors}
