#!/usr/bin/env python3
"""Execute the byte-identical sealed verifier on this actual C2 artifact.

This wrapper records the actual command, process exit and exact output bytes.
All scientific checks remain in the unchanged verify_actual_ci_artifact.py.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def now():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    data = path.read_bytes()
    return {"file": str(path), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    packet = Path(__file__).resolve().parent
    article = workspace / "theta-theory/papers/A2-DYN-marked-boundary-source-author-revision"
    reference = article / "evidence/current-execution/marked-boundary-source-final-precision"
    inventory = workspace / "iteration-20261019c-recovery/current-transport/c2-staged-b5d618b/EXPECTED_FILE_IDENTITIES.json"
    verifier = packet / "verify_actual_ci_artifact.py"
    if identity(verifier)["sha256"] != "e44db871d6afaea2aaac23ec836ceb1e57993ecb464afcf884475530b1e7b42f":
        raise RuntimeError("The sealed verifier bytes changed")
    if identity(inventory)["sha256"] != "e2009b63912d698f7eaf4a8875e332d3ff5bf23b53059f243f7236272cb3dc38":
        raise RuntimeError("The actual C2 inventory bytes changed")
    observation = args.observation.resolve()
    observation.read_bytes()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    command = [
        sys.executable, str(verifier), "--article", str(article),
        "--archive", str(packet / "a2-dyn-marked-boundary-source-39281615689.zip"),
        "--tested-commit", "efde9fa6c45e7835989b653622a9870e59027530",
        "--tested-article-tree", "b4add0580cc8211223dfa57e6e618e2bf9546d09",
        "--tested-root-tree", "b5d618b8a4b356f8ca07f1c9f1238e35d879ede8",
        "--workflow", ".github/workflows/a2-dyn-marked-boundary-source-20261019.yml",
        "--expected-identities", str(inventory), "--manifest", str(article / "SOURCE_MANIFEST.json"),
        "--reference-build", str(reference), "--reference-source", str(reference / "source-checks.json"),
        "--reference-history", str(article / "evidence/current-execution/historical-recovery/20261019T145453154865Z/REBUILD_RECEIPT.json"),
        "--observation", str(observation), "--artifact-id", "12201151164", "--job-id", "118156848926",
        "--job-log-identity", str(packet / "CI_JOB_LOG_IDENTITY.json"),
        "--job-log", str(packet / "CI_JOB_LOG_EXACT.log"), "--output-dir", str(output),
    ]
    receipt = {"schema": 1, "scope": "Actual local execution of the sealed independent CI artifact verifier",
               "started_utc": now(), "cwd": str(workspace), "command": command,
               "verifier_identity": identity(verifier), "tested_inventory_identity": identity(inventory),
               "observation_identity": identity(observation)}
    (output / "ACTUAL_VERIFIER_INVOCATION.json").write_text(json.dumps(receipt, indent=2) + "\n")
    result = subprocess.run(command, cwd=workspace, capture_output=True)
    stdout = output / "verify_actual_ci_artifact.stdout.json"
    stderr = output / "verify_actual_ci_artifact.stderr.txt"
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    receipt.update({"completed_utc": now(), "exit_code": result.returncode,
                    "stdout": identity(stdout), "stderr": identity(stderr),
                    "status": "passed" if result.returncode == 0 else "failed"})
    (output / "ACTUAL_VERIFIER_EXECUTION.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
