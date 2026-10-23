#!/usr/bin/env python3
"""Authenticate a remote ref snapshot, scoped history and complete R77 source.

Reads existing Git caches and retained archives without mutating either. The
scope is content retrieval/hash verification, not a reproof or external review.
"""
import argparse, collections, datetime, gzip, hashlib, io, json, os, pathlib, re, subprocess, tarfile

SCOPE = re.compile(r'general[ _-]*theta|theta[ _-]*general|gtf[ _-]*i(?:[ _./-]|$)', re.I)
TEXT = {'.tex','.bib','.md','.txt','.json','.csv','.tsv','.yml','.yaml','.py','.sh','.log','.sty','.cls','.toml','.html','.xml','.rst','.cfg','.ini','.aux','.bbl','.out'}
ISSUE = re.compile(r'\b(open|unproved|unresolved|gap|missing|incomplete|not proved|not established|conditional|priority|novelty|reject|A1|A2|pipeline|reset|rank constraint|no.message)\b',re.I)

def scoped_path(path):
    return bool(SCOPE.search(path) or (len(path.split('/'))<=3 and not path.startswith(('papers/','reviews/','revision/','tools/')) and re.search(r'audit|pipeline|ledger|referee|review|response|progress|governance|status|dependency',path,re.I)))

def jwrite(p,d):
    b=json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True).encode()+b'\n'
    if p.suffix=='.gz':
        with gzip.GzipFile(filename=str(p),mode='wb',mtime=0) as f:f.write(b)
    else:p.write_bytes(b)

def git_hash(kind,raw):return hashlib.sha1(f'{kind} {len(raw)}\0'.encode()+raw).hexdigest()

