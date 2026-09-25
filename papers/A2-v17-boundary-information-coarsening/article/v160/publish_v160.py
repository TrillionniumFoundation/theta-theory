#!/usr/bin/env python3
"""Prepare publication metadata after checks and complete PDF compilation."""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BRANCH='revision/a2-v160-intrinsic-blowup-boundary-2026-09-25'
REL='papers/A2-v17-boundary-information-coarsening/article/v160'
REVIEW='b81ba4a2fac700f17b26163079bd17ef54947509'
def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->None:
    source=os.environ['GITHUB_SHA']
    if os.environ['GITHUB_REF_NAME']!=BRANCH:raise RuntimeError('Wrong publication branch')
    receipt=json.loads((HERE/'BUILD_RECEIPT_V160.json').read_text())
    checks=json.loads((HERE/'EXACT_CHECKS_V160.json').read_text())
    if not receipt['compiled'] or not checks['all_checks_pass'] or not checks['inherited_v159_suite_rerun']:
        raise RuntimeError('Complete build and actual inherited checks are required')
    if receipt['source_commit']!=source:raise RuntimeError('Source lock mismatch')
    labels={};wanted={'thm:intrinsic-envelope-v158','prop:universal-envelope-v159','thm:failure-incidence-v160','lem:incidence-centre-v160','thm:incidence-blowup-v160','prop:exceptional-powers-v160','ex:tangent-limit-v160','thm:ordinary-fibres-v159','thm:boundary-moduli-v159','thm:singular-complete-data-v158'}
    render=HERE/'render-audit';render.mkdir(exist_ok=True)
    for name in ('reconstruction','divisor-geometry','geometry'):
        pages={1}
        for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',(HERE/(name+'.aux')).read_text()):
            if m.group(1) in wanted and name!='geometry':
                labels[m.group(1)]={'paper':name,'number':m.group(2),'page':int(m.group(3))}
                if 'v160' in m.group(1):pages.add(int(m.group(3)))
        for page in sorted(pages):
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1400','-png','-singlefile',str(HERE/(name+'.pdf')),str(render/(name+'-page-'+str(page)))],check=True)
    (HERE/'THEOREM_INDEX_V160.json').write_text(json.dumps(labels,indent=2)+'\n')
    original=ROOT/'CURRENT_REVIEW_ENTRY.md'
    previous=HERE/'PREVIOUS_ROOT_ENTRY.md'
    if not previous.exists():shutil.copyfile(original,previous)
    report=ROOT/'reviews/a2-v157-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md'
    shutil.copyfile(report,HERE/'CONTROLLING_REFEREE_REPORT_V157.md')
    out=receipt['outputs']
    entry=f'''# A2 revision 160: controlling review entry

Branch: `{BRANCH}`.
Mathematical source commit: `{source}`.
Controlling referee report: `{REVIEW}`,
`reviews/a2-v157-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`.
Preserved post-review derivations: v158 and v159, through
`a27bd7fcea5c4ef04cdd8748411cdeab7ba42855`.

## The two review objects

**Paper I — Finite failure schemes and the reconstruction of quadratic pencils.**
[Complete PDF]({REL}/reconstruction.pdf),
[complete source]({REL}/reconstruction.tex), {out['reconstruction']['pages']} pages.

**Paper II — Intrinsic power geometry and the boundary of quadratic pencils.**
[Complete PDF]({REL}/divisor-geometry.pdf),
[complete source]({REL}/divisor-geometry.tex), {out['divisor-geometry']['pages']} pages.

The [preservation master]({REL}/geometry.pdf),
{out['geometry']['pages']} pages, contains all mathematics of both papers.
It is not a third submission. Each focused source has embedded, stable
companion references and can be compiled independently.

## Revision and evidence

[Point-by-point response]({REL}/RESPONSE_TO_V157_REPORT.md).
[Theorem and page index]({REL}/THEOREM_INDEX_V160.json).
[Build receipt]({REL}/BUILD_RECEIPT_V160.json).
[Nondeletion audit]({REL}/NONDELETION_V160.json).
[Exact finite checks]({REL}/EXACT_CHECKS_V160.json).
[Primary-source audit]({REL}/LITERATURE_AUDIT_V160.md).

The source commit above contains authored inputs. The subsequent build
commit materializes the complete sources, PDFs and receipts; its SHA is
recorded separately in `{REL}/PUBLICATION_SEAL_V160.json` after remote
verification. No self-referential commit hash is asserted inside a commit.
The former root entry is archived in `{REL}/PREVIOUS_ROOT_ENTRY.md`.

The new result identifies the entire normalized Hilbert incidence space
on the simple corank-two open in every dimension with the blow-up of a
smooth codimension-two centre. It computes the full exceptional fibre,
the nodal family and all exceptional power systems. The centre's ideal,
Rees algebra and first normal directions are recovered from failure
multiplication. The universal ideal theorem, singular-pencil data and
arbitrary-multiplicity ordinary collision theory remain intact.

All 405 labels and 268 mathematical blocks of the locked v159 master
are retained; the new master has 421 labels and 277 blocks. The audit
checks predecessor mathematical blocks byte for byte and partitions the
body exactly once between the two papers. Earlier v157 and v158 content
is retained transitively. Finite computations supplement the written
proofs; they do not certify general theorems, historical priority or
journal acceptance. The Ballico 1993 full-text comparison remains
incomplete and is disclosed inside both papers.
'''
    original.write_text(entry)
    # Relative links in the root index are rewritten for the article README.
    (HERE/'README.md').write_text(entry.replace(f']({REL}/',']('))
    manifest={'revision':160,'source_commit':source,'controlling_review_commit':REVIEW,
              'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'branch':BRANCH,
              'files':{p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(HERE.iterdir()) if p.is_file() and p.suffix in ('.tex','.pdf','.py','.json','.md') and p.name!='PUBLICATION_MANIFEST_V160.json'},
              'rendered_pages':sorted(p.name for p in render.glob('*.png')),
              'visual_human_or_assistant_inspection_asserted_by_script':False}
    (HERE/'PUBLICATION_MANIFEST_V160.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Prepared source-bound v160 publication metadata and rendered pages.')
if __name__=='__main__':main()
