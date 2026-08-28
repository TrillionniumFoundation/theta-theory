#!/usr/bin/env python3
"""Exact zero-credit proof that reverse rechart is the inverse true-seam relation."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CERT = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
VERIFY = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
PRIMITIVE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
PINS = {
    CERT: "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    VERIFY: "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    PRIMITIVE: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
}

def sha(path: Path) -> str:
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def canon(v: Any) -> bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")

def digest(v: Any) -> str:
    return hashlib.sha256(canon(v)).hexdigest()

def need(v: bool, label: str) -> None:
    if type(v) is not bool or not v: raise RuntimeError(label)

def main() -> int:
    need(all(sha(ROOT/n)==h for n,h in PINS.items()),"pins")
    tree=ast.parse((ROOT/PRIMITIVE).read_text(),filename=PRIMITIVE)
    need(any(isinstance(n,ast.FunctionDef) and n.name=="geometry" for n in tree.body),"primitive geometry")
    cert=json.loads((ROOT/CERT).read_bytes())["result"]
    verify=json.loads((ROOT/VERIFY).read_bytes())["result"]
    need(verify["status"]=="PASS" and verify["producer_imported_or_executed"] is False,"independent R171 verification")
    seams=cert["exact_source_G_coordinate_bridge"]["seam_rows"]
    need(len(seams)==4,"four seams")
    expected={("E","N"),("N","W"),("W","S"),("S","E")}
    forward=set(); rows=[]
    for seam in seams:
        left,right=seam["left_face"],seam["right_face"]
        need(left["z"]=="+kappa" and right["z"]=="-kappa","opposite seam faces")
        need(seam["normal_glues_exactly"] is True and seam["source_G_position_glues_exactly"] is True and seam["quarter_turn_and_velocity_glue_for_every_q"] is True,"full phase glue")
        forward.add((left["chart"],right["chart"]))
        body={
            "forward_chart_pair":[left["chart"],right["chart"]],
            "reverse_chart_pair":[right["chart"],left["chart"]],
            "forward_faces":[left["z"],right["z"]],
            "reverse_faces":[right["z"],left["z"]],
            "same_equivalence_relation":True,
            "inverse_of_exact_bijective_phase_glue":True,
            "new_physical_identification_added":False,
            "formal_credit":0,
        }
        rows.append({**body,"row_sha256":digest(body)})
    need(forward==expected and len({tuple(r["reverse_chart_pair"]) for r in rows})==4,"cyclic and reverse cover")
    result={
        "status":"PASS_ZERO_CREDIT__REVERSE_RECHART_IS_EXACT_INVERSE_OF_FOUR_TRUE_SEAMS",
        "row_count":4,"unresolved_count":0,"new_edge_count":0,"rows_sha256":digest(rows),
        "C27_imported":False,"formal_credit":0,"C27_C28_C29":"REJECT_PENDING_FULL_20_FAMILY_GATE",
    }
    print(canon({**result,"result_sha256":digest(result)}).decode())
    return 0

if __name__=="__main__": raise SystemExit(main())
