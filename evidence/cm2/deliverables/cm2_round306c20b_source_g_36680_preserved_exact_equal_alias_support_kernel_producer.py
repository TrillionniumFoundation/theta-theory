#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20b_source_g_36680_preserved_exact_equal_alias_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";I2="cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz";R294="cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={C20:"bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",I2:"68774286f5e25c8e0e41ea42ee3b59fb601ea56d8540ef22e3b949cdce427e83",R294:"f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"};K="EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EVIDENCE"
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
 owner={r["member_id"]:r for r in rows(ROOT/C20)};need(len(owner)==126468,"C20 census")
 i2={r["source_row_id"]:r for r in rows(ROOT/I2) if r.get("representation_semantics")==K};need(len(i2)==36680,"I2 census");source={}
 with gzip.open(ROOT/R294,"rt")as f:d=json.load(f)
 for r in d["rows"]:
  if r["support_representation_kind"]!=K:continue
  b=dict(r);need(b.pop("row_sha256",None)==h(b),"R294 closure");rid=r["Round294_occurrence_representation_binding_row_id"];x=i2.get(rid);need(x is not None and x["source_row_sha256"]==r["row_sha256"] and x["owner_member_id"]==r["target_registry_occurrence_id"],"I2/R294 join");o=owner[x["owner_member_id"]]["support_ast"];need(r["exact_support_representation_box"]==o["bounds"] and r["physical_support_chart"]==o["coordinate_chart"] and r["formal_occurrence_alias_credit"]==1 and r["outer_envelope_used_as_inner_support"] is False,"exact equality");source[x["representation_id"]]=(x,r,o)
 need(len(source)==36680,"source census");rep={r["representation_id"]:r for r in rows(ROOT/REP) if r["representation_id"] in source};need(set(rep)==set(source),"C16 join");out=[]
 for i,rid in enumerate(sorted(source,key=lambda x:x.encode())):
  x,s,ast=source[rid];need(rep[rid]["owner_member_id"]==x["owner_member_id"],"owner");b={"schema":"cm2.round306c20b.source-g-36680-preserved-exact-equal-alias-support-kernel.v1.row.v1","ordinal":i,"representation_id":rid,"owner_member_id":x["owner_member_id"],"fresh_component_id":rep[rid]["fresh_component_id"],"representation_support_ast":ast,"representation_support_ast_sha256":h(ast),"set_equality_certificate":{"kind":"R294_EXACT_EQUAL_SUPPORT_ENVELOPE_ALIAS_EQUALS_C20A_OWNER_SUPPORT","R294_row_sha256":s["row_sha256"],"I2_representation_row_sha256":x["row_sha256"],"physical_support_chart":s["physical_support_chart"],"exact_box_equality":True,"interchart_or_subcover_promotion_used":False},"formal_credit":{"alias_representation_set_equality":1},"strict_nonpromotion":{"TPS_inclusion_subcover":0,"T2PS_refined_subcover":0,"R295A_adjacent_continuation":0,"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 desc={"filename":L,"row_count":36680,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c20b.source-g-36680-preserved-exact-equal-alias-support-kernel.v1","status":"PASS_36680_PRESERVED_EXACT_EQUAL_ALIAS_REPRESENTATION_SET_EQUALITIES","alias_representation_equality_credit":36680,"cumulative_preserved_representation_equality_credit":163148,"remaining_preserved_alias_representation_debt":2596,"remaining_alias_debt_by_kind":{"TPS_INCLUSION_SUBCOVER":720,"T2PS_REFINED_SUBCOVER":1600,"R295A_ADJACENT_CONTINUATION":276},"remaining_preserved_A1_A2_obligation_debt":80092,"ledger":desc,"strict_nonpromotion":{"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
