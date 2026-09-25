#!/usr/bin/env python3
"""Prepare source-bound review metadata only after full checks and compilation."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BRANCH='revision/a2-v163-embedded-comparison-contact-fibres-2026-09-25'
REL='papers/A2-v17-boundary-information-coarsening/article/v163'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if os.environ['GITHUB_REF_NAME']!=BRANCH:raise RuntimeError('Wrong publication branch')
    source=os.environ['GITHUB_SHA']
    r=json.loads((HERE/'BUILD_RECEIPT_V163.json').read_text());c=json.loads((HERE/'EXACT_CHECKS_V163.json').read_text())
    assert r['compiled'] and r['source_commit']==source
    assert r['all_predecessor_math_blocks_retained_byte_for_byte'] and r['body_partitioned_exactly_once']
    assert c['all_checks_pass'] and c['inherited_v162_suite_rerun']
    assert (r['predecessor_labels'],r['predecessor_math_blocks'])==(490,325)
    assert (r['current_labels'],r['current_math_blocks'])==(520,348)
    response=(HERE/'RESPONSE_TO_V162_REPORT.md').read_text()
    assert [int(x) for x in re.findall(r'^### (\d+)\.',response,re.M)]==list(range(1,45))
    for name,item in r['outputs'].items():
        assert item['clean_references_and_no_overfull_hboxes']
        assert sha(HERE/(name+'.pdf'))==item['pdf_sha256']
        assert sha(HERE/(name+'.tex'))==item['source_sha256']
    old=ROOT/'CURRENT_REVIEW_ENTRY.md'
    if not (HERE/'PREVIOUS_ROOT_ENTRY.md').exists():shutil.copyfile(old,HERE/'PREVIOUS_ROOT_ENTRY.md')
    report=ROOT/'reviews/a2-v162-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md'
    shutil.copyfile(report,HERE/'CONTROLLING_REFEREE_REPORT_V162.md')
    text=f'''# A2 revision 163 — controlling review entry

Branch: `{BRANCH}`.
Authored source commit: `{source}`.
Controlling v162 report: `7e9c057907cc4502858a54f32ab0c0cfa264680f`.
Complete reviewed baseline: `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`.

## Complete reading objects

'''
    for title,name in [('Paper I: Finite failure schemes and the reconstruction of quadratic pencils','reconstruction'),('Paper II: Power ideals and the Hilbert boundary of quadratic pencils','divisor-geometry'),('Complete preservation master, not a third submission','geometry')]:
        text+=f'**{title}** — {r["outputs"][name]["pages"]} pages. [PDF]({REL}/{name}.pdf); [independent complete LaTeX]({REL}/{name}.tex).\n\n'
    text+=f'''## Main revision

The fixed-target comparison is stated separately as an equivalence of
completed embedded quotient functors, retaining the coefficient base and
undoing parameter-dependent congruences. A Hilbert–Burch chart with a
regular inverse identifies the whole first nonreduced fibre: its reduced
components are P^4 and F_2, meeting along the doubled-line P^1. The exact
local ideal `(eA,eB,e^2C)` also records a nonzero square-zero nilradical.
The proof exhausts the proper fibre by connectedness; it is not another
selected family of limits.

For r distinct length-two contacts and s length-one contacts, with
arbitrary larger Smith exponents and no higher corank, the complete
actual pencil fibre is `X_2^r x (P^1)^s`. All `2^r` reduced components,
their dimensions and intersections, and the exact nilpotence order `r+1`
are determined. Higher lengths have a separately labelled conjecture,
not an asserted full classification. The failure-family application is
explicitly through the effective inverse, not the raw Artin-algebra stack.

[All 44 responses]({REL}/RESPONSE_TO_V162_REPORT.md).
[Theorem/page index]({REL}/THEOREM_INDEX_V163.json).
[Build receipt]({REL}/BUILD_RECEIPT_V163.json).
[Preservation]({REL}/NONDELETION_V163.json).
[Exact audits]({REL}/EXACT_CHECKS_V163.json).
[Primary-source record]({REL}/LITERATURE_AUDIT_V163.md).

All 490 predecessor labels and 325 mathematical environment blocks are
retained; the current master has 520 labels and 348 blocks. Preservation
of the predecessor mathematical blocks is checked byte for byte and the
body is allocated exactly once between the two companions. Replaced
front matter and the old root entry are archived. The sources embed
stable companion references; no external companion auxiliary file is needed.

The authored source commit precedes the separate materialization commit
containing complete sources, PDFs and receipts. Remote read-back is bound
to that output commit in `{REL}/PUBLICATION_SEAL_V163.json` after verification.
No file claims to know its own future commit hash.

The full inherited v162 check chain was executed by this build. Tests
are exact finite audits, not certificates of general proofs, novelty or
editorial acceptance. No new external independent proof audit of Paper I
has been obtained. Ballico 1993 remains unavailable at theorem/proof level;
this limitation is retained in both papers. The original all-pencil
sharp inverse and singular-pencil invariant results have not been restricted.
'''
    old.write_text(text);(HERE/'README.md').write_text(text.replace(f']({REL}/',']('))
    index=json.loads((HERE/'THEOREM_INDEX_V163.json').read_text())
    render=HERE/'render-audit';render.mkdir(exist_ok=True)
    pages={'reconstruction':{1},'divisor-geometry':{1},'geometry':{1}}
    for label,item in index.items():
        if label.endswith('v163') and label.startswith(('thm:','prop:','lem:','cor:')):
            page=int(item['page']);pages[item['paper']].add(page)
            if label.startswith('thm:'):pages[item['paper']].add(page+1)
    for name,pp in pages.items():
        for page in sorted(pp):
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1400','-singlefile','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
    manifest=dict(revision=163,branch=BRANCH,source_commit=source,workflow_run=os.environ.get('GITHUB_RUN_ID'),outputs=r['outputs'],rendered_pages={k:sorted(v) for k,v in pages.items()},visual_inspection_claimed_by_script=False,
                  files={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in HERE.iterdir() if p.is_file() and p.suffix in ('.tex','.pdf','.py','.md','.json') and p.name!='PUBLICATION_MANIFEST_V163.json'})
    (HERE/'PUBLICATION_MANIFEST_V163.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Complete v163 publication metadata prepared; rendered pages still require visual inspection.')
if __name__=='__main__':main()
