#!/usr/bin/env python3
"""Verify and rebuild the v78 focused journal package outside a repository.

Requires pdflatex and PyMuPDF. No historical PDF, research archive, Git history,
code regression or repository-relative input is needed. Submitted files are
read-only; compilation occurs in a fresh temporary directory.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import fitz

R=Path(__file__).resolve().parent
DOCUMENTS={'quantitative.tex':'paper.pdf','structural.tex':'STRUCTURAL_PAPER.pdf'}
EXTRAS={'paper.pdf','STRUCTURAL_PAPER.pdf','RESPONSE_TO_REFEREE.md',
        'journal_verify.py','LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md'}


def sha(data):return hashlib.sha256(data).hexdigest()


def check(ok,message):
    if not ok:raise RuntimeError(message)


def path(name):
    p=Path(name)
    check(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,
          'unsafe or noncanonical package path '+name)
    return R/p


def graph(entry,seen=None):
    seen=set() if seen is None else seen
    entry=str(Path(entry).with_suffix('.tex'))
    check(entry not in seen,'recursive or duplicate input '+entry)
    seen.add(entry)
    source=path(entry).read_text()
    for name in re.findall(r'\\input\{([^}]+)\}',source):graph(name,seen)
    return seen


def signature(pdf):
    out=[]
    with fitz.open(pdf) as document:
        for page in document:
            pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
            text=page.get_text(sort=True)
            out.append({'page':page.number+1,'text_sha256':sha(text.encode()),
                        'raster_sha256':sha(pix.samples),'width':pix.width,
                        'height':pix.height,'characters':len(text)})
    return out


def main():
    manifest=json.loads((R/'JOURNAL_MANIFEST.json').read_text())
    check(manifest['schema']=='gtf78.journal/1','v78 journal manifest required')
    check(re.fullmatch(r'[0-9a-f]{40}',manifest['source_commit']) is not None,
          'full source commit is missing')
    check(manifest['historical_PDF_dependencies'] is False
          and manifest['repository_dependencies'] is False,'standalone dependency scope differs')
    needed=set(EXTRAS)
    for entry in DOCUMENTS:needed.update(graph(entry))
    check(set(manifest['files'])==needed,'journal package contains an unexpected source inventory')
    for name,digest in manifest['files'].items():
        check(sha(path(name).read_bytes())==digest,'hash mismatch '+name)
    check(set(manifest['documents'])==set(DOCUMENTS.values()),'unexpected journal document set')
    for pdf,info in manifest['documents'].items():
        check(sha(path(pdf).read_bytes())==info['sha256'],'submitted PDF digest mismatch '+pdf)
        check(signature(path(pdf))==info['page_checks'] and len(info['page_checks'])==info['pages'],
              'submitted PDF page signature mismatch '+pdf)
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1791072000',FORCE_SOURCE_DATE='1',TZ='UTC')
    with tempfile.TemporaryDirectory(prefix='gtf78-journal-') as temporary:
        target=Path(temporary)
        for name in manifest['files']:
            if name.endswith('.tex'):
                (target/name).parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(path(name),target/name)
        for entry,pdf in DOCUMENTS.items():
            for _ in range(3):
                run=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                                    '-file-line-error',entry],cwd=target,env=env,
                                   capture_output=True,timeout=180)
                check(run.returncode==0,run.stdout.decode(errors='replace')[-4000:])
            log=(target/Path(entry).with_suffix('.log')).read_text(errors='replace')
            forbidden=['There were undefined references','There were undefined citations',
                       'multiply defined','Undefined control sequence',
                       'Rerun to get cross-references right']
            check(not any(text in log for text in forbidden),'unresolved LaTeX reference/citation '+entry)
            check(not re.findall(r'(?:Overfull|Underfull) \\[^\n]+',log),
                  'unresolved typesetting boxes '+entry)
            check(signature(target/Path(entry).with_suffix('.pdf'))==manifest['documents'][pdf]['page_checks'],
                  'standalone rebuild differs '+pdf)
    for name,digest in manifest['files'].items():
        check(sha(path(name).read_bytes())==digest,'verifier modified submitted file '+name)
    print(json.dumps({'schema':'gtf78.journal-rebuild/1','status':'success',
          'source_commit':manifest['source_commit'],
          'documents':{name:{'pages':info['pages'],'sha256':info['sha256']}
                       for name,info in manifest['documents'].items()},
          'historical_dependencies':False,'repository_dependencies':False,
          'read_only':True,'native_rebuild_text_and_rasters_match':True,
          'independent_proof_certification':False},indent=2,sort_keys=True))


if __name__=='__main__':main()
