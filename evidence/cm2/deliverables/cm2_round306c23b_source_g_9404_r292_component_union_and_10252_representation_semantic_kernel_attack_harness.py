#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c23b_source_g_9404_r292_component_union_and_10252_representation_semantic_kernel";R=P+"_result.json";V=ROOT/(P+"_independent_verifier.py");PY=ROOT.parent/".venv-cm2/bin/python"
def canon(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def close(value):body=dict(value);body.pop("result_sha256",None);return{**body,"result_sha256":hashlib.sha256(canon(body)).hexdigest()}
def main():
 candidate=Path(sys.argv[1]).resolve();base=json.loads((candidate/R).read_bytes());attacks=[("member_credit",lambda d:d.__setitem__("R292_member_normalized_support_set_equality_credit",9403)),("representation_credit",lambda d:d.__setitem__("R292_typed_representation_semantic_credit",10251)),("single_equality",lambda d:d.__setitem__("R292_single_cell_representation_set_equality_credit",9123)),("subcover",lambda d:d.__setitem__("R292_multicell_representation_exact_subcover_disposition_credit",1127)),("face_reglue",lambda d:d.__setitem__("R292_internal_physical_face_reglue_credit_consumed",847)),("global_debt",lambda d:d.__setitem__("remaining_global_member_support_debt",15391)),("B1A",lambda d:d["strict_nonpromotion"].__setitem__("B1A",1)),("CM2",lambda d:d["strict_nonpromotion"].__setitem__("CM2","GO"))];rejected=[]
 for name,mutate in attacks:
  with tempfile.TemporaryDirectory(prefix="c23b-attack-")as raw:
   target=Path(raw)
   for entry in candidate.iterdir():
    if entry.name!=R:os.symlink(entry,target/entry.name)
   forged=copy.deepcopy(base);mutate(forged);(target/R).write_bytes(canon(close(forged)));run=subprocess.run([str(PY),"-I","-B",str(V),"--candidate-dir",str(target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   if run.returncode==0:raise RuntimeError("accepted:"+name)
   rejected.append(name)
 print(canon({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rejected}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
