#!/usr/bin/env python3
"""Coherent negative harness for the C30q3 independent verifier."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
PRODUCER = HERE / "cm2_round306c30q3_compact_q_south_paired_origin_analytic_probe.py"
VERIFIER = HERE / "cm2_round306c30q3_compact_q_south_paired_origin_analytic_independent_verifier.py"
PRODUCER_SHA256 = "364280a41b868ba1fd3b83b849506040b44af836e2065cd17cc9ef5846673975"
VERIFIER_SHA256 = "86c9b437371b78ee65430118a0afa328a6d21e070328f0684720cb561225240f"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def close(document: dict[str, Any]) -> bytes:
    document["result_sha256"] = hashlib.sha256(canonical(document["result"])).hexdigest()
    return canonical(document) + b"\n"


def run(path: Path, payload: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONHASHSEED"] = "30630071"
    return subprocess.run(
        [sys.executable, "-B", "-s", os.fspath(path), "-"] if payload is not None
        else [sys.executable, "-B", "-s", os.fspath(path)],
        input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=HERE.parent, env=environment, check=False,
    )


def mutate(document: dict[str, Any], action: Callable[[dict[str, Any]], None]) -> bytes:
    candidate = deepcopy(document)
    action(candidate["result"])
    return close(candidate)


def main() -> int:
    try:
        need(hashlib.sha256(PRODUCER.read_bytes()).hexdigest() == PRODUCER_SHA256, "producer pin")
        verifier_raw = VERIFIER.read_bytes()
        need(hashlib.sha256(verifier_raw).hexdigest() == VERIFIER_SHA256, "verifier pin")
        tree = ast.parse(verifier_raw.decode())
        imports = {
            alias.name for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        need(
            not any("cm2_round306c30q3_compact_q_south_paired_origin_analytic_probe" in name for name in imports)
            and b"def independent_authority" in verifier_raw
            and b"def independent_partition" in verifier_raw,
            "verifier independent implementation AST smoke",
        )

        produced = run(PRODUCER)
        need(produced.returncode == 0 and produced.stderr == b"" and bool(produced.stdout), "clean producer smoke")
        baseline = json.loads(produced.stdout)
        verified = run(VERIFIER, produced.stdout)
        need(
            verified.returncode == 0 and verified.stderr == b""
            and json.loads(verified.stdout)["status"].startswith("PASS_INDEPENDENT_C30Q3"),
            "clean verifier smoke",
        )

        attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            ("formal_credit_pregrant", lambda r: r["strict_nonpromotion"].__setitem__("formal_credit", 1)),
            ("compact_remaining_decrement", lambda r: r["strict_nonpromotion"].__setitem__("compact_q_formal_remaining_origins", 53)),
            ("ledger_changed_claim", lambda r: r["strict_nonpromotion"].__setitem__("ledger_unchanged", False)),
            ("illegal_release_authority", lambda r: r["strict_nonpromotion"].__setitem__("seal_or_release_authority", True)),
            ("illegal_CM2_go", lambda r: r["strict_nonpromotion"].__setitem__("CM2", "GO_FOR_CLAIM")),
            ("origin_substitution", lambda r: r["selected_origin"].__setitem__("origin_key", "W:N:03.15.01111111")),
            ("root_count_drop", lambda r: r["selected_origin"].__setitem__("root_count", 15)),
            ("partition_digest_forge", lambda r: r["cross_root_half_open_partition"].__setitem__("owner_assignment_rows_sha256", "0" * 64)),
            ("frozen_margin_weaken", lambda r: r["analytic_whole_origin_certificate"]["frozen_target_strictly_behind"].__setitem__("uniform_strict_upper", "0")),
            ("status_overclaim", lambda r: r.__setitem__("status", "PASS_54_TO_0_FORMAL_PROMOTION")),
        ]
        outcomes: list[dict[str, Any]] = []
        for name, action in attacks:
            payload = mutate(baseline, action)
            result = run(VERIFIER, payload)
            need(
                result.returncode != 0 and result.stdout == b""
                and result.stderr.startswith(b"REJECT_C30Q3_INDEPENDENT_VERIFICATION:"),
                "attack rejected:" + name,
            )
            outcomes.append({"attack": name, "coherent_result_sha256_reclosed": True, "rejected": True})
        output = {
            "schema": "cm2.round306c30q3.compact-q-south-paired-origin-coherent-attacks.v1",
            "status": f"PASS_{len(outcomes)}_OF_{len(attacks)}_COHERENT_ATTACKS_REJECTED",
            "verifier_independent_AST_smoke": True,
            "baseline_verification_passed": True,
            "attacks": outcomes,
            "formal_credit": 0,
            "ledger_unchanged": True,
            "compact_q_formal_remaining_origins": 54,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Reject, OSError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_C30Q3_ATTACK_HARNESS:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
