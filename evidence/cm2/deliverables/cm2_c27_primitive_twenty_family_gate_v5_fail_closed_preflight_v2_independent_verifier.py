#!/usr/bin/env python3
"""No-import verifier for the authority-hardened primitive v5 preflight v2."""

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
from typing import Any, Iterator


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


def row_closure(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    require(type(claim) is str and claim == object_hash(body), label + ":closure")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class View:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "View":
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

    def document(self, closure_key: str | None,
                 canonical_file: bool = False) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        require(type(value) is dict, self.label + ":document")
        if canonical_file:
            require(encode(value) + b"\n" == raw, self.label + ":canonical")
        if closure_key is not None:
            body = dict(value)
            claim = body.pop(closure_key, None)
            require(type(claim) is str and claim == object_hash(body),
                    self.label + ":document closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    require(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    require(type(row) is dict and encode(row) == payload,
                            f"{self.label}:{ordinal}:canonical")
                    row_closure(row, f"{self.label}:{ordinal}")
                    yield row
        self.stable("rows")

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


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def manifest(raw: bytes, label: str) -> dict[str, str]:
    answer: dict[str, str] = {}
    for ordinal, line in enumerate(raw.decode("ascii").splitlines()):
        pieces = line.split("  ", 1)
        require(len(pieces) == 2 and len(pieces[0]) == 64,
                f"{label}:{ordinal}:line")
        sha, path = pieces
        require(path not in answer, f"{label}:{ordinal}:duplicate")
        answer[path] = sha
    return answer


def pair_key(value: Any, label: str) -> tuple[str, str]:
    require(type(value) is list and len(value) == 2
            and all(type(item) is str for item in value) and value[0] != value[1],
            label + ":pair")
    return tuple(sorted(value))


def acquire(args: argparse.Namespace) -> dict[str, View]:
    labels = (
        "correction_v2", "strict_volume_receipt", "lower_contact_receipt",
        "c19c_receipt", "g2a_final_receipt", "g2a_payload_manifest",
        "g2a_root_manifest", "g2a_terminal_replay", "g2a_invalidation_notice",
        "g2b_receipt", "pair_union_receipt", "pair_union_manifest",
        "pair_ownership", "preflight_result", "gap_ledger",
    )
    return {
        label: View.open(label, Path(getattr(args, label)),
                         getattr(args, label + "_sha256"))
        for label in labels
    }


def verify_preflight(preflight: dict[str, Any], gaps: dict[str, dict[str, Any]],
                     gap_sequence: str, views: dict[str, View]) -> None:
    expected_present = {
        "CORRECTION_V2_MANY_TO_MANY_ATOM_CONTRACT",
        "SAME_CHART_STRICT_VOLUME_187132",
        "SAME_CHART_LOWER_EXACT_CONTACT_5783708",
        "C19C_ENDPOINT_V3_HALF_OPEN",
        "G2A_FINAL_V2_SEAL_AND_TERMINAL_REPLAY",
        "G2B_TERMINAL_AUTHORITY",
        "SEALED_SCOPED_PAIR_UNION_101080",
    }
    expected_missing = {
        "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT",
        "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT",
    }
    require(set(gaps) == expected_present | expected_missing,
            "exact authority slot universe")
    require(all(gaps[name]["gate_blocking"] is False for name in expected_present)
            and all(gaps[name]["gate_blocking"] is True
                    and gaps[name]["authority_status"] == "MISSING_FORMAL_AUTHORITY"
                    for name in expected_missing), "exact gap partition")
    expected_pair = {
        "G2A_alias_counted_as_second_pair": False,
        "each_candidate_pair_exactly_one_terminal": True,
        "pair_count": 101_080,
        "source_census": {
            "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER": 9_408,
            "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER": 91_672,
        },
        "terminal_census": {
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 64_940,
            "SIGNED_BOUNDARY_FACES": 25_452,
        },
    }
    expected_full_evidence = {
        "rejected_legacy_coarse_current_only_contract": {
            "complement_atoms": 420_992,
            "expanded_incidences": 197_408,
            "reason": "POSITIVE_OWNER_ALL_ATOMS_COARSE_FANOUT_PLUS184",
        },
        "required_authority": "DUAL_SEED_INDEPENDENT_ATTACK_SEALED_FINAL_RECEIPT",
        "required_exact_formal_census": {
            "C24A_G2B_target_incidences": 9_408,
            "current_exact_expanded_incidences": 197_224,
            "exact_complement_atoms": 420_464,
            "full_expanded_incidences": 206_632,
            "incident_atoms": 62_768,
            "multi_terminal_atoms": 3_896,
        },
        "seed_result_is_not_formal_authority": True,
    }
    require(gaps["CORRECTION_V2_MANY_TO_MANY_ATOM_CONTRACT"]["evidence"]
            == {"design_sha256": "6baa40703f55e9d1df2855c8d2f2f8cce6ccd8042177d39ebb46713baae2fdc1"}
            and gaps["SAME_CHART_STRICT_VOLUME_187132"]["evidence"]
            == {"primitive_row_count": 187_132}
            and gaps["SAME_CHART_LOWER_EXACT_CONTACT_5783708"]["evidence"]
            == {"C26_absence_used_as_negative_theorem": False,
                "C26_rows_read": 691_424, "primitive_row_count": 5_783_708}
            and gaps["C19C_ENDPOINT_V3_HALF_OPEN"]["evidence"]
            == {"direct_rule": "oriented [lower,upper) on internal faces"}
            and gaps["G2B_TERMINAL_AUTHORITY"]["evidence"]
            == {"empty_keys": 9_392, "positive_keys": 9_408}
            and gaps["FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT"]["evidence"]
            == expected_full_evidence
            and gaps["C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT"]["evidence"]
            == {"C26_rows_known_in_lower_authority": 691_424,
                "missing_rows_or_volume_may_not_imply_absence": True,
                "required_authority":
                    "SOURCE_FACTORIZED_DUAL_SEED_INDEPENDENT_ATTACK_SEALED_THEOREM"},
            "exact gap evidence")
    g2a_evidence = gaps["G2A_FINAL_V2_SEAL_AND_TERMINAL_REPLAY"]["evidence"]
    require(g2a_evidence == {
        "old_invalidated_seal_rejected": True,
        "payload_manifest_file_sha256": views["g2a_payload_manifest"].sha256,
        "receipt_file_sha256": views["g2a_final_receipt"].sha256,
        "root_manifest_file_sha256": views["g2a_root_manifest"].sha256,
        "terminal_replay_file_sha256": views["g2a_terminal_replay"].sha256,
    }, "G2A gap evidence")
    union_evidence = gaps["SEALED_SCOPED_PAIR_UNION_101080"]["evidence"]
    require(union_evidence == {**expected_pair,
        "coherent_attacks_18_of_18_rejected": True,
        "manifest_file_sha256": views["pair_union_manifest"].sha256,
        "no_import_verification_bound": True,
        "terminal_receipt_file_sha256": views["pair_union_receipt"].sha256,
    }, "pair union gap evidence")

    require(preflight["schema"]
            == "cm2.c27-independent.primitive-twenty-family-gate-v5-fail-closed-preflight.v2"
            and preflight["status"]
            == "REJECT_MISSING_FULL_ATOM_AND_OR_C26_FORMAL_RECEIPT__ZERO_CREDIT"
            and preflight["decision"] == "REJECT"
            and preflight["intended_process_exit_code"] == 2
            and set(preflight["blocking_authority_slots"]) == expected_missing
            and preflight["authority_slot_census"]
            == {"total": 9, "present": 7, "missing_or_blocking": 2}
            and preflight["pair_authority_reconstruction"] == expected_pair,
            "truthful preflight reject")
    require(preflight["authority_hardening"] == {
        "G2A_final_v2_receipt_bound": True,
        "G2A_old_invalidated_seal_rejected": True,
        "G2A_payload_and_root_manifests_bound": True,
        "G2A_terminal_replay_bound": True,
        "full_atom_seed_result_alone_is_authority": False,
        "pair_union_18_of_18_attacks_bound": True,
        "pair_union_no_import_verification_bound": True,
        "pair_union_terminal_receipt_bound": True,
        "raw_G2A_theorem_result_alone_is_authority": False,
        "raw_pair_union_result_alone_is_authority": False,
    }, "strong authority bindings")
    require(preflight["corrected_contract"] == {
        "atom_exact_incidence_set_or_empty_complement": True,
        "atom_multi_pair_allowed": True,
        "atom_multi_terminal_allowed": True,
        "atom_pair_incidence_key_unique": True,
        "atom_single_pair_or_terminal_constraint_imposed": False,
        "each_candidate_pair_exactly_one_terminal": True,
    }, "corrected many-to-many atom contract")
    require(preflight["forbidden_input_governance"] == {
        "C28_imported_or_read": False,
        "C29_imported_or_read": False,
        "historical_edge_ledger_used_as_candidate_universe": False,
        "legacy_coarse_current_atom_contract_accepted": False,
        "old_C27_FAMILIES_imported_or_read": False,
        "old_invalidated_G2A_seal_accepted": False,
        "old_transition_ledger_imported_or_read": False,
        "producer_module_imported": False,
    }, "forbidden inputs absent")
    require(preflight["global_gate"] == {
        "C26_formal_receipt_present": False,
        "decision": "FAIL_CLOSED_REJECT",
        "full_atom_formal_receipt_present": False,
        "pair_authority_row_count": 101_080,
        "primitive_support_atom_denominator": 483_232,
        "primitive_twenty_family_totality_proved": False,
    } and preflight["formal_credit"] == 0
       and preflight["manifest_authorized"] is False
       and preflight["strict_nonpromotion"] == {
           "C27_transition_totality": 0, "C28_pair_routing": 0,
           "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
       "fail-closed nonpromotion")
    descriptor = preflight["gap_ledger"]
    require(descriptor == {"filename": "authority_gap_ledger_v2.jsonl.gz",
                           "row_count": 9,
                           "file_sha256": views["gap_ledger"].sha256,
                           "row_sequence_sha256": gap_sequence},
            "gap descriptor")
    projection = {key: value for key, value in preflight.items()
                  if key not in {"invocation_seed", "root_input_capture",
                                 "semantic_projection_sha256", "result_sha256"}}
    require(preflight["semantic_projection_sha256"] == object_hash(projection),
            "semantic projection")


def verify(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    require(not output.exists(), "fresh verifier output")
    views = acquire(args)
    try:
        preflight = views["preflight_result"].document("result_sha256", True)
        gaps: dict[str, dict[str, Any]] = {}
        gap_sequence = hashlib.sha256()
        for ordinal, row in enumerate(views["gap_ledger"].rows()):
            require(row["schema"]
                    == "cm2.c27-independent.primitive-twenty-family-v5-authority-gap.row.v2"
                    and row["formal_credit"] == 0, f"gap:{ordinal}:schema")
            slot = row["authority_slot"]
            require(slot not in gaps, f"gap:{ordinal}:duplicate slot")
            gaps[slot] = row
            gap_sequence.update(bytes.fromhex(row["row_sha256"]))
        verify_preflight(preflight, gaps, gap_sequence.hexdigest(), views)

        input_labels = set(views) - {"preflight_result", "gap_ledger"}
        attestations = preflight["root_input_capture"]["attestations"]
        require(set(attestations) == input_labels
                and preflight["root_input_capture"]
                    ["all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat"] is True,
                "exact preflight root inputs")
        for label in input_labels:
            item = attestations[label]
            item_path = Path(item["path"])
            resolved = item_path.resolve() if item_path.is_absolute() else (ROOT / item_path).resolve()
            require(item["sha256"] == views[label].sha256
                    and resolved == views[label].path
                    and item["O_NOFOLLOW"] is True
                    and item["single_open_file_description_hash_parse_fstat"] is True,
                    label + ":preflight attestation")

        correction = views["correction_v2"].document("design_sha256", True)
        levels = correction["corrected_uniqueness_levels"]
        require(correction["formal_credit"] == 0
                and levels["candidate_pair"]
                    ["each_pair_has_exactly_one_assigned_terminal"] is True
                and levels["atom_pair_incidence"]
                    ["duplicate_incidence_key_forbidden"] is True
                and levels["atom_pair_incidence"]
                    ["one_atom_may_have_multiple_distinct_pair_incidences"] is True
                and levels["atom_pair_incidence"]
                    ["one_atom_may_therefore_observe_multiple_distinct_terminals"] is True
                and levels["atom"]["atom_terminal_uniqueness_required"] is False,
                "correction authority")
        strict = views["strict_volume_receipt"].document("receipt_sha256")
        lower = views["lower_contact_receipt"].document("receipt_sha256")
        c19c = views["c19c_receipt"].document("receipt_sha256")
        g2b = views["g2b_receipt"].document("result_sha256", True)
        require(strict["exact_census"]["all_component_strict_intersection_pair_count"]
                == 187_132 and strict["exact_census"]["primitive_atom_count"] == 483_232
                and strict["formal_credit"] == 0, "strict authority")
        require(lower["lower_dimensional_candidate_pair_count"] == 5_783_708
                and lower["C26_role"]["full_rows_read"] == 691_424
                and lower["C26_role"]["absence_used_as_negative_geometry_theorem"]
                    is False and lower["formal_credit"] == 0,
                "lower authority does not close C26")
        require(c19c["authority"]["direct_rule"]
                == "oriented [lower,upper) on internal faces"
                and c19c["formal_credit"] == 0, "C19C authority")
        require(g2b["G2B_closed_diagnostic"]["exact_positive"] == 9_408
                and g2b["G2B_closed_diagnostic"]["exact_empty"] == 9_392
                and g2b["formal_state_unchanged"]["formal_credit"] == 0,
                "G2B authority")

        g2a = views["g2a_final_receipt"].document("result_sha256", True)
        replay = views["g2a_terminal_replay"].document("result_sha256", True)
        invalidation = views["g2a_invalidation_notice"].document(None)
        payload_entries = manifest(views["g2a_payload_manifest"].raw(), "G2A payload")
        root_entries = manifest(views["g2a_root_manifest"].raw(), "G2A root")
        require(g2a["schema"]
                == "cm2.c27-independent.g2a-relative2d-primitive-totality-zero-credit-receipt.v2"
                and g2a["formal_credit"] == 0 and g2a["manifest_authorized"] is False
                and g2a["double_seed"]["all_materialized_ledgers_byte_identical"] is True
                and g2a["double_seed"]["ledgers"]["theorem"]["contacts"]["row_count"]
                    == 9_408
                and g2a["double_seed"]["ledgers"]["theorem"]["reverse_empty"]
                    ["row_count"] == 9_392
                and g2a["independent_verifier"]["imports_chain_or_shared_module"]
                    is False
                and g2a["coherent_attacks"]["control_pass"] is True
                and g2a["coherent_attacks"]["rejected"] == 15
                and g2a["coherent_attacks"]["accepted"] == 0
                and g2a["payload_manifest"]["entry_count"] == 37
                and g2a["payload_manifest"]["file_sha256"]
                    == views["g2a_payload_manifest"].sha256,
                "G2A final-v2 receipt")
        require(len(payload_entries) == 37 and len(root_entries) == 2
                and root_entries == {
                    "payload_manifest.sha256": views["g2a_payload_manifest"].sha256,
                    "receipt.json": views["g2a_final_receipt"].sha256,
                }, "G2A root/payload manifest closure")
        require(replay["schema"]
                == "cm2.c27-independent.g2a-relative2d-primitive-totality-terminal-replay.v2"
                and replay["receipt_file_sha256"] == views["g2a_final_receipt"].sha256
                and replay["receipt_result_sha256"] == g2a["result_sha256"]
                and replay["payload_manifest_file_sha256"]
                    == views["g2a_payload_manifest"].sha256
                and replay["root_manifest_file_sha256"]
                    == views["g2a_root_manifest"].sha256
                and replay["global_three_terminal_unique_assignment"] is False
                and replay["formal_credit"] == 0, "G2A terminal replay")
        require(invalidation["status"] == "INVALIDATED_BY_POSTSEAL_SOURCE_CHANGE"
                and invalidation["invalidated_seal_path"]
                    == ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final"
                and invalidation["replacement_seal_path"]
                    == ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2"
                and invalidation["formal_credit"] == 0, "old G2A seal invalidated")

        union = views["pair_union_receipt"].document("result_sha256", True)
        union_entries = manifest(views["pair_union_manifest"].raw(), "pair union")
        ownership_item = union["root_input_capture"]["attestations"]["ownership_ledger"]
        receipt_path = str(views["pair_union_receipt"].path.relative_to(ROOT))
        require(union["schema"]
                == "cm2.c27-independent.c24a-current-primitive-three-terminal-union-terminal-receipt.v1"
                and union["formal_credit"] == 0 and union["manifest_authorized"] is False
                and union["authority_scope"]["candidate_pair_count"] == 101_080
                and union["authority_scope"]["each_candidate_pair_exactly_one_terminal"]
                    is True
                and union["authority_scope"]["G2A_alias_counted_as_second_pair"]
                    is False
                and union["independent_verifier"]["no_producer_import"] is True
                and union["coherent_attacks"] == {
                    "accepted": 0, "attack_count": 18,
                    "attack_file_sha256":
                        "8a36d231cb536831b25ce3d219ccac138f0ca1173830eb38ebd51a55a65df15e",
                    "attack_result_sha256":
                        "fc650d555d839dedf2e1b765dde0851e3bdbae846683997f7b7f4cba059c863e",
                    "rejected": 18}
                and ownership_item["sha256"] == views["pair_ownership"].sha256
                and (ROOT / ownership_item["path"]).resolve()
                    == views["pair_ownership"].path
                and union_entries[receipt_path] == views["pair_union_receipt"].sha256
                and union_entries[ownership_item["path"]] == views["pair_ownership"].sha256,
                "sealed pair union authority")

        seen: set[tuple[str, str]] = set()
        terminal = Counter()
        source = Counter()
        for ordinal, row in enumerate(views["pair_ownership"].rows()):
            key = pair_key(row["pair_key"], f"ownership:{ordinal}")
            require(key not in seen, f"ownership:{ordinal}:duplicate")
            seen.add(key)
            assigned = row["assigned_terminal"]
            authority = row["source_authority"]
            require(assigned in {"SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
                                 "POSITIVE_VOLUME_CARRIERS"}
                    and row["formal_credit"] == 0, f"ownership:{ordinal}:terminal")
            if authority == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":
                require(assigned == "POSITIVE_VOLUME_CARRIERS"
                        and type(row["G2A_diagnostic_alias_row_sha256"]) is str,
                        f"ownership:{ordinal}:G2B normalization")
            terminal[assigned] += 1
            source[authority] += 1
        require(len(seen) == 101_080
                and terminal == {"SIGNED_BOUNDARY_FACES": 25_452,
                                 "COMPLETE_BOUNDARY_FACES": 10_688,
                                 "POSITIVE_VOLUME_CARRIERS": 64_940}
                and source == {"CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER": 91_672,
                               "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER": 9_408},
                "independent 101080 pair reconstruction")

        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-verification.v2",
            "status": "PASS_INDEPENDENT_AUTHORITY_BOUND_TRUTHFUL_REJECT__ZERO_CREDIT",
            "verification_seed": args.seed,
            "reconstructed": {
                "candidate_pair_count": len(seen),
                "terminal_census": dict(sorted(terminal.items())),
                "source_census": dict(sorted(source.items())),
                "blocking_authority_slots": sorted({
                    "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT",
                    "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT"}),
                "G2A_final_v2_manifest_and_replay_chain_valid": True,
                "pair_union_terminal_receipt_and_manifest_chain_valid": True,
                "old_invalidated_G2A_seal_rejected": True,
                "legacy_coarse_atom_contract_rejected": True,
                "atom_multi_pair_and_multi_terminal_allowed": True,
                "expected_preflight_exit_code": 2,
            },
            "implementation_independence": {
                "preflight_or_workspace_module_imported": False,
                "stdlib_only": True,
                "verifier_source_sha256": file_hash(Path(__file__).resolve()),
            },
            "decision": "VERIFY_REJECT",
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": preflight["strict_nonpromotion"],
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: view.attestation()
                                 for label, view in sorted(views.items())},
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = object_hash({
            key: value for key, value in body.items()
            if key not in {"verification_seed", "root_input_capture"}
        })
        result["verification_sha256"] = object_hash(result)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(encode(result) + b"\n")
        return result
    finally:
        for view in views.values():
            view.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "correction-v2", "strict-volume-receipt", "lower-contact-receipt",
        "c19c-receipt", "g2a-final-receipt", "g2a-payload-manifest",
        "g2a-root-manifest", "g2a-terminal-replay", "g2a-invalidation-notice",
        "g2b-receipt", "pair-union-receipt", "pair-union-manifest",
        "pair-ownership", "preflight-result", "gap-ledger",
    ):
        add_input(parser, name)
    parser.add_argument("--out-file", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = verify(args)
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": result["status"],
                  "verification_sha256": result["verification_sha256"],
                  "semantic_projection_sha256":
                      result["semantic_projection_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
