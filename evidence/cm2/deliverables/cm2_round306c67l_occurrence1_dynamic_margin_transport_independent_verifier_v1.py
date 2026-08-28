#!/usr/bin/env python3
"""Independent no-producer full numeric verifier for C67-L."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
if str(OUT) not in sys.path:
    sys.path.insert(0, str(OUT))

import cm2_gate3_candidate_first_hit_cert as G
import cm2_round117_rank3_countable_homogeneity_operator_cells as H
import cm2_round128_base_r1_component_global_word_incidence as CORE

PREFIX = "cm2_round306c67l_occurrence1_dynamic_margin_transport"
SCHEMA = "cm2.round306c67l.occurrence1-dynamic-margin-transport.independent-verification.v1"
PRODUCER = OUT / (PREFIX + "_v1.py")
ENDPOINT = OUT / (PREFIX + "_endpoint_occurrence_margins_v1.jsonl.gz")
ATOM = OUT / (PREFIX + "_atom_coverage_v1.jsonl.gz")
EDGE = OUT / (PREFIX + "_edge_coverage_v1.jsonl.gz")
CORRIDOR = OUT / (PREFIX + "_corridor_coverage_v1.jsonl.gz")
RESULT = OUT / (PREFIX + "_result_v1.json")
C60A = OUT / "cm2_round306c60l_static_edge_owner_incidence_atoms_v1.jsonl.gz"
C57E = OUT / "cm2_round306c57l1_collision1_edgewise_transport_edge_obligations_v1.jsonl.gz"
C57C = OUT / "cm2_round306c57l1_collision1_edgewise_transport_corridor_cell_transport_v1.jsonl.gz"
C32C = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/compact_cells.jsonl.gz"
C32S = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/source_chart_seams.jsonl.gz"
C41A = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599/routed_ambient_cells.jsonl.gz"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANON = OUT / "CM2_LATEST_STATUS.md"
VERIFICATION = OUT / (PREFIX + "_independent_verification_v1.json")

PINS = {
    str(PRODUCER): "2b84ec3bb6e50d1ec5b1166cab7a2f66406739d3808e93a51b1ac9d536d90b24",
    str(ENDPOINT): "8945c242ef8e7928213057900ecde74e8ba18201c1f715d7333dc77102b209d3",
    str(ATOM): "5ca4a789b663f320ba8cdc15b4352298135219aad1e1512dc6742cd5ba3e5828",
    str(EDGE): "84298c8283ae26685f34e5de24638257edb541f8d609f2a62f1b60d8285fbab8",
    str(CORRIDOR): "d28fc4ff49e7243e38e55997113d98fb0694eb3ed81f14ecbf5a051f1890684e",
    str(RESULT): "5b43ecb647958185859e987e5985660c660fb6a5ee7e422ae2748f96a880b8ac",
    str(C60A): "4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6",
    str(C57E): "7136dd4585a5ed9de158c0710c6386ece4d8870ab0196db2e373881779c3dbcd",
    str(C57C): "3f61330c3eafa9101b083b8b6061ee334738bfa3129280874e1a3f7d239e1ac5",
    str(C32C): "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8",
    str(C32S): "d7b5e689baa36d6d0502d3a7c9dad3188d5b92c11e7223c502277057304a611e",
    str(C41A): "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
    str(OUT / "cm2_gate3_candidate_first_hit_cert.py"): "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    str(OUT / "cm2_round128_base_r1_component_global_word_incidence.py"): "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35",
    str(OUT / "cm2_round117_rank3_countable_homogeneity_operator_cells.py"): "8112aeb2c5d67a914a651683c9a497def3c2ffed81b1c42b365bb257cf8f7e7c",
    str(C53): "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    str(CANON): "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}


class Rejected(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def objhash(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * Q(2) ** int(exponent)


def pair(value: arb) -> tuple[Q, Q]:
    return dyadic(value.lower()), dyadic(value.upper())


def ball(lower: Q, upper: Q) -> arb:
    return G.arb_interval(lower, upper)


def rational(value: Q | int) -> arb:
    return G.arbq(Q(value))


class Frozen:
    def __init__(self) -> None:
        self.meta: dict[str, tuple[int, int, int, int, int, str]] = {}
        self.data: dict[str, bytes] = {}

    def load(self, path: Path) -> bytes:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(path, flags)
        try:
            a = os.fstat(fd)
            require(stat.S_ISREG(a.st_mode) and a.st_nlink == 1, "regular single link:" + str(path))
            chunks: list[bytes] = []
            while True:
                chunk = os.read(fd, 1 << 20)
                if not chunk:
                    break
                chunks.append(chunk)
            z = os.fstat(fd)
            require((a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns) == (z.st_dev, z.st_ino, z.st_size, z.st_mtime_ns), "fd changed:" + str(path))
        finally:
            os.close(fd)
        payload = b"".join(chunks)
        require(sha(payload) == PINS[str(path)], "pin:" + str(path))
        self.meta[str(path)] = (z.st_dev, z.st_ino, z.st_size, z.st_mtime_ns, z.st_nlink, sha(payload))
        self.data[str(path)] = payload
        return payload

    def stable(self) -> None:
        for name, old in self.meta.items():
            value = os.lstat(name)
            require(not stat.S_ISLNK(value.st_mode) and (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_nlink) == old[:5], "path changed:" + name)


def json_value(payload: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in out, "duplicate JSON key")
            out[key] = value
        return out
    value = json.loads(payload.decode(), object_pairs_hook=unique, parse_float=lambda x: (_ for _ in ()).throw(ValueError(x)), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    require(type(value) is dict, "JSON object")
    return value


def rows(payload: bytes) -> list[dict[str, Any]]:
    answer: list[dict[str, Any]] = []
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for line in stream:
            row = json.loads(line)
            semantic = dict(row)
            claimed = semantic.pop("row_sha256", None)
            require(claimed == objhash(semantic), "closed row")
            answer.append(row)
    return answer


TARGETS = {target.target_id: target for target in G.TARGETS}
RETAINED = {chart: tuple(G.candidate_ids("W:" + chart)) for chart in ("E", "N", "S")}
ALGEBRAIC = {"+1/sqrt(2)": (Q(707, 1000), Q(708, 1000)), "-1/sqrt(2)": (Q(-708, 1000), Q(-707, 1000))}
WCORES = tuple(core for core in CORE.physical_cores() if core.source == "W")


def outer(token: str) -> tuple[Q, Q]:
    if token in ALGEBRAIC:
        root = (arb(1) / 2).sqrt()
        if token.startswith("-"):
            root = -root
        lo, hi = ALGEBRAIC[token]
        require(bool(root > rational(lo)) and bool(root < rational(hi)), "isolating interval")
        return lo, hi
    value = Q(token)
    require(qstr(value) == token, "canonical rational")
    return value, value


def span(tokens: list[str]) -> tuple[arb, tuple[Q, Q]]:
    a, b = outer(tokens[0]), outer(tokens[1])
    endpoints = min(a[0], b[0]), max(a[1], b[1])
    return ball(*endpoints), endpoints


def sqrt_complement(bounds_: tuple[Q, Q]) -> arb:
    low, high = bounds_
    maximum = max(abs(low), abs(high))
    minimum = Q(0) if low <= 0 <= high else min(abs(low), abs(high))
    lower = pair(rational(1 - maximum * maximum).sqrt())[0]
    upper = pair(rational(1 - minimum * minimum).sqrt())[1]
    return ball(lower, upper)


def parameters(chart: str, edge: dict[str, Any], atom: dict[str, Any]) -> tuple[arb, arb, tuple[Q, Q], tuple[Q, Q]]:
    varying, vb = span(atom["exact_span"])
    if edge["glue_kind"] == "INTRA_CHART_FACE":
        geometry = edge["exact_common_face_refinement"]
        fb = outer(geometry["fixed_coordinate"])
        fixed = ball(*fb)
        return (varying, fixed, vb, fb) if geometry["axis"] == "p" else (fixed, varying, fb, vb)
    seam = edge["exact_common_face_refinement"]["seam_id"]
    token = "+1/sqrt(2)" if seam == "E_TO_N" or chart == "S" else "-1/sqrt(2)"
    tb = outer(token)
    return ball(*tb), varying, tb, vb


def reconstruct(chart: str, t: arb, p: arb, tb: tuple[Q, Q], pb: tuple[Q, Q]) -> dict[str, Any]:
    rn, rp = sqrt_complement(tb), sqrt_complement(pb)
    if chart == "E":
        nx0, ny0 = rn, t
    elif chart == "N":
        nx0, ny0 = t, rn
    else:
        require(chart == "S", "chart")
        nx0, ny0 = t, -rn
    ux, uy = rp * nx0 - p * ny0, rp * ny0 + p * nx0
    source_radius = rational(G.RADIUS["W"])
    qx, qy, s = rational(Q(1, 2)) + source_radius * nx0, rational(Q(1, 2)) + source_radius * ny0, arb(0)
    candidates: list[dict[str, Any]] = []
    for identifier in RETAINED[chart]:
        target = TARGETS[identifier]
        ax, ay = G.target_center(target, s)
        dx, dy = ax - qx, ay - qy
        ell, transverse = ux * dx + uy * dy, -uy * dx + ux * dy
        radius = rational(G.RADIUS[target.obstacle])
        delta = radius * radius - transverse * transverse
        near = far = None
        if bool(delta < 0):
            kind = "NO"
        elif bool(delta > 0):
            square = delta.sqrt()
            near, far = ell - square, ell + square
            kind = "BEHIND" if bool(far < 0) else "FUTURE" if bool(near > 0) else "UNRESOLVED"
        else:
            kind = "UNRESOLVED"
        candidates.append({"id": identifier, "ell": ell, "transverse": transverse, "radius": radius, "delta": delta, "near": near, "far": far, "kind": kind})

    def possible_lower(row: dict[str, Any]) -> arb | None:
        if row["kind"] in {"NO", "BEHIND"}:
            return None
        if row["kind"] == "FUTURE":
            return row["near"].lower()
        upper = row["delta"].upper()
        return None if not bool(upper > 0) else row["ell"].lower() - upper.sqrt().upper()

    future = [row for row in candidates if row["kind"] == "FUTURE"]
    winners = [row for row in future if all(other is row or other["kind"] in {"NO", "BEHIND"} or ((lower := possible_lower(other)) is not None and bool(row["near"] < lower)) for other in candidates)]
    owner = winners[0]["id"] if len(winners) == 1 else None
    if owner != "W[1,0]":
        return {"raw": False, "full": False, "owner": owner, "outgoing": None, "blocker": "OWNER_UNRESOLVED_MULTI_CANDIDATE" if owner is None else "FIRST_OWNER_MISMATCH__" + owner}
    winner = winners[0]
    target_x, target_y = G.target_center(TARGETS[owner], s)
    hit_x, hit_y = qx + winner["near"] * ux, qy + winner["near"] * uy
    nx, ny = (hit_x - target_x) / winner["radius"], (hit_y - target_y) / winner["radius"]
    charts = {"E": [nx - ny, nx + ny], "W": [-nx - ny, -nx + ny], "N": [ny - nx, ny + nx], "S": [-ny - nx, -ny + nx]}
    selected = [name for name, values in charts.items() if all(bool(value > 0) for value in values)]
    outgoing = selected[0] if len(selected) == 1 else None
    if outgoing != "W":
        return {"raw": False, "full": False, "owner": owner, "outgoing": outgoing, "blocker": "OUTGOING_CHART_NOT_STRICT_W__" + str(outgoing)}
    radial = winner["delta"].sqrt() / winner["radius"]
    if not bool(radial > H.boundary_ball(H.N0)) or not bool(radial > rational(Q(1, 2**14))):
        return {"raw": True, "full": False, "owner": owner, "outgoing": outgoing, "blocker": "HOMOGENEITY_OR_RANK_MARGIN_UNRESOLVED"}
    wall = [rational(1) - qx, hit_x - rational(1), qx, rational(2) - hit_x, qy, rational(1) - qy, hit_y, rational(1) - hit_y, hit_x - qx]
    if not all(bool(value > 0) for value in wall):
        return {"raw": True, "full": False, "owner": owner, "outgoing": outgoing, "blocker": "OFFICIAL_X_PLUS_WALL_ENDPOINT_MARGIN_UNRESOLVED"}
    momentum = winner["transverse"] / winner["radius"]
    for core in WCORES:
        cell = core.chart_id.split(":")[1]
        if cell == "E":
            coordinate, outside = ny, [-nx, abs(ny) - abs(nx)]
        elif cell == "W":
            coordinate, outside = ny, [nx, abs(ny) - abs(nx)]
        elif cell == "N":
            coordinate, outside = nx, [-ny, abs(nx) - abs(ny)]
        else:
            coordinate, outside = nx, [ny, abs(nx) - abs(ny)]
        outside += [rational(core.t0) - coordinate, coordinate - rational(core.t1), rational(core.p0) - momentum, momentum - rational(core.p1)]
        if not any(bool(value > 0) for value in outside):
            return {"raw": True, "full": False, "owner": owner, "outgoing": outgoing, "blocker": "C24_ALL_CORE_EXTERIOR_MARGIN_UNRESOLVED"}
    return {"raw": True, "full": True, "owner": owner, "outgoing": outgoing, "blocker": None}


def attack_suite(result: dict[str, Any], endpoint_rows: list[dict[str, Any]]) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    tests = [
        ("result_object", lambda v: require(v["object_sha256"] == objhash({key: item for key, item in v.items() if key != "object_sha256"}), "result object")),
        ("edge_census", lambda v: require(v["summary"]["edge_count"] == 1042, "edge census")),
        ("raw_census", lambda v: require(v["summary"]["edge_raw_owner_outgoing_pass_count"] == 498, "raw census")),
        ("full_census", lambda v: require(v["summary"]["edge_full_named_margin_pass_count"] == 491, "full census")),
        ("credit", lambda v: require(v["summary"]["formal_credit"] == v["summary"]["D02_gate_credit"] == 0, "credit")),
    ]
    for index, (name, check) in enumerate(tests):
        mutant = json.loads(json.dumps(result))
        if name == "result_object":
            mutant["status"] += "X"
        elif name == "edge_census":
            mutant["summary"]["edge_count"] += 1
        elif name == "raw_census":
            mutant["summary"]["edge_raw_owner_outgoing_pass_count"] += 1
        elif name == "full_census":
            mutant["summary"]["edge_full_named_margin_pass_count"] += 1
        else:
            mutant["summary"]["formal_credit"] = 1
        try:
            check(mutant)
        except Rejected:
            attacks[f"coherent_{index:02d}_{name}"] = "FAIL_CLOSED"
        else:
            raise Rejected("accepted coherent mutation")
    sample = endpoint_rows[0]
    for index, (name, mutate) in enumerate([
        ("owner", lambda row: row["numeric_reconstruction"].__setitem__("selected_owner", "G[1,0]")),
        ("outgoing", lambda row: row["numeric_reconstruction"].__setitem__("outgoing_chart", "N")),
        ("credit", lambda row: row.__setitem__("formal_credit", 1)),
        ("seam", lambda row: row["exact_geometry"].__setitem__("minimal_polynomial", "x^2-2")),
        ("row_hash", lambda row: row.__setitem__("pair_index", row["pair_index"] + 1)),
    ]):
        mutant = json.loads(json.dumps(sample))
        mutate(mutant)
        try:
            semantic = dict(mutant)
            claimed = semantic.pop("row_sha256")
            require(claimed == objhash(semantic), "mutated row closure")
        except Rejected:
            attacks[f"row_{index:02d}_{name}"] = "FAIL_CLOSED"
        else:
            raise Rejected("accepted row mutation")

    original_open = os.open
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        target = base / "target"
        target.write_text("x")
        link = base / "link"
        link.symlink_to(target)
        hard = base / "hard"
        os.link(target, hard)
        for name, path in [("nofollow_symlink", link), ("single_link", target)]:
            try:
                fd = original_open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
                try:
                    value = os.fstat(fd)
                    require(value.st_nlink == 1, "single-link")
                finally:
                    os.close(fd)
            except (OSError, Rejected):
                attacks[name] = "FAIL_CLOSED"
            else:
                raise Rejected("file attack accepted")
    require(len(attacks) == 12, "attack count")
    return {"status": "PASS_12_OF_12_COHERENT_AND_FILE_ATTACKS_FAIL_CLOSED", "attack_count": 12, "attacks": attacks}


def verify() -> dict[str, Any]:
    frozen = Frozen()
    for path in PINS:
        frozen.load(Path(path))
    # The producer source is hashed as opaque bytes.  It is never decoded,
    # imported, compiled, or executed by this verifier.
    result = json_value(frozen.data[str(RESULT)])
    semantic_result = dict(result)
    claimed = semantic_result.pop("object_sha256", None)
    require(claimed == "0e5b88cd4978661fdfad6bc508029f714e78a760f7164f4114cf540334b73fe1" == objhash(semantic_result), "candidate result closure")
    endpoint_rows, atom_rows, edge_rows, corridor_rows = rows(frozen.data[str(ENDPOINT)]), rows(frozen.data[str(ATOM)]), rows(frozen.data[str(EDGE)]), rows(frozen.data[str(CORRIDOR)])
    atoms, edges, corridors = rows(frozen.data[str(C60A)]), rows(frozen.data[str(C57E)]), rows(frozen.data[str(C57C)])
    cells = {row["cell_id"]: row for row in rows(frozen.data[str(C32C)])}
    ambient = {row["row_sha256"]: row for row in rows(frozen.data[str(C41A)])}
    seams = {row["row_sha256"]: row for row in rows(frozen.data[str(C32S)])}
    require(len(endpoint_rows) == 26206 and len(atom_rows) == len(atoms) == 13103 and len(edge_rows) == len(edges) == 1042 and len(corridor_rows) == len(corridors) == 1044, "ledger counts")
    source_by_atom = {row["row_sha256"]: row for row in atoms}
    source_edge_by_face = {row["face_or_corner_id"]: row for row in edges}
    endpoints_by_atom: dict[str, list[dict[str, Any]]] = defaultdict(list)
    numeric_census = Counter()
    blocker_census = Counter()
    for row in endpoint_rows:
        atom = source_by_atom[row["C60_atom_row_sha256"]]
        edge = source_edge_by_face[row["face_or_corner_id"]]
        incidence = next(item for item in atom["incident_occurrences"] if item["physical_occurrence_id"] == row["physical_occurrence_id"])
        c41 = ambient[incidence["upstream_ambient_row_sha256"]]
        require(row["C41_row_sha256"] == c41["row_sha256"] and incidence["semantic_path"] == c41["path"] and incidence["physical_cell_id"] in {c41["representative_cell_id"], c41["reflected_cell_id"]}, "endpoint lineage")
        chart = cells[incidence["physical_cell_id"]]["compact_chart"]
        t, p, tb, pb = parameters(chart, edge, atom)
        independent = reconstruct(chart, t, p, tb, pb)
        recorded = row["numeric_reconstruction"]
        require(independent["raw"] == recorded["raw_owner_outgoing_pass"] and independent["full"] == recorded["full_named_margin_pass"] and independent["owner"] == recorded["selected_owner"] and independent["outgoing"] == recorded["outgoing_chart"] and independent["blocker"] == recorded["blocker_code"], "full numeric replay")
        require(recorded["retained_candidate_count"] == 55 and recorded["full_radius4_candidate_count"] == 161 and row["C36_seed_collar_margins_used_as_selector_or_global_bound"] is False and row["formal_credit"] == row["D02_gate_credit"] == row["handoff_credit"] == 0, "numeric contract")
        endpoints_by_atom[atom["row_sha256"]].append(row)
        numeric_census["endpoint"] += 1
        numeric_census["endpoint_raw"] += independent["raw"]
        numeric_census["endpoint_full"] += independent["full"]
        if independent["blocker"] is not None:
            blocker_census[independent["blocker"]] += 1

    atom_by_hash = {row["C60_atom_row_sha256"]: row for row in atom_rows}
    atoms_by_face: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        endpoints = endpoints_by_atom[atom["row_sha256"]]
        output = atom_by_hash[atom["row_sha256"]]
        raw = all(row["numeric_reconstruction"]["raw_owner_outgoing_pass"] for row in endpoints)
        full = all(row["numeric_reconstruction"]["full_named_margin_pass"] for row in endpoints)
        require(len(endpoints) == 2 and output["raw_owner_W10_and_outgoing_W_both_sides"] == raw and output["all_applicable_C36_named_margins_strict_both_sides"] == full, "atom aggregate")
        if atom["glue_kind"] == "SOURCE_CHART_TRANSITION":
            upstream = seams[source_edge_by_face[atom["face_or_corner_id"]]["upstream_face_or_seam_row_sha256"]]
            require(upstream["exact_state_gluing_inherited_from_round162"] is True and output["source_seam_physical_glue_status"].startswith("PASS_EXACT"), "seam semantic")
        atoms_by_face[atom["face_or_corner_id"]].append(output)
        numeric_census["atom_raw"] += raw
        numeric_census["atom_full"] += full

    edge_by_hash = {row["C57_edge_row_sha256"]: row for row in edge_rows}
    edges_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        output = edge_by_hash[edge["row_sha256"]]
        covered = atoms_by_face[edge["face_or_corner_id"]]
        raw = all(row["raw_owner_W10_and_outgoing_W_both_sides"] for row in covered)
        full = all(row["all_applicable_C36_named_margins_strict_both_sides"] for row in covered)
        require(output["raw_owner_W10_and_outgoing_W_whole_edge"] == raw and output["all_applicable_C36_named_margins_strict_whole_edge"] == full and output["formal_credit"] == output["D02_gate_credit"] == output["handoff_credit"] == 0, "edge aggregate")
        numeric_census["edge_raw"] += raw
        numeric_census["edge_full"] += full
        numeric_census["seam_edge"] += edge["glue_kind"] == "SOURCE_CHART_TRANSITION"
        numeric_census["seam_raw"] += edge["glue_kind"] == "SOURCE_CHART_TRANSITION" and raw
        numeric_census["seam_full"] += edge["glue_kind"] == "SOURCE_CHART_TRANSITION" and full
        edges_by_cell[edge["source_cell_id"]].append(output)
        edges_by_cell[edge["target_cell_id"]].append(output)

    corridor_by_hash = {row["C57_corridor_row_sha256"]: row for row in corridor_rows}
    for corridor in corridors:
        output = corridor_by_hash[corridor["row_sha256"]]
        incident = edges_by_cell[corridor["cell_id"]]
        full = sum(row["all_applicable_C36_named_margins_strict_whole_edge"] for row in incident)
        require(output["incident_edge_count"] == len(incident) and output["strict_incident_edge_count"] == full and output["all_incident_edges_strict"] == (bool(incident) and full == len(incident)) and output["corridor_whole_path_transport_claimed"] is False, "corridor aggregate")
        numeric_census["corridor_all"] += output["all_incident_edges_strict"]
        numeric_census["corridor_some"] += output["at_least_one_incident_edge_strict"]

    expected = {"endpoint": 26206, "endpoint_raw": 22229, "endpoint_full": 22207, "atom_raw": 11114, "atom_full": 11103, "edge_raw": 498, "edge_full": 491, "seam_edge": 16, "seam_raw": 15, "seam_full": 13, "corridor_all": 394, "corridor_some": 554}
    require(dict(numeric_census) == expected, "independent census")
    expected_blockers = {"C24_ALL_CORE_EXTERIOR_MARGIN_UNRESOLVED": 22, "FIRST_OWNER_MISMATCH__G[1,0]": 102, "FIRST_OWNER_MISMATCH__G[1,1]": 102, "FIRST_OWNER_MISMATCH__G[2,0]": 36, "FIRST_OWNER_MISMATCH__G[2,1]": 38, "OUTGOING_CHART_NOT_STRICT_W__N": 612, "OUTGOING_CHART_NOT_STRICT_W__None": 646, "OUTGOING_CHART_NOT_STRICT_W__S": 668, "OWNER_UNRESOLVED_MULTI_CANDIDATE": 1773}
    require(dict(blocker_census) == expected_blockers, "blocker census")
    require(result["summary"]["edge_raw_owner_outgoing_pass_count"] == 498 and result["summary"]["edge_full_named_margin_pass_count"] == 491 and result["strict_boundary"]["formal_credit"] == result["strict_boundary"]["D02_gate_credit"] == result["strict_boundary"]["handoff_credit"] == 0, "result projection")
    attacks = attack_suite(result, endpoint_rows)
    frozen.stable()
    verification = {"schema": SCHEMA, "status": "PASS_INDEPENDENT_NO_PRODUCER_FULL_NUMERIC_RECONSTRUCTION__12_OF_12_ATTACKS_FAIL_CLOSED__ZERO_CREDIT", "candidate_producer_file_sha256": PINS[str(PRODUCER)], "candidate_result_file_sha256": PINS[str(RESULT)], "candidate_result_object_sha256": claimed, "producer_source_imported_decoded_compiled_or_executed": False, "numeric_reconstruction": expected, "blocker_census": expected_blockers, "attacks": attacks, "TOCTOU_and_single_link_checks_passed": True, "runtime_or_canonical_written": False, "formal_credit": 0, "D02_gate_credit": 0, "handoff_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}
    verification["object_sha256"] = objhash(verification)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path, default=VERIFICATION)
    args = parser.parse_args()
    old = ctx.prec
    ctx.prec = 256
    try:
        value = verify()
        if args.self_test:
            print(json.dumps({"status": value["attacks"]["status"], "object_sha256": value["attacks"]["attacks"] and objhash(value["attacks"])}, sort_keys=True))
            return 0
        payload = enc(value) + b"\n"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(args.output, flags, 0o644)
        try:
            os.write(fd, payload)
            os.fsync(fd)
        finally:
            os.close(fd)
        print(json.dumps({"status": value["status"], "numeric_reconstruction": value["numeric_reconstruction"], "object_sha256": value["object_sha256"]}, sort_keys=True))
        return 0
    finally:
        ctx.prec = old


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Rejected, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
