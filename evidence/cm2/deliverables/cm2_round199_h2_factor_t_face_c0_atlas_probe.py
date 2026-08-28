#!/usr/bin/env python3
"""Read-only endpoint-face C0-atlas probe for the Round185 H2 residual.

Round185 retained 592 boxes where exactly one of

    H2 = HPLUS * HMINUS

was strictly absent and the other factor had strict C1 regularity but no
certified zero-set existence statement.  This spike reconstructs those
records from the pinned Round185 certificate, fixes t as the graph axis, and
builds a complete centered-C0 atlas on both t-endpoint faces.  A face that is
not strict in one shot is covered by exact rational p-bisection cells to
depth at most two.

The decisive rules deliberately separate regularity from existence:

* a strict derivative never proves that a zero exists;
* absence needs a single strict full-box dt sign and two complete endpoint
  face C0 atlases whose every cell has the same strict sign;
* a full graph needs complete endpoint-face atlases with opposite signs; and
* every other case remains residual.

The script has no output-path option and writes only its JSON result to
stdout.  It emits compact per-box evidence hashes, not a formal certificate,
and grants neither whole-parent nor global credit.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib
import json
from pathlib import Path
import stat
import sys
from typing import Any

import flint


HERE = Path(__file__).resolve().parent
PROBE = Path(__file__).resolve()
SCHEMA = "cm2.round199.h2-factor-t-face-c0-atlas-probe.v1"

R185_PREFIX = "cm2_round185_preconditioned_c1_residual_refinement"
R185_PRODUCER = f"{R185_PREFIX}.py"
R185_CERTIFICATE = f"{R185_PREFIX}_certificate.json"
R185_VERIFIER = f"{R185_PREFIX}_verifier.py"
R185_VERIFICATION = f"{R185_PREFIX}_verification.json"
R185_REPORT = f"{R185_PREFIX}_report.md"
R185_COLD_REPLAY = f"{R185_PREFIX}_cold_replay.md"
R185_MANIFEST = f"{R185_PREFIX}_manifest.sha256"
R185_PINS = {
    R185_PRODUCER:
        "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    R185_CERTIFICATE:
        "2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1",
    R185_VERIFIER:
        "88d5b72c68ba216a1c807b868156c8e0da7e9e63db968eda5b5a66dd86d5651f",
    R185_VERIFICATION:
        "bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e",
    R185_REPORT:
        "77e29b55ff4be771fce34e3032b92ed52e94ab0833e20a069f491ad227ae7619",
    R185_COLD_REPLAY:
        "c14d3908a42746c7ff8a60f5f07319e0bd86b2f94d27154a3126b8f895447a7d",
}
R185_MANIFEST_SHA256 = (
    "ec018e261e866b48039d1cf775e972c6a9b1a9558a1ecf043665c6340ad3dc26"
)
R185_CERTIFICATE_SCHEMA = (
    "cm2.round185.preconditioned-c1-residual-refinement.v1"
)
R185_VERIFICATION_SCHEMA = (
    "cm2.round185.preconditioned-c1-residual-refinement-verification.v1"
)
R185_RESULT_SHA256 = (
    "ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf"
)
R185_VERIFICATION_RESULT_SHA256 = (
    "b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6"
)
R185_DYNAMIC_RESIDUAL_ROWS_SHA256 = (
    "707577c77ef26050b331c3be4e657431dcfade82a4caec51d3a65a26e37d0f73"
)

EXPECTED_INPUT_COUNT = 592
EXPECTED_INPUT_VOLUME = Q(2301, 2684354560000)
EXPECTED_PARENT_COUNTS = {
    "W:E:00.14.01101": 264,
    "W:E:02.11.110": 32,
    "W:E:05.04.001": 32,
    "W:E:07.01.10010": 264,
}
EXPECTED_OWNER_COUNTS = {"W[1,-1]": 296, "W[1,1]": 296}
EXPECTED_ACTIVE_FACTOR_COUNTS = {"HMINUS": 296, "HPLUS": 296}
EXPECTED_FIXED_FACTOR_COUNTS = {"HMINUS": 296, "HPLUS": 296}
EXPECTED_DYNAMIC_STATUS_COUNTS = {
    "ACTIVE_DELTA_1": 4170,
    "ACTIVE_DELTA_2": 220,
    "H2_FACTOR_EXISTENCE_RESIDUAL": 592,
    "POINT_WINNER_NONSTRICT": 9076,
    "WALL_ENDPOINT": 1772,
}
EXPECTED_DYNAMIC_STATUS_VOLUMES = {
    "ACTIVE_DELTA_1": "1593/107374182400",
    "ACTIVE_DELTA_2": "5133/5368709120000",
    "H2_FACTOR_EXISTENCE_RESIDUAL": "2301/2684354560000",
    "POINT_WINNER_NONSTRICT": "54339/1342177280000",
    "WALL_ENDPOINT": "219657/26843545600000",
}

AXES = ("t", "p", "s")
SIGNS = {"NEGATIVE", "POSITIVE"}
CLASSIFICATIONS = (
    "ACTIVE_FACTOR_ZERO_ABSENT",
    "FULL_2D_GRAPH",
    "T_FACE_C0_ATLAS_RESIDUAL",
)
T_FACE_P_ATLAS_MAX_DEPTH = 2
MAX_INPUT_BYTES = 160 * 1024 * 1024


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


def file_sha256(path: Path, maximum: int = MAX_INPUT_BYTES) -> str:
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(metadata.st_nlink == 1, f"hardlink:{path.name}")
    require(metadata.st_size <= maximum, f"oversized:{path.name}")
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def read_regular(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(metadata.st_nlink == 1, f"hardlink:{path.name}")
    require(metadata.st_size <= maximum, f"oversized:{path.name}")
    data = path.read_bytes()
    require(len(data) == metadata.st_size, f"stable-size:{path.name}")
    return data


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise RuntimeError(f"noninteger JSON number:{value}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str and "\x00" not in key,
                f"JSON key:{path}",
            )
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"JSON NUL:{path}")


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"JSON parse:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    require(
        raw == canonical_bytes(value) + b"\n",
        f"canonical JSON:{label}",
    )
    return value


def manifest_entries(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise RuntimeError("manifest ASCII") from exc
    require(text.endswith("\n"), "manifest final newline")
    result: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split("  ", 1)
        require(len(parts) == 2, "manifest line shape")
        value, name = parts
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value),
            f"manifest digest:{name}",
        )
        require(
            name not in result
            and "/" not in name
            and "\\" not in name
            and name not in {".", ".."},
            f"manifest name:{name}",
        )
        result[name] = value
    return result


def load_and_pin_round185() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in R185_PINS.items():
        require(
            file_sha256(HERE / name) == expected,
            f"Round185 file pin:{name}",
        )
    require(
        file_sha256(HERE / R185_MANIFEST) == R185_MANIFEST_SHA256,
        "Round185 manifest pin",
    )
    require(
        manifest_entries(read_regular(HERE / R185_MANIFEST)) == R185_PINS,
        "Round185 manifest exact six entries",
    )

    certificate = strict_json(
        read_regular(HERE / R185_CERTIFICATE),
        R185_CERTIFICATE,
    )
    verification = strict_json(
        read_regular(HERE / R185_VERIFICATION),
        R185_VERIFICATION,
    )
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == R185_CERTIFICATE_SCHEMA
        and certificate["result_sha256"] == R185_RESULT_SHA256
        and digest(certificate["result"]) == R185_RESULT_SHA256,
        "Round185 certificate wrapper",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["schema"] == R185_VERIFICATION_SCHEMA
        and verification["result_sha256"]
        == R185_VERIFICATION_RESULT_SHA256
        and digest(verification["result"])
        == R185_VERIFICATION_RESULT_SHA256,
        "Round185 verification wrapper",
    )
    checked = verification["result"]
    require(
        checked["status"] == "PASS"
        and checked["certificate_result_sha256"] == R185_RESULT_SHA256
        and checked["independently_rebuilt_result_sha256"]
        == R185_RESULT_SHA256
        and checked["full_expected_result_canonical_equality"] is True
        and checked["producer_imported_or_executed"] is False
        and checked["re_signed_semantic_attacks"]["rejected"] == 32
        and checked["re_signed_semantic_attacks"]["total"] == 32
        and checked["strict_JSON_attacks"]["rejected"] == 9
        and checked["strict_JSON_attacks"]["total"] == 9
        and checked["path_attacks"]["rejected"] == 11
        and checked["path_attacks"]["total"] == 11,
        "Round185 accepted independent verification",
    )

    result = certificate["result"]
    require(
        result["status"]
        == "PARTIAL_PRECONDITIONED_C0_C1_RESIDUAL_REFINEMENT"
           "__NO_WHOLE_PARENT_PROMOTION",
        "Round185 partial status",
    )
    nonpromotion = result["strict_nonpromotion"]
    require(
        nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["global_Gate5_fields"] == "10/18"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM"
        and nonpromotion["global_complete_18_field_blocks"] == 0,
        "Round185 nonpromotion state",
    )
    ledger = result["dynamic_residual_ledger"]
    require(
        ledger["row_count"] == 15830
        and ledger["rows_sha256"] == R185_DYNAMIC_RESIDUAL_ROWS_SHA256
        and digest(ledger["rows"]) == R185_DYNAMIC_RESIDUAL_ROWS_SHA256
        and ledger["status_counts"] == EXPECTED_DYNAMIC_STATUS_COUNTS
        and ledger["status_volumes"] == EXPECTED_DYNAMIC_STATUS_VOLUMES,
        "Round185 dynamic residual ledger",
    )
    pins = {
        "Round185_manifest_sha256": R185_MANIFEST_SHA256,
        "Round185_manifest_entry_count": len(R185_PINS),
        "Round185_certificate_file_sha256":
            R185_PINS[R185_CERTIFICATE],
        "Round185_certificate_result_sha256": R185_RESULT_SHA256,
        "Round185_verifier_file_sha256": R185_PINS[R185_VERIFIER],
        "Round185_verification_file_sha256":
            R185_PINS[R185_VERIFICATION],
        "Round185_verification_result_sha256":
            R185_VERIFICATION_RESULT_SHA256,
        "Round185_verification_status": "PASS",
        "Round185_full_expected_result_canonical_equality": True,
        "Round185_semantic_JSON_path_attacks_rejected": "32/32,9/9,11/11",
    }
    return result, pins


def qstr(value: Q) -> str:
    return str(value)


def sign_name(value: int) -> str:
    return "POSITIVE" if value > 0 else "NEGATIVE" if value < 0 else "UNRESOLVED"


def opposite(left: str, right: str) -> bool:
    return left in SIGNS and right in SIGNS and left != right


def bounds(box: Any) -> tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]:
    return (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    )


def fixed_label(fixed: dict[int, int]) -> str:
    return "|".join(
        f"{AXES[axis]}{'+' if bit else '-'}"
        for axis, bit in sorted(fixed.items())
    )


def factor_chart(hplus: str, hminus: str) -> str:
    require(hplus in SIGNS and hminus in SIGNS, "strict chart factors")
    if hplus == hminus:
        return "E" if hplus == "POSITIVE" else "W"
    return "N" if hplus == "POSITIVE" else "S"


def strip_row_sha256(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "row_sha256"}


class FactorAtlas:
    """One active-factor atlas on one exact rational box."""

    def __init__(
        self,
        module: Any,
        parent_key: str,
        box: Any,
        identifier: str,
        factor: str,
    ) -> None:
        self.module = module
        self.parent_key = parent_key
        self.box = box
        self.identifier = identifier
        self.factor = factor
        self.function = (
            module.outgoing_hplus_ad
            if factor == "HPLUS"
            else module.outgoing_hminus_ad
        )
        self.cache: dict[tuple[tuple[int, int], ...], dict[str, Any]] = {}

    def subbox(self, fixed: dict[int, int]) -> Any:
        cell = self.box
        original = bounds(self.box)
        for axis, bit in sorted(fixed.items()):
            cell = self.module.fixed_axis_box(
                cell,
                axis,
                original[axis][bit],
                "." + fixed_label({axis: bit}),
            )
        return cell

    def evidence(self, fixed: dict[int, int]) -> dict[str, Any]:
        key = tuple(sorted(fixed.items()))
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        cell = self.subbox(fixed)
        full = self.function(
            self.parent_key,
            cell,
            self.identifier,
        )[0]
        center = tuple((low + high) / 2 for low, high in bounds(cell))
        center_box = self.module.point_box(
            cell,
            *center,
            ".round199-centered-C0",
        )
        center_value = self.function(
            self.parent_key,
            center_box,
            self.identifier,
        )[0].value
        centered = center_value
        for derivative, (low, high) in zip(
            full.derivative,
            bounds(cell),
        ):
            width = (high - low) / 2
            centered += derivative * self.module.BASE.arb_interval(
                -width,
                width,
            )

        direct_sign = self.module.strict_sign(full.value)
        centered_sign = self.module.strict_sign(centered)
        require(
            not (
                direct_sign != 0
                and centered_sign != 0
                and direct_sign != centered_sign
            ),
            f"direct/centered sign consistency:{fixed_label(fixed)}",
        )
        selected_sign = centered_sign or direct_sign
        derivative_signs = tuple(
            self.module.strict_sign(value) for value in full.derivative
        )
        record = {
            "factor": self.factor,
            "fixed_coordinates": {
                AXES[axis]: (
                    str(bounds(self.box)[axis][bit])
                )
                for axis, bit in sorted(fixed.items())
            },
            "dimension": sum(
                low < high for low, high in bounds(cell)
            ),
            "direct_C0": self.module.arb_bounds(full.value),
            "centered_mean_value_C0": self.module.arb_bounds(centered),
            "direct_C0_sign": sign_name(direct_sign),
            "centered_C0_sign": sign_name(centered_sign),
            "selected_C0_sign": sign_name(selected_sign),
            "selected_C0_method": (
                "CENTERED_MEAN_VALUE"
                if centered_sign != 0
                else "DIRECT_INTERVAL"
                if direct_sign != 0
                else "UNRESOLVED"
            ),
            "C1_derivatives": {
                axis: {
                    **self.module.arb_bounds(value),
                    "strict_sign": sign_name(derivative_signs[index]),
                }
                for index, (axis, value) in enumerate(
                    zip(AXES, full.derivative)
                )
            },
            "strict_derivative_axes": [
                axis
                for axis, value in zip(AXES, derivative_signs)
                if value != 0
            ],
            "regularity_is_not_existence": True,
        }
        record["evidence_sha256"] = digest(record)
        self.cache[key] = record
        return record

    def t_face_c0_atlas(self, bit: int) -> dict[str, Any]:
        """Cover one complete t-face by strict centered-C0 p-cells."""

        face = self.subbox({0: bit})
        face_area = (
            (face.p1 - face.p0) * (face.s1 - face.s0)
        )
        pending = [(face, 0, "")]
        terminal_rows: list[dict[str, Any]] = []
        split_count = 0
        while pending:
            cell, depth, path = pending.pop()
            local = FactorAtlas(
                self.module,
                self.parent_key,
                cell,
                self.identifier,
                self.factor,
            )
            evidence = local.evidence({})
            sign = evidence["centered_C0_sign"]
            if sign in SIGNS or depth == T_FACE_P_ATLAS_MAX_DEPTH:
                area = (
                    (cell.p1 - cell.p0) * (cell.s1 - cell.s0)
                )
                terminal_rows.append({
                    "p_refinement_path": path,
                    "relative_depth": depth,
                    "p": [str(cell.p0), str(cell.p1)],
                    "s": [str(cell.s0), str(cell.s1)],
                    "exact_face_area": str(area),
                    "centered_C0_sign": sign,
                    "centered_C0_bounds":
                        evidence["centered_mean_value_C0"],
                    "cell_evidence_sha256": evidence["evidence_sha256"],
                })
                continue
            left, right = self.module.split_axis(cell, 1)
            require(
                left.p0 == cell.p0
                and left.p1 == right.p0
                and right.p1 == cell.p1
                and left.t0 == left.t1 == face.t0
                and right.t0 == right.t1 == face.t0,
                "exact rational p-bisection",
            )
            split_count += 1
            pending.extend(((right, depth + 1, path + "1"),
                            (left, depth + 1, path + "0")))
        terminal_rows.sort(key=lambda row: row["p_refinement_path"])
        signs = {
            row["centered_C0_sign"] for row in terminal_rows
        }
        complete = (
            signs <= SIGNS
            and len(signs) == 1
            and sum(
                (Q(row["exact_face_area"]) for row in terminal_rows),
                Q(0),
            ) == face_area
        )
        return {
            "face_id": "t-" if bit == 0 else "t+",
            "t_coordinate": str(face.t0),
            "exact_face_area": str(face_area),
            "p_refinement_max_depth": max(
                row["relative_depth"] for row in terminal_rows
            ),
            "split_count": split_count,
            "terminal_cell_count": len(terminal_rows),
            "terminal_rows": terminal_rows,
            "terminal_rows_sha256": digest(terminal_rows),
            "all_terminal_centered_C0_enclosures_strict": (
                signs <= SIGNS
            ),
            "all_terminal_signs_identical": len(signs) == 1,
            "resolved_face_sign": (
                next(iter(signs)) if len(signs) == 1 else None
            ),
            "exact_face_area_conserved": (
                sum(
                    (Q(row["exact_face_area"]) for row in terminal_rows),
                    Q(0),
                ) == face_area
            ),
            "complete_C0_atlas": complete,
        }


def official_factor_records(
    module: Any,
    row: dict[str, Any],
    box: Any,
) -> tuple[dict[str, dict[str, Any]], str, str]:
    parent_key = row["origin_parent_key"]
    identifier = row["detail"]["point_owner"]
    records = module.hfactor_records(parent_key, box, identifier)
    evidence = [records["HPLUS"], records["HMINUS"]]
    summaries = [
        module.compact_surface_summary(records["HPLUS"]),
        module.compact_surface_summary(records["HMINUS"]),
    ]
    require(
        summaries == row["surface_summaries"]
        and digest(evidence) == row["surface_evidence_rows_sha256"],
        f"Round185 surface evidence reconstruction:{row['terminal_path']}",
    )
    by_kind = {
        summary["kind"]: summary for summary in summaries
    }
    active = [
        kind for kind in ("HPLUS", "HMINUS")
        if by_kind[kind]["centered_C0_sign"] == "UNRESOLVED"
    ]
    fixed = [
        kind for kind in ("HPLUS", "HMINUS")
        if by_kind[kind]["centered_C0_sign"] in SIGNS
    ]
    require(
        len(active) == len(fixed) == 1
        and by_kind[fixed[0]]["centered_C0_sign"] == "NEGATIVE"
        and by_kind[active[0]]["strict_derivative_axes"] == ["dt", "dp"]
        and by_kind[fixed[0]]["strict_derivative_axes"] == [],
        f"one-active-one-fixed factor structure:{row['terminal_path']}",
    )
    return records, active[0], fixed[0]


def classify_box(
    module: Any,
    row: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        digest(strip_row_sha256(row)) == row["row_sha256"],
        f"Round185 row digest:{row['terminal_path']}",
    )
    box = module.box_from_payload(row["box"], row["terminal_path"])
    exact_volume = module.volume(box)
    require(
        exact_volume == Q(row["box"]["volume"]) and exact_volume > 0,
        f"box exact volume:{row['terminal_path']}",
    )
    records, active, fixed = official_factor_records(module, row, box)
    active_atlas = FactorAtlas(
        module,
        row["origin_parent_key"],
        box,
        row["detail"]["point_owner"],
        active,
    )
    fixed_atlas = FactorAtlas(
        module,
        row["origin_parent_key"],
        box,
        row["detail"]["point_owner"],
        fixed,
    )
    active_full = active_atlas.evidence({})
    fixed_full = fixed_atlas.evidence({})
    require(
        active_full["selected_C0_sign"] == "UNRESOLVED"
        and active_full["strict_derivative_axes"] == ["t", "p"]
        and fixed_full["selected_C0_sign"] == "NEGATIVE",
        f"fresh centered C0/C1 structure:{row['terminal_path']}",
    )
    t_faces = [
        active_atlas.t_face_c0_atlas(bit) for bit in (0, 1)
    ]
    t_face_signs = [
        face["resolved_face_sign"] for face in t_faces
    ]
    dt_sign = active_full["C1_derivatives"]["t"]["strict_sign"]
    complete_faces = all(
        face["complete_C0_atlas"] for face in t_faces
    )
    same_sign_faces = (
        complete_faces
        and t_face_signs[0] == t_face_signs[1]
        and t_face_signs[0] in SIGNS
    )
    opposite_sign_faces = (
        complete_faces and opposite(*t_face_signs)
    )
    direction_consistent = (
        same_sign_faces
        or (
            dt_sign == "POSITIVE"
            and t_face_signs == ["NEGATIVE", "POSITIVE"]
        )
        or (
            dt_sign == "NEGATIVE"
            and t_face_signs == ["POSITIVE", "NEGATIVE"]
        )
    )

    active_resolved_sign: str | None = None
    potential_chart: str | None = None
    proof_basis: str
    if (
        same_sign_faces
        and dt_sign in SIGNS
        and direction_consistent
    ):
        classification = "ACTIVE_FACTOR_ZERO_ABSENT"
        active_resolved_sign = t_face_signs[0]
        proof_basis = (
            "ONE_STRICT_FULL_BOX_DT_SIGN_PLUS_TWO_COMPLETE_SAME_SIGN"
            "_CENTERED_C0_T_FACE_ATLASES"
        )
        hplus = (
            active_resolved_sign
            if active == "HPLUS"
            else fixed_full["selected_C0_sign"]
        )
        hminus = (
            active_resolved_sign
            if active == "HMINUS"
            else fixed_full["selected_C0_sign"]
        )
        potential_chart = factor_chart(hplus, hminus)
    elif (
        opposite_sign_faces
        and dt_sign in SIGNS
        and direction_consistent
    ):
        classification = "FULL_2D_GRAPH"
        proof_basis = (
            "ONE_STRICT_FULL_BOX_DT_SIGN_PLUS_TWO_COMPLETE_OPPOSITE_SIGN"
            "_CENTERED_C0_T_FACE_ATLASES"
        )
    else:
        classification = "T_FACE_C0_ATLAS_RESIDUAL"
        proof_basis = (
            "REGULARITY_RETAINED_BUT_ENDPOINT_FACE_C0_ATLAS_INCOMPLETE"
        )

    full_evidence = {
        "origin_parent_key": row["origin_parent_key"],
        "terminal_path": row["terminal_path"],
        "box": row["box"],
        "identifier": row["detail"]["point_owner"],
        "active_factor": active,
        "fixed_absent_factor": fixed,
        "official_factor_evidence_sha256": {
            kind: digest(records[kind])
            for kind in ("HPLUS", "HMINUS")
        },
        "fresh_active_full_box_evidence": active_full,
        "fresh_fixed_full_box_evidence": fixed_full,
        "t_endpoint_face_C0_atlases": t_faces,
        "t_endpoint_face_signs": t_face_signs,
        "t_endpoint_face_signs_identical": same_sign_faces,
        "dt_and_endpoint_sign_direction_consistent": direction_consistent,
        "classification": classification,
        "proof_basis": proof_basis,
        "active_resolved_sign": active_resolved_sign,
        "potential_local_outgoing_chart": potential_chart,
        "whole_parent_or_stratum_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }
    compact = {
        "origin_parent_key": row["origin_parent_key"],
        "terminal_path": row["terminal_path"],
        "box_volume": str(exact_volume),
        "point_owner": row["detail"]["point_owner"],
        "Round185_input_row_sha256": row["row_sha256"],
        "Round185_surface_evidence_rows_sha256":
            row["surface_evidence_rows_sha256"],
        "active_factor": active,
        "fixed_absent_factor": fixed,
        "selected_full_box_graph_axis": "t",
        "active_dt_sign": dt_sign,
        "active_dp_sign":
            active_full["C1_derivatives"]["p"]["strict_sign"],
        "fixed_factor_sign": fixed_full["selected_C0_sign"],
        "t_endpoint_face_methods": [
            (
                "DIRECT_FULL_FACE_CENTERED_C0"
                if face["p_refinement_max_depth"] == 0
                else "EXACT_P_REFINED_CENTERED_C0_ATLAS_DEPTH_"
                + str(face["p_refinement_max_depth"])
            )
            for face in t_faces
        ],
        "t_endpoint_face_terminal_cell_counts": [
            face["terminal_cell_count"] for face in t_faces
        ],
        "t_endpoint_face_atlas_max_depths": [
            face["p_refinement_max_depth"] for face in t_faces
        ],
        "t_endpoint_face_signs": t_face_signs,
        "both_t_endpoint_faces_have_complete_centered_C0_atlases":
            complete_faces,
        "t_endpoint_face_signs_identical": same_sign_faces,
        "dt_and_endpoint_sign_direction_consistent": direction_consistent,
        "classification": classification,
        "proof_basis": proof_basis,
        "active_resolved_sign": active_resolved_sign,
        "potential_local_outgoing_chart": potential_chart,
        "t_minus_face_atlas_sha256": digest(t_faces[0]),
        "t_plus_face_atlas_sha256": digest(t_faces[1]),
        "full_box_evidence_sha256": digest(full_evidence),
        "probe_local_credit_issued": 0,
        "probe_global_credit_issued": 0,
    }
    compact["evidence_hash_row_sha256"] = digest(compact)
    return compact, {
        "volume": exact_volume,
        "t_faces": t_faces,
        "counterexample_flags": {
            "non_strict_full_box_dt": dt_sign not in SIGNS,
            "incomplete_t_face_C0_atlas": not complete_faces,
            "mixed_or_unresolved_t_face_cell_sign": any(
                not face["all_terminal_centered_C0_enclosures_strict"]
                or not face["all_terminal_signs_identical"]
                for face in t_faces
            ),
            "opposite_t_face_signs": opposite_sign_faces,
            "dt_endpoint_direction_contradiction":
                not direction_consistent,
        },
    }


def counter_dict(counter: Counter[Any]) -> dict[str, int]:
    return {
        str(key): value
        for key, value in sorted(
            counter.items(),
            key=lambda item: str(item[0]),
        )
    }


def volume_dict(counter: dict[str, Q]) -> dict[str, str]:
    return {
        key: str(counter.get(key, Q(0)))
        for key in CLASSIFICATIONS
    }


def main() -> int:
    require(len(sys.argv) == 1, "Round199 accepts no arguments")
    print("pinning Round185 six-file formal delivery", file=sys.stderr)
    round185, pins = load_and_pin_round185()

    print("loading pinned Round185 independent evaluator", file=sys.stderr)
    flint.ctx.prec = 384
    module = importlib.import_module(
        "cm2_round185_preconditioned_c1_residual_refinement_verifier"
    )
    require(
        Path(module.__file__).resolve() == (HERE / R185_VERIFIER).resolve()
        and file_sha256(Path(module.__file__).resolve())
        == R185_PINS[R185_VERIFIER]
        and flint.__version__ == "0.9.0"
        and module.atlas.ctx.prec == 384,
        "pinned Round185 evaluator identity",
    )

    all_dynamic = round185["dynamic_residual_ledger"]["rows"]
    rows = [
        row for row in all_dynamic
        if row["status"] == "H2_FACTOR_EXISTENCE_RESIDUAL"
    ]
    require(
        len(rows) == EXPECTED_INPUT_COUNT
        and rows == sorted(
            rows,
            key=lambda row: (
                row["origin_parent_key"],
                row["terminal_path"],
            ),
        )
        and len({row["terminal_path"] for row in rows})
        == EXPECTED_INPUT_COUNT,
        "Round185 H2 cohort exact sorted census",
    )
    require(
        Counter(row["origin_parent_key"] for row in rows)
        == EXPECTED_PARENT_COUNTS
        and Counter(row["detail"]["point_owner"] for row in rows)
        == EXPECTED_OWNER_COUNTS,
        "Round185 H2 parent/owner census",
    )

    classification_counts: Counter[str] = Counter()
    classification_volumes = {
        key: Q(0) for key in CLASSIFICATIONS
    }
    parent_counts: Counter[str] = Counter()
    parent_volumes: Counter[str] = Counter()
    owner_counts: Counter[str] = Counter()
    active_factor_counts: Counter[str] = Counter()
    fixed_factor_counts: Counter[str] = Counter()
    graph_axis_counts: Counter[str] = Counter()
    active_derivative_sign_counts: Counter[str] = Counter()
    active_resolved_sign_counts: Counter[str] = Counter()
    potential_chart_counts: Counter[str] = Counter()
    t_endpoint_proof_counts: Counter[str] = Counter()
    t_endpoint_depth_counts: Counter[str] = Counter()
    t_endpoint_cell_counts: Counter[str] = Counter()
    t_endpoint_sign_counts: Counter[str] = Counter()
    same_sign_direction_cross_counts: Counter[str] = Counter()
    counterexample_counts: Counter[str] = Counter()
    per_parent_classification_counts: Counter[str] = Counter()
    per_parent_factor_counts: Counter[str] = Counter()
    t_face_terminal_cell_total = 0
    evidence_hash_rows = []
    exact_input_volume = Q(0)

    print(
        "rebuilding 592 factor records and endpoint-face C0 atlases",
        file=sys.stderr,
    )
    for index, row in enumerate(rows, 1):
        compact, diagnostics = classify_box(module, row)
        classification = compact["classification"]
        require(classification in CLASSIFICATIONS, "known classification")
        volume = diagnostics["volume"]
        exact_input_volume += volume
        classification_counts[classification] += 1
        classification_volumes[classification] += volume
        parent = compact["origin_parent_key"]
        active = compact["active_factor"]
        fixed = compact["fixed_absent_factor"]
        owner = compact["point_owner"]
        parent_counts[parent] += 1
        parent_volumes[parent] += volume
        owner_counts[owner] += 1
        active_factor_counts[active] += 1
        fixed_factor_counts[fixed] += 1
        graph_axis_counts[compact["selected_full_box_graph_axis"]] += 1
        active_derivative_sign_counts[
            compact["active_dt_sign"]
            + "|"
            + compact["active_dp_sign"]
        ] += 1
        active_resolved_sign_counts[
            str(compact["active_resolved_sign"])
        ] += 1
        potential_chart_counts[
            str(compact["potential_local_outgoing_chart"])
        ] += 1
        per_parent_classification_counts[
            parent + "|" + classification
        ] += 1
        per_parent_factor_counts[
            parent + "|" + active + "|" + fixed
        ] += 1
        for endpoint, method, depth, cells, sign in zip(
            ("t-", "t+"),
            compact["t_endpoint_face_methods"],
            compact["t_endpoint_face_atlas_max_depths"],
            compact["t_endpoint_face_terminal_cell_counts"],
            compact["t_endpoint_face_signs"],
        ):
            t_endpoint_proof_counts[
                parent + "|" + active + "|" + endpoint + "|" + method
            ] += 1
            t_endpoint_depth_counts[
                active + "|" + endpoint + "|depth=" + str(depth)
            ] += 1
            t_endpoint_cell_counts[
                active + "|" + endpoint + "|cells=" + str(cells)
            ] += 1
            t_endpoint_sign_counts[
                active + "|" + endpoint + "|" + str(sign)
            ] += 1
            t_face_terminal_cell_total += cells
        same_sign_direction_cross_counts[
            active
            + "|dt="
            + compact["active_dt_sign"]
            + "|t-="
            + str(compact["t_endpoint_face_signs"][0])
            + "|t+="
            + str(compact["t_endpoint_face_signs"][1])
            + "|methods="
            + compact["t_endpoint_face_methods"][0]
            + ","
            + compact["t_endpoint_face_methods"][1]
        ] += 1
        for label, triggered in diagnostics[
            "counterexample_flags"
        ].items():
            counterexample_counts[label] += int(triggered)
        evidence_hash_rows.append(compact)
        if index % 64 == 0 or index == len(rows):
            print(
                f"Round199 t-face C0 atlas {index}/{len(rows)}",
                file=sys.stderr,
                flush=True,
            )

    require(
        exact_input_volume == EXPECTED_INPUT_VOLUME
        and sum(classification_counts.values()) == EXPECTED_INPUT_COUNT
        and sum(classification_volumes.values(), Q(0))
        == EXPECTED_INPUT_VOLUME
        and parent_counts == EXPECTED_PARENT_COUNTS
        and owner_counts == EXPECTED_OWNER_COUNTS
        and active_factor_counts == EXPECTED_ACTIVE_FACTOR_COUNTS
        and fixed_factor_counts == EXPECTED_FIXED_FACTOR_COUNTS,
        "Round199 count/volume/factor conservation",
    )
    require(
        all(
            digest(strip_row_sha256(row)) == row["row_sha256"]
            for row in rows
        ),
        "all Round185 input row hashes",
    )
    counterexample_labels = (
        "non_strict_full_box_dt",
        "incomplete_t_face_C0_atlas",
        "mixed_or_unresolved_t_face_cell_sign",
        "opposite_t_face_signs",
        "dt_endpoint_direction_contradiction",
    )
    require(
        classification_counts == {
            "ACTIVE_FACTOR_ZERO_ABSENT": EXPECTED_INPUT_COUNT
        }
        and all(
            counterexample_counts[label] == 0
            for label in counterexample_labels
        ),
        "Round199 strict same-sign absence outcome",
    )
    verdict = (
        "VALIDATED"
        if classification_counts[
            "T_FACE_C0_ATLAS_RESIDUAL"
        ] == 0
        else "PARTIAL"
    )
    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_H2_FACTOR_T_FACE_C0_ATLAS_PROBE",
        "question":
            "Can the 592 Round185 H2 factor-existence residual boxes be "
            "classified from a strict full-box active-factor dt sign and "
            "two independently rebuilt complete endpoint-face centered-C0 "
            "atlases, without treating regularity alone as existence?",
        "verdict": verdict,
        "verdict_scope":
            "bounded Round185 H2 factor-existence cohort only; spike "
            "evidence, not a formal local-key, whole-parent, or global "
            "certificate",
        "input_chain": {
            **pins,
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": module.atlas.ctx.prec,
            "probe_imports_pinned_verifier_only_after_formal_six_file"
            "_hash_check":
                True,
        },
        "scope": {
            "Round185_input_status": "H2_FACTOR_EXISTENCE_RESIDUAL",
            "box_count": EXPECTED_INPUT_COUNT,
            "parent_count": len(parent_counts),
            "point_owner_count": len(owner_counts),
            "exact_coordinate_volume": str(exact_input_volume),
            "parent_count_census": counter_dict(parent_counts),
            "parent_exact_volume_census": {
                key: str(value)
                for key, value in sorted(parent_volumes.items())
            },
            "point_owner_count_census": counter_dict(owner_counts),
        },
        "factor_structure": {
            "active_factor_count": counter_dict(active_factor_counts),
            "fixed_absent_factor_count":
                counter_dict(fixed_factor_counts),
            "selected_full_box_graph_axis_count":
                counter_dict(graph_axis_counts),
            "active_dt_dp_sign_pair_count":
                counter_dict(active_derivative_sign_counts),
            "all_fixed_factors_centered_C0_strict_negative": (
                fixed_factor_counts == EXPECTED_FIXED_FACTOR_COUNTS
            ),
            "all_active_factors_have_exactly_strict_dt_dp": True,
            "double_active_factor_box_count": 0,
            "strict_derivative_used_only_for_regularity_or_with_independent"
            "_boundary_sign_evidence": True,
        },
        "endpoint_face_centered_C0_atlas": {
            "t_endpoint_face_count": 2 * EXPECTED_INPUT_COUNT,
            "exact_rational_refinement_axis": "p",
            "maximum_allowed_refinement_depth":
                T_FACE_P_ATLAS_MAX_DEPTH,
            "terminal_C0_cell_count": t_face_terminal_cell_total,
            "active_factor_endpoint_depth_count":
                counter_dict(t_endpoint_depth_counts),
            "active_factor_endpoint_terminal_cell_count":
                counter_dict(t_endpoint_cell_counts),
            "active_factor_endpoint_resolved_sign_count":
                counter_dict(t_endpoint_sign_counts),
            "t_endpoint_parent_factor_method_count":
                counter_dict(t_endpoint_proof_counts),
            "per_parent_active_fixed_factor_count":
                counter_dict(per_parent_factor_counts),
            "all_terminal_cells_use_strict_centered_C0_enclosures": True,
            "every_endpoint_face_exact_area_conserved": True,
            "every_endpoint_face_has_one_uniform_strict_sign": True,
            "regularity_is_not_existence": True,
        },
        "same_sign_strict_dt_absence_proof": {
            "proof":
                "For each fixed (p,s), the active factor is strictly "
                "monotone in t because its full-box dt enclosure has one "
                "strict sign.  Each complete t-endpoint face is covered by "
                "strict centered-C0 cells, and both faces have the same "
                "uniform sign.  Therefore the active factor cannot vanish "
                "at any interior t.",
            "active_dt_t_minus_t_plus_method_cross_count":
                counter_dict(same_sign_direction_cross_counts),
            "counterexample_gate": {
                label: counterexample_counts[label]
                for label in counterexample_labels
            },
            "counterexample_gate_all_zero": all(
                counterexample_counts[label] == 0
                for label in counterexample_labels
            ),
            "strict_dt_is_not_used_without_two_complete_C0_face_atlases":
                True,
        },
        "classification": {
            "count": {
                key: classification_counts.get(key, 0)
                for key in CLASSIFICATIONS
            },
            "exact_coordinate_volume":
                volume_dict(classification_volumes),
            "per_parent_count":
                counter_dict(per_parent_classification_counts),
            "active_resolved_sign_count":
                counter_dict(active_resolved_sign_counts),
            "potential_local_outgoing_chart_count":
                counter_dict(potential_chart_counts),
            "count_conserved": True,
            "exact_volume_conserved": True,
            "classified_zero_set_dimension_not_promoted_to_ambient_credit":
                True,
        },
        "per_box_evidence_hash_ledger": {
            "row_count": len(evidence_hash_rows),
            "rows": evidence_hash_rows,
            "rows_sha256": digest(evidence_hash_rows),
            "full_interval_evidence_emitted_inline": False,
            "hash_scope":
                "fresh full-box C0/C1, both complete t-face centered-C0 "
                "atlases, same-sign/direction gates, classification, and "
                "zero-credit fields",
        },
        "exact_conservation": {
            "input_box_count": EXPECTED_INPUT_COUNT,
            "classified_box_count": sum(classification_counts.values()),
            "input_exact_coordinate_volume": str(exact_input_volume),
            "classified_exact_coordinate_volume": str(
                sum(classification_volumes.values(), Q(0))
            ),
            "probe_formal_credit_volume": "0",
            "official_residual_volume_retained_until_formal_verification":
                str(exact_input_volume),
            "integer_delta": 0,
            "exact_volume_delta": "0",
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "formal_local_exact_key_credit_issued": 0,
            "whole_parent_or_stratum_credit_issued": 0,
            "global_exact_key_disposition_credit": 0,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO_FOR_CLAIM",
            "required_next":
                "formal producer plus a separately implemented verifier "
                "must emit/rebuild the complete interval evidence before "
                "any of these boxes can leave the official residual ledger",
        },
        "probe_provenance": {
            "schema": SCHEMA,
            "probe_source_sha256": file_sha256(PROBE),
            "PYTHONHASHSEED_observed":
                str(__import__("os").environ.get("PYTHONHASHSEED")),
            "stdout_JSON_only": True,
            "progress_stream": "stderr",
        },
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
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
