#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C5="cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz"
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
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");b=dict(z);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need((z["member_support_credit"],z["primary_representation_equality_credit"],z["cumulative_nongraph_support_credit"],z["remaining_nongraph_debt"],z["ledger"]["row_count"])==(33344,33344,51172,4432,33344),"census");need(z["strict_nonpromotion"]=={"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"nonpromotion");need(fh(q/L)==z["ledger"]["sha256"] and (q/L).stat().st_size==z["ledger"]["size"],"descriptor")
 src={}
 for source in rows(ROOT/C5):
  s=source["semantic_classification"]
  if s["classification"]!="EMPTY_GRAPH":continue
  mid=s["surviving_side_member"];box=s["complete_parameter_domain"]["box"];v=(Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]));need(mid not in src and v>0 and s["graph_definition_disposition_credit"]==1,"source");src[mid]=(source,s,box,v)
 need(len(src)==33344,"source census");mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["member_id"] in src};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["owner_member_id"] in src};need(set(src)==set(mem)==set(rep),"joins");seen=set()
 for i,r in enumerate(rows(q/L)):
  mid=r["member_id"];need(mid in src and mid not in seen and r["ordinal"]==i,"order");seen.add(mid);source,s,box,v=src[mid];ast={"kind":"HALF_OPEN_RATIONAL_BOX","coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}","lineage":s["complete_parameter_domain"]["half_open_owner_lineage"]};cert={"kind":"C5_EMPTY_GRAPH_FIXED_SIGN_MAKES_SURVIVING_SIDE_EQUAL_COMPLETE_PARAMETER_DOMAIN","C5_row_sha256":source["row_sha256"],"graph_id":source["graph_id"],"surviving_side_role":s["surviving_side_role"],"invalid_side_role":s["invalid_side_role"],"fixed_factor_sign":s["fixed_factor_sign_on_complete_domain"],"empty_graph_proof_method":s["empty_graph_proof"]["method"],"inner_witness_or_R248_null_box_substitution_used":False};need(r["representation_id"]==rep[mid]["representation_id"] and r["fresh_component_id"]==mem[mid]["fresh_component_id"] and r["support_ast"]==ast and r["support_ast_sha256"]==h(ast),"body");need(r["construction_certificate"]==cert and r["formal_credit"]=={"member_typed_normalized_support":1,"primary_representation_set_equality":1},"credit")
 need(seen==set(src),"exhaustion");return {"status":"PASS_INDEPENDENT_C19C_33344_COMPLETE_DOMAIN_SIDE_SUPPORTS","result_sha256":claimed,"rows":33344}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
