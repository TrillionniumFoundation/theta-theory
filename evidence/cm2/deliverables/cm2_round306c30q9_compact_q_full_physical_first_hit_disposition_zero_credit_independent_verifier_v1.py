#!/usr/bin/env python3
"""No-import independent verifier for the append-only zero-credit C30q9 gate."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any

from flint import arb, ctx


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
SCHEMA = "cm2.round306c30q9.independent-verification.zero-credit.v1"
EXPECTED_RESULT_SHA256 = "9102308165cefc800321b859a7e9f87db503b9b9d61f99feafc637ac2677cb23"
K, RW, RG = Q(1023, 262144), Q(4, 25), Q(9, 25)
PINS = {
    ROOT / ".cm2-runtime/audit/c30q8-full-54-global-template-zero-credit-v1-20260808T112500Z/manifest.sha256":
        "2105ce1e7e898a33a3beb05063f203799e10430a4d5498a47e1e4db744c60a73",
    ROOT / ".cm2-runtime/audit/c30q8-full-54-global-template-zero-credit-v1-20260808T112500Z/receipt.json":
        "760a21c62bc22820b1a03cd5b72aa61d776ff7d7860d0926c1bfc11305383a1c",
    ROOT / ".cm2-runtime/audit/c30q8-full-54-global-template-zero-credit-v1-20260808T112500Z/producer_seed30880079_stdout.json":
        "e15cbad0515af501d2d5be2d7c01b9f5d77bd97598b7c6f0efef7e513efcdb1c",
    ROOT / "deliverables/cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    ROOT / "deliverables/cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py":
        "f1297881f724cb0a2087ebbfa6961a95750dffa751c003879eb2e14714581796",
    ROOT / "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_producer.py":
        "003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762",
}
Q8_MANIFEST = next(path for path in PINS if path.name == "manifest.sha256")
Q8_RECEIPT = next(path for path in PINS if path.name == "receipt.json")
Q8_CANDIDATE = next(path for path in PINS if path.name == "producer_seed30880079_stdout.json")

BRIDGE = ("03.15.11110101",)
MISS = ("06.00.00101010", "06.00.10000000", "06.00.10000010")
ROUTE = ("04.00.00001010", "04.00.00100000", "04.00.00100010",
         "04.00.00101000", "04.00.00101010", "04.00.10000000")
SWITCH = {token: (Q(1, 2) if index < 3 else Q(63, 64))
          for index, token in enumerate(ROUTE)}
LIVE_T = {
    "04.00.00100000": Q(27789, 512000),
    "04.00.00100010": Q(28497, 512000),
    "04.00.00101000": Q(34161, 512000),
    "04.00.00101010": Q(1593, 20480),
    "04.00.10000000": Q(45489, 512000),
}
T1 = ("G[0,0]", "G[0,1]", "G[1,0]", "G[1,1]", "W[-1,0]",
      "W[0,-1]", "W[0,0]", "W[0,1]", "W[1,0]")
T32 = ("G[-1,0]", "G[-1,1]", "G[0,-1]", "G[0,0]", "G[0,1]", "G[0,2]",
       "G[1,-1]", "G[1,0]", "G[1,1]", "G[1,2]", "G[2,0]", "G[2,1]",
       "W[-1,-1]", "W[-1,0]", "W[-1,1]", "W[0,-1]", "W[0,0]",
       "W[0,1]", "W[1,-1]", "W[1,0]", "W[1,1]")


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


def safe_read(path: Path) -> bytes:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical input:" + str(path))
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link input:" + str(path))
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
              "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")
    need(all(getattr(before, field) == getattr(after, field) for field in fields),
         "stable input:" + str(path))
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate key:" + label)
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique,
                           parse_float=lambda token: token,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    return value


def verify_pins_and_manifest() -> None:
    for path, expected in PINS.items():
        need(hashlib.sha256(safe_read(path)).hexdigest() == expected, "pin:" + path.name)
    base = Q8_MANIFEST.parent
    seen: set[str] = set()
    for row in safe_read(Q8_MANIFEST).decode("ascii", "strict").splitlines():
        need(len(row) >= 67 and row[64:66] == "  ", "Q8 manifest syntax")
        expected, member = row[:64], row[66:]
        part = Path(member)
        need(all(char in "0123456789abcdef" for char in expected)
             and not part.is_absolute() and ".." not in part.parts and member not in seen,
             "Q8 manifest row")
        seen.add(member)
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        need(target.absolute().is_relative_to(ROOT)
             and hashlib.sha256(safe_read(target)).hexdigest() == expected,
             "Q8 manifest member:" + member)
    need(bool(seen), "nonempty Q8 manifest")


def origins(tokens: tuple[str, ...]) -> list[str]:
    return sorted(key for token in tokens for key in ("W:N:" + token, "W:S:H." + token))


def token_of(origin: str) -> str:
    return origin.split(":")[-1].removeprefix("H.")


def aq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def iv(lower: Q, upper: Q) -> arb:
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return aq(middle) + arb(0, aq(radius).upper())


def hydrate(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["tq"] = tuple(Q(value) for value in row["t_domain"])
    result["sq"] = tuple(Q(value) for value in row["s_domain"])
    need(result["sq"] == (Q(-1, 400), Q(1, 400)), "s domain")
    return result


def target(target_id: str, s: arb) -> tuple[arb, arb, Q]:
    match = re.fullmatch(r"([GW])\[(-?\d+),(-?\d+)\]", target_id)
    need(match is not None, "target id")
    kind, ix, iy = match.group(1), int(match.group(2)), int(match.group(3))
    return ((arb(ix), arb(iy), RG) if kind == "G" else
            (arb(ix) + aq(Q(1, 2)) + s, arb(iy) + aq(Q(1, 2)), RW))


def flight(origin: dict[str, Any], rbox: tuple[Q, Q], target_id: str,
           tbox: tuple[Q, Q] | None = None,
           sbox: tuple[Q, Q] | None = None) -> dict[str, arb]:
    t = iv(*(origin["tq"] if tbox is None else tbox))
    s = iv(*(origin["sq"] if sbox is None else sbox))
    a = (arb(1) - t * t).sqrt()
    nx, ny = t, a if origin["source_chart"] == "W:N" else -a
    b = aq(K).sqrt() * iv(*rbox)
    pabs = (arb(1) - b * b).sqrt()
    p = pabs if origin["p_sign"] == 1 else -pabs
    ux, uy = b * nx - p * ny, b * ny + p * nx
    qx, qy = aq(Q(1, 2)) + s + aq(RW) * nx, aq(Q(1, 2)) + aq(RW) * ny
    ax, ay, radius = target(target_id, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    delta = aq(radius * radius) - transverse * transverse
    result = {"ell": ell, "f0": dx * dx + dy * dy - aq(radius * radius),
              "delta": delta}
    if bool(delta > 0):
        result["tau"] = ell - delta.sqrt()
    return result


def hit(values: dict[str, arb], horizon: Q) -> bool:
    return ("tau" in values and bool(values["f0"] > 0) and bool(values["ell"] > 0)
            and bool(values["delta"] > 0) and bool(values["tau"] > 0)
            and bool(values["tau"] < aq(horizon)))


def eliminated(values: dict[str, arb], radius: Q) -> bool:
    return bool(values["delta"] < 0) or bool(values["ell"] + aq(radius) < 0)


def exact_completeness(horizon: Q) -> tuple[list[str], Q]:
    possible: list[str] = []
    gaps: list[Q] = []
    for kind in ("G", "W"):
        radius = RG if kind == "G" else RW
        threshold = horizon + RW + radius
        for ix in range(-5, 6):
            for iy in range(-5, 6):
                if kind == "W":
                    d2 = Q(ix * ix + iy * iy)
                else:
                    lo, hi = Q(199, 400), Q(201, 400)
                    dx = lo - ix if ix < lo else (Q(ix) - hi if ix > hi else Q(0))
                    d2 = dx * dx + (Q(iy) - Q(1, 2)) ** 2
                gap = d2 - threshold * threshold
                if gap <= 0:
                    possible.append(f"{kind}[{ix},{iy}]")
                else:
                    gaps.append(gap)
    return sorted(possible), min(gaps)


def seam_H(origin: dict[str, Any]) -> arb:
    t = iv(*origin["tq"])
    a = (arb(1) - t * t).sqrt()
    north = origin["source_chart"] == "W:N"
    nx, ny = t, a if north else -a
    b = aq(K).sqrt() * iv(Q(0), Q(1))
    pabs = (arb(1) - b * b).sqrt()
    p = pabs if origin["p_sign"] == 1 else -pabs
    ux, uy = b * nx - p * ny, b * ny + p * nx
    h = aq(Q(1, 2)).sqrt()
    mx, my = -h, h if north else -h
    dx, dy = arb(1) + aq(RW) * mx - aq(RW) * nx, aq(RW) * my - aq(RW) * ny
    return ux * dy - uy * dx


def contact_W(origin: dict[str, Any], tbox: tuple[Q, Q], rbox: tuple[Q, Q]) -> bool:
    t = iv(*tbox)
    a = (arb(1) - t * t).sqrt()
    north = origin["source_chart"] == "W:N"
    nx, ny = t, a if north else -a
    b = aq(K).sqrt() * iv(*rbox)
    pabs = (arb(1) - b * b).sqrt()
    p = pabs if origin["p_sign"] == 1 else -pabs
    ux, uy = b * nx - p * ny, b * ny + p * nx
    dx, dy = arb(1) - aq(RW) * nx, -aq(RW) * ny
    ell = ux * dx + uy * dy
    tr = -uy * dx + ux * dy
    delta = aq(RW * RW) - tr * tr
    need(bool(delta > 0), "contact delta")
    radical = delta.sqrt()
    cx = (-radical * ux + tr * uy) / aq(RW)
    cy = (-radical * uy - tr * ux) / aq(RW)
    return bool(-cx - cy > 0) and bool(-cx + cy > 0)


def verify_semantics(candidate: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = 256
    verify_pins_and_manifest()
    receipt = strict_json(safe_read(Q8_RECEIPT), "Q8 receipt")
    q8 = strict_json(safe_read(Q8_CANDIDATE), "Q8 candidate")
    need(receipt["formal_boundary"]["formal_credit"] == 0
         and receipt["formal_boundary"]["source_W_formal_remaining"] == 80,
         "Q8 boundary")
    need(q8["result_sha256"] == digest(q8["result"]), "Q8 result closure")
    census = {row["origin_key"]: hydrate(row)
              for row in q8["result"]["historic_full_census"]["origin_rows"]}
    need(len(census) == 54, "54 census")

    t1, gap1 = exact_completeness(Q(1))
    t32, gap32 = exact_completeness(Q(3, 2))
    need(t1 == sorted(T1) and gap1 == Q(29137, 160000), "T1 complete family")
    need(t32 == sorted(T32) and gap32 == Q(65937, 160000), "T3/2 complete family")

    for key in origins(BRIDGE):
        origin = census[key]
        g = "G[0,1]" if origin["source_chart"] == "W:N" else "G[0,0]"
        need(hit(flight(origin, (Q(0), Q(1, 2)), "W[-1,0]"), Q(1))
             and hit(flight(origin, (Q(1, 2), Q(1)), g), Q(1))
             and hit(flight(origin, (Q(1, 2), Q(1, 2)), "W[-1,0]"), Q(1))
             and hit(flight(origin, (Q(1, 2), Q(1, 2)), g), Q(1)),
             "bridge two-box strict cover:" + key)
        frozen = flight(origin, (Q(0), Q(1)), "W[1,0]")
        need(bool(frozen["ell"] + aq(RW) < 0), "bridge frozen behind:" + key)

    for key in origins(MISS):
        origin = census[key]
        selected = "G[2,0]" if origin["source_chart"] == "W:N" else "G[2,1]"
        need(hit(flight(origin, (Q(0), Q(1)), selected), Q(3, 2)), "06 selected hit")
        for target_id in T32:
            if target_id in {selected, "W[0,0]"}:
                continue
            values = flight(origin, (Q(0), Q(1)), target_id)
            need(eliminated(values, RG if target_id.startswith("G") else RW),
                 "06 competitor:" + key + ":" + target_id)

    epsilon = Q(1, 2000000)
    for key in origins(ROUTE):
        origin = census[key]
        token = token_of(key)
        switch = SWITCH[token]
        g = "G[1,1]" if origin["source_chart"] == "W:N" else "G[1,0]"
        for values in (flight(origin, (Q(0), switch), "W[1,0]"),
                       flight(origin, (switch, Q(1)), g),
                       flight(origin, (switch, switch), "W[1,0]"),
                       flight(origin, (switch, switch), g)):
            need(hit(values, Q(1)), "04 two-box cover:" + key)
        for target_id in T1:
            if target_id in {"W[1,0]", g, "W[0,0]"}:
                continue
            values = flight(origin, (Q(0), Q(1)), target_id)
            need(eliminated(values, RG if target_id.startswith("G") else RW),
                 "04 competitor:" + key + ":" + target_id)
        if token == ROUTE[0]:
            h = seam_H(origin)
            need(bool(h < 0) if origin["source_chart"] == "W:N" else bool(h > 0),
                 "04 first whole outgoing mismatch")
            continue
        live_t = LIVE_T[token]
        tbox = (live_t - epsilon, live_t + epsilon)
        sbox = (-epsilon, epsilon)
        live_r = (Q(15, 1024), Q(17, 1024))
        need(hit(flight(origin, live_r, "W[1,0]", tbox, sbox), Q(1))
             and bool(flight(origin, live_r, g, tbox, sbox)["delta"] < 0)
             and contact_W(origin, tbox, live_r), "mixed strict LIVE subbox:" + key)
        midpoint = sum(origin["tq"], Q(0)) / 2
        ex_t = (midpoint - epsilon, midpoint + epsilon)
        ex_r = (Q(127, 128), Q(1))
        ex_g = flight(origin, ex_r, g, ex_t, sbox)
        ex_w = flight(origin, ex_r, "W[1,0]", ex_t, sbox)
        need(hit(ex_g, Q(1)) and bool(ex_w["ell"] - aq(RW) > ex_g["tau"]),
             "mixed strict EXCLUDED subbox:" + key)

    # Independent one-switch impossibility witness.
    test = Q(3, 4)
    first, last = census["W:N:04.00.00001010"], census["W:N:04.00.10000000"]
    first_mid, last_mid = sum(first["tq"], Q(0)) / 2, sum(last["tq"], Q(0)) / 2
    need(bool(flight(first, (test, test), "W[1,0]", (first_mid, first_mid),
                            (Q(0), Q(0)))["delta"] < 0)
         and bool(flight(last, (test, test), "G[1,1]", (last_mid, last_mid),
                         (Q(0), Q(0)))["delta"] < 0), "one-switch impossibility")

    result = candidate["result"]
    ledger = result["research_disposition_ledger"]
    need(len(ledger) == 54 and len({row["origin_key"] for row in ledger}) == 54
         and {row["origin_key"] for row in ledger} == set(census), "candidate 54 partition")
    need(sum(row["research_disposition"] == "EXCLUDED" for row in ledger) == 44
         and sum(row["research_disposition"] == "RESOLVED_MIXED" for row in ledger) == 10,
         "candidate 44+10")
    closure = result["classification_closure"]
    need(closure == {
        "formal_EXCLUDED_minted": 0, "formal_RESOLVED_MIXED_minted": 0,
        "formal_dispositions_minted": 0, "mutually_exclusive_and_exhaustive": True,
        "research_EXCLUDED_candidates": 44, "research_RESOLVED_MIXED_candidates": 10,
        "strict_EXCLUDED_subboxes_for_all_mixed": 10,
        "strict_LIVE_subboxes_for_all_mixed": 10, "total_origins": 54,
        "unresolved_research_origins": 0,
    }, "classification closure")
    handoff = result["future_C30f_gated_handoff_candidate"]
    need(handoff["before"] == {"excluded": 74768, "conservative_live": 2064,
                              "resolved_nonexcluded": 2010, "remaining": 54,
                              "remaining_partition": {"compact_q": 54}}
         and handoff["candidate_after"] == {"excluded": 74812, "conservative_live": 2020,
                                            "resolved_nonexcluded": 2020, "remaining": 0,
                                            "remaining_partition": {"compact_q": 0}}
         and handoff["candidate_credit"] == {"EXCLUDED": 44, "RESOLVED_MIXED": 10,
                                             "total_dispositions": 54}
         and handoff["predecessor_exists_in_this_audit"] is False
         and handoff["terminal_adapter_present"] is False
         and handoff["formal_54_to_0_minted"] is False
         and handoff["release_state"] == "PROHIBITED_PRE_TERMINAL",
         "future C30f handoff")
    boundary = result["formal_boundary"]
    need(boundary["formal_credit"] == 0 and boundary["ledger_unchanged"] is True
         and boundary["source_W_formal_remaining"] == 80
         and boundary["compact_q_formal_remaining_origins"] == 54
         and boundary["terminal_gate_present"] is False
         and boundary["can_serve_as_compact_q_formal_predecessor"] is False
         and boundary["CM2"] == "NO-GO_FOR_CLAIM", "formal boundary")
    need(result["template_inventory"]["route_template_minimality"]["distinct_switch_value_count"] == 2
         and result["template_inventory"]["historic_root_by_root_subdivision_used"] is False,
         "template minimality/no root split")
    need(result["lower_strata_half_open_closure"]["formal_atomic_3D_2D_1D_0D_rebuild_still_required"] is True,
         "lower-strata formal boundary")
    return {
        "status": "PASS_INDEPENDENT_C30Q9_FULL_PHYSICAL_FIRST_HIT_DISPOSITION_ZERO_CREDIT",
        "candidate_result_sha256": candidate["result_sha256"],
        "Q8_manifest_reverified": True,
        "physical_target_completeness_recomputed": True,
        "all_54_origins_recomputed": True,
        "44_EXCLUDED_plus_10_RESOLVED_MIXED": True,
        "mixed_live_and_excluded_subboxes_recomputed": 10,
        "two_switch_minimality_counterexample_recomputed": True,
        "producer_imported_or_executed": False,
        "formal_credit": 0,
        "source_W_formal_remaining": 80,
        "compact_q_formal_remaining": 54,
        "formal_54_to_0_minted": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage: verifier CANDIDATE_JSON")
        raw = safe_read(Path(argv[1]).absolute())
        candidate = strict_json(raw, "candidate")
        need(raw == canonical(candidate) + b"\n", "canonical candidate bytes")
        need(candidate["schema"] ==
             "cm2.round306c30q9.compact-q-full-physical-first-hit-disposition.zero-credit.v1",
             "candidate schema")
        need(candidate["result_sha256"] == digest(candidate["result"])
             and candidate["result_sha256"] == EXPECTED_RESULT_SHA256,
             "candidate exact result pin")
        result = verify_semantics(candidate)
        output = {"schema": SCHEMA, **result, "verification_sha256": digest(result)}
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, StopIteration, Reject) as error:
        sys.stderr.write("REJECT_C30Q9_VERIFY:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