class JoinedParts(io.RawIOBase):
    def __init__(self,paths):self.paths=iter(paths);self.handle=None
    def readable(self):return True
    def readinto(self,b):
        while True:
            if self.handle is None:
                try:self.handle=open(next(self.paths),'rb')
                except StopIteration:return 0
            n=self.handle.readinto(b)
            if n:return n
            self.handle.close();self.handle=None
    def close(self):
        if self.handle:self.handle.close()
        super().close()

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--extra-repo',type=pathlib.Path,required=True);p.add_argument('--r77-source',type=pathlib.Path,required=True);p.add_argument('--refs',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_ALTERNATE_OBJECT_DIRECTORIES':str(a.extra_repo/'.git/objects')}
    def git(args):return subprocess.run(['git','-C',str(a.repo)]+args,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
    snap=json.loads(a.refs.read_text());refs=snap['all'];heads=sorted({r['sha'] for r in refs});old=json.loads((a.r77_source/'provenance/r77-audit/CURRENT_REFS.json').read_text())['all'];od={r['ref']:r['sha'] for r in old};nd={r['ref']:r['sha'] for r in refs}
    delta={'added':[r for r in refs if r['ref'] not in od],'changed':[{'ref':r['ref'],'old':od[r['ref']],'new':r['sha']} for r in refs if r['ref'] in od and od[r['ref']]!=r['sha']],'removed':[r for r in old if r['ref'] not in nd]};jwrite(a.out/'REF_DELTA_FROM_R77.json',delta)
    identities=[]
    for h in heads:
        raw=git(['cat-file','commit',h]);assert git_hash('commit',raw)==h
        header,body=raw.split(b'\n\n',1);lines=header.decode().splitlines();identities.append({'sha':h,'tree':next(l[5:] for l in lines if l.startswith('tree ')),'parents':[l[7:] for l in lines if l.startswith('parent ')],'subject':body.decode().splitlines()[0]})
    jwrite(a.out/'ALL_HEAD_COMMIT_IDENTITIES.json',identities)
    versions=collections.defaultdict(list);commits={};selected={};paths=set();current=None
    proc=subprocess.Popen(['git','-C',str(a.repo),'log','--raw','--no-abbrev','--no-renames','--full-history','--root','-m','--format=COMMIT%x09%H%x09%cI%x09%s',*heads,'--'],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for line in proc.stdout:
        if line.startswith(b'COMMIT\t'):
            f=line.decode().rstrip('\n').split('\t',3);current={'sha':f[1],'date':f[2],'subject':f[3]};commits[current['sha']]=current
        elif line.startswith(b':'):
            meta,sep,pathraw=line.rstrip(b'\n').partition(b'\t')
            if not sep:continue
            path=pathraw.decode('utf-8','replace')
            if not scoped_path(path):continue
            selected[current['sha']]=current;paths.add(path);f=meta.decode().split();sha=f[3]
            if sha=='0'*40 or pathlib.Path(path).suffix.lower() not in TEXT:continue
            rec={'commit':current['sha'],'path':path,'status':f[4]}
            if rec not in versions[sha]:versions[sha].append(rec)
    err=proc.stderr.read();assert proc.wait()==0,err.decode()
    jwrite(a.out/'ALL_ANCESTOR_COMMITS.json',sorted(commits.values(),key=lambda x:(x['date'],x['sha'])))
    jwrite(a.out/'SCOPED_CHANGE_COMMITS.json',sorted(selected.values(),key=lambda x:(x['date'],x['sha'])))
    jwrite(a.out/'HISTORICAL_BLOB_VERSIONS.json.gz',versions)
    src_commit='18b76a739898d2734c4f5bfcb609db0786cd4c11';src_path='papers/General-Theta-Foundations-I-restart/r77-shared-preparation-and-memory';pub_commit='300807bad3eb00ad8e1975ae9ff1ea1971a333db'
    source_tree=git(['rev-parse',src_commit+':'+src_path]).decode().strip();pub_tree=git(['rev-parse',pub_commit+':'+src_path]).decode().strip();assert source_tree==pub_tree
    source_entries=[];local_blob_paths={}
    for line in git(['ls-tree','-r','-z',src_commit+':'+src_path]).split(b'\0'):
        if not line:continue
        meta,name=line.split(b'\t',1);mode,kind,sha=meta.decode().split();name=name.decode();fp=a.r77_source/name;raw=fp.read_bytes();assert kind=='blob' and git_hash('blob',raw)==sha,(name,sha)
        source_entries.append({'path':name,'mode':mode,'git_blob':sha,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)});local_blob_paths[sha]=fp
    jwrite(a.out/'R77_SOURCE_AUTHENTICATION.json',{'source_commit':src_commit,'publication_commit':pub_commit,'source_tree':source_tree,'source_path':src_path,'files':source_entries,'count':len(source_entries)})
    found={};issues={};errors=[];legacy=[];archive_checks=[]
    def consume(sha,raw,origin):
        if sha not in versions or sha in found:return
        assert git_hash('blob',raw)==sha,(sha,origin)
        encoding='utf-8'
        try:body=raw.decode()
        except UnicodeDecodeError:
            if all(pathlib.Path(v['path']).suffix.lower()=='.log' for v in versions[sha]):encoding='latin-1';body=raw.decode(encoding);legacy.append(sha)
            else:raise
        cats=[]
        for v in versions[sha]:
            path=v['path'].lower();name=pathlib.Path(path).name
            if pathlib.Path(path).suffix in {'.tex','.bib'}:cats.append('native_mathematical_source')
            if re.search(r'proof|theorem|dependenc|ledger',path):cats.append('proof_ledger_or_map')
            if re.search(r'audit|pipeline',path):cats.append('internal_or_pipeline_audit')
            if re.search(r'response|rebuttal',path):cats.append('author_response')
            if re.search(r'verif|diagnostic|receipt|build|test|validation',path):cats.append('finite_or_build_verification')
            if re.search(r'referee.*report|report.*referee|external.*review|review.*report',path) and not re.search(r'^response|^author.response|^rebuttal|manifest|receipt',name):cats.append('report_candidate')
        lines=body.splitlines();hits=[{'line':i,'text':s[:1200]} for i,s in enumerate(lines,1) if ISSUE.search(s)]
        if hits:issues[sha]=hits
        found[sha]={'git_blob':sha,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(lines),'encoding':encoding,'categories':sorted(set(cats)),'retrieval':origin}
    audit=a.r77_source/'provenance/r77-audit';groups=[sorted((audit/'history-base-parts').glob('*.part*')),[audit/'history-delta/HISTORICAL_TEXT_DELTA_R77.tar.gz'],[audit/'all-ref-scope-extension/ADDITIONAL_TEXT_CORPUS.tar.gz']]
    for parts in groups:
        assert parts
        with io.BufferedReader(JoinedParts(parts)) as joined,tarfile.open(fileobj=joined,mode='r|gz') as tar:
            n=0;nb=0
            for member in tar:
                if not member.isfile():continue
                raw=tar.extractfile(member).read();sha=git_hash('blob',raw);declared=pathlib.Path(member.name).stem
                assert declared==sha,(member.name,sha)
                n+=1;nb+=len(raw);consume(sha,raw,'retained-r77-archive')
        archive_checks.append({'parts':[str(x.relative_to(a.r77_source)) for x in parts],'members_authenticated':n,'uncompressed_bytes':nb})
    for sha in sorted(set(versions)-set(found)):
        if sha in local_blob_paths:raw=local_blob_paths[sha].read_bytes();origin='authenticated-r77-source-file'
        else:
            try:raw=git(['cat-file','blob',sha]);origin='authenticated-git-object'
            except subprocess.CalledProcessError as e:errors.append({'sha':sha,'error':e.stderr.decode()});continue
        consume(sha,raw,origin)
    jwrite(a.out/'HISTORICAL_TEXT_INDEX.json.gz',list(found.values()));jwrite(a.out/'HISTORICAL_ISSUE_LINES.json.gz',issues);jwrite(a.out/'ARCHIVE_STREAM_AUTHENTICATION.json',archive_checks)
    review_refs=[r for r in refs if '/review/' in r['ref'] and SCOPE.search(r['ref'])];old_review_refs=[r for r in old if '/review/' in r['ref'] and SCOPE.search(r['ref'])];new_reports=[]
    oldidx=json.loads(gzip.decompress((audit/'full-scan/HISTORICAL_TEXT_INDEX.json.gz').read_bytes()));oldblobs={x['git_blob'] for x in oldidx};oldextra=json.loads(gzip.decompress((audit/'all-ref-scope-extension/ADDITIONAL_TEXT_INDEX.json.gz').read_bytes()))
    oldblobs.update(x['git_blob'] for x in oldextra)
    for sha,x in found.items():
        if sha not in oldblobs and 'report_candidate' in x['categories']:new_reports.append({**x,'versions':versions[sha]})
    jwrite(a.out/'NEW_REPORT_CANDIDATES.json',new_reports)
    receipt={'schema':'theta.r78.provenance-census.v1','started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_remote_refs':len(refs),'all_unique_heads':len(heads),'head_commit_payloads_sha1_authenticated':len(identities),'all_ancestor_commits':len(commits),'scoped_changing_commits':len(selected),'scoped_versioned_paths':len(paths),'unique_scoped_text_blobs':len(versions),'authenticated_decoded_text_blobs':len(found),'authenticated_decoded_bytes':sum(x['bytes'] for x in found.values()),'legacy_latex_logs_decoded_latin1':legacy,'missing_or_read_errors':errors,'r77_source_files_authenticated':len(source_entries),'r77_source_tree':source_tree,'current_general_theta_review_refs':len(review_refs),'previous_general_theta_review_refs':len(old_review_refs),'changed_review_refs':[r for r in review_refs if od.get(r['ref'])!=r['sha']],'new_report_candidates':len(new_reports),'scope':'All 1306 branch heads and their ancestors; General Theta/GTF-I versioned text and shared root-level governance/audits. Retrieval, byte authentication, decoding and lexical issue indexing, not line-by-line reproof or independent human review.'}
    jwrite(a.out/'CENSUS_RECEIPT.json',receipt);print(json.dumps(receipt));assert not errors

if __name__=='__main__':main()
