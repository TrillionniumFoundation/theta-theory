#!/usr/bin/env python3
"""Independent exact solver for the 192 cross-chart graph/side t=0 pairs.

The candidate universe is rebuilt from R236/R248, not from C27 or an edge
ledger.  Current membership/support bindings are checked through C15/C24A/
C25.  The physical decision is rebuilt from the primitive atlas AST and the
R272 exact source-factor contract.  This file does not import or read the
first DOUBLE_GRAPHS probe.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
R236 = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C24A = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
R272 = "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json"
PRIMITIVE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
PINS = {
    R236: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R248: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C24A: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    R272: "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    PRIMITIVE: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(name: str) -> str:
    h = hashlib.sha256()
    with (ROOT / name).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def path_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def wrapped(name: str) -> dict[str, Any]:
    obj = json.loads((ROOT / name).read_bytes())
    result = obj["result"]
    need(obj["result_sha256"] == digest(result), "wrapper closure:" + name)
    return result


def rows(name: str):
    with gzip.open(ROOT / name, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def validate_primitive() -> None:
    tree = ast.parse((ROOT / PRIMITIVE).read_text(encoding="utf-8"), filename=PRIMITIVE)
    geometry = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "geometry")
    branches: dict[str, str] = {}
    for node in ast.walk(geometry):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        if ast.unparse(node.test.left) != "cell" or len(node.test.comparators) != 1:
            continue
        comparator = node.test.comparators[0]
        if not isinstance(comparator, ast.Constant) or comparator.value not in {"E", "W", "N", "S"}:
            continue
        assignment = next(
            item for item in node.body
            if isinstance(item, ast.Assign) and ast.unparse(item.targets[0]) == "(nx, ny)"
        )
        branches[str(comparator.value)] = ast.unparse(assignment.value)
    need(branches == {
        "E": "(radical_n, t)", "W": "(-radical_n, t)",
        "N": "(t, radical_n)", "S": "(t, -radical_n)",
    }, "primitive normal AST")
    returns = [node for node in ast.walk(geometry) if isinstance(node, ast.Return)]
    need(len(returns) == 1 and ast.unparse(returns[0].value) ==
         "(cx + radius * nx, cy + radius * ny, ux, uy, s, radical_p)",
         "primitive phase return AST")


def t0_normal(chart: str) -> tuple[Fraction, Fraction]:
    need(chart.startswith("G:"), "source-G chart")
    return {
        "E": (Fraction(1), Fraction(0)),
        "W": (Fraction(-1), Fraction(0)),
        "N": (Fraction(0), Fraction(1)),
        "S": (Fraction(0), Fraction(-1)),
    }[chart.split(":", 1)[1]]


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    need(all(file_sha(name) == expected for name, expected in PINS.items()), "all pinned inputs")
    validate_primitive()
    r272 = wrapped(R272)
    scope = r272["scope_contract"]
    need(
        scope["source_factor_is_exactly_chart_dependent_plus_or_minus_9_over_25_times_t"] is True
        and scope["source_factor_zero_is_confined_to_one_excluded_t0_face_on_every_leaf"] is True,
        "R272 exact t0 source-factor contract",
    )
    r236 = wrapped(R236)
    partitions = {row["double_endpoint_partition_row_id"]: row for row in r236["double_endpoint_partition_rows"]}
    need(len(partitions) == 16, "16 double partitions")
    # R234 frontier chart is already materialized in each partition signature.
    charts = {pid: row["same_sign_event_absent_signature"]["source_chart"] for pid, row in partitions.items()}
    r248 = wrapped(R248)
    sheet_rows = r248["formal_wall_half_open_sheet_owner_ledger"]["rows"]
    bulk_rows = r248["formal_wall_positive_volume_bulk_ledger"]["rows"]
    sheets = [row for row in sheet_rows if row["source_partition_row_id"] in partitions and row["endpoint_factor"] == "source"]
    sides = [row for row in bulk_rows if row["source_partition_row_id"] in partitions and row["branch_label"] == "SAME_SIGN_EVENT_ABSENT"]
    need(len(sheets) == len(sides) == 16, "16 source sheets and 16 present sides")
    for row in sheets + sides:
        row["chart"] = charts[row["source_partition_row_id"]]
    need(Counter(row["chart"] for row in sheets) == Counter(row["chart"] for row in sides) ==
         {"G:E": 4, "G:W": 4, "G:N": 4, "G:S": 4}, "four per chart")
    selected = {row["wall_sheet_node_id"] for row in sheets} | {row["wall_bulk_node_id"] for row in sides}
    c15: dict[str, dict[str, Any]] = {}
    for row in rows(C15):
        if row["registry_member_id"] in selected:
            c15[row["registry_member_id"]] = row
    need(set(c15) == selected, "C15 complete selected cover")
    c24: dict[str, dict[str, Any]] = {}
    for row in rows(C24A):
        if row["member_id"] in selected:
            c24[row["member_id"]] = row
    need(set(c24) == selected, "C24A complete selected support cover")
    c25: dict[str, dict[str, Any]] = {}
    for row in rows(C25):
        if row["member_id"] in selected:
            c25[row["member_id"]] = row
    need(set(c25) == selected, "C25 complete selected typed cover")
    for member in selected:
        need(c25[member]["fresh_component_id"] == c15[member]["fresh_component_id"], "C15/C25 component join")
        need(c25[member]["normalized_support_ast_sha256"] == c24[member]["normalized_support_ast_sha256"], "C24A/C25 support join")

    output: list[dict[str, Any]] = []
    radius = Fraction(9, 25)
    for sheet in sorted(sheets, key=canonical):
        sid = sheet["wall_sheet_node_id"]
        for side in sorted(sides, key=canonical):
            if sheet["chart"] == side["chart"]:
                continue
            tid = side["wall_bulk_node_id"]
            sn, tn = t0_normal(sheet["chart"]), t0_normal(side["chart"])
            need(sn != tn, "cross-chart cardinal normal mismatch")
            sq, tq = tuple(radius*x for x in sn), tuple(radius*x for x in tn)
            need(sq != tq, "cross-chart source-G position mismatch")
            body = {
                "sheet_member_id": sid,
                "side_member_id": tid,
                "sheet_chart": sheet["chart"],
                "side_chart": side["chart"],
                "sheet_component_id": c15[sid]["fresh_component_id"],
                "side_component_id": c15[tid]["fresh_component_id"],
                "sheet_t": "0", "side_closure_t": "0",
                "sheet_normal": [str(x) for x in sn], "side_normal": [str(x) for x in tn],
                "sheet_position": [str(x) for x in sq], "side_position": [str(x) for x in tq],
                "route": "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH",
                "formal_credit": 0,
            }
            output.append({**body, "row_sha256": digest(body)})
    output.sort(key=canonical)
    need(len(output) == 192 and len({row["row_sha256"] for row in output}) == 192, "exact 192-row universe")
    body = {
        "status": "PASS_ZERO_CREDIT__INDEPENDENT_192_GRAPH_SIDE_T0_PHASE_EQUATIONS_EMPTY",
        "candidate_universe": "R236_R248_COMPLETE_16_SOURCE_SHEETS_X_16_PRESENT_SIDES_CROSS_CHART_ONLY",
        "C27_or_first_probe_imported_or_read": False,
        "edge_ledger_used": False,
        "candidate_count": 192,
        "unresolved_count": 0,
        "cross_component_witness_count": 0,
        "rows_sha256": digest(output),
        "formal_credit": 0,
        "unconditional_C27_C28_C29": "REJECT_REMAINS_PENDING_FULL_20_FAMILY_GATE",
    }
    return output, {**body, "result_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-tag", required=True)
    parser.add_argument("--seed", required=True)
    args = parser.parse_args()
    need(args.seed.isdigit(), "numeric seed")
    target = AUDIT / args.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    ledger, result = reconstruct()
    target.mkdir(mode=0o700)
    ledger_bytes = b"".join(canonical(row) + b"\n" for row in ledger)
    with gzip.GzipFile(filename="", mode="wb", fileobj=(target / "ledger.jsonl.gz").open("wb"), mtime=0) as stream:
        stream.write(ledger_bytes)
    (target / "result.json").write_bytes(canonical(result))
    manifest = {
        "ledger_sha256": path_sha(target / "ledger.jsonl.gz"),
        "result_sha256": path_sha(target / "result.json"),
    }
    (target / "manifest.json").write_bytes(canonical(manifest))
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
