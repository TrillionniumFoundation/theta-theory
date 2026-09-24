#!/usr/bin/env python3
"""Source-pinned mathematical revision, explicit regressions and preservation."""
from __future__ import annotations
import hashlib,json,os,re,runpy,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
import fitz
from concurrent.futures import ThreadPoolExecutor
H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v28-causal-response'
V27=H.parent/'GTF-I-v27-resource-saddle'
V26=H.parent/'GTF-I-v26-controlled-memory-foundations'
V25=H.parent/'GTF-I-v25-controlled-minimax'
V24=H.parent/'GTF-I-v24-structural-resources'
E=H/'evidence'
BASE='9c8161e9df1b017fa2dfb46218a4fa42f42e9bdd'
PREVIOUS='cdc749027c5f7a6f66c572ea498cd15e1b1a3391'

def require(ok:bool,msg:str)->None:
    if not ok:raise RuntimeError(msg)

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def cmd(args:list[str],cwd:Path|None=None)->str:
    print('EXECUTE', ' '.join(args), flush=True)
    x=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if x.returncode:
        print(x.stdout)
        raise RuntimeError('Command failed: '+' '.join(args))
    return x.stdout

def main()->None:
    E.mkdir(exist_ok=True)
    existing=(H/'main.tex').read_bytes() if (H/'main.tex').exists() else None
    runpy.run_path(str(H/'assemble.py'))
    if existing is not None:require(existing==(H/'main.tex').read_bytes(),'Native main differs from its pinned assembly')
    shutil.copy2(H/'ASSEMBLY_MANIFEST.json',E/'ASSEMBLY_MANIFEST.json')
    regression={}
    versions=[('v29',H),('v28',O),('v27',V27),('v26',V26),('v25',V25),('v24',V24)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={(label,opt):pool.submit(cmd,[sys.executable,*(['-O'] if opt else []),str(path/'verify.py')])
                 for label,path in versions for opt in [False,True]}
        for label,path in versions:
            x=futures[label,False].result();y=futures[label,True].result()
            require(json.loads(x)==json.loads(y),label+' normal/optimized disagreement')
            regression[label]=json.loads(x)
            (E/(label.upper()+'_EXACT_CHECKS.json')).write_text(x)
    controls=[('v29',H,['missing-component','false-completeness','incompatible-update','free-memory','unread-action','marginal-product']),
              ('v28',O,['omit-leakage','independent-unconditional-noise','face-overlap','free-zero-coupling','eleven-states','delete-support']),
              ('v27',V27,['free-tie','face-overlap','residual-vertex','anticipating-action','nearest-value','mark-cost']),
              ('v26',V26,['cubic','coin','response','free-selector','unbalanced-minimax','calibration-register']),
              ('v24',V24,['certificate','selector','polynomial','profile','shared-row','autonomous'])]
    def negative(label,path,mode,mutant):
        print('NEGATIVE CONTROL',label,mode,mutant,flush=True)
        cp=subprocess.run([sys.executable,*mode,str(path/'verify.py'),'--mutant',mutant],text=True,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        require(cp.returncode!=0,'Undetected negative control '+label+':'+mutant)
        return {'version':label,'mode':mode,'mutant':mutant,'detected':True,
                'last_line':cp.stdout.strip().splitlines()[-1]}
    with ThreadPoolExecutor(max_workers=4) as pool:
        tasks=[pool.submit(negative,label,path,mode,name) for label,path,names in controls
               for mode in [[],['-O']] for name in names]
        mutants=[f.result() for f in tasks]
    (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(mutants,indent=2)+'\n')
    cmd([sys.executable,str(H/'verify.py'),'--emit',str(E/'STREAMING_ENCODER_N8.json')])
    with tempfile.TemporaryDirectory(prefix='gtf29-latex-') as td:
        work=Path(td)
        for p in H.glob('*.tex'):shutil.copy2(p,work/p.name)
        for _ in range(3):cmd(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],work)
        log=(work/'main.log').read_text(errors='replace')
        (E/'LATEX_LOG.txt').write_text(log)
        require(not re.search(r'(Reference|Citation) .+ undefined',log) and 'undefined references' not in log,'Undefined references/citations')
        require('Overfull \\hbox' not in log and 'Overfull \\vbox' not in log,'Overfull layout')
        shutil.copy2(work/'main.pdf',H/'paper.pdf')
        labels={m[1]:{'number':m[2],'page':m[3]} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',(work/'main.aux').read_text())}
        (E/'THEOREM_LOCATIONS.json').write_text(json.dumps(labels,indent=2,sort_keys=True)+'\n')
    doc=fitz.open(H/'paper.pdf');pages=len(doc)
    appendix_page=int(labels['sec:retained29']['page'])
    render_pages=set(range(appendix_page))|{pages-1}
    for lab in ['thm:intrinsic29','thm:tensor29','thm:access29','cor:contact-class29','prop:marked-csr29','thm:positive-saddle','prop:physical-acquisition','thm:all-clock-orders']:
        require(lab in labels,'Missing theorem label '+lab)
        render_pages.add(int(labels[lab]['page'])-1)
    for i in sorted(render_pages):doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(E/f'page-{i+1}.png')
    volumes={};comparisons=0;raster_comparisons=0
    for name in ['complete-manuscript.pdf','complete-development.pdf']:
        print('PRESERVE',name,flush=True)
        previous=fitz.open(O/name);out=fitz.open();out.insert_pdf(doc)
        page=out.new_page(width=612,height=792)
        page.insert_textbox(fitz.Rect(65,155,550,665),'PRESERVED PREDECESSOR\n\nGeneral Theta Foundations I, revision 28\n\nThe following predecessor volume is reproduced without alteration.\nThe complete current article precedes this divider.\n\nFrozen predecessor commit:\n'+PREVIOUS,fontsize=13)
        offset=len(out);out.insert_pdf(previous);out.save(H/name,garbage=4,deflate=True);out.close()
        combined=fitz.open(H/name)
        for i in range(len(previous)):
            require(combined[offset+i].get_text()==previous[i].get_text(),'Predecessor PDF text changed')
            if i in {0,1,len(previous)//4,len(previous)//2,3*len(previous)//4,len(previous)-1}:
                require(combined[offset+i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples==previous[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples,'Predecessor raster sample changed')
                raster_comparisons+=1
            comparisons+=1
        volumes[name]={'pages':len(combined),'predecessor_pages':len(previous),'sha256':sha(H/name),'predecessor_sha256':sha(O/name)}
        combined.close();previous.close()
    doc.close()
    sources={p.name:sha(p) for p in H.iterdir() if p.suffix in ['.tex','.py','.md','.json']}
    (E/'SOURCE_HASHES.json').write_text(json.dumps(sources,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(E/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in H.iterdir():
            if p.suffix in ['.tex','.py','.md','.json']:z.write(p,arcname=H.name+'/'+p.name)
        for p in O.iterdir():
            if p.suffix=='.tex' or p.name in ['verify.py','complete-manuscript.pdf','complete-development.pdf']:
                z.write(p,arcname=O.name+'/'+p.name)
        z.write(V27/'verify.py',arcname=V27.name+'/verify.py')
        z.write(V26/'verify.py',arcname=V26.name+'/verify.py')
        z.write(V25/'verify.py',arcname=V25.name+'/verify.py')
        z.write(V24/'verify.py',arcname=V24.name+'/verify.py')
    receipt={'schema':'gtf29.build/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted'),
             'workflow_trigger_commit':os.environ.get('GITHUB_SHA'),'workflow_run':os.environ.get('GITHUB_RUN_ID'),
             'review_commit':BASE,'predecessor_commit':PREVIOUS,'article_pages':pages,'supporting_appendices_start_page':appendix_page,'article_sha256':sha(H/'paper.pdf'),
             'complete_volumes':volumes,'predecessor_page_text_comparisons':comparisons,'predecessor_raster_sample_comparisons':raster_comparisons,
             'normal_optimized_agreement':True,'regressions':regression,'negative_control_executions':len(mutants),
             'undefined_references':False,'overfull_boxes':False,
             'scope':'Executed regressions and reproducible publication; not independent proof certification, priority clearance or journal acceptance.'}
    (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    (H.parent.parent/'GENERAL_THETA_FOUNDATIONS_I_V29_REVIEW_READY.md').write_text(
        '# General Theta Foundations I — revision 29\n\n'
        '**Intrinsic Continuation Geometry and Causal Memory**\n\n'
        f"Native source commit: `{receipt['source_commit']}`. Controlling r13 review: `{BASE}`.\n\n"
        f'[Canonical English article ({pages} pages)](papers/{H.name}/paper.pdf) · '
        f'[English LaTeX source](papers/{H.name}/main.tex) · '
        f'[Response to referee](papers/{H.name}/RESPONSE_TO_REFEREE.md)\n\n'
        f'[Complete mathematical manuscript](papers/{H.name}/complete-manuscript.pdf) · '
        f'[Complete preserved development](papers/{H.name}/complete-development.pdf) · '
        f'[Executed build receipt](papers/{H.name}/evidence/BUILD_RECEIPT.json)\n\n'
        f'The theorem spine precedes supporting appendices beginning on page {appendix_page}. '
        'Intrinsic support-component rank with a finite completeness test and simultaneous realization; '
        'multiplicative terminal-channel capacities; exact n+1 and 2^n binary-query regimes with adaptive acquisition.\n\n'
        'The intrinsic theorem is complete on its stated geometric class. The intermediate query-signal range '
        'and fully adaptive collision validation optimum are not identified with these results. '
        'Known-target atomic exactness and acquired calibration remain distinct. Historical A2/B4/C2 obligations are preserved.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':main()
