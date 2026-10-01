import shutil
from pathlib import Path

import pytest
import torch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server_addons import router as addons

BAKED = Path(__file__).resolve().parents[2] / "api/src/voices/v1_0"
BASE_VOICES = ("pf_dora", "pm_alex")


class FakeVoiceManager:
    """Reads voicepacks from a temp dir the same way the upstream manager does."""

    def __init__(self, voices_dir: Path):
        self.voices_dir = voices_dir
        self._voices: dict = {}

    async def list_voices(self):
        return sorted(p.stem for p in self.voices_dir.glob("*.pt"))

    async def load_voice(self, name):
        voice = torch.load(
            self.voices_dir / f"{name}.pt", map_location="cpu", weights_only=True
        )
        self._voices[name] = voice
        return voice


@pytest.fixture
def voices_dir(tmp_path):
    for name in BASE_VOICES:
        shutil.copy(BAKED / f"{name}.pt", tmp_path / f"{name}.pt")
    return tmp_path


@pytest.fixture
def manager(voices_dir, monkeypatch):
    fake = FakeVoiceManager(voices_dir)

    async def get_manager():
        return fake

    monkeypatch.setattr("api.src.inference.voice_manager.get_manager", get_manager)
    monkeypatch.setattr(addons, "_voices_dir", lambda: voices_dir)
    return fake


@pytest.fixture
def client(manager):
    app = FastAPI()
    app.include_router(addons.router)
    return TestClient(app)
