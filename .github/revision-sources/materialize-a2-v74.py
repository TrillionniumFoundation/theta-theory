#!/usr/bin/env python3
"""Materialize the reviewed-source delta; publish non-circular review pins."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zlib

ROOT=Path(__file__).resolve().parents[2]
PREFIX='papers/A2-v17-boundary-information-coarsening'
REVIEW='9c69f03f97dea57e83061af96aeb9bfe4dcc80d3'
BASE_TREE='80996c207ce723e8d84068f4fe95172f5d18fa65'
EXPECTED_TREE='9e86d9eedeb4c6d8b9456ef4dbb4e11c1d733677'
PATCH_SHA='0dce47b5afc8e969a9e532a9ae5c4c59afef0008cc2e84f8374f7abf588779c7'
SOURCE_BRANCH='revision/a2-v74-moment-reconstruction-2026-09-17'
URL='https://github.com/TrillionniumFoundation/theta-theory'


def require(ok: bool, message: str) -> None:
    if not ok:raise RuntimeError(message)


def git(*args: str, data: bytes|None=None) -> bytes:
    result=subprocess.run(['git',*args],cwd=ROOT,input=data,capture_output=True)
    require(result.returncode==0,'Git failure: '+result.stderr.decode(errors='replace'))
    return result.stdout


def historical_entry() -> str:
    source='3b1e7ce971cf84c8eed10a0077914f43b1b7ca68'
    products='70b0e466bdd2615381e007ed73b1576aaa21f3a0'
    dest=f'deliveries/a2-v73/{source}'
    for name in ('rigidity.pdf','main.pdf','two_collision.pdf','native-source.zip'):
        git('cat-file','-e',f'{products}:{dest}/{name}')
    return f'''# A2 v73 — corrected historical review entry

This repairs the missing v73 handoff identified in the v73 report. It is historical; the current revision is [A2 v74](A2_REVISION_V74_REVIEW_READY.md).

Reviewed source: `{source}`. Native-products head: `{products}`. Review baseline: `{REVIEW}`.

[Principal PDF]({URL}/blob/{products}/{dest}/rigidity.pdf) · [Full technical PDF]({URL}/blob/{products}/{dest}/main.pdf) · [Two-collision companion]({URL}/blob/{products}/{dest}/two_collision.pdf) · [Frozen source ZIP]({URL}/blob/{products}/{dest}/native-source.zip).

[Principal TeX]({URL}/blob/{source}/{PREFIX}/rigidity.tex) · [Response v73]({URL}/blob/{source}/{PREFIX}/RESPONSE_TO_REFEREE_V73.md) · [Referee report]({URL}/blob/{REVIEW}/reviews/a2-v73-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md).

These entries share content. Native build evidence is not independent mathematical certification or journal acceptance.
'''


def write_entry(source: str|None, products: str|None, branch: str) -> None:
    original=ROOT/'README_PRE_V74.md'
    if not original.exists():
        data=git('cat-file','blob',f'{REVIEW}:README.md')
        original.write_bytes(data)
    header='''# Theta-Theory — A2 revision 74

**Current referee entry: [A2_REVISION_V74_REVIEW_READY.md](A2_REVISION_V74_REVIEW_READY.md).**

The complete English revision adds first-moment reconstruction and stronger charged sampling bounds while retaining the relative physical law, actual smooth contact inverse and all inherited mathematical proof inputs. The preparation convention and current-version source/PDF handoff are explicit.

[Principal source](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [Full technical source](papers/A2-v17-boundary-information-coarsening/main.tex) · [Response to v73](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V74.md) · [Corrected historical v73 entry](A2_REVISION_V73_REVIEW_READY.md).

'''
    if source and products:
        dest=f'deliveries/a2-v74/{source}'
        report=json.loads(git('cat-file','blob',f'{products}:{dest}/build-report.json'))
        require(report['source_commit']==source and report['status']=='passed','Wrong native report')
        require(report['source_tree']==EXPECTED_TREE,'Wrong source tree in native report')
        rows=[]
        for stem,title in (('rigidity','Principal article'),('main','Full technical manuscript'),('two_collision','Two-collision companion')):
            item=report['entries'][stem]['product']
            rows.append(f"| {title} | {item['pages']} | [PDF]({URL}/blob/{products}/{dest}/{stem}.pdf) | `{item['sha256']}` |")
        entry=f'''# A2 revision 74 — source-matched referee handoff

Qian Qi · September 17, 2026

## Immutable references

Reviewed report: `{REVIEW}` on `review/a2-v73-independent-harsh-top4-2026-09-17`.

Compiled source commit: **`{source}`**. Manuscript subtree: **`{EXPECTED_TREE}`**.

Native product commit: **`{products}`**. Reading branch: **`{branch}`**. Source branch: **`{SOURCE_BRANCH}`**. Later handoff/inspection commits may update documentation without changing the compiled manuscript subtree.

## Complete native manuscripts

| Entry | Pages | Native object | SHA-256 |
|---|---:|---|---|
'''+ '\n'.join(rows)+f'''

The page counts overlap; they are not added as independent mathematical output.

[Frozen complete source ZIP]({URL}/blob/{products}/{dest}/native-source.zip) · [Native build report]({URL}/blob/{products}/{dest}/build-report.json) · [Retained-object hashes]({URL}/blob/{products}/{dest}/REPOSITORY_RETENTION.json) · [Fetched-object verification]({URL}/blob/{branch}/{dest}/COMMITTED_OBJECTS_VERIFIED.json).

## Reading and response

[Principal TeX]({URL}/blob/{source}/{PREFIX}/rigidity.tex) · [Complete technical TeX]({URL}/blob/{source}/{PREFIX}/main.tex) · [Point-by-point response]({URL}/blob/{source}/{PREFIX}/RESPONSE_TO_REFEREE_V74.md) · [Historical derivation audit]({URL}/blob/{source}/{PREFIX}/HISTORICAL_DERIVATION_AUDIT_V74.md) · [Preservation evidence]({URL}/blob/{source}/{PREFIX}/REVISION_V74_PRESERVATION.json).

The new overview is `article/00p_moment_overview_v74.tex`; complete new proofs are in `article/10i_moment_reconstruction_v74.tex`. The density is reconstructed from four one-dimensional weighted profiles. The signed slopes imply a determinant floor; the finite rank defect is retained; the estimator fits actual table–offset pairs. Area recovery retains its flight-length sensitivity and assumes independent normalized unit-speed Liouville preparations with exact success tags.

All 969 inherited manuscript paths remain. Nine modified originals are byte- and mode-preserved. No previously active mathematical proof input is removed. The normal-incidence two-offset, analytic/global, information and companion routes remain under their hypotheses.

## Verification boundary

The three complete entries were built from the pinned Git source; normal/optimized diagnostics and source/recorder checks are retained. Native publication checks the fetched Git object bytes. These checks are not mathematical correctness, minimax optimality, or journal-acceptance certificates. Visual inspection is separate; the latest reading branch records any subsequently performed inspection. The full historical catalogue is preserved and compiled, not newly independently recertified theorem by theorem.
'''
        header+=f'Compiled source: `{source}`. Source-matched native products: `{products}`. See the current entry for individual PDFs and hashes.\n\n'
        record={'review_commit':REVIEW,'source_commit':source,'source_tree':EXPECTED_TREE,'native_product_commit':products,'products_branch':branch,'source_branch':SOURCE_BRANCH,'delivery':dest,'run_id':os.environ.get('GITHUB_RUN_ID'),'status':'native-built-and-published'}
        (ROOT/'A2_REVISION_V74_PROVENANCE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:
        entry=f'''# A2 revision 74 — source handoff

The complete materialized source is on `{SOURCE_BRANCH}` with manuscript subtree `{EXPECTED_TREE}`, based on review `{REVIEW}`.

[Principal source]({PREFIX}/rigidity.tex) · [Full source]({PREFIX}/main.tex) · [Response]({PREFIX}/RESPONSE_TO_REFEREE_V74.md).

The native workflow publishes to `{branch}`. This source-stage entry does not yet claim a successful native build. After successful publication it is replaced, on both new branches, by immutable source/PDF references and actual hashes. The corrected [historical v73 entry](A2_REVISION_V73_REVIEW_READY.md) remains available.
'''
    (ROOT/'A2_REVISION_V74_REVIEW_READY.md').write_text(entry)
    (ROOT/'README.md').write_text(header+'<details>\n<summary>Historical v72 root entry, retained verbatim</summary>\n\n'+original.read_text()+'\n</details>\n')
    (ROOT/'A2_REVISION_V73_REVIEW_READY.md').write_text(historical_entry())


def materialize(branch: str) -> None:
    require(git('rev-parse',f'HEAD:{PREFIX}').decode().strip()==BASE_TREE,'Refusing an unexpected manuscript baseline')
    files=sorted(Path(__file__).parent.glob('a2-v74.delta.zlib.part*'))
    require(len(files)==4,'Expected four ordered delta parts')
    patch=zlib.decompress(b''.join(p.read_bytes() for p in files))
    require(hashlib.sha256(patch).hexdigest()==PATCH_SHA,'Corrupt source delta')
    git('apply','--check','--directory='+PREFIX,'-',data=patch)
    git('apply','--index','--directory='+PREFIX,'-',data=patch)
    edited=json.loads((ROOT/PREFIX/'REVISION_V74_EDITED_PATHS.json').read_text())
    require(len(edited)==9,'Unexpected archived-original list')
    for name in edited:
        p=ROOT/PREFIX/'history/v73-review-baseline'/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(git('cat-file','blob',f'{BASE_TREE}:{name}'))
        mode=git('ls-tree',BASE_TREE,'--',name).split()[0].decode()
        p.chmod(int(mode,8)&0o777)
    git('add','--',PREFIX+'/history/v73-review-baseline')
    require(git('write-tree','--prefix='+PREFIX+'/').decode().strip()==EXPECTED_TREE,'Materialized tree differs from tested source')
    write_entry(None,None,branch)
    git('add','--','README.md','README_PRE_V74.md','A2_REVISION_V73_REVIEW_READY.md','A2_REVISION_V74_REVIEW_READY.md')
    print(json.dumps({'status':'materialized','source_tree':EXPECTED_TREE},sort_keys=True))


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation',choices=('materialize','handoff'))
    p.add_argument('--products-branch',required=True)
    p.add_argument('--source-commit')
    p.add_argument('--products-commit')
    a=p.parse_args()
    if a.operation=='materialize':materialize(a.products_branch)
    else:
        require(bool(a.source_commit and a.products_commit),'Missing immutable publication references')
        write_entry(a.source_commit,a.products_commit,a.products_branch)

if __name__=='__main__':main()
