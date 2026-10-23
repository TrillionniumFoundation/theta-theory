#!/usr/bin/env python3
import argparse,collections,gzip,hashlib,json,pathlib,re,subprocess,datetime
P=argparse.ArgumentParser(description='Read-only tree-content catalog for each pinned branch head.')
P.add_argument('--repo',type=pathlib.Path,required=True);P.add_argument('--refs',type=pathlib.Path,required=True);P.add_argument('--out',type=pathlib.Path,required=True)
ARGS=P.parse_args();ROOT=ARGS.out;ROOT.mkdir(parents=True,exist_ok=True);REPO=ARGS.repo
snapshot=json.loads(ARGS.refs.read_text()); refs=snapshot['all']; heads=sorted({r['sha'] for r in refs})
SCOPE=re.compile(r'general[ _-]*theta|theta[ _-]*general|gtf[ _-]*i(?:[ _./-]|$)',re.I)
REPORT=re.compile(r'referee.*report|report.*referee|external.*review|review.*report',re.I)
records=[]
for i,sha in enumerate(heads):
 raw=subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r','-z',sha]); sources=[]; reports=collections.defaultdict(list); relevant_count=0
 for row in raw.split(b'\0'):
  if not row:continue
  meta,p=row.split(b'\t',1); mode,kind,blob=meta.decode().split(); path=p.decode('utf-8','replace')
  if kind!='blob' or not SCOPE.search(path):continue
  relevant_count+=1;name=pathlib.PurePosixPath(path).name
  if name in {'main.tex','manuscript.tex','paper.tex'}:sources.append({'path':path,'git_blob':blob})
  if REPORT.search(path) and name.lower().endswith(('.md','.txt','.tex')):reports[blob].append(path)
 # Actual changed paths at each head, independently of branch naming.
 changed=subprocess.check_output(['git','-C',str(REPO),'diff-tree','--root','--no-commit-id','-r','-m','--name-only',sha]).decode('utf-8','replace').splitlines()
 introduced=[p for p in changed if SCOPE.search(p) and REPORT.search(p) and p.lower().endswith(('.md','.txt','.tex'))]
 record={'head':sha,'refs':[r['ref'] for r in refs if r['sha']==sha],'relevant_blob_paths':relevant_count,'native_entrypoints':sources,'report_candidate_blobs':[{'git_blob':s,'path_count':len(v),'representative_path':v[0]} for s,v in sorted(reports.items())],'tip_changed_relevant_paths':len([p for p in changed if SCOPE.search(p)]),'tip_changed_report_candidate_paths':sorted(set(introduced)),'classification_limit':'Tree-content presence and raw commit delta only. A copied/unchanged report is not a new independent review; completeness/build and substantive scope require source reading.'}
 records.append(record)
 if i%100==0:print('cataloged',i,flush=True)
with gzip.GzipFile(filename=str(ROOT/'ALL_HEAD_CONTENT_CATALOG.json.gz'),mode='wb',mtime=0) as f:f.write(json.dumps(records,separators=(',',':')).encode())
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_refs':len(refs),'distinct_heads':len(heads),'heads_with_general_theta_content':sum(x['relevant_blob_paths']>0 for x in records),'refs_with_general_theta_content':sum(len(x['refs']) for x in records if x['relevant_blob_paths']),'scope':'Every current remote branch head; source entrypoint and report candidate content identities, with actual tip deltas; not a completeness or mathematical-validity assertion.'}
(ROOT/'HEAD_CONTENT_CATALOG_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
