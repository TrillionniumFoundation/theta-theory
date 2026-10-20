#!/usr/bin/env python3
"""Assemble unchanged actual API objects with explicit byte provenance."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def identity(path):
    data = path.read_bytes()
    return {"file": str(path.resolve()), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-dir", type=Path, required=True)
    parser.add_argument("--artifact-observations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.provenance.exists():
        raise RuntimeError("Refusing to overwrite existing actual observations")
    sources = {}
    observation = {}
    for kind, basename in (("run", "run"), ("jobs", "attempt_jobs")):
        raw_path = args.api_dir / (basename + ".response.bin")
        parsed_path = args.api_dir / (basename + ".parsed.json")
        receipt_path = args.api_dir / (basename + ".receipt.json")
        raw = raw_path.read_bytes()
        response = json.loads(raw)
        receipt = json.loads(receipt_path.read_bytes())
        if receipt["http_status"] != 200 or response != json.loads(parsed_path.read_bytes()):
            raise RuntimeError("Actual HTTP/parsed response mismatch: " + kind)
        if len(raw) != receipt["response_bytes"] or hashlib.sha256(raw).hexdigest() != receipt["response_sha256"]:
            raise RuntimeError("Actual raw response byte identity mismatch: " + kind)
        observation[kind] = response
        sources[kind] = {"raw": identity(raw_path), "parsed": identity(parsed_path),
                         "receipt": identity(receipt_path), "requested_at": receipt["requested_at"],
                         "observed_at": receipt["observed_at"], "url": receipt["url"]}
    observations = json.loads(args.artifact_observations.read_bytes())
    artifacts = [row for row in observations if row.get("kind") == "artifacts"]
    if len(artifacts) != 1:
        raise RuntimeError("Exactly one actual artifact collection is required")
    artifact = artifacts[0]
    if artifact["isError"] or json.loads(artifact["response_text"]) != artifact["response"]:
        raise RuntimeError("Actual artifact API response mismatch")
    observation["artifacts"] = artifact["response"]
    sources["artifacts"] = {"receipt": identity(args.artifact_observations),
                            "requested_at": artifact["requested_at"], "observed_at": artifact["observed_at"],
                            "url": artifact["url"],
                            "response_text_sha256": hashlib.sha256(artifact["response_text"].encode()).hexdigest()}
    for key, array in (("jobs", "jobs"), ("artifacts", "artifacts")):
        if observation[key]["total_count"] != len(observation[key][array]):
            raise RuntimeError("Actual collection is not completely represented: " + key)
    args.output.write_text(json.dumps(observation, indent=2) + "\n")
    provenance = {"schema": 1, "assembled_utc": datetime.now(timezone.utc).isoformat(),
                  "scope": "Actual API objects copied without changing any status, conclusion, timestamp or job step",
                  "sources": sources, "output": identity(args.output),
                  "run_status": observation["run"]["status"],
                  "run_conclusion": observation["run"]["conclusion"]}
    args.provenance.write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
