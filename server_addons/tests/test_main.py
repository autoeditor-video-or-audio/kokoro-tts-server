from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient

from server_addons import main


@pytest.fixture
def boot(monkeypatch):
    """Start the real fork app with the upstream model warmup stubbed out."""
    events = []

    @asynccontextmanager
    async def upstream_lifespan(app):
        events.append("upstream")
        yield

    monkeypatch.setattr(main, "_upstream_lifespan", upstream_lifespan)

    def fake_sync(target):
        events.append("sync")
        return {"synced": [], "skipped": [], "errors": []}

    def run():
        with TestClient(main.app):
            pass
        return events

    monkeypatch.setattr(main, "sync_voicepacks", fake_sync)
    return run


@pytest.mark.parametrize("flag", ["1", "true", "YES"])
def test_sync_on_start_runs_after_upstream_lifespan(boot, monkeypatch, flag):
    monkeypatch.setenv("KOKORO_SYNC_ON_START", flag)

    assert boot() == ["upstream", "sync"]


@pytest.mark.parametrize("flag", [None, "0", "false", ""])
def test_sync_on_start_disabled(boot, monkeypatch, flag):
    if flag is None:
        monkeypatch.delenv("KOKORO_SYNC_ON_START", raising=False)
    else:
        monkeypatch.setenv("KOKORO_SYNC_ON_START", flag)

    assert boot() == ["upstream"]


def test_sync_failure_does_not_block_startup(boot, monkeypatch):
    monkeypatch.setenv("KOKORO_SYNC_ON_START", "1")

    def broken(target):
        raise RuntimeError("required env var MINIO_ENDPOINT is empty")

    monkeypatch.setattr(main, "sync_voicepacks", broken)

    assert boot() == ["upstream"]


def test_fork_routes_are_mounted_on_upstream_app():
    paths = set(main.app.openapi()["paths"])

    assert {
        "/v1/voices/save-combined",
        "/v1/voices/sync-from-minio",
        "/v1/voices/reload",
    } <= paths
    assert "/v1/audio/speech" in paths
