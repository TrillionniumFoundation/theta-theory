#!/usr/bin/env python3
"""C27-independent OUTGOING_GRAPHS physical-totality probe (stream implementation).

The graph-root universe is rebuilt from the pinned C10 graph class and exact
base/equation ASTs.  C24/C26 are consumed only after that universe exists.
No C27 family table or transition edge ledger is read.  This is deliberately
zero-credit until the complete primitive twenty-family gate is closed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
SCHEMA = "cm2.c27.outgoing-graphs-physical-totality-zero-credit.v1"

C10 = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C24A = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
C24B = "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"

PINS = {
    C10: "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C24A: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
    C24B: "788f16cf6c8e67cdd5c1f3bcdb89e6cde00047bda19531a9a42c56339a31e380",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
}

CLASS_TO_TERMINAL = {
    "R242_UNIQUE_GRAPH_FULL_PATCH": "OUTGOING",
    "R235_TARGET_POSITIVE_PARTIAL_BASE": "SINGLE",
    "R235_SOURCE_EXACT_FACE_FULL_BASE": "SINGLE",
    "R235D_SOURCE_EXACT_FACE_FULL_BASE": "DOUBLE",
}
EXPECTED_PARTITION = {"OUTGOING": 264, "SINGLE": 4984, "DOUBLE": 16}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def path_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def checked_relevant(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body), "row closure:" + label)


def rows(name: str) -> Iterable[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for raw_line in stream:
            need(raw_line.endswith(b"\n"), "newline:" + name)
            raw = raw_line[:-1]
            row = json.loads(raw)
            need(isinstance(row, dict), "row object:" + name)
            yield row


def validate_pins() -> None:
    for name, expected in PINS.items():
        need(path_sha(ROOT / name) == expected, "input pin:" + name)


def ast_closure(row: dict[str, Any]) -> None:
    names = ("base_domain_ast", "carrier_domain_ast", "equation_ast", "exact_support_ast")
    for name in names:
        need(row["ast_sha256"][name + "_sha256"] == digest(row[name]), "C10 AST closure:" + name)
    need(row["exact_support_ast"] == {
        "op": "AND",
        "args": [row["carrier_domain_ast"], row["base_domain_ast"], row["equation_ast"]],
    }, "C10 exact-support construction")


def load_c10() -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    partition: Counter[str] = Counter()
    outgoing: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for row in rows(C10):
        checked_relevant(row, "C10")
        graph_id = row.get("graph_id")
        graph_class = row.get("graph_class")
        need(isinstance(graph_id, str) and graph_id not in seen, "C10 unique graph id")
        need(graph_class in CLASS_TO_TERMINAL, "C10 recognized graph class")
        seen.add(graph_id)
        ast_closure(row)
        terminal = CLASS_TO_TERMINAL[graph_class]
        partition[terminal] += 1
        if terminal != "OUTGOING":
            continue
        need(graph_id.startswith("round242-positive-2d-transition-sheet-patch:"), "outgoing graph id authority")
        need(row["coordinate_parameter"] == "TPS", "outgoing coordinate parameter")
        need(row["support_properties"] == {
            "R248_rectangle_used_as_support": False,
            "connected": True,
            "nonempty": True,
            "one_graph_point_per_exact_base_point": True,
            "s_independent_equation": False,
        }, "outgoing support properties")
        certificate = row["monotone_graph_certificate"]
        need(certificate.get("kind") == "SEALED_R242_STRICT_T_MONOTONE_UNIQUE_FULL_PATCH_GRAPH", "outgoing monotone kind")
        need(certificate.get("unique_t_for_every_exact_base_point") is True, "outgoing unique graph point")
        sign_triple = (
            certificate.get("lower_t_face_F_sign"),
            certificate.get("strict_t_derivative_sign"),
            certificate.get("upper_t_face_F_sign"),
        )
        need(sign_triple in {
            ("STRICT_NEGATIVE", "STRICT_POSITIVE", "STRICT_POSITIVE"),
            ("STRICT_POSITIVE", "STRICT_NEGATIVE", "STRICT_NEGATIVE"),
        }, "outgoing monotone orientation")
        outgoing[graph_id] = {
            "graph_id": graph_id,
            "graph_class": graph_class,
            "sheet_member_id": row["sheet_member_id"],
            "c10_row_sha256": row["row_sha256"],
            "ast_sha256": dict(row["ast_sha256"]),
            "geometry_root_sha256": digest({
                "graph_id": graph_id,
                "graph_class": graph_class,
                "base_domain_ast": row["base_domain_ast"],
                "carrier_domain_ast": row["carrier_domain_ast"],
                "equation_ast": row["equation_ast"],
                "exact_support_ast": row["exact_support_ast"],
            }),
        }
    actual = dict(partition)
    need(len(seen) == sum(partition.values()) == 5264, "C10 G1 denominator")
    need(actual == EXPECTED_PARTITION, "C10 actual terminal partition")
    need(len(outgoing) == actual["OUTGOING"], "outgoing root count")
    return outgoing, actual


def load_relations(outgoing: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    selected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows(C24A):
        graph_id = row.get("graph_id")
        if graph_id not in outgoing:
            continue
        checked_relevant(row, "C24A")
        family = row.get("coarse_family")
        need(family in {"G2A", "G2B"}, "C24A outgoing family")
        expected_kind = (
            "G2A_GRAPH_TO_SHEET_MEMBER_AND_REPRESENTATION_SET_EQUALITY"
            if family == "G2A" else
            "G2B_RELATION_BACKED_SIDE_MEMBER_AND_REPRESENTATION_SET_EQUALITY"
        )
        need(row.get("row_kind") == expected_kind, "C24A outgoing row kind")
        need(row["normalized_support_ast_sha256"] == digest(row["normalized_support_ast"]), "C24A support AST closure")
        need(row["semantic_theorem_ast_sha256"] == digest(row["semantic_theorem_ast"]), "C24A theorem AST closure")
        selected[graph_id].append(row)
    negative_hits = 0
    for row in rows(C24B):
        if row.get("graph_id") in outgoing:
            checked_relevant(row, "C24B")
            negative_hits += 1
    need(negative_hits == 0, "outgoing roots absent from negative C24B")
    need(set(selected) == set(outgoing), "C24A outgoing root totality")
    all_members: set[str] = set()
    for graph_id, relation_rows in selected.items():
        census = Counter(row["coarse_family"] for row in relation_rows)
        need(census == {"G2A": 1, "G2B": 2}, "one sheet plus two sides:" + graph_id)
        need(len({row["member_id"] for row in relation_rows}) == 3, "three distinct dispositions:" + graph_id)
        need(len({row["base_root_id"] for row in relation_rows}) == 1, "shared base root:" + graph_id)
        sheet = next(row for row in relation_rows if row["coarse_family"] == "G2A")
        need(sheet["member_id"] == outgoing[graph_id]["sheet_member_id"], "C10/C24A sheet identity:" + graph_id)
        need(sheet["normalized_support_ast_sha256"] == outgoing[graph_id]["ast_sha256"]["base_domain_ast_sha256"], "sheet/base support equality:" + graph_id)
        for row in relation_rows:
            need(row["member_id"] not in all_members, "member belongs to one outgoing root")
            all_members.add(row["member_id"])
    need(len(all_members) == 792, "outgoing disposition member denominator")
    return selected


def load_current_members(member_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    c15: dict[str, dict[str, Any]] = {}
    for row in rows(C15):
        member_id = row.get("registry_member_id")
        if member_id not in member_ids:
            continue
        checked_relevant(row, "C15")
        need(member_id not in c15, "C15 selected unique")
        c15[member_id] = row
    c25: dict[str, dict[str, Any]] = {}
    for row in rows(C25):
        member_id = row.get("member_id")
        if member_id not in member_ids:
            continue
        checked_relevant(row, "C25")
        need(member_id not in c25, "C25 selected unique")
        c25[member_id] = row
    need(set(c15) == member_ids and set(c25) == member_ids, "current C15/C25 selected cover")
    return c15, c25


def load_features(outgoing: dict[str, dict[str, Any]], member_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    g1: dict[str, dict[str, Any]] = {}
    g2: dict[str, dict[str, Any]] = {}
    for row in rows(C26):
        node = row.get("node_id")
        feature_id = row.get("feature_id")
        chosen = (node == "G1" and feature_id in outgoing) or (node in {"G2A", "G2B"} and feature_id in member_ids)
        if not chosen:
            continue
        checked_relevant(row, "C26")
        target = g1 if node == "G1" else g2
        need(feature_id not in target, "C26 selected unique")
        target[feature_id] = row
    need(set(g1) == set(outgoing), "C26 G1 outgoing cover")
    need(set(g2) == member_ids, "C26 G2 outgoing cover")
    return g1, g2


def disposition_body(
    relation: dict[str, Any], c15: dict[str, Any], c25: dict[str, Any], c26: dict[str, Any]
) -> dict[str, Any]:
    member_id = relation["member_id"]
    family = relation["coarse_family"]
    need(c15["registry_member_id"] == c25["member_id"] == member_id, "member join")
    need(c15["fresh_component_id"] == c25["fresh_component_id"], "C15/C25 component join")
    need(c15["base_root_id"] == c25["base_root_id"] == relation["base_root_id"], "base-root join")
    need(c15["official_key_id"] == c25["official_key_id"], "official-key join")
    need(c25["coarse_family"] == family, "C24/C25 family join")
    need(c25["normalized_support_ast_sha256"] == relation["normalized_support_ast_sha256"], "C24/C25 support join")
    need(c25["support_semantic_kind"] == "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY", "C25 relation-backed semantic")
    need(c25["support_semantic_certificate_sha256"] == relation["semantic_theorem_ast_sha256"], "C24/C25 theorem join")
    need(c25["source_bindings"]["support_kernel"] == "C24A", "C25 C24A source kernel")
    need(c25["source_bindings"]["support_kernel_row_sha256"] == relation["row_sha256"], "C25 C24A row binding")
    need(c25["source_bindings"]["C15_member_row_sha256"] == c15["row_sha256"], "C25 C15 row binding")
    expected_kind = "G2A_GRAPH_TO_SHEET_IDENTIFICATION" if family == "G2A" else "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE"
    need(c26["node_id"] == family and c26["obligation_kind"] == expected_kind, "C26 G2 obligation kind")
    need(c26["owner_member_id"] == member_id, "C26 G2 owner")
    need(c26["definition_or_dependency_theorem_ast_sha256"] == relation["semantic_theorem_ast_sha256"], "C26 G2 theorem binding")
    need(c26["source_bindings"]["source_kernel"] == "C24A", "C26 C24A source kernel")
    need(c26["source_bindings"]["source_row_sha256"] == relation["row_sha256"], "C26 C24A row binding")
    return {
        "role": "G2A_SHEET" if family == "G2A" else "G2B_SIDE",
        "member_id": member_id,
        "fresh_component_id": c15["fresh_component_id"],
        "base_root_id": c15["base_root_id"],
        "official_key_id": c15["official_key_id"],
        "normalized_support_ast_sha256": relation["normalized_support_ast_sha256"],
        "semantic_theorem_ast_sha256": relation["semantic_theorem_ast_sha256"],
        "C15_row_sha256": c15["row_sha256"],
        "C24A_row_sha256": relation["row_sha256"],
        "C25_row_sha256": c25["row_sha256"],
        "C26_row_sha256": c26["row_sha256"],
    }


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validate_pins()
    outgoing, partition = load_c10()
    relations = load_relations(outgoing)
    member_ids = {row["member_id"] for values in relations.values() for row in values}
    c15, c25 = load_current_members(member_ids)
    g1, g2 = load_features(outgoing, member_ids)
    output: list[dict[str, Any]] = []
    for graph_id in sorted(outgoing):
        graph = outgoing[graph_id]
        feature = g1[graph_id]
        need(feature["obligation_kind"] == "G1_EXACT_GRAPH_DEFINITION", "C26 G1 obligation")
        need(feature["owner_member_id"] == graph["sheet_member_id"], "C26 G1 owner")
        need(feature["definition_or_dependency_theorem_ast_sha256"] == digest(graph["ast_sha256"]), "C26 G1 AST binding")
        need(feature["source_bindings"]["source_kernel"] == "C10", "C26 C10 source kernel")
        need(feature["source_bindings"]["source_row_sha256"] == graph["c10_row_sha256"], "C26 C10 row binding")
        dispositions = [disposition_body(row, c15[row["member_id"]], c25[row["member_id"]], g2[row["member_id"]]) for row in relations[graph_id]]
        dispositions.sort(key=lambda row: (row["role"], row["member_id"]))
        need(Counter(row["role"] for row in dispositions) == {"G2A_SHEET": 1, "G2B_SIDE": 2}, "disposition roles")
        need(len({row["fresh_component_id"] for row in dispositions}) == 1, "shared current component")
        need(len({row["base_root_id"] for row in dispositions}) == 1, "shared current base root")
        need(len({row["official_key_id"] for row in dispositions}) == 1, "shared current official key")
        body = {
            "schema": SCHEMA + ".candidate-row.v1",
            "terminal": "OUTGOING_GRAPHS",
            "graph_id": graph_id,
            "graph_class": graph["graph_class"],
            "geometry_root_sha256": graph["geometry_root_sha256"],
            "base_domain_ast_sha256": graph["ast_sha256"]["base_domain_ast_sha256"],
            "carrier_domain_ast_sha256": graph["ast_sha256"]["carrier_domain_ast_sha256"],
            "equation_ast_sha256": graph["ast_sha256"]["equation_ast_sha256"],
            "exact_support_ast_sha256": graph["ast_sha256"]["exact_support_ast_sha256"],
            "C10_row_sha256": graph["c10_row_sha256"],
            "C26_G1_row_sha256": feature["row_sha256"],
            "dispositions": dispositions,
            "physical_totality_certificate": {
                "root_generated_before_C24_C26_join": True,
                "exactly_one_G2A_sheet": True,
                "exactly_two_G2B_sides": True,
                "C24B_negative_dispositions": 0,
                "all_G2A_G2B_C26_obligations_joined": True,
                "current_C15_C25_component_base_root_official_key_agree": True,
                "unresolved": 0,
            },
            "formal_credit": 0,
        }
        output.append({**body, "candidate_digest": digest(body)})
    need(len(output) == 264 and len({row["candidate_digest"] for row in output}) == 264, "264 unique output rows")
    body = {
        "schema": SCHEMA + ".result.v1",
        "status": "PASS_ZERO_CREDIT__OUTGOING_GRAPHS_264_ROOTS_264_G2A_528_G2B_PHYSICAL_TOTALITY",
        "implementation_neutral_semantics": "STREAM_OR_SQLITE_MUST_REBUILD_IDENTICAL_CANDIDATE_DIGESTS",
        "candidate_universe": "C10_GRAPH_CLASS_BASE_AST_EQUATION_AST__NOT_C27_FAMILIES_OR_EDGE_LEDGER",
        "C10_actual_G1_partition": partition,
        "outgoing_root_count": len(output),
        "G2A_sheet_disposition_count": sum(row["role"] == "G2A_SHEET" for item in output for row in item["dispositions"]),
        "G2B_side_disposition_count": sum(row["role"] == "G2B_SIDE" for item in output for row in item["dispositions"]),
        "C24B_negative_disposition_count": 0,
        "unresolved_count": 0,
        "duplicate_or_orphan_count": 0,
        "ordered_candidate_digests_sha256": digest([row["candidate_digest"] for row in output]),
        "input_pins": [{"filename": name, "sha256": PINS[name]} for name in sorted(PINS)],
        "C27_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return output, {**body, "result_sha256": digest(body)}


def write_output(target: Path, ledger: list[dict[str, Any]], result: dict[str, Any]) -> None:
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    with gzip.GzipFile(filename="", mode="wb", fileobj=(target / "ledger.jsonl.gz").open("wb"), mtime=0) as stream:
        for row in ledger:
            stream.write(canonical(row) + b"\n")
    (target / "result.json").write_bytes(canonical(result))
    manifest = {
        "ledger.jsonl.gz": path_sha(target / "ledger.jsonl.gz"),
        "result.json": path_sha(target / "result.json"),
    }
    (target / "manifest.json").write_bytes(canonical(manifest))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-tag", required=True)
    parser.add_argument("--seed", required=True)
    args = parser.parse_args()
    need(args.seed.isdigit(), "numeric seed")
    ledger, result = reconstruct()
    write_output(AUDIT / args.output_tag, ledger, result)
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
