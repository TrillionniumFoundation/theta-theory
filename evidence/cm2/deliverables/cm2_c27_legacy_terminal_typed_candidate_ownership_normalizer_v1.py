#!/usr/bin/env python3
"""Normalize row-backed legacy C27 terminals under correction-v2 semantics.

Candidate ownership and proof incidence are deliberately separate.  In
particular, OUTGOING/SINGLE dispositions are evidence rows, not candidates,
and the 276 R295A representation aliases are auxiliary annotations on the
same RETAINED_CONTINUATION candidates, never a second terminal universe.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime/audit"

RETAINED_STREAM = DELIVERABLES / "cm2_c27_retained_continuation_stream_probe.py"
RETAINED_RECEIPT = DELIVERABLES / "cm2_c27_retained_continuation_subgate_receipt.json"
R295A = DELIVERABLES / "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz"
OUTGOING = RUNTIME / "c27-outgoing-graphs-stream-seed-30627101/ledger.jsonl.gz"
OUTGOING_RECEIPT = DELIVERABLES / "cm2_c27_outgoing_graphs_physical_totality_subgate_receipt.json"
SINGLE = RUNTIME / "c27-single-graphs-stream-seed-30628101/ledger.jsonl.gz"
SINGLE_RECEIPT = DELIVERABLES / "cm2_c27_single_graphs_subgate_receipt.json"
SHEET = RUNTIME / "c27-sheet-owner-shadow-physical-stream-seed-30627401/sheet_owner_shadow_terminal_ledger.jsonl.gz"
SHEET_RECEIPT = DELIVERABLES / "cm2_c27_sheet_owner_shadow_physical_totality_subgate_receipt.json"
INCLUDED = RUNTIME / "c27-included-stratum-10660-materialized-v1-seed-30646101/included_stratum_10660_materialized_candidates.jsonl.gz"
INCLUDED_RECEIPT = DELIVERABLES / "cm2_c27_included_stratum_10660_materialized_zero_credit_receipt_v1.json"

PINS = {
    RETAINED_STREAM: "bc5faef574966d61ab278a188180b7ae4b08819c1300f42c15e7190efc6f687a",
    RETAINED_RECEIPT: "08b760876914406e2fbe4e897609afd6ffc6f3667acaf6a1b4a7a9df58f6e263",
    R295A: "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
    OUTGOING: "3e915eb5f45d2e0cef6911b898d3f9653d13e2035c8d4129613021e82e9f5f4e",
    OUTGOING_RECEIPT: "39fc442c396038dfcfd9ca01a99c1188c87015b778bc8d15795a0336a8bbd5e9",
    SINGLE: "72f34d0246799fa89338849c92c2f1a3e0048ef9d4e75f4da054812822496262",
    SINGLE_RECEIPT: "40435bf43d9bab01b54f9bc0a8c283930228e84a33f95d2af14783a2eb1d6ad5",
    SHEET: "3050f59733c5f5e183a3babc3ff1f2e772153b2e655997a3acd0826ad184fac2",
    SHEET_RECEIPT: "2833cc5f1c9d35eeca36722dfb348ad16e9d09e8d44d8983e63b61f390a93d0f",
    INCLUDED: "4fc13179695407b093395243fb891d59ed7b7c5c7423208d394a59d6612a78be",
    INCLUDED_RECEIPT: "bfe26acf520f98b889a2a10bc6a4933c6519d610b0896a58e83cde4bfcd999c7",
}

EXPECTED_CANDIDATES = {
    "RETAINED_CONTINUATION": 276,
    "OUTGOING_GRAPHS": 264,
    "SINGLE_GRAPHS": 4_984,
    "SHEET_OWNER": 17_940,
    "SHEET_SHADOW": 17_940,
    "INCLUDED_STRATUM_ATTACHMENTS": 10_660,
}
EXPECTED_INCIDENCES = {
    "RETAINED_CONTINUATION": 276,
    "OUTGOING_GRAPHS": 792,
    "SINGLE_GRAPHS": 14_552,
    "SHEET_OWNER": 17_940,
    "SHEET_SHADOW": 17_940,
    "INCLUDED_STRATUM_ATTACHMENTS": 10_660,
}

RETAINED_BODY_KEYS = {
    "representation_id", "owner_member_id", "fresh_component_id",
    "base_root_id", "official_key_id", "shared_full_face_sha256",
    "typed_source_support_ast_sha256", "owner_support_ast_sha256",
    "C15_row_sha256", "C20A_row_sha256", "C20D_row_sha256",
    "I2_row_sha256", "R295A_row_sha256", "C25_member_row_sha256",
    "C25_representation_row_sha256", "C26_handle_row_sha256",
    "formal_credit",
}


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
            value = json.loads(line)
            need(type(value) is dict, "jsonl object:" + path.name)
            yield value


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                zipped.write(encode(row) + b"\n")


def load_retained(seed: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec = importlib.util.spec_from_file_location("cm2_retained_pinned", RETAINED_STREAM)
    need(spec is not None and spec.loader is not None, "retained module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_digest = module.digest
    captured: dict[str, dict[str, Any]] = {}

    def capture(value: Any) -> str:
        answer = original_digest(value)
        if type(value) is dict and set(value) == RETAINED_BODY_KEYS:
            representation = value["representation_id"]
            need(representation not in captured, "retained capture unique")
            captured[representation] = copy.deepcopy(value)
        return answer

    module.digest = capture
    result = module.build(seed)
    need(len(captured) == 276, "retained captured body count")
    receipt = json.loads(RETAINED_RECEIPT.read_bytes())
    commitments = sorted((key, digest(body)) for key, body in captured.items())
    identifiers = hashlib.sha256()
    sequence = hashlib.sha256()
    for representation, row_hash in commitments:
        identifiers.update(representation.encode("ascii") + b"\n")
        sequence.update(bytes.fromhex(row_hash))
    need(identifiers.hexdigest() == receipt["candidate_commitment"]["candidate_representation_ids_sha256"]
         == result["candidate_universe"]["candidate_representation_ids_sha256"],
         "retained ID commitment")
    need(sequence.hexdigest() == receipt["candidate_commitment"]["candidate_row_sequence_sha256"]
         == result["candidate_universe"]["candidate_row_sequence_sha256"],
         "retained row commitment")
    return [captured[key] for key in sorted(captured)], result


def candidate(terminal: str, unit: str, key: str, source_kind: str,
              source_file: Path, source_row_sha: str,
              proof_count: int) -> dict[str, Any]:
    candidate_id = f"cm2-c27-independent:{terminal}:{key}"
    return {
        "schema": "cm2.c27-independent.legacy-terminal.typed-candidate-ownership-row.v1",
        "candidate_id": candidate_id,
        "candidate_key": key,
        "candidate_unit": unit,
        "terminal": terminal,
        "terminal_assignment_cardinality": 1,
        "source_authority_kind": source_kind,
        "source_authority_file_sha256": PINS[source_file],
        "source_authority_row_sha256": source_row_sha,
        "proof_incidence_count": proof_count,
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def incidence(candidate_row: dict[str, Any], ordinal: int, role: str,
              evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "cm2.c27-independent.legacy-terminal.proof-incidence-row.v1",
        "candidate_id": candidate_row["candidate_id"],
        "terminal": candidate_row["terminal"],
        "incidence_ordinal_within_candidate": ordinal,
        "incidence_role": role,
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def close_and_sort(rows: list[dict[str, Any]], key_fields: tuple[str, ...]) -> None:
    rows.sort(key=lambda row: tuple(str(row[key]) for key in key_fields))
    for ordinal, row in enumerate(rows):
        row["ordinal"] = ordinal
        row["row_sha256"] = digest(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        for path, expected in PINS.items():
            need(path.is_file() and not path.is_symlink(), "regular input:" + str(path))
            need(file_hash(path) == expected, "input pin:" + path.name)
        candidates: list[dict[str, Any]] = []
        incidences: list[dict[str, Any]] = []
        aliases: list[dict[str, Any]] = []

        retained_bodies, retained_result = load_retained(args.seed)
        with gzip.open(R295A, "rt", encoding="utf-8") as handle:
            alias_top = json.load(handle)
        alias_by_sha = {row["row_sha256"]: row for row in alias_top["rows"]}
        need(len(alias_by_sha) == 276, "alias row cover")
        for body in retained_bodies:
            source_sha = digest(body)
            row = candidate("RETAINED_CONTINUATION", "REPRESENTATION",
                            body["representation_id"], "RETAINED_SEMANTIC_BODY",
                            RETAINED_STREAM, source_sha, 1)
            candidates.append(row)
            incidences.append(incidence(row, 0, "EXACT_POSITIVE_T_FULL_FACE_AUTHORITY",
                                         body))
            alias = alias_by_sha.get(body["R295A_row_sha256"])
            need(alias is not None, "retained alias binding")
            aliases.append({
                "schema": "cm2.c27-independent.representation-alias.auxiliary-crosswalk-row.v1",
                "representation_id": body["representation_id"],
                "retained_candidate_id": row["candidate_id"],
                "candidate_terminal": "RETAINED_CONTINUATION",
                "representation_map_role": "AUXILIARY_ALIAS_ANNOTATION",
                "independent_terminal_candidate": False,
                "representation_alias_terminal_candidate_count": 0,
                "R295A_alias_row_id": alias["Round295A_retained_continuation_alias_row_id"],
                "R295A_alias_row_sha256": alias["row_sha256"],
                "formal_credit": 0,
                "source_W_transition_authorized": False,
            })

        for source in jsonl(OUTGOING):
            closed(source, "candidate_digest", "outgoing")
            need(source["terminal"] == "OUTGOING_GRAPHS"
                 and len(source["dispositions"]) == 3
                 and source["formal_credit"] == 0, "outgoing semantics")
            row = candidate("OUTGOING_GRAPHS", "GRAPH_ROOT", source["graph_id"],
                            "OUTGOING_ROOT_ROW", OUTGOING,
                            source["candidate_digest"], len(source["dispositions"]))
            candidates.append(row)
            for index, proof in enumerate(source["dispositions"]):
                incidences.append(incidence(row, index, proof["role"], proof))

        for source in jsonl(SINGLE):
            closed(source, "candidate_digest", "single")
            need(source["terminal"] == "SINGLE_GRAPHS"
                 and len(source["dispositions"]) >= 2
                 and source["formal_credit"] == 0, "single semantics")
            row = candidate("SINGLE_GRAPHS", "GRAPH_ROOT", source["graph_id"],
                            "SINGLE_ROOT_ROW", SINGLE,
                            source["candidate_digest"], len(source["dispositions"]))
            candidates.append(row)
            for index, proof in enumerate(source["dispositions"]):
                incidences.append(incidence(row, index, proof["role"], proof))

        for source in jsonl(SHEET):
            closed(source, "row_sha256", "sheet")
            need(source["terminal"] in {"SHEET_OWNER", "SHEET_SHADOW"}
                 and source["formal_credit"] == 0, "sheet semantics")
            key = source["physical_sheet_id"] + "|" + source["role"]
            row = candidate(source["terminal"], "PHYSICAL_SHEET_ROLE", key,
                            "SHEET_ROLE_ROW", SHEET, source["row_sha256"], 1)
            candidates.append(row)
            evidence = {key: source[key] for key in (
                "physical_sheet_id", "role", "assigned_member_id",
                "owner_member_id", "shadow_member_id", "fresh_component_id",
                "primitive_sheet_row_sha256", "owner_C15_row_sha256",
                "shadow_C15_row_sha256", "owner_C25_row_sha256",
                "shadow_C25_row_sha256", "C26_owner_root_row_sha256",
                "materialized_shadow_node_row_sha256", "terminal_disposition")}
            evidence["source_row_sha256"] = source["row_sha256"]
            incidences.append(incidence(row, 0, source["role"] + "_HALF_OPEN_ASSIGNMENT",
                                         evidence))

        for source in jsonl(INCLUDED):
            closed(source, "row_sha256", "included")
            need(source["terminal"] == "INCLUDED_STRATUM_ATTACHMENTS"
                 and source["retained_continuation_candidate"] is False
                 and source["formal_credit"] == 0, "included semantics")
            row = candidate("INCLUDED_STRATUM_ATTACHMENTS", "REPRESENTATION",
                            source["representation_id"], "INCLUDED_MATERIALIZED_ROW",
                            INCLUDED, source["row_sha256"], 1)
            candidates.append(row)
            evidence = {key: source[key] for key in (
                "representation_id", "owner_member_id", "fresh_component_id",
                "base_root_id", "official_key_id", "representation_semantic_kind",
                "semantic_kernel", "semantic_body_sha256", "C15_member_row_sha256",
                "C25_representation_row_sha256", "C26_handle_row_sha256")}
            evidence["source_row_sha256"] = source["row_sha256"]
            incidences.append(incidence(row, 0, "MATERIALIZED_ATTACHMENT_AUTHORITY", evidence))

        close_and_sort(candidates, ("terminal", "candidate_key"))
        close_and_sort(incidences, ("candidate_id", "incidence_ordinal_within_candidate"))
        close_and_sort(aliases, ("representation_id",))
        candidate_by_id = {row["candidate_id"]: row for row in candidates}
        need(len(candidate_by_id) == len(candidates), "candidate ID uniqueness")
        incidence_census: dict[str, int] = {}
        terminal_census: dict[str, int] = {}
        incidence_by_candidate: dict[str, int] = {}
        for row in candidates:
            terminal_census[row["terminal"]] = terminal_census.get(row["terminal"], 0) + 1
            need(row["terminal_assignment_cardinality"] == 1, "exact-one terminal")
        for row in incidences:
            need(row["candidate_id"] in candidate_by_id
                 and candidate_by_id[row["candidate_id"]]["terminal"] == row["terminal"],
                 "incidence candidate binding")
            incidence_census[row["terminal"]] = incidence_census.get(row["terminal"], 0) + 1
            incidence_by_candidate[row["candidate_id"]] = incidence_by_candidate.get(row["candidate_id"], 0) + 1
        need(terminal_census == EXPECTED_CANDIDATES, "candidate census")
        need(incidence_census == EXPECTED_INCIDENCES, "incidence census")
        need(all(incidence_by_candidate.get(row["candidate_id"]) == row["proof_incidence_count"]
                 for row in candidates), "per-candidate incidence cardinality")
        need(len(aliases) == 276
             and all(row["retained_candidate_id"] in candidate_by_id
                     and row["independent_terminal_candidate"] is False
                     and row["representation_alias_terminal_candidate_count"] == 0
                     for row in aliases), "auxiliary alias semantics")

        output = Path(args.output_dir)
        need(not output.exists(), "fresh output dir")
        output.mkdir(parents=True)
        candidate_path = output / "typed_candidate_ownership.jsonl.gz"
        incidence_path = output / "proof_incidence.jsonl.gz"
        alias_path = output / "representation_alias_auxiliary_crosswalk.jsonl.gz"
        write_jsonl(candidate_path, candidates)
        write_jsonl(incidence_path, incidences)
        write_jsonl(alias_path, aliases)
        body = {
            "schema": "cm2.c27-independent.legacy-terminal.typed-candidate-ownership-normalization.result.v1",
            "status": "PASS_SCOPED_ROW_BACKED_TERMINALS_NORMALIZED_UNDER_CORRECTION_V2__ZERO_CREDIT",
            "correction_v2_rule": "EACH_CANDIDATE_HAS_EXACTLY_ONE_TERMINAL__PROOF_INCIDENCES_ARE_NOT_CANDIDATES",
            "candidate_census": dict(sorted(terminal_census.items())),
            "candidate_total": len(candidates),
            "proof_incidence_census": dict(sorted(incidence_census.items())),
            "proof_incidence_total": len(incidences),
            "representation_aliases": {
                "auxiliary_crosswalk_rows": len(aliases),
                "independent_terminal_candidates": 0,
                "double_count_with_retained_continuation": 0,
            },
            "retained_stream_result_sha256": retained_result["result_sha256"],
            "ledgers": {
                candidate_path.name: {"row_count": len(candidates), "file_sha256": file_hash(candidate_path),
                                      "row_sequence_sha256": digest([row["row_sha256"] for row in candidates])},
                incidence_path.name: {"row_count": len(incidences), "file_sha256": file_hash(incidence_path),
                                      "row_sequence_sha256": digest([row["row_sha256"] for row in incidences])},
                alias_path.name: {"row_count": len(aliases), "file_sha256": file_hash(alias_path),
                                  "row_sequence_sha256": digest([row["row_sha256"] for row in aliases])},
            },
            "input_pins": {str(path.relative_to(ROOT)): expected
                           for path, expected in sorted(PINS.items(), key=lambda item: str(item[0]))},
            "seed_declared_but_not_semantically_used": True,
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "scope_excludes_DOUBLE_GRAPHS": True,
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
    print(encode({"status": value["status"], "candidate_total": value["candidate_total"],
                  "proof_incidence_total": value["proof_incidence_total"],
                  "result_sha256": value["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
