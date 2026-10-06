#!/usr/bin/env python3
"""Source-bound v96 build, complete preservation, and read-only reconstruction.

--preflight is deliberately not a publication qualification. Production builds
must run at an actual native-source Git commit. --verify-published checks that
source object and rebuilds the source archive without changing the submission.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor
import fitz

ROOT=Path(__file__).resolve().parent
BASE='db6739da3487be8787a67fc175b9086bd62f0e80'
EPOCH='1791244800'
DOCS={'quantitative.tex':'paper.pdf','supplement.tex':'BINARY_SUPPLEMENT.pdf','structural.tex':'STRUCTURAL_PAPER.pdf',
      'main.tex':'COMPLETE_REVISION.pdf'}
NEW_SECTIONS=['sections/87-exact-initial-spectral-values.tex','sections/89-receiver-message-criterion.tex','sections/90-finite-attainment-and-example.tex']
NEW_LABELS=['lem:watermap96', 'lem:postponement96', 'thm:messagecriterion96', 'cor:messageperturb96', 'prop:finiteinstrument96', 'prop:qutritwitness96']
JOURNAL_EXTRAS={'paper.pdf','BINARY_SUPPLEMENT.pdf','REPRODUCIBILITY.md','JOURNAL_README.md','requirements.txt','journal_verify.py','THEOREM_MAP.md','RESPONSE_TO_REFEREE.md'}
# These established parsing/rendering helpers and regression names are retained
# byte-for-byte. All tests below are executed anew on this revision's files.
spec=importlib.util.spec_from_file_location('v81_build_helpers',ROOT/'predecessor-v81-audit/build_revision.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
sha=old.sha;require=old.require;put=old.put;graph=old.graph;sources=old.sources
SCRIPTS=(*old.REGRESSION_SCRIPTS,'finite_outcome_check.py','covariance_check.py','support_check.py','curve_check.py','cone_check.py','block_check.py','feedback_check.py','profile_check.py','resource_check.py','memory_check.py','budget_domain_check.py','reset_variational_check.py','equal_prior_check.py','rigidity_check.py','rank_hierarchy_check.py','spectral_rigidity_check.py','spectral_value_check.py','equal_prior_initial_check.py','referee_resolution_check.py')


def run(cmd,cwd=ROOT,timeout=240,env=None):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=timeout,env=env)
    require(p.returncode==0,'command failed: '+str(cmd)+'\n'+p.stdout[-6000:]+'\n'+p.stderr[-6000:])
    return p.stdout


def git(*args):
    return run(['git',*args]).strip()


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def proof_retained(name,digest):
    data=(ROOT/name).read_bytes()
    if sha(data)==digest:return True
    entries=json.loads((ROOT/'EDITORIAL_INSERTIONS.json').read_text())['insertions']
    require(name in entries,'unregistered proof edit: '+name)
    for addition in entries[name]:
        encoded=addition.encode('utf-8')
        require(data.count(encoded)==1,'missing or repeated editorial insertion: '+name)
        data=data.replace(encoded,b'')
    return sha(data)==digest


def check_source():
    inv=sources(ROOT);baseline=json.loads((ROOT/'V94_BASELINE.json').read_text())
    require(baseline['commit']==BASE and baseline['source_commit']=='24f48c90d6bcc1eae1d4c38ac5195405ac21da7d',
            'wrong frozen v94 identity')
    local=json.loads((ROOT/'LOCAL_V95_IMPORT.json').read_text())
    previous={**baseline['files'],**local['inventory_overrides_on_V94_BASELINE']}
    require(len(previous)==local['source_files']==896,'local import inventory differs')
    require(local['these_local_commits_are_not_remote_ancestors'] is True,
            'local provenance may not be promoted to remote ancestry')
    changed=[]
    for name,digest in baseline['files'].items():
        require(name in inv,'removed v94 native file: '+name)
        if inv[name]!=digest:
            require(sha((ROOT/'predecessor-v94-audit'/name).read_bytes())==digest,
                    'missing exact v94 predecessor: '+name)
            changed.append(name)
    transforms=json.loads((ROOT/'EDITORIAL_TRANSFORMS_V96.json').read_text())['transforms']
    for name,digest in previous.items():
        require(name in inv,'removed local v95 native file: '+name)
        if inv[name]!=digest:
            require(sha((ROOT/'unpublished-local-v95-audit'/name).read_bytes())==digest,
                    'missing exact local v95 predecessor: '+name)
        if name.startswith('sections/') and inv[name]!=digest:
            require(name in transforms,'unregistered inherited proof edit: '+name)
            data=(ROOT/name).read_text()
            for edit in reversed(transforms[name]):
                require(data.count(edit['new'])==1,'ambiguous editorial reversal: '+name)
                data=data.replace(edit['new'],edit['old'],1)
            require(sha(data.encode())==digest,'inherited proof not recovered: '+name)
    graphs={}
    for entry in DOCS:
        files,entry_labels=graph(ROOT,entry)
        graphs[entry]={'files':sorted(files),'labels':sorted(entry_labels)}
    joint_files=set(graphs['quantitative.tex']['files'])|set(graphs['supplement.tex']['files'])
    joint_labels=set(graphs['quantitative.tex']['labels'])|set(graphs['supplement.tex']['labels'])
    for entry,prior in baseline['graphs'].items():
        files=joint_files if entry in ('quantitative.tex','supplement.tex') else set(graphs[entry]['files'])
        active=joint_labels if entry in ('quantitative.tex','supplement.tex') else set(graphs[entry]['labels'])
        require(set(prior['labels'])<=active,'inherited active label lost: '+entry)
        for name in prior['files']:
            if name.startswith('sections/'):require(name in files,'inherited proof inactive: '+name)
            if entry=='structural.tex':
                require(name in files and inv[name]==baseline['files'][name],'structural source changed: '+name)
    require(not(set(graphs['quantitative.tex']['labels'])&set(graphs['supplement.tex']['labels'])),
            'ambiguous current primary/supplement labels')
    # The entire imported mathematical corpus remains active in the complete edition.
    require(len(graphs['main.tex']['labels'])>=local['complete_labels'],'complete label count decreased')
    for name in previous:
        if name.startswith('sections/') and name.endswith('.tex'):
            # Some inherited bibliography files are not mathematical modules.
            if name in baseline['graphs']['main.tex']['files'] or name=='sections/88-equal-prior-initial-spectra.tex':
                require(name in graphs['main.tex']['files'],'imported complete proof inactive: '+name)
    for name in NEW_SECTIONS:
        require(all(name in graphs[e]['files'] for e in ('main.tex','quantitative.tex')),'new proof inactive: '+name)
    found=[]
    for name in NEW_SECTIONS:
        found+=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]*96)\}',(ROOT/name).read_text())
    require(sorted(found)==sorted(NEW_LABELS),'new theorem inventory differs')
    for name,digest in [
      ('FROZEN_R62_REPORT.md','232a7c9e2c7397acb171df115d5ea1f1792ecbfc'),
      ('FROZEN_R61_REPORT.md','5c83d11eab4e74b0856d21ee5e9ed271c79c224a'),
      ('FROZEN_R61_PIPELINE_AUDIT.md','fe047c17e3676a0bbe77d39ae5f0f12d003d91de')]:
        require(blob((ROOT/name).read_bytes())==digest,'frozen controlling report changed: '+name)
    require('Revision 96' in (ROOT/'main.tex').read_text(),'stale complete-edition PDF title')
    status=json.loads((ROOT/'PROOF_STATUS.json').read_text())
    require(status['revision']==96 and all(v is False for v in status['analytic_pipeline_closure'].values()),
            'wrong revision or promoted analytic aggregate')
    require(status['external_status']['independent_human_priority_clearance'] is False,'human priority approval invented')
    relocated=sorted(set(baseline['graphs']['quantitative.tex']['labels'])-set(graphs['quantitative.tex']['labels']))
    return inv,{'schema':'gtf96.source-check/1','status':'success','base_commit':BASE,
      'controlling_report_commit':'58581d5a6391642fb0849f8c8bb49c8c0c20b63c',
      'predecessor_native_files':len(baseline['files']),'local_import_native_files':len(previous),
      'source_files':len(inv),'changed_predecessor_paths':changed,
      'all_original_proof_text_retained':True,'all_predecessor_sections_byte_identical':False,
      'reversible_editorial_sections':sorted(transforms),'structural_source_unchanged':True,
      'preserved_complete_labels':len(baseline['graphs']['main.tex']['labels']),
      'local_import_complete_labels':local['complete_labels'],'current_complete_labels':len(graphs['main.tex']['labels']),
      'preserved_quantitative_package_labels':len(baseline['graphs']['quantitative.tex']['labels']),
      'preserved_structural_labels':len(baseline['graphs']['structural.tex']['labels']),
      'relocated_to_current_supplement':relocated,'relocated_count':len(relocated),
      'new_theorems':NEW_LABELS,'regression_suites':len(SCRIPTS),'graphs':graphs}


def source_commit_inventory(source,inv):
    repository=Path(git('rev-parse','--show-toplevel'))
    prefix=ROOT.relative_to(repository).as_posix()+'/'
    entries=run(['git','ls-tree','-r',source,'--',prefix],cwd=repository).splitlines()
    actual={line.split('\t')[1]:line.split()[2] for line in entries}
    expected={prefix+n:blob((ROOT/n).read_bytes()) for n in inv}
    require(actual==expected,'native Git object differs from the complete native inventory')
    return repository,prefix


def regression():
    # Each suite gets a byte-identical native workspace. Parallel suites cannot
    # mutate one another's inputs, and normal/-O runs share only that suite's
    # own disposable copy. Numeric library threads are capped to avoid nested
    # oversubscription; the finite test results must still match exactly.
    inv=sources(ROOT)
    def one(script):
        print('ordinary/optimized regression: '+script,file=sys.stderr,flush=True)
        with tempfile.TemporaryDirectory(prefix='gtf96-suite-') as directory:
            work=Path(directory)
            for name in inv:
                dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(ROOT/name,dest)
            require(sources(work)==inv,'suite workspace copy differs: '+script)
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
            a=json.loads(run([sys.executable,str(work/script)],cwd=work,timeout=240,env=env))
            b=json.loads(run([sys.executable,'-O',str(work/script)],cwd=work,timeout=240,env=env))
            require(a==b and a['status'] in {'success','pass'},'regression failed: '+script)
            require(sources(work)==inv,'suite mutated a native input: '+script)
            return a
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(one,SCRIPTS))
    return dict(zip(SCRIPTS,rows))


def signatures():
    return {name:{**old.pdf_signature(ROOT/name),'sha256':sha((ROOT/name).read_bytes())}
            for name in DOCS.values()}


def extract(archive,destination):
    with zipfile.ZipFile(archive) as z:
        old.archive_names(z)
        z.extractall(destination)


def reconstruct(source,inv,expected_pages,expected_tests):
    with tempfile.TemporaryDirectory(prefix='gtf96-reconstruction-') as directory:
        dest=Path(directory);extract(ROOT/'evidence/NATIVE_SOURCE.zip',dest)
        output=run([sys.executable,str(dest/'build_revision.py'),'--reconstruct',source],cwd=dest,timeout=1500)
        replay=json.loads(output)
        require(replay['status']=='success' and replay['source_commit']==source,'reconstruction identity failed')
        require(sources(dest)==inv,'reconstruction source inventory differs')
        pages=json.loads((dest/'evidence/PAGE_CHECKS.json').read_text())
        for name in DOCS.values():
            require(pages[name]['page_checks']==expected_pages[name]['page_checks'],
                    'reconstruction page text/raster differs: '+name)
        require(json.loads((dest/'evidence/REGRESSION_RESULTS.json').read_text())==expected_tests,
                'isolated finite regression results differ')
    return {'source_commit':source,'all_page_text_and_rasters_match':True,
            'finite_regressions_match':True,'native_files_match':True}


def journal_verify():
    with tempfile.TemporaryDirectory(prefix='gtf96-journal-') as directory:
        dest=Path(directory);extract(ROOT/'evidence/JOURNAL_PACKAGE.zip',dest)
        result=json.loads(run([sys.executable,str(dest/'journal_verify.py')],cwd=dest,timeout=900))
        require(result['status']=='success' and result['read_only'],'standalone journal rebuild failed')
        return result


def build(preflight=False,reconstruction=None,isolated=False):
    inv,checked=check_source()
    if preflight: source=None;tree=None
    elif reconstruction:
        require(re.fullmatch('[0-9a-f]{40}',reconstruction) is not None,'invalid reconstruction identity')
        source=reconstruction;tree=None
    else:
        source=git('rev-parse','HEAD');source_commit_inventory(source,inv)
        tree=git('rev-parse','HEAD^{tree}')
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    builddir=ROOT/'build';builddir.mkdir(exist_ok=True)
    env=dict(os.environ,SOURCE_DATE_EPOCH=EPOCH,FORCE_SOURCE_DATE='1',TZ='UTC')
    diagnostics={};locations={}
    for cycle in range(4):
        for entry in DOCS:
            print('typesetting linked documents, round '+str(cycle+1)+': '+entry,file=sys.stderr,flush=True)
            run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                 '-output-directory='+str(builddir),entry],env=env)
            if entry in ('quantitative.tex','supplement.tex'):
                own=set(graph(ROOT,entry)[1]);stem=Path(entry).stem
                lines=(builddir/(stem+'.aux')).read_text().splitlines()
                kept=[line for line in lines if (match:=re.match(r'\\newlabel\{([^}]+)\}',line))
                      and match.group(1) in own]
                (builddir/('xref-'+stem+'.aux')).write_text('\n'.join(kept)+'\n')
    for entry,pdf in DOCS.items():
        stem=Path(entry).stem;log=(builddir/(stem+'.log')).read_text(errors='replace')
        diagnostics[entry]=old.diagnostics(log,entry)
        (evidence/(stem.upper()+'_LATEX_LOG.txt')).write_text(log)
        shutil.copy2(builddir/(stem+'.pdf'),ROOT/pdf)
        aux=(builddir/(stem+'.aux')).read_text()
        locations[entry]={key:{'number':number,'page':page}
            for key,number,page in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux)}
    pages=signatures();tests=regression()
    require(sources(ROOT)==inv,'build changed native sources')
    put(evidence/'SOURCE_HASHES.json',inv);put(evidence/'PAGE_CHECKS.json',pages)
    put(evidence/'THEOREM_LOCATIONS.json',locations);put(evidence/'REGRESSION_RESULTS.json',tests)
    put(evidence/'PRESERVATION_CHECK.json',checked)
    native={n:(ROOT/n).read_bytes() for n in inv}
    old.make_zip(evidence/'NATIVE_SOURCE.zip',native)
    receipt={'schema':'gtf96.build/1','status':'success','source_commit':source,'source_git_tree':tree,
        'base_commit':BASE,'source_date_epoch':int(EPOCH),'source_files':len(inv),
        'qualified_git_source':source is not None and reconstruction is None and not preflight,
        'git_identity_scope':'exact native source commit; transport and check status are recorded separately',
        'execution_environment':('GitHub Actions' if os.getenv('GITHUB_ACTIONS')=='true' else 'local'),
        'workflow_run_id':os.getenv('GITHUB_RUN_ID'),
        'preflight_only':preflight,'temporary_reconstruction':reconstruction is not None,
        'normal_optimized_identical':True,'regression_suites':len(tests),
        'suite_workspaces':'separate byte-checked native copies','max_parallel_suites':4,
        'native_source_sha256':sha((evidence/'NATIVE_SOURCE.zip').read_bytes()),
        'source_inventory_sha256':sha((evidence/'SOURCE_HASHES.json').read_bytes()),
        'documents':{n:{'pages':v['pages'],'sha256':v['sha256']} for n,v in pages.items()},
        'preservation':{k:v for k,v in checked.items() if k!='graphs'},
        'latex_diagnostics':diagnostics,'isolated_native_rebuild':False,'standalone_journal_rebuild':False,
        'historical_evidence_reused_as_current_qualification':False,
        'physical_learner_executed':False,'independent_human_priority_clearance':False,
        'tools':{'python':sys.version.split()[0],'pymupdf':fitz.VersionBind,
                 'pdflatex':run(['pdflatex','--version']).splitlines()[0]}}
    if source is not None:
        names=set(JOURNAL_EXTRAS)
        for entry in ('quantitative.tex','supplement.tex'):names.update(graph(ROOT,entry)[0])
        journal={n:(ROOT/n).read_bytes() for n in names}
        manifest={'schema':'gtf96.journal/1','source_commit':source,'source_date_epoch':int(EPOCH),
            'files':{n:sha(v) for n,v in journal.items()},
            'documents':{n:pages[n] for n in ('paper.pdf','BINARY_SUPPLEMENT.pdf')},
            'historical_PDF_dependencies':False,'repository_dependencies':False}
        journal['JOURNAL_MANIFEST.json']=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
        old.make_zip(evidence/'JOURNAL_PACKAGE.zip',journal)
    if isolated:
        require(source is not None and not reconstruction,'isolated qualification needs an actual source commit')
        print('isolated complete native reconstruction',file=sys.stderr,flush=True)
        put(evidence/'ISOLATED_REBUILD.json',reconstruct(source,inv,pages,tests))
        receipt['isolated_native_rebuild']=True
        print('standalone primary/supplement reconstruction',file=sys.stderr,flush=True)
        put(evidence/'JOURNAL_REBUILD.json',journal_verify())
        receipt['standalone_journal_rebuild']=True
    put(evidence/'BUILD_RECEIPT.json',receipt)
    if source is not None:
        research={**native,**{n:(ROOT/n).read_bytes() for n in DOCS.values()}}
        for n in ['BUILD_RECEIPT.json','SOURCE_HASHES.json','PAGE_CHECKS.json','REGRESSION_RESULTS.json',
                  'PRESERVATION_CHECK.json','THEOREM_LOCATIONS.json']:
            research['evidence/'+n]=(evidence/n).read_bytes()
        old.make_zip(evidence/'RESEARCH_PACKAGE.zip',research)
    generated={p.relative_to(ROOT).as_posix():sha(p.read_bytes())
               for p in sorted(evidence.rglob('*')) if p.is_file() and p.name!='PACKAGE_MANIFEST.json'}
    generated.update({n:sha((ROOT/n).read_bytes()) for n in DOCS.values()})
    put(evidence/'PACKAGE_MANIFEST.json',generated)
    return receipt


def verify_published():
    inv,checked=check_source();evidence=ROOT/'evidence'
    receipt=json.loads((evidence/'BUILD_RECEIPT.json').read_text());source=receipt['source_commit']
    require(receipt['qualified_git_source'] and receipt['isolated_native_rebuild']
            and receipt['standalone_journal_rebuild'] and not receipt['preflight_only'],
            'publication is not based on a fully qualified native source')
    repository,prefix=source_commit_inventory(source,inv)
    head=git('rev-parse','HEAD');run(['git','merge-base','--is-ancestor',source,head])
    for name in git('diff','--name-only',source,head).splitlines():
        require(name.startswith(prefix+'evidence/') or name in {prefix+n for n in DOCS.values()}
                or name.startswith('GENERAL_THETA_FOUNDATIONS_I_V96_'),
                'publication changed a non-artifact source: '+name)
    require(inv==json.loads((evidence/'SOURCE_HASHES.json').read_text()),'source hashes differ')
    generated=json.loads((evidence/'PACKAGE_MANIFEST.json').read_text())
    for name,digest in generated.items():require(sha((ROOT/name).read_bytes())==digest,'artifact hash differs: '+name)
    before={n:sha((ROOT/n).read_bytes()) for n in [*inv,*generated,'evidence/PACKAGE_MANIFEST.json']}
    pages=json.loads((evidence/'PAGE_CHECKS.json').read_text())
    tests=json.loads((evidence/'REGRESSION_RESULTS.json').read_text())
    result=reconstruct(source,inv,pages,tests);journal=journal_verify()
    require(all(sha((ROOT/n).read_bytes())==digest for n,digest in before.items()),
            'read-only verification modified the submitted object')
    return {'schema':'gtf96.exact-head/1','status':'success','verified_head':head,'source_commit':source,
        'source_files':len(inv),'documents':receipt['documents'],'read_only':True,
        'native_reconstruction':result,'standalone_journal':journal,
        'regression_suites':len(tests),'normal_optimized_identical':True,
        'independent_proof_or_priority_certification':False,'verification_scope':'source-bound read-only reconstruction',
        'workflow_run_id':os.getenv('GITHUB_RUN_ID'),'execution_environment':('GitHub Actions' if os.getenv('GITHUB_ACTIONS')=='true' else 'local')}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--check-source',action='store_true');group.add_argument('--preflight',action='store_true')
    group.add_argument('--reconstruct');group.add_argument('--verify-published',action='store_true')
    parser.add_argument('--isolated',action='store_true');a=parser.parse_args()
    if a.check_source:result=check_source()[1]
    elif a.verify_published:result=verify_published()
    else:result=build(a.preflight,a.reconstruct,a.isolated)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
