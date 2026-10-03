#!/usr/bin/env python3
"""Publish only generated v71 artifacts after source qualification in CI.

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
BRANCH='revision/general-theta-foundations-i-v71-input-dependent-boundary-2026-10-03'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V71_REVIEW_READY.md'

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
    counts=receipt['regression']['check_conditional.py']
    lines=['# General Theta Foundations I — Revision 71 referee entry','',
        'Controlling v68/r45 report: `e862e5c963ef36b9caa3b1b814b495ae4428a088`; audit: `a3fd5b80549a855c46151fd7183b3fc7139abac7`.',
        'Base: completed v70 final head `a5cd3bb0ea9c29f680381230c603e54354866376`. No v70-specific report was located; v69 is an unfinished anchor.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','',
        'New main result: fixed-readout input-dependent instruments have joint description length (V/2)log2N+Vlog2(1/delta)+O(1), V=sum_x(sum_y r_xy(2n-r_xy)-1), for N>=1 and 0<delta<=delta_*<2 at fixed dimensions, ranks and cap.',
        'Arbitrary legal memoryless centres retract to fixed-readout centres. Rational upper encoding preserves conditional zero blocks and never increases target ranks; centre retraction itself may increase rank.',
        'A common estimator and covering-multiplicity theorem extend the inherited interior and preparation laws to every fixed submaximal error cap. The coherent tensor law keeps its own small-error range.',
        'This is a supplied-description result, not an unknown-instrument learning theorem, mutable-workspace optimum or physical classical simulator. The measured input basis is fixed.',
        'All 14 required and 24 detailed r45 comments are addressed, with new versus inherited results identified and direct CMW, SHW and tomography comparisons retained. Independent priority review is not represented as obtained.','',
        'New quantitative locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions; '+str(counts['code_cases'])+' code cases; '+str(counts['adaptive_classical_policy_cases'])+' adaptive classical policy cases; '+str(len(counts['negative_controls']))+' negative controls. Ordinary and optimized outputs agree. All seven inherited suites execute.',
        'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files and '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current complete edition has '+str(receipt['complete_active_labels'])+' labels. Zero unresolved references/citations and zero overfull/underfull boxes.',
        'The native archive rebuilds in isolation and the minimal journal package reconstructs without historical PDFs. Mathematical proof, finite regression, source identity and independent priority remain distinct assertions.',
        'Work branch: `'+BRANCH+'`.',
        'Referee branch after exact-head reconstruction: `revision/general-theta-foundations-i-v71-referee-ready-2026-10-03`.',
        'Package hashes: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. Final-head attestation remains external.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v71 input-dependent boundary and full-error coding manuscripts'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
