#!/usr/bin/env python3
"""Round294-B zero-credit registry-builder admission closure.

Round294 is immutable and mathematically sealed, but its producer directly
pins the Round292-A result, ledger, verification, and manifest without
directly pinning the actual independent-verifier source file.  This wrapper
closes that admission-boundary omission without rebuilding or rewriting any
Round294 artifact.

The wrapper directly hashes the inert Round292 registry builder, the actual
Round292-A verifier source, and the Round292-A manifest.  It requires exact
manifest member sets for the complete Round292-A and Round294 packages,
validates every actual member, rechecks the promoted census and explicit
superseded-census rejections, and emits only a zero-credit admission result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round294b_source_g_registry_builder_admission_closure"
RESULT = HERE / f"{PREFIX}_result.json"
SCHEMA = "cm2.round294b.source-g-registry-builder-admission-closure.v1"

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


class AdmissionError(RuntimeError):
    """Fail-closed admission-boundary error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AdmissionError(label)


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


def safe_path(filename: str) -> Path:
    need(Path(filename).name == filename, "UNSAFE_FILENAME:" + filename)
    path = HERE / filename
    need(path.parent == HERE, "PATH_ESCAPE:" + filename)
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise AdmissionError("MISSING_FILE:" + filename) from error
    need(not stat.S_ISLNK(metadata.st_mode), "SYMLINK_FILE:" + filename)
    need(stat.S_ISREG(metadata.st_mode), "NONREGULAR_FILE:" + filename)
    need(metadata.st_nlink == 1, "HARDLINK_FILE:" + filename)
    need(0 < metadata.st_size <= MAX_FILE_BYTES, "FILE_SIZE:" + filename)
    return path


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def verify_actual_pin(filename: str, expected: str) -> None:
    need(PIN_RE.fullmatch(expected) is not None, "INVALID_PIN:" + filename)
    need(file_sha256(safe_path(filename)) == expected, "PIN_MISMATCH:" + filename)


