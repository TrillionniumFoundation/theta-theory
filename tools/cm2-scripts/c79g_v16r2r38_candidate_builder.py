#!/usr/bin/env python3
"""Fresh r38 clean-room builder after r37 checkpoint-census rejection."""
from __future__ import annotations
import ast, os
from pathlib import Path
from types import ModuleType
os.environ.update({"PYTHONDONTWRITEBYTECODE":"1","PYTHONNOUSERSITE":"1","CM2_TEMPLATE_SUFFIX":"v16r2r34","CM2_TEMPLATE_PREV_SUFFIX":"v16r2r33","CM2_PREDECESSOR_SUFFIX":"v16r2r37","CM2_SUCCESSOR_SUFFIX":"v16r2r38"})
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]; BASE="cm2_round306c79g_true_global_no_producer_consumer"; TAG="v16r2r38"; PREV="v16r2r37"

def load_outer()->ModuleType:
    p=ROOT/"scripts/c79g_v16r2r35_candidate_builder.py"; t=p.read_text(encoding="utf-8")
    for old,new in (("TAG = \"v16r2r35\"",f"TAG = \"{TAG}\""),("PREV = \"v16r2r34\"",f"PREV = \"{PREV}\""),("CM2_PREDECESSOR_SUFFIX\"] = \"v16r2r34\"",f"CM2_PREDECESSOR_SUFFIX\"] = \"{PREV}\""),("CM2_SUCCESSOR_SUFFIX\"] = \"v16r2r35\"",f"CM2_SUCCESSOR_SUFFIX\"] = \"{TAG}\"")): t=t.replace(old,new,1)
    m=ModuleType("_r38_builder"); m.__file__=str(p); m.__package__=None; exec(compile(t,str(p),"exec"),m.__dict__,m.__dict__); return m

def prepare(mod:ModuleType)->None:
    inner=mod.load_r34_module()
    def fixed_loads(text:str,role:str):
        tree=ast.parse(text,mode="exec"); starts=[]; total=0
        for line in text.splitlines(keepends=True): starts.append(total); total+=len(line.encode())
        symbol="CHECKPOINT" if role=="launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"; replacement=symbol
        spans=[(starts[n.lineno-1]+n.col_offset,starts[n.end_lineno-1]+n.end_col_offset) for n in ast.walk(tree) if isinstance(n,ast.Name) and n.id==symbol and isinstance(n.ctx,ast.Load)]
        raw=text.encode()
        for a,b in sorted(spans,reverse=True): raw=raw[:a]+replacement.encode()+raw[b:]
        return raw.decode(),len(spans)
    def fixed_paths(text:str,role:str)->str:
        for old,new in ((f"{BASE}_v16r2r34_semantic_source.py",f"{BASE}_{TAG}_semantic_source.py"),(f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r34_semantic_source.py",f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"),(f"{BASE}_cold_launch_v16r2r34_semantic_source.py",f"{BASE}_cold_launch_{TAG}_semantic_source.py")): text=text.replace(old,new)
        return text
    inner.replace_checkpoint_loads=fixed_loads; inner.source_paths=fixed_paths; mod.install_retag(inner); mod.load_r34_module=lambda:inner
    old=inner.load_generic
    def load_generic_patched():
        b=old(); b.retag=inner.retag; b.source_patch=inner.source_patch; return b
    inner.load_generic=load_generic_patched

def main()->int:
    mod=load_outer(); prepare(mod); return int(mod.main())
if __name__=="__main__": raise SystemExit(main())
