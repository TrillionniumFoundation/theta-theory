#!/usr/bin/env python3
"""Native page geometry and actual recorder coverage; no proof certification."""
from pathlib import Path
import hashlib,json,math,re,subprocess,xml.etree.ElementTree as ET
from check_v104 import require
PAPER=Path(__file__).resolve().parents[1]
BUILD=PAPER/'build';E=PAPER/'evidence'
def inspect(name):
    pdf=BUILD/(name+'.pdf');bbox=E/(name+'-bbox.html')
    subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    text=''.join(c for c in bbox.read_text() if ord(c)>=32 or c in '\n\r\t')
    doc=ET.fromstring(text);pages=[x for x in doc.iter() if x.tag.rsplit('}',1)[-1]=='page']
    require(bool(pages),'empty native PDF')
    words=0
    for number,p in enumerate(pages,1):
        w,h=float(p.attrib['width']),float(p.attrib['height'])
        for x in p.iter():
            if x.tag.rsplit('}',1)[-1]!='word':continue
            x0,y0,x1,y1=[float(x.attrib[k]) for k in ('xMin','yMin','xMax','yMax')]
            require(all(math.isfinite(z) for z in (x0,y0,x1,y1)),'nonfinite PDF geometry')
            require(-.5<=x0<=x1<=w+.5 and -.5<=y0<=y1<=h+.5,f'{name} page {number} text outside page')
            words+=1
    cores=set()
    for line in (BUILD/(name+'.fls')).read_text().splitlines():
        if line.startswith('INPUT '):
            m=re.search(r'(?:^|/)core/([^/]+\.tex)$',line[6:])
            if m:cores.add(m.group(1))
    return {'pages':len(pages),'words':words,'core_modules':sorted(cores),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}
def main():
    E.mkdir(exist_ok=True)
    result={n:inspect(n) for n in ('main','supplement')}
    expected={p.name for p in (PAPER/'core').glob('*.tex')}
    union=set(result['main']['core_modules'])|set(result['supplement']['core_modules'])
    require(len(expected)==252 and union==expected,'252-core recorder union')
    require(len(result['main']['core_modules'])==3,'three new article modules')
    require(len(result['supplement']['core_modules'])==249,'complete inherited supplement modules')
    for name in ('main','supplement'):
        pages=range(1,result[name]['pages']+1) if name=='main' else (1,2,result[name]['pages'])
        for p in pages:
            subprocess.run(['pdftoppm','-f',str(p),'-l',str(p),'-singlefile','-r','80','-png',
                str(BUILD/(name+'.pdf')),str(E/f'{name}-{p:03d}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    result['scope']='Native PDF geometry and TeX recorder coverage, not continuum proof certification'
    (E/'v104-render.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({n:{'pages':result[n]['pages'],'cores':len(result[n]['core_modules'])} for n in ('main','supplement')},indent=2))
if __name__=='__main__':main()
