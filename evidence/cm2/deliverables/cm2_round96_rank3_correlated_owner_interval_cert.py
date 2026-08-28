#!/usr/bin/env python3
"""Correlation-preserving q-dual owner/competitor coverage for rank three."""
from __future__ import annotations
import hashlib,json,multiprocessing as mp,os
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from flint import arb,ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round94_rank3_adjacent_chart_transfer_cert as round94
import cm2_round95_rank3_centered_reverse_interval_cert as round95
from cm2_round79_tangency_intersection_generator import aq,digest,strict_sign
HERE=Path(__file__).resolve().parent;R95=HERE/"cm2-round95-rank3-centered-reverse-interval-2026-07-22.json";R94=HERE/"cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json"
PINS={R95.name:"134991f623c54c42265da2bde17e01dfc21d551349636d04f7808f3e2ef68297",R94.name:"915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3"}
SCHEMA="cm2.round96.rank3-correlated-owner-interval.v1";PRECISION_BITS=512;MAX_DEPTH=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def chart(normal):
 x,y=normal;ax,ay=abs(x.value),abs(y.value)
 if bool(ax>ay):
  if bool(x.value>0):return "E"
  if bool(x.value<0):return "W"
 if bool(ay>ax):
  if bool(y.value>0):return "N"
  if bool(y.value<0):return "S"
 raise RuntimeError("correlated chart seam")
def state(source,branch,q,path):
 n,direction,h=round95.tangent(branch,q);hit2,normal2=round95.line_hit(n,direction,h,branch[1],path[0]);incoming2=round95.reflect(direction,normal2);reverse1=round95.scale(-1,incoming2);hit1,normal1,flight1=round95.ray_hit(hit2,reverse1,source.target_id,path[1]);initial=round95.reflect(incoming2,normal1);reverse0=round95.scale(-1,initial);hit0,normal0,flight0=round95.ray_hit(hit1,reverse0,f"{source.source}[0,0]",path[2]);contact=round95.sub(round95.center(branch[2]),round95.scale(branch[3]*round95.radius(branch[2]),n));tangent_flight=round95.dot(direction,round95.sub(contact,hit2));return {"hit0":hit0,"initial":initial,"flight0":flight0,"hit1":hit1,"outgoing1":incoming2,"normal1":normal1,"flight1":flight1,"hit2":hit2,"outgoing2":direction,"normal2":normal2,"tangent_flight":tangent_flight}
def clear_before(point,velocity,target,terminal,stage):
 delta=round95.sub(round95.center(target),point);ell=round95.dot(velocity,delta);transverse=round95.cross(velocity,delta);r=round95.radius(target);line_clear=transverse*transverse-r*r;end_clear=(ell-terminal)*(ell-terminal)+transverse*transverse-r*r
 if strict_sign(line_clear.value)==1:return "WHOLE_LINE_MISS"
 if bool(ell.value<0):return "CLOSEST_BEHIND_START"
 if bool(ell.value>terminal.value) and strict_sign(end_clear.value)==1:return "CLOSEST_AFTER_TERMINAL__END_CLEAR"
 raise RuntimeError(f"{stage} competitor segment unresolved:{target}")
def certify(source,branch,qa,qb):
 lo,hi=min(qa,qb),max(qa,qb);mid=(lo+hi)/2;rad=(hi-lo)/2;path=round95.discover_path(source,branch,mid);delta=arb(0,aq(rad).upper());q=round95.Centered.variable(aq(mid),round91.qball(lo,hi),delta);row=state(source,branch,q,path)
 for terminal in (row["flight0"],row["flight1"],row["tangent_flight"]):
  if not bool(terminal.value>0) or not bool(terminal.value<aq(Q(3))):raise RuntimeError("selected flight")
 first=[]
 for target in first_hit.candidate_ids(source.chart_id):
  if target not in {source.target_id,f"{source.source}[0,0]"}:first.append((target,clear_before(row["hit0"],row["initial"],target,row["flight0"],"first")))
 c1=chart(row["normal1"]);second=[]
 for target in time2.translated_candidate_ids(source.target_id,c1):
  if target not in {branch[1],source.target_id}:second.append((target,clear_before(row["hit1"],row["outgoing1"],target,row["flight1"],"second")))
 c2=chart(row["normal2"]);third=[]
 for target in time2.translated_candidate_ids(branch[1],c2):
  if target not in {branch[2],branch[1]}:third.append((target,clear_before(row["hit2"],row["outgoing2"],target,row["tangent_flight"],"third")))
 return path,c1,c2,digest(first),digest(second),digest(third)
