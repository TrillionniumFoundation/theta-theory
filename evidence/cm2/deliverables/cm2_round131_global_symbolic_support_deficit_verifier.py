#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round131-global-symbolic-support-deficit-2026-07-24.json"
OUTPUT = HERE / "cm2-round131-global-symbolic-support-deficit-verification-2026-07-24.json"
ROUND127 = HERE / "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json"
ROUND128 = HERE / "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
ROUND130 = HERE / "cm2-round130-rank3-positive-borel-local-18-field-completion-2026-07-24.json"
CERTIFICATE_SCHEMA = "cm2.round131.global-symbolic-support-deficit.v1"
SCHEMA = "cm2.round131.global-symbolic-support-deficit-verification.v1"
PINS = {
    ROUND127.name: "4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408",
    ROUND128.name: "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    ROUND130.name: "5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5",
}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def strict_bytes(raw):
    def reject_constant(value):
        raise ValueError(value)
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw:
        raise ValueError("encoding")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_constant=reject_constant)
    if type(value) is not dict:
        raise ValueError("top object")
    return value

def load_pinned(path):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINS[path.name]:
        raise ValueError("pin")
    return strict_bytes(raw)

def ordinal_from_key(key_id):
    prefix, ordinal, suffix = key_id.split(":")
    if prefix != "gate5-word" or len(suffix) != 64:
        raise ValueError("key")
    return int(ordinal)

def reconstruct(r127, r128, r130):
    exact = {}
    for row in r127["result"]["exact_path_official_word_registry_incidence_rows"]:
        key_id = row["official_word_key_id"]
        exact[ordinal_from_key(key_id)] = key_id
    r1 = {}
    incidence = r128["result"]["A_base_R1_component_to_global_word_incidence"]
    for row in incidence["component_incidence_rows"]:
        for role in ("source", "destination"):
            ordinal = row[f"{role}_official_word_ordinal"]
            key_id = row[f"{role}_official_word_key_id"]
            if ordinal_from_key(key_id) != ordinal or (ordinal in r1 and r1[ordinal] != key_id):
                raise ValueError("R1 key")
            r1[ordinal] = key_id
    touched = sorted(set(exact) | set(r1))
    rows = []
    for ordinal in touched:
        exact_hit, r1_hit = ordinal in exact, ordinal in r1
        key_id = exact.get(ordinal, r1.get(ordinal))
        if exact_hit and r1_hit and exact[ordinal] != r1[ordinal]:
            raise ValueError("overlap")
        rows.append({"official_word_ordinal": ordinal, "official_word_key_id": key_id,
                     "exact_seed_path_incidence": exact_hit, "base_R1_component_incidence": r1_hit,
                     "support_class": "BOTH_SYMBOLIC_ONLY" if exact_hit and r1_hit else ("EXACT_SEED_ONLY" if exact_hit else "BASE_R1_ONLY")})
    runs, start = [], 0
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
        "scope": "441280-key frozen symbolic registry; incidence evidence only", "upstream_sha256": PINS,
        "global_symbolic_candidate_word_count": 441280, "exact_seed_incident_word_count": len(exact),
        "base_R1_incident_word_count": len(r1), "symbolic_overlap_word_count": len(set(exact) & set(r1)),
        "touched_symbolic_word_count": len(touched), "no_certified_incidence_word_count": 441280-len(touched),
        "touched_symbolic_word_rows": rows, "touched_symbolic_word_rows_sha256": digest(rows),
        "no_certified_incidence_ordinal_runs": runs, "no_certified_incidence_ordinal_runs_sha256": digest(runs),
        "reciprocal_base_R1_unordered_pair_count": incidence["reciprocal_unordered_word_pair_count"],
        "overlap_contract": {"official_word_ordinal": overlap["overlap_official_word_ordinal"], "official_word_key_id": overlap["overlap_official_word_key_id"], "symbolic_word_overlap_only": overlap["symbolic_word_overlap_only"], "same_physical_root": overlap["same_physical_root"], "same_physical_subbranch": overlap["same_physical_subbranch"], "same_operator_block": overlap["same_operator_block"]},
        "priority_frontier": {"next_finite_same_root_target": "16 base-R1 incident official words / 8 reciprocal pairs", "reason": "they already carry certified physical component incidences and local F10/F13/F16 values", "required_before_promotion": ["same-root homogeneous-subbranch materialization", "F1-F18 same-key operator registration", "owner/cemetery and raw-Z/Orlicz control", "independent all-field verifier"]},
        "safety_state": {"positive_Borel_every_exact_fibre_local_maturity": safety["positive_Borel_family_every_exact_fibre_local_field_maturity"], "global_complete_18_field_block_count": 0, "gate5_block_count": 0, "global_gate5_maturity": "10/18", "gate5_status": "NOT_CERTIFIED", "cm2_verdict": "NO-GO_FOR_CLAIM"},
        "strict_nonclaims": ["no-certified-incidence is not an empty-domain decision", "symbolic incidence is not physical, measure, or probability coverage", "the one overlapping word does not identify physical roots or operator blocks", "the positive-Borel local family does not cover the global word universe or arbitrary return depth", "no global Gate5 field or block is promoted"]}

def require(condition, label):
    if not condition:
        raise ValueError(label)

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--certificate", type=Path, default=CERTIFICATE); parser.add_argument("--output", type=Path, default=OUTPUT); args = parser.parse_args()
    require(args.certificate.is_file() and not args.certificate.is_symlink(), "certificate type")
    certificate = strict_bytes(args.certificate.read_bytes())
    require(set(certificate) == {"schema", "result", "result_sha256"}, "envelope")
    require(certificate["schema"] == CERTIFICATE_SCHEMA, "schema")
    expected = reconstruct(load_pinned(ROUND127), load_pinned(ROUND128), load_pinned(ROUND130))
    require(certificate["result"] == expected and certificate["result_sha256"] == digest(expected), "reconstruction")
    rows, runs = expected["touched_symbolic_word_rows"], expected["no_certified_incidence_ordinal_runs"]
    require(len(rows) == 18 and sum(x["count"] for x in runs) == 441262, "counts")
    require(sum(x["support_class"] == "BOTH_SYMBOLIC_ONLY" for x in rows) == 1, "overlap")
    require(expected["overlap_contract"]["same_physical_root"] is False, "nonidentification")
    result = {"status": "PASS", "certificate_result_sha256": certificate["result_sha256"], "reconstructed_touched_symbolic_word_count": 18, "reconstructed_no_certified_incidence_word_count": 441262, "reconstructed_symbolic_overlap_word_count": 1, "reconstructed_reciprocal_base_R1_unordered_pair_count": expected["reciprocal_base_R1_unordered_pair_count"], "producer_imported_or_executed": False, "strict_nonpromotion_checked": True, "safety_state": expected["safety_state"]}
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(canonical({"status": "PASS", "output": str(args.output), "result_sha256": document["result_sha256"]}))

if __name__ == "__main__":
    main()
