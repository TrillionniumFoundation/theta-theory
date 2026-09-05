#!/usr/bin/env python3
"""Build the exact local principal source, with shell escape disabled."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    for binary in ('pdflatex','pdfinfo'):
        if not shutil.which(binary):
            raise RuntimeError(f'Required executable not found: {binary}')
    source_files=[ROOT/'main.tex',ROOT/'references.tex',*sorted((ROOT/'sections').glob('*.tex'))]
    inventory={str(p.relative_to(ROOT)):sha256(p) for p in source_files}
    validation=ROOT/'validation'; validation.mkdir(exist_ok=True)
    raw_logs=validation/'build_logs'; raw_logs.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='a1-v4-build-') as temp:
        work=Path(temp)
        for source in source_files:
            destination=work/source.relative_to(ROOT)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,destination)
        command=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','main.tex']
        for run in range(1,4):
            result=subprocess.run(command,cwd=work,capture_output=True,text=True,timeout=120)
            (raw_logs/f'pass-{run}.txt').write_text(result.stdout+result.stderr)
            if result.returncode:
                raise RuntimeError(f'LaTeX pass {run} failed; inspect validation/build_logs.')
        log=(work/'main.log').read_text(errors='replace')
        fatal_patterns=[r'Undefined control sequence',r'There were undefined references',
                        r'Citation .* undefined',r'Reference .* undefined',r'Missing character:',r'Overfull \\[hv]box']
        failures=[pattern for pattern in fatal_patterns if re.search(pattern,log)]
        shutil.copy2(work/'main.log',raw_logs/'main.log')
        if failures:
            raise RuntimeError(f'Strict final-log checks failed: {failures}')
        info=subprocess.run(['pdfinfo',str(work/'main.pdf')],capture_output=True,text=True,check=True).stdout
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        shutil.copy2(work/'main.pdf',ROOT/'A1_REVIEW.pdf')
        shutil.copy2(work/'main.aux',validation/'labels.aux')
    for relative,digest in inventory.items():
        if sha256(ROOT/relative)!=digest:
            raise RuntimeError('A source changed during compilation: '+relative)
    receipt=dict(principal_source_sha256=inventory,pdf='A1_REVIEW.pdf',pdf_pages=pages,
                 pdf_sha256=sha256(ROOT/'A1_REVIEW.pdf'),latex_passes=3,shell_escape=False,
                 command=command,strict_final_log_findings=failures,
                 build_environment=subprocess.run(['pdflatex','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
                 build_script_sha256=sha256(Path(__file__)),
                 visual_inspection='Recorded separately in VISUAL_REVIEW.json; compilation alone is not visual inspection.',
                 mathematical_status='Compilation is not proof verification or referee acceptance.',
                 github_ci_execution=False)
    (validation/'BUILD.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'Compiled and strictly checked {pages} pages; {len(inventory)} source files unchanged.')

if __name__=='__main__': main()
