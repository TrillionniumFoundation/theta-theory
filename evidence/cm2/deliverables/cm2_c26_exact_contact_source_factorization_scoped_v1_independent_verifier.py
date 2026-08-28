#!/usr/bin/env python3
"""Independent verifier for the scoped C26 source-factorization theorem.

The producer uses a lockstep source stream.  This verifier instead builds a
source-row keyed SQLite relation and joins the C26/output rows by exact hashes.
It does not import the producer or a shared implementation module.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
LEDGER = "c26_691424_scoped_exact_contact_source_factorization.jsonl.gz"
PINS = {
    "C26": ("deliverables/cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz", "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e"),
    "C21A": ("deliverables/cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel_ledger.jsonl.gz", "1c60f2ef752b1b3ab363740cec7505cbddacfbc7509922dab63bbf011e3659f1"),
    "C21C": ("deliverables/cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_ledger.jsonl.gz", "add22270845ef504427475e91696451f2d53c41b4b2cb9af2784a9507ce60c09"),
    "C22A": ("deliverables/cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C22B": ("deliverables/cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_ledger.jsonl.gz", "c0f3d3a9fc6002f0af23271f7483aeff7eac0b0cc92399fc3785b0a5b9291f97"),
    "C10": ("deliverables/cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz", "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    "C24A": ("deliverables/cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz", "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58"),
    "C24B": ("deliverables/cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz", "788f16cf6c8e67cdd5c1f3bcdb89e6cde00047bda19531a9a42c56339a31e380"),
    "C19A": ("deliverables/cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),
    "C19B": ("deliverables/cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),
    "C19C": ("deliverables/cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),
    "C20A": ("deliverables/cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),
    "C23A": ("deliverables/cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "STRICT": ("deliverables/cm2_c27_same_chart_strict_volume_totality_subgate_receipt.json", "22f8f8f6635a6083254311f5ee776e9ebe82b3192b0aadac6dc9585a0b0db3a4"),
    "LOWER": ("deliverables/cm2_c27_same_chart_lower_dimensional_exact_contact_v1_result.json", "67aafe571ebfad6dbc0861f370d9ce8227e2905a660b9be739233afd1e524015"),
    "LOWER_RECEIPT": ("deliverables/cm2_c27_same_chart_lower_dimensional_exact_contact_v1_terminal_receipt.json", "54da91e93d3248f931c9654ec002fc4fb5e43eca59cdefbd5586d727ae008b94"),
    "G2A_RECEIPT": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/receipt.json", "acb9b25d309efbf52026bacbb5208aa2775b4e4c5c98fcca30c7ed7ce42585b5"),
    "G2A_ROUTES": (".cm2-runtime/audit/g2a-relative2d-v2-theorem-bound-seed30635101/G2A_5264_final_unique_routes.jsonl.gz", "b282c78c1289ed21cb4be85b031b62302398870fe462a8f09ef850eaa83c12e5"),
    "G2A_CONTACTS": (".cm2-runtime/audit/g2a-relative2d-v2-theorem-bound-seed30635101/G2A_9408_exact_relative2D_contact_alias_routes.jsonl.gz", "adffbf0f67faf8de7fb586a0879465fdbc9ac00b007698d605b1fe1ccdbdc173"),
    "G2A_COMPLEMENT": (".cm2-runtime/audit/g2a-relative2d-v2-theorem-bound-seed30635101/G2A_552_no_current_contact_complement.jsonl.gz", "fd73328d100f3c5dc7b941611d9a9fc2d2eb2bf866495cd739db25c182370a0a"),
    "UNION_RESULT": (".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/result.json", "25c3f914dd653cf11eaea69532308c55d6bd5a4143ecc338aa55adaec1b36c4b"),
}
NODE_COUNTS = {"A1": 17_940, "A2": 62_152, "G1": 5_264, "G2A": 5_264, "G2B": 10_128, "R1": 295_340, "R2": 295_336}
EXPECTED_DISPOSITIONS = {
    "OWNER_CONTACT_CANDIDATES_EXHAUSTED_BY_STRICT_AND_LOWER_AUTHORITIES__NO_NEW_C26_CONTACT": 80_092,
    "STRICT_DIM3_HANDLED__LOWER_DIM012_EXHAUSTED_WITH_ZERO_LEGAL_WITNESS": 295_340,
    "NO_NEW_ATOM_BEYOND_R1__STRICT_DIM3_HANDLED__LOWER_DIM012_REJECTED": 295_336,
    "SCOPED_G2A_ROUTE_BOUND__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN": 5_264,
    "SCOPED_G2A_UNIQUE_ROUTE_CLOSED__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN": 5_264,
    "EXACT_POSITIVE_PAIR_ASSIGNED_POSITIVE_VOLUME_CARRIERS_IN_SCOPED_COMPARATOR": 9_408,
    "NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT": 552,
    "EXACT_EMPTY_SUPPORT_CANNOT_FORM_CONTACT": 168,
}
EXPECTED_SOURCE_COUNTS = {"C21A": 1_008, "C21C": 79_084, "C22A": 295_340, "C22B": 295_336, "C10": 5_264, "C24A": 15_224, "C24B": 168}


class Failure(RuntimeError):
    pass


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def path_for(tag: str) -> Path:
    path, pin = PINS[tag]
    target = ROOT / path
    need(file_sha(target) == pin, "pin:" + tag)
    return target


def rows_path(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == digest(body), f"closure:{path.name}:{ordinal}")
            yield row


def rows(tag: str) -> Iterator[dict[str, Any]]:
    yield from rows_path(path_for(tag))


def result_document(candidate: Path) -> dict[str, Any]:
    raw = (candidate / "result.json").read_bytes()
    value = json.loads(raw)
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(claimed == digest(body), "result closure")
    return value


def front_gate(candidate: Path) -> tuple[dict[str, Any], str]:
    result = result_document(candidate)
    need(result["schema"] == "cm2.c26-independent.exact-contact-source-factorization-scoped-theorem.v1", "schema")
    need(result["status"].startswith("PASS_NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS__691424_SOURCE_FACTORIZED"), "status")
    census = result["census"]
    need(census["C26_feature_rows"] == 691_424 and census["C26_direct_support_carrier_rows"] == 0 and census["C26_source_factorized_rows"] == 691_424 and census["scoped_unresolved_rows"] == 0, "headline census")
    need(census["node_census"] == NODE_COUNTS and census["disposition_census"] == EXPECTED_DISPOSITIONS, "node/disposition census")
    need(census["source_kernel_census"] == EXPECTED_SOURCE_COUNTS, "source-kernel census")
    need(census["six_kernel_primitive_atoms"] == 483_232 and census["six_kernel_primitive_owners"] == 482_380, "primitive census")
    need(census["C26_rows_on_six_kernel_primitive_owners"] == 670_768 and census["C26_graph_rows_outside_six_kernel_owner_ids"] == 20_656, "owner row partition")
    need(census["unique_six_kernel_primitive_owners_with_C26_feature_rows"] == 313_276 and census["six_kernel_owners_without_C26_feature_rows"] == 169_104, "owner coverage")
    need(census["R2_C22A_atom_factor_histogram"] == {"1": 295_332, "2": 4}, "R2 factor histogram")
    need(census["same_chart_strict_dim3_pairs"] == 187_132 and census["same_chart_lower_dim012_pairs"] == 5_783_708 and census["same_chart_lower_legal_cross_component_witnesses"] == 0, "same chart authority census")
    need(census["G2A_scoped_graph_routes"] == 5_264 and census["C24A_G2B_positive_priority_pairs"] == 9_408 and census["C24A_G2B_no_current_contact_members"] == 552 and census["C24B_exact_empty_members"] == 168, "graph census")
    need(census["graph_feature_row_disjoint_bucket_census"] == {"G1_C10_definition_handoff_by_graph_id": 5_264, "G2A_C24A_scoped_route": 5_264, "G2B_C24A_positive": 9_408, "G2B_C24A_complement": 552, "G2B_C24B_exact_empty": 168}, "graph disjoint buckets")
    need(census["graph_feature_rows_total"] == 20_656 and census["graph_geometry_double_count_created_by_G1_G2A_feature_dependency"] == 0, "graph no double count")
    need(census["same_chart_contact_owners_with_C26_feature_rows"] == 313_276 and census["same_chart_contact_owners_without_C26_feature_rows"] == 168_832, "contact owner coverage")
    governance = result["candidate_governance"]
    need(governance == {
        "C27_FAMILIES_or_transition_imported_or_read": False, "C28_imported_or_read": False, "C29_imported_or_read": False,
        "historical_edge_ledger_used_as_candidate_universe": False, "old_transition_or_pair_ledger_used_as_candidate_universe": False,
        "six_primitive_support_kernels_are_candidate_denominator": True, "C26_absence_used_as_negative_geometry_theorem": False,
    }, "candidate governance")
    scope = result["theorem_scope"]
    need(scope["global_three_terminal_totality_and_unique_assignment"] is False and scope["global_atom_to_pair_incidence_join"] == "OPEN_NOT_CLAIMED_BY_THIS_THEOREM" and scope["G2A_global_positive_C19_extension"] == "OPEN", "fail closed scope")
    need(len(result["open_blockers"]) == 5 and result["formal_credit"] == 0 and result["manifest_authorized"] is False and result["source_W_transition_authorized"] is False, "zero credit")
    conclusion = result["conclusion"]
    need(conclusion["NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS"] is True and conclusion["G1_and_G2A_feature_rows_are_disjoint_DAG_rows_but_not_two_geometry_candidates"] is True, "scoped conclusion")
    need(conclusion["fills_v5_C26_absence_slot"].startswith("YES__") and conclusion["does_not_close_twenty_family_gate"].startswith("PRIMITIVE_SOURCE_GLOBAL_TERMINAL_ASSIGNMENT"), "v5/nonclosure boundary")
    need(result["strict_nonpromotion"] == {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "strict nonpromotion")
    need(result["semantic_projection_sha256"] == digest(census), "semantic projection")
    ledger_path = candidate / LEDGER
    observed = file_sha(ledger_path)
    meta = census["ledger"]
    need(meta["filename"] == LEDGER and meta["row_count"] == 691_424 and meta["file_sha256"] == observed, "ledger metadata")
    return result, observed


def build_primitive_owners() -> tuple[dict[str, set[str]], dict[str, tuple[str, str, str]]]:
    owner_sources: dict[str, set[str]] = defaultdict(set)
    c22a: dict[str, tuple[str, str, str]] = {}
    counts = {"C19A": 5_596, "C19B": 12_232, "C19C": 33_344, "C20A": 126_468, "C22A": 295_340, "C23A": 10_252}
    for tag in ("C23A", "C22A", "C20A", "C19C", "C19B", "C19A"):
        n = 0
        for row in rows(tag):
            n += 1
            owner = row.get("member_id") or row["owner_member_id"]
            owner_sources[owner].add(tag)
            if tag == "C22A":
                c22a[row["row_sha256"]] = (row["predicate_cell_row_id"], owner, row["support_ast_sha256"])
        need(n == counts[tag], "primitive count:" + tag)
    need(len(owner_sources) == 482_380 and len(c22a) == 295_340, "primitive owners")
    return owner_sources, c22a


def insert_sources(db: sqlite3.Connection, c22a: dict[str, tuple[str, str, str]]) -> None:
    db.execute("CREATE TABLE source (sha TEXT PRIMARY KEY, kernel TEXT, node TEXT, obligation TEXT, feature TEXT, owner TEXT, theorem TEXT, factor_count INTEGER, graph_id TEXT)")
    statement = "INSERT INTO source VALUES (?,?,?,?,?,?,?,?,?)"
    def add(values: tuple[Any, ...]) -> None:
        db.execute(statement, values)
    # Deliberately different keyed-build order from the producer.
    for row in rows("C24B"):
        add((row["row_sha256"], "C24B", "G2B", "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE", row["member_id"], row["member_id"], row["semantic_theorem_ast_sha256"], 0, row["graph_id"]))
    for row in rows("C24A"):
        node = row["coarse_family"]
        obligation = "G2A_GRAPH_TO_SHEET_IDENTIFICATION" if node == "G2A" else "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE"
        add((row["row_sha256"], "C24A", node, obligation, row["member_id"], row["member_id"], row["semantic_theorem_ast_sha256"], 0, row["graph_id"]))
    for row in rows("C10"):
        add((row["row_sha256"], "C10", "G1", "G1_EXACT_GRAPH_DEFINITION", row["graph_id"], row["sheet_member_id"], digest(row["ast_sha256"]), 0, row["graph_id"]))
    for row in rows("C22B"):
        if row["row_kind"] != "R2_PRIMARY_MEMBER_NORMALIZED_SUPPORT_AND_REPRESENTATION_SET_EQUALITY":
            continue
        factors = row["member_union_theorem_ast"]["predicate_cell_equalities"]
        need(len(factors) in {1, 2}, "R2 factor count")
        for factor in factors:
            need(c22a[factor["C22a_row_sha256"]] == (factor["predicate_cell_row_id"], row["member_id"], factor["support_ast_sha256"]), "R2 independent atom join")
        add((row["row_sha256"], "C22B", "R2", "R2_MEMBER_FULL_SUPPORT_UNION", row["member_id"], row["member_id"], row["member_union_theorem_ast_sha256"], len(factors), None))
    for row in rows("C22A"):
        add((row["row_sha256"], "C22A", "R1", "R1_SOURCE_FREE_PREDICATE_CELL_DEFINITION", row["predicate_cell_row_id"], row["owner_member_id"], row["theorem_ast_sha256"], 1, None))
    for row in rows("C21C"):
        node = row["obligation_kind"].split("_", 1)[0]
        add((row["row_sha256"], "C21C", node, row["obligation_kind"], row["feature_row_id"], row["owner_member_id"], row["theorem_ast_sha256"], 0, None))
    for row in rows("C21A"):
        node = row["obligation_kind"].split("_", 1)[0]
        add((row["row_sha256"], "C21A", node, row["obligation_kind"], row["feature_row_id"], row["owner_member_id"], row["feature_theorem_ast_sha256"], 0, None))
    db.commit()
    need(db.execute("SELECT COUNT(*) FROM source").fetchone()[0] == 691_424, "source DB count")


def graph_authority() -> tuple[dict[str, str], set[str], set[str]]:
    receipt = json.loads(path_for("G2A_RECEIPT").read_bytes())
    need(receipt["headline"]["G2A_graphs"] == 5_264 and receipt["formal_credit"] == 0, "G2A receipt")
    routes: dict[str, str] = {}
    for row in rows("G2A_ROUTES"):
        routes[row["graph_id"]] = row["g2a_member_id"]
    positive = {row["positive_side_member_id"] for row in rows("G2A_CONTACTS")}
    complement = {row["one_sided_member_id"] for row in rows("G2A_COMPLEMENT")}
    union = json.loads(path_for("UNION_RESULT").read_bytes())
    need(union["C24A_G2A_G2B_key_by_key"]["G2B_exact_positive_equals_G2B_priority"] is True, "union priority")
    need(len(routes) == 5_264 and len(positive) == 9_408 and len(complement) == 552 and not positive & complement, "graph authority sets")
    return routes, positive, complement


def expected_class(node: str, kernel: str, owner: str, graph: str | None, routes: dict[str, str], positive: set[str], complement: set[str]) -> tuple[str, str]:
    if node in {"A1", "A2"}:
        return "FEATURE_THEOREM_ON_SIX_KERNEL_PRIMITIVE_OWNER__NO_C26_SUPPORT_CARRIER", "OWNER_CONTACT_CANDIDATES_EXHAUSTED_BY_STRICT_AND_LOWER_AUTHORITIES__NO_NEW_C26_CONTACT"
    if node == "R1":
        return "DIRECT_C22A_PRIMITIVE_ATOM_DEFINITION", "STRICT_DIM3_HANDLED__LOWER_DIM012_EXHAUSTED_WITH_ZERO_LEGAL_WITNESS"
    if node == "R2":
        return "C22B_MEMBER_UNION_FACTORS_EXACTLY_TO_C22A_PRIMITIVE_ATOMS", "NO_NEW_ATOM_BEYOND_R1__STRICT_DIM3_HANDLED__LOWER_DIM012_REJECTED"
    if node == "G1":
        need(graph in routes, "G1 graph-id route handoff")
        return "C10_EXACT_GRAPH_DEFINITION_HANDOFF_BY_GRAPH_ID_TO_G2A__NO_SECOND_GEOMETRY_CANDIDATE", "SCOPED_G2A_ROUTE_BOUND__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN"
    if node == "G2A":
        need(graph in routes and routes[graph] == owner, "G2A route")
        return "C24A_GRAPH_TO_SHEET_ALIAS", "SCOPED_G2A_UNIQUE_ROUTE_CLOSED__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN"
    need(node == "G2B", "known node")
    if kernel == "C24B":
        return "C24B_EXACT_EMPTY_SUPPORT", "EXACT_EMPTY_SUPPORT_CANNOT_FORM_CONTACT"
    if owner in positive:
        return "C24A_RELATION_BACKED_PHYSICAL_SIDE", "EXACT_POSITIVE_PAIR_ASSIGNED_POSITIVE_VOLUME_CARRIERS_IN_SCOPED_COMPARATOR"
    need(owner in complement, "G2B partition")
    return "C24A_RELATION_BACKED_ONE_SIDED_COMPLEMENT", "NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT"


def full_verify(candidate: Path, verification_dir: Path, seed: int) -> dict[str, Any]:
    result, ledger_sha = front_gate(candidate)
    strict = json.loads(path_for("STRICT").read_bytes())
    lower = json.loads(path_for("LOWER").read_bytes())
    lower_receipt = json.loads(path_for("LOWER_RECEIPT").read_bytes())
    need(strict["exact_census"]["all_component_strict_intersection_pair_count"] == 187_132, "strict boundary")
    need(lower["census"]["legal_cross_component_lower_dimensional_witness_count"] == 0 and lower["authority_joins"]["C26_absence_used_as_negative_geometry_theorem"] is False, "lower boundary")
    need(lower_receipt["formal_credit"] == 0 and lower_receipt["source_W_transition_authorized"] is False, "lower receipt")
    owners, c22a = build_primitive_owners()
    verification_dir.mkdir(parents=True, exist_ok=True)
    db_path = verification_dir / "independent_source_join.sqlite"
    need(not db_path.exists(), "new sqlite")
    db = sqlite3.connect(db_path)
    try:
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("PRAGMA temp_store=MEMORY")
        insert_sources(db, c22a)
        routes, positive, complement = graph_authority()
        c26_iter = rows("C26")
        out_iter = rows_path(candidate / LEDGER)
        nodes: Counter[str] = Counter()
        dispositions: Counter[str] = Counter()
        covered: set[str] = set()
        for ordinal in range(691_424):
            c26 = next(c26_iter)
            out = next(out_iter)
            need(c26["feature_ordinal"] == ordinal and out["feature_ordinal"] == ordinal and out["C26_row_sha256"] == c26["row_sha256"], "ordinal/C26 join")
            source_sha = c26["source_bindings"]["source_row_sha256"]
            source = db.execute("SELECT kernel,node,obligation,feature,owner,theorem,factor_count,graph_id FROM source WHERE sha=?", (source_sha,)).fetchone()
            need(source is not None, "source hash exists")
            kernel, node, obligation, feature, owner, theorem, factor_count, graph = source
            need((c26["source_bindings"]["source_kernel"], c26["node_id"], c26["obligation_kind"], c26["feature_id"], c26["owner_member_id"], c26["definition_or_dependency_theorem_ast_sha256"]) == (kernel, node, obligation, feature, owner, theorem), "keyed source tuple")
            primitive = owner in owners
            need(primitive == (node in {"A1", "A2", "R1", "R2"}), "owner partition")
            primitive_sources = sorted(owners[owner]) if primitive else []
            factor_class, disposition = expected_class(node, kernel, owner, graph, routes, positive, complement)
            need(out["node_id"] == node and out["source_kernel"] == kernel and out["source_row_sha256"] == source_sha and out["feature_id"] == feature and out["owner_member_id"] == owner, "output identity")
            need(out["primitive_owner_source_kernels"] == primitive_sources and out["source_atom_factor_count"] == factor_count, "output source factor")
            need(out["source_factor_class"] == factor_class and out["scoped_exact_contact_disposition"] == disposition, "output disposition")
            need(out["C26_row_direct_support_carrier"] is False and out["C26_absence_used_as_negative_geometry_theorem"] is False and out["scoped_unresolved"] is False and out["global_three_terminal_assignment_claimed"] is False and out["formal_credit"] == 0, "row fail closed")
            nodes[node] += 1
            dispositions[disposition] += 1
            if primitive:
                covered.add(owner)
        try:
            next(c26_iter)
            raise Failure("extra C26 row")
        except StopIteration:
            pass
        try:
            next(out_iter)
            raise Failure("extra output row")
        except StopIteration:
            pass
        need(dict(nodes) == NODE_COUNTS and dict(dispositions) == EXPECTED_DISPOSITIONS and len(covered) == 313_276, "independent census")
    finally:
        db.close()

    body = {
        "schema": "cm2.c26-independent.exact-contact-source-factorization-independent-verification.v1",
        "status": "PASS_INDEPENDENT_KEYED_SOURCE_HASH_JOIN__691424_ROWS__ZERO_DIRECT_C26_CARRIERS__GLOBAL_TOTALITY_OPEN__ZERO_CREDIT",
        "execution_seed": seed,
        "independent_implementation": {"imports_producer_or_shared_module": False, "algorithm": "SQLITE_SOURCE_ROW_SHA256_RELATION_PLUS_INDEPENDENT_NODE_DISPOSITION_RECONSTRUCTION"},
        "candidate_result_sha256": result["result_sha256"],
        "candidate_ledger_sha256": ledger_sha,
        "census": {"verified_rows": 691_424, "node_census": dict(nodes), "disposition_census": dict(dispositions), "unique_primitive_owners_with_C26_rows": len(covered), "scoped_unresolved": 0},
        "semantic_projection_sha256": digest({"verified_rows": 691_424, "node_census": dict(nodes), "disposition_census": dict(dispositions), "unique_primitive_owners_with_C26_rows": len(covered), "scoped_unresolved": 0}),
        "C27_FAMILIES_or_transition_imported_or_read": False,
        "historical_edge_ledger_used_as_candidate_universe": False,
        "global_three_terminal_totality_and_unique_assignment": False,
        "formal_credit": 0,
        "strict_nonpromotion": {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
    }
    verification = dict(body)
    verification["result_sha256"] = digest(body)
    with (verification_dir / "verification.json").open("xb") as stream:
        stream.write(canonical(verification) + b"\n")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--verification-dir")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--front-gate-only", action="store_true")
    args = parser.parse_args()
    candidate = Path(args.candidate_dir).resolve()
    if args.front_gate_only:
        result, ledger_sha = front_gate(candidate)
        print(canonical({"status": "PASS_FRONT_GATE", "result_sha256": result["result_sha256"], "ledger_sha256": ledger_sha}).decode())
        return 0
    need(args.verification_dir is not None, "verification dir required")
    result = full_verify(candidate, Path(args.verification_dir).resolve(), args.seed)
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"], "semantic_projection_sha256": result["semantic_projection_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
