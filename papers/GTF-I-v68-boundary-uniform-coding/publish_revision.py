#!/usr/bin/env python3
"""Publish only generated v68 artifacts after source qualification in CI.

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
BRANCH='revision/general-theta-foundations-i-v68-boundary-uniform-coding-2026-10-03'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V68_REVIEW_READY.md'

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
    counts=receipt['regression']['check_preparation.py']
    lines=['# General Theta Foundations I — Revision 68 referee entry','',
           'Controlling v67/r44 report: `68c69a4a2e8b4e3b11c43a181806ab578584b719`; companion audit: `7a9586cd8cf7995152fbbf501f3e47da4aa89900`.',
           'Base v67 qualified publication: `98a4b12126502ea41c620b58bad4b9aa30f9c72c`. The controlling reports review this exact v67 publication.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','',
        'Main additions: uniform joint code length (s/2) log2 N+s log2(1/delta)+O(1) on a fixed positive Choi body, and rank-stratified boundary preparation code length (v/2) log2 N+v log2(1/delta)+O(1), v=sum_y r_y(2n-r_y)-1. Remainders are independent of N and delta for N>=1 and 0<delta<=1/32. A rational triangular-factor codec preserves zero outcomes and never increases ranks.',
        'The adaptive bound covers a common tester with quantum memory, initially entangled reference, feedback and bounded public stopping. The preparation family admits an exact product-state reduction, while the general positive-body theorem uses the inherited classical-programme bound. Unitary boundary examples are retained, not contradicted by the restricted preparation theorem.',
        'These are description lower bounds, not general mutable-space lower bounds, channel-learning query bounds, or physical finite-classical-message simulation of unknown quantum input. All inherited spectral, numerical, causal and crossover hypotheses remain.',
        'The response treats all fourteen required r44 items and twenty-four detailed comments. The bibliography compares Naik et al., current channel-learning results, adaptive binary channel discrimination, quantum population compression and the classical-programme metrology antecedent. Independent expert priority clearance is not represented as obtained.','',
        'New quantitative locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions and '+str(len(counts['negative_controls']))+' named negative controls; ordinary and optimized outputs agree. All five inherited suites also execute.',
       'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files and '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current complete edition has '+str(receipt['complete_active_labels'])+' labels. Zero unresolved references/citations and zero overfull/underfull boxes.',
       'The native source archive rebuilds in isolation and the journal package rebuilds without historical PDFs. These are executed source, arithmetic and typesetting checks, not universal mathematical or independent priority certificates.',
       'No cryptographic author signature, journal acceptance or A/B/C/D analytic aggregate completion is asserted.','',
       'Work branch: `'+BRANCH+'`.',
       'Referee branch, created after exact-head verification: `revision/general-theta-foundations-i-v68-referee-ready-2026-10-03`.',
       'Package digests: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. The final-head attestation is external to the checked tree.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v68 joint-precision and rank-boundary coding manuscripts'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
