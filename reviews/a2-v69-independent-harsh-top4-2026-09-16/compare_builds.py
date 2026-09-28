#!/usr/bin/env python3
"""Compare supplied and independently built PDFs; does not examine proofs."""
from pathlib import Path
import argparse, hashlib, json, re
import fitz

def compare(native:Path, rebuilt:Path,dpi:float=72):
    rows=[]
    for stem in ('two_collision','main','rigidity'):
        a=fitz.open(native/(stem+'.pdf'));b=fitz.open(rebuilt/(stem+'.pdf'))
        if len(a)!=len(b): raise ValueError('page-count mismatch: '+stem)
        text_bad=[];render_bad=[]
        for i,(pa,pb) in enumerate(zip(a,b),1):
            if pa.get_text()!=pb.get_text():text_bad.append(i)
            xa=pa.get_pixmap(matrix=fitz.Matrix(dpi/72,dpi/72),colorspace=fitz.csRGB,alpha=False)
            xb=pb.get_pixmap(matrix=fitz.Matrix(dpi/72,dpi/72),colorspace=fitz.csRGB,alpha=False)
            if (xa.width,xa.height,xa.samples)!=(xb.width,xb.height,xb.samples):render_bad.append(i)
        log=(rebuilt/(stem+'.log')).read_text(errors='replace')
        bad=[p for p in [r'Overfull \\[hv]box',r'LaTeX Error',r'Missing character:',r'LaTeX Warning: (?:Reference|Citation).*undefined',r'There were undefined references',r'multiply[- ]defined'] if re.search(p,log,re.I)]
        rows.append(dict(entry=stem,pages=len(a),text_mismatch_pages=text_bad,RGB_mismatch_pages=render_bad,dpi=dpi,local_pdf_sha256=hashlib.sha256((rebuilt/(stem+'.pdf')).read_bytes()).hexdigest(),fatal_scan=bad,local_underfull=len(re.findall(r'Underfull \\[hv]box',log))))
    return dict(scope='Same-renderer page text and RGB consistency, not mathematical or all-page visual review',entries=rows)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('rebuilt',type=Path);p.add_argument('--dpi',type=float,default=72);args=p.parse_args()
    print(json.dumps(compare(args.native,args.rebuilt,args.dpi),indent=2,sort_keys=True))
