#!/usr/bin/env python3
"""Read-only reviewer/CI gate for the r19 static DAG."""
from __future__ import annotations
import ast, copy, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"; TAG="v16r2r19"; PREV="v16r2r18"
FILES = {
 "anchor": OUT/f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json",
 "schema": OUT/f"{BASE}_schema_{TAG}.json", "contract": OUT/f"{BASE}_contract_{TAG}.json",
 "producer": OUT/f"{BASE}_{TAG}_semantic_source.py",
 "consumer": OUT/f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
 "transition": OUT/f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
 "audit": OUT/f"{BASE}_static_audit_{TAG}.json",
 "launcher": OUT/f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
SENT = {"d"*64,"e"*64,"f"*64,"c"*64,"b4"*32,"c4"*32}
def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def walk(v):
 yield v
 if isinstance(v,dict):
  for x in v.values(): yield from walk(x)
 elif isinstance(v,list):
  for x in v: yield from walk(x)
def load(p):
 b=p.read_bytes(); v=json.loads(b,object_pairs_hook=lambda xs: dict(xs))
 return v,b
def main():
 rows=[]; fail=[]
 def check(name, ok, detail=None):
  rows.append({"name":name,"passed":bool(ok),**({"detail":detail} if detail else {})})
  if not ok: fail.append(name)
 missing=[k for k,p in FILES.items() if not p.is_file()]; check("all_static_nodes_present",not missing,missing)
 vals={}; raws={}
 if not missing:
  for k,p in FILES.items():
   if p.suffix=='.json':
    try: vals[k],raws[k]=load(p)
    except Exception as e: check(f"json_{k}_strict",False,str(e))
   else:
    try: raws[k]=p.read_bytes(); ast.parse(raws[k].decode()); compile(ast.parse(raws[k].decode()),str(p),'exec'); check(f"ast_compile_{k}",True)
    except Exception as e: check(f"ast_compile_{k}",False,str(e))
  for k,v in vals.items():
   claim=v.get('object_sha256'); b=copy.deepcopy(v); b.pop('object_sha256',None)
   check(f"closure_{k}", isinstance(claim,str) and claim==sha(canon(b)))
  schema=vals.get('schema',{}); refs=sum(isinstance(x,dict) and '$ref' in x for x in walk(schema)); adds=sum(isinstance(x,dict) and x.get('additionalProperties') is False for x in walk(schema))
  check('schema_46_242_52',(len(schema.get('$defs',{})),refs,adds)==(46,242,52),(len(schema.get('$defs',{})),refs,adds))
  check('top_level_30_31_30',(len(vals.get('contract',{})),len(vals.get('transition',{})),len(vals.get('audit',{})))==(30,31,30))
  succ=vals.get('transition',{}).get('successor_v16r2_static_bundle',{}); check('successor_exact11',len(succ)==11,sorted(succ))
  check('no_source_hashes',not any(isinstance(x,dict) and 'source_hashes' in x for x in walk(vals.get('contract',{}))) and not any(isinstance(x,dict) and 'source_hashes' in x for x in walk(succ)) and not any(isinstance(x,dict) and 'source_hashes' in x for x in walk(vals.get('audit',{}).get('audited_v16r2_bundle',{}))))
  blobs=b''.join(raws.get(k,b'') for k in ('producer','consumer','launcher')) + b''.join(raws.get(k,b'') for k in ('schema','contract','transition','audit'))
  check('no_sentinels',not any(s.encode() in blobs for s in SENT) and b'UNPINNED_' not in blobs)
  # Actual pins in the exact successor must match the installed earlier bytes.
  def rel(p): return str(p.relative_to(ROOT))
  h={k:sha(raws[k]) for k in raws};
  checks=[('schema',succ.get('closed_schema',{}).get('file_sha256')),('contract',succ.get('contract',{}).get('file_sha256')),('producer',succ.get('build_only_producer',{}).get('file_sha256')),('consumer',succ.get('independent_verifier_assembler_authority_consumer',{}).get('file_sha256'))]
  check('actual_successor_hashes',all(x[1]==h[x[0]] for x in checks),checks)
  forbidden=[p.name for p in OUT.glob(f'*{TAG}*') if ('manifest' in p.name or 'outer' in p.name or 'credit' in p.name)]
  check('no_manifest_outer_credit',not forbidden,forbidden)
 result={"schema":f"cm2.c79g.{TAG}.reviewer-ci.v1","status":"PASS" if not fail else "REJECT","passed":not fail,"failed_checks":fail,"checks":rows,"hashes":{k:sha(v) for k,v in raws.items()}}
 print(json.dumps(result,sort_keys=True)); return 0 if not fail else 1
if __name__=='__main__': raise SystemExit(main())
