#!/usr/bin/env python3
"""Classify immutable review-branch content, without equating names with reviews."""
import argparse,json,pathlib,re,subprocess,hashlib,datetime
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--refs',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args();REPO=args.repo;OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
snap=json.loads(args.refs.read_text())
refs=[r for r in snap['selected_refs'] if r['ref'].startswith('refs/heads/review/')]
def candidate(path):
    name=pathlib.Path(path).name.lower()
    return bool(re.search(r'general[ _-]*theta|theta[ _-]*general|gtf[ _-]*i',path,re.I) and re.search(r'referee.*report|report.*referee|external.*review|review.*report',name) and not re.search(r'^response|^author.response|^rebuttal|manifest|receipt|ready|input|package|audit|diagnostic|verification',name) and pathlib.Path(name).suffix in {'.md','.txt','.tex','.pdf'})
cache={};rows=[]
for r in refs:
    head=r['sha']
    if head not in cache:
        raw=subprocess.check_output(['git','-C',str(REPO),'diff-tree','--root','-r','--no-abbrev','--no-renames','--no-commit-id',head]).decode();changes=[]
        for line in raw.splitlines():
            if not line.startswith(':') or '\t' not in line:continue
            meta,path=line.split('\t',1);f=meta.split()
            if candidate(path) and f[4]!='D':changes.append({'path':path,'status':f[4],'old_blob':f[2],'new_blob':f[3]})
        full=subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r',head]).decode();visible=[]
        for line in full.splitlines():
            meta,path=line.split('\t',1);f=meta.split()
            if f[1]=='blob' and candidate(path) and not any('/'+p+'/' in '/'+path for p in ['retained','history','archive','source-editions']):visible.append({'path':path,'git_blob':f[2]})
        cache[head]={'report_candidate_head_changes':changes,'nonarchival_report_candidates_in_tree':visible}
    role='pipeline_audit_branch' if re.search(r'pipeline|proof.*audit',r['ref'],re.I) else 'review_candidate_branch'
    rows.append({'ref':r['ref'],'head':head,'branch_role_hint':role,**cache[head],'interpretation':'File and branch names identify candidates only. A head delta with no report may append a manifest to an existing report; it is not automatically an empty branch. Pipeline audits and copied reports are not fresh independent reviews.'})
(OUT/'REVIEW_DIFF_CLASSIFICATION.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'review_refs':len(refs),'unique_review_heads':len(cache),'heads_with_report_delta':sum(bool(x['report_candidate_head_changes']) for x in cache.values()),'pipeline_role_refs':sum(x['branch_role_hint']=='pipeline_audit_branch' for x in rows),'reported_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
