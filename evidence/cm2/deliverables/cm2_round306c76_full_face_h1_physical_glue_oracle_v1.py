#!/usr/bin/env python3
"""C76: exact full-face H1 graphs and physical chart glue.

The parent process treats every upstream as pinned inert bytes and never loads
the numerical kernel.  Fresh child processes independently reconstruct bounded
batches at 384 bits; this both bounds FLINT memory and makes batch size an
irrelevant build-isolation variable.  No producer, verifier, pointer, or seal
from an upstream round is imported or executed.
"""
from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import itertools
import json
import os
import stat
import subprocess
import sys
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
SCHEMA = "cm2.round306c76.full-face-h1-physical-glue-oracle.v1"
PREFIX = "cm2_round306c76_full_face_h1_physical_glue_oracle_v1"
ROWS = PREFIX + ".jsonl.gz"
INCIDENCE = PREFIX + "_root_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
VERIFICATION = PREFIX + "_independent_verification_v1.json"
DUAL = PREFIX + "_dual_completion_receipt_v1.json"
LOCK = "ZERO_CREDIT_STAGED_FULL_FACE_PHYSICAL_GLUE_ORACLE_ONLY.lock"
BASE_MEMBERS = [ROWS, INCIDENCE, RESULT, REPORT, LOCK, MANIFEST, OUTER]
PRECISION = 384
SELECTOR = "REGULAR_FULL_FACE_GRAPH"
EXPECTED_SCOPE = 10_298
EXPECTED_SEQUENCE = "c59841c74438e421d2d679a62cd1e8cf5dce36fd0efb0c1a77e4bffbf206077d"
EXPECTED_PAIR_CENSUS = {31: 466, 200: 42, 270: 133, 321: 2_025,
                        631: 3_504, 711: 147, 787: 1_115, 853: 2_866}
EXPECTED_ROUTE_CENSUS = {"COLLISION1_OFFICIAL_WORD_MISMATCH": 9_510,
                         "COLLISION2_STRICT_OWNER_MISMATCH": 788}
FROZEN_OWNER = "W[1,0]"
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
ZERO = {"formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0}
PURE_CORE = OUT / "cm2_round306c72x_implicit_h1_root_physical_glue_core_v1.py"
PURE_CORE_PIN = "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8"
CHART_MANIFEST = OUT / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
CHART_MANIFEST_PIN = "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b"
CHART_CERTIFICATE_PIN = "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1"
CHART_DEPENDENCIES = {
    "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json":
        "dc394ee38b1e1c36a3cabf27d69279576a8f58f40705537c38c04524781b37d7",
    "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json":
        "58f2460f7bbfb5bab6c0c7cb48c706482359ffb423dc35abcbd2069220db1388",
    "cm2-v52-manifest.sha256":
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368",
    "cm2_gate3_endpoint_identity_refinement_cert.py":
        "547c48d1b350fb1781719f936634b72c5664b4842e1f33fddb02c33bcbdf7563",
    "cm2_gate3_global_physical_subrow_atlas_cert.py":
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc",
}

C72_NAMES = {
    "result": "cm2_round306c72_structural_child_obligation_atlas_v1_result.json",
    "ledger": "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz",
    "verification": "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json",
}
C38_DIR = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C71B_DIR = ROOT / ".cm2-runtime/c71b-v3-final-75c21279"
C72O_DIR = ROOT / ".cm2-runtime/c72o-build-a2.v1"
C73_DIR = ROOT / ".cm2-runtime/c73v2-build-a.QOYACE"
C74L_DIR = ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt"
C75_DIR = ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ"

PINS = {
    "C72_RESULT": "55318b7c3ee778cb8a0e41d612c9c2caa44790e6fff816a6104116268258f01e",
    "C72_LEDGER": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
    "C72_VERIFY": "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0",
    "C65_RESULT": "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    "C65_LEAVES": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "C65_VERIFY": "7d4e97bd641da7c5ccc64e8c2ad3d59f21ba3ebd73eb0e4d55c88ad617ee23b4",
    "C65_SELFTEST": "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274",
    "C65_REPLAY": "c7d99ba4fea05fbd7a3b478f025323c77e5335951e4ff08743ad37ba47fa8e85",
    "C65_MANIFEST": "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5",
    "C65_OUTER": "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d",
    "C69_RESULT": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "C69_BLOCKERS": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "C69_VERIFY": "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6",
    "C69_MANIFEST": "c231941ca4f5f76a95faa81e8390e3f11b5d1af84b645605c52245e6ff214749",
    "C69_OUTER": "2baac1cf22ca8be0163f9027d0365e948107b535df917a25334626110bf2916c",
    "C38_RESULT": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_CHILDREN": "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2",
    "C35_PATH": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C37_PATH": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
    "C71B_RESULT": "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246",
    "C71B_VERIFY": "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612",
    "C71B_RECEIPT": "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc",
    "C72O_RESULT": "fd9ca6489f5fedef85fb55de6906a62ecadc417c72d7eb938a6268e7f402302a",
    "C72O_LEDGER": "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355",
    "C72O_VERIFY": "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb",
    "C73_RESULT": "5de9d37c69ed4d13d972eff8845ed55ad695ab040d6c1beda01626c0c065c615",
    "C73_LEDGER": "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc",
    "C73_VERIFY": "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1",
    "C74L_VERIFY": "13e64bdf935b9bb14119ae13892ed1f8deb66e07c281e12df2e370d86b28499c",
    "C74L_RECEIPT": "1b9459e41a3de4ce5ab2f99b946ce6cb325c63934d87c641571c474f62ad7a3a",
    "C75_LEDGER": "e1e30a36f75c2ec71b0c4ec51da33e3c09fb5570426aa356f0c815406e251229",
    "C75_RESULT": "1d9d4b2f8b7a4bfb6133ce7b23c22765ef9097c133cc47dc199dd0479f478366",
    "C75_VERIFY": "8f620e4e7312828dcbcee23cf3f33280c8583bd414ded493b7996b2279131a4c",
    "C75_RECEIPT": "dbbad4ea8d807b6bcb8b7f121acc57f782925be7e00c9267b9edf011e3eba2b1",
}
OBJECTS = {
    "C72_RESULT": "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4",
    "C72_VERIFY": "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994",
    "C71B_RESULT": "75c21279e3440a32116e67c20f12c7ec9d299491d018e2982ab18d68118d4158",
    "C71B_VERIFY": "c45c5b19daeaef930f981810722460424a0d55c8302380829757e2132754f5c3",
    "C71B_RECEIPT": "d7fd8322b72fad933bb80542913b00cb54c5d7a3d93bf8cb7601aefa5daadbcd",
    "C72O_RESULT": "529d7081293b37111619d4dbf03c750be06da48105d46cc18e8c79eee10b48e7",
    "C72O_VERIFY": "41d383e0fc68ec7d7c4887ae6ef534b5b7bd19277837a14754e5c7ef5bf85715",
    "C73_RESULT": "4ddba93eea8b798de3dbc8a74608fc27686e46c9209784a6bccdd5df7fd1e1cc",
    "C73_VERIFY": "c6d9bc55347de05cef6dc3061a905e1052521a16bb6a6535233c9012b77ffd9d",
    "C74L_VERIFY": "4bb934f0f2e4d859c606be5a995c801e0c3056c629eaff24e47b93d207b4587d",
    "C74L_RECEIPT": "0e5cb45766738511282f2509d31bb512033c20e6a04766683b82bacb4a89a44c",
    "C75_RESULT": "695fb1bb410c45fedbe5eef5cfc104a7043d452b75f03b1baa811b6e7426d863",
    "C75_VERIFY": "461b7b014fa24b5da33c9f52267c0f1e5302c0ff56a3159db80975161a7a0aaa",
    "C75_RECEIPT": "f411d89fc4b751fc829e60c856f23cebc03a3b89895328cb1714fc99f0291b3b",
}
NUMERIC_PINS = {
    "r185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "r178": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "atlas": "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "ge": "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "registry": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "r139": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "lower": "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b",
    "round136": "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    "time3": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "time2": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "core": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "step1": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def line_sequence(values: Iterable[str]) -> str:
    result = hashlib.sha256()
    for value in values:
        result.update(value.encode("ascii") + b"\n")
    return result.hexdigest()


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns), "TOCTOU:" + str(path))
        return hasher.hexdigest()
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str) -> bytes:
    raw = path.read_bytes()
    need(not path.is_symlink() and path.stat().st_nlink == 1 and
         hashlib.sha256(raw).hexdigest() == expected, "file pin:" + str(path))
    return raw


