#!/usr/bin/env python3
"""Coherently re-signed mutation attacks for the C19C v3 authority."""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


PREFIX = "cm2_c19c_endpoint_ownership_v3"
FILES = {
    "authority": PREFIX + "_authority_ledger.jsonl.gz",
    "face_atoms": PREFIX + "_face_atom_ledger.jsonl.gz",
    "junction_1d": PREFIX + "_codimension1_in_face_junction_1d_ledger.jsonl.gz",
    "junction_0d": PREFIX + "_codimension2_in_face_junction_0d_ledger.jsonl.gz",
    "C19C_additive_replay": PREFIX + "_c19c_additive_replay_ledger.jsonl.gz",
    "C25_additive_replay": PREFIX + "_c25_additive_replay_ledger.jsonl.gz",
    "C26_additive_replay": PREFIX + "_c26_additive_replay_ledger.jsonl.gz",
}
RESULT = PREFIX + "_result.json"
FACES = ("t_lower", "t_upper", "p_lower", "p_upper", "s_lower", "s_upper")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        return [json.loads(line) for line in handle]


def resign_row(row: dict[str, Any]) -> None:
    body = dict(row)
    body.pop("row_sha256", None)
    row["row_sha256"] = objsha(body)


def write_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    for row in rows:
        resign_row(row)
    raw = b"".join(canonical(row) + b"\n" for row in rows)
    with path.open("wb") as raw_handle:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_handle, mtime=0) as handle:
            handle.write(raw)
    return {
        "filename": path.name,
        "row_count": len(rows),
        "sha256": filesha(path),
        "size": path.stat().st_size,
        "row_sequence_sha256": objsha([row["row_sha256"] for row in rows]),
    }


class Candidate:
    def __init__(self, path: Path):
        self.path = path
        self.result = json.loads((path / RESULT).read_bytes())
        self.cache: dict[str, list[dict[str, Any]]] = {}

    def rows(self, key: str) -> list[dict[str, Any]]:
        if key not in self.cache:
            self.cache[key] = read_rows(self.path / FILES[key])
        return self.cache[key]

    def write(self, key: str) -> None:
        self.result["ledgers"][key] = write_rows(self.path / FILES[key], self.rows(key))

    def authority_index(self, mid: str) -> int:
        return next(index for index, row in enumerate(self.rows("authority")) if row["member_id"] == mid)

    def cascade_authority(self, mid: str) -> None:
        authority = self.rows("authority")
        auth = authority[self.authority_index(mid)]
        resign_row(auth)
        self.write("authority")
        c19 = next(row for row in self.rows("C19C_additive_replay") if row["member_id"] == mid)
        c19["endpoint_authority_row_sha256"] = auth["row_sha256"]
        c19["support_ast"]["endpoint_authority_row_sha256"] = auth["row_sha256"]
        c19["support_ast_sha256"] = objsha(c19["support_ast"])
        resign_row(c19)
        self.write("C19C_additive_replay")
        c25 = next(row for row in self.rows("C25_additive_replay") if row["member_id"] == mid)
        c25["v3_C19C_replay_row_sha256"] = c19["row_sha256"]
        c25["v3_normalized_support_ast_sha256"] = c19["support_ast_sha256"]
        resign_row(c25)
        self.write("C25_additive_replay")
        c26 = next(row for row in self.rows("C26_additive_replay") if row["member_id"] == mid)
        c26["v3_C25_replay_row_sha256"] = c25["row_sha256"]
        c26["v3_owner_normalized_support_ast_sha256"] = c19["support_ast_sha256"]
        resign_row(c26)
        self.write("C26_additive_replay")

    def bind_face_group(self, mid: str, face: str) -> None:
        group = sorted(
            (row for row in self.rows("face_atoms") if row["member_id"] == mid and row["face"] == face),
            key=lambda row: row["face_atom_ordinal"],
        )
        auth = self.rows("authority")[self.authority_index(mid)]
        disposition = next(item for item in auth["face_dispositions"] if item["face"] == face)
        disposition["face_atom_count"] = len(group)
        disposition["face_atom_row_sequence_sha256"] = objsha([row["row_sha256"] for row in group])

    def bind_junction_group(self, mid: str, key: str) -> None:
        ordinal_key = "junction_1d_ordinal" if key == "junction_1d" else "junction_0d_ordinal"
        group = sorted((row for row in self.rows(key) if row["member_id"] == mid), key=lambda row: row[ordinal_key])
        auth = self.rows("authority")[self.authority_index(mid)]
        auth[key + "_count"] = len(group)
        auth[key + "_row_sequence_sha256"] = objsha([row["row_sha256"] for row in group])

    def finish(self) -> None:
        body = dict(self.result)
        body.pop("result_sha256", None)
        self.result["result_sha256"] = objsha(body)
        (self.path / RESULT).write_bytes(canonical(self.result))


