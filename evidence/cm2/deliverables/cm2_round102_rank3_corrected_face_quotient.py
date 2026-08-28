#!/usr/bin/env python3
"""Assemble the corrected endpoint-complete rank-three physical face quotient."""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from flint import ctx
import cm2_round89_rank3_projective_gap_closure_cert as round89
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent
R87=HERE/"cm2-round87-rank3-port-event-continuation-2026-07-22.json"
R99=HERE/"cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
R100=HERE/"cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json"
R101=HERE/"cm2-round101-rank3-eight-ray-source-grazing-closure-2026-07-22.json"
PINS={R87.name:"f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",R99.name:"e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",R100.name:"097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",R101.name:"df29ea8467c09351276a40b38424d6c9effc763f287815e7bac67829bca58172"}
SCHEMA="cm2.round102.rank3-corrected-face-quotient.v1";PRECISION_BITS=512
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(precision_bits=PRECISION_BITS):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin:{n}")
 old=json.loads(R87.read_text())["result"]["port_event_rows"];by_id={r["registered_port_id"]:r for r in old}
 ids=set(json.loads(R99.read_text())["result"]["corrected_locally_physical_registered_port_ids"]);physical={p:by_id[p] for p in ids}
 f100=json.loads(R100.read_text())["result"];f101=json.loads(R101.read_text())["result"]
 source={(tuple(r["branch_key"]),r["projective_end"]):r for r in f100["source_cap_rows"]}
 grazing={(tuple(r["branch_key"]),r["projective_end"]):r for r in f101["ray_rows"]}
 _,pairs=round89.load();registered={frozenset(r["registered_elementary_arc_endpoint_port_ids"]):r for r in pairs}
 gaps={frozenset((r["left_registered_port_id"],r["right_registered_port_id"])):r for r in f100["gap_rows"]}
 grouped=defaultdict(list)
 for p,r in physical.items():grouped[round89.key(r)].append(p)
 faces=[];links=[];endpoints=[]
 for rank,branch in enumerate(sorted(grouped),1):
  ports=grouped[branch];ports.sort(key=lambda p:float(round89.qball(physical[p]).mid()))
  face_id="physical-s0-rank3-corrected-face:"+digest({"branch_key":list(branch),"ordered_ports":ports})
  face_links=[]
  for index,(a,b) in enumerate(zip(ports,ports[1:])):
   pair=frozenset((a,b))
   if pair in registered:kind="REGISTERED_PHYSICAL_ARC";evidence=registered[pair]["physical_root_component_id"]
   elif pair in gaps:kind="IMMUTABLE_CERTIFIED_INTERIOR_GAP";evidence=gaps[pair]["immutable_candidate_reaudit_method"]+":"+gaps[pair].get("certified_tube_boxes_sha256",gaps[pair].get("tracked_boxes_sha256"))
   else:raise RuntimeError("missing consecutive link")
   link={"face_id":face_id,"link_rank":index+1,"left_registered_port_id":a,"right_registered_port_id":b,"link_type":kind,"evidence_id":evidence};links.append(link);face_links.append(link)
  face_endpoints=[]
  for side in ("LEFT_PROJECTIVE_END","RIGHT_PROJECTIVE_END"):
   key=(branch,side)
   if key in source:
    row=source[key];endpoint={"face_id":face_id,"projective_end":side,"endpoint_type":"REGISTERED_SOURCE_CAP","endpoint_id":row["registered_source_port_id"],"mated_registered_port_id":row["mated_physical_port_id"]}
   elif key in grazing:
    row=grazing[key];endpoint={"face_id":face_id,"projective_end":side,"endpoint_type":"SOURCE_GRAZING","endpoint_id":"source-grazing:"+digest({"branch":list(branch),"side":side,"bracket":row["terminal_event_parameter_bracket"]}),"mated_registered_port_id":ports[0] if side.startswith("LEFT") else ports[-1],"terminal_event_parameter_bracket":row["terminal_event_parameter_bracket"],"adjacent_source_chart":row["adjacent_source_chart"]}
   else:raise RuntimeError("missing face endpoint")
   endpoints.append(endpoint);face_endpoints.append(endpoint)
  faces.append({"face_rank":rank,"face_id":face_id,"source_core_index":branch[0],"second_selected_target_id":branch[1],"third_candidate_id":branch[2],"signed_transverse_tangency_factor_sign":branch[3],"ordered_registered_port_count":len(ports),"ordered_registered_port_ids":ports,"ordered_registered_port_ids_sha256":digest(ports),"interior_link_count":len(face_links),"registered_arc_link_count":sum(x["link_type"]=="REGISTERED_PHYSICAL_ARC" for x in face_links),"certified_gap_link_count":sum(x["link_type"]=="IMMUTABLE_CERTIFIED_INTERIOR_GAP" for x in face_links),"endpoint_type_pair":[x["endpoint_type"] for x in face_endpoints],"endpoint_ids":[x["endpoint_id"] for x in face_endpoints],"endpoint_complete":True})
 endpoint_hist=Counter(e["endpoint_type"] for e in endpoints);pair_hist=Counter(" + ".join(sorted(f["endpoint_type_pair"])) for f in faces)
 result={"precision_bits":precision_bits,"corrected_rank3_physical_face_count":len(faces),"corrected_face_registered_port_count":sum(f["ordered_registered_port_count"] for f in faces),"corrected_face_interior_link_count":len(links),"registered_physical_arc_link_count":sum(x["link_type"]=="REGISTERED_PHYSICAL_ARC" for x in links),"immutable_certified_gap_link_count":sum(x["link_type"]=="IMMUTABLE_CERTIFIED_INTERIOR_GAP" for x in links),"face_endpoint_count":len(endpoints),"endpoint_type_histogram":dict(sorted(endpoint_hist.items())),"face_endpoint_pair_histogram":dict(sorted(pair_hist.items())),"unmatched_registered_port_count":0,"unmatched_face_endpoint_count":0,"remaining_geometric_residual_count":0,"face_rows":faces,"face_rows_sha256":digest(faces),"interior_link_rows":links,"interior_link_rows_sha256":digest(links),"endpoint_incidence_rows":endpoints,"endpoint_incidence_rows_sha256":digest(endpoints),"strict_scope":"complete corrected rank-three physical-face quotient and endpoint incidence ledger assembled from immutable-candidate certified chains","strict_nonclaims":["return-map RN fields are not derived by this topological quotient","Gate5 block installation remains downstream"],"upstream_pins":PINS}
 if (len(faces),sum(f["ordered_registered_port_count"] for f in faces),len(links),len(endpoints))!=(12,120,108,24):raise RuntimeError("quotient accounting")
 if endpoint_hist!=Counter({"REGISTERED_SOURCE_CAP":16,"SOURCE_GRAZING":8}) or pair_hist!=Counter({"REGISTERED_SOURCE_CAP + SOURCE_GRAZING":8,"REGISTERED_SOURCE_CAP + REGISTERED_SOURCE_CAP":4}):raise RuntimeError("endpoint accounting")
 if sum(x["link_type"]=="REGISTERED_PHYSICAL_ARC" for x in links)!=52 or sum(x["link_type"]=="IMMUTABLE_CERTIFIED_INTERIOR_GAP" for x in links)!=56:raise RuntimeError("link accounting")
 result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--precision-bits",type=int,default=PRECISION_BITS);a=p.parse_args();print(json.dumps(build(a.precision_bits),sort_keys=True,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
