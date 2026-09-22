#!/usr/bin/env python3
"""Build the revision, preserving v1 sources and binding products to actual inputs."""
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

ROOT=Path(__file__).resolve().parent

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def execute(command: list[str], cwd: Path, env=None):
    return subprocess.run(command,cwd=cwd,env=env,text=True,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)

def main() -> None:
    for program in ['pdflatex','pdfinfo']:
        if not shutil.which(program):
            raise SystemExit('Missing required executable: '+program)
    evidence=ROOT/'evidence'; evidence.mkdir(exist_ok=True)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name,expected in manifest['compiled_and_executable_inputs'].items():
        if digest(ROOT/name) != expected:
            raise SystemExit('Revision source hash mismatch: '+name)
    old=json.loads((ROOT/'legacy/SOURCE_MANIFEST.json').read_text())
    for name,expected in old['compiled_and_executable_inputs'].items():
        if digest(ROOT/'legacy'/name) != expected:
            raise SystemExit('Changed first-edition source: '+name)
    results=[]
    for flags,name in [([], 'DIAGNOSTICS.json'),(['-O'],'DIAGNOSTICS_OPTIMIZED.json')]:
        run=execute([sys.executable,*flags,str(ROOT/'verify.py')],ROOT)
        (evidence/name).write_text(run.stdout)
        if run.returncode:
            raise SystemExit('Diagnostic failure: '+name)
        results.append(run.stdout)
    if results[0] != results[1]:
        raise SystemExit('Optimized diagnostics differ')
    negative={}
    for mutant in ['omit-calibration-noise','wrong-projective-rate']:
        run=execute([sys.executable,str(ROOT/'verify.py'),'--mutant',mutant],ROOT)
        (evidence/('MUTANT_'+mutant+'.txt')).write_text(run.stdout)
        if run.returncode == 0:
            raise SystemExit('Negative control survived: '+mutant)
        negative[mutant]={'rejected':True,'exit_code':run.returncode}
    run=execute([sys.executable,str(ROOT/'legacy/tools/verify.py')],ROOT/'legacy')
    (evidence/'LEGACY_DIAGNOSTICS.json').write_text(run.stdout)
    if run.returncode:
        raise SystemExit('Preserved first-edition diagnostics failed')
    env=os.environ.copy(); env['SOURCE_DATE_EPOCH']='1790035200'; env['FORCE_SOURCE_DATE']='1'
    sources=[ROOT/name for name in sorted(manifest['compiled_and_executable_inputs'])]
    retained=sorted((ROOT/'legacy/sections').glob('*.tex'))
    retained=[p for p in retained if p.name != '01_introduction.tex']
    tree_checks={}
    if os.environ.get('GITHUB_SHA'):
        for name,expected in manifest['preserved_trees'].items():
            query=os.environ['GITHUB_SHA']+':papers/GTF-I-v2/'+name
            result=execute(['git','rev-parse',query],ROOT)
            if result.returncode or result.stdout.strip() != expected:
                raise SystemExit('Preserved Git tree mismatch: '+name)
            tree_checks[name]=expected
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}', '\n'.join(p.read_text() for p in retained)))
    with tempfile.TemporaryDirectory(prefix='gtf-i-v2-') as tmp:
        work=Path(tmp)
        shutil.copytree(ROOT/'legacy',work/'legacy')
        for name in ['main.tex','revision.tex']:
            shutil.copy2(ROOT/name,work/name)
        refs=(ROOT/'legacy/references.tex').read_text().replace(
            '\\end{thebibliography}',(ROOT/'new_references.tex').read_text()+'\n\\end{thebibliography}')
        (work/'references.tex').write_text(refs)
        previous=None
        for passes in range(1,7):
            run=execute(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                         '-file-line-error','-recorder','main.tex'],work,env)
            (evidence/f'LATEX_PASS_{passes}.txt').write_text(run.stdout)
            if run.returncode:
                raise SystemExit(f'LaTeX failure on pass {passes}; see evidence')
            state=tuple(digest(work/f'main.{ext}') if (work/f'main.{ext}').exists() else ''
                        for ext in ['aux','toc','out'])
            if state == previous and passes >= 2:
                break
            previous=state
        else:
            raise SystemExit('Cross-references did not stabilize')
        log=(work/'main.log').read_text(errors='replace')
        (evidence/'LATEX_FINAL.log').write_text(log)
        bad=['There were undefined references','There were undefined citations','multiply defined',
             'Overfull \\hbox','Overfull \\vbox']
        failures=[x for x in bad if x in log]
        if failures:
            raise SystemExit('LaTeX final warnings: '+repr(failures))
        aux=(work/'main.aux').read_text()
        missing=sorted(label for label in oldlabels if '\\newlabel{'+label+'}' not in aux)
        if missing:
            raise SystemExit('Missing retained label(s): '+repr(missing))
        shutil.copy2(work/'main.pdf',ROOT/'paper.pdf')
        shutil.copy2(work/'main.aux',evidence/'LABELS.aux')
        info=execute(['pdfinfo',str(work/'main.pdf')],work).stdout
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        # Store a readable list of the TeX inputs actually opened by the engine.
        recorder=(work/'main.fls').read_text().splitlines()
        inputs=sorted({x[6:] for x in recorder if x.startswith('INPUT ') and '.tex' in x})
        (evidence/'TEX_INPUTS.json').write_text(json.dumps(inputs,indent=2)+'\n')
        combined=(ROOT/'revision.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in retained)
        counts={kind:len(re.findall(r'\\begin\{'+kind+r'\}',combined))
                for kind in ['theorem','lemma','proposition','corollary','proof','example']}
        with zipfile.ZipFile(evidence/'COMPILED_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for path in sources+[ROOT/'SOURCE_MANIFEST.json']:
                entry=zipfile.ZipInfo(str(path.relative_to(ROOT)),(2026,9,22,0,0,0))
                entry.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(entry,path.read_bytes())
            entry=zipfile.ZipInfo('references.tex',(2026,9,22,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(entry,refs.encode())
        receipt={'status':'passed','source_commit':os.environ.get('GITHUB_SHA'),
            'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in sources},
            'derived_references_sha256':digest(work/'references.tex'),
            'pdf_sha256':digest(ROOT/'paper.pdf'),'pdf_pages':pages,'compiler_passes':passes,
            'compiled_statement_counts':counts,'retained_label_count':len(oldlabels),
            'retained_v1_manifest_verified':True,'preserved_git_trees_verified':tree_checks,
            'negative_controls':negative,
            'new_diagnostics':json.loads(results[0]),'optimized_output_identical':True,
            'undefined_references':False,'overfull_boxes':False,
            'visual_review':'Requires a separate rendered-page inspection; not certified by this script.',
            'run_id':os.environ.get('GITHUB_RUN_ID'),
            'scope':'Executed build and finite regression evidence, not independent referee approval or formal proof verification.'}
        (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'pages':pages,'passes':passes,'retained_labels':len(oldlabels),
                          'counts':counts},indent=2))

if __name__ == '__main__':
    main()
