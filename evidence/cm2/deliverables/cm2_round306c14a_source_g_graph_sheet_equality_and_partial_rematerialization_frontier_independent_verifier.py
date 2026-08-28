#!/usr/bin/env python3
"""Independent verifier for C14a equality/rematerialization split."""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,stat,sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any,Final,Iterator
ROOT:Final=Path(__file__).parent;PREFIX:Final="cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier";EQ:Final=PREFIX+"_equality_ledger.jsonl.gz";PART:Final=PREFIX+"_partial_rematerialization_frontier.jsonl.gz";RESULT:Final=PREFIX+"_result.json";MANIFEST:Final=PREFIX+"_manifest.sha256";PRODUCER_SHA:Final="c20813f2aed71f3b9c4ff165ed1c7350f700aa34ae8ca2fc6ca05a300cd9f5d8"
class Rejected(RuntimeError):pass
def need(x:bool,label:str)->None:
 if type(x) is not bool or not x:raise Rejected(label)
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def fsha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def ref(r:dict[str,Any])->dict[str,str]:return {"row_id":r["row_id"],"row_sha256":r["row_sha256"]}
@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
PINS:Final=(Pin("C7","cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz",9771275,"e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"),Pin("C10","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz",19958893,"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),Pin("C11B","cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_interface_kernel_ledger.jsonl.gz",288024,"815ed3b2ab73b3165e203cf8215421c89412b6d4f5190b816cb0d2e02f409a59"),Pin("C13_RESULT","cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition_result.json",3326,"9569d4d4d7c831942653d10c9a4cd328be66aca3466cc875c1c0aa01e15a5009"))
ZERO_KEYS:Final={"representation_pullback","member_normalized_support","global_normalized_support","DSU_edge","DSU_union","B1A","B2","maximality","CM2"}
def read(p:Pin)->bytes:
 path=ROOT/p.filename;i=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(i.st_mode) and i.st_size==p.size,"pin size:"+p.role);raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==p.sha256,"pin sha:"+p.role);return raw
def rows(raw:bytes,label:str)->Iterator[dict[str,Any]]:
 with gzip.GzipFile(fileobj=io.BytesIO(raw)) as f:
  for n,l in enumerate(f):
   r=json.loads(l);c=dict(r);claimed=c.pop("row_sha256",None);need(claimed==obj(c),f"row closure:{label}:{n}");yield r
def rectangle(base:dict[str,Any])->list[str]:
 m={x.get("coordinate"):x for x in base["args"] if x.get("op")=="CLOSED_INTERVAL"};need(set(m)=={"p","s"},"base rectangle");return [m["p"]["lower"],m["p"]["upper"],m["s"]["lower"],m["s"]["upper"]]
