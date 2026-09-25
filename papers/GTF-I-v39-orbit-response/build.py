#!/usr/bin/env python3
"""Source-bound v39 build, with an optional small, archive-free core build."""
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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz

H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v38-orbit-entropy'
E=H/'evidence'
BASE='5439c0ea2540e3caddbab600cc7a4f8699421439'
PREVIOUS='8ec190c921656b9869f3520ec9bf7bf754622e97'
OLD_NAMES=['GTF-I-v38-orbit-entropy','GTF-I-v37-spectral-memory','GTF-I-v36-finite-alphabet-memory','GTF-I-v35-sharp-memory','GTF-I-v34-compatible-dynamics','GTF-I-v33-compatible-lifts','GTF-I-v32-causal-width','GTF-I-v31-compatible-memory','GTF-I-v30-streaming-geometry',
 'GTF-I-v29-intrinsic-continuation','GTF-I-v28-causal-response',
 'GTF-I-v27-resource-saddle','GTF-I-v26-controlled-memory-foundations',
 'GTF-I-v25-controlled-minimax','GTF-I-v24-structural-resources']
NATIVE={'.tex','.py','.md','.json'}


def require(ok:bool,msg:str)->None:
    if not ok: raise RuntimeError(msg)


def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(args:list[str],cwd:Path|None=None)->str:
    print('EXECUTE',' '.join(args),flush=True)
    p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if p.returncode:
        print(p.stdout,flush=True)
        raise RuntimeError('Command failed: '+' '.join(args))
    return p.stdout


def zip_sources(path:Path,extra:list[tuple[Path,str]]=())->None:
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(H.iterdir()):
            if p.suffix in NATIVE: z.write(p,arcname=H.name+'/'+p.name)
        for p,name in extra: z.write(p,arcname=name)


