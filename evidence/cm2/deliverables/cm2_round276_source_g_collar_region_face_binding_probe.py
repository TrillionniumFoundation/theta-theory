#!/usr/bin/env python3
"""Zero-credit census of provenance-safe collar-region face candidates."""
from __future__ import annotations
import collections, hashlib, json
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def load(name):
 d=json.loads((HERE/name).read_bytes());assert d["result_sha256"]==digest(d["result"]);return d["result"]
def unpack(r,t):
 c=r["row_column_schemas"][t];e=r["table_census_and_sha256"][t];assert len(r[t])==e["row_count"] and digest(r[t])==e["rows_sha256"];return [dict(zip(c,x,strict=True)) for x in r[t]]

SOURCES=((208,"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","formal_local_open_3D_signature_ledger","leaf_row_id","region_row_id"),(269,"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","formal_direct_side_signature_ledger","Round182_leaf_row_id","signed_region_row_id"),(270,"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","formal_direct_side_signature_ledger","Round182_leaf_row_id","signed_region_row_id"),(271,"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","formal_side_signature_ledger","Round182_leaf_row_id","signed_region_row_id"),(272,"cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json","formal_side_signature_ledger","Round182_leaf_row_id","signed_region_row_id"))

def main():
 leaf_signatures=collections.defaultdict(dict); source_rows=0; row_ids=set(); physical_aliases=collections.defaultdict(list)
 for rnd,name,ledger,leaf_field,id_field in SOURCES:
  rows=load(name)[ledger]["rows"]
  for row in rows:
   source_rows+=1;rid=row[id_field];assert rid not in row_ids;row_ids.add(rid);sig=row["local_return_signature"];h=row.get("complete_10_field_return_signature_sha256",digest(sig));assert h==digest(sig)
   leaf=row[leaf_field];leaf_signatures[leaf].setdefault(h,{"signature":sig,"rounds":set(),"source_row_ids":[]});node=leaf_signatures[leaf][h];node["rounds"].add(rnd);node["source_row_ids"].append(rid);physical_aliases[(leaf,h)].append(rid)
 assert source_rows==332020
 canonical_nodes=sum(len(x) for x in leaf_signatures.values());assert canonical_nodes==332016
 alias_hist=collections.Counter(len(v) for v in physical_aliases.values());assert alias_hist=={1:332012,2:4}
 r182=load("cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json");leaves=unpack(r182,"collar_leaf_rows");occs=unpack(r182,"collar_occurrence_rows");occ={x["Round179_occurrence_row_id"]:x for x in occs}
 faces=collections.defaultdict(lambda:[[],[]])
 for leaf in leaves:
  nodes=leaf_signatures.get(leaf["row_id"],{});box=tuple(map(Q,leaf["box"]));o=occ[leaf["occurrence_row_id"]]
  for axis in range(3):
   tang=tuple((box[2*i],box[2*i+1]) for i in range(3) if i!=axis)
   for side in (0,1):faces[(o["origin_row_id"],o["chart"],axis,box[2*axis+side])][side].append((leaf["row_id"],tang,nodes))
 candidates=set();leaf_face_pairs=0;full_face_pairs=0
 for (origin,chart,axis,coordinate),(lower,upper) in faces.items():
  for left,left_t,left_nodes in upper:
   for right,right_t,right_nodes in lower:
    if left==right:continue
    overlap=tuple((max(a[0],b[0]),min(a[1],b[1])) for a,b in zip(left_t,right_t,strict=True))
    if not all(a<b for a,b in overlap):continue
    leaf_face_pairs+=1
    if left_t==right_t:full_face_pairs+=1
    for h in set(left_nodes)&set(right_nodes):
     a=(left,h);b=(right,h);lo,hi=sorted((a,b));candidates.add((lo,hi,origin,chart,axis,str(coordinate),tuple((str(a),str(b)) for a,b in overlap)))
 incident={node for edge in candidates for node in edge[:2]}
 direct_ids=set()
 r266=load("cm2_round266_source_g_expanded_curved_face_closure_certificate.json")
 for x in r266["formal_post_Round266_expanded_occurrence_frontier_ledger"]["rows"]:direct_ids.add(x["local_occurrence_row_id"])
 directly_materialized=sum(any(rid in direct_ids for rid in data["source_row_ids"]) for nodes in leaf_signatures.values() for data in nodes.values())
 result={"status":"ROUND276_COLLAR_REGION_FACE_BINDING_PROBE__ZERO_CREDIT","census":{"source_signature_row_count":source_rows,"canonical_collar_region_node_count":canonical_nodes,"artificial_split_alias_reduction_count":source_rows-canonical_nodes,"canonical_node_source_alias_multiplicity_histogram":dict(sorted(alias_hist.items())),"directly_materialized_Round266_occurrence_node_count":directly_materialized,"new_occurrence_candidate_node_count":canonical_nodes-directly_materialized,"positive_common_face_leaf_pair_count":leaf_face_pairs,"exact_full_common_face_leaf_pair_count":full_face_pairs,"same_signature_positive_common_face_candidate_edge_count":len(candidates),"candidate_incident_node_count":len(incident),"candidate_isolated_node_count":canonical_nodes-len(incident)},"candidate_edges_sha256":digest(sorted(candidates,key=str)),"strict_nonpromotion":{"expanded_occurrence_credit":0,"component_edge_credit":0,"maximality_credit":0,"Jx_Jy_same_point_glue_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"independently certify each candidate by a positive-area 2D MATCH face and strict two-sided inward 3D corridors"}
 print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
