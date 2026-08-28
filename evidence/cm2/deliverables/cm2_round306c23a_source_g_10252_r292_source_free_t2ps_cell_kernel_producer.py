#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterator,TextIO
ROOT=Path(__file__).resolve().parent;P="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json"
R287="cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz";R292L="cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz";R292R="cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_result.json";R292V="cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verification.json";R292M="cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_manifest.sha256"
C16M="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";C16R="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";C16RESULT="cm2_round306c16a_source_g_identity_representation_family_replay_result.json";C16V="cm2_round306c16a_source_g_identity_representation_family_replay_verification.json";C16MAN="cm2_round306c16a_source_g_identity_representation_family_replay_manifest.sha256"
C22BR="cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_result.json";C22BV="cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_verification.json";C22BM="cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_manifest.sha256"
PINS={R287:"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",R292L:"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",R292R:"f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",R292V:"7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd",R292M:"4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",C16M:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",C16R:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1",C16RESULT:"85e692b6e6889ab8fe3c74ede8e11d48aae664988ed93da7a139d3d9137599f8",C16V:"1c9a1ff52673a9865741b95b400c23176bb27563644705b637a3609c20fb6436",C16MAN:"597a9a402190989baa72f0e7955be376b3142850695096e2fdc6d651ce3ce7f4",C22BR:"218a64732da853bf426f4882c84633f8421511a3490b2f0b830bed5484d83506",C22BV:"0450bc7a46f681becec30f7c395e55eb4339833ff9104cdbe7b4fa4659b27502",C22BM:"cd6ed594efe7cd24ddc5e267c564ad650f48f3289e06da658337743a1469399e"}
READ=1<<18;CAP=10<<20;DEC=json.JSONDecoder()
class E(RuntimeError):pass
def need(value:bool,label:str)->None:
 if type(value)is not bool or not value:raise E(label)
def canon(value:Any)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(value:Any)->str:return hashlib.sha256(canon(value)).hexdigest()
def file_hash(path:Path)->str:
 state=hashlib.sha256()
 with path.open("rb")as stream:
  while block:=stream.read(1048576):state.update(block)
 return state.hexdigest()
def check_row(row:dict[str,Any],label:str)->None:
 body=dict(row);need(body.pop("row_sha256",None)==digest(body),label)
def check_result(result:dict[str,Any],label:str)->str:
 body=dict(result);claimed=body.pop("result_sha256",None);need(type(claimed)is str and claimed==digest(body),label);return claimed
def iter_array(stream:TextIO,marker:str)->Iterator[Any]:
 def more(buffer:str)->str:
  block=stream.read(READ);need(bool(block),"truncated");out=buffer+block;need(len(out.encode())<=CAP,"buffer cap");return out
 buffer=""
 while marker not in buffer:buffer=more(buffer);buffer=buffer[-max(len(marker)-1,1):]if marker not in buffer else buffer
 buffer=buffer[buffer.find(marker)+len(marker):].lstrip()
 if buffer.startswith(":"):buffer=buffer[1:].lstrip();need(buffer.startswith("["),"array marker");buffer=buffer[1:]
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
def gz_rows(path:Path)->Iterator[dict[str,Any]]:
 with gzip.open(path,"rb")as stream:
  for line in stream:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];row=json.loads(raw);need(canon(row)==raw,"canonical");check_row(row,"row closure");yield row
def manifest_has(name:str,member:str,sha:str)->bool:
 return any(len(parts:=line.split(None,1))==2 and parts[0]==sha and Path(parts[1].strip()).name==member for line in(ROOT/name).read_text().splitlines())