def parse_manifest(filename: str) -> dict[str, str]:
    raw = safe_path(filename).read_bytes()
    need(b"\x00" not in raw, "MANIFEST_NUL:" + filename)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise AdmissionError("MANIFEST_NON_UTF8:" + filename) from error
    need(text.endswith("\n"), "MANIFEST_FINAL_NEWLINE:" + filename)
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
        need(match is not None, "MANIFEST_SYNTAX:" + filename)
        value, member = match.groups()
        need(Path(member).name == member, "MANIFEST_MEMBER_PATH:" + member)
        need(member not in rows, "MANIFEST_DUPLICATE_MEMBER:" + member)
        rows[member] = value
    return rows


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(len(raw) <= 10_000_000, "JSON_SIZE:" + label)
    need(b"\x00" not in raw, "JSON_NUL:" + label)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise AdmissionError("JSON_NON_UTF8:" + label) from error

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            need(key not in result, "JSON_DUPLICATE_KEY:" + label + ":" + key)
            result[key] = value
        return result

    def integer(token: str) -> int:
        need(len(token.lstrip("-")) <= 19, "JSON_HUGE_INTEGER:" + label)
        return int(token)

    def reject_float(_token: str) -> float:
        raise AdmissionError("JSON_FLOAT:" + label)

    def reject_constant(_token: str) -> float:
        raise AdmissionError("JSON_NONFINITE:" + label)

    try:
        value = json.loads(
            text,
            object_pairs_hook=pairs,
            parse_int=integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise AdmissionError("JSON_DOCUMENT:" + label) from error
    need(type(value) is dict, "JSON_NOT_OBJECT:" + label)
    return value


def load_json(filename: str, canonical_file: bool = True) -> dict[str, Any]:
    raw = safe_path(filename).read_bytes()
    value = strict_json_bytes(raw, filename)
    if canonical_file:
        need(
            raw in (canonical(value), canonical(value) + b"\n"),
            "JSON_NONCANONICAL_BYTES:" + filename,
        )
    return value


def verify_self_hash(value: dict[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    need(type(claimed) is str and PIN_RE.fullmatch(claimed) is not None,
         "SELF_HASH_FIELD:" + label)
    payload = dict(value)
    payload.pop(field)
    need(digest(payload) == claimed, "SELF_HASH_MISMATCH:" + label)


def verify_gzip_file(filename: str) -> int:
    path = safe_path(filename)
    with path.open("rb") as stream:
        header = stream.read(10)
        need(
            header == bytes.fromhex("1f8b08000000000002ff"),
            "GZIP_NONDETERMINISTIC_HEADER:" + filename,
        )
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        total = len(decoder.decompress(header))
        while True:
            piece = stream.read(1 << 20)
            if not piece:
                break
            output = decoder.decompress(piece)
            total += len(output)
            need(total <= MAX_GZIP_OUTPUT_BYTES, "GZIP_OUTPUT_CAP:" + filename)
            need(not decoder.unconsumed_tail, "GZIP_UNCONSUMED:" + filename)
        total += len(decoder.flush())
    need(decoder.eof, "GZIP_TRUNCATED:" + filename)
    need(not decoder.unused_data, "GZIP_TRAILING_OR_MULTIMEMBER:" + filename)
    need(total <= MAX_GZIP_OUTPUT_BYTES, "GZIP_OUTPUT_CAP:" + filename)
    return total


def verify_manifest_package(
    manifest_name: str,
    manifest_pin: str,
    expected_members: dict[str, str],
) -> None:
    verify_actual_pin(manifest_name, manifest_pin)
    observed = parse_manifest(manifest_name)
    need(observed == expected_members, "MANIFEST_EXACT_SET:" + manifest_name)
    for member, expected in sorted(expected_members.items()):
        verify_actual_pin(member, expected)


def validate_upstream_semantics() -> None:
    r292a = load_json(R292A_VERIFICATION)
    verify_self_hash(r292a, "verification_sha256", "Round292A verification")
    need(
        r292a.get("status", "").startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND292_R287_REGISTRY_OVERLAP"
        ),
        "ROUND292A_VERIFICATION_STATUS",
    )
    reconstruction = r292a.get("independent_reconstruction", {})
    attacks = r292a.get("targeted_reclosed_attacks", {})
    need(
        reconstruction.get("registry_occurrence_count") == 421_804
        and reconstruction.get("Round287_support_union_count") == 10_020
        and reconstruction.get("refined_new_support_component_count") == 9_404
        and reconstruction.get("pairwise_unresolved_positive_overlap_count") == 0
        and attacks.get("attack_count") == 31
        and attacks.get("rejected_attack_count") == 31,
        "ROUND292A_VERIFIED_CENSUS",
    )

    result = load_json(R294_RESULT)
    verification = load_json(R294_VERIFICATION)
    attack_suite = load_json(R294_ATTACKS)
    verify_self_hash(result, "result_sha256", "Round294 result")
    verify_self_hash(verification, "verification_sha256", "Round294 verification")
    verify_self_hash(attack_suite, "attack_suite_sha256", "Round294 attacks")

    census = result.get("census", {})
    rejection = result.get("superseded_census_rejection", {})
    verified = verification.get("verified_census", {})
    attack_audit = verification.get("attack_audit", {})
    nonpromotion = verification.get("post_registry_nonpromotion", {})
    need(
        census.get("formal_occurrence_registry_row_count") == 431_208
        and census.get("formal_representation_binding_count") == 46_288
        and census.get("preserved_Round266_occurrence_count") == 126_468
        and census.get("formal_new_occurrence_count") == 304_740
        and census.get("formal_occurrence_ID_issued_by_binding_rows") == 0,
        "ROUND294_RESULT_CENSUS",
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
        "ROUND294_SUPERSEDED_REJECTION",
    )
    need(
        attack_audit.get("attack_count") == 41
        and attack_audit.get("rejected_attack_count") == 41
        and attack_audit.get("direct_R287_10020_issuance_explicitly_rejected")
        is True
        and attack_audit.get("superseded_431824_explicitly_rejected") is True
        and attack_audit.get("legacy_63224_as_current_quotient_explicitly_rejected")
        is True
        and attack_suite.get("all_attacks_rejected") is True,
        "ROUND294_ATTACK_REJECTION",
    )
    need(
        nonpromotion.get("post_Round294_component_DSU_status") == "NOT_REBUILT"
        and nonpromotion.get("post_Round294_quotient_component_count") is None,
        "ROUND294_NONPROMOTION",
    )
    serialized_dependencies = canonical({
        "result_inputs": result.get("input_file_pins", {}),
        "verification_inputs": verification.get("artifact_pins", {}),
        "r292a_manifest": R292A_MEMBER_PINS,
        "r294_manifest": R294_MEMBER_PINS,
    }).decode("utf-8")
    need(
        DENIED_R292B_FRAGMENT not in serialized_dependencies,
        "NONADMISSIBLE_R292B_DEPENDENCY",
    )


def build_result() -> dict[str, Any]:
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
    validate_upstream_semantics()

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND294B_ZERO_CREDIT_REGISTRY_BUILDER_ADMISSION__"
            "R292A_ACTUAL_VERIFIER_AND_MANIFEST_DIRECTLY_PINNED__"
            "R292A_7_MEMBER_AND_R294_9_MEMBER_EXACT_SETS__"
            "431208_REGISTRY_ROWS__46288_BINDINGS__"
            "10020_AND_431824_AND_LEGACY_63224_REJECTED"
        ),
        "provenance": {
            "producer_sha256": file_sha256(Path(__file__).resolve()),
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
    result["result_sha256"] = digest(result)
    return result


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
    parser.add_argument("--seed", type=int, default=294_201)
    parser.add_argument("--output", type=Path, default=RESULT)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build_result()
    payload = canonical(result)
    if not arguments.no_write:
        need(
            arguments.output.resolve().parent == HERE,
            "OUTPUT_OUTSIDE_DELIVERABLES",
        )
        atomic_write(arguments.output, payload)
    print(result["status"])
    print("result_sha256=" + result["result_sha256"])
    print("result_file_sha256=" + hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
