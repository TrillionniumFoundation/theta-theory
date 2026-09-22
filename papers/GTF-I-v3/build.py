#!/usr/bin/env python3
"""Build exact v3 inputs; retain v2/v1 sources and fail on unresolved TeX output."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent/'GTF-I-v2'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(args: list[str], cwd: Path, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    for executable in ['pdflatex','pdfinfo']:
        require(shutil.which(executable) is not None, 'Missing executable: '+executable)
    evidence = ROOT/'evidence'
    evidence.mkdir(exist_ok=True)
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    marker = b'\\section{Acquired geometry and nonuniform causal resolution}'
    original = (OLD/'revision.tex').read_bytes()
    reference_base = (OLD/'legacy/references.tex').read_text()
    references = reference_base.replace('\\end{thebibliography}',
        (OLD/'new_references.tex').read_text()+'\n'+(ROOT/'new-references.tex').read_text()+'\n\\end{thebibliography}')
    derived = {'retained-results.tex':original[original.index(marker):],
               'references.tex':references.encode()}
    for name, data in derived.items():
        target = ROOT/name
        require(hashlib.sha256(data).hexdigest() == manifest['derived_source_sha256'][name],
                'Derived source hash mismatch: '+name)
        if target.exists():
            require(target.read_bytes() == data, 'Edited generated source: '+name)
        else:
            target.write_bytes(data)
    for name, digest in manifest['new_source_sha256'].items():
        require(sha(ROOT/name) == digest, 'Changed v3 source: '+name)
    old_manifest = json.loads((OLD/'SOURCE_MANIFEST.json').read_text())
    for name, digest in old_manifest['compiled_and_executable_inputs'].items():
        require(sha(OLD/name) == digest, 'Changed inherited v2 input: '+name)
    require(sha(OLD/'SOURCE_MANIFEST.json') == manifest['v2_manifest_sha256'], 'Changed inherited v2 manifest')
    for name, digest in manifest['inherited_input_sha256'].items():
        require(sha(OLD/name) == digest, 'Changed inherited input: '+name)
    tree_checks = {}
    if os.environ.get('GITHUB_SHA'):
        for name, expected in old_manifest['preserved_trees'].items():
            run = call(['git','rev-parse',os.environ['GITHUB_SHA']+':papers/GTF-I-v2/'+name],ROOT)
            require(run.returncode == 0 and run.stdout.strip() == expected, 'Inherited Git tree changed: '+name)
            tree_checks[name] = expected
    outputs = []
    for flags, name in [([], 'DIAGNOSTICS.json'), (['-O'], 'DIAGNOSTICS_OPTIMIZED.json')]:
        run = call([sys.executable,*flags,str(ROOT/'verify.py')],ROOT)
        (evidence/name).write_text(run.stdout)
        require(run.returncode == 0, 'Diagnostic failure: '+name)
        outputs.append(run.stdout)
    require(outputs[0] == outputs[1], 'Optimized diagnostic output differs')
    negatives = {}
    for mutant in ['erase-critical-log','omit-cross-covariance']:
        run = call([sys.executable,str(ROOT/'verify.py'),'--mutant',mutant],ROOT)
        (evidence/('MUTANT_'+mutant+'.txt')).write_text(run.stdout)
        require(run.returncode != 0, 'Negative control survived: '+mutant)
        negatives[mutant] = {'rejected':True,'exit_code':run.returncode}
    for script, name in [(OLD/'verify.py','V2_DIAGNOSTICS.json'),
                         (OLD/'legacy/tools/verify.py','V1_DIAGNOSTICS.json')]:
        run = call([sys.executable,str(script)],script.parent)
        (evidence/name).write_text(run.stdout)
        require(run.returncode == 0, 'Inherited diagnostic failure: '+name)
    own_tex = [ROOT/n for n in ['main.tex','introduction.tex','regenerative.tex','calibration.tex','retained-results.tex','references.tex']]
    inherited_tex = [OLD/'legacy/preamble.tex'] + sorted((OLD/'legacy/sections').glob('*.tex'))
    inherited_tex = [p for p in inherited_tex if p.name != '01_introduction.tex']
    combined = '\n'.join(p.read_text() for p in own_tex[1:-1]+inherited_tex[1:])
    old_body = (OLD/'revision.tex').read_text()
    oldlabels = set(re.findall(r'\\label\{([^}]+)\}',old_body + '\n' + '\n'.join(p.read_text() for p in inherited_tex[1:])))
    # The superseded introduction's section label has no mathematical payload.
    oldlabels.discard('sec:v2-introduction')
    env=os.environ.copy(); env['SOURCE_DATE_EPOCH']='1790035200'; env['FORCE_SOURCE_DATE']='1'
    with tempfile.TemporaryDirectory(prefix='gtf-v3-') as tmp:
        base = Path(tmp)/'papers'; work = base/'GTF-I-v3'; work.mkdir(parents=True)
        shutil.copytree(OLD/'legacy',base/'GTF-I-v2/legacy')
        for source in own_tex:
            shutil.copy2(source,work/source.name)
        previous = None
        for passes in range(1,7):
            run = call(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','main.tex'],work,env)
            (evidence/f'LATEX_PASS_{passes}.txt').write_text(run.stdout)
            require(run.returncode == 0, 'LaTeX failed; see pass '+str(passes))
            state = tuple(sha(work/f'main.{ext}') if (work/f'main.{ext}').exists() else '' for ext in ['aux','toc','out'])
            if passes >= 2 and state == previous:
                break
            previous = state
        else:
            raise SystemExit('LaTeX references did not stabilize')
        log = (work/'main.log').read_text(errors='replace')
        (evidence/'LATEX_FINAL.log').write_text(log)
        faults = [x for x in ['There were undefined references','There were undefined citations','multiply defined','Overfull \\hbox','Overfull \\vbox'] if x in log]
        require(not faults,'LaTeX final warnings: '+repr(faults))
        aux = (work/'main.aux').read_text()
        require(all('\\newlabel{'+label+'}' in aux for label in oldlabels), 'Missing inherited mathematical label')
        shutil.copy2(work/'main.pdf',ROOT/'paper.pdf')
        shutil.copy2(work/'main.aux',evidence/'LABELS.aux')
        (evidence/'TEX_RECORDER.fls').write_text((work/'main.fls').read_text())
        pages = int(re.search(r'^Pages:\s+(\d+)',call(['pdfinfo',str(work/'main.pdf')],work).stdout,re.M).group(1))
    archive_files = {str(p.relative_to(ROOT.parent.parent)):p for p in own_tex}
    for p in [ROOT/'SOURCE_MANIFEST.json']+[ROOT/n for n in manifest['new_source_sha256']]:
        archive_files[str(p.relative_to(ROOT.parent.parent))] = p
    for name in set(old_manifest['compiled_and_executable_inputs']) | set(manifest['inherited_input_sha256']) | {'SOURCE_MANIFEST.json'}:
        p=OLD/name
        archive_files[str(p.relative_to(ROOT.parent.parent))] = p
    with zipfile.ZipFile(evidence/'COMPILED_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name,p in sorted(archive_files.items()):
            item=zipfile.ZipInfo(name,(2026,9,22,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(item,p.read_bytes())
    counts = {kind:len(re.findall(r'\\begin\{'+kind+r'\}',combined)) for kind in ['theorem','lemma','proposition','corollary','proof','example']}
    receipt = {'status':'passed','source_commit':os.environ.get('GITHUB_SHA'),
        'run_id':os.environ.get('GITHUB_RUN_ID'),'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),
        'pdf_sha256':sha(ROOT/'paper.pdf'),'pdf_pages':pages,'compiler_passes':passes,
        'compiled_statement_counts':counts,'inherited_mathematical_labels':len(oldlabels),
        'v2_quantitative_body_byte_identical':True,'inherited_git_trees':tree_checks,
        'undefined_references':False,'overfull_boxes':False,'optimized_diagnostics_identical':True,
        'negative_controls':negatives,'diagnostics':json.loads(outputs[0]),
        'scope':'Executed source/build/finite-regression evidence; not independent referee approval or formal proof verification.',
        'visual_review':'Requires separate rendered-page inspection.'}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'pages':pages,'passes':passes,'counts':counts,'retained_labels':len(oldlabels)},indent=2))


if __name__ == '__main__':
    main()
