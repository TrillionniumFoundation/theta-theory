#!/usr/bin/env python3
"""Hash-bound canonical article and preserved-development build (stdlib only)."""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
PREFIX=ROOT.relative_to(REPO).as_posix()
from verify import MUTANTS

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p:Path)->str:
    d=p.read_bytes();return hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()
def require(ok:bool,message:str)->None:
    if not ok:raise SystemExit(message)
def run(args:list[str],cwd:Path,env=None):
    return subprocess.run(args,cwd=cwd,env=env,text=True,encoding='utf-8',errors='replace',
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
def labelmap(aux:str)->dict:
    return {m.group(1):{'number':m.group(2),'page':int(m.group(3))}
            for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{(\d+)\}',aux)}
def texpaths(job:str)->list[Path]:
    seen=set();ordered=[]
    def visit(p):
        p=p.resolve();require(p.is_relative_to(REPO),'TeX path escapes source root')
        if p in seen:return
        seen.add(p);require(p.is_file(),'Missing TeX input '+str(p));ordered.append(p)
        for name in re.findall(r'\\input\{([^}]+)\}',p.read_text()):
            visit(ROOT/(name if name.endswith('.tex') else name+'.tex'))
    visit(ROOT/(job+'.tex'));return ordered

def main()->None:
    for exe in ['pdflatex','pdfinfo']:
        require(shutil.which(exe) is not None,'Missing '+exe)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ev=ROOT/'evidence';ev.mkdir(exist_ok=True)
    for name,digest in manifest['input_sha256'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe manifest path')
        require((REPO/name).is_file() and sha(REPO/name)==digest,'Input changed: '+name)
    previous=REPO/'papers/GTF-I-v6-markov/SOURCE_MANIFEST.json'
    inherited=json.loads(previous.read_text())
    for name,digest in inherited['input_sha256'].items():
        require(sha(REPO/name)==digest,'Inherited v6 input changed: '+name)
    history=json.loads((ROOT/'HISTORY_INPUT_MANIFEST.json').read_text())
    for record in history['active_a2_mathematics']['files'].values():
        p=REPO/record['repository_copy']
        require(sha(p)==record['sha256'] and blob(p)==record['git_blob'],'A2 consultation source changed')
    fullrefs=(REPO/'papers/GTF-I-v6-markov/references.tex').read_text().replace(
        '\\end{thebibliography}',(ROOT/'new-references.tex').read_text()+'\n\\end{thebibliography}')
    require((ROOT/'references.tex').read_text()==fullrefs,'Inherited bibliography entries changed')
    corefiles=[p for p in texpaths('main') if p.parent==ROOT and p.name not in
               {'main.tex','frontmatter.tex','core.tex','references-main.tex'}]
    core='\n'.join(p.read_text() for p in corefiles)
    citekeys={k for m in re.finditer(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',core)
              for k in m.group(1).split(',')}
    items=re.findall(r'(\\bibitem\{([^}]+)\}.*?)(?=\\bibitem|\\end\{thebibliography\})',fullrefs,re.S)
    expected='\\begin{thebibliography}{99}\n'+''.join(s for s,k in items if k in citekeys)+'\\end{thebibliography}\n'
    require((ROOT/'references-main.tex').read_text()==expected,'Main bibliography is not exact cited subset')
    allfiles=texpaths('development')
    for p in allfiles+texpaths('main'):
        require(p.relative_to(REPO).as_posix() in manifest['input_sha256'],'Unmanifested TeX '+str(p))
    oldbody='\n'.join(p.read_text() for p in allfiles if p.parent!=ROOT and p.name!='preamble.tex')
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldbody))
    corelabels=set(re.findall(r'\\label\{([^}]+)\}',core))
    source=os.environ.get('GTF_SOURCE_SHA') or os.environ.get('GITHUB_SHA')
    preserved={};changed=[];git_checked=False
    if source and (REPO/'.git').exists():
        require(run(['git','rev-parse','HEAD'],REPO).stdout.strip()==source,'Source is not current HEAD')
        report=run(['git','rev-parse',source+':'+manifest['review_report_path']],REPO)
        require(report.returncode==0 and report.stdout.strip()==manifest['review_report_blob'],'Review identity changed')
        for name,want in manifest['preserved_trees'].items():
            got=run(['git','rev-parse',source+':'+name],REPO)
            require(got.returncode==0 and got.stdout.strip()==want,'Preserved tree changed: '+name)
            preserved[name]=want
        diff=run(['git','diff','--name-status',manifest['review_commit'],source],REPO)
        require(diff.returncode==0,'Cannot inspect source changes')
        for line in diff.stdout.splitlines():
            status,name=line.split('\t',1)
            require(status=='A','Only new paths may change: '+line)
            require(name.startswith((PREFIX+'/', '.github/revision-inputs/gtf-i-v7-structural/')) or
                    name=='.github/workflows/general-theta-foundations-i-v7-structural.yml',
                    'Change outside new revision paths: '+name)
            changed.append(name)
        git_checked=True
    print('Input hashes and preservation checked',flush=True)
    normal=[]
    for flags,name in [([], 'DIAGNOSTICS.json'),(['-O'],'DIAGNOSTICS_OPTIMIZED.json')]:
        got=run([sys.executable,*flags,str(ROOT/'verify.py')],ROOT)
        (ev/name).write_text(got.stdout)
        require(got.returncode==0,'Diagnostics failed: '+name);normal.append(got.stdout)
    require(normal[0]==normal[1],'Normal/optimized diagnostics differ')
    mutants={}
    for mutant in MUTANTS:
        codes=[]
        for flags in [[],['-O']]:
            got=run([sys.executable,*flags,str(ROOT/'verify.py'),'--mutant',mutant],ROOT)
            (ev/('MUTANT_'+mutant+('_OPT' if flags else '')+'.txt')).write_text(got.stdout)
            require(got.returncode!=0 and 'FAILED:' in got.stdout,'Mutant not rejected: '+mutant)
            codes.append(got.returncode)
        mutants[mutant]={'rejected':True,'exit_codes':codes}
    print('New normal/optimized diagnostics and all negative controls passed',flush=True)
    legacy={}
    for name,path in [('V6','papers/GTF-I-v6-markov/verify.py'),('V5','papers/GTF-I-v5-intrinsic/verify.py'),
                      ('V4','papers/GTF-I-v4/verify.py'),('V3','papers/GTF-I-v3/verify.py'),
                      ('V2','papers/GTF-I-v2/verify.py'),('V1','papers/GTF-I-v2/legacy/tools/verify.py')]:
        got=run([sys.executable,str(REPO/path)],(REPO/path).parent)
        dest=ev/(name+'_DIAGNOSTICS.json');dest.write_text(got.stdout)
        require(got.returncode==0,'Inherited diagnostics failed: '+name)
        legacy[name]={'passed':True,'output_sha256':sha(dest)}
        print('Inherited '+name+' diagnostics passed',flush=True)
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790035200',FORCE_SOURCE_DATE='1')
    outputs={};maps={}
    with tempfile.TemporaryDirectory(prefix='gtf-v7-structural-') as tmp:
        base=Path(tmp)
        for p in manifest['input_sha256']:
            dest=base/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(REPO/p,dest)
            require(sha(dest)==manifest['input_sha256'][p],'Input changed during staging: '+p)
        work=base/PREFIX
        for job,filename in [('main','paper.pdf'),('development','complete-development.pdf')]:
            last=None
            for passes in range(1,7):
                got=run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',job+'.tex'],work,env)
                (ev/f'{job.upper()}_PASS_{passes}.txt').write_text(got.stdout)
                require(got.returncode==0,'TeX failed: '+job+' '+str(passes))
                state=tuple(sha(work/(job+'.'+ext)) for ext in ['aux','toc','out'])
                if passes>=2 and state==last:break
                last=state
            else:raise SystemExit('References did not stabilize: '+job)
            log=(work/(job+'.log')).read_text(errors='replace')
            for fault in ['undefined references','undefined citations','multiply defined','Overfull \\hbox','Overfull \\vbox']:
                require(fault not in log,'TeX fault '+job+': '+fault)
            lm=labelmap((work/(job+'.aux')).read_text());maps[job]=lm
            must=corelabels if job=='main' else corelabels|oldlabels
            require(must<=set(lm),'Missing labels '+job+': '+repr(sorted(must-set(lm))))
            for ext,dest in [('pdf',ROOT/filename),('aux',ev/(job.upper()+'_LABELS.aux')),
                             ('log',ev/(job.upper()+'_LATEX.log')),('fls',ev/(job.upper()+'_RECORDER.fls'))]:
                shutil.copy2(work/(job+'.'+ext),dest)
            info=run(['pdfinfo',str(work/(job+'.pdf'))],work)
            require(info.returncode==0,'Cannot read generated PDF')
            (ev/(job.upper()+'_PDFINFO.txt')).write_text(info.stdout)
            pages=int(re.search(r'^Pages:\s+(\d+)',info.stdout,re.M).group(1))
            body=core if job=='main' else core+'\n'+oldbody
            counts={k:len(re.findall(r'\\begin\{'+k+r'\}',body)) for k in
                    ['theorem','lemma','proposition','corollary','proof','example']}
            outputs[job]={'file':filename,'pages':pages,'sha256':sha(ROOT/filename),
                          'compiler_passes':passes,'statement_counts':counts,
                          'new_statement_locations':{k:v for k,v in lm.items() if k.startswith(
                              ('thm:v7','lem:v7','cor:v7','prop:v7','ex:v7'))}}
            print(job+' stable: '+str(pages)+' pages in '+str(passes)+' passes',flush=True)
    require(all(maps['main'][k]['number']==maps['development'][k]['number'] for k in corelabels),
            'Core numbering differs')
    for name,digest in manifest['input_sha256'].items():
        require(sha(REPO/name)==digest,'Input changed during build: '+name)
    archive_paths=sorted(set(manifest['input_sha256'])|{PREFIX+'/SOURCE_MANIFEST.json'})
    with zipfile.ZipFile(ev/'COMPILED_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name in archive_paths:
            z=zipfile.ZipInfo(name,(2026,9,22,0,0,0));z.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(z,(REPO/name).read_bytes())
    receipt={'status':'passed','edition':'GTF I seventh structural revision','source_commit':source,
        'git_head_and_only_new_paths_verified':git_checked,
        'review_commit':manifest['review_commit'],'review_report_blob':manifest['review_report_blob'],
        'run_id':os.environ.get('GITHUB_RUN_ID'),'outputs':outputs,
        'compiler':run(['pdflatex','--version'],ROOT).stdout.splitlines()[0],
        'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),
        'compiled_source_archive_sha256':sha(ev/'COMPILED_SOURCES.zip'),
        'compiled_source_archive_files':len(archive_paths),'preserved_git_trees':preserved,
        'source_changes':changed,'retained_mathematical_labels':len(oldlabels),'all_retained_labels_resolve':True,
        'core_labels':len(corelabels),'core_numbers_identical':True,'ordinary_optimized_identical':True,
        'finite_diagnostics':json.loads(normal[0]),'negative_controls':mutants,'inherited_diagnostics':legacy,
        'undefined_references':False,'overfull_boxes':False,
        'scope':'Build, preservation and finite diagnostics only; not a proof certificate, independent referee approval or priority determination.'}
    (ev/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'outputs':outputs,'retained_labels':len(oldlabels),'core_labels':len(corelabels),
                      'finite_checks':json.loads(normal[0])['finite_checks']},indent=2))
if __name__=='__main__':main()