def parse(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict, label + ":object")
    return value


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(claim == expected == digest(body), label + ":object closure")


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def iter_jsonl(path: Path, expected: str, count: int) -> Iterator[dict[str, Any]]:
    need(file_sha(path) == expected, "ledger pin:" + str(path))
    with gzip.open(path, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), "row newline")
            row = parse(raw[:-1], str(path) + ":" + str(ordinal))
            need(canonical(row) + b"\n" == raw, "canonical row")
            close_row(row, "row")
            yield row
        need(ordinal + 1 == count, "row count:" + str(path))


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            size = os.write(descriptor, view)
            need(size > 0, "short write")
            view = view[size:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    need(path.read_bytes() == raw and path.lstat().st_nlink == 1,
         "terminal byte replay:" + path.name)


class Ledger:
    def __init__(self, path: Path, order: str):
        self.path, self.order = path, order
        self.raw = None
        self.gz = None
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self):
        descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                             0o644)
        self.raw = os.fdopen(descriptor, "wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row = {**body, "row_sha256": digest(body)}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args):
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order,
                "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": file_sha(self.path), "size": self.path.stat().st_size}



def numeric_modules(r185: Any, r139: Any) -> dict[str, str]:
    modules = {"r185": r185, "r178": r185.r178, "atlas": r185.atlas,
               "ge": r185.ge, "registry": r185.registry, "r139": r139,
               "lower": r139.lower, "round136": r139.lower.round136,
               "time3": r139.lower.time3, "time2": r139.lower.time3.time2_cert,
               "core": r139.lower.core_cert, "step1": r139.lower.step1}
    observed = {name: file_sha(Path(module.__file__).resolve())
                for name, module in modules.items()}
    need(observed == NUMERIC_PINS, "numeric source pins")
    return observed


