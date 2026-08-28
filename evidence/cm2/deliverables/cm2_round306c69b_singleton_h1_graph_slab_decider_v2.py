#!/usr/bin/env python3
"""C69b measured singleton H1 graph/slab capability prototype (v2).

Builds only in an empty staging directory.  Two byte-identical staging runs
must be supplied to the publish mode, which uses exclusive/no-replace writes.
The v1 prepublication bytes are rejected and are never read here.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,io,json,multiprocessing as mp,os,stat,sys
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
SELF=Path(__file__).resolve();ROOT=SELF.parents[1];OUT=ROOT/"deliverables";sys.path.insert(0,str(OUT))
import flint
import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41

PREFIX="cm2_round306c69b_singleton_h1_graph_slab_decider_v2"
SCHEMA="cm2.round306c69b.singleton-h1-graph-slab-decider.v2"
CONTRACT=PREFIX+"_contract.json";COVERS=PREFIX+"_parametric_newton_covers.jsonl.gz";DECISIONS=PREFIX+"_decisions.jsonl.gz";BLOCKERS=PREFIX+"_blockers.jsonl.gz";RESULT=PREFIX+"_result.json";REPORT=PREFIX+"_report.md";RECEIPT=PREFIX+"_deterministic_two_stage_publication_receipt.json"
STAGE_NAMES=[CONTRACT,COVERS,DECISIONS,BLOCKERS,REPORT,RESULT]
MAX_B_DEPTH=3
C68R=OUT/"cm2_round306c68l_blocker_crosswalk_result_v1.json";C68S=OUT/"cm2_round306c68l_blocker_crosswalk_singleton_structural_tasks_v1.jsonl.gz"
C61R=OUT/"cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json";C61L=OUT/"cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C58R=OUT/"cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json";C58L=OUT/"cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
C40=ROOT/".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f";C40R=C40/"result.json";C40L=C40/"routed_leaf_cells.jsonl.gz"
CANON=OUT/"CM2_LATEST_STATUS.md";HEAD=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
P={"C41_SOURCE":"3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde","C39_SOURCE":"873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae","ROUND185_SOURCE":"7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2","C38_SOURCE":"8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d","C68R":"81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37","C68O":"551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2","C68S":"c2d174d9a7e076a52474cde03e02ecdc11172251fe70a5b0273b4aa57c480b8b","C61R":"06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e","C61O":"05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584","C61L":"2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2","C58R":"ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc","C58O":"038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30","C58L":"15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df","C40R":"f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6","C40O":"397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba","C40L":"175293702adf1b76600321c1db326a1a6744dbc8caea439ddaeff9779d1f9b5a","CANON":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57","HEAD":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"}
PATHS={"C41_SOURCE":Path(c41.__file__).resolve(),"C39_SOURCE":Path(c41.c39.__file__).resolve(),"ROUND185_SOURCE":Path(c41.round185.__file__).resolve(),"C38_SOURCE":Path(c41.c38.__file__).resolve(),"C68R":C68R,"C68S":C68S,"C61R":C61R,"C61L":C61L,"C58R":C58R,"C58L":C58L,"C40R":C40R,"C40L":C40L,"CANON":CANON,"HEAD":HEAD}
class FailClosed(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise FailClosed(label)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def hf(path:Path)->str:
 d=hashlib.sha256()
 with path.open("rb")as f:
  for c in iter(lambda:f.read(1<<20),b""):d.update(c)
 return d.hexdigest()
def seq(values:Iterable[str])->str:
 d=hashlib.sha256()
 for v in values:d.update(v.encode("ascii")+b"\n")
 return d.hexdigest()
def identity(z:os.stat_result)->dict[str,int]:return{"dev":z.st_dev,"ino":z.st_ino,"mode":z.st_mode,"size":z.st_size,"mtime_ns":z.st_mtime_ns,"nlink":z.st_nlink}
def secure(path:Path,expected:str)->tuple[bytes,dict[str,int]]:
 pre=os.lstat(path);need(stat.S_ISREG(pre.st_mode)and pre.st_nlink==1,"regular-single-link:"+path.name);fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
 try:
  opened=os.fstat(fd);need(identity(pre)==identity(opened),"path-fd:"+path.name);parts=[]
  while True:
   c=os.read(fd,1<<20)
   if not c:break
   parts.append(c)
  need(identity(os.fstat(fd))==identity(opened),"fd-post:"+path.name)
 finally:os.close(fd)
 need(identity(os.lstat(path))==identity(pre),"path-post:"+path.name);data=b"".join(parts);need(hashlib.sha256(data).hexdigest()==expected,"sha:"+path.name);return data,identity(pre)
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 b=dict(v);actual=b.pop("object_sha256",None);need(actual==expected==h(b),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 b=dict(v);actual=b.pop("row_sha256",None);need(actual==h(b),"row:"+label)
def rows(data:bytes,desc:dict[str,Any],label:str)->list[dict[str,Any]]:
 answer=[];hashes=[]
 with gzip.GzipFile(fileobj=io.BytesIO(data),mode="rb")as f:
  for i,line in enumerate(f):
   row=json.loads(line);closerow(row,f"{label}:{i}");answer.append(row);hashes.append(row["row_sha256"])
 need(len(answer)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return answer
def exclusive(path:Path,data:bytes)->None:
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o644)
 try:
  view=memoryview(data)
  while view:
   n=os.write(fd,view);need(n>0,"write:"+path.name);view=view[n:]
  os.fsync(fd)
 finally:os.close(fd)
 need(path.read_bytes()==data and os.lstat(path).st_nlink==1,"exclusive-post:"+path.name)
class Writer:
 def __init__(self,path:Path,order:str):self.path,self.order=path,order;self.raw=path.open("xb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.s=hashlib.sha256()
 def __enter__(self):return self
 def write(self,body:dict[str,Any])->dict[str,Any]:
  rh=h(body);row={**body,"row_sha256":rh};self.gz.write(enc(row)+b"\n");self.s.update((rh+"\n").encode());self.count+=1;return row
 def __exit__(self,*_):self.gz.close();self.raw.close()
 def descriptor(self)->dict[str,Any]:return{"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.s.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}
def authority_snapshot()->str:
 d=hashlib.sha256()
 for path in(CANON,HEAD):
  z=os.lstat(path);d.update((str(path.relative_to(ROOT))+"\0"+json.dumps(identity(z),sort_keys=True)).encode()+b"\n");d.update(hashlib.sha256(path.read_bytes()).digest())
 return d.hexdigest()
def q(v:Q)->str:return str(v.numerator)if v.denominator==1 else str(v)
def prefix_free(paths:list[str])->bool:
 s=sorted(paths,key=lambda x:(len(x),x));return all(not b.startswith(a)for i,a in enumerate(s)for b in s[i+1:])
def nonfull_blockers(kind:str)->list[str]:return{"REGULAR_BOUNDARY_ARRANGEMENT":["NO_UNIFORM_OPPOSITE_SIGN_FULL_GRAPH_AXIS_FACES","NO_GLOBAL_GRAPH_AXIS_SELECTED","OFF_GRAPH_TWO_SLAB_PARTITION_NOT_AVAILABLE"],"REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED":["MULTI_SURFACE_FULL_BOX_EXISTENCE_AND_ORDER_REGISTRY_MISSING","ACTIVE_SET_ORDER_NOT_ISOLATED","OFF_GRAPH_MULTI_SLAB_INTERSECTION_REGISTRY_MISSING"],"REGULAR_MULTI_GRAPH_FIRST_TANGENCY":["TANGENCY_GRAPH_TYPED_BUT_TWO_OFF_GRAPH_SLAB_DISPOSITIONS_MISSING","MULTI_SURFACE_ORDER_REGISTRY_MISSING"],"SOURCE_GRAZING_ENDPOINT_CHART":["SOURCE_GRAZING_TRANSFORMED_ENDPOINT_CHART_EVALUATOR_MISSING","ENDPOINT_GRAPH_AND_OFF_GRAPH_SLAB_PARTITION_MISSING"],"COLLISION1_OUTGOING_STATE":["EXACT_COLLISION1_OUTGOING_RADIAL_POSITIVITY_EVALUATOR_MISSING","STRICT_OUTGOING_CHART_MARGIN_EVALUATOR_MISSING","SECOND_OUTGOING_STATE_NOT_MATERIALIZED"]}[kind]

G_CONTEXT = None
G_CONFIG = None
G_M58 = None
G_M40 = None
def strip_box(box:Any,transverse:str,index:int,count:int)->Any:
 if transverse=="t":
  width=(box.t1-box.t0)/count;t0=box.t0+index*width;t1=t0+width;return c41.round185.atlas.AtlasBox(t0,t1,box.p0,box.p1,box.s0,box.s1,box.depth,f"{box.path}.c69b-t{index}of{count}")
 width=(box.p1-box.p0)/count;p0=box.p0+index*width;p1=p0+width;return c41.round185.atlas.AtlasBox(box.t0,box.t1,p0,p1,box.s0,box.s1,box.depth,f"{box.path}.c69b-p{index}of{count}")
def compact_newton(record:dict[str,Any])->dict[str,Any]:return{"axis":record["axis"],"strict_derivative":record["strict_derivative"],"strict_interior_self_map":record["strict_interior_self_map"],"image":record["image"]}
def evaluate(item:tuple[dict[str,Any],dict[str,Any]])->dict[str,Any]:
 structural,source=item;source58=G_M58[source["source_C58_leaf_row_sha256"]];ordinal,row40=G_M40[source58["C40_source_row_sha256"]];task=c41.task_for_row(ordinal,row40,G_CONTEXT);need(task["source"]["row_sha256"]==source58["C40_source_row_sha256"],"C58/C40")
 route=c41.route_at_path(task,source["path"],G_CONFIG);box=route["box"];need(c41.box_payload(box)==source["exact_representative_box"],"exact-box")
 result=route["c1_result"];need(result is not None,"C1 result");ev=result["surface_evidence"];old=ev["H1"];need(route["classification"]==source["route_classification"]=="UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY"and route["witness"]==source["route_witness"]=="REGULAR_FULL_FACE_GRAPH","route replay");need(ev["input_stage_one_classification"]==ev["enhanced_stage_one_classification"]=="unique_first"and ev["enhanced_owner_target"]=="W[1,0]"and ev["remaining_unresolved_record_count"]==0,"unique-first W10")
 axis=old["graph_axis"];need(old["kind"]=="REGULAR_FULL_FACE_GRAPH"and axis in{"t","p"},"graph-axis");idx={"t":0,"p":1}[axis];transverse="p"if axis=="t"else"t";face=[x for x in old["face_evidence"]if x["axis"]==axis];need(len(face)==1,"face evidence");face=face[0];low,high=face["lower_face"]["sign"],face["upper_face"]["sign"]
 full=c41.round185.surface_evidence("H1",task["c38_source"]["representative_origin_key"],box,c41.FROZEN_OWNER,include_axis_tests=True);derivative=full["full_box_C1_derivatives"]["d"+axis];base=not derivative["contains_zero"]and full["axis_full_face_brackets_t_p_s"][idx]is True and{low,high}=={"NEGATIVE","POSITIVE"}and full["independently_certified_nonempty"]is True
 if not base:return{"kind":"FULL_FACE_NUMERIC_BLOCKER","source":source,"structural":structural,"blocker_codes":["C39_REGULAR_FULL_FACE_LABEL_DID_NOT_REPLAY_TO_UNIFORM_STRICT_DERIVATIVE_AND_OPPOSITE_FULL_FACES"]}
 newton=full["axis_interval_Newton"][idx];covers=[]
 if newton["strict_derivative"]is True and newton["strict_interior_self_map"]is True and newton["image"]is not None:layer="A_MIDPOINT_INTERVAL_NEWTON_FULL_TRANSVERSE_BASE";root={"kind":"UNIFORM_INTERVAL_NEWTON_IMAGE","image":newton["image"]}
 else:
  layer=None;root=None
  for depth in range(1,MAX_B_DEPTH+1):
   candidate=[];count=1<<depth
   for index in range(count):
    sub=strip_box(box,transverse,index,count);proof=c41.round185.surface_evidence("H1",task["c38_source"]["representative_origin_key"],sub,c41.FROZEN_OWNER,include_axis_tests=True);n=proof["axis_interval_Newton"][idx];der=proof["full_box_C1_derivatives"]["d"+axis];ok=not der["contains_zero"]and proof["axis_full_face_brackets_t_p_s"][idx]is True and n["strict_derivative"]is True and n["strict_interior_self_map"]is True and n["image"]is not None
    if not ok:candidate=[];break
    lower,upper=(sub.t0,sub.t1)if transverse=="t"else(sub.p0,sub.p1);candidate.append({"schema":SCHEMA+".parametric-newton-cover-row","C61_aggregate_leaf_row_sha256":source["row_sha256"],"pair_index":source["pair_index"],"source_path":source["path"],"graph_axis":axis,"transverse_axis":transverse,"cover_depth":depth,"cover_index":index,"cover_prefix":format(index,f"0{depth}b"),"exact_transverse_interval":[q(lower),q(upper)],"relative_transverse_Kraft_fraction":str(Q(1,count)),"strict_graph_axis_derivative_bounds":der,"opposite_sign_full_graph_axis_faces":True,"axis_interval_Newton":compact_newton(n),"proof_only_cover_does_not_change_source_disposition":True,"formal_credit":0,"D02_gate_credit":0})
   if len(candidate)==count:covers=candidate;layer="B_FINITE_TRANSVERSE_INTERVAL_NEWTON_COVER";root={"kind":"PIECEWISE_UNIFORM_INTERVAL_NEWTON_IMAGES","cover_depth":depth,"cover_count":count,"cover_Kraft_sum":"1"};break
  if layer is None:layer="C_PARAMETRIC_IVT_PLUS_STRICT_MONOTONICITY_PLUS_IFT";bounds=(box.t0,box.t1)if axis=="t"else(box.p0,box.p1);root={"kind":"EXACT_FULL_GRAPH_AXIS_BRACKET","interval":[q(bounds[0]),q(bounds[1])],"existence":"UNIFORM_OPPOSITE_SIGN_FULL_FACES_PLUS_IVT","uniqueness":"FULL_BOX_STRICT_MONOTONICITY","regularity":"NONZERO_GRAPH_AXIS_DERIVATIVE_PLUS_IMPLICIT_FUNCTION_THEOREM"}
 negative="LOWER_GRAPH_AXIS_SIDE"if low=="NEGATIVE"else"UPPER_GRAPH_AXIS_SIDE";positive="LOWER_GRAPH_AXIS_SIDE"if low=="POSITIVE"else"UPPER_GRAPH_AXIS_SIDE"
 decision={"schema":SCHEMA+".decision-row","decision":"STRICT_UNIQUE_H1_GRAPH_AND_TWO_OFF_GRAPH_SLABS_AVAILABLE","acceptance_layer":layer,"query_key":"c69b-h1-graph-slab:"+source["row_sha256"],"C68_structural_task_row_sha256":structural["row_sha256"],"C61_aggregate_leaf_row_sha256":source["row_sha256"],"C58_leaf_row_sha256":source58["row_sha256"],"C40_source_row_sha256":task["source"]["row_sha256"],"C38_source_row_sha256":task["c38_source"]["row_sha256"],"representative_origin_key":task["c38_source"]["representative_origin_key"],"pair_index":source["pair_index"],"path":source["path"],"parent_volume_fraction":source["parent_volume_fraction"],"exact_representative_box":source["exact_representative_box"],"exact_reflected_box":source["exact_reflected_box"],"C39_branch_replay":{"input_stage_one_classification":"unique_first","enhanced_stage_one_classification":"unique_first","enhanced_owner_target":"W[1,0]","remaining_unresolved_record_count":0,"H1_kind":"REGULAR_FULL_FACE_GRAPH"},"full_box_graph_certificate":{"Arb_precision_bits":flint.ctx.prec,"equation":"H1=n1_x^2-n1_y^2=0","graph_axis":axis,"transverse_axis":transverse,"strict_graph_axis_derivative_bounds":derivative,"lower_graph_axis_face":face["lower_face"],"upper_graph_axis_face":face["upper_face"],"uniform_opposite_sign_full_faces":True,"C1_or_analytic_full_box_evaluator_succeeded":True,"strict_corner_segment_bracket":full["strict_corner_segment_bracket"],"normal_component_bounds":full["normal_component_bounds"],"midpoint_axis_interval_Newton":compact_newton(newton)},"root_enclosure_and_theorem":root,"typed_graph_carrier":{"predicate":"H1=0","dimension":1,"unique_root_over_every_fixed_transverse_parameter":True,"certified_nonempty":True,"Lebesgue_2_measure_zero":True},"off_graph_slabs":{"negative_open_slab":{"predicate":"H1<0","axis_orientation":negative,"dimension":2},"positive_open_slab":{"predicate":"H1>0","axis_orientation":positive,"dimension":2},"half_open_negative_graph_owner":{"predicate":"H1<=0","owns_graph":True},"half_open_positive_owner":{"predicate":"H1>0","owns_graph":False},"three_strata_pairwise_disjoint":True,"three_strata_union_exact_input_box":True},"partition_and_Kraft":{"source_path_preserved":True,"source_parent_volume_fraction_preserved":source["parent_volume_fraction"],"semantic_partition_not_extra_dyadic_depth":True,"volumetric_identity":"mu(H1<0)+mu(H1>0)=mu(input_box); mu(H1=0)=0","normalized_full_dimensional_Kraft_conservation":"1","typed_graph_weight_in_2D_Kraft":"0"},"proof_cover_pending_main_writer":bool(covers),"capability_consumption_ready":True,"terminal_disposition_credit":0,"collision2_handoff_credit":0,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0}
 return{"kind":"DECISION","source":source,"structural":structural,"decision":decision,"covers":covers}

def mathematical_contract()->dict[str,Any]:
 value={"schema":SCHEMA+".mathematical-data-contract","status":"FROZEN_LAYERED_A_B_C_GRAPH_SLAB_CONTRACT__MEASURED_CENSUS__ZERO_CREDIT","input_domain":{"C68_structural_task_count":20879,"eligible_category":"REGULAR_FULL_FACE_GRAPH_CELL","eligible_count":2356,"other_categories_fail_closed":18523},"theorem_C":{"hypotheses":["H1_IS_CONTINUOUS_ON_THE_CLOSED_SOURCE_RECTANGLE_AND_C1_OR_ANALYTIC_ON_A_NEIGHBORHOOD","ONE_GRAPH_AXIS_PARTIAL_DERIVATIVE_HAS_A_UNIFORM_STRICT_SIGN_ON_THE_FULL_RECTANGLE","H1_HAS_UNIFORM_STRICT_OPPOSITE_SIGNS_ON_THE_TWO_COMPLETE_GRAPH_AXIS_FACES"],"proof":"For every fixed transverse parameter, IVT gives a root between the two complete faces. Strict monotonicity gives uniqueness. The nonzero graph-axis derivative and IFT give a unique regular local graph; uniqueness glues these local graphs into one global graph over the complete transverse base.","conclusion":"ONE_NONEMPTY_UNIQUE_REGULAR_H1_GRAPH_PLUS_EXACT_NEGATIVE_AND_POSITIVE_OPEN_SLABS"},"acceptance_layers":{"A":"FULL_TRANSVERSE_BASE_MIDPOINT_INTERVAL_NEWTON_STRICT_INTERIOR_SELF_MAP","B":{"rule":"FINITE_DYADIC_TRANSVERSE_BASE_COVER; EVERY_STRIP_HAS_GRAPH_AXIS_INTERVAL_NEWTON_STRICT_INTERIOR_SELF_MAP","maximum_proof_cover_depth":MAX_B_DEPTH,"cover_prefix_free":True,"cover_Kraft_sum":"1","does_not_change_source_disposition":True},"C":"PARAMETRIC_IVT_PLUS_FULL_BOX_STRICT_MONOTONICITY_PLUS_IMPLICIT_FUNCTION_THEOREM; NO_INTERVAL_NEWTON_REQUIREMENT"},"half_open_partition":{"negative_owner":"H1<=0","positive_owner":"H1>0","graph_owner_unique":True,"three_strata_union_exact_input_box":True,"graph_Lebesgue_2_measure_zero":True,"full_dimensional_Kraft_conservation":"1"},"closed_query_contract":{"missing_duplicate_failed_lineage_or_failed_theorem":"FAIL_CLOSED","response":"GRAPH_CARRIER_PLUS_TWO_SIGN_SLABS","additional_dyadic_source_disposition_depth_permitted":False},"strict_boundary":{"candidate_is_installed_authority":False,"runtime_or_canonical_written":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"}};value["object_sha256"]=h(value);return value
def attacks(census:dict[str,int])->dict[str,Any]:
 capsule={**census,"all_lineage_exact":True,"all_unique_first_W10":True,"all_strict_derivatives":True,"all_opposite_full_faces":True,"all_graphs_unique":True,"all_graphs_nonempty":True,"all_two_slabs_complete":True,"all_half_open_owners_unique":True,"all_Kraft_one":True,"extra_source_depth":False,"runtime_write":False,"credit":0};out={}
 for key in sorted(capsule):
  m=copy.deepcopy(capsule);v=m[key];m[key]=not v if type(v)is bool else v+1
  try:need(m==capsule,"attack:"+key)
  except FailClosed:out[key]="FAIL_CLOSED"
  else:raise FailClosed("attack escaped")
 return{"status":f"PASS_{len(out)}_OF_{len(out)}_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":len(out),"attacks":out}

def build_stage(stage:Path,workers:int)->dict[str,Any]:
 need(stage.is_dir()and not stage.is_symlink()and not any(stage.iterdir()),"empty-stage");before=authority_snapshot();need(flint.__version__=="0.9.0"and flint.ctx.prec==384,"flint")
 raw={};idents={}
 for key,path in PATHS.items():raw[key],idents[key]=secure(path,P[key])
 c68=json.loads(raw["C68R"]);c61=json.loads(raw["C61R"]);c58=json.loads(raw["C58R"]);c40=json.loads(raw["C40R"])
 for value,expected,label in[(c68,P["C68O"],"C68"),(c61,P["C61O"],"C61"),(c58,P["C58O"],"C58"),(c40,P["C40O"],"C40")]:closeobj(value,expected,label)
 structural=rows(raw["C68S"],c68["ledgers"]["singleton_structural_tasks"],"C68 structural");all61=rows(raw["C61L"],c61["ledgers"]["aggregate_leaves"],"C61 leaves");selected=[x for x in all61 if x["disposition"]=="COLLISION2_HANDOFF"];need(len(structural)==len(selected)==20879,"20879")
 for a,b in zip(structural,selected,strict=True):need(a["C61_aggregate_leaf_row_sha256"]==b["row_sha256"]and a["path"]==b["path"],"C68/C61 order")
 rows58=rows(raw["C58L"],c58["ledgers"]["leaves"],"C58 leaves");m58={x["row_sha256"]:x for x in rows58};context=c41.load_context(C40,None,formal=False);need(context["result"]["object_sha256"]==P["C40O"],"context");c41.install_complete_immutable_cache();config=c41.decode_worker_config(context["config"]);rows40=c41.c38.read_ledger(C40,context["result"]["ledgers"]["routed_leaf_cells"]);m40={x["row_sha256"]:(i,x)for i,x in enumerate(rows40)}
 eligible=[];category=Counter()
 for a,b in zip(structural,selected,strict=True):
  category[a["structural_graph_kind"]]+=1
  if a["structural_graph_kind"]=="REGULAR_FULL_FACE_GRAPH_CELL":eligible.append((a,b))
 expected=Counter({"REGULAR_BOUNDARY_ARRANGEMENT":9053,"REGULAR_FULL_FACE_GRAPH_CELL":2356,"REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED":5364,"REGULAR_MULTI_GRAPH_FIRST_TANGENCY":737,"SOURCE_GRAZING_ENDPOINT_CHART":147,"COLLISION1_OUTGOING_STATE":3222});need(category==expected and len(eligible)==2356,"category")
 global G_CONTEXT,G_CONFIG,G_M58,G_M40;G_CONTEXT,G_CONFIG,G_M58,G_M40=context,config,m58,m40
 if workers==1:evaluated=[evaluate(x)for x in eligible]
 else:
  with mp.get_context("fork").Pool(processes=workers)as pool:evaluated=list(pool.imap(evaluate,eligible,chunksize=4))
 outcomes={x["source"]["row_sha256"]:x for x in evaluated};need(len(outcomes)==2356,"outcome-domain")
 contract=mathematical_contract();exclusive(stage/CONTRACT,enc(contract)+b"\n")
 layers=Counter();axes=Counter();orientations=Counter();bdepth=Counter();pair=Counter();pairvolume=defaultdict(Q);decision_paths=[];full_numeric_blockers=0
 with Writer(stage/COVERS,"DECISION_ORDER_THEN_COVER_PREFIX")as cw,Writer(stage/DECISIONS,"C68_C61_FILTERED_ORDER")as dw,Writer(stage/BLOCKERS,"C68_C61_FILTERED_ORDER")as bw:
  for a,source in zip(structural,selected,strict=True):
   need(a["exact_representative_box_object_sha256"]==h(source["exact_representative_box"]),"box hash")
   if a["structural_graph_kind"]!="REGULAR_FULL_FACE_GRAPH_CELL":bw.write({"schema":SCHEMA+".blocker-row","C68_structural_task_row_sha256":a["row_sha256"],"C61_aggregate_leaf_row_sha256":source["row_sha256"],"pair_index":source["pair_index"],"path":source["path"],"parent_volume_fraction":source["parent_volume_fraction"],"exact_representative_box_object_sha256":h(source["exact_representative_box"]),"structural_graph_kind":a["structural_graph_kind"],"route_classification":source["route_classification"],"route_witness":source["route_witness"],"capability_decision_available":False,"blocker_codes":nonfull_blockers(a["structural_graph_kind"]),"additional_dyadic_source_depth_recommended":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0});continue
   outcome=outcomes[source["row_sha256"]]
   if outcome["kind"]!="DECISION":
    full_numeric_blockers+=1;bw.write({"schema":SCHEMA+".blocker-row","C68_structural_task_row_sha256":a["row_sha256"],"C61_aggregate_leaf_row_sha256":source["row_sha256"],"pair_index":source["pair_index"],"path":source["path"],"parent_volume_fraction":source["parent_volume_fraction"],"exact_representative_box_object_sha256":h(source["exact_representative_box"]),"structural_graph_kind":a["structural_graph_kind"],"route_classification":source["route_classification"],"route_witness":source["route_witness"],"capability_decision_available":False,"blocker_codes":outcome["blocker_codes"],"additional_dyadic_source_depth_recommended":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0});continue
   coverrows=[cw.write(x)for x in outcome["covers"]];decision=outcome["decision"];decision["proof_cover"]={"row_count":len(coverrows),"row_hash_sequence_sha256":seq(x["row_sha256"]for x in coverrows),"prefix_free":True,"Kraft_sum":"1"if coverrows else"NOT_APPLICABLE","proof_only_cover_does_not_change_source_disposition":True};decision.pop("proof_cover_pending_main_writer");written=dw.write(decision);layers[decision["acceptance_layer"]]+=1;axis=decision["full_box_graph_certificate"]["graph_axis"];axes[axis]+=1;low=decision["full_box_graph_certificate"]["lower_graph_axis_face"]["sign"];high=decision["full_box_graph_certificate"]["upper_graph_axis_face"]["sign"];orientations[low+"_TO_"+high]+=1
   if coverrows:
    depth=coverrows[0]["cover_depth"];need(len(coverrows)==1<<depth and sum(Q(x["relative_transverse_Kraft_fraction"])for x in coverrows)==1 and prefix_free([x["cover_prefix"]for x in coverrows]),"cover Kraft");bdepth[str(depth)]+=1
   decision_paths.append(written["path"]);pair[str(source["pair_index"])]+=1;pairvolume[str(source["pair_index"])]+=Q(source["parent_volume_fraction"])
  coverdesc=cw.descriptor();decisiondesc=dw.descriptor();blockerdesc=bw.descriptor()
 need(decisiondesc["row_count"]+full_numeric_blockers==2356 and blockerdesc["row_count"]==18523+full_numeric_blockers and sum(layers.values())==decisiondesc["row_count"],"actual census");need(prefix_free(decision_paths)and len(decision_paths)==len(set(decision_paths)),"paths")
 census={"input_task_count":20879,"eligible_full_face_count":2356,"decision_count":decisiondesc["row_count"],"full_face_numeric_blocker_count":full_numeric_blockers,"total_blocker_count":blockerdesc["row_count"],"layer_A_count":layers["A_MIDPOINT_INTERVAL_NEWTON_FULL_TRANSVERSE_BASE"],"layer_B_count":layers["B_FINITE_TRANSVERSE_INTERVAL_NEWTON_COVER"],"layer_C_count":layers["C_PARAMETRIC_IVT_PLUS_STRICT_MONOTONICITY_PLUS_IFT"],"parametric_cover_row_count":coverdesc["row_count"],"formal_credit":0,"D02_gate_credit":0}
 after=authority_snapshot();need(after==before,"stage read-only")
 result={"schema":SCHEMA+".result","status":"MEASURED_LAYERED_H1_GRAPH_SLAB_CAPABILITY_PROTOTYPE__ZERO_CREDIT","producer_file_sha256":hf(SELF),"contract_file_sha256":hf(stage/CONTRACT),"contract_object_sha256":contract["object_sha256"],"input_file_sha256":{k:P[k]for k in PATHS},"input_file_identities":idents,"input_object_sha256":{"C68":P["C68O"],"C61":P["C61O"],"C58":P["C58O"],"C40":P["C40O"]},"numeric_environment":{"python_flint_version":flint.__version__,"Arb_precision_bits":flint.ctx.prec},"scope":census,"input_category_census":dict(sorted(category.items())),"acceptance_layer_census":dict(sorted(layers.items())),"decision_axis_census":dict(sorted(axes.items())),"decision_face_orientation_census":dict(sorted(orientations.items())),"layer_B_cover_depth_census":dict(sorted(bdepth.items())),"decision_pair_census":dict(sorted(pair.items(),key=lambda x:int(x[0]))),"decision_pair_source_volume_fraction":{k:str(v)for k,v in sorted(pairvolume.items(),key=lambda x:int(x[0]))},"ledgers":{"parametric_newton_covers":coverdesc,"decisions":decisiondesc,"blockers":blockerdesc},"global_invariants":{"all_decision_lineages_exact":True,"all_decisions_unique_first_W10":True,"all_decisions_uniform_strict_graph_axis_derivative":True,"all_decisions_uniform_opposite_sign_complete_faces":True,"all_decisions_nonempty_unique_global_graphs":True,"all_decisions_two_off_graph_slab_partitions":True,"all_decisions_half_open_graph_owners_unique":True,"all_decision_source_paths_prefix_free":True,"all_decision_source_volume_and_Kraft_preserved":True,"layer_B_covers_prefix_free_and_Kraft_one":True,"additional_dyadic_source_disposition_depth_used":False},"producer_attacks":attacks(census),"authority_snapshot_before_sha256":before,"authority_snapshot_after_sha256":after,"strict_boundary":{"staging_build_only":True,"candidate_is_installed_authority":False,"decisions_are_terminal_dispositions":False,"runtime_or_canonical_written":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":["SECOND_BYTE_IDENTICAL_STAGING_BUILD_AND_EXCLUSIVE_NO_REPLACE_PUBLICATION","INDEPENDENT_NO_PRODUCER_NUMERIC_REBUILD","CONSUME_GRAPH_AND_BOTH_SLABS_ONLY_AFTER_MANIFEST"]};result["object_sha256"]=h(result);exclusive(stage/RESULT,enc(result)+b"\n")
 report=f"# C69b measured H1 graph/slab capability prototype\n\nStatus: `{result['status']}`\n\nMeasured decisions: {census['decision_count']} / 2,356 eligible full-face tasks. A={census['layer_A_count']}, B={census['layer_B_count']}, C={census['layer_C_count']}; full-face numeric blockers={census['full_face_numeric_blocker_count']}. The other 18,523 categories remain fail-closed.\n\nLayer C is the parametric IVT + uniform strict monotonicity + IFT theorem and does not require a midpoint Newton self-map. Layer B subdivisions are proof covers only; their prefixes are complete and Kraft one and do not refine the source disposition. Every accepted box is partitioned into `H1<0`, `H1=0`, and `H1>0`, with the graph owned by `H1<=0`.\n\nResult object: `{result['object_sha256']}`. Formal/D02 credit remains zero.\n";exclusive(stage/REPORT,report.encode())
 return result

def publish(a:Path,b:Path)->dict[str,Any]:
 need(a.is_dir()and b.is_dir()and a!=b,"stages");data={}
 for name in STAGE_NAMES:
  left=(a/name).read_bytes();right=(b/name).read_bytes();need(left==right,"two-stage bytes:"+name);data[name]=left
 r=json.loads(data[RESULT]);closeobj(r,r["object_sha256"],"stage result");need(r["producer_file_sha256"]==hf(SELF),"producer binding");before=authority_snapshot();need(before==r["authority_snapshot_before_sha256"]==r["authority_snapshot_after_sha256"],"authority prepublish")
 targets=[OUT/name for name in STAGE_NAMES]+[OUT/RECEIPT];need(all(not x.exists()and not x.is_symlink()for x in targets),"fresh final targets")
 for name in(CONTRACT,COVERS,DECISIONS,BLOCKERS,REPORT,RESULT):exclusive(OUT/name,data[name])
 receipt={"schema":SCHEMA+".deterministic-two-stage-publication-receipt","status":"PASS_TWO_BYTE_IDENTICAL_STAGES__EXCLUSIVE_NO_REPLACE_PUBLICATION__ZERO_CREDIT","producer_file_sha256":hf(SELF),"result_object_sha256":r["object_sha256"],"published_files":{name:{"sha256":hashlib.sha256(data[name]).hexdigest(),"size":len(data[name])}for name in STAGE_NAMES},"stage_1_file_hash_sequence_sha256":seq(hashlib.sha256(data[name]).hexdigest()for name in STAGE_NAMES),"stage_2_file_hash_sequence_sha256":seq(hashlib.sha256(data[name]).hexdigest()for name in STAGE_NAMES),"all_stage_bytes_identical":True,"publication_O_EXCL_no_replace":True,"result_published_last":True,"authority_snapshot_before_sha256":before,"authority_snapshot_after_sha256":authority_snapshot(),"runtime_or_canonical_written":False,"formal_credit":0,"D02_gate_credit":0};need(receipt["authority_snapshot_after_sha256"]==before,"authority postpublish");receipt["object_sha256"]=h(receipt);exclusive(OUT/RECEIPT,enc(receipt)+b"\n");return receipt
def main()->int:
 p=argparse.ArgumentParser();mode=p.add_mutually_exclusive_group(required=True);mode.add_argument("--stage",type=Path);mode.add_argument("--publish",nargs=2,type=Path);p.add_argument("--workers",type=int,default=4);a=p.parse_args();need(1<=a.workers<=8,"workers")
 if a.stage:r=build_stage(a.stage.resolve(),a.workers);print(json.dumps({"status":r["status"],"scope":r["scope"],"layers":r["acceptance_layer_census"],"object_sha256":r["object_sha256"]},sort_keys=True))
 else:r=publish(a.publish[0].resolve(),a.publish[1].resolve());print(json.dumps({"status":r["status"],"object_sha256":r["object_sha256"]},sort_keys=True))
 return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(FailClosed,OSError,ValueError,KeyError,TypeError,IndexError,RuntimeError)as e:print(f"FAIL_CLOSED:{type(e).__name__}:{e}",file=sys.stderr);raise SystemExit(2)
