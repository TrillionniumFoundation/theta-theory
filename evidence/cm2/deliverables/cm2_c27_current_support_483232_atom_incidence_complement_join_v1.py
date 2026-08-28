#!/usr/bin/env python3
"""Materialize the 483,232 primitive-atom to rebuilt-pair incidence/complement join.

The old primitive census is used only as a frozen primitive candidate universe,
not as C27 routing authority.  C19C's formerly missing endpoint vector is
replaced row-by-row by the append-only endpoint-v3 authority.  Every atom is
then disposed as incident to one or more uniquely-routed pair rows or as the
exact complement of the rebuilt 91,672 pair universe.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterator


TERMINALS = ("SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS")


class Fail(RuntimeError): pass


def need(v: bool, m: str) -> None:
    if type(v) is not bool or not v: raise Fail(m)


def canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def sha(v: Any) -> str: return hashlib.sha256(canon(v)).hexdigest()


def closure(row: dict[str, Any], label: str) -> None:
    body=dict(row); claimed=body.pop("row_sha256",None); need(claimed==sha(body),label+":closure")


def fp(s: os.stat_result)->tuple[int,...]:
    return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)


class Capture:
    def __init__(self,label:str,path:Path,expected:str):
        self.label,self.path=label,path
        self.fd=os.open(path,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
        s=os.fstat(self.fd);need(stat.S_ISREG(s.st_mode),label+":regular");self.pre=fp(s)
        h=hashlib.sha256()
        while b:=os.read(self.fd,4<<20):h.update(b)
        self.file_sha=h.hexdigest();need(self.file_sha==expected,label+":pin");need(fp(os.fstat(self.fd))==self.pre,label+":hash-fstat")
    def rows(self)->Iterator[dict[str,Any]]:
        os.lseek(self.fd,0,os.SEEK_SET)
        with os.fdopen(os.dup(self.fd),"rb") as raw:
            with gzip.GzipFile(fileobj=raw,mode="rb") as z:
                for i,line in enumerate(z):
                    need(line.endswith(b"\n"),f"{self.label}:{i}:newline")
                    r=json.loads(line);need(canon(r)==line[:-1],f"{self.label}:{i}:canonical");closure(r,f"{self.label}:{i}");yield r
        need(fp(os.fstat(self.fd))==self.pre,self.label+":rows-fstat")
    def document(self)->dict[str,Any]:
        os.lseek(self.fd,0,os.SEEK_SET); chunks=[]
        while b:=os.read(self.fd,4<<20):chunks.append(b)
        need(fp(os.fstat(self.fd))==self.pre,self.label+":document-fstat")
        return json.loads(b"".join(chunks))
    def receipt(self)->dict[str,Any]:
        need(fp(os.fstat(self.fd))==self.pre,self.label+":final-fstat")
        return {"path":str(self.path),"sha256":self.file_sha,"stat_fingerprint":list(self.pre),"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True}
    def close(self)->None:os.close(self.fd)


def main()->int:
    ap=argparse.ArgumentParser()
    for name in ("atoms","priority","c15","endpoint-authority","endpoint-receipt"):
        ap.add_argument("--"+name,type=Path,required=True);ap.add_argument("--"+name+"-sha256",required=True)
    ap.add_argument("--out-dir",type=Path,required=True);ap.add_argument("--seed",type=int,required=True)
    args=ap.parse_args();caps={}
    try:
        for name in ("atoms","priority","c15","endpoint_authority","endpoint_receipt"):
            caps[name]=Capture(name,getattr(args,name),getattr(args,name+"_sha256"))
        receipt=caps["endpoint_receipt"].document(); body=dict(receipt); claimed=body.pop("receipt_sha256",None)
        need(claimed==sha(body),"endpoint receipt closure")
        need(receipt["status"]=="PASS_APPEND_ONLY_V3_AUTHORITY_DUAL_SEED_DUAL_VERIFIER_ATTACK_SEALED"
             and receipt["byte_identical_dual_seed_ledgers"]["authority"]["sha256"]==args.endpoint_authority_sha256
             and receipt["byte_identical_dual_seed_ledgers"]["authority"]["row_count"]==33344,
             "endpoint receipt authority binding")

        c15={}
        for r in caps["c15"].rows():
            m=r["registry_member_id"];need(m not in c15,"C15 unique");c15[m]=r["fresh_component_id"]
        need(len(c15)==502204,"C15 census")

        endpoint={}
        for r in caps["endpoint_authority"].rows():
            m=r["member_id"];need(m not in endpoint,"endpoint unique")
            need(r["all_six_faces_uniquely_disposed"] is True and len(r["face_dispositions"])==6,"endpoint six faces")
            endpoint[m]=r
        need(len(endpoint)==33344,"endpoint census")

        incidence:dict[str,list[dict[str,Any]]]=defaultdict(list);pair_seen=set();route_count=Counter()
        for r in caps["priority"].rows():
            pair=(r["left_member_id"],r["right_member_id"]);need(pair[0]<pair[1] and pair not in pair_seen,"route canonical unique");pair_seen.add(pair)
            t=r["assigned_terminal"];need(t in TERMINALS,"route terminal");route_count[t]+=1
            for member,other in ((pair[0],pair[1]),(pair[1],pair[0])):
                incidence[member].append({"assigned_terminal":t,"other_member_id":other,
                                         "pair_key":"|".join(pair),"priority_route_row_sha256":r["row_sha256"]})
        need(len(pair_seen)==91672 and route_count=={"SIGNED_BOUNDARY_FACES":25452,"COMPLETE_BOUNDARY_FACES":10688,"POSITIVE_VOLUME_CARRIERS":55532},"route census")
        for rows in incidence.values():rows.sort(key=lambda r:(r["other_member_id"],r["assigned_terminal"],r["priority_route_row_sha256"]))

        args.out_dir.mkdir(parents=True,exist_ok=False)
        out=args.out_dir/"current_support_483232_atom_pair_incidence_or_complement.jsonl.gz"
        out_hash=hashlib.sha256();row_seq=hashlib.sha256();atom_ids=hashlib.sha256()
        atom_count=0;source=Counter();disposition=Counter();by_kernel=Counter();terminal_sets=Counter();terminal_atom_presence=Counter();expanded_incidence=0
        distinct_owners=set();seen_endpoint=set();seen_route_owners=set();multi_terminal=0
        with out.open("wb") as raw:
            with gzip.GzipFile(fileobj=raw,mode="wb",mtime=0,filename="") as z:
                for atom in caps["atoms"].rows():
                    atom_count+=1;kernel=atom["source_kernel"];source[kernel]+=1;owner=atom["owner_member_id"];distinct_owners.add(owner)
                    need(owner in c15,"atom C15 join")
                    if kernel=="C19C":
                        a=endpoint.get(owner);need(a is not None,"C19C endpoint join")
                        bounds=[q["value"] for q in atom["physical_bounds"]]
                        need(a["C19C_row_sha256"]==atom["source_row_sha256"] and a["chart"]==atom["chart"]
                             and a["bounds"]==bounds,"C19C endpoint primitive binding")
                        bits=a["endpoint_inclusion_bits"]
                        effective=[bits["t_lower_closed"],bits["t_upper_closed"],bits["p_lower_closed"],bits["p_upper_closed"],bits["s_lower_closed"],bits["s_upper_closed"]]
                        endpoint_binding={"authority_row_sha256":a["row_sha256"],"authority_rule":a["authority_rule"],"source":"C19C_ENDPOINT_OWNERSHIP_V3"};seen_endpoint.add(owner)
                    else:
                        effective=atom["endpoint_inclusion_flags_lower_upper_t_p_s"]
                        need(atom["endpoint_ownership_state"]=="EXPLICIT_ALL_OPEN" and effective==[False]*6,"open atom endpoint semantics")
                        endpoint_binding={"authority_row_sha256":atom["row_sha256"],"authority_rule":"PRIMITIVE_OPEN_SUPPORT","source":"FROZEN_PRIMITIVE_ATOM_ROW"}
                    inc=incidence.get(owner,[]);expanded_incidence+=len(inc)
                    tc=Counter(r["assigned_terminal"] for r in inc);tset=tuple(t for t in TERMINALS if tc[t]);terminal_sets[tset]+=1
                    for t in tset:terminal_atom_presence[t]+=1
                    if len(tset)>1:multi_terminal+=1
                    if inc: disp="INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS";seen_route_owners.add(owner)
                    else: disp="EXACT_COMPLEMENT__OWNER_ABSENT_FROM_ALL_91672_PAIR_ROUTE_ENDPOINTS"
                    disposition[disp]+=1;by_kernel[(kernel,disp)]+=1
                    row={"atom_id":atom["atom_id"],"atom_source_row_sha256":atom["source_row_sha256"],"atom_source_kernel":kernel,
                         "candidate_disposition":disp,"candidate_incidence_count":len(inc),"current_C15_component":c15[owner],
                         "effective_endpoint_inclusion_flags_lower_upper_t_p_s":effective,"endpoint_authority_binding":endpoint_binding,
                         "formal_credit":0,"incident_pair_routes":inc,"owner_member_id":owner,
                         "pair_routes_each_have_unique_terminal_assignment":True,
                         "schema":"cm2.c27-independent.current-support-483232.atom-incidence-complement.row.v1",
                         "terminal_incidence_census":{t:tc[t] for t in TERMINALS},"terminal_incidence_set":list(tset)}
                    row["row_sha256"]=sha(row);line=canon(row)+b"\n";z.write(line);row_seq.update(row["row_sha256"].encode()+b"\n");atom_ids.update(atom["atom_id"].encode()+b"\n")
        need(atom_count==483232 and source=={"C19A":5596,"C19B":12232,"C19C":33344,"C20A":126468,"C22A":295340,"C23A":10252},"atom census")
        need(len(distinct_owners)==482380 and set(incidence)==seen_route_owners and seen_endpoint==set(endpoint),"owner/endpoint totality")
        need(sum(disposition.values())==483232 and expanded_incidence==197408,"incidence closure")
        out_file_sha=hashlib.sha256(out.read_bytes()).hexdigest()
        attest={k:v.receipt() for k,v in sorted(caps.items())}
        result={"schema":"cm2.c27-independent.current-support-483232.atom-incidence-complement.result.v1",
                "status":"PASS_MATERIALIZED_483232_ATOM_INCIDENCE_OR_EXACT_COMPLEMENT__PAIR_LEVEL_TERMINALS_UNIQUE__ATOM_LEVEL_MULTI_TERMINAL_INCIDENCE_EXPLICIT__ZERO_CREDIT",
                "scope":"MATERIALIZED_ATOM_TO_REBUILT_PAIR_INCIDENCE_OR_COMPLEMENT_JOIN__NOT_YET_A_GLOBAL_20_FAMILY_TERMINAL_SEAL",
                "formal_credit":0,"manifest_authorized":False,
                "primitive_atom_census":{"atoms":atom_count,"distinct_owners":len(distinct_owners),"by_source_kernel":dict(sorted(source.items())),"atom_ids_sha256":atom_ids.hexdigest()},
                "endpoint_v3_join":{"C19C_rows":len(seen_endpoint),"unresolved_C19C_endpoint_rows":0,"authority_receipt_sha256":claimed},
                "incidence_complement":{"incident_atoms":disposition["INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS"],
                                         "complement_atoms":disposition["EXACT_COMPLEMENT__OWNER_ABSENT_FROM_ALL_91672_PAIR_ROUTE_ENDPOINTS"],
                                         "expanded_atom_pair_route_incidences":expanded_incidence,"pair_route_endpoint_owners":len(incidence),
                                         "multi_terminal_incident_atoms":multi_terminal,
                                         "terminal_atom_presence":{t:terminal_atom_presence[t] for t in TERMINALS},
                                         "terminal_set_atom_census":{"|".join(k) if k else "COMPLEMENT":v for k,v in sorted(terminal_sets.items())},
                                         "by_source_kernel_and_disposition":{"|".join(k):v for k,v in sorted(by_kernel.items())}},
                "pair_route_census":{"pairs":len(pair_seen),"by_terminal":{t:route_count[t] for t in TERMINALS},"pair_terminal_assignment_mutually_exclusive":True},
                "output":{"filename":out.name,"row_count":atom_count,"file_sha256":out_file_sha,"row_sequence_sha256":row_seq.hexdigest()},
                "root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":attest},
                "governance":{"C27_FAMILIES_imported_or_read":False,"historical_edge_ledger_used_as_candidate_universe":False,
                              "atom_single_terminal_assignment_inferred_from_multiple_pair_incidences":False,
                              "remaining_contract":"INDEPENDENT_ATOM_JOIN_VERIFIER_AND_ATTACKS__THEN_DECIDE_WHETHER_PAIR_LEVEL_UNIQUENESS_SATISFIES_GLOBAL_TERMINAL_GRAMMAR"},
                "C27_C28_C29":"FULL_REBUILD_REQUIRED","Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM"}
        result["result_sha256"]=sha(result);(args.out_dir/"result.json").write_bytes(canon(result)+b"\n")
        print(canon({"status":result["status"],"result_sha256":result["result_sha256"],"incident_atoms":disposition["INCIDENT_TO_ONE_OR_MORE_UNIQUELY_ROUTED_PAIR_ROWS"],"complement_atoms":disposition["EXACT_COMPLEMENT__OWNER_ABSENT_FROM_ALL_91672_PAIR_ROUTE_ENDPOINTS"]}).decode());return 0
    except (Fail,KeyError,TypeError,ValueError,OSError) as e:
        print("FAIL:"+str(e));return 2
    finally:
        for c in caps.values():c.close()


if __name__=="__main__":raise SystemExit(main())
