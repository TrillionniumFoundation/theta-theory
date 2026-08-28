#!/usr/bin/env python3
"""Seal 832 current graph-sheet equalities and freeze 4,432 partial-sheet rematerializations."""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,stat,sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any,Final,Iterator
ROOT:Final=Path(__file__).parent;PREFIX:Final="cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier";SCHEMA:Final="cm2.round306c14a.source-g-graph-sheet-equality-and-partial-rematerialization-frontier.v1";EQ=PREFIX+"_equality_ledger.jsonl.gz";PART=PREFIX+"_partial_rematerialization_frontier.jsonl.gz";RESULT=PREFIX+"_result.json"
class Rejected(RuntimeError):pass
def need(x:bool,label:str)->None:
 if type(x) is not bool or not x:raise Rejected(label)
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def close(c:dict[str,Any])->dict[str,Any]:return {**c,"row_sha256":obj(c)}
def ref(r:dict[str,Any],field:str="row_id")->dict[str,str]:return {"row_id":r[field],"row_sha256":r["row_sha256"]}
@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
PINS:Final=(Pin("C7","cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz",9771275,"e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"),Pin("C10","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz",19958893,"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),Pin("C11B","cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_interface_kernel_ledger.jsonl.gz",288024,"815ed3b2ab73b3165e203cf8215421c89412b6d4f5190b816cb0d2e02f409a59"),Pin("C13_RESULT","cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition_result.json",3326,"9569d4d4d7c831942653d10c9a4cd328be66aca3466cc875c1c0aa01e15a5009"),Pin("R248","cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",205148977,"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"))
ZERO:Final={"representation_pullback":0,"member_normalized_support":0,"global_normalized_support":0,"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}
def read(p:Pin)->bytes:
 path=ROOT/p.filename;i=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(i.st_mode) and i.st_size==p.size,"pin size:"+p.role);raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==p.sha256,"pin sha:"+p.role);return raw
def rows(raw:bytes,label:str)->Iterator[dict[str,Any]]:
 with gzip.GzipFile(fileobj=io.BytesIO(raw)) as f:
  for n,l in enumerate(f):
   r=json.loads(l);c=dict(r);claimed=c.pop("row_sha256",None);need(claimed==obj(c),f"row closure:{label}:{n}");yield r
def legacy(raw:bytes)->dict[str,Any]:
 d=json.loads(raw);need(d["result_sha256"]==obj(d["result"]),"R248 closure");return d["result"]
def closed(raw:bytes)->dict[str,Any]:
 d=json.loads(raw);c=dict(d);need(c.pop("result_sha256")==obj(c),"C13 closure");return d
def rect(base:dict[str,Any])->list[str]:
 need(base["op"]=="AND","base conjunction");m={x.get("coordinate"):x for x in base["args"] if x.get("op")=="CLOSED_INTERVAL"};need(set(m)=={"p","s"},"base rectangle coordinates");return [m["p"]["lower"],m["p"]["upper"],m["s"]["lower"],m["s"]["upper"]]
def gz(rs:list[dict[str,Any]])->tuple[bytes,bytes]:
 plain=b"".join(canonical(r)+b"\n" for r in rs);b=io.BytesIO()
 with gzip.GzipFile(filename="",mode="wb",compresslevel=9,fileobj=b,mtime=0) as f:f.write(plain)
 return b.getvalue(),plain
def desc(name:str,wire:bytes,plain:bytes,rs:list[dict[str,Any]])->dict[str,Any]:return {"filename":name,"compression":"gzip-level9-mtime-zero","row_count":len(rs),"compressed_size":len(wire),"compressed_sha256":hashlib.sha256(wire).hexdigest(),"uncompressed_size":len(plain),"uncompressed_sha256":hashlib.sha256(plain).hexdigest(),"ordered_rows_sha256":obj(rs)}
def build()->tuple[dict[str,Any],bytes,bytes]:
 raw={p.role:read(p) for p in PINS};c13=closed(raw["C13_RESULT"]);need(c13["corrected_physical_relation_census"]["corrected_physical_denominator"]==15224,"C13 denominator")
 supports=list(rows(raw["C10"],"C10"));need(len(supports)==5264,"support census");c7={r["graph_id"]:r for r in rows(raw["C7"],"C7") if r["incidence_role"]=="GRAPH_TO_SHEET"};need(len(c7)==5264,"C7 graph-sheet census");r242={r["graph_id"]:r for r in rows(raw["C11B"],"C11b")};need(len(r242)==264,"R242 interface census");R=legacy(raw["R248"]);wanted={s["sheet_member_id"] for s in supports if s["graph_class"]!="R242_UNIQUE_GRAPH_FULL_PATCH"};owners={r["wall_sheet_node_id"]:r for r in R["formal_wall_half_open_sheet_owner_ledger"]["rows"] if r["wall_sheet_node_id"] in wanted};need(len(owners)==5000,"R248 sheet census")
 eq=[];partial=[];classes={}
 for s in sorted(supports,key=lambda r:r["graph_id"]):
  g=s["graph_id"];m=s["sheet_member_id"];rel=c7[g];need(rel["member_id"]==m and rel["incidence_statement_ast"]["proved"] is False,"C7 pending equality");need(s["support_properties"]["one_graph_point_per_exact_base_point"] is True,"projection bijection");rectangle=rect(s["base_domain_ast"]);cls=s["graph_class"];classes[cls]=classes.get(cls,0)+1
  if cls=="R235_TARGET_POSITIVE_PARTIAL_BASE":
   x=s["legacy_source_refs"]["R248_outer_envelope"];owner=owners[m];need(x["disposition"]=="OUTER_ENVELOPE_ONLY__NOT_FULL_GRAPH_SUPPORT" and x["rectangle"]==rectangle,"partial outer envelope");need(owner["exact_closed_base_rectangle"]==rectangle,"partial owner rectangle");extra=[n for n in s["base_domain_ast"]["args"] if n.get("op") not in {"CLOSED_INTERVAL"}];need(len(extra)==1 and extra[0]["op"]=="OR_DISJOINT","partial exact predicate");base_sha=s["ast_sha256"]["base_domain_ast_sha256"];proposal="round306c14-exact-partial-sheet:"+obj([g,base_sha]);partial.append(close({"schema":SCHEMA+".partial-rematerialization-row.v1","row_id":PREFIX+":partial:"+obj([g,m]),"partial_ordinal":len(partial),"graph_id":g,"old_outer_envelope_sheet_member_id":m,"C7_old_relation_ref":ref(rel),"C10_exact_support_ref":ref(s),"outer_envelope_rectangle":rectangle,"exact_partial_base_ast":s["base_domain_ast"],"exact_partial_base_ast_sha256":base_sha,"old_relation_disposition":"NOT_SET_EQUAL__OUTER_ENVELOPE_STRICTLY_COARSER_THAN_EXACT_PARTIAL_BASE","old_graph_sheet_set_equality_credit":0,"proposed_exact_sheet_natural_key":["ROUND306C14_EXACT_PARTIAL_BASE_SHEET",g,base_sha],"proposed_exact_sheet_member_id":proposal,"new_member_or_DSU_credit":0,"required_next":"REMATERIALIZE_AND_INDEPENDENTLY_VERIFY_EXACT_PARTIAL_SHEET"}))
   continue
  if cls in {"R235_SOURCE_EXACT_FACE_FULL_BASE","R235D_SOURCE_EXACT_FACE_FULL_BASE"}:
   owner=owners[m];x=next(v for k,v in s["legacy_source_refs"].items() if k.startswith("R248_identity_and_base_coordinate_lineage") or k.startswith("R248_identity_and_exact_base_lineage"));need(x["disposition"]=="EXACT_BASE_GEOMETRY_AVAILABLE__PHYSICAL_PULLBACK_PENDING" and x["rectangle"]==rectangle,"R248 exact base lineage");need(owner["exact_closed_base_rectangle"]==rectangle,"R248 exact sheet rectangle");authority={"kind":"R248_EXACT_CLOSED_BASE_SHEET_EQUALITY","R248_sheet_ref":{"row_id":owner["wall_sheet_node_id"],"row_sha256":owner["row_sha256"]},"exact_closed_base_rectangle":rectangle}
  else:
   need(cls=="R242_UNIQUE_GRAPH_FULL_PATCH","R242 class");k=r242[g];need(k["node_bundle"]["sheet"]["row_id"]==m and k["exact_closed_base_rectangle"]==rectangle,"R242 exact sheet patch");authority={"kind":"R242_R245_EXACT_FULL_PATCH_SHEET_EQUALITY","C11b_interface_kernel_ref":ref(k),"R245_sheet_ref":k["node_bundle"]["sheet"],"exact_closed_base_rectangle":rectangle}
  cert={"projection_map":"(t,p,s)->(p,s)","exact_graph_support_ast_sha256":s["ast_sha256"]["exact_support_ast_sha256"],"exact_base_domain_ast_sha256":s["ast_sha256"]["base_domain_ast_sha256"],"one_graph_point_for_every_exact_base_point":True,"every_graph_point_projects_into_exact_base":True,"projection_is_bijection":True,"current_sheet_support_equals_exact_base":True,"authority":authority};cert["certificate_sha256"]=obj(cert)
  eq.append(close({"schema":SCHEMA+".equality-row.v1","row_id":PREFIX+":equality:"+obj([g,m]),"equality_ordinal":len(eq),"graph_id":g,"graph_class":cls,"sheet_member_id":m,"C7_graph_sheet_relation_ref":ref(rel),"C10_exact_support_ref":ref(s),"graph_to_sheet_set_equality_certificate":cert,"graph_sheet_set_equality_credit":1,"representation_pullback_credit":0,"DSU_edge_or_union_authorized":False,"downstream_nonpromotion":ZERO}))
 need(len(eq)==832 and len(partial)==4432 and classes=={"R235_TARGET_POSITIVE_PARTIAL_BASE":4432,"R235_SOURCE_EXACT_FACE_FULL_BASE":552,"R242_UNIQUE_GRAPH_FULL_PATCH":264,"R235D_SOURCE_EXACT_FACE_FULL_BASE":16},"output census");ew,ep=gz(eq);pw,pp=gz(partial);source=Path(__file__).read_bytes();body={"schema":SCHEMA,"status":"PASS_832_CURRENT_GRAPH_SHEET_EQUALITIES__4432_PARTIAL_OUTER_ENVELOPES_FROZEN_FOR_EXACT_SHEET_REMATERIALIZATION","producer_source":{"filename":Path(__file__).name,"size":len(source),"sha256":hashlib.sha256(source).hexdigest()},"source_pins":[p.__dict__ for p in PINS],"census":{**classes,"current_graph_sheet_relations":5264,"set_equalities_proved":832,"outer_envelope_non_equal_relations":4432,"partial_sheet_rematerializations_required":4432},"scoped_credit":{"graph_sheet_set_equality":832},"formal_credit":ZERO,"strict_nonpromotion":{"partial_sheet_members_materialized":0,"old_outer_envelope_relations_promoted":0,"representation_pullback_proved":False,"DSU_edge_or_union_authorized":False,"normalized_support_sealed":False,"CM2":"NO-GO_FOR_CLAIM"},"equality_ledger":desc(EQ,ew,ep,eq),"partial_rematerialization_frontier":desc(PART,pw,pp,partial),"required_next":"REMATERIALIZE_4432_EXACT_PARTIAL_SHEETS_AND_AUDIT_MEMBER_EDGE_DSU_IMPACT"};return {**body,"result_sha256":obj(body)},ew,pw
def write(d:Path,n:str,b:bytes)->None:
 p=d/n;need(not p.exists(),"no clobber:"+n);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  off=0
  while off<len(b):off+=os.write(fd,b[off:])
  os.fsync(fd)
 finally:os.close(fd)
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");a=argparse.ArgumentParser();a.add_argument("--candidate-dir");a.add_argument("--publish",action="store_true");x=a.parse_args();need((x.candidate_dir is not None)!=x.publish,"one mode");r,e,p=build();d=ROOT if x.publish else Path(x.candidate_dir).resolve()
 if not x.publish:d.mkdir(mode=0o700,parents=False,exist_ok=False)
 write(d,EQ,e);write(d,PART,p);write(d,RESULT,canonical(r));print(json.dumps({"status":r["status"],"result_sha256":r["result_sha256"]},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
