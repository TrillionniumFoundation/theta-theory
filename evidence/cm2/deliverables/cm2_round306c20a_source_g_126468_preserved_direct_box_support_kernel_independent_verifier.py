#!/usr/bin/env python3
from __future__ import annotations
import argparse,gc,gzip,hashlib,json,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R174="cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json";R179="cm2_round179_source_g_residual_tube_arrangement_rows.json";R204="cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json";R208="cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";EXPECTED={"ROUND174_RESOLVED":72500,"ROUND179_RESOLVED":17192,"ROUND204_REGION":736,"ROUND208_REGION":36040}
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
def vol(x):return (Fraction(x[1])-Fraction(x[0]))*(Fraction(x[3])-Fraction(x[2]))*(Fraction(x[5])-Fraction(x[4]))
def add(s,m,f,r,ch,b,d,k):need(m not in s and type(ch)is str and vol(b)>0 and Fraction(d)==vol(b),"source");s[m]=(f,r,ch,b,vol(b),k)
def sources():
 s={};d=json.loads((ROOT/R174).read_bytes())
 for r in d["result"]["resolved_3d_occurrence_rows"]:add(s,r[0],"ROUND174_RESOLVED",h(r),r[1],r[4],r[5],r[18])
 del d;gc.collect();d=json.loads((ROOT/R179).read_bytes())
 for r in d["result"]["resolved_3d_child_rows"]:add(s,r[0],"ROUND179_RESOLVED",h(r),r[3],r[6],r[7],r[18])
 del d;gc.collect();d=json.loads((ROOT/R204).read_bytes())
 for r in d["result"]["formal_local_open_3D_region_ledger"]["rows"]:
  b=dict(r);need(b.pop("row_sha256")==h(b),"R204");add(s,r["region_row_id"],"ROUND204_REGION",r["row_sha256"],r["chart"],r["leaf_exact_box"],r["leaf_exact_coordinate_volume"],r["region_kind"])
 del d;gc.collect();d=json.loads((ROOT/R208).read_bytes())
 for r in d["result"]["formal_local_open_3D_signature_ledger"]["rows"]:
  b=dict(r);need(b.pop("row_sha256")==h(b),"R208");add(s,r["region_row_id"],"ROUND208_REGION",r["row_sha256"],r["local_return_signature"]["source_chart"],r["Round182_leaf_box"],r["Round182_leaf_coordinate_volume"],r["whole_region_outgoing_chart_proof"])
 need(len(s)==126468 and Counter(v[0] for v in s.values())==Counter(EXPECTED),"census");return s
def verify(q):
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");b=dict(z);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need((z["member_support_credit"],z["primary_representation_equality_credit"],z["cumulative_member_support_credit"],z["remaining_member_support_debt"],z["remaining_preserved_alias_representation_debt"],z["remaining_preserved_A1_A2_obligation_debt"],z["ledger"]["row_count"])==(126468,126468,182072,320132,39276,80092,126468),"census");need(z["family_census"]==EXPECTED and z["strict_nonpromotion"]=={"alias_representation_set_equality":0,"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"boundary");need(fh(q/L)==z["ledger"]["sha256"] and (q/L).stat().st_size==z["ledger"]["size"],"descriptor")
 src=sources();mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["coarse_family"]=="PRESERVED"};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["coarse_family"]=="PRESERVED" and r["representation_id"].startswith("k2i2-primary:")};need(set(src)==set(mem)==set(rep),"joins");seen=set()
 for i,r in enumerate(rows(q/L)):
  mid=r["member_id"];need(mid in src and mid not in seen and r["ordinal"]==i,"order");seen.add(mid);family,row_sha,chart,box,v,kind=src[mid];ast={"kind":"OPEN_RATIONAL_BOX","coordinate_chart":chart,"coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}"};cert={"kind":"PINNED_DIRECT_CONSTRUCTION_ROW_IS_COMPLETE_PRESERVED_MEMBER_OPEN_BOX","source_family":family,"source_row_sha256":row_sha,"source_construction_kind":kind,"witness_envelope_or_promotion_summary_substitution_used":False};need(r["fine_family"]==family and r["representation_id"]==rep[mid]["representation_id"] and r["fresh_component_id"]==mem[mid]["fresh_component_id"] and r["support_ast"]==ast and r["support_ast_sha256"]==h(ast),"body");need(r["construction_certificate"]==cert and r["formal_credit"]=={"member_typed_normalized_support":1,"primary_representation_set_equality":1},"credit")
 need(seen==set(src),"exhaustion");return {"status":"PASS_INDEPENDENT_C20A_126468_PRESERVED_DIRECT_BOX_SUPPORTS","result_sha256":claimed,"rows":126468}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
