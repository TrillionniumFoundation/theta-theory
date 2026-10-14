#!/usr/bin/env python3
"""Check full native PDFs and actual recorder coverage; no proof certification."""
from pathlib import Path
import json
import subprocess
import sys
from check_v100 import require
from render_v102 import inspect
PAPER=Path(__file__).resolve().parents[1]
def main():
    require(not sys.argv[1:],'full article and supplement are mandatory')
    out={name:inspect(name) for name in ('main','supplement')}
    expected={p.name for p in (PAPER/'core').glob('*.tex')}
    require(len(out['main']['core_modules'])==6,'journal six-core coverage')
    require(len(out['supplement']['core_modules'])==246,'complete inherited supplement')
    require(len(expected)==249 and set(out['main']['core_modules'])|set(out['supplement']['core_modules'])==expected,
            'complete 249-core recorder union')
    out['scope']='native PDF word geometry and recorded inputs; not mathematical certification'
    (PAPER/'evidence/v103-render.json').write_text(json.dumps(out,indent=2)+'\n')
    for name in ('main','supplement'):
        pages=range(1,out[name]['pages']+1) if name=='main' else (1,2,out[name]['pages'])
        for page in pages:
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','90','-png',
                str(PAPER/'build'/f'{name}.pdf'),str(PAPER/'evidence'/f'{name}-{page:03d}')],
                check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(json.dumps({k:{'pages':out[k]['pages'],'cores':len(out[k]['core_modules'])} for k in ('main','supplement')},indent=2))
if __name__=='__main__':main()
