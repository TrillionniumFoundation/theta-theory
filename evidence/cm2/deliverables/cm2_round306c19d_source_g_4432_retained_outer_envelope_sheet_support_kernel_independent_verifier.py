#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19d_source_g_4432_retained_outer_envelope_sheet_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C14="cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_old_outer_envelope_family_disposition_ledger.jsonl.gz";R248="cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz"
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def h(v):return hashlib.sha256(c(v)).hexdigest()
def fh(q):
 x=hashlib.sha256()
 with q.open("rb")as f:
  while b:=f.read(1048576):x.update(b)
 return x.hexdigest()
def rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   raw=line[:-1];r=json.loads(raw);need(line.endswith(b"\n") and c(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==h(b),"closure");yield r
def verify(q):
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");b=dict(z);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need((z["member_support_credit"],z["primary_representation_equality_credit"],z["cumulative_nongraph_support_credit"],z["remaining_nongraph_debt"],z["ledger"]["row_count"])==(4432,4432,55604,0,4432),"census");need(z["strict_nonpromotion"]=={"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"nonpromotion");need(fh(q/L)==z["ledger"]["sha256"] and (q/L).stat().st_size==z["ledger"]["size"],"descriptor")
 disp={r["old_outer_envelope_sheet_member_id"]:r for r in rows(ROOT/C14)};owners={}
 for s in json.loads((ROOT/R248).read_bytes())["result"]["formal_wall_half_open_sheet_owner_ledger"]["rows"]:
  mid=s["wall_sheet_node_id"]
  if mid not in disp:continue
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R248 closure");rect=s["exact_closed_base_rectangle"];area=(Fraction(rect[1])-Fraction(rect[0]))*(Fraction(rect[3])-Fraction(rect[2]));need(area>0 and Fraction(s["exact_positive_2D_sheet_area"])==area and disp[mid]["R248_owner_row_sha256"]==s["row_sha256"],"owner");owners[mid]=(s,rect,area)
 need(len(disp)==4432 and set(owners)==set(disp),"source census");mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["member_id"] in disp};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["owner_member_id"] in disp};need(set(disp)==set(mem)==set(rep),"joins");seen=set()
 for i,r in enumerate(rows(q/L)):
  mid=r["member_id"];need(mid in disp and mid not in seen and r["ordinal"]==i,"order");seen.add(mid);d=disp[mid];s,rect,area=owners[mid];ast={"kind":"CLOSED_RATIONAL_RECTANGLE_SHEET","coordinates":["p","s"],"bounds":rect,"exact_area":str(area.numerator) if area.denominator==1 else f"{area.numerator}/{area.denominator}","ambient_coordinates":["t","p","s"],"ambient_3D_coordinate_volume":"0"};cert={"kind":"R248_HALF_OPEN_OWNER_ROW_DEFINES_COMPLETE_RETAINED_OUTER_ENVELOPE_SHEET","R248_owner_row_sha256":s["row_sha256"],"C14c_family_disposition_row_sha256":d["row_sha256"],"half_open_owner_rule":s["half_open_owner_rule"],"source_partition_kind":s["source_partition_kind"],"graph_projection_or_new_exact_partial_sheet_substitution_used":False};need(r["representation_id"]==rep[mid]["representation_id"] and r["fresh_component_id"]==mem[mid]["fresh_component_id"] and r["support_ast"]==ast and r["support_ast_sha256"]==h(ast),"body");need(r["construction_certificate"]==cert and r["formal_credit"]=={"member_typed_normalized_support":1,"primary_representation_set_equality":1},"credit")
 need(seen==set(disp),"exhaustion");return {"status":"PASS_INDEPENDENT_C19D_4432_OUTER_ENVELOPE_SHEET_SUPPORTS","result_sha256":claimed,"rows":4432}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
