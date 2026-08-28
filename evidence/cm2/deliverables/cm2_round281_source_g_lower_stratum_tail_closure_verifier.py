#!/usr/bin/env python3
"""Independent verifier for the Round281 lower-stratum tail closure.

The producer is pinned as inert bytes and is never imported.  This verifier
reconstructs all t=0 owner/shadow/absence partitions from frozen Round174/179
geometry, and rechecks all fully-replaced two-child covers and strict signs.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "cm2_round281_source_g_lower_stratum_tail_closure.py"
LEDGER = HERE / "cm2_round281_source_g_lower_stratum_tail_closure_ledger.json.gz"
RESULT = HERE / "cm2_round281_source_g_lower_stratum_tail_closure_result.json"
OUTPUT = HERE / "cm2_round281_source_g_lower_stratum_tail_closure_verification.json"
SCHEMA = "cm2.round281.source-g-lower-stratum-tail-closure.verification.v1"
PINS = {
    PRODUCER.name: "c49b3ab561251eba9c4af2fb5058f164cc7afe664bf46b4a6fb0250a73293d5b",
    LEDGER.name: "ffa333f040551d583c6afd34a1b466fbc67fe0628683782d80f905329b800fc7",
    RESULT.name: "84ea62964c4199bdec66f7a82cfdee964b8b2b610f9c8c1c6298cc6fbaf1942c",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round280_source_g_lower_stratum_physical_disposition_probe_ledger.json.gz":
        "0f939334f9ca65c535be7123b8f9370b0833f84743b6a094c92ffcc1087dec1b",
}

OWNER = "CERTIFIED_PHYSICAL_SUPPORT_EXISTS__POSITIVE_T_HALF_OPEN_OWNER"
SHADOW = "CERTIFIED_PHYSICAL_SUPPORT_EXISTS__NEGATIVE_T_SHADOW_TO_POSITIVE_OWNER"
PARTITIONED = "CERTIFIED_PARTITIONED__NEGATIVE_T_SHADOW_AND_ABSENCE"
ABSENT = "CERTIFIED_SUPPORT_ABSENT__NEGATIVE_T_SHADOW_WITH_NO_ADMISSIBLE_POSITIVE_OWNER"
REPLACED = "CERTIFIED_SUPPORT_ABSENT__FULLY_REPLACED_RESOLVED_CHILD_COVER"
ZERO_FIELDS = (
    "expanded_occurrence_credit", "component_edge_credit",
    "maximality_credit", "exact_key_fibre_credit",
    "global_exact_key_disposition_credit", "Jx_Jy_same_point_glue_credit",
)


class VerificationError(RuntimeError):
    pass


def need(ok: bool, label: str) -> None:
    if not ok:
        raise VerificationError(label)


ENC = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return json.load(f)


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    return [dict(zip(columns, row)) for row in result[table]]


def box(values: list[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    return tuple(map(Q, values))  # type: ignore[return-value]


def rect(values: list[str]) -> tuple[Q, Q, Q, Q]:
    b = box(values)
    return b[2], b[3], b[4], b[5]


def stored_rect(values: list[str]) -> tuple[Q, Q, Q, Q]:
    need(len(values) == 6 and Q(values[0]) == 0 and Q(values[1]) == 0, "stored face")
    return tuple(map(Q, values[2:]))  # type: ignore[return-value]


def area(r: tuple[Q, Q, Q, Q]) -> Q:
    return (r[1] - r[0]) * (r[3] - r[2])


def intersect(a: tuple[Q, Q, Q, Q], b: tuple[Q, Q, Q, Q]):
    r = max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3])
    return None if r[0] >= r[1] or r[2] >= r[3] else r


def union_area(rs: list[tuple[Q, Q, Q, Q]]) -> tuple[Q, bool]:
    if not rs:
        return Q(0), True
    ps = sorted({x for r in rs for x in r[:2]})
    ss = sorted({x for r in rs for x in r[2:]})
    total, disjoint = Q(0), True
    for p0, p1 in zip(ps, ps[1:]):
        for s0, s1 in zip(ss, ss[1:]):
            n = sum(r[0] <= p0 and p1 <= r[1] and r[2] <= s0 and s1 <= r[3] for r in rs)
            if n:
                total += (p1-p0)*(s1-s0)
            disjoint &= n <= 1
    return total, disjoint


def complement(container: tuple[Q, Q, Q, Q], covered: list[tuple[Q, Q, Q, Q]]):
    clipped = [x for r in covered if (x := intersect(container, r)) is not None]
    ps = sorted({container[0], container[1], *(x for r in clipped for x in r[:2])})
    ss = sorted({container[2], container[3], *(x for r in clipped for x in r[2:])})
    out = []
    for p0, p1 in zip(ps, ps[1:]):
        for s0, s1 in zip(ss, ss[1:]):
            if not any(r[0] <= p0 and p1 <= r[1] and r[2] <= s0 and s1 <= r[3] for r in clipped):
                out.append((p0, p1, s0, s1))
    return sorted(out)


def verify() -> dict[str, Any]:
    for name, expected in PINS.items():
        need(file_sha(HERE / name) == expected, f"pin:{name}")
    result = read_json(RESULT)
    need(result["result_sha256"] == digest({k: v for k, v in result.items() if k != "result_sha256"}), "result digest")
    with gzip.open(LEDGER, "rb") as f:
        ledger = json.load(f)
    rows = ledger["rows"]
    need(len(rows) == 1276 and digest(rows) == ledger["rows_sha256"], "ledger closure")
    for row in rows:
        payload = dict(row); h = payload.pop("row_sha256")
        need(digest(payload) == h, "row digest")
        need(all(row[x] == 0 for x in ZERO_FIELDS), "zero credit")

    r174 = read_json(HERE / "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json")["result"]
    parents = unpack(r174, "parent_rows")
    r179 = read_json(HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json")["result"]
    origins = unpack(r179, "origin_tube_rows")
    walls = unpack(r179, "wall_normal_form_rows")
    outgoing = unpack(r179, "outgoing_normal_form_rows")
    resolved = unpack(r179, "resolved_3d_child_rows")
    retained = unpack(r179, "retained_3d_child_rows")
    guards = unpack(r179, "chart_guard_child_rows")
    origin_by = {r["origin_row_id"]: r for r in origins}
    wall_by = {r["row_id"]: r for r in walls}
    outgoing_by = {r["row_id"]: r for r in outgoing}
    children: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for kind, table in (("RESOLVED", resolved), ("RETAINED", retained), ("GUARD", guards)):
        for r in table: children[r["origin_row_id"]].append((kind, r))
    pos_owners: dict[str, list[tuple[dict[str, Any], dict[str, Any], tuple[Q,Q,Q,Q]]]] = defaultdict(list)
    for o in origins:
        b = box(o["original_box"])
        if b[0] == 0 and b[1] > 0:
            kids = [c for k,c in children[o["origin_row_id"]] if k == "RETAINED" and box(c["box"])[0] == 0]
            need(len(kids) == 1 and rect(kids[0]["box"]) == rect(o["original_box"]), "positive owner")
            pos_owners[o["chart"]].append((o, kids[0], rect(o["original_box"])))
    pos_parents: dict[str, list[tuple[dict[str, Any], tuple[Q,Q,Q,Q]]]] = defaultdict(list)
    for p in parents:
        b = box(p["box"])
        if b[0] == 0 and b[1] > 0: pos_parents[p["chart"]].append((p, rect(p["box"])))

    histogram = Counter()
    t0_area = owner_area = absence_area = Q(0)
    replaced_checked = 0
    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement_verifier as rv
    for row in rows:
        state = row["physical_disposition"]; histogram[state] += 1
        support = row["canonical_support_row_id"]
        if row["decision_family"] == "EXACT_SOURCE_T0_HALF_OPEN_OWNER":
            w = wall_by[support]; o = origin_by[w["origin_row_id"]]; b = box(o["original_box"]); face = rect(o["original_box"])
            t0_area += area(face)
            expected_patches = []
            if b[0] == 0:
                expected_patches = [(face, o["origin_row_id"])]
                expected_state = OWNER
            else:
                for po, _pc, pr in pos_owners[o["chart"]]:
                    if (hit := intersect(face, pr)) is not None: expected_patches.append((hit, po["origin_row_id"]))
                u, disjoint = union_area([x[0] for x in expected_patches]); need(disjoint, "owner disjoint")
                expected_state = SHADOW if u == area(face) else PARTITIONED if u else ABSENT
            actual_patches = sorted((stored_rect(x["patch_exact_bounds"]), x["positive_owner_origin_row_id"]) for x in row["owner_patches"])
            need(actual_patches == sorted(expected_patches), f"patch reconstruction:{support}")
            u, d = union_area([x[0] for x in expected_patches]); comp = complement(face, [x[0] for x in expected_patches])
            actual_comp = sorted(stored_rect(x["cell_exact_bounds"]) for x in row["absence_cells"])
            need(actual_comp == comp and d and state == expected_state, f"state/partition:{support}")
            need(all(intersect(c, pr) is None for c in comp for _p,pr in pos_parents[o["chart"]]), f"complement owner absent:{support}")
            need(u + sum(map(area, comp)) == area(face), f"area:{support}")
            owner_area += u; absence_area += sum(map(area, comp))
        else:
            normal = outgoing_by.get(support) or wall_by.get(support); need(normal is not None, "normal")
            o = origin_by[normal["origin_row_id"]]
            kids = children[o["origin_row_id"]]
            rr = sorted((c for k,c in kids if k == "RESOLVED"), key=lambda x: x["child_index"])
            need(o["fully_replaced_by_bounded_children"] and o["chosen_split_axis"] == "p" and len(rr) == 2 and all(k == "RESOLVED" for k,_c in kids), f"cover:{support}")
            need(sum(Q(c["coordinate_volume"]) for c in rr) == Q(o["original_coordinate_volume"]), "volume")
            if support in outgoing_by:
                signs = ["STRICT_POSITIVE" if c["outgoing_cell"] in {"E","W"} else "STRICT_NEGATIVE" for c in rr]
                need(len(set(signs)) == 1, f"outgoing sign:{support}")
            else:
                w = wall_by[support]; sn = "source_x" if w["axis"] == "X" else "source_y"; tn = "hit_x" if w["axis"] == "X" else "hit_y"
                pairs = []
                for c in rr:
                    bb = rv.box_from(c["box"], len(c["refinement_path"]), c["row_id"]); g = rv.independent_geometry(c["chart"], o["owner_target"], bb)
                    pairs.append((rv.arb_sign(rv.subtract_wall(g[sn], w["integer_wall"])[0]), rv.arb_sign(rv.subtract_wall(g[tn], w["integer_wall"])[0])))
                need(len(set(pairs)) == 1 and all(x in {"STRICT_NEGATIVE","STRICT_POSITIVE"} for pair in pairs for x in pair), f"wall signs:{support}")
            need(state == REPLACED, f"replacement state:{support}"); replaced_checked += 1

    expected = Counter({OWNER:440, SHADOW:372, PARTITIONED:8, ABSENT:60, REPLACED:396})
    need(histogram == expected and replaced_checked == 396, "final census")
    need(t0_area == Q(31,640) and owner_area == Q(59,1280) and absence_area == Q(3,1280), "global area")
    verification = {
        "schema": SCHEMA,
        "status": "PASS_INDEPENDENT_ROUND281_LOWER_STRATUM_TAIL_CLOSURE__ZERO_CREDIT",
        "pins": PINS,
        "census": {
            "verified_row_count": len(rows),
            "disposition_histogram": dict(sorted(histogram.items())),
            "reconstructed_t0_row_count": 880,
            "reconstructed_fully_replaced_row_count": replaced_checked,
            "total_t0_face_area": str(t0_area),
            "owner_or_shadow_area": str(owner_area),
            "absence_area": str(absence_area),
            "partition_delta": str(t0_area-owner_area-absence_area),
        },
        "strict_nonpromotion": result["strict_nonpromotion"],
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--output", type=Path, default=OUTPUT); args = ap.parse_args()
    value = verify(); args.output.write_bytes(canonical(value)+b"\n")


if __name__ == "__main__":
    main()
