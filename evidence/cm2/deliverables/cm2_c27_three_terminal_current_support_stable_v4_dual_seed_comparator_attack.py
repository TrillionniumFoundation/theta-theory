#!/usr/bin/env python3
"""Coherent fail-closed attacks against the v4b dual-seed comparator."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


EXPECTED_COMPARATOR_SHA = "1418f525411ee8257f3de05be1ad559c4894a4455bd60a30ba68b60f257ff620"


def load_comparator(path: Path):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_COMPARATOR_SHA:
        raise RuntimeError("comparator pin")
    spec = importlib.util.spec_from_file_location("cm2_v4b_comparator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("comparator loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def close(module, row: dict[str, Any]) -> None:
    row.pop("result_sha256", None)
    row["result_sha256"] = module.digest(row)


def set_path(row: dict[str, Any], pointer: str, value: Any) -> None:
    cursor: Any = row
    parts = pointer.strip("/").split("/")
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    if isinstance(cursor, list):
        cursor[int(parts[-1])] = value
    else:
        cursor[parts[-1]] = value


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--comparator", type=Path, required=True)
    ap.add_argument("--seed1-result", type=Path, required=True)
    ap.add_argument("--seed2-result", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    module = load_comparator(args.comparator)
    seed1 = json.loads(args.seed1_result.read_bytes())
    seed2 = json.loads(args.seed2_result.read_bytes())
    psha = "c20ffeb59b120fa8bbadb255e57566c746277a98def254c8ce153e065ad3baf1"
    xsha = "548dfce1df93b974abde9874dc73e43a8541e9524e15f109c442069b40a0fca0"
    module.compare_objects(seed1, seed2, psha, xsha)

    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = []
    def add(name: str, mutation: Callable[[dict[str, Any]], None], reclose: bool = True) -> None:
        attacks.append((name, mutation, reclose))

    add("extra_top_level_field", lambda r: r.__setitem__("unauthorized", True))
    add("formal_credit_flip", lambda r: r.__setitem__("formal_credit", 1))
    add("manifest_authorized_flip", lambda r: r.__setitem__("manifest_authorized", True))
    add("CM2_promotion", lambda r: r.__setitem__("CM2", "GO"))
    add("invocation_seed_wrong", lambda r: r.__setitem__("invocation_seed", 30637992))
    add("priority_file_sha_flip", lambda r: r["priority_ledger"].__setitem__("file_sha256", "0" * 64))
    add("priority_row_count_decrement", lambda r: r["priority_ledger"].__setitem__("row_count", 91671))
    add("priority_sequence_sha_flip", lambda r: r["priority_ledger"].__setitem__("row_sequence_sha256", "0" * 64))
    add("positive_file_sha_flip", lambda r: r["fresh_positive_primitive_scan"].__setitem__("positive_ledger_file_sha256", "0" * 64))
    add("union_count_decrement", lambda r: r["primitive_pair_sets"].__setitem__("union", 91671))
    add("positive_count_decrement", lambda r: r["primitive_pair_sets"].__setitem__("POSITIVE_C19", 55531))
    add("intersection_fabrication", lambda r: r["primitive_pair_sets"].__setitem__("POSITIVE_intersection_COMPLETE", 1))
    add("terminal_signed_decrement", lambda r: r["unique_priority_assignment_census"].__setitem__("SIGNED_BOUNDARY_FACES", 25451))
    add("terminal_complete_increment", lambda r: r["unique_priority_assignment_census"].__setitem__("COMPLETE_BOUNDARY_FACES", 10689))
    add("terminal_positive_flip", lambda r: r["unique_priority_assignment_census"].__setitem__("POSITIVE_VOLUME_CARRIERS", 55533))
    add("candidate_governance_flip", lambda r: r["candidate_governance"].__setitem__("C27_FAMILIES_imported_or_read", True))
    add("static_C15_pin_flip", lambda r: r["root_input_capture"]["attestations"]["cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"].__setitem__("sha256", "0" * 64))
    add("static_crosswalk_pin_flip", lambda r: r["root_input_capture"]["attestations"]["v3_crosswalk"].__setitem__("sha256", "0" * 64))
    add("nonwhitelisted_positive_inode_flip", lambda r: r["root_input_capture"]["attestations"]["self_produced_positive_ledger"]["stat_fingerprint"].__setitem__(0, 999))
    add("whitelist_difference_removed", lambda r: set_path(r, "/fresh_positive_primitive_scan/inner_result_sha256", seed1["fresh_positive_primitive_scan"]["inner_result_sha256"]))
    add("whitelist_path_difference_removed", lambda r: set_path(r, "/root_input_capture/attestations/self_produced_positive_ledger/path", seed1["root_input_capture"]["attestations"]["self_produced_positive_ledger"]["path"]))
    add("whitelist_inode_difference_removed", lambda r: set_path(r, "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/1", seed1["root_input_capture"]["attestations"]["self_produced_inner_result"]["stat_fingerprint"][1]))
    add("result_closure_flip", lambda r: r.__setitem__("result_sha256", "0" * 64), False)
    add("schema_flip", lambda r: r.__setitem__("schema", r["schema"] + ".MUTATED"))

    rows = []
    for ordinal, (name, mutation, reclose) in enumerate(attacks):
        candidate = copy.deepcopy(seed2)
        mutation(candidate)
        if reclose:
            close(module, candidate)
        rejected = False
        reason = None
        try:
            module.compare_objects(seed1, candidate, psha, xsha)
        except (module.Reject, KeyError, IndexError, TypeError, ValueError) as error:
            rejected, reason = True, str(error)
        if not rejected:
            raise RuntimeError("accepted coherent attack:" + name)
        body = {"attack": name, "ordinal": ordinal, "rejected": True,
                "rejection_reason": reason,
                "schema": "cm2.c27-independent.current-support-91672.dual-seed-comparator.attack-row.v1"}
        body["row_sha256"] = module.digest(body)
        rows.append(body)
    result = {
        "schema": "cm2.c27-independent.current-support-91672.dual-seed-comparator.attacks.v1",
        "status": "PASS_ALL_COHERENT_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(rows),
        "rejected_count": len(rows),
        "accepted_count": 0,
        "comparator_source_sha256": EXPECTED_COMPARATOR_SHA,
        "formal_credit": 0,
        "manifest_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "attacks": rows,
    }
    result["result_sha256"] = module.digest(result)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(module.canon(result) + b"\n")
    print(module.canon({"result": str(args.out), "result_sha256": result["result_sha256"],
                        "rejected": len(rows)}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
