#!/usr/bin/env python3
"""Materialize Round269's OUTGOING-G residuals with exact G geometry."""

from __future__ import annotations
import argparse, collections, gc, hashlib, json, multiprocessing as mp, os, stat, sys, tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb, ctx
import cm2_round207_source_g_whole_region_direct_signature_probe as r207

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PREFIX="cm2_round270_source_g_outgoing_g_factor_signature_materialization"
OUTPUT=HERE/f"{PREFIX}_certificate.json"
SCHEMA="cm2.round270.source-g-outgoing-g-factor-signature-materialization.v1"
R182="cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R208="cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R268="cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json"
R269="cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json"
PINS={
R182:("ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c","9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"),
R208:("4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938","d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"),
R268:("10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9","ce8718d74189e678b7ebc7ac9beeec44305d01091cafcfde012f6bb3a882cf24"),
R269:("472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3","2e8071d2a99a206177f5293747bc7c7c9b1716184f4084c4f22fd3cf5bf45b7d"),}
SOURCE_PINS={
"cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py":"f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1",
"cm2_round198_source_g_outgoing_return_signature_probe.py":"59dac5b6e2d79e1612dad51780174f97f71dc1223c01a21b502805d6e9510fbf",
"cm2_round207_source_g_whole_region_direct_signature_probe.py":"0262235b43d74084c37b742b8b4fc435b82e752663d5f816e092faf14e64404a",}
FIELDS=("official_key_id","official_key_ordinal","official_key_row","ordered_integer_wall_events","outgoing_cell","roof","signed_wall_word","source_chart","target_chart","target_lift")
REGISTRY=None; R174=None; R195=None; R198=None

class Error(RuntimeError): pass
def need(x,l):
 if not x: raise Error(l)
def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def digest(x): return hashlib.sha256(canonical(x)).hexdigest()
def close(x):
 y=dict(x); need("row_sha256" not in y,"unclosed"); y["row_sha256"]=digest(y); return y
def ledger(rows,idf): return {"row_count":len(rows),"rows_sha256":digest(rows),"row_ids_sha256":digest([r[idf] for r in rows]),"row_hashes_sha256":digest([r["row_sha256"] for r in rows]),"every_row_closed_by_own_SHA256":True,"rows":rows}
def raw(path,maxn=1_200_000_000):
 st=path.lstat(); need(path.parent==HERE and stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_nlink==1 and 0<st.st_size<=maxn,"regular:"+path.name)
 return path.read_bytes()
def load(name):
 b=raw(HERE/name); fp,rp=PINS[name]; need(hashlib.sha256(b).hexdigest()==fp,"file pin:"+name); d=json.loads(b); need(d["result_sha256"]==rp and digest(d["result"])==rp,"result pin:"+name); return d["result"]
def unpack(r,t):
 rows=r[t]; cols=r["row_column_schemas"][t]; e=r["table_census_and_sha256"][t]; need(len(rows)==e["row_count"] and digest(rows)==e["rows_sha256"],"table:"+t); return [dict(zip(cols,x,strict=True)) for x in rows]

def factor_geometry_g(chart,target_id,box):
 r179=R195.r191.r189.r188.r186.r179
 dc=r179.dconstant
 t=(R174.first_hit.arb_interval(box.t0,box.t1),(arb(1),arb(0),arb(0)))
 p=(R174.first_hit.arb_interval(box.p0,box.p1),(arb(0),arb(1),arb(0)))
 rt0=R174.atlas.ge.sqrt_one_minus_square(box.t0,box.t1); rp0=R174.atlas.ge.sqrt_one_minus_square(box.p0,box.p1)
 rt=(rt0,(-t[0]/rt0,arb(0),arb(0))); rp=(rp0,(arb(0),None if not bool(rp0>0) else -p[0]/rp0,arb(0)))
 cell=chart.split(":")[1]
 if cell=="E": nx,ny=rt,t
 elif cell=="W": nx,ny=r179.dneg(rt),t
 elif cell=="N": nx,ny=t,rt
 else: nx,ny=t,r179.dneg(rt)
 ux=r179.dsub(r179.dmul(rp,nx),r179.dmul(p,ny)); uy=r179.dadd(r179.dmul(rp,ny),r179.dmul(p,nx))
 sx=r179.dscale(nx,arb(9)/25); sy=r179.dscale(ny,arb(9)/25); target=R174.first_hit.target_by_id(target_id)
 need(target.obstacle=="G","G target identity"); cx=dc(arb(target.ix)); cy=dc(arb(target.iy))
 dx=r179.dsub(cx,sx); dy=r179.dsub(cy,sy); transverse=r179.dadd(r179.dneg(r179.dmul(uy,dx)),r179.dmul(ux,dy))
 rq=R174.first_hit.RADIUS["G"]; radius=arb(rq.numerator)/rq.denominator
 disc=r179.dsub(dc(radius*radius),r179.dmul(transverse,transverse)); need(bool(disc[0]>0),"strict G discriminant")
 radical_value=disc[0].sqrt(); radical=(radical_value,tuple(None if q is None else q/(2*radical_value) for q in disc[1]))
 ox=r179.dscale(r179.dadd(r179.dneg(r179.dmul(radical,ux)),r179.dmul(transverse,uy)),1/radius)
 oy=r179.dscale(r179.dsub(r179.dneg(r179.dmul(radical,uy)),r179.dmul(transverse,ux)),1/radius)
 return {"HPLUS":r179.dadd(ox,oy),"HMINUS":r179.dsub(ox,oy),"NX":ox,"NY":oy}

