#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROUND127 = HERE / "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json"
ROUND128 = HERE / "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
ROUND130 = HERE / "cm2-round130-rank3-positive-borel-local-18-field-completion-2026-07-24.json"
OUTPUT = HERE / "cm2-round131-global-symbolic-support-deficit-2026-07-24.json"
SCHEMA = "cm2.round131.global-symbolic-support-deficit.v1"
PINS = {
    ROUND127.name: "4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408",
    ROUND128.name: "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    ROUND130.name: "5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pinned(path):
    if file_digest(path) != PINS[path.name]:
        raise ValueError(f"pin mismatch: {path.name}")
    return json.loads(path.read_text(encoding="utf-8"))


def ordinal_from_key(key_id):
    prefix, ordinal, suffix = key_id.split(":")
    if prefix != "gate5-word" or len(suffix) != 64:
        raise ValueError("bad official word key")
    return int(ordinal)


def build_result(r127, r128, r130):
    exact_rows = r127["result"]["exact_path_official_word_registry_incidence_rows"]
    incidence_rows = r128["result"]["A_base_R1_component_to_global_word_incidence"]["component_incidence_rows"]
    exact = {ordinal_from_key(row["official_word_key_id"]): row["official_word_key_id"] for row in exact_rows}
    r1 = {}
    for row in incidence_rows:
        for role in ("source", "destination"):
            ordinal = row[f"{role}_official_word_ordinal"]
            key_id = row[f"{role}_official_word_key_id"]
            if ordinal_from_key(key_id) != ordinal:
                raise ValueError("ordinal/key mismatch")
            if ordinal in r1 and r1[ordinal] != key_id:
                raise ValueError("nonunique official key")
            r1[ordinal] = key_id
    touched = sorted(set(exact) | set(r1))
    rows = []
    for ordinal in touched:
        exact_hit = ordinal in exact
        r1_hit = ordinal in r1
        key_id = exact.get(ordinal, r1.get(ordinal))
        if exact_hit and r1_hit and exact[ordinal] != r1[ordinal]:
            raise ValueError("overlap key mismatch")
        rows.append({
            "official_word_ordinal": ordinal,
            "official_word_key_id": key_id,
            "exact_seed_path_incidence": exact_hit,
            "base_R1_component_incidence": r1_hit,
            "support_class": "BOTH_SYMBOLIC_ONLY" if exact_hit and r1_hit else (
                "EXACT_SEED_ONLY" if exact_hit else "BASE_R1_ONLY"
            ),
        })
    runs = []
    start = 0
    for ordinal in touched:
        if start < ordinal:
            runs.append({"first_ordinal": start, "last_ordinal": ordinal - 1, "count": ordinal - start})
        start = ordinal + 1
    if start < 441280:
        runs.append({"first_ordinal": start, "last_ordinal": 441279, "count": 441280 - start})
    overlap = r128["result"]["C_exact_seed_overlap_and_coordinate_separation"]
    safety = r130["result"]
    return {
        "status": "VERIFIED_EXHAUSTIVE_SYMBOLIC_SUPPORT_DEFICIT_DECOMPOSITION",
        "scope": "441280-key frozen symbolic registry; incidence evidence only",
        "upstream_sha256": PINS,
        "global_symbolic_candidate_word_count": 441280,
        "exact_seed_incident_word_count": len(exact),
        "base_R1_incident_word_count": len(r1),
        "symbolic_overlap_word_count": len(set(exact) & set(r1)),
        "touched_symbolic_word_count": len(touched),
        "no_certified_incidence_word_count": 441280 - len(touched),
        "touched_symbolic_word_rows": rows,
        "touched_symbolic_word_rows_sha256": digest(rows),
        "no_certified_incidence_ordinal_runs": runs,
        "no_certified_incidence_ordinal_runs_sha256": digest(runs),
        "reciprocal_base_R1_unordered_pair_count": r128["result"]["A_base_R1_component_to_global_word_incidence"]["reciprocal_unordered_word_pair_count"],
        "overlap_contract": {
            "official_word_ordinal": overlap["overlap_official_word_ordinal"],
            "official_word_key_id": overlap["overlap_official_word_key_id"],
            "symbolic_word_overlap_only": overlap["symbolic_word_overlap_only"],
            "same_physical_root": overlap["same_physical_root"],
            "same_physical_subbranch": overlap["same_physical_subbranch"],
            "same_operator_block": overlap["same_operator_block"],
        },
        "priority_frontier": {
            "next_finite_same_root_target": "16 base-R1 incident official words / 8 reciprocal pairs",
            "reason": "they already carry certified physical component incidences and local F10/F13/F16 values",
            "required_before_promotion": [
                "same-root homogeneous-subbranch materialization",
                "F1-F18 same-key operator registration",
                "owner/cemetery and raw-Z/Orlicz control",
                "independent all-field verifier",
            ],
        },
        "safety_state": {
            "positive_Borel_every_exact_fibre_local_maturity": safety["positive_Borel_family_every_exact_fibre_local_field_maturity"],
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "global_gate5_maturity": "10/18",
            "gate5_status": "NOT_CERTIFIED",
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "no-certified-incidence is not an empty-domain decision",
            "symbolic incidence is not physical, measure, or probability coverage",
            "the one overlapping word does not identify physical roots or operator blocks",
            "the positive-Borel local family does not cover the global word universe or arbitrary return depth",
            "no global Gate5 field or block is promoted",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result(load_pinned(ROUND127), load_pinned(ROUND128), load_pinned(ROUND130))
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(canonical({"status": result["status"], "touched": result["touched_symbolic_word_count"], "deficit": result["no_certified_incidence_word_count"], "result_sha256": document["result_sha256"]}))


if __name__ == "__main__":
    main()
