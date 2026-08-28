#!/usr/bin/env python3
"""Independent verifier for the CM2 Round-61 aggregate core-frontier audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORT = HERE / "cm2-round61-independent-core-frontier-audit-2026-07-20.md"
MANIFEST = HERE / "cm2-round61-independent-core-frontier-audit-manifest-2026-07-20.json"
CERT = HERE / "cm2_round61_independent_core_frontier_audit_cert.py"

FROZEN_PINS = {
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.sha256":
        "a7499c939a1b167a21b62f8f0485ceaac5b44a9c21d2c59e3e22ee45805c56e2",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json":
        "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.sha256":
        "27f936d543d7b0f4794741f6896387ab0dcbc4b5d2e729f3412beb6ddc190d26",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256":
        "744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b",
}

RESULT_SHA256 = "3372a1bb268b7f56042bcaa8f18308679c4c427ead43e572e2bae2f542f2cb26"
BLOCK_DEPTH = 9148
C_P = Q(4 * 10**90 * 360493663, 358863)
FWD = Q(395304765824751, 220000)
REV = Q(162772550633721, 176000)
BI = Q(2395081816467609, 880000)


class VerifyError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyError(message)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                       allow_nan=False) + "\n").encode()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False
    ).encode()).hexdigest()


def reject_constant(token: str) -> None:
    raise VerifyError(f"nonfinite JSON constant: {token}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerifyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_loads(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8"), parse_constant=reject_constant,
                          object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerifyError(f"strict JSON parse: {exc}") from exc


def strict_load_file(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
            f"JSON file/type: {path.name}")
    value = strict_loads(path.read_bytes())
    require(type(value) is dict, f"JSON root: {path.name}")
    return value


def resolve_ledger_target(raw_name: str) -> Path:
    candidate = Path(raw_name)
    require(not candidate.is_absolute() and ".." not in candidate.parts,
            f"unsafe ledger name: {raw_name}")
    path = ROOT / candidate if candidate.parts[:1] == ("deliverables",) else HERE / candidate
    require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
            f"ledger target: {raw_name}")
    return path


def validate_frozen() -> tuple[dict[str, dict[str, Any]], list[dict[str, str]], int]:
    manifests: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, str]] = []
    for name, expected in FROZEN_PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
                f"frozen file/type: {name}")
        require(sha(path) == expected, f"frozen digest: {name}")
        if name.endswith(".json"):
            manifests[name] = strict_load_file(path)
        else:
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                parts = line.split(maxsplit=1)
                require(len(parts) == 2 and len(parts[0]) == 64,
                        f"ledger syntax: {name}")
                target = resolve_ledger_target(parts[1].strip())
                require(sha(target) == parts[0], f"ledger hash: {target.name}")
                rows.append({"name": target.name, "sha256": parts[0]})
    require(len(rows) == 12 and len({row["name"] for row in rows}) == 12,
            "leaf ledger rows")
    g4 = next(value for name, value in manifests.items() if name.startswith("cm2-gate4-"))
    g5 = next(value for name, value in manifests.items() if name.startswith("cm2-gate5-"))
    g123 = next(value for name, value in manifests.items() if name.startswith("cm2-gate123-"))
    dependency_count = (
        len(g4["dependencies"]) + len(g4["baseline_files"])
        + len(g5["dependencies"]) + len(g5["Round60_aggregate_artifact_sha256"])
        + len(g123["dependencies"])
    )
    require(dependency_count == 30, "older dependency/artifact pins")
    return manifests, rows, dependency_count


def expected_frozen_rows() -> list[dict[str, str]]:
    return [{"name": name, "sha256": digest}
            for name, digest in FROZEN_PINS.items()]


STRICT_STATUS = {
    "gate1": "NOT_CERTIFIED",
    "gate2": "NOT_CERTIFIED",
    "gate2_immutable_fields": "0/17",
    "gate2_landing_join": "1/7",
    "gate3": "NOT_CERTIFIED",
    "gate4": "NOT_CERTIFIED",
    "gate5": "NOT_CERTIFIED",
    "gate5_maturity": "10/18",
    "complete_18_field_blocks": 0,
    "composite_gates": "0/5",
    "cm2": "NO-GO_FOR_CLAIM",
}


ACCEPTANCE = {
    "main_leaves": {
        "syntax": "6/6", "older_dependency_artifact_pins": "30/30",
        "frozen_manifest_ledger_pins": "6/6", "leaf_ledger_rows": "12/12",
        "integrity": "3/3", "replay": "3/3", "reemit": "3/3",
        "hostile_and_strict_JSON": "615/615_REJECTED",
        "default_cert_verifier": "6/6_EXIT_2",
    },
    "independent_audit_leaf": {
        "syntax": "2/2", "frozen_manifest_ledger_pins": "6/6",
        "leaf_ledger_rows": "12/12", "integrity": "1/1", "replay": "1/1",
        "reemit": "1/1", "hostile_and_strict_JSON": "108/108_REJECTED",
        "default_cert_verifier": "2/2_EXIT_2", "SHA_ledger": "4/4",
    },
    "final_four_leaf_matrix": {
        "syntax": "8/8", "dependency_artifact_pins": "36/36",
        "integrity": "4/4", "replay": "4/4", "reemit": "4/4",
        "hostile_and_strict_JSON": "723/723_REJECTED",
        "SHA_ledger_rows": "16/16", "default_cert_verifier": "8/8_EXIT_2",
        "stale_temp_files": 0,
    },
}


def validate_obj(data: Any, raw: bytes | None = None) -> None:
    require(type(data) is dict, "manifest object")
    require(set(data) == {
        "artifact", "certificate_sha256", "date", "frozen_pins",
        "report_sha256", "result", "result_sha256", "schema",
        "strict_verdict", "verifier_sha256",
    }, "manifest exact top-level schema")
    if raw is not None:
        require(raw == canonical_bytes(data), "canonical manifest bytes")
    require(data["schema"] == "cm2.round61-independent-core-frontier-audit.v1",
            "schema")
    require(data["artifact"] == "cm2-round61-independent-core-frontier-audit",
            "artifact")
    require(data["date"] == "2026-07-20", "date")
    require(data["frozen_pins"] == expected_frozen_rows(), "frozen pins")
    require(type(data["result"]) is dict, "result type")
    digest = canonical_digest(data["result"])
    require(digest == data["result_sha256"] == RESULT_SHA256, "result digest")
    require(data["strict_verdict"] == (
        "PASS after pre-freeze Gate4 cone-curve/BV scoping and Gate5 "
        "standard-Borel cemetery/injective-code corrections; all five Gates "
        "remain not certified, composite gates are 0/5 and CM2 is no-go"
    ), "strict verdict")
    result = data["result"]
    require(result.get("strict_status") == STRICT_STATUS, "strict status")
    require(result.get("acceptance") == ACCEPTANCE, "acceptance matrix")
    require(result.get("older_dependency_artifact_pins") == 30, "pin count")
    require(len(result.get("frozen_leaf_pins", [])) == 6, "frozen pin count")
    require(len(result.get("leaf_ledger_rows", [])) == 12, "ledger row count")
    require(result.get("cross_leaf_audit") == {
        "D_land_is_Dbar": False,
        "weak_graph_TV_is_physical_strong_space": False,
        "positive_bad_or_complement_mass_is_collision_null_cemetery": False,
        "orientation_RN_is_Jordan_marginal": False,
        "exact_Gate1_transport_requires_future_same_token_cohomology": True,
        "status": "PASS_NO_CARRIER_OR_STATE_COLLISION",
    }, "cross-leaf guards")
    require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
    require(CERT.is_file() and not CERT.is_symlink(), "certificate file/type")
    require(Path(__file__).resolve().is_file(), "verifier file/type")
    require(data["report_sha256"] == sha(REPORT), "report hash")
    require(data["certificate_sha256"] == sha(CERT), "certificate hash")
    require(data["verifier_sha256"] == sha(Path(__file__).resolve()), "verifier hash")


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    depth = 1
    while z / 2**depth >= C_P / 2:
        depth += 1
    return depth


def replay_gate4(data: dict[str, Any], manifests: dict[str, dict[str, Any]]) -> None:
    g4 = next(value for name, value in manifests.items() if name.startswith("cm2-gate4-"))
    source = g4["result"]
    atoms = source["weighted_graph_defect_lattice"]["sample_atoms"]
    mass = sum((Q(row["mass"]) for row in atoms), Q(0))
    weighted = sum((2 ** row["D"] * Q(row["mass"]) for row in atoms), Q(0))
    require(mass == Q(53, 320) and weighted == Q(7, 5), "Gate4 atom replay")
    length = Q(2, 1) / (3 * C_P)
    require(1 / length == Q(3, 2) * C_P, "Gate4 separator z")
    require(defect_depth(1 / length) == 2, "Gate4 separator depth")
    rows = source["smooth_Dland_vs_strong_separator"]["rows"]
    require([row["BV_variation_of_marker"] for row in rows] == [1, 2, 17, 257, 4096],
            "Gate4 BV rows")
    require(source["seven_field_materialization_audit"]["actual_complete_rows"] == "1/7",
            "Gate4 field count")
    audit = data["result"]["gate4_audit"]
    require(audit["graph_norm_sample"] == "7/5" and
            audit["BV_separator_terminal_variation"] == 4096 and
            audit["gate4"] == "NOT_CERTIFIED", "Gate4 aggregate replay")


def orlicz_rows() -> list[tuple[int, int]]:
    with localcontext() as ctx:
        ctx.prec = 150
        gamma = (Decimal(2000) / Decimal(1999)
                 * Decimal(1 + 48 * BLOCK_DEPTH)
                 * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH)
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        q_col = Decimal(2).ln() / (beta * w.ln())
        require(w > 1 and beta > 0 and q_col > 1, "Gate5 Orlicz constants")
        rows: list[tuple[int, int]] = []
        for k in (0, 1, 2, 16, 4381, 10000):
            r = int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))
            phi = (w ** r) ** q_col
            raw = Decimal(2) ** (k + 1)
            require(raw <= phi < (w ** q_col) * raw, f"Gate5 Orlicz row {k}")
            rows.append((k, r))
        return rows


def replay_gate5(data: dict[str, Any], manifests: dict[str, dict[str, Any]]) -> None:
    g5 = next(value for name, value in manifests.items() if name.startswith("cm2-gate5-"))
    source = g5["result"]
    require(FWD + REV == BI, "Gate5 F10 arithmetic")
    owner = source["actual_owner_complement_RN_anchor"]
    suffix = source["seven_bit_common_Borel_code_materialisation"]
    require("standard-Borel product" in owner["cemetery_pushforward"] and
            "not a countable atom list" in owner["cemetery_pushforward"],
            "Gate5 cemetery product")
    require("injective" in suffix["countable_separating_generator"] and
            suffix["unconditional_Borel_predicate_count"] == 7 and
            suffix["certified_universal_true_count"] == 2 and
            suffix["missing_universal_value_count"] == 5,
            "Gate5 Borel suffix")
    require("all labelled cemetery atoms" not in
            (HERE / "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-assault-2026-07-20.md").read_text(encoding="utf-8"),
            "Gate5 stale wording")
    rows = orlicz_rows()
    audit = data["result"]["gate5_audit"]
    require([(row["K"], row["r_K"]) for row in audit["Orlicz_rows_replayed"]] == rows,
            "Gate5 aggregate Orlicz replay")
    require(audit["suffix_Borel"] == "7/7" and
            audit["suffix_values"] == "2_TRUE_5_OPEN" and
            audit["maturity"] == "10/18" and audit["blocks"] == 0 and
            audit["gate5"] == "NOT_CERTIFIED", "Gate5 aggregate state")


def mm(a: Any, b: Any) -> Any:
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
                       for j in range(2)) for i in range(2))


def mv(a: Any, v: Any) -> Any:
    return tuple(sum((a[i][k] * v[k] for k in range(2)), Q(0))
                 for i in range(2))


def wedge(v: Any, w: Any) -> Q:
    return v[0] * w[1] - v[1] * w[0]


def replay_gate123(data: dict[str, Any], manifests: dict[str, dict[str, Any]]) -> None:
    g123 = next(value for name, value in manifests.items() if name.startswith("cm2-gate123-"))
    source = g123["result"]
    d = ((Q(2), Q(1)), (Q(1), Q(1)))
    d_inv = ((Q(1), Q(-1)), (Q(-1), Q(2)))
    psi = ((Q(2), Q(3)), (Q(5), Q(7)))
    psi_new = mm(mm(d, psi), d_inv)
    basis = ((Q(1), Q(0)), (Q(0), Q(1)))
    transported = tuple(mv(d, v) for v in basis)
    old = [wedge(mv(psi, basis[i]), basis[j]) for i in range(2) for j in range(2)]
    new = [wedge(mv(psi_new, transported[i]), transported[j])
           for i in range(2) for j in range(2)]
    require(old == new == [Q(-5), Q(2), Q(-7), Q(3)], "Gate123 wedges")
    mu_u = [Q(1, 2), Q(1, 3), Q(1, 6)]
    mu_v = [Q(1, 4), Q(1, 2), Q(1, 4)]
    marker = [Q(1), Q(1, 2), Q(0)]
    target = [1, 2, 0]
    push_mu = [Q(0), Q(0), Q(0)]
    push_marked = [Q(0), Q(0), Q(0)]
    for i in range(3):
        push_mu[target[i]] += mu_u[i]
        push_marked[target[i]] += marker[i] * mu_u[i]
    jac = [push_mu[i] / mu_v[i] for i in range(3)]
    marked = [push_marked[i] / mu_v[i] for i in range(3)]
    require(jac == [Q(2, 3), Q(1), Q(4, 3)] and
            marked == [Q(0), Q(1), Q(2, 3)], "Gate123 RN marker")
    signed = [Q(1, 3), Q(-1, 6), Q(1, 2), Q(-1, 4),
              Q(1, 8), Q(-1, 12), Q(1, 7), Q(-1, 9)]
    bins = [0, 0, 1, 1, 2, 2, 2, 1]
    output = [Q(0), Q(0), Q(0)]
    for value, cell in zip(signed, bins):
        output[cell] += value
    input_tv = sum((abs(value) for value in signed), Q(0))
    output_tv = sum((abs(value) for value in output), Q(0))
    require(input_tv == Q(863, 504) and output_tv == Q(247, 504), "Gate123 TV")
    require(source["gate3"]["actual_stopped_graph_partition"]["status"] ==
            "CERTIFIED_ACTUAL_WEAK_STOPPED_GRAPH_TV_NORM_ONE", "Gate123 weak type")
    audit = data["result"]["gate123_audit"]
    require(audit["same_loop_wedges"] == ["-5", "2", "-7", "3"] and
            audit["stopped_input_TV"] == "863/504" and
            audit["stopped_output_TV"] == "247/504" and
            audit["gate123"] == "NOT_CERTIFIED", "Gate123 aggregate replay")


def independent_replay(data: dict[str, Any]) -> dict[str, Any]:
    manifests, rows, count = validate_frozen()
    require(rows == data["result"]["leaf_ledger_rows"], "ledger rows in result")
    require(count == data["result"]["older_dependency_artifact_pins"], "pin count in result")
    replay_gate4(data, manifests)
    replay_gate5(data, manifests)
    replay_gate123(data, manifests)
    return {
        "frozen_pins": 6,
        "leaf_ledger_rows": 12,
        "older_dependency_artifact_pins": 30,
        "gate4": "PASS",
        "gate5": "PASS",
        "gate123": "PASS_AFTER_ROOT_INDEPENDENT_RED_TEAM_AND_FRESH_AUDIT_REPLAY",
        "cross_leaf": "PASS_NO_CARRIER_OR_STATE_COLLISION",
        "status": "PASS",
    }


def hostile_self_test(base: dict[str, Any]) -> int:
    mutations: list[dict[str, Any]] = []
    for i in range(40):
        candidate = copy.deepcopy(base)
        candidate[f"hostile_extra_{i}"] = i
        mutations.append(candidate)
    for i in range(30):
        candidate = copy.deepcopy(base)
        candidate["result"]["strict_status"]["composite_gates"] = f"{i + 1}/5"
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    for i in range(20):
        candidate = copy.deepcopy(base)
        candidate["frozen_pins"][i % 6]["sha256"] = f"{i + 1:064x}"[-64:]
        mutations.append(candidate)
    for i in range(10):
        candidate = copy.deepcopy(base)
        candidate["result"]["older_dependency_artifact_pins"] = 31 + i
        candidate["result_sha256"] = canonical_digest(candidate["result"])
        mutations.append(candidate)
    rejected = 0
    for candidate in mutations:
        try:
            validate_obj(candidate)
        except VerifyError:
            rejected += 1
    require(rejected == len(mutations) == 100, "semantic hostile rejection")
    raw_attacks = [
        b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}',
        b'{"x":1,"x":2}', b'[]', b'null', b'"manifest"', b'{',
    ]
    raw_rejected = 0
    for raw in raw_attacks:
        try:
            candidate = strict_loads(raw)
            validate_obj(candidate, raw)
        except VerifyError:
            raw_rejected += 1
    require(raw_rejected == len(raw_attacks) == 8, "strict JSON hostile rejection")
    return rejected + raw_rejected


def load_manifest() -> tuple[dict[str, Any], bytes]:
    require(MANIFEST.is_file() and not MANIFEST.is_symlink(), "manifest file/type")
    raw = MANIFEST.read_bytes()
    value = strict_loads(raw)
    require(type(value) is dict, "manifest mapping")
    return value, raw


def reemit(path: Path) -> None:
    command = [sys.executable, str(CERT), "--emit-manifest", str(path)]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    require(completed.returncode == 0, f"producer reemit: {completed.stderr}")
    require(path.is_file() and path.read_bytes() == MANIFEST.read_bytes(),
            "byte-identical reemit")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        validate_frozen()
        data, raw = load_manifest()
        validate_obj(data, raw)
        if args.integrity_only:
            print("INTEGRITY: PASS")
            print("FROZEN_PINS: 6/6")
            print("LEAF_LEDGER_ROWS: 12/12")
            return 0
        if args.replay:
            print(json.dumps(independent_replay(data), sort_keys=True))
            return 0
        if args.self_test:
            count = hostile_self_test(data)
            print(f"HOSTILE_MUTATIONS_REJECTED: {count}/{count}")
            return 0
        if args.reemit is not None:
            reemit(args.reemit)
            print("REEMIT: BYTE_IDENTICAL")
            return 0
        independent_replay(data)
    except (VerifyError, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as exc:
        print(f"VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND61_INDEPENDENT_CORE_FRONTIER_AUDIT: PASS")
    print("GATES_1_2_3_4_5: NOT_CERTIFIED")
    print("GATE2_IMMUTABLE_FIELDS: 0/17")
    print("GATE2_LANDING_JOIN: 1/7")
    print("GATE5_MATURITY: 10/18; COMPLETE_BLOCKS: 0")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
