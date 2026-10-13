#!/usr/bin/env python3
"""Reuse the pinned page inspector; require complete native recorder coverage."""
from pathlib import Path
import json
import subprocess
import sys
from check_v92 import require
from render_v90 import inspect, PAPER, BUILD, EVIDENCE

def main() -> None:
    require(sys.argv[1:] in ([],['--local']),'unknown arguments')
    result={name:inspect(name) for name in ('main','supplement')}
    expected={p.name for p in (PAPER/'core').glob('*.tex')}
    main_cores=set(result['main']['core_modules'])
    archive_cores=set(result['supplement']['core_modules'])
    require(len(main_cores)==3 and len(archive_cores)==216,'recorder counts')
    require(len(expected)==219 and main_cores|archive_cores==expected,'complete core union')
    result['scope']='all PDF word boxes and native recorder coverage, not proof certification'
    (EVIDENCE/'v92-render.json').write_text(json.dumps(result,indent=2)+'\n')
    for name in ('main','supplement'):
        pages=range(1,result[name]['pages']+1) if name=='main' else [1,2,result[name]['pages']]
        for page in pages:
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','90','-png',
                            str(BUILD/(name+'.pdf')),str(EVIDENCE/f'{name}-{page:03d}')],
                           check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(json.dumps({k:{'pages':result[k]['pages'],'cores':len(result[k]['core_modules'])}
                      for k in ('main','supplement')},indent=2))
if __name__=='__main__':main()
