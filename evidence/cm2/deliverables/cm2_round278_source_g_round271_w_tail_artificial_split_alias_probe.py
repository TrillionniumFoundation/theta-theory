#!/usr/bin/env python3
"""Zero-credit proof probe for the four Round271 W-tail t-split aliases.

Round271 bisected four OUTGOING-W Round182 leaves once in ``t``.  On each
parent, one strict-negative physical region was consequently named twice.
This probe reconstructs those four pairs from the frozen rows and proves that
the duplicate names join through the complete artificial middle face.

No occurrence or component credit is issued here.  A later pinned
producer/independent-verifier pair may consume the witness rows.
"""
from __future__ import annotations

import collections
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round179_source_g_residual_tube_arrangement_verifier as r179


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round278.source-g-round271-w-tail-artificial-split-alias-probe.v1"
PRECISION_BITS = 256
CORRIDOR_RELATIVE_DENOMINATOR = 8

R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R271 = (
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_"
    "materialization_certificate.json"
)
INPUT_PINS = {
    R182: (
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
        "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269",
    ),
    R271: (
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
        "30f509eb10b1a25c5195e672e980d7e4e651dadc3defd5e150245c6798060506",
    ),
}
EVALUATOR_PIN = (
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py",
    "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qtext(value: Q) -> str:
    return str(value)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def load_pinned(name: str) -> dict[str, Any]:
    raw = (HERE / name).read_bytes()
    file_pin, result_pin = INPUT_PINS[name]
    require(hashlib.sha256(raw).hexdigest() == file_pin, f"file pin:{name}")
    document = json.loads(raw)
    require(document["result_sha256"] == result_pin, f"result pin:{name}")
    return document["result"]


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    entry = result["table_census_and_sha256"][table]
    raw_rows = result[table]
    require(len(raw_rows) == entry["row_count"], f"row count:{table}")
    require(digest(raw_rows) == entry["rows_sha256"], f"row digest:{table}")
    return [dict(zip(columns, row, strict=True)) for row in raw_rows]


def box(values: list[str] | tuple[str, ...], path: str) -> Any:
    coordinates = tuple(Q(value) for value in values)
    return r179.r174.atlas.AtlasBox(*coordinates, 0, path)


def box_payload(values: tuple[Q, ...]) -> list[str]:
    return [qtext(value) for value in values]


def volume(values: tuple[Q, ...]) -> Q:
    return (
        (values[1] - values[0])
        * (values[3] - values[2])
        * (values[5] - values[4])
    )


def outgoing_equality_witness(
    chart: str,
    owner_target: str,
    values: tuple[Q, ...],
    path: str,
) -> dict[str, Any]:
    equality = r179.independent_geometry(
        chart,
        owner_target,
        box(box_payload(values), path),
    )["outgoing_equality"][0]
    sign = r179.arb_sign(equality)
    lower = equality.lower()
    upper = equality.upper()
    require(sign == "STRICT_NEGATIVE", f"strict-negative equality:{path}")
    require(bool(upper < 0), f"strict-negative upper endpoint:{path}")
    return {
        "precision_bits": ctx.prec,
        "equation": "target_normal_x^2-target_normal_y^2",
        "sign": sign,
        "arb_repr": repr(equality),
        "lower_endpoint_arb_repr": repr(lower),
        "upper_endpoint_arb_repr": repr(upper),
        "strict_upper_endpoint_negative": True,
    }


def close(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "unclosed row")
    row["row_sha256"] = digest(row)
    return row


def build() -> dict[str, Any]:
    evaluator_name, evaluator_sha256 = EVALUATOR_PIN
    require(
        hashlib.sha256((HERE / evaluator_name).read_bytes()).hexdigest()
        == evaluator_sha256,
        "Round179 evaluator pin",
    )
    ctx.prec = PRECISION_BITS
    require(ctx.prec == PRECISION_BITS, "fixed FLINT precision")

    round271 = load_pinned(R271)
    source_rows = round271["formal_side_signature_ledger"]["rows"]
    require(len(source_rows) == 70_420, "Round271 signed-row census")
    groups: dict[tuple[str, str], list[dict[str, Any]]] = (
        collections.defaultdict(list)
    )
    for row in source_rows:
        if (
            row["signed_region_row_id"].startswith("round271-W-tail-side:")
            and row["collar_kind"] == "OUTGOING"
            and row["region_product_sign"] == "STRICT_NEGATIVE"
        ):
            signature = row["local_return_signature"]
            signature_sha256 = row[
                "complete_10_field_return_signature_sha256"
            ]
            require(signature_sha256 == digest(signature), "signature digest")
            groups[(row["Round182_leaf_row_id"], signature_sha256)].append(row)
    aliases = {
        key: sorted(rows, key=lambda row: row["t_child"])
        for key, rows in groups.items()
        if len(rows) == 2
    }
    require(len(groups) == 4, "four strict-negative W-tail groups")
    require(
        sum(len(rows) for rows in groups.values()) == 8,
        "eight strict-negative W-tail source rows",
    )
    require(len(aliases) == 4, "four artificial aliases")
    alias_leaf_ids = {leaf_id for leaf_id, _signature in aliases}
    del round271

    round182 = load_pinned(R182)
    leaves = {
        row["row_id"]: row
        for row in unpack(round182, "collar_leaf_rows")
        if row["row_id"] in alias_leaf_ids
    }
    require(set(leaves) == alias_leaf_ids, "all alias parent leaves")
    occurrence_ids = {row["occurrence_row_id"] for row in leaves.values()}
    occurrences = {
        row["Round179_occurrence_row_id"]: row
        for row in unpack(round182, "collar_occurrence_rows")
        if row["Round179_occurrence_row_id"] in occurrence_ids
    }
    require(set(occurrences) == occurrence_ids, "all alias collars")
    del round182

    witness_rows: list[dict[str, Any]] = []
    total_face_area = Q(0)
    total_corridor_volume = Q(0)
    for (leaf_id, signature_sha256), rows in sorted(aliases.items()):
        require(
            [row["t_child"] for row in rows] == [0, 1],
            f"child labels:{leaf_id}",
        )
        left_row, right_row = rows
        parent = leaves[leaf_id]
        collar = occurrences[parent["occurrence_row_id"]]
        parent_box = tuple(Q(value) for value in parent["box"])
        left_box = tuple(Q(value) for value in left_row["t_child_box"])
        right_box = tuple(Q(value) for value in right_row["t_child_box"])

        split = left_box[1]
        require(left_box[0] == parent_box[0], f"left endpoint:{leaf_id}")
        require(right_box[1] == parent_box[1], f"right endpoint:{leaf_id}")
        require(split == right_box[0], f"common t face:{leaf_id}")
        require(
            left_box[2:] == right_box[2:] == parent_box[2:],
            f"complete common p-s base:{leaf_id}",
        )
        require(
            volume(left_box) + volume(right_box) == volume(parent_box),
            f"child volume partition:{leaf_id}",
        )
        require(
            left_box[1] - left_box[0]
            == right_box[1] - right_box[0]
            > 0,
            f"positive equal child widths:{leaf_id}",
        )
        common_face_area = (
            (parent_box[3] - parent_box[2])
            * (parent_box[5] - parent_box[4])
        )
        require(common_face_area > 0, f"positive common face:{leaf_id}")

        signature = left_row["local_return_signature"]
        require(
            signature == right_row["local_return_signature"],
            f"complete signature equality:{leaf_id}",
        )
        require(digest(signature) == signature_sha256, "signature identity")
        require(
            left_row["owner_target"]
            == right_row["owner_target"]
            == collar["owner_target"]
            == signature["target_lift"],
            f"owner identity:{leaf_id}",
        )
        require(
            left_row["region_product_sign"]
            == right_row["region_product_sign"]
            == "STRICT_NEGATIVE",
            f"F sign identity:{leaf_id}",
        )
        require(
            signature["source_chart"] == collar["chart"],
            f"source chart identity:{leaf_id}",
        )

        face_values = (
            split,
            split,
            parent_box[2],
            parent_box[3],
            parent_box[4],
            parent_box[5],
        )
        face_witness = outgoing_equality_witness(
            collar["chart"],
            collar["owner_target"],
            face_values,
            f"round278:{leaf_id}:face",
        )

        child_width = left_box[1] - left_box[0]
        corridor_width = child_width / CORRIDOR_RELATIVE_DENOMINATOR
        left_corridor = (
            split - corridor_width,
            split,
            *parent_box[2:],
        )
        right_corridor = (
            split,
            split + corridor_width,
            *parent_box[2:],
        )
        require(
            left_box[0] <= left_corridor[0] < left_corridor[1] == split,
            f"left inward corridor:{leaf_id}",
        )
        require(
            split == right_corridor[0] < right_corridor[1] <= right_box[1],
            f"right inward corridor:{leaf_id}",
        )
        corridor_rows = []
        for side, values, source_row in (
            ("LEFT_CHILD_INWARD", left_corridor, left_row),
            ("RIGHT_CHILD_INWARD", right_corridor, right_row),
        ):
            corridor_volume = volume(values)
            require(corridor_volume > 0, f"positive corridor:{leaf_id}:{side}")
            total_corridor_volume += corridor_volume
            corridor_rows.append({
                "side": side,
                "source_signed_region_row_id":
                    source_row["signed_region_row_id"],
                "box": box_payload(values),
                "exact_coordinate_volume": qtext(corridor_volume),
                "outgoing_equality_256_bit": outgoing_equality_witness(
                    collar["chart"],
                    collar["owner_target"],
                    values,
                    f"round278:{leaf_id}:{side}",
                ),
            })

        total_face_area += common_face_area
        witness_rows.append(close({
            "alias_witness_row_id": (
                "round278-W-tail-artificial-split-alias:"
                + digest([leaf_id, signature_sha256])
            ),
            "Round182_parent_leaf_row_id": leaf_id,
            "Round182_occurrence_row_id": parent["occurrence_row_id"],
            "chart": collar["chart"],
            "owner_target": collar["owner_target"],
            "source_signed_region_row_ids": [
                left_row["signed_region_row_id"],
                right_row["signed_region_row_id"],
            ],
            "child_boxes": [box_payload(left_box), box_payload(right_box)],
            "children_exactly_partition_parent_box": True,
            "parent_box": box_payload(parent_box),
            "artificial_split_t": qtext(split),
            "complete_common_p_s_face_box": box_payload(face_values),
            "complete_common_p_s_face_exact_area": qtext(common_face_area),
            "common_face_outgoing_equality_256_bit": face_witness,
            "inward_corridor_relative_width": (
                f"1/{CORRIDOR_RELATIVE_DENOMINATOR}"
                "_OF_EACH_CHILD_T_WIDTH"
            ),
            "strict_negative_inward_corridors": corridor_rows,
            "complete_10_field_return_signature":
                signature,
            "complete_10_field_return_signature_sha256": signature_sha256,
            "official_key_id": signature["official_key_id"],
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_row": signature["official_key_row"],
            "region_product_F_sign": "STRICT_NEGATIVE",
            "signature_key_owner_F_sign_all_identical": True,
            "graph_classification_difference_is_not_a_physical_separator": [
                left_row["graph_classification"],
                right_row["graph_classification"],
            ],
            "physical_interpretation": (
                "ONE_STRICT_NEGATIVE_OPEN_3D_REGION_NAMED_TWICE_BY_AN_"
                "ARTIFICIAL_ROUND271_T_SPLIT"
            ),
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
        }))

    witness_rows.sort(key=lambda row: row["alias_witness_row_id"])
    require(len(witness_rows) == 4, "witness row census")
    require(total_face_area == Q(1, 51_200), "face-area census")
    require(
        total_corridor_volume == Q(177, 26_214_400_000),
        "corridor-volume census",
    )

    rows_sha256 = digest(witness_rows)
    row_hashes_sha256 = digest(
        [row["row_sha256"] for row in witness_rows]
    )
    result = {
        "status": (
            "ROUND278_ROUND271_W_TAIL_ARTIFICIAL_SPLIT_ALIAS_PROBE__"
            "FOUR_OF_FOUR_CERTIFIED__ZERO_CREDIT"
        ),
        "census": {
            "Round271_W_tail_artificial_t_split_alias_pair_count": 4,
            "source_signed_region_row_count": 8,
            "canonical_physical_region_count": 4,
            "artificial_alias_reduction_count": 4,
            "same_parent_leaf_pair_count": 4,
            "exact_child_partition_count": 4,
            "complete_positive_p_s_common_face_count": 4,
            "strict_negative_common_face_outgoing_equality_count": 4,
            "strict_negative_inward_corridor_count": 8,
            "complete_signature_key_owner_F_sign_identity_count": 4,
            "remaining_alias_pair_failclosed_count": 0,
        },
        "precision_bits": PRECISION_BITS,
        "corridor_relative_denominator": CORRIDOR_RELATIVE_DENOMINATOR,
        "exact_common_face_area_sum": qtext(total_face_area),
        "exact_inward_corridor_volume_sum": qtext(total_corridor_volume),
        "formal_zero_credit_alias_witness_ledger": {
            "row_count": len(witness_rows),
            "rows_sha256": rows_sha256,
            "row_hashes_sha256": row_hashes_sha256,
            "rows": witness_rows,
        },
        "scope_contract": {
            "alias_is_by_same_Round182_parent_and_same_complete_signature":
                True,
            "artificial_children_exactly_partition_the_parent": True,
            "middle_face_is_the_complete_positive_area_p_s_rectangle": True,
            "fixed_256_bit_outgoing_equality_is_strict_negative_on_face":
                True,
            "fixed_256_bit_outgoing_equality_is_strict_negative_in_both_"
            "inward_corridors": True,
            "official_key_owner_and_F_sign_are_identical": True,
            "graph_classification_labels_do_not_separate_the_strict_negative_"
            "physical_region": True,
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "consume these four alias reductions only inside a pinned "
            "collar-region producer and independent verifier before any "
            "expanded-occurrence or DSU credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "input_file_sha256": {
                name: pins[0] for name, pins in sorted(INPUT_PINS.items())
            },
            "input_result_sha256": {
                name: pins[1] for name, pins in sorted(INPUT_PINS.items())
            },
            "evaluator_file": evaluator_name,
            "evaluator_sha256": evaluator_sha256,
        },
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    print(json.dumps(build(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
