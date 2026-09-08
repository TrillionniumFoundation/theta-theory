#!/usr/bin/env python3
"""Compile changed TeX modules only. External labels use explicit test stubs.

This is NOT the complete native two-volume build or reference validation.
Run from a complete revision checkout or from the preparation directory.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import tempfile


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    compiler = shutil.which('pdflatex')
    if compiler is None:
        raise RuntimeError('pdflatex is required')
    rels = ('v34/introduction.tex','v34/moment_controllers.tex','v34/comparison.tex',
            'v34/references_main.tex')
    chunks = [(root/p).read_text() for p in rels]
    chunks[0] = chunks[0].replace(r'\input{text/main_classification}',
        r'\paragraph{External main theorem.} The native build inputs the unchanged collision theorem here.')
    contents = '\n'.join(chunks)
    labels = re.findall(r'\\label\{([^}]+)\}',contents)
    if len(labels) != len(set(labels)):
        raise RuntimeError('duplicate labels in changed modules')
    refs = set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',contents))
    external = sorted(refs-set(labels))
    mocks = '\n'.join(r'\expandafter\def\csname r@'+s+r'\endcsname{{X}{0}{}{}{}}' for s in external)
    preamble = (root/'preamble.tex').read_text()
    abstract = (root/'main.tex').read_text().split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    tex = preamble + '\n' + mocks + r'''
\title{A1 v34: changed-module layout check}
\author{Preparation test, not the complete manuscript}
\begin{document}
\begin{abstract}'''+abstract+r'''\end{abstract}
\maketitle
'''+contents+'\n\\end{document}\n'
    out = root/'v34'/'smoke-output'
    out.mkdir(exist_ok=True)
    (out/'smoke.tex').write_text(tex)
    for cycle in range(3):
        result=subprocess.run([compiler,'-no-shell-escape','-interaction=nonstopmode',
                '-halt-on-error','smoke.tex'],cwd=out,capture_output=True,text=True)
        (out/f'pass-{cycle+1}.log').write_text(result.stdout+result.stderr)
        if result.returncode:
            raise RuntimeError(f'compilation failed at pass {cycle+1}')
    log=(out/'smoke.log').read_text()
    failures=[x for x in ('undefined references','undefined citations','multiply defined',
                         'Label(s) may have changed') if x in log]
    warnings=[x for x in log.splitlines() if 'Overfull \\hbox' in x or 'Overfull \\vbox' in x]
    if failures or warnings:
        raise RuntimeError(f'smoke failures={failures}; layout={warnings}')
    receipt={'scope':'Changed modules and abstract only; native main theorem replaced by a test marker; external labels mocked.',
        'complete_native_build':False,'complete_native_references_checked':False,
        'external_test_stub_labels':external,'tex_passes':3,
        'overfull_boxes':warnings,'pdf_sha256':hashlib.sha256((out/'smoke.pdf').read_bytes()).hexdigest(),
        'source_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in rels},
        'status':'CHANGED_MODULE_SMOKE_PASS'}
    (root/'v34'/'SMOKE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
