#!/usr/bin/env python3
"""Materialize T11--T19 without double-counting proof-only branches."""

from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "deliverables"
R = ROOT / ".cm2-runtime/audit"
CERT = D / "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
CERT_VERIFY = D / "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
PRIMITIVE = D / "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
QUOTIENT_RESULT = R / "c27-explicit-quotient-map-alias-v2-final-seed-30627301/cm2_c27_explicit_quotient_map_alias_zero_credit_v2_result.json"
QUOTIENT_SOURCE = D / "cm2_c27_explicit_quotient_map_alias_zero_credit_probe_v2.py"
R236 = D / "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248 = D / "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
COMMON_RESULT = R / "c27-legacy-terminal-typed-ownership-v1-seed-30650101/result.json"
ALIAS = R / "c27-legacy-terminal-typed-ownership-v1-seed-30650101/representation_alias_auxiliary_crosswalk.jsonl.gz"

PINS = {
    CERT: "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    CERT_VERIFY: "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    PRIMITIVE: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    QUOTIENT_RESULT: "b6e01dfbae63628931105d9884d9ece46329c2ebb9f629931117e9b2861a2adc",
    QUOTIENT_SOURCE: "63cc28c2b1e7ea34b5ef313cdb3a68c71521e29409aa7551604acf90cef7ad5a",
    R236: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R248: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    COMMON_RESULT: "743eb648f62858508d38cec5cc533a3e3ceeb3e0852b642a82dba65377655542",
    ALIAS: "27e2d297025970e7d99200577151e104037aff6e1326b091e05c7281ae37be16",
}

