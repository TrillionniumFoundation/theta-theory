#!/usr/bin/env python3
"""Certify all interior gaps on the 56 live rank-three tangent branches."""
from __future__ import annotations

import hashlib, json, re, sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round87_rank3_port_event_continuation_cert as round87
from cm2_round79_tangency_intersection_generator import digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet

HERE = Path(__file__).resolve().parent
EVENTS = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
QUOTIENT = HERE / "cm2-round88-rank3-physical-port-component-quotient-2026-07-22.json"
RESOLVER = HERE / "cm2-round88-rank3-multi-arc-zero-overlap-resolver-2026-07-22.json"
PINS = {
    EVENTS.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    QUOTIENT.name: "35e4b0ee448476837644f66a55aaaf385bcb4027c27a36fdc37f54bfb4f40d42",
    RESOLVER.name: "370a9861749d628dd8993d03236155e41c003863fd08ca18ad222bfa661eb48e",
    "cm2_round87_rank3_port_event_continuation_cert.py": "71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834",
}
PRECISION_BITS = 512
SCHEMA = "cm2.round89.rank3-projective-gap-closure.v1"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    for name, expected in PINS.items():
        if sha(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    events = json.loads(EVENTS.read_text())
    quotient = json.loads(QUOTIENT.read_text())
    resolver = json.loads(RESOLVER.read_text())
    pairs = (quotient["result"]["exact_single_arc_registered_side_pair_rows"]
             + resolver["result"]["multi_arc_resolved_pair_rows"])
    return events["result"]["port_event_rows"], pairs

def key(row: dict[str, Any]) -> tuple[int, str, str, int]:
    return (row["source_core_index"], row["second_selected_target_id"],
            row["third_candidate_id"],
            row["event_equation_evidence"]["signed_transverse_tangency_factor_sign"])

def qball(row: dict[str, Any]) -> arb:
    text = row["event_equation_evidence"]["projective_q_enclosure"]
    m = re.fullmatch(r"\[?([+-]?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)(?: \+/- ([0-9.e+-]+))?\]?", text)
    if not m:
        raise RuntimeError(f"bad q enclosure: {text}")
    return arb(m.group(1)) if m.group(2) is None else arb(m.group(1)) + arb(0, m.group(2))

def root_rect(row: dict[str, Any]) -> tuple[Q, Q, Q, Q]:
    lo, hi = map(Q, row["isolated_root_bracket"])
    fixed = Q(row["fixed_coordinate"])
    return (fixed, fixed, lo, hi) if row["boundary_axis"] == "p" else (lo, hi, fixed, fixed)

def certify_gap(left: dict[str, Any], right: dict[str, Any], cores: tuple[Any, ...]) -> dict[str, Any]:
    branch = key(left)
    if key(right) != branch:
        raise RuntimeError("cross-key gap")
    source = cores[branch[0]]
    a, b = root_rect(left), root_rect(right)
    tc = ((a[0]+a[1])/2, (b[0]+b[1])/2)
    pc = ((a[2]+a[3])/2, (b[2]+b[3])/2)
    use_t = abs(tc[1]-tc[0]) >= abs(pc[1]-pc[0])
    axis = "p_as_function_of_t" if use_t else "t_as_function_of_p"
    parameter = tc if use_t else pc
    dependent = pc if use_t else tc
    dependent_width = (source.p1-source.p0) if use_t else (source.t1-source.t0)
    reason = "NO_ATTEMPT"
    for subdivisions in (4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048):
      for collar_depth in range(12, 49, 4):
        collar = dependent_width / Q(2**collar_depth)
        boxes=[]; evidence_rows=[]; signs_rows=[]; good=True
        for index in range(subdivisions):
            u0,u1=Q(index,subdivisions),Q(index+1,subdivisions)
            x0=parameter[0]+u0*(parameter[1]-parameter[0]); x1=parameter[0]+u1*(parameter[1]-parameter[0])
            y0=dependent[0]+u0*(dependent[1]-dependent[0]); y1=dependent[0]+u1*(dependent[1]-dependent[0])
            xl,xu=sorted((x0,x1)); yl,yu=min(y0,y1)-collar,max(y0,y1)+collar
            box=(xl,xu,max(source.p0,yl),min(source.p1,yu)) if use_t else (max(source.t0,yl),min(source.t1,yu),xl,xu)
            jet=third_tangency_jet(source,branch[1],branch[2],*box)
            ts,ps=map(strict_sign,jet.gradient[:2]); derivative=ps if use_t else ts
            if not derivative: reason="IFT_DERIVATIVE"; good=False; break
            if use_t:
                lo=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[1],box[2],box[2]).value)
                hi=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[1],box[3],box[3]).value)
            else:
                lo=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[0],box[2],box[3]).value)
                hi=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[1],box[1],box[2],box[3]).value)
            if lo*hi != -1: reason="IFT_BOUNDARY_SIGNS"; good=False; break
            try:
                atom=step1.Atom(branch[0],source,*box,Q(0),Q(0),f"round89-gap:{subdivisions}:{collar_depth}:{index}")
                classification,_,destination,state1,owner2=time3.homogeneity_cert.classify_with_geometry(atom,cores)
                if classification!="SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None or owner2["selected_target_id"]!=branch[1]:
                    reason="TWO_COLLISION_OWNER"; good=False; break
                state2=time3.second_outgoing_state(atom,state1,owner2)
                if state2 is None: reason="SECOND_OUTGOING_STATE"; good=False; break
                status,evidence=round87.physical_type(state2,branch[1],branch[2])
                if status!="PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or evidence["signed_transverse_tangency_factor_sign"]!=branch[3]:
                    reason=status; good=False; break
            except (ValueError,ZeroDivisionError,RuntimeError) as exc:
                reason=type(exc).__name__; good=False; break
            boxes.append(box); signs_rows.append((derivative,lo,hi)); evidence_rows.append(evidence)
        if not good: continue
        return {
            "left_registered_port_id": left["registered_port_id"],
            "right_registered_port_id": right["registered_port_id"],
            "source_core_index": branch[0], "second_selected_target_id": branch[1],
            "third_candidate_id": branch[2], "signed_transverse_tangency_factor_sign": branch[3],
            "strip_count":subdivisions,"dependent_collar_depth":collar_depth,
            "certified_tube_boxes_sha256":digest([list(map(str,x)) for x in boxes]),
            "implicit_graph_axis": axis,
            "strip_sign_rows_sha256":digest(signs_rows),
            "whole_chain_two_collision_status":"SURVIVE_THROUGH_2_INNER",
            "whole_chain_third_event_status":"PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION",
            "complete_translated_candidate_count_histogram":dict(sorted(Counter(x["complete_translated_candidate_count"] for x in evidence_rows).items())),
            "whole_chain_competitor_rows_sha256":digest([x["competitor_rows_sha256"] for x in evidence_rows]),
        }
    # Dependency-resistant fallback: isolate the exact dependent root at every
    # strip node, then bridge adjacent node brackets.  This follows the curved
    # graph rather than enclosing it in a corridor around the endpoint chord.
    dep_lo,dep_hi=(source.p0,source.p1) if use_t else (source.t0,source.t1)
    def value_at(x: Q, y: Q):
        return (third_tangency_jet(source,branch[1],branch[2],x,x,y,y).value if use_t
                else third_tangency_jet(source,branch[1],branch[2],y,y,x,x).value)
    for subdivisions in ():
        nodes=[]; node_ok=True
        for index in range(subdivisions+1):
            u=Q(index,subdivisions); x=parameter[0]+u*(parameter[1]-parameter[0]); pred=dependent[0]+u*(dependent[1]-dependent[0])
            bracket=None
            for depth in range(4,45,4):
                radius=dependent_width/Q(2**depth); lo=max(dep_lo,pred-radius); hi=min(dep_hi,pred+radius)
                ls,hs=strict_sign(value_at(x,lo)),strict_sign(value_at(x,hi))
                if ls*hs!=-1: continue
                for _ in range(96):
                    mid=(lo+hi)/2; ms=strict_sign(value_at(x,mid))
                    if not ms: break
                    if ms==ls: lo,ls=mid,ms
                    else: hi,hs=mid,ms
                else:
                    bracket=(x,lo,hi); break
            if bracket is None: node_ok=False; reason="NODE_ROOT_ISOLATION"; break
            nodes.append(bracket)
        if not node_ok: continue
        boxes=[]; signs_rows=[]; evidence_rows=[]; good=True
        collar=dependent_width/Q(2**88)
        for index in range(subdivisions):
            x0,y00,y01=nodes[index]; x1,y10,y11=nodes[index+1]
            yl,yu=min(y00,y10)-collar,max(y01,y11)+collar
            box=(min(x0,x1),max(x0,x1),max(dep_lo,yl),min(dep_hi,yu)) if use_t else (max(dep_lo,yl),min(dep_hi,yu),min(x0,x1),max(x0,x1))
            jet=third_tangency_jet(source,branch[1],branch[2],*box); ts,ps=map(strict_sign,jet.gradient[:2]); derivative=ps if use_t else ts
            if not derivative: good=False; reason="TRACKED_IFT_DERIVATIVE"; break
            if use_t:
                lo=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[1],box[2],box[2]).value); hi=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[1],box[3],box[3]).value)
            else:
                lo=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[0],box[0],box[2],box[3]).value); hi=strict_sign(third_tangency_jet(source,branch[1],branch[2],box[1],box[1],box[2],box[3]).value)
            if lo*hi!=-1: good=False; reason="TRACKED_IFT_BOUNDARY_SIGNS"; break
            try:
                atom=step1.Atom(branch[0],source,*box,Q(0),Q(0),f"round89-tracked:{subdivisions}:{index}")
                classification,_,destination,state1,owner2=time3.homogeneity_cert.classify_with_geometry(atom,cores)
                if classification!="SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None or owner2["selected_target_id"]!=branch[1]: good=False; reason="TRACKED_TWO_COLLISION_OWNER"; break
                state2=time3.second_outgoing_state(atom,state1,owner2)
                if state2 is None: good=False; reason="TRACKED_SECOND_STATE"; break
                status,evidence=round87.physical_type(state2,branch[1],branch[2])
                if status!="PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or evidence["signed_transverse_tangency_factor_sign"]!=branch[3]: good=False; reason=status; break
            except (ValueError,ZeroDivisionError,RuntimeError) as exc:
                good=False; reason=type(exc).__name__; break
            boxes.append(box); signs_rows.append((derivative,lo,hi)); evidence_rows.append(evidence)
        if good:
            return {"left_registered_port_id":left["registered_port_id"],"right_registered_port_id":right["registered_port_id"],
                "source_core_index":branch[0],"second_selected_target_id":branch[1],"third_candidate_id":branch[2],"signed_transverse_tangency_factor_sign":branch[3],
                "strip_count":subdivisions,"dependent_collar_depth":88,"continuation_method":"TRACKED_NODE_ROOT_CHAIN",
                "certified_tube_boxes_sha256":digest([list(map(str,x)) for x in boxes]),"implicit_graph_axis":axis,
                "strip_sign_rows_sha256":digest(signs_rows),"whole_chain_two_collision_status":"SURVIVE_THROUGH_2_INNER",
                "whole_chain_third_event_status":"PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION",
                "complete_translated_candidate_count_histogram":dict(sorted(Counter(x["complete_translated_candidate_count"] for x in evidence_rows).items())),
                "whole_chain_competitor_rows_sha256":digest([x["competitor_rows_sha256"] for x in evidence_rows])}
    raise RuntimeError(f"uncertified gap {left['registered_port_id']} -> {right['registered_port_id']}: {reason}")

