#!/usr/bin/env python3
"""Reconstruct the complete R77 source archive from authenticated Git objects.

This packages source; it does not run mathematical or compilation validation.
It never reads a working-tree file to construct the archive.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

SOURCE_COMMIT = "18b76a739898d2734c4f5bfcb609db0786cd4c11"
SOURCE_PATH = "papers/General-Theta-Foundations-I-restart/r77-shared-preparation-and-memory"
SOURCE_TREE = "c48519790add40e3c67aa245aa8e5ee1fcc47de6"
PREFIX = "General_Theta_Foundations_I_R77_Source"


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path,
                        default=Path("General_Theta_Foundations_I_R77_Complete_Source.tar.gz"))
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    repo = args.repository.resolve()
    tree = git(repo, "rev-parse", f"{SOURCE_COMMIT}:{SOURCE_PATH}").decode().strip()
    if tree != SOURCE_TREE:
        raise RuntimeError("The authenticated source subtree does not match")
    epoch = int(git(repo, "show", "-s", "--format=%ct", SOURCE_COMMIT))
    entries = []
    for raw in git(repo, "ls-tree", "-rz", f"{SOURCE_COMMIT}:{SOURCE_PATH}").split(b"\0"):
        if not raw:
            continue
        meta, name = raw.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise RuntimeError(f"Unexpected source entry: {name!r}")
        entries.append((name.decode(), mode, sha))
    entries.sort(key=lambda row: row[0].encode())
    if len(entries) != 622:
        raise RuntimeError("Incomplete source inventory")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    process = subprocess.Popen(["git", "-C", str(repo), "cat-file", "--batch"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        with args.output.open("wb") as target:
            with gzip.GzipFile(filename="", fileobj=target, mode="wb", mtime=epoch,
                               compresslevel=9) as compressed:
                with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as archive:
                    for name, mode, sha in entries:
                        process.stdin.write((sha + "\n").encode())
                        process.stdin.flush()
                        header = process.stdout.readline().decode().strip().split()
                        if len(header) != 3 or header[0] != sha or header[1] != "blob":
                            raise RuntimeError(f"Bad Git object response for {name}")
                        size = int(header[2])
                        content = process.stdout.read(size)
                        if len(content) != size or process.stdout.read(1) != b"\n":
                            raise RuntimeError(f"Truncated Git object for {name}")
                        actual = hashlib.sha1(f"blob {size}\0".encode() + content).hexdigest()
                        if actual != sha:
                            raise RuntimeError(f"Git object authentication failed for {name}")
                        info = tarfile.TarInfo(f"{PREFIX}/{name}")
                        info.size, info.mtime = size, epoch
                        info.mode = 0o755 if mode == "100755" else 0o644
                        info.uid = info.gid = 0
                        info.uname = info.gname = ""
                        archive.addfile(info, io.BytesIO(content))
                        rows.append({"path": name, "mode": mode, "bytes": size,
                                     "git_blob": sha, "sha256": hashlib.sha256(content).hexdigest()})
    finally:
        process.stdin.close()
        code = process.wait()
        if code:
            raise RuntimeError(f"git cat-file exited {code}")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    receipt = {"schema": "theta.r77.complete-source-bundle.v1", "source_commit": SOURCE_COMMIT,
               "source_path": SOURCE_PATH, "source_git_tree": tree, "source_date_epoch": epoch,
               "file_count": len(rows), "uncompressed_file_bytes": sum(x["bytes"] for x in rows),
               "archive_name": args.output.name, "archive_sha256": digest,
               "archive_bytes": args.output.stat().st_size, "archive_prefix": PREFIX,
               "method": "Sorted authenticated Git blobs, PAX tar, gzip level 9, zero ownership, source-commit mtime",
               "scope": "Packaging and object authentication, not theorem proof verification", "files": rows}
    manifest = args.manifest or args.output.with_suffix(args.output.suffix + ".json")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "files"}, indent=2))


if __name__ == "__main__":
    main()
