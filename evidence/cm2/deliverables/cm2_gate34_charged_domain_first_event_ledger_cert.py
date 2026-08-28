#!/usr/bin/env python3
"""Domain-specific Borel first-event ledgers for 128 charged cylinders.

The earlier selected-germ ledgers cannot receive 124 of the new charged
cylinders because their source domains differ.  This certificate does not
reuse those ledgers.  It registers each exact charged ``(z,h)`` cylinder as
its own canonical Borel domain and binds the source-relative first-core
replay to one domain-equal nonempty first-event slot.

Only the certified finite word is materialized.  All core slots before the
stop, all singular slots through the stop, and the 23 wrong destination slots
at the stop are empty.  No post-stop slot or nonreturning-cemetery slot is
created, and no full-germ, collision-SRB-mass, or post-core return statement
is inferred.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate34_source_relative_first_core_stopping_cert as source_first


Q = Fraction
HERE = Path(__file__).resolve().parent
PRECISION_BITS = 2048

DEPENDENCIES = {
    "cm2-gate34-source-relative-first-core-stopping-manifest-2026-07-18.json": (
        "c08d7dbee41b45c11845c3e905cc9aaacc8d6e1a37bb4fb221c9632bc0e0df8e"
    ),
    "cm2_gate34_source_relative_first_core_stopping_cert.py": (
        "0e4aaf50f2221d81a78706da3f8c6a85ccbf678db622df62c275c00fa3b991a6"
    ),
    "cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.json": (
        "711ce6d5af1a28d26c596cde9df3c7f0de4a20f7821d5a11adba69d10270e07b"
    ),
    "cm2_gate34_physical_first_return_partition_interface_cert.py": (
        "686296673afaa549d2e6d5ef7b01a50b1a20c5e3458e53cde80b386f2ba3be95"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            loaded[name] = load_json(name)

    source_manifest = loaded[
        "cm2-gate34-source-relative-first-core-stopping-manifest-2026-07-18.json"
    ]
    require(
        source_manifest["verdict"][
            "source_relative_first_core_stopping_cylinders_128"
        ]
        == "CERTIFIED",
        "source-relative verdict",
    )
    interface = loaded[
        "cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.json"
    ]
    require(
        interface["verdict"]["occurrence_only_ledger_domain_mismatches_124"]
        == "CERTIFIED_REJECTED",
        "prior domain mismatch verdict",
    )
    cores = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]["physical_return_core_registry"]
    require(cores["physical_compact_homogeneous_core_count"] == 24, "core count")

    source_first.load_dependencies()
    source_first.parent.load_dependencies()
    return loaded


def source_relative_raw_rows(
    source_manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Recreate the exact raw rows hidden behind the upstream row digests."""
    ctx.prec = PRECISION_BITS
    source_first.parent.all_charge.refresh_arb_constants()
    require(ctx.prec == PRECISION_BITS, "precision")
    maximal_rows, _registry = source_first.current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    specifications = source_first.parent.occurrence_specifications(maximal_rows)
    require(len(by_id) == len(specifications) == 64, "occurrence count")

    source_rows: list[dict[str, Any]] = []
    hit_rows: list[dict[str, Any]] = []
    branch_rows: list[dict[str, Any]] = []
    for occurrence_id, specification in sorted(specifications.items()):
        row = dict(by_id[occurrence_id])
        row["witness"] = dict(row["witness"])
        row["witness"]["chart_id"] = specification["source_chart"]
        row["witness"]["z"] = specification["z"]
        owner = source_first.parent.physical_row_and_owner_audit(row, specification)
        source_row = source_first.source_state_row(row, specification)
        hit_row = source_first.hit_intermediate_state_row(
            row, specification, owner["source_owner_audit_id"]
        )
        source_rows.append(source_row)
        hit_rows.append(hit_row)
        for side in ("hit", "miss"):
            suffix = source_first.parent.replay_first_stopping_branch(
                row, specification, side, owner["source_owner_audit_id"]
            )
            offset = suffix["source_collision_count_to_regular_suffix"]
            source_time = (
                suffix["first_core_stopping_time_from_regular_suffix"] + offset
            )
            preterminal = (
                suffix["strict_outside_core_state_count_before_stop"] + offset
            )
            payload = {
                "parent_first_stopping_branch_id": suffix[
                    "first_stopping_branch_id"
                ],
                "source_state_classification_id": source_row[
                    "source_state_classification_id"
                ],
                "hit_intermediate_classification_id": (
                    hit_row["hit_intermediate_classification_id"]
                    if side == "hit" else None
                ),
                "source_relative_first_core_time": source_time,
                "destination_core_id": suffix["destination_core_id"],
            }
            branch_rows.append({
                "source_relative_first_stopping_branch_id": (
                    "source-first-core:" + canonical_digest(payload)
                ),
                "occurrence_id": occurrence_id,
                "side": side,
                "parent_first_stopping_branch_id": suffix[
                    "first_stopping_branch_id"
                ],
                "source_owner_audit_id": owner["source_owner_audit_id"],
                "source_state_classification_id": source_row[
                    "source_state_classification_id"
                ],
                "hit_intermediate_classification_id": (
                    hit_row["hit_intermediate_classification_id"]
                    if side == "hit" else None
                ),
                "source_to_regular_suffix_collision_offset": offset,
                "suffix_relative_first_core_time": suffix[
                    "first_core_stopping_time_from_regular_suffix"
                ],
                "source_relative_first_core_time": source_time,
                "strict_preterminal_outside_all_24_core_state_count": preterminal,
                "destination_core_id": suffix["destination_core_id"],
                "destination_chart": suffix["destination_chart"],
                "every_state_before_source_relative_stop_is_strictly_outside": True,
                "terminal_state_is_strictly_inside_unique_destination_core": True,
                "all_suffix_word_collisions_unique_and_regular": suffix[
                    "all_listed_first_collision_decisions_unique_and_regular"
                ],
            })

    source_rows.sort(key=canonical_json)
    hit_rows.sort(key=canonical_json)
    branch_rows.sort(key=canonical_json)
    registry = source_manifest["result"][
        "source_relative_first_core_stopping_registry"
    ]
    require(
        canonical_digest(source_rows) == registry["source_state_rows_sha256"],
        "source rows digest",
    )
    require(
        canonical_digest(hit_rows)
        == registry["hit_intermediate_state_rows_sha256"],
        "hit rows digest",
    )
    upstream_branch_projection = [
        {key: value for key, value in row.items() if key != "all_suffix_word_collisions_unique_and_regular"}
        for row in branch_rows
    ]
    require(
        canonical_digest(upstream_branch_projection)
        == registry["source_relative_branch_rows_sha256"],
        "source-relative branch rows digest",
    )
    return source_rows, hit_rows, branch_rows


