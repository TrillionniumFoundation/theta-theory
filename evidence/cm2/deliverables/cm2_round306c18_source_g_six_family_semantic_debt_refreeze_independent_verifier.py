#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c18_source_g_six_family_semantic_debt_refreeze";L=P+"_ledger.jsonl.gz";R=P+"_result.json";M="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";RP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PB="cm2_round306c17_source_g_15224_representation_pullback_kernel_ledger.jsonl.gz";NG="cm2_round306c16b_source_g_relation_theorem_component_replay_negative_disposition_ledger.jsonl.gz"
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
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(c(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==h(b),"closure");yield r
def basecat(r):
 f=r["coarse_family"];p=r["member_id"].split(":",1)[0]
 if f=="PRESERVED":return "PRESERVED_DIRECT_GEOMETRY"
 if f=="R2":return "R2_SOURCE_FREE_INTERVAL_AND_REGLUE"
 if f=="R292":return "R292_FIXED_SIGN_SIGMA_AND_FACE"
 if f=="G2A":return "G2A_PULLBACK_CLOSED_SUPPORT_PENDING"
 if f=="G2B":return "G2B"
 if r["C14c_family_disposition_ref"] is not None:return "NON_GRAPH_RETAINED_OUTER_ENVELOPE"
 if p=="round248-wall-bulk":return "NON_GRAPH_WALL_BULK"
 return "NON_GRAPH_LEGACY_DIRECT"
def verify(q):
 raw=(q/R).read_bytes();x=json.loads(raw);need(c(x)==raw,"result canonical");b=dict(x);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need(x["member_count"]==502204 and x["representation_count"]==549616 and x["category_count"]==9 and x["pullback_closed_endpoint_count"]==15224 and x["negative_nonincidence_endpoint_count"]==168,"result census");need(x["strict_nonpromotion"]=={"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"nonpromotion");need((q/L).stat().st_size==x["ledger"]["size"] and fh(q/L)==x["ledger"]["sha256"],"descriptor")
 mc=Counter();owner={}
 for r in rows(ROOT/M):mc[basecat(r)]+=1;owner[r["member_id"]]=basecat(r)
 need(sum(mc.values())==502204,"member census");covered=set(r["endpoint_member_id"] for r in rows(ROOT/PB));neg=set(r["endpoint_member_id"] for r in rows(ROOT/NG));need(len(covered)==15224 and len(neg)==168,"relation partition")
 rc=Counter()
 for r in rows(ROOT/RP):
  cat=owner[r["owner_member_id"]]
  if cat=="G2B":cat="G2B_RELATION_BACKED_PULLBACK_CLOSED" if r["owner_member_id"] in covered else "G2B_NEGATIVE_NONINCIDENCE_SIDE"
  rc[cat]+=1
 exp={"PRESERVED_DIRECT_GEOMETRY":(126468,165744),"NON_GRAPH_LEGACY_DIRECT":(5596,5596),"NON_GRAPH_WALL_BULK":(45576,45576),"NON_GRAPH_RETAINED_OUTER_ENVELOPE":(4432,4432),"R2_SOURCE_FREE_INTERVAL_AND_REGLUE":(295336,302624),"R292_FIXED_SIGN_SIGMA_AND_FACE":(9404,10252),"G2A_PULLBACK_CLOSED_SUPPORT_PENDING":(5264,5264),"G2B_RELATION_BACKED_PULLBACK_CLOSED":(9960,9960),"G2B_NEGATIVE_NONINCIDENCE_SIDE":(168,168)};got={}
 for r in rows(q/L):got[r["category"]]=(r["member_count"],r["representation_count"]);need(r["formal_credit"]=={"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":0},"row nonpromotion")
 need(got==exp,"ledger census");need(all(rc[k]==v[1] for k,v in exp.items()),"representation partition");return {"status":"PASS_INDEPENDENT_C18_SEMANTIC_DEBT_REFREEZE","result_sha256":claimed,"categories":9,"members":502204,"representations":549616}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