def cover(source,branch,qa,qb):
 pending=[(qa,qb,0)];leaves=[];fail=[]
 while pending:
  a,b,d=pending.pop()
  try:data=certify(source,branch,a,b)
  except (RuntimeError,ValueError,ZeroDivisionError) as exc:
   if d==MAX_DEPTH:fail.append((str(a),str(b),type(exc).__name__,str(exc)));continue
   m=(a+b)/2;pending.extend(((m,b,d+1),(a,m,d+1)));continue
  leaves.append((str(a),str(b),d,*data))
 return leaves,fail
def ray_task(task):
 ri,branch,side,pid,segments,precision_bits=task;ctx.prec=precision_bits;leaves=[];fail=[]
 for source,a,b in segments:
  x,y=cover(source,branch,a,b);leaves+=x;fail+=y
 return {"ray_index":ri,"exterior_port_id":pid,"branch_key":list(branch),"projective_end":side,"input_gap_count":len(segments),"certified_correlated_leaf_count":len(leaves),"maximum_split_depth":max((x[2] for x in leaves),default=0),"unresolved_leaf_count":len(fail),"certified_rows_sha256":digest(leaves),"unresolved_rows_sha256":digest(fail),"unresolved_reason_histogram":dict(sorted(Counter(x[2]+":"+x[3] for x in fail).items()))}
def build(precision_bits=PRECISION_BITS):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin:{n}")
 f94=json.loads(R94.read_text())["result"];t94={r["exterior_port_id"]:r for r in f94["transfer_rows"]};events,_=round89.load();physical={r["registered_port_id"]:r for r in events if r["port_is_locally_physical_third_tangency"]};cores=core_cert.physical_cores();tasks=[]
 for ri,(branch,side,pid) in enumerate(round93.rays(physical)):
  q0,d,ce,inner,seam_outer,*_=round93.isolate_event(branch,side,pid,physical,cores);source=cores[branch[0]];segments=[];bounds=[ce+(inner-ce)*Q(i,round93.PROBE_COUNT+1) for i in range(round93.PROBE_COUNT+2)];segments.extend((source,q0+d*a,q0+d*b) for a,b in zip(bounds,bounds[1:]))
  if pid in t94:
   tr=t94[pid];source=replace(source,chart_id=f"{source.source}:{tr['adjacent_source_chart']}");end=Q(tr["first_physical_terminal_event_parameter_bracket"][0]);bounds=[seam_outer+(end-seam_outer)*Q(i,round94.PROBE_COUNT+1) for i in range(round94.PROBE_COUNT+2)];segments.extend((source,q0+d*a,q0+d*b) for a,b in zip(bounds,bounds[1:]))
  tasks.append((ri,branch,side,pid,segments,precision_bits))
 workers=min(16,os.cpu_count() or 1)
 with mp.Pool(workers) as pool:rows=list(pool.imap_unordered(ray_task,tasks))
 rows.sort(key=lambda row:row["ray_index"])
 all_reasons=Counter()
 for row in rows:all_reasons.update(row["unresolved_reason_histogram"])
 representation_residual=sum(value for key,value in all_reasons.items() if "third competitor" not in key)
 third_residual=sum(value for key,value in all_reasons.items() if "third competitor" in key)
 result={"precision_bits":precision_bits,"input_rank3_ray_count":65,"input_probe_gap_count":sum(r["input_gap_count"] for r in rows),"first_second_owner_base_gap_certified_count":sum(r["input_gap_count"] for r in rows)-representation_residual,"third_competitor_base_gap_certified_count":sum(r["certified_correlated_leaf_count"] for r in rows),"third_competitor_residual_count":third_residual,"representation_boundary_residual_count":representation_residual,"fully_correlated_owner_covered_ray_count":sum(not r["unresolved_leaf_count"] for r in rows),"remaining_unresolved_leaf_count":sum(r["unresolved_leaf_count"] for r in rows),"global_unresolved_reason_histogram":dict(sorted(all_reasons.items())),"ray_rows":rows,"ray_rows_sha256":digest(rows),"strict_scope":"same-q centered mean-form propagation through first-owner, second-owner, and third-competitor segment-clearance comparisons","strict_nonclaims":["depth-zero base-gap frontier; Round95 subdivisions are not replayed here","third-competitor residuals require root-order rather than segment-clearance treatment","physical face quotient incidence assembly remains separate"],"upstream_pins":PINS};result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
