#!/usr/bin/env python3
"""Package the actual R76 source-SHA execution, including failed development evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import shutil
import stat
import subprocess
import zipfile

BASE=Path('/workspace/scratch/f856e3d63ac5')
REPO=BASE/'theta-r76-work'
PAPER='papers/General-Theta-Foundations-I-restart/r76-robust-memory-realization'
SOURCE=REPO/PAPER
PUB=REPO/(PAPER+'-publication')
DELIVERY=BASE/'r76-delivery'
BUILD=BASE/'r76-build/strict-corrected-source'
SHA='891643799f2dfb2737ad5c147bf8def2d460630b'
TREE='38930b53fb64ca4ca1ebcc7e20919f2ed0ba74ae'
BRANCH='revision/general-theta-r76-robust-memory-realization-20261021'
PREFIX='General_Theta_Foundations_I_R76'
PART=6*1024*1024

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def h(data):return hashlib.sha256(data).hexdigest()
def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def identity(path,name=None):
    data=path.read_bytes()
    return {'path':name or path.name,'bytes':len(data),'sha256':h(data)}
def copy(src,dest):
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
def regular(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
def write_zip(path,records,prefix,epoch):
    date=dt.datetime.fromtimestamp(epoch,dt.timezone.utc)
    stamp=(date.year,date.month,date.day,date.hour,date.minute,date.second//2*2)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name,src,mode in records:
            item=zipfile.ZipInfo(prefix+'/'+name,stamp);item.create_system=3;item.external_attr=int(mode,8)<<16
            archive.writestr(item,src.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)

receipt=json.loads((BUILD/'BUILD_RECEIPT.json').read_text())
require(receipt['status']=='PASS' and receipt['mode']=='strict','No actual strict PASS')
require(receipt['declared_source_commit']==SHA and receipt['source_git_tree_after']==TREE,'Wrong source identity')
require(receipt['source_files_verified']==507 and receipt['diagnostic_suite_count']==23,'Incomplete source or diagnostics')
require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==SHA,'Local source HEAD changed')
manifest=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_text())
require(h((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==receipt['source_manifest_sha256'],'Source manifest changed')
PUB.mkdir(exist_ok=True)
require(not any(PUB.iterdir()),'Publication target must be empty on first assembly')
(PUB/'evidence').mkdir();(PUB/'archives').mkdir()
for f in ['BUILD_RECEIPT.json','THEOREM_INDEX.json']:copy(BUILD/f,PUB/f)
for doc in receipt['documents']:
    for k in ['file','text_file']:copy(BUILD/doc[k],PUB/doc[k])
for name in ['RESPONSE_TO_REFEREE.md','PROOF_AUDIT.md','RESEARCH_STATUS.md','LITERATURE_AND_PRIORITY.md','PRESERVATION_MAP.md','SOURCE_PROVENANCE.md','THEOREM_MAP.md','THEOREM_DEPENDENCIES_R76.md','THEOREM_DEPENDENCIES.json']:
    copy(SOURCE/name,PUB/name)
copy(SOURCE/'provenance/R65_REFEREE_REPORT.md',PUB/'CONTROLLING_R65_REPORT.md')
for name in ['restore_archives.py','verify_received.py']:copy(BASE/'r76-publication-tools'/name,PUB/name)
for f in regular(BASE/'r76-publication-tools'):
    if f.name not in {'restore_archives.py','verify_received.py'}:copy(f,PUB/'evidence/publication-helper'/f.relative_to(BASE/'r76-publication-tools'))
for f in regular(DELIVERY/'remote'):copy(f,PUB/'evidence/remote'/f.relative_to(DELIVERY/'remote'))
for name in ['SOURCE_COMMIT_RECEIPT.json','CORRECTED_SOURCE_COMMIT_RECEIPT.json']:copy(DELIVERY/name,PUB/'evidence/remote'/name)
copy(Path(__file__),PUB/'evidence/build_publication.py')

visual={}
for doc in receipt['documents']:
    folder='visual-main-draft03' if doc['document']=='manuscript' else 'visual-retained-draft02'
    qa=BASE/'r76-build'/folder
    reviewed=(BASE/'r76-build'/('draft03' if doc['document']=='manuscript' else 'draft02')/doc['file'])
    require(h(reviewed.read_bytes())==doc['sha256'],'Final PDF is not identical to visually reviewed PDF')
    visual[doc['document']]={'pdf_sha256':doc['sha256'],'pages':doc['pages'],'byte_identical_to_reviewed_pdf':True,'reviewed_pdf':str(reviewed),'review_receipt':folder+'/VISUAL_QA_RECEIPT.json','review_receipt_sha256':h((qa/'VISUAL_QA_RECEIPT.json').read_bytes())}
for folder in ['visual-main-draft02','visual-main-draft03','visual-retained-draft02']:
    for f in (BASE/'r76-build'/folder).iterdir():
        if f.is_file() and f.suffix in {'.json','.md','.txt','.py'}:copy(f,PUB/'evidence/visual'/folder/f.name)
write_json(PUB/'VISUAL_QA_RECEIPT.json',{'schema':'theta.r76.final-pdf-visual-binding.v1','source_commit':SHA,'documents':visual,'status':'Final PDFs byte-identical to the actually visually inspected drafts','coverage':'All252 current pages at overview scale;39 enlarged page inspections across the main,supplement and companion. See individual logs for exact coverage and inherited-pixel comparison.','limitations':['Author-team AI layout inspection, not mathematical proof or human referee review.','Not a microscopic check of every page.','All original renders, actual-view logs and failed-render record are retained in the validation archive.']})

identity_doc={'schema':'theta.r76.publication-identity.v1','source_commit':SHA,'source_paper_tree':TREE,'source_manifest_sha256':receipt['source_manifest_sha256'],'source_files':507,'publication_role':'Child repository delivery of the actual corrected-source strict execution','publication_commit':'The immutable Git commit containing this directory; not self-embedded before creation.','publication_parent':SHA,'revision_branch':BRANCH,'initial_source_commit':'4f61c7a5173416c3532e1b6b967bed8e2a559f08','controlling_report_commit':'358481b21ceeeedb1205ebd30f86982e32a2cb04','build_receipt_sha256':h((BUILD/'BUILD_RECEIPT.json').read_bytes()),'documents':receipt['documents'],'claims':{'local_strict_verification':True,'formal_proof_assistant':False,'independent_human_review':False,'journal_acceptance':False},'hosted_ci_authority':'Actual exact-SHA observations in evidence/remote; local strict execution is not hosted CI.'}
write_json(PUB/'PUBLICATION_IDENTITY.json',identity_doc)

# Source ZIP: exactly the sealed native inventory, including the manifest itself.
archives_dir=DELIVERY/'complete-archives';archives_dir.mkdir(exist_ok=True)
source_zip=archives_dir/(PREFIX+'_Source.zip')
source_rows=[(row['path'],SOURCE/row['path'],row['mode']) for row in manifest['files']]
source_rows.append(('SOURCE_MANIFEST.json',SOURCE/'SOURCE_MANIFEST.json','100644'));source_rows.sort()
require(len(source_rows)==507,'Source ZIP inventory differs')
for name,src,mode in source_rows:
    if name!='SOURCE_MANIFEST.json':
        row=next(x for x in manifest['files'] if x['path']==name)
        require(src.stat().st_size==row['bytes'] and h(src.read_bytes())==row['sha256'],'Source payload changed:'+name)
write_zip(source_zip,source_rows,PREFIX+'_Source',receipt['source_date_epoch'])
write_json(PUB/'evidence/SOURCE_ARCHIVE_CREATION.json',{'source_commit':SHA,'source_paper_tree':TREE,'source_files':507,'archive':identity(source_zip),'exact_native_manifest_inventory':True,'mode_preservation':True,'includes_source_manifest':True})

# Validation ZIP includes every recorded development/strict output and render.
validation_rows=[]
for f in regular(BASE/'r76-build'):
    rel=f.relative_to(BASE/'r76-build')
    name=('build/'+Path(*rel.parts[1:]).as_posix()) if rel.parts[0]=='strict-corrected-source' else rel.as_posix()
    validation_rows.append((name,f,'100644'))
for f in regular(BASE/'r76-publication-tools'):
    validation_rows.append(('publication-helper/'+f.relative_to(BASE/'r76-publication-tools').as_posix(),f,'100755' if f.stat().st_mode&0o111 else '100644'))
for f in regular(DELIVERY/'remote'):
    validation_rows.append(('remote/'+f.relative_to(DELIVERY/'remote').as_posix(),f,'100644'))
validation_rows.sort()
require(len({x[0] for x in validation_rows})==len(validation_rows),'Duplicate validation archive member')
validation_manifest=DELIVERY/'VALIDATION_ARCHIVE_MANIFEST.json'
write_json(validation_manifest,{'schema':'theta.r76.validation-archive.v1','source_commit':SHA,'source_paper_tree':TREE,'build_receipt':'build/BUILD_RECEIPT.json','manifest_excludes_itself':True,'files':[identity(src,name) for name,src,_ in validation_rows],'scope':'Complete current execution, failed initial source run, all native drafts, all rendered pages/contact sheets and author layout records; these are evidence types, not a formal proof.'})
validation_zip=archives_dir/(PREFIX+'_Validation.zip')
write_zip(validation_zip,validation_rows+[('ARCHIVE_MANIFEST.json',validation_manifest,'100644')],PREFIX+'_Validation',receipt['source_date_epoch'])
historical=BASE/'r76-audit/full-scan/HISTORICAL_TEXT_CORPUS.tar.gz'
require(h(historical.read_bytes())=='492d79c1c8cb350d5f8fb19aaa6d73a0670f0144f677d4e14641801424b887e4','Historical corpus mismatch')
archive_records=[]
for role,src,name in [('source',source_zip,source_zip.name),('validation',validation_zip,validation_zip.name),('historical',historical,PREFIX+'_Historical_Text_Corpus.tar.gz')]:
    parts=[]
    with src.open('rb') as stream:
        counter=0
        while raw:=stream.read(PART):
            counter+=1;part=PUB/'archives'/(name+f'.part{counter:03d}');part.write_bytes(raw);parts.append(identity(part,part.relative_to(PUB).as_posix()))
    row={'file':name,'role':role,'bytes':src.stat().st_size,'sha256':h(src.read_bytes()),'format':'ordered raw byte concatenation','parts':parts}
    archive_records.append(row)
write_json(PUB/'archives/ARCHIVE_PARTS.json',{'schema':'theta.r76.lossless-archive-parts.v1','source_commit':SHA,'reason':'Transport-sized ordinary Git blobs preserve the exact complete archive bytes. Ordered raw concatenation restores each archive without omitting source, validation or historical bytes.','archives':archive_records})
(PUB/'archives/README.md').write_text('''# Complete source, validation and historical archives

Each archive is stored as ordered raw byte parts of at most 6 MiB. `ARCHIVE_PARTS.json` fixes the part order, byte counts and SHA-256 values, and the exact complete-archive identity. No content is represented by a placeholder or partial source transfer. Use the receiving helpers in the parent publication directory to authenticate and restore the complete ZIP/TAR.GZ files. The source ZIP contains every sealed native file. The validation ZIP contains all recorded current builds, the failed initial strict attempt, all rendered pages and QA records. The historical TAR.GZ contains all 6,664 authenticated original text objects.
''')

counts={'suites':receipt['diagnostic_suite_count'],'total':receipt['total_checks'],'exact':receipt['exact_finite_checks'],'floating':receipt['floating_finite_checks']}
start=f'''# General Theta Foundations I — R76 independent-referee entry

This is the complete author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, Qian Qi. The original Annals / Acta / Inventiones / JAMS research objective is retained.

## Read the current submission

1. [Complete English main article,34pages]({PREFIX}.pdf).
2. [Current technical supplement,181pages]({PREFIX}_Supplement.pdf).
3. [Independent retained R58 companion,37pages]({PREFIX}_Retained_Companion_R58.pdf).
4. [Point-by-point response](RESPONSE_TO_REFEREE.md): all ten major and forty technical controlling R65 items, with inherited closures and surviving questions separated.
5. [Theorem map](THEOREM_MAP.md), [actual native index](THEOREM_INDEX.json), [logical dependency ledger](THEOREM_DEPENDENCIES.json) and [R76 dependency guide](THEOREM_DEPENDENCIES_R76.md).
6. [Proof audit](PROOF_AUDIT.md), [research status](RESEARCH_STATUS.md), [primary-source priority ledger](LITERATURE_AND_PRIORITY.md), [source provenance](SOURCE_PROVENANCE.md) and [complete preservation map](PRESERVATION_MAP.md).

Keep the main and supplement PDF filenames together for paired links. Plain extracted text files accompany each PDF for searching; they are not substituted for the typeset mathematical submission.

## Mathematical increment

The main article proves a cost-preserving finite-group normal form for closed convex specifications, an attained finite minimax principle for uniform all-word approximation and robust multiplicity certificates. A sharp two-output common-null inequality gives an exact three-piece synthesis boundary, equality classification and the complete mean–contrast resource law for every symmetric group of degree at least five. A general return-polytope theorem gives one finite simulator for all specified adaptive stopped experiments; finite angle alphabets have polylogarithmic memory. At fixed positive expected budget and a fixed badly approximable phase, physical dictionaries with Born readouts have a matching logarithmic law with leading constant one.

The physical-dictionary lower is not an unrestricted-decoder lower. The matrix theorem equates parameter-existence regions, not factorizations of every given matrix pair. The group mean is not a Bayesian prior. The original general-M squared-sign risk frontier and independent A1/A2/Theta objectives remain distinct open problems. All209 inherited indexed statements remain active, along with eleven additions, for220 total; the independent companion and all original causal/optimization/reset/discrimination/geometric results retain their scopes.

## Exact source and validation identity

- **Controlling complete R75 source:** `bc2952aa9a9695fe9985d491a4156b8975024285`, delivered at `2c103f924720435700e947cc8df31b8b648f61e9`.
- **Current complete source:** `{SHA}`; source subtree `{TREE}`;507 files.
- **Source path:** `{PAPER}`.
- **Revision branch:** `{BRANCH}`.
- **Source manifest SHA-256:** `{receipt['source_manifest_sha256']}`.
- **Publication identity:** the Git commit containing this directory, with the source commit above as sole parent. It is intentionally not circularly embedded in its own files.
- **Latest substantive deposited report:** R65 `358481b21ceeeedb1205ebd30f86982e32a2cb04`, preserved [in full](CONTROLLING_R65_REPORT.md). It reviewed R65, not this revision. No new independent review or human identity is inferred from audit/test files.

[BUILD_RECEIPT.json](BUILD_RECEIPT.json) records an actual strict PASS at the current source SHA: {counts['suites']} suites, {counts['total']:,} checks per mode ({counts['exact']:,} exact and {counts['floating']:,} floating), with ordinary/optimized outputs byte-identical. These modes execute the same checks; their counts are not added together as independent evidence. All three PDFs were natively compiled in three passes with shell escape disabled and no final undefined/overfull warnings. The final PDFs are byte-identical to the visually inspected drafts; [VISUAL_QA_RECEIPT.json](VISUAL_QA_RECEIPT.json) binds that comparison.

The initial source `4f61c7a5173416c3532e1b6b967bed8e2a559f08` failed at a development-relative diagnostic source path. Its failed receipt is preserved. The child source corrects only that path, records the correction, and independently passes the full strict gate. No failed or partial run has been renamed PASS. Actual hosted Actions observations are separate under `evidence/remote/`; local verification is not hosted CI.

## Verify and restore the complete files

Download this entire publication directory from its immutable Git commit. From it run:

```bash
python verify_received.py --root . --expect-source-commit {SHA} --expect-paper-tree {TREE}
python restore_archives.py --root . --out /absolute/fresh/restored --expect-source-commit {SHA} --expect-paper-tree {TREE}
```

The receiver checks every delivery file, archive part and complete payload, the exact507-file source tree, all386 predecessor destinations,59 protected native bodies, the34-file companion,220 current statements,23 stored diagnostic outputs and all6,664 historical text objects. It reads stored execution evidence; it does not execute new mathematical tests or certify theorems. The archive hashes and part order are in [archives/ARCHIVE_PARTS.json](archives/ARCHIVE_PARTS.json).

To reproduce the strict execution, check out the exact source commit in Git, install its pinned requirements and native LaTeX tools, then run `python verify.py --source-commit {SHA} --out /absolute/fresh/build` from the source directory. An extracted/edited source can use `--draft`; it cannot issue a Git-bound strict PASS.

Complete written mathematical proofs, finite exact/floating diagnostics, formal proof verification, independent human assessment and editorial decisions are different categories. This delivery provides the first two with exact source identities. It claims neither the latter three nor exhaustive priority clearance.
'''
# Add normal prose spacing to machine-composed count phrases.
for a,b in [('article,34','article, 34'),('supplement,181','supplement, 181'),('companion,37','companion, 37'),('All209','All 209'),('for220','for 220'),(';507','; 507'),('exact507','exact 507'),('all386','all 386'),(',59',', 59'),('the34','the 34'),(',220',', 220'),(',23',', 23'),('all6,664','all 6,664')]:start=start.replace(a,b)
(PUB/'START_HERE.md').write_text(start)
(PUB/'README.md').write_text('# General Theta Foundations I — R76 publication\n\nStart with [the independent-referee entry](START_HERE.md). This directory delivers the complete current English main article, technical supplement, independent companion, full source and verification/history archives, the fifty-item response and the exact-source mathematical/provenance records.\n\nSource commit: `'+SHA+'`. The publication is its child commit; all changes remain confined to this paper’s two new R76 folders. The original four-journal objective remains in force, with every unproved extension explicitly distinguished.\n')
(PUB/'evidence/EXECUTION_NOTES.md').write_text('''# Actual execution and limits

The complete initial source was pushed, fetched and run at its real Git HEAD. That strict attempt failed at the new structure diagnostic's development-relative theorem-file default. Its complete partial output and failure receipt remain in the validation archive under `strict-source/`. The path-only correction has its own child source commit and preserved precommit check; the final `build/` output is the actual complete strict rerun at the corrected source SHA.

Draft01 stopped at an unavailable script-font command in a new section. Replacing it by the existing calligraphic command fixed compilation. Draft02 completed; visual review found a missing space in one infimum subscript and one orphan final reference. Draft03 corrected both without changing theorem numbers/pages. The current native index is identical across those two successful drafts. All three documents from the final strict run are byte-identical to the reviewed versions.

The shared filesystem briefly exhausted space during a remote-head redirection and a Poppler render. The incomplete head output was discarded as a snapshot; a fresh successful enumeration matched all1,300 initial heads. Only two explicitly reproducible audit caches were removed; source, current corpus and all receipts remained intact. The renderer's failure and successful bounded-chunk retry are preserved. An index-subtree inspection command was also corrected to inspect the written tree instead of attempting a directory lookup directly in the index; no source or remote commit was changed by that read error.

The validation archive includes every current build directory, every rendered page/contact sheet and all actual visual-view records, not just a summary PASS. Finite diagnostics do not prove continuum assertions. Source integrity, native compilation, author-team AI argument challenges, image inspection, a hosted workflow, human peer review and editorial decisions remain separate evidence types. Only actual matching-SHA completed runs can be called successful hosted CI.
''')
write_json(PUB/'DELIVERY_MANIFEST.json',{'schema':'theta.r76.delivery-manifest.v1','source_commit':SHA,'source_paper_tree':TREE,'source_manifest_sha256':receipt['source_manifest_sha256'],'manifest_excludes_itself':True,'optional_local_reconstructions_excluded':[x['file'] for x in archive_records],'files':[identity(f,f.relative_to(PUB).as_posix()) for f in regular(PUB) if f.name!='DELIVERY_MANIFEST.json'],'limitations':['Manifest identity is not a proof or editorial verdict.','Final remote download/receiving checks are separate from this local assembly.']})
print(json.dumps({'publication':str(PUB),'source_files':507,'validation_files':len(validation_rows),'archives':[{k:x[k] for k in ['file','bytes','sha256']} for x in archive_records],'archive_parts':sum(len(x['parts']) for x in archive_records),'delivery_files':len(regular(PUB)),'source_commit':SHA,'counts':counts},indent=2))
