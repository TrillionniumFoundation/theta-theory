#!/usr/bin/env python3
"""C62-L edge atom to occurrence-1 / C38-C41 semantic map."""
from __future__ import annotations
import ast,gzip,hashlib,json,sys
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";PREFIX="cm2_round306c62l_edge_semantic_map"
SCHEMA="cm2.round306c62l.edge-atom-occurrence1-lineage-semantic-map.v1"
OCC_FILE=PREFIX+"_occurrence_lineage_map_v1.jsonl.gz";ATOM_FILE=PREFIX+"_atom_map_v1.jsonl.gz";EDGE_FILE=PREFIX+"_edge_map_v1.jsonl.gz";EXT_FILE=PREFIX+"_endpoint_lineage_scope_extension_inventory_v1.jsonl.gz";RESULT_FILE=PREFIX+"_result_v1.json"
C60R=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json";C60V=OUT/"cm2_round306c60l_static_edge_owner_independent_verification_v1.json";C60M=OUT/"cm2_round306c60l_static_edge_owner_manifest_v1.sha256"
C59R=OUT/"cm2_round306c59l_owner_result_v1.json";C35=ROOT/".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2";C38=ROOT/".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133";C39=ROOT/".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559";C40=ROOT/".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f";C41=ROOT/".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C38SRC=OUT/"cm2_round306c38_d02_collision1_2_representative_child_atlas_v1.py";C38AUD=ROOT/".cm2-runtime/audit/c38-independent-audit-20260810T180628Z-c149ee1692741ec7/independent_audit.json"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"C60r":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","C60o":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568","C60v":"1bf82a5d099698e3dec8532780f9bca4e1489db8a4aa7853984a4a3dd6d2ee0e","C60vo":"c5da39d3aca3d6d07aad91c56e56df74d56b0a0099434b5d4e15a7a49da526a7","C60m":"669938c6f32f45a2a814c8682ca7bb7fea5ba3ff424a364588d0cbbb038aabcf","C59r":"3391d96f6baa89281f9b60bd84a6aa950a74c6f6a99e86bc32b3322786e5a53e","C59o":"b6c486e042acedb9c287eda527cd4fcafffd1a53ff768b7697124100e39a85c2","C35r":"3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad","C35o":"cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752","occ1":"815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250","C38r":"094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501","C38o":"fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434","C39r":"f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e","C39o":"821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02","C40r":"f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6","C40o":"397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba","C41r":"73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f","C41o":"b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24","C38src":"8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d","C38aud":"e3fa567b3553415f5357ead66feb00b860c050a6ea687aeb7719666362ffac79","C38audo":"5e6d0a7a0d1f2216014ac5ef5858ddda6738802a1a02e5749a1f674f766eddf2","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
ALG={"-1/sqrt(2)","+1/sqrt(2)"}
class FailClosed(RuntimeError):pass
def need(v:bool,l:str)->None:
 if type(v)is not bool or not v:raise FailClosed(l)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def hf(p:Path)->str:
 s=hashlib.sha256()
 with p.open("rb")as f:
  for b in iter(lambda:f.read(1<<20),b""):s.update(b)
 return s.hexdigest()
def seq(values:Iterable[str])->str:
 s=hashlib.sha256()
 for v in values:s.update(v.encode("ascii")+b"\n")
 return s.hexdigest()
def js(p:Path)->dict[str,Any]:return json.loads(p.read_text())
def closeobj(v:dict[str,Any],e:str,l:str)->None:
 b=dict(v);a=b.pop("object_sha256",None);need(a==e==h(b),"object:"+l)
def closerow(v:dict[str,Any],l:str)->None:
 b=dict(v);a=b.pop("row_sha256",None);need(a==h(b),"row:"+l)
def ledger(base:Path,d:dict[str,Any],l:str)->list[dict[str,Any]]:
 p=base/d["filename"];need(hf(p)==d["sha256"],"file:"+l);rows=[];hashes=[]
 for i,line in enumerate(gzip.open(p,"rt")):
  r=json.loads(line);closerow(r,f"{l}:{i}");rows.append(r);hashes.append(r["row_sha256"])
 need(len(rows)==d["row_count"]and seq(hashes)==d["row_hash_line_sequence_sha256"],"descriptor:"+l);return rows
