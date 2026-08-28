#!/usr/bin/env python3
"""Independent 640-bit fixed-grid verifier for Round109 (no producer import)."""
from __future__ import annotations
import argparse, copy, hashlib, json, multiprocessing as mp, os, sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb, ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round89_rank3_projective_gap_closure_cert as round89
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet

HERE=Path(__file__).resolve().parent
CERT=HERE/"cm2-round109-rank3-registered-arc-immutable-whole-tube-reaudit-2026-07-22.json"
R99=HERE/"cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
R102=HERE/"cm2-round102-rank3-corrected-face-quotient-2026-07-22.json"
PRODUCER=HERE/"cm2_round109_rank3_registered_arc_immutable_whole_tube_reaudit.py"
SCHEMA="cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1"
VSCHEMA="cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit-verification.v1"
PINS={CERT.name:"fa5231f91f71da8014f9ca606702e3a59499adf78ce86ce09954bb424dae540e",R99.name:"e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",R102.name:"85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",PRODUCER.name:"d24f6cf4e4fd67cefa0ebb1e3cc3170a921c861e4a1d3dfad977e8a2ab23b3e4"}
UPSTREAM={"cm2-round87-rank3-port-event-continuation-2026-07-22.json":"f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b","cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json":"e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e","cm2-round102-rank3-corrected-face-quotient-2026-07-22.json":"85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb","cm2_round87_rank3_port_event_continuation_cert.py":"71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834","cm2_round89_rank3_projective_gap_closure_cert.py":"6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf","cm2_round99_rank3_registered_port_candidate_audit.py":"bbacd4407aa026850d9a410b61e841bd6e799e67ba16549e4a478a9fcfb7a26f","cm2_round100_rank3_immutable_interior_gap_closure.py":"be5c7d9413f03810210eea8b8d2eb37a9256886f0a339cdcd4ddcf1d32c1e224"}
RKEYS={"precision_bits","input_corrected_face_count","input_registered_physical_arc_link_count","certified_registered_arc_whole_tube_count","remaining_unaudited_registered_arc_count","whole_tube_strip_count","complete_immutable_candidate_tuple_replay_count","complete_translated_candidate_equation_count","complete_nontarget_competitor_equation_count","strip_count_histogram","dependent_collar_depth_histogram","implicit_graph_axis_histogram","registered_arc_rows","registered_arc_rows_sha256","strict_scope","strict_nonclaims","upstream_and_executable_pins"}
ROWKEYS={"registered_arc_reaudit_id","face_id","link_rank","left_registered_port_id","right_registered_port_id","physical_root_component_id","source_core_index","second_selected_target_id","third_candidate_id","signed_transverse_tangency_factor_sign","strip_count","dependent_collar_depth","implicit_graph_axis","certified_tube_boxes_sha256","strip_sign_rows_sha256","whole_chain_two_collision_status","whole_chain_third_event_status","complete_translated_candidate_count_histogram","whole_chain_competitor_rows_sha256","immutable_candidate_table_materialization","tangent_face_whole_tube_complete_candidate_chain_certified","transverse_D_sign_side_cell_asserted","homogeneity_child_asserted","Gate5_field_installed"}
CORES:tuple[Any,...]=(); EVENTS={}; LINKS={}; PAIRS={}

def fsha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d: raise ValueError("duplicate key")
  d[k]=v
 return d
def nonfinite(x): raise ValueError(x)
def loadraw(raw):
 d=json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite)
 if set(d)!={"schema","result","result_sha256"} or d["schema"]!=SCHEMA or d["result_sha256"]!=digest(d["result"]): raise RuntimeError("bad envelope")
 if set(d["result"])!=RKEYS or any(set(r)!=ROWKEYS for r in d["result"]["registered_arc_rows"]): raise RuntimeError("bad schema")
 return d
def closed(p,s):
 d=json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=nonfinite)
 if set(d)!={"schema","result","result_sha256"} or d["schema"]!=s or d["result_sha256"]!=digest(d["result"]): raise RuntimeError("bad upstream")
 return d["result"]
def init(bits):
 global CORES
 ctx.prec=bits; CORES=tuple(core_cert.physical_cores())
