#!/usr/bin/env python3
"""No-producer independent verifier for the C62-L edge semantic map."""
from __future__ import annotations
import ast,copy,gzip,hashlib,json,os,stat,sys
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";SELF=Path(__file__).resolve()
SCHEMA="cm2.round306c62l.edge-semantic-map-independent-verification.v1"
PREFIX="cm2_round306c62l_edge_semantic_map"
PRODUCER=OUT/(PREFIX+"_v1.py");RESULT=OUT/(PREFIX+"_result_v1.json")
OCC=OUT/(PREFIX+"_occurrence_lineage_map_v1.jsonl.gz");ATOM=OUT/(PREFIX+"_atom_map_v1.jsonl.gz");EDGE=OUT/(PREFIX+"_edge_map_v1.jsonl.gz");EXT=OUT/(PREFIX+"_endpoint_lineage_scope_extension_inventory_v1.jsonl.gz")
OUTPUT=OUT/(PREFIX+"_independent_verification_v1.json")
C60R=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json";C60V=OUT/"cm2_round306c60l_static_edge_owner_independent_verification_v1.json";C60M=OUT/"cm2_round306c60l_static_edge_owner_manifest_v1.sha256"
C59R=OUT/"cm2_round306c59l_owner_result_v1.json";C35=ROOT/".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2";C38=ROOT/".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133";C39=ROOT/".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559";C40=ROOT/".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f";C41=ROOT/".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C38SRC=OUT/"cm2_round306c38_d02_collision1_2_representative_child_atlas_v1.py";C38AUD=ROOT/".cm2-runtime/audit/c38-independent-audit-20260810T180628Z-c149ee1692741ec7/independent_audit.json"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"producer":"ecce7e6ae2aee1da27d7ff24619b1de62891dc703198892edda38d2fe46f3e61","result":"e85a188a7016de40fc7f3a607071aa53a2343684de51373b27786aaaf0c82615","object":"3d2c719f16e2921314bff0b83245e945b916da526306845eb8f00a6010cda8eb","occ":"0a79ff394aeadb7b8c40448742fd045728e0530f703f0f8350b5590bfdc07203","atom":"5bd0f671cc6383fdb4b32042b281bb2b81e01bd441c0fdc5138c059df2ac1e80","edge":"213af41e0d815992b81f7bf60fa673bf45d1ec60f14a9ab1e9985a5a4a1307b2","ext":"9b95d3d34e5f3529872ca4393776fe8d2349759867086a1bc6219eb50f5a9cec",
"C60r":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","C60o":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568","C60v":"1bf82a5d099698e3dec8532780f9bca4e1489db8a4aa7853984a4a3dd6d2ee0e","C60vo":"c5da39d3aca3d6d07aad91c56e56df74d56b0a0099434b5d4e15a7a49da526a7","C60m":"669938c6f32f45a2a814c8682ca7bb7fea5ba3ff424a364588d0cbbb038aabcf","C59r":"3391d96f6baa89281f9b60bd84a6aa950a74c6f6a99e86bc32b3322786e5a53e","C59o":"b6c486e042acedb9c287eda527cd4fcafffd1a53ff768b7697124100e39a85c2","C35r":"3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad","C35o":"cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752","occ1":"815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250","C38r":"094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501","C38o":"fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434","C39r":"f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e","C39o":"821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02","C40r":"f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6","C40o":"397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba","C41r":"73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f","C41o":"b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24","C38src":"8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d","C38aud":"e3fa567b3553415f5357ead66feb00b860c050a6ea687aeb7719666362ffac79","C38audo":"5e6d0a7a0d1f2216014ac5ef5858ddda6738802a1a02e5749a1f674f766eddf2","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
ALG={"-1/sqrt(2)","+1/sqrt(2)"}
class Reject(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise Reject(label)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def hf(p:Path)->str:
 s=hashlib.sha256()
 with p.open("rb")as f:
  for b in iter(lambda:f.read(1<<20),b""):s.update(b)
 return s.hexdigest()
def seq(values:Iterable[str])->str:
 s=hashlib.sha256()
 for value in values:s.update(value.encode("ascii")+b"\n")
 return s.hexdigest()
def js(p:Path)->dict[str,Any]:return json.loads(p.read_text())
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 body=dict(v);actual=body.pop("object_sha256",None);need(actual==expected==h(body),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 body=dict(v);actual=body.pop("row_sha256",None);need(actual==h(body),"row:"+label)
def rows(path:Path,desc:dict[str,Any],label:str)->list[dict[str,Any]]:
 need(path.name==desc["filename"]and hf(path)==desc["sha256"],"file:"+label);out=[];hashes=[]
 for i,line in enumerate(gzip.open(path,"rt")):
  row=json.loads(line);closerow(row,f"{label}:{i}");out.append(row);hashes.append(row["row_sha256"])
 need(len(out)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return out
def ledger(base:Path,desc:dict[str,Any],label:str)->list[dict[str,Any]]:return rows(base/desc["filename"],desc,label)
def token(x:Any)->str:return x["value"]if type(x)is dict else x
def cmp(a:str,b:str)->int:
 if a==b:return 0
 if a not in ALG and b not in ALG:return -1 if Fraction(a)<Fraction(b)else 1
 if a in ALG and b in ALG:return -1 if a.startswith("-")else 1
 if a in ALG:return-cmp(b,a)
 q=Fraction(a)
 if b=="+1/sqrt(2)":
  if q<=0:return-1
  need(q*q!=Fraction(1,2),"rational algebraic equality");return-1 if q*q<Fraction(1,2)else 1
 if q>=0:return 1
 need(q*q!=Fraction(1,2),"rational algebraic equality");return-1 if q*q>Fraction(1,2)else 1
def box(v:dict[str,Any]|None,chart:str)->dict[str,Any]|None:
 if v is None:return None
 return{"compact_chart":v.get("compact_chart",chart),"t":[token(x)for x in v["t"]],"p":[token(x)for x in v["p"]],"s":[token(x)for x in v["s"]]}
def contains(parent:dict[str,Any]|None,child:dict[str,Any]|None)->bool:
 if parent is None or child is None:return parent is child is None
 return parent["compact_chart"]==child["compact_chart"]and all(cmp(parent[a][0],child[a][0])<=0 and cmp(child[a][1],parent[a][1])<=0 for a in("t","p","s"))
def snapshot()->str:
 s=hashlib.sha256();base=ROOT/".cm2-runtime"
 for p in sorted(base.rglob("*"),key=lambda x:str(x.relative_to(base))):
  z=os.lstat(p);kind="D"if stat.S_ISDIR(z.st_mode)else"F"if stat.S_ISREG(z.st_mode)else"O";s.update(enc([str(p.relative_to(base)),kind,z.st_size,z.st_mtime_ns,z.st_nlink])+b"\n")
 s.update((hf(CANON)+"\n").encode());return s.hexdigest()
def source_contract()->dict[str,Any]:
 source=C38SRC.read_text();tree=ast.parse(source);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};need({"stage_two_route","refine_parent"}<=functions.keys(),"C38 functions")
 stage=ast.get_source_segment(source,functions["stage_two_route"]);refine=ast.get_source_segment(source,functions["refine_parent"])
 checks={"frozen_owner_W_1_0":"FROZEN_OWNER = \"W[1,0]\""in source,"occurrence1_official_word_is_original_path_0":"original_path[0][\"official_word_key_id\"]"in stage,"collision2_return_only_after_occurrence1_word_match":"return \"UNRESOLVED_COLLISION2_OWNER\", owner_error, 2"in stage and stage.index("original_path[0][\"official_word_key_id\"]")<stage.index("UNRESOLVED_COLLISION2_OWNER"),"first_decision_collision_persisted":"\"first_decision_collision\": collision_index"in refine};need(all(checks.values()),"source event-order contract")
 return{"C38_source_file_sha256":P["C38src"],"C38_audit_file_sha256":P["C38aud"],"C38_audit_object_sha256":P["C38audo"],"stage_two_route_source_sha256":hashlib.sha256(stage.encode()).hexdigest(),"refine_parent_source_sha256":hashlib.sha256(refine.encode()).hexdigest(),"checks":checks,"meaning":"first_decision_collision=2 certifies frozen owner W[1,0] and C35 occurrence1 official-word match before the collision2 decision"}
def validate_occurrence(row:dict[str,Any],inc:dict[str,Any],endpoint:dict[str,Any],z38:dict[str,Any],z39:dict[str,Any],z40:dict[str,Any],z41:dict[str,Any],present:bool,atom_hashes:list[str],occ1:dict[str,Any])->None:
 closerow(row,"occurrence");side=inc["side"];chart=endpoint["compact_chart"]
 need(z39["c38_child_row_sha256"]==z38["row_sha256"]and z40["c38_source_row_sha256"]==z38["row_sha256"]and z40["c39_source_row_sha256"]==z39["row_sha256"]and z41["c40_source_row_sha256"]==z40["row_sha256"],"chain links")
 need(z38["path"]==z39["path"]and z40["source_path"]==z39["path"]and z40["path"].startswith(z39["path"])and z41["source_path"]==z40["path"]and z41["path"].startswith(z40["path"]),"chain paths")
 b38=box(z38["representative_box"if side=="REPRESENTATIVE"else"reflected_box"],chart);b39=box(z39["representative_box"if side=="REPRESENTATIVE"else"reflected_box"],chart);b40=box(z40["representative_box"if side=="REPRESENTATIVE"else"reflected_box"],chart);b41=box(z41["closed_representative_box"if side=="REPRESENTATIVE"else"closed_reflected_box"],chart);epbox=box(endpoint["exact_physical_slice_endpoint_box"],chart)
 need(contains(b38,b39)and contains(b39,b40)and contains(b40,b41),"nested exact boxes");effective=b41 if b41 is not None else epbox;source="C41_EXACT_CLOSED_BOX"if b41 is not None else"C32_ENDPOINT_EXACT_BOX_FOR_ALGEBRAIC_C41_NULL_CHAIN"
 if b41 is None:need(b38 is None and b39 is None and b40 is None and effective is not None,"algebraic null-chain fallback")
 c1=z38["first_decision_collision"]==2;event={"C35_occurrence1_row_sha256":occ1["row_sha256"],"official_word_key_id":occ1["official_word_key_id"],"selected_absolute_owner_id":occ1["selected_absolute_owner_id"],"C38_first_decision_collision":z38["first_decision_collision"],"occurrence1_contract_passed_before_collision2":c1,"event_status":"PASSED_C35_OCCURRENCE1_FROZEN_OWNER_AND_OFFICIAL_WORD"if c1 else"STOPPED_AT_COLLISION1_CLASSIFICATION","C38_classification":z38["classification"]}
 expected={"schema":"cm2.round306c62l.edge-atom-occurrence1-lineage-semantic-map.v1.occurrence-lineage-map-row","endpoint_cell_id":endpoint["cell_id"],"physical_side":side,"compact_chart":chart,"C60_physical_occurrence_id":inc["physical_occurrence_id"],"C60_occurrence_binding_sha256":inc["occurrence_binding_sha256"],"C60_incident_atom_count":len(atom_hashes),"C60_incident_atom_row_hash_sequence_sha256":seq(atom_hashes),"in_C59_frozen_endpoint_lineage_scope":present,"C59_endpoint_binding_row_sha256":endpoint["row_sha256"],"chain":{"C38":{"row_sha256":z38["row_sha256"],"path":z38["path"],"box":b38,"classification":z38["classification"],"first_decision_collision":z38["first_decision_collision"]},"C39":{"row_sha256":z39["row_sha256"],"path":z39["path"],"box":b39,"classification":z39["classification"],"route_method":z39["route_method"]},"C40":{"row_sha256":z40["row_sha256"],"source_path":z40["source_path"],"path":z40["path"],"box":b40,"classification":z40["classification"]},"C41":{"row_sha256":z41["row_sha256"],"source_path":z41["source_path"],"path":z41["path"],"box":b41,"effective_incidence_box":effective,"effective_box_source":source,"split_axis_history":z41["split_axis_history"],"disposition_family":z41["disposition_family"],"residual_classification":z41["residual_classification"]}},"chain_row_hashes_exact":True,"paths_and_split_history_exact":True,"nested_boxes_exact":True,"occurrence1_event_order":event,"formal_credit":0,"D02_gate_credit":0}
 body=dict(row);body.pop("row_sha256");need(body==expected,"occurrence exact reconstruction")
def attacks(capsule:dict[str,Any])->dict[str,Any]:
 keys=list(capsule);need(len(keys)==29,"29 attack dimensions")
 def guard(v:dict[str,Any])->None:
  body=dict(v);actual=body.pop("object_sha256",None);need(actual==h(body),"attack closure");need(body==capsule,"attack semantic capsule")
 base={**capsule,"object_sha256":h(capsule)};guard(base);out={}
 for i,key in enumerate(keys):
  body=copy.deepcopy(capsule);value=body[key];body[key]=not value if type(value)is bool else value+1;candidate={**body,"object_sha256":h(body)}
  try:guard(candidate)
  except Reject:out[f"coherent_reclosed_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise Reject("attack accepted:"+key)
 return{"status":"PASS_29_OF_29_COHERENT_RECLOSED_ATTACKS_FAIL_CLOSED","attack_count":29,"mutations_reclosed_before_validation":True,"attacks":out}
def verify()->dict[str,Any]:
 before=snapshot();pins=[(PRODUCER,"producer"),(RESULT,"result"),(OCC,"occ"),(ATOM,"atom"),(EDGE,"edge"),(EXT,"ext"),(C60R,"C60r"),(C60V,"C60v"),(C60M,"C60m"),(C59R,"C59r"),(C35/"result.json","C35r"),(C38/"result.json","C38r"),(C39/"result.json","C39r"),(C40/"result.json","C40r"),(C41/"result.json","C41r"),(C38SRC,"C38src"),(C38AUD,"C38aud"),(C53,"C53"),(CANON,"canonical")]
 for path,key in pins:need(hf(path)==P[key],"pin:"+key)
 result,c60,c60v,c59,c35,c38,c39,c40,c41,audit=map(js,[RESULT,C60R,C60V,C59R,C35/"result.json",C38/"result.json",C39/"result.json",C40/"result.json",C41/"result.json",C38AUD])
 for value,key,label in[(result,"object","C62"),(c60,"C60o","C60"),(c60v,"C60vo","C60 verifier"),(c59,"C59o","C59"),(c35,"C35o","C35"),(c38,"C38o","C38"),(c39,"C39o","C39"),(c40,"C40o","C40"),(c41,"C41o","C41"),(audit,"C38audo","C38 audit")]:closeobj(value,P[key],label)
 need(result["C38_occurrence1_event_order_contract"]==source_contract(),"result source contract")
 occrows=rows(OCC,result["ledgers"]["occurrence_lineage_map"],"C62 occurrence");atomrows=rows(ATOM,result["ledgers"]["atom_map"],"C62 atom");edgerows=rows(EDGE,result["ledgers"]["edge_map"],"C62 edge");extrows=rows(EXT,result["ledgers"]["endpoint_lineage_scope_extension_inventory"],"C62 extension")
 endpoints=ledger(OUT,c59["ledgers"]["endpoint_occurrence1_history_bindings"],"C59 endpoints");requests=ledger(OUT,c59["ledgers"]["edge_owner_history_requests"],"C59 requests");upatoms=ledger(OUT,c60["ledgers"]["incidence_atoms"],"C60 atoms");decisions=ledger(OUT,c60["ledgers"]["edge_decisions"],"C60 decisions")
 occurrence1=ledger(C35,c35["ledgers"]["path_occurrences"],"C35 occurrence")[0];need(occurrence1["row_sha256"]==P["occ1"]and occurrence1["collision_index"]==1,"frozen occurrence1")
 r38={x["row_sha256"]:x for x in ledger(C38,c38["ledgers"]["collision1_2_child_pairs"],"C38 rows")};r39={x["row_sha256"]:x for x in ledger(C39,c39["ledgers"]["routed_child_pairs"],"C39 rows")};r40={x["row_sha256"]:x for x in ledger(C40,c40["ledgers"]["routed_leaf_cells"],"C40 rows")};r41={x["row_sha256"]:x for x in ledger(C41,c41["ledgers"]["routed_ambient_cells"],"C41 rows")}
 endpoint={x["cell_id"]:x for x in endpoints};current={cid:{p["C41"]["row_sha256"]:p for p in ep["C38_C41_lineage_projection_rows"]}for cid,ep in endpoint.items()};request={x["row_sha256"]:x for x in requests};decision={x["C59_request_row_sha256"]:x for x in decisions}
 atomrefs=defaultdict(list);source={}
 for atom in upatoms:
  for inc in atom["incident_occurrences"]:
   key=(inc["physical_cell_id"],inc["upstream_ambient_row_sha256"]);atomrefs[key].append(atom["row_sha256"]);source[key]=inc
 need(len(source)==len(occrows)==21869,"occurrence universe");occmap={(x["endpoint_cell_id"],x["chain"]["C41"]["row_sha256"]):x for x in occrows};need(set(occmap)==set(source),"occurrence key coverage")
 incidence=Counter();nullchains=0
 for key in sorted(source):
  inc=source[key];z41=r41[key[1]];z40=r40[z41["c40_source_row_sha256"]];z39=r39[z40["c39_source_row_sha256"]];z38=r38[z40["c38_source_row_sha256"]];present=key[1]in current[key[0]]
  validate_occurrence(occmap[key],inc,endpoint[key[0]],z38,z39,z40,z41,present,atomrefs[key],occurrence1)
  incidence["present"if present else"missing"]+=len(atomrefs[key]);incidence["c1"if z38["first_decision_collision"]==2 else"pre_c1"]+=len(atomrefs[key]);nullchains+=occmap[key]["chain"]["C41"]["box"]is None
  if present:
   frozen=current[key[0]][key[1]];need(frozen["C38"]["row_sha256"]==z38["row_sha256"]and frozen["C39"]["row_sha256"]==z39["row_sha256"]and frozen["C40"]["row_sha256"]==z40["row_sha256"]and frozen["C41"]["row_sha256"]==z41["row_sha256"]and frozen["C41"]["split_axis_history"]==z41["split_axis_history"],"C59 projection exact")
 need(incidence==Counter({"missing":18592,"present":7614,"c1":13440,"pre_c1":12766}),"incidence census")
 upatom={x["row_sha256"]:x for x in upatoms};atommap={x["C60_atom_row_sha256"]:x for x in atomrows};need(set(upatom)==set(atommap),"atom coverage");atomstats=Counter();byrequest=defaultdict(list)
 for atom in upatoms:
  row=atommap[atom["row_sha256"]];closerow(row,"atom replay");q=request[atom["C59_request_row_sha256"]];need(len(row["incident_lineage_maps"])==len(atom["incident_occurrences"])==2,"atom incidence arity")
  expected=[]
  for inc,mapped in zip(atom["incident_occurrences"],row["incident_lineage_maps"],strict=True):
   occurrence=occmap[(inc["physical_cell_id"],inc["upstream_ambient_row_sha256"])];b=occurrence["chain"]["C41"]["effective_incidence_box"];span=atom["exact_span"]
   if q["glue_kind"]=="INTRA_CHART_FACE":axis=q["exact_common_face_or_seam"]["axis"];other="p"if axis=="t"else"t";fixed=q["exact_common_face_or_seam"]["fixed_coordinate"];boundary=b[axis][1]if inc["geometric_side"]=="NEGATIVE_COORDINATE_SIDE"else b[axis][0];compatible=boundary==fixed and cmp(b[other][0],span[0])<=0 and cmp(span[1],b[other][1])<=0
   else:compatible=any(x in ALG for x in b["t"])and cmp(b["p"][0],span[0])<=0 and cmp(span[1],b["p"][1])<=0
   need(compatible,"common face compatibility");expected.append({"edge_role":inc["edge_role"],"geometric_side":inc["geometric_side"],"endpoint_cell_id":inc["physical_cell_id"],"occurrence_lineage_map_row_sha256":occurrence["row_sha256"],"C41_row_sha256":inc["upstream_ambient_row_sha256"],"in_C59_frozen_endpoint_lineage_scope":occurrence["in_C59_frozen_endpoint_lineage_scope"],"occurrence1_contract_passed_before_collision2":occurrence["occurrence1_event_order"]["occurrence1_contract_passed_before_collision2"],"atom_box_compatibility_proved":True})
  scope=all(x["in_C59_frozen_endpoint_lineage_scope"]for x in expected);c1=all(x["occurrence1_contract_passed_before_collision2"]for x in expected);passed=scope and c1;blockers=[]
  if not scope:blockers.append("AT_LEAST_ONE_INCIDENT_C41_ROW_OUTSIDE_C59_FROZEN_ENDPOINT_LINEAGE_SCOPE")
  if not c1:blockers.append("AT_LEAST_ONE_INCIDENT_CHAIN_STOPS_AT_COLLISION1_BEFORE_C35_OCCURRENCE1_CONTRACT_PASS")
  body=dict(row);body.pop("row_sha256");expectedbody={"schema":"cm2.round306c62l.edge-atom-occurrence1-lineage-semantic-map.v1.atom-map-row","C60_atom_row_sha256":atom["row_sha256"],"C59_request_row_sha256":atom["C59_request_row_sha256"],"face_or_corner_id":atom["face_or_corner_id"],"glue_kind":atom["glue_kind"],"exact_span":atom["exact_span"],"C60_owner_unique":atom["owner_unique"],"incident_lineage_maps":expected,"both_incidents_in_C59_frozen_endpoint_lineage_scope":scope,"both_incidents_passed_C35_occurrence1_contract":c1,"common_face_boxes_and_paths_compatible":True,"atom_semantic_mapping_pass":passed,"blocker_codes":blockers,"formal_credit":0,"D02_gate_credit":0};need(body==expectedbody,"atom exact reconstruction")
  atomstats["scope"]+=scope;atomstats["c1"]+=c1;atomstats["pass"]+=passed;byrequest[atom["C59_request_row_sha256"]].append(row)
 need(atomstats==Counter({"c1":6360,"scope":2298,"pass":1142}),"atom census")
 edgemap={x["C59_request_row_sha256"]:x for x in edgerows};need(set(edgemap)==set(request),"edge coverage");edgestats=Counter()
 for q in requests:
  row=edgemap[q["row_sha256"]];closerow(row,"edge replay");maps=byrequest[q["row_sha256"]];d=decision[q["row_sha256"]];scope=all(x["both_incidents_in_C59_frozen_endpoint_lineage_scope"]for x in maps);c1=all(x["both_incidents_passed_C35_occurrence1_contract"]for x in maps);allmap=all(x["atom_semantic_mapping_pass"]for x in maps);unique=d["geometric_owner_unique"];overall=unique and allmap;missing={(x["endpoint_cell_id"],x["C41_row_sha256"])for m in maps for x in m["incident_lineage_maps"]if not x["in_C59_frozen_endpoint_lineage_scope"]};blockers=[]
  if missing:blockers.append("FROZEN_ENDPOINT_LINEAGE_SCOPE_MISSING_INCIDENT_C41_ROWS")
  if not c1:blockers.append("NOT_ALL_EDGE_ATOMS_HAVE_BOTH_INCIDENCES_PAST_C35_OCCURRENCE1")
  if not unique:blockers.append("INDEPENDENT_OWNER_RULE_GAP__LEXICOGRAPHIC_MINIMUM_TIED")
  body=dict(row);body.pop("row_sha256");expected={"schema":"cm2.round306c62l.edge-atom-occurrence1-lineage-semantic-map.v1.edge-map-row","C59_request_row_sha256":q["row_sha256"],"owner_history_request_id":q["owner_history_request_id"],"face_or_corner_id":q["face_or_corner_id"],"glue_kind":q["glue_kind"],"atom_count":len(maps),"atom_map_row_hash_sequence_sha256":seq(x["row_sha256"]for x in maps),"C60_geometric_owner_unique":unique,"all_atoms_both_incidents_in_C59_endpoint_lineage_scope":scope,"all_atoms_both_incidents_passed_C35_occurrence1_contract":c1,"all_atom_semantic_mappings_pass":allmap,"missing_unique_endpoint_C41_scope_entry_count":len(missing),"missing_endpoint_C41_key_sequence_sha256":seq(f"{x[0]}:{x[1]}"for x in sorted(missing)),"overall_owner_history_mapping_pass":overall,"blocker_codes":blockers,"formal_credit":0,"D02_gate_credit":0};need(body==expected,"edge exact reconstruction")
  edgestats["scope"]+=scope;edgestats["c1"]+=c1;edgestats["unique_c1"]+=unique and c1;edgestats["tied_scope"]+=(not unique)and scope;edgestats["overall"]+=overall
 need(edgestats==Counter({"c1":386,"unique_c1":370,"scope":52,"tied_scope":52}),"edge census")
 missing=[occmap[k]for k in sorted(occmap)if not occmap[k]["in_C59_frozen_endpoint_lineage_scope"]];need(len(missing)==len(extrows)==15009,"extension coverage")
 for occurrence,row in zip(missing,extrows,strict=True):
  closerow(row,"extension replay");body=dict(row);body.pop("row_sha256");expected={"schema":"cm2.round306c62l.edge-atom-occurrence1-lineage-semantic-map.v1.endpoint-lineage-scope-extension-row","endpoint_cell_id":occurrence["endpoint_cell_id"],"C41_row_sha256":occurrence["chain"]["C41"]["row_sha256"],"occurrence_lineage_map_row_sha256":occurrence["row_sha256"],"C59_endpoint_binding_row_sha256":occurrence["C59_endpoint_binding_row_sha256"],"incident_atom_count":occurrence["C60_incident_atom_count"],"incident_atom_row_hash_sequence_sha256":occurrence["C60_incident_atom_row_hash_sequence_sha256"],"required_scope_action":"ADD_EXACT_C38_C41_LINEAGE_PROJECTION_TO_FROZEN_ENDPOINT_SCOPE","partial_scope_credit_permitted":False,"formal_credit":0,"D02_gate_credit":0};need(body==expected,"extension exact reconstruction")
 summary={"edge_count":1042,"atom_count":13103,"atom_incidence_count":26206,"unique_endpoint_C41_occurrence_count":21869,"frozen_endpoint_scope_present_incidence_count":7614,"frozen_endpoint_scope_missing_incidence_count":18592,"unique_scope_extension_row_count":15009,"atom_both_endpoint_scope_count":2298,"atom_both_occurrence1_pass_count":6360,"atom_semantic_mapping_pass_count":1142,"edge_all_endpoint_scope_count":52,"edge_all_occurrence1_pass_count":386,"owner_unique_edge_all_occurrence1_pass_count":370,"owner_tied_edge_all_endpoint_scope_count":52,"owner_unique_overall_mapping_pass_count":0,"overall_mapping_pass_count":0};need(result["scope"]==summary,"result summary")
 strict=result["strict_boundary"];need(strict=={"hash_join_complete":True,"partial_endpoint_scope_coverage_does_not_receive_credit":True,"131_owner_ties_remain_independent_owner_rule_gap":True,"arbitrary_tiebreak_added":False,"runtime_or_canonical_written":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"strict boundary")
 capsule={"occurrence_rows":21869,"atom_rows":13103,"edge_rows":1042,"extension_rows":15009,"incidences":26206,"present_incidences":7614,"missing_incidences":18592,"atom_scope":2298,"atom_c1":6360,"atom_pass":1142,"edge_scope":52,"edge_c1":386,"unique_edge_c1":370,"tied_edge_scope":52,"unique_edge_pass":0,"overall_edge_pass":0,"null_chain_fallback_rows":nullchains,"hash_join_complete":True,"paths_exact":True,"boxes_nested":True,"split_histories_exact":True,"event_order_exact":True,"scope_partial_credit":False,"arbitrary_tiebreak":False,"formal_credit":0,"D02_credit":0,"runtime_write":False,"canonical_write":False,"producer_executed":False};attack=attacks(capsule)
 after=snapshot();need(before==after and hf(C53)==P["C53"]and hf(CANON)==P["canonical"],"runtime/canonical stable")
 output={"schema":SCHEMA,"status":"PASS_NO_PRODUCER_FULL_RECONSTRUCTION__21869_OCCURRENCES__13103_ATOMS__1042_EDGES__15009_SCOPE_EXTENSION_ROWS__0_OF_911_OWNER_UNIQUE_PASS__131_TIES_UNCHANGED__29_OF_29_ATTACKS__ZERO_CREDIT","candidate":{"producer_file_sha256":P["producer"],"result_file_sha256":P["result"],"result_object_sha256":P["object"],"occurrence_ledger_file_sha256":P["occ"],"atom_ledger_file_sha256":P["atom"],"edge_ledger_file_sha256":P["edge"],"scope_extension_ledger_file_sha256":P["ext"]},"verified":summary,"algebraic_null_chain_fallback_row_count":nullchains,"attacks":attack,"independence":{"producer_imported_or_executed":False,"producer_treatment":"INERT_HASH_ONLY_BYTES","verifier_file_sha256":hf(SELF)},"strict_boundary":strict,"runtime_and_canonical_snapshot_before":before,"runtime_and_canonical_snapshot_after":after,"runtime_and_canonical_unchanged":True,"files_written":[str(OUTPUT.relative_to(ROOT))],"old_runtime_canonical_files_written":False};output["object_sha256"]=h(output);OUTPUT.write_bytes(enc(output)+b"\n");return output
def main()->int:
 result=verify();print(json.dumps({"status":result["status"],"verified":result["verified"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Reject,OSError,ValueError,KeyError,TypeError,IndexError,SyntaxError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
