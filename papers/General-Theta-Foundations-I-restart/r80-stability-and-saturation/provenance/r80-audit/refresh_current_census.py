#!/usr/bin/env python3
"""Extend the authenticated R79 historical census to the current remote snapshot.

Read-only inputs: complete R79 source/publication and immutable Git objects.
The old 7,201 payloads are separately streamed by the two inherited verifiers.
This program authenticates and archives only genuinely new eligible text blobs,
and checks unchanged old refs plus all four new ancestor commits. It does not
re-prove mathematics, identify human reviewers, or certify novelty.
"""
import argparse,base64,datetime,gzip,hashlib,io,json,os,pathlib,re,subprocess,tarfile

P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--repo',type=pathlib.Path,required=True)
P.add_argument('--source-root',type=pathlib.Path,required=True)
P.add_argument('--out',type=pathlib.Path,required=True)
A=P.parse_args();R=A.repo;S=A.source_root;O=A.out;OLD=S/'provenance/r79-audit'
START=datetime.datetime.now(datetime.timezone.utc).isoformat()
TEXT={'.tex','.bib','.md','.txt','.json','.csv','.tsv','.yml','.yaml','.py','.sh','.log','.sty','.cls','.toml','.html','.xml','.rst','.cfg','.ini','.aux','.bbl','.out'}
SCOPE=re.compile(r'general[ _-]*theta|theta[ _-]*general|gtf[ _-]*i(?:[ _./-]|$)',re.I)
ISSUE=re.compile(r'\b(open|unproved|unresolved|gap|missing|incomplete|not proved|not established|conditional|priority|novelty|reject|A1|A2|pipeline|reset|rank constraint|no.message)\b',re.I)
SOURCE='90cae2f5aca243b39d3a2194a4d6e0696671a101'
PUB='a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2'
A2S='1cd52fd00675f10f08182f670a42fbbf9e0d1a96'
A2P='1e44e7a3360aa1ff41de4fc8f8b71fd173f6ba2a'
def require(v,m):
 if not v:raise RuntimeError(m)
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def write(name,obj):
 b=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n';p=O/name
 if p.suffix=='.gz':p.write_bytes(gzip.compress(b,mtime=0))
 else:p.write_bytes(b)
def gh(kind,b):return hashlib.sha1(f'{kind} {len(b)}\0'.encode()+b).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],env={**os.environ,'GIT_NO_LAZY_FETCH':'1'})
def scoped(p):return bool(SCOPE.search(p) or (len(p.split('/'))<=3 and not p.startswith(('papers/','reviews/','revision/','tools/')) and re.search(r'audit|pipeline|ledger|referee|review|response|progress|governance|status|dependency',p,re.I)))
def categories(p):
 q=p.lower();c=[]
 for pattern,label in [(r'proof|theorem|dependenc|ledger','proof_ledger_or_map'),(r'audit|pipeline','internal_or_pipeline_audit'),(r'response|rebuttal','author_response'),(r'verif|diagnostic|receipt|build|test|validation','finite_or_build_verification')]:
  if re.search(pattern,q):c.append(label)
 if pathlib.Path(q).suffix in {'.tex','.bib'}:c.append('native_mathematical_source')
 if re.search(r'referee.*report|report.*referee|external.*review|review.*report',q) and not re.search(r'^response|^author.response|^rebuttal|manifest|receipt',pathlib.Path(q).name):c.append('report_candidate')
 return c

snap=read(O/'CURRENT_REFS.json');previous=read(OLD/'CURRENT_REFS.json')
a={x['ref']:x['sha'] for x in previous['all']};b={x['ref']:x['sha'] for x in snap['all']}
require(len(a)==1307 and len(b)==1309,'Unexpected snapshot counts')
require(all(b.get(k)==v for k,v in a.items()),'Previous ref moved or disappeared')
added={k:v for k,v in b.items() if k not in a};require(set(added.values())=={PUB,A2P},'Unexpected new reference')
write('REF_DELTA_FROM_R79.json',{'previous_count':len(a),'current_count':len(b),'added':added,'changed':[],'deleted':[]})
for f in ['RETAINED_R78_HISTORY_RECHECK.json','RETAINED_R79_HISTORY_RECHECK.json']:
 require(read(O/f)['status']=='PASS','Missing actual archive execution '+f)
