#!/usr/bin/env python3
"""Publish only generated v70 artifacts after source qualification in CI.

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
BRANCH='revision/general-theta-foundations-i-v70-coherent-boundary-coding-2026-10-03'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V70_REVIEW_READY.md'

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
    counts=receipt['regression']['check_coherent.py']
    lines=['# General Theta Foundations I — Revision 70 referee entry','',
           'Controlling v68/r45 report: `e862e5c963ef36b9caa3b1b814b495ae4428a088`; companion audit: `a3fd5b80549a855c46151fd7183b3fc7139abac7`.',
           'Mathematical base: completed v68 head `d9d8c464282157485813041d181e909e648b1f4f`. The preserved v69 continuation is an anchor, not a theorem premise.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','',
        'New main result: for F_(U,sigma),y(X)=U X U* tensor sigma_y, let u=d^2-1 and v=sum r_y(2n-r_y)-1. The optimal reusable description length is (u+v/2)log2N+(u+v)log2(1/delta)+O(1), uniformly for N>=1 and 0<delta<=1/32 at fixed dimensions/ranks. The converse permits all legal memoryless centres; rational upper centres retain zero outcomes and do not increase preparation ranks.',
        'The family retains coherent data and permits singular support-changing preparation blocks. Outcome probabilities are input independent; the theorem is not a classification of all disturbing-instrument directions. The metric includes common adaptive quantum testers, references, feedback and bounded public stopping.',
        'A separate exact preparation-centre retraction C -> R_(C(I/d)) is valid at every positive covering radius and may increase centre rank. It does not prove the full-error coding-law proposal in the v69 anchor.',
        'A general-d rational unitary atlas with d^2-1 digits and an exact finite search encoder is proved and implemented. The direct qubit codec uses three stereographic quaternion digits and the inherited preparation factor codec. It uses exact rational arithmetic and a valid triangle-error certificate.',
        'The response addresses fourteen required and twenty-four detailed r45 comments and directly compares Cooney–Mosonyi–Wilde and classical unitary-discrimination antecedents. Independent priority review is not represented as obtained. All earlier mathematical results and analytic status flags remain.','',
        'New quantitative locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions and '+str(len(counts['negative_controls']))+' named negative controls; ordinary and optimized outputs agree. All six inherited suites also execute.',
       'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files and '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current complete edition has '+str(receipt['complete_active_labels'])+' labels. Zero unresolved references/citations and zero overfull/underfull boxes.',
       'The native source archive rebuilds in isolation and the journal package rebuilds without historical PDFs. These are executed source, arithmetic and typesetting checks, not universal mathematical or independent priority certificates.',
       'No cryptographic author signature, journal acceptance or A/B/C/D analytic aggregate completion is asserted.','',
       'Work branch: `'+BRANCH+'`.',
       'Referee branch, created after exact-head verification: `revision/general-theta-foundations-i-v70-referee-ready-2026-10-03`.',
       'Package digests: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. The final-head attestation is external to the checked tree.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v70 coherent and preparation boundary coding manuscripts'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
