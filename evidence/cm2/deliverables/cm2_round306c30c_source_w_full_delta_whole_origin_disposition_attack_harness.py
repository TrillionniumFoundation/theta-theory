#!/usr/bin/env python3
"""Coherent-corruption rejection harness for candidate-only C30c.

The baseline is first accepted by the pinned independent verifier.  Each
attack then rewrites all directly dependent row hashes, ledger descriptors,
and the result self-hash, so rejection cannot be attributed merely to a stale
checksum.  No attack success or baseline pass grants formal credit.
"""
from __future__ import annotations

import argparse
import ast
import ctypes
import errno
import gzip
import hashlib
import importlib.machinery
import json
import os
import shutil
import stat
import sys
import tempfile
import types
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
COMBINED = PREFIX + "_delta_h_cell_ledger.jsonl.gz"
INHERITED_H = PREFIX + "_inherited_h_cell_ledger.jsonl.gz"
JOIN = PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz"
ORIGINS = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
RUNTIME = "cm2_round306c30b_python_flint_runtime_attestation.json"
EXPECTED_FILES = {COMBINED, INHERITED_H, JOIN, ORIGINS, RESULT, RUNTIME}
VERIFIER = PREFIX + "_independent_verifier.py"
PRODUCER = PREFIX + "_producer.py"
PRODUCER_SHA256 = (
    "4644f8aad5fb9b2956a3854d1457d40c93c7f4f134ca808c782d61e0c526e549"
)
# Refreshed after every verifier edit; the final hash is set below after static
# hardening completes.
VERIFIER_SHA256 = (
    "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377"
)


class HarnessFailure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise HarnessFailure(label)


