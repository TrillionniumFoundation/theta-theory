#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import gzip,hashlib,json,os
from pathlib import Path
import sys
from typing import Any
ROOT=Path(__file__).resolve().parent;PREFIX="cm2_round306c16b_source_g_relation_theorem_component_replay";SCHEMA="cm2.round306c16b.source-g-relation-theorem-component-replay.v1";POS=PREFIX+"_positive_relation_ledger.jsonl.gz";NEG=PREFIX+"_negative_disposition_ledger.jsonl.gz";RESULT=PREFIX+"_result.json"
PINS={"C15_MEMBER":("cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",142025813,"e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),"C14A_EQ":("cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_equality_ledger.jsonl.gz",415063,"09aff7b141e519a1d7252e4ad8becdb668b8b12f84c99cdb69ffe43ae3529883"),"C14B_EQ":("cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_exact_sheet_member_ledger.jsonl.gz",7121724,"6f69b5e82377cde72e7223e86b518da12e19ef85b93a5706989ebb81ab78a6d6"),"C11A":("cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_ledger.jsonl.gz",18096972,"87a37e007408adf667ae30a7575c928263512bf8a08cfd9e7144db11296680cd"),"C11B":("cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_relation_theorem_ledger.jsonl.gz",1328712,"37155fe874b8f4acd49773c013f4ec605a2f9388a0d1eb7443c88a731f1e0299"),"C12A":("cm2_round306c12a_source_g_rerouted_shared_side_kernel_ledger.jsonl.gz",13027,"12ae529eb5ccb53b75da1622c2c7b655a2acea6faf25d9018871a4fd079b35b9"),"C13":("cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition_ledger.jsonl.gz",97305,"fd226973ff16a60feb73e6bf4d36adcf5a361db7cd73db247eff8981876e68e7")}
class Blocked(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise Blocked(l)
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(v):return hashlib.sha256(canonical(v)).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open("rb")as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def rows(role):
 with gzip.open(ROOT/PINS[role][0],"rb")as f:
  for ordinal,line in enumerate(f):
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(canonical(r)==raw,"canonical");body=dict(r);need(body.pop("row_sha256",None)==obj(body),"closure");yield ordinal,r,hashlib.sha256(raw).hexdigest()
def close(b):return canonical({**b,"row_sha256":obj(b)})+b"\n"
class Writer:
 def __init__(self,d,n):self.path=d/n;need(not self.path.exists(),"clobber");self.raw=self.path.open("xb");self.gz=gzip.GzipFile(fileobj=self.raw,mode="wb",compresslevel=9,mtime=0);self.h=hashlib.sha256();self.count=0
 def add(self,b):w=close(b);self.gz.write(w);self.h.update(w);self.count+=1
 def finish(self):self.gz.close();self.raw.flush();os.fsync(self.raw.fileno());self.raw.close();return {"filename":self.path.name,"row_count":self.count,"sequence_sha256":self.h.hexdigest(),"size":self.path.stat().st_size,"sha256":fsha(self.path)}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");p.add_argument("--publish",action="store_true");a=p.parse_args();need((a.candidate_dir is not None)!=a.publish,"mode");d=ROOT if a.publish else Path(a.candidate_dir).resolve()
 if not a.publish:d.mkdir(mode=0o700,parents=False,exist_ok=False)
 for role,(n,s,h) in PINS.items():q=ROOT/n;need(q.stat().st_size==s and fsha(q)==h,"pin:"+role)
 meta={}
 for o,r,w in rows("C15_MEMBER"):meta[r["registry_member_id"]]=(r["base_root_id"],r["fresh_component_id"],r["official_key_id"],[o,r["row_id"],w,r["row_sha256"]])
 need(len(meta)==502204,"C15 members")
 positive=[];negative=[];classes=Counter()
 def add_positive(role,r,o,w,kind,endpoint,endpoint_role,credit):
  need(endpoint in meta,"endpoint admission");root,component,key,mref=meta[endpoint];rid=PREFIX+":positive:"+obj([kind,r["graph_id"],endpoint,endpoint_role]);positive.append((rid,{"schema":SCHEMA+".positive-row.v1","row_id":rid,"relation_kind":kind,"graph_id":r["graph_id"],"endpoint_member_id":endpoint,"endpoint_role":endpoint_role,"endpoint_base_root_id":root,"endpoint_fresh_component_id":component,"endpoint_official_key_id":key,"C15_endpoint_member_ref":mref,"theorem_source_role":role,"theorem_source_ref":[o,r["row_id"],w,r["row_sha256"]],"formal_credit":credit,"strict_nonpromotion":{"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"CM2":0}}));classes[kind]+=1
 for o,r,w in rows("C14A_EQ"):need(r["graph_sheet_set_equality_credit"]==1,"C14a credit");add_positive("C14A_EQ",r,o,w,"GRAPH_TO_SHEET",r["sheet_member_id"],"SHEET",{"graph_sheet_set_equality":1,"local_graph_side_physical_incidence":0,"one_sided_trace":0})
 for o,r,w in rows("C14B_EQ"):need(r["graph_sheet_set_equality_credit"]==1,"C14b credit");add_positive("C14B_EQ",r,o,w,"GRAPH_TO_SHEET",r["new_exact_sheet_member_id"],"EXACT_PARTIAL_SHEET",{"graph_sheet_set_equality":1,"local_graph_side_physical_incidence":0,"one_sided_trace":0})
 for role in("C11A","C12A"):
  for o,r,w in rows(role):need(r["scoped_credit"]=={"local_graph_side_physical_incidence":1,"one_sided_trace":1},role+" credit");add_positive(role,r,o,w,"GRAPH_TO_SIDE",r["side_member_id"],r["side_role"],{"graph_sheet_set_equality":0,"local_graph_side_physical_incidence":1,"one_sided_trace":1})
 for o,r,w in rows("C11B"):need(r["local_graph_side_physical_incidence_proved"]is True and r["one_sided_trace_proved"]is True,"C11b credit");add_positive("C11B",r,o,w,"GRAPH_TO_SIDE",r["side_member_id"],r["side_role"],{"graph_sheet_set_equality":0,"local_graph_side_physical_incidence":1,"one_sided_trace":1})
 need(classes=={"GRAPH_TO_SHEET":5264,"GRAPH_TO_SIDE":9960},"positive census")
 for o,r,w in rows("C13"):
  endpoint=r["side_member_id"];need(endpoint in meta and r["relation_nonincidence_disposition_credit"]==1,"C13 credit");root,component,key,mref=meta[endpoint];rid=PREFIX+":negative:"+obj([r["graph_id"],endpoint,r["side_role"]]);negative.append((rid,{"schema":SCHEMA+".negative-row.v1","row_id":rid,"graph_id":r["graph_id"],"endpoint_member_id":endpoint,"endpoint_role":r["side_role"],"endpoint_base_root_id":root,"endpoint_fresh_component_id":component,"endpoint_official_key_id":key,"C15_endpoint_member_ref":mref,"C13_source_ref":[o,r["row_id"],w,r["row_sha256"]],"formal_credit":{"relation_nonincidence_disposition":1},"representation_pullback_required":False,"strict_nonpromotion":{"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"CM2":0}}))
 need(len(positive)==15224 and len({x[0]for x in positive})==15224 and len(negative)==168 and len({x[0]for x in negative})==168,"relation uniqueness")
 positive.sort();negative.sort();pw=Writer(d,POS);nw=Writer(d,NEG)
 for ordinal,(_,b) in enumerate(positive):b["relation_ordinal"]=ordinal;pw.add(b)
 for ordinal,(_,b) in enumerate(negative):b["disposition_ordinal"]=ordinal;nw.add(b)
 pd=pw.finish();nd=nw.finish();body={"schema":SCHEMA,"status":"PASS_15224_POSITIVE_RELATIONS_168_NEGATIVE_DISPOSITIONS_REPLAYED_ON_C15_COMPONENTS__PULLBACK_PENDING","source_pins":[{"role":k,"filename":v[0],"size":v[1],"sha256":v[2]}for k,v in PINS.items()],"relation_census":{"positive":15224,"graph_to_sheet":5264,"graph_to_side":9960,"negative_dispositions":168},"component_base":{"members":502204,"components":57876},"ledgers":{"positive":pd,"negative":nd},"formal_credit":{"graph_sheet_set_equality_replay":5264,"graph_side_physical_incidence_replay":9960,"one_sided_trace_replay":9960,"negative_nonincidence_disposition_replay":168},"strict_nonpromotion":{"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"BUILD_15224_REPRESENTATION_PULLBACK_KERNEL"};result={**body,"result_sha256":obj(body)};(d/RESULT).write_bytes(canonical(result));print(json.dumps({"status":result["status"],"result_sha256":result["result_sha256"]},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
