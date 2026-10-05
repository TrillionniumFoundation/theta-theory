#!/usr/bin/env python3
"""Source-bound v85 build, complete preservation, and read-only reconstruction.

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
import fitz

ROOT=Path(__file__).resolve().parent
BASE='9ee14476f539a38f2f45f9bd4ed99a658a7eb14d'
EPOCH='1791158400'
DOCS={'quantitative.tex':'paper.pdf','supplement.tex':'BINARY_SUPPLEMENT.pdf','structural.tex':'STRUCTURAL_PAPER.pdf',
      'main.tex':'COMPLETE_REVISION.pdf'}
NEW_SECTIONS=['sections/72-finite-product-prerequisite.tex', 'sections/73-smooth-boundary-curves.tex', 'sections/74-certified-control-stability.tex']
NEW_LABELS=['lem:bernoulli85', 'lem:curvegenerator85', 'thm:curveclassification85', 'lem:horizontalcurve85', 'lem:curvelogical85', 'cor:rankopening85', 'thm:controlstability85', 'prop:curveexact85']
JOURNAL_EXTRAS={'paper.pdf','BINARY_SUPPLEMENT.pdf','STRUCTURAL_PAPER.pdf','RESPONSE_TO_REFEREE.md',
 'LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','JOURNAL_README.md','journal_verify.py'}
# These established parsing/rendering helpers and regression names are retained
# byte-for-byte. All tests below are executed anew on this revision's files.
spec=importlib.util.spec_from_file_location('v81_build_helpers',ROOT/'predecessor-v81-audit/build_revision.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
sha=old.sha;require=old.require;put=old.put;graph=old.graph;sources=old.sources
SCRIPTS=(*old.REGRESSION_SCRIPTS,'finite_outcome_check.py','covariance_check.py','support_check.py','curve_check.py')


def run(cmd,cwd=ROOT,timeout=240,env=None):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=timeout,env=env)
    require(p.returncode==0,'command failed: '+str(cmd)+'\n'+p.stdout[-6000:]+'\n'+p.stderr[-6000:])
    return p.stdout


def git(*args):
    return run(['git',*args]).strip()


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def check_source():
    inv=sources(ROOT);baseline=json.loads((ROOT/'V84_BASELINE.json').read_text())
    require(baseline['commit']==BASE and len(baseline['files'])==529,'wrong predecessor inventory')
    changed=set(baseline['changed_predecessor_paths']);actual=[]
    for name,digest in baseline['files'].items():
        require(name in inv,'predecessor native file deleted: '+name)
        if inv[name]!=digest:
            require(name in changed,'undeclared predecessor change: '+name)
            require(sha((ROOT/'predecessor-v84-audit'/name).read_bytes())==digest,
                    'missing unchanged predecessor text: '+name)
            actual.append(name)
    graphs={}
    for entry in DOCS:
        files,active=graph(ROOT,entry)
        graphs[entry]={'files':sorted(files),'labels':sorted(active)}
    # The shorter primary plus its current binary supplement is the conserved
    # quantitative proof package. Complete and structural editions stay intact.
    joint_files=set(graphs['quantitative.tex']['files'])|set(graphs['supplement.tex']['files'])
    joint_labels=set(graphs['quantitative.tex']['labels'])|set(graphs['supplement.tex']['labels'])
    relocated=sorted(set(baseline['graphs']['quantitative.tex']['labels'])-
                     set(graphs['quantitative.tex']['labels']))
    for entry,prior in baseline['graphs'].items():
        files=joint_files if entry=='quantitative.tex' else set(graphs[entry]['files'])
        active=joint_labels if entry=='quantitative.tex' else set(graphs[entry]['labels'])
        require(set(prior['labels'])<=active,'inherited active label was lost: '+entry)
        for name in prior['files']:
            if name.startswith('sections/') or entry=='structural.tex':
                require(name in files and inv[name]==baseline['files'][name],
                        'inherited active proof text changed: '+name)
    require(all(n in graphs['supplement.tex']['labels'] for n in relocated),
            'a relocated label is not active in the supplement')
    require(not(set(graphs['quantitative.tex']['labels'])&set(graphs['supplement.tex']['labels'])),
            'ambiguous cross-document labels')
    # No inherited mathematical source is changed, including inactive archival sections.
    for name,digest in baseline['files'].items():
        if name.startswith('sections/'):
            require(inv[name]==digest,'inherited mathematical section changed: '+name)
    require(len(baseline['graphs']['main.tex']['labels'])==891,'wrong complete predecessor graph')
    for name in NEW_SECTIONS:
        require(all(name in graphs[e]['files'] for e in ('main.tex','quantitative.tex')),
                'new proof not active in both editions')
    labels=[]
    for name in NEW_SECTIONS:
        labels+=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(ROOT/name).read_text())
    require(sorted(labels)==sorted(NEW_LABELS),'new theorem inventory differs')
    status=json.loads((ROOT/'PROOF_STATUS.json').read_text())
    require(status['analytic_pipeline_closure'] and
            all(v is False for v in status['analytic_pipeline_closure'].values()),
            'measurement results cannot promote independent analytic flags')
    for name,digest in [('FROZEN_R54_REPORT.md','ca0712f6e1afaf6ea87f445a14aee9451d07239adebaeb4db37e234f8d64d4d3'),
      ('FROZEN_R54_PIPELINE_AUDIT.md','789767007436d9a8109ced9421a8af5ee26088df46793540a13f1066f8afe855')]:
        require(inv[name]==digest,'controlling report bytes differ')
    return inv,{'schema':'gtf85.source-check/1','status':'success','base_commit':BASE,
        'predecessor_native_files':529,'source_files':len(inv),'changed_predecessor_paths':sorted(actual),
        'preserved_complete_labels':891,'preserved_quantitative_package_labels':402,
        'preserved_structural_labels':116,'all_predecessor_sections_byte_identical':True,
        'relocated_to_current_supplement':relocated,'relocated_count':len(relocated),
        'structural_source_unchanged':True,'new_theorems':NEW_LABELS,
        'regression_suites':len(SCRIPTS),'graphs':graphs}


def source_commit_inventory(source,inv):
    repository=Path(git('rev-parse','--show-toplevel'))
    prefix=ROOT.relative_to(repository).as_posix()+'/'
    entries=run(['git','ls-tree','-r',source,'--',prefix],cwd=repository).splitlines()
    actual={line.split('\t')[1]:line.split()[2] for line in entries}
    expected={prefix+n:blob((ROOT/n).read_bytes()) for n in inv}
    require(actual==expected,'native Git object differs from the complete native inventory')
    return repository,prefix


def regression():
    result={}
    for script in SCRIPTS:
        print('exact ordinary/optimized regression: '+script,file=sys.stderr,flush=True)
        a=json.loads(run([sys.executable,str(ROOT/script)],timeout=240))
        b=json.loads(run([sys.executable,'-O',str(ROOT/script)],timeout=240))
        require(a==b and a['status'] in {'success','pass'},'regression failed: '+script)
        result[script]=a
    return result


def signatures():
    return {name:{**old.pdf_signature(ROOT/name),'sha256':sha((ROOT/name).read_bytes())}
            for name in DOCS.values()}


def extract(archive,destination):
    with zipfile.ZipFile(archive) as z:
        old.archive_names(z)
        z.extractall(destination)


def reconstruct(source,inv,expected_pages,expected_tests):
    with tempfile.TemporaryDirectory(prefix='gtf85-reconstruction-') as directory:
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
    with tempfile.TemporaryDirectory(prefix='gtf85-journal-') as directory:
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
    receipt={'schema':'gtf85.build/1','status':'success','source_commit':source,'source_git_tree':tree,
        'base_commit':BASE,'source_date_epoch':int(EPOCH),'source_files':len(inv),
        'qualified_git_source':source is not None and reconstruction is None and not preflight,
        'preflight_only':preflight,'temporary_reconstruction':reconstruction is not None,
        'normal_optimized_identical':True,'regression_suites':len(tests),
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
        for entry in ('quantitative.tex','supplement.tex','structural.tex'):names.update(graph(ROOT,entry)[0])
        journal={n:(ROOT/n).read_bytes() for n in names}
        manifest={'schema':'gtf85.journal/1','source_commit':source,'source_date_epoch':int(EPOCH),
            'files':{n:sha(v) for n,v in journal.items()},
            'documents':{n:pages[n] for n in ('paper.pdf','BINARY_SUPPLEMENT.pdf','STRUCTURAL_PAPER.pdf')},
            'historical_PDF_dependencies':False,'repository_dependencies':False}
        journal['JOURNAL_MANIFEST.json']=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
        old.make_zip(evidence/'JOURNAL_PACKAGE.zip',journal)
    if isolated:
        require(source is not None and not reconstruction,'isolated qualification needs an actual source commit')
        print('isolated complete native reconstruction',file=sys.stderr,flush=True)
        put(evidence/'ISOLATED_REBUILD.json',reconstruct(source,inv,pages,tests))
        receipt['isolated_native_rebuild']=True
        print('standalone primary/supplement/structural reconstruction',file=sys.stderr,flush=True)
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
                or name.startswith('GENERAL_THETA_FOUNDATIONS_I_V85_'),
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
    return {'schema':'gtf85.exact-head/1','status':'success','verified_head':head,'source_commit':source,
        'source_files':len(inv),'documents':receipt['documents'],'read_only':True,
        'native_reconstruction':result,'standalone_journal':journal,
        'regression_suites':len(tests),'normal_optimized_identical':True,
        'independent_proof_or_priority_certification':False}


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
