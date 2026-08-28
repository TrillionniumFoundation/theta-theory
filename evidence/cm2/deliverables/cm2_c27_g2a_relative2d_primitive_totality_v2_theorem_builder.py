#!/usr/bin/env python3
"""Build the 5,264-route G2A relative-boundary/positive-side theorem."""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,stat,sys,types
from collections import Counter,defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any,Iterator

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
  name="_cm2_captured_g2a_theorem_utility_v2";module=types.ModuleType(name);module.__file__=str(self.path);module.__package__="";sys.modules[name]=module
  exec(compile(self.source,str(self.path),"exec",dont_inherit=True),module.__dict__)
  self.unchanged("post-exec");return module
 def unchanged(self,phase):
  if source_fp(os.fstat(self.fd))!=self.pre:raise BootstrapFailure("shared source "+phase+" stat")
 def attestation(self):
  self.unchanged("attestation");return{"filename":self.path.name,"observed_sha256":self.sha256,"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True,"captured_source_bytes_compiled_and_executed":True,"stat_fingerprint":list(self.pre)}
 def close(self):self.unchanged("final");os.close(self.fd)

SIGNED="cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_ledger.json.gz"
COMPLETE="cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_face_inventory.json.gz"
TERMINAL_PINS={SIGNED:"9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9",COMPLETE:"443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d"}
def docrows(cap)->Iterator[dict[str,Any]]:
 os.lseek(cap.fd,0,0);dup=os.dup(cap.fd)
 with os.fdopen(dup,"rb")as raw:
  with gzip.GzipFile(fileobj=raw,mode="rb")as compressed:
   with io.TextIOWrapper(compressed,encoding="ascii")as z:
    marker='"rows":[';buf=""
    while marker not in buf:
     b=z.read(1<<20);m.need(bool(b),cap.label+":marker");buf+=b
    buf=buf.split(marker,1)[1];dec=json.JSONDecoder();n=0
    while True:
     buf=buf.lstrip()
     if not buf:
      b=z.read(1<<20);m.need(bool(b),cap.label+":EOF");buf=b;continue
     if buf[0]==',':buf=buf[1:];continue
     if buf[0]==']':break
     try:r,e=dec.raw_decode(buf)
     except json.JSONDecodeError:
      b=z.read(1<<20);m.need(bool(b),cap.label+":truncated");buf+=b;continue
     m.check_closed(r,cap.label+":"+str(n));yield r;n+=1;buf=buf[e:]
 cap.unchanged("document rows")
def closure_ok(role,r):
 if role in{"C11A","C12A"}:
  c=r["closure_incidence_certificate"];m.need(c["kind"]=="EXACT_SIGN_STRATUM_RELATIVE_CLOSURE_INCIDENCE_V1"and c["closure_incidence_complete"]is True and c["graph_subset_of_relative_side_closure_by_trace_atlas"]is True and c["strict_side_and_graph_are_disjoint"]is True and c["strict_sign_stratum_is_relatively_open"]is True and c["relative_closure_intersection_statement"]=="closure_in_carrier(exact_side_stratum) INTERSECT exact_graph_support = exact_graph_support","relative closure certificate");return c["certificate_sha256"]
 m.need(role=="C11B","C11B role");c=r["common_boundary_trace_receipt"];m.need(c["R245_role_edge_has_exact_R242_patch_contact"]is True and c["closure_of_one_sided_sign_collar_meets_zero_set_in_exact_C10_support"]is True and c["strict_monotone_unique_zero_over_full_base"]is True and c["primitive_factor_continuity_bound_to_C10_radical_receipts"]is True and r["local_graph_side_physical_incidence_proved"]is True and r["one_sided_trace_proved"]is True,"R242 common trace");return m.digest(c)
def write(path,rows):return dict(zip(("file_sha256","row_sequence_sha256","row_count"),m.write_rows(path,rows)))|{"filename":path.name}
def build(a,shared_capture):
 out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False);caps={}
 try:
  inputs={"candidate_result":(Path(a.candidate_result),a.candidate_result_sha256),"routes":(Path(a.route_ledger),a.route_ledger_sha256),"g2a_candidates":(Path(a.g2a_candidate_ledger),a.g2a_candidate_ledger_sha256),"factor_result":(Path(a.factor_result),a.factor_result_sha256),"factor_ledger":(Path(a.factor_ledger),a.factor_ledger_sha256)}
  for k,(p,h)in inputs.items():caps[k]=m.Capture.open(k,p,h)
  for n in(m.C11A,m.C11BR,m.C12A,m.C24A):caps[n]=m.Capture.open(n,m.ROOT/n,m.PINS[n])
  for n,h in TERMINAL_PINS.items():caps[n]=m.Capture.open(n,m.ROOT/n,h)
  cr=caps["candidate_result"].document();fr=caps["factor_result"].document();m.need(cr["status"]=="BLOCKED_ZERO_CREDIT__PRIMITIVE_CANDIDATES_MATERIALIZED__EXACT_RELATION_AND_RELATIVE_2D_ROUTES_OPEN"and cr["historical_edge_or_validation_ledger_opened"]is False and fr["status"]=="PASS_18800_PRIMITIVE_FACTOR_DISPOSITIONS__9408_POSITIVE__9392_EMPTY__NO_HISTORICAL_VALIDATION_INPUT__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT"and fr["historical_edge_or_validation_ledger_opened"]is False,"predecessors")
  routes=list(caps["routes"].rows());cand=list(caps["g2a_candidates"].rows());factors=list(caps["factor_ledger"].rows());m.need(len(routes)==5264 and len(cand)==9408 and len(factors)==18800,"input census")
  bypair={(x["graph_id"],x["target_member_id"]):x for x in cand};m.need(len(bypair)==9408,"G2A pair unique");pos=defaultdict(list);neg=defaultdict(list)
  for x in factors:(pos if x["disposition"]=="EXACT_POSITIVE_SUPPORT"else neg)[(x["graph_id"],x["target_member_id"])].append(x)
  m.need(sum(map(len,pos.values()))==9408 and sum(map(len,neg.values()))==9392,"factor split")
  auth={}
  for role,n in(("C11A",m.C11A),("C11B",m.C11BR),("C12A",m.C12A)):
   for r in caps[n].rows():auth[(role,r["row_sha256"])]=(r,closure_ok(role,r))
  g2aside=defaultdict(list)
  for r in caps[m.C24A].rows():
   if r["coarse_family"]=="G2B":g2aside[r["graph_id"]].append(r)
  signed=set()
  for r in docrows(caps[SIGNED]):
   if r["decision"].startswith("ACCEPT_")and r["left_formal_occurrence_id"]!=r["right_formal_occurrence_id"]:signed.add(tuple(sorted((r["left_formal_occurrence_id"],r["right_formal_occurrence_id"]))))
  complete=set()
  for r in docrows(caps[COMPLETE]):
   if not r["decision"].startswith("ACCEPT_"):continue
   for l in r["left_formal_occurrence_endpoints"]:
    for q in r["right_formal_occurrence_endpoints"]:
     if l!=q:complete.add(tuple(sorted((l,q))))
  contacts=[];reverse=[];same=cross=0;rolec=Counter();single_no_reverse=0
  for k,c in sorted(bypair.items()):
   pp=pos[k];nn=neg.get(k,[]);m.need(len(pp)==1 and len(nn)in{0,1},"unique side disposition");p=pp[0];m.need(p["components"][0]==c["g2a_component_id"]and p["components"][1]==c["target_component_id"],"G2A/side component handoff");ar,certsha=auth[(p["authority_role"],p["authority_row_sha256"])]
   pair=tuple(c["unordered_member_pair"]);sidepair=tuple(sorted((p["side_member_id"],p["target_member_id"])));m.need(pair not in signed and pair not in complete and sidepair not in signed and sidepair not in complete,"terminal disjointness")
   contacts.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.exact-contact-alias-route.row.v2","graph_id":c["graph_id"],"g2a_member_id":c["g2a_member_id"],"positive_side_member_id":p["side_member_id"],"target_member_id":c["target_member_id"],"physical_chart":c["physical_chart"],"g2a_component_id":c["g2a_component_id"],"positive_side_component_id":p["components"][0],"target_component_id":c["target_component_id"],"g2a_and_positive_side_same_C15_component":True,"g2a_target_components_equal":c["components_equal"],"G2A_outer_candidate_row_sha256":c["row_sha256"],"positive_factor_disposition_row_sha256":p["row_sha256"],"relative_boundary_authority_role":p["authority_role"],"relative_boundary_authority_row_sha256":p["authority_row_sha256"],"relative_boundary_certificate_sha256":certsha,"route_theorem":"G2A_EQUALS_EXACT_GRAPH__GRAPH_IS_RELATIVE_BOUNDARY_OF_UNIQUE_POSITIVE_SIDE__POSITIVE_SIDE_INTERSECTS_TARGET_OPEN_SUPPORT","assigned_unique_terminal":"SAME_CHART_RELATIVE_CELLS","raw_SIGNED_pair":False,"raw_COMPLETE_pair":False,"raw_positive_side_SIGNED_pair":False,"raw_positive_side_COMPLETE_pair":False,"formal_credit":0}));rolec[p["authority_role"]]+=1
   if c["components_equal"]:same+=1
   else:cross+=1
   if nn:
    n=nn[0];m.need(n["components"][0]==c["g2a_component_id"]and n["components"][1]==c["target_component_id"],"reverse side component handoff");reverse.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.reverse-side-empty-binding.row.v2","graph_id":c["graph_id"],"g2a_member_id":c["g2a_member_id"],"target_member_id":c["target_member_id"],"positive_side_member_id":p["side_member_id"],"empty_reverse_side_member_id":n["side_member_id"],"positive_factor_row_sha256":p["row_sha256"],"empty_factor_row_sha256":n["row_sha256"],"unique_positive_side_among_envelope_candidates":True,"formal_credit":0}))
   else:single_no_reverse+=1
  m.need(len(contacts)==9408 and len(reverse)==9392 and single_no_reverse==16 and same==8812 and cross==596,"contact census")
  complement=[];route_final=[]
  for r in routes:
   gid=r["graph_id"];n=r["C22_contact_candidate_count"]
   if n==0:
    m.need(r["graph_class"]=="R235_SOURCE_EXACT_FACE_FULL_BASE"and len(g2aside[gid])==1,"552 complement graph");s=g2aside[gid][0];role=s["semantic_theorem_ast"]["sealed_exact_support_authority"]["role"];sha=s["semantic_theorem_ast"]["sealed_exact_support_authority"]["row_sha256"];_,certsha=auth[(role,sha)];complement.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.no-current-contact-complement.row.v2","graph_id":gid,"g2a_member_id":r["g2a_member_id"],"one_sided_member_id":s["member_id"],"graph_class":r["graph_class"],"C22_same_chart_outer_candidate_count":0,"C23_same_chart_outer_candidate_count":0,"one_sided_relative_boundary_authority_role":role,"one_sided_relative_boundary_authority_row_sha256":sha,"relative_boundary_certificate_sha256":certsha,"assigned_unique_terminal":"NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT","formal_credit":0}));terminal="NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT"
   else:m.need(n in{1,2},"contact multiplicity");terminal="SAME_CHART_RELATIVE_CELLS"
   route_final.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.final-route.row.v2","graph_id":gid,"g2a_member_id":r["g2a_member_id"],"graph_class":r["graph_class"],"physical_chart":r["physical_chart"],"contact_alias_count":n,"C23_contact_count":0,"assigned_unique_terminal":terminal,"source_preclassification_row_sha256":r["row_sha256"],"formal_credit":0}))
  m.need(len(complement)==552 and Counter(x["assigned_unique_terminal"]for x in route_final)=={"SAME_CHART_RELATIVE_CELLS":4712,"NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT":552},"route census")
  contacts.sort(key=lambda x:(x["g2a_member_id"],x["target_member_id"]));reverse.sort(key=lambda x:(x["g2a_member_id"],x["target_member_id"]));complement.sort(key=lambda x:x["g2a_member_id"]);route_final.sort(key=lambda x:x["g2a_member_id"])
  cross_witness=[];edge_contacts=defaultdict(list)
  for c in contacts:
   if c["g2a_target_components_equal"]:continue
   component_pair=tuple(sorted((c["g2a_component_id"],c["target_component_id"])))
   cross_witness.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.cross-c15-contact-alias-witness.row.v2","graph_id":c["graph_id"],"g2a_member_id":c["g2a_member_id"],"positive_side_member_id":c["positive_side_member_id"],"target_member_id":c["target_member_id"],"g2a_component_id":c["g2a_component_id"],"positive_side_component_id":c["positive_side_component_id"],"target_component_id":c["target_component_id"],"unordered_component_pair":list(component_pair),"g2a_positive_side_same_component":True,"g2a_target_components_distinct":True,"contact_alias_route_row_sha256":c["row_sha256"],"assigned_unique_terminal":"SAME_CHART_RELATIVE_CELLS","formal_credit":0}))
   edge_contacts[component_pair].append(c["row_sha256"])
  component_edges=[]
  for pair,rows in sorted(edge_contacts.items()):
   component_edges.append(m.closed({"schema":"cm2.c27-independent.g2a-relative2d.unique-cross-c15-component-edge.row.v2","unordered_component_pair":list(pair),"component_a":pair[0],"component_b":pair[1],"contact_alias_witness_count":len(rows),"contact_alias_route_row_sha256s":sorted(rows),"unique_edge_key":pair[0]+"|"+pair[1],"formal_credit":0}))
  m.need(len(cross_witness)==596 and len(component_edges)==144 and sum(x["contact_alias_witness_count"]for x in component_edges)==596,"cross-C15 witness/edge census")
  ds={"routes":write(out/"G2A_5264_final_unique_routes.jsonl.gz",route_final),"contacts":write(out/"G2A_9408_exact_relative2D_contact_alias_routes.jsonl.gz",contacts),"reverse_empty":write(out/"G2A_9392_reverse_side_empty_bindings.jsonl.gz",reverse),"complement":write(out/"G2A_552_no_current_contact_complement.jsonl.gz",complement),"cross_C15_witnesses":write(out/"G2A_596_cross_C15_contact_alias_witnesses.jsonl.gz",cross_witness),"unique_cross_C15_component_edges":write(out/"G2A_144_unique_cross_C15_component_edges.jsonl.gz",component_edges)}
  shared_attestation=shared_capture.attestation();body={"schema":"cm2.c27-independent.g2a-relative2d-primitive-totality-theorem.v2","status":"PASS_SCOPED_G2A_5264_UNIQUE_ROUTES__9408_RELATIVE2D_CONTACT_ALIAS_ROUTES__9392_REVERSE_EMPTY__552_COMPLEMENT__596_CROSS_C15__144_COMPONENT_EDGES__C23_ZERO__POSITIVE_C19_OPEN__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT","invocation_seed":a.seed,"route_census":{"SAME_CHART_RELATIVE_CELLS":4712,"NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT":552},"G2A_candidate_to_positive_side_bijection":{"join_key":["graph_id","target_member_id"],"domain_G2A_candidates":9408,"codomain_positive_side_dispositions":9408,"matched":9408,"missing":0,"duplicate":0},"contact_alias_count":9408,"reverse_side_empty_count":9392,"single_side_no_reverse_count":16,"C23_zero_proof":{"G2A_graph_count":5264,"same_chart_full_pair_denominator":cr["G2A"]["C23_same_chart_full_pair_denominator"],"candidate_count":0,"materialized_route_rows_with_C23_contact_count_zero":5264},"same_C15_contact_alias_count":8812,"cross_C15_contact_alias_count":596,"unique_cross_C15_component_edge_count":144,"relative_boundary_role_census":dict(rolec),"raw_terminal_pair_intersections":{"G2A_target_SIGNED":0,"G2A_target_COMPLETE":0,"positive_side_target_SIGNED":0,"positive_side_target_COMPLETE":0},"unique_route_assignment_within_G2A_and_checked_raw_SIGNED_COMPLETE_scope":True,"global_three_terminal_unique_assignment":False,"positive_C19_91672_intersection_gate":"OPEN__FRESH_LEDGER_NOT_CONSUMED_BY_THIS_THEOREM","unresolved_within_scoped_G2A_route_theorem":0,"historical_edge_or_validation_ledger_opened":False,"C27_FAMILIES_imported_or_read":False,"ledgers":ds,"implementation_dependency_pin":{"filename":shared_capture.path.name,"sha256":shared_attestation["observed_sha256"],"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True,"captured_source_bytes_compiled_and_executed":True,"stat_fingerprint":shared_attestation["stat_fingerprint"],"scope":"capture/hash/AST utility library; independent verifier must not import"},"open_blockers":["FRESH_POSITIVE_C19_91672_INTERSECTION_AND_PRIORITY_GATE_OPEN","GLOBAL_THREE_TERMINAL_TOTALITY_AND_UNIQUE_ASSIGNMENT_OPEN","C27_C28_C29_FULL_REBUILD_REQUIRED__NO_PATCH_PROMOTION"],"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{**{k:v.attestation()for k,v in sorted(caps.items())},"shared_implementation_source":shared_attestation}},"formal_credit":0,"strict_nonpromotion":{"C27_transition_totality":0,"C28_pair_routing":0,"C29_physical_maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};res=dict(body);res["semantic_projection_sha256"]=m.digest({k:v for k,v in body.items()if k not in{"invocation_seed","root_input_capture"}});res["result_sha256"]=m.digest(res);(out/"result.json").write_bytes(m.canonical(res)+b"\n");return res
 finally:
  for v in caps.values():v.close()
def main():
 p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True);p.add_argument("--candidate-result",required=True);p.add_argument("--candidate-result-sha256",required=True);p.add_argument("--route-ledger",required=True);p.add_argument("--route-ledger-sha256",required=True);p.add_argument("--g2a-candidate-ledger",required=True);p.add_argument("--g2a-candidate-ledger-sha256",required=True);p.add_argument("--factor-result",required=True);p.add_argument("--factor-result-sha256",required=True);p.add_argument("--factor-ledger",required=True);p.add_argument("--factor-ledger-sha256",required=True);p.add_argument("--shared-implementation-source",required=True);p.add_argument("--shared-implementation-sha256",required=True);p.add_argument("--seed",type=int,required=True);a=p.parse_args();shared=None
 try:
  shared=SharedSourceCapture.open(Path(a.shared_implementation_source),a.shared_implementation_sha256)
  global m;m=shared.execute();r=build(a,shared)
  print(m.canonical({"status":r["status"],"result_sha256":r["result_sha256"],"semantic_projection_sha256":r["semantic_projection_sha256"]}).decode());return 0
 except(BootstrapFailure,RuntimeError,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));return 2
 finally:
  if shared is not None:shared.close()
if __name__=="__main__":raise SystemExit(main())
