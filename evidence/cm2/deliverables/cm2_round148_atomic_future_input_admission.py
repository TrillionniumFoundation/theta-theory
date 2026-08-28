#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round148-atomic-future-input-admission-2026-07-24.json"
SCHEMA = "cm2.round148.atomic-future-input-admission.v1"

R144 = HERE / "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
R147 = HERE / "cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json"
R145_SOURCE = HERE / "cm2_round145_finite_connected_leaf_corridor_atlas.py"
R145_CERT = HERE / "cm2-round145-finite-connected-leaf-corridor-atlas-2026-07-24.json"
R145_VERIFIER = HERE / "cm2_round145_finite_connected_leaf_corridor_atlas_verifier.py"
R145_VERIFICATION = HERE / "cm2-round145-finite-connected-leaf-corridor-atlas-verification-2026-07-24.json"
R146_SOURCE = HERE / "cm2_round146_physical_centered_jet_2d_frontier.py"
R146_CERT = HERE / "cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json"
R146_VERIFIER = HERE / "cm2_round146_physical_centered_jet_2d_frontier_verifier.py"
R146_VERIFICATION = HERE / "cm2-round146-physical-centered-jet-2d-frontier-verification-2026-07-24.json"

PINS = {
    R144.name: "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f",
    R147.name: "db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee",
    R145_SOURCE.name: "6deed0506b0105eee9ee9a89dd4c28ee9bed81aa4922586eb8b8005a433ba4c7",
    R145_CERT.name: "5edac93e1425c72992ab671f3b3f7db269d236819ea3ad689b612505426ccec6",
    R145_VERIFIER.name: "47f283b48bba7c28a94ca01fcaec0389728c1aebd90d31a1f8c36fca0ee4f255",
    R145_VERIFICATION.name: "6101a4bdd7e1bea160a6d1bf36f0b4be281d340f217eb87d38b47f9961fd24a8",
    R146_SOURCE.name: "db0241c9bae4937cd1a01f23b4951247fa69fd16d9b06a75d446e5336c9930c4",
    R146_CERT.name: "38ad7cdd5a2af7cda94792a31a8a83275022f943e8e6b9801ee4bece73b04eac",
    R146_VERIFIER.name: "d75af7cc251c212a11522a8884ad9afbb983197ba9e6e0d43598ffe06916ad44",
    R146_VERIFICATION.name: "c25646413467deb2c1c5ea68f92e97116546eb62333596afc61973430e002dd4",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load_pinned_json(path):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINS[path.name]:
        raise ValueError(f"pin mismatch: {path.name}")
    return json.loads(raw.decode("utf-8"))


def check_source_pin(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINS[path.name]:
        raise ValueError(f"source pin mismatch: {path.name}")


def bound_slot(name, source, certificate, verifier, verification, result_sha256, outcome):
    return {
        "slot": name,
        "status": "ATOMICALLY_BOUND_AND_VERIFIED",
        "source_sha256": PINS[source.name],
        "certificate_sha256": PINS[certificate.name],
        "verifier_sha256": PINS[verifier.name],
        "verification_sha256": PINS[verification.name],
        "verification_result_sha256": result_sha256,
        "acceptance_outcome": outcome,
    }


def build_result(r144, r145, r145v, r146, r146v, r147):
    for path in (R145_SOURCE, R145_VERIFIER, R146_SOURCE, R146_VERIFIER):
        check_source_pin(path)
    if r145v["result"]["status"] != "PASS" or r146v["result"]["status"] != "PASS":
        raise ValueError("future verification not PASS")
    if r145v["result"]["certificate_sha256"] != PINS[R145_CERT.name]:
        raise ValueError("Round145 certificate hash")
    if r145v["result"]["certificate_result_sha256"] != r145["result_sha256"]:
        raise ValueError("Round145 result hash")
    if r146v["result"]["pins"]["certificate_sha256"] != PINS[R146_CERT.name]:
        raise ValueError("Round146 certificate hash")
    if r146v["result"]["pins"]["certificate_result_sha256"] != r146["result_sha256"]:
        raise ValueError("Round146 result hash")
    old_slots = r147["result"]["Round144_atomic_migration_frontier"]["future_input_slots"]
    if [row["status"] for row in old_slots] != ["UNBOUND_NULL_FUTURE_INPUT"] * 2:
        raise ValueError("Round147 slot state")

    slots = [
        bound_slot(
            "Round145_leaf_corridor_atlas",
            R145_SOURCE,
            R145_CERT,
            R145_VERIFIER,
            R145_VERIFICATION,
            r145v["result_sha256"],
            "D05_D06_D08_CERTIFIED",
        ),
        bound_slot(
            "Round146_two_generator_outer_atlas",
            R146_SOURCE,
            R146_CERT,
            R146_VERIFIER,
            R146_VERIFICATION,
            r146v["result_sha256"],
            "LOCAL_2D_EVIDENCE_ACCEPTED__D02_REMAINS_BLOCKED",
        ),
    ]
    status_map = {
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
    dag_rows = []
    for old in r144["result"]["migration_DAG_rows"]:
        status, evidence = status_map[old["node_id"]]
        dag_rows.append({
            "node_id": old["node_id"],
            "operation": old["operation"],
            "depends_on": old["depends_on"],
            "round148_status": status,
            "evidence_or_blocker": evidence,
        })
    r145_branch = r145["result"]["boundary_and_physical_branch_proof"]
    r145_leaf = r145["result"]["promoted_Round137_v1_leaf_rank"]
    r145_short = r145["result"]["promoted_v1_source_short_cell"]
    r145_image = r145["result"]["promoted_v1_image_recut"]
    r146_d02 = r146["result"]["Round144_D02_status"]
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
            "maximal_component_outer_atlas_complete": r146_d02["maximal_component_outer_atlas_complete"],
            "all_event_frontiers_exhausted": r146_d02["all_event_frontiers_exhausted"],
            "D03_least_rank_negative_oracle_authorized": r146_d02["D03_least_rank_negative_oracle_authorized"],
            "next_required_object": "finite connected maximal 2D leaf-corridor atlas with every exit and physical event frontier exhausted",
        },
        "Round145_promotions": {
            "connected_physical_open_branch_certified": r145_branch["connected_physical_open_branch_certified"],
            "global_two_dimensional_component_maximality_certified": r145_branch["global_two_dimensional_component_maximality_certified"],
            "canonical_H1_x_level": r145_leaf["canonical_H1_x_level"],
            "canonical_H1_x_rank_sha256": r145_leaf["canonical_H1_x_least_rank"]["contained_primitive_basis_rank"]["sha256_of_decimal"],
            "corrected_left_anchored_natural_short_cell_k": r145_short["corrected_left_anchored_natural_short_cell_k"],
            "corrected_v1_source_cell_id": r145_short["corrected_v1_source_cell_id"],
            "corrected_v1_image_recut_registry_id": r145_image["corrected_v1_image_recut_registry_id"],
            "endpoint_difference_is_complete_image_span": r145_image["endpoint_difference_is_complete_image_span"],
        },
        "identifier_ledger": {
            "component_v1_id": None,
            "parent_W_v1_id": None,
            "restriction_v1_id": None,
            "owner_v1_id": None,
            "t54_v1_token": None,
            "Omega_j_v1_record": None,
            "q_j_v1_output": None,
        },
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
        "upstream_sha256": PINS,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result(
        load_pinned_json(R144),
        load_pinned_json(R145_CERT),
        load_pinned_json(R145_VERIFICATION),
        load_pinned_json(R146_CERT),
        load_pinned_json(R146_VERIFICATION),
        load_pinned_json(R147),
    )
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(canonical({
        "status": result["status"],
        "certified_DAG_nodes": result["certified_DAG_nodes"],
        "first_exact_blocker": "D02",
        "result_sha256": document["result_sha256"],
    }))


if __name__ == "__main__":
    main()
