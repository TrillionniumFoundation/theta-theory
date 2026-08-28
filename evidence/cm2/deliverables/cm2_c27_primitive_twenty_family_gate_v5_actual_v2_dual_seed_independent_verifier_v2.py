#!/usr/bin/env python3
"""Independent dual-real-seed verifier v2 for the C27 actual-v2 aggregate.

This verifier is intentionally stdlib-only and does not import the assembler,
runner, handoff watcher, or any historical C27/C28/C29 implementation.  It
replays the five materialized ledgers, their joins, the proof-derived component
edge union, and the fresh DSU census for two completed real-seed transactions.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
RUNNER_SHA256 = "c0f2c29d03aad122762ba0b3dad5885418c17872dab3da665eb764dad9cab245"
ASSEMBLER_SHA256 = "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561"
WATCHER_SHA256 = "3e5f874230c9faf809975808a2bd7284acf32c6e2b771e36a86d532a1a22c386"
C15_PATH = ROOT / "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C15_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
EMPTY_SEQUENCE = hashlib.sha256(b"").hexdigest()

TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION",
    "OUTGOING_GRAPHS", "SINGLE_GRAPHS", "DOUBLE_GRAPHS",
    "SHEET_OWNER", "SHEET_SHADOW", "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS",
    "INCLUDED_STRATUM_ATTACHMENTS", "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
)
EXPECTED_CANDIDATES = (
    5_970_840, 276, 264, 4_984, 1_362_088, 17_940, 17_940,
    25_452, 10_688, 64_940, 10_660, 0, 1, 1, 1, 1, 0, 0, 0, 0,
)
EXPECTED_PROOFS = (
    32_240, 0, 0, 216, 0, 0, 0, 0, 0, 32_608,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
)
EXPECTED_DISPOSITIONS = {
    "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 65_064,
    "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 264_156,
    "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 7_156_856,
}
EXPECTED_LEDGER_COUNTS = {
    "candidate_ownership": 7_486_076,
    "materialized_physical_proof_join": 65_064,
    "atom_pair_incidence": 206_632,
    "atom_incidence_disposition": 483_232,
    "full_component_edge_union": 14_860,
}
SCHEMAS = {
    "candidate_ownership": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2",
    "materialized_physical_proof_join": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2",
    "atom_pair_incidence": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-pair-incidence.row.v2",
    "atom_incidence_disposition": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-incidence-disposition.row.v2",
    "full_component_edge_union": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.full-component-edge-union.row.v2",
}
EXPECTED_OUTPUT_NAMES = {
    *(name + ".jsonl.gz" for name in EXPECTED_LEDGER_COUNTS),
    "assembler_receipt.json", "manifest.sha256",
}


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def row_sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def fingerprint(info: os.stat_result) -> list[int]:
    """Match the runner's exact nine-field identity schema and ordering."""
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                "stable regular single-link file:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        require(fingerprint(os.fstat(descriptor)) == fingerprint(before),
                "stable fstat while hashing:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def strict_load(path: Path, closure: str | None = None) -> Any:
    raw = path.read_bytes()

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            require(key not in value, "duplicate JSON key:" + str(path))
            value[key] = item
        return value

    value = json.loads(raw, object_pairs_hook=pairs,
                       parse_constant=lambda item: (_ for _ in ()).throw(
                           Reject("non-finite JSON:" + item)))
    require(raw == encode(value) + b"\n", "canonical JSON:" + str(path))
    if closure is not None:
        require(type(value) is dict, "closed JSON object:" + str(path))
        body = dict(value)
        claim = body.pop(closure, None)
        require(type(claim) is str and claim == object_hash(body),
                "object closure:" + str(path))
    return value


def inside(path: Path) -> Path:
    resolved = path.resolve()
    require(resolved == ROOT or ROOT in resolved.parents,
            "path inside workspace:" + str(path))
    require(not path.is_symlink(), "no symlink path:" + str(path))
    return resolved