def worker(task):
 rawleaf,collar=task
 need(collar["kind"]=="OUTGOING" and collar["owner_target"].startswith("G["),"Round270 G task domain")
 box=R174.atlas.AtlasBox(*(Q(v) for v in rawleaf["box"]),len(rawleaf["base_refinement_path"]),rawleaf["row_id"])
 base,reasons=r207.direct_leaf_signature_base(collar["chart"],box,REGISTRY)
 if base is None or base["target_lift"]!=collar["owner_target"]:
  return [],close({"failclosed_leaf_row_id":"round270-failclosed:"+digest([rawleaf["row_id"],reasons]),"Round182_leaf_row_id":rawleaf["row_id"],"collar_kind":collar["kind"],"owner_target":collar["owner_target"],"graph_classification":rawleaf["graph_classification"],"direct_failure_reasons":reasons+(["direct_target_mismatch"] if base is not None else []),"signature_credit":0,"occurrence_credit":0,"component_credit":0})
 try:
  lower=R195.decode_round182_face(rawleaf["lower_t_face_status"]); upper=R195.decode_round182_face(rawleaf["upper_t_face_status"])
  leaf=R195.classify_leaf(rawleaf,collar,box,lower,upper)
  geom=R198.factor_region_rows(leaf,rawleaf,collar,box,[],None,set(),{},None)
 except Exception as exc:
  reason=type(exc).__name__+":"+str(exc)
  return [],close({"failclosed_leaf_row_id":"round270-failclosed:"+digest([rawleaf["row_id"],reason]),"Round182_leaf_row_id":rawleaf["row_id"],"collar_kind":collar["kind"],"owner_target":collar["owner_target"],"graph_classification":rawleaf["graph_classification"],"direct_failure_reasons":["OUTSIDE_PINNED_ROUND270_G_FACTOR_DOMAIN",reason],"signature_credit":0,"occurrence_credit":0,"component_credit":0})
 rows=[]
 for g in geom:
  sig={k:base[k] for k in ("source_chart","target_lift","ordered_integer_wall_events","signed_wall_word","roof","official_key_row","official_key_ordinal","official_key_id")}
  sig["outgoing_cell"]=g["outgoing_cell"]; sig["target_chart"]=sig["target_lift"].split("[",1)[0]+":"+g["outgoing_cell"]
  need(set(sig)==set(FIELDS),"signature fields")
  rows.append(close({"signed_region_row_id":"round270-signed-region:"+digest([g["candidate_region_id"],sig]),"Round182_leaf_row_id":rawleaf["row_id"],"candidate_region_id":g["candidate_region_id"],"occurrence_row_id":rawleaf["occurrence_row_id"],"retained_child_row_id":rawleaf["retained_child_row_id"],"chart":collar["chart"],"owner_target":collar["owner_target"],"graph_classification":leaf["final_graph_classification"],"region_factor_sign":g["F_sign"],"HPLUS_sign":g["HPLUS_sign"],"HMINUS_sign":g["HMINUS_sign"],"local_return_signature":sig,"complete_10_field_return_signature_sha256":digest(sig),"direct_whole_leaf_base_certified":True,"side_specific_signature_credit":1,"expanded_occurrence_credit":0,"component_edge_credit":0,"maximality_credit":0,"global_exact_key_disposition_credit":0}))
 return rows,None

