#!/usr/bin/env python3
"""No-import independent audit for the C42 P391 closed-cover candidate.

Formal C42 pins are deliberately left pending until the hardened producer is
frozen.  The auditor treats C41 plus its installed independent audit as the
only authority and never installs an authority pointer.
"""

from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as registry
import cm2_round181_parametric_collision2_graph_arrangement as round181
import cm2_round183_residual_face_bracket_refinement as round183
import cm2_round185_preconditioned_c1_residual_refinement as round185

import cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1 as c41a


sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
PRODUCER = DELIVERABLES / "cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_v1.py"
SCHEMA = "cm2.round306c42.d02-singleton-wall-endpoint-owner-closure.independent-audit.v1"
CANDIDATE_SCHEMA = "cm2.round306c42.d02-singleton-wall-endpoint-owner-closure.v1"

# These five values are patched exactly once, after the formal producer freeze.
EXPECTED_PRODUCER_SOURCE = "4b4e96bcb2c701fd6820a04271e2f02058e3699d980a4bee61d4090b2ce30c78"
EXPECTED_CANDIDATE_OBJECT = "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
EXPECTED_CANDIDATE_STATUS = (
    "FORMAL_PRODUCER_PASS_C42_P391_OWNER_CLOSURE__PENDING_INDEPENDENT_C42_AUDIT"
)
EXPECTED_RECEIPT_OBJECT = "e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08"
EXPECTED_RECEIPT_STATUS = (
    "FORMAL_PRODUCER_PASS_C42_RECEIPT__PENDING_INDEPENDENT_C42_AUDIT__NO_AUTHORITY"
)
EXPECTED_RESULT_FILE_SHA256 = "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0"
EXPECTED_MANIFEST_FILE_SHA256 = "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058"
EXPECTED_RECEIPT_FILE_SHA256 = "5a14c48b028dd20951d02659f9d9655f5718a13e69d2811ee823d78c38530a55"

EXPECTED_C41_SOURCE = "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
EXPECTED_C41_AUDITOR_SOURCE = "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c"
EXPECTED_C41_OBJECT = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
EXPECTED_C41_RECEIPT_OBJECT = "39f1c6dadcf21a428174520b5a1aa4d072a57c73ffd9c9b04d2c3d639d94fed9"
EXPECTED_C41_MANIFEST = "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
EXPECTED_C41_AUDIT_OBJECT = "44061ec6e26108692fe6e635e9e666cca0b11c66f00384eab539be08f66fe877"
EXPECTED_C41_AUDIT_FILE = "6a800959a90c227d587b82c6246f60123483471f61dcf6a5de4da5381fee4b1e"
EXPECTED_C41_TOKEN_FILE = "9e4f2d9c02c1f3e56639d69c971ccc7846ba229f87723e878f101730df3dd1a9"
EXPECTED_C41_AUDIT_TOKEN_FILE = "f8a9a0bf69169eba05ef3bec1db7e924de4b06b4ab61c97693b2919effd9c86c"
EXPECTED_ROUND185_SOURCE = "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2"
EXPECTED_OFFICIAL_REGISTRY = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
EXPECTED_C41_STATUS = (
    "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__91879_AMBIENT_LEAVES__"
    "572_WHOLE_CELLS_TERMINAL__1152_FORMAL_UNRESOLVED"
)
EXPECTED_C41_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C41_DEPTH3_CLOSURE_AUDIT__37_OF_37_MUTATIONS_REJECTED"
)
EXPECTED_C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
EXPECTED_C41_AUDIT_TOKEN = "c41-independent-audit-20260811T031547Z-ab94d420c43c94cd"
EXPECTED_C41_CANDIDATE = ROOT / ".cm2-runtime/candidates" / EXPECTED_C41_TOKEN
EXPECTED_C41_RECEIPT = ROOT / ".cm2-runtime/audit" / EXPECTED_C41_TOKEN / "execution_receipt.json"
EXPECTED_C41_AUDIT = ROOT / ".cm2-runtime/audit" / EXPECTED_C41_AUDIT_TOKEN / "independent_audit.json"
EXPECTED_LOCK = "C42_SINGLETON_CLOSURE.lock"
EXPECTED_LOCK_SHA256 = "32c2e9234e33b9d794a544c7e9d9273e55b5fce06a706778a479327aa6426109"
EXPECTED_LOCK_BYTES = (
    b"C42 is a non-authority formal producer pass pending an independent C42 audit. "
    b"The independently audited C41 object is pinned as input. This producer materializes "
    b"the exact P391 closed-box proof, four faces, four corners, reflection pair and "
    b"862-parent conservation ledger, but it cannot mint C42 authority or install an "
    b"authority pointer. D02 remains blocked by 1150 complete R1648 continuations; D03, "
    b"D04, Gate5 promotion and any CM2 claim remain unauthorized.\n"
)

PAIR_INDEX = 391
TARGET_PATH = "111101111"
TARGET_AMBIENT_ID = "c41-ambient:01bcc14671eacb7628822945582e307e70cf9fbeeff7f3f47adc6e9597f3ab38"
TARGET_AMBIENT_ROW_SHA = "49b986a5ba33c0fba075e854feb5316348815199e56e2b93e1ab224898c6c0e8"
REP_PARENT = "W:E:01.12.000110"
REF_PARENT = "W:E:06.03.111001"
MID_P = Q(1119, 2048)
PRECISION_BITS = 384
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{15,127}\Z")

LEDGERS = {
    "exact_source": ("exact_source.jsonl.gz", "exact_source_id", "c42-source:"),
    "interior": ("interior_certificates.jsonl.gz", "interior_certificate_id", "c42-interior:"),
    "faces": ("face_owner_incidence.jsonl.gz", "face_owner_incidence_id", "c42-face:"),
    "corners": ("corner_owner_incidence.jsonl.gz", "corner_owner_incidence_id", "c42-corner:"),
    "reflection": ("reflection_transport.jsonl.gz", "reflection_transport_id", "c42-reflection:"),
    "parents": ("parent_conservation.jsonl.gz", None, None),
}
DESCRIPTOR_KEYS = {
    "exact_source": "exact_source",
    "interior": "interior_certificates",
    "faces": "face_owner_incidence",
    "corners": "corner_owner_incidence",
    "reflection": "reflection_transport",
    "parents": "parent_conservation",
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def stable_read(path: Path, maximum: int, label: str) -> bytes:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and not path.is_symlink() and
         before.st_nlink == 1 and 0 < before.st_size <= maximum,
         "regular/single-link/bounded:" + label)
    raw = path.read_bytes()
    after = path.lstat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
          before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
          after.st_ctime_ns) and len(raw) == before.st_size,
         "stable capture:" + label)
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw == raw.strip() + b"\n", "terminal newline:" + label)
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        need(len(items) == len({k for k, _ in items}), "duplicate key:" + label)
        return dict(items)
    value = json.loads(raw, object_pairs_hook=pairs,
                       parse_float=lambda _: (_ for _ in ()).throw(Reject("float:" + label)),
                       parse_constant=lambda _: (_ for _ in ()).throw(Reject("constant:" + label)))
    need(type(value) is dict and canonical(value) + b"\n" == raw, "canonical JSON:" + label)
    return value


def self_closed(value: dict[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    semantic = copy.deepcopy(value)
    semantic.pop(field, None)
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None and
         claimed == digest(semantic), "self hash:" + label)


def row_closed(row: dict[str, Any], field: str | None, prefix: str | None, label: str) -> None:
    claimed = row.get("row_sha256")
    semantic = copy.deepcopy(row)
    semantic.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(semantic), "row hash:" + label)
    if field is not None:
        claimed_id = semantic.pop(field, None)
        need(type(claimed_id) is str and claimed_id == prefix + digest(semantic),
             "domain id:" + label)


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def no_producer_import() -> None:
    producer_name = PRODUCER.stem
    need(producer_name not in sys.modules, "C42 producer present in sys.modules")
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name != producer_name for alias in node.names), "producer import")
        elif isinstance(node, ast.ImportFrom):
            need(node.module != producer_name, "producer from-import")


