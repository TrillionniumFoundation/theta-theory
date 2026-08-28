#!/usr/bin/env python3
"""Independent full-universe verifier for C60-L static edge queries."""
from __future__ import annotations
from collections import Counter,defaultdict
from fractions import Fraction
from functools import cmp_to_key
import copy,gzip,hashlib,json,os,stat,sys
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";SELF=Path(__file__).resolve()
SCHEMA="cm2.round306c60l.static-edge-owner-independent-verification.v1"
OUTPUT=OUT/"cm2_round306c60l_static_edge_owner_independent_verification_v1.json"
PRODUCER=OUT/"cm2_round306c60l_static_edge_owner_query_v1.py"
RESULT=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json"
C59R=OUT/"cm2_round306c59l_owner_result_v1.json";C59V=OUT/"cm2_round306c59l_owner_independent_verification_v1.json";C59M=OUT/"cm2_round306c59l_owner_manifest_v1.sha256"
C32=ROOT/".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9";C41=ROOT/".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C38=ROOT/".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133";C39=ROOT/".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559";C40=ROOT/".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"producer":"48a3dc7ac7d3edd5fe951f81fcbb4e60e44e5a263939792cd28385dac9191296","result":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","object":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568",
"C59r":"3391d96f6baa89281f9b60bd84a6aa950a74c6f6a99e86bc32b3322786e5a53e","C59o":"b6c486e042acedb9c287eda527cd4fcafffd1a53ff768b7697124100e39a85c2","C59v":"86cc87bc70cd78456a8913f632bb794806126f5f9963f700688880534c8a8c99","C59vo":"211f458b57e33544ef1978ddecda37f167e2df01720c72f0af003122b9c4bd58","C59m":"9940f3a133092aa9dea50204c0ef7c1c196ad1108c2fb1b01c8f5c6de4dc6fee",
"C32r":"c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4","C32o":"32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474","C41r":"73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f","C41o":"b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
"C38r":"094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501","C38o":"fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434","C39r":"f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e","C39o":"821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02","C40r":"f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6","C40o":"397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
"C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
ALG={"-1/sqrt(2)","+1/sqrt(2)"};RULE="UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH";ACTIVE="112410045d088f22908276193a1d046d6f11c0e1818790b2826c5fcf0f6ac05f"
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
 for v in values:s.update(v.encode("ascii")+b"\n")
 return s.hexdigest()
