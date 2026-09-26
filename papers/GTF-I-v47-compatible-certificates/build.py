"""Source-bound v47 article build; no network access or repository mutation."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
import fitz

HOME = Path(__file__).resolve().parent
EVIDENCE = HOME/'evidence'
BASE = 'd7914880e7df679756c3b6ae86311485ac922f8a'
REVIEW = '6e8a9504a1a0820e6195317df885d99aed06c878'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (EVIDENCE/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def run(command, cwd=HOME):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError('Failed: '+repr(command)+'\n'+result.stdout+'\n'+result.stderr)
    return result.stdout


def make_zip(dest, files, prefix=''):
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for file in files:
            z.write(file, prefix+file.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--core-only', action='store_true')
    args = ap.parse_args()
    EVIDENCE.mkdir(exist_ok=True)
    manifest = json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    for name, expected in manifest['unchanged_sources'].items():
        if sha(HOME/name) != expected:
            raise RuntimeError('Inherited source changed: '+name)
    results = {}
    for name, filename in [('v47','check_compatibility.py'), ('v44','verify_inherited.py')]:
        ordinary = json.loads(run([sys.executable, filename]))
        optimized = json.loads(run([sys.executable, '-O', filename]))
        if ordinary != optimized:
            raise RuntimeError('Optimization-mode disagreement: '+name)
        results[name] = ordinary
        save(name.upper()+'_CHECKS.json', ordinary)
    logs = []
    for _ in range(3):
        logs.append(run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex']))
    log = (HOME/'main.log').read_text(errors='replace')
    (EVIDENCE/'LATEX_LOG.txt').write_text(log)
    issues = {
        'undefined_references': bool(re.search(r'(Reference|Citation).*undefined|There were undefined', log)),
        'overfull_boxes': 'Overfull \\hbox' in log or 'Overfull \\vbox' in log,
        'malformed_bookmarks': 'Token not allowed in a PDF string' in log,
    }
    if any(issues.values()):
        raise RuntimeError('LaTeX qualification failed: '+str(issues))
    shutil.copy2(HOME/'main.pdf', HOME/'paper.pdf')
    doc = fitz.open(HOME/'paper.pdf')
    if not len(doc) or any(not p.get_text().strip() for p in doc):
        raise RuntimeError('Empty manuscript page')
    for i, page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1,1), alpha=False).save(EVIDENCE/f'page-{i+1}.png')
    aux = (HOME/'main.aux').read_text()
    labels = {name:{'number':number,'page':page} for name,number,page in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}', aux)}
    save('THEOREM_LOCATIONS.json', labels)
    sources = sorted(p for p in HOME.iterdir() if p.suffix in {'.tex','.py','.md','.json'} and p.is_file())
    hashes = {p.name:sha(p) for p in sources}
    save('SOURCE_HASHES.json', hashes)
    make_zip(EVIDENCE/'CORE_SOURCES.zip', sources, HOME.name+'/')
    archives = {}
    if not args.core_only:
        old = Path(os.getenv('GTF_V44_INPUT', str(HOME.parent/'GTF-I-v44-hankel-resonance')))
        expected = {
            'paper.pdf':'8bfacc80ff9b58177137d465fa86c10028be1b903504f6087dd5e85efa3238b1',
            'complete-manuscript.pdf':'469dbb4845b859d240c6d913d1c2ab0278d41c401f35100a7132652de1ccd641',
            'complete-development.pdf':'4afaf696c23016d5f958c6af6f8623a4c9ca3bdca2ca2692ef7d823a69016fab'
        }
        for name, digest in expected.items():
            if sha(old/name) != digest:
                raise RuntimeError('Published archive mismatch: '+name)
        shutil.copy2(old/'paper.pdf', HOME/'supporting-v44.pdf')
        for name in ['complete-manuscript.pdf','complete-development.pdf']:
            combined = fitz.open()
            combined.insert_pdf(doc)
            divider = combined.new_page(width=612, height=792)
            divider.insert_text((72,100), 'Preserved v44 published archive', fontsize=18)
            divider.insert_text((72,132), 'The following predecessor pages are unchanged archival material.', fontsize=10)
            older = fitz.open(old/name)
            offset = len(combined)
            combined.insert_pdf(older)
            dest = HOME/name
            if dest.exists():
                dest.unlink()
            combined.save(dest, garbage=3, deflate=True)
            combined.close()
            check = fitz.open(dest)
            for i in range(len(older)):
                if older[i].get_text() != check[offset+i].get_text():
                    raise RuntimeError('Archive text changed')
            indices = sorted(set([0, len(older)//2, len(older)-1]))
            for i in indices:
                if older[i].get_pixmap().samples != check[offset+i].get_pixmap().samples:
                    raise RuntimeError('Archive raster changed')
            archives[name] = {'pages':len(check),'predecessor_pages':len(older),
                              'predecessor_sha256':expected[name], 'sha256':sha(dest),
                              'text_pages_compared':len(older),'raster_pages_compared':len(indices)}
            older.close(); check.close()
    source_commit = os.getenv('GTF_SOURCE_COMMIT', 'local-uncommitted-build')
    receipt = {'schema':'gtf47.build/1','source_commit':source_commit,
               'base_commit':BASE,'review_commit':REVIEW,
               'workflow_run':os.getenv('GITHUB_RUN_ID'), 'core_only':args.core_only,
               'article_pages':len(doc),'article_sha256':sha(HOME/'paper.pdf'),
               'unchanged_sources_verified':len(manifest['unchanged_sources']),
               'normal_optimized_agreement':True,
               'negative_control_executions':2*len(results['v47']['negative_controls_detected']),
               'regressions':results,'complete_volumes':archives,
               'core_archive_sha256':sha(EVIDENCE/'CORE_SOURCES.zip'),
               **issues,
               'scope':'Executed finite rational checks and source-bound typesetting/preservation; not independent proof, priority, or generic global optimization certification.'}
    save('BUILD_RECEIPT.json', receipt)
    make_zip(EVIDENCE/'REFEREE_PACKAGE.zip', [HOME/'paper.pdf', HOME/'RESPONSE_TO_REFEREE.md',
             HOME/'LITERATURE_AUDIT.md', EVIDENCE/'CORE_SOURCES.zip', EVIDENCE/'BUILD_RECEIPT.json'])
    if not args.core_only:
        root = HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V47_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 47\n\n'
            '**Robust Compatibility of Numerical Word Realizations**\n\n'
            f'Native source: `{source_commit}`. Controlling r29: `{REVIEW}`.\n\n'
            f'[Article ({len(doc)} pages)](papers/{HOME.name}/paper.pdf) · '
            f'[Native LaTeX](papers/{HOME.name}/main.tex) · '
            f'[Response](papers/{HOME.name}/RESPONSE_TO_REFEREE.md)\n\n'
            f'[Compact review package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip) · '
            f'[Standalone sources](papers/{HOME.name}/evidence/CORE_SOURCES.zip) · '
            f'[Executed receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json)\n\n'
            'Exact two-label antisymmetric normal form, balanced sign certificates, robust two-bottleneck obstruction, and complete finite error frontiers in the stated profile classes. '
            'All v46 mathematical modules are retained. No new arithmetic growth exponent, general higher-width classification or independent analytic pipeline closure is claimed.\n\n'
            'The latest actual review remains r29 of v43. v44/v46 antecedents are explicitly attributed. '
            'The old v46 failed workflow is not relabelled as a successful build. Older paths and branches are unchanged.\n')
    doc.close()
    for suffix in ['.aux','.log','.out','.pdf']:
        (HOME/('main'+suffix)).unlink(missing_ok=True)
    shutil.rmtree(HOME/'__pycache__', ignore_errors=True)
    print(json.dumps({'status':'success','pages':receipt['article_pages'], 'source_commit':source_commit,
                      'core_only':args.core_only, 'negative_controls':receipt['negative_control_executions']}))


if __name__ == '__main__':
    main()
