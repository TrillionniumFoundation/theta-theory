#!/usr/bin/env python3
"""Independent lockstep verifier for the 483,232 atom incidence/complement join."""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,stat
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterator
TERMINALS=("SIGNED_BOUNDARY_FACES","COMPLETE_BOUNDARY_FACES","POSITIVE_VOLUME_CARRIERS")
class Fail(RuntimeError):pass
def need(v:bool,m:str)->None:
    if type(v) is not bool or not v:raise Fail(m)
def canon(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def sha(v:Any)->str:return hashlib.sha256(canon(v)).hexdigest()
def closure(r:dict[str,Any],m:str)->None:
    b=dict(r);c=b.pop("row_sha256",None);need(c==sha(b),m)
def fp(s:os.stat_result)->tuple[int,...]:return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
class Cap:
    def __init__(self,n:str,p:Path,x:str):
        self.n,self.p=n,p;self.fd=os.open(p,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0));s=os.fstat(self.fd);need(stat.S_ISREG(s.st_mode),n+":regular");self.pre=fp(s);h=hashlib.sha256()
        while b:=os.read(self.fd,4<<20):h.update(b)
        self.h=h.hexdigest();need(self.h==x,n+":pin");need(fp(os.fstat(self.fd))==self.pre,n+":hash-fstat")
    def rows(self)->Iterator[dict[str,Any]]:
        os.lseek(self.fd,0,os.SEEK_SET)
        with os.fdopen(os.dup(self.fd),"rb") as raw:
            with gzip.GzipFile(fileobj=raw,mode="rb") as z:
                for i,line in enumerate(z):
                    need(line.endswith(b"\n"),f"{self.n}:{i}:newline");r=json.loads(line);need(canon(r)==line[:-1],f"{self.n}:{i}:canonical");closure(r,f"{self.n}:{i}:closure");yield r
        need(fp(os.fstat(self.fd))==self.pre,self.n+":rows-fstat")
    def doc(self)->dict[str,Any]:
        os.lseek(self.fd,0,os.SEEK_SET);a=[]
        while b:=os.read(self.fd,4<<20):a.append(b)
        need(fp(os.fstat(self.fd))==self.pre,self.n+":doc-fstat");return json.loads(b"".join(a))
    def rec(self)->dict[str,Any]:need(fp(os.fstat(self.fd))==self.pre,self.n+":final");return{"path":str(self.p),"sha256":self.h,"stat_fingerprint":list(self.pre),"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True}
    def close(self):os.close(self.fd)
def same_bytes(a:Cap,b:Cap)->bool:
    if a.pre[2]!=b.pre[2]:return False
    off=0
    while off<a.pre[2]:
        x=os.pread(a.fd,4<<20,off);y=os.pread(b.fd,4<<20,off)
        if x!=y:return False
        off+=len(x)
    return True
def main()->int:
    ap=argparse.ArgumentParser()
    for n in("atoms","priority","c15","endpoint-authority","endpoint-receipt","seed1-result","seed1-ledger","seed2-result","seed2-ledger"):
        ap.add_argument("--"+n,type=Path,required=True);ap.add_argument("--"+n+"-sha256",required=True)
    ap.add_argument("--out-dir",type=Path,required=True);args=ap.parse_args();caps={}
    try:
        for n in("atoms","priority","c15","endpoint_authority","endpoint_receipt","seed1_result","seed1_ledger","seed2_result","seed2_ledger"):caps[n]=Cap(n,getattr(args,n),getattr(args,n+"_sha256"))
        need(same_bytes(caps["seed1_ledger"],caps["seed2_ledger"]),"dual seed ledger byte identity")
        receipt=caps["endpoint_receipt"].doc();b=dict(receipt);claimed=b.pop("receipt_sha256");need(claimed==sha(b) and receipt["byte_identical_dual_seed_ledgers"]["authority"]["sha256"]==args.endpoint_authority_sha256,"endpoint receipt")
        c15={r["registry_member_id"]:r["fresh_component_id"] for r in caps["c15"].rows()};need(len(c15)==502204,"C15")
        endpoint={r["member_id"]:r for r in caps["endpoint_authority"].rows()};need(len(endpoint)==33344,"endpoint")
        inc=defaultdict(list);pairs=set();routes=Counter()
        for r in caps["priority"].rows():
            p=(r["left_member_id"],r["right_member_id"]);need(p not in pairs,"pair unique");pairs.add(p);t=r["assigned_terminal"];routes[t]+=1
            inc[p[0]].append({"assigned_terminal":t,"other_member_id":p[1],"pair_key":"|".join(p),"priority_route_row_sha256":r["row_sha256"]});inc[p[1]].append({"assigned_terminal":t,"other_member_id":p[0],"pair_key":"|".join(p),"priority_route_row_sha256":r["row_sha256"]})
        for v in inc.values():v.sort(key=lambda r:(r["other_member_id"],r["assigned_terminal"],r["priority_route_row_sha256"]))
        need(len(pairs)==91672 and routes=={"SIGNED_BOUNDARY_FACES":25452,"COMPLETE_BOUNDARY_FACES":10688,"POSITIVE_VOLUME_CARRIERS":55532},"pair census")
        ai=caps["atoms"].rows();oi=caps["seed1_ledger"].rows();atoms=0;owners=set();seen_endpoint=set();seen_route=set();source=Counter();disp=Counter();terminal_sets=Counter();expanded=0
        while True:
            try:a=next(ai)
            except StopIteration:a=None
            try:o=next(oi)
            except StopIteration:o=None
            need((a is None)==(o is None),"lockstep length")
            if a is None:break
            atoms+=1;owner=a["owner_member_id"];owners.add(owner);source[a["source_kernel"]]+=1;need(owner in c15,"atom C15")
            if a["source_kernel"]=="C19C":
                e=endpoint.get(owner);need(e is not None,"C19C join");bounds=[q["value"] for q in a["physical_bounds"]];need(e["C19C_row_sha256"]==a["source_row_sha256"] and e["chart"]==a["chart"] and e["bounds"]==bounds,"C19C binding")
                x=e["endpoint_inclusion_bits"];bits=[x["t_lower_closed"],x["t_upper_closed"],x["p_lower_closed"],x["p_upper_closed"],x["s_lower_closed"],x["s_upper_closed"]];eb={"authority_row_sha256":e["row_sha256"],"authority_rule":e["authority_rule"],"source":"C19C_ENDPOINT_OWNERSHIP_V3"};seen_endpoint.add(owner)
            else:
                bits=a["endpoint_inclusion_flags_lower_upper_t_p_s"];need(bits==[False]*6 and a["endpoint_ownership_state"]=="EXPLICIT_ALL_OPEN","open endpoints");eb={"authority_row_sha256":a["row_sha256"],"authority_rule":"PRIMITIVE_OPEN_SUPPORT","source":"FROZEN_PRIMITIVE_ATOM_ROW"}
            ir=inc.get(owner,[]);expanded+=len(ir);tc=Counter(r["assigned_terminal"] for r in ir);ts=tuple(t for t in TERMINALS if tc[t]);terminal_sets[ts]+=1
            d="INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS" if ir else "EXACT_COMPLEMENT__OWNER_ABSENT_FROM_ALL_91672_PAIR_ROUTE_ENDPOINTS";disp[d]+=1
            if ir:seen_route.add(owner)
            expected={"atom_id":a["atom_id"],"atom_source_row_sha256":a["source_row_sha256"],"atom_source_kernel":a["source_kernel"],"candidate_disposition":d,"candidate_incidence_count":len(ir),"current_C15_component":c15[owner],"effective_endpoint_inclusion_flags_lower_upper_t_p_s":bits,"endpoint_authority_binding":eb,"formal_credit":0,"incident_pair_routes":ir,"owner_member_id":owner,"pair_routes_each_have_unique_terminal_assignment":True,"schema":"cm2.c27-independent.current-support-483232.atom-incidence-complement.row.v1","terminal_incidence_census":{t:tc[t] for t in TERMINALS},"terminal_incidence_set":list(ts)};expected["row_sha256"]=sha(expected);need(o==expected,"atom output exact semantics")
        need(atoms==483232 and len(owners)==482380 and source=={"C19A":5596,"C19B":12232,"C19C":33344,"C20A":126468,"C22A":295340,"C23A":10252},"atom totality")
        need(disp["INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS"]==62240 and disp["EXACT_COMPLEMENT__OWNER_ABSENT_FROM_ALL_91672_PAIR_ROUTE_ENDPOINTS"]==420992 and expanded==197408 and seen_route==set(inc) and seen_endpoint==set(endpoint),"join closure")
        for prefix in("seed1","seed2"):
            r=caps[prefix+"_result"].doc();b=dict(r);claimed=b.pop("result_sha256");need(claimed==sha(b) and r["output"]["file_sha256"]==getattr(args,prefix+"_ledger_sha256") and r["output"]["row_count"]==483232 and r["incidence_complement"]["incident_atoms"]==62240 and r["incidence_complement"]["complement_atoms"]==420992 and r["incidence_complement"]["expanded_atom_pair_route_incidences"]==197408,prefix+":result")
        result={"schema":"cm2.c27-independent.current-support-483232.atom-incidence-complement.verification.v1","status":"PASS_INDEPENDENT_LOCKSTEP_483232_ATOM_JOIN_AND_DUAL_SEED_BYTE_IDENTITY__ZERO_CREDIT","primitive_atoms":483232,"incident_atoms":62240,"exact_complement_atoms":420992,"expanded_atom_pair_route_incidences":197408,"C19C_endpoint_v3_rows":33344,"terminal_set_atom_census":{"|".join(k) if k else "COMPLEMENT":v for k,v in sorted(terminal_sets.items())},"dual_seed_join_ledgers_byte_identical":True,"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{k:v.rec() for k,v in sorted(caps.items())}},"formal_credit":0,"manifest_authorized":False,"C27_C28_C29":"FULL_REBUILD_REQUIRED","Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM"};result["result_sha256"]=sha(result);args.out_dir.mkdir(parents=True,exist_ok=False);(args.out_dir/"verification.json").write_bytes(canon(result)+b"\n");print(canon({"status":result["status"],"result_sha256":result["result_sha256"]}).decode());return 0
    except(Fail,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));return 2
    finally:
        for c in caps.values():c.close()
if __name__=="__main__":raise SystemExit(main())
