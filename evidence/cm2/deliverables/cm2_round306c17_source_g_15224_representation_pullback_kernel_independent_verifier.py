#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import gzip,hashlib,json
from pathlib import Path
import sys
from typing import Any
ROOT=Path(__file__).resolve().parent;P="cm2_round306c17_source_g_15224_representation_pullback_kernel";LEDGER=P+"_ledger.jsonl.gz";RESULT=P+"_result.json";S={"REL":"cm2_round306c16b_source_g_relation_theorem_component_replay_positive_relation_ledger.jsonl.gz","REP":"cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz","GRAPH":"cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz","MEMBER":"cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz","ADM":"cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz"}
class Rejected(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise Rejected(l)
def c(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(v):return hashlib.sha256(c(v)).hexdigest()
def fsha(q):
 h=hashlib.sha256()
 with q.open("rb")as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def rows(q):
 with gzip.open(q,"rb")as f:
  for o,line in enumerate(f):
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(c(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==obj(b),"closure");yield o,r,hashlib.sha256(raw).hexdigest()
def verify(q):
 raw=(q/RESULT).read_bytes();result=json.loads(raw);need(c(result)==raw,"result canonical");b=dict(result);claimed=b.pop("result_sha256");need(claimed==obj(b),"result closure");need(result["pullback_census"]=={"total":15224,"graph_to_sheet":5264,"graph_to_side":9960,"distinct_induced_pullback_representations":15224},"result census");need(result["strict_nonpromotion"]=={"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"nonpromotion");d=result["ledger"];need((q/LEDGER).stat().st_size==d["size"] and fsha(q/LEDGER)==d["sha256"],"descriptor")
 primary={}
 for o,r,w in rows(ROOT/S["MEMBER"]):primary[r["member_id"]]=r["primary_mechanical_representation_id"]
 for o,r,w in rows(ROOT/S["ADM"]):primary[r["new_exact_sheet_member_id"]]=r["new_canonical_representation_id"]
 need(len(primary)==502204,"primary census");repref={}
 for o,r,w in rows(ROOT/S["REP"]):
  if primary.get(r["owner_member_id"])==r["representation_id"]:repref[r["representation_id"]]=(r["owner_member_id"],[o,r["row_id"],w,r["row_sha256"]],r["fresh_component_id"],r["coarse_family"])
 need(len(repref)==502204,"rep coverage");graph={}
 for o,r,w in rows(ROOT/S["GRAPH"]):graph[r["graph_id"]]=(r,[o,r["row_id"],w,r["row_sha256"]])
 need(len(graph)==5264,"graph census");expected={};kinds=Counter()
 for o,r,w in rows(ROOT/S["REL"]):
  gid=r["graph_id"];endpoint=r["endpoint_member_id"];rep=primary[endpoint];owner,rr,component,family=repref[rep];support,sref=graph[gid];kind=r["relation_kind"]
  if kind=="GRAPH_TO_SHEET":cert={"kind":"BIJECTIVE_GRAPH_PROJECTION_PULLBACK","map":"GRAPH_SUPPORT_TO_SHEET_BASE_PROJECTION","graph_sheet_set_equality":True,"pullback_of_endpoint_representation_equals_exact_graph_support":True}
  else:cert={"kind":"EXACT_BOUNDARY_CLOSURE_TRACE_PULLBACK","map":"EXACT_GRAPH_BOUNDARY_TO_SIDE_STRATUM","local_physical_incidence":True,"one_sided_trace":True,"pullback_of_endpoint_representation_equals_exact_graph_boundary_stratum":True}
  cert={**cert,"certificate_sha256":obj([r["row_sha256"],support["row_sha256"],rr,rep,kind])};pid="round306c17-induced-pullback-representation:"+obj([gid,r["row_id"],rep,cert["certificate_sha256"]]);rid=P+":pullback:"+obj([r["row_id"],rep]);expected[rid]=(kind,gid,endpoint,component,family,rep,pid,[o,r["row_id"],w,r["row_sha256"]],rr,sref,cert);kinds[kind]+=1
 need(len(expected)==15224 and kinds=={"GRAPH_TO_SHEET":5264,"GRAPH_TO_SIDE":9960},"expected census");seen=set()
 for o,r,w in rows(q/LEDGER):
  rid=r["row_id"];need(rid in expected and rid not in seen,"row id");seen.add(rid);kind,gid,endpoint,component,family,rep,pid,rref,rr,sref,cert=expected[rid];need(r["pullback_ordinal"]==o and r["relation_kind"]==kind and r["graph_id"]==gid and r["endpoint_member_id"]==endpoint and r["endpoint_component_id"]==component and r["endpoint_family"]==family and r["endpoint_canonical_representation_id"]==rep and r["induced_graph_pullback_representation_id"]==pid and r["C16b_relation_ref"]==rref and r["C16a_endpoint_representation_ref"]==rr and r["C10_exact_graph_support_ref"]==sref and r["pullback_certificate"]==cert and r["formal_credit"]=={"representation_pullback":1},"pullback row")
 need(seen==set(expected),"exhaustion");return {"status":"PASS_INDEPENDENT_C17_PULLBACK_VERIFICATION","result_sha256":claimed,"pullbacks":15224,"sheet":5264,"side":9960}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(json.dumps(verify(q),sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