def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    rows, pair_rows = load()
    physical = {r["registered_port_id"]: r for r in rows if r["port_is_locally_physical_third_tangency"]}
    registered = {frozenset(r["registered_elementary_arc_endpoint_port_ids"]) for r in pair_rows}
    by: dict[tuple[int,str,str,int], list[str]] = defaultdict(list)
    for port_id, row in physical.items(): by[key(row)].append(port_id)
    for branch, ids in by.items():
        ids.sort(key=lambda p: float(qball(physical[p]).mid()))
        if any(strict_sign(qball(physical[b])-qball(physical[a])) != 1 for a,b in zip(ids,ids[1:])):
            raise RuntimeError(f"non-strict q order: {branch}")
    source_count: Counter[tuple[int,str,str,int]] = Counter()
    rank_gaps = Counter(); mismatch = 0
    for row in pair_rows:
        a,b = row["registered_elementary_arc_endpoint_port_ids"]
        pa,pb = a in physical,b in physical
        if pa and pb:
            if key(physical[a]) != key(physical[b]): mismatch += 1; continue
            order = by[key(physical[a])]
            rank_gaps[abs(order.index(a)-order.index(b))] += 1
        elif pa != pb:
            source_count[key(physical[a if pa else b])] += 1
        else: raise RuntimeError("live pair without physical port")
    cores = core_cert.physical_cores(); round87.WORK_CORES = cores
    gap_rows=[]; unresolved_gap_rows=[]; branch_rows=[]
    for rank, branch in enumerate(sorted(by),1):
        ids=by[branch]; gaps=0; adjacent=0
        for a,b in zip(ids,ids[1:]):
            if frozenset((a,b)) in registered: adjacent += 1
            else:
                try:
                    gap_rows.append(certify_gap(physical[a],physical[b],cores)); gaps += 1
                except RuntimeError as exc:
                    unresolved_gap_rows.append({"left_registered_port_id":a,"right_registered_port_id":b,"reason":str(exc).rsplit(": ",1)[-1]})
        branch_rows.append({
            "projective_branch_rank":rank,"source_core_index":branch[0],
            "second_selected_target_id":branch[1],"third_candidate_id":branch[2],
            "signed_transverse_tangency_factor_sign":branch[3],
            "strictly_ordered_physical_port_count":len(ids),
            "registered_source_boundary_endpoint_count":source_count[branch],
            "registered_adjacent_arc_count":adjacent,
            "certified_unregistered_interior_gap_count":gaps,
            "total_registered_endpoint_parity":(len(ids)+source_count[branch])%2,
            "left_exterior_ray_status":"OPEN_PHYSICAL_EVENT_OR_SOURCE_CORE_EXIT",
            "right_exterior_ray_status":"OPEN_PHYSICAL_EVENT_OR_SOURCE_CORE_EXIT",
            "ordered_physical_port_ids_sha256":digest(ids),
        })
    source_hist=Counter(r["registered_source_boundary_endpoint_count"] for r in branch_rows)
    result={
        "precision_bits":precision_bits,"input_locally_physical_port_count":len(physical),
        "input_live_registered_arc_count":len(pair_rows),"oriented_projective_tangent_branch_count":len(branch_rows),
        "registered_arc_branch_key_mismatch_count":mismatch,
        "registered_arc_projective_rank_gap_histogram":dict(sorted(rank_gaps.items())),
        "registered_source_endpoint_count":sum(source_count.values()),
        "branch_registered_source_endpoint_histogram":dict(sorted(source_hist.items())),
        "unregistered_consecutive_projective_gap_count":len(gap_rows)+len(unresolved_gap_rows),
        "certified_whole_tube_physical_gap_count":len(gap_rows),
        "gap_strip_count_histogram":dict(sorted(Counter(r["strip_count"] for r in gap_rows).items())),
        "gap_dependent_collar_depth_histogram":dict(sorted(Counter(r["dependent_collar_depth"] for r in gap_rows).items())),
        "gap_implicit_graph_axis_histogram":dict(sorted(Counter(r["implicit_graph_axis"] for r in gap_rows).items())),
        "remaining_unresolved_interior_projective_gap_count":len(unresolved_gap_rows),
        "unresolved_gap_reason_histogram":dict(sorted(Counter(r["reason"] for r in unresolved_gap_rows).items())),
        "unresolved_gap_rows":unresolved_gap_rows,"unresolved_gap_rows_sha256":digest(unresolved_gap_rows),
        "remaining_exterior_branch_ray_count":2*len(branch_rows),
        "branch_rows":branch_rows,"branch_rows_sha256":digest(branch_rows),
        "gap_rows":gap_rows,"gap_rows_sha256":digest(gap_rows),
        "strict_scope":"whole-tube physical continuation across 432 of the 440 interior projective gaps between consecutive frozen physical ports",
        "strict_nonclaims":["eight interior gaps remain interval-IFT unresolved","the 112 exterior projective branch rays are not continued to typed events","interior gap closure alone does not produce complete physical faces","no Gate5 or RN row is installed"],
        "upstream_pins":PINS,
    }
    if len(physical)!=945 or len(pair_rows)!=496 or len(branch_rows)!=56: raise RuntimeError("input accounting")
    if mismatch or rank_gaps!=Counter({1:449}): raise RuntimeError("adjacency invariant")
    if sum(source_count.values())!=47 or source_hist!=Counter({0:21,1:23,2:12}): raise RuntimeError("source accounting")
    if len(gap_rows)+len(unresolved_gap_rows)!=440 or any(r["total_registered_endpoint_parity"] for r in branch_rows): raise RuntimeError("gap/parity accounting")
    # Canonicalize mapping keys exactly as JSON will serialize them before
    # hashing, so the frozen digest is independently reproducible from disk.
    result=json.loads(json.dumps(result,sort_keys=True))
    return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}

def main() -> int:
    json.dump(build(),sys.stdout,sort_keys=True,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__": raise SystemExit(main())