def validate_seals()->dict[str,str]:
 for name,sha in PINS.items():need(file_hash(ROOT/name)==sha,"pin:"+name)
 r292=json.loads((ROOT/R292R).read_bytes());r292_sha=check_result(r292,"R292 result");v=json.loads((ROOT/R292V).read_bytes());need(r292["status"]=="PASS_ZERO_CREDIT__R287_FULL_REGISTRY_OVERLAP_EXHAUSTED"and r292["census"]["uncovered_refinement_cell_count"]==10252 and r292["census"]["refined_strictly_new_support_component_count"]==9404 and v["status"].startswith("PASS_INDEPENDENT_CACHELESS_ROUND292")and manifest_has(R292M,R292L,PINS[R292L])and manifest_has(R292M,R292V,PINS[R292V]),"R292 seal")
 c16=json.loads((ROOT/C16RESULT).read_bytes());c16_sha=check_result(c16,"C16 result");v=json.loads((ROOT/C16V).read_bytes());need(c16["member_census"]["family_counts"]["R292"]==9404 and c16["representation_census"]["family_counts"]["R292"]==10252 and v["status"].startswith("PASS_INDEPENDENT_VERIFIER")and manifest_has(C16MAN,C16M,PINS[C16M])and manifest_has(C16MAN,C16R,PINS[C16R]),"C16 seal")
 c22b=json.loads((ROOT/C22BR).read_bytes());c22b_sha=check_result(c22b,"C22b result");v=json.loads((ROOT/C22BV).read_bytes());need(c22b["R2_remaining_member_support_debt"]==0 and c22b["remaining_global_member_support_debt"]==24796 and v["status"].startswith("PASS_INDEPENDENT_C22B")and manifest_has(C22BM,C22BR,PINS[C22BR])and manifest_has(C22BM,C22BV,PINS[C22BV]),"C22b seal")
 return{"R292_result_object_sha256":r292_sha,"C16_result_object_sha256":c16_sha,"C22b_result_object_sha256":c22b_sha}
def source_index()->tuple[dict[str,dict[str,Any]],Counter[str]]:
 out={};counts=Counter()
 with gzip.open(ROOT/R287,"rt")as stream:
  for row in iter_array(stream,'"region_rows"'):
   check_row(row,"R287 region")
   if row["disposition"]!="ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT":continue
   source_id="WHOLE:"+row["Round275_region_id"];payload={"source_kind":"WHOLE_R275_DISJOINT_SUPPORT_CELL","source_row_id":row["Round287_region_disposition_row_id"],"source_row_sha256":row["row_sha256"],"source_chart":row["source_chart"],"adjacent_chart":row["adjacent_chart"],"owner_target":row["owner_target"],"physical_t_sign":row["physical_t_sign"],"physical_t_square_open_interval":row["physical_t_square_open_interval"],"complete_10_field_return_signature_sha256":row["complete_10_field_return_signature_sha256"],"Round287_potential_new_support_union_id":row["Round287_potential_new_support_union_id"]};need(source_id not in out,"source duplicate");out[source_id]=payload;counts[payload["source_kind"]]+=1
 with gzip.open(ROOT/R287,"rt")as stream:
  for row in iter_array(stream,'"refinement_cell_rows"'):
   check_row(row,"R287 refinement")
   if row["disposition"]!="NONEMPTY_UNCOVERED_SLICE__MEMBER_OF_ONE_PARENT_LOCAL_NEW_SUPPORT_UNION":continue
   source_id=row["Round286_refinement_cell_id"];payload={"source_kind":"R286_NONEMPTY_UNCOVERED_SUPPORT_CELL","source_row_id":row["Round287_refinement_cell_disposition_row_id"],"source_row_sha256":row["row_sha256"],"source_chart":row["source_chart"],"adjacent_chart":row["adjacent_chart"],"owner_target":row["owner_target"],"physical_t_sign":row["physical_t_sign"],"physical_t_square_open_interval":row["physical_t_square_open_interval"],"complete_10_field_return_signature_sha256":row["complete_10_field_return_signature_sha256"],"coordinate_box":row["coordinate_box"],"signed_region_cell_state":row["signed_region_cell_state"]};need(source_id not in out,"source duplicate");out[source_id]=payload;counts[payload["source_kind"]]+=1
 need(len(out)==10668 and counts=={"WHOLE_R275_DISJOINT_SUPPORT_CELL":9128,"R286_NONEMPTY_UNCOVERED_SUPPORT_CELL":1540},"R287 source census");return out,counts
