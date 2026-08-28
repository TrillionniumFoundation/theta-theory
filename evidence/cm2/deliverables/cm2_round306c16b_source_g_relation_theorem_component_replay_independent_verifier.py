#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import gzip,hashlib,json
from pathlib import Path
import sys
from typing import Any
ROOT=Path(__file__).resolve().parent;PREFIX="cm2_round306c16b_source_g_relation_theorem_component_replay";POS=PREFIX+"_positive_relation_ledger.jsonl.gz";NEG=PREFIX+"_negative_disposition_ledger.jsonl.gz";RESULT=PREFIX+"_result.json"
SOURCE={"C15_MEMBER":"cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz","C14A_EQ":"cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_equality_ledger.jsonl.gz","C14B_EQ":"cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_exact_sheet_member_ledger.jsonl.gz","C11A":"cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_ledger.jsonl.gz","C11B":"cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_relation_theorem_ledger.jsonl.gz","C12A":"cm2_round306c12a_source_g_rerouted_shared_side_kernel_ledger.jsonl.gz","C13":"cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition_ledger.jsonl.gz"}
class Rejected(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise Rejected(l)
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(v):return hashlib.sha256(canonical(v)).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open("rb")as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def rows(path):
 with gzip.open(path,"rb")as f:
  for o,line in enumerate(f):
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(canonical(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==obj(b),"closure");yield o,r,hashlib.sha256(raw).hexdigest()
def verify(candidate):
 raw=(candidate/RESULT).read_bytes();result=json.loads(raw);need(canonical(result)==raw,"result canonical");b=dict(result);claimed=b.pop("result_sha256");need(claimed==obj(b),"result closure")
 need(result["relation_census"]=={"positive":15224,"graph_to_sheet":5264,"graph_to_side":9960,"negative_dispositions":168},"result census");need(result["strict_nonpromotion"]=={"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"nonpromotion")
 for d in result["ledgers"].values():q=candidate/d["filename"];need(q.stat().st_size==d["size"] and fsha(q)==d["sha256"],"descriptor")
 meta={}
 for o,r,w in rows(ROOT/SOURCE["C15_MEMBER"]):meta[r["registry_member_id"]]=(r["base_root_id"],r["fresh_component_id"],r["official_key_id"],[o,r["row_id"],w,r["row_sha256"]])
 need(len(meta)==502204,"C15 exhaustion");expected={};classes=Counter()
 def add(role,o,r,w,kind,endpoint,endpoint_role,credit):
  root,component,key,mref=meta[endpoint];rid=PREFIX+":positive:"+obj([kind,r["graph_id"],endpoint,endpoint_role]);need(rid not in expected,"relation duplicate");expected[rid]=(kind,r["graph_id"],endpoint,endpoint_role,root,component,key,mref,role,[o,r["row_id"],w,r["row_sha256"]],credit);classes[kind]+=1
 for o,r,w in rows(ROOT/SOURCE["C14A_EQ"]):need(r["graph_sheet_set_equality_credit"]==1,"C14a");add("C14A_EQ",o,r,w,"GRAPH_TO_SHEET",r["sheet_member_id"],"SHEET",{"graph_sheet_set_equality":1,"local_graph_side_physical_incidence":0,"one_sided_trace":0})
 for o,r,w in rows(ROOT/SOURCE["C14B_EQ"]):need(r["graph_sheet_set_equality_credit"]==1,"C14b");add("C14B_EQ",o,r,w,"GRAPH_TO_SHEET",r["new_exact_sheet_member_id"],"EXACT_PARTIAL_SHEET",{"graph_sheet_set_equality":1,"local_graph_side_physical_incidence":0,"one_sided_trace":0})
 for role in("C11A","C12A"):
  for o,r,w in rows(ROOT/SOURCE[role]):need(r["scoped_credit"]=={"local_graph_side_physical_incidence":1,"one_sided_trace":1},role);add(role,o,r,w,"GRAPH_TO_SIDE",r["side_member_id"],r["side_role"],{"graph_sheet_set_equality":0,"local_graph_side_physical_incidence":1,"one_sided_trace":1})
 for o,r,w in rows(ROOT/SOURCE["C11B"]):need(r["local_graph_side_physical_incidence_proved"]and r["one_sided_trace_proved"],"C11b");add("C11B",o,r,w,"GRAPH_TO_SIDE",r["side_member_id"],r["side_role"],{"graph_sheet_set_equality":0,"local_graph_side_physical_incidence":1,"one_sided_trace":1})
 need(len(expected)==15224 and classes=={"GRAPH_TO_SHEET":5264,"GRAPH_TO_SIDE":9960},"positive exhaustion")
 seen=set()
 for o,r,w in rows(candidate/POS):
  rid=r["row_id"];need(rid in expected and rid not in seen,"candidate positive id");seen.add(rid);kind,graph,endpoint,endpoint_role,root,component,key,mref,role,sref,credit=expected[rid];need(r["relation_ordinal"]==o and r["relation_kind"]==kind and r["graph_id"]==graph and r["endpoint_member_id"]==endpoint and r["endpoint_role"]==endpoint_role and r["endpoint_base_root_id"]==root and r["endpoint_fresh_component_id"]==component and r["endpoint_official_key_id"]==key and r["C15_endpoint_member_ref"]==mref and r["theorem_source_role"]==role and r["theorem_source_ref"]==sref and r["formal_credit"]==credit,"positive replay")
 need(seen==set(expected),"positive candidate exhaustion")
 expected_neg={}
 for o,r,w in rows(ROOT/SOURCE["C13"]):
  endpoint=r["side_member_id"];root,component,key,mref=meta[endpoint];rid=PREFIX+":negative:"+obj([r["graph_id"],endpoint,r["side_role"]]);expected_neg[rid]=(r["graph_id"],endpoint,r["side_role"],root,component,key,mref,[o,r["row_id"],w,r["row_sha256"]])
 need(len(expected_neg)==168,"negative source")
 seen=set()
 for o,r,w in rows(candidate/NEG):
  rid=r["row_id"];need(rid in expected_neg and rid not in seen,"negative id");seen.add(rid);graph,endpoint,role,root,component,key,mref,sref=expected_neg[rid];need(r["disposition_ordinal"]==o and r["graph_id"]==graph and r["endpoint_member_id"]==endpoint and r["endpoint_role"]==role and r["endpoint_base_root_id"]==root and r["endpoint_fresh_component_id"]==component and r["endpoint_official_key_id"]==key and r["C15_endpoint_member_ref"]==mref and r["C13_source_ref"]==sref and r["formal_credit"]=={"relation_nonincidence_disposition":1} and r["representation_pullback_required"]is False,"negative replay")
 need(seen==set(expected_neg),"negative exhaustion");return {"status":"PASS_INDEPENDENT_C16B_RELATION_REPLAY_VERIFICATION","result_sha256":claimed,"positive":15224,"negative":168,"components":57876}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(json.dumps(verify(q),sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
