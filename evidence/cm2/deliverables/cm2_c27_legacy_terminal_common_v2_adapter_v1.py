#!/usr/bin/env python3
"""Adapt six native legacy authorities to the corrected actual-v5 v2 wire."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / ".cm2-runtime/audit/c27-legacy-terminal-typed-ownership-v1-seed-30650101"
SOURCE_RESULT = SOURCE_DIR / "result.json"
SOURCE_CANDIDATES = SOURCE_DIR / "typed_candidate_ownership.jsonl.gz"
SOURCE_INCIDENCES = SOURCE_DIR / "proof_incidence.jsonl.gz"
SOURCE_ALIASES = SOURCE_DIR / "representation_alias_auxiliary_crosswalk.jsonl.gz"
SOURCE_VERIFY = SOURCE_DIR / "independent_verification_seed30651701.json"
INTERFACE = ROOT / ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json"

PINS = {
    SOURCE_RESULT: "743eb648f62858508d38cec5cc533a3e3ceeb3e0852b642a82dba65377655542",
    SOURCE_CANDIDATES: "0eb6f69029f8fa005b105867641027c8a70b41d0fd72c9fe271b367b64c31887",
    SOURCE_INCIDENCES: "89198283305ea41885c8aa7c36faaf410a3bd92b536f8e8f46cd87b488cad4db",
    SOURCE_ALIASES: "27e2d297025970e7d99200577151e104037aff6e1326b091e05c7281ae37be16",
    SOURCE_VERIFY: "7efea3814968b13cba70a86a53fa4c8e4f649806c289e0a12c88f78d9634fe9c",
    INTERFACE: "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
}

TERMINALS = {
    "RETAINED_CONTINUATION": (1, "T01_RETAINED_CONTINUATION", "REPRESENTATION_CANDIDATE",
                               "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"),
    "OUTGOING_GRAPHS": (2, "T02_OUTGOING_GRAPHS", "GRAPH_ROOT_CANDIDATE",
                        "SAME_FROZEN_C15_COMPONENT__NO_EDGE"),
    "SINGLE_GRAPHS": (3, "T03_SINGLE_GRAPHS", "GRAPH_ROOT_CANDIDATE",
                      "PER_CANDIDATE_SINGLE_GRAPH_COMPONENT_RELATION"),
    "SHEET_OWNER": (5, "T05_SHEET_OWNER", "PHYSICAL_SHEET_ROLE_CANDIDATE",
                    "SAME_FROZEN_C15_COMPONENT__NO_EDGE"),
    "SHEET_SHADOW": (6, "T06_SHEET_SHADOW", "PHYSICAL_SHEET_ROLE_CANDIDATE",
                     "SAME_FROZEN_C15_COMPONENT__NO_EDGE"),
    "INCLUDED_STRATUM_ATTACHMENTS": (10, "T10_INCLUDED_STRATUM_ATTACHMENTS",
                                     "REPRESENTATION_CANDIDATE",
                                     "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"),
}
EXPECTED = {
    "RETAINED_CONTINUATION": 276,
    "OUTGOING_GRAPHS": 264,
    "SINGLE_GRAPHS": 4_984,
    "SHEET_OWNER": 17_940,
    "SHEET_SHADOW": 17_940,
    "INCLUDED_STRATUM_ATTACHMENTS": 10_660,
}
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
EMPTY_SEQUENCE_SHA256 = hashlib.sha256(b"").hexdigest()


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(8 << 20):
            state.update(block)
    return state.hexdigest()


def closed(row: dict[str, Any], key: str, label: str) -> None:
    claim = row.get(key)
    body = dict(row); body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line in handle:
            yield json.loads(line)


def sequence_sha(row_shas: list[str]) -> str:
    state = hashlib.sha256()
    for value in row_shas:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                zipped.write(encode(row) + b"\n")


def descriptor(path: Path, rows: list[dict[str, Any]], schema: str,
               unique_key: str, ordering: list[str]) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(path.parents[1])),
        "row_schema": schema,
        "row_count": len(rows),
        "file_size": path.stat().st_size,
        "file_sha256": file_hash(path),
        "row_sequence_sha256": sequence_sha([row["row_sha256"] for row in rows]),
        "unique_key": unique_key,
        "ordering": ordering,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        for path, expected in PINS.items():
            need(path.is_file() and not path.is_symlink() and file_hash(path) == expected,
                 "input pin:" + path.name)
        interface = json.loads(INTERFACE.read_bytes())["corrected_interface"]
        need(interface["candidate_ownership_ledger"]["row_schema"] == CANDIDATE_SCHEMA
             and interface["materialized_physical_proof_join_ledger"]["row_schema"] == PROOF_SCHEMA,
             "corrected v2 interface")
        verification = json.loads(SOURCE_VERIFY.read_bytes())
        closed(verification, "verification_sha256", "native verification")
        need(verification["producer_imported_or_executed"] is False
             and verification["candidate_total"] == 52_064
             and verification["proof_incidence_total"] == 62_160
             and verification["formal_credit"] == 0
             and verification["source_W_transition_authorized"] is False,
             "native verification semantics")

        source_candidates: dict[str, dict[str, Any]] = {}
        by_terminal: dict[str, list[dict[str, Any]]] = {terminal: [] for terminal in TERMINALS}
        for ordinal, row in enumerate(jsonl(SOURCE_CANDIDATES)):
            closed(row, "row_sha256", f"native candidate:{ordinal}")
            need(row["ordinal"] == ordinal and row["terminal"] in TERMINALS,
                 f"native candidate:{ordinal}:wire")
            need(row["candidate_id"] not in source_candidates, "native candidate unique")
            source_candidates[row["candidate_id"]] = row
            by_terminal[row["terminal"]].append(row)
        source_incidences: dict[str, list[dict[str, Any]]] = {key: [] for key in source_candidates}
        for ordinal, row in enumerate(jsonl(SOURCE_INCIDENCES)):
            closed(row, "row_sha256", f"native incidence:{ordinal}")
            need(row["ordinal"] == ordinal and row["candidate_id"] in source_incidences,
                 f"native incidence:{ordinal}:wire")
            source_incidences[row["candidate_id"]].append(row)
        need({terminal: len(rows) for terminal, rows in by_terminal.items()} == EXPECTED,
             "native candidate census")

        # Incidence rows are semantic/provenance evidence.  They become a
        # materialized physical proof only if they expose a cross-component
        # ordered C15 member pair.  These six authorities expose none.
        for candidate_id, source in source_candidates.items():
            evidence_rows = source_incidences[candidate_id]
            need(len(evidence_rows) == source["proof_incidence_count"],
                 "native incidence cardinality")
            terminal = source["terminal"]
            if terminal == "OUTGOING_GRAPHS":
                components = {row["evidence"]["fresh_component_id"] for row in evidence_rows}
                need(len(components) == 1, terminal + ":same frozen component")
            elif terminal == "SINGLE_GRAPHS":
                components = {row["evidence"]["fresh_component_id"] for row in evidence_rows}
                g2a = [row["evidence"] for row in evidence_rows
                       if row["evidence"]["role"] == "G2A_SHEET"]
                positive = [row["evidence"] for row in evidence_rows
                            if row["evidence"]["role"] == "G2B_POSITIVE_SIDE"]
                need(len(g2a) == 1 and len(components) in {1, 2}
                     and len(positive) in {1, 2},
                     terminal + ":positive-incidence/exact-empty partition")
            elif terminal in {"SHEET_OWNER", "SHEET_SHADOW"}:
                need(len(evidence_rows) == 1
                     and type(evidence_rows[0]["evidence"]["fresh_component_id"]) is str,
                     terminal + ":bound frozen component")
            else:
                need(terminal in {"RETAINED_CONTINUATION", "INCLUDED_STRATUM_ATTACHMENTS"},
                     terminal + ":no-edge semantics")

        output = Path(args.output_dir).resolve()
        need(not output.exists(), "fresh output")
        output.mkdir(parents=True)
        entries = []
        total = 0
        relation_census: dict[str, int] = {}
        for terminal, (terminal_ordinal, slot, kind, relation) in sorted(
                TERMINALS.items(), key=lambda item: item[1][0]):
            candidate_rows = []
            proof_rows: list[dict[str, Any]] = []
            for ordinal, source in enumerate(sorted(by_terminal[terminal],
                                                     key=lambda row: row["candidate_id"])):
                candidate_relation = relation
                candidate_proofs: list[dict[str, Any]] = []
                if terminal == "SINGLE_GRAPHS":
                    evidence_rows = source_incidences[source["candidate_id"]]
                    g2a_rows = [row for row in evidence_rows
                                if row["evidence"]["role"] == "G2A_SHEET"]
                    need(len(g2a_rows) == 1, "single graph G2A")
                    g2a = g2a_rows[0]["evidence"]
                    positive_rows = [row for row in evidence_rows
                                     if row["evidence"]["role"] == "G2B_POSITIVE_SIDE"]
                    cross_positive = [row for row in positive_rows
                                      if row["evidence"]["fresh_component_id"]
                                         != g2a["fresh_component_id"]]
                    components = {row["evidence"]["fresh_component_id"]
                                  for row in evidence_rows}
                    if cross_positive:
                        candidate_relation = "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"
                        for incidence_row in sorted(cross_positive,
                                                    key=lambda row: row["row_sha256"]):
                            positive = incidence_row["evidence"]
                            member_pair = sorted([g2a["member_id"], positive["member_id"]])
                            component_pair = sorted([g2a["fresh_component_id"],
                                                     positive["fresh_component_id"]])
                            need(member_pair[0] != member_pair[1]
                                 and component_pair[0] != component_pair[1],
                                 "single graph cross pair")
                            proof_key = "round306c27r2-v5-physical-proof:" + digest([
                                source["candidate_id"], incidence_row["row_sha256"], member_pair])
                            witness_key = "single-graph-positive-incidence:" + digest([
                                source["candidate_id"], g2a_rows[0]["row_sha256"],
                                incidence_row["row_sha256"]])
                            edge_key = "round306c27r2-v5-component-edge:" + digest(component_pair)
                            proof_body = {
                                "schema": PROOF_SCHEMA,
                                "ordinal": len(proof_rows),
                                "proof_row_key": proof_key,
                                "candidate_key": source["candidate_id"],
                                "atom_pair_incidence_key_or_null": None,
                                "terminal": terminal,
                                "authority_slot": slot,
                                "primitive_authority_row_sha256": source["row_sha256"],
                                "ordered_C15_member_pair": member_pair,
                                "ordered_C15_component_pair": component_pair,
                                "component_edge_key": edge_key,
                                "physical_witness_key": witness_key,
                                "formal_credit": 0,
                            }
                            proof = {**proof_body, "row_sha256": digest(proof_body)}
                            proof_rows.append(proof); candidate_proofs.append(proof)
                    elif len(components) == 1:
                        candidate_relation = "SAME_FROZEN_C15_COMPONENT__NO_EDGE"
                    else:
                        # Only an EXACT_EMPTY_SIDE may be cross-component here;
                        # empty support is nonincidence and cannot mint an edge.
                        empty_cross = [row for row in evidence_rows
                                       if row["evidence"]["role"] == "G2B_EXACT_EMPTY_SIDE"
                                       and row["evidence"]["fresh_component_id"]
                                          != g2a["fresh_component_id"]]
                        need(empty_cross and all(
                            row["evidence"]["fresh_component_id"] == g2a["fresh_component_id"]
                            for row in positive_rows), "single exact-empty-only cross split")
                        candidate_relation = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
                body = {
                    "schema": CANDIDATE_SCHEMA,
                    "ordinal": ordinal,
                    "candidate_key": source["candidate_id"],
                    "candidate_kind": kind,
                    "candidate_pair_key_or_null": None,
                    "terminal_ordinal": terminal_ordinal,
                    "terminal": terminal,
                    "authority_slot": slot,
                    "primitive_authority_row_sha256": source["row_sha256"],
                    "component_relation_disposition": candidate_relation,
                    "physical_proof_row_count": len(candidate_proofs),
                    "physical_proof_row_sequence_sha256": sequence_sha(
                        [row["row_sha256"] for row in candidate_proofs]),
                    "formal_credit": 0,
                }
                candidate_rows.append({**body, "row_sha256": digest(body)})
            terminal_dir = output / slot
            terminal_dir.mkdir()
            candidate_path = terminal_dir / "candidate_ownership.jsonl.gz"
            proof_path = terminal_dir / "materialized_physical_proof_join.jsonl.gz"
            write_jsonl(candidate_path, candidate_rows)
            write_jsonl(proof_path, proof_rows)
            entries.append({
                "terminal_ordinal": terminal_ordinal,
                "terminal": terminal,
                "authority_slot": slot,
                "native_candidate_count": len(candidate_rows),
                "native_semantic_proof_incidence_count": sum(
                    len(source_incidences[row["candidate_id"]]) for row in by_terminal[terminal]),
                "semantic_incidences_promoted_to_physical_proof_count": len(proof_rows),
                "candidate_ownership_ledger": descriptor(
                    candidate_path, candidate_rows, CANDIDATE_SCHEMA, "candidate_key", ["candidate_key"]),
                "materialized_physical_proof_join_ledger": descriptor(
                    proof_path, proof_rows, PROOF_SCHEMA, "proof_row_key", ["candidate_key"]),
                "formal_credit": 0,
            })
            total += len(candidate_rows)
            for row in candidate_rows:
                disposition = row["component_relation_disposition"]
                relation_census[disposition] = relation_census.get(disposition, 0) + 1
        need(total == 52_064 and relation_census == {
            "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 40_792,
            "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 11_056,
            "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 216,
        }, "adapter total/relation census")
        body = {
            "schema": "cm2.c27-independent.legacy-terminal.common-v2-adapter.result.v1",
            "status": "PASS_SIX_LEGACY_AUTHORITIES_ADAPTED_TO_ACTUAL_V5_COMMON_V2__52064_CANDIDATES__216_PHYSICAL_PROOFS__ZERO_CREDIT",
            "adapter_entries": entries,
            "candidate_ownership_row_schema": CANDIDATE_SCHEMA,
            "materialized_physical_proof_join_row_schema": PROOF_SCHEMA,
            "candidate_total": total,
            "native_semantic_proof_incidence_total": 62_160,
            "materialized_physical_proof_join_total": 216,
            "component_relation_disposition_census": dict(sorted(relation_census.items())),
            "incidence_row_is_not_automatically_a_physical_proof": True,
            "proof_join_disposition": "ONLY_216_T03_G2B_POSITIVE_CROSS_COMPONENT_INCIDENCES_PROMOTED__EXACT_EMPTY_SIDES_AND_SAME_COMPONENT_INCIDENCES_NOT_PROMOTED",
            "source_native_verification_sha256": verification["verification_sha256"],
            "input_pins": {str(path.relative_to(ROOT)): expected
                           for path, expected in sorted(PINS.items(), key=lambda item: str(item[0]))},
            "seed_declared_but_not_semantically_used": True,
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        value = {**body, "result_sha256": digest(body)}
        (output / "result.json").write_bytes(encode(value) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": value["status"],
                  "result_sha256": value["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
