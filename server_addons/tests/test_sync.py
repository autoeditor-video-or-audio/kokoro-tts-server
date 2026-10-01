import hashlib
from types import SimpleNamespace

from server_addons import sync


class FakeMinio:
    def __init__(self, objects, fail=()):
        self.objects = objects
        self.fail = set(fail)
        self.downloads = []

    def list_objects(self, bucket, prefix, recursive):
        for key, data in self.objects.items():
            yield SimpleNamespace(
                object_name=key,
                size=len(data),
                etag=f'"{hashlib.sha256(data).hexdigest()}"',
                last_modified=None,
            )

    def fget_object(self, bucket, key, path):
        if key in self.fail:
            raise OSError("connection reset")
        self.downloads.append(key)
        with open(path, "wb") as fh:
            fh.write(self.objects[key])


def test_sync_downloads_new_skips_identical_and_reports_failures(tmp_path, monkeypatch):
    (tmp_path / "same.pt").write_bytes(b"same-bytes")
    fake = FakeMinio(
        {
            "voicepacks/new.pt": b"new-bytes",
            "voicepacks/same.pt": b"same-bytes",
            "voicepacks/broken.pt": b"broken-bytes",
            "voicepacks/readme.txt": b"not a voicepack",
        },
        fail={"voicepacks/broken.pt"},
    )
    monkeypatch.setattr(sync, "_client", lambda: fake)

    result = sync.sync_voicepacks(tmp_path)

    assert result["synced"] == ["new"]
    assert result["skipped"] == ["same"]
    assert [e["name"] for e in result["errors"]] == ["broken"]
    assert (tmp_path / "new.pt").read_bytes() == b"new-bytes"
    assert fake.downloads == ["voicepacks/new.pt"]


def test_sync_replaces_local_file_whose_content_differs(tmp_path, monkeypatch):
    (tmp_path / "trained.pt").write_bytes(b"old")
    fake = FakeMinio({"voicepacks/trained.pt": b"retrained"})
    monkeypatch.setattr(sync, "_client", lambda: fake)

    result = sync.sync_voicepacks(tmp_path)

    assert result["synced"] == ["trained"]
    assert (tmp_path / "trained.pt").read_bytes() == b"retrained"
