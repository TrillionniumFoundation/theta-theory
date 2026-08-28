#!/usr/bin/env python3
"""Discharge 168 blocked graph-side joins as empty on their exact carriers."""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,stat,sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any,Final,Iterator

ROOT:Final=Path(__file__).parent;PREFIX:Final="cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition";SCHEMA:Final="cm2.round306c13.source-g-blocked-relation-empty-carrier-disposition.v1";ROW_SCHEMA:Final=SCHEMA+".row.v1";LEDGER:Final=PREFIX+"_ledger.jsonl.gz";RESULT:Final=PREFIX+"_result.json"
class Rejected(RuntimeError):pass
def need(x:bool,label:str)->None:
 if type(x) is not bool or not x:raise Rejected(label)
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def close(core:dict[str,Any])->dict[str,Any]:return {**core,"row_sha256":obj(core)}
def ref(r:dict[str,Any],field:str="row_id")->dict[str,str]:return {"row_id":r[field],"row_sha256":r["row_sha256"]}
@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
PINS:Final=(
 Pin("BLOCKED","cm2_round306c11_source_g_graph_side_local_theorem_disposition_blocked_ledger.jsonl.gz",43313,"8607da23d37de93d6cdf8e04a36d2f70d7908e8b55a8595cd34693f377479bdf"),Pin("DISPOSITION","cm2_round306c11_source_g_graph_side_local_theorem_disposition_disposition_ledger.jsonl.gz",10888167,"b1af6336b83842f2c6380929977f6d3591cfb50a1b305c7eafd197931d623543"),Pin("SUPPORT","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz",19958893,"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),Pin("C4","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz",101147,"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),Pin("R235","cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json",67765471,"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),Pin("R248","cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",205148977,"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),)
ZERO:Final={"local_graph_side_physical_incidence":0,"one_sided_trace":0,"graph_sheet_set_equality":0,"representation_pullback":0,"member_normalized_support":0,"global_normalized_support":0,"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}
def read(p:Pin)->bytes:
 path=ROOT/p.filename;i=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(i.st_mode) and i.st_size==p.size,"pin size:"+p.role);raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==p.sha256,"pin sha:"+p.role);return raw
def rows(raw:bytes,label:str)->Iterator[dict[str,Any]]:
 with gzip.GzipFile(fileobj=io.BytesIO(raw)) as f:
  for n,line in enumerate(f):
   r=json.loads(line);core=dict(r);claimed=core.pop("row_sha256",None);need(claimed==obj(core),f"row closure:{label}:{n}");yield r
def legacy(raw:bytes,label:str)->dict[str,Any]:
 d=json.loads(raw);need(d["result_sha256"]==obj(d["result"]),"legacy closure:"+label);return d["result"]
def t_bounds(s:dict[str,Any])->tuple[Fraction, Fraction]:
 nodes=s["carrier_domain_ast"]["args"];t=next(n for n in nodes if n.get("op")=="CLOSED_INTERVAL" and n.get("coordinate")=="t");lo,hi=Fraction(t["lower"]),Fraction(t["upper"]);need(lo<hi and (lo==0 or hi==0),"one-sided t carrier");return lo,hi
def factor_exact(s:dict[str,Any])->None:
 need(s["equation_ast"]=={"op":"EQ","left":{"op":"MUL","args":[{"op":"RATIONAL_CONSTANT","value":"9/25"},{"op":"COORDINATE","name":"t"}]},"right":{"op":"RATIONAL_CONSTANT","value":"0"}},"exact 9/25*t equation")
def gzip_rows(rs:list[dict[str,Any]])->tuple[bytes,bytes]:
 plain=b"".join(canonical(r)+b"\n" for r in rs);b=io.BytesIO()
 with gzip.GzipFile(filename="",mode="wb",compresslevel=9,fileobj=b,mtime=0) as f:f.write(plain)
 return b.getvalue(),plain
