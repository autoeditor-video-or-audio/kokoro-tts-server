import pytest
import torch

from server_addons import router as addons


def test_save_combined_persists_normalised_weighted_blend(client, manager, voices_dir):
    resp = client.post(
        "/v1/voices/save-combined",
        json={"voices": ["pf_dora(0.7)", "pm_alex(0.3)"], "name": "ptbr_warm"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "ptbr_warm"
    assert body["base_voices"] == ["pf_dora(0.7)", "pm_alex(0.3)"]

    saved = torch.load(voices_dir / "ptbr_warm.pt", weights_only=True)
    dora = torch.load(voices_dir / "pf_dora.pt", weights_only=True)
    alex = torch.load(voices_dir / "pm_alex.pt", weights_only=True)
    assert torch.allclose(saved, dora * 0.7 + alex * 0.3)
    assert manager._voices == {}


def test_save_combined_unweighted_entries_default_to_equal_weights(client, voices_dir):
    resp = client.post(
        "/v1/voices/save-combined",
        json={"voices": ["pf_dora", "pm_alex"], "name": "even"},
    )

    assert resp.status_code == 200
    saved = torch.load(voices_dir / "even.pt", weights_only=True)
    dora = torch.load(voices_dir / "pf_dora.pt", weights_only=True)
    alex = torch.load(voices_dir / "pm_alex.pt", weights_only=True)
    assert torch.allclose(saved, (dora + alex) / 2)


@pytest.mark.parametrize("name", ["../escape", "with space", "", "x" * 65, "dot.name"])
def test_save_combined_rejects_invalid_name(client, voices_dir, name):
    resp = client.post(
        "/v1/voices/save-combined", json={"voices": ["pf_dora"], "name": name}
    )

    assert resp.status_code == 400
    assert sorted(p.name for p in voices_dir.iterdir()) == ["pf_dora.pt", "pm_alex.pt"]


def test_save_combined_rejects_unknown_base_voice(client):
    resp = client.post(
        "/v1/voices/save-combined",
        json={"voices": ["pf_dora", "zz_ghost"], "name": "blend"},
    )

    assert resp.status_code == 400
    assert "zz_ghost" in resp.json()["detail"]


@pytest.mark.parametrize("entry", ["pf_dora(abc)", "pf_dora(1", "pf/dora"])
def test_save_combined_rejects_malformed_entry(client, entry):
    resp = client.post(
        "/v1/voices/save-combined", json={"voices": [entry], "name": "blend"}
    )

    assert resp.status_code == 400


def test_save_combined_rejects_zero_weight_sum(client, voices_dir):
    resp = client.post(
        "/v1/voices/save-combined",
        json={"voices": ["pf_dora(1)", "pm_alex(-1)"], "name": "zero"},
    )

    assert resp.status_code == 400
    assert not (voices_dir / "zero.pt").exists()


def test_save_combined_rejects_empty_voice_list(client):
    resp = client.post("/v1/voices/save-combined", json={"voices": [], "name": "blend"})

    assert resp.status_code == 422


def test_save_combined_conflict_without_overwrite_keeps_existing_file(
    client, voices_dir
):
    original = (voices_dir / "pf_dora.pt").read_bytes()

    resp = client.post(
        "/v1/voices/save-combined", json={"voices": ["pm_alex"], "name": "pf_dora"}
    )

    assert resp.status_code == 409
    assert (voices_dir / "pf_dora.pt").read_bytes() == original


def test_save_combined_overwrite_replaces_existing_file(client, voices_dir):
    client.post(
        "/v1/voices/save-combined", json={"voices": ["pf_dora"], "name": "blend"}
    )

    resp = client.post(
        "/v1/voices/save-combined",
        json={"voices": ["pm_alex"], "name": "blend", "overwrite": True},
    )

    assert resp.status_code == 200
    saved = torch.load(voices_dir / "blend.pt", weights_only=True)
    alex = torch.load(voices_dir / "pm_alex.pt", weights_only=True)
    assert torch.allclose(saved, alex)


def test_saved_blend_is_listed_by_reload(client):
    client.post(
        "/v1/voices/save-combined", json={"voices": ["pf_dora"], "name": "blend"}
    )

    resp = client.post("/v1/voices/reload")

    assert resp.status_code == 200
    assert resp.json() == {"voices": ["blend", "pf_dora", "pm_alex"], "count": 3}


def test_reload_clears_cached_tensors(client, manager):
    manager._voices["pf_dora"] = torch.zeros(1)

    client.post("/v1/voices/reload")

    assert manager._voices == {}


def test_sync_from_minio_returns_result_and_flushes_cache(client, manager, monkeypatch):
    result = {"synced": ["trained"], "skipped": ["pf_dora"], "errors": []}
    monkeypatch.setattr(addons, "sync_voicepacks", lambda target: result)
    manager._voices["pf_dora"] = torch.zeros(1)

    resp = client.post("/v1/voices/sync-from-minio")

    assert resp.status_code == 200
    assert resp.json() == result
    assert manager._voices == {}


def test_sync_from_minio_without_credentials_is_503(client, monkeypatch):
    for var in ("MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY"):
        monkeypatch.delenv(var, raising=False)

    resp = client.post("/v1/voices/sync-from-minio")

    assert resp.status_code == 503
    assert "MINIO_ENDPOINT" in resp.json()["detail"]
