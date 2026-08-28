#!/usr/bin/env python3
"""Independent verifier for the Round306C30b outgoing-H disposition.

The verifier deliberately does not import or execute the C30b producer.  It
replays the pinned Round184/Round215 mathematics, checks the complete sealed
C30a hand-off, reconstructs all H partitions and their half-open lower strata,
and only then compares the candidate's canonical ledgers and result object.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import io
import json
import os
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator
from types import MappingProxyType

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
RUNTIME_AUDITOR = "cm2_round306c30b_python_flint_runtime_attestation_auditor.py"
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


def _bootstrap_regular_bytes(path: Path, maximum: int) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    if not (
        stat.S_ISREG(status.st_mode) and not absolute.is_symlink()
        and status.st_nlink == 1 and 0 < status.st_size <= maximum
    ):
        raise RuntimeError("bootstrap regular singleton:" + absolute.name)
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        if not (
            stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino, opened.st_size)
            == (status.st_dev, status.st_ino, status.st_size)
        ):
            raise RuntimeError("bootstrap opened identity:" + absolute.name)
        output = bytearray()
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1024 * 1024, remaining))
            if not block:
                raise RuntimeError("bootstrap short read:" + absolute.name)
            output.extend(block)
            remaining -= len(block)
        if os.read(descriptor, 1):
            raise RuntimeError("bootstrap growing input:" + absolute.name)
        return bytes(output)
    finally:
        os.close(descriptor)


def _bootstrap_runtime_attestation() -> tuple[bytes, dict[str, Any]]:
    if any(
        name == "flint" or name.startswith("flint.")
        for name in sys.modules
    ):
        raise RuntimeError(
            "flint modules preloaded before runtime attestation"
        )
    auditor = ROOT / RUNTIME_AUDITOR
    auditor_raw = _bootstrap_regular_bytes(auditor, 4 * 1024 * 1024)
    if hashlib.sha256(auditor_raw).hexdigest() != RUNTIME_AUDITOR_SHA256:
        raise RuntimeError("bootstrap runtime auditor pin")
    completed = subprocess.run(
        [sys.executable, "-I", "-B", os.fspath(auditor)],
        cwd=WORKSPACE,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    raw = completed.stdout
    if completed.returncode != 0 or completed.stderr or not raw.endswith(b"\n"):
        raise RuntimeError("bootstrap runtime auditor process")
    payload = raw[:-1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise ValueError("duplicate key")
            output[key] = value
        return output

    try:
        value = json.loads(
            payload.decode("ascii"),
            object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise RuntimeError("bootstrap runtime attestation JSON") from error
    canonical = json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    if type(value) is not dict or raw != canonical + b"\n":
        raise RuntimeError("bootstrap canonical runtime attestation")
    expected_keys = {
        "schema", "verdict", "offline", "auditor", "trust_roots",
        "sealed_wheel", "interpreter", "installed_distribution",
        "native_runtime", "imported_flint", "attestation_payload_sha256",
    }
    body = {
        key: item for key, item in value.items()
        if key != "attestation_payload_sha256"
    }
    if not (
        set(value) == expected_keys
        and value["schema"]
        == "cm2.round306c30b.python-flint-runtime-attestation.v1"
        and value["verdict"] == "PASS"
        and value["offline"] is True
        and value["auditor"] == {
            "path": "deliverables/" + RUNTIME_AUDITOR,
            "sha256": RUNTIME_AUDITOR_SHA256,
        }
        and value["trust_roots"]["p0_runtime_lock"]["sha256"]
        == "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79"
        and value["trust_roots"]["requirements_lock"]["sha256"]
        == "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c"
        and value["attestation_payload_sha256"]
        == hashlib.sha256(json.dumps(
            body, ensure_ascii=True, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")).hexdigest()
        == RUNTIME_ATTESTATION_PAYLOAD_SHA256
        and hashlib.sha256(raw).hexdigest() == RUNTIME_ATTESTATION_RAW_SHA256
    ):
        raise RuntimeError("bootstrap runtime attestation contract")
    return raw, value


BOOTSTRAP_RUNTIME_ATTESTATION_RAW, BOOTSTRAP_RUNTIME_ATTESTATION = (
    _bootstrap_runtime_attestation()
)

import flint


PREFIX = "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition"
H_LEDGER = PREFIX + "_h_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
PRODUCER = PREFIX + "_producer.py"

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
C30A_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
C30A_MANIFEST = C30A_PREFIX + "_manifest.sha256"
C30A_SOURCE = C30A_PREFIX + "_producer.py"
C30A_SEALED = ROOT / "cm2_round306c30a_sealed"
C30A_CELL = C30A_PREFIX + "_cell_ledger.jsonl.gz"
C30A_HELD = C30A_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz"
C30A_ORIGIN = C30A_PREFIX + "_whole_origin_ledger.jsonl.gz"
C30A_RESULT = C30A_PREFIX + "_result.json"
RUNTIME_REQUIREMENTS = "cm2_round306c30a_python_flint_requirements.lock"
RUNTIME_LOCK = "cm2_round306c30a_python_flint_runtime_lock.json"

PINS = {
    RUNTIME_AUDITOR: RUNTIME_AUDITOR_SHA256,
    C30A_SOURCE:
        "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714",
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
    C30A_MANIFEST:
        "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc",
    RUNTIME_REQUIREMENTS:
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    RUNTIME_LOCK:
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
}
C30A_SEALED_PINS = {
    C30A_CELL:
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    C30A_HELD:
        "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    C30A_ORIGIN:
        "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
    C30A_RESULT:
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
}

R215_BOUNDED_RESULT_SHA256 = (
    "e6af59b19440723c4770a286d6261d950fb2a22702ec8900d285b43a06d0158c"
)
R215_CELL_ROWS_SHA256 = (
    "50431dc6c73add077aef263c781df428d81493751250bf1683f9c560faa420d9"
)
EXPECTED_R215_H_KEYS = (
    "W:N:07.01.01100010", "W:N:07.01.01101001",
    "W:N:07.01.01101110", "W:N:07.01.11000101",
    "W:N:07.01.11011100", "W:S:H.07.01.01100010",
    "W:S:H.07.01.01101001", "W:S:H.07.01.01101110",
    "W:S:H.07.01.11000101", "W:S:H.07.01.11011100",
)
EXPECTED_HELD_KEYS = (
    "W:N:04.00.10101011", "W:S:H.04.00.10101011",
)
EXPECTED_KEYS = tuple(sorted(EXPECTED_R215_H_KEYS + EXPECTED_HELD_KEYS))
EXPECTED_EXCLUDED_KEYS = (
    "W:N:07.01.01100010", "W:S:H.07.01.01100010",
)
EXPECTED_MIXED_KEYS = tuple(
    key for key in EXPECTED_KEYS if key not in set(EXPECTED_EXCLUDED_KEYS)
)
EXPECTED_ALL_KEYS_SHA256 = (
    "f133c1e5e9b2f467e3fad8e691b6bb81eaf3ac65a931e67ef2a0e20dc8486335"
)
EXPECTED_EXCLUDED_KEYS_SHA256 = (
    "ae9b6dbdeab5163fac6ab992766d019d36fedcbc392a94f7dae7f95370dd317d"
)
EXPECTED_MIXED_KEYS_SHA256 = (
    "507447f2a97f8c804280b2a46de8aef70e7dd7260835edd9ec2a1f22bf155ba8"
)
EXPECTED_R215_PER_ORIGIN = {
    "W:N:07.01.01100010": 8, "W:N:07.01.01101001": 40,
    "W:N:07.01.01101110": 40, "W:N:07.01.11000101": 152,
    "W:N:07.01.11011100": 40, "W:S:H.07.01.01100010": 8,
    "W:S:H.07.01.01101001": 40, "W:S:H.07.01.01101110": 40,
    "W:S:H.07.01.11000101": 152, "W:S:H.07.01.11011100": 40,
}
H_EXCLUSION_CLASSES = {
    "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
    "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
}
H_LIVE_CLASSES = {
    "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
    "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
}
H_TYPED = "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"
EXPECTED_H_CELL_CENSUS = Counter({
    "EXCLUDED": 352, "LIVE": 144, "MIXED": 192,
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
EXPECTED_HYBRID_ANALYTIC_SEMANTIC_PROJECTION_SHA_LIST_SHA256 = (
    "7aa65c7d779078b89fe745b0883008805db1cb17b4c24806c38199e1dfa8bf28"
)


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_hash(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def regular_bytes(path: Path, maximum: int = 64 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode) and not absolute.is_symlink()
        and status.st_nlink == 1 and 0 < status.st_size <= maximum,
        "regular singleton:" + absolute.name,
    )
    descriptor = os.open(absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino) == (status.st_dev, status.st_ino),
            "opened identity:" + absolute.name,
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(block), "short read:" + absolute.name)
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing input:" + absolute.name)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def strict_object_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(raw and b"\x00" not in raw, "nonempty JSON:" + label)
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output

    def reject_constant(token: str) -> None:
        raise ValueError(token)

    try:
        text = raw.decode("ascii")
        value = json.loads(
            text, object_pairs_hook=unique, parse_constant=reject_constant,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    require(type(value) is dict, "JSON object:" + label)
    canonical = wire(value)
    require(raw in {canonical, canonical + b"\n"}, "canonical JSON:" + label)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    return strict_object_bytes(regular_bytes(path), path.name)


def canonical_rows(path: Path) -> list[dict[str, Any]]:
    raw = regular_bytes(path)
    require(raw[:2] == b"\x1f\x8b" and raw[3] == 0, "canonical gzip header:" + path.name)
    try:
        clear = gzip.decompress(raw)
    except (OSError, EOFError) as error:
        raise Reject("gzip stream:" + path.name) from error
    require(clear.endswith(b"\n") and b"\r" not in clear, "JSONL framing:" + path.name)
    canonical_stream = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=canonical_stream,
        compresslevel=9, mtime=0,
    ) as output:
        output.write(clear)
    require(raw == canonical_stream.getvalue(), "canonical gzip bytes:" + path.name)
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(clear.splitlines()):
        row = strict_object_bytes(line, f"{path.name}:{ordinal}")
        require(row.get("row_sha256") is not None, "row hash present")
        body = dict(row)
        claimed = body.pop("row_sha256")
        require(claimed == digest(body), "row hash:" + path.name)
        rows.append(row)
    return rows


def pinned_pretty_json(path: Path) -> dict[str, Any]:
    """Strictly parse a hash-pinned upstream JSON that is intentionally pretty."""
    raw = regular_bytes(path)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, "duplicate pinned JSON key:" + path.name)
            output[key] = value
        return output

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict pinned JSON:" + path.name) from error
    require(type(value) is dict, "pinned JSON object:" + path.name)
    return value


def validate_runtime() -> None:
    lock = pinned_pretty_json(ROOT / RUNTIME_LOCK)
    site_packages = (
        WORKSPACE
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
            require(
                resolved.is_relative_to(site_packages),
                "loaded flint file outside attested distribution",
            )
            relative = resolved.relative_to(site_packages).as_posix()
            require(
                installed_files.get(relative) == file_hash(resolved),
                "loaded flint file hash:" + relative,
            )
            loaded_flint_files[module_name + ":" + attribute] = relative
    attested_import = BOOTSTRAP_RUNTIME_ATTESTATION["imported_flint"]
    require(
        sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1
        and sys.flags.no_user_site == 1 and sys.dont_write_bytecode is True
        and sys.implementation.name == lock["implementation"]
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
        "locked isolated python-flint runtime",
    )


def validate_manifest() -> dict[str, str]:
    raw = regular_bytes(ROOT / C30A_MANIFEST, 64 * 1024)
    require(file_hash(ROOT / C30A_MANIFEST) == PINS[C30A_MANIFEST], "C30a manifest pin")
    expected: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        require(len(parts) == 2 and len(parts[0]) == 64, "C30a manifest syntax")
        require(parts[1] not in expected and ".." not in Path(parts[1]).parts, "C30a manifest path")
        expected[parts[1]] = parts[0]
    for filename, claimed in expected.items():
        path = ROOT / filename
        require(path.resolve().is_relative_to(ROOT.resolve()), "manifest containment")
        require(file_hash(path) == claimed, "C30a manifest member:" + filename)
    for filename, claimed in C30A_SEALED_PINS.items():
        manifest_name = "cm2_round306c30a_sealed/" + filename
        require(expected.get(manifest_name) == claimed, "sealed manifest member:" + filename)
    return expected


def validate_sources() -> list[dict[str, str]]:
    validate_runtime()
    pins: list[dict[str, str]] = []
    for filename, expected in sorted(PINS.items()):
        actual = file_hash(ROOT / filename)
        require(actual == expected, "source pin:" + filename)
        pins.append({"filename": filename, "sha256": actual})
    manifest = validate_manifest()
    for filename, expected in sorted(C30A_SEALED_PINS.items()):
        actual = file_hash(C30A_SEALED / filename)
        require(actual == expected, "sealed C30a pin:" + filename)
        pins.append({
            "filename": "cm2_round306c30a_sealed/" + filename,
            "sha256": actual,
        })
    certificate = pinned_pretty_json(ROOT / R215_CERTIFICATE)
    r215_verify = pinned_pretty_json(ROOT / R215_VERIFICATION)
    r184_verify = pinned_pretty_json(ROOT / R184_VERIFICATION)
    c30a = pinned_pretty_json(C30A_SEALED / C30A_RESULT)
    require(
        certificate["result"]["bounded_probe_result_sha256"]
        == R215_BOUNDED_RESULT_SHA256
        and r215_verify["result"]["verdict"] == "PASS"
        and r184_verify["result"]["status"] == "PASS_PARTIAL_BOUNDED_ROUND184"
        and c30a["result_sha256"]
        == "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
        and c30a["source_W_ledger_transition"]["after"]
        == {
            "conservative_live": 2088, "excluded": 74744,
            "remaining": 92,
            "remaining_partition": {
                "compact_q": 54, "mixed_active_nonseam": 36,
                "mixed_retained_source_seams": 2, "total": 92,
            },
            "total": 76832,
        }
        and c30a["strict_nonpromotion"]["D02"]
        == "BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS",
        "sealed upstream state",
    )
    pin_map = {row["filename"]: row["sha256"] for row in pins}
    for filename, expected in manifest.items():
        require(pin_map.get(filename) in {None, expected}, "manifest/pin agreement")
        pin_map[filename] = expected
    return [
        {"filename": filename, "sha256": expected}
        for filename, expected in sorted(pin_map.items())
    ]


# Import only the pinned mathematical probe.  The candidate producer name is
# never passed to importlib and is rejected if it appears in sys.modules.
validate_runtime()
if os.fspath(ROOT) not in sys.path:
    sys.path.insert(0, os.fspath(ROOT))
require(
    not any(
        name in sys.modules
        for name in (
            PRODUCER[:-3], C30A_SOURCE[:-3], R215_PROBE[:-3],
            R201_VERIFIER[:-3], R180_VERIFIER[:-3], R176_VERIFIER[:-3],
        )
    ),
    "candidate/upstream modules not preloaded",
)
r215 = importlib.import_module(R215_PROBE[:-3])
r201 = r215.r201
r176 = r215.r176
r180 = r215.r180


def validate_imported_mathematics() -> None:
    modules = {
        R215_PROBE: r215,
        R201_VERIFIER: r201,
        R180_VERIFIER: r180,
        R176_VERIFIER: r176,
    }
    for filename, module in modules.items():
        expected_path = (ROOT / filename).resolve(strict=True)
        actual_path = Path(module.__file__).resolve(strict=True)
        require(
            sys.modules.get(filename[:-3]) is module
            and actual_path == expected_path
            and PINS.get(filename) == file_hash(actual_path),
            "imported mathematics module identity/hash:" + filename,
        )
    require(
        PRODUCER[:-3] not in sys.modules
        and C30A_SOURCE[:-3] not in sys.modules,
        "producer independence after upstream import",
    )


validate_imported_mathematics()
validate_runtime()


def capture_round215() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
    dict[str, tuple[str | None, dict[str, Any]]],
]:
    captured: list[dict[str, Any]] = []
    captured_replays: list[dict[str, Any]] = []
    residual_frontiers: dict[str, Any] = {}
    closure_results: dict[str, tuple[str | None, dict[str, Any]]] = {}
    original_add = r215.ListDigest.add
    original_replay = r176.replay_frontier
    original_analyze = r215.analyze_residual_cell
    original_closure = r176.closure

    def recording(self: Any, value: Any) -> None:
        # Round215 creates exactly one ListDigest, and every value added to
        # it is one complete active-cell evidence row.  Those upstream rows
        # intentionally have no per-row schema field, so filtering on a
        # fabricated schema would capture zero rows and fail closed only
        # after the expensive replay.
        require(type(value) is dict, "Round215 cell evidence row type")
        captured.append(value)
        original_add(self, value)

    def recording_replay() -> dict[str, Any]:
        require(not captured_replays, "single Round176 replay in Round215")
        value = original_replay()
        captured_replays.append(value)
        return value

    def recording_analyze(row: Any, reduction: dict[str, Any]) -> dict[str, Any]:
        require(
            row.key not in residual_frontiers,
            "unique Round215 residual frontier:" + row.key,
        )
        residual_frontiers[row.key] = row
        return original_analyze(row, reduction)

    def recording_closure(row: Any) -> tuple[str | None, dict[str, Any]]:
        require(
            row.key not in closure_results,
            "unique Round215 Round176 closure:" + row.key,
        )
        value = original_closure(row)
        closure_results[row.key] = value
        return value

    r215.ListDigest.add = recording
    r176.replay_frontier = recording_replay
    r215.analyze_residual_cell = recording_analyze
    r176.closure = recording_closure
    try:
        result = r215.rebuild()
    finally:
        r215.ListDigest.add = original_add
        r176.replay_frontier = original_replay
        r215.analyze_residual_cell = original_analyze
        r176.closure = original_closure
    require(
        len(captured) == 18_432
        and len(captured_replays) == 1
        and len(residual_frontiers) == 18_432
        and set(residual_frontiers)
        == {value["cell_key"] for value in captured}
        and closure_results
        and set(closure_results) <= {
            row.key for row in captured_replays[0]["frontier"]
        }
        # ``Round215.rebuild`` returns the result body.  The published probe
        # wraps it and commits ``digest(result)`` as ``probe_result_sha256``;
        # there is deliberately no self-hash field inside this body.
        and digest(result) == R215_BOUNDED_RESULT_SHA256
        and digest(captured) == R215_CELL_ROWS_SHA256,
        "full Round215 reconstruction",
    )
    return (
        result, captured, captured_replays[0], residual_frontiers,
        closure_results,
    )


def derive_source_w_frontier_lanes(
    bounded: dict[str, Any],
    evidence_rows: list[dict[str, Any]],
) -> dict[str, tuple[str, ...]]:
    """Derive the 92-origin C30a hand-off without trusting C30b keys.

    The R215 body is independently rebuilt above.  Starting from its full
    198-row active outcome, remove exactly the two R215 formal promotions and
    the 160 sealed C30a promotions.  Classify the remaining 36 active origins
    solely by their reconstructed blocker support, with the two fail-closed
    C30a inherited-H holds added to the direct outgoing-H lane.  The retained
    seams and compact-q cohort are independently recovered from R215/R184.
    """
    outcome = bounded["whole_origin_outcome"]
    per_origin_rows = outcome["per_origin_rows"]
    per_origin = {row["origin_key"]: row for row in per_origin_rows}
    require(
        len(per_origin_rows) == len(per_origin) == 198,
        "R215 active outcome identity",
    )
    evidence_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for evidence in evidence_rows:
        evidence_by_origin[evidence["origin_key"]].append(evidence)
    require(
        set(evidence_by_origin) == set(per_origin)
        and sum(map(len, evidence_by_origin.values())) == 18_432,
        "R215 per-cell/per-origin exhaustion",
    )
    derived_formal: set[str] = set()
    for origin, summary in per_origin.items():
        rows = evidence_by_origin[origin]
        blockers = Counter(
            row["blocker"] for row in rows if not row["analytic_closed"]
        )
        methods = Counter(row["method"] for row in rows)
        analytic_closed = sum(row["analytic_closed"] for row in rows)
        all_closed = not blockers
        require(
            len(rows) == summary["Round201_residual_cell_count"]
            and analytic_closed
            == summary["Round215_analytic_closed_cell_count"]
            and dict(sorted(blockers.items()))
            == summary["Round215_blocker_count"]
            and dict(sorted(methods.items())) == summary["Round215_method_count"]
            and all_closed
            is summary["all_Round201_residual_cells_analytically_closed"]
            and digest([digest(row) for row in rows])
            == summary["per_cell_evidence_hashes_sha256"],
            "independent R215 per-origin summary:" + origin,
        )
        if all_closed:
            derived_formal.add(origin)
    formal = set(outcome["candidate_complete_origin_keys"])
    require(
        formal == derived_formal
        and len(formal) == outcome["candidate_complete_origin_count"] == 2,
        "R215 formal promotion identity",
    )
    c30a_cell_rows = canonical_rows(C30A_SEALED / C30A_CELL)
    c30a_cell_keys = [row["cell_key"] for row in c30a_cell_rows]
    clipped_evidence_keys = [
        row["cell_key"] for row in evidence_rows
        if row["blocker"] == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
    ]
    require(
        len(c30a_cell_keys) == len(set(c30a_cell_keys)) == 12_888
        and set(c30a_cell_keys) == set(clipped_evidence_keys)
        and len(clipped_evidence_keys) == 12_888,
        "C30a complete clipped-cell hand-off",
    )
    c30a_cells_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in c30a_cell_rows:
        c30a_cells_by_origin[row["origin_key"]].append(row)
    pure_clipped_closed = {
        origin for origin, summary in per_origin.items()
        if set(summary["Round215_blocker_count"])
        == {"SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"}
        and origin in c30a_cells_by_origin
        and all(
            row["whole_closed_cell_excluded"]
            for row in c30a_cells_by_origin[origin]
        )
    }
    promoted_rows = canonical_rows(C30A_SEALED / C30A_ORIGIN)
    promoted = {row["origin_key"] for row in promoted_rows}
    held_rows = canonical_rows(C30A_SEALED / C30A_HELD)
    held = {row["origin_key"] for row in held_rows}
    require(
        len(promoted_rows) == len(promoted) == 160
        and len(held_rows) == len(held) == 2
        and formal.isdisjoint(promoted | held)
        and promoted.isdisjoint(held)
        and formal | promoted | held <= set(per_origin),
        "sealed R215/C30a active dispositions",
    )
    require(
        pure_clipped_closed == promoted | held
        and len(pure_clipped_closed) == 162,
        "outcome-derived C30a 160 promoted plus 2 held",
    )
    active = set(per_origin) - formal - promoted
    require(len(active) == 36 and held <= active,
            "derived 36-origin active frontier")

    direct_h: set[str] = set()
    full_delta: set[str] = set()
    multi_delta: set[str] = set()
    reduced_live: set[str] = set()
    for origin in active - held:
        blockers = set(per_origin[origin]["Round215_blocker_count"])
        if blockers == {"NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST"}:
            direct_h.add(origin)
        elif "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED" in blockers:
            require(
                blockers == {
                    "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP",
                    "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED",
                },
                "full-Delta blocker support:" + origin,
            )
            full_delta.add(origin)
        elif "MULTI_DELTA_GRAPH_ARRANGEMENT" in blockers:
            require(
                blockers == {
                    "MULTI_DELTA_GRAPH_ARRANGEMENT",
                    "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP",
                },
                "multi-Delta blocker support:" + origin,
            )
            multi_delta.add(origin)
        elif "REDUCED_LIVE_3D_CELL" in blockers:
            require(
                blockers == {
                    "NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST",
                    "REDUCED_LIVE_3D_CELL",
                },
                "reduced-live blocker support:" + origin,
            )
            reduced_live.add(origin)
        else:
            raise Reject("unclassified active Source-W origin:" + origin)

    require(
        all(
            set(per_origin[origin]["Round215_blocker_count"])
            == {"SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"}
            for origin in held
        ),
        "C30a held blocker support",
    )
    outgoing_h = direct_h | held
    classified_active = outgoing_h | full_delta | multi_delta | reduced_live
    require(
        classified_active == active
        and sum(map(len, (outgoing_h, full_delta, multi_delta, reduced_live)))
        == len(active)
        and (len(outgoing_h), len(full_delta), len(multi_delta), len(reduced_live))
        == (12, 2, 20, 2),
        "derived active Source-W lane partition",
    )

    seams = set(bounded["Round212_seam_exclusion"]["seam_origin_keys"])
    registry_rows = pinned_pretty_json(ROOT / R184_CERTIFICATE)["result"][
        "priority_registry"
    ]["rows"]
    compact_q = {
        row["origin_key"] for row in registry_rows
        if row["priority_class"] == "COMPACT_Q_PRESENT"
    }
    require(
        len(seams) == bounded["Round212_seam_exclusion"]["seam_origin_count"] == 2
        and digest(sorted(seams))
        == bounded["Round212_seam_exclusion"]["seam_origin_keys_sha256"]
        and len(compact_q) == 54
        and digest(sorted(compact_q))
        == bounded["selection"]["outer_audit_compact_q_origin_keys_sha256"]
        and active.isdisjoint(seams | compact_q)
        and set(per_origin).isdisjoint(seams | compact_q)
        and seams.isdisjoint(compact_q),
        "derived seam/compact-q lane partition",
    )
    lanes = {
        "outgoing_H": tuple(sorted(outgoing_h)),
        "full_Delta": tuple(sorted(full_delta)),
        "multi_Delta": tuple(sorted(multi_delta)),
        "reduced_live": tuple(sorted(reduced_live)),
        "retained_source_seams": tuple(sorted(seams)),
        "compact_q": tuple(sorted(compact_q)),
    }
    require(
        tuple(lanes["outgoing_H"]) == EXPECTED_KEYS
        and sum(len(value) for value in lanes.values()) == 92,
        "outcome-derived outgoing-H keys / 92-origin frontier",
    )
    return lanes


def sealed(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def sign_name(value: Any) -> str:
    value_sign = r176.sign(value)
    return (
        "STRICT_POSITIVE" if value_sign > 0
        else "STRICT_NEGATIVE" if value_sign < 0 else "OVERWRAP"
    )


def point_box(
    box: Any, *, t_value: Q | None = None, p_value: Q | None = None
) -> Any:
    return r176.Box(
        box.t0 if t_value is None else t_value,
        box.t1 if t_value is None else t_value,
        box.p0 if p_value is None else p_value,
        box.p1 if p_value is None else p_value,
        box.s0, box.s1, box.depth, box.path,
    )


def independent_seam_evidence(
    chart_id: str, box: Any, seam_id: str
) -> dict[str, Any]:
    data = r176.SEAMS[seam_id]
    _cell, nx, ny = r176.tight_contact(chart_id, box)
    values = r176.seam_values(chart_id, box, seam_id)
    corners_raw = {
        f"t{ti}_p{pi}": r176.seam_values(
            chart_id, point_box(box, t_value=t, p_value=p), seam_id
        )["H"]
        for ti, t in enumerate((box.t0, box.t1))
        for pi, p in enumerate((box.p0, box.p1))
    }
    corners = {key: sign_name(value) for key, value in sorted(corners_raw.items())}
    integer_signs = [r176.sign(value) for value in corners_raw.values()]
    lower = r176.seam_values(
        chart_id, point_box(box, p_value=box.p0), seam_id
    )["H"]
    upper = r176.seam_values(
        chart_id, point_box(box, p_value=box.p1), seam_id
    )["H"]
    dt_sign = r176.sign(values["dt"])
    typed = (
        r176.sign(data["normal"](nx, ny)) == 0
        and bool(data["other"](nx, ny) < 0)
        and bool(values["forward"] > 0)
        and bool(values["inward"] > 0)
        and bool(values["dp"] < 0)
    )
    uniform = (
        integer_signs[0]
        if dt_sign != 0 and integer_signs[0] != 0
        and all(value == integer_signs[0] for value in integer_signs)
        else 0
    )
    outgoing = None
    if uniform:
        outgoing = (
            ("W" if uniform > 0 else "N") if seam_id == "NW"
            else ("W" if uniform < 0 else "S")
        )
    return {
        "seam_id": seam_id,
        "adjacent_chart": data["adjacent"],
        "normal_sign": sign_name(data["normal"](nx, ny)),
        "other_margin_sign": sign_name(data["other"](nx, ny)),
        "H_whole_box_sign": sign_name(values["H"]),
        "forward_sign": sign_name(values["forward"]),
        "inward_sign": sign_name(values["inward"]),
        "dH_dt_sign": sign_name(values["dt"]),
        "dH_dp_sign": sign_name(values["dp"]),
        "p_lower_face_H_sign": sign_name(lower),
        "p_upper_face_H_sign": sign_name(upper),
        "corner_H_signs": corners,
        "typed_preconditions": typed,
        "full_graph": bool(lower > 0) and bool(upper < 0),
        "clipped_graph": (
            dt_sign != 0 and 1 in integer_signs and -1 in integer_signs
        ),
        "uniform_outgoing_chart": outgoing,
    }


def independent_typed_strata(
    detail: dict[str, Any], terminal_id: str
) -> dict[str, Any]:
    seam_id = detail["seam_id"]
    adjacent = detail["adjacent_chart"]
    corners = detail["corner_H_signs"]
    chart_for = (
        {"STRICT_POSITIVE": "W", "STRICT_NEGATIVE": "N"}
        if seam_id == "NW"
        else {"STRICT_NEGATIVE": "W", "STRICT_POSITIVE": "S"}
    )
    sides = [
        sealed({
            "schema": "cm2.round306c30b.H-open-side.row.v1",
            "terminal_id": terminal_id,
            "predicate": predicate,
            "ambient_dimension": 3,
            "outgoing_chart": chart_for[sign],
            "disposition": "LIVE" if chart_for[sign] == "W" else "EXCLUDED",
            "nonempty_positive_measure": True,
            "H_continuity_and_strict_side_sign_proved": True,
            "dyadic_leaf_owner": terminal_id,
        })
        for sign, predicate in (
            ("STRICT_NEGATIVE", "H<0"),
            ("STRICT_POSITIVE", "H>0"),
        )
    ]
    crosses = lambda first, second: {first, second} == {
        "STRICT_NEGATIVE", "STRICT_POSITIVE"
    }
    t_cross = {
        side: crosses(corners[f"t{index}_p0"], corners[f"t{index}_p1"])
        for index, side in enumerate(("LOWER", "UPPER"))
    }
    p_cross = {
        side: detail["dH_dt_sign"] != "OVERWRAP"
        and crosses(corners[f"t0_p{index}"], corners[f"t1_p{index}"])
        for index, side in enumerate(("LOWER", "UPPER"))
    }
    specs = [
        ("t", "LOWER", t_cross["LOWER"], "STRICT_dH_dp_UNIQUE_POINT_X_s"),
        ("t", "UPPER", t_cross["UPPER"], "STRICT_dH_dp_UNIQUE_POINT_X_s"),
        ("p", "LOWER", p_cross["LOWER"], "STRICT_dH_dt_UNIQUE_POINT_X_s"),
        ("p", "UPPER", p_cross["UPPER"], "STRICT_dH_dt_UNIQUE_POINT_X_s"),
        ("s", "LOWER", True, "H_GRAPH_CURVE_AT_FIXED_s"),
        ("s", "UPPER", True, "H_GRAPH_CURVE_AT_FIXED_s"),
    ]
    faces = [
        sealed({
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
            "dyadic_leaf_owner": terminal_id if nonempty else "NONE",
            "shadow_chart": adjacent if nonempty else "NONE",
            "disposition": "LIVE" if nonempty else "EMPTY",
            "ambient_dyadic_owner_rule": (
                "LOWER_CHILD_OWNS_SPLIT_EQUALITY__LEXICOGRAPHIC_RECURSION"
            ),
        })
        for axis, side, nonempty, proof in specs
    ]
    edges: list[dict[str, Any]] = []
    for t_side in ("LOWER", "UPPER"):
        for s_side in ("LOWER", "UPPER"):
            nonempty = t_cross[t_side]
            edges.append(sealed({
                "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
                "terminal_id": terminal_id,
                "fixed": {"t": t_side, "s": s_side},
                "free_axis": "p", "predicate": "H=0",
                "nonempty": nonempty, "dimension_if_nonempty": 0,
                "proof": "STRICT_dH_dp_UNIQUE_POINT",
                "half_open_outgoing_owner_chart": "W" if nonempty else "NONE",
                "chart_level_half_open_owner": "W" if nonempty else "NONE",
                "dyadic_leaf_owner": terminal_id if nonempty else "NONE",
                "disposition": "LIVE" if nonempty else "EMPTY",
            }))
    for p_side in ("LOWER", "UPPER"):
        for s_side in ("LOWER", "UPPER"):
            nonempty = p_cross[p_side]
            edges.append(sealed({
                "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
                "terminal_id": terminal_id,
                "fixed": {"p": p_side, "s": s_side},
                "free_axis": "t", "predicate": "H=0",
                "nonempty": nonempty, "dimension_if_nonempty": 0,
                "proof": "STRICT_dH_dt_UNIQUE_POINT",
                "half_open_outgoing_owner_chart": "W" if nonempty else "NONE",
                "chart_level_half_open_owner": "W" if nonempty else "NONE",
                "dyadic_leaf_owner": terminal_id if nonempty else "NONE",
                "disposition": "LIVE" if nonempty else "EMPTY",
            }))
    for ti, t_side in enumerate(("LOWER", "UPPER")):
        for pi, p_side in enumerate(("LOWER", "UPPER")):
            edges.append(sealed({
                "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
                "terminal_id": terminal_id,
                "fixed": {"t": t_side, "p": p_side},
                "free_axis": "s", "predicate": "H=0",
                "nonempty": False, "dimension_if_nonempty": 0,
                "proof": "STRICT_NONZERO_H_AT_t_p_CORNER",
                "H_sign": corners[f"t{ti}_p{pi}"],
                "half_open_outgoing_owner_chart": "NONE",
                "chart_level_half_open_owner": "NONE",
                "dyadic_leaf_owner": "NONE_EMPTY_STRATUM",
                "disposition": "EMPTY",
            }))
    corners_rows = [
        sealed({
            "schema": "cm2.round306c30b.H-sheet-corner-incidence.row.v1",
            "terminal_id": terminal_id,
            "corner": {"t": t_side, "p": p_side, "s": s_side},
            "predicate": "H=0", "nonempty": False,
            "dimension_if_nonempty": 0,
            "proof": "STRICT_NONZERO_H_AT_t_p_CORNER",
            "H_sign": corners[f"t{ti}_p{pi}"], "disposition": "EMPTY",
            "chart_level_half_open_owner": "NONE",
            "dyadic_leaf_owner": "NONE_EMPTY_STRATUM",
        })
        for ti, t_side in enumerate(("LOWER", "UPPER"))
        for pi, p_side in enumerate(("LOWER", "UPPER"))
        for s_side in ("LOWER", "UPPER")
    ]
    sheet = sealed({
        "schema": "cm2.round306c30b.H-zero-sheet.row.v1",
        "terminal_id": terminal_id,
        "predicate": "H=ux*dy-uy*dx=0", "seam_id": seam_id,
        "ambient_dimension": 2, "nonempty": True,
        "unique_graph_in_p_by_strict_dH_dp": True,
        "half_open_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "half_open_owner_chart": "W", "shadow_chart": adjacent,
        "chart_level_half_open_owner": "W",
        "dyadic_leaf_owner": terminal_id,
        "disposition": "LIVE",
        "face_incidence_row_count": len(faces),
        "face_incidence_rows_sha256": digest(faces),
        "edge_incidence_row_count": len(edges),
        "edge_incidence_rows_sha256": digest(edges),
        "corner_incidence_row_count": len(corners_rows),
        "corner_incidence_rows_sha256": digest(corners_rows),
    })
    return {
        "open_3D_sides": sides, "H_zero_2D_sheet": sheet,
        "H_zero_1D_face_incidences": faces,
        "H_zero_0D_edge_incidences": edges,
        "H_zero_0D_corner_absence_rows": corners_rows,
    }


def crossing(first: str, second: str) -> bool:
    return {first, second} == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


def independent_complete_typed_strata(
    chart_id: str,
    box: Any,
    detail: dict[str, Any],
    terminal_id: str,
) -> dict[str, Any]:
    seam_id = detail["seam_id"]
    adjacent = detail["adjacent_chart"]
    corners = detail["corner_H_signs"]
    require(
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
        sealed({
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
        sealed({
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
        require(
            present_signs <= {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and bool(present_signs),
            "typed face strict sign partition",
        )
        require(crosses_face or len(present_signs) == 1,
             "typed face uniform noncrossing sign")
        for sign in ("STRICT_NEGATIVE", "STRICT_POSITIVE"):
            nonempty = sign in present_signs
            outgoing_chart = sign_chart[sign] if nonempty else "NONE"
            face_region_rows.append(sealed({
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
            edge_rows.append(sealed({
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
            edge_rows.append(sealed({
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
            require(corners[f"t{ti}_p{pi}"] != "OVERWRAP",
                 "typed sheet corner strict")
            edge_rows.append(sealed({
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
        require(
            present_signs <= {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and bool(present_signs),
            "typed edge strict sign partition",
        )
        require(crosses_edge or len(present_signs) == 1,
             "typed edge uniform noncrossing sign")
        zero_row = next(
            row for row in edge_rows
            if row["fixed"] == fixed and row["free_axis"] == free_axis
        )
        for sign in ("STRICT_NEGATIVE", "STRICT_POSITIVE"):
            nonempty = sign in present_signs
            outgoing_chart = sign_chart[sign] if nonempty else "NONE"
            edge_region_rows.append(sealed({
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
        sealed({
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
    sheet = sealed({
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



def independent_terminal(chart_id: str, box: Any) -> tuple[str | None, dict[str, Any]]:
    cell, nx, ny = r176.tight_contact(chart_id, box)
    if cell is not None:
        margins = {
            "E.first": nx - ny, "E.second": nx + ny,
            "W.first": -nx - ny, "W.second": -nx + ny,
            "N.first": ny - nx, "N.second": ny + nx,
            "S.first": -ny - nx, "S.second": -ny + nx,
        }
        classification = (
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE" if cell == "W"
            else "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE"
        )
        return classification, {
            "method": "STRICT_OUTGOING_NORMAL_RECTANGLE",
            "outgoing_chart": cell,
            "outgoing_margin_signs": {
                key: sign_name(value) for key, value in sorted(margins.items())
            },
        }
    candidates = [
        independent_seam_evidence(chart_id, box, seam_id)
        for seam_id in sorted(r176.SEAMS)
    ]
    separated = [
        value for value in candidates
        if value["typed_preconditions"]
        and value["uniform_outgoing_chart"] is not None
    ]
    typed = [
        value for value in candidates
        if value["typed_preconditions"]
        and (value["full_graph"] or value["clipped_graph"])
    ]
    if len(separated) == 1 and not typed:
        chosen = separated[0]
        return (
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            if chosen["uniform_outgoing_chart"] == "W"
            else "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE"
        ), {
            "method": "MONOTONE_H_STRICT_SIGN_RECTANGLE",
            "seam_evidence": chosen,
            "outgoing_chart": chosen["uniform_outgoing_chart"],
        }
    if len(typed) == 1 and not separated:
        return H_TYPED, {
            "method": "TYPED_H_GRAPH_AND_TWO_OPEN_SIDES",
            "seam_evidence": typed[0],
        }
    return None, {"method": "UNRESOLVED_H_INTERVAL", "candidates": candidates}


def independent_internal_lower_strata(
    faces: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    edge_groups: dict[bytes, dict[str, Any]] = {}
    corner_groups: dict[bytes, dict[str, Any]] = {}
    axes = ("t", "p", "s")
    for face in faces:
        face_axis = face["axis"]
        span_axes = [axis for axis in axes if axis != face_axis]
        require(set(span_axes) == set(face["spans"]), "independent split spans")
        for fixed_axis, free_axis in (
            (span_axes[0], span_axes[1]),
            (span_axes[1], span_axes[0]),
        ):
            for endpoint, coordinate in zip(
                ("LOWER", "UPPER"), face["spans"][fixed_axis]
            ):
                geometry = {
                    "fixed_coordinates": {
                        face_axis: face["coordinate"], fixed_axis: coordinate,
                    },
                    "free_axis": free_axis,
                    "free_span": face["spans"][free_axis],
                }
                group = edge_groups.setdefault(wire(geometry), {
                    "geometry": geometry, "owners": [], "nonowners": [],
                    "faces": [],
                    "orientations": [],
                })
                group["owners"].append(face["lower_child_owner"])
                group["nonowners"].append(face["upper_child_nonowner"])
                group["faces"].append(face["face_sha256"])
                group["orientations"].append({
                    "incident_split_face_sha256": face["face_sha256"],
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
                group = corner_groups.setdefault(wire(geometry), {
                    "geometry": geometry, "owners": [], "nonowners": [],
                    "faces": [],
                    "orientations": [],
                })
                group["owners"].append(face["lower_child_owner"])
                group["nonowners"].append(face["upper_child_nonowner"])
                group["faces"].append(face["face_sha256"])
                group["orientations"].append({
                    "incident_split_face_sha256": face["face_sha256"],
                    "split_face_axis": face_axis,
                    "boundary_endpoints": {
                        span_axes[0]: first_endpoint,
                        span_axes[1]: second_endpoint,
                    },
                    "lower_child_owner": face["lower_child_owner"],
                    "upper_child_nonowner": face["upper_child_nonowner"],
                })
    edges = [sealed({
        "schema": "cm2.round306c30b.internal-split-face-edge-owner.row.v1",
        **group["geometry"], "ambient_dimension": 1,
        "half_open_owner_prefix": min(group["owners"]),
        "incident_lower_child_owners": sorted(set(group["owners"])),
        "incident_upper_child_nonowners": sorted(set(group["nonowners"])),
        "incident_split_face_sha256": sorted(set(group["faces"])),
        "incident_split_face_count": len(set(group["faces"])),
        "incident_orientations": sorted(group["orientations"], key=wire),
        "incident_orientations_sha256": digest(sorted(
            group["orientations"], key=wire
        )),
        "half_open_rule": (
            "LOWER_CHILD_OWNS_SPLIT_EQUALITY__"
            "LEXICOGRAPHIC_LEAST_INCIDENT_LOWER_CHILD"
        ),
    }) for _key, group in sorted(edge_groups.items())]
    corners = [sealed({
        "schema": "cm2.round306c30b.internal-split-face-corner-owner.row.v1",
        **group["geometry"], "ambient_dimension": 0,
        "half_open_owner_prefix": min(group["owners"]),
        "incident_lower_child_owners": sorted(set(group["owners"])),
        "incident_upper_child_nonowners": sorted(set(group["nonowners"])),
        "incident_split_face_sha256": sorted(set(group["faces"])),
        "incident_split_face_count": len(set(group["faces"])),
        "incident_orientations": sorted(group["orientations"], key=wire),
        "incident_orientations_sha256": digest(sorted(
            group["orientations"], key=wire
        )),
        "half_open_rule": (
            "LOWER_CHILD_OWNS_SPLIT_EQUALITY__"
            "LEXICOGRAPHIC_LEAST_INCIDENT_LOWER_CHILD"
        ),
    }) for _key, group in sorted(corner_groups.items())]
    edges.sort(key=wire)
    corners.sort(key=wire)
    require(
        len(edges) <= 4 * len(faces) and len(corners) <= 4 * len(faces),
        "deduplicated internal split 1D/0D strata",
    )
    return edges, corners


def independent_analytic_semantic_core(value: Any) -> Any:
    """Drop schemas, hashes, and aggregate counts from analytic evidence."""
    if type(value) is dict:
        return {
            key: independent_analytic_semantic_core(item)
            for key, item in sorted(value.items())
            if key != "schema"
            and key != "row_sha256"
            and not key.endswith("_sha256")
            and not key.endswith("_row_count")
        }
    if type(value) is list:
        return [independent_analytic_semantic_core(item) for item in value]
    return value


def independent_complete_partition(row: Any) -> dict[str, Any]:
    pending = [(row.box, 0)]
    terminals: list[dict[str, Any]] = []
    terminal_boxes: dict[str, Any] = {}
    split_faces: list[dict[str, Any]] = []
    while pending:
        box, depth = pending.pop()
        classification, evidence = independent_terminal(row.chart_id, box)
        if classification is not None:
            terminal_id = f"{row.chart_id}:{box.path}"
            coarse = (
                "EXCLUDED" if classification in H_EXCLUSION_CLASSES
                else "LIVE" if classification in H_LIVE_CLASSES else "MIXED"
            )
            body = {
                "schema": "cm2.round306c30b.H-terminal-rectangle.row.v1",
                "terminal_id": terminal_id, "relative_depth": depth,
                "closed_box": r176.box_row(box),
                "exact_volume": str(r215.box_volume(box)),
                "classification": classification,
                "coarse_disposition": coarse,
                "analytic_evidence": evidence,
            }
            if classification == H_TYPED:
                body["typed_strata"] = independent_complete_typed_strata(
                    row.chart_id, box, evidence["seam_evidence"], terminal_id
                )
            require(terminal_id not in terminal_boxes,
                    "unique independent H terminal:" + terminal_id)
            terminal_boxes[terminal_id] = box
            terminals.append(sealed(body))
            continue
        require(depth < 4, "independent H depth exhaustion:" + row.key)
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
    census = Counter(value["coarse_disposition"] for value in terminals)
    whole = (
        "EXCLUDED" if set(census) == {"EXCLUDED"}
        else "LIVE" if set(census) == {"LIVE"} else "MIXED"
    )
    coverage = sum(Q(1, 2 ** value["relative_depth"]) for value in terminals)
    volume = sum(Q(value["exact_volume"]) for value in terminals)
    require(
        coverage == 1 and volume == r215.box_volume(row.box),
        "independent H coverage/volume:" + row.key,
    )
    split_edges, split_corners = independent_internal_lower_strata(split_faces)
    analytic_terminal_projection = [
        {
            "terminal_id": terminal["terminal_id"],
            "relative_depth": terminal["relative_depth"],
            "closed_box": terminal["closed_box"],
            "exact_volume": terminal["exact_volume"],
            "classification": terminal["classification"],
            "coarse_disposition": terminal["coarse_disposition"],
            "analytic_evidence": independent_analytic_semantic_core(
                terminal["analytic_evidence"]
            ),
            **({
                "typed_strata_semantic_core": (
                    independent_analytic_semantic_core(
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
        "terminal_rectangle_disposition_census": dict(sorted(census.items())),
        "terminal_semantic_rows": analytic_terminal_projection,
        "split_face_geometry_and_child_rows": [
            {
                key: face[key]
                for key in (
                    "parent_cell_key", "axis", "coordinate", "spans",
                    "dimension", "lower_child_owner", "upper_child_nonowner",
                    "both_closed_interval_enclosures_include_face",
                )
            }
            for face in split_faces
        ],
        "relative_3D_coverage": "1",
        "exact_volume": str(volume),
    }
    terminal_by_id = {
        value["terminal_id"]: value for value in terminals
    }
    require(
        set(terminal_boxes) == set(terminal_by_id),
        "independent H terminal box binding:" + row.key,
    )
    terminal_reclosure = _independent_atomic_owner_reclosure(
        row.key,
        row.box,
        terminal_boxes,
        {
            terminal_id: (
                "ROUND306C30B_H_TERMINAL_ROW:"
                + terminal_by_id[terminal_id]["row_sha256"]
            )
            for terminal_id in terminal_boxes
        },
        {
            terminal_id: terminal_by_id[terminal_id]["coarse_disposition"]
            for terminal_id in terminal_boxes
        },
        [],
        split_faces,
        audit_scope="PER_H_CELL_TERMINAL_SUBDIVISION",
        leaf_key_kind="H_TERMINAL_ID",
    )
    terminal_atomic_audit = terminal_reclosure["candidate_audit"]
    exact_atomic_closure = (
        terminal_atomic_audit["exact_3D_enclosure"][
            "all_leaf_boxes_contained_in_parent_and_nondegenerate"
        ] is True
        and terminal_atomic_audit["exact_3D_enclosure"][
            "pairwise_leaf_interiors_disjoint"
        ] is True
        and terminal_atomic_audit["exact_3D_enclosure"][
            "leaf_exact_volume_sum_equals_parent"
        ] is True
        and terminal_atomic_audit["all_raw_2D_strata_exactly_reclosed"]
        is True
        and terminal_atomic_audit["all_raw_1D_strata_exactly_reclosed"]
        is True
        and terminal_atomic_audit["closed_3D_leaf_count"] == len(terminals)
        and terminal_atomic_audit["atomic_2D_owner_row_count"] > 0
        and terminal_atomic_audit["atomic_1D_owner_row_count"] > 0
        and terminal_atomic_audit["atomic_0D_owner_row_count"] > 0
    )
    require(exact_atomic_closure,
            "independent H exact atomic closure:" + row.key)
    partition_body = {
        "whole_cell_disposition": whole,
        "terminal_rectangle_count": len(terminals),
        "terminal_rectangle_disposition_census": dict(sorted(census.items())),
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
        "typed_H_zero_2D_sheet_count": sum(
            value["classification"] == H_TYPED for value in terminals
        ),
        "relative_3D_coverage": "1",
        "exact_volume": str(volume),
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


def independent_r215_evidence(row: Any, reduction: dict[str, Any]) -> dict[str, Any]:
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
        and evidence["method"] == "MONOTONE_P_SAME_SIGN_DELTA_STRICT_EXCLUSION"
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


def reconstruct_h_sources(
    evidence_rows: list[dict[str, Any]],
    replay: dict[str, Any],
    residual_frontiers: dict[str, Any],
    closure_results: dict[str, tuple[str | None, dict[str, Any]]],
) -> tuple[list[tuple[str, Any, dict[str, Any]]], dict[str, dict[str, Any]]]:
    """Reconstruct 560 R215 + 128 inherited follow-up H cells outcome-blind.

    Eight inherited cells first prove an empty same-sign Delta graph and then
    explicitly request ``FOLLOWUP_H_PARTITION``.  Their distinct provenance
    is verified before H materialization; they are never mislabeled as direct
    outgoing-H terminals.
    """
    by_origin = Counter()
    sources: list[tuple[str, Any, dict[str, Any]]] = []
    for evidence in evidence_rows:
        if evidence["origin_key"] not in set(EXPECTED_R215_H_KEYS):
            continue
        # A Round215 row can retain its pre-closure blocker label even when
        # the later analytic pass closes the cell.  Such a row is exclusion
        # evidence, not an outgoing-H source.  Mirror the producer's
        # outcome-blind selection rule and admit only the final blocked rows.
        if evidence["analytic_closed"] is not False:
            continue
        if evidence["blocker"] != "NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST":
            continue
        row = residual_frontiers[evidence["cell_key"]]
        require(
            row.key == evidence["cell_key"]
            and row.origin_key == evidence["origin_key"]
            and row.chart_id == evidence["source_chart_id"]
            and list(row.active_targets) == evidence["active_targets"]
            and row.failure == evidence["original_failure_type"],
            "captured Round215 frontier identity:" + row.key,
        )
        reduction = r215.exact_behind_reduce(row, r180.residual_category(row))
        rebuilt_evidence = independent_r215_evidence(row, reduction)
        require(
            reduction["closed"] is False
            and reduction["category"] == evidence["original_residual_category"]
            and reduction["residual_reason"]
            == evidence["exact_behind_residual_reason"]
            and rebuilt_evidence == evidence,
            "R215 H source identity:" + row.key,
        )
        by_origin[row.origin_key] += 1
        sources.append((
            "ROUND215_RESIDUAL_OUTGOING_H",
            row,
            {
                "Round215_cell_row_sha256": rebuilt_evidence["row_sha256"],
                "Round215_blocker": rebuilt_evidence["blocker"],
                "Round215_reduction_sha256": digest({
                    key: reduction[key] for key in (
                        "category", "residual_reason", "closed", "disposition",
                        "eligible_targets", "candidate_evidence",
                    )
                }),
            },
        ))
    require(
        len(sources) == 560 and dict(sorted(by_origin.items()))
        == EXPECTED_R215_PER_ORIGIN,
        "exact 560 R215 H cells",
    )

    origin_context: dict[str, dict[str, Any]] = {}
    held_rows = canonical_rows(C30A_SEALED / C30A_HELD)
    held_by_origin = {row["origin_key"]: row for row in held_rows}
    require(
        tuple(sorted(held_by_origin)) == EXPECTED_HELD_KEYS and len(held_rows) == 2,
        "sealed held origin identities",
    )
    for origin in EXPECTED_KEYS:
        roots: list[Any] = []
        preclosed: list[Any] = []
        preclosed_kinds: Counter[str] = Counter()
        preclosed_closure_evidence: dict[str, dict[str, Any]] = {}
        for row in replay["frontier"]:
            if row.origin_key != origin:
                continue
            require(
                row.key in closure_results,
                "captured Round176 closure presence:" + row.key,
            )
            kind, proof = closure_results[row.key]
            if kind is None:
                roots.append(row)
            else:
                preclosed.append(row)
                preclosed_kinds[kind] += 1
                preclosed_closure_evidence[row.key] = proof
        require(
            roots
            and set(preclosed_kinds) <= {"EXCLUDED"}
            and set(preclosed_closure_evidence)
            == {row.key for row in preclosed}
            and all(
                type(value) is dict
                for value in preclosed_closure_evidence.values()
            ),
            "Round176 residual roots/preclosed exclusions:" + origin,
        )
        refinement = r180.refine_origin(roots, 4)
        leaves = r215.reconstruct_refinement_leaf_frontiers(roots, refinement)
        terminal_frontiers = leaves["terminal"]
        nonexcluded = sorted(
            (
                item for item in refinement["terminal_rows"]
                if item["coarse_disposition"] != "EXCLUDED"
            ),
            key=lambda item: item["cell_key"],
        )
        inherited_h = [
            item for item in nonexcluded
            if item["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE"
        ]
        inherited_delta_mixed = [
            item for item in nonexcluded
            if item["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
        ]
        require(
            len(inherited_h) + len(inherited_delta_mixed) == len(nonexcluded)
            and all(item["coarse_disposition"] == "MIXED"
                    for item in inherited_delta_mixed),
            "inherited nonexcluded H/Delta partition:" + origin,
        )
        for item in nonexcluded:
            require(item["cell_key"] in terminal_frontiers,
                    "inherited H source:" + item["cell_key"])
            row = terminal_frontiers[item["cell_key"]]
            source_binding = {
                "Round180_terminal_evidence": item,
                "Round180_terminal_sha256": item["terminal_sha256"],
            }
            if item["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX":
                require(
                    origin.endswith("07.01.11011100")
                    and item["coarse_disposition"] == "MIXED"
                    and item["Delta_zero_graph_inside_closed_box"] is False
                    and item["empty_2D_graph_edge_and_corner_ledger"] is True
                    and item["witness"] == "FOLLOWUP_H_PARTITION",
                    "same-sign Delta empty-graph followup H:" + item["cell_key"],
                )
                source_kind = "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
                source_binding["Round180_same_sign_Delta_followup"] = {
                    "method": item["method"], "target": item["target"],
                    "derivative_sign": item["derivative_sign"],
                    "strict_common_face_sign": item["strict_common_face_sign"],
                    "Delta_p_lower_face_sign": item[
                        "strict_common_face_sign"
                    ],
                    "Delta_p_upper_face_sign": item[
                        "strict_common_face_sign"
                    ],
                    "Delta_zero_graph_inside_closed_box": False,
                    "empty_2D_graph_edge_and_corner_ledger": True,
                    "witness": item["witness"],
                }
            elif origin in held_by_origin:
                source_kind = "ROUND306C30A_HELD_INHERITED_OUTGOING_H"
                source_binding["C30a_held_row_sha256"] = held_by_origin[
                    origin
                ]["row_sha256"]
            else:
                source_kind = "ROUND180_INHERITED_OUTGOING_H"
            sources.append((source_kind, row, source_binding))
        if origin in held_by_origin:
            sealed = held_by_origin[origin]
            require(
                nonexcluded == sealed["Round180_nonexcluded_terminal_rows"]
                and digest(nonexcluded)
                == sealed["Round180_nonexcluded_terminal_rows_sha256"]
                and len(nonexcluded) == 4,
                "independent C30a held reconstruction:" + origin,
            )
        origin_context[origin] = {
            "source_chart_id": replay["origins"][origin]["chart_id"],
            "source_box": replay["origins"][origin]["box"],
            "Round176_prior_rows": replay["prior"][origin],
            "Round176_prior_closed_count": len(replay["prior"][origin]),
            "Round176_residual_root_count": len(roots),
            "Round176_preclosed_count": len(preclosed),
            "Round176_preclosed_kind_census": dict(sorted(preclosed_kinds.items())),
            "Round180_terminal_count": len(refinement["terminal_rows"]),
            "Round180_inherited_direct_H_count": len(inherited_h),
            "Round180_inherited_same_sign_Delta_followup_H_count": len(
                inherited_delta_mixed
            ),
            "Round180_inherited_H_materialized_count": len(nonexcluded),
            "Round180_inherited_same_sign_Delta_followup_H_rows": (
                inherited_delta_mixed
            ),
            "Round180_final_residual_count": len(refinement["final_residual_rows"]),
            "refinement": refinement,
            "roots": roots,
            "preclosed_rows": preclosed,
            "preclosed_closure_evidence": preclosed_closure_evidence,
        }
    sources.sort(key=lambda item: item[1].key)
    keys = [item[1].key for item in sources]
    require(
        len(sources) == 688 and len(set(keys)) == 688
        and sum(
            item[0] in {
                "ROUND180_INHERITED_OUTGOING_H",
                "ROUND306C30A_HELD_INHERITED_OUTGOING_H",
                "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H",
            }
            for item in sources
        ) == 128
        and sum(value["Round180_inherited_same_sign_Delta_followup_H_count"]
                for value in origin_context.values()) == 8,
        "complete 688 H including 8 Delta-empty-graph followup sources",
    )
    return sources, origin_context


def validate_nested_row(value: dict[str, Any], schema: str, label: str) -> None:
    require(value.get("schema") == schema, "nested schema:" + label)
    body = dict(value)
    claimed = body.pop("row_sha256", None)
    require(type(claimed) is str and claimed == digest(body), "nested hash:" + label)


def validate_typed_boundary_exhaustion(terminal: dict[str, Any]) -> None:
    detail = terminal["analytic_evidence"]["seam_evidence"]
    corners = detail["corner_H_signs"]
    require(
        set(corners.values()) == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
        "typed terminal has both strict sign complements",
    )
    strata = terminal["typed_strata"]
    for row in strata["H_zero_1D_face_incidences"]:
        if row["nonempty"]:
            require(
                row["chart_level_half_open_owner"] == "W"
                and row["closed_enclosure_terminal_id"] == terminal["terminal_id"]
                and row["disposition"] == "LIVE",
                "typed face chart/dyadic owner",
            )
        else:
            require(
                row["chart_level_half_open_owner"] == "NONE"
                and row["closed_enclosure_terminal_id"] == terminal["terminal_id"]
                and row["disposition"] == "EMPTY",
                "typed empty face",
            )
        # A nonempty H=0 curve plus its H<0/H>0 2D complements, or one
        # uniform strict-sign 2D face, exhausts each of the six box faces.
        require(
            row["fixed_axis"] == "s" or row["proof"].startswith("STRICT_dH_"),
            "typed face complement proof",
        )
    for row in strata["H_zero_0D_edge_incidences"]:
        if row["nonempty"]:
            require(
                row["chart_level_half_open_owner"] == "W"
                and row["closed_enclosure_terminal_id"] == terminal["terminal_id"]
                and row["disposition"] == "LIVE",
                "typed edge chart/dyadic owner",
            )
        else:
            require(
                row["chart_level_half_open_owner"] == "NONE"
                and row["closed_enclosure_terminal_id"] == terminal["terminal_id"]
                and row["disposition"] == "EMPTY",
                "typed empty edge",
            )
        # Strict one-variable monotonicity gives at most one H=0 point;
        # its two sign-open 1D complements (when present) are exhaustive.
        require(
            row["proof"] in {
                "STRICT_dH_dp_UNIQUE_POINT", "STRICT_dH_dt_UNIQUE_POINT",
                "STRICT_NONZERO_H_AT_t_p_CORNER",
            },
            "typed edge complement proof",
        )
    for row in strata["H_zero_0D_corner_absence_rows"]:
        require(
            row["H_sign"] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and row["nonempty"] is False
            and row["chart_level_half_open_owner"] == "NONE"
            and row["strict_corner_closed_enclosure_terminal_id"]
            == terminal["terminal_id"]
            and row["strict_corner_outgoing_chart"] in {"W", "N", "S"}
            and row["strict_corner_disposition"] in {"LIVE", "EXCLUDED"},
            "typed strict 0D corner exhaustion",
        )
    face_regions = strata["terminal_face_2D_H_sign_regions"]
    edge_regions = strata["terminal_edge_1D_H_sign_intervals"]
    require(
        len(face_regions) == 12 and len(edge_regions) == 24
        and all(row["dimension_if_nonempty"] == 2 for row in face_regions)
        and all(row["dimension_if_nonempty"] == 1 for row in edge_regions)
        and all(row["closed_enclosure_terminal_id"] == terminal["terminal_id"]
                for row in face_regions + edge_regions)
        and all(row["disposition"] in {"LIVE", "EXCLUDED", "EMPTY"}
                for row in face_regions + edge_regions),
        "typed face/edge strict sign complements exhaustive",
    )


def validate_disposition_aware_split_owners(partition: dict[str, Any]) -> None:
    terminals = partition["terminal_rectangles"]
    by_id = {row["terminal_id"]: row["coarse_disposition"] for row in terminals}
    require(len(by_id) == len(terminals), "unique H terminal ids")
    face_hashes = {
        face["face_sha256"]: face
        for face in partition["internal_split_2D_face_rows"]
    }
    require(
        len(face_hashes) == partition["internal_split_2D_face_row_count"],
        "unique internal split faces",
    )
    for face in face_hashes.values():
        owner_prefix = face["lower_child_owner"]
        nonowner_prefix = face["upper_child_nonowner"]
        owner_dispositions = Counter(
            disposition for key, disposition in by_id.items()
            if key.startswith(owner_prefix)
        )
        nonowner_dispositions = Counter(
            disposition for key, disposition in by_id.items()
            if key.startswith(nonowner_prefix)
        )
        require(
            bool(owner_dispositions) and bool(nonowner_dispositions)
            and set(owner_dispositions) <= {"EXCLUDED", "LIVE", "MIXED"}
            and set(nonowner_dispositions) <= {"EXCLUDED", "LIVE", "MIXED"},
            "disposition-aware split owner subtrees",
        )
    for row in partition["internal_split_1D_edge_owner_rows"]:
        validate_nested_row(
            row, "cm2.round306c30b.internal-split-face-edge-owner.row.v1",
            "internal split edge",
        )
        require(
            row["half_open_owner_prefix"]
            == min(row["incident_lower_child_owners"])
            and row["incident_split_face_count"]
            == len(row["incident_split_face_sha256"])
            and all(value in face_hashes for value in row[
                "incident_split_face_sha256"
            ]),
            "deduplicated internal split edge owner",
        )
    for row in partition["internal_split_0D_corner_owner_rows"]:
        validate_nested_row(
            row, "cm2.round306c30b.internal-split-face-corner-owner.row.v1",
            "internal split corner",
        )
        require(
            row["half_open_owner_prefix"]
            == min(row["incident_lower_child_owners"])
            and row["incident_split_face_count"]
            == len(row["incident_split_face_sha256"])
            and all(value in face_hashes for value in row[
                "incident_split_face_sha256"
            ]),
            "deduplicated internal split corner owner",
        )


def validate_candidate_h_row(
    candidate: dict[str, Any],
    source_kind: str,
    source: Any,
    source_binding: dict[str, Any],
) -> str:
    require(
        candidate["schema"]
        == "cm2.round306c30b.source-w-outgoing-h.h-cell.row.v1"
        and candidate["source_kind"] == source_kind
        and candidate["origin_key"] == source.origin_key
        and candidate["cell_key"] == source.key
        and candidate["source_chart_id"] == source.chart_id
        and candidate["closed_box"] == r176.box_row(source.box)
        and Q(candidate["exact_volume"]) == r215.box_volume(source.box)
        and candidate["unique_first_owner"] == r176.FROZEN_OWNER
        and candidate["frozen_outgoing_chart"] == r176.FROZEN_CHART
        and candidate["source_binding"] == source_binding
        and candidate["half_open_owner_rule"]
        == "E_OR_W_OWNS__N_OR_S_SHADOWS"
        and candidate["whole_origin_exclusion_credit"] == 0,
        "H candidate source binding:" + source.key,
    )
    complete_independent = independent_complete_partition(source)
    coarse = complete_independent["whole_cell_disposition"]
    independent_terminals = complete_independent["terminal_rectangles"]
    ownership = {
        "internal_split_2D_face_count": complete_independent[
            "internal_split_2D_face_row_count"
        ],
    }
    partition = candidate["H_partition"]
    terminals = partition["terminal_rectangles"]
    typed_expected = [
        value for value in complete_independent["terminal_rectangles"]
        if value["coarse_disposition"] == "MIXED"
    ]
    typed_sheets_expected = [
        value["typed_strata"]["H_zero_2D_sheet"] for value in typed_expected
    ]
    face_regions_expected = [
        row for value in typed_expected
        for row in value["typed_strata"]["terminal_face_2D_H_sign_regions"]
    ]
    faces_expected = [
        row for value in typed_expected
        for row in value["typed_strata"]["H_zero_1D_face_incidences"]
    ]
    edge_regions_expected = [
        row for value in typed_expected
        for row in value["typed_strata"]["terminal_edge_1D_H_sign_intervals"]
    ]
    edges_expected = [
        row for value in typed_expected
        for row in value["typed_strata"]["H_zero_0D_edge_incidences"]
    ]
    corners_expected = [
        row for value in typed_expected
        for row in value["typed_strata"]["H_zero_0D_corner_absence_rows"]
    ]
    expected_body = {
        "schema": "cm2.round306c30b.source-w-outgoing-h.h-cell.row.v1",
        "source_kind": source_kind, "origin_key": source.origin_key,
        "cell_key": source.key, "source_chart_id": source.chart_id,
        "closed_box": r176.box_row(source.box),
        "exact_volume": str(r215.box_volume(source.box)),
        "unique_first_owner": r176.FROZEN_OWNER,
        "frozen_outgoing_chart": r176.FROZEN_CHART,
        "source_binding": source_binding, "H_partition": complete_independent,
        "whole_H_cell_disposition": complete_independent[
            "whole_cell_disposition"
        ],
        "typed_H_zero_2D_sheet_count": len(typed_expected),
        "typed_H_zero_2D_sheet_rows_sha256": digest(typed_sheets_expected),
        "terminal_face_2D_H_sign_region_row_count": len(face_regions_expected),
        "terminal_face_2D_H_sign_region_rows_sha256": digest(
            face_regions_expected
        ),
        "H_zero_1D_face_incidence_row_count": len(faces_expected),
        "H_zero_1D_face_incidence_rows_sha256": digest(faces_expected),
        "terminal_edge_1D_H_sign_interval_row_count": len(
            edge_regions_expected
        ),
        "terminal_edge_1D_H_sign_interval_rows_sha256": digest(
            edge_regions_expected
        ),
        "H_zero_0D_edge_incidence_row_count": len(edges_expected),
        "H_zero_0D_edge_incidence_rows_sha256": digest(edges_expected),
        "H_zero_0D_corner_absence_row_count": len(corners_expected),
        "H_zero_0D_corner_absence_rows_sha256": digest(corners_expected),
        "half_open_owner_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "whole_origin_exclusion_credit": 0,
    }
    require(
        candidate == sealed(expected_body)
        and
        partition == complete_independent
        and
        candidate["whole_H_cell_disposition"] == coarse
        and partition["whole_cell_disposition"] == coarse
        and partition["relative_3D_coverage"] == "1"
        and Q(partition["exact_volume"]) == r215.box_volume(source.box)
        and partition["terminal_rectangle_count"] == len(terminals)
        == len(independent_terminals)
        and partition["terminal_rectangle_disposition_census"]
        == dict(sorted(Counter(
            value["coarse_disposition"] for value in terminals
        ).items()))
        and partition["terminal_rectangles_sha256"] == digest(terminals)
        and partition["internal_split_2D_face_rows_sha256"]
        == digest(partition["internal_split_2D_face_rows"])
        and len(partition["internal_split_2D_face_rows"])
        == ownership["internal_split_2D_face_count"],
        "H independent partition:" + source.key,
    )
    expected_classes = Counter(
        value["classification"] for value in independent_terminals
    )
    require(
        Counter(value["classification"] for value in terminals)
        == expected_classes,
        "H independent terminal classes:" + source.key,
    )
    validate_disposition_aware_split_owners(partition)
    typed_sheets: list[dict[str, Any]] = []
    all_faces: list[dict[str, Any]] = []
    all_edges: list[dict[str, Any]] = []
    all_corners: list[dict[str, Any]] = []
    for terminal in terminals:
        validate_nested_row(
            terminal, "cm2.round306c30b.H-terminal-rectangle.row.v1",
            terminal["terminal_id"],
        )
        require(
            terminal["coarse_disposition"]
            == (
                "EXCLUDED" if terminal["classification"] in H_EXCLUSION_CLASSES
                else "LIVE" if terminal["classification"] in H_LIVE_CLASSES
                else "MIXED"
            ),
            "terminal coarse class",
        )
        if terminal["classification"] != H_TYPED:
            require("typed_strata" not in terminal, "untyped terminal strata")
            continue
        strata = terminal["typed_strata"]
        validate_typed_boundary_exhaustion(terminal)
        sides = strata["open_3D_sides"]
        require(
            len(sides) == 2
            and Counter(value["disposition"] for value in sides)
            == Counter({"LIVE": 1, "EXCLUDED": 1})
            and all(value["ambient_dimension"] == 3 for value in sides)
            and all(value["nonempty_positive_measure"] is True for value in sides),
            "typed H open sides",
        )
        for side in sides:
            validate_nested_row(side, "cm2.round306c30b.H-open-side.row.v1", "H side")
        sheet = strata["H_zero_2D_sheet"]
        validate_nested_row(sheet, "cm2.round306c30b.H-zero-sheet.row.v1", "H sheet")
        require(
            sheet["ambient_dimension"] == 2 and sheet["nonempty"] is True
            and sheet["half_open_owner_chart"] == "W"
            and sheet["disposition"] == "LIVE"
            and sheet["unique_graph_in_p_by_strict_dH_dp"] is True,
            "typed H 2D owner",
        )
        faces = strata["H_zero_1D_face_incidences"]
        edges = strata["H_zero_0D_edge_incidences"]
        corners = strata["H_zero_0D_corner_absence_rows"]
        require(
            len(faces) == 6 and len(edges) == 12 and len(corners) == 8
            and sheet["face_incidence_rows_sha256"] == digest(faces)
            and sheet["edge_incidence_rows_sha256"] == digest(edges)
            and sheet["corner_incidence_rows_sha256"] == digest(corners),
            "typed H 1D/0D exhaustion",
        )
        for value in faces:
            validate_nested_row(value, "cm2.round306c30b.H-sheet-face-incidence.row.v1", "H face")
            require(
                not value["nonempty"]
                or value["half_open_outgoing_owner_chart"] == "W",
                "H face owner",
            )
        for value in edges:
            validate_nested_row(value, "cm2.round306c30b.H-sheet-edge-incidence.row.v1", "H edge")
            require(
                not value["nonempty"]
                or value["half_open_outgoing_owner_chart"] == "W",
                "H edge owner",
            )
        for value in corners:
            validate_nested_row(value, "cm2.round306c30b.H-sheet-corner-incidence.row.v1", "H corner")
            require(value["nonempty"] is False, "strict H corner absence")
        typed_sheets.append(sheet)
        all_faces.extend(faces)
        all_edges.extend(edges)
        all_corners.extend(corners)
    require(
        candidate["typed_H_zero_2D_sheet_count"] == len(typed_sheets)
        and candidate["typed_H_zero_2D_sheet_rows_sha256"] == digest(typed_sheets)
        and candidate["H_zero_1D_face_incidence_row_count"] == len(all_faces)
        and candidate["H_zero_1D_face_incidence_rows_sha256"] == digest(all_faces)
        and candidate["H_zero_0D_edge_incidence_row_count"] == len(all_edges)
        and candidate["H_zero_0D_edge_incidence_rows_sha256"] == digest(all_edges)
        and candidate["H_zero_0D_corner_absence_row_count"] == len(all_corners)
        and candidate["H_zero_0D_corner_absence_rows_sha256"] == digest(all_corners),
        "H lower-dimensional aggregate:" + source.key,
    )
    return coarse


def descriptor_check(path: Path, descriptor: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    require(
        set(descriptor) == {
            "filename", "row_count", "size", "sha256",
            "row_sequence_sha256", "order",
        }
        and descriptor["filename"] == path.name
        and descriptor["row_count"] == len(rows)
        and descriptor["size"] == path.stat().st_size
        and descriptor["sha256"] == file_hash(path)
        and descriptor["row_sequence_sha256"] == sequence.hexdigest(),
        "ledger descriptor:" + path.name,
    )
    require(
        descriptor["order"] == (
            "LEXICOGRAPHIC_H_CELL_KEY" if path.name == H_LEDGER
            else "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY"
        ),
        "ledger order contract:" + path.name,
    )


def independent_prior_boxes(
    origin: str, context: dict[str, Any]
) -> dict[str, Any]:
    evidence = sorted(
        context["Round176_prior_rows"], key=lambda value: value["leaf_key"]
    )
    by_key = {value["leaf_key"]: value for value in evidence}
    boxes: dict[str, Any] = {}
    pending = [(context["source_box"], 0)]
    while pending:
        box, depth = pending.pop()
        key = f"{context['source_chart_id']}:{box.path}"
        if key in by_key:
            require(
                by_key[key]["relative_depth"] == depth,
                "prior evidence relative depth:" + key,
            )
            boxes[key] = box
            continue
        if depth == 6:
            continue
        lower, upper = r176.split(box)
        pending.extend(((lower, depth + 1), (upper, depth + 1)))
    require(set(boxes) == set(by_key), "prior evidence boxes:" + origin)
    return boxes


def independent_prior_evidence_sha256(
    origin: str, context: dict[str, Any]
) -> str:
    boxes = independent_prior_boxes(origin, context)
    evidence = sorted(
        context["Round176_prior_rows"], key=lambda value: value["leaf_key"]
    )
    rows = [{
        "upstream_evidence": value,
        "closed_box": r176.box_row(boxes[value["leaf_key"]]),
        "whole_closed_box_excluded": True,
    } for value in evidence]
    return digest(rows)


def _independent_atomic_owner_reclosure(
    label: str,
    parent: Any,
    leaf_boxes: dict[str, Any],
    proof_source: dict[str, str],
    dispositions: dict[str, str],
    round176_faces: list[dict[str, Any]],
    round180_faces: list[dict[str, Any]],
    *,
    audit_scope: str = "WHOLE_ORIGIN_LINEAGE",
    leaf_key_kind: str = "CELL_KEY",
) -> dict[str, Any]:
    """Reclose the full 3D leaf partition and every induced lower stratum.

    This is deliberately reconstructed from the pinned R176/R180/R215 inputs.
    No producer conclusion, owner choice, count, or digest is used as an input.
    """
    require(
        bool(leaf_boxes)
        and len(leaf_boxes) == len(set(leaf_boxes))
        and
        set(leaf_boxes) == set(dispositions) == set(proof_source),
        "complete 3D leaf maps:" + label,
    )

    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (box.t0, box.t1),
            "p": (box.p0, box.p1),
            "s": (box.s0, box.s1),
        }
        for key, box in leaf_boxes.items()
    }
    parent_bounds = {
        "t": (parent.t0, parent.t1),
        "p": (parent.p0, parent.p1),
        "s": (parent.s0, parent.s1),
    }

    # Closed 3D boxes are an exhaustive partition once containment, positive
    # volume, strict-interior disjointness, and exact total volume all hold.
    leaf_volume_rows: list[dict[str, Any]] = []
    leaf_volume = Q(0)
    for key in sorted(leaf_boxes):
        box = leaf_boxes[key]
        require(
            all(
                parent_bounds[axis][0] <= bounds[key][axis][0]
                < bounds[key][axis][1] <= parent_bounds[axis][1]
                for axis in axes
            ),
            "3D leaf parent containment:" + key,
        )
        volume = r215.box_volume(box)
        require(volume > 0, "positive 3D leaf volume:" + key)
        leaf_volume += volume
        leaf_volume_rows.append({
            "cell_key": key,
            "closed_box": r176.box_row(box),
            "exact_volume": str(volume),
            "disposition": dispositions[key],
            "proof_source": proof_source[key],
        })
    parent_volume = r215.box_volume(parent)
    require(leaf_volume == parent_volume, "exact 3D leaf volume sum:" + label)

    pair_count = 0
    pair_hash = hashlib.sha256()
    pair_hash.update(b"[")
    ordered_keys = sorted(leaf_boxes)
    for first_ordinal, first in enumerate(ordered_keys):
        for second in ordered_keys[first_ordinal + 1:]:
            interior_overlap = all(
                max(bounds[first][axis][0], bounds[second][axis][0])
                < min(bounds[first][axis][1], bounds[second][axis][1])
                for axis in axes
            )
            require(
                not interior_overlap,
                "strict-interior 3D leaf overlap:" + first + ":" + second,
            )
            pair_row = {
                "first": first,
                "second": second,
                "interior_overlap": interior_overlap,
            }
            if pair_count:
                pair_hash.update(b",")
            pair_hash.update(wire(pair_row))
            pair_count += 1
    pair_hash.update(b"]")
    require(
        pair_count == len(leaf_boxes) * (len(leaf_boxes) - 1) // 2,
        "complete 3D pair census:" + label,
    )
    three_dimensional_reclosure = {
        "closed_leaf_count": len(leaf_boxes),
        "closed_leaf_rows_sha256": digest(leaf_volume_rows),
        "closed_leaf_pair_count": pair_count,
        "closed_leaf_pair_rows_sha256": pair_hash.hexdigest(),
        "parent_exact_volume": str(parent_volume),
        "closed_leaf_exact_volume_sum": str(leaf_volume),
        "all_closed_leaves_contained_in_parent": True,
        "all_closed_leaf_strict_interiors_pairwise_disjoint": True,
        "closed_leaf_union_exhausts_parent_by_exact_volume": True,
    }
    three_dimensional_reclosure["reclosure_sha256"] = digest(
        three_dimensional_reclosure
    )

    grid = {
        axis: sorted({value for item in bounds.values() for value in item[axis]})
        for axis in axes
    }
    require(
        all(
            values and values[0] == parent_bounds[axis][0]
            and values[-1] == parent_bounds[axis][1]
            for axis, values in grid.items()
        ),
        "axis grid spans parent:" + label,
    )

    def cuts(axis: str, lower: Q, upper: Q) -> list[Q]:
        values = [lower] + [
            value for value in grid[axis] if lower < value < upper
        ] + [upper]
        require(
            lower < upper and values == sorted(set(values)),
            "strict atomic grid cuts:" + label,
        )
        return values

    def containing_owner(
        fixed: dict[str, Q], open_spans: dict[str, tuple[Q, Q]]
    ) -> str:
        require(
            set(fixed).isdisjoint(open_spans)
            and set(fixed) | set(open_spans) == set(axes),
            "atomic geometry axes:" + label,
        )
        midpoints = {
            axis: (span[0] + span[1]) / 2
            for axis, span in open_spans.items()
        }
        midpoint_candidates = sorted(
            key for key, item in bounds.items()
            if all(item[axis][0] <= value <= item[axis][1]
                   for axis, value in fixed.items())
            and all(item[axis][0] < value < item[axis][1]
                    for axis, value in midpoints.items())
        )
        whole_atom_candidates = sorted(
            key for key, item in bounds.items()
            if all(item[axis][0] <= value <= item[axis][1]
                   for axis, value in fixed.items())
            and all(item[axis][0] <= span[0] < span[1] <= item[axis][1]
                    for axis, span in open_spans.items())
        )
        require(
            midpoint_candidates
            and midpoint_candidates == whole_atom_candidates,
            "constant closed-leaf incidence on whole atom:" + label,
        )
        return midpoint_candidates[0]

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
                "coordinate": str(coordinate),
                "spans": {
                    axis: [str(parent_bounds[axis][0]),
                           str(parent_bounds[axis][1])]
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
                    "fixed": {fixed_axis: str(fixed_value)},
                    "open_spans": {
                        free_axes[0]: [str(first_lower), str(first_upper)],
                        free_axes[1]: [str(second_lower), str(second_upper)],
                    },
                }
                encoded = wire(geometry).decode("ascii")
                group = face_atoms.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(raw["source"])
                atom_keys.append(encoded)
                atom_measure += (
                    (first_upper - first_lower)
                    * (second_upper - second_lower)
                )
        require(atom_measure == source_measure,
                "exact atomic face reclosure:" + label)
        raw_face_reclosure.append({
            "source": raw["source"],
            "source_exact_measure": str(source_measure),
            "atomic_exact_measure": str(atom_measure),
            "atomic_geometry_keys_sha256": digest(sorted(atom_keys)),
        })
        for boundary_axis in free_axes:
            other = next(axis for axis in free_axes if axis != boundary_axis)
            for side, endpoint in zip(
                ("LOWER", "UPPER"), spans[boundary_axis]
            ):
                geometry = {
                    "fixed": {
                        fixed_axis: str(fixed_value),
                        boundary_axis: str(endpoint),
                    },
                    "open_span": {
                        other: [str(spans[other][0]), str(spans[other][1])]
                    },
                }
                encoded = wire(geometry).decode("ascii")
                group = raw_edges.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
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
                    fixed_axis: str(fixed_value),
                    free_axes[0]: str(first),
                    free_axes[1]: str(second),
                }}
                encoded = wire(geometry).decode("ascii")
                group = raw_corners.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(
                    raw["source"] + ":" + first_side + ":" + second_side
                )

    # Every 2D grid atom contributes its complete cut-line/cut-point boundary.
    # This closes measure-zero strata created by interior leaf-bound cuts, not
    # merely the outer boundaries of the original unsplit face rectangles.
    for _encoded, atom in sorted(face_atoms.items()):
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
                encoded = wire(geometry).decode("ascii")
                group = raw_edges.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
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
                encoded = wire(geometry).decode("ascii")
                group = raw_corners.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(
                    atom_source + ":" + first_side + ":" + second_side
                )

    face_rows: list[dict[str, Any]] = []
    for _encoded, group in sorted(face_atoms.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["fixed"].items()
        }
        open_spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in group["geometry"]["open_spans"].items()
        }
        owner = containing_owner(fixed, open_spans)
        span_values = list(open_spans.values())
        face_rows.append(sealed({
            "schema": "cm2.round306c30b.atomic-2D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
            "exact_measure": str(
                (span_values[0][1] - span_values[0][0])
                * (span_values[1][1] - span_values[1][0])
            ),
        }))

    edge_atoms: dict[str, dict[str, Any]] = {}
    raw_edge_reclosure: list[dict[str, Any]] = []
    for _encoded, raw in sorted(raw_edges.items()):
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
                    free_axis: [str(atom_lower), str(atom_upper)]
                },
            }
            encoded = wire(geometry).decode("ascii")
            group = edge_atoms.setdefault(encoded, {
                "geometry": geometry, "incident_sources": [],
            })
            group["incident_sources"].extend(raw["incident_sources"])
            atom_keys.append(encoded)
            atom_measure += atom_upper - atom_lower
            atom_source = "ATOMIC_1D:" + digest(geometry)
            for side, endpoint in (
                ("LOWER", atom_lower), ("UPPER", atom_upper)
            ):
                point = dict(raw["geometry"]["fixed"])
                point[free_axis] = str(endpoint)
                point_geometry = {"point": point}
                point_key = wire(point_geometry).decode("ascii")
                point_group = raw_corners.setdefault(point_key, {
                    "geometry": point_geometry, "incident_sources": [],
                })
                point_group["incident_sources"].append(
                    atom_source + ":" + side
                )
        require(atom_measure == source_measure,
                "exact atomic edge reclosure:" + label)
        raw_edge_reclosure.append({
            "source_geometry_sha256": digest(raw["geometry"]),
            "source_exact_measure": str(source_measure),
            "atomic_exact_measure": str(atom_measure),
            "atomic_geometry_keys_sha256": digest(sorted(atom_keys)),
        })

    edge_rows: list[dict[str, Any]] = []
    for _encoded, group in sorted(edge_atoms.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["fixed"].items()
        }
        free_axis, values = next(iter(group["geometry"]["open_span"].items()))
        open_spans = {free_axis: (Q(values[0]), Q(values[1]))}
        owner = containing_owner(fixed, open_spans)
        edge_rows.append(sealed({
            "schema": "cm2.round306c30b.atomic-1D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
            "exact_measure": str(open_spans[free_axis][1]
                                 - open_spans[free_axis][0]),
        }))

    corner_rows: list[dict[str, Any]] = []
    for _encoded, group in sorted(raw_corners.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["point"].items()
        }
        owner = containing_owner(fixed, {})
        corner_rows.append(sealed({
            "schema": "cm2.round306c30b.atomic-0D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
        }))

    all_rows = face_rows + edge_rows + corner_rows
    candidate_audit = {
        "schema": "cm2.round306c30b.exact-atomic-half-open-owner-audit.v2",
        "audit_scope": audit_scope,
        "leaf_key_kind": leaf_key_kind,
        "exact_3D_enclosure": {
            "all_leaf_boxes_contained_in_parent_and_nondegenerate": True,
            "pairwise_leaf_interiors_disjoint": True,
            "tested_unordered_leaf_pair_count": pair_count,
            "tested_leaf_pair_rows_sha256": pair_hash.hexdigest(),
            "leaf_exact_volume_sum": str(leaf_volume),
            "parent_exact_volume": str(parent_volume),
            "leaf_exact_volume_sum_equals_parent": True,
        },
        "axis_grid_coordinate_count": {
            axis: len(values) for axis, values in grid.items()
        },
        "axis_grid_coordinates_sha256": digest({
            axis: [str(value) for value in values]
            for axis, values in grid.items()
        }),
        "atomic_owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "closed_3D_leaf_count": len(leaf_boxes),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_boxes)),
        "closed_3D_leaf_disposition_census": dict(sorted(Counter(
            dispositions.values()
        ).items())),
        "raw_2D_stratum_reclosure_row_count": len(raw_face_reclosure),
        "raw_2D_stratum_reclosure_rows_sha256": digest(raw_face_reclosure),
        "all_raw_2D_strata_exactly_reclosed": all(
            value["source_exact_measure"] == value["atomic_exact_measure"]
            for value in raw_face_reclosure
        ),
        "raw_1D_stratum_reclosure_row_count": len(raw_edge_reclosure),
        "raw_1D_stratum_reclosure_rows_sha256": digest(raw_edge_reclosure),
        "all_raw_1D_strata_exactly_reclosed": all(
            value["source_exact_measure"] == value["atomic_exact_measure"]
            for value in raw_edge_reclosure
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
            value["owner_disposition"] for value in all_rows
        ).items())),
        "atomic_owner_rows_sha256": digest(all_rows),
    }
    require(
        bool(face_rows) and bool(edge_rows) and bool(corner_rows),
        "nonempty 2D/1D/0D atomic owner ledgers:" + label,
    )
    return {
        "candidate_audit": candidate_audit,
        "independent_3D_reclosure": three_dimensional_reclosure,
    }


def exact_axis_grid_owner_reclosure(
    origin: str, context: dict[str, Any], h_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    refinement = context["refinement"]
    leaves = r215.reconstruct_refinement_leaf_frontiers(
        context["roots"], refinement
    )
    prior_boxes = independent_prior_boxes(origin, context)
    leaf_boxes: dict[str, Any] = {}

    def add_leaf(key: str, box: Any) -> None:
        require(key not in leaf_boxes, "duplicate closed 3D leaf:" + key)
        leaf_boxes[key] = box

    for key, box in prior_boxes.items():
        add_leaf(key, box)
    for value in context["preclosed_rows"]:
        add_leaf(value.key, value.box)
    for key, value in leaves["terminal"].items():
        add_leaf(key, value.box)
    for key, value in leaves["final"].items():
        add_leaf(key, value.box)

    h_by_key = {value["cell_key"]: value for value in h_rows}
    require(len(h_by_key) == len(h_rows), "origin H key uniqueness:" + origin)
    require(set(h_by_key) <= set(leaf_boxes), "H leaves in 3D closure:" + origin)
    dispositions = {
        key: (
            h_by_key[key]["whole_H_cell_disposition"]
            if key in h_by_key else "EXCLUDED"
        )
        for key in leaf_boxes
    }
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED" for key in prior_boxes
    }
    proof_source.update({
        value.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED"
        for value in context["preclosed_rows"]
    })
    proof_source.update({
        key: (
            "ROUND306C30B_MATERIALIZED_SAME_SIGN_DELTA_FOLLOWUP_H"
            if key in h_by_key and h_by_key[key]["source_kind"]
            == "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
            else "ROUND306C30B_MATERIALIZED_INHERITED_OUTGOING_H"
            if key in h_by_key
            else "PINNED_ROUND180_INHERITED_EXCLUDED"
        )
        for key in leaves["terminal"]
    })
    proof_source.update({
        key: (
            "ROUND306C30B_MATERIALIZED_ROUND215_OUTGOING_H"
            if key in h_by_key
            else "PINNED_OR_RECONSTRUCTED_FINAL_EXCLUDED_BUCKET"
        )
        for key in leaves["final"]
    })

    # Reconstruct the pre-R176 split faces without importing C30a.
    prior_faces: list[dict[str, Any]] = []
    frontier_keys = {
        value.key for value in context["roots"] + context["preclosed_rows"]
    }
    pending = [(context["source_box"], 0)]
    while pending:
        box, depth = pending.pop()
        key = f"{context['source_chart_id']}:{box.path}"
        if key in prior_boxes:
            continue
        if depth == 6:
            require(key in frontier_keys, "Round176 frontier identity:" + key)
            continue
        lower, upper = r176.split(box)
        parent_row = r176.Frontier(
            context["source_chart_id"], box, (), origin,
            "ROUND176_PARTITION_SPLIT",
        )
        prior_faces.append(r180.split_face(
            parent_row, r180.split_axis(box), lower, upper
        ))
        pending.extend(((lower, depth + 1), (upper, depth + 1)))
    prior_faces.sort(key=lambda value: value["parent_cell_key"])
    return _independent_atomic_owner_reclosure(
        origin,
        context["source_box"],
        leaf_boxes,
        proof_source,
        dispositions,
        prior_faces,
        refinement["split_face_rows"],
    )


def origin_compositions(
    origin_context: dict[str, dict[str, Any]],
    evidence_by_key: dict[str, dict[str, Any]],
    h_by_key: dict[str, str],
) -> dict[str, dict[str, Any]]:
    c30a_rows = canonical_rows(C30A_SEALED / C30A_CELL)
    c30a_by_key = {row["cell_key"]: row for row in c30a_rows}
    require(len(c30a_by_key) == 12_888, "sealed C30a cell uniqueness")
    output: dict[str, dict[str, Any]] = {}
    for origin in EXPECTED_KEYS:
        context = origin_context[origin]
        refinement = context["refinement"]
        inherited_excluded = sum(
            item["coarse_disposition"] == "EXCLUDED"
            for item in refinement["terminal_rows"]
        )
        inherited_h = [
            item["cell_key"] for item in refinement["terminal_rows"]
            if item["coarse_disposition"] != "EXCLUDED"
        ]
        inherited_followup_h = [
            item for item in refinement["terminal_rows"]
            if item["coarse_disposition"] != "EXCLUDED"
            and item["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
        ]
        inherited_direct_h = [
            item for item in refinement["terminal_rows"]
            if item["coarse_disposition"] != "EXCLUDED"
            and item["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE"
        ]
        exact_closed = analytic_closed = c30a_closed = 0
        exact_volume = analytic_volume = c30a_volume = Q(0)
        final_excluded_evidence: dict[str, list[dict[str, Any]]] = {
            "Round201_exact_behind": [], "Round215_analytic": [],
            "Round306C30A": [],
        }
        final_h: list[str] = []
        for row in sorted(
            refinement["final_residual_rows"], key=lambda value: value.key
        ):
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            if reduction["closed"]:
                exact_closed += 1
                exact_volume += r215.box_volume(row.box)
                final_excluded_evidence["Round201_exact_behind"].append({
                    "cell_key": row.key,
                    "reduction_sha256": digest({
                        key: reduction[key] for key in (
                            "category", "residual_reason", "closed",
                            "disposition", "eligible_targets",
                            "candidate_evidence",
                        )
                    }),
                })
                continue
            evidence = evidence_by_key[row.key]
            if evidence["analytic_closed"]:
                proof = evidence.get("closed_box_boundary_restriction_proof")
                require(
                    proof is not None
                    and proof[
                        "closed_box_strict_inequalities_restrict_to_all_faces_edges_vertices"
                    ] is True,
                    "R215 analytic lower strata:" + row.key,
                )
                analytic_closed += 1
                analytic_volume += r215.box_volume(row.box)
                final_excluded_evidence["Round215_analytic"].append({
                    "cell_key": row.key,
                    "Round215_cell_row_sha256": independent_r215_evidence(
                        row, reduction
                    )["row_sha256"],
                })
                continue
            if row.key in h_by_key:
                final_h.append(row.key)
                continue
            sealed = c30a_by_key.get(row.key)
            require(
                sealed is not None
                and sealed["whole_closed_cell_excluded"] is True
                and sealed["partition"][
                    "closed_box_and_all_owned_faces_edges_vertices_excluded"
                ] is True,
                "C30a non-H final closure:" + row.key,
            )
            c30a_closed += 1
            c30a_volume += r215.box_volume(row.box)
            final_excluded_evidence["Round306C30A"].append({
                "cell_key": row.key,
                "C30a_cell_row_sha256": sealed["row_sha256"],
            })
        h_keys = sorted(inherited_h + final_h)
        require(
            len(h_keys) == len(set(h_keys))
            and all(key in h_by_key for key in h_keys),
            "origin H lineage exhaustion:" + origin,
        )
        h_census = Counter(h_by_key[key] for key in h_keys)
        disposition = (
            "EXCLUDED" if set(h_census) == {"EXCLUDED"}
            else "RESOLVED_MIXED"
        )
        composition = {
            "Round176_prior_closed_count": context[
                "Round176_prior_closed_count"
            ],
            "Round176_preclosed_frontier_count": context[
                "Round176_preclosed_count"
            ],
            "Round176_residual_root_count": context[
                "Round176_residual_root_count"
            ],
            "Round180_inherited_excluded_count": inherited_excluded,
            "Round180_inherited_direct_H_count": len(inherited_direct_h),
            "Round180_inherited_same_sign_Delta_followup_H_count": len(
                inherited_followup_h
            ),
            "Round180_inherited_H_materialized_count": len(inherited_h),
            "Round180_final_cell_count": len(
                refinement["final_residual_rows"]
            ),
            "Round201_exact_behind_closed_count": exact_closed,
            "Round215_analytic_closed_count": analytic_closed,
            "Round306C30A_closed_count": c30a_closed,
            "outgoing_H_cell_count": len(h_keys),
            "all_non_H_3D_2D_1D_0D_strata_excluded_or_empty": True,
        }
        output[origin] = {
            "H_cell_keys": h_keys,
            "H_cell_disposition_census": dict(sorted(h_census.items())),
            "lineage_composition": composition,
            "whole_origin_disposition": disposition,
            "inherited_same_sign_Delta_followup_H_rows": inherited_followup_h,
            "_context": context,
            "_closed_volumes": {
                "Round201": exact_volume, "Round215": analytic_volume,
                "Round306C30A": c30a_volume,
            },
            "_final_excluded_evidence": final_excluded_evidence,
        }
    require(
        tuple(sorted(
            key for key, value in output.items()
            if value["whole_origin_disposition"] == "EXCLUDED"
        )) == EXPECTED_EXCLUDED_KEYS
        and tuple(sorted(
            key for key, value in output.items()
            if value["whole_origin_disposition"] == "RESOLVED_MIXED"
        )) == EXPECTED_MIXED_KEYS,
        "evidence-derived 2 excluded / 10 resolved mixed",
    )
    return output


def validate_origin_row(
    row: dict[str, Any], ordinal: int, expected: dict[str, Any],
    h_rows: list[dict[str, Any]], priority_ordinal: int,
) -> None:
    origin = row["origin_key"]
    disposition = expected["whole_origin_disposition"]
    excluded = disposition == "EXCLUDED"
    context = expected["_context"]
    require(set(row) == {
        "schema", "origin_ordinal", "origin_key", "priority_ordinal",
        "source_chart_id", "original_parent_box", "H_cell_count",
        "H_cell_keys_sha256", "H_cell_rows_sha256",
        "H_cell_disposition_census", "whole_origin_disposition",
        "whole_original_physical_origin_excluded",
        "whole_origin_exclusion_credit", "resolved_nonexcluded_credit",
        "positive_measure_LIVE_witness_count",
        "positive_measure_LIVE_witnesses_sha256",
        "lexicographic_first_positive_measure_LIVE_witness",
        "lineage_composition", "lineage_composition_evidence",
        "whole_origin_theorem", "whole_origin_theorem_sha256",
        "formal_credit", "strict_nonpromotion", "row_sha256",
    }, "whole-origin exact keyset:" + origin)
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
    live_witnesses.sort(key=wire)
    all_h_partitions_exact = all(
        value["H_partition"][
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True
        and value["H_partition"]["terminal_exact_atomic_owner_audit"][
            "closed_3D_leaf_count"
        ] == value["H_partition"]["terminal_rectangle_count"]
        for value in h_rows
    )
    theorem = {
        "kind": "SOURCE_W_OUTGOING_H_WHOLE_ORIGIN_DISPOSITION_THEOREM",
        "prior_frontier_and_refinement_partitions_are_exact": True,
        "all_components_outside_materialized_outgoing_H_cells_excluded": True,
        "same_sign_Delta_followup_H_provenance_is_explicitly_bound": bool(
            expected["inherited_same_sign_Delta_followup_H_rows"]
        ),
        "each_outgoing_H_cell_has_exhaustive_disjoint_3D_2D_1D_0D_partition": (
            all_h_partitions_exact
        ),
        "half_open_H_zero_owner_rule": (
            "CHART_W_FOR_RELATIVE_INTERIOR__ATOMIC_GRID_FOR_DYADIC_BOUNDARY"
        ),
        "whole_origin_outcome_derived_from_complete_composition": True,
        "whole_original_physical_origin_excluded": excluded,
    }
    require(
        row["schema"]
        == (
            "cm2.round306c30b.source-w-outgoing-h."
            "whole-origin-disposition.row.v1"
        )
        and row["origin_ordinal"] == ordinal
        and row["priority_ordinal"] == priority_ordinal
        and row["source_chart_id"] == context["source_chart_id"],
        "origin priority/source preliminary:" + origin,
    )
    require(
        row["original_parent_box"] == r176.box_row(context["source_box"])
        and row["H_cell_count"] == len(expected["H_cell_keys"])
        and row["H_cell_keys_sha256"] == digest(expected["H_cell_keys"])
        and row["H_cell_disposition_census"]
        == expected["H_cell_disposition_census"]
        and row["H_cell_rows_sha256"] == digest(h_rows)
        and row["lineage_composition"] == expected["lineage_composition"]
        and row["whole_origin_disposition"] == disposition
        and row["whole_original_physical_origin_excluded"] is excluded
        and row["whole_origin_exclusion_credit"] == int(excluded)
        and row["resolved_nonexcluded_credit"] == int(not excluded)
        and row["positive_measure_LIVE_witness_count"] == len(live_witnesses)
        and row["positive_measure_LIVE_witnesses_sha256"]
        == digest(live_witnesses)
        and row["lexicographic_first_positive_measure_LIVE_witness"]
        == (live_witnesses[0] if live_witnesses else "NOT_APPLICABLE_EXCLUDED")
        and row["formal_credit"] == {
            "resolved_source_W_origin_disposition": 1,
            "whole_source_W_origin_exclusion": int(excluded),
        }
        and row["strict_nonpromotion"] == {
            "child_or_volume_as_integer_credit": 0,
            "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
        }
        and row["whole_origin_theorem"] == theorem
        and row["whole_origin_theorem_sha256"] == digest(theorem),
        "whole-origin row:" + origin,
    )
    body = dict(row)
    claimed = body.pop("row_sha256")
    require(claimed == digest(body), "whole-origin closure:" + origin)
    evidence = row["lineage_composition_evidence"]
    refinement = context["refinement"]
    require(set(evidence) == {
        "Round176_prior_rows_sha256",
        "Round176_preclosed_frontier_keys_sha256",
        "Round176_residual_root_keys_sha256",
        "Round180_inherited_terminal_rows_sha256",
        "Round180_final_cell_keys_sha256", "Round180_split_face_rows_sha256",
        "disposition_aware_half_open_owner_audit",
        "non_H_upstream_evidence_binding_sha256",
        "same_sign_Delta_followup_H_provenance_bucket",
        "materialized_H_strata_owner_aggregation", "exact_volume_conservation",
    }, "origin composition evidence exact keyset:" + origin)
    require(
        evidence["Round176_prior_rows_sha256"]
        == digest(sorted(item["leaf_key"] for item in context[
            "Round176_prior_rows"
        ]))
        and evidence["Round176_preclosed_frontier_keys_sha256"]
        == digest(sorted(item.key for item in context["preclosed_rows"]))
        and evidence["Round176_residual_root_keys_sha256"]
        == digest(sorted(item.key for item in context["roots"]))
        and evidence["Round180_inherited_terminal_rows_sha256"]
        == digest(sorted(refinement["terminal_rows"], key=lambda value: value[
            "cell_key"
        ]))
        and evidence["Round180_final_cell_keys_sha256"]
        == digest(sorted(item.key for item in refinement["final_residual_rows"]))
        and evidence["Round180_split_face_rows_sha256"]
        == digest(refinement["split_face_rows"]),
        "origin lineage exact key buckets:" + origin,
    )
    h_internal_2d = [
        face["face_sha256"] for value in h_rows
        for face in value["H_partition"]["internal_split_2D_face_rows"]
    ]
    h_internal_1d = [
        item["row_sha256"] for value in h_rows
        for item in value["H_partition"]["internal_split_1D_edge_owner_rows"]
    ]
    h_internal_0d = [
        item["row_sha256"] for value in h_rows
        for item in value["H_partition"]["internal_split_0D_corner_owner_rows"]
    ]
    h_terminal_atomic_audits = [
        value["H_partition"]["terminal_exact_atomic_owner_audit"]
        for value in h_rows
    ]
    h_partitions_exact = all(
        value["H_partition"][
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True
        and value["H_partition"]["terminal_exact_atomic_owner_audit"][
            "closed_3D_leaf_count"
        ] == value["H_partition"]["terminal_rectangle_count"]
        for value in h_rows
    )
    typed = [
        terminal for value in h_rows
        for terminal in value["H_partition"]["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
    ]
    sheets = [value["typed_strata"]["H_zero_2D_sheet"]["row_sha256"]
              for value in typed]
    face_regions = [item["row_sha256"] for value in typed for item in
                    value["typed_strata"]["terminal_face_2D_H_sign_regions"]]
    edge_regions = [item["row_sha256"] for value in typed for item in
                    value["typed_strata"]["terminal_edge_1D_H_sign_intervals"]]
    corner_signs = [item["row_sha256"] for value in typed for item in
                    value["typed_strata"]["H_zero_0D_corner_absence_rows"]]
    require(evidence["materialized_H_strata_owner_aggregation"] == {
        "internal_split_2D_face_count": len(h_internal_2d),
        "internal_split_2D_face_sha256": digest(h_internal_2d),
        "raw_noncredit_internal_split_1D_incidence_count": len(h_internal_1d),
        "raw_noncredit_internal_split_1D_incidence_sha256": digest(
            h_internal_1d
        ),
        "raw_noncredit_internal_split_0D_incidence_count": len(h_internal_0d),
        "raw_noncredit_internal_split_0D_incidence_sha256": digest(
            h_internal_0d
        ),
        "terminal_exact_atomic_audit_count": len(h_terminal_atomic_audits),
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
        "typed_H_zero_2D_sheet_count": len(sheets),
        "typed_H_zero_2D_sheet_sha256": digest(sheets),
        "closed_enclosure_face_2D_sign_region_count": len(face_regions),
        "closed_enclosure_face_2D_sign_region_sha256": digest(face_regions),
        "closed_enclosure_edge_1D_sign_interval_count": len(edge_regions),
        "closed_enclosure_edge_1D_sign_interval_sha256": digest(edge_regions),
        "closed_enclosure_corner_0D_strict_sign_count": len(corner_signs),
        "closed_enclosure_corner_0D_strict_sign_sha256": digest(corner_signs),
        "typed_boundary_ownership_scope": "CLOSED_ENCLOSURE_ONLY",
        "dyadic_boundary_owner_source": (
            "PER_H_CELL_TERMINAL_EXACT_ATOMIC_HALF_OPEN_OWNER_AUDIT"
        ),
    }, "origin materialized H strata aggregation:" + origin)
    leaves = r215.reconstruct_refinement_leaf_frontiers(
        context["roots"], refinement
    )
    h_by_cell = {value["cell_key"]: value for value in h_rows}
    followup_evidence = [
        sealed({
            "schema": (
                "cm2.round306c30b.same-sign-delta-followup-h."
                "evidence-row.v1"
            ),
            "origin_key": origin, "cell_key": item["cell_key"],
            "closed_box": r176.box_row(leaves["terminal"][item[
                "cell_key"
            ]].box),
            "exact_volume": str(r215.box_volume(leaves["terminal"][item[
                "cell_key"
            ]].box)),
            "upstream_terminal_evidence": item,
            "upstream_terminal_sha256": item["terminal_sha256"],
            "method": item["method"],
            "Delta_zero_graph_inside_closed_box": False,
            "empty_2D_graph_edge_and_corner_ledger": True,
            "followup_witness": item["witness"],
            "followup_H_cell_row_sha256": h_by_cell[item["cell_key"]][
                "row_sha256"
            ],
            "formal_disposition_after_followup_H": h_by_cell[item[
                "cell_key"
            ]]["whole_H_cell_disposition"],
            "included_in_outgoing_H_cell_ledger": True,
            "whole_origin_exclusion_credit": 0,
        })
        for item in expected["inherited_same_sign_Delta_followup_H_rows"]
    ]
    followup_volume = sum((r215.box_volume(leaves["terminal"][item[
        "cell_key"
    ]].box) for item in expected[
        "inherited_same_sign_Delta_followup_H_rows"
    ]), Q(0))
    require(evidence["same_sign_Delta_followup_H_provenance_bucket"] == {
        "row_count": len(followup_evidence), "rows": followup_evidence,
        "rows_sha256": digest(followup_evidence),
        "exact_volume": str(followup_volume),
        "post_followup_H_disposition_census": dict(sorted(Counter(
            value["formal_disposition_after_followup_H"]
            for value in followup_evidence
        ).items())),
        "all_Delta_zero_graphs_empty": all(
            value["Delta_zero_graph_inside_closed_box"] is False
            for value in followup_evidence
        ),
        "all_rows_included_in_outgoing_H_ledger": True,
        "all_rows_receive_zero_exclusion_credit": True,
    }, "same-sign Delta followup-H provenance bucket:" + origin)
    base_evidence: list[dict[str, Any]] = []
    for item in context["preclosed_rows"]:
        proof = context["preclosed_closure_evidence"][item.key]
        base_evidence.append({
            "cell_key": item.key, "coarse_disposition": "EXCLUDED",
            "evidence": proof,
        })
    base_evidence.sort(key=lambda value: value["cell_key"])
    inherited_excluded_rows = sorted((
        item for item in refinement["terminal_rows"]
        if item["coarse_disposition"] == "EXCLUDED"
    ), key=lambda value: value["cell_key"])
    final_keys = sorted(
        item.key for item in refinement["final_residual_rows"]
        if item.key not in h_by_cell
    )
    expected_non_h_binding = {
        "Round176_prior_evidence_rows_sha256": (
            independent_prior_evidence_sha256(origin, context)
        ),
        "Round176_preclosed_evidence_rows": base_evidence,
        "Round180_inherited_excluded_rows": inherited_excluded_rows,
        "Round180_inherited_same_sign_Delta_followup_H_rows": followup_evidence,
        "final_excluded_cell_keys": final_keys,
        "final_excluded_evidence": expected["_final_excluded_evidence"],
    }
    require(
        evidence["non_H_upstream_evidence_binding_sha256"]
        == digest(expected_non_h_binding),
        "non-H upstream evidence binding:" + origin,
    )
    original_volume = r215.box_volume(context["source_box"])
    prior_units = sum(item["coverage_numerator_64"] for item in
                      context["Round176_prior_rows"])
    prior_volume = original_volume * Q(prior_units, 64)
    base_volume = sum((r215.box_volume(item.box) for item in
                       context["preclosed_rows"]), Q(0))
    root_volume = sum((r215.box_volume(item.box) for item in context["roots"]), Q(0))
    inherited_volume = sum((r215.box_volume(leaves["terminal"][item[
        "cell_key"
    ]].box) for item in refinement["terminal_rows"]), Q(0))
    final_volume = sum((r215.box_volume(item.box) for item in
                        refinement["final_residual_rows"]), Q(0))
    closed = expected["_closed_volumes"]
    h_volume = sum((Q(value["exact_volume"]) for value in h_rows), Q(0))
    require(evidence["exact_volume_conservation"] == {
        "original_parent": str(original_volume), "Round176_prior": str(prior_volume),
        "Round176_preclosed_frontier": str(base_volume),
        "Round176_residual_roots": str(root_volume),
        "Round180_inherited": str(inherited_volume), "Round180_final": str(final_volume),
        "Round201_exact_behind_closed": str(closed["Round201"]),
        "Round215_analytic_closed": str(closed["Round215"]),
        "Round306C30A_closed": str(closed["Round306C30A"]),
        "outgoing_H_cells": str(h_volume),
        "all_lineage_buckets_pairwise_disjoint": True,
        "all_lineage_buckets_exhaust_original_parent": True,
    }, "origin exact volume conservation:" + origin)
    audit = evidence["disposition_aware_half_open_owner_audit"]
    independent_reclosure = exact_axis_grid_owner_reclosure(
        origin, context, h_rows
    )
    require(
        audit == independent_reclosure["candidate_audit"]
        and (
            not excluded
            or set(audit["atomic_owner_disposition_census"])
            == {"EXCLUDED"}
        )
        and audit["all_raw_2D_strata_exactly_reclosed"] is True
        and audit["all_raw_1D_strata_exactly_reclosed"] is True
        and independent_reclosure["independent_3D_reclosure"][
            "all_closed_leaves_contained_in_parent"
        ] is True
        and independent_reclosure["independent_3D_reclosure"][
            "all_closed_leaf_strict_interiors_pairwise_disjoint"
        ] is True
        and independent_reclosure["independent_3D_reclosure"][
            "closed_leaf_union_exhausts_parent_by_exact_volume"
        ] is True,
        "independent exact 3D/2D/1D/0D owner reclosure:" + origin,
    )


def validate_result(
    result: dict[str, Any],
    candidate: Path,
    h_rows: list[dict[str, Any]],
    origin_rows: list[dict[str, Any]],
    pins: list[dict[str, str]],
    lanes: dict[str, tuple[str, ...]],
) -> None:
    claimed = result.get("result_sha256")
    body = {key: value for key, value in result.items() if key != "result_sha256"}
    require(
        type(claimed) is str and claimed == digest(body),
        "result object closure",
    )
    require(
        set(result) == {
            "schema", "status", "input_pins", "ledgers", "H_cell_census",
            "whole_origin_census", "source_W_ledger_transition",
            "formal_credit", "strict_nonpromotion", "required_next",
            "runtime_attestation", "result_sha256",
        }
        and set(result["ledgers"]) == {
            "outgoing_H_cell", "whole_origin_disposition",
        }
        and result["input_pins"] == pins and len(pins) == 26
        and
        result["schema"]
        == "cm2.round306c30b.source-w-outgoing-h-whole-origin-disposition.v1",
        "result schema",
    )
    require(
        result["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION"
        and result["required_next"] == (
            "CLOSE_2_FULL_DELTA_THEN_20_MULTI_DELTA_THEN_2_REDUCED_LIVE_"
            "THEN_2_RETAINED_SOURCE_SEAMS_THEN_54_COMPACT_Q_ORIGINS"
        ),
        "result status/required next",
    )
    descriptor_check(
        candidate / H_LEDGER,
        result["ledgers"]["outgoing_H_cell"], h_rows,
    )
    descriptor_check(
        candidate / ORIGIN_LEDGER,
        result["ledgers"]["whole_origin_disposition"], origin_rows,
    )
    runtime_raw = regular_bytes(candidate / RUNTIME_ATTESTATION)
    require(
        runtime_raw == BOOTSTRAP_RUNTIME_ATTESTATION_RAW
        and result["runtime_attestation"] == {
            "filename": RUNTIME_ATTESTATION,
            "size": len(runtime_raw),
            "sha256": RUNTIME_ATTESTATION_RAW_SHA256,
            "attestation_payload_sha256": (
                RUNTIME_ATTESTATION_PAYLOAD_SHA256
            ),
            "auditor_sha256": RUNTIME_AUDITOR_SHA256,
            "schema": (
                "cm2.round306c30b.python-flint-runtime-attestation.v1"
            ),
            "verdict": "PASS",
        },
        "runtime attestation result descriptor",
    )
    hybrid_rows = [
        value for value in h_rows
        if value["source_kind"]
        == "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
    ]
    hybrid_pairs = [{
        "Round180_terminal_sha256": value["source_binding"][
            "Round180_terminal_sha256"
        ],
        "analytic_semantic_projection_sha256": value["H_partition"][
            "analytic_semantic_projection_sha256"
        ],
    } for value in hybrid_rows]
    require(
        result["H_cell_census"] == {
            "input": 688,
            "by_disposition": {
                "EXCLUDED": 352, "LIVE": 144, "MIXED": 192,
            },
            "by_source_kind": {
                "ROUND180_INHERITED_OUTGOING_H": 112,
                "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H": 8,
                "ROUND215_RESIDUAL_OUTGOING_H": 560,
                "ROUND306C30A_HELD_INHERITED_OUTGOING_H": 8,
            },
            "typed_H_zero_2D_sheet_count": 192,
            "same_sign_Delta_followup_H": {
                "row_count": 8,
                "cell_keys_sha256": digest([
                    value["cell_key"] for value in hybrid_rows
                ]),
                "full_terminal_evidence_sha256": digest([
                    value["source_binding"]["Round180_terminal_evidence"]
                    for value in hybrid_rows
                ]),
                "terminal_sha256_list_sha256": digest([
                    value["source_binding"]["Round180_terminal_sha256"]
                    for value in hybrid_rows
                ]),
                "analytic_semantic_projection_sha256_list_sha256": digest([
                    value["H_partition"][
                        "analytic_semantic_projection_sha256"
                    ] for value in hybrid_rows
                ]),
                "terminal_to_analytic_semantic_projection_pair_count": 8,
                "terminal_to_analytic_semantic_projection_pairs_sha256": (
                    digest(hybrid_pairs)
                ),
            },
        }
        and result["whole_origin_census"] == {
            "audited": 12,
            "excluded": 2,
            "resolved_mixed": 10,
            "all_origin_keys_sha256": EXPECTED_ALL_KEYS_SHA256,
            "excluded_origin_keys_sha256": EXPECTED_EXCLUDED_KEYS_SHA256,
            "resolved_mixed_origin_keys_sha256": EXPECTED_MIXED_KEYS_SHA256,
        },
        "fixed H/origin census",
    )
    transition = result["source_W_ledger_transition"]
    before_partition = {
        name: len(keys) for name, keys in lanes.items()
    }
    after_partition = {
        name: count for name, count in before_partition.items()
        if name != "outgoing_H"
    }
    require(
        transition == {
            "before": {
            "excluded": 74744, "conservative_live": 2088,
            "remaining": 92, "resolved_nonexcluded": 1996,
            "total": 76832,
            "remaining_partition": before_partition,
            },
            "credits": {
                "whole_origin_exclusion": 2,
                "resolved_origin_disposition": 12,
                "resolved_nonexcluded": 10,
            },
            "after": {
            "excluded": 74746, "conservative_live": 2086,
            "remaining": 80, "resolved_nonexcluded": 2006,
            "total": 76832,
            "remaining_partition": after_partition,
            },
            "conservation_identity": "74746+2086=76832",
        },
        "source-W 92 to 80 transition",
    )
    require(
        result["formal_credit"] == {
            "outgoing_H_cells_disposed": 688,
            "resolved_source_W_origin_dispositions": 12,
            "whole_source_W_origin_exclusions": 2,
        }
        and result["strict_nonpromotion"] == {
            "D02": "BLOCKED_BY_80_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
            "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "formal credit / composite fail-close",
    )
    # Explicit anti-regression: the earlier 568-cell/4-credit hypothesis is
    # incompatible with the reconstructed inherited R180 lineage.
    serialized = wire(result)
    require(
        b'"input":568' not in serialized
        and b'"whole_source_W_origin_exclusions":4' not in serialized
        and b'"new_whole_origin_exclusion_credit":4' not in serialized,
        "reject superseded 568-cell / 4-exclusion hypothesis",
    )


@dataclass(frozen=True)
class Reference:
    pins: tuple[tuple[str, str], ...]
    bounded_result_sha256: str
    sources: tuple[tuple[str, Any, dict[str, Any]], ...]
    context: Any
    compositions: Any
    registry: Any
    lanes: Any


def reconstruct_reference() -> Reference:
    pins = validate_sources()
    (
        bounded, evidence_rows, replay, residual_frontiers,
        closure_results,
    ) = capture_round215()
    lanes = derive_source_w_frontier_lanes(bounded, evidence_rows)
    evidence_by_key = {row["cell_key"]: row for row in evidence_rows}
    require(len(evidence_by_key) == 18_432, "Round215 evidence uniqueness")
    sources, context = reconstruct_h_sources(
        evidence_rows, replay, residual_frontiers, closure_results,
    )
    h_dispositions = {
        source.key: independent_complete_partition(source)[
            "whole_cell_disposition"
        ]
        for _kind, source, _binding in sources
    }
    require(Counter(h_dispositions.values()) == EXPECTED_H_CELL_CENSUS,
            "reference H census")
    compositions = origin_compositions(context, evidence_by_key, h_dispositions)
    registry = {
        item["origin_key"]: item["priority_ordinal"]
        for item in pinned_pretty_json(ROOT / R184_CERTIFICATE)["result"]
        ["priority_registry"]["rows"]
        if item["origin_key"] in set(EXPECTED_KEYS)
    }
    require(set(registry) == set(EXPECTED_KEYS), "R184 priority registry")
    return Reference(
        tuple((row["filename"], row["sha256"]) for row in pins),
        digest(bounded), tuple(sources),
        MappingProxyType(context), MappingProxyType(compositions),
        MappingProxyType(registry),
        MappingProxyType(lanes),
    )


def verify_candidate_dir(candidate: Path, reference: Reference) -> dict[str, Any]:
    candidate = Path(os.path.abspath(os.fspath(candidate)))
    status = candidate.lstat()
    require(
        stat.S_ISDIR(status.st_mode) and not candidate.is_symlink(),
        "candidate regular directory",
    )
    expected_files = {H_LEDGER, ORIGIN_LEDGER, RESULT, RUNTIME_ATTESTATION}
    require(
        {path.name for path in candidate.iterdir()} == expected_files,
        "candidate exact file set",
    )
    pins = [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in reference.pins
    ]
    runtime_attestation_raw = regular_bytes(
        candidate / RUNTIME_ATTESTATION, 64 * 1024 * 1024
    )
    require(
        runtime_attestation_raw == BOOTSTRAP_RUNTIME_ATTESTATION_RAW,
        "candidate runtime attestation byte identity",
    )
    result = strict_json(candidate / RESULT)
    h_rows = canonical_rows(candidate / H_LEDGER)
    origin_rows = canonical_rows(candidate / ORIGIN_LEDGER)
    require(
        len(h_rows) == 688 and len(origin_rows) == 12
        and [row["cell_key"] for row in h_rows]
        == sorted(row["cell_key"] for row in h_rows)
        and [row["origin_key"] for row in origin_rows]
        == list(EXPECTED_KEYS),
        "candidate row count and canonical order",
    )
    sources = reference.sources
    h_by_key: dict[str, str] = {}
    for candidate_row, (source_kind, source, binding) in zip(h_rows, sources):
        require(candidate_row["cell_key"] == source.key, "H row order/source key")
        h_by_key[source.key] = validate_candidate_h_row(
            candidate_row, source_kind, source, binding
        )
    require(
        Counter(h_by_key.values()) == EXPECTED_H_CELL_CENSUS,
        "independent H disposition census",
    )
    hybrid_rows = [
        value for value in h_rows
        if value["source_kind"]
        == "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
    ]
    require(
        len(hybrid_rows) == 8
        and digest([value["cell_key"] for value in hybrid_rows])
        == EXPECTED_HYBRID_CELL_KEYS_SHA256
        and digest([
            value["source_binding"]["Round180_terminal_evidence"]
            for value in hybrid_rows
        ]) == EXPECTED_HYBRID_TERMINAL_ROWS_SHA256
        and digest([
            value["source_binding"]["Round180_terminal_sha256"]
            for value in hybrid_rows
        ]) == EXPECTED_HYBRID_TERMINAL_SHA_LIST_SHA256
        and digest([
            value["H_partition"]["analytic_semantic_projection_sha256"]
            for value in hybrid_rows
        ])
        == EXPECTED_HYBRID_ANALYTIC_SEMANTIC_PROJECTION_SHA_LIST_SHA256,
        "independent hybrid terminal-to-analytic semantic projection binding",
    )
    compositions = reference.compositions
    registry = reference.registry
    h_rows_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for value in h_rows:
        h_rows_by_origin[value["origin_key"]].append(value)
    for ordinal, row in enumerate(origin_rows):
        origin = row["origin_key"]
        validate_origin_row(
            row, ordinal, compositions[origin],
            h_rows_by_origin[origin], registry[origin],
        )
    require(
        digest(list(EXPECTED_KEYS)) == EXPECTED_ALL_KEYS_SHA256
        and digest(list(EXPECTED_EXCLUDED_KEYS))
        == EXPECTED_EXCLUDED_KEYS_SHA256
        and digest(list(EXPECTED_MIXED_KEYS)) == EXPECTED_MIXED_KEYS_SHA256,
        "fixed origin key digests",
    )
    validate_result(
        result, candidate, h_rows, origin_rows, pins, reference.lanes,
    )
    require(
        PRODUCER[:-3] not in sys.modules
        and all(
            "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
            "whole_origin_promotion_producer" != name
            for name in sys.modules
        ),
        "producer modules never imported",
    )
    return {
        "schema": (
            "cm2.round306c30b.source-w-outgoing-h."
            "independent-verification.v1"
        ),
        "status": (
            "PASS_INDEPENDENT_C30B__688_H_CELLS__8_DELTA_FOLLOWUP_H__"
            "2_EXCLUDED__"
            "10_RESOLVED_MIXED__92_TO_80__D02_COMPOSITE_BLOCKED"
        ),
        "candidate_result_sha256": result["result_sha256"],
        "candidate_H_ledger_sha256": file_hash(candidate / H_LEDGER),
        "candidate_origin_ledger_sha256": file_hash(candidate / ORIGIN_LEDGER),
        "input_pin_count": len(pins),
        "Round215_bounded_result_sha256": reference.bounded_result_sha256,
        "H_cell_disposition_census": dict(sorted(EXPECTED_H_CELL_CENSUS.items())),
        "whole_origin_disposition_census": {
            "EXCLUDED": 2, "RESOLVED_MIXED": 10,
        },
        "source_W_remaining_transition": "92->80",
        "outcome_derived_frontier_lane_census": {
            name: len(keys) for name, keys in reference.lanes.items()
        },
        "outcome_derived_frontier_lane_key_digests": {
            name: digest(list(keys))
            for name, keys in reference.lanes.items()
        },
        "outcome_derived_before_92_keys_sha256": digest(sorted(
            key for keys in reference.lanes.values() for key in keys
        )),
        "outcome_derived_after_80_keys_sha256": digest(sorted(
            key for name, keys in reference.lanes.items()
            if name != "outgoing_H" for key in keys
        )),
        "D02": "BLOCKED_BY_80_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "candidate_producer_imported_or_executed": False,
    }


def verify(candidate: Path) -> dict[str, Any]:
    return verify_candidate_dir(candidate, reconstruct_reference())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    try:
        output = verify(arguments.candidate)
    except (Reject, KeyError, OSError, ValueError, TypeError) as error:
        print(wire({
            "schema": (
                "cm2.round306c30b.source-w-outgoing-h."
                "independent-verification.v1"
            ),
            "status": "FAIL_CLOSED",
            "error": str(error),
        }).decode("ascii"))
        return 1
    print(wire(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