def bkey(r): return (r["source_core_index"],r["second_selected_target_id"],r["third_candidate_id"],r["event_equation_evidence"]["signed_transverse_tangency_factor_sign"])
def rect(r):
 lo,hi=map(Q,r["isolated_root_bracket"]); fixed=Q(r["fixed_coordinate"])
 return (fixed,fixed,lo,hi) if r["boundary_axis"]=="p" else (lo,hi,fixed,fixed)

def event(state,second,target):
 x,y=time3.time2_cert.target_center(target,state["s"]); dx=x-state["contact_x"]; dy=y-state["contact_y"]; ux,uy=state["outgoing_x"],state["outgoing_y"]
 flight=ux*dx+uy*dy; transverse=-uy*dx+ux*dy
 if strict_sign(flight)!=1 or strict_sign(transverse)==0 or strict_sign(arb(1)+ux)!=1 or not bool(flight<aq(time3.time2_cert.step1.first_hit.TAU_MAX)): raise RuntimeError("tangent geometry")
 ids=tuple(time3.time2_cert.translated_candidate_ids(second,state["chart"]))
 if len(ids)!=57 or len(ids)!=len(set(ids)) or target not in ids: raise RuntimeError("candidate tuple")
 rows=[]; future=[]
 for cid in ids:
  if cid==target: continue
  c=time3.time2_cert.candidate_root(state["contact_x"],state["contact_y"],state["outgoing_x"],state["outgoing_y"],state["s"],cid); cls=c["classification"]
  if cls=="no_real_intersection": rel="NO_REAL_INTERSECTION"
  elif cls=="intersection_strictly_behind": rel="INTERSECTION_STRICTLY_BEHIND"
  elif cls=="strict_future_near_root":
   near=c["near"]
   if bool(near<flight): rel="STRICTLY_BEFORE_TANGENT_TARGET"
   elif bool(flight<near): rel="STRICTLY_AFTER_TANGENT_TARGET"
   else: raise RuntimeError("root order")
   future.append((cid,near))
  else: raise RuntimeError("root class")
  rows.append({"candidate_id":cid,"candidate_root_classification":cls,"relation_to_tangent_target_flight":rel})
 rows.sort(key=lambda x:x["candidate_id"])
 if any(x["relation_to_tangent_target_flight"]=="STRICTLY_BEFORE_TANGENT_TARGET" for x in rows): raise RuntimeError("earlier competitor")
 winners=[cid for cid,n in future if all(cid==oid or bool(n<on) for oid,on in future)]
 if future and len(winners)!=1: raise RuntimeError("winner")
 return strict_sign(transverse),digest(rows)

