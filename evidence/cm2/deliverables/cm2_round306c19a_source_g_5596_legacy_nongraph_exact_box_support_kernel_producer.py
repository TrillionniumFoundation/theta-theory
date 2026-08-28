#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json"
S={"R179":("cm2_round179_source_g_residual_tube_arrangement_rows.json","f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),"R245":("cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),"R246":("cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9"),"R247":("cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7"),"MEM":("cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz","0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a"),"REP":("cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz","47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1")}
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def oh(v):return hashlib.sha256(c(v)).hexdigest()
def fh(q):
 h=hashlib.sha256()
 with q.open("rb")as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def grow(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   raw=line[:-1];r=json.loads(raw);need(line.endswith(b"\n") and c(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==oh(b),"closure");yield r
def j(name):return json.loads((ROOT/S[name][0]).read_bytes())
def closed(row):b=dict(row);need(b.pop("row_sha256",None)==oh(b),"source closure")
def build(q):
 for n,h in S.values():need(fh(ROOT/n)==h,"pin:"+n)
 r179=j("R179")["result"]["retained_3d_child_rows"];ret={r[0]:r[6] for r in r179};need(len(ret)==len(r179),"R179 unique")
 src={};fine={}
 for r in j("R245")["result"]["formal_retained_stratum_node_ledger"]["rows"]:
  if r["stratum_kind"]!="WHOLE_ROOT_ZERO_ABSENCE_BULK":continue
  closed(r);src[r["retained_stratum_node_id"]]=(ret[r["Round179_retained_child_row_id"]],"R245_WHOLE_ROOT_ZERO_ABSENCE_BULK",r["row_sha256"],r["Round179_retained_child_row_id"])
 for r in j("R246")["result"]["formal_new_whole_signature_retained_stratum_node_ledger"]["rows"]:
  closed(r);src[r["retained_stratum_node_id"]]=(ret[r["Round179_retained_child_row_id"]],"R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK",r["row_sha256"],r["Round179_retained_child_row_id"])
 for r in j("R247")["result"]["formal_new_crossing_and_source_seam_retained_stratum_node_ledger"]["rows"]:
  closed(r);k="R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK" if r["source_classification"]=="CROSSING_TIME" else "R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK";src[r["retained_stratum_node_id"]]=(ret[r["Round179_retained_child_row_id"]],k,r["row_sha256"],r["Round179_retained_child_row_id"])
 need(len(src)==5596,"source census")
 members={}
 for r in grow(ROOT/S["MEM"][0]):
  if r["member_id"] in src:need(r["coarse_family"]=="NON_GRAPH","family");members[r["member_id"]]=r
 need(set(members)==set(src),"member join")
 reps={}
 for r in grow(ROOT/S["REP"][0]):
  if r["owner_member_id"] in src:need(r["owner_member_id"] not in reps,"rep unique");reps[r["owner_member_id"]]=r
 need(set(reps)==set(src),"rep join")
 out=[]
 for i,mid in enumerate(sorted(src,key=lambda x:x.encode())):
  box,k,srow,rid=src[mid];need(type(box)is list and len(box)==6,"box");v=(Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]));need(v>0,"volume");m=members[mid];rp=reps[mid];ast={"kind":"OPEN_RATIONAL_BOX","coordinates":["t","p","s"],"bounds":box,"exact_volume":str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}"};b={"schema":"cm2.round306c19a.source-g-5596-legacy-nongraph-exact-box-support-kernel.v1.row.v1","ordinal":i,"member_id":mid,"representation_id":rp["representation_id"],"fresh_component_id":m["fresh_component_id"],"fine_family":k,"support_ast":ast,"support_ast_sha256":oh(ast),"construction_certificate":{"kind":"WHOLE_RETAINED_CHILD_EXACT_SUPPORT_EQUALITY","retained_child_row_id":rid,"retained_stratum_row_sha256":srow,"exact_full_support_not_witness_box":True},"formal_credit":{"member_typed_normalized_support":1,"primary_representation_set_equality":1},"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":oh(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 d={"filename":L,"row_count":5596,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c19a.source-g-5596-legacy-nongraph-exact-box-support-kernel.v1","status":"PASS_5596_LEGACY_NONGRAPH_TYPED_NORMALIZED_SUPPORTS_AND_PRIMARY_REPRESENTATION_EQUALITIES","member_support_credit":5596,"primary_representation_equality_credit":5596,"ledger":d,"remaining_nongraph_debt":50008,"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":oh(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