def build()->tuple[dict[str,Any],bytes]:
 raw={p.role:read(p) for p in PINS};blocked=list(rows(raw["BLOCKED"],"blocked"));need(len(blocked)==168,"blocked census")
 wanted_disp={r["disposition_ref"]["row_id"] for r in blocked};disp={r["row_id"]:r for r in rows(raw["DISPOSITION"],"disposition") if r["row_id"] in wanted_disp}
 wanted_graph={r["graph_id"] for r in blocked};support={r["graph_id"]:r for r in rows(raw["SUPPORT"],"support") if r["graph_id"] in wanted_graph};bridges={r["bridge_row_id"]:r for r in rows(raw["C4"],"C4")}
 r235_result=legacy(raw["R235"],"R235");r235={r["endpoint_graph_partition_row_id"]:r for r in r235_result["single_endpoint_graph_partition_rows"] if r["endpoint_graph_partition_row_id"] in wanted_graph}
 r248_result=legacy(raw["R248"],"R248");wanted_side={r["side_member_id"] for r in blocked};bulk={r["wall_bulk_node_id"]:r for r in r248_result["formal_wall_positive_volume_bulk_ledger"]["rows"] if r["wall_bulk_node_id"] in wanted_side}
 need(len(disp)==len(support)==len(bulk)==168 and len(bridges)==16 and len(r235)==152,"input exhaustion")
 out=[];census={"R235_EVENT_ABSENT":0,"R235_EVENT_PRESENT":0,"R235D_NEGATIVE_TO_POSITIVE":0};seen=set()
 for b in sorted(blocked,key=lambda r:r["row_id"]):
  d=disp[b["disposition_ref"]["row_id"]];s=support[b["graph_id"]];v=bulk[b["side_member_id"]];need(ref(d)==b["disposition_ref"],"blocked-disposition binding");need(d["graph_id"]==b["graph_id"] and d["side_member_id"]==b["side_member_id"],"subject binding");need(d["component_relation"] in {"CROSS_COMPONENT","SAME_BASE_ROOT"} and d["DSU_edge_or_union_authorized"] is False,"zero edge boundary");need(v["exact_positive_3D_box"] is None and v["exact_positive_3D_volume"] is None and v["physical_component_credit"]==0,"R248 no geometry");factor_exact(s);lo,hi=t_bounds(s);zero_face="LOWER" if lo==0 else "UPPER";inward=1 if zero_face=="LOWER" else -1
  if b["graph_class"]=="R235_SOURCE_EXACT_FACE_FULL_BASE":
   p=r235[b["graph_id"]];need(p["active_endpoint_factor"]=="source" and p["active_factor_strict_t_derivative_sign"]=="STRICT_POSITIVE","R235 source derivative");eta=1 if p["fixed_endpoint_factor_sign"]=="STRICT_POSITIVE" else -1;local_role="EVENT_ABSENT" if eta*inward>0 else "EVENT_PRESENT";need(b["side_role"] in {"EVENT_ABSENT","EVENT_PRESENT"} and b["side_role"]!=local_role,"R235 opposite branch");need(v["branch_label"]==b["side_role"] and v["source_partition_row_id"]==p["endpoint_graph_partition_row_id"],"R235 R248 branch binding");branch_requirement="eta_times_source_factor_STRICT_POSITIVE" if b["side_role"]=="EVENT_ABSENT" else "eta_times_source_factor_STRICT_NEGATIVE";interior_sign="STRICT_POSITIVE" if eta*inward>0 else "STRICT_NEGATIVE";key="R235_"+b["side_role"];census[key]+=1;authority={"kind":"R235_EXACT_ONE_SIDED_CARRIER_SIGN_EXHAUSTION","R235_partition_ref":{"row_id":p["endpoint_graph_partition_row_id"],"row_object_sha256":obj(p)},"fixed_endpoint_eta":eta,"active_factor":"9/25*t","active_factor_strict_t_derivative_sign":"STRICT_POSITIVE","zero_face":zero_face,"carrier_t_interval":[str(lo),str(hi)],"interior_eta_times_source_factor_sign":interior_sign,"blocked_branch_requirement":branch_requirement,"strict_branch_intersection_with_carrier":"EMPTY"}
  else:
   need(b["graph_class"]=="R235D_SOURCE_EXACT_FACE_FULL_BASE" and b["side_role"]=="source:NEGATIVE_TO_POSITIVE","R235D scope");bridge=bridges[d["theorem_basis"]["C4_bridge_ref"]["row_id"]];rec=bridge["semantic_reconstruction"];need(d["theorem_basis"]["C4_bridge_ref"]==ref(bridge,"bridge_row_id") and rec["complete_domain_partition_verified"] is True,"R235D C4 complete domain");target=rec["target_factor_fixed_sign"];source_interior="STRICT_POSITIVE" if inward>0 else "STRICT_NEGATIVE";need(target==source_interior,"R235D same-sign carrier");need(v["branch_label"]=="NEGATIVE_TO_POSITIVE" and v["positive_volume_proof_kind"]=="ROUND236_TWO_ENDPOINT_GRAPHS_NEGATIVE_TO_POSITIVE_OPEN_REGION","R235D R248 branch label");census["R235D_NEGATIVE_TO_POSITIVE"]+=1;authority={"kind":"R235D_COMPLETE_DOMAIN_ENDPOINT_SIGN_EXHAUSTION","C4_bridge_ref":ref(bridge,"bridge_row_id"),"complete_domain_partition_verified":True,"target_factor_fixed_sign":target,"source_factor":"9/25*t","source_factor_strict_t_derivative_sign":"STRICT_POSITIVE","zero_face":zero_face,"carrier_t_interval":[str(lo),str(hi)],"source_factor_interior_sign":source_interior,"blocked_branch_requirement":"source_STRICT_NEGATIVE_AND_target_STRICT_POSITIVE","strict_branch_intersection_with_complete_carrier":"EMPTY"}
  need((b["graph_id"],b["side_member_id"]) not in seen,"relation uniqueness");seen.add((b["graph_id"],b["side_member_id"]));cert={**authority,"R248_null_positive_box_not_used_as_geometry":True,"certificate_sha256":obj(authority)}
  core={"schema":ROW_SCHEMA,"row_id":PREFIX+":disposition:"+obj([b["row_id"],b["graph_id"],b["side_member_id"]]),"disposition_ordinal":len(out),"graph_id":b["graph_id"],"graph_class":b["graph_class"],"side_member_id":b["side_member_id"],"side_role":b["side_role"],"C11_blocked_ref":ref(b),"C11_disposition_ref":ref(d),"C10_exact_support_ref":ref(s),"R248_side_ref":{"row_id":v["wall_bulk_node_id"],"row_sha256":v["row_sha256"]},"empty_carrier_certificate":cert,"disposition":"MECHANICAL_GRAPH_SIDE_JOIN_INVALID__STRICT_BRANCH_EMPTY_ON_EXACT_CARRIER","relation_nonincidence_disposition_credit":1,"local_graph_side_physical_incidence_proved":False,"one_sided_trace_required":False,"representation_pullback_required":False,"DSU_edge_or_union_authorized":False,"formal_credit":ZERO};out.append(close(core))
 need(len(out)==len(seen)==168 and census=={"R235_EVENT_ABSENT":32,"R235_EVENT_PRESENT":120,"R235D_NEGATIVE_TO_POSITIVE":16},"output census")
 wire,plain=gzip_rows(out);desc={"filename":LEDGER,"compression":"gzip-level9-mtime-zero","row_count":168,"compressed_size":len(wire),"compressed_sha256":hashlib.sha256(wire).hexdigest(),"uncompressed_size":len(plain),"uncompressed_sha256":hashlib.sha256(plain).hexdigest(),"ordered_rows_sha256":obj(out)};source=Path(__file__).read_bytes();body={"schema":SCHEMA,"status":"PASS_168_BLOCKED_RELATIONS_DISPOSED_AS_EMPTY_ON_EXACT_CARRIER__ZERO_INCIDENCE_EDGE_AND_DOWNSTREAM_CREDIT","producer_source":{"filename":Path(__file__).name,"size":len(source),"sha256":hashlib.sha256(source).hexdigest()},"source_pins":[p.__dict__ for p in PINS],"census":{**census,"blocked_input_rows":168,"empty_carrier_nonincidence_dispositions":168},"scoped_credit":{"relation_nonincidence_disposition":168},"formal_credit":ZERO,"corrected_physical_relation_census":{"prior_mechanical_physical_denominator":15392,"invalid_graph_side_relations_removed":168,"corrected_physical_denominator":15224,"valid_graph_to_sheet_relations":5264,"valid_graph_to_side_relations":9960,"remaining_blocked_graph_side_relations":0},"strict_nonpromotion":{"new_physical_incidence_credit":0,"new_one_sided_trace_credit":0,"new_DSU_edge_or_union":0,"representation_pullback_proved":False,"normalized_support_sealed":False,"CM2":"NO-GO_FOR_CLAIM"},"disposition_ledger":desc,"required_next":"PROVE_5264_GRAPH_TO_SHEET_SET_EQUALITIES_THEN_REBUILD_15224_VALID_RELATION_PULLBACKS"};return {**body,"result_sha256":obj(body)},wire
def write_once(d:Path,n:str,b:bytes)->None:
 p=d/n;need(not p.exists(),"no clobber:"+n);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  off=0
  while off<len(b):off+=os.write(fd,b[off:])
  os.fsync(fd)
 finally:os.close(fd)
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir");ap.add_argument("--publish",action="store_true");a=ap.parse_args();need((a.candidate_dir is not None)!=a.publish,"one output mode");result,wire=build();d=ROOT if a.publish else Path(a.candidate_dir).resolve()
 if not a.publish:d.mkdir(mode=0o700,parents=False,exist_ok=False)
 write_once(d,LEDGER,wire);write_once(d,RESULT,canonical(result));print(json.dumps({"status":result["status"],"result_sha256":result["result_sha256"]},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
