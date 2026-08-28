#!/usr/bin/env python3
"""No-materializer-import verifier for T11--T19 typed authority roles."""

from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable


ROOT=Path(__file__).resolve().parent.parent;D=ROOT/"deliverables";R=ROOT/".cm2-runtime/audit"
CERT=D/"cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
CERT_VERIFY=D/"cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
PRIMITIVE=D/"cm2_gate3_eight_cell_symmetry_atlas_cert.py"
QUOTIENT_SOURCE=D/"cm2_c27_explicit_quotient_map_alias_zero_credit_probe_v2.py"
QUOTIENT_RESULT=R/"c27-explicit-quotient-map-alias-v2-final-seed-30627301/cm2_c27_explicit_quotient_map_alias_zero_credit_v2_result.json"
R236=D/"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248=D/"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
COMMON_RESULT=R/"c27-legacy-terminal-typed-ownership-v1-seed-30650101/result.json"
ALIAS=R/"c27-legacy-terminal-typed-ownership-v1-seed-30650101/representation_alias_auxiliary_crosswalk.jsonl.gz"
PINS={CERT:"1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
      CERT_VERIFY:"effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
      PRIMITIVE:"d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
      QUOTIENT_SOURCE:"63cc28c2b1e7ea34b5ef313cdb3a68c71521e29409aa7551604acf90cef7ad5a",
      QUOTIENT_RESULT:"b6e01dfbae63628931105d9884d9ece46329c2ebb9f629931117e9b2861a2adc",
      R236:"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
      R248:"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
      COMMON_RESULT:"743eb648f62858508d38cec5cc533a3e3ceeb3e0852b642a82dba65377655542",
      ALIAS:"27e2d297025970e7d99200577151e104037aff6e1326b091e05c7281ae37be16"}
SEAMS={("E","N"):"TRUE_CYCLIC_SEAM_E_TO_N",("N","W"):"TRUE_CYCLIC_SEAM_N_TO_W",
       ("W","S"):"TRUE_CYCLIC_SEAM_W_TO_S",("S","E"):"TRUE_CYCLIC_SEAM_S_TO_E"}
ACTIONS={"Jx":"Jx_NEGATIVE_CONTROL","Jy":"Jy_NEGATIVE_CONTROL","JxJy":"JxJy_NEGATIVE_CONTROL"}


class Reject(RuntimeError):pass
def need(v:bool,l:str)->None:
    if type(v) is not bool or not v:raise Reject(l)
def encode(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v:Any)->str:return hashlib.sha256(encode(v)).hexdigest()
def fsha(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        while b:=f.read(8<<20):h.update(b)
    return h.hexdigest()
def closed(r:dict[str,Any],k:str,l:str)->None:
    c=r.get(k);b=dict(r);b.pop(k,None);need(type(c)is str and c==digest(b),l+":closure")
def jsonl(p:Path)->Iterable[dict[str,Any]]:
    with gzip.open(p,"rt",encoding="ascii") as f:
        for l in f:yield json.loads(l)
def close_sort(rows:list[dict[str,Any]],fields:tuple[str,...])->None:
    rows.sort(key=lambda r:tuple(str(r[f]) for f in fields))
    for i,r in enumerate(rows):r["ordinal"]=i;r["row_sha256"]=digest(r)
def load(p:Path,schema:str,label:str)->list[dict[str,Any]]:
    out=[]
    for i,r in enumerate(jsonl(p)):
        closed(r,"row_sha256",f"{label}:{i}");need(r["ordinal"]==i and r["schema"]==schema,f"{label}:{i}:wire");out.append(r)
    return out
def reconstruct_sheets()->tuple[list[dict[str,Any]],dict[str,Any]]:
    spec=importlib.util.spec_from_file_location("cm2_quotient_verify_pinned",QUOTIENT_SOURCE)
    need(spec is not None and spec.loader is not None,"quotient module")
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);sheets,audit=m.reconstruct_source_sheets()
    for fd in m.CAPTURE_FDS.values():
        try:m.os.close(fd)
        except OSError:pass
    return sheets,audit


