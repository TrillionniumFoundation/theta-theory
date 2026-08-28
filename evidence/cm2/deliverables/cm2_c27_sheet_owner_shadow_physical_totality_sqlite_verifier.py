#!/usr/bin/env python3
"""Independent SQLite verifier for SHEET_OWNER/SHEET_SHADOW physical totality.

The 17,940-sheet candidate universe is rebuilt before any C21/C25/C26 row is
read.  R204 candidates come from opposite target-factor signs in the complete
open-region geometry.  R211 candidates come from the complete R208 leaf and
region geometry, with factor signs and the pinned R173 E/W half-open rule
deriving the unique owner and N/S shadow.  C15/C20/C21/C25/C26 are consumed
only afterwards as current-lineage and theorem bindings.

This module deliberately does not import the streamed producer, Round306C27,
its FAMILIES declaration, or any edge ledger.  SQLite insertion order is
seeded, while every semantic comparison is canonical and order-independent.
The conclusion is local zero credit and does not promote C27/C28/C29.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import sqlite3
import sys
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
R173 = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C20 = "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz"
C21A = "cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel_ledger.jsonl.gz"
C21B = "cm2_round306c21b_source_g_17716_r211_self_contained_sheet_theorem_materialization_ledger.jsonl.gz"
C21C = "cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
PINS = {
    R173: "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208: "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C20: "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    C21A: "1c60f2ef752b1b3ab363740cec7505cbddacfbc7509922dab63bbf011e3659f1",
    C21B: "1500052cf49cfa7a22388567173a912be6b79d2ba647ad5d1906f9e170dc26bb",
    C21C: "add22270845ef504427475e91696451f2d53c41b4b2cb9af2784a9507ce60c09",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
}
CELL_SIGNS = {
    "E": ("STRICT_POSITIVE", "STRICT_POSITIVE"),
    "N": ("STRICT_POSITIVE", "STRICT_NEGATIVE"),
    "W": ("STRICT_NEGATIVE", "STRICT_NEGATIVE"),
    "S": ("STRICT_NEGATIVE", "STRICT_POSITIVE"),
}
SIGN_CELL = {value: key for key, value in CELL_SIGNS.items()}
OPPOSITE = {"STRICT_NEGATIVE": "STRICT_POSITIVE", "STRICT_POSITIVE": "STRICT_NEGATIVE"}
NONPROMOTION_21 = {"B1A": 0, "B2": 0, "CM2": 0, "DSU_edge": 0, "DSU_union": 0, "maximality": 0}
NONPROMOTION_26 = {
    "B2": 0, "CM2": 0, "DSU_edge": 0, "maximality": 0,
    "member_identity": 0, "pair_routing": 0, "transition_theorem": 0,
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def close_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body), "row closure:" + label)


def source_rows(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), f"newline:{name}:{ordinal}")
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) + b"\n" == raw, f"canonical:{name}:{ordinal}")
            close_row(row, f"{name}:{ordinal}")
            yield row


def envelope(name: str) -> dict[str, Any]:
    value = json.loads((ROOT / name).read_bytes())
    need(type(value) is dict and set(value) == {"schema", "result", "result_sha256"}, "envelope shape:" + name)
    need(value["result_sha256"] == digest(value["result"]), "envelope closure:" + name)
    return value["result"]


def validate_pins() -> dict[str, str]:
    observed = {name: file_sha(ROOT / name) for name in sorted(PINS)}
    need(observed == {name: PINS[name] for name in sorted(PINS)}, "exact input pins")
    return observed


def shuffled(values: Iterable[tuple[Any, ...]], rng: random.Random) -> list[tuple[Any, ...]]:
    output = list(values)
    rng.shuffle(output)
    return output


def make_database() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA journal_mode=MEMORY")
    db.execute("PRAGMA synchronous=OFF")
    db.executescript("""
      CREATE TABLE candidate(
        sheet_id TEXT PRIMARY KEY, source_class TEXT NOT NULL, mechanism TEXT NOT NULL,
        chart TEXT NOT NULL, ambient_box TEXT NOT NULL, equation_kind TEXT NOT NULL,
        equation_parameter TEXT NOT NULL, inclusion_rule TEXT NOT NULL,
        owner TEXT NOT NULL, shadow TEXT NOT NULL, owner_side TEXT NOT NULL,
        shadow_side TEXT NOT NULL, primitive_sheet_sha TEXT NOT NULL,
        owner_region_sha TEXT NOT NULL, shadow_region_sha TEXT NOT NULL
      ) WITHOUT ROWID;
      CREATE TABLE current15(member TEXT PRIMARY KEY, component TEXT NOT NULL, row_sha TEXT NOT NULL) WITHOUT ROWID;
      CREATE TABLE current20(member TEXT PRIMARY KEY, family TEXT NOT NULL, chart TEXT NOT NULL,
        bounds TEXT NOT NULL, support_sha TEXT NOT NULL, source_region_sha TEXT NOT NULL,
        row_sha TEXT NOT NULL) WITHOUT ROWID;
      CREATE TABLE current25(member TEXT PRIMARY KEY, component TEXT NOT NULL,
        semantic_kind TEXT NOT NULL, normalized_sha TEXT NOT NULL, c15_sha TEXT NOT NULL,
        kernel TEXT NOT NULL, kernel_sha TEXT NOT NULL, row_sha TEXT NOT NULL) WITHOUT ROWID;
      CREATE TABLE c21a(sheet_id TEXT PRIMARY KEY, owner TEXT NOT NULL, shadow TEXT NOT NULL,
        source_sha TEXT NOT NULL, theorem_sha TEXT NOT NULL, theorem_kind TEXT NOT NULL,
        derivative TEXT NOT NULL, credit TEXT NOT NULL, nonpromotion TEXT NOT NULL,
        row_sha TEXT NOT NULL) WITHOUT ROWID;
      CREATE TABLE c21b(sheet_id TEXT PRIMARY KEY, owner TEXT NOT NULL, shadow TEXT NOT NULL,
        theorem_kind TEXT NOT NULL, identity_on_sheet TEXT NOT NULL, credit TEXT NOT NULL,
        nonpromotion TEXT NOT NULL, row_sha TEXT NOT NULL) WITHOUT ROWID;
      CREATE TABLE c21c(sheet_id TEXT PRIMARY KEY, owner TEXT NOT NULL, c21b_sha TEXT NOT NULL,
        theorem_sha TEXT NOT NULL, theorem_kind TEXT NOT NULL, credit TEXT NOT NULL,
        nonpromotion TEXT NOT NULL, row_sha TEXT NOT NULL) WITHOUT ROWID;
      CREATE TABLE c26(feature_id TEXT PRIMARY KEY, kind TEXT NOT NULL, role TEXT NOT NULL,
        owner TEXT NOT NULL, dependencies TEXT NOT NULL, theorem_sha TEXT NOT NULL,
        kernel TEXT NOT NULL, source_sha TEXT NOT NULL, credit TEXT NOT NULL,
        nonpromotion TEXT NOT NULL, row_sha TEXT NOT NULL) WITHOUT ROWID;
    """)
    return db


def signature_core(signature: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in signature.items() if key not in {"outgoing_cell", "target_chart"}}


def reconstruct_r204(db: sqlite3.Connection, result: dict[str, Any], rng: random.Random) -> None:
    regions = result["formal_local_open_3D_region_ledger"]["rows"]
    sheets = result["formal_2D_sheet_lineage"]["target_sheet_rows"]
    need(len(regions) == 736 and len(sheets) == 224, "R204 primitive census")
    sheet_index: dict[str, dict[str, Any]] = {}
    for row in sheets:
        close_row(row, "R204 sheet")
        need(row["sheet_row_id"] not in sheet_index, "R204 unique sheet")
        sheet_index[row["sheet_row_id"]] = row
    temporary = sqlite3.connect(":memory:")
    temporary.execute("CREATE TABLE region(leaf TEXT,region TEXT PRIMARY KEY,sign TEXT,incident INT,sheet TEXT,payload TEXT)")
    insertions = []
    for row in regions:
        close_row(row, "R204 region")
        if row["target_graph_sheet_incident"]:
            need(row["target_sheet_row_id"] is not None, "R204 incident sheet id")
        else:
            need(row["target_sheet_row_id"] is None, "R204 nonincident null sheet")
        insertions.append((row["leaf_row_id"], row["region_row_id"], row["target_factor_sign"], int(row["target_graph_sheet_incident"]), row["target_sheet_row_id"], canonical(row).decode()))
    temporary.executemany("INSERT INTO region VALUES(?,?,?,?,?,?)", shuffled(insertions, rng))
    need(temporary.execute("SELECT count(*) FROM region").fetchone()[0] == 736, "R204 SQL region census")
    malformed = temporary.execute("SELECT leaf FROM region WHERE incident=1 GROUP BY leaf HAVING count(*)<>2 OR sum(sign='POSITIVE')<>1 OR sum(sign='NEGATIVE')<>1 OR count(DISTINCT sheet)<>1").fetchall()
    need(not malformed, "R204 opposite-side SQL partition")
    pairs = temporary.execute("""
      SELECT p.payload,n.payload FROM region p JOIN region n ON n.leaf=p.leaf
      WHERE p.incident=1 AND n.incident=1 AND p.sign='POSITIVE' AND n.sign='NEGATIVE'
      ORDER BY p.leaf COLLATE BINARY
    """).fetchall()
    need(len(pairs) == 224, "R204 generated sheet denominator")
    generated: list[tuple[Any, ...]] = []
    for positive_raw, negative_raw in pairs:
        positive, negative = json.loads(positive_raw), json.loads(negative_raw)
        common = ("chart", "owner_target", "wall_axis", "integer_wall", "leaf_exact_box", "origin_row_id", "parent_id")
        need(all(positive[key] == negative[key] for key in common), "R204 paired primitive geometry")
        identity = [positive["leaf_row_id"], positive["chart"], positive["owner_target"], positive["wall_axis"], positive["integer_wall"], positive["leaf_exact_box"][2:]]
        sheet_id = "round204-target-graph-sheet-cell:" + digest(identity)
        need(positive["target_sheet_row_id"] == negative["target_sheet_row_id"] == sheet_id, "R204 derived sheet id")
        sheet = sheet_index.get(sheet_id)
        need(sheet is not None, "R204 primitive sheet binding exists")
        need(
            sheet["leaf_row_id"] == positive["leaf_row_id"]
            and sheet["chart"] == positive["chart"]
            and sheet["owner_target"] == positive["owner_target"]
            and sheet["wall_axis"] == positive["wall_axis"]
            and sheet["integer_wall"] == positive["integer_wall"]
            and sheet["base_p_s_exact_bounds"] == positive["leaf_exact_box"][2:]
            and sheet["leaf_t_exact_bounds"] == positive["leaf_exact_box"][:2]
            and sheet["target_factor_graph_axis"] == "t"
            and sheet["target_t_derivative_sign"] == "STRICT_POSITIVE"
            and sheet["half_open_owner_policy"] == "TARGET_FACTOR_POSITIVE_SIDE_OWNS__NEGATIVE_SIDE_IS_SHADOW",
            "R204 regular sheet physical rule",
        )
        need(
            sheet["positive_side_region_row_id"] == positive["region_row_id"]
            and sheet["negative_side_region_row_id"] == negative["region_row_id"]
            and sheet["half_open_owner_region_row_id"] == positive["region_row_id"]
            and sheet["half_open_shadow_region_row_id"] == negative["region_row_id"],
            "R204 declaration agrees after sign derivation",
        )
        generated.append((
            sheet_id, "R204", "R204_TARGET_REGULAR_GRAPH_SHEET", sheet["chart"],
            canonical(positive["leaf_exact_box"]).decode(), "TARGET_FACTOR_MINUS_INTEGER_WALL_EQUALS_ZERO",
            canonical({"target": sheet["owner_target"], "wall_axis": sheet["wall_axis"], "integer_wall": sheet["integer_wall"]}).decode(),
            "POSITIVE_OPEN_SIDE_PLUS_EQUALITY_SHEET_OWNS", positive["region_row_id"], negative["region_row_id"],
            "TARGET_FACTOR_STRICT_POSITIVE", "TARGET_FACTOR_STRICT_NEGATIVE", sheet["row_sha256"], positive["row_sha256"], negative["row_sha256"],
        ))
    need(set(sheet_index) == {row[0] for row in generated}, "R204 no orphan primitive sheet")
    db.executemany("INSERT INTO candidate VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", shuffled(generated, rng))
    temporary.close()


def reconstruct_r211(db: sqlite3.Connection, result: dict[str, Any], rng: random.Random) -> None:
    leaves = result["formal_leaf_geometry_ledger"]["rows"]
    regions = result["formal_local_open_3D_signature_ledger"]["rows"]
    need(len(leaves) == 18_324 and len(regions) == 36_040, "R208 primitive census")
    temporary = sqlite3.connect(":memory:")
    temporary.executescript("CREATE TABLE leaf(id TEXT PRIMARY KEY,class TEXT,payload TEXT); CREATE TABLE region(id TEXT PRIMARY KEY,leaf TEXT,cell TEXT,payload TEXT);")
    leaf_rows = []
    for row in leaves:
        close_row(row, "R208 leaf")
        leaf_rows.append((row["leaf_row_id"], row["final_graph_classification"], canonical(row).decode()))
    region_rows = []
    for row in regions:
        close_row(row, "R208 region")
        region_rows.append((row["region_row_id"], row["leaf_row_id"], row["outgoing_cell"], canonical(row).decode()))
    temporary.executemany("INSERT INTO leaf VALUES(?,?,?)", shuffled(leaf_rows, rng))
    temporary.executemany("INSERT INTO region VALUES(?,?,?,?)", shuffled(region_rows, rng))
    need(temporary.execute("SELECT count(*) FROM leaf").fetchone()[0] == 18_324 and temporary.execute("SELECT count(*) FROM region").fetchone()[0] == 36_040, "R208 SQL census")
    need(temporary.execute("SELECT count(*) FROM leaf WHERE class='EMPTY'").fetchone()[0] == 608, "R208 empty census")
    empty_bad = temporary.execute("SELECT l.id FROM leaf l LEFT JOIN region r ON r.leaf=l.id WHERE l.class='EMPTY' GROUP BY l.id HAVING count(r.id)<>1").fetchall()
    need(not empty_bad, "R208 empty leaf exclusion")
    malformed = temporary.execute("""
      SELECT l.id FROM leaf l LEFT JOIN region r ON r.leaf=l.id
      WHERE l.class<>'EMPTY' GROUP BY l.id
      HAVING count(r.id)<>2 OR sum(r.cell IN ('E','W'))<>1 OR sum(r.cell IN ('N','S'))<>1
    """).fetchall()
    need(not malformed, "R208 owner/shadow SQL partition")
    pairs = temporary.execute("""
      SELECT l.payload,o.payload,h.payload FROM leaf l
      JOIN region o ON o.leaf=l.id AND o.cell IN ('E','W')
      JOIN region h ON h.leaf=l.id AND h.cell IN ('N','S')
      WHERE l.class<>'EMPTY' ORDER BY l.id COLLATE BINARY
    """).fetchall()
    need(len(pairs) == 17_716, "R211 generated sheet denominator")
    generated: list[tuple[Any, ...]] = []
    for leaf_raw, owner_raw, shadow_raw in pairs:
        leaf, owner, shadow = json.loads(leaf_raw), json.loads(owner_raw), json.loads(shadow_raw)
        need(
            leaf["final_graph_classification"] in {"CLIPPED_2D_BOUNDARY_1D", "FULL_2D"}
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and leaf["side_specific_signature_candidate_region_count"] == 2
            and leaf["candidate_region_signs"] == ["STRICT_NEGATIVE", "STRICT_POSITIVE"],
            "R208 nonempty leaf sheet contract",
        )
        need(owner["F_sign"] == "STRICT_POSITIVE" and shadow["F_sign"] == "STRICT_NEGATIVE", "R211 F-side partition")
        inactive = owner["inactive_factor"]
        need(inactive == shadow["inactive_factor"] and inactive in {"HPLUS", "HMINUS"}, "R211 common inactive factor")
        active = "HMINUS" if inactive == "HPLUS" else "HPLUS"
        need(owner["whole_box_factor_C0"] == shadow["whole_box_factor_C0"], "R211 C0 pair equality")
        c0 = owner["whole_box_factor_C0"][inactive]
        inactive_sign = c0["selected_sign"]
        need(inactive_sign in OPPOSITE, "R211 strict inactive sign")
        if c0["direct_sign"] == inactive_sign:
            c0_proof = "DIRECT_WHOLE_BOX_C0"
        else:
            need(c0["centered_sign"] == inactive_sign, "R211 centered C0 proof")
            c0_proof = "CENTERED_WHOLE_BOX_C0"
        owner_cell = "E" if inactive_sign == "STRICT_POSITIVE" else "W"
        active_shadow_sign = OPPOSITE[inactive_sign]
        shadow_signs = (active_shadow_sign, inactive_sign) if active == "HPLUS" else (inactive_sign, active_shadow_sign)
        shadow_cell = SIGN_CELL[shadow_signs]
        need(owner["outgoing_cell"] == owner_cell and shadow["outgoing_cell"] == shadow_cell, "R211 factor-derived chart roles")
        need((owner["HPLUS_sign"], owner["HMINUS_sign"]) == CELL_SIGNS[owner_cell] and (shadow["HPLUS_sign"], shadow["HMINUS_sign"]) == CELL_SIGNS[shadow_cell], "R211 exact chart sign table")
        need(owner[active + "_sign"] == owner[inactive + "_sign"] == inactive_sign and shadow[inactive + "_sign"] == inactive_sign and shadow[active + "_sign"] == OPPOSITE[inactive_sign], "R211 active/inactive factor sides")
        owner_signature, shadow_signature = owner["local_return_signature"], shadow["local_return_signature"]
        owner_prefix = owner_signature["target_lift"].split("[", 1)[0]
        shadow_prefix = shadow_signature["target_lift"].split("[", 1)[0]
        core = signature_core(owner_signature)
        need(core == signature_core(shadow_signature), "R211 signature cores")
        need(owner_signature["target_chart"] == f"{owner_prefix}:{owner_cell}" and shadow_signature["target_chart"] == f"{shadow_prefix}:{shadow_cell}", "R211 chart transport")
        relation = "HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET" if active == "HPLUS" else "HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET"
        identity = {"leaf_row_id": leaf["leaf_row_id"], "owner_region_row_id": owner["region_row_id"], "shadow_region_row_id": shadow["region_row_id"], "rule": "E_OR_W_OWNS__N_OR_S_SHADOWS"}
        probe_id = "round209-half-open-sheet:" + digest(identity)
        probe_body = {
            "sheet_row_id": probe_id, "leaf_row_id": leaf["leaf_row_id"], "origin_row_id": leaf["origin_row_id"],
            "occurrence_row_id": leaf["occurrence_row_id"], "retained_child_row_id": leaf["retained_child_row_id"],
            "leaf_classification": leaf["final_graph_classification"], "active_factor": active, "inactive_factor": inactive,
            "inactive_factor_whole_box_C0_proof": c0_proof, "inactive_factor_whole_box_strict_sign": inactive_sign,
            "factor_identity_on_sheet": relation, "Nx_sign_on_sheet": inactive_sign,
            "owner_region_row_id": owner["region_row_id"], "shadow_region_row_id": shadow["region_row_id"],
            "owner_outgoing_cell": owner_cell, "shadow_outgoing_cell": shadow_cell,
            "owner_signature_core_sha256": digest(core), "shadow_signature_core_sha256": digest(core),
            "signature_difference_field_allowlist": ["outgoing_cell", "target_chart"],
            "Round173_half_open_rule": "E or W owns; N or S excludes", "deterministic_unique_owner_lineage": True,
            "incidence_is_not_a_global_component": True, "formal_half_open_owner_credit": 0,
            "whole_original_tube_credit": 0, "global_exact_key_disposition_credit": 0,
        }
        probe_sha = digest(probe_body)
        sheet_id = "round211-half-open-sheet-owner:" + digest({"probe_id": probe_id, "probe_row_sha256": probe_sha})
        generated.append((
            sheet_id, "R211", "R211_ACTIVE_FACTOR_ZERO_SHEET", owner_signature["source_chart"], canonical(leaf["box"]).decode(),
            "ACTIVE_FACTOR_EQUALS_ZERO", canonical({"active_factor": active, "inactive_factor": inactive, "inactive_factor_strict_sign": inactive_sign, "factor_identity_on_sheet": relation}).decode(),
            "E_OR_W_OPEN_SIDE_PLUS_EQUALITY_SHEET_OWNS", owner["region_row_id"], shadow["region_row_id"],
            "OUTGOING_CELL_IN_E_OR_W", "OUTGOING_CELL_IN_N_OR_S", probe_sha, owner["row_sha256"], shadow["row_sha256"],
        ))
    db.executemany("INSERT INTO candidate VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", shuffled(generated, rng))
    temporary.close()


def generate_primitive_candidates(seed: int) -> tuple[sqlite3.Connection, dict[str, str]]:
    need(type(seed) is int and seed >= 0, "nonnegative declared seed")
    pins = validate_pins()
    r173 = envelope(R173)
    contract = r173["outgoing_chart_contract"]
    need(contract["diagonal_seam_rule"] == "E or W owns; N or S excludes" and contract["owner_set"] == ["E", "W"] and contract["strict_chart_transport_is_total_on_E_W_N_S"] is True, "R173 physical half-open convention")
    db = make_database()
    rng = random.Random(seed)
    reconstruct_r204(db, envelope(R204), rng)
    reconstruct_r211(db, envelope(R208), rng)
    need(db.execute("SELECT count(*) FROM candidate").fetchone()[0] == 17_940, "combined primitive candidate denominator")
    need(dict(db.execute("SELECT source_class,count(*) FROM candidate GROUP BY source_class")) == {"R204": 224, "R211": 17_716}, "combined primitive class census")
    need(db.execute("SELECT count(DISTINCT sheet_id) FROM candidate").fetchone()[0] == 17_940, "unique primitive sheets")
    return db, pins


def load_bindings(db: sqlite3.Connection, rng: random.Random) -> None:
    """Read current ledgers only after the primitive candidate table is closed."""
    role_members = {row[0] for row in db.execute("SELECT owner FROM candidate UNION SELECT shadow FROM candidate")}
    need(len(role_members) == 35_880, "distinct primitive role members")
    candidate_ids = {row[0] for row in db.execute("SELECT sheet_id FROM candidate")}

    rows15 = []
    for ordinal, row in enumerate(source_rows(C15)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        if row["registry_member_id"] in role_members:
            rows15.append((row["registry_member_id"], row["fresh_component_id"], row["row_sha256"]))
    db.executemany("INSERT INTO current15 VALUES(?,?,?)", shuffled(rows15, rng))
    need(len(rows15) == len(role_members), "C15 role-member cover")

    candidate_geometry = {}
    for sheet, source_class, chart, bounds, owner, shadow, owner_sha, shadow_sha in db.execute("SELECT sheet_id,source_class,chart,ambient_box,owner,shadow,owner_region_sha,shadow_region_sha FROM candidate"):
        family = "ROUND204_REGION" if source_class == "R204" else "ROUND208_REGION"
        candidate_geometry[owner] = (family, chart, bounds, owner_sha)
        candidate_geometry[shadow] = (family, chart, bounds, shadow_sha)
    rows20 = []
    for row in source_rows(C20):
        member = row["member_id"]
        if member not in role_members:
            continue
        family, chart, bounds, primitive_sha = candidate_geometry[member]
        support = row["support_ast"]
        need(row["fine_family"] == family and row["construction_certificate"]["source_row_sha256"] == primitive_sha, "C20 primitive provenance")
        need(support["kind"] == "OPEN_RATIONAL_BOX" and support["coordinate_chart"] == chart and support["coordinates"] == ["t", "p", "s"] and canonical(support["bounds"]).decode() == bounds, "C20 exact primitive open box")
        need(row["support_ast_sha256"] == digest(support), "C20 support closure")
        rows20.append((member, family, chart, bounds, row["support_ast_sha256"], primitive_sha, row["row_sha256"]))
    db.executemany("INSERT INTO current20 VALUES(?,?,?,?,?,?,?)", shuffled(rows20, rng))
    need(len(rows20) == len(role_members), "C20 role-member cover")

    rows25 = []
    for row in source_rows(C25):
        member = row["member_id"]
        if member not in role_members:
            continue
        binding = row["source_bindings"]
        rows25.append((member, row["fresh_component_id"], row["support_semantic_kind"], row["normalized_support_ast_sha256"], binding["C15_member_row_sha256"], binding["support_kernel"], binding["support_kernel_row_sha256"], row["row_sha256"]))
    db.executemany("INSERT INTO current25 VALUES(?,?,?,?,?,?,?,?)", shuffled(rows25, rng))
    need(len(rows25) == len(role_members), "C25 role-member cover")

    rows21a = []
    census21a: Counter[str] = Counter()
    for row in source_rows(C21A):
        census21a[row["obligation_kind"]] += 1
        if row["obligation_kind"] != "A1_R204_TARGET_SHEET":
            continue
        ast = row["feature_theorem_ast"]
        rows21a.append((row["feature_row_id"], row["owner_member_id"], row["shadow_member_id"], row["source_row_sha256"], row["feature_theorem_ast_sha256"], ast["kind"], ast["strict_t_derivative_sign"], canonical(row["formal_credit"]).decode(), canonical(row["strict_nonpromotion"]).decode(), row["row_sha256"]))
    need(census21a == {"A1_R204_TARGET_SHEET": 224, "A2_R204_SOURCE_TARGET_CURVE": 504, "A2_R204_SOURCE_TARGET_ENDPOINT": 280}, "C21A census")
    db.executemany("INSERT INTO c21a VALUES(?,?,?,?,?,?,?,?,?,?)", shuffled(rows21a, rng))

    rows21b = []
    for row in source_rows(C21B):
        ast = row["theorem_ast"]
        rows21b.append((row["R211_sheet_row_id"], row["owner_member_id"], row["shadow_member_id"], ast["kind"], ast["exact_identity_on_active_sheet"], canonical(row["formal_credit"]).decode(), canonical(row["strict_nonpromotion"]).decode(), row["row_sha256"]))
    db.executemany("INSERT INTO c21b VALUES(?,?,?,?,?,?,?,?)", shuffled(rows21b, rng))
    need(len(rows21b) == 17_716, "C21B census")

    rows21c = []
    census21c: Counter[str] = Counter()
    for row in source_rows(C21C):
        census21c[row["obligation_kind"]] += 1
        if row["obligation_kind"] != "A1_R211_OWNER_SHEET":
            continue
        rows21c.append((row["feature_row_id"], row["owner_member_id"], row["source_bindings"]["C21b_sheet_theorem_row_sha256"], row["theorem_ast_sha256"], row["theorem_ast"]["kind"], canonical(row["formal_credit"]).decode(), canonical(row["strict_nonpromotion"]).decode(), row["row_sha256"]))
    need(census21c == {"A1_R211_OWNER_SHEET": 17_716, "A2_R211_OWNER_CURVE": 20_456, "A2_R211_OWNER_ENDPOINT": 40_912}, "C21C census")
    db.executemany("INSERT INTO c21c VALUES(?,?,?,?,?,?,?,?)", shuffled(rows21c, rng))

    rows26 = []
    node_census: Counter[str] = Counter()
    for ordinal, row in enumerate(source_rows(C26)):
        need(row["feature_ordinal"] == ordinal, "C26 ordinal")
        node_census[row["node_id"]] += 1
        if row["node_id"] != "A1":
            continue
        binding = row["source_bindings"]
        rows26.append((row["feature_id"], row["obligation_kind"], row["obligation_role"], row["owner_member_id"], canonical(row["depends_on_node_ids"]).decode(), row["definition_or_dependency_theorem_ast_sha256"], binding["source_kernel"], binding["source_row_sha256"], canonical(row["formal_credit"]).decode(), canonical(row["strict_nonpromotion"]).decode(), row["row_sha256"]))
    need(node_census == {"A1": 17_940, "A2": 62_152, "G1": 5_264, "G2A": 5_264, "G2B": 10_128, "R1": 295_340, "R2": 295_336}, "C26 census")
    db.executemany("INSERT INTO c26 VALUES(?,?,?,?,?,?,?,?,?,?,?)", shuffled(rows26, rng))
    need(len(rows26) == len(candidate_ids) == 17_940, "C26 A1 denominator")
    db.commit()


def validate_post_generation_bindings(db: sqlite3.Connection) -> None:
    need(db.execute("SELECT count(*) FROM current15").fetchone()[0] == 35_880, "C15 SQL cover")
    need(db.execute("SELECT count(*) FROM current20").fetchone()[0] == 35_880, "C20 SQL cover")
    need(db.execute("SELECT count(*) FROM current25").fetchone()[0] == 35_880, "C25 SQL cover")
    bad_current = db.execute("""
      SELECT c.sheet_id FROM candidate c
      LEFT JOIN current15 o15 ON o15.member=c.owner LEFT JOIN current15 h15 ON h15.member=c.shadow
      LEFT JOIN current20 o20 ON o20.member=c.owner LEFT JOIN current20 h20 ON h20.member=c.shadow
      LEFT JOIN current25 o25 ON o25.member=c.owner LEFT JOIN current25 h25 ON h25.member=c.shadow
      WHERE o15.member IS NULL OR h15.member IS NULL OR o20.member IS NULL OR h20.member IS NULL OR o25.member IS NULL OR h25.member IS NULL
         OR c.owner=c.shadow OR o15.component<>h15.component OR o25.component<>o15.component OR h25.component<>h15.component
         OR o25.semantic_kind<>'EXACT_MEMBER_SUPPORT_EQUALITY' OR h25.semantic_kind<>'EXACT_MEMBER_SUPPORT_EQUALITY'
         OR o25.normalized_sha<>o20.support_sha OR h25.normalized_sha<>h20.support_sha
         OR o25.c15_sha<>o15.row_sha OR h25.c15_sha<>h15.row_sha
         OR o25.kernel<>'C20A' OR h25.kernel<>'C20A' OR o25.kernel_sha<>o20.row_sha OR h25.kernel_sha<>h20.row_sha
    """).fetchall()
    need(not bad_current, "exact current C15/C20/C25 support/component join")

    expected21 = canonical(NONPROMOTION_21).decode()
    expected26 = canonical(NONPROMOTION_26).decode()
    bad204 = db.execute("""
      SELECT c.sheet_id FROM candidate c
      LEFT JOIN c21a a ON a.sheet_id=c.sheet_id LEFT JOIN c26 f ON f.feature_id=c.sheet_id
      WHERE c.source_class='R204' AND (a.sheet_id IS NULL OR f.feature_id IS NULL
        OR a.owner<>c.owner OR a.shadow<>c.shadow OR a.source_sha<>c.primitive_sheet_sha
        OR a.theorem_kind<>'A1_UNIQUE_TARGET_REGULAR_GRAPH_SHEET' OR a.derivative<>'STRICT_POSITIVE'
        OR a.credit<>? OR a.nonpromotion<>? OR f.kind<>'A1_R204_TARGET_SHEET'
        OR f.role<>'INDEPENDENT_DEFINITION_ROOT' OR f.dependencies<>'[]' OR f.owner<>c.owner
        OR f.theorem_sha<>a.theorem_sha OR f.kernel<>'C21A' OR f.source_sha<>a.row_sha
        OR f.credit<>? OR f.nonpromotion<>?)
    """, (canonical({"A1": 1, "A2": 0}).decode(), expected21, canonical({"B1A_feature_obligation": 1, "dependent_feature_closure": 0, "source_free_definition_root": 1}).decode(), expected26)).fetchall()
    need(not bad204, "R204 post-generation C21A/C26 join")
    bad211 = db.execute("""
      SELECT c.sheet_id FROM candidate c
      LEFT JOIN c21b b ON b.sheet_id=c.sheet_id LEFT JOIN c21c a ON a.sheet_id=c.sheet_id
      LEFT JOIN c26 f ON f.feature_id=c.sheet_id
      WHERE c.source_class='R211' AND (b.sheet_id IS NULL OR a.sheet_id IS NULL OR f.feature_id IS NULL
        OR b.owner<>c.owner OR b.shadow<>c.shadow OR b.theorem_kind<>'SELF_CONTAINED_REGULAR_R211_ACTIVE_FACTOR_ZERO_SHEET'
        OR b.identity_on_sheet<>json_extract(c.equation_parameter,'$.factor_identity_on_sheet') OR b.credit<>? OR b.nonpromotion<>?
        OR a.owner<>c.owner OR a.c21b_sha<>b.row_sha OR a.theorem_kind<>'A1_R211_REGULAR_ACTIVE_FACTOR_ZERO_SHEET_DISCHARGE'
        OR a.credit<>? OR a.nonpromotion<>? OR f.kind<>'A1_R211_OWNER_SHEET'
        OR f.role<>'INDEPENDENT_DEFINITION_ROOT' OR f.dependencies<>'[]' OR f.owner<>c.owner
        OR f.theorem_sha<>a.theorem_sha OR f.kernel<>'C21C' OR f.source_sha<>a.row_sha
        OR f.credit<>? OR f.nonpromotion<>?)
    """, (canonical({"A1_obligation_discharge": 0, "A2_obligation_discharge": 0, "self_contained_sheet_theorem_materialization": 1}).decode(), expected21, canonical({"A1": 1, "A2": 0}).decode(), expected21, canonical({"B1A_feature_obligation": 1, "dependent_feature_closure": 0, "source_free_definition_root": 1}).decode(), expected26)).fetchall()
    need(not bad211, "R211 post-generation C21B/C21C/C26 join")
    need(db.execute("SELECT count(*) FROM c21a").fetchone()[0] == 224 and db.execute("SELECT count(*) FROM c21b").fetchone()[0] == 17_716 and db.execute("SELECT count(*) FROM c21c").fetchone()[0] == 17_716 and db.execute("SELECT count(*) FROM c26").fetchone()[0] == 17_940, "post-generation theorem table census")
    need(not db.execute("SELECT a.sheet_id FROM c21a a LEFT JOIN candidate c ON c.sheet_id=a.sheet_id WHERE c.sheet_id IS NULL").fetchall(), "no orphan C21A sheet")
    need(not db.execute("SELECT b.sheet_id FROM c21b b LEFT JOIN candidate c ON c.sheet_id=b.sheet_id WHERE c.sheet_id IS NULL").fetchall(), "no orphan C21B sheet")
    need(not db.execute("SELECT f.feature_id FROM c26 f LEFT JOIN candidate c ON c.sheet_id=f.feature_id WHERE c.sheet_id IS NULL").fetchall(), "no orphan C26 A1")


def materialize_reference(db: sqlite3.Connection) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    roles: list[dict[str, Any]] = []
    companions: list[dict[str, Any]] = []
    query = """
      SELECT c.sheet_id,c.source_class,c.mechanism,c.chart,c.ambient_box,c.equation_kind,c.equation_parameter,c.inclusion_rule,
             c.owner,c.shadow,c.owner_side,c.shadow_side,c.primitive_sheet_sha,c.shadow_region_sha,
             o15.component,o15.row_sha,h15.row_sha,o25.row_sha,h25.row_sha,
             CASE WHEN c.source_class='R204' THEN a.row_sha ELSE d.row_sha END,
             CASE WHEN c.source_class='R204' THEN a.theorem_sha ELSE d.theorem_sha END,
             f.row_sha
      FROM candidate c JOIN current15 o15 ON o15.member=c.owner JOIN current15 h15 ON h15.member=c.shadow
      JOIN current25 o25 ON o25.member=c.owner JOIN current25 h25 ON h25.member=c.shadow
      LEFT JOIN c21a a ON a.sheet_id=c.sheet_id LEFT JOIN c21c d ON d.sheet_id=c.sheet_id
      JOIN c26 f ON f.feature_id=c.sheet_id ORDER BY c.sheet_id COLLATE BINARY
    """
    for values in db.execute(query):
        (sheet_id, source_class, mechanism, chart, bounds_raw, equation_kind, parameter_raw, inclusion_rule,
         owner, shadow, owner_side, shadow_side, primitive_sha, shadow_region_sha, component,
         owner15, shadow15, owner25, shadow25, theorem_row, theorem_ast, c26_row) = values
        companion_body = {
            "schema": "cm2.c27.independent-sheet-shadow-companion.v1.row.v1", "physical_sheet_id": sheet_id,
            "source_class": source_class, "mechanism": mechanism, "shadow_member_id": shadow, "owner_member_id": owner,
            "fresh_component_id": component, "shadow_open_side": shadow_side, "equality_sheet_included": False,
            "exclusion_reason": "HALF_OPEN_EQUALITY_SHEET_ASSIGNED_TO_UNIQUE_OWNER_SIDE", "primitive_sheet_row_sha256": primitive_sha,
            "primitive_shadow_region_row_sha256": shadow_region_sha, "shadow_C15_row_sha256": shadow15,
            "shadow_C25_row_sha256": shadow25, "C26_owner_root_row_sha256": c26_row,
            "C26_shadow_node_was_absent_and_not_used_as_authority": True, "formal_credit": 0,
        }
        node_id = "cm2-c27-independent-shadow-companion:" + digest(companion_body)
        companion_preordinal = {**companion_body, "materialized_shadow_node_id": node_id}
        companion_preordinal["row_sha256"] = digest(companion_preordinal)
        companions.append(companion_preordinal)
        common = {
            "schema": "cm2.c27.sheet-owner-shadow-physical-totality.v1.row.v1", "physical_sheet_id": sheet_id,
            "source_class": source_class, "mechanism": mechanism, "coordinate_chart": chart,
            "exact_ambient_box": json.loads(bounds_raw), "equation_kind": equation_kind,
            "equation_parameter": json.loads(parameter_raw), "sheet_inclusion_rule": inclusion_rule,
            "owner_member_id": owner, "shadow_member_id": shadow, "fresh_component_id": component,
            "primitive_sheet_row_sha256": primitive_sha, "A1_theorem_row_sha256": theorem_row,
            "A1_theorem_ast_sha256": theorem_ast, "C26_owner_root_row_sha256": c26_row,
            "owner_C15_row_sha256": owner15, "shadow_C15_row_sha256": shadow15,
            "owner_C25_row_sha256": owner25, "shadow_C25_row_sha256": shadow25,
            "materialized_shadow_node_id": node_id, "materialized_shadow_node_row_sha256": companion_preordinal["row_sha256"],
            "formal_credit": 0,
        }
        for role in ("OWNER", "SHADOW"):
            is_owner = role == "OWNER"
            roles.append({
                **common, "terminal": "SHEET_OWNER" if is_owner else "SHEET_SHADOW", "role": role,
                "assigned_member_id": owner if is_owner else shadow,
                "open_side_predicate": owner_side if is_owner else shadow_side,
                "equality_sheet_included": is_owner,
                "terminal_disposition": "UNIQUE_HALF_OPEN_SHEET_OWNER" if is_owner else "UNIQUE_ADJACENT_SHADOW_EXCLUDED_FROM_EQUALITY_SHEET",
            })
    roles.sort(key=lambda row: (row["physical_sheet_id"].encode(), row["role"].encode()))
    companions.sort(key=lambda row: row["physical_sheet_id"].encode())
    roles = [{**row, "ordinal": ordinal} for ordinal, row in enumerate(roles)]
    roles = [{**row, "row_sha256": digest(row)} for row in roles]
    companions = [{**{key: value for key, value in row.items() if key != "row_sha256"}, "ordinal": ordinal} for ordinal, row in enumerate(companions)]
    companions = [{**row, "row_sha256": digest(row)} for row in companions]
    need(len(roles) == 35_880 and len(companions) == 17_940, "reference materialization census")
    return roles, companions


def reconstruct_sqlite(seed: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    db, pins = generate_primitive_candidates(seed)
    try:
        rng = random.Random(seed ^ 0xC2717940)
        load_bindings(db, rng)
        validate_post_generation_bindings(db)
        roles, companions = materialize_reference(db)
        projection = [{"physical_sheet_id": row["physical_sheet_id"], "terminal": row["terminal"], "assigned_member_id": row["assigned_member_id"], "fresh_component_id": row["fresh_component_id"], "equality_sheet_included": row["equality_sheet_included"], "materialized_shadow_node_id": row["materialized_shadow_node_id"]} for row in roles]
        reference = {
            "candidate_projection_sha256": digest(projection),
            "role_ordered_row_hashes_sha256": digest([row["row_sha256"] for row in roles]),
            "shadow_ordered_row_hashes_sha256": digest([row["row_sha256"] for row in companions]),
            "primitive_sheet_count": 17_940, "candidate_role_row_count": 35_880,
            "shadow_companion_count": 17_940, "terminal_census": {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940},
            "source_census": {"R204": 224, "R211": 17_716}, "unresolved": 0,
            "input_sha256": pins, "formal_credit": 0,
        }
        return roles, companions, reference
    finally:
        db.close()


def read_gzip_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with gzip.open(path, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), f"candidate newline:{path.name}:{ordinal}")
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) + b"\n" == raw, f"candidate canonical:{path.name}:{ordinal}")
            close_row(row, f"candidate:{path.name}:{ordinal}")
            rows.append(row)
    return rows


def read_candidate(candidate_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    roles = read_gzip_rows(candidate_dir / "sheet_owner_shadow_terminal_ledger.jsonl.gz")
    companions = read_gzip_rows(candidate_dir / "materialized_shadow_companion_ledger.jsonl.gz")
    raw = (candidate_dir / "result.json").read_bytes()
    need(raw.endswith(b"\n"), "candidate result newline")
    result = json.loads(raw)
    need(canonical(result) + b"\n" == raw, "candidate canonical result")
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    need(claimed == digest(body), "candidate result closure")
    return roles, companions, result


def validate_supplied(
    roles: list[dict[str, Any]], companions: list[dict[str, Any]], result: dict[str, Any],
    reference_roles: list[dict[str, Any]], reference_companions: list[dict[str, Any]], reference: dict[str, Any],
    expected_seed: int | None = None,
) -> None:
    result_body = dict(result)
    result_claimed = result_body.pop("result_sha256", None)
    need(result_claimed == digest(result_body), "supplied result closure")
    if expected_seed is not None:
        need(
            result.get("declared_seed") == expected_seed
            and result.get("declared_seed_semantically_used_before_canonical_sort") is True,
            "stream declared seed authority",
        )
        invocation = result.get("invocation", {})
        argv = invocation.get("command_argv", [])
        need(
            invocation.get("isolated_runtime") is True
            and invocation.get("dont_write_bytecode") is True
            and type(argv) is list
            and len(argv) >= 2
            and "--seed" in argv
            and argv[argv.index("--seed") + 1] == str(expected_seed),
            "stream invocation seed authority",
        )
        semantic = dict(result)
        for key in (
            "declared_seed", "declared_seed_semantically_used_before_canonical_sort",
            "invocation", "semantic_projection_sha256", "result_sha256",
        ):
            semantic.pop(key, None)
        need(
            result.get("semantic_projection_sha256") == digest(semantic),
            "stream cross-seed semantic projection commitment",
        )
    need(len(roles) == len(reference_roles) == 35_880, "role candidate count")
    need(len(companions) == len(reference_companions) == 17_940, "shadow candidate count")
    for ordinal, row in enumerate(roles):
        need(row.get("ordinal") == ordinal, "role ordinal")
        close_row(row, "supplied role")
    for ordinal, row in enumerate(companions):
        need(row.get("ordinal") == ordinal, "companion ordinal")
        close_row(row, "supplied companion")
    need([row["physical_sheet_id"] for row in companions] == sorted(row["physical_sheet_id"] for row in companions), "companion canonical order")
    need([(row["physical_sheet_id"], row["role"]) for row in roles] == sorted((row["physical_sheet_id"], row["role"]) for row in roles), "role canonical order")
    need(all(canonical(a) == canonical(b) for a, b in zip(roles, reference_roles)), "cross-implementation exact role rows")
    need(all(canonical(a) == canonical(b) for a, b in zip(companions, reference_companions)), "cross-implementation exact shadow rows")
    projection = [{"physical_sheet_id": row["physical_sheet_id"], "terminal": row["terminal"], "assigned_member_id": row["assigned_member_id"], "fresh_component_id": row["fresh_component_id"], "equality_sheet_included": row["equality_sheet_included"], "materialized_shadow_node_id": row["materialized_shadow_node_id"]} for row in roles]
    need(digest(projection) == reference["candidate_projection_sha256"], "candidate projection commitment")
    need(result["candidate_projection_sha256"] == reference["candidate_projection_sha256"], "stream projection commitment")
    need(result["primitive_candidate_generation"] == {"R204_target_factor_sign_partition": 224, "R211_factor_sign_and_outgoing_chart_partition": 17_716, "total_physical_sheets": 17_940}, "stream primitive generation census")
    need(result["terminal_census"] == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940} and result["candidate_role_row_count"] == 35_880, "stream terminal census")
    need(result["role_ledger"]["ordered_row_hashes_sha256"] == reference["role_ordered_row_hashes_sha256"], "role row-hash commitment")
    need(result["shadow_companion_ledger"]["ordered_row_hashes_sha256"] == reference["shadow_ordered_row_hashes_sha256"], "shadow row-hash commitment")
    need(result["role_ledger"]["sha256"] == file_sha(Path(result.get("_candidate_dir", ".")) / "sheet_owner_shadow_terminal_ledger.jsonl.gz") if "_candidate_dir" in result else True, "role compressed hash")
    need(result["unresolved"] == result["orphan_or_duplicate"] == result["legal_cross_component_witness"] == result["formal_credit"] == 0, "strict zero/unresolved result")
    need(result["half_open_side_inclusion_independently_derived"] is True and result["terminal_physical_totality"] == "PASS_LOCAL_ZERO_CREDIT", "physical totality local gate")
    need(result["C27_source_or_FAMILIES_imported_or_read"] is False and result["edge_ledger_used_as_candidate_universe"] is False, "forbidden authority absent")
    need(result["C27_C28_C29"] == "REJECT_PENDING_ALL_20_TERMINAL_GATE" and result["CM2"] == "NO-GO_FOR_CLAIM", "strict nonpromotion")


def verify(candidate_dir: Path, seed: int) -> dict[str, Any]:
    reference_roles, reference_companions, reference = reconstruct_sqlite(seed)
    roles, companions, result = read_candidate(candidate_dir)
    validate_supplied(
        roles, companions, result, reference_roles, reference_companions,
        reference, seed,
    )
    need(result["input_sha256"] == reference["input_sha256"], "stream/SQLite input pins")
    need(result["role_ledger"]["sha256"] == file_sha(candidate_dir / "sheet_owner_shadow_terminal_ledger.jsonl.gz"), "role compressed file hash")
    need(result["shadow_companion_ledger"]["sha256"] == file_sha(candidate_dir / "materialized_shadow_companion_ledger.jsonl.gz"), "shadow compressed file hash")
    semantic_projection = {
        "schema": "cm2.c27.sheet-owner-shadow-physical-totality.zero-credit.v1.sqlite-independent-verification.v1",
        "status": "PASS_SQLITE_INDEPENDENT_R173_R204_R208_REBUILD__17940_SHEETS_35880_EXACT_ROLE_ROWS__ZERO_CREDIT",
        "primitive_candidates_generated_before_C21_C25_C26_read": True,
        "R204_generated_sheet_count": 224, "R211_generated_sheet_count": 17_716,
        "primitive_sheet_count": 17_940, "role_row_count": 35_880, "shadow_companion_count": 17_940,
        "per_role_row_exact_mismatch_count": 0, "per_shadow_row_exact_mismatch_count": 0,
        "candidate_projection_sha256": reference["candidate_projection_sha256"],
        "role_ordered_row_hashes_sha256": reference["role_ordered_row_hashes_sha256"],
        "shadow_ordered_row_hashes_sha256": reference["shadow_ordered_row_hashes_sha256"],
        "unresolved": 0, "C27_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False, "formal_credit": 0,
        "C27_C28_C29": "REJECT_PENDING_ALL_20_TERMINAL_GATE", "CM2": "NO-GO_FOR_CLAIM",
    }
    body = {
        **semantic_projection,
        "declared_seed": seed,
        "declared_seed_used_for_primitive_and_binding_insertion_order": True,
        "semantic_projection_sha256": digest(semantic_projection),
    }
    return {**body, "verification_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output-tag", required=True)
    arguments = parser.parse_args()
    target = AUDIT / arguments.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    candidate_dir = Path(arguments.candidate_dir).resolve()
    verification = verify(candidate_dir, arguments.seed)
    body = dict(verification)
    body.pop("verification_sha256")
    body["invocation"] = {
        "command_argv": [
            sys.executable, "-I", "-B", str(Path(__file__).resolve()),
            "--candidate-dir", str(candidate_dir),
            "--seed", str(arguments.seed),
            "--output-tag", arguments.output_tag,
        ],
        "isolated_runtime": True,
        "dont_write_bytecode": True,
    }
    verification = {**body, "verification_sha256": digest(body)}
    target.mkdir(mode=0o700)
    (target / "verification.json").write_bytes(canonical(verification) + b"\n")
    print(canonical(verification).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, sqlite3.Error) as error:
        print("REJECT_SHEET_OWNER_SHADOW_PHYSICAL_SQLITE:" + str(error), file=sys.stderr)
        raise SystemExit(2)
