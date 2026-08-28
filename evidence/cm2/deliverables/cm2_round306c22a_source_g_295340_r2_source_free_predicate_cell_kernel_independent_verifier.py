#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterator,TextIO
ROOT=Path(__file__).resolve().parent;P="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R182="cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json";R269="cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json";R270="cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json";R271="cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json";R272="cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json";B1="cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz";C16="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";C21C="cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_result.json";PINS={R182:"ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",R269:"472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",R270:"72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",R271:"c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",R272:"16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",B1:"19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96",C16:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",C21C:"d60f0aff6a0baa04b0c37b450caea2d7f83c28c8d7c2db180fd5a5c959baf3b5"};STRICT={"STRICT_NEGATIVE","STRICT_POSITIVE"};LEAF_COLUMNS=("row_id","occurrence_row_id","retained_child_row_id","base_refinement_path","box","coordinate_volume","base_coordinate_area","lower_t_face_status","upper_t_face_status","graph_classification","two_dimensional_graph_sheet_count","one_dimensional_clipping_curve_segment_count","zero_dimensional_boundary_endpoint_incidence_count","closed_3d_side_union_volume","residual_3d_collar_volume");SOURCE_SPECS=((269,R269,"formal_direct_side_signature_ledger",187128),(270,R270,"formal_direct_side_signature_ledger",37712),(271,R271,"formal_side_signature_ledger",70420),(272,R272,"formal_side_signature_ledger",720));READ=1<<18;CAP=10<<20;DEC=json.JSONDecoder()
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def canon(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v):return hashlib.sha256(canon(v)).hexdigest()
def file_hash(path):
 state=hashlib.sha256()
 with path.open("rb")as stream:
  while block:=stream.read(1048576):state.update(block)
 return state.hexdigest()
def check_row(row,label):body=dict(row);need(body.pop("row_sha256",None)==digest(body),label)
def arrays(stream:TextIO,marker:str,anchor:str|None=None)->Iterator[Any]:
 def more(buffer,label):block=stream.read(READ);need(bool(block),label);value=buffer+block;need(len(value.encode())<=CAP,"buffer cap");return value
 def seek(token,buffer):
  while True:
   pos=buffer.find(token)
   if pos>=0:return buffer[pos+len(token):]
   buffer=more(buffer,"missing:"+token);pos=buffer.find(token)
   if pos>=0:return buffer[pos+len(token):]
   buffer=buffer[-max(1,len(token)-1):]
 buffer=""
 if anchor is not None:buffer=seek(anchor,buffer)
 buffer=seek(marker,buffer).lstrip()
 if buffer.startswith(":"):buffer=buffer[1:].lstrip();need(buffer.startswith("["),"array marker");buffer=buffer[1:]
 comma=False
 while True:
  buffer=buffer.lstrip()
  while not buffer:buffer=more(buffer,"truncated").lstrip()
  if buffer[0]=="]":return
  if comma:need(buffer[0]==",","comma");buffer=buffer[1:].lstrip()
  while True:
   try:value,end=DEC.raw_decode(buffer);break
   except json.JSONDecodeError:buffer=more(buffer,"row truncated")
  yield value;buffer=buffer[end:];comma=True
def gz_rows(path):
 with gzip.open(path,"rb")as stream:
  for line in stream:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];row=json.loads(raw);need(canon(row)==raw,"canonical");check_row(row,"row closure");yield row
