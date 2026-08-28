#!/usr/bin/env python3
"""Cold manifest-first replay of the sealed T04 common-v2 adapter."""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,stat
from pathlib import Path
from typing import Any,Iterator
ROOT=Path(__file__).resolve().parent.parent
CS="cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PS="cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
class Reject(RuntimeError):pass
def need(v:bool,l:str)->None:
    if type(v) is not bool or not v:raise Reject(l)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def sha(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()
def rel(p:Path)->str:return str(p.resolve().relative_to(ROOT))
def parse(p:Path)->dict[str,str]:
    d={}
    for l in p.read_text("ascii").splitlines():
        h,n=l.split("  ",1);need(n not in d,"duplicate manifest");d[n]=h
    return d
def fp(p:Path)->tuple[int,...]:
    s=os.lstat(p);need(stat.S_ISREG(s.st_mode) and not p.is_symlink(),"regular")
    return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_nlink)
def rows(p:Path)->Iterator[dict[str,Any]]:
    with gzip.open(p,"rt",encoding="ascii") as f:
        for i,l in enumerate(f):
            r=json.loads(l);b=dict(r);c=b.pop("row_sha256",None);need(c==digest(b),"row closure:"+str(i));yield r
def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("--seal-dir",required=True);ap.add_argument("--out-dir",required=True);a=ap.parse_args()
    seal,out=Path(a.seal_dir),Path(a.out_dir);need(not out.exists(),"fresh output")
    pm,rp,rm=seal/"payload_manifest.sha256",seal/"receipt.json",seal/"root_manifest.sha256"
    need(parse(rm)=={rel(pm):sha(pm),rel(rp):sha(rp)},"root")
    payload=parse(pm);before={}
    for n,h in payload.items():p=ROOT/n;before[n]=fp(p);need(sha(p)==h,"payload:"+n)
    receipt=json.loads(rp.read_bytes());b=dict(receipt);c=b.pop("receipt_sha256",None);need(c==digest(b),"receipt")
    need(receipt["candidate_pairs"]==receipt["materialized_physical_proof_rows"]==1_362_088
         and receipt["terminal_ordinal"]==4 and receipt["authority_slot"]=="T04_DOUBLE_GRAPHS"
         and receipt["unresolved"]==receipt["legal_cross_component_witnesses"]==receipt["component_edges"]==0,"receipt semantics")
    cn=next(n for n in payload if n.endswith("seed-30649101/T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz"))
    pn=next(n for n in payload if n.endswith("seed-30649101/T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz"))
    ci,pi=rows(ROOT/cn),rows(ROOT/pn);seen_c:set[bytes]=set();seen_p:set[bytes]=set();count=0
    while True:
        try:cr=next(ci)
        except StopIteration:break
        try:pr=next(pi)
        except StopIteration as e:raise Reject("proof omission") from e
        need(cr["schema"]==CS and pr["schema"]==PS and cr["ordinal"]==pr["ordinal"]==count
             and cr["candidate_key"]==pr["candidate_key"]
             and cr["physical_proof_row_count"]==1
             and cr["physical_proof_row_sequence_sha256"]==hashlib.sha256(pr["row_sha256"].encode()+b"\n").hexdigest()
             and cr["terminal_ordinal"]==pr["terminal_ordinal"]==4
             and cr["authority_slot"]==pr["authority_slot"]=="T04_DOUBLE_GRAPHS"
             and cr["primitive_authority_row_sha256"]==pr["primitive_authority_row_sha256"]
             and pr["component_edge_key"] is None and pr["physical_witness_key"] is None
             and pr["legal_cross_component_same_physical_point_witness"] is False
             and cr["formal_credit"]==pr["formal_credit"]==0,"lockstep")
        ch,ph=hashlib.sha256(cr["candidate_key"].encode()).digest(),hashlib.sha256(pr["proof_row_key"].encode()).digest()
        need(ch not in seen_c and ph not in seen_p,"unique");seen_c.add(ch);seen_p.add(ph);count+=1
    try:next(pi);raise Reject("extra proof")
    except StopIteration:pass
    need(count==len(seen_c)==len(seen_p)==1_362_088,"cold census")
    for n,h in payload.items():p=ROOT/n;need(fp(p)==before[n] and sha(p)==h,"post stable:"+n)
    out.mkdir(parents=True);body={"schema":"cm2.c27-independent.t04-double-graphs.common-v2-postpublication-cold-terminal-replay.v1",
        "status":"PASS_COLD_COMMON_V2_1362088_CANDIDATE_PROOF_LOCKSTEP_UNIQUENESS_REPLAY__ZERO_CREDIT",
        "base_receipt_file_sha256":sha(rp),"base_receipt_sha256":receipt["receipt_sha256"],
        "payload_manifest_file_sha256":sha(pm),"root_manifest_file_sha256":sha(rm),
        "candidate_pairs":count,"materialized_physical_proof_rows":count,"unique_candidate_keys":len(seen_c),"unique_proof_keys":len(seen_p),
        "unresolved":0,"legal_cross_component_witnesses":0,"component_edges":0,"manifest_first_terminal_replay":True,
        "pre_post_sha256_identical":True,"pre_post_stat_identical":True,"numeric_exit":0,"signal":None,"stderr_empty":True,
        "formal_credit":0,"manifest_authorized":False,"source_W_transition_authorized":False}
    rec={**body,"receipt_sha256":digest(body)};tp=out/"terminal_replay.json";tp.write_bytes(enc(rec)+b"\n")
    tm=out/"terminal_manifest.sha256";paths=sorted([pm,rp,rm,tp],key=rel);tm.write_bytes(b"".join(sha(p).encode()+b"  "+rel(p).encode()+b"\n" for p in paths))
    print(enc({"status":rec["status"],"terminal_file_sha256":sha(tp),"terminal_receipt_sha256":rec["receipt_sha256"],"terminal_manifest_sha256":sha(tm)}).decode());return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except Reject as e:print("T04_COMMON_V2_COLD_REJECT:"+str(e));raise SystemExit(2)
