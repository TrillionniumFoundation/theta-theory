#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R248="cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={R248:"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",MEM:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"}
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
 for r in json.loads((ROOT/R248).read_bytes())["result"]["formal_wall_positive_volume_bulk_ledger"]["rows"]:
  if r["exact_positive_3D_box"] is None:continue
  b=dict(r);need(b.pop("row_sha256")==h(b),"R248 closure");box=r["exact_positive_3D_box"];v=(Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]));need(v>0 and Fraction(r["exact_positive_3D_volume"])==v,"volume");src[r["wall_bulk_node_id"]]=(r,box,v)
 need(len(src)==12232,"source census");mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["member_id"] in src};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["owner_member_id"] in src};need(set(mem)==set(rep)==set(src),"joins");out=[]
 for i,mid in enumerate(sorted(src,key=lambda x:x.encode())):
  s,box,v=src[mid];need(mem[mid]["coarse_family"]=="NON_GRAPH","family");ast={"kind":"OPEN_RATIONAL_BOX","coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}"};b={"schema":"cm2.round306c19b.source-g-12232-r248-exact-positive-box-support-kernel.v1.row.v1","ordinal":i,"member_id":mid,"representation_id":rep[mid]["representation_id"],"fresh_component_id":mem[mid]["fresh_component_id"],"support_ast":ast,"support_ast_sha256":h(ast),"construction_certificate":{"kind":"R248_EXACT_POSITIVE_OPEN_BOX_IS_COMPLETE_MEMBER_SUPPORT","R248_row_sha256":s["row_sha256"],"source_partition_kind":s["source_partition_kind"],"source_partition_row_id":s["source_partition_row_id"],"witness_or_outer_envelope_substitution_used":False},"formal_credit":{"member_typed_normalized_support":1,"primary_representation_set_equality":1},"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 d={"filename":L,"row_count":12232,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c19b.source-g-12232-r248-exact-positive-box-support-kernel.v1","status":"PASS_12232_R248_EXACT_POSITIVE_BOX_TYPED_SUPPORTS_AND_PRIMARY_REPRESENTATION_EQUALITIES","member_support_credit":12232,"primary_representation_equality_credit":12232,"cumulative_nongraph_support_credit":17828,"remaining_nongraph_debt":37776,"ledger":d,"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
