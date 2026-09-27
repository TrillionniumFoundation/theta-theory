"""Source-bound v59 build and native-only reproduction; no network or writes to GitHub."""
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
OLD=HOME/'retained-v58'
EV=HOME/'evidence'
BASE='27be4b236b9336bbfa2fa855dec3a346d63b8be7'
REVIEW='6daa50db42873a4a32cd3c1610f19630f5739b51'
AUDIT='849cbc2fb4d589d8fd13d8c7d34492af191e0f75'
FROZEN={'FROZEN_R39_REPORT.md':'5ba98081a61e12f11a0858e696bf79492c106ae9',
        'FROZEN_R39_PIPELINE_AUDIT.md':'6f36057b0f12c0a1d71798b6b9f0fe9fc0f592a9',
        'FROZEN_PIPELINE_LEDGER.md':'c1ef29a5bcab0e2d4729c7c6815ec11e95be5808',
        'FROZEN_PIPELINE_HISTORY.md':'6041ef8b9e5e76883e86d4009c0735869b51b7a6'}
PDFS={'article':'paper.pdf','structural':'STRUCTURAL_PAPER.pdf','complete_revision':'COMPLETE_REVISION.pdf',
      'quantitative_predecessor':'QUANTITATIVE_PREDECESSOR.pdf','structural_predecessor':'STRUCTURAL_PREDECESSOR.pdf',
      'finite_input_predecessor':'FINITE_INPUT_PREDECESSOR.pdf','orbit_predecessor':'ORBIT_PREDECESSOR.pdf',
      'boundary_predecessor':'BOUNDARY_PREDECESSOR.pdf','purification_predecessor':'PURIFICATION_PREDECESSOR.pdf',
      'radius_predecessor':'RADIUS_PREDECESSOR.pdf','scalar_predecessor':'SCALAR_PREDECESSOR.pdf',
      'companion':'COMPANION_NOTES.pdf','complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}
spec=importlib.util.spec_from_file_location('retained_v58_build',OLD/'build.py')
if spec is None or spec.loader is None:raise RuntimeError('Missing retained builder')
v58=importlib.util.module_from_spec(spec);spec.loader.exec_module(v58)
core=v58.core
require=core.require
sha=core.sha

def save(name,data):
    (EV/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def sources():
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    retained=[OLD/name for name in manifest['files']]
    own=[p for p in HOME.rglob('*') if p.is_file()
         and not {'retained-v58','evidence','assembly','__pycache__'}.intersection(p.relative_to(HOME).parts)
         and p.suffix in {'.tex','.py','.md','.json'} and p.name!='assemble_revision.py']
    return sorted(retained+own)

def preservation(local_missing):
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_commit']==REVIEW
            and manifest['audit_commit']==AUDIT,'Frozen identity changed')
    require(manifest['review_blob']==FROZEN['FROZEN_R39_REPORT.md']
            and manifest['audit_blob']==FROZEN['FROZEN_R39_PIPELINE_AUDIT.md'],'Report blob changed')
    require(len(manifest['files'])==230,'Unexpected predecessor native count')
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
    require(status['required_revision_items']==list(range(1,11)) and status['local_comments']==list(range(1,19)), 'Incomplete external response inventory')
    require(status['pipeline_audit_release_items']==list(range(1,7)),'Incomplete audit inventory')
    require(not any(status['analytic_pipeline_closure'].values()),'Unsupported analytic closure')
    response=(HOME/'RESPONSE_TO_REFEREE.md').read_text()
    for prefix,count in [('R39 required',10),('R39 local',18),('R39 audit release',6)]:
        require(all(f'{prefix} {i:02d}' in response for i in range(1,count+1)),'Missing response: '+prefix)
    v58.EV=EV/'inherited-v58';v58.EV.mkdir(exist_ok=True)
    nested=v58.preservation(False)
    _,oldlabels=core.input_inventory(OLD,'main.tex');_,newlabels=core.input_inventory(HOME,'main.tex')
    require(oldlabels<=newlabels,'A predecessor active label was deleted')
    return {'native_predecessor_files':230,'byte_identical':True,'frozen_evidence':pins,
            'all_frozen_evidence_verified':all(pins.values()),'previous_active_labels_preserved':len(oldlabels),
            'nested_v58_preservation':nested}

def build(local_missing,isolated_mode,check_isolated):
    EV.mkdir(exist_ok=True)
    for path in EV.glob('page-*.png'):path.unlink()
    kept=preservation(local_missing)
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-preflight')
    before={str(p.relative_to(HOME)):sha(p) for p in sources()}
    inherited=core.regressions()
    v57=OLD/'retained-v57';v56=v57/'retained-v56';v55=v56/'retained-v55';v54=v55/'retained-v54';v53=v54/'retained-v53'
    for name,cwd in [('v54',v54),('v55',v55),('v56',v56),('v57',v57),('v58',OLD)]:
        normal=json.loads(core.run([sys.executable,'check_revision.py'],cwd))
        optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],cwd))
        require(normal==optimized and normal['status']=='success',name+' normal/optimized mismatch')
        save(name.upper()+'_CHECKS.json',normal)
    normal=json.loads(core.run([sys.executable,'check_revision.py'],HOME))
    optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],HOME))
    require(normal==optimized and normal['status']=='success','V59 normal/optimized mismatch')
    save('V59_CHECKS.json',normal)
    examples={}
    for name,args in [
        ('DEFAULT_TERMINAL',['--horizon','2','--amplitude','1/2']),
        ('GENERIC_TERMINAL',['--input','GENERIC_INPUT.json','--horizon','2','--amplitude','1/2']),
        ('GENERIC_CAUSAL',['--input','GENERIC_INPUT.json','--horizon','3','--process-error','1/2'])]:
        result=json.loads(core.run([sys.executable,'qubit_compiler.py',*args,'--max-labels','100','--output',str(EV/(name+'.json'))],HOME))
        require(result['status']=='success' and result['max_row_support']<=4,'Compiler CLI failed: '+name)
        examples[name]={'labels':result['labels'],'max_row_support':result['max_row_support'],'schema':result['schema'],'sha256':sha(EV/(name+'.json'))}
    save('COMPILER_CLI_RECEIPT.json',examples)
    core.HOME=HOME;core.EV=EV;core.PDFS=PDFS
    docs=[('article',HOME,'quantitative.tex'),('structural',HOME,'structural.tex'),('complete_revision',HOME,'main.tex'),
          ('quantitative_predecessor',OLD,'quantitative.tex'),('structural_predecessor',OLD,'structural.tex'),
          ('finite_input_predecessor',OLD,'main.tex'),('orbit_predecessor',v57,'main.tex'),
          ('boundary_predecessor',v56,'main.tex'),('purification_predecessor',v55,'main.tex'),
          ('radius_predecessor',v54,'main.tex'),('scalar_predecessor',v53,'main.tex'),
          ('companion',v53,'supplement-notes.tex'),('complete_supplement',v53/'retained-v52','main.tex')]
    pdfs={};pages={};locations={};inventory={}
    for kind,cwd,name in docs:
        inputs,labels=core.input_inventory(cwd,name)
        pdfs[kind],pages[kind],locations[kind]=core.typeset(kind,cwd,name)
        require(labels<=set(locations[kind]),'Unloaded labels: '+kind)
        # Hash every rendered page, but retain only representative archival previews.
        if kind not in {'article','structural'}:
            keep={1,(len(pages[kind])+1)//2,len(pages[kind])}
            for preview in EV.glob('page-'+kind+'-*.png'):
                if int(preview.stem.rsplit('-',1)[1]) not in keep:preview.unlink()
        inventory[kind]={'inputs':[str(p.relative_to(HOME)) for p in inputs],'labels':sorted(labels),'label_count':len(labels)}
    status=json.loads((HOME/'PROOF_STATUS.json').read_text())
    require(set(status['theorems'])<=set(locations['complete_revision']),'New theorem absent from complete edition')
    require(set(status['quantitative_theorems'])<=set(locations['article']),'Quantitative proof missing')
    require(set(status['structural_theorems'])<=set(locations['structural']),'Structural proof missing')
    after={str(p.relative_to(HOME)):sha(p) for p in sources()}
    require(before==after,'Build changed native sources')
    save('SOURCE_HASHES.json',after);save('PAGE_CHECKS.json',pages)
    save('THEOREM_LOCATIONS.json',locations);save('ACTIVE_INPUTS.json',inventory)
    core.makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in sources()])
    isolated=None
    if check_isolated:
        require(kept['all_frozen_evidence_verified'],'A local preflight cannot qualify publication')
        with tempfile.TemporaryDirectory(prefix='gtf59-isolated-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z:z.extractall(temp)
            other=Path(temp)/HOME.name
            output=core.run([sys.executable,'build.py','--isolated'],other,timeout=1500)
            (EV/'ISOLATED_REBUILD_LOG.txt').write_text(output)
            require(json.loads((other/'evidence/PAGE_CHECKS.json').read_text())==pages,'Isolated text/raster mismatch')
            require(json.loads((other/'evidence/SOURCE_HASHES.json').read_text())==after,'Isolated source mismatch')
            require(json.loads((other/'evidence/COMPILER_CLI_RECEIPT.json').read_text())==examples,'Isolated compiler mismatch')
            rr=json.loads((other/'evidence/BUILD_RECEIPT.json').read_text())
            require(rr['status']=='success' and rr['source_commit']==source,'Isolated source identity mismatch')
            isolated={'status':'success','all_native_source_hashes_equal':True,'all_page_text_equal':True,
                      'all_page_raster_equal':True,'all_regressions_reexecuted':True,'all_compiler_outputs_equal':True,
                      'repository_or_network_required':False,'pages':{k:len(v) for k,v in pages.items()}}
            save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    try:
        import scipy
        sv=scipy.__version__
    except ImportError:sv=None
    receipt={'schema':'gtf59.build/1','status':'success' if kept['all_frozen_evidence_verified'] else 'local-preflight-only',
             'source_commit':source,'predecessor_publication':BASE,'review_commit':REVIEW,'audit_commit':AUDIT,
             'workflow_run':os.environ.get('GITHUB_RUN_ID'),'documents':pdfs,'preservation':kept,
             'native_source_files':len(after),'normal_optimized_agreement':True,
             'new_exact_finite_assertions':normal['exact_finite_assertions'],
             'new_named_negative_controls':len(normal['negative_controls_detected']),
             'new_negative_control_executions':2*len(normal['negative_controls_detected']),
             'inherited_regression_suites':['v58','v57','v56','v55','v54']+list(inherited),
             'compiler_examples':examples,'isolated_rebuild':isolated,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
             'dependency_versions':{'python':sys.version.split()[0],'sympy':sympy.__version__,'pymupdf':fitz.VersionBind,'scipy_optional_accelerator':sv},
             'final_head_ci':'separate read-only verifier; this build receipt is not its result',
             'scope':'Finite rational regressions, source preservation, generic compiler execution and rendered reproduction. Universal proofs, external priority, signatures and editorial acceptance are not certified.'}
    save('BUILD_RECEIPT.json',receipt)
    essential=[HOME/n for n in ['README.md','RESPONSE_TO_REFEREE.md','HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md',
                                 'PROOF_STATUS.json','PRESERVATION_MANIFEST.json','REVISION_SCOPE.md','GENERIC_INPUT.json']]
    essential += [HOME/n for n in FROZEN if (HOME/n).exists()]
    evidence=[EV/n for n in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                            'V59_CHECKS.json','COMPILER_CLI_RECEIPT.json','DEFAULT_TERMINAL.json','GENERIC_TERMINAL.json','GENERIC_CAUSAL.json']]
    if isolated:evidence.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    full=[HOME/n for n in PDFS.values()]+essential+evidence+[EV/'PAGE_CHECKS.json',EV/'ACTIVE_INPUTS.json']
    core.makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in full])
    focused=[HOME/'paper.pdf',HOME/'STRUCTURAL_PAPER.pdf',*essential,*evidence]
    core.makezip(EV/'FOCUSED_REVIEW_PACKAGE.zip',[(p,p.name) for p in focused])
    if check_isolated and not isolated_mode:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V59_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 59\n\n'
          '**Finite physical actions, repeatable observation processes, and adaptive rational realization.**\n\n'
          f'Qualified native source: `{source}`. Base v58: `{BASE}`. External r39: `{REVIEW}`; audit r39: `{AUDIT}`.\n\n'
          f'[Quantitative article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
          f'[Structural article ({pdfs["structural"]["pages"]} pages)](papers/{HOME.name}/STRUCTURAL_PAPER.pdf) · '
          f'[Complete edition ({pdfs["complete_revision"]["pages"]} pages)](papers/{HOME.name}/COMPLETE_REVISION.pdf) · '
          f'[Response to both reports](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
          f'[Build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json) · '
          f'[Focused review package](papers/{HOME.name}/evidence/FOCUSED_REVIEW_PACKAGE.zip)\n\n'
          'Work branch: `revision/general-theta-foundations-i-v59-causal-realization-2026-09-27`.\n'
          'Referee branch: `revision/general-theta-foundations-i-v59-referee-ready-2026-09-27`.\n\n'
          'New proofs: bounded causal width at every fixed whole-transcript TV error below one iff the future-response quotient is finite; '
          'eventual exact minimum below one half; all-profile occupation; adaptive rational/dyadic instruments; and explicit spectral-gap-free process testing bounds. '
          'The terminal logarithmic gap is retained. Nondisturbing classical probes are not a quantum measurement claim.\n\n'
          f'All 230 predecessor native files and {kept["previous_active_labels_preserved"]} active mathematical labels are preserved. '
          f'New finite checks: {normal["exact_finite_assertions"]} assertions and {len(normal["negative_controls_detected"])} named negative controls in both Python modes. '
          'All thirteen documents and all generic compiler examples agree with the isolated native-only rebuild.\n\n'
          'Final-head qualification is a second, read-only Actions run on a connector-authored request commit after this publication. '
          'That request adds only a root provenance record; its exact head is pinned for review after success. '
          'Read its external FINAL_HEAD_ATTESTATION artifact and check the successful Actions run against the exact reviewed head SHA. The verifier records its conclusion outside the reviewed commit. '
          'No signature, independent priority clearance, formal proof certificate, journal acceptance or A/B/C/D closure is asserted.\n')
    return receipt

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check-isolated',action='store_true')
    parser.add_argument('--isolated',action='store_true');parser.add_argument('--local-missing-evidence',action='store_true')
    args=parser.parse_args();require(not(args.check_isolated and args.isolated),'Conflicting modes')
    print(json.dumps(build(args.local_missing_evidence,args.isolated,args.check_isolated),indent=2,sort_keys=True))
if __name__=='__main__':main()
