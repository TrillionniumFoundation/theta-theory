#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import gzip,hashlib,json,os
from pathlib import Path
import sys
from typing import Any
ROOT=Path(__file__).resolve().parent;PREFIX="cm2_round306c17_source_g_15224_representation_pullback_kernel";SCHEMA="cm2.round306c17.source-g-15224-representation-pullback-kernel.v1";LEDGER=PREFIX+"_ledger.jsonl.gz";RESULT=PREFIX+"_result.json"
PINS={"C16B_REL":("cm2_round306c16b_source_g_relation_theorem_component_replay_positive_relation_ledger.jsonl.gz",7983980,"532da85010d3cef78ae5c8e46bb1e14c15fb8271934697c823fa76236daec38b"),"C16A_REP":("cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz",202540524,"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"),"C10_GRAPH":("cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz",19958893,"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),"C7_MEMBER":("cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz",269633111,"de85e6f26b64299d70c5006df76c5e4a242dc46d5b4885bca1f37b13d923c4e0"),"C14C_ADM":("cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz",2526805,"7f65ab28ad43a762d1e02bbd9d869965950b7b6d6db9cceef3fdd8cef12cc205")}
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
  for o,line in enumerate(f):
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(canonical(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==obj(b),"closure");yield o,r,hashlib.sha256(raw).hexdigest()
def close(b):return canonical({**b,"row_sha256":obj(b)})+b"\n"
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");p.add_argument("--publish",action="store_true");a=p.parse_args();need((a.candidate_dir is not None)!=a.publish,"mode");d=ROOT if a.publish else Path(a.candidate_dir).resolve()
 if not a.publish:d.mkdir(mode=0o700,parents=False,exist_ok=False)
 for role,(n,s,h) in PINS.items():q=ROOT/n;need(q.stat().st_size==s and fsha(q)==h,"pin:"+role)
 primary={}
 for o,r,w in rows("C7_MEMBER"):
  rep=r["primary_mechanical_representation_id"];need(type(rep)is str,"primary rep");primary[r["member_id"]]=rep
 for o,r,w in rows("C14C_ADM"):primary[r["new_exact_sheet_member_id"]]=r["new_canonical_representation_id"]
 need(len(primary)==502204,"primary endpoint census")
 repref={}
 for o,r,w in rows("C16A_REP"):
  rep=r["representation_id"]
  if primary.get(r["owner_member_id"])==rep:repref[rep]=(r["owner_member_id"],[o,r["row_id"],w,r["row_sha256"]],r["fresh_component_id"],r["coarse_family"])
 need(len(repref)==502204,"primary representation coverage")
 graph={}
 for o,r,w in rows("C10_GRAPH"):
  gid=r["graph_id"];need(gid not in graph,"graph unique");graph[gid]=(r,[o,r["row_id"],w,r["row_sha256"]])
 need(len(graph)==5264,"graph support census")
 relations=[];kinds=Counter();induced=set()
 for o,r,w in rows("C16B_REL"):
  gid=r["graph_id"];endpoint=r["endpoint_member_id"];need(gid in graph and endpoint in primary,"relation join");rep=primary[endpoint];owner,rr,component,family=repref[rep];need(owner==endpoint and component==r["endpoint_fresh_component_id"],"representation owner/component")
  support,sref=graph[gid];kind=r["relation_kind"]
  if kind=="GRAPH_TO_SHEET":
   need(r["formal_credit"]=={"graph_sheet_set_equality":1,"local_graph_side_physical_incidence":0,"one_sided_trace":0},"sheet theorem");certificate={"kind":"BIJECTIVE_GRAPH_PROJECTION_PULLBACK","map":"GRAPH_SUPPORT_TO_SHEET_BASE_PROJECTION","graph_sheet_set_equality":True,"pullback_of_endpoint_representation_equals_exact_graph_support":True}
  else:
   need(r["formal_credit"]=={"graph_sheet_set_equality":0,"local_graph_side_physical_incidence":1,"one_sided_trace":1},"side theorem");certificate={"kind":"EXACT_BOUNDARY_CLOSURE_TRACE_PULLBACK","map":"EXACT_GRAPH_BOUNDARY_TO_SIDE_STRATUM","local_physical_incidence":True,"one_sided_trace":True,"pullback_of_endpoint_representation_equals_exact_graph_boundary_stratum":True}
  certificate={**certificate,"certificate_sha256":obj([r["row_sha256"],support["row_sha256"],rr,rep,kind])};pullback_id="round306c17-induced-pullback-representation:"+obj([gid,r["row_id"],rep,certificate["certificate_sha256"]]);need(pullback_id not in induced,"pullback id unique");induced.add(pullback_id);rid=PREFIX+":pullback:"+obj([r["row_id"],rep]);relations.append((rid,{"schema":SCHEMA+".row.v1","row_id":rid,"relation_kind":kind,"graph_id":gid,"endpoint_member_id":endpoint,"endpoint_component_id":component,"endpoint_family":family,"endpoint_canonical_representation_id":rep,"induced_graph_pullback_representation_id":pullback_id,"C16b_relation_ref":[o,r["row_id"],w,r["row_sha256"]],"C16a_endpoint_representation_ref":rr,"C10_exact_graph_support_ref":sref,"pullback_certificate":certificate,"formal_credit":{"representation_pullback":1},"strict_nonpromotion":{"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}}));kinds[kind]+=1
 need(len(relations)==15224 and kinds=={"GRAPH_TO_SHEET":5264,"GRAPH_TO_SIDE":9960},"pullback census");relations.sort();q=d/LEDGER;raw=q.open("xb");gz=gzip.GzipFile(fileobj=raw,mode="wb",compresslevel=9,mtime=0);seq=hashlib.sha256()
 for ordinal,(_,b) in enumerate(relations):b["pullback_ordinal"]=ordinal;wire=close(b);gz.write(wire);seq.update(wire)
 gz.close();raw.flush();os.fsync(raw.fileno());raw.close();desc={"filename":LEDGER,"row_count":15224,"sequence_sha256":seq.hexdigest(),"size":q.stat().st_size,"sha256":fsha(q)};body={"schema":SCHEMA,"status":"PASS_15224_OF_15224_REPRESENTATION_PULLBACKS_SEALED__NORMALIZED_SUPPORT_PENDING","source_pins":[{"role":k,"filename":v[0],"size":v[1],"sha256":v[2]}for k,v in PINS.items()],"pullback_census":{"total":15224,"graph_to_sheet":5264,"graph_to_side":9960,"distinct_induced_pullback_representations":len(induced)},"ledger":desc,"formal_credit":{"representation_pullback":15224},"strict_nonpromotion":{"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"REBUILD_MEMBER_TYPED_NORMALIZED_SUPPORT_AND_CLEAR_SIX_FAMILY_SEMANTIC_DEBT"};result={**body,"result_sha256":obj(body)};(d/RESULT).write_bytes(canonical(result));print(json.dumps({"status":result["status"],"result_sha256":result["result_sha256"]},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
