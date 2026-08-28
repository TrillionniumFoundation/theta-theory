#!/usr/bin/env python3
"""Coherent mutation attacks for C11a."""
from __future__ import annotations
import argparse,gzip,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from typing import Any,Callable
ROOT=Path(__file__).parent; PREFIX="cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel"; RESULT=PREFIX+"_result.json"; LEDGER=PREFIX+"_ledger.jsonl.gz"; VERIFIER=ROOT/(PREFIX+"_independent_verifier.py")
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def object_sha(x:Any)->str:return sha(canonical(x))
def close_row(r:dict[str,Any])->None:r.pop("row_sha256",None);r["row_sha256"]=object_sha(r)
def load(p:Path)->list[dict[str,Any]]:
    with gzip.open(p,"rt",encoding="utf-8") as f:return [json.loads(x) for x in f]
def store(p:Path,rs:list[dict[str,Any]],d:dict[str,Any])->None:
    plain=b"".join(canonical(r)+b"\n" for r in rs);wire=gzip.compress(plain,compresslevel=9,mtime=0);p.write_bytes(wire)
    d.update({"row_count":len(rs),"compressed_size":len(wire),"compressed_sha256":sha(wire),"uncompressed_size":len(plain),"uncompressed_sha256":sha(plain),"ordered_row_ids_sha256":object_sha([r["row_id"] for r in rs]),"ordered_row_hashes_sha256":object_sha([r["row_sha256"] for r in rs]),"ordered_rows_sha256":object_sha(rs)})
def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir",required=True);a=ap.parse_args();src=Path(a.candidate_dir).resolve()
    def ref(field:str)->Callable[[list[dict[str,Any]]],None]:
        def f(rs:list[dict[str,Any]])->None:rs[0][field]["row_sha256"]="0"*64;close_row(rs[0])
        return f
    changes:list[tuple[str,Callable[[list[dict[str,Any]]],None]]]=[
      ("routing-ref",ref("C11_routing_disposition_ref")),("support-ref",ref("C10_exact_graph_support_ref")),
      ("side-ast",lambda rs:(rs[0].__setitem__("exact_side_stratum_ast",{"op":"RATIONAL_CONSTANT","value":"0"}),rs[0].__setitem__("exact_side_stratum_ast_sha256",object_sha(rs[0]["exact_side_stratum_ast"])),close_row(rs[0]))),
      ("erase-branch-equivalence",lambda rs:(rs[0]["partition_branch_to_side_member_equivalence_certificate"].__setitem__("side_member_exact_support_equivalence_proved",False),rs[0]["partition_branch_to_side_member_equivalence_certificate"].__setitem__("certificate_sha256",object_sha({k:v for k,v in rs[0]["partition_branch_to_side_member_equivalence_certificate"].items() if k!="certificate_sha256"})),close_row(rs[0]))),
      ("erase-closure",lambda rs:(rs[0]["closure_incidence_certificate"].__setitem__("closure_incidence_complete",False),rs[0]["closure_incidence_certificate"].__setitem__("certificate_sha256",object_sha({k:v for k,v in rs[0]["closure_incidence_certificate"].items() if k!="certificate_sha256"})),close_row(rs[0]))),
      ("erase-trace",lambda rs:(rs[0]["one_sided_trace_certificate"].__setitem__("every_graph_point_has_a_side_approach_path",False),close_row(rs[0]))),
      ("forge-B1A",lambda rs:(rs[0]["strict_nonpromotion"].__setitem__("B1A",1),close_row(rs[0]))),
      ("duplicate-subject",lambda rs:(rs[1].__setitem__("graph_id",rs[0]["graph_id"]),rs[1].__setitem__("side_role",rs[0]["side_role"]),rs[1].__setitem__("side_member_id",rs[0]["side_member_id"]),close_row(rs[1]))),]
    rejected=[]
    with tempfile.TemporaryDirectory(prefix="c11a-attacks.") as base:
      for i,(name,change) in enumerate(changes):
        d=Path(base)/f"{i:02d}-{name}";d.mkdir();shutil.copy2(src/RESULT,d/RESULT);shutil.copy2(src/LEDGER,d/LEDGER)
        result=json.loads((d/RESULT).read_bytes());rs=load(d/LEDGER);change(rs);store(d/LEDGER,rs,result["kernel_ledger"]);result.pop("result_sha256",None);result["result_sha256"]=object_sha(result);(d/RESULT).write_bytes(canonical(result))
        run=subprocess.run([sys.executable,"-I","-B",str(VERIFIER),"--candidate-dir",str(d)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if run.returncode==0:raise RuntimeError("attack accepted:"+name)
        rejected.append(name)
    print(json.dumps({"status":"PASS_C11A_COHERENT_ATTACKS","rejected":len(rejected),"attacks":rejected},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
