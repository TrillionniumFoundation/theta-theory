#!/usr/bin/env python3
"""Produce the bounded C30b source-W outgoing-H disposition certificate.

This producer resolves exactly twelve frozen source-W origins.  It grants
integer exclusion credit only to the two origins whose complete outgoing-H
partition is excluded.  The other ten origins are completely disposed as
mixed (they contain a live open side or a typed H=0 seam) and receive zero
exclusion credit.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import os
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable, Iterator

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition"
H_CELL_LEDGER = PREFIX + "_h_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

C30A_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
C30A_SOURCE = C30A_PREFIX + "_producer.py"
C30A_MANIFEST = C30A_PREFIX + "_manifest.sha256"
C30A_SEALED = Path("cm2_round306c30a_sealed")
C30A_RESULT = C30A_SEALED / (C30A_PREFIX + "_result.json")
C30A_CELL_LEDGER = C30A_SEALED / (C30A_PREFIX + "_cell_ledger.jsonl.gz")
C30A_HELD_LEDGER = C30A_SEALED / (
    C30A_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz"
)

R215_PROBE = "cm2_round215_source_w_mixed_algebraic_blocker_probe.py"
R215_CERTIFICATE = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_certificate.json"
)
R215_VERIFICATION = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_verification.json"
)
R215_MANIFEST = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_manifest.sha256"
)
R201_VERIFIER = (
    "cm2_round201_source_w_exact_behind_formal_promotion_verifier.py"
)
R180_VERIFIER = (
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py"
)
R176_VERIFIER = (
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py"
)
R184_PRODUCER = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta.py"
)
R184_CERTIFICATE = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "certificate.json"
)
R184_VERIFICATION = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "verification.json"
)
R184_MANIFEST = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "manifest.sha256"
)
RUNTIME_LOCK = "cm2_round306c30a_python_flint_runtime_lock.json"
RUNTIME_REQUIREMENTS = "cm2_round306c30a_python_flint_requirements.lock"
RUNTIME_AUDITOR = (
    "cm2_round306c30b_python_flint_runtime_attestation_auditor.py"
)
RUNTIME_ATTESTATION = "cm2_round306c30b_python_flint_runtime_attestation.json"
RUNTIME_AUDITOR_SHA256 = (
    "0309dc5710421a5e56b0d1b7b04ef2c5ccf971d054943dc6baf7765e512b76f8"
)
RUNTIME_ATTESTATION_RAW_SHA256 = (
    "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df"
)
RUNTIME_ATTESTATION_PAYLOAD_SHA256 = (
    "1d9aa48715a01bdd224582887fc95be175b8c2dbd47c35136a971874d16ad759"
)

# ``python -I`` implies ``-E`` and therefore ignores ``PYTHONHASHSEED``.
# Producer reproducibility is instead tested in a scrubbed, safe-path process
# launched with ``-P -s -B``.  Only these two independently controlled hash
# seeds and this exact four-variable environment are accepted.  The runtime
# auditor and the independent verifier continue to run separately under
# ``-I -B``.
CONTROLLED_HASH_SEEDS = frozenset({"30630071", "30630929"})
CONTROLLED_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
}
INITIAL_SAFE_SYS_PATH = tuple(sys.path)

PINS = {
    C30A_SOURCE:
        "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714",
    C30A_MANIFEST:
        "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc",
    os.fspath(C30A_RESULT):
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    os.fspath(C30A_CELL_LEDGER):
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    os.fspath(C30A_HELD_LEDGER):
        "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    R215_PROBE:
        "463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1",
    R215_CERTIFICATE:
        "9ad5321f5b29111aabe9f044ee22220c83d8c76ace45383ed34a0255a485a3ec",
    R215_VERIFICATION:
        "9af901607edd4b95f1ec149bb6426a84315de22decbcd331a8d71d727894c519",
    R215_MANIFEST:
        "6a6463c2574b971ce6909593886f6ad4c23bddb232772fdacebb4ecca70a405a",
    R201_VERIFIER:
        "29344dd3c0590ac9d0d3f0618a3f0f034316759468e15af2674813ab72f7ce2b",
    R180_VERIFIER:
        "12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4",
    R176_VERIFIER:
        "f1297881f724cb0a2087ebbfa6961a95750dffa751c003879eb2e14714581796",
    R184_PRODUCER:
        "28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906",
    R184_CERTIFICATE:
        "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f",
    R184_VERIFICATION:
        "7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6",
    R184_MANIFEST:
        "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1",
    RUNTIME_LOCK:
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    RUNTIME_REQUIREMENTS:
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    RUNTIME_AUDITOR:
        RUNTIME_AUDITOR_SHA256,
}

C30A_RESULT_OBJECT_SHA256 = (
    "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
)
BEFORE_EXCLUDED = 74_744
BEFORE_LIVE = 2_088
BEFORE_REMAINING = 92
BEFORE_RESOLVED_NONEXCLUDED = 1_996
AFTER_EXCLUDED = 74_746
AFTER_LIVE = 2_086
AFTER_REMAINING = 80
AFTER_RESOLVED_NONEXCLUDED = 2_006

HELD_KEYS = (
    "W:N:04.00.10101011",
    "W:S:H.04.00.10101011",
)
R215_H_KEYS = (
    "W:N:07.01.01100010",
    "W:N:07.01.01101001",
    "W:N:07.01.01101110",
    "W:N:07.01.11000101",
    "W:N:07.01.11011100",
    "W:S:H.07.01.01100010",
    "W:S:H.07.01.01101001",
    "W:S:H.07.01.01101110",
    "W:S:H.07.01.11000101",
    "W:S:H.07.01.11011100",
)
ORIGIN_KEYS = tuple(sorted(HELD_KEYS + R215_H_KEYS))
EXCLUDED_ORIGIN_KEYS = (
    "W:N:07.01.01100010",
    "W:S:H.07.01.01100010",
)
MIXED_ORIGIN_KEYS = tuple(
    key for key in ORIGIN_KEYS if key not in set(EXCLUDED_ORIGIN_KEYS)
)
EXPECTED_R215_H_CELLS_BY_ORIGIN = {
    "W:N:07.01.01100010": 8,
    "W:N:07.01.01101001": 40,
    "W:N:07.01.01101110": 40,
    "W:N:07.01.11000101": 152,
    "W:N:07.01.11011100": 40,
    "W:S:H.07.01.01100010": 8,
    "W:S:H.07.01.01101001": 40,
    "W:S:H.07.01.01101110": 40,
    "W:S:H.07.01.11000101": 152,
    "W:S:H.07.01.11011100": 40,
}
EXPECTED_H_CELL_DISPOSITION = Counter({
    "EXCLUDED": 352,
    "LIVE": 144,
    "MIXED": 192,
})
EXPECTED_H_CELLS = 688
EXPECTED_H_SOURCE_KIND = Counter({
    "ROUND215_RESIDUAL_OUTGOING_H": 560,
    "ROUND180_INHERITED_OUTGOING_H": 112,
    "ROUND306C30A_HELD_INHERITED_OUTGOING_H": 8,
    "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H": 8,
})
EXPECTED_HYBRID_CELL_KEYS_SHA256 = (
    "df94409e23e48645f02d52b412650f5fa01d43751621677813b99b3095708a98"
)
EXPECTED_HYBRID_TERMINAL_ROWS_SHA256 = (
    "525cf73d888e74282847ffe57b682b3bc9de0c2c4cc32305123d538d51b0003d"
)
EXPECTED_HYBRID_TERMINAL_SHA_LIST_SHA256 = (
    "535e3292640422abae8accdbccc08c9e1845dbe754ddc32fa247a98dc0e0a165"
)
# Filled from an isolated replay of the explicit v1 semantic projection below.
# The obsolete historical complete-return-object digest is not a contract: it
# included schema/row-hash/diagnostic material that legitimately changes when
# the certificate is strengthened.
EXPECTED_HYBRID_ANALYTIC_SEMANTIC_PROJECTION_SHA_LIST_SHA256 = (
    "7aa65c7d779078b89fe745b0883008805db1cb17b4c24806c38199e1dfa8bf28"
)
EXPECTED_HYBRID_TERMINAL_TO_ANALYTIC_SEMANTIC_PROJECTION_SHA256: tuple[
    tuple[str, str], ...
] = (
    (
        "feffdf0b13a596d7f94649258323dcc6607f2355b0f5d4a10942ee7b5cd2f9cd",
        "33714baf9bc53b7d3a05a90306f27fb0103ed59c2b706d2613ccf45dc2e0f12d",
    ),
    (
        "7c4ec648e8bfcc8d3172e70525f7829a8cc270f92356c81e0cd3e4aa38f14eae",
        "f89b7be393a350b36d068cb53ed4fd8dff3ebdc183640fc2c6d944166d3a9d51",
    ),
    (
        "7dcfd22df39dd509c476a42a8b9104c3b69cecd611b3526af4741ee275445b52",
        "ee6c8dda81407cc20a2749e901ee889159969a6dded4f6b9349909d4f073dfeb",
    ),
    (
        "d924df7b2a617278e019a9d18bad84c4077900a7ccf2e3fff75878153814aca7",
        "83f5a10ab849ccb6b7009262a83d2cb5d6cdbb75c7de3a9d853aa9cb416bbb7a",
    ),
    (
        "22286207d8eb06e6f36d78b7e8ac1f8b16b3d6aea21ec0dc3e15a1ce53d1aa8e",
        "42d650e2ff8351d12a9812b33063cab1857c80c9ea43886360d57452ca9ca0be",
    ),
    (
        "dc1e22d52b55fe2a110f54316f6e74fdc09679bea2b325142cd71c94696e4eb1",
        "c3db1475e1f2cec93e377895c2f7b490575fd98d31a5a9d521c9015e2ea9754c",
    ),
    (
        "bbada2b577d389d9605cecc63330790e3b8da8d57309e2c37e646b2c4a51626d",
        "87634cd6dae75dc294856bd2772789d343f845989ce69ceb7bd9f1db274abaff",
    ),
    (
        "ac240a541551abb25a3252394decdfe7e2b16bf7729cf6d87f6939c2c2e440cb",
        "a34e72c6e705cdc8e7690082e68c4483e9cfb9efe1f60f1313d0c72c48c77c42",
    ),
)
EXPECTED_INHERITED_H_BY_ORIGIN = {
    "W:N:04.00.10101011": 4,
    "W:S:H.04.00.10101011": 4,
    "W:N:07.01.01100010": 0,
    "W:N:07.01.01101001": 4,
    "W:N:07.01.01101110": 12,
    "W:N:07.01.11000101": 36,
    "W:N:07.01.11011100": 8,
    "W:S:H.07.01.01100010": 0,
    "W:S:H.07.01.01101001": 4,
    "W:S:H.07.01.01101110": 12,
    "W:S:H.07.01.11000101": 36,
    "W:S:H.07.01.11011100": 8,
}
EXPECTED_INHERITED_FOLLOWUP_H_BY_ORIGIN = {
    key: (4 if key.endswith("07.01.11011100") else 0)
    for key in ORIGIN_KEYS
}
EXPECTED_EXCLUDED_KEYS_SHA256 = (
    "ae9b6dbdeab5163fac6ab992766d019d36fedcbc392a94f7dae7f95370dd317d"
)
EXPECTED_MIXED_KEYS_SHA256 = (
    "507447f2a97f8c804280b2a46de8aef70e7dd7260835edd9ec2a1f22bf155ba8"
)


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def semantic_without_hash_or_aggregate_metadata(value: Any) -> Any:
    """Project semantic content without self hashes or derived aggregates."""
    if isinstance(value, dict):
        return {
            key: semantic_without_hash_or_aggregate_metadata(item)
            for key, item in sorted(value.items())
            if key != "schema"
            and key != "row_sha256"
            and not key.endswith("_sha256")
            and not key.endswith("_row_count")
        }
    if isinstance(value, list):
        return [
            semantic_without_hash_or_aggregate_metadata(item)
            for item in value
        ]
    return value


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def regular_bytes(path: Path, maximum: int = 256 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.is_relative_to(ROOT), "input outside deliverables")
    status = absolute.lstat()
    need(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and 0 < status.st_size <= maximum,
        "input regular singleton:" + absolute.name,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino) == (status.st_dev, status.st_ino)
            and opened.st_size == status.st_size,
            "input race:" + absolute.name,
        )
        output = bytearray()
        while len(output) < opened.st_size:
            block = os.read(descriptor, min(1 << 20, opened.st_size-len(output)))
            need(bool(block), "input short read:" + absolute.name)
            output.extend(block)
        need(not os.read(descriptor, 1), "input growth:" + absolute.name)
    finally:
        os.close(descriptor)
    return bytes(output)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "JSON encoding:" + label)

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "JSON duplicate:" + label)
            output[key] = value
        return output

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=str,
    )
    need(type(value) is dict, "JSON top object:" + label)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    return strict_object(regular_bytes(path), path.name)


def bootstrap_runtime_attestation() -> tuple[bytes, dict[str, Any]]:
    """Audit the installed distribution before importing any FLINT code."""
    need(
        not any(
            name == "flint" or name.startswith("flint.")
            for name in sys.modules
        ),
        "flint modules not preloaded before runtime attestation",
    )
    auditor = ROOT / RUNTIME_AUDITOR
    need(
        hashlib.sha256(regular_bytes(auditor, 4 * 1024 * 1024)).hexdigest()
        == RUNTIME_AUDITOR_SHA256,
        "runtime auditor bootstrap pin",
    )
    completed = subprocess.run(
        [sys.executable, "-I", "-B", os.fspath(auditor)],
        cwd=ROOT.parent,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    raw = completed.stdout
    need(
        completed.returncode == 0
        and completed.stderr == b""
        and raw.endswith(b"\n")
        and raw.count(b"\n") == 1,
        "runtime auditor bootstrap process",
    )
    attestation = strict_object(raw[:-1], RUNTIME_ATTESTATION)
    body = {
        key: value for key, value in attestation.items()
        if key != "attestation_payload_sha256"
    }
    need(
        raw == canonical(attestation) + b"\n"
        and set(attestation) == {
            "attestation_payload_sha256", "auditor", "imported_flint",
            "installed_distribution", "interpreter", "native_runtime",
            "offline", "schema", "sealed_wheel", "trust_roots", "verdict",
        }
        and attestation["schema"]
        == "cm2.round306c30b.python-flint-runtime-attestation.v1"
        and attestation["verdict"] == "PASS"
        and attestation["offline"] is True
        and attestation["auditor"] == {
            "path": "deliverables/" + RUNTIME_AUDITOR,
            "sha256": RUNTIME_AUDITOR_SHA256,
        }
        and attestation["attestation_payload_sha256"] == digest(body)
        == RUNTIME_ATTESTATION_PAYLOAD_SHA256
        and hashlib.sha256(raw).hexdigest()
        == RUNTIME_ATTESTATION_RAW_SHA256
        and attestation["installed_distribution"]["file_count"] == 139
        and attestation["installed_distribution"]["file_table_sha256"]
        == "862c9185021eccf86b89b24f0245c7db67f28c72be00a36a21d7e5745662f83a"
        and attestation["installed_distribution"]["record_raw_sha256"]
        == "a140c3cb2ba819edc913c2adae2dc0a60d49f7f3be547f139b7beb8be9c0d3da"
        and attestation["native_runtime"]["native_file_count"] == 42
        and attestation["native_runtime"]["native_file_table_sha256"]
        == "cf716cb11ace362a84e11c43b97d6170cb2909e281775567cbdd9e530b5a8b24",
        "runtime attestation bootstrap contract",
    )
    return raw, attestation


def manifest_entries() -> dict[str, str]:
    raw = regular_bytes(ROOT / C30A_MANIFEST, 64 * 1024)
    entries: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, "manifest syntax")
        expected, filename = parts
        need(
            filename not in entries
            and not Path(filename).is_absolute()
            and ".." not in Path(filename).parts,
            "manifest path",
        )
        actual = file_hash(ROOT / filename)
        need(actual == expected, "manifest entry:" + filename)
        entries[filename] = expected
    need(
        entries[os.fspath(C30A_RESULT)] == PINS[os.fspath(C30A_RESULT)]
        and entries[os.fspath(C30A_CELL_LEDGER)]
        == PINS[os.fspath(C30A_CELL_LEDGER)]
        and entries[os.fspath(C30A_HELD_LEDGER)]
        == PINS[os.fspath(C30A_HELD_LEDGER)]
        and entries[C30A_SOURCE] == PINS[C30A_SOURCE],
        "C30a manifest required entries",
    )
    return entries


def validate_inputs() -> list[dict[str, str]]:
    pin_map: dict[str, str] = {}
    for filename, expected in sorted(PINS.items()):
        actual = file_hash(ROOT / filename)
        need(actual == expected, "input pin:" + filename)
        pin_map[filename] = actual
    entries = manifest_entries()
    for filename, expected in entries.items():
        previous = pin_map.get(filename)
        need(previous in {None, expected}, "pin/manifest disagreement:" + filename)
        pin_map[filename] = expected
    c30a = strict_json(ROOT / C30A_RESULT)
    need(
        c30a["result_sha256"] == C30A_RESULT_OBJECT_SHA256
        and digest({k: v for k, v in c30a.items() if k != "result_sha256"})
        == C30A_RESULT_OBJECT_SHA256
        and c30a["source_W_ledger_transition"]["after"]["excluded"]
        == BEFORE_EXCLUDED
        and c30a["source_W_ledger_transition"]["after"]["conservative_live"]
        == BEFORE_LIVE
        and c30a["source_W_ledger_transition"]["after"]["remaining"]
        == BEFORE_REMAINING
        and c30a["strict_nonpromotion"]["D02"]
        == "BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS",
        "C30a sealed result",
    )
    r215 = strict_json(ROOT / R215_CERTIFICATE)
    r215v = strict_json(ROOT / R215_VERIFICATION)
    r184v = strict_json(ROOT / R184_VERIFICATION)
    need(
        r215["result"]["status"] == "PARTIAL_FORMAL_ROUND215"
        and r215v["result"]["status"] == "PASS_PARTIAL_FORMAL_ROUND215"
        and r184v["result"]["status"] == "PASS_PARTIAL_BOUNDED_ROUND184",
        "R184/R215 sealed pins",
    )
    return [
        {"filename": filename, "sha256": expected}
        for filename, expected in sorted(pin_map.items())
    ]


def validate_runtime() -> None:
    lock = strict_json(ROOT / RUNTIME_LOCK)
    site_packages = (
        ROOT.parent
        / BOOTSTRAP_RUNTIME_ATTESTATION["installed_distribution"][
            "site_packages_relpath"
        ]
    ).resolve(strict=True)
    installed_files = {
        row["path"]: row["sha256"]
        for row in BOOTSTRAP_RUNTIME_ATTESTATION["installed_distribution"][
            "file_table"
        ]
    }
    loaded_flint_files: dict[str, str] = {}
    for module_name, module in sorted(sys.modules.items()):
        if module_name != "flint" and not module_name.startswith("flint."):
            continue
        for attribute in ("__file__", "__cached__"):
            raw_path = getattr(module, attribute, None)
            if type(raw_path) is not str or not Path(raw_path).exists():
                continue
            resolved = Path(raw_path).resolve(strict=True)
            need(
                resolved.is_relative_to(site_packages),
                "loaded flint file outside attested distribution",
            )
            relative = resolved.relative_to(site_packages).as_posix()
            need(
                installed_files.get(relative) == file_hash(resolved),
                "loaded flint file hash:" + relative,
            )
            loaded_flint_files[module_name + ":" + attribute] = relative
    attested_import = BOOTSTRAP_RUNTIME_ATTESTATION["imported_flint"]
    environment = dict(os.environ)
    seed = environment.pop("PYTHONHASHSEED", None)
    need(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is True
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.no_user_site == 1
        and sys.flags.hash_randomization == 1,
        "scrubbed seeded interpreter flags",
    )
    need(
        "" not in INITIAL_SAFE_SYS_PATH
        and os.fspath(ROOT) not in INITIAL_SAFE_SYS_PATH
        and tuple(
            entry for entry in sys.path if entry != os.fspath(ROOT)
        ) == INITIAL_SAFE_SYS_PATH,
        "safe module search path",
    )
    need(sys.dont_write_bytecode is True, "bytecode writes disabled")
    need(
        seed in CONTROLLED_HASH_SEEDS
        and environment == CONTROLLED_ENVIRONMENT,
        "scrubbed controlled environment",
    )
    need(
        sys.implementation.name == lock["implementation"]
        and os.uname().machine == lock["architecture"]
        and ".".join(str(value) for value in sys.version_info[:3])
        == lock["python_version"]
        and flint.__version__ == lock["python_flint"]
        and flint.__FLINT_VERSION__ == lock["flint_version"]
        and flint.__FLINT_RELEASE__ == lock["flint_release"]
        and sys.modules.get("flint") is flint
        and loaded_flint_files.get("flint:__file__")
        == Path(attested_import["module_file_relpath"]).relative_to(
            BOOTSTRAP_RUNTIME_ATTESTATION["installed_distribution"][
                "site_packages_relpath"
            ]
        ).as_posix()
        and file_hash(Path(flint.__file__).resolve(strict=True))
        == attested_import["module_file_sha256"],
        "locked scrubbed seeded python-flint runtime",
    )


BOOTSTRAP_RUNTIME_ATTESTATION_RAW, BOOTSTRAP_RUNTIME_ATTESTATION = (
    bootstrap_runtime_attestation()
)

import flint
from flint import arb, ctx


validate_runtime()
INPUT_PINS = validate_inputs()
if os.fspath(ROOT) not in sys.path:
    sys.path.insert(0, os.fspath(ROOT))
need(
    not any(
        filename[:-3] in sys.modules
        for filename in (
            C30A_SOURCE, R215_PROBE, R201_VERIFIER,
            R180_VERIFIER, R176_VERIFIER,
        )
    ),
    "upstream mathematics modules not preloaded",
)
c30a = importlib.import_module(C30A_SOURCE[:-3])
r215 = c30a.r215
r201 = r215.r201
r176 = c30a.r176
r180 = c30a.r180


def validate_imported_mathematics() -> None:
    pin_map = {row["filename"]: row["sha256"] for row in INPUT_PINS}
    modules = {
        C30A_SOURCE: c30a,
        R215_PROBE: r215,
        R201_VERIFIER: r201,
        R180_VERIFIER: r180,
        R176_VERIFIER: r176,
    }
    for filename, module in modules.items():
        expected_path = (ROOT / filename).resolve(strict=True)
        actual_path = Path(module.__file__).resolve(strict=True)
        need(
            sys.modules.get(filename[:-3]) is module
            and actual_path == expected_path
            and pin_map.get(filename) == file_hash(actual_path),
            "imported mathematics module identity/hash:" + filename,
        )


validate_imported_mathematics()
validate_runtime()


def sign_name(value: arb) -> str:
    value_sign = r176.sign(value)
    return (
        "STRICT_POSITIVE" if value_sign > 0 else
        "STRICT_NEGATIVE" if value_sign < 0 else "OVERWRAP"
    )


def fraction(value: Q) -> str:
    return str(value)


def coarse_classification(classification: str) -> str:
    if classification in r176.H_EXCLUDED:
        return "EXCLUDED"
    if classification in r176.H_LIVE:
        return "LIVE"
    need(classification == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES",
         "H terminal class")
    return "MIXED"


def sealed_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def point_box(
    box: Any,
    *,
    t_value: Q | None = None,
    p_value: Q | None = None,
) -> Any:
    return r176.Box(
        box.t0 if t_value is None else t_value,
        box.t1 if t_value is None else t_value,
        box.p0 if p_value is None else p_value,
        box.p1 if p_value is None else p_value,
        box.s0,
        box.s1,
        box.depth,
        box.path,
    )


def outgoing_margin_signs(nx: arb, ny: arb) -> dict[str, str]:
    margins = {
        "E.first": nx - ny,
        "E.second": nx + ny,
        "W.first": -nx - ny,
        "W.second": -nx + ny,
        "N.first": ny - nx,
        "N.second": ny + nx,
        "S.first": -ny - nx,
        "S.second": -ny + nx,
    }
    return {key: sign_name(value) for key, value in sorted(margins.items())}


def seam_candidate(chart_id: str, box: Any, seam_id: str) -> dict[str, Any]:
    data = r176.SEAMS[seam_id]
    _cell, nx, ny = r176.tight_contact(chart_id, box)
    normal = data["normal"](nx, ny)
    other = data["other"](nx, ny)
    values = r176.seam_values(chart_id, box, seam_id)
    corner_values = {
        f"t{ti}_p{pi}": r176.seam_values(
            chart_id,
            point_box(box, t_value=t, p_value=p),
            seam_id,
        )["H"]
        for ti, t in enumerate((box.t0, box.t1))
        for pi, p in enumerate((box.p0, box.p1))
    }
    corner_signs = {
        key: sign_name(value) for key, value in sorted(corner_values.items())
    }
    corner_integer_signs = [r176.sign(value) for value in corner_values.values()]
    low = r176.seam_values(
        chart_id, point_box(box, p_value=box.p0), seam_id
    )["H"]
    high = r176.seam_values(
        chart_id, point_box(box, p_value=box.p1), seam_id
    )["H"]
    dt_sign = r176.sign(values["dt"])
    full_graph = bool(low > 0) and bool(high < 0)
    clipped_graph = (
        dt_sign != 0
        and 1 in corner_integer_signs
        and -1 in corner_integer_signs
    )
    typed_preconditions = (
        r176.sign(normal) == 0
        and bool(other < 0)
        and bool(values["forward"] > 0)
        and bool(values["inward"] > 0)
        and dt_sign != 0
        and bool(values["dp"] < 0)
    )
    uniform_corner_sign = (
        corner_integer_signs[0]
        if dt_sign != 0
        and all(value == corner_integer_signs[0]
                for value in corner_integer_signs)
        and corner_integer_signs[0] != 0
        else 0
    )
    outgoing = None
    if uniform_corner_sign:
        outgoing = (
            ("W" if uniform_corner_sign > 0 else "N")
            if seam_id == "NW"
            else ("W" if uniform_corner_sign < 0 else "S")
        )
    return {
        "seam_id": seam_id,
        "adjacent_chart": data["adjacent"],
        "normal_sign": sign_name(normal),
        "other_margin_sign": sign_name(other),
        "H_whole_box_sign": sign_name(values["H"]),
        "forward_sign": sign_name(values["forward"]),
        "inward_sign": sign_name(values["inward"]),
        "dH_dt_sign": sign_name(values["dt"]),
        "dH_dp_sign": sign_name(values["dp"]),
        "p_lower_face_H_sign": sign_name(low),
        "p_upper_face_H_sign": sign_name(high),
        "corner_H_signs": corner_signs,
        "typed_preconditions": typed_preconditions,
        "full_graph": full_graph,
        "clipped_graph": clipped_graph,
        "uniform_outgoing_chart": outgoing,
    }


def crossing(first: str, second: str) -> bool:
    return {first, second} == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


def typed_sheet_materialization(
    chart_id: str,
    box: Any,
    detail: dict[str, Any],
    terminal_id: str,
) -> dict[str, Any]:
    seam_id = detail["seam_id"]
    adjacent = detail["adjacent_chart"]
    corners = detail["corner_H_signs"]
    need(
        detail["typed_preconditions"]
        and (detail["full_graph"] or detail["clipped_graph"])
        and all(value != "OVERWRAP" for value in corners.values()),
        "typed H sheet preconditions:" + terminal_id,
    )
    sign_chart = (
        {"STRICT_POSITIVE": "W", "STRICT_NEGATIVE": "N"}
        if seam_id == "NW"
        else {"STRICT_NEGATIVE": "W", "STRICT_POSITIVE": "S"}
    )
    open_sides = [
        sealed_row({
            "schema": "cm2.round306c30b.H-open-side.row.v1",
            "terminal_id": terminal_id,
            "predicate": predicate,
            "ambient_dimension": 3,
            "outgoing_chart": sign_chart[sign],
            "disposition": (
                "LIVE" if sign_chart[sign] == "W" else "EXCLUDED"
            ),
            "nonempty_positive_measure": True,
            "H_continuity_and_strict_side_sign_proved": True,
            "closed_enclosure_terminal_id": terminal_id,
        })
        for sign, predicate in (
            ("STRICT_NEGATIVE", "H<0"),
            ("STRICT_POSITIVE", "H>0"),
        )
    ]

    t_cross = {
        endpoint: crossing(corners[f"t{ti}_p0"], corners[f"t{ti}_p1"])
        for ti, endpoint in enumerate(("LOWER", "UPPER"))
    }
    p_cross = {
        endpoint: (
            detail["dH_dt_sign"] != "OVERWRAP"
            and crossing(corners[f"t0_p{pi}"], corners[f"t1_p{pi}"])
        )
        for pi, endpoint in enumerate(("LOWER", "UPPER"))
    }
    face_specs = [
        ("t", "LOWER", t_cross["LOWER"], "STRICT_dH_dp_UNIQUE_POINT_X_s"),
        ("t", "UPPER", t_cross["UPPER"], "STRICT_dH_dp_UNIQUE_POINT_X_s"),
        ("p", "LOWER", p_cross["LOWER"], "STRICT_dH_dt_UNIQUE_POINT_X_s"),
        ("p", "UPPER", p_cross["UPPER"], "STRICT_dH_dt_UNIQUE_POINT_X_s"),
        ("s", "LOWER", True, "H_GRAPH_CURVE_AT_FIXED_s"),
        ("s", "UPPER", True, "H_GRAPH_CURVE_AT_FIXED_s"),
    ]
    face_rows = [
        sealed_row({
            "schema": "cm2.round306c30b.H-sheet-face-incidence.row.v1",
            "terminal_id": terminal_id,
            "fixed_axis": axis,
            "boundary_side": side,
            "predicate": "H=0",
            "nonempty": nonempty,
            "dimension_if_nonempty": 1,
            "proof": proof,
            "half_open_outgoing_owner_chart": "W" if nonempty else "NONE",
            "chart_level_half_open_owner": "W" if nonempty else "NONE",
            "closed_enclosure_terminal_id": terminal_id,
            "shadow_chart": adjacent if nonempty else "NONE",
            "disposition": "LIVE" if nonempty else "EMPTY",
            "ambient_dyadic_owner_rule":
                "LOWER_CHILD_OWNS_SPLIT_EQUALITY__LEXICOGRAPHIC_RECURSION",
        })
        for axis, side, nonempty, proof in face_specs
    ]
    face_sign_inputs = [
        ("t", "LOWER", [corners["t0_p0"], corners["t0_p1"]],
         t_cross["LOWER"]),
        ("t", "UPPER", [corners["t1_p0"], corners["t1_p1"]],
         t_cross["UPPER"]),
        ("p", "LOWER", [corners["t0_p0"], corners["t1_p0"]],
         p_cross["LOWER"]),
        ("p", "UPPER", [corners["t0_p1"], corners["t1_p1"]],
         p_cross["UPPER"]),
        ("s", "LOWER", list(corners.values()), True),
        ("s", "UPPER", list(corners.values()), True),
    ]
    face_region_rows: list[dict[str, Any]] = []
    for axis, side, boundary_signs, crosses_face in face_sign_inputs:
        present_signs = (
            {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            if crosses_face else set(boundary_signs)
        )
        need(
            present_signs <= {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and bool(present_signs),
            "typed face strict sign partition",
        )
        need(crosses_face or len(present_signs) == 1,
             "typed face uniform noncrossing sign")
        for sign in ("STRICT_NEGATIVE", "STRICT_POSITIVE"):
            nonempty = sign in present_signs
            outgoing_chart = sign_chart[sign] if nonempty else "NONE"
            face_region_rows.append(sealed_row({
                "schema": (
                    "cm2.round306c30b.H-sheet-face-open-region.row.v1"
                ),
                "terminal_id": terminal_id,
                "fixed_axis": axis,
                "boundary_side": side,
                "predicate": "H<0" if sign == "STRICT_NEGATIVE" else "H>0",
                "H_sign": sign,
                "nonempty": nonempty,
                "dimension_if_nonempty": 2,
                "proof": (
                    "STRICT_MONOTONE_CROSSING_COMPLEMENT_REGION"
                    if crosses_face else "UNIFORM_STRICT_FACE_SIGN"
                ),
                "outgoing_chart": outgoing_chart,
                "chart_level_half_open_owner": (
                    outgoing_chart if nonempty else "NONE"
                ),
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": (
                    "LIVE" if outgoing_chart == "W"
                    else "EXCLUDED" if nonempty else "EMPTY"
                ),
                "H_zero_boundary_row_sha256": next(
                    row["row_sha256"] for row in face_rows
                    if row["fixed_axis"] == axis
                    and row["boundary_side"] == side
                ),
            }))

    edge_rows: list[dict[str, Any]] = []
    edge_sign_inputs: list[tuple[dict[str, str], str, list[str], bool]] = []
    for t_side in ("LOWER", "UPPER"):
        for s_side in ("LOWER", "UPPER"):
            nonempty = t_cross[t_side]
            edge_rows.append(sealed_row({
                "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
                "terminal_id": terminal_id,
                "fixed": {"t": t_side, "s": s_side},
                "free_axis": "p",
                "predicate": "H=0",
                "nonempty": nonempty,
                "dimension_if_nonempty": 0,
                "proof": "STRICT_dH_dp_UNIQUE_POINT",
                "half_open_outgoing_owner_chart": "W" if nonempty else "NONE",
                "chart_level_half_open_owner": "W" if nonempty else "NONE",
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": "LIVE" if nonempty else "EMPTY",
            }))
            ti = 0 if t_side == "LOWER" else 1
            edge_sign_inputs.append((
                {"t": t_side, "s": s_side},
                "p",
                [corners[f"t{ti}_p0"], corners[f"t{ti}_p1"]],
                nonempty,
            ))
    for p_side in ("LOWER", "UPPER"):
        for s_side in ("LOWER", "UPPER"):
            nonempty = p_cross[p_side]
            edge_rows.append(sealed_row({
                "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
                "terminal_id": terminal_id,
                "fixed": {"p": p_side, "s": s_side},
                "free_axis": "t",
                "predicate": "H=0",
                "nonempty": nonempty,
                "dimension_if_nonempty": 0,
                "proof": "STRICT_dH_dt_UNIQUE_POINT",
                "half_open_outgoing_owner_chart": "W" if nonempty else "NONE",
                "chart_level_half_open_owner": "W" if nonempty else "NONE",
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": "LIVE" if nonempty else "EMPTY",
            }))
            pi = 0 if p_side == "LOWER" else 1
            edge_sign_inputs.append((
                {"p": p_side, "s": s_side},
                "t",
                [corners[f"t0_p{pi}"], corners[f"t1_p{pi}"]],
                nonempty,
            ))
    for ti, t_side in enumerate(("LOWER", "UPPER")):
        for pi, p_side in enumerate(("LOWER", "UPPER")):
            need(corners[f"t{ti}_p{pi}"] != "OVERWRAP",
                 "typed sheet corner strict")
            edge_rows.append(sealed_row({
                "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
                "terminal_id": terminal_id,
                "fixed": {"t": t_side, "p": p_side},
                "free_axis": "s",
                "predicate": "H=0",
                "nonempty": False,
                "dimension_if_nonempty": 0,
                "proof": "STRICT_NONZERO_H_AT_t_p_CORNER",
                "H_sign": corners[f"t{ti}_p{pi}"],
                "half_open_outgoing_owner_chart": "NONE",
                "chart_level_half_open_owner": "NONE",
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": "EMPTY",
            }))
            edge_sign_inputs.append((
                {"t": t_side, "p": p_side},
                "s",
                [corners[f"t{ti}_p{pi}"]],
                False,
            ))
    edge_region_rows: list[dict[str, Any]] = []
    for fixed, free_axis, endpoint_signs, crosses_edge in edge_sign_inputs:
        present_signs = (
            {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            if crosses_edge else set(endpoint_signs)
        )
        need(
            present_signs <= {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and bool(present_signs),
            "typed edge strict sign partition",
        )
        need(crosses_edge or len(present_signs) == 1,
             "typed edge uniform noncrossing sign")
        zero_row = next(
            row for row in edge_rows
            if row["fixed"] == fixed and row["free_axis"] == free_axis
        )
        for sign in ("STRICT_NEGATIVE", "STRICT_POSITIVE"):
            nonempty = sign in present_signs
            outgoing_chart = sign_chart[sign] if nonempty else "NONE"
            edge_region_rows.append(sealed_row({
                "schema": (
                    "cm2.round306c30b.H-sheet-edge-open-interval.row.v1"
                ),
                "terminal_id": terminal_id,
                "fixed": fixed,
                "free_axis": free_axis,
                "predicate": "H<0" if sign == "STRICT_NEGATIVE" else "H>0",
                "H_sign": sign,
                "nonempty": nonempty,
                "dimension_if_nonempty": 1,
                "proof": (
                    "STRICT_MONOTONE_CROSSING_COMPLEMENT_INTERVAL"
                    if crosses_edge else "UNIFORM_STRICT_EDGE_SIGN"
                ),
                "outgoing_chart": outgoing_chart,
                "chart_level_half_open_owner": (
                    outgoing_chart if nonempty else "NONE"
                ),
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": (
                    "LIVE" if outgoing_chart == "W"
                    else "EXCLUDED" if nonempty else "EMPTY"
                ),
                "H_zero_boundary_row_sha256": zero_row["row_sha256"],
            }))
    corner_rows = [
        sealed_row({
            "schema": "cm2.round306c30b.H-sheet-corner-incidence.row.v1",
            "terminal_id": terminal_id,
            "corner": {"t": t_side, "p": p_side, "s": s_side},
            "predicate": "H=0",
            "nonempty": False,
            "dimension_if_nonempty": 0,
            "proof": "STRICT_NONZERO_H_AT_t_p_CORNER",
            "H_sign": corners[f"t{ti}_p{pi}"],
            "disposition": "EMPTY",
            "chart_level_half_open_owner": "NONE",
            "closed_enclosure_terminal_id": terminal_id,
            "strict_corner_outgoing_chart": sign_chart[
                corners[f"t{ti}_p{pi}"]
            ],
            "strict_corner_disposition": (
                "LIVE" if sign_chart[corners[f"t{ti}_p{pi}"]] == "W"
                else "EXCLUDED"
            ),
            "strict_corner_closed_enclosure_terminal_id": terminal_id,
        })
        for ti, t_side in enumerate(("LOWER", "UPPER"))
        for pi, p_side in enumerate(("LOWER", "UPPER"))
        for s_side in ("LOWER", "UPPER")
    ]
    sheet = sealed_row({
        "schema": "cm2.round306c30b.H-zero-sheet.row.v1",
        "terminal_id": terminal_id,
        "predicate": "H=ux*dy-uy*dx=0",
        "seam_id": seam_id,
        "ambient_dimension": 2,
        "nonempty": True,
        "unique_graph_in_p_by_strict_dH_dp": (
            detail["dH_dp_sign"] == "STRICT_NEGATIVE"
        ),
        "half_open_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "half_open_owner_chart": "W",
        "chart_level_half_open_owner": "W",
        "relative_interior_dyadic_owner_terminal_id": terminal_id,
        "ownership_scope": (
            "RELATIVE_INTERIOR_OF_CLOSED_TERMINAL__"
            "BOUNDARY_OWNERSHIP_DEFERRED_TO_ATOMIC_OWNER_AUDIT"
        ),
        "shadow_chart": adjacent,
        "disposition": "LIVE",
        "face_incidence_row_count": len(face_rows),
        "face_incidence_rows_sha256": digest(face_rows),
        "edge_incidence_row_count": len(edge_rows),
        "edge_incidence_rows_sha256": digest(edge_rows),
        "corner_incidence_row_count": len(corner_rows),
        "corner_incidence_rows_sha256": digest(corner_rows),
    })
    return {
        "open_3D_sides": open_sides,
        "H_zero_2D_sheet": sheet,
        "terminal_face_2D_H_sign_regions": face_region_rows,
        "H_zero_1D_face_incidences": face_rows,
        "terminal_edge_1D_H_sign_intervals": edge_region_rows,
        "H_zero_0D_edge_incidences": edge_rows,
        "H_zero_0D_corner_absence_rows": corner_rows,
    }


def classify_h_terminal(chart_id: str, box: Any) -> tuple[str | None, dict[str, Any]]:
    upstream = r176.seam_terminal(chart_id, box)
    cell, nx, ny = r176.tight_contact(chart_id, box)
    if cell is not None:
        classification = (
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            if cell == "W"
            else "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE"
        )
        need(classification == upstream, "strict H classification control")
        return classification, {
            "method": "STRICT_OUTGOING_NORMAL_RECTANGLE",
            "outgoing_chart": cell,
            "outgoing_margin_signs": outgoing_margin_signs(nx, ny),
        }

    candidates = [seam_candidate(chart_id, box, seam_id)
                  for seam_id in sorted(r176.SEAMS)]
    separated = [row for row in candidates
                 if row["typed_preconditions"]
                 and row["uniform_outgoing_chart"] is not None]
    typed = [row for row in candidates
             if row["typed_preconditions"]
             and (row["full_graph"] or row["clipped_graph"])]
    if len(separated) == 1 and not typed:
        chosen = separated[0]
        classification = (
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            if chosen["uniform_outgoing_chart"] == "W"
            else "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE"
        )
        need(classification == upstream, "monotone H classification control")
        return classification, {
            "method": "MONOTONE_H_STRICT_SIGN_RECTANGLE",
            "seam_evidence": chosen,
            "outgoing_chart": chosen["uniform_outgoing_chart"],
        }
    if len(typed) == 1 and not separated:
        need(upstream == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES",
             "typed H classification control")
        return upstream, {
            "method": "TYPED_H_GRAPH_AND_TWO_OPEN_SIDES",
            "seam_evidence": typed[0],
        }
    need(upstream is None, "H unresolved control")
    return None, {"method": "UNRESOLVED_H_INTERVAL", "candidates": candidates}


def materialize_internal_split_lower_strata(
    face_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    edge_groups: dict[str, dict[str, Any]] = {}
    corner_groups: dict[str, dict[str, Any]] = {}
    axes = ("t", "p", "s")
    for face in face_rows:
        face_axis = face["axis"]
        span_axes = [axis for axis in axes if axis != face_axis]
        need(set(span_axes) == set(face["spans"]), "internal split spans")
        face_hash = face["face_sha256"]
        for fixed_axis, free_axis in (
            (span_axes[0], span_axes[1]),
            (span_axes[1], span_axes[0]),
        ):
            for endpoint, coordinate in zip(
                ("LOWER", "UPPER"), face["spans"][fixed_axis]
            ):
                geometry = {
                    "fixed_coordinates": {
                        face_axis: face["coordinate"],
                        fixed_axis: coordinate,
                    },
                    "free_axis": free_axis,
                    "free_span": face["spans"][free_axis],
                }
                key = canonical(geometry).decode("ascii")
                group = edge_groups.setdefault(key, {
                    "geometry": geometry,
                    "owners": [],
                    "nonowners": [],
                    "faces": [],
                    "orientations": [],
                })
                group["owners"].append(face["lower_child_owner"])
                group["nonowners"].append(face["upper_child_nonowner"])
                group["faces"].append(face_hash)
                group["orientations"].append({
                    "incident_split_face_sha256": face_hash,
                    "split_face_axis": face_axis,
                    "boundary_axis": fixed_axis,
                    "boundary_endpoint": endpoint,
                    "lower_child_owner": face["lower_child_owner"],
                    "upper_child_nonowner": face["upper_child_nonowner"],
                })
        for first_endpoint, first_coordinate in zip(
            ("LOWER", "UPPER"), face["spans"][span_axes[0]]
        ):
            for second_endpoint, second_coordinate in zip(
                ("LOWER", "UPPER"), face["spans"][span_axes[1]]
            ):
                geometry = {
                    "fixed_coordinates": {
                        face_axis: face["coordinate"],
                        span_axes[0]: first_coordinate,
                        span_axes[1]: second_coordinate,
                    },
                }
                key = canonical(geometry).decode("ascii")
                group = corner_groups.setdefault(key, {
                    "geometry": geometry,
                    "owners": [],
                    "nonowners": [],
                    "faces": [],
                    "orientations": [],
                })
                group["owners"].append(face["lower_child_owner"])
                group["nonowners"].append(face["upper_child_nonowner"])
                group["faces"].append(face_hash)
                group["orientations"].append({
                    "incident_split_face_sha256": face_hash,
                    "split_face_axis": face_axis,
                    "boundary_endpoints": {
                        span_axes[0]: first_endpoint,
                        span_axes[1]: second_endpoint,
                    },
                    "lower_child_owner": face["lower_child_owner"],
                    "upper_child_nonowner": face["upper_child_nonowner"],
                })

    edge_rows = [
        sealed_row({
                    "schema": (
                        "cm2.round306c30b.internal-split-face-edge-owner."
                        "row.v1"
                    ),
                    **group["geometry"],
                    "ambient_dimension": 1,
                    "half_open_owner_prefix": min(group["owners"]),
                    "incident_lower_child_owners": sorted(set(group["owners"])),
                    "incident_upper_child_nonowners": sorted(
                        set(group["nonowners"])
                    ),
                    "incident_split_face_sha256": sorted(set(group["faces"])),
                    "incident_split_face_count": len(set(group["faces"])),
                    "incident_orientations": sorted(
                        group["orientations"], key=canonical
                    ),
                    "incident_orientations_sha256": digest(sorted(
                        group["orientations"], key=canonical
                    )),
                    "half_open_rule": (
                        "LOWER_CHILD_OWNS_SPLIT_EQUALITY__"
                        "LEXICOGRAPHIC_LEAST_INCIDENT_LOWER_CHILD"
                    ),
                })
        for _key, group in sorted(edge_groups.items())
    ]
    corner_rows = [
        sealed_row({
                    "schema": (
                        "cm2.round306c30b.internal-split-face-corner-owner."
                        "row.v1"
                    ),
                    **group["geometry"],
                    "ambient_dimension": 0,
                    "half_open_owner_prefix": min(group["owners"]),
                    "incident_lower_child_owners": sorted(set(group["owners"])),
                    "incident_upper_child_nonowners": sorted(
                        set(group["nonowners"])
                    ),
                    "incident_split_face_sha256": sorted(set(group["faces"])),
                    "incident_split_face_count": len(set(group["faces"])),
                    "incident_orientations": sorted(
                        group["orientations"], key=canonical
                    ),
                    "incident_orientations_sha256": digest(sorted(
                        group["orientations"], key=canonical
                    )),
                    "half_open_rule": (
                        "LOWER_CHILD_OWNS_SPLIT_EQUALITY__"
                        "LEXICOGRAPHIC_LEAST_INCIDENT_LOWER_CHILD"
                    ),
                })
        for _key, group in sorted(corner_groups.items())
    ]
    edge_rows.sort(key=lambda row: canonical(row))
    corner_rows.sort(key=lambda row: canonical(row))
    need(len(edge_rows) <= 4 * len(face_rows)
         and len(corner_rows) <= 4 * len(face_rows),
         "internal split deduplicated lower strata")
    return edge_rows, corner_rows


def partition_h_cell(row: Any) -> dict[str, Any]:
    pending = [(row.box, 0)]
    terminals: list[dict[str, Any]] = []
    terminal_boxes: dict[str, Any] = {}
    split_faces: list[dict[str, Any]] = []
    while pending:
        box, depth = pending.pop()
        classification, evidence = classify_h_terminal(row.chart_id, box)
        if classification is not None:
            terminal_id = f"{row.chart_id}:{box.path}"
            body: dict[str, Any] = {
                "schema": "cm2.round306c30b.H-terminal-rectangle.row.v1",
                "terminal_id": terminal_id,
                "relative_depth": depth,
                "closed_box": r176.box_row(box),
                "exact_volume": fraction(r215.box_volume(box)),
                "classification": classification,
                "coarse_disposition": coarse_classification(classification),
                "analytic_evidence": evidence,
            }
            if classification == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES":
                body["typed_strata"] = typed_sheet_materialization(
                    row.chart_id,
                    box,
                    evidence["seam_evidence"],
                    terminal_id,
                )
            terminal_boxes[terminal_id] = box
            terminals.append(sealed_row(body))
            continue
        need(depth < 4, "H partition depth exhaustion:" + row.key)
        t_width = (box.t1 - box.t0) / (r176.T_UPPER - r176.T_LOWER)
        p_width = (box.p1 - box.p0) / (r176.P_UPPER - r176.P_LOWER)
        axis = 0 if t_width >= p_width else 1
        lower, upper = r176.split(box, axis)
        parent = r176.Frontier(
            row.chart_id, box, (r176.FROZEN_OWNER,), row.origin_key,
            "OUTGOING_CHART_SEAM_OVERWRAP",
        )
        split_faces.append(r180.split_face(parent, axis, lower, upper))
        pending.extend(((lower, depth + 1), (upper, depth + 1)))
    terminals.sort(key=lambda value: value["terminal_id"])
    split_faces.sort(key=lambda value: value["parent_cell_key"])
    dispositions = Counter(row_["coarse_disposition"] for row_ in terminals)
    whole = (
        "EXCLUDED" if set(dispositions) == {"EXCLUDED"} else
        "LIVE" if set(dispositions) == {"LIVE"} else "MIXED"
    )
    coverage = sum((Q(1, 2 ** row_["relative_depth"]) for row_ in terminals), Q(0))
    exact_volume = sum((Q(row_["exact_volume"]) for row_ in terminals), Q(0))
    typed_count = sum(
        row_["classification"] == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"
        for row_ in terminals
    )
    need(
        coverage == 1
        and exact_volume == r215.box_volume(row.box)
        and whole == r176.h_partition(row)[0],
        "H partition exact control:" + row.key,
    )
    split_edges, split_corners = materialize_internal_split_lower_strata(
        split_faces
    )
    analytic_terminal_projection = [
        {
            "terminal_id": terminal["terminal_id"],
            "relative_depth": terminal["relative_depth"],
            "closed_box": terminal["closed_box"],
            "exact_volume": terminal["exact_volume"],
            "classification": terminal["classification"],
            "coarse_disposition": terminal["coarse_disposition"],
            "analytic_evidence": semantic_without_hash_or_aggregate_metadata(
                terminal["analytic_evidence"]
            ),
            **({
                "typed_strata_semantic_core": (
                    semantic_without_hash_or_aggregate_metadata(
                        terminal["typed_strata"]
                    )
                ),
            } if "typed_strata" in terminal else {}),
        }
        for terminal in terminals
    ]
    analytic_semantic_projection = {
        "projection_schema": (
            "cm2.round306c30b.H-partition-analytic-semantic-projection.v1"
        ),
        "whole_cell_disposition": whole,
        "terminal_rectangle_disposition_census": dict(sorted(
            dispositions.items()
        )),
        "terminal_semantic_rows": analytic_terminal_projection,
        "split_face_geometry_and_child_rows": [
            {
                key: face[key]
                for key in (
                    "parent_cell_key",
                    "axis",
                    "coordinate",
                    "spans",
                    "dimension",
                    "lower_child_owner",
                    "upper_child_nonowner",
                    "both_closed_interval_enclosures_include_face",
                )
            }
            for face in split_faces
        ],
        "relative_3D_coverage": "1",
        "exact_volume": fraction(exact_volume),
    }
    terminal_rows_by_id = {
        terminal["terminal_id"]: terminal for terminal in terminals
    }
    need(
        set(terminal_boxes) == set(terminal_rows_by_id),
        "H terminal box binding:" + row.key,
    )
    audit_leaf_rows = {
        terminal_id: r176.Frontier(
            row.chart_id,
            box,
            (r176.FROZEN_OWNER,),
            row.origin_key,
            "H_TERMINAL_ATOMIC_OWNER_AUDIT",
        )
        for terminal_id, box in terminal_boxes.items()
    }
    terminal_atomic_audit = disposition_aware_atomic_owner_audit(
        [],
        split_faces,
        row.box,
        audit_leaf_rows,
        {
            terminal_id: (
                "ROUND306C30B_H_TERMINAL_ROW:"
                + terminal_rows_by_id[terminal_id]["row_sha256"]
            )
            for terminal_id in terminal_boxes
        },
        {
            terminal_id: terminal_rows_by_id[terminal_id][
                "coarse_disposition"
            ]
            for terminal_id in terminal_boxes
        },
        audit_scope="PER_H_CELL_TERMINAL_SUBDIVISION",
        leaf_key_kind="H_TERMINAL_ID",
    )
    exact_3d = terminal_atomic_audit["exact_3D_enclosure"]
    exact_atomic_closure = (
        exact_3d["all_leaf_boxes_contained_in_parent_and_nondegenerate"]
        and exact_3d["pairwise_leaf_interiors_disjoint"]
        and exact_3d["leaf_exact_volume_sum_equals_parent"]
        and terminal_atomic_audit["all_raw_2D_strata_exactly_reclosed"]
        and terminal_atomic_audit["all_raw_1D_strata_exactly_reclosed"]
        and terminal_atomic_audit["closed_3D_leaf_count"] == len(terminals)
        and terminal_atomic_audit["atomic_2D_owner_row_count"] > 0
        and terminal_atomic_audit["atomic_1D_owner_row_count"] > 0
        and terminal_atomic_audit["atomic_0D_owner_row_count"] > 0
    )
    need(exact_atomic_closure, "H terminal exact atomic audit:" + row.key)
    partition_body = {
        "whole_cell_disposition": whole,
        "terminal_rectangle_count": len(terminals),
        "terminal_rectangle_disposition_census": dict(sorted(dispositions.items())),
        "terminal_rectangles": terminals,
        "terminal_rectangles_sha256": digest(terminals),
        "internal_split_2D_face_rows": split_faces,
        "internal_split_2D_face_row_count": len(split_faces),
        "internal_split_2D_face_rows_sha256": digest(split_faces),
        "internal_split_1D_edge_owner_rows": split_edges,
        "internal_split_1D_edge_owner_row_count": len(split_edges),
        "internal_split_1D_edge_owner_rows_sha256": digest(split_edges),
        "internal_split_0D_corner_owner_rows": split_corners,
        "internal_split_0D_corner_owner_row_count": len(split_corners),
        "internal_split_0D_corner_owner_rows_sha256": digest(split_corners),
        "typed_H_zero_2D_sheet_count": typed_count,
        "relative_3D_coverage": "1",
        "exact_volume": fraction(exact_volume),
    }
    return partition_body | {
        "analytic_semantic_projection": analytic_semantic_projection,
        "analytic_semantic_projection_sha256": digest(
            analytic_semantic_projection
        ),
        "terminal_exact_atomic_owner_audit": terminal_atomic_audit,
        "terminal_exact_atomic_owner_audit_sha256": digest(
            terminal_atomic_audit
        ),
        "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified": (
            exact_atomic_closure
        ),
        "formal_lower_strata_owner_source": (
            "TERMINAL_EXACT_ATOMIC_OWNER_AUDIT__RAW_PREFIX_INCIDENCE_"
            "DIAGNOSTICS_RECEIVE_ZERO_CREDIT"
        ),
        "raw_prefix_lower_strata_formal_owner_credit": 0,
    }


def gzip_rows(path: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    need(
        file_hash(path) == descriptor["sha256"]
        and path.stat().st_size == descriptor["size"],
        "gzip descriptor:" + path.name,
    )
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n") and line.count(b"\n") == 1,
                 "JSONL framing:" + path.name)
            value = strict_object(line[:-1], f"{path.name}:{ordinal}")
            need(canonical(value) + b"\n" == line, "JSONL canonical bytes")
            row_hash = value.get("row_sha256")
            need(
                type(row_hash) is str
                and row_hash == digest({
                    key: item for key, item in value.items()
                    if key != "row_sha256"
                }),
                "JSONL row closure:" + path.name,
            )
            sequence.update(bytes.fromhex(row_hash))
            rows.append(value)
    need(
        len(rows) == descriptor["row_count"]
        and sequence.hexdigest() == descriptor["row_sequence_sha256"],
        "JSONL sequence closure:" + path.name,
    )
    return rows


def reconstructed_r215_evidence(row: Any, reduction: dict[str, Any]) -> dict[str, Any]:
    evidence = r215.analyze_residual_cell(row, reduction) | {
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "active_targets": list(row.active_targets),
    }
    boundary = evidence.get("closed_box_boundary_restriction_proof")
    evidence[
        "strict_closed_box_predicates_restrict_to_cell_faces_edges_vertices"
    ] = bool(
        evidence["analytic_closed"]
        and evidence["method"]
        == "MONOTONE_P_SAME_SIGN_DELTA_STRICT_EXCLUSION"
        and boundary
        and boundary["Delta_endpoints_have_same_strict_sign"]
        and boundary["Delta_zero_graph_intersects_closed_box"] is False
        and boundary["post_enhancement_leaf"] == "unique_first"
        and (
            boundary["unique_first_owner_mismatch_on_whole_closed_box"]
            or boundary["outgoing_owner_chart_mismatch_on_whole_closed_box"]
        )
        and boundary["all_applicable_owner_chart_margins_strict"]
        and boundary[
            "closed_box_strict_inequalities_restrict_to_all_faces_edges_vertices"
        ]
    )
    evidence["row_sha256"] = digest(evidence)
    return evidence


def h_cell_body(
    source_kind: str,
    row: Any,
    source_binding: dict[str, Any],
) -> dict[str, Any]:
    partition = partition_h_cell(row)
    typed = [
        terminal
        for terminal in partition["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
    ]
    face_rows = [
        incidence
        for terminal in typed
        for incidence in terminal["typed_strata"]["H_zero_1D_face_incidences"]
    ]
    face_region_rows = [
        incidence
        for terminal in typed
        for incidence in terminal["typed_strata"][
            "terminal_face_2D_H_sign_regions"
        ]
    ]
    edge_rows = [
        incidence
        for terminal in typed
        for incidence in terminal["typed_strata"]["H_zero_0D_edge_incidences"]
    ]
    edge_region_rows = [
        incidence
        for terminal in typed
        for incidence in terminal["typed_strata"][
            "terminal_edge_1D_H_sign_intervals"
        ]
    ]
    corner_rows = [
        incidence
        for terminal in typed
        for incidence in terminal["typed_strata"]["H_zero_0D_corner_absence_rows"]
    ]
    return {
        "schema": "cm2.round306c30b.source-w-outgoing-h.h-cell.row.v1",
        "source_kind": source_kind,
        "origin_key": row.origin_key,
        "cell_key": row.key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": fraction(r215.box_volume(row.box)),
        "unique_first_owner": r176.FROZEN_OWNER,
        "frozen_outgoing_chart": r176.FROZEN_CHART,
        "source_binding": source_binding,
        "H_partition": partition,
        "whole_H_cell_disposition": partition["whole_cell_disposition"],
        "typed_H_zero_2D_sheet_count": len(typed),
        "typed_H_zero_2D_sheet_rows_sha256": digest([
            terminal["typed_strata"]["H_zero_2D_sheet"]
            for terminal in typed
        ]),
        "terminal_face_2D_H_sign_region_row_count": len(face_region_rows),
        "terminal_face_2D_H_sign_region_rows_sha256": digest(
            face_region_rows
        ),
        "H_zero_1D_face_incidence_row_count": len(face_rows),
        "H_zero_1D_face_incidence_rows_sha256": digest(face_rows),
        "terminal_edge_1D_H_sign_interval_row_count": len(edge_region_rows),
        "terminal_edge_1D_H_sign_interval_rows_sha256": digest(
            edge_region_rows
        ),
        "H_zero_0D_edge_incidence_row_count": len(edge_rows),
        "H_zero_0D_edge_incidence_rows_sha256": digest(edge_rows),
        "H_zero_0D_corner_absence_row_count": len(corner_rows),
        "H_zero_0D_corner_absence_rows_sha256": digest(corner_rows),
        "half_open_owner_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "whole_origin_exclusion_credit": 0,
    }


def box_from_row(value: dict[str, Any], path: str) -> Any:
    return r176.Box(
        Q(value["t"][0]), Q(value["t"][1]),
        Q(value["p"][0]), Q(value["p"][1]),
        Q(value["s"][0]), Q(value["s"][1]),
        0, path,
    )


def write_rows(
    path: Path,
    rows: Iterable[dict[str, Any]],
) -> tuple[int, str]:
    sequence = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output:
            for row in rows:
                output.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return count, sequence.hexdigest()


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {
        "filename": path.name,
        "row_count": count,
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence,
        "order": order,
    }


def candidate_directory(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute != ROOT and absolute.parent != absolute, "candidate target")
    if absolute.exists():
        status = absolute.lstat()
        need(stat.S_ISDIR(status.st_mode) and not absolute.is_symlink(),
             "candidate regular directory")
        need(not any(absolute.iterdir()), "candidate directory not empty")
    else:
        need(absolute.parent.is_dir(), "candidate parent missing")
        absolute.mkdir()
    return absolute


def reduction_binding(reduction: dict[str, Any]) -> dict[str, Any]:
    """Return the complete JSON-valued part of an exact-behind reduction."""
    return {
        "category": reduction["category"],
        "residual_reason": reduction["residual_reason"],
        "closed": reduction["closed"],
        "disposition": reduction["disposition"],
        "eligible_targets": reduction["eligible_targets"],
        "candidate_evidence": reduction["candidate_evidence"],
    }


def collect_frozen_rows() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    r184 = strict_json(ROOT / R184_CERTIFICATE)
    bounded = strict_json(ROOT / R215_CERTIFICATE)["result"][
        "bounded_probe_result"
    ]
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    summaries = {
        row["origin_key"]: row
        for row in bounded["whole_origin_outcome"]["per_origin_rows"]
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    need(
        set(registry) == set(ORIGIN_KEYS)
        and set(summaries) == set(ORIGIN_KEYS),
        "frozen twelve-origin registry identity",
    )

    c30a_result = strict_json(ROOT / C30A_RESULT)
    held_rows = gzip_rows(
        ROOT / C30A_HELD_LEDGER,
        c30a_result["ledgers"]["inherited_H_obstruction_hold"],
    )
    held_by_origin = {row["origin_key"]: row for row in held_rows}
    need(set(held_by_origin) == set(HELD_KEYS), "C30a held row identity")

    c30a_cells = gzip_rows(
        ROOT / C30A_CELL_LEDGER,
        c30a_result["ledgers"]["reduced_clipped_cell"],
    )
    c30a_by_key = {
        row["cell_key"]: row
        for row in c30a_cells
        if row["origin_key"] in set(HELD_KEYS)
    }
    need(
        len(c30a_by_key) == 72
        and Counter(row["origin_key"] for row in c30a_by_key.values())
        == Counter({key: 36 for key in HELD_KEYS})
        and all(
            row["whole_closed_cell_excluded"] is True
            and row["partition"][
                "closed_box_and_all_owned_faces_edges_vertices_excluded"
            ] is True
            for row in c30a_by_key.values()
        ),
        "C30a held final-cell closure",
    )
    return bounded, registry, summaries, {
        "held_by_origin": held_by_origin,
        "c30a_by_key": c30a_by_key,
    }


def inherited_source_binding(
    evidence: dict[str, Any],
    held_row: dict[str, Any] | None,
) -> tuple[str, dict[str, Any]]:
    binding = {
        "Round180_terminal_evidence": evidence,
        "Round180_terminal_sha256": evidence["terminal_sha256"],
    }
    if held_row is None:
        return "ROUND180_INHERITED_OUTGOING_H", binding
    return (
        "ROUND306C30A_HELD_INHERITED_OUTGOING_H",
        {**binding, "C30a_held_row_sha256": held_row["row_sha256"]},
    )


def inherited_same_sign_delta_followup_h_binding(
    evidence: dict[str, Any],
) -> dict[str, Any]:
    need(
        evidence["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
        and evidence["coarse_disposition"] == "MIXED"
        and evidence["Delta_zero_graph_inside_closed_box"] is False
        and evidence["empty_2D_graph_edge_and_corner_ledger"] is True
        and evidence["witness"] == "FOLLOWUP_H_PARTITION",
        "same-sign Delta followup-H evidence",
    )
    return {
        "Round180_terminal_evidence": evidence,
        "Round180_terminal_sha256": evidence["terminal_sha256"],
        "Round180_same_sign_Delta_followup": {
            "method": evidence["method"],
            "target": evidence["target"],
            "derivative_sign": evidence["derivative_sign"],
            "strict_common_face_sign": evidence["strict_common_face_sign"],
            "Delta_p_lower_face_sign": evidence["strict_common_face_sign"],
            "Delta_p_upper_face_sign": evidence["strict_common_face_sign"],
            "Delta_zero_graph_inside_closed_box": False,
            "empty_2D_graph_edge_and_corner_ledger": True,
            "witness": evidence["witness"],
        },
    }


def r215_source_binding(
    evidence: dict[str, Any],
    reduction: dict[str, Any],
) -> dict[str, Any]:
    return {
        "Round215_cell_row_sha256": evidence["row_sha256"],
        "Round215_blocker": evidence["blocker"],
        "Round215_reduction_sha256": digest(reduction_binding(reduction)),
    }


def _closed_enclosure_measure_diagnostic(
    round176_faces: list[dict[str, Any]],
    round180_faces: list[dict[str, Any]],
    original_parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
) -> dict[str, Any]:
    """Rebuild geometric owners without assuming that every leaf is excluded."""
    need(
        set(leaf_rows) == set(proof_source) == set(leaf_disposition),
        "disposition-aware owner leaf maps",
    )
    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }

    def descendants(prefix: str | None) -> list[str]:
        return sorted(
            key for key in leaf_rows
            if prefix is None or key.startswith(prefix)
        )

    def overlap(first: tuple[Q, Q], second: tuple[Q, Q]) -> Q:
        return max(Q(0), min(first[1], second[1]) - max(first[0], second[0]))

    def owner_payload(owners: list[str]) -> dict[str, Any]:
        need(bool(owners), "lower stratum owner exists")
        return {
            "owning_closed_3D_enclosures": owners,
            "owning_closed_3D_enclosures_sha256": digest(owners),
            "owning_proof_source_census": dict(sorted(Counter(
                proof_source[key] for key in owners
            ).items())),
            "owning_disposition_census": dict(sorted(Counter(
                leaf_disposition[key] for key in owners
            ).items())),
            "all_owners_excluded": all(
                leaf_disposition[key] == "EXCLUDED" for key in owners
            ),
        }

    def face_row(
        geometry: dict[str, Any], prefix: str | None, label: str
    ) -> dict[str, Any]:
        fixed_axis = geometry["fixed_axis"]
        coordinate = Q(geometry["coordinate"])
        spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in geometry["spans"].items()
        }
        free = sorted(spans)
        measure = ((spans[free[0]][1] - spans[free[0]][0])
                   * (spans[free[1]][1] - spans[free[1]][0]))
        owners: list[str] = []
        covered = Q(0)
        for key in descendants(prefix):
            item = bounds[key]
            if not item[fixed_axis][0] <= coordinate <= item[fixed_axis][1]:
                continue
            area = overlap(item[free[0]], spans[free[0]]) * overlap(
                item[free[1]], spans[free[1]]
            )
            if area:
                owners.append(key)
                covered += area
        need(covered == measure, "face exact half-open coverage")
        return sealed_row({
            "schema": "cm2.round306c30b.disposition-aware-face-owner.row.v1",
            "stratum_class": label,
            "geometry": geometry,
            "half_open_owner_prefix": prefix or "PARENT",
            "exact_measure": fraction(measure),
            "covered_exact_measure": fraction(covered),
            **owner_payload(owners),
        })

    def edge_row(
        geometry: dict[str, Any], prefix: str | None, label: str
    ) -> dict[str, Any]:
        fixed = {axis: Q(value) for axis, value in geometry["fixed"].items()}
        free_axis, raw_span = next(iter(geometry["free"].items()))
        span = (Q(raw_span[0]), Q(raw_span[1]))
        measure = span[1] - span[0]
        owners: list[str] = []
        covered = Q(0)
        for key in descendants(prefix):
            item = bounds[key]
            if not all(item[axis][0] <= value <= item[axis][1]
                       for axis, value in fixed.items()):
                continue
            length = overlap(item[free_axis], span)
            if length:
                owners.append(key)
                covered += length
        need(covered == measure, "edge exact half-open coverage")
        return sealed_row({
            "schema": "cm2.round306c30b.disposition-aware-edge-owner.row.v1",
            "stratum_class": label,
            "geometry": geometry,
            "half_open_owner_prefix": prefix or "PARENT",
            "exact_measure": fraction(measure),
            "covered_exact_measure": fraction(covered),
            **owner_payload(owners),
        })

    def corner_row(
        geometry: dict[str, str], prefix: str | None, label: str
    ) -> dict[str, Any]:
        point = {axis: Q(value) for axis, value in geometry.items()}
        candidates = [
            key for key in descendants(prefix)
            if all(bounds[key][axis][0] <= value <= bounds[key][axis][1]
                   for axis, value in point.items())
        ]
        owner = min(candidates)
        return sealed_row({
            "schema": "cm2.round306c30b.disposition-aware-corner-owner.row.v1",
            "stratum_class": label,
            "geometry": geometry,
            "half_open_owner_prefix": prefix or "PARENT",
            "owning_closed_3D_enclosure": owner,
            "owning_proof_source": proof_source[owner],
            "owning_disposition": leaf_disposition[owner],
            "all_owners_excluded": leaf_disposition[owner] == "EXCLUDED",
        })

    def internal(rows: list[dict[str, Any]], label: str) -> dict[str, Any]:
        faces: list[dict[str, Any]] = []
        edges: dict[str, dict[str, Any]] = {}
        corners: dict[str, dict[str, Any]] = {}
        for face in rows:
            face_geometry = {
                "fixed_axis": face["axis"],
                "coordinate": face["coordinate"],
                "spans": face["spans"],
            }
            faces.append(face_row(
                face_geometry, face["lower_child_owner"],
                label + "_INTERNAL_SPLIT_FACE"
            ))
            free_axes = [axis for axis in axes if axis != face["axis"]]
            for boundary_axis in free_axes:
                other = next(axis for axis in free_axes if axis != boundary_axis)
                for endpoint in face["spans"][boundary_axis]:
                    geometry = {
                        "fixed": {
                            face["axis"]: face["coordinate"],
                            boundary_axis: endpoint,
                        },
                        "free": {other: face["spans"][other]},
                    }
                    key = canonical(geometry).decode("ascii")
                    current = edges.get(key)
                    prefix = face["lower_child_owner"]
                    if current is None or prefix < current["prefix"]:
                        edges[key] = {"geometry": geometry, "prefix": prefix}
            for first in face["spans"][free_axes[0]]:
                for second in face["spans"][free_axes[1]]:
                    geometry = {
                        face["axis"]: face["coordinate"],
                        free_axes[0]: first,
                        free_axes[1]: second,
                    }
                    key = canonical(geometry).decode("ascii")
                    current = corners.get(key)
                    prefix = face["lower_child_owner"]
                    if current is None or prefix < current["prefix"]:
                        corners[key] = {"geometry": geometry, "prefix": prefix}
        edge_rows = [
            edge_row(item["geometry"], item["prefix"],
                     label + "_INTERNAL_SPLIT_FACE_EDGE")
            for _key, item in sorted(edges.items())
        ]
        corner_rows = [
            corner_row(item["geometry"], item["prefix"],
                       label + "_INTERNAL_SPLIT_FACE_CORNER")
            for _key, item in sorted(corners.items())
        ]
        return {
            "2D_rows": faces,
            "1D_rows": edge_rows,
            "0D_rows": corner_rows,
        }

    round176 = internal(round176_faces, "ROUND176")
    round180 = internal(round180_faces, "ROUND180")
    parent_bounds = {
        "t": (original_parent.t0, original_parent.t1),
        "p": (original_parent.p0, original_parent.p1),
        "s": (original_parent.s0, original_parent.s1),
    }
    outer_faces: list[dict[str, Any]] = []
    for fixed_axis in axes:
        free_axes = [axis for axis in axes if axis != fixed_axis]
        spans = {
            axis: [fraction(parent_bounds[axis][0]), fraction(parent_bounds[axis][1])]
            for axis in free_axes
        }
        for coordinate in parent_bounds[fixed_axis]:
            outer_faces.append(face_row({
                "fixed_axis": fixed_axis,
                "coordinate": fraction(coordinate),
                "spans": spans,
            }, None, "OUTER_PARENT_FACE"))
    outer_edges: list[dict[str, Any]] = []
    for free_axis in axes:
        fixed_axes = [axis for axis in axes if axis != free_axis]
        for first in parent_bounds[fixed_axes[0]]:
            for second in parent_bounds[fixed_axes[1]]:
                outer_edges.append(edge_row({
                    "fixed": {
                        fixed_axes[0]: fraction(first),
                        fixed_axes[1]: fraction(second),
                    },
                    "free": {free_axis: [
                        fraction(parent_bounds[free_axis][0]),
                        fraction(parent_bounds[free_axis][1]),
                    ]},
                }, None, "OUTER_PARENT_EDGE"))
    outer_corners = [
        corner_row({"t": fraction(t), "p": fraction(p), "s": fraction(s)},
                   None, "OUTER_PARENT_CORNER")
        for t in parent_bounds["t"]
        for p in parent_bounds["p"]
        for s in parent_bounds["s"]
    ]
    groups = {
        "Round176_internal": round176,
        "Round180_internal": round180,
        "outer_parent": {
            "2D_rows": outer_faces,
            "1D_rows": outer_edges,
            "0D_rows": outer_corners,
        },
    }
    output: dict[str, Any] = {
        "schema": "cm2.round306c30b.disposition-aware-owner-audit.v1",
        "owner_reduction_rule": (
            "LOWER_CHILD_OWNS_INTERNAL_EQUALITY__GEOMETRY_DEDUP__"
            "LEXICOGRAPHIC_LEAST_INCIDENT_PREFIX"
        ),
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_leaf_disposition_census": dict(sorted(Counter(
            leaf_disposition.values()
        ).items())),
    }
    all_rows: list[dict[str, Any]] = []
    for label, group in groups.items():
        for dimension in ("2D", "1D", "0D"):
            rows = group[dimension + "_rows"]
            output[f"{label}_{dimension}_owner_row_count"] = len(rows)
            output[f"{label}_{dimension}_owner_rows_sha256"] = digest(rows)
            all_rows.extend(rows)
    output["owner_row_disposition_census"] = dict(sorted(Counter(
        "EXCLUDED_ONLY" if row["all_owners_excluded"] else "NONEXCLUDED_PRESENT"
        for row in all_rows
    ).items()))
    output["all_owner_rows_sha256"] = digest(all_rows)
    return output


def disposition_aware_atomic_owner_audit(
    round176_faces: list[dict[str, Any]],
    round180_faces: list[dict[str, Any]],
    original_parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
    *,
    audit_scope: str = "WHOLE_ORIGIN_LINEAGE",
    leaf_key_kind: str = "CELL_KEY",
) -> dict[str, Any]:
    """Atomize every lower stratum and select its pointwise half-open owner."""
    need(
        set(leaf_rows) == set(proof_source) == set(leaf_disposition),
        "atomic owner leaf maps",
    )
    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    parent_bounds = {
        "t": (original_parent.t0, original_parent.t1),
        "p": (original_parent.p0, original_parent.p1),
        "s": (original_parent.s0, original_parent.s1),
    }
    contained_in_parent = all(
        all(
            parent_bounds[axis][0] <= item[axis][0] < item[axis][1]
            <= parent_bounds[axis][1]
            for axis in axes
        )
        for item in bounds.values()
    )
    leaf_volume = sum(
        (
            (item["t"][1] - item["t"][0])
            * (item["p"][1] - item["p"][0])
            * (item["s"][1] - item["s"][0])
            for item in bounds.values()
        ),
        Q(0),
    )
    parent_volume = (
        (original_parent.t1 - original_parent.t0)
        * (original_parent.p1 - original_parent.p0)
        * (original_parent.s1 - original_parent.s0)
    )
    ordered_leaf_keys = sorted(bounds)
    pair_state = hashlib.sha256()
    pair_state.update(b"[")
    pair_count = 0
    pairwise_interior_disjoint = True
    for first_index, first_key in enumerate(ordered_leaf_keys):
        for second_key in ordered_leaf_keys[first_index + 1:]:
            interior_overlap = all(
                max(bounds[first_key][axis][0], bounds[second_key][axis][0])
                < min(bounds[first_key][axis][1], bounds[second_key][axis][1])
                for axis in axes
            )
            pairwise_interior_disjoint &= not interior_overlap
            if pair_count:
                pair_state.update(b",")
            pair_state.update(canonical({
                "first": first_key,
                "second": second_key,
                "interior_overlap": interior_overlap,
            }))
            pair_count += 1
    pair_state.update(b"]")
    volume_exhaustive = leaf_volume == parent_volume
    need(
        contained_in_parent
        and pairwise_interior_disjoint
        and volume_exhaustive
        and pair_count == len(leaf_rows) * (len(leaf_rows) - 1) // 2,
        "exact 3D leaf enclosure",
    )
    grid = {
        axis: sorted({value for item in bounds.values() for value in item[axis]})
        for axis in axes
    }

    def cuts(axis: str, lower: Q, upper: Q) -> list[Q]:
        values = [lower] + [
            value for value in grid[axis] if lower < value < upper
        ] + [upper]
        need(values == sorted(set(values)), "atomic grid cuts")
        return values

    def containing_owner(
        fixed: dict[str, Q], open_spans: dict[str, tuple[Q, Q]]
    ) -> str:
        midpoints = {
            axis: (span[0] + span[1]) / 2
            for axis, span in open_spans.items()
        }
        candidates = [
            key for key, item in bounds.items()
            if all(item[axis][0] <= value <= item[axis][1]
                   for axis, value in fixed.items())
            and all(item[axis][0] < value < item[axis][1]
                    for axis, value in midpoints.items())
        ]
        need(bool(candidates), "atomic half-open owner exists")
        owner = min(candidates)
        need(
            all(
                bounds[owner][axis][0] <= span[0] < span[1]
                <= bounds[owner][axis][1]
                for axis, span in open_spans.items()
            ),
            "atomic owner covers whole atom",
        )
        return owner

    raw_faces: list[dict[str, Any]] = []
    for stage, faces in (
        ("ROUND176_INTERNAL", round176_faces),
        ("ROUND180_INTERNAL", round180_faces),
    ):
        for face in faces:
            raw_faces.append({
                "source": stage + ":" + face["face_sha256"],
                "fixed_axis": face["axis"],
                "coordinate": face["coordinate"],
                "spans": face["spans"],
            })
    for fixed_axis in axes:
        free_axes = [axis for axis in axes if axis != fixed_axis]
        for side, coordinate in zip(
            ("LOWER", "UPPER"), parent_bounds[fixed_axis]
        ):
            raw_faces.append({
                "source": f"OUTER_PARENT:{fixed_axis}:{side}",
                "fixed_axis": fixed_axis,
                "coordinate": fraction(coordinate),
                "spans": {
                    axis: [fraction(parent_bounds[axis][0]),
                           fraction(parent_bounds[axis][1])]
                    for axis in free_axes
                },
            })

    face_atoms: dict[str, dict[str, Any]] = {}
    raw_face_reclosure: list[dict[str, Any]] = []
    raw_edges: dict[str, dict[str, Any]] = {}
    raw_corners: dict[str, dict[str, Any]] = {}
    for raw in raw_faces:
        fixed_axis = raw["fixed_axis"]
        fixed_value = Q(raw["coordinate"])
        free_axes = sorted(raw["spans"])
        spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in raw["spans"].items()
        }
        axis_cuts = {
            axis: cuts(axis, spans[axis][0], spans[axis][1])
            for axis in free_axes
        }
        source_measure = (
            (spans[free_axes[0]][1] - spans[free_axes[0]][0])
            * (spans[free_axes[1]][1] - spans[free_axes[1]][0])
        )
        atom_measure = Q(0)
        atom_keys: list[str] = []
        for first_lower, first_upper in zip(
            axis_cuts[free_axes[0]], axis_cuts[free_axes[0]][1:]
        ):
            for second_lower, second_upper in zip(
                axis_cuts[free_axes[1]], axis_cuts[free_axes[1]][1:]
            ):
                geometry = {
                    "fixed": {fixed_axis: fraction(fixed_value)},
                    "open_spans": {
                        free_axes[0]: [fraction(first_lower), fraction(first_upper)],
                        free_axes[1]: [fraction(second_lower), fraction(second_upper)],
                    },
                }
                key = canonical(geometry).decode("ascii")
                group = face_atoms.setdefault(key, {
                    "geometry": geometry, "incident_sources": []
                })
                group["incident_sources"].append(raw["source"])
                atom_keys.append(key)
                atom_measure += ((first_upper - first_lower)
                                 * (second_upper - second_lower))
        need(atom_measure == source_measure, "atomic face reclosure")
        raw_face_reclosure.append({
            "source": raw["source"],
            "source_exact_measure": fraction(source_measure),
            "atomic_exact_measure": fraction(atom_measure),
            "atomic_geometry_keys_sha256": digest(sorted(atom_keys)),
        })
        for boundary_axis in free_axes:
            other = next(axis for axis in free_axes if axis != boundary_axis)
            for side, endpoint in zip(
                ("LOWER", "UPPER"), spans[boundary_axis]
            ):
                geometry = {
                    "fixed": {
                        fixed_axis: fraction(fixed_value),
                        boundary_axis: fraction(endpoint),
                    },
                    "open_span": {
                        other: [fraction(spans[other][0]),
                                fraction(spans[other][1])]
                    },
                }
                key = canonical(geometry).decode("ascii")
                group = raw_edges.setdefault(key, {
                    "geometry": geometry, "incident_sources": []
                })
                group["incident_sources"].append(
                    raw["source"] + ":" + boundary_axis + ":" + side
                )
        for first_side, first in zip(
            ("LOWER", "UPPER"), spans[free_axes[0]]
        ):
            for second_side, second in zip(
                ("LOWER", "UPPER"), spans[free_axes[1]]
            ):
                geometry = {"point": {
                    fixed_axis: fraction(fixed_value),
                    free_axes[0]: fraction(first),
                    free_axes[1]: fraction(second),
                }}
                key = canonical(geometry).decode("ascii")
                group = raw_corners.setdefault(key, {
                    "geometry": geometry, "incident_sources": []
                })
                group["incident_sources"].append(
                    raw["source"] + ":" + first_side + ":" + second_side
                )

    # Close every axis-grid 2D atom by materializing its own 1D/0D boundary.
    # This adds intersections created by interior grid cuts, not merely the
    # outer edges of the original split-face rectangles.
    for _key, atom in sorted(face_atoms.items()):
        fixed_axis, fixed_value = next(iter(atom["geometry"]["fixed"].items()))
        span_axes = sorted(atom["geometry"]["open_spans"])
        spans = {
            axis: tuple(values)
            for axis, values in atom["geometry"]["open_spans"].items()
        }
        atom_source = "ATOMIC_2D:" + digest(atom["geometry"])
        for boundary_axis in span_axes:
            other = next(axis for axis in span_axes if axis != boundary_axis)
            for side, endpoint in zip(
                ("LOWER", "UPPER"), spans[boundary_axis]
            ):
                geometry = {
                    "fixed": {
                        fixed_axis: fixed_value,
                        boundary_axis: endpoint,
                    },
                    "open_span": {other: list(spans[other])},
                }
                key = canonical(geometry).decode("ascii")
                group = raw_edges.setdefault(key, {
                    "geometry": geometry, "incident_sources": []
                })
                group["incident_sources"].append(
                    atom_source + ":" + boundary_axis + ":" + side
                )
        for first_side, first in zip(
            ("LOWER", "UPPER"), spans[span_axes[0]]
        ):
            for second_side, second in zip(
                ("LOWER", "UPPER"), spans[span_axes[1]]
            ):
                geometry = {"point": {
                    fixed_axis: fixed_value,
                    span_axes[0]: first,
                    span_axes[1]: second,
                }}
                key = canonical(geometry).decode("ascii")
                group = raw_corners.setdefault(key, {
                    "geometry": geometry, "incident_sources": []
                })
                group["incident_sources"].append(
                    atom_source + ":" + first_side + ":" + second_side
                )

    face_rows: list[dict[str, Any]] = []
    for _key, group in sorted(face_atoms.items()):
        fixed = {axis: Q(value)
                 for axis, value in group["geometry"]["fixed"].items()}
        open_spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in group["geometry"]["open_spans"].items()
        }
        owner = containing_owner(fixed, open_spans)
        face_rows.append(sealed_row({
            "schema": "cm2.round306c30b.atomic-2D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
            "exact_measure": fraction(
                next(iter(open_spans.values()))[1]
                - next(iter(open_spans.values()))[0]
            ) if len(open_spans) == 1 else fraction(
                (list(open_spans.values())[0][1]
                 - list(open_spans.values())[0][0])
                * (list(open_spans.values())[1][1]
                   - list(open_spans.values())[1][0])
            ),
        }))

    edge_atoms: dict[str, dict[str, Any]] = {}
    raw_edge_reclosure: list[dict[str, Any]] = []
    for _key, raw in sorted(raw_edges.items()):
        free_axis, values = next(iter(raw["geometry"]["open_span"].items()))
        lower, upper = Q(values[0]), Q(values[1])
        source_measure = upper - lower
        atom_measure = Q(0)
        atom_keys: list[str] = []
        axis_cuts = cuts(free_axis, lower, upper)
        for atom_lower, atom_upper in zip(axis_cuts, axis_cuts[1:]):
            geometry = {
                "fixed": raw["geometry"]["fixed"],
                "open_span": {
                    free_axis: [fraction(atom_lower), fraction(atom_upper)]
                },
            }
            key = canonical(geometry).decode("ascii")
            group = edge_atoms.setdefault(key, {
                "geometry": geometry, "incident_sources": []
            })
            group["incident_sources"].extend(raw["incident_sources"])
            atom_keys.append(key)
            atom_measure += atom_upper - atom_lower
            atom_source = "ATOMIC_1D:" + digest(geometry)
            for side, endpoint in (
                ("LOWER", atom_lower), ("UPPER", atom_upper)
            ):
                point = dict(raw["geometry"]["fixed"])
                point[free_axis] = fraction(endpoint)
                point_geometry = {"point": point}
                point_key = canonical(point_geometry).decode("ascii")
                point_group = raw_corners.setdefault(point_key, {
                    "geometry": point_geometry, "incident_sources": []
                })
                point_group["incident_sources"].append(
                    atom_source + ":" + side
                )
        need(atom_measure == source_measure, "atomic edge reclosure")
        raw_edge_reclosure.append({
            "source_geometry_sha256": digest(raw["geometry"]),
            "source_exact_measure": fraction(source_measure),
            "atomic_exact_measure": fraction(atom_measure),
            "atomic_geometry_keys_sha256": digest(sorted(atom_keys)),
        })
    edge_rows: list[dict[str, Any]] = []
    for _key, group in sorted(edge_atoms.items()):
        fixed = {axis: Q(value)
                 for axis, value in group["geometry"]["fixed"].items()}
        free_axis, values = next(iter(group["geometry"]["open_span"].items()))
        open_spans = {free_axis: (Q(values[0]), Q(values[1]))}
        owner = containing_owner(fixed, open_spans)
        edge_rows.append(sealed_row({
            "schema": "cm2.round306c30b.atomic-1D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
            "exact_measure": fraction(open_spans[free_axis][1]
                                      - open_spans[free_axis][0]),
        }))

    corner_rows: list[dict[str, Any]] = []
    for _key, group in sorted(raw_corners.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["point"].items()
        }
        owner = containing_owner(fixed, {})
        corner_rows.append(sealed_row({
            "schema": "cm2.round306c30b.atomic-0D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
        }))

    all_rows = face_rows + edge_rows + corner_rows
    return {
        "schema": "cm2.round306c30b.exact-atomic-half-open-owner-audit.v2",
        "audit_scope": audit_scope,
        "leaf_key_kind": leaf_key_kind,
        "exact_3D_enclosure": {
            "all_leaf_boxes_contained_in_parent_and_nondegenerate": (
                contained_in_parent
            ),
            "pairwise_leaf_interiors_disjoint": pairwise_interior_disjoint,
            "tested_unordered_leaf_pair_count": pair_count,
            "tested_leaf_pair_rows_sha256": pair_state.hexdigest(),
            "leaf_exact_volume_sum": fraction(leaf_volume),
            "parent_exact_volume": fraction(parent_volume),
            "leaf_exact_volume_sum_equals_parent": volume_exhaustive,
        },
        "axis_grid_coordinate_count": {
            axis: len(values) for axis, values in grid.items()
        },
        "axis_grid_coordinates_sha256": digest({
            axis: [fraction(value) for value in values]
            for axis, values in grid.items()
        }),
        "atomic_owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_leaf_disposition_census": dict(sorted(Counter(
            leaf_disposition.values()
        ).items())),
        "raw_2D_stratum_reclosure_row_count": len(raw_face_reclosure),
        "raw_2D_stratum_reclosure_rows_sha256": digest(raw_face_reclosure),
        "all_raw_2D_strata_exactly_reclosed": all(
            row["source_exact_measure"] == row["atomic_exact_measure"]
            for row in raw_face_reclosure
        ),
        "raw_1D_stratum_reclosure_row_count": len(raw_edge_reclosure),
        "raw_1D_stratum_reclosure_rows_sha256": digest(raw_edge_reclosure),
        "all_raw_1D_strata_exactly_reclosed": all(
            row["source_exact_measure"] == row["atomic_exact_measure"]
            for row in raw_edge_reclosure
        ),
        "lower_strata_generation_rule": (
            "EACH_2D_ATOM_GENERATES_ALL_FOUR_1D_CUT_BOUNDARIES__"
            "EACH_1D_ATOM_GENERATES_BOTH_0D_CUT_ENDPOINTS__"
            "GLOBAL_PURE_GEOMETRY_DEDUP"
        ),
        "atomic_2D_owner_row_count": len(face_rows),
        "atomic_2D_owner_rows_sha256": digest(face_rows),
        "atomic_1D_owner_row_count": len(edge_rows),
        "atomic_1D_owner_rows_sha256": digest(edge_rows),
        "atomic_0D_owner_row_count": len(corner_rows),
        "atomic_0D_owner_rows_sha256": digest(corner_rows),
        "atomic_owner_disposition_census": dict(sorted(Counter(
            row["owner_disposition"] for row in all_rows
        ).items())),
        "atomic_owner_rows_sha256": digest(all_rows),
    }


def origin_materialization(
    origin_ordinal: int,
    origin: str,
    replay: dict[str, Any],
    roots: list[Any],
    base_rows: list[Any],
    refinement: dict[str, Any],
    leaves: dict[str, Any],
    h_rows: list[dict[str, Any]],
    round201_count: int,
    round201_volume: Q,
    round215_count: int,
    round215_volume: Q,
    c30a_count: int,
    c30a_volume: Q,
    final_excluded_evidence: dict[str, list[dict[str, Any]]],
    registry: dict[str, Any],
) -> dict[str, Any]:
    prior = c30a.generalized_prior_partition(replay, origin)
    inherited = sorted(
        refinement["terminal_rows"], key=lambda value: value["cell_key"]
    )
    inherited_excluded = [
        row for row in inherited if row["coarse_disposition"] == "EXCLUDED"
    ]
    inherited_h = [
        row for row in inherited
        if row["coarse_disposition"] != "EXCLUDED"
        and row["method"] in {
            "OUTGOING_H_CLOSED_RECTANGLE_TREE",
            "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX",
        }
    ]
    inherited_direct_h = [
        row for row in inherited_h
        if row["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE"
    ]
    inherited_followup_h = [
        row for row in inherited_h
        if row["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
    ]
    final_rows = sorted(
        refinement["final_residual_rows"], key=lambda value: value.key
    )
    h_rows.sort(key=lambda value: value["cell_key"])
    h_dispositions = Counter(
        row["whole_H_cell_disposition"] for row in h_rows
    )
    whole_disposition = (
        "EXCLUDED"
        if set(h_dispositions) == {"EXCLUDED"}
        else "RESOLVED_LIVE"
        if set(h_dispositions) == {"LIVE"}
        else "RESOLVED_MIXED"
    )
    expected_whole = (
        "EXCLUDED" if origin in set(EXCLUDED_ORIGIN_KEYS)
        else "RESOLVED_MIXED"
    )
    live_witnesses: list[dict[str, Any]] = []
    for h_row in h_rows:
        for terminal in h_row["H_partition"]["terminal_rectangles"]:
            if terminal["coarse_disposition"] == "LIVE":
                live_witnesses.append({
                    "witness_kind": "WHOLE_LIVE_H_TERMINAL_RECTANGLE",
                    "cell_key": h_row["cell_key"],
                    "terminal_row_sha256": terminal["row_sha256"],
                    "exact_volume": terminal["exact_volume"],
                    "strictly_positive_measure": Q(terminal["exact_volume"]) > 0,
                })
            elif terminal["coarse_disposition"] == "MIXED":
                live_side = next(
                    side for side in terminal["typed_strata"]["open_3D_sides"]
                    if side["disposition"] == "LIVE"
                )
                live_witnesses.append({
                    "witness_kind": "TYPED_H_TERMINAL_LIVE_OPEN_SIDE",
                    "cell_key": h_row["cell_key"],
                    "terminal_row_sha256": terminal["row_sha256"],
                    "live_open_side_row_sha256": live_side["row_sha256"],
                    "predicate": live_side["predicate"],
                    "nonempty_positive_measure": live_side[
                        "nonempty_positive_measure"
                    ],
                })
    live_witnesses.sort(key=lambda value: canonical(value))

    root_volume = sum((r215.box_volume(row.box) for row in roots), Q(0))
    base_volume = sum((r215.box_volume(row.box) for row in base_rows), Q(0))
    inherited_volume = sum(
        (
            r215.box_volume(leaves["terminal"][row["cell_key"]].box)
            for row in inherited
        ),
        Q(0),
    )
    final_volume = sum(
        (r215.box_volume(row.box) for row in final_rows), Q(0)
    )
    h_volume = sum((Q(row["exact_volume"]) for row in h_rows), Q(0))
    parent_volume = r215.box_volume(replay["origins"][origin]["box"])
    final_closed_volume = round201_volume + round215_volume + c30a_volume
    need(
        len(inherited_h) == EXPECTED_INHERITED_H_BY_ORIGIN[origin]
        and len(inherited_followup_h)
        == EXPECTED_INHERITED_FOLLOWUP_H_BY_ORIGIN[origin]
        and len(inherited_direct_h) == (
            EXPECTED_INHERITED_H_BY_ORIGIN[origin]
            - EXPECTED_INHERITED_FOLLOWUP_H_BY_ORIGIN[origin]
        )
        and len(h_rows) == (
            EXPECTED_INHERITED_H_BY_ORIGIN[origin]
            + EXPECTED_R215_H_CELLS_BY_ORIGIN.get(origin, 0)
        )
        and whole_disposition == expected_whole
        and (
            not live_witnesses if whole_disposition == "EXCLUDED"
            else all(
                (
                    witness.get("witness_kind")
                    == "WHOLE_LIVE_H_TERMINAL_RECTANGLE"
                    and witness.get("strictly_positive_measure") is True
                    and "nonempty_positive_measure" not in witness
                )
                or (
                    witness.get("witness_kind")
                    == "TYPED_H_TERMINAL_LIVE_OPEN_SIDE"
                    and witness.get("nonempty_positive_measure") is True
                    and "strictly_positive_measure" not in witness
                )
                for witness in live_witnesses
            )
        )
        and prior["prior_closed_exact_volume"] + base_volume + root_volume
        == parent_volume
        and inherited_volume + final_volume == root_volume
        and h_volume + final_closed_volume + sum(
            (
                r215.box_volume(leaves["terminal"][row["cell_key"]].box)
                for row in inherited_excluded
            ),
            Q(0),
        ) == root_volume,
        "whole origin exact composition:" + origin,
    )

    h_by_key = {row["cell_key"]: row for row in h_rows}
    audit_leaf_rows: dict[str, Any] = dict(prior["prior_closed_rows"])
    audit_leaf_rows.update({row.key: row for row in base_rows})
    audit_leaf_rows.update(leaves["terminal"])
    audit_leaf_rows.update(leaves["final"])
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED" for key in prior["prior_closed_rows"]
    }
    proof_source.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED" for row in base_rows
    })
    proof_source.update({
        row["cell_key"]: (
            "ROUND306C30B_MATERIALIZED_SAME_SIGN_DELTA_FOLLOWUP_H"
            if row["cell_key"] in h_by_key
            and h_by_key[row["cell_key"]]["source_kind"]
            == "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
            else "ROUND306C30B_MATERIALIZED_INHERITED_OUTGOING_H"
            if row["cell_key"] in h_by_key
            else "PINNED_ROUND180_INHERITED_EXCLUDED"
        )
        for row in inherited
    })
    proof_source.update({
        row.key: (
            "ROUND306C30B_MATERIALIZED_ROUND215_OUTGOING_H"
            if row.key in h_by_key
            else "PINNED_OR_RECONSTRUCTED_FINAL_EXCLUDED_BUCKET"
        )
        for row in final_rows
    })
    leaf_disposition = {
        key: "EXCLUDED" for key in prior["prior_closed_rows"]
    }
    leaf_disposition.update({row.key: "EXCLUDED" for row in base_rows})
    leaf_disposition.update({
        row["cell_key"]: h_by_key[row["cell_key"]][
            "whole_H_cell_disposition"
        ] if row["cell_key"] in h_by_key
        else "EXCLUDED"
        for row in inherited
    })
    leaf_disposition.update({
        row.key: h_by_key[row.key]["whole_H_cell_disposition"]
        if row.key in h_by_key else "EXCLUDED"
        for row in final_rows
    })
    all_non_h_closed_leaves_excluded = all(
        leaf_disposition[key] == "EXCLUDED"
        for key in set(leaf_disposition) - set(h_by_key)
    )
    owner_audit = disposition_aware_atomic_owner_audit(
        prior["split_face_rows"],
        refinement["split_face_rows"],
        replay["origins"][origin]["box"],
        audit_leaf_rows,
        proof_source,
        leaf_disposition,
    )
    origin_exact_atomic_closure = (
        owner_audit["exact_3D_enclosure"][
            "all_leaf_boxes_contained_in_parent_and_nondegenerate"
        ] is True
        and owner_audit["exact_3D_enclosure"][
            "pairwise_leaf_interiors_disjoint"
        ] is True
        and owner_audit["exact_3D_enclosure"][
            "leaf_exact_volume_sum_equals_parent"
        ] is True
        and owner_audit["all_raw_2D_strata_exactly_reclosed"] is True
        and owner_audit["all_raw_1D_strata_exactly_reclosed"] is True
        and owner_audit["atomic_2D_owner_row_count"] > 0
        and owner_audit["atomic_1D_owner_row_count"] > 0
        and owner_audit["atomic_0D_owner_row_count"] > 0
        and (
            whole_disposition != "EXCLUDED"
            or set(owner_audit["atomic_owner_disposition_census"])
            == {"EXCLUDED"}
        )
    )
    need(
        origin_exact_atomic_closure,
        "origin disposition-aware owner audit:" + origin,
    )

    base_evidence = []
    for row in base_rows:
        kind, evidence = r176.closure(row)
        need(kind == "EXCLUDED" and evidence is not None,
             "base exclusion evidence:" + row.key)
        base_evidence.append({
            "cell_key": row.key,
            "coarse_disposition": kind,
            "evidence": evidence,
        })
    base_evidence.sort(key=lambda value: value["cell_key"])
    inherited_followup_h_evidence = [
        sealed_row({
            "schema": (
                "cm2.round306c30b.same-sign-delta-followup-h."
                "evidence-row.v1"
            ),
            "origin_key": origin,
            "cell_key": row["cell_key"],
            "closed_box": r176.box_row(
                leaves["terminal"][row["cell_key"]].box
            ),
            "exact_volume": fraction(r215.box_volume(
                leaves["terminal"][row["cell_key"]].box
            )),
            "upstream_terminal_evidence": row,
            "upstream_terminal_sha256": row["terminal_sha256"],
            "method": row["method"],
            "Delta_zero_graph_inside_closed_box": False,
            "empty_2D_graph_edge_and_corner_ledger": True,
            "followup_witness": row["witness"],
            "followup_H_cell_row_sha256": h_by_key[
                row["cell_key"]
            ]["row_sha256"],
            "formal_disposition_after_followup_H": h_by_key[
                row["cell_key"]
            ]["whole_H_cell_disposition"],
            "included_in_outgoing_H_cell_ledger": True,
            "whole_origin_exclusion_credit": 0,
        })
        for row in inherited_followup_h
    ]

    h_internal_2d = [
        face["face_sha256"]
        for row in h_rows
        for face in row["H_partition"]["internal_split_2D_face_rows"]
    ]
    h_internal_1d = [
        edge["row_sha256"]
        for row in h_rows
        for edge in row["H_partition"]["internal_split_1D_edge_owner_rows"]
    ]
    h_internal_0d = [
        corner["row_sha256"]
        for row in h_rows
        for corner in row["H_partition"]["internal_split_0D_corner_owner_rows"]
    ]
    h_terminal_atomic_audits = [
        row["H_partition"]["terminal_exact_atomic_owner_audit"]
        for row in h_rows
    ]
    h_partitions_exact = all(
        row["H_partition"][
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True
        and row["H_partition"]["terminal_exact_atomic_owner_audit"][
            "closed_3D_leaf_count"
        ] == row["H_partition"]["terminal_rectangle_count"]
        for row in h_rows
    )
    need(h_partitions_exact, "all H partitions exact atomic closure:" + origin)
    typed_sheets = [
        terminal["typed_strata"]["H_zero_2D_sheet"]["row_sha256"]
        for row in h_rows
        for terminal in row["H_partition"]["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
    ]
    closed_face_regions = [
        incidence["row_sha256"]
        for row in h_rows
        for terminal in row["H_partition"]["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
        for incidence in terminal["typed_strata"][
            "terminal_face_2D_H_sign_regions"
        ]
    ]
    closed_edge_regions = [
        incidence["row_sha256"]
        for row in h_rows
        for terminal in row["H_partition"]["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
        for incidence in terminal["typed_strata"][
            "terminal_edge_1D_H_sign_intervals"
        ]
    ]
    closed_corner_signs = [
        incidence["row_sha256"]
        for row in h_rows
        for terminal in row["H_partition"]["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
        for incidence in terminal["typed_strata"][
            "H_zero_0D_corner_absence_rows"
        ]
    ]
    lineage = {
        "Round176_prior_closed_count": prior["prior_closed_count"],
        "Round176_preclosed_frontier_count": len(base_rows),
        "Round176_residual_root_count": len(roots),
        "Round180_inherited_excluded_count": len(inherited_excluded),
        "Round180_inherited_direct_H_count": len(inherited_direct_h),
        "Round180_inherited_same_sign_Delta_followup_H_count": len(
            inherited_followup_h
        ),
        "Round180_inherited_H_materialized_count": len(inherited_h),
        "Round180_final_cell_count": len(final_rows),
        "Round201_exact_behind_closed_count": round201_count,
        "Round215_analytic_closed_count": round215_count,
        "Round306C30A_closed_count": c30a_count,
        "outgoing_H_cell_count": len(h_rows),
        "all_non_H_3D_2D_1D_0D_strata_excluded_or_empty": (
            all_non_h_closed_leaves_excluded
        ),
    }
    composition_evidence = {
        "Round176_prior_rows_sha256": digest(sorted(
            prior["prior_closed_rows"]
        )),
        "Round176_preclosed_frontier_keys_sha256": digest(sorted(
            row.key for row in base_rows
        )),
        "Round176_residual_root_keys_sha256": digest(sorted(
            row.key for row in roots
        )),
        "Round180_inherited_terminal_rows_sha256": digest(inherited),
        "Round180_final_cell_keys_sha256": digest(
            [row.key for row in final_rows]
        ),
        "Round180_split_face_rows_sha256": digest(
            refinement["split_face_rows"]
        ),
        "disposition_aware_half_open_owner_audit": owner_audit,
        "non_H_upstream_evidence_binding_sha256": digest({
            "Round176_prior_evidence_rows_sha256": prior[
                "prior_closed_evidence_rows_sha256"
            ],
            "Round176_preclosed_evidence_rows": base_evidence,
            "Round180_inherited_excluded_rows": inherited_excluded,
            "Round180_inherited_same_sign_Delta_followup_H_rows": (
                inherited_followup_h_evidence
            ),
            "final_excluded_cell_keys": sorted(
                row.key for row in final_rows if row.key not in h_by_key
            ),
            "final_excluded_evidence": final_excluded_evidence,
        }),
        "same_sign_Delta_followup_H_provenance_bucket": {
            "row_count": len(inherited_followup_h_evidence),
            "rows": inherited_followup_h_evidence,
            "rows_sha256": digest(inherited_followup_h_evidence),
            "exact_volume": fraction(sum(
                (
                    r215.box_volume(leaves["terminal"][row["cell_key"]].box)
                    for row in inherited_followup_h
                ),
                Q(0),
            )),
            "post_followup_H_disposition_census": dict(sorted(Counter(
                row["formal_disposition_after_followup_H"]
                for row in inherited_followup_h_evidence
            ).items())),
            "all_Delta_zero_graphs_empty": all(
                row["Delta_zero_graph_inside_closed_box"] is False
                for row in inherited_followup_h_evidence
            ),
            "all_rows_included_in_outgoing_H_ledger": all(
                row["included_in_outgoing_H_cell_ledger"] is True
                for row in inherited_followup_h_evidence
            ),
            "all_rows_receive_zero_exclusion_credit": all(
                row["whole_origin_exclusion_credit"] == 0
                for row in inherited_followup_h_evidence
            ),
        },
        "materialized_H_strata_owner_aggregation": {
            "internal_split_2D_face_count": len(h_internal_2d),
            "internal_split_2D_face_sha256": digest(h_internal_2d),
            "raw_noncredit_internal_split_1D_incidence_count": len(
                h_internal_1d
            ),
            "raw_noncredit_internal_split_1D_incidence_sha256": digest(
                h_internal_1d
            ),
            "raw_noncredit_internal_split_0D_incidence_count": len(
                h_internal_0d
            ),
            "raw_noncredit_internal_split_0D_incidence_sha256": digest(
                h_internal_0d
            ),
            "terminal_exact_atomic_audit_count": len(
                h_terminal_atomic_audits
            ),
            "terminal_exact_atomic_audit_list_sha256": digest(
                h_terminal_atomic_audits
            ),
            "terminal_atomic_2D_owner_row_count": sum(
                audit["atomic_2D_owner_row_count"]
                for audit in h_terminal_atomic_audits
            ),
            "terminal_atomic_1D_owner_row_count": sum(
                audit["atomic_1D_owner_row_count"]
                for audit in h_terminal_atomic_audits
            ),
            "terminal_atomic_0D_owner_row_count": sum(
                audit["atomic_0D_owner_row_count"]
                for audit in h_terminal_atomic_audits
            ),
            "all_H_partitions_exact_atomic_closure": h_partitions_exact,
            "typed_H_zero_2D_sheet_count": len(typed_sheets),
            "typed_H_zero_2D_sheet_sha256": digest(typed_sheets),
            "closed_enclosure_face_2D_sign_region_count": len(
                closed_face_regions
            ),
            "closed_enclosure_face_2D_sign_region_sha256": digest(
                closed_face_regions
            ),
            "closed_enclosure_edge_1D_sign_interval_count": len(
                closed_edge_regions
            ),
            "closed_enclosure_edge_1D_sign_interval_sha256": digest(
                closed_edge_regions
            ),
            "closed_enclosure_corner_0D_strict_sign_count": len(
                closed_corner_signs
            ),
            "closed_enclosure_corner_0D_strict_sign_sha256": digest(
                closed_corner_signs
            ),
            "typed_boundary_ownership_scope": "CLOSED_ENCLOSURE_ONLY",
            "dyadic_boundary_owner_source": (
                "PER_H_CELL_TERMINAL_EXACT_ATOMIC_HALF_OPEN_OWNER_AUDIT"
            ),
        },
        "exact_volume_conservation": {
            "original_parent": fraction(parent_volume),
            "Round176_prior": fraction(prior["prior_closed_exact_volume"]),
            "Round176_preclosed_frontier": fraction(base_volume),
            "Round176_residual_roots": fraction(root_volume),
            "Round180_inherited": fraction(inherited_volume),
            "Round180_final": fraction(final_volume),
            "Round201_exact_behind_closed": fraction(round201_volume),
            "Round215_analytic_closed": fraction(round215_volume),
            "Round306C30A_closed": fraction(c30a_volume),
            "outgoing_H_cells": fraction(h_volume),
            "all_lineage_buckets_pairwise_disjoint": owner_audit[
                "exact_3D_enclosure"
            ]["pairwise_leaf_interiors_disjoint"],
            "all_lineage_buckets_exhaust_original_parent": owner_audit[
                "exact_3D_enclosure"
            ]["leaf_exact_volume_sum_equals_parent"],
        },
    }
    theorem = {
        "kind": "SOURCE_W_OUTGOING_H_WHOLE_ORIGIN_DISPOSITION_THEOREM",
        "prior_frontier_and_refinement_partitions_are_exact": (
            origin_exact_atomic_closure
        ),
        "all_components_outside_materialized_outgoing_H_cells_excluded": (
            all_non_h_closed_leaves_excluded
        ),
        "same_sign_Delta_followup_H_provenance_is_explicitly_bound": bool(
            inherited_followup_h
        ),
        "each_outgoing_H_cell_has_exhaustive_disjoint_3D_2D_1D_0D_partition": (
            h_partitions_exact
        ),
        "half_open_H_zero_owner_rule": (
            "CHART_W_FOR_RELATIVE_INTERIOR__ATOMIC_GRID_FOR_DYADIC_BOUNDARY"
        ),
        "whole_origin_outcome_derived_from_complete_composition": (
            origin_exact_atomic_closure
            and h_partitions_exact
            and whole_disposition == expected_whole
        ),
        "whole_original_physical_origin_excluded": (
            whole_disposition == "EXCLUDED"
        ),
    }
    body = {
        "schema": (
            "cm2.round306c30b.source-w-outgoing-h."
            "whole-origin-disposition.row.v1"
        ),
        "origin_ordinal": origin_ordinal,
        "origin_key": origin,
        "priority_ordinal": registry["priority_ordinal"],
        "source_chart_id": replay["origins"][origin]["chart_id"],
        "original_parent_box": r176.box_row(replay["origins"][origin]["box"]),
        "H_cell_count": len(h_rows),
        "H_cell_keys_sha256": digest([row["cell_key"] for row in h_rows]),
        "H_cell_rows_sha256": digest(h_rows),
        "H_cell_disposition_census": dict(sorted(h_dispositions.items())),
        "whole_origin_disposition": whole_disposition,
        "whole_original_physical_origin_excluded": (
            whole_disposition == "EXCLUDED"
        ),
        "whole_origin_exclusion_credit": int(whole_disposition == "EXCLUDED"),
        "resolved_nonexcluded_credit": int(
            whole_disposition != "EXCLUDED"
        ),
        "positive_measure_LIVE_witness_count": len(live_witnesses),
        "positive_measure_LIVE_witnesses_sha256": digest(live_witnesses),
        "lexicographic_first_positive_measure_LIVE_witness": (
            live_witnesses[0] if live_witnesses else "NOT_APPLICABLE_EXCLUDED"
        ),
        "lineage_composition": lineage,
        "lineage_composition_evidence": composition_evidence,
        "whole_origin_theorem": theorem,
        "whole_origin_theorem_sha256": digest(theorem),
        "formal_credit": {
            "resolved_source_W_origin_disposition": 1,
            "whole_source_W_origin_exclusion": int(
                whole_disposition == "EXCLUDED"
            ),
        },
        "strict_nonpromotion": {
            "child_or_volume_as_integer_credit": 0,
            "D02": 0,
            "D03": 0,
            "D04": 0,
            "Gate5": 0,
            "CM2": 0,
        },
    }
    return sealed_row(body)


def build(candidate_path: Path) -> dict[str, Any]:
    need(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is True
        and sys.flags.no_user_site == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True,
        "scrubbed seeded runtime",
    )
    ctx.prec = 192
    candidate = candidate_directory(candidate_path)
    runtime_path = candidate / RUNTIME_ATTESTATION
    runtime_path.write_bytes(BOOTSTRAP_RUNTIME_ATTESTATION_RAW)
    need(
        runtime_path.read_bytes() == BOOTSTRAP_RUNTIME_ATTESTATION_RAW
        and file_hash(runtime_path) == RUNTIME_ATTESTATION_RAW_SHA256,
        "published runtime attestation bytes",
    )
    bounded, registry, summaries, c30a_rows = collect_frozen_rows()
    replay = r176.replay_frontier()
    target_set = set(ORIGIN_KEYS)
    roots_by_origin: dict[str, list[Any]] = defaultdict(list)
    base_by_origin: dict[str, list[Any]] = defaultdict(list)
    base_kinds: dict[str, set[str]] = defaultdict(set)
    for row in replay["frontier"]:
        if row.origin_key not in target_set:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            roots_by_origin[row.origin_key].append(row)
        else:
            base_by_origin[row.origin_key].append(row)
            base_kinds[row.origin_key].add(kind)
    need(
        set(roots_by_origin) == target_set
        and all(base_kinds[key] <= {"EXCLUDED"} for key in ORIGIN_KEYS),
        "twelve-origin frozen base reconstruction",
    )

    all_h_rows: list[dict[str, Any]] = []
    origin_rows: list[dict[str, Any]] = []
    for origin_ordinal, origin in enumerate(ORIGIN_KEYS):
        roots = sorted(roots_by_origin[origin], key=lambda value: value.key)
        refinement = r180.refine_origin(roots, 4)
        leaves = r215.reconstruct_refinement_leaf_frontiers(roots, refinement)
        inherited = sorted(
            refinement["terminal_rows"], key=lambda value: value["cell_key"]
        )
        h_rows: list[dict[str, Any]] = []
        for evidence in inherited:
            if evidence["coarse_disposition"] == "EXCLUDED":
                continue
            frontier = leaves["terminal"][evidence["cell_key"]]
            if evidence["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX":
                need(
                    origin.endswith("07.01.11011100")
                    and evidence["coarse_disposition"] == "MIXED"
                    and c30a_rows["held_by_origin"].get(origin) is None,
                    "unexpected same-sign Delta followup H terminal:"
                    + evidence["cell_key"],
                )
                source_kind = (
                    "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
                )
                source_binding = inherited_same_sign_delta_followup_h_binding(
                    evidence
                )
            else:
                need(
                    evidence["method"]
                    == "OUTGOING_H_CLOSED_RECTANGLE_TREE",
                    "inherited non-H nonexclusion:" + evidence["cell_key"],
                )
                source_kind, source_binding = inherited_source_binding(
                    evidence,
                    c30a_rows["held_by_origin"].get(origin),
                )
            h_rows.append(sealed_row(h_cell_body(
                source_kind, frontier, source_binding
            )))

        round201_count = 0
        round201_volume = Q(0)
        round215_count = 0
        round215_volume = Q(0)
        c30a_count = 0
        c30a_volume = Q(0)
        rebuilt_r215 = 0
        final_excluded_evidence: dict[str, list[dict[str, Any]]] = {
            "Round201_exact_behind": [],
            "Round215_analytic": [],
            "Round306C30A": [],
        }
        for row in sorted(
            refinement["final_residual_rows"], key=lambda value: value.key
        ):
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            if reduction["closed"]:
                round201_count += 1
                round201_volume += r215.box_volume(row.box)
                final_excluded_evidence["Round201_exact_behind"].append({
                    "cell_key": row.key,
                    "reduction_sha256": digest(reduction_binding(reduction)),
                })
                continue
            if origin in set(HELD_KEYS):
                closed = c30a_rows["c30a_by_key"].get(row.key)
                need(closed is not None, "missing C30a held closure:" + row.key)
                c30a_count += 1
                c30a_volume += r215.box_volume(row.box)
                final_excluded_evidence["Round306C30A"].append({
                    "cell_key": row.key,
                    "C30a_cell_row_sha256": closed["row_sha256"],
                })
                continue
            evidence = reconstructed_r215_evidence(row, reduction)
            if evidence["analytic_closed"]:
                round215_count += 1
                round215_volume += r215.box_volume(row.box)
                final_excluded_evidence["Round215_analytic"].append({
                    "cell_key": row.key,
                    "Round215_cell_row_sha256": evidence["row_sha256"],
                })
                continue
            need(
                evidence["blocker"]
                == "NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST",
                "non-H Round215 residual:" + row.key,
            )
            h_rows.append(sealed_row(h_cell_body(
                "ROUND215_RESIDUAL_OUTGOING_H",
                row,
                r215_source_binding(evidence, reduction),
            )))
            rebuilt_r215 += 1

        expected_summary = summaries[origin]
        need(
            rebuilt_r215 == EXPECTED_R215_H_CELLS_BY_ORIGIN.get(origin, 0)
            and round215_count
            == expected_summary["Round215_analytic_closed_cell_count"]
            and (
                c30a_count == 36 if origin in set(HELD_KEYS)
                else c30a_count == 0
            ),
            "final composition census:" + origin,
        )
        origin_row = origin_materialization(
            origin_ordinal,
            origin,
            replay,
            roots,
            sorted(base_by_origin[origin], key=lambda value: value.key),
            refinement,
            leaves,
            h_rows,
            round201_count,
            round201_volume,
            round215_count,
            round215_volume,
            c30a_count,
            c30a_volume,
            final_excluded_evidence,
            registry[origin],
        )
        all_h_rows.extend(h_rows)
        origin_rows.append(origin_row)

    all_h_rows.sort(key=lambda value: value["cell_key"])
    origin_rows.sort(key=lambda value: value["origin_key"])
    h_census = Counter(
        row["whole_H_cell_disposition"] for row in all_h_rows
    )
    h_source_census = Counter(row["source_kind"] for row in all_h_rows)
    hybrid_rows = [
        row for row in all_h_rows
        if row["source_kind"]
        == "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
    ]
    hybrid_terminal_projection_pairs = tuple(
        (
            row["source_binding"]["Round180_terminal_sha256"],
            row["H_partition"]["analytic_semantic_projection_sha256"],
        )
        for row in hybrid_rows
    )
    hybrid_binding = {
        "cell_keys_sha256": digest([
            row["cell_key"] for row in hybrid_rows
        ]),
        "full_terminal_evidence_sha256": digest([
            row["source_binding"]["Round180_terminal_evidence"]
            for row in hybrid_rows
        ]),
        "terminal_sha256_list_sha256": digest([
            row["source_binding"]["Round180_terminal_sha256"]
            for row in hybrid_rows
        ]),
        "analytic_semantic_projection_sha256_list_sha256": digest([
            row["H_partition"]["analytic_semantic_projection_sha256"]
            for row in hybrid_rows
        ]),
        "terminal_to_analytic_semantic_projection_pair_count": len(
            hybrid_terminal_projection_pairs
        ),
        "terminal_to_analytic_semantic_projection_pairs_sha256": digest([
            {"Round180_terminal_sha256": terminal_sha,
             "analytic_semantic_projection_sha256": projection_sha}
            for terminal_sha, projection_sha in hybrid_terminal_projection_pairs
        ]),
    }
    origin_census = Counter(
        row["whole_origin_disposition"] for row in origin_rows
    )
    typed_count = sum(row["typed_H_zero_2D_sheet_count"] for row in all_h_rows)
    excluded_keys = [
        row["origin_key"] for row in origin_rows
        if row["whole_origin_disposition"] == "EXCLUDED"
    ]
    mixed_keys = [
        row["origin_key"] for row in origin_rows
        if row["whole_origin_disposition"] == "RESOLVED_MIXED"
    ]
    need(
        len(all_h_rows) == EXPECTED_H_CELLS
        and h_census == EXPECTED_H_CELL_DISPOSITION
        and h_source_census == EXPECTED_H_SOURCE_KIND
        and len(hybrid_rows) == 8
        and Counter(row["origin_key"] for row in hybrid_rows)
        == Counter({
            "W:N:07.01.11011100": 4,
            "W:S:H.07.01.11011100": 4,
        })
        and hybrid_terminal_projection_pairs
        == EXPECTED_HYBRID_TERMINAL_TO_ANALYTIC_SEMANTIC_PROJECTION_SHA256
        and {
            key: hybrid_binding[key]
            for key in (
                "cell_keys_sha256",
                "full_terminal_evidence_sha256",
                "terminal_sha256_list_sha256",
                "analytic_semantic_projection_sha256_list_sha256",
            )
        } == {
            "cell_keys_sha256": EXPECTED_HYBRID_CELL_KEYS_SHA256,
            "full_terminal_evidence_sha256": (
                EXPECTED_HYBRID_TERMINAL_ROWS_SHA256
            ),
            "terminal_sha256_list_sha256": (
                EXPECTED_HYBRID_TERMINAL_SHA_LIST_SHA256
            ),
            "analytic_semantic_projection_sha256_list_sha256": (
                EXPECTED_HYBRID_ANALYTIC_SEMANTIC_PROJECTION_SHA_LIST_SHA256
            ),
        }
        and typed_count == 192
        and origin_census == Counter({"RESOLVED_MIXED": 10, "EXCLUDED": 2})
        and digest(excluded_keys) == EXPECTED_EXCLUDED_KEYS_SHA256
        and digest(mixed_keys) == EXPECTED_MIXED_KEYS_SHA256,
        "global outgoing-H disposition census",
    )

    h_count, h_sequence = write_rows(candidate / H_CELL_LEDGER, all_h_rows)
    origin_count, origin_sequence = write_rows(
        candidate / ORIGIN_LEDGER, origin_rows
    )
    need(h_count == EXPECTED_H_CELLS and origin_count == 12,
         "published outgoing-H ledgers")
    h_descriptor = descriptor(
        candidate / H_CELL_LEDGER,
        h_count,
        h_sequence,
        "LEXICOGRAPHIC_H_CELL_KEY",
    )
    origin_descriptor = descriptor(
        candidate / ORIGIN_LEDGER,
        origin_count,
        origin_sequence,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    runtime_descriptor = {
        "filename": RUNTIME_ATTESTATION,
        "size": len(BOOTSTRAP_RUNTIME_ATTESTATION_RAW),
        "sha256": RUNTIME_ATTESTATION_RAW_SHA256,
        "attestation_payload_sha256": RUNTIME_ATTESTATION_PAYLOAD_SHA256,
        "auditor_sha256": RUNTIME_AUDITOR_SHA256,
        "schema": BOOTSTRAP_RUNTIME_ATTESTATION["schema"],
        "verdict": BOOTSTRAP_RUNTIME_ATTESTATION["verdict"],
    }
    all_keys = [row["origin_key"] for row in origin_rows]
    need(
        digest(all_keys)
        == "f133c1e5e9b2f467e3fad8e691b6bb81eaf3ac65a931e67ef2a0e20dc8486335",
        "twelve origin key digest",
    )
    body = {
        "schema": (
            "cm2.round306c30b.source-w-outgoing-h-"
            "whole-origin-disposition.v1"
        ),
        "status": "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION",
        "input_pins": INPUT_PINS,
        "runtime_attestation": runtime_descriptor,
        "H_cell_census": {
            "input": EXPECTED_H_CELLS,
            "by_disposition": dict(sorted(h_census.items())),
            "by_source_kind": dict(sorted(h_source_census.items())),
            "typed_H_zero_2D_sheet_count": typed_count,
            "same_sign_Delta_followup_H": {
                "row_count": len(hybrid_rows),
                **hybrid_binding,
            },
        },
        "whole_origin_census": {
            "audited": 12,
            "excluded": 2,
            "resolved_mixed": 10,
            "all_origin_keys_sha256": digest(all_keys),
            "excluded_origin_keys_sha256": digest(excluded_keys),
            "resolved_mixed_origin_keys_sha256": digest(mixed_keys),
        },
        "source_W_ledger_transition": {
            "before": {
                "excluded": BEFORE_EXCLUDED,
                "conservative_live": BEFORE_LIVE,
                "remaining": BEFORE_REMAINING,
                "resolved_nonexcluded": BEFORE_RESOLVED_NONEXCLUDED,
                "total": 76_832,
                "remaining_partition": {
                    "outgoing_H": 12,
                    "full_Delta": 2,
                    "multi_Delta": 20,
                    "reduced_live": 2,
                    "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "credits": {
                "whole_origin_exclusion": 2,
                "resolved_origin_disposition": 12,
                "resolved_nonexcluded": 10,
            },
            "after": {
                "excluded": AFTER_EXCLUDED,
                "conservative_live": AFTER_LIVE,
                "remaining": AFTER_REMAINING,
                "resolved_nonexcluded": AFTER_RESOLVED_NONEXCLUDED,
                "total": 76_832,
                "remaining_partition": {
                    "full_Delta": 2,
                    "multi_Delta": 20,
                    "reduced_live": 2,
                    "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "conservation_identity": "74746+2086=76832",
        },
        "ledgers": {
            "outgoing_H_cell": h_descriptor,
            "whole_origin_disposition": origin_descriptor,
        },
        "formal_credit": {
            "outgoing_H_cells_disposed": EXPECTED_H_CELLS,
            "resolved_source_W_origin_dispositions": 12,
            "whole_source_W_origin_exclusions": 2,
        },
        "strict_nonpromotion": {
            "D02": (
                "BLOCKED_BY_80_REMAINING_SOURCE_W_ORIGINS_"
                "AND_COMPOSITE_GATE"
            ),
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "CLOSE_2_FULL_DELTA_THEN_20_MULTI_DELTA_THEN_2_REDUCED_LIVE_"
            "THEN_2_RETAINED_SOURCE_SEAMS_THEN_54_COMPACT_Q_ORIGINS"
        ),
    }
    result = {**body, "result_sha256": digest(body)}
    (candidate / RESULT).write_bytes(canonical(result))
    need(
        {path.name for path in candidate.iterdir()} == {
            H_CELL_LEDGER, ORIGIN_LEDGER, RESULT, RUNTIME_ATTESTATION,
        },
        "candidate final exact file set",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    arguments = parser.parse_args()
    result = build(Path(arguments.candidate_dir))
    print(canonical({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
