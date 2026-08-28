#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterator,TextIO
ROOT=Path(__file__).resolve().parent;P="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R182="cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json";R269="cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json";R270="cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json";R271="cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json";R272="cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json";B1="cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz";C16="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";C21C="cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_result.json";PINS={R182:"ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",R269:"472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",R270:"72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",R271:"c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",R272:"16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",B1:"19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96",C16:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",C21C:"d60f0aff6a0baa04b0c37b450caea2d7f83c28c8d7c2db180fd5a5c959baf3b5"};STRICT={"STRICT_NEGATIVE","STRICT_POSITIVE"};LEAF_COLUMNS=("row_id","occurrence_row_id","retained_child_row_id","base_refinement_path","box","coordinate_volume","base_coordinate_area","lower_t_face_status","upper_t_face_status","graph_classification","two_dimensional_graph_sheet_count","one_dimensional_clipping_curve_segment_count","zero_dimensional_boundary_endpoint_incidence_count","closed_3d_side_union_volume","residual_3d_collar_volume");SOURCE_SPECS=((269,R269,"formal_direct_side_signature_ledger",187128),(270,R270,"formal_direct_side_signature_ledger",37712),(271,R271,"formal_side_signature_ledger",70420),(272,R272,"formal_side_signature_ledger",720));READ=1<<18;CAP=10<<20;DEC=json.JSONDecoder()
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def h(v):return hashlib.sha256(c(v)).hexdigest()
def fh(q):
 state=hashlib.sha256()
 with q.open("rb")as f:
  while block:=f.read(1048576):state.update(block)
 return state.hexdigest()
def closed(row,label):body=dict(row);need(body.pop("row_sha256",None)==h(body),label)
def iter_array(stream:TextIO,marker:str,anchor:str|None=None)->Iterator[Any]:
 def append(buffer,label):
  block=stream.read(READ);need(bool(block),label);out=buffer+block;need(len(out.encode())<=CAP,"buffer cap");return out
 def seek(token,buffer):
  while True:
   at=buffer.find(token)
   if at>=0:return buffer[at+len(token):]
   buffer=append(buffer,"missing marker:"+token);at=buffer.find(token)
   if at>=0:return buffer[at+len(token):]
   buffer=buffer[-max(1,len(token)-1):]
 buffer=""
 if anchor is not None:buffer=seek(anchor,buffer)
 buffer=seek(marker,buffer);buffer=buffer.lstrip()
 if buffer.startswith(":"):buffer=buffer[1:].lstrip();need(buffer.startswith("["),"marker array");buffer=buffer[1:]
 comma=False
 while True:
  buffer=buffer.lstrip()
  while not buffer:buffer=append(buffer,"truncated array").lstrip()
  if buffer[0]=="]":return
  if comma:need(buffer[0]==",","comma");buffer=buffer[1:].lstrip()
  while True:
   try:value,end=DEC.raw_decode(buffer);break
   except json.JSONDecodeError:buffer=append(buffer,"truncated row")
  yield value;buffer=buffer[end:];comma=True
