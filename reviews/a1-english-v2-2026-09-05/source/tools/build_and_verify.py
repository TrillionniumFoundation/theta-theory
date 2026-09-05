#!/usr/bin/env python3
"""Build and verify A1 in isolated directories; never edits mathematical source.

Runs actual finite checks and two independent three-pass LaTeX builds. Page
pixel equality is checked at 100 dpi. This is reproducibility evidence, not
formal mathematical verification. It neither downloads files nor invokes a
shell, and LaTeX shell escape is explicitly disabled.
"""
from __future__ import annotations
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

import fitz

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / 'validation'
SINGLE = 'A1_English_Full_Manuscript_2026-09-05.tex'
STATEMENT = re.compile(r'\\begin\{(theorem|proposition|lemma|corollary)\}(?:\[([^\]]*)\])?(.*?)\\end\{\1\}', re.S)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot() -> dict[str, str]:
    paths = [ROOT/'main.tex', ROOT/'references.tex', ROOT/'README.md', ROOT/'CHANGES.md', ROOT/'requirements.txt']
    paths += sorted((ROOT/'sections').glob('*.tex'))
    paths += sorted((ROOT/'tests').glob('*.py'))
    paths += sorted((ROOT/'tools').glob('*.py'))
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def inline_file(path: Path, stack: tuple[Path, ...] = ()) -> str:
    path = path.resolve()
    if path in stack:
        raise ValueError('Recursive TeX input cycle')
    def replace(m: re.Match) -> str:
        q = ROOT / m.group(1)
        if q.suffix != '.tex': q = q.with_suffix('.tex')
        if not q.resolve().is_relative_to(ROOT):
            raise ValueError('Input outside the package')
        return inline_file(q, stack + (path,)).rstrip('\n')
    return re.sub(r'\\input\{([^}]+)\}', replace, path.read_text())


def run(args: list[str], cwd: Path, logfile: Path, timeout: int = 180) -> str:
    env = os.environ.copy()
    env.update({'SOURCE_DATE_EPOCH': '1788566400', 'FORCE_SOURCE_DATE': '1', 'PYTHONHASHSEED': '0'})
    result = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=timeout, check=False)
    text = result.stdout.decode('utf-8', errors='replace')
    logfile.write_text(text)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}); see {logfile}')
    return text


def build(folder: Path, prefix: str) -> str:
    for i in range(1,4):
        run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape','main.tex'],
            folder, VALID/f'{prefix}_pass_{i}.txt')
    log = (folder/'main.log').read_text(errors='replace')
    fatal = [r'Overfull \\hbox',r'Overfull \\vbox',r'Undefined control sequence',
             r'LaTeX Warning: (?:Reference|Citation).*undefined',r'There were undefined',
             r'Label\(s\) may have changed',r'Missing character:',r'! LaTeX Error',r'Emergency stop']
    found = [x for x in fatal if re.search(x,log)]
    if found:
        raise RuntimeError(f'{prefix} layout/reference errors: {found}')
    return log