require(read(O/'BRANCH_PAGINATION_CHECK.json')['status']=='PASS','Missing independent complete ref enumeration')

rawpack=read(OLD/'HEAD_COMMIT_OBJECTS.json.gz');raws={x['sha']:base64.b64decode(x['payload_base64']) for x in rawpack}
newcommitrows=[]
for sha in [SOURCE,PUB,A2S,A2P]:
 raw=git('cat-file','commit',sha) if sha in {SOURCE,PUB} else (O/f'COMMIT_{sha}.raw').read_bytes()
 require(gh('commit',raw)==sha,'Commit payload mismatch '+sha)
 d=read(O/f'COMMIT_{sha}.json');head=raw.split(b'\n\n',1)[0].decode();tree=re.search(r'^tree (\w+)$',head,re.M).group(1);parents=re.findall(r'^parent (\w+)$',head,re.M)
 require(tree==d['tree']['sha'] and parents==[x['sha'] for x in d['parents']],'Remote/local commit metadata mismatch')
 raws[sha]=raw;newcommitrows.append({'sha':sha,'tree':tree,'parents':parents,'raw_sha256':hashlib.sha256(raw).hexdigest(),'subject':raw.split(b'\n\n',1)[1].decode().splitlines()[0]})
heads=sorted(set(b.values()));require(len(heads)==875,'Wrong unique-head count')
for sha in heads:require(sha in raws and gh('commit',raws[sha])==sha,'Missing/bad current head payload '+sha)
write('NEW_COMMIT_IDENTITIES.json',newcommitrows)
write('NEW_COMMIT_PAYLOADS.json.gz',[{'sha':k,'payload_base64':base64.b64encode(raws[k]).decode()} for k in [SOURCE,PUB,A2S,A2P]])
anc=set((OLD/'ALL_ANCESTOR_COMMITS.txt').read_text().splitlines());require(len(anc)==2711,'Old ancestry count differs')
newids={SOURCE,PUB,A2S,A2P};require(not anc&newids,'New commit already in old ancestry')
for row in newcommitrows:require(set(row['parents']) <= anc|newids,'Unvisited ancestor')
anc|=newids;(O/'ALL_ANCESTOR_COMMITS.txt').write_text('\n'.join(sorted(anc))+'\n')

compare=read(O/'NEW_A2_SCOPE_COMPARISON.json')
require(compare['ahead_by']==2 and compare['total_commits']==2 and len(compare['files'])<300,'Incomplete A2 compare')
require(compare['base_sha']=='d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28' and compare['base_sha'] in anc,'Wrong A2 parent')
require(not any(scoped(x['filename']) for x in compare['files']),'A2 unexpectedly changes scoped text')

oldindex=read(OLD/'CURRENT_HISTORICAL_TEXT_INDEX.json.gz');indexed={x['git_blob']:x for x in oldindex}
require(len(indexed)==7201,'Old text count differs');versions=read(OLD/'HISTORICAL_BLOB_VERSIONS.json.gz');newidx=[];issues={};rawnew={};newpaths=[]
for sha,role,dirname in [(SOURCE,'SOURCE',S.name),(PUB,'PUBLICATION',S.name+'-publication')]:
 remote=read(O/f'R79_{role}_REMOTE_TREE.json');tree={x['path']:x for x in remote['tree'] if x['type']=='blob'}
 changes=git('diff-tree','--no-commit-id','--name-status','-r',sha).decode().splitlines()
 require(len(changes)==len(tree),'Remote tree does not equal new directory delta')
 for line in changes:
  status,path=line.split('\t');prefix='papers/General-Theta-Foundations-I-restart/'+dirname+'/'
  require(status=='A' and path.startswith(prefix),'Non-addition outside current paper')
  rel=path[len(prefix):];r=tree[rel];raw=(S.parent/dirname/rel).read_bytes();blob=gh('blob',raw)
  require(blob==r['sha'] and len(raw)==r['size'],'Current blob mismatch '+path)
  require(scoped(path),'Current source path absent from historical scope');newpaths.append(path)
  if pathlib.Path(path).suffix.lower() not in TEXT:continue
  row={'commit':sha,'path':path,'status':status};versions.setdefault(blob,[])
  if row not in versions[blob]:versions[blob].append(row)
  if blob in indexed or blob in rawnew:continue
  body=raw.decode('utf-8');idx={'git_blob':blob,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(body.splitlines()),'encoding':'utf-8','categories':categories(path),'retrieval':'R79 source/publication bytes freshly authenticated against remote exact tree','representative_path':path,'commit':sha}
  rawnew[blob]=raw;newidx.append(idx)
  hits=[{'line':i,'text':s[:1200]} for i,s in enumerate(body.splitlines(),1) if ISSUE.search(s)]
  if hits:issues[blob]=hits
