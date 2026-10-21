#!/usr/bin/env python3
"""Verify every received delivery file, all archive parts and complete payloads.

Place this file beside restore_archives.py and the publication manifests.
This reads the stored strict execution evidence; it does not execute a new
build, mathematical diagnostic, proof check, human review or editorial step.
"""
from __future__ import annotations

import json
import sys
import tarfile
import zipfile

sys.dont_write_bytecode = True
from restore_archives import arguments, assembled_archives, read_delivery, verify_contents


def main() -> None:
    args = arguments(__doc__, restore=False)
    root = args.root.resolve()
    delivery, parts, metadata = read_delivery(root, args.expect_source_commit, args.expect_paper_tree)
    with assembled_archives(root, parts) as paths:
        report = verify_contents(root, delivery, metadata, paths)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile, tarfile.TarError) as error:
        raise SystemExit("FAIL: " + str(error)) from error
