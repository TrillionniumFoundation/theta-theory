#!/usr/bin/env python3
"""Minimal r46 append-only clean-room wrapper.

The r45 attempt never installed a candidate; only its builder pyc exists.
This wrapper keeps that pyc as a rejection witness, retains r44 as the real
active predecessor, and retags immutable r39 inputs in memory.
"""
from __future__ import annotations
import ast, hashlib, json, os, stat, sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE":"1", "PYTHONNOUSERSITE":"1"})
ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
PREV = "v16r2r44"; TAG = "v16r2r46"
R44_ANCHOR = OUT / f"{BASE}_v16r2r44_active_predecessor_supersession_receipt_v1.json"
R44_ANCHOR_SHA = "19514a07b5cc65167e7805b73779bd0726ddc6ec023f7456fec120ca3427f316"
R44_ANCHOR_OBJECT = "5a16d62b835f118d309767dd10cdb2f8faa6f9631897edac451b1348d822178d"
R45_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r45_candidate_builder.cpython-312.pyc"
R45_PYC_SHA = "1c813fcba09c07a2613c1d3e96160edba2bc1fa80000ef464ac91b1e806ac892"
R45_PYC_SIZE = 41065
R44_TOOL = ROOT / "scripts/c79g_v16r2r44_candidate_builder.py"

def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def canon(v: Any) -> bytes: return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False).encode()
def stable(p: Path) -> bytes:
    fd=os.open(p,os.O_RDONLY|os.O_CLOEXEC|getattr(os,"O_NOFOLLOW",0))
    try:
        st=os.fstat(fd); named=os.lstat(p)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or (st.st_dev,st.st_ino,st.st_size)!=(named.st_dev,named.st_ino,named.st_size): raise RuntimeError(f"unstable:{p}")
        chunks=[]
        while True:
            x=os.read(fd,1<<20)
            if not x: break
            chunks.append(x)
        if sha(b''.join(chunks)) != sha(b''.join(chunks)): raise RuntimeError("read")
        return b''.join(chunks)
    finally: os.close(fd)
def pycs(): return {str(p):sha(stable(p)) for p in ROOT.rglob("*.pyc")}

def load_r45_tooling():
    p=ROOT/"scripts/c79g_v16r2r45_candidate_builder.py"; raw=stable(p).decode(); tree=ast.parse(raw,str(p)); compile(tree,str(p),"exec")
    ns={"__name__":"_r46_r45_tooling","__file__":str(p),"__package__":None}; exec(compile(tree,str(p),"exec"),ns,ns)
    ns["PREV"]=PREV; ns["TAG"]=TAG
    return ns

def check():
    if not R44_ANCHOR.is_file() or sha(stable(R44_ANCHOR)) != R44_ANCHOR_SHA: raise RuntimeError("r44 anchor drift")
    a=json.loads(stable(R44_ANCHOR).decode())
    if a.get("object_sha256") != R44_ANCHOR_OBJECT or a.get("successor_namespace") != "v16r2r44_semantic_source": raise RuntimeError("r44 anchor semantics")
    if not R45_PYC.is_file() or sha(stable(R45_PYC)) != R45_PYC_SHA or R45_PYC.stat().st_size != R45_PYC_SIZE: raise RuntimeError("r45 pyc witness drift")
    targets=[OUT/f"{BASE}_{TAG}_semantic_source.py",OUT/f"{BASE}_schema_{TAG}.json",OUT/f"{BASE}_contract_{TAG}.json",OUT/f"{BASE}_static_audit_{TAG}.json",OUT/f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",OUT/f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"]
    if any(p.exists() for p in targets): raise RuntimeError("r46 target exists")
    if any(TAG in p for p in pycs()): raise RuntimeError("r46 pyc preexists")
    # Reuse only the r39 clean-room constructor; this read-only call also
    # proves the r42 witness remains reproducible under -I -B.
    t=load_r45_tooling(); t["recompute_guard_witness"]()
    return {"status":"PASS_R46_CLEAN_ROOM_PYC_REJECTION_WITNESS_STATIC_ONLY","predecessor_namespace":PREV,"target_namespace":TAG,"r45_pyc_sha256":R45_PYC_SHA,"formal_global_closure_credit":0,"D02_unlock":False,"runtime_authorized":False,"installation_performed":False}

def install():
    t=load_r45_tooling(); ns=t["load_r44_tooling"](); ctor=ns["load_r40_constructor"](); original=ctor["configure"]
    def configure(module,b):
        original(module,b); ns["_configure_r44"](ctor,b)
    ctor["configure"]=configure
    def reject(b):
        path=OUT/f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
        if path.exists(): raise RuntimeError("r44 rejection unexpectedly exists")
        raw=stable(R45_PYC); value=b.close({"schema":f"cm2.c79g.{PREV}.tooling-pyc-rejection.v1","status":"PERMANENT_FAIL_CLOSED_R45_TOOLING__ZERO_CREDIT","failed_namespace":PREV,"failed_tooling_namespace":"v16r2r45","rejection_reason":"R45_BUILDER_PYC_FAIL_CLOSED","detail":{"pyc_path":str(R45_PYC.relative_to(ROOT)),"pyc_file_sha256":sha(raw),"pyc_size":len(raw),"pyc_mode":stat.S_IMODE(R45_PYC.stat().st_mode),"pyc_nlink":R45_PYC.stat().st_nlink,"active_predecessor_anchor_path":str(R44_ANCHOR.relative_to(ROOT)),"active_predecessor_anchor_file_sha256":R44_ANCHOR_SHA,"candidate_install":False,"runtime_protocol_executed":False},"append_only":True,"overwrite_delete_or_reuse_allowed":False,"runtime_authorized":False,"formal_global_closure_credit":0,"D02_unlock":False,"manifest_created":False,"outer_created":False,"runtime_surface_created":False})
        rr=b.canon(value)+b"\n"; action=b.install(path,rr); v,ir=b.load(path); return {"action":action,"file_sha256":b.sha(ir),"object_sha256":v["object_sha256"]}
    ctor["seal_r39_rejection"]=reject
    return int(ctor["main"]())

def main():
    try:
        result=check()
        if "--install" in sys.argv[1:]: return install()
        print(json.dumps(result,sort_keys=True)); return 0
    except Exception as e:
        print(json.dumps({"status":"FAIL_CLOSED_R46_CLEAN_ROOM","error":{"type":type(e).__name__,"message":str(e)},"formal_global_closure_credit":0,"D02_unlock":False,"installation_performed":False},sort_keys=True)); return 1
if __name__=="__main__": raise SystemExit(main())
