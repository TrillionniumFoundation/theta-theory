#!/usr/bin/env python3
"""Assemble an additive, source-pinned revision and execute its build."""
from __future__ import annotations
import hashlib
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

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'GTF-I-v24-structural-resources'
REVIEW='c5c1a0d64f830bc3f036292357d8bbe2dbd04ca6'
OLD_HEAD='ad1336e48e414b2c01e928b844c796ab4765178b'
SOURCE_BLOB='8574b9769a88ef71d3494b2d310f699cb3515f84'
EVIDENCE=HERE/'evidence'


def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(args: list[str], cwd: Path|None=None) -> str:
    result=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout)
        raise RuntimeError('Command failed: '+' '.join(args))
    return result.stdout


def replace_once(text: str, old: str, new: str) -> str:
    require(text.count(old)==1,'Expected one source match: '+old[:100])
    return text.replace(old,new,1)


def assemble() -> dict:
    raw=(OLD/'main.tex').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob==SOURCE_BLOB,'Unpinned predecessor manuscript')
    text=raw.decode()
    pre=text.split('\\begin{abstract}',1)[0]
    pre=replace_once(pre,'Statistical Resource Duality and Two-Preparation Physical Certification','Controlled Experiment Duality and Exact Marked Minimax Laws')
    pre=pre.replace('Revision 24','Revision 25').replace('[Statistical resource duality]','[Controlled statistical minimax]')
    model='\\section{Experiments, architectures and attainable resources}'
    physical='\\section{The physical experiment and its sharp preparation boundary}'
    quantitative='\\section{Quantitative certificates for a finite compatible architecture}'
    body=text[text.index(model):text.index('\\begin{thebibliography}')]
    body=replace_once(body,physical,'\\input{controlled-dual}\n\\input{marked-minimax}\n\\input{physical-bridge}\n\n'+physical)
    body=replace_once(body,quantitative,'\\input{physical-improvement}\n\\input{joint-revelation}\n\n'+quantitative)
    body=replace_once(body,'\\cite[physical-complexity, feedback-completion lemma]{Companion}',
                      'Definition~\\ref{def:physical-class} and Theorem~\\ref{thm:local-physical}')
    body=replace_once(body,'the inherited microscopic\nestimate','the local microscopic\nestimate')
    body=replace_once(body,'is proved in the retained microscopic-composition\nand physical-complexity modules \\cite{Companion}',
                     'is proved in Theorem~\\ref{thm:local-physical}')
    bib=text[text.index('\\begin{thebibliography}'):]
    bib=replace_once(bib,'\\begin{thebibliography}{99}',
        '\\begin{thebibliography}{99}\n\\bibitem{SmallwoodSondik} R. D. Smallwood and E. J. Sondik,\nThe optimal control of partially observable Markov processes over a finite horizon,\n\\emph{Operations Research} \\textbf{21} (1973), 1071--1088.')
    main=pre+(HERE/'introduction.tex').read_text()+'\n'+body+bib
    (HERE/'main.tex').write_text(main)
    return {'predecessor_source_git_blob':blob,'predecessor_source_sha256':hashlib.sha256(raw).hexdigest(),
            'strategy':'All substantive v24 body sections retained; new theorem modules inserted; three physical-reference replacements; new introduction and one bibliography entry.',
            'new_modules':['controlled-dual.tex','marked-minimax.tex','physical-bridge.tex','physical-improvement.tex','joint-revelation.tex']}


