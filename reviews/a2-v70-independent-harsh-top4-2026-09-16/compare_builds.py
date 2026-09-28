#!/usr/bin/env python3
"""Compare independently compiled PDFs to native PDFs, page by page.
Usage: python compare_builds.py ARTIFACT_DIRECTORY BUILD_DIRECTORY
Requires PyMuPDF. Matching pixels/text is not a mathematical or all-page visual review.
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
import fitz

def main():
    if len(sys.argv)!=3:
        raise SystemExit(__doc__)
    native,build=map(Path,sys.argv[1:]); results={}
    for entry in ('two_collision','main','rigidity'):
        a=native/(entry+'.pdf'); b=build/(entry+'.pdf')
        da,db=fitz.open(a),fitz.open(b)
        if len(da)!=len(db):
            raise ValueError(f'page-count mismatch {entry}')
        text_bad=[];pixel_bad=[]
        for i in range(len(da)):
            pa,pb=da[i],db[i]
            if pa.get_text()!=pb.get_text(): text_bad.append(i+1)
            xa=pa.get_pixmap(dpi=72,colorspace=fitz.csRGB,alpha=False)
            xb=pb.get_pixmap(dpi=72,colorspace=fitz.csRGB,alpha=False)
            if (xa.width,xa.height,xa.samples)!=(xb.width,xb.height,xb.samples):pixel_bad.append(i+1)
        log=(build/(entry+'.log')).read_text(errors='replace')
        critical=[s for s in log.splitlines() if re.search(r'^!|LaTeX Error|Missing character|undefined|multiply defined|Overfull',s,re.I)]
        results[entry]={'pages':len(da),'native_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),
            'independent_sha256':hashlib.sha256(b.read_bytes()).hexdigest(),
            'identical_pdf_bytes':a.read_bytes()==b.read_bytes(),
            'text_difference_pages':text_bad,'rgb72_difference_pages':pixel_bad,
            'critical_final_log_lines':critical,'underfull_notices':log.count('Underfull'),
            'no_shell_escape_marker':'restricted \\write18 enabled' not in log and '\\write18 enabled' not in log}
        if text_bad or pixel_bad or critical:
            raise ValueError(json.dumps({entry:results[entry]}))
    print(json.dumps({'renderer':fitz.VersionBind,'rgb_dpi':72,'entries':results,
        'all_pages_text_and_rgb_equal':True,'total_pages':sum(v['pages'] for v in results.values()),
        'scope':'Automated same-renderer equality, not an all-page visual/mathematical examination.'},indent=2))
if __name__=='__main__':main()
