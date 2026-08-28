#!/usr/bin/env python3
"""Seal the scoped full-union atom contract without granting formal credit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

AUTHORITIES = {
    "join_producer_v2": (
        "deliverables/cm2_c27_full_union_101080_to_483232_atom_join_v2.py",
        "5b2ca56f5e3fa79871e5cee1e19050ae235961d00ba258420af4de56a6de8556",
    ),
    "independent_verifier_v2": (
        "deliverables/cm2_c27_full_union_101080_to_483232_atom_independent_verifier_v2.py",
        "4e869e94aa5c7e8d324bba1a9a86fe73e38add9d63ee1621dfc85e4e6b7bc9e2",
    ),
    "attack_harness_v1": (
        "deliverables/cm2_c27_full_union_101080_to_483232_atom_attack_v1.py",
        "6032297a2dc9d20bfe8529c5fcb89f82e4f4a0e849300b8d0f7a10073c2551d0",
    ),
    "primitive_atoms": (
        ".cm2-runtime/audit/c27-same-chart-relative-cells-census-v2-seed-30628101/cm2_c27_same_chart_relative_cells_totality_census_atom_ledger.jsonl.gz",
        "6e3aacd47d1331634f5b9d5c89f21fae62695203deb81acd4009deca81b4d069",
    ),
    "union_ownership": (
        ".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/primitive_three_terminal_101080_unique_ownership.jsonl.gz",
        "caaee424b629887ce8d44479861f311f802140cdd9adcd4dcf7556b1c6eb5fe2",
    ),
    "union_result": (
        ".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/result.json",
        "25c3f914dd653cf11eaea69532308c55d6bd5a4143ecc338aa55adaec1b36c4b",
    ),
    "current_priority_seed1": (
        ".cm2-runtime/audit/c27-current-support-91672-stable-v4b-seed-30637101-attempt1/payload/current_support_91672_unique_priority_routes.jsonl.gz",
        "c20ffeb59b120fa8bbadb255e57566c746277a98def254c8ce153e065ad3baf1",
    ),
    "current_priority_seed2": (
        ".cm2-runtime/audit/c27-current-support-91672-stable-v4b-seed-30637991-attempt1/payload/current_support_91672_unique_priority_routes.jsonl.gz",
        "c20ffeb59b120fa8bbadb255e57566c746277a98def254c8ce153e065ad3baf1",
    ),
    "current_positive_seed1": (
        ".cm2-runtime/audit/c27-current-support-91672-stable-v4b-seed-30637101-attempt1/payload/primitive_scan/current_new_C19_carrier_exact_positive_pair_universe.jsonl.gz",
        "548dfce1df93b974abde9874dc73e43a8541e9524e15f109c442069b40a0fca0",
    ),
    "current_positive_seed2": (
        ".cm2-runtime/audit/c27-current-support-91672-stable-v4b-seed-30637991-attempt1/payload/primitive_scan/current_new_C19_carrier_exact_positive_pair_universe.jsonl.gz",
        "548dfce1df93b974abde9874dc73e43a8541e9524e15f109c442069b40a0fca0",
    ),
    "g2b_exact": (
        ".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634101-clean-replay/payload/C24A_G2B_18800_exact_factor_sign_disposition.jsonl.gz",
        "c3dbfb3363af18dc79b27aeb4245266102914de5a8c2cab980c019337776d899",
    ),
    "g2b_terminal_receipt": (
        "deliverables/cm2_c27_c24a_g2b_terminal_zero_credit_v1/terminal_zero_credit_receipt.json",
        "2e81e5084eb16f20d02865d0e90696f3a776673b8df0f727a7438703ce78549f",
    ),
    "c15": (
        "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
        "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    ),
    "endpoint_authority": (
        "deliverables/cm2_c19c_endpoint_ownership_v3_authority_ledger.jsonl.gz",
        "77b220d803b64066a09a0172e06f53f0ddc7a229d208cb7248c2293f493f3166",
    ),
    "endpoint_receipt": (
        "deliverables/cm2_c19c_endpoint_ownership_v3_terminal_receipt.json",
        "c620034783676f20d99e3f9a600cfe9b3e22a48129cd2f0555479d5b6c25e63b",
    ),
    "seed1_ledger": (
        ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-join-v2-seed-30640101-attempt2/full_union_101080_on_483232_atom_incidence_or_complement_v2.jsonl.gz",
        "9b642b40fea1bbae5121ca9fcc43461795190c92f38753d41ff7d0e4e358b114",
    ),
    "seed1_result": (
        ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-join-v2-seed-30640101-attempt2/result.json",
        "66b71c4860be2b2e94f3f5694216a6943100bf6bc5c4d9636a57f165da5b997f",
    ),
    "seed2_ledger": (
        ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-join-v2-seed-30640991-attempt1/full_union_101080_on_483232_atom_incidence_or_complement_v2.jsonl.gz",
        "9b642b40fea1bbae5121ca9fcc43461795190c92f38753d41ff7d0e4e358b114",
    ),
    "seed2_result": (
        ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-join-v2-seed-30640991-attempt1/result.json",
        "3b4c25172b70b0dd6daca0ff5aa22ba1658c08acaa236a8ff5f864f5b0898d4b",
    ),
    "independent_verification": (
        ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-independent-verification-v2-attempt1/verification.json",
        "11d5004f0590a22bb48517c301cc9b5c11f1289ff519abccefa0475742f5f204",
    ),
    "attacks": (
        ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-attacks-v1-attempt2/attacks.json",
        "b34984857fe634fb917c0f050182495c99d8ac37719fe3d95458384bd1aa96a7",
    ),
    "old_current_coarse_ledger": (
        ".cm2-runtime/audit/c27-current-support-483232-atom-incidence-complement-v1-seed-30639101-attempt1/current_support_483232_atom_pair_incidence_or_complement.jsonl.gz",
        "b1bc4f19f1ae10ac34e444b0119be52a25f813b2db01d5faabd405ea1654673c",
    ),
    "old_current_coarse_result": (
        ".cm2-runtime/audit/c27-current-support-483232-atom-incidence-complement-v1-seed-30639101-attempt1/result.json",
        "cac521db926e9b100b72688a9287baace4d71f6fed3b293a8fe431820dd2d725",
    ),
}


class Failure(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class Capture:
    label: str
    relative: str
    fd: int
    pre: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, relative: str, expected: str | None = None) -> "Capture":
        fd = os.open(ROOT / relative, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            if expected is not None:
                need(observed == expected, label + ":pin")
            pre = fingerprint(before)
            need(fingerprint(os.fstat(fd)) == pre, label + ":hash-fstat")
            return cls(label, relative, fd, pre, observed)
        except BaseException:
            os.close(fd)
            raise

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        need(fingerprint(os.fstat(self.fd)) == self.pre, self.label + ":parse-fstat")
        return b"".join(chunks)

    def document(self) -> dict[str, Any]:
        value = json.loads(self.raw())
        body = dict(value)
        claimed = None
        for key in ("result_sha256", "receipt_sha256", "verification_sha256"):
            if key in body:
                claimed = body.pop(key)
                break
        need(type(claimed) is str and claimed == object_sha(body), self.label + ":closure")
        return value

    def same_bytes(self, other: "Capture") -> bool:
        if self.pre[2] != other.pre[2]:
            return False
        offset = 0
        while offset < self.pre[2]:
            left = os.pread(self.fd, 4 << 20, offset)
            right = os.pread(other.fd, 4 << 20, offset)
            if left != right:
                return False
            offset += len(left)
        return True

    def receipt(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == self.pre, self.label + ":final-fstat")
        return {
            "path": self.relative,
            "sha256": self.sha256,
            "size": self.pre[2],
            "stat_fingerprint": list(self.pre),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    captures: dict[str, Capture] = {}
    try:
        need(not args.out_dir.exists(), "fresh output")
        for label, (relative, expected) in AUTHORITIES.items():
            captures[label] = Capture.open(label, relative, expected)
        own_relative = str(Path(__file__).resolve().relative_to(ROOT))
        captures["terminal_builder"] = Capture.open("terminal_builder", own_relative)
        need(captures["seed1_ledger"].same_bytes(captures["seed2_ledger"]),
             "dual seed ledger byte identity")

        seed1 = captures["seed1_result"].document()
        seed2 = captures["seed2_result"].document()
        independent = captures["independent_verification"].document()
        attacks = captures["attacks"].document()
        old = captures["old_current_coarse_result"].document()
        expected_status = (
            "PASS_FULL_UNION_101080_PAIR_OWNERSHIP_MATERIALIZED_ON_ALL_483232_ATOMS__"
            "POSITIVE_SOURCE_KEYS_EXACTLY_RESOLVED__G2B_IS_POSITIVE_VOLUME_NOT_SAME_CHART__"
            "G2A_ALIAS_NOT_COUNTED__ZERO_CREDIT"
        )
        for label, result in (("seed1", seed1), ("seed2", seed2)):
            need(result["status"] == expected_status, label + ":status")
            need(result["output"]["file_sha256"] == AUTHORITIES["seed1_ledger"][1]
                 and result["output"]["row_count"] == 483232, label + ":output")
            need(result["pair_union"]["pairs"] == 101080
                 and result["pair_union"]["G2A_alias_independent_candidate_count"] == 0
                 and result["pair_union"]["G2B_20_terminal_owner"] == "POSITIVE_VOLUME_CARRIERS"
                 and result["pair_union"]["G2B_assigned_to_SAME_CHART_RELATIVE_CELLS"] is False,
                 label + ":union semantics")
            need(result["formal_credit"] == 0 and result["manifest_authorized"] is False
                 and result["C27_C28_C29"] == "FULL_REBUILD_REQUIRED"
                 and result["Source_W_formal_remainder"] == 80
                 and result["CM2"] == "NO-GO_FOR_CLAIM", label + ":nonpromotion")

        exact_atom = {
            "atoms": 483232,
            "incident_atoms": 62768,
            "exact_complement_atoms": 420464,
            "expanded_atom_route_incidences": 206632,
            "multi_terminal_incident_atoms": 3896,
        }
        for key, value in exact_atom.items():
            need(seed1["atom_denominator"][key] == value
                 and seed2["atom_denominator"][key] == value
                 and (independent["primitive_atoms"] if key == "atoms" else\n                      sum(count for name, count in independent["terminal_set_atom_census"].items() if "|" in name)\n                      if key == "multi_terminal_incident_atoms" else independent[key]) == value,
                 "exact atom census:" + key)
        binding = {
            "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS": 111064,
            "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE": 86160,
            "EXACT_C24A_G2B_C22_TARGET_ATOM": 9408,
        }
        terminal_sets = {
            "COMPLEMENT": 420464,
            "COMPLETE_BOUNDARY_FACES": 528,
            "COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS": 32,
            "POSITIVE_VOLUME_CARRIERS": 51248,
            "SIGNED_BOUNDARY_FACES": 7096,
            "SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES": 3756,
            "SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS": 108,
        }
        need(seed1["binding_census"] == binding == independent["binding_census"],
             "binding census")
        need(seed1["atom_denominator"]["terminal_set_atom_census"] == terminal_sets
             and independent["terminal_set_atom_census"] == terminal_sets,
             "terminal set census")
        need(independent["dual_seed_join_ledgers_byte_identical"] is True
             and independent["pair_routes"] == 101080
             and independent["formal_credit"] == 0
             and independent["manifest_authorized"] is False,
             "independent verifier")

        required_attacks = {
            "positive_coarse_owner_fanout_regression",
            "result_coarse_positive_fanout_plus_184",
            "result_coarse_positive_terminal_set_regression",
            "result_remove_G2B_528_new_incident_atoms",
        }
        attack_names = {row["attack"] for row in attacks["attacks"] if row["rejected"] is True}
        need(attacks["attack_count"] == attacks["rejected_count"] == 54
             and attacks["accepted_count"] == 0
             and required_attacks <= attack_names
             and attacks["formal_credit"] == 0
             and attacks["manifest_authorized"] is False, "coherent attacks")

        old_incidence = old["incidence_complement"]
        old_sets = old_incidence["terminal_set_atom_census"]
        need(old_incidence["incident_atoms"] == 62240
             and old_incidence["complement_atoms"] == 420992
             and old_incidence["expanded_atom_pair_route_incidences"] == 197408
             and old_incidence["multi_terminal_incident_atoms"] == 3896
             and old_sets["SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES"] == 3612
             and old_sets["SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS"] == 252
             and old_sets["COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS"] == 32
             and old_sets["POSITIVE_VOLUME_CARRIERS"] == 50720,
             "old coarse comparison authority")

        attestations = {label: capture.receipt()
                        for label, capture in sorted(captures.items())}
        semantic = {
            "schema": "cm2.c27-independent.full-union-101080-on-483232.atom-terminal-zero-credit.v2",
            "status": "PASS_SCOPED_THREE_TERMINAL_FULL_UNION_ATOM_CONTRACT_DUAL_SEED_INDEPENDENT_ATTACK_SEALED__ZERO_FORMAL_CREDIT",
            "scope": "THREE_TERMINAL_PAIR_OWNERSHIP_MATERIALIZED_AS_EXACT_ATOM_INCIDENCE_OR_COMPLEMENT_ONLY",
            "pair_union": {
                "pairs": 101080,
                "by_terminal": {
                    "SIGNED_BOUNDARY_FACES": 25452,
                    "COMPLETE_BOUNDARY_FACES": 10688,
                    "POSITIVE_VOLUME_CARRIERS": 64940,
                },
                "current_pairs": 91672,
                "C24A_G2B_positive_pairs": 9408,
                "G2A_alias_bound_but_not_counted": 9408,
                "G2A_alias_independent_candidate_count": 0,
            },
            "exact_atom_contract": {**exact_atom, "binding_census": binding,
                                    "terminal_set_atom_census": terminal_sets,
                                    "C19C_endpoint_v3_rows": 33344},
            "coarse_to_exact_contract_correction": {
                "old_current_only_owner_fanout_expanded_incidences": 197408,
                "correct_current_exact_expanded_incidences": 197224,
                "coarse_positive_incidences_removed": 184,
                "atoms_affected_by_coarse_positive_removal": 144,
                "then_add_exact_C24A_G2B_incidences": 9408,
                "full_union_exact_expanded_incidences": 206632,
                "old_current_incident_atoms": 62240,
                "new_atoms_added_by_G2B": 528,
                "full_union_incident_atoms": 62768,
                "terminal_set_changes": {
                    "SIGNED_COMPLETE_POSITIVE": {"old": 252, "new": 108},
                    "SIGNED_COMPLETE": {"old": 3612, "new": 3756},
                    "COMPLETE_POSITIVE": {"old": 32, "new": 32},
                    "POSITIVE_ONLY": {"old": 50720, "new": 51248},
                    "multi_terminal_atoms": {"old": 3896, "new": 3896},
                },
                "coarse_positive_owner_fanout_is_authority": False,
                "positive_routes_bind_exact_two_representative_atoms_via_frozen_source_key": True,
            },
            "dual_seed": {
                "seeds": [30640101, 30640991],
                "ledgers_byte_identical": True,
                "ledger_sha256": AUTHORITIES["seed1_ledger"][1],
                "row_sequence_sha256": "61b0feb579f03b330130a6c88a755fe518ea0809dc9a40013db6ddb3644c0f8e",
            },
            "independent_inverse_verifier": {
                "status": independent["status"],
                "result_sha256": independent["result_sha256"],
            },
            "coherent_attacks": {"rejected": 54, "accepted": 0,
                                 "required_regression_attacks": sorted(required_attacks)},
            "open_blockers": [
                "OTHER_20_FAMILY_TERMINALS_STILL_REQUIRE_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT",
                "C27_C28_C29_FULL_REBUILD_REMAINS_REQUIRED",
                "NO_PATCH_PROMOTION_AND_NO_PHYSICAL_MAXIMALITY_CLAIM",
            ],
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27_C28_C29": "FULL_REBUILD_REQUIRED",
            "latest_formal_seal": "Round306C30b",
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
            "source_W_transition_authorized": False,
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": attestations,
            },
        }
        receipt = {**semantic, "receipt_sha256": object_sha(semantic)}
        args.out_dir.mkdir(parents=True)
        receipt_path = args.out_dir / "terminal_zero_credit_receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        receipt_file_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        entries = [(item["path"], item["sha256"]) for item in attestations.values()]
        entries.append((str(receipt_path.resolve().relative_to(ROOT)), receipt_file_sha))
        manifest_bytes = b"".join(
            f"{digest}  {path}\n".encode("ascii")
            for path, digest in sorted(entries)
        )
        manifest_path = args.out_dir / "manifest.sha256"
        manifest_path.write_bytes(manifest_bytes)
        print(canonical({
            "status": receipt["status"],
            "receipt_sha256": receipt["receipt_sha256"],
            "receipt_file_sha256": receipt_file_sha,
            "manifest_file_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        }).decode("ascii"))
        return 0
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    finally:
        for capture in captures.values():
            capture.close()


if __name__ == "__main__":
    raise SystemExit(main())

