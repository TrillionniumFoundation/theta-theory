#!/usr/bin/env python3
"""Prepare complete review outputs after verified compilation; never publish partial drafts."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BRANCH='revision/a2-v162-versal-contact-neighborhoods-2026-09-25'
REL='papers/A2-v17-boundary-information-coarsening/article/v162'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if os.environ['GITHUB_REF_NAME']!=BRANCH:raise RuntimeError('Wrong publication branch')
    source=os.environ['GITHUB_SHA']
    r=json.loads((HERE/'BUILD_RECEIPT_V162.json').read_text());c=json.loads((HERE/'EXACT_CHECKS_V162.json').read_text())
    assert r['compiled'] and r['source_commit']==source
    assert r['all_predecessor_math_blocks_retained_byte_for_byte'] and r['body_partitioned_exactly_once']
    assert c['all_checks_pass'] and c['inherited_v161_suite_actually_rerun']
    assert r['predecessor_labels']==453 and r['predecessor_math_blocks']==299
    assert r['current_labels']==490 and r['current_math_blocks']==325
    response=(HERE/'RESPONSE_TO_V161_REPORT.md').read_text()
    assert [int(x) for x in re.findall(r'^### (\d+)\.',response,re.M)]==list(range(1,39))
    for name,item in r['outputs'].items():
        assert item['clean_references_and_no_overfull_hboxes']
        assert sha(HERE/(name+'.pdf'))==item['pdf_sha256']
        assert sha(HERE/(name+'.tex'))==item['source_sha256']
    old=ROOT/'CURRENT_REVIEW_ENTRY.md'
    if not (HERE/'PREVIOUS_ROOT_ENTRY.md').exists():shutil.copyfile(old,HERE/'PREVIOUS_ROOT_ENTRY.md')
    report=ROOT/'reviews/a2-v161-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md'
    shutil.copyfile(report,HERE/'CONTROLLING_REFEREE_REPORT_V161.md')
    text=f'''# A2 revision 162 — controlling review entry

Branch: `{BRANCH}`.
Authored source commit: `{source}`.
Controlling v161 report: `3d22c10f34d889081000232bb8f2241d5988fc37`.
Complete reviewed baseline: `9e3b6639021a5f1fdb725961c7a7b6bb9cf55779`.

## Two complete reading objects

'''
    for title,name in [('Paper I: Finite failure schemes and the reconstruction of quadratic pencils','reconstruction'),('Paper II: Power ideals and the Hilbert boundary of quadratic pencils','divisor-geometry'),('Complete preservation master, not a third submission','geometry')]:
        text+=f'**{title}** — {r["outputs"][name]["pages"]} pages. [PDF]({REL}/{name}.pdf); [independent full LaTeX]({REL}/{name}.tex).\n\n'
    text+=f'''## Mathematical reading route

Paper II, Theorems 6.2, 7.1, 7.2 and 8.1: full formal contact parameters;
a Euclidean open Hilbert chart with a regular inverse; ambient primitive
jet-tail neighbourhoods and their exact gcd collision law; and an actual
non-equidimensional fibre at contact type (2,2). The latter has a
2-dimensional component and a distinct component of dimension at least 4.
The primitive jet open is not asserted to be the entire proper fibre.

Paper II, Appendix T: the exact incidence/descent, normality, Artin
coefficient and ramified-normalization details requested in the report.
Paper I, Appendix F: an algebraic envelope target, chart-invariant relative
cotangent obstruction, and the explicitly effective family application.
The sharp inverse and all inherited mathematical results remain intact.

[All 38 referee responses]({REL}/RESPONSE_TO_V161_REPORT.md).
[Theorem/page index]({REL}/THEOREM_INDEX_V162.json).
[Build receipt]({REL}/BUILD_RECEIPT_V162.json).
[Preservation audit]({REL}/NONDELETION_V162.json).
[Exact finite checks]({REL}/EXACT_CHECKS_V162.json).
[Primary-source comparison]({REL}/LITERATURE_AUDIT_V162.md).

All 453 predecessor labels and all 299 predecessor mathematical blocks
are retained byte for byte. The current master has 490 labels and 325
mathematical blocks; the body is allocated exactly once across the two
companions. All three replaced front matters and the old root entry are
archived. Each focused source embeds stable companion references.

The source commit above precedes the build commit containing complete
PDFs, sources and receipts. After remote read-back the distinct output
commit is recorded in `{REL}/PUBLICATION_SEAL_V162.json`. The seal is not
a self-referential assertion about its own future commit hash.

The full inherited v161 check chain was executed by this build. Finite
checks do not certify the general proofs. No new independent external
proof audit of Paper I was obtained. The Ballico 1993 theorem/proof-level
comparison remains incomplete and is disclosed inside both papers.
No full classification of every global Hilbert fibre, pre-reconstruction
internal boundary operation, historical priority, or editorial acceptance
is asserted.
'''
    old.write_text(text)
    (HERE/'README.md').write_text(text.replace(f']({REL}/',']('))
    index=json.loads((HERE/'THEOREM_INDEX_V162.json').read_text());render=HERE/'render-audit';render.mkdir(exist_ok=True)
    pages={'reconstruction':{1},'divisor-geometry':{1},'geometry':{1}}
    for label,item in index.items():
        if label.endswith('v162') and label.startswith(('thm:','prop:','cor:')):
            page=int(item['page']);pages[item['paper']].add(page)
            if label.startswith('thm:'):pages[item['paper']].add(page+1)
    for name,pp in pages.items():
        for page in sorted(pp):
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1400','-singlefile','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
    manifest=dict(revision=162,branch=BRANCH,source_commit=source,workflow_run=os.environ.get('GITHUB_RUN_ID'),outputs=r['outputs'],rendered_pages={k:sorted(v) for k,v in pages.items()},visual_inspection_claimed_by_script=False,files={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in HERE.iterdir() if p.is_file() and p.suffix in ('.tex','.pdf','.py','.md','.json') and p.name!='PUBLICATION_MANIFEST_V162.json'})
    (HERE/'PUBLICATION_MANIFEST_V162.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Complete v162 publication metadata prepared; rendered pages require visual inspection.')
if __name__=='__main__':main()
