"""Native v53 qualification and portable referee package; no network or remote writes.

The checks are finite regressions, typesetting, preservation, and reproducibility.
They are not a formal verification of the analytic theorems.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
import fitz

HOME=Path(__file__).resolve().parent
EV=HOME/'evidence'
OLD=HOME/'retained-v52'
BASE='7641901c2ef957542aa50d9918f272ac7a72ca1c'
REVIEW='4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c'
PDFS={'article':'paper.pdf','companion':'COMPANION_NOTES.pdf','complete_supplement':'COMPLETE_SUPPLEMENT.pdf'}

def require(condition: bool, message: str) -> None:
    if not condition:raise RuntimeError(message)

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name: str, value) -> None:
    (EV/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def environment() -> dict[str,str]:
    env=os.environ.copy()
    env.update(SOURCE_DATE_EPOCH='1790467200',FORCE_SOURCE_DATE='1',TZ='UTC',PYTHONHASHSEED='0')
    return env

def run(command: list[str], cwd: Path=HOME, timeout: int=300) -> str:
    result=subprocess.run(command,cwd=cwd,env=environment(),text=True,capture_output=True,timeout=timeout)
    if result.returncode:
        (EV/'FAILED_COMMAND.txt').write_text(repr(command)+'\n'+result.stdout+'\n'+result.stderr)
        raise RuntimeError('Command failed: '+repr(command)+'\n'+result.stdout[-10000:]+'\n'+result.stderr[-4000:])
    return result.stdout

def native_sources() -> list[Path]:
    return sorted(p for p in HOME.rglob('*') if p.is_file()
                  and 'evidence' not in p.relative_to(HOME).parts and '__pycache__' not in p.parts
                  and p.suffix in {'.tex','.py','.md','.json'})

def makezip(dest: Path, entries: list[tuple[Path,str]]) -> None:
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as archive:
        names=set()
        for path,name in sorted(entries,key=lambda item:item[1]):
            require(name not in names,'Duplicate archive path: '+name);names.add(name)
            require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe archive member')
            require(path.suffix.lower() not in {'.ttf','.otf','.woff','.woff2','.pfb'},'Font packaging prohibited')
            info=zipfile.ZipInfo(name,date_time=(2026,9,27,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,path.read_bytes())

def active(root: Path, file: Path, seen: set[Path]) -> list[Path]:
    require(file not in seen,'Repeated active source: '+str(file));seen.add(file)
    require(file.is_relative_to(root),'Input escapes native source root')
    out=[file]
    for name in re.findall(r'\\input\{([^}]+)\}',file.read_text()):
        path=root/name
        if not path.suffix:path=path.with_suffix('.tex')
        out.extend(active(root,path,seen))
    return out

def input_inventory(root: Path, main: str) -> tuple[list[Path],set[str]]:
    paths=active(root,root/main,set())
    labels=re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in paths))
    require(len(labels)==len(set(labels)),'Duplicate labels in '+main)
    return paths,set(labels)

def check_sources() -> dict:
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    require(manifest['predecessor_publication']==BASE and manifest['review_commit']==REVIEW,'Frozen identity mismatch')
    for name,digest in manifest['files'].items():
        require(sha(OLD/name)==digest,'Retained source changed: '+name)
    paths,labels=input_inventory(OLD,'main.tex')
    require([str(p.relative_to(OLD)) for p in paths]==manifest['active_inputs'],'Retained active input inventory changed')
    require(labels==set(manifest['loaded_labels']),'A predecessor mathematical label is missing')
    require(len(manifest['files'])==59 and len(paths)==33 and len(labels)==242,'Frozen count mismatch')
    report=(HOME/'FROZEN_R34_REPORT.md').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest()
    require(blob==manifest['review_blob'],'Controlling report bytes changed')
    documents={}
    for kind,root,name in [('article',HOME,'main.tex'),('companion',HOME,'supplement-notes.tex'),('complete_supplement',OLD,'main.tex')]:
        inputs,current=input_inventory(root,name)
        documents[kind]={'inputs':[str(p.relative_to(HOME)) for p in inputs],
                         'loaded_labels':sorted(current),'label_count':len(current)}
    save('ACTIVE_INPUTS.json',documents)
    return {'retained_native_files':59,'retained_active_inputs':33,'retained_loaded_labels':242,
            'byte_identical':True,'documents':documents}

def regressions() -> dict:
    results={}
    cases=[('v53','check_revision.py',HOME),('v52','check_revision.py',OLD),
           ('v51','check_v51.py',OLD),('v50','check_v50.py',OLD),
           ('v49','check_duality.py',OLD/'inherited'),('v47','check_compatibility.py',OLD/'inherited'),
           ('v44','verify_inherited.py',OLD/'inherited')]
    for name,script,cwd in cases:
        normal=json.loads(run([sys.executable,script],cwd))
        optimized=json.loads(run([sys.executable,'-O',script],cwd))
        require(normal==optimized,'Normal/optimized result mismatch: '+name)
        results[name]=normal;save(name.upper()+'_CHECKS.json',normal)
    helptext=run([sys.executable,'dual_certificate.py','--help'],OLD/'inherited')
    require('--max-sign-variables' in helptext and '--max-rows' in helptext,'Missing documented CLI limits')
    (EV/'DUAL_CHECKER_HELP.txt').write_text(helptext)
    case=EV/'CLI_LIMIT_INPUT.json';case.write_text(json.dumps({'dims':[2,2],'values':['1','1','1','1']}))
    command=[sys.executable,str(OLD/'inherited/dual_certificate.py'),str(case),'--delta','0','--max-sign-variables','0']
    result=subprocess.run(command,env=environment(),capture_output=True,text=True,timeout=30)
    status=json.loads(result.stdout)
    require(result.returncode==2 and status.get('feasibility')=='undetermined','Inherited CLI resource limit did not fail closed')
    save('CLI_LIMIT_RECEIPT.json',{'status':'success','exit_code':result.returncode,'resource_result':status})
    return results

def typeset(kind: str, cwd: Path, name: str) -> tuple[dict,list[dict],dict]:
    stem=Path(name).stem
    for _ in range(3):run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name],cwd)
    log=(cwd/(stem+'.log')).read_text(errors='replace')
    (EV/(kind.upper()+'_LATEX_LOG.txt')).write_text(log)
    flags={'undefined_references':bool(re.search(r'(Reference|Citation).*undefined|There were undefined',log)),
           'overfull_boxes':r'Overfull \hbox' in log or r'Overfull \vbox' in log,
           'malformed_bookmarks':'Token not allowed in a PDF string' in log}
    require(not any(flags.values()),'Typesetting qualification failed: '+kind+' '+repr(flags))
    shutil.copyfile(cwd/(stem+'.pdf'),HOME/PDFS[kind])
    document=fitz.open(HOME/PDFS[kind]);require(len(document)>0,'Empty PDF: '+kind)
    checks=[]
    for i,page in enumerate(document):
        text=page.get_text();require(bool(text.strip()),'Empty PDF page: '+kind)
        pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        # Retain all main/companion pages, plus representative supplement pages.
        if kind!='complete_supplement' or i in {0,len(document)//2,len(document)-1}:
            pix.save(EV/f'page-{kind}-{i+1:02d}.png')
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    require(min(x0,y0)>=-0.1 and x1<=page.rect.width+0.1 and y1<=page.rect.height+0.1,
                            'Text outside page: '+kind+' '+str(i+1))
        checks.append({'page':i+1,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
                       'raster_sha256':hashlib.sha256(pix.samples).hexdigest()})
    aux=(cwd/(stem+'.aux')).read_text()
    labels={key:{'number':number,'page':page} for key,number,page in
            re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux)}
    information={'pages':len(document),'filename':PDFS[kind],'sha256':sha(HOME/PDFS[kind]),**flags}
    document.close()
    for suffix in ['aux','log','out','pdf']:(cwd/(stem+'.'+suffix)).unlink(missing_ok=True)
    return information,checks,labels

def isolated_rebuild(source: str, page_checks: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix='gtf53-isolated-') as temp:
        with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as archive:archive.extractall(temp)
        isolated=Path(temp)/HOME.name
        output=run([sys.executable,'build.py','--isolated'],isolated,timeout=900)
        (EV/'ISOLATED_REBUILD_LOG.txt').write_text(output)
        other=json.loads((isolated/'evidence/PAGE_CHECKS.json').read_text())
        require(page_checks==other,'Native-only isolated page text/raster differs')
        other_receipt=json.loads((isolated/'evidence/BUILD_RECEIPT.json').read_text())
        require(other_receipt['status']=='success' and other_receipt['source_commit']==source,'Isolated source identity mismatch')
        return {'status':'success','source_commit':source,'all_page_text_equal':True,'all_page_raster_equal':True,
                'pages_by_document':{kind:len(pages) for kind,pages in page_checks.items()},
                'all_regressions_reexecuted':True,'no_repository_or_network_needed':True}

def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--check-isolated',action='store_true');parser.add_argument('--isolated',action='store_true')
    args=parser.parse_args();require(not (args.check_isolated and args.isolated),'Conflicting build modes')
    EV.mkdir(exist_ok=True)
    for stale in EV.glob('page-*.png'):stale.unlink()
    (EV/'FAILED_COMMAND.txt').unlink(missing_ok=True)
    preservation=check_sources()
    results=regressions()
    pdfs={};page_checks={};locations={}
    for kind,cwd,name in [('article',HOME,'main.tex'),('companion',HOME,'supplement-notes.tex'),('complete_supplement',OLD,'main.tex')]:
        pdfs[kind],page_checks[kind],locations[kind]=typeset(kind,cwd,name)
    for kind,inventory in preservation['documents'].items():
        require(set(inventory['loaded_labels'])<=set(locations[kind]),'A source label did not reach the compiled document: '+kind)
    save('PAGE_CHECKS.json',page_checks);save('THEOREM_LOCATIONS.json',locations)
    source_files=native_sources()
    hashes={str(p.relative_to(HOME)):sha(p) for p in source_files}
    save('SOURCE_HASHES.json',hashes)
    makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in source_files])
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-build')
    isolated=isolated_rebuild(source,page_checks) if args.check_isolated else None
    if isolated:save('ISOLATED_REBUILD_RECEIPT.json',isolated)
    new_negatives=2*len(results['v53'].get('negative_controls_detected',[]))
    inherited_negatives=sum(2*len(data.get('negative_controls_detected',[])) for key,data in results.items() if key!='v53')
    receipt={'schema':'gtf53.build/1','status':'success','source_commit':source,
             'predecessor_publication':BASE,'review_commit':REVIEW,'workflow_run':os.environ.get('GITHUB_RUN_ID'),
             'documents':pdfs,'preservation':preservation,'native_source_files':len(source_files),
             'normal_optimized_agreement':True,'new_v53_exact_finite_assertions':results['v53']['exact_finite_assertions'],
             'new_v53_negative_control_executions':new_negatives,'inherited_negative_control_executions':inherited_negatives,
             'total_named_negative_control_executions':new_negatives+inherited_negatives,
             'cli_limit_fail_closed':True,'regression_suites':list(results),'isolated_rebuild':isolated,
             'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
             'scope':'Written mathematical proofs with exact finite regressions, complete source preservation and reproducible typesetting; not independent formal theorem verification, exhaustive priority clearance, or analytic-pipeline closure.'}
    save('BUILD_RECEIPT.json',receipt)
    package_files=[HOME/name for name in [*PDFS.values(),'README.md','RESPONSE_TO_REFEREE.md',
                   'HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md','PROOF_STATUS.json',
                   'PRESERVATION_MANIFEST.json','FROZEN_R34_REPORT.md','FROZEN_PIPELINE_LEDGER.md']]
    package_files += [EV/name for name in ['CORE_SOURCES.zip','BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                      'V53_CHECKS.json','V52_CHECKS.json','PAGE_CHECKS.json','CLI_LIMIT_RECEIPT.json']]
    if isolated:package_files.append(EV/'ISOLATED_REBUILD_RECEIPT.json')
    makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package_files])
    if not args.isolated:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V53_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 53\n\n'
            '**Sharp Noise Thresholds for Stochastic Realizations of Compact Group Experiments**\n\n'
            f'Validated native source: `{source}`. Controlling r34: `{REVIEW}`. Frozen v52 publication: `{BASE}`.\n\n'
            f'[Main article ({pdfs["article"]["pages"]} pages)](papers/{HOME.name}/paper.pdf) · '
            f'[Companion notes ({pdfs["companion"]["pages"]} pages)](papers/{HOME.name}/COMPANION_NOTES.pdf) · '
            f'[Complete retained supplement ({pdfs["complete_supplement"]["pages"]} pages)](papers/{HOME.name}/COMPLETE_SUPPLEMENT.pdf)\n\n'
            f'[Response to r34](papers/{HOME.name}/RESPONSE_TO_REFEREE.md) · '
            f'[Native main source](papers/{HOME.name}/main.tex) · '
            f'[Portable referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip) · '
            f'[Source-bound build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json)\n\n'
            'Working branch: `revision/general-theta-foundations-i-v53-component-oscillation-2026-09-27`.  \n'
            'Referee branch: `revision/general-theta-foundations-i-v53-referee-ready-2026-09-27`.\n\n'
            'The critical binary total-variation error is one quarter of the maximal componentwise output oscillation. '
            'Bounded horizon-specific clocked width exists exactly at and above this boundary; one stationary permutation realization attains it. '
            'Below it, every fixed width has a horizon-independent occupation budget. '
            'The theorem allows arbitrary finite continuous interfaces, without spanning, reachability-rank, state-mass or conditioning assumptions. '
            'The planar threshold is exactly rho/2, and explicit algebraic-circle width bounds hold throughout the subcritical interval.\n\n'
            f'Qualification: {results["v53"]["exact_finite_assertions"]} new exact finite assertions per interpreter mode; '
            f'{new_negatives} new and {inherited_negatives} inherited named negative-control executions across normal and optimized Python; '
            'all 59 predecessor native files byte-identical, all 33 active inputs and 242 labels preserved. '
            f'All-page isolated text/raster equality: {bool(isolated)}.\n\n'
            'The main article is independently complete, not a selected-page excerpt. Previous mathematical material is retained in the complete supplement. '
            'The proof-status ledger does not claim independent formal verification, a sharp width growth law, an executed large-horizon six-state noise search, '
            'a general SOS discovery engine, or closure of unrelated analytic pipeline gates.\n')
    require(all(sha(HOME/name)==digest for name,digest in hashes.items()),'Native sources changed during qualification')
    for cache in list(HOME.rglob('__pycache__')):shutil.rmtree(cache,ignore_errors=True)
    print(json.dumps({'status':'success','source_commit':source,'pages':{kind:entry['pages'] for kind,entry in pdfs.items()},
                      'isolated_rebuild':bool(isolated),'exact_assertions':results['v53']['exact_finite_assertions'],
                      'new_negative_executions':new_negatives,'inherited_negative_executions':inherited_negatives},sort_keys=True))

if __name__=='__main__':
    main()