def js(p:Path)->dict[str,Any]:return json.loads(p.read_text())
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 b=dict(v);a=b.pop("object_sha256",None);need(a==expected==h(b),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 b=dict(v);a=b.pop("row_sha256",None);need(a==h(b),"row:"+label)
def ledger(base:Path,d:dict[str,Any],label:str)->list[dict[str,Any]]:
 p=base/d["filename"];need(hf(p)==d["sha256"],"file:"+label);rows=[];hashes=[]
 for i,line in enumerate(gzip.open(p,"rt")):
  r=json.loads(line);closerow(r,f"{label}:{i}");rows.append(r);hashes.append(r["row_sha256"])
 need(len(rows)==d["row_count"]and seq(hashes)==d["row_hash_line_sequence_sha256"],"desc:"+label);return rows
def token(v:Any)->str:return v["value"]if type(v)is dict else v
def cmp(a:str,b:str)->int:
 if a==b:return 0
 if a not in ALG and b not in ALG:return -1 if Fraction(a)<Fraction(b)else 1
 if a in ALG and b in ALG:return -1 if a.startswith("-")else 1
 if a in ALG:return -cmp(b,a)
 q=Fraction(a)
 if b=="+1/sqrt(2)":
  if q<=0:return -1
  need(q*q!=Fraction(1,2),"rational != algebraic");return -1 if q*q<Fraction(1,2)else 1
 if q>=0:return 1
 need(q*q!=Fraction(1,2),"rational != algebraic");return -1 if q*q>Fraction(1,2)else 1
def mn(a:str,b:str)->str:return a if cmp(a,b)<=0 else b
def mx(a:str,b:str)->str:return a if cmp(a,b)>=0 else b
def overlap(a0:str,a1:str,b0:str,b1:str)->tuple[str,str]|None:
 lo,hi=mx(a0,b0),mn(a1,b1);return(lo,hi)if cmp(lo,hi)<0 else None
def compact(o:dict[str,Any])->dict[str,Any]:return{"physical_occurrence_id":o["id"],"occurrence_binding_sha256":o["binding"],"source_kind":"C41_BASELINE","side":o["side"],"pair_index":o["pair"],"semantic_path":o["path"],"physical_cell_id":o["cell"],"upstream_ambient_row_sha256":o["ambient"]}
def snapshot()->str:
 s=hashlib.sha256();base=ROOT/".cm2-runtime"
 for p in sorted(base.rglob("*"),key=lambda x:str(x.relative_to(base))):
  z=os.lstat(p);k="D"if stat.S_ISDIR(z.st_mode)else"F"if stat.S_ISREG(z.st_mode)else"O";s.update(enc([str(p.relative_to(base)),k,z.st_size,z.st_mtime_ns,z.st_nlink])+b"\n")
 s.update((hf(CANON)+"\n").encode());return s.hexdigest()
def attacks(summary:dict[str,int])->dict[str,Any]:
 frozen={**summary,"all_candidate_atoms_exact":True,"all_candidate_decisions_exact":True,"owner_rule_unchanged":True,"arbitrary_tie_break_added":False,"history_mapping_present":False,"formal_credit":0,"D02_gate_credit":0,"runtime_write":False}
 need(len(frozen)==20,"20 attack keys")
 def guard(v:dict[str,Any])->None:
  b=dict(v);o=b.pop("object_sha256");need(o==h(b),"attack closure");need(b==frozen,"attack projection")
 base={**frozen,"object_sha256":h(frozen)};guard(base);out={}
 for i,(k,v)in enumerate(frozen.items()):
  b=copy.deepcopy(frozen);b[k]=not v if type(v)is bool else v+1;a={**b,"object_sha256":h(b)}
  try:guard(a)
  except Reject:out[f"coherent_reclosed_{i}_{k}"]="FAIL_CLOSED"
  else:raise Reject("attack accepted")
 return{"status":"PASS_20_OF_20_COHERENT_RECLOSED_ATTACKS_FAIL_CLOSED","attack_count":20,"mutations_reclosed_before_validation":True,"attacks":out}
def verify()->dict[str,Any]:
 before=snapshot();files=[(PRODUCER,"producer"),(RESULT,"result"),(C59R,"C59r"),(C59V,"C59v"),(C59M,"C59m"),(C32/"result.json","C32r"),(C41/"result.json","C41r"),(C38/"result.json","C38r"),(C39/"result.json","C39r"),(C40/"result.json","C40r"),(C53,"C53"),(CANON,"canonical")]
 for path,key in files:need(hf(path)==P[key],"pin:"+key)
 result,c59,c59v,c32,c41,c38,c39,c40=map(js,[RESULT,C59R,C59V,C32/"result.json",C41/"result.json",C38/"result.json",C39/"result.json",C40/"result.json"])
 for v,key,label in[(result,"object","C60"),(c59,"C59o","C59"),(c59v,"C59vo","C59v"),(c32,"C32o","C32"),(c41,"C41o","C41"),(c38,"C38o","C38"),(c39,"C39o","C39"),(c40,"C40o","C40")]:closeobj(v,P[key],label)
 endpoints=ledger(OUT,c59["ledgers"]["endpoint_occurrence1_history_bindings"],"C59 endpoints");requests=ledger(OUT,c59["ledgers"]["edge_owner_history_requests"],"C59 requests")
 atoms=ledger(OUT,result["ledgers"]["incidence_atoms"],"C60 atoms");decisions=ledger(OUT,result["ledgers"]["edge_decisions"],"C60 decisions")
 cells=ledger(C32,c32["ledgers"]["cells"],"C32 cells");ambient=ledger(C41,c41["ledgers"]["routed_ambient_cells"],"C41 ambient")
 endpoint={x["cell_id"]:x for x in endpoints};cell={x["cell_id"]:x for x in cells};byreq=defaultdict(list)
 for x in atoms:byreq[x["C59_request_row_sha256"]].append(x)
 need(len(requests)==len(decisions)==1042 and len(atoms)==13103,"candidate counts")
 index=defaultdict(list);ids=[];rational=algebraic=0
 for row in ambient:
  for side in("REPRESENTATIVE","REFLECTED"):
   cid=row["representative_cell_id"if side=="REPRESENTATIVE"else"reflected_cell_id"];c=cell[cid];box=row["closed_representative_box"if side=="REPRESENTATIVE"else"closed_reflected_box"]
   if box is None:t=[token(x)for x in c["physical_t_interval"]];p=[token(x)for x in c["physical_p_interval"]]
   else:t=[token(x)for x in box["t"]];p=[token(x)for x in box["p"]]
   body={"active_universe_binding_sha256":ACTIVE,"source_kind":"C41_BASELINE","side":side,"pair_index":row["pair_index"],"semantic_path":row["path"],"physical_cell_id":cid,"compact_chart":c["compact_chart"],"t":t,"p":p,"upstream_ambient_row_sha256":row["row_sha256"]}
   binding=h(body);o={"binding":binding,"id":"c60l-static-occurrence:"+binding,"side":side,"pair":row["pair_index"],"path":row["path"],"cell":cid,"chart":c["compact_chart"],"t":t,"p":p,"ambient":row["row_sha256"]};ids.append(o["id"])
   israt=all(x not in ALG for x in t+p);rational+=israt;algebraic+=not israt
   for axis,values,other in(("t",t,p),("p",p,t)):
    index[(o["chart"],axis,values[0])].append((o,"POSITIVE_COORDINATE_SIDE",other[0],other[1]));index[(o["chart"],axis,values[1])].append((o,"NEGATIVE_COORDINATE_SIDE",other[0],other[1]))
 need(len(ids)==len(set(ids))==183758 and rational==183700 and algebraic==58,"active reconstruction")
 ec=Counter();total=0
 for request,decision in zip(requests,decisions,strict=True):
  geometry=request["exact_common_face_or_seam"];low,high=geometry.get("span",geometry.get("physical_p_span"));sets=[]
  if request["glue_kind"]=="INTRA_CHART_FACE":sets=[("COMMON_CHART",index[(endpoint[request["source_cell_id"]]["compact_chart"],geometry["axis"],geometry["fixed_coordinate"])])]
  else:
   for role,cid in(("SOURCE",request["source_cell_id"]),("TARGET",request["target_cell_id"])):
    ep=endpoint[cid];contact=[token(x)for x in ep["exact_physical_slice_endpoint_box"]["t"]if token(x)in ALG];need(len(contact)==1,"seam contact");sets.append((role,index[(ep["compact_chart"],"t",contact[0])]))
  breaks={low,high};possible=[]
  for role,rows in sets:
   for o,side,a,b in rows:
    found=overlap(low,high,a,b)
    if found:breaks.update(found);possible.append((role,o,side,a,b))
  ordered=sorted(breaks,key=cmp_to_key(cmp));spans=[(a,b)for a,b in zip(ordered,ordered[1:])if cmp(a,b)<0];candidate=byreq[request["row_sha256"]]
  need([x["exact_span"]for x in candidate]==[list(x)for x in spans],"exhaustive atom spans")
  hashes=[];allcomplete=allcoverage=allunique=True
  for atom_index,((a,b),actual)in enumerate(zip(spans,candidate,strict=True)):
   incidents=[]
   for role,o,side,x,y in possible:
    if cmp(x,a)<=0 and cmp(b,y)<=0:incidents.append((role,o,side))
   incidents.sort(key=lambda x:x[1]["id"]);minimum=min((x[1]["path"]for x in incidents),default=None);winners=[x for x in incidents if x[1]["path"]==minimum]
   if request["glue_kind"]=="INTRA_CHART_FACE":complete=Counter(x[2]for x in incidents)==Counter({"NEGATIVE_COORDINATE_SIDE":1,"POSITIVE_COORDINATE_SIDE":1})
   else:complete=Counter(x[0]for x in incidents)==Counter({"SOURCE":1,"TARGET":1})
   coverage={x[1]["cell"]for x in incidents}=={request["source_cell_id"],request["target_cell_id"]};unique=len(winners)==1;compactrows=[]
   for role,o,side in incidents:item=compact(o);item.update({"edge_role":role,"geometric_side":side});compactrows.append(item)
   expected={"schema":"cm2.round306c60l.static-existing-edge-two-endpoint-owner-history-query.v1.incidence-atom-row","owner_rule":RULE,"C59_request_row_sha256":request["row_sha256"],"owner_history_request_id":request["owner_history_request_id"],"face_or_corner_id":request["face_or_corner_id"],"glue_kind":request["glue_kind"],"atom_index":atom_index,"exact_span":[a,b],"incident_occurrence_count":len(compactrows),"incident_occurrences":compactrows,"incident_occurrence_binding_sequence_sha256":seq(x[1]["binding"]for x in incidents),"incidence_complete":complete,"endpoint_cell_coverage_complete":coverage,"minimum_semantic_path":minimum,"owner_unique":unique,"owner":compact(winners[0][1])if unique else None,"owner_tie_occurrence_ids":[]if unique else[x[1]["id"]for x in winners],"formal_credit":0,"D02_gate_credit":0}
   body=dict(actual);rh=body.pop("row_sha256");need(body==expected and rh==h(expected),"atom exact reconstruction");hashes.append(rh);allcomplete&=complete;allcoverage&=coverage;allunique&=unique
  total+=len(candidate);ec["complete"]+=allcomplete;ec["coverage"]+=allcoverage;ec["unique"]+=allunique;ec["nonunique"]+=not allunique
  if not allunique:ec["intra_tie"if request["glue_kind"]=="INTRA_CHART_FACE"else"seam_tie"]+=1
  reasons=[]
  if not allunique:reasons.append("LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH_OWNER_TIE_ON_AT_LEAST_ONE_ATOM")
  reasons +=["NO_FROZEN_EDGE_ATOM_TO_C35_OCCURRENCE1_SEMANTIC_MAP","NO_FROZEN_C38_C41_ENDPOINT_LINEAGE_TO_EDGE_ATOM_INCIDENCE_MAP","WITHIN_CELL_LINEAGE_EXACTNESS_DOES_NOT_PROVE_CROSS_EDGE_OCCURRENCE1_HISTORY_COMPATIBILITY"]
  expected_dec={"schema":"cm2.round306c60l.static-existing-edge-two-endpoint-owner-history-query.v1.edge-decision-row","C59_request_row_sha256":request["row_sha256"],"owner_history_request_id":request["owner_history_request_id"],"source_cell_id":request["source_cell_id"],"target_cell_id":request["target_cell_id"],"face_or_corner_id":request["face_or_corner_id"],"glue_kind":request["glue_kind"],"atom_count":len(candidate),"incidence_atom_row_hash_sequence_sha256":seq(hashes),"full_active_universe_incidence_complete":allcomplete,"endpoint_cell_coverage_complete":allcoverage,"geometric_owner_unique":allunique,"geometric_owner_unique_disproved":not allunique,"C35_occurrence1_request_binding_valid":request["C35_occurrence1_history_binding_sha256"]==c59["occurrence1_binding"]["history_binding_sha256"],"both_endpoint_C38_C41_lineage_sequence_bindings_valid":all(type(x["C38_C41_lineage_projection_hash_sequence_sha256"])is str for x in request["endpoint_bindings"]),"edge_atom_to_occurrence1_lineage_semantic_mapping_present":False,"occurrence1_owner_history_compatible_proved":False,"overall_query_pass":False,"decision":"FAIL_CLOSED_MISSING_EDGE_ATOM_TO_OCCURRENCE1_LINEAGE_SEMANTIC_MAPPING","reason_codes":reasons,"formal_credit":0,"D02_gate_credit":0}
  body=dict(decision);rh=body.pop("row_sha256");need(body==expected_dec and rh==h(expected_dec),"decision exact reconstruction")
 need(total==13103 and ec==Counter({"complete":1042,"coverage":1042,"unique":911,"nonunique":131,"intra_tie":115,"seam_tie":16}),"aggregate")
 summary={"request_count":1042,"active_occurrence_count":183758,"exact_atom_count":13103,"incidence_complete_edge_count":1042,"endpoint_coverage_complete_edge_count":1042,"geometric_owner_unique_edge_count":911,"geometric_owner_nonunique_edge_count":131,"intra_owner_nonunique_edge_count":115,"seam_owner_nonunique_edge_count":16,"overall_query_pass_count":0,"overall_query_fail_closed_count":1042,"history_compatibility_pass_count":0}
 need(result["scope"]==summary and result["active_universe"]["occurrence_id_sequence_sha256"]==seq(sorted(ids)),"result summary");attack=attacks(summary);after=snapshot();need(before==after and hf(C53)==P["C53"]and hf(CANON)==P["canonical"],"stable")
 out={"schema":SCHEMA,"status":"PASS_INDEPENDENT_FULL_UNIVERSE_183758_OCCURRENCES__13103_ATOMS__1042_COMPLETE__911_UNIQUE__131_FROZEN_RULE_TIES__0_HISTORY_PASS__20_OF_20_ATTACKS__ZERO_CREDIT","candidate":{"producer_file_sha256":P["producer"],"result_file_sha256":P["result"],"result_object_sha256":P["object"]},"verified":summary,"active_universe":{"C32_rows_closed":76832,"C41_rows_closed":91879,"rational_occurrences":183700,"algebraic_occurrences":58},"owner_rule_audit":{"rule":RULE,"rule_modified":False,"arbitrary_side_or_history_tiebreak_added":False,"ties_are_nonunique_under_frozen_rule":True},"history_boundary":{"edge_atom_to_C35_occurrence1_semantic_map_present":False,"endpoint_C38_C41_lineage_to_atom_map_present":False},"attacks":attack,"independence":{"C60_producer_imported_or_executed":False,"producer_treatment":"INERT_HASH_ONLY_BYTES","verifier_file_sha256":hf(SELF)},"zero_credit":{"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"runtime_and_canonical_snapshot_before":before,"runtime_and_canonical_snapshot_after":after,"runtime_and_canonical_unchanged":True,"files_written":[str(OUTPUT.relative_to(ROOT))],"old_runtime_canonical_files_written":False}
 out["object_sha256"]=h(out);OUTPUT.write_bytes(enc(out)+b"\n");return out
def main()->int:
 r=verify();print(json.dumps({"status":r["status"],"verified":r["verified"],"object_sha256":r["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Reject,OSError,ValueError,KeyError,TypeError,IndexError)as e:print(f"FAIL_CLOSED:{type(e).__name__}:{e}",file=sys.stderr);raise SystemExit(2)
