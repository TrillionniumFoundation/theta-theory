#!/usr/bin/env python3
"""Coherent mutation harness for the retained-continuation subgate."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
STREAM = HERE / "cm2_c27_retained_continuation_stream_probe.py"
SQLITE = HERE / "cm2_c27_retained_continuation_sqlite_verifier.py"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def baseline_claim(stream: dict[str, Any], sqlite: dict[str, Any]) -> dict[str, Any]:
    for key in ("candidate_count", "chart_census",
                "candidate_representation_ids_sha256", "candidate_row_sequence_sha256"):
        need(stream["candidate_universe"][key] == sqlite["candidate_universe"][key],
             "cross implementation:" + key)
    need(stream["C20D_source_semantic_census"] == sqlite["C20D_source_semantic_census"],
         "cross implementation semantic census")
    need(stream["C20D_relation_census"] == sqlite["C20D_relation_census"],
         "cross implementation relation census")
    need(stream["join_gap_census"] == sqlite["join_gap_census"],
         "cross implementation gaps")
    need(stream["input_pins"] == sqlite["input_pins"], "cross implementation pins")
    return {
        "schema": "cm2.c27.retained-continuation-subgate-material-claim.v1",
        "status": "PASS_LOCAL_ZERO_CREDIT__RETAINED_CONTINUATION_DUAL_IMPLEMENTATION",
        "candidate_count": stream["candidate_universe"]["candidate_count"],
        "chart_census": stream["candidate_universe"]["chart_census"],
        "candidate_representation_ids_sha256": stream["candidate_universe"]["candidate_representation_ids_sha256"],
        "candidate_row_sequence_sha256": stream["candidate_universe"]["candidate_row_sequence_sha256"],
        "source_semantic_census": stream["C20D_source_semantic_census"],
        "relation_census": stream["C20D_relation_census"],
        "join_gap_census": stream["join_gap_census"],
        "unique_assignment": stream["unique_assignment"],
        "attachment_terminal_overlap": stream["attachment_terminal_overlap_after_required_C20D_SOURCE_SPLIT"],
        "input_pins": stream["input_pins"],
        "stream_script_sha256": file_hash(STREAM),
        "sqlite_script_sha256": file_hash(SQLITE),
        "stream_result_sha256": stream["result_sha256"],
        "sqlite_result_sha256": sqlite["result_sha256"],
        "stream_seed_byte_identical_required": True,
        "sqlite_seed_byte_identical_required": True,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_PENDING_COMPLETE_TWENTY_TERMINAL_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def validate(claim: dict[str, Any], reference: dict[str, Any]) -> None:
    need(set(claim) == set(reference), "claim exact keys")
    for key, expected in reference.items():
        need(claim.get(key) == expected, "claim binding:" + key)
    need(claim["candidate_count"] == 276, "candidate denominator")
    need(sum(claim["chart_census"].values()) == 276 and
         set(claim["chart_census"].values()) == {69}, "chart partition")
    need(sum(claim["source_semantic_census"].values()) == 2_520, "semantic denominator")
    need(claim["source_semantic_census"]["ADJACENT_POSITIVE_T_CONTINUATION"] == 276,
         "adjacent semantic")
    need(claim["relation_census"] == {
        "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE": 276,
        "STRICT_SUBCOVER_OF_OWNER_SUPPORT": 2_244,
    }, "relation partition")
    need(all(value == 0 for value in claim["join_gap_census"].values()), "zero gaps")
    need(claim["attachment_terminal_overlap"] == 0, "terminal disjointness")
    need(claim["formal_credit"] == 0 and claim["CM2"] == "NO-GO_FOR_CLAIM",
         "strict nonpromotion")


def mutate_digest(value: str) -> str:
    return ("0" if value[0] != "0" else "1") + value[1:]


def main() -> int:
    stream_module = load(STREAM, "cm2_retained_stream_attack")
    sqlite_module = load(SQLITE, "cm2_retained_sqlite_attack")
    stream = stream_module.build(30627411)
    sqlite = sqlite_module.build(30627412)
    reference = baseline_claim(stream, sqlite)
    validate(reference, reference)

    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []
    attacks.append(("drop_candidate", lambda d: d.__setitem__("candidate_count", 275)))
    attacks.append(("add_candidate", lambda d: d.__setitem__("candidate_count", 277)))
    attacks.append(("empty_candidate_set", lambda d: d.__setitem__("candidate_count", 0)))
    attacks.append(("reinject_276_into_attachment", lambda d: d.__setitem__("attachment_terminal_overlap", 276)))
    attacks.append(("promote_attachment_overlap_boolean", lambda d: d.__setitem__("attachment_terminal_overlap", True)))
    attacks.append(("flip_candidate_id_commitment", lambda d: d.__setitem__(
        "candidate_representation_ids_sha256", mutate_digest(d["candidate_representation_ids_sha256"]))))
    attacks.append(("flip_candidate_row_commitment", lambda d: d.__setitem__(
        "candidate_row_sequence_sha256", mutate_digest(d["candidate_row_sequence_sha256"]))))
    attacks.append(("drop_east_chart", lambda d: d["chart_census"].__setitem__("G:E", 68)))
    attacks.append(("move_chart_coherently", lambda d: (d["chart_census"].__setitem__("G:E", 68),
                                                        d["chart_census"].__setitem__("G:N", 70))))
    attacks.append(("reclassify_strict_as_adjacent", lambda d: (
        d["source_semantic_census"].__setitem__("ADJACENT_POSITIVE_T_CONTINUATION", 277),
        d["source_semantic_census"].__setitem__("EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER", 719),
        d["relation_census"].__setitem__("ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE", 277),
        d["relation_census"].__setitem__("STRICT_SUBCOVER_OF_OWNER_SUPPORT", 2243),
        d.__setitem__("candidate_count", 277))))
    attacks.append(("reclassify_adjacent_as_strict", lambda d: (
        d["source_semantic_census"].__setitem__("ADJACENT_POSITIVE_T_CONTINUATION", 275),
        d["source_semantic_census"].__setitem__("EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER", 721),
        d["relation_census"].__setitem__("ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE", 275),
        d["relation_census"].__setitem__("STRICT_SUBCOVER_OF_OWNER_SUPPORT", 2245),
        d.__setitem__("candidate_count", 275))))
    attacks.append(("rename_adjacent_semantic", lambda d: d["source_semantic_census"].__setitem__(
        "ADJACENT_POSITIVE_T_CONTINUATION_FORGED", d["source_semantic_census"].pop("ADJACENT_POSITIVE_T_CONTINUATION"))))
    attacks.append(("rename_face_relation", lambda d: d["relation_census"].__setitem__(
        "ADJACENT_CONTINUATION_SHARED_PARTIAL_FACE", d["relation_census"].pop(
            "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE"))))
    for gap in reference["join_gap_census"]:
        attacks.append(("inject_gap_" + gap, lambda d, name=gap: d["join_gap_census"].__setitem__(name, 1)))
    attacks.append(("flip_C20D_pin", lambda d: d["input_pins"].__setitem__(
        stream_module.C20D, mutate_digest(d["input_pins"][stream_module.C20D]))))
    attacks.append(("flip_C20A_pin", lambda d: d["input_pins"].__setitem__(
        stream_module.C20A, mutate_digest(d["input_pins"][stream_module.C20A]))))
    attacks.append(("flip_stream_script_pin", lambda d: d.__setitem__(
        "stream_script_sha256", mutate_digest(d["stream_script_sha256"]))))
    attacks.append(("flip_sqlite_script_pin", lambda d: d.__setitem__(
        "sqlite_script_sha256", mutate_digest(d["sqlite_script_sha256"]))))
    attacks.append(("flip_stream_result", lambda d: d.__setitem__(
        "stream_result_sha256", mutate_digest(d["stream_result_sha256"]))))
    attacks.append(("flip_sqlite_result", lambda d: d.__setitem__(
        "sqlite_result_sha256", mutate_digest(d["sqlite_result_sha256"]))))
    attacks.append(("drop_stream_seed_identity", lambda d: d.__setitem__(
        "stream_seed_byte_identical_required", False)))
    attacks.append(("drop_sqlite_seed_identity", lambda d: d.__setitem__(
        "sqlite_seed_byte_identical_required", False)))
    attacks.append(("inflate_formal_credit", lambda d: d.__setitem__("formal_credit", 1)))
    attacks.append(("promote_C27", lambda d: d.__setitem__("C27_C28_C29", "PASS")))
    attacks.append(("promote_CM2", lambda d: d.__setitem__("CM2", "GO_FOR_CLAIM")))
    attacks.append(("forge_status", lambda d: d.__setitem__("status", "PASS_FORMAL_CREDIT")))
    attacks.append(("drop_unique_assignment", lambda d: d.__setitem__("unique_assignment", "UNRESOLVED")))
    attacks.append(("extra_unbound_field", lambda d: d.__setitem__("producer_only", False)))

    rejected: list[str] = []
    for attack_id, mutation in attacks:
        candidate = copy.deepcopy(reference)
        mutation(candidate)
        try:
            validate(candidate, reference)
        except Failure:
            rejected.append(attack_id)
        else:
            raise Failure("unexpected acceptance:" + attack_id)
    need(len(rejected) == len(attacks), "all attacks rejected")
    result = {
        "schema": "cm2.c27.retained-continuation-coherent-attack-harness.v1",
        "status": f"PASS_{len(attacks)}_COHERENT_RETAINED_CONTINUATION_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "rejected_attacks": rejected,
        "baseline_candidate_count": 276,
        "baseline_candidate_representation_ids_sha256": reference["candidate_representation_ids_sha256"],
        "baseline_candidate_row_sequence_sha256": reference["candidate_row_sequence_sha256"],
        "stream_result_sha256": stream["result_sha256"],
        "sqlite_result_sha256": sqlite["result_sha256"],
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_PENDING_COMPLETE_TWENTY_TERMINAL_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(canonical({**result, "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
