"""Pinned-source revision-49 build. No network requests or remote writes."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
import fitz

HOME=Path(__file__).resolve().parent
EV=HOME/'evidence'
BASE='98b59f3f45f63dacd8dba8cf132d23e54e7596e8'
REVIEW='6ecf57a2d7ce804352f85daead8ec38e56377631'

def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name:str,value)->None:
    (EV/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def run(command:list[str],cwd:Path=HOME)->str:
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1790467200';env['FORCE_SOURCE_DATE']='1';env['TZ']='UTC'
    result=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=300)
    if result.returncode:
        (EV/'FAILED_COMMAND.txt').write_text(repr(command)+'\n'+result.stdout+'\n'+result.stderr)
        raise RuntimeError('Failed command: '+repr(command)+'\n'+result.stdout[-12000:]+'\n'+result.stderr[-4000:])
    return result.stdout

def zip_files(dest:Path,entries:list[tuple[Path,str]])->None:
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p,n in sorted(entries,key=lambda t:t[1]):
            if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2','.pfb'}:
                raise RuntimeError('Font file rejected')
            info=zipfile.ZipInfo(n,date_time=(2026,9,27,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes())

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--core-only',action='store_true');ap.add_argument('--check-core',action='store_true')
    args=ap.parse_args();EV.mkdir(exist_ok=True)
    manifest=json.loads((HOME/'PRESERVATION_MANIFEST.json').read_text())
    for group in ['unchanged_sources','archived_introductions']:
        for name,digest in manifest[group].items():
            if sha(HOME/name)!=digest: raise RuntimeError('Preservation mismatch: '+name)
    results={}
    for version,script in [('v49','check_duality.py'),('v47','check_compatibility.py'),('v44','verify_inherited.py')]:
        normal=json.loads(run([sys.executable,script]));optimized=json.loads(run([sys.executable,'-O',script]))
        if normal!=optimized: raise RuntimeError('Normal/optimized disagreement: '+version)
        results[version]=normal;save(version.upper()+'_CHECKS.json',normal)
    for _ in range(3): run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'])
    log=(HOME/'main.log').read_text(errors='replace');(EV/'LATEX_LOG.txt').write_text(log)
    flags={'undefined_references':bool(re.search(r'(Reference|Citation).*undefined|There were undefined',log)),
           'overfull_boxes':r'Overfull \hbox' in log or r'Overfull \vbox' in log,
           'malformed_bookmarks':'Token not allowed in a PDF string' in log}
    if any(flags.values()): raise RuntimeError('Typesetting qualification failed: '+str(flags))
    shutil.copyfile(HOME/'main.pdf',HOME/'paper.pdf')
    doc=fitz.open(HOME/'paper.pdf')
    if not len(doc) or any(not p.get_text().strip() for p in doc): raise RuntimeError('Empty article page')
    for i,p in enumerate(doc): p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(EV/f'page-{i+1}.png')
    labels={n:{'number':v,'page':p} for n,v,p in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',(HOME/'main.aux').read_text())}
    save('THEOREM_LOCATIONS.json',labels)
    sources=sorted(p for p in HOME.iterdir() if p.is_file() and p.suffix in {'.tex','.py','.md','.json'})
    save('SOURCE_HASHES.json',{p.name:sha(p) for p in sources})
    zip_files(EV/'CORE_SOURCES.zip',[(p,HOME.name+'/'+p.name) for p in sources])
    archives={};old=None
    if not args.core_only:
        old=Path(os.getenv('GTF_V47_INPUT',str(HOME.parent/'GTF-I-v47-compatible-certificates')))
        for n,digest in manifest['predecessor_pdfs'].items():
            if sha(old/n)!=digest: raise RuntimeError('Predecessor PDF mismatch: '+n)
        shutil.copyfile(old/'paper.pdf',HOME/'supporting-v47.pdf')
        for name in ['complete-manuscript.pdf','complete-development.pdf']:
            older=fitz.open(old/name);out=fitz.open();out.insert_pdf(doc)
            page=out.new_page(width=612,height=792)
            page.insert_text((72,100),'Preserved v47 mathematical archive',fontsize=17)
            page.insert_text((72,132),'The following predecessor pages are unchanged optional history.',fontsize=10)
            offset=len(out);out.insert_pdf(older)
            dest=HOME/name;dest.unlink(missing_ok=True);out.save(dest,garbage=3,deflate=True);out.close()
            checked=fitz.open(dest)
            for i in range(len(older)):
                if checked[offset+i].get_text()!=older[i].get_text(): raise RuntimeError('Archive text changed')
            samples=sorted(set([0,len(older)//2,len(older)-1]))
            for i in samples:
                if checked[offset+i].get_pixmap().samples!=older[i].get_pixmap().samples: raise RuntimeError('Archive raster changed')
            archives[name]={'pages':len(checked),'predecessor_pages':len(older),'sha256':sha(dest),
                'predecessor_sha256':manifest['predecessor_pdfs'][name],
                'text_pages_compared':len(older),'raster_pages_compared':len(samples)}
            older.close();checked.close()
        zip_files(EV/'SUBMISSION_SOURCES.zip',[(p,HOME.name+'/'+p.name) for p in sources]+[(old/n,old.name+'/'+n) for n in manifest['predecessor_pdfs']])
    source=os.getenv('GTF_SOURCE_COMMIT','local-uncommitted-build')
    core_check=None
    if args.check_core:
        with tempfile.TemporaryDirectory(prefix='gtf49-core-') as temp:
            with zipfile.ZipFile(EV/'CORE_SOURCES.zip') as z: z.extractall(temp)
            isolated=Path(temp)/HOME.name
            output=run([sys.executable,'build.py','--core-only'],cwd=isolated)
            (EV/'CORE_REBUILD_LOG.txt').write_text(output)
            other=fitz.open(isolated/'paper.pdf')
            if len(other)!=len(doc): raise RuntimeError('Isolated core page count mismatch')
            for i in range(len(doc)):
                if doc[i].get_text()!=other[i].get_text(): raise RuntimeError('Isolated core text mismatch')
                if doc[i].get_pixmap().samples!=other[i].get_pixmap().samples: raise RuntimeError('Isolated core raster mismatch')
            other.close()
            core_check={'status':'success','pages':len(doc),'all_page_text_equal':True,'all_page_raster_equal':True,'source_commit':source}
            save('CORE_REBUILD_RECEIPT.json',core_check)
    receipt={'schema':'gtf49.build/1','source_commit':source,'source_ancestor':BASE,'review_commit':REVIEW,
        'workflow_run':os.getenv('GITHUB_RUN_ID'),'core_only':args.core_only,'article_pages':len(doc),'article_sha256':sha(HOME/'paper.pdf'),
        'unchanged_sources_verified':len(manifest['unchanged_sources']),'archived_introductions_verified':len(manifest['archived_introductions']),
        'normal_optimized_agreement':True,'new_negative_control_executions':2*len(results['v49']['negative_controls_detected']),
        'inherited_v47_negative_control_executions':2*len(results['v47']['negative_controls_detected']),
        'regressions':results,'core_rebuild':core_check,'complete_volumes':archives,'core_archive_sha256':sha(EV/'CORE_SOURCES.zip'),**flags,
        'scope':'Executed exact finite checks, input-bound certificates and source-bound build/preservation; not independent proof, priority clearance or general higher-width optimization.'}
    if old is not None:
        receipt['supporting_article_sha256']=sha(HOME/'supporting-v47.pdf');receipt['source_archive_sha256']=sha(EV/'SUBMISSION_SOURCES.zip')
    save('BUILD_RECEIPT.json',receipt)
    package=[HOME/'paper.pdf',HOME/'RESPONSE_TO_REFEREE.md',HOME/'LITERATURE_AUDIT.md',EV/'CORE_SOURCES.zip',EV/'BUILD_RECEIPT.json',EV/'CUBIC_CERTIFICATE.json']
    if core_check: package.append(EV/'CORE_REBUILD_RECEIPT.json')
    zip_files(EV/'REFEREE_PACKAGE.zip',[(p,p.name) for p in package])
    if not args.core_only:
        root=HOME.parents[1]/'GENERAL_THETA_FOUNDATIONS_I_V49_REVIEW_READY.md'
        root.write_text('# General Theta Foundations I — Revision 49\n\n**Sign and Magnitude Duality for Numerical Word Realizations**\n\n'
            f'Validated native source: `{source}`. Controlling r30: `{REVIEW}`. Completed source ancestor v47: `{BASE}`.\n\n'
            f'[English article ({len(doc)} pages)](papers/{HOME.name}/paper.pdf) · [Native LaTeX](papers/{HOME.name}/main.tex) · [Response to r30](papers/{HOME.name}/RESPONSE_TO_REFEREE.md)\n\n'
            f'[Compact referee package](papers/{HOME.name}/evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](papers/{HOME.name}/evidence/CORE_SOURCES.zip) · [Build receipt](papers/{HOME.name}/evidence/BUILD_RECEIPT.json)\n\n'
            f'[Unchanged v47 article](papers/{HOME.name}/supporting-v47.pdf) · [Mathematical archive](papers/{HOME.name}/complete-manuscript.pdf) · [Development archive](papers/{HOME.name}/complete-development.pdf)\n\n'
            'Complete finite sign/magnitude alternative for antisymmetric all-two-state numerical targets; sparse integer multiplicative infeasibility witnesses; algebraic optimal errors and stochastic witnesses; exact cubic positive-error frontier with no rational minimizer; rational orthogonal bottleneck example; explicit rational Gram height bound.\n\n'
            'Fixed-sign matrix feasibility, monomial logarithms and Farkas alternatives are credited. The implemented exact rational threshold oracle is distinct from the proved general symbolic algebraic optimizer. Higher-width structural duality and unrelated analytic pipeline closure are not inferred. r30 reviews v46; v47 is a later source ancestor, not a manuscript with an invented r30 review. v48 and all old paths remain untouched.\n')
    doc.close()
    for suffix in ['aux','log','out','pdf']: (HOME/f'main.{suffix}').unlink(missing_ok=True)
    shutil.rmtree(HOME/'__pycache__',ignore_errors=True)
    print(json.dumps({'status':'success','pages':receipt['article_pages'],'source_commit':source,'core_only':args.core_only,'core_rebuild':core_check is not None,'new_negative_controls':receipt['new_negative_control_executions']}))

if __name__=='__main__': main()