def descriptor(result:dict[str,Any],key:str,path:Path)->None:
 d=result[key];need(path.stat().st_size==d["compressed_size"] and fsha(path)==d["compressed_sha256"],key+" descriptor")
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");a=argparse.ArgumentParser();a.add_argument("--candidate-dir");a.add_argument("--manifest-first",action="store_true");x=a.parse_args();out=ROOT if x.candidate_dir is None else Path(x.candidate_dir).resolve()
 if x.manifest_first:
  m={}
  for line in (ROOT/MANIFEST).read_text("ascii").splitlines():d,sep,n=line.partition("  ");need(sep=="  " and n not in m,"manifest syntax");m[n]=d
  need(len(m)==9 and all(fsha(ROOT/n)==d for n,d in m.items()),"manifest members")
 raw={p.role:read(p) for p in PINS};rr=(out/RESULT).read_bytes();result=json.loads(rr);core=dict(result);claimed=core.pop("result_sha256",None);need(rr==canonical(result) and claimed==obj(core),"result closure");need(result["producer_source"]["sha256"]==PRODUCER_SHA,"producer binding");need(result["census"]=={"R235_TARGET_POSITIVE_PARTIAL_BASE":4432,"R235_SOURCE_EXACT_FACE_FULL_BASE":552,"R242_UNIQUE_GRAPH_FULL_PATCH":264,"R235D_SOURCE_EXACT_FACE_FULL_BASE":16,"current_graph_sheet_relations":5264,"set_equalities_proved":832,"outer_envelope_non_equal_relations":4432,"partial_sheet_rematerializations_required":4432},"result census");need(result["scoped_credit"]=={"graph_sheet_set_equality":832} and set(result["formal_credit"])==ZERO_KEYS and all(v==0 for v in result["formal_credit"].values()),"result credit");descriptor(result,"equality_ledger",out/EQ);descriptor(result,"partial_rematerialization_frontier",out/PART)
 supports={r["graph_id"]:r for r in rows(raw["C10"],"C10")};c7={r["graph_id"]:r for r in rows(raw["C7"],"C7") if r["incidence_role"]=="GRAPH_TO_SHEET"};r242={r["graph_id"]:r for r in rows(raw["C11B"],"C11b")};need(len(supports)==len(c7)==5264 and len(r242)==264,"source exhaustion")
 eq=list(rows((out/EQ).read_bytes(),"equality"));part=list(rows((out/PART).read_bytes(),"partial"));need(len(eq)==832 and len(part)==4432,"output counts");seen=set()
 for n,r in enumerate(eq):
  need(r["equality_ordinal"]==n,"equality order");s=supports[r["graph_id"]];q=c7[r["graph_id"]];need(r["C10_exact_support_ref"]==ref(s) and r["C7_graph_sheet_relation_ref"]==ref(q),"equality refs");need(r["sheet_member_id"]==s["sheet_member_id"]==q["member_id"],"equality subject");need(s["support_properties"]["one_graph_point_per_exact_base_point"] is True,"projection bijection source");cert=r["graph_to_sheet_set_equality_certificate"];cc=dict(cert);cs=cc.pop("certificate_sha256",None);need(cs==obj(cc),"equality certificate closure");need(cert["exact_graph_support_ast_sha256"]==s["ast_sha256"]["exact_support_ast_sha256"] and cert["exact_base_domain_ast_sha256"]==s["ast_sha256"]["base_domain_ast_sha256"],"equality AST binding");need(cert["projection_is_bijection"] is True and cert["current_sheet_support_equals_exact_base"] is True,"set equality theorem");rect=rectangle(s["base_domain_ast"]);need(cert["authority"]["exact_closed_base_rectangle"]==rect,"equality rectangle")
  if r["graph_class"]=="R242_UNIQUE_GRAPH_FULL_PATCH":
   k=r242[r["graph_id"]];need(cert["authority"]["kind"]=="R242_R245_EXACT_FULL_PATCH_SHEET_EQUALITY" and cert["authority"]["C11b_interface_kernel_ref"]==ref(k) and k["exact_closed_base_rectangle"]==rect,"R242 authority")
  else:
   need(r["graph_class"] in {"R235_SOURCE_EXACT_FACE_FULL_BASE","R235D_SOURCE_EXACT_FACE_FULL_BASE"} and cert["authority"]["kind"]=="R248_EXACT_CLOSED_BASE_SHEET_EQUALITY","R235 authority class");lineage=next(v for k,v in s["legacy_source_refs"].items() if k.startswith("R248_identity_and_"));need(lineage["disposition"]=="EXACT_BASE_GEOMETRY_AVAILABLE__PHYSICAL_PULLBACK_PENDING" and lineage["rectangle"]==rect,"sealed R248 exact lineage")
  need(r["graph_sheet_set_equality_credit"]==1 and r["representation_pullback_credit"]==0 and r["DSU_edge_or_union_authorized"] is False and set(r["downstream_nonpromotion"])==ZERO_KEYS and all(v==0 for v in r["downstream_nonpromotion"].values()),"equality scope");need(r["graph_id"] not in seen,"graph uniqueness");seen.add(r["graph_id"])
 for n,r in enumerate(part):
  need(r["partial_ordinal"]==n,"partial order");s=supports[r["graph_id"]];q=c7[r["graph_id"]];need(s["graph_class"]=="R235_TARGET_POSITIVE_PARTIAL_BASE" and r["C10_exact_support_ref"]==ref(s) and r["C7_old_relation_ref"]==ref(q),"partial refs");lineage=s["legacy_source_refs"]["R248_outer_envelope"];rect=rectangle(s["base_domain_ast"]);need(lineage["disposition"]=="OUTER_ENVELOPE_ONLY__NOT_FULL_GRAPH_SUPPORT" and lineage["rectangle"]==rect,"partial lineage");extra=[z for z in s["base_domain_ast"]["args"] if z.get("op")!="CLOSED_INTERVAL"];need(len(extra)==1 and extra[0]["op"]=="OR_DISJOINT","partial predicate");need(r["exact_partial_base_ast"]==s["base_domain_ast"] and r["exact_partial_base_ast_sha256"]==s["ast_sha256"]["base_domain_ast_sha256"],"partial AST");expected="round306c14-exact-partial-sheet:"+obj([r["graph_id"],r["exact_partial_base_ast_sha256"]]);need(r["proposed_exact_sheet_member_id"]==expected and r["new_member_or_DSU_credit"]==0 and r["old_graph_sheet_set_equality_credit"]==0,"partial boundary");need(r["graph_id"] not in seen,"graph uniqueness");seen.add(r["graph_id"])
 need(len(seen)==5264,"graph exhaustion");status="PASS_MANIFEST_FIRST_NO_WRITE_C14A_832_EQUALITIES_4432_FRONTIER" if x.manifest_first else "PASS_INDEPENDENT_C14A_832_EQUALITIES_4432_FRONTIER";print(json.dumps({"status":status,"result_sha256":claimed},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
