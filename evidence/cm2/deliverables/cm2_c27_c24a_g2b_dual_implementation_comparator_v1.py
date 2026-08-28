#!/usr/bin/env python3
"""Fail-closed comparator for the two independent C24A G2B classifiers.

This is a diagnostic, zero-credit comparator.  It also binds the independent
SIGNED/COMPLETE priority and C27R1D component-edge diagnostic ledgers.  Root
inputs are hashed, parsed, and post-fstat checked through one O_NOFOLLOW file
description each.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


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


def check_closed(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":row closure")


def check_result(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":result closure")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON object key:" + key)
        output[key] = value
    return output


def fp(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    expected: str
    fd: int
    pre: tuple[int, ...]
    observed: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":file pin")
            need(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, path, expected, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def rows(self) -> list[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        output: list[dict[str, Any]] = []
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:newline:{ordinal}")
                    encoded = line[:-1]
                    row = json.loads(encoded)
                    need(type(row) is dict and canonical(row) == encoded,
                         f"{self.label}:canonical:{ordinal}")
                    check_closed(row, f"{self.label}:{ordinal}")
                    output.append(row)
        self.unchanged("parse")
        return output

    def document(self) -> dict[str, Any]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        encoded = b"".join(pieces)
        row = json.loads(encoded, object_pairs_hook=unique_object)
        need(type(row) is dict, self.label + ":JSON object document")
        check_result(row, self.label)
        self.unchanged("parse")
        return row

    def unchanged(self, phase: str) -> None:
        need(fp(os.fstat(self.fd)) == self.pre, self.label + ":" + phase + ":fstat")

    def attestation(self) -> dict[str, Any]:
        self.unchanged("final")
        return {"filename": self.path.name, "observed_sha256": self.observed,
                "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True,
                "stat_fingerprint": list(self.pre)}

    def close(self) -> None:
        os.close(self.fd)


def ordered(left: str, right: str) -> tuple[str, str]:
    need(type(left) is str and type(right) is str and left != right, "nonself pair")
    return (left, right) if left < right else (right, left)


def semantic_compare(
    primary: list[dict[str, Any]], secondary: list[dict[str, Any]],
    priority: list[dict[str, Any]], cross: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    for label, rows in (("primary", primary), ("secondary", secondary),
                        ("priority", priority), ("cross", cross), ("edges", edges)):
        for ordinal, row in enumerate(rows):
            check_closed(row, f"{label}:{ordinal}")

    p: dict[str, dict[str, Any]] = {}
    for row in primary:
        key = row["candidate_ledger_row_sha256"]
        need(key not in p, "primary duplicate pair authority")
        p[key] = row
    s: dict[str, dict[str, Any]] = {}
    for row in secondary:
        key = row["pair_row_sha256"]
        need(key not in s, "secondary duplicate pair authority")
        s[key] = row
    need(len(p) == len(s) == 18_800 and set(p) == set(s), "dual pair-key totality")

    disposition = {"EXACT_POSITIVE_SUPPORT": "SUPPORT_POSITIVE",
                   "EXACT_EMPTY_INTERSECTION": "SUPPORT_EMPTY"}
    mismatch = Counter()
    positive: dict[tuple[str, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    cross_positive: dict[tuple[str, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for key in sorted(p):
        a, b = p[key], s[key]
        expected_target_sign = (a["target_region_product_sign"]
                                if a["target_region_product_sign"] is not None
                                else a["factor_sign_on_target_open_box"])
        checks = {
            "row_binding": (a["C24_row_sha256"], a["C22_target_row_sha256"])
                           == (b["c24_row_sha256"], b["target_row_sha256"]),
            "member_binding": (a["c24_member_id"], a["target_member_id"])
                              == (b["c24_member_id"], b["target_member_id"]),
            "authority_role": a["C11_or_C12_authority_role"] == b["authority_role"],
            "component_equality": a["current_C15_components_equal"]
                                  == b["current_C15_components_equal"],
            "R300C_validation_flag": a["R300C_validation_pair"]
                == b["R300C_validation_pair_not_used_as_universe_or_classifier"],
            "disposition": disposition.get(a["disposition"]) == b["disposition"],
            "source_required_sign": a["predicate_required_sign"] == b["c24_side_sign"],
            "target_whole_box_sign": expected_target_sign == b["target_whole_box_sign"],
            "zero_credit": a["formal_credit"] == b["formal_credit"] == 0,
        }
        for label, passed in checks.items():
            if not passed:
                mismatch[label] += 1
        need(all(checks.values()), "dual semantic mismatch:" + key)
        if b["disposition"] == "SUPPORT_POSITIVE":
            pair = ordered(a["c24_member_id"], a["target_member_id"])
            need(pair not in positive, "duplicate positive member pair")
            positive[pair] = (a, b)
            if a["current_C15_components_equal"] is False:
                cross_positive[pair] = (a, b)
    need(len(positive) == 9_408 and len(cross_positive) == 596, "positive census")

    pri: dict[tuple[str, str], dict[str, Any]] = {}
    for row in priority:
        pair = ordered(row["left_member_id"], row["right_member_id"])
        need(pair not in pri, "priority duplicate pair")
        pri[pair] = row
    need(set(pri) == set(positive), "priority exact positive set")
    for pair, row in pri.items():
        _, b = positive[pair]
        need(row["raw_signed_exact_pair"] is False
             and row["raw_complete_exact_pair"] is False
             and row["assigned_terminal"] == "C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE"
             and row["priority_rule"]
                 == "SIGNED_THEN_COMPLETE_THEN_C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE"
             and row["source_C24A_C22A_disposition_row_sha256"] == b["row_sha256"]
             and row["formal_credit"] == 0,
             "priority row exact binding")

    cr: dict[tuple[str, str], dict[str, Any]] = {}
    derived_edges: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for row in cross:
        pair = ordered(row["left_member_id"], row["right_member_id"])
        need(pair not in cr, "cross duplicate member pair")
        cr[pair] = row
    need(set(cr) == set(cross_positive), "cross exact member set")
    for pair, row in cr.items():
        a, b = cross_positive[pair]
        component_pair = ordered(*a["current_C15_components"])
        need(tuple(row["ordered_C15_component_pair"]) == component_pair
             and row["source_C24A_C22A_disposition_row_sha256"] == b["row_sha256"]
             and row["formal_credit"] == 0,
             "cross member-to-component exact binding")
        derived_edges.setdefault(component_pair, []).append(pair)

    er: dict[tuple[str, str], dict[str, Any]] = {}
    for row in edges:
        edge = tuple(row["ordered_C15_component_pair"])
        need(len(edge) == 2 and edge[0] < edge[1] and edge not in er,
             "unique ordered component edge")
        er[edge] = row
    need(len(er) == len(derived_edges) == 144 and set(er) == set(derived_edges),
         "component edge exact set")
    for edge, row in er.items():
        sources = sorted(derived_edges[edge])
        need(row["source_member_pair_count"] == len(sources)
             and row["source_member_pairs"] == [list(pair) for pair in sources]
             and row["overlaps_C27R1D_strict_volume_edge"] is True
             and row["formal_credit"] == 0,
             "component edge source/overlap binding")

    return {
        "dual_pair_count": len(p),
        "dual_semantic_mismatch_census": dict(mismatch),
        "positive_pair_count": len(positive),
        "priority_SIGNED_intersection": sum(row["raw_signed_exact_pair"] for row in priority),
        "priority_COMPLETE_intersection": sum(row["raw_complete_exact_pair"] for row in priority),
        "cross_positive_member_pair_count": len(cross_positive),
        "unique_component_edge_count": len(derived_edges),
        "distinct_component_vertex_count": len({v for edge in derived_edges for v in edge}),
        "C27R1D_overlap_edge_count": sum(row["overlaps_C27R1D_strict_volume_edge"] for row in edges),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    specs = {
        "primary_ledger": (Path(args.primary_ledger), args.primary_ledger_sha256, "rows"),
        "primary_result": (Path(args.primary_result), args.primary_result_sha256, "document"),
        "secondary_ledger": (Path(args.secondary_ledger), args.secondary_ledger_sha256, "rows"),
        "secondary_result": (Path(args.secondary_result), args.secondary_result_sha256, "document"),
        "priority_ledger": (Path(args.priority_ledger), args.priority_ledger_sha256, "rows"),
        "cross_ledger": (Path(args.cross_ledger), args.cross_ledger_sha256, "rows"),
        "edge_ledger": (Path(args.edge_ledger), args.edge_ledger_sha256, "rows"),
        "priority_result": (Path(args.priority_result), args.priority_result_sha256, "document"),
    }
    captures: dict[str, Capture] = {}
    try:
        parsed: dict[str, Any] = {}
        for label, (path, sha, kind) in specs.items():
            captures[label] = Capture.open(label, path, sha)
            parsed[label] = (captures[label].rows() if kind == "rows"
                             else captures[label].document())
        pr, sr, rr = parsed["primary_result"], parsed["secondary_result"], parsed["priority_result"]
        need(pr["status"].startswith("PASS_DIAGNOSTIC_18800_EXACT_FACTOR_SIGN_DISPOSITIONS")
             and pr["formal_credit"] == 0
             and pr["ledger"]["file_sha256"] == args.primary_ledger_sha256,
             "primary result authority")
        need(sr["status"] == "PASS_EXACT_FACTOR_SIGN_DISPOSITION_ZERO_UNRESOLVED"
             and sr["strict_scope"]["formal_credit"] == 0
             and sr["ledger"]["sha256"] == args.secondary_ledger_sha256,
             "secondary result authority")
        need(rr["status"] in {
                 "PASS_EXACT_SET_INTERSECTIONS_AND_PROVISIONAL_RANK_DIAGNOSTIC_ZERO_CREDIT",
                 "PASS_EXACT_SET_INTERSECTIONS_AND_PROVISIONAL_RANK_DIAGNOSTIC_CLOSURE_VALID_V2_ZERO_CREDIT",
             }
             and rr["strict_scope"]["formal_credit"] == 0
             and rr["raw_exact_pair_sets"]["SIGNED_pair_count"] == 25_452
             and rr["raw_exact_pair_sets"]["COMPLETE_pair_count"] == 36_140
             and rr["raw_exact_pair_sets"]["SIGNED_is_subset_of_COMPLETE"] is True
             and rr["raw_exact_pair_sets"]["C24A_positive_intersection_SIGNED"] == 0
             and rr["raw_exact_pair_sets"]["C24A_positive_intersection_COMPLETE"] == 0
             and rr["raw_exact_pair_sets"]["C24A_positive_novel_against_SIGNED_union_COMPLETE"] == 9_408
             and rr["C27R1D_comparison"]["candidate_component_edge_overlap_count"] == 144
             and rr["C27R1D_comparison"]["candidate_component_edge_novel_count"] == 0
             and rr["C27R1D_comparison"]["candidate_incremental_rank_reduction_after_C27R1D"] == 0
             and rr["C27R1D_comparison"]["union_provisional_component_count"] == 43_772,
             "priority/rank result authority")

        summary = semantic_compare(parsed["primary_ledger"], parsed["secondary_ledger"],
                                   parsed["priority_ledger"], parsed["cross_ledger"],
                                   parsed["edge_ledger"])
        need(summary == {
            "dual_pair_count": 18_800,
            "dual_semantic_mismatch_census": {},
            "positive_pair_count": 9_408,
            "priority_SIGNED_intersection": 0,
            "priority_COMPLETE_intersection": 0,
            "cross_positive_member_pair_count": 596,
            "unique_component_edge_count": 144,
            "distinct_component_vertex_count": 216,
            "C27R1D_overlap_edge_count": 144,
        }, "exact comparator acceptance census")

        body = {
            "schema": "cm2.c27-independent.c24a-g2b-dual-implementation-comparator.v1",
            "status": "PASS_DUAL_IMPLEMENTATION_18800_EXACT__9408_PRIORITY_NOVEL__596_TO_144_ALL_C27R1D_OVERLAP__ZERO_CREDIT",
            "comparison": summary,
            "three_terminal_priority_union_count": 25_452 + (36_140 - 25_452) + 9_408,
            "component_rank_diagnostic": {
                "C24A_unique_component_edges": 144,
                "overlap_with_C27R1D_14772": 144,
                "novel_after_C27R1D": 0,
                "incremental_rank_reduction_after_C27R1D": 0,
                "provisional_component_count_remains": 43_772,
            },
            "C27_C28_C29": "FULL_REBUILD_REQUIRED__UNION_ALL_EXISTING_STRICT_VOLUME_AND_C19_WITNESSES_WITH_C24A_BRANCH__NO_PATCH_PROMOTION",
            "formal_credit": 0,
            "manifest_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())},
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items() if key != "root_input_capture"
        })
        result["result_sha256"] = digest(result)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=False)
        (out / "result.json").write_bytes(canonical(result) + b"\n")
        return result
    finally:
        for capture in captures.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in ("primary-ledger", "primary-result", "secondary-ledger", "secondary-result",
                 "priority-ledger", "cross-ledger", "edge-ledger", "priority-result"):
        parser.add_argument("--" + name, required=True)
        parser.add_argument("--" + name + "-sha256", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        result = run(args)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "semantic_projection_sha256": result["semantic_projection_sha256"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
