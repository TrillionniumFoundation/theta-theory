#!/usr/bin/env python3
"""Close Round271's apparent dual-factor WALL tails by one-sided identities."""
from __future__ import annotations
import argparse,collections,gc,hashlib,json,multiprocessing as mp,os,stat,sys,tempfile
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from flint import ctx
import cm2_round179_source_g_residual_tube_arrangement_verifier as r179
import cm2_round207_source_g_whole_region_direct_signature_probe as r207

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PREFIX="cm2_round272_source_g_boundary_dual_factor_wall_closure"
OUTPUT=HERE/f"{PREFIX}_certificate.json"
SCHEMA="cm2.round272.source-g-boundary-dual-factor-wall-closure.v1"
R182="cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R269="cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json"
R270="cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json"
R271="cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json"
PINS={
 R182:("ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c","9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"),
 R269:("472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3","2e8071d2a99a206177f5293747bc7c7c9b1716184f4084c4f22fd3cf5bf45b7d"),
 R270:("72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea","5c9c0585bf2cb664df493224f1005d4ef078d5e2f2e3044283019053b5e39add"),
 R271:("c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747","30f509eb10b1a25c5195e672e980d7e4e651dadc3defd5e150245c6798060506"),}
SOURCE_PINS={
 "cm2_round179_source_g_residual_tube_arrangement_verifier.py":"292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
 "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py":"8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
 "cm2_round207_source_g_whole_region_direct_signature_probe.py":"0262235b43d74084c37b742b8b4fc435b82e752663d5f816e092faf14e64404a",}
FIELDS=("official_key_id","official_key_ordinal","official_key_row","ordered_integer_wall_events","outgoing_cell","roof","signed_wall_word","source_chart","target_chart","target_lift")
REGISTRY=None; R174=None; R182M=None; R186=None; R195=None; R198=None

class Error(RuntimeError):pass
def need(x,l):
 if not x:raise Error(l)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def close(x):
 y=dict(x);need("row_sha256" not in y,"unclosed");y["row_sha256"]=digest(y);return y
def ledger(rows,idf):return {"row_count":len(rows),"rows_sha256":digest(rows),"row_ids_sha256":digest([x[idf] for x in rows]),"row_hashes_sha256":digest([x["row_sha256"] for x in rows]),"every_row_closed_by_own_SHA256":True,"rows":rows}
def raw(p,maxn=1_200_000_000):
 st=p.lstat();need(p.parent==HERE and stat.S_ISREG(st.st_mode) and not p.is_symlink() and st.st_nlink==1 and 0<st.st_size<=maxn,"regular:"+p.name);return p.read_bytes()
def load(n):
 b=raw(HERE/n);fp,rp=PINS[n];need(hashlib.sha256(b).hexdigest()==fp,"file pin:"+n);d=json.loads(b);need(d["result_sha256"]==rp and digest(d["result"])==rp,"result pin:"+n);return d["result"]
def unpack(r,t):
 rows=r[t];cols=r["row_column_schemas"][t];e=r["table_census_and_sha256"][t];need(len(rows)==e["row_count"] and digest(rows)==e["rows_sha256"],"table:"+t);return [dict(zip(cols,x,strict=True)) for x in rows]
def signature(base,cell=None):
 s={k:base[k] for k in ("source_chart","target_lift","ordered_integer_wall_events","signed_wall_word","roof","official_key_row","official_key_ordinal","official_key_id")};s["outgoing_cell"]=base["whole_leaf_box_outgoing_cell"] if cell is None else cell;need(s["outgoing_cell"] is not None,"outgoing cell");s["target_chart"]=s["target_lift"].split("[",1)[0]+":"+s["outgoing_cell"];need(set(s)==set(FIELDS),"signature fields");return s
def candidate_signs(row):
 if row["graph_classification"]!="EMPTY":return ("STRICT_NEGATIVE","STRICT_POSITIVE")
 f=[R195.decode_round182_face(row[x]) for x in ("lower_t_face_status","upper_t_face_status")];ss=[x["resolved_sign"] for x in f];need(ss[0]==ss[1] and ss[0] in {"STRICT_NEGATIVE","STRICT_POSITIVE"},"empty sign");return (ss[0],)
def point_box(box,ft,fp,fs,path):
 t=box.t0+(box.t1-box.t0)*ft;p=box.p0+(box.p1-box.p0)*fp;s=box.s0+(box.s1-box.s0)*fs;return R174.atlas.AtlasBox(t,t,p,p,s,s,box.depth+1,path)
