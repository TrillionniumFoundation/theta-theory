#!/usr/bin/env python3
"""Independent verifier for the Round294-B admission closure.

This verifier does not import or execute the Round294-B producer, any
Round294 producer, or any Round292 producer.  It independently validates the
actual direct-file pins, both exact manifest sets, every actual package
member, strict JSON/GZIP/path boundaries, the frozen registry census, and the
explicit 10,020 / 431,824 / legacy-63,224 rejections before opening the
Round294-B candidate result.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round294b_source_g_registry_builder_admission_closure"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_result.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
SCHEMA = "cm2.round294b.source-g-registry-builder-admission-closure.v1"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"

EXPECTED_PRODUCER_SHA256 = (
    "ed8346b550c461cea28a4a01393c4c5d1be802f9e6145537a0ae7fe5c2e13192"
)
R292_BUILDER = "cm2_round292_source_g_occurrence_registry_candidate_construction.py"
R292A_VERIFIER = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verifier.py"
)
R292A_MANIFEST = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_manifest.sha256"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256"
)

DIRECT_FILE_PINS = {
    R292_BUILDER:
        "2c0b7e864839880f47cca2989b3f8d48fcec0399c0644c92f8aabab225402004",
    R292A_VERIFIER:
        "9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010",
    R292A_MANIFEST:
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
}

R292A_MEMBER_PINS = {
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe.py":
        "69078405b39dff3e924630ffbc9fbe35c14e4114e1e33c946b9ab44fe26e8c4c",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_result.json":
        "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz":
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R292A_VERIFIER:
        "9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verification.json":
        "7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_report.md":
        "b83900259649ff13c40623bc122366c3b014bcc92bb11e27007eb8b7a47add2b",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_cold_replay.md":
        "de9e6f34197a921a1af09d8922456b8a4900b7eb88f8f7b88260c6705ff0f441",
}

R294_MEMBER_PINS = {
    "cm2_round294_source_g_occurrence_registry_atomic_promotion.py":
        "6e0ab06cf6ab7dfb7868b2fe7a4699a914e6a3b0f8b18e4181d138bc2d887a9b",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz":
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json":
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verifier.py":
        "154158d7910b1ffa1f71475c4e0505c6ab72ca3ab856a2fa4c27d7e376533aaa",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json":
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_attack_suite.json":
        "aefb50be4969676d752cf8c8cb06f355db508007be4c1ee95f07c305e19a8adb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_report.md":
        "37676f39ab54092cd6c57ebd85bc21f9ec1de820ea82a4971998106df5c57114",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_cold_replay.md":
        "017172cac7075e7b90655ad2883fba2989cd27819c91ab5f04f2358737a7bea9",
}

R292A_VERIFICATION = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verification.json"
)
R294_RESULT = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json"
)
R294_ATTACKS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_attack_suite.json"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
)
R294_BINDINGS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz"
)

DENIED_R292B_FRAGMENT = (
    "cm2_round292_source_g_r289_r291_witness_binding_audit_probe"
)
PIN_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_FILE_BYTES = 1_100_000_000
MAX_GZIP_OUTPUT_BYTES = 2_000_000_000


class VerificationError(RuntimeError):
    """Fail-closed independent verification error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def strict_regular_under(path: Path, parent: Path, max_bytes: int) -> None:
    need(path.parent == parent, "PATH_PARENT:" + path.name)
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise VerificationError("PATH_MISSING:" + path.name) from error
    need(not stat.S_ISLNK(metadata.st_mode), "PATH_SYMLINK:" + path.name)
    need(stat.S_ISREG(metadata.st_mode), "PATH_NONREGULAR:" + path.name)
    need(metadata.st_nlink == 1, "PATH_HARDLINK:" + path.name)
    need(0 < metadata.st_size <= max_bytes, "PATH_SIZE:" + path.name)


def safe_path(filename: str) -> Path:
    need(Path(filename).name == filename, "UNSAFE_FILENAME:" + filename)
    path = HERE / filename
    strict_regular_under(path, HERE, MAX_FILE_BYTES)
    return path


def verify_actual_pin(filename: str, expected: str) -> None:
    need(PIN_RE.fullmatch(expected) is not None, "INVALID_PIN:" + filename)
    need(file_sha256(safe_path(filename)) == expected, "PIN_MISMATCH:" + filename)