def main() -> None:
    EVIDENCE.mkdir(exist_ok=True)
    assembly=assemble()
    (EVIDENCE/'ASSEMBLY_MANIFEST.json').write_text(json.dumps(assembly,indent=2)+'\n')
    check=command([sys.executable,str(HERE/'verify.py')])
    optimized=command([sys.executable,'-O',str(HERE/'verify.py')])
    require(json.loads(check)==json.loads(optimized),'New normal/optimized disagreement')
    (EVIDENCE/'EXACT_CHECKS.json').write_text(check)
    oldcheck=command([sys.executable,str(OLD/'verify.py'),'--output-dir',str(EVIDENCE/'v24')])
    oldoptimized=command([sys.executable,'-O',str(OLD/'verify.py')])
    require(json.loads(oldcheck)==json.loads(oldoptimized),'Predecessor normal/optimized disagreement')
    (EVIDENCE/'V24_REGRESSION.json').write_text(oldcheck)
    mutants=[]
    for mode in [[],['-O']]:
        for mutant in ['certificate','selector','polynomial','profile','shared-row','autonomous']:
            cp=subprocess.run([sys.executable,*mode,str(OLD/'verify.py'),'--mutant',mutant],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            require(cp.returncode!=0,'Undetected predecessor negative control: '+mutant)
            mutants.append({'mode':'optimized' if mode else 'ordinary','mutant':mutant,'detected':True})
    (EVIDENCE/'NEGATIVE_CONTROLS.json').write_text(json.dumps(mutants,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='gtf25-tex-') as td:
        work=Path(td)
        for p in HERE.glob('*.tex'): shutil.copy2(p,work/p.name)
        for _ in range(3):
            log=command(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],work)
        latex=(work/'main.log').read_text(errors='replace')
        (EVIDENCE/'LATEX_LOG.txt').write_text(latex)
        require('undefined references' not in latex and 'undefined citations' not in latex,'Undefined references')
        require(not re.search(r'(Reference|Citation) .+ undefined',latex),'Undefined citation or reference')
        require('Overfull \\hbox' not in latex and 'Overfull \\vbox' not in latex,'Overfull layout')
        shutil.copy2(work/'main.pdf',HERE/'paper.pdf')
        labels={}
        for match in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',(work/'main.aux').read_text()):
            labels[match[1]]={'number':match[2],'page':match[3]}
        (EVIDENCE/'THEOREM_LOCATIONS.json').write_text(json.dumps(labels,indent=2,sort_keys=True)+'\n')
    doc=fitz.open(HERE/'paper.pdf')
    pages=len(doc)
    require(pages<=45,'Canonical article unexpectedly cumulative')
    for i in [0,min(4,pages-1),min(9,pages-1),pages-1]:
        doc[i].get_pixmap(matrix=fitz.Matrix(1,1)).save(EVIDENCE/f'page-{i+1}.png')
    volumes={}
    comparisons=0
    for filename in ['complete-manuscript.pdf','complete-development.pdf']:
        previous=fitz.open(OLD/filename)
        volume=fitz.open()
        volume.insert_pdf(doc)
        page=volume.new_page(width=612,height=792)
        page.insert_textbox(fitz.Rect(65,170,550,650),
            'PRESERVED PREDECESSOR\n\nGeneral Theta Foundations I, revision 24\n\nThe following volume is reproduced without alteration.\nThe current revision precedes this divider.\n\nPredecessor commit:\n'+OLD_HEAD,fontsize=13)
        start=len(volume)
        volume.insert_pdf(previous)
        out=HERE/filename
        volume.save(out,garbage=4,deflate=True)
        volume.close()
        combined=fitz.open(out)
        for i in range(len(previous)):
            require(combined[start+i].get_text()==previous[i].get_text(),'Preserved PDF text differs')
            a=combined[start+i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
            b=previous[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
            require(a.samples==b.samples,'Preserved PDF raster differs')
            comparisons+=1
        volumes[filename]={'pages':len(combined),'predecessor_pages':len(previous),'sha256':sha(out),'predecessor_sha256':sha(OLD/filename)}
        combined.close();previous.close()
    doc.close()
    source_files={p.name:sha(p) for p in HERE.iterdir() if p.suffix in ['.tex','.py','.md','.json']}
    (EVIDENCE/'SOURCE_HASHES.json').write_text(json.dumps(source_files,indent=2,sort_keys=True)+'\n')
    inherited_sources={p.name:sha(p) for p in OLD.iterdir() if p.suffix in ['.tex','.py','.md','.json']}
    (EVIDENCE/'PREDECESSOR_SOURCE_HASHES.json').write_text(json.dumps(inherited_sources,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(EVIDENCE/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for p in HERE.iterdir():
            if p.suffix in ['.tex','.py','.md','.json']:
                archive.write(p,arcname=HERE.name+'/'+p.name)
        for name in ['main.tex','verify.py','complete-manuscript.pdf','complete-development.pdf']:
            archive.write(OLD/name,arcname=OLD.name+'/'+name)
    receipt={'schema':'gtf25.build/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted'),
             'review_commit':REVIEW,'predecessor_commit':OLD_HEAD,'workflow_run':os.environ.get('GITHUB_RUN_ID'),
             'article_pages':pages,'article_sha256':sha(HERE/'paper.pdf'),'complete_volumes':volumes,
             'preserved_page_comparisons':comparisons,'new_exact_checks':json.loads(check),
             'v24_checks_rerun':json.loads(oldcheck),'negative_control_executions':len(mutants)+6,
             'normal_optimized_agreement':True,'undefined_references':False,'overfull_boxes':False,
             'scope':'Build and algebraic regressions are not independent proof certification, priority clearance or acceptance.'}
    (EVIDENCE/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    root=HERE.parent.parent
    root.joinpath('GENERAL_THETA_FOUNDATIONS_I_V25_REVIEW_READY.md').write_text(
        '# General Theta Foundations I — revision 25\n\n'
        '**Controlled Experiment Duality and Exact Marked Minimax Laws**\n\n'
        f"Source commit: `{receipt['source_commit']}`. Controlling r8 review: `{REVIEW}`.\n\n"
        f"[Canonical English article ({pages} pages)](papers/{HERE.name}/paper.pdf) · "
        f"[Complete mathematical manuscript](papers/{HERE.name}/complete-manuscript.pdf) · "
        f"[Complete preserved development](papers/{HERE.name}/complete-development.pdf)\n\n"
        f"[Response to r8](papers/{HERE.name}/RESPONSE_TO_REFEREE.md) · "
        f"[Reproduction and scope](papers/{HERE.name}/README.md) · "
        f"[Build receipt](papers/{HERE.name}/evidence/BUILD_RECEIPT.json)\n\n"
        'The exact marked one-preparation value is `(85-7*sqrt(73))/64`; '
        'the controlled dual no longer requires a dominating action. '
        'The physical two-preparation theorem is self-contained and its threshold interval is enlarged. '
        'An exact preparation/decision-memory law is proved for the separate erasure family. '
        'The collision least peak at two preparations, U2, and historical B4/C2 aggregate closure are not claimed.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__': main()
