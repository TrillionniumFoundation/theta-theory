#!/usr/bin/env python3
"""Prepare review metadata only after actual tests and complete compilation."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BRANCH='revision/a2-v161-multiple-incidence-contact-singularities-2026-09-25'
REL='papers/A2-v17-boundary-information-coarsening/article/v161'
REVIEW='596df442f9155c79b6b33378c0a208259385b2ae'

def main():
    source=os.environ['GITHUB_SHA']
    if os.environ['GITHUB_REF_NAME']!=BRANCH:raise RuntimeError('Wrong branch')
    r=json.loads((HERE/'BUILD_RECEIPT_V161.json').read_text())
    c=json.loads((HERE/'EXACT_CHECKS_V161.json').read_text())
    if not(r['compiled'] and c['all_checks_pass'] and c['inherited_v160_suite_actually_rerun']):raise RuntimeError('Full build and inherited run required')
    if r['source_commit']!=source or not r['all_predecessor_math_blocks_retained_byte_for_byte']:raise RuntimeError('Source or preservation mismatch')
    index=json.loads((HERE/'THEOREM_INDEX_V161.json').read_text())
    render=HERE/'render-audit';render.mkdir(exist_ok=True)
    pages={name:{1} for name in ('geometry','reconstruction','divisor-geometry')}
    chosen={'thm:multiple-incidence-v161','thm:contact-hilbert-v161','prop:contact-deformations-v161','thm:stable-tail-v161','thm:boundary-stack-v161','prop:relative-obstructions-v161'}
    for label in chosen:
        if label not in index:raise RuntimeError('Missing new theorem '+label)
        info=index[label];page=int(info['page']);name=info['paper'];pages[name].update((page,page+1))
    for name,pp in pages.items():
        for page in sorted(p for p in pp if p<=r['outputs'][name]['pages']):
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1350','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
    previous=HERE/'PREVIOUS_ROOT_ENTRY.md'
    if not previous.exists():shutil.copyfile(ROOT/'CURRENT_REVIEW_ENTRY.md',previous)
    shutil.copyfile(ROOT/'reviews/a2-v160-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md',HERE/'CONTROLLING_REFEREE_REPORT_V160.md')
    text=f'''# A2 revision 161 — controlling referee entry

Branch: `{BRANCH}`.
Authored source commit: `{source}`.
Controlling complete-v160 report: `{REVIEW}`.
Preserved complete predecessor: `58c33453bf01d1f73083cb744d0479ecdc3dcf2f`.

## Complete reading objects

'''
    for title,name in [('Paper I — Finite failure schemes and the reconstruction of quadratic pencils','reconstruction'),('Paper II — Power ideals and the Hilbert boundary of quadratic pencils','divisor-geometry'),('Preservation master — not a third submission','geometry')]:
        text+=f'**{title}.** {r["outputs"][name]["pages"]} pages. [PDF]({REL}/{name}.pdf) · [complete standalone LaTeX]({REL}/{name}.tex).\n\n'
    text+=f'''Paper I has a seven-section main inverse proof; its full applications
and prior extensions are in appendices. Paper II has a six-section main
route ending in the multiple-incidence and higher-contact theorems;
all earlier power, spectral, collision and reciprocal-fibre extensions
remain in appendices. Embedded companion references are stable and do
not require an external auxiliary file.

[All 30 referee responses]({REL}/RESPONSE_TO_V160_REPORT.md) ·
[Theorem/page index]({REL}/THEOREM_INDEX_V161.json) ·
[Primary-source comparison]({REL}/LITERATURE_AUDIT_V161.md) ·
[Build receipt]({REL}/BUILD_RECEIPT_V161.json) ·
[Preservation audit]({REL}/NONDELETION_V161.json) ·
[Exact checks]({REL}/EXACT_CHECKS_V161.json).

## Principal changes

The full reduced corank-two incidence open now has a normalized Hilbert
modification given by a Fitting-ideal blow-up. Its entire fibre at k
incidences is (P^1)^k. Independence is proved from the distinct spectral
radicals, not assumed generically. Every symmetric Jordan contact slice
of order m >= 2 has an explicitly computed thick tail, length-m
attachment, A_(m-1) graph singularity and degree-m stable-map tail after
ramified base change. The effective stack, multi-Rees equations and
relative Artin lifting conditions are stated in their precise categories.

The full ambient nonreduced and higher-corank boundary is not claimed
classified by the slice theorem. The original all-pencil sharp inverse
and all inherited statements retain their scopes. The envelope is not a
subquotient of the original algebra, and the recovered pencil line is
an essential intermediate object of the boundary interpretation.

## Preservation and verification

All {r['predecessor_labels']} predecessor labels and
{r['predecessor_math_blocks']} mathematical environment blocks are
retained. The current master has {r['current_labels']} labels and
{r['current_math_blocks']} blocks. The audit checks old mathematical
blocks byte for byte and allocates the body exactly once across the
companions. All three previous introductions and the former root entry
are archived. The full inherited v160 check chain was actually executed.
Finite computations are audits of explicit equations, not certification
of universal proofs, historical priority or editorial acceptance.
The Ballico 1993 theorem/proof-level comparison remains incomplete in
both papers; a separate available 1996 theorem is not substituted for it.

The authored input commit above precedes the materialization commit
containing the complete sources and PDFs. After remote read-back,
`{REL}/PUBLICATION_SEAL_V161.json` records the output commit and the
checks actually performed. No self-referential commit hash is asserted.
'''
    (ROOT/'CURRENT_REVIEW_ENTRY.md').write_text(text)
    (HERE/'README.md').write_text(text.replace(f']({REL}/','](')+'''\n## Reproduction\n\nFrom this directory in a full branch checkout:\n\n```sh\npython3 check_v161.py\npython3 assemble_v161.py --build\n```\n\nThe complete `.tex` files can also be compiled independently with pdflatex.\n''')
    manifest=dict(revision=161,source_commit=source,workflow_run=os.environ.get('GITHUB_RUN_ID'),branch=BRANCH,outputs=r['outputs'],rendered_files=sorted(p.name for p in render.glob('*.png')),visual_inspection_asserted_by_script=False)
    (HERE/'PUBLICATION_MANIFEST_V161.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Prepared complete v161 publication entry and rendered theorem pages.')
if __name__=='__main__':main()
