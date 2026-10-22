#!/usr/bin/env python3
"""Stream a purpose-built tool's signed file reference to verified ZIP bytes.

Input is one JSON object on stdin. The signed URL is never printed or saved.
Only unsigned artifact identities and actual download results are recorded.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    request = json.load(sys.stdin)
    output = Path(request["output"])
    receipt_path = Path(request["receipt"])
    temporary = output.with_suffix(output.suffix + ".part")
    parsed = urllib.parse.urlsplit(request["url"])
    if parsed.scheme != "https" or parsed.username or parsed.password:
        raise RuntimeError("Expected an HTTPS file reference without embedded credentials")
    if output.exists() or temporary.exists():
        raise RuntimeError("Refusing to overwrite an existing artifact or partial download")
    receipt = {
        "status": "started", "artifact_id": request["artifact_id"],
        "run_id": request["run_id"], "exact_head": request["head_sha"],
        "started_utc": now(), "expected_bytes": request["expected_bytes"],
        "expected_sha256": request["expected_sha256"], "file": output.name,
        "method": "Actual ZIP bytes from the signed file reference returned by the purpose-built GitHub artifact tool",
        "signed_url_persisted": False,
    }
    total = 0
    state = hashlib.sha256()
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(request["url"], timeout=45) as response:
            receipt["http_status"] = response.status
            receipt["content_type"] = response.headers.get("Content-Type")
            with temporary.open("xb") as stream:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > request["expected_bytes"]:
                        raise RuntimeError("Artifact exceeds the exact advertised byte count")
                    stream.write(chunk)
                    state.update(chunk)
        if total != request["expected_bytes"] or state.hexdigest() != request["expected_sha256"]:
            raise RuntimeError("Actual artifact bytes do not match the advertised identity")
        temporary.replace(output)
        receipt.update({"status": "passed", "bytes": total,
                        "sha256": state.hexdigest(), "github_advertised_digest_matches": True})
    except Exception as error:
        receipt.update({"status": "failed", "bytes_received": total,
                        "sha256_received": state.hexdigest(),
                        "error_type": type(error).__name__})
        receipt["completed_utc"] = now()
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(receipt, indent=2))
        raise SystemExit("Artifact download failed; see the unsigned failure receipt") from None
    receipt["completed_utc"] = now()
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
