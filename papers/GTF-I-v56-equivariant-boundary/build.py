"""Source-bound v56 qualification, including independent native-only rebuilding.

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
OLD=HOME/'retained-v55'
EV=HOME/'evidence'
BASE='00a0864003790aa3efcdc7f88358b6fa27ffe868'
REVIEW='0b2226b43a10f10c4ed0c5f969c058cde8d59230'
REPORT='d9841d9b928800977e5965d5d6df52347fa64547'
FROZEN={'FROZEN_R37_REPORT.md':REPORT,
        'FROZEN_PIPELINE_LEDGER.md':'c1ef29a5bcab0e2d4729c7c6815ec11e95be5808',
        'FROZEN_PIPELINE_HISTORY.md':'6041ef8b9e5e76883e86d4009c0735869b51b7a6'}
PDFS={'article':'paper.pdf','purification_predecessor':'PURIFICATION_PREDECESSOR.pdf',
      'radius_predecessor':'RADIUS_PREDECESSOR.pdf','scalar_predecessor':'SCALAR_PREDECESSOR.pdf',
      'companion':'COMPANION_NOTES.pdf','complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}
spec=importlib.util.spec_from_file_location('retained_v55_build',OLD/'build.py')
if spec is None or spec.loader is None:raise RuntimeError('Missing retained builder')
v55=importlib.util.module_from_spec(spec);spec.loader.exec_module(v55)
core=v55.core
require=core.require
sha=core.sha

def save(name,data):
    (EV/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def sources():
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    retained=[OLD/name for name in manifest['files']]
    own=[p for p in HOME.rglob('*') if p.is_file()
         and not {'retained-v55','evidence','assembly','__pycache__'}.intersection(p.relative_to(HOME).parts)
         and p.suffix in {'.tex','.py','.md','.json'} and p.name!='assemble_revision.py']
    return sorted(retained+own)

def preservation(local_missing):
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_commit']==REVIEW
            and manifest['review_blob']==REPORT,'Frozen identities changed')
    require(len(manifest['files'])==114,'Unexpected predecessor native count')
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
    require(status['required_revision_items']==['7.'+str(i) for i in range(1,8)],'Incomplete major inventory')
    require(status['local_comments']==list(range(1,33)),'Incomplete local inventory')
    require(not any(status['analytic_pipeline_closure'].values()),'Unsupported analytic closure')
    response=(HOME/'RESPONSE_TO_REFEREE.md').read_text()
    require(all(f'R37 local {i:02d}' in response for i in range(1,33)),'Missing local response')
    require(all('R37 7.'+str(i)+' ' in response for i in range(1,8)),'Missing major response')
    v55.EV=EV/'inherited-v55';v55.EV.mkdir(exist_ok=True)
    nested=v55.preservation(False)
    _,oldlabels=core.input_inventory(OLD,'main.tex')
    _,newlabels=core.input_inventory(HOME,'main.tex')
    require(oldlabels<=newlabels,'A previous active mathematical label was deleted')
    return {'native_predecessor_files':114,'byte_identical':True,'frozen_evidence':pins,
            'controlling_report_verified':pins['FROZEN_R37_REPORT.md'],
            'all_frozen_evidence_verified':all(pins.values()),
            'previous_active_labels_preserved':len(oldlabels),'nested_v55_preservation':nested}

def build(local_missing,isolated_mode,check_isolated):
    EV.mkdir(exist_ok=True)
    for path in EV.glob('page-*.png'):path.unlink()
    (EV/'FAILED_COMMAND.txt').unlink(missing_ok=True)
    kept=preservation(local_missing)
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-preflight')
    before={str(p.relative_to(HOME)):sha(p) for p in sources()}
    # The retained core still points to its v53/v52 source here.
    inherited=core.regressions()
    for name,cwd in [('v54',OLD/'retained-v54'),('v55',OLD)]:
        normal=json.loads(core.run([sys.executable,'check_revision.py'],cwd))
        optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],cwd))
        require(normal==optimized and normal['status']=='success',name+' normal/optimized mismatch')
        save(name.upper()+'_CHECKS.json',normal)
    normal=json.loads(core.run([sys.executable,'check_revision.py'],HOME))
    optimized=json.loads(core.run([sys.executable,'-O','check_revision.py'],HOME))
    require(normal==optimized and normal['status']=='success','V56 normal/optimized mismatch')
    save('V56_CHECKS.json',normal)
    core.HOME=HOME;core.EV=EV;core.PDFS=PDFS
    v54=OLD/'retained-v54';v53=v54/'retained-v53'
    docs=[('article',HOME,'main.tex'),('purification_predecessor',OLD,'main.tex'),
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
    require(int(locations['article']['tab:map56']['page'])<=5,'The theorem map was deferred beyond the introduction')
    after={str(p.relative_to(HOME)):sha(p) for p in sources()}
    require(before==after,'Build changed native sources')
    save('SOURCE_HASHES.json',after);save('PAGE_CHECKS.json',pages)
    save('THEOREM_LOCATIONS.json',locations);save('ACTIVE_INPUTS.json',inventory)
    core.makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in sources()])
    isolated=None
    if check_isolated:
        require(kept['all_frozen_evidence_verified'],'An incomplete local preflight cannot qualify publication')
        with tempfile.TemporaryDirectory(prefix='gtf56-isolated-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z:z.extractall(temp)
            other=Path(temp)/HOME.name
            output=core.run([sys.executable,'build.py','--isolated'],other,timeout=1200)
            (EV/'ISOLATED_REBUILD_LOG.txt').write_text(output)
            require(json.loads((other/'evidence/PAGE_CHECKS.json').read_text())==pages,'Isolated text/raster mismatch')
            require(json.loads((other/'evidence/SOURCE_HASHES.json').read_text())==after,'Isolated source mismatch')
            receipt=json.loads((other/'evidence/BUILD_RECEIPT.json').read_text())
            require(receipt['status']=='success' and receipt['source_commit']==source,'Isolated source identity mismatch')
            isolated={'status':'success','all_page_text_equal':True,'all_page_raster_equal':True,
                      'all_native_source_hashes_equal':True,'all_regressions_reexecuted':True,
                      'repository_or_network_required':False,'pages':{k:len(v) for k,v in pages.items()}}
            save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    receipt={'schema':'gtf56.build/1','status':'success' if kept['all_frozen_evidence_verified'] else 'local-preflight-only',
             'source_commit':source,'predecessor_publication':BASE,'review_commit':REVIEW,
             'workflow_run':os.environ.get('GITHUB_RUN_ID'),'documents':pdfs,'preservation':kept,
             'native_source_files':len(after),'normal_optimized_agreement':True,
             'new_exact_finite_assertions':normal['exact_finite_assertions'],
             'new_named_negative_controls':len(normal['negative_controls_detected']),
             'new_negative_control_executions':2*len(normal['negative_controls_detected']),
             'inherited_regression_suites':['v55','v54']+list(inherited),
             'isolated_rebuild':isolated,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
             'dependency_versions':{'python':sys.version.split()[0],'sympy':sympy.__version__,'pymupdf':fitz.VersionBind},
             'scope':'Finite exact regression, native source preservation and complete rendered reproduction. Universal proofs, imported spectral gaps and existential-real hardness are written mathematics, not certified by these tests. No independent priority, editorial acceptance or analytic pipeline closure is asserted.'}
    save('BUILD_RECEIPT.json',receipt)
    package=[HOME/n for n in [*PDFS.values(),'README.md','RESPONSE_TO_REFEREE.md','HISTORY_AND_PIPELINE_AUDIT.md',
                             'LITERATURE_AUDIT.md','PROOF_STATUS.json','PRESERVATION_MANIFEST.json','REVISION_SCOPE.md']]
    package += [HOME/n for n in FROZEN if (HOME/n).exists()]
    package += [EV/n for n in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                               'V56_CHECKS.json','V55_CHECKS.json','V54_CHECKS.json','PAGE_CHECKS.json','ACTIVE_INPUTS.json',
                               'FINITE_GROUP_EXAMPLE.json','FINITE_GROUP_EXAMPLE.smt2']]
    if isolated:package.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    core.makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package])
    if check_isolated and not isolated_mode:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V56_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 56\n\n'
          '**Clocked Stochastic Realization and Finite Observable Quotients**\n\n'
          f'Qualified native source: `{source}`. Frozen r37: `{REVIEW}`. Base v55: `{BASE}`.\n\n'
          f'[Main article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
          f'[Readable source](papers/{HOME.name}/main.tex) · '
          f'[Response to r37](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
          f'[Actual build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json) · '
          f'[Portable referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip)\n\n'
          'Work branch: `revision/general-theta-foundations-i-v56-equivariant-boundary-2026-09-27`.\n'
          'Referee branch: `revision/general-theta-foundations-i-v56-referee-ready-2026-09-27`.\n\n'
          'Principal additions: same-width stationarization under eventual approximate returns; '
          'physical-equivariant purification; equality-inclusive clocked finite-quotient classification; '
          'exact phase minima; nonabelian spherical rates up to a logarithm; existential-real completeness '
          'for finite-group data; explicit precision and random-bit budgets.\n\n'
          f'All 114 predecessor native files and {kept["previous_active_labels_preserved"]} active labels are preserved. '
          'The six rebuilt documents have '+', '.join(str(pdfs[k]['pages']) for k in PDFS)+' pages. '
          f'The new exact finite regression executes {normal["exact_finite_assertions"]:,} assertions and '
          f'{len(normal["negative_controls_detected"])} named negative controls in both normal and optimized Python. '
          'Every native source hash and all page text/raster hashes agree with the isolated rebuild.\n\n'
          'The preparation anchor is superseded by this actual source-bound qualification. '
          'This evidence concerns reproduction, not a formal proof certificate, independent priority clearance '
          'or a promise of journal acceptance. Independent A/B/C/D analytic closure flags remain false.\n')
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
