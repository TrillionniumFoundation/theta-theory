#!/usr/bin/env python3
"""Independent verifier for the round306c50b fail-closed oracle contract.

The verifier neither imports nor executes the producer.  It independently
reconstructs the only currently lawful contract/result: positive cemetery or
disconnected-exterior decisions are disabled until a pinned four-chart global
branch-and-bound/component decider exists.  It also validates the producer's
executed hostile-test receipt and attacks the documents, parser, and stable
file-read boundary.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent
PRODUCER = DELIVERABLES / (
    "cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_v1.py"
)
DEFAULT_CONTRACT = DELIVERABLES / (
    "cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_contract_v1.json"
)
DEFAULT_SELF_TEST = DELIVERABLES / (
    "cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_hostile_tests_v1.json"
)

SCHEMA = "cm2.round306c50b.d02-b-global-cemetery-disconnected-exterior-oracle.v1"
CONTRACT_SCHEMA = SCHEMA + ".missing-oracle-contract"
SELF_TEST_SCHEMA = SCHEMA + ".executed-hostile-self-test"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification"
PRODUCER_SHA256 = "6c57f7ed935603e7094b73e4f6492cd1ea1d26b7beeac8c43733d5a006965a4b"
CONTRACT_OBJECT_SHA256 = "ddd1776bc133cac340b872f03325e97e8526a545e3e1a3fb11d56a159a4f9d97"
SELF_TEST_OBJECT_SHA256 = "2bfe14bd0694f96d9e85ac8f361019b0474d7d78ba8c93150070747a17217dbf"
GLOBAL_ORACLE_NAME = "GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE"
REQUESTED_TERMINAL = "STRICT_CEMETERY_OR_DISCONNECTED"
EXACT_FIELDS = (
    "exact_owner", "discriminant", "root_order", "official_word", "chart",
    "wall", "homogeneity", "incidence", "core",
    "structured_terminal_decision_margin",
)
MISSING_GLOBAL_CONTRACT = (
    "PINNED_NO_PRODUCER_IMPORT_ARBITRARY_HISTORY_NUMERIC_REPLAY_AUTHORITY",
    "GLOBAL_FOUR_CHART_FUNDAMENTAL_DOMAIN_ATLAS_WITH_EXACT_QUOTIENT",
    "GLOBAL_FACE_CORNER_SOURCE_GRAZING_GLUE_AND_OWNER_LEDGER",
    "GLOBAL_EXTERIOR_BRANCH_AND_BOUND_LEAF_LEDGER_WITH_UNRESOLVED_ZERO",
    "GLOBAL_COMPONENT_ADJACENCY_RECONSTRUCTION_AND_KNOWN_SHEET_ANCHOR",
    "INDEPENDENT_RECONSTRUCTION_OF_STRICT_CEMETERY_OR_DISCONNECTED_DECISION",
)
FORBIDDEN_SHORTCUT_TOKENS = (
    "BOUNDED_NO_CONTACT",
    "BOUNDED_PILOT",
    "FINITE_HORIZON_NO_CONTACT",
    "NO_CURRENT_CONTACT",
    "NO_CONTACT_WITHIN",
    "CURRENTLY_DISCONNECTED",
    "ENDPOINT_OUTSIDE",
    "LOCAL_CHART_EXIT",
    "CHART_FACE_EXIT",
)
HOSTILE_TEST_NAMES = (
    "baseline_full_occurrence_binding_validated",
    "baseline_terminal_denied_missing_global_math",
    "history_order_mutation_rejected",
    "owner_mutation_rejected",
    "root_order_mutation_rejected",
    "official_word_mutation_rejected",
    "chart_mutation_rejected",
    "wall_mutation_rejected",
    "core_mutation_rejected",
    "original_box_mutation_rejected",
    "physical_side_mutation_rejected",
    "bounded_no_contact_not_terminal",
    "no_current_contact_not_terminal",
    "coherent_unapproved_global_claim_not_terminal",
    "query_path_TOCTOU_swap_rejected",
)
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Rejected(RuntimeError):
    """Independent audit rejection."""


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "hash absent before close")
    answer["object_sha256"] = digest(answer)
    return answer


def verify_closed(value: Any, label: str) -> None:
    need(
        type(value) is dict
        and type(value.get("object_sha256")) is str
        and HEX64.fullmatch(value["object_sha256"]) is not None,
        label + " closed object",
    )
    body = copy.deepcopy(value)
    claimed = body.pop("object_sha256")
    need(digest(body) == claimed, label + " self hash")


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
        if key in answer:
            raise Rejected("duplicate JSON key:" + key)
        answer[key] = value
    return answer


def parse_json(raw: bytes, label: str) -> Any:
    need(0 < len(raw) <= 32 << 20, label + " bounded nonempty")
    need(not raw.startswith(b"\xef\xbb\xbf"), label + " no BOM")
    try:
        return json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected(label + " non-finite token:" + token)
            ),
        )
    except Rejected:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Rejected(label + " strict JSON:" + str(exc)) from exc


def stable_read(
    path: Path, maximum: int = 32 << 20,
    mutation_hook: Callable[[], None] | None = None,
) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and 0 < before.st_size <= maximum,
            "stable regular single-link bounded file",
        )
        chunks: list[bytes] = []
        remaining = maximum + 1
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            if not block:
                break
            chunks.append(block)
            remaining -= len(block)
        raw = b"".join(chunks)
        need(len(raw) <= maximum, "stable read size")
        if mutation_hook is not None:
            mutation_hook()
        after = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)

        def fp(item: os.stat_result) -> tuple[int, ...]:
            return (
                item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
                item.st_size, item.st_mtime_ns,
            )

        need(fp(before) == fp(after) == fp(named), "stable read TOCTOU/inode/bytes")
        return raw
    finally:
        os.close(descriptor)


def expected_contract() -> dict[str, Any]:
    return close_object({
        "schema": CONTRACT_SCHEMA,
        "status": "MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED",
        "oracle_name": GLOBAL_ORACLE_NAME,
        "producer_source_sha256": PRODUCER_SHA256,
        "accepted_input_scope": (
            "one fully bound physical-side occurrence: frozen original_box + contiguous owner_history + current exact numeric step + independent replay attestation"
        ),
        "structurally_checked_exact_fields": list(EXACT_FIELDS),
        "missing_global_oracle_contract": list(MISSING_GLOBAL_CONTRACT),
        "positive_terminal_enabled": False,
        "approved_global_decider_source_sha256": None,
        "allowed_positive_terminal_class_after_future_decider": REQUESTED_TERMINAL,
        "forbidden_nonterminal_shortcuts": list(FORBIDDEN_SHORTCUT_TOKENS),
        "bounded_or_no_current_contact_is_terminal": False,
        "templates_are_occurrence_proof": False,
        "C35_C36_C37_role": "TEMPLATE_AND_MARGIN_REGRESSION_ONLY",
        "C46_C49_role": "OCCURRENCE_BINDING_AND_LOCAL_CONTINUATION_ONLY",
        "global_decider_minimum_obligations": {
            "four_chart_fundamental_domain_complete": True,
            "face_corner_source_grazing_gluing_complete": True,
            "all_branch_and_bound_leaves_strictly_typed": True,
            "unresolved_leaf_count": 0,
            "component_adjacency_independently_reconstructed": True,
            "known_connected_sheet_anchor_cross_bound": True,
            "every_positive_decision_recomputed_not_boolean_trusted": True,
        },
        "formal_credit": 0,
        "D02_credit": 0,
        "terminal_credit": 0,
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def expected_self_test() -> dict[str, Any]:
    return close_object({
        "schema": SELF_TEST_SCHEMA,
        "status": "PASS_15_OF_15_EXECUTED_HOSTILE_TESTS_FAIL_CLOSED",
        "producer_source_sha256": PRODUCER_SHA256,
        "attacks": {name: True for name in HOSTILE_TEST_NAMES},
        "positive_terminal_enabled": False,
        "terminal_credit": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "writes_performed": False,
    })


def verify_contract(value: Any) -> None:
    verify_closed(value, "contract")
    expected = expected_contract()
    need(expected["object_sha256"] == CONTRACT_OBJECT_SHA256,
         "independent expected contract pin")
    need(value == expected, "exact independently reconstructed contract")


def verify_self_test(value: Any) -> None:
    verify_closed(value, "hostile test result")
    expected = expected_self_test()
    need(expected["object_sha256"] == SELF_TEST_OBJECT_SHA256,
         "independent expected hostile-test pin")
    need(value == expected, "exact hostile test receipt")
    attacks = value["attacks"]
    need(
        set(attacks) == set(HOSTILE_TEST_NAMES)
        and len(attacks) == 15
        and all(attacks.values()),
        "all 15 named hostile tests passed",
    )


def independently_classify_candidate(claim: str) -> str:
    normalized = claim.upper().replace("-", "_").replace(" ", "_")
    if any(token in normalized for token in FORBIDDEN_SHORTCUT_TOKENS):
        return "REJECTED_NONTERMINAL_SHORTCUT_FAIL_CLOSED"
    return "PENDING_MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED"


def coherently_mutated(
    value: dict[str, Any], mutator: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    answer.pop("object_sha256", None)
    mutator(answer)
    return close_object(answer)


def rejected(action: Callable[[], Any]) -> bool:
    try:
        action()
    except (Rejected, KeyError, ValueError, TypeError, OSError):
        return True
    return False


def semantic_attacks(contract: dict[str, Any], receipt: dict[str, Any]) -> dict[str, bool]:
    contract_mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "enable_positive_terminal_rejected":
            lambda value: value.__setitem__("positive_terminal_enabled", True),
        "invent_approved_decider_rejected":
            lambda value: value.__setitem__("approved_global_decider_source_sha256", "f" * 64),
        "bounded_as_terminal_rejected":
            lambda value: value.__setitem__("bounded_or_no_current_contact_is_terminal", True),
        "template_as_occurrence_proof_rejected":
            lambda value: value.__setitem__("templates_are_occurrence_proof", True),
        "C35_C37_role_promotion_rejected":
            lambda value: value.__setitem__("C35_C36_C37_role", "GLOBAL_ORACLE"),
        "C46_C49_role_promotion_rejected":
            lambda value: value.__setitem__("C46_C49_role", "GLOBAL_TERMINAL_AUTHORITY"),
        "missing_oracle_row_removal_rejected":
            lambda value: value["missing_global_oracle_contract"].pop(),
        "four_chart_obligation_removal_rejected":
            lambda value: value["global_decider_minimum_obligations"].__setitem__("four_chart_fundamental_domain_complete", False),
        "face_corner_obligation_removal_rejected":
            lambda value: value["global_decider_minimum_obligations"].__setitem__("face_corner_source_grazing_gluing_complete", False),
        "unresolved_nonzero_rejected":
            lambda value: value["global_decider_minimum_obligations"].__setitem__("unresolved_leaf_count", 1),
        "component_reconstruction_removal_rejected":
            lambda value: value["global_decider_minimum_obligations"].__setitem__("component_adjacency_independently_reconstructed", False),
        "forbidden_shortcut_removal_rejected":
            lambda value: value["forbidden_nonterminal_shortcuts"].remove("NO_CURRENT_CONTACT"),
        "formal_credit_forgery_rejected":
            lambda value: value.__setitem__("formal_credit", 1),
        "D02_credit_forgery_rejected":
            lambda value: value.__setitem__("D02_credit", 1),
        "authority_install_forgery_rejected":
            lambda value: value.__setitem__("authority_pointer_installed", True),
        "canonical_touch_forgery_rejected":
            lambda value: value.__setitem__("canonical_status_touched", True),
    }
    attacks = {
        name: rejected(lambda mutation=mutation: verify_contract(
            coherently_mutated(contract, mutation)
        ))
        for name, mutation in contract_mutations.items()
    }
    receipt_mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "history_attack_false_rejected":
            lambda value: value["attacks"].__setitem__("history_order_mutation_rejected", False),
        "owner_attack_deleted_rejected":
            lambda value: value["attacks"].pop("owner_mutation_rejected"),
        "word_attack_renamed_rejected":
            lambda value: value["attacks"].__setitem__("official_word_mutation_ACCEPTED", value["attacks"].pop("official_word_mutation_rejected")),
        "receipt_positive_terminal_rejected":
            lambda value: value.__setitem__("positive_terminal_enabled", True),
        "receipt_credit_rejected":
            lambda value: value.__setitem__("terminal_credit", 1),
    }
    attacks.update({
        name: rejected(lambda mutation=mutation: verify_self_test(
            coherently_mutated(receipt, mutation)
        ))
        for name, mutation in receipt_mutations.items()
    })
    attacks.update({
        "independent_bounded_no_contact_rejection":
            independently_classify_candidate("BOUNDED_NO_CONTACT")
            == "REJECTED_NONTERMINAL_SHORTCUT_FAIL_CLOSED",
        "independent_no_current_contact_rejection":
            independently_classify_candidate("NO_CURRENT_CONTACT")
            == "REJECTED_NONTERMINAL_SHORTCUT_FAIL_CLOSED",
        "independent_unapproved_strict_claim_still_pending":
            independently_classify_candidate("STRICT_GLOBAL_COMPONENT_DISCONNECTION")
            == "PENDING_MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED",
    })
    return attacks


def parser_and_file_attacks(contract: dict[str, Any]) -> dict[str, bool]:
    duplicate = b'{"schema":"a","schema":"b"}'
    nonfinite = b'{"x":NaN}'
    bom = b"\xef\xbb\xbf{}"
    attacks = {
        "duplicate_JSON_key_rejected": rejected(lambda: parse_json(duplicate, "attack")),
        "nonfinite_JSON_rejected": rejected(lambda: parse_json(nonfinite, "attack")),
        "BOM_JSON_rejected": rejected(lambda: parse_json(bom, "attack")),
    }
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        real = root / "real.json"
        alias = root / "alias.json"
        hard = root / "hard.json"
        replacement = root / "replacement.json"
        displaced = root / "displaced.json"
        real.write_bytes(canonical(contract))
        alias.symlink_to(real.name)
        attacks["symlink_input_rejected"] = rejected(lambda: stable_read(alias))
        os.link(real, hard)
        attacks["hardlink_input_rejected"] = rejected(lambda: stable_read(real))
        hard.unlink()
        replacement.write_bytes(canonical(coherently_mutated(
            contract, lambda value: value.__setitem__("formal_credit", 1)
        )))

        def swap() -> None:
            os.replace(real, displaced)
            os.replace(replacement, real)

        attacks["TOCTOU_name_swap_rejected"] = rejected(
            lambda: stable_read(real, mutation_hook=swap)
        )
    return attacks


def run_verification(contract_path: Path, self_test_path: Path) -> dict[str, Any]:
    producer_raw = stable_read(PRODUCER, 2 << 20)
    need(bytes_sha(producer_raw) == PRODUCER_SHA256, "pinned producer source")
    producer_text = producer_raw.decode("utf-8", "strict")
    need(
        "positive_terminal_enabled\": False" in producer_text
        and "approved_global_decider_source_sha256\": None" in producer_text
        and "bounded_or_no_current_contact_is_terminal\": False" in producer_text,
        "producer fail-closed source markers",
    )
    contract_raw = stable_read(contract_path)
    receipt_raw = stable_read(self_test_path)
    contract = parse_json(contract_raw, "contract")
    receipt = parse_json(receipt_raw, "hostile tests")
    verify_contract(contract)
    verify_self_test(receipt)
    attacks = semantic_attacks(contract, receipt)
    attacks.update(parser_and_file_attacks(contract))
    need(len(attacks) == 30 and all(attacks.values()), "30/30 independent attacks")
    return close_object({
        "schema": VERIFICATION_SCHEMA,
        "status": "PASS_INDEPENDENT_NO_PRODUCER_IMPORT_FAIL_CLOSED_ORACLE_AUDIT",
        "verifier_source_sha256": file_sha(SELF),
        "producer_source_sha256": PRODUCER_SHA256,
        "contract_file_sha256": bytes_sha(contract_raw),
        "contract_object_sha256": contract["object_sha256"],
        "hostile_test_file_sha256": bytes_sha(receipt_raw),
        "hostile_test_object_sha256": receipt["object_sha256"],
        "producer_imported": False,
        "producer_executed": False,
        "producer_hostile_tests_pinned": len(receipt["attacks"]),
        "independent_attack_count": len(attacks),
        "independent_attacks": attacks,
        "positive_terminal_enabled": False,
        "approved_global_decider_source_sha256": None,
        "disposition": "UNRESOLVED",
        "terminal_class": None,
        "bounded_or_no_current_contact_is_terminal": False,
        "formal_credit": 0,
        "D02_credit": 0,
        "terminal_credit": 0,
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--hostile-tests", type=Path, default=DEFAULT_SELF_TEST)
    args = parser.parse_args()
    try:
        emit(run_verification(args.contract, args.hostile_tests))
        return 0
    except (Rejected, KeyError, ValueError, TypeError, OSError) as exc:
        emit(close_object({
            "schema": VERIFICATION_SCHEMA,
            "status": "REJECTED_FAIL_CLOSED",
            "reason": str(exc),
            "verifier_source_sha256": file_sha(SELF),
            "producer_imported": False,
            "producer_executed": False,
            "disposition": "UNRESOLVED",
            "terminal_class": None,
            "formal_credit": 0,
            "D02_credit": 0,
            "terminal_credit": 0,
            "writes_performed": False,
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
