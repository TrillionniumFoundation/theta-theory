#!/usr/bin/env python3
"""Publish only generated v67 artifacts after source qualification in CI.

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
BRANCH='revision/general-theta-foundations-i-v67-intrinsic-instrument-entropy-2026-10-03'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V67_REVIEW_READY.md'

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
    counts=receipt['regression']['check_codec.py']
    lines=['# General Theta Foundations I — Revision 67 referee entry','',
           'Controlling v66/r43 report: `0a3d74582eeeda315237ee73fdd2ac0021862184`; companion audit: `6c2aee0e242668ff960f3bf4835c87923b8e730f`.',
           'Base v66 final head: `58490231d19fd5c5e557e353593251f1202105fa`.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','',
        'Main additions: intrinsic dimension s=d^2(mn^2-1), optimal fixed-dimension high-resolution instrument-description length s log2(1/eta)+O(1), and optimal fixed-error reusable memoryless-instrument description length (s/2) log2 N+O(1) on a fixed strictly positive Choi body. The exact intrinsic rational codec attains both exponents.',
        'The adaptive bound covers a common tester with quantum memory, initially entangled reference, feedback and bounded public stopping. Its classical-programme ingredient is credited; unitary boundary examples exclude a uniform square-root continuity claim without a margin.',
        'These are description lower bounds, not general mutable-space lower bounds, channel-learning query bounds, or physical finite-classical-message simulation of unknown quantum input. All inherited spectral, numerical, causal and crossover hypotheses remain.',
        'The response treats all fifteen required r43 items and twenty-four detailed comments. The bibliography compares Naik et al., current channel-learning results and the classical-programme metrology antecedent. Independent expert priority clearance is not represented as obtained.','',
        'New quantitative locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions and '+str(len(counts['negative_controls']))+' named negative controls; ordinary and optimized outputs agree. All four inherited suites also execute.',
       'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files and '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current complete edition has '+str(receipt['complete_active_labels'])+' labels. Zero unresolved references/citations and zero overfull/underfull boxes.',
       'The native source archive rebuilds in isolation and the journal package rebuilds without historical PDFs. These are executed source, arithmetic and typesetting checks, not universal mathematical or independent priority certificates.',
       'No cryptographic author signature, journal acceptance or A/B/C/D analytic aggregate completion is asserted.','',
       'Work branch: `'+BRANCH+'`.',
       'Referee branch, created after exact-head verification: `revision/general-theta-foundations-i-v67-referee-ready-2026-10-03`.',
       'Package digests: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. The final-head attestation is external to the checked tree.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v67 intrinsic and adaptive instrument entropy manuscripts'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
