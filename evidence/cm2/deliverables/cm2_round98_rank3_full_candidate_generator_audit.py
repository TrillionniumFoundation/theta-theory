#!/usr/bin/env python3
"""Audit the consumed-generator bug in the Round92 third-candidate replay."""
from __future__ import annotations
import hashlib,json,multiprocessing as mp,os
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from flint import arb,ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round94_rank3_adjacent_chart_transfer_cert as round94
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round96_rank3_correlated_owner_interval_cert as round96
from cm2_round79_tangency_intersection_generator import aq,digest,strict_sign
HERE=Path(__file__).resolve().parent;R97=HERE/"cm2-round97-rank3-centered-near-root-order-frontier-2026-07-22.json";R94=HERE/"cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json"
PINS={R97.name:"9e6b31dd1256ed3d62bbd95f83fcbbf02c80e51e7422bb20fef06a9d7a52d2c5",R94.name:"915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3"};SCHEMA="cm2.round98.rank3-full-candidate-generator-audit.v1";PRECISION_BITS=512
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def point_audit(task):
 index,source,branch,qvalue,precision_bits=task;ctx.prec=precision_bits;path=round95.discover_path(source,branch,qvalue);state=round96.state(source,branch,round95.Dual(aq(qvalue),arb(1)),path);chart=round96.chart(state["normal2"]);full=list(time2.translated_candidate_ids(branch[1],chart));generator=time2.translated_candidate_ids(branch[1],chart);present=branch[2] in generator;suffix=list(generator)
 if not present:raise RuntimeError("tangent target absent")
 before=[];terminal=state["tangent_flight"]
 for target in full:
  if target in {branch[1],branch[2]}:continue
  delta=round95.sub(round95.center(target),state["hit2"]);ell=round95.dot(state["outgoing2"],delta);trans=round95.cross(state["outgoing2"],delta);radius=round95.radius(target);disc=radius*radius-trans*trans
  if strict_sign(disc.value)<=0:continue
  root=disc.sqrt();near=ell-root;far=ell+root
  if bool(far.value<0):continue
  if bool(near.value>0) and bool(near.value<terminal.value):before.append((target,str(near.value)))
 return index,{"full_candidate_count":len(full),"post_membership_suffix_count":len(suffix),"consumed_prefix_count":len(full)-len(suffix),"corrected_status":"OCCLUDED_BY_EARLIER_THIRD_OWNER" if before else "PHYSICAL_NEXT_TANGENCY","earlier_candidate_ids":sorted(x[0] for x in before),"earlier_rows_sha256":digest(before)}
def build(precision_bits=PRECISION_BITS):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin:{n}")
 f94=json.loads(R94.read_text())["result"];t94={r["exterior_port_id"]:r for r in f94["transfer_rows"]};events,_=round89.load();physical={r["registered_port_id"]:r for r in events if r["port_is_locally_physical_third_tangency"]};cores=core_cert.physical_cores();tasks=[];meta=[]
 for ri,(branch,side,pid) in enumerate(round93.rays(physical)):
  q0,d,ce,inner,seam_outer,*_=round93.isolate_event(branch,side,pid,physical,cores);source=cores[branch[0]]
  for i in range(1,round93.PROBE_COUNT+1):meta.append((ri,pid,branch,side,"ROUND93"));tasks.append((len(tasks),source,branch,q0+d*(ce+(inner-ce)*Q(i,round93.PROBE_COUNT+1)),precision_bits))
  if pid in t94:
   tr=t94[pid];source=replace(source,chart_id=f"{source.source}:{tr['adjacent_source_chart']}");end=Q(tr["first_physical_terminal_event_parameter_bracket"][0])
   for i in range(1,round94.PROBE_COUNT+1):meta.append((ri,pid,branch,side,"ROUND94_TRANSFER"));tasks.append((len(tasks),source,branch,q0+d*(seam_outer+(end-seam_outer)*Q(i,round94.PROBE_COUNT+1)),precision_bits))
 with mp.Pool(min(16,os.cpu_count() or 1)) as pool:raw=list(pool.imap_unordered(point_audit,tasks));raw.sort()
 rows=[]
 for (index,data),identity in zip(raw,meta):rows.append({"probe_index":index,"ray_index":identity[0],"exterior_port_id":identity[1],"branch_key":list(identity[2]),"projective_end":identity[3],"probe_layer":identity[4],**data})
 occluded=[r for r in rows if r["corrected_status"]!="PHYSICAL_NEXT_TANGENCY"];ray_status={}
 for r in rows:ray_status.setdefault(r["exterior_port_id"],Counter())[r["corrected_status"]]+=1
 result={"precision_bits":precision_bits,"audited_probe_count":len(rows),"round93_probe_count":sum(r["probe_layer"]=="ROUND93" for r in rows),"round94_transferred_probe_count":sum(r["probe_layer"]=="ROUND94_TRANSFER" for r in rows),"corrected_physical_probe_count":len(rows)-len(occluded),"corrected_occluded_probe_count":len(occluded),"rays_with_any_corrected_occlusion":sum(counts["OCCLUDED_BY_EARLIER_THIRD_OWNER"]>0 for counts in ray_status.values()),"rays_all_probes_corrected_physical":sum(counts["OCCLUDED_BY_EARLIER_THIRD_OWNER"]==0 for counts in ray_status.values()),"earlier_candidate_histogram":dict(sorted(Counter(x for r in occluded for x in r["earlier_candidate_ids"]).items())),"minimum_consumed_prefix_count":min(r["consumed_prefix_count"] for r in rows),"maximum_consumed_prefix_count":max(r["consumed_prefix_count"] for r in rows),"probe_rows":rows,"probe_rows_sha256":digest(rows),"strict_conclusion":"Round92 centered_competitor_rows consumes the translated-candidate generator during membership testing and omits every preceding candidate from the subsequent loop","invalidated_claims":["Round93 all 8320 probes physical","Round94 transferred physical-prefix census","Round95 physical-prefix interpretation; reverse-coordinate coverage remains algebraic"],"strict_nonclaims":["no corrected whole-interval quotient is asserted","global gate vector was never promoted and remains unchanged"],"upstream_pins":PINS};result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