def attack_direct_rule(c: Candidate) -> None:
    c.result["authority"]["direct_rule"] = "oriented (lower,upper] on internal faces"


def attack_axis_transport(c: Candidate) -> None:
    c.result["authority"]["transported_axis_signs"]["G:W"] = [1, 1, 1]


def attack_authority_bit(c: Candidate) -> None:
    auth = next(row for row in c.rows("authority") if not row["face_dispositions"][0]["physical_outer"])
    mid = auth["member_id"]
    auth["endpoint_inclusion_bits"]["t_lower_closed"] = not auth["endpoint_inclusion_bits"]["t_lower_closed"]
    auth["face_dispositions"][0]["closed"] = not auth["face_dispositions"][0]["closed"]
    c.cascade_authority(mid)


def attack_outer(c: Candidate) -> None:
    auth = next(row for row in c.rows("authority") if any(item["face"] == "s_upper" and item["physical_outer"] for item in row["face_dispositions"]))
    mid = auth["member_id"]
    face = next(item for item in auth["face_dispositions"] if item["face"] == "s_upper")
    face["physical_outer"] = False
    face["closed"] = False
    auth["endpoint_inclusion_bits"]["s_upper_closed"] = False
    c.cascade_authority(mid)


def first_internal_face(c: Candidate) -> tuple[str, str, list[dict[str, Any]]]:
    row = next(row for row in c.rows("face_atoms") if row["neighbor_terminal_id"] is not None)
    mid, face = row["member_id"], row["face"]
    group = [item for item in c.rows("face_atoms") if item["member_id"] == mid and item["face"] == face]
    return mid, face, group


def attack_face_neighbor(c: Candidate) -> None:
    mid, face, group = first_internal_face(c)
    row = group[0]
    auth = c.rows("authority")[c.authority_index(mid)]
    row["neighbor_terminal_id"] = auth["R234_frontier_row_id"]
    row["neighbor_disposition"] = "R234_FRONTIER"
    row["neighbor_box"] = auth["bounds"]
    resign_row(row)
    c.write("face_atoms")
    c.bind_face_group(mid, face)
    c.cascade_authority(mid)


def attack_face_delete(c: Candidate) -> None:
    rows = c.rows("face_atoms")
    seed = next(row for row in rows if row["face_atom_ordinal"] > 0)
    mid, face = seed["member_id"], seed["face"]
    rows.remove(seed)
    group = sorted((row for row in rows if row["member_id"] == mid and row["face"] == face), key=lambda row: row["face_atom_ordinal"])
    for ordinal, row in enumerate(group):
        row["face_atom_ordinal"] = ordinal
        resign_row(row)
    c.write("face_atoms")
    c.bind_face_group(mid, face)
    c.cascade_authority(mid)


def attack_face_duplicate(c: Candidate) -> None:
    rows = c.rows("face_atoms")
    seed = next(row for row in rows if row["neighbor_terminal_id"] is not None)
    mid, face = seed["member_id"], seed["face"]
    duplicate = json.loads(json.dumps(seed))
    group = [row for row in rows if row["member_id"] == mid and row["face"] == face]
    duplicate["face_atom_ordinal"] = len(group)
    resign_row(duplicate)
    rows.append(duplicate)
    rows.sort(key=lambda row: (row["member_ordinal"], FACES.index(row["face"]), row["face_atom_ordinal"]))
    c.write("face_atoms")
    c.bind_face_group(mid, face)
    c.cascade_authority(mid)


def attack_junction_owner(c: Candidate, key: str) -> None:
    rows = c.rows(key)
    row = next(row for row in rows if row["incident_terminal_count"] > 1)
    mid = row["member_id"]
    row["owner_terminal_id"] = next(value for value in row["incident_terminal_ids"] if value != row["owner_terminal_id"])
    row["owner_member_id_if_C19C"] = None
    resign_row(row)
    c.write(key)
    c.bind_junction_group(mid, key)
    c.cascade_authority(mid)


def attack_junction_delete(c: Candidate, key: str) -> None:
    rows = c.rows(key)
    row = rows[0]
    mid = row["member_id"]
    rows.remove(row)
    ordinal_key = "junction_1d_ordinal" if key == "junction_1d" else "junction_0d_ordinal"
    group = sorted((item for item in rows if item["member_id"] == mid), key=lambda item: item[ordinal_key])
    for ordinal, item in enumerate(group):
        item[ordinal_key] = ordinal
        resign_row(item)
    c.write(key)
    c.bind_junction_group(mid, key)
    c.cascade_authority(mid)


