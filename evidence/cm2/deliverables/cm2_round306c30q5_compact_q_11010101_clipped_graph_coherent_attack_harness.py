#!/usr/bin/env python3
"""Coherent negative attacks for the C30q5 independent verifier."""

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
PRODUCER = (
    HERE / "cm2_round306c30q5_compact_q_11010101_clipped_graph_gate.py"
)
VERIFIER = (
    HERE
    / "cm2_round306c30q5_compact_q_11010101_clipped_graph_"
      "independent_verifier.py"
)
PRODUCER_SHA256 = (
    "ba6ee02b1e4910762f242bebc8697c389d789a12be21d0e57761f81e5be06972"
)
VERIFIER_SHA256 = (
    "d564d6187b7e28042866bce8d3dafc5040ac61ee7ae032521908794e1bcb8d99"
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def reclose(document: dict[str, Any]) -> bytes:
    document["result_sha256"] = digest(document["result"])
    return canonical(document) + b"\n"


def run_verifier(payload: bytes) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment.update({
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "30630929",
    })
    return subprocess.run(
        [sys.executable, "-B", "-s", os.fspath(VERIFIER), "-"],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=HERE.parent,
        env=environment,
        check=False,
    )


def main() -> int:
    try:
        need(len(sys.argv) == 2, "candidate path required")
        raw = Path(sys.argv[1]).absolute().read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document) + b"\n",
             "canonical baseline candidate")
        need(hashlib.sha256(PRODUCER.read_bytes()).hexdigest()
             == PRODUCER_SHA256, "producer pin")
        verifier_raw = VERIFIER.read_bytes()
        need(hashlib.sha256(verifier_raw).hexdigest()
             == VERIFIER_SHA256, "verifier pin")
        tree = ast.parse(verifier_raw.decode("utf-8", "strict"))
        imports = {
            alias.name for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        need(
            not any(
                "cm2_round306c30q5_compact_q_11010101_clipped_graph_gate"
                in name for name in imports
            )
            and b"def clipped_geometry" in verifier_raw
            and b"def p_star" in verifier_raw
            and b"def outer_ledger" in verifier_raw
            and b"def partition_hash" in verifier_raw,
            "independent verifier AST smoke",
        )
        baseline = run_verifier(raw)
        need(
            baseline.returncode == 0
            and baseline.stderr == b""
            and json.loads(baseline.stdout)["status"].startswith(
                "PASS_INDEPENDENT_C30Q5"
            ),
            "baseline verifier PASS",
        )

        def first_origin(result: dict[str, Any]) -> dict[str, Any]:
            return result["universal_residual_containment"]["origin_rows"][0]

        def first_clipped(result: dict[str, Any]) -> dict[str, Any]:
            return next(
                row for row in first_origin(result)["residual_rows"]
                if row["category"].startswith("CLIPPED_")
            )

        def first_graph(result: dict[str, Any]) -> dict[str, Any]:
            return result["clipped_graph_three_stratum_closure"]["graph_rows"][0]

        def proof_mutation(
            result: dict[str, Any], key: str, value: Any
        ) -> None:
            proof = first_graph(result)["three_stratum_proof"]
            proof[key] = value
            proof["proof_sha256"] = digest({
                name: item for name, item in proof.items()
                if name != "proof_sha256"
            })

        def delete_s_bin(result: dict[str, Any]) -> None:
            row = first_origin(result)
            del row["clipped_s_bins"][0]

        attacks: list[
            tuple[str, Callable[[dict[str, Any]], None]]
        ] = [
            ("formal_credit_pregrant", lambda r:
             r["strict_nonpromotion"].__setitem__("formal_credit", 2)),
            ("compact_remaining_decrement", lambda r:
             r["strict_nonpromotion"].__setitem__(
                 "compact_q_formal_remaining_origins", 52)),
            ("source_W_remaining_decrement", lambda r:
             r["strict_nonpromotion"].__setitem__(
                 "source_W_formal_remaining", 78)),
            ("ledger_changed", lambda r:
             r["strict_nonpromotion"].__setitem__("ledger_unchanged", False)),
            ("release_authority", lambda r:
             r["strict_nonpromotion"].__setitem__(
                 "seal_or_release_authority", True)),
            ("D02_forged_pass", lambda r:
             r["strict_nonpromotion"].__setitem__("D02", "PASS")),
            ("CM2_go", lambda r:
             r["strict_nonpromotion"].__setitem__("CM2", "GO_FOR_CLAIM")),
            ("status_overclaim", lambda r:
             r.__setitem__("status", "PASS_FORMAL_54_TO_52")),
            ("residual_count_drop", lambda r:
             r["universal_residual_containment"].__setitem__(
                 "residual_child_count", 271)),
            ("container_multiplicity_forge", lambda r:
             first_clipped(r).__setitem__(
                 "analytic_root_container_count", 0)),
            ("container_key_forge", lambda r:
             first_clipped(r).__setitem__(
                 "analytic_root_containers", ["FORGED_ROOT"])),
            ("clipped_category_forge", lambda r:
             first_clipped(r).__setitem__("category", COMPACT_FORGE)),
            ("wrong_reflected_G_target", lambda r:
             first_graph(r).__setitem__("active_targets", ["G[0,0]", "W[-1,0]"])),
            ("derivative_sign_swap", lambda r:
             proof_mutation(r, "strict_p_derivative_sign", "POSITIVE")),
            ("full_p_graph_forge", lambda r:
             proof_mutation(r, "full_p_graph", True)),
            ("positive_first_margin_drop", lambda r:
             proof_mutation(
                 r, "target_strict_positive_first_on_closed_outer", False)),
            ("negative_side_live_forge", lambda r:
             proof_mutation(
                 r, "Delta_negative_open_3D_disposition",
                 "LIVE_UNIQUE_FIRST_FROZEN_OWNER")),
            ("all_three_strata_forge", lambda r:
             proof_mutation(r, "all_three_strata_excluded", False)),
            ("s_bin_removed", delete_s_bin),
            ("shared_face_owner_forge", lambda r:
             r["clipped_graph_three_stratum_closure"]
              ["analytic_outer_half_open_ledger"].__setitem__(
                  "half_open_owner", "duplicate owners allowed")),
            ("outer_1D_count_forge", lambda r:
             r["clipped_graph_three_stratum_closure"]
              ["analytic_outer_half_open_ledger"].__setitem__(
                  "1D_graph_face_outer_count", 81)),
            ("root_partition_digest_forge", lambda r:
             r["cross_root_half_open_partitions"]
              ["W:N:03.15.11010101"].__setitem__(
                  "owner_assignment_rows_sha256", "0" * 64)),
            ("uniform_inside_slab_forge", lambda r:
             r["whole_origin_conclusion"].__setitem__(
                 "graph_uniformly_inside_clipped_slab", True)),
            ("shared_face_crossing_drop", lambda r:
             r["clipped_graph_three_stratum_closure"]
              ["exact_common_graph_certificate"]
              ["shared_face_falsification"].__setitem__(
                  "graph_crosses_shared_abs_p_face", False)),
            ("squared_branch_acceptance", lambda r:
             r["clipped_graph_three_stratum_closure"]
              ["exact_common_graph_certificate"]["branch_guards"].__setitem__(
                  "squared_extraneous_branch_rejected", False)),
        ]
        outcomes: list[dict[str, Any]] = []
        for name, action in attacks:
            mutated = deepcopy(document)
            action(mutated["result"])
            rejected = run_verifier(reclose(mutated))
            need(
                rejected.returncode != 0
                and rejected.stdout == b""
                and rejected.stderr.startswith(
                    b"REJECT_C30Q5_INDEPENDENT_VERIFICATION:"
                ),
                "attack rejected:" + name,
            )
            outcomes.append({
                "attack": name,
                "nested_proof_hash_reclosed_if_applicable":
                    name in {
                        "derivative_sign_swap", "full_p_graph_forge",
                        "positive_first_margin_drop", "negative_side_live_forge",
                        "all_three_strata_forge",
                    },
                "top_level_result_sha256_reclosed": True,
                "rejected": True,
            })
        output = {
            "schema": (
                "cm2.round306c30q5.compact-q-11010101-clipped-graph-"
                "coherent-attacks.v1"
            ),
            "status": (
                f"PASS_{len(outcomes)}_OF_{len(attacks)}_COHERENT_ATTACKS_"
                "REJECTED"
            ),
            "baseline_verification_passed": True,
            "independent_verifier_AST_smoke": True,
            "attacks": outcomes,
            "formal_credit": 0,
            "ledger_unchanged": True,
            "compact_q_formal_remaining_origins": 54,
            "source_W_formal_remaining": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Reject, KeyError, StopIteration, OSError, ValueError,
            json.JSONDecodeError) as error:
        print("REJECT_C30Q5_ATTACK_HARNESS:" + str(error), file=sys.stderr)
        return 1


COMPACT_FORGE = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"


if __name__ == "__main__":
    raise SystemExit(main())
