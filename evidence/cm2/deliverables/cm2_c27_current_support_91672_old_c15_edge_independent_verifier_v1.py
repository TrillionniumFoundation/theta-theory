#!/usr/bin/env python3
"""Independent verifier for current-support old-C15 edge materialization.

No producer/adapter module is imported.  Edges are rebuilt from the priority
routes and frozen C15 mapping using direct grouped adjacency rather than the
adapter's witness-slice construction.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
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


def close_row(r: dict[str, Any], label: str) -> None:
    b = dict(r); claimed = b.pop("row_sha256", None)
    need(claimed == sha(b), label + ":closure")


def fp(s: os.stat_result) -> tuple[int, ...]:
    return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)


class Capture:
    def __init__(self, label: str, path: Path, expected: str):
        self.label, self.path = label, path
        self.fd = os.open(path, os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
        s=os.fstat(self.fd); need(stat.S_ISREG(s.st_mode),label+":regular");self.pre=fp(s)
        h=hashlib.sha256()
        while b:=os.read(self.fd,4<<20): h.update(b)
        self.file_sha=h.hexdigest();need(self.file_sha==expected,label+":pin");need(fp(os.fstat(self.fd))==self.pre,label+":hash-fstat")
    def raw(self)->bytes:
        os.lseek(self.fd,0,os.SEEK_SET); out=[]
        while b:=os.read(self.fd,4<<20):out.append(b)
        need(fp(os.fstat(self.fd))==self.pre,self.label+":raw-fstat");return b"".join(out)
    def rows(self)->Iterator[dict[str,Any]]:
        os.lseek(self.fd,0,os.SEEK_SET)
        with os.fdopen(os.dup(self.fd),"rb") as raw:
            with gzip.GzipFile(fileobj=raw,mode="rb") as z:
                for i,line in enumerate(z):
                    need(line.endswith(b"\n"),f"{self.label}:{i}:newline")
                    r=json.loads(line);need(canon(r)==line[:-1],f"{self.label}:{i}:canonical");close_row(r,f"{self.label}:{i}");yield r
        need(fp(os.fstat(self.fd))==self.pre,self.label+":rows-fstat")
    def receipt(self)->dict[str,Any]:
        need(fp(os.fstat(self.fd))==self.pre,self.label+":final-fstat")
        return {"path":str(self.path),"sha256":self.file_sha,"stat_fingerprint":list(self.pre),"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True}
    def close(self)->None:os.close(self.fd)


def edge(row:dict[str,Any],kind:str)->tuple[str,str]:
    p=row["component_pair"] if kind=="strict" else row["unordered_component_pair"]
    return tuple(sorted(p))


def main()->int:
    ap=argparse.ArgumentParser()
    for prefix in ("seed1","seed2"):
        for kind in ("result","witness","edges"):
            ap.add_argument(f"--{prefix}-{kind}",type=Path,required=True);ap.add_argument(f"--{prefix}-{kind}-sha256",required=True)
    for kind in ("priority","positive","c15","strict","g2a"):
        ap.add_argument(f"--{kind}",type=Path,required=True);ap.add_argument(f"--{kind}-sha256",required=True)
    ap.add_argument("--out-dir",type=Path,required=True)
    args=ap.parse_args();caps={}
    try:
        for kind in ("priority","positive","c15","strict","g2a"):
            caps[kind]=Capture(kind,getattr(args,kind),getattr(args,kind+"_sha256"))
        for prefix in ("seed1","seed2"):
            for kind in ("result","witness","edges"):
                label=prefix+"_"+kind;caps[label]=Capture(label,getattr(args,label),getattr(args,label+"_sha256"))
        need(caps["seed1_witness"].raw()==caps["seed2_witness"].raw(),"dual witness bytes")
        need(caps["seed1_edges"].raw()==caps["seed2_edges"].raw(),"dual edge bytes")

        c15={}
        for r in caps["c15"].rows():
            m=r["registry_member_id"];need(m not in c15,"C15 unique");c15[m]=r["fresh_component_id"]
        need(len(c15)==502204,"C15 census")
        positives={}
        for r in caps["positive"].rows():
            p=(r["left_member_id"],r["right_member_id"]);need(p not in positives,"positive unique");positives[p]=r["row_sha256"]
        need(len(positives)==55532,"positive census")
        expected=[];byedge=defaultdict(list);cross=Counter();same=Counter();route=Counter();seen=set()
        for r in caps["priority"].rows():
            p=(r["left_member_id"],r["right_member_id"]);need(p not in seen,"route unique");seen.add(p)
            t=r["assigned_terminal"];route[t]+=1;cs=(c15[p[0]],c15[p[1]])
            need(r["current_C15_components"]==list(cs),"route C15 join")
            if cs[0]==cs[1]:same[t]+=1;continue
            cross[t]+=1;e=tuple(sorted(cs))
            body={"assigned_terminal":t,"formal_credit":0,"member_pair":list(p),"old_C15_component_pair":list(e),
                  "positive_primitive_row_sha256":r["positive_primitive_row_sha256"],"priority_route_row_sha256":r["row_sha256"],
                  "schema":"cm2.c27-independent.current-support-91672.old-c15-cross-member-witness.row.v1"}
            body["row_sha256"]=sha(body);expected.append(body);byedge[e].append(body)
        need(len(seen)==91672 and route=={"SIGNED_BOUNDARY_FACES":25452,"COMPLETE_BOUNDARY_FACES":10688,"POSITIVE_VOLUME_CARRIERS":55532},"route census")
        need(cross=={"POSITIVE_VOLUME_CARRIERS":32012} and len(byedge)==14620,"cross census")
        expected.sort(key=lambda r:(r["old_C15_component_pair"],r["member_pair"],r["assigned_terminal"]))

        strict=set()
        for r in caps["strict"].rows():
            e=edge(r,"strict");need(e not in strict,"strict unique");strict.add(e)
        g2a=set()
        for r in caps["g2a"].rows():
            e=edge(r,"g2a");need(e not in g2a,"G2A unique");g2a.add(e)
        current=set(byedge);need(len(strict)==14772 and len(g2a)==144 and current<=strict and len(current&g2a)==40,"validation relations")

        for prefix in ("seed1","seed2"):
            observed=list(caps[prefix+"_witness"].rows());need(observed==expected,prefix+":witness exact")
            edge_rows=list(caps[prefix+"_edges"].rows());need(len(edge_rows)==14620,prefix+":edge census")
            cursor=0
            for r,e in zip(edge_rows,sorted(current)):
                need(tuple(r["old_C15_component_pair"])==e,prefix+":edge order")
                ws=byedge[e];tc=Counter(x["assigned_terminal"] for x in ws);seq=hashlib.sha256()
                for x in ws:seq.update(x["row_sha256"].encode()+b"\n")
                need(r["member_witness_ordinal_range"]==[cursor,cursor+len(ws)]
                     and r["supporting_member_pair_count"]==len(ws)
                     and r["source_terminal_member_pair_census"]=={t:tc[t] for t in TERMINALS}
                     and r["supporting_witness_row_sequence_sha256"]==seq.hexdigest()
                     and r["overlaps_strict_volume_component_edge"] is True
                     and r["overlaps_G2A_component_edge"]==(e in g2a),prefix+":edge semantics")
                cursor+=len(ws)
            need(cursor==32012,prefix+":slice closure")
            result=json.loads(caps[prefix+"_result"].raw());b=dict(result);claimed=b.pop("result_sha256")
            need(claimed==sha(b) and result["formal_credit"]==0 and result["CM2"]=="NO-GO_FOR_CLAIM",prefix+":result closure")
            need(result["route_census"]["unique_cross_old_C15_component_edges"]==14620
                 and result["route_census"]["cross_old_C15_component_member_pairs"]==32012
                 and result["validation_set_relations"]["current_edges_intersection_strict_volume"]==14620
                 and result["validation_set_relations"]["current_edges_minus_strict_volume"]==0
                 and result["validation_set_relations"]["current_edges_intersection_G2A"]==40,prefix+":result census")
        result={"schema":"cm2.c27-independent.current-support-91672.old-c15-edge.verification.v1",
                "status":"PASS_INDEPENDENT_DIRECT_GROUPED_ADJACENCY_EDGE_REBUILD_DUAL_SEED__ZERO_CREDIT",
                "cross_member_pair_census":{"SIGNED_BOUNDARY_FACES":0,"COMPLETE_BOUNDARY_FACES":0,"POSITIVE_VOLUME_CARRIERS":32012},
                "unique_old_C15_component_edges":14620,"intersection_strict_volume":14620,"minus_strict_volume":0,"intersection_G2A":40,
                "dual_seed_witness_and_edge_ledgers_byte_identical":True,
                "root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{k:v.receipt() for k,v in sorted(caps.items())}},
                "formal_credit":0,"manifest_authorized":False,"C27_C28_C29":"FULL_REBUILD_REQUIRED","Source_W_formal_remainder":80,"CM2":"NO-GO_FOR_CLAIM"}
        result["result_sha256"]=sha(result);args.out_dir.mkdir(parents=True,exist_ok=False);(args.out_dir/"verification.json").write_bytes(canon(result)+b"\n")
        print(canon({"status":result["status"],"result_sha256":result["result_sha256"]}).decode());return 0
    except (Fail,KeyError,TypeError,ValueError,OSError) as e:
        print("FAIL:"+str(e));return 2
    finally:
        for c in caps.values():c.close()


if __name__=="__main__":raise SystemExit(main())
