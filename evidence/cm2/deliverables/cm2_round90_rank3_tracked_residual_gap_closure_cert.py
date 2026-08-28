#!/usr/bin/env python3
"""Interval-root tracking closure of the eight Round89 rank-three gap residuals."""
from __future__ import annotations
import hashlib,json,sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round80_time3_dihedral_quotient_generator as dihedral
from cm2_round79_tangency_intersection_generator import aq,digest,strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet

HERE=Path(__file__).resolve().parent
FRONTIER=HERE/"cm2-round89-rank3-projective-gap-closure-2026-07-22.json"
SYMMETRY=HERE/"cm2-round80-time3-dihedral-quotient-2026-07-21.json"
PINS={FRONTIER.name:"189044e2b366b9a1620375f2a1eeaf163d2eff0a8996ccf76869fa2294a34a08",
      "cm2_round89_rank3_projective_gap_closure_cert.py":"6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf",
      "cm2_round80_time3_dihedral_quotient_generator.py":"0c1e1715c00cb43ee7210b4d28488027373b8f2dc175cf000dddc7d6f7729b89",
      SYMMETRY.name:"0f08fcacd3085024f396a7d657e3e3f4410018d51d7656d5572c39aa8667c712"}
SCHEMA="cm2.round90.rank3-tracked-residual-gap-closure.v1"
PRECISION_BITS=512

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def tracked_gap(left:dict[str,Any],right:dict[str,Any],cores:tuple[Any,...])->dict[str,Any]:
    branch=round89.key(left)
    if round89.key(right)!=branch:raise RuntimeError("cross-key residual")
    source=cores[branch[0]];a,b=round89.root_rect(left),round89.root_rect(right)
    tc=((a[0]+a[1])/2,(b[0]+b[1])/2);pc=((a[2]+a[3])/2,(b[2]+b[3])/2)
    use_t=abs(tc[1]-tc[0])>=abs(pc[1]-pc[0]);axis="p_as_function_of_t" if use_t else "t_as_function_of_p"
    parameter=tc if use_t else pc;dependent=pc if use_t else tc
    dep_lo,dep_hi=(source.p0,source.p1) if use_t else (source.t0,source.t1)
    dep_width=dep_hi-dep_lo
    def value(x:Q,y:Q):
        return (third_tangency_jet(source,branch[1],branch[2],x,x,y,y).value if use_t
                else third_tangency_jet(source,branch[1],branch[2],y,y,x,x).value)
    last="NO_ATTEMPT"
    for subdivisions in (64,128,256,512,1024,2048):
        nodes=[];ok=True
        for index in range(subdivisions+1):
            u=Q(index,subdivisions);x=parameter[0]+u*(parameter[1]-parameter[0]);pred=dependent[0]+u*(dependent[1]-dependent[0]);bracket=None
            for depth in range(4,49,4):
                radius=dep_width/Q(2**depth);lo=max(dep_lo,pred-radius);hi=min(dep_hi,pred+radius);ls,hs=strict_sign(value(x,lo)),strict_sign(value(x,hi))
                if ls*hs!=-1:continue
                for _ in range(48):
                    mid=(lo+hi)/2;ms=strict_sign(value(x,mid))
                    if not ms:break
                    if ms==ls:lo,ls=mid,ms
                    else:hi,hs=mid,ms
                else:bracket=(x,lo,hi);break
            if bracket is None:last="NODE_ROOT_ISOLATION";ok=False;break
            nodes.append(bracket)
        if not ok:continue
        collar_depth=subdivisions.bit_length()-1
        boxes=[];signs=[];events=[];collar=dep_width/Q(2**collar_depth)
        for index in range(subdivisions):
            x0,y00,y01=nodes[index];x1,y10,y11=nodes[index+1];yl,yu=min(y00,y10)-collar,max(y01,y11)+collar
            box=(min(x0,x1),max(x0,x1),max(dep_lo,yl),min(dep_hi,yu)) if use_t else (max(dep_lo,yl),min(dep_hi,yu),min(x0,x1),max(x0,x1))
            jet=third_tangency_jet(source,branch[1],branch[2],*box);ts,ps=map(strict_sign,jet.gradient[:2]);derivative=ps if use_t else ts
            if not derivative:last="IFT_DERIVATIVE";ok=False;break
            if use_t:
                tm=(box[0]+box[1])/2;tr=(box[1]-box[0])/2
                def face(p):
                    point=third_tangency_jet(source,branch[1],branch[2],tm,tm,p,p).value
                    gradient=third_tangency_jet(source,branch[1],branch[2],box[0],box[1],p,p).gradient[0]
                    return point+gradient*__import__('flint').arb(0,aq(tr).upper())
                flo,fhi=face(box[2]),face(box[3]);lo,hi=strict_sign(flo),strict_sign(fhi)
            else:
                pm=(box[2]+box[3])/2;pr=(box[3]-box[2])/2
                def face(t):
                    point=third_tangency_jet(source,branch[1],branch[2],t,t,pm,pm).value
                    gradient=third_tangency_jet(source,branch[1],branch[2],t,t,box[2],box[3]).gradient[1]
                    return point+gradient*__import__('flint').arb(0,aq(pr).upper())
                flo,fhi=face(box[0]),face(box[1]);lo,hi=strict_sign(flo),strict_sign(fhi)
            if lo*hi!=-1:last="IFT_BOUNDARY_SIGNS";ok=False;break
            try:
                atom=step1.Atom(branch[0],source,*box,Q(0),Q(0),f"round90:{subdivisions}:{index}")
                classification,_,destination,state1,owner2=time3.homogeneity_cert.classify_with_geometry(atom,cores)
                if classification!="SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None or owner2["selected_target_id"]!=branch[1]:last="TWO_COLLISION_OWNER";ok=False;break
                state2=time3.second_outgoing_state(atom,state1,owner2)
                if state2 is None:last="SECOND_OUTGOING_STATE";ok=False;break
                status,evidence=round87.physical_type(state2,branch[1],branch[2])
                if status!="PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or evidence["signed_transverse_tangency_factor_sign"]!=branch[3]:last=status;ok=False;break
            except (ValueError,ZeroDivisionError,RuntimeError) as exc:last=type(exc).__name__;ok=False;break
            boxes.append(list(map(str,box)));signs.append((derivative,lo,hi));events.append(evidence)
        if ok:
            return {"left_registered_port_id":left["registered_port_id"],"right_registered_port_id":right["registered_port_id"],
                    "source_core_index":branch[0],"second_selected_target_id":branch[1],"third_candidate_id":branch[2],
                    "signed_transverse_tangency_factor_sign":branch[3],"implicit_graph_axis":axis,"strip_count":subdivisions,
                    "node_root_bisection_depth":48,"dependent_collar_depth":collar_depth,"tracked_boxes_sha256":digest(boxes),
                    "strict_sign_rows_sha256":digest(signs),"competitor_rows_sha256":digest([e["competitor_rows_sha256"] for e in events]),
                    "whole_chain_status":"PHYSICAL_NEXT_TANGENCY__TRACKED_IFT_CHAIN"}
    raise RuntimeError(f"tracked residual unresolved: {last}")

