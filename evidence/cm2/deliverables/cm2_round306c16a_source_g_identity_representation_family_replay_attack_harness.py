#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PREFIX="cm2_round306c16a_source_g_identity_representation_family_replay";RESULT=PREFIX+"_result.json";VERIFIER=ROOT/(PREFIX+"_independent_verifier.py")
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def close(v):
 b=dict(v);b.pop("result_sha256",None);return {**b,"result_sha256":hashlib.sha256(canonical(b)).hexdigest()}
def main():
 candidate=Path(sys.argv[1]).resolve();base=json.loads((candidate/RESULT).read_bytes())
 attacks=[("member_total",lambda d:d["member_census"].__setitem__("total",502203)),("new_member_count",lambda d:d["member_census"].__setitem__("new_C14c",4431)),("nongraph_family",lambda d:d["member_census"]["family_counts"].__setitem__("NON_GRAPH",55603)),("representation_total",lambda d:d["representation_census"].__setitem__("total",549615)),("G2A_rep_family",lambda d:d["representation_census"]["family_counts"].__setitem__("G2A",5263)),("member_credit",lambda d:d["formal_credit"].__setitem__("member_identity_family_replay",502203)),("pullback_pollution",lambda d:d["strict_nonpromotion"].__setitem__("representation_pullback",1)),("CM2_pollution",lambda d:d["strict_nonpromotion"].__setitem__("CM2","GO"))]
 rejected=[]
 for name,mutate in attacks:
  with tempfile.TemporaryDirectory(prefix="c16a-attack-")as raw:
   q=Path(raw)
   for p in candidate.iterdir():
    if p.name!=RESULT:os.symlink(p,q/p.name)
   d=copy.deepcopy(base);mutate(d);(q/RESULT).write_bytes(canonical(close(d)));run=subprocess.run([sys.executable,"-I","-B",str(VERIFIER),"--candidate-dir",str(q)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   if run.returncode==0:raise RuntimeError("accepted:"+name)
   rejected.append(name)
 print(json.dumps({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rejected},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