def rebuild_row(row):
 left=EVENTS[row["left_registered_port_id"]]; right=EVENTS[row["right_registered_port_id"]]
 branch=bkey(left)
 if bkey(right)!=branch: raise RuntimeError("cross-branch endpoints")
 source=CORES[branch[0]]; a,b=rect(left),rect(right)
 tc=((a[0]+a[1])/2,(b[0]+b[1])/2); pc=((a[2]+a[3])/2,(b[2]+b[3])/2)
 use_t=abs(tc[1]-tc[0])>=abs(pc[1]-pc[0]); axis="p_as_function_of_t" if use_t else "t_as_function_of_p"
 parameter=tc if use_t else pc; dependent=pc if use_t else tc
 width=(source.p1-source.p0) if use_t else (source.t1-source.t0)
 subdivisions=row["strip_count"]; collar=width/Q(2**row["dependent_collar_depth"])
 boxes=[]; signs=[]; competitor_digests=[]; transverse_signs=[]
 for index in range(subdivisions):
  u0,u1=Q(index,subdivisions),Q(index+1,subdivisions)
  x0=parameter[0]+u0*(parameter[1]-parameter[0]); x1=parameter[0]+u1*(parameter[1]-parameter[0])
  y0=dependent[0]+u0*(dependent[1]-dependent[0]); y1=dependent[0]+u1*(dependent[1]-dependent[0])
  xl,xu=sorted((x0,x1)); yl,yu=min(y0,y1)-collar,max(y0,y1)+collar
  box=(xl,xu,max(source.p0,yl),min(source.p1,yu)) if use_t else (max(source.t0,yl),min(source.t1,yu),xl,xu)
  jet=third_tangency_jet(source,branch[1],branch[2],*box); ts,ps=map(strict_sign,jet.gradient[:2]); derivative=ps if use_t else ts
  if not derivative: raise RuntimeError("IFT derivative")
  if use_t:
   lo=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[1],box[2],box[2]).value)
   hi=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[1],box[3],box[3]).value)
  else:
   lo=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[0],box[2],box[3]).value)
   hi=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[1],box[1],box[2],box[3]).value)
  if lo*hi!=-1: raise RuntimeError("IFT boundary signs")
  atom=step1.Atom(branch[0],source,*box,Q(0),Q(0),f"round109-verify:{subdivisions}:{index}")
  classification,_,destination,state1,owner2=time3.homogeneity_cert.classify_with_geometry(atom,CORES)
  if classification!="SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None or owner2["selected_target_id"]!=branch[1]: raise RuntimeError("two-collision chain")
  state2=time3.second_outgoing_state(atom,state1,owner2)
  if state2 is None: raise RuntimeError("second outgoing state")
  transverse,competitors=event(state2,branch[1],branch[2])
  boxes.append(box); signs.append((derivative,lo,hi)); transverse_signs.append(transverse); competitor_digests.append(competitors)
 if set(transverse_signs)!={branch[3]}: raise RuntimeError("transverse sign changed")
 link=LINKS[(row["face_id"],row["link_rank"])]
 identity={"face_id":link["face_id"],"link_rank":link["link_rank"],"left_registered_port_id":link["left_registered_port_id"],"right_registered_port_id":link["right_registered_port_id"],"physical_root_component_id":link["evidence_id"]}
 return {
  "registered_arc_reaudit_id":"physical-s0-rank3-registered-arc-immutable-reaudit:"+digest(identity),**identity,
  "source_core_index":branch[0],"second_selected_target_id":branch[1],"third_candidate_id":branch[2],
  "signed_transverse_tangency_factor_sign":branch[3],"strip_count":subdivisions,
  "dependent_collar_depth":row["dependent_collar_depth"],"implicit_graph_axis":axis,
  "certified_tube_boxes_sha256":digest([list(map(str,x)) for x in boxes]),"strip_sign_rows_sha256":digest(signs),
  "whole_chain_two_collision_status":"SURVIVE_THROUGH_2_INNER","whole_chain_third_event_status":"PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION",
  "complete_translated_candidate_count_histogram":{"57":subdivisions},"whole_chain_competitor_rows_sha256":digest(competitor_digests),
  "immutable_candidate_table_materialization":"TUPLE_BEFORE_MEMBERSHIP_OR_ITERATION",
  "tangent_face_whole_tube_complete_candidate_chain_certified":True,"transverse_D_sign_side_cell_asserted":False,
  "homogeneity_child_asserted":False,"Gate5_field_installed":False,
 }

def worker(row):
 return rebuild_row(row)

def validate(document,expected=None):
 result=document["result"]
 if result["registered_arc_rows_sha256"]!=digest(result["registered_arc_rows"]): raise RuntimeError("row digest")
 if result["upstream_and_executable_pins"]!=UPSTREAM: raise RuntimeError("upstream pin ledger")
 rows=result["registered_arc_rows"]
 if len(rows)!=52 or result["certified_registered_arc_whole_tube_count"]!=52 or result["remaining_unaudited_registered_arc_count"]!=0: raise RuntimeError("arc counts")
 if sum(r["strip_count"] for r in rows)!=41984 or result["whole_tube_strip_count"]!=41984: raise RuntimeError("strip counts")
 if result["complete_immutable_candidate_tuple_replay_count"]!=41984 or result["complete_translated_candidate_equation_count"]!=2393088 or result["complete_nontarget_competitor_equation_count"]!=2351104: raise RuntimeError("candidate counts")
 if Counter(r["strip_count"] for r in rows)!=Counter({1024:36,512:8,128:8}): raise RuntimeError("strip histogram")
 if any(r["transverse_D_sign_side_cell_asserted"] or r["homogeneity_child_asserted"] or r["Gate5_field_installed"] for r in rows): raise RuntimeError("illegal promotion")
 if expected is not None and rows!=expected: raise RuntimeError("640-bit reconstruction mismatch")
 return digest(rows)

