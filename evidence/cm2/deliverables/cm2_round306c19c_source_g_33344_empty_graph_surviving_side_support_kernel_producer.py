#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C5="cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={C5:"8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",MEM:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"}
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
def build(q):
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 src={}
 for r in rows(ROOT/C5):
  s=r["semantic_classification"]
  if s["classification"]!="EMPTY_GRAPH":continue
  mid=s["surviving_side_member"];box=s["complete_parameter_domain"]["box"];need(mid not in src and len(box)==6 and s["graph_definition_disposition_credit"]==1,"C5 source")
  v=(Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]));need(v>0 and s["fixed_factor_sign_on_complete_domain"] in {"STRICT_NEGATIVE","STRICT_POSITIVE"},"complete domain")
  src[mid]=(r,s,box,v)
 need(len(src)==33344,"source census")
 mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["member_id"] in src};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["owner_member_id"] in src};need(set(src)==set(mem)==set(rep),"joins")
 out=[]
 for i,mid in enumerate(sorted(src,key=lambda x:x.encode())):
  source,s,box,v=src[mid];need(mem[mid]["coarse_family"]=="NON_GRAPH","family");ast={"kind":"HALF_OPEN_RATIONAL_BOX","coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}","lineage":s["complete_parameter_domain"]["half_open_owner_lineage"]};b={"schema":"cm2.round306c19c.source-g-33344-empty-graph-surviving-side-support-kernel.v1.row.v1","ordinal":i,"member_id":mid,"representation_id":rep[mid]["representation_id"],"fresh_component_id":mem[mid]["fresh_component_id"],"support_ast":ast,"support_ast_sha256":h(ast),"construction_certificate":{"kind":"C5_EMPTY_GRAPH_FIXED_SIGN_MAKES_SURVIVING_SIDE_EQUAL_COMPLETE_PARAMETER_DOMAIN","C5_row_sha256":source["row_sha256"],"graph_id":source["graph_id"],"surviving_side_role":s["surviving_side_role"],"invalid_side_role":s["invalid_side_role"],"fixed_factor_sign":s["fixed_factor_sign_on_complete_domain"],"empty_graph_proof_method":s["empty_graph_proof"]["method"],"inner_witness_or_R248_null_box_substitution_used":False},"formal_credit":{"member_typed_normalized_support":1,"primary_representation_set_equality":1},"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 d={"filename":L,"row_count":33344,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c19c.source-g-33344-empty-graph-surviving-side-support-kernel.v1","status":"PASS_33344_EMPTY_GRAPH_SURVIVING_SIDES_EQUAL_COMPLETE_PARAMETER_DOMAINS","member_support_credit":33344,"primary_representation_equality_credit":33344,"cumulative_nongraph_support_credit":51172,"remaining_nongraph_debt":4432,"ledger":d,"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
