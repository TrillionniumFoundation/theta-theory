#!/usr/bin/env python3
"""Generate a precise handoff after source-matched products are committed."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

P='papers/A2-v17-boundary-information-coarsening'
REPO='https://github.com/TrillionniumFoundation/theta-theory'
SOURCE_BRANCH='revision/a2-v75-mechanism-first-2026-09-17'

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-commit',required=True)
    ap.add_argument('--products-commit',required=True)
    ap.add_argument('--products-branch',required=True)
    a=ap.parse_args()
    for value in (a.source_commit,a.products_commit):
        if not re.fullmatch('[0-9a-f]{40}',value):
            raise RuntimeError('Noncanonical commit')
    dest=Path('deliveries/a2-v75')/a.source_commit
    report=json.loads((dest/'build-report.json').read_text())
    if report['status']!='passed' or report['source_commit']!=a.source_commit:
        raise RuntimeError('Unmatched native build')
    tree=subprocess.check_output(['git','rev-parse',a.source_commit+':'+P],text=True).strip()
    products={}
    for stem in ('rigidity','main','two_collision'):
        path=dest/(stem+'.pdf')
        info=subprocess.check_output(['pdfinfo',str(path)],text=True)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
        products[stem]={'pages':pages,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'url':f'{REPO}/blob/{a.products_commit}/{path.as_posix()}',
          'path':path.as_posix()}
    data={'revision':75,'review_commit':'1ad828fd3cec7d39881fa4bb31d14423c4fd35da',
      'source_branch':SOURCE_BRANCH,'compiled_source_commit':a.source_commit,
      'manuscript_tree':tree,'native_products_commit':a.products_commit,
      'native_products_branch':a.products_branch,'products':products,
      'baseline_files_retained':992,'baseline_active_labels_retained':1423,
      'new_mathematical_certification':False,
      'visual_coverage':'Recorded in A2_REVISION_V75_VERIFICATION.md after retrieval, separately from native build evidence.'}
    Path('A2_REVISION_V75_PROVENANCE.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    lines=['# A2 revision 75: referee entry', '',
      '**Principal manuscript:** Boundary laws and smooth contact rigidity of periodic dispersing billiards.', '',
      'This revision answers the v74 report by centering the relatively normalized physical law and actual smooth contact inverse. The full technical programme and all inherited proof files remain available; the compressed principal architecture is not a reduction in theorem scope.', '',
      f'- Source branch: `{SOURCE_BRANCH}`.',
      f'- Frozen compiled source: `{a.source_commit}`.',
      f'- Manuscript subtree: `{tree}`.',
      f'- Native products branch: `{a.products_branch}`.',
      f'- Native products commit: `{a.products_commit}`.',
      '- Root documentation commits made later are not substituted for the compiled source identity.', '',
      '| Entry | Pages | Pinned native PDF |','|---|---:|---|']
    for stem,label in [('rigidity','Principal article'),('main','Full technical manuscript'),('two_collision','Two-collision companion')]:
        x=products[stem];lines.append(f"| {label} | {x['pages']} | [{stem}.pdf]({x['url']}) |")
    lines+=['','The entries overlap; their page counts must not be added as independent mathematical output.','',
      f'[Complete source]({REPO}/tree/{a.source_commit}/{P}) · '+
      f'[Response to referee]({REPO}/blob/{a.source_commit}/{P}/RESPONSE_TO_REFEREE_V75.md) · '+
      f'[Historical derivation audit]({REPO}/blob/{a.source_commit}/{P}/HISTORICAL_DERIVATION_AUDIT_V75.md)', '',
      '## Source retention and validation', '',
      'All 992 original source paths survive. Seven edited originals have byte-exact archived copies. All 1,423 previously active mathematical labels remain reachable from the three entries. Two principal proof slices are exact prefixes of unchanged full technical modules. The six external principal aliases are extension/comparison references, not missing premises of the principal smooth theorem.', '',
      f'Build logs, frozen source archive, recorder inputs, hashes, and the fetched-object attestation are in [`{dest}`]({REPO}/tree/{a.products_commit}/{dest}). The attestation itself is added on the native branch after the product commit; it names the product commit verified, rather than asserting a self-referential hash.', '',
      'Finite algebra/source diagnostics and native compilation are distinct from theorem correctness and editorial significance. No journal acceptance or independent formal proof certification is claimed. The visual record is supplied separately after artifact retrieval.', '',
      '## Main changes', '',
      'One principal theorem replaces successive nested introductory headlines. The complete central proof is internal to the principal article. Observation refinements retain their full proofs as consequences; the two-offset finite-preparation appendix preserves normal-incidence coverage. Analytic/global/lattice/coarsening routes remain in the full technical entry. The old full introduction now includes the moment roadmap, and a proved, attributed affine example displays gate/obliquity conditioning.', '']
    Path('A2_REVISION_V75_REVIEW_READY.md').write_text('\n'.join(lines))
    readme=Path('README.md')
    old=readme.read_text()
    marker='<!-- A2-V75-REVIEW-ENTRY -->'
    if marker not in old:
        readme.write_text(marker+'\n## Current A2 referee entry: revision 75\n\n'+
          '[Source-matched manuscript, full technical entry, response and native products](A2_REVISION_V75_REVIEW_READY.md). '+
          'The v74 history below is retained; the compiled v75 source and native commits are pinned in the new entry.\n\n'+old)

if __name__=='__main__':main()
