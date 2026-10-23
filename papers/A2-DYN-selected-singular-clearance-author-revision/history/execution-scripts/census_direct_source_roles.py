#!/usr/bin/env python3
"""Read only Git census: direct article/review trees, never recursive history expansion."""
import json, pathlib, subprocess, hashlib, datetime, re
ROOT=pathlib.Path('/workspace/scratch/917494ae78f7')
REPO=ROOT/'theta-theory'
OUT=ROOT/'revision-prep'
refs=json.loads((ROOT/'remote_refs_initial.json').read_text())
refs=[r for r in refs if 'a2-dyn' in r['ref'].lower()]
cache={}
calls=0
def git(*args):
    global calls
    calls+=1
    return subprocess.check_output(['git',*args],cwd=REPO)
def entries(sha):
    if sha not in cache:
        result=[]
        for row in git('ls-tree','-z',sha).split(b'\0'):
            if not row: continue
            left,name=row.split(b'\t',1);mode,typ,obj=left.decode().split()
            result.append({'name':name.decode(),'mode':mode,'type':typ,'sha':obj})
        cache[sha]=result
    return cache[sha]
def named(sha,name):
    return next((r for r in entries(sha) if r['name']==name),None)
commits={};paper_sets={};review_sets={};articles={};report_dirs={}
for sha in sorted({r['object']['sha'] for r in refs}):
    raw=git('cat-file','-p',sha).decode()
    headers,msg=raw.split('\n\n',1)
    lines=headers.splitlines()
    tree=next(x[5:] for x in lines if x.startswith('tree '))
    parents=[x[7:] for x in lines if x.startswith('parent ')]
    paper=named(tree,'papers');review=named(tree,'reviews')
    commits[sha]={'root_tree':tree,'parents':parents,'subject':msg.splitlines()[0] if msg else '', 'papers_tree':paper['sha'] if paper else None, 'reviews_tree':review['sha'] if review else None}
    if paper and paper['sha'] not in paper_sets:
        aset={r['name']:r['sha'] for r in entries(paper['sha']) if r['type']=='tree' and r['name'].startswith('A2-DYN')}
        paper_sets[paper['sha']]=aset
        for name,atree in aset.items():
            if atree in articles: continue
            es=entries(atree)
            selected={r['name']:{'type':r['type'],'sha':r['sha'],'mode':r['mode']} for r in es if r['name'] in ['main.tex','supplement.tex','core','model.tex','inputs.tex','RESPONSE_TO_REFEREE.md','SOURCE_MANIFEST.json','PROOF_LEDGER.md','PROOF_DEPENDENCY_LEDGER.md','PUBLICATION_STATUS.json','build.sh','tools','provenance','archive','history']}
            articles[atree]={'first_seen_path':'papers/'+name,'direct_entries':selected,'native_main_present':bool(next((r for r in es if r['name']=='main.tex' and r['type']=='blob'),None)),'scientific_completeness':'not inferred from direct entry presence; entry closure and actual build require separate verification'}
    if review and review['sha'] not in review_sets:
        rs={r['name']:r['sha'] for r in entries(review['sha']) if r['type']=='tree' and 'a2-dyn' in r['name'].lower()}
        review_sets[review['sha']]=rs
        for name,rtree in rs.items():
            if rtree in report_dirs:continue
            es=entries(rtree)
            report_dirs[rtree]={'first_seen_path':'reviews/'+name,'direct_reports':[{k:r[k] for k in ('name','sha','type')} for r in es if 'report' in r['name'].lower()]}
mapped=[]
for r in refs:
    ref=r['ref'];kind=ref.split('/')[2]
    mapped.append({'ref':ref,'sha':r['object']['sha'],'role_hint_from_ref':kind,'content_identity_lookup':'commits[sha]; paper_sets[papers_tree]; review_sets[reviews_tree]'})
result={'schema':'a2-dyn-direct-source-role-census-v1','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256':hashlib.sha256((ROOT/'remote_refs_initial.json').read_bytes()).hexdigest(),'scope':'All 435 A2-DYN refs from full GitHub-plugin response; commit/root/direct papers/direct article/direct reviews only; no recursive historical trees','counts':{'refs':len(refs),'commits':len(commits),'distinct_papers_trees':len(paper_sets),'distinct_direct_article_trees':len(articles),'distinct_review_trees':len(review_sets),'distinct_report_dirs':len(report_dirs),'git_commands':calls,'deduplicated_tree_objects':len(cache)},'refs':mapped,'commits':commits,'paper_sets':paper_sets,'article_trees':articles,'review_sets':review_sets,'report_directory_trees':report_dirs}
p=OUT/'all435-direct-source-role-census.json';p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'output':str(p),'counts':result['counts'],'bytes':p.stat().st_size},indent=2))
