#!/usr/bin/env python3
"""Publish only generated v72 artifacts after source qualification in CI.

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
BRANCH='revision/general-theta-foundations-i-v72-varying-readout-2026-10-03'
ENTRY='GENERAL_THETA_FOUNDATIONS_I_V72_REVIEW_READY.md'

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
    counts=receipt['regression']['check_readout.py']
    lines=['# General Theta Foundations I — Revision 72 referee entry','',
        'Controlling v71/r46 report: `b78c1dddd41de645edf207bc415406b3fc1b5e83`; audit: `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.',
        'Base: completed v71 final head `8c053f4820da3abcbb04daab628aa94379fd01e3`. The existing incomplete v72 work anchor was continued, not treated as a prior verified publication.','']
    for title,name in [('Quantitative','paper.pdf'),('Structural','STRUCTURAL_PAPER.pdf'),('Complete research edition','COMPLETE_REVISION.pdf')]:
        lines.append(title+': `'+prefix+'/'+name+'` ('+str(receipt['documents'][name]['pages'])+' pages).')
    lines+=['','Native source: `'+source+'`.','Builder run: `'+os.environ['GITHUB_RUN_ID']+'`.','',
        'Main theorem: observable varying projective readout has joint description length (b+V/2)log2N+(b+V)log2(1/delta)+O(1), with b=d^2-d and V=sum_x(sum_y r_xy(2n-r_xy)-1), at fixed dimensions/ranks, N>=1 and 0<delta<=1/32.',
        'The direct rational projector codec uses bounded pivoted triangular coordinates, not normalized algebraic eigenvectors or exhaustive unitary search. Upper centres preserve conditional zeros and ranks; the lower cover permits arbitrary legal memoryless centres.',
        'Uniform ambient-domain environment seizing transfers family covering numbers exactly, including arbitrary centres. The inherited full submaximal-error rank-state law yields a Pauli/Bell coding corollary. Centre retraction itself may increase Choi rank.',
        'The imported measurement-discrimination and environment-state principles are cited separately from the new family-covering and coding arguments. Readout must remain observable or be recovered by fixed orthogonal output supports.',
        'All sixteen required and twenty-six detailed r46 comments are mapped in RESPONSE_TO_REFEREE.md. No independent priority opinion, author signature or journal acceptance is claimed. Every analytic A/B/C/D aggregate flag remains false.','',
        'New quantitative locations:']
    for label in receipt['new_theorems']:
        item=loc[label];lines.append('- `'+label+'`: '+item['number']+', page '+item['page']+'.')
    lines+=['','New exact regression: '+str(counts['exact_assertions'])+' assertions; '+str(counts['flag_chart_cases'])+' chart cases; '+str(counts['codec_cases'])+' codec cases; '+str(len(counts['negative_controls']))+' negative controls. Normal and optimized outputs agree. All eight inherited suites execute unchanged.',
        'Preserved: '+str(receipt['predecessor_native_files'])+' predecessor native files and '+str(receipt['preserved_native_labels'])+' prior complete-edition labels; current complete edition has '+str(receipt['complete_active_labels'])+' labels. Zero unresolved references/citations and zero overfull/underfull boxes.',
        'The native archive and minimal journal package rebuild independently without historical PDFs. Finite regression, written proof, source identity, independent priority and acceptance remain distinct assertions.',
        'Work branch: `'+BRANCH+'`.',
        'Referee branch after exact-head reconstruction: `revision/general-theta-foundations-i-v72-referee-ready-2026-10-03`.',
        'Package hashes: `'+prefix+'/evidence/PACKAGE_MANIFEST.json`. Final-head attestation remains external.','']
    (repo/ENTRY).write_text('\n'.join(lines))
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    paths=[prefix+'/'+n for n in receipt['documents']]+[prefix+'/evidence',ENTRY]
    subprocess.run(['git','add','-f',*paths],cwd=repo,check=True)
    subprocess.run(['git','commit','-m','docs(gtf-i): publish qualified v72 observable readout and seizable-family manuscripts'],cwd=repo,check=True)
    subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    print(json.dumps({'publication':git('rev-parse','HEAD'),'source':source,'branch':BRANCH}))

if __name__=='__main__':main()
