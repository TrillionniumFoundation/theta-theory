#!/usr/bin/env python3
"""Independent fail-closed verifier for the frozen Round208 package.

The Round208 producer is treated only as pinned inert bytes and is never
imported or executed.  The expected certificate is reconstructed before the
candidate is loaded.  Geometry is rebuilt from the independently accepted
Round182 attachment through a separately pinned pre-Round208 evaluator stack;
the direct target, wall word, regional chart, closed rows, origin ledger, and
exact-key joins are reconstructed here without importing Round207.
"""

from __future__ import annotations

import argparse
import ast
import copy
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Callable

from flint import ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round208_source_g_outgoing_direct_signature_materialization"
    "_verification.json"
)
PRODUCER = (
    HERE
    / "cm2_round208_source_g_outgoing_direct_signature_materialization.py"
)
CERTIFICATE = (
    HERE
    / "cm2_round208_source_g_outgoing_direct_signature_materialization"
    "_certificate.json"
)
SCHEMA = (
    "cm2.round208.source-g-outgoing-direct-signature-materialization.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round208.source-g-outgoing-direct-signature-materialization"
    ".verification.v1"
)
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_OUTGOING_W_DIRECT_SIGNATURE_ROWS__"
    "NO_LOWER_DIMENSIONAL_OR_GLOBAL_EXACT_KEY_DISPOSITION"
)
MAX_INPUT_BYTES = 400 * 1024 * 1024
EXPECTED_PRODUCER_SHA256 = (
    "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"
)
EXPECTED_CERTIFICATE_SIZE = 193_161_618
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
)
ROUND208_PREFIX = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization"
)
ROUND208_REPORT = f"{ROUND208_PREFIX}_report.md"
ROUND208_COLD = f"{ROUND208_PREFIX}_cold_replay.md"
ROUND208_MANIFEST = f"{ROUND208_PREFIX}_manifest.sha256"

R207_SOURCE = (
    "cm2_round207_source_g_whole_region_direct_signature_probe.py"
)
R207_REPORT = (
    "cm2_round207_source_g_whole_region_direct_signature_spike_report.md"
)
R207_SOURCE_SHA256 = (
    "0262235b43d74084c37b742b8b4fc435b82e752663d5f816e092faf14e64404a"
)
R207_REPORT_SHA256 = (
    "27b75a8848787fc60b9cd7d0ee57c20ffb96eb4687711adc93597e929f7e90ea"
)
R207_RESULT_SHA256 = (
    "d49b3c9cef0738a03bca8f6477121c7b27aa63e3be8b9ac5854c2521f97448ce"
)
R207_DOCUMENT_SHA256 = (
    "21b388fbd147219f5f52fbdcbe8528b7b9afc06590f2bb997e70042a759f5277"
)

R182_PREFIX = "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
R182_PRODUCER = f"{R182_PREFIX}.py"
R182_CERTIFICATE = f"{R182_PREFIX}_certificate.json"
R182_ATTACHMENT = f"{R182_PREFIX}_rows.json"
R182_VERIFIER = f"{R182_PREFIX}_verifier.py"
R182_VERIFICATION = f"{R182_PREFIX}_verification.json"
R182_REPORT = f"{R182_PREFIX}_report.md"
R182_COLD = f"{R182_PREFIX}_cold_replay.md"
R182_MANIFEST = f"{R182_PREFIX}_manifest.sha256"
R182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
R182_RESULT_SHA256 = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
R182_VERIFICATION_RESULT_SHA256 = (
    "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797"
)
R182_ATTACHMENT_RESULT_SHA256 = (
    "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"
)
R182_PINS = {
    R182_PRODUCER:
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    R182_CERTIFICATE:
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    R182_ATTACHMENT:
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R182_VERIFIER:
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    R182_VERIFICATION:
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    R182_REPORT:
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    R182_COLD:
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}

# The evaluator stack predates Round208.  Every byte is pinned before import.
# Round207 and Round203 are deliberately absent: direct signature fields are
# reconstructed below rather than borrowed from either feasibility probe.
EVALUATOR_PINS = {
    "cm2_round186_source_g_factor_face_probe.py":
        "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64",
    "cm2_round186_source_g_factor_face_spike_report.md":
        "43112bf127a717b1e0ed4403d5c4a3290847a9e575208195354f2aff03562bcf",
    "cm2_round188_source_g_factor_face_boundary_arrangement_probe.py":
        "11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de",
    "cm2_round188_source_g_factor_face_boundary_arrangement_spike_report.md":
        "7b3cf3cd5faaf2e987266fe4ac11740dc2e0c2be0a9a0faf00d2849830a161f6",
    "cm2_round189_source_g_endpoint_p_refinement_probe.py":
        "118f0ec0333562026294ba4667cf7498403c4b6274378921afaa3819ef9323e4",
    "cm2_round191_source_g_stereographic_endpoint_chart_probe.py":
        "b37c0a06a392107d7d859c65ab323cf04c7f06cdd4f51cba59c2049c53f70b9f",
    "cm2_round191_source_g_stereographic_endpoint_chart_spike_report.md":
        "a0b1bfd51b7fcfb23f6f8b77ab20f5f4769bbe2228ff2ca2c20b539f9082aa2d",
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py":
        "f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1",
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_spike_report.md":
        "2f4318f381b79c28c457ce3e2f54e0b6e843c649738789c6d0f95dc8a6332dac",
    "cm2_round198_source_g_outgoing_return_signature_probe.py":
        "59dac5b6e2d79e1612dad51780174f97f71dc1223c01a21b502805d6e9510fbf",
    "cm2_round198_source_g_outgoing_return_signature_spike_report.md":
        "4c7996179638a21fdd4b8b0b15f347ca85b627e5002df20fbce58897223ff358",
}
CELL_SIGNS = {
    "E": ("STRICT_POSITIVE", "STRICT_POSITIVE"),
    "W": ("STRICT_NEGATIVE", "STRICT_NEGATIVE"),
    "N": ("STRICT_POSITIVE", "STRICT_NEGATIVE"),
    "S": ("STRICT_NEGATIVE", "STRICT_POSITIVE"),
}

EXPECTED_LEAVES = 18_324
EXPECTED_CANDIDATES = 36_040
EXPECTED_ORIGINS = 8_268
EXPECTED_PARENTS = 912
EXPECTED_RETAINED_CHILDREN = 11_960
EXPECTED_U2_LEAVES = 88
EXPECTED_U2_ORIGINS = 76
EXPECTED_U2_CANDIDATES = 176
EXPECTED_UNRESOLVED_FACE_INCIDENCES = 18_412
EXPECTED_OUTGOING_VOLUME = Q(861459, 419430400000)
EXPECTED_SOURCE_G_KEY_COUNT = 224_580
EXPECTED_FINAL_FACE_ROWS_SHA256 = (
    "0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396"
)
EXPECTED_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
EXPECTED_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)
EXPECTED_DIRECT_LEAF_ROWS_SHA256 = (
    "4d541ea5bfc4b9db30e78f994e36177dee7112b4c4057c71d6d6376650e20e9e"
)
EXPECTED_ASSIGNMENT_ROWS_SHA256 = (
    "e46fc7e35f2728e48a81e47cd0266cf25c07ad63e534a9fd5b57cc8b0007bb72"
)
EXPECTED_U2_ASSIGNMENT_ROWS_SHA256 = (
    "de20109df8b913a12627b42340ccdacb88e633a5c96cd56bcdd8bafe410fee53"
)
EXPECTED_FACE_METHODS = {
    "ROUND186_BOTH_FACTORS_STRICT_ZERO_ABSENT": 4,
    "ROUND186_ONE_ACTIVE_FACTOR_STRICT_ZERO_ABSENT": 1_172,
    "ROUND186_ONE_ACTIVE_FACTOR_FULL_GRAPH": 1_104,
    "ROUND188_UNIQUE_TWO_ENDPOINT_FACTOR_CURVE": 15_844,
    "ROUND191_STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT": 32,
    "ROUND191_UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE": 256,
}
EXPECTED_LEAF_CLASSES = {
    "CLIPPED_2D_BOUNDARY_1D": 17_308,
    "EMPTY": 608,
    "FULL_2D": 408,
}
EXPECTED_OUTGOING_COUNTS = {
    "E": 9_008,
    "N": 9_012,
    "S": 9_012,
    "W": 9_008,
}


class Round208Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round208Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(
    path: Path,
    expected: str,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    raw = regular_bytes(path, maximum)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"pin:{path.name}",
    )
    return raw


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(token: str) -> None:
    raise Round208Error(f"noninteger JSON number:{token}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str
                and "\x00" not in key
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"JSON key:{path}",
            )
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require(
            "\x00" not in value
            and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"JSON string:{path}",
        )


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round208Error(f"JSON parse:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    require(
        raw == canonical_bytes(value) + b"\n",
        f"canonical JSON:{label}",
    )
    return value


def manifest_entries(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round208Error("manifest ASCII") from exc
    require(text.endswith("\n"), "manifest newline")
    output: dict[str, str] = {}
    for line in text.splitlines():
        pieces = line.split("  ", 1)
        require(len(pieces) == 2, "manifest line")
        value, name = pieces
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value),
            f"manifest digest:{name}",
        )
        require(
            name not in output
            and name not in {"", ".", ".."}
            and "/" not in name
            and "\\" not in name,
            f"manifest name:{name}",
        )
        output[name] = value
    return output


def pin_round182() -> None:
    observed = {
        name: hashlib.sha256(regular_bytes(HERE / name)).hexdigest()
        for name in R182_PINS
    }
    require(observed == R182_PINS, "Round182 package pins")
    manifest_raw = pinned_bytes(
        HERE / R182_MANIFEST,
        R182_MANIFEST_SHA256,
        10_000,
    )
    require(
        manifest_entries(manifest_raw) == R182_PINS,
        "Round182 exact manifest entries",
    )


def unpack(
    packed: list[list[Any]],
    columns: list[str],
) -> list[dict[str, Any]]:
    return [dict(zip(columns, row, strict=True)) for row in packed]


