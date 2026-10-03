#!/usr/bin/env python3
"""Publish only generated v73 artifacts after source qualification in CI.

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
BRANCH='revision/general-theta-foundations-i-v73-noisy-readout-crossover-2026-10-04'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V73_REVIEW_READY.md'

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
    counts=receipt['regression']['check_noisy_readout.py']
    lines=['# General Theta Foundations I — Revision 73 referee entry','',
        'Controlling v71/r46 report: `b78c1dddd41de645edf207bc415406b3fc1b5e83`; audit: `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.',
        'Base: completed v72 final head `12296ed387dbc197ff7cb854d3a78d0bf964960e`. Its source and exact-head runs succeeded; no v72-specific external review was located.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','Transfer/workflow trigger: `'+os.environ.get('GTF73_TRANSFER_COMMIT',source)+'`; all native files were committed before qualification.','',
        'Main theorem: for public visibility lambda in [0,1], let K=lambda*sqrt(N*min(N,1/(1-lambda^2))), with K(N,1)=N and K(N,0)=0. The adaptive angular metric lies between (1/64)min(1,K h) and min(2,K h). For N>=1 and 0<delta<=2^-10, optimal supplied-description length is log2(1+K/delta)+O(1), uniformly in noise, horizon and accuracy.',
        'The exact finite programme upper bound controls references, adaptive feedback and bounded stopping. Finite GHZ blocks with an elementary Bernoulli product bound give the reverse modulus; no local Fisher-information inference substitutes for a finite-distance proof.',
        'Two rational circle charts yield legal effects. Appending labelled rank-bounded conditional states contributes (V/2)log2N+Vlog2(1/delta), where V=sum_y[r_y(2n-r_y)-1]. Rational visibility gives rational Choi centres, and encoded conditional state ranks never increase.',
        'Classical simulation and the familiar metrological noise crossover are credited to primary antecedents. The new claim is the noise-uniform finite-use covering/rational-code consequence, not invention of those principles. The v72 observable projective-readout and seizing results are inherited with their full proofs.',
        'All sixteen required and twenty-six detailed r46 comments are mapped in RESPONSE_TO_REFEREE.md. No independent priority opinion, author signature or journal acceptance is claimed. Every analytic A/B/C/D aggregate flag remains false.','',
        'New quantitative locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions; '+str(counts['readout_cases'])+' readout cases; '+str(counts['ghz_block_cases'])+' GHZ block cases; '+str(counts['conditional_cases'])+' conditional cases; '+str(len(counts['negative_controls']))+' negative controls. Normal and optimized outputs agree. All nine inherited suites execute unchanged.',
        'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files and '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current complete edition has '+str(receipt['complete_active_labels'])+' labels. Zero unresolved references/citations and zero overfull/underfull boxes.',
        'The native archive and minimal journal package rebuild independently without historical PDFs. Finite regression, written proof, source identity, independent priority and acceptance remain distinct assertions.',
        'Work branch: `'+BRANCH+'`.',
        'Referee branch after exact-head reconstruction: `revision/general-theta-foundations-i-v73-referee-ready-2026-10-04`.',
        'Package hashes: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. Final-head attestation remains external.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v73 noise-uniform readout manuscripts and exact codec'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
