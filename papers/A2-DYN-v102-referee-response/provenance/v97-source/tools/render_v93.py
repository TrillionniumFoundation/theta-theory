#!/usr/bin/env python3
"""Validate PDF geometry and actual core recorder coverage; not proof certification."""
from pathlib import Path
import hashlib,json,math,re,subprocess,sys
import xml.etree.ElementTree as ET
from check_v93 import require
PAPER=Path(__file__).resolve().parents[1]

def inspect(name: str) -> dict:
    pdf=PAPER/'build'/f'{name}.pdf';bbox=PAPER/'evidence'/f'{name}-bbox.html'
    subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    text=''.join(c for c in bbox.read_text() if ord(c)>=32 or c in '\n\t\r')
    root=ET.fromstring(text);pages=[e for e in root.iter() if e.tag.split('}')[-1]=='page']
    require(bool(pages),'empty PDF');words=0
    for i,page in enumerate(pages,1):
        w,h=float(page.attrib['width']),float(page.attrib['height'])
        for x in page.iter():
            if x.tag.split('}')[-1]!='word':continue
            a,b,c,d=[float(x.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
            require(all(math.isfinite(z) for z in [a,b,c,d]) and -.5<=a<=c<=w+.5 and -.5<=b<=d<=h+.5,
                    f'{name} page {i}: word outside page')
            words+=1
    cores=set()
    for line in (PAPER/'build'/f'{name}.fls').read_text().splitlines():
        if line.startswith('INPUT '):
            found=re.search(r'(?:^|/)core/([^/]+\.tex)$',line[6:])
            if found:cores.add(found.group(1))
    return {'pages':len(pages),'words':words,'cores':sorted(cores),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}

def main() -> None:
    require(sys.argv[1:] in ([],['--local']),'unknown arguments')
    out={n:inspect(n) for n in ['main','supplement']}
    require(len(out['main']['cores'])==3,'journal core coverage')
    require(len(out['supplement']['cores'])==219,'complete inherited supplement coverage')
    expected={p.name for p in (PAPER/'core').glob('*.tex')}
    require(len(expected)==222 and set(out['main']['cores'])|set(out['supplement']['cores'])==expected,'core union')
    (PAPER/'evidence/v93-render.json').write_text(json.dumps(out,indent=2)+'\n')
    for name in out:
        pages=range(1,out[name]['pages']+1) if name=='main' else [1,2,out[name]['pages']]
        for n in pages:
            subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1200','-png',
                str(PAPER/'build'/f'{name}.pdf'),str(PAPER/'evidence'/f'{name}-{n:03d}')],check=True,
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(json.dumps({n:{'pages':r['pages'],'core_count':len(r['cores'])} for n,r in out.items()},indent=2))
if __name__=='__main__':main()
