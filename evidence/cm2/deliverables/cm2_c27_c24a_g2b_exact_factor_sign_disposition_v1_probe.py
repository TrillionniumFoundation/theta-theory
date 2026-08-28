#!/usr/bin/env python3
"""Exact factor-sign disposition of the 18,800 C24A G2B envelope pairs.

This probe is C27-independent.  It consumes the append-only outer-envelope
candidate ledger produced by the full-support v3 diagnostic and classifies
each candidate as exact positive support or exact empty intersection.  An
envelope hit is never used as support evidence by itself.

Every root input is captured through one O_NOFOLLOW file descriptor and is
hashed, parsed, and post-fstat checked through that same open description.
The result is deliberately zero-credit until an independently written
verifier, two seeds, coherent attacks, priority joins, and component-edge
deduplication are complete.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent

C10 = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C11A = "cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_ledger.jsonl.gz"
C11BR = "cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_relation_theorem_ledger.jsonl.gz"
C11BI = "cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_interface_kernel_ledger.jsonl.gz"
C12A = "cm2_round306c12a_source_g_rerouted_shared_side_kernel_ledger.jsonl.gz"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C22A = "cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz"
C24A = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"

PINS = {
    C10: "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",
    C11A: "87a37e007408adf667ae30a7575c928263512bf8a08cfd9e7144db11296680cd",
    C11BR: "37155fe874b8f4acd49773c013f4ec605a2f9388a0d1eb7443c88a731f1e0299",
    C11BI: "815ed3b2ab73b3165e203cf8215421c89412b6d4f5190b816cb0d2e02f409a59",
    C12A: "12ae529eb5ccb53b75da1622c2c7b655a2acea6faf25d9018871a4fd079b35b9",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C22A: "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",
    C24A: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    need("row_sha256" not in row, "fresh row")
    row["row_sha256"] = digest(row)
    return row


def check_closed(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":closure")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid,
    )


@dataclass
class Capture:
    label: str
    path: Path
    expected_sha256: str
    fd: int
    pre: tuple[int, ...]
    observed_sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            pre_stat = os.fstat(fd)
            need(stat.S_ISREG(pre_stat.st_mode), label + ":regular file")
            state = hashlib.sha256()
            while block := os.read(fd, 4 * 1024 * 1024):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":sha256 pin")
            need(fingerprint(os.fstat(fd)) == fingerprint(pre_stat), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, path, expected, fd, fingerprint(pre_stat), observed)
        except BaseException:
            os.close(fd)
            raise

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:newline:{ordinal}")
                    encoded = line[:-1]
                    row = json.loads(encoded)
                    need(type(row) is dict and canonical(row) == encoded,
                         f"{self.label}:canonical:{ordinal}")
                    check_closed(row, f"{self.label}:{ordinal}")
                    yield row
        self.unchanged("parse")

    def document(self) -> dict[str, Any]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 * 1024 * 1024):
            chunks.append(block)
        encoded = b"".join(chunks)
        row = json.loads(encoded)
        need(type(row) is dict and canonical(row) + b"\n" == encoded,
             self.label + ":canonical document")
        body = dict(row)
        claimed = body.pop("result_sha256", None)
        need(type(claimed) is str and claimed == digest(body), self.label + ":closure")
        self.unchanged("parse")
        return row

    def unchanged(self, phase: str) -> None:
        need(fingerprint(os.fstat(self.fd)) == self.pre, f"{self.label}:{phase}:fstat")

    def attestation(self) -> dict[str, Any]:
        self.unchanged("final")
        return {
            "filename": self.path.name,
            "observed_sha256": self.observed_sha256,
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
            "stat_fingerprint": list(self.pre),
        }

    def close(self) -> None:
        os.close(self.fd)


def strict_predicate(ast: Any) -> dict[str, Any]:
    found: list[dict[str, Any]] = []

    def visit(node: Any) -> None:
        if type(node) is dict:
            if node.get("op") in {"LT", "GT"}:
                found.append(node)
            else:
                for value in node.values():
                    visit(value)
        elif type(node) is list:
            for value in node:
                visit(value)

    visit(ast)
    need(len(found) == 1, "unique strict predicate")
    return found[0]


def strip_unit(expr: Any) -> tuple[int, Any]:
    if type(expr) is dict and expr.get("op") == "MUL" and type(expr.get("args")) is list:
        units: list[int] = []
        others: list[Any] = []
        for arg in expr["args"]:
            if (
                type(arg) is dict and arg.get("op") == "RATIONAL_CONSTANT"
                and Fraction(arg["value"]) in {-1, 1}
            ):
                units.append(int(Fraction(arg["value"])))
            else:
                others.append(arg)
        if len(units) == len(others) == 1:
            return units[0], others[0]
    return 1, expr


def is_zero(node: Any) -> bool:
    return (
        type(node) is dict and node.get("op") == "RATIONAL_CONSTANT"
        and Fraction(node["value"]) == 0
    )


def sign(value: str) -> int:
    need(value in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "strict sign")
    return 1 if value == "STRICT_POSITIVE" else -1


def sign_name(value: int) -> str:
    need(value in {-1, 1}, "sign integer")
    return "STRICT_POSITIVE" if value == 1 else "STRICT_NEGATIVE"


def simple_t_factor_sign(expr: Any, bounds: list[str]) -> int:
    need(type(expr) is dict and expr.get("op") == "MUL", "simple t factor MUL")
    coefficient: Fraction | None = None
    coordinate: str | None = None
    for arg in expr["args"]:
        if arg.get("op") == "RATIONAL_CONSTANT":
            coefficient = Fraction(arg["value"])
        elif arg.get("op") == "COORDINATE":
            coordinate = arg["name"]
    need(coefficient not in {None, Fraction(0)} and coordinate == "t", "simple t factor")
    lower, upper = map(Fraction, bounds[:2])
    need(lower < upper and (upper <= 0 or lower >= 0), "one-sided t box")
    t_sign = -1 if upper <= 0 else 1
    return (1 if coefficient > 0 else -1) * t_sign


def source_t_identity(authority: dict[str, Any]) -> str:
    need(
        authority["kind"] == "WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_AUTHORITY"
        and authority.get("exact_source_factor_identity")
            == "source transverse wall factor = (9/25)*t with chart-dependent sign"
        and authority.get("excluded_zero_face") == "t=0",
        "R235D exact source factor identity",
    )
    reason = authority["reason_label"]
    need(reason in {
        "wall_endpoint_or_count_transition:X:0",
        "wall_endpoint_or_count_transition:Y:0",
    }, "R235D zero-wall reason")
    axis = reason.split(":")[1].lower()
    need(
        authority["equation"] == f"(source_{axis}-0)*(target_{axis}-0)=0",
        "R235D primitive factor equation",
    )
    return reason


def wall_authority_closed(authority: dict[str, Any], theorem: dict[str, Any]) -> None:
    need(
        theorem["case_kind"] == "WALL_CONNECTED_STRICT_SIDE"
        and authority["kind"] == "WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_AUTHORITY",
        "wall theorem kind",
    )
    source_sign = authority["witness_source_factor_sign"]
    target_sign = authority["witness_target_factor_sign"]
    need(
        sign(authority["region_product_sign"]) == sign(source_sign) * sign(target_sign),
        "wall product sign",
    )
    atoms = theorem["source_predicate_ast"]["atoms"]
    need(
        atoms == [
            {"equation": authority["equation"], "op": "EXACT_FACTOR_EQUATION",
             "reason_label": authority["reason_label"]},
            {"op": "ONE_SIDED_SOURCE_FACTOR_STRICT_SIGN", "sign": source_sign},
            {"op": "CONNECTED_TARGET_FACTOR_SIDE_SIGN", "sign": target_sign},
            {"factor": "SOURCE_FACTOR_TIMES_TARGET_FACTOR", "op": "DERIVED_PRODUCT_SIGN",
             "sign": authority["region_product_sign"]},
        ],
        "wall theorem exact primitive sign atoms",
    )


def write_rows(path: Path, rows: list[dict[str, Any]]) -> tuple[str, str, int]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            for row in rows:
                encoded = canonical(row)
                sequence.update(bytes.fromhex(row["row_sha256"]))
                stream.write(encoded + b"\n")
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest(), sequence.hexdigest(), len(rows)


def build(args: argparse.Namespace) -> dict[str, Any]:
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)
    captures: dict[str, Capture] = {}
    try:
        for name, expected in PINS.items():
            captures[name] = Capture.open(name, ROOT / name, expected)
        candidate_path = Path(args.candidate_ledger)
        predecessor_path = Path(args.predecessor_result)
        captures["candidate_ledger"] = Capture.open(
            "candidate_ledger", candidate_path, args.candidate_ledger_sha256
        )
        captures["predecessor_result"] = Capture.open(
            "predecessor_result", predecessor_path, args.predecessor_result_sha256
        )

        predecessor = captures["predecessor_result"].document()
        scan = predecessor["C24A_G2B_interval_envelope_scan"]
        need(
            predecessor["status"]
                == "BLOCKED_ZERO_CREDIT__C24A_ENVELOPE_SCAN_MATERIALIZED__EXACT_RELATION_AND_RELATIVE_2D_ROUTES_OPEN"
            and scan["distinct_envelope_candidate_pair_count"] == 18_800
            and scan["R300C_validation_pair_count"] == 906
            and scan["ledger_file_sha256"] == args.candidate_ledger_sha256
            and scan["ledger_filename"] == candidate_path.name,
            "predecessor exact candidate binding",
        )

        candidates = list(captures["candidate_ledger"].rows())
        need(
            len(candidates) == 18_800
            and len({(row["left_member_id"], row["right_member_id"]) for row in candidates})
                == 18_800,
            "candidate census and uniqueness",
        )
        c24_needed = {row["c24_row_sha256"] for row in candidates}
        c22_needed = {row["target_row_sha256"] for row in candidates}
        member_needed = {
            member for row in candidates
            for member in (row["c24_member_id"], row["target_member_id"])
        }

        c10: dict[str, dict[str, Any]] = {}
        for row in captures[C10].rows():
            equation = row["equation_ast"]
            unit, core = strip_unit(equation["left"])
            need(unit == 1 and equation["op"] == "EQ" and is_zero(equation["right"]),
                 "C10 primitive zero equation")
            c10[row["graph_id"]] = {
                "core_sha256": digest(core),
                "core": core if row["graph_class"] == "R235D_SOURCE_EXACT_FACE_FULL_BASE" else None,
                "graph_class": row["graph_class"],
                "row_sha256": row["row_sha256"],
            }
        need(len(c10) == 5_264, "C10 census")

        c24: dict[str, dict[str, Any]] = {}
        c24_authority_ids: dict[str, set[str]] = {
            "C11A": set(), "C11B": set(), "C12A": set()
        }
        for row in captures[C24A].rows():
            if row["row_sha256"] not in c24_needed:
                continue
            predicate = strict_predicate(row["normalized_support_ast"])
            unit, core = strip_unit(predicate["left"])
            graph = c10[row["graph_id"]]
            need(
                row["coarse_family"] == "G2B" and is_zero(predicate["right"])
                and digest(core) == graph["core_sha256"],
                "C24/C10 exact primitive factor core",
            )
            authority = row["semantic_theorem_ast"]["sealed_exact_support_authority"]
            role = authority["role"]
            need(role in c24_authority_ids, "known C24 authority role")
            c24_authority_ids[role].add(authority["row_id"])
            c24[row["row_sha256"]] = {
                "authority": authority,
                "factor_core": graph["core"],
                "factor_core_sha256": graph["core_sha256"],
                "graph_class": graph["graph_class"],
                "graph_id": row["graph_id"],
                "member_id": row["member_id"],
                "normalized_support_ast_sha256": row["normalized_support_ast_sha256"],
                "official_key_id": row["official_key_id"],
                "predicate_op": predicate["op"],
                "predicate_sha256": digest(predicate),
                "predicate_unit_sign": unit,
                "role": role,
                "row_sha256": row["row_sha256"],
            }
        need(set(c24) == c24_needed, "all candidate C24 rows joined")

        c22: dict[str, dict[str, Any]] = {}
        for row in captures[C22A].rows():
            if row["row_sha256"] in c22_needed:
                c22[row["row_sha256"]] = {
                    "member_id": row["owner_member_id"],
                    "row_sha256": row["row_sha256"],
                    "source_bindings": row["source_bindings"],
                    "support_ast": row["support_ast"],
                    "theorem_ast": row["theorem_ast"],
                    "theorem_ast_sha256": row["theorem_ast_sha256"],
                }
        need(set(c22) == c22_needed, "all candidate C22 rows joined")

        c15: dict[str, dict[str, Any]] = {}
        for row in captures[C15].rows():
            member = row["registry_member_id"]
            if member in member_needed:
                c15[member] = {
                    "component_id": row["fresh_component_id"],
                    "official_key_id": row["official_key_id"],
                    "row_sha256": row["row_sha256"],
                }
        need(set(c15) == member_needed, "all candidate C15 members joined")

        c11a: dict[str, dict[str, Any]] = {}
        for row in captures[C11A].rows():
            if row["row_id"] in c24_authority_ids["C11A"]:
                need(digest(row["exact_side_stratum_ast"]) == row["exact_side_stratum_ast_sha256"],
                     "C11A support AST closure")
                c11a[row["row_id"]] = row
        need(set(c11a) == c24_authority_ids["C11A"], "C11A authority totality")

        c11br: dict[str, dict[str, Any]] = {}
        interface_needed: set[str] = set()
        for row in captures[C11BR].rows():
            if row["row_id"] in c24_authority_ids["C11B"]:
                need(digest(row["exact_side_carrier_ast"])
                     == row["ast_sha256"]["exact_side_carrier_ast"],
                     "C11B side AST closure")
                c11br[row["row_id"]] = row
                interface_needed.add(row["interface_kernel_ref"]["row_id"])
        need(set(c11br) == c24_authority_ids["C11B"], "C11B relation authority totality")
        c11bi = {
            row["row_id"]: row for row in captures[C11BI].rows()
            if row["row_id"] in interface_needed
        }
        need(set(c11bi) == interface_needed, "C11B interface authority totality")

        c12a: dict[str, dict[str, Any]] = {}
        for row in captures[C12A].rows():
            if row["row_id"] in c24_authority_ids["C12A"]:
                need(digest(row["exact_side_stratum_ast"]) == row["exact_side_stratum_ast_sha256"],
                     "C12A support AST closure")
                c12a[row["row_id"]] = row
        need(set(c12a) == c24_authority_ids["C12A"], "C12A authority totality")

        output: list[dict[str, Any]] = []
        disposition_census: Counter[str] = Counter()
        role_disposition: Counter[str] = Counter()
        validation_disposition: Counter[str] = Counter()
        component_disposition: Counter[str] = Counter()
        identity_disposition: Counter[str] = Counter()

        for candidate in candidates:
            source = c24[candidate["c24_row_sha256"]]
            target = c22[candidate["target_row_sha256"]]
            theorem = target["theorem_ast"]
            authority = theorem["sealed_source_authority"]
            role = source["role"]
            required = 1 if source["predicate_op"] == "GT" else -1
            c24_member = source["member_id"]
            target_member = target["member_id"]
            need(
                candidate["target_source"] == "C22A"
                and candidate["c24_member_id"] == c24_member
                and candidate["target_member_id"] == target_member
                and candidate["physical_chart"] == target["support_ast"]["coordinate_chart"]
                and candidate["c24_predicate_op"] == source["predicate_op"]
                and candidate["c24_predicate_ast_sha256"]
                    == source["predicate_sha256"],
                "candidate exact row binding",
            )
            # The candidate ledger's predicate hash was checked against C24 by
            # the predecessor.  Here the C24 row and authority hashes are
            # independently rejoined and materialized below.
            need(
                c15[c24_member]["component_id"] == candidate["c24_C15_component_id"]
                and c15[target_member]["component_id"] == candidate["target_C15_component_id"]
                and c15[c24_member]["official_key_id"] == source["official_key_id"]
                and candidate["current_C15_components_equal"]
                    == (c15[c24_member]["component_id"] == c15[target_member]["component_id"]),
                "candidate C15 binding",
            )

            authority_row_sha: str
            interface_row_sha: str | None = None
            primitive_reason: str
            target_core_sign: int
            target_product_sign: str | None = None

            if role == "C11A":
                row = c11a[source["authority"]["row_id"]]
                need(
                    row["row_sha256"] == source["authority"]["row_sha256"]
                    and row["graph_id"] == source["graph_id"]
                    and row["side_member_id"] == c24_member
                    and row["exact_side_stratum_ast_sha256"]
                        == source["normalized_support_ast_sha256"]
                        == source["authority"]["support_ast_sha256"]
                    and row["R248_side_member_identity"]["official_key_id"]
                        == source["official_key_id"],
                    "C11A/C24 exact authority binding",
                )
                wall_authority_closed(authority, theorem)
                partition = row["partition_semantic_ref"]
                if partition["kind"] == "R235_SINGLE_ENDPOINT_GRAPH_PARTITION_ROW":
                    event = partition["transition_event"]
                    axis, position = event[0][0], str(event[1])
                    primitive_reason = f"wall_endpoint_or_count_transition:{axis}:{position}"
                    need(
                        authority["reason_label"] == primitive_reason
                        and authority["equation"]
                            == f"(source_{axis.lower()}-{position})*(target_{axis.lower()}-{position})=0",
                        "C11A R235 primitive factor identity",
                    )
                    active = partition["active_endpoint_factor"]
                    fixed = "target" if active == "source" else "source"
                    target_core_sign = sign(authority[f"witness_{active}_factor_sign"])
                    need(
                        source["predicate_unit_sign"] == row["fixed_other_endpoint_eta"]
                            == sign(partition["fixed_endpoint_factor_sign"])
                        and sign(authority[f"witness_{fixed}_factor_sign"])
                            == sign(partition["fixed_endpoint_factor_sign"]),
                        "C11A R235 fixed primitive factor sign identity",
                    )
                    primitive_reason = "C11A_R235_ACTIVE_" + active.upper() + "|" + primitive_reason
                else:
                    need(
                        partition["kind"] == "R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE"
                        and partition["active_endpoint_factor"] == "source",
                        "C11A R235D partition",
                    )
                    primitive_reason = source_t_identity(authority)
                    target_core_sign = simple_t_factor_sign(
                        source["factor_core"], target["support_ast"]["bounds"]
                    )
                    need(
                        target_core_sign == sign(authority["witness_source_factor_sign"])
                        and source["predicate_unit_sign"] == row["fixed_other_endpoint_eta"]
                            == sign(partition["fixed_target_factor_sign"])
                        and sign(authority["witness_target_factor_sign"])
                            == sign(partition["fixed_target_factor_sign"]),
                        "C11A R235D primitive factor signs",
                    )
                    primitive_reason = "C11A_R235D_EXACT_SOURCE_9_OVER_25_TIMES_T|" + primitive_reason
                target_product_sign = authority["region_product_sign"]
                need(required == sign(row["desired_eta_times_active_factor_sign"]),
                     "C11A predicate desired sign")
                authority_row_sha = row["row_sha256"]

            elif role == "C11B":
                row = c11br[source["authority"]["row_id"]]
                interface = c11bi[row["interface_kernel_ref"]["row_id"]]
                need(
                    row["row_sha256"] == source["authority"]["row_sha256"]
                    and row["graph_id"] == source["graph_id"]
                    and row["side_member_id"] == c24_member
                    and row["ast_sha256"]["exact_side_carrier_ast"]
                        == source["normalized_support_ast_sha256"]
                        == source["authority"]["support_ast_sha256"]
                    and row["collar_receipt"]["witness_corridor_signature"]["official_key_id"]
                        == source["official_key_id"]
                    and interface["row_sha256"] == row["interface_kernel_ref"]["row_sha256"]
                    and interface["graph_id"] == source["graph_id"],
                    "C11B/C24 exact authority binding",
                )
                need(
                    theorem["case_kind"] == "DIRECT_WHOLE_OPEN_LEAF"
                    and authority["kind"] == "DIRECT_WHOLE_OPEN_LEAF_FACTOR_SIGN_AUTHORITY",
                    "C11B direct theorem kind",
                )
                product_atoms = [
                    atom for atom in theorem["source_predicate_ast"]["atoms"]
                    if atom.get("factor") == "HPLUS_TIMES_HMINUS"
                ]
                need(
                    len(product_atoms) == 1
                    and product_atoms[0]["sign"] == authority["region_factor_sign"]
                    and sign(authority["region_factor_sign"])
                        == sign(authority["HPLUS_sign"]) * sign(authority["HMINUS_sign"]),
                    "C11B F equals HPLUS times HMINUS identity",
                )
                target_core_sign = sign(authority["region_factor_sign"])
                side_sign = row["one_sided_direction_receipt"]["factor_sign_on_side"]
                need(
                    source["predicate_unit_sign"] == 1 and sign(side_sign) == required
                    and side_sign
                        == row["one_sided_direction_receipt"]["corresponding_carrier_face_sign"],
                    "C11B side factor sign",
                )
                primitive_reason = "C11B_F_EQUALS_HPLUS_TIMES_HMINUS"
                authority_row_sha = row["row_sha256"]
                interface_row_sha = interface["row_sha256"]

            else:
                need(role == "C12A", "C12A role")
                row = c12a[source["authority"]["row_id"]]
                need(
                    row["row_sha256"] == source["authority"]["row_sha256"]
                    and row["graph_id"] == source["graph_id"]
                    and row["side_member_id"] == c24_member
                    and row["exact_side_stratum_ast_sha256"]
                        == source["normalized_support_ast_sha256"]
                        == source["authority"]["support_ast_sha256"]
                    and row["R248_side_member_identity"]["official_key_id"]
                        == source["official_key_id"],
                    "C12A/C24 exact authority binding",
                )
                wall_authority_closed(authority, theorem)
                primitive_reason = source_t_identity(authority)
                target_core_sign = simple_t_factor_sign(
                    source["factor_core"], target["support_ast"]["bounds"]
                )
                partition = row["partition_semantic_ref"]
                need(
                    partition["active_endpoint_factor"] == "source"
                    and target_core_sign == sign(authority["witness_source_factor_sign"])
                    and source["predicate_unit_sign"] == row["fixed_other_endpoint_eta"]
                        == sign(partition["fixed_target_factor_sign"])
                    and sign(authority["witness_target_factor_sign"])
                        == sign(partition["fixed_target_factor_sign"])
                    and required == sign(row["desired_eta_times_active_factor_sign"]),
                    "C12A primitive factor signs",
                )
                target_product_sign = authority["region_product_sign"]
                primitive_reason = "C12A_EXACT_SOURCE_9_OVER_25_TIMES_T|" + primitive_reason
                authority_row_sha = row["row_sha256"]

            actual = source["predicate_unit_sign"] * target_core_sign
            disposition = "EXACT_POSITIVE_SUPPORT" if actual == required else "EXACT_EMPTY_INTERSECTION"
            if target_product_sign is not None:
                need(
                    (disposition == "EXACT_POSITIVE_SUPPORT")
                        == (sign(target_product_sign) == required),
                    "direct product-sign disposition equality",
                )
            disposition_census[disposition] += 1
            role_disposition[role + "|" + disposition] += 1
            validation_disposition[
                ("R300C" if candidate["R300C_validation_pair"] else "NON_R300C")
                + "|" + disposition
            ] += 1
            component_disposition[
                ("SAME_C15" if candidate["current_C15_components_equal"] else "CROSS_C15")
                + "|" + disposition
            ] += 1
            identity_disposition[primitive_reason + "|" + disposition] += 1

            output.append(closed({
                "C10_exact_graph_support_row_sha256": c10[source["graph_id"]]["row_sha256"],
                "C11_or_C12_authority_role": role,
                "C11_or_C12_authority_row_sha256": authority_row_sha,
                "C11B_interface_row_sha256": interface_row_sha,
                "C15_c24_member_row_sha256": c15[c24_member]["row_sha256"],
                "C15_target_member_row_sha256": c15[target_member]["row_sha256"],
                "C22_target_row_sha256": target["row_sha256"],
                "C22_target_theorem_ast_sha256": target["theorem_ast_sha256"],
                "C24_row_sha256": source["row_sha256"],
                "R300C_validation_pair": candidate["R300C_validation_pair"],
                "c24_member_id": c24_member,
                "candidate_ledger_row_sha256": candidate["row_sha256"],
                "current_C15_components": [
                    c15[c24_member]["component_id"], c15[target_member]["component_id"]
                ],
                "current_C15_components_equal": candidate["current_C15_components_equal"],
                "disposition": disposition,
                "exact_envelope_intersection_box": candidate["exact_envelope_intersection_box"],
                "factor_core_sha256": source["factor_core_sha256"],
                "factor_identity_route": primitive_reason,
                "factor_sign_on_target_open_box": sign_name(target_core_sign),
                "formal_credit": 0,
                "physical_chart": candidate["physical_chart"],
                "predicate_op": source["predicate_op"],
                "predicate_required_sign": sign_name(required),
                "predicate_unit_sign": source["predicate_unit_sign"],
                "signed_factor_value_on_target_open_box": sign_name(actual),
                "target_member_id": target_member,
                "target_region_product_sign": target_product_sign,
            }))

        need(
            disposition_census == {
                "EXACT_POSITIVE_SUPPORT": 9_408,
                "EXACT_EMPTY_INTERSECTION": 9_392,
            }
            and role_disposition == {
                "C11A|EXACT_POSITIVE_SUPPORT": 8_870,
                "C11A|EXACT_EMPTY_INTERSECTION": 8_864,
                "C11B|EXACT_POSITIVE_SUPPORT": 528,
                "C11B|EXACT_EMPTY_INTERSECTION": 528,
                "C12A|EXACT_POSITIVE_SUPPORT": 10,
            }
            and validation_disposition == {
                "R300C|EXACT_POSITIVE_SUPPORT": 906,
                "NON_R300C|EXACT_POSITIVE_SUPPORT": 8_502,
                "NON_R300C|EXACT_EMPTY_INTERSECTION": 9_392,
            }
            and component_disposition == {
                "SAME_C15|EXACT_POSITIVE_SUPPORT": 8_812,
                "SAME_C15|EXACT_EMPTY_INTERSECTION": 8_796,
                "CROSS_C15|EXACT_POSITIVE_SUPPORT": 596,
                "CROSS_C15|EXACT_EMPTY_INTERSECTION": 596,
            },
            "exact disposition acceptance census",
        )

        output.sort(key=lambda row: (row["c24_member_id"], row["target_member_id"]))
        ledger_path = out / "C24A_G2B_18800_exact_factor_sign_disposition.jsonl.gz"
        ledger_file_sha, ledger_sequence_sha, ledger_count = write_rows(ledger_path, output)
        need(ledger_count == 18_800, "output ledger count")

        attestations = {
            label: capture.attestation() for label, capture in sorted(captures.items())
        }
        body = {
            "schema": "cm2.c27-independent.c24a-g2b-exact-factor-sign-disposition.v1",
            "status": "PASS_DIAGNOSTIC_18800_EXACT_FACTOR_SIGN_DISPOSITIONS__9408_POSITIVE__9392_EMPTY__596_CROSS_COMPONENT_WITNESSES__ZERO_CREDIT",
            "invocation_seed": args.seed,
            "candidate_pair_count": 18_800,
            "disposition_census": dict(sorted(disposition_census.items())),
            "authority_role_disposition_census": dict(sorted(role_disposition.items())),
            "R300C_validation_disposition_census": dict(sorted(validation_disposition.items())),
            "current_C15_component_disposition_census": dict(sorted(component_disposition.items())),
            "factor_identity_disposition_census": dict(sorted(identity_disposition.items())),
            "exact_factor_core_C24_to_C10_gap": 0,
            "unresolved_candidate_count": 0,
            "C27_C28_C29": "FULL_REBUILD_REQUIRED__596_C24A_G2B_CROSS_CURRENT_C15_COMPONENT_POSITIVE_WITNESSES",
            "formal_credit": 0,
            "ledger": {
                "filename": ledger_path.name,
                "row_count": ledger_count,
                "file_sha256": ledger_file_sha,
                "row_sequence_sha256": ledger_sequence_sha,
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": attestations,
            },
            "hard_blockers": [
                "SIGNED_AND_COMPLETE_PRIORITY_JOIN_FOR_9408_POSITIVE_PAIRS_NOT_YET_MATERIALIZED",
                "596_CROSS_MEMBER_PAIRS_NOT_YET_DEDUPLICATED_TO_COMPONENT_EDGES_OR_COMPARED_WITH_C27R1D",
                "C24A_G2A_5264_RELATIVE_2D_ROUTE_OPEN",
                "INDEPENDENT_SECOND_IMPLEMENTATION_DOUBLE_SEED_AND_COHERENT_ATTACKS_OPEN",
            ],
            "strict_nonpromotion": {
                "C27_transition_totality": 0,
                "C28_pair_routing": 0,
                "C29_physical_maximality": 0,
                "manifest_authorized": False,
                "CM2": "NO-GO_FOR_CLAIM",
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items()
            if key not in {"invocation_seed", "root_input_capture"}
        })
        result["result_sha256"] = digest(result)
        (out / "result.json").write_bytes(canonical(result) + b"\n")
        return result
    finally:
        for capture in captures.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--candidate-ledger", required=True)
    parser.add_argument("--candidate-ledger-sha256", required=True)
    parser.add_argument("--predecessor-result", required=True)
    parser.add_argument("--predecessor-result-sha256", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = build(args)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        "semantic_projection_sha256": result["semantic_projection_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
