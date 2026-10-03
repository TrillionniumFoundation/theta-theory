#!/usr/bin/env python3
"""Verify the focused journal package and rebuild without repository history.
Requires pdflatex and PyMuPDF; no old PDF, code test or archive is needed.
"""
from pathlib import Path
import hashlib,json,os,subprocess,tempfile,shutil
import fitz
R=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def signature(path):
    out=[]
    with fitz.open(path) as d:
        for p in d:
            pix=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
            text=p.get_text(sort=True)
            out.append({'page':p.number+1,'text_sha256':sha(text.encode()),'raster_sha256':sha(pix.samples),
                        'width':pix.width,'height':pix.height,'characters':len(text)})
    return out

def main():
    m=json.loads((R/'JOURNAL_MANIFEST.json').read_text())
    for n,h in m['files'].items():check(sha((R/n).read_bytes())==h,'hash mismatch '+n)
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1791072000',FORCE_SOURCE_DATE='1',TZ='UTC')
    with tempfile.TemporaryDirectory(prefix='gtf73-journal-') as t:
        p=Path(t)
        for n in m['files']:
            if n.endswith('.tex'):
                (p/n).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/n,p/n)
        for entry,pdf in [('quantitative.tex','paper.pdf'),('structural.tex','STRUCTURAL_PAPER.pdf')]:
            for _ in range(3):
                r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',entry],cwd=p,env=env,capture_output=True)
                check(r.returncode==0,r.stdout.decode(errors='replace')[-4000:])
            check(signature(p/Path(entry).with_suffix('.pdf'))==m['documents'][pdf]['page_checks'],'rebuild differs '+pdf)
    print(json.dumps({'schema':'gtf73.journal-rebuild/1','status':'success','source_commit':m['source_commit'],
                      'historical_dependencies':False,'independent_proof_certification':False},indent=2))
if __name__=='__main__':main()
