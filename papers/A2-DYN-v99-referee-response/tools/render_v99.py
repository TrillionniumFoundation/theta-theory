#!/usr/bin/env python3
"""Native PDF geometry and actual recorder coverage, not proof certification."""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from check_v99 import require
PAPER=Path(__file__).resolve().parents[1]
BUILD=PAPER/'build'; EVIDENCE=PAPER/'evidence'

def inspect(name: str) -> dict:
    pdf=BUILD/(name+'.pdf'); box=EVIDENCE/(name+'-bbox.html')
    subprocess.run(['pdftotext','-bbox',str(pdf),str(box)],check=True)
    text=''.join(c for c in box.read_text() if ord(c)>=32 or c in '\n\r\t')
    doc=ET.fromstring(text)
    pages=[p for p in doc.iter() if p.tag.rsplit('}',1)[-1]=='page']
    require(bool(pages),'empty PDF')
    words=0
    for i,page in enumerate(pages,1):
        w,h=float(page.attrib['width']),float(page.attrib['height'])
        for word in page.iter():
            if word.tag.rsplit('}',1)[-1]!='word':continue
            x0,y0,x1,y1=[float(word.attrib[k]) for k in ('xMin','yMin','xMax','yMax')]
            require(all(math.isfinite(v) for v in (x0,y0,x1,y1)),'nonfinite word')
            require(-.5<=x0<=x1<=w+.5 and -.5<=y0<=y1<=h+.5,f'{name} page {i}: clipped word')
            words+=1
    cores=set()
    for line in (BUILD/(name+'.fls')).read_text().splitlines():
        if line.startswith('INPUT '):
            match=re.search(r'(?:^|/)core/([^/]+\.tex)$',line[6:])
            if match:cores.add(match.group(1))
    return {'pages':len(pages),'words':words,'core_modules':sorted(cores),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}

def main() -> None:
    require(sys.argv[1:] in ([],['--preview'],['--local']),'unknown render arguments')
    preview=sys.argv[1:]==['--preview'];require(not preview or os.environ.get('GITHUB_ACTIONS')!='true','CI preview')
    names=['main'] if preview else ['main','supplement']
    out={name:inspect(name) for name in names}
    require(len(out['main']['core_modules'])==6,'journal core coverage')
    if not preview:
        expected={p.name for p in (PAPER/'core').glob('*.tex')}
        union=set(out['main']['core_modules'])|set(out['supplement']['core_modules'])
        require(len(expected)==240 and union==expected,'complete 240-core coverage')
        require(len(out['supplement']['core_modules'])==237,'full preceding archive coverage')
    out['qualification_mode']='journal preview only' if preview else 'full native article and archive'
    (EVIDENCE/'v99-render.json').write_text(json.dumps(out,indent=2)+'\n')
    for name in names:
        page_numbers=range(1,out[name]['pages']+1) if name=='main' else [1,2,out[name]['pages']]
        for n in page_numbers:
            subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-r','90','-png',
                            str(BUILD/(name+'.pdf')),str(EVIDENCE/f'{name}-{n:03d}')],
                           check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(json.dumps({name:{'pages':out[name]['pages'],'cores':len(out[name]['core_modules'])} for name in names},indent=2))
if __name__=='__main__':main()
