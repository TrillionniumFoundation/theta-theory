#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel";R=P+"_result.json";V=ROOT/(P+"_independent_verifier.py")
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def close(v):b=dict(v);b.pop("result_sha256",None);return{**b,"result_sha256":hashlib.sha256(c(b)).hexdigest()}
def main():
 q=Path(sys.argv[1]).resolve();base=json.loads((q/R).read_bytes());attacks=[("A1",lambda d:d.__setitem__("A1_credit",223)),("A2",lambda d:d.__setitem__("A2_credit",783)),("debt",lambda d:d.__setitem__("remaining_preserved_A1_A2_obligation_debt",79085)),("exhaustion",lambda d:d["incidence_exhaustion"].__setitem__("all_504_A2_curves_referenced_by_A2_endpoints",False)),("DSU",lambda d:d["strict_nonpromotion"].__setitem__("new_DSU_unions",1)),("B1A",lambda d:d["strict_nonpromotion"].__setitem__("B1A",1)),("B2",lambda d:d["strict_nonpromotion"].__setitem__("B2",1)),("CM2",lambda d:d["strict_nonpromotion"].__setitem__("CM2","GO"))];rejected=[]
 for name,mutate in attacks:
  with tempfile.TemporaryDirectory(prefix="c21a-attack-")as raw:
   target=Path(raw)
   for entry in q.iterdir():
    if entry.name!=R:os.symlink(entry,target/entry.name)
   forged=copy.deepcopy(base);mutate(forged);(target/R).write_bytes(c(close(forged)));run=subprocess.run([sys.executable,"-I","-B",str(V),"--candidate-dir",str(target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   if run.returncode==0:raise RuntimeError("accepted:"+name)
   rejected.append(name)
 print(c({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rejected}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
