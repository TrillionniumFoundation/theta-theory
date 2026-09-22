#!/usr/bin/env python3
"""Rebuild the complete v4 article from hash-bound native sources."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok:bool,msg:str)->None:
    if not ok:raise SystemExit(msg)
def run(args:list[str],cwd:Path,env=None):
    return subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
def main()->None:
    for exe in ['pdflatex','pdfinfo']:require(shutil.which(exe) is not None,'Missing '+exe)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    for path,digest in manifest['input_sha256'].items():require(sha(REPO/path)==digest,'Source changed: '+path)
    expected_references=(REPO/'papers/GTF-I-v3/references.tex').read_text().replace('\\end{thebibliography}',(ROOT/'new-references.tex').read_text()+'\n\\end{thebibliography}')
    require((ROOT/'references.tex').read_text()==expected_references,'Bibliography does not preserve v3 entries')
    old_v2=(REPO/'papers/GTF-I-v2/revision.tex').read_bytes();marker=b'\\section{Acquired geometry and nonuniform causal resolution}'
    require((REPO/'papers/GTF-I-v3/retained-results.tex').read_bytes()==old_v2[old_v2.index(marker):],'Retained v2 mathematical body changed')
    preserved={}
    source_commit=os.environ.get('GTF_SOURCE_SHA') or os.environ.get('GITHUB_SHA')
    if source_commit and (REPO/'.git').exists():
        for path,expected in manifest['preserved_trees'].items():
            result=run(['git','rev-parse',source_commit+':'+path],REPO)
            require(result.returncode==0 and result.stdout.strip()==expected,'Preserved tree mismatch: '+path)
            preserved[path]=expected
        result=run(['git','diff','--name-only',manifest['review_commit'],source_commit,'--','papers/GTF-I-v1','papers/GTF-I-v2','papers/GTF-I-v3','reviews'],REPO)
        require(result.returncode==0 and not result.stdout.strip(),'A prior edition or report changed')
    outputs=[]
    for flags,name in [([], 'DIAGNOSTICS.json'),(['-O'],'DIAGNOSTICS_OPTIMIZED.json')]:
        result=run([sys.executable,*flags,str(ROOT/'verify.py')],ROOT)
        (evidence/name).write_text(result.stdout)
        require(result.returncode==0,'Diagnostics failed: '+name);outputs.append(result.stdout)
    require(outputs[0]==outputs[1],'Optimized diagnostics differ')
    mutants={}
    for mutant in ['uncharged-age','erase-critical-log','omit-noise-floor','regularize-collision']:
        exits=[]
        for flags in [[],['-O']]:
            result=run([sys.executable,*flags,str(ROOT/'verify.py'),'--mutant',mutant],ROOT)
            require(result.returncode!=0,'Mutant accepted: '+mutant)
            exits.append(result.returncode)
            (evidence/('MUTANT_'+mutant+('_OPT' if flags else '')+'.txt')).write_text(result.stdout)
        mutants[mutant]={'rejected':True,'exit_codes':exits}
    inherited_diagnostics={}
    for name,script in [('V3','papers/GTF-I-v3/verify.py'),('V2','papers/GTF-I-v2/verify.py'),('V1','papers/GTF-I-v2/legacy/tools/verify.py')]:
        result=run([sys.executable,str(REPO/script)],(REPO/script).parent)
        (evidence/(name+'_DIAGNOSTICS.json')).write_text(result.stdout)
        require(result.returncode==0,'Inherited diagnostic failed: '+name)
        inherited_diagnostics[name]={'passed':True,'output_sha256':sha(evidence/(name+'_DIAGNOSTICS.json'))}
    # Old sources remain physically unchanged; all mathematical labels must also resolve in this edition.
    old_paths=['papers/GTF-I-v3/regenerative.tex','papers/GTF-I-v3/calibration.tex','papers/GTF-I-v3/retained-results.tex']
    old_paths+=sorted(p for p in manifest['input_sha256'] if '/legacy/sections/' in p and not p.endswith('01_introduction.tex'))
    old_body='\n'.join((REPO/p).read_text() for p in old_paths)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',old_body))
    new_body='\n'.join((ROOT/p).read_text() for p in ['introduction.tex','posterior-orbits.tex','expanding-noisy.tex','collision-moments.tex'])
    all_body=old_body+'\n'+new_body
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790035200',FORCE_SOURCE_DATE='1')
    with tempfile.TemporaryDirectory(prefix='gtf-v4-') as tmp:
        base=Path(tmp)
        for path in manifest['input_sha256']:
            dest=base/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(REPO/path,dest)
        work=base/'papers/GTF-I-v4';previous=None
        for passes in range(1,7):
            result=run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','main.tex'],work,env)
            (evidence/f'LATEX_PASS_{passes}.txt').write_text(result.stdout)
            require(result.returncode==0,'LaTeX failed on pass '+str(passes))
            state=tuple(sha(work/f'main.{ext}') for ext in ['aux','toc','out'])
            if passes>=2 and state==previous:break
            previous=state
        else:raise SystemExit('References did not stabilize')
        log=(work/'main.log').read_text(errors='replace');aux=(work/'main.aux').read_text()
        for fault in ['undefined references','undefined citations','multiply defined','Overfull \\hbox','Overfull \\vbox']:
            require(fault not in log,'LaTeX fault: '+fault)
        missing=sorted(x for x in oldlabels if '\\newlabel{'+x+'}' not in aux)
        require(not missing,'Missing preserved labels: '+repr(missing))
        for ext,dest in [('pdf',ROOT/'paper.pdf'),('aux',evidence/'LABELS.aux'),('log',evidence/'LATEX_FINAL.log'),('fls',evidence/'TEX_RECORDER.fls')]:shutil.copy2(work/f'main.{ext}',dest)
        info=run(['pdfinfo',str(work/'main.pdf')],work)
        pages=int(re.search(r'^Pages:\s+(\d+)',info.stdout,re.M).group(1))
        (evidence/'PDFINFO.txt').write_text(info.stdout)
    archive_paths=sorted(set(manifest['input_sha256'])|{'papers/GTF-I-v4/SOURCE_MANIFEST.json'})
    with zipfile.ZipFile(evidence/'COMPILED_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name in archive_paths:
            item=zipfile.ZipInfo(name,(2026,9,22,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(item,(REPO/name).read_bytes())
    counts={kind:len(re.findall(r'\\begin\{'+kind+r'\}',all_body)) for kind in ['theorem','lemma','proposition','corollary','proof','example']}
    label_map={m.group(1):{'number':m.group(2),'page':int(m.group(3))} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{(\d+)\}',aux) if m.group(1).startswith(('thm:v4','lem:v4','cor:v4','prop:v4','ex:v4'))}
    receipt={'status':'passed','source_commit':source_commit,'run_id':os.environ.get('GITHUB_RUN_ID'),'review_commit':manifest['review_commit'],'pdf_sha256':sha(ROOT/'paper.pdf'),'pdf_pages':pages,'compiler_passes':passes,'compiled_statement_counts':counts,'retained_mathematical_labels':len(oldlabels),'all_retained_labels_resolve':True,'v2_quantitative_body_byte_identical':True,'preserved_git_trees':preserved,'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),'compiled_source_archive_sha256':sha(evidence/'COMPILED_SOURCES.zip'),'compiled_source_archive_files':len(archive_paths),'undefined_references':False,'overfull_boxes':False,'ordinary_optimized_identical':True,'diagnostics':json.loads(outputs[0]),'negative_controls':mutants,'inherited_diagnostics':inherited_diagnostics,'new_mathematical_locations':label_map,'scope':'Executed reproducibility and finite regression evidence, not a formal proof certificate or independent referee approval.'}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'pages':pages,'passes':passes,'counts':counts,'retained_labels':len(oldlabels),'locations':label_map},indent=2))
if __name__=='__main__':main()
