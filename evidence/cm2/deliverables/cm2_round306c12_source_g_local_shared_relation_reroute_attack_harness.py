#!/usr/bin/env python3
"""Coherent mutation attacks for C12 rerouting."""
from __future__ import annotations
import argparse,gzip,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from typing import Any,Callable
ROOT=Path(__file__).parent;PREFIX="cm2_round306c12_source_g_local_shared_relation_reroute";RESULT=PREFIX+"_result.json";LEDGER=PREFIX+"_ledger.jsonl.gz";VERIFIER=ROOT/(PREFIX+"_independent_verifier.py")
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def obj(x:Any)->str:return sha(canonical(x))
def close(r:dict[str,Any])->None:r.pop("row_sha256",None);r["row_sha256"]=obj(r)
def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir",required=True);a=ap.parse_args();src=Path(a.candidate_dir).resolve()
 def finding(rs):rs[0]["C11_finding_ref"]["row_sha256"]="0"*64;close(rs[0])
 def bridge(rs):rs[0]["C4_bridge_ref"]["row_sha256"]="0"*64;close(rs[0])
 attacks:[tuple[str,Callable[[list[dict[str,Any]]],None]]]=[("finding-ref",finding),("bridge-ref",bridge),("graph-id",lambda rs:(rs[0].__setitem__("positive_source_graph_id","forged"),close(rs[0]))),("side-role",lambda rs:(rs[0].__setitem__("side_role","target:SAME_SIGN_EVENT_ABSENT"),close(rs[0]))),("component",lambda rs:(rs[0].__setitem__("component_relation","CROSS_COMPONENT"),close(rs[0]))),("physical-credit",lambda rs:(rs[0].__setitem__("local_graph_side_physical_incidence_proved",True),close(rs[0]))),("DSU-credit",lambda rs:(rs[0].__setitem__("DSU_edge_or_union_authorized",True),close(rs[0]))),("duplicate-graph",lambda rs:(rs[1].__setitem__("positive_source_graph_id",rs[0]["positive_source_graph_id"]),close(rs[1])))]
 rejected=[]
 with tempfile.TemporaryDirectory(prefix="c12-attacks.") as base:
  for i,(name,change) in enumerate(attacks):
   d=Path(base)/str(i);d.mkdir();shutil.copy2(src/RESULT,d/RESULT);shutil.copy2(src/LEDGER,d/LEDGER);result=json.loads((d/RESULT).read_bytes())
   with gzip.open(d/LEDGER,"rt",encoding="utf-8") as f:rs=[json.loads(x) for x in f]
   change(rs);plain=b"".join(canonical(r)+b"\n" for r in rs);wire=gzip.compress(plain,compresslevel=9,mtime=0);(d/LEDGER).write_bytes(wire);desc=result["reroute_ledger"];desc.update({"compressed_size":len(wire),"compressed_sha256":sha(wire),"uncompressed_size":len(plain),"uncompressed_sha256":sha(plain),"ordered_rows_sha256":obj(rs)});result.pop("result_sha256",None);result["result_sha256"]=obj(result);(d/RESULT).write_bytes(canonical(result))
   run=subprocess.run([sys.executable,"-I","-B",str(VERIFIER),"--candidate-dir",str(d)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   if run.returncode==0:raise RuntimeError("attack accepted:"+name)
   rejected.append(name)
 print(json.dumps({"status":"PASS_C12_COHERENT_ATTACKS","rejected":len(rejected),"attacks":rejected},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
