"""Source-bound v63 build and native-only reproduction; no network or writes to GitHub."""
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
OLD=HOME/'retained-v62'
EV=HOME/'evidence'
BASE='3be9f51ed1c33ed9262339a8d3999dab3400f33f'
REVIEW='4a99da0aab823418d95631d5dbbd8e9b8178994d'
AUDIT='02c642d3c08774d2dbaee939ffb2eee57b545f92'
FROZEN={'FROZEN_R40_REPORT.md':'86653eccc8f66078e4eea3e18af3ee6cd4db2af8',
        'FROZEN_R40_PIPELINE_AUDIT.md':'b5140e6665062ef6a5ab49a3af3d6e97ed7466d8',
        'FROZEN_PIPELINE_LEDGER.md':'c1ef29a5bcab0e2d4729c7c6815ec11e95be5808',
        'FROZEN_PIPELINE_HISTORY.md':'6041ef8b9e5e76883e86d4009c0735869b51b7a6'}
PDFS={'article':'paper.pdf','structural':'STRUCTURAL_PAPER.pdf','complete_revision':'COMPLETE_REVISION.pdf',
      'accuracy_predecessor':'ACCURACY_PREDECESSOR.pdf','strong_process_predecessor':'STRONG_PROCESS_PREDECESSOR.pdf','v62_complete':'V62_COMPLETE.pdf',
      'spectral_predecessor':'SPECTRAL_PREDECESSOR.pdf','process_predecessor':'PROCESS_PREDECESSOR.pdf','v61_complete':'V61_COMPLETE.pdf',
      'quantitative_predecessor':'QUANTITATIVE_PREDECESSOR.pdf','structural_predecessor':'STRUCTURAL_PREDECESSOR.pdf',
      'causal_predecessor':'CAUSAL_PREDECESSOR.pdf','finite_input_predecessor':'FINITE_INPUT_PREDECESSOR.pdf','orbit_predecessor':'ORBIT_PREDECESSOR.pdf',
      'boundary_predecessor':'BOUNDARY_PREDECESSOR.pdf','purification_predecessor':'PURIFICATION_PREDECESSOR.pdf',
      'radius_predecessor':'RADIUS_PREDECESSOR.pdf','scalar_predecessor':'SCALAR_PREDECESSOR.pdf',
      'companion':'COMPANION_NOTES.pdf','complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}
spec=importlib.util.spec_from_file_location('retained_v62_build',OLD/'build.py')
if spec is None or spec.loader is None:raise RuntimeError('Missing retained builder')
v62=importlib.util.module_from_spec(spec);spec.loader.exec_module(v62)
core=v62.core
require=core.require
sha=core.sha
_original_run=core.run

def _traced_run(command,cwd=None,timeout=300):
    print('[build] '+str(cwd or core.HOME)+' :: '+' '.join(map(str,command)),file=sys.stderr,flush=True)
    if cwd is None:return _original_run(command,timeout=timeout)
    return _original_run(command,cwd,timeout)

core.run=_traced_run

def save(name,data):
    (EV/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def sources():
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    retained=[OLD/name for name in manifest['files']]
    own=[p for p in HOME.rglob('*') if p.is_file()
         and not {'retained-v62','evidence','assembly','__pycache__'}.intersection(p.relative_to(HOME).parts)
         and p.suffix in {'.tex','.py','.md','.json'} and p.name!='assemble_revision.py']
    return sorted(retained+own)

def preservation(local_missing):
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_commit']==REVIEW
            and manifest['audit_commit']==AUDIT,'Frozen identity changed')
    require(manifest['review_blob']==FROZEN['FROZEN_R40_REPORT.md']
            and manifest['audit_blob']==FROZEN['FROZEN_R40_PIPELINE_AUDIT.md'],'Report blob changed')
    require(len(manifest['files'])==410,'Unexpected predecessor native count')
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
    require(status['required_revision_items']==list(range(1,11)) and status['local_comments']==list(range(1,25)), 'Incomplete external response inventory')
    require(status['pipeline_audit_release_items']==list(range(1,9)),'Incomplete audit inventory')
    require(not any(status['analytic_pipeline_closure'].values()),'Unsupported analytic closure')
    response=(HOME/'RESPONSE_TO_REFEREE.md').read_text()
    for prefix,count in [('R40 required',10),('R40 local',24),('R40 audit release',8)]:
        require(all(f'{prefix} {i:02d}' in response for i in range(1,count+1)),'Missing response: '+prefix)
    v62.EV=EV/'inherited-v62';v62.EV.mkdir(exist_ok=True)
    nested=v62.preservation(False)
    _,oldlabels=core.input_inventory(OLD,'main.tex');_,newlabels=core.input_inventory(HOME,'main.tex')
    require(oldlabels<=newlabels,'A predecessor active label was deleted')
    return {'native_predecessor_files':410,'byte_identical':True,'frozen_evidence':pins,
            'all_frozen_evidence_verified':all(pins.values()),'previous_active_labels_preserved':len(oldlabels),
            'nested_v62_preservation':nested}

def journal_package(source,pdfs,pages):
    import shutil
    with tempfile.TemporaryDirectory(prefix='gtf63-journal-package-') as td:
        root=Path(td)
        active=set()
        for name in ['quantitative.tex','structural.tex']:
            inputs,_=core.input_inventory(HOME,name);active.update(inputs)
        hashes={str(p.relative_to(HOME)):sha(p) for p in sorted(active)}
        for name in hashes:
            dest=root/'source'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HOME/name,dest)
        documents={}
        for kind,tex in [('article','quantitative.tex'),('structural','structural.tex')]:
            file=PDFS[kind];shutil.copyfile(HOME/file,root/file)
            documents[kind]={'tex':tex,'pdf':file,'pdf_sha256':pdfs[kind]['sha256'],'pages':pages[kind]}
        manifest={'schema':'gtf63.journal-manifest/1','source_commit':source,'documents':documents,'source_sha256':hashes,
                  'scope':'Two independent proof-complete papers; no historical source or predecessor PDF is required.'}
        (root/'JOURNAL_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
        (root/'README.md').write_text('# Revision 63 journal package\n\n'
            'Read paper.pdf and STRUCTURAL_PAPER.pdf as separate manuscripts. RESPONSE_TO_REFEREE.md answers both r40 reports.\n\n'
            'Run python journal_verify.py with Python, PyMuPDF and a LaTeX installation. This verifies hashes, copies only source/ '
            'to a temporary directory, typesets both papers, and compares every page text and raster. No repository, retained history, '
            'or network is required. The manifest pins the qualified source commit. It is not a formal proof or priority certificate.\n')
        shutil.copyfile(HOME/'journal_verify.py',root/'journal_verify.py')
        shutil.copyfile(HOME/'RESPONSE_TO_REFEREE.md',root/'RESPONSE_TO_REFEREE.md')
        result=json.loads(core.run([sys.executable,'journal_verify.py'],root,timeout=300))
        require(result['status']=='success','Minimal journal package did not rebuild')
        entries=[(p,str(p.relative_to(root))) for p in root.rglob('*') if p.is_file()]
        core.makezip(EV/'JOURNAL_PACKAGE.zip',entries)
        save('JOURNAL_MANIFEST.json',manifest)
        result.update(package_sha256=sha(EV/'JOURNAL_PACKAGE.zip'),package_files=len(entries))
        save('JOURNAL_REBUILD_RECEIPT.json',result)
        return result

def build(local_missing,isolated_mode,check_isolated):
    EV.mkdir(exist_ok=True)
    for path in EV.glob('page-*.png'):path.unlink()
    kept=preservation(local_missing)
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-preflight')
    before={str(p.relative_to(HOME)):sha(p) for p in sources()}
    inherited=core.regressions()
    prev61=OLD/'retained-v61';v59=prev61/'retained-v59';v58=v59/'retained-v58';v57=v58/'retained-v57';v56=v57/'retained-v56';v55=v56/'retained-v55';v54=v55/'retained-v54';v53=v54/'retained-v53'
    for name,cwd in [('v54',v54),('v55',v55),('v56',v56),('v57',v57),('v58',v58),('v59',v59),('v61',prev61),('v62',OLD)]:
        normal=json.loads(core.run([sys.executable,'check_revision.py'],cwd))
        optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],cwd))
        require(normal==optimized and normal['status']=='success',name+' normal/optimized mismatch')
        save(name.upper()+'_CHECKS.json',normal)
    normal=json.loads(core.run([sys.executable,'check_revision.py'],HOME))
    optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],HOME))
    require(normal==optimized and normal['status']=='success','V63 normal/optimized mismatch')
    save('V63_CHECKS.json',normal)
    examples={}
    for name,args in [
        ('DEFAULT_TERMINAL',['--horizon','2','--amplitude','1/2']),
        ('GENERIC_TERMINAL',['--input','GENERIC_INPUT.json','--horizon','2','--amplitude','1/2']),
        ('GENERIC_CAUSAL',['--input','GENERIC_INPUT.json','--horizon','3','--process-error','1/2']),
        ('LPS_TERMINAL',['--input','RAMANUJAN_INPUT.json','--horizon','2','--amplitude','1/2']),
        ('LPS_NOISY',['--input','RAMANUJAN_INPUT.json','--horizon','1','--error','1/2']),
        ('NO_IDLE_TERMINAL',['--input','NO_IDLE_INPUT.json','--horizon','2','--amplitude','1/2']),
        ('NO_IDLE_NOISY',['--input','NO_IDLE_INPUT.json','--horizon','1','--error','1/2'])]:
        result=json.loads(core.run([sys.executable,'qubit_compiler.py',*args,'--max-labels','100','--output',str(EV/(name+'.json'))],HOME))
        require(result['status']=='success' and result['max_row_support']<=4,'Compiler CLI failed: '+name)
        examples[name]={'labels':result['labels'],'max_row_support':result['max_row_support'],'schema':result['schema'],'sha256':sha(EV/(name+'.json'))}
    save('COMPILER_CLI_RECEIPT.json',examples)
    exclusions={}
    for name,n,k,error,b,expected in [
        ('SMALL_ERROR_EXCLUSION',100,10,'1/'+str(5**30),10,True),
        ('EXPONENTIAL_EXCLUSION',1000,5**100,'1/'+str(5**300),40,True),
        ('EXACT_EXCLUSION',32,100,'0',8,True),
        ('INCONCLUSIVE_CONTROL',1,1,'1/2',4,False)]:
        result=json.loads(core.run([sys.executable,'accuracy_profile.py','--horizon',str(n),'--width',str(k),
            '--error',error,'--block-length',str(b),'--terms','8','--output',str(EV/(name+'.json'))],HOME))
        require(result['excluded']==expected,'Exclusion CLI disagrees: '+name)
        exclusions[name]={'excluded':expected,'sha256':sha(EV/(name+'.json')),'horizon':n,'width':str(k)}
    save('EXCLUSION_CLI_RECEIPT.json',exclusions)
    core.HOME=HOME;core.EV=EV;core.PDFS=PDFS
    docs=[('article',HOME,'quantitative.tex'),('structural',HOME,'structural.tex'),('complete_revision',HOME,'main.tex'),
          ('accuracy_predecessor',OLD,'quantitative.tex'),('strong_process_predecessor',OLD,'structural.tex'),('v62_complete',OLD,'main.tex'),
          ('spectral_predecessor',prev61,'quantitative.tex'),('process_predecessor',prev61,'structural.tex'),('v61_complete',prev61,'main.tex'),
          ('quantitative_predecessor',v59,'quantitative.tex'),('structural_predecessor',v59,'structural.tex'),
          ('causal_predecessor',v59,'main.tex'),('finite_input_predecessor',v58,'main.tex'),('orbit_predecessor',v57,'main.tex'),
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
    journal=journal_package(source,pdfs,pages)
    after={str(p.relative_to(HOME)):sha(p) for p in sources()}
    require(before==after,'Build changed native sources')
    save('SOURCE_HASHES.json',after);save('PAGE_CHECKS.json',pages)
    save('THEOREM_LOCATIONS.json',locations);save('ACTIVE_INPUTS.json',inventory)
    core.makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in sources()])
    isolated=None
    if check_isolated:
        require(kept['all_frozen_evidence_verified'],'A local preflight cannot qualify publication')
        with tempfile.TemporaryDirectory(prefix='gtf63-isolated-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z:z.extractall(temp)
            other=Path(temp)/HOME.name
            output=core.run([sys.executable,'build.py','--isolated'],other,timeout=1500)
            (EV/'ISOLATED_REBUILD_LOG.txt').write_text(output)
            require(json.loads((other/'evidence/PAGE_CHECKS.json').read_text())==pages,'Isolated text/raster mismatch')
            require(json.loads((other/'evidence/SOURCE_HASHES.json').read_text())==after,'Isolated source mismatch')
            require(json.loads((other/'evidence/COMPILER_CLI_RECEIPT.json').read_text())==examples,'Isolated compiler mismatch')
            require(json.loads((other/'evidence/EXCLUSION_CLI_RECEIPT.json').read_text())==exclusions,'Isolated exclusion mismatch')
            require(json.loads((other/'evidence/JOURNAL_REBUILD_RECEIPT.json').read_text())==journal,'Isolated journal package mismatch')
            rr=json.loads((other/'evidence/BUILD_RECEIPT.json').read_text())
            require(rr['status']=='success' and rr['source_commit']==source,'Isolated source identity mismatch')
            isolated={'status':'success','all_native_source_hashes_equal':True,'all_page_text_equal':True,
                      'all_page_raster_equal':True,'all_regressions_reexecuted':True,'all_compiler_outputs_equal':True,'all_exclusion_outputs_equal':True,
                      'repository_or_network_required':False,'pages':{k:len(v) for k,v in pages.items()}}
            save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    try:
        import scipy
        sv=scipy.__version__
    except ImportError:sv=None
    receipt={'schema':'gtf63.build/1','status':'success' if kept['all_frozen_evidence_verified'] else 'local-preflight-only',
             'source_commit':source,'predecessor_publication':BASE,'review_commit':REVIEW,'audit_commit':AUDIT,
             'workflow_run':os.environ.get('GITHUB_RUN_ID'),'documents':pdfs,'preservation':kept,
             'native_source_files':len(after),'normal_optimized_agreement':True,
             'new_exact_finite_assertions':normal['exact_finite_assertions'],
             'new_named_negative_controls':len(normal['negative_controls_detected']),
             'new_negative_control_executions':2*len(normal['negative_controls_detected']),
             'inherited_regression_suites':['v62','v61','v59','v58','v57','v56','v55','v54']+list(inherited),
             'compiler_examples':examples,'exclusion_examples':exclusions,'journal_package':journal,'isolated_rebuild':isolated,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
             'dependency_versions':{'python':sys.version.split()[0],'sympy':sympy.__version__,'pymupdf':fitz.VersionBind,'scipy_optional_accelerator':sv},
             'final_head_ci':'separate read-only verifier; this build receipt is not its result',
             'scope':'Finite rational regressions, source preservation, generic compiler execution, exact-rational exclusion examples and rendered reproduction. Universal proofs, external priority, signatures and editorial acceptance are not certified.'}
    save('BUILD_RECEIPT.json',receipt)
    essential=[HOME/n for n in ['README.md','RESPONSE_TO_REFEREE.md','HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md',
                                 'PROOF_STATUS.json','PRESERVATION_MANIFEST.json','REVISION_SCOPE.md','GENERIC_INPUT.json','RAMANUJAN_INPUT.json','NO_IDLE_INPUT.json','PROOF_AUDIT.md']]
    essential += [HOME/n for n in FROZEN if (HOME/n).exists()]
    evidence=[EV/n for n in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                            'V63_CHECKS.json','EXCLUSION_CLI_RECEIPT.json','SMALL_ERROR_EXCLUSION.json','EXPONENTIAL_EXCLUSION.json','EXACT_EXCLUSION.json','INCONCLUSIVE_CONTROL.json','JOURNAL_REBUILD_RECEIPT.json','JOURNAL_MANIFEST.json','JOURNAL_PACKAGE.zip','COMPILER_CLI_RECEIPT.json','DEFAULT_TERMINAL.json','GENERIC_TERMINAL.json','GENERIC_CAUSAL.json','LPS_TERMINAL.json','LPS_NOISY.json','NO_IDLE_TERMINAL.json','NO_IDLE_NOISY.json']]
    if isolated:evidence.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    full=[HOME/n for n in PDFS.values()]+essential+evidence+[EV/'PAGE_CHECKS.json',EV/'ACTIVE_INPUTS.json']
    core.makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in full])
    focused=[HOME/'paper.pdf',HOME/'STRUCTURAL_PAPER.pdf',*essential,*evidence]
    core.makezip(EV/'FOCUSED_REVIEW_PACKAGE.zip',[(p,p.name) for p in focused])
    if check_isolated and not isolated_mode:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V63_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 63\n\n'
          '**Stochastic Widths at Exponential Accuracy and Spectral Entropy on Spheres.**\n\n'
          '**Finite Physical Actions and a Strong Converse for Repeatable Observations.**\n\n'
          f'Qualified native source: `{source}`. Base v62: `{BASE}`. External r40: `{REVIEW}`; audit r40: `{AUDIT}`.\n\n'
          f'[Quantitative article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
          f'[Structural article ({pdfs["structural"]["pages"]} pages)](papers/{HOME.name}/STRUCTURAL_PAPER.pdf) · '
          f'[Archival complete edition ({pdfs["complete_revision"]["pages"]} pages)](papers/{HOME.name}/COMPLETE_REVISION.pdf) · '
          f'[Response to both reports](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
          f'[Build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json) · '
          f'[Minimal journal package](papers/{HOME.name}/evidence/JOURNAL_PACKAGE.zip) · '
          f'[Full referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip)\n\n'
          'Work branch: `revision/general-theta-foundations-i-v63-accuracy-profile-2026-09-28`.\n'
          'Referee branch: `revision/general-theta-foundations-i-v63-referee-ready-2026-09-28`.\n\n'
          'New proofs: logarithmic block entropy and an arbitrary-profile budget; a uniform exponential-scale crossover '
          'for spherical Ramanujan alphabets; the full rate min(a,log 5) for the six rational LPS Bloch commands. '
          'Exact profiles, subexponential matching, return-free occupation and the repeatable-probe strong converse are inherited.\n\n'
          f'All 410 predecessor native files and {kept["previous_active_labels_preserved"]} active mathematical labels are preserved. '
          f'New finite checks: {normal["exact_finite_assertions"]} assertions and {len(normal["negative_controls_detected"])} named negative controls in both Python modes. '
          f'All {len(pdfs)} documents and seven compiler plus four exclusion examples agree with the isolated native-only rebuild. '
          f'The minimal journal package independently rebuilds both focused articles from {journal["active_tex_files"]} active TeX files without histories.\n\n'
          'Final-head qualification is a separate read-only Actions run on a connector-authored request commit. '
          'Its FINAL_HEAD_ATTESTATION is recorded outside the reviewed tree and must match the exact final SHA. '
          'This entry supersedes the preparation anchor but does not itself claim that later verifier result. '
          'No formal proof certificate, independent human priority clearance, signature, acceptance guarantee, '
          'optimal leading constants, uniform multiplicative crossover equivalent or A/B/C/D closure is asserted.\n')
    return receipt

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check-isolated',action='store_true')
    parser.add_argument('--isolated',action='store_true');parser.add_argument('--local-missing-evidence',action='store_true')
    args=parser.parse_args();require(not(args.check_isolated and args.isolated),'Conflicting modes')
    print(json.dumps(build(args.local_missing_evidence,args.isolated,args.check_isolated),indent=2,sort_keys=True))
if __name__=='__main__':main()
