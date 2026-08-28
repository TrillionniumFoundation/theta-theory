#!/usr/bin/env python3
"""Coherent local-row and aggregate attacks for the 483,232 scoped atom join."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Callable,Iterator
T=("SIGNED_BOUNDARY_FACES","COMPLETE_BOUNDARY_FACES","POSITIVE_VOLUME_CARRIERS")
class Reject(RuntimeError):pass
def need(v:bool,m:str):
    if not v:raise Reject(m)
def canon(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
def sha(v:Any)->str:return hashlib.sha256(canon(v)).hexdigest()
def close(r:dict[str,Any]):r.pop("row_sha256",None);r["row_sha256"]=sha(r)
def rows(p:Path)->Iterator[dict[str,Any]]:
    with gzip.open(p,"rt") as f:
        for x in f:yield json.loads(x)
def main()->int:
    ap=argparse.ArgumentParser()
    for n in("atoms","priority","c15","endpoint-authority","join-ledger","join-result"):ap.add_argument("--"+n,type=Path,required=True)
    ap.add_argument("--join-ledger-sha256",required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args()
    need(hashlib.sha256(a.join_ledger.read_bytes()).hexdigest()==a.join_ledger_sha256,"baseline ledger pin")
    c15={r["registry_member_id"]:r["fresh_component_id"] for r in rows(a.c15)}
    ep={r["member_id"]:r for r in rows(a.endpoint_authority)}
    inc=defaultdict(list)
    for r in rows(a.priority):
        p=(r["left_member_id"],r["right_member_id"]);t=r["assigned_terminal"]
        inc[p[0]].append({"assigned_terminal":t,"other_member_id":p[1],"pair_key":"|".join(p),"priority_route_row_sha256":r["row_sha256"]});inc[p[1]].append({"assigned_terminal":t,"other_member_id":p[0],"pair_key":"|".join(p),"priority_route_row_sha256":r["row_sha256"]})
    for v in inc.values():v.sort(key=lambda r:(r["other_member_id"],r["assigned_terminal"],r["priority_route_row_sha256"]))
    def expected(atom:dict[str,Any])->dict[str,Any]:
        owner=atom["owner_member_id"]
        if atom["source_kernel"]=="C19C":
            e=ep[owner];x=e["endpoint_inclusion_bits"];bits=[x["t_lower_closed"],x["t_upper_closed"],x["p_lower_closed"],x["p_upper_closed"],x["s_lower_closed"],x["s_upper_closed"]];eb={"authority_row_sha256":e["row_sha256"],"authority_rule":e["authority_rule"],"source":"C19C_ENDPOINT_OWNERSHIP_V3"}
        else:bits=atom["endpoint_inclusion_flags_lower_upper_t_p_s"];eb={"authority_row_sha256":atom["row_sha256"],"authority_rule":"PRIMITIVE_OPEN_SUPPORT","source":"FROZEN_PRIMITIVE_ATOM_ROW"}
        ir=inc.get(owner,[]);tc=Counter(r["assigned_terminal"] for r in ir);ts=[t for t in T if tc[t]];d="INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS" if ir else "EXACT_COMPLEMENT__OWNER_ABSENT_FROM_ALL_91672_PAIR_ROUTE_ENDPOINTS"
        o={"atom_id":atom["atom_id"],"atom_source_row_sha256":atom["source_row_sha256"],"atom_source_kernel":atom["source_kernel"],"candidate_disposition":d,"candidate_incidence_count":len(ir),"current_C15_component":c15[owner],"effective_endpoint_inclusion_flags_lower_upper_t_p_s":bits,"endpoint_authority_binding":eb,"formal_credit":0,"incident_pair_routes":ir,"owner_member_id":owner,"pair_routes_each_have_unique_terminal_assignment":True,"schema":"cm2.c27-independent.current-support-483232.atom-incidence-complement.row.v1","terminal_incidence_census":{t:tc[t] for t in T},"terminal_incidence_set":ts};close(o);return o
    samples=[];seen=set()
    for atom,out in zip(rows(a.atoms),rows(a.join_ledger)):
        need(out==expected(atom),"baseline lockstep")
        key=(atom["source_kernel"],out["candidate_disposition"],len(out["terminal_incidence_set"]))
        if key not in seen:seen.add(key);samples.append((atom,out))
        if len(samples)>=14 and any(len(x[1]["terminal_incidence_set"])==3 for x in samples):break
    need(samples,"samples")
    def validate(atom,row):need(row==expected(atom),"local exact semantics")
    base_atom,base=samples[0];c19=next(x for x in samples if x[0]["source_kernel"]=="C19C");incident=next(x for x in samples if x[1]["candidate_incidence_count"]>0);multi=next(x for x in samples if len(x[1]["terminal_incidence_set"])>1)
    cases=[]
    def add(n,pair,mut:Callable[[dict[str,Any]],None],reclose=True):cases.append((n,pair,mut,reclose))
    add("atom_id_flip",(base_atom,base),lambda r:r.__setitem__("atom_id","forged"));add("owner_flip",(base_atom,base),lambda r:r.__setitem__("owner_member_id","forged"));add("kernel_flip",(base_atom,base),lambda r:r.__setitem__("atom_source_kernel","C19C"));add("source_row_flip",(base_atom,base),lambda r:r.__setitem__("atom_source_row_sha256","0"*64));add("C15_component_flip",(base_atom,base),lambda r:r.__setitem__("current_C15_component","forged"));add("disposition_flip",(base_atom,base),lambda r:r.__setitem__("candidate_disposition","INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS"));add("endpoint_bit_flip",c19,lambda r:r["effective_endpoint_inclusion_flags_lower_upper_t_p_s"].__setitem__(0,not r["effective_endpoint_inclusion_flags_lower_upper_t_p_s"][0]));add("endpoint_authority_hash_flip",c19,lambda r:r["endpoint_authority_binding"].__setitem__("authority_row_sha256","0"*64));add("endpoint_source_flip",c19,lambda r:r["endpoint_authority_binding"].__setitem__("source","FROZEN_PRIMITIVE_ATOM_ROW"));add("incidence_count_flip",incident,lambda r:r.__setitem__("candidate_incidence_count",r["candidate_incidence_count"]+1));add("incident_route_drop",incident,lambda r:r["incident_pair_routes"].pop());add("incident_route_duplicate",incident,lambda r:r["incident_pair_routes"].append(copy.deepcopy(r["incident_pair_routes"][0])));add("incident_other_member_flip",incident,lambda r:r["incident_pair_routes"][0].__setitem__("other_member_id","forged"));add("incident_terminal_flip",incident,lambda r:r["incident_pair_routes"][0].__setitem__("assigned_terminal","COMPLETE_BOUNDARY_FACES"));add("incident_pair_key_flip",incident,lambda r:r["incident_pair_routes"][0].__setitem__("pair_key","forged"));add("incident_route_hash_flip",incident,lambda r:r["incident_pair_routes"][0].__setitem__("priority_route_row_sha256","0"*64));add("terminal_census_flip",multi,lambda r:r["terminal_incidence_census"].__setitem__("SIGNED_BOUNDARY_FACES",999));add("terminal_set_drop",multi,lambda r:r["terminal_incidence_set"].pop());add("pair_unique_flag_flip",incident,lambda r:r.__setitem__("pair_routes_each_have_unique_terminal_assignment",False));add("formal_credit_flip",incident,lambda r:r.__setitem__("formal_credit",1));add("schema_flip",incident,lambda r:r.__setitem__("schema",r["schema"]+".X"));add("row_closure_flip",incident,lambda r:r.__setitem__("row_sha256","0"*64),False)
    outcomes=[]
    for i,(n,(atom,row),mut,reclose) in enumerate(cases):
        x=copy.deepcopy(row);mut(x)
        if reclose:close(x)
        try:validate(atom,x)
        except Reject as e:reason=str(e)
        else:raise RuntimeError("accepted:"+n)
        b={"attack":n,"ordinal":i,"rejected":True,"reason":reason,"schema":"cm2.c27-independent.current-support-483232.atom-join.attack-row.v1"};close(b);outcomes.append(b)
    result=json.load(open(a.join_result));aggregate=[("result_incident_flip",lambda r:r["incidence_complement"].__setitem__("incident_atoms",62239)),("result_complement_flip",lambda r:r["incidence_complement"].__setitem__("complement_atoms",420993)),("result_endpoint_flip",lambda r:r["endpoint_v3_join"].__setitem__("C19C_rows",33343)),("result_output_hash_flip",lambda r:r["output"].__setitem__("file_sha256","0"*64)),("result_formal_credit_flip",lambda r:r.__setitem__("formal_credit",1)),("result_global_promotion",lambda r:r.__setitem__("CM2","GO"))]
    for n,mut in aggregate:
        x=copy.deepcopy(result);mut(x);x.pop("result_sha256",None);x["result_sha256"]=sha(x)
        ok=(x["incidence_complement"]["incident_atoms"]==62240 and x["incidence_complement"]["complement_atoms"]==420992 and x["endpoint_v3_join"]["C19C_rows"]==33344 and x["output"]["file_sha256"]==a.join_ledger_sha256 and x["formal_credit"]==0 and x["CM2"]=="NO-GO_FOR_CLAIM")
        need(not ok,"aggregate attack rejected")
        b={"attack":n,"ordinal":len(outcomes),"rejected":True,"reason":"aggregate exact contract","schema":"cm2.c27-independent.current-support-483232.atom-join.attack-row.v1"};close(b);outcomes.append(b)
    out={"schema":"cm2.c27-independent.current-support-483232.atom-join.attacks.v1","status":"PASS_ALL_COHERENT_ATOM_JOIN_ATTACKS_REJECTED__ZERO_CREDIT","attack_count":len(outcomes),"rejected_count":len(outcomes),"accepted_count":0,"formal_credit":0,"manifest_authorized":False,"Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM","attacks":outcomes};out["result_sha256"]=sha(out);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(canon(out)+b"\n");print(canon({"rejected":len(outcomes),"result_sha256":out["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
