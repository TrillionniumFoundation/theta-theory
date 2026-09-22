#!/usr/bin/env python3
"""Export only the opposite part's labels, avoiding duplicate definitions."""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
text=(HERE/'paper.tex').read_text();core,apps=text.split(r'\appendix',1)
def labels(part):
    out=set()
    for path in re.findall(r'\\input\{([^}]+)\}',part):
        if path=='references.tex': continue
        source=(HERE/path).read_text()
        out.update(re.findall(r'\\label\{([^}]+)\}',source))
        out.update(labels(source))
    return out
sets={'core':labels(core),'applications':labels(apps)}
lines=(HERE/'paper.aux').read_text().splitlines()
(HERE/'crossrefs').mkdir(exist_ok=True)
for part,names in sets.items():
    chosen=[line for line in lines if (m:=re.match(r'\\newlabel\{([^}]+)\}',line)) and m.group(1) in names]
    if len(chosen)!=len(names):raise RuntimeError('incomplete compiled reference set '+part)
    (HERE/'crossrefs'/f'{part}.aux').write_text('\n'.join(chosen)+'\n')
    print(part,len(chosen),'labels exported')
