#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round148-atomic-future-input-admission-2026-07-24.json"
OUTPUT = HERE / "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json"
SCHEMA = "cm2.round148.atomic-future-input-admission-verification.v1"
CERT_SCHEMA = "cm2.round148.atomic-future-input-admission.v1"

FILES = {
    "r144": ("cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json", "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f"),
    "r147": ("cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json", "db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee"),
    "r145s": ("cm2_round145_finite_connected_leaf_corridor_atlas.py", "6deed0506b0105eee9ee9a89dd4c28ee9bed81aa4922586eb8b8005a433ba4c7"),
    "r145": ("cm2-round145-finite-connected-leaf-corridor-atlas-2026-07-24.json", "5edac93e1425c72992ab671f3b3f7db269d236819ea3ad689b612505426ccec6"),
    "r145vsrc": ("cm2_round145_finite_connected_leaf_corridor_atlas_verifier.py", "47f283b48bba7c28a94ca01fcaec0389728c1aebd90d31a1f8c36fca0ee4f255"),
    "r145v": ("cm2-round145-finite-connected-leaf-corridor-atlas-verification-2026-07-24.json", "6101a4bdd7e1bea160a6d1bf36f0b4be281d340f217eb87d38b47f9961fd24a8"),
    "r146s": ("cm2_round146_physical_centered_jet_2d_frontier.py", "db0241c9bae4937cd1a01f23b4951247fa69fd16d9b06a75d446e5336c9930c4"),
    "r146": ("cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json", "38ad7cdd5a2af7cda94792a31a8a83275022f943e8e6b9801ee4bece73b04eac"),
    "r146vsrc": ("cm2_round146_physical_centered_jet_2d_frontier_verifier.py", "d75af7cc251c212a11522a8884ad9afbb983197ba9e6e0d43598ffe06916ad44"),
    "r146v": ("cm2-round146-physical-centered-jet-2d-frontier-verification-2026-07-24.json", "c25646413467deb2c1c5ea68f92e97116546eb62333596afc61973430e002dd4"),
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def strict_json_bytes(raw):
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


def pinned(key, parse=True):
    name, expected = FILES[key]
    raw = (HERE / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"pin {key}")
    return strict_json_bytes(raw) if parse else expected


def reconstruct():
    r144, r147 = pinned("r144"), pinned("r147")
    r145, r145v = pinned("r145"), pinned("r145v")
    r146, r146v = pinned("r146"), pinned("r146v")
    for key in ("r145s", "r145vsrc", "r146s", "r146vsrc"):
        pinned(key, parse=False)
    if r145v["result"]["status"] != "PASS" or r146v["result"]["status"] != "PASS":
        raise ValueError("PASS")
    if r145v["result"]["certificate_result_sha256"] != r145["result_sha256"]:
        raise ValueError("R145 result")
    if r146v["result"]["pins"]["certificate_result_sha256"] != r146["result_sha256"]:
        raise ValueError("R146 result")
    old_slots = r147["result"]["Round144_atomic_migration_frontier"]["future_input_slots"]
    if any(row["status"] != "UNBOUND_NULL_FUTURE_INPUT" for row in old_slots):
        raise ValueError("old slots")
    slots = [
        {
            "slot": "Round145_leaf_corridor_atlas",
            "status": "ATOMICALLY_BOUND_AND_VERIFIED",
            "source_sha256": FILES["r145s"][1],
            "certificate_sha256": FILES["r145"][1],
            "verifier_sha256": FILES["r145vsrc"][1],
            "verification_sha256": FILES["r145v"][1],
            "verification_result_sha256": r145v["result_sha256"],
            "acceptance_outcome": "D05_D06_D08_CERTIFIED",
        },
        {
            "slot": "Round146_two_generator_outer_atlas",
            "status": "ATOMICALLY_BOUND_AND_VERIFIED",
            "source_sha256": FILES["r146s"][1],
            "certificate_sha256": FILES["r146"][1],
            "verifier_sha256": FILES["r146vsrc"][1],
            "verification_sha256": FILES["r146v"][1],
            "verification_result_sha256": r146v["result_sha256"],
            "acceptance_outcome": "LOCAL_2D_EVIDENCE_ACCEPTED__D02_REMAINS_BLOCKED",
        },
    ]
    states = {
        "D00": ("READY", "Round144"),
        "D01": ("READY", "Round144"),
        "D02": ("BLOCKED", "Round146 proves local two-cell atlas and one D3 frontier only"),
        "D03": ("BLOCKED", "requires D02 and complete earlier-rank exclusion"),
        "D04": ("BLOCKED", "requires D03"),
        "D05": ("CERTIFIED", "Round145 complete connected leaf corridor"),
        "D06": ("CERTIFIED", "Round145 exact v1 least leaf rank and natural k=0"),
        "D07": ("BLOCKED", "D04 remains blocked although D06 is certified"),
        "D08": ("CERTIFIED", "Round145 connected monotone image and corrected v1 recut registry"),
        "D09": ("BLOCKED", "requires D04 and D07"),
        "D10": ("BLOCKED", "requires D09 and active-representation crosswalk"),
        "D11": ("BLOCKED", "requires D10"),
        "D12": ("BLOCKED", "requires D11 and same-root Round54 serialization"),
        "D13": ("BLOCKED", "requires D12 and typed Omega_j/q_j serialization"),
    }
    dag_rows = [{
        "node_id": row["node_id"],
        "operation": row["operation"],
        "depends_on": row["depends_on"],
        "round148_status": states[row["node_id"]][0],
        "evidence_or_blocker": states[row["node_id"]][1],
    } for row in r144["result"]["migration_DAG_rows"]]
    branch = r145["result"]["boundary_and_physical_branch_proof"]
    leaf = r145["result"]["promoted_Round137_v1_leaf_rank"]
    short = r145["result"]["promoted_v1_source_short_cell"]
    image = r145["result"]["promoted_v1_image_recut"]
    d02 = r146["result"]["Round144_D02_status"]
    pins = {name: sha for name, sha in FILES.values()}
    return {
        "status": "CERTIFIED_ATOMIC_FUTURE_INPUT_ADMISSION_AND_PARTIAL_DAG_ADVANCE",
        "supersedes_audit_generation": "Round147",
        "migration_registry_id": r144["result"]["migration_registry_id"],
        "atomic_future_input_slots": slots,
        "atomic_future_input_slots_sha256": digest(slots),
        "migration_DAG_rows": dag_rows,
        "migration_DAG_rows_sha256": digest(dag_rows),
        "certified_DAG_nodes": ["D00", "D01", "D05", "D06", "D08"],
        "blocked_DAG_nodes": ["D02", "D03", "D04", "D07", "D09", "D10", "D11", "D12", "D13"],
        "first_exact_blocker": {
            "node_id": "D02",
            "operation": "complete_2D_centered_jet_outer_atlas",
            "maximal_component_outer_atlas_complete": d02["maximal_component_outer_atlas_complete"],
            "all_event_frontiers_exhausted": d02["all_event_frontiers_exhausted"],
            "D03_least_rank_negative_oracle_authorized": d02["D03_least_rank_negative_oracle_authorized"],
            "next_required_object": "finite connected maximal 2D leaf-corridor atlas with every exit and physical event frontier exhausted",
        },
        "Round145_promotions": {
            "connected_physical_open_branch_certified": branch["connected_physical_open_branch_certified"],
            "global_two_dimensional_component_maximality_certified": branch["global_two_dimensional_component_maximality_certified"],
            "canonical_H1_x_level": leaf["canonical_H1_x_level"],
            "canonical_H1_x_rank_sha256": leaf["canonical_H1_x_least_rank"]["contained_primitive_basis_rank"]["sha256_of_decimal"],
            "corrected_left_anchored_natural_short_cell_k": short["corrected_left_anchored_natural_short_cell_k"],
            "corrected_v1_source_cell_id": short["corrected_v1_source_cell_id"],
            "corrected_v1_image_recut_registry_id": image["corrected_v1_image_recut_registry_id"],
            "endpoint_difference_is_complete_image_span": image["endpoint_difference_is_complete_image_span"],
        },
        "identifier_ledger": {key: None for key in (
            "component_v1_id", "parent_W_v1_id", "restriction_v1_id", "owner_v1_id",
            "t54_v1_token", "Omega_j_v1_record", "q_j_v1_output"
        )},
        "gate5_global_ledger": {
            "strictly_satisfied_field_indices": [1, 2, 3, 4, 7, 8, 9, 12, 13, 16],
            "strictly_blocked_field_indices": [5, 6, 10, 11, 14, 15, 17, 18],
            "global_maturity_before": "10/18",
            "global_maturity_after": "10/18",
            "newly_promoted_field_indices": [],
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "binding a verified future input does not imply that every admissible DAG node closes",
            "Round146 is local two-generator evidence and does not close D02",
            "Round145 closes D05 D06 D08 but cannot mint parent-W or restriction while D04 is blocked",
            "no prospective v1 identifier aliases a historical Round27/35/50/54/67 identifier",
            "no local or prospective evidence receives global Gate5 field credit",
        ],
        "upstream_sha256": pins,
    }


def require(condition, label):
    if not condition:
        raise ValueError(label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    require(args.certificate.is_file() and not args.certificate.is_symlink(), "certificate type")
    certificate = strict_json_bytes(args.certificate.read_bytes())
    require(set(certificate) == {"schema", "result", "result_sha256"}, "envelope")
    require(certificate["schema"] == CERT_SCHEMA, "schema")
    expected = reconstruct()
    require(certificate["result"] == expected, "independent reconstruction")
    require(certificate["result_sha256"] == digest(expected), "result digest")
    require(expected["certified_DAG_nodes"] == ["D00", "D01", "D05", "D06", "D08"], "DAG advance")
    require(expected["first_exact_blocker"]["node_id"] == "D02", "first blocker")
    require(all(value is None for value in expected["identifier_ledger"].values()), "identifier nonpromotion")
    require(expected["gate5_global_ledger"]["global_maturity_after"] == "10/18", "Gate5")
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_imported_or_executed": False,
        "atomic_slot_count": 2,
        "certified_DAG_node_count": 5,
        "newly_certified_DAG_nodes": ["D05", "D06", "D08"],
        "first_exact_blocker": "D02",
        "all_versioned_identifiers_still_null": True,
        "global_gate5_maturity": "10/18",
        "global_complete_18_field_block_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(canonical({"status": "PASS", "output": str(args.output), "result_sha256": document["result_sha256"]}))


if __name__ == "__main__":
    main()
