#!/usr/bin/env python3
"""Prepare publication after complete compilation and the full inherited suite."""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL='papers/A2-v17-boundary-information-coarsening/article/v164'
BRANCH='revision/a2-v164-collision-wall-crossing-2026-09-26'
REVIEW='7e9c057907cc4502858a54f32ab0c0cfa264680f'
BASE='40a72ddfd85e16363385a1b64b922d61055e875c'
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->None:
    source=os.environ['GITHUB_SHA']
    if os.environ['GITHUB_REF_NAME']!=BRANCH:raise RuntimeError('Wrong publication branch')
    r=json.loads((HERE/'BUILD_RECEIPT_V164.json').read_text())
    c=json.loads((HERE/'EXACT_CHECKS_V164.json').read_text())
    if not (r['compiled'] and r['all_predecessor_math_blocks_retained_byte_for_byte'] and r['body_partitioned_exactly_once']):
        raise RuntimeError('Complete compiled preservation checks required')
    if not (c['all_checks_pass'] and c['inherited_v163_suite_rerun']):
        raise RuntimeError('Actual complete inherited checks required')
    if r['source_commit']!=source:raise RuntimeError('Source commit mismatch')
    if r['predecessor_labels']!=520 or r['predecessor_math_blocks']!=348:
        raise RuntimeError('Wrong predecessor object')
    response=(HERE/'RESPONSE_TO_V162_REPORT.md').read_text()
    if list(map(int,re.findall(r'^### (\d+)\.',response,re.M)))!=list(range(1,45)):
        raise RuntimeError('All 44 numbered responses required')
    for name,rec in r['outputs'].items():
        if not rec['clean_references_and_no_overfull_hboxes'] or sha(HERE/(name+'.pdf'))!=rec['pdf_sha256']:
            raise RuntimeError('PDF verification failed for '+name)
    original=ROOT/'CURRENT_REVIEW_ENTRY.md'
    previous=HERE/'PREVIOUS_ROOT_ENTRY.md'
    if not previous.exists():shutil.copyfile(original,previous)
    shutil.copyfile(ROOT/'reviews/a2-v162-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md',HERE/'CONTROLLING_REFEREE_REPORT_V162.md')
    shutil.copyfile(HERE.parent/'v163'/'RESPONSE_TO_V162_REPORT.md',HERE/'PREVIOUS_RESPONSE_V163.md')
    render=HERE/'render-audit';render.mkdir(exist_ok=True)
    index=json.loads((HERE/'THEOREM_INDEX_V164.json').read_text())
    pages={name:{1} for name in r['outputs']}
    for label,rec in index.items():
        if label.endswith('v164') and label.startswith(('thm:','cor:','prop:')):
            start=int(rec['page']);name=rec['paper']
            pages[name].update(range(start,min(start+2,r['outputs'][name]['pages'])+1))
    rendered={}
    for name,selected in pages.items():
        rendered[name]=sorted(selected)
        for page in sorted(selected):
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1500','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
    text=f'''# A2 revision 164 — controlling review entry

Branch: `{BRANCH}`.
Authored source commit: `{source}`.
Latest controlling v162 referee report: `{REVIEW}`.
Complete post-report v163 baseline: `{BASE}`.
The reviewed v162 tip is `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`.

## Complete reading objects

'''
    titles={'reconstruction':'Paper I: Finite failure schemes and the reconstruction of quadratic pencils','divisor-geometry':'Paper II: Power ideals and the Hilbert boundary of quadratic pencils','geometry':'Complete preservation master, not a third submission'}
    for name,title in titles.items():
        text+=f'**{title}** — {r["outputs"][name]["pages"]} pages. [PDF]({REL}/{name}.pdf); [independent complete LaTeX]({REL}/{name}.tex).\n\n'
    text+='''## Main revision

The collision family separates the full pullback of the normalized total
Hilbert graph from the schematic closure of its generic fibres. The
horizontal space is a smooth quotient of the blow-up of the ordered
direction product along its central diagonal. Its special divisor is
`F_2 + 2 P^2`; the full pullback has an additional vertical `P^4`, attached
along the singular-conic plane. Its exact base-torsion is that plane's
ideal sheaf inside `P^4`. Ordering the roots and normalizing gives the
reduced normal-crossing model. This is a degeneration of parameter spaces,
not a replacement of nonreduced Hilbert curves by stable maps.

The nilradical of the complete first-contact fibre is identified globally
as `j_* O_(P^2)(-1)`, with square zero; no splitting of the algebra extension
is asserted. Independent collisions have explicit component multiplicities.
An explicit 4-by-4 symmetric pencil realizes the collision in a fixed
complete-quadric target. Its application to failure algebras remains through
the effective inverse, not the unrestricted raw Artin-algebra stack.

'''
    links=[('All 44 current referee responses','RESPONSE_TO_V162_REPORT.md'),('Archived v163 response','PREVIOUS_RESPONSE_V163.md'),('Theorem/page index','THEOREM_INDEX_V164.json'),('Build receipt','BUILD_RECEIPT_V164.json'),('Preservation audit','NONDELETION_V164.json'),('Exact finite audits','EXACT_CHECKS_V164.json'),('Primary-source comparison','LITERATURE_AUDIT_V164.md')]
    text+='\n'.join(f'[{title}]({REL}/{name}).' for title,name in links)+'\n\n'
    text+=f'''All {r['predecessor_labels']} predecessor labels and {r['predecessor_math_blocks']}
mathematical environment blocks are retained. The current master has
{r['current_labels']} labels and {r['current_math_blocks']} blocks. Preservation
is checked byte for byte for mathematical blocks; the body is partitioned
exactly once across the companions. Replaced front matter and the old root
entry are archived. Each complete source embeds stable companion references.

The authored source commit above precedes the separate materialization
commit with complete PDFs, sources and receipts. The latter is recorded
in `{REL}/PUBLICATION_SEAL_V164.json` only after actual remote read-back.
No file asserts its own future commit hash. The workflow renders pages
for inspection but rendering alone is not recorded as visual inspection.

## Reproduce

From a full checkout of this branch, run:

```sh
python3 {REL}/check_v164.py
python3 {REL}/assemble_v164.py --build
```

The three complete `.tex` files also compile individually without external
companion auxiliary files. The scripts require the preserved historical
inputs in the repository; the independently compiling sources do not.

The remote build actually runs the inherited v163 chain. Finite audits do
not certify general proofs, novelty or journal acceptance. No new external
independent audit of Paper I has been obtained. The Ballico 1993 full-text
comparison remains incomplete and is disclosed inside both papers. The
higher-contact and higher-corank full Hilbert classification is not claimed
complete; the original all-pencil inverse and singular-pencil invariants
retain their domains.
'''
    original.write_text(text)
    (HERE/'README.md').write_text(text.replace(f']({REL}/',']('))
    manifest={'revision':164,'branch':BRANCH,'source_commit':source,'controlling_review_commit':REVIEW,'baseline_commit':BASE,'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'outputs':r['outputs'],'rendered_pages':rendered,'rendering_alone_is_visual_inspection':False,'all_44_responses_present':True,'files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(HERE.iterdir()) if p.is_file() and p.suffix in ('.tex','.pdf','.py','.md','.json') and p.name!='PUBLICATION_MANIFEST_V164.json'}}
    (HERE/'PUBLICATION_MANIFEST_V164.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Prepared source-bound complete v164 publication and rendered inspection pages.')
if __name__=='__main__':main()