def main() -> None:
    start=time.monotonic(); VALID.mkdir(exist_ok=True)
    before=source_snapshot()
    manifest=ROOT/'SOURCE_MANIFEST.json'
    if manifest.exists():
        expected=json.loads(manifest.read_text())['files']
        if expected != before:
            changed=sorted(k for k in set(expected)|set(before) if expected.get(k)!=before.get(k))
            raise RuntimeError(f'Source manifest mismatch: {changed}')
    text=inline_file(ROOT/'main.tex')
    bad=[c for c in text if ord(c)<32 and c not in '\n\t']
    if bad or re.search('[\u3400-\u9fff]',text):
        raise RuntimeError('Unexpected control character or Chinese text in English manuscript')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    if len(labels)!=len(set(labels)): raise RuntimeError('Duplicate labels')
    refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',text)
    if set(refs)-set(labels): raise RuntimeError('Unresolved source labels')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    cites={x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text) for x in group.split(',')}
    if cites-bib: raise RuntimeError('Unresolved source bibliography keys')
    statements=[]
    for f in sorted((ROOT/'sections').glob('*.tex')):
        s=f.read_text()
        for m in STATEMENT.finditer(s):
            lab=re.search(r'\\label\{([^}]+)\}',m.group(3))
            if not lab: raise RuntimeError(f'Unlabeled statement in {f.name}')
            after=s[m.end():]
            if not re.match(r'\s*\\begin\{proof\}',after):
                raise RuntimeError(f'No adjacent proof for {lab.group(1)}')
            statements.append({'label':lab.group(1),'kind':m.group(1),'title':m.group(2) or '',
                'source':str(f.relative_to(ROOT)),'line':s[:m.start()].count('\n')+1})
    proofs=len(re.findall(r'\\begin\{proof\}',text))
    if proofs != len(statements): raise RuntimeError('Statement/proof count mismatch')
    testlog=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],ROOT,VALID/'tests.txt')
    count=re.search(r'Ran (\d+) tests?',testlog)
    if not count or not re.search(r'\nOK\s*$',testlog): raise RuntimeError('Test receipt not successful')
    (ROOT/SINGLE).write_text(text)
    with tempfile.TemporaryDirectory(prefix='a1_english_verify_') as tmp:
        temp=Path(tmp);split=temp/'split';single=temp/'single';split.mkdir();single.mkdir()
        shutil.copy2(ROOT/'main.tex',split/'main.tex');shutil.copy2(ROOT/'references.tex',split/'references.tex')
        shutil.copytree(ROOT/'sections',split/'sections')
        (single/'main.tex').write_text(text)
        splitlog=build(split,'split');singlelog=build(single,'single')
        aux=(split/'main.aux').read_text()
        numbers={k:(num,page) for k,num,page in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux)}
        doc=fitz.open(split/'main.pdf');doc2=fitz.open(single/'main.pdf')
        if len(doc)!=len(doc2):raise RuntimeError('PDF page counts differ')
        page_hashes=[];bound_errors=[]
        for i,(page,other) in enumerate(zip(doc,doc2),1):
            pix=page.get_pixmap(dpi=100,alpha=False);pix2=other.get_pixmap(dpi=100,alpha=False)
            digest=hashlib.sha256(pix.samples).hexdigest()
            if pix.width!=pix2.width or pix.height!=pix2.height or pix.samples!=pix2.samples:
                shutil.copy2(split/'main.pdf', VALID/'diagnostic_split.pdf')
                shutil.copy2(single/'main.pdf', VALID/'diagnostic_single.pdf')
                raise RuntimeError(f'Page {i} differs between split and single source')
            page_hashes.append(digest)
            for block in page.get_text('dict')['blocks']:
                if 'lines' not in block:continue
                for line in block['lines']:
                    for span in line['spans']:
                        box=fitz.Rect(span['bbox'])
                        if box.x0 < -1 or box.y0 < -1 or box.x1 > page.rect.width+1 or box.y1 > page.rect.height+1:
                            bound_errors.append({'page':i,'text':span['text'],'bbox':list(box)})
        if bound_errors:raise RuntimeError(f'PDF content outside page: {bound_errors[:3]}')
        pages=len(doc);pdftext='\n'.join(p.get_text() for p in doc)
        doc.close();doc2.close()
        shutil.copy2(split/'main.pdf',ROOT/'main.pdf')
        shutil.copy2(split/'main.aux',VALID/'compiled_labels.aux')
        shutil.copy2(split/'main.log',VALID/'final_tex.log')
        shutil.copy2(single/'main.pdf',VALID/'single_file.pdf')
    ledger=['# A1 English edition 2.0 — proof ledger','',
        'Numbers and PDF pages below come from the actual final compilation.',
        'Every listed statement has an adjacent written proof. This is a structural audit, not formal proof verification.','',
        '| Number | Statement | Source label | Source location | PDF page |',
        '|---|---|---|---|---:|']
    for s in statements:
        if s['label'] not in numbers:raise RuntimeError('Missing compiled statement label')
        num,page=numbers[s['label']]
        s.update({'number':num,'pdf_page':int(page)})
        title=s['title'].replace('|','/')
        ledger.append(f"| {s['kind'].title()} {num} | {title} | `{s['label']}` | `{s['source']}:{s['line']}` | {page} |")
    (ROOT/'PROOF_LEDGER.md').write_text('\n'.join(ledger)+'\n')
    after=source_snapshot()
    if after!=before:raise RuntimeError('Source changed during verification')
    packages={name:importlib.metadata.version(name) for name in ['numpy','scipy','sympy','PyMuPDF','Pillow']}
    receipt={'edition':'A1 English 2.0','date_utc':datetime.now(timezone.utc).isoformat(),
      'execution':'local actual execution','python':sys.version,'platform':platform.platform(),'packages':packages,
      'test_count':int(count.group(1)),'test_failures':0,'test_errors':0,'test_skips':0,
      'statement_count':len(statements),'proof_count':proofs,'unique_labels':len(labels),
      'bibliography_entries':len(bib),'pdf_pages':pages,'pdf_text_words':len(pdftext.split()),
      'latex_passes':{'split':3,'single_file':3},'shell_escape':False,
      'overfull_boxes':0,'undefined_references_or_citations':0,'missing_characters':0,
      'underfull_box_diagnostics':len(re.findall(r'Underfull \\hbox',splitlog)),
      'split_single_pixel_equal':True,'comparison_dpi':100,'page_pixel_sha256':page_hashes,
      'out_of_page_text_spans':0,'source_hashes_unchanged':True,'source_manifest_verified':manifest.exists(),'source_files_checked':len(before),
      'pdf_sha256':sha(ROOT/'main.pdf'),'single_source_sha256':sha(ROOT/SINGLE),
      'elapsed_seconds':round(time.monotonic()-start,3),
      'limitations':['Finite checks are not theorem proofs.','No proof assistant or external peer review performed.',
                      'Visual inspection is a separate record.','No GitHub write or remote CI was performed.'],
      'statements':statements}
    (VALID/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['test_count','statement_count','proof_count','pdf_pages',
                    'split_single_pixel_equal','overfull_boxes','source_hashes_unchanged','elapsed_seconds']},indent=2))


if __name__=='__main__':
    main()
