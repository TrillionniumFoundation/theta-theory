#!/usr/bin/env python3
"""Rematerialize ten missing local-shared relations onto their positive source graphs."""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,stat,sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any,Final,Iterator

ROOT:Final=Path(__file__).parent; PREFIX:Final="cm2_round306c12_source_g_local_shared_relation_reroute"; SCHEMA:Final="cm2.round306c12.source-g-local-shared-relation-reroute.v1"; ROW_SCHEMA:Final=SCHEMA+".rerouted-relation-row.v1"; LEDGER:Final=PREFIX+"_ledger.jsonl.gz"; RESULT:Final=PREFIX+"_result.json"
class Rejected(RuntimeError):pass
def need(x:bool,label:str)->None:
 if type(x) is not bool or not x:raise Rejected(label)
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def object_sha(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def closed_row(core:dict[str,Any])->dict[str,Any]:return {**core,"row_sha256":object_sha(core)}
def ref(r:dict[str,Any],id_field:str="row_id")->dict[str,str]:return {"row_id":r[id_field],"row_sha256":r["row_sha256"]}
@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
PINS:Final=(
 Pin("C11_MANIFEST","cm2_round306c11_source_g_graph_side_local_theorem_disposition_manifest.sha256",1652,"b087b80d90bc524af29ccbc0dc80ea82f157ae491404f64de342bb10c16d5d73"),Pin("C11_RESULT","cm2_round306c11_source_g_graph_side_local_theorem_disposition_result.json",12545,"083103ac958dfcb01283850abcda03fcdce26a8910c42b79c570a87486925506"),Pin("C11_FINDINGS","cm2_round306c11_source_g_graph_side_local_theorem_disposition_missing_local_shared_reroute_findings.jsonl.gz",13480,"3e257ca914aeb2306eab4064a118d5f1e28a753a215e694b137233a3b066f5c8"),
 Pin("C10_MANIFEST","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_manifest.sha256",1431,"b7277863feb9edc5f35906b04af2a9a256becb7ee9f1f1df6558b897184029ca"),Pin("C10_SUPPORT","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz",19958893,"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),Pin("C10_IDENTITY","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_member_identity_disposition_ledger.jsonl.gz",2966603,"5041df1ab4b5bf9e79984859f828c9fb69718f53bd62d2920d51ebea8b7ec9df"),
 Pin("C4_MANIFEST","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256",1177,"5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),Pin("C4_LEDGER","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz",101147,"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
 Pin("C7_MANIFEST","cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256",2184,"4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),Pin("C7_PHYSICAL","cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz",9771275,"e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"),
)
PIN={p.role:p for p in PINS}; ZERO={"local_graph_side_physical_incidence":0,"one_sided_trace":0,"graph_sheet_set_equality":0,"representation_pullback":0,"member_normalized_support":0,"global_normalized_support":0,"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}
class Snapshot:
 def __init__(self):self.data={}
 def __enter__(self):
  for p in PINS:
   path=ROOT/p.filename;info=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(info.st_mode) and info.st_size==p.size,"pin size:"+p.role);raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==p.sha256,"pin sha:"+p.role);self.data[p.role]=raw
  return self
 def __exit__(self,*a):return False
def rows(s:Snapshot,role:str)->Iterator[dict[str,Any]]:
 with gzip.GzipFile(fileobj=__import__('io').BytesIO(s.data[role])) as f:
  for i,line in enumerate(f):
   r=json.loads(line);core=dict(r);claimed=core.pop("row_sha256",None);need(claimed==object_sha(core),f"row closure:{role}:{i}");yield r
def manifest(s:Snapshot,role:str,members:tuple[str,...])->None:
 entries={}
 for line in s.data[role].decode().splitlines():
  digest,mark,name=line.partition("  ");need(mark=="  ","manifest syntax");entries[name]=digest
 for m in members:need(entries.get(PIN[m].filename)==PIN[m].sha256,"manifest member:"+m)
def gzip_rows(rs:list[dict[str,Any]])->tuple[bytes,bytes]:
 plain=b"".join(canonical(r)+b"\n" for r in rs);return gzip.compress(plain,compresslevel=9,mtime=0),plain
def build()->tuple[dict[str,Any],bytes]:
 with Snapshot() as s:
  manifest(s,"C11_MANIFEST",("C11_RESULT","C11_FINDINGS"));manifest(s,"C10_MANIFEST",("C10_SUPPORT","C10_IDENTITY"));manifest(s,"C4_MANIFEST",("C4_LEDGER",));manifest(s,"C7_MANIFEST",("C7_PHYSICAL",))
  c11=json.loads(s.data["C11_RESULT"]);core=dict(c11);need(core.pop("result_sha256")==object_sha(core),"C11 result closure");need(c11["disposition_census"]["missing_local_shared_reroute_findings"]==10,"C11 finding census");need(all(v==0 for v in c11["formal_credit"].values()),"C11 zero")
  findings=list(rows(s,"C11_FINDINGS"));need(len(findings)==10,"finding exhaustion")
  supports={r["graph_id"]:r for r in rows(s,"C10_SUPPORT")};identities={r["graph_id"]:r for r in rows(s,"C10_IDENTITY")};need(len(supports)==len(identities)==5264,"C10 exhaustion")
  bridges={r["bridge_row_id"]:r for r in rows(s,"C4_LEDGER")};need(len(bridges)==16,"C4 exhaustion")
  wanted={r["C7_surviving_target_shared_relation_ref"]["row_id"] for r in findings};c7={}
  for r in rows(s,"C7_PHYSICAL"):
   if r["row_id"] in wanted:c7[r["row_id"]]=r
  need(len(c7)==10,"C7 shared exhaustion")
  out=[];seen_graph=set();seen_side=set()
  for ordinal,f in enumerate(sorted(findings,key=lambda x:x["positive_source_graph_id"])):
   graph=f["positive_source_graph_id"];side=f["surviving_shared_side_member_id"];need(graph not in seen_graph and side not in seen_side,"reroute uniqueness");seen_graph.add(graph);seen_side.add(side)
   sup=supports[graph];ident=identities[graph];bridge=bridges[f["C4_bridge_ref"]["row_id"]];old=c7[f["C7_surviving_target_shared_relation_ref"]["row_id"]]
   need(f["C4_bridge_ref"]==ref(bridge,"bridge_row_id"),"finding C4 ref");need(f["C10_positive_source_support_ref"]==ref(sup) and f["C10_positive_source_identity_ref"]==ref(ident),"finding C10 refs")
   need(old["row_sha256"]==f["C7_surviving_target_shared_relation_ref"]["row_sha256"] and old["member_id"]==side and old["empty_graph_disposition_credit"]==1,"old target relation")
   need(old["incidence_statement_ast"]["side_role"]=="target:SAME_SIGN_EVENT_ABSENT" and old["graph_id"]==f["empty_target_graph_id"],"old relation semantics")
   commit=bridge["canonical_input_commitment"];need(commit["B1G0_source_shared_side_row"][1]==f["missing_source_shared_mechanical_row"]["row_id"],"missing source commitment");need(sup["legacy_source_refs"]["C4_exact_source_semantic_authority"]["row_id"]==bridge["bridge_row_id"] and sup["legacy_source_refs"]["C4_exact_source_semantic_authority"]["row_sha256"]==bridge["row_sha256"],"positive source binding")
   need(bridge["semantic_reconstruction"]["source_zero_set"]=="EXACT_FACE_GRAPH_t_EQUALS_0" and bridge["semantic_reconstruction"]["complete_domain_partition_verified"] is True,"C4 source theorem")
   need(f["component_relation"]=="SAME_BASE_ROOT" and f["shared_side_component_ref"]["fresh_component_id"]==f["source_graph_sheet_component_ref"]["fresh_component_id"],"same component")
   relation_id=PREFIX+":rerouted-relation:"+object_sha([graph,side])
   out.append(closed_row({"schema":ROW_SCHEMA,"row_id":relation_id,"reroute_ordinal":ordinal,"C11_finding_ref":ref(f),"C4_bridge_ref":ref(bridge,"bridge_row_id"),"C10_positive_source_support_ref":ref(sup),"C10_positive_source_identity_ref":ref(ident),"retired_empty_target_relation_ref":ref(old),"retired_empty_target_graph_id":f["empty_target_graph_id"],"positive_source_graph_id":graph,"sheet_member_id":sup["sheet_member_id"],"side_member_id":side,"side_role":"source:SAME_SIGN_EVENT_ABSENT","source_incidence_row_commitment":f["missing_source_shared_mechanical_row"],"component_relation":"SAME_BASE_ROOT","reroute_disposition":"REROUTED_EMPTY_TARGET_SHARED_SIDE_TO_POSITIVE_SOURCE_GRAPH","relation_reroute_disposition_credit":1,"local_graph_side_physical_incidence_proved":False,"one_sided_trace_proved":False,"representation_pullback_proved":False,"DSU_edge_or_union_authorized":False,"formal_credit":ZERO,"required_next":"PROVE_REROUTED_LOCAL_SHARED_SIDE_CARRIER_CLOSURE_AND_TRACE"}))
  need(len(out)==10,"output census");wire,plain=gzip_rows(out);desc={"filename":LEDGER,"compression":"gzip-level9-mtime-zero","row_count":10,"compressed_size":len(wire),"compressed_sha256":hashlib.sha256(wire).hexdigest(),"uncompressed_size":len(plain),"uncompressed_sha256":hashlib.sha256(plain).hexdigest(),"ordered_rows_sha256":object_sha(out)}
  body={"schema":SCHEMA,"status":"PASS_10_LOCAL_SHARED_RELATIONS_REROUTED_TO_POSITIVE_SOURCE_GRAPH__ZERO_LOCAL_THEOREM_AND_DOWNSTREAM_CREDIT","producer_source":{"filename":Path(__file__).name,"size":Path(__file__).stat().st_size,"sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},"source_pins":[p.__dict__ for p in PINS],"census":{"C11_findings":10,"rerouted_relations":10,"distinct_positive_source_graphs":10,"distinct_surviving_shared_side_members":10},"scoped_credit":{"relation_reroute_disposition":10},"formal_credit":ZERO,"strict_nonpromotion":{"physical_incidence_proved":False,"one_sided_trace_proved":False,"pullback_proved":False,"DSU_edge_or_union_authorized":False,"normalized_support_sealed":False,"CM2":"NO-GO_FOR_CLAIM"},"reroute_ledger":desc,"required_next":"PROVE_10_REROUTED_LOCAL_SHARED_SIDE_CARRIER_CLOSURE_AND_TRACE"};return {**body,"result_sha256":object_sha(body)},wire
def write_once(d:Path,n:str,b:bytes)->None:
 p=d/n;need(not p.exists(),"no clobber:"+n);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  off=0
  while off<len(b):off+=os.write(fd,b[off:])
  os.fsync(fd)
 finally:os.close(fd)
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir");ap.add_argument("--publish",action="store_true");a=ap.parse_args();need((a.candidate_dir is not None)!=a.publish,"one mode");result,wire=build();rw=canonical(result);d=ROOT if a.publish else Path(a.candidate_dir).resolve()
 if not a.publish:d.mkdir(mode=0o700,parents=False,exist_ok=False)
 write_once(d,LEDGER,wire);write_once(d,RESULT,rw);print(json.dumps({"status":result["status"],"result_sha256":result["result_sha256"],"files":[{"filename":LEDGER,"size":len(wire),"sha256":hashlib.sha256(wire).hexdigest()},{"filename":RESULT,"size":len(rw),"sha256":hashlib.sha256(rw).hexdigest()}]},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
