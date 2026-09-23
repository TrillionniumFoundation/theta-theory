#!/usr/bin/env python3
"""Publish discoverability and scope evidence; never label diagnostics as proofs."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parents[2]
P=R/'papers/GTF-I-v18-continuation-transport'
BASE='a94ec98d6e33d9719f72deec160f5c8270ce006f'
ROOTFILE='GENERAL_THETA_FOUNDATIONS_I_V18_REVIEW_READY.md'
def git(*args):
 return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
if '--check-index' in sys.argv:
 raw=git('diff','--cached','--name-status',BASE)
 rows=[]
 allowed=('.github/scripts/gtf18_materialize.py','.github/scripts/gtf18_publish.py','.github/workflows/gtf18-publication.yml',ROOTFILE)
 for line in raw.splitlines():
  fields=line.split('\t')
  if len(fields)!=2 or fields[0]!='A':raise RuntimeError('Existing content changed: '+line)
  if not (fields[1].startswith('papers/GTF-I-v18-continuation-transport/') or fields[1] in allowed):raise RuntimeError('Scope escaped: '+line)
  rows.append({'status':fields[0],'path':fields[1]})
 out={'base_review_commit':BASE,'mathematical_source_commit':os.environ['GTF_SOURCE_COMMIT'],'entries':rows,'all_additions':True,'pre_existing_files_modified_or_deleted':0,'scope':'The staged publication plus its source commits relative to the controlling review. This record itself is added after the check.'}
 (P/'evidence/PRESERVATION_GIT_DIFF.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'all_additions':True,'entries':len(rows)}));sys.exit(0)
r=json.loads((P/'evidence/BUILD_RECEIPT.json').read_text())
if r['source_commit']!=os.environ['GTF_SOURCE_COMMIT'] or git('rev-parse','HEAD')!=r['source_commit']:raise RuntimeError('Source identity changed')
for name,item in r['artifacts'].items():
 if hashlib.sha256((P/name).read_bytes()).hexdigest()!=item['sha256']:raise RuntimeError('Artifact digest changed: '+name)
prefix='papers/GTF-I-v18-continuation-transport/'
text=f'''# General Theta Foundations I — v18 review-ready revision

**General Theta Foundations I: Continuation, Testing, and Microscopic Transport**  
Qian Qi · Full English theorem–proof manuscript · 23 September 2026

## Frozen provenance

- Mathematical source commit: `{r['source_commit']}`.
- Controlling v17 r3 review commit: `{BASE}`.
- Additional pipeline-aware v17 r2 review: `9f4787221c086e25f7d95b36e97aff870bd2b0c5`.
- Publication workflow run: `{r['workflow_run']}`.
- Revision branch: `revision/general-theta-foundations-i-v18-continuation-transport-2026-09-23`.

## Reading entry points

- [Canonical English article]({prefix}paper.pdf): {r['canonical_pages']} pages.
- [Complete development, including all preserved historical pages]({prefix}complete-development.pdf): {r['complete_development_pages']} pages.
- [Point-by-point response to the two latest referee reports]({prefix}RESPONSE_TO_REFEREE.md).
- [Manuscript sources and build instructions]({prefix}README.md).
- [Proof ledger]({prefix}PROOF_LEDGER.md) and [source-bound statements]({prefix}evidence/BOUND_PROOF_STATUS.json).
- [Historical source audit]({prefix}HISTORY_AUDIT.md), [pipeline status]({prefix}PIPELINE_STATUS.md), and [literature comparison]({prefix}LITERATURE_COMPARISON.md).
- [Executed build receipt]({prefix}evidence/BUILD_RECEIPT.json), [finite diagnostics]({prefix}evidence/DIAGNOSTICS.json), and [negative controls]({prefix}evidence/NEGATIVE_CONTROLS.json).
- [Portable submission sources]({prefix}evidence/SUBMISSION_SOURCES.zip) and [complete source closure]({prefix}evidence/COMPILED_SOURCES.zip).

## Substantive revision

The article develops simultaneous continuation covers and an exact memory-cut lower bound; finite reset audits on the original, possibly nonconvex, behavior family; an exact effective discrepancy chart; and a composition theorem carrying the same finite certificate through changing hard-sphere observations, whole-process likelihood and posterior convergence, and bounded risk-sensitive backward equations. A fixed rational audit with 2,800 training resets has a certified score greater than 2/5 on the stated collision family. Its memory and sample costs are explicitly charged.

The predecessor's 256-page development is retained in full, with equality of every inherited page's extracted text and raster verified by the build. No earlier manuscript or pipeline file is overwritten. The canonical article is an organized proof manuscript, not a sequence of referee replies; revision bookkeeping is separate.

## Executed checks and remaining review questions

This run recorded {r['finite_exact_checks']} exact finite checks, equality of ordinary and optimized Python results, {r['negative_control_executions']} negative-control executions, {len(r['inherited_diagnostic_runs'])} inherited diagnostic runs, {r['theorem_statement_count']} source-bound theorem/lemma/proposition statements, and {r['resolved_label_count']} resolved labels. The compiler was `{r['compiler']}` and required {r['tex_passes']} passes. The receipt reports no unresolved references/citations or overfull boxes.

These are reproducibility and diagnostic results, **not independent certification of the analytic proofs, priority, or journal acceptance**. The proof-level comparison with Norberg (2002) remains explicitly unverified because the full original argument was not obtained. The full eleven-paper kinetic program is preserved, not declared closed by a finite-particle or bounded-observation result. A2 remains independently developed rather than being assigned a fictitious dependency on this article.

## Artifact SHA-256

'''
for name,item in r['artifacts'].items():text+=f"- `{name}`: `{item['sha256']}` ({item['bytes']} bytes).\n"
(R/ROOTFILE).write_text(text)
print(ROOTFILE)
