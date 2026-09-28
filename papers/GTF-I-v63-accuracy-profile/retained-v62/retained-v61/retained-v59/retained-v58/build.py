"""Source-bound v58 qualification, including independent native-only rebuilding.

No network and no GitHub writes. Finite regression, source identity and rendering
are checked here; universal proofs and imported theorems are not formalized.
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
OLD=HOME/'retained-v57'
EV=HOME/'evidence'
BASE='0e07470b9693a2789af00222f063e715a83ff454'
REVIEW='5b2fb03f87a6b28bddcef51d498a0c78429bfa22'
REPORT='c530ec0f755d2aa9a9d23b3d99dc4675fcacc679'
FROZEN={'FROZEN_R38_REPORT.md':REPORT,
        'FROZEN_PIPELINE_LEDGER.md':'c1ef29a5bcab0e2d4729c7c6815ec11e95be5808',
        'FROZEN_PIPELINE_HISTORY.md':'6041ef8b9e5e76883e86d4009c0735869b51b7a6'}
PDFS={'article':'paper.pdf','structural':'STRUCTURAL_PAPER.pdf','complete_revision':'COMPLETE_REVISION.pdf','orbit_predecessor':'ORBIT_PREDECESSOR.pdf','boundary_predecessor':'BOUNDARY_PREDECESSOR.pdf','purification_predecessor':'PURIFICATION_PREDECESSOR.pdf',
      'radius_predecessor':'RADIUS_PREDECESSOR.pdf','scalar_predecessor':'SCALAR_PREDECESSOR.pdf',
      'companion':'COMPANION_NOTES.pdf','complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}
spec=importlib.util.spec_from_file_location('retained_v57_build',OLD/'build.py')
if spec is None or spec.loader is None:raise RuntimeError('Missing retained builder')
v57=importlib.util.module_from_spec(spec);spec.loader.exec_module(v57)
core=v57.core
require=core.require
sha=core.sha

def save(name,data):
    (EV/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def sources():
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    retained=[OLD/name for name in manifest['files']]
    own=[p for p in HOME.rglob('*') if p.is_file()
         and not {'retained-v57','evidence','assembly','__pycache__'}.intersection(p.relative_to(HOME).parts)
         and p.suffix in {'.tex','.py','.md','.json'} and p.name!='assemble_revision.py']
    return sorted(retained+own)

def preservation(local_missing):
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_commit']==REVIEW
            and manifest['review_blob']==REPORT,'Frozen identities changed')
    require(len(manifest['files'])==181,'Unexpected predecessor native count')
    for name,digest in manifest['files'].items():require(sha(OLD/name)==digest,'Retained source changed: '+name)
    pins={}
    for name,blob in FROZEN.items():
        path=HOME/name
        if path.exists():
            raw=path.read_bytes()
            require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blob,'Frozen evidence changed: '+name)
            pins[name]=True
        else:
            require(local_missing and not os.environ.get('GITHUB_ACTIONS'),'Missing frozen evidence: '+name)
            pins[name]=False
    status=json.loads((HOME/'PROOF_STATUS.json').read_text())
    require(status['required_revision_items']==['10.'+str(i) for i in range(1,9)],'Incomplete major inventory')
    require(status['local_comments']==list(range(1,37)),'Incomplete local inventory')
    require(not any(status['analytic_pipeline_closure'].values()),'Unsupported analytic closure')
    response=(HOME/'RESPONSE_TO_REFEREE.md').read_text()
    require(all(f'R38 local {i:02d}' in response for i in range(1,37)),'Missing local response')
    require(all('R38 10.'+str(i)+' ' in response for i in range(1,9)),'Missing major response')
    v57.EV=EV/'inherited-v57';v57.EV.mkdir(exist_ok=True)
    nested=v57.preservation(False)
    _,oldlabels=core.input_inventory(OLD,'main.tex')
    _,newlabels=core.input_inventory(HOME,'main.tex')
    require(oldlabels<=newlabels,'A previous active mathematical label was deleted')
    return {'native_predecessor_files':181,'byte_identical':True,'frozen_evidence':pins,
            'controlling_report_verified':pins['FROZEN_R38_REPORT.md'],
            'all_frozen_evidence_verified':all(pins.values()),
            'previous_active_labels_preserved':len(oldlabels),'nested_v57_preservation':nested}

def build(local_missing,isolated_mode,check_isolated):
    EV.mkdir(exist_ok=True)
    for path in EV.glob('page-*.png'):path.unlink()
    (EV/'FAILED_COMMAND.txt').unlink(missing_ok=True)
    kept=preservation(local_missing)
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-preflight')
    before={str(p.relative_to(HOME)):sha(p) for p in sources()}
    # The retained core still points to its v53/v52 source here.
    inherited=core.regressions()
    v56=OLD/'retained-v56';v55=v56/'retained-v55';v54=v55/'retained-v54';v53=v54/'retained-v53'
    for name,cwd in [('v54',v54),('v55',v55),('v56',v56),('v57',OLD)]:
        normal=json.loads(core.run([sys.executable,'check_revision.py'],cwd))
        optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],cwd))
        require(normal==optimized and normal['status']=='success',name+' normal/optimized mismatch')
        save(name.upper()+'_CHECKS.json',normal)
    normal=json.loads(core.run([sys.executable,'check_revision.py'],HOME))
    optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],HOME))
    require(normal==optimized and normal['status']=='success','V58 normal/optimized mismatch')
    save('V58_CHECKS.json',normal)
    example=json.loads(core.run([sys.executable,'qubit_compiler.py','--horizon','2','--amplitude','1/2',
                               '--max-labels','100','--output',str(EV/'COMPILED_EXAMPLE.json')],HOME))
    require(example['status']=='success' and example['max_row_support']<=4,'Compiler CLI failed')
    save('COMPILER_CLI_RECEIPT.json',{'status':'success','horizon':2,'amplitude':'1/2',
         'labels':example['labels'],'max_row_support':example['max_row_support'],
         'example_sha256':sha(EV/'COMPILED_EXAMPLE.json'),'large_horizon_benchmark_claimed':False})
    core.HOME=HOME;core.EV=EV;core.PDFS=PDFS
    docs=[('article',HOME,'quantitative.tex'),('structural',HOME,'structural.tex'),('complete_revision',HOME,'main.tex'),
          ('orbit_predecessor',OLD,'main.tex'),('boundary_predecessor',v56,'main.tex'),
          ('purification_predecessor',v55,'main.tex'),
          ('radius_predecessor',v54,'main.tex'),('scalar_predecessor',v53,'main.tex'),
          ('companion',v53,'supplement-notes.tex'),('complete_supplement',v53/'retained-v52','main.tex')]
    pdfs={};pages={};locations={};inventory={}
    for kind,cwd,name in docs:
        inputs,labels=core.input_inventory(cwd,name)
        pdfs[kind],pages[kind],locations[kind]=core.typeset(kind,cwd,name)
        require(labels<=set(locations[kind]),'Unloaded labels: '+kind)
        inventory[kind]={'inputs':[str(p.relative_to(HOME)) for p in inputs],
                         'labels':sorted(labels),'label_count':len(labels)}
    principal=set(json.loads((HOME/'PROOF_STATUS.json').read_text())['theorems'])
    require(principal<=set(locations['article']),'A principal theorem is not in the compiled article')
    require(principal<=set(locations['complete_revision']),'New principal theorem absent from complete edition')
    after={str(p.relative_to(HOME)):sha(p) for p in sources()}
    require(before==after,'Build changed native sources')
    save('SOURCE_HASHES.json',after);save('PAGE_CHECKS.json',pages)
    save('THEOREM_LOCATIONS.json',locations);save('ACTIVE_INPUTS.json',inventory)
    core.makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in sources()])
    isolated=None
    if check_isolated:
        require(kept['all_frozen_evidence_verified'],'An incomplete local preflight cannot qualify publication')
        with tempfile.TemporaryDirectory(prefix='gtf58-isolated-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z:z.extractall(temp)
            other=Path(temp)/HOME.name
            output=core.run([sys.executable,'build.py','--isolated'],other,timeout=1200)
            (EV/'ISOLATED_REBUILD_LOG.txt').write_text(output)
            require(json.loads((other/'evidence/PAGE_CHECKS.json').read_text())==pages,'Isolated text/raster mismatch')
            require(json.loads((other/'evidence/SOURCE_HASHES.json').read_text())==after,'Isolated source mismatch')
            require(sha(other/'evidence/COMPILED_EXAMPLE.json')==sha(EV/'COMPILED_EXAMPLE.json'),'Isolated compiler output mismatch')
            receipt=json.loads((other/'evidence/BUILD_RECEIPT.json').read_text())
            require(receipt['status']=='success' and receipt['source_commit']==source,'Isolated source identity mismatch')
            isolated={'status':'success','all_page_text_equal':True,'all_page_raster_equal':True,
                      'all_native_source_hashes_equal':True,'all_regressions_reexecuted':True,'rational_compiler_output_equal':True,
                      'repository_or_network_required':False,'pages':{k:len(v) for k,v in pages.items()}}
            save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    try:
        import scipy
        scipy_version=scipy.__version__
    except ImportError:scipy_version=None
    receipt={'schema':'gtf58.build/1','status':'success' if kept['all_frozen_evidence_verified'] else 'local-preflight-only',
             'source_commit':source,'predecessor_publication':BASE,'review_commit':REVIEW,
             'workflow_run':os.environ.get('GITHUB_RUN_ID'),'documents':pdfs,'preservation':kept,
             'native_source_files':len(after),'normal_optimized_agreement':True,
             'new_exact_finite_assertions':normal['exact_finite_assertions'],
             'new_named_negative_controls':len(normal['negative_controls_detected']),
             'new_negative_control_executions':2*len(normal['negative_controls_detected']),
             'inherited_regression_suites':['v57','v56','v55','v54']+list(inherited),
             'rational_compiler_example':{'horizon':2,'labels':example['labels'],'max_row_support':example['max_row_support']},
             'isolated_rebuild':isolated,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
             'dependency_versions':{'python':sys.version.split()[0],'sympy':sympy.__version__,'pymupdf':fitz.VersionBind,'scipy_optional_accelerator':scipy_version},
             'scope':'Finite exact regression, rational compiler rows, native preservation and rendered reproduction. Universal proofs and imported spectral gaps are written mathematics, not formally certified by these tests. No log-free width law, effective spectral constant, independent priority, editorial acceptance or analytic pipeline closure is asserted.'}
    save('BUILD_RECEIPT.json',receipt)
    package=[HOME/n for n in [*PDFS.values(),'README.md','RESPONSE_TO_REFEREE.md','HISTORY_AND_PIPELINE_AUDIT.md',
                             'LITERATURE_AUDIT.md','PROOF_STATUS.json','PRESERVATION_MANIFEST.json','REVISION_SCOPE.md','EXPLICIT_INPUT.json','qubit_compiler.py']]
    package += [HOME/n for n in FROZEN if (HOME/n).exists()]
    package += [EV/n for n in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                               'V58_CHECKS.json','V57_CHECKS.json','V56_CHECKS.json','V55_CHECKS.json','V54_CHECKS.json','PAGE_CHECKS.json','ACTIVE_INPUTS.json','COMPILED_EXAMPLE.json','COMPILER_CLI_RECEIPT.json']]
    if isolated:package.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    core.makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package])
    if check_isolated and not isolated_mode:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V58_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 58\n\n'
          '**Stochastic Width of Compact Orbits and a Rational Exact–Noisy Separation**\n\n'
          f'Qualified native source: `{source}`. Frozen r38: `{REVIEW}`. Base v57: `{BASE}`.\n\n'
          f'[Quantitative article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
          f'[Independent structural article ({pdfs["structural"]["pages"]} pages)](papers/{HOME.name}/STRUCTURAL_PAPER.pdf) · '
          f'[Complete preservation edition ({pdfs["complete_revision"]["pages"]} pages)](papers/{HOME.name}/COMPLETE_REVISION.pdf) · '
          f'[Response to r38](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
          f'[Actual build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json) · '
          f'[Portable referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip)\n\n'
          'Work branch: `revision/general-theta-foundations-i-v58-finite-input-2026-09-27`.\n'
          'Referee branch: `revision/general-theta-foundations-i-v58-referee-ready-2026-09-27`.\n\n'
          'New results: optimal uniform cap exponent from the least orbit dimension; explicit rational '
          'unitary generators and pure seed; exact pointwise exponential width persisting for error '
          'at most 625^(-N)/16; a uniform sparse rational and dyadic qubit compiler. '
          'The nonabelian noisy converse retains its logarithm and non-effective spectral-gap constant.\n\n'
          f'All 181 predecessor native files and {kept["previous_active_labels_preserved"]} active labels are preserved. '
          'The ten rebuilt documents have '+', '.join(str(pdfs[k]['pages']) for k in PDFS)+' pages. '
          f'The new exact finite regression executes {normal["exact_finite_assertions"]:,} assertions and '
          f'{len(normal["negative_controls_detected"])} named negative controls in both normal and optimized Python. '
          'All native source hashes, all page text/raster hashes, and the rational compiler example agree '
          'with an isolated native-only rebuild.\n\n'
          'The preparation anchor is superseded by this source-bound delivery. These are reproduction facts, '
          'not a formal proof certificate, independent priority clearance or a promise of journal acceptance. '
          'All independent A/B/C/D analytic closure flags remain false.\n')
    return receipt

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-isolated',action='store_true')
    parser.add_argument('--isolated',action='store_true')
    parser.add_argument('--local-missing-evidence',action='store_true')
    args=parser.parse_args()
    require(not(args.check_isolated and args.isolated),'Conflicting rebuild modes')
    print(json.dumps(build(args.local_missing_evidence,args.isolated,args.check_isolated),indent=2,sort_keys=True))

if __name__=='__main__':main()
