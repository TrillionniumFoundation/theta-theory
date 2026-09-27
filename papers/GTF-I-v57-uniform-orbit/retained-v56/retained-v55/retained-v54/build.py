"""Source-bound v54 qualification. No network access or remote mutation.

Finite exact regressions, preservation and rendered reproducibility are not a
formal proof checker or an implementation of general algebraic classification.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, re, sys, tempfile, zipfile
from pathlib import Path
import fitz
import sympy

HOME=Path(__file__).resolve().parent
OLD=HOME/'retained-v53'
EV=HOME/'evidence'
BASE='825d1d302cfca6c6b5abe8497bddb4df8680d810'
REVIEW='ea6d8b71653ec4aa6084b4faf63fe7d702505a26'
REPORT='a4f024689b9470c0f311fe0b1f744abc14ea54ac'
PDFS={'article':'paper.pdf','scalar_predecessor':'SCALAR_PREDECESSOR.pdf',
      'companion':'COMPANION_NOTES.pdf','complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}
spec=importlib.util.spec_from_file_location('gtf53_build',OLD/'build.py')
if spec is None or spec.loader is None:raise RuntimeError('Missing native predecessor builder')
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
require=core.require
sha=core.sha

def save(name: str, data) -> None:
    (EV/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def sources() -> list[Path]:
    return sorted(p for p in HOME.rglob('*') if p.is_file()
        and 'evidence' not in p.relative_to(HOME).parts and '__pycache__' not in p.parts
        and p.suffix in {'.tex','.py','.md','.json'}
        and p.name not in {'assemble_revision.py'})

def preservation(local_missing: bool=False) -> dict:
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_blob']==REPORT,'Frozen identity mismatch')
    require(len(manifest['files'])==72,'Unexpected native predecessor count')
    for name,digest in manifest['files'].items():
        require(sha(OLD/name)==digest,'Retained native source changed: '+name)
    report=HOME/'FROZEN_R35_REPORT.md'
    report_ok=False
    if report.exists():
        data=report.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(digest==REPORT,'Controlling r35 report bytes changed');report_ok=True
    else:
        require(local_missing and not os.environ.get('GITHUB_ACTIONS'),'Missing frozen r35 report')
    status=json.loads((HOME/'PROOF_STATUS.json').read_text())
    require(status['local_comments']==list(range(1,31)),'Local response coverage missing')
    require(status['required_revision_items']==['8.'+str(i) for i in range(1,10)],'Major response coverage missing')
    response=(HOME/'RESPONSE_TO_REFEREE.md').read_text()
    require(all(f'R35 local {i:02d}' in response for i in range(1,31)),'Response heading missing')
    core.HOME=OLD;core.OLD=OLD/'retained-v52';core.EV=EV/'inherited';core.EV.mkdir(exist_ok=True)
    nested=core.check_sources()
    return {'native_predecessor_files':72,'byte_identical':True,
            'controlling_report_verified':report_ok,'nested_v52':nested}

def build(local_missing: bool, isolated_mode: bool, check_isolated: bool) -> dict:
    EV.mkdir(exist_ok=True)
    for p in EV.glob('page-*.png'):p.unlink()
    (EV/'FAILED_COMMAND.txt').unlink(missing_ok=True)
    kept=preservation(local_missing)
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-build')
    before={str(p.relative_to(HOME)):sha(p) for p in sources()}
    inherited=core.regressions()
    core.HOME=HOME;core.EV=EV;core.PDFS=PDFS
    normal=json.loads(core.run([sys.executable,'check_revision.py'],HOME))
    optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],HOME))
    require(normal==optimized,'New normal/optimized results differ')
    require(normal['status']=='success','New checks did not succeed')
    save('V54_CHECKS.json',normal)
    pdfs={};pages={};locations={};inputs={}
    docs=[('article',HOME,'main.tex'),('scalar_predecessor',OLD,'main.tex'),
          ('companion',OLD,'supplement-notes.tex'),('complete_supplement',OLD/'retained-v52','main.tex')]
    for kind,cwd,name in docs:
        active,labels=core.input_inventory(cwd,name)
        pdfs[kind],pages[kind],locations[kind]=core.typeset(kind,cwd,name)
        require(labels<=set(locations[kind]),'Unloaded mathematical label: '+kind)
        inputs[kind]={'inputs':[str(p.relative_to(HOME)) for p in active],
                      'labels':sorted(labels),'label_count':len(labels)}
    require(set(json.loads((HOME/'PROOF_STATUS.json').read_text())['theorems'])<=set(locations['article']),
            'Principal theorem absent from article')
    after={str(p.relative_to(HOME)):sha(p) for p in sources()}
    require(before==after,'Qualification modified native source')
    save('SOURCE_HASHES.json',after);save('PAGE_CHECKS.json',pages)
    save('THEOREM_LOCATIONS.json',locations);save('ACTIVE_INPUTS.json',inputs)
    core.makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in sources()])
    isolated=None
    if check_isolated:
        require(kept['controlling_report_verified'],'An unpinned local build cannot qualify publication')
        with tempfile.TemporaryDirectory(prefix='gtf54-isolated-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as archive:archive.extractall(temp)
            other=Path(temp)/HOME.name
            output=core.run([sys.executable,'build.py','--isolated'],other,timeout=1200)
            (EV/'ISOLATED_REBUILD_LOG.txt').write_text(output)
            require(json.loads((other/'evidence/PAGE_CHECKS.json').read_text())==pages,'Isolated text/raster page mismatch')
            receipt=json.loads((other/'evidence/BUILD_RECEIPT.json').read_text())
            require(receipt['status']=='success' and receipt['source_commit']==source,'Isolated source identity mismatch')
            require(json.loads((other/'evidence/SOURCE_HASHES.json').read_text())==after,'Isolated native source mismatch')
            isolated={'status':'success','all_page_text_equal':True,'all_page_raster_equal':True,
                'all_native_source_hashes_equal':True,'regressions_reexecuted':True,
                'repository_or_network_required':False,'pages':{k:len(v) for k,v in pages.items()}}
            save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    versions={'python':sys.version.split()[0],'sympy':sympy.__version__,'pymupdf':fitz.VersionBind}
    receipt={'schema':'gtf54.build/1','status':'success' if kept['controlling_report_verified'] else 'local-preflight-only',
        'source_commit':source,'predecessor_publication':BASE,'review_commit':REVIEW,
        'workflow_run':os.environ.get('GITHUB_RUN_ID'),'documents':pdfs,'preservation':kept,
        'native_source_files':len(after),'normal_optimized_agreement':True,
        'new_exact_finite_assertions':normal['exact_finite_assertions'],
        'new_named_negative_controls':len(normal['negative_controls_detected']),
        'new_negative_control_executions':2*len(normal['negative_controls_detected']),
        'inherited_regression_suites':list(inherited),'isolated_rebuild':isolated,
        'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),'dependency_versions':versions,
        'scope':'Written mathematical proofs, finite exact examples, native preservation and rendered reproducibility. Not formal theorem verification, a general implemented algebraic solver, exhaustive priority clearance, or closure of unrelated analytic gates.'}
    save('BUILD_RECEIPT.json',receipt)
    package=[HOME/n for n in [*PDFS.values(),'README.md','RESPONSE_TO_REFEREE.md',
        'HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md','PROOF_STATUS.json','PRESERVATION_MANIFEST.json']]
    if kept['controlling_report_verified']:package.append(HOME/'FROZEN_R35_REPORT.md')
    package += [EV/n for n in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json',
        'THEOREM_LOCATIONS.json','V54_CHECKS.json','PAGE_CHECKS.json','ACTIVE_INPUTS.json']]
    if isolated:package.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    core.makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package])
    if check_isolated and not isolated_mode:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V54_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 54\n\n'
            '**Sharp Noise Thresholds and Width Laws for Stochastic Realizations of Compact Group Experiments**\n\n'
            f'Validated native source: `{source}`. Frozen r35: `{REVIEW}`. Base v53: `{BASE}`.\n\n'
            f'[Main article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
            f'[Native source](papers/{HOME.name}/main.tex) · '
            f'[Response to r35](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
            f'[Portable referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip) · '
            f'[Actual build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json)\n\n'
            'Work branch: `revision/general-theta-foundations-i-v54-chebyshev-radius-2026-09-27`.\n'
            'Ready branch: `revision/general-theta-foundations-i-v54-referee-ready-2026-09-27`.\n\n'
            'The principal results are the sharp constrained component-image radius for joint outputs, '
            'an intrinsic compact-group/return-language converse, and full-subcritical matching '
            'Theta(N^(s/(2s+1))) width for a specified Diophantine rotation family with 0<rho<1. '
            'The rational polynomial specialization is effective; the quotient minimum is explicitly '
            'restricted to deterministic component-quotient machines.\n\n'
            f'The {pdfs["scalar_predecessor"]["pages"]}-page scalar predecessor, '
            f'{pdfs["companion"]["pages"]}-page companion and '
            f'{pdfs["complete_supplement"]["pages"]}-page complete supplement are retained and rebuilt. '
            'All 72 predecessor native files remain byte-identical, including the 59-file, 242-label earlier supplement. '
            'Normal/optimized checks and all-page isolated text/raster comparison passed for the cited source. '
            'These facts are reproducibility evidence, not a claim of independent formal mathematical verification or journal acceptance.\n')
    return receipt

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-isolated',action='store_true')
    parser.add_argument('--isolated',action='store_true')
    parser.add_argument('--local-missing-report',action='store_true',help='Local preflight only; never qualifies publication')
    args=parser.parse_args()
    require(not(args.check_isolated and args.isolated),'Conflicting modes')
    result=build(args.local_missing_report,args.isolated,args.check_isolated)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