def build(precision_bits:int=PRECISION_BITS)->dict[str,Any]:
    ctx.prec=precision_bits
    for name,expected in PINS.items():
        if sha(HERE/name)!=expected:raise RuntimeError(f"pin mismatch: {name}")
    frontier=json.loads(FRONTIER.read_text());symmetry=json.loads(SYMMETRY.read_text());event_rows,pair_rows=round89.load()
    if symmetry["result"]["symmetry_group"]!="stratified exact action: D4 on 16 cross-obstacle cores; diagonal C2 on 8 radial cores" or not symmetry["result"]["all_component_grid_sets_mapped_exactly"]:
        raise RuntimeError("Round80 exact D4 theorem mismatch")
    physical={r["registered_port_id"]:r for r in event_rows if r["port_is_locally_physical_third_tangency"]}
    by_branch={}
    for port_id,row in physical.items():by_branch.setdefault(round89.key(row),[]).append(port_id)
    for ids in by_branch.values():ids.sort(key=lambda p:float(round89.qball(physical[p]).mid()))
    source_caps=[]
    for pair in pair_rows:
        a,b=pair["registered_elementary_arc_endpoint_port_ids"];pa,pb=a in physical,b in physical
        if pa==pb:continue
        port=a if pa else b;source_port=b if pa else a;branch=round89.key(physical[port]);order=by_branch[branch];rank=order.index(port)
        side="LEFT_PROJECTIVE_END" if rank==0 else "RIGHT_PROJECTIVE_END" if rank==len(order)-1 else "NONEXTREME"
        source_caps.append({"registered_source_port_id":source_port,"mated_physical_port_id":port,"branch_key":list(branch),"projective_end":side})
    if len(source_caps)!=47 or any(r["projective_end"]=="NONEXTREME" for r in source_caps):raise RuntimeError("source endpoint is not a projective cap")
    cores=core_cert.physical_cores();round87.WORK_CORES=cores
    residuals=frontier["result"]["unresolved_gap_rows"]
    representative=residuals[0]
    representative_row=tracked_gap(physical[representative["left_registered_port_id"]],physical[representative["right_registered_port_id"]],cores)
    source_action=dihedral.core_action();base=(1,"G[0,0]","W[1,-1]",1)
    expected={(round89.key(physical[r["left_registered_port_id"]])) for r in residuals}
    orbit=set()
    action_rows=[]
    for name,matrix in dihedral.MATRICES.items():
        target_source,_t_sign,p_sign=source_action[(base[0],name)]
        target_second=dihedral.transform_obstacle(base[1],"G",matrix)
        target_third=dihedral.transform_obstacle(base[2],"G",matrix)
        transformed=(target_source,target_second,target_third,base[3]*p_sign)
        orbit.add(transformed)
        action_rows.append({"symmetry":name,"target_source_core_index":target_source,"target_second_id":target_second,"target_third_id":target_third,"target_signed_transverse_sign":base[3]*p_sign})
    if orbit!=expected:raise RuntimeError("eight residuals are not the exact D4 orbit")
    rows=[]
    by_key={round89.key(physical[r["left_registered_port_id"]]):r for r in residuals}
    for action in sorted(action_rows,key=lambda r:r["symmetry"]):
        target=(action["target_source_core_index"],action["target_second_id"],action["target_third_id"],action["target_signed_transverse_sign"])
        residual=by_key[target]
        rows.append({"left_registered_port_id":residual["left_registered_port_id"],"right_registered_port_id":residual["right_registered_port_id"],
                     "D4_symmetry_from_representative":action["symmetry"],"target_branch_key":list(target),
                     "representative_tracked_boxes_sha256":representative_row["tracked_boxes_sha256"],
                     "whole_chain_status":"PHYSICAL_NEXT_TANGENCY__D4_EXPANDED_TRACKED_IFT_CHAIN"})
    result={"precision_bits":precision_bits,"input_round89_residual_gap_count":8,"direct_tracked_representative_gap_count":1,
            "D4_expanded_tracked_gap_closure_count":len(rows),
            "remaining_unresolved_interior_projective_gap_count":8-len(rows),
            "representative_strip_count":representative_row["strip_count"],"D4_action_count":len(action_rows),
            "representative_closure_row":representative_row,"D4_action_rows":action_rows,"D4_action_rows_sha256":digest(action_rows),
            "closure_rows":rows,"closure_rows_sha256":digest(rows),
            "combined_round89_round90_certified_interior_gap_count":432+len(rows),"combined_interior_gap_count":440,
            "round89_conservative_exterior_ray_count":112,"source_capped_projective_end_count":len(source_caps),
            "source_cap_rows":source_caps,"source_cap_rows_sha256":digest(source_caps),
            "remaining_exterior_projective_ray_count":112-len(source_caps),
            "strict_scope":"tracked interval-root closure of the eight Round89 IFT-envelope residual gaps",
            "strict_nonclaims":["the 112 exterior rays remain open","interior closure does not itself create complete physical faces or RN rows"],"upstream_pins":PINS}
    if len(rows)!=8:raise RuntimeError("Round90 residual closure incomplete")
    result=json.loads(json.dumps(result,sort_keys=True))
    return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
def main():json.dump(build(),sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main())
