#!/usr/bin/env python3
"""Exact non-R300C factor classifier for the primitive G2A theorem chain."""
from __future__ import annotations
import argparse,hashlib,json,os,stat,sys,types
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

m: Any = None
class BootstrapFailure(RuntimeError):pass
def source_fp(s):return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
@dataclass
class SharedSourceCapture:
 path:Path;fd:int;pre:tuple[int,...];sha256:str;source:bytes
 @classmethod
 def open(cls,path:Path,expected:str):
  p=path.resolve();fd=os.open(p,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
  try:
   s=os.fstat(fd)
   if not stat.S_ISREG(s.st_mode):raise BootstrapFailure("shared source regular")
   h=hashlib.sha256();chunks=[]
   while b:=os.read(fd,4<<20):h.update(b);chunks.append(b)
   got=h.hexdigest()
   if got!=expected:raise BootstrapFailure("shared source sha256")
   if source_fp(os.fstat(fd))!=source_fp(s):raise BootstrapFailure("shared source hash-stat")
   return cls(p,fd,source_fp(s),got,b"".join(chunks))
  except BaseException:os.close(fd);raise
 def execute(self):
  name="_cm2_captured_g2a_factor_utility_v2";module=types.ModuleType(name);module.__file__=str(self.path);module.__package__="";sys.modules[name]=module
  exec(compile(self.source,str(self.path),"exec",dont_inherit=True),module.__dict__)
  self.unchanged("post-exec");return module
 def unchanged(self,phase):
  if source_fp(os.fstat(self.fd))!=self.pre:raise BootstrapFailure("shared source "+phase+" stat")
 def attestation(self):
  self.unchanged("attestation");return{"filename":self.path.name,"observed_sha256":self.sha256,"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True,"captured_source_bytes_compiled_and_executed":True,"stat_fingerprint":list(self.pre)}
 def close(self):self.unchanged("final");os.close(self.fd)

def build(a,shared_capture):
 out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False);caps={}
 try:
  for n,h in m.PINS.items():caps[n]=m.Capture.open(n,m.ROOT/n,h)
  cp=Path(a.candidate_ledger);rp=Path(a.predecessor_result);caps["candidate"]=m.Capture.open("candidate",cp,a.candidate_ledger_sha256);caps["predecessor"]=m.Capture.open("predecessor",rp,a.predecessor_result_sha256)
  pre=caps["predecessor"].document();scan=pre["C24A_G2B_interval_envelope_scan"]
  m.need(pre["status"]=="BLOCKED_ZERO_CREDIT__PRIMITIVE_CANDIDATES_MATERIALIZED__EXACT_RELATION_AND_RELATIVE_2D_ROUTES_OPEN"and pre["historical_edge_or_validation_ledger_opened"]is False and scan["historical_validation_set_opened"]is False and scan["distinct_envelope_candidate_pair_count"]==18800 and scan["ledger_file_sha256"]==a.candidate_ledger_sha256,"primitive predecessor")
  candidates=list(caps["candidate"].rows());m.need(len(candidates)==18800 and all("R300C_validation_pair"not in x for x in candidates),"candidate excludes R300C")
  m.need(len({(x["left_member_id"],x["right_member_id"])for x in candidates})==18800,"candidate unique")
  c24need={x["c24_row_sha256"]for x in candidates};c22need={x["target_row_sha256"]for x in candidates};members={z for x in candidates for z in(x["c24_member_id"],x["target_member_id"])}
  c10={}
  for r in caps[m.C10].rows():
   u,core=m.strip_unit(r["equation_ast"]["left"]);m.need(u==1 and r["equation_ast"]["op"]=="EQ"and m.is_zero(r["equation_ast"]["right"]),"C10 zero core");c10[r["graph_id"]]={"core":core if r["graph_class"]=="R235D_SOURCE_EXACT_FACE_FULL_BASE"else None,"core_sha":m.digest(core),"class":r["graph_class"],"rowsha":r["row_sha256"]}
  m.need(len(c10)==5264,"C10 census")
  c24={};authids={"C11A":set(),"C11B":set(),"C12A":set()}
  for r in caps[m.C24A].rows():
   if r["row_sha256"]not in c24need:continue
   p=m.strict_predicate(r["normalized_support_ast"]);u,core=m.strip_unit(p["left"]);g=c10[r["graph_id"]];m.need(r["coarse_family"]=="G2B"and m.is_zero(p["right"])and m.digest(core)==g["core_sha"],"C24/C10 core")
   au=r["semantic_theorem_ast"]["sealed_exact_support_authority"];role=au["role"];m.need(role in authids,"role");authids[role].add(au["row_id"]);c24[r["row_sha256"]]={"authority":au,"core":g["core"],"core_sha":g["core_sha"],"class":g["class"],"graph":r["graph_id"],"member":r["member_id"],"support_sha":r["normalized_support_ast_sha256"],"key":r["official_key_id"],"op":p["op"],"predicate_sha":m.digest(p),"unit":u,"role":role,"rowsha":r["row_sha256"]}
  m.need(set(c24)==c24need,"C24 totality")
  c22={}
  for r in caps[m.C22A].rows():
   if r["row_sha256"]in c22need:c22[r["row_sha256"]]={"member":r["owner_member_id"],"rowsha":r["row_sha256"],"support":r["support_ast"],"theorem":r["theorem_ast"],"theorem_sha":r["theorem_ast_sha256"]}
  m.need(set(c22)==c22need,"C22 totality")
  c15={}
  for r in caps[m.C15].rows():
   z=r["registry_member_id"]
   if z in members:c15[z]={"component":r["fresh_component_id"],"key":r["official_key_id"],"rowsha":r["row_sha256"]}
  m.need(set(c15)==members,"C15 totality")
  c11a={r["row_id"]:r for r in caps[m.C11A].rows()if r["row_id"]in authids["C11A"]};m.need(set(c11a)==authids["C11A"],"C11A totality")
  c11br={};interfaces=set()
  for r in caps[m.C11BR].rows():
   if r["row_id"]in authids["C11B"]:c11br[r["row_id"]]=r;interfaces.add(r["interface_kernel_ref"]["row_id"])
  m.need(set(c11br)==authids["C11B"],"C11B totality");c11bi={r["row_id"]:r for r in caps[m.C11BI].rows()if r["row_id"]in interfaces};m.need(set(c11bi)==interfaces,"C11B interface totality")
  c12a={r["row_id"]:r for r in caps[m.C12A].rows()if r["row_id"]in authids["C12A"]};m.need(set(c12a)==authids["C12A"],"C12A totality")
  output=[];dc=Counter();rc=Counter();cc=Counter();ic=Counter()
  for cand in candidates:
   s=c24[cand["c24_row_sha256"]];t=c22[cand["target_row_sha256"]];th=t["theorem"];au=th["sealed_source_authority"];role=s["role"];required=1 if s["op"]=="GT"else-1;sm=s["member"];tm=t["member"]
   m.need(cand["schema"]=="cm2.c27-independent.c24a-envelope-candidate.row.v2"and cand["target_source"]=="C22A"and cand["c24_member_id"]==sm and cand["target_member_id"]==tm and cand["physical_chart"]==t["support"]["coordinate_chart"]and cand["c24_predicate_op"]==s["op"]and cand["c24_predicate_ast_sha256"]==s["predicate_sha"],"candidate binding")
   m.need(c15[sm]["component"]==cand["c24_C15_component_id"]and c15[tm]["component"]==cand["target_C15_component_id"]and c15[sm]["key"]==s["key"]and cand["current_C15_components_equal"]==(c15[sm]["component"]==c15[tm]["component"]),"C15 binding")
   interface_sha=None;target_product=None
   if role=="C11A":
    r=c11a[s["authority"]["row_id"]];m.need(r["row_sha256"]==s["authority"]["row_sha256"]and r["graph_id"]==s["graph"]and r["side_member_id"]==sm and r["exact_side_stratum_ast_sha256"]==s["support_sha"]==s["authority"]["support_ast_sha256"],"C11A binding");m.wall_authority_closed(au,th);p=r["partition_semantic_ref"]
    if p["kind"]=="R235_SINGLE_ENDPOINT_GRAPH_PARTITION_ROW":
     ev=p["transition_event"];axis,pos=ev[0][0],str(ev[1]);reason=f"wall_endpoint_or_count_transition:{axis}:{pos}";m.need(au["reason_label"]==reason and au["equation"]==f"(source_{axis.lower()}-{pos})*(target_{axis.lower()}-{pos})=0","C11A factor identity");active=p["active_endpoint_factor"];fixed="target"if active=="source"else"source";ts=m.sign(au[f"witness_{active}_factor_sign"]);m.need(s["unit"]==r["fixed_other_endpoint_eta"]==m.sign(p["fixed_endpoint_factor_sign"])and m.sign(au[f"witness_{fixed}_factor_sign"])==m.sign(p["fixed_endpoint_factor_sign"]),"C11A fixed sign");why="C11A_R235_ACTIVE_"+active.upper()+"|"+reason
    else:
     m.need(p["kind"]=="R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE"and p["active_endpoint_factor"]=="source","C11A R235D");why=m.source_t_identity(au);ts=m.simple_t_factor_sign(s["core"],t["support"]["bounds"]);m.need(ts==m.sign(au["witness_source_factor_sign"])and s["unit"]==r["fixed_other_endpoint_eta"]==m.sign(p["fixed_target_factor_sign"])and m.sign(au["witness_target_factor_sign"])==m.sign(p["fixed_target_factor_sign"]),"C11A R235D signs");why="C11A_R235D_EXACT_SOURCE_9_OVER_25_TIMES_T|"+why
    target_product=au["region_product_sign"];m.need(required==m.sign(r["desired_eta_times_active_factor_sign"]),"C11A desired");authority_sha=r["row_sha256"]
   elif role=="C11B":
    r=c11br[s["authority"]["row_id"]];i=c11bi[r["interface_kernel_ref"]["row_id"]];m.need(r["row_sha256"]==s["authority"]["row_sha256"]and r["graph_id"]==s["graph"]and r["side_member_id"]==sm and r["ast_sha256"]["exact_side_carrier_ast"]==s["support_sha"]==s["authority"]["support_ast_sha256"]and i["row_sha256"]==r["interface_kernel_ref"]["row_sha256"],"C11B binding");atoms=[x for x in th["source_predicate_ast"]["atoms"]if x.get("factor")=="HPLUS_TIMES_HMINUS"];m.need(th["case_kind"]=="DIRECT_WHOLE_OPEN_LEAF"and au["kind"]=="DIRECT_WHOLE_OPEN_LEAF_FACTOR_SIGN_AUTHORITY"and len(atoms)==1 and atoms[0]["sign"]==au["region_factor_sign"]and m.sign(au["region_factor_sign"])==m.sign(au["HPLUS_sign"])*m.sign(au["HMINUS_sign"]),"C11B factor identity");ts=m.sign(au["region_factor_sign"]);side=r["one_sided_direction_receipt"]["factor_sign_on_side"];m.need(s["unit"]==1 and m.sign(side)==required and side==r["one_sided_direction_receipt"]["corresponding_carrier_face_sign"],"C11B side");why="C11B_F_EQUALS_HPLUS_TIMES_HMINUS";authority_sha=r["row_sha256"];interface_sha=i["row_sha256"]
   else:
    m.need(role=="C12A","C12A role");r=c12a[s["authority"]["row_id"]];m.need(r["row_sha256"]==s["authority"]["row_sha256"]and r["graph_id"]==s["graph"]and r["side_member_id"]==sm and r["exact_side_stratum_ast_sha256"]==s["support_sha"]==s["authority"]["support_ast_sha256"],"C12A binding");m.wall_authority_closed(au,th);why=m.source_t_identity(au);ts=m.simple_t_factor_sign(s["core"],t["support"]["bounds"]);p=r["partition_semantic_ref"];m.need(p["active_endpoint_factor"]=="source"and ts==m.sign(au["witness_source_factor_sign"])and s["unit"]==r["fixed_other_endpoint_eta"]==m.sign(p["fixed_target_factor_sign"])and m.sign(au["witness_target_factor_sign"])==m.sign(p["fixed_target_factor_sign"])and required==m.sign(r["desired_eta_times_active_factor_sign"]),"C12A signs");target_product=au["region_product_sign"];why="C12A_EXACT_SOURCE_9_OVER_25_TIMES_T|"+why;authority_sha=r["row_sha256"]
   actual=s["unit"]*ts;disp="EXACT_POSITIVE_SUPPORT"if actual==required else"EXACT_EMPTY_INTERSECTION"
   if target_product is not None:m.need((disp=="EXACT_POSITIVE_SUPPORT")== (m.sign(target_product)==required),"product disposition")
   dc[disp]+=1;rc[role+"|"+disp]+=1;cc[("SAME_C15"if cand["current_C15_components_equal"]else"CROSS_C15")+"|"+disp]+=1;ic[why+"|"+disp]+=1
   output.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.primitive-factor-disposition.row.v2","graph_id":s["graph"],"C10_row_sha256":c10[s["graph"]]["rowsha"],"authority_role":role,"authority_row_sha256":authority_sha,"C11B_interface_row_sha256":interface_sha,"C15_side_row_sha256":c15[sm]["rowsha"],"C15_target_row_sha256":c15[tm]["rowsha"],"C22_target_row_sha256":t["rowsha"],"C22_theorem_ast_sha256":t["theorem_sha"],"C24_side_row_sha256":s["rowsha"],"side_member_id":sm,"target_member_id":tm,"components":[c15[sm]["component"],c15[tm]["component"]],"components_equal":cand["current_C15_components_equal"],"disposition":disp,"factor_core_sha256":s["core_sha"],"factor_identity_route":why,"factor_sign_on_target_open_box":m.sign_name(ts),"predicate_op":s["op"],"predicate_required_sign":m.sign_name(required),"predicate_unit_sign":s["unit"],"signed_factor_value_on_target_open_box":m.sign_name(actual),"target_region_product_sign":target_product,"candidate_row_sha256":cand["row_sha256"],"formal_credit":0}))
  m.need(dc=={"EXACT_POSITIVE_SUPPORT":9408,"EXACT_EMPTY_INTERSECTION":9392}and rc=={"C11A|EXACT_POSITIVE_SUPPORT":8870,"C11A|EXACT_EMPTY_INTERSECTION":8864,"C11B|EXACT_POSITIVE_SUPPORT":528,"C11B|EXACT_EMPTY_INTERSECTION":528,"C12A|EXACT_POSITIVE_SUPPORT":10}and cc=={"SAME_C15|EXACT_POSITIVE_SUPPORT":8812,"SAME_C15|EXACT_EMPTY_INTERSECTION":8796,"CROSS_C15|EXACT_POSITIVE_SUPPORT":596,"CROSS_C15|EXACT_EMPTY_INTERSECTION":596},"acceptance census")
  output.sort(key=lambda r:(r["side_member_id"],r["target_member_id"]));lp=out/"G2B_18800_exact_factor_dispositions_no_historical_validation.jsonl.gz";fsha,seq,n=m.write_rows(lp,output);body={"schema":"cm2.c27-independent.g2a-relative2d.primitive-factor-classifier.v2","status":"PASS_18800_PRIMITIVE_FACTOR_DISPOSITIONS__9408_POSITIVE__9392_EMPTY__NO_HISTORICAL_VALIDATION_INPUT__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT","invocation_seed":a.seed,"candidate_pair_count":18800,"disposition_census":dict(dc),"authority_role_disposition_census":dict(rc),"component_disposition_census":dict(cc),"factor_identity_disposition_census":dict(ic),"unresolved":0,"historical_edge_or_validation_ledger_opened":False,"ledger":{"filename":lp.name,"row_count":n,"file_sha256":fsha,"row_sequence_sha256":seq},"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{**{k:v.attestation()for k,v in sorted(caps.items())},"shared_implementation_source":shared_capture.attestation()}},"formal_credit":0,"strict_nonpromotion":{"C27_transition_totality":0,"C28_pair_routing":0,"C29_physical_maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};res=dict(body);res["semantic_projection_sha256"]=m.digest({k:v for k,v in body.items()if k not in{"invocation_seed","root_input_capture"}});res["result_sha256"]=m.digest(res);(out/"result.json").write_bytes(m.canonical(res)+b"\n");return res
 finally:
  for v in caps.values():v.close()
def main():
 p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True);p.add_argument("--candidate-ledger",required=True);p.add_argument("--candidate-ledger-sha256",required=True);p.add_argument("--predecessor-result",required=True);p.add_argument("--predecessor-result-sha256",required=True);p.add_argument("--shared-implementation-source",required=True);p.add_argument("--shared-implementation-sha256",required=True);p.add_argument("--seed",type=int,required=True);a=p.parse_args();shared=None
 try:
  shared=SharedSourceCapture.open(Path(a.shared_implementation_source),a.shared_implementation_sha256)
  global m;m=shared.execute();r=build(a,shared)
  print(m.canonical({"status":r["status"],"result_sha256":r["result_sha256"],"semantic_projection_sha256":r["semantic_projection_sha256"]}).decode());return 0
 except(BootstrapFailure,RuntimeError,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));return 2
 finally:
  if shared is not None:shared.close()
if __name__=="__main__":raise SystemExit(main())
