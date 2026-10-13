#!/usr/bin/env python3
"""Check PDF word geometry and actual TeX recorder coverage; not proof certification."""
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
from check_v95 import require
PAPER=Path(__file__).resolve().parents[1]
BUILD=PAPER/'build'; EVIDENCE=PAPER/'evidence'


def inspect(name: str) -> dict:
    pdf=BUILD/(name+'.pdf'); bbox=EVIDENCE/(name+'-bbox.html')
    subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    text=''.join(c for c in bbox.read_text() if ord(c)>=32 or c in '\n\r\t')
    root=ET.fromstring(text)
    pages=[x for x in root.iter() if x.tag.rsplit('}',1)[-1]=='page']
    require(bool(pages),'empty PDF')
    words=0
    for number,page in enumerate(pages,1):
        width,height=float(page.attrib['width']),float(page.attrib['height'])
        for word in page.iter():
            if word.tag.rsplit('}',1)[-1]!='word':continue
            x0,y0,x1,y1=[float(word.attrib[k]) for k in ('xMin','yMin','xMax','yMax')]
            require(all(math.isfinite(v) for v in (x0,y0,x1,y1)),'nonfinite word box')
            require(-.5<=x0<=x1<=width+.5 and -.5<=y0<=y1<=height+.5,
                    f'{name} page {number}: text outside page')
            words+=1
    cores=set()
    for line in (BUILD/(name+'.fls')).read_text().splitlines():
        if line.startswith('INPUT '):
            match=re.search(r'(?:^|/)core/([^/]+\.tex)$',line[6:])
            if match:cores.add(match.group(1))
    return {'pages':len(pages),'words':words,'core_modules':sorted(cores),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}


def main() -> None:
    require(sys.argv[1:] in ([],['--preview']),'unknown render argument')
    preview=bool(sys.argv[1:])
    require(not preview or os.environ.get('GITHUB_ACTIONS')!='true','preview cannot qualify CI')
    EVIDENCE.mkdir(exist_ok=True)
    names=['main'] if preview else ['main','supplement']
    result={name:inspect(name) for name in names}
    require(len(result['main']['core_modules'])==3,'new journal recorder coverage')
    if not preview:
        actual=set(result['main']['core_modules'])|set(result['supplement']['core_modules'])
        expected={x.name for x in (PAPER/'core').glob('*.tex')}
        require(len(result['supplement']['core_modules'])==225,'complete inherited archive')
        require(len(expected)==228 and actual==expected,'all 228 cores recorded')
    result['scope']='local article preview only' if preview else 'exact-source PDF geometry and 228-core coverage'
    result['mathematical_certificate']=False
    for name in names:
        selected=range(1,result[name]['pages']+1) if name=='main' else [1,2,result[name]['pages']]
        for page in selected:
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','90','-png',
                            str(BUILD/(name+'.pdf')),str(EVIDENCE/f'{name}-{page:03d}')],
                           check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    out=EVIDENCE/('v95-preview-render.json' if preview else 'v95-render.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({n:{'pages':result[n]['pages'],'cores':len(result[n]['core_modules'])} for n in names},indent=2))


if __name__=='__main__':main()
