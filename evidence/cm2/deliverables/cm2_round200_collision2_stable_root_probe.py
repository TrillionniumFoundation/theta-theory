#!/usr/bin/env python3
"""Read-only stable-root probe for Round185 point-winner residuals.

Round185 evaluates a future collision root as ``ell - sqrt(Delta)``.
On narrow boxes this expression may overwrap zero through interval
subtraction even when the exact root is strictly positive.  This probe
independently evaluates the algebraically identical, cancellation-free form

    near = (distance^2 - radius^2) / (ell + sqrt(Delta))

whenever centered C0 proves ``Delta > 0`` and both numerator and denominator
are strictly positive.  The corresponding stable far-root formula is used
when ``ell < 0``.  Every candidate is then reclassified before owner
selection.

The probe is diagnostic only.  It does not write files, materialize formal
rows, or award whole-parent, Gate5, D02, or global credit.
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
SCHEMA = "cm2.round200.collision2-stable-root-probe.v1"
MAX_INPUT_BYTES = 180 * 1024 * 1024

ROUND185_FILES = {
    "cm2_round185_preconditioned_c1_residual_refinement.py":
        "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "cm2_round185_preconditioned_c1_residual_refinement_certificate.json":
        "2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1",
    "cm2_round185_preconditioned_c1_residual_refinement_verifier.py":
        "88d5b72c68ba216a1c807b868156c8e0da7e9e63db968eda5b5a66dd86d5651f",
    "cm2_round185_preconditioned_c1_residual_refinement_verification.json":
        "bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e",
    "cm2_round185_preconditioned_c1_residual_refinement_report.md":
        "77e29b55ff4be771fce34e3032b92ed52e94ab0833e20a069f491ad227ae7619",
    "cm2_round185_preconditioned_c1_residual_refinement_cold_replay.md":
        "c14d3908a42746c7ff8a60f5f07319e0bd86b2f94d27154a3126b8f895447a7d",
    "cm2_round185_preconditioned_c1_residual_refinement_manifest.sha256":
        "ec018e261e866b48039d1cf775e972c6a9b1a9558a1ecf043665c6340ad3dc26",
}
ROUND185_CERT = (
    "cm2_round185_preconditioned_c1_residual_refinement_certificate.json"
)
ROUND185_VERIFICATION = (
    "cm2_round185_preconditioned_c1_residual_refinement_verification.json"
)
ROUND185_RESULT = (
    "ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf"
)
ROUND185_VERIFICATION_RESULT = (
    "b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6"
)
EXPECTED_DYNAMIC_RESIDUAL = 15830
EXPECTED_POINT_WINNER = 9076
EXPECTED_STATUS_COUNTS = {
    "ACTIVE_DELTA_1": 4170,
    "ACTIVE_DELTA_2": 220,
    "H2_FACTOR_EXISTENCE_RESIDUAL": 592,
    "POINT_WINNER_NONSTRICT": 9076,
    "WALL_ENDPOINT": 1772,
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise RuntimeError(f"noninteger JSON number:{value}")


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=duplicate_guard,
        parse_float=reject_number,
        parse_constant=reject_number,
    )
    require(type(value) is dict, f"JSON top-level:{label}")
    return value


def read_regular(path: Path) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input resolved parent:{absolute.name}",
    )
    before = absolute.lstat()
    require(stat.S_ISREG(before.st_mode), f"input regular:{absolute.name}")
    require(not absolute.is_symlink(), f"input symlink:{absolute.name}")
    require(before.st_nlink == 1, f"input hardlink:{absolute.name}")
    require(
        0 < before.st_size <= MAX_INPUT_BYTES,
        f"input size:{absolute.name}",
    )
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (before.st_dev, before.st_ino),
            f"input race:{absolute.name}",
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == before.st_size,
            f"opened input metadata:{absolute.name}",
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
    require(len(raw) == before.st_size, f"input byte count:{absolute.name}")
    return raw


def pin_round185() -> dict[str, bytes]:
    raw: dict[str, bytes] = {}
    for name, expected in ROUND185_FILES.items():
        payload = read_regular(HERE / name)
        require(
            hashlib.sha256(payload).hexdigest() == expected,
            f"Round185 pin:{name}",
        )
        raw[name] = payload
    manifest_lines = raw[
        "cm2_round185_preconditioned_c1_residual_refinement_manifest.sha256"
    ].decode("ascii", "strict").splitlines()
    require(
        len(manifest_lines) == 6
        and all(
            line == f"{ROUND185_FILES[name]}  {name}"
            for line, name in zip(
                manifest_lines,
                tuple(ROUND185_FILES)[:6],
                strict=True,
            )
        ),
        "Round185 manifest content and order",
    )
    return raw


PINNED_RAW = pin_round185()
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r185 = importlib.import_module(
    "cm2_round185_preconditioned_c1_residual_refinement"
)
PINNED_RAW = pin_round185()
r181 = r185.r181
r178 = r185.r178
registry = r185.registry


def load_formal_result() -> dict[str, Any]:
    require(
        Path(r185.__file__).resolve()
        == (
            HERE
            / "cm2_round185_preconditioned_c1_residual_refinement.py"
        ).resolve(),
        "Round185 imported module identity",
    )
    certificate = strict_json(PINNED_RAW[ROUND185_CERT], ROUND185_CERT)
    verification = strict_json(
        PINNED_RAW[ROUND185_VERIFICATION], ROUND185_VERIFICATION
    )
    require(
        certificate["result_sha256"] == ROUND185_RESULT
        and digest(certificate["result"]) == ROUND185_RESULT,
        "Round185 certificate result",
    )
    require(
        verification["result_sha256"] == ROUND185_VERIFICATION_RESULT
        and digest(verification["result"]) == ROUND185_VERIFICATION_RESULT
        and verification["result"]["status"] == "PASS"
        and verification["result"][
            "full_expected_result_canonical_equality"
        ],
        "Round185 verification result",
    )
    return certificate["result"]


def sign_name(value: Any) -> str:
    if bool(value > 0):
        return "STRICT_POSITIVE"
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    return "OVERWRAP"


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def direct_distance_margin(
    geometry: tuple[Any, Any, Any, Any, Any],
    identifier: str,
) -> Any:
    qx, qy, _ux, _uy, s = geometry
    ax, ay = r178.target_center(identifier, s)
    dx, dy = ax - qx, ay - qy
    radius = r178.RADIUS[identifier[0]]
    return dx * dx + dy * dy - radius * radius


def centered_delta(
    parent_key: str,
    box: Any,
    identifier: str,
) -> tuple[Any | None, dict[str, Any]]:
    evidence = r185.surface_evidence(
        "DELTA",
        parent_key,
        box,
        identifier,
        include_axis_tests=False,
    )
    sign = evidence["centered_C0_sign"]
    if sign == "NEGATIVE":
        return None, evidence
    if sign != "POSITIVE":
        return None, evidence
    bounds = evidence["centered_mean_value_C0_enclosure"]
    value = r185.ge.arb_hull(
        arb(bounds["lower"]).lower(),
        arb(bounds["upper"]).upper(),
    )
    require(bool(value > 0), f"positive centered Delta:{identifier}")
    return value, evidence


def stable_root_record(
    parent_key: str,
    box: Any,
    geometry: tuple[Any, Any, Any, Any, Any],
    identifier: str,
) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
    base_kind, base_data = r178.root_record(*geometry, identifier)
    if base_kind in {
        "NO_REAL_INTERSECTION",
        "INTERSECTION_BEHIND",
        "STRICT_FUTURE",
    }:
        return base_kind, base_data, {
            "mode": f"BASE_{base_kind}",
            "centered_C0_sign": "NOT_NEEDED",
        }

    delta, surface = centered_delta(parent_key, box, identifier)
    centered_sign = surface["centered_C0_sign"]
    if centered_sign == "NEGATIVE":
        return "NO_REAL_INTERSECTION", None, {
            "mode": "CENTERED_C0_NO_REAL_INTERSECTION",
            "centered_C0_sign": centered_sign,
            "surface_evidence_sha256": digest(surface),
        }
    if delta is None:
        return base_kind, None, {
            "mode": f"RESIDUAL_{base_kind}",
            "centered_C0_sign": centered_sign,
            "surface_evidence_sha256": digest(surface),
        }

    raw = r181.raw_candidate(geometry, identifier)
    ell = raw["ell"]
    radical = delta.sqrt()
    direct = direct_distance_margin(geometry, identifier)
    identity = ell * ell - delta
    require(
        bool(direct.overlaps(identity)),
        f"distance identity overlap:{parent_key}:{box.path}:{identifier}",
    )
    if bool(ell > 0) and bool(direct > 0):
        denominator = ell + radical
        require(bool(denominator > 0), f"stable near denominator:{identifier}")
        near = direct / denominator
        require(bool(near > 0), f"stable near positive:{identifier}")
        raw_near = ell - radical
        require(
            bool(near.overlaps(raw_near)),
            f"stable/raw near overlap:{identifier}",
        )
        return "STRICT_FUTURE", {
            "near": near,
            "radical": radical,
            "transverse": raw["transverse"],
            "radius": raw["radius"],
        }, {
            "mode": "STABLE_RATIONALIZED_NEAR_STRICT_FUTURE",
            "centered_C0_sign": centered_sign,
            "ell_sign": "STRICT_POSITIVE",
            "direct_distance_margin_sign": "STRICT_POSITIVE",
            "surface_evidence_sha256": digest(surface),
        }
    if bool(ell < 0) and bool(direct > 0):
        denominator = -ell + radical
        require(bool(denominator > 0), f"stable far denominator:{identifier}")
        far = -direct / denominator
        require(bool(far < 0), f"stable far negative:{identifier}")
        raw_far = ell + radical
        require(
            bool(far.overlaps(raw_far)),
            f"stable/raw far overlap:{identifier}",
        )
        return "INTERSECTION_BEHIND", None, {
            "mode": "STABLE_RATIONALIZED_FAR_INTERSECTION_BEHIND",
            "centered_C0_sign": centered_sign,
            "ell_sign": "STRICT_NEGATIVE",
            "direct_distance_margin_sign": "STRICT_POSITIVE",
            "surface_evidence_sha256": digest(surface),
        }
    return base_kind, None, {
        "mode": f"RESIDUAL_{base_kind}",
        "centered_C0_sign": centered_sign,
        "ell_sign": sign_name(ell),
        "direct_distance_margin_sign": sign_name(direct),
        "surface_evidence_sha256": digest(surface),
    }


def stable_select_owner(
    parent_key: str,
    box: Any,
) -> tuple[str, tuple[str, dict[str, Any]] | None, list[dict[str, Any]]]:
    state = r181.collision1_state_direct(parent_key, box)
    geometry = r185.r183.collision2_geometry(state)
    rows: dict[str, tuple[str, dict[str, Any] | None]] = {}
    evidence_rows: list[dict[str, Any]] = []
    for identifier in r185.CANDIDATES:
        kind, data, evidence = stable_root_record(
            parent_key, box, geometry, identifier
        )
        rows[identifier] = kind, data
        evidence_rows.append({
            "identifier": identifier,
            "root_kind": kind,
            **evidence,
        })
    future = [
        (identifier, data)
        for identifier, (kind, data) in rows.items()
        if kind == "STRICT_FUTURE" and data is not None
    ]
    unresolved = [
        identifier
        for identifier, (kind, _data) in rows.items()
        if kind in {"UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}
    ]
    winners = [
        (identifier, data)
        for identifier, data in future
        if all(
            identifier == other_identifier
            or bool(data["near"] < other_data["near"])
            for other_identifier, other_data in future
        )
    ]
    if len(winners) == 1 and not unresolved:
        return "STRICT_UNIQUE_OWNER", winners[0], evidence_rows
    reason = (
        "UNRESOLVED_CANDIDATE_ROOTS"
        if unresolved
        else "STRICT_FUTURE_ROOT_ORDER_OVERWRAP"
    )
    return reason, None, evidence_rows


class StreamingListDigest:
    def __init__(self) -> None:
        self._hasher = hashlib.sha256()
        self._hasher.update(b"[")
        self._count = 0

    def add(self, value: Any) -> None:
        if self._count:
            self._hasher.update(b",")
        self._hasher.update(canonical_bytes(value))
        self._count += 1

    def finish(self) -> str:
        self._hasher.update(b"]")
        return self._hasher.hexdigest()


def counter_map(counter: Counter[Any]) -> dict[str, int]:
    return {
        str(key): value for key, value in sorted(counter.items())
    }


def volume_map(values: dict[str, Q]) -> dict[str, str]:
    return {key: str(value) for key, value in sorted(values.items())}


def analyze(formal: dict[str, Any]) -> dict[str, Any]:
    ledger = formal["dynamic_residual_ledger"]
    rows = ledger["rows"]
    require(
        len(rows) == ledger["row_count"] == EXPECTED_DYNAMIC_RESIDUAL,
        "Round185 dynamic row count",
    )
    status_counts = Counter(row["status"] for row in rows)
    require(
        dict(sorted(status_counts.items())) == EXPECTED_STATUS_COUNTS,
        "Round185 dynamic status census",
    )
    point_rows = [
        row for row in rows if row["status"] == "POINT_WINNER_NONSTRICT"
    ]
    require(len(point_rows) == EXPECTED_POINT_WINNER, "point-winner count")
    point_rows.sort(
        key=lambda row: (row["origin_parent_key"], row["terminal_path"])
    )

    pair_index, pattern_index, registry_digest = registry.key_index_tables()
    require(
        registry_digest == r178.GATE5_REGISTRY_DIGEST,
        "Gate5 registry digest",
    )

    input_volume = Q(0)
    outcome_volume: defaultdict[str, Q] = defaultdict(Q)
    owner_status_counts: Counter[str] = Counter()
    downstream_counts: Counter[str] = Counter()
    candidate_mode_counts: Counter[str] = Counter()
    candidate_root_counts: Counter[str] = Counter()
    point_owner_mode_counts: Counter[str] = Counter()
    selected_owner_counts: Counter[str] = Counter()
    residual_identifier_counts: Counter[str] = Counter()
    per_origin_input: Counter[str] = Counter()
    per_origin_residual: Counter[str] = Counter()
    exact_row_keys: list[str] = []
    residual_row_keys: list[str] = []
    evidence_digest = StreamingListDigest()
    first_examples: dict[str, dict[str, Any]] = {}

    for index, row in enumerate(point_rows, 1):
        parent_key = row["origin_parent_key"]
        box = r185.box_from_payload(row["box"], row["terminal_path"])
        volume = box_volume(box)
        require(
            volume == Q(row["box"]["volume"]),
            f"row volume:{parent_key}:{box.path}",
        )
        input_volume += volume
        per_origin_input[parent_key] += 1

        owner_status, selected, evidence_rows = stable_select_owner(
            parent_key, box
        )
        owner_status_counts[owner_status] += 1
        for evidence in evidence_rows:
            candidate_mode_counts[evidence["mode"]] += 1
            candidate_root_counts[evidence["root_kind"]] += 1
            if evidence["identifier"] == row["detail"]["point_owner"]:
                point_owner_mode_counts[evidence["mode"]] += 1
            if evidence["root_kind"] in {
                "UNRESOLVED_DELTA",
                "UNRESOLVED_ROOT_SIGN",
            }:
                residual_identifier_counts[evidence["identifier"]] += 1

        if owner_status == "STRICT_UNIQUE_OWNER" and selected is not None:
            selected_owner_counts[selected[0]] += 1
            downstream_status, downstream_detail, h2_evidence = (
                r185.finish_collision2_owner(
                    parent_key,
                    box,
                    selected,
                    pair_index,
                    pattern_index,
                )
            )
            downstream = downstream_status
            detail_digest = digest(downstream_detail)
            h2_digest = digest(h2_evidence)
        else:
            downstream = owner_status
            detail_digest = digest({})
            h2_digest = digest([])
        downstream_counts[downstream] += 1
        outcome_volume[downstream] += volume

        locally_exact = downstream.startswith("LOCAL_EXACT_KEY")
        row_key = f"{parent_key}:{box.path}"
        if locally_exact:
            exact_row_keys.append(row_key)
        else:
            residual_row_keys.append(row_key)
            per_origin_residual[parent_key] += 1

        compact = {
            "origin_parent_key": parent_key,
            "terminal_path": box.path,
            "input_point_owner": row["detail"]["point_owner"],
            "stable_owner_status": owner_status,
            "selected_owner":
                selected[0] if selected is not None else "NONE",
            "downstream_status": downstream,
            "candidate_evidence_sha256": digest(evidence_rows),
            "downstream_detail_sha256": detail_digest,
            "downstream_H2_evidence_sha256": h2_digest,
            "locally_exact_3D": locally_exact,
            "whole_parent_or_stratum_credit": 0,
            "global_credit": 0,
        }
        evidence_digest.add(compact)
        first_examples.setdefault(downstream, compact)
        if index % 500 == 0 or index == len(point_rows):
            print(
                f"stable-root point-winner {index}/{len(point_rows)}",
                file=sys.stderr,
                flush=True,
            )

    require(
        sum(downstream_counts.values()) == EXPECTED_POINT_WINNER
        and sum(outcome_volume.values(), Q(0)) == input_volume,
        "count and exact-volume conservation",
    )
    complete_cohort_origins = sorted(
        origin
        for origin in per_origin_input
        if per_origin_residual.get(origin, 0) == 0
    )
    residual_cohort_origins = sorted(
        origin
        for origin in per_origin_input
        if per_origin_residual.get(origin, 0) != 0
    )
    require(
        len(complete_cohort_origins) + len(residual_cohort_origins)
        == len(per_origin_input),
        "cohort origin partition",
    )
    verdict = (
        "VALIDATED"
        if not residual_row_keys
        else "PARTIAL"
        if exact_row_keys
        else "INVALIDATED"
    )
    return {
        "spike_verdict": verdict,
        "scope": "Round185 POINT_WINNER_NONSTRICT dynamic residual rows only",
        "input_row_count": len(point_rows),
        "input_origin_count": len(per_origin_input),
        "input_exact_coordinate_volume": str(input_volume),
        "stable_owner_status_count": counter_map(owner_status_counts),
        "downstream_status_count": counter_map(downstream_counts),
        "downstream_exact_coordinate_volume":
            volume_map(outcome_volume),
        "candidate_root_kind_occurrence":
            counter_map(candidate_root_counts),
        "candidate_resolution_mode_occurrence":
            counter_map(candidate_mode_counts),
        "input_point_owner_resolution_mode_count":
            counter_map(point_owner_mode_counts),
        "selected_owner_count": counter_map(selected_owner_counts),
        "residual_identifier_occurrence":
            counter_map(residual_identifier_counts),
        "locally_exact_3D_row_count": len(exact_row_keys),
        "locally_exact_3D_row_keys_sha256": digest(exact_row_keys),
        "residual_row_count": len(residual_row_keys),
        "residual_row_keys_sha256": digest(residual_row_keys),
        "complete_within_point_winner_cohort_origin_count":
            len(complete_cohort_origins),
        "complete_within_point_winner_cohort_origin_keys_sha256":
            digest(complete_cohort_origins),
        "residual_within_point_winner_cohort_origin_count":
            len(residual_cohort_origins),
        "residual_within_point_winner_cohort_origin_keys_sha256":
            digest(residual_cohort_origins),
        "per_row_compact_evidence_sha256": evidence_digest.finish(),
        "first_example_by_downstream_status": {
            key: first_examples[key] for key in sorted(first_examples)
        },
        "stable_identity_contract": {
            "near":
                "(distance^2-radius^2)/(ell+sqrt(Delta))",
            "far":
                "-(distance^2-radius^2)/(-ell+sqrt(Delta))",
            "precondition":
                "centered C0 Delta>0 and strict signs on the full closed box",
            "raw_and_stable_interval_enclosures_required_to_overlap": True,
        },
        "strict_nonpromotion": {
            "probe_only": True,
            "formal_materialized_row_count": 0,
            "whole_parent_or_stratum_credit": 0,
            "global_credit": 0,
            "D02": "BLOCKED",
            "Gate5": "10/18",
            "complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> None:
    require(
        ctx.prec == 384 and getattr(r185.flint, "__version__", "") == "0.9.0",
        "python-flint runtime",
    )
    formal = load_formal_result()
    result = analyze(formal)
    envelope = {
        "schema": SCHEMA,
        "probe_only": True,
        "Round185_formal_result_sha256": ROUND185_RESULT,
        "probe_result": result,
    }
    envelope["result_sha256"] = digest(result)
    print(canonical_bytes(envelope).decode())


if __name__ == "__main__":
    main()
