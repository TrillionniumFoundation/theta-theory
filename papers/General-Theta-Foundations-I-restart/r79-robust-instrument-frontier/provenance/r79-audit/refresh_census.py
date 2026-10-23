#!/usr/bin/env python3
"""Refresh the all-ref scoped census from independently authenticated old archives.
Read-only: no fetching, checkout, extraction or remote mutation. Scope is source
retrieval, byte identity and lexical indexing, not theorem reproof or refereeing.
"""
import argparse,collections,datetime,gzip,hashlib,json,os,pathlib,re,subprocess,sys
P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--repo',type=pathlib.Path,required=True)
P.add_argument('--source-root',type=pathlib.Path,required=True)
P.add_argument('--refs',type=pathlib.Path,required=True)
P.add_argument('--archive-receipt',type=pathlib.Path,required=True)
P.add_argument('--out',type=pathlib.Path,required=True)
ARGS=P.parse_args();HERE=ARGS.out;HERE.mkdir(parents=True,exist_ok=True);REPO=ARGS.repo;SOURCE=ARGS.source_root
SCOPE=re.compile(r'general[ _-]*theta|theta[ _-]*general|gtf[ _-]*i(?:[ _./-]|$)',re.I)
TEXT={'.tex','.bib','.md','.txt','.json','.csv','.tsv','.yml','.yaml','.py','.sh','.log','.sty','.cls','.toml','.html','.xml','.rst','.cfg','.ini','.aux','.bbl','.out'}
ISSUE=re.compile(r'\b(open|unproved|unresolved|gap|missing|incomplete|not proved|not established|conditional|priority|novelty|reject|A1|A2|pipeline|reset|rank constraint|no.message)\b',re.I)
def scoped(path):return bool(SCOPE.search(path) or (len(path.split('/'))<=3 and not path.startswith(('papers/','reviews/','revision/','tools/')) and re.search(r'audit|pipeline|ledger|referee|review|response|progress|governance|status|dependency',path,re.I)))
def write(path,obj):
 raw=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n'
 if path.suffix=='.gz':
  with gzip.GzipFile(filename=str(path),mode='wb',mtime=0) as f:f.write(raw)
 else:path.write_bytes(raw)
def require(value,msg):
 if not value:raise RuntimeError(msg)