def formal_upstream_chain() -> dict[str, Any]:
    """Exact producer provenance rebuilt from individually pinned inputs."""

    return {
        "Round174_manifest_sha256":
            "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76",
        "Round179_manifest_sha256":
            "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
        "Round182_manifest_sha256": R182_MANIFEST_SHA256,
        "Round182_result_sha256": R182_RESULT_SHA256,
        "Round182_rows_sha256": R182_PINS[R182_ATTACHMENT],
        "Round182_verification_result_sha256":
            R182_VERIFICATION_RESULT_SHA256,
        "Round186_probe_report_sha256":
            EVALUATOR_PINS[
                "cm2_round186_source_g_factor_face_spike_report.md"
            ],
        "Round186_probe_source_sha256":
            EVALUATOR_PINS[
                "cm2_round186_source_g_factor_face_probe.py"
            ],
        "Round188_probe_report_sha256":
            EVALUATOR_PINS[
                "cm2_round188_source_g_factor_face_boundary_arrangement_"
                "spike_report.md"
            ],
        "Round188_probe_source_sha256":
            EVALUATOR_PINS[
                "cm2_round188_source_g_factor_face_boundary_arrangement_"
                "probe.py"
            ],
        "Round189_probe_source_sha256":
            EVALUATOR_PINS[
                "cm2_round189_source_g_endpoint_p_refinement_probe.py"
            ],
        "Round191_probe_report_sha256":
            EVALUATOR_PINS[
                "cm2_round191_source_g_stereographic_endpoint_chart_"
                "spike_report.md"
            ],
        "Round191_probe_source_sha256":
            EVALUATOR_PINS[
                "cm2_round191_source_g_stereographic_endpoint_chart_probe.py"
            ],
        "Round195_probe_report_sha256":
            EVALUATOR_PINS[
                "cm2_round195_source_g_outgoing_assembly_and_u2_order_"
                "spike_report.md"
            ],
        "Round195_probe_source_sha256":
            EVALUATOR_PINS[
                "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py"
            ],
        "Round198_probe_document_sha256":
            "5d3ddddd6445bc364f7b4febd5f81adcb311d085bce636f9ec74c7a54d3711ee",
        "Round198_probe_report_sha256":
            EVALUATOR_PINS[
                "cm2_round198_source_g_outgoing_return_signature_"
                "spike_report.md"
            ],
        "Round198_probe_result_sha256":
            "b6f1660dfe18613ac2b3443c68f56a05f9399d3715c4e7f301fdc0482be459d5",
        "Round198_probe_source_sha256":
            EVALUATOR_PINS[
                "cm2_round198_source_g_outgoing_return_signature_probe.py"
            ],
        "Round203_probe_document_sha256": R207_DOCUMENT_SHA256.replace(
            "21b388fbd147219f5f52fbdcbe8528b7b9afc06590f2bb997e70042a759f5277",
            "7c4e34d146adb5f34637bed6eeae19719bdd477c47c235a9e57384f950f63e48",
        ),
        "Round203_probe_report_sha256":
            "4a9cffcb920d45a27d91cf9accb723bfcbea443ede981e7c2433949ba5981721",
        "Round203_probe_result_sha256":
            "8addc49f7e1c2661fa82525f59765627f7a2cbb322a0b3b55d4ca5c6a04341d9",
        "Round203_probe_source_sha256":
            "86214ed1d37400cdde787c915b4467c7d081e018a7c7522470bdcb5d1abc351f",
        "probe_only_import_before_pin_boundary": True,
    }


