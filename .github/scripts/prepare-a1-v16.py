#!/usr/bin/env python3
"""Materialize the complete v16 revision from the immutable v15 source.

All replacement text is committed beside this script. The new paper is
materialized before validation/publication; the payload is not the deliverable.
No network access, hidden token, or external source is used by this script.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

BASIS = 'e1d0ff2ef04a8641ac77923b664c4d3e8386f212'
REVIEW = 'd89bc35dc5d50240c8ae3c82aa251437dcc2165a'
MANIFEST_BLOB = 'deae18f5a30c8ceb9b7a801584a8c94f672c7f14'
PAYLOAD_SHA256 = 'cac6c3bb3e51a87b66ac3556b35416a2ec8e4fb4ac10f288c4673b891e59904e'
OLD_BASIS = 'ffb9214b0fc7e218d6183c1f81bccb3e47587421'
OLD_REVIEW = '3d58bb33ae122ebb2430874e2a57a5863e6a876a'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError('Expected exactly one source anchor: '+old[:90])
    return text.replace(old, new, 1)


def copy_source(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(
        'build', 'validation', '__pycache__', '*.pyc', '*.aux', '*.log',
        '*.out', '*.pdf', '*.synctex.gz'))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--payload', type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    baseline = args.baseline or repo/'papers/A1-english-v15'
    destination = args.destination or repo/'papers/A1-english-v16'
    payload = args.payload or Path(__file__).with_name('a1-v16-inputs.json.xz.b64')
    raw_manifest = (baseline/'SOURCE_MANIFEST.json').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(raw_manifest)).encode()+b'\0'+raw_manifest).hexdigest()
    if blob != MANIFEST_BLOB:
        raise ValueError('The v15 source manifest is not the pinned submission manifest')
    old_manifest = json.loads(raw_manifest)
    for name, digest in old_manifest['files'].items():
        if sha((baseline/name).read_bytes()) != digest:
            raise ValueError('Pinned v15 source mismatch: '+name)
    compressed = base64.b64decode(payload.read_text(), validate=False)
    if sha(compressed) != PAYLOAD_SHA256:
        raise ValueError('Committed revision input digest mismatch')
    inputs = json.loads(lzma.decompress(compressed))
    expected_names = {'abstract.tex','opening.tex','structural_comparison.tex',
        'circular_context.tex','references-v16.tex','README.md','RESPONSE_TO_REFEREE.md',
        'PROOF_LEDGER.md','HISTORICAL_DERIVATION_MAP.md','LITERATURE_VERIFICATION.md',
        'NUMERICAL_EVIDENCE.md','VISUAL_INSPECTION.md'}
    if set(inputs) != expected_names or not all(isinstance(v,str) for v in inputs.values()):
        raise ValueError('Unexpected revision input names or types')
    if destination.exists():
        raise FileExistsError('Refusing to overwrite an existing revision: '+str(destination))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='a1-v15-proof-baseline-') as tmp:
        copied = Path(tmp)/'source'
        copy_source(baseline, copied)
        subprocess.run([sys.executable,str(copied/'build.py'),'--prepare-only'],
                       cwd=copied, check=True, capture_output=True, text=True)
        expanded = (copied/'build/expanded.tex').read_text()
    proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',expanded,re.S)
    statements = [m.group() for m in re.finditer(
        r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}',expanded,re.S)]
    if len(proofs) != 84 or len(statements) != 87:
        raise ValueError('Unexpected baseline proof/statement count')
    copy_source(baseline, destination)
    archive = ['main.tex','references.tex','sections/introduction.tex','sections/circular.tex',
        'README.md','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','HISTORICAL_DERIVATION_MAP.md',
        'LITERATURE_VERIFICATION.md','NUMERICAL_EVIDENCE.md','VISUAL_INSPECTION.md',
        'SOURCE_MANIFEST.json','BUILD_REPORT.json','PRESERVATION_REPORT.json',
        'build.py','validate.py','manifest.py']
    for name in archive:
        path = baseline/name
        if path.exists():
            shutil.copy2(path,destination/'history'/('V15_'+path.name))
    previous_receipt = baseline/'validation/EXECUTION_REPORT.json'
    if previous_receipt.is_file():
        shutil.copy2(previous_receipt,destination/'history/V15_EXECUTION_REPORT.json')
    preservation = {'version':15,'submission_commit':BASIS,
        'source_manifest_blob':MANIFEST_BLOB,
        'expanded_source_sha256':sha(expanded.encode()),
        'proof_sha256':[sha(p.encode()) for p in proofs],
        'statement_sha256':[sha(s.encode()) for s in statements],
        'named_results':re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',expanded),
        'scope':'Bytewise preservation of complete statements and proofs, not formal verification.'}
    (destination/'V15_PRESERVATION_MANIFEST.json').write_text(json.dumps(preservation,indent=2)+'\n')
    for name,text in inputs.items():
        if name.endswith('.md') or name == 'references-v16.tex':
            (destination/name).write_text(text)
    main_tex = (destination/'main.tex').read_text()
    main_tex = replace_once(main_tex,'\\date{September 6, 2026}','\\date{September 7, 2026}')
    abstract = re.search(r'\\begin\{abstract\}\n(.*?)\\end\{abstract\}',main_tex,re.S)
    if abstract is None:
        raise ValueError('Missing abstract')
    main_tex = main_tex[:abstract.start(1)]+inputs['abstract.tex']+main_tex[abstract.end(1):]
    (destination/'main.tex').write_text(main_tex)
    intro = (destination/'sections/introduction.tex').read_text()
    first = intro.index('\\subsection{The experiment and its resolution profile}')
    intro = '\\section{Introduction}\n'+inputs['opening.tex']+'\n'+intro[first:]
    intro = replace_once(intro,'\\subsection{Unresolved prior information}',
        '\\input{sections/structural_comparison}\n\n\\subsection{Unresolved prior information}')
    intro = replace_once(intro,'One causal $M$-label filter attains the maximum over checkpoints.',
        'With the contrast known to a read-only program, one causal $M$-label\n'
        'filter attains the maximum over checkpoints. Its constants and\n'
        'contrast interval are chosen for this fixed $N$, not uniformly in\n'
        'unbounded horizon.')
    (destination/'sections/introduction.tex').write_text(intro)
    (destination/'sections/structural_comparison.tex').write_text(inputs['structural_comparison.tex'])
    circle = (destination/'sections/circular.tex').read_text()
    circle = replace_once(circle,'\\subsection{Acquisition: a symmetric-polynomial submersion}',
        '\\input{sections/circular_context}\n\n\\subsection{Acquisition: a symmetric-polynomial submersion}')
    (destination/'sections/circular.tex').write_text(circle)
    (destination/'sections/circular_context.tex').write_text(inputs['circular_context.tex'])
    references = (destination/'references.tex').read_text()
    references = replace_once(references,'\\VnineEndBibliography}',
                              '\\input{references-v16}\n\\VnineEndBibliography}')
    (destination/'references.tex').write_text(references)
    build = (destination/'build.py').read_text()
    anchor = "    refs=set(re.findall(r'\\\\(?:eq)?ref\\{([^}]+)\\}',expanded))"
    addition = '''    v15_manifest=json.loads((ROOT/'V15_PRESERVATION_MANIFEST.json').read_text())
    v15=Counter(v15_manifest['proof_sha256'])
    v15_statements=Counter(v15_manifest['statement_sha256'])
    if v15-current:raise ValueError('A complete v15 proof was changed or removed')
    if v15_statements-statements:raise ValueError('A complete v15 statement was changed or removed')
    if set(v15_manifest['named_results'])-set(labels):
        raise ValueError('A v15 named result is absent')
'''
    build = replace_once(build,anchor,addition+anchor)
    build = replace_once(build,"    (ROOT/'PRESERVATION_REPORT.json').write_text",
        "    report.update(retained_v15_proofs_byte_identical=sum(v15.values()),\n"
        "                  retained_v15_statements_byte_identical=sum(v15_statements.values()),\n"
        "                  retained_v15_named_results=len(v15_manifest['named_results']))\n"
        "    (ROOT/'PRESERVATION_REPORT.json').write_text")
    (destination/'build.py').write_text(build)
    for name in ['manifest.py','validate.py']:
        text = (destination/name).read_text().replace("'version': 15","'version': 16")
        text = text.replace(OLD_REVIEW,REVIEW).replace(OLD_BASIS,BASIS)
        if name == 'validate.py':
            start = text.index('"""'); stop = text.index('"""',start+3)+3
            text = text[:start]+'''"""Execute all six inherited author suites and the complete v16 build.