def gzip_rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   need(line.endswith(b"\n"),"gzip newline");raw=line[:-1];row=json.loads(raw);need(c(row)==raw,"gzip canonical");closed(row,"gzip closure");yield row
def compact_source(row,round_no):
 closed(row,"source closure");signature=row["local_return_signature"];need(h(signature)==row["complete_10_field_return_signature_sha256"],"signature closure");base={"source_round":round_no,"source_signature_row_sha256":row["row_sha256"],"Round182_leaf_row_id":row["Round182_leaf_row_id"],"source_chart":signature["source_chart"],"target_lift":signature["target_lift"],"official_key_id":signature["official_key_id"],"official_key_ordinal":signature["official_key_ordinal"],"complete_10_field_return_signature_sha256":row["complete_10_field_return_signature_sha256"],"graph_classification":row["graph_classification"]}
 if round_no in(269,270):
  need(row["direct_whole_leaf_base_certified"]is True and row["side_specific_signature_credit"]==1,"direct authority");proof={"kind":"DIRECT_WHOLE_OPEN_LEAF_FACTOR_SIGN_AUTHORITY","region_factor_sign":row["region_factor_sign"],"HPLUS_sign":row["HPLUS_sign"],"HMINUS_sign":row["HMINUS_sign"],"direct_whole_leaf_base_certified":True}
 elif row.get("t_child")in(0,1):
  need(row["side_signature_credit"]==1 and row["collar_kind"]=="OUTGOING","W-tail authority");proof={"kind":"R271_W_TAIL_EXACT_CHILD_FACTOR_CELL_AUTHORITY","region_product_sign":row["region_product_sign"],"t_child":row["t_child"],"t_child_box":row["t_child_box"]}
 elif row.get("one_sided_extension")=="EXACT_SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_t_WITH_STRICT_NONZERO_INTERIOR_SIGN":
  need(row["side_signature_credit"]==1 and row["excluded_transition_face"]=="t=0","G-tail authority");proof={"kind":"R271_G_TAIL_ONE_SIDED_OPEN_INTERIOR_AUTHORITY","excluded_transition_face":row["excluded_transition_face"],"one_sided_extension":row["one_sided_extension"],"one_sided_interior_witness":row["one_sided_interior_witness"]}
 else:
  need(row["side_signature_credit"]==1 and row["collar_kind"]=="WALL"and row["region_product_sign"]in STRICT,"wall authority");proof={"kind":"WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_AUTHORITY","equation":row["equation"],"reason_label":row["reason_label"],"region_product_sign":row["region_product_sign"],"witness_source_factor_sign":row["witness_source_factor_sign"],"witness_target_factor_sign":row["witness_target_factor_sign"],"connected_side_extension":row["connected_side_extension"],"witness_point":row["witness_point"]}
  if "exact_source_factor_identity"in row:proof["exact_source_factor_identity"]=row["exact_source_factor_identity"];proof["excluded_zero_face"]=row["excluded_zero_face"]
 return{**base,"authority_proof":proof}
def source_index():
 out={};counts=Counter()
 for round_no,name,table,expected in SOURCE_SPECS:
  seen=0
  with(ROOT/name).open("rt",encoding="utf-8")as f:
   for row in iter_array(f,'"rows"',anchor='"'+table+'"'):
    compact=compact_source(row,round_no);row_id=next(value for key,value in row.items()if key.endswith("signed_region_row_id"));need(row_id not in out,"source duplicate");out[row_id]=compact;seen+=1;counts[round_no]+=1
  need(seen==expected,"source census:"+str(round_no))
 need(len(out)==295980,"source total");return out,counts
def leaf_index():
 out={};seen=0
 with(ROOT/R182).open("rt",encoding="utf-8")as f:
  for packed in iter_array(f,'"collar_leaf_rows"'):
   need(type(packed)is list and len(packed)==len(LEAF_COLUMNS),"leaf width");row=dict(zip(LEAF_COLUMNS,packed,strict=True));need(row["row_id"]not in out,"leaf duplicate");out[row["row_id"]]={"box":row["box"],"graph_classification":row["graph_classification"],"packed_row_sha256":h(packed)};seen+=1
 need(seen==202840,"leaf census");return out
def member_index():
 out={};seen=0
 for row in gzip_rows(ROOT/C16):
  if row["coarse_family"]!="R2":continue
  need(row["member_id"]not in out and row["formal_credit"]["identity"]==1 and row["formal_credit"]["family"]==1,"member authority");out[row["member_id"]]={"fresh_component_id":row["fresh_component_id"],"official_key_id":row["official_key_id"],"C16a_member_row_sha256":row["row_sha256"]};seen+=1
 need(seen==len(out)==295336,"member census");return out
