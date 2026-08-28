#!/usr/bin/env python3
"""Authority-hardened append-only v2 preflight for primitive gate v5.

Unlike diagnostic v1, this preflight binds the valid G2A final-v2 receipt,
both G2A manifests, its terminal replay and the old-seal invalidation notice.
It also binds the scoped 101,080 pair-union terminal receipt, manifest,
no-import verification and 18/18 coherent attacks through that receipt.

The full atom join seed result is not a formal authority.  Until a final
dual-seed/independent/attack receipt and the formal C26 exact-contact absence
theorem exist, this preflight materializes the gaps and exits 2.
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
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "fresh row")
    return {**body, "row_sha256": digest(body)}


def check_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def fp(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


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
        fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":sha256")
            need(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            return cls(label, resolved, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        need(fp(os.fstat(self.fd)) == self.pre, self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.stable("raw")
        return b"".join(pieces)

    def document(
        self, closure_key: str | None, require_canonical: bool = False
    ) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        need(type(value) is dict, self.label + ":document")
        if require_canonical:
            need(canonical(value) + b"\n" == raw, self.label + ":canonical")
        if closure_key is not None:
            body = dict(value)
            claim = body.pop(closure_key)
            need(type(claim) is str and claim == digest(body), self.label + ":closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
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
        return {"path": rendered, "sha256": self.sha256, "size": self.pre[2],
                "stat_fingerprint": list(self.pre), "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def unordered(values: Any, label: str) -> tuple[str, str]:
    need(type(values) is list and len(values) == 2
         and all(type(item) is str for item in values)
         and values[0] != values[1], label + ":pair")
    return tuple(sorted(values))


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
    return {"filename": path.name, "row_count": count,
            "file_sha256": file_sha(path),
            "row_sequence_sha256": sequence.hexdigest()}


def manifest_entries(raw: bytes, label: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for ordinal, line in enumerate(raw.decode("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64,
             f"{label}:{ordinal}:manifest line")
        sha, path = pieces
        need(path not in entries, f"{label}:{ordinal}:unique path")
        entries[path] = sha
    return entries


def validate_correction(value: dict[str, Any]) -> None:
    levels = value["corrected_uniqueness_levels"]
    need(value["schema"].endswith("aggregator-design-correction.v2")
         and value["formal_credit"] == 0
         and levels["candidate_pair"]["each_pair_has_exactly_one_assigned_terminal"]
             is True
         and levels["atom_pair_incidence"]["duplicate_incidence_key_forbidden"] is True
         and levels["atom_pair_incidence"]["one_atom_may_have_multiple_distinct_pair_incidences"]
             is True
         and levels["atom_pair_incidence"]["one_atom_may_therefore_observe_multiple_distinct_terminals"]
             is True
         and levels["atom"]["atom_terminal_uniqueness_required"] is False,
         "correction-v2 contract")


def validate_g2a_final(
    receipt: dict[str, Any], replay: dict[str, Any], invalidation: dict[str, Any],
    captures: dict[str, Capture]
) -> None:
    need(receipt["schema"]
             == "cm2.c27-independent.g2a-relative2d-primitive-totality-zero-credit-receipt.v2"
         and receipt["status"]
             == "PASS_DOUBLE_SEED_DUAL_IMPLEMENTATION_AND_15_ATTACKS__SCOPED_G2A_5264_CLOSED__POSITIVE_C19_AND_GLOBAL_THREE_TERMINAL_OPEN__ZERO_CREDIT"
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["double_seed"]["all_materialized_ledgers_byte_identical"] is True
         and receipt["double_seed"]["ledgers"]["theorem"]["contacts"]["row_count"] == 9_408
         and receipt["double_seed"]["ledgers"]["theorem"]["reverse_empty"]["row_count"] == 9_392
         and receipt["independent_verifier"]["imports_chain_or_shared_module"] is False
         and receipt["coherent_attacks"] == {
             "accepted": 0,
             "control_pass": True,
             "receipt_file_sha256": "55c504e9dc25f7b5d19078b4b2ddec0d9558941cef730d7d38bc9cc1a75861e7",
             "rejected": 15,
         }, "G2A final-v2 receipt")
    need(receipt["payload_manifest"]["file_sha256"]
             == captures["g2a_payload_manifest"].sha256
         and receipt["payload_manifest"]["entry_count"] == 37,
         "G2A receipt payload manifest")
    need(replay["schema"]
             == "cm2.c27-independent.g2a-relative2d-primitive-totality-terminal-replay.v2"
         and replay["status"]
             == "PASS_INDEPENDENT_ROOT_PAYLOAD_AND_SCOPED_RECEIPT_REPLAY__ZERO_CREDIT"
         and replay["receipt_file_sha256"] == captures["g2a_final_receipt"].sha256
         and replay["receipt_result_sha256"] == receipt["result_sha256"]
         and replay["payload_manifest_file_sha256"]
             == captures["g2a_payload_manifest"].sha256
         and replay["root_manifest_file_sha256"]
             == captures["g2a_root_manifest"].sha256
         and replay["payload_entry_count"] == 37
         and replay["global_three_terminal_unique_assignment"] is False
         and replay["formal_credit"] == 0,
         "G2A terminal replay")
    payload_entries = manifest_entries(captures["g2a_payload_manifest"].raw(),
                                       "G2A payload")
    root_entries = manifest_entries(captures["g2a_root_manifest"].raw(), "G2A root")
    need(len(payload_entries) == 37
         and len(root_entries) == 2
         and root_entries["payload_manifest.sha256"]
             == captures["g2a_payload_manifest"].sha256
         and root_entries["receipt.json"] == captures["g2a_final_receipt"].sha256,
         "G2A manifest closure")
    need(invalidation["schema"]
             == "cm2.c27-independent.g2a-relative2d.zero-credit-seal-invalidation.v1"
         and invalidation["status"] == "INVALIDATED_BY_POSTSEAL_SOURCE_CHANGE"
         and invalidation["invalidated_seal_path"]
             == ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final"
         and invalidation["replacement_seal_path"]
             == ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2"
         and invalidation["formal_credit"] == 0,
         "old G2A seal invalidation")


def validate_static(receipts: dict[str, dict[str, Any]]) -> None:
    strict = receipts["strict_volume_receipt"]
    lower = receipts["lower_contact_receipt"]
    c19c = receipts["c19c_receipt"]
    g2b = receipts["g2b_receipt"]
    need(strict["exact_census"]["all_component_strict_intersection_pair_count"]
             == 187_132
         and strict["exact_census"]["primitive_atom_count"] == 483_232
         and strict["formal_credit"] == 0,
         "strict-volume receipt")
    need(lower["lower_dimensional_candidate_pair_count"] == 5_783_708
         and lower["C26_role"]["full_rows_read"] == 691_424
         and lower["C26_role"]["absence_used_as_negative_geometry_theorem"] is False
         and lower["formal_credit"] == 0,
         "lower-contact/C26-open receipt")
    need(c19c["authority"]["direct_rule"]
             == "oriented [lower,upper) on internal faces"
         and c19c["formal_credit"] == 0,
         "C19C half-open receipt")
    need(g2b["G2B_closed_diagnostic"]["exact_positive"] == 9_408
         and g2b["G2B_closed_diagnostic"]["exact_empty"] == 9_392
         and g2b["formal_state_unchanged"]["formal_credit"] == 0,
         "G2B terminal receipt")


def validate_union_receipt(
    receipt: dict[str, Any], captures: dict[str, Capture]
) -> None:
    need(receipt["schema"]
             == "cm2.c27-independent.c24a-current-primitive-three-terminal-union-terminal-receipt.v1"
         and receipt["status"]
             == "PASS_SCOPED_101080_PAIR_UNION_DUAL_SEED_NO_IMPORT_18_ATTACKS__GLOBAL_ATOM_TOTALITY_OPEN__ZERO_CREDIT"
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["authority_scope"]["candidate_pair_count"] == 101_080
         and receipt["authority_scope"]["each_candidate_pair_exactly_one_terminal"]
             is True
         and receipt["authority_scope"]["G2A_alias_counted_as_second_pair"] is False
         and receipt["authority_scope"]["G2B_positive_terminal"]
             == "POSITIVE_VOLUME_CARRIERS"
         and receipt["independent_verifier"]["no_producer_import"] is True
         and receipt["coherent_attacks"]["attack_count"]
             == receipt["coherent_attacks"]["rejected"] == 18
         and receipt["coherent_attacks"]["accepted"] == 0,
         "101080 terminal receipt")
    ownership = receipt["root_input_capture"]["attestations"]["ownership_ledger"]
    need(ownership["sha256"] == captures["pair_ownership"].sha256
         and (ROOT / ownership["path"]).resolve() == captures["pair_ownership"].path,
         "union receipt ownership binding")
    entries = manifest_entries(captures["pair_union_manifest"].raw(), "pair union")
    receipt_relative = str(captures["pair_union_receipt"].path.relative_to(ROOT))
    need(entries[receipt_relative] == captures["pair_union_receipt"].sha256
         and entries[ownership["path"]] == captures["pair_ownership"].sha256,
         "pair union manifest closure")


def scan_pairs(capture: Capture) -> dict[str, Any]:
    seen: set[tuple[str, str]] = set()
    terminal = Counter()
    source = Counter()
    for ordinal, row in enumerate(capture.rows()):
        key = unordered(row["pair_key"], f"ownership:{ordinal}")
        need(key not in seen, f"ownership:{ordinal}:unique pair")
        seen.add(key)
        assigned = row["assigned_terminal"]
        need(assigned in {"SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
                          "POSITIVE_VOLUME_CARRIERS"}
             and row["formal_credit"] == 0,
             f"ownership:{ordinal}:terminal")
        authority = row["source_authority"]
        if authority == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":
            need(assigned == "POSITIVE_VOLUME_CARRIERS"
                 and type(row["G2A_diagnostic_alias_row_sha256"]) is str,
                 f"ownership:{ordinal}:C24A normalization")
        terminal[assigned] += 1
        source[authority] += 1
    need(len(seen) == 101_080
         and terminal == {"SIGNED_BOUNDARY_FACES": 25_452,
                          "COMPLETE_BOUNDARY_FACES": 10_688,
                          "POSITIVE_VOLUME_CARRIERS": 64_940}
         and source == {"CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER": 91_672,
                        "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER": 9_408},
         "pair authority reconstruction")
    return {"pair_count": len(seen), "terminal_census": dict(sorted(terminal.items())),
            "source_census": dict(sorted(source.items())),
            "each_candidate_pair_exactly_one_terminal": True,
            "G2A_alias_counted_as_second_pair": False}


def gap(slot: str, status: str, blocking: bool, evidence: dict[str, Any]) -> dict[str, Any]:
    return closed({
        "schema": "cm2.c27-independent.primitive-twenty-family-v5-authority-gap.row.v2",
        "authority_slot": slot,
        "authority_status": status,
        "gate_blocking": blocking,
        "evidence": evidence,
        "formal_credit": 0,
    })


def run(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    output = Path(args.out_dir)
    need(not output.exists(), "fresh output directory")
    required = {
        "correction_v2": (args.correction_v2, args.correction_v2_sha256),
        "strict_volume_receipt": (args.strict_volume_receipt,
                                  args.strict_volume_receipt_sha256),
        "lower_contact_receipt": (args.lower_contact_receipt,
                                  args.lower_contact_receipt_sha256),
        "c19c_receipt": (args.c19c_receipt, args.c19c_receipt_sha256),
        "g2a_final_receipt": (args.g2a_final_receipt, args.g2a_final_receipt_sha256),
        "g2a_payload_manifest": (args.g2a_payload_manifest,
                                 args.g2a_payload_manifest_sha256),
        "g2a_root_manifest": (args.g2a_root_manifest, args.g2a_root_manifest_sha256),
        "g2a_terminal_replay": (args.g2a_terminal_replay,
                                args.g2a_terminal_replay_sha256),
        "g2a_invalidation_notice": (args.g2a_invalidation_notice,
                                    args.g2a_invalidation_notice_sha256),
        "g2b_receipt": (args.g2b_receipt, args.g2b_receipt_sha256),
        "pair_union_receipt": (args.pair_union_receipt,
                               args.pair_union_receipt_sha256),
        "pair_union_manifest": (args.pair_union_manifest,
                                args.pair_union_manifest_sha256),
        "pair_ownership": (args.pair_ownership, args.pair_ownership_sha256),
    }
    captures: dict[str, Capture] = {}
    try:
        for label, (path, sha) in required.items():
            captures[label] = Capture.open(label, Path(path), sha)
        for label, path, sha in (
            ("full_atom_formal_receipt", args.full_atom_formal_receipt,
             args.full_atom_formal_receipt_sha256),
            ("c26_formal_receipt", args.c26_formal_receipt,
             args.c26_formal_receipt_sha256),
        ):
            need((path is None) is (sha is None), label + ":path/sha pair")
            if path is not None:
                captures[label] = Capture.open(label, Path(path), sha)

        correction = captures["correction_v2"].document("design_sha256", True)
        validate_correction(correction)
        static = {
            label: captures[label].document("receipt_sha256", False)
            for label in ("strict_volume_receipt", "lower_contact_receipt",
                          "c19c_receipt")
        }
        static["g2b_receipt"] = captures["g2b_receipt"].document("result_sha256", True)
        validate_static(static)
        g2a_receipt = captures["g2a_final_receipt"].document("result_sha256", True)
        g2a_replay = captures["g2a_terminal_replay"].document("result_sha256", True)
        invalidation = captures["g2a_invalidation_notice"].document(None, False)
        validate_g2a_final(g2a_receipt, g2a_replay, invalidation, captures)
        union_receipt = captures["pair_union_receipt"].document("result_sha256", True)
        validate_union_receipt(union_receipt, captures)
        pair_summary = scan_pairs(captures["pair_ownership"])

        full_ready = "full_atom_formal_receipt" in captures
        c26_ready = "c26_formal_receipt" in captures
        # Formal schemas are intentionally strict.  A seed result alone cannot
        # satisfy either slot.
        if full_ready:
            full = captures["full_atom_formal_receipt"].document("result_sha256", True)
            need(full["schema"]
                     == "cm2.c27-independent.full-union-101080-on-483232-atom-incidence-terminal-receipt.v1"
                 and full["formal_credit"] == 0
                 and full["dual_seed_byte_identical"] is True
                 and full["independent_verification_passed"] is True
                 and full["coherent_attacks_all_rejected"] is True
                 and full["atom_denominator"] == 483_232
                 and full["expanded_atom_pair_incidences"] == 206_632
                 and full["incident_atoms"] == 62_768
                 and full["exact_complement_atoms"] == 420_464
                 and full["multi_terminal_incident_atoms"] == 3_896,
                 "full atom formal receipt")
        if c26_ready:
            c26 = captures["c26_formal_receipt"].document("result_sha256", True)
            need(c26["schema"]
                     == "cm2.c27-independent.c26-primitive-exact-contact-absence-terminal-receipt.v1"
                 and c26["formal_credit"] == 0
                 and c26["dual_seed_byte_identical"] is True
                 and c26["independent_verification_passed"] is True
                 and c26["coherent_attacks_all_rejected"] is True
                 and c26["C26_rows_enumerated"] == 691_424
                 and c26["explicit_absence_theorem"] is True
                 and c26["absence_inferred_from_missing_rows_or_volume"] is False,
                 "C26 formal receipt")

        rows = [
            gap("CORRECTION_V2_MANY_TO_MANY_ATOM_CONTRACT", "PRESENT_VALID", False,
                {"design_sha256": correction["design_sha256"]}),
            gap("SAME_CHART_STRICT_VOLUME_187132", "PRESENT_VALID", False,
                {"primitive_row_count": 187_132}),
            gap("SAME_CHART_LOWER_EXACT_CONTACT_5783708",
                "PRESENT_VALID_C26_ABSENCE_NOT_IMPLIED", False,
                {"primitive_row_count": 5_783_708, "C26_rows_read": 691_424,
                 "C26_absence_used_as_negative_theorem": False}),
            gap("C19C_ENDPOINT_V3_HALF_OPEN", "PRESENT_VALID", False,
                {"direct_rule": "oriented [lower,upper) on internal faces"}),
            gap("G2A_FINAL_V2_SEAL_AND_TERMINAL_REPLAY", "PRESENT_VALID", False,
                {"receipt_file_sha256": captures["g2a_final_receipt"].sha256,
                 "payload_manifest_file_sha256": captures["g2a_payload_manifest"].sha256,
                 "root_manifest_file_sha256": captures["g2a_root_manifest"].sha256,
                 "terminal_replay_file_sha256": captures["g2a_terminal_replay"].sha256,
                 "old_invalidated_seal_rejected": True}),
            gap("G2B_TERMINAL_AUTHORITY", "PRESENT_VALID_ZERO_CREDIT", False,
                {"positive_keys": 9_408, "empty_keys": 9_392}),
            gap("SEALED_SCOPED_PAIR_UNION_101080", "PRESENT_VALID", False,
                {**pair_summary,
                 "terminal_receipt_file_sha256": captures["pair_union_receipt"].sha256,
                 "manifest_file_sha256": captures["pair_union_manifest"].sha256,
                 "no_import_verification_bound": True,
                 "coherent_attacks_18_of_18_rejected": True}),
            gap("FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT",
                "PRESENT_VALID" if full_ready else "MISSING_FORMAL_AUTHORITY",
                not full_ready,
                ({"atom_denominator": 483_232, "expanded_incidences": 206_632,
                  "incident_atoms": 62_768, "exact_complement_atoms": 420_464,
                  "multi_terminal_atoms": 3_896}
                 if full_ready else {
                     "seed_result_is_not_formal_authority": True,
                     "required_exact_formal_census": {
                         "current_exact_expanded_incidences": 197_224,
                         "C24A_G2B_target_incidences": 9_408,
                         "full_expanded_incidences": 206_632,
                         "incident_atoms": 62_768,
                         "exact_complement_atoms": 420_464,
                         "multi_terminal_atoms": 3_896,
                     },
                     "rejected_legacy_coarse_current_only_contract": {
                         "expanded_incidences": 197_408,
                         "complement_atoms": 420_992,
                         "reason": "POSITIVE_OWNER_ALL_ATOMS_COARSE_FANOUT_PLUS184",
                     },
                     "required_authority": "DUAL_SEED_INDEPENDENT_ATTACK_SEALED_FINAL_RECEIPT",
                 })),
            gap("C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT",
                "PRESENT_VALID" if c26_ready else "MISSING_FORMAL_AUTHORITY",
                not c26_ready,
                ({"C26_rows_enumerated": 691_424, "explicit_absence_theorem": True}
                 if c26_ready else {
                     "C26_rows_known_in_lower_authority": 691_424,
                     "missing_rows_or_volume_may_not_imply_absence": True,
                     "required_authority": "SOURCE_FACTORIZED_DUAL_SEED_INDEPENDENT_ATTACK_SEALED_THEOREM",
                 })),
        ]
        missing = [row["authority_slot"] for row in rows if row["gate_blocking"]]
        accepted = not missing
        output.mkdir(parents=True, exist_ok=False)
        gap_descriptor = write_rows(output / "authority_gap_ledger_v2.jsonl.gz", rows)
        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-fail-closed-preflight.v2",
            "status": ("PASS_ALL_FORMAL_AUTHORITIES_PRESENT__ZERO_CREDIT" if accepted
                       else "REJECT_MISSING_FULL_ATOM_AND_OR_C26_FORMAL_RECEIPT__ZERO_CREDIT"),
            "decision": "SCOPED_READY_ZERO_CREDIT" if accepted else "REJECT",
            "intended_process_exit_code": 0 if accepted else 2,
            "invocation_seed": args.seed,
            "authority_hardening": {
                "G2A_final_v2_receipt_bound": True,
                "G2A_payload_and_root_manifests_bound": True,
                "G2A_terminal_replay_bound": True,
                "G2A_old_invalidated_seal_rejected": True,
                "pair_union_terminal_receipt_bound": True,
                "pair_union_no_import_verification_bound": True,
                "pair_union_18_of_18_attacks_bound": True,
                "raw_G2A_theorem_result_alone_is_authority": False,
                "raw_pair_union_result_alone_is_authority": False,
                "full_atom_seed_result_alone_is_authority": False,
            },
            "corrected_contract": {
                "each_candidate_pair_exactly_one_terminal": True,
                "atom_pair_incidence_key_unique": True,
                "atom_exact_incidence_set_or_empty_complement": True,
                "atom_multi_pair_allowed": True,
                "atom_multi_terminal_allowed": True,
                "atom_single_pair_or_terminal_constraint_imposed": False,
            },
            "pair_authority_reconstruction": pair_summary,
            "authority_slot_census": {"total": len(rows),
                                      "present": len(rows) - len(missing),
                                      "missing_or_blocking": len(missing)},
            "blocking_authority_slots": missing,
            "gap_ledger": gap_descriptor,
            "forbidden_input_governance": {
                "old_C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False,
                "C29_imported_or_read": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "old_invalidated_G2A_seal_accepted": False,
                "legacy_coarse_current_atom_contract_accepted": False,
                "producer_module_imported": False,
            },
            "global_gate": {
                "primitive_support_atom_denominator": 483_232,
                "pair_authority_row_count": 101_080,
                "full_atom_formal_receipt_present": full_ready,
                "C26_formal_receipt_present": c26_ready,
                "primitive_twenty_family_totality_proved": accepted,
                "decision": "ZERO_CREDIT_SCOPED_READY" if accepted else "FAIL_CLOSED_REJECT",
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": {"C27_transition_totality": 0,
                                    "C28_pair_routing": 0,
                                    "C29_physical_maximality": 0,
                                    "CM2": "NO-GO_FOR_CLAIM"},
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())},
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items()
            if key not in {"invocation_seed", "root_input_capture"}
        })
        result["result_sha256"] = digest(result)
        (output / "preflight_result_v2.json").write_bytes(canonical(result) + b"\n")
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
        "correction-v2", "strict-volume-receipt", "lower-contact-receipt",
        "c19c-receipt", "g2a-final-receipt", "g2a-payload-manifest",
        "g2a-root-manifest", "g2a-terminal-replay", "g2a-invalidation-notice",
        "g2b-receipt", "pair-union-receipt", "pair-union-manifest",
        "pair-ownership",
    ):
        add_required(parser, name)
    parser.add_argument("--full-atom-formal-receipt")
    parser.add_argument("--full-atom-formal-receipt-sha256")
    parser.add_argument("--c26-formal-receipt")
    parser.add_argument("--c26-formal-receipt-sha256")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result, code = run(args)
    except (Failure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print("REJECT_INVALID_INPUT:" + str(error))
        return 2
    print(canonical({"status": result["status"], "decision": result["decision"],
                     "blocking_authority_slots": result["blocking_authority_slots"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
