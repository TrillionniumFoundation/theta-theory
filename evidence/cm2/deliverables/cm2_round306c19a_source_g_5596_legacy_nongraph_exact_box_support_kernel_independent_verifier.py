#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json"
F={"R179":"cm2_round179_source_g_residual_tube_arrangement_rows.json","R245":"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","R246":"cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","R247":"cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","MEM":"cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz","REP":"cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz"}
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
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");b=dict(z);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need(z["member_support_credit"]==5596 and z["primary_representation_equality_credit"]==5596 and z["remaining_nongraph_debt"]==50008 and z["ledger"]["row_count"]==5596,"census");need(z["strict_nonpromotion"]=={"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"nonpromotion");need((q/L).stat().st_size==z["ledger"]["size"] and fh(q/L)==z["ledger"]["sha256"],"descriptor")
 d179=json.loads((ROOT/F["R179"]).read_bytes());ret={x[0]:x[6] for x in d179["result"]["retained_3d_child_rows"]};src={}
 for key,path in (("R245","formal_retained_stratum_node_ledger"),("R246","formal_new_whole_signature_retained_stratum_node_ledger"),("R247","formal_new_crossing_and_source_seam_retained_stratum_node_ledger")):
  for r in json.loads((ROOT/F[key]).read_bytes())["result"][path]["rows"]:
   if key=="R245" and r["stratum_kind"]!="WHOLE_ROOT_ZERO_ABSENCE_BULK":continue
   bb=dict(r);need(bb.pop("row_sha256")==h(bb),"source closure");mid=r["retained_stratum_node_id"];fine="R245_WHOLE_ROOT_ZERO_ABSENCE_BULK" if key=="R245" else ("R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK" if key=="R246" else ("R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK" if r["source_classification"]=="CROSSING_TIME" else "R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK"));src[mid]=(ret[r["Round179_retained_child_row_id"]],fine,r["row_sha256"],r["Round179_retained_child_row_id"])
 need(len(src)==5596,"source census");mem={r["member_id"]:r for r in rows(ROOT/F["MEM"]) if r["member_id"] in src};rep={r["owner_member_id"]:r for r in rows(ROOT/F["REP"]) if r["owner_member_id"] in src};need(set(mem)==set(rep)==set(src),"joins")
 seen=set()
 for i,r in enumerate(rows(q/L)):
  mid=r["member_id"];need(mid in src and mid not in seen and r["ordinal"]==i,"order");seen.add(mid);box,fine,srow,rid=src[mid];v=(Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]));ast={"kind":"OPEN_RATIONAL_BOX","coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}"};need(r["representation_id"]==rep[mid]["representation_id"] and r["fresh_component_id"]==mem[mid]["fresh_component_id"] and r["fine_family"]==fine and r["support_ast"]==ast and r["support_ast_sha256"]==h(ast),"row body");need(r["construction_certificate"]=={"kind":"WHOLE_RETAINED_CHILD_EXACT_SUPPORT_EQUALITY","retained_child_row_id":rid,"retained_stratum_row_sha256":srow,"exact_full_support_not_witness_box":True} and r["formal_credit"]=={"member_typed_normalized_support":1,"primary_representation_set_equality":1},"credit")
 need(seen==set(src),"exhaustion");return {"status":"PASS_INDEPENDENT_C19A_5596_EXACT_BOX_SUPPORTS","result_sha256":claimed,"rows":5596}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
