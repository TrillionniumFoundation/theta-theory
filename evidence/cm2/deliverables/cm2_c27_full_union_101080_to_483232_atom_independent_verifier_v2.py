#!/usr/bin/env python3
"""Independent inverse-incidence audit of the full 101,080→483,232 join."""
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
def closed(r:dict[str,Any],m:str):b=dict(r);c=b.pop("row_sha256",None);need(c==sha(b),m)
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
    def doc(self):
        os.lseek(self.fd,0,os.SEEK_SET);a=[]
        while b:=os.read(self.fd,4<<20):a.append(b)
        need(fp(os.fstat(self.fd))==self.pre,self.n+":doc-fstat");return json.loads(b"".join(a))
    def rec(self):need(fp(os.fstat(self.fd))==self.pre,self.n+":final");return{"path":str(self.p),"sha256":self.h,"stat_fingerprint":list(self.pre),"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True}
    def close(self):os.close(self.fd)
def same(a:Cap,b:Cap)->bool:
    if a.pre[2]!=b.pre[2]:return False
    off=0
    while off<a.pre[2]:
        x=os.pread(a.fd,4<<20,off);y=os.pread(b.fd,4<<20,off)
        if x!=y:return False
        off+=len(x)
    return True
def rkey(x:str)->tuple[str,str]:
    s,h=x.split(":",1);need(s in {"C19A","C19B","C19C","C20A","C22A","C23A"} and len(h)==64,"positive representative source key");return s,h
def main()->int:
    ap=argparse.ArgumentParser()
    for n in("atoms","union-ledger","current-priority","current-positive","g2b-exact","c15","endpoint-authority","seed1-result","seed1-ledger","seed2-result","seed2-ledger"):
        ap.add_argument("--"+n,type=Path,required=True);ap.add_argument("--"+n+"-sha256",required=True)
    ap.add_argument("--out-dir",type=Path,required=True);a=ap.parse_args();caps={}
    try:
        for n in("atoms","union_ledger","current_priority","current_positive","g2b_exact","c15","endpoint_authority","seed1_result","seed1_ledger","seed2_result","seed2_ledger"):caps[n]=Cap(n,getattr(a,n),getattr(a,n+"_sha256"))
        need(same(caps["seed1_ledger"],caps["seed2_ledger"]),"dual join byte identity")
        c15={r["registry_member_id"]:r["fresh_component_id"]for r in caps["c15"].rows()};endpoint={r["member_id"]:r for r in caps["endpoint_authority"].rows()};need(len(c15)==502204 and len(endpoint)==33344,"authorities")
        atom={};atoms_by_owner=defaultdict(list);by_source={}
        for r in caps["atoms"].rows():aid=r["atom_id"];need(aid not in atom,"atom unique");atom[aid]=r;atoms_by_owner[r["owner_member_id"]].append(aid);by_source[(r["source_kernel"],r["source_row_sha256"])]=aid
        need(len(atom)==483232,"atom census")
        current={r["row_sha256"]:r for r in caps["current_priority"].rows()};positive={r["row_sha256"]:r for r in caps["current_positive"].rows()};g2b={r["row_sha256"]:r for r in caps["g2b_exact"].rows()};need(len(current)==91672 and len(positive)==55532 and len(g2b)==18800,"route inputs")
        union={};expected={};terminal=Counter();mode=Counter()
        for u in caps["union_ledger"].rows():
            us=u["row_sha256"];need(us not in union,"union unique");union[us]=u;t=u["assigned_terminal"];terminal[t]+=1;pair=tuple(u["pair_key"])
            if u["source_authority"]=="CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER":
                r=current[u["source_row_sha256"]];need((r["left_member_id"],r["right_member_id"])==pair and r["assigned_terminal"]==t,"current binding")
                if t=="POSITIVE_VOLUME_CARRIERS":
                    p=positive[r["positive_primitive_row_sha256"]];need((p["left_member_id"],p["right_member_id"])==pair,"positive pair binding");keys=[rkey(x)for x in p["representative_atom_ids"]];need([k[0]for k in keys]==p["representative_sources"],"positive representative source agreement");aids=tuple(sorted(by_source.get(k)for k in keys));need(None not in aids and len(set(aids))==2,"positive frozen source-key resolution");m="EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS";ev=p["row_sha256"]
                else:aids=tuple(sorted(atoms_by_owner[pair[0]]+atoms_by_owner[pair[1]]));m="MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE";ev=r["row_sha256"]
            else:
                need(u["source_authority"]=="C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER" and t=="POSITIVE_VOLUME_CARRIERS","C24 ownership");x=g2b[u["C24A_G2B_exact_row_sha256"]];need(pair==(x["c24_member_id"],x["target_member_id"]) and not atoms_by_owner[x["c24_member_id"]],"C24 source");aids=(by_source[("C22A",x["C22_target_row_sha256"])],);m="EXACT_C24A_G2B_C22_TARGET_ATOM";ev=x["row_sha256"]
            need(all(x in atom for x in aids)and len(set(aids))==len(aids),"expected atom set");expected[us]=(set(aids),m,ev);mode[m]+=len(aids)
        need(len(union)==101080 and terminal=={"SIGNED_BOUNDARY_FACES":25452,"COMPLETE_BOUNDARY_FACES":10688,"POSITIVE_VOLUME_CARRIERS":64940},"union census")
        seen_atoms=set();seen_refs=defaultdict(set);disp=Counter();expanded=0;sets=Counter();seen_ep=set()
        for o in caps["seed1_ledger"].rows():
            aid=o["atom_id"];need(aid in atom and aid not in seen_atoms,"output atom unique");seen_atoms.add(aid);a0=atom[aid];owner=a0["owner_member_id"]
            need(o["owner_member_id"]==owner and o["atom_source_kernel"]==a0["source_kernel"] and o["atom_source_row_sha256"]==a0["source_row_sha256"] and o["current_C15_component"]==c15[owner],"atom base join")
            if a0["source_kernel"]=="C19C":
                e=endpoint[owner];x=e["endpoint_inclusion_bits"];bits=[x["t_lower_closed"],x["t_upper_closed"],x["p_lower_closed"],x["p_upper_closed"],x["s_lower_closed"],x["s_upper_closed"]];eb={"authority_row_sha256":e["row_sha256"],"authority_rule":e["authority_rule"],"source":"C19C_ENDPOINT_OWNERSHIP_V3"};seen_ep.add(owner)
            else:bits=a0["endpoint_inclusion_flags_lower_upper_t_p_s"];eb={"authority_row_sha256":a0["row_sha256"],"authority_rule":"PRIMITIVE_OPEN_SUPPORT","source":"FROZEN_PRIMITIVE_ATOM_ROW"}
            need(o["effective_endpoint_inclusion_flags_lower_upper_t_p_s"]==bits and o["endpoint_authority_binding"]==eb,"endpoint join")
            tc=Counter()
            for q in o["incident_union_pair_routes"]:
                us=q["union_route_row_sha256"];need(us in union and aid in expected[us][0] and q["atom_binding_mode"]==expected[us][1] and q["source_evidence_row_sha256"]==expected[us][2],"inverse incidence")
                u=union[us];need(q["assigned_terminal"]==u["assigned_terminal"] and q["pair_key"]=="|".join(u["pair_key"]) and q["source_authority"]==u["source_authority"],"incidence route fields");need(aid not in seen_refs[us],"duplicate route/atom ref");seen_refs[us].add(aid);tc[q["assigned_terminal"]]+=1;expanded+=1
            ts=[t for t in T if tc[t]];need(o["candidate_incidence_count"]==sum(tc.values()) and o["terminal_incidence_census"]=={t:tc[t]for t in T} and o["terminal_incidence_set"]==ts,"incidence census");d="INCIDENT_TO_FULL_101080_UNION_PAIR_ROUTES"if ts else"EXACT_COMPLEMENT__ATOM_ABSENT_FROM_ALL_FULL_UNION_ROUTE_INCIDENCES";need(o["candidate_disposition"]==d and o["pair_routes_each_have_unique_20_terminal_ownership"]is True,"disposition");disp[d]+=1;sets[tuple(ts)]+=1
        need(seen_atoms==set(atom) and seen_ep==set(endpoint),"atom/endpoint totality")
        for us,(aids,_,_)in expected.items():need(seen_refs[us]==aids,"route exact atom incidence totality")
        for prefix in("seed1","seed2"):
            r=caps[prefix+"_result"].doc();b=dict(r);c=b.pop("result_sha256");need(c==sha(b) and r["output"]["file_sha256"]==getattr(a,prefix+"_ledger_sha256") and r["pair_union"]["pairs"]==101080 and r["atom_denominator"]["atoms"]==483232,prefix+":result")
        result={"schema":"cm2.c27-independent.full-union-101080-on-483232.atom-inverse-incidence-verification.v2","status":"PASS_INDEPENDENT_INVERSE_ROUTE_TO_ATOM_INCIDENCE_AUDIT__POSITIVE_SOURCE_KEYS_EXACTLY_RESOLVED__DUAL_SEED_BYTE_IDENTITY__ZERO_CREDIT","pair_routes":101080,"primitive_atoms":483232,"incident_atoms":disp["INCIDENT_TO_FULL_101080_UNION_PAIR_ROUTES"],"exact_complement_atoms":disp["EXACT_COMPLEMENT__ATOM_ABSENT_FROM_ALL_FULL_UNION_ROUTE_INCIDENCES"],"expanded_atom_route_incidences":expanded,"binding_census":dict(sorted(mode.items())),"terminal_set_atom_census":{"|".join(k)if k else"COMPLEMENT":v for k,v in sorted(sets.items())},"C19C_endpoint_v3_rows":len(seen_ep),"dual_seed_join_ledgers_byte_identical":True,"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{k:v.rec()for k,v in sorted(caps.items())}},"formal_credit":0,"manifest_authorized":False,"C27_C28_C29":"FULL_REBUILD_REQUIRED","Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM"};result["result_sha256"]=sha(result);a.out_dir.mkdir(parents=True,exist_ok=False);(a.out_dir/"verification.json").write_bytes(canon(result)+b"\n");print(canon({"status":result["status"],"result_sha256":result["result_sha256"]}).decode());return 0
    except(Fail,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));return 2
    finally:
        for c in caps.values():c.close()
if __name__=="__main__":raise SystemExit(main())