The optional pinned v15 referee diagnostic is a regression execution,
not a fresh independent review. No previous execution receipt is reused.
"""'''+text[stop:]
            text = text.replace("history/V14_SOURCE_MANIFEST.json","history/V15_SOURCE_MANIFEST.json")
            text = text.replace('range(10,15)','range(10,16)')
            text = text.replace("report['new_author_diagnostic_total'] = EXPECTED[15]",
                                "report['new_author_diagnostic_total'] = 0")
            a = text.index('    if args.prior_review:')
            b = text.index("    report['build_seconds']",a)
            text = text[:a]+'''    if args.prior_review:
        repo = ROOT.parents[1]
        script = repo/'reviews/a1-english-v15-positive-history-2026-09-07/reproduce_review.py'
        expected_sha = '7b406a8a4bd16e61a0c5017232b20d0a9126d9d63150c343e84b7da8e3f4f22d'
        if not script.is_file() or digest(script) != expected_sha:
            raise ValueError('The original pinned v15 referee diagnostic is unavailable or changed')
        target = out/'PRIOR_REVIEW_RERUN.json'
        elapsed = run([sys.executable,str(script),'--output',str(target)],out/'prior-review-stdout.txt')
        data = json.loads(target.read_text())
        if data['assertions'] != 1800 or data.get('status') != 'PASS':
            raise ValueError('Unexpected original v15 referee diagnostic outcome')
        report['prior_review_probe'] = {'source_version':15,'assertions':1800,
            'passed':True,'seconds':elapsed,'source_sha256':digest(script),
            'result_sha256':digest(target),
            'scope':'Regression execution of the pinned v15 referee diagnostic; not a new independent review of v16.'}
'''+text[b:]
        (destination/name).write_text(text)
    for stale in ['BUILD_REPORT.json','PRESERVATION_REPORT.json','SOURCE_MANIFEST.json']:
        (destination/stale).unlink(missing_ok=True)
    (destination/'MATERIALIZATION.json').write_text(json.dumps({
        'version':16,'submission_basis':BASIS,'controlling_review':REVIEW,
        'baseline_source_manifest_blob':MANIFEST_BLOB,
        'baseline_source_entries_verified':len(old_manifest['files']),
        'revision_inputs_sha256':PAYLOAD_SHA256,
        'retained_complete_proofs':len(proofs),'retained_complete_statements':len(statements)
    },indent=2)+'\n')
    subprocess.run([sys.executable,str(destination/'manifest.py'),'--write'],
                   cwd=destination,check=True)
    subprocess.run([sys.executable,str(destination/'build.py'),'--prepare-only'],
                   cwd=destination,check=True)
    print('Complete revision materialized:',destination)


if __name__ == '__main__':
    main()
