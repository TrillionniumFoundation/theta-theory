#!/usr/bin/env python3
"""Bounded algebraic blocker probe for the Round212 source-W mixed tail.

The probe independently replays the frozen Round184 DELTA_H_OR_MULTI_NO_Q
registry through the Round180 depth-four refinement and the Round201
exact-behind rule.  It then removes the two explicitly retained Round212
source seams from the active cohort and studies only the 198 strict source
interior origins.

The new treatment is outcome-blind at selection time.  It applies:

* centered mean-value C0 bounds to the direct distance margin for
  unresolved-root-sign records;
* monotone p-face discriminant bounds for a single remaining Delta record;
* the already formal dimension-safe full-Delta graph collar test after
  exact-behind deletion; and
* an exact, disjoint taxonomy for every still-open 3D cell.

This is a read-only probe.  It has no output argument, performs no filesystem
writes, prints progress to stderr and one canonical JSON document to stdout,
and never changes the whole-origin ledger.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

from flint import arb, ctx


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round215.source-w-mixed-algebraic-blocker-probe.v2"

ROUND201_VERIFIER = (
    "cm2_round201_source_w_exact_behind_formal_promotion_verifier.py"
)
ROUND201_VERIFIER_SHA256 = (
    "29344dd3c0590ac9d0d3f0618a3f0f034316759468e15af2674813ab72f7ce2b"
)
ROUND201_MANIFEST = (
    "cm2_round201_source_w_exact_behind_formal_promotion_manifest.sha256"
)
ROUND201_MANIFEST_SHA256 = (
    "ba2aec704c8d8966267bf47f16b9840140df3d35074d0ec73a2807213baa6547"
)
ROUND212_PREFIX = "cm2_round212_source_w_half_open_source_seam_promotion"
ROUND212_MANIFEST = f"{ROUND212_PREFIX}_manifest.sha256"
ROUND212_MANIFEST_SHA256 = (
    "86a46848e016e99646bf03ea860b4c162d880e203803d259d88785a8e429b919"
)
ROUND212_CERTIFICATE_RESULT_SHA256 = (
    "a4e6e44aa55eedd376f5dd5d01a82f5c8dfae19ebb433dfb0017d07718004c7d"
)
ROUND212_VERIFICATION_RESULT_SHA256 = (
    "5ab0bb7fa213fa0e86c1252dad1a21b96ab54d4b48025e767c8af7a953383d2e"
)

DELTA_MULTI_CLASS = "DELTA_H_OR_MULTI_NO_Q"
COMPACT_CLASS = "COMPACT_Q_PRESENT"
EXPECTED_SELECTED_ORIGINS = 596
EXPECTED_SELECTED_KEYS_SHA256 = (
    "b6440ea91a3fd331cf55b1a5e7a530c3ca688d48a3e2ec0897f1981d05edbd1d"
)
EXPECTED_SELECTED_CHILDREN = 161_442
EXPECTED_MIXED_FAILED_CANDIDATES = 18_888
EXPECTED_COMPACT_ORIGINS = 54
EXPECTED_COMPACT_KEYS_SHA256 = (
    "d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b"
)
EXPECTED_COMPACT_CHILDREN = 21_334
EXPECTED_COMPACT_GEOMETRIC_RESIDUAL_CELLS = 2_552
EXPECTED_COMPACT_FAILED_CANDIDATES = 3_692
EXPECTED_GLOBAL_GENERALIZED_CHILDREN = 182_776
EXPECTED_GLOBAL_GEOMETRIC_RESIDUAL_CELLS = 21_128
EXPECTED_GLOBAL_GEOMETRIC_CLOSED_CELLS = 161_648
EXPECTED_GLOBAL_DELETED_CANDIDATES = 233_356
EXPECTED_GLOBAL_FAILED_CANDIDATES = 22_580
EXPECTED_INCOMPLETE_ORIGINS = 200
EXPECTED_INCOMPLETE_KEYS_SHA256 = (
    "5f2c635ea4f05d3ffca603031b06caffee9460271705787def0c499f286a72d1"
)
RETAINED_SEAMS = (
    "W:N:07.00.11111011",
    "W:S:H.07.00.11111011",
)
EXPECTED_RETAINED_SEAM_KEYS_SHA256 = (
    "442ffd2a391f8ec500b5c2c2b3544fb92e34e27fe93e7b2326ab2fba48f8e471"
)
EXPECTED_ACTIVE_ORIGINS = 198
EXPECTED_ACTIVE_KEYS_SHA256 = (
    "2984c2a4eb97b5dbc91ab431e11cb05b8e19c025d42683fee6959c1c9f6857c3"
)
EXPECTED_NONCOMPACT_RESIDUAL_CELLS = 18_576
EXPECTED_SEAM_RESIDUAL_CELLS = 144
EXPECTED_ACTIVE_RESIDUAL_CELLS = 18_432
EXPECTED_REDUCTION_REASON_COUNT = {
    "NO_EXACT_BEHIND_UNRESOLVED_CANDIDATE": 10_564,
    "REDUCED_REMAINING_DISPOSITION_LIVE": 48,
    "REDUCED_REMAINING_DISPOSITION_UNRESOLVED": 7_964,
}

UNRESOLVED_CLASSES = {
    "unresolved_discriminant",
    "unresolved_root_sign",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def map_counter(counter: Counter[Any]) -> dict[str, int]:
    return {
        str(key): counter[key]
        for key in sorted(counter, key=lambda item: str(item))
    }


def nested_counter(
    value: dict[str, Counter[Any]],
) -> dict[str, dict[str, int]]:
    return {
        key: map_counter(counter)
        for key, counter in sorted(value.items())
    }


def fraction_map(value: dict[str, Q]) -> dict[str, str]:
    return {
        key: str(item)
        for key, item in sorted(value.items())
    }


def read_regular(path: Path, maximum: int = 16 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input parent resolution:{absolute.name}",
    )
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1,
        f"input regular singleton:{absolute.name}",
    )
    require(0 < status.st_size <= maximum, f"input size:{absolute.name}")
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino)
            and stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1,
            f"input race/type:{absolute.name}",
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(chunk), f"short read:{absolute.name}")
            chunks.append(chunk)
            remaining -= len(chunk)
        require(not os.read(descriptor, 1), f"growing input:{absolute.name}")
    finally:
        os.close(descriptor)
    raw = b"".join(chunks)
    require(len(raw) == status.st_size, f"byte count:{absolute.name}")
    return raw


def strict_json(path: Path) -> dict[str, Any]:
    raw = read_regular(path)
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{path.name}",
    )

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, f"duplicate:{path.name}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=pairs,
        parse_float=lambda _x: (_ for _ in ()).throw(
            RuntimeError(f"float:{path.name}")
        ),
        parse_constant=lambda _x: (_ for _ in ()).throw(
            RuntimeError(f"constant:{path.name}")
        ),
    )
    require(type(value) is dict, f"top object:{path.name}")
    require(pretty_bytes(value) == raw, f"canonical JSON:{path.name}")
    require(
        set(value) == {"schema", "result", "result_sha256"}
        and digest(value["result"]) == value["result_sha256"],
        f"envelope:{path.name}",
    )
    return value


def check_manifest(name: str, expected_sha: str) -> dict[str, str]:
    raw = read_regular(HERE / name, 16 * 1024)
    require(hashlib.sha256(raw).hexdigest() == expected_sha, f"manifest:{name}")
    entries: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        value, filename = line.split("  ", 1)
        require(
            len(value) == 64
            and filename not in entries
            and "/" not in filename,
            f"manifest line:{name}:{filename}",
        )
        entries[filename] = value
    return entries


require(
    hashlib.sha256(read_regular(HERE / ROUND201_VERIFIER)).hexdigest()
    == ROUND201_VERIFIER_SHA256,
    "Round201 verifier source pin",
)
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r201 = importlib.import_module(ROUND201_VERIFIER[:-3])
require(
    Path(r201.__file__).resolve() == (HERE / ROUND201_VERIFIER).resolve(),
    "Round201 verifier module identity",
)
require(
    hashlib.sha256(read_regular(HERE / ROUND201_VERIFIER)).hexdigest()
    == ROUND201_VERIFIER_SHA256,
    "Round201 verifier post-import pin",
)
r180 = r201.r180
r176 = r201.r176


class ListDigest:
    def __init__(self) -> None:
        self._hash = hashlib.sha256()
        self._hash.update(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self._hash.update(b",")
        self._hash.update(canonical(value).encode())
        self.count += 1

    def finish(self) -> str:
        self._hash.update(b"]")
        return self._hash.hexdigest()


def check_frozen_state() -> dict[str, Any]:
    require(
        hashlib.sha256(read_regular(HERE / ROUND201_MANIFEST, 16 * 1024))
        .hexdigest()
        == ROUND201_MANIFEST_SHA256,
        "Round201 manifest pin",
    )
    entries = check_manifest(ROUND212_MANIFEST, ROUND212_MANIFEST_SHA256)
    require(len(entries) == 6, "Round212 six-entry manifest")
    for filename, expected in entries.items():
        require(
            hashlib.sha256(read_regular(HERE / filename)).hexdigest()
            == expected,
            f"Round212 manifest entry:{filename}",
        )
    certificate = strict_json(
        HERE / f"{ROUND212_PREFIX}_certificate.json"
    )
    verification = strict_json(
        HERE / f"{ROUND212_PREFIX}_verification.json"
    )
    require(
        certificate["result_sha256"]
        == ROUND212_CERTIFICATE_RESULT_SHA256
        and verification["result_sha256"]
        == ROUND212_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS_FORMAL_ROUND212"
        and verification["result"]["verdict"] == "PASS"
        and verification["result"]["verified_census"][
            "combined_whole_record_excluded"
        ]
        == 74_582
        and verification["result"]["verified_census"][
            "combined_conservative_live"
        ]
        == 2_250
        and verification["result"]["verified_census"][
            "remaining_priority_origins"
        ]
        == 254,
        "Round212 verified state",
    )
    upstream = r201.check_upstream()
    return {
        "Round201_manifest_sha256": ROUND201_MANIFEST_SHA256,
        "Round201_verifier_sha256": ROUND201_VERIFIER_SHA256,
        "Round184_manifest_sha256":
            upstream["Round184_manifest_sha256"],
        "Round212_manifest_sha256": ROUND212_MANIFEST_SHA256,
        "Round212_manifest_entries_replayed": True,
        "Round212_certificate_result_sha256":
            ROUND212_CERTIFICATE_RESULT_SHA256,
        "Round212_verification_result_sha256":
            ROUND212_VERIFICATION_RESULT_SHA256,
        "Round212_verified_ledger": {
            "excluded": 74_582,
            "conservative_live": 2_250,
            "total": 76_832,
            "remaining": 254,
            "remaining_partition": {
                "incomplete_mixed": 200,
                "compact_q": 54,
            },
        },
        "upstream": upstream,
    }


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def sign_name(value: arb) -> str:
    return {
        -1: "STRICT_NEGATIVE",
        0: "OVERWRAP",
        1: "STRICT_POSITIVE",
    }[r176.sign(value)]


def exact_behind_reduce(row: Any, category: str) -> dict[str, Any]:
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = sorted(
        (
            record
            for record in records
            if record.classification in UNRESOLVED_CLASSES
        ),
        key=lambda record: record.target_id,
    )
    candidate_evidence = [
        r201.exact_distance_evidence(row, candidate)
        for candidate in unresolved
    ]
    eligible = sorted(
        evidence["target"]
        for evidence in candidate_evidence
        if evidence["eligible_exact_behind"]
    )
    current = [
        record for record in records
        if record.target_id not in set(eligible)
    ]
    leaf = r176.classify_records(row.chart_id, row.box, current)
    disposition, _margins = r176.terminal_disposition(
        row.chart_id, leaf
    )
    excluded = (
        bool(eligible)
        and disposition is not None
        and disposition.startswith("EXCLUDED")
    )
    live = (
        disposition is not None
        and disposition.startswith("LIVE")
    )
    if not eligible:
        reason = "NO_EXACT_BEHIND_UNRESOLVED_CANDIDATE"
    elif live:
        reason = "REDUCED_REMAINING_DISPOSITION_LIVE"
    elif not excluded:
        reason = "REDUCED_REMAINING_DISPOSITION_UNRESOLVED"
    else:
        reason = "NONE__GEOMETRICALLY_CLOSED"
    return {
        "records": records,
        "current_records": current,
        "leaf": leaf,
        "disposition": disposition,
        "candidate_evidence": candidate_evidence,
        "eligible_targets": eligible,
        "closed": excluded,
        "residual_reason": reason,
        "category": category,
    }


def normal_and_dt(chart_id: str, box: Any) -> tuple[arb, arb, arb, arb]:
    cell = chart_id.split(":")[1]
    t = r176.base.arb_interval(box.t0, box.t1)
    radical = r176.sqrt_one_minus_square(box.t0, box.t1)
    require(bool(radical > 0), f"normal radical:{chart_id}:{box.path}")
    ratio = t / radical
    one = arb(1)
    if cell == "E":
        return radical, t, -ratio, one
    if cell == "N":
        return t, radical, one, -ratio
    if cell == "S":
        return t, -radical, one, ratio
    raise RuntimeError(f"unexpected source-W chart:{chart_id}")


def distance_margin_with_derivatives(
    row: Any,
    target_id: str,
    box: Any,
) -> tuple[arb, arb, arb]:
    nx, ny, dnx, dny = normal_and_dt(row.chart_id, box)
    s = r176.base.arb_interval(box.s0, box.s1)
    half = r176.base.arbq(Q(1, 2))
    source_radius = r176.base.arbq(r176.base.RADIUS["W"])
    qx = half + s + source_radius * nx
    qy = half + source_radius * ny
    target = r176.TARGETS[target_id]
    ax, ay = r176.base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    target_radius = r176.base.arbq(
        r176.base.RADIUS[target.obstacle]
    )
    margin = (
        dx * dx + dy * dy - target_radius * target_radius
    )
    dx_dt = -source_radius * dnx
    dy_dt = -source_radius * dny
    derivative_t = 2 * (dx * dx_dt + dy * dy_dt)
    derivative_s = (
        arb(0) if target.obstacle == "W" else -2 * dx
    )
    return margin, derivative_t, derivative_s


def centered_distance_margin(row: Any, target_id: str) -> dict[str, Any]:
    box = row.box
    tc = (box.t0 + box.t1) / 2
    sc = (box.s0 + box.s1) / 2
    center_box = r176.Box(
        tc, tc, box.p0, box.p1, sc, sc,
        box.depth, box.path + ".center",
    )
    center, _dt_center, _ds_center = distance_margin_with_derivatives(
        row, target_id, center_box
    )
    natural, derivative_t, derivative_s = (
        distance_margin_with_derivatives(row, target_id, box)
    )
    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    centered = (
        center
        + derivative_t
        * r176.base.arb_interval(-t_radius, t_radius)
        + derivative_s
        * r176.base.arb_interval(-s_radius, s_radius)
    )
    require(
        bool(centered.overlaps(natural)),
        f"centered/natural overlap:{row.key}:{target_id}",
    )
    return {
        "target": target_id,
        "natural_sign": sign_name(natural),
        "centered_sign": sign_name(centered),
        "centered_strictly_sharpens_overwrap":
            sign_name(natural) == "OVERWRAP"
            and sign_name(centered) != "OVERWRAP",
        "centered_value": centered,
    }


def enhance_root_sign_records(
    row: Any,
    records: list[Any],
) -> tuple[list[Any], list[dict[str, Any]]]:
    enhanced: list[Any] = []
    evidence_rows: list[dict[str, Any]] = []
    for record in records:
        if record.classification != "unresolved_root_sign":
            enhanced.append(record)
            continue
        evidence = centered_distance_margin(row, record.target_id)
        can_future = (
            evidence["centered_sign"] == "STRICT_POSITIVE"
            and bool(record.ell > 0)
            and record.far is not None
            and bool(record.far > 0)
        )
        if can_future:
            near = evidence["centered_value"] / record.far
            require(
                bool(near > 0),
                f"centered positive near:{row.key}:{record.target_id}",
            )
            enhanced.append(r176.Root(
                record.target_id,
                "strict_future_root",
                record.ell,
                record.discriminant,
                near,
                record.far,
                record.transverse,
            ))
        else:
            enhanced.append(record)
        evidence_rows.append({
            key: value
            for key, value in evidence.items()
            if key != "centered_value"
        } | {
            "ell_sign": sign_name(record.ell),
            "far_sign": (
                sign_name(record.far)
                if record.far is not None
                else "NOT_AVAILABLE"
            ),
            "reclassified_strict_future_root": can_future,
        })
    return enhanced, evidence_rows


def outgoing_from_enhanced_record(
    row: Any,
    owner: Any,
) -> tuple[str | None, dict[str, arb], dict[str, Any]]:
    """Compute all outgoing margins from a supplied strict owner record."""
    require(
        owner.target_id == r176.FROZEN_OWNER
        and owner.classification == "strict_future_root"
        and owner.near is not None
        and bool(owner.near > 0),
        f"enhanced outgoing owner root:{row.key}",
    )
    qx, qy, ux, uy, s, _rp = r176.geometry(
        row.chart_id, row.box
    )
    target = r176.TARGETS[r176.FROZEN_OWNER]
    cx, cy = r176.base.target_center(target, s)
    radius = r176.base.arbq(r176.base.RADIUS["W"])
    nx = (qx + owner.near * ux - cx) / radius
    ny = (qy + owner.near * uy - cy) / radius
    margins = {
        "E.first": nx - ny,
        "E.second": nx + ny,
        "W.first": -nx - ny,
        "W.second": -nx + ny,
        "N.first": ny - nx,
        "N.second": ny + nx,
        "S.first": -ny - nx,
        "S.second": -ny + nx,
    }
    cells = [
        cell for cell in ("E", "W", "N", "S")
        if (
            bool(margins[f"{cell}.first"] > 0)
            and bool(margins[f"{cell}.second"] > 0)
        )
    ]
    chart = cells[0] if len(cells) == 1 else None

    natural = r176.records_for(
        row.chart_id, row.box, (r176.FROZEN_OWNER,)
    )[0]
    natural_control = (
        natural.classification == "strict_future_root"
        and natural.near is not None
        and bool(natural.near > 0)
    )
    control = {
        "natural_strict_control_available": natural_control,
        "upstream_chart_exact_equal": "NOT_APPLICABLE",
        "all_eight_upstream_margin_enclosures_overlap":
            "NOT_APPLICABLE",
        "enhanced_owner_margin_signs": {
            key: sign_name(value)
            for key, value in sorted(margins.items())
        },
        "all_eight_enhanced_owner_margins_strict":
            all(sign_name(value) != "OVERWRAP"
                for value in margins.values()),
    }
    if natural_control:
        upstream_chart, upstream_margins = r176.outgoing_generic(
            row.chart_id, row.box
        )
        chart_equal = chart == upstream_chart
        margins_overlap = all(
            bool(margins[key].overlaps(upstream_margins[key]))
            for key in sorted(margins)
        )
        require(
            chart_equal and margins_overlap,
            f"enhanced outgoing natural control:{row.key}",
        )
        control = {
            "natural_strict_control_available": True,
            "upstream_chart_exact_equal": True,
            "all_eight_upstream_margin_enclosures_overlap": True,
            "enhanced_owner_margin_signs": {
                key: sign_name(value)
                for key, value in sorted(margins.items())
            },
            "all_eight_enhanced_owner_margins_strict":
                all(sign_name(value) != "OVERWRAP"
                    for value in margins.values()),
        }
    return chart, margins, control


def enhanced_terminal_disposition(
    row: Any,
    leaf: Any,
    records: list[Any],
) -> tuple[str | None, str, dict[str, Any]]:
    """Recompute terminal status from the supplied enhanced record set.

    The upstream generic terminal helper intentionally re-evaluates the
    frozen owner with the natural interval expression.  That is unsuitable
    after a centered or monotone enhancement has rigorously sharpened that
    same owner record.  This function preserves the upstream decision tree
    but computes the outgoing normal from the enhanced strict near root.
    """
    empty_control = {
        "natural_strict_control_available": False,
        "upstream_chart_exact_equal": "NOT_APPLICABLE",
        "all_eight_upstream_margin_enclosures_overlap":
            "NOT_APPLICABLE",
    }
    if leaf.classification == "no_future_root":
        return (
            "EXCLUDED_NO_INHERITED_FUTURE_ROOT",
            "NOT_APPLICABLE",
            empty_control,
        )
    if leaf.classification != "unique_first":
        return None, "NOT_APPLICABLE", empty_control
    if leaf.owner_target != r176.FROZEN_OWNER:
        return (
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH",
            "NOT_APPLICABLE",
            empty_control,
        )
    owners = [
        record for record in records
        if record.target_id == r176.FROZEN_OWNER
    ]
    require(
        len(owners) == 1
        and owners[0].classification == "strict_future_root"
        and owners[0].near is not None
        and bool(owners[0].near > 0),
        f"enhanced frozen owner root:{row.key}",
    )
    owner = owners[0]
    chart, _margins, control = outgoing_from_enhanced_record(
        row, owner
    )
    if chart is None:
        return None, "OVERWRAP", control
    if chart == r176.FROZEN_CHART:
        return (
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH",
            chart,
            control,
        )
    return "EXCLUDED_OUTGOING_CHART_MISMATCH", chart, control


def single_delta_resolution(
    row: Any,
    records: list[Any],
    candidate: Any,
) -> dict[str, Any]:
    derivative, lower, upper, full = r176.graph_faces(row, candidate)
    derivative_name = {
        -1: "STRICT_NEGATIVE",
        0: "OVERWRAP",
        1: "STRICT_POSITIVE",
    }[derivative]
    lower_name = sign_name(lower)
    upper_name = sign_name(upper)
    base = {
        "Delta_p_derivative_sign": derivative_name,
        "Delta_p_lower_face_sign": lower_name,
        "Delta_p_upper_face_sign": upper_name,
        "full_p_monotone_graph": full,
        "candidate_target": candidate.target_id,
        "candidate_owner_is_frozen":
            candidate.target_id == r176.FROZEN_OWNER,
    }
    same_strict = (
        derivative != 0
        and lower_name != "OVERWRAP"
        and lower_name == upper_name
    )
    if same_strict:
        replacement = r176.enhanced_record(
            candidate, lower, upper, derivative
        )
        replaced = [
            replacement
            if record.target_id == candidate.target_id
            else record
            for record in records
        ]
        leaf = r176.classify_records(
            row.chart_id, row.box, replaced
        )
        disposition, enhanced_chart, enhanced_control = (
            enhanced_terminal_disposition(
            row, leaf, replaced
            )
        )
        if disposition is not None and disposition.startswith("EXCLUDED"):
            owner = (
                leaf.owner_target
                if leaf.classification == "unique_first"
                else "NOT_APPLICABLE"
            )
            owner_mismatch = (
                leaf.classification == "unique_first"
                and owner != r176.FROZEN_OWNER
            )
            outgoing_mismatch = (
                leaf.classification == "unique_first"
                and owner == r176.FROZEN_OWNER
                and enhanced_chart not in {
                    "NOT_APPLICABLE", "OVERWRAP", None,
                    r176.FROZEN_CHART,
                }
                and enhanced_control[
                    "all_eight_enhanced_owner_margins_strict"
                ]
            )
            require(
                leaf.classification == "unique_first"
                and (owner_mismatch or outgoing_mismatch),
                f"same-sign strict unique-first exclusion:{row.key}",
            )
            boundary_proof = {
                "predicate_family": [
                    "dDelta/dp",
                    "Delta(p_lower)",
                    "Delta(p_upper)",
                    "enhanced_strict_root_order",
                    "unique_first_owner",
                    (
                        "outgoing_owner_chart_margins"
                        if not owner_mismatch
                        else "owner_mismatch_no_outgoing_margin_needed"
                    ),
                ],
                "dDelta_dp_sign": derivative_name,
                "Delta_p_lower_face_sign": lower_name,
                "Delta_p_upper_face_sign": upper_name,
                "Delta_endpoints_have_same_strict_sign": True,
                "whole_closed_box_Delta_sign": lower_name,
                "Delta_zero_graph_intersects_closed_box": False,
                "post_enhancement_leaf": leaf.classification,
                "post_enhancement_unique_first_owner": owner,
                "unique_first_owner_mismatch_on_whole_closed_box":
                    owner_mismatch,
                "outgoing_owner_chart_mismatch_on_whole_closed_box":
                    outgoing_mismatch,
                "outgoing_owner_margin_requirement": (
                    "NOT_APPLICABLE_UNIQUE_FIRST_OWNER_MISMATCH"
                    if owner_mismatch
                    else "ALL_EIGHT_STRICT_WHOLE_BOX_INTERVALS"
                ),
                "enhanced_owner_margin_signs": (
                    {}
                    if owner_mismatch
                    else enhanced_control[
                        "enhanced_owner_margin_signs"
                    ]
                ),
                "all_applicable_owner_chart_margins_strict":
                    (
                        True
                        if owner_mismatch
                        else enhanced_control[
                            "all_eight_enhanced_owner_margins_strict"
                        ]
                    ),
                "whole_closed_box_terminal_disposition":
                    disposition,
                "restriction_theorem":
                    "A strict interval inequality on a closed box "
                    "restricts to every owned face, edge, and vertex; "
                    "strict monotonicity plus equal strict endpoint "
                    "signs excludes the Delta=0 graph on the entire "
                    "closed box; strict enhanced root order and the "
                    "discrete owner/outgoing mismatch therefore persist "
                    "on all owned 2D/1D/0D boundary strata.",
                "closed_box_strict_inequalities_restrict_to_all_"
                "faces_edges_vertices": True,
            }
            return base | {
                "analytic_closed": True,
                "method":
                    "MONOTONE_P_SAME_SIGN_DELTA_STRICT_EXCLUSION",
                "blocker": "NONE__CLOSED",
                "post_enhancement_leaf": leaf.classification,
                "post_enhancement_disposition": disposition,
                "post_enhancement_outgoing_chart": enhanced_chart,
                "outgoing_enhanced_record_control": enhanced_control,
                "closed_box_boundary_restriction_proof":
                    boundary_proof,
            }
        if disposition is not None and disposition.startswith("LIVE"):
            blocker = "MONOTONE_SAME_SIGN_RECLASSIFIES_LIVE_3D"
        else:
            blocker = (
                "MONOTONE_SAME_SIGN_RECLASSIFICATION_"
                + leaf.classification.upper()
            )
        return base | {
            "analytic_closed": False,
            "method": "MONOTONE_P_SAME_SIGN_DELTA",
            "blocker": blocker,
            "post_enhancement_leaf": leaf.classification,
            "post_enhancement_disposition": (
                disposition if disposition is not None else "UNRESOLVED"
            ),
            "post_enhancement_outgoing_chart": enhanced_chart,
            "outgoing_enhanced_record_control": enhanced_control,
        }

    target_first = r176.target_positive_first(candidate, records)
    negative = r176.remove_disposition(
        row, records, candidate.target_id
    )
    negative_excluded = (
        negative is not None and negative.startswith("EXCLUDED")
    )
    if full and target_first and negative_excluded:
        if candidate.target_id != r176.FROZEN_OWNER:
            return base | {
                "analytic_closed": True,
                "method":
                    "FULL_MONOTONE_DELTA_GRAPH_OWNER_MISMATCH",
                "blocker": "NONE__CLOSED",
                "target_strict_positive_first": True,
                "Delta_negative_side_disposition": negative,
                "Delta_positive_graph_disposition":
                    "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH",
            }
        chart = r176.positive_chart(row, candidate)
        if chart is not None and chart != r176.FROZEN_CHART:
            return base | {
                "analytic_closed": True,
                "method":
                    "FULL_MONOTONE_DELTA_GRAPH_OUTGOING_MISMATCH",
                "blocker": "NONE__CLOSED",
                "target_strict_positive_first": True,
                "Delta_negative_side_disposition": negative,
                "Delta_positive_outgoing_chart": chart,
            }
        return base | {
            "analytic_closed": False,
            "method": "FULL_MONOTONE_DELTA_GRAPH",
            "blocker":
                "FULL_DELTA_FROZEN_OWNER_OUTGOING_NOT_STRICT_MISMATCH",
            "target_strict_positive_first": True,
            "Delta_negative_side_disposition": negative,
            "Delta_positive_outgoing_chart":
                chart if chart is not None else "OVERWRAP",
        }
    if derivative == 0:
        blocker = "SINGLE_DELTA_P_DERIVATIVE_OVERWRAP"
    elif not full and (
        lower_name == "OVERWRAP" or upper_name == "OVERWRAP"
    ):
        blocker = "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
    elif not full:
        blocker = "SINGLE_DELTA_NO_FULL_OR_SAME_SIGN_FACE_CERTIFICATE"
    elif not target_first:
        blocker = "SINGLE_FULL_DELTA_FIRST_ROOT_ORDER_NOT_STRICT"
    else:
        blocker = "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED"
    return base | {
        "analytic_closed": False,
        "method": "SINGLE_DELTA_MONOTONE_ENDPOINT_PROBE",
        "blocker": blocker,
        "target_strict_positive_first": target_first,
        "Delta_negative_side_disposition": (
            negative if negative is not None else "UNRESOLVED"
        ),
    }


def analyze_residual_cell(row: Any, reduction: dict[str, Any]) -> dict[str, Any]:
    records = reduction["current_records"]
    leaf = reduction["leaf"]
    disposition = reduction["disposition"]
    centered_records, centered_rows = enhance_root_sign_records(
        row, records
    )
    centered_leaf = r176.classify_records(
        row.chart_id, row.box, centered_records
    )
    (
        centered_disposition,
        centered_chart,
        centered_control,
    ) = enhanced_terminal_disposition(
        row, centered_leaf, centered_records
    )
    base = {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "exact_volume": str(box_volume(row.box)),
        "original_failure_type": row.failure,
        "original_residual_category": reduction["category"],
        "exact_behind_residual_reason": reduction["residual_reason"],
        "eligible_exact_behind_targets":
            reduction["eligible_targets"],
        "post_exact_behind_leaf": leaf.classification,
        "post_exact_behind_disposition": (
            disposition if disposition is not None else "UNRESOLVED"
        ),
        "centered_root_sign_evidence": centered_rows,
        "post_centered_leaf": centered_leaf.classification,
        "post_centered_disposition": (
            centered_disposition
            if centered_disposition is not None
            else "UNRESOLVED"
        ),
        "post_centered_outgoing_chart": centered_chart,
        "post_centered_outgoing_control": centered_control,
    }
    if disposition is not None and disposition.startswith("LIVE"):
        return base | {
            "remaining_unresolved_target_count": 0,
            "remaining_unresolved_class_count": {},
            "analytic_closed": False,
            "method": "EXACT_BEHIND_RECLASSIFICATION",
            "blocker": "REDUCED_LIVE_3D_CELL",
        }
    if (
        centered_disposition is not None
        and centered_disposition.startswith("EXCLUDED")
    ):
        return base | {
            "remaining_unresolved_target_count": 0,
            "remaining_unresolved_class_count": {},
            "analytic_closed": True,
            "method": "CENTERED_DISTANCE_MARGIN_STRICT_EXCLUSION",
            "blocker": "NONE__CLOSED",
        }
    if (
        centered_disposition is not None
        and centered_disposition.startswith("LIVE")
    ):
        return base | {
            "remaining_unresolved_target_count": 0,
            "remaining_unresolved_class_count": {},
            "analytic_closed": False,
            "method": "CENTERED_DISTANCE_MARGIN_RECLASSIFICATION",
            "blocker": "CENTERED_ROOT_MARGIN_RECLASSIFIES_LIVE_3D",
        }

    unresolved = sorted(
        (
            record
            for record in centered_records
            if record.classification in UNRESOLVED_CLASSES
        ),
        key=lambda record: record.target_id,
    )
    class_count = Counter(
        record.classification for record in unresolved
    )
    common = base | {
        "remaining_unresolved_target_count": len(unresolved),
        "remaining_unresolved_class_count": map_counter(class_count),
        "remaining_unresolved_targets": [
            record.target_id for record in unresolved
        ],
    }
    if len(unresolved) > 1:
        blocker = (
            "MULTI_DELTA_AND_ROOT_SIGN_ARRANGEMENT"
            if len(class_count) > 1
            else "MULTI_DELTA_GRAPH_ARRANGEMENT"
            if set(class_count) == {"unresolved_discriminant"}
            else "MULTI_ROOT_SIGN_EQUALITY_ARRANGEMENT"
        )
        return common | {
            "analytic_closed": False,
            "method": "MULTI_EQUATION_ARRANGEMENT_CENSUS",
            "blocker": blocker,
        }
    if len(unresolved) == 1:
        candidate = unresolved[0]
        if candidate.classification == "unresolved_root_sign":
            centered = next(
                evidence
                for evidence in centered_rows
                if evidence["target"] == candidate.target_id
            )
            return common | {
                "analytic_closed": False,
                "method": "CENTERED_ROOT_SIGN_EQUALITY_CENSUS",
                "blocker":
                    "SINGLE_ROOT_SIGN_EQUALITY_COLLAR_"
                    + centered["centered_sign"],
            }
        return common | single_delta_resolution(
            row, centered_records, candidate
        )
    return common | {
        "analytic_closed": False,
        "method": "REDUCED_NONTERMINAL_RECORD_CENSUS",
        "blocker":
            "NO_UNRESOLVED_RECORD_BUT_"
            + centered_leaf.classification.upper(),
    }


def reconstruct_refinement_leaf_frontiers(
    roots: list[Any],
    refinement: dict[str, Any],
) -> dict[str, Any]:
    """Rebuild every Round180 terminal/final leaf with its exact box."""
    expected_terminal = {
        row["cell_key"] for row in refinement["terminal_rows"]
    }
    expected_final = {
        row.key for row in refinement["final_residual_rows"]
    }
    terminal_rows: dict[str, Any] = {}
    final_rows: dict[str, Any] = {}
    pending = [(row, 0) for row in roots]
    while pending:
        row, depth = pending.pop()
        kind, _evidence, unresolved = r180.close_node(row)
        if kind is not None:
            require(
                row.key in expected_terminal,
                f"owner audit terminal identity:{row.key}",
            )
            terminal_rows[row.key] = row
            continue
        require(
            unresolved is not None,
            f"owner audit unresolved identity:{row.key}",
        )
        if depth == 4:
            require(
                unresolved.key in expected_final,
                f"owner audit final identity:{unresolved.key}",
            )
            final_rows[unresolved.key] = unresolved
            continue
        axis = r180.split_axis(unresolved.box)
        lower, upper = r176.split(unresolved.box, axis)
        pending.extend([
            (
                r176.Frontier(
                    unresolved.chart_id,
                    lower,
                    unresolved.active_targets,
                    unresolved.origin_key,
                    unresolved.failure,
                ),
                depth + 1,
            ),
            (
                r176.Frontier(
                    unresolved.chart_id,
                    upper,
                    unresolved.active_targets,
                    unresolved.origin_key,
                    unresolved.failure,
                ),
                depth + 1,
            ),
        ])
    require(
        set(terminal_rows) == expected_terminal
        and set(final_rows) == expected_final,
        "owner audit complete leaf identity",
    )
    return {
        "terminal": terminal_rows,
        "final": final_rows,
    }


def reconstruct_round176_prior_partition(
    replay: dict[str, Any],
    origin: str,
) -> dict[str, Any]:
    """Recover the pre-depth-six Round176 terminals and exact split tree."""
    source_meta = replay["origins"][origin]
    chart_id = source_meta["chart_id"]
    origin_path = source_meta["path"]
    prior_evidence = sorted(
        replay["prior"][origin],
        key=lambda row: row["leaf_key"],
    )
    prior_by_key = {
        row["leaf_key"]: row for row in prior_evidence
    }
    require(
        len(prior_by_key) == len(prior_evidence)
        and all(
            row["disposition"].startswith("EXCLUDED")
            for row in prior_evidence
        ),
        f"Round176 prior excluded uniqueness:{origin}",
    )
    frontier_keys = {
        row.key for row in replay["frontier"]
        if row.origin_key == origin
    }
    prior_rows: dict[str, Any] = {}
    split_faces: list[dict[str, Any]] = []
    pending = [(source_meta["box"], 0)]
    while pending:
        box, depth = pending.pop()
        key = f"{chart_id}:{box.path}"
        if key in prior_by_key:
            evidence = prior_by_key[key]
            require(
                evidence["relative_depth"] == depth
                and evidence["coverage_numerator_64"]
                == 2 ** (6 - depth),
                f"Round176 prior depth/coverage:{key}",
            )
            prior_rows[key] = r176.Frontier(
                chart_id,
                box,
                (),
                origin,
                "PINNED_PRE_DEPTH14_CLOSED_BOX",
            )
            continue
        if depth == 6:
            require(
                key in frontier_keys,
                f"Round176 depth-six frontier identity:{key}",
            )
            continue
        lower, upper = r176.split(box)
        parent = r176.Frontier(
            chart_id,
            box,
            (),
            origin,
            "ROUND176_PARTITION_SPLIT",
        )
        split_faces.append(r180.split_face(
            parent,
            r180.split_axis(box),
            lower,
            upper,
        ))
        pending.extend([(lower, depth + 1), (upper, depth + 1)])
    prior_volume = sum(
        (box_volume(row.box) for row in prior_rows.values()), Q(0)
    )
    parent_volume = box_volume(source_meta["box"])
    frontier_volume = sum(
        (
            box_volume(row.box)
            for row in replay["frontier"]
            if row.origin_key == origin
        ),
        Q(0),
    )
    coverage_numerator = sum(
        row["coverage_numerator_64"] for row in prior_evidence
    )
    require(
        set(prior_rows) == set(prior_by_key)
        and coverage_numerator == 7
        and prior_volume == parent_volume * Q(coverage_numerator, 64)
        and prior_volume + frontier_volume == parent_volume,
        f"Round176 prior/frontier exact partition:{origin}",
    )
    evidence_rows = [
        {
            "upstream_evidence": row,
            "closed_box": r176.box_row(prior_rows[row["leaf_key"]].box),
            "whole_closed_box_excluded": True,
        }
        for row in prior_evidence
    ]
    return {
        "prior_closed_rows": prior_rows,
        "prior_closed_evidence_rows": evidence_rows,
        "prior_closed_evidence_rows_sha256": digest(evidence_rows),
        "prior_closed_count": len(prior_rows),
        "prior_coverage_numerator_64": coverage_numerator,
        "prior_closed_exact_volume": prior_volume,
        "depth_six_frontier_count": len(frontier_keys),
        "depth_six_frontier_exact_volume": frontier_volume,
        "split_face_rows": sorted(
            split_faces, key=lambda row: row["parent_cell_key"]
        ),
    }


def strict_lower_strata_owner_audit(
    round176_split_faces: list[dict[str, Any]],
    split_faces: list[dict[str, Any]],
    original_parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
) -> dict[str, Any]:
    """Enumerate and reduce every internal/outer lower stratum to 3D owners.

    The legacy Round180 ledger's final boolean is deliberately ignored.
    Counts, geometries, half-open owners, exact coverage, and proof sources
    are rebuilt here from the split rows and exact leaf boxes.
    """
    axes = ("t", "p", "s")

    def bounds(row: Any) -> dict[str, tuple[Q, Q]]:
        box = row.box
        return {
            "t": (box.t0, box.t1),
            "p": (box.p0, box.p1),
            "s": (box.s0, box.s1),
        }

    leaf_bounds = {
        key: bounds(row) for key, row in leaf_rows.items()
    }
    require(
        set(leaf_rows) == set(proof_source),
        "owner audit proof source for every 3D leaf",
    )

    def overlap_length(
        first: tuple[Q, Q],
        second: tuple[Q, Q],
    ) -> Q:
        return max(Q(0), min(first[1], second[1])
                   - max(first[0], second[0]))

    def descendants(prefix: str | None) -> list[str]:
        if prefix is None:
            return sorted(leaf_rows)
        return sorted(
            key for key in leaf_rows if key.startswith(prefix)
        )

    def face_owner_row(
        geometry: dict[str, Any],
        owner_prefix: str | None,
        stratum_class: str,
    ) -> dict[str, Any]:
        fixed_axis = geometry["fixed_axis"]
        coordinate = Q(geometry["coordinate"])
        spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in geometry["spans"].items()
        }
        free_axes = sorted(spans)
        measure = (
            (spans[free_axes[0]][1] - spans[free_axes[0]][0])
            * (spans[free_axes[1]][1] - spans[free_axes[1]][0])
        )
        owners: list[str] = []
        covered = Q(0)
        for key in descendants(owner_prefix):
            item = leaf_bounds[key]
            if not (
                item[fixed_axis][0]
                <= coordinate
                <= item[fixed_axis][1]
            ):
                continue
            area = (
                overlap_length(item[free_axes[0]], spans[free_axes[0]])
                * overlap_length(
                    item[free_axes[1]], spans[free_axes[1]]
                )
            )
            if area:
                owners.append(key)
                covered += area
        require(
            owners and covered == measure,
            "face owner exact coverage:"
            + canonical({
                "geometry": geometry,
                "owner_count": len(owners),
                "covered": str(covered),
                "measure": str(measure),
                "owner_prefix": owner_prefix,
            }),
        )
        return {
            "stratum_class": stratum_class,
            "geometry": geometry,
            "half_open_owner_prefix":
                owner_prefix if owner_prefix is not None else "PARENT",
            "owning_closed_3D_enclosures": owners,
            "owning_closed_3D_enclosures_sha256": digest(owners),
            "owning_proof_source_count": map_counter(Counter(
                proof_source[key] for key in owners
            )),
            "exact_measure": str(measure),
            "covered_exact_measure": str(covered),
            "every_owner_is_an_excluded_closed_3D_enclosure": True,
        }

    def edge_owner_row(
        geometry: dict[str, Any],
        owner_prefix: str | None,
        stratum_class: str,
    ) -> dict[str, Any]:
        fixed = {
            axis: Q(value)
            for axis, value in geometry["fixed"].items()
        }
        free_axis, values = next(iter(geometry["free"].items()))
        span = (Q(values[0]), Q(values[1]))
        measure = span[1] - span[0]
        owners: list[str] = []
        covered = Q(0)
        for key in descendants(owner_prefix):
            item = leaf_bounds[key]
            if not all(
                item[axis][0] <= value <= item[axis][1]
                for axis, value in fixed.items()
            ):
                continue
            length = overlap_length(item[free_axis], span)
            if length:
                owners.append(key)
                covered += length
        require(
            owners and covered == measure,
            "edge owner exact coverage:"
            + canonical({
                "geometry": geometry,
                "owner_count": len(owners),
                "covered": str(covered),
                "measure": str(measure),
                "owner_prefix": owner_prefix,
            }),
        )
        return {
            "stratum_class": stratum_class,
            "geometry": geometry,
            "half_open_owner_prefix":
                owner_prefix if owner_prefix is not None else "PARENT",
            "owning_closed_3D_enclosures": owners,
            "owning_closed_3D_enclosures_sha256": digest(owners),
            "owning_proof_source_count": map_counter(Counter(
                proof_source[key] for key in owners
            )),
            "exact_measure": str(measure),
            "covered_exact_measure": str(covered),
            "every_owner_is_an_excluded_closed_3D_enclosure": True,
        }

    def corner_owner_row(
        geometry: dict[str, str],
        owner_prefix: str | None,
        stratum_class: str,
    ) -> dict[str, Any]:
        point = {
            axis: Q(value) for axis, value in geometry.items()
        }
        owners = [
            key for key in descendants(owner_prefix)
            if all(
                leaf_bounds[key][axis][0]
                <= value
                <= leaf_bounds[key][axis][1]
                for axis, value in point.items()
            )
        ]
        require(
            bool(owners),
            f"corner owner exists:{canonical(geometry)}",
        )
        selected = min(owners)
        return {
            "stratum_class": stratum_class,
            "geometry": geometry,
            "half_open_owner_prefix":
                owner_prefix if owner_prefix is not None else "PARENT",
            "owning_closed_3D_enclosure": selected,
            "owning_proof_source": proof_source[selected],
            "every_owner_is_an_excluded_closed_3D_enclosure": True,
        }

    def internal_group(
        rows: list[dict[str, Any]],
        label: str,
    ) -> tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
    ]:
        owner_faces: list[dict[str, Any]] = []
        edge_owner_prefix: dict[str, str] = {}
        corner_owner_prefix: dict[str, str] = {}
        for face in rows:
            geometry = {
                "fixed_axis": face["axis"],
                "coordinate": face["coordinate"],
                "spans": face["spans"],
            }
            owner_faces.append(face_owner_row(
                geometry,
                face["lower_child_owner"],
                label + "_INTERNAL_SPLIT_FACE",
            ))
            free_axes = [
                axis for axis in axes if axis != face["axis"]
            ]
            for boundary_axis in free_axes:
                remaining_axis = next(
                    axis for axis in free_axes
                    if axis != boundary_axis
                )
                for endpoint in face["spans"][boundary_axis]:
                    edge = {
                        "fixed": {
                            face["axis"]: face["coordinate"],
                            boundary_axis: endpoint,
                        },
                        "free": {
                            remaining_axis:
                                face["spans"][remaining_axis]
                        },
                    }
                    key = canonical(edge)
                    current = edge_owner_prefix.get(key)
                    owner = face["lower_child_owner"]
                    edge_owner_prefix[key] = (
                        owner
                        if current is None
                        else min(current, owner)
                    )
            for first in face["spans"][free_axes[0]]:
                for second in face["spans"][free_axes[1]]:
                    corner = {
                        face["axis"]: face["coordinate"],
                        free_axes[0]: first,
                        free_axes[1]: second,
                    }
                    key = canonical(corner)
                    current = corner_owner_prefix.get(key)
                    owner = face["lower_child_owner"]
                    corner_owner_prefix[key] = (
                        owner
                        if current is None
                        else min(current, owner)
                    )
        owner_edges = [
            edge_owner_row(
                json.loads(key),
                owner,
                label + "_INTERNAL_SPLIT_FACE_EDGE",
            )
            for key, owner in sorted(edge_owner_prefix.items())
        ]
        owner_corners = [
            corner_owner_row(
                json.loads(key),
                owner,
                label + "_INTERNAL_SPLIT_FACE_CORNER",
            )
            for key, owner in sorted(corner_owner_prefix.items())
        ]
        return owner_faces, owner_edges, owner_corners

    (
        round176_internal_faces,
        round176_internal_edges,
        round176_internal_corners,
    ) = internal_group(round176_split_faces, "ROUND176")
    (
        round180_internal_faces,
        round180_internal_edges,
        round180_internal_corners,
    ) = internal_group(split_faces, "ROUND180")

    parent_bounds = {
        "t": (original_parent.t0, original_parent.t1),
        "p": (original_parent.p0, original_parent.p1),
        "s": (original_parent.s0, original_parent.s1),
    }
    outer_faces: list[dict[str, Any]] = []
    for fixed_axis in axes:
        free_axes = [axis for axis in axes if axis != fixed_axis]
        spans = {
            axis: [
                str(parent_bounds[axis][0]),
                str(parent_bounds[axis][1]),
            ]
            for axis in free_axes
        }
        for coordinate in parent_bounds[fixed_axis]:
            outer_faces.append(face_owner_row(
                {
                    "fixed_axis": fixed_axis,
                    "coordinate": str(coordinate),
                    "spans": spans,
                },
                None,
                "OUTER_PARENT_FACE",
            ))
    outer_edges: list[dict[str, Any]] = []
    for free_axis in axes:
        fixed_axes = [axis for axis in axes if axis != free_axis]
        for first in parent_bounds[fixed_axes[0]]:
            for second in parent_bounds[fixed_axes[1]]:
                outer_edges.append(edge_owner_row(
                    {
                        "fixed": {
                            fixed_axes[0]: str(first),
                            fixed_axes[1]: str(second),
                        },
                        "free": {
                            free_axis: [
                                str(parent_bounds[free_axis][0]),
                                str(parent_bounds[free_axis][1]),
                            ]
                        },
                    },
                    None,
                    "OUTER_PARENT_EDGE",
                ))
    outer_corners = [
        corner_owner_row(
            {
                "t": str(t),
                "p": str(p),
                "s": str(s),
            },
            None,
            "OUTER_PARENT_CORNER",
        )
        for t in parent_bounds["t"]
        for p in parent_bounds["p"]
        for s in parent_bounds["s"]
    ]
    require(
        len(outer_faces) == 6
        and len(outer_edges) == 12
        and len(outer_corners) == 8,
        "outer parent strata exact census",
    )
    return {
        "trusted_legacy_ledger_conclusion_boolean": False,
        "owner_reduction_rule":
            "internal equality belongs to the lower child; recursively "
            "partition it into exact terminal descendants; parent outer "
            "strata use the unique half-open parent-side leaf partition",
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_proof_source_count":
            map_counter(Counter(proof_source.values())),
        "Round176_internal_2D_face_owner_row_count":
            len(round176_internal_faces),
        "Round176_internal_2D_face_owner_rows_sha256":
            digest(round176_internal_faces),
        "Round176_internal_1D_edge_owner_row_count":
            len(round176_internal_edges),
        "Round176_internal_1D_edge_owner_rows_sha256":
            digest(round176_internal_edges),
        "Round176_internal_0D_corner_owner_row_count":
            len(round176_internal_corners),
        "Round176_internal_0D_corner_owner_rows_sha256":
            digest(round176_internal_corners),
        "Round180_internal_2D_face_owner_row_count":
            len(round180_internal_faces),
        "Round180_internal_2D_face_owner_rows_sha256":
            digest(round180_internal_faces),
        "Round180_internal_1D_edge_owner_row_count":
            len(round180_internal_edges),
        "Round180_internal_1D_edge_owner_rows_sha256":
            digest(round180_internal_edges),
        "Round180_internal_0D_corner_owner_row_count":
            len(round180_internal_corners),
        "Round180_internal_0D_corner_owner_rows_sha256":
            digest(round180_internal_corners),
        "outer_2D_face_owner_row_count": len(outer_faces),
        "outer_2D_face_owner_rows_sha256": digest(outer_faces),
        "outer_1D_edge_owner_row_count": len(outer_edges),
        "outer_1D_edge_owner_rows_sha256": digest(outer_edges),
        "outer_0D_corner_owner_row_count": len(outer_corners),
        "outer_0D_corner_owner_rows_sha256": digest(outer_corners),
        "internal_and_outer_strata_classes_are_disjoint": True,
        "all_owner_rows_reduce_to_excluded_closed_3D_enclosures": True,
    }


def blocker_rank(name: str) -> tuple[int, str]:
    priorities = (
        "REDUCED_LIVE_3D_CELL",
        "CENTERED_ROOT_MARGIN_RECLASSIFIES_LIVE_3D",
        "MONOTONE_SAME_SIGN_RECLASSIFIES_LIVE_3D",
        "MULTI_DELTA_AND_ROOT_SIGN_ARRANGEMENT",
        "MULTI_ROOT_SIGN_EQUALITY_ARRANGEMENT",
        "MULTI_DELTA_GRAPH_ARRANGEMENT",
        "SINGLE_ROOT_SIGN_EQUALITY_COLLAR",
        "SINGLE_DELTA_P_DERIVATIVE_OVERWRAP",
        "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP",
        "SINGLE_DELTA_NO_FULL_OR_SAME_SIGN_FACE_CERTIFICATE",
        "SINGLE_FULL_DELTA_FIRST_ROOT_ORDER_NOT_STRICT",
        "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED",
        "FULL_DELTA_FROZEN_OWNER_OUTGOING_NOT_STRICT_MISMATCH",
        "MONOTONE_SAME_SIGN_RECLASSIFICATION",
        "NO_UNRESOLVED_RECORD_BUT",
    )
    for rank, prefix in enumerate(priorities):
        if name.startswith(prefix):
            return rank, name
    return len(priorities), name


def rebuild() -> dict[str, Any]:
    frozen = check_frozen_state()
    upstream = frozen.pop("upstream")
    registry_rows = upstream["certificate"]["result"][
        "priority_registry"
    ]["rows"]
    selected_rows = [
        row for row in registry_rows
        if row["priority_class"] == DELTA_MULTI_CLASS
    ]
    selected_keys = sorted(
        row["origin_key"] for row in selected_rows
    )
    compact_rows = [
        row for row in registry_rows
        if row["priority_class"] == COMPACT_CLASS
    ]
    compact_keys = sorted(
        row["origin_key"] for row in compact_rows
    )
    require(
        len(selected_rows) == EXPECTED_SELECTED_ORIGINS
        and digest(selected_keys) == EXPECTED_SELECTED_KEYS_SHA256
        and sum(
            row["Round180_residual_child_count"]
            for row in selected_rows
        )
        == EXPECTED_SELECTED_CHILDREN
        and all(
            row["selection_uses_new_closure_outcome"] is False
            for row in selected_rows
        ),
        "outcome-blind 596 registry selection",
    )
    require(
        len(compact_rows) == EXPECTED_COMPACT_ORIGINS
        and digest(compact_keys) == EXPECTED_COMPACT_KEYS_SHA256
        and sum(
            row["Round180_residual_child_count"]
            for row in compact_rows
        )
        == EXPECTED_COMPACT_CHILDREN
        and all(
            row["selection_uses_new_closure_outcome"] is False
            for row in compact_rows
        ),
        "outcome-blind 54 compact-q registry selection",
    )

    selected_set = set(selected_keys)
    compact_set = set(compact_keys)
    replay_set = selected_set | compact_set
    progress("Round215 replay frozen source-W frontier")
    replay = r176.replay_frontier()
    residual_roots: dict[str, list[Any]] = defaultdict(list)
    base_kinds: defaultdict[str, set[str]] = defaultdict(set)
    base_kinds.update({
        key: set(value)
        for key, value in replay["origin_kinds"].items()
        if key in replay_set
    })
    base_closed: Counter[str] = Counter()
    base_closed_volume: defaultdict[str, Q] = defaultdict(Q)
    base_closed_keys: defaultdict[str, list[str]] = defaultdict(list)
    base_closed_rows: defaultdict[str, list[Any]] = defaultdict(list)
    for row in replay["frontier"]:
        if row.origin_key not in replay_set:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            residual_roots[row.origin_key].append(row)
        else:
            base_kinds[row.origin_key].add(kind)
            base_closed[row.origin_key] += 1
            base_closed_volume[row.origin_key] += box_volume(row.box)
            base_closed_keys[row.origin_key].append(row.key)
            base_closed_rows[row.origin_key].append(row)
    require(
        set(residual_roots) == replay_set,
        "all mixed and compact-q origins reconstructed",
    )
    for rows in residual_roots.values():
        rows.sort(key=lambda row: row.key)

    registry_by_origin = {
        row["origin_key"]: row for row in selected_rows
    }
    residual_by_origin: dict[str, list[tuple[Any, dict[str, Any]]]] = {}
    total_children = 0
    total_closed = 0
    total_deleted_candidates = 0
    total_reason_count: Counter[str] = Counter()
    total_failure_reason: Counter[str] = Counter()
    total_category_reason: dict[str, Counter[str]] = defaultdict(Counter)
    selected_rows.sort(key=lambda row: row["priority_ordinal"])
    for index, registry in enumerate(selected_rows, 1):
        origin = registry["origin_key"]
        require(
            len(residual_roots[origin])
            == registry["Round176_residual_root_count"]
            and base_closed[origin]
            == registry["Round176_preclosed_frontier_count"]
            and sorted(base_kinds[origin])
            == registry["Round176_preclosed_kinds"],
            f"Round176 registry replay:{origin}",
        )
        refinement = r180.refine_origin(
            residual_roots[origin], 4
        )
        final_rows = sorted(
            refinement["final_residual_rows"],
            key=lambda row: row.key,
        )
        categories = Counter(
            r180.residual_category(row) for row in final_rows
        )
        require(
            len(final_rows)
            == registry["Round180_residual_child_count"]
            and digest([row.key for row in final_rows])
            == registry["Round180_residual_child_keys_sha256"]
            and str(sum(
                (box_volume(row.box) for row in final_rows), Q(0)
            ))
            == registry["Round180_residual_child_volume"]
            and map_counter(categories)
            == registry["Round180_residual_category_count"],
            f"Round180 registry replay:{origin}",
        )
        residual_rows: list[tuple[Any, dict[str, Any]]] = []
        for row in final_rows:
            category = r180.residual_category(row)
            reduction = exact_behind_reduce(row, category)
            total_children += 1
            total_deleted_candidates += len(
                reduction["eligible_targets"]
            )
            if reduction["closed"]:
                total_closed += 1
                continue
            residual_rows.append((row, reduction))
            total_reason_count[reduction["residual_reason"]] += 1
            total_category_reason[category][
                reduction["residual_reason"]
            ] += 1
            for candidate in reduction["candidate_evidence"]:
                if not candidate["eligible_exact_behind"]:
                    if not candidate["ell_strict_negative"]:
                        total_failure_reason[
                            "ELL_NOT_STRICT_NEGATIVE"
                        ] += 1
                    if not candidate[
                        "distance_margin_strict_positive"
                    ]:
                        total_failure_reason[
                            "DISTANCE_MARGIN_NOT_STRICT_POSITIVE"
                        ] += 1
        if residual_rows:
            residual_by_origin[origin] = residual_rows
        if index % 20 == 0 or index == len(selected_rows):
            progress(
                f"Round215 exact-behind origins {index}/"
                f"{len(selected_rows)}"
            )

    incomplete_keys = sorted(residual_by_origin)
    reconstruction_diagnostic = {
        "total_children": total_children,
        "incomplete_origin_count": len(incomplete_keys),
        "incomplete_keys_sha256": digest(incomplete_keys),
        "residual_cell_count":
            sum(len(value) for value in residual_by_origin.values()),
        "residual_reason_count": map_counter(total_reason_count),
        "failed_candidate_reason_count":
            map_counter(total_failure_reason),
    }
    progress(
        "Round215 reconstruction diagnostic "
        + canonical(reconstruction_diagnostic)
    )
    require(
        total_children == EXPECTED_SELECTED_CHILDREN,
        "Round197 total child count:"
        + canonical(reconstruction_diagnostic),
    )
    require(
        len(incomplete_keys) == EXPECTED_INCOMPLETE_ORIGINS,
        "Round197 incomplete origin count:"
        + canonical(reconstruction_diagnostic),
    )
    require(
        digest(incomplete_keys) == EXPECTED_INCOMPLETE_KEYS_SHA256,
        "Round197 incomplete key identity:"
        + canonical(reconstruction_diagnostic),
    )
    require(
        sum(len(value) for value in residual_by_origin.values())
        == EXPECTED_NONCOMPACT_RESIDUAL_CELLS,
        "Round197 residual cell count:"
        + canonical(reconstruction_diagnostic),
    )
    require(
        map_counter(total_reason_count)
        == EXPECTED_REDUCTION_REASON_COUNT,
        "Round197 residual reason partition:"
        + canonical(reconstruction_diagnostic),
    )
    require(
        map_counter(total_failure_reason)
        == {
            "ELL_NOT_STRICT_NEGATIVE":
                EXPECTED_MIXED_FAILED_CANDIDATES
        },
        "Round197 failed candidate reason partition:"
        + canonical(reconstruction_diagnostic),
    )

    compact_children = 0
    compact_closed = 0
    compact_deleted_candidates = 0
    compact_residual_count = 0
    compact_reason_count: Counter[str] = Counter()
    compact_failure_reason: Counter[str] = Counter()
    compact_category_reason: dict[str, Counter[str]] = defaultdict(Counter)
    compact_rows.sort(key=lambda row: row["priority_ordinal"])
    for index, registry in enumerate(compact_rows, 1):
        origin = registry["origin_key"]
        require(
            len(residual_roots[origin])
            == registry["Round176_residual_root_count"]
            and base_closed[origin]
            == registry["Round176_preclosed_frontier_count"]
            and sorted(base_kinds[origin])
            == registry["Round176_preclosed_kinds"],
            f"Round176 compact registry replay:{origin}",
        )
        refinement = r180.refine_origin(
            residual_roots[origin], 4
        )
        final_rows = sorted(
            refinement["final_residual_rows"],
            key=lambda row: row.key,
        )
        categories = Counter(
            r180.residual_category(row) for row in final_rows
        )
        require(
            len(final_rows)
            == registry["Round180_residual_child_count"]
            and digest([row.key for row in final_rows])
            == registry["Round180_residual_child_keys_sha256"]
            and str(sum(
                (box_volume(row.box) for row in final_rows), Q(0)
            ))
            == registry["Round180_residual_child_volume"]
            and map_counter(categories)
            == registry["Round180_residual_category_count"],
            f"Round180 compact registry replay:{origin}",
        )
        for row in final_rows:
            category = r180.residual_category(row)
            reduction = exact_behind_reduce(row, category)
            compact_children += 1
            compact_deleted_candidates += len(
                reduction["eligible_targets"]
            )
            if reduction["closed"]:
                compact_closed += 1
                continue
            compact_residual_count += 1
            compact_reason_count[reduction["residual_reason"]] += 1
            compact_category_reason[category][
                reduction["residual_reason"]
            ] += 1
            for candidate in reduction["candidate_evidence"]:
                if not candidate["eligible_exact_behind"]:
                    if not candidate["ell_strict_negative"]:
                        compact_failure_reason[
                            "ELL_NOT_STRICT_NEGATIVE"
                        ] += 1
                    if not candidate[
                        "distance_margin_strict_positive"
                    ]:
                        compact_failure_reason[
                            "DISTANCE_MARGIN_NOT_STRICT_POSITIVE"
                        ] += 1
        if index % 10 == 0 or index == len(compact_rows):
            progress(
                f"Round215 compact outer audit {index}/"
                f"{len(compact_rows)}"
            )

    compact_diagnostic = {
        "origin_count": len(compact_rows),
        "origin_keys_sha256": digest(compact_keys),
        "child_count": compact_children,
        "geometric_closed_cell_count": compact_closed,
        "geometric_residual_cell_count": compact_residual_count,
        "deleted_candidate_count": compact_deleted_candidates,
        "failed_candidate_reason_count":
            map_counter(compact_failure_reason),
        "residual_reason_count":
            map_counter(compact_reason_count),
    }
    progress(
        "Round215 compact outer diagnostic "
        + canonical(compact_diagnostic)
    )
    require(
        compact_children == EXPECTED_COMPACT_CHILDREN
        and compact_residual_count
        == EXPECTED_COMPACT_GEOMETRIC_RESIDUAL_CELLS
        and compact_closed + compact_residual_count
        == compact_children
        and map_counter(compact_failure_reason)
        == {
            "ELL_NOT_STRICT_NEGATIVE":
                EXPECTED_COMPACT_FAILED_CANDIDATES
        },
        "compact-q independent outer audit:"
        + canonical(compact_diagnostic),
    )
    global_diagnostic = {
        "origin_count":
            len(selected_rows) + len(compact_rows),
        "child_count": total_children + compact_children,
        "geometric_closed_cell_count":
            total_closed + compact_closed,
        "geometric_residual_cell_count":
            EXPECTED_NONCOMPACT_RESIDUAL_CELLS
            + compact_residual_count,
        "deleted_candidate_count":
            total_deleted_candidates + compact_deleted_candidates,
        "failed_candidate_count":
            sum(total_failure_reason.values())
            + sum(compact_failure_reason.values()),
    }
    progress(
        "Round215 global generalized diagnostic "
        + canonical(global_diagnostic)
    )
    require(
        global_diagnostic["origin_count"] == 650
        and global_diagnostic["child_count"]
        == EXPECTED_GLOBAL_GENERALIZED_CHILDREN
        and global_diagnostic["geometric_closed_cell_count"]
        == EXPECTED_GLOBAL_GEOMETRIC_CLOSED_CELLS
        and global_diagnostic["geometric_residual_cell_count"]
        == EXPECTED_GLOBAL_GEOMETRIC_RESIDUAL_CELLS
        and global_diagnostic["deleted_candidate_count"]
        == EXPECTED_GLOBAL_DELETED_CANDIDATES
        and global_diagnostic["failed_candidate_count"]
        == EXPECTED_GLOBAL_FAILED_CANDIDATES,
        "650-origin outer conservation:"
        + canonical(global_diagnostic),
    )

    seam_keys = sorted(RETAINED_SEAMS)
    require(
        digest(seam_keys) == EXPECTED_RETAINED_SEAM_KEYS_SHA256
        and all(key in residual_by_origin for key in seam_keys)
        and sum(
            len(residual_by_origin[key]) for key in seam_keys
        )
        == EXPECTED_SEAM_RESIDUAL_CELLS,
        "Round212 seams frozen outside active cohort",
    )
    active_keys = sorted(set(incomplete_keys) - set(seam_keys))
    require(
        len(active_keys) == EXPECTED_ACTIVE_ORIGINS
        and digest(active_keys) == EXPECTED_ACTIVE_KEYS_SHA256
        and sum(
            len(residual_by_origin[key]) for key in active_keys
        )
        == EXPECTED_ACTIVE_RESIDUAL_CELLS,
        "active 198 strict-interior cohort",
    )
    source_classes = Counter()
    for origin in active_keys:
        meta = replay["origins"][origin]
        source = r176.physical_domain(
            meta["chart_id"], meta["box"]
        )
        source_classes[source["classification"]] += 1
    require(
        len(source_classes) == 1
        and source_classes[r201.SOURCE_INTERIOR]
        == EXPECTED_ACTIVE_ORIGINS,
        "active cohort strict physical interior",
    )

    blocker_count: Counter[str] = Counter()
    blocker_volume: defaultdict[str, Q] = defaultdict(Q)
    method_count: Counter[str] = Counter()
    reason_count: Counter[str] = Counter()
    category_count: Counter[str] = Counter()
    category_blocker: dict[str, Counter[str]] = defaultdict(Counter)
    failure_blocker: dict[str, Counter[str]] = defaultdict(Counter)
    unresolved_cardinality: Counter[int] = Counter()
    unresolved_class_support: Counter[str] = Counter()
    centered_sign_count: Counter[str] = Counter()
    centered_sharpened = 0
    enhanced_outgoing_control_invocations = 0
    natural_strict_outgoing_control_count = 0
    owner_margin_attack_fixture: dict[str, Any] | None = None
    analytic_closed_cells: list[str] = []
    blocked_cells: list[str] = []
    cell_digest = ListDigest()
    origin_rows: list[dict[str, Any]] = []
    candidate_complete: list[str] = []
    candidate_cell_evidence: dict[str, list[dict[str, Any]]] = {}
    active_volume = Q(0)
    analytic_closed_volume = Q(0)
    blocked_volume = Q(0)

    for index, origin in enumerate(active_keys, 1):
        origin_blockers: Counter[str] = Counter()
        origin_methods: Counter[str] = Counter()
        origin_cell_hashes: list[str] = []
        origin_cell_evidence: list[dict[str, Any]] = []
        origin_volume = Q(0)
        origin_closed_volume = Q(0)
        for row, reduction in residual_by_origin[origin]:
            try:
                evidence = analyze_residual_cell(row, reduction)
            except Exception as error:
                raise RuntimeError(
                    f"Round215 active cell failure:{origin}:{row.key}:"
                    f"{type(error).__name__}:{error}"
                ) from error
            evidence = evidence | {
                "source_chart_id": row.chart_id,
                "closed_box": r176.box_row(row.box),
                "active_targets": list(row.active_targets),
            }
            boundary_proof = evidence.get(
                "closed_box_boundary_restriction_proof"
            )
            all_owned_boundary = bool(
                evidence["analytic_closed"]
                and evidence["method"]
                == "MONOTONE_P_SAME_SIGN_DELTA_STRICT_EXCLUSION"
                and boundary_proof
                and boundary_proof[
                    "Delta_endpoints_have_same_strict_sign"
                ]
                and boundary_proof[
                    "Delta_zero_graph_intersects_closed_box"
                ] is False
                and boundary_proof[
                    "post_enhancement_leaf"
                ] == "unique_first"
                and (
                    boundary_proof[
                        "unique_first_owner_mismatch_on_whole_closed_box"
                    ]
                    or boundary_proof[
                        "outgoing_owner_chart_mismatch_on_whole_closed_box"
                    ]
                )
                and boundary_proof[
                    "all_applicable_owner_chart_margins_strict"
                ]
                and boundary_proof[
                    "closed_box_strict_inequalities_restrict_to_all_"
                    "faces_edges_vertices"
                ]
            )
            evidence[
                "strict_closed_box_predicates_restrict_to_cell_"
                "faces_edges_vertices"
            ] = all_owned_boundary
            evidence["row_sha256"] = digest(evidence)
            row_hash = digest(evidence)
            cell_digest.add(evidence)
            origin_cell_hashes.append(row_hash)
            origin_cell_evidence.append(evidence)
            volume = box_volume(row.box)
            origin_volume += volume
            active_volume += volume
            reason_count[reduction["residual_reason"]] += 1
            category_count[reduction["category"]] += 1
            method_count[evidence["method"]] += 1
            origin_methods[evidence["method"]] += 1
            unresolved_cardinality[
                evidence["remaining_unresolved_target_count"]
            ] += 1
            support = "+".join(
                sorted(evidence["remaining_unresolved_class_count"])
            ) or "NONE"
            unresolved_class_support[support] += 1
            for centered in evidence["centered_root_sign_evidence"]:
                centered_sign_count[centered["centered_sign"]] += 1
                centered_sharpened += centered[
                    "centered_strictly_sharpens_overwrap"
                ]
            controls = [evidence["post_centered_outgoing_control"]]
            if "outgoing_enhanced_record_control" in evidence:
                controls.append(
                    evidence["outgoing_enhanced_record_control"]
                )
            enhanced_outgoing_control_invocations += len(controls)
            natural_strict_outgoing_control_count += sum(
                control["natural_strict_control_available"]
                for control in controls
            )
            if owner_margin_attack_fixture is None:
                named_controls = [
                    (
                        "post_centered_outgoing_control",
                        evidence["post_centered_outgoing_control"],
                    )
                ]
                if "outgoing_enhanced_record_control" in evidence:
                    named_controls.append((
                        "outgoing_enhanced_record_control",
                        evidence[
                            "outgoing_enhanced_record_control"
                        ],
                    ))
                for label, control in named_controls:
                    signs = control.get(
                        "enhanced_owner_margin_signs"
                    )
                    if signs is not None and len(signs) == 8:
                        owner_margin_attack_fixture = {
                            "cell_key": row.key,
                            "control_field": label,
                            "enhanced_owner_margin_signs": signs,
                            "all_eight_enhanced_owner_margins_strict":
                                control[
                                    "all_eight_enhanced_owner_"
                                    "margins_strict"
                                ],
                            "fixture_sha256": digest({
                                "cell_key": row.key,
                                "control_field": label,
                                "enhanced_owner_margin_signs": signs,
                            }),
                        }
                        break
            if evidence["analytic_closed"]:
                analytic_closed_cells.append(row.key)
                analytic_closed_volume += volume
                origin_closed_volume += volume
            else:
                blocker = evidence["blocker"]
                blocked_cells.append(row.key)
                blocked_volume += volume
                blocker_count[blocker] += 1
                blocker_volume[blocker] += volume
                origin_blockers[blocker] += 1
                category_blocker[reduction["category"]][blocker] += 1
                failure_blocker[row.failure][blocker] += 1
        all_closed = not origin_blockers
        if all_closed:
            candidate_complete.append(origin)
            candidate_cell_evidence[origin] = origin_cell_evidence
        first = (
            min(origin_blockers, key=blocker_rank)
            if origin_blockers
            else "NONE__ALL_RESIDUAL_CELLS_ANALYTICALLY_CLOSED"
        )
        origin_rows.append({
            "origin_key": origin,
            "priority_ordinal":
                registry_by_origin[origin]["priority_ordinal"],
            "source_domain_classification":
                r201.SOURCE_INTERIOR,
            "Round201_residual_cell_count":
                len(residual_by_origin[origin]),
            "Round201_residual_exact_volume": str(origin_volume),
            "Round215_analytic_closed_cell_count":
                len(residual_by_origin[origin])
                - sum(origin_blockers.values()),
            "Round215_analytic_closed_exact_volume":
                str(origin_closed_volume),
            "Round215_blocker_count":
                map_counter(origin_blockers),
            "Round215_method_count":
                map_counter(origin_methods),
            "first_obstruction": first,
            "all_Round201_residual_cells_analytically_closed":
                all_closed,
            "per_cell_evidence_hashes_sha256":
                digest(origin_cell_hashes),
        })
        if index % 20 == 0 or index == len(active_keys):
            progress(
                f"Round215 algebraic cells origins {index}/"
                f"{len(active_keys)}"
            )

    analytic_closed_cells.sort()
    blocked_cells.sort()
    candidate_complete.sort()
    require(
        len(analytic_closed_cells) + len(blocked_cells)
        == EXPECTED_ACTIVE_RESIDUAL_CELLS
        and analytic_closed_volume + blocked_volume == active_volume
        and cell_digest.count == EXPECTED_ACTIVE_RESIDUAL_CELLS
        and len(origin_rows) == EXPECTED_ACTIVE_ORIGINS,
        "active exact count/volume conservation",
    )
    require(
        owner_margin_attack_fixture is not None,
        "deterministic enhanced owner eight-margin attack fixture",
    )

    first_obstruction_count = Counter(
        row["first_obstruction"] for row in origin_rows
    )
    seam_residual_keys = sorted(
        row.key
        for origin in seam_keys
        for row, _reduction in residual_by_origin[origin]
    )
    seam_reason_count = Counter(
        reduction["residual_reason"]
        for origin in seam_keys
        for _row, reduction in residual_by_origin[origin]
    )
    formalization_candidate_rows: list[dict[str, Any]] = []
    for origin in candidate_complete:
        roots = residual_roots[origin]
        refinement = r180.refine_origin(roots, 4)
        final_rows = sorted(
            refinement["final_residual_rows"],
            key=lambda row: row.key,
        )
        inherited_terminals = sorted(
            refinement["terminal_rows"],
            key=lambda row: row["cell_key"],
        )
        inherited_dispositions = Counter(
            row["coarse_disposition"]
            for row in inherited_terminals
        )
        inherited_nonexcluded = [
            row for row in inherited_terminals
            if row["coarse_disposition"] != "EXCLUDED"
        ]
        root_volumes = {
            row.key: box_volume(row.box) for row in roots
        }
        inherited_volume = sum(
            (
                root_volumes[row["root_depth14_cell_key"]]
                * Q(
                    row["coverage_numerator"],
                    row["coverage_denominator"],
                )
                for row in inherited_terminals
            ),
            Q(0),
        )
        exact_behind_closed_count = 0
        exact_behind_closed_volume = Q(0)
        final_proof_source: dict[str, str] = {}
        rebuilt_residual_keys: list[str] = []
        rebuilt_residual_volume = Q(0)
        for row in final_rows:
            reduction = exact_behind_reduce(
                row, r180.residual_category(row)
            )
            if reduction["closed"]:
                exact_behind_closed_count += 1
                exact_behind_closed_volume += box_volume(row.box)
                final_proof_source[row.key] = (
                    "PINNED_ROUND201_EXACT_BEHIND_CLOSED_BOX"
                )
            else:
                rebuilt_residual_keys.append(row.key)
                rebuilt_residual_volume += box_volume(row.box)
                final_proof_source[row.key] = (
                    "ROUND215_EXPLICIT_STRICT_CLOSED_BOX"
                )
        expected_residual_keys = sorted(
            row.key for row, _reduction in residual_by_origin[origin]
        )
        require(
            rebuilt_residual_keys == expected_residual_keys,
            f"candidate residual identity:{origin}",
        )
        source_meta = replay["origins"][origin]
        prior_partition = reconstruct_round176_prior_partition(
            replay, origin
        )
        source = r176.physical_domain(
            source_meta["chart_id"], source_meta["box"]
        )
        input_root_volume = sum(root_volumes.values(), Q(0))
        original_parent_volume = box_volume(source_meta["box"])
        final_volume = sum(
            (box_volume(row.box) for row in final_rows), Q(0)
        )
        lower_ledger = r180.lower_strata_ledger(
            refinement["split_face_rows"]
        )
        refinement_leaves = reconstruct_refinement_leaf_frontiers(
            roots, refinement
        )
        leaf_rows = {
            row.key: row
            for row in base_closed_rows[origin]
        }
        leaf_rows.update(prior_partition["prior_closed_rows"])
        leaf_rows.update(refinement_leaves["terminal"])
        leaf_rows.update(refinement_leaves["final"])
        proof_source = {
            row.key: "PINNED_ROUND176_PRECLOSED_BOX"
            for row in base_closed_rows[origin]
        }
        proof_source.update({
            key: "PINNED_PRE_DEPTH14_CLOSED_BOX"
            for key in prior_partition["prior_closed_rows"]
        })
        proof_source.update({
            key: "PINNED_ROUND180_INHERITED_CLOSED_BOX"
            for key in refinement_leaves["terminal"]
        })
        proof_source.update(final_proof_source)
        owner_audit = strict_lower_strata_owner_audit(
            prior_partition["split_face_rows"],
            refinement["split_face_rows"],
            source_meta["box"],
            leaf_rows,
            proof_source,
        )
        all_owned_lower_strata_excluded = bool(
            owner_audit[
                "all_owner_rows_reduce_to_excluded_closed_3D_"
                "enclosures"
            ]
            and all(
                row[
                    "strict_closed_box_predicates_restrict_to_cell_"
                    "faces_edges_vertices"
                ]
                for row in candidate_cell_evidence[origin]
            )
        )
        require(
            source["classification"] == r201.SOURCE_INTERIOR
            and base_kinds[origin] == {"EXCLUDED"}
            and not inherited_nonexcluded
            and len(candidate_cell_evidence[origin])
            == len(rebuilt_residual_keys)
            and all(
                row["analytic_closed"]
                and row["method"]
                == "MONOTONE_P_SAME_SIGN_DELTA_STRICT_EXCLUSION"
                and row[
                    "strict_closed_box_predicates_restrict_to_cell_"
                    "faces_edges_vertices"
                ]
                for row in candidate_cell_evidence[origin]
            )
            and all_owned_lower_strata_excluded
            and owner_audit[
                "trusted_legacy_ledger_conclusion_boolean"
            ] is False
            and owner_audit[
                "Round180_internal_2D_face_owner_row_count"
            ] == len(refinement["split_face_rows"])
            and owner_audit[
                "Round180_internal_1D_edge_owner_row_count"
            ] == lower_ledger[
                "1D_deduplicated_split_face_edge_count"
            ]
            and owner_audit[
                "Round180_internal_0D_corner_owner_row_count"
            ] == lower_ledger[
                "0D_deduplicated_split_face_corner_count"
            ]
            and owner_audit["outer_2D_face_owner_row_count"] == 6
            and owner_audit["outer_1D_edge_owner_row_count"] == 12
            and owner_audit["outer_0D_corner_owner_row_count"] == 8
            and owner_audit[
                "Round176_internal_2D_face_owner_row_count"
            ] == len(prior_partition["split_face_rows"])
            and inherited_volume + final_volume == input_root_volume
            and (
                exact_behind_closed_volume + rebuilt_residual_volume
                == final_volume
            )
            and (
                prior_partition["prior_closed_exact_volume"]
                + base_closed_volume[origin] + input_root_volume
                == original_parent_volume
            ),
            f"candidate complete whole-origin partition:{origin}",
        )
        candidate_row = {
            "origin_key": origin,
            "priority_ordinal":
                registry_by_origin[origin]["priority_ordinal"],
            "selection_derived_only_after_full_198_origin_analysis": True,
            "source_chart_id": source_meta["chart_id"],
            "original_parent_box": r176.box_row(source_meta["box"]),
            "source_chart_domain": source,
            "Round176_preclosed_frontier_count":
                base_closed[origin],
            "Round176_preclosed_kinds":
                sorted(base_kinds[origin]),
            "Round176_preclosed_cell_keys_sha256":
                digest(sorted(base_closed_keys[origin])),
            "Round176_preclosed_exact_volume":
                str(base_closed_volume[origin]),
            "Round176_preclosed_all_excluded":
                base_kinds[origin] == {"EXCLUDED"},
            "Round176_prior_terminal_count":
                prior_partition["prior_closed_count"],
            "Round176_prior_coverage_numerator_64":
                prior_partition["prior_coverage_numerator_64"],
            "Round176_prior_terminal_exact_volume":
                str(prior_partition["prior_closed_exact_volume"]),
            "Round176_prior_terminal_evidence_rows_sha256":
                prior_partition[
                    "prior_closed_evidence_rows_sha256"
                ],
            "Round176_prior_all_excluded": True,
            "Round176_prior_split_face_count":
                len(prior_partition["split_face_rows"]),
            "Round176_prior_split_face_rows_sha256":
                digest(prior_partition["split_face_rows"]),
            "Round176_residual_root_count": len(roots),
            "Round176_residual_root_exact_volume":
                str(input_root_volume),
            "Round180_inherited_terminal_count":
                len(inherited_terminals),
            "Round180_inherited_terminal_count_by_coarse_disposition":
                map_counter(inherited_dispositions),
            "Round180_inherited_nonexcluded_terminal_count":
                len(inherited_nonexcluded),
            "Round180_all_inherited_terminals_excluded":
                not inherited_nonexcluded,
            "Round180_inherited_terminal_rows_sha256":
                digest(inherited_terminals),
            "Round180_inherited_terminal_exact_volume":
                str(inherited_volume),
            "Round180_final_cell_count": len(final_rows),
            "Round180_final_cell_keys_sha256":
                digest([row.key for row in final_rows]),
            "Round180_final_cell_exact_volume":
                str(final_volume),
            "Round201_exact_behind_closed_cell_count":
                exact_behind_closed_count,
            "Round201_exact_behind_closed_exact_volume":
                str(exact_behind_closed_volume),
            "Round201_residual_cell_count":
                len(rebuilt_residual_keys),
            "Round201_residual_cell_keys":
                rebuilt_residual_keys,
            "Round201_residual_cell_keys_sha256":
                digest(rebuilt_residual_keys),
            "Round201_residual_exact_volume":
                str(rebuilt_residual_volume),
            "Round215_new_terminal_cell_count":
                len(candidate_cell_evidence[origin]),
            "Round215_new_terminal_exact_volume":
                str(rebuilt_residual_volume),
            "Round215_new_terminal_rows":
                candidate_cell_evidence[origin],
            "Round215_new_terminal_rows_sha256":
                digest(candidate_cell_evidence[origin]),
            "Round180_split_face_count":
                len(refinement["split_face_rows"]),
            "Round180_split_face_rows_sha256":
                digest(refinement["split_face_rows"]),
            "lower_dimensional_strata": lower_ledger,
            "independent_lower_dimensional_owner_audit":
                owner_audit,
            "lower_dimensional_inheritance_derived_from_strict_"
            "predicates_and_rebuilt_ledger":
                all_owned_lower_strata_excluded,
            "prior_plus_frontier_base_plus_residual_roots_equals_"
            "original_parent": True,
            "inherited_plus_final_equals_residual_roots": True,
            "exact_behind_plus_Round215_equals_final_cells": True,
            "all_3D_2D_1D_0D_target_strata_excluded":
                all_owned_lower_strata_excluded,
            "whole_original_physical_parent_excluded": True,
            "whole_origin_integer_credit": 1,
            "child_count_or_volume_used_as_integer_credit": False,
        }
        candidate_row["row_sha256"] = digest(candidate_row)
        formalization_candidate_rows.append(candidate_row)
    require(
        [row["origin_key"] for row in formalization_candidate_rows]
        == candidate_complete,
        "formalization candidates exactly outcome-derived",
    )
    result = {
        "status":
            "READ_ONLY_ROUND215_MIXED_ALGEBRAIC_BLOCKER_CENSUS",
        "verdict": (
            "PROMOTION_CANDIDATES_REQUIRE_FORMALIZATION"
            if candidate_complete
            else "BOUNDED_PROBE_NO_WHOLE_ORIGIN_PROMOTION"
        ),
        "selection": {
            "selection_rule":
                "frozen Round184 priority_class DELTA_H_OR_MULTI_NO_Q; "
                "then independently rebuilt Round201 incomplete outcome; "
                "then remove exactly two frozen Round212 seam keys",
            "registry_selection_uses_Round215_outcome": False,
            "selected_registry_origin_count":
                EXPECTED_SELECTED_ORIGINS,
            "selected_registry_origin_keys_sha256":
                EXPECTED_SELECTED_KEYS_SHA256,
            "outer_audit_compact_q_origin_count":
                EXPECTED_COMPACT_ORIGINS,
            "outer_audit_compact_q_origin_keys_sha256":
                EXPECTED_COMPACT_KEYS_SHA256,
            "compact_q_used_only_for_650_scope_conservation": True,
            "independently_rebuilt_incomplete_origin_count":
                EXPECTED_INCOMPLETE_ORIGINS,
            "independently_rebuilt_incomplete_keys_sha256":
                EXPECTED_INCOMPLETE_KEYS_SHA256,
            "active_strict_source_interior_origin_count":
                EXPECTED_ACTIVE_ORIGINS,
            "active_origin_keys_sha256":
                EXPECTED_ACTIVE_KEYS_SHA256,
            "active_source_domain_count":
                map_counter(source_classes),
        },
        "frozen_state": frozen,
        "Round197_independent_reconstruction": {
            "scope": "596 mixed-only origins",
            "selected_Round180_child_count": total_children,
            "exact_behind_closed_child_count": total_closed,
            "deleted_candidate_count": total_deleted_candidates,
            "noncompact_residual_cell_count":
                EXPECTED_NONCOMPACT_RESIDUAL_CELLS,
            "residual_reason_count":
                map_counter(total_reason_count),
            "failed_candidate_reason_count":
                map_counter(total_failure_reason),
            "category_by_residual_reason":
                nested_counter(total_category_reason),
            "incomplete_origin_count":
                len(incomplete_keys),
            "incomplete_origin_keys_sha256":
                digest(incomplete_keys),
            "count_conservation":
                total_closed
                + EXPECTED_NONCOMPACT_RESIDUAL_CELLS
                == total_children,
        },
        "generalized_650_scope_split_outer_conservation": {
            "selection_uses_Round215_outcome": False,
            "mixed": {
                "origin_count": len(selected_rows),
                "origin_keys_sha256": digest(selected_keys),
                "child_count": total_children,
                "geometric_closed_cell_count": total_closed,
                "geometric_residual_cell_count":
                    EXPECTED_NONCOMPACT_RESIDUAL_CELLS,
                "deleted_candidate_count":
                    total_deleted_candidates,
                "failed_candidate_reason_count":
                    map_counter(total_failure_reason),
            },
            "compact_q": {
                "origin_count": len(compact_rows),
                "origin_keys_sha256": digest(compact_keys),
                "child_count": compact_children,
                "geometric_closed_cell_count": compact_closed,
                "geometric_residual_cell_count":
                    compact_residual_count,
                "deleted_candidate_count":
                    compact_deleted_candidates,
                "failed_candidate_reason_count":
                    map_counter(compact_failure_reason),
                "geometric_residual_reason_count":
                    map_counter(compact_reason_count),
                "category_by_geometric_residual_reason":
                    nested_counter(compact_category_reason),
                "Round215_active_theorem_applied": False,
                "retained_for_independent_source_stratum": True,
                "whole_origin_integer_credit": 0,
            },
            "global_650": global_diagnostic,
            "mixed_plus_compact_exact_conservation": True,
        },
        "Round212_seam_exclusion": {
            "seam_origin_count": len(seam_keys),
            "seam_origin_keys": seam_keys,
            "seam_origin_keys_sha256": digest(seam_keys),
            "seam_residual_cell_count":
                len(seam_residual_keys),
            "seam_residual_cell_keys_sha256":
                digest(seam_residual_keys),
            "seam_residual_reason_count":
                map_counter(seam_reason_count),
            "mixed_into_Round215_active_cohort": False,
            "whole_origin_integer_credit": 0,
        },
        "active_algebraic_census": {
            "active_residual_cell_count":
                EXPECTED_ACTIVE_RESIDUAL_CELLS,
            "active_residual_exact_volume": str(active_volume),
            "exact_behind_residual_reason_count":
                map_counter(reason_count),
            "original_residual_category_count":
                map_counter(category_count),
            "method_count": map_counter(method_count),
            "remaining_unresolved_target_count_per_cell":
                map_counter(unresolved_cardinality),
            "remaining_unresolved_class_support":
                map_counter(unresolved_class_support),
            "centered_distance_margin_sign_count":
                map_counter(centered_sign_count),
            "centered_distance_margin_strict_sharpen_count":
                centered_sharpened,
            "enhanced_outgoing_control_invocation_count":
                enhanced_outgoing_control_invocations,
            "natural_strict_outgoing_control_count":
                natural_strict_outgoing_control_count,
            "natural_strict_controls_chart_exact_equal": True,
            "natural_strict_controls_all_eight_margin_overlap":
                True,
            "owner_margin_attack_fixture":
                owner_margin_attack_fixture,
            "analytic_closed_cell_count":
                len(analytic_closed_cells),
            "analytic_closed_exact_volume":
                str(analytic_closed_volume),
            "analytic_closed_cell_keys_sha256":
                digest(analytic_closed_cells),
            "blocked_cell_count": len(blocked_cells),
            "blocked_exact_volume": str(blocked_volume),
            "blocked_cell_keys_sha256": digest(blocked_cells),
            "blocker_count": map_counter(blocker_count),
            "blocker_exact_volume":
                fraction_map(blocker_volume),
            "blocker_count_by_original_category":
                nested_counter(category_blocker),
            "blocker_count_by_original_failure":
                nested_counter(failure_blocker),
            "per_cell_evidence_rows_sha256":
                cell_digest.finish(),
            "exact_count_and_volume_conservation": True,
        },
        "whole_origin_outcome": {
            "candidate_complete_origin_count":
                len(candidate_complete),
            "candidate_complete_origin_keys":
                candidate_complete,
            "candidate_complete_origin_keys_sha256":
                digest(candidate_complete),
            "still_blocked_origin_count":
                EXPECTED_ACTIVE_ORIGINS
                - len(candidate_complete),
            "first_obstruction_origin_count":
                map_counter(first_obstruction_count),
            "per_origin_rows": origin_rows,
            "per_origin_rows_sha256": digest(origin_rows),
            "formalization_candidate_rows":
                formalization_candidate_rows,
            "formalization_candidate_rows_sha256":
                digest(formalization_candidate_rows),
            "official_whole_origin_integer_credit": 0,
        },
        "dimension_safety": {
            "active_objects_are_three_dimensional_closed_cells": True,
            "full_Delta_graph_method_accounts_for":
                ["3D Delta<0", "2D Delta=0", "3D Delta>0",
                 "1D graph/face intersections",
                 "0D graph edge/corner intersections"],
            "centered_C0_strict_bounds_inherit_to_owned_faces": True,
            "child_cell_count_promoted_as_integer_credit": 0,
            "analytic_sheet_count_promoted_as_integer_credit": 0,
            "one_dimensional_count_promoted_as_integer_credit": 0,
            "zero_dimensional_count_promoted_as_integer_credit": 0,
            "only_complete_original_origin_may_later_be_promoted": True,
        },
        "next_theorem": {
            "priority_rule":
                "largest blocker population first, but reduced-live 3D "
                "cells remain hard non-exclusion blockers",
            "required_for_single_root_sign":
                "formal centered C0/C1 root-equality cylinder partition "
                "with first-root and outgoing-owner recomputation",
            "required_for_clipped_single_Delta":
                "centered/Krawczyk graph collar on the overwrapped p face "
                "and its owned 1D/0D boundary",
            "required_for_multi_Delta":
                "rank-aware multi-graph arrangement with exact first-root "
                "ordering on every 3D/2D/1D/0D stratum",
            "blind_deep_subdivision_authorized": False,
        },
        "strict_nonpromotion": {
            "probe_only": True,
            "filesystem_writes": 0,
            "official_ledger_mutated": False,
            "Round212_excluded": 74_582,
            "Round212_conservative_live": 2_250,
            "Round212_remaining_priority_origins": 254,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "Gate5": "10/18",
            "complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return result


def main() -> int:
    ctx.prec = 192
    result = rebuild()
    document = {
        "schema": SCHEMA,
        "probe_result": result,
        "probe_result_sha256": digest(result),
    }
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
