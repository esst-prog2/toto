"""Synthetic Git histories prove that historical guards survive later commits."""
import hashlib
from pathlib import Path
import subprocess

import pytest

from toto_estimator.audit_snapshot import historical_view, verify_preserved_files


def git(root, *args, env=None):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env).decode().strip()


@pytest.fixture
def history(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Synthetic Test")
    git(root, "config", "user.email", "synthetic@example.invalid")
    (root / "sample.txt").write_text("original\n")
    git(root, "add", "sample.txt")
    git(root, "commit", "-qm", "Initial synthetic state")
    old = git(root, "rev-parse", "HEAD")
    index = tmp_path / "index.bin"
    index.write_bytes((root / ".git/index").read_bytes())
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "sample.txt").write_text("original\n")
    archive = tmp_path / "archive"
    archive.mkdir()
    (root / "sample.txt").write_text("later\n")
    git(root, "commit", "-qam", "Later synthetic state")
    return root, sources, archive, index, old


def build(history, tmp_path, **overrides):
    root, sources, archive, index, old = history
    args = dict(root=root, sources=sources, archive=archive, index=index,
                index_sha256=hashlib.sha256(index.read_bytes()).hexdigest(),
                commit=old, destination=tmp_path / "view", branch="recorded-audit")
    args.update(overrides)
    return historical_view(**args)


def test_later_head_is_preserved_while_historical_head_and_index_are_verified(history, tmp_path):
    root, _, _, index, old = history
    live_head = git(root, "rev-parse", "HEAD")
    live_index = (root / ".git/index").read_bytes()
    view, env = build(history, tmp_path)
    assert live_head != old
    assert git(view, "rev-parse", "HEAD", env=env) == old
    assert Path(env["GIT_INDEX_FILE"]).read_bytes() == index.read_bytes()
    assert (view / "sample.txt").read_text() == "original\n"
    assert git(root, "rev-parse", "HEAD") == live_head
    assert (root / ".git/index").read_bytes() == live_index


def test_index_tampering_is_rejected(history, tmp_path):
    with pytest.raises(ValueError, match="index changed"):
        build(history, tmp_path, index_sha256="0" * 64)


def test_recorded_git_pointer_is_evidence_not_repository_navigation(history, tmp_path):
    recorded = b"gitdir: /unavailable/synthetic-worktree-metadata\n"
    (history[1] / ".git").write_bytes(recorded)
    view, env = build(history, tmp_path)
    assert (view / ".git").read_bytes() == recorded
    assert git(view, "rev-parse", "HEAD", env=env) == history[4]
    assert Path(env["GIT_INDEX_FILE"]).is_relative_to(tmp_path)


def test_valid_index_for_wrong_commit_is_rejected(history, tmp_path):
    with pytest.raises(ValueError, match="does not represent"):
        build(history, tmp_path, commit=git(history[0], "rev-parse", "HEAD"))


def test_nonancestor_commit_is_rejected(history, tmp_path):
    root = history[0]
    git(root, "checkout", "--orphan", "unrelated")
    git(root, "commit", "-qm", "Unrelated synthetic root")
    with pytest.raises(ValueError, match="not a current ancestor"):
        build(history, tmp_path)


def test_preserved_content_tampering_is_rejected(tmp_path):
    (tmp_path / "sample.txt").write_text("original")
    files = {"sample.txt": hashlib.sha256(b"original").hexdigest()}
    assert verify_preserved_files(tmp_path, files) == 1
    (tmp_path / "sample.txt").write_text("changed")
    with pytest.raises(ValueError, match="Preserved file changed"):
        verify_preserved_files(tmp_path, files)


def test_manifest_cannot_escape_snapshot(tmp_path):
    with pytest.raises(ValueError, match="relative"):
        verify_preserved_files(tmp_path, {"../outside": "0" * 64})
