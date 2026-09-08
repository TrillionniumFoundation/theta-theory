#!/usr/bin/env python3
"""Compare the native referee build to the supplied v36 PDF contents.

Text identity is checked on every page; sampled render identity is separate.
The contact sheets aid manual inspection, not automatic proof or layout approval.
Requires PyMuPDF and Pillow. This script does not alter either source tree.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--original-root',required=True,type=Path)
    ap.add_argument('--rebuilt-root',required=True,type=Path)
    ap.add_argument('--output-root',required=True,type=Path)
    args=ap.parse_args();out=args.output_root;out.mkdir(parents=True,exist_ok=True)
    selections={'main':[1,8,13,19,22,37,38,39,40,42], 'companions':[1,80,159]}
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),'volumes':{}}
    for name in ('main','companions'):
        a=fitz.open(args.original_root/(name+'.pdf'))
        b=fitz.open(args.rebuilt_root/(name+'.pdf'))
        if len(a)!=len(b):raise RuntimeError('Page count mismatch')
        text_match=[x.get_text()==y.get_text() for x,y in zip(a,b)]
        if not all(text_match):raise RuntimeError('PDF page text differs')
        sample={}
        for page in selections[name]:
            x=a[page-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
            y=b[page-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
            same=x.samples==y.samples and (x.width,x.height)==(y.width,y.height)
            if not same:raise RuntimeError('Sampled raster mismatch')
            y.save(out/f'{name}-{page:03}.png')
            sample[str(page)]={'pixels_identical':same,'pixel_sha256':sha(y.samples)}
        result['volumes'][name]={'pages':len(b),'all_page_text_identical':True,
            'original_pdf_sha256':sha((args.original_root/(name+'.pdf')).read_bytes()),
            'rebuilt_pdf_sha256':sha((args.rebuilt_root/(name+'.pdf')).read_bytes()),
            'sampled_rasters':sample}
        if name=='main':
            for start in range(0,len(b),14):
                sheet=Image.new('RGB',(1800,7*370),'white');draw=ImageDraw.Draw(sheet)
                for j in range(start,min(start+14,len(b))):
                    pix=b[j].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
                    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
                    im.thumbnail((870,345))
                    col,row=(j-start)%2,(j-start)//2
                    x=col*900+(900-im.width)//2;y=row*370+20
                    sheet.paste(im,(x,y));draw.text((col*900+10,row*370+3),f'Main p.{j+1}',fill='black')
                sheet.save(out/f'main-contact-{start//14+1}.png')
    result['scope']='Every-page extracted text identity and 13 sampled raster comparisons; manual visual judgment recorded separately. PDF bytes differ across executions; no byte identity is claimed.'
    (out/'PRODUCTION_COMPARISON.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:{'pages':v['pages'],'text_match':v['all_page_text_identical'],'sampled_renders':len(v['sampled_rasters'])} for k,v in result['volumes'].items()},indent=2))

if __name__=='__main__':
    main()