def core_ids() -> list[str]:
    identifiers = sorted(
        source_first.parent.core_id(core)
        for core in source_first.parent.core_cert.physical_cores()
    )
    require(len(identifiers) == len(set(identifiers)) == 24, "core identifiers")
    return identifiers


def slot_id(
    ledger_id: str, time: int, kind: str, destination_core_id: str | None,
) -> str:
    payload = {
        "charged_domain_ledger_id": ledger_id,
        "time_from_source": time,
        "event_kind": kind,
        "destination_core_id": destination_core_id,
    }
    return "charged-first-event-slot:" + canonical_digest(payload)


def charged_domain_ledgers(
    loaded: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_manifest = loaded[
        "cm2-gate34-source-relative-first-core-stopping-manifest-2026-07-18.json"
    ]
    source_rows, hit_rows, branches = source_relative_raw_rows(source_manifest)
    source_by_occurrence = {row["occurrence_id"]: row for row in source_rows}
    hit_by_occurrence = {row["occurrence_id"]: row for row in hit_rows}
    branch_by_key = {
        (row["occurrence_id"], row["side"]): row for row in branches
    }
    interface = loaded[
        "cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.json"
    ]
    entrance_atoms = interface["result"]["charged_entrance_atom_rows"]
    require(len(entrance_atoms) == 128, "entrance atom count")
    entrance_by_key = {
        (row["occurrence_id"], row["parameter_side"]): row
        for row in entrance_atoms
    }
    require(set(entrance_by_key) == set(branch_by_key), "branch-domain key equality")
    all_core_ids = core_ids()
    all_finite_slot_ids: list[str] = []
    all_empty_slot_ids: list[str] = []
    rows: list[dict[str, Any]] = []

    for key in sorted(branch_by_key):
        occurrence_id, side = key
        branch = branch_by_key[key]
        entrance = entrance_by_key[key]
        source_row = source_by_occurrence[occurrence_id]
        hit_row = hit_by_occurrence[occurrence_id]
        require(
            entrance["source_owner_audit_id"] == branch["source_owner_audit_id"],
            "source owner binding",
        )
        require(
            entrance["upstream_first_stopping_branch_id"]
            == branch["parent_first_stopping_branch_id"],
            "suffix branch binding",
        )
        require(
            entrance["suffix_relative_first_core_time"]
            == branch["suffix_relative_first_core_time"],
            "suffix time binding",
        )
        require(
            entrance["destination_core_id"] == branch["destination_core_id"],
            "destination binding",
        )
        coordinates = entrance["source_coordinates"]
        radius_power = coordinates["z_half_width"]["denominator_power_of_two"]
        radius = Q(1, 2**radius_power)
        z_center = Q(coordinates["z_center"])
        parameter_sign = int(entrance["parameter_sign"])
        signed_h_interval = (
            ["0_open", str(radius)]
            if parameter_sign == 1
            else [str(-radius), "0_open"]
        )
        domain_payload = {
            "occurrence_id": occurrence_id,
            "parameter_side": side,
            "source_chart": entrance["source_chart"],
            "z_interval_closed": [str(z_center - radius), str(z_center + radius)],
            "fixed_phase_coordinate": "s=0",
            "signed_h_interval": signed_h_interval,
        }
        domain_id = "charged-borel-domain:" + canonical_digest(domain_payload)
        ledger_payload = {
            "charged_borel_domain_id": domain_id,
            "frozen_core_ids_sha256": canonical_digest(all_core_ids),
            "clock_origin": "source_collision_state_at_time_0",
        }
        ledger_id = "charged-first-event-ledger:" + canonical_digest(ledger_payload)
        stop_time = int(branch["source_relative_first_core_time"])
        destination = branch["destination_core_id"]
        nonempty_id = slot_id(ledger_id, stop_time, "core", destination)
        empty_ids: list[str] = []
        for time in range(stop_time):
            for core_identifier in all_core_ids:
                empty_ids.append(slot_id(ledger_id, time, "core", core_identifier))
            empty_ids.append(slot_id(ledger_id, time, "singular", None))
        for core_identifier in all_core_ids:
            if core_identifier != destination:
                empty_ids.append(slot_id(ledger_id, stop_time, "core", core_identifier))
        empty_ids.append(slot_id(ledger_id, stop_time, "singular", None))
        finite_ids = empty_ids + [nonempty_id]
        require(len(finite_ids) == (stop_time + 1) * 25, "finite slot count")
        require(len(set(finite_ids)) == len(finite_ids), "finite slot identity")
        all_finite_slot_ids.extend(finite_ids)
        all_empty_slot_ids.extend(empty_ids)
        rows.append({
            "charged_domain_ledger_id": ledger_id,
            "charged_borel_domain_id": domain_id,
            "occurrence_id": occurrence_id,
            "parameter_side": side,
            "canonical_domain": {
                **domain_payload,
                "parameter_magnitude_interval": ["0_open", str(radius)],
                "parameter_sign": parameter_sign,
                "coordinates": ["z", "h"],
                "parameterized_dimension": 2,
                "fixed_parameter_collision_source_dimension": 1,
                "is_Borel": True,
                "open_side_source_map_is_Borel": True,
            },
            "domain_equals_upstream_certified_charged_cylinder": True,
            "upstream_entrance_atom_id": entrance["entrance_atom_id"],
            "upstream_source_relative_branch_id": branch[
                "source_relative_first_stopping_branch_id"
            ],
            "source_owner_audit_id": branch["source_owner_audit_id"],
            "source_state_classification_id": source_row[
                "source_state_classification_id"
            ],
            "hit_intermediate_classification_id": (
                hit_row["hit_intermediate_classification_id"]
                if side == "hit" else None
            ),
            "clock_origin": "source_collision_state_at_time_0",
            "source_relative_first_core_time": stop_time,
            "destination_core_id": destination,
            "unique_nonempty_first_event_slot_id": nonempty_id,
            "unique_nonempty_slot_equals_whole_charged_domain": True,
            "strict_preterminal_outside_regular_state_count": stop_time,
            "all_preterminal_states_strictly_outside_C24": branch[
                "every_state_before_source_relative_stop_is_strictly_outside"
            ],
            "all_collisions_in_certified_finite_word_unique_and_regular": branch[
                "all_suffix_word_collisions_unique_and_regular"
            ],
            "hit_open_side_intermediate_regular_guard": (
                hit_row["regularity_claim_is_only_for_open_positive_side"]
                if side == "hit" else None
            ),
            "terminal_strictly_inside_unique_destination_core": branch[
                "terminal_state_is_strictly_inside_unique_destination_core"
            ],
            "finite_prefix_core_empty_slot_count": stop_time * 24 + 23,
            "finite_prefix_singular_empty_slot_count": stop_time + 1,
            "finite_prefix_empty_slot_count": len(empty_ids),
            "finite_prefix_total_slot_count": len(finite_ids),
            "finite_prefix_empty_slot_ids_sha256": canonical_digest(sorted(empty_ids)),
            "old_selected_germ_ledger_reused": False,
            "occurrence_id_only_domain_join_used": False,
            "post_stop_slots_materialized": 0,
            "nonreturning_cemetery_slot_materialized": False,
        })

    rows.sort(key=lambda row: (row["occurrence_id"], row["parameter_side"]))
    require(len(rows) == 128, "ledger count")
    require(len({row["charged_borel_domain_id"] for row in rows}) == 128, "domain identity")
    require(len({row["charged_domain_ledger_id"] for row in rows}) == 128, "ledger identity")
    require(len({row["unique_nonempty_first_event_slot_id"] for row in rows}) == 128, "nonempty slot identity")
    require(len(all_finite_slot_ids) == len(set(all_finite_slot_ids)), "global slot identity")
    require(len(all_finite_slot_ids) == 26900, "global finite slot count")
    require(len(all_empty_slot_ids) == 26772, "global empty slot count")
    time_histogram = Counter(row["source_relative_first_core_time"] for row in rows)
    require(sum(key * value for key, value in time_histogram.items()) == 948, "preterminal count")
    summary = {
        "exact_charged_borel_domain_count": 128,
        "domain_specific_first_event_ledger_count": 128,
        "domain_equal_unique_nonempty_first_event_slot_count": 128,
        "old_selected_germ_ledger_reuse_count": 0,
        "prior_occurrence_only_domain_mismatch_count": 124,
        "domain_specific_registration_resolves_prior_mismatch_count": 124,
        "source_relative_first_core_time_histogram": {
            str(key): value for key, value in sorted(time_histogram.items())
        },
        "maximum_source_relative_first_core_time": max(time_histogram),
        "strict_preterminal_outside_regular_state_count": 948,
        "finite_prefix_total_first_event_slot_count": len(all_finite_slot_ids),
        "finite_prefix_unique_nonempty_core_slot_count": 128,
        "finite_prefix_empty_core_slot_count": sum(
            row["finite_prefix_core_empty_slot_count"] for row in rows
        ),
        "finite_prefix_empty_singular_slot_count": sum(
            row["finite_prefix_singular_empty_slot_count"] for row in rows
        ),
        "finite_prefix_total_empty_slot_count": len(all_empty_slot_ids),
        "post_stop_slot_count": 0,
        "nonreturning_cemetery_slot_count": 0,
        "all_domains_equal_their_certified_charged_cylinders": True,
        "all_128_first_event_slots_equal_their_whole_domains": True,
        "all_preterminal_core_and_singular_slots_empty": True,
        "all_terminal_wrong_core_and_singular_slots_empty": True,
        "charged_domain_ledger_rows_sha256": canonical_digest(rows),
        "all_finite_prefix_slot_ids_sha256": canonical_digest(
            sorted(all_finite_slot_ids)
        ),
        "all_finite_prefix_empty_slot_ids_sha256": canonical_digest(
            sorted(all_empty_slot_ids)
        ),
    }
    require(summary["finite_prefix_empty_core_slot_count"] == 25696, "empty core slots")
    require(summary["finite_prefix_empty_singular_slot_count"] == 1076, "empty singular slots")
    return rows, summary


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    rows, summary = charged_domain_ledgers(loaded)
    result: dict[str, Any] = {
        "schema": "cm2.gate34.charged-domain-first-event-ledger.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "domain_policy": "exact_charged_cylinder_not_occurrence_matched_old_germ",
            "first_event_clock": "source_collision_state_at_time_0",
            "admission_engine": "python-flint Arb plus canonical Borel IDs",
            "precision_bits": PRECISION_BITS,
        },
        "charged_domain_first_event_ledger_registry": summary,
        "charged_domain_first_event_ledger_rows": rows,
        "finite_prefix_scope": {
            "materialized_times_per_ledger": "0_through_source_relative_first_core_time",
            "preterminal_core_slots": "EMPTY_BY_STRICT_OUTSIDE_C24",
            "finite_word_singular_slots": "EMPTY_BY_UNIQUE_REGULAR_COLLISION_REPLAY",
            "terminal_destination_slot": "WHOLE_EXACT_CHARGED_DOMAIN",
            "terminal_other_23_core_slots": "EMPTY_BY_UNIQUE_CORE_INTERIOR",
            "post_stop_slots": "NOT_MATERIALIZED",
            "nonreturning_cemetery_slot": "NOT_MATERIALIZED",
        },
        "strict_nonpromotion": {
            "domain_specific_ledgers_are_old_selected_germ_ledgers": False,
            "charged_domains_cover_whole_all_scale_germs": False,
            "charged_domains_have_positive_fixed_parameter_collision_SRB_mass": False,
            "finite_prefix_singular_emptiness_is_global_cemetery_tail": False,
            "nonreturning_cemetery_is_materialized": False,
            "post_core_first_return_partition": "NOT_CERTIFIED",
            "collision_SRB_mass_or_normalized_hit_fraction": "NOT_CERTIFIED",
            "quantitative_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_core_return_operator": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("EXACT_CHARGED_BOREL_DOMAINS_128: CERTIFIED")
    print("DOMAIN_SPECIFIC_FIRST_EVENT_LEDGERS_128: CERTIFIED")
    print("DOMAIN_EQUAL_UNIQUE_NONEMPTY_SOURCE_FIRST_CORE_SLOTS_128: CERTIFIED")
    print("PRIOR_OCCURRENCE_ONLY_MISMATCHES_RESOLVED_BY_NEW_DOMAIN_REGISTRATION_124: CERTIFIED")
    print("FINITE_PREFIX_EMPTY_CORE_SLOTS_25696: CERTIFIED")
    print("FINITE_PREFIX_EMPTY_SINGULAR_SLOTS_1076: CERTIFIED")
    print("NONRETURNING_CEMETERY_SLOT: NOT_MATERIALIZED")
    print("COLLISION_SRB_MASS: NOT_CERTIFIED")
    print("POST_CORE_RETURN_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
