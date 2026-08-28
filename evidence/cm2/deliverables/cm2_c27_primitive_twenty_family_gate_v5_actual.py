#!/usr/bin/env python3
"""Fresh actual primitive twenty-family v5 gate.

This aggregator never rewrites the sealed truthful-reject preflight.  It can
only pass from a fresh output directory after consuming that cold-replayed
baseline plus separately cold-replayed full-atom and C26 scoped authorities.
All conclusions remain zero-credit and do not authorize C27/C28/C29 or CM2.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        require(type(expected) is str and len(expected) == 64, label + ":expected sha")
        resolved = path.resolve()
        fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            require(observed == expected, label + ":sha256")
            require(fingerprint(os.fstat(fd)) == fingerprint(before),
                    label + ":hash fstat")
            return cls(label, resolved, fd, fingerprint(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        require(fingerprint(os.fstat(self.fd)) == self.initial,
                self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.stable("raw")
        return b"".join(pieces)

    def document(self, closure_key: str,
                 canonical_file: bool = False) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        require(type(value) is dict, self.label + ":document")
        if canonical_file:
            require(encode(value) + b"\n" == raw, self.label + ":canonical")
        body = dict(value)
        claim = body.pop(closure_key, None)
        require(type(claim) is str and claim == object_hash(body),
                self.label + ":closure")
        return value

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {"path": rendered, "sha256": self.sha256, "size": self.initial[2],
                "stat_fingerprint": list(self.initial), "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def manifest(raw: bytes, label: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for ordinal, line in enumerate(raw.decode("ascii").splitlines()):
        pieces = line.split("  ", 1)
        require(len(pieces) == 2 and len(pieces[0]) == 64,
                f"{label}:{ordinal}:line")
        sha, path = pieces
        require(path not in entries, f"{label}:{ordinal}:duplicate")
        entries[path] = sha
    return entries


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_preflight(documents: dict[str, dict[str, Any]],
                       captures: dict[str, Capture]) -> None:
    receipt = documents["preflight_receipt"]
    replay = documents["preflight_terminal_replay"]
    payload_entries = manifest(captures["preflight_payload_manifest"].raw(),
                               "preflight payload")
    root_entries = manifest(captures["preflight_root_manifest"].raw(),
                            "preflight root")
    blockers = {
        "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT",
        "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT",
    }
    require(receipt["schema"]
            == "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-v2-zero-credit-receipt.v1"
            and receipt["status"]
            == "PASS_SEALED_TRUTHFUL_REJECT_PREFLIGHT_VERIFIER_AND_18_ATTACKS__ZERO_CREDIT"
            and receipt["preflight_execution"] == {
                "decision": "REJECT", "intended_exit_code": 2,
                "observed_exit_code": 2, "observed_matches_intended": True,
                "truthful_reject": True}
            and set(receipt["blocking_authority_slots"]) == blockers
            and receipt["global_gate"]["primitive_twenty_family_totality_proved"]
                is False
            and receipt["global_gate"]["future_closure_requires_fresh_actual_gate_run"]
                is True
            and receipt["global_gate"]["sealed_preflight_may_not_be_rewritten"]
                is True
            and receipt["formal_credit"] == 0
            and receipt["manifest_authorized"] is False,
            "sealed truthful-reject preflight")
    require(len(payload_entries) == receipt["payload_manifest"]["entry_count"] == 22
            and captures["preflight_payload_manifest"].sha256
                == receipt["payload_manifest"]["file_sha256"]
            and root_entries == {
                "payload_manifest.sha256": captures["preflight_payload_manifest"].sha256,
                "receipt.json": captures["preflight_receipt"].sha256,
            }, "preflight manifest closure")
    require(replay["schema"]
            == "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-v2-terminal-replay.v1"
            and replay["status"]
            == "PASS_COLD_ROOT_PAYLOAD_AND_TRUTHFUL_REJECT_REPLAY__ZERO_CREDIT"
            and replay["receipt_file_sha256"] == captures["preflight_receipt"].sha256
            and replay["receipt_result_sha256"] == receipt["result_sha256"]
            and replay["payload_manifest_file_sha256"]
                == captures["preflight_payload_manifest"].sha256
            and replay["root_manifest_file_sha256"]
                == captures["preflight_root_manifest"].sha256
            and replay["preflight_intended_and_observed_exit_code"] == 2
            and set(replay["blocking_authority_slots"]) == blockers
            and replay["future_closure_requires_fresh_actual_gate_run"] is True
            and replay["formal_credit"] == 0
            and replay["manifest_authorized"] is False,
            "preflight cold replay")


def validate_full_atom(documents: dict[str, dict[str, Any]],
                       captures: dict[str, Capture]) -> None:
    receipt = documents["full_atom_receipt"]
    cold = documents["full_atom_cold_receipt"]
    verification = documents["full_atom_cold_verification"]
    base_entries = manifest(captures["full_atom_manifest"].raw(), "full atom base")
    cold_entries = manifest(captures["full_atom_cold_manifest"].raw(),
                            "full atom cold")
    receipt_path = relative(captures["full_atom_receipt"].path)
    require(receipt["schema"]
            == "cm2.c27-independent.full-union-101080-on-483232.atom-terminal-zero-credit.v3"
            and receipt["status"]
            == "PASS_SCOPED_THREE_TERMINAL_FULL_UNION_ATOM_CONTRACT_DUAL_SEED_INDEPENDENT_ATTACK_SEALED__ZERO_FORMAL_CREDIT"
            and receipt["scope"]
            == "THREE_TERMINAL_PAIR_OWNERSHIP_MATERIALIZED_AS_EXACT_ATOM_INCIDENCE_OR_COMPLEMENT_ONLY"
            and receipt["formal_credit"] == 0
            and receipt["manifest_authorized"] is False
            and receipt["source_W_transition_authorized"] is False,
            "full atom base receipt")
    exact = receipt["exact_atom_contract"]
    require(exact["atoms"] == 483_232
            and exact["incident_atoms"] == 62_768
            and exact["exact_complement_atoms"] == 420_464
            and exact["expanded_atom_route_incidences"] == 206_632
            and exact["multi_terminal_incident_atoms"] == 3_896
            and exact["binding_census"] == {
                "EXACT_C24A_G2B_C22_TARGET_ATOM": 9_408,
                "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS": 111_064,
                "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE": 86_160}
            and receipt["pair_union"]["pairs"] == 101_080
            and receipt["pair_union"]["G2A_alias_independent_candidate_count"] == 0
            and receipt["dual_seed"]["ledgers_byte_identical"] is True
            and receipt["dual_seed"]["ledger_sha256"]
                == "9b642b40fea1bbae5121ca9fcc43461795190c92f38753d41ff7d0e4e358b114"
            and receipt["coherent_attacks"] == {
                "accepted": 0, "rejected": 54,
                "required_regression_attacks": [
                    "positive_coarse_owner_fanout_regression",
                    "result_coarse_positive_fanout_plus_184",
                    "result_coarse_positive_terminal_set_regression",
                    "result_remove_G2B_528_new_incident_atoms"]},
            "full atom exact contract")
    require(len(base_entries) == 25
            and base_entries[receipt_path] == captures["full_atom_receipt"].sha256,
            "full atom base manifest")
    require(verification["schema"]
            == "cm2.c27-independent.full-union-atom-terminal-manifest-verification.v1"
            and verification["status"]
            == "PASS_MANIFEST_FIRST_TERMINAL_REPLAY__DUAL_LEDGER_BYTES_AND_SCOPED_ZERO_CREDIT_CONTRACT_VERIFIED"
            and verification["base_manifest_sha256"]
                == captures["full_atom_manifest"].sha256
            and verification["base_receipt_file_sha256"]
                == captures["full_atom_receipt"].sha256
            and verification["base_receipt_sha256"] == receipt["receipt_sha256"]
            and verification["primitive_atoms"] == 483_232
            and verification["pair_routes"] == 101_080
            and verification["expanded_atom_route_incidences"] == 206_632
            and verification["incident_atoms"] == 62_768
            and verification["exact_complement_atoms"] == 420_464
            and verification["coherent_attacks_rejected"] == 54
            and verification["formal_credit"] == 0
            and verification["manifest_authorized"] is False,
            "full atom cold verification")
    require(cold["schema"]
            == "cm2.c27-independent.full-union-atom.postpublication-cold-terminal-replay-receipt.v1"
            and cold["status"]
            == "PASS_COLD_POSTPUBLICATION_MANIFEST_FIRST_TERMINAL_REPLAY__PRE_POST_SHA_STAT_IDENTICAL__ZERO_CREDIT"
            and cold["base_manifest_sha256"] == captures["full_atom_manifest"].sha256
            and cold["base_receipt_file_sha256"] == captures["full_atom_receipt"].sha256
            and cold["verification_file_sha256"]
                == captures["full_atom_cold_verification"].sha256
            and cold["verification_sha256"] == verification["verification_sha256"]
            and cold["manifest_first_terminal_replay"] is True
            and cold["numeric_exit"] == 0 and cold["signal"] is None
            and cold["stderr_empty"] is True
            and cold["pre_post_sha256_identical"] is True
            and cold["pre_post_stat_identical"] is True
            and cold["formal_credit"] == 0
            and cold["manifest_authorized"] is False
            and cold["source_W_transition_authorized"] is False,
            "full atom cold terminal receipt")
    require(len(cold_entries) == 6
            and cold_entries[relative(captures["full_atom_manifest"].path)]
                == captures["full_atom_manifest"].sha256
            and cold_entries[relative(captures["full_atom_receipt"].path)]
                == captures["full_atom_receipt"].sha256
            and cold_entries[relative(captures["full_atom_cold_receipt"].path)]
                == captures["full_atom_cold_receipt"].sha256
            and cold_entries[relative(captures["full_atom_cold_verification"].path)]
                == captures["full_atom_cold_verification"].sha256,
            "full atom cold manifest")


def validate_c26(documents: dict[str, dict[str, Any]],
                 captures: dict[str, Capture]) -> None:
    receipt = documents["c26_receipt"]
    replay = documents["c26_terminal_replay"]
    base_entries = manifest(captures["c26_manifest"].raw(), "C26 base")
    terminal_entries = manifest(captures["c26_terminal_manifest"].raw(),
                                "C26 terminal")
    require(receipt["schema"]
            == "cm2.c26-independent.no-new-geometry-from-c26-feature-rows-zero-credit-receipt.v1"
            and receipt["C26_feature_rows"] == 691_424
            and receipt["mutually_exclusive_disposition_sum"] == 691_424
            and receipt["C26_direct_support_carriers"] == 0
            and receipt["scoped_unresolved"] == 0
            and receipt["A1_A2_feature_only_primitive_owner_rows"] == 80_092
            and receipt["R1_direct_C22A_rows"] == 295_340
            and receipt["R2_C22A_union_alias_rows"] == 295_336
            and receipt["graph_feature_rows"] == 20_656
            and receipt["graph_feature_row_disjoint_buckets"] == {
                "G1_C10_definition_handoff_by_graph_id": 5_264,
                "G2A_C24A_scoped_route": 5_264,
                "G2B_C24A_positive": 9_408,
                "G2B_C24A_complement": 552,
                "G2B_C24B_exact_empty": 168}
            and receipt["graph_geometry_double_count"] == 0
            and receipt["six_kernel_primitive_atoms"] == 483_232
            and receipt["same_chart_strict_dim3_pairs"] == 187_132
            and receipt["same_chart_lower_dim012_pairs"] == 5_783_708
            and receipt["same_chart_lower_legal_witnesses"] == 0,
            "C26 exact source-factorized census")
    require(receipt["authority_scope"] == {
                "NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS": True,
                "fills_v5_C26_absence_slot": True,
                "global_three_terminal_totality_and_unique_assignment": False,
                "twenty_family_gate_closed_by_this_receipt": False,
                "C26_absence_used_as_negative_geometry_theorem": False}
            and receipt["formal_credit"] == 0
            and receipt["manifest_authorized"] is False
            and receipt["source_W_transition_authorized"] is False,
            "C26 scoped-only authority")
    # Exact final replay field names are deliberately required.  This source
    # remains fail-closed until the separately published C26 terminal bundle
    # supplies these bindings; no raw producer or base receipt can pass alone.
    require(replay["schema"]
            == "cm2.c26-independent.no-new-geometry-from-c26-feature-rows-terminal-replay-receipt.v1"
            and replay["status"].startswith("PASS_")
            and replay["base_receipt_file_sha256"] == captures["c26_receipt"].sha256
            and replay["base_manifest_file_sha256"] == captures["c26_manifest"].sha256
            and replay["formal_credit"] == 0
            and replay["manifest_authorized"] is False
            and replay["source_W_transition_authorized"] is False,
            "C26 cold terminal replay")
    require(base_entries[relative(captures["c26_receipt"].path)]
                == captures["c26_receipt"].sha256
            and terminal_entries[relative(captures["c26_receipt"].path)]
                == captures["c26_receipt"].sha256
            and terminal_entries[relative(captures["c26_manifest"].path)]
                == captures["c26_manifest"].sha256
            and terminal_entries[relative(captures["c26_terminal_replay"].path)]
                == captures["c26_terminal_replay"].sha256,
            "C26 manifest and replay closure")


def run(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_dir)
    require(not output.exists(), "fresh actual-gate output directory")
    labels = (
        "preflight_receipt", "preflight_payload_manifest",
        "preflight_root_manifest", "preflight_terminal_replay",
        "full_atom_receipt", "full_atom_manifest", "full_atom_cold_receipt",
        "full_atom_cold_manifest", "full_atom_cold_verification",
        "c26_receipt", "c26_manifest", "c26_terminal_replay",
        "c26_terminal_manifest",
    )
    captures: dict[str, Capture] = {}
    try:
        for label in labels:
            captures[label] = Capture.open(label, Path(getattr(args, label)),
                                           getattr(args, label + "_sha256"))
        documents = {
            "preflight_receipt": captures["preflight_receipt"].document(
                "result_sha256", True),
            "preflight_terminal_replay":
                captures["preflight_terminal_replay"].document("result_sha256", True),
            "full_atom_receipt": captures["full_atom_receipt"].document(
                "receipt_sha256"),
            "full_atom_cold_receipt": captures["full_atom_cold_receipt"].document(
                "receipt_sha256"),
            "full_atom_cold_verification":
                captures["full_atom_cold_verification"].document(
                    "verification_sha256"),
            "c26_receipt": captures["c26_receipt"].document("receipt_sha256"),
            "c26_terminal_replay": captures["c26_terminal_replay"].document(
                "receipt_sha256"),
        }
        validate_preflight(documents, captures)
        validate_full_atom(documents, captures)
        validate_c26(documents, captures)
        output.mkdir(parents=True, exist_ok=False)
        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.v1",
            "status": "PASS_ALL_PRIMITIVE_V5_AUTHORITIES_PRESENT_AND_COLD_REPLAYED__ZERO_CREDIT",
            "decision": "PRIMITIVE_TWENTY_FAMILY_TOTALITY_SCOPED_READY_ZERO_CREDIT",
            "invocation_seed": args.seed,
            "append_only_transition": {
                "sealed_truthful_reject_preflight_preserved": True,
                "fresh_actual_gate_run": True,
                "formerly_blocking_slots_closed_by_new_formal_receipts": [
                    "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT",
                    "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT"],
            },
            "authority_slot_census": {"total": 9, "present": 9,
                                      "missing_or_blocking": 0},
            "three_terminal_pair_authority": {
                "candidate_pairs": 101_080,
                "each_pair_exactly_one_terminal": True,
                "G2A_alias_counted_as_second_pair": False,
                "terminal_census": {"SIGNED_BOUNDARY_FACES": 25_452,
                                    "COMPLETE_BOUNDARY_FACES": 10_688,
                                    "POSITIVE_VOLUME_CARRIERS": 64_940}},
            "atom_incidence_authority": {
                "atoms": 483_232, "incident_atoms": 62_768,
                "exact_complement_atoms": 420_464,
                "expanded_atom_pair_incidences": 206_632,
                "multi_terminal_incident_atoms": 3_896,
                "atom_multi_pair_allowed": True,
                "atom_multi_terminal_allowed": True,
                "atom_single_pair_or_terminal_constraint_imposed": False,
                "legacy_coarse_current_contract_accepted": False},
            "C26_scoped_absence_authority": {
                "C26_feature_rows": 691_424,
                "C26_direct_support_carriers": 0,
                "scoped_unresolved": 0,
                "fills_only_C26_absence_slot": True,
                "used_alone_as_global_totality": False},
            "global_gate": {
                "primitive_twenty_family_totality_proved": True,
                "full_atom_formal_receipt_present_and_cold_replayed": True,
                "C26_formal_receipt_present_and_cold_replayed": True,
                "decision": "SCOPED_READY_ZERO_CREDIT"},
            "forbidden_input_governance": {
                "old_C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False,
                "C29_imported_or_read": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "old_invalidated_G2A_seal_accepted": False,
                "legacy_coarse_current_atom_contract_accepted": False,
                "producer_module_imported": False},
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": {"C27_transition_totality": 0,
                                    "C28_pair_routing": 0,
                                    "C29_physical_maximality": 0,
                                    "Source_W_formal_remainder": 80,
                                    "CM2": "NO-GO_FOR_CLAIM"},
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())}},
        }
        result = dict(body)
        result["semantic_projection_sha256"] = object_hash({
            key: value for key, value in body.items()
            if key not in {"invocation_seed", "root_input_capture"}})
        result["result_sha256"] = object_hash(result)
        (output / "actual_gate_result.json").write_bytes(encode(result) + b"\n")
        return result
    finally:
        for capture in captures.values():
            capture.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "preflight-receipt", "preflight-payload-manifest",
        "preflight-root-manifest", "preflight-terminal-replay",
        "full-atom-receipt", "full-atom-manifest", "full-atom-cold-receipt",
        "full-atom-cold-manifest", "full-atom-cold-verification",
        "c26-receipt", "c26-manifest", "c26-terminal-replay",
        "c26-terminal-manifest",
    ):
        add_input(parser, name)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    try:
        result = run(args)
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": result["status"], "decision": result["decision"],
                  "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
