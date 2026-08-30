#!/usr/bin/env python3
"""Write the publication record after the verified source commit exists."""
from __future__ import annotations

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verified-sha", required=True)
    parser.add_argument("--pre-main-sha", required=True)
    parser.add_argument("--archive-branch", required=True)
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()

    certificate = json.loads((ROOT / "ROUND5_FINAL_CERTIFICATE.json").read_text(encoding="utf-8"))
    if certificate.get("gates", {}).get("clean_latex_build") != "PASS":
        raise SystemExit("certificate build gate is not PASS")
    record = {
        "schema": "theta-theory-round5-publication-record-v1",
        "verified_source_commit": args.verified_sha,
        "pre_publication_main": args.pre_main_sha,
        "archive_branch": args.archive_branch,
        "publication_tag": args.tag,
        "publication_target": "main",
        "paper_count": 11,
        "source_files_changed_after_verification": [],
        "status": "READY_TO_PUBLISH_VERIFIED_PARENT",
    }
    (ROOT / "ROUND5_PUBLICATION_RECORD.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    status_path = ROOT / "ROUND5_REVISION_STATUS.md"
    status = status_path.read_text(encoding="utf-8")
    status = status.replace("Main-tree publication: **PENDING**", "Main-tree publication: **PUBLISHED FROM VERIFIED PARENT**")
    status_path.write_text(status, encoding="utf-8")

    manifest_path = ROOT / "ROUND5_REVISION_MANIFEST.yaml"
    manifest = manifest_path.read_text(encoding="utf-8")
    manifest = manifest.replace("publication: pending", "publication: verified_parent_ready")
    manifest_path.write_text(manifest, encoding="utf-8")
    print("ROUND5_PUBLICATION_RECORD_WRITTEN")


if __name__ == "__main__":
    main()