SEAM_TERMINALS = {
    ("E", "N"): "TRUE_CYCLIC_SEAM_E_TO_N",
    ("N", "W"): "TRUE_CYCLIC_SEAM_N_TO_W",
    ("W", "S"): "TRUE_CYCLIC_SEAM_W_TO_S",
    ("S", "E"): "TRUE_CYCLIC_SEAM_S_TO_E",
}
ACTIONS = {
    "Jx": "Jx_NEGATIVE_CONTROL",
    "Jy": "Jy_NEGATIVE_CONTROL",
    "JxJy": "JxJy_NEGATIVE_CONTROL",
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(8 << 20):
            state.update(block)
    return state.hexdigest()


def closed(row: dict[str, Any], key: str, label: str) -> None:
    claim = row.get(key)
    body = dict(row); body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line in handle:
            yield json.loads(line)


def close_sort(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    rows.sort(key=lambda row: tuple(str(row[field]) for field in fields))
    for ordinal, row in enumerate(rows):
        row["ordinal"] = ordinal
        row["row_sha256"] = digest(row)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                zipped.write(encode(row) + b"\n")


def reconstruct_source_sheets() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec = importlib.util.spec_from_file_location("cm2_quotient_source_pinned", QUOTIENT_SOURCE)
    need(spec is not None and spec.loader is not None, "quotient source module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sheets, audit = module.reconstruct_source_sheets()
    for descriptor in module.CAPTURE_FDS.values():
        try:
            module.os.close(descriptor)
        except OSError:
            pass
    module.CAPTURE_FDS.clear()
    return sheets, audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        for path, expected in PINS.items():
            need(path.is_file() and not path.is_symlink() and file_hash(path) == expected,
                 "input pin:" + path.name)
        cert = json.loads(CERT.read_bytes())["result"]
        verification = json.loads(CERT_VERIFY.read_bytes())["result"]
        need(verification["status"] == "PASS"
             and verification["producer_imported_or_executed"] is False,
             "R171 independent verification")
        seam_source = cert["exact_source_G_coordinate_bridge"]["seam_rows"]
        need(len(seam_source) == 4, "four source seams")
        candidates: list[dict[str, Any]] = []
        proofs: list[dict[str, Any]] = []
        for seam in seam_source:
            left = seam["left_face"]; right = seam["right_face"]
            pair = (left["chart"], right["chart"])
            need(pair in SEAM_TERMINALS
                 and left["z"] == "+kappa" and right["z"] == "-kappa"
                 and seam["normal_glues_exactly"] is True
                 and seam["source_G_position_glues_exactly"] is True
                 and seam["quarter_turn_and_velocity_glue_for_every_q"] is True,
                 "seam semantics")
            terminal = SEAM_TERMINALS[pair]
            key = f"ATLAS_SEAM|{pair[0]}|{pair[1]}|+kappa|-kappa"
            candidate_id = f"cm2-c27-independent:{terminal}:{key}"
            candidates.append({
                "schema": "cm2.c27-independent.atlas-seam.typed-candidate-ownership-row.v1",
                "candidate_id": candidate_id,
                "candidate_key": key,
                "candidate_key_namespace": "ATLAS_FORWARD_SEAM",
                "candidate_unit": "ATLAS_FORWARD_SEAM",
                "terminal": terminal,
                "terminal_assignment_cardinality": 1,
                "forward_chart_pair": list(pair),
                "forward_faces": [left["z"], right["z"]],
                "source_seam_body_sha256": digest(seam),
                "R171_certificate_file_sha256": PINS[CERT],
                "formal_credit": 0,
                "source_W_transition_authorized": False,
            })
            proofs.append({
                "schema": "cm2.c27-independent.reverse-rechart.auxiliary-proof-row.v1",
                "proof_key": f"REVERSE_PROOF|{pair[1]}|{pair[0]}|-kappa|+kappa",
                "proof_key_namespace": "ATLAS_REVERSE_PROOF_ONLY",
                "terminal": "REVERSE_RECHART",
                "forward_candidate_id": candidate_id,
                "forward_chart_pair": list(pair),
                "reverse_chart_pair": [pair[1], pair[0]],
                "forward_faces": [left["z"], right["z"]],
                "reverse_faces": [right["z"], left["z"]],
                "inverse_of_exact_bijective_phase_glue": True,
                "same_equivalence_relation": True,
                "independent_terminal_candidate": False,
                "candidate_count_contribution": 0,
                "new_physical_identification_added": False,
                "source_seam_body_sha256": digest(seam),
                "formal_credit": 0,
                "source_W_transition_authorized": False,
            })

        source_sheets, source_sheet_audit = reconstruct_source_sheets()
        need(len(source_sheets) == 16
             and source_sheet_audit["source_sheet_count"] == 16,
             "source sheet census")
        chart_census: dict[str, int] = {}
        for raw_sheet in sorted(source_sheets, key=encode):
            member = raw_sheet["member_id"]
            sheet = {
                "source_sheet_member_id": member,
                "source_partition_row_id": raw_sheet["partition_row_id"],
                "source_sheet_chart": raw_sheet["chart"],
                "source_t": raw_sheet["source_t"],
                "source_sheet_normal": raw_sheet["source_normal"],
                "source_sheet_position": raw_sheet["source_position"],
                "source_sheet_p_s_rectangle": raw_sheet["closed_p_s_rectangle"],
                "owner_official_key_id": raw_sheet["owner_official_key_id"],
                "owner_signature_sha256": raw_sheet["owner_signature_sha256"],
                "R248_row_sha256": raw_sheet["R248_row_sha256"],
            }
            p0, p1 = map(Fraction, sheet["source_sheet_p_s_rectangle"][:2])
            need(p0 < p1 and not (p0 <= 0 <= p1), "source sheet p excludes zero")
            nx, ny = map(Fraction, sheet["source_sheet_normal"])
            need(nx * nx + ny * ny == 1, "unit coordinate-axis normal")
            chart_census[sheet["source_sheet_chart"]] = chart_census.get(sheet["source_sheet_chart"], 0) + 1
            for action, terminal in ACTIONS.items():
                if action == "Jx":
                    equations = ["n_x=0", "q_x=0", "s=0", "p=0"]
                    decisive = "SOURCE_N_X_NONZERO" if nx != 0 else "SOURCE_P_INTERVAL_EXCLUDES_ZERO"
                elif action == "Jy":
                    equations = ["n_y=0", "q_y=0", "p=0"]
                    decisive = "SOURCE_N_Y_NONZERO" if ny != 0 else "SOURCE_P_INTERVAL_EXCLUDES_ZERO"
                else:
                    equations = ["n_x=0", "n_y=0", "q_x=0", "q_y=0", "s=0"]
                    decisive = "UNIT_NORMAL_CANNOT_HAVE_N_X_EQUALS_N_Y_EQUALS_ZERO"
                proofs.append({
                    "schema": "cm2.c27-independent.physical-action-negative-control.auxiliary-proof-row.v1",
                    "proof_key": f"NEGATIVE_CONTROL|{action}|{member}",
                    "proof_key_namespace": "PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY",
                    "terminal": terminal,
                    "action": action,
                    "source_sheet_member_id": member,
                    "source_sheet_projection": sheet,
                    "source_sheet_projection_sha256": digest(sheet),
                    "R248_source_sheet_row_sha256": raw_sheet["R248_row_sha256"],
                    "fixed_point_equations": equations,
                    "decisive_empty_fixed_set_fact": decisive,
                    "p_zero_in_open_interval": False,
                    "fixed_sheet_point_family_count": 0,
                    "physical_action_is_quotient_identification": False,
                    "independent_terminal_candidate": False,
                    "candidate_count_contribution": 0,
                    "formal_credit": 0,
                    "source_W_transition_authorized": False,
                })
        need(chart_census == {"G:E": 4, "G:N": 4, "G:S": 4, "G:W": 4},
             "source sheet chart census")

        aliases = list(jsonl(ALIAS))
        need(len(aliases) == 276, "external alias count")
        for ordinal, alias in enumerate(aliases):
            closed(alias, "row_sha256", f"external alias:{ordinal}")
            need(alias["independent_terminal_candidate"] is False
                 and alias["representation_alias_terminal_candidate_count"] == 0
                 and alias["candidate_terminal"] == "RETAINED_CONTINUATION",
                 f"external alias:{ordinal}:semantics")

        close_sort(candidates, ("terminal", "candidate_key"))
        close_sort(proofs, ("terminal", "proof_key"))
        need(len(candidates) == 4 and len(proofs) == 52, "atlas candidate/proof census")
        slot_rows = [
            {"slot":"T11","terminal":"REVERSE_RECHART","role":"AUXILIARY_INVERSE_PROOF_ONLY",
             "candidate_count":0,"authority_row_count":4,"candidate_key_namespace":None,
             "proof_key_namespace":"ATLAS_REVERSE_PROOF_ONLY"},
            {"slot":"T12","terminal":"TRUE_CYCLIC_SEAM_E_TO_N","role":"CANDIDATE_OWNERSHIP",
             "candidate_count":1,"authority_row_count":1,"candidate_key_namespace":"ATLAS_FORWARD_SEAM",
             "proof_key_namespace":None},
            {"slot":"T13","terminal":"TRUE_CYCLIC_SEAM_N_TO_W","role":"CANDIDATE_OWNERSHIP",
             "candidate_count":1,"authority_row_count":1,"candidate_key_namespace":"ATLAS_FORWARD_SEAM",
             "proof_key_namespace":None},
            {"slot":"T14","terminal":"TRUE_CYCLIC_SEAM_W_TO_S","role":"CANDIDATE_OWNERSHIP",
             "candidate_count":1,"authority_row_count":1,"candidate_key_namespace":"ATLAS_FORWARD_SEAM",
             "proof_key_namespace":None},
            {"slot":"T15","terminal":"TRUE_CYCLIC_SEAM_S_TO_E","role":"CANDIDATE_OWNERSHIP",
             "candidate_count":1,"authority_row_count":1,"candidate_key_namespace":"ATLAS_FORWARD_SEAM",
             "proof_key_namespace":None},
            {"slot":"T16","terminal":"Jx_NEGATIVE_CONTROL","role":"NEGATIVE_CONTROL_PROOF_ONLY",
             "candidate_count":0,"authority_row_count":16,"candidate_key_namespace":None,
             "proof_key_namespace":"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY"},
            {"slot":"T17","terminal":"Jy_NEGATIVE_CONTROL","role":"NEGATIVE_CONTROL_PROOF_ONLY",
             "candidate_count":0,"authority_row_count":16,"candidate_key_namespace":None,
             "proof_key_namespace":"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY"},
            {"slot":"T18","terminal":"JxJy_NEGATIVE_CONTROL","role":"NEGATIVE_CONTROL_PROOF_ONLY",
             "candidate_count":0,"authority_row_count":16,"candidate_key_namespace":None,
             "proof_key_namespace":"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY"},
            {"slot":"T19","terminal":"REPRESENTATION_ALIASES","role":"AUXILIARY_ALIAS_PROOF_ONLY",
             "candidate_count":0,"authority_row_count":276,"candidate_key_namespace":None,
             "proof_key_namespace":"REPRESENTATION_ALIAS_AUXILIARY_CROSSWALK"},
        ]
        for row in slot_rows:
            row.update({
                "schema": "cm2.c27-independent.t11-t19.slot-authority-row.v1",
                "exact_candidate_key_disjointness_rule":
                    "ONLY_ATLAS_FORWARD_SEAM_ROWS_ENTER_T11_T19_CANDIDATE_UNION; REVERSE/CONTROL/ALIAS_ROWS_ARE_PROOF_ONLY; T01_KEYS_USE_REPRESENTATION_NAMESPACE; T04_KEYS_USE_GRAPH_ROOT_NAMESPACE",
                "formal_credit": 0,
                "source_W_transition_authorized": False,
            })
        close_sort(slot_rows, ("slot",))

        output = Path(args.output_dir)
        need(not output.exists(), "fresh output")
        output.mkdir(parents=True)
        candidate_path = output / "t11_t19_atlas_seam_candidate_ownership.jsonl.gz"
        proof_path = output / "t11_t18_auxiliary_proof_rows.jsonl.gz"
        slot_path = output / "t11_t19_slot_authority.jsonl.gz"
        write_jsonl(candidate_path, candidates)
        write_jsonl(proof_path, proofs)
        write_jsonl(slot_path, slot_rows)
        ledgers = {}
        for path, rows in ((candidate_path, candidates), (proof_path, proofs), (slot_path, slot_rows)):
            ledgers[path.name] = {"row_count": len(rows), "file_sha256": file_hash(path),
                                  "row_sequence_sha256": digest([row["row_sha256"] for row in rows])}
        quotient = json.loads(QUOTIENT_RESULT.read_bytes())["result"]
        need(quotient["nontrivial_physical_action_fixed_set_audit"]["source_sheet_count"] == 16
             and quotient["nontrivial_physical_action_fixed_set_audit"]["Jx_fixed_sheet_point_family_count"] == 0
             and quotient["nontrivial_physical_action_fixed_set_audit"]["Jy_fixed_sheet_point_family_count"] == 0
             and quotient["nontrivial_physical_action_fixed_set_audit"]["JxJy_fixed_sheet_point_family_count"] == 0,
             "published quotient negative-control census")
        body = {
            "schema": "cm2.c27-independent.t11-t19-atlas-control-alias-authority.result.v1",
            "status": "PASS_T11_T19_EXACT_ROLE_NORMALIZATION__4_SEAM_CANDIDATES__328_PROOF_ONLY_ROWS__ZERO_CREDIT",
            "slot_census": {row["slot"]: {"terminal": row["terminal"], "role": row["role"],
                                            "candidate_count": row["candidate_count"],
                                            "authority_row_count": row["authority_row_count"]}
                            for row in slot_rows},
            "candidate_ownership_total": 4,
            "local_auxiliary_proof_row_total_T11_T18": 52,
            "external_alias_auxiliary_proof_rows_T19": 276,
            "total_proof_only_authority_rows": 328,
            "representation_alias_independent_candidate_count": 0,
            "reverse_rechart_independent_candidate_count": 0,
            "negative_control_independent_candidate_count": 0,
            "candidate_key_disjointness": {
                "T12_T15": "ATLAS_FORWARD_SEAM|forward_chart_pair|faces",
                "T11": "ATLAS_REVERSE_PROOF_ONLY; references exactly one T12_T15 forward candidate",
                "T16_T18": "PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY|action|source_sheet_member_id",
                "T19": "REPRESENTATION_ALIAS_AUXILIARY_CROSSWALK|representation_id; references T01 retained candidate",
                "T01": "REPRESENTATION",
                "T04": "GRAPH_ROOT",
                "pairwise_disjoint_by_typed_namespace_and_candidate_flag": True,
            },
            "source_sheet_count": 16,
            "source_sheet_chart_census": dict(sorted(chart_census.items())),
            "ledgers": ledgers,
            "external_T19_alias_ledger": {"row_count": 276, "file_sha256": PINS[ALIAS]},
            "input_pins": {str(path.relative_to(ROOT)): expected
                           for path, expected in sorted(PINS.items(), key=lambda item: str(item[0]))},
            "seed_declared_but_not_semantically_used": True,
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        value = {**body, "result_sha256": digest(body)}
        (output / "result.json").write_bytes(encode(value) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": value["status"],
                  "result_sha256": value["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