def source_summary(row,round_no):
 check_row(row,"source closure");signature=row["local_return_signature"];need(digest(signature)==row["complete_10_field_return_signature_sha256"],"signature hash");summary={"source_round":round_no,"source_signature_row_sha256":row["row_sha256"],"Round182_leaf_row_id":row["Round182_leaf_row_id"],"source_chart":signature["source_chart"],"target_lift":signature["target_lift"],"official_key_id":signature["official_key_id"],"official_key_ordinal":signature["official_key_ordinal"],"complete_10_field_return_signature_sha256":row["complete_10_field_return_signature_sha256"],"graph_classification":row["graph_classification"]}
 if round_no in(269,270):need(row["direct_whole_leaf_base_certified"]is True and row["side_specific_signature_credit"]==1,"direct source");authority={"kind":"DIRECT_WHOLE_OPEN_LEAF_FACTOR_SIGN_AUTHORITY","region_factor_sign":row["region_factor_sign"],"HPLUS_sign":row["HPLUS_sign"],"HMINUS_sign":row["HMINUS_sign"],"direct_whole_leaf_base_certified":True}
 elif row.get("t_child")in(0,1):need(row["side_signature_credit"]==1 and row["collar_kind"]=="OUTGOING","W tail");authority={"kind":"R271_W_TAIL_EXACT_CHILD_FACTOR_CELL_AUTHORITY","region_product_sign":row["region_product_sign"],"t_child":row["t_child"],"t_child_box":row["t_child_box"]}
 elif row.get("one_sided_extension")=="EXACT_SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_t_WITH_STRICT_NONZERO_INTERIOR_SIGN":need(row["side_signature_credit"]==1 and row["excluded_transition_face"]=="t=0","G tail");authority={"kind":"R271_G_TAIL_ONE_SIDED_OPEN_INTERIOR_AUTHORITY","excluded_transition_face":row["excluded_transition_face"],"one_sided_extension":row["one_sided_extension"],"one_sided_interior_witness":row["one_sided_interior_witness"]}
 else:
  need(row["side_signature_credit"]==1 and row["collar_kind"]=="WALL"and row["region_product_sign"]in STRICT,"wall source");authority={"kind":"WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_AUTHORITY","equation":row["equation"],"reason_label":row["reason_label"],"region_product_sign":row["region_product_sign"],"witness_source_factor_sign":row["witness_source_factor_sign"],"witness_target_factor_sign":row["witness_target_factor_sign"],"connected_side_extension":row["connected_side_extension"],"witness_point":row["witness_point"]}
  if "exact_source_factor_identity"in row:authority["exact_source_factor_identity"]=row["exact_source_factor_identity"];authority["excluded_zero_face"]=row["excluded_zero_face"]
 return{**summary,"authority_proof":authority}
def build_sources():
 result={};counts=Counter()
 for round_no,name,table,expected in SOURCE_SPECS:
  seen=0
  with(ROOT/name).open("rt")as stream:
   for row in arrays(stream,'"rows"',anchor='"'+table+'"'):
    summary=source_summary(row,round_no);row_id=next(value for key,value in row.items()if key.endswith("signed_region_row_id"));need(row_id not in result,"source duplicate");result[row_id]=summary;seen+=1;counts[round_no]+=1
  need(seen==expected,"source count")
 need(len(result)==295980,"source total");return result,counts
def build_leaves():
 result={}
 with(ROOT/R182).open("rt")as stream:
  for packed in arrays(stream,'"collar_leaf_rows"'):
   need(type(packed)is list and len(packed)==len(LEAF_COLUMNS),"leaf width");row=dict(zip(LEAF_COLUMNS,packed,strict=True));need(row["row_id"]not in result,"leaf duplicate");result[row["row_id"]]={"box":row["box"],"graph_classification":row["graph_classification"],"packed_row_sha256":digest(packed)}
 need(len(result)==202840,"leaf total");return result
def build_members():
 result={}
 for row in gz_rows(ROOT/C16):
  if row["coarse_family"]!="R2":continue
  need(row["member_id"]not in result and row["formal_credit"]["identity"]==1 and row["formal_credit"]["family"]==1,"member");result[row["member_id"]]={"fresh_component_id":row["fresh_component_id"],"official_key_id":row["official_key_id"],"C16a_member_row_sha256":row["row_sha256"]}
 need(len(result)==295336,"member total");return result
def predicate(inventory):
 family=inventory["predicate_family"]
 if family=="OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL":return{"op":"AND","atoms":[{"op":"WHOLE_OPEN_BOX_STRICT_SIGN","factor":"HPLUS","sign":inventory["HPLUS_sign"]},{"op":"WHOLE_OPEN_BOX_STRICT_SIGN","factor":"HMINUS","sign":inventory["HMINUS_sign"]},{"op":"DERIVED_PRODUCT_SIGN","factor":"HPLUS_TIMES_HMINUS","sign":inventory["region_factor_sign"]}]}
 if family=="OUTGOING_G_ONE_SIDED_INTERIOR_CELL":return{"op":"AND","atoms":[{"op":"OPEN_INTERVAL_EXCLUDES_FACE","face":inventory["excluded_transition_face"]},{"op":"SOURCE_AXIS_FACTOR_PROPORTIONAL_TO_T_AND_STRICT_ON_INTERIOR","authority":inventory["one_sided_extension"]}]}
 if family=="OUTGOING_W_TAIL_CHILD_FACTOR_CELL":return{"op":"WHOLE_OPEN_CHILD_BOX_STRICT_SIGN","factor":"TARGET_NORMAL_X_SQUARED_MINUS_TARGET_NORMAL_Y_SQUARED","sign":inventory["region_product_sign"],"t_child":inventory["t_child"]}
 need(family=="WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL","predicate family");return{"op":"AND","atoms":[{"op":"EXACT_FACTOR_EQUATION","equation":inventory["equation"],"reason_label":inventory["reason_label"]},{"op":"ONE_SIDED_SOURCE_FACTOR_STRICT_SIGN","sign":inventory["witness_source_factor_sign"]},{"op":"CONNECTED_TARGET_FACTOR_SIDE_SIGN","sign":inventory["witness_target_factor_sign"]},{"op":"DERIVED_PRODUCT_SIGN","factor":"SOURCE_FACTOR_TIMES_TARGET_FACTOR","sign":inventory["region_product_sign"]}]}