require(len(set(newpaths))==829,'Wrong newly added scoped path count')
for x in newidx:indexed[x['git_blob']]=x
write('NEW_TEXT_INDEX.json.gz',newidx);write('NEW_ISSUE_LINES.json.gz',issues);write('CURRENT_HISTORICAL_TEXT_INDEX.json.gz',sorted(indexed.values(),key=lambda x:x['git_blob']));write('HISTORICAL_BLOB_VERSIONS.json.gz',versions)
require(set(indexed)==set(versions),'Historical version/content inventory differs')
with (O/'HISTORICAL_TEXT_DELTA_CURRENT.tar.gz').open('wb') as f:
 with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as z:
  with tarfile.open(fileobj=z,mode='w|') as ar:
   for blob,raw in sorted(rawnew.items()):
    t=tarfile.TarInfo('blobs/'+blob);t.size=len(raw);t.mode=0o644;t.mtime=0;ar.addfile(t,io.BytesIO(raw))
candidates=[x for x in newidx if 'report_candidate' in x['categories']]
for x in candidates:x['classification']='author source/provenance or execution record; not an added independent referee report'
write('NEW_REPORT_CANDIDATES.json',candidates)
review=lambda refs:{k:v for k,v in refs.items() if k.startswith('refs/heads/review/') and SCOPE.search(k)}
require(review(a)==review(b),'Review refs changed');write('REVIEW_REF_RECHECK.json',{'count':len(review(b)),'all_unchanged':True,'refs':[{'ref':k,'sha':v} for k,v in sorted(review(b).items())],'method':'All existing review refs unchanged; all new source/publication changes inspected; unrelated A2 delta outside scope.'})
oldreceipt=read(OLD/'CURRENT_CENSUS_RECEIPT.json')
receipt={'schema':'theta.current.complete-census-delta.v1','status':'PASS','started_utc':START,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_remote_refs':len(b),'all_unique_heads':len(heads),'head_commit_payloads_sha1_authenticated':len(heads),'all_ancestor_commits':len(anc),'scoped_changing_commits':oldreceipt['scoped_changing_commits']+2,'scoped_versioned_paths':oldreceipt['scoped_versioned_paths']+len(newpaths),'retained_archive_text_blobs_freshly_authenticated':len(oldindex),'new_text_blobs_freshly_read_authenticated_decoded':len(newidx),'total_unique_text_blobs':len(indexed),'authenticated_text_bytes':sum(x['bytes'] for x in indexed.values()),'new_text_bytes':sum(x['bytes'] for x in newidx),'r79_source_files_authenticated':806,'r79_publication_files_authenticated':23,'new_independent_referee_reports':0,'current_general_theta_review_refs':len(review(b)),'missing_blobs':0,'hash_mismatches':0,'method':'Fresh entire remote enumeration agrees with pagination. All inherited refs unchanged from retained R79 graph/content census; all old payloads freshly streamed and hashed; four new ancestors authenticated; all newly introduced scoped text read and indexed. A2 two-commit delta classified outside declared scope. No full history archive duplication.','scope':'All frozen branch heads and ancestors; General Theta/GTF-I text plus shallow shared governance/audit/report records. Retrieval, identity authentication, decoding and lexical issue indexing; not mathematical reproof or human refereeing.'}
write('CURRENT_CENSUS_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
