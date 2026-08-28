#!/usr/bin/env python3
"""Coherent attacks for the materialized 91,672 old-C15 edge adapter."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Callable

TERMINALS=("SIGNED_BOUNDARY_FACES","COMPLETE_BOUNDARY_FACES","POSITIVE_VOLUME_CARRIERS")
class Reject(RuntimeError):pass
def need(v:bool,m:str)->None:
    if not v:raise Reject(m)
def canon(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
def sha(v:Any)->str:return hashlib.sha256(canon(v)).hexdigest()
def close(r:dict[str,Any])->None:r.pop("row_sha256",None);r["row_sha256"]=sha(r)
def rows(p:Path)->list[dict[str,Any]]:
    with gzip.open(p,"rt") as f:return [json.loads(x) for x in f]
def check_closed(r:dict[str,Any],m:str)->None:
    b=dict(r);c=b.pop("row_sha256",None);need(c==sha(b),m)

def main()->int:
    ap=argparse.ArgumentParser()
    for n in ("priority","c15","strict","g2a","witness","edges"):ap.add_argument("--"+n,type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
    c15={r["registry_member_id"]:r["fresh_component_id"] for r in rows(args.c15)};need(len(c15)==502204,"C15")
    expected_w=[]
    for r in rows(args.priority):
        p=(r["left_member_id"],r["right_member_id"]);cs=(c15[p[0]],c15[p[1]])
        if cs[0]==cs[1]:continue
        e=tuple(sorted(cs));b={"assigned_terminal":r["assigned_terminal"],"formal_credit":0,"member_pair":list(p),"old_C15_component_pair":list(e),"positive_primitive_row_sha256":r["positive_primitive_row_sha256"],"priority_route_row_sha256":r["row_sha256"],"schema":"cm2.c27-independent.current-support-91672.old-c15-cross-member-witness.row.v1"};close(b);expected_w.append(b)
    expected_w.sort(key=lambda r:(r["old_C15_component_pair"],r["member_pair"],r["assigned_terminal"]));need(len(expected_w)==32012,"expected witnesses")
    strict={tuple(sorted(r["component_pair"])) for r in rows(args.strict)};g2a={tuple(sorted(r["unordered_component_pair"])) for r in rows(args.g2a)}
    grouped=defaultdict(list)
    for r in expected_w:grouped[tuple(r["old_C15_component_pair"])].append(r)
    expected_e=[];cursor=0
    for e in sorted(grouped):
        ws=grouped[e];tc=Counter(r["assigned_terminal"] for r in ws);h=hashlib.sha256()
        for r in ws:h.update(r["row_sha256"].encode()+b"\n")
        b={"formal_credit":0,"member_witness_ordinal_range":[cursor,cursor+len(ws)],"old_C15_component_pair":list(e),"overlaps_G2A_component_edge":e in g2a,"overlaps_strict_volume_component_edge":e in strict,"schema":"cm2.c27-independent.current-support-91672.unique-old-c15-component-edge.row.v1","source_terminal_member_pair_census":{t:tc[t] for t in TERMINALS},"supporting_member_pair_count":len(ws),"supporting_witness_row_sequence_sha256":h.hexdigest(),"unique_edge_key":"|".join(e)};close(b);expected_e.append(b);cursor+=len(ws)
    need(len(expected_e)==14620 and cursor==32012,"expected edges")
    base_w,base_e=rows(args.witness),rows(args.edges)
    def validate(w:list[dict[str,Any]],e:list[dict[str,Any]])->None:
        need(len(w)==32012 and len(e)==14620,"census")
        for i,(x,y) in enumerate(zip(w,expected_w)):check_closed(x,f"w:{i}:closure");need(x==y,f"w:{i}:semantics")
        for i,(x,y) in enumerate(zip(e,expected_e)):check_closed(x,f"e:{i}:closure");need(x==y,f"e:{i}:semantics")
    validate(base_w,base_e)
    attacks=[]
    def attack(name:str,kind:str,index:int,mut:Callable[[dict[str,Any]],None],reclose=True):attacks.append((name,kind,index,mut,reclose))
    attack("witness_member_flip","w",0,lambda r:r["member_pair"].__setitem__(0,"forged"))
    attack("witness_component_flip","w",1,lambda r:r["old_C15_component_pair"].__setitem__(0,"forged"))
    attack("witness_terminal_signed_forge","w",2,lambda r:r.__setitem__("assigned_terminal","SIGNED_BOUNDARY_FACES"))
    attack("witness_terminal_complete_forge","w",3,lambda r:r.__setitem__("assigned_terminal","COMPLETE_BOUNDARY_FACES"))
    attack("witness_priority_hash_flip","w",4,lambda r:r.__setitem__("priority_route_row_sha256","0"*64))
    attack("witness_positive_hash_flip","w",5,lambda r:r.__setitem__("positive_primitive_row_sha256","0"*64))
    attack("witness_formal_credit_flip","w",6,lambda r:r.__setitem__("formal_credit",1))
    attack("witness_schema_flip","w",7,lambda r:r.__setitem__("schema",r["schema"]+".X"))
    attack("witness_closure_flip","w",8,lambda r:r.__setitem__("row_sha256","0"*64),False)
    attack("edge_component_flip","e",0,lambda r:r["old_C15_component_pair"].__setitem__(0,"forged"))
    attack("edge_range_gap","e",1,lambda r:r["member_witness_ordinal_range"].__setitem__(0,r["member_witness_ordinal_range"][0]+1))
    attack("edge_range_overlap","e",2,lambda r:r["member_witness_ordinal_range"].__setitem__(1,r["member_witness_ordinal_range"][1]+1))
    attack("edge_count_flip","e",3,lambda r:r.__setitem__("supporting_member_pair_count",r["supporting_member_pair_count"]+1))
    attack("edge_signed_census_forge","e",4,lambda r:r["source_terminal_member_pair_census"].__setitem__("SIGNED_BOUNDARY_FACES",1))
    attack("edge_complete_census_forge","e",5,lambda r:r["source_terminal_member_pair_census"].__setitem__("COMPLETE_BOUNDARY_FACES",1))
    attack("edge_positive_census_flip","e",6,lambda r:r["source_terminal_member_pair_census"].__setitem__("POSITIVE_VOLUME_CARRIERS",0))
    attack("edge_sequence_hash_flip","e",7,lambda r:r.__setitem__("supporting_witness_row_sequence_sha256","0"*64))
    attack("edge_strict_overlap_flip","e",8,lambda r:r.__setitem__("overlaps_strict_volume_component_edge",False))
    attack("edge_G2A_overlap_flip","e",next(i for i,r in enumerate(base_e) if r["overlaps_G2A_component_edge"]),lambda r:r.__setitem__("overlaps_G2A_component_edge",False))
    attack("edge_key_flip","e",10,lambda r:r.__setitem__("unique_edge_key","forged"))
    attack("edge_formal_credit_flip","e",11,lambda r:r.__setitem__("formal_credit",1))
    attack("edge_schema_flip","e",12,lambda r:r.__setitem__("schema",r["schema"]+".X"))
    attack("edge_closure_flip","e",13,lambda r:r.__setitem__("row_sha256","0"*64),False)
    results=[]
    for ordinal,(name,kind,index,mut,reclose) in enumerate(attacks):
        w,e=list(base_w),list(base_e);target=copy.deepcopy(w[index] if kind=="w" else e[index]);mut(target)
        if reclose:close(target)
        (w if kind=="w" else e)[index]=target
        try:validate(w,e)
        except Reject as ex:reason=str(ex)
        else:raise RuntimeError("accepted:"+name)
        b={"attack":name,"ordinal":ordinal,"rejected":True,"rejection_reason":reason,"schema":"cm2.c27-independent.current-support-91672.old-c15-edge.attack-row.v1"};close(b);results.append(b)
    # Sequence-level omission, duplication and reordering attacks.
    for name,w,e in [("witness_omission",base_w[:-1],base_e),("witness_duplication",base_w+[base_w[-1]],base_e),("edge_omission",base_w,base_e[:-1]),("edge_duplication",base_w,base_e+[base_e[-1]]),("witness_reorder",[base_w[1],base_w[0]]+base_w[2:],base_e),("edge_reorder",base_w,[base_e[1],base_e[0]]+base_e[2:])]:
        try:validate(w,e)
        except Reject as ex:reason=str(ex)
        else:raise RuntimeError("accepted:"+name)
        b={"attack":name,"ordinal":len(results),"rejected":True,"rejection_reason":reason,"schema":"cm2.c27-independent.current-support-91672.old-c15-edge.attack-row.v1"};close(b);results.append(b)
    result={"schema":"cm2.c27-independent.current-support-91672.old-c15-edge.attacks.v1","status":"PASS_ALL_COHERENT_EDGE_AND_WITNESS_ATTACKS_REJECTED__ZERO_CREDIT","attack_count":len(results),"rejected_count":len(results),"accepted_count":0,"formal_credit":0,"manifest_authorized":False,"Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM","attacks":results};result["result_sha256"]=sha(result);args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(canon(result)+b"\n");print(canon({"rejected":len(results),"result_sha256":result["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