def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--core-only',action='store_true')
    args=parser.parse_args();E.mkdir(exist_ok=True)
    manifest=json.loads((H/'PREDECESSOR_MANIFEST.json').read_text())
    require(manifest['predecessor_commit']==PREVIOUS,'Wrong predecessor identity')
    if not args.core_only:
        for name,value in {**manifest['source_files'],**manifest['pdfs']}.items():
            require((O/name).is_file(),'Missing preserved predecessor '+name+'; use --core-only for the small archive')
            require(sha(O/name)==value,'Frozen predecessor changed: '+name)
    shutil.copy2(H/'PREDECESSOR_MANIFEST.json',E/'PREDECESSOR_MANIFEST.json')
    shutil.copy2(H/'GAP_CERTIFICATE.json',E/'GAP_CERTIFICATE.json')
    versions=[('v39',H)]
    if not args.core_only: versions += [(name.split('-')[2],H.parent/name) for name in OLD_NAMES]
    regressions={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs={(label,opt):pool.submit(run,[sys.executable,*(['-O'] if opt else []),str(path/'verify.py')])
              for label,path in versions for opt in [False,True]}
        for label,path in versions:
            ordinary=json.loads(jobs[label,False].result())
            optimized=json.loads(jobs[label,True].result())
            require(ordinary==optimized,'Optimized disagreement '+label)
            regressions[label]=ordinary
            (E/(label.upper()+'_EXACT_CHECKS.json')).write_text(json.dumps(ordinary,indent=2,sort_keys=True)+'\n')
    names=['generic-orbit-exponent','fixed-vector-small-ball','unnormalized-sign-row','attenuation-is-exact-numeric',
           'minimum-across-constituents','missing-branch-amplification','quaternion-trace-is-real','unsquared-gap']
    controls=[]
    for mode in [[],['-O']]:
        for name in names:
            p=subprocess.run([sys.executable,*mode,str(H/'verify.py'),'--negative-control',name],text=True,capture_output=True)
            require(p.returncode!=0 and 'CHECK_REJECTED:' in p.stderr,'Undetected negative control '+name)
            controls.append({'mode':mode,'mutant':name,'detected':True,'reason':p.stderr.strip()})
    (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(controls,indent=2,sort_keys=True)+'\n')
    run([sys.executable,str(H/'verify.py'),'--export',str(E/'EXPLICIT_ROWS.json')])
    for p in H.glob('*.tex'):
        require(all(ord(c)>=32 or c in '\n\t' for c in p.read_text()),'Control character in '+p.name)
    with tempfile.TemporaryDirectory(prefix='gtf39-latex-') as td:
        work=Path(td)
        for p in H.glob('*.tex'): shutil.copy2(p,work/p.name)
        for _ in range(3): run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],work)
        log=(work/'main.log').read_text(errors='replace')
        require(not re.search(r'(Reference|Citation) .+ undefined',log) and 'undefined references' not in log,'Unresolved reference')
        require('Overfull \\hbox' not in log and 'Overfull \\vbox' not in log,'Overfull box')
        require('Token not allowed in a PDF string' not in log,'Malformed bookmark')
        (E/'LATEX_LOG.txt').write_text(log)
        shutil.copy2(work/'main.pdf',H/'paper.pdf')
        aux=(work/'main.aux').read_text()
        labels={m[1]:{'number':m[2],'page':int(m[3])}
                for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    must=['thm:main','def:machine','thm:uniform-orbits','cor:intrinsic-budget','thm:occupation',
          'lem:orbit-enclosure','thm:orbit-upper','cor:irreducible-width','thm:sum-width','prop:separate-width39',
          'prop:matrix-orbits','cor:projective39','prop:harmonic-family','prop:sign-simulator',
          'cor:semantic-separation','prop:lps-transfer39','thm:effective','thm:all-spectra','thm:projective-upper']
    require(all(k in labels for k in must),'Missing principal labels')
    (E/'THEOREM_LOCATIONS.json').write_text(json.dumps(labels,indent=2,sort_keys=True)+'\n')
    doc=fitz.open(H/'paper.pdf');pages=len(doc)
    for i in range(pages):
        doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(E/f'page-{i+1}.png')
    volumes={};texts=rasters=0
    if not args.core_only:
        shutil.copy2(O/'paper.pdf',H/'supporting-results.pdf')
        require(sha(H/'supporting-results.pdf')==manifest['pdfs']['paper.pdf'],'Supporting article changed')
        for name in ['complete-manuscript.pdf','complete-development.pdf']:
            print('PRESERVE',name,flush=True)
            old=fitz.open(O/name);out=fitz.open();out.insert_pdf(doc)
            p=out.new_page(width=612,height=792)
            rest=p.insert_textbox(fitz.Rect(64,130,548,690),
              'PRESERVED MATHEMATICAL DEVELOPMENT\n\nGeneral Theta Foundations I - revision 38\n\n'
              'The complete current article precedes this divider.\n'
              'The following predecessor cumulative volume is reproduced without alteration.\n\n'
              'Frozen predecessor publication:\n'+PREVIOUS+'\n\n'
              'This archive is not part of the compact referee package. Independent historical analytic '
              'obligations keep their original hypotheses and proof status.',fontsize=12)
            require(rest>=0,'Divider overflow')
            offset=len(out);out.insert_pdf(old);out.save(H/name,garbage=1,deflate=True);out.close()
            combined=fitz.open(H/name)
            samples={0,1,len(old)//4,len(old)//2,3*len(old)//4,len(old)-1}
            for i in range(len(old)):
                require(old[i].get_text()==combined[offset+i].get_text(),'Changed predecessor text '+name+':'+str(i))
                texts+=1
                if i in samples:
                    a=old[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
                    b=combined[offset+i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
                    require(a.samples==b.samples and (a.width,a.height)==(b.width,b.height),'Changed predecessor raster')
                    rasters+=1
            volumes[name]={'pages':len(combined),'predecessor_pages':len(old),
                           'sha256':sha(H/name),'predecessor_sha256':sha(O/name)}
            old.close();combined.close()
    doc.close()
    sources={p.name:sha(p) for p in sorted(H.iterdir()) if p.suffix in NATIVE}
    (E/'SOURCE_HASHES.json').write_text(json.dumps(sources,indent=2,sort_keys=True)+'\n')
    zip_sources(E/'CORE_SOURCES.zip')
    if not args.core_only:
        extra=[(O/name,O.name+'/'+name) for name in sorted({**manifest['source_files'],**manifest['pdfs']})]
        extra += [(H.parent/name/'verify.py',name+'/verify.py') for name in OLD_NAMES[1:]]
        zip_sources(E/'SUBMISSION_SOURCES.zip',extra)
    receipt={'schema':'gtf39.build/1','core_only':args.core_only,
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
       'scope':'Executed finite algebra, labelled numerical diagnostics, source-bound build and preservation; not independent proof certification, optimized finite constants, priority clearance or journal acceptance.'}
    (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(E/'REFEREE_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [H/'paper.pdf',H/'RESPONSE_TO_REFEREE.md',H/'LITERATURE_AUDIT.md',
                  E/'CORE_SOURCES.zip',E/'THEOREM_LOCATIONS.json',E/'BUILD_RECEIPT.json',H/'GAP_CERTIFICATE.json']:
            z.write(p,arcname=p.name)
    root=H.parent.parent if H.parent.name=='papers' else H.parent
    (root/'GENERAL_THETA_FOUNDATIONS_I_V39_REVIEW_READY.md').write_text(
      '# General Theta Foundations I — Revision 39\n\n**Minimal Orbits and the Width of Numerical Experiments**\n\n'
      f'Native source commit: `{receipt["source_commit"]}`. Controlling r23: `{BASE}`.\n\n'
      f'[English article ({pages} pages)](papers/{H.name}/paper.pdf) · [Native LaTeX](papers/{H.name}/main.tex) · [Response to r23](papers/{H.name}/RESPONSE_TO_REFEREE.md)\n\n'
      f'[Compact referee package](papers/{H.name}/evidence/REFEREE_PACKAGE.zip) · [Core sources](papers/{H.name}/evidence/CORE_SOURCES.zip) · [Executed receipt](papers/{H.name}/evidence/BUILD_RECEIPT.json)\n\n'
      f'[Unchanged v38 article](papers/{H.name}/supporting-results.pdf) · [Mathematical archive](papers/{H.name}/complete-manuscript.pdf) · [Development archive](papers/{H.name}/complete-development.pdf)\n\n'
      'Full-gap numerical width is Theta(N^(s/2)) for an irreducible compact connected representation, where s is its minimum nontrivial orbit dimension. For spanning reducible seeds at the stated small signal and error, use the maximum of those constituent minima. Uniform all-strata orbital geometry, paid common-row synthesis, constant separate positive minima, and an explicit numerical/cutpoint separation are proved.\n\n'
      'The projective and effective six-gate results remain. Full expansion, fixed calibrated signal/error and nonuniform atomic-row resources are explicit. The original LPS theorem number has not been verified from the original full text; the exact required arithmetic inequality and every subsequent normalization are stated separately. Independent historical analytic closure and priority certification are not inferred. Large archives are optional.\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__': main()