def capture_c41_authority() -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    """Capture the already installed C41 candidate and audit, without C42 code."""
    token = stable_read(ROOT / ".cm2-runtime/c41-current-token", 256, "C41 token")
    audit_token = stable_read(ROOT / ".cm2-runtime/c41-current-audit-token", 256,
                              "C41 audit token")
    need(token == (EXPECTED_C41_TOKEN + "\n").encode(), "installed C41 token")
    need(audit_token == (EXPECTED_C41_AUDIT_TOKEN + "\n").encode(),
         "installed C41 audit token")
    need(file_sha(Path(c41a.__file__).resolve()) == EXPECTED_C41_AUDITOR_SOURCE,
         "frozen C41 auditor")
    result, rows, manifest, _directory_identity, _file_identities = (
        c41a.capture_c41_candidate(EXPECTED_C41_CANDIDATE)
    )
    need(result.get("object_sha256") == EXPECTED_C41_OBJECT and
         result.get("status") == EXPECTED_C41_STATUS and
         manifest == EXPECTED_C41_MANIFEST, "pinned C41 candidate")
    receipt = strict_json(stable_read(EXPECTED_C41_RECEIPT, 4 << 20, "C41 receipt"),
                          "C41 receipt")
    self_closed(receipt, "receipt_object_sha256", "C41 receipt")
    need(receipt.get("receipt_object_sha256") == EXPECTED_C41_RECEIPT_OBJECT and
         receipt.get("candidate_object_sha256") == EXPECTED_C41_OBJECT,
         "pinned C41 receipt")
    audit_raw = stable_read(EXPECTED_C41_AUDIT, 32 << 20, "C41 independent audit")
    need(hashlib.sha256(audit_raw).hexdigest() == EXPECTED_C41_AUDIT_FILE,
         "C41 audit file pin")
    audit = strict_json(audit_raw, "C41 independent audit")
    self_closed(audit, "object_sha256", "C41 independent audit")
    need(audit.get("object_sha256") == EXPECTED_C41_AUDIT_OBJECT and
         audit.get("status") == EXPECTED_C41_AUDIT_STATUS and
         audit.get("candidate_object_sha256") == EXPECTED_C41_OBJECT and
         audit.get("producer_source_sha256") == EXPECTED_C41_SOURCE,
         "installed independent C41 authority")
    return result, rows


def candidate_paths(candidate: Path, receipt: Path) -> tuple[Path, Path]:
    absolute_candidate = Path(os.path.abspath(os.fspath(candidate)))
    absolute_receipt = Path(os.path.abspath(os.fspath(receipt)))
    need(absolute_candidate == absolute_candidate.resolve(strict=True),
         "canonical real candidate path")
    need(absolute_receipt == absolute_receipt.resolve(strict=True),
         "canonical real receipt path")
    candidates_root = (ROOT / ".cm2-runtime/candidates").resolve(strict=True)
    audit_root = (ROOT / ".cm2-runtime/audit").resolve(strict=True)
    need(absolute_candidate.parent == candidates_root and
         absolute_receipt.name == "execution_receipt.json" and
         absolute_receipt.parent.parent == audit_root and
         absolute_receipt.parent.name == absolute_candidate.name,
         "direct-child candidate/receipt token binding")
    protected = (EXPECTED_C41_CANDIDATE, EXPECTED_C41_RECEIPT.parent,
                 EXPECTED_C41_AUDIT.parent, DELIVERABLES)
    targets = (absolute_candidate, absolute_receipt.parent)
    for target in targets:
        for authority in protected:
            authority = authority.resolve(strict=True)
            need(not within(target, authority) and not within(authority, target),
                 "bidirectional target/authority disjointness")
    return absolute_candidate, absolute_receipt


def gunzip_rows(raw: bytes, descriptor: dict[str, Any], label: str,
                id_field: str | None, prefix: str | None) -> list[dict[str, Any]]:
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
            plain = stream.read(256 << 20)
            need(stream.read(1) == b"", "bounded gzip:" + label)
    except (OSError, EOFError) as exc:
        raise Reject("gzip:" + label) from exc
    need(plain.endswith(b"\n") and b"\r" not in plain, "ledger newlines:" + label)
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(plain.splitlines()):
        row = strict_json(line + b"\n", f"{label}:{ordinal}")
        row_closed(row, id_field, prefix, f"{label}:{ordinal}")
        rows.append(row)
    row_hash_bytes = b"".join((row["row_sha256"] + "\n").encode() for row in rows)
    need(descriptor.get("row_count") == len(rows) and
         descriptor.get("row_hash_line_sequence_sha256") ==
         hashlib.sha256(row_hash_bytes).hexdigest(), "ledger descriptor rows:" + label)
    need(len({row["row_sha256"] for row in rows}) == len(rows),
         "unique ledger rows:" + label)
    return rows


