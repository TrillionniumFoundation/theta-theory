#!/usr/bin/env python3
"""Build both review volumes and record source-bound finite diagnostics.

Default mode requires a Git checkout. --allow-partial permits a local source
bundle build but explicitly marks source_bound false; it cannot claim CI success.
"""
from __future__ import annotations
import argparse
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
ARTICLE = HERE.parent
PAPER = HERE.parents[1]
REPO = HERE.parents[3]
REVIEW = '5a8a8190e6a5979719591b286fca92aae3cc15cc'
REFEREE = REPO/'reviews/a2-v108-independent-harsh-top4-2026-09-21/INDEPENDENT_CHECKS.py'
DIAGNOSTICS = re.compile(r'undefined|multiply defined|Label\(s\) may have changed|Overfull \\hbox',re.I)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob_id(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def run(args: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess:
    return subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)


def tex_closure(path: Path) -> list[Path]:
    seen = set()
    def visit(p: Path):
        p = p.resolve()
        if p in seen:
            return
        if not p.is_file():
            raise FileNotFoundError(p)
        seen.add(p)
        for rel in re.findall(r'\\input\{([^}]+)\}',p.read_text()):
            visit(PAPER/rel)
    visit(path)
    return sorted(seen)


def verify(allow_partial: bool = False) -> dict:
    evidence = HERE/'evidence'
    evidence.mkdir(exist_ok=True)
    inputs = sorted(set(tex_closure(HERE/'paper.tex') + tex_closure(ARTICLE/'v108/paper.tex')))
    extra = [HERE/'checks.py',HERE/'verify.py',HERE/'README.md',HERE/'RESPONSE_TO_R108.md',
             HERE/'DEPENDENCIES.md',ARTICLE/'v108/prepare.py',ARTICLE/'v108/checks.py',
             ARTICLE/'v108/build_review.py',ARTICLE/'v107/checks.py',REFEREE,
             ARTICLE/'v108/prepared/preservation.json']
    preservation = json.loads((ARTICLE/'v108/prepared/preservation.json').read_text())
    for name,record in preservation.items():
        old = ARTICLE/record['input']
        prepared = ARTICLE/'v108/prepared'/name
        if sha256(old) != record['input_sha256'] or sha256(prepared) != record['output_sha256']:
            raise RuntimeError(f'Preservation hash mismatch: {name}')
        extra.append(old)
    sources = sorted(set(inputs+extra))
    if not all(p.is_file() for p in sources):
        raise FileNotFoundError('A required source or diagnostic is absent')
    got = run(['git','rev-parse','HEAD'])
    commit = got.stdout.strip() if got.returncode == 0 else None
    if commit is None and not allow_partial:
        raise RuntimeError('A Git checkout is required; use --allow-partial only for explicitly unbound local replay')
    bound = commit is not None
    if bound:
        for p in sources:
            rel = str(p.relative_to(REPO))
            data = subprocess.run(['git','show',f'{commit}:{rel}'],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if data.returncode or data.stdout != p.read_bytes():
                raise RuntimeError('Source differs from exact commit: '+rel)
        inherited = [str(p.relative_to(REPO)) for p in inputs
                     if '/v109/' not in str(p) and '/v108/prepared/' not in str(p)]
        diff = run(['git','diff','--exit-code',REVIEW,commit,'--',*inherited])
        if diff.returncode:
            raise RuntimeError('Inherited mathematical input changed: '+diff.stdout)
    manifest = {str(p.relative_to(REPO)):{'sha256':sha256(p),'git_blob':blob_id(p)} for p in sources}
    manifest_text = json.dumps(manifest,indent=2,sort_keys=True)+'\n'
    (evidence/'source-manifest.json').write_text(manifest_text)
    runs = []
    for version in ('v109','v108','v107'):
        proc = run([sys.executable,str(ARTICLE/version/'checks.py'),'--output',str(evidence/f'checks-{version}.json')])
        (evidence/f'checks-{version}-console.txt').write_text(proc.stdout)
        if proc.returncode:
            raise RuntimeError(proc.stdout)
        result = json.loads((evidence/f'checks-{version}.json').read_text())
        if result['status'] != 'passed':
            raise RuntimeError('Failed diagnostic: '+version)
        runs.append({'version':version,'check_count':result['check_count'],'status':'passed',
                     'script_sha256':sha256(ARTICLE/version/'checks.py')})
    proc = run([sys.executable,str(REFEREE)])
    (evidence/'independent-referee-checks.json').write_text(proc.stdout)
    if proc.returncode:
        raise RuntimeError(proc.stdout)
    independent = json.loads(proc.stdout)
    assert independent['d2_k4'] == {'symmetric_dimension':10,'sampled_rank':9,'nullity':1,'B_in_kernel':True}
    assert independent['d3_k6'] == {'symmetric_dimension':21,'sampled_rank':21,'nullity':0}
    assert independent['three_site_k4'] == {'constraint_rank':3,'native_span_dimension':7,'expected_native_span_dimension':7}
    volumes = []
    for version,jobname in (('v109','A2-v109'),('v108','A2-v109-companion-v108')):
        with tempfile.TemporaryDirectory(prefix=jobname+'-') as tmp:
            args = ['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                    f'-outdir={tmp}',f'-jobname={jobname}',f'article/{version}/paper.tex']
            proc = run(args,PAPER)
            (evidence/f'{jobname}-console.txt').write_text(proc.stdout)
            log_path = Path(tmp)/(jobname+'.log')
            log = log_path.read_text(errors='replace') if log_path.exists() else ''
            (evidence/(jobname+'.log')).write_text(log)
            diagnostics = [line for line in log.splitlines() if DIAGNOSTICS.search(line)]
            pdf = Path(tmp)/(jobname+'.pdf')
            if proc.returncode or not pdf.exists() or diagnostics:
                raise RuntimeError(f'Native build failed for {version}: {diagnostics}; inspect saved log')
            shutil.copyfile(pdf,evidence/pdf.name)
            info = run(['pdfinfo',str(pdf)])
            pages = re.search(r'^Pages:\s+(\d+)',info.stdout,re.M)
            volumes.append({'version':version,'file':pdf.name,'pages':int(pages.group(1)) if pages else None,
                            'pdf_sha256':sha256(pdf),'log_sha256':sha256(evidence/(jobname+'.log')),
                            'final_log_diagnostics':diagnostics,'command':args,'exit_code':proc.returncode})
    receipt = {'status':'passed','scope':'native compilation and finite diagnostics; not proof certification or journal acceptance',
               'source_commit':commit,'source_bound':bound,'review_commit':REVIEW,
               'run_url':os.environ.get('A2_RUN_URL'),'execution':'Git checkout' if bound else 'partial local source bundle',
               'tex_input_count':len(inputs),'source_file_count':len(sources),
               'source_manifest_sha256':hashlib.sha256(manifest_text.encode()).hexdigest(),
               'inherited_inputs_unchanged':True if bound else None,'prepared_hashes_verified':True,
               'checks':runs,'independent_referee_groups':3,'independent_referee_script_git_blob':blob_id(REFEREE),
               'total_diagnostic_groups':sum(x['check_count'] for x in runs)+3,
               'volumes':volumes,'compiler':run(['pdflatex','--version']).stdout.splitlines()[0],
               'latexmk':run(['latexmk','-v']).stdout.strip()}
    name = 'verification.json' if bound else 'local-verification.json'
    (evidence/name).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(evidence/'source-bundle.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for p in sources:
            archive.write(p,str(p.relative_to(REPO)))
        archive.writestr('BUILD_FROM_SOURCE.txt',
            'Run python3 papers/A2-v17-boundary-information-coarsening/article/v109/verify.py --allow-partial\n'
            'A source bundle does not include the Git history; that flag marks source_bound false.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-partial',action='store_true')
    args = parser.parse_args()
    verify(args.allow_partial)
