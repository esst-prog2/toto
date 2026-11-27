"""Read-only historical audit views, separate from the current repository state.

An audit's captured index must represent its recorded commit. The temporary Git
directory shares read-only object storage, never the live index or references.
Callers supply preserved source bytes and separately check current data integrity.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess


def git_environment():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_LAZY_FETCH"] = "1"
    return env


def _git(root, *args, env=None):
    return subprocess.check_output(
        ["git", "-C", str(root), *args], env=env or git_environment(),
        stderr=subprocess.PIPE, timeout=20,
    )


def verify_preserved_files(root, files):
    """Reject missing/changed preserved bytes and unsafe manifest paths."""
    root = Path(root)
    for name, expected in files.items():
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("Preservation paths must remain relative")
        actual = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Preserved file changed: {name}")
    return len(files)


def historical_view(root, sources, archive, index, index_sha256, commit,
                    destination, *, branch):
    """Build a verified historical Git/source view in an empty private directory.

    ``sources`` is a preserved working-source snapshot. Its data/private subtree
    is supplied independently through ``archive``. No current HEAD, index,
    worktree registration, source file or historical receipt is modified.
    """
    root, sources, archive, index, destination = map(
        Path, (root, sources, archive, index, destination)
    )
    if hashlib.sha256(index.read_bytes()).hexdigest() != index_sha256:
        raise ValueError("Captured historical index changed")
    if subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", commit, "HEAD"],
        env=git_environment(), capture_output=True, timeout=20,
    ).returncode:
        raise ValueError("Recorded historical commit is not a current ancestor")
    destination.mkdir(exist_ok=False)
    metadata = destination / "snapshot.git"
    subprocess.run(
        ["git", "init", "--bare", "-q", str(metadata)], check=True,
        env=git_environment(), capture_output=True, timeout=20,
    )
    objects = _git(root, "rev-parse", "--path-format=absolute", "--git-path", "objects").decode().strip()
    (metadata / "objects/info/alternates").write_text(objects + "\n")
    env = git_environment() | {"GIT_DIR": str(metadata)}
    subprocess.run(["git", "check-ref-format", "refs/heads/" + branch],
                   env=env, check=True, capture_output=True, timeout=20)
    subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/" + branch],
                   env=env, check=True, capture_output=True, timeout=20)
    subprocess.run(["git", "update-ref", "HEAD", commit], env=env, check=True,
                   capture_output=True, timeout=20)
    shutil.copyfile(index, metadata / "index")
    tree = {}
    for entry in _git(root, "ls-tree", "-rz", commit).split(b"\0"):
        if entry:
            header, path = entry.split(b"\t", 1)
            mode, _, oid = header.split()
            tree[path] = (mode, oid)
    captured = {}
    for entry in _git(root, "ls-files", "--stage", "-z", env=env).split(b"\0"):
        if entry:
            header, path = entry.split(b"\t", 1)
            mode, oid, stage = header.split()
            if stage != b"0":
                raise ValueError("Captured historical index contains conflicts")
            captured[path] = (mode, oid)
    if captured != tree:
        raise ValueError("Captured index does not represent the recorded commit")
    view = destination / "work"
    # Real copies keep Path(__file__).resolve() anchored in the isolated view
    # when a frozen parser is executed in a subprocess. Archives are not copied.
    shutil.copytree(sources, view, ignore=shutil.ignore_patterns(".git"))
    (view / "data").mkdir(exist_ok=True)
    if (view / "data/private").exists():
        raise ValueError("Preserved sources must not contain a private archive")
    (view / "data/private").symlink_to(archive, target_is_directory=True)
    # Some frozen inventories hash the old .git pointer as documentary bytes.
    # Returned GIT_DIR/GIT_INDEX_FILE, not that pointer, select the audit state.
    if (sources / ".git").is_file():
        shutil.copyfile(sources / ".git", view / ".git")
    else:
        (view / ".git").write_text("gitdir: " + str(metadata) + "\n")
    return view, env | {"GIT_WORK_TREE": str(view), "GIT_INDEX_FILE": str(metadata / "index")}
