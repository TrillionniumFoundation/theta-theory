#!/usr/bin/env python3
"""Independently verify Round236 wall closure and root key partitions."""

from __future__ import annotations
import argparse, hashlib, json, os, stat, tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from flint import arb

H=Path(__file__).resolve().parent
OUT=H/"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_verification.json"
P={"cm2_round179_source_g_residual_tube_arrangement_rows.json":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42","cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974","cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json":"6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac","cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json":"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787","cm2_round179_source_g_residual_tube_arrangement.py":"8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab","cm2_round236_source_g_wall_residual_closure_and_root_key_partition.py":"6eb2641df1b64676f145c922dc074d935813e15ce62fe1bee64309da0e509514","cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json":"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"}

def need(x:bool,s:str)->None:
 if not x:raise RuntimeError(s)
def can(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def dg(x:Any)->str:return hashlib.sha256(can(x)).hexdigest()
def raw(n:str)->bytes:
 p=H/n;i=p.lstat();need(stat.S_ISREG(i.st_mode)and not p.is_symlink()and i.st_nlink==1,"regular:"+n);b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==P[n],"pin:"+n);return b
def load(n:str)->dict[str,Any]:
 d=json.loads(raw(n));need(set(d)=={"schema","result","result_sha256"}and dg(d["result"])==d["result_sha256"],"envelope:"+n);return d["result"]
def unpack(d:dict[str,Any],n:str)->list[dict[str,Any]]:
 c=d["row_column_schemas"][n];return[dict(zip(c,r,strict=True))for r in d[n]]
def sig(r:dict[str,Any])->dict[str,Any]:return{"source_chart":r["chart"],"target_lift":r["owner_target"],"ordered_integer_wall_events":r["ordered_integer_wall_events"],"signed_wall_word":r["signed_wall_word"],"roof":r["roof"],"outgoing_cell":r["outgoing_cell"],"target_chart":r["target_chart"],"official_key_row":r["official_key_row"],"official_key_ordinal":r["official_key_ordinal"],"official_key_id":r["official_key_id"]}
def event_sig(base:dict[str,Any],event:list[Any],chart:str,owner:str,reg:dict[str,Any],fn:Any)->dict[str,Any]:
 r=dict(base);r["ordered_integer_wall_events"]=[event];r["signed_wall_word"]=[event[0]];r["roof"]=2;k=fn(chart,owner,(event[0],),reg);r["official_key_row"],r["official_key_ordinal"],r["official_key_id"]=k["row"],k["ordinal"],k["identifier"];return r
def write(b:bytes)->None:
 f,n=tempfile.mkstemp(prefix=".r236.",suffix=".tmp",dir=H);p=Path(n)
 try:
  with os.fdopen(f,"wb")as h:h.write(b);h.flush();os.fsync(h.fileno())
  os.replace(p,OUT)
 finally:
  if p.exists():p.unlink()

def verify()->dict[str,Any]:
 for n in P:raw(n)
 import cm2_round179_source_g_residual_tube_arrangement as r179
 reg=r179.load_inputs()["registry"];a=load("cm2_round179_source_g_residual_tube_arrangement_rows.json");resolved={r["row_id"]:r for r in unpack(a,"resolved_3d_child_rows")};b=load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json");t=b["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"];ints={r["split_interface_id"]:r for r in(dict(zip(t["columns"],x,strict=True))for x in t["rows"])};r234=load("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json");r235=load("cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json");candidate=load("cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json")
 gotd={r["Round234_frontier_row_id"]:r for r in candidate["double_endpoint_partition_rows"]};gotc={r["Round234_frontier_row_id"]:r for r in candidate["crossing_dependency_discharge_rows"]};doubleids={r["Round234_frontier_row_id"]for r in r235["double_endpoint_deferred_rows"]};front={r["frontier_row_id"]:r for r in r234["depth6_frontier_rows"]};need(len(doubleids)==16,"double universe")
 keys:dict[str,set[tuple[int,str]]]=defaultdict(set);pieces:Counter[str]=Counter()
 for r in r234["resolved_descendant_rows"]:s=r["local_return_signature"];keys[r["Round220_split_interface_id"]].add((s["official_key_ordinal"],s["official_key_id"]));pieces[r["Round220_split_interface_id"]]+=1
 for r in r235["single_endpoint_graph_partition_rows"]:
  for n in("event_absent_signature","event_present_signature"):s=r[n];keys[r["Round220_split_interface_id"]].add((s["official_key_ordinal"],s["official_key_id"]))
  pieces[r["Round220_split_interface_id"]]+=2
 for fid in sorted(doubleids):
  r=front[fid];_,axis,wtext=r["reason_labels"][0].split(":");wall=int(wtext);box=r179.box_from(r["box"],r["adaptive_depth"],fid);g=r179.interval_geometry(r["chart"],r["owner_target"],box);sn,tn=(("source_x","hit_x")if axis=="X"else("source_y","hit_y"));need(r179.sign(g[sn][0])==r179.sign(g[tn][0])=="OVERWRAP","double");sd,td=r179.sign(g[sn][1][0]),r179.sign(g[tn][1][0]);need(sd!="OVERWRAP"and td!="OVERWRAP","derivatives");i=ints[r["Round220_split_interface_id"]];sid=i["lower_child_row_id"]if i["lower_child_kind"]=="RESOLVED"else i["upper_child_row_id"];base=sig(resolved[sid]);need(base["ordered_integer_wall_events"]==[],"empty");plus=event_sig(base,[axis+"+",wall],r["chart"],r["owner_target"],reg,r179.r174.exact_key);minus=event_sig(base,[axis+"-",wall],r["chart"],r["owner_target"],reg,r179.r174.exact_key);expected={"double_endpoint_partition_row_id":"round236-double:"+dg(fid),"Round234_frontier_row_id":fid,"Round220_split_interface_id":r["Round220_split_interface_id"],"axis":axis,"wall":wall,"source_factor_strict_t_derivative_sign":sd,"target_factor_strict_t_derivative_sign":td,"same_sign_event_absent_signature":base,"negative_to_positive_signature":plus,"positive_to_negative_signature":minus,"endpoint_graph_union_dimension":2,"endpoint_graph_union_three_dimensional_volume":0,"local_finite_exact_key_partition_credit":1,"whole_root_credit":0};need(gotd.get(fid)==expected,"double row")
  for s in(base,plus,minus):keys[r["Round220_split_interface_id"]].add((s["official_key_ordinal"],s["official_key_id"]));pieces[r["Round220_split_interface_id"]]+=1
 cross=[r for r in r234["depth6_frontier_rows"]if r["reason_labels"][0].startswith("wall_crossing_time_not_strict:")];need(len(cross)==32,"cross universe")
 for r in cross:
  fid=r["frontier_row_id"];_,axis,wtext=r["reason_labels"][0].split(":");wall=int(wtext);box=r179.box_from(r["box"],r["adaptive_depth"],fid);g=r179.interval_geometry(r["chart"],r["owner_target"],box);s=g["source_x"][0]if axis=="X"else g["source_y"][0];f=g["hit_x"][0]if axis=="X"else g["hit_y"][0];ss,fs=r179.sign(s-arb(wall)),r179.sign(f-arb(wall));need({ss,fs}=={"STRICT_NEGATIVE","STRICT_POSITIVE"},"opposite");token=axis+("+"if ss=="STRICT_NEGATIVE"else"-");tm=(arb(wall)-s)/(f-s);i=ints[r["Round220_split_interface_id"]];sid=i["lower_child_row_id"]if i["lower_child_kind"]=="RESOLVED"else i["upper_child_row_id"];base=sig(resolved[sid]);others=[]
  for tok,w in base["ordered_integer_wall_events"]:
   if[tok,w]==[token,wall]:continue
   os=g["source_x"][0]if tok[0]=="X"else g["source_y"][0];of=g["hit_x"][0]if tok[0]=="X"else g["hit_y"][0];others.append((arb(w)-os)/(of-os))
  need(all(bool(tm>x)for x in others),"order");expected={"crossing_dependency_discharge_row_id":"round236-crossing:"+dg(fid),"Round234_frontier_row_id":fid,"Round220_split_interface_id":r["Round220_split_interface_id"],"axis":axis,"wall":wall,"source_endpoint_sign":ss,"target_endpoint_sign":fs,"transition_event":[token,wall],"exact_endpoint_opposition_proves_time_in_open_unit_interval":True,"event_order_position":"STRICT_LAST","strictly_preceding_existing_event_count":len(others),"local_return_signature":base,"local_exact_key_disposition_credit":1,"whole_root_credit":0};need(gotc.get(fid)==expected,"cross row");keys[r["Round220_split_interface_id"]].add((base["official_key_ordinal"],base["official_key_id"]));pieces[r["Round220_split_interface_id"]]+=1
 roots=[]
 for iid in sorted(keys):ks=sorted(keys[iid]);roots.append({"whole_root_partition_row_id":"round236-root:"+dg(iid),"Round220_split_interface_id":iid,"finite_partition_piece_count":pieces[iid],"candidate_exact_key_count":len(ks),"candidate_exact_key_ordinals":[x[0]for x in ks],"candidate_exact_key_ids":[x[1]for x in ks],"positive_volume_and_graph_partition_exhaustive":True,"lower_dimensional_graph_volume_credit":0,"whole_root_local_finite_exact_key_partition_credit":1,"known_block_incidence_credit":0,"global_exact_key_fibre_credit":0})
 need(len(roots)==2640 and candidate["whole_root_finite_key_partition_rows"]==roots,"roots");hist=Counter(r["candidate_exact_key_count"]for r in roots);need(candidate["census"]["whole_root_candidate_key_count_histogram"]=={str(k):v for k,v in sorted(hist.items())}and candidate["census"]["remaining_unclassified_wall_frontier_count"]==0,"census");need(candidate["strict_nonpromotion"]["CM2"]=="NO-GO_FOR_CLAIM","no-go")
 return{"status":"PASS_INDEPENDENT_ROUND236","candidate_sha256":P["cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"],"candidate_result_sha256":dg(candidate),"producer_imported_or_executed":False,"double_endpoint_count":16,"crossing_time_count":32,"whole_root_partition_count":2640,"remaining_unclassified_wall_frontier_count":0,"strict_nonpromotion_reconfirmed":True}

def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--no-write",action="store_true");x=p.parse_args();r=verify();d={"schema":"cm2.round236.source-g-wall-residual-closure-and-root-key-partition.verification.v1","result":r,"result_sha256":dg(r)};b=can(d)+b"\n"
 if not x.no_write:write(b)
 print(r["status"]);print(json.dumps(r,sort_keys=True));print("verification_result_sha256="+d["result_sha256"]);return 0
if __name__=="__main__":raise SystemExit(main())
