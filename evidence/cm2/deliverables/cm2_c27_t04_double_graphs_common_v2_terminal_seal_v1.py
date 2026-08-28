#!/usr/bin/env python3
"""Seal the independently verified T04 common-v2 adapter."""

from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parent.parent
class Reject(RuntimeError): pass
def need(v:bool,l:str)->None:
    if type(v) is not bool or not v: raise Reject(l)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def sha(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()
def rel(p:Path)->str:return str(p.resolve().relative_to(ROOT))
def man(ps:list[Path])->bytes:return b"".join(sha(p).encode()+b"  "+rel(p).encode()+b"\n" for p in sorted(ps,key=rel))
def closed(p:Path,k:str)->dict[str,Any]:
    v=json.loads(p.read_bytes());b=dict(v);c=b.pop(k,None);need(c==digest(b),"closure:"+p.name);return v

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("--adapter-a",required=True);ap.add_argument("--adapter-b",required=True)
    ap.add_argument("--verification",required=True);ap.add_argument("--attacks",required=True)
    ap.add_argument("--native-receipt",required=True);ap.add_argument("--native-cold-replay",required=True);ap.add_argument("--out-dir",required=True)
    a=ap.parse_args();aa,bb=Path(a.adapter_a),Path(a.adapter_b);vpath,apath=Path(a.verification),Path(a.attacks)
    nr,nc=Path(a.native_receipt),Path(a.native_cold_replay);out=Path(a.out_dir);need(not out.exists(),"fresh seal")
    names=["T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz","T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz","adapter_receipt.json","manifest.sha256"]
    for n in names:need(sha(aa/n)==sha(bb/n),"dual adapter bytes:"+n)
    ar=closed(aa/"adapter_receipt.json","receipt_sha256");vr=closed(vpath,"verification_sha256");attack=closed(apath,"attack_receipt_sha256")
    native=closed(nr,"receipt_sha256");cold=closed(nc,"receipt_sha256")
    need(ar["terminal_ordinal"]==4 and ar["authority_slot"]=="T04_DOUBLE_GRAPHS"
         and ar["exact_census"]["candidate_pairs"]==ar["exact_census"]["physical_proof_rows"]==1_362_088
         and ar["exact_census"]["unresolved"]==ar["exact_census"]["legal_cross_component_witnesses"]==ar["exact_census"]["component_edges"]==0,"adapter")
    need(vr["status"].startswith("PASS_NO_ADAPTER_IMPORT") and vr["candidate_pairs"]==vr["physical_proof_rows"]==1_362_088
         and vr["dual_seed_all_files_byte_identical"] is True,"verification")
    need(attack["attack_count"]==attack["rejected"]==25 and attack["accepted"]==0,"attacks")
    need(native["authority_slot"]=="T04_DOUBLE_GRAPHS" and cold["base_receipt_file_sha256"]==sha(nr),"native chain")
    sources=[ROOT/"deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_v1.py",
             ROOT/"deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_independent_verifier_v1.py",
             ROOT/"deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_attack_harness_v1.py",
             ROOT/"deliverables/cm2_c27_t04_double_graphs_common_v2_terminal_seal_v1.py",
             ROOT/"deliverables/cm2_c27_t04_double_graphs_common_v2_postpublication_cold_replay_v1.py"]
    members=[*(aa/n for n in names),*(bb/n for n in names),vpath,apath,nr,nc,*sources]
    out.mkdir(parents=True);pm=out/"payload_manifest.sha256";pm.write_bytes(man(members))
    body={"schema":"cm2.c27-independent.t04-double-graphs.common-v2-terminal-zero-credit-receipt.v1",
          "status":"PASS_T04_COMMON_V2_CANDIDATE_OWNERSHIP_AND_MATERIALIZED_PROOF_JOIN_DUAL_SEED_NO_IMPORT_25_ATTACKS_SEALED__ZERO_CREDIT",
          "terminal":"DOUBLE_GRAPHS","terminal_ordinal":4,"authority_slot":"T04_DOUBLE_GRAPHS",
          "candidate_schema":ar["candidate_ownership_ledger"]["row_schema"],"proof_schema":ar["materialized_physical_proof_join_ledger"]["row_schema"],
          "candidate_key_namespace":ar["candidate_key_namespace"],"proof_key_namespace":ar["proof_key_namespace"],
          "candidate_pairs":1_362_088,"materialized_physical_proof_rows":1_362_088,
          "candidate_ledger_sha256":sha(aa/names[0]),"proof_ledger_sha256":sha(aa/names[1]),
          "each_candidate_exactly_one_terminal":True,"each_candidate_exactly_one_proof":True,
          "unresolved":0,"legal_cross_component_witnesses":0,"component_edges":0,
          "coherent_attacks":{"accepted":0,"rejected":25},
          "native_T04_terminal_receipt_sha256":sha(nr),"native_T04_cold_replay_sha256":sha(nc),
          "payload_manifest":{"path":rel(pm),"sha256":sha(pm),"entry_count":len(members)},
          "formal_credit":0,"manifest_authorized":False,"source_W_transition_authorized":False,
          "strict_nonpromotion":{"C27":"UNAUTHORIZED","C28":"UNAUTHORIZED","C29":"UNAUTHORIZED","Source_W":80,"CM2":"NO-GO_FOR_CLAIM"}}
    receipt={**body,"receipt_sha256":digest(body)};rp=out/"receipt.json";rp.write_bytes(enc(receipt)+b"\n")
    rm=out/"root_manifest.sha256";rm.write_bytes(man([pm,rp]))
    print(enc({"status":receipt["status"],"receipt_file_sha256":sha(rp),"receipt_sha256":receipt["receipt_sha256"],"root_manifest_sha256":sha(rm)}).decode());return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except Reject as e:print("T04_COMMON_V2_SEAL_REJECT:"+str(e));raise SystemExit(2)