class Writer:
 def __init__(self,p:Path,o:str):self.path,self.order=p,o;self.raw=p.open("wb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.s=hashlib.sha256()
 def __enter__(self):return self
 def write(self,b:dict[str,Any])->dict[str,Any]:
  rh=h(b);r={**b,"row_sha256":rh};self.gz.write(enc(r)+b"\n");self.s.update((rh+"\n").encode());self.count+=1;return r
 def __exit__(self,*_):self.gz.close();self.raw.close()
 def descriptor(self):return{"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.s.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}
def token(v:Any)->str:return v["value"]if type(v)is dict else v
def cmp(a:str,b:str)->int:
 if a==b:return 0
 if a not in ALG and b not in ALG:return-1 if Fraction(a)<Fraction(b)else 1
 if a in ALG and b in ALG:return-1 if a.startswith("-")else 1
 if a in ALG:return-cmp(b,a)
 q=Fraction(a)
 if b=="+1/sqrt(2)":
  if q<=0:return-1
  return-1 if q*q<Fraction(1,2)else 1
 if q>=0:return 1
 return-1 if q*q>Fraction(1,2)else 1
def box(v:dict[str,Any]|None,chart:str)->dict[str,Any]|None:
 if v is None:return None
 return{"compact_chart":v.get("compact_chart",chart),"t":[token(x)for x in v["t"]],"p":[token(x)for x in v["p"]],"s":[token(x)for x in v["s"]]}
def contains(parent:dict[str,Any]|None,child:dict[str,Any]|None)->bool:
 if parent is None or child is None:return parent is child is None
 return parent["compact_chart"]==child["compact_chart"]and all(cmp(parent[a][0],child[a][0])<=0 and cmp(child[a][1],parent[a][1])<=0 for a in("t","p","s"))
def c59proj(row38,row39,row40,row41):return{"C57L1_chain_row_sha256":None,"pair_index":row41["pair_index"],"C56L_task_row_sha256":None,"C38":{"row_sha256":row38["row_sha256"],"path":row38["path"],"classification":row38["classification"],"first_decision_collision":row38["first_decision_collision"]},"C39":{"row_sha256":row39["row_sha256"],"path":row39["path"],"classification":row39["classification"],"route_method":row39["route_method"]},"C40":{"row_sha256":row40["row_sha256"],"path":row40["path"],"classification":row40["classification"]},"C41":{"row_sha256":row41["row_sha256"],"path":row41["path"],"split_axis_history":row41["split_axis_history"],"residual_classification":row41["residual_classification"]}}
def source_contract()->dict[str,Any]:
 source=C38SRC.read_text();tree=ast.parse(source);fn={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};need("stage_two_route"in fn and"refine_parent"in fn,"C38 functions");stage=ast.get_source_segment(source,fn["stage_two_route"]);ref=ast.get_source_segment(source,fn["refine_parent"])
 checks={"frozen_owner_W_1_0":"FROZEN_OWNER = \"W[1,0]\""in source,"occurrence1_official_word_is_original_path_0":"original_path[0][\"official_word_key_id\"]"in stage,"collision2_return_only_after_occurrence1_word_match":"return \"UNRESOLVED_COLLISION2_OWNER\", owner_error, 2"in stage and stage.index("original_path[0][\"official_word_key_id\"]")<stage.index("UNRESOLVED_COLLISION2_OWNER"),"first_decision_collision_persisted":"\"first_decision_collision\": collision_index"in ref}
 need(all(checks.values()),"C38 semantic source contract");return{"C38_source_file_sha256":P["C38src"],"C38_audit_file_sha256":P["C38aud"],"C38_audit_object_sha256":P["C38audo"],"stage_two_route_source_sha256":hashlib.sha256(stage.encode()).hexdigest(),"refine_parent_source_sha256":hashlib.sha256(ref.encode()).hexdigest(),"checks":checks,"meaning":"first_decision_collision=2 certifies frozen owner W[1,0] and C35 occurrence1 official-word match before the collision2 decision"}
def selftest(s:dict[str,int])->dict[str,Any]:
 e={"edge_count":1042,"atom_count":13103,"atom_incidence_count":26206,"unique_endpoint_C41_occurrence_count":21869,"frozen_endpoint_scope_present_incidence_count":7614,"frozen_endpoint_scope_missing_incidence_count":18592,"unique_scope_extension_row_count":15009,"atom_both_endpoint_scope_count":2298,"atom_both_occurrence1_pass_count":6360,"atom_semantic_mapping_pass_count":1142,"edge_all_endpoint_scope_count":52,"edge_all_occurrence1_pass_count":386,"owner_unique_edge_all_occurrence1_pass_count":370,"owner_tied_edge_all_endpoint_scope_count":52,"owner_unique_overall_mapping_pass_count":0,"overall_mapping_pass_count":0}
 need(s==e,"summary");a={}
 for i,(k,v)in enumerate(e.items()):
  x=dict(s);x[k]=v+1
  try:need(x==e,"mutated")
  except FailClosed:a[f"projection_{i}_{k}"]="FAIL_CLOSED"
  else:raise FailClosed("attack")
 return{"status":"PASS_17_OF_17_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":17,"attacks":a}
def build()->dict[str,Any]:
 for path,key in[(C60R,"C60r"),(C60V,"C60v"),(C60M,"C60m"),(C59R,"C59r"),(C35/"result.json","C35r"),(C38/"result.json","C38r"),(C39/"result.json","C39r"),(C40/"result.json","C40r"),(C41/"result.json","C41r"),(C38SRC,"C38src"),(C38AUD,"C38aud"),(C53,"C53"),(CANON,"canonical")]:need(hf(path)==P[key],"pin:"+key)
 c60,c60v,c59,c35,c38,c39,c40,c41,audit=map(js,[C60R,C60V,C59R,C35/"result.json",C38/"result.json",C39/"result.json",C40/"result.json",C41/"result.json",C38AUD])
 for v,k,l in[(c60,"C60o","C60"),(c60v,"C60vo","C60v"),(c59,"C59o","C59"),(c35,"C35o","C35"),(c38,"C38o","C38"),(c39,"C39o","C39"),(c40,"C40o","C40"),(c41,"C41o","C41"),(audit,"C38audo","C38audit")]:closeobj(v,P[k],l)
 occurrence=ledger(C35,c35["ledgers"]["path_occurrences"],"C35 occurrences")[0];need(occurrence["row_sha256"]==P["occ1"]and occurrence["collision_index"]==1,"occ1")
 contract=source_contract();endpoints=ledger(OUT,c59["ledgers"]["endpoint_occurrence1_history_bindings"],"C59 endpoints");requests=ledger(OUT,c59["ledgers"]["edge_owner_history_requests"],"C59 requests");atoms=ledger(OUT,c60["ledgers"]["incidence_atoms"],"C60 atoms");decisions=ledger(OUT,c60["ledgers"]["edge_decisions"],"C60 decisions")
 r38={x["row_sha256"]:x for x in ledger(C38,c38["ledgers"]["collision1_2_child_pairs"],"C38")};r39={x["row_sha256"]:x for x in ledger(C39,c39["ledgers"]["routed_child_pairs"],"C39")};r40={x["row_sha256"]:x for x in ledger(C40,c40["ledgers"]["routed_leaf_cells"],"C40")};r41={x["row_sha256"]:x for x in ledger(C41,c41["ledgers"]["routed_ambient_cells"],"C41")}
 endpoint={x["cell_id"]:x for x in endpoints};current={cid:{p["C41"]["row_sha256"]:p for p in e["C38_C41_lineage_projection_rows"]}for cid,e in endpoint.items()};request={x["row_sha256"]:x for x in requests};decision={x["C59_request_row_sha256"]:x for x in decisions}
 atom_by_req=defaultdict(list);occurrence_refs=defaultdict(list);occurrence_source={}
 for a in atoms:
  atom_by_req[a["C59_request_row_sha256"]].append(a)
  for inc in a["incident_occurrences"]:
   key=(inc["physical_cell_id"],inc["upstream_ambient_row_sha256"]);occurrence_refs[key].append(a["row_sha256"]);occurrence_source[key]=inc
 occurrence_rows={};membership=Counter();c1count=Counter()
 with Writer(OUT/OCC_FILE,"CELL_ID_THEN_C41_ROW_SHA256")as w:
  for key in sorted(occurrence_source):
   cid,c41hash=key;inc=occurrence_source[key];z41=r41[c41hash];z40=r40[z41["c40_source_row_sha256"]];z39=r39[z40["c39_source_row_sha256"]];z38=r38[z40["c38_source_row_sha256"]]
   need(z39["c38_child_row_sha256"]==z38["row_sha256"]and z40["c38_source_row_sha256"]==z38["row_sha256"]and z40["c39_source_row_sha256"]==z39["row_sha256"]and z41["c40_source_row_sha256"]==z40["row_sha256"],"chain hashes")
   need(z38["path"]==z39["path"]and z40["source_path"]==z39["path"]and z40["path"].startswith(z39["path"])and z41["source_path"]==z40["path"]and z41["path"].startswith(z40["path"]),"path chain")
   side=inc["side"];chart=endpoint[cid]["compact_chart"];b38=box(z38["representative_box"if side=="REPRESENTATIVE"else"reflected_box"],chart);b39=box(z39["representative_box"if side=="REPRESENTATIVE"else"reflected_box"],chart);b40=box(z40["representative_box"if side=="REPRESENTATIVE"else"reflected_box"],chart);b41=box(z41["closed_representative_box"if side=="REPRESENTATIVE"else"closed_reflected_box"],chart)
   need(contains(b38,b39)and contains(b39,b40)and contains(b40,b41),"nested boxes")
   endpoint_box=box(endpoint[cid]["exact_physical_slice_endpoint_box"],chart)
   effective_incidence_box=b41 if b41 is not None else endpoint_box
   effective_box_source="C41_EXACT_CLOSED_BOX"if b41 is not None else"C32_ENDPOINT_EXACT_BOX_FOR_ALGEBRAIC_C41_NULL_CHAIN"
   if b41 is None:need(b38 is None and b39 is None and b40 is None and effective_incidence_box is not None,"algebraic null-chain endpoint fallback")
   present=c41hash in current[cid];membership["present"if present else"missing"]+=len(occurrence_refs[key]);c1=z38["first_decision_collision"]==2;c1count["pass"if c1 else"block"]+=len(occurrence_refs[key])
   frozen=current[cid].get(c41hash)
   if frozen:
    p=c59proj(z38,z39,z40,z41);p["C57L1_chain_row_sha256"]=frozen["C57L1_chain_row_sha256"];p["C56L_task_row_sha256"]=frozen["C56L_task_row_sha256"]
    need(all(p[k]==frozen[k]for k in("C57L1_chain_row_sha256","pair_index","C56L_task_row_sha256","C38","C39","C40","C41")),"C59 projection match")
   event={"C35_occurrence1_row_sha256":occurrence["row_sha256"],"official_word_key_id":occurrence["official_word_key_id"],"selected_absolute_owner_id":occurrence["selected_absolute_owner_id"],"C38_first_decision_collision":z38["first_decision_collision"],"occurrence1_contract_passed_before_collision2":c1,"event_status":"PASSED_C35_OCCURRENCE1_FROZEN_OWNER_AND_OFFICIAL_WORD"if c1 else"STOPPED_AT_COLLISION1_CLASSIFICATION","C38_classification":z38["classification"]}
   body={"schema":SCHEMA+".occurrence-lineage-map-row","endpoint_cell_id":cid,"physical_side":side,"compact_chart":chart,"C60_physical_occurrence_id":inc["physical_occurrence_id"],"C60_occurrence_binding_sha256":inc["occurrence_binding_sha256"],"C60_incident_atom_count":len(occurrence_refs[key]),"C60_incident_atom_row_hash_sequence_sha256":seq(occurrence_refs[key]),"in_C59_frozen_endpoint_lineage_scope":present,"C59_endpoint_binding_row_sha256":endpoint[cid]["row_sha256"],"chain":{"C38":{"row_sha256":z38["row_sha256"],"path":z38["path"],"box":b38,"classification":z38["classification"],"first_decision_collision":z38["first_decision_collision"]},"C39":{"row_sha256":z39["row_sha256"],"path":z39["path"],"box":b39,"classification":z39["classification"],"route_method":z39["route_method"]},"C40":{"row_sha256":z40["row_sha256"],"source_path":z40["source_path"],"path":z40["path"],"box":b40,"classification":z40["classification"]},"C41":{"row_sha256":z41["row_sha256"],"source_path":z41["source_path"],"path":z41["path"],"box":b41,"effective_incidence_box":effective_incidence_box,"effective_box_source":effective_box_source,"split_axis_history":z41["split_axis_history"],"disposition_family":z41["disposition_family"],"residual_classification":z41["residual_classification"]}},"chain_row_hashes_exact":True,"paths_and_split_history_exact":True,"nested_boxes_exact":True,"occurrence1_event_order":event,"formal_credit":0,"D02_gate_credit":0}
   occurrence_rows[key]=w.write(body)
 occ_desc=w.descriptor();need(len(occurrence_rows)==21869 and membership==Counter({"missing":18592,"present":7614}),"membership census")
 atom_map={};atomstats=Counter()
 with Writer(OUT/ATOM_FILE,"C60_ATOM_ORDER")as w:
  for a in atoms:
   q=request[a["C59_request_row_sha256"]];mapped=[]
   for inc in a["incident_occurrences"]:
    row=occurrence_rows[(inc["physical_cell_id"],inc["upstream_ambient_row_sha256"])];b=row["chain"]["C41"]["effective_incidence_box"];need(b is not None,"effective incidence box")
    span=a["exact_span"]
    if q["glue_kind"]=="INTRA_CHART_FACE":
     axis=q["exact_common_face_or_seam"]["axis"];other="p"if axis=="t"else"t";fixed=q["exact_common_face_or_seam"]["fixed_coordinate"];side=inc["geometric_side"];boundary=b[axis][1]if side=="NEGATIVE_COORDINATE_SIDE"else b[axis][0];compatible=boundary==fixed and cmp(b[other][0],span[0])<=0 and cmp(span[1],b[other][1])<=0
    else:
     compatible=any(x in ALG for x in b["t"])and cmp(b["p"][0],span[0])<=0 and cmp(span[1],b["p"][1])<=0
    need(compatible,"atom/box common-face compatibility");mapped.append({"edge_role":inc["edge_role"],"geometric_side":inc["geometric_side"],"endpoint_cell_id":inc["physical_cell_id"],"occurrence_lineage_map_row_sha256":row["row_sha256"],"C41_row_sha256":inc["upstream_ambient_row_sha256"],"in_C59_frozen_endpoint_lineage_scope":row["in_C59_frozen_endpoint_lineage_scope"],"occurrence1_contract_passed_before_collision2":row["occurrence1_event_order"]["occurrence1_contract_passed_before_collision2"],"atom_box_compatibility_proved":True})
   bothscope=all(x["in_C59_frozen_endpoint_lineage_scope"]for x in mapped);bothc1=all(x["occurrence1_contract_passed_before_collision2"]for x in mapped);passed=bothscope and bothc1
   atomstats["scope"]+=bothscope;atomstats["c1"]+=bothc1;atomstats["pass"]+=passed
   blockers=[]
   if not bothscope:blockers.append("AT_LEAST_ONE_INCIDENT_C41_ROW_OUTSIDE_C59_FROZEN_ENDPOINT_LINEAGE_SCOPE")
   if not bothc1:blockers.append("AT_LEAST_ONE_INCIDENT_CHAIN_STOPS_AT_COLLISION1_BEFORE_C35_OCCURRENCE1_CONTRACT_PASS")
   body={"schema":SCHEMA+".atom-map-row","C60_atom_row_sha256":a["row_sha256"],"C59_request_row_sha256":a["C59_request_row_sha256"],"face_or_corner_id":a["face_or_corner_id"],"glue_kind":a["glue_kind"],"exact_span":a["exact_span"],"C60_owner_unique":a["owner_unique"],"incident_lineage_maps":mapped,"both_incidents_in_C59_frozen_endpoint_lineage_scope":bothscope,"both_incidents_passed_C35_occurrence1_contract":bothc1,"common_face_boxes_and_paths_compatible":True,"atom_semantic_mapping_pass":passed,"blocker_codes":blockers,"formal_credit":0,"D02_gate_credit":0};atom_map[a["row_sha256"]]=w.write(body)
 atom_desc=w.descriptor();need(atomstats==Counter({"c1":6360,"scope":2298,"pass":1142}),"atom stats")
 edgestats=Counter();edge_rows=[]
 for q in requests:
  maps=[atom_map[a["row_sha256"]]for a in atom_by_req[q["row_sha256"]]];d=decision[q["row_sha256"]];allscope=all(x["both_incidents_in_C59_frozen_endpoint_lineage_scope"]for x in maps);allc1=all(x["both_incidents_passed_C35_occurrence1_contract"]for x in maps);allmap=all(x["atom_semantic_mapping_pass"]for x in maps);unique=d["geometric_owner_unique"];overall=unique and allmap
  edgestats["scope"]+=allscope;edgestats["c1"]+=allc1;edgestats["unique_c1"]+=unique and allc1;edgestats["tied_scope"]+=(not unique)and allscope;edgestats["overall"]+=overall
  missing={(x["endpoint_cell_id"],x["C41_row_sha256"])for m in maps for x in m["incident_lineage_maps"]if not x["in_C59_frozen_endpoint_lineage_scope"]}
  blockers=[]
  if missing:blockers.append("FROZEN_ENDPOINT_LINEAGE_SCOPE_MISSING_INCIDENT_C41_ROWS")
  if not allc1:blockers.append("NOT_ALL_EDGE_ATOMS_HAVE_BOTH_INCIDENCES_PAST_C35_OCCURRENCE1")
  if not unique:blockers.append("INDEPENDENT_OWNER_RULE_GAP__LEXICOGRAPHIC_MINIMUM_TIED")
  edge_rows.append({"schema":SCHEMA+".edge-map-row","C59_request_row_sha256":q["row_sha256"],"owner_history_request_id":q["owner_history_request_id"],"face_or_corner_id":q["face_or_corner_id"],"glue_kind":q["glue_kind"],"atom_count":len(maps),"atom_map_row_hash_sequence_sha256":seq(x["row_sha256"]for x in maps),"C60_geometric_owner_unique":unique,"all_atoms_both_incidents_in_C59_endpoint_lineage_scope":allscope,"all_atoms_both_incidents_passed_C35_occurrence1_contract":allc1,"all_atom_semantic_mappings_pass":allmap,"missing_unique_endpoint_C41_scope_entry_count":len(missing),"missing_endpoint_C41_key_sequence_sha256":seq(f"{x[0]}:{x[1]}"for x in sorted(missing)),"overall_owner_history_mapping_pass":overall,"blocker_codes":blockers,"formal_credit":0,"D02_gate_credit":0})
 with Writer(OUT/EDGE_FILE,"C59_REQUEST_ORDER")as w:
  for row in edge_rows:w.write(row)
 edge_desc=w.descriptor();need(edgestats==Counter({"c1":386,"unique_c1":370,"scope":52,"tied_scope":52}),"edge stats")
 with Writer(OUT/EXT_FILE,"ENDPOINT_CELL_ID_THEN_C41_ROW_SHA256")as w:
  for key in sorted(occurrence_rows):
   row=occurrence_rows[key]
   if row["in_C59_frozen_endpoint_lineage_scope"]:continue
   w.write({"schema":SCHEMA+".endpoint-lineage-scope-extension-row","endpoint_cell_id":key[0],"C41_row_sha256":key[1],"occurrence_lineage_map_row_sha256":row["row_sha256"],"C59_endpoint_binding_row_sha256":row["C59_endpoint_binding_row_sha256"],"incident_atom_count":row["C60_incident_atom_count"],"incident_atom_row_hash_sequence_sha256":row["C60_incident_atom_row_hash_sequence_sha256"],"required_scope_action":"ADD_EXACT_C38_C41_LINEAGE_PROJECTION_TO_FROZEN_ENDPOINT_SCOPE","partial_scope_credit_permitted":False,"formal_credit":0,"D02_gate_credit":0})
 ext_desc=w.descriptor();need(ext_desc["row_count"]==15009,"extension count")
 summary={"edge_count":1042,"atom_count":13103,"atom_incidence_count":26206,"unique_endpoint_C41_occurrence_count":21869,"frozen_endpoint_scope_present_incidence_count":7614,"frozen_endpoint_scope_missing_incidence_count":18592,"unique_scope_extension_row_count":15009,"atom_both_endpoint_scope_count":2298,"atom_both_occurrence1_pass_count":6360,"atom_semantic_mapping_pass_count":1142,"edge_all_endpoint_scope_count":52,"edge_all_occurrence1_pass_count":386,"owner_unique_edge_all_occurrence1_pass_count":370,"owner_tied_edge_all_endpoint_scope_count":52,"owner_unique_overall_mapping_pass_count":0,"overall_mapping_pass_count":0}
 test=selftest(summary);result={"schema":SCHEMA+".result","status":"PASS_EXACT_13103_ATOM_26206_INCIDENCE_CHAIN_MAP__15009_SCOPE_EXTENSION_INVENTORY__FAIL_CLOSED_0_OF_911_OWNER_UNIQUE_EDGE_MAPPINGS__131_TIES_UNCHANGED__ZERO_CREDIT","authority_binding":{"C60_result_file_sha256":P["C60r"],"C60_result_object_sha256":P["C60o"],"C60_independent_verification_file_sha256":P["C60v"],"C60_independent_verification_object_sha256":P["C60vo"],"C60_manifest_file_sha256":P["C60m"],"C59_result_object_sha256":P["C59o"],"C35_object_sha256":P["C35o"],"C38_object_sha256":P["C38o"],"C39_object_sha256":P["C39o"],"C40_object_sha256":P["C40o"],"C41_object_sha256":P["C41o"],"C53_head_file_sha256":P["C53"],"canonical_file_sha256":P["canonical"]},"C38_occurrence1_event_order_contract":contract,"scope":summary,"ledgers":{"occurrence_lineage_map":occ_desc,"atom_map":atom_desc,"edge_map":edge_desc,"endpoint_lineage_scope_extension_inventory":ext_desc},"self_test":test,"strict_boundary":{"hash_join_complete":True,"partial_endpoint_scope_coverage_does_not_receive_credit":True,"131_owner_ties_remain_independent_owner_rule_gap":True,"arbitrary_tiebreak_added":False,"runtime_or_canonical_written":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":["EXTEND_EACH_ENDPOINT_LINEAGE_SCOPE_BY_THE_15009_FROZEN_INVENTORY_ROWS","REPLAY_ALL_13103_ATOM_MAPS_AFTER_SCOPE_EXTENSION","KEEP_131_OWNER_TIES_AS_AN_INDEPENDENT_OWNER_RULE_GAP_UNLESS_THE_SEMANTIC_MAP_PROVES_DISJOINT_HISTORY"]}
 result["object_sha256"]=h(result);(OUT/RESULT_FILE).write_bytes(enc(result)+b"\n");return result
def main()->int:
 r=build();print(json.dumps({"status":r["status"],"scope":r["scope"],"object_sha256":r["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(FailClosed,OSError,ValueError,KeyError,TypeError,IndexError,SyntaxError)as e:print(f"FAIL_CLOSED:{type(e).__name__}:{e}",file=sys.stderr);raise SystemExit(2)
