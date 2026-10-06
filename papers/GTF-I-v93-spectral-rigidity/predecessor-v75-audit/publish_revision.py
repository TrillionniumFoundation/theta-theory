#!/usr/bin/env python3
"""Publish only generated v74 artifacts after source qualification in CI.

Never force-push; require an unchanged remote branch and immutable native and
predecessor sources. This script is not a mathematical or signature verifier.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent
BRANCH='revision/general-theta-foundations-i-v74-coupled-boundary-geometry-2026-10-04'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V74_REVIEW_READY.md'

def require(ok:bool,message:str)->None:
    if not ok: raise RuntimeError(message)

def git(*args:str)->str:
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main()->None:
    repo=Path(git('rev-parse','--show-toplevel'))
    prefix=ROOT.relative_to(repo).as_posix()
    source=os.environ['GITHUB_SHA']
    require(os.environ.get('GITHUB_REF')=='refs/heads/'+BRANCH,'wrong publication branch')
    require(git('rev-parse','HEAD')==source,'wrong checkout')
    remote=git('ls-remote','--heads','origin','refs/heads/'+BRANCH).split()
    require(len(remote)==2 and remote[0]==source,'remote advanced; refusing publication')
    receipt=json.loads((ROOT/'evidence/BUILD_RECEIPT.json').read_text())
    require(receipt['status']=='success' and receipt['source_commit']==source and receipt['isolated_rebuild'],'source qualification failed')
    require(receipt['normal_optimized_identical'],'optimization mismatch')
    require(all(not v for v in receipt['latex_diagnostics'].values()),'typesetting diagnostics remain')
    jr=json.loads((ROOT/'evidence/JOURNAL_REBUILD_RECEIPT.json').read_text())
    require(jr['status']=='success' and jr['source_commit']==source,'journal reconstruction failed')
    inv=json.loads((ROOT/'evidence/SOURCE_HASHES.json').read_text())
    for name,h in inv.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'native changed: '+name)
    preserve=json.loads((ROOT/'PRESERVATION_MANIFEST.json').read_text())
    for name,h in preserve['files'].items():
        p=repo/preserve['source_root']/name
        require(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==h,'predecessor differs: '+name)
    allowed={prefix+'/'+n for n in receipt['documents']}
    for name in git('diff','--name-only').splitlines():
        require(name.startswith(prefix+'/evidence/') or name in allowed,'builder altered tracked source: '+name)
    loc=json.loads((ROOT/'evidence/THEOREM_LOCATIONS.json').read_text())['quantitative.tex']
    counts=receipt['regression']['check_coupled_geometry.py']
    lines=['# General Theta Foundations I — Revision 74 referee entry','',
        'Controlling v73/r47 report: `fa857238020a0b5f2befd936b39820a9b426390a`; audit: `62ffc56f0911b939f3e6b79ae0a5e38563e5a988`.',
        'Base: completed v73 final head `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`. This revision continues the existing v74 anchor.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','',
        'New metric: for all unbiased binary qubit measurements, s=min(|x|,|y|) and D=sqrt(N/(1-s²+1/N))|x-y| give (1/256)min(1,D)<=d_N<=min(2,6D). Visibility and direction may both change.',
        'New geometric criterion: a compact k-Ahlfors-regular identifiable subfamily has small-error covering order delta^(-k) integral [N/(1-|x|²+1/N)]^(k/2) dmu. Lower centres are arbitrary legal memoryless instruments; upper centres lie in the family.',
        'Boundary-depth order t^alpha gives a contact trichotomy. The jointly encoded disk has cover order N log(N+2)/delta²; the ball has N²/delta³. These statements retain a fixed small-error cap and explicit geometric hypotheses.',
        'An exact rational codec accepts Cartesian rational inputs with possibly irrational norm. One index charges both visibility and direction. Every word decodes to a legal rational instrument; target replay is a separate check.',
        'All 17 required and 30 detailed r47 comments are mapped. Sedlak–Ziman (2014) and Puchala et al. (2018) are directly compared. Independent human priority and author signing remain external, not fabricated. No change of journal target is made.','',
        'New quantitative theorem locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions; '+str(counts['cases'])+'; '+str(len(counts['negative_controls']))+' negative controls. Normal/optimized results agree. All ten inherited suites run unchanged.',
        'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files, '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current total '+str(receipt['complete_active_labels'])+'. No unresolved references/citations or overfull/underfull boxes.',
        'Native ZIP and minimal journal package reconstruct independently. CI certifies source/artifact identity, not universal proof, independent priority, authorship or acceptance.',
        'Work branch: `'+BRANCH+'`.',
        'Referee alias after exact-head verification: `revision/general-theta-foundations-i-v74-referee-ready-2026-10-04`.',
        'Package hashes: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. The final-head attestation remains an external artifact.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v74 coupled-boundary manuscripts and joint rational codec'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
