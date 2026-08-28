#!/usr/bin/env python3
"""Full-union 101,080 pair routes to the 483,232 primitive-atom denominator.

Current positive routes bind their unique primitive atom witness; boundary-face
routes bind the full member support union; C24A G2B binds exactly its C22 target
atom and never adds its C24A source or the G2A diagnostic alias as a candidate.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,stat
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterator
T=("SIGNED_BOUNDARY_FACES","COMPLETE_BOUNDARY_FACES","POSITIVE_VOLUME_CARRIERS")
class Fail(RuntimeError):pass
def need(v:bool,m:str):
    if type(v)is not bool or not v:raise Fail(m)
def canon(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def sha(v:Any)->str:return hashlib.sha256(canon(v)).hexdigest()
def closed(r:dict[str,Any],m:str):
    b=dict(r);c=b.pop("row_sha256",None);need(c==sha(b),m)
def fp(s:os.stat_result)->tuple[int,...]:return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
class Cap:
    def __init__(self,n:str,p:Path,x:str):
        self.n,self.p=n,p;self.fd=os.open(p,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0));s=os.fstat(self.fd);need(stat.S_ISREG(s.st_mode),n+":regular");self.pre=fp(s);h=hashlib.sha256()
        while b:=os.read(self.fd,4<<20):h.update(b)
        self.h=h.hexdigest();need(self.h==x,n+":pin");need(fp(os.fstat(self.fd))==self.pre,n+":hash-fstat")
    def rows(self)->Iterator[dict[str,Any]]:
        os.lseek(self.fd,0,os.SEEK_SET)
        with os.fdopen(os.dup(self.fd),"rb")as raw:
            with gzip.GzipFile(fileobj=raw,mode="rb")as z:
                for i,line in enumerate(z):need(line.endswith(b"\n"),f"{self.n}:{i}:newline");r=json.loads(line);need(canon(r)==line[:-1],f"{self.n}:{i}:canonical");closed(r,f"{self.n}:{i}:closure");yield r
        need(fp(os.fstat(self.fd))==self.pre,self.n+":rows-fstat")
    def doc(self)->dict[str,Any]:
        os.lseek(self.fd,0,os.SEEK_SET);a=[]
        while b:=os.read(self.fd,4<<20):a.append(b)
        need(fp(os.fstat(self.fd))==self.pre,self.n+":doc-fstat");return json.loads(b"".join(a))
    def rec(self):need(fp(os.fstat(self.fd))==self.pre,self.n+":final");return{"path":str(self.p),"sha256":self.h,"stat_fingerprint":list(self.pre),"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True}
    def close(self):os.close(self.fd)
def rep_atom_id(x:str)->str:
    source,h=x.split(":",1);return source.lower()+"-support-atom:"+h
def main()->int:
    ap=argparse.ArgumentParser()
    for n in("atoms","union-ledger","union-result","current-priority","current-positive","g2b-exact","g2b-receipt","c15","endpoint-authority","endpoint-receipt"):
        ap.add_argument("--"+n,type=Path,required=True);ap.add_argument("--"+n+"-sha256",required=True)
    ap.add_argument("--out-dir",type=Path,required=True);ap.add_argument("--seed",type=int,required=True);a=ap.parse_args();caps={}
    try:
        for n in("atoms","union_ledger","union_result","current_priority","current_positive","g2b_exact","g2b_receipt","c15","endpoint_authority","endpoint_receipt"):caps[n]=Cap(n,getattr(a,n),getattr(a,n+"_sha256"))
        ur=caps["union_result"].doc();b=dict(ur);uclaimed=b.pop("result_sha256");need(uclaimed==sha(b) and ur["formal_credit"]==0 and ur["ledgers"]["unique_ownership"]["file_sha256"]==a.union_ledger_sha256 and ur["ledgers"]["unique_ownership"]["row_count"]==101080,"union result authority")
        er=caps["endpoint_receipt"].doc();b=dict(er);eclaimed=b.pop("receipt_sha256");need(eclaimed==sha(b) and er["byte_identical_dual_seed_ledgers"]["authority"]["sha256"]==a.endpoint_authority_sha256,"endpoint receipt")
        gr=caps["g2b_receipt"].doc();b=dict(gr);gclaimed=b.pop("result_sha256");need(gclaimed==sha(b) and gr["status"]=="PASS_TERMINAL_DIAGNOSTIC_C24A_G2B_EXACT_ROUTE__ZERO_FORMAL_CREDIT","G2B receipt")
        c15={r["registry_member_id"]:r["fresh_component_id"] for r in caps["c15"].rows()};need(len(c15)==502204,"C15")
        endpoint={r["member_id"]:r for r in caps["endpoint_authority"].rows()};need(len(endpoint)==33344,"endpoint")
        atom_by_source={};atoms_by_owner=defaultdict(list);atom_owner={};source_census=Counter();atom_count=0
        for r in caps["atoms"].rows():
            atom_count+=1;aid=r["atom_id"];owner=r["owner_member_id"];key=(r["source_kernel"],r["source_row_sha256"]);need(aid not in atom_owner and key not in atom_by_source,"atom unique");atom_owner[aid]=owner;atom_by_source[key]=aid;atoms_by_owner[owner].append(aid);source_census[r["source_kernel"]]+=1
        need(atom_count==483232 and len(atoms_by_owner)==482380,"atom denominator")
        current={}
        for r in caps["current_priority"].rows():need(r["row_sha256"]not in current,"current row unique");current[r["row_sha256"]]=r
        need(len(current)==91672,"current rows")
        positive={}
        for r in caps["current_positive"].rows():need(r["row_sha256"]not in positive and r["atom_overlap_witness_count"]==1,"positive unique witness");positive[r["row_sha256"]]=r
        need(len(positive)==55532,"positive rows")
        g2b={}
        for r in caps["g2b_exact"].rows():need(r["row_sha256"]not in g2b,"G2B unique");g2b[r["row_sha256"]]=r
        need(len(g2b)==18800,"G2B exact rows")
        incid=defaultdict(list);pairs=set();terminal=Counter();authority=Counter();binding=Counter();c24_sources=set();c24_target_atoms=set();g2a_alias=0
        for u in caps["union_ledger"].rows():
            pair=tuple(u["pair_key"]);need(pair[0]<pair[1] and pair not in pairs,"union pair unique");pairs.add(pair);t=u["assigned_terminal"];need(t in T,"exact terminal grammar");terminal[t]+=1;auth=u["source_authority"];authority[auth]+=1
            common={"assigned_terminal":t,"pair_key":"|".join(pair),"source_authority":auth,"union_route_row_sha256":u["row_sha256"]}
            if auth=="CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER":
                r=current.get(u["source_row_sha256"]);need(r is not None and tuple((r["left_member_id"],r["right_member_id"]))==pair and r["assigned_terminal"]==t and u["current_source_terminal"]==t,"current union binding")
                if t=="POSITIVE_VOLUME_CARRIERS":
                    p=positive.get(r["positive_primitive_row_sha256"]);need(p is not None and (p["left_member_id"],p["right_member_id"])==pair,"current positive binding")
                    aids=[rep_atom_id(x) for x in p["representative_atom_ids"]];need(len(aids)==2 and set(atom_owner[x] for x in aids)==set(pair),"current exact atom witness")
                    for aid in aids:
                        q=dict(common);q.update({"atom_binding_mode":"EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS","source_evidence_row_sha256":p["row_sha256"]});incid[aid].append(q);binding[q["atom_binding_mode"]]+=1
                else:
                    for member in pair:
                        aids=atoms_by_owner.get(member);need(bool(aids),"boundary owner atom support")
                        for aid in aids:
                            q=dict(common);q.update({"atom_binding_mode":"MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE","source_evidence_row_sha256":r["row_sha256"]});incid[aid].append(q);binding[q["atom_binding_mode"]]+=1
            elif auth=="C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":
                need(t=="POSITIVE_VOLUME_CARRIERS" and u["current_source_terminal"]is None and u["positive_support_branch"]=="C24A_G2B_EXACT_FACTOR_SIGN_POSITIVE_WITH_G2A_RELATIVE_BOUNDARY_DIAGNOSTIC","C24 terminal ownership")
                x=g2b.get(u["C24A_G2B_exact_row_sha256"]);need(x is not None and x["disposition"]=="EXACT_POSITIVE_SUPPORT" and pair==(x["c24_member_id"],x["target_member_id"]),"C24 exact binding")
                need(not atoms_by_owner.get(x["c24_member_id"]),"C24 source outside denominator");aid=atom_by_source.get(("C22A",x["C22_target_row_sha256"]));need(aid is not None and atom_owner[aid]==x["target_member_id"],"C24 exact C22 target atom")
                q=dict(common);q.update({"atom_binding_mode":"EXACT_C24A_G2B_C22_TARGET_ATOM","source_evidence_row_sha256":x["row_sha256"]});incid[aid].append(q);binding[q["atom_binding_mode"]]+=1;c24_sources.add(x["c24_member_id"]);c24_target_atoms.add(aid);need(u["G2A_diagnostic_alias_row_sha256"]is not None,"G2A diagnostic binding");g2a_alias+=1
            else:raise Fail("union source authority")
        need(len(pairs)==101080 and authority=={"CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER":91672,"C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":9408},"union authority census")
        need(terminal=={"SIGNED_BOUNDARY_FACES":25452,"COMPLETE_BOUNDARY_FACES":10688,"POSITIVE_VOLUME_CARRIERS":64940} and g2a_alias==9408,"union terminal census")
        for v in incid.values():v.sort(key=lambda r:(r["pair_key"],r["source_authority"],r["atom_binding_mode"],r["union_route_row_sha256"]))
        a.out_dir.mkdir(parents=True,exist_ok=False);out=a.out_dir/"full_union_101080_on_483232_atom_incidence_or_complement.jsonl.gz";rowseq=hashlib.sha256();atomids=hashlib.sha256();disp=Counter();sets=Counter();presence=Counter();multi=0;expanded=0;seen_ep=set()
        with out.open("wb")as raw:
            with gzip.GzipFile(fileobj=raw,mode="wb",mtime=0,filename="")as z:
                for atom in caps["atoms"].rows():
                    aid=atom["atom_id"];owner=atom["owner_member_id"]
                    if atom["source_kernel"]=="C19C":
                        e=endpoint.get(owner);need(e is not None and e["C19C_row_sha256"]==atom["source_row_sha256"] and e["chart"]==atom["chart"] and e["bounds"]==[q["value"]for q in atom["physical_bounds"]],"C19C endpoint exact join");x=e["endpoint_inclusion_bits"];bits=[x["t_lower_closed"],x["t_upper_closed"],x["p_lower_closed"],x["p_upper_closed"],x["s_lower_closed"],x["s_upper_closed"]];eb={"authority_row_sha256":e["row_sha256"],"authority_rule":e["authority_rule"],"source":"C19C_ENDPOINT_OWNERSHIP_V3"};seen_ep.add(owner)
                    else:bits=atom["endpoint_inclusion_flags_lower_upper_t_p_s"];need(bits==[False]*6,"open endpoint");eb={"authority_row_sha256":atom["row_sha256"],"authority_rule":"PRIMITIVE_OPEN_SUPPORT","source":"FROZEN_PRIMITIVE_ATOM_ROW"}
                    ir=incid.get(aid,[]);expanded+=len(ir);tc=Counter(r["assigned_terminal"]for r in ir);ts=tuple(t for t in T if tc[t]);sets[ts]+=1
                    for t in ts:presence[t]+=1
                    if len(ts)>1:multi+=1
                    d="INCIDENT_TO_FULL_101080_UNION_PAIR_ROUTES"if ir else"EXACT_COMPLEMENT__ATOM_ABSENT_FROM_ALL_FULL_UNION_ROUTE_INCIDENCES";disp[d]+=1
                    r={"atom_id":aid,"atom_source_kernel":atom["source_kernel"],"atom_source_row_sha256":atom["source_row_sha256"],"candidate_disposition":d,"candidate_incidence_count":len(ir),"current_C15_component":c15[owner],"effective_endpoint_inclusion_flags_lower_upper_t_p_s":bits,"endpoint_authority_binding":eb,"formal_credit":0,"incident_union_pair_routes":ir,"owner_member_id":owner,"pair_routes_each_have_unique_20_terminal_ownership":True,"schema":"cm2.c27-independent.full-union-101080-on-483232.atom-incidence-complement.row.v1","terminal_incidence_census":{t:tc[t]for t in T},"terminal_incidence_set":list(ts)};r["row_sha256"]=sha(r);z.write(canon(r)+b"\n");rowseq.update(r["row_sha256"].encode()+b"\n");atomids.update(aid.encode()+b"\n")
        need(seen_ep==set(endpoint) and sum(disp.values())==483232,"atom output totality");fh=hashlib.sha256(out.read_bytes()).hexdigest();att={k:v.rec()for k,v in sorted(caps.items())}
        result={"schema":"cm2.c27-independent.full-union-101080-on-483232.atom-incidence-complement.result.v1","status":"PASS_FULL_UNION_101080_PAIR_OWNERSHIP_MATERIALIZED_ON_ALL_483232_ATOMS__G2B_IS_POSITIVE_VOLUME_NOT_SAME_CHART__G2A_ALIAS_NOT_COUNTED__ZERO_CREDIT","formal_credit":0,"manifest_authorized":False,"pair_union":{"pairs":101080,"by_terminal":{t:terminal[t]for t in T},"current_pairs":91672,"C24A_G2B_positive_pairs":9408,"G2A_alias_independent_candidate_count":0,"G2B_20_terminal_owner":"POSITIVE_VOLUME_CARRIERS","G2B_assigned_to_SAME_CHART_RELATIVE_CELLS":False},"atom_denominator":{"atoms":483232,"source_census":dict(sorted(source_census.items())),"atom_ids_sha256":atomids.hexdigest(),"incident_atoms":disp["INCIDENT_TO_FULL_101080_UNION_PAIR_ROUTES"],"exact_complement_atoms":disp["EXACT_COMPLEMENT__ATOM_ABSENT_FROM_ALL_FULL_UNION_ROUTE_INCIDENCES"],"expanded_atom_route_incidences":expanded,"multi_terminal_incident_atoms":multi,"terminal_atom_presence":{t:presence[t]for t in T},"terminal_set_atom_census":{"|".join(k)if k else"COMPLEMENT":v for k,v in sorted(sets.items())}},"binding_census":dict(sorted(binding.items())),"C24A_scope":{"distinct_C24A_sources_outside_atom_denominator":len(c24_sources),"C24A_source_rows_added_to_atom_denominator":0,"distinct_exact_C22_target_atoms":len(c24_target_atoms),"G2A_alias_rows_bound_but_not_counted":g2a_alias},"C19C_endpoint_v3_rows":len(seen_ep),"output":{"filename":out.name,"row_count":483232,"file_sha256":fh,"row_sequence_sha256":rowseq.hexdigest()},"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":att},"scope_governance":{"three_terminal_atom_incidence_or_complement_contract":"MATERIALIZED_FULL_UNION","other_20_family_terminals_and_C27_C28_C29_full_rebuild":"STILL_REQUIRED","C27_FAMILIES_imported_or_read":False,"historical_edge_ledger_used_as_candidate_universe":False},"C27_C28_C29":"FULL_REBUILD_REQUIRED","Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM"};result["result_sha256"]=sha(result);(a.out_dir/"result.json").write_bytes(canon(result)+b"\n");print(canon({"status":result["status"],"result_sha256":result["result_sha256"],"incident_atoms":result["atom_denominator"]["incident_atoms"],"complement_atoms":result["atom_denominator"]["exact_complement_atoms"]}).decode());return 0
    except(Fail,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));return 2
    finally:
        for c in caps.values():c.close()
if __name__=="__main__":raise SystemExit(main())