def parse_manifest_bytes(raw: bytes, label: str) -> dict[str, str]:
    need(b"\x00" not in raw, "MANIFEST_NUL:" + label)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise VerificationError("MANIFEST_NON_UTF8:" + label) from error
    need(text.endswith("\n"), "MANIFEST_FINAL_NEWLINE:" + label)
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
        need(match is not None, "MANIFEST_SYNTAX:" + label)
        value, member = match.groups()
        need(Path(member).name == member, "MANIFEST_MEMBER_PATH:" + label)
        need(member not in rows, "MANIFEST_DUPLICATE:" + label)
        rows[member] = value
    return rows


def parse_manifest(filename: str) -> dict[str, str]:
    return parse_manifest_bytes(safe_path(filename).read_bytes(), filename)


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(len(raw) <= 10_000_000, "JSON_SIZE:" + label)
    need(b"\x00" not in raw, "JSON_NUL:" + label)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise VerificationError("JSON_NON_UTF8:" + label) from error

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            need(key not in result, "JSON_DUPLICATE:" + label)
            result[key] = value
        return result

    def integer(token: str) -> int:
        need(len(token.lstrip("-")) <= 19, "JSON_HUGE_INTEGER:" + label)
        return int(token)

    def reject_float(_token: str) -> float:
        raise VerificationError("JSON_FLOAT:" + label)

    def reject_constant(_token: str) -> float:
        raise VerificationError("JSON_NONFINITE:" + label)

    try:
        value = json.loads(
            text,
            object_pairs_hook=pairs,
            parse_int=integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise VerificationError("JSON_DOCUMENT:" + label) from error
    need(type(value) is dict, "JSON_NOT_OBJECT:" + label)
    return value


def load_json(filename: str) -> dict[str, Any]:
    raw = safe_path(filename).read_bytes()
    value = strict_json_bytes(raw, filename)
    need(
        raw in (canonical(value), canonical(value) + b"\n"),
        "JSON_NONCANONICAL:" + filename,
    )
    return value


def verify_self_hash(value: dict[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    need(type(claimed) is str and PIN_RE.fullmatch(claimed) is not None,
         "SELF_FIELD:" + label)
    payload = dict(value)
    payload.pop(field)
    need(digest(payload) == claimed, "SELF_MISMATCH:" + label)


def strict_gzip_bytes(raw: bytes, label: str, cap: int = 1_000_000) -> int:
    need(
        raw[:10] == bytes.fromhex("1f8b08000000000002ff"),
        "GZIP_HEADER:" + label,
    )
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    output = decoder.decompress(raw)
    output += decoder.flush()
    need(decoder.eof, "GZIP_TRUNCATED:" + label)
    need(not decoder.unused_data, "GZIP_TRAILING_OR_MULTIMEMBER:" + label)
    need(not decoder.unconsumed_tail, "GZIP_UNCONSUMED:" + label)
    need(len(output) <= cap, "GZIP_CAP:" + label)
    return len(output)


def verify_gzip_file(filename: str) -> int:
    path = safe_path(filename)
    with path.open("rb") as stream:
        header = stream.read(10)
        need(
            header == bytes.fromhex("1f8b08000000000002ff"),
            "GZIP_HEADER:" + filename,
        )
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        total = len(decoder.decompress(header))
        while True:
            piece = stream.read(1 << 20)
            if not piece:
                break
            output = decoder.decompress(piece)
            total += len(output)
            need(total <= MAX_GZIP_OUTPUT_BYTES, "GZIP_CAP:" + filename)
            need(not decoder.unconsumed_tail, "GZIP_UNCONSUMED:" + filename)
        total += len(decoder.flush())
    need(decoder.eof, "GZIP_TRUNCATED:" + filename)
    need(not decoder.unused_data, "GZIP_TRAILING_OR_MULTIMEMBER:" + filename)
    need(total <= MAX_GZIP_OUTPUT_BYTES, "GZIP_CAP:" + filename)
    return total


def verify_manifest_package(
    manifest: str,
    manifest_pin: str,
    expected: dict[str, str],
) -> None:
    verify_actual_pin(manifest, manifest_pin)
    need(parse_manifest(manifest) == expected, "MANIFEST_EXACT_SET:" + manifest)
    for member, value in sorted(expected.items()):
        verify_actual_pin(member, value)


def validate_semantics() -> None:
    r292a = load_json(R292A_VERIFICATION)
    r294 = load_json(R294_RESULT)
    verification = load_json(R294_VERIFICATION)
    attacks = load_json(R294_ATTACKS)
    verify_self_hash(r292a, "verification_sha256", "Round292A verification")
    verify_self_hash(r294, "result_sha256", "Round294 result")
    verify_self_hash(verification, "verification_sha256", "Round294 verification")
    verify_self_hash(attacks, "attack_suite_sha256", "Round294 attacks")

    r292_reconstruction = r292a.get("independent_reconstruction", {})
    census = r294.get("census", {})
    rejection = r294.get("superseded_census_rejection", {})
    verified = verification.get("verified_census", {})
    audit = verification.get("attack_audit", {})
    nonpromotion = verification.get("post_registry_nonpromotion", {})
    need(
        r292a.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND292_R287_REGISTRY_OVERLAP"
        )
        and r292_reconstruction.get("registry_occurrence_count") == 421_804
        and r292_reconstruction.get("Round287_support_union_count") == 10_020
        and r292_reconstruction.get("refined_new_support_component_count") == 9_404
        and r292_reconstruction.get(
            "pairwise_unresolved_positive_overlap_count"
        ) == 0,
        "ROUND292A_SEMANTICS",
    )
    need(
        census.get("formal_occurrence_registry_row_count") == 431_208
        and census.get("formal_representation_binding_count") == 46_288
        and census.get("preserved_Round266_occurrence_count") == 126_468
        and census.get("formal_new_Round288_atom_occurrence_count") == 295_336
        and census.get("formal_new_refined_Round287_occurrence_count") == 9_404
        and census.get("formal_new_occurrence_count") == 304_740
        and census.get("formal_occurrence_ID_issued_by_binding_rows") == 0,
        "ROUND294_CENSUS",
    )
    need(
        verified.get("formal_occurrence_registry_row_count") == 431_208
        and verified.get("formal_representation_binding_count") == 46_288
        and verified.get("direct_Round287_union_issuance_count_rejected") == 10_020
        and verified.get("superseded_registry_row_count_rejected") == 431_824,
        "ROUND294_VERIFIED_CENSUS",
    )
    need(
        rejection.get("direct_Round287_union_issuance_accepted") is False
        and rejection.get("superseded_direct_Round287_union_issuance_count")
        == 10_020
        and rejection.get("superseded_registry_row_count") == 431_824
        and rejection.get("superseded_registry_row_count_accepted") is False,
        "ROUND294_REJECTIONS",
    )
    need(
        audit.get("attack_count") == 41
        and audit.get("rejected_attack_count") == 41
        and audit.get("direct_R287_10020_issuance_explicitly_rejected")
        is True
        and audit.get("superseded_431824_explicitly_rejected") is True
        and audit.get("legacy_63224_as_current_quotient_explicitly_rejected")
        is True
        and attacks.get("all_attacks_rejected") is True,
        "ROUND294_ATTACKS",
    )
    need(
        nonpromotion.get("post_Round294_component_DSU_status") == "NOT_REBUILT"
        and nonpromotion.get("post_Round294_quotient_component_count") is None,
        "ROUND294_NONPROMOTION",
    )
    dependency_bytes = canonical({
        "result": r294.get("input_file_pins", {}),
        "verification": verification.get("artifact_pins", {}),
        "r292a": R292A_MEMBER_PINS,
        "r294": R294_MEMBER_PINS,
    })
    need(
        DENIED_R292B_FRAGMENT.encode() not in dependency_bytes,
        "NONADMISSIBLE_R292B_DEPENDENCY",
    )


def build_expected_result() -> dict[str, Any]:
    strict_regular_under(PRODUCER, HERE, MAX_FILE_BYTES)
    need(file_sha256(PRODUCER) == EXPECTED_PRODUCER_SHA256,
         "ROUND294B_PRODUCER_PIN")
    for filename, expected in sorted(DIRECT_FILE_PINS.items()):
        verify_actual_pin(filename, expected)
    verify_manifest_package(
        R292A_MANIFEST,
        DIRECT_FILE_PINS[R292A_MANIFEST],
        R292A_MEMBER_PINS,
    )
    verify_manifest_package(
        R294_MANIFEST,
        DIRECT_FILE_PINS[R294_MANIFEST],
        R294_MEMBER_PINS,
    )
    registry_uncompressed = verify_gzip_file(R294_REGISTRY)
    binding_uncompressed = verify_gzip_file(R294_BINDINGS)
    validate_semantics()
    expected: dict[str, Any] = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND294B_ZERO_CREDIT_REGISTRY_BUILDER_ADMISSION__"
            "R292A_ACTUAL_VERIFIER_AND_MANIFEST_DIRECTLY_PINNED__"
            "R292A_7_MEMBER_AND_R294_9_MEMBER_EXACT_SETS__"
            "431208_REGISTRY_ROWS__46288_BINDINGS__"
            "10020_AND_431824_AND_LEGACY_63224_REJECTED"
        ),
        "provenance": {
            "producer_sha256": EXPECTED_PRODUCER_SHA256,
            "seed_affects_output": False,
            "Round292A_or_Round294_producer_imported_or_executed": False,
            "Round294_artifact_modified": False,
        },
        "direct_actual_file_pins": dict(sorted(DIRECT_FILE_PINS.items())),
        "manifest_exact_set_audit": {
            "Round292A_manifest_member_count": 7,
            "Round292A_manifest_members_sha256": digest(
                dict(sorted(R292A_MEMBER_PINS.items()))
            ),
            "Round292A_actual_verifier_entry_matches_direct_pin": True,
            "Round294_manifest_member_count": 9,
            "Round294_manifest_members_sha256": digest(
                dict(sorted(R294_MEMBER_PINS.items()))
            ),
            "all_16_manifest_members_actual_regular_nonsymlink_single_link": True,
            "all_16_manifest_members_match_exact_sha256": True,
        },
        "full_Round294_package_pins": {
            "manifest_filename": R294_MANIFEST,
            "manifest_sha256": DIRECT_FILE_PINS[R294_MANIFEST],
            "members": dict(sorted(R294_MEMBER_PINS.items())),
            "registry_ledger_uncompressed_bytes": registry_uncompressed,
            "representation_binding_ledger_uncompressed_bytes":
                binding_uncompressed,
        },
        "verified_registry_census": {
            "formal_occurrence_registry_row_count": 431_208,
            "preserved_Round266_occurrence_count": 126_468,
            "formal_new_Round288_atom_occurrence_count": 295_336,
            "formal_new_refined_Round287_occurrence_count": 9_404,
            "formal_new_occurrence_count": 304_740,
            "formal_representation_binding_count": 46_288,
            "formal_occurrence_ID_issued_by_binding_rows": 0,
        },
        "explicit_rejection_contract": {
            "direct_Round287_union_issuance_count_rejected": 10_020,
            "superseded_registry_row_count_rejected": 431_824,
            "legacy_pre_Round294_quotient_component_count": 63_224,
            "legacy_63224_accepted_as_current_quotient": False,
            "nonadmissible_Round292B_consumed": False,
        },
        "formal_credit_transition": {
            "formal_registry_delta": 0,
            "formal_representation_binding_delta": 0,
            "formal_new_occurrence_ID_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "downstream_admission_contract": {
            "new_downstream_consumers_must_pin_Round294B_manifest": True,
            "new_downstream_consumers_must_pin_Round294B_verification": True,
            "historical_Round294_or_Round295_plus_artifacts_rewritten": False,
            "Round294B_is_evidence_admission_only": True,
        },
        "strict_nonpromotion": {
            "formal_registry_row_count": 431_208,
            "formal_representation_binding_count": 46_288,
            "post_Round294_expanded_registry_component_DSU_status":
                "NOT_REBUILT",
            "post_Round294_quotient_component_count": None,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "seed_affects_output": False,
    }
    expected["result_sha256"] = digest(expected)
    return expected


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    target: Any = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def validate_candidate_object(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    verify_self_hash(candidate, "result_sha256", "Round294B candidate")
    need(candidate == expected, "ROUND294B_CANDIDATE_EXACT_EXPECTED")


def expect_rejected(label: str, action: Callable[[], None]) -> None:
    try:
        action()
    except (VerificationError, OSError, ValueError, zlib.error):
        return
    raise VerificationError("ATTACK_ACCEPTED:" + label)


def resigned_attack(
    expected: dict[str, Any],
    attack_id: str,
    path: tuple[str, ...],
    replacement: Any,
) -> dict[str, str]:
    forged = copy.deepcopy(expected)
    set_path(forged, path, replacement)
    forged.pop("result_sha256")
    forged["result_sha256"] = digest(forged)
    expect_rejected(
        attack_id,
        lambda: validate_candidate_object(forged, expected),
    )
    return {
        "attack_id": attack_id,
        "classification": "RESIGNED_SEMANTIC_OR_PIN_FORGERY",
        "disposition": "REJECTED",
    }


def deterministic_gzip(payload: bytes) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0
    ) as stream:
        stream.write(payload)
    return output.getvalue()


def build_attack_suite(expected: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    mutations = [
        (
            "A01_R292A_ACTUAL_VERIFIER_PIN_SUBSTITUTION",
            ("direct_actual_file_pins", R292A_VERIFIER),
            "0" * 64,
        ),
        (
            "A02_R292A_MANIFEST_PIN_SUBSTITUTION",
            ("direct_actual_file_pins", R292A_MANIFEST),
            "1" * 64,
        ),
        (
            "A03_R294_MANIFEST_PIN_SUBSTITUTION",
            ("direct_actual_file_pins", R294_MANIFEST),
            "2" * 64,
        ),
        (
            "A04_R292A_VERIFIER_ENTRY_FALSE",
            (
                "manifest_exact_set_audit",
                "Round292A_actual_verifier_entry_matches_direct_pin",
            ),
            False,
        ),
        (
            "A05_R294_MEMBER_COUNT_OMISSION",
            ("manifest_exact_set_audit", "Round294_manifest_member_count"),
            8,
        ),
        (
            "A06_REGISTRY_COUNT_431824",
            ("verified_registry_census", "formal_occurrence_registry_row_count"),
            431_824,
        ),
        (
            "A07_BINDING_COUNT_FORGERY",
            ("verified_registry_census", "formal_representation_binding_count"),
            46_287,
        ),
        (
            "A08_FORMAL_NEW_COUNT_FORGERY",
            ("verified_registry_census", "formal_new_occurrence_count"),
            304_741,
        ),
        (
            "A09_BINDING_ROW_ISSUES_ID",
            (
                "verified_registry_census",
                "formal_occurrence_ID_issued_by_binding_rows",
            ),
            1,
        ),
        (
            "A10_DIRECT_10020_ISSUANCE_RESTORED",
            (
                "explicit_rejection_contract",
                "direct_Round287_union_issuance_count_rejected",
            ),
            0,
        ),
        (
            "A11_SUPERSEDED_431824_RESTORED",
            (
                "explicit_rejection_contract",
                "superseded_registry_row_count_rejected",
            ),
            0,
        ),
        (
            "A12_LEGACY_63224_AS_CURRENT",
            (
                "explicit_rejection_contract",
                "legacy_63224_accepted_as_current_quotient",
            ),
            True,
        ),
        (
            "A13_NONADMISSIBLE_R292B_CONSUMED",
            (
                "explicit_rejection_contract",
                "nonadmissible_Round292B_consumed",
            ),
            True,
        ),
        (
            "A14_DSU_REBUILT_FORGERY",
            (
                "strict_nonpromotion",
                "post_Round294_expanded_registry_component_DSU_status",
            ),
            "REBUILT",
        ),
        (
            "A15_QUOTIENT_63224_FORGERY",
            (
                "strict_nonpromotion",
                "post_Round294_quotient_component_count",
            ),
            63_224,
        ),
        (
            "A16_NONZERO_DSU_CREDIT",
            ("formal_credit_transition", "formal_DSU_rank_reduction_credit"),
            1,
        ),
        (
            "A17_DOWNSTREAM_MANIFEST_PIN_DISABLED",
            (
                "downstream_admission_contract",
                "new_downstream_consumers_must_pin_Round294B_manifest",
            ),
            False,
        ),
    ]
    for attack_id, path, replacement in mutations:
        rows.append(resigned_attack(expected, attack_id, path, replacement))

    json_attacks: list[tuple[str, bytes]] = [
        ("A18_JSON_DUPLICATE_KEY", b'{"x":1,"x":2}'),
        ("A19_JSON_TRAILING_DOCUMENT", b'{}{}'),
        ("A20_JSON_FLOAT", b'{"x":1.5}'),
        ("A21_JSON_NAN", b'{"x":NaN}'),
        ("A22_JSON_HUGE_INTEGER", b'{"x":123456789012345678901}'),
        ("A23_JSON_NON_UTF8", b'{"x":"\xff"}'),
        ("A24_JSON_NUL", b'{"x":"\x00"}'),
    ]
    for attack_id, payload in json_attacks:
        expect_rejected(
            attack_id,
            lambda payload=payload, attack_id=attack_id:
                strict_json_bytes(payload, attack_id),
        )
        rows.append({
            "attack_id": attack_id,
            "classification": "STRICT_JSON_ATTACK",
            "disposition": "REJECTED",
        })

    base_manifest = (
        "0" * 64 + "  a.txt\n"
        + "1" * 64 + "  b.txt\n"
    ).encode()
    manifest_attacks = [
        ("A25_MANIFEST_DUPLICATE_MEMBER", base_manifest + ("2" * 64 + "  a.txt\n").encode()),
        ("A26_MANIFEST_PATH_TRAVERSAL", ("0" * 64 + "  ../a.txt\n").encode()),
        ("A27_MANIFEST_NO_FINAL_NEWLINE", base_manifest.rstrip(b"\n")),
        ("A28_MANIFEST_MALFORMED_HASH", b"xyz  a.txt\n"),
    ]
    for attack_id, payload in manifest_attacks:
        expect_rejected(
            attack_id,
            lambda payload=payload, attack_id=attack_id:
                parse_manifest_bytes(payload, attack_id),
        )
        rows.append({
            "attack_id": attack_id,
            "classification": "STRICT_MANIFEST_ATTACK",
            "disposition": "REJECTED",
        })

    with tempfile.TemporaryDirectory(prefix="cm2-r294b-path-") as temporary:
        root = Path(temporary)
        source = root / "source"
        source.write_bytes(b"x")
        symlink = root / "symlink"
        symlink.symlink_to(source)
        hardlink = root / "hardlink"
        os.link(source, hardlink)
        fifo = root / "fifo"
        os.mkfifo(fifo)
        directory = root / "directory"
        directory.mkdir()
        missing = root / "missing"
        outside = root.parent / "outside-r294b"
        path_attacks = [
            ("A29_PATH_SYMLINK", symlink, root),
            ("A30_PATH_HARDLINK", hardlink, root),
            ("A31_PATH_FIFO", fifo, root),
            ("A32_PATH_DIRECTORY", directory, root),
            ("A33_PATH_MISSING", missing, root),
            ("A34_PATH_PARENT_ESCAPE", outside, root),
        ]
        for attack_id, path, parent in path_attacks:
            expect_rejected(
                attack_id,
                lambda path=path, parent=parent:
                    strict_regular_under(path, parent, 100),
            )
            rows.append({
                "attack_id": attack_id,
                "classification": "STRICT_PATH_FILE_OBJECT_ATTACK",
                "disposition": "REJECTED",
            })

    good_gzip = deterministic_gzip(b'{"x":1}')
    gzip_attacks = [
        ("A35_GZIP_TRUNCATED", good_gzip[:-3]),
        ("A36_GZIP_CONCATENATED_MEMBER", good_gzip + good_gzip),
        ("A37_GZIP_TRAILING_BYTES", good_gzip + b"x"),
        (
            "A38_GZIP_NONDETERMINISTIC_HEADER",
            good_gzip[:4] + b"\x01\x00\x00\x00" + good_gzip[8:],
        ),
    ]
    for attack_id, payload in gzip_attacks:
        expect_rejected(
            attack_id,
            lambda payload=payload, attack_id=attack_id:
                strict_gzip_bytes(payload, attack_id),
        )
        rows.append({
            "attack_id": attack_id,
            "classification": "STRICT_GZIP_ATTACK",
            "disposition": "REJECTED",
        })

    suite: dict[str, Any] = {
        "schema": ATTACK_SCHEMA,
        "status": "PASS_ALL_38_ROUND294B_ADMISSION_ATTACKS_REJECTED",
        "attack_count": len(rows),
        "rejected_attack_count": len(rows),
        "accepted_attack_count": 0,
        "all_attacks_rejected": True,
        "rows": rows,
    }
    need(len(rows) == 38, "ATTACK_COUNT")
    suite["attack_suite_sha256"] = digest(suite)
    return suite


def build_verification() -> tuple[dict[str, Any], dict[str, Any]]:
    expected = build_expected_result()
    attacks = build_attack_suite(expected)
    candidate_opened_after_expected_reconstruction = True
    candidate_raw = safe_path(CANDIDATE.name).read_bytes()
    candidate = strict_json_bytes(candidate_raw, CANDIDATE.name)
    need(candidate_raw == canonical(candidate), "CANDIDATE_CANONICAL_BYTES")
    validate_candidate_object(candidate, expected)

    verification: dict[str, Any] = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND294B_ZERO_CREDIT_ADMISSION__"
            "ACTUAL_R292A_VERIFIER_DIRECT_PIN__7_PLUS_9_EXACT_MANIFESTS__"
            "431208_REGISTRY_ROWS__46288_BINDINGS__38_OF_38_ATTACKS_REJECTED"
        ),
        "candidate_artifacts": {
            "producer_filename": PRODUCER.name,
            "producer_sha256": EXPECTED_PRODUCER_SHA256,
            "verifier_filename": Path(__file__).name,
            "verifier_sha256": file_sha256(Path(__file__).resolve()),
            "result_filename": CANDIDATE.name,
            "result_file_sha256": hashlib.sha256(candidate_raw).hexdigest(),
            "result_sha256": candidate["result_sha256"],
        },
        "independence_contract": {
            "Round294B_producer_imported_or_executed": False,
            "Round292A_or_Round294_producer_imported_or_executed": False,
            "candidate_opened_after_complete_expected_reconstruction":
                candidate_opened_after_expected_reconstruction,
            "candidate_used_as_expected_oracle": False,
            "cache_pickle_or_pyc_input_used": False,
        },
        "direct_actual_file_audit": {
            "Round292_builder_sha256": DIRECT_FILE_PINS[R292_BUILDER],
            "Round292A_actual_verifier_sha256":
                DIRECT_FILE_PINS[R292A_VERIFIER],
            "Round292A_manifest_sha256": DIRECT_FILE_PINS[R292A_MANIFEST],
            "Round294_manifest_sha256": DIRECT_FILE_PINS[R294_MANIFEST],
            "all_direct_files_actual_regular_nonsymlink_single_link": True,
        },
        "manifest_exact_set_audit": {
            "Round292A_member_count": 7,
            "Round294_member_count": 9,
            "all_16_members_actual_hash_match": True,
            "extra_or_missing_member_count": 0,
        },
        "independent_registry_census": {
            "formal_occurrence_registry_row_count": 431_208,
            "formal_representation_binding_count": 46_288,
            "formal_new_occurrence_count": 304_740,
            "binding_rows_issuing_occurrence_ID_count": 0,
            "direct_Round287_union_issuance_count_rejected": 10_020,
            "superseded_registry_row_count_rejected": 431_824,
            "legacy_63224_as_current_quotient_rejected": True,
        },
        "attack_audit": {
            "attack_count": attacks["attack_count"],
            "rejected_attack_count": attacks["rejected_attack_count"],
            "accepted_attack_count": attacks["accepted_attack_count"],
            "all_attacks_rejected": attacks["all_attacks_rejected"],
            "attack_suite_sha256": attacks["attack_suite_sha256"],
        },
        "strict_boundary": {
            "single_document_duplicate_free_integral_finite_JSON": True,
            "canonical_candidate_JSON_bytes": True,
            "exact_set_manifests": True,
            "deterministic_single_member_trailing_free_bounded_GZIP": True,
            "HERE_only_regular_nonsymlink_single_link_files": True,
        },
        "strict_nonpromotion": expected["strict_nonpromotion"],
        "formal_credit_transition": expected["formal_credit_transition"],
        "seed_affects_output": False,
    }
    verification["verification_sha256"] = digest(verification)
    return verification, attacks


def atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=294_271)
    parser.add_argument("--output", type=Path, default=VERIFICATION)
    parser.add_argument("--attack-output", type=Path, default=ATTACKS)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    verification, attacks = build_verification()
    verification_payload = canonical(verification)
    attack_payload = canonical(attacks)
    if not arguments.no_write:
        need(
            arguments.output.resolve().parent == HERE
            and arguments.attack_output.resolve().parent == HERE,
            "OUTPUT_OUTSIDE_DELIVERABLES",
        )
        atomic_write(arguments.output, verification_payload)
        atomic_write(arguments.attack_output, attack_payload)
    print(verification["status"])
    print("verification_sha256=" + verification["verification_sha256"])
    print(
        "verification_file_sha256="
        + hashlib.sha256(verification_payload).hexdigest()
    )
    print("attack_suite_sha256=" + attacks["attack_suite_sha256"])
    print("attack_file_sha256=" + hashlib.sha256(attack_payload).hexdigest())


if __name__ == "__main__":
    main()
