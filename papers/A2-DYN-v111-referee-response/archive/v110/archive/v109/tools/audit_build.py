#!/usr/bin/env python3
"""Check recorder coverage and current-article typesetting, not theorem truth."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def inputs(folder,name):
    found=set()
    for line in (folder/'build'/f'{name}.fls').read_text().splitlines():
        if line.startswith('INPUT '):
            path=Path(line[6:])
            found.add((path if path.is_absolute() else folder/path).resolve())
    return found
log=(P/'build/main.log').read_text()
for bad in ('LaTeX Warning:','Package hyperref Warning:','Overfull \\hbox','Overfull \\vbox','Undefined control sequence','Missing character:'):
    need(bad not in log,'current TeX diagnostic: '+bad)
new_inputs=inputs(P,'main')
old=P/'archive/v108'
old_inputs=inputs(old,'main')|inputs(old,'supplement')
new_core=set((P/'core').glob('*.tex')); old_core=set((old/'core').glob('*.tex'))
need(len(new_core)==2 and len(old_core)==259,'wrong core counts')
need(all(p.resolve() in new_inputs for p in new_core),'current core omitted')
need(all(p.resolve() in old_inputs for p in old_core),'historical core omitted')
for name in ('main','history','supplement'):
    need((P/'build'/f'{name}.pdf').stat().st_size>1000,'missing PDF: '+name)
print(json.dumps({'current_core_coverage':2,'historical_core_coverage':259,
                  'total_core_coverage':261,'current_tex_diagnostics':'clean',
                  'formal_proof_certificate':False},sort_keys=True,indent=2))
