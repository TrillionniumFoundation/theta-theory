#!/usr/bin/env python3
"""Fail-closed C27R2 fresh-primitive rebuild preflight.

This program is deliberately not a C27 producer.  It checks whether the
fresh C27R2 producer has a complete, primitive-only input surface and, when
possible, computes only the old-C15 component-edge topology that the later
producer must replay.  It never reads a C27 FAMILIES table, a C27 transition
ledger, C28, C29, or an historical edge ledger as candidate authority.

Missing G2A or current-support terminal receipts are a truthful rejection,
not an exception and not evidence for a 43,772 component conclusion.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent

C15 = HERE / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
STRICT_RECEIPT = HERE / "cm2_c27_same_chart_strict_volume_totality_subgate_receipt.json"
STRICT_EDGES = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run3/candidate/cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz"
LOWER_RECEIPT = HERE / "cm2_c27_same_chart_lower_dimensional_exact_contact_v1_terminal_receipt.json"
G2B_RECEIPT = HERE / "cm2_c27_c24a_g2b_terminal_zero_credit_v1/terminal_zero_credit_receipt.json"
G2B_EDGES = WORKSPACE / ".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101/payload/C24A_cross_positive_unique_component_edges.jsonl.gz"

# These exact terminal interfaces are intentionally absent until their
# respective dual-verifier/attack/cold chains publish them.  A future receipt
# must expose a ``rebuild_input`` object as documented in FUTURE_CONTRACTS.
G2A_RECEIPT = HERE / "cm2_c27_g2a_relative2d_primitive_totality_v2_terminal_receipt.json"
CURRENT_RECEIPT = HERE / "cm2_c27_three_terminal_current_support_91672_v4_terminal_receipt.json"

FILE_PINS = {
    C15: (142_025_813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    STRICT_RECEIPT: (4_234, "22f8f8f6635a6083254311f5ee776e9ebe82b3192b0aadac6dc9585a0b0db3a4"),
    STRICT_EDGES: (2_157_061, "64cb62aa3b5ae298699ef5809e075ce6c2314baad1f589965e675c82deaa4632"),
    LOWER_RECEIPT: (5_247, "54da91e93d3248f931c9654ec002fc4fb5e43eca59cdefbd5586d727ae008b94"),
    G2B_RECEIPT: (15_964, "2e81e5084eb16f20d02865d0e90696f3a776673b8df0f727a7438703ce78549f"),
    G2B_EDGES: (48_188, "d922bbf6d8f487df1e826271b0d65d2d9765432f6d4a02919fe1157b94c117ef"),
}

FUTURE_CONTRACTS = {
    "G2A": {
        "path": str(G2A_RECEIPT.relative_to(WORKSPACE)),
        "schema": "cm2.c27-independent.g2a-relative2d-primitive-totality-terminal-receipt.v2",
        "required_census": {
            "primitive_graphs": 5_264,
            "relative2d_contact_alias_routes": 9_408,
            "cross_old_C15_member_witnesses": 596,
            "unique_old_C15_component_edges": 144,
            "unresolved": 0,
        },
        "required_rebuild_input": ["old_C15_component_edge_ledger"],
    },
    "CURRENT_SUPPORT_91672": {
        "path": str(CURRENT_RECEIPT.relative_to(WORKSPACE)),
        "schema": "cm2.c27-independent.current-support-91672-terminal-receipt.v4",
        "required_census": {
            "priority_pair_count": 91_672,
            "SIGNED_BOUNDARY_FACES": 25_452,
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 55_532,
            "unresolved": 0,
        },
        "required_rebuild_input": [
            "priority_route_ledger",
            "old_C15_component_edge_ledger",
        ],
    },
}

FORBIDDEN_DEPENDENCIES = [
    "OLD_C27_FAMILIES",
    "OLD_C27_TRANSITION_CANDIDATE_LEDGER",
    "OLD_C27_TRANSITION_FAMILY_COVERAGE_LEDGER",
    "OLD_C28_PAIR_ROUTING",
    "OLD_C29_PHYSICAL_MAXIMALITY",
    "HISTORICAL_EDGE_LEDGER_AS_CANDIDATE_UNIVERSE",
]


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


class Capture:
    def __init__(self, path: Path, expected: tuple[int, str] | None, label: str):
        self.path = path.resolve()
        self.label = label
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(self.fd)
        need(stat.S_ISREG(before.st_mode), label + ":regular")
        self.before = fingerprint(before)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        self.sha256 = state.hexdigest()
        need(fingerprint(os.fstat(self.fd)) == self.before, label + ":hash-fstat")
        if expected is not None:
            need(before.st_size == expected[0], label + ":size-pin")
            need(self.sha256 == expected[1], label + ":sha-pin")

    def unchanged(self, phase: str) -> None:
        need(fingerprint(os.fstat(self.fd)) == self.before,
             self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.unchanged("raw")
        return b"".join(pieces)

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as packed:
                for ordinal, line in enumerate(packed):
                    need(line.endswith(b"\n"), f"{self.label}:newline:{ordinal}")
                    payload = line[:-1]
                    row = json.loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
                         f"{self.label}:canonical:{ordinal}")
                    body = dict(row)
                    claimed = body.pop("row_sha256", None)
                    need(type(claimed) is str and claimed == digest(body),
                         f"{self.label}:row-closure:{ordinal}")
                    yield row
        self.unchanged("rows")

    def attestation(self) -> dict[str, Any]:
        self.unchanged("attestation")
        return {
            "path": str(self.path.relative_to(WORKSPACE)),
            "sha256": self.sha256,
            "size": self.before[2],
            "stat_fingerprint": list(self.before),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def object_from(cap: Capture, closure_field: str) -> dict[str, Any]:
    raw = cap.raw()
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(payload != b"" and b"\n" not in payload, cap.label + ":single-object")
    value = json.loads(payload)
    need(type(value) is dict and canonical(value) == payload, cap.label + ":canonical-object")
    body = dict(value)
    claimed = body.pop(closure_field, None)
    need(type(claimed) is str and claimed == digest(body), cap.label + ":object-closure")
    return value


class DSU:
    def __init__(self, values: set[str]):
        self.values = sorted(values)
        self.index = {value: ordinal for ordinal, value in enumerate(self.values)}
        self.parent = list(range(len(self.values)))
        self.size = [1] * len(self.values)

    def find(self, ordinal: int) -> int:
        while self.parent[ordinal] != ordinal:
            self.parent[ordinal] = self.parent[self.parent[ordinal]]
            ordinal = self.parent[ordinal]
        return ordinal

    def union(self, left: str, right: str) -> int:
        a, b = self.find(self.index[left]), self.find(self.index[right])
        if a == b:
            return 0
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b]
                                          and self.values[a] > self.values[b]):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return 1


def pair_from(row: dict[str, Any], field: str, components: set[str], label: str) -> tuple[str, str]:
    pair = row.get(field)
    need(type(pair) is list and len(pair) == 2 and pair == sorted(pair)
         and pair[0] != pair[1], label + ":ordered-nonself-pair")
    need(pair[0] in components and pair[1] in components, label + ":C15-bound")
    need(row.get("formal_credit") == 0, label + ":zero-credit-row")
    return pair[0], pair[1]


def future_terminal(path: Path, contract: dict[str, Any], components: set[str]) -> tuple[dict[str, Any], dict[str, Capture], set[tuple[str, str]]]:
    captures: dict[str, Capture] = {}
    cap = Capture(path, None, path.name)
    captures["receipt"] = cap
    value = object_from(cap, "receipt_sha256")
    need(value.get("schema") == contract["schema"], path.name + ":schema")
    need(type(value.get("status")) is str and value["status"].startswith("PASS_"), path.name + ":status")
    need(value.get("formal_credit") == 0 and value.get("manifest_authorized") is False,
         path.name + ":nonpromotion")
    need(value.get("census") == contract["required_census"], path.name + ":exact-census")
    rebuild = value.get("rebuild_input")
    need(type(rebuild) is dict, path.name + ":rebuild-input")
    for key in contract["required_rebuild_input"]:
        need(key in rebuild, path.name + ":missing-rebuild-input:" + key)
    edge = rebuild["old_C15_component_edge_ledger"]
    need(type(edge) is dict and set(edge) >= {"path", "sha256", "size", "row_count", "pair_field"},
         path.name + ":edge-contract")
    edge_path = (WORKSPACE / edge["path"]).resolve()
    need(edge_path.is_relative_to(WORKSPACE), path.name + ":edge-under-workspace")
    edge_cap = Capture(edge_path, (edge["size"], edge["sha256"]), path.name + ":edges")
    captures["edge_ledger"] = edge_cap
    pairs = set()
    for ordinal, row in enumerate(edge_cap.rows()):
        pair = pair_from(row, edge["pair_field"], components,
                         f"{path.name}:edge:{ordinal}")
        need(pair not in pairs, path.name + ":unique-edge")
        pairs.add(pair)
    need(len(pairs) == edge["row_count"], path.name + ":edge-row-count")
    return value, captures, pairs


def write_exclusive(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def build(output: Path) -> tuple[dict[str, Any], bool]:
    captures: dict[str, Capture] = {}
    errors: list[str] = []
    missing: list[str] = []
    future_pairs: dict[str, set[tuple[str, str]]] = {}
    future_attestations: dict[str, Any] = {}
    try:
        for label, path in (
            ("C15_members", C15), ("strict_receipt", STRICT_RECEIPT),
            ("strict_edges", STRICT_EDGES), ("lower_receipt", LOWER_RECEIPT),
            ("G2B_receipt", G2B_RECEIPT), ("G2B_edges", G2B_EDGES),
        ):
            captures[label] = Capture(path, FILE_PINS[path], label)

        c15_components: set[str] = set()
        members = 0
        for ordinal, row in enumerate(captures["C15_members"].rows()):
            need(row.get("schema") == "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1.member-component-row.v1", "C15:schema")
            need(row.get("member_ordinal") == ordinal, "C15:ordinal")
            c15_components.add(row["fresh_component_id"])
            members += 1
        need((members, len(c15_components)) == (502_204, 57_876), "C15:census")

        strict = object_from(captures["strict_receipt"], "receipt_sha256")
        need(strict.get("exact_census", {}).get("union_component_edge_count") == 14_772,
             "strict:edge-census")
        need(strict.get("formal_credit") == 0 and strict.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED",
             "strict:nonpromotion")
        need(strict.get("forbidden_inputs") == {
            "C27_or_FAMILIES_imported_or_read": False,
            "historical_edge_ledger_used": False,
            "older_same_chart_census_ledger_imported_or_read": False,
        }, "strict:forbidden-inputs")
        strict_pairs = set()
        for ordinal, row in enumerate(captures["strict_edges"].rows()):
            need(row.get("schema") == "cm2.c27.same-chart-strict-volume-totality.v1.component-edge-row.v1",
                 "strict:edge-schema")
            need(row.get("ordinal") == ordinal, "strict:edge-ordinal")
            pair = pair_from(row, "component_pair", c15_components, f"strict:{ordinal}")
            need(pair not in strict_pairs, "strict:unique-edge")
            strict_pairs.add(pair)
        need(len(strict_pairs) == 14_772, "strict:edge-count")

        lower = object_from(captures["lower_receipt"], "receipt_sha256")
        endpoint = lower.get("endpoint_dependent_C19C_x_C19C", {})
        need(lower.get("lower_dimensional_candidate_pair_count") == 5_783_708,
             "lower:denominator")
        need(endpoint.get("candidate_count") == 76_000
             and endpoint.get("legal_witness_count") == 0,
             "lower:zero-edge-closure")
        need(lower.get("formal_credit") == 0
             and lower.get("full_20_family_totality_authorized") is False,
             "lower:nonpromotion")

        g2b = object_from(captures["G2B_receipt"], "result_sha256")
        gc = g2b.get("G2B_closed_diagnostic", {})
        need(gc == {
            "candidate_pairs": 18_800,
            "cross_current_C15_positive_member_pairs": 596,
            "edges_already_in_C27R1D": 144,
            "exact_empty": 9_392,
            "exact_positive": 9_408,
            "incremental_rank_reduction_after_C27R1D": 0,
            "new_component_edges_after_C27R1D": 0,
            "unique_old_C15_component_edges": 144,
            "unresolved": 0,
        }, "G2B:exact-census")
        need(g2b.get("formal_state_unchanged", {}).get("formal_credit") == 0,
             "G2B:nonpromotion")
        g2b_pairs = set()
        for ordinal, row in enumerate(captures["G2B_edges"].rows()):
            need(row.get("schema") == "cm2.audit.c24a-cross-positive-unique-component-edge.row.v1",
                 "G2B:edge-schema")
            need(row.get("overlaps_C27R1D_strict_volume_edge") is True,
                 "G2B:strict-overlap-flag")
            pair = pair_from(row, "ordered_C15_component_pair", c15_components,
                             f"G2B:{ordinal}")
            need(pair not in g2b_pairs, "G2B:unique-edge")
            g2b_pairs.add(pair)
        need(len(g2b_pairs) == 144 and g2b_pairs <= strict_pairs,
             "G2B:144-subset-strict")

        for name, path in (("G2A", G2A_RECEIPT),
                           ("CURRENT_SUPPORT_91672", CURRENT_RECEIPT)):
            if not path.exists():
                missing.append(name + "_TERMINAL_RECEIPT")
                continue
            try:
                _, local_caps, pairs = future_terminal(
                    path, FUTURE_CONTRACTS[name], c15_components
                )
                future_pairs[name] = pairs
                future_attestations[name] = {
                    key: cap.attestation() for key, cap in sorted(local_caps.items())
                }
                for key, cap in local_caps.items():
                    captures[name + ":" + key] = cap
            except (Failure, KeyError, TypeError, ValueError, OSError) as error:
                errors.append(name + ":" + str(error))

        dsu = DSU(c15_components)
        strict_rank = sum(dsu.union(*pair) for pair in sorted(strict_pairs))
        need(strict_rank == 14_104, "strict:rank")
        g2b_incremental_rank = sum(dsu.union(*pair) for pair in sorted(g2b_pairs))
        need(g2b_incremental_rank == 0, "G2B:incremental-rank")
        incremental_rank: dict[str, int] = {}
        for name in ("G2A", "CURRENT_SUPPORT_91672"):
            if name in future_pairs:
                incremental_rank[name] = sum(
                    dsu.union(*pair) for pair in sorted(future_pairs[name])
                )
        known_rank = strict_rank + sum(incremental_rank.values())
        complete = not missing and not errors and len(future_pairs) == 2
        observed_components = 57_876 - known_rank
        component_conclusion = (
            str(observed_components) + "_PREFLIGHT_EDGE_UNION_ONLY__NOT_C27_AUTHORITY"
            if complete else
            "UNAUTHORIZED__43772_IS_STRICT_VOLUME_UPPER_BOUND_ONLY__FUTURE_EDGE_RANK_UNKNOWN"
        )

        body = {
            "schema": "cm2.round306c27r2.source-g-fresh-primitive-rebuild-preflight.v1",
            "status": (
                "PASS_INPUT_COMPLETE_FOR_FRESH_C27R2_PRODUCER__ZERO_CREDIT__NO_FORMAL_STATE_CHANGE"
                if complete else
                "REJECT_INCOMPLETE_FRESH_PRIMITIVE_INPUT_CONTRACT__ZERO_CREDIT__NO_FORMAL_STATE_CHANGE"
            ),
            "input_contract": {
                "frozen_C15_members": 502_204,
                "frozen_old_C15_components": 57_876,
                "strict_volume_component_edges": 14_772,
                "same_chart_lower_edge_contribution": 0,
                "G2B_unique_component_edges": 144,
                "G2B_edges_subset_of_strict_volume": True,
                "future_terminal_contracts": FUTURE_CONTRACTS,
            },
            "missing_required_authority": missing,
            "invalid_required_authority": errors,
            "edge_topology_preflight": {
                "strict_volume_rank": strict_rank,
                "strict_volume_component_count": 43_772,
                "G2B_incremental_rank_after_strict_volume": 0,
                "future_incremental_rank_if_present": incremental_rank,
                "current_preflight_union_rank": known_rank,
                "current_preflight_component_count": observed_components,
                "component_count_conclusion": component_conclusion,
                "may_assert_final_component_count_43772": False,
            },
            "forbidden_dependencies": FORBIDDEN_DEPENDENCIES,
            "forbidden_dependency_open_count": 0,
            "root_input_capture": {
                "known_authorities": {
                    key: captures[key].attestation()
                    for key in ("C15_members", "strict_receipt", "strict_edges",
                                "lower_receipt", "G2B_receipt", "G2B_edges")
                },
                "future_authorities_if_present": future_attestations,
                "all_opened_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
            },
            "producer_authorization": complete,
            "C27_transition_totality": "UNAUTHORIZED",
            "C28_pair_routing": "UNAUTHORIZED",
            "C29_physical_maximality": "UNAUTHORIZED",
            "formal_credit": 0,
            "manifest_authorized": False,
            "Source_W_transition_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = dict(body)
        result["preflight_sha256"] = digest(body)
        write_exclusive(output, result)
        return result, complete
    finally:
        seen = set()
        for cap in captures.values():
            if id(cap) not in seen:
                seen.add(id(cap))
                cap.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result, complete = build(Path(args.output))
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "preflight_sha256": result["preflight_sha256"]}).decode("ascii"))
    return 0 if complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
