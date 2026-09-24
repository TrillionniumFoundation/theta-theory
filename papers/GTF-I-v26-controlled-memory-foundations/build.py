#!/usr/bin/env python3
"""Source-pinned mathematical revision, explicit regressions and preservation."""
from __future__ import annotations
import hashlib,json,os,re,runpy,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
import fitz
H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v25-controlled-minimax'
V24=H.parent/'GTF-I-v24-structural-resources'
E=H/'evidence'
BASE='568301ff5d8991af9a99a478371c1c4993d0bcd1'
PREVIOUS='818ca30bab506cfedaf6aee4c32bedff70c1e251'

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
    for label,path in [('v26',H),('v25',O),('v24',V24)]:
        x=cmd([sys.executable,str(path/'verify.py')])
        y=cmd([sys.executable,'-O',str(path/'verify.py')])
        require(json.loads(x)==json.loads(y),label+' normal/optimized disagreement')
        regression[label]=json.loads(x)
        (E/(label.upper()+'_EXACT_CHECKS.json')).write_text(x)
    mutants=[]
    for label,path,names in [('v26',H,['cubic','coin','response','free-selector','unbalanced-minimax','calibration-register']),
                             ('v24',V24,['certificate','selector','polynomial','profile','shared-row','autonomous'])]:
        for mode in [[],['-O']]:
            for mutant in names:
                print('NEGATIVE CONTROL', label, mode, mutant, flush=True)
                cp=subprocess.run([sys.executable,*mode,str(path/'verify.py'),'--mutant',mutant],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                require(cp.returncode!=0,'Undetected negative control '+label+':'+mutant)
                mutants.append({'version':label,'mode':mode,'mutant':mutant,'detected':True,'last_line':cp.stdout.strip().splitlines()[-1]})
    (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(mutants,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='gtf26-latex-') as td:
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
    render_pages={0,pages-1}
    for lab in ['thm:predictive-quotient','thm:online-resolution','thm:joint-transport','thm:memory-dp','thm:routing-gap','thm:two-saddle','thm:two-family','thm:two-label-erasure','thm:transported-consumer']:
        require(lab in labels,'Missing theorem label '+lab)
        render_pages.add(int(labels[lab]['page'])-1)
    for i in sorted(render_pages):doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(E/f'page-{i+1}.png')
    volumes={};comparisons=0
    for name in ['complete-manuscript.pdf','complete-development.pdf']:
        print('PRESERVE',name,flush=True)
        previous=fitz.open(O/name);out=fitz.open();out.insert_pdf(doc)
        page=out.new_page(width=612,height=792)
        page.insert_textbox(fitz.Rect(65,155,550,665),'PRESERVED PREDECESSOR\n\nGeneral Theta Foundations I, revision 25\n\nThe following predecessor volume is reproduced without alteration.\nThe complete current article precedes this divider.\n\nFrozen predecessor commit:\n'+PREVIOUS,fontsize=13)
        offset=len(out);out.insert_pdf(previous);out.save(H/name,garbage=4,deflate=True);out.close()
        combined=fitz.open(H/name)
        for i in range(len(previous)):
            require(combined[offset+i].get_text()==previous[i].get_text(),'Predecessor PDF text changed')
            require(combined[offset+i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples==previous[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples,'Predecessor raster changed')
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
        z.write(V24/'verify.py',arcname=V24.name+'/verify.py')
    receipt={'schema':'gtf26.build/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted'),
             'workflow_trigger_commit':os.environ.get('GITHUB_SHA'),'workflow_run':os.environ.get('GITHUB_RUN_ID'),
             'review_commit':BASE,'predecessor_commit':PREVIOUS,'article_pages':pages,'article_sha256':sha(H/'paper.pdf'),
             'complete_volumes':volumes,'predecessor_page_text_and_raster_comparisons':comparisons,
             'normal_optimized_agreement':True,'regressions':regression,'negative_control_executions':len(mutants),
             'undefined_references':False,'overfull_boxes':False,
             'scope':'Executed regressions and reproducible publication; not independent proof certification, priority clearance or journal acceptance.'}
    (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    (H.parent.parent/'GENERAL_THETA_FOUNDATIONS_I_V26_REVIEW_READY.md').write_text(
        '# General Theta Foundations I — revision 26\n\n'
        '**Causal Experiments, Finite-Memory Control, and Exact Minimax Laws**\n\n'
        f"Native source commit: `{receipt['source_commit']}`. Controlling r9 review: `{BASE}`.\n\n"
        f'[Canonical English article ({pages} pages)](papers/{H.name}/paper.pdf) · '
        f'[English LaTeX source](papers/{H.name}/main.tex) · '
        f'[Response to referee](papers/{H.name}/RESPONSE_TO_REFEREE.md)\n\n'
        f'[Complete mathematical manuscript](papers/{H.name}/complete-manuscript.pdf) · '
        f'[Complete preserved development](papers/{H.name}/complete-development.pdf) · '
        f'[Executed build receipt](papers/{H.name}/evidence/BUILD_RECEIPT.json)\n\n'
        'Exact two-preparation marked saddle and continuous gamma family; a sharp informative-control finite-register ceiling law and charged-selector gap; restored foundational predictive quotient and acquired causal transport; integer revelation laws.\n\n'
        'The collision score is exact at N=2 and W>=12; the least peak at N=2 and the full widths 3–11 frontier are not identified with that result. Independent A2 and B4/C2 obligations are preserved.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':main()