def capture_candidate(candidate: Path) -> dict[str, Any]:
    before = candidate.lstat()
    need(stat.S_ISDIR(before.st_mode) and not candidate.is_symlink(),
         "real C42 candidate directory")
    names = {item.name for item in candidate.iterdir()}
    inventory = {EXPECTED_LOCK, "result.json", "root_manifest.sha256"} | {
        item[0] for item in LEDGERS.values()
    }
    need(names == inventory, "exact C42 inventory")
    payloads = {name: stable_read(candidate / name, 256 << 20, "C42:" + name)
                for name in sorted(names)}
    need(payloads[EXPECTED_LOCK] == EXPECTED_LOCK_BYTES and
         hashlib.sha256(payloads[EXPECTED_LOCK]).hexdigest() == EXPECTED_LOCK_SHA256,
         "exact formal nonauthority lock bytes")
    manifest_raw = payloads["root_manifest.sha256"]
    expected_manifest = b"".join(
        hashlib.sha256(payloads[name]).hexdigest().encode() + b"  " +
        name.encode() + b"\n"
        for name in sorted(inventory - {"root_manifest.sha256"})
    )
    need(manifest_raw == expected_manifest, "C42 root manifest")
    need(hashlib.sha256(manifest_raw).hexdigest() == EXPECTED_MANIFEST_FILE_SHA256 and
         hashlib.sha256(payloads["result.json"]).hexdigest() == EXPECTED_RESULT_FILE_SHA256,
         "pinned C42 result/manifest terminal bytes")
    result = strict_json(payloads["result.json"], "C42 result")
    self_closed(result, "object_sha256", "C42 result")
    need(result.get("schema") == CANDIDATE_SCHEMA and
         result.get("object_sha256") == EXPECTED_CANDIDATE_OBJECT and
         result.get("status") == EXPECTED_CANDIDATE_STATUS,
         "pinned C42 result")
    descriptors = result.get("ledgers")
    need(type(descriptors) is dict and set(descriptors) == set(DESCRIPTOR_KEYS.values()),
         "exact C42 ledger descriptors")
    rows: dict[str, list[dict[str, Any]]] = {}
    for key, (filename, id_field, prefix) in LEDGERS.items():
        descriptor = descriptors[DESCRIPTOR_KEYS[key]]
        need(type(descriptor) is dict and descriptor.get("filename") == filename and
             descriptor.get("sha256") == hashlib.sha256(payloads[filename]).hexdigest() and
             descriptor.get("size") == len(payloads[filename]),
             "C42 ledger byte descriptor:" + key)
        rows[key] = gunzip_rows(payloads[filename], descriptor, key, id_field, prefix)
    need({key: len(value) for key, value in rows.items()} == {
        "exact_source": 1, "interior": 4, "faces": 4, "corners": 4,
        "reflection": 2, "parents": 862,
    }, "fixed C42 ledger censuses")
    after = candidate.lstat()
    need((before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns),
         "stable C42 directory")
    return {"candidate": candidate, "result": result, "rows": rows,
            "payloads": payloads,
            "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest()}


def capture_receipt(path: Path, invocation_id: str,
                    captured: dict[str, Any]) -> dict[str, Any]:
    need(stat.S_IMODE(path.stat().st_mode) == 0o600, "C42 receipt mode 0600")
    raw = stable_read(path, 8 << 20, "C42 receipt")
    need(hashlib.sha256(raw).hexdigest() == EXPECTED_RECEIPT_FILE_SHA256,
         "pinned C42 receipt terminal bytes")
    receipt = strict_json(raw, "C42 receipt")
    self_closed(receipt, "receipt_object_sha256", "C42 receipt")
    need(TOKEN.fullmatch(invocation_id) is not None and
         receipt.get("schema") == CANDIDATE_SCHEMA + ".execution-receipt" and
         receipt.get("status") == EXPECTED_RECEIPT_STATUS and
         receipt.get("receipt_object_sha256") == EXPECTED_RECEIPT_OBJECT and
         receipt.get("InvocationID") == invocation_id and
         receipt.get("candidate_path") == str(captured["candidate"].relative_to(ROOT)) and
         receipt.get("candidate_object_sha256") == EXPECTED_CANDIDATE_OBJECT and
         receipt.get("producer_source_sha256") == EXPECTED_PRODUCER_SOURCE and
         receipt.get("root_manifest_sha256") == captured["manifest_sha256"] and
         receipt.get("mode") == "FORMAL_PRODUCER_PASS_PENDING_INDEPENDENT_C42_AUDIT" and
         receipt.get("candidate_inventory_count") == 9 and
         receipt.get("C41_candidate_object_sha256") == EXPECTED_C41_OBJECT and
         receipt.get("C41_independent_audit_object_sha256") == EXPECTED_C41_AUDIT_OBJECT and
         receipt.get("C41_independent_audit_status") == EXPECTED_C41_AUDIT_STATUS and
         receipt.get("formal_producer_run") is True and
         receipt.get("producer_output_is_authority") is False and
         receipt.get("formal_authority") is False and
         receipt.get("independent_C42_audit_outstanding") is True and
         receipt.get("authority_pointer_installed") is False and
         type(receipt.get("producer_pid")) is int and receipt["producer_pid"] > 1 and
         type(receipt.get("producer_parent_pid")) is int and receipt["producer_parent_pid"] > 0 and
         type(receipt.get("producer_proc_start_ticks")) is int and
         receipt["producer_proc_start_ticks"] > 0 and
         Path(receipt.get("producer_executable", "")).resolve() == Path(sys.executable).resolve(),
         "C42 receipt PID/InvocationID/object/manifest binding")
    return receipt


def as_q(value: str) -> Q:
    return Q(value)


def box_contains(container: dict[str, Any], contained: dict[str, Any]) -> bool:
    return all(as_q(container[axis][0]) <= as_q(contained[axis][0]) and
               as_q(contained[axis][1]) <= as_q(container[axis][1])
               for axis in ("t", "p", "s"))


def incident_record(row: dict[str, Any]) -> dict[str, Any]:
    target = row["c41_ambient_cell_id"] == TARGET_AMBIENT_ID
    family = row["disposition_family"]
    need(target or family == "TERMINAL_EXCLUDED", "incident terminal source")
    return {
        "C41_disposition_family": family,
        "C42_effective_disposition_family": (
            "TERMINAL_EXCLUDED_BY_C42_CLOSED_COVER" if target else family
        ),
        "c41_ambient_cell_id": row["c41_ambient_cell_id"],
        "c41_row_sha256": row["row_sha256"],
        "pair_index": row["pair_index"],
        "path": row["path"],
        "representative_cell_id": row["representative_cell_id"],
        "terminal_after_C42": True,
    }


def owner_key(row: dict[str, Any]) -> tuple[str, int, str]:
    return row["path"], row["pair_index"], row["c41_ambient_cell_id"]


def validate_source(rows: dict[str, list[dict[str, Any]]],
                    c41_rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    source = rows["exact_source"][0]
    ambient = next((row for row in c41_rows["routed_ambient_cells.jsonl.gz"]
                    if row["c41_ambient_cell_id"] == TARGET_AMBIENT_ID), None)
    need(ambient is not None and ambient["row_sha256"] == TARGET_AMBIENT_ROW_SHA and
         ambient["pair_index"] == PAIR_INDEX and ambient["path"] == TARGET_PATH and
         ambient["parent_volume_fraction"] == "1/512" and
         ambient["representative_box" if "representative_box" in ambient else
                 "closed_representative_box"] == {
                     "t": ["-125493/256000", "-31329/64000"],
                     "p": ["559/1024", "35/64"], "s": ["0", "0"]},
         "unique exact C41 P391 source")
    required = {
        "pair_index": PAIR_INDEX,
        "C41_target_ambient_cell_id": TARGET_AMBIENT_ID,
        "C41_target_ambient_row_sha256": TARGET_AMBIENT_ROW_SHA,
        "C41_candidate_object_sha256": EXPECTED_C41_OBJECT,
        "C41_receipt_object_sha256": EXPECTED_C41_RECEIPT_OBJECT,
        "C41_root_manifest_sha256": EXPECTED_C41_MANIFEST,
        "C41_independent_audit_object_sha256": EXPECTED_C41_AUDIT_OBJECT,
        "C41_independent_audit_status": EXPECTED_C41_AUDIT_STATUS,
        "C41_candidate_and_audit_pointers_installed": True,
        "producer_output_is_authority": False,
        "C41_input_mode": "AUDITED_C41_FORMAL_INPUT",
        "source_parent_volume_fraction": "1/512",
        "representative_parent_key": REP_PARENT,
        "reflected_parent_key": REF_PARENT,
        "source_closed_representative_box": ambient["closed_representative_box"],
        "source_closed_reflected_box": ambient["closed_reflected_box"],
    }
    need(all(source.get(key) == value for key, value in required.items()),
         "C42 exact source binding")
    return ambient


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def box_payload(box: Any, reflected: bool = False) -> dict[str, Any]:
    value = {"t": [qstr(box.t0), qstr(box.t1)],
             "p": [qstr(box.p0), qstr(box.p1)],
             "s": [qstr(box.s0), qstr(box.s1)]}
    if reflected:
        value["compact_chart"] = "E"
    return value


def box_from_payload(value: dict[str, Any], path: str, depth: int = 10) -> Any:
    return atlas.AtlasBox(Q(value["t"][0]), Q(value["t"][1]),
                          Q(value["p"][0]), Q(value["p"][1]),
                          Q(value["s"][0]), Q(value["s"][1]), depth, path)


def reflected_box(box: Any, path: str) -> Any:
    return atlas.AtlasBox(-box.t1, -box.t0, -box.p1, -box.p0,
                          box.s0, box.s1, box.depth, path)


def arb_bounds(value: arb) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def strict_strip(start: arb, hit: arb, axis: str) -> dict[str, Any]:
    walls = [wall for wall in range(-6, 7)
             if bool(start > wall) and bool(start < wall + 1) and
             bool(hit > wall) and bool(hit < wall + 1)]
    need(len(walls) == 1, "independent strict integer strip:" + axis)
    events, reason = registry.ordered_axis_events(start, hit, axis)
    need(events == [] and reason is None, "independent empty axis events:" + axis)
    wall = walls[0]
    return {"axis": axis, "open_integer_strip": [wall, wall + 1],
            "start_endpoint": arb_bounds(start), "hit_endpoint": arb_bounds(hit),
            "start_and_hit_strictly_inside_same_open_strip": True,
            "ordered_axis_event_tokens": [], "endpoint_on_integer_wall": False}


def enhanced_census(parent_key: str, box: Any) -> dict[str, int]:
    state = round181.collision1_state_direct(parent_key, box)
    geometry = round183.collision2_geometry(state)
    census = Counter()
    for identifier in round185.CANDIDATES:
        kind, _data, _evidence = round185.enhanced_root_record(
            parent_key, box, geometry, identifier)
        census[kind] += 1
    need(sum(census.values()) == 55 and not any(
        key.startswith("UNRESOLVED") for key in census),
         "complete independently resolved 55-candidate census")
    return dict(sorted(census.items()))


def independent_certificate(orientation: str, parent_key: str, box: Any,
                            ordinal: int, role: str,
                            indexes: tuple[dict[Any, int], dict[Any, int]]) -> tuple[dict[str, Any], dict[str, int]]:
    pair_index, pattern_index = indexes
    status, detail, evidence, baseline = round185.resolve_dynamic_box(
        parent_key, box, pair_index, pattern_index)
    owner_status, owner, owner_evidence = round185.enhanced_select_owner(parent_key, box)
    need(status == baseline == "LOCAL_EXACT_KEY" and evidence == [] and
         owner_status == "STRICT_UNIQUE_OWNER" and owner is not None,
         "independent strict lower kernel:" + orientation + ":" + str(ordinal))
    if orientation == "REPRESENTATIVE":
        expected_owner, live, outgoing = "G[1,0]", "G[0,1]", "N"
        word = ["W:W", "G[0,0]", [], 1]
    else:
        expected_owner, live, outgoing = "G[1,1]", "G[0,0]", "S"
        word = ["W:W", "G[0,1]", [], 1]
    need(owner[0] == detail["absolute_collision2_owner"] == expected_owner and
         detail["collision2_outgoing_chart"] == outgoing and
         detail["official_gate5_key"]["row"] == word and
         detail["ordered_clean_wall_record"] == [] and expected_owner != live,
         "independent owner/chart/word mismatch")
    state = round181.collision1_state_direct(parent_key, box)
    hit_x = state["contact_x"] + owner[1]["near"] * state["outgoing_x"]
    hit_y = state["contact_y"] + owner[1]["near"] * state["outgoing_y"]
    axes = [strict_strip(state["contact_x"] - 1, hit_x - 1, "X"),
            strict_strip(state["contact_y"], hit_y, "Y")]
    crossings, reason = registry.strict_event_order([])
    need(crossings == () and reason is None, "independent empty event order")
    value: dict[str, Any] = {
        "schema": CANDIDATE_SCHEMA + ".closed-interior-certificate",
        "pair_index": PAIR_INDEX,
        "source_c41_ambient_cell_id": TARGET_AMBIENT_ID,
        "source_c41_row_sha256": TARGET_AMBIENT_ROW_SHA,
        "orientation": orientation, "certificate_ordinal": ordinal,
        "parent_key": parent_key,
        "closed_box": box_payload(box, orientation == "REFLECTED"),
        "closed_box_scope": "ENTIRE_CLOSED_DYADIC_HALF_BOX",
        "half_open_shared_mid_face_role": role,
        "Round185_baseline_status": baseline, "Round185_status": status,
        "enhanced_owner_status": owner_status,
        "enhanced_owner_surface_evidence_count": len(owner_evidence),
        "absolute_collision2_owner": owner[0],
        "strict_owner_near_root": arb_bounds(owner[1]["near"]),
        "collision2_outgoing_chart": detail["collision2_outgoing_chart"],
        "official_gate5_key": detail["official_gate5_key"],
        "ordered_clean_wall_record": [],
        "strict_axis_endpoint_certificates": axes,
        "wall_endpoint_or_corner_present_on_closed_box": False,
        "strict_disposition": "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
        "disposition_witness": expected_owner,
        "expected_live_collision2_owner": live,
        "owner_mismatch_is_uniform_on_entire_closed_box": True,
        "local_round144_terminal_credit": 1, "D02_gate_credit": 0,
    }
    value["interior_certificate_id"] = "c42-interior:" + digest(value)
    return value, enhanced_census(parent_key, box)


def lower_indexes() -> tuple[dict[Any, int], dict[Any, int]]:
    need(file_sha(Path(round185.__file__).resolve()) == EXPECTED_ROUND185_SOURCE,
         "frozen Round185 source")
    pair_index, pattern_index, registry_sha = registry.key_index_tables()
    need(registry_sha == EXPECTED_OFFICIAL_REGISTRY and
         len(pair_index) == 448 and len(pattern_index) == 985,
         "complete frozen official registry")
    return pair_index, pattern_index


def validate_interiors(rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    expected = [
        (0, "REPRESENTATIVE", REP_PARENT,
         {"t": ["-125493/256000", "-31329/64000"],
          "p": ["559/1024", "1119/2048"], "s": ["0", "0"]},
         "G[1,0]", "G[0,1]", "N", 290575,
         "5e5950ce63693dc08790f017f8e5cc79eb8aa776ff4c53c10a60b27a161178b2"),
        (1, "REPRESENTATIVE", REP_PARENT,
         {"t": ["-125493/256000", "-31329/64000"],
          "p": ["1119/2048", "35/64"], "s": ["0", "0"]},
         "G[1,0]", "G[0,1]", "N", 290575,
         "5e5950ce63693dc08790f017f8e5cc79eb8aa776ff4c53c10a60b27a161178b2"),
        (2, "REFLECTED", REF_PARENT,
         {"compact_chart": "E", "t": ["31329/64000", "125493/256000"],
          "p": ["-35/64", "-1119/2048"], "s": ["0", "0"]},
         "G[1,1]", "G[0,0]", "S", 291560,
         "6c7c484df06c7e03aef7e83aa2fe403090d4843175262deb78c507154f349115"),
        (3, "REFLECTED", REF_PARENT,
         {"compact_chart": "E", "t": ["31329/64000", "125493/256000"],
          "p": ["-1119/2048", "-559/1024"], "s": ["0", "0"]},
         "G[1,1]", "G[0,0]", "S", 291560,
         "6c7c484df06c7e03aef7e83aa2fe403090d4843175262deb78c507154f349115"),
    ]
    need([row["certificate_ordinal"] for row in rows["interior"]] == list(range(4)),
         "interior order")
    for row, (ordinal, orientation, parent, box, owner, live, chart, gate_ordinal,
              gate_sha) in zip(rows["interior"], expected):
        gate = row.get("official_gate5_key", {})
        need(row.get("certificate_ordinal") == ordinal and
             row.get("orientation") == orientation and row.get("parent_key") == parent and
             row.get("closed_box") == box and row.get("pair_index") == PAIR_INDEX and
             row.get("Round185_status") == "LOCAL_EXACT_KEY" and
             row.get("Round185_baseline_status") == "LOCAL_EXACT_KEY" and
             row.get("absolute_collision2_owner") == owner and
             row.get("expected_live_collision2_owner") == live and
             row.get("collision2_outgoing_chart") == chart and
             row.get("ordered_clean_wall_record") == [] and
             row.get("enhanced_owner_status") == "STRICT_UNIQUE_OWNER" and
             row.get("enhanced_owner_surface_evidence_count") == 0 and
             row.get("owner_mismatch_is_uniform_on_entire_closed_box") is True and
             row.get("wall_endpoint_or_corner_present_on_closed_box") is False and
             gate.get("ordinal_zero_based") == gate_ordinal and
             gate.get("row_sha256") == gate_sha,
             "independent exact interior semantic:" + str(ordinal))
        axes = row.get("strict_axis_endpoint_certificates")
        need(type(axes) is list and [item.get("axis") for item in axes] == ["X", "Y"] and
             all(item.get("endpoint_on_integer_wall") is False and
                 item.get("start_and_hit_strictly_inside_same_open_strip") is True and
                 item.get("open_integer_strip") == [0, 1] and
                 item.get("ordered_axis_event_tokens") == [] and
                 item.get("start_endpoint", {}).get("contains_zero") is False and
                 item.get("hit_endpoint", {}).get("contains_zero") is False
                 for item in axes), "strict endpoint strips:" + str(ordinal))
    indexes = lower_indexes()
    censuses = []
    roles = ("OWNS_SHARED_P_MID_FACE", "EXCLUDES_SHARED_P_MID_FACE",
             "OWNS_SHARED_P_MID_FACE", "EXCLUDES_SHARED_P_MID_FACE")
    for row, role in zip(rows["interior"], roles):
        box = box_from_payload(row["closed_box"],
                               TARGET_PATH + ".independent." + str(row["certificate_ordinal"]))
        independent, census = independent_certificate(
            row["orientation"], row["parent_key"], box,
            row["certificate_ordinal"], role, indexes)
        observed = copy.deepcopy(row)
        observed.pop("row_sha256", None)
        need(observed == independent,
             "full independent lower certificate byte semantics:" +
             str(row["certificate_ordinal"]))
        need(census == {"INTERSECTION_BEHIND": 1, "NO_REAL_INTERSECTION": 50,
                        "STRICT_FUTURE": 4},
             "exact enhanced 55-candidate census")
        censuses.append(census)
    return {"four_closed_halves": True, "exact_split_midpoint": str(MID_P),
            "enhanced_55_candidate_censuses": censuses,
            "all_full_certificate_semantics_recomputed": True}


def validate_reflection(rows: dict[str, list[dict[str, Any]]]) -> None:
    interiors = rows["interior"]
    expected_pairs = ((interiors[0], interiors[3]), (interiors[1], interiors[2]))
    need(len(rows["reflection"]) == 2, "two reflection rows")
    for transport, (representative, reflected) in zip(rows["reflection"], expected_pairs):
        rep_box, ref_box = representative["closed_box"], reflected["closed_box"]
        exact_reflection = {
            "compact_chart": "E",
            "t": [str(-as_q(rep_box["t"][1])), str(-as_q(rep_box["t"][0]))],
            "p": [str(-as_q(rep_box["p"][1])), str(-as_q(rep_box["p"][0]))],
            "s": rep_box["s"],
        }
        need(ref_box == exact_reflection and
             transport.get("exact_map") == "(t,p,s)->(-t,-p,s)" and
             transport.get("representative_certificate_id") ==
             representative["interior_certificate_id"] and
             transport.get("reflected_certificate_id") ==
             reflected["interior_certificate_id"] and
             transport.get("representative_closed_box") == rep_box and
             transport.get("reflected_closed_box") == ref_box and
             transport.get("endpoint_order_reversal_materialized") is True and
             transport.get("strict_owner_mismatch_preserved") is True and
             transport.get("empty_wall_word_preserved") is True and
             transport.get("reflection_transport_terminal_credit") == 1,
             "exact reflection/order reversal")


def validate_incidence(rows: dict[str, list[dict[str, Any]]],
                       c41_rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    # Incidence is global across compact-cell seams: the p_upper neighbour,
    # for example, belongs to pair 153 rather than pair 391.
    ambient = [row for row in c41_rows["routed_ambient_cells.jsonl.gz"]
               if row.get("closed_representative_box") is not None]
    need(len(c41_rows["routed_ambient_cells.jsonl.gz"]) == 91879,
         "global C41 ambient census")
    indexes = lower_indexes()
    face_counts: list[int] = []
    direct_censuses: list[dict[str, int]] = []
    reflected_restrictions: list[str] = []
    for ordinal, face in enumerate(rows["faces"]):
        box = face["exact_closed_face_box"]
        incident_source = [row for row in ambient
                           if box_contains(row["closed_representative_box"], box)]
        expected = sorted((incident_record(row) for row in incident_source), key=owner_key)
        need(len(expected) == 2 and face.get("incident_ambient_cells") == expected and
             face.get("incident_cell_count") == 2 and
             face.get("owner_incident") == expected[0] and
             face.get("owner_is_terminal_after_C42") is True and
             face.get("face_has_no_unresolved_wall_endpoint") is True,
             "global face incidence:" + str(face.get("face")))
        direct = face.get("direct_closed_face_certificate")
        need(type(direct) is dict and direct.get("closed_box") == box and
             direct.get("Round185_status") == "LOCAL_EXACT_KEY" and
             direct.get("owner_mismatch_is_uniform_on_entire_closed_box") is True,
             "direct face lower certificate")
        face_box = box_from_payload(box, TARGET_PATH + ".face." + str(ordinal))
        independent, census = independent_certificate(
            "REPRESENTATIVE", REP_PARENT, face_box, 100 + ordinal,
            "FACE_RESTRICTION_NO_MID_FACE_ROLE", indexes)
        need(direct == independent, "full independent direct face certificate")
        reflected, reflected_census = independent_certificate(
            "REFLECTED", REF_PARENT,
            reflected_box(face_box, TARGET_PATH + ".face.reflected." + str(ordinal)),
            300 + ordinal, "FACE_RESTRICTION_NO_MID_FACE_ROLE", indexes)
        need(sum(reflected_census.values()) == 55,
             "complete reflected face 55-candidate restriction")
        direct_censuses.append(census)
        reflected_restrictions.append(digest(reflected))
        face_counts.append(len(expected))
    corner_counts: list[int] = []
    for ordinal, corner in enumerate(rows["corners"]):
        box = corner["exact_closed_corner_box"]
        incident_source = [row for row in ambient
                           if box_contains(row["closed_representative_box"], box)]
        expected = sorted((incident_record(row) for row in incident_source), key=owner_key)
        need(len(expected) in (3, 4) and
             corner.get("global_incident_ambient_cells") == expected and
             corner.get("global_incident_cell_count") == len(expected) and
             corner.get("owner_incident") == expected[0] and
             corner.get("owner_is_terminal_after_C42") is True and
             corner.get("all_incidents_terminal_after_C42") is True and
             corner.get("global_incident_census_complete") is True and
             corner.get("corner_has_no_unresolved_wall_endpoint") is True,
             "global corner incidence:" + str(corner.get("corner")))
        direct = corner.get("direct_closed_point_certificate")
        need(type(direct) is dict and direct.get("closed_box") == box and
             direct.get("Round185_status") == "LOCAL_EXACT_KEY" and
             direct.get("owner_mismatch_is_uniform_on_entire_closed_box") is True,
             "direct corner lower certificate")
        corner_box = box_from_payload(box, TARGET_PATH + ".corner." + str(ordinal))
        independent, census = independent_certificate(
            "REPRESENTATIVE", REP_PARENT, corner_box, 200 + ordinal,
            "ZERO_DIMENSIONAL_OWNER_POINT", indexes)
        need(direct == independent, "full independent direct corner certificate")
        reflected, reflected_census = independent_certificate(
            "REFLECTED", REF_PARENT,
            reflected_box(corner_box, TARGET_PATH + ".corner.reflected." + str(ordinal)),
            400 + ordinal, "ZERO_DIMENSIONAL_OWNER_POINT", indexes)
        need(sum(reflected_census.values()) == 55,
             "complete reflected corner 55-candidate restriction")
        direct_censuses.append(census)
        reflected_restrictions.append(digest(reflected))
        corner_counts.append(len(expected))
    need(face_counts == [2, 2, 2, 2] and sorted(corner_counts) == [3, 3, 4, 4],
         "complete face/corner incidence census")
    return {"global_ambient_rows_scanned": 91879, "face_incident_counts": face_counts,
            "corner_incident_counts": corner_counts,
            "direct_face_corner_55_candidate_censuses": direct_censuses,
            "reflected_face_corner_restriction_count": 8,
            "reflected_face_corner_certificate_sha256": reflected_restrictions}


def q_text(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def validate_parents(rows: dict[str, list[dict[str, Any]]],
                     c41_rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    prior = c41_rows["parent_conservation.jsonl.gz"]
    current = rows["parents"]
    need([row["pair_index"] for row in prior] == list(range(862)) and
         [row["pair_index"] for row in current] == list(range(862)),
         "862 ordered unique parents")
    whole_before = credit_before = whole_after = credit_after = newly_whole = 0
    for old, new in zip(prior, current):
        need(new.get("C41_parent_row_sha256") == old["row_sha256"] and
             new.get("leaf_count") == old["leaf_count"] and
             new.get("parent_Kraft_conservation") == "1",
             "parent source/conservation:" + str(old["pair_index"]))
        old_whole = bool(old["whole_representative_parent_terminal"] and
                         old["whole_reflected_parent_terminal"] and
                         old["nonterminal_leaf_count"] == 0 and
                         old["terminal_reflection_transport_materialized"] and
                         old["unresolved_parent_volume"] == "0")
        if old["pair_index"] == PAIR_INDEX:
            expected_terminal_volume = "1"
            expected_unresolved_volume = "0"
            expected_terminal_leaves = old["terminal_leaf_count"] + 1
            expected_nonterminal_leaves = old["nonterminal_leaf_count"] - 1
            expected_gain = "1/512"
        else:
            expected_terminal_volume = old["terminal_excluded_parent_volume"]
            expected_unresolved_volume = old["unresolved_parent_volume"]
            expected_terminal_leaves = old["terminal_leaf_count"]
            expected_nonterminal_leaves = old["nonterminal_leaf_count"]
            expected_gain = "0"
        derived_whole = bool(expected_terminal_volume == "1" and
                             expected_unresolved_volume == "0" and
                             expected_nonterminal_leaves == 0 and
                             new.get("terminal_reflection_transport_materialized") is True)
        expected_credit = 2 if derived_whole else 0
        expected_new = derived_whole and not old_whole
        need(new.get("C41_terminal_excluded_parent_volume") ==
             old["terminal_excluded_parent_volume"] and
             new.get("C41_unresolved_parent_volume") == old["unresolved_parent_volume"] and
             new.get("terminal_excluded_parent_volume") == expected_terminal_volume and
             new.get("unresolved_parent_volume") == expected_unresolved_volume and
             new.get("C42_terminal_gain") == expected_gain and
             new.get("terminal_leaf_count") == expected_terminal_leaves and
             new.get("nonterminal_leaf_count") == expected_nonterminal_leaves and
             new.get("leaf_count") == expected_terminal_leaves + expected_nonterminal_leaves and
             new.get("whole_representative_parent_terminal") is derived_whole and
             new.get("whole_reflected_parent_terminal") is derived_whole and
             new.get("C34_common_refinement_credit") == expected_credit and
             new.get("newly_whole_terminal_vs_C41") is expected_new,
             "exact parent/credit invariant:" + str(old["pair_index"]))
        whole_before += int(old_whole)
        credit_before += old["C34_common_refinement_credit"]
        whole_after += int(derived_whole)
        credit_after += expected_credit
        newly_whole += int(expected_new)
    need((whole_before, credit_before, whole_after, credit_after, newly_whole) ==
         (286, 572, 287, 574, 1), "global 862 parent credit transition")
    return {"parent_count": 862, "whole_representative_before": 286,
            "whole_representative_after": 287, "paired_credit_before": 572,
            "paired_credit_after": 574, "newly_whole_pair_indexes": [391],
            "formal_unresolved_before": 1152, "formal_unresolved_after": 1150}


def validate_result(result: dict[str, Any], reconstructed: dict[str, Any]) -> None:
    audited = result.get("C41_audited_input")
    nonpromotion = result.get("strict_nonpromotion")
    census = result.get("round144_terminal_census")
    closure = result.get("closure_census")
    pointer_pins = audited.get("installed_pointer_sha256", {}) if type(audited) is dict else {}
    need(type(audited) is dict and
         audited.get("C41_authority_pointers_installed") is True and
         audited.get("object_sha256") == EXPECTED_C41_OBJECT and
         audited.get("independent_audit_object_sha256") == EXPECTED_C41_AUDIT_OBJECT and
         audited.get("independent_audit_status") == EXPECTED_C41_AUDIT_STATUS and
         pointer_pins.get("candidate_pointer_sha256") == EXPECTED_C41_TOKEN_FILE and
         pointer_pins.get("audit_pointer_sha256") == EXPECTED_C41_AUDIT_TOKEN_FILE,
         "C41 audited authority fields")
    need(result.get("formal_authority") is False and
         result.get("authority_pointer_installed") is False and
         result.get("formal_producer_run") is True and
         result.get("producer_output_is_authority") is False and
         result.get("review_only") is False and
         result.get("independent_C42_audit_outstanding") is True and
         type(nonpromotion) is dict and
         nonpromotion.get("formal_producer_pass_is_authority") is False and
         nonpromotion.get("producer_can_mint_C42_authority") is False and
         nonpromotion.get("authority_pointer_installed") is False and
         nonpromotion.get("D02") == "BLOCKED_BY_1150_COMPLETE_R1648_CONTINUATIONS" and
         nonpromotion.get("D03") == "UNAUTHORIZED" and
         nonpromotion.get("D04") == "NOT_MINTED" and
         nonpromotion.get("CM2") == "NO-GO_FOR_CLAIM",
         "strict C42 nonauthority/nonpromotion")
    need(type(census) is dict and census.get("EARLIEST_PREFIX_EXCLUDED") == 75386 and
         census.get("TYPED_EVENT_GRAPH") == 296 and
         census.get("UNRESOLVED_R1648_CONTINUATION") == 1150 and
         census.get("terminal_total") == 76832 and
         census.get("unresolved_zero") is False,
         "Round144 75386+296+1150 conservation")
    need(type(closure) is dict and
         closure.get("whole_terminal_representative_parent_count") == 287 and
         closure.get("whole_terminal_paired_coarse_cell_count") == 574 and
         closure.get("C34_common_refinement_credit_sum") == 574 and
         closure.get("C34_common_refinement_credit_two_row_count") == 287 and
         closure.get("C34_common_refinement_credit_zero_row_count") == 575 and
         closure.get("newly_whole_terminal_representative_parent_count") == 1 and
         closure.get("newly_whole_terminal_paired_coarse_cell_count") == 2 and
         closure.get("parent_credit_regression_count") == 11,
         "C42 closure census")
    lock = result.get("nonpromotion_lock")
    need(type(lock) is dict and lock == {
        "filename": EXPECTED_LOCK, "sha256": EXPECTED_LOCK_SHA256,
        "size": len(EXPECTED_LOCK_BYTES),
        "producer_mode_semantic": "formal producer pass pending an independent C42 audit",
        "producer_output_is_authority": False,
    }, "exact result lock descriptor")
    need(result.get("execution_receipt_policy") ==
         "out-of-band self-hashed receipt binds InvocationID/PID, source SHA, candidate "
         "object and root manifest through O_EXCL, fsync and atomic no-replace publication; "
         "no producer receipt carries authority", "receipt hardening policy")
    need(reconstructed["parents"]["paired_credit_after"] == 574,
         "result/reconstruction credit")


def reclose_row(row: dict[str, Any], id_field: str | None,
                prefix: str | None) -> None:
    row.pop("row_sha256", None)
    if id_field is not None:
        row.pop(id_field, None)
        row[id_field] = prefix + digest(row)
    row["row_sha256"] = digest(row)


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("object_sha256", None)
    result["object_sha256"] = digest(result)


def rejected(label: str, operation: Callable[[], None]) -> bool:
    try:
        operation()
    except Exception:
        return True
    raise Reject("hostile mutation accepted:" + label)


def mutation_suite(result: dict[str, Any], rows: dict[str, list[dict[str, Any]]],
                   c41_rows: dict[str, list[dict[str, Any]]],
                   reconstructed: dict[str, Any]) -> dict[str, bool]:
    attacks: dict[str, bool] = {}

    def result_attack(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        value = copy.deepcopy(result)
        mutate(value)
        reclose_result(value)
        attacks[label] = rejected(label, lambda: validate_result(value, reconstructed))

    def ledger_attack(label: str, ledger: str, ordinal: int,
                      mutate: Callable[[dict[str, Any]], None],
                      validator: Callable[[dict[str, list[dict[str, Any]]]], Any]) -> None:
        value = copy.deepcopy(rows)
        mutate(value[ledger][ordinal])
        filename, field, prefix = LEDGERS[ledger]
        del filename
        reclose_row(value[ledger][ordinal], field, prefix)
        attacks[label] = rejected(label, lambda: validator(value))

    result_attack("result_formal_authority", lambda value: value.__setitem__("formal_authority", True))
    result_attack("result_pointer_installed", lambda value: value.__setitem__("authority_pointer_installed", True))
    result_attack("result_not_formal_run", lambda value: value.__setitem__("formal_producer_run", False))
    result_attack("result_producer_authority", lambda value: value.__setitem__("producer_output_is_authority", True))
    result_attack("nonpromotion_formal_authority", lambda value: value["strict_nonpromotion"].__setitem__("formal_producer_pass_is_authority", True))
    result_attack("nonpromotion_D02", lambda value: value["strict_nonpromotion"].__setitem__("D02", "PASS"))
    result_attack("nonpromotion_D03", lambda value: value["strict_nonpromotion"].__setitem__("D03", "AUTHORIZED"))
    result_attack("round144_terminal", lambda value: value["round144_terminal_census"].__setitem__("EARLIEST_PREFIX_EXCLUDED", 75387))
    result_attack("round144_unresolved", lambda value: value["round144_terminal_census"].__setitem__("UNRESOLVED_R1648_CONTINUATION", 1149))
    result_attack("round144_total", lambda value: value["round144_terminal_census"].__setitem__("terminal_total", 76831))
    result_attack("closure_whole", lambda value: value["closure_census"].__setitem__("whole_terminal_representative_parent_count", 288))
    result_attack("closure_credit", lambda value: value["closure_census"].__setitem__("C34_common_refinement_credit_sum", 576))
    result_attack("closure_new_parent", lambda value: value["closure_census"].__setitem__("newly_whole_terminal_representative_parent_count", 2))
    result_attack("C41_pointer_claim", lambda value: value["C41_audited_input"].__setitem__("C41_authority_pointers_installed", False))
    result_attack("C41_candidate_pointer_sha", lambda value: value["C41_audited_input"]["installed_pointer_sha256"].__setitem__("candidate_pointer_sha256", "0" * 64))
    result_attack("C41_audit_pointer_sha", lambda value: value["C41_audited_input"]["installed_pointer_sha256"].__setitem__("audit_pointer_sha256", "0" * 64))
    result_attack("lock_authority", lambda value: value["nonpromotion_lock"].__setitem__("producer_output_is_authority", True))
    result_attack("lock_sha", lambda value: value["nonpromotion_lock"].__setitem__("sha256", "0" * 64))
    result_attack("receipt_policy", lambda value: value.__setitem__("execution_receipt_policy", "ordinary write"))

    source_validator = lambda value: validate_source(value, c41_rows)
    ledger_attack("source_pair", "exact_source", 0,
                  lambda row: row.__setitem__("pair_index", 390), source_validator)
    ledger_attack("source_ambient", "exact_source", 0,
                  lambda row: row.__setitem__("C41_target_ambient_cell_id", "c41-ambient:" + "0" * 64), source_validator)
    ledger_attack("source_audit", "exact_source", 0,
                  lambda row: row.__setitem__("C41_independent_audit_object_sha256", "0" * 64), source_validator)
    ledger_attack("source_pointer", "exact_source", 0,
                  lambda row: row.__setitem__("C41_candidate_and_audit_pointers_installed", False), source_validator)
    ledger_attack("source_authority", "exact_source", 0,
                  lambda row: row.__setitem__("producer_output_is_authority", True), source_validator)
    ledger_attack("source_volume", "exact_source", 0,
                  lambda row: row.__setitem__("source_parent_volume_fraction", "1/256"), source_validator)

    interior_validator = lambda value: validate_interiors(value)
    ledger_attack("interior_owner", "interior", 0,
                  lambda row: row.__setitem__("absolute_collision2_owner", "G[0,1]"), interior_validator)
    ledger_attack("interior_live_owner", "interior", 0,
                  lambda row: row.__setitem__("expected_live_collision2_owner", "G[1,0]"), interior_validator)
    ledger_attack("interior_status", "interior", 0,
                  lambda row: row.__setitem__("Round185_status", "WALL_ENDPOINT"), interior_validator)
    ledger_attack("interior_box", "interior", 0,
                  lambda row: row["closed_box"]["p"].__setitem__(1, "35/64"), interior_validator)
    ledger_attack("interior_wall", "interior", 1,
                  lambda row: row.__setitem__("wall_endpoint_or_corner_present_on_closed_box", True), interior_validator)
    ledger_attack("interior_event", "interior", 1,
                  lambda row: row["strict_axis_endpoint_certificates"][0]["ordered_axis_event_tokens"].append("X=0"), interior_validator)
    ledger_attack("interior_gate", "interior", 2,
                  lambda row: row["official_gate5_key"].__setitem__("ordinal_zero_based", 0), interior_validator)

    reflection_validator = lambda value: (validate_interiors(value), validate_reflection(value))
    ledger_attack("reflection_map", "reflection", 0,
                  lambda row: row.__setitem__("exact_map", "identity"), reflection_validator)
    ledger_attack("reflection_credit", "reflection", 0,
                  lambda row: row.__setitem__("reflection_transport_terminal_credit", 0), reflection_validator)
    ledger_attack("reflection_reversal", "reflection", 1,
                  lambda row: row.__setitem__("endpoint_order_reversal_materialized", False), reflection_validator)

    incidence_validator = lambda value: validate_incidence(value, c41_rows)
    ledger_attack("face_count", "faces", 0,
                  lambda row: row.__setitem__("incident_cell_count", 1), incidence_validator)
    ledger_attack("face_owner", "faces", 1,
                  lambda row: row.__setitem__("owner_incident", row["incident_ambient_cells"][-1]), incidence_validator)
    ledger_attack("face_direct", "faces", 2,
                  lambda row: row["direct_closed_face_certificate"].__setitem__("Round185_status", "FAIL"), incidence_validator)
    ledger_attack("corner_count", "corners", 0,
                  lambda row: row.__setitem__("global_incident_cell_count", 2), incidence_validator)
    ledger_attack("corner_all_terminal", "corners", 1,
                  lambda row: row.__setitem__("all_incidents_terminal_after_C42", False), incidence_validator)
    ledger_attack("corner_direct", "corners", 2,
                  lambda row: row["direct_closed_point_certificate"].__setitem__("Round185_status", "FAIL"), incidence_validator)

    parent_validator = lambda value: validate_parents(value, c41_rows)
    ledger_attack("whole_credit_zero", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("C34_common_refinement_credit", 0), parent_validator)
    ledger_attack("credit_one", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("C34_common_refinement_credit", 1), parent_validator)
    ledger_attack("partial_credit_two", "parents", 1,
                  lambda row: row.__setitem__("C34_common_refinement_credit", 2), parent_validator)
    ledger_attack("target_nonterminal", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("nonterminal_leaf_count", 1), parent_validator)
    ledger_attack("target_reflection", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("terminal_reflection_transport_materialized", False), parent_validator)
    ledger_attack("target_newly_whole", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("newly_whole_terminal_vs_C41", False), parent_validator)
    ledger_attack("target_gain", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("C42_terminal_gain", "0"), parent_validator)
    ledger_attack("target_terminal_leaves", "parents", PAIR_INDEX,
                  lambda row: row.__setitem__("terminal_leaf_count", 83), parent_validator)
    value = copy.deepcopy(rows)
    value["parents"][0], value["parents"][1] = value["parents"][1], value["parents"][0]
    attacks["parent_out_of_order"] = rejected(
        "parent_out_of_order", lambda: validate_parents(value, c41_rows))
    value = copy.deepcopy(rows)
    value["parents"].pop()
    attacks["parent_missing"] = rejected("parent_missing",
                                           lambda: validate_parents(value, c41_rows))
    need(len(attacks) >= 50 and all(attacks.values()), "complete hostile matrix")
    return attacks


def formal_pins_ready() -> bool:
    return bool(HEX64.fullmatch(EXPECTED_PRODUCER_SOURCE) and
                HEX64.fullmatch(EXPECTED_CANDIDATE_OBJECT) and
                HEX64.fullmatch(EXPECTED_RECEIPT_OBJECT) and
                EXPECTED_CANDIDATE_STATUS.startswith("FORMAL_") and
                EXPECTED_RECEIPT_STATUS.startswith("FORMAL_"))


def core_projection(candidate: Path, receipt: Path,
                    invocation_id: str) -> dict[str, Any]:
    need(formal_pins_ready(), "formal C42 pins pending")
    no_producer_import()
    need(file_sha(PRODUCER) == EXPECTED_PRODUCER_SOURCE, "frozen C42 producer")
    ctx.prec = PRECISION_BITS
    producer_hardening = producer_hardening_self_test()
    candidate, receipt = candidate_paths(candidate, receipt)
    c41_result, c41_rows = capture_c41_authority()
    captured = capture_candidate(candidate)
    receipt_value = capture_receipt(receipt, invocation_id, captured)
    ambient = validate_source(captured["rows"], c41_rows)
    math = validate_interiors(captured["rows"])
    validate_reflection(captured["rows"])
    incidence = validate_incidence(captured["rows"], c41_rows)
    parents = validate_parents(captured["rows"], c41_rows)
    reconstructed = {
        "exact_source_ambient_id": ambient["c41_ambient_cell_id"],
        "math": math, "incidence": incidence, "parents": parents,
    }
    validate_result(captured["result"], reconstructed)
    attacks = mutation_suite(captured["result"], captured["rows"], c41_rows,
                             reconstructed)
    replay = capture_candidate(candidate)
    replay_receipt = capture_receipt(receipt, invocation_id, replay)
    need(replay["payloads"] == captured["payloads"] and
         replay_receipt == receipt_value, "terminal candidate/receipt byte replay")
    return {
        "schema": SCHEMA + ".core-projection.v1",
        "candidate_path": str(candidate.relative_to(ROOT)),
        "candidate_object_sha256": EXPECTED_CANDIDATE_OBJECT,
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "root_manifest_sha256": captured["manifest_sha256"],
        "execution_receipt_object_sha256": EXPECTED_RECEIPT_OBJECT,
        "InvocationID": invocation_id,
        "C41_candidate_object_sha256": c41_result["object_sha256"],
        "C41_independent_audit_object_sha256": EXPECTED_C41_AUDIT_OBJECT,
        "C41_independent_audit_status": EXPECTED_C41_AUDIT_STATUS,
        "ledger_row_counts": {key: len(value) for key, value in captured["rows"].items()},
        "reconstructed": reconstructed,
        "producer_hardening_self_test": producer_hardening,
        "hostile_mutations": attacks,
        "strict_nonpromotion": captured["result"]["strict_nonpromotion"],
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
    }


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    current = environment.get("PYTHONPATH")
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = (str(DELIVERABLES) if not current else
                                  str(DELIVERABLES) + os.pathsep + current)
    return environment


def producer_hardening_self_test() -> dict[str, Any]:
    """Execute, but never import, the frozen producer's destructive-envelope tests."""
    process = subprocess.run([sys.executable, str(PRODUCER), "--self-test"],
                             cwd=ROOT, env=child_environment(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             check=False, timeout=900)
    need(process.returncode == 0 and process.stderr == b"",
         "producer hardening self-test:" +
         process.stderr.decode("utf-8", "replace")[-3000:])
    value = strict_json(process.stdout, "producer hardening self-test")
    hardening = value.get("hardening_regressions")
    expected_prewrite = [
        "VALID_DIRECT_CHILD_ENVELOPE_ACCEPTED",
        "OUTPUT_OUTSIDE_CANDIDATE_ROOT_REJECTED",
        "RECEIPT_OUTSIDE_AUDIT_ROOT_REJECTED",
        "OUTPUT_RECEIPT_TOKEN_MISMATCH_REJECTED",
        "PREEXISTING_INPUT_CANDIDATE_OUTPUT_REJECTED",
        "SYMLINK_ALIAS_INPUT_REJECTED",
        "PREEXISTING_RECEIPT_SYMLINK_REJECTED",
        "CANDIDATE_RENAME_NOREPLACE_COLLISION_REJECTED",
    ]
    expected_orphan = [
        "AFTER_OUTPUT_RENAME_CLEANUP_TRIGGERED",
        "AFTER_RECEIPT_PARENT_CREATE_CLEANUP_TRIGGERED",
        "AFTER_RECEIPT_STAGE_WRITE_CLEANUP_TRIGGERED",
        "AFTER_RECEIPT_FINAL_RENAME_CLEANUP_TRIGGERED",
    ]
    pointers = value.get("installed_C41_pointer_sha256")
    need(value.get("status") ==
         "PASS_C42_HARDENED_SELF_TEST__C41_AUDIT_BOUND__PREWRITE_AND_ORPHAN_REGRESSIONS_PASS" and
         value.get("formal_gate_ready") is True and
         value.get("C41_independent_audit_object_sha256") == EXPECTED_C41_AUDIT_OBJECT and
         value.get("C41_independent_audit_status") == EXPECTED_C41_AUDIT_STATUS and
         pointers == {"candidate_pointer_sha256": EXPECTED_C41_TOKEN_FILE,
                      "audit_pointer_sha256": EXPECTED_C41_AUDIT_TOKEN_FILE} and
         type(hardening) is dict and hardening.get("prewrite_case_count") == 8 and
         hardening.get("prewrite_cases") == expected_prewrite and
         hardening.get("injected_orphan_case_count") == 4 and
         hardening.get("injected_orphan_cases") == expected_orphan and
         hardening.get("orphan_candidate_count_after_cleanup") == 0 and
         hardening.get("orphan_receipt_count_after_cleanup") == 0,
         "complete producer path/authority/atomic hardening self-test")
    return {"status": value["status"], "hardening_regressions": hardening,
            "producer_source_sha256": EXPECTED_PRODUCER_SOURCE}


def cold_core(candidate: Path, receipt: Path,
              invocation_id: str) -> tuple[dict[str, Any], bytes]:
    command = [sys.executable, str(Path(__file__).resolve()), "--core-projection",
               "--candidate", str(candidate), "--receipt", str(receipt),
               "--invocation-id", invocation_id]
    process = subprocess.run(command, cwd=ROOT, env=child_environment(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             check=False, timeout=1800)
    need(process.returncode == 0 and process.stderr == b"",
         "fresh C42 core:" + process.stderr.decode("utf-8", "replace")[-3000:])
    return strict_json(process.stdout, "fresh C42 core"), process.stdout


def output_preflight(output: Path, candidate: Path, receipt: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(output)))
    need(absolute == absolute.resolve(strict=False) and
         absolute.name == "independent_audit.json" and not absolute.exists(),
         "canonical fresh audit output")
    audit_root = (ROOT / ".cm2-runtime/audit").resolve(strict=True)
    need(absolute.parent.parent == audit_root and not absolute.parent.exists() and
         TOKEN.fullmatch(absolute.parent.name) is not None,
         "fresh direct-child audit token")
    protected = (candidate.resolve(strict=True), receipt.resolve(strict=True).parent,
                 EXPECTED_C41_CANDIDATE, EXPECTED_C41_RECEIPT.parent,
                 EXPECTED_C41_AUDIT.parent, DELIVERABLES)
    for authority in protected:
        authority = authority.resolve(strict=True)
        need(not within(absolute.parent, authority) and
             not within(authority, absolute.parent),
             "audit output bidirectionally disjoint")
    return absolute


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_audit_write(path: Path, value: dict[str, Any]) -> bytes:
    raw = canonical(value) + b"\n"
    stage = path.with_name(path.name + ".stage-" + str(os.getpid()))
    created_stage = created_output = False
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(stage, flags, 0o600)
        created_stage = True
        try:
            view = memoryview(raw)
            while view:
                written = os.write(descriptor, view)
                need(written > 0, "audit short write")
                view = view[written:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.link(stage, path, follow_symlinks=False)
        created_output = True
        stage.unlink()
        created_stage = False
        fsync_directory(path.parent)
        replay = stable_read(path, 16 << 20, "sealed C42 independent audit")
        need(replay == raw, "terminal audit byte replay")
        parsed = strict_json(replay, "sealed C42 independent audit")
        self_closed(parsed, "object_sha256", "sealed C42 independent audit")
        return replay
    except Exception:
        if created_stage and stage.exists():
            stage.unlink()
        if created_output and path.exists():
            path.unlink()
        fsync_directory(path.parent)
        raise


def no_c42_pointer() -> None:
    for name in ("c42-current-token", "c42-current-audit-token"):
        need(not (ROOT / ".cm2-runtime" / name).exists(), "no C42 authority pointer:" + name)


def run_audit(candidate: Path, receipt: Path, invocation_id: str,
              output: Path) -> dict[str, Any]:
    no_c42_pointer()
    candidate, receipt = candidate_paths(candidate, receipt)
    output = output_preflight(output, candidate, receipt)
    created_parent = False
    try:
        output.parent.mkdir(mode=0o700, parents=False, exist_ok=False)
        created_parent = True
        first, first_raw = cold_core(candidate, receipt, invocation_id)
        second, second_raw = cold_core(candidate, receipt, invocation_id)
        need(first == second and first_raw == second_raw,
             "two byte-identical fresh-process C42 cores")
        attacks = dict(first["hostile_mutations"])
        attacks.update({"cold_core_byte_identity": True,
                        "candidate_terminal_byte_replay": True,
                        "atomic_audit_seal": True})
        need(len(attacks) >= 53 and all(attacks.values()), "full C42 hostile matrix")
        audit: dict[str, Any] = {
            "schema": SCHEMA,
            "status": ("PASS_INDEPENDENT_C42_P391_OWNER_CLOSURE_AUDIT__" +
                       f"{len(attacks)}_OF_{len(attacks)}_ATTACKS_FAIL_CLOSED"),
            "candidate_path": first["candidate_path"],
            "candidate_object_sha256": EXPECTED_CANDIDATE_OBJECT,
            "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
            "root_manifest_sha256": first["root_manifest_sha256"],
            "execution_receipt_object_sha256": EXPECTED_RECEIPT_OBJECT,
            "InvocationID": invocation_id,
            "C41_candidate_object_sha256": EXPECTED_C41_OBJECT,
            "C41_independent_audit_object_sha256": EXPECTED_C41_AUDIT_OBJECT,
            "C41_independent_audit_status": EXPECTED_C41_AUDIT_STATUS,
            "independent_auditor_source_sha256": file_sha(Path(__file__).resolve()),
            "method": ("no C42 producer import; installed C41 candidate+audit authority; "
                       "independent Round185 recomputation of 4 interiors, 4 faces, 4 corners "
                       "and 8 reflected restrictions with complete 55-candidate censuses; "
                       "global 91,879 ambient incidence; exact 862-parent credit; producer "
                       "8 prewrite plus 4 orphan-cleanup hardening regressions; 51 semantic "
                       "mutations; two fresh cores; atomic no-replace seal"),
            "cold_core_projection_sha256": hashlib.sha256(first_raw).hexdigest(),
            "cold_core_projection_byte_count": len(first_raw),
            "reconstructed": first["reconstructed"],
            "producer_hardening_self_test": first["producer_hardening_self_test"],
            "attacks": attacks,
            "strict_nonpromotion": first["strict_nonpromotion"],
            "producer_output_is_authority": False,
            "authority_pointer_installed": False,
        }
        audit["object_sha256"] = digest(audit)
        atomic_audit_write(output, audit)
        final_candidate = capture_candidate(candidate)
        final_receipt = capture_receipt(receipt, invocation_id, final_candidate)
        need(final_candidate["result"]["object_sha256"] == EXPECTED_CANDIDATE_OBJECT and
             final_receipt["receipt_object_sha256"] == EXPECTED_RECEIPT_OBJECT,
             "post-seal candidate/receipt replay")
        no_c42_pointer()
        return audit
    except Exception:
        if output.exists():
            output.unlink()
        if created_parent and output.parent.exists() and not any(output.parent.iterdir()):
            output.parent.rmdir()
            fsync_directory(output.parent.parent)
        raise


def self_test() -> dict[str, Any]:
    no_producer_import()
    pending = all(value.startswith("PENDING_") for value in (
        EXPECTED_PRODUCER_SOURCE, EXPECTED_CANDIDATE_OBJECT,
        EXPECTED_CANDIDATE_STATUS, EXPECTED_RECEIPT_OBJECT,
        EXPECTED_RECEIPT_STATUS))
    need(pending != formal_pins_ready(), "consistent formal/pending pins")
    need(file_sha(Path(c41a.__file__).resolve()) == EXPECTED_C41_AUDITOR_SOURCE,
         "C41 auditor source self-test")
    need(EXPECTED_LOCK == "C42_SINGLETON_CLOSURE.lock" and PAIR_INDEX == 391 and
         MID_P == Q(1119, 2048), "C42 exact constants")
    return {
        "status": ("PASS_C42_INDEPENDENT_AUDITOR_FORMAL_PIN_SELF_TEST" if
                   formal_pins_ready() else
                   "PASS_C42_INDEPENDENT_AUDITOR_PROVISIONAL_SELF_TEST__FORMAL_PINS_PENDING"),
        "formal_pins_ready": formal_pins_ready(),
        "no_C42_producer_import": True,
        "C41_independent_audit_object_sha256": EXPECTED_C41_AUDIT_OBJECT,
        "precision_bits": PRECISION_BITS,
        "pair_index": PAIR_INDEX,
        "exact_split_midpoint": str(MID_P),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--invocation-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--core-projection", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        print(canonical(self_test()).decode())
        return 0
    need(arguments.candidate is not None and arguments.receipt is not None and
         arguments.invocation_id is not None, "candidate/receipt/InvocationID")
    if arguments.core_projection:
        need(arguments.output is None, "core projection has no output")
        print(canonical(core_projection(arguments.candidate, arguments.receipt,
                                        arguments.invocation_id)).decode())
        return 0
    need(arguments.output is not None, "audit output")
    audit = run_audit(arguments.candidate, arguments.receipt,
                      arguments.invocation_id, arguments.output)
    print(canonical({"status": audit["status"],
                     "object_sha256": audit["object_sha256"],
                     "authority_pointer_installed": False}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