def attack_c26_promotion(c: Candidate) -> None:
    row = c.rows("C26_additive_replay")[0]
    row["transition_theorem_claimed"] = True
    c.write("C26_additive_replay")


ATTACKS: list[tuple[str, Callable[[Candidate], None], tuple[str, ...]]] = [
    ("direct_rule_flip", attack_direct_rule, ("direct owner rule",)),
    ("Jx_axis_transport_flip", attack_axis_transport, ("transported axis signs",)),
    ("authority_internal_bit_flip", attack_authority_bit, ("face bit", "six-bit vector")),
    ("closed_outer_override_removed", attack_outer, ("outer predicate",)),
    ("face_neighbor_rebound", attack_face_neighbor, ("unique geometric neighbor on atom", "neighbor binding")),
    ("face_atom_deleted", attack_face_delete, ("atom common refinement no gap/no overlap", "junction1 exact line coverage")),
    ("face_atom_duplicated", attack_face_duplicate, ("atom common refinement no gap/no overlap", "atom ordinals")),
    ("junction1_owner_flip", lambda c: attack_junction_owner(c, "junction_1d"), ("junction1 owner binding",)),
    ("junction1_segment_deleted", lambda c: attack_junction_delete(c, "junction_1d"), ("junction1 exact line coverage", "junction1 line-key completeness")),
    ("junction0_owner_flip", lambda c: attack_junction_owner(c, "junction_0d"), ("junction0 owner binding",)),
    ("junction0_point_deleted", lambda c: attack_junction_delete(c, "junction_0d"), ("junction0 all face-grid and T-break points",)),
    ("C26_transition_promotion", attack_c26_promotion, ("C26 replay",)),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed-base", type=int, required=True)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()
    verifier = Path(args.verifier).resolve()
    work = Path(args.work_dir).resolve()
    work.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="c19c-v3-attacks-", dir=work))
    attack_dirs: list[tuple[int, str, Path, tuple[str, ...]]] = []
    try:
        source_result = json.loads((source / RESULT).read_bytes())
        source_body = dict(source_result)
        source_claimed = source_body.pop("result_sha256", None)
        if source_claimed != objsha(source_body):
            raise RuntimeError("source candidate result closure")
        for index, (name, mutate, expected) in enumerate(ATTACKS):
            destination = root / f"{index:02d}-{name}"
            subprocess.run(["cp", "-a", "--reflink=auto", str(source), str(destination)], check=True)
            candidate = Candidate(destination)
            mutate(candidate)
            candidate.finish()
            attack_dirs.append((index, name, destination, expected))

        def execute(item: tuple[int, str, Path, tuple[str, ...]]) -> dict[str, Any]:
            index, name, directory, expected = item
            command = [
                sys.executable, "-B", str(verifier),
                "--candidate-dir", str(directory),
                "--seed", str(args.seed_base + index),
            ]
            proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            combined = proc.stdout + "\n" + proc.stderr
            rejected = proc.returncode != 0 and any(label in combined for label in expected)
            return {
                "attack_ordinal": index,
                "attack_name": name,
                "verification_seed": args.seed_base + index,
                "numeric_exit": proc.returncode,
                "expected_rejection_labels": list(expected),
                "expected_rejection_observed": rejected,
                "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
                "stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
                "stderr_tail": proc.stderr[-2000:],
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            attack_rows = list(pool.map(execute, attack_dirs))
        attack_rows.sort(key=lambda row: row["attack_ordinal"])
        if not all(row["expected_rejection_observed"] for row in attack_rows):
            raise RuntimeError("one or more attacks did not reach the expected fail-closed gate")
        semantic = {
            "schema": "cm2.c19c-endpoint-ownership-v3.attack-result.v1",
            "status": "PASS_ALL_COHERENT_RESIGNED_ATTACKS_REJECTED",
            "candidate_result_sha256": source_result["result_sha256"],
            "candidate_ledgers": source_result["ledgers"],
            "independent_verifier_sha256": filesha(verifier),
            "seed_base": args.seed_base,
            "attack_count": len(attack_rows),
            "rejected_attack_count": sum(row["expected_rejection_observed"] for row in attack_rows),
            "attacks": attack_rows,
            "formal_credit": 0,
        }
        result = {**semantic, "result_sha256": objsha(semantic)}
        Path(args.output).resolve().write_bytes(canonical(result))
        print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