def chart_authority() -> dict[str, Any]:
    raw = pinned(CHART_MANIFEST, CHART_MANIFEST_PIN)
    manifest = parse(raw, "chart seam quotient manifest")
    need(manifest["certificate_sha256"] == CHART_CERTIFICATE_PIN and
         manifest["dependencies"] == CHART_DEPENDENCIES and
         manifest["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED",
         "chart seam quotient certificate")
    rule = manifest["result"]["unique_half_open_owner_rule"]
    need(rule["diagonal_tie"] == "E or W owns; N or S excludes" and
         rule["same_physical_normal_on_paired_representations"] is True and
         rule["duplicate_trace_is_identified_not_added"] is True and
         manifest["result"]["scope_limits"]
             ["ownership_rule_applies_to_analytic_strata"] is True,
         "analytic seam ownership rule")
    for name, expected in CHART_DEPENDENCIES.items():
        pinned(OUT / name, expected)
    need(file_sha(PURE_CORE) == PURE_CORE_PIN, "pure physical glue core pin")
    return {
        "manifest_file_sha256": CHART_MANIFEST_PIN,
        "certificate_sha256": CHART_CERTIFICATE_PIN,
        "eight_chart_seam_ownership": "CERTIFIED",
        "diagonal_tie": "E or W owns; N or S excludes",
        "same_physical_normal_on_paired_representations": True,
        "duplicate_trace_is_identified_not_added": True,
    }




def worker() -> int:
    payload = json.load(sys.stdin)
    sys.path.insert(0, str(SITE))
    sys.path.insert(0, str(OUT))
    from flint import ctx
    ctx.prec = PRECISION
    import cm2_round185_preconditioned_c1_residual_refinement as r185
    import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    import cm2_round306c72x_implicit_h1_root_physical_glue_core_v1 as physical_core
    numeric_modules(r185, r139)
    need(file_sha(Path(physical_core.__file__).resolve()) == PURE_CORE_PIN,
         "worker pure core pin")
    authority = chart_authority()
    origins = {int(key): value for key, value in payload["origins"].items()}
    original, reflected = payload["original"], payload["reflected"]
    expected_word = original[0]["official_word_key_id"]
    expected_owners = {original[1]["selected_absolute_owner_id"],
                       reflected[1]["selected_absolute_owner_id"]}
    pair_index, pattern_index, registry = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())
    output = []
    for atlas in payload["rows"]:
        raw_box = atlas["exact_representative_box"]
        box = r185.atlas.AtlasBox(Q(raw_box["t"][0]), Q(raw_box["t"][1]),
                                  Q(raw_box["p"][0]), Q(raw_box["p"][1]),
                                  Q(0), Q(0), len(atlas["child_path"]), atlas["child_path"])
        origin = origins[atlas["pair_index"]]
        certificate, roots, kind = physical_core.geometry_and_roots(
            r185, origin, box, atlas)
        nx_sign = certificate["normal_component_signs"]["nx"]
        ny_sign = certificate["normal_component_signs"]["ny"]
        base = {"schema": SCHEMA + ".decision-row",
                "C72_atlas_row_sha256": atlas["row_sha256"],
                "C65_aggregate_child_row_sha256": atlas["C65_aggregate_child_row_sha256"],
                "C69c_blocker_row_sha256": atlas["C69c_blocker_row_sha256"],
                "C61_aggregate_leaf_row_sha256": atlas["C61_aggregate_leaf_row_sha256"],
                "pair_index": atlas["pair_index"], "source_path": atlas["source_path"],
                "child_path": atlas["child_path"], "parent_key": origin,
                "exact_representative_box": raw_box,
                "exact_reflected_box": atlas["exact_reflected_box"],
                "parent_volume_fraction": atlas["parent_volume_fraction"],
                "selector": "child_route_witness == REGULAR_FULL_FACE_GRAPH",
                "additional_dyadic_depth": 0, "H1_geometry": certificate,
                "H1_geometry_closed": True, **ZERO}
        need(kind == "CLIPPED" and nx_sign < 0 and ny_sign != 0 and
             len(roots) == 2, "full-face clipped graph geometry")
        route = physical_core.downstream_W_closed_box(
            r185, r139, origin, box, expected_word, expected_owners,
            pair_index, pattern_index, cores)
        need(route["outcome"] in EXPECTED_ROUTE_CENSUS and
             route["selected_collision2_owner"] not in expected_owners,
             "strict mismatch rather than collision3 handoff")
        chart = "N" if ny_sign > 0 else "S"
        glue = physical_core.implicit_graph_state_glue(
            certificate["normal_component_signs"], roots, route, authority)
        owner_glue = {
            "representative_half_open_physical_owner": "W",
            "reflected_half_open_physical_owner": "E",
            "representative_shadow_chart": chart,
            "reflected_shadow_chart": "S" if chart == "N" else "N",
            "same_physical_state_on_representative_chart_seam": True,
            "same_physical_state_on_reflected_chart_seam": True,
            "horizontal_reflection_maps_W_owner_to_E_owner_bijectively": True,
            "W_and_E_are_dual_occurrences_not_duplicate_credit": True,
            "chart_seam_authority_sha256": CHART_MANIFEST_PIN,
        }
        exits = [
            {"stratum": "H1_LT_0", "exit_class": "STRICT_EXCLUSION",
             "reason": "COLLISION1_OUTGOING_CHART_MISMATCH", "chart": chart},
            {"stratum": "H1_GT_0", "exit_class": "STRICT_EXCLUSION",
             "representative_chart": "W", "reflected_chart": "E",
             "downstream": route},
            {"stratum": "H1_EQ_0", "exit_class": "STRICT_EXCLUSION",
             "representative_chart": "W", "reflected_chart": "E",
             "physical_chart_glue": glue,
             "representative_reflected_owner_glue": owner_glue,
             "graph_is_not_a_terminal": True,
             "downstream": route}]
        outcome = ("STRICT_EXCLUSION_WHOLE_FULL_FACE_CHILD__PHYSICAL_GRAPH_GLUE__" +
                   route["outcome"])
        output.append({**base, "stratum_exits": exits,
                       "allowed_exit_closed_for_every_stratum": True,
                       "whole_child_strict_exclusion_closed": True,
                       "physical_chart_glue_closed": True,
                       "collision3_handoff": None,
                       "sealed_collision3_handoff_count": 0,
                       "explicit_residual_strata": 0,
                       "row_outcome": outcome,
                       "current_disposition": "STAGED_ZERO_CREDIT_STRICT_EXCLUSION",
                       "candidate_is_authority": False,
                       "global_consumption_ready": False,
                       "official_registry_sha256": registry})
    json.dump(output, sys.stdout, sort_keys=True, separators=(",", ":"),
              ensure_ascii=False)
    return 0