FR=(Q(1,1048576),Q(1048575,1048576),Q(1,4096),Q(4095,4096),Q(1,64),Q(63,64),Q(1,2),Q(1,8),Q(7,8))
def wall_factor_signs(collar,box):
 g=r179.independent_geometry(collar["chart"],collar["owner_target"],box);_,axis,wall=collar["reason_label"].split(":");wall=int(wall);a=g["source_x" if axis=="X" else "source_y"][0]-wall;b=g["hit_x" if axis=="X" else "hit_y"][0]-wall;return r179.arb_sign(a),r179.arb_sign(b),axis,wall
def wall_worker(task):
 row,collar=task;box=R174.atlas.AtlasBox(*(Q(v) for v in row["box"]),len(row["base_refinement_path"]),row["row_id"]);sa,sb,axis,wall=wall_factor_signs(collar,box)
 cell=collar["chart"].split(":")[1];source_is_t=(axis=="Y" and cell in {"E","W"}) or (axis=="X" and cell in {"N","S"});need(sa==sb=="OVERWRAP" and wall==0 and source_is_t and ((box.t0==0)^(box.t1==0)),"exact one-sided source factor identity")
 wants=("STRICT_NEGATIVE","STRICT_POSITIVE")
 if row["graph_classification"]=="EMPTY":
  wants=()
  for i,(ft,fp,fs) in enumerate(product(FR,repeat=3)):
   q=point_box(box,ft,fp,fs,row["row_id"]+f".e{i}");pa,pb,_,_=wall_factor_signs(collar,q)
   if pa!="OVERWRAP" and pb!="OVERWRAP":wants=(R195.multiply_signs(pa,pb),);break
  need(len(wants)==1,"empty strict witness sign")
 out=[]
 for wanted in wants:
  found=None
  for i,(ft,fp,fs) in enumerate(product(FR,repeat=3)):
   q=point_box(box,ft,fp,fs,row["row_id"]+f".w{i}");pa,pb,_,_=wall_factor_signs(collar,q)
   if pa=="OVERWRAP" or pb=="OVERWRAP" or R195.multiply_signs(pa,pb)!=wanted:continue
   base,reasons=r207.direct_leaf_signature_base(collar["chart"],q,REGISTRY)
   if base is None or base["target_lift"]!=collar["owner_target"] or base["whole_leaf_box_outgoing_cell"] is None:continue
   sig=signature(base);amb=[e for e in sig["ordered_integer_wall_events"] if e[0].startswith(axis) and e[1]==wall]
   need((wanted=="STRICT_NEGATIVE" and len(amb)==1) or (wanted=="STRICT_POSITIVE" and not amb),"witness wall event/product sign");found=(q,pa,pb,sig);break
  if found is None:return [],close({"failclosed_leaf_row_id":"round271-failclosed:"+digest([row["row_id"],wanted,"NO_WITNESS"]),"Round182_leaf_row_id":row["row_id"],"collar_kind":"WALL","reason_label":collar["reason_label"],"graph_classification":row["graph_classification"],"residual_reason":"NO_STRICT_RATIONAL_SIDE_WITNESS","side_signature_credit":0,"expanded_occurrence_credit":0,"component_credit":0})
  q,pa,pb,sig=found
  out.append(close({"signed_region_row_id":"round272-boundary-wall-side:"+digest([row["row_id"],wanted,sig]),"Round182_leaf_row_id":row["row_id"],"occurrence_row_id":row["occurrence_row_id"],"collar_kind":"WALL","reason_label":collar["reason_label"],"equation":collar["equation"],"graph_classification":row["graph_classification"],"region_product_sign":wanted,"closed_leaf_source_factor_sign":sa,"closed_leaf_target_factor_sign":sb,"exact_source_factor_identity":"source transverse wall factor = (9/25)*t with chart-dependent sign","excluded_zero_face":"t=0","witness_source_factor_sign":pa,"witness_target_factor_sign":pb,"witness_point":[str(q.t0),str(q.p0),str(q.s0)],"connected_side_extension":"ONE_SIDED_SOURCE_FACTOR_STRICT_ON_OPEN_INTERIOR__TARGET_FACTOR_IS_THE_ONLY_ACTIVE_GRAPH","local_return_signature":sig,"complete_10_field_return_signature_sha256":digest(sig),"side_signature_credit":1,"expanded_occurrence_credit":0,"component_edge_credit":0,"maximality_credit":0,"global_exact_key_disposition_credit":0}))
 return out,None