def c16_indices()->tuple[dict[str,dict[str,str]],dict[str,dict[str,str]]]:
 members={};representations={}
 for row in gz_rows(ROOT/C16M):
  if row["coarse_family"]!="R292":continue
  need(row["formal_credit"]["identity"]==row["formal_credit"]["family"]==1,"member identity");members[row["member_id"]]={"fresh_component_id":row["fresh_component_id"],"base_root_id":row["base_root_id"],"official_key_id":row["official_key_id"],"row_sha256":row["row_sha256"]}
 for row in gz_rows(ROOT/C16R):
  if row["coarse_family"]!="R292":continue
  need(row["formal_credit"]["representation_identity"]==row["formal_credit"]["representation_owner_binding"]==1 and row["formal_credit"]["normalized_support"]==0,"representation identity");representations[row["representation_id"]]={"owner_member_id":row["owner_member_id"],"fresh_component_id":row["fresh_component_id"],"base_root_id":row["base_root_id"],"official_key_id":row["official_key_id"],"row_sha256":row["row_sha256"]}
 need(len(members)==9404 and len(representations)==10252,"C16 census");return members,representations
def build(candidate:Path)->dict[str,Any]:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"runtime");seals=validate_seals();sources,source_full_counts=source_index();members,reps=c16_indices();candidate.mkdir(parents=True,exist_ok=True);sequence=hashlib.sha256();owner_counts=Counter();selected_source_counts=Counter();chart_counts=Counter();heterogeneous=Counter();seen=set();ordinal=0
 with(candidate/L).open("wb")as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0)as out:
   with gzip.open(ROOT/R292L,"rt")as stream:
    for row in iter_array(stream,'"rows"'):
     check_row(row,"R292 row");disposition=row.get("disposition")
     if disposition=="EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT":
      heterogeneous["UNCOVERED_CELL"]+=1;cell_id=row["Round292_R287_existing_overlap_refinement_cell_id"];need(cell_id not in seen and cell_id in reps,"cell representation");seen.add(cell_id);rep=reps[cell_id];owner=rep["owner_member_id"];member=members[owner];need((rep["fresh_component_id"],rep["base_root_id"],rep["official_key_id"])==(member["fresh_component_id"],member["base_root_id"],member["official_key_id"]),"fresh identity agreement");source=sources[row["source_Round287_support_cell_id"]];box=row["exact_transformed_open_cell"];need(row["existing_occurrence_occupancy_count"]==0 and row["existing_occurrence_ids"]==[]and row["formal_new_occurrence_credit"]==0,"uncovered boundary");need(row["source_chart"]==source["adjacent_chart"]and row["complete_10_field_return_signature_sha256"]==source["complete_10_field_return_signature_sha256"],"source join");need(all(Q(box[i])<Q(box[i+1])for i in(0,2,4))and Q(box[0])>0,"positive open box");interval=source["physical_t_square_open_interval"];need(Q(interval[0])<=Q(box[0])<Q(box[1])<=Q(interval[1]),"t2 subset");volume=(Q(box[1])-Q(box[0]))*(Q(box[3])-Q(box[2]))*(Q(box[5])-Q(box[4]));need(str(volume)==row["exact_transformed_cell_volume"],"volume")
      support={"kind":"T2PS_BRANCH_OPEN_RATIONAL_BOX","recharted_target_chart":row["source_chart"],"coordinates":["t_squared","p","s"],"bounds":box,"physical_t_sign":source["physical_t_sign"],"TPS_branch_lift_ast":{"t":{"op":"SIGNED_SQRT","sign":source["physical_t_sign"],"argument":"t_squared"},"p":"p","s":"s"}};theorem={"kind":"R292_SOURCE_FREE_UNCOVERED_TRANSFORMED_CELL_EQUIVALENCE","R287_source_classification":source,"sealed_R292_exhaustion":{"result_object_sha256":seals["R292_result_object_sha256"],"independent_verification_sha256":PINS[R292V],"exact_partition_cell_is_uncovered":True,"strictly_disjoint_from_complete_conditional_registry":True},"branch_map_is_analytic_bijection_for_strictly_positive_t_squared_interval":True,"R287_adjacent_chart_equals_R292_recharted_target_chart":True,"source_support_restricted_to_exact_partition_cell_equals_T2PS_branch_open_box":True,"boundary_faces_excluded_by_open_interval_semantics":True};body={"schema":"cm2.round306c23a.source-g-10252-r292-source-free-t2ps-cell-kernel.v1.row.v1","ordinal":ordinal,"R292_refinement_cell_id":cell_id,"R292_local_component_id":row["Round292_refined_new_support_component_id"],"owner_member_id":owner,"owner_fresh_component_id":member["fresh_component_id"],"representation_id":cell_id,"support_ast":support,"support_ast_sha256":digest(support),"theorem_ast":theorem,"theorem_ast_sha256":digest(theorem),"source_bindings":{"R292_row_sha256":row["row_sha256"],"R287_row_sha256":source["source_row_sha256"],"C16a_member_row_sha256":member["row_sha256"],"C16a_representation_row_sha256":rep["row_sha256"],"C22b_result_object_sha256":seals["C22b_result_object_sha256"]},"formal_credit":{"R292_cell_support_set_equality":1,"member_normalized_support":0,"typed_representation_semantic_disposition":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};output={**body,"row_sha256":digest(body)};out.write(canon(output)+b"\n");sequence.update(bytes.fromhex(output["row_sha256"]));owner_counts[owner]+=1;selected_source_counts[source["source_kind"]]+=1;chart_counts[row["source_chart"]]+=1;ordinal+=1
     elif disposition=="EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__NO_NEW_OCCURRENCE_ID":heterogeneous["OCCUPIED_CELL"]+=1
     elif "Round292_refined_new_support_component_id"in row:heterogeneous["COMPONENT_ROW"]+=1
     else:heterogeneous["REGISTRY_OVERLAP_ROW"]+=1
 need(ordinal==len(seen)==len(reps)==10252 and set(seen)==set(reps),"cell exhaustion");hist=Counter(owner_counts.values());need(len(owner_counts)==9404 and hist=={1:9124,2:80,3:12,4:88,5:84,10:16},"owner census");need(selected_source_counts=={"WHOLE_R275_DISJOINT_SUPPORT_CELL":8756,"R286_NONEMPTY_UNCOVERED_SUPPORT_CELL":1496}and chart_counts=={"G:N":2566,"G:S":2566,"G:W":2560,"G:E":2560},"selected source census");need(heterogeneous=={"UNCOVERED_CELL":10252,"OCCUPIED_CELL":1600,"COMPONENT_ROW":9404,"REGISTRY_OVERLAP_ROW":1564},"R292 table census")
 descriptor={"filename":L,"row_count":ordinal,"size":(candidate/L).stat().st_size,"sha256":file_hash(candidate/L),"row_sequence_sha256":sequence.hexdigest()};body={"schema":"cm2.round306c23a.source-g-10252-r292-source-free-t2ps-cell-kernel.v1","status":"PASS_10252_R292_SOURCE_FREE_T2PS_CELL_EQUALITIES__MEMBER_UNION_CREDIT_DEFERRED","R292_cell_support_set_equality_credit":10252,"R292_member_count":9404,"R292_member_normalized_support_credit":0,"remaining_R292_member_support_debt":9404,"R292_representation_count":10252,"R292_typed_representation_semantic_credit":0,"cumulative_global_member_support_credit":477408,"remaining_global_member_support_debt":24796,"remaining_global_member_debt_by_family":{"R292":9404,"G2A":5264,"G2B":10128},"R292_member_cell_multiplicity_histogram":{str(key):value for key,value in sorted(hist.items())},"R292_selected_source_kind_census":dict(selected_source_counts),"R292_source_chart_census":dict(chart_counts),"R292_full_source_kind_census":dict(source_full_counts),"R292_heterogeneous_input_census":dict(heterogeneous),"input_pins":[{"filename":name,"sha256":sha}for name,sha in sorted(PINS.items())],"ledger":descriptor,"strict_nonpromotion":{"new_DSU_edges":0,"new_DSU_unions":0,"member_normalized_support":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"CONSUME_9404_R292_COMPONENT_UNIONS_AND_SEALED_INTERNAL_FACE_REGLUE_AUTHORITY"};result={**body,"result_sha256":digest(body)};(candidate/R).write_bytes(canon(result));return result
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument("--candidate-dir",required=True);args=parser.parse_args();result=build(Path(args.candidate_dir).resolve());print(canon({"status":result["status"],"result_sha256":result["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
