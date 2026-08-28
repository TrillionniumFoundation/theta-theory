#!/usr/bin/env python3
"""Coherent negative attacks for the C30q6 independent verifier."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
VERIFIER = HERE / "cm2_round306c30q6_compact_q_six_origin_clean_room_zero_credit_independent_verifier_v1.py"
VERIFIER_SHA256 = "6ee4adb36cd071ba5015281508416c45e7ab70788f8165535c6339e6f4515351"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def close(document: dict[str, Any]) -> bytes:
    document["result_sha256"] = hashlib.sha256(canonical(document["result"])).hexdigest()
    return canonical(document) + b"\n"


def invoke(path: Path) -> subprocess.CompletedProcess[bytes]:
    environment = {
        "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "30660793",
    }
    return subprocess.run(
        [sys.executable, "-B", "-s", str(VERIFIER), str(path)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=environment, timeout=60, check=False,
    )


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage")
        need(hashlib.sha256(VERIFIER.read_bytes()).hexdigest() == VERIFIER_SHA256,
             "verifier pin")
        original_raw = Path(argv[1]).read_bytes()
        original = json.loads(original_raw)
        need(original_raw == canonical(original) + b"\n", "canonical original")
        attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            ("schema_rebind", lambda d: d.__setitem__("schema", "forged.schema")),
            ("status_promotion", lambda d: d["result"].__setitem__("status", "PASS_FORMAL_54_TO_48")),
            ("origin_count_shrink", lambda d: d["result"]["six_origin_research_closure"].__setitem__("origin_count", 5)),
            ("origin_drop", lambda d: d["result"]["six_origin_research_closure"]["origin_keys"].pop()),
            ("origin_substitution", lambda d: d["result"]["six_origin_research_closure"]["origin_keys"].__setitem__(0, "W:N:03.15.11011101")),
            ("research_closure_clear", lambda d: d["result"]["six_origin_research_closure"].__setitem__("all_six_research_closed", False)),
            ("uniform_authority_forge", lambda d: d["result"]["six_origin_research_closure"].__setitem__("uniform_formal_predecessor_authority", True)),
            ("transition_authorize", lambda d: d["result"]["authority_fail_closed"].__setitem__("formal_transition_authorized", True)),
            ("blocker_drop", lambda d: d["result"]["authority_fail_closed"]["blocking_reasons"].pop()),
            ("q0_authority_upgrade", lambda d: d["result"]["six_origin_research_closure"]["origin_evidence"]["W:N:03.15.01111111"].__setitem__("authority_class", "FORMAL_TERMINAL_RECEIPT")),
            ("q4_authority_upgrade", lambda d: d["result"]["six_origin_research_closure"]["origin_evidence"]["W:N:03.15.11010111"].__setitem__("authority_class", "FORMAL_TERMINAL_RECEIPT")),
            ("formal_credit_six", lambda d: d["result"]["strict_nonpromotion"].__setitem__("formal_credit", 6)),
            ("compact_q_54_to_48", lambda d: d["result"]["strict_nonpromotion"].__setitem__("compact_q_formal_remaining_origins", 48)),
            ("source_w_80_to_74", lambda d: d["result"]["strict_nonpromotion"].__setitem__("source_W_formal_remaining", 74)),
            ("ledger_changed", lambda d: d["result"]["strict_nonpromotion"].__setitem__("ledger_unchanged", False)),
            ("cm2_go", lambda d: d["result"]["strict_nonpromotion"].__setitem__("CM2", "GO_FOR_CLAIM")),
            ("d02_clear", lambda d: d["result"]["strict_nonpromotion"].__setitem__("D02", "PASS")),
            ("predecessor_rebind", lambda d: d["result"]["formal_predecessor"].__setitem__("round", "Round306C30f")),
            ("manifest_pin_drift", lambda d: d["result"]["formal_predecessor"].__setitem__("manifest_sha256", "0" * 64)),
        ]
        results: list[dict[str, Any]] = []
        with tempfile.TemporaryDirectory(prefix="cm2-c30q6-attacks-") as directory:
            base = Path(directory)
            valid = base / "valid.json"
            valid.write_bytes(original_raw)
            baseline = invoke(valid)
            need(baseline.returncode == 0 and baseline.stderr == b"", "valid baseline")
            for index, (name, mutate) in enumerate(attacks):
                document = copy.deepcopy(original)
                mutate(document)
                path = base / f"attack-{index:02d}.json"
                path.write_bytes(close(document))
                process = invoke(path)
                need(process.returncode == 2 and process.stdout == b""
                     and process.stderr.startswith(b"REJECT:"), "attack accepted:" + name)
                results.append({"attack": name,
                                "rejection": process.stderr.decode("utf-8").strip()})

            malformed = [
                ("duplicate_schema", original_raw.replace(
                    b'{"result":', b'{"schema":"duplicate","result":', 1)),
                ("trailing_document", original_raw + b"{}\n"),
                ("noncanonical_whitespace", b" " + original_raw),
            ]
            for offset, (name, raw) in enumerate(malformed, len(attacks)):
                path = base / f"attack-{offset:02d}.json"
                path.write_bytes(raw)
                process = invoke(path)
                need(process.returncode == 2 and process.stdout == b""
                     and process.stderr.startswith(b"REJECT:"), "malformed accepted:" + name)
                results.append({"attack": name,
                                "rejection": process.stderr.decode("utf-8").strip()})

            target = base / "symlink-target.json"
            target.write_bytes(original_raw)
            link = base / "attack-symlink.json"
            link.symlink_to(target)
            process = invoke(link)
            need(process.returncode == 2 and process.stdout == b""
                 and process.stderr.startswith(b"REJECT:"), "symlink accepted")
            results.append({"attack": "candidate_symlink",
                            "rejection": process.stderr.decode("utf-8").strip()})

            hard_source = base / "hard-source.json"
            hard_source.write_bytes(original_raw)
            hard_link = base / "attack-hardlink.json"
            os.link(hard_source, hard_link)
            process = invoke(hard_link)
            need(process.returncode == 2 and process.stdout == b""
                 and process.stderr.startswith(b"REJECT:"), "hardlink accepted")
            results.append({"attack": "candidate_hardlink",
                            "rejection": process.stderr.decode("utf-8").strip()})

        output = {
            "schema": "cm2.round306c30q6.compact-q-six-origin-clean-room-zero-credit-coherent-attacks.v1",
            "status": f"PASS_{len(results)}_OF_{len(results)}_COHERENT_ATTACKS_REJECTED",
            "attack_count": len(results), "rejected": len(results),
            "valid_baseline_passed": True, "attacks": results,
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, Reject,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