def gh(raw):return hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()
started=datetime.datetime.now(datetime.timezone.utc).isoformat();snap=json.loads(ARGS.refs.read_text());heads=sorted({r['sha'] for r in snap['all']});versions=collections.defaultdict(list);commits={};selected={};paths=set();cur=None
proc=subprocess.Popen(['git','-C',str(REPO),'log','--raw','--no-abbrev','--no-renames','--full-history','--root','-m','--format=COMMIT%x09%H%x09%cI%x09%s',*heads,'--'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'})
for line in proc.stdout:
 if line.startswith(b'COMMIT\t'):
  f=line.decode().rstrip('\n').split('\t',3);cur={'sha':f[1],'date':f[2],'subject':f[3]};commits[cur['sha']]=cur
 elif line.startswith(b':'):
  meta,sep,pr=line.rstrip(b'\n').partition(b'\t')
  if not sep:continue
  path=pr.decode('utf-8','replace')
  if not scoped(path):continue
  selected[cur['sha']]=cur;paths.add(path);f=meta.decode().split();sha=f[3]
  if sha=='0'*40 or pathlib.Path(path).suffix.lower() not in TEXT:continue
  rec={'commit':cur['sha'],'path':path,'status':f[4]}
  if rec not in versions[sha]:versions[sha].append(rec)
err=proc.stderr.read();require(proc.wait()==0,err.decode());write(HERE/'HISTORICAL_BLOB_VERSIONS.json.gz',versions)
old={r['git_blob']:r for r in json.loads(gzip.decompress((SOURCE/'provenance/r78-audit/current-census/HISTORICAL_TEXT_INDEX.json.gz').read_bytes()))};hist_receipt=json.loads(ARGS.archive_receipt.read_text());require(hist_receipt['status']=='PASS' and hist_receipt['total_unique_text_blobs']==len(old),'Archive authentication missing');require(set(old)<=set(versions),'Unexpected removed history')
local={}
source_auth=[]
for row in subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r','-z','e0377beea364e456af2301f5e4fec98fe343cbcb:papers/General-Theta-Foundations-I-restart/r78-reset-memory-frontier']).split(b'\0'):
 if not row:continue
 meta,name=row.split(b'\t',1);mode,kind,sha=meta.decode().split();rel=name.decode();path=SOURCE/rel;raw=path.read_bytes();require(kind=='blob' and gh(raw)==sha,'Source blob differs '+rel);local[sha]=path;source_auth.append({'path':rel,'git_blob':sha,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'mode':mode})
write(HERE/'R78_SOURCE_AUTHENTICATION.json',{'commit':'e0377beea364e456af2301f5e4fec98fe343cbcb','tree':'072a5a8c7b251964c0f5ba8c1c109d88a93302ee','files':source_auth,'count':len(source_auth)})
newidx=[];issues={};report_candidates=[]
for sha in sorted(set(versions)-set(old)):
 require(sha in local,'New scoped blob not present in full R78 source: '+sha);raw=local[sha].read_bytes();require(gh(raw)==sha,'New blob mismatch');body=raw.decode();cats=[]
 for v in versions[sha]:
  path=v['path'].lower();name=pathlib.Path(path).name
  if pathlib.Path(path).suffix in {'.tex','.bib'}:cats.append('native_mathematical_source')
  if re.search(r'proof|theorem|dependenc|ledger',path):cats.append('proof_ledger_or_map')
  if re.search(r'audit|pipeline',path):cats.append('internal_or_pipeline_audit')
  if re.search(r'response|rebuttal',path):cats.append('author_response')
  if re.search(r'verif|diagnostic|receipt|build|test|validation',path):cats.append('finite_or_build_verification')
  if re.search(r'referee.*report|report.*referee|external.*review|review.*report',path) and not re.search(r'^response|^author.response|^rebuttal|manifest|receipt',name):cats.append('report_candidate')
 idx={'git_blob':sha,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(body.splitlines()),'encoding':'utf-8','categories':sorted(set(cats)),'retrieval':'authenticated R78 source file','representative_path':str(local[sha].relative_to(SOURCE))};newidx.append(idx)
 hits=[{'line':i,'text':s[:1200]} for i,s in enumerate(body.splitlines(),1) if ISSUE.search(s)]
 if hits:issues[sha]=hits
 if 'report_candidate' in cats:report_candidates.append({**idx,'versions':versions[sha]})
write(HERE/'NEW_TEXT_INDEX.json.gz',newidx);write(HERE/'NEW_ISSUE_LINES.json.gz',issues);write(HERE/'NEW_REPORT_CANDIDATES.json',report_candidates)
write(HERE/'CURRENT_HISTORICAL_TEXT_INDEX.json.gz',list(old.values())+newidx)
receipt={'command':[sys.executable,*sys.argv],'verifier_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'refs_sha256':hashlib.sha256(ARGS.refs.read_bytes()).hexdigest(),'archive_receipt_sha256':hashlib.sha256(ARGS.archive_receipt.read_bytes()).hexdigest(),'schema':'theta.r79.current-source-census.v1','started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','remote_heads':len(snap['all']),'distinct_head_commits':len(heads),'ancestor_commits':len(commits),'scoped_changing_commits':len(selected),'scoped_versioned_paths':len(paths),'historical_archive_blobs_read_authenticated_decoded':len(old),'new_text_blobs_read_authenticated_decoded':len(newidx),'total_text_blobs_read_authenticated_decoded':len(versions),'total_text_bytes':sum(x['bytes'] for x in old.values())+sum(x['bytes'] for x in newidx),'r78_source_files_authenticated':len(source_auth),'new_report_candidates':len(report_candidates),'scope':'All snapshotted remote branch heads and ancestors; General Theta/GTF-I text and shared shallow governance/audits. Complete historical archives streamed and decoded; all new text read from authenticated R78 source. Not mathematical reproof, human refereeing, independent endorsement, hosted CI or editorial decision.'}
write(HERE/'CURRENT_CENSUS_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