def build(psha,processes):
 global REGISTRY,R174,R195,R198
 for n,h in SOURCE_PINS.items(): need(hashlib.sha256(raw(HERE/n,5_000_000)).hexdigest()==h,"source pin:"+n)
 chain=r207.check_inputs(); R198=r207.r203.r198; R195=R198.r195; R174=R195.r191.r189.r188.r186.r179.r174
 frozen=R174.load_frozen_inputs(); REGISTRY=R174.rebuild_registry(frozen["gate5"]); del frozen; gc.collect()
 r182=load(R182); r208=load(R208); r268=load(R268); r269=load(R269)
 need(r268["census"]["post_Round268_component_count"]==63224 and r269["census"]["remaining_OUTGOING_G_leaf_count"]==24512,"baseline")
 R195.r191.r189.r188.r186.factor_geometry=factor_geometry_g
 collars={x["Round179_occurrence_row_id"]:x for x in unpack(r182,"collar_occurrence_rows")}
 tasks=[]
 for x in unpack(r182,"collar_leaf_rows"):
  collar=collars[x["occurrence_row_id"]]
  if x["closed_3d_side_union_volume"]!="0" and collar["kind"]=="OUTGOING" and collar["owner_target"].startswith("G["): tasks.append((x,collar))
 need(len(tasks)==24512,"G residual census")
 signed=[]; failed=[]
 with mp.get_context("fork").Pool(processes) as pool:
  for rows,bad in pool.imap_unordered(worker,tasks,chunksize=16): signed.extend(rows); failed.extend([] if bad is None else [bad])
 signed.sort(key=lambda x:x["signed_region_row_id"]); failed.sort(key=lambda x:x["failclosed_leaf_row_id"])
 print(f"observed_signed={len(signed)} observed_failed={len(failed)} observed_success_leaves={len({x['Round182_leaf_row_id'] for x in signed})}",file=sys.stderr,flush=True)
 need(len(signed)==37712 and len(failed)==8,"G tranche census")
 success_leaves={x["Round182_leaf_row_id"] for x in signed}; need(len(success_leaves)==24504,"G success leaves")
 existing=r208["formal_local_open_3D_signature_ledger"]["rows"]
 need(len(existing)==36040 and len({x["leaf_row_id"] for x in existing})==18324 and not ({x["leaf_row_id"] for x in existing}&success_leaves),"Round208 residual-leaf disjointness")
 prior={x["Round182_leaf_row_id"] for x in r269["formal_direct_side_signature_ledger"]["rows"]}; need(len(prior)==114032 and not (prior&success_leaves),"Round269 W/G disjointness")
 return {"status":"CERTIFIED_24504_OF_24512_OUTGOING_G_LEAVES__37712_COMPLETE_SIDE_SIGNATURES__8_WALL_EVENT_RESIDUALS__ZERO_OCCURRENCE_OR_COMPONENT_PROMOTION","census":{"input_OUTGOING_G_leaf_count":24512,"signature_leaf_count":24504,"signed_region_count":37712,"remaining_OUTGOING_G_failclosed_leaf_count":8,"remaining_OUTGOING_W_failclosed_leaf_count":4,"remaining_WALL_leaf_count":45904,"remaining_total_closed_leaf_count":45916,"post_Round270_component_count":63224,"expanded_occurrence_frontier_count":126468,"exact_key_frontier_count":116,"maximal_component_assignment_count":0,"globally_exhausted_exact_key_fibre_count":0,"global_exact_key_disposition_count":0},"formal_direct_side_signature_ledger":ledger(signed,"signed_region_row_id"),"formal_failclosed_leaf_ledger":ledger(failed,"failclosed_leaf_row_id"),"scope_contract":{"all_24512_OUTGOING_G_residual_leaves_evaluated":True,"all_24504_accepts_use_the_exact_G_target_center_and_radius":True,"all_accepts_have_complete_direct_10_field_bases_and_strict_factor_cells":True,"Round208_and_Round269_leaf_domains_disjoint_from_accepts":True,"signatures_are_not_yet_expanded_occurrences":True,"remaining_8_leaves_receive_zero_credit":True,"Jx_Jy_same_point_glue_credit":0},"strict_nonpromotion":{"new_expanded_occurrence_credit":0,"new_component_union_credit":0,"Jx_Jy_same_point_glue_credit":0,"maximal_physical_component_credit":0,"global_exact_key_fibre_credit":0,"global_exact_key_disposition_credit":0,"source_G_global_exact_key_dispositions":"0/224580","D02":"BLOCKED","Gate5_filled_field_slot_count":10,"Gate5_total_field_slot_count":18,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"close the 8 outgoing-G wall-event and 4 outgoing-W t-derivative residuals; materialize 45,904 WALL leaves by exact side-specific integer-wall insertion; then bind all signed regions and the 152 frozen true-seam patches to the expanded component frontier","provenance":{"schema":SCHEMA,"producer_sha256":psha,"python_version":sys.version.split()[0],"python_flint_version":str(ctx),"process_count":processes,"seed_affects_output":False,"pinned_evaluator_chain":chain,"G_factor_geometry":"exact target center (ix,iy), radius 9/25, 256-bit Arb dual enclosure"}}

def write(b):
 fd,n=tempfile.mkstemp(prefix="."+OUTPUT.name+".",suffix=".tmp",dir=HERE); p=Path(n)
 try:
  with os.fdopen(fd,"wb") as f:f.write(b);f.flush();os.fsync(f.fileno())
  os.replace(p,OUTPUT)
 finally:
  if p.exists():p.unlink()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--seed",type=int,default=270071);ap.add_argument("--processes",type=int,default=40);ap.add_argument("--no-write",action="store_true");a=ap.parse_args();need(1<=a.processes<=64,"processes")
 psha=hashlib.sha256(raw(Path(__file__).resolve(),5_000_000)).hexdigest(); result=build(psha,a.processes); doc={"schema":SCHEMA,"result":result,"result_sha256":digest(result)}; b=canonical(doc)+b"\n";
 if not a.no_write:write(b)
 print(result["status"]);print("producer_sha256="+psha);print("result_sha256="+doc["result_sha256"]);print("certificate_sha256="+hashlib.sha256(b).hexdigest());return 0
if __name__=="__main__":raise SystemExit(main())