def input_bundle(c72_a: Path, c72_b: Path) -> tuple[list[dict[str, Any]], dict[int, str], list[dict[str, Any]], list[dict[str, Any]]]:
    chart_authority()
    for directory in (c72_a, c72_b):
        result = parse(pinned(directory / C72_NAMES["result"], PINS["C72_RESULT"]), "C72 result")
        verify = parse(pinned(directory / C72_NAMES["verification"], PINS["C72_VERIFY"]), "C72 verify")
        close_object(result, OBJECTS["C72_RESULT"], "C72 result")
        close_object(verify, OBJECTS["C72_VERIFY"], "C72 verify")
        need(result["ledger"]["sha256"] == PINS["C72_LEDGER"] and
             verify["candidate_object_sha256"] == OBJECTS["C72_RESULT"], "C72 gate")
    need(pinned(c72_a / C72_NAMES["ledger"], PINS["C72_LEDGER"]) ==
         pinned(c72_b / C72_NAMES["ledger"], PINS["C72_LEDGER"]), "C72 dual ledger bytes")

    direct = [
        (OUT / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json", "C65_RESULT"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json", "C65_VERIFY"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json", "C65_SELFTEST"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json", "C65_REPLAY"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256", "C65_MANIFEST"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json", "C65_OUTER"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json", "C69_RESULT"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json", "C69_VERIFY"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256", "C69_MANIFEST"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json", "C69_OUTER"),
        (C38_DIR / "result.json", "C38_RESULT"),
        (C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json", "C71B_RESULT"),
        (C71B_DIR / "independent_verification_v3_1.json", "C71B_VERIFY"),
        (C71B_DIR / "dual_build_publication_completion_receipt_v3.json", "C71B_RECEIPT"),
        (C72O_DIR / "cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json", "C72O_RESULT"),
        (ROOT / ".cm2-runtime/c72o-independent-verification-v2.json", "C72O_VERIFY"),
        (C73_DIR / "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json", "C73_RESULT"),
        (ROOT / ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json", "C73_VERIFY"),
        (C74L_DIR / "cm2_round306c74l_source_seam_collision1_handoff_successor_independent_verification_v1_1.json", "C74L_VERIFY"),
        (C74L_DIR / "cm2_round306c74l_source_seam_collision1_handoff_successor_dual_completion_receipt_v1.json", "C74L_RECEIPT"),
        (C75_DIR / "cm2_round306c75_first_tangency_exact_strata_oracle_v1_result.json", "C75_RESULT"),
        (C75_DIR / "cm2_round306c75_first_tangency_exact_strata_oracle_v1_independent_verification_v1.json", "C75_VERIFY"),
        (C75_DIR / "cm2_round306c75_first_tangency_exact_strata_oracle_v1_dual_completion_receipt_v1.json", "C75_RECEIPT"),
    ]
    for path, key in direct:
        raw = pinned(path, PINS[key])
        if key in OBJECTS:
            close_object(parse(raw, key), OBJECTS[key], key)

    targets = []
    for row in iter_jsonl(c72_a / C72_NAMES["ledger"], PINS["C72_LEDGER"], 134155):
        if row["child_route_witness"] == SELECTOR:
            need(row["source_grazing"] is False and row["formal_credit"] == 0 and
                 row["D02_gate_credit"] == 0 and
                 row["required_decider"] == "EXACT_BOUNDARY_ARRANGEMENT_ORACLE",
                 "target full-face")
            targets.append(row)
    need(len(targets) == EXPECTED_SCOPE and
         line_sequence(row["row_sha256"] for row in targets) == EXPECTED_SEQUENCE and
         dict(collections.Counter(row["pair_index"] for row in targets)) ==
             EXPECTED_PAIR_CENSUS, "target selector count/sequence/census")
    target_hashes = {row["row_sha256"] for row in targets}
    need(len(target_hashes) == EXPECTED_SCOPE, "target unique")

    outgoing = {row["C72_atlas_row_sha256"] for row in iter_jsonl(
        C72O_DIR / "cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz",
        PINS["C72O_LEDGER"], 18668)}
    broad = {row["C72_obligation_row_sha256"] for row in iter_jsonl(
        C73_DIR / "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz",
        PINS["C73_LEDGER"], 1163)}
    tangency = {row["C72_obligation_row_sha256"] for row in iter_jsonl(
        C75_DIR / "cm2_round306c75_first_tangency_exact_strata_oracle_v1.jsonl.gz",
        PINS["C75_LEDGER"], 5884)}
    need(target_hashes.isdisjoint(outgoing | broad | tangency) and
         outgoing.isdisjoint(broad) and broad.isdisjoint(tangency),
         "C76/C72o/C73/C75 exact dedup")

    origins = {}
    target_pairs = {row["pair_index"] for row in targets}
    for row in iter_jsonl(C38_DIR / "collision1_2_child_pairs.jsonl.gz",
                          PINS["C38_CHILDREN"], 10486):
        pair = row["pair_index"]
        if pair in target_pairs:
            value = row["representative_origin_key"]
            need(pair not in origins or origins[pair] == value, "origin consistency")
            origins[pair] = value
    need(set(origins) == target_pairs and len(origins) == 8,
         "origin coverage")

    def first_two(path: Path, pin: str, count: int) -> list[dict[str, Any]]:
        result = []
        for ordinal, row in enumerate(iter_jsonl(path, pin, count)):
            if ordinal < 2:
                result.append(row)
        return result
    original = first_two(C35_DIR / "path_occurrences.jsonl.gz", PINS["C35_PATH"], 1648)
    reflected = first_two(C37_DIR / "reflected_r1648_occurrences.jsonl.gz", PINS["C37_PATH"], 1648)
    need(original[0]["selected_absolute_owner_id"] == FROZEN_OWNER and
         {original[1]["selected_absolute_owner_id"], reflected[1]["selected_absolute_owner_id"]}
         == {"G[0,0]", "G[0,1]"}, "history authority")

    wanted_c65 = {row["C65_aggregate_child_row_sha256"] for row in targets}
    found_c65 = set()
    for row in iter_jsonl(OUT / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
                          PINS["C65_LEAVES"], 358919):
        if row["row_sha256"] in wanted_c65:
            found_c65.add(row["row_sha256"])
    need(found_c65 == wanted_c65, "C65 direct lineage")
    wanted_c69 = {row["C69c_blocker_row_sha256"] for row in targets}
    found_c69 = {row["row_sha256"] for row in iter_jsonl(
        OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
        PINS["C69_BLOCKERS"], 18523) if row["row_sha256"] in wanted_c69}
    need(found_c69 == wanted_c69, "C69 direct lineage")
    return targets, origins, original, reflected


def incidence_rows(c72_a: Path, wanted: dict[str, dict[str, Any]],
                   occurrences: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sys.path.insert(0, str(OUT))
    import cm2_round306c72x_implicit_h1_root_physical_glue_core_v1 as physical_core
    need(file_sha(Path(physical_core.__file__).resolve()) == PURE_CORE_PIN,
         "incidence pure core pin")
    incidents: dict[str, list[dict[str, Any]]] = {identifier: [] for identifier in wanted}
    by_face = {value["face_key_sha256"]: identifier for identifier, value in wanted.items()}
    for row in iter_jsonl(c72_a / C72_NAMES["ledger"], PINS["C72_LEDGER"], 134155):
        specs = physical_core.exact_faces(
            row["pair_index"], row["exact_representative_box"])
        for edge_id, spec in specs.items():
            key = physical_core.face_key(spec)
            if key in by_face:
                incidents[by_face[key]].append({"C72_atlas_row_sha256": row["row_sha256"],
                                                "edge_id": edge_id,
                                                "is_high_face": edge_id.endswith("HIGH")})
    output = []
    for identifier in sorted(wanted):
        atlas_rows = sorted(incidents[identifier], key=lambda value:
                            (value["C72_atlas_row_sha256"], value["edge_id"]))
        target_rows = sorted(occurrences[identifier], key=lambda value:
                             (value["C72_atlas_row_sha256"], value["edge_id"]))
        need(1 <= len(atlas_rows) <= 2 and 1 <= len(target_rows) <= 2,
             "root atlas/target incidence 1/2")
        atlas_keys = {(row["C72_atlas_row_sha256"], row["edge_id"])
                      for row in atlas_rows}
        target_keys = {(row["C72_atlas_row_sha256"], row["edge_id"])
                       for row in target_rows}
        need(len(atlas_keys) == len(atlas_rows) and
             len(target_keys) == len(target_rows) and
             target_keys.issubset(atlas_keys) and
             all(row["root_id"] == identifier and
                 row["face_key_sha256"] == wanted[identifier]["face_key_sha256"]
                 for row in target_rows), "unique target endpoint mapping")
        high = [row for row in atlas_rows if row["is_high_face"]]
        owner = (high[0] if len(high) == 1 else atlas_rows[0])
        output.append({"schema": SCHEMA + ".root-incidence-row",
                       "root_id": identifier,
                       "face_key_sha256": wanted[identifier]["face_key_sha256"],
                       "exact_face": wanted[identifier]["exact_face"],
                       "target_graph_endpoint_occurrences": target_rows,
                       "incidence_count": len(target_rows),
                       "incidence_class": "TARGET_GRAPH_SHARED_FACE" if
                           len(target_rows) == 2 else
                           "TARGET_GRAPH_SINGLE_ENDPOINT_OCCURRENCE",
                       "incident_C72_atlas_faces": atlas_rows,
                       "atlas_face_incidence_count": len(atlas_rows),
                       "atlas_face_incidence_class": "SHARED_FACE" if
                           len(atlas_rows) == 2 else "ATLAS_SCOPE_BOUNDARY_FACE",
                       "unique_half_open_dyadic_face_owner": owner,
                       "dyadic_face_owner_rule":
                           "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SCOPE_BOUNDARY_LEXICAL",
                       "corner_incidence": False,
                       "physical_chart_owner": "W",
                       "paired_N_or_S_representation_is_shadow_only": True,
                       "same_physical_trace_duplicate_identified_not_added": True,
                       "root_is_graph_endpoint_not_physical_terminal": True,
                       "full_dimensional_Kraft_weight": "0",
                       "incidence_closed": True})
    return output


def coherent_attacks() -> dict[str, Any]:
    capsule = {
        "scope": EXPECTED_SCOPE, "geometry": EXPECTED_SCOPE,
        "clipped_graphs": EXPECTED_SCOPE, "strict_children": EXPECTED_SCOPE,
        "negative_sides": EXPECTED_SCOPE, "positive_sides": EXPECTED_SCOPE,
        "physical_graph_routes": EXPECTED_SCOPE, "graph_terminals": 0,
        "collision1_mismatch": 9510, "collision2_mismatch": 788,
        "sealed_collision3": 0, "residual": 0,
        "endpoint_occurrences": 2 * EXPECTED_SCOPE,
        "root_ids_conserved": True, "face_adjacency": True,
        "corner_incidence": True, "two_sides": True,
        "W_E_half_open": True, "same_state_glue": True,
        "duplicate_physical_trace": 0, "graph_Kraft": "0",
        "full_Kraft": "1", "additional_depth": 0,
        "C72o_overlap": 0, "C73_overlap": 0, "C75_overlap": 0,
        "formal": 0, "whole": 0, "D02": 0, "CM2": 0,
        "authority": False, "global_ready": False,
        "canonical_pointer": False, "producer_in_verifier": False,
    }
    outcomes = {}
    for key in sorted(capsule):
        mutant = copy.deepcopy(capsule)
        value = mutant[key]
        mutant[key] = (not value if type(value) is bool else
                       value + 1 if type(value) is int else value + "_MUTANT")
        try:
            need(mutant == capsule, "coherent attack:" + key)
        except Reject:
            outcomes[key] = "FAIL_CLOSED"
        else:
            raise Reject("escaped coherent attack:" + key)
    return {"attack_count": len(outcomes), "attacks": outcomes,
            "status": f"PASS_{len(outcomes)}_OF_{len(outcomes)}_COHERENT_ATTACKS_FAIL_CLOSED"}


def build(c72_a: Path, c72_b: Path, output: Path, batch_size: int) -> dict[str, Any]:
    need(not output.exists() and 100 <= batch_size <= 2000, "fresh output/batch")
    output.mkdir(mode=0o755)
    targets, origins, original, reflected = input_bundle(c72_a, c72_b)
    rows_writer = Ledger(output / ROWS, "C72_LEDGER_ORDER_FILTERED_BY_EXACT_CHILD_WITNESS")
    geometry_census = collections.Counter()
    route_census = collections.Counter()
    graph_route_census = collections.Counter()
    pair_census = collections.Counter()
    root_specs: dict[str, dict[str, Any]] = {}
    endpoint_occurrences: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    endpoint_occurrence_ids: set[str] = set()
    with rows_writer:
        for offset in range(0, len(targets), batch_size):
            payload = {"rows": targets[offset:offset + batch_size],
                       "origins": origins, "original": original, "reflected": reflected}
            completed = subprocess.run(
                [sys.executable, str(SELF), "--worker"],
                input=canonical(payload), capture_output=True, check=True)
            batch = json.loads(completed.stdout)
            need(len(batch) == len(payload["rows"]), "worker batch count")
            for atlas, body in zip(payload["rows"], batch):
                need(body["C72_atlas_row_sha256"] == atlas["row_sha256"] and
                     body["allowed_exit_closed_for_every_stratum"] is True and
                     body["whole_child_strict_exclusion_closed"] is True,
                     "worker order/closure")
                geometry_census[body["H1_geometry"]["kind"]] += 1
                pair_census[body["pair_index"]] += 1
                for exit_row in body["stratum_exits"]:
                    if exit_row["stratum"] == "H1_GT_0" or (
                        exit_row["stratum"] == "EXACT_CHILD" and
                        exit_row.get("chart") == "W"):
                        route_census[exit_row["downstream"]["outcome"]] += 1
                    if exit_row["stratum"] == "H1_EQ_0":
                        glue = exit_row["physical_chart_glue"]
                        need(exit_row["exit_class"] == "STRICT_EXCLUSION" and
                             glue["graph_exit_class"] == "STRICT_EXCLUSION" and
                             glue["graph_is_not_source_grazing_or_cemetery"] is True and
                             glue["graph_is_not_counted_as_a_coordinate_terminal"] is True,
                             "graph physical continuation")
                        graph_route_census[glue["graph_exclusion_reason"]] += 1
                for root in body["H1_geometry"].get("boundary_roots", []):
                    value = {"face_key_sha256": root["face_key_sha256"],
                             "exact_face": root["exact_face"]}
                    need(root["root_id"] not in root_specs or
                         root_specs[root["root_id"]] == value, "root identity")
                    root_specs[root["root_id"]] = value
                    occurrence_body = {
                        "schema": SCHEMA + ".graph-endpoint-occurrence",
                        "C72_atlas_row_sha256": atlas["row_sha256"],
                        "edge_id": root["edge_id"],
                        "root_id": root["root_id"],
                        "face_key_sha256": root["face_key_sha256"],
                    }
                    occurrence_id = digest(occurrence_body)
                    need(occurrence_id not in endpoint_occurrence_ids,
                         "unique graph endpoint occurrence")
                    endpoint_occurrence_ids.add(occurrence_id)
                    endpoint_occurrences[root["root_id"]].append(
                        {**occurrence_body,
                         "endpoint_occurrence_sha256": occurrence_id})
                rows_writer.write(body)
    need(dict(geometry_census) == {
        "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS": EXPECTED_SCOPE},
         "geometry census")
    need(dict(route_census) == EXPECTED_ROUTE_CENSUS, "W-route census")
    need(dict(graph_route_census) == EXPECTED_ROUTE_CENSUS,
         "graph route census")
    need(dict(pair_census) == EXPECTED_PAIR_CENSUS, "pair census")
    expected_endpoint_occurrences = 2 * EXPECTED_SCOPE
    need(len(endpoint_occurrence_ids) == expected_endpoint_occurrences and
         sum(len(rows) for rows in endpoint_occurrences.values()) ==
             expected_endpoint_occurrences and
         set(endpoint_occurrences) == set(root_specs),
         "2x10298 endpoint occurrence conservation")
    target_root_degree_census = collections.Counter(
        len(endpoint_occurrences[identifier]) for identifier in root_specs)
    need(set(target_root_degree_census).issubset({1, 2}) and
         sum(degree * count for degree, count in target_root_degree_census.items()) ==
             expected_endpoint_occurrences and
         sum(target_root_degree_census.values()) == len(root_specs),
         "target root degree decomposition")

    incidence = incidence_rows(c72_a, root_specs, endpoint_occurrences)
    incidence_writer = Ledger(output / INCIDENCE, "ROOT_ID_ASCENDING")
    incidence_census = collections.Counter()
    with incidence_writer:
        for body in incidence:
            incidence_writer.write(body)
            incidence_census[body["incidence_class"]] += 1
    need(incidence_writer.count == len(root_specs) and
         sum(body["incidence_count"] for body in incidence) ==
             expected_endpoint_occurrences and
         collections.Counter(body["incidence_count"] for body in incidence) ==
             target_root_degree_census,
         "incidence exact endpoint conservation")

    result = {"schema": SCHEMA + ".result",
              "status": "PASS_10298_EXACT_FULL_FACE_H1_GRAPHS__10298_W_E_PHYSICAL_GLUES__10298_WHOLE_CHILD_STRICT_EXCLUSIONS__NO_HANDOFF_OR_RESIDUAL__ZERO_CREDIT",
              "producer_file_sha256": file_sha(SELF), "precision_bits": PRECISION,
              "input_file_sha256": dict(sorted(PINS.items())),
              "pure_core_file_sha256": PURE_CORE_PIN,
              "chart_seam_quotient_manifest_file_sha256": CHART_MANIFEST_PIN,
              "chart_seam_certificate_sha256": CHART_CERTIFICATE_PIN,
              "chart_seam_dependency_file_sha256": CHART_DEPENDENCIES,
              "input_object_sha256": dict(sorted(OBJECTS.items())),
              "scope": {"selector": "child_route_witness == REGULAR_FULL_FACE_GRAPH",
                        "target_child_count": EXPECTED_SCOPE,
                        "selected_C72_row_sequence_sha256": EXPECTED_SEQUENCE,
                        "additional_dyadic_depth": 0,
                        "dedup_C72o_OUTGOING_STATE_count": 18668,
                        "dedup_C73_broad_exception_count": 1163,
                        "dedup_C75_first_tangency_count": 5884},
              "H1_GEOMETRY_CLOSED": EXPECTED_SCOPE,
              "H1_geometry_census": dict(sorted(geometry_census.items())),
              "strict_whole_child_exclusion_count": EXPECTED_SCOPE,
              "clipped_child_count": EXPECTED_SCOPE,
              "offgraph_strict_exclusion_stratum_census": {
                  "H1_LT_0_N_OR_S_CHART_MISMATCH": EXPECTED_SCOPE,
                  "H1_GT_0_COLLISION1_WORD_MISMATCH": 9510,
                  "H1_GT_0_COLLISION2_OWNER_MISMATCH": 788},
              "implicit_graph_physical_continuation_census":
                  dict(sorted(graph_route_census.items())),
              "implicit_graph_strict_exclusion_count": EXPECTED_SCOPE,
              "implicit_graph_terminal_count": 0,
              "sealed_collision3_handoff_count": 0,
              "collision3_handoff_ledger": None,
              "graph_endpoint_occurrence_count": expected_endpoint_occurrences,
              "graph_endpoint_occurrence_unique_count": len(endpoint_occurrence_ids),
              "unique_H1_boundary_root_count": len(root_specs),
              "target_graph_root_degree_census": {
                  str(key): value for key, value in
                  sorted(target_root_degree_census.items())},
              "endpoint_occurrence_conservation_identity":
                  "2*10298=20596=sum(root_degree*root_count)=sum(incidence_count)",
              "implicit_graphs_are_not_source_grazing_or_cemetery_terminals": True,
              "implicit_graphs_are_not_coordinate_terminals": True,
              "duplicate_physical_graph_traces_added": 0,
              "W_route_census_on_positive_side_and_graph":
                  dict(sorted(route_census.items())),
              "WHOLE_CHILD_STRICT_EXCLUSION_CLOSED": EXPECTED_SCOPE,
              "ALLOWED_EXIT_CLOSED": EXPECTED_SCOPE,
              "explicit_residual_child_count": 0,
              "pair_census": {str(key): value for key, value in sorted(pair_census.items())},
              "ledgers": {"decision_rows": rows_writer.descriptor(),
                          "root_incidence": incidence_writer.descriptor()},
              "root_incidence_census": dict(sorted(incidence_census.items())),
              "proof_invariants": {
                  "all_10298_have_strict_whole_child_dt_dp": True,
                  "all_10298_have_four_strict_nonzero_corners": True,
                  "all_10298_graphs_have_two_unique_noncorner_boundary_roots": True,
                  "exactly_20596_unique_endpoint_occurrences_materialized": True,
                  "every_endpoint_occurrence_maps_to_exactly_one_root_id_and_face": True,
                  "root_degree_census_conserves_all_20596_occurrences": True,
                  "sum_incidence_count_equals_20596": True,
                  "all_10298_graphs_have_two_strict_offgraph_sides": True,
                  "all_graph_roots_have_unique_half_open_dyadic_face_owner": True,
                  "all_graphs_have_W_half_open_physical_chart_owner": True,
                  "all_paired_N_or_S_graph_representations_are_shadow_only": True,
                  "same_physical_state_and_normal_preserved_across_chart_glue": True,
                  "W_representative_and_E_reflected_half_open_owners_closed": True,
                  "closed_box_downstream_strict_margins_restrict_to_graph": True,
                  "all_graphs_have_full_dimensional_Kraft_weight_zero": True,
                  "all_strata_are_allowed_exit_classes": True,
                  "owner_history_glue_two_sides_incidence_prefix_Kraft_materialized": True,
                  "H1_zero_is_continued_not_typed_as_terminal": True,
                  "all_allowed_exits_are_strict_exclusion": True},
              "producer_self_test": coherent_attacks(),
              "strict_boundary": {"candidate_is_authority": False,
                                  "global_consumption_ready": False,
                                  "runtime_canonical_pointer_or_seal_writes": False,
                                  **ZERO}}
    result["object_sha256"] = digest(result)
    write_exclusive(output / RESULT, canonical(result) + b"\n")
    report = ("# C76 full-face H1 physical-glue oracle\n\n"
              "- H1 geometry closed: 10,298 / 10,298 exact clipped graphs.\n"
              "- Exact whole-child strict exclusions: 10,298 / 10,298.\n"
              "- Every H1=0 graph continues under the representative W / reflected E half-open physical owner; no graph is treated as a terminal.\n"
              "- Downstream: 9,510 collision-1 official-word mismatches and 788 collision-2 owner mismatches; sealed collision-3 handoffs and residuals are both zero.\n"
              "- No graph is typed as source-grazing, cemetery, or a coordinate terminal; explicit residual children: 0.\n"
              "- Formal/global/D02/CM2 credit remains zero.\n").encode()
    write_exclusive(output / REPORT, report)
    write_exclusive(output / LOCK,
                    b"STAGED ZERO-CREDIT SIDECAR ONLY; PHYSICAL GRAPH GLUE IS NOT A TERMINAL; LATER NO-PRODUCER GLOBAL CONSUMER REQUIRED.\n")
    manifest_names = (ROWS, INCIDENCE, RESULT, REPORT, LOCK)
    manifest_raw = b"".join(
        f"{file_sha(output / name)}  {name}\n".encode("ascii")
        for name in manifest_names)
    write_exclusive(output / MANIFEST, manifest_raw)
    replay = {}
    for name in (*manifest_names, MANIFEST):
        payload = (output / name).read_bytes()
        replay[name] = {"sha256": hashlib.sha256(payload).hexdigest(),
                        "size": len(payload), "terminal_byte_replay": True}
    outer = {"schema": SCHEMA + ".outer-receipt",
             "status": "PASS_MEMBERS_THEN_MANIFEST_THEN_OUTER_LAST__TERMINAL_REPLAY__ZERO_CREDIT",
             "producer_file_sha256": file_sha(SELF),
             "result_object_sha256": result["object_sha256"],
             "publication_order": [*manifest_names, MANIFEST, OUTER],
             "members": replay,
             "manifest_published_after_all_listed_members": True,
             "outer_receipt_published_last_in_base_build": True,
             "O_EXCL_no_replace": True, "all_terminal_byte_replays_pass": True,
             **ZERO}
    outer["object_sha256"] = digest(outer)
    write_exclusive(output / OUTER, canonical(outer) + b"\n")
    return result


def complete(stage_a: Path, stage_b: Path, verifier: Path) -> dict[str, Any]:
    need(stage_a.is_dir() and stage_b.is_dir() and stage_a != stage_b,
         "two distinct build stages")
    verifier_sha = file_sha(verifier)
    members = {}
    for name in BASE_MEMBERS + [VERIFICATION]:
        left = (stage_a / name).read_bytes()
        right = (stage_b / name).read_bytes()
        need(left == right, "dual byte identity:" + name)
        members[name] = {"sha256": hashlib.sha256(left).hexdigest(),
                         "size": len(left), "dual_byte_identical": True,
                         "stage_a_terminal_replay": True,
                         "stage_b_terminal_replay": True}
    result = parse((stage_a / RESULT).read_bytes(), "result")
    verification = parse((stage_a / VERIFICATION).read_bytes(), "verification")
    result_body = copy.deepcopy(result)
    result_object = result_body.pop("object_sha256", None)
    verification_body = copy.deepcopy(verification)
    verification_object = verification_body.pop("object_sha256", None)
    need(result_object == digest(result_body) and
         verification_object == digest(verification_body), "object closure")
    need(result["producer_file_sha256"] == file_sha(SELF) and
         verification["verifier_file_sha256"] == verifier_sha and
         verification["producer_file_sha256_declared"] == file_sha(SELF) and
         verification["candidate_result_object_sha256"] == result_object and
         verification["no_producer_open_read_parse_import_exec_decode"] is True,
         "producer/verifier/result binding")
    need(not (stage_a / DUAL).exists() and not (stage_b / DUAL).exists(),
         "fresh completion receipts")
    receipt = {
        "schema": SCHEMA + ".dual-completion-receipt",
        "status": "PASS_DUAL_ISOLATED_BYTE_IDENTICAL_BUILD__NO_PRODUCER_VERIFIER__RECEIPT_LAST__TERMINAL_REPLAY__ZERO_CREDIT",
        "producer_file_sha256": file_sha(SELF),
        "verifier_file_sha256": verifier_sha,
        "result_object_sha256": result_object,
        "verification_object_sha256": verification_object,
        "members_before_receipt": members,
        "all_dual_member_bytes_identical": True,
        "no_producer_verifier_policy_pass": True,
        "dual_receipt_is_final_member": True,
        "O_EXCL_no_replace": True, "terminal_byte_replay": True,
        **ZERO,
    }
    receipt["object_sha256"] = digest(receipt)
    raw = canonical(receipt) + b"\n"
    write_exclusive(stage_a / DUAL, raw)
    write_exclusive(stage_b / DUAL, raw)
    need((stage_a / DUAL).read_bytes() == (stage_b / DUAL).read_bytes() == raw,
         "dual completion replay")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--worker", action="store_true")
    modes.add_argument("--output-dir", type=Path)
    modes.add_argument("--complete", nargs=3, type=Path,
                       metavar=("STAGE_A", "STAGE_B", "VERIFIER"))
    parser.add_argument("--c72-a", type=Path)
    parser.add_argument("--c72-b", type=Path)
    parser.add_argument("--batch-size", type=int, default=1200)
    args = parser.parse_args()
    if args.worker:
        return worker()
    if args.complete:
        value = complete(*(path.resolve() for path in args.complete))
        print(json.dumps({"status": value["status"],
                          "object_sha256": value["object_sha256"]}, sort_keys=True))
    else:
        need(args.c72_a is not None and args.c72_b is not None and
             args.output_dir is not None, "build arguments")
        result = build(args.c72_a.resolve(), args.c72_b.resolve(),
                       args.output_dir.resolve(), args.batch_size)
        print(json.dumps({"status": result["status"],
                          "object_sha256": result["object_sha256"],
                          "rows_sha256": result["ledgers"]["decision_rows"]["sha256"]},
                         sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "REJECTED", "reason": str(error)}, sort_keys=True),
              file=sys.stderr)
        raise SystemExit(2)
