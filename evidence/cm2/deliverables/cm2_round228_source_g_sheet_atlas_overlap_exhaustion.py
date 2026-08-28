#!/usr/bin/env python3
"""Exhaust true atlas-overlap channels for the materialized Round211 sheets."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round228_source_g_sheet_atlas_overlap_exhaustion"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round228.source-g-sheet-atlas-overlap-exhaustion.v1"
R171 = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R171_SHA = "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5"
R171_RESULT = "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R208_SHA = "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"
R208_RESULT = "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
R211 = "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json"
R211_SHA = "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"
R211_RESULT = "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b"


class Round228Error(RuntimeError): pass
def need(value: bool, label: str) -> None:
    if not value: raise Round228Error(label)
ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value): yield chunk.encode()
def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value): state.update(chunk)
    return state.hexdigest()
def canonical(value: Any) -> bytes: return b"".join(chunks(value))
def closed(value: dict[str, Any]) -> dict[str, Any]:
    row = dict(value); row["row_sha256"] = digest(row); return row
def ledger(rows: list[dict[str, Any]]) -> dict[str, Any]:
    need(len({row["sheet_atlas_disposition_row_id"] for row in rows}) == len(rows), "unique rows")
    return {"row_count": len(rows), "rows_sha256": digest(rows), "row_ids_sha256": digest([r["sheet_atlas_disposition_row_id"] for r in rows]), "row_hashes_sha256": digest([r["row_sha256"] for r in rows]), "every_row_closed_by_own_SHA256": True, "rows": rows}
def regular_bytes(path: Path, maximum: int) -> bytes:
    before = path.lstat(); need(stat.S_ISREG(before.st_mode) and not path.is_symlink() and before.st_nlink == 1, f"regular:{path.name}"); need(0 < before.st_size <= maximum, f"bounded:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        opened = os.fstat(descriptor); need((opened.st_dev,opened.st_ino,opened.st_size,opened.st_mtime_ns)==(before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns), f"stable:{path.name}")
        parts=[]; size=0
        while True:
            part=os.read(descriptor,1024*1024)
            if not part: break
            size+=len(part); need(size<=maximum,f"read bound:{path.name}"); parts.append(part)
        return b"".join(parts)
    finally: os.close(descriptor)
def strict_json(raw: bytes) -> dict[str, Any]:
    def pairs(items: list[tuple[str,Any]]) -> dict[str,Any]:
        out={}
        for key,value in items: need(key not in out,f"duplicate:{key}"); out[key]=value
        return out
    def reject(token: str) -> None: raise Round228Error(f"number:{token}")
    value=json.loads(raw,object_pairs_hook=pairs,parse_float=reject,parse_constant=reject); need(isinstance(value,dict),"object"); return value
def load(name: str, file_sha: str, result_sha: str, maximum: int) -> dict[str,Any]:
    raw=regular_bytes(HERE/name,maximum); need(hashlib.sha256(raw).hexdigest()==file_sha,f"file pin:{name}"); env=strict_json(raw); need(env["result_sha256"]==result_sha and digest(env["result"])==result_sha,f"result pin:{name}"); return env["result"]


def build(producer_sha256: str) -> dict[str,Any]:
    r171=load(R171,R171_SHA,R171_RESULT,100_000_000)
    bridge=r171["exact_source_G_coordinate_bridge"]
    need(bridge["all_four_source_G_seams_glue_exactly"] is True and len(bridge["seam_rows"])==4,"four true source seams")
    need(all(row["source_G_position_glues_exactly"] is True and row["normal_glues_exactly"] is True and row["quarter_turn_and_velocity_glue_for_every_q"] is True for row in bridge["seam_rows"]),"seam identities")
    r208=load(R208,R208_SHA,R208_RESULT,300_000_000)
    r211=load(R211,R211_SHA,R211_RESULT,250_000_000)
    bases={row["leaf_row_id"]:row for row in r208["formal_direct_leaf_signature_base_ledger"]["rows"]}
    sheets=r211["formal_2D_sheet_owner_ledger"]["rows"]
    need(len(bases)==18_324 and len(sheets)==17_716,"input census")
    scope211=r211["formal_scope_and_conservation"]
    need(scope211["all_sheet_signature_pairs_match_except_outgoing_chart_fields"] is True and scope211["all_nonempty_sheets_have_exactly_one_E_or_W_owner"] is True,"Round211 global owner conservation")
    rows=[]; source_charts=Counter(); owner_shadow=Counter(); max_abs_t=Fraction(0)
    for sheet in sheets:
        base=bases[sheet["leaf_row_id"]]
        direct=base["direct_signature_base"]
        box=base["box"]
        max_abs_t=max(max_abs_t,abs(Fraction(box[0])),abs(Fraction(box[1])))
        need(base["direct_base_status"]=="DIRECT_WHOLE_LEAF_BASE_CERTIFIED","direct base")
        need(direct["whole_leaf_source_chart_classification"]=="STRICTLY_INSIDE_TRUE_SOURCE_CHART","source chart interior")
        need(direct["whole_leaf_box_outgoing_reasons"]==["outgoing_chart_seam"],"outgoing seam reason")
        need(sheet["Round173_half_open_rule"]=="E or W owns; N or S excludes","outgoing owner rule")
        need(sheet["owner_outgoing_cell"] in {"E","W"} and sheet["shadow_outgoing_cell"] in {"N","S"},"owner/shadow partition")
        need(sheet["deterministic_unique_owner_lineage"] is True and sheet["formal_half_open_owner_credit"]==1 and sheet["local_dimensional_owner_materialized"] is True,"unique owner")
        need(sheet["owner_signature_core_sha256"]==sheet["shadow_signature_core_sha256"] and sheet["signature_difference_field_allowlist"]==["outgoing_cell","target_chart"],"paired signature equality")
        need(sheet["incidence_is_not_a_global_component"] is True,"local incidence only")
        source_charts[base["chart"]]+=1; owner_shadow[(sheet["owner_outgoing_cell"],sheet["shadow_outgoing_cell"])]+=1
        rows.append(closed({
            "sheet_atlas_disposition_row_id": f"round228-sheet-atlas:{sheet['sheet_row_id'].split(':',1)[1]}",
            "sheet_row_id": sheet["sheet_row_id"], "leaf_row_id": sheet["leaf_row_id"], "source_chart": base["chart"],
            "whole_leaf_source_chart_classification": direct["whole_leaf_source_chart_classification"],
            "source_chart_seam_overlap_candidate": False, "owner_outgoing_cell": sheet["owner_outgoing_cell"], "shadow_outgoing_cell": sheet["shadow_outgoing_cell"],
            "outgoing_chart_duplicate_trace_disposition": "IDENTIFIED_NOT_ADDED__UNIQUE_E_OR_W_OWNER",
            "unclassified_atlas_overlap_channel": False, "physical_glue_credit_added": 0, "component_union_credit_added": 0,
        }))
    need(source_charts==Counter({"G:E":5726,"G:W":5726,"G:N":3132,"G:S":3132}),"chart census")
    need(owner_shadow==Counter({("E","N"):4429,("E","S"):4429,("W","N"):4429,("W","S"):4429}),"owner census")
    seam_square_gap=Fraction(1,2)-max_abs_t*max_abs_t
    need(max_abs_t==Fraction(90447,128000) and seam_square_gap==Fraction(11340191,16384000000)>0,"strict rational source-seam gap")
    return {
        "status":"CERTIFIED_ROUND211_SHEET_ATLAS_OVERLAP_EXHAUSTION__SOURCE_SEAM_ZERO__OUTGOING_SEAM_UNIQUE_OWNER__NO_NEW_EDGE",
        "formal_input_binding":{"Round171_certificate_sha256":R171_SHA,"Round171_result_sha256":R171_RESULT,"Round208_certificate_sha256":R208_SHA,"Round208_result_sha256":R208_RESULT,"Round211_certificate_sha256":R211_SHA,"Round211_result_sha256":R211_RESULT},
        "formal_sheet_atlas_disposition_ledger":ledger(rows),
        "census":{"Round211_sheet_count":17_716,"strictly_inside_true_source_chart_count":17_716,"maximum_absolute_t_over_all_sheet_leaf_boxes":str(max_abs_t),"exact_gap_from_true_source_seam_1_over_2_minus_max_t_squared":str(seam_square_gap),"true_source_seam_equation":"2*t^2-1=0","source_chart_seam_overlap_candidate_count":0,"outgoing_chart_unique_half_open_owner_count":17_716,"outgoing_chart_unowned_or_multiply_owned_count":0,"unclassified_atlas_overlap_channel_count":0,"new_physical_glue_credit":0,"new_component_union_credit":0},
        "source_chart_histogram":dict(sorted(source_charts.items())),
        "outgoing_owner_shadow_histogram":{f"{a}|{b}":count for (a,b),count in sorted(owner_shadow.items())},
        "scope_contract":{"true_source_chart_seams_exist_and_glue_exactly":True,"materialized_Round211_sheet_leaves_meet_true_source_chart_seams":False,"all_sheet_signature_pairs_match_except_outgoing_chart_fields":True,"outgoing_chart_seam_duplicate_trace_is_identified_not_added":True,"claim_applies_only_to_materialized_Round211_sheet_pool":True,"all_future_retained_strata_exhausted":False},
        "strict_nonpromotion":{"known_connectivity_blocks":7404,"known_connectivity_blocks_are_maximal_physical_components":False,"component_credit":0,"global_exact_key_disposition_credit":0,"source_G_global_exact_key_dispositions":"0/224580","D02":"BLOCKED","global_Gate5_fields":"10/18","CM2":"NO-GO_FOR_CLAIM"},
        "required_next":"combine frozen local contact closure, Round220 coordinate-only exclusion, Round227 symmetry non-glue, and this Round211 atlas-overlap exhaustion in a physical-equivalence reconstruction; do not promote until occurrence-fibre completeness is independently verified",
        "provenance":{"schema":SCHEMA,"producer_sha256":producer_sha256,"python_version":sys.version.split()[0]},
    }
def safe_write(data: bytes) -> None:
    fd,name=tempfile.mkstemp(prefix=f".{OUTPUT.name}.",suffix=".tmp",dir=HERE); temp=Path(name)
    try:
        with os.fdopen(fd,"wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temp,OUTPUT)
    finally:
        if temp.exists(): temp.unlink()
def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--no-write",action="store_true"); args=parser.parse_args(); producer_sha=hashlib.sha256(regular_bytes(Path(__file__),5_000_000)).hexdigest(); result=build(producer_sha); env={"schema":SCHEMA,"result":result,"result_sha256":digest(result)}; encoded=canonical(env)+b"\n"
    if not args.no_write: safe_write(encoded)
    print(result["status"]); print(f"producer_sha256={producer_sha}"); print(f"result_sha256={env['result_sha256']}"); print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}"); print("sheets=17716 source_seam_candidates=0 outgoing_unique_owner=17716 unclassified=0"); print("new_glue=0 component_credit=0"); return 0
if __name__=="__main__": raise SystemExit(main())
