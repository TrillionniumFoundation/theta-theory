#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c17_source_g_15224_representation_pullback_kernel";RESULT=P+"_result.json";V=ROOT/(P+"_independent_verifier.py")
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def close(v):b=dict(v);b.pop("result_sha256",None);return {**b,"result_sha256":hashlib.sha256(c(b)).hexdigest()}
def main():
 q=Path(sys.argv[1]).resolve();base=json.loads((q/RESULT).read_bytes());attacks=[("total",lambda d:d["pullback_census"].__setitem__("total",15223)),("sheet",lambda d:d["pullback_census"].__setitem__("graph_to_sheet",5263)),("side",lambda d:d["pullback_census"].__setitem__("graph_to_side",9959)),("induced",lambda d:d["pullback_census"].__setitem__("distinct_induced_pullback_representations",15223)),("support",lambda d:d["strict_nonpromotion"].__setitem__("normalized_support",1)),("B1A",lambda d:d["strict_nonpromotion"].__setitem__("B1A",1)),("B2",lambda d:d["strict_nonpromotion"].__setitem__("B2",1)),("CM2",lambda d:d["strict_nonpromotion"].__setitem__("CM2","GO"))];rejected=[]
 for name,mutate in attacks:
  with tempfile.TemporaryDirectory(prefix="c17-attack-")as raw:
   d=Path(raw)
   for f in q.iterdir():
    if f.name!=RESULT:os.symlink(f,d/f.name)
   x=copy.deepcopy(base);mutate(x);(d/RESULT).write_bytes(c(close(x)));r=subprocess.run([sys.executable,"-I","-B",str(V),"--candidate-dir",str(d)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   if r.returncode==0:raise RuntimeError("accepted:"+name)
   rejected.append(name)
 print(json.dumps({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rejected},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