def verify(directory:Path)->dict[str,Any]:
    for p,h in PINS.items():need(p.is_file() and not p.is_symlink() and fsha(p)==h,"pin:"+p.name)
    result_path=directory/"result.json";result=json.loads(result_path.read_bytes());closed(result,"result_sha256","result")
    need(result["candidate_ownership_total"]==4 and result["local_auxiliary_proof_row_total_T11_T18"]==52
         and result["external_alias_auxiliary_proof_rows_T19"]==276
         and result["total_proof_only_authority_rows"]==328
         and result["representation_alias_independent_candidate_count"]==0
         and result["reverse_rechart_independent_candidate_count"]==0
         and result["negative_control_independent_candidate_count"]==0
         and result["formal_credit"]==0 and result["manifest_authorized"] is False
         and result["source_W_transition_authorized"] is False
         and result["global_atom_and_full_twenty_family_totality_closed"] is False,"result semantics")
    candidate_path=directory/"t11_t19_atlas_seam_candidate_ownership.jsonl.gz"
    proof_path=directory/"t11_t18_auxiliary_proof_rows.jsonl.gz"
    slot_path=directory/"t11_t19_slot_authority.jsonl.gz"

    cert=json.loads(CERT.read_bytes())["result"]
    verify_r171=json.loads(CERT_VERIFY.read_bytes())["result"]
    need(verify_r171["status"]=="PASS" and verify_r171["producer_imported_or_executed"] is False,"R171 verify")
    candidates=[];proofs=[]
    for seam in cert["exact_source_G_coordinate_bridge"]["seam_rows"]:
        left,right=seam["left_face"],seam["right_face"];pair=(left["chart"],right["chart"]);terminal=SEAMS[pair]
        need(left["z"]=="+kappa" and right["z"]=="-kappa"
             and seam["normal_glues_exactly"] is True and seam["source_G_position_glues_exactly"] is True
             and seam["quarter_turn_and_velocity_glue_for_every_q"] is True,"seam")
        key=f"ATLAS_SEAM|{pair[0]}|{pair[1]}|+kappa|-kappa";cid=f"cm2-c27-independent:{terminal}:{key}"
        candidates.append({"schema":"cm2.c27-independent.atlas-seam.typed-candidate-ownership-row.v1",
          "candidate_id":cid,"candidate_key":key,"candidate_key_namespace":"ATLAS_FORWARD_SEAM",
          "candidate_unit":"ATLAS_FORWARD_SEAM","terminal":terminal,"terminal_assignment_cardinality":1,
          "forward_chart_pair":list(pair),"forward_faces":[left["z"],right["z"]],
          "source_seam_body_sha256":digest(seam),"R171_certificate_file_sha256":PINS[CERT],
          "formal_credit":0,"source_W_transition_authorized":False})
        proofs.append({"schema":"cm2.c27-independent.reverse-rechart.auxiliary-proof-row.v1",
          "proof_key":f"REVERSE_PROOF|{pair[1]}|{pair[0]}|-kappa|+kappa",
          "proof_key_namespace":"ATLAS_REVERSE_PROOF_ONLY","terminal":"REVERSE_RECHART",
          "forward_candidate_id":cid,"forward_chart_pair":list(pair),"reverse_chart_pair":[pair[1],pair[0]],
          "forward_faces":[left["z"],right["z"]],"reverse_faces":[right["z"],left["z"]],
          "inverse_of_exact_bijective_phase_glue":True,"same_equivalence_relation":True,
          "independent_terminal_candidate":False,"candidate_count_contribution":0,
          "new_physical_identification_added":False,"source_seam_body_sha256":digest(seam),
          "formal_credit":0,"source_W_transition_authorized":False})
    sheets,audit=reconstruct_sheets();need(len(sheets)==audit["source_sheet_count"]==16,"sheets")
    charts={}
    for raw in sorted(sheets,key=encode):
        member=raw["member_id"]
        sheet={"source_sheet_member_id":member,"source_partition_row_id":raw["partition_row_id"],
          "source_sheet_chart":raw["chart"],"source_t":raw["source_t"],"source_sheet_normal":raw["source_normal"],
          "source_sheet_position":raw["source_position"],"source_sheet_p_s_rectangle":raw["closed_p_s_rectangle"],
          "owner_official_key_id":raw["owner_official_key_id"],"owner_signature_sha256":raw["owner_signature_sha256"],
          "R248_row_sha256":raw["R248_row_sha256"]}
        p0,p1=map(Fraction,sheet["source_sheet_p_s_rectangle"][:2]);nx,ny=map(Fraction,sheet["source_sheet_normal"])
        need(p0<p1 and not(p0<=0<=p1) and nx*nx+ny*ny==1,"sheet math")
        charts[raw["chart"]]=charts.get(raw["chart"],0)+1
        for action,terminal in ACTIONS.items():
            if action=="Jx":eq=["n_x=0","q_x=0","s=0","p=0"];fact="SOURCE_N_X_NONZERO" if nx!=0 else "SOURCE_P_INTERVAL_EXCLUDES_ZERO"
            elif action=="Jy":eq=["n_y=0","q_y=0","p=0"];fact="SOURCE_N_Y_NONZERO" if ny!=0 else "SOURCE_P_INTERVAL_EXCLUDES_ZERO"
            else:eq=["n_x=0","n_y=0","q_x=0","q_y=0","s=0"];fact="UNIT_NORMAL_CANNOT_HAVE_N_X_EQUALS_N_Y_EQUALS_ZERO"
            proofs.append({"schema":"cm2.c27-independent.physical-action-negative-control.auxiliary-proof-row.v1",
              "proof_key":f"NEGATIVE_CONTROL|{action}|{member}","proof_key_namespace":"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY",
              "terminal":terminal,"action":action,"source_sheet_member_id":member,"source_sheet_projection":sheet,
              "source_sheet_projection_sha256":digest(sheet),"R248_source_sheet_row_sha256":raw["R248_row_sha256"],
              "fixed_point_equations":eq,"decisive_empty_fixed_set_fact":fact,"p_zero_in_open_interval":False,
              "fixed_sheet_point_family_count":0,"physical_action_is_quotient_identification":False,
              "independent_terminal_candidate":False,"candidate_count_contribution":0,"formal_credit":0,
              "source_W_transition_authorized":False})
    need(charts=={"G:E":4,"G:N":4,"G:S":4,"G:W":4},"chart census")
    close_sort(candidates,("terminal","candidate_key"));close_sort(proofs,("terminal","proof_key"))
    observed_candidates=load(candidate_path,"cm2.c27-independent.atlas-seam.typed-candidate-ownership-row.v1","candidate")
    # Mixed proof schemas are checked after generic row closure.
    observed_proofs=[]
    for i,row in enumerate(jsonl(proof_path)):
        closed(row,"row_sha256",f"proof:{i}");need(row["ordinal"]==i,"proof ordinal");observed_proofs.append(row)
    need(observed_candidates==candidates and observed_proofs==proofs,"exact inverse rows")
    slots=load(slot_path,"cm2.c27-independent.t11-t19.slot-authority-row.v1","slot")
    observed_slot_roles=[(r["slot"],r["terminal"],r["role"],r["candidate_count"],
                          r["authority_row_count"],r["candidate_key_namespace"],
                          r["proof_key_namespace"],r["formal_credit"],
                          r["source_W_transition_authorized"]) for r in slots]
    expected_slot_roles=[
      ("T11","REVERSE_RECHART","AUXILIARY_INVERSE_PROOF_ONLY",0,4,None,"ATLAS_REVERSE_PROOF_ONLY",0,False),
      ("T12","TRUE_CYCLIC_SEAM_E_TO_N","CANDIDATE_OWNERSHIP",1,1,"ATLAS_FORWARD_SEAM",None,0,False),
      ("T13","TRUE_CYCLIC_SEAM_N_TO_W","CANDIDATE_OWNERSHIP",1,1,"ATLAS_FORWARD_SEAM",None,0,False),
      ("T14","TRUE_CYCLIC_SEAM_W_TO_S","CANDIDATE_OWNERSHIP",1,1,"ATLAS_FORWARD_SEAM",None,0,False),
      ("T15","TRUE_CYCLIC_SEAM_S_TO_E","CANDIDATE_OWNERSHIP",1,1,"ATLAS_FORWARD_SEAM",None,0,False),
      ("T16","Jx_NEGATIVE_CONTROL","NEGATIVE_CONTROL_PROOF_ONLY",0,16,None,"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY",0,False),
      ("T17","Jy_NEGATIVE_CONTROL","NEGATIVE_CONTROL_PROOF_ONLY",0,16,None,"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY",0,False),
      ("T18","JxJy_NEGATIVE_CONTROL","NEGATIVE_CONTROL_PROOF_ONLY",0,16,None,"PHYSICAL_ACTION_NEGATIVE_CONTROL_PROOF_ONLY",0,False),
      ("T19","REPRESENTATION_ALIASES","AUXILIARY_ALIAS_PROOF_ONLY",0,276,None,"REPRESENTATION_ALIAS_AUXILIARY_CROSSWALK",0,False)]
    need(len(slots)==9 and observed_slot_roles==expected_slot_roles,"slot exact roles/namespaces/census")
    need(all(r["exact_candidate_key_disjointness_rule"].startswith(
             "ONLY_ATLAS_FORWARD_SEAM_ROWS_ENTER_T11_T19_CANDIDATE_UNION") for r in slots),
         "slot disjointness rule")
    aliases=list(jsonl(ALIAS));need(len(aliases)==276,"aliases")
    for i,row in enumerate(aliases):
        closed(row,"row_sha256",f"alias:{i}");need(row["independent_terminal_candidate"] is False
             and row["representation_alias_terminal_candidate_count"]==0,"alias proof-only")
    for p in (candidate_path,proof_path,slot_path):
        d=result["ledgers"][p.name];need(fsha(p)==d["file_sha256"] and d["row_count"] in {4,52,9},"descriptor:"+p.name)
    body={"schema":"cm2.c27-independent.t11-t19-atlas-control-alias-authority.verification.v1",
      "status":"PASS_NO_MATERIALIZER_IMPORT__T11_T19_EXACT_INVERSE__4_CANDIDATES__328_PROOF_ONLY_ROWS__ZERO_CREDIT",
      "materializer_imported_or_executed":False,"candidate_ownership_total":4,
      "local_auxiliary_proof_rows":52,"external_alias_auxiliary_proof_rows":276,
      "total_proof_only_authority_rows":328,"source_sheet_count":16,
      "reverse_candidate_count":0,"negative_control_candidate_count":0,"alias_candidate_count":0,
      "candidate_key_namespaces_pairwise_disjoint":True,"result_file_sha256":fsha(result_path),
      "formal_credit":0,"manifest_authorized":False,"source_W_transition_authorized":False,
      "global_atom_and_full_twenty_family_totality_closed":False}
    return {**body,"verification_sha256":digest(body)}


def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    try:
        v=verify(Path(a.candidate_dir).resolve());o=Path(a.output);need(not o.exists(),"fresh output");o.write_bytes(encode(v)+b"\n")
    except (Reject,KeyError,TypeError,ValueError,OSError,json.JSONDecodeError) as e:print("REJECT:"+str(e));return 2
    print(encode({"status":v["status"],"verification_sha256":v["verification_sha256"]}).decode("ascii"));return 0
if __name__=="__main__":raise SystemExit(main())
