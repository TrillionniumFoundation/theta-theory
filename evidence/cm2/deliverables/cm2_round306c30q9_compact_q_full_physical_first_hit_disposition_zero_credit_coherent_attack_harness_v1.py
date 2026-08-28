#!/usr/bin/env python3
"""Coherent mutation attacks for the zero-credit C30q9 research candidate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
VERIFIER = HERE / (
    "cm2_round306c30q9_compact_q_full_physical_first_hit_disposition_"
    "zero_credit_independent_verifier_v1.py"
)
VERIFIER_SHA256 = "2b6e49ffd8fcaa0f3fd307bfdc539a99b2ac62fd8de0103a44a204cdff331155"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def safe_read(path: Path) -> bytes:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical file")
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular single-link file")
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
          before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_size,
                                  after.st_mtime_ns, after.st_ctime_ns), "stable file")
    return raw


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    target: Any = value
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = replacement


def path_attack(path: tuple[Any, ...], replacement: Any) -> Callable[[dict[str, Any]], None]:
    return lambda value: set_path(value, path, replacement)


def finalize(value: dict[str, Any]) -> None:
    value["result_sha256"] = digest(value["result"])


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage: attacks CANDIDATE_JSON")
        candidate_path = Path(argv[1]).absolute()
        raw = safe_read(candidate_path)
        candidate = json.loads(raw.decode("utf-8", "strict"))
        need(type(candidate) is dict and raw == canonical(candidate) + b"\n"
             and candidate["result_sha256"] == digest(candidate["result"]),
             "canonical base candidate")
        need(hashlib.sha256(safe_read(VERIFIER)).hexdigest() == VERIFIER_SHA256,
             "verifier pin")
        r = candidate["result"]
        bridge_index = 0
        miss_index = 0
        route_excluded_index = next(
            index for index, row in enumerate(r["route_resolution_rows"])
            if row["research_disposition"] == "EXCLUDED"
        )
        route_mixed_index = next(
            index for index, row in enumerate(r["route_resolution_rows"])
            if row["research_disposition"] == "RESOLVED_MIXED"
        )
        ledger_mixed_index = next(
            index for index, row in enumerate(r["research_disposition_ledger"])
            if row["research_disposition"] == "RESOLVED_MIXED"
        )
        attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            ("top_schema", path_attack(("schema",), "cm2.fake")),
            ("status", path_attack(("result", "status"), "PASS_FAKE")),
            ("verdict", path_attack(("result", "verdict"), "FORMAL_RELEASE")),
            ("q8_pin", path_attack(("result", "authority_binding", "Q8", "candidate_sha256"), "0" * 64)),
            ("geometry_pin", path_attack(("result", "authority_binding", "geometry_registry_sha256"), "0" * 64)),
            ("T1_family_drop", lambda value: value["result"]["physical_target_completeness"]
             ["horizon_1"]["possible_targets"].pop()),
            ("T32_family_drop", lambda value: value["result"]["physical_target_completeness"]
             ["horizon_3_over_2"]["possible_targets"].pop()),
            ("T1_margin", path_attack(("result", "physical_target_completeness", "horizon_1",
                                       "first_excluded_squared_distance_margin"), "0")),
            ("self_reentry", path_attack(("result", "physical_target_completeness", "source_self",
                                          "strictly_greater_than_source_radius_squared"), False)),
            ("target_tie", path_attack(("result", "physical_target_completeness",
                                        "strict_obstacle_disjointness",
                                        "simultaneous_first_target_tie_impossible"), False)),
            ("template_count", path_attack(("result", "template_inventory",
                                             "irreducible_semantic_template_count"), 2)),
            ("switch_count", path_attack(("result", "template_inventory", "route_template_minimality",
                                           "distinct_switch_value_count"), 1)),
            ("one_switch", path_attack(("result", "template_inventory", "route_template_minimality",
                                        "one_shared_switch_is_impossible"), False)),
            ("root_subdivision", path_attack(("result", "template_inventory",
                                              "historic_root_by_root_subdivision_used"), True)),
            ("bridge_disposition", path_attack(("result", "bridge_rows", bridge_index,
                                                 "research_disposition"), "RESOLVED_MIXED")),
            ("bridge_seam_owner", path_attack(("result", "bridge_rows", bridge_index,
                                                "switch_seam", "owner"), "left")),
            ("miss_selected", path_attack(("result", "global_miss_resolution_rows", miss_index,
                                            "selected_unique_first_target"), "W[1,0]")),
            ("miss_competitor", path_attack(("result", "global_miss_resolution_rows", miss_index,
                                              "all_twenty_competitors_no_contact_or_behind_or_self"), False)),
            ("route_excluded_flip", path_attack(("result", "route_resolution_rows",
                                                  route_excluded_index, "research_disposition"),
                                                 "RESOLVED_MIXED")),
            ("route_switch_owner", path_attack(("result", "route_resolution_rows",
                                                 route_mixed_index, "switch_seam", "owner"), "left_W")),
            ("mixed_live", path_attack(("result", "route_resolution_rows", route_mixed_index,
                                        "LIVE_and_EXCLUDED_subboxes_are_disjoint_and_nonempty"), False)),
            ("mixed_chart", path_attack(("result", "route_resolution_rows", route_mixed_index,
                                         "strict_positive_measure_LIVE_subbox", "strict_outgoing_W_chart",
                                         "outgoing_chart"), "N")),
            ("half_open_rule", path_attack(("result", "lower_strata_half_open_closure",
                                            "outgoing_chart_partition", "seam_owner_rule"),
                                           "N_OR_S_OWNS")),
            ("atomic_rebuild", path_attack(("result", "lower_strata_half_open_closure",
                                            "formal_atomic_3D_2D_1D_0D_rebuild_still_required"), False)),
            ("ledger_duplicate", lambda value: value["result"]["research_disposition_ledger"]
             .__setitem__(1, copy.deepcopy(value["result"]["research_disposition_ledger"][0]))),
            ("ledger_mixed_flip", path_attack(("result", "research_disposition_ledger",
                                                ledger_mixed_index, "research_disposition"), "EXCLUDED")),
            ("closure_excluded", path_attack(("result", "classification_closure",
                                               "research_EXCLUDED_candidates"), 45)),
            ("closure_mixed", path_attack(("result", "classification_closure",
                                            "research_RESOLVED_MIXED_candidates"), 9)),
            ("closure_unresolved", path_attack(("result", "classification_closure",
                                                 "unresolved_research_origins"), 1)),
            ("formal_mint", path_attack(("result", "classification_closure",
                                         "formal_dispositions_minted"), 54)),
            ("handoff_before", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                             "before", "excluded"), 74769)),
            ("handoff_after", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                            "candidate_after", "excluded"), 74813)),
            ("handoff_credit", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                             "candidate_credit", "EXCLUDED"), 45)),
            ("predecessor_present", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                                  "predecessor_exists_in_this_audit"), True)),
            ("terminal_adapter", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                               "terminal_adapter_present"), True)),
            ("formal_54_to_0", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                            "formal_54_to_0_minted"), True)),
            ("release_state", path_attack(("result", "future_C30f_gated_handoff_candidate",
                                           "release_state"), "RELEASED")),
            ("formal_credit", path_attack(("result", "formal_boundary", "formal_credit"), 54)),
            ("formal_remaining", path_attack(("result", "formal_boundary",
                                               "source_W_formal_remaining"), 0)),
            ("compact_formal_remaining", path_attack(("result", "formal_boundary",
                                                       "compact_q_formal_remaining_origins"), 0)),
            ("terminal_gate", path_attack(("result", "formal_boundary", "terminal_gate_present"), True)),
            ("formal_predecessor", path_attack(("result", "formal_boundary",
                                                "can_serve_as_compact_q_formal_predecessor"), True)),
            ("CM2", path_attack(("result", "formal_boundary", "CM2"), "GO_FOR_CLAIM")),
            ("extra_result_member", lambda value: value["result"].__setitem__("formal_release", True)),
        ]
        rejected: list[dict[str, Any]] = []
        environment = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                       "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "30990083"}
        with tempfile.TemporaryDirectory(prefix="cm2-c30q9-attacks-") as directory:
            work = Path(directory)
            for index, (name, mutate) in enumerate(attacks):
                attacked = copy.deepcopy(candidate)
                mutate(attacked)
                finalize(attacked)
                path = work / f"attack-{index:02d}.json"
                path.write_bytes(canonical(attacked) + b"\n")
                process = subprocess.run(
                    [sys.executable, "-B", "-s", str(VERIFIER), str(path)],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    cwd=work, env=environment, timeout=60, check=False,
                )
                need(process.returncode == 2 and process.stdout == b""
                     and process.stderr.startswith(b"REJECT_C30Q9_VERIFY:"),
                     "attack not rejected:" + name)
                rejected.append({"attack": name, "numeric_exit_code": 2,
                                 "stdout_empty": True, "rejected": True})
        coverage = {
            "candidate_schema_and_status": True,
            "authority_and_geometry_pins": True,
            "physical_target_completeness": True,
            "self_reentry_and_target_ties": True,
            "template_minimality_and_no_root_split": True,
            "bridge_and_unique_first_semantics": True,
            "mixed_live_excluded_subboxes": True,
            "half_open_and_lower_strata_boundary": True,
            "54_origin_partition_and_44_plus_10_counts": True,
            "future_C30f_handoff_arithmetic": True,
            "terminal_and_formal_nonpromotion": True,
        }
        result = {
            "schema": "cm2.round306c30q9.coherent-attacks.zero-credit.v1",
            "status": "PASS_ALL_COHERENT_C30Q9_MUTATIONS_REJECTED",
            "attack_count": len(attacks), "rejected": len(rejected),
            "all_rejected": len(rejected) == len(attacks),
            "mandatory_coverage": coverage,
            "attacks": rejected,
            "formal_credit": 0, "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54, "formal_54_to_0_minted": False,
        }
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, Reject,
            subprocess.SubprocessError, subprocess.TimeoutExpired) as error:
        sys.stderr.write("REJECT_C30Q9_ATTACKS:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
