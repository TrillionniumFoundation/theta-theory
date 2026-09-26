#!/usr/bin/env python3
"""Source-bound revision-43 build; the core mode needs no historical PDFs."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
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

H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v42-canonical-gap-calibration'
E=H/'evidence'
BASE='d5fdba334f7a031413bba08c29af30a555936905'
PREVIOUS='b5f9874903a429f9c1a9cb080547d50c891d050a'
OLD_NAMES=['GTF-I-v42-canonical-gap-calibration','GTF-I-v41-intrinsic-action',
 'GTF-I-v39-orbit-response','GTF-I-v38-orbit-entropy','GTF-I-v37-spectral-memory',
 'GTF-I-v36-finite-alphabet-memory','GTF-I-v35-sharp-memory','GTF-I-v34-compatible-dynamics',
 'GTF-I-v33-compatible-lifts','GTF-I-v32-causal-width','GTF-I-v31-compatible-memory',
 'GTF-I-v30-streaming-geometry','GTF-I-v29-intrinsic-continuation','GTF-I-v28-causal-response',
 'GTF-I-v27-resource-saddle','GTF-I-v26-controlled-memory-foundations',
 'GTF-I-v25-controlled-minimax','GTF-I-v24-structural-resources']
NATIVE={'.tex','.py','.md','.json'}
CONTROL_NAMES=['omit-dilation','free-packet-length','wrong-metric-log','lose-rational-phase',
 'reverse-profile-order','drop-partition-constraints','false-convergent-separation','wrong-cubic-scale']


def require(ok: bool,message: str) -> None:
    if not ok: raise RuntimeError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str],cwd: Path|None=None) -> str:
    print('EXECUTE',' '.join(command),flush=True)
    result=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout,flush=True)
        raise RuntimeError('Failed: '+' '.join(command))
    return result.stdout


def save_json(path: Path,data) -> None:
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


def zip_sources(path: Path,extra: list[tuple[Path,str]]=()) -> None:
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(H.iterdir()):
            if p.suffix in NATIVE: z.write(p,arcname=H.name+'/'+p.name)
        for p,name in extra: z.write(p,arcname=name)


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--core-only',action='store_true')
    args=parser.parse_args();E.mkdir(exist_ok=True)
    manifest=json.loads((H/'PREDECESSOR_MANIFEST.json').read_text())
    if not args.core_only:
        for name,digest in {**manifest['source_files'],**manifest['pdfs']}.items():
            require((O/name).exists(),'Missing predecessor '+name+'; use --core-only for the small package')
            require(sha(O/name)==digest,'Frozen predecessor changed: '+name)
    shutil.copy2(H/'PREDECESSOR_MANIFEST.json',E/'PREDECESSOR_MANIFEST.json')
    shutil.copy2(H/'PROFILE_CERTIFICATE.json',E/'PROFILE_CERTIFICATE.json')
    versions=[('v43',H)]
    if not args.core_only: versions += [(name.split('-')[2],H.parent/name) for name in OLD_NAMES]
    regressions={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={(label,opt):pool.submit(run,[sys.executable,*(['-O'] if opt else []),str(path/'verify.py')])
                 for label,path in versions for opt in [False,True]}
        for label,path in versions:
            ordinary=json.loads(futures[label,False].result())
            optimized=json.loads(futures[label,True].result())
            require(ordinary==optimized,'Ordinary/optimized disagreement: '+label)
            regressions[label]=ordinary
            save_json(E/(label.upper()+'_EXACT_CHECKS.json'),ordinary)
    controls=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={(name,opt):pool.submit(subprocess.run,[sys.executable,*(['-O'] if opt else []),str(H/'verify.py'),'--negative-control',name],text=True,capture_output=True)
                 for name in CONTROL_NAMES for opt in [False,True]}
        for name in CONTROL_NAMES:
            for opt in [False,True]:
                result=futures[name,opt].result()
                require(result.returncode!=0 and 'CHECK_REJECTED:' in result.stderr,'Undetected negative control: '+name)
                controls.append({'mode':'optimized' if opt else 'ordinary','mutant':name,'detected':True,'reason':result.stderr.strip()})
    save_json(E/'NEGATIVE_CONTROLS.json',controls)
    run([sys.executable,str(H/'verify.py'),'--export',str(E/'EXPLICIT_ROWS.json')])
    for p in H.glob('*.tex'):
        require(all(ord(c)>=32 or c in '\n\t' for c in p.read_text()),'Bad control character: '+p.name)
    with tempfile.TemporaryDirectory(prefix='gtf43-tex-') as tmp:
        work=Path(tmp)
        for p in H.glob('*.tex'):shutil.copy2(p,work/p.name)
        for _ in range(3):run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],work)
        log=(work/'main.log').read_text(errors='replace')
        require(not re.search(r'(Reference|Citation) .+ undefined',log) and 'undefined references' not in log,'Unresolved reference')
        require('Overfull \\hbox' not in log and 'Overfull \\vbox' not in log,'Overfull box')
        require('Token not allowed in a PDF string' not in log,'Malformed PDF bookmark')
        (E/'LATEX_LOG.txt').write_text(log);shutil.copy2(work/'main.pdf',H/'paper.pdf')
        aux=(work/'main.aux').read_text()
        labels={m[1]:{'number':m[2],'page':int(m[3])}
                for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    needed=['thm:metric-main','thm:liouville-main','def:machine','lem:calibration',
      'prop:finite-profile','lem:packet','thm:profile','prop:caps','thm:enclosure',
      'prop:recoding','cor:balance','thm:circle-socp','prop:square-packet','cor:separated',
      'thm:arithmetic','lem:weak-denominator','cor:power-type','cor:ba',
      'lem:metric-separation','prop:metric-rates','cor:rational-extension',
      'lem:cf','thm:cubic-scales','prop:resonant-horizons','cor:liouville-explicit']
    require(all(key in labels for key in needed),'Missing principal theorem labels')
    save_json(E/'THEOREM_LOCATIONS.json',labels)
    doc=fitz.open(H/'paper.pdf'); pages=len(doc)
    for i in range(pages):
        doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(E/f'page-{i+1}.png')
    volumes={};texts=rasters=0
    if not args.core_only:
        shutil.copy2(O/'paper.pdf',H/'supporting-results.pdf')
        require(sha(H/'supporting-results.pdf')==manifest['pdfs']['paper.pdf'],'Supporting PDF changed')
        for name in ['complete-manuscript.pdf','complete-development.pdf']:
            print('PRESERVE',name,flush=True)
            old=fitz.open(O/name);out=fitz.open();out.insert_pdf(doc)
            page=out.new_page(width=612,height=792)
            remaining=page.insert_textbox(fitz.Rect(64,130,548,690),
               'PRESERVED MATHEMATICAL DEVELOPMENT\n\nGeneral Theta Foundations I - revision 42\n\n'
               'The complete current article precedes this divider.\n'
               'The following predecessor cumulative volume is reproduced without alteration.\n\n'
               'Frozen predecessor publication:\n'+PREVIOUS+'\n\n'
               'This archive is not part of the compact referee package. Independent historical '
               'analytic obligations retain their original hypotheses and proof status.',fontsize=12)
            require(remaining>=0,'Archive divider overflow')
            offset=len(out);out.insert_pdf(old);out.save(H/name,garbage=1,deflate=True);out.close()
            combined=fitz.open(H/name)
            samples={0,1,len(old)//4,len(old)//2,3*len(old)//4,len(old)-1}
            for i in range(len(old)):
                require(old[i].get_text()==combined[offset+i].get_text(),'Changed predecessor page text: '+name+':'+str(i))
                texts+=1
                if i in samples:
                    a=old[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
                    b=combined[offset+i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
                    require((a.width,a.height,a.samples)==(b.width,b.height,b.samples),'Changed predecessor sample raster')
                    rasters+=1
            volumes[name]={'pages':len(combined),'predecessor_pages':len(old),
                           'sha256':sha(H/name),'predecessor_sha256':sha(O/name)}
            old.close();combined.close()
    doc.close()
    sources={p.name:sha(p) for p in sorted(H.iterdir()) if p.suffix in NATIVE}
    save_json(E/'SOURCE_HASHES.json',sources)
    zip_sources(E/'CORE_SOURCES.zip')
    if not args.core_only:
        extra=[(O/name,O.name+'/'+name) for name in sorted({**manifest['source_files'],**manifest['pdfs']})]
        extra += [(H.parent/name/'verify.py',name+'/verify.py') for name in OLD_NAMES[1:]]
        zip_sources(E/'SUBMISSION_SOURCES.zip',extra)
    receipt={'schema':'gtf43.build/1','core_only':args.core_only,
       'source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted'),
       'workflow_trigger_commit':os.environ.get('GITHUB_SHA'),'workflow_run':os.environ.get('GITHUB_RUN_ID'),
       'review_commit':BASE,'predecessor_commit':PREVIOUS,'article_pages':pages,'article_sha256':sha(H/'paper.pdf'),
       'supporting_article_sha256':None if args.core_only else sha(H/'supporting-results.pdf'),
       'complete_volumes':volumes,'predecessor_source_files_verified':0 if args.core_only else len(manifest['source_files']),
       'predecessor_page_text_comparisons':texts,'predecessor_raster_sample_comparisons':rasters,
       'normal_optimized_agreement':True,'negative_control_executions':len(controls),'regressions':regressions,
       'undefined_references':False,'overfull_boxes':False,'malformed_bookmarks':False,
       'core_archive_sha256':sha(E/'CORE_SOURCES.zip'),
       'source_archive_sha256':None if args.core_only else sha(E/'SUBMISSION_SOURCES.zip'),
       'scope':'Executed finite algebra, labelled numerical diagnostics and source-bound publication/preservation. Not universal proof, independent priority certification, an optimized hidden-width solution or journal acceptance.'}
    save_json(E/'BUILD_RECEIPT.json',receipt)
    with zipfile.ZipFile(E/'REFEREE_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [H/'paper.pdf',H/'RESPONSE_TO_REFEREE.md',H/'LITERATURE_AUDIT.md',
          E/'CORE_SOURCES.zip',E/'THEOREM_LOCATIONS.json',E/'BUILD_RECEIPT.json',
          H/'PROFILE_CERTIFICATE.json',H/'PRIMARY_SOURCE_AUDIT.json']:
            z.write(p,arcname=p.name)
    root=H.parent.parent if H.parent.name=='papers' else H.parent
    (root/'GENERAL_THETA_FOUNDATIONS_I_V43_REVIEW_READY.md').write_text(
      '# General Theta Foundations I — Revision 43\n\n'
      '**Word Profiles and Arithmetic Fluctuations of Numerical Memory**\n\n'
      f'Native source commit: `{receipt["source_commit"]}`. Controlling r28: `{BASE}`.\n\n'
      f'[English article ({pages} pages)](papers/{H.name}/paper.pdf) · [Native LaTeX](papers/{H.name}/main.tex) · [Response to r28](papers/{H.name}/RESPONSE_TO_REFEREE.md)\n\n'
      f'[Compact referee package](papers/{H.name}/evidence/REFEREE_PACKAGE.zip) · [Core sources](papers/{H.name}/evidence/CORE_SOURCES.zip) · [Executed receipt](papers/{H.name}/evidence/BUILD_RECEIPT.json)\n\n'
      f'[Unchanged v42 article](papers/{H.name}/supporting-results.pdf) · [Mathematical archive](papers/{H.name}/complete-manuscript.pdf) · [Development archive](papers/{H.name}/complete-development.pdf)\n\n'
      'Finite optimized word distortion and compatible enclosure profiles give all-hidden interval/error bounds and exact common-row synthesis. Planar word-law optimization has a finite cone formulation. Minimal ordinary dual type gives exponent r/(2r+1), with explicit almost-everywhere logarithmic bounds. Every irrational angle has matched cubic convergent scales; every Liouville angle has liminf exponent zero and limsup at least one third, while width diverges.\n\n'
      'The endpoint mechanism and classical arithmetic are credited, including the direct DGLPS v2 comparison. The model is fixed-dimensional nonuniform clocked atomic-row label width, at fixed signal and small error. Exact finite widths, the precise Liouville limsup, a universal profile equality, independent priority certification and unrelated analytic pipeline closure are not claimed. All old paths and branches remain unchanged. Large archives are optional.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))


if __name__=='__main__':main()
