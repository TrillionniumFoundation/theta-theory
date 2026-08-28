#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterator,TextIO

ROOT=Path(__file__).resolve().parent
P="cm2_round306c23b_source_g_9404_r292_component_union_and_10252_representation_semantic_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json"
C23AL="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz";C23AR="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_result.json";C23AV="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_verification.json";C23AM="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_manifest.sha256";R292="cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz";FACES="cm2_round299c_source_g_r292_signed_support_face_edge_promotion_classification_inventory.json.gz";SELF="cm2_round299c_source_g_r292_signed_support_face_edge_promotion_self_and_exclusion.json.gz";FRESULT="cm2_round299c_source_g_r292_signed_support_face_edge_promotion_result.json";FVERIFY="cm2_round299c_source_g_r292_signed_support_face_edge_promotion_verification.json";FMAN="cm2_round299c_source_g_r292_signed_support_face_edge_promotion_manifest.sha256";C16M="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz"
PINS={C23AL:"230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",C23AR:"ec6a608a6d929371e19b697b0043081e2e0a6f7c42019379dc036518b416560d",C23AV:"8a09248bf1cc72b196534120843738c45a3481855acb4eaeeb9925d31363574b",C23AM:"5841fd23569669eb97b3563fdf375c1db6ee8f82d87ed2348076db44f13a4bbb",R292:"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",FACES:"2b7afa578911a701bf72e9d04032cd179bec3b7f86163530561d6fe81c53faa3",SELF:"cc9583b5a00db9f4c727c95692db7a356b1d37a443074b28610a3e6822168b96",FRESULT:"7954669c0cc421732b28277ae2c03cacd6fbd70d9c5575765a5c087b7c65c5f4",FVERIFY:"82a96d122f6b3059d390d5864b99ff2d58e2720da9b0677bdd06012adaf02853",FMAN:"62e04cdd7f9c3d2fb865be0a999e1ce5ed1de435151a1b7bb5bba0176709b9b3",C16M:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a"}
READ=1<<18;CAP=10<<20;DEC=json.JSONDecoder()
class E(RuntimeError):pass
def need(value,label):
 if type(value)is not bool or not value:raise E(label)
def canon(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(value):return hashlib.sha256(canon(value)).hexdigest()
def file_hash(path):
 state=hashlib.sha256()
 with path.open("rb")as stream:
  while block:=stream.read(1048576):state.update(block)
 return state.hexdigest()
def check_row(row,label):body=dict(row);need(body.pop("row_sha256",None)==digest(body),label)
def check_result(result,label):body=dict(result);claimed=body.pop("result_sha256",None);need(type(claimed)is str and claimed==digest(body),label);return claimed
def iter_array(stream:TextIO,marker:str)->Iterator[Any]:
 def more(buffer):block=stream.read(READ);need(bool(block),"truncated");out=buffer+block;need(len(out.encode())<=CAP,"buffer cap");return out
 buffer=""
 while marker not in buffer:buffer=more(buffer);buffer=buffer[-max(len(marker)-1,1):]if marker not in buffer else buffer
 buffer=buffer[buffer.find(marker)+len(marker):].lstrip()
 if buffer.startswith(":"):buffer=buffer[1:].lstrip();need(buffer.startswith("["),"array");buffer=buffer[1:]
 comma=False
 while True:
  buffer=buffer.lstrip()
  while not buffer:buffer=more(buffer).lstrip()
  if buffer[0]=="]":return
  if comma:need(buffer[0]==",","comma");buffer=buffer[1:].lstrip()
  while True:
   try:value,end=DEC.raw_decode(buffer);break
   except json.JSONDecodeError:buffer=more(buffer)
  yield value;buffer=buffer[end:];comma=True
def gz_rows(path):
 with gzip.open(path,"rb")as stream:
  for line in stream:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];row=json.loads(raw);need(canon(row)==raw,"canonical");check_row(row,"row closure");yield row
def manifest_has(name,member,sha):return any(len(parts:=line.split(None,1))==2 and parts[0]==sha and Path(parts[1].strip()).name==member for line in(ROOT/name).read_text().splitlines())
def validate_exact_face(row,label):
 axis=row["common_face_axis"];face=row["exact_positive_area_transformed_coordinate_face"]
 need(axis in(0,1,2)and type(face)is list and len(face)==6 and all(type(value)is str for value in face),label)
 exact=[Q(value)for value in face];need(exact[2*axis]==exact[2*axis+1],label);area=Q(1)
 for dimension in range(3):
  if dimension==axis:continue
  width=exact[2*dimension+1]-exact[2*dimension];need(width>0,label);area*=width
 need(area>0 and Q(row["exact_transformed_coordinate_face_area"])==area,label);return face
def validate_sources():
 for name,sha in PINS.items():need(file_hash(ROOT/name)==sha,"pin:"+name)
 c23a=json.loads((ROOT/C23AR).read_bytes());c23a_sha=check_result(c23a,"C23a");v=json.loads((ROOT/C23AV).read_bytes());need(c23a["R292_cell_support_set_equality_credit"]==10252 and c23a["remaining_R292_member_support_debt"]==9404 and v["status"].startswith("PASS_INDEPENDENT_C23A")and manifest_has(C23AM,C23AL,PINS[C23AL])and manifest_has(C23AM,C23AV,PINS[C23AV]),"C23a seal")
 face=json.loads((ROOT/FRESULT).read_bytes());face_sha=check_result(face,"face result");v=json.loads((ROOT/FVERIFY).read_bytes());need(face["status"]=="PASS_FORMAL_R292_SIGNED_FACE_COMPONENT_EDGE_PACKAGE_SEALED"and face["promotion_contract"]["accepted_self_endpoint_no_edge_count"]==2092 and v["status"].startswith("PASS_INDEPENDENT_CACHELESS_ROUND299C")and manifest_has(FMAN,FACES,PINS[FACES])and manifest_has(FMAN,SELF,PINS[SELF])and manifest_has(FMAN,FVERIFY,PINS[FVERIFY]),"face seal")
 return{"C23a_result_object_sha256":c23a_sha,"Round299C_result_object_sha256":face_sha}
def load_cells():
 cells={};owners=defaultdict(list)
 for row in gz_rows(ROOT/C23AL):
  need(row["formal_credit"]=={"R292_cell_support_set_equality":1,"member_normalized_support":0,"typed_representation_semantic_disposition":0},"C23a credit");cell=row["R292_refinement_cell_id"];need(cell not in cells,"cell uniqueness");cells[cell]=row;owners[row["owner_member_id"]].append(cell)
 need(len(cells)==10252 and len(owners)==9404,"cell census");return cells,owners
def load_members():
 members={}
 for row in gz_rows(ROOT/C16M):
  if row["coarse_family"]!="R292":continue
  need(row["formal_credit"]["identity"]==row["formal_credit"]["family"]==1 and row["member_id"]not in members,"member identity");members[row["member_id"]]={"fresh_component_id":row["fresh_component_id"],"base_root_id":row["base_root_id"],"official_key_id":row["official_key_id"],"row_sha256":row["row_sha256"]}
 need(len(members)==9404,"member census");return members
def components():
 with gzip.open(ROOT/R292,"rt")as stream:
  for row in iter_array(stream,'"rows"'):
   check_row(row,"R292 row")
   if "Round292_refined_new_support_component_id"not in row or "member_refinement_cell_ids"not in row:continue
   need(row["one_connected_positive_open_support"]is True and row["strictly_disjoint_from_complete_conditional_base_atom_registry"]is True and row["member_refinement_cell_count"]==len(row["member_refinement_cell_ids"]),"component construction");yield row
def self_rows():
 out={};accepted=0
 with gzip.open(ROOT/SELF,"rt")as stream:
  for row in iter_array(stream,'"rows"'):
   check_row(row,"self row")
   if row["disposition"]!="ACCEPTED_POSITIVE_PATCH_BUT_SELF_ENDPOINT_NO_EDGE":continue
   accepted+=1;source=row["source_Round299_classification_row_id"];need(source not in out and row["decision"]=="ACCEPT_STRICT_POSITIVE_AREA_FACE_PATCH_AND_TWO_SIDED_CORRIDOR"and row["left_formal_occurrence_id"]==row["right_formal_occurrence_id"]and row["formal_component_edge_credit"]==0,"self authority");out[source]={"self_no_edge_row_id":row["Round299C_signed_face_no_edge_row_id"],"self_no_edge_row_sha256":row["row_sha256"],"source_classification_row_sha256":row["source_Round299_classification_row_sha256"],"formal_occurrence_id":row["left_formal_occurrence_id"],"accepted_patch":row["accepted_patch"],"accepted_patch_area":row["accepted_patch_area"],"left_corridor_trace_sha256":row["left_corridor"]["dyadic_inward_shrink_trace_sha256"],"right_corridor_trace_sha256":row["right_corridor"]["dyadic_inward_shrink_trace_sha256"]}
 need(accepted==len(out)==2092,"self census");return out
def internal_faces(cells,owner_cells):
 sealed_rows=self_rows();faces=defaultdict(list);classes=Counter();selected=0
 with gzip.open(ROOT/FACES,"rt")as stream:
  for row in iter_array(stream,'"rows"'):
   check_row(row,"face row");left=row["left_Round292_refinement_cell_id"];right=row["right_Round292_refinement_cell_id"]
   if row["decision"]!="ACCEPT_STRICT_POSITIVE_AREA_FACE_PATCH_AND_TWO_SIDED_CORRIDOR"or left not in cells or right not in cells or cells[left]["owner_member_id"]!=cells[right]["owner_member_id"]:continue
   owner=cells[left]["owner_member_id"];face=validate_exact_face(row,"exact internal face");need(left!=right and row["same_formal_occurrence_endpoint"]is True and row["left_formal_occurrence_id"]==row["right_formal_occurrence_id"]==owner,"internal endpoint")
   sealed=sealed_rows[row["Round299_independent_signed_face_classification_row_id"]];need(sealed["source_classification_row_sha256"]==row["row_sha256"]and sealed["formal_occurrence_id"]==owner,"self join")
   authority={"classification_row_id":row["Round299_independent_signed_face_classification_row_id"],"classification_row_sha256":row["row_sha256"],"self_no_edge_row_id":sealed["self_no_edge_row_id"],"self_no_edge_row_sha256":sealed["self_no_edge_row_sha256"],"left_cell_id":left,"right_cell_id":right,"contact_class":row["contact_class"],"common_face_axis":row["common_face_axis"],"exact_transformed_coordinate_face":face,"accepted_patch":sealed["accepted_patch"],"accepted_patch_area":sealed["accepted_patch_area"],"left_corridor_trace_sha256":sealed["left_corridor_trace_sha256"],"right_corridor_trace_sha256":sealed["right_corridor_trace_sha256"],"two_sided_positive_volume_corridors":True};faces[owner].append(authority);classes[row["contact_class"]]+=1;selected+=1
 need(selected==848 and classes=={"FULL_FULL":716,"DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE":104,"SINGLE_GRAPH":28},"face census")
 for owner,cell_ids in owner_cells.items():
  edges=sorted(faces[owner],key=lambda item:item["classification_row_id"]);parent={cell:cell for cell in cell_ids}
  def find(cell):
   while parent[cell]!=cell:parent[cell]=parent[parent[cell]];cell=parent[cell]
   return cell
  for edge in edges:
   left,right=find(edge["left_cell_id"]),find(edge["right_cell_id"]);need(left!=right,"face cycle");parent[right]=left
  need(len(edges)==len(cell_ids)-1 and len({find(cell)for cell in cell_ids})==1,"owner spanning tree");faces[owner]=edges
 return faces,classes
def verify(candidate):
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"runtime");raw=(candidate/R).read_bytes();result=json.loads(raw);need(canon(result)==raw,"result canonical");claimed=check_result(result,"result closure")
 need(result["status"]=="PASS_9404_R292_MEMBER_SUPPORTS_AND_10252_TYPED_REPRESENTATION_SEMANTICS__R292_CLOSED"and(result["R292_member_count"],result["R292_member_normalized_support_set_equality_credit"],result["R292_remaining_member_support_debt"],result["R292_representation_count"],result["R292_single_cell_representation_set_equality_credit"],result["R292_multicell_representation_exact_subcover_disposition_credit"],result["R292_typed_representation_semantic_credit"],result["R292_remaining_representation_semantic_debt"],result["R292_internal_physical_face_reglue_credit_consumed"])==(9404,9404,0,10252,9124,1128,10252,0,848),"result census")
 need((result["cumulative_global_member_support_credit"],result["remaining_global_member_support_debt"])==(486812,15392)and result["remaining_global_member_debt_by_family"]=={"G2A":5264,"G2B":10128}and result["strict_nonpromotion"]=={"new_DSU_edges":0,"new_DSU_unions":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}and result["input_pins"]==[{"filename":name,"sha256":sha}for name,sha in sorted(PINS.items())],"global boundary");seals=validate_sources()
 cells,owner_cells=load_cells();members=load_members();faces,face_classes=internal_faces(cells,owner_cells);ledger=iter(gz_rows(candidate/L));sequence=hashlib.sha256();member_semantic={};member_hist=Counter();seen_owners=set();ordinal=member_count=0
 for component in components():
  cell_ids=component["member_refinement_cell_ids"];need(bool(cell_ids)and all(cell in cells for cell in cell_ids),"component cells");owner=cells[cell_ids[0]]["owner_member_id"];need(owner not in seen_owners and set(cell_ids)==set(owner_cells[owner])and all(cells[cell]["owner_member_id"]==owner and cells[cell]["R292_local_component_id"]==component["Round292_refined_new_support_component_id"]for cell in cell_ids),"component owner");seen_owners.add(owner);member=members[owner];need(member["fresh_component_id"]==cells[cell_ids[0]]["owner_fresh_component_id"],"fresh member")
  face_rows=faces[owner];cell_refs=[{"cell_id":cell,"C23a_row_sha256":cells[cell]["row_sha256"],"support_ast_sha256":cells[cell]["support_ast_sha256"]}for cell in cell_ids];face_refs=[{"classification_row_id":face["classification_row_id"],"classification_row_sha256":face["classification_row_sha256"],"self_no_edge_row_sha256":face["self_no_edge_row_sha256"]}for face in face_rows];support={"kind":"CONNECTED_REGLUED_FINITE_UNION_OF_T2PS_BRANCH_OPEN_BOXES","cell_supports":cell_refs,"internal_physical_face_reglues":face_refs};theorem={"kind":"R292_COMPONENT_CELL_COMPLEX_EQUALS_MEMBER_NORMALIZED_SUPPORT","sealed_cell_equalities":cell_refs,"sealed_internal_face_authorities":face_rows,"component_construction_row_sha256":component["row_sha256"],"component_declared_one_connected_positive_open_support":True,"internal_face_graph_is_spanning_tree":True,"artificial_partition_faces_are_not_physical_support_boundaries":True,"reglued_cell_complex_equals_exact_member_physical_support":True,"member_physical_support_equals_normalized_support_ast":True}
  body={"schema":"cm2.round306c23b.source-g-9404-r292-component-union-and-10252-representation-semantic-kernel.v1.row.v1","ordinal":ordinal,"row_kind":"R292_MEMBER_NORMALIZED_SUPPORT_SET_EQUALITY","member_id":owner,"fresh_component_id":member["fresh_component_id"],"base_root_id":member["base_root_id"],"official_key_id":member["official_key_id"],"R292_local_component_id":component["Round292_refined_new_support_component_id"],"normalized_support_ast":support,"normalized_support_ast_sha256":digest(support),"member_union_theorem_ast":theorem,"member_union_theorem_ast_sha256":digest(theorem),"source_bindings":{"C16a_member_row_sha256":member["row_sha256"],"R292_component_row_sha256":component["row_sha256"],"C23a_result_object_sha256":seals["C23a_result_object_sha256"],"Round299C_result_object_sha256":seals["Round299C_result_object_sha256"]},"formal_credit":{"member_normalized_support_set_equality":1,"representation_set_equality":0,"exact_subcover_inclusion_disposition":0,"typed_representation_semantic_disposition":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};expected={**body,"row_sha256":digest(body)};actual=next(ledger,None);need(actual==expected,"member row reconstruction");sequence.update(bytes.fromhex(actual["row_sha256"]));member_semantic[owner]=actual["row_sha256"];member_hist[len(cell_ids)]+=1;member_count+=1;ordinal+=1
 need(member_count==len(seen_owners)==len(member_semantic)==9404,"component exhaustion")
 single_eq=multi_subcover=rep_count=0
 for cell in gz_rows(ROOT/C23AL):
  cell_id=cell["R292_refinement_cell_id"];owner=cell["owner_member_id"];count=len(owner_cells[owner]);is_equal=count==1;theorem={"kind":"R292_CELL_REPRESENTATION_TO_OWNER_NORMALIZED_SUPPORT_SEMANTIC_DISPOSITION","C23a_cell_support_row_sha256":cell["row_sha256"],"owner_member_semantic_row_sha256":member_semantic[owner],"owner_component_cell_count":count,"cell_support_equals_owner_normalized_support":is_equal,"cell_support_is_exact_strict_subcover_of_owner_normalized_support":not is_equal};body={"schema":"cm2.round306c23b.source-g-9404-r292-component-union-and-10252-representation-semantic-kernel.v1.row.v1","ordinal":ordinal,"row_kind":"R292_SINGLE_CELL_REPRESENTATION_SET_EQUALITY"if is_equal else"R292_COMPONENT_CELL_EXACT_SUBCOVER_INCLUSION_DISPOSITION","member_id":owner,"fresh_component_id":cell["owner_fresh_component_id"],"representation_id":cell_id,"representation_theorem_ast":theorem,"representation_theorem_ast_sha256":digest(theorem),"source_bindings":{"C23a_cell_row_sha256":cell["row_sha256"],"owner_member_semantic_row_sha256":member_semantic[owner]},"formal_credit":{"member_normalized_support_set_equality":0,"representation_set_equality":1 if is_equal else 0,"exact_subcover_inclusion_disposition":0 if is_equal else 1,"typed_representation_semantic_disposition":1},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};expected={**body,"row_sha256":digest(body)};actual=next(ledger,None);need(actual==expected,"representation row reconstruction");sequence.update(bytes.fromhex(actual["row_sha256"]));single_eq+=int(is_equal);multi_subcover+=int(not is_equal);rep_count+=1;ordinal+=1
 need(next(ledger,None)is None and(ordinal,rep_count,single_eq,multi_subcover)==(19656,10252,9124,1128),"ledger exhaustion");need(member_hist=={1:9124,2:80,3:12,4:88,5:84,10:16},"member histogram")
 need(result["R292_internal_face_contact_class_census"]==dict(face_classes)and result["R292_member_cell_multiplicity_histogram"]=={str(key):value for key,value in sorted(member_hist.items())},"result replay census");descriptor=result["ledger"];need(descriptor["filename"]==L and descriptor["row_count"]==19656 and descriptor["size"]==(candidate/L).stat().st_size and descriptor["sha256"]==file_hash(candidate/L)and descriptor["row_sequence_sha256"]==sequence.hexdigest()and descriptor["order"]=="9404_COMPONENT_ROWS_THEN_10252_C23A_CELL_REPRESENTATION_ROWS","ledger descriptor")
 return{"status":"PASS_INDEPENDENT_C23B_9404_MEMBER_AND_10252_REPRESENTATION_FULL_RECONSTRUCTION__R292_CLOSED_NO_GLOBAL_PROMOTION","result_sha256":claimed,"rows":19656,"member_supports":9404,"representation_semantics":10252,"internal_face_reglues":848}
def main():
 parser=argparse.ArgumentParser();parser.add_argument("--candidate-dir");args=parser.parse_args();candidate=ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve();print(canon(verify(candidate)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