def verify(q):
 for name,claimed in PINS.items():need(file_hash(ROOT/name)==claimed,"pin:"+name)
 raw=(q/R).read_bytes();result=json.loads(raw);need(canon(result)==raw,"result canonical");body=dict(result);claimed=body.pop("result_sha256");need(claimed==digest(body),"result closure");need(result["status"]=="PASS_295340_R2_SOURCE_FREE_INTERVAL_PREDICATE_CELL_EQUALITIES__MEMBER_UNION_CREDIT_DEFERRED"and(result["predicate_cell_support_set_equality_credit"],result["R2_member_count"],result["R2_member_normalized_support_credit"],result["remaining_R2_member_support_debt"])==(295340,295336,0,295336),"result census");need((result["cumulative_global_member_support_credit"],result["remaining_global_member_support_debt"])==(182072,320132)and result["source_round_census"]=={"269":187128,"270":37712,"271":70356,"272":144}and result["source_case_census"]=={"DIRECT_WHOLE_OPEN_LEAF":224840,"G_TAIL_ONE_SIDED_OPEN_INTERIOR":8,"WALL_CONNECTED_STRICT_SIDE":70480,"W_TAIL_EXACT_CHILD_BOX":12},"semantic census");need(result["source_table_full_row_census"]=={"269":187128,"270":37712,"271":70420,"272":720}and result["member_cell_multiplicity_histogram"]=={"1":295332,"2":4}and result["box_relation_census"]=={"WHOLE_LEAF":295328,"W_TAIL_CHILD":12},"source census");need(result["input_pins"]==[{"filename":name,"sha256":value}for name,value in sorted(PINS.items())]and result["strict_nonpromotion"]=={"new_DSU_edges":0,"new_DSU_unions":0,"member_normalized_support":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"boundary");need(result["ledger"]["filename"]==L and result["ledger"]["row_count"]==295340 and result["ledger"]["size"]==(q/L).stat().st_size and result["ledger"]["sha256"]==file_hash(q/L),"ledger descriptor");c21c=json.loads((ROOT/C21C).read_bytes());need(c21c["PRESERVED_semantic_kernel_closed"]is True and c21c["remaining_global_member_support_debt"]==320132,"C21c");sources,source_counts=build_sources();leaves=build_leaves();members=build_members();ledger=iter(gz_rows(q/L));case_counts=Counter();round_counts=Counter();owner_counts=Counter();box_counts=Counter();sequence=hashlib.sha256();seen=set()
 with gzip.open(ROOT/B1,"rt")as stream:
  for ordinal,cell in enumerate(arrays(stream,'"predicate_source_cell_rows"')):
   check_row(cell,"B1 cell");row=next(ledger,None);need(row is not None,"ledger short");cell_id=cell["Round306B1R0_predicate_source_cell_row_id"];need(cell_id not in seen,"cell duplicate");seen.add(cell_id);source=sources[cell["source_signature_row_id"]];leaf=leaves[cell["Round182_leaf_row_id"]];member=members[cell["formal_member_id"]];need(source["source_signature_row_sha256"]==cell["source_signature_row_sha256"]and source["Round182_leaf_row_id"]==cell["Round182_leaf_row_id"]and source["complete_10_field_return_signature_sha256"]==cell["official_key_metadata_only"]["complete_10_field_return_signature_sha256"]and source["official_key_id"]==cell["official_key_metadata_only"]["official_key_id"]==member["official_key_id"]and source["official_key_ordinal"]==cell["official_key_metadata_only"]["official_key_ordinal"],"join");inventory=cell["predicate_source_inventory"];authority=source["authority_proof"];family=inventory["predicate_family"]
   if family=="OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL":need(all(authority[k]==inventory[k]for k in("region_factor_sign","HPLUS_sign","HMINUS_sign")),"direct");case="DIRECT_WHOLE_OPEN_LEAF";box=leaf["box"]
   elif family=="OUTGOING_G_ONE_SIDED_INTERIOR_CELL":need(authority["excluded_transition_face"]==inventory["excluded_transition_face"]and authority["one_sided_extension"]==inventory["one_sided_extension"],"G tail");case="G_TAIL_ONE_SIDED_OPEN_INTERIOR";box=leaf["box"]
   elif family=="OUTGOING_W_TAIL_CHILD_FACTOR_CELL":need(authority["region_product_sign"]==inventory["region_product_sign"]and authority["t_child"]==inventory["t_child"],"W tail");case="W_TAIL_EXACT_CHILD_BOX";box=authority["t_child_box"]
   else:need(family=="WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL"and all(authority[k]==inventory[k]for k in("equation","reason_label","region_product_sign","witness_source_factor_sign","witness_target_factor_sign")),"wall");case="WALL_CONNECTED_STRICT_SIDE";box=leaf["box"]
   need(cell["outer_carrier_box"]==box and all(Q(box[i])<=Q(box[i+1])for i in(0,2,4)),"box");support={"kind":"OPEN_RATIONAL_BOX","coordinate_chart":source["source_chart"],"coordinates":["t","p","s"],"bounds":box};theorem={"kind":"R2_SOURCE_FREE_INTERVAL_PREDICATE_CELL_EQUIVALENCE","case_kind":case,"source_predicate_ast":predicate(inventory),"sealed_source_authority":authority,"source_predicate_is_true_everywhere_on_exact_open_box":True,"source_defined_cell_equals_source_free_open_box":True,"boundary_faces_excluded_by_open_interval_semantics":True};row_body={"schema":"cm2.round306c22a.source-g-295340-r2-source-free-predicate-cell-kernel.v1.row.v1","ordinal":ordinal,"predicate_cell_row_id":cell_id,"owner_member_id":cell["formal_member_id"],"owner_fresh_component_id":member["fresh_component_id"],"support_ast":support,"support_ast_sha256":digest(support),"theorem_ast":theorem,"theorem_ast_sha256":digest(theorem),"source_bindings":{"B1R0_cell_row_sha256":cell["row_sha256"],"source_signature_row_sha256":source["source_signature_row_sha256"],"R182_leaf_packed_row_sha256":leaf["packed_row_sha256"],"C16a_member_row_sha256":member["C16a_member_row_sha256"]},"formal_credit":{"predicate_cell_support_set_equality":1,"member_normalized_support":0,"representation_cover":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};expected={**row_body,"row_sha256":digest(row_body)};need(row==expected,"full row reconstruction");sequence.update(bytes.fromhex(row["row_sha256"]));case_counts[case]+=1;round_counts[cell["source_round"]]+=1;owner_counts[cell["formal_member_id"]]+=1;box_counts["W_TAIL_CHILD"if case=="W_TAIL_EXACT_CHILD_BOX"else"WHOLE_LEAF"]+=1
 need(next(ledger,None)is None and len(seen)==295340 and Counter(owner_counts.values())=={1:295332,2:4},"exhaustion");need(sequence.hexdigest()==result["ledger"]["row_sequence_sha256"]and case_counts=={"DIRECT_WHOLE_OPEN_LEAF":224840,"G_TAIL_ONE_SIDED_OPEN_INTERIOR":8,"W_TAIL_EXACT_CHILD_BOX":12,"WALL_CONNECTED_STRICT_SIDE":70480}and round_counts=={269:187128,270:37712,271:70356,272:144}and box_counts=={"WHOLE_LEAF":295328,"W_TAIL_CHILD":12}and source_counts=={269:187128,270:37712,271:70420,272:720},"replay census");return{"status":"PASS_INDEPENDENT_C22A_295340_SOURCE_FREE_PREDICATE_CELL_EQUALITIES__NO_MEMBER_OR_GLOBAL_PROMOTION","result_sha256":claimed,"rows":295340,"owner_members":295336}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");parser=argparse.ArgumentParser();parser.add_argument("--candidate-dir");args=parser.parse_args();q=ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve();print(canon(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
