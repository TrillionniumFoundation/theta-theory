#!/usr/bin/env python3
"""Coherent negative attacks for the C30q4 independent verifier."""

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
PRODUCER = HERE / "cm2_round306c30q4_compact_q_11010111_universal_containment_gate.py"
VERIFIER = HERE / "cm2_round306c30q4_compact_q_11010111_universal_containment_independent_verifier.py"
PRODUCER_SHA256 = "cdf1b43cec11aa6f3b03ef3a934cd1260478c1266dc38a89fb23e1996f482232"
VERIFIER_SHA256 = "72bc8dbae24b5d1a2a2313330f9f737fe4a3a8a660263dab117b71da88558d5d"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def reclose(document: dict[str, Any]) -> bytes:
    document["result_sha256"] = hashlib.sha256(canonical(document["result"])).hexdigest()
    return canonical(document) + b"\n"


def run_verifier(payload: bytes) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "30630929"})
    return subprocess.run(
        [sys.executable, "-B", "-s", os.fspath(VERIFIER), "-"],
        input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=HERE.parent, env=environment, check=False,
    )


def main() -> int:
    try:
        need(len(sys.argv) == 2, "candidate path required")
        candidate_path = Path(sys.argv[1]).absolute()
        raw = candidate_path.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document) + b"\n", "canonical baseline candidate")
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
            not any("cm2_round306c30q4_compact_q_11010111_universal_containment_gate" in name for name in imports)
            and b"def roots_from_frozen" in verifier_raw
            and b"def partition" in verifier_raw,
            "independent verifier AST smoke",
        )
        baseline = run_verifier(raw)
        need(
            baseline.returncode == 0 and baseline.stderr == b""
            and json.loads(baseline.stdout)["status"].startswith("PASS_INDEPENDENT_C30Q4"),
            "baseline verifier PASS",
        )

        def first_origin(result: dict[str, Any]) -> dict[str, Any]:
            return result["universal_residual_containment"]["origin_rows"][0]

        attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            ("formal_credit_pregrant", lambda r: r["strict_nonpromotion"].__setitem__("formal_credit", 2)),
            ("formal_remaining_decrement", lambda r: r["strict_nonpromotion"].__setitem__("compact_q_formal_remaining_origins", 52)),
            ("ledger_changed", lambda r: r["strict_nonpromotion"].__setitem__("ledger_unchanged", False)),
            ("release_authority", lambda r: r["strict_nonpromotion"].__setitem__("seal_or_release_authority", True)),
            ("CM2_go", lambda r: r["strict_nonpromotion"].__setitem__("CM2", "GO_FOR_CLAIM")),
            ("status_overclaim", lambda r: r.__setitem__("status", "PASS_FORMAL_54_TO_52")),
            ("residual_count_drop", lambda r: r["universal_residual_containment"].__setitem__("residual_child_count", 255)),
            ("container_multiplicity_forge", lambda r: first_origin(r)["residual_rows"][0].__setitem__("analytic_root_container_count", 0)),
            ("container_key_forge", lambda r: first_origin(r)["residual_rows"][0].__setitem__("analytic_root_containers", ["FORGED_ROOT"])),
            ("residual_category_forge", lambda r: first_origin(r)["residual_rows"][0].__setitem__("category", "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH")),
            ("partition_digest_forge", lambda r: r["cross_root_half_open_partitions"]["W:N:03.15.11010111"].__setitem__("owner_assignment_rows_sha256", "0" * 64)),
            ("analytic_root_count_drop", lambda r: r["analytic_root_rebuild"].__setitem__("root_count", 31)),
        ]
        outcomes: list[dict[str, Any]] = []
        for name, action in attacks:
            mutated = deepcopy(document)
            action(mutated["result"])
            payload = reclose(mutated)
            rejected = run_verifier(payload)
            need(
                rejected.returncode != 0 and rejected.stdout == b""
                and rejected.stderr.startswith(b"REJECT_C30Q4_INDEPENDENT_VERIFICATION:"),
                "attack rejected:" + name,
            )
            outcomes.append({"attack": name, "top_level_result_sha256_reclosed": True, "rejected": True})
        output = {
            "schema": "cm2.round306c30q4.compact-q-11010111-coherent-attacks.v1",
            "status": f"PASS_{len(outcomes)}_OF_{len(attacks)}_COHERENT_ATTACKS_REJECTED",
            "baseline_verification_passed": True,
            "independent_verifier_AST_smoke": True,
            "attacks": outcomes,
            "formal_credit": 0,
            "ledger_unchanged": True,
            "compact_q_formal_remaining_origins": 54,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Reject, OSError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_C30Q4_ATTACK_HARNESS:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
