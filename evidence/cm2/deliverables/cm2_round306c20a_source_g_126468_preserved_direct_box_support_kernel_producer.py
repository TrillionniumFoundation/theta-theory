#!/usr/bin/env python3
from __future__ import annotations
import argparse,gc,gzip,hashlib,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R174="cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json";R179="cm2_round179_source_g_residual_tube_arrangement_rows.json";R204="cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json";R208="cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={R174:"9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",R179:"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",R204:"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",R208:"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",MEM:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"};EXPECTED={"ROUND174_RESOLVED":72500,"ROUND179_RESOLVED":17192,"ROUND204_REGION":736,"ROUND208_REGION":36040}
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
def volume(box):return (Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]))
def add(src,mid,family,row_sha,chart,box,declared,kind):
 need(mid not in src and type(chart)is str and type(box)is list and len(box)==6,"source unique");v=volume(box);need(v>0 and Fraction(declared)==v,"source volume");src[mid]=(family,row_sha,chart,box,v,kind)
def sources():
 src={};d=json.loads((ROOT/R174).read_bytes())
 for r in d["result"]["resolved_3d_occurrence_rows"]:need(type(r)is list and len(r)==21,"R174 row");add(src,r[0],"ROUND174_RESOLVED",h(r),r[1],r[4],r[5],r[18])
 del d;gc.collect();d=json.loads((ROOT/R179).read_bytes())
 for r in d["result"]["resolved_3d_child_rows"]:need(type(r)is list and len(r)==20,"R179 row");add(src,r[0],"ROUND179_RESOLVED",h(r),r[3],r[6],r[7],r[18])
 del d;gc.collect();d=json.loads((ROOT/R204).read_bytes())
 for r in d["result"]["formal_local_open_3D_region_ledger"]["rows"]:
  b=dict(r);need(b.pop("row_sha256",None)==h(b),"R204 closure");add(src,r["region_row_id"],"ROUND204_REGION",r["row_sha256"],r["chart"],r["leaf_exact_box"],r["leaf_exact_coordinate_volume"],r["region_kind"])
 del d;gc.collect();d=json.loads((ROOT/R208).read_bytes())
 for r in d["result"]["formal_local_open_3D_signature_ledger"]["rows"]:
  b=dict(r);need(b.pop("row_sha256",None)==h(b),"R208 closure");add(src,r["region_row_id"],"ROUND208_REGION",r["row_sha256"],r["local_return_signature"]["source_chart"],r["Round182_leaf_box"],r["Round182_leaf_coordinate_volume"],r["whole_region_outgoing_chart_proof"])
 need(Counter(v[0] for v in src.values())==Counter(EXPECTED) and len(src)==126468,"source census");return src
def build(q):
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 src=sources();mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["coarse_family"]=="PRESERVED"};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["coarse_family"]=="PRESERVED" and r["representation_id"].startswith("k2i2-primary:")};need(set(src)==set(mem)==set(rep),"joins");out=[]
 for i,mid in enumerate(sorted(src,key=lambda x:x.encode())):
  family,row_sha,chart,box,v,kind=src[mid];ast={"kind":"OPEN_RATIONAL_BOX","coordinate_chart":chart,"coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}"};b={"schema":"cm2.round306c20a.source-g-126468-preserved-direct-box-support-kernel.v1.row.v1","ordinal":i,"member_id":mid,"fine_family":family,"representation_id":rep[mid]["representation_id"],"fresh_component_id":mem[mid]["fresh_component_id"],"support_ast":ast,"support_ast_sha256":h(ast),"construction_certificate":{"kind":"PINNED_DIRECT_CONSTRUCTION_ROW_IS_COMPLETE_PRESERVED_MEMBER_OPEN_BOX","source_family":family,"source_row_sha256":row_sha,"source_construction_kind":kind,"witness_envelope_or_promotion_summary_substitution_used":False},"formal_credit":{"member_typed_normalized_support":1,"primary_representation_set_equality":1},"strict_nonpromotion":{"alias_representation_set_equality":0,"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 d={"filename":L,"row_count":126468,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c20a.source-g-126468-preserved-direct-box-support-kernel.v1","status":"PASS_126468_PRESERVED_DIRECT_BOX_MEMBER_SUPPORTS_AND_PRIMARY_REPRESENTATION_EQUALITIES","family_census":EXPECTED,"member_support_credit":126468,"primary_representation_equality_credit":126468,"cumulative_member_support_credit":182072,"remaining_member_support_debt":320132,"remaining_preserved_alias_representation_debt":39276,"remaining_preserved_A1_A2_obligation_debt":80092,"ledger":d,"strict_nonpromotion":{"alias_representation_set_equality":0,"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