def predicate_ast(inventory):
 family=inventory["predicate_family"]
 if family=="OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL":return{"op":"AND","atoms":[{"op":"WHOLE_OPEN_BOX_STRICT_SIGN","factor":"HPLUS","sign":inventory["HPLUS_sign"]},{"op":"WHOLE_OPEN_BOX_STRICT_SIGN","factor":"HMINUS","sign":inventory["HMINUS_sign"]},{"op":"DERIVED_PRODUCT_SIGN","factor":"HPLUS_TIMES_HMINUS","sign":inventory["region_factor_sign"]}]}
 if family=="OUTGOING_G_ONE_SIDED_INTERIOR_CELL":return{"op":"AND","atoms":[{"op":"OPEN_INTERVAL_EXCLUDES_FACE","face":inventory["excluded_transition_face"]},{"op":"SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_T_AND_STRICT_ON_INTERIOR","authority":inventory["one_sided_extension"]}]}
 if family=="OUTGOING_W_TAIL_CHILD_FACTOR_CELL":return{"op":"WHOLE_OPEN_CHILD_BOX_STRICT_SIGN","factor":"TARGET_NORMAL_X_SQUARED_MINUS_TARGET_NORMAL_Y_SQUARED","sign":inventory["region_product_sign"],"t_child":inventory["t_child"]}
 need(family=="WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL","predicate family");return{"op":"AND","atoms":[{"op":"EXACT_FACTOR_EQUATION","equation":inventory["equation"],"reason_label":inventory["reason_label"]},{"op":"ONE_SIDED_SOURCE_FACTOR_STRICT_SIGN","sign":inventory["witness_source_factor_sign"]},{"op":"CONNECTED_TARGET_FACTOR_SIDE_SIGN","sign":inventory["witness_target_factor_sign"]},{"op":"DERIVED_PRODUCT_SIGN","factor":"SOURCE_FACTOR_TIMES_TARGET_FACTOR","sign":inventory["region_product_sign"]}]}
