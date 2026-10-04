#!/usr/bin/env python3
"""Rebuild the standalone v79 focused submission without repository dependencies."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import fitz
R = Path(__file__).resolve().parent

def sha(data): return hashlib.sha256(data).hexdigest()
def require(ok, message):
    if not ok: raise RuntimeError(message)

def signature(path):
    out = []
    with fitz.open(path) as doc:
        for p in doc:
            text = p.get_text(sort=True)
            pix = p.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            out.append({'page': p.number+1, 'text_sha256': sha(text.encode()),
                        'raster_sha256': sha(pix.samples), 'width': pix.width,
                        'height': pix.height, 'characters': len(text)})
    return out

def main():
    m = json.loads((R/'JOURNAL_MANIFEST.json').read_text())
    require(m['schema'] == 'gtf79.journal/1' and not m['repository_dependencies']
            and not m['historical_PDF_dependencies'], 'wrong standalone manifest')
    for n, digest in m['files'].items():
        p = Path(n)
        require(not p.is_absolute() and '..' not in p.parts, 'unsafe manifest path')
        require(sha((R/n).read_bytes()) == digest, 'submitted file changed: '+n)
    require(signature(R/'paper.pdf') == m['document']['page_checks'], 'submitted PDF differs')
    env = os.environ.copy(); env.update(SOURCE_DATE_EPOCH='1791072000', FORCE_SOURCE_DATE='1', TZ='UTC')
    with tempfile.TemporaryDirectory(prefix='gtf79-journal-readonly-') as t:
        dest = Path(t)
        for n in m['files']:
            if n.endswith('.tex'):
                (dest/n).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(R/n, dest/n)
        for _ in range(3):
            run = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                                  '-file-line-error', 'quantitative.tex'], cwd=dest, env=env,
                                 capture_output=True, timeout=180)
            require(run.returncode == 0, run.stdout.decode(errors='replace')[-5000:])
        log = (dest/'quantitative.log').read_text(errors='replace')
        require(not any(s in log for s in ['There were undefined references', 'There were undefined citations',
                    'multiply defined', 'Undefined control sequence', 'Rerun to get cross-references right']),
                'unresolved typesetting reference')
        require(not re.findall(r'(?:Overfull|Underfull) \\[^\n]+', log), 'unresolved typesetting box')
        require(signature(dest/'quantitative.pdf') == m['document']['page_checks'], 'journal rebuild differs')
    for n, h in m['files'].items(): require(sha((R/n).read_bytes()) == h, 'verifier modified input')
    print(json.dumps({'schema': 'gtf79.journal-rebuild/1', 'status': 'success',
                      'source_commit': m['source_commit'], 'pages': m['document']['pages'],
                      'read_only': True, 'independent_proof_certification': False}, indent=2, sort_keys=True))

if __name__ == '__main__': main()
