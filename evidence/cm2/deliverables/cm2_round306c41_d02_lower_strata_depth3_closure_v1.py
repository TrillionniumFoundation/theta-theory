#!/usr/bin/env python3
"""C41: consolidated depth-three strict routing of the C40 lower frontier.

This producer consumes exactly the 12,398 nonterminal, pre-collision-three
rows of the audited C40 object.  It repairs the Round166 W:W cache omission,
then applies at most three further exact dyadic splits.  Strict exclusions may
stop early; every graph, endpoint, boundary, corner, incidence, exception and
collision-three-ready row remains zero-credit.  All credit is reconstructed
only through the unified 862-parent Kraft ledger.

The C40 audit pins below intentionally remain fail-closed placeholders until
the independent C40 audit has passed.  Pilot mode never writes a candidate.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import heapq
import itertools
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from contextlib import ExitStack
from fractions import Fraction as Q
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator

import flint
from flint import ctx

import cm2_round185_preconditioned_c1_residual_refinement as round185
import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38
import cm2_round306c39_d02_h1_c1_graph_cell_router_v1 as c39
import cm2_round306c40_d02_h1_endpoint_collision2_arrangement_v1 as c40


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c41.d02-lower-strata-depth3-closure.v1"
CROSSWALK_SCHEMA = SCHEMA + ".input-blocker-crosswalk"
AMBIENT_SCHEMA = SCHEMA + ".routed-ambient-cell"
SPLIT_SCHEMA = SCHEMA + ".split-face-adjacency"
CACHE_REPLAY_SCHEMA = SCHEMA + ".full-chart-cache-replay"
SINGLETON_SCHEMA = SCHEMA + ".candidate-universe-singleton"
C1_OUTER_SCHEMA = SCHEMA + ".c1-h1-surface-outer"
ENDPOINT_SCHEMA = SCHEMA + ".endpoint-rechart"
C2_OUTER_SCHEMA = SCHEMA + ".c2-surface-outer"
INCIDENCE_SCHEMA = SCHEMA + ".incidence-outer"
BOUNDARY_SCHEMA = SCHEMA + ".boundary-corner-outer"
PARENT_SCHEMA = SCHEMA + ".parent-conservation"
RECEIPT_SCHEMA = SCHEMA + ".execution-receipt"
NORMALIZED_SURFACE_REGISTRY_SCHEMA = (
    SCHEMA + ".nested-normalized-surface-registry.v1"
)

CANDIDATE_INVENTORY = tuple(sorted([
    "C41_LOWER_STRATA_PARTIAL.lock",
    "boundary_corner_outers.jsonl.gz",
    "c1_h1_surface_outers.jsonl.gz",
    "c2_surface_outers.jsonl.gz",
    "candidate_universe_singletons.jsonl.gz",
    "endpoint_recharts.jsonl.gz",
    "full_chart_cache_replay.jsonl.gz",
    "incidence_outers.jsonl.gz",
    "input_blocker_crosswalk.jsonl.gz",
    "parent_conservation.jsonl.gz",
    "result.json",
    "root_manifest.sha256",
    "routed_ambient_cells.jsonl.gz",
    "split_face_adjacency.jsonl.gz",
]))

PRECISION_BITS = 384
EXTRA_DEPTH = 3
SHARD_COUNT = 8
FROZEN_OWNER = "W[1,0]"

EXPECTED_C40_OBJECT = (
    "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba"
)
EXPECTED_UPSTREAM_OBJECTS = {
    "C39": "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "C38": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C37": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    "C36": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C35": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C34": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C32": "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
}
EXPECTED_C40_SOURCE = (
    "9ec1ad4df72b0f25b646d17a43e1186188ace97d2e76ac480c1c2a476fac5f57"
)
EXPECTED_C40_AUDIT_OBJECT = (
    "4acfe9cf77f4e394458a32c0f341bc679768fc3f137ea9d6f6362cc68df9e485"
)
EXPECTED_C40_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C40_DIMENSION_SAFE_OUTER_AUDIT__"
    "31_OF_31_ATTACKS_FAIL_CLOSED"
)

EXPECTED_SOURCE_SHA256 = {
    "C40": EXPECTED_C40_SOURCE,
    "C39": "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae",
    "C38": "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d",
    "Round185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "Round166": "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "candidate_generator": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
}

CHART_ORDER = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
EXPECTED_CHART_CANDIDATES = {
    "G:E": (57, "d02bd7d102705087f2ee15af47a52d3a2c15495f690d39d8c17939a3843d7808"),
    "G:W": (57, "47276a2b2d2e428ba50326b6fc620a85045f58bf6e057d571716acb2dc55dccc"),
    "G:N": (57, "c3cb961313f9e229809fb695713b410f2663a3858c0d11f2398842c70efa365e"),
    "G:S": (57, "2fa312582b254c8994ddaf24e011bff88eaa7ac516320bf0bdf41ab07079640a"),
    "W:E": (55, "ebeeae12ba192d7808031ebf4be3537fb49e73e17295404adcad371045e7c2e7"),
    "W:W": (55, "a7b777d2bf74577fafef77eafa1da6237883e5e6420352772395978a146b9a49"),
    "W:N": (55, "4719c19ccb8c63288e8815c4b8961f64d9d096dd4377641acafbec59c00769e5"),
    "W:S": (55, "89d699755e74a71b2771fb907e3f1bcf0e13d96621a977a4731c563cb928a5f8"),
}
EXPECTED_OFFICIAL_REGISTRY_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)

LOWER_BLOCKER_CENSUS = {
    "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE": 218,
    "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY": 1147,
    "UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT": 3550,
    "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL": 29,
    "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER": 19,
    "UNRESOLVED_C40_COLLISION2_ACTIVE_DELTA_1": 1362,
    "UNRESOLVED_C40_COLLISION2_ACTIVE_DELTA_2": 140,
    "UNRESOLVED_C40_COLLISION2_ACTIVE_DELTA_3": 3,
    "UNRESOLVED_C40_COLLISION2_EVALUATION_EXCEPTION": 88,
    "UNRESOLVED_C40_COLLISION2_OUTGOING_H2": 2327,
    "UNRESOLVED_C40_COLLISION2_POINT_WINNER_NONSTRICT": 1804,
    "UNRESOLVED_C40_COLLISION2_WALL_ENDPOINT": 1511,
    "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_EVALUATION_FAILURE_OUTER": 200,
}
EXPECTED_LOWER_BLOCKER_COUNT = 12_398
EXPECTED_C40_TERMINAL_ROW_COUNT = 21_951
EXPECTED_C40_COLLISION3_READY_ROW_COUNT = 660
EXPECTED_C40_ROW_COUNT = 35_009
EXPECTED_CACHE_REPLAY_CENSUS = {
    "UNRESOLVED_C40_LIVE_COLLISION2_ORIGINAL_MATCH_NEEDS_COLLISION3_1648": 7,
    "UNRESOLVED_C40_LIVE_COLLISION2_REFLECTED_MATCH_NEEDS_COLLISION3_1648": 12,
}

INVOCATION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{15,127}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


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
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(raw == raw.strip() + b"\n", f"canonical newline:{path}")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        require(len(values) == len({key for key, _value in values}),
                f"duplicate JSON key:{path}")
        return dict(values)

    value = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=lambda _value: (_ for _ in ()).throw(
            RuntimeError(f"float forbidden:{path}")
        ),
        parse_constant=lambda _value: (_ for _ in ()).throw(
            RuntimeError(f"constant forbidden:{path}")
        ),
    )
    require(type(value) is dict and canonical(value) + b"\n" == raw,
            f"canonical JSON:{path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def require_regular_single_link(path: Path, label: str) -> os.stat_result:
    value = path.lstat()
    require(
        stat.S_ISREG(value.st_mode)
        and not path.is_symlink()
        and value.st_nlink == 1,
        f"regular single-link {label}:{path}",
    )
    return value


def fsync_file(path: Path) -> None:
    require_regular_single_link(path, "fsync file")
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_directory(path: Path) -> None:
    value = path.lstat()
    require(stat.S_ISDIR(value.st_mode) and not path.is_symlink(),
            f"fsync directory:{path}")
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def canonical_workspace_path(
    path: Path,
    label: str,
    *,
    must_exist: bool,
) -> Path:
    resolved = path.resolve(strict=must_exist)
    require(within(resolved, ROOT) and resolved != ROOT,
            f"{label} must be canonical and inside workspace")
    if must_exist:
        require(path.absolute().resolve(strict=True) == resolved,
                f"{label} canonical resolution")
    else:
        ancestor = resolved.parent
        while not ancestor.exists():
            require(ancestor != ROOT, f"{label} existing ancestor")
            ancestor = ancestor.parent
        ancestor = ancestor.resolve(strict=True)
        require(within(ancestor, ROOT), f"{label} parent inside workspace")
        parent_stat = ancestor.lstat()
        require(
            stat.S_ISDIR(parent_stat.st_mode) and not ancestor.is_symlink(),
            f"{label} ancestor is real directory",
        )
    return resolved


def validate_manifest(directory: Path) -> None:
    directory_stat = directory.lstat()
    require(
        stat.S_ISDIR(directory_stat.st_mode) and not directory.is_symlink(),
        f"manifest directory:{directory}",
    )
    manifest = directory / "root_manifest.sha256"
    require_regular_single_link(manifest, "root manifest")
    rows = manifest.read_text(encoding="utf-8").splitlines()
    listed_names: list[str] = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", row)
        require(match is not None, f"manifest row syntax:{directory}")
        listed_names.append(match.group(2))
    require(
        listed_names == sorted(set(listed_names))
        and "result.json" in listed_names,
        f"manifest listed inventory:{directory}",
    )
    expected = []
    unlisted: list[str] = []
    for path in sorted(directory.iterdir()):
        if path.name == manifest.name:
            continue
        require_regular_single_link(path, "manifest member")
        if path.name in listed_names:
            expected.append(f"{file_sha256(path)}  {path.name}")
        else:
            unlisted.append(path.name)
    require(
        all(name.endswith(".lock") for name in unlisted),
        f"manifest unlisted non-lock member:{directory}:{unlisted}",
    )
    require(rows == expected, f"manifest exact:{directory}")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir()
        if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def validate_object(value: dict[str, Any], expected: str, label: str) -> None:
    observed = value.get("object_sha256")
    semantic = dict(value)
    semantic.pop("object_sha256", None)
    require(observed == digest(semantic) and observed == expected,
            f"object:{label}")


def validate_self_object(value: dict[str, Any], label: str) -> None:
    observed = value.get("object_sha256")
    semantic = dict(value)
    semantic.pop("object_sha256", None)
    require(
        HEX64.fullmatch(observed or "") is not None
        and observed == digest(semantic),
        f"self object:{label}",
    )


def validate_c41_candidate(
    directory: Path,
    expected_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(
        sorted(path.name for path in directory.iterdir())
        == list(CANDIDATE_INVENTORY),
        "C41 exact fourteen-file inventory replay",
    )
    validate_manifest(directory)
    result = strict_json(directory / "result.json")
    validate_self_object(result, "C41 candidate")
    if expected_result is not None:
        require(result == expected_result, "C41 expected result byte replay")
    return result


def formal_path_preflight(
    candidate: Path,
    audit: Path,
    output: Path,
    receipt: Path,
    pid: int,
) -> tuple[Path, Path, Path, Path]:
    candidate = canonical_workspace_path(
        candidate, "C40 candidate", must_exist=True
    )
    audit = canonical_workspace_path(audit, "C40 audit", must_exist=True)
    output = canonical_workspace_path(output, "C41 output", must_exist=False)
    receipt = canonical_workspace_path(
        receipt, "C41 receipt", must_exist=False
    )
    stage = output.with_name(output.name + f".stage-{pid}")
    require(
        not output.exists()
        and not stage.exists()
        and not receipt.exists(),
        "formal targets must not preexist",
    )
    require(
        not within(receipt, output)
        and not within(receipt, stage),
        "receipt must be out-of-band from candidate and stage",
    )
    for target, target_label in (
        (output, "output"),
        (stage, "stage"),
        (receipt, "receipt"),
    ):
        require(
            not within(target, candidate)
            and not within(target, audit.parent),
            f"{target_label} must be disjoint from upstream candidate/audit authority",
        )
    require_regular_single_link(audit, "C40 independent audit preflight")
    validate_manifest(candidate)
    return candidate, audit, output, receipt


def source_pins() -> dict[str, str]:
    paths = {
        "C40": Path(c40.__file__).resolve(),
        "C39": Path(c39.__file__).resolve(),
        "C38": Path(c38.__file__).resolve(),
        "Round185": Path(round185.__file__).resolve(),
        "Round166": Path(c38.round166.__file__).resolve(),
        "candidate_generator": Path(c38.round166.base.__file__).resolve(),
    }
    observed = {key: file_sha256(path) for key, path in paths.items()}
    require(observed == EXPECTED_SOURCE_SHA256, "source SHA256 pins")
    tuple_codec_self_test()
    return observed


def encoded_tuple_map(value: dict[tuple[str, ...], int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, item in value.items():
        require(
            type(key) is tuple
            and all(type(part) is str for part in key)
            and type(item) is int
            and not isinstance(item, bool),
            "tuple codec input",
        )
        encoded = json.dumps(
            list(key), ensure_ascii=False, separators=(",", ":"), allow_nan=False
        )
        require(encoded not in result, "tuple codec collision")
        result[encoded] = item
    return result


def decoded_tuple_map(value: dict[str, int]) -> dict[tuple[str, ...], int]:
    require(type(value) is dict, "tuple codec mapping")
    result: dict[tuple[str, ...], int] = {}
    for encoded, item in value.items():
        require(
            type(encoded) is str
            and type(item) is int
            and not isinstance(item, bool),
            "tuple codec encoded item",
        )
        try:
            raw = json.loads(encoded)
        except Exception as error:
            raise RuntimeError("tuple codec invalid JSON") from error
        require(
            type(raw) is list
            and all(type(part) is str for part in raw)
            and json.dumps(
                raw, ensure_ascii=False, separators=(",", ":"), allow_nan=False
            ) == encoded,
            "tuple codec canonical list[str]",
        )
        key = tuple(raw)
        require(key not in result, "tuple codec decoded duplicate")
        result[key] = item
    return result


def tuple_codec_self_test() -> None:
    keys = (
        (), ("",), ("\u001f",), ("a", "b"), ("a\u001fb",),
        ('"', "[", "]"), ("雪",), ("", ""),
    )
    original = {key: index for index, key in enumerate(keys)}
    require(decoded_tuple_map(encoded_tuple_map(original)) == original,
            "tuple codec roundtrip")
    hostile = (
        {"": 0}, {" [\"a\"]": 0}, {"{}": 0}, {"[1]": 0},
        {"[\"a\",]": 0}, {"[true]": 0}, {"[\"\\u0061\"]": 0},
    )
    for value in hostile:
        try:
            decoded_tuple_map(value)
        except RuntimeError:
            pass
        else:
            raise RuntimeError("tuple codec hostile accepted")
    require(
        residual_classification("UNRESOLVED_COLLISION1_WORD")
        == "UNRESOLVED_C41_COLLISION1_WORD_COLLAR_OUTER"
        and residual_classification("UNRESOLVED_COLLISION2_WORD")
        == "UNRESOLVED_C41_COLLISION2_WORD_COLLAR_OUTER",
        "explicit word-collar residual mappings",
    )


def install_complete_immutable_cache() -> dict[str, tuple[str, ...]]:
    """Freeze the official generator before any monkeypatch, then install it."""
    base = c38.round166.base
    generator = base.candidate_ids
    generated = {chart: tuple(generator(chart)) for chart in CHART_ORDER}
    for chart in CHART_ORDER:
        count, expected_digest = EXPECTED_CHART_CANDIDATES[chart]
        require(
            len(generated[chart]) == count
            and base.canonical_digest(list(generated[chart])) == expected_digest,
            f"complete candidate cache:{chart}",
        )
    candidate_cache = MappingProxyType(dict(generated))
    target_cache = MappingProxyType({
        target.target_id: target for target in base.TARGETS
    })
    try:
        candidate_cache["W:W"] = ()  # type: ignore[index]
    except TypeError:
        pass
    else:  # pragma: no cover - MappingProxyType contract
        raise RuntimeError("candidate cache mutable")

    def candidate_ids(chart_id: str) -> list[str]:
        require(chart_id in candidate_cache, f"uncached chart:{chart_id}")
        return list(candidate_cache[chart_id])

    def target_by_id(target_id: str) -> Any:
        require(target_id in target_cache, f"uncached target:{target_id}")
        return target_cache[target_id]

    c38.round166._candidate_cache = candidate_cache
    c38.round166._target_cache = target_cache
    base.candidate_ids = candidate_ids
    base.target_by_id = target_by_id
    c38.round166.atlas.records = c38.round166.records_full
    c38.round166.atlas.root_record = c38.round166.root_record_fast
    for chart in CHART_ORDER:
        require(tuple(base.candidate_ids(chart)) == generated[chart],
                f"cache replay:{chart}")
    return generated


def iter_ledger(
    directory: Path, descriptor: dict[str, Any]
) -> Iterator[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(
        path.is_file()
        and path.stat().st_size == descriptor["size"]
        and file_sha256(path) == descriptor["sha256"],
        f"ledger bytes:{path}",
    )
    count = 0
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            semantic = dict(row)
            row_sha = semantic.pop("row_sha256", None)
            require(row_sha == digest(semantic), f"row closure:{path}:{count}")
            sequence.update((row_sha + "\n").encode("ascii"))
            count += 1
            yield row
    require(
        count == descriptor["row_count"]
        and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger descriptor:{path}",
    )


LedgerWriter = c38.LedgerWriter


def is_lower_blocker(row: dict[str, Any]) -> bool:
    return row["classification"] in LOWER_BLOCKER_CENSUS


def disposition_family(classification: str) -> str:
    if classification.startswith("EXCLUDED_"):
        return "TERMINAL_EXCLUDED"
    if "NEEDS_COLLISION3_1648" in classification:
        return "COLLISION3_READY"
    return "RESIDUAL_OUTER"


def residual_classification(classification: str) -> str:
    if "ALGEBRAIC_ENDPOINT" in classification:
        return "UNRESOLVED_C41_ALGEBRAIC_H0_SEAM_RECHART_OUTER"
    if any(token in classification for token in (
        "SOURCE_RADICAL", "SOURCE_GRAZING_ENDPOINT", "P_ENDPOINT_BOX",
    )):
        return "UNRESOLVED_C41_SOURCE_RADICAL_STEREOGRAPHIC_ENDPOINT_OUTER"
    if "COLLISION1_WORD" in classification:
        return "UNRESOLVED_C41_COLLISION1_WORD_COLLAR_OUTER"
    if "COLLISION2_WORD" in classification:
        return "UNRESOLVED_C41_COLLISION2_WORD_COLLAR_OUTER"
    if "H1_GRAPH" in classification or "H1_BOUNDARY" in classification:
        return "UNRESOLVED_C41_H1_GRAPH_OR_BOUNDARY_OUTER"
    if "COLLISION1_OUTGOING_STATE" in classification:
        return "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER"
    if any(token in classification for token in (
        "REGULAR_MULTI_GRAPH", "SINGULAR_OR_ORDER", "COLLISION1_OWNER_GEOMETRY",
        "C1_ROUTE_EVALUATION", "COLLISION1_DELTA", "COLLISION1_ROOT",
    )):
        return "UNRESOLVED_C41_C1_REGULAR_MULTI_GRAPH_OUTER"
    for count in (1, 2, 3):
        if f"ACTIVE_DELTA_{count}" in classification:
            return f"UNRESOLVED_C41_COLLISION2_ACTIVE_DELTA_{count}_OUTER"
    if "POINT_WINNER_NONSTRICT" in classification or "POINT_OWNER_NOT_UNIQUE" in classification:
        return "UNRESOLVED_C41_COLLISION2_POINT_WINNER_NONSTRICT_OUTER"
    if "OUTGOING_H2" in classification or "COLLISION2_OUTGOING_STATE" in classification:
        return "UNRESOLVED_C41_COLLISION2_H2_FACTOR_OUTER"
    if "WALL_ENDPOINT" in classification or "WALL_OR_CORNER" in classification:
        return "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER"
    if "EVALUATION_EXCEPTION" in classification or "FAILURE_OUTER" in classification:
        return "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER"
    raise RuntimeError("unmapped residual classification:" + classification)


def box_payload(box: Any | None) -> dict[str, Any] | None:
    if box is None:
        return None
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def reflected_box(parent_key: str, box: Any | None) -> dict[str, Any] | None:
    if box is None:
        return None
    chart = parent_key.split(":")[1]
    return c40.reflected_payload(chart, box)


def load_context(
    candidate: Path,
    audit_path: Path | None,
    *,
    formal: bool,
) -> dict[str, Any]:
    source_pins()
    validate_manifest(candidate)
    result = strict_json(candidate / "result.json")
    validate_object(result, EXPECTED_C40_OBJECT, "C40")
    require(result["schema"] == c40.SCHEMA, "C40 schema")
    audit: dict[str, Any] | None = None
    if formal:
        require(
            HEX64.fullmatch(EXPECTED_C40_AUDIT_OBJECT) is not None
            and EXPECTED_C40_AUDIT_STATUS.startswith("PASS_"),
            "C40 audit pins pending",
        )
        require(audit_path is not None, "C40 audit path")
        require_regular_single_link(audit_path, "C40 independent audit")
        audit = strict_json(audit_path)
        validate_object(audit, EXPECTED_C40_AUDIT_OBJECT, "C40 audit")
        require(
            audit.get("candidate_object_sha256") == EXPECTED_C40_OBJECT
            and audit.get("status") == EXPECTED_C40_AUDIT_STATUS,
            "C40 independent audit binding",
        )

    c39_dir = (ROOT / result["C39_authority"]["path"]).resolve()
    require(
        result["C39_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C39"],
        "C40 to C39 authority object pin",
    )
    validate_manifest(c39_dir)
    c39_result = strict_json(c39_dir / "result.json")
    validate_object(c39_result, EXPECTED_UPSTREAM_OBJECTS["C39"], "C39")
    c38_dir = (ROOT / c39_result["C38_authority"]["path"]).resolve()
    require(
        c39_result["C38_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C38"],
        "C39 to C38 authority object pin",
    )
    validate_manifest(c38_dir)
    c38_result = strict_json(c38_dir / "result.json")
    validate_object(c38_result, EXPECTED_UPSTREAM_OBJECTS["C38"], "C38")
    c38_rows = c38.read_ledger(
        c38_dir, c38_result["ledgers"]["collision1_2_child_pairs"]
    )
    c38_index = {row["row_sha256"]: row for row in c38_rows}
    require(len(c38_index) == len(c38_rows), "C38 row index")

    c37_dir = (ROOT / c38_result["C37_authority"]["path"]).resolve()
    require(
        c38_result["C37_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C37"],
        "C38 to C37 authority object pin",
    )
    validate_manifest(c37_dir)
    c37_result = strict_json(c37_dir / "result.json")
    validate_object(c37_result, EXPECTED_UPSTREAM_OBJECTS["C37"], "C37")
    c36_dir = (ROOT / c37_result["C36_authority"]["path"]).resolve()
    require(
        c37_result["C36_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C36"],
        "C37 to C36 authority object pin",
    )
    validate_manifest(c36_dir)
    c36_result = strict_json(c36_dir / "result.json")
    validate_object(c36_result, EXPECTED_UPSTREAM_OBJECTS["C36"], "C36")
    c35_dir = (ROOT / c36_result["C35_authority"]["path"]).resolve()
    c34_dir = (ROOT / c36_result["C34_authority"]["path"]).resolve()
    require(
        c36_result["C35_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C35"]
        and c36_result["C34_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C34"],
        "C36 split authority object pins",
    )
    validate_manifest(c35_dir)
    validate_manifest(c34_dir)
    c35_result = strict_json(c35_dir / "result.json")
    c34_result = strict_json(c34_dir / "result.json")
    validate_object(c35_result, EXPECTED_UPSTREAM_OBJECTS["C35"], "C35")
    validate_object(c34_result, EXPECTED_UPSTREAM_OBJECTS["C34"], "C34")
    require(
        c35_result["C34_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C34"],
        "C35 to C34 authority object pin",
    )
    c32_dir = (ROOT / c34_result["C32_authority"]["path"]).resolve()
    require(
        c34_result["C32_authority"]["object_sha256"]
        == EXPECTED_UPSTREAM_OBJECTS["C32"],
        "C34 to C32 authority object pin",
    )
    validate_manifest(c32_dir)
    c32_result = strict_json(c32_dir / "result.json")
    validate_object(c32_result, EXPECTED_UPSTREAM_OBJECTS["C32"], "C32")
    cells = {
        row["cell_id"]: row
        for row in c38.read_ledger(c32_dir, c32_result["ledgers"]["cells"])
    }
    seam_rows = c38.read_ledger(
        c32_dir, c32_result["ledgers"]["source_chart_seams"]
    )
    seams_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for seam in seam_rows:
        seams_by_cell[seam["left_cell_id"]].append(seam)
        seams_by_cell[seam["right_cell_id"]].append(seam)
    pair_index, pattern_index, registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    require(
        len(pair_index) == 448
        and len(pattern_index) == 985
        and pattern_index.get(()) == 0
        and registry_sha == EXPECTED_OFFICIAL_REGISTRY_SHA256,
        "official tuple registry",
    )
    config = {
        "original_path": c38.read_ledger(
            c35_dir, c35_result["ledgers"]["path_occurrences"]
        )[:2],
        "reflected_path": c38.read_ledger(
            c37_dir, c37_result["ledgers"]["reflected_r1648_occurrences"]
        )[:2],
        "pair_index": encoded_tuple_map(pair_index),
        "pattern_index": encoded_tuple_map(pattern_index),
        "official_registry_sha256": registry_sha,
    }
    return {
        "result": result,
        "audit": audit,
        "c38_index": c38_index,
        "cells": cells,
        "seams_by_cell": seams_by_cell,
        "config": config,
        "upstream_authority_objects": dict(EXPECTED_UPSTREAM_OBJECTS),
    }


def decode_worker_config(value: dict[str, Any]) -> dict[str, Any]:
    config = copy.deepcopy(value)
    config["pair_index"] = decoded_tuple_map(config["pair_index"])
    config["pattern_index"] = decoded_tuple_map(config["pattern_index"])
    official_pair, official_pattern, registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    require(
        config["pair_index"] == official_pair
        and config["pattern_index"] == official_pattern
        and config["official_registry_sha256"] == registry_sha
        and registry_sha == EXPECTED_OFFICIAL_REGISTRY_SHA256
        and config["pattern_index"].get(()) == 0,
        "worker official tuple registry equality",
    )
    config["cores"] = tuple(c38.round139.lower.core_cert.physical_cores())
    return config


def route_at_path(
    task: dict[str, Any],
    path: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    source = task["source"]
    c38_source = task["c38_source"]
    cell = task["cell"]
    pseudo = copy.deepcopy(c38_source)
    pseudo["path"] = path
    route_task = {
        "task_id": source["c40_leaf_id"] + ":" + path,
        "kind": "C1",
        "row": pseudo,
        "cell": cell,
    }
    box, _active = c39.reconstruct_box(cell, path)
    try:
        result = c39.route_c1_task(route_task, config)
    except Exception as error:
        replay = c40.source_radical_failure_replay(
            c38_source["representative_origin_key"], box, error
        )
        exact_endpoint_phase = c40.endpoint_phase(box)
        if replay["source_radical_causal_match"]:
            classification = (
                "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_"
                "EVALUATION_FAILURE_OUTER"
            )
        elif exact_endpoint_phase is not None:
            classification = (
                "UNRESOLVED_C40_P_ENDPOINT_BOX_ROUTE_EVALUATION_"
                "FAILURE_OUTER"
            )
        else:
            classification = "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
        return {
            "box": box,
            "classification": classification,
            "witness": type(error).__name__ + ":" + str(error),
            "route_method": "C41_C1_ROUTE_EXCEPTION_FAIL_CLOSED",
            "c1_result": None,
            "c2_status": None,
            "c2_baseline": None,
            "c2_detail": None,
            "c2_evidence": [],
            "route_failure": {
                "phase": "C39_ROUTE_C1_TASK",
                "exception_type": type(error).__name__,
                "exception_module": type(error).__module__,
                "exception_message": str(error),
                "exact_box_endpoint_phase": exact_endpoint_phase,
                "source_radical_initial_geometry_replay": replay,
            },
        }

    classification = result["classification"]
    witness = result["witness"]
    route_method = result["route_method"]
    c2_status: str | None = None
    c2_baseline: str | None = None
    c2_detail: dict[str, Any] | None = None
    c2_evidence: list[dict[str, Any]] = []
    if c40.collision2_safe(result, classification):
        try:
            c2_status, c2_detail, c2_evidence, c2_baseline = (
                round185.resolve_dynamic_box(
                    c38_source["representative_origin_key"],
                    box,
                    config["pair_index"],
                    config["pattern_index"],
                )
            )
            if c2_status.startswith("LOCAL_EXACT_KEY"):
                classification, witness = c40.expected_collision2(
                    c2_detail, config
                )
            else:
                classification = "UNRESOLVED_C40_COLLISION2_" + c2_status
                witness = c2_baseline
            route_method = "C41_ROUND185_DEPTH3_STRICT_ROUTER"
        except Exception as error:
            classification = "UNRESOLVED_C40_COLLISION2_EVALUATION_EXCEPTION"
            witness = type(error).__name__ + ":" + str(error)
            route_method = "C41_ROUND185_FAIL_CLOSED"
            c2_status = "EVALUATION_EXCEPTION"
            c2_baseline = "ROUND185_FAIL_CLOSED"
            c2_detail = {
                "error_type": type(error).__name__,
                "error_module": type(error).__module__,
                "error_message": str(error),
            }
            c2_evidence = []
    return {
        "box": box,
        "classification": classification,
        "witness": witness,
        "route_method": route_method,
        "c1_result": result,
        "c2_status": c2_status,
        "c2_baseline": c2_baseline,
        "c2_detail": c2_detail,
        "c2_evidence": c2_evidence,
        "route_failure": None,
    }


def compact_root_surface(value: dict[str, Any]) -> dict[str, Any]:
    derivatives = value.get("tp_derivatives", {})
    return {
        "kind": "COLLISION1_DELTA_OR_NEAR_ROOT",
        "identifier": value.get("target_id"),
        "equation": (
            f"collision1_Delta_{value.get('target_id')}=0"
            if value.get("output_classification") == "unresolved_discriminant"
            else f"collision1_near_{value.get('target_id')}=0"
        ),
        "input_classification": value.get("input_classification"),
        "output_classification": value.get("output_classification"),
        "derivatives": derivatives,
        "strict_derivative_axes": [
            axis for axis in ("dt", "dp")
            if derivatives.get(axis, {}).get("sign") != "UNRESOLVED"
        ],
        "certified_nonempty_regular_graph": False,
        "carrier_existence_status": "UNRESOLVED_POTENTIAL_SURFACE_OUTER",
    }


def compact_h1_surface(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "H1",
        "identifier": FROZEN_OWNER,
        "equation": "H1=n1_x^2-n1_y^2=0",
        "H1_centered": value.get("H1_centered"),
        "H1_natural": value.get("H1_natural"),
        "graph_axis": value.get("graph_axis"),
        "face_evidence": value.get("face_evidence", []),
        "strict_derivative_axes": [value["graph_axis"]]
        if value.get("graph_axis") in {"t", "p"} else [],
        "certified_nonempty_regular_graph": (
            value.get("kind") == "REGULAR_FULL_FACE_GRAPH"
        ),
        "carrier_existence_status": (
            "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
            if value.get("kind") == "REGULAR_FULL_FACE_GRAPH"
            else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
        ),
    }


def surface_summaries(route: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    result = route.get("c1_result")
    if result is not None:
        evidence = result.get("surface_evidence") or {}
        for value in evidence.get("root_surfaces", []):
            if value.get("output_classification") in {
                "unresolved_discriminant", "unresolved_root_sign"
            }:
                rows.append(compact_root_surface(value))
        h1 = evidence.get("H1")
        if h1 is not None and h1.get("kind") not in {None, "STRICT_SIDE"}:
            rows.append(compact_h1_surface(h1))
    for value in route.get("c2_evidence", []):
        compact = c40.compact_surface(value)
        rows.append({
            "kind": compact["kind"],
            "identifier": compact["identifier"],
            "equation": compact["equation"],
            "centered_C0_sign": compact["centered_C0_sign"],
            "strict_derivative_axes": compact["strict_derivative_axes"],
            "axis_full_face_brackets_t_p_s": compact[
                "axis_full_face_brackets_t_p_s"
            ],
            "axis_interval_Newton": compact["axis_interval_Newton"],
            "certified_nonempty_regular_graph": bool(
                compact["independently_certified_nonempty"]
                and compact["strict_derivative_axes"]
            ),
            "carrier_existence_status": (
                "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
                if compact["independently_certified_nonempty"]
                and compact["strict_derivative_axes"]
                else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
            ),
            "evidence_sha256": compact["evidence_sha256"],
        })
    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        key = (row.get("kind"), row.get("identifier"), row.get("equation"))
        unique.setdefault(key, row)
    return list(unique.values())


def endpoint_rechart_payload(
    task: dict[str, Any],
    route: dict[str, Any],
    residual: str,
) -> dict[str, Any]:
    cell = task["cell"]
    c38_source = task["c38_source"]
    box = route["box"]
    if "ALGEBRAIC_H0" in residual:
        require(box is None, "algebraic endpoint has no rational box")
        algebraic = [
            (index, value)
            for index, value in enumerate(cell["physical_t_interval"])
            if value["kind"] == "ALGEBRAIC"
        ]
        require(len(algebraic) == 1, "single algebraic H0 endpoint")
        endpoint_index, endpoint = algebraic[0]
        require(
            endpoint["minimal_polynomial"] == "2*x^2-1"
            and len(endpoint["isolating_interval"]) == 2,
            "algebraic H0 polynomial and isolator",
        )
        seams = task["seams"]
        require(bool(seams), "algebraic endpoint seam rows")
        spans = [
            tuple(Q(value["value"]) for value in seam["physical_p_span"])
            for seam in seams
        ]
        require(
            spans[0][0] == Q(cell["physical_p_interval"][0])
            and spans[-1][1] == Q(cell["physical_p_interval"][1])
            and all(left[1] == right[0]
                    for left, right in zip(spans, spans[1:])),
            "algebraic seam exact p-span exhaustion",
        )
        incidences = []
        for ordinal, seam in enumerate(seams):
            current_is_left = seam["left_cell_id"] == cell["cell_id"]
            require(
                current_is_left or seam["right_cell_id"] == cell["cell_id"],
                "algebraic seam cell incidence",
            )
            owner_cell = seam["left_cell_id"]
            incidences.append({
                "seam_segment_ordinal": ordinal,
                "seam_id": seam["seam_id"],
                "face_id": seam["face_id"],
                "C32_seam_row_sha256": seam["row_sha256"],
                "left_cell_id": seam["left_cell_id"],
                "left_chart": seam["left_chart"],
                "left_compact_endpoint": seam["left_compact_endpoint"],
                "right_cell_id": seam["right_cell_id"],
                "right_chart": seam["right_chart"],
                "right_compact_endpoint": seam["right_compact_endpoint"],
                "exact_physical_p_span": seam["physical_p_span"],
                "exact_state_gluing_inherited_from_round162": seam[
                    "exact_state_gluing_inherited_from_round162"
                ],
                "half_open_adjacent_chart_policy": (
                    "C41_LEFT_CELL_OWNS_SEAM__RIGHT_CELL_EXCLUDES_DUPLICATE"
                ),
                "half_open_owner_cell_id": owner_cell,
                "representative_cell_half_open_role": (
                    "OWNS_SEAM"
                    if cell["cell_id"] == owner_cell
                    else "EXCLUDES_DUPLICATE_SEAM"
                ),
                "seam_ambient_credit": 0,
                "D02_gate_credit": 0,
            })
        return {
            "endpoint_kind": "ALGEBRAIC_H0_SOURCE_CHART_SEAM",
            "H0_equation": "H0=2*t^2-1=0",
            "minimal_polynomial": endpoint["minimal_polynomial"],
            "isolating_interval": endpoint["isolating_interval"],
            "algebraic_value": endpoint["value"],
            "exact_sign": (
                "NEGATIVE" if endpoint["value"].startswith("-")
                else "POSITIVE"
            ),
            "physical_interval_side": (
                "INTERIOR_ABOVE_ALGEBRAIC_ENDPOINT"
                if endpoint_index == 0
                else "INTERIOR_BELOW_ALGEBRAIC_ENDPOINT"
            ),
            "representative_cell_id": cell["cell_id"],
            "representative_chart": cell["compact_chart"],
            "horizontal_reflection_partner_cell_id": c38_source[
                "reflected_cell_id"
            ],
            "horizontal_reflection_partner_origin_key": c38_source[
                "reflected_origin_key"
            ],
            "horizontal_reflection_materialized_in_rational_box": False,
            "adjacent_chart_seam_incidence_count": len(incidences),
            "adjacent_chart_seam_incidences": incidences,
            "adjacent_chart_seam_p_span_exhaustive": True,
            "rechart_route_status": (
                "EXACT_ENDPOINT_CARRIER_RETAINED__RECHART_ROUTE_PENDING"
            ),
            "certified_carrier_dimension": 1,
            "carrier_existence_status": "CERTIFIED_EXACT_ENDPOINT_CARRIER",
        }

    require(box is not None and c40.endpoint_phase(box) is not None,
            "rational p endpoint exact phase")
    if box.p0 == -1:
        sigma = -1
        interior_p = box.p1
        endpoint_side = "P_LOWER"
    else:
        require(box.p1 == 1, "rational endpoint p=+/-1")
        sigma = 1
        interior_p = box.p0
        endpoint_side = "P_UPPER"
    radial_ratio = Q(sigma) * interior_p
    require(-1 < radial_ratio <= 1, "stereographic endpoint interior ratio")
    u_squared_max = (1 - radial_ratio) / (1 + radial_ratio)
    require(u_squared_max >= 0, "stereographic u squared interval")
    return {
        "endpoint_kind": "RATIONAL_P_ENDPOINT_STEREOGRAPHIC_RECHART",
        "sigma": sigma,
        "exact_p_endpoint": str(sigma),
        "endpoint_side": endpoint_side,
        "source_radical_equation": "q_source^2=1-p^2",
        "stereographic_coordinate_domain": "u>=0",
        "stereographic_p_formula": "p=sigma*(1-u^2)/(1+u^2)",
        "stereographic_q_formula": "q_source=2*u/(1+u^2)",
        "unit_circle_identity": (
            "(sigma*(1-u^2)/(1+u^2))^2"
            "+(2*u/(1+u^2))^2=1"
        ),
        "unit_circle_identity_exact_polynomial": (
            "(1-u^2)^2+4*u^2=(1+u^2)^2"
        ),
        "closed_t_interval": [qstr(box.t0), qstr(box.t1)],
        "closed_p_interval": [qstr(box.p0), qstr(box.p1)],
        "closed_u_squared_interval": ["0", qstr(u_squared_max)],
        "u_zero_endpoint_owner": "ENDPOINT_RECHART_OWNS_U_EQUALS_ZERO",
        "positive_u_ambient_owner": "AMBIENT_CELL_OWNS_U_GREATER_THAN_ZERO",
        "half_open_endpoint_dedup_complete": True,
        "route_failure": route["route_failure"],
        "rechart_route_status": (
            "EXACT_ENDPOINT_CARRIER_RETAINED__RECHART_ROUTE_PENDING"
        ),
        "transformed_route_evaluator_status": "PENDING",
        "certified_carrier_dimension": 1,
        "carrier_existence_status": "CERTIFIED_EXACT_ENDPOINT_CARRIER",
    }


def exact_face_box(box: Any, face: str) -> dict[str, list[str]]:
    payload = box_payload(box)
    require(payload is not None, "exact face rational box")
    axis = face[0]
    endpoint = 0 if face.endswith("lower") else 1
    payload[axis] = [payload[axis][endpoint], payload[axis][endpoint]]
    return payload


def exact_corner_box(box: Any, corner: str) -> dict[str, list[str]]:
    payload = box_payload(box)
    require(payload is not None, "exact corner rational box")
    t_endpoint = int(corner[1])
    p_endpoint = int(corner[3])
    payload["t"] = [payload["t"][t_endpoint], payload["t"][t_endpoint]]
    payload["p"] = [payload["p"][p_endpoint], payload["p"][p_endpoint]]
    return payload


def make_outer_rows(
    task: dict[str, Any],
    ambient_identity: dict[str, Any],
    residual: str,
    route: dict[str, Any],
    split_link: dict[str, Any] | None,
) -> dict[str, list[dict[str, Any]]]:
    surfaces = surface_summaries(route)
    normalized: list[dict[str, Any]] = []
    for ordinal, surface in enumerate(surfaces):
        candidate_id = "c41-normalized-surface:" + digest({
            "ambient": ambient_identity,
            "ordinal": ordinal,
            "kind": surface.get("kind"),
            "identifier": surface.get("identifier"),
            "equation": surface.get("equation"),
        })
        normalized.append({
            "schema": NORMALIZED_SURFACE_REGISTRY_SCHEMA + ".entry",
            "normalized_surface_id": candidate_id,
            "surface_ordinal": ordinal,
            **surface,
            "candidate_carrier_expected_dimension": 1,
            "certified_carrier_dimension": (
                1 if surface.get("certified_nonempty_regular_graph") else None
            ),
            "ambient_or_whole_parent_credit": 0,
            "D02_gate_credit": 0,
        })

    common = {
        "pair_index": ambient_identity["pair_index"],
        "c40_source_leaf_id": ambient_identity["c40_source_leaf_id"],
        "descendant_path": ambient_identity["path"],
        "residual_classification": residual,
        "raw_classification": route["classification"],
        "raw_witness": route["witness"],
        "route_failure": route["route_failure"],
        "normalized_surface_count": len(normalized),
        "normalized_surfaces": normalized,
        "normalized_surface_registry_schema": (
            NORMALIZED_SURFACE_REGISTRY_SCHEMA
        ),
        "normalized_surface_registry_storage": (
            "NESTED_ONE_ENTRY_PER_SURFACE_INSIDE_OWNING_PRIMARY_OUTER_ROW"
        ),
        "normalized_surface_registry_foreign_key": (
            "normalized_surface_id__SCOPED_TO_OWNING_PRIMARY_OUTER_ID"
        ),
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    groups = {
        "c1": [], "endpoint": [], "c2": [],
        "incidence": [], "boundary": [],
    }
    if "SOURCE_RADICAL" in residual or "ALGEBRAIC_H0" in residual:
        schema = ENDPOINT_SCHEMA
        id_field = "endpoint_rechart_id"
        prefix = "c41-endpoint-rechart:"
        group = "endpoint"
    elif "COLLISION2" in residual:
        schema = C2_OUTER_SCHEMA
        id_field = "c2_surface_outer_id"
        prefix = "c41-c2-outer:"
        group = "c2"
    else:
        schema = C1_OUTER_SCHEMA
        id_field = "c1_h1_surface_outer_id"
        prefix = "c41-c1-h1-outer:"
        group = "c1"
    endpoint_payload = (
        endpoint_rechart_payload(task, route, residual)
        if group == "endpoint" else None
    )
    primary = {
        "schema": schema,
        **common,
        "carrier_existence_status": (
            endpoint_payload["carrier_existence_status"]
            if endpoint_payload is not None
            else "UNRESOLVED_STRATIFIED_SURFACE_OUTER"
        ),
        "certified_carrier_dimension": (
            endpoint_payload["certified_carrier_dimension"]
            if endpoint_payload is not None else None
        ),
        "candidate_intersection_rank_status": None,
        "endpoint_rechart_geometry": endpoint_payload,
    }
    primary[id_field] = prefix + digest(primary)
    groups[group].append(primary)
    primary_id = primary[id_field]
    orthogonal_endpoint_ids: list[str] = []
    if (
        group != "endpoint"
        and route["box"] is not None
        and c40.endpoint_phase(route["box"]) is not None
    ):
        orthogonal_geometry = endpoint_rechart_payload(task, route, residual)
        endpoint_outer = {
            "schema": ENDPOINT_SCHEMA,
            **common,
            "normalized_surface_count": 0,
            "normalized_surfaces": [],
            "carrier_existence_status": orthogonal_geometry[
                "carrier_existence_status"
            ],
            "certified_carrier_dimension": orthogonal_geometry[
                "certified_carrier_dimension"
            ],
            "candidate_intersection_rank_status": None,
            "endpoint_rechart_geometry": orthogonal_geometry,
            "orthogonal_to_primary_residual": True,
            "owning_primary_outer_id": primary_id,
        }
        endpoint_outer["endpoint_rechart_id"] = (
            "c41-endpoint-rechart:" + digest(endpoint_outer)
        )
        groups["endpoint"].append(endpoint_outer)
        orthogonal_endpoint_ids.append(endpoint_outer["endpoint_rechart_id"])

    for left, right in itertools.combinations(normalized, 2):
        incidence = {
            "schema": INCIDENCE_SCHEMA,
            "pair_index": ambient_identity["pair_index"],
            "c40_source_leaf_id": ambient_identity["c40_source_leaf_id"],
            "descendant_path": ambient_identity["path"],
            "owning_outer_id": primary_id,
            "left_normalized_surface_id": left["normalized_surface_id"],
            "right_normalized_surface_id": right["normalized_surface_id"],
            "classification": (
                "UNRESOLVED_C41_PAIR_INCIDENCE_KRAWCZYK_PENDING"
            ),
            "candidate_incidence_expected_dimension": 0,
            "certified_intersection_dimension": None,
            "intersection_existence": None,
            "rank_status": None,
            "ambient_or_whole_parent_credit": 0,
            "D02_gate_credit": 0,
        }
        incidence["incidence_outer_id"] = "c41-incidence:" + digest(incidence)
        groups["incidence"].append(incidence)

    box = route["box"]
    face_rows: list[dict[str, Any]] = []
    corner_rows: list[dict[str, Any]] = []
    if box is not None:
        for face in ("t_lower", "t_upper", "p_lower", "p_upper"):
            is_last_split_face = bool(
                split_link is not None
                and split_link["shared_face"] == face
            )
            face_semantic = {
                "face": face,
                "exact_closed_face_box": exact_face_box(box, face),
                "face_dimension_in_s0_slice": 1,
                "last_split_face": is_last_split_face,
                "split_face_adjacency_id": (
                    split_link["split_face_adjacency_id"]
                    if is_last_split_face else None
                ),
                "sibling_path": (
                    split_link["sibling_path"] if is_last_split_face else None
                ),
                "half_open_face_role": (
                    split_link["half_open_role"]
                    if is_last_split_face
                    else "GLOBAL_FACE_OWNER_PENDING_INCIDENCE_CENSUS"
                ),
                "global_face_owner_rule": (
                    "LEXICOGRAPHIC_MINIMUM_AMBIENT_PATH_AMONG_INCIDENT_CELLS"
                ),
                "global_face_owner_resolved": False,
                "surface_face_incidence_links": [],
                "face_ambient_credit": 0,
                "D02_gate_credit": 0,
            }
            face_semantic["boundary_face_id"] = "c41-boundary-face:" + digest({
                "ambient": ambient_identity,
                **face_semantic,
            })
            for surface in normalized:
                link = {
                    "boundary_face_id": face_semantic["boundary_face_id"],
                    "normalized_surface_id": surface[
                        "normalized_surface_id"
                    ],
                    "candidate_intersection_expected_dimension": 0,
                    "certified_intersection_dimension": None,
                    "intersection_existence": None,
                    "rank_status": None,
                    "classification": "SURFACE_FACE_INCIDENCE_OUTER_PENDING",
                    "ambient_or_whole_parent_credit": 0,
                    "D02_gate_credit": 0,
                }
                link["surface_face_incidence_id"] = (
                    "c41-surface-face-incidence:" + digest(link)
                )
                face_semantic["surface_face_incidence_links"].append(link)
            face_rows.append(face_semantic)
        for corner in ("t0p0", "t0p1", "t1p0", "t1p1"):
            corner_semantic = {
                "corner": corner,
                "exact_closed_corner_box": exact_corner_box(box, corner),
                "corner_dimension_in_s0_slice": 0,
                "global_corner_owner_rule": (
                    "LEXICOGRAPHIC_MINIMUM_AMBIENT_PATH_AMONG_INCIDENT_CELLS"
                ),
                "global_corner_owner_resolved": False,
                "half_open_corner_role": "GLOBAL_CORNER_OWNER_PENDING_INCIDENCE_CENSUS",
                "surface_corner_incidence_status": (
                    "SURFACE_CORNER_CENSUS_PENDING"
                ),
                "corner_ambient_credit": 0,
                "D02_gate_credit": 0,
            }
            corner_semantic["boundary_corner_id"] = (
                "c41-boundary-corner-point:" + digest({
                    "ambient": ambient_identity,
                    **corner_semantic,
                })
            )
            corner_rows.append(corner_semantic)
    boundary = {
        "schema": BOUNDARY_SCHEMA,
        "pair_index": ambient_identity["pair_index"],
        "c40_source_leaf_id": ambient_identity["c40_source_leaf_id"],
        "descendant_path": ambient_identity["path"],
        "owning_outer_id": primary_id,
        "face_family": ["t_lower", "t_upper", "p_lower", "p_upper"],
        "corner_family": ["t0p0", "t0p1", "t1p0", "t1p1"],
        "exact_face_row_count": len(face_rows),
        "exact_corner_row_count": len(corner_rows),
        "face_rows": face_rows,
        "corner_rows": corner_rows,
        "face_intersection_status": "FACE_RESTRICTION_PENDING",
        "corner_intersection_status": "CORNER_CENSUS_PENDING",
        "exact_rational_face_and_corner_geometry_complete": box is not None,
        "global_sibling_adjacency_and_half_open_owner_complete": False,
        "boundary_and_corner_inventory_complete": False,
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    boundary["boundary_corner_outer_id"] = "c41-boundary-corner:" + digest(
        boundary
    )
    groups["boundary"].append(boundary)
    groups["obligation_ids"] = [[
        primary_id,
        *orthogonal_endpoint_ids,
        *[row["incidence_outer_id"] for row in groups["incidence"]],
        boundary["boundary_corner_outer_id"],
    ]]
    return groups


def make_ambient_row(
    task: dict[str, Any],
    route: dict[str, Any],
    descendant_bits: str,
    additional_depth: int,
    fraction: Q,
    axis_history: list[str],
) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    source = task["source"]
    box = route["box"]
    classification = route["classification"]
    family = disposition_family(classification)
    identity = {
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "path": source["path"] + descendant_bits,
        "parent_volume_fraction": qstr(fraction),
    }
    residual = residual_classification(classification) if family == "RESIDUAL_OUTER" else None
    groups: dict[str, list[dict[str, Any]]] = {
        "c1": [], "endpoint": [], "c2": [],
        "incidence": [], "boundary": [], "obligation_ids": [[]],
    }
    if residual is not None:
        split_link: dict[str, Any] | None = None
        if descendant_bits:
            parent_bits = descendant_bits[:-1]
            parent_path = source["path"] + parent_bits
            parent_box, _active = c39.reconstruct_box(task["cell"], parent_path)
            adjacency, _children, axis = split_row(
                task,
                parent_box,
                parent_bits,
                additional_depth - 1,
                axis_history[:-1],
            )
            bit = descendant_bits[-1]
            axis_name = ("t", "p", "s")[axis]
            require(axis_name in {"t", "p"}, "s=0 split axis is in-slice")
            split_link = {
                "split_face_adjacency_id": adjacency[
                    "split_face_adjacency_id"
                ],
                "sibling_path": source["path"] + parent_bits + (
                    "1" if bit == "0" else "0"
                ),
                "shared_face": axis_name + (
                    "_upper" if bit == "0" else "_lower"
                ),
                "half_open_role": (
                    "OWNS_SHARED_SPLIT_FACE"
                    if bit == "0" else "EXCLUDES_DUPLICATE_SHARED_SPLIT_FACE"
                ),
            }
        groups = make_outer_rows(
            task, identity, residual, route, split_link
        )
    semantic = {
        "schema": AMBIENT_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "c40_source_classification": source["classification"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "descendant_bits": descendant_bits,
        "path": identity["path"],
        "additional_depth": additional_depth,
        "split_axis_history": axis_history,
        "parent_volume_fraction": qstr(fraction),
        "closed_representative_box": box_payload(box),
        "closed_reflected_box": reflected_box(
            task["c38_source"]["representative_origin_key"], box
        ),
        "half_open_owner_policy": (
            "LOWER_BIT_OWNS_SHARED_SPLIT_FACE__UPPER_BIT_EXCLUDES"
        ),
        "raw_classification": classification,
        "raw_witness": route["witness"],
        "route_method": route["route_method"],
        "disposition_family": family,
        "residual_classification": residual,
        "route_failure": route["route_failure"],
        "c2_status": route["c2_status"],
        "c2_baseline": route["c2_baseline"],
        "obligation_ids": groups["obligation_ids"][0],
        "round144_terminal_class": (
            "EARLIEST_PREFIX_EXCLUDED"
            if family == "TERMINAL_EXCLUDED"
            else "UNRESOLVED_R1648_CONTINUATION"
        ),
        "local_round144_terminal_credit": (
            1 if family == "TERMINAL_EXCLUDED" else 0
        ),
        "lower_dimensional_ambient_credit": 0,
        "collision3_ready_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["c41_ambient_cell_id"] = "c41-ambient:" + digest(semantic)
    return semantic, groups


def split_row(
    task: dict[str, Any],
    box: Any,
    descendant_bits: str,
    additional_depth: int,
    axis_history: list[str],
) -> tuple[dict[str, Any], tuple[Any, Any], int]:
    axis = c38.round166.longest_axis(box)
    children = c38.round166.split_axis(box, axis)
    axis_name = ("t", "p", "s")[axis]
    lower, upper = (
        (box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1)
    )[axis]
    middle = (lower + upper) / 2
    source = task["source"]
    semantic = {
        "schema": SPLIT_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "parent_descendant_bits": descendant_bits,
        "parent_path": source["path"] + descendant_bits,
        "additional_depth_before_split": additional_depth,
        "split_axis": axis_name,
        "exact_split_coordinate": qstr(middle),
        "parent_closed_box": box_payload(box),
        "lower_child_path": source["path"] + descendant_bits + "0",
        "upper_child_path": source["path"] + descendant_bits + "1",
        "lower_child_closed_box": box_payload(children[0]),
        "upper_child_closed_box": box_payload(children[1]),
        "axis_history_before_split": axis_history,
        "half_open_shared_face_owner": "LOWER_BIT_CHILD",
        "lower_child_fraction_multiplier": "1/2",
        "upper_child_fraction_multiplier": "1/2",
        "exact_split_conservation": "1",
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["split_face_adjacency_id"] = "c41-split:" + digest(semantic)
    return semantic, children, axis


def make_cache_replay_row(
    source: dict[str, Any],
    repaired_route: dict[str, Any],
) -> dict[str, Any]:
    require(
        repaired_route["route_failure"] is None
        and repaired_route["c1_result"] is not None,
        "cache replay repaired without exception",
    )
    repaired_c1_classification = repaired_route["c1_result"]["classification"]
    require(
        repaired_route["classification"] in EXPECTED_CACHE_REPLAY_CENSUS,
        "19-row full cache replay disposition",
    )
    semantic = {
        "schema": CACHE_REPLAY_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "old_exception_type": source["route_exception_type"],
        "old_exception_message": source["route_exception_message"],
        "required_chart": "W:W",
        "official_candidate_count": 55,
        "official_candidate_ids_sha256": EXPECTED_CHART_CANDIDATES["W:W"][1],
        "repaired_C39_c1_classification": repaired_c1_classification,
        "repaired_C39_c1_witness": repaired_route["c1_result"]["witness"],
        "replay_classification": repaired_route["classification"],
        "replay_witness": repaired_route["witness"],
        "replay_exception": None,
        "disposition_family": "COLLISION3_READY",
        "collision3_ready_credit": 0,
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["cache_replay_id"] = "c41-cache-replay:" + digest(semantic)
    return semantic


def process_task(task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    source = task["source"]
    source_fraction = Q(source["parent_volume_fraction"])
    packet: dict[str, Any] = {
        "source_ordinal": task["source_ordinal"],
        "source_leaf_id": source["c40_leaf_id"],
        "ambient": [], "split": [], "cache_replay": [],
        "c1": [], "endpoint": [], "c2": [],
        "incidence": [], "boundary": [],
    }
    if source["representative_box"] is None:
        route = {
            "box": None,
            "classification": "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL",
            "witness": source["witness"],
            "route_method": "C41_EXACT_ALGEBRAIC_H0_RECHART_OUTER",
            "c1_result": None,
            "c2_status": None,
            "c2_baseline": None,
            "c2_detail": None,
            "c2_evidence": [],
            "route_failure": None,
        }
        ambient, groups = make_ambient_row(
            task, route, "", 0, source_fraction, []
        )
        packet["ambient"].append(ambient)
        for key in ("c1", "endpoint", "c2", "incidence", "boundary"):
            packet[key].extend(groups[key])
        return packet

    original_route = route_at_path(task, source["path"], config)
    require(
        box_payload(original_route["box"]) == source["representative_box"],
        "C40 source box replay equality",
    )
    if source["classification"] == (
        "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
    ):
        packet["cache_replay"].append(
            make_cache_replay_row(source, original_route)
        )

    # Strict exclusions may stop before depth three.  Every other source is
    # split until depth three, including collision-three-ready descendants.
    stack: list[tuple[str, int, Q, list[str], dict[str, Any] | None]] = [
        ("", 0, source_fraction, [], original_route)
    ]
    while stack:
        bits, depth, fraction, history, cached_route = stack.pop()
        path = source["path"] + bits
        route = cached_route or route_at_path(task, path, config)
        family = disposition_family(route["classification"])
        if family == "TERMINAL_EXCLUDED" or depth == EXTRA_DEPTH:
            ambient, groups = make_ambient_row(
                task, route, bits, depth, fraction, history
            )
            packet["ambient"].append(ambient)
            for key in ("c1", "endpoint", "c2", "incidence", "boundary"):
                packet[key].extend(groups[key])
            continue
        adjacency, children, axis = split_row(
            task, route["box"], bits, depth, history
        )
        packet["split"].append(adjacency)
        axis_name = ("t", "p", "s")[axis]
        # Reverse push preserves lexical path order in the emitted packet.
        for bit in ("1", "0"):
            child_path = path + bit
            child_route = route_at_path(task, child_path, config)
            require(
                box_payload(child_route["box"])
                == box_payload(children[int(bit)]),
                "exact split/reconstruction equality",
            )
            stack.append((
                bits + bit,
                depth + 1,
                fraction / 2,
                history + [axis_name],
                child_route,
            ))

    packet["ambient"].sort(key=lambda row: row["path"])
    paths = [row["path"] for row in packet["ambient"]]
    require(
        len(paths) == len(set(paths))
        and not any(
            left != right and right.startswith(left)
            for left, right in itertools.product(paths, repeat=2)
        ),
        "source descendant prefix-free",
    )
    require(
        sum(Q(row["parent_volume_fraction"]) for row in packet["ambient"])
        == source_fraction,
        "source descendant Fraction conservation",
    )
    return packet


def worker(input_path: Path, output_path: Path, config_path: Path) -> None:
    source_pins()
    ctx.prec = PRECISION_BITS
    install_complete_immutable_cache()
    config = decode_worker_config(strict_json(config_path))
    require(not output_path.exists(), "worker output exists")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw = output_path.open("wb")
    stream = gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0)
    try:
        with gzip.open(input_path, "rt", encoding="utf-8") as source:
            prior_ordinal = -1
            for line in source:
                task = json.loads(line)
                require(
                    task["source_ordinal"] > prior_ordinal,
                    "worker source ordinal order",
                )
                prior_ordinal = task["source_ordinal"]
                packet = process_task(task, config)
                packet["packet_sha256"] = digest(packet)
                stream.write(canonical(packet) + b"\n")
    finally:
        stream.close()
        raw.close()


def worker_packets(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        prior = -1
        for line in stream:
            packet = json.loads(line)
            packet_sha = packet.pop("packet_sha256", None)
            require(packet_sha == digest(packet), "worker packet closure")
            require(packet["source_ordinal"] > prior, "worker packet order")
            prior = packet["source_ordinal"]
            yield packet


def merge_worker_packets(paths: list[Path]) -> Iterator[dict[str, Any]]:
    iterators = [worker_packets(path) for path in paths]
    heap: list[tuple[int, int, dict[str, Any]]] = []
    for index, iterator in enumerate(iterators):
        try:
            packet = next(iterator)
        except StopIteration:
            continue
        heap.append((packet["source_ordinal"], index, packet))
    heapq.heapify(heap)
    prior = -1
    while heap:
        ordinal, index, packet = heapq.heappop(heap)
        require(ordinal > prior, "merged packet ordinal uniqueness")
        prior = ordinal
        yield packet
        try:
            following = next(iterators[index])
        except StopIteration:
            continue
        heapq.heappush(heap, (following["source_ordinal"], index, following))


def task_for_row(
    ordinal: int,
    source: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    c38_source = context["c38_index"].get(source["c38_source_row_sha256"])
    require(c38_source is not None, "C40 to C38 source binding")
    cell = context["cells"].get(source["representative_cell_id"])
    require(cell is not None, "C40 to C32 cell binding")
    seams = sorted(
        context["seams_by_cell"].get(cell["cell_id"], []),
        key=lambda row: (
            Q(row["physical_p_span"][0]["value"]),
            Q(row["physical_p_span"][1]["value"]),
            row["row_sha256"],
        ),
    )
    if source["representative_box"] is None:
        require(bool(seams), "algebraic endpoint seam incidence nonempty")
    return {
        "source_ordinal": ordinal,
        "source": source,
        "c38_source": c38_source,
        "cell": cell,
        "seams": seams if source["representative_box"] is None else [],
    }


def input_crosswalk_row(
    ordinal: int,
    source: dict[str, Any],
) -> dict[str, Any]:
    residual = residual_classification(source["classification"])
    semantic = {
        "schema": CROSSWALK_SCHEMA,
        "c40_source_ordinal": ordinal,
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": source["c38_source_row_sha256"],
        "pair_index": source["pair_index"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "source_parent_volume_fraction": source["parent_volume_fraction"],
        "source_classification": source["classification"],
        "normalized_residual_classification": residual,
        "route_exception_phase": source["route_exception_phase"],
        "route_exception_type": source["route_exception_type"],
        "route_exception_message": source["route_exception_message"],
        "selected_exactly_once": True,
        "depth_policy": (
            "STRICT_EXCLUSION_EARLY_STOP_OTHERWISE_EXACTLY_THREE_DYADIC_SPLITS"
        ),
        "maximum_additional_depth": EXTRA_DEPTH,
        "input_ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["input_crosswalk_id"] = "c41-input:" + digest(semantic)
    return semantic


def write_task_shards(
    stage: Path,
    candidate: Path,
    result: dict[str, Any],
    context: dict[str, Any],
) -> tuple[list[Path], dict[str, Any], Counter[str]]:
    work = stage / ".worker"
    work.mkdir()
    paths = [work / f"input-{index}.jsonl.gz" for index in range(SHARD_COUNT)]
    raws = [path.open("wb") for path in paths]
    streams = [
        gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0)
        for raw in raws
    ]
    crosswalk = LedgerWriter(
        stage / "input_blocker_crosswalk.jsonl.gz", "C40_ROW_ORDER"
    )
    classification_census: Counter[str] = Counter()
    terminal = ready = selected = total = 0
    try:
        with crosswalk:
            for ordinal, source in enumerate(iter_ledger(
                candidate, result["ledgers"]["routed_leaf_cells"]
            )):
                require(source["pair_index"] in range(862), "C40 pair range")
                total += 1
                classification_census[source["classification"]] += 1
                family = disposition_family(source["classification"])
                if family == "TERMINAL_EXCLUDED":
                    terminal += 1
                    require(
                        source["local_round144_terminal_credit"] == 1,
                        "C40 terminal carry credit",
                    )
                elif family == "COLLISION3_READY":
                    ready += 1
                    require(
                        source["local_round144_terminal_credit"] == 0,
                        "C40 collision3 carry zero credit",
                    )
                else:
                    require(is_lower_blocker(source), "unexpected C40 residual")
                    selected += 1
                    crosswalk.write(input_crosswalk_row(ordinal, source))
                    task = task_for_row(ordinal, source, context)
                    streams[ordinal % SHARD_COUNT].write(canonical(task) + b"\n")
    finally:
        for stream in streams:
            stream.close()
        for raw in raws:
            raw.close()
    require(
        total == EXPECTED_C40_ROW_COUNT
        and terminal == EXPECTED_C40_TERMINAL_ROW_COUNT
        and ready == EXPECTED_C40_COLLISION3_READY_ROW_COUNT
        and selected == EXPECTED_LOWER_BLOCKER_COUNT
        and crosswalk.count == EXPECTED_LOWER_BLOCKER_COUNT,
        "exact C40 input partition",
    )
    require(
        {key: classification_census[key] for key in LOWER_BLOCKER_CENSUS}
        == LOWER_BLOCKER_CENSUS,
        "exact lower blocker census",
    )
    census = {
        "C40_routed_leaf_count": total,
        "C40_terminal_carry_count": terminal,
        "C40_collision3_ready_carry_count": ready,
        "selected_lower_blocker_count": selected,
    }
    return paths, census, classification_census


def run_worker_shards(
    stage: Path,
    input_paths: list[Path],
    config: dict[str, Any],
) -> list[Path]:
    work = stage / ".worker"
    config_path = work / "config.json"
    write_json(config_path, config)
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONHASHSEED"] = "0"
    environment["PYTHONPATH"] = str(DELIVERABLES) + (
        os.pathsep + environment["PYTHONPATH"]
        if environment.get("PYTHONPATH") else ""
    )
    outputs: list[Path] = []
    processes: list[tuple[subprocess.Popen[bytes], Any, Any, Path]] = []
    for index, input_path in enumerate(input_paths):
        output_path = work / f"output-{index}.jsonl.gz"
        stdout_path = work / f"stdout-{index}.log"
        stderr_path = work / f"stderr-{index}.log"
        stdout = stdout_path.open("wb")
        stderr = stderr_path.open("wb")
        process = subprocess.Popen(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker-input", str(input_path),
                "--worker-output", str(output_path),
                "--worker-config", str(config_path),
            ],
            cwd=ROOT,
            env=environment,
            stdout=stdout,
            stderr=stderr,
        )
        processes.append((process, stdout, stderr, stderr_path))
        outputs.append(output_path)
    failures: list[str] = []
    for index, (process, stdout, stderr, stderr_path) in enumerate(processes):
        code = process.wait()
        stdout.close()
        stderr.close()
        if code != 0:
            failures.append(
                f"worker {index} exit {code}:"
                + stderr_path.read_text(
                    encoding="utf-8", errors="replace"
                )[-8000:]
            )
        else:
            require(
                stdout_path.stat().st_size == 0
                and stderr_path.stat().st_size == 0,
                f"worker {index} success streams must be empty",
            )
    require(not failures, "\n".join(failures))
    require(all(path.is_file() for path in outputs), "worker output inventory")
    return outputs


def carry_ambient_row(source: dict[str, Any]) -> dict[str, Any]:
    family = disposition_family(source["classification"])
    require(
        family in {"TERMINAL_EXCLUDED", "COLLISION3_READY"},
        "carry family",
    )
    semantic = {
        "schema": AMBIENT_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "c40_source_classification": source["classification"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "descendant_bits": "",
        "path": source["path"],
        "additional_depth": 0,
        "split_axis_history": [],
        "parent_volume_fraction": source["parent_volume_fraction"],
        "closed_representative_box": source["representative_box"],
        "closed_reflected_box": source["reflected_box"],
        "half_open_owner_policy": "C40_FROZEN_PREFIX_CARRY",
        "raw_classification": source["classification"],
        "raw_witness": source["witness"],
        "route_method": "C41_C40_FROZEN_PREFIX_CARRY",
        "disposition_family": family,
        "residual_classification": None,
        "route_failure": source["route_failure"],
        "c2_status": None,
        "c2_baseline": None,
        "obligation_ids": [],
        "round144_terminal_class": source["round144_terminal_class"],
        "local_round144_terminal_credit": (
            1 if family == "TERMINAL_EXCLUDED" else 0
        ),
        "lower_dimensional_ambient_credit": 0,
        "collision3_ready_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["c41_ambient_cell_id"] = "c41-ambient:" + digest(semantic)
    return semantic


def singleton_rows(
    generated: dict[str, tuple[str, ...]],
) -> Iterator[dict[str, Any]]:
    pair_index, _pattern_index, registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    require(registry_sha == EXPECTED_OFFICIAL_REGISTRY_SHA256,
            "singleton official registry")
    count = 0
    for chart in CHART_ORDER:
        for ordinal, target_id in enumerate(generated[chart]):
            key = (chart, target_id)
            require(key in pair_index, "singleton registry foreign key")
            semantic = {
                "schema": SINGLETON_SCHEMA,
                "chart_id": chart,
                "chart_candidate_ordinal": ordinal,
                "target_id": target_id,
                "official_pair_key_index": pair_index[key],
                "chart_candidate_count": len(generated[chart]),
                "chart_candidate_ids_sha256": EXPECTED_CHART_CANDIDATES[chart][1],
                "official_registry_sha256": registry_sha,
                "immutable_full_chart_cache": True,
                "singleton_ambient_or_whole_parent_credit": 0,
                "D02_gate_credit": 0,
            }
            semantic["candidate_singleton_id"] = (
                "c41-candidate-singleton:" + digest(semantic)
            )
            count += 1
            yield semantic
    require(count == 448, "candidate singleton census")


def require_row_id(
    row: dict[str, Any],
    field: str,
    prefix: str,
    label: str,
) -> None:
    semantic = dict(row)
    observed = semantic.pop(field, None)
    require(observed == prefix + digest(semantic), f"row ID closure:{label}")


def exact_axis_history(task: dict[str, Any], bits: str) -> list[str]:
    source_path = task["source"]["path"]
    history: list[str] = []
    for depth in range(len(bits)):
        parent, _active = c39.reconstruct_box(
            task["cell"], source_path + bits[:depth]
        )
        axis = c38.round166.longest_axis(parent)
        axis_name = ("t", "p", "s")[axis]
        require(axis_name in {"t", "p"}, "exact history s=0 split")
        history.append(axis_name)
    return history


def packet_obligation_check(
    packet: dict[str, Any],
    task: dict[str, Any],
) -> None:
    source = task["source"]
    require(
        packet["source_ordinal"] == task["source_ordinal"]
        and packet["source_leaf_id"] == source["c40_leaf_id"],
        "packet task/source closure",
    )
    ambient_by_path: dict[str, dict[str, Any]] = {}
    leaf_bits: list[str] = []
    for ambient in packet["ambient"]:
        bits = ambient["descendant_bits"]
        require(
            type(bits) is str
            and set(bits) <= {"0", "1"}
            and len(bits) == ambient["additional_depth"]
            and len(bits) <= EXTRA_DEPTH
            and ambient["path"] == source["path"] + bits
            and ambient["source_path"] == source["path"]
            and ambient["pair_index"] == source["pair_index"]
            and ambient["c40_source_leaf_id"] == source["c40_leaf_id"]
            and ambient["c40_source_row_sha256"] == source["row_sha256"]
            and ambient["representative_cell_id"]
            == source["representative_cell_id"]
            and ambient["reflected_cell_id"] == source["reflected_cell_id"]
            and Q(ambient["parent_volume_fraction"])
            == Q(source["parent_volume_fraction"]) / (2 ** len(bits))
            and ambient["split_axis_history"]
            == ([] if source["representative_box"] is None
                else exact_axis_history(task, bits)),
            "ambient task/path/Fraction closure",
        )
        if source["representative_box"] is None:
            require(
                bits == ""
                and ambient["closed_representative_box"] is None
                and ambient["closed_reflected_box"] is None,
                "algebraic ambient exact closure",
            )
        else:
            reconstructed, _active = c39.reconstruct_box(
                task["cell"], ambient["path"]
            )
            require(
                ambient["closed_representative_box"]
                == box_payload(reconstructed)
                and ambient["closed_reflected_box"] == reflected_box(
                    task["c38_source"]["representative_origin_key"],
                    reconstructed,
                ),
                "ambient representative/reflected exact box closure",
            )
        require_row_id(
            ambient, "c41_ambient_cell_id", "c41-ambient:", "ambient"
        )
        require(ambient["path"] not in ambient_by_path,
                "ambient path uniqueness")
        ambient_by_path[ambient["path"]] = ambient
        leaf_bits.append(bits)
    ordered_leaf_bits = sorted(leaf_bits)
    require(
        not any(
            right.startswith(left)
            for left, right in zip(ordered_leaf_bits, ordered_leaf_bits[1:])
        )
        and sum(
            (Q(row["parent_volume_fraction"])
             for row in packet["ambient"]),
            Q(0),
        ) == Q(source["parent_volume_fraction"]),
        "ambient prefix-free exact source Fraction conservation",
    )

    split_by_bits: dict[str, dict[str, Any]] = {}
    for row in packet["split"]:
        bits = row["parent_descendant_bits"]
        require(
            type(bits) is str
            and set(bits) <= {"0", "1"}
            and len(bits) < EXTRA_DEPTH
            and row["parent_path"] == source["path"] + bits
            and row["pair_index"] == source["pair_index"]
            and row["c40_source_leaf_id"] == source["c40_leaf_id"]
            and row["additional_depth_before_split"] == len(bits)
            and row["axis_history_before_split"]
            == exact_axis_history(task, bits)
            and row["lower_child_fraction_multiplier"] == "1/2"
            and row["upper_child_fraction_multiplier"] == "1/2",
            "split task/path/Fraction metadata closure",
        )
        parent, _active = c39.reconstruct_box(task["cell"], row["parent_path"])
        axis = c38.round166.longest_axis(parent)
        axis_name = ("t", "p", "s")[axis]
        children = c38.round166.split_axis(parent, axis)
        interval = (
            (parent.t0, parent.t1),
            (parent.p0, parent.p1),
            (parent.s0, parent.s1),
        )[axis]
        require(
            axis_name in {"t", "p"}
            and row["split_axis"] == axis_name
            and row["exact_split_coordinate"] == qstr(
                (interval[0] + interval[1]) / 2
            )
            and row["parent_closed_box"] == box_payload(parent)
            and row["lower_child_path"] == source["path"] + bits + "0"
            and row["upper_child_path"] == source["path"] + bits + "1"
            and row["lower_child_closed_box"] == box_payload(children[0])
            and row["upper_child_closed_box"] == box_payload(children[1]),
            "split parent/axis/children exact box closure",
        )
        require_row_id(
            row,
            "split_face_adjacency_id",
            "c41-split:",
            "split face adjacency",
        )
        require(bits not in split_by_bits, "split parent uniqueness")
        split_by_bits[bits] = row
    expected_split_bits = {
        bits[:depth]
        for bits in leaf_bits
        for depth in range(len(bits))
    }
    require(
        set(split_by_bits) == expected_split_bits,
        "split tree equals ambient leaf prefix closure",
    )

    id_fields = {
        "c1": "c1_h1_surface_outer_id",
        "endpoint": "endpoint_rechart_id",
        "c2": "c2_surface_outer_id",
        "incidence": "incidence_outer_id",
        "boundary": "boundary_corner_outer_id",
    }
    by_path: dict[str, set[str]] = defaultdict(set)
    endpoint_by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    primary_by_id: dict[str, dict[str, Any]] = {}
    normalized_by_id: dict[str, tuple[str, dict[str, Any]]] = {}
    all_ids: list[str] = []
    for group, id_field in id_fields.items():
        for row in packet[group]:
            value = row[id_field]
            path = row["descendant_path"]
            require(value not in by_path[path], "duplicate local obligation id")
            by_path[path].add(value)
            all_ids.append(value)
            if group in {"c1", "endpoint", "c2"}:
                primary_by_id[value] = row
            if group == "endpoint":
                endpoint_by_path[path].append(row)
            require(
                row["ambient_or_whole_parent_credit"] == 0
                and row["D02_gate_credit"] == 0,
                "lower stratum zero credit",
            )
            if group == "c1":
                require_row_id(row, id_field, "c41-c1-h1-outer:", group)
            elif group == "endpoint":
                require_row_id(row, id_field, "c41-endpoint-rechart:", group)
            elif group == "c2":
                require_row_id(row, id_field, "c41-c2-outer:", group)
            elif group == "incidence":
                require_row_id(row, id_field, "c41-incidence:", group)
            else:
                require_row_id(
                    row, id_field, "c41-boundary-corner:", group
                )
    require(len(all_ids) == len(set(all_ids)), "packet obligation uniqueness")
    for primary_id, primary in primary_by_id.items():
        path = primary["descendant_path"]
        ambient = ambient_by_path.get(path)
        require(
            ambient is not None
            and primary["pair_index"] == ambient["pair_index"]
            and primary["c40_source_leaf_id"]
            == ambient["c40_source_leaf_id"]
            and primary["residual_classification"]
            == ambient["residual_classification"]
            and primary["normalized_surface_registry_schema"]
            == NORMALIZED_SURFACE_REGISTRY_SCHEMA
            and primary["normalized_surface_registry_storage"]
            == "NESTED_ONE_ENTRY_PER_SURFACE_INSIDE_OWNING_PRIMARY_OUTER_ROW"
            and primary["normalized_surface_count"]
            == len(primary["normalized_surfaces"]),
            "primary outer to ambient and nested registry closure",
        )
        identity = {
            "pair_index": ambient["pair_index"],
            "c40_source_leaf_id": ambient["c40_source_leaf_id"],
            "path": ambient["path"],
            "parent_volume_fraction": ambient["parent_volume_fraction"],
        }
        for ordinal, surface in enumerate(primary["normalized_surfaces"]):
            expected_surface_id = "c41-normalized-surface:" + digest({
                "ambient": identity,
                "ordinal": ordinal,
                "kind": surface.get("kind"),
                "identifier": surface.get("identifier"),
                "equation": surface.get("equation"),
            })
            require(
                surface["schema"]
                == NORMALIZED_SURFACE_REGISTRY_SCHEMA + ".entry"
                and surface["surface_ordinal"] == ordinal
                and surface["normalized_surface_id"] == expected_surface_id
                and expected_surface_id not in normalized_by_id,
                "nested normalized surface row ID/ordinal closure",
            )
            normalized_by_id[expected_surface_id] = (primary_id, surface)
    for ambient in packet["ambient"]:
        require(
            ambient["lower_dimensional_ambient_credit"] == 0
            and ambient["collision3_ready_credit"] == 0
            and ambient["D02_gate_credit"] == 0,
            "ambient strict zero-credit fields",
        )
        obligations = ambient["obligation_ids"]
        if ambient["disposition_family"] == "RESIDUAL_OUTER":
            require(
                obligations
                and set(obligations) == by_path[ambient["path"]]
                and len(obligations) == len(set(obligations)),
                "residual obligation foreign keys",
            )
            box = ambient["closed_representative_box"]
            rational_p_endpoint = bool(
                box is not None
                and (box["p"][0] == "-1" or box["p"][1] == "1")
            )
            algebraic_endpoint = box is None
            require(
                len(endpoint_by_path[ambient["path"]])
                == int(rational_p_endpoint or algebraic_endpoint),
                "endpoint carrier is an orthogonal ambient obligation",
            )
        else:
            require(not obligations and ambient["path"] not in by_path,
                    "nonresidual has no lower obligation")
    require(
        len(packet["ambient"]) == len(packet["split"]) + 1,
        "binary split leaf/internal conservation",
    )
    for row in packet["split"]:
        require(
            row["exact_split_conservation"] == "1"
            and row["ambient_or_whole_parent_credit"] == 0
            and row["D02_gate_credit"] == 0,
            "split exact zero-credit conservation",
        )
    split_ids = {
        row["split_face_adjacency_id"] for row in packet["split"]
    }
    for row in packet["incidence"]:
        owner = row["owning_outer_id"]
        left = row["left_normalized_surface_id"]
        right = row["right_normalized_surface_id"]
        require(owner in primary_by_id, "incidence owning primary FK")
        primary = primary_by_id[owner]
        ambient = ambient_by_path[primary["descendant_path"]]
        require(
            row["pair_index"] == primary["pair_index"]
            == ambient["pair_index"]
            and row["c40_source_leaf_id"]
            == primary["c40_source_leaf_id"]
            == ambient["c40_source_leaf_id"]
            and row["descendant_path"]
            == primary["descendant_path"]
            == ambient["path"]
            and left in normalized_by_id
            and right in normalized_by_id
            and left != right
            and normalized_by_id[left][0] == owner
            and normalized_by_id[right][0] == owner
            and row["classification"]
            == "UNRESOLVED_C41_PAIR_INCIDENCE_KRAWCZYK_PENDING"
            and row["certified_intersection_dimension"] is None
            and row["intersection_existence"] is None
            and row["rank_status"] is None,
            "incidence owning primary and normalized-surface FK closure",
        )
    for row in packet["boundary"]:
        require(
            row["boundary_and_corner_inventory_complete"] is False
            and row[
                "global_sibling_adjacency_and_half_open_owner_complete"
            ] is False,
            "boundary outer honest partial status",
        )
        require(row["owning_outer_id"] in primary_by_id,
                "boundary owning primary FK")
        primary = primary_by_id[row["owning_outer_id"]]
        ambient = ambient_by_path[row["descendant_path"]]
        require(
            row["pair_index"] == primary["pair_index"]
            == ambient["pair_index"]
            and row["c40_source_leaf_id"]
            == primary["c40_source_leaf_id"]
            == ambient["c40_source_leaf_id"]
            and row["descendant_path"]
            == primary["descendant_path"]
            == ambient["path"],
            "boundary pair/source/path owning primary and ambient closure",
        )
        identity = {
            "pair_index": ambient["pair_index"],
            "c40_source_leaf_id": ambient["c40_source_leaf_id"],
            "path": ambient["path"],
            "parent_volume_fraction": ambient["parent_volume_fraction"],
        }
        normalized_ids = {
            surface["normalized_surface_id"]
            for surface in primary["normalized_surfaces"]
        }
        if row["exact_rational_face_and_corner_geometry_complete"]:
            require(
                row["exact_face_row_count"] == 4
                and row["exact_corner_row_count"] == 4,
                "exact four-face/four-corner materialization",
            )
        else:
            require(
                row["exact_face_row_count"] == 0
                and row["exact_corner_row_count"] == 0,
                "nonrational boundary retained incomplete",
            )
        for face in row["face_rows"]:
            face_semantic = dict(face)
            face_id = face_semantic.pop("boundary_face_id", None)
            links = face_semantic["surface_face_incidence_links"]
            face_semantic["surface_face_incidence_links"] = []
            require(
                face_id == "c41-boundary-face:" + digest({
                    "ambient": identity,
                    **face_semantic,
                }),
                "boundary face row ID closure",
            )
            if face["last_split_face"]:
                require(
                    face["split_face_adjacency_id"] in split_ids
                    and face["half_open_face_role"] in {
                        "OWNS_SHARED_SPLIT_FACE",
                        "EXCLUDES_DUPLICATE_SHARED_SPLIT_FACE",
                    },
                    "boundary to split adjacency foreign key",
                )
            for link in links:
                require_row_id(
                    link,
                    "surface_face_incidence_id",
                    "c41-surface-face-incidence:",
                    "surface-face incidence",
                )
                require(
                    link["boundary_face_id"] == face_id
                    and link["normalized_surface_id"] in normalized_by_id
                    and normalized_by_id[
                        link["normalized_surface_id"]
                    ][0] == row["owning_outer_id"],
                    "surface-face incidence owning primary/link closure",
                )
            require(
                {
                    link["normalized_surface_id"]
                    for link in face["surface_face_incidence_links"]
                } == normalized_ids
                and all(
                    link["certified_intersection_dimension"] is None
                    and link["intersection_existence"] is None
                    and link["rank_status"] is None
                    and link["ambient_or_whole_parent_credit"] == 0
                    and link["D02_gate_credit"] == 0
                    for link in face["surface_face_incidence_links"]
                ),
                "surface-face incidence exact foreign keys and null status",
            )
        for corner in row["corner_rows"]:
            corner_semantic = dict(corner)
            corner_id = corner_semantic.pop("boundary_corner_id", None)
            require(
                corner_id == "c41-boundary-corner-point:" + digest({
                    "ambient": identity,
                    **corner_semantic,
                }),
                "boundary corner row ID closure",
            )
    for row in packet["endpoint"]:
        geometry = row["endpoint_rechart_geometry"]
        require(
            row["carrier_existence_status"]
            == "CERTIFIED_EXACT_ENDPOINT_CARRIER"
            and row["certified_carrier_dimension"] == 1
            and geometry["rechart_route_status"]
            == "EXACT_ENDPOINT_CARRIER_RETAINED__RECHART_ROUTE_PENDING"
            and row["ambient_or_whole_parent_credit"] == 0
            and row["D02_gate_credit"] == 0,
            "endpoint exact carrier but route pending zero credit",
        )
        if row.get("orthogonal_to_primary_residual"):
            require(
                row["owning_primary_outer_id"] in primary_by_id
                and primary_by_id[row["owning_primary_outer_id"]]
                ["descendant_path"] == row["descendant_path"],
                "orthogonal endpoint to primary outer foreign key",
            )
        if geometry["endpoint_kind"] == (
            "RATIONAL_P_ENDPOINT_STEREOGRAPHIC_RECHART"
        ):
            require(
                geometry["sigma"] in {-1, 1}
                and geometry["stereographic_coordinate_domain"] == "u>=0"
                and geometry["transformed_route_evaluator_status"] == "PENDING",
                "rational stereographic endpoint self-contained",
            )
        else:
            require(
                geometry["endpoint_kind"]
                == "ALGEBRAIC_H0_SOURCE_CHART_SEAM"
                and geometry["minimal_polynomial"] == "2*x^2-1"
                and geometry["adjacent_chart_seam_p_span_exhaustive"],
                "algebraic H0 endpoint self-contained",
            )
    for row in packet["cache_replay"]:
        require_row_id(
            row, "cache_replay_id", "c41-cache-replay:", "cache replay"
        )
        require(
            row["replay_exception"] is None
            and row["official_candidate_count"] == 55
            and row["collision3_ready_credit"] == 0
            and row["ambient_or_whole_parent_credit"] == 0
            and row["D02_gate_credit"] == 0,
            "cache micro-ledger strict fields",
        )


def accumulate_parent(
    accumulators: dict[int, dict[str, Any]],
    row: dict[str, Any],
) -> None:
    pair = row["pair_index"]
    value = accumulators[pair]
    fraction = Q(row["parent_volume_fraction"])
    require(fraction > 0, "positive ambient Fraction")
    value["paths"].append(row["path"])
    value["total"] += fraction
    if row["disposition_family"] == "TERMINAL_EXCLUDED":
        value["terminal"] += fraction
        value["terminal_leaf_count"] += 1
        value["terminal_reflection_materialized"] = bool(
            value["terminal_reflection_materialized"]
            and row["closed_reflected_box"] is not None
        )
    else:
        value["nonterminal_leaf_count"] += 1


def write_parent_ledger(
    writer: LedgerWriter,
    accumulators: dict[int, dict[str, Any]],
    prior_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    prior = {row["pair_index"]: row for row in prior_rows}
    require(len(prior) == 862, "C40 parent index")
    full = partial = zero = newly_full = 0
    terminal_equivalent = Q(0)
    unresolved_equivalent = Q(0)
    with writer:
        for pair in range(862):
            value = accumulators[pair]
            paths = sorted(value["paths"])
            require(
                paths
                and len(paths) == len(set(paths))
                and not any(
                    right.startswith(left)
                    for left, right in zip(paths, paths[1:])
                ),
                f"pair prefix-free:{pair}",
            )
            total = value["total"]
            terminal = value["terminal"]
            unresolved = total - terminal
            require(total == 1 and unresolved >= 0,
                    f"pair exact Kraft:{pair}:{total}")
            old = prior[pair]
            prior_terminal = Q(old["terminal_excluded_parent_volume"])
            require(terminal >= prior_terminal, "terminal volume monotonicity")
            whole = (
                terminal == 1
                and value["nonterminal_leaf_count"] == 0
                and value["terminal_reflection_materialized"]
            )
            if terminal == 1:
                require(whole, "whole pair reflection transport")
            if whole:
                full += 1
            elif terminal == 0:
                zero += 1
            else:
                partial += 1
            newly = whole and not old["whole_representative_parent_terminal"]
            newly_full += int(newly)
            terminal_equivalent += terminal
            unresolved_equivalent += unresolved
            writer.write({
                "schema": PARENT_SCHEMA,
                "pair_index": pair,
                "c40_parent_row_sha256": old["row_sha256"],
                "leaf_count": len(paths),
                "terminal_leaf_count": value["terminal_leaf_count"],
                "nonterminal_leaf_count": value["nonterminal_leaf_count"],
                "path_prefix_free": True,
                "terminal_excluded_parent_volume": qstr(terminal),
                "unresolved_parent_volume": qstr(unresolved),
                "parent_Kraft_conservation": "1",
                "whole_representative_parent_terminal": whole,
                "whole_reflected_parent_terminal": whole,
                "terminal_reflection_transport_materialized": value[
                    "terminal_reflection_materialized"
                ],
                "newly_whole_terminal_vs_C40": newly,
                "C34_common_refinement_credit": 2 if whole else 0,
                "lower_dimensional_credit": 0,
                "D02_gate_credit": 0,
            })
    require(
        writer.count == 862
        and full + partial + zero == 862
        and full >= 250
        and newly_full == full - 250
        and terminal_equivalent + unresolved_equivalent == 862,
        "global parent conservation",
    )
    return {
        "whole_terminal_representative_parent_count": full,
        "whole_terminal_paired_coarse_cell_count": 2 * full,
        "newly_whole_terminal_representative_parent_count": newly_full,
        "newly_whole_terminal_paired_coarse_cell_count": 2 * newly_full,
        "partial_representative_parent_count": partial,
        "zero_progress_representative_parent_count": zero,
        "representative_terminal_parent_equivalent": qstr(terminal_equivalent),
        "representative_unresolved_parent_equivalent": qstr(
            unresolved_equivalent
        ),
    }


def build(
    output: Path,
    candidate: Path,
    audit_path: Path,
) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    ctx.prec = PRECISION_BITS
    context = load_context(candidate, audit_path, formal=True)
    c40_result = context["result"]
    pins = source_pins()
    generated = install_complete_immutable_cache()
    worker_config = context["config"]
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    renamed = False
    try:
        input_paths, input_census, input_classifications = write_task_shards(
            stage, candidate, c40_result, context
        )
        output_paths = run_worker_shards(stage, input_paths, worker_config)
        writers = {
            "ambient": LedgerWriter(
                stage / "routed_ambient_cells.jsonl.gz",
                "C40_ROW_ORDER_THEN_DESCENDANT_PATH",
            ),
            "split": LedgerWriter(
                stage / "split_face_adjacency.jsonl.gz",
                "C40_ROW_ORDER_THEN_PARENT_PATH",
            ),
            "cache_replay": LedgerWriter(
                stage / "full_chart_cache_replay.jsonl.gz", "C40_ROW_ORDER"
            ),
            "singleton": LedgerWriter(
                stage / "candidate_universe_singletons.jsonl.gz",
                "CHART_ORDER_THEN_CANDIDATE_ORDINAL",
            ),
            "c1": LedgerWriter(
                stage / "c1_h1_surface_outers.jsonl.gz",
                "C40_ROW_ORDER_THEN_DESCENDANT_PATH",
            ),
            "endpoint": LedgerWriter(
                stage / "endpoint_recharts.jsonl.gz",
                "C40_ROW_ORDER_THEN_DESCENDANT_PATH",
            ),
            "c2": LedgerWriter(
                stage / "c2_surface_outers.jsonl.gz",
                "C40_ROW_ORDER_THEN_DESCENDANT_PATH",
            ),
            "incidence": LedgerWriter(
                stage / "incidence_outers.jsonl.gz",
                "C40_ROW_ORDER_THEN_DESCENDANT_PATH",
            ),
            "boundary": LedgerWriter(
                stage / "boundary_corner_outers.jsonl.gz",
                "C40_ROW_ORDER_THEN_DESCENDANT_PATH",
            ),
        }
        accumulators: dict[int, dict[str, Any]] = {
            pair: {
                "paths": [],
                "total": Q(0),
                "terminal": Q(0),
                "terminal_leaf_count": 0,
                "nonterminal_leaf_count": 0,
                "terminal_reflection_materialized": True,
            }
            for pair in range(862)
        }
        raw_census: Counter[str] = Counter()
        disposition_census: Counter[str] = Counter()
        residual_census: Counter[str] = Counter()
        cache_census: Counter[str] = Counter()
        endpoint_kind_census: Counter[str] = Counter()
        algebraic_seam_incidence_count = 0
        packet_iterator = merge_worker_packets(output_paths)
        next_packet = next(packet_iterator, None)
        with ExitStack() as stack:
            for writer in writers.values():
                stack.enter_context(writer)
            for row in singleton_rows(generated):
                writers["singleton"].write(row)
            for ordinal, source in enumerate(iter_ledger(
                candidate, c40_result["ledgers"]["routed_leaf_cells"]
            )):
                if is_lower_blocker(source):
                    require(
                        next_packet is not None
                        and next_packet["source_ordinal"] == ordinal
                        and next_packet["source_leaf_id"] == source["c40_leaf_id"],
                        "selected packet exact merge",
                    )
                    packet = next_packet
                    packet_obligation_check(
                        packet, task_for_row(ordinal, source, context)
                    )
                    for ambient in packet["ambient"]:
                        writers["ambient"].write(ambient)
                        accumulate_parent(accumulators, ambient)
                        raw_census[ambient["raw_classification"]] += 1
                        disposition_census[ambient["disposition_family"]] += 1
                        if ambient["residual_classification"] is not None:
                            residual_census[ambient["residual_classification"]] += 1
                    for group in (
                        "split", "cache_replay", "c1", "endpoint", "c2",
                        "incidence", "boundary",
                    ):
                        for item in packet[group]:
                            writers[group].write(item)
                            if group == "cache_replay":
                                cache_census[item["replay_classification"]] += 1
                            elif group == "endpoint":
                                endpoint_geometry = item[
                                    "endpoint_rechart_geometry"
                                ]
                                endpoint_kind_census[
                                    endpoint_geometry["endpoint_kind"]
                                ] += 1
                                algebraic_seam_incidence_count += (
                                    endpoint_geometry.get(
                                        "adjacent_chart_seam_incidence_count", 0
                                    )
                                )
                    next_packet = next(packet_iterator, None)
                else:
                    ambient = carry_ambient_row(source)
                    writers["ambient"].write(ambient)
                    accumulate_parent(accumulators, ambient)
                    raw_census[ambient["raw_classification"]] += 1
                    disposition_census[ambient["disposition_family"]] += 1
        require(next_packet is None, "no surplus worker packets")
        require(
            writers["singleton"].count == 448
            and writers["cache_replay"].count == 19
            and dict(sorted(cache_census.items()))
            == EXPECTED_CACHE_REPLAY_CENSUS
            and writers["ambient"].count <= 121_795
            and writers["split"].count <= 86_786
            and endpoint_kind_census[
                "ALGEBRAIC_H0_SOURCE_CHART_SEAM"
            ] == 29
            and algebraic_seam_incidence_count == 33,
            "depth-three and cache replay census bounds",
        )
        shutil.rmtree(stage / ".worker")

        parent_writer = LedgerWriter(
            stage / "parent_conservation.jsonl.gz", "PAIR_INDEX_ASCENDING"
        )
        prior_parents = list(iter_ledger(
            candidate, c40_result["ledgers"]["parent_conservation"]
        ))
        parent_census = write_parent_ledger(
            parent_writer, accumulators, prior_parents
        )
        full_count = parent_census[
            "whole_terminal_representative_parent_count"
        ]
        formal_excluded = 74_812 + 2 * full_count
        formal_unresolved = 1_724 - 2 * full_count
        require(
            formal_excluded + 296 + formal_unresolved == 76_832
            and 0 <= formal_unresolved <= 1_224,
            "formal terminal census conservation",
        )
        (stage / "C41_LOWER_STRATA_PARTIAL.lock").write_text(
            "C41 performs a fixed maximum of three exact dyadic ambient splits "
            "after C40, repairs the omitted W:W candidate cache, and materializes "
            "surface, endpoint, incidence, boundary, corner and conservation "
            "outers. Only complete uniformly excluded closed ambient parents earn "
            "paired coarse-cell credit. Every graph, endpoint, seam, incidence, "
            "corner, collision-three-ready or evaluation-failure obligation earns "
            "zero D02/D03/D04/Gate5/CM2 credit. This object is partial.\n",
            encoding="utf-8",
        )
        crosswalk_descriptor = {
            "filename": "input_blocker_crosswalk.jsonl.gz",
            "order": "C40_ROW_ORDER",
            "row_count": EXPECTED_LOWER_BLOCKER_COUNT,
            "row_hash_line_sequence_sha256": None,
            "sha256": file_sha256(stage / "input_blocker_crosswalk.jsonl.gz"),
            "size": (stage / "input_blocker_crosswalk.jsonl.gz").stat().st_size,
        }
        # Recover the sequence digest without retaining 12,398 input rows.
        sequence = hashlib.sha256()
        count = 0
        with gzip.open(
            stage / "input_blocker_crosswalk.jsonl.gz", "rt", encoding="utf-8"
        ) as stream:
            for line in stream:
                row = json.loads(line)
                sequence.update((row["row_sha256"] + "\n").encode("ascii"))
                count += 1
        require(count == EXPECTED_LOWER_BLOCKER_COUNT, "crosswalk replay count")
        crosswalk_descriptor["row_hash_line_sequence_sha256"] = (
            sequence.hexdigest()
        )
        ledger_descriptors = {
            "input_blocker_crosswalk": crosswalk_descriptor,
            "routed_ambient_cells": writers["ambient"].descriptor(),
            "split_face_adjacency": writers["split"].descriptor(),
            "full_chart_cache_replay": writers["cache_replay"].descriptor(),
            "candidate_universe_singletons": writers["singleton"].descriptor(),
            "c1_h1_surface_outers": writers["c1"].descriptor(),
            "endpoint_recharts": writers["endpoint"].descriptor(),
            "c2_surface_outers": writers["c2"].descriptor(),
            "incidence_outers": writers["incidence"].descriptor(),
            "boundary_corner_outers": writers["boundary"].descriptor(),
            "parent_conservation": parent_writer.descriptor(),
        }
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__"
                f"{writers['ambient'].count}_AMBIENT_LEAVES__"
                f"{2 * full_count}_WHOLE_CELLS_TERMINAL__"
                f"{formal_unresolved}_FORMAL_UNRESOLVED"
            ),
            "C40_authority": {
                "path": str(candidate.resolve().relative_to(ROOT)),
                "object_sha256": c40_result["object_sha256"],
                "independent_audit_path": str(
                    audit_path.resolve().relative_to(ROOT)
                ),
                "independent_audit_object_sha256": context["audit"][
                    "object_sha256"
                ],
                "independent_audit_status": context["audit"]["status"],
            },
            "numeric_authority": {
                "source_sha256": pins,
                "flint_version": flint.__version__,
                "precision_bits": PRECISION_BITS,
                "maximum_additional_dyadic_depth": EXTRA_DEPTH,
                "strict_exclusion_early_stop": True,
                "official_registry_sha256": EXPECTED_OFFICIAL_REGISTRY_SHA256,
                "upstream_authority_object_sha256": context[
                    "upstream_authority_objects"
                ],
                "full_chart_candidate_cache": {
                    chart: {
                        "candidate_count": EXPECTED_CHART_CANDIDATES[chart][0],
                        "candidate_ids_sha256": EXPECTED_CHART_CANDIDATES[chart][1],
                    }
                    for chart in CHART_ORDER
                },
                "full_chart_candidate_count": 448,
                "candidate_cache_immutable": True,
                "tuple_codec": "CANONICAL_JSON_LIST_OF_STRINGS_COLLISION_FREE",
                "source_slice": "s=0",
            },
            "input_census": {
                **input_census,
                "C40_classification_census": dict(
                    sorted(input_classifications.items())
                ),
                "selected_lower_blocker_classification_census": (
                    LOWER_BLOCKER_CENSUS
                ),
            },
            "routing_census": {
                "routed_ambient_cell_count": writers["ambient"].count,
                "split_face_adjacency_count": writers["split"].count,
                "raw_classification_census": dict(sorted(raw_census.items())),
                "disposition_family_census": dict(
                    sorted(disposition_census.items())
                ),
                "normalized_residual_classification_census": dict(
                    sorted(residual_census.items())
                ),
                "full_chart_cache_replay_count": writers[
                    "cache_replay"
                ].count,
                "full_chart_cache_replay_census": dict(
                    sorted(cache_census.items())
                ),
                **parent_census,
            },
            "lower_strata_census": {
                "normalized_surface_registry_schema": (
                    NORMALIZED_SURFACE_REGISTRY_SCHEMA
                ),
                "normalized_surface_registry_storage": (
                    "NESTED_ONE_ENTRY_PER_SURFACE_INSIDE_OWNING_PRIMARY_OUTER_ROW"
                ),
                "normalized_surface_registry_scope": (
                    "normalized_surface_id FOREIGN KEY is scoped to exactly one "
                    "owning C1/H1 or C2 primary outer row; incidence and face "
                    "links must bind that same owning primary"
                ),
                "candidate_universe_singleton_count": writers[
                    "singleton"
                ].count,
                "c1_h1_surface_outer_count": writers["c1"].count,
                "endpoint_rechart_count": writers["endpoint"].count,
                "endpoint_rechart_kind_census": dict(
                    sorted(endpoint_kind_census.items())
                ),
                "algebraic_H0_endpoint_rechart_count": 29,
                "algebraic_C32_seam_incidence_count": (
                    algebraic_seam_incidence_count
                ),
                "c2_surface_outer_count": writers["c2"].count,
                "incidence_outer_count": writers["incidence"].count,
                "boundary_corner_outer_count": writers["boundary"].count,
                "certified_zero_dimensional_intersection_count": 0,
                "lower_dimensional_ambient_credit": 0,
                "D02_gate_credit": 0,
            },
            "ledgers": ledger_descriptors,
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "EARLIEST_PREFIX_EXCLUDED": formal_excluded,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": formal_unresolved,
                "terminal_total": 76_832,
                "unresolved_zero": formal_unresolved == 0,
            },
            "strict_nonpromotion": {
                "lower_dimensional_graph_credit": 0,
                "endpoint_seam_incidence_corner_ambient_credit": 0,
                "collision3_ready_credit": 0,
                "four_class_terminal_census_unresolved_zero": False,
                "D02": (
                    f"BLOCKED_BY_{formal_unresolved}_COMPLETE_R1648_CONTINUATIONS"
                ),
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "execution_receipt_policy": (
                "out-of-band self-hashed receipt binds InvocationID/PID to this "
                "deterministic object and root manifest without polluting replay bytes"
            ),
            "required_next": (
                "close every retained C1/H1/endpoint/C2/incidence/boundary/corner "
                "outer and continue every collision-three-ready branch through "
                "collisions 3--1648 before any D02 promotion"
            ),
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        write_manifest(stage)
        require(
            sorted(path.name for path in stage.iterdir())
            == list(CANDIDATE_INVENTORY),
            "exact fourteen-file candidate inventory",
        )
        validate_manifest(stage)
        replay = strict_json(stage / "result.json")
        validate_self_object(replay, "C41 pre-rename")
        require(replay == result, "C41 pre-rename exact result replay")
        for path in sorted(stage.iterdir()):
            fsync_file(path)
        fsync_directory(stage)
        fsync_directory(output.parent)
        os.rename(stage, output)
        renamed = True
        fsync_directory(output.parent)
        replay = validate_c41_candidate(output, result)
        require(
            replay == result
            and sorted(path.name for path in output.iterdir())
            == list(CANDIDATE_INVENTORY),
            "C41 terminal byte/inventory replay",
        )
        return result
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        if renamed:
            shutil.rmtree(output, ignore_errors=True)
            fsync_directory(output.parent)
        raise


def process_start_ticks(pid: int) -> int:
    fields = (Path("/proc") / str(pid) / "stat").read_text(
        encoding="ascii"
    ).split()
    value = int(fields[21])
    require(value > 0, "process start ticks")
    return value


def write_receipt(
    path: Path,
    invocation_id: str,
    pid: int,
    start_ticks: int,
    output: Path,
    result: dict[str, Any],
) -> dict[str, Any]:
    require(INVOCATION.fullmatch(invocation_id) is not None,
            "InvocationID syntax")
    require(not path.exists(), f"receipt exists:{path}")
    require(
        pid == os.getpid() and process_start_ticks(pid) == start_ticks,
        "live PID/start binding",
    )
    validate_c41_candidate(output, result)
    semantic = {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS_LIVE_PID_INVOCATION_BOUND_TO_C41_OBJECT",
        "InvocationID": invocation_id,
        "producer_pid": pid,
        "producer_parent_pid": os.getppid(),
        "producer_proc_start_ticks": start_ticks,
        "producer_executable": str(Path(sys.executable).resolve()),
        "producer_source_sha256": file_sha256(Path(__file__).resolve()),
        "candidate_path": str(output.resolve().relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "root_manifest_sha256": file_sha256(output / "root_manifest.sha256"),
        "candidate_inventory_count": 14,
    }
    semantic["receipt_object_sha256"] = digest(semantic)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    payload = canonical(semantic) + b"\n"
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            require(written > 0, "receipt short write made no progress")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    fsync_directory(path.parent)
    require_regular_single_link(path, "C41 execution receipt")
    require(path.read_bytes() == payload, "receipt terminal byte replay")
    replay = strict_json(path)
    observed = replay.pop("receipt_object_sha256", None)
    require(
        observed == semantic["receipt_object_sha256"]
        and observed == digest(replay),
        "receipt self object replay",
    )
    validate_c41_candidate(output, result)
    return semantic


def discover_candidate() -> Path:
    matches: list[Path] = []
    for directory in sorted(
        (RUNTIME / "candidates").glob("c40-h1-endpoint-c2-arrangement-*")
    ):
        result_path = directory / "result.json"
        if not result_path.is_file():
            continue
        try:
            value = strict_json(result_path)
        except Exception:
            continue
        if value.get("object_sha256") == EXPECTED_C40_OBJECT:
            matches.append(directory)
    require(bool(matches), "pinned C40 candidate not found")
    return matches[-1]


def scan_candidate(
    candidate: Path,
    context: dict[str, Any],
    retain_limit: int = 0,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = context["result"]
    total = terminal = ready = selected = 0
    lower: Counter[str] = Counter()
    retained: list[dict[str, Any]] = []
    for ordinal, source in enumerate(iter_ledger(
        candidate, result["ledgers"]["routed_leaf_cells"]
    )):
        total += 1
        family = disposition_family(source["classification"])
        if family == "TERMINAL_EXCLUDED":
            terminal += 1
        elif family == "COLLISION3_READY":
            ready += 1
        else:
            require(is_lower_blocker(source), "scan unexpected residual")
            selected += 1
            lower[source["classification"]] += 1
            if len(retained) < retain_limit:
                retained.append(task_for_row(ordinal, source, context))
    require(
        total == EXPECTED_C40_ROW_COUNT
        and terminal == EXPECTED_C40_TERMINAL_ROW_COUNT
        and ready == EXPECTED_C40_COLLISION3_READY_ROW_COUNT
        and selected == EXPECTED_LOWER_BLOCKER_COUNT
        and dict(sorted(lower.items())) == LOWER_BLOCKER_CENSUS,
        "pilot exact C40 partition",
    )
    return {
        "C40_routed_leaf_count": total,
        "terminal_carry_count": terminal,
        "collision3_ready_carry_count": ready,
        "selected_lower_blocker_count": selected,
        "selected_lower_blocker_census": dict(sorted(lower.items())),
    }, retained


def pilot_cache_replay(candidate: Path, context: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = PRECISION_BITS
    install_complete_immutable_cache()
    config = decode_worker_config(context["config"])
    census: Counter[str] = Counter()
    micro_ids: set[str] = set()
    count = 0
    for ordinal, source in enumerate(iter_ledger(
        candidate, context["result"]["ledgers"]["routed_leaf_cells"]
    )):
        if source["classification"] != (
            "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
        ):
            continue
        task = task_for_row(ordinal, source, context)
        route = route_at_path(task, source["path"], config)
        micro = make_cache_replay_row(source, route)
        require(micro["cache_replay_id"] not in micro_ids,
                "cache micro-ledger id uniqueness")
        micro_ids.add(micro["cache_replay_id"])
        census[micro["replay_classification"]] += 1
        count += 1
    require(
        count == 19
        and dict(sorted(census.items())) == EXPECTED_CACHE_REPLAY_CENSUS,
        "pilot exact 19-row cache replay",
    )
    return {
        "cache_replay_count": count,
        "cache_micro_ledger_unique_id_count": len(micro_ids),
        "cache_replay_census": dict(sorted(census.items())),
        "W:W_candidate_count": EXPECTED_CHART_CANDIDATES["W:W"][0],
        "W:W_candidate_ids_sha256": EXPECTED_CHART_CANDIDATES["W:W"][1],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--invocation-id")
    parser.add_argument("--worker-input", type=Path)
    parser.add_argument("--worker-output", type=Path)
    parser.add_argument("--worker-config", type=Path)
    parser.add_argument("--pilot-scan", action="store_true")
    parser.add_argument("--pilot-cache-replay", action="store_true")
    parser.add_argument("--pilot-limit", type=int, default=0)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.worker_input is not None:
        require(
            arguments.worker_output is not None
            and arguments.worker_config is not None,
            "worker output/config",
        )
        worker(
            arguments.worker_input.resolve(),
            arguments.worker_output.resolve(),
            arguments.worker_config.resolve(),
        )
        return 0
    if arguments.self_test:
        pins = source_pins()
        generated = install_complete_immutable_cache()
        print(canonical({
            "status": "PASS_C41_STATIC_SELF_TEST",
            "source_sha256": pins,
            "chart_candidate_counts": {
                chart: len(generated[chart]) for chart in CHART_ORDER
            },
            "full_chart_candidate_count": sum(map(len, generated.values())),
        }).decode("utf-8"))
        return 0
    candidate = (arguments.candidate or discover_candidate()).resolve()
    if (
        arguments.pilot_scan
        or arguments.pilot_cache_replay
        or arguments.pilot_limit
    ):
        context = load_context(candidate, None, formal=False)
        payload: dict[str, Any] = {
            "status": "PASS_C41_READ_ONLY_PILOT",
            "candidate": str(candidate.relative_to(ROOT)),
        }
        if arguments.pilot_scan or arguments.pilot_limit:
            require(arguments.pilot_limit >= 0, "pilot nonnegative limit")
            scan, retained = scan_candidate(
                candidate, context, arguments.pilot_limit
            )
            payload["input_scan"] = scan
            if retained:
                ctx.prec = PRECISION_BITS
                generated = install_complete_immutable_cache()
                config = decode_worker_config(context["config"])
                singleton_inventory = list(singleton_rows(generated))
                require(
                    len(singleton_inventory) == 448
                    and len({
                        row["candidate_singleton_id"]
                        for row in singleton_inventory
                    }) == 448,
                    "pilot normalized singleton registry",
                )
                prior_parent = {
                    row["pair_index"]: Q(
                        row["terminal_excluded_parent_volume"]
                    )
                    for row in iter_ledger(
                        candidate,
                        context["result"]["ledgers"]["parent_conservation"],
                    )
                }
                terminal_gain: dict[int, Q] = defaultdict(Q)
                packet_census: Counter[str] = Counter()
                outer_census: Counter[str] = Counter()
                ambient_count = split_count = 0
                for task in retained:
                    packet = process_task(task, config)
                    packet_obligation_check(packet, task)
                    ambient_count += len(packet["ambient"])
                    split_count += len(packet["split"])
                    for group in (
                        "cache_replay", "c1", "endpoint", "c2",
                        "incidence", "boundary",
                    ):
                        outer_census[group] += len(packet[group])
                    terminal_gain[task["source"]["pair_index"]] += sum(
                        (
                            Q(row["parent_volume_fraction"])
                            for row in packet["ambient"]
                            if row["disposition_family"]
                            == "TERMINAL_EXCLUDED"
                        ),
                        Q(0),
                    )
                    packet_census.update(
                        row["disposition_family"] for row in packet["ambient"]
                    )
                require(
                    all(
                        prior_parent[pair] <= prior_parent[pair] + gain <= 1
                        for pair, gain in terminal_gain.items()
                    ),
                    "pilot projected parent terminal monotonicity",
                )
                payload["depth3_sample"] = {
                    "source_count": len(retained),
                    "ambient_count": ambient_count,
                    "split_count": split_count,
                    "outer_ledger_row_census": dict(
                        sorted(outer_census.items())
                    ),
                    "normalized_singleton_registry_count": len(
                        singleton_inventory
                    ),
                    "projected_parent_monotonicity_checked_count": len(
                        terminal_gain
                    ),
                    "disposition_family_census": dict(
                        sorted(packet_census.items())
                    ),
                }
        if arguments.pilot_cache_replay:
            payload["cache_replay"] = pilot_cache_replay(candidate, context)
        print(canonical(payload).decode("utf-8"))
        return 0
    require(arguments.output is not None, "output")
    require(arguments.audit is not None, "C40 independent audit")
    require(arguments.receipt is not None, "receipt")
    require(arguments.invocation_id is not None, "InvocationID")
    pid = os.getpid()
    start_ticks = process_start_ticks(pid)
    candidate, audit_path, output, receipt_path = formal_path_preflight(
        candidate,
        arguments.audit,
        arguments.output,
        arguments.receipt,
        pid,
    )
    result = build(
        output, candidate, audit_path
    )
    try:
        receipt = write_receipt(
            receipt_path,
            arguments.invocation_id,
            pid,
            start_ticks,
            output,
            result,
        )
        validate_c41_candidate(output, result)
    except Exception as error:
        # A deterministic candidate without its live-PID receipt is never left
        # behind as apparent authority.  Both paths were preflighted in-workspace.
        if output.exists():
            shutil.rmtree(output)
            fsync_directory(output.parent)
        if receipt_path.exists():
            require_regular_single_link(receipt_path, "failed receipt cleanup")
            receipt_path.unlink()
            fsync_directory(receipt_path.parent)
        raise RuntimeError(
            "receipt failure removed orphan C41 candidate fail-closed"
        ) from error
    print(canonical({
        "result": result,
        "execution_receipt": receipt,
    }).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