def build(q):
 for name,digest in PINS.items():need(fh(ROOT/name)==digest,"pin:"+name)
 c21c=json.loads((ROOT/C21C).read_bytes());need(c21c["PRESERVED_semantic_kernel_closed"]is True and c21c["remaining_global_member_support_debt"]==320132,"C21c boundary");sources,source_counts=source_index();leaves=leaf_index();members=member_index();q.mkdir(parents=True,exist_ok=True);case_counts=Counter();round_counts=Counter();owner_counts=Counter();box_relations=Counter();seen_cells=set();sequence=hashlib.sha256();row_count=0
 with(q/L).open("wb")as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0)as out:
   with gzip.open(ROOT/B1,"rt",encoding="utf-8")as f:
    for cell in iter_array(f,'"predicate_source_cell_rows"'):
     closed(cell,"B1 cell");cell_id=cell["Round306B1R0_predicate_source_cell_row_id"];need(cell_id not in seen_cells,"cell duplicate");seen_cells.add(cell_id);source=sources[cell["source_signature_row_id"]];leaf=leaves[cell["Round182_leaf_row_id"]];member=members[cell["formal_member_id"]];need(source["source_signature_row_sha256"]==cell["source_signature_row_sha256"]and source["Round182_leaf_row_id"]==cell["Round182_leaf_row_id"]and source["complete_10_field_return_signature_sha256"]==cell["official_key_metadata_only"]["complete_10_field_return_signature_sha256"]and source["official_key_id"]==cell["official_key_metadata_only"]["official_key_id"]==member["official_key_id"]and source["official_key_ordinal"]==cell["official_key_metadata_only"]["official_key_ordinal"],"source join");inventory=cell["predicate_source_inventory"];proof=source["authority_proof"];family=inventory["predicate_family"]
     if family=="OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL":need({k:proof[k]for k in("region_factor_sign","HPLUS_sign","HMINUS_sign")}=={k:inventory[k]for k in("region_factor_sign","HPLUS_sign","HMINUS_sign")},"direct predicate");case="DIRECT_WHOLE_OPEN_LEAF";expected_box=leaf["box"]
     elif family=="OUTGOING_G_ONE_SIDED_INTERIOR_CELL":need(proof["excluded_transition_face"]==inventory["excluded_transition_face"]and proof["one_sided_extension"]==inventory["one_sided_extension"],"G-tail predicate");case="G_TAIL_ONE_SIDED_OPEN_INTERIOR";expected_box=leaf["box"]
     elif family=="OUTGOING_W_TAIL_CHILD_FACTOR_CELL":need(proof["region_product_sign"]==inventory["region_product_sign"]and proof["t_child"]==inventory["t_child"],"W-tail predicate");case="W_TAIL_EXACT_CHILD_BOX";expected_box=proof["t_child_box"]
     else:need(family=="WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL"and all(proof[k]==inventory[k]for k in("equation","reason_label","region_product_sign","witness_source_factor_sign","witness_target_factor_sign")),"wall predicate");case="WALL_CONNECTED_STRICT_SIDE";expected_box=leaf["box"]
     need(cell["outer_carrier_box"]==expected_box and all(Q(expected_box[i])<=Q(expected_box[i+1])for i in(0,2,4)),"exact box");support={"kind":"OPEN_RATIONAL_BOX","coordinate_chart":source["source_chart"],"coordinates":["t","p","s"],"bounds":expected_box};theorem={"kind":"R2_SOURCE_FREE_INTERVAL_PREDICATE_CELL_EQUIVALENCE","case_kind":case,"source_predicate_ast":predicate_ast(inventory),"sealed_source_authority":proof,"source_predicate_is_true_everywhere_on_exact_open_box":True,"source_defined_cell_equals_source_free_open_box":True,"boundary_faces_excluded_by_open_interval_semantics":True};body={"schema":"cm2.round306c22a.source-g-295340-r2-source-free-predicate-cell-kernel.v1.row.v1","ordinal":row_count,"predicate_cell_row_id":cell_id,"owner_member_id":cell["formal_member_id"],"owner_fresh_component_id":member["fresh_component_id"],"support_ast":support,"support_ast_sha256":h(support),"theorem_ast":theorem,"theorem_ast_sha256":h(theorem),"source_bindings":{"B1R0_cell_row_sha256":cell["row_sha256"],"source_signature_row_sha256":source["source_signature_row_sha256"],"R182_leaf_packed_row_sha256":leaf["packed_row_sha256"],"C16a_member_row_sha256":member["C16a_member_row_sha256"]},"formal_credit":{"predicate_cell_support_set_equality":1,"member_normalized_support":0,"representation_cover":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};row={**body,"row_sha256":h(body)};out.write(c(row)+b"\n");sequence.update(bytes.fromhex(row["row_sha256"]));row_count+=1;case_counts[case]+=1;round_counts[cell["source_round"]]+=1;owner_counts[cell["formal_member_id"]]+=1;box_relations["W_TAIL_CHILD"if case=="W_TAIL_EXACT_CHILD_BOX"else"WHOLE_LEAF"]+=1
 need(row_count==len(seen_cells)==295340 and len(owner_counts)==295336 and Counter(owner_counts.values())=={1:295332,2:4},"cell/member census");need(round_counts=={269:187128,270:37712,271:70356,272:144}and case_counts=={"DIRECT_WHOLE_OPEN_LEAF":224840,"G_TAIL_ONE_SIDED_OPEN_INTERIOR":8,"W_TAIL_EXACT_CHILD_BOX":12,"WALL_CONNECTED_STRICT_SIDE":70480}and box_relations=={"WHOLE_LEAF":295328,"W_TAIL_CHILD":12},"case census");descriptor={"filename":L,"row_count":row_count,"size":(q/L).stat().st_size,"sha256":fh(q/L),"row_sequence_sha256":sequence.hexdigest()};body={"schema":"cm2.round306c22a.source-g-295340-r2-source-free-predicate-cell-kernel.v1","status":"PASS_295340_R2_SOURCE_FREE_INTERVAL_PREDICATE_CELL_EQUALITIES__MEMBER_UNION_CREDIT_DEFERRED","predicate_cell_support_set_equality_credit":295340,"R2_member_count":295336,"R2_member_normalized_support_credit":0,"remaining_R2_member_support_debt":295336,"cumulative_global_member_support_credit":182072,"remaining_global_member_support_debt":320132,"source_round_census":dict(round_counts),"source_case_census":dict(case_counts),"source_table_full_row_census":dict(source_counts),"member_cell_multiplicity_histogram":{"1":295332,"2":4},"box_relation_census":dict(box_relations),"input_pins":[{"filename":name,"sha256":digest}for name,digest in sorted(PINS.items())],"ledger":descriptor,"strict_nonpromotion":{"new_DSU_edges":0,"new_DSU_unions":0,"member_normalized_support":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"CONSUME_CELL_EQUALITIES_IN_295336_MEMBER_UNIONS_AND_FOUR_SEALED_W_TAIL_REGLUE_THEOREMS"};result={**body,"result_sha256":h(body)};(q/R).write_bytes(c(result));return result
def main():
 parser=argparse.ArgumentParser();parser.add_argument("--candidate-dir",required=True);args=parser.parse_args();result=build(Path(args.candidate_dir).resolve());print(c({"status":result["status"],"result_sha256":result["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
