#!/usr/bin/env python3
"""Conservative variable-return crosswalk and exact frozen-atlas deficit."""

from __future__ import annotations

import hashlib, json, math
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as atlas

HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round85.c24-variable-return-crosswalk.v1"
FULL = HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
PINS = {FULL.name: "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
        "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
        "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"}
N, NS = 64, 16

def canon(x: Any) -> str: return json.dumps(x, sort_keys=True, separators=(",", ":"), allow_nan=False)
def digest(x: Any) -> str: return hashlib.sha256(canon(x).encode()).hexdigest()
def fsha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def req(x: bool, s: str) -> None:
    if not x: raise ValueError(s)
def collect(x: Any, out: list[dict[str, Any]]) -> None:
    if isinstance(x, dict):
        if "classification" in x and "source_box" in x and "atom_id" in x: out.append(x)
        for y in x.values(): collect(y, out)
    elif isinstance(x, list):
        for y in x: collect(y, out)

def irange(a: Q, z: Q, lo: Q, hi: Q, n: int) -> range:
    i0 = max(0, min(n-1, int((a-lo)*n/(hi-lo))))
    i1 = max(0, min(n-1, int((z-lo)*n/(hi-lo))))
    return range(i0, i1+1)

def build(bits: int = 512) -> dict[str, Any]:
    ctx.prec = bits
    for n,h in PINS.items(): req(fsha(HERE/n)==h, "pin "+n)
    rows: list[dict[str, Any]]=[]; collect(json.loads(FULL.read_text()), rows)
    hist=Counter(r["classification"] for r in rows)
    req(hist=={"RETURN_AT_1_INNER":4216,"SURVIVE_THROUGH_1_INNER":2868,"UNRESOLVED_OUTER":26876},"leaf census")
    returns=[r for r in rows if r["classification"]=="RETURN_AT_1_INNER"]
    cores_list=core_cert.physical_cores(); cores={atlas.core_id(c):c for c in cores_list}
    bins: dict[tuple[str,int,int,int],set[int]]={}
    for j,r in enumerate(rows):
        c=cores[r["source_core_id"]]; b=r["source_box"]
        rr=[irange(*map(Q,b["t"]),c.t0,c.t1,N),irange(*map(Q,b["p"]),c.p0,c.p1,N),
            irange(*map(Q,b["s"]),core_cert.S_LOWER,core_cert.S_UPPER,NS)]
        for it in rr[0]:
            for ip in rr[1]:
                for iss in rr[2]: bins.setdefault((r["source_core_id"],it,ip,iss),set()).add(j)
    edge_hist=Counter(); class_sets=Counter(); mult=Counter(); reached=set(); reached_unresolved=set(); contained=Counter(); edge_rows=[]
    for r in sorted(returns,key=lambda x:x["atom_id"]):
        c=cores[r["source_core_id"]]; b=r["source_box"]
        a=atlas.Atom(0,c,*map(Q,b["t"]),*map(Q,b["p"]),*map(Q,b["s"]),"")
        g=atlas.atom_geometry(a); req(g is not None,"geometry")
        d=cores[r["destination_core_id"]]
        t=atlas.chart_tests(d.chart_id.split(":")[1],g["normal_x"],g["normal_y"])[0]; p=g["p_target"]
        specs=[(float(t.lower()),float(t.upper()),d.t0,d.t1,N),(float(p.lower()),float(p.upper()),d.p0,d.p1,N),
               (float(Q(b["s"][0])),float(Q(b["s"][1])),core_cert.S_LOWER,core_cert.S_UPPER,NS)]
        br=[]
        for x0,x1,lo,hi,n in specs:
            i0=max(0,min(n-1,math.floor((x0-float(lo))*n/float(hi-lo))-1)); i1=max(0,min(n-1,math.floor((x1-float(lo))*n/float(hi-lo))+1)); br.append(range(i0,i1+1))
        # Expanded proposal bins are accepted only after enclosure coverage checks.
        req(br[0].start==0 or bool(t>atlas.arbq(d.t0+(d.t1-d.t0)*Q(br[0].start,N))),"t lower bin cover")
        req(br[0].stop==N or bool(t<atlas.arbq(d.t0+(d.t1-d.t0)*Q(br[0].stop,N))),"t upper bin cover")
        req(br[1].start==0 or bool(p>atlas.arbq(d.p0+(d.p1-d.p0)*Q(br[1].start,N))),"p lower bin cover")
        req(br[1].stop==N or bool(p<atlas.arbq(d.p0+(d.p1-d.p0)*Q(br[1].stop,N))),"p upper bin cover")
        cand=set()
        for it in br[0]:
            for ip in br[1]:
                for iss in br[2]: cand.update(bins.get((r["destination_core_id"],it,ip,iss),()))
        local=[]; s0,s1=map(Q,b["s"])
        for j in sorted(cand):
            q=rows[j]; tb=list(map(Q,q["source_box"]["t"])); pb=list(map(Q,q["source_box"]["p"])); sb=list(map(Q,q["source_box"]["s"]))
            if s1<sb[0] or sb[1]<s0 or bool(t<atlas.arbq(tb[0])) or bool(t>atlas.arbq(tb[1])) or bool(p<atlas.arbq(pb[0])) or bool(p>atlas.arbq(pb[1])): continue
            kind=q["classification"]; local.append(kind); reached.add(j); edge_hist[kind]+=1
            if kind=="UNRESOLVED_OUTER": reached_unresolved.add(j)
            inside=(bool(t>atlas.arbq(tb[0])) and bool(t<atlas.arbq(tb[1])) and bool(p>atlas.arbq(pb[0])) and bool(p<atlas.arbq(pb[1])) and s0>=sb[0] and s1<=sb[1])
            if inside: contained[kind]+=1
            edge_rows.append([r["atom_id"],q["atom_id"],kind,"WHOLE_ENCLOSURE_CONTAINED" if inside else "INTERVAL_POSSIBLE"])
        req(bool(local),"landing coverage"); class_sets[tuple(sorted(set(local)))]+=1; mult[len(local)]+=1
    req(edge_hist=={"SURVIVE_THROUGH_1_INNER":10352,"UNRESOLVED_OUTER":32},"edge histogram")
    req(class_sets=={("SURVIVE_THROUGH_1_INNER",):4208,("SURVIVE_THROUGH_1_INNER","UNRESOLVED_OUTER"):8},"class sets")
    req(contained=={"SURVIVE_THROUGH_1_INNER":1888},"containment")
    reached_hist=Counter(rows[j]["classification"] for j in reached)
    req(reached_hist=={"SURVIVE_THROUGH_1_INNER":176,"UNRESOLVED_OUTER":32},"reached targets")
    # Re-run the 32 reached unresolved parents at current precision: all remain unresolved.
    unresolved_replay=[]
    for j in sorted(reached_unresolved):
        q=rows[j]; c=cores[q["source_core_id"]]; b=q["source_box"]
        z=atlas.classify_atom(atlas.Atom(0,c,*map(Q,b["t"]),*map(Q,b["p"]),*map(Q,b["s"]),q["dyadic_path"]),cores_list)
        req(z["classification"]=="UNRESOLVED_OUTER","reached unresolved replay"); unresolved_replay.append(q["atom_id"])
    evidence={"precision_bits":bits,"full_leaf_count":33960,"leaf_classification_histogram":dict(sorted(hist.items())),
              "return_landing_count":4216,"possible_edge_count":len(edge_rows),"possible_edge_classification_histogram":dict(sorted(edge_hist.items())),
              "landing_candidate_class_set_histogram":{"SURVIVE_ONLY":4208,"SURVIVE_AND_UNRESOLVED":8},
              "whole_enclosure_contained_in_one_survivor_box_count":1888,"boundary_straddling_landing_count":2328,
              "unique_reached_target_atom_histogram":dict(sorted(reached_hist.items())),"reached_unresolved_512bit_replay_count":len(unresolved_replay),
              "multiplicity_histogram":{str(k):v for k,v in sorted(mult.items())},"edge_rows":edge_rows,"reached_unresolved_atom_ids":unresolved_replay}
    result={"status":"CERTIFIED_VARIABLE_RETURN_CROSSWALK_COVERAGE_WITH_32_UNRESOLVED_TARGET_ATOMS",
            "graph_frontier":{"RETURN_to_RETURN_possible_edges":0,"RETURN_to_SURVIVE_possible_edges":10352,"RETURN_to_UNRESOLVED_possible_edges":32,
                              "nonempty_recurrent_or_cyclic_SCC_certified":False,"reason":"all available next boxes are survivor or unresolved; no frozen later-time atlas exists"},
            "minimum_next_generator_interface":{"inputs":["32 unresolved rational t,p,s boxes","source core and target word key","4216-to-leaf edge ledger"],
              "operations":["normalized-longest-axis dyadic subdivision","512-bit strict classification against all 24 C24 cores","interval preimage crosswalk refinement for 2328 boundary-straddling landings","mass-preserving child cover ledger"],
              "required_outputs":["resolved RETURN/SURVIVE children","all residual unresolved children","variable return time and path key","landing-to-child incidence rows"]},
            "strict_nonpromotion":{"interval_possible_edge_is_not_nonempty_orbit":True,"graph_recurrence_would_not_be_a_stable_plaque":True,"Gate2":"NOT_CERTIFIED__0_OF_17","Gate4":"NOT_CERTIFIED__1_OF_7"},
            "evidence":evidence,"evidence_sha256":digest(evidence)}
    return {"schema":SCHEMA,"pins":dict(PINS),"result":result,"result_sha256":digest(result)}

if __name__=="__main__": print(json.dumps(build(),sort_keys=True,indent=2,allow_nan=False))