def mutations(document,expected):
 tests=[]
 for field,value in [("Gate5_field_installed",True),("homogeneity_child_asserted",True),("transverse_D_sign_side_cell_asserted",True),("strip_count",127),("third_candidate_id","G[999,999]")]:
  item=copy.deepcopy(document); item["result"]["registered_arc_rows"][0][field]=value; tests.append(item)
 item=copy.deepcopy(document); item["result"]["complete_nontarget_competitor_equation_count"]-=1; tests.append(item)
 rejected=0
 for item in tests:
  item["result"]["registered_arc_rows_sha256"]=digest(item["result"]["registered_arc_rows"]); item["result_sha256"]=digest(item["result"])
  try: validate(item,expected)
  except RuntimeError: rejected+=1
 return rejected

def json_attacks(raw):
 attacks=[raw.rstrip()[:-1]+',"schema":"duplicate"}',raw.replace('"precision_bits": 512','"precision_bits": NaN',1),raw.rstrip()[:-1]+',"unknown":0}']
 rejected=0
 for attack in attacks:
  try: loadraw(attack)
  except (ValueError,RuntimeError): rejected+=1
 return rejected

def main():
 global EVENTS,LINKS,PAIRS
 raw=CERT.read_text(); document=loadraw(raw)
 for name,expected in PINS.items():
  if fsha(HERE/name)!=expected: raise RuntimeError(f"pin mismatch: {name}")
 for name,expected in UPSTREAM.items():
  if fsha(HERE/name)!=expected: raise RuntimeError(f"upstream pin mismatch: {name}")
 r99=closed(R99,"cm2.round99.rank3-registered-port-candidate-audit.v1")
 r102=closed(R102,"cm2.round102.rank3-corrected-face-quotient.v1")
 events,pairs_rows=round89.load(); EVENTS={r["registered_port_id"]:r for r in events}; PAIRS={frozenset(r["registered_elementary_arc_endpoint_port_ids"]):r for r in pairs_rows}
 LINKS={(r["face_id"],r["link_rank"]):r for r in r102["interior_link_rows"] if r["link_type"]=="REGISTERED_PHYSICAL_ARC"}
 corrected=set(r99["corrected_locally_physical_registered_port_ids"])
 if len(LINKS)!=52 or any({r["left_registered_port_id"],r["right_registered_port_id"]}-corrected for r in LINKS.values()): raise RuntimeError("corrected link census")
 init(640)
 context=mp.get_context("fork")
 with context.Pool(min(8,os.cpu_count() or 1),initializer=init,initargs=(640,)) as pool:
  rebuilt=list(pool.imap(worker,document["result"]["registered_arc_rows"]))
 projection=validate(document,rebuilt); semantic=mutations(document,rebuilt); attacks=json_attacks(raw)
 if semantic!=6 or attacks!=3: raise RuntimeError("attack accounting")
 result={"verification_precision_bits":640,"producer_module_imported":False,"fixed_grid_reconstructed_arc_count":52,
  "fixed_grid_reconstructed_strip_count":41984,"immutable_candidate_tuple_replay_count":41984,
  "translated_candidate_equation_replay_count":2393088,"semantic_projection_sha256":projection,
  "hostile_semantic_mutations_rejected":"6/6","strict_json_attacks_rejected":"3/3",
  "illegal_side_cell_or_operator_promotion_detected":False,"verdict":"VERIFIED_REGISTERED_ARC_IMMUTABLE_WHOLE_TUBE_REAUDIT"}
 output={"schema":VSCHEMA,"result":result,"result_sha256":digest(result)}
 rendered=json.dumps(output,sort_keys=True,indent=2)+"\n"
 args=argparse.ArgumentParser(); args.add_argument("--output",type=Path); ns=args.parse_args()
 (ns.output.write_text(rendered) if ns.output else sys.stdout.write(rendered)); return 0

if __name__=="__main__": raise SystemExit(main())
