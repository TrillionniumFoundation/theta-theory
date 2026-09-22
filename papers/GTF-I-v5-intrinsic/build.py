#!/usr/bin/env python3
"""Hash-bound build of the full and same-source principal fifth editions."""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
PREFIX=ROOT.relative_to(REPO).as_posix()
MUTANTS=['drop-survival-pressure','forget-suffix-states','replace-dependent-posterior',
         'erase-critical-log','ordinary-matrix-power']

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok:bool,message:str)->None:
    if not ok:raise SystemExit(message)
def run(args:list[str],cwd:Path,env=None):
    return subprocess.run(args,cwd=cwd,env=env,text=True,encoding="utf-8",errors="replace",stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,check=False)
def labels(aux:str)->dict:
    return {m.group(1):{'number':m.group(2),'page':int(m.group(3))}
            for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{(\d+)\}',aux)}
def main()->None:
    for exe in ['pdflatex','pdfinfo']:require(shutil.which(exe) is not None,'Missing '+exe)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ev=ROOT/'evidence';ev.mkdir(exist_ok=True)
    for path,digest in manifest['input_sha256'].items():
        require((REPO/path).is_file() and sha(REPO/path)==digest,'Input changed: '+path)
    inherited=json.loads((REPO/'papers/GTF-I-v4/SOURCE_MANIFEST.json').read_text())
    for path,digest in inherited['input_sha256'].items():
        require(sha(REPO/path)==digest,'Inherited v4 input changed: '+path)
    fullrefs=(REPO/'papers/GTF-I-v4/references.tex').read_text().replace(
        '\\end{thebibliography}',(ROOT/'new-references.tex').read_text()+'\n\\end{thebibliography}')
    require((ROOT/'references.tex').read_text()==fullrefs,'Full bibliography changed inherited entries')
    core_paths=[PREFIX+'/'+p for p in ['introduction.tex','intrinsic-model.tex',
        'cylinder-realization.tex','pressure-law.tex','dependent-acquisitions.tex']]
    core_paths+=['papers/GTF-I-v4/posterior-orbits.tex','papers/GTF-I-v4/expanding-noisy.tex']
    core='\n'.join((REPO/p).read_text() for p in core_paths)
    citekeys={k for m in re.finditer(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',core) for k in m.group(1).split(',')}
    items=re.findall(r'(\\bibitem\{([^}]+)\}.*?)(?=\\bibitem|\\end\{thebibliography\})',fullrefs,re.S)
    expected='\\begin{thebibliography}{99}\n'+''.join(s for s,k in items if k in citekeys)+'\\end{thebibliography}\n'
    require((ROOT/'references-principal.tex').read_text()==expected,'Principal bibliography is not exact cited subset')
    old_paths=['papers/GTF-I-v4/posterior-orbits.tex','papers/GTF-I-v4/expanding-noisy.tex',
        'papers/GTF-I-v4/collision-moments.tex','papers/GTF-I-v3/regenerative.tex',
        'papers/GTF-I-v3/calibration.tex','papers/GTF-I-v3/retained-results.tex']
    old_paths+=sorted(p for p in inherited['input_sha256'] if '/legacy/sections/' in p
                      and not p.endswith('01_introduction.tex'))
    oldbody='\n'.join((REPO/p).read_text() for p in old_paths)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldbody))
    corelabels=set(re.findall(r'\\label\{([^}]+)\}',core))
    ownbody='\n'.join((REPO/p).read_text() for p in core_paths if p.startswith(PREFIX+'/'))
    completebody=ownbody+'\n'+oldbody
    source=os.environ.get('GTF_SOURCE_SHA') or os.environ.get('GITHUB_SHA')
    preserved={};changed=[]
    if source and (REPO/'.git').exists():
        head=run(['git','rev-parse','HEAD'],REPO)
        require(head.returncode==0 and head.stdout.strip()==source,'Build source is not checked-out HEAD')
        report=run(['git','rev-parse',source+':'+manifest['review_report_path']],REPO)
        require(report.returncode==0 and report.stdout.strip()==manifest['review_report_blob'],'Controlling review changed')
        for path,expected in manifest['preserved_trees'].items():
            got=run(['git','rev-parse',source+':'+path],REPO)
            require(got.returncode==0 and got.stdout.strip()==expected,'Preserved tree changed: '+path)
            preserved[path]=expected
        diff=run(['git','diff','--name-only',manifest['review_commit'],source],REPO)
        require(diff.returncode==0,'Cannot inspect source diff')
        changed=diff.stdout.splitlines()
        allowed=[PREFIX+'/', '.github/revision-inputs/gtf-i-v5-intrinsic/',
                 '.github/workflows/general-theta-foundations-i-v5-intrinsic.yml',
                 'GTF_I_V5_INTRINSIC_INDEX.md']
        require(all(any(p.startswith(a) for a in allowed) for p in changed),'Change outside new revision paths')
    normal=[]
    for flags,name in [([], 'DIAGNOSTICS.json'),(['-O'],'DIAGNOSTICS_OPTIMIZED.json')]:
        got=run([sys.executable,*flags,str(ROOT/'verify.py')],ROOT)
        (ev/name).write_text(got.stdout)
        require(got.returncode==0,'Diagnostics failed: '+name);normal.append(got.stdout)
    require(normal[0]==normal[1],'Ordinary and optimized outputs differ')
    mutants={}
    for mutant in MUTANTS:
        statuses=[]
        for flags in [[],['-O']]:
            got=run([sys.executable,*flags,str(ROOT/'verify.py'),'--mutant',mutant],ROOT)
            (ev/('MUTANT_'+mutant+('_OPT' if flags else '')+'.txt')).write_text(got.stdout)
            require(got.returncode!=0 and 'FAILED:' in got.stdout,'Negative control not rejected: '+mutant)
            statuses.append(got.returncode)
        mutants[mutant]={'rejected':True,'exit_codes':statuses}
    legacy={}
    for name,path in [('V4','papers/GTF-I-v4/verify.py'),('V3','papers/GTF-I-v3/verify.py'),
                      ('V2','papers/GTF-I-v2/verify.py'),('V1','papers/GTF-I-v2/legacy/tools/verify.py')]:
        got=run([sys.executable,str(REPO/path)],(REPO/path).parent)
        (ev/(name+'_DIAGNOSTICS.json')).write_text(got.stdout)
        require(got.returncode==0,'Inherited diagnostics failed: '+name)
        legacy[name]={'passed':True,'output_sha256':sha(ev/(name+'_DIAGNOSTICS.json'))}
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790035200',FORCE_SOURCE_DATE='1')
    outputs={};maps={}
    with tempfile.TemporaryDirectory(prefix='gtf-v5-intrinsic-') as tmp:
        base=Path(tmp)
        for p in manifest['input_sha256']:
            dest=base/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(REPO/p,dest)
        work=base/PREFIX
        for job,filename in [('main','paper.pdf'),('principal','principal-paper.pdf')]:
            last=None
            for passes in range(1,7):
                got=run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                         '-recorder',job+'.tex'],work,env)
                (ev/f'{job.upper()}_PASS_{passes}.txt').write_text(got.stdout)
                require(got.returncode==0,'LaTeX failed: '+job+' pass '+str(passes))
                state=tuple(sha(work/(job+'.'+ext)) for ext in ['aux','toc','out'])
                if passes>=2 and state==last:break
                last=state
            else:raise SystemExit('References did not stabilize: '+job)
            log=(work/(job+'.log')).read_text(errors='replace')
            for fault in ['undefined references','undefined citations','multiply defined','Overfull \\hbox','Overfull \\vbox']:
                require(fault not in log,'LaTeX fault in '+job+': '+fault)
            lm=labels((work/(job+'.aux')).read_text());maps[job]=lm
            must=oldlabels|corelabels if job=='main' else corelabels
            require(must<=set(lm),'Missing labels in '+job+': '+repr(sorted(must-set(lm))))
            for ext,dest in [('pdf',ROOT/filename),('aux',ev/(job.upper()+'_LABELS.aux')),
                             ('log',ev/(job.upper()+'_LATEX.log')),('fls',ev/(job.upper()+'_RECORDER.fls'))]:
                shutil.copy2(work/(job+'.'+ext),dest)
            info=run(['pdfinfo',str(work/(job+'.pdf'))],work)
            (ev/(job.upper()+'_PDFINFO.txt')).write_text(info.stdout)
            pages=int(re.search(r'^Pages:\s+(\d+)',info.stdout,re.M).group(1))
            body=completebody if job=='main' else core
            counts={k:len(re.findall(r'\\begin\{'+k+r'\}',body)) for k in ['theorem','lemma','proposition','corollary','proof','example']}
            outputs[job]={'file':filename,'pages':pages,'sha256':sha(ROOT/filename),
                          'compiler_passes':passes,'statement_counts':counts,
                          'new_statement_locations':{k:v for k,v in lm.items() if k.startswith(('thm:v5','lem:v5','cor:v5','prop:v5','ex:v5'))}}
    require(all(maps['main'][k]['number']==maps['principal'][k]['number'] for k in corelabels),'Core numbering differs between editions')
    archive_paths=sorted(set(manifest['input_sha256'])|{PREFIX+'/SOURCE_MANIFEST.json'})
    with zipfile.ZipFile(ev/'COMPILED_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name in archive_paths:
            z=zipfile.ZipInfo(name,(2026,9,22,0,0,0));z.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(z,(REPO/name).read_bytes())
    version=run(['pdflatex','--version'],ROOT).stdout.splitlines()[0]
    receipt={'status':'passed','edition':'GTF I fifth intrinsic revision','source_commit':source,
        'review_commit':manifest['review_commit'],'review_report_blob':manifest['review_report_blob'],
        'run_id':os.environ.get('GITHUB_RUN_ID'),'outputs':outputs,'compiler':version,
        'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),
        'compiled_source_archive_sha256':sha(ev/'COMPILED_SOURCES.zip'),
        'compiled_source_archive_files':len(archive_paths),'preserved_git_trees':preserved,
        'source_changes':changed,'retained_mathematical_labels':len(oldlabels),
        'all_retained_labels_resolve':True,'core_labels':len(corelabels),'core_numbers_identical':True,
        'ordinary_optimized_identical':True,'finite_diagnostics':json.loads(normal[0]),
        'negative_controls':mutants,'inherited_diagnostics':legacy,'undefined_references':False,
        'overfull_boxes':False,'scope':'Build, preservation and finite regression evidence; not a formal proof certificate, priority determination or independent refereeing.'}
    (ev/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'outputs':outputs,'retained_labels':len(oldlabels),'core_labels':len(corelabels),
                      'finite_checks':json.loads(normal[0])['finite_checks']},indent=2))
if __name__=='__main__':main()
