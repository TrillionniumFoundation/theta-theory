#!/usr/bin/env python3
"""Produce a hardened, narrowly scoped authority ledger for frozen Round235.

This producer treats Round235 as a local single-endpoint graph/word/key
partition only.  It binds every old output row to every frozen source row used
by that conclusion.  It deliberately does not turn an outer envelope, an
inner witness, or a graph-word partition into normalized support, physical
incidence/equivalence, representation pullback, B1A, B2, maximality, or CM2.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Final


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


HERE: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306b1af4k2r235_source_g_single_endpoint_graph_word_key_local_authority_"
LEDGER_NAME: Final = PREFIX + "row_commitment_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "result.json"
SCHEMA: Final = "cm2.round306b1af4k2r235.source-g-single-endpoint-graph-word-key-local-authority.result.v1"
ROW_SCHEMA: Final = "cm2.round306b1af4k2r235.source-g-single-endpoint-graph-word-key-local-authority.row.v1"
STATUS: Final = "PASS_R235_SINGLE_ENDPOINT_LOCAL_GRAPH_WORD_KEY_PARTITION_AUTHORITY_ONLY__16_DOUBLE_ENDPOINT_FACTORS_BLOCKED__ZERO_GLOBAL_FORMAL_CREDIT"
ROW_CAP: Final = 8_388_608

# The old manifest is first.  Narrative files are intentionally pinned under
# their actual erroneous nested path, but excluded from authority membership.
PINS: Final = (
    ("R235_MANIFEST", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256", 566, "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0"),
    ("R235_SOURCE", "cm2_round235_source_g_single_endpoint_graph_word_key_partition.py", 13_043, "8e5f807dfc43632d59cc9c994fd58907080a52bedc7789f8bb507b002ce8641a"),
    ("R235_CERT", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    ("R235_VERIFIER", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_verifier.py", 10_882, "4ce8c9d516dd95f27bea0f951ea2644705af9b50b63362004e3d3e5d7221dc4d"),
    ("R235_VERIFICATION", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_verification.json", 643, "8009f857b45aa05848b84258f2081bd6de54ff04643387ea3e8fd9c74bdb0e2a"),
    ("R235_MISPLACED_REPORT", "deliverables/cm2_round235_source_g_single_endpoint_graph_word_key_partition_report.md", 1_860, "5055ea85cce2d09154d5a77f7e8aa4a8157ac5398ab4bf140bdcb4ebcc838296"),
    ("R235_MISPLACED_COLD", "deliverables/cm2_round235_source_g_single_endpoint_graph_word_key_partition_cold_replay.md", 259, "98bac1ab341f64cf5a0501662b78d3860d251732771ee5a083c2cd35081ee599"),
    ("R179_ROWS", "cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    ("R220_CERT", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    ("R234_CERT", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    ("GATE5_REGISTRY", "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json", 10_733, "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"),
    ("FIRST_HIT_ENGINE", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"),
    ("GE_ENGINE", "cm2_gate3_ge_interval_atlas_cert.py", 17_052, "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b"),
    ("ATLAS_ENGINE", "cm2_gate3_eight_cell_symmetry_atlas_cert.py", 18_141, "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da"),
    ("R174_ENGINE", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py", 96_797, "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058"),
    ("R179_ENGINE", "cm2_round179_source_g_residual_tube_arrangement.py", 63_683, "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"),
)

OLD_MANIFEST_MEMBERS: Final = (
    ("cm2_round235_source_g_single_endpoint_graph_word_key_partition.py", PINS[1][3]),
    ("cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", PINS[2][3]),
    ("cm2_round235_source_g_single_endpoint_graph_word_key_partition_verifier.py", PINS[3][3]),
    ("cm2_round235_source_g_single_endpoint_graph_word_key_partition_verification.json", PINS[4][3]),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def type_strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return set(left) == set(right) and all(type_strict_equal(left[k], right[k]) for k in right)
    if type(right) is list:
        return len(left) == len(right) and all(type_strict_equal(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)


def strict_need(left: Any, right: Any, label: str) -> None:
    need(type_strict_equal(left, right), label)


def duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral/nonfinite JSON number:" + token)


def strict_decode(raw: bytes, label: str, maximum: int) -> Any:
    need(0 < len(raw) <= maximum, "raw size:" + label)
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "raw encoding:" + label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=duplicate_reject,
                           parse_float=reject_number, parse_constant=reject_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("JSON decode:" + label) from exc

    def walk(item: Any) -> None:
        if type(item) is dict:
            for key, child in item.items():
                need(type(key) is str, "key type:" + label); walk(key); walk(child)
        elif type(item) is list:
            for child in item: walk(child)
        elif type(item) is str:
            need("\x00" not in item and not any(0xD800 <= ord(c) <= 0xDFFF for c in item), "string:" + label)
        else:
            need(item is None or type(item) in {bool, int}, "scalar:" + label)
    walk(value)
    return value


def row_wire(row: Any, label: str) -> bytes:
    wire = canonical(row)
    need(len(wire) <= ROW_CAP, "final canonical row cap:" + label)
    return wire


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def dir_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode)


class HeldPins:
    def __init__(self) -> None:
        self.rootfd = -1; self.nestedfd = -1
        self.rootstat: os.stat_result | None = None; self.nestedstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}

    @staticmethod
    def hash_fd(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET); state = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk: return state.hexdigest()
            state.update(chunk)

    def parent_name(self, relative: str) -> tuple[int, str]:
        parts = Path(relative).parts
        if len(parts) == 1: return self.rootfd, parts[0]
        need(len(parts) == 2 and parts[0] == "deliverables" and parts[1] == os.path.basename(parts[1]), "safe nested path:" + relative)
        return self.nestedfd, parts[1]

    def __enter__(self) -> "HeldPins":
        before = os.stat(HERE, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not HERE.is_symlink(), "deliverables directory")
        self.rootfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.rootstat = os.fstat(self.rootfd); need(dir_identity(before) == dir_identity(self.rootstat), "root race")
        nested_before = os.stat("deliverables", dir_fd=self.rootfd, follow_symlinks=False)
        need(stat.S_ISDIR(nested_before.st_mode), "nested deliverables directory")
        self.nestedfd = os.open("deliverables", os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.rootfd)
        self.nestedstat = os.fstat(self.nestedfd); need(dir_identity(nested_before) == dir_identity(self.nestedstat), "nested race")
        try:
            for label, relative, size, sha in PINS:
                parent, name = self.parent_name(relative)
                before_file = os.stat(name, dir_fd=parent, follow_symlinks=False)
                need(stat.S_ISREG(before_file.st_mode) and before_file.st_nlink == 1 and before_file.st_size == size, "regular/size/nlink:" + label)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent)
                opened = os.fstat(fd); need(identity(before_file) == identity(opened), "open race:" + label)
                self.fds[label] = fd
                need(self.hash_fd(fd) == sha and self.hash_fd(fd) == sha, "two-pass pin:" + label)
                need(identity(opened) == identity(os.stat(name, dir_fd=parent, follow_symlinks=False)), "post-hash path:" + label)
            return self
        except BaseException:
            self.__exit__(None, None, None); raise

    def bytes(self, label: str) -> bytes:
        fd = self.fds[label]; os.lseek(fd, 0, os.SEEK_SET); chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk: return b"".join(chunks)
            chunks.append(chunk)

    def final_revalidate(self) -> None:
        need(self.rootstat is not None and self.nestedstat is not None, "snapshot active")
        need(dir_identity(self.rootstat) == dir_identity(os.fstat(self.rootfd)) == dir_identity(os.stat(HERE, follow_symlinks=False)), "final root")
        need(dir_identity(self.nestedstat) == dir_identity(os.fstat(self.nestedfd)) == dir_identity(os.stat("deliverables", dir_fd=self.rootfd, follow_symlinks=False)), "final nested")
        for label, relative, size, sha in PINS:
            parent, name = self.parent_name(relative); held = os.fstat(self.fds[label]); path = os.stat(name, dir_fd=parent, follow_symlinks=False)
            need(identity(held) == identity(path) and held.st_size == size and held.st_nlink == 1, "final FD/path:" + label)
            need(self.hash_fd(self.fds[label]) == sha, "final pin:" + label)

    def __exit__(self, *_args: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        for field in ("nestedfd", "rootfd"):
            fd = getattr(self, field)
            if fd >= 0:
                try: os.close(fd)
                except OSError: pass
                setattr(self, field, -1)


def validate_old_manifest(raw: bytes) -> dict[str, Any]:
    try: text = raw.decode("ascii")
    except UnicodeDecodeError as exc: raise Blocked("old manifest encoding") from exc
    need(text.endswith("\n"), "old manifest newline")
    entries: list[tuple[str, str]] = []
    for line in text.splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64 and all(c in "0123456789abcdef" for c in parts[0]), "old manifest syntax")
        need(parts[1] == os.path.basename(parts[1]), "old manifest basename")
        entries.append((parts[1], parts[0]))
    strict_need(tuple(entries), OLD_MANIFEST_MEMBERS, "old manifest exact membership")
    return {"entry_count": 4, "ordered_entries_sha256": object_sha([list(x) for x in entries]),
            "misplaced_report_in_manifest": False, "misplaced_cold_replay_in_manifest": False,
            "misplaced_narratives_pinned_for_audit_only": True}


def load_envelope(raw: bytes, schema: str, label: str, maximum: int) -> dict[str, Any]:
    document = strict_decode(raw, label, maximum)
    need(type(document) is dict and set(document) == {"schema", "result", "result_sha256"}, "envelope:" + label)
    strict_need(document["schema"], schema, "schema:" + label)
    strict_need(document["result_sha256"], object_sha(document["result"]), "result digest:" + label)
    need(canonical(document) + b"\n" == raw, "canonical wire:" + label)
    return document


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [dict(zip(columns, packed, strict=True)) for packed in document[table]]


def index_rows(rows: list[dict[str, Any]], id_field: str, label: str) -> dict[str, tuple[int, dict[str, Any]]]:
    out: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(rows):
        need(type(row) is dict and type(row.get(id_field)) is str, "row shape:" + label)
        need(row[id_field] not in out, "duplicate row id:" + label); row_wire(row, label)
        out[row[id_field]] = (ordinal, row)
    return out


def row_ref(ordinal: int, row: dict[str, Any], id_field: str, label: str) -> list[Any]:
    return [ordinal, row[id_field], hashlib.sha256(row_wire(row, label)).hexdigest()]


def table_summary(total: int, selected: list[tuple[int, dict[str, Any]]], id_field: str, label: str) -> dict[str, Any]:
    selected = sorted(selected)
    refs = [row_ref(i, row, id_field, label) for i, row in selected]
    return {"source_row_count": total, "selected_row_count": len(selected), "id_field": id_field,
            "ordered_selected_row_refs_sha256": object_sha(refs),
            "ordered_selected_rows_sha256": object_sha([row for _, row in selected]),
            "source_ordinal_sequence_sha256": object_sha([i for i, _ in selected])}


def gzip_bytes(lines: list[bytes]) -> bytes:
    raw = b"".join(line + b"\n" for line in lines)
    return gzip.compress(raw, compresslevel=9, mtime=0)


def write_once(directory: Path, name: str, data: bytes) -> None:
    resolved = directory.resolve(strict=True)
    info = os.stat(resolved, follow_symlinks=False)
    need(stat.S_ISDIR(info.st_mode) and not directory.is_symlink(), "output directory")
    path = resolved / name
    if path.exists():
        st = path.lstat(); need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and path.read_bytes() == data, "existing output mismatch:" + name); return
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
    finally:
        os.close(fd)
    st = path.lstat(); need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(data).digest(), "published output:" + name)


def build(snapshot: HeldPins) -> tuple[dict[str, Any], bytes]:
    old_manifest = validate_old_manifest(snapshot.bytes("R235_MANIFEST"))
    old = load_envelope(snapshot.bytes("R235_CERT"), "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1", "R235 certificate", 70_000_000)
    old_verification = load_envelope(snapshot.bytes("R235_VERIFICATION"), "cm2.round235.source-g-single-endpoint-graph-word-key-partition.verification.v1", "R235 verification", 10_000)
    candidate = old["result"]
    single_rows = candidate["single_endpoint_graph_partition_rows"]; double_rows = candidate["double_endpoint_deferred_rows"]
    strict_need((len(single_rows), len(double_rows)), (38_328, 16), "old output census")
    strict_need(candidate["single_endpoint_graph_partition_rows_sha256"], object_sha(single_rows), "single table digest")
    strict_need(candidate["double_endpoint_deferred_rows_sha256"], object_sha(double_rows), "double table digest")
    strict_need(old_verification["result"]["candidate_sha256"], PINS[2][3], "old verification candidate pin")
    strict_need(old_verification["result"]["candidate_result_sha256"], old["result_sha256"], "old verification result pin")

    r234_doc = load_envelope(snapshot.bytes("R234_CERT"), "cm2.round234.source-g-wall-endpoint-order-depth6-materialization.v1", "R234 certificate", 55_000_000)
    r234 = r234_doc["result"]
    endpoint_selected = [(i, row) for i, row in enumerate(r234["depth6_frontier_rows"]) if row["reason_labels"][0].startswith("wall_endpoint_or_count_transition:")]
    strict_need(len(endpoint_selected), 38_344, "endpoint frontier census")
    endpoint_index = {row["frontier_row_id"]: (i, row) for i, row in endpoint_selected}; need(len(endpoint_index) == 38_344, "endpoint IDs unique")
    interface_ids = {row["Round220_split_interface_id"] for _, row in endpoint_selected}; strict_need(len(interface_ids), 2_232, "endpoint interface census")
    released_selected = [(i, row) for i, row in enumerate(r234["resolved_descendant_rows"]) if row["Round220_split_interface_id"] in interface_ids]
    strict_need(len(released_selected), 10_832, "released descendant census")
    released_by_interface: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for item in released_selected: released_by_interface[item[1]["Round220_split_interface_id"]].append(item)

    r220_doc = load_envelope(snapshot.bytes("R220_CERT"), "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1", "R220 certificate", 310_000_000)
    t220 = r220_doc["result"]["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    strict_need(t220["row_count"], 13_076, "R220 total census")
    interfaces = [dict(zip(t220["columns"], packed, strict=True)) for packed in t220["rows"]]
    interface_all_index = index_rows(interfaces, "split_interface_id", "R220 interface")
    selected_interfaces = [interface_all_index[i] for i in interface_ids]; strict_need(len(selected_interfaces), 2_232, "selected interfaces")

    r179_doc = load_envelope(snapshot.bytes("R179_ROWS"), "cm2.round179.source-g-residual-tube-arrangement-rows.v1", "R179 rows", 140_000_000)
    resolved = unpack(r179_doc["result"], "resolved_3d_child_rows"); strict_need(len(resolved), 17_192, "R179 resolved census")
    resolved_index = index_rows(resolved, "row_id", "R179 resolved")
    sibling_ids = set()
    for _, interface in selected_interfaces:
        sibling_ids.add(interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"])
    selected_siblings = [resolved_index[i] for i in sibling_ids]; strict_need(len(selected_siblings), 2_232, "selected sibling census")

    old_single_index = index_rows(single_rows, "Round234_frontier_row_id", "R235 single")
    old_double_index = index_rows(double_rows, "Round234_frontier_row_id", "R235 double")
    strict_need(set(old_single_index) | set(old_double_index), set(endpoint_index), "output exact endpoint universe")
    need(not (set(old_single_index) & set(old_double_index)), "single/double disjoint")
    engine_commitment = [[label, sha] for label, _name, _size, sha in PINS if label in {"GATE5_REGISTRY", "FIRST_HIT_ENGINE", "GE_ENGINE", "ATLAS_ENGINE", "R174_ENGINE", "R179_ENGINE"}]
    engine_sha = object_sha(engine_commitment)
    endpoint_universe_sha = object_sha([row_ref(i, row, "frontier_row_id", "R234 endpoint") for i, row in endpoint_selected])

    authority_rows: list[dict[str, Any]] = []
    active_hist: Counter[str] = Counter(); token_hist: Counter[str] = Counter(); double_reason_hist: Counter[str] = Counter()
    for endpoint_ordinal, endpoint in endpoint_selected:
        frontier_id = endpoint["frontier_row_id"]; interface_ordinal, interface = interface_all_index[endpoint["Round220_split_interface_id"]]
        sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]
        sibling_ordinal, sibling = resolved_index[sibling_id]
        released = released_by_interface[interface["split_interface_id"]]
        input_commitment = {
            "engine_and_registry_chain_sha256": engine_sha,
            "endpoint_universe_sha256": endpoint_universe_sha,
            "R234_endpoint_frontier": row_ref(endpoint_ordinal, endpoint, "frontier_row_id", "R234 endpoint"),
            "R220_split_interface": row_ref(interface_ordinal, interface, "split_interface_id", "R220 interface"),
            "R179_resolved_sibling": row_ref(sibling_ordinal, sibling, "row_id", "R179 resolved"),
            "R234_released_descendants": [row_ref(i, row, "materialized_row_id", "R234 released") for i, row in released],
        }
        if frontier_id in old_single_index:
            output_ordinal, output = old_single_index[frontier_id]; kind = "SINGLE_ENDPOINT_LOCAL_GRAPH_WORD_KEY_PARTITION_AUTHORITY"
            local_credit = 1; active_hist[output["active_endpoint_factor"]] += 1; token_hist[output["transition_event"][0]] += 1
            gap = None
        else:
            output_ordinal, output = old_double_index[frontier_id]; kind = "DOUBLE_ENDPOINT_TWO_FACTOR_ARRANGEMENT_DEFERRED_NO_AUTHORITY"
            local_credit = 0; double_reason_hist[output["reason_label"]] += 1
            gap = {"active_factors": output["active_factors"], "required_next": "two-factor endpoint arrangement", "double_endpoint_factor_count": 2}
        output_sha = hashlib.sha256(row_wire(output, "R235 output")).hexdigest()
        core = {"schema": ROW_SCHEMA, "kind": kind, "authority_ordinal": len(authority_rows), "old_output_ordinal": output_ordinal,
                "authority_row_id": ("k2r235:" + frontier_id), "Round234_frontier_row_id": frontier_id,
                "canonical_input_commitment": input_commitment, "canonical_input_commitment_sha256": object_sha(input_commitment),
                "old_output_row_sha256": output_sha, "local_single_endpoint_graph_word_key_partition_authority_credit": local_credit,
                "double_endpoint_gap": gap,
                "normalized_full_support_credit": 0, "physical_incidence_equivalence_credit": 0,
                "representation_pullback_credit": 0, "G2_authority_credit": 0, "B1A_credit": 0, "B2_credit": 0,
                "maximality_credit": 0, "CM2_credit": 0}
        core["conclusion_sha256"] = object_sha({"canonical_input_commitment": input_commitment, "old_output_row_sha256": output_sha,
                                                  "kind": kind, "local_credit": local_credit, "double_endpoint_gap": gap})
        row_wire(core, "authority row"); authority_rows.append(core)

    strict_need((len(authority_rows), active_hist, token_hist), (38_344, Counter({"source": 552, "target": 37_776}), Counter({"X+": 9_582, "X-": 9_582, "Y+": 9_582, "Y-": 9_582})), "rebuilt census")
    ledger_wire = gzip_bytes([canonical(row) for row in authority_rows])
    ledger_sha = hashlib.sha256(ledger_wire).hexdigest()
    result = {
        "status": STATUS,
        "old_package_audit": {**old_manifest, "old_row_level_input_commitments_present": False,
                              "old_held_fd_two_pass_and_final_path_revalidation_present": False,
                              "old_strict_duplicate_nonintegral_nonfinite_json_present": False,
                              "old_post_decode_final_canonical_row_cap_present": False,
                              "old_type_strict_bool_int_equality_present": False,
                              "old_structured_attack_suite_present": False},
        "authority_scope": {"positive_authority": "LOCAL_SINGLE_ENDPOINT_GRAPH_WORD_AND_OFFICIAL_EXACT_KEY_PARTITION_ROW_ONLY",
                            "outer_envelope_is_full_support": False, "inner_witness_is_full_support": False,
                            "graph_word_partition_is_normalized_support": False, "graph_word_partition_is_G2_authority": False},
        "census": {"R234_endpoint_frontier_count": 38_344, "single_endpoint_local_authority_count": 38_328,
                   "double_endpoint_factor_deferred_count": 16, "double_endpoint_active_factor_total": 32,
                   "selected_interface_count": 2_232, "selected_resolved_sibling_count": 2_232,
                   "selected_released_descendant_count": 10_832, "active_factor_histogram": dict(sorted(active_hist.items())),
                   "transition_token_histogram": dict(sorted(token_hist.items())),
                   "double_endpoint_reason_histogram": dict(sorted(double_reason_hist.items())),
                   "distinct_candidate_exact_key_count": 92},
        "selected_table_commitments": {
            "R234_ENDPOINT_FRONTIER": table_summary(len(r234["depth6_frontier_rows"]), endpoint_selected, "frontier_row_id", "R234 endpoint"),
            "R234_RELEASED_DESCENDANTS": table_summary(len(r234["resolved_descendant_rows"]), released_selected, "materialized_row_id", "R234 released"),
            "R220_SPLIT_INTERFACES": table_summary(len(interfaces), selected_interfaces, "split_interface_id", "R220 interface"),
            "R179_RESOLVED_SIBLINGS": table_summary(len(resolved), selected_siblings, "row_id", "R179 resolved"),
            "R235_SINGLE_OUTPUTS": table_summary(len(single_rows), [(i, row) for i, row in enumerate(single_rows)], "endpoint_graph_partition_row_id", "R235 single"),
            "R235_DOUBLE_DEFERRED_OUTPUTS": table_summary(len(double_rows), [(i, row) for i, row in enumerate(double_rows)], "deferred_row_id", "R235 double"),
        },
        "engine_and_registry_chain": engine_commitment, "engine_and_registry_chain_sha256": engine_sha,
        "authority_ledger": {"filename": LEDGER_NAME, "compression": "gzip-mtime-zero", "row_schema": ROW_SCHEMA,
                             "row_count": 38_344, "sha256": ledger_sha,
                             "ordered_row_sha256_sequence_sha256": object_sha([hashlib.sha256(canonical(row)).hexdigest() for row in authority_rows]),
                             "ordered_conclusion_sha256_sequence_sha256": object_sha([row["conclusion_sha256"] for row in authority_rows])},
        "strict_nonpromotion": {"normalized_full_support_credit": 0, "physical_incidence_equivalence_credit": 0,
                                "representation_pullback_credit": 0, "G2_authority_credit": 0, "B1A_credit": 0,
                                "B2_credit": 0, "maximality_credit": 0, "fibre_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": {"double_endpoint_two_factor_arrangement_rows": 16,
                          "double_endpoint_active_factor_instances": 32,
                          "physical_support_incidence_equivalence_and_representation_pullback": "BLOCKED",
                          "B1A_and_B2": "NOT_AUTHORIZED"},
    }
    snapshot.final_revalidate()
    return result, ledger_wire


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True,
         "isolated -I -B execution required")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True); mode.add_argument("--produce", action="store_true"); mode.add_argument("--no-write", action="store_true")
    parser.add_argument("--output-directory", type=Path, default=HERE)
    args = parser.parse_args()
    with HeldPins() as snapshot: result, ledger_wire = build(snapshot)
    document = {"schema": SCHEMA, "result": result, "result_sha256": object_sha(result)}
    result_wire = canonical(document) + b"\n"
    if args.produce:
        write_once(args.output_directory, LEDGER_NAME, ledger_wire); write_once(args.output_directory, RESULT_NAME, result_wire)
    print(STATUS); print("result_sha256=" + document["result_sha256"]); print("result_file_sha256=" + hashlib.sha256(result_wire).hexdigest()); print("ledger_sha256=" + hashlib.sha256(ledger_wire).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
