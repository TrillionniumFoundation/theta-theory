#!/usr/bin/env python3
"""Source-bound revision-45 build; the core mode needs no historical PDFs."""
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
O=H.parent/'GTF-I-v44-hankel-resonance'
E=H/'evidence'
BASE='6e8a9504a1a0820e6195317df885d99aed06c878'
PREVIOUS='d7042cf71485f661e27d87d12ffae35a2edfc15c'
OLD_NAMES=['GTF-I-v44-hankel-resonance','GTF-I-v43-arithmetic-profile','GTF-I-v42-canonical-gap-calibration','GTF-I-v41-intrinsic-action',
 'GTF-I-v39-orbit-response','GTF-I-v38-orbit-entropy','GTF-I-v37-spectral-memory',
 'GTF-I-v36-finite-alphabet-memory','GTF-I-v35-sharp-memory','GTF-I-v34-compatible-dynamics',
 'GTF-I-v33-compatible-lifts','GTF-I-v32-causal-width','GTF-I-v31-compatible-memory',
 'GTF-I-v30-streaming-geometry','GTF-I-v29-intrinsic-continuation','GTF-I-v28-causal-response',
 'GTF-I-v27-resource-saddle','GTF-I-v26-controlled-memory-foundations',
 'GTF-I-v25-controlled-minimax','GTF-I-v24-structural-resources']
NATIVE={'.tex','.py','.md','.json'}
CONTROL_NAMES=['omit-clock-drift','omit-tail-conjugates','reverse-cocycle-order',
 'ambient-instead-active','drop-row-compatibility','drop-normalization',
 'ignore-moving-projection','drop-minimum-branch']


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
    for name in ['finite-bit-memory.tex','finite_bit.py']:
        require(sha(H/name)==manifest['source_files'][name],'Inherited finite-bit module changed: '+name)
    compiler=json.loads(run([sys.executable,str(H/'finite_bit.py'),'--horizon','16','--angles','2']))
    save_json(E/'FINITE_BIT_COMPILER_CHECK.json',compiler)
    versions=[('v45',H)]
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
    with tempfile.TemporaryDirectory(prefix='gtf45-tex-') as tmp:
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
    needed=['thm:main45','lem:tail45','lem:stabilize45','lem:positive-packet45',
      'thm:decision45','thm:flag45','thm:comparison45','prop:zero-packet45',
      'prop:rank-three45','cor:planar-dichotomy45','thm:metric-main','thm:liouville-main',
      'thm:profile','thm:circle-socp','thm:cubic-scales','thm:uniform44','cor:space44']
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
               'PRESERVED MATHEMATICAL DEVELOPMENT\n\nGeneral Theta Foundations I - revision 44\n\n'
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
    receipt={'schema':'gtf45.build/1','core_only':args.core_only,
       'source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-uncommitted'),
       'workflow_trigger_commit':os.environ.get('GITHUB_SHA'),'workflow_run':os.environ.get('GITHUB_RUN_ID'),
       'review_commit':BASE,'predecessor_commit':PREVIOUS,'article_pages':pages,'article_sha256':sha(H/'paper.pdf'),
       'supporting_article_sha256':None if args.core_only else sha(H/'supporting-results.pdf'),
       'complete_volumes':volumes,'predecessor_source_files_verified':0 if args.core_only else len(manifest['source_files']),
       'predecessor_page_text_comparisons':texts,'predecessor_raster_sample_comparisons':rasters,
       'normal_optimized_agreement':True,'negative_control_executions':len(controls),'regressions':regressions,'finite_bit_compiler_check':compiler,
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
    (root/'GENERAL_THETA_FOUNDATIONS_I_V45_REVIEW_READY.md').write_text(
      '# General Theta Foundations I — Revision 45\n\n'
      '**A Boundedness Criterion for Numerical Realization**\n\n'
      f'Native source commit: `{receipt["source_commit"]}`. Controlling r29: `{BASE}`. Preserved v44 publication: `{PREVIOUS}`.\n\n'
      f'[English article ({pages} pages)](papers/{H.name}/paper.pdf) · [Native LaTeX](papers/{H.name}/main.tex) · [Response to r29](papers/{H.name}/RESPONSE_TO_REFEREE.md)\n\n'
      f'[Compact referee package](papers/{H.name}/evidence/REFEREE_PACKAGE.zip) · [Core sources](papers/{H.name}/evidence/CORE_SOURCES.zip) · [Build receipt](papers/{H.name}/evidence/BUILD_RECEIPT.json)\n\n'
      f'[Unchanged v44 article](papers/{H.name}/supporting-results.pdf) · [Mathematical archive](papers/{H.name}/complete-manuscript.pdf) · [Development archive](papers/{H.name}/complete-development.pdf)\n\n'
      'Uniformly bounded exact width is equivalent to finiteness of the closed normal subgroup generated by equal-length command differences on the active seed space. Otherwise width tends to infinity at fixed sufficiently small wordwise error. No commutativity, connectedness, Diophantine hypothesis or spectral gap is assumed. Algebraic inputs admit a finite decision by a proved group-order bound.\n\n'
      'The continuation-flag formula, packet/enclosure comparison, metric arithmetic proofs and finite-bit compiler remain. General rates, sharp finite integer optima, independent priority clearance and unrelated analytic pipeline closure are not asserted. All predecessor paths and branches remain unchanged.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))


if __name__=='__main__':main()
