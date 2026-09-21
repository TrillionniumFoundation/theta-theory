#!/usr/bin/env python3
"""Build the exact tracked source and record finite checks, never certify proofs."""
from __future__ import annotations
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER_ROOT = HERE.parents[1]
REPO = HERE.parents[3]
BASELINE = 'b3d0c5ce18a5f6e4491ed70f50a6991ea846dcd8'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(args: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def closure(main: Path) -> list[Path]:
    seen: set[Path] = set()
    def visit(path: Path):
        path = path.resolve()
        if path in seen:
            return
        if not path.is_file():
            raise FileNotFoundError(path)
        seen.add(path)
        for rel in re.findall(r'\\input\{([^}]+)\}', path.read_text()):
            visit(PAPER_ROOT / rel)
    visit(main)
    return sorted(seen)


def build() -> dict:
    evidence = HERE / 'evidence'
    evidence.mkdir(exist_ok=True)
    head = command(['git', 'rev-parse', 'HEAD'])
    sha = head.stdout.strip() if head.returncode == 0 else None
    inputs = closure(HERE / 'paper.tex')
    manifest = {str(p.relative_to(REPO)): digest(p) for p in inputs}
    tracked = sha is not None
    if tracked:
        for path in inputs + [HERE/'checks.py', HERE/'prepare.py', HERE/'build_review.py']:
            rel = str(path.relative_to(REPO))
            got = subprocess.run(['git','show',f'{sha}:{rel}'],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if got.returncode or got.stdout != path.read_bytes():
                raise RuntimeError(f'Build input is not identical to exact source commit: {rel}')
        inherited = [str(p.relative_to(REPO)) for p in inputs if '/v108/' not in str(p)]
        diff = command(['git','diff','--exit-code',BASELINE,sha,'--',*inherited])
        if diff.returncode:
            raise RuntimeError('Inherited mathematical source changed: '+diff.stdout)
    manifest_text = json.dumps(manifest,indent=2,sort_keys=True)+'\n'
    (evidence/'source-manifest.json').write_text(manifest_text)
    checks = []
    for version in ('v108','v107'):
        script = HERE.parent/version/'checks.py'
        if not script.exists():
            if tracked:
                raise FileNotFoundError(script)
            checks.append({'version':version,'status':'not available in partial local checkout'})
            continue
        out = evidence/f'checks-{version}.json'
        proc = command([sys.executable,str(script),'--output',str(out)])
        if proc.returncode:
            (evidence/f'checks-{version}-failure.txt').write_text(proc.stdout)
            raise RuntimeError(proc.stdout)
        result = json.loads(out.read_text())
        checks.append({'version':version, 'status':result['status'], 'check_count':result['check_count'],
                       'script_sha256':digest(script), 'receipt_sha256':digest(out)})
    with tempfile.TemporaryDirectory(prefix='a2-v108-') as temp:
        outdir = Path(temp)
        args = ['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                f'-outdir={outdir}','-jobname=A2-v108','article/v108/paper.tex']
        proc = command(args, PAPER_ROOT)
        (evidence/'build-console.txt').write_text(proc.stdout)
        log_path = outdir/'A2-v108.log'
        log = log_path.read_text(errors='replace') if log_path.exists() else ''
        (evidence/'A2-v108.log').write_text(log)
        diagnostics = [line for line in log.splitlines()
                       if re.search(r'undefined|multiply defined|Label\(s\) may have changed|Overfull \\hbox',line,re.I)]
        pdf_path = outdir/'A2-v108.pdf'
        ok = proc.returncode == 0 and pdf_path.exists() and not diagnostics
        if pdf_path.exists():
            shutil.copyfile(pdf_path,evidence/'A2-v108.pdf')
        info = command(['pdfinfo',str(pdf_path)]) if pdf_path.exists() else None
        pages = re.search(r'^Pages:\s+(\d+)',info.stdout,re.M) if info else None
        receipt = {
            'status':'passed' if ok else 'failed','scope':'native compilation and finite checks, not mathematical certification',
            'source_commit':sha,'source_bound':tracked,'review_commit':BASELINE,
            'run_url':os.environ.get('A2_RUN_URL'),
            'source_manifest_sha256':hashlib.sha256(manifest_text.encode()).hexdigest(),
            'input_count':len(inputs),'inherited_inputs_unchanged':tracked,
            'command':args,'compiler':command(['pdflatex','--version']).stdout.splitlines()[0],
            'latexmk':command(['latexmk','-v']).stdout.strip(),
            'exit_code':proc.returncode,'final_log_diagnostics':diagnostics,
            'checks':checks,'pages':int(pages.group(1)) if pages else None,
            'pdf_sha256':digest(evidence/'A2-v108.pdf') if pdf_path.exists() else None,
            'final_log_sha256':digest(evidence/'A2-v108.log')}
        (evidence/'verification.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        with zipfile.ZipFile(evidence/'source-bundle.zip','w',zipfile.ZIP_DEFLATED) as archive:
            extra=[HERE/'prepare.py',HERE/'checks.py',HERE/'build_review.py',HERE/'README.md',HERE/'RESPONSE_TO_R107.md']
            for path in sorted(set(inputs+extra)):
                if path.exists():
                    archive.write(path,str(path.relative_to(REPO)))
        if not ok:
            raise RuntimeError('Native build or final-log closure failed; inspect evidence/verification.json')
    print(json.dumps(receipt,indent=2))
    return receipt


if __name__ == '__main__':
    build()