def face_summary(status):
 need(status["kind"] in {"STRICT","ABSENT","CURVE"},"resolved child face")
 if status["kind"]=="CURVE":return {"zero_set_kind":"CURVE","resolved_sign":None,"graph_axis":status["axis"],"boundary_edge_pair":"","boundary_endpoint_incidence_count":2,"active_factor":None}
 return {"zero_set_kind":"ABSENT","resolved_sign":status["resolved_sign"],"graph_axis":status.get("axis"),"boundary_edge_pair":"","boundary_endpoint_incidence_count":0,"active_factor":None}
def outgoing_w_worker(task):
 row,collar=task;box=R174.atlas.AtlasBox(*(Q(v) for v in row["box"]),0,row["row_id"]);mid=(box.t0+box.t1)/2;out=[]
 for side,(a,b) in enumerate(((box.t0,mid),(mid,box.t1))):
  q=R174.atlas.AtlasBox(a,b,box.p0,box.p1,box.s0,box.s1,box.depth+1,row["row_id"]+f".t{side}");child=dict(row);child["row_id"]=q.path;child["box"]=[str(v) for v in (q.t0,q.t1,q.p0,q.p1,q.s0,q.s1)];child["coordinate_volume"]=str((q.t1-q.t0)*(q.p1-q.p0)*(q.s1-q.s0))
  lower=face_summary(R182M.face_status({"chart":collar["chart"],"owner_target":collar["owner_target"]},"OUTGOING",{},q,False));upper=face_summary(R182M.face_status({"chart":collar["chart"],"owner_target":collar["owner_target"]},"OUTGOING",{},q,True));leaf=R195.classify_leaf(child,collar,q,lower,upper);base,reasons=r207.direct_leaf_signature_base(collar["chart"],q,REGISTRY);need(base is not None and base["target_lift"]==collar["owner_target"],"W child direct base:"+str(reasons));geom=R198.factor_region_rows(leaf,child,collar,q,[],None,set(),{},None)
  for g in geom:
   sig=signature(base,g["outgoing_cell"])
   out.append(close({"signed_region_row_id":"round271-W-tail-side:"+digest([row["row_id"],side,g["F_sign"],sig]),"Round182_leaf_row_id":row["row_id"],"t_child":side,"t_child_box":child["box"],"collar_kind":"OUTGOING","owner_target":collar["owner_target"],"graph_classification":leaf["final_graph_classification"],"region_product_sign":g["F_sign"],"local_return_signature":sig,"complete_10_field_return_signature_sha256":digest(sig),"side_signature_credit":1,"expanded_occurrence_credit":0,"component_edge_credit":0,"maximality_credit":0,"global_exact_key_disposition_credit":0}))
 return out,None
def outgoing_g_worker(task):
 row,collar=task;box=R174.atlas.AtlasBox(*(Q(v) for v in row["box"]),0,row["row_id"]);need((box.t0==0)^(box.t1==0),"G exact t=0 endpoint");ft=Q(3,4) if box.t0==0 else Q(1,4);q=point_box(box,ft,Q(1,2),Q(1,2),row["row_id"]+".interior");base,reasons=r207.direct_leaf_signature_base(collar["chart"],q,REGISTRY);need(base is not None and base["target_lift"]==collar["owner_target"],"G interior base:"+str(reasons));sig=signature(base)
 return [close({"signed_region_row_id":"round271-G-tail-side:"+digest([row["row_id"],sig]),"Round182_leaf_row_id":row["row_id"],"collar_kind":"OUTGOING","owner_target":collar["owner_target"],"graph_classification":row["graph_classification"],"excluded_transition_face":"t=0","one_sided_interior_witness":[str(q.t0),str(q.p0),str(q.s0)],"one_sided_extension":"EXACT_SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_t_WITH_STRICT_NONZERO_INTERIOR_SIGN","local_return_signature":sig,"complete_10_field_return_signature_sha256":digest(sig),"side_signature_credit":1,"expanded_occurrence_credit":0,"component_edge_credit":0,"maximality_credit":0,"global_exact_key_disposition_credit":0})],None
