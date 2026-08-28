#!/usr/bin/env python3
"""K2R230 hardening freeze for the Round230 local bulk continuation package.

This producer is intentionally a receipt builder, not a theorem producer.  It
opens the legacy manifest first and every allow-listed construction input by a
held file descriptor, performs two complete initial SHA-256 passes and a final
post-parse pass, and emits exact path/order/per-row canonical commitments for
the eight selected Round230 ledgers.  No upstream Python is imported or
executed here.  The independent K2R230 verifier separately replays the pinned
legacy semantic verifier and is the only place where the narrow local theorem
authority can be re-established.

The output has zero member-full-support, representation-pullback, membership,
maximality, fibre, B1A, B2, Gate5, D02, or CM2 credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Final, Iterable


sys.dont_write_bytecode = True


class HardeningBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise HardeningBlocked(label)


PREFIX: Final = (
    "cm2_round306b1af4k2r230_source_g_resolved_retained_bulk_authority_hardening"
)
SCHEMA: Final = (
    "cm2.round306b1af4k2r230.source-g-resolved-retained-bulk-authority-hardening.v1"
)
HERE: Final = Path(os.path.abspath(__file__)).parent
ROW_CAP: Final = 8_388_608
OLD_SCHEMA: Final = "cm2.round230.source-g-resolved-retained-bulk-continuation.v1"
OLD_RESULT_SHA256: Final = (
    "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e"
)


# Manifest-first order is contractual.  label, filename, exact size, SHA-256,
# role.  The last twelve files are the complete local semantic replay input
# surface used by the pinned independent Round230 verifier.
PINS: Final = (
    ("R230_MANIFEST", "cm2_round230_source_g_resolved_retained_bulk_continuation_manifest.sha256", 546, "54a6a7f91aa9f7bd2caebd5778e8522fa072d5621da2b4015f425fb7f9d67229", "LEGACY_MANIFEST_OPENED_FIRST"),
    ("R230_PRODUCER", "cm2_round230_source_g_resolved_retained_bulk_continuation.py", 63_598, "6b9bac3fd7da301bffb73b0545cc16505df84f69c4f496075cbb146157377cbb", "LEGACY_PRODUCER"),
    ("R230_CERT", "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json", 67_327_799, "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73", "LEGACY_ROW_CERTIFICATE"),
    ("R230_VERIFIER", "cm2_round230_source_g_resolved_retained_bulk_continuation_verifier.py", 54_481, "e2fdd802ab5d2ccb0d99483da4aed5cff96004c4c6c04518ac9a80cbafe79d72", "LEGACY_INDEPENDENT_SEMANTIC_VERIFIER"),
    ("R230_VERIFICATION", "cm2_round230_source_g_resolved_retained_bulk_continuation_verification.json", 763, "a48df50b6ffd38f096dbbeece6e6f1707a69ce08313ae302c993aac5d34fca0c", "LEGACY_VERIFICATION_RECEIPT"),
    ("R179_ROWS", "cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42", "SEMANTIC_INPUT"),
    ("R208_CERT", "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json", 193_161_618, "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938", "SEMANTIC_INPUT"),
    ("R211_CERT", "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json", 140_690_802, "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f", "SEMANTIC_INPUT"),
    ("R220_CERT", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974", "SEMANTIC_INPUT"),
    ("R225_CERT", "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json", 56_136_957, "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841", "SEMANTIC_INPUT"),
    ("R229_CERT", "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json", 70_103_992, "c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a", "SEMANTIC_INPUT"),
    ("R186_KERNEL", "cm2_round186_source_g_factor_face_probe.py", 17_076, "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64", "PINNED_SEMANTIC_KERNEL"),
    ("R182_KERNEL", "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py", 67_870, "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56", "PINNED_KERNEL_DEPENDENCY"),
    ("R179_KERNEL", "cm2_round179_source_g_residual_tube_arrangement_verifier.py", 78_867, "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679", "PINNED_KERNEL_DEPENDENCY"),
    ("R174_KERNEL", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py", 96_797, "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058", "PINNED_KERNEL_DEPENDENCY"),
    ("G3_FIRST_HIT", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2", "PINNED_KERNEL_DEPENDENCY"),
    ("G3_ATLAS", "cm2_gate3_eight_cell_symmetry_atlas_cert.py", 18_141, "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da", "PINNED_KERNEL_DEPENDENCY"),
)


# label, exact result-relative path, row ID, count, ordered row digest.
TABLES: Final = (
    ("R230_ABSENCE", ("formal_resolved_child_event_zero_set_absence_ledger", "rows"), "event_zero_set_absence_row_id", 8_976, "9e5451b5f808ff80b1bc25dcad1746a78cb8fa7ae3f77483a0fc3e47f2345626"),
    ("R230_FACE_CANDIDATE", ("formal_exact_face_candidate_ledger", "rows"), "face_candidate_row_id", 1_512, "421dd9039658c7e8bcb17f434b9d80515e65188083a8905f11c249814bbc18ad"),
    ("R230_EDGE", ("formal_certified_local_bulk_continuation_edge_ledger", "rows"), "certified_local_bulk_bridge_edge_id", 784, "7a63ba5416a34ad1fcf5084dc0a5ee4b135816358c7a02b69e258bd9f924f6e3"),
    ("R230_REJECT", ("formal_rejected_local_bulk_candidate_ledger", "rows"), "reject_row_id", 740, "a1ca4f398d1202da6a504ffc977eac25cd68867b280f83eea76651dd257bd773"),
    ("R230_STAR", ("formal_certified_local_bulk_bridge_star_ledger", "rows"), "bridge_star_row_id", 448, "2d3348cac30d52bf97a1fb62c342bbf317bf388d09b256f186485f11c3cf3152"),
    ("R230_INCIDENCE_DELTA", ("formal_occurrence_known_block_incidence_delta_ledger", "rows"), "incidence_delta_row_id", 464, "e0663279b21bdd6e983907ef228bfe5ef88a606cb881de981f1d3b9d732869c0"),
    ("R230_POST_OCCURRENCE", ("formal_post_Round230_occurrence_known_block_frontier_ledger", "rows"), "post_frontier_row_id", 53_968, "dcceb9f3ce4f210e3d16ea262b87678d061defd7e333fb4a963483feba0bca95"),
    ("R230_POST_KEY", ("formal_post_Round230_key_frontier_ledger", "rows"), "key_frontier_row_id", 116, "345678761e03efb721acc9d5e7ac3405371c4de383d671a7dfd8c6b3cbaf4be9"),
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(typed_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)


def duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise HardeningBlocked("nonintegral/nonfinite JSON number:" + token)


def validate_tree(value: Any) -> None:
    if value is None or type(value) in {bool, int}:
        return
    if isinstance(value, str):
        need(not any(0xD800 <= ord(c) <= 0xDFFF for c in value), "surrogate")
        return
    if isinstance(value, list):
        for item in value:
            validate_tree(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            need(isinstance(key, str), "JSON key string")
            validate_tree(item)
        return
    raise HardeningBlocked("unsupported JSON type")


def strict_json(raw: bytes, label: str, *, canonical_wire: bool = True) -> dict[str, Any]:
    need(raw.endswith(b"\n"), "final newline:" + label)
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "BOM/NUL:" + label)
    try:
        value = json.loads(raw.decode("utf-8", errors="strict"),
                           object_pairs_hook=duplicate_reject,
                           parse_float=reject_number, parse_constant=reject_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HardeningBlocked("strict JSON:" + label) from exc
    need(isinstance(value, dict), "JSON root object:" + label)
    validate_tree(value)
    if canonical_wire:
        need(raw == canonical_bytes(value) + b"\n", "canonical JSON wire:" + label)
    return value


def file_identity(st: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns)


def dir_identity(st: os.stat_result) -> tuple[int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode)


class HeldPins:
    def __init__(self) -> None:
        self.dir_fd = -1
        self.dir_before: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.initial: dict[str, tuple[str, str]] = {}
        self.final_hashes: dict[str, str] = {}

    def __enter__(self) -> "HeldPins":
        before = os.stat(os.fspath(HERE), follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "deliverables directory")
        self.dir_fd = os.open(os.fspath(HERE), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        held = os.fstat(self.dir_fd)
        need(dir_identity(before) == dir_identity(held), "directory open race")
        self.dir_before = held
        for label, filename, size, expected, _role in PINS:
            self._add(label, filename, size, expected)
        return self

    def _add(self, label: str, filename: str, size: int, expected: str) -> None:
        need(filename == os.path.basename(filename) and filename not in {".", ".."}, "pin basename")
        before = os.stat(filename, dir_fd=self.dir_fd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "regular/nlink/size:" + label)
        fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dir_fd)
        opened = os.fstat(fd)
        need(file_identity(before) == file_identity(opened), "open race:" + label)
        self.fds[label] = fd
        first, second = self._hash(fd), self._hash(fd)
        need(first == expected and second == expected, "two-pass SHA:" + label)
        after = os.stat(filename, dir_fd=self.dir_fd, follow_symlinks=False)
        need(file_identity(opened) == file_identity(after), "post-hash path:" + label)
        self.initial[label] = (first, second)

    @staticmethod
    def _hash(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                break
            state.update(chunk)
        return state.hexdigest()

    def bytes(self, label: str) -> bytes:
        os.lseek(self.fds[label], 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(self.fds[label], 1_048_576)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)

    def final(self) -> None:
        need(self.dir_before is not None, "held set active")
        for label, filename, _size, expected, _role in PINS:
            final = self._hash(self.fds[label])
            need(final == expected, "final SHA:" + label)
            held = os.fstat(self.fds[label])
            path = os.stat(filename, dir_fd=self.dir_fd, follow_symlinks=False)
            need(file_identity(held) == file_identity(path), "final path/FD:" + label)
            need(stat.S_ISREG(held.st_mode) and held.st_nlink == 1, "final regular/nlink:" + label)
            self.final_hashes[label] = final
        need(dir_identity(self.dir_before) == dir_identity(os.fstat(self.dir_fd)) == dir_identity(os.stat(os.fspath(HERE), follow_symlinks=False)), "final directory identity")

    def __exit__(self, *_args: object) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dir_fd >= 0:
            try:
                os.close(self.dir_fd)
            except OSError:
                pass


def get_path(root: Any, path: Iterable[str], label: str) -> Any:
    node = root
    for part in path:
        need(isinstance(node, dict) and part in node, "exact property path:" + label + ":" + part)
        node = node[part]
    return node


def validate_old_manifest(raw: bytes) -> dict[str, Any]:
    expected = [
        {"filename": PINS[index][1], "sha256": PINS[index][3]}
        for index in (1, 2, 3, 4)
    ]
    rows: list[dict[str, str]] = []
    for line in raw.decode("ascii", errors="strict").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, "legacy manifest syntax")
        rows.append({"filename": parts[1], "sha256": parts[0]})
    need(typed_equal(rows, expected), "legacy manifest exact ordered membership")
    return {"entry_count": 4, "ordered_entries": rows,
            "ordered_entries_sha256": sha(rows), "exact_membership": True}


def zero_credit_types(row: dict[str, Any]) -> None:
    for key, value in row.items():
        if key.endswith("_credit") or key.endswith("_credit_count"):
            need(type(value) is int, "credit integer type:" + key)
        if key in {"global_exact_key_fibre_exhausted", "whole_interface_certified"}:
            need(type(value) is bool, "boolean type:" + key)


def commit_table(
    result: dict[str, Any], label: str, path: tuple[str, ...], id_field: str,
    expected_count: int, expected_rows_sha: str, context_sha: str,
) -> dict[str, Any]:
    rows = get_path(result, path, label)
    need(isinstance(rows, list) and len(rows) == expected_count, "row count:" + label)
    need(sha(rows) == expected_rows_sha, "ordered rows digest:" + label)
    source_ledger = get_path(result, path[:-1], label + ":ledger")
    need(isinstance(source_ledger, dict) and source_ledger.get("row_count") == expected_count, "declared count:" + label)
    need(source_ledger.get("rows_sha256") == expected_rows_sha, "declared rows digest:" + label)
    commitments: list[dict[str, Any]] = []
    seen: set[str] = set()
    canonical_total = 0
    for ordinal, row in enumerate(rows):
        need(isinstance(row, dict) and type(row.get(id_field)) is str, "row/id shape:" + label)
        row_id = row[id_field]
        need(row_id not in seen, "unique row ID:" + label)
        seen.add(row_id)
        row_bytes = canonical_bytes(row)
        canonical_total += len(row_bytes)
        need(len(row_bytes) <= ROW_CAP, "8MiB final canonical row cap:" + label)
        declared = row.get("row_sha256")
        need(type(declared) is str and len(declared) == 64, "declared row SHA:" + label)
        body = dict(row)
        del body["row_sha256"]
        need(sha(body) == declared, "own row closure:" + label + ":" + row_id)
        zero_credit_types(row)
        canonical_input = {
            "authority_context_sha256": context_sha,
            "source_file": PINS[2][1],
            "source_file_sha256": PINS[2][3],
            "source_schema": OLD_SCHEMA,
            "source_result_sha256": OLD_RESULT_SHA256,
            "exact_result_property_path": list(path),
            "source_row_ordinal": ordinal,
            "source_row_id_field": id_field,
            "source_row_id": row_id,
            "source_row_canonical_sha256": sha(row),
            "source_row_declared_body_sha256": declared,
        }
        wrapper = {
            "commitment_id": "k2r230:" + label.lower() + ":" + str(ordinal) + ":" + sha([row_id, declared]),
            "canonical_input_commitment": canonical_input,
            "canonical_input_commitment_sha256": sha(canonical_input),
        }
        wrapper["row_sha256"] = sha(wrapper)
        commitments.append(wrapper)
    return {
        "table_label": label,
        "source_file": PINS[2][1],
        "exact_result_property_path": list(path),
        "row_id_field": id_field,
        "row_count": expected_count,
        "ordered_source_rows_sha256": expected_rows_sha,
        "ordered_source_row_ids_sha256": sha([row[id_field] for row in rows]),
        "ordered_source_row_body_sha256s_sha256": sha([row["row_sha256"] for row in rows]),
        "canonical_source_row_bytes_total": canonical_total,
        "max_final_canonical_row_bytes": max(map(lambda r: len(canonical_bytes(r)), rows), default=0),
        "every_source_row_closed_by_own_sha256": True,
        "every_canonical_input_commitment_closed_by_sha256": True,
        "ordered_commitment_rows_sha256": sha(commitments),
        "rows": commitments,
    }


def build(seed: int) -> dict[str, Any]:
    need(type(seed) is int, "seed integer")
    with HeldPins() as held:
        manifest = validate_old_manifest(held.bytes("R230_MANIFEST"))
        raw = held.bytes("R230_CERT")
        old = strict_json(raw, "R230_CERT")
        need(set(old) == {"schema", "result", "result_sha256"}, "legacy envelope")
        need(old["schema"] == OLD_SCHEMA and old["result_sha256"] == OLD_RESULT_SHA256, "legacy schema/result pins")
        result = old["result"]
        need(isinstance(result, dict) and sha(result) == OLD_RESULT_SHA256, "legacy result digest")
        pin_rows = [
            {"label": label, "filename": filename, "exact_size": size,
             "sha256": expected, "role": role,
             "two_pass_held_fd_sha256": list(held.initial[label])}
            for label, filename, size, expected, role in PINS
        ]
        context = {
            "schema": SCHEMA + ".authority-context",
            "manifest_first_pin_label": "R230_MANIFEST",
            "pins": [{k: row[k] for k in ("label", "filename", "exact_size", "sha256", "role")} for row in pin_rows],
            "legacy_manifest": manifest,
            "legacy_certificate_schema": OLD_SCHEMA,
            "legacy_certificate_result_sha256": OLD_RESULT_SHA256,
            "canonical_json": {"allow_nan": False, "ensure_ascii": False, "separators": [",", ":"], "sort_keys": True},
            "final_canonical_row_cap_bytes": ROW_CAP,
            "software_contract": {"python_major_minor": "3.12", "python_flint_version": "0.9.0"},
        }
        context_sha = sha(context)
        tables = [commit_table(result, *spec, context_sha) for spec in TABLES]
        need(sum(table["row_count"] for table in tables) == 67_008, "selected row total")
        need(sum(table["canonical_source_row_bytes_total"] for table in tables) > 0, "canonical row bytes")
        # The seed is deliberately absent from the artifact.  It exists only to
        # make double-seed byte identity executable rather than aspirational.
        ledger = {
            "schema": SCHEMA,
            "status": "PASS_EXACT_R230_ROW_PATH_ORDER_AND_INPUT_COMMITMENT_FREEZE__LOCAL_SEMANTIC_AUTHORITY_REQUIRES_INDEPENDENT_REPLAY__ZERO_GLOBAL_CREDIT",
            "artifact_kind": "HARDENED_INPUT_BOUND_LOCAL_AUTHORITY_RECEIPT",
            "seed_independent_output": True,
            "authority_context": context,
            "authority_context_sha256": context_sha,
            "exact_pins": pin_rows,
            "pin_security": {
                "manifest_opened_first": True,
                "held_directory_descriptor": True,
                "held_file_descriptors": True,
                "two_full_initial_sha256_passes_per_pin": True,
                "final_full_sha256_after_all_parsing": True,
                "path_fd_identity_before_after_and_final": True,
                "regular_file_required": True,
                "nlink_must_equal_one": True,
                "O_NOFOLLOW": True,
                "symlink_hardlink_TOCTOU": "FAIL_CLOSED",
                "temporary_files_or_spill": False,
                "TMPDIR_consulted": False,
                "decoded_documents_loaded_in_memory": True,
                "bounded_memory_claim": False,
                "final_canonical_selected_row_cap_bytes": ROW_CAP,
                "upstream_python_imported_or_executed": False,
            },
            "selected_table_commitments": tables,
            "census": {
                "selected_table_count": 8,
                "selected_row_count": 67_008,
                "interfaces": 8_960,
                "absence_references": 8_976,
                "exact_face_candidates": 1_512,
                "accepted_local_bulk_patches": 784,
                "rejected_candidates": 740,
                "local_bridge_stars": 448,
                "local_known_block_incidence_deltas": 464,
                "post_frontier_occurrences": 53_968,
                "post_frontier_keys": 116,
                "post_incident": 35_896,
                "post_unattached": 18_072,
            },
            "narrow_authority_contract": {
                "exact_row_extraction_path_order_and_input_commitment": "PROVED_BY_THIS_RECEIPT",
                "strict_positive_area_local_bulk_patch_count": 784,
                "local_patch_semantic_status": "CONDITIONAL_UNTIL_PINNED_INDEPENDENT_SEMANTIC_REPLAY_PASSES",
                "known_block_local_incidence_delta_count": 464,
                "incidence_semantic_status": "CONDITIONAL_LOCAL_INCIDENCE_NOT_MEMBERSHIP",
                "post_frontier_and_key_rows": "ZERO_CREDIT_BOOKKEEPING_ONLY",
            },
            "bridge_theorem_missing": {
                "local_patch_to_member_full_support_equivalence": True,
                "all_member_cells_and_event_strata_exhausted": True,
                "representation_pullback_totality": True,
                "representation_pullback_uniqueness": True,
                "half_open_owner_global_compatibility": True,
                "known_block_to_maximal_physical_component": True,
                "all_cross_component_transitions_exhausted": True,
            },
            "strict_nonpromotion": {
                "normalized_member_full_support_credit": 0,
                "representation_cover_credit": 0,
                "known_block_membership_assignment_credit": 0,
                "maximal_physical_component_credit": 0,
                "global_exact_key_fibre_credit": 0,
                "global_exact_key_disposition_credit": 0,
                "B1A_credit": 0,
                "B2_credit": 0,
                "D02": "BLOCKED",
                "Gate5": "10/18",
                "complete_18_field_global_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "legacy_package_defects_closed_or_contained": [
                "legacy per-file open/close was replaced by one held manifest-first pin set with final revalidation",
                "legacy importlib semantic path is allowed only inside the new verifier while all local sources remain held and are finally rehashed",
                "legacy ordinary-equality bool/int aliases are contained by exact certificate pinning and new recursive type-strict contracts",
                "legacy rows lacked explicit transitive canonical input commitments; all 67008 selected rows now have them",
                "legacy package had no final canonical per-row 8MiB cap; the cap is now measured after canonical encoding",
                "legacy nested deliverables/deliverables report/cold copies are excluded from authority",
            ],
        }
        held.final()
        for row in ledger["exact_pins"]:
            row["final_post_parse_held_fd_sha256"] = held.final_hashes[row["label"]]
        # Final pin receipts are deliberately outside authority_context so the
        # transitive row commitments bind only immutable allow-list facts.
        return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    ledger = build(args.seed)
    envelope = {"schema": SCHEMA + ".envelope", "ledger": ledger,
                "ledger_sha256": sha(ledger)}
    sys.stdout.buffer.write(canonical_bytes(envelope) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