class Ledger:
    def __init__(self, out_dir: Path, name: str, descriptor: dict[str, Any]):
        self.name = name
        self.path = inside(out_dir / (name + ".jsonl.gz"))
        self.descriptor = descriptor
        self.expected_count = EXPECTED_LEDGER_COUNTS[name]
        require(descriptor["path"] == str(self.path.relative_to(ROOT))
                and descriptor["row_schema"] == SCHEMAS[name]
                and descriptor["row_count"] == self.expected_count
                and descriptor["size"] == self.path.stat().st_size
                and descriptor["sha256"] == file_sha(self.path),
                "ledger descriptor/file binding:" + name)
        ordering = descriptor["ordering"]
        require(type(ordering) is list and ordering
                and all(type(item) is str and item for item in ordering),
                "ledger ordering contract:" + name)
        self.ordering = ordering
        self.count = 0
        self.sequence = hashlib.sha256()
        self.previous: tuple[bytes, ...] | None = None

    def rows(self) -> Iterator[dict[str, Any]]:
        try:
            with gzip.open(self.path, "rb") as stream:
                for raw in stream:
                    require(raw.endswith(b"\n"), "ledger newline:" + self.name)
                    payload = raw[:-1]
                    row = json.loads(payload)
                    require(type(row) is dict and encode(row) == payload,
                            "canonical ledger row:" + self.name)
                    body = dict(row)
                    claim = body.pop("row_sha256", None)
                    require(type(claim) is str and claim == object_hash(body),
                            "ledger row closure:" + self.name)
                    require(row.get("schema") == SCHEMAS[self.name]
                            and row.get("ordinal") == self.count
                            and row.get("formal_credit") == 0,
                            "ledger schema/ordinal/governance:" + self.name)
                    key = tuple(encode(row[item]) for item in self.ordering)
                    require(self.previous is None or self.previous < key,
                            "strict ledger ordering:" + self.name)
                    self.previous = key
                    self.sequence.update(claim.encode("ascii") + b"\n")
                    self.count += 1
                    yield row
        except (EOFError, gzip.BadGzipFile) as error:
            raise Reject("gzip integrity:" + self.name + ":" + str(error))
        require(self.count == self.expected_count
                and self.sequence.hexdigest()
                    == self.descriptor["row_sequence_sha256"],
                "ledger count/sequence closure:" + self.name)


class DSU:
    def __init__(self, components: set[str]):
        self.parent = {item: item for item in components}
        self.size = {item: 1 for item in components}

    def find(self, item: str) -> str:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while item != root:
            parent = self.parent[item]
            self.parent[item] = root
            item = parent
        return root

    def union(self, left: str, right: str) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right] or (
                self.size[left] == self.size[right] and right < left):
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size.pop(right)
        return True


