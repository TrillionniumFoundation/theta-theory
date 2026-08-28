#!/usr/bin/env python3
"""Actual fail-closed preflight for the primitive twenty-family gate v5.

Only primitive/scoped authorities are consumed.  The preflight validates the
corrected v2 contract and reconstructs unique terminal ownership for all
101,080 candidate pairs.  Atom incidence is many-to-many: uniqueness is on
(atom, pair), never on atom alone.  Until both the full 101080-to-483232 atom
join and the explicit C26 exact-contact absence theorem are formally bound,
the program writes a gap ledger/result and exits 2.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent.parent


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "fresh row")
    return {**body, "row_sha256": digest(body)}


def check_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_mode,
        value.st_uid,
        value.st_gid,
    )


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    pre: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        need(type(expected) is str and len(expected) == 64, label + ":expected sha")
        resolved = path.resolve()
        fd = os.open(
            resolved,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":file sha")
            need(fingerprint(os.fstat(fd)) == fingerprint(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, resolved, fd, fingerprint(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        need(fingerprint(os.fstat(self.fd)) == self.pre, self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self.stable("raw")
        return b"".join(chunks)

    def document(self, require_canonical: bool = False) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        need(type(value) is dict, self.label + ":document")
        if require_canonical:
            need(canonical(value) + b"\n" == raw, self.label + ":canonical")
        closure_keys = [key for key in (
            "result_sha256",
            "receipt_sha256",
            "design_sha256",
            "verification_sha256",
        ) if key in value]
        need(len(closure_keys) == 1, self.label + ":closure key")
        body = dict(value)
        claim = body.pop(closure_keys[0])
        need(type(claim) is str and claim == digest(body), self.label + ":document closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    encoded = line[:-1]
                    row = json.loads(encoded)
                    need(type(row) is dict and canonical(row) == encoded,
                         f"{self.label}:{ordinal}:canonical")
                    check_row(row, f"{self.label}:{ordinal}")
                    yield row
        self.stable("rows")

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {
            "path": rendered,
            "sha256": self.sha256,
            "size": self.pre[2],
            "stat_fingerprint": list(self.pre),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def unordered(left: str, right: str) -> tuple[str, str]:
    need(type(left) is str and type(right) is str and left != right, "nonself pair")
    return (left, right) if left < right else (right, left)


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
            for row in rows:
                check_row(row, path.name + f":{count}")
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return {
        "filename": path.name,
        "row_count": count,
        "file_sha256": file_sha(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


def validate_correction(value: dict[str, Any]) -> None:
    need(value["schema"]
             == "cm2.c27-independent.primitive-twenty-family-gate-v5-aggregator-design-correction.v2"
         and value["status"].startswith("CORRECTED_DESIGN_READY__")
         and value["formal_credit"] == 0
         and value["manifest_authorized"] is False,
         "correction-v2 authority")
    levels = value["corrected_uniqueness_levels"]
    need(levels["candidate_pair"]["each_pair_has_exactly_one_assigned_terminal"] is True
         and levels["atom_pair_incidence"]["duplicate_incidence_key_forbidden"] is True
         and levels["atom_pair_incidence"]["one_atom_may_have_multiple_distinct_pair_incidences"]
             is True
         and levels["atom_pair_incidence"]["one_atom_may_therefore_observe_multiple_distinct_terminals"]
             is True
         and levels["atom"]["each_atom_has_an_exact_materialized_incidence_set"] is True
         and levels["atom"]["empty_incidence_set_is_the_atom_complement_disposition"] is True
         and levels["atom"]["atom_terminal_uniqueness_required"] is False
         and levels["atom"]["atom_terminal_mutual_exclusivity_required"] is False,
         "corrected many-to-many incidence contract")
    contract = value["corrected_full_union_atom_contract"]
    need(contract["primitive_support_atom_denominator"] == 483_232
         and contract["full_pair_authority_row_count"] == 101_080,
         "corrected denominator/pair authority")


def validate_static_authorities(documents: dict[str, dict[str, Any]]) -> None:
    strict = documents["strict_volume_receipt"]
    need(strict["schema"]
             == "cm2.c27.same-chart-strict-volume-totality.v1.final-zero-credit-receipt.v1"
         and strict["formal_credit"] == 0
         and strict["exact_census"]["all_component_strict_intersection_pair_count"] == 187_132
         and strict["exact_census"]["primitive_atom_count"] == 483_232
         and strict["forbidden_inputs"] == {
             "C27_or_FAMILIES_imported_or_read": False,
             "historical_edge_ledger_used": False,
             "older_same_chart_census_ledger_imported_or_read": False,
         }, "strict-volume authority")

    lower = documents["lower_contact_receipt"]
    need(lower["schema"]
             == "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.terminal-receipt.v1"
         and lower["formal_credit"] == 0
         and lower["lower_dimensional_candidate_pair_count"] == 5_783_708
         and lower["dimension_census"]["3"] == 187_132
         and lower["C26_role"]["full_rows_read"] == 691_424
         and lower["C26_role"]["absence_used_as_negative_geometry_theorem"] is False
         and lower["full_20_family_totality_authorized"] is False
         and lower["forbidden_inputs"] == {
             "C27_FAMILIES_read": False,
             "historical_edge_universe_read": False,
             "older_same_chart_candidate_ledger_read": False,
         }, "lower-contact authority and C26 insufficiency")

    c19c = documents["c19c_receipt"]
    need(c19c["schema"] == "cm2.c19c-endpoint-ownership-v3.terminal-receipt.v1"
         and c19c["formal_credit"] == 0
         and c19c["source_W_transition_authorized"] is False
         and c19c["authority"]["direct_rule"] == "oriented [lower,upper) on internal faces",
         "C19C half-open authority")

    g2a = documents["g2a_result"]
    need(g2a["schema"] == "cm2.c27-independent.g2a-relative2d-primitive-totality-theorem.v2"
         and g2a["formal_credit"] == 0
         and g2a["global_three_terminal_unique_assignment"] is False
         and g2a["ledgers"]["contacts"]["row_count"] == 9_408
         and g2a["ledgers"]["reverse_empty"]["row_count"] == 9_392,
         "G2A scoped authority")

    g2b = documents["g2b_receipt"]
    need(g2b["schema"] == "cm2.c27-independent.c24a-g2b-terminal-zero-credit.v1"
         and g2b["formal_state_unchanged"]["formal_credit"] == 0
         and g2b["G2B_closed_diagnostic"]["exact_positive"] == 9_408
         and g2b["G2B_closed_diagnostic"]["exact_empty"] == 9_392,
         "G2B terminal authority")


def validate_pair_union(
    union: dict[str, Any], ownership: Capture
) -> dict[str, Any]:
    need(union["schema"]
             == "cm2.c27-independent.c24a-current-primitive-three-terminal-union-comparator.v1"
         and union["formal_credit"] == 0
         and union["manifest_authorized"] is False
         and union["scoped_candidate_union"]["union_pair_count"] == 101_080
         and union["scoped_candidate_union"]["scoped_unique_assignment_closed"] is True
         and union["global_claim_gate"]["global_candidate_totality_proved"] is False,
         "scoped pair-union authority")
    descriptor = union["ledgers"]["unique_ownership"]
    need(descriptor["file_sha256"] == ownership.sha256
         and descriptor["row_count"] == 101_080
         and descriptor["filename"] == ownership.path.name,
         "ownership/result binding")
    seen: set[tuple[str, str]] = set()
    terminal = Counter()
    source = Counter()
    branch = Counter()
    sequence = hashlib.sha256()
    for ordinal, row in enumerate(ownership.rows()):
        label = f"ownership:{ordinal}"
        need(row["schema"]
                 == "cm2.c27-independent.primitive-three-terminal-unique-ownership.row.v1"
             and row["formal_credit"] == 0,
             label + ":schema/credit")
        values = row["pair_key"]
        need(type(values) is list and len(values) == 2, label + ":pair")
        key = unordered(values[0], values[1])
        need(key not in seen, label + ":pair unique")
        seen.add(key)
        assigned = row["assigned_terminal"]
        need(assigned in {
            "SIGNED_BOUNDARY_FACES",
            "COMPLETE_BOUNDARY_FACES",
            "POSITIVE_VOLUME_CARRIERS",
        }, label + ":allowed terminal")
        need(row["pair_assignment_rule"]
                 == "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE_VOLUME_CARRIERS",
             label + ":priority")
        authority = row["source_authority"]
        if authority == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":
            need(assigned == "POSITIVE_VOLUME_CARRIERS"
                 and row["positive_support_branch"]
                     == "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC"
                 and row["current_source_terminal"] is None
                 and type(row["C24A_G2B_exact_row_sha256"]) is str
                 and type(row["G2A_diagnostic_alias_row_sha256"]) is str,
                 label + ":C24A pair normalization")
        else:
            need(authority == "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER"
                 and row["C24A_G2B_exact_row_sha256"] is None
                 and row["G2A_diagnostic_alias_row_sha256"] is None,
                 label + ":current authority")
        terminal[assigned] += 1
        source[authority] += 1
        if row["positive_support_branch"] is not None:
            branch[row["positive_support_branch"]] += 1
        sequence.update(bytes.fromhex(row["row_sha256"]))
    need(len(seen) == 101_080
         and terminal == {
             "SIGNED_BOUNDARY_FACES": 25_452,
             "COMPLETE_BOUNDARY_FACES": 10_688,
             "POSITIVE_VOLUME_CARRIERS": 64_940,
         }
         and source == {
             "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER": 91_672,
             "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER": 9_408,
         }
         and branch == {
             "CURRENT_C19_PHYSICAL_SUPPORT": 55_532,
             "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC": 9_408,
         }
         and sequence.hexdigest() == descriptor["row_sequence_sha256"],
         "101080 pair authority exact census")
    return {
        "pair_count": len(seen),
        "terminal_census": dict(sorted(terminal.items())),
        "source_census": dict(sorted(source.items())),
        "positive_branch_census": dict(sorted(branch.items())),
        "each_candidate_pair_exactly_one_terminal": True,
        "G2A_alias_counted_as_second_pair": False,
    }


def validate_optional_full_atom(document: dict[str, Any]) -> None:
    need(document["schema"]
             == "cm2.c27-independent.full-101080-atom-pair-incidence.v1"
         and document["formal_credit"] == 0
         and document["pair_authority_row_count"] == 101_080
         and document["primitive_support_atom_denominator"] == 483_232
         and document["per_candidate_pair_exactly_one_terminal"] is True
         and document["atom_pair_incidence_key_unique"] is True
         and document["all_incidence_pairs_bound_to_pair_authority"] is True
         and document["all_atoms_exact_incidence_set_or_empty_complement"] is True
         and document["atom_multi_pair_allowed"] is True
         and document["atom_multi_terminal_allowed"] is True
         and document["C24A_G2B_target_C22_atom_join_count"] == 9_408
         and document["C24A_source_member_outside_atom_denominator"] is True
         and document["G2A_alias_adds_second_incidence"] is False,
         "full atom-incidence formal contract")


def validate_optional_c26(document: dict[str, Any]) -> None:
    need(document["schema"]
             == "cm2.c27-independent.c26-primitive-exact-contact-absence-theorem.v1"
         and document["formal_credit"] == 0
         and document["C26_rows_enumerated"] == 691_424
         and document["lower_dimensional_denominator_bound"] == 5_783_708
         and document["exact_contact_witness_count"] == 0
         and document["explicit_absence_theorem"] is True
         and document["absence_inferred_from_missing_rows_or_volume"] is False,
         "C26 formal absence theorem")


def gap_row(
    slot: str,
    status: str,
    gate_blocking: bool,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return closed({
        "schema": "cm2.c27-independent.primitive-twenty-family-v5-authority-gap.row.v1",
        "authority_slot": slot,
        "authority_status": status,
        "gate_blocking": gate_blocking,
        "evidence": evidence,
        "formal_credit": 0,
    })


def run(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    output = Path(args.out_dir)
    need(not output.exists(), "fresh output directory")
    required = {
        "correction_v2": (args.correction_v2, args.correction_v2_sha256),
        "strict_volume_receipt": (
            args.strict_volume_receipt,
            args.strict_volume_receipt_sha256,
        ),
        "lower_contact_receipt": (
            args.lower_contact_receipt,
            args.lower_contact_receipt_sha256,
        ),
        "c19c_receipt": (args.c19c_receipt, args.c19c_receipt_sha256),
        "g2a_result": (args.g2a_result, args.g2a_result_sha256),
        "g2b_receipt": (args.g2b_receipt, args.g2b_receipt_sha256),
        "pair_union_result": (args.pair_union_result, args.pair_union_result_sha256),
        "pair_ownership": (args.pair_ownership, args.pair_ownership_sha256),
    }
    captures: dict[str, Capture] = {}
    try:
        for label, (path, sha) in required.items():
            captures[label] = Capture.open(label, Path(path), sha)
        optional_pairs = (
            ("full_atom_join_result", args.full_atom_join_result,
             args.full_atom_join_result_sha256),
            ("c26_absence_result", args.c26_absence_result,
             args.c26_absence_result_sha256),
        )
        for label, path, sha in optional_pairs:
            need((path is None) is (sha is None), label + ":path/sha paired")
            if path is not None:
                captures[label] = Capture.open(label, Path(path), sha)

        correction = captures["correction_v2"].document(require_canonical=True)
        validate_correction(correction)
        documents = {
            label: captures[label].document(require_canonical=False)
            for label in (
                "strict_volume_receipt",
                "lower_contact_receipt",
                "c19c_receipt",
                "g2a_result",
                "g2b_receipt",
            )
        }
        validate_static_authorities(documents)
        union = captures["pair_union_result"].document(require_canonical=True)
        pair_summary = validate_pair_union(union, captures["pair_ownership"])

        full_ready = "full_atom_join_result" in captures
        c26_ready = "c26_absence_result" in captures
        if full_ready:
            validate_optional_full_atom(
                captures["full_atom_join_result"].document(require_canonical=True)
            )
        if c26_ready:
            validate_optional_c26(
                captures["c26_absence_result"].document(require_canonical=True)
            )

        gaps = [
            gap_row("CORRECTION_V2_MANY_TO_MANY_ATOM_CONTRACT",
                    "PRESENT_VALID", False,
                    {"design_sha256": correction["design_sha256"]}),
            gap_row("SAME_CHART_STRICT_VOLUME_187132",
                    "PRESENT_VALID", False,
                    {"primitive_row_count": 187_132}),
            gap_row("SAME_CHART_LOWER_EXACT_CONTACT_5783708",
                    "PRESENT_VALID_C26_ABSENCE_NOT_IMPLIED", False,
                    {"primitive_row_count": 5_783_708,
                     "C26_rows_read": 691_424,
                     "C26_absence_used_as_negative_theorem": False}),
            gap_row("C19C_ENDPOINT_V3_HALF_OPEN",
                    "PRESENT_VALID", False,
                    {"direct_rule": "oriented [lower,upper) on internal faces"}),
            gap_row("FORMAL_SCOPED_G2A_ROUTE",
                    "PRESENT_VALID_GLOBAL_OPEN", False,
                    {"positive_alias_keys": 9_408, "reverse_empty_keys": 9_392}),
            gap_row("G2B_TERMINAL_AUTHORITY",
                    "PRESENT_VALID_ZERO_CREDIT", False,
                    {"positive_keys": 9_408, "empty_keys": 9_392}),
            gap_row("SCOPED_PAIR_UNION_101080",
                    "PRESENT_VALID_PAIR_UNIQUE", False,
                    pair_summary),
            gap_row("FULL_101080_TO_483232_ATOM_INCIDENCE",
                    "PRESENT_VALID" if full_ready else "MISSING_FORMAL_AUTHORITY",
                    not full_ready,
                    ({"primitive_support_atom_denominator": 483_232,
                      "atom_pair_incidence_unique": True,
                      "atom_multi_pair_allowed": True,
                      "atom_multi_terminal_allowed": True}
                     if full_ready else {
                         "required_pair_authority_rows": 101_080,
                         "required_atom_denominator": 483_232,
                         "required_contract": "EXACT_DUPLICATE_FREE_INCIDENCE_SET_OR_EMPTY_COMPLEMENT",
                         "current_only_complement_420992_is_not_global": True,
                     })),
            gap_row("C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_THEOREM",
                    "PRESENT_VALID" if c26_ready else "MISSING_FORMAL_AUTHORITY",
                    not c26_ready,
                    ({"C26_rows_enumerated": 691_424,
                      "exact_contact_witness_count": 0,
                      "explicit_absence_theorem": True}
                     if c26_ready else {
                         "C26_rows_known_in_lower_authority": 691_424,
                         "absence_may_not_be_inferred_from_missing_rows_or_volume": True,
                         "explicit_primitive_exact_contact_theorem_required": True,
                     })),
        ]
        missing = [row["authority_slot"] for row in gaps if row["gate_blocking"]]
        accepted = not missing
        output.mkdir(parents=True, exist_ok=False)
        gap_descriptor = write_rows(output / "authority_gap_ledger.jsonl.gz", gaps)
        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-fail-closed-preflight.v1",
            "status": (
                "PASS_ALL_REQUIRED_FORMAL_AUTHORITIES_PRESENT__ZERO_CREDIT"
                if accepted else
                "REJECT_MISSING_FULL_ATOM_JOIN_AND_OR_C26_EXACT_ABSENCE__ZERO_CREDIT"
            ),
            "decision": "SCOPED_READY_ZERO_CREDIT" if accepted else "REJECT",
            "intended_process_exit_code": 0 if accepted else 2,
            "invocation_seed": args.seed,
            "corrected_contract": {
                "each_candidate_pair_exactly_one_terminal": True,
                "atom_pair_incidence_key_unique": True,
                "atom_exact_incidence_set_or_empty_complement": True,
                "atom_multi_pair_allowed": True,
                "atom_multi_terminal_allowed": True,
                "atom_single_pair_or_terminal_constraint_imposed": False,
            },
            "pair_authority_reconstruction": pair_summary,
            "authority_slot_census": {
                "total": len(gaps),
                "present": len(gaps) - len(missing),
                "missing_or_blocking": len(missing),
            },
            "blocking_authority_slots": missing,
            "gap_ledger": gap_descriptor,
            "forbidden_input_governance": {
                "old_C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False,
                "C29_imported_or_read": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "producer_module_imported": False,
            },
            "global_gate": {
                "primitive_support_atom_denominator": 483_232,
                "pair_authority_row_count": 101_080,
                "full_atom_incidence_formal_authority_present": full_ready,
                "C26_exact_contact_absence_formal_authority_present": c26_ready,
                "primitive_twenty_family_totality_proved": accepted,
                "decision": "ZERO_CREDIT_SCOPED_READY" if accepted else "FAIL_CLOSED_REJECT",
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": {
                "C27_transition_totality": 0,
                "C28_pair_routing": 0,
                "C29_physical_maximality": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {
                    label: capture.attestation()
                    for label, capture in sorted(captures.items())
                },
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items()
            if key not in {"invocation_seed", "root_input_capture"}
        })
        result["result_sha256"] = digest(result)
        (output / "preflight_result.json").write_bytes(canonical(result) + b"\n")
        return result, (0 if accepted else 2)
    finally:
        for capture in captures.values():
            capture.close()


def add_required(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "correction-v2",
        "strict-volume-receipt",
        "lower-contact-receipt",
        "c19c-receipt",
        "g2a-result",
        "g2b-receipt",
        "pair-union-result",
        "pair-ownership",
    ):
        add_required(parser, name)
    parser.add_argument("--full-atom-join-result")
    parser.add_argument("--full-atom-join-result-sha256")
    parser.add_argument("--c26-absence-result")
    parser.add_argument("--c26-absence-result-sha256")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result, exit_code = run(args)
    except (Failure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print("REJECT_INVALID_INPUT:" + str(error))
        return 2
    print(canonical({
        "status": result["status"],
        "decision": result["decision"],
        "blocking_authority_slots": result["blocking_authority_slots"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
