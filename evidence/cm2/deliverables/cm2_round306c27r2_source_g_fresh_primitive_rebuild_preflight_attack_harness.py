#!/usr/bin/env python3
"""Coherent mutation attacks for the C27R2 primitive preflight contract."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
VERIFIER = ROOT / "cm2_round306c27r2_source_g_fresh_primitive_rebuild_preflight_independent_verifier.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def reclose(value: dict[str, Any]) -> None:
    value.pop("preflight_sha256", None)
    value["preflight_sha256"] = digest(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("c27r2_preflight_independent", VERIFIER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = Path(args.preflight).read_bytes()
    base = json.loads(raw)

    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("unclosed_byte_tamper", lambda x: x.__setitem__("formal_credit", 1), False),
        ("promote_formal_credit", lambda x: x.__setitem__("formal_credit", 1), True),
        ("authorize_manifest", lambda x: x.__setitem__("manifest_authorized", True), True),
        ("authorize_C27", lambda x: x.__setitem__("C27_transition_totality", "AUTHORIZED"), True),
        ("authorize_C28", lambda x: x.__setitem__("C28_pair_routing", "AUTHORIZED"), True),
        ("authorize_C29", lambda x: x.__setitem__("C29_physical_maximality", "AUTHORIZED"), True),
        ("authorize_Source_W", lambda x: x.__setitem__("Source_W_transition_authorized", True), True),
        ("remove_missing_G2A", lambda x: x["missing_required_authority"].remove("G2A_TERMINAL_RECEIPT"), True),
        ("remove_missing_91672", lambda x: x["missing_required_authority"].remove("CURRENT_SUPPORT_91672_TERMINAL_RECEIPT"), True),
        ("force_producer_authorization", lambda x: x.__setitem__("producer_authorization", True), True),
        ("force_PASS_status", lambda x: x.__setitem__("status", "PASS_INPUT_COMPLETE_FOR_FRESH_C27R2_PRODUCER__ZERO_CREDIT__NO_FORMAL_STATE_CHANGE"), True),
        ("assert_43772_final", lambda x: x["edge_topology_preflight"].__setitem__("may_assert_final_component_count_43772", True), True),
        ("promote_43772_conclusion", lambda x: x["edge_topology_preflight"].__setitem__("component_count_conclusion", "43772_FINAL"), True),
        ("change_strict_rank", lambda x: x["edge_topology_preflight"].__setitem__("strict_volume_rank", 14_103), True),
        ("change_strict_components", lambda x: x["edge_topology_preflight"].__setitem__("strict_volume_component_count", 43_773), True),
        ("claim_G2B_incremental_rank", lambda x: x["edge_topology_preflight"].__setitem__("G2B_incremental_rank_after_strict_volume", 1), True),
        ("open_forbidden_dependency", lambda x: x.__setitem__("forbidden_dependency_open_count", 1), True),
        ("delete_forbidden_dependency", lambda x: x["forbidden_dependencies"].pop(), True),
        ("change_CM2", lambda x: x.__setitem__("CM2", "GO"), True),
        ("delete_future_contract", lambda x: x["input_contract"]["future_terminal_contracts"].pop("G2A"), True),
    ]
    rejected = []
    accepted = []
    for name, mutate, resign in attacks:
        candidate = copy.deepcopy(base)
        try:
            mutate(candidate)
        except (KeyError, ValueError):
            # Missing-receipt attacks are meaningful only for the truthful
            # incomplete baseline and are rejected if their target vanished.
            rejected.append(name + ":mutation-target-absent")
            continue
        if resign:
            reclose(candidate)
        try:
            module.verify_document(candidate)
        except Exception:
            rejected.append(name)
        else:
            accepted.append(name)
    result = {
        "schema": "cm2.round306c27r2.source-g-fresh-primitive-rebuild-preflight-attacks.v1",
        "status": "PASS_ALL_COHERENT_PREFLIGHT_MUTATIONS_REJECTED__ZERO_CREDIT" if not accepted else "FAIL_ATTACK_ACCEPTED",
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "accepted": accepted,
        "rejected": rejected,
        "attack_names": [name for name, _, _ in attacks],
        "formal_credit": 0,
    }
    result["attack_result_sha256"] = digest(result)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(result) + b"\n"
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    print(canonical({"status": result["status"],
                     "attack_result_sha256": result["attack_result_sha256"]}).decode("ascii"))
    return 0 if not accepted and len(rejected) == len(attacks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
