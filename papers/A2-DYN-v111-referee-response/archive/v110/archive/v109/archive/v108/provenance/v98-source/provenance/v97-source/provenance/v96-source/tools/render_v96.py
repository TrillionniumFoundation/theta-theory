#!/usr/bin/env python3
"""Native PDF page-box and actual recorder checks; not proof certification."""
from pathlib import Path
import hashlib,json,math,re,subprocess
import xml.etree.ElementTree as ET
from check_v96 import require
PAPER=Path(__file__).resolve().parents[1]
BUILD=PAPER/'build';EVIDENCE=PAPER/'evidence'

def inspect(name: str) -> dict:
    pdf=BUILD/(name+'.pdf');box=EVIDENCE/(name+'-bbox.html')
    subprocess.run(['pdftotext','-bbox',str(pdf),str(box)],check=True)
    clean=''.join(c for c in box.read_text() if ord(c)>=32 or c in '\n\r\t')
    root=ET.fromstring(clean);pages=[p for p in root.iter() if p.tag.split('}')[-1]=='page']
    require(bool(pages),'empty PDF');words=0
    for page in pages:
        w,h=float(page.attrib['width']),float(page.attrib['height'])
        for x in page.iter():
            if x.tag.split('}')[-1]!='word':continue
            a,b,c,d=[float(x.attrib[k]) for k in ('xMin','yMin','xMax','yMax')]
            require(all(math.isfinite(v) for v in (a,b,c,d)),'nonfinite box')
            require(-.5<=a<=c<=w+.5 and -.5<=b<=d<=h+.5,'text outside page')
            words+=1
    cores=set()
    for l in (BUILD/(name+'.fls')).read_text().splitlines():
        if l.startswith('INPUT '):
            m=re.search(r'(?:^|/)core/([^/]+\.tex)$',l[6:])
            if m:cores.add(m.group(1))
    return {'pages':len(pages),'words':words,'core_modules':sorted(cores),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}

def main() -> None:
    EVIDENCE.mkdir(exist_ok=True)
    r={n:inspect(n) for n in ('main','supplement')}
    require(len(r['main']['core_modules'])==3,'journal core coverage')
    require(len(r['supplement']['core_modules'])==228,'prior archive coverage')
    expected={p.name for p in (PAPER/'core').glob('*.tex')}
    require(len(expected)==231 and set(r['main']['core_modules'])|set(r['supplement']['core_modules'])==expected,'full recorder union')
    r['scope']='page geometry and recorder coverage, not mathematical certification'
    (EVIDENCE/'v96-render.json').write_text(json.dumps(r,indent=2)+'\n')
    for n in ('main','supplement'):
        pages=range(1,r[n]['pages']+1) if n=='main' else (1,2,r[n]['pages'])
        for p in pages:
            subprocess.run(['pdftoppm','-f',str(p),'-l',str(p),'-singlefile','-r','90','-png',
               str(BUILD/(n+'.pdf')),str(EVIDENCE/f'{n}-{p:03d}')],check=True,
               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(json.dumps({n:{'pages':r[n]['pages'],'cores':len(r[n]['core_modules'])} for n in ('main','supplement')},indent=2))
if __name__=='__main__':main()
