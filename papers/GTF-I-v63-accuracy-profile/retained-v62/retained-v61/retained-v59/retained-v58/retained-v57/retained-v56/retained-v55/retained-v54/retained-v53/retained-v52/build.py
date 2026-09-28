"""Reproducible source-bound v52 build; no network calls or remote mutations."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
import fitz
HOME=Path(__file__).resolve().parent
EV=HOME/'evidence'
REVIEW='9d2f516b4113016f57fc8193c24ba192f8f782d5'
BASE='6363748923a5623801a53cfdb507a776aad414c3'

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name:str,value)->None:(EV/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def run(command:list[str],cwd:Path=HOME)->str:
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790467200',FORCE_SOURCE_DATE='1',TZ='UTC',PYTHONHASHSEED='0')
    result=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=300)
    if result.returncode:
        (EV/'FAILED_COMMAND.txt').write_text(repr(command)+'\n'+result.stdout+'\n'+result.stderr)
        raise RuntimeError('Failed '+repr(command)+'\n'+result.stdout[-8000:]+'\n'+result.stderr[-3000:])
    return result.stdout

def sources()->list[Path]:
    return sorted(p for p in HOME.rglob('*') if p.is_file() and 'evidence' not in p.relative_to(HOME).parts
                  and '__pycache__' not in p.parts and p.suffix in {'.tex','.py','.md','.json'})
def makezip(dest:Path,entries:list[tuple[Path,str]])->None:
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p,n in sorted(entries,key=lambda t:t[1]):
            if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2','.pfb'}:raise RuntimeError('Font packaging prohibited')
            info=zipfile.ZipInfo(n,date_time=(2026,9,27,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes())
def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--check-core',action='store_true');parser.add_argument('--core-only',action='store_true')
    args=parser.parse_args();EV.mkdir(exist_ok=True)
    for stale in EV.glob('page-*.png'):stale.unlink()
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    for name,entry in manifest['files'].items():
        if sha(HOME/name)!=entry['v52_sha256']:raise RuntimeError('Preserved source mismatch '+name)
    original_labels=set(json.loads((HOME/'EXPECTED_V51.json').read_text())['loaded_labels'])
    def active(p:Path,seen:set[Path])->list[Path]:
        if p in seen:raise RuntimeError('Repeated manuscript input '+str(p))
        seen.add(p);out=[p]
        for n in re.findall(r'\\input\{([^}]+)\}',p.read_text()):
            q=HOME/n
            if not q.suffix:q=q.with_suffix('.tex')
            if not q.is_relative_to(HOME):raise RuntimeError('Input outside manuscript')
            out.extend(active(q,seen))
        return out
    actual_inputs=active(HOME/'main.tex',set())
    current_tex='\n'.join(p.read_text() for p in actual_inputs)
    save('ACTIVE_INPUTS.json',[str(p.relative_to(HOME)) for p in actual_inputs])
    current_labels=set(re.findall(r'\\label\{([^}]+)\}',current_tex))
    if original_labels-current_labels:raise RuntimeError('Lost original labels '+repr(original_labels-current_labels))
    results={}
    for version,script,cwd in [('v52','check_revision.py',HOME),('v51','check_v51.py',HOME),('v50','check_v50.py',HOME),('v49','check_duality.py',HOME/'inherited'),
                                ('v47','check_compatibility.py',HOME/'inherited'),('v44','verify_inherited.py',HOME/'inherited')]:
        normal=json.loads(run([sys.executable,script],cwd));optimized=json.loads(run([sys.executable,'-O',script],cwd))
        if normal!=optimized:raise RuntimeError('Normal/optimized disagreement '+version)
        results[version]=normal;save(version.upper()+'_CHECKS.json',normal)
    helptext=run([sys.executable,'dual_certificate.py','--help'],HOME/'inherited')
    if '--max-sign-variables' not in helptext or '--max-rows' not in helptext:raise RuntimeError('CLI limits not documented')
    (EV/'DUAL_CHECKER_HELP.txt').write_text(helptext)
    # Verify the newly exposed CLI actually fails closed, rather than just naming its limit.
    case=EV/'CLI_LIMIT_INPUT.json';case.write_text(json.dumps({'dims':[2,2],'values':['1','1','1','1']}))
    command=[sys.executable,str(HOME/'inherited'/'dual_certificate.py'),str(case),'--delta','0','--max-sign-variables','0']
    exhausted=subprocess.run(command,capture_output=True,text=True,timeout=30)
    status=json.loads(exhausted.stdout)
    if exhausted.returncode!=2 or status.get('feasibility')!='undetermined':raise RuntimeError('CLI did not fail closed')
    save('CLI_LIMIT_RECEIPT.json',{'status':'success','exit_code':2,'resource_result':status})
    for _ in range(3):run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'])
    log=(HOME/'main.log').read_text(errors='replace');(EV/'LATEX_LOG.txt').write_text(log)
    flags={'undefined_references':bool(re.search(r'(Reference|Citation).*undefined|There were undefined',log)),
           'overfull_boxes':r'Overfull \hbox' in log or r'Overfull \vbox' in log,
           'malformed_bookmarks':'Token not allowed in a PDF string' in log}
    if any(flags.values()):raise RuntimeError('Typesetting qualification '+repr(flags))
    shutil.copyfile(HOME/'main.pdf',HOME/'paper.pdf')
    doc=fitz.open(HOME/'paper.pdf')
    if not len(doc) or any(not p.get_text().strip() for p in doc):raise RuntimeError('Empty manuscript page')
    page_checks=[]
    for i,p in enumerate(doc):
        pix=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);pix.save(EV/f'page-{i+1:02d}.png')
        for block in p.get_text('dict')['blocks']:
            if 'lines' not in block:continue
            for line in block['lines']:
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if min(x0,y0)<0 or x1>p.rect.width+0.1 or y1>p.rect.height+0.1:raise RuntimeError('Text outside page')
        page_checks.append({'page':i+1,'text_sha256':hashlib.sha256(p.get_text().encode()).hexdigest(),
                            'raster_sha256':hashlib.sha256(pix.samples).hexdigest()})
    save('PAGE_CHECKS.json',page_checks)
    labels={n:{'number':v,'page':p} for n,v,p in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',(HOME/'main.aux').read_text())}
    save('THEOREM_LOCATIONS.json',labels)
    # A marked reading excerpt, not a replacement for the complete retained appendices.
    boundary=int(labels['boundary:retained52']['page'])-1
    reference_candidates=[i for i,p in enumerate(doc) if '\nReferences\n' in p.get_text()]
    if not 0<boundary<len(doc) or not reference_candidates:raise RuntimeError('Core/reference boundary absent')
    reference_start=reference_candidates[-1]
    if reference_start<boundary:raise RuntimeError('Unexpected bibliography position')
    core_page_indices=list(range(boundary))+list(range(reference_start,len(doc)))
    excerpt=fitz.open()
    for i in core_page_indices:excerpt.insert_pdf(doc,from_page=i,to_page=i)
    excerpt.set_metadata({'title':'GTF-I Revision 52: focused core excerpt with references',
                          'subject':'Excerpt only. See paper.pdf for all retained appendices and cited proofs.',
                          'author':'Qian Qi'})
    excerpt.save(HOME/'CORE_ARGUMENT.pdf',garbage=4,deflate=True);excerpt.close()
    save('CORE_EXCERPT_RECEIPT.json',{'schema':'gtf52.excerpt/1','complete_article_pages':len(doc),
         'excerpt_original_page_numbers':[i+1 for i in core_page_indices],
         'scope':'Reading excerpt, not a deletion of appendices or a standalone replacement for cited proofs.'})
    ss=sources();save('SOURCE_HASHES.json',{str(p.relative_to(HOME)):sha(p) for p in ss})
    makezip(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+str(p.relative_to(HOME))) for p in ss])
    source=os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted-build');core=None
    if args.check_core:
        with tempfile.TemporaryDirectory(prefix='gtf52-core-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z:z.extractall(temp)
            isolated=Path(temp)/HOME.name
            output=run([sys.executable,'build.py','--core-only'],isolated);(EV/'CORE_REBUILD_LOG.txt').write_text(output)
            other=fitz.open(isolated/'paper.pdf')
            if len(other)!=len(doc):raise RuntimeError('Isolated page count differs')
            for i in range(len(doc)):
                if doc[i].get_text()!=other[i].get_text():raise RuntimeError('Isolated text differs')
                if doc[i].get_pixmap().samples!=other[i].get_pixmap().samples:raise RuntimeError('Isolated raster differs')
            other.close()
            core={'status':'success','pages':len(doc),'all_page_text_equal':True,'all_page_raster_equal':True,'source_commit':source}
            save('CORE_REBUILD_RECEIPT.json',core)
    negatives=sum(2*len(r.get('negative_controls_detected',[])) for r in results.values())
    receipt={'schema':'gtf52.build/1','status':'success','source_commit':source,'v51_publication':BASE,'review_commit':REVIEW,
        'workflow_run':os.environ.get('GITHUB_RUN_ID'),'article_pages':len(doc),'article_sha256':sha(HOME/'paper.pdf'),
        'focused_excerpt_pages':len(core_page_indices),'focused_excerpt_sha256':sha(HOME/'CORE_ARGUMENT.pdf'),
        'current_loaded_labels':len(current_labels),'active_input_files':len(actual_inputs),
        'native_source_files':len(ss),'original_loaded_labels_preserved':len(original_labels),
        'inherited_files_preserved':len(manifest['files']),'edited_inherited_copies':sum(bool(x['amendments']) for x in manifest['files'].values()),
        'normal_optimized_agreement':True,'negative_control_executions_named':negatives,'new_v52_negative_control_executions':2*len(results['v52']['negative_controls_detected']),
        'cli_limit_fail_closed':True,'regressions':results,'core_rebuild':core,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),
        'scope':'Exact finite regression and reproducible manuscript qualification. Not independent theorem verification, exhaustive priority clearance, or unrelated analytic-pipeline closure.',**flags}
    save('BUILD_RECEIPT.json',receipt)
    package=[HOME/'paper.pdf',HOME/'CORE_ARGUMENT.pdf',HOME/'RESPONSE_TO_REFEREE.md',HOME/'LITERATURE_AUDIT.md',HOME/'HISTORY_AUDIT.md',
             EV/'CORE_SOURCES.zip',EV/'BUILD_RECEIPT.json',EV/'V52_CHECKS.json',EV/'V51_CHECKS.json',EV/'THEOREM_LOCATIONS.json',EV/'SOURCE_HASHES.json',EV/'CORE_EXCERPT_RECEIPT.json']
    if core:package.append(EV/'CORE_REBUILD_RECEIPT.json')
    makezip(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package])
    if not args.core_only:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V52_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 52\n\n'
            '**Quantitative and Noisy Finite-Group Rigidity for Stochastic Realizations**\n\n'
            f'Validated native source: `{source}`. Controlling r33: `{REVIEW}`. v51 publication: `{BASE}`.\n\n'
            f'[Complete English article ({len(doc)} pages)](papers/{HOME.name}/paper.pdf) · '
            f'[Focused excerpt ({len(core_page_indices)} pages)](papers/{HOME.name}/CORE_ARGUMENT.pdf) · '
            f'[Native source](papers/{HOME.name}/main.tex) · [Response to r33](papers/{HOME.name}/RESPONSE_TO_REFEREE.md)\n\n'
            f'[Referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip) · '
            f'[Complete isolated sources](papers/{HOME.name}/evidence/CORE_SOURCES.zip) · '
            f'[Build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json) · '
            f'[Theorem locations](papers/{HOME.name}/evidence/THEOREM_LOCATIONS.json)\n\n'
            'The new main theorem treats fixed positive error at unrestricted stochastic width. '
            'Its finite-orbit reduction yields a finite-group classification and an occupation budget. '
            'Companion results give a rational-height rate, an explicit one-surplus multiplier and six-state horizon, '
            'conditioned geometric stability, an unconditional computable noise interval, '
            'a complete global residual certificate hierarchy, and a priced uniform rational compiler.\n\n'
            'All 201 predecessor labels and its mathematical modules remain in the complete article. '
            'The focused PDF is only a reading excerpt; the complete retained appendices are not deleted. '
            'The unconditional six-state noise-search algorithm is proved to terminate but is not executed at the large illustrative horizon. '
            'No numerical unconditional threshold, practical general SOS search engine, exhaustive priority clearance, '
            'independent verification of all theorems, or unrelated analytic-pipeline closure is inferred.\n')
    doc.close()
    for suffix in ['aux','log','out','pdf']:(HOME/f'main.{suffix}').unlink(missing_ok=True)
    for p in HOME.rglob('__pycache__'):shutil.rmtree(p,ignore_errors=True)
    print(json.dumps({'status':'success','pages':receipt['article_pages'],'source_commit':source,'core_rebuild':core is not None,'new_negative_executions':receipt['new_v52_negative_control_executions']}))
if __name__=='__main__':main()
