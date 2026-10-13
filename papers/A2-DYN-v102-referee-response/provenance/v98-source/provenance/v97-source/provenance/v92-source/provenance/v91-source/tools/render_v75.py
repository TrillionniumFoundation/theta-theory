#!/usr/bin/env python3
"""PDF geometry and recorder coverage, not mathematical certification."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

PAPER=Path(__file__).resolve().parents[1]
BUILD=PAPER/'build'; EVIDENCE=PAPER/'evidence'


def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)


def labels() -> None:
    # amsart tocindent labels are layout registers, not cross-document references.
    lines=(BUILD/'supplement.aux').read_text().splitlines()
    selected=[s for s in lines if s.startswith('\\newlabel{')
              and not s.startswith('\\newlabel{tocindent')]
    require(len(selected)>1000,'inherited label table unexpectedly short')
    (BUILD/'inherited-labels.aux').write_text('\n'.join(selected)+'\n')


def inspect(name: str) -> dict:
    pdf=BUILD/(name+'.pdf'); bbox=EVIDENCE/(name+'-bbox.html')
    subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    raw=bbox.read_text()
    cleaned=''.join(c for c in raw if ord(c)>=32 or c in '\n\r\t')
    doc=ET.fromstring(cleaned); pages=[e for e in doc.iter() if e.tag.endswith('}page') or e.tag=='page']
    require(bool(pages),'empty PDF')
    words=0
    for number,page in enumerate(pages,1):
        width=float(page.attrib['width']); height=float(page.attrib['height'])
        for item in page.iter():
            if not (item.tag.endswith('}word') or item.tag=='word'): continue
            box=[float(item.attrib[k]) for k in ('xMin','yMin','xMax','yMax')]
            require(all(math.isfinite(x) for x in box),f'{name} page {number}: nonfinite bbox')
            x0,y0,x1,y1=box
            require(-0.5<=x0<=x1<=width+0.5 and -0.5<=y0<=y1<=height+0.5,
                    f'{name} page {number}: text outside page {box}')
            words+=1
    inputs=[]
    for line in (BUILD/(name+'.fls')).read_text().splitlines():
        if line.startswith('INPUT '):
            match=re.search(r'(?:^|/)core/([^/]+\.tex)$',line[6:])
            if match: inputs.append(match.group(1))
    return dict(pages=len(pages),words=words,core_modules=sorted(set(inputs)),
                pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())


def main() -> None:
    import sys
    if sys.argv[1:]==['--labels']:
        labels(); return
    require(not sys.argv[1:],'unknown arguments')
    EVIDENCE.mkdir(exist_ok=True)
    result={name:inspect(name) for name in ('main','supplement')}
    expected={p.name for p in (PAPER/'core').glob('*.tex')}
    union=set(result['main']['core_modules'])|set(result['supplement']['core_modules'])
    require(len(expected)==170 and union==expected,'recorder does not cover every core')
    require(len(result['main']['core_modules'])==3,'journal module count')
    require(len(result['supplement']['core_modules'])==167,'supplement module count')
    result['scope']='native page geometry and actual recorder coverage only'
    result['formal_proof_certificate']=False
    result['independent_human_review']=False
    (EVIDENCE/'v75-render-and-recorder.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{'pages':v['pages'],'cores':len(v['core_modules'])}
                     for k,v in result.items() if isinstance(v,dict)},indent=2))
    # Review images of every journal page; representative supplement pages.
    for name,page_numbers in [('main',range(1,result['main']['pages']+1)),
                              ('supplement',[1,2,result['supplement']['pages']])]:
        for number in page_numbers:
            subprocess.run(['pdftoppm','-f',str(number),'-l',str(number),'-singlefile',
                            '-r','90','-png',str(BUILD/(name+'.pdf')),
                            str(EVIDENCE/f'{name}-preview-{number:04d}')],
                           check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

if __name__=='__main__': main()