def wire(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def race_checked_single_read(
    path: Path, label: str
) -> tuple[bytes, tuple[int, int, int, int, int, int, int]]:
    """Capture executable bytes once and bind them to one stable inode."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = absolute.lstat()
    identity = (
        before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
        before.st_size, before.st_mtime_ns, before.st_ctime_ns,
    )
    require(
        stat.S_ISREG(before.st_mode)
        and before.st_nlink == 1
        and identity == (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        )
        and identity == (
            current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
            current.st_size, current.st_mtime_ns, current.st_ctime_ns,
        ),
        "race-checked regular singleton:" + label,
    )
    raw = b"".join(chunks)
    require(len(raw) == before.st_size, "race-checked byte count:" + label)
    return raw, identity


def require_capture_current(
    path: Path, identity: tuple[int, int, int, int, int, int, int], label: str
) -> None:
    current = path.lstat()
    require(
        identity == (
            current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
            current.st_size, current.st_mtime_ns, current.st_ctime_ns,
        ),
        "captured path identity changed:" + label,
    )


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = {key: item for key, item in value.items() if key != "row_sha256"}
    return {**body, "row_sha256": digest(body)}


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    return {**body, "result_sha256": digest(body)}


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("ascii"))
    require(type(value) is dict, "object JSON:" + path.name)
    return value


def read_rows(path: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="ascii", newline="") as stream:
        for line in stream:
            value = json.loads(line)
            require(type(value) is dict, "row JSON:" + path.name)
            output.append(value)
    return output


def write_result(target: Path, result: dict[str, Any]) -> None:
    (target / RESULT).write_bytes(wire(close_result(result)))


def write_rows(
    path: Path, rows: list[dict[str, Any]], order: str
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            for row in rows:
                closed = close_row(row)
                row.clear()
                row.update(closed)
                stream.write(wire(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
        "order": order,
    }


def copy_candidate(source: Path, target: Path) -> None:
    require(
        source.is_dir() and not source.is_symlink()
        and {path.name for path in source.iterdir()} == EXPECTED_FILES,
        "baseline candidate exact file set",
    )
    target.mkdir()
    for filename in EXPECTED_FILES:
        shutil.copyfile(source / filename, target / filename)


def copy_c30b_seal_tree(
    verifier: ModuleType, target_root: Path
) -> tuple[Path, Path]:
    """Replay the complete 14-member authority, never a loose lookalike."""
    target_root.mkdir()
    manifest = target_root / verifier.C30B_MANIFEST
    shutil.copyfile(verifier.ROOT / verifier.C30B_MANIFEST, manifest)
    for relative in sorted(verifier.C30B_MANIFEST_MEMBER_PINS):
        source = verifier.ROOT / relative
        destination = target_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    sealed = target_root / verifier.C30B_SEALED_DIRNAME
    require(
        sealed.is_dir()
        and {path.name for path in sealed.iterdir()}
        == set(verifier.C30B_SEALED_FILE_PINS),
        "copied C30b complete seal tree",
    )
    return sealed, manifest


def load_pinned_verifier() -> ModuleType:
    path = ROOT / VERIFIER
    raw, identity = race_checked_single_read(path, VERIFIER)
    require(
        hashlib.sha256(raw).hexdigest() == VERIFIER_SHA256,
        "pinned C30c independent verifier",
    )
    name = VERIFIER[:-3]
    require(name not in sys.modules, "verifier not preloaded")
    module = types.ModuleType(name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = importlib.machinery.ModuleSpec(
        name=name, loader=None, origin=os.fspath(path)
    )
    sys.modules[name] = module
    try:
        exec(compile(raw, os.fspath(path), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    require_capture_current(path, identity, VERIFIER)
    require(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and hashlib.sha256(raw).hexdigest() == VERIFIER_SHA256,
        "imported verifier identity",
    )
    return module


def load_pinned_producer_io() -> ModuleType:
    """Load only the pinned producer's publication helpers from its bytes."""
    path = ROOT / PRODUCER
    raw, identity = race_checked_single_read(path, PRODUCER)
    require(
        hashlib.sha256(raw).hexdigest() == PRODUCER_SHA256,
        "pinned C30c producer I/O source",
    )
    tree = ast.parse(raw, filename=os.fspath(path))
    function_names = {
        "bootstrap_need", "durable_exclusive_write", "fsync_directory",
        "prepare_staging", "atomic_rename_noreplace",
        "validate_staging_bytes",
    }
    selected: list[ast.stmt] = []
    discovered: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BootstrapFailure":
            selected.append(node)
            discovered.add(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and node.name in function_names:
            selected.append(node)
            discovered.add(node.name)
    require(
        discovered == function_names | {"BootstrapFailure"},
        "producer I/O AST exact helper set",
    )
    isolated_tree = ast.Module(body=selected, type_ignores=[])
    ast.fix_missing_locations(isolated_tree)
    name = PREFIX + "_pinned_io_helpers"
    module = types.ModuleType(name)
    module.__file__ = os.fspath(path)
    module.__dict__.update({
        "Any": Any,
        "Path": Path,
        "ROOT": ROOT,
        "EXPECTED_CANDIDATE_FILES": set(EXPECTED_FILES),
        "ctypes": ctypes,
        "errno": errno,
        "hashlib": hashlib,
        "os": os,
        "stat": stat,
        "tempfile": tempfile,
    })
    exec(
        compile(isolated_tree, os.fspath(path), "exec", dont_inherit=True),
        module.__dict__,
    )
    module.need = module.bootstrap_need
    require_capture_current(path, identity, PRODUCER)
    require(
        hashlib.sha256(raw).hexdigest() == PRODUCER_SHA256
        and all(callable(getattr(module, name, None)) for name in function_names)
        and callable(module.need),
        "loaded pinned producer I/O helper identity",
    )
    return module


def baseline_state(candidate: Path) -> dict[str, str]:
    return {
        filename: file_hash(candidate / filename)
        for filename in sorted(EXPECTED_FILES)
    }


def cascade_combined(target: Path, rows: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGINS)
    old_hashes = {row["cell_key"]: row["row_sha256"] for row in rows}
    combined_descriptor = write_rows(
        target / COMBINED, rows,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    replacements = {
        old_hashes[row["cell_key"]]: row["row_sha256"] for row in rows
    }

    def replace_hashes(value: Any) -> Any:
        if type(value) is str:
            return replacements.get(value, value)
        if type(value) is list:
            return [replace_hashes(item) for item in value]
        if type(value) is dict:
            return {key: replace_hashes(item) for key, item in value.items()}
        return value

    joins = [replace_hashes(row) for row in read_rows(target / JOIN)]
    by_origin: dict[str, list[dict[str, Any]]] = {}
    for origin in origins:
        values = [
            row for row in rows if row["origin_key"] == origin["origin_key"]
        ]
        by_origin[origin["origin_key"]] = values
        origin["combined_Delta_H_cell_count"] = len(values)
        origin["combined_Delta_H_cell_keys_sha256"] = digest([
            row["cell_key"] for row in values
        ])
        origin["combined_Delta_H_cell_rows_sha256"] = digest(values)
        origin.update(close_row(origin))
    origin_descriptor = write_rows(
        target / ORIGINS, origins, "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY"
    )
    result["ledgers"]["combined_Delta_H_cell_candidate"] = combined_descriptor
    result["ledgers"]["whole_origin_disposition_candidate"] = origin_descriptor
    write_result(target, result)
    cascade_join(target, joins)


def cascade_h(target: Path, rows: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGINS)
    old_hashes = {row["cell_key"]: row["row_sha256"] for row in rows}
    h_descriptor = write_rows(
        target / INHERITED_H, rows,
        "LEXICOGRAPHIC_ROUND180_INHERITED_H_CELL_KEY",
    )
    replacements = {
        old_hashes[row["cell_key"]]: row["row_sha256"] for row in rows
    }

    def replace_hashes(value: Any) -> Any:
        if type(value) is str:
            return replacements.get(value, value)
        if type(value) is list:
            return [replace_hashes(item) for item in value]
        if type(value) is dict:
            return {key: replace_hashes(item) for key, item in value.items()}
        return value

    joins = [replace_hashes(row) for row in read_rows(target / JOIN)]
    for origin in origins:
        values = [
            row for row in rows if row["origin_key"] == origin["origin_key"]
        ]
        origin["inherited_H_cell_count"] = len(values)
        origin["inherited_H_cell_keys_sha256"] = digest([
            row["cell_key"] for row in values
        ])
        origin["inherited_H_cell_rows_sha256"] = digest(values)
        origin.update(close_row(origin))
    origin_descriptor = write_rows(
        target / ORIGINS, origins, "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY"
    )
    result["ledgers"]["inherited_H_cell_candidate"] = h_descriptor
    result["ledgers"]["whole_origin_disposition_candidate"] = origin_descriptor
    write_result(target, result)
    cascade_join(target, joins)


def normalize_join_row(row: dict[str, Any]) -> dict[str, Any]:
    def normalize_binding(binding: dict[str, Any]) -> dict[str, Any]:
        alignment = binding["whole_origin_atomic_owner_alignment"]
        owner_object = close_row(alignment["full_atomic_owner_row"])
        alignment["full_atomic_owner_row"] = owner_object
        alignment["full_atomic_owner_row_sha256"] = owner_object[
            "row_sha256"
        ]
        binding["whole_origin_atomic_owner_alignment"] = close_row(alignment)
        semantic = binding["selected_owner_semantic_binding"]
        if semantic["kind"] == "ROUND306C30C_MATERIALIZED_INHERITED_H":
            relative = semantic["relative_H_sign_sheet_stratum_binding"]

            def normalize_relative_row(item: dict[str, Any]) -> dict[str, Any]:
                support = [close_row(row) for row in item[
                    "H_sign_sheet_stratum_rows"
                ]]
                item["H_sign_sheet_stratum_rows"] = support
                item["H_sign_sheet_stratum_rows_sha256"] = digest(support)
                item["pointwise_H_predicate_row_count"] = len(support)
                if "parent_piece_incidences" in item:
                    parents = [close_row(row) for row in item[
                        "parent_piece_incidences"
                    ]]
                    item["parent_piece_incidences"] = parents
                    item["parent_piece_incidence_count"] = len(parents)
                    item["parent_piece_incidences_sha256"] = digest(parents)
                return close_row(item)

            pieces: list[dict[str, Any]] = []
            for piece in relative["terminal_piece_rows"]:
                pieces.append(normalize_relative_row(piece))
            relative["terminal_piece_rows"] = pieces
            relative["terminal_piece_row_count"] = len(pieces)
            relative["terminal_piece_rows_sha256"] = digest(pieces)
            recursive = relative["recursive_internal_cut_equality_complex"]
            lines = [normalize_relative_row(item) for item in recursive[
                "atomic_1D_internal_cut_rows"
            ]]
            points = [normalize_relative_row(item) for item in recursive[
                "atomic_0D_internal_cut_rows"
            ]]
            recursive["atomic_1D_internal_cut_rows"] = lines
            recursive["atomic_1D_internal_cut_row_count"] = len(lines)
            recursive["atomic_1D_internal_cut_rows_sha256"] = digest(lines)
            recursive["atomic_0D_internal_cut_rows"] = points
            recursive["atomic_0D_internal_cut_row_count"] = len(points)
            recursive["atomic_0D_internal_cut_rows_sha256"] = digest(points)
            recursive["expected_1D_parent_piece_incidence_count"] = sum(
                item["parent_piece_incidence_count"] for item in lines
            )
            recursive["expected_0D_parent_piece_incidence_count"] = sum(
                item["parent_piece_incidence_count"] for item in points
            )
            exhaustion = recursive["point_set_exhaustion_by_dimension"]
            exhaustion["same_dimension_open_piece_count"] = len(pieces)
            exhaustion["internal_1D_cut_equality_count"] = len(lines)
            exhaustion["internal_0D_cut_equality_count"] = len(points)
            relative["recursive_internal_cut_equality_complex_sha256"] = digest(
                recursive
            )
        incidences = [
            close_row(incidence)
            for incidence in binding["closed_incident_combined_cells"]
        ]
        binding["closed_incident_combined_cells"] = incidences
        binding["closed_incident_combined_cells_sha256"] = digest(incidences)
        return close_row(binding)

    atoms: list[dict[str, Any]] = []
    for atom in row["atomic_bindings"]:
        atoms.append(normalize_binding(atom))
    row["atomic_bindings"] = atoms
    row["atomic_binding_count"] = len(atoms)
    row["atomic_bindings_sha256"] = digest(atoms)
    lower = row["recursive_lower_strata"]
    line_rows: list[dict[str, Any]] = []
    for line in lower["atomic_1D_cut_rows"]:
        line_rows.append(normalize_binding(line))
    point_rows: list[dict[str, Any]] = []
    for point in lower["atomic_0D_cut_rows"]:
        point_rows.append(normalize_binding(point))
    lower["atomic_1D_cut_rows"] = line_rows
    lower["atomic_1D_cut_row_count"] = len(line_rows)
    lower["atomic_1D_cut_rows_sha256"] = digest(line_rows)
    lower["atomic_0D_cut_rows"] = point_rows
    lower["atomic_0D_cut_row_count"] = len(point_rows)
    lower["atomic_0D_cut_rows_sha256"] = digest(point_rows)
    return close_row(row)


def join_summary(
    rows: list[dict[str, Any]], owner_audit: dict[str, Any]
) -> dict[str, Any]:
    identities: dict[str, dict[str, Any]] = {}
    boundary_census: dict[str, int] = {}
    atom_census: dict[str, int] = {}
    lower_census: dict[str, int] = {"0D": 0, "1D": 0}
    identity_fields = (
        "ambient_dimension", "geometry", "closed_containing_leaf_keys",
        "half_open_owner_leaf_key", "owner_proof_source",
        "owner_disposition", "selected_owner_semantic_binding",
        "whole_origin_atomic_owner_alignment",
    )
    def register_identity(atom: dict[str, Any]) -> None:
        atom_dimension = str(atom["ambient_dimension"]) + "D"
        identity = {key: atom[key] for key in identity_fields}
        key = atom_dimension + ":" + wire(atom["geometry"]).decode("ascii")
        identities.setdefault(key, identity)

    for row in rows:
        dimension = str(row["ambient_dimension"]) + "D"
        boundary_census[dimension] = boundary_census.get(dimension, 0) + 1
        for atom in row["atomic_bindings"]:
            atom_dimension = str(atom["ambient_dimension"]) + "D"
            atom_census[atom_dimension] = atom_census.get(atom_dimension, 0) + 1
            register_identity(atom)
        lower = row["recursive_lower_strata"]
        for line in lower["atomic_1D_cut_rows"]:
            register_identity(line)
            lower_census["1D"] += 1
        for point in lower["atomic_0D_cut_rows"]:
            register_identity(point)
            lower_census["0D"] += 1
    return {
        "schema": "cm2.round306c30c.combined-boundary-atomic-owner-join.summary.v1",
        "row_count": len(rows),
        "row_sha256_sequence_sha256": digest([
            row["row_sha256"] for row in rows
        ]),
        "boundary_dimension_census": dict(sorted(boundary_census.items())),
        "materialized_atom_incidence_census": dict(sorted(atom_census.items())),
        "recursive_lower_strata_row_census": dict(sorted(lower_census.items())),
        "unique_atomic_geometry_owner_identity_count": len(identities),
        "unique_atomic_geometry_owner_identities_sha256": digest([
            identities[key] for key in sorted(identities)
        ]),
        "whole_origin_atomic_owner_audit_sha256": digest(owner_audit),
        "owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "every_boundary_measure_exactly_reclosed": True,
        "every_atom_has_pointwise_semantic_owner_binding": True,
        "every_atom_has_object_level_whole_origin_owner_alignment": True,
        "every_2D_atom_cut_line_and_1D_cut_endpoint_materialized": True,
        "sampled_evidence_used_for_uniform_conclusion": False,
    }


def cascade_join(target: Path, rows: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGINS)
    normalized = [normalize_join_row(row) for row in rows]
    descriptor = write_rows(
        target / JOIN, normalized,
        "LEXICOGRAPHIC_COMBINED_CELL_KEY_THEN_BOUNDARY_ORDINAL",
    )
    for origin in origins:
        values = [
            row for row in normalized if row["origin_key"] == origin["origin_key"]
        ]
        origin["combined_boundary_to_atomic_owner_binding"] = join_summary(
            values, origin["disposition_aware_half_open_owner_audit"]
        )
        origin.update(close_row(origin))
    origin_descriptor = write_rows(
        target / ORIGINS, origins, "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY"
    )
    result["ledgers"][
        "combined_boundary_atomic_owner_join_candidate"
    ] = descriptor
    result["ledgers"]["whole_origin_disposition_candidate"] = origin_descriptor
    write_result(target, result)


def cascade_origins(target: Path, origins: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    descriptor = write_rows(
        target / ORIGINS, origins, "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY"
    )
    result["ledgers"]["whole_origin_disposition_candidate"] = descriptor
    write_result(target, result)


def mutate_runtime(target: Path) -> None:
    path = target / RUNTIME
    raw = bytearray(path.read_bytes())
    raw[len(raw) // 2] ^= 1
    path.write_bytes(bytes(raw))


def mutate_delta_collar(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    rows[0]["Delta_on_H_graph_bracket"]["Delta_interval_sign"] = "STRICT_POSITIVE"
    rows[0]["Delta_on_H_graph_bracket"]["conclusion"] = (
        "H_ZERO_SHEET_NOT_CERTIFIED_INSIDE_DELTA_NEGATIVE"
    )
    cascade_combined(target, rows)


def mutate_delta_h_intersection(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    rows[0]["Delta_H_intersection"].update({
        "status": "NONEMPTY_CLAIMED",
        "certificate": "COHERENT_ATTACK_REPLACES_EMPTY_CERTIFICATE",
        "all_outer_face_edge_vertex_restrictions_empty": False,
    })
    rows[0]["partition_theorem"]["Delta_zero_H_zero_intersection_empty"] = False
    cascade_combined(target, rows)


def mutate_live_stratum_owner(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    live = next(
        row for row in rows[0]["combined_strata"]
        if row["disposition"] == "LIVE_W_STAGE_ONE_OWNER_CHART_MATCH"
    )
    live["disposition"] = "EXCLUDED_OUTGOING_CHART_MISMATCH"
    live["owner"] = "N"
    live.update(close_row(live))
    rows[0]["combined_strata_sha256"] = digest(rows[0]["combined_strata"])
    cascade_combined(target, rows)


def mutate_boundary_exhaustion(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    rows[0]["outer_boundary_restriction_rows"].pop()
    rows[0]["outer_boundary_restriction_rows_sha256"] = digest(
        rows[0]["outer_boundary_restriction_rows"]
    )
    rows[0]["partition_theorem"][
        "all_3D_2D_1D_0D_outer_restrictions_disposed"
    ] = False
    cascade_combined(target, rows)


def mutate_cell_box_and_volume(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    row = rows[0]
    lower, upper = (Q(value) for value in row["closed_box"]["t"])
    midpoint = (lower + upper) / 2
    row["closed_box"]["t"][0] = str(midpoint)
    row["exact_volume"] = str(Q(row["exact_volume"]) / 2)
    cascade_combined(target, rows)


def mutate_sampled_to_uniform(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    rows[0]["sampled_uniform_upgrade"] = {
        "samples": ["LOWER", "MIDPOINT", "UPPER"],
        "claimed_uniform": True,
    }
    rows[0]["Delta_on_H_graph_bracket"][
        "strict_on_entire_closed_t_s_p_bracket"
    ] = False
    cascade_combined(target, rows)


def mutate_combined_truth_table_order(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    strata = rows[0]["combined_strata"]
    strata[2], strata[4] = strata[4], strata[2]
    rows[0]["combined_strata_sha256"] = digest(strata)
    cascade_combined(target, rows)


def mutate_h_bracket_step_order(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    steps = rows[0]["H_graph_bracket"]["step_rows"]
    require(len(steps) > 1, "H bracket attack requires two steps")
    steps[0], steps[1] = steps[1], steps[0]
    rows[0]["H_graph_bracket"]["step_rows_sha256"] = digest(steps)
    cascade_combined(target, rows)


def mutate_h_provenance(target: Path) -> None:
    rows = read_rows(target / INHERITED_H)
    rows[0]["source_binding"]["Round180_terminal_sha256"] = "0" * 64
    cascade_h(target, rows)


def corrupt_sha256(value: str) -> str:
    require(
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value),
        "coherent digest attack requires lowercase SHA256",
    )
    replacement = "1" if value[0] != "1" else "0"
    return replacement + value[1:]


def mutate_h_legacy_audit(
    target: Path, mutation: Callable[[dict[str, Any]], None]
) -> None:
    rows = read_rows(target / INHERITED_H)
    candidate = next((
        row for row in rows
        if type(row.get("H_partition")) is dict
        and type(row["H_partition"].get(
            "terminal_exact_atomic_owner_audit"
        )) is dict
    ), None)
    require(candidate is not None, "candidate H legacy audit exists")
    partition = candidate["H_partition"]
    audit = partition["terminal_exact_atomic_owner_audit"]
    mutation(audit)
    partition["terminal_exact_atomic_owner_audit_sha256"] = digest(audit)
    cascade_h(target, rows)


def mutate_h_legacy_atomic_2d_digest(target: Path) -> None:
    def mutation(audit: dict[str, Any]) -> None:
        audit["atomic_2D_owner_rows_sha256"] = corrupt_sha256(
            audit["atomic_2D_owner_rows_sha256"]
        )

    mutate_h_legacy_audit(target, mutation)


def mutate_h_legacy_raw_2d_digest(target: Path) -> None:
    def mutation(audit: dict[str, Any]) -> None:
        audit["raw_2D_stratum_reclosure_rows_sha256"] = corrupt_sha256(
            audit["raw_2D_stratum_reclosure_rows_sha256"]
        )

    mutate_h_legacy_audit(target, mutation)


def mutate_h_legacy_pair_digest(target: Path) -> None:
    def mutation(audit: dict[str, Any]) -> None:
        enclosure = audit["exact_3D_enclosure"]
        enclosure["tested_leaf_pair_rows_sha256"] = corrupt_sha256(
            enclosure["tested_leaf_pair_rows_sha256"]
        )

    mutate_h_legacy_audit(target, mutation)


def mutate_h_legacy_owner_census(target: Path) -> None:
    def mutation(audit: dict[str, Any]) -> None:
        census = audit["atomic_owner_disposition_census"]
        require(
            type(census) is dict and bool(census),
            "candidate H legacy owner census exists",
        )
        disposition = sorted(census)[0]
        require(
            type(census[disposition]) is int,
            "candidate H legacy owner census integer",
        )
        census[disposition] += 1

    mutate_h_legacy_audit(target, mutation)


def mutate_origin_atomic_reclosure(target: Path) -> None:
    origins = read_rows(target / ORIGINS)
    audit = origins[0]["disposition_aware_half_open_owner_audit"]
    ledger = audit["C30c_full_atomic_owner_ledger"]
    row = ledger["atomic_2D_owner_rows"][0]
    row["exact_measure"] = str(Q(row["exact_measure"]) / 2)
    ledger["atomic_2D_owner_rows"][0] = close_row(row)
    for dimension in (2, 1, 0):
        rows = ledger["atomic_" + str(dimension) + "D_owner_rows"]
        ledger["atomic_" + str(dimension) + "D_owner_row_count"] = len(rows)
        ledger["atomic_" + str(dimension) + "D_owner_rows_sha256"] = digest(rows)
    ledger["all_atomic_owner_rows_sha256"] = digest(sum((
        ledger["atomic_" + str(dimension) + "D_owner_rows"]
        for dimension in (2, 1, 0)
    ), []))
    audit["C30c_full_atomic_owner_ledger_sha256"] = digest(ledger)
    binding = origins[0]["combined_boundary_to_atomic_owner_binding"]
    binding["whole_origin_atomic_owner_audit_sha256"] = digest(audit)
    origins[0].update(close_row(origins[0]))
    cascade_origins(target, origins)


def mutate_join_atom_drop(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next((value for value in rows if value["atomic_bindings"]), None)
    require(row is not None, "join atom-drop attack requires an atomic binding")
    removed = row["atomic_bindings"].pop()
    remaining_measure = sum(
        (Q(value["exact_measure"]) for value in row["atomic_bindings"]), Q(0)
    )
    source_measure = Q(row["source_exact_measure"])
    require(
        Q(removed["exact_measure"]) > 0 and remaining_measure < source_measure,
        "join atom-drop attack creates a positive-measure gap",
    )
    row["atomic_exact_measure"] = str(remaining_measure)
    row["atomic_measure_reclosed"] = remaining_measure == source_measure
    cascade_join(target, rows)


def mutate_join_owner_to_valid_alternate(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for row in rows:
        for atom in row["atomic_bindings"]:
            alternates = [
                key for key in atom["closed_containing_leaf_keys"]
                if key != atom["half_open_owner_leaf_key"]
            ]
            if not alternates:
                continue
            alternate = next((
                incidence
                for incidence in atom["closed_incident_combined_cells"]
                if not incidence["selected_by_half_open_owner"]
                and incidence["combined_cell_key"] in alternates
            ), None)
            for incidence in atom["closed_incident_combined_cells"]:
                incidence["selected_by_half_open_owner"] = (
                    alternate is not None and incidence is alternate
                )
            if alternate is not None:
                atom["half_open_owner_leaf_key"] = alternate["combined_cell_key"]
                atom["owner_proof_source"] = (
                    "ROUND306C30C_COMBINED_DELTA_H_PARTITION"
                )
                atom["owner_disposition"] = "MIXED"
                atom["selected_owner_semantic_binding"] = {
                    "kind": "ROUND306C30C_COMBINED_ANALYTIC_PARTITION",
                    "owner_cell_row_sha256": alternate[
                        "combined_cell_row_sha256"
                    ],
                    "analytic_support": alternate["analytic_support"],
                }
            else:
                atom["half_open_owner_leaf_key"] = alternates[0]
                atom["owner_proof_source"] = (
                    "COHERENT_ATTACK_RETARGETS_VALID_CONTAINING_LEAF"
                )
                atom["selected_owner_semantic_binding"] = {
                    "kind": "PINNED_OR_SEALED_UPSTREAM_LEAF_DISPOSITION",
                    "proof_source": atom["owner_proof_source"],
                    "whole_cell_disposition": atom["owner_disposition"],
                }
            cascade_join(target, rows)
            return
    raise HarnessFailure("no alternate incident combined owner")


def mutate_join_cross_origin_owner(target: Path) -> None:
    rows = read_rows(target / JOIN)
    first = next(row for row in rows if row["origin_key"].startswith("W:N:"))
    second = next(row for row in rows if row["origin_key"].startswith("W:S:"))
    source = second["atomic_bindings"][0]
    atom = first["atomic_bindings"][0]
    for key in (
        "half_open_owner_leaf_key", "owner_proof_source", "owner_disposition",
        "selected_owner_semantic_binding",
    ):
        atom[key] = source[key]
    atom["closed_containing_leaf_keys"] = sorted(set(
        atom["closed_containing_leaf_keys"]
        + [source["half_open_owner_leaf_key"]]
    ))
    cascade_join(target, rows)


def mutate_join_boundary_rebind(target: Path) -> None:
    rows = read_rows(target / JOIN)
    group = [row for row in rows if row["combined_cell_key"] == rows[0]["combined_cell_key"]]
    first, second = next(
        (a, b) for a in group for b in group
        if a is not b and a["ambient_dimension"] == b["ambient_dimension"]
    )
    for key in (
        "boundary_restriction_row_sha256", "fixed_coordinates",
        "absolute_boundary_geometry", "source_boundary_analytic_support",
    ):
        first[key] = second[key]
    cascade_join(target, rows)


def mutate_join_t_junction_codimension(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for row in rows:
        for atom in row["atomic_bindings"]:
            geometric_codimension = 3 - atom["ambient_dimension"]
            for incidence in atom["closed_incident_combined_cells"]:
                if incidence["relative_boundary_codimension"] < geometric_codimension:
                    incidence["relative_boundary_codimension"] = geometric_codimension
                    cascade_join(target, rows)
                    return
    incidence = rows[0]["atomic_bindings"][0][
        "closed_incident_combined_cells"
    ][0]
    incidence["relative_boundary_codimension"] = (
        0 if incidence["relative_boundary_codimension"] else 1
    )
    cascade_join(target, rows)


def mutate_join_composition_order(target: Path) -> None:
    rows = read_rows(target / JOIN)
    rows[0]["composition_order"].reverse()
    cascade_join(target, rows)


def mutate_join_1d_owner_content(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next(value for value in rows if value["ambient_dimension"] == 1)
    row["atomic_bindings"][0]["exact_measure"] = "0"
    cascade_join(target, rows)


def mutate_join_2d_owner_content(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next(value for value in rows if value["ambient_dimension"] == 2)
    row["atomic_bindings"][0]["owner_disposition"] = "UNRESOLVED"
    cascade_join(target, rows)


def mutate_join_0d_owner_content(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next(value for value in rows if value["ambient_dimension"] == 0)
    atom = row["atomic_bindings"][0]
    axis = sorted(atom["geometry"]["fixed"])[0]
    atom["geometry"]["fixed"][axis] = "999"
    cascade_join(target, rows)


def mutate_recursive_cut_line_drop(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next(
        value for value in rows
        if value["recursive_lower_strata"]["atomic_1D_cut_row_count"] > 1
    )
    row["recursive_lower_strata"]["atomic_1D_cut_rows"].pop()
    cascade_join(target, rows)


def mutate_recursive_cut_point_drop(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next(
        value for value in rows
        if value["recursive_lower_strata"]["atomic_0D_cut_row_count"] > 1
    )
    row["recursive_lower_strata"]["atomic_0D_cut_rows"].pop()
    cascade_join(target, rows)


def mutate_recursive_parent_membership(target: Path) -> None:
    rows = read_rows(target / JOIN)
    row = next(
        value for value in rows
        if value["recursive_lower_strata"]["atomic_1D_cut_rows"]
    )
    line = row["recursive_lower_strata"]["atomic_1D_cut_rows"][0]
    membership = line["parent_boundary_sides"][0]
    membership["side"] = (
        "UPPER" if membership["side"] == "LOWER" else "LOWER"
    )
    cascade_join(target, rows)


def mutate_whole_owner_alignment(target: Path) -> None:
    rows = read_rows(target / JOIN)
    alignment = rows[0]["atomic_bindings"][0][
        "whole_origin_atomic_owner_alignment"
    ]
    alignment["owner_proof_source"] = "COHERENT_ATTACK_REBINDS_OWNER_AUDIT"
    cascade_join(target, rows)


def mutate_embedded_full_owner_measure(target: Path) -> None:
    rows = read_rows(target / JOIN)
    atom = rows[0]["atomic_bindings"][0]
    full = atom["whole_origin_atomic_owner_alignment"][
        "full_atomic_owner_row"
    ]
    full["exact_measure"] = str(Q(full["exact_measure"]) / 2)
    cascade_join(target, rows)


def mutate_embedded_full_owner_source(target: Path) -> None:
    rows = read_rows(target / JOIN)
    atom = rows[0]["atomic_bindings"][0]
    full = atom["whole_origin_atomic_owner_alignment"][
        "full_atomic_owner_row"
    ]
    full["incident_sources"][0] = "COHERENT_ATTACK:FALSE_INCIDENT_SOURCE"
    cascade_join(target, rows)


def inherited_relative_bindings(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        candidates = row["atomic_bindings"] + row[
            "recursive_lower_strata"
        ]["atomic_1D_cut_rows"] + row["recursive_lower_strata"][
            "atomic_0D_cut_rows"
        ]
        for candidate in candidates:
            semantic = candidate["selected_owner_semantic_binding"]
            if semantic["kind"] == "ROUND306C30C_MATERIALIZED_INHERITED_H":
                output.append(
                    semantic["relative_H_sign_sheet_stratum_binding"]
                )
    require(bool(output), "no inherited-H relative binding")
    return output


def inherited_relative_binding(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return inherited_relative_bindings(rows)[0]


def inherited_recursive_rows(
    relative: dict[str, Any], dimension: int
) -> list[dict[str, Any]]:
    require(
        relative.get("schema")
        == "cm2.round306c30c.inherited-H-relative-binding.v2",
        "inherited-H relative v2 binding",
    )
    recursive = relative["recursive_internal_cut_equality_complex"]
    return recursive[
        "atomic_" + str(dimension) + "D_internal_cut_rows"
    ]


def mutate_inherited_h_recursive_1d_drop(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for relative in inherited_relative_bindings(rows):
        lines = inherited_recursive_rows(relative, 1)
        if lines:
            lines.pop()
            cascade_join(target, rows)
            return
    raise HarnessFailure("no inherited-H recursive 1D cut row")


def mutate_inherited_h_recursive_0d_drop(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for relative in inherited_relative_bindings(rows):
        points = inherited_recursive_rows(relative, 0)
        if points:
            points.pop()
            cascade_join(target, rows)
            return
    raise HarnessFailure("no inherited-H recursive 0D cut row")


def mutate_inherited_h_recursive_0d_retarget(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for relative in inherited_relative_bindings(rows):
        points = inherited_recursive_rows(relative, 0)
        if not points:
            continue
        point = points[0]
        fixed = point["geometry"]["fixed"]
        require(bool(fixed), "inherited-H recursive 0D fixed geometry")
        axis = sorted(fixed)[0]
        fixed[axis] = str(Q(fixed[axis]) + 1)
        cascade_join(target, rows)
        return
    raise HarnessFailure("no inherited-H recursive 0D cut row to retarget")


def mutate_inherited_h_recursive_parent_incidence(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for relative in inherited_relative_bindings(rows):
        recursive_rows = (
            inherited_recursive_rows(relative, 0)
            + inherited_recursive_rows(relative, 1)
        )
        for cut in recursive_rows:
            incidences = cut["parent_piece_incidences"]
            if not incidences:
                continue
            incidence = incidences[0]
            incidence["boundary_side"] = (
                "UPPER"
                if incidence["boundary_side"] == "LOWER" else "LOWER"
            )
            cascade_join(target, rows)
            return
    raise HarnessFailure("no inherited-H recursive parent incidence")


def mutate_inherited_h_recursive_terminal_owner(target: Path) -> None:
    rows = read_rows(target / JOIN)
    for relative in inherited_relative_bindings(rows):
        recursive_rows = (
            inherited_recursive_rows(relative, 1)
            + inherited_recursive_rows(relative, 0)
        )
        if recursive_rows:
            cut = recursive_rows[0]
            cut["half_open_owner_terminal_id"] += "#COHERENT_REBIND"
            cascade_join(target, rows)
            return
    raise HarnessFailure("no inherited-H recursive cut terminal owner")


def mutate_inherited_h_recursive_equality_support(target: Path) -> None:
    rows = read_rows(target / JOIN)
    predicates = {"H=0", "H=ux*dy-uy*dx=0"}
    relatives = inherited_relative_bindings(rows)
    for relative in relatives:
        recursive_rows = (
            inherited_recursive_rows(relative, 1)
            + inherited_recursive_rows(relative, 0)
        )
        for cut in recursive_rows:
            supports = cut["H_sign_sheet_stratum_rows"]
            for ordinal, support in enumerate(supports):
                if support.get("predicate") in predicates:
                    supports.pop(ordinal)
                    cascade_join(target, rows)
                    return
    for relative in relatives:
        recursive_rows = (
            inherited_recursive_rows(relative, 1)
            + inherited_recursive_rows(relative, 0)
        )
        for cut in recursive_rows:
            if cut.get("contains_internal_terminal_cut_equality") is True:
                cut["contains_internal_terminal_cut_equality"] = False
                cascade_join(target, rows)
                return
    raise HarnessFailure("no inherited-H recursive H=0 pointwise support")


def mutate_inherited_h_relative_measure(target: Path) -> None:
    rows = read_rows(target / JOIN)
    relative = inherited_relative_binding(rows)
    piece = relative["terminal_piece_rows"][0]
    piece["exact_measure"] = str(Q(piece["exact_measure"]) / 2)
    cascade_join(target, rows)


def mutate_inherited_h_terminal_owner(target: Path) -> None:
    rows = read_rows(target / JOIN)
    relative = inherited_relative_binding(rows)
    piece = next((
        item for item in relative["terminal_piece_rows"]
        if len(item["closed_containing_terminal_ids"]) > 1
    ), relative["terminal_piece_rows"][0])
    piece["half_open_owner_terminal_id"] = (
        piece["half_open_owner_terminal_id"] + "#COHERENT_REBIND"
    )
    cascade_join(target, rows)


def mutate_inherited_h_equality_stratum(target: Path) -> None:
    rows = read_rows(target / JOIN)
    relatives = inherited_relative_bindings(rows)
    for relative in relatives:
        for piece in relative["terminal_piece_rows"]:
            for support in piece["H_sign_sheet_stratum_rows"]:
                if support.get("predicate") in {"H=0", "H=ux*dy-uy*dx=0"}:
                    support["disposition"] = "EXCLUDED"
                    cascade_join(target, rows)
                    return
    for relative in relatives:
        for piece in relative["terminal_piece_rows"]:
            if piece.get("H_equality_stratum_explicitly_bound") is True:
                piece["H_equality_stratum_explicitly_bound"] = False
                cascade_join(target, rows)
                return
    raise HarnessFailure("no inherited-H equality stratum")


def mutate_join_row_order(target: Path) -> None:
    rows = read_rows(target / JOIN)
    rows[0], rows[1] = rows[1], rows[0]
    cascade_join(target, rows)


def mutate_origin_disposition(target: Path) -> None:
    origins = read_rows(target / ORIGINS)
    origin = origins[0]
    origin["whole_origin_disposition"] = "EXCLUDED"
    origin["whole_original_physical_origin_excluded"] = True
    origin["candidate_credit_if_independently_verified"] = {
        "resolved_source_W_origin_disposition": 1,
        "resolved_nonexcluded": 0,
        "whole_source_W_origin_exclusion": 1,
    }
    theorem = origin["whole_origin_theorem_candidate"]
    theorem["whole_original_physical_origin_disposition"] = "EXCLUDED"
    theorem["whole_original_physical_origin_excluded"] = True
    origin["whole_origin_theorem_candidate_sha256"] = digest(theorem)
    origin.update(close_row(origin))
    cascade_origins(target, origins)
    result = read_object(target / RESULT)
    result["scope"]["whole_origin_disposition_census"] = {
        "EXCLUDED": 1, "RESOLVED_MIXED": 1,
    }
    result["scope"]["whole_origin_exclusion_count"] = 1
    result["candidate_credit_if_independently_verified"][
        "whole_source_W_origin_exclusions"
    ] = 1
    write_result(target, result)


def mutate_formal_credit(target: Path) -> None:
    result = read_object(target / RESULT)
    result["formal_credit"] = {
        "combined_Delta_H_cell_dispositions": 80,
        "resolved_source_W_origin_dispositions": 2,
        "resolved_nonexcluded": 2,
        "whole_source_W_origin_exclusions": 0,
    }
    result["strict_nonpromotion"]["manifest_present"] = True
    write_result(target, result)


def mutate_transition(target: Path) -> None:
    result = read_object(target / RESULT)
    transition = result[
        "proposed_source_W_ledger_transition_if_independently_verified"
    ]
    transition["after"]["remaining"] = 0
    transition["after"]["resolved_nonexcluded"] = 2086
    transition["after"]["remaining_partition"] = {}
    write_result(target, result)


def mutate_d02_clear(target: Path) -> None:
    result = read_object(target / RESULT)
    result["strict_nonpromotion"]["D02"] = "PASS"
    result["strict_nonpromotion"]["official_source_W_transition"] = "80_TO_78"
    write_result(target, result)


def mutate_cm2_go(target: Path) -> None:
    result = read_object(target / RESULT)
    result["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    result["strict_nonpromotion"]["Gate5_complete_global_blocks"] = 1
    write_result(target, result)


def mutate_input_pin(target: Path) -> None:
    result = read_object(target / RESULT)
    result["input_pins"][0]["sha256"] = "f" * 64
    write_result(target, result)


def mutate_descriptor_order(target: Path) -> None:
    result = read_object(target / RESULT)
    result["ledgers"]["combined_Delta_H_cell_candidate"]["order"] = (
        "OUTCOME_DEPENDENT_ORDER"
    )
    write_result(target, result)


def mutate_row_order(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    rows[0], rows[1] = rows[1], rows[0]
    cascade_combined(target, rows)


def mutate_cross_origin_rebinding(target: Path) -> None:
    rows = read_rows(target / COMBINED)
    north = next(row for row in rows if row["origin_key"].startswith("W:N:"))
    south = next(row for row in rows if row["origin_key"].startswith("W:S:"))
    north["origin_key"], south["origin_key"] = (
        south["origin_key"], north["origin_key"]
    )
    cascade_combined(target, rows)


def mutate_phantom_file(target: Path) -> None:
    (target / "phantom-credit.json").write_bytes(b"{}")


def mutate_symlink_member(target: Path) -> None:
    path = target / RESULT
    path.unlink()
    path.symlink_to(RUNTIME)


def mutate_hardlink_member(target: Path) -> None:
    path = target / RESULT
    shadow = target.parent / (target.name + "-hardlink-shadow")
    os.link(path, shadow)
    require(path.stat().st_nlink == 2, "candidate hardlink attack precondition")


def mutate_partial_publication(target: Path) -> None:
    """Consumer-side partial-directory corruption: one member is absent."""
    (target / JOIN).unlink()


def publisher_payloads(tag: str) -> dict[str, bytes]:
    return {
        filename: ("C30C-PUBLISHER-IO-" + tag + ":" + filename).encode("ascii")
        for filename in sorted(EXPECTED_FILES)
    }


def populate_staging_exact_six(
    producer_io: ModuleType, staging: Path, tag: str
) -> dict[str, bytes]:
    payloads = publisher_payloads(tag)
    for filename, payload in payloads.items():
        producer_io.durable_exclusive_write(staging / filename, payload)
    require(
        {path.name for path in staging.iterdir()} == EXPECTED_FILES,
        "publisher staging synthetic exact six",
    )
    return payloads


def assert_payloads_unchanged(
    directory: Path, payloads: dict[str, bytes], label: str
) -> None:
    require(
        directory.is_dir()
        and not directory.is_symlink()
        and {path.name for path in directory.iterdir()} == set(payloads)
        and all((directory / name).read_bytes() == payload
                for name, payload in payloads.items()),
        label,
    )


def publisher_positive_contract(
    producer_io: ModuleType, temporary: Path
) -> None:
    parent = temporary / "publisher-positive-parent"
    parent.mkdir()
    final = parent / "candidate-final"
    target, staging = producer_io.prepare_staging(final)
    visibility: list[set[str] | None] = [
        None if not target.exists() else {path.name for path in target.iterdir()}
    ]
    require(
        visibility == [None]
        and staging.parent == parent
        and staging.name.startswith("." + final.name + ".c30c-staging-"),
        "publisher final absent before same-parent staging",
    )
    payloads = populate_staging_exact_six(
        producer_io, staging, "POSITIVE"
    )
    hashes = producer_io.validate_staging_bytes(staging)
    require(
        hashes == {
            name: hashlib.sha256(payload).hexdigest()
            for name, payload in payloads.items()
        }
        and not target.exists(),
        "publisher validated staging remains invisible",
    )
    producer_io.atomic_rename_noreplace(staging, target)
    producer_io.fsync_directory(parent)
    visibility.append({path.name for path in target.iterdir()})
    require(
        visibility == [None, EXPECTED_FILES]
        and not staging.exists(),
        "publisher visibility transition absent-to-exact-six",
    )
    assert_payloads_unchanged(
        target, payloads, "publisher exact-six payload visible atomically"
    )


def publisher_preexisting_rejection(
    producer_io: ModuleType, temporary: Path, *, partial: bool
) -> None:
    parent = temporary / (
        "publisher-preexisting-partial" if partial
        else "publisher-preexisting-complete"
    )
    parent.mkdir()
    final = parent / "candidate-final"
    final.mkdir()
    payloads = (
        {RESULT: b"PREEXISTING-PARTIAL-SENTINEL"}
        if partial else publisher_payloads("PREEXISTING-COMPLETE")
    )
    for filename, payload in payloads.items():
        producer_io.durable_exclusive_write(final / filename, payload)
    producer_io.fsync_directory(final)
    producer_io.fsync_directory(parent)
    try:
        producer_io.prepare_staging(final)
    except producer_io.BootstrapFailure as error:
        require(
            str(error) == "candidate target already exists",
            "publisher preexisting exact rejection reason",
        )
        assert_payloads_unchanged(
            final, payloads, "publisher preexisting target not overwritten"
        )
        raise
    raise HarnessFailure("publisher preexisting target accepted")


def publisher_concurrent_rejection(
    producer_io: ModuleType, temporary: Path
) -> None:
    publisher_positive_contract(producer_io, temporary)
    parent = temporary / "publisher-concurrent-parent"
    parent.mkdir()
    final = parent / "candidate-final"
    target, staging = producer_io.prepare_staging(final)
    require(not target.exists(), "publisher concurrent final initially absent")
    populate_staging_exact_six(producer_io, staging, "CONCURRENT-STAGING")
    producer_io.validate_staging_bytes(staging)
    target.mkdir()
    sentinel = {RESULT: b"CONCURRENT-WINNER-SENTINEL"}
    producer_io.durable_exclusive_write(target / RESULT, sentinel[RESULT])
    producer_io.fsync_directory(target)
    producer_io.fsync_directory(parent)
    try:
        producer_io.atomic_rename_noreplace(staging, target)
    except producer_io.BootstrapFailure as error:
        require(
            str(error) == "candidate target appeared before publication",
            "publisher concurrent exact rejection reason",
        )
        assert_payloads_unchanged(
            target, sentinel, "publisher concurrent winner not overwritten"
        )
        require(
            staging.is_dir()
            and {path.name for path in staging.iterdir()} == EXPECTED_FILES,
            "publisher losing staging retained after EEXIST",
        )
        raise
    raise HarnessFailure("publisher concurrent target overwritten")


@dataclass(frozen=True)
class Attack:
    name: str
    layer: str
    expected_reason_prefix: str
    mutate: Callable[[Path], None] | None = None
    mode: str = "candidate"


ATTACKS = (
    Attack("c30b_manifest_bitflip", "upstream-seal", "C30b sealed manifest hash",
           mode="seal-manifest-bitflip"),
    Attack("c30b_lookalike_directory", "upstream-seal",
           "C30b sealed fixed path authority", mode="seal-lookalike"),
    Attack("c30b_sealed_member_hardlink", "upstream-seal",
           "race-checked regular singleton identity:", mode="seal-hardlink"),
    Attack("c30b_manifest_TOCTOU_replace", "upstream-seal",
           "race-checked regular singleton identity:", mode="seal-toctou"),
    Attack("c30b_sealed_data_member_content_bitflip", "upstream-seal",
           "C30b sealed member hash:", mode="seal-member-bitflip"),
    Attack("runtime_attestation_bitflip", "runtime",
           "candidate runtime byte identity", mutate_runtime),
    Attack("combined_cell_box_and_volume", "combined-3D",
           "combined.identity:", mutate_cell_box_and_volume),
    Attack("delta_collar_sign_reversal", "combined-uniform",
           "combined.delta-h.uniform-collar:", mutate_delta_collar),
    Attack("delta_h_intersection_nonempty", "combined-intersection",
           "combined.delta-h.empty-intersection:", mutate_delta_h_intersection),
    Attack("sampled_to_uniform_upgrade", "combined-uniform",
           "combined.schema.keys:", mutate_sampled_to_uniform),
    Attack("live_stratum_owner_flip", "combined-stratum",
           "combined.truth-table.row:", mutate_live_stratum_owner),
    Attack("combined_truth_table_reorder", "combined-stratum-order",
           "combined.truth-table.row:", mutate_combined_truth_table_order),
    Attack("H_bracket_step_reorder", "combined-H-bracket",
           "combined.h.bracket:", mutate_h_bracket_step_order),
    Attack("boundary_26_to_25", "combined-boundary",
           "combined.boundary.26-exact-restrictions:", mutate_boundary_exhaustion),
    Attack("inherited_h_provenance_rebind", "inherited-H",
           "C30c local inherited H exact row:", mutate_h_provenance),
    Attack("inherited_h_legacy_atomic_2D_digest", "inherited-H-legacy-audit",
           "C30c local H legacy audit exact reconstruction:",
           mutate_h_legacy_atomic_2d_digest),
    Attack("inherited_h_legacy_raw_2D_digest", "inherited-H-legacy-audit",
           "C30c local H legacy audit exact reconstruction:",
           mutate_h_legacy_raw_2d_digest),
    Attack("inherited_h_legacy_pair_digest", "inherited-H-legacy-audit",
           "C30c local H legacy audit exact reconstruction:",
           mutate_h_legacy_pair_digest),
    Attack("inherited_h_legacy_owner_census", "inherited-H-legacy-audit",
           "C30c local H legacy audit exact reconstruction:",
           mutate_h_legacy_owner_census),
    Attack("join_atom_drop_gap", "join-measure",
           "object-level analytic/atomic join:", mutate_join_atom_drop),
    Attack("join_valid_alternate_owner", "join-owner",
           "object-level analytic/atomic join:", mutate_join_owner_to_valid_alternate),
    Attack("join_cross_origin_owner", "join-owner",
           "object-level analytic/atomic join:", mutate_join_cross_origin_owner),
    Attack("join_boundary_valid_row_rebind", "join-boundary",
           "object-level analytic/atomic join:", mutate_join_boundary_rebind),
    Attack("join_t_junction_codimension", "join-composition",
           "object-level analytic/atomic join:", mutate_join_t_junction_codimension),
    Attack("join_composition_order", "join-composition",
           "object-level analytic/atomic join:", mutate_join_composition_order),
    Attack("join_2d_owner_content", "join-2D",
           "object-level analytic/atomic join:", mutate_join_2d_owner_content),
    Attack("join_1d_owner_content", "join-1D",
           "object-level analytic/atomic join:", mutate_join_1d_owner_content),
    Attack("join_0d_owner_content", "join-0D",
           "object-level analytic/atomic join:", mutate_join_0d_owner_content),
    Attack("recursive_cut_line_drop", "join-recursive-1D",
           "object-level analytic/atomic join:", mutate_recursive_cut_line_drop),
    Attack("recursive_cut_point_drop", "join-recursive-0D",
           "object-level analytic/atomic join:", mutate_recursive_cut_point_drop),
    Attack("recursive_parent_membership", "join-recursive-incidence",
           "object-level analytic/atomic join:", mutate_recursive_parent_membership),
    Attack("whole_owner_alignment_rebind", "join-whole-owner-alignment",
           "object-level analytic/atomic join:", mutate_whole_owner_alignment),
    Attack("embedded_full_owner_exact_measure", "join-full-owner-measure",
           "object-level analytic/atomic join:", mutate_embedded_full_owner_measure),
    Attack("embedded_full_owner_incident_source", "join-full-owner-source",
           "object-level analytic/atomic join:", mutate_embedded_full_owner_source),
    Attack("inherited_H_relative_exact_measure", "join-H-relative-measure",
           "object-level analytic/atomic join:", mutate_inherited_h_relative_measure),
    Attack("inherited_H_terminal_owner_rebind", "join-H-terminal-owner",
           "object-level analytic/atomic join:", mutate_inherited_h_terminal_owner),
    Attack("inherited_H_equality_stratum_flip", "join-H-equality",
           "object-level analytic/atomic join:", mutate_inherited_h_equality_stratum),
    Attack("inherited_H_recursive_1D_drop", "join-H-recursive-1D",
           "object-level analytic/atomic join:",
           mutate_inherited_h_recursive_1d_drop),
    Attack("inherited_H_recursive_0D_drop", "join-H-recursive-0D",
           "object-level analytic/atomic join:",
           mutate_inherited_h_recursive_0d_drop),
    Attack("inherited_H_recursive_0D_retarget", "join-H-recursive-0D",
           "object-level analytic/atomic join:",
           mutate_inherited_h_recursive_0d_retarget),
    Attack("inherited_H_recursive_parent_incidence",
           "join-H-recursive-incidence",
           "object-level analytic/atomic join:",
           mutate_inherited_h_recursive_parent_incidence),
    Attack("inherited_H_recursive_terminal_owner", "join-H-recursive-owner",
           "object-level analytic/atomic join:",
           mutate_inherited_h_recursive_terminal_owner),
    Attack("inherited_H_recursive_equality_support",
           "join-H-recursive-equality",
           "object-level analytic/atomic join:",
           mutate_inherited_h_recursive_equality_support),
    Attack("join_row_order", "join-order",
           "C30c candidate canonical row order/census", mutate_join_row_order),
    Attack("origin_atomic_reclosure_digest", "origin-owner",
           "exact independent whole-origin row:", mutate_origin_atomic_reclosure),
    Attack("origin_mixed_to_excluded", "origin-disposition",
           "exact independent whole-origin row:", mutate_origin_disposition),
    Attack("formal_credit_pregrant", "formal-credit",
           "exact candidate-only C30c result", mutate_formal_credit),
    Attack("remaining_78_to_0", "ledger-transition",
           "exact candidate-only C30c result", mutate_transition),
    Attack("D02_illegal_clear", "D02", "C30c D02 fail-close", mutate_d02_clear),
    Attack("CM2_illegal_GO", "CM2", "C30c CM2 fail-close", mutate_cm2_go),
    Attack("upstream_input_pin_rewrite", "input-pins",
           "exact candidate-only C30c result", mutate_input_pin),
    Attack("descriptor_order_rewrite", "descriptor",
           "ledger descriptor:", mutate_descriptor_order),
    Attack("combined_row_order_swap", "combined-order",
           "C30c candidate canonical row order/census", mutate_row_order),
    Attack("cross_origin_cell_rebinding", "origin-binding",
           "combined.identity:", mutate_cross_origin_rebinding),
    Attack("phantom_credit_file", "candidate-members",
           "C30c candidate exact race-checked file set", mutate_phantom_file),
    Attack("symlink_result_member", "candidate-members",
           "C30c candidate race-checked regular singleton:",
           mutate_symlink_member),
    Attack("hardlink_result_member", "candidate-members",
           "C30c candidate race-checked regular singleton:",
           mutate_hardlink_member, mode="candidate-hardlink"),
    Attack("atomic_replace_during_candidate_capture", "candidate-TOCTOU",
           "C30c candidate directory changed during capture",
           mode="candidate-toctou"),
    Attack("consumer_partial_directory_missing_JOIN", "consumer-partial-dir",
           "C30c candidate exact race-checked file set", mutate_partial_publication),
    Attack("publisher_atomicity_positive_then_concurrent_EEXIST",
           "publisher-atomic-rename", "candidate target appeared before publication",
           mode="publisher-positive-concurrent"),
    Attack("publisher_preexisting_complete_target_no_overwrite",
           "publisher-noreplace", "candidate target already exists",
           mode="publisher-preexisting"),
    Attack("publisher_preexisting_partial_target_no_overwrite",
           "publisher-noreplace", "candidate target already exists",
           mode="publisher-partial"),
)


def assert_rejected(
    verifier: ModuleType,
    producer_io: ModuleType,
    candidate: Path | None,
    reference: Any,
    attack: Attack,
    temporary: Path,
) -> str:
    try:
        if attack.mode in {"candidate", "candidate-hardlink"}:
            require(candidate is not None, "candidate attack target")
            verifier.verify_candidate_dir(candidate, reference)
        elif attack.mode == "candidate-toctou":
            require(candidate is not None, "candidate TOCTOU attack target")
            member = candidate / RESULT
            replacement = temporary / (attack.name + "-replacement")
            replacement.write_bytes(member.read_bytes())
            original_read = verifier.os.read
            fired = False

            def racing_candidate_read(descriptor: int, size: int) -> bytes:
                nonlocal fired
                block = original_read(descriptor, size)
                if not fired:
                    fired = True
                    os.replace(replacement, member)
                return block

            verifier.os.read = racing_candidate_read
            try:
                verifier.verify_candidate_dir(candidate, reference)
            finally:
                verifier.os.read = original_read
        elif attack.mode == "seal-manifest-bitflip":
            tree = temporary / ("seal-" + attack.name)
            sealed, manifest = copy_c30b_seal_tree(verifier, tree)
            raw = bytearray(manifest.read_bytes())
            raw[len(raw) // 2] ^= 1
            manifest.write_bytes(bytes(raw))
            verifier.validate_c30b_seal_tree(
                tree, sealed, manifest, enforce_fixed_authority=False
            )
        elif attack.mode == "seal-lookalike":
            tree = temporary / ("seal-" + attack.name)
            sealed, manifest = copy_c30b_seal_tree(verifier, tree)
            copied = verifier.validate_c30b_seal_tree(
                tree, sealed, manifest, enforce_fixed_authority=False
            )
            require(
                copied["manifest_member_count"] == 14
                and copied["formal_source_W_remaining"] == 80,
                "lookalike complete tree prevalidation",
            )
            verifier.validate_c30b_seal_path(sealed)
        elif attack.mode == "seal-hardlink":
            tree = temporary / ("seal-" + attack.name)
            sealed, manifest = copy_c30b_seal_tree(verifier, tree)
            member = sealed / verifier.C30B_RESULT
            shadow = tree / "hardlink-shadow"
            member.replace(shadow)
            os.link(shadow, member)
            verifier.validate_c30b_seal_tree(
                tree, sealed, manifest, enforce_fixed_authority=False
            )
        elif attack.mode == "seal-toctou":
            tree = temporary / ("seal-" + attack.name)
            sealed, manifest = copy_c30b_seal_tree(verifier, tree)
            original_read = verifier.os.read
            fired = False

            def racing_read(descriptor: int, size: int) -> bytes:
                nonlocal fired
                block = original_read(descriptor, size)
                if not fired:
                    fired = True
                    replacement = tree / "manifest-replacement"
                    replacement.write_bytes(manifest.read_bytes())
                    os.replace(replacement, manifest)
                return block

            verifier.os.read = racing_read
            try:
                verifier.validate_c30b_seal_tree(
                    tree, sealed, manifest, enforce_fixed_authority=False
                )
            finally:
                verifier.os.read = original_read
        elif attack.mode == "seal-member-bitflip":
            tree = temporary / ("seal-" + attack.name)
            sealed, manifest = copy_c30b_seal_tree(verifier, tree)
            member = sealed / verifier.C30B_RESULT
            raw = bytearray(member.read_bytes())
            raw[len(raw) // 2] ^= 1
            member.write_bytes(bytes(raw))
            verifier.validate_c30b_seal_tree(
                tree, sealed, manifest, enforce_fixed_authority=False
            )
        elif attack.mode == "publisher-positive-concurrent":
            publisher_concurrent_rejection(producer_io, temporary)
        elif attack.mode == "publisher-preexisting":
            publisher_preexisting_rejection(
                producer_io, temporary, partial=False
            )
        elif attack.mode == "publisher-partial":
            publisher_preexisting_rejection(
                producer_io, temporary, partial=True
            )
        else:
            raise HarnessFailure("unknown attack mode:" + attack.mode)
    except (verifier.Reject, verifier.base.Reject) as error:
        reason = str(error)
        require(
            reason.startswith(attack.expected_reason_prefix),
            "wrong rejection layer/reason:" + attack.name + ":" + reason,
        )
        return type(error).__name__ + ":" + reason
    except producer_io.BootstrapFailure as error:
        reason = str(error)
        require(
            attack.mode.startswith("publisher-")
            and reason.startswith(attack.expected_reason_prefix),
            "wrong publisher rejection layer/reason:"
            + attack.name + ":" + reason,
        )
        return type(error).__name__ + ":" + reason
    except BaseException as error:
        raise HarnessFailure(
            "unexpected exception type:" + attack.name + ":"
            + type(error).__name__ + ":" + str(error)
        ) from error
    raise HarnessFailure("attack accepted:" + attack.name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    candidate = Path(os.path.abspath(os.fspath(arguments.candidate)))
    verifier = load_pinned_verifier()
    producer_io = load_pinned_producer_io()
    reference = verifier.reconstruct_reference()
    baseline = verifier.verify_candidate_dir(candidate, reference)
    require(
        baseline["formal_credit"] == 0
        and baseline["manifest_authorized"] is False,
        "candidate-only baseline",
    )
    before = baseline_state(candidate)
    outcomes: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c30c-attacks-") as temporary:
        root = Path(temporary)
        for ordinal, attack in enumerate(ATTACKS):
            if attack.mode not in {
                "candidate", "candidate-hardlink", "candidate-toctou",
            }:
                reason = assert_rejected(
                    verifier, producer_io, None, reference, attack, root
                )
                outcomes.append({
                    "attack": attack.name, "layer": attack.layer,
                    "expected_reason_prefix": attack.expected_reason_prefix,
                    "rejection": reason,
                })
                continue
            mutated = root / f"{ordinal:02d}-{attack.name}"
            copy_candidate(candidate, mutated)
            if attack.mode != "candidate-toctou":
                require(attack.mutate is not None, "candidate mutator")
                attack.mutate(mutated)
            if attack.mode == "candidate":
                require(
                    {path.name for path in mutated.iterdir()} != EXPECTED_FILES
                    or baseline_state(mutated) != before,
                    "attack changes candidate:" + attack.name,
                )
            reason = assert_rejected(
                verifier, producer_io, mutated, reference, attack, root
            )
            outcomes.append({
                "attack": attack.name, "layer": attack.layer,
                "expected_reason_prefix": attack.expected_reason_prefix,
                "rejection": reason,
            })
            shutil.rmtree(mutated)
    require(baseline_state(candidate) == before, "baseline immutable")
    output = {
        "schema": "cm2.round306c30c.source-w-full-delta.coherent-attack-harness.candidate.v1",
        "status": (
            "PASS_" + str(len(outcomes)) + "_OF_" + str(len(ATTACKS))
            + "_LAYER_SPECIFIC_COHERENT_ATTACKS_REJECTED__ZERO_FORMAL_CREDIT"
        ),
        "baseline_result_sha256": baseline["candidate_result_sha256"],
        "baseline_file_sha256": before,
        "C30b_input_kind": "FIXED_FORMALLY_SEALED_MANIFEST_AUTHORITY",
        "C30c_publisher_I_O_authority": {
            "producer_filename": PRODUCER,
            "producer_sha256": PRODUCER_SHA256,
            "loading": "AST_EXTRACTED_SHORT_I_O_HELPERS_FROM_PINNED_BYTES",
            "synthetic_payload_file_count": len(EXPECTED_FILES),
            "positive_visibility_transition": "ABSENT_TO_EXACT_SIX",
            "noreplace_cases": [
                "PREEXISTING_COMPLETE", "PREEXISTING_PARTIAL",
                "CONCURRENT_EEXIST",
            ],
        },
        "attack_count": len(outcomes),
        "attacks": outcomes,
        "formal_credit": 0,
        "manifest_authorized": False,
    }
    print(wire(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