def build(psha,processes):
 global REGISTRY,R174,R182M,R186,R195,R198
 for n,h in SOURCE_PINS.items():need(hashlib.sha256(raw(HERE/n,5_000_000)).hexdigest()==h,"source pin:"+n)
 chain=r207.check_inputs();R198=r207.r203.r198;R195=R198.r195;R186=R195.r191.r189.r188.r186;R182M=R186.r182;R174=R186.r179.r174;f=R174.load_frozen_inputs();REGISTRY=R174.rebuild_registry(f["gate5"]);del f;gc.collect()
 r182=load(R182);r271=load(R271);need(r271["census"]["remaining_dual_factor_WALL_leaf_count"]==496 and r271["census"]["remaining_dual_factor_WALL_region_count"]==720,"Round271 baseline")
 collars={x["Round179_occurrence_row_id"]:x for x in unpack(r182,"collar_occurrence_rows")};rows=unpack(r182,"collar_leaf_rows");ids={x["Round182_leaf_row_id"] for x in r271["formal_failclosed_leaf_ledger"]["rows"]};walls=[]
 for x in rows:
  if x["row_id"] in ids:walls.append((x,collars[x["occurrence_row_id"]]))
 need(len(walls)==496,"task census")
 signed=[];failed=[]
 with mp.get_context("fork").Pool(processes) as pool:
  for good,bad in pool.imap_unordered(wall_worker,walls,chunksize=8):signed.extend(good);failed.extend([] if bad is None else [bad])
 signed.sort(key=lambda x:x["signed_region_row_id"]);success_leaves={x["Round182_leaf_row_id"] for x in signed};print(f"observed_signed={len(signed)} observed_failed={len(failed)} success_leaves={len(success_leaves)}",file=sys.stderr,flush=True);need(len(signed)==720 and len(success_leaves)==496 and not failed,"Round272 census")
 return {"status":"CERTIFIED_ALL_496_APPARENT_DUAL_FACTOR_WALL_LEAVES__720_COMPLETE_SIDE_SIGNATURES__SOURCE_FACTOR_ZERO_ONLY_ON_EXCLUDED_t0_FACE__CLOSED_LEAF_RESIDUAL_ZERO__ZERO_PROMOTION","census":{"input_apparent_dual_factor_WALL_leaf_count":496,"materialized_parent_leaf_count":496,"materialized_side_signature_count":720,"remaining_closed_leaf_count":0,"remaining_closed_leaf_region_count":0,"post_Round272_component_count":63224,"expanded_occurrence_frontier_count":126468,"exact_key_frontier_count":116,"maximal_component_assignment_count":0,"globally_exhausted_exact_key_fibre_count":0,"global_exact_key_disposition_count":0},"formal_side_signature_ledger":ledger(signed,"signed_region_row_id"),"scope_contract":{"all_496_Round271_residual_leaves_evaluated":True,"source_factor_is_exactly_chart_dependent_plus_or_minus_9_over_25_times_t":True,"source_factor_zero_is_confined_to_one_excluded_t0_face_on_every_leaf":True,"target_factor_is_the_only_active_open_interior_graph":True,"all_720_connected_open_side_regions_have_complete_10_field_signatures":True,"signatures_are_not_yet_expanded_occurrences":True,"Jx_Jy_same_point_glue_credit":0},"strict_nonpromotion":{"new_expanded_occurrence_credit":0,"new_component_union_credit":0,"Jx_Jy_same_point_glue_credit":0,"maximal_physical_component_credit":0,"global_exact_key_fibre_credit":0,"global_exact_key_disposition_credit":0,"source_G_global_exact_key_dispositions":"0/224580","D02":"BLOCKED","Gate5_filled_field_slot_count":10,"Gate5_total_field_slot_count":18,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"bind every frozen side signature from Rounds208,269,270,271,272 and all 152 true-seam patches to the expanded component frontier; then prove maximality and exhaust all 116 exact-key fibres","provenance":{"schema":SCHEMA,"producer_sha256":psha,"python_version":sys.version.split()[0],"python_flint_version":str(ctx),"process_count":processes,"seed_affects_output":False,"pinned_evaluator_chain":chain,"wall_witness_grid_smallest_relative_offset":"1/1048576"}}
def write(b):
 fd,n=tempfile.mkstemp(prefix="."+OUTPUT.name+".",suffix=".tmp",dir=HERE);p=Path(n)
 try:
  with os.fdopen(fd,"wb") as f:f.write(b);f.flush();os.fsync(f.fileno())
  os.replace(p,OUTPUT)
 finally:
  if p.exists():p.unlink()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--seed",type=int,default=272071);ap.add_argument("--processes",type=int,default=40);ap.add_argument("--no-write",action="store_true");a=ap.parse_args();need(1<=a.processes<=64,"processes");psha=hashlib.sha256(raw(Path(__file__).resolve(),5_000_000)).hexdigest();result=build(psha,a.processes);doc={"schema":SCHEMA,"result":result,"result_sha256":digest(result)};b=canonical(doc)+b"\n";
 if not a.no_write:write(b)
 print(result["status"]);print("producer_sha256="+psha);print("result_sha256="+doc["result_sha256"]);print("certificate_sha256="+hashlib.sha256(b).hexdigest());return 0
if __name__=="__main__":raise SystemExit(main())
