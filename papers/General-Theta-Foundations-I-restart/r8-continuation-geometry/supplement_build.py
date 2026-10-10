#!/usr/bin/env python3
"""Attach the source-controlled submission cover to the unchanged technical PDF."""
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from pypdf import PdfReader, PdfWriter
from verify import ROOT, require, sha256, git_hash

def command(args, cwd=None, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    require(result.returncode == 0, 'supplement command failed: '+result.stdout[-10000:])
    return result.stdout

def cover_and_attach(raw_pdf, output_pdf):
    raw_pdf, output_pdf = Path(raw_pdf), Path(output_pdf)
    original = raw_pdf.read_bytes()
    retained = PdfReader(io.BytesIO(original))
    template = (ROOT/'supplement_cover.tex.in').read_bytes()
    env = os.environ.copy()
    env.update(SOURCE_DATE_EPOCH='1791331200', FORCE_SOURCE_DATE='1', TZ='UTC', LC_ALL='C.UTF-8')
    products=[]
    for _ in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-supplement-cover-') as tmp:
            p=Path(tmp); (p/'cover.tex').write_bytes(template)
            for _pass in range(3):
                command(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','cover.tex'],cwd=p,env=env)
            log=(p/'cover.log').read_text(errors='replace')
            for forbidden in ('Overfull \\hbox','Overfull \\vbox','There were undefined references'):
                require(forbidden not in log,'supplement cover: '+forbidden)
            cover=PdfReader(str(p/'cover.pdf')); require(len(cover.pages)==1,'cover must have one page')
            writer=PdfWriter()
            writer.append(cover, import_outline=False)
            writer.append(PdfReader(io.BytesIO(original)), import_outline=False)
            writer.add_metadata({'/Title':'Supplement S to General Theta Foundations I', '/Author':'Qian Qi'})
            data=io.BytesIO(); writer.write(data); data=data.getvalue()
            merged=PdfReader(io.BytesIO(data))
            require(len(merged.pages)==len(retained.pages)+1,'supplement page loss')
            for old,new in zip(retained.pages,list(merged.pages)[1:]):
                require(old.extract_text()==new.extract_text(),'technical page text changed during attachment')
            products.append(data)
    require(products[0]==products[1],'supplement attachment not byte reproducible')
    require(raw_pdf.read_bytes()==original,'raw technical PDF mutated')
    output_pdf.write_bytes(products[0])
    return {'status':'PASS', 'cover_source_sha256':sha256(template), 'cover_isolated_builds':2,
            'passes_per_cover':3, 'merged_byte_identical':True, 'raw_text_unchanged':True,
            'raw_pdf_sha256':sha256(original), 'pdf_sha256':sha256(products[0]),
            'pdf_git_blob_sha':git_hash('blob',products[0]), 'pdf_pages':len(retained.pages)+1,
            'formal_status':'Supplement S, integral part of this submission, not an external publication'}
