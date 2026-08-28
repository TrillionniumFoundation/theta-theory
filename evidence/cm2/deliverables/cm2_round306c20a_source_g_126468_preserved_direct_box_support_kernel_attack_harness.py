#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel";R=P+"_result.json";V=ROOT/(P+"_independent_verifier.py")
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def close(v):b=dict(v);b.pop("result_sha256",None);return {**b,"result_sha256":hashlib.sha256(c(b)).hexdigest()}
def main():
 q=Path(sys.argv[1]).resolve();base=json.loads((q/R).read_bytes());att=[("member",lambda d:d.__setitem__("member_support_credit",126467)),("rep",lambda d:d.__setitem__("primary_representation_equality_credit",126467)),("alias",lambda d:d.__setitem__("remaining_preserved_alias_representation_debt",39275)),("A1A2",lambda d:d.__setitem__("remaining_preserved_A1_A2_obligation_debt",80091)),("B1A",lambda d:d["strict_nonpromotion"].__setitem__("B1A",1)),("B2",lambda d:d["strict_nonpromotion"].__setitem__("B2",1)),("max",lambda d:d["strict_nonpromotion"].__setitem__("maximality",1)),("CM2",lambda d:d["strict_nonpromotion"].__setitem__("CM2","GO"))];rej=[]
 for name,mut in att:
  with tempfile.TemporaryDirectory(prefix="c20a-attack-")as raw:
   d=Path(raw)
   for f in q.iterdir():
    if f.name!=R:os.symlink(f,d/f.name)
   x=copy.deepcopy(base);mut(x);(d/R).write_bytes(c(close(x)));z=subprocess.run([sys.executable,"-I","-B",str(V),"--candidate-dir",str(d)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   if z.returncode==0:raise RuntimeError("accepted:"+name)
   rej.append(name)
 print(c({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rej}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
