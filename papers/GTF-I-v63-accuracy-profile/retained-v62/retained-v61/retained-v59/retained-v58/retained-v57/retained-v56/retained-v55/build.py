"""Source-bound qualification for revision 55. No network or remote mutation.

This checks native preservation, finite examples, typesetting and independent
rendered reproduction. It is not formal verification of universal theorems.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile
import fitz
import sympy

HOME=Path(__file__).resolve().parent
OLD=HOME/'retained-v54'
EV=HOME/'evidence'
BASE='1eb16a3f857d17a91dc1c82906ef16a5965a47d2'
REVIEW='9c92a08458b92fd831010dca835de8e2239f82fc'
REPORT='85a4bd2e1d4d6b02cb2360a66c25253148e8f2c1'
PDFS={'article':'paper.pdf','radius_predecessor':'RADIUS_PREDECESSOR.pdf',
      'scalar_predecessor':'SCALAR_PREDECESSOR.pdf','companion':'COMPANION_NOTES.pdf',
      'complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}
spec=importlib.util.spec_from_file_location('v54_build',OLD/'build.py')
if spec is None or spec.loader is None:raise RuntimeError('Missing retained native builder')
v54=importlib.util.module_from_spec(spec);spec.loader.exec_module(v54)
core=v54.core
require=core.require
sha=core.sha

def save(name,data):
    (EV/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def sources():
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    retained=[OLD/name for name in manifest['files']]
    own=[p for p in HOME.rglob('*') if p.is_file()
         and not {'retained-v54','evidence','assembly','__pycache__'}.intersection(p.relative_to(HOME).parts)
         and p.suffix in {'.tex','.py','.md','.json'} and p.name!='assemble_revision.py']
    return sorted(retained+own)

def preservation(local_missing):
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_commit']==REVIEW
            and manifest['review_blob']==REPORT,'Frozen identities changed')
    require(len(manifest['files'])==91,'Unexpected predecessor native count')
    for name,digest in manifest['files'].items():require(sha(OLD/name)==digest,'Retained native changed: '+name)
    report=HOME/'FROZEN_R36_REPORT.md';pinned=False
    if report.exists():
        raw=report.read_bytes()
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==REPORT,'Report bytes changed')
        pinned=True
    else:
        require(local_missing and not os.environ.get('GITHUB_ACTIONS'),'Missing frozen r36 report')
    status=json.loads((HOME/'PROOF_STATUS.json').read_text())
    require(status['required_revision_items']==['9.'+str(i) for i in range(1,10)],'Incomplete required-item inventory')
    require(status['local_comments']==list(range(1,31)),'Incomplete local-comment inventory')
    require(not any(status['analytic_pipeline_closure'].values()),'Unjustified analytic pipeline closure')
    response=(HOME/'RESPONSE_TO_REFEREE.md').read_text()
    require(all(f'R36 local {i:02d}' in response for i in range(1,31)),'Missing local response')
    require(all('R36 9.'+str(i)+' ' in response for i in range(1,10)),'Missing major response')
    # Check inherited identities and loaded sources, not just the outer hash list.
    v54.EV=EV/'inherited-v54';v54.EV.mkdir(exist_ok=True)
    nested=v54.preservation(False)
    return {'native_predecessor_files':91,'byte_identical':True,
            'controlling_report_verified':pinned,'nested_v54_preservation':nested}

def build(local_missing,isolated_mode,check_isolated):
    EV.mkdir(exist_ok=True)
    for path in EV.glob('page-*.png'):path.unlink()
    (EV/'FAILED_COMMAND.txt').unlink(missing_ok=True)
    kept=preservation(local_missing)
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-preflight')
    before={str(p.relative_to(HOME)):sha(p) for p in sources()}
    inherited=core.regressions()
    v54normal=json.loads(core.run([sys.executable,'check_revision.py'],OLD))
    v54optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],OLD))
    require(v54normal==v54optimized and v54normal['status']=='success','V54 regression mismatch')
    save('V54_CHECKS.json',v54normal)
    normal=json.loads(core.run([sys.executable,'check_revision.py'],HOME))
    optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],HOME))
    require(normal==optimized and normal['status']=='success','V55 normal/optimized mismatch')
    save('V55_CHECKS.json',normal)
    core.HOME=HOME;core.EV=EV;core.PDFS=PDFS
    docs=[('article',HOME,'main.tex'),('radius_predecessor',OLD,'main.tex'),
          ('scalar_predecessor',OLD/'retained-v53','main.tex'),
          ('companion',OLD/'retained-v53','supplement-notes.tex'),
          ('complete_supplement',OLD/'retained-v53'/'retained-v52','main.tex')]
    pdfs={};pages={};locations={};inventory={}
    for kind,cwd,name in docs:
        inputs,labels=core.input_inventory(cwd,name)
        pdfs[kind],pages[kind],locations[kind]=core.typeset(kind,cwd,name)
        require(labels<=set(locations[kind]),'Unloaded labels: '+kind)
        inventory[kind]={'inputs':[str(p.relative_to(HOME)) for p in inputs],
                         'labels':sorted(labels),'label_count':len(labels)}
    principal=set(json.loads((HOME/'PROOF_STATUS.json').read_text())['theorems'])
    require(principal<=set(locations['article']),'Principal theorem absent from compiled article')
    after={str(p.relative_to(HOME)):sha(p) for p in sources()}
    require(before==after,'Build altered native source')
    save('SOURCE_HASHES.json',after);save('PAGE_CHECKS.json',pages)
    save('THEOREM_LOCATIONS.json',locations);save('ACTIVE_INPUTS.json',inventory)
    core.makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in sources()])
    isolated=None
    if check_isolated:
        require(kept['controlling_report_verified'],'An unpinned local preflight cannot qualify publication')
        with tempfile.TemporaryDirectory(prefix='gtf55-isolated-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z:z.extractall(temp)
            other=Path(temp)/HOME.name
            log=core.run([sys.executable,'build.py','--isolated'],other,timeout=1200)
            (EV/'ISOLATED_REBUILD_LOG.txt').write_text(log)
            require(json.loads((other/'evidence/PAGE_CHECKS.json').read_text())==pages,'Isolated page text/raster mismatch')
            require(json.loads((other/'evidence/SOURCE_HASHES.json').read_text())==after,'Isolated source mismatch')
            receipt=json.loads((other/'evidence/BUILD_RECEIPT.json').read_text())
            require(receipt['status']=='success' and receipt['source_commit']==source,'Isolated receipt identity mismatch')
            isolated={'status':'success','all_page_text_equal':True,'all_page_raster_equal':True,
                      'all_native_source_hashes_equal':True,'all_regressions_reexecuted':True,
                      'repository_or_network_required':False,'pages':{k:len(v) for k,v in pages.items()}}
            save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    receipt={'schema':'gtf55.build/1','status':'success' if kept['controlling_report_verified'] else 'local-preflight-only',
             'source_commit':source,'predecessor_publication':BASE,'review_commit':REVIEW,
             'workflow_run':os.environ.get('GITHUB_RUN_ID'),'documents':pdfs,'preservation':kept,
             'native_source_files':len(after),'normal_optimized_agreement':True,
             'new_exact_finite_assertions':normal['exact_finite_assertions'],
             'new_named_negative_controls':len(normal['negative_controls_detected']),
             'new_negative_control_executions':2*len(normal['negative_controls_detected']),
             'inherited_regression_suites':['v54']+list(inherited),
             'isolated_rebuild':isolated,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
             'dependency_versions':{'python':sys.version.split()[0],'sympy':sympy.__version__,'pymupdf':fitz.VersionBind},
             'scope':'Complete written proofs, finite exact examples, preserved native history and rendered reproducibility; not a formal proof checker, exhaustive priority clearance, implemented general algebraic solver, or closure of independent analytic gates.'}
    save('BUILD_RECEIPT.json',receipt)
    package=[HOME/n for n in [*PDFS.values(),'README.md','RESPONSE_TO_REFEREE.md','HISTORY_AND_PIPELINE_AUDIT.md',
                             'LITERATURE_AUDIT.md','PROOF_STATUS.json','PRESERVATION_MANIFEST.json','REVISION_SCOPE.md']]
    if kept['controlling_report_verified']:package.append(HOME/'FROZEN_R36_REPORT.md')
    package += [EV/n for n in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                               'V55_CHECKS.json','V54_CHECKS.json','PAGE_CHECKS.json','ACTIVE_INPUTS.json']]
    if isolated:package.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    core.makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package])
    if check_isolated and not isolated_mode:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V55_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 55\n\n'
          '**Stochastic Purification and Sharp Noise Thresholds for Compact Group Experiments**\n\n'
          f'Qualified native source: `{source}`. Frozen r36: `{REVIEW}`. Base v54: `{BASE}`.\n\n'
          f'[Main article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
          f'[Readable source](papers/{HOME.name}/main.tex) · '
          f'[Response to r36](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
          f'[Actual build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json) · '
          f'[Portable referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip)\n\n'
          'Work branch: `revision/general-theta-foundations-i-v55-stochastic-purification-2026-09-27`.\n'
          'Referee branch: `revision/general-theta-foundations-i-v55-referee-ready-2026-09-27`.\n\n'
          'Principal additions: stationary purification without width/error loss; exact unrestricted stationary minimum '
          'and finite-quotient existence; all nonempty exact-return languages and their phases; infinite-component '
          'strict thresholds and exact boundary; a sharp linear-width 2-adic example; a curved categorical example; '
          'unit-amplitude matching width at positive error; effective stationary minimization.\n\n'
          f'All 91 predecessor native files are byte-identical. The five rebuilt documents have '
          f'{", ".join(str(pdfs[k]["pages"]) for k in PDFS)} pages '
          '(new article, radius predecessor, scalar predecessor, companion, complete supplement). '
          f'The new finite regression executes {normal["exact_finite_assertions"]:,} assertions and '
          f'{len(normal["negative_controls_detected"])} named negative controls in both normal and optimized Python. '
          'All native source hashes and every page text/raster agree with an independent isolated rebuild.\n\n'
          'The preparation anchor is superseded by this source-bound qualification. No other paper branch is modified. '
          'These are reproduction facts, not a formal mathematical proof certificate, independent priority clearance, '
          'or a guarantee of journal acceptance. Independent A/B/C/D analytic closure flags remain false.\n')
    return receipt

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-isolated',action='store_true')
    parser.add_argument('--isolated',action='store_true')
    parser.add_argument('--local-missing-report',action='store_true')
    args=parser.parse_args()
    require(not (args.check_isolated and args.isolated),'Conflicting modes')
    print(json.dumps(build(args.local_missing_report,args.isolated,args.check_isolated),indent=2,sort_keys=True))

if __name__=='__main__':main()