def load_c15() -> tuple[dict[str, str], set[str]]:
    require(file_sha(C15_PATH) == C15_SHA256, "frozen C15 SHA256 pin")
    members: dict[str, str] = {}
    components: set[str] = set()
    with gzip.open(C15_PATH, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            require(raw.endswith(b"\n"), "C15 newline")
            payload = raw[:-1]
            row = json.loads(payload)
            require(type(row) is dict and encode(row) == payload
                    and row["member_ordinal"] == ordinal,
                    "C15 canonical/ordinal")
            body = dict(row)
            claim = body.pop("row_sha256", None)
            require(claim == object_hash(body), "C15 row closure")
            member = row["registry_member_id"]
            component = row["fresh_component_id"]
            require(member not in members, "C15 unique member")
            members[member] = component
            components.add(component)
    require(len(members) == 502_204 and len(components) == 57_876,
            "C15 denominator")
    return members, components


def manifest_rows(path: Path) -> dict[str, str]:
    raw = path.read_bytes()
    require(raw.endswith(b"\n") and raw.decode("ascii").encode("ascii") == raw,
            "canonical manifest")
    lines = raw.decode("ascii").splitlines()
    require(lines == sorted(lines) and len(lines) == len(set(lines)),
            "sorted unique manifest")
    result: dict[str, str] = {}
    for line in lines:
        pieces = line.split("  ", 1)
        require(len(pieces) == 2 and len(pieces[0]) == 64
                and pieces[1] not in result, "manifest row")
        result[pieces[1]] = pieces[0]
    return result


def validate_native_run(seed: int, out_dir: Path,
                        run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    out_dir = inside(out_dir)
    run_dir = inside(run_dir)
    require((run_dir / "PASS.lock").read_bytes()
            == b"PASS_TRANSACTION_COMPLETE__ZERO_CREDIT\n"
            and not (run_dir / "FAILED.lock").exists(),
            "exclusive native PASS lock")
    require((run_dir / "exit_code.txt").read_bytes() == b"0\n"
            and strict_load(run_dir / "signal.json") is None
            and (run_dir / "stderr.log").read_bytes() == b"",
            "native exit0/no-signal/empty-stderr")
    pins = strict_load(run_dir / "pins.json")
    require(pins["runner"]["sha256"] == RUNNER_SHA256
            and pins["assembler"]["sha256"] == ASSEMBLER_SHA256,
            "native source pins")
    pre = strict_load(run_dir / "input_pre.json")
    post = strict_load(run_dir / "input_post.json")
    require(pre == post, "native pre/post exact identity")
    attestation = strict_load(run_dir / "run_attestation.json",
                              "run_attestation_sha256")
    require(attestation["status"]
            == "PASS_EXIT0_NO_SIGNAL_STDERR_EMPTY_PRE_POST_IDENTICAL_7_OF_7_GZIP_CANONICAL_COUNT_CLOSURE__ZERO_CREDIT"
            and attestation["execution_seed"] == seed
            and attestation["numeric_exit_code"] == 0
            and attestation["signal"] is None
            and attestation["stderr_empty"] is True
            and attestation["pre_post_sha256_identical"] is True
            and attestation["pre_post_stat_identical"] is True
            and attestation["input_pre"] == pre == attestation["input_post"]
            and attestation["runner_source_sha256"] == RUNNER_SHA256
            and attestation["formal_credit"] == 0
            and attestation["manifest_authorized"] is False
            and attestation["C27_C28_C29"]
                == "UNAUTHORIZED_PENDING_FINAL_RECEIPT_V2"
            and attestation["CM2"] == "NO-GO_FOR_CLAIM",
            "native run attestation state")
    validation = strict_load(run_dir / "output_validation.json")
    require(object_hash(validation) == attestation["output_validation_sha256"]
            and validation["status"]
                == "PASS_7_OF_7_GZIP_CANONICAL_COUNT_CLOSURE"
            and validation["output_file_count"] == 7
            and validation["formal_credit"] == 0
            and validation["manifest_authorized"] is False,
            "native output validation closure")
    entries = sorted(out_dir.iterdir(), key=lambda item: item.name)
    require({item.name for item in entries} == EXPECTED_OUTPUT_NAMES
            and all(item.is_file() and not item.is_symlink()
                    for item in entries), "exact current 7/7 outputs")
    for item in entries:
        recorded = validation["output_files"][item.name]
        require(file_sha(item) == recorded["sha256"]
                and fingerprint(item.stat()) == recorded["stat"],
                "current output SHA/stat:" + item.name)
    receipt = strict_load(out_dir / "assembler_receipt.json",
                          "assembler_receipt_sha256")
    require(receipt["schema"]
            == "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-assembler-receipt.v2"
            and receipt["status"]
                == "PASS_FRESH_TWENTY_TERMINAL_GLOBAL_RECLOSURE_PROOF_DERIVED_EDGE_UNION_AND_DSU__PENDING_FINAL_ZERO_CREDIT_RECEIPT_V2"
            and receipt["execution_seed"] == seed
            and receipt["assembler_source_sha256"] == ASSEMBLER_SHA256
            and receipt["formal_credit"] == 0
            and receipt["manifest_authorized"] is False
            and receipt["source_W_transition_authorized"] is False
            and receipt["C27_C28_C29"]
                == "UNAUTHORIZED_PENDING_FINAL_RECEIPT_V2"
            and receipt["CM2"] == "NO-GO_FOR_CLAIM",
            "assembler receipt state")
    require(file_sha(out_dir / "assembler_receipt.json")
            == attestation["assembler_receipt_file_sha256"]
            and receipt["assembler_receipt_sha256"]
                == attestation["assembler_receipt_object_sha256"],
            "attestation/receipt binding")
    manifest = manifest_rows(out_dir / "manifest.sha256")
    for name in EXPECTED_LEDGER_COUNTS:
        relative = str((out_dir / (name + ".jsonl.gz")).relative_to(ROOT))
        require(manifest.get(relative)
                == receipt["materialized_ledger_descriptors"][name]["sha256"],
                "manifest output binding:" + name)
    return receipt, attestation


def replay_math(seed: int, out_dir: Path, run_dir: Path,
                members: dict[str, str], components: set[str]) -> dict[str, Any]:
    receipt, attestation = validate_native_run(seed, out_dir, run_dir)
    descriptors = receipt["materialized_ledger_descriptors"]
    require(set(descriptors) == set(EXPECTED_LEDGER_COUNTS),
            "five exact ledger descriptors")

    proof_hashes: dict[str, list[str]] = defaultdict(list)
    edge_support: dict[str, tuple[list[str], list[str]]] = {}
    proof_terminal = Counter()
    proof_ledger = Ledger(out_dir, "materialized_physical_proof_join",
                          descriptors["materialized_physical_proof_join"])
    for row in proof_ledger.rows():
        terminal = row["terminal"]
        member_pair = row["ordered_C15_member_pair"]
        component_pair = row["ordered_C15_component_pair"]
        require(terminal in TERMINALS
                and type(member_pair) is list and len(member_pair) == 2
                and member_pair[0] < member_pair[1]
                and all(item in members for item in member_pair),
                "proof terminal/member pair")
        remapped = sorted((members[member_pair[0]], members[member_pair[1]]))
        require(type(component_pair) is list and len(component_pair) == 2
                and component_pair[0] < component_pair[1]
                and component_pair == remapped,
                "proof fresh C15 remap")
        edge_key = EDGE_PREFIX + object_hash(component_pair)
        require(row["component_edge_key"] == edge_key,
                "proof edge derivation")
        proof_hashes[row["candidate_key"]].append(row["row_sha256"])
        proof_terminal[terminal] += 1
        if edge_key not in edge_support:
            edge_support[edge_key] = (component_pair, [])
        require(edge_support[edge_key][0] == component_pair,
                "edge key unique pair")
        edge_support[edge_key][1].append(row["row_sha256"])
    require(tuple(proof_terminal[name] for name in TERMINALS)
            == EXPECTED_PROOFS and len(proof_hashes) == 65_064,
            "proof terminal/candidate census")

    candidate_terminal = Counter()
    dispositions = Counter()
    pair_owners: dict[str, tuple[str, str]] = {}
    seen_proof_candidates: set[str] = set()
    candidate_ledger = Ledger(out_dir, "candidate_ownership",
                              descriptors["candidate_ownership"])
    for row in candidate_ledger.rows():
        terminal = row["terminal"]
        terminal_ordinal = row["terminal_ordinal"]
        require(type(terminal_ordinal) is int
                and 0 <= terminal_ordinal < len(TERMINALS)
                and TERMINALS[terminal_ordinal] == terminal
                and row["authority_slot"]
                    == f"T{terminal_ordinal:02d}_{terminal}",
                "candidate terminal binding")
        hashes = proof_hashes.get(row["candidate_key"], [])
        disposition = row["component_relation_disposition"]
        require(row["physical_proof_row_count"] == len(hashes)
                and row["physical_proof_row_sequence_sha256"]
                    == row_sequence(hashes)
                and disposition in EXPECTED_DISPOSITIONS
                and ((disposition
                      == "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED")
                     == bool(hashes)),
                "candidate/proof exact join")
        if hashes:
            seen_proof_candidates.add(row["candidate_key"])
        if terminal_ordinal in {7, 8, 9}:
            require(row["candidate_key"] not in pair_owners,
                    "unique T07/T09 candidate owner")
            pair_owners[row["candidate_key"]] = (
                row["row_sha256"], terminal)
        candidate_terminal[terminal] += 1
        dispositions[disposition] += 1
    require(tuple(candidate_terminal[name] for name in TERMINALS)
            == EXPECTED_CANDIDATES
            and dict(dispositions) == EXPECTED_DISPOSITIONS
            and seen_proof_candidates == set(proof_hashes)
            and len(pair_owners) == 101_080,
            "candidate global conservation")

    atom_hashes: dict[str, list[str]] = defaultdict(list)
    atom_terminals: dict[str, set[str]] = defaultdict(set)
    incidence_terminal = Counter()
    incidence_candidates: set[str] = set()
    incidence_keys: set[str] = set()
    incidence_ledger = Ledger(out_dir, "atom_pair_incidence",
                              descriptors["atom_pair_incidence"])
    for row in incidence_ledger.rows():
        candidate = row["candidate_pair_key"]
        terminal = row["candidate_terminal"]
        require(candidate in pair_owners
                and pair_owners[candidate] == (
                    row["candidate_owner_row_sha256"], terminal)
                and row["incidence_key"] not in incidence_keys,
                "incidence candidate owner/unique key")
        incidence_keys.add(row["incidence_key"])
        incidence_candidates.add(candidate)
        atom = row["primitive_support_atom_key"]
        atom_hashes[atom].append(row["row_sha256"])
        atom_terminals[atom].add(terminal)
        incidence_terminal[terminal] += 1
    require(incidence_candidates == set(pair_owners)
            and dict(incidence_terminal) == {
                "SIGNED_BOUNDARY_FACES": 55_536,
                "COMPLETE_BOUNDARY_FACES": 30_624,
                "POSITIVE_VOLUME_CARRIERS": 120_472,
            }, "incidence exact coverage/census")

    incident = complement = multi_terminal = 0
    disposition_atoms: set[str] = set()
    disposition_ledger = Ledger(out_dir, "atom_incidence_disposition",
                                descriptors["atom_incidence_disposition"])
    for row in disposition_ledger.rows():
        atom = row["primitive_support_atom_key"]
        require(atom not in disposition_atoms, "unique atom disposition")
        disposition_atoms.add(atom)
        hashes = atom_hashes.get(atom, [])
        terminals = sorted(atom_terminals.get(atom, set()))
        expected = ("EXACT_NONEMPTY_ATOM_PAIR_INCIDENCE_SET" if hashes
                    else "EXACT_EMPTY_INCIDENCE_COMPLEMENT")
        require(row["incidence_count"] == len(hashes)
                and row["incidence_row_sequence_sha256"]
                    == row_sequence(hashes)
                and row["terminal_set"] == terminals
                and row["disposition"] == expected,
                "atom/incidence exact join")
        incident += int(bool(hashes))
        complement += int(not hashes)
        multi_terminal += int(len(terminals) > 1)
    require(set(atom_hashes).issubset(disposition_atoms)
            and incident == 62_768 and complement == 420_464
            and multi_terminal == 3_896,
            "atom denominator/complement census")

    dsu = DSU(components)
    merges = cycles = 0
    seen_edges: set[str] = set()
    edge_ledger = Ledger(out_dir, "full_component_edge_union",
                         descriptors["full_component_edge_union"])
    for row in edge_ledger.rows():
        edge = row["component_edge_key"]
        require(edge not in seen_edges and edge in edge_support
                and row["ordered_C15_component_pair"] == edge_support[edge][0]
                and row["supporting_physical_proof_row_count"]
                    == len(edge_support[edge][1])
                and row["supporting_physical_proof_row_sequence_sha256"]
                    == row_sequence(edge_support[edge][1]),
                "edge/proof exact union")
        seen_edges.add(edge)
        if dsu.union(*row["ordered_C15_component_pair"]):
            merges += 1
        else:
            cycles += 1
    require(seen_edges == set(edge_support)
            and merges == 14_192 and cycles == 668
            and len(components) - merges == 43_684,
            "fresh proof-derived DSU census")

    calculated_exact = {
        "candidate_total": sum(candidate_terminal.values()),
        "materialized_physical_proof_total": sum(proof_terminal.values()),
        "terminal_candidate_census": {
            name: candidate_terminal[name] for name in TERMINALS},
        "terminal_materialized_physical_proof_census": {
            name: proof_terminal[name] for name in TERMINALS},
        "candidate_component_disposition_census": dict(dispositions),
        "atom_pair_incidence_total": sum(incidence_terminal.values()),
        "atom_pair_incidence_terminal_census": dict(incidence_terminal),
        "primitive_atom_denominator": incident + complement,
        "incident_atoms": incident,
        "exact_complement_atoms": complement,
        "multi_terminal_atoms": multi_terminal,
        "full_component_edge_union_total": len(seen_edges),
        "frozen_C15_member_total": len(members),
        "frozen_C15_component_total": len(components),
        "fresh_DSU_successful_merges": merges,
        "fresh_DSU_cycle_edges": cycles,
        "fresh_DSU_final_component_total": len(components) - merges,
    }
    require(receipt["exact_census"] == calculated_exact,
            "independently recomputed exact census")
    expected_closures = {
        "candidate_pairs_each_exactly_one_terminal": True,
        "incidence_is_candidate": False,
        "candidate_proof_sequences_use_global_reclosed_proof_rows": True,
        "incidence_owner_hashes_use_global_reclosed_candidate_rows": True,
        "atom_dispositions_use_global_reclosed_incidence_rows": True,
        "component_edges_derived_only_from_physical_proof_member_pairs": True,
        "proof_member_pairs_freshly_remapped_through_frozen_C15": True,
        "fresh_DSU_starts_from_57876_singletons": True,
    }
    require(receipt["derivation_closures"] == expected_closures
            and all(value is False for value in
                    receipt["forbidden_input_governance"].values()),
            "derivation/non-import governance")
    projection = {
        "ledger_descriptors": {
            name: {key: value for key, value in descriptors[name].items()
                   if key != "path"}
            for name in sorted(descriptors)},
        "exact_census": calculated_exact,
        "derivation_closures": expected_closures,
        "forbidden_input_governance": receipt["forbidden_input_governance"],
        "interface_v2_file_sha256": receipt["interface_v2_file_sha256"],
        "interface_v2_object_sha256": receipt["interface_v2_object_sha256"],
        "terminal_authority_descriptors": receipt["terminal_authority_descriptors"],
    }
    return {
        "execution_seed": seed,
        "run_attestation_file_sha256": file_sha(run_dir / "run_attestation.json"),
        "run_attestation_object_sha256": attestation["run_attestation_sha256"],
        "assembler_receipt_file_sha256": file_sha(out_dir / "assembler_receipt.json"),
        "assembler_receipt_object_sha256": receipt["assembler_receipt_sha256"],
        "manifest_file_sha256": file_sha(out_dir / "manifest.sha256"),
        "input_snapshot_sha256": object_hash(attestation["input_pre"]),
        "mathematical_projection_sha256": object_hash(projection),
        "projection": projection,
    }


def verify(args: argparse.Namespace) -> dict[str, Any]:
    require(args.seed1 > 0 and args.seed2 > 0 and args.seed1 != args.seed2,
            "two distinct positive real seeds")
    require(args.verification_seed > 0, "positive verification seed")
    require(file_sha(SELF) == args.expect_verifier_sha256,
            "verifier self SHA256 pin")
    runner = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_runner.py"
    assembler = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2.py"
    watcher = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_seed2_gated_handoff.py"
    require(file_sha(runner) == RUNNER_SHA256
            and file_sha(assembler) == ASSEMBLER_SHA256
            and file_sha(watcher) == WATCHER_SHA256,
            "runner/assembler/handoff watcher source pins")
    members, components = load_c15()
    jobs = [
        (args.seed1, inside(Path(args.seed1_out)), inside(Path(args.seed1_run))),
        (args.seed2, inside(Path(args.seed2_out)), inside(Path(args.seed2_run))),
    ]
    random.Random(args.verification_seed).shuffle(jobs)
    observed: dict[int, dict[str, Any]] = {}
    for seed, out_dir, run_dir in jobs:
        observed[seed] = replay_math(seed, out_dir, run_dir,
                                     members, components)
    first = observed[args.seed1]
    second = observed[args.seed2]
    require(first["input_snapshot_sha256"] == second["input_snapshot_sha256"],
            "dual-seed identical immutable input snapshot")
    require(first["mathematical_projection_sha256"]
            == second["mathematical_projection_sha256"]
            and first["projection"] == second["projection"],
            "exact seed-invariant mathematical outputs")
    for name in EXPECTED_LEDGER_COUNTS:
        require(first["projection"]["ledger_descriptors"][name]["sha256"]
                == second["projection"]["ledger_descriptors"][name]["sha256"],
                "byte-identical dual-seed ledger:" + name)
    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-real-seed-verification.v1",
        "status": "PASS_TWO_REAL_SEEDS_NATIVE_FULL_PASS_INDEPENDENT_GLOBAL_REPLAY_AND_EXACT_SEED_INVARIANCE__ZERO_CREDIT",
        "verification_seed": args.verification_seed,
        "execution_seeds": [args.seed1, args.seed2],
        "seed_runs": {str(seed): {key: value for key, value in item.items()
                                  if key != "projection"}
                      for seed, item in sorted(observed.items())},
        "seed_invariant_mathematical_projection_sha256":
            first["mathematical_projection_sha256"],
        "exact_census": first["projection"]["exact_census"],
        "ledger_descriptors": first["projection"]["ledger_descriptors"],
        "source_pins": {
            "runner": RUNNER_SHA256,
            "assembler": ASSEMBLER_SHA256,
            "seed2_handoff_watcher": WATCHER_SHA256,
            "frozen_C15": C15_SHA256,
            "independent_verifier": args.expect_verifier_sha256,
        },
        "implementation_independence": {
            "assembler_runner_watcher_or_C27_C28_C29_module_imported": False,
            "stdlib_only": True,
            "fresh_join_and_DSU_recomputed": True,
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2_C28_C29": "UNAUTHORIZED_PENDING_ACTUAL_V2_TERMINAL_SEAL",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["semantic_projection_sha256"] = object_hash({
        key: value for key, value in body.items()
        if key not in {"verification_seed", "seed_runs"}
    })
    result["verification_sha256"] = object_hash(result)
    output = inside(Path(args.out_file))
    require(not output.exists(), "fresh verification output")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, encode(result) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed1", type=int, required=True)
    parser.add_argument("--seed1-out", required=True)
    parser.add_argument("--seed1-run", required=True)
    parser.add_argument("--seed2", type=int, required=True)
    parser.add_argument("--seed2-out", required=True)
    parser.add_argument("--seed2-run", required=True)
    parser.add_argument("--verification-seed", type=int, required=True)
    parser.add_argument("--expect-verifier-sha256", required=True)
    parser.add_argument("--out-file", required=True)
    args = parser.parse_args()
    try:
        result = verify(args)
    except (Reject, KeyError, TypeError, ValueError, OSError, EOFError,
            gzip.BadGzipFile, json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": result["status"],
                  "verification_sha256": result["verification_sha256"],
                  "semantic_projection_sha256":
                      result["semantic_projection_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
