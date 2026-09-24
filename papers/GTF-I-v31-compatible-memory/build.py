#!/usr/bin/env python3
"""Build revision 31 and preserve the frozen revision-30 mathematical volumes."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,tempfile,zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz
H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v30-streaming-geometry'
E=H/'evidence'
BASE='cd793fde91fca07958c6c5bc3989e9c51a17540b'
PREVIOUS='a4abeb1c5e0323e5850e7f2446bf96fb1f7d4d8a'
OLDER=[('v30',O),('v29',H.parent/'GTF-I-v29-intrinsic-continuation'),('v28',H.parent/'GTF-I-v28-causal-response'),('v27',H.parent/'GTF-I-v27-resource-saddle'),('v26',H.parent/'GTF-I-v26-controlled-memory-foundations'),('v25',H.parent/'GTF-I-v25-controlled-minimax'),('v24',H.parent/'GTF-I-v24-structural-resources')]

def require(ok:bool,msg:str)->None:
    if not ok: raise RuntimeError(msg)

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args:list[str],cwd:Path|None=None)->str:
    print('EXECUTE',' '.join(args),flush=True)
    p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if p.returncode:
        print(p.stdout,flush=True)
        raise RuntimeError('Command failed: '+' '.join(args))
    return p.stdout

def main()->None:
    E.mkdir(exist_ok=True)
    manifest=json.loads((H/'PREDECESSOR_MANIFEST.json').read_text())
    require(manifest['predecessor_commit']==PREVIOUS,'Wrong predecessor')
    for name,value in {**manifest['source_files'],**manifest['pdfs']}.items():
        require(sha(O/name)==value,'Frozen predecessor changed: '+name)
    shutil.copy2(H/'PREDECESSOR_MANIFEST.json',E/'PREDECESSOR_MANIFEST.json')
    versions=[('v31',H),*OLDER]; regressions={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs={(label,opt):pool.submit(run,[sys.executable,*(['-O'] if opt else []),str(path/'verify.py')]) for label,path in versions for opt in [False,True]}
        for label,path in versions:
            ordinary=jobs[label,False].result();optimized=jobs[label,True].result()
            a,b=json.loads(ordinary),json.loads(optimized)
            require(a==b,'Optimized check disagreement: '+label)
            regressions[label]=a
            (E/(label.upper()+'_EXACT_CHECKS.json')).write_text(json.dumps(a,indent=2,sort_keys=True)+'\n')
    names=['incompatible-splice','center-shift','hadamard-assumption','coin-boundary','replacement-weight','query-factor']
    def negative(mode:list[str],name:str)->dict:
        p=subprocess.run([sys.executable,*mode,str(H/'verify.py'),'--negative-control',name],text=True,capture_output=True)
        require(p.returncode!=0 and 'CHECK_REJECTED:' in p.stderr,'Negative control not detected: '+name)
        return {'mode':mode,'mutant':name,'detected':True,'reason':p.stderr.strip()}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(negative,mode,name) for mode in [[],['-O']] for name in names]
        controls=[f.result() for f in futures]
    (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(controls,indent=2,sort_keys=True)+'\n')
    run([sys.executable,str(H/'verify.py'),'--export',str(E/'CRITICAL_SIMPLEX_ROWS.json')])
    with tempfile.TemporaryDirectory(prefix='gtf31-latex-') as td:
        work=Path(td)
        for p in H.glob('*.tex'): shutil.copy2(p,work/p.name)
        for _ in range(3): run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],work)
        log=(work/'main.log').read_text(errors='replace')
        require(not re.search(r'(Reference|Citation) .+ undefined',log) and 'undefined references' not in log,'Undefined references')
        require('Overfull \\hbox' not in log and 'Overfull \\vbox' not in log,'Overfull box')
        require('Token not allowed in a PDF string' not in log,'Malformed PDF bookmark')
        (E/'LATEX_LOG.txt').write_text(log)
        shutil.copy2(work/'main.pdf',H/'paper.pdf')
        aux=(work/'main.aux').read_text()
        labels={m[1]:{'number':m[2],'page':int(m[3])} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    must=['thm:slice','prop:slice-shift','thm:obstruction','thm:additive','thm:all-simplices','prop:critical-rows','cor:nonhadamard','prop:critical-tensor','prop:exactification','prop:finite-coins','def:automaton','prop:language']
    require(all(k in labels for k in must),'Missing main theorem label')
    (E/'THEOREM_LOCATIONS.json').write_text(json.dumps(labels,indent=2,sort_keys=True)+'\n')
    shutil.copy2(O/'paper.pdf',H/'supporting-results.pdf')
    require(sha(H/'supporting-results.pdf')==manifest['pdfs']['paper.pdf'],'Supporting article differs')
    doc=fitz.open(H/'paper.pdf');pages=len(doc)
    for i in range(pages): doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(E/f'page-{i+1}.png')
    volumes={};texts=rasters=0
    for name in ['complete-manuscript.pdf','complete-development.pdf']:
        print('PRESERVE',name,flush=True)
        old=fitz.open(O/name);out=fitz.open();out.insert_pdf(doc)
        p=out.new_page(width=612,height=792)
        rest=p.insert_textbox(fitz.Rect(64,130,548,690),'PRESERVED MATHEMATICAL DEVELOPMENT\n\nGeneral Theta Foundations I — revision 30\n\nThe entire current focused article precedes this divider.\nThe following cumulative predecessor volume is reproduced without alteration.\n\nFrozen predecessor publication:\n'+PREVIOUS+'\n\nThe independent geometric and analytic obligations of the historical program retain their stated hypotheses.',fontsize=12)
        require(rest>=0,'Divider text overflow')
        offset=len(out);out.insert_pdf(old);out.save(H/name,garbage=4,deflate=True);out.close()
        combined=fitz.open(H/name)
        samples={0,1,len(old)//4,len(old)//2,3*len(old)//4,len(old)-1}
        for i in range(len(old)):
            require(old[i].get_text()==combined[offset+i].get_text(),'Preserved text changed: '+name+':'+str(i))
            texts+=1
            if i in samples:
                a=old[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
                b=combined[offset+i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
                require(a.samples==b.samples and (a.width,a.height)==(b.width,b.height),'Preserved raster changed')
                rasters+=1
        volumes[name]={'pages':len(combined),'predecessor_pages':len(old),'sha256':sha(H/name),'predecessor_sha256':sha(O/name)}
        old.close();combined.close()
    doc.close()
    sources={p.name:sha(p) for p in sorted(H.iterdir()) if p.suffix in ['.tex','.py','.md','.json']}
    (E/'SOURCE_HASHES.json').write_text(json.dumps(sources,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(E/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in H.iterdir():
            if p.suffix in ['.tex','.py','.md','.json']: z.write(p,arcname=H.name+'/'+p.name)
        for p in O.iterdir():
            if p.name in manifest['source_files'] or p.name in manifest['pdfs']:
                z.write(p,arcname=O.name+'/'+p.name)
        for label,path in OLDER[1:]: z.write(path/'verify.py',arcname=path.name+'/verify.py')
    receipt={'schema':'gtf31.build/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted'),
      'workflow_trigger_commit':os.environ.get('GITHUB_SHA'),'workflow_run':os.environ.get('GITHUB_RUN_ID'),
      'review_commit':BASE,'predecessor_commit':PREVIOUS,'article_pages':pages,'article_sha256':sha(H/'paper.pdf'),
      'supporting_article_sha256':sha(H/'supporting-results.pdf'),'complete_volumes':volumes,
      'predecessor_source_files_verified':len(manifest['source_files']),
      'predecessor_page_text_comparisons':texts,'predecessor_raster_sample_comparisons':rasters,
      'normal_optimized_agreement':True,'negative_control_executions':len(controls),'regressions':regressions,
      'undefined_references':False,'overfull_boxes':False,'malformed_bookmarks':False,
      'source_archive_sha256':sha(E/'SUBMISSION_SOURCES.zip'),
      'scope':'Executed finite regressions, source-bound build and preservation; not independent mathematical proof verification, priority clearance or journal acceptance.'}
    (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    root=H.parent.parent if H.parent.name=='papers' else H.parent
    (root/'GENERAL_THETA_FOUNDATIONS_I_V31_REVIEW_READY.md').write_text(
      '# General Theta Foundations I — Revision 31\n\n**Compatibility of Positive Memory and Online Simplex Synthesis**\n\n'
      f"Native source commit: `{receipt['source_commit']}`. Controlling r15 report: `{BASE}`.\n\n"
      f'[Focused English article ({pages} pages)](papers/{H.name}/paper.pdf) · [Native LaTeX](papers/{H.name}/main.tex) · [Response to r15](papers/{H.name}/RESPONSE_TO_REFEREE.md)\n\n'
      f'[Unaltered v30 supporting article](papers/{H.name}/supporting-results.pdf) · [Complete mathematical manuscript](papers/{H.name}/complete-manuscript.pdf) · [Complete preserved development](papers/{H.name}/complete-development.pdf) · [Executed build receipt](papers/{H.name}/evidence/BUILD_RECEIPT.json)\n\n'
      'Canonical shift-closed affine slices and rank-two compatibility; a full-support rank-three family with exact Pareto profiles (3,4) and (4,3); same-label online synthesis for every additive encoder and every cube-enclosing simplex; explicit non-Hadamard critical encoders in dimensions five and nine; fair-bit implementation and internal automaton conventions.\n\n'
      'Classical cube absorption and the Kondo et al. v3 checkpoint exactification equivalence are expressly attributed. The new online transfer is not a new static threshold claim. Atomic rows, fair-bit samplers, one-query laws and autonomous phases have separate ledgers. Fully adaptive collision scheduling and historical A2/B4/C2 aggregate closure are not inferred.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__': main()