def load_evaluator() -> tuple[
    Any,
    Any,
    Any,
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    """Load only pre-Round208 evaluators after all relevant bytes are pinned."""

    require(FLINT_VERSION == "0.9.0", "python-flint version")
    pin_round182()
    for name, expected in EVALUATOR_PINS.items():
        pinned_bytes(HERE / name, expected, 5_000_000)
    require(
        "cm2_round207_source_g_whole_region_direct_signature_probe"
        not in sys.modules
        and "cm2_round208_source_g_outgoing_direct_signature_materialization"
        not in sys.modules,
        "candidate evaluator/producer absent before import",
    )
    evaluator182 = importlib.import_module(
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier"
    )
    require(
        Path(evaluator182.__file__).resolve()
        == (HERE / R182_VERIFIER).resolve(),
        "Round182 independent evaluator identity",
    )
    (
        _source179,
        _certificate182,
        attachment182,
        _certificate182_raw,
        _attachment182_raw,
    ) = evaluator182.load_source_and_documents()
    require(
        attachment182["result_sha256"] == R182_ATTACHMENT_RESULT_SHA256
        and digest(attachment182["result"])
        == R182_ATTACHMENT_RESULT_SHA256,
        "Round182 attachment binding",
    )
    r198 = importlib.import_module(
        "cm2_round198_source_g_outgoing_return_signature_probe"
    )
    r195 = r198.r195
    require(
        Path(r198.__file__).resolve()
        == (
            HERE
            / "cm2_round198_source_g_outgoing_return_signature_probe.py"
        ).resolve()
        and Path(r195.__file__).resolve()
        == (
            HERE
            / "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py"
        ).resolve(),
        "pre-Round208 evaluator identities",
    )
    r174 = evaluator182.r179.r174
    require(
        r195.r191.r189.r188.r186.r179.r174 is r174,
        "shared independently verified Round174 evaluator identity",
    )
    frozen = r174.load_frozen_inputs()
    registry = r174.rebuild_registry(frozen["gate5"])
    global_census = frozen["r169"][
        "source_G_exact_key_coverage_census"
    ]
    require(
        global_census["candidate_exact_key_envelope_count"]
        == EXPECTED_SOURCE_G_KEY_COUNT
        and global_census["global_geometric_exact_key_disposition_count"]
        == 0
        and global_census[
            "keys_without_a_global_geometric_disposition_count"
        ] == EXPECTED_SOURCE_G_KEY_COUNT
        and len(registry["pairs"]) == 448
        and len(registry["patterns"]) == 985,
        "rebuilt registry/global source-G census",
    )
    source = attachment182["result"]
    schemas = source["row_column_schemas"]
    collars = unpack(
        source["collar_occurrence_rows"],
        schemas["collar_occurrence_rows"],
    )
    collar_by_occurrence = {
        row["Round179_occurrence_row_id"]: row for row in collars
    }
    leaves = unpack(
        source["collar_leaf_rows"],
        schemas["collar_leaf_rows"],
    )
    outgoing = [
        row
        for row in leaves
        if Q(row["residual_3d_collar_volume"]) > 0
        and collar_by_occurrence[row["occurrence_row_id"]]["kind"]
        == "OUTGOING"
    ]
    require(
        len(outgoing) == EXPECTED_LEAVES
        and sum((Q(row["coordinate_volume"]) for row in outgoing), Q(0))
        == EXPECTED_OUTGOING_VOLUME,
        "independent outgoing scope",
    )
    del frozen, source, leaves, attachment182
    gc.collect()
    pin_round182()
    return (
        r195,
        r198,
        r174,
        registry,
        outgoing,
        collar_by_occurrence,
        formal_upstream_chain(),
    )


def direct_leaf_signature_base(
    r174: Any,
    chart: str,
    box: Any,
    registry: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    """Independently rebuild every signature field except regional cell."""

    chart_class = r174.rational_chart_class(box)
    if chart_class != "inside":
        return None, ["whole_leaf_not_strictly_inside_source_chart"]
    direct_leaf = r174.atlas.classify_box(chart, box)
    if (
        direct_leaf.classification != "unique_first"
        or direct_leaf.owner_target is None
        or direct_leaf.active_targets != (direct_leaf.owner_target,)
    ):
        return None, [
            "complete_candidate_list_not_unique_first:"
            + direct_leaf.classification
        ]
    target = direct_leaf.owner_target
    complete_candidates = r174.first_hit.candidate_ids(chart)
    if target not in complete_candidates:
        return None, ["direct_target_not_in_complete_candidate_list"]
    qx, qy, ux, uy, s, _source_cosine = r174.atlas.geometry(chart, box)
    record = r174.atlas.root_record(chart, box, target)
    reasons: list[str] = []
    if (
        record.classification != "strict_future_root"
        or record.near is None
        or not bool(record.discriminant > 0)
    ):
        reasons.append("direct_selected_root_not_strict_future")
    elif not bool(record.near < r174.first_hit.arbq(Q(3))):
        reasons.append("direct_return_time_not_below_three")
    if reasons:
        return None, reasons
    radical = record.discriminant.sqrt()
    radius = r174.first_hit.arbq(r174.first_hit.RADIUS[target[0]])
    normal_x = (-radical * ux + record.transverse * uy) / radius
    normal_y = (-radical * uy - record.transverse * ux) / radius
    target_object = r174.first_hit.target_by_id(target)
    center_x, center_y = r174.first_hit.target_center(target_object, s)
    hit_x = center_x + radius * normal_x
    hit_y = center_y + radius * normal_y
    x_events, x_reasons = r174.crossing_events(qx, hit_x, "X")
    y_events, y_reasons = r174.crossing_events(qy, hit_y, "Y")
    reasons.extend(x_reasons)
    reasons.extend(y_reasons)
    ordered = None
    if x_events is not None and y_events is not None:
        ordered, order_reasons = r174.order_events(x_events + y_events)
        reasons.extend(order_reasons)
    if reasons:
        return None, sorted(set(reasons))
    assert ordered is not None
    pattern = tuple(event[0] for event in ordered)
    require(
        len(pattern) <= 8
        and sum(token.startswith("X") for token in pattern) <= 4
        and sum(token.startswith("Y") for token in pattern) <= 4,
        "direct strict wall grammar",
    )
    key = r174.exact_key(chart, target, pattern, registry)
    whole_box_outgoing, whole_box_reasons = r174.outgoing_cell(
        normal_x,
        normal_y,
    )
    return {
        "source_chart": chart,
        "target_lift": target,
        "ordered_integer_wall_events": ordered,
        "signed_wall_word": list(pattern),
        "roof": len(pattern) + 1,
        "official_key_row": key["row"],
        "official_key_ordinal": key["ordinal"],
        "official_key_id": key["identifier"],
        "complete_retained_target_count": len(complete_candidates),
        "whole_leaf_source_chart_classification":
            "STRICTLY_INSIDE_TRUE_SOURCE_CHART",
        "complete_candidate_list_unique_first": True,
        "selected_root_strict_future_nongrazing_below_three": True,
        "wall_endpoints_and_crossing_counts_strict_on_leaf_enclosure": True,
        "wall_event_order_strict_on_leaf_enclosure": True,
        "whole_leaf_box_outgoing_cell": whole_box_outgoing,
        "whole_leaf_box_outgoing_reasons": whole_box_reasons,
    }, []


def materialize(
    r195: Any,
    r198: Any,
    r174: Any,
    registry: dict[str, Any],
    outgoing: list[dict[str, Any]],
    collars: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    require(len(outgoing) == EXPECTED_LEAVES, "outgoing leaf census")
    require(
        sum((Q(row["coordinate_volume"]) for row in outgoing), Q(0))
        == EXPECTED_OUTGOING_VOLUME,
        "outgoing exact volume",
    )

    raw_face_rows: list[dict[str, Any]] = []
    raw_leaf_rows: list[dict[str, Any]] = []
    raw_u2_rows: list[dict[str, Any]] = []
    raw_direct_leaf_rows: list[dict[str, Any]] = []
    raw_assignment_rows: list[dict[str, Any]] = []
    formal_region_rows: list[dict[str, Any]] = []

    for index, raw in enumerate(outgoing, 1):
        collar = collars[raw["occurrence_row_id"]]
        require(
            collar["kind"] == "OUTGOING"
            and collar["target_obstacle"] == "W",
            f"outgoing-W collar:{raw['row_id']}",
        )
        box = r174.atlas.AtlasBox(
            *(Q(value) for value in raw["box"]),
            0,
            raw["row_id"],
        )
        final_faces: dict[str, dict[str, Any]] = {}
        for side, upper, encoded in (
            ("LOWER", False, raw["lower_t_face_status"]),
            ("UPPER", True, raw["upper_t_face_status"]),
        ):
            if encoded == "U":
                face = r195.final_unresolved_face(
                    raw,
                    collar,
                    box,
                    side,
                    upper,
                )
                final_faces[side] = face
                raw_face_rows.append(face)
        lower = (
            r195.side_summary(final_faces["LOWER"])
            if "LOWER" in final_faces
            else r195.decode_round182_face(raw["lower_t_face_status"])
        )
        upper = (
            r195.side_summary(final_faces["UPPER"])
            if "UPPER" in final_faces
            else r195.decode_round182_face(raw["upper_t_face_status"])
        )
        leaf = r195.classify_leaf(raw, collar, box, lower, upper)
        raw_leaf_rows.append(leaf)
        if len(final_faces) == 2:
            raw_u2_rows.append(r195.audit_u2_leaf(
                leaf,
                raw,
                collar,
                box,
                final_faces["LOWER"],
                final_faces["UPPER"],
            ))

        geometry_rows = r198.factor_region_rows(
            leaf,
            raw,
            collar,
            box,
            list(final_faces.values()),
            None,
            set(),
            {},
            None,
        )
        base, reasons = direct_leaf_signature_base(
            r174,
            collar["chart"],
            box,
            registry,
        )
        target_matches = (
            base is not None
            and base["target_lift"] == collar["owner_target"]
        )
        direct_leaf = {
            "leaf_row_id": leaf["leaf_row_id"],
            "origin_row_id": leaf["origin_row_id"],
            "parent_id": collar["parent_id"],
            "chart": collar["chart"],
            "box": raw["box"],
            "candidate_region_count": len(geometry_rows),
            "direct_base_status": (
                "DIRECT_WHOLE_LEAF_BASE_CERTIFIED"
                if base is not None and target_matches
                else "DIRECT_WHOLE_LEAF_BASE_RESIDUAL"
            ),
            "direct_failure_reasons": reasons,
            "direct_target_lift":
                None if base is None else base["target_lift"],
            "frozen_collar_owner_target_for_posthoc_comparison":
                collar["owner_target"],
            "direct_target_matches_frozen_collar": target_matches,
            "frozen_owner_used_as_direct_target_selection_input": False,
            "direct_signature_base": base,
        }
        raw_direct_leaf_rows.append(direct_leaf)
        require(
            base is not None and target_matches and not reasons,
            f"whole-leaf direct signature base:{leaf['leaf_row_id']}",
        )

        face_ids = sorted(
            face["face_row_id"] for face in final_faces.values()
        )
        for geometry in geometry_rows:
            cell = geometry["outgoing_cell"]
            require(
                (
                    geometry["HPLUS_sign"],
                    geometry["HMINUS_sign"],
                )
                == CELL_SIGNS[cell],
                f"strict factor cell:{geometry['candidate_region_id']}",
            )
            signature = {
                "source_chart": base["source_chart"],
                "target_lift": base["target_lift"],
                "ordered_integer_wall_events":
                    base["ordered_integer_wall_events"],
                "signed_wall_word": base["signed_wall_word"],
                "roof": base["roof"],
                "outgoing_cell": cell,
                "target_chart":
                    f"{base['target_lift'].split('[', 1)[0]}:{cell}",
                "official_key_row": base["official_key_row"],
                "official_key_ordinal": base["official_key_ordinal"],
                "official_key_id": base["official_key_id"],
            }
            require(
                signature["official_key_row"]
                == [
                    signature["source_chart"],
                    signature["target_lift"],
                    signature["signed_wall_word"],
                    signature["roof"],
                ],
                f"official key row:{geometry['candidate_region_id']}",
            )
            raw_assignment_rows.append({
                "candidate_region_id": geometry["candidate_region_id"],
                "leaf_row_id": geometry["leaf_row_id"],
                "origin_row_id": geometry["origin_row_id"],
                "parent_id": collar["parent_id"],
                "leaf_classification":
                    geometry["leaf_classification"],
                "F_sign": geometry["F_sign"],
                "HPLUS_sign": geometry["HPLUS_sign"],
                "HMINUS_sign": geometry["HMINUS_sign"],
                "outgoing_cell": cell,
                "whole_region_outgoing_chart_proof":
                    "STRICT_HPLUS_HMINUS_SIGN_PAIR_ON_R195_REGION",
                "containing_leaf_certifies_target_and_wall_fields": True,
                "frozen_owner_used_as_signature_input": False,
                "resolved_anchor_or_component_used_as_signature_input":
                    False,
                "direct_failure_reasons": [],
                "assignment_status":
                    "DIRECT_WHOLE_REGION_SIGNATURE_CERTIFIED",
                "local_return_signature": signature,
                "formal_signature_row_materialized": False,
                "single_point_evaluation_used": False,
                "global_exact_key_disposition_credit": 0,
            })
            formal_region_rows.append(closed_row({
                "region_row_id": geometry["candidate_region_id"],
                "leaf_row_id": geometry["leaf_row_id"],
                "origin_row_id": geometry["origin_row_id"],
                "parent_id": collar["parent_id"],
                "occurrence_row_id": geometry["occurrence_row_id"],
                "retained_child_row_id":
                    leaf["retained_child_row_id"],
                "Round182_leaf_box": raw["box"],
                "Round182_leaf_coordinate_volume":
                    raw["coordinate_volume"],
                "leaf_classification":
                    geometry["leaf_classification"],
                "incident_final_face_row_ids": face_ids,
                "F_sign": geometry["F_sign"],
                "HPLUS_sign": geometry["HPLUS_sign"],
                "HMINUS_sign": geometry["HMINUS_sign"],
                "outgoing_cell": cell,
                "whole_box_factor_C0":
                    geometry["whole_box_factor_C0"],
                "inactive_factor": geometry["inactive_factor"],
                "strict_open_3D_region_exists": True,
                "whole_region_outgoing_chart_proof":
                    "STRICT_HPLUS_HMINUS_SIGN_PAIR",
                "containing_leaf_direct_target_and_wall_proof_row_id":
                    leaf["leaf_row_id"],
                "local_return_signature": signature,
                "complete_retained_target_count":
                    base["complete_retained_target_count"],
                "target_selected_from_complete_list_without_frozen_owner":
                    True,
                "frozen_owner_posthoc_match": True,
                "target_root_strict_future_nongrazing_below_three": True,
                "wall_endpoint_count_and_order_strict_on_leaf": True,
                "resolved_anchor_used": False,
                "parent_signature_guess_used": False,
                "adjacency_or_component_propagation_used": False,
                "single_point_evaluation_used": False,
                "formal_local_open_3D_signature_credit": 1,
                "lower_dimensional_half_open_owner_credit": 0,
                "whole_original_tube_credit": 0,
                "global_exact_key_disposition_credit": 0,
            }))
        if index % 1000 == 0 or index == EXPECTED_LEAVES:
            print(
                f"Round208 materialization {index}/{EXPECTED_LEAVES}",
                file=sys.stderr,
                flush=True,
            )

    raw_face_rows.sort(key=lambda row: row["face_row_id"])
    raw_leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    raw_u2_rows.sort(key=lambda row: row["leaf_row_id"])
    raw_direct_leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    raw_assignment_rows.sort(key=lambda row: row["candidate_region_id"])
    formal_region_rows.sort(key=lambda row: row["region_row_id"])
    require(
        len(raw_face_rows) == EXPECTED_UNRESOLVED_FACE_INCIDENCES
        and len({row["face_row_id"] for row in raw_face_rows})
        == EXPECTED_UNRESOLVED_FACE_INCIDENCES
        and digest(raw_face_rows) == EXPECTED_FINAL_FACE_ROWS_SHA256,
        "final face exact pin",
    )
    require(
        len(raw_leaf_rows) == EXPECTED_LEAVES
        and len({row["leaf_row_id"] for row in raw_leaf_rows})
        == EXPECTED_LEAVES
        and digest(raw_leaf_rows) == EXPECTED_LEAF_ROWS_SHA256,
        "final leaf exact pin",
    )
    require(
        len(raw_u2_rows) == EXPECTED_U2_LEAVES
        and digest(raw_u2_rows) == EXPECTED_U2_ROWS_SHA256,
        "U|U exact pin",
    )
    require(
        digest(raw_direct_leaf_rows)
        == EXPECTED_DIRECT_LEAF_ROWS_SHA256,
        "direct leaf exact pin",
    )
    require(
        len(raw_assignment_rows) == EXPECTED_CANDIDATES
        and len({
            row["candidate_region_id"] for row in raw_assignment_rows
        }) == EXPECTED_CANDIDATES
        and len({
            row["region_row_id"] for row in formal_region_rows
        }) == EXPECTED_CANDIDATES
        and digest(raw_assignment_rows)
        == EXPECTED_ASSIGNMENT_ROWS_SHA256,
        "direct assignment exact pin",
    )
    u2_leaf_ids = {
        row["leaf_row_id"] for row in raw_u2_rows
    }
    require(
        digest([
            row for row in raw_assignment_rows
            if row["leaf_row_id"] in u2_leaf_ids
        ])
        == EXPECTED_U2_ASSIGNMENT_ROWS_SHA256,
        "U|U assignment exact pin",
    )

    face_rows = [closed_row(row) for row in raw_face_rows]
    leaf_rows = [
        closed_row({
            **row,
            "formal_final_geometry_row_materialized": True,
        })
        for row in raw_leaf_rows
    ]
    u2_rows = [
        closed_row({
            **row,
            "both_strict_sides_formally_signature_materialized": True,
        })
        for row in raw_u2_rows
    ]
    direct_leaf_rows = [
        closed_row({
            **row,
            "formal_direct_signature_base_materialized": True,
            "formal_local_credit": 1,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        for row in raw_direct_leaf_rows
    ]
    return (
        face_rows,
        leaf_rows,
        u2_rows,
        direct_leaf_rows,
        formal_region_rows,
        raw_assignment_rows,
    )


def build_origin_rows(
    leaf_rows: list[dict[str, Any]],
    region_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    leaves: dict[str, list[dict[str, Any]]] = defaultdict(list)
    regions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in leaf_rows:
        leaves[row["origin_row_id"]].append(row)
    for row in region_rows:
        regions[row["origin_row_id"]].append(row)
    output: list[dict[str, Any]] = []
    for origin_id in sorted(leaves):
        origin_leaves = leaves[origin_id]
        origin_regions = regions[origin_id]
        require(
            len({row["parent_id"] for row in origin_regions}) == 1,
            f"origin parent identity:{origin_id}",
        )
        output.append(closed_row({
            "origin_row_id": origin_id,
            "parent_id": origin_regions[0]["parent_id"],
            "leaf_row_count": len(origin_leaves),
            "leaf_row_ids": sorted(
                row["leaf_row_id"] for row in origin_leaves
            ),
            "strict_open_3D_signature_region_count":
                len(origin_regions),
            "strict_open_3D_signature_region_row_ids": sorted(
                row["region_row_id"] for row in origin_regions
            ),
            "exact_outer_coordinate_volume": qstr(sum(
                (Q(row["coordinate_volume"]) for row in origin_leaves),
                Q(0),
            )),
            "leaf_classification_count": dict(sorted(Counter(
                row["final_graph_classification"]
                for row in origin_leaves
            ).items())),
            "distinct_local_signature_count": len({
                digest(row["local_return_signature"])
                for row in origin_regions
            }),
            "all_leaves_have_direct_signature_bases": True,
            "all_strict_open_3D_regions_have_formal_signatures": True,
            "formal_local_open_3D_origin_coverage_credit": 1,
            "lower_dimensional_half_open_ownership_materialized": False,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        len(output) == EXPECTED_ORIGINS
        and sum(
            (Q(row["exact_outer_coordinate_volume"]) for row in output),
            Q(0),
        ) == EXPECTED_OUTGOING_VOLUME
        and all(
            row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in output
        ),
        "origin local completion",
    )
    return output


def build_key_rows(
    region_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in region_rows:
        grouped[row["local_return_signature"]["official_key_id"]].append(row)
    output: list[dict[str, Any]] = []
    for key_id, rows in grouped.items():
        signature = rows[0]["local_return_signature"]
        require(
            all(
                row["local_return_signature"]["official_key_id"] == key_id
                and row["local_return_signature"]["official_key_ordinal"]
                == signature["official_key_ordinal"]
                and row["local_return_signature"]["official_key_row"]
                == signature["official_key_row"]
                for row in rows
            ),
            f"local exact-key join:{key_id}",
        )
        output.append(closed_row({
            "official_key_id": key_id,
            "official_key_ordinal":
                signature["official_key_ordinal"],
            "official_key_row": signature["official_key_row"],
            "local_region_occurrence_count": len(rows),
            "local_region_row_ids": sorted(
                row["region_row_id"] for row in rows
            ),
            "join_cardinality_per_local_region": 1,
            "formal_local_join_materialized": True,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    output.sort(key=lambda row: row["official_key_ordinal"])
    require(
        len(output) == 24
        and sum(
            row["local_region_occurrence_count"] for row in output
        ) == EXPECTED_CANDIDATES
        and all(
            row["global_exact_key_disposition_credit"] == 0
            for row in output
        ),
        "24 local exact-key joins",
    )
    return output


def build_result(producer_sha256: str) -> dict[str, Any]:
    ctx.prec = 256
    print("Round208 pinning evaluator chain", file=sys.stderr, flush=True)
    (
        r195,
        r198,
        r174,
        registry,
        outgoing,
        collars,
        upstream,
    ) = load_evaluator()
    print("Round208 rebuilding all formal rows", file=sys.stderr, flush=True)
    (
        face_rows,
        leaf_rows,
        u2_rows,
        direct_leaf_rows,
        region_rows,
        raw_assignment_rows,
    ) = materialize(
        r195,
        r198,
        r174,
        registry,
        outgoing,
        collars,
    )
    origin_rows = build_origin_rows(leaf_rows, region_rows)
    key_rows = build_key_rows(region_rows)

    parent_ids = {row["parent_id"] for row in region_rows}
    retained_ids = {
        row["retained_child_row_id"] for row in region_rows
    }
    u2_leaf_ids = {row["leaf_row_id"] for row in u2_rows}
    u2_region_rows = [
        row for row in region_rows if row["leaf_row_id"] in u2_leaf_ids
    ]
    signatures = [
        row["local_return_signature"] for row in region_rows
    ]
    signature_digests = sorted({digest(row) for row in signatures})
    exact_key_ids = sorted({
        row["official_key_id"] for row in signatures
    })
    exact_key_ordinals = sorted({
        row["official_key_ordinal"] for row in signatures
    })
    face_methods = Counter(
        row["final_method"] for row in face_rows
    )
    leaf_classes = Counter(
        row["final_graph_classification"] for row in leaf_rows
    )
    outgoing_counts = Counter(
        row["outgoing_cell"] for row in region_rows
    )
    word_lengths = Counter(
        len(row["signed_wall_word"]) for row in signatures
    )
    complete_target_counts = Counter(
        row["direct_signature_base"]["complete_retained_target_count"]
        for row in direct_leaf_rows
    )
    require(
        len(parent_ids) == EXPECTED_PARENTS
        and len(retained_ids) == EXPECTED_RETAINED_CHILDREN
        and len(u2_region_rows) == EXPECTED_U2_CANDIDATES
        and len({row["origin_row_id"] for row in u2_rows})
        == EXPECTED_U2_ORIGINS
        and dict(sorted(face_methods.items())) == EXPECTED_FACE_METHODS
        and dict(sorted(leaf_classes.items())) == EXPECTED_LEAF_CLASSES
        and dict(sorted(outgoing_counts.items())) == EXPECTED_OUTGOING_COUNTS
        and word_lengths == {0: 30_080, 1: 5_960}
        and complete_target_counts == {57: EXPECTED_LEAVES}
        and all(
            row["direct_base_status"]
            == "DIRECT_WHOLE_LEAF_BASE_CERTIFIED"
            and row["direct_target_matches_frozen_collar"] is True
            and row["direct_failure_reasons"] == []
            for row in direct_leaf_rows
        )
        and len(signature_digests) == 52
        and len(exact_key_ids) == len(exact_key_ordinals) == 24,
        "formal census pins",
    )

    return {
        "status": STATUS,
        "formal_input_binding": {
            "Round182_manifest_sha256": R182_MANIFEST_SHA256,
            "Round182_result_sha256": R182_RESULT_SHA256,
            "Round182_verification_result_sha256":
                R182_VERIFICATION_RESULT_SHA256,
            "Round207_source_sha256": R207_SOURCE_SHA256,
            "Round207_report_sha256": R207_REPORT_SHA256,
            "Round207_probe_result_sha256": R207_RESULT_SHA256,
            "Round207_probe_document_sha256": R207_DOCUMENT_SHA256,
            "Round207_used_as_producer_side_evaluator": True,
            "independent_verifier_must_not_import_Round207": True,
            "upstream_chain": upstream,
        },
        "formal_scope_contract": {
            "source_obstacle": "G",
            "target_obstacle": "W",
            "Round182_outgoing_residual_leaf_count": EXPECTED_LEAVES,
            "outgoing_origin_count": EXPECTED_ORIGINS,
            "parent_count": len(parent_ids),
            "retained_child_count": len(retained_ids),
            "exact_outer_coordinate_volume": qstr(
                EXPECTED_OUTGOING_VOLUME
            ),
            "strict_open_3D_candidate_region_count":
                EXPECTED_CANDIDATES,
            "formal_local_open_3D_signature_row_count":
                len(region_rows),
            "all_local_open_3D_signature_rows_materialized": True,
            "lower_dimensional_half_open_ownership_materialized": False,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_final_factor_face_ledger": {
            "row_count": len(face_rows),
            "rows_sha256": digest(face_rows),
            "rows": face_rows,
            "method_count": dict(sorted(face_methods.items())),
            "raw_Round195_rows_sha256":
                EXPECTED_FINAL_FACE_ROWS_SHA256,
            "all_target_normal_zeros_excluded": True,
            "local_face_residual_count": 0,
        },
        "formal_leaf_geometry_ledger": {
            "row_count": len(leaf_rows),
            "rows_sha256": digest(leaf_rows),
            "rows": leaf_rows,
            "classification_count": dict(sorted(leaf_classes.items())),
            "raw_Round195_rows_sha256": EXPECTED_LEAF_ROWS_SHA256,
            "strict_open_3D_candidate_region_count":
                EXPECTED_CANDIDATES,
            "local_geometric_residual_leaf_count": 0,
        },
        "formal_direct_leaf_signature_base_ledger": {
            "row_count": len(direct_leaf_rows),
            "rows_sha256": digest(direct_leaf_rows),
            "rows": direct_leaf_rows,
            "raw_Round207_rows_sha256":
                EXPECTED_DIRECT_LEAF_ROWS_SHA256,
            "complete_target_list_size_histogram":
                {
                    str(key): value
                    for key, value in sorted(
                        complete_target_counts.items()
                    )
                },
            "all_direct_targets_match_frozen_collars_posthoc": True,
            "all_target_and_wall_fields_strict_on_whole_leaf": True,
            "direct_residual_count": 0,
        },
        "formal_local_open_3D_signature_ledger": {
            "row_count": len(region_rows),
            "rows_sha256": digest(region_rows),
            "rows": region_rows,
            "raw_Round207_assignment_rows_sha256":
                digest(raw_assignment_rows),
            "distinct_local_signature_count":
                len(signature_digests),
            "distinct_local_signature_digests_sha256":
                digest(signature_digests),
            "involved_exact_key_count": len(exact_key_ids),
            "involved_exact_key_ids_sha256": digest(exact_key_ids),
            "involved_exact_key_ordinals_sha256":
                digest(exact_key_ordinals),
            "signed_wall_word_length_count":
                {
                    str(key): value
                    for key, value in sorted(word_lengths.items())
                },
            "outgoing_cell_count":
                dict(sorted(outgoing_counts.items())),
            "formal_local_open_3D_signature_credit":
                len(region_rows),
            "lower_dimensional_half_open_owner_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_U_pipe_U_side_specific_ledger": {
            "leaf_row_count": len(u2_rows),
            "rows_sha256": digest(u2_rows),
            "rows": u2_rows,
            "raw_Round195_rows_sha256": EXPECTED_U2_ROWS_SHA256,
            "side_specific_region_row_count": len(u2_region_rows),
            "side_specific_region_rows_sha256":
                digest(u2_region_rows),
            "raw_Round207_assignment_rows_sha256":
                EXPECTED_U2_ASSIGNMENT_ROWS_SHA256,
            "both_sides_formally_materialized_leaf_count":
                EXPECTED_U2_LEAVES,
            "cross_t_signature_copy_used": False,
        },
        "formal_origin_local_completion_ledger": {
            "row_count": len(origin_rows),
            "rows_sha256": digest(origin_rows),
            "rows": origin_rows,
            "formal_local_open_3D_origin_coverage_credit":
                len(origin_rows),
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_exact_key_local_join_ledger": {
            "row_count": len(key_rows),
            "rows_sha256": digest(key_rows),
            "rows": key_rows,
            "all_local_regions_join_exactly_one_immutable_key": True,
            "no_global_exact_key_fibre_exhausted": True,
            "global_source_G_exact_key_fibre_count":
                EXPECTED_SOURCE_G_KEY_COUNT,
            "global_source_G_exact_key_disposition_count": 0,
        },
        "exact_dimension_and_volume_conservation": {
            "input_leaf_count": EXPECTED_LEAVES,
            "input_exact_outer_coordinate_volume":
                qstr(EXPECTED_OUTGOING_VOLUME),
            "formal_output_leaf_cover_count": EXPECTED_LEAVES,
            "formal_output_exact_outer_coordinate_volume":
                qstr(EXPECTED_OUTGOING_VOLUME),
            "strict_open_3D_region_count": EXPECTED_CANDIDATES,
            "individual_curved_region_volumes_not_summed": True,
            "each_leaf_outer_volume_counted_exactly_once": True,
            "2D_1D_0D_strata_have_zero_ambient_3D_volume": True,
            "integer_leaf_delta": 0,
            "exact_coordinate_volume_delta": "0",
        },
        "method_independence_contract": {
            "complete_target_list_recomputed_per_leaf": True,
            "frozen_owner_used_only_posthoc": True,
            "resolved_signature_anchor_used": False,
            "parent_signature_base_used": False,
            "Round198_adjacency_assignment_used": False,
            "Round203_component_assignment_used": False,
            "single_point_evaluation_used": False,
            "target_and_wall_fields_certified_on_containing_leaf": True,
            "outgoing_chart_certified_on_each_strict_region": True,
        },
        "formal_local_materialization_and_strict_nonpromotion": {
            "formal_local_open_3D_signature_count":
                EXPECTED_CANDIDATES,
            "formal_local_open_3D_origin_coverage_count":
                EXPECTED_ORIGINS,
            "separate_wall_G_local_replacement_is_out_of_scope": True,
            "lower_dimensional_half_open_ownership": "NOT_MATERIALIZED",
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions":
                f"0/{EXPECTED_SOURCE_G_KEY_COUNT}",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "independently verify every row, join with the separately "
            "formalized wall-G local replacement, then materialize all "
            "lower-dimensional half-open owners before any complete "
            "global exact-key fibre coverage/exclusion claim",
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_flint_version": FLINT_VERSION,
            "effective_Arb_precision_bits": ctx.prec,
            "producer_side_evaluator":
                "pinned Round207 probe chain rooted in verified Round182",
            "formal_upstream_files_modified": False,
        },
    }


def audit_closed_rows(
    rows: list[dict[str, Any]],
    *,
    id_key: str,
    label: str,
) -> set[str]:
    require(type(rows) is list and rows, f"{label}:nonempty rows")
    identifiers: set[str] = set()
    for row in rows:
        require(type(row) is dict, f"{label}:row object")
        identifier = row[id_key]
        require(
            type(identifier) is str and identifier not in identifiers,
            f"{label}:unique identifier",
        )
        identifiers.add(identifier)
        payload = {
            key: value
            for key, value in row.items()
            if key != "row_sha256"
        }
        require(
            set(row) == {*payload, "row_sha256"}
            and row["row_sha256"] == digest(payload),
            f"{label}:closed row",
        )
    return identifiers


def audit_exact_key_value(
    value: Any,
    key_name: str,
    expected: Any,
) -> int:
    count = 0
    if type(value) is dict:
        for key, child in value.items():
            if key == key_name:
                require(
                    type(child) is type(expected) and child == expected,
                    f"recursive strict value:{key_name}",
                )
                count += 1
            count += audit_exact_key_value(child, key_name, expected)
    elif type(value) is list:
        for child in value:
            count += audit_exact_key_value(child, key_name, expected)
    return count


def audit_reconstructed_result(result: dict[str, Any]) -> dict[str, int]:
    """Cross-audit the rebuilt object without consulting the candidate."""

    require(
        set(result) == {
            "status",
            "formal_input_binding",
            "formal_scope_contract",
            "formal_final_factor_face_ledger",
            "formal_leaf_geometry_ledger",
            "formal_direct_leaf_signature_base_ledger",
            "formal_local_open_3D_signature_ledger",
            "formal_U_pipe_U_side_specific_ledger",
            "formal_origin_local_completion_ledger",
            "formal_exact_key_local_join_ledger",
            "exact_dimension_and_volume_conservation",
            "method_independence_contract",
            "formal_local_materialization_and_strict_nonpromotion",
            "next_core_gate",
            "provenance",
        },
        "expected result exact top-level keys",
    )
    require(result["status"] == STATUS, "formal status")

    binding = result["formal_input_binding"]
    require(
        binding["Round182_manifest_sha256"] == R182_MANIFEST_SHA256
        and binding["Round182_result_sha256"] == R182_RESULT_SHA256
        and binding["Round182_verification_result_sha256"]
        == R182_VERIFICATION_RESULT_SHA256
        and binding["Round207_source_sha256"] == R207_SOURCE_SHA256
        and binding["Round207_report_sha256"] == R207_REPORT_SHA256
        and binding["Round207_probe_result_sha256"] == R207_RESULT_SHA256
        and binding["Round207_probe_document_sha256"]
        == R207_DOCUMENT_SHA256
        and binding["Round207_used_as_producer_side_evaluator"] is True
        and binding["independent_verifier_must_not_import_Round207"] is True
        and binding["upstream_chain"] == formal_upstream_chain(),
        "formal input binding",
    )

    scope = result["formal_scope_contract"]
    require(
        scope["source_obstacle"] == "G"
        and scope["target_obstacle"] == "W"
        and scope["Round182_outgoing_residual_leaf_count"]
        == EXPECTED_LEAVES
        and scope["outgoing_origin_count"] == EXPECTED_ORIGINS
        and scope["parent_count"] == EXPECTED_PARENTS
        and scope["retained_child_count"] == EXPECTED_RETAINED_CHILDREN
        and scope["exact_outer_coordinate_volume"]
        == qstr(EXPECTED_OUTGOING_VOLUME)
        and scope["strict_open_3D_candidate_region_count"]
        == EXPECTED_CANDIDATES
        and scope["formal_local_open_3D_signature_row_count"]
        == EXPECTED_CANDIDATES
        and scope["all_local_open_3D_signature_rows_materialized"] is True
        and scope["lower_dimensional_half_open_ownership_materialized"]
        is False
        and scope["whole_original_tube_credit"] == 0
        and scope["global_exact_key_disposition_credit"] == 0,
        "formal scope contract",
    )

    face = result["formal_final_factor_face_ledger"]
    face_rows = face["rows"]
    face_ids = audit_closed_rows(
        face_rows,
        id_key="face_row_id",
        label="final factor face",
    )
    require(
        len(face_ids) == EXPECTED_UNRESOLVED_FACE_INCIDENCES
        and face["row_count"] == EXPECTED_UNRESOLVED_FACE_INCIDENCES
        and face["rows_sha256"] == digest(face_rows)
        and face["method_count"] == EXPECTED_FACE_METHODS
        and face["raw_Round195_rows_sha256"]
        == EXPECTED_FINAL_FACE_ROWS_SHA256
        and face["all_target_normal_zeros_excluded"] is True
        and face["local_face_residual_count"] == 0,
        "formal final factor-face ledger",
    )

    leaf = result["formal_leaf_geometry_ledger"]
    leaf_rows = leaf["rows"]
    leaf_ids = audit_closed_rows(
        leaf_rows,
        id_key="leaf_row_id",
        label="leaf geometry",
    )
    require(
        len(leaf_ids) == EXPECTED_LEAVES
        and leaf["row_count"] == EXPECTED_LEAVES
        and leaf["rows_sha256"] == digest(leaf_rows)
        and leaf["classification_count"] == EXPECTED_LEAF_CLASSES
        and leaf["raw_Round195_rows_sha256"] == EXPECTED_LEAF_ROWS_SHA256
        and leaf["strict_open_3D_candidate_region_count"]
        == EXPECTED_CANDIDATES
        and leaf["local_geometric_residual_leaf_count"] == 0
        and all(
            row["formal_final_geometry_row_materialized"] is True
            for row in leaf_rows
        ),
        "formal leaf geometry ledger",
    )

    direct = result["formal_direct_leaf_signature_base_ledger"]
    direct_rows = direct["rows"]
    direct_ids = audit_closed_rows(
        direct_rows,
        id_key="leaf_row_id",
        label="direct leaf signature base",
    )
    require(
        direct_ids == leaf_ids
        and direct["row_count"] == EXPECTED_LEAVES
        and direct["rows_sha256"] == digest(direct_rows)
        and direct["raw_Round207_rows_sha256"]
        == EXPECTED_DIRECT_LEAF_ROWS_SHA256
        and direct["complete_target_list_size_histogram"]
        == {"57": EXPECTED_LEAVES}
        and direct["all_direct_targets_match_frozen_collars_posthoc"] is True
        and direct["all_target_and_wall_fields_strict_on_whole_leaf"] is True
        and direct["direct_residual_count"] == 0
        and all(
            row["direct_base_status"]
            == "DIRECT_WHOLE_LEAF_BASE_CERTIFIED"
            and row["direct_failure_reasons"] == []
            and row["direct_target_matches_frozen_collar"] is True
            and row["frozen_owner_used_as_direct_target_selection_input"]
            is False
            and row["formal_direct_signature_base_materialized"] is True
            and row["formal_local_credit"] == 1
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            and row["direct_signature_base"]["complete_retained_target_count"]
            == 57
            for row in direct_rows
        ),
        "formal direct leaf signature-base ledger",
    )

    region = result["formal_local_open_3D_signature_ledger"]
    region_rows = region["rows"]
    region_ids = audit_closed_rows(
        region_rows,
        id_key="region_row_id",
        label="strict open 3D signature region",
    )
    require(
        len(region_ids) == EXPECTED_CANDIDATES
        and region["row_count"] == EXPECTED_CANDIDATES
        and region["rows_sha256"] == digest(region_rows)
        and region["raw_Round207_assignment_rows_sha256"]
        == EXPECTED_ASSIGNMENT_ROWS_SHA256
        and region["distinct_local_signature_count"] == 52
        and region["involved_exact_key_count"] == 24
        and region["signed_wall_word_length_count"]
        == {"0": 30_080, "1": 5_960}
        and region["outgoing_cell_count"] == EXPECTED_OUTGOING_COUNTS
        and region["formal_local_open_3D_signature_credit"]
        == EXPECTED_CANDIDATES
        and region["lower_dimensional_half_open_owner_credit"] == 0
        and region["whole_original_tube_credit"] == 0
        and region["global_exact_key_disposition_credit"] == 0,
        "formal local open-3D signature ledger summaries",
    )
    require(
        all(
            row["leaf_row_id"] in leaf_ids
            and set(row["incident_final_face_row_ids"]) <= face_ids
            and (
                row["HPLUS_sign"],
                row["HMINUS_sign"],
            ) == CELL_SIGNS[row["outgoing_cell"]]
            and row["strict_open_3D_region_exists"] is True
            and row["whole_region_outgoing_chart_proof"]
            == "STRICT_HPLUS_HMINUS_SIGN_PAIR"
            and row["complete_retained_target_count"] == 57
            and row["target_selected_from_complete_list_without_frozen_owner"]
            is True
            and row["frozen_owner_posthoc_match"] is True
            and row["target_root_strict_future_nongrazing_below_three"]
            is True
            and row["wall_endpoint_count_and_order_strict_on_leaf"] is True
            and row["resolved_anchor_used"] is False
            and row["parent_signature_guess_used"] is False
            and row["adjacency_or_component_propagation_used"] is False
            and row["single_point_evaluation_used"] is False
            and row["formal_local_open_3D_signature_credit"] == 1
            and row["lower_dimensional_half_open_owner_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            and row["local_return_signature"]["outgoing_cell"]
            == row["outgoing_cell"]
            and row["local_return_signature"]["target_chart"]
            == (
                row["local_return_signature"]["target_lift"].split("[", 1)[0]
                + ":"
                + row["outgoing_cell"]
            )
            and row["local_return_signature"]["official_key_row"]
            == [
                row["local_return_signature"]["source_chart"],
                row["local_return_signature"]["target_lift"],
                row["local_return_signature"]["signed_wall_word"],
                row["local_return_signature"]["roof"],
            ]
            for row in region_rows
        ),
        "formal local open-3D signature rows",
    )
    signature_digests = sorted({
        digest(row["local_return_signature"]) for row in region_rows
    })
    exact_key_ids = sorted({
        row["local_return_signature"]["official_key_id"]
        for row in region_rows
    })
    exact_key_ordinals = sorted({
        row["local_return_signature"]["official_key_ordinal"]
        for row in region_rows
    })
    require(
        region["distinct_local_signature_digests_sha256"]
        == digest(signature_digests)
        and region["involved_exact_key_ids_sha256"]
        == digest(exact_key_ids)
        and region["involved_exact_key_ordinals_sha256"]
        == digest(exact_key_ordinals),
        "signature and exact-key census digests",
    )

    u2 = result["formal_U_pipe_U_side_specific_ledger"]
    u2_rows = u2["rows"]
    u2_ids = audit_closed_rows(
        u2_rows,
        id_key="leaf_row_id",
        label="U-pipe-U leaf",
    )
    u2_region_rows = [
        row for row in region_rows if row["leaf_row_id"] in u2_ids
    ]
    require(
        len(u2_ids) == EXPECTED_U2_LEAVES
        and u2_ids <= leaf_ids
        and u2["leaf_row_count"] == EXPECTED_U2_LEAVES
        and u2["rows_sha256"] == digest(u2_rows)
        and u2["raw_Round195_rows_sha256"] == EXPECTED_U2_ROWS_SHA256
        and u2["side_specific_region_row_count"]
        == EXPECTED_U2_CANDIDATES
        and u2["side_specific_region_rows_sha256"]
        == digest(u2_region_rows)
        and u2["raw_Round207_assignment_rows_sha256"]
        == EXPECTED_U2_ASSIGNMENT_ROWS_SHA256
        and u2["both_sides_formally_materialized_leaf_count"]
        == EXPECTED_U2_LEAVES
        and u2["cross_t_signature_copy_used"] is False
        and len(u2_region_rows) == EXPECTED_U2_CANDIDATES
        and len({row["origin_row_id"] for row in u2_rows})
        == EXPECTED_U2_ORIGINS
        and all(
            row["both_strict_sides_formally_signature_materialized"] is True
            for row in u2_rows
        ),
        "formal U-pipe-U side-specific ledger",
    )

    origin = result["formal_origin_local_completion_ledger"]
    origin_rows = origin["rows"]
    origin_ids = audit_closed_rows(
        origin_rows,
        id_key="origin_row_id",
        label="origin local completion",
    )
    origin_leaf_ids = [
        leaf_id
        for row in origin_rows
        for leaf_id in row["leaf_row_ids"]
    ]
    origin_region_ids = [
        region_id
        for row in origin_rows
        for region_id in row["strict_open_3D_signature_region_row_ids"]
    ]
    require(
        len(origin_ids) == EXPECTED_ORIGINS
        and origin["row_count"] == EXPECTED_ORIGINS
        and origin["rows_sha256"] == digest(origin_rows)
        and origin["formal_local_open_3D_origin_coverage_credit"]
        == EXPECTED_ORIGINS
        and len(origin_leaf_ids) == EXPECTED_LEAVES
        and len(set(origin_leaf_ids)) == EXPECTED_LEAVES
        and set(origin_leaf_ids) == leaf_ids
        and len(origin_region_ids) == EXPECTED_CANDIDATES
        and len(set(origin_region_ids)) == EXPECTED_CANDIDATES
        and set(origin_region_ids) == region_ids
        and all(
            row["all_leaves_have_direct_signature_bases"] is True
            and row["all_strict_open_3D_regions_have_formal_signatures"]
            is True
            and row["formal_local_open_3D_origin_coverage_credit"] == 1
            and row["lower_dimensional_half_open_ownership_materialized"]
            is False
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in origin_rows
        ),
        "formal origin-local completion ledger",
    )

    join = result["formal_exact_key_local_join_ledger"]
    join_rows = join["rows"]
    join_ids = audit_closed_rows(
        join_rows,
        id_key="official_key_id",
        label="exact-key local join",
    )
    joined_region_ids = [
        region_id
        for row in join_rows
        for region_id in row["local_region_row_ids"]
    ]
    require(
        len(join_ids) == 24
        and set(exact_key_ids) == join_ids
        and join["row_count"] == 24
        and join["rows_sha256"] == digest(join_rows)
        and join["all_local_regions_join_exactly_one_immutable_key"] is True
        and join["no_global_exact_key_fibre_exhausted"] is True
        and join["global_source_G_exact_key_fibre_count"]
        == EXPECTED_SOURCE_G_KEY_COUNT
        and join["global_source_G_exact_key_disposition_count"] == 0
        and len(joined_region_ids) == EXPECTED_CANDIDATES
        and len(set(joined_region_ids)) == EXPECTED_CANDIDATES
        and set(joined_region_ids) == region_ids
        and all(
            row["local_region_occurrence_count"]
            == len(row["local_region_row_ids"])
            and row["join_cardinality_per_local_region"] == 1
            and row["formal_local_join_materialized"] is True
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0
            for row in join_rows
        ),
        "formal exact-key local joins",
    )

    conservation = result["exact_dimension_and_volume_conservation"]
    require(
        conservation["input_leaf_count"] == EXPECTED_LEAVES
        and conservation["input_exact_outer_coordinate_volume"]
        == qstr(EXPECTED_OUTGOING_VOLUME)
        and conservation["formal_output_leaf_cover_count"] == EXPECTED_LEAVES
        and conservation["formal_output_exact_outer_coordinate_volume"]
        == qstr(EXPECTED_OUTGOING_VOLUME)
        and conservation["strict_open_3D_region_count"]
        == EXPECTED_CANDIDATES
        and conservation["individual_curved_region_volumes_not_summed"]
        is True
        and conservation["each_leaf_outer_volume_counted_exactly_once"]
        is True
        and conservation["2D_1D_0D_strata_have_zero_ambient_3D_volume"]
        is True
        and conservation["integer_leaf_delta"] == 0
        and conservation["exact_coordinate_volume_delta"] == "0",
        "exact dimension and volume conservation",
    )
    require(
        result["method_independence_contract"] == {
            "complete_target_list_recomputed_per_leaf": True,
            "frozen_owner_used_only_posthoc": True,
            "resolved_signature_anchor_used": False,
            "parent_signature_base_used": False,
            "Round198_adjacency_assignment_used": False,
            "Round203_component_assignment_used": False,
            "single_point_evaluation_used": False,
            "target_and_wall_fields_certified_on_containing_leaf": True,
            "outgoing_chart_certified_on_each_strict_region": True,
        },
        "method independence contract",
    )
    nonpromotion = result[
        "formal_local_materialization_and_strict_nonpromotion"
    ]
    require(
        nonpromotion["formal_local_open_3D_signature_count"]
        == EXPECTED_CANDIDATES
        and nonpromotion["formal_local_open_3D_origin_coverage_count"]
        == EXPECTED_ORIGINS
        and nonpromotion["separate_wall_G_local_replacement_is_out_of_scope"]
        is True
        and nonpromotion["lower_dimensional_half_open_ownership"]
        == "NOT_MATERIALIZED"
        and nonpromotion["whole_original_tube_credit"] == 0
        and nonpromotion["global_exact_key_disposition_credit"] == 0
        and nonpromotion["source_G_global_exact_key_dispositions"]
        == f"0/{EXPECTED_SOURCE_G_KEY_COUNT}"
        and nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["global_Gate5_fields"] == "10/18"
        and nonpromotion["global_complete_18_field_blocks"] == 0
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "strict nonpromotion",
    )
    require(
        result["provenance"]["schema"] == SCHEMA
        and result["provenance"]["producer_sha256"]
        == EXPECTED_PRODUCER_SHA256
        and result["provenance"]["python_flint_version"] == FLINT_VERSION
        and result["provenance"]["effective_Arb_precision_bits"] == 192
        and result["provenance"]["formal_upstream_files_modified"] is False,
        "formal provenance",
    )

    global_zero_count = audit_exact_key_value(
        result, "global_exact_key_disposition_credit", 0
    )
    whole_zero_count = audit_exact_key_value(
        result, "whole_original_tube_credit", 0
    )
    lower_credit_zero_count = audit_exact_key_value(
        result, "lower_dimensional_half_open_owner_credit", 0
    )
    lower_ownership_false_count = audit_exact_key_value(
        result, "lower_dimensional_half_open_ownership_materialized", False
    )
    fibre_false_count = audit_exact_key_value(
        result, "global_exact_key_fibre_exhausted", False
    )
    require(
        global_zero_count == 99_484
        and whole_zero_count == 62_636
        and lower_credit_zero_count == 36_041
        and lower_ownership_false_count == 8_269
        and fibre_false_count == 24,
        "recursive strict nonpromotion occurrence census",
    )
    return {
        "closed_row_count": (
            EXPECTED_UNRESOLVED_FACE_INCIDENCES
            + EXPECTED_LEAVES
            + EXPECTED_LEAVES
            + EXPECTED_CANDIDATES
            + EXPECTED_U2_LEAVES
            + EXPECTED_ORIGINS
            + 24
        ),
        "final_factor_face_row_count": len(face_ids),
        "leaf_geometry_row_count": len(leaf_ids),
        "direct_leaf_signature_base_row_count": len(direct_ids),
        "strict_open_3D_signature_row_count": len(region_ids),
        "U_pipe_U_leaf_count": len(u2_ids),
        "U_pipe_U_side_specific_region_count": len(u2_region_rows),
        "origin_local_completion_row_count": len(origin_ids),
        "exact_key_local_join_row_count": len(join_ids),
        "distinct_local_signature_count": len(signature_digests),
        "global_zero_credit_field_occurrence_count": global_zero_count,
        "whole_tube_zero_credit_field_occurrence_count": whole_zero_count,
        "lower_dimensional_owner_zero_credit_field_occurrence_count":
            lower_credit_zero_count,
        "lower_dimensional_ownership_false_occurrence_count":
            lower_ownership_false_count,
        "global_fibre_exhaustion_false_occurrence_count":
            fibre_false_count,
    }


def same_directory_regular_bytes(
    path: Path,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    require(
        not any(part == ".." for part in path.parts),
        f"input parent alias:{path.name}",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        f"input exact directory:{absolute.name}",
    )
    return regular_bytes(absolute, maximum)


def literal_duplicate_key_count(tree: ast.AST) -> int:
    duplicate_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[tuple[type, Any]] = set()
        for key in node.keys:
            if not isinstance(key, ast.Constant):
                continue
            marker = (type(key.value), key.value)
            if marker in seen:
                duplicate_count += 1
            seen.add(marker)
    return duplicate_count


def static_inert_boundary_audit() -> dict[str, Any]:
    producer_raw = same_directory_regular_bytes(PRODUCER, 5_000_000)
    require(
        hashlib.sha256(producer_raw).hexdigest()
        == EXPECTED_PRODUCER_SHA256,
        "producer inert-byte pin",
    )
    verifier_raw = same_directory_regular_bytes(
        Path(__file__), 5_000_000
    )
    producer_tree = ast.parse(
        producer_raw.decode("utf-8", "strict"),
        filename=PRODUCER.name,
    )
    verifier_tree = ast.parse(
        verifier_raw.decode("utf-8", "strict"),
        filename=Path(__file__).name,
    )

    def imports(tree: ast.AST) -> list[str]:
        names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.append(node.module or "")
        return sorted(names)

    verifier_imports = imports(verifier_tree)
    require(
        PRODUCER.stem not in verifier_imports
        and not any(
            name.startswith((
                "cm2_round203_",
                "cm2_round207_",
                ROUND208_PREFIX,
            ))
            for name in verifier_imports
        ),
        "forbidden Round203/Round207/Round208 import",
    )
    dynamic_imports = sorted({
        node.args[0].value
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "importlib"
        and node.func.attr == "import_module"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    })
    require(
        dynamic_imports == [
            "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier",
            "cm2_round198_source_g_outgoing_return_signature_probe",
        ],
        "exact dynamic import allowlist",
    )
    dangerous_calls = {
        node.func.id
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "eval", "compile"}
    }
    require(not dangerous_calls, "dynamic code execution boundary")
    require(
        PRODUCER.stem not in sys.modules
        and not any(
            name.startswith(("cm2_round203_", "cm2_round207_"))
            for name in sys.modules
        ),
        "producer and post-Round198 probe modules absent",
    )

    def function_bodies(tree: ast.Module) -> dict[str, str]:
        result: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = ast.Module(body=node.body, type_ignores=[])
                result[node.name] = hashlib.sha256(
                    ast.dump(
                        body,
                        annotate_fields=True,
                        include_attributes=False,
                    ).encode()
                ).hexdigest()
        return result

    producer_bodies = function_bodies(producer_tree)
    verifier_bodies = function_bodies(verifier_tree)
    reverse_producer: defaultdict[str, list[str]] = defaultdict(list)
    for name, value in producer_bodies.items():
        reverse_producer[value].append(name)
    overlap_pairs = sorted(
        (producer_name, verifier_name)
        for verifier_name, value in verifier_bodies.items()
        for producer_name in reverse_producer.get(value, [])
    )
    require(
        ("build_result", "build_result") not in overlap_pairs
        and ("main", "main") not in overlap_pairs,
        "producer build/main body reuse",
    )
    producer_duplicate_keys = literal_duplicate_key_count(producer_tree)
    verifier_duplicate_keys = literal_duplicate_key_count(verifier_tree)
    require(
        producer_duplicate_keys == 0 and verifier_duplicate_keys == 0,
        "AST duplicate literal keys",
    )
    return {
        "producer_treated_as_inert_regular_bytes": True,
        "producer_imported_or_executed": False,
        "Round207_imported_or_executed": False,
        "Round203_imported_or_executed": False,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "verifier_sha256": hashlib.sha256(verifier_raw).hexdigest(),
        "producer_AST_parse": "PASS",
        "verifier_AST_parse": "PASS",
        "producer_AST_duplicate_literal_key_count": producer_duplicate_keys,
        "verifier_AST_duplicate_literal_key_count": verifier_duplicate_keys,
        "verifier_forbidden_import_count": 0,
        "dynamic_import_allowlist": dynamic_imports,
        "pre_Round208_pinned_evaluator_probe_imported": True,
        "producer_top_level_function_count": len(producer_bodies),
        "verifier_top_level_function_count": len(verifier_bodies),
        "exact_AST_body_overlap_pair_count": len(overlap_pairs),
        "exact_AST_body_overlap_pairs": [
            {
                "producer_function": producer_name,
                "verifier_function": verifier_name,
            }
            for producer_name, verifier_name in overlap_pairs
        ],
        "producer_build_result_body_reused": False,
        "producer_main_body_reused": False,
        "implementation_diverse_second_derivation_claimed": False,
        "shared_lower_level_algorithm_risk_disclosed": True,
    }


def resign_one_ledger_row(
    result: dict[str, Any],
    ledger_name: str,
    index: int,
) -> None:
    ledger = result[ledger_name]
    row = ledger["rows"][index]
    payload = {
        key: value for key, value in row.items() if key != "row_sha256"
    }
    row["row_sha256"] = digest(payload)
    ledger["rows_sha256"] = digest(ledger["rows"])


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> Any:
    cursor = root
    for item in path[:-1]:
        cursor = cursor[item]
    old = cursor[path[-1]]
    cursor[path[-1]] = value
    return old


def validate_candidate_document(
    document: dict[str, Any],
    expected_result: dict[str, Any],
) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == SCHEMA
        and document["result_sha256"] == digest(document["result"]),
        "candidate self-consistent envelope",
    )
    audit_reconstructed_result(document["result"])
    require(
        document["result"] == expected_result,
        "complete independently expected result equality",
    )


def semantic_attack_suite(
    certificate: dict[str, Any],
    expected_result: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[
        tuple[str, tuple[Any, ...], Any, tuple[str, int] | None]
    ] = [
        ("status promotion", ("result", "status"), "PROMOTED", None),
        (
            "Round207 verifier dependency lie",
            ("result", "formal_input_binding",
             "independent_verifier_must_not_import_Round207"),
            False,
            None,
        ),
        (
            "formal scope region count",
            ("result", "formal_scope_contract",
             "strict_open_3D_candidate_region_count"),
            EXPECTED_CANDIDATES - 1,
            None,
        ),
        (
            "factor-face method",
            ("result", "formal_final_factor_face_ledger",
             "rows", 0, "final_method"),
            "FABRICATED_FACE_METHOD",
            ("formal_final_factor_face_ledger", 0),
        ),
        (
            "leaf classification",
            ("result", "formal_leaf_geometry_ledger",
             "rows", 0, "final_graph_classification"),
            "FABRICATED_LEAF_CLASS",
            ("formal_leaf_geometry_ledger", 0),
        ),
        (
            "direct target",
            ("result", "formal_direct_leaf_signature_base_ledger",
             "rows", 0, "direct_target_lift"),
            "FABRICATED_TARGET",
            ("formal_direct_leaf_signature_base_ledger", 0),
        ),
        (
            "regional outgoing cell",
            ("result", "formal_local_open_3D_signature_ledger",
             "rows", 0, "local_return_signature", "outgoing_cell"),
            "FABRICATED_CELL",
            ("formal_local_open_3D_signature_ledger", 0),
        ),
        (
            "regional lower-dimensional credit",
            ("result", "formal_local_open_3D_signature_ledger",
             "rows", 0, "lower_dimensional_half_open_owner_credit"),
            1,
            ("formal_local_open_3D_signature_ledger", 0),
        ),
        (
            "U-pipe-U copied signature",
            ("result", "formal_U_pipe_U_side_specific_ledger",
             "cross_t_signature_copy_used"),
            True,
            None,
        ),
        (
            "origin whole-tube credit",
            ("result", "formal_origin_local_completion_ledger",
             "rows", 0, "whole_original_tube_credit"),
            1,
            ("formal_origin_local_completion_ledger", 0),
        ),
        (
            "exact-key global exhaustion",
            ("result", "formal_exact_key_local_join_ledger",
             "rows", 0, "global_exact_key_fibre_exhausted"),
            True,
            ("formal_exact_key_local_join_ledger", 0),
        ),
        (
            "exact-key global disposition credit",
            ("result", "formal_exact_key_local_join_ledger",
             "rows", 0, "global_exact_key_disposition_credit"),
            1,
            ("formal_exact_key_local_join_ledger", 0),
        ),
        (
            "coordinate volume delta",
            ("result", "exact_dimension_and_volume_conservation",
             "exact_coordinate_volume_delta"),
            "1",
            None,
        ),
        (
            "frozen owner used for direct selection",
            ("result", "method_independence_contract",
             "frozen_owner_used_only_posthoc"),
            False,
            None,
        ),
        (
            "D02 promotion",
            ("result",
             "formal_local_materialization_and_strict_nonpromotion", "D02"),
            "OPEN",
            None,
        ),
        (
            "global source-G disposition promotion",
            ("result",
             "formal_local_materialization_and_strict_nonpromotion",
             "source_G_global_exact_key_dispositions"),
            f"1/{EXPECTED_SOURCE_G_KEY_COUNT}",
            None,
        ),
        (
            "producer provenance",
            ("result", "provenance", "producer_sha256"),
            "0" * 64,
            None,
        ),
        (
            "global next-gate overclaim",
            ("result", "next_core_gate"),
            "declare every global exact-key fibre complete",
            None,
        ),
    ]
    rejected: list[str] = []
    for name, path, replacement, ledger_row in attacks:
        original = set_path(certificate, path, replacement)
        require(original != replacement, f"attack collision:{name}")
        try:
            if ledger_row is not None:
                resign_one_ledger_row(
                    certificate["result"],
                    ledger_row[0],
                    ledger_row[1],
                )
            certificate["result_sha256"] = digest(certificate["result"])
            require(
                certificate["result_sha256"]
                != EXPECTED_CERTIFICATE_RESULT_SHA256,
                f"re-signed mutation changed digest:{name}",
            )
            try:
                validate_candidate_document(certificate, expected_result)
            except Exception:
                rejected.append(name)
            else:
                raise Round208Error(f"semantic attack accepted:{name}")
        finally:
            set_path(certificate, path, original)
            if ledger_row is not None:
                resign_one_ledger_row(
                    certificate["result"],
                    ledger_row[0],
                    ledger_row[1],
                )
            certificate["result_sha256"] = digest(certificate["result"])
    require(
        len(rejected) == len(attacks)
        and certificate["result"] == expected_result
        and certificate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "semantic attack restoration and census",
    )
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": True,
        "attack_names": rejected,
        "every_attack_result_digest_recomputed": True,
        "affected_closed_row_and_ledger_digests_recomputed": True,
    }


def expect_rejection(
    name: str,
    operation: Callable[[], Any],
) -> str:
    try:
        operation()
    except Exception:
        return name
    raise Round208Error(f"attack accepted:{name}")


def strict_json_attack_suite() -> dict[str, Any]:
    cases = [
        ("duplicate key", b'{"a":1,"a":2}'),
        ("float", b'{"a":1.0}'),
        ("NaN", b'{"a":NaN}'),
        ("Infinity", b'{"a":Infinity}'),
        ("negative Infinity", b'{"a":-Infinity}'),
        ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
        ("NUL", b'{"a":"x\\u0000"}\x00\n'),
        ("invalid UTF-8", b'{"a":"\xff"}\n'),
        ("surrogate value", b'{"a":"\\ud800"}\n'),
        ("surrogate key", b'{"\\udfff":1}\n'),
        ("trailing JSON", b'{"a":1}{}\n'),
        ("top array", b'[]\n'),
        ("empty", b''),
        ("noncanonical whitespace", b'{ "a": 1 }\n'),
    ]
    rejected = [
        expect_rejection(
            name,
            lambda raw=raw, name=name: strict_json(raw, f"attack:{name}"),
        )
        for name, raw in cases
    ]
    oversize = HERE / (
        f".cm2_round208_{os.getpid()}_oversize_JSON_input.json"
    )
    try:
        with oversize.open("wb") as handle:
            handle.truncate(65)
        rejected.append(expect_rejection(
            "oversize",
            lambda: same_directory_regular_bytes(oversize, 64),
        ))
    finally:
        if oversize.exists() or oversize.is_symlink():
            oversize.unlink()
    require(len(rejected) == 15, "strict JSON attack census")
    return {
        "attack_count": len(rejected),
        "rejected_count": len(rejected),
        "all_rejected": True,
        "attack_names": rejected,
    }


def protected_output_paths() -> set[Path]:
    protected = {
        Path(__file__).resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        (HERE / ROUND208_REPORT).resolve(),
        (HERE / ROUND208_COLD).resolve(),
        (HERE / ROUND208_MANIFEST).resolve(),
        (HERE / R207_SOURCE).resolve(),
        (HERE / R207_REPORT).resolve(),
        (HERE / R182_MANIFEST).resolve(),
    }
    protected.update((HERE / name).resolve() for name in R182_PINS)
    protected.update((HERE / name).resolve() for name in EVALUATOR_PINS)
    return protected


def validate_output(path: Path) -> Path:
    require(
        not any(part == ".." for part in path.parts),
        "output parent alias",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact directory",
    )
    require(
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round208_")
            and absolute.name.endswith("_verification.json")
        ),
        "verification output allowlist",
    )
    require(
        absolute.resolve(strict=False) not in protected_output_paths(),
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "verification output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    absolute = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.",
        suffix=".tmp",
        dir=absolute.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        metadata = temporary.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not temporary.is_symlink()
            and metadata.st_nlink == 1,
            "atomic temporary type",
        )
        os.replace(temporary, absolute)
        directory_descriptor = os.open(
            os.fspath(absolute.parent),
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        raise
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


def path_type_alias_and_temp_attack_suite() -> dict[str, Any]:
    pid = os.getpid()
    scratch = Path(tempfile.mkdtemp(
        prefix=".cm2_round208_verifier_attack.",
        dir=HERE,
    ))
    source = scratch / "source"
    source.write_bytes(b"SAFE\n")
    victim = scratch / "victim"
    victim.write_bytes(b"SAFE\n")
    input_symlink = HERE / f".cm2_round208_{pid}_input_symlink"
    input_hardlink = HERE / f".cm2_round208_{pid}_input_hardlink"
    input_fifo = HERE / f".cm2_round208_{pid}_input_fifo"
    output_symlink = (
        HERE / f".cm2_round208_{pid}_symlink_verification.json"
    )
    output_hard_base = (
        HERE / f".cm2_round208_{pid}_base_verification.json"
    )
    output_hardlink = (
        HERE / f".cm2_round208_{pid}_hard_verification.json"
    )
    output_fifo = (
        HERE / f".cm2_round208_{pid}_fifo_verification.json"
    )
    outside = (
        HERE.parent / f".cm2_round208_{pid}_escape_verification.json"
    )
    parent_alias = HERE / f".cm2_round208_parent_alias_{pid}"
    safe_target = (
        HERE / f".cm2_round208_{pid}_safe_verification.json"
    )
    predictable_temp = (
        HERE / f".{safe_target.name}.prepositioned.tmp"
    )
    rejected: list[str] = []
    created = [
        input_symlink,
        input_hardlink,
        input_fifo,
        output_symlink,
        output_hardlink,
        output_hard_base,
        output_fifo,
        outside,
        parent_alias,
        safe_target,
        predictable_temp,
    ]
    try:
        input_symlink.symlink_to(source)
        os.link(source, input_hardlink)
        os.mkfifo(input_fifo)
        rejected.extend([
            expect_rejection(
                "input symlink",
                lambda: same_directory_regular_bytes(input_symlink, 64),
            ),
            expect_rejection(
                "input hardlink",
                lambda: same_directory_regular_bytes(input_hardlink, 64),
            ),
            expect_rejection(
                "input FIFO",
                lambda: same_directory_regular_bytes(input_fifo, 64),
            ),
            expect_rejection(
                "input directory",
                lambda: same_directory_regular_bytes(scratch, 64),
            ),
            expect_rejection(
                "input parent escape",
                lambda: same_directory_regular_bytes(
                    HERE.parent / "round208-outside-input", 64
                ),
            ),
            expect_rejection(
                "input parent-dot-dot alias",
                lambda: same_directory_regular_bytes(
                    HERE / ".." / HERE.name / PRODUCER.name, 5_000_000
                ),
            ),
        ])
        parent_alias.symlink_to(HERE, target_is_directory=True)
        rejected.append(expect_rejection(
            "input symlink parent alias",
            lambda: same_directory_regular_bytes(
                parent_alias / PRODUCER.name, 5_000_000
            ),
        ))

        output_symlink.symlink_to(victim)
        output_hard_base.write_bytes(b"SAFE\n")
        os.link(output_hard_base, output_hardlink)
        os.mkfifo(output_fifo)
        rejected.extend([
            expect_rejection(
                "output symlink",
                lambda: safe_write(output_symlink, b"x"),
            ),
            expect_rejection(
                "output hardlink",
                lambda: safe_write(output_hardlink, b"x"),
            ),
            expect_rejection(
                "output FIFO",
                lambda: safe_write(output_fifo, b"x"),
            ),
            expect_rejection(
                "output parent escape",
                lambda: safe_write(outside, b"x"),
            ),
            expect_rejection(
                "nested output",
                lambda: safe_write(
                    scratch
                    / f".cm2_round208_{pid}_nested_verification.json",
                    b"x",
                ),
            ),
            expect_rejection(
                "output symlink parent alias",
                lambda: safe_write(
                    parent_alias
                    / f".cm2_round208_{pid}_alias_verification.json",
                    b"x",
                ),
            ),
            expect_rejection(
                "output parent-dot-dot alias",
                lambda: safe_write(
                    HERE / ".." / HERE.name
                    / f".cm2_round208_{pid}_dotdot_verification.json",
                    b"x",
                ),
            ),
            expect_rejection(
                "unallowlisted same-directory output",
                lambda: safe_write(
                    HERE / f"cm2_round208_{pid}_unlisted.json", b"x"
                ),
            ),
            expect_rejection(
                "certificate-shaped hidden output",
                lambda: safe_write(
                    HERE / f".cm2_round208_{pid}_certificate.json",
                    b"x",
                ),
            ),
            expect_rejection(
                "temporary-shaped direct output",
                lambda: safe_write(
                    HERE
                    / f".cm2_round208_{pid}_verification.json.tmp",
                    b"x",
                ),
            ),
            expect_rejection(
                "producer output alias",
                lambda: safe_write(PRODUCER, b"x"),
            ),
            expect_rejection(
                "certificate output alias",
                lambda: safe_write(CERTIFICATE, b"x"),
            ),
            expect_rejection(
                "verifier output alias",
                lambda: safe_write(Path(__file__), b"x"),
            ),
            expect_rejection(
                "Round182 manifest output alias",
                lambda: safe_write(HERE / R182_MANIFEST, b"x"),
            ),
            expect_rejection(
                "existing output directory",
                lambda: safe_write(scratch, b"x"),
            ),
        ])

        predictable_temp.symlink_to(victim)
        safe_write(safe_target, b"NEW\n")
        require(
            victim.read_bytes() == b"SAFE\n"
            and safe_target.read_bytes() == b"NEW\n"
            and predictable_temp.is_symlink(),
            "prepositioned temporary symlink untouched",
        )
        rejected.append("prepositioned temporary symlink not followed")
    finally:
        for path in created:
            if path.exists() or path.is_symlink():
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
        if scratch.exists():
            shutil.rmtree(scratch)
    require(len(rejected) == 23, "path/type/alias/temp attack census")
    return {
        "attack_count": len(rejected),
        "rejected_or_safely_bypassed_count": len(rejected),
        "all_rejected_or_safely_bypassed": True,
        "attack_names": rejected,
        "real_protected_files_modified": False,
        "prepositioned_temporary_symlink_not_followed": True,
        "file_fsync_before_replace": True,
        "parent_directory_fsync_after_replace": True,
    }


def load_candidate_certificate() -> tuple[dict[str, Any], bytes]:
    raw = same_directory_regular_bytes(
        CERTIFICATE,
        EXPECTED_CERTIFICATE_SIZE,
    )
    require(
        len(raw) == EXPECTED_CERTIFICATE_SIZE
        and hashlib.sha256(raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "candidate certificate byte pin",
    )
    return strict_json(raw, CERTIFICATE.name), raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--expect-result")
    arguments = parser.parse_args()
    ctx.prec = 256

    boundary = static_inert_boundary_audit()
    rebuilt_result = build_result(EXPECTED_PRODUCER_SHA256)
    expected_result = strict_json(
        canonical_bytes({"result": rebuilt_result}) + b"\n",
        "canonical independently rebuilt expected result",
    )["result"]
    del rebuilt_result
    reconstructed_result_sha256 = digest(expected_result)
    require(
        reconstructed_result_sha256
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "independent expected result digest",
    )
    census = audit_reconstructed_result(expected_result)

    # Candidate loading deliberately occurs only after expected reconstruction.
    certificate, certificate_raw = load_candidate_certificate()
    expected_document = {
        "schema": SCHEMA,
        "result": expected_result,
        "result_sha256": reconstructed_result_sha256,
    }
    validate_candidate_document(certificate, expected_result)
    expected_raw = canonical_bytes(expected_document) + b"\n"
    require(
        certificate == expected_document
        and certificate_raw == expected_raw
        and hashlib.sha256(expected_raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "full expected Python-object and canonical-byte equality",
    )
    del certificate_raw, expected_raw

    semantic_attacks = semantic_attack_suite(
        certificate, expected_result
    )
    json_attacks = strict_json_attack_suite()
    path_attacks = path_type_alias_and_temp_attack_suite()
    require(
        PRODUCER.stem not in sys.modules
        and not any(
            name.startswith(("cm2_round203_", "cm2_round207_"))
            for name in sys.modules
        ),
        "producer and post-Round198 probes never imported",
    )
    pin_round182()

    verification_result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND208",
        "verdict": "PASS",
        "verifier_filename": Path(__file__).name,
        "verifier_sha256": boundary["verifier_sha256"],
        "producer_filename": PRODUCER.name,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "certificate_filename": CERTIFICATE.name,
        "certificate_file_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_size_bytes": EXPECTED_CERTIFICATE_SIZE,
        "certificate_result_sha256":
            EXPECTED_CERTIFICATE_RESULT_SHA256,
        "reconstructed_result_sha256": reconstructed_result_sha256,
        "complete_expected_result_rebuilt_before_candidate_load": True,
        "full_expected_python_object_equality": True,
        "full_expected_canonical_byte_equality": True,
        "verified_census": census,
        "strict_nonpromotion": {
            "lower_dimensional_half_open_ownership": "NOT_MATERIALIZED",
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions":
                f"0/{EXPECTED_SOURCE_G_KEY_COUNT}",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "independence_contract": {
            **boundary,
            "imports_only_pinned_pre_Round208_evaluator_stack": True,
            "Round182_manifest_and_all_seven_entries_replayed": True,
            "candidate_certificate_loaded_only_after_expected_rebuilt":
                True,
            "complete_expected_result_rebuilt": True,
            "full_expected_canonical_byte_equality": True,
            "implementation_diverse_second_derivation_claimed": False,
        },
        "semantic_resigned_attack_suite": semantic_attacks,
        "strict_JSON_and_oversize_attack_suite": json_attacks,
        "path_type_alias_and_temp_attack_suite": path_attacks,
        "output_safety": {
            "strict_verification_only_allowlist": True,
            "parent_dot_dot_and_symlink_aliases_rejected": True,
            "single_link_regular_existing_output_required": True,
            "unpredictable_same_directory_temporary": True,
            "file_fsync_before_replace": True,
            "parent_directory_fsync_after_replace": True,
        },
    }
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "result": verification_result,
        "result_sha256": digest(verification_result),
    }
    if arguments.expect_result is not None:
        require(
            verification["result_sha256"] == arguments.expect_result,
            "expected verification result",
        )
    safe_write(
        arguments.output,
        canonical_bytes(verification) + b"\n",
    )
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
