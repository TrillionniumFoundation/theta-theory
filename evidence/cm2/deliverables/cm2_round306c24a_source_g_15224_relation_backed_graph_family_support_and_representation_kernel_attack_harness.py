#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel";R=P+"_result.json";V=ROOT/(P+"_independent_verifier.py");PY=ROOT.parent/".venv-cm2/bin/python"
def canon(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def close(value):body=dict(value);body.pop("result_sha256",None);return{**body,"result_sha256":hashlib.sha256(canon(body)).hexdigest()}
def main():
 candidate=Path(sys.argv[1]).resolve();base=json.loads((candidate/R).read_bytes());attacks=[("G2A_member",lambda d:d.__setitem__("G2A_member_normalized_support_set_equality_credit",5263)),("G2B_member",lambda d:d.__setitem__("G2B_relation_backed_member_normalized_support_set_equality_credit",9959)),("pullback",lambda d:d.__setitem__("sealed_representation_pullback_credit_consumed",15223)),("representation",lambda d:d.__setitem__("typed_representation_semantic_credit",15223)),("global_credit",lambda d:d.__setitem__("cumulative_global_member_support_credit",502037)),("global_debt",lambda d:d.__setitem__("remaining_global_member_support_debt",167)),("B1A",lambda d:d["strict_nonpromotion"].__setitem__("B1A",1)),("CM2",lambda d:d["strict_nonpromotion"].__setitem__("CM2","GO"))];rejected=[]
 for name,mutate in attacks:
  with tempfile.TemporaryDirectory(prefix="c24a-attack-")as raw:
   target=Path(raw)
   for entry in candidate.iterdir():
    if entry.name!=R:os.symlink(entry,target/entry.name)
   forged=copy.deepcopy(base);mutate(forged);(target/R).write_bytes(canon(close(forged)));run=subprocess.run([str(PY),"-I","-B",str(V),"--candidate-dir",str(target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   if run.returncode==0:raise RuntimeError("accepted:"+name)
   rejected.append(name)
 print(canon({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rejected}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
