#!/usr/bin/env python3
"""Reproduce the General Theta history inventory without a full worktree.

The inventory traverses all ancestors of an immutable, supplied branch snapshot.
It filters versioned paths, then checks complete text blob contents and records
both Git object IDs and SHA-256. Four historical eight-bit TeX logs require
byte-preserving Latin-1 decoding; text decoding/lexical indexing is not a reproof.
Network materialization is a separate explicit step; this script never fetches.
"""
import argparse, collections, datetime, gzip, hashlib, json, os, pathlib, re, subprocess, tarfile, io

SCOPE = re.compile(r'general[ _-]*theta|theta[ _-]*general|gtf[ _-]*i(?:[ _./-]|$)', re.I)
TEXT = {'.tex','.bib','.md','.txt','.json','.csv','.tsv','.yml','.yaml','.py','.sh','.log','.sty','.cls','.toml','.html','.xml','.rst','.cfg','.ini','.aux','.bbl','.out'}
ISSUE = re.compile(r'\b(open|unproved|unresolved|gap|missing|incomplete|not proved|not established|conditional|priority|novelty|reject|A1|A2|B4|C2|pipeline|reset|rank constraint|no.message)\b',re.I)

def scoped_path(path):
    if SCOPE.search(path):return True
    # Shared repository-level pipeline governance and audits are dependencies,
    # not independent General Theta referee reports or new author manuscripts.
    return (len(path.split('/'))<=3 and not path.startswith(('papers/','reviews/','revision/','tools/')) and re.search(r'audit|pipeline|ledger|referee|review|response|progress|governance|status|dependency',path,re.I))

def run(repo, args, **kw):
    return subprocess.run(['git','-C',str(repo)]+args,check=True,stdout=subprocess.PIPE,**kw).stdout

def jwrite(path, data):
    raw=json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True).encode()+b'\n'
    if str(path).endswith('.gz'):
        with gzip.GzipFile(filename=str(path),mode='wb',mtime=0) as f:f.write(raw)
    else:path.write_bytes(raw)

def categories(path, body):
    p=path.lower(); ans=[]
    if pathlib.Path(p).suffix in {'.tex','.bib'}:ans.append('native_mathematical_source')
    if re.search(r'proof|theorem|dependenc|ledger',p):ans.append('proof_ledger_or_map')
    if re.search(r'audit|pipeline',p):ans.append('internal_or_pipeline_audit')
    if re.search(r'response|rebuttal',p):ans.append('author_response')
    if re.search(r'verif|diagnostic|receipt|build|test|validation',p):ans.append('finite_or_build_verification')
    name=pathlib.Path(p).name
    if re.search(r'referee.*report|report.*referee|external.*review|review.*report',p) and not re.search(r'^response|^author.response|^rebuttal|manifest|receipt',name):ans.append('report_candidate')
    return ans

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=pathlib.Path);ap.add_argument('--refs',required=True,type=pathlib.Path);ap.add_argument('--out',required=True,type=pathlib.Path);ap.add_argument('--inventory-only',action='store_true');ap.add_argument('--corpus',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat(); snap=json.loads(a.refs.read_text()); allrefs=snap['all']; scoped=[r for r in allrefs if re.search(r'general[-_]theta|gtf[-_]i|gtf1|^refs/heads/realization/',r['ref'],re.I)]; mainref=next(r for r in allrefs if r['ref']=='refs/heads/main');selected=scoped+[mainref]; heads=sorted({r['sha'] for r in selected})
    args=['log','--raw','--no-abbrev','--no-renames','--full-history','--root','-m','--format=COMMIT%x09%H%x09%cI%x09%s']+heads+['--']
    proc=subprocess.Popen(['git','-C',str(a.repo)]+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    versions=collections.defaultdict(list); commits={}; selected_commits={}; current=None; allpaths=set()
    with gzip.GzipFile(filename=str(a.out/'PINNED_HISTORY_RAW_DIFF.txt.gz'),mode='wb',mtime=0) as rawout:
        for line in proc.stdout:
            if line.startswith(b'COMMIT\t'):
                fields=line.decode('utf-8').rstrip('\n').split('\t',3);current={'sha':fields[1],'date':fields[2],'subject':fields[3]};commits[current['sha']]=current
            elif line.startswith(b':'):
                meta,sep,pathraw=line.rstrip(b'\n').partition(b'\t')
                if not sep:continue
                path=pathraw.decode('utf-8','replace')
                if not scoped_path(path):continue
                rawout.write(('COMMIT\t'+current['sha']+'\t'+current['date']+'\t'+current['subject']+'\n').encode());rawout.write(line)
                selected_commits[current['sha']]=current;allpaths.add(path)
                fields=meta.decode().split();sha=fields[3];status=fields[4]
                if sha=='0'*40 or pathlib.Path(path).suffix.lower() not in TEXT:continue
                record={'commit':current['sha'],'path':path,'status':status}
                if record not in versions[sha]:versions[sha].append(record)
    err=proc.stderr.read();code=proc.wait()
    if code:raise RuntimeError(err.decode())
    check=subprocess.Popen(['git','-C',str(a.repo),'cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'})
    result,err=check.communicate(('\n'.join(sorted(versions))+'\n').encode());missing=[];sizes={}
    for line in result.decode().splitlines():
        f=line.split()
        if len(f)==2 and f[1]=='missing':missing.append(f[0])
        elif len(f)==3:sizes[f[0]]=int(f[2])
        else:raise RuntimeError(line)
    (a.out/'MISSING_BLOBS.txt').write_text('\n'.join(missing)+ ('\n' if missing else ''))
    jwrite(a.out/'BRANCH_PROVENANCE.json',{'scope_rule':'General Theta/GTF-I and all realization branches, plus main','retrieval':snap.get('retrieval_observed_by_utc'), 'all_refs':allrefs,'selected_refs':selected,'selected_unique_heads':len(heads)})
    jwrite(a.out/'HISTORICAL_BLOB_VERSIONS.json.gz',versions);jwrite(a.out/'HISTORICAL_COMMITS.json',sorted(selected_commits.values(),key=lambda x:(x['date'],x['sha'])));jwrite(a.out/'HISTORICAL_ALL_PATHS.json.gz',sorted(allpaths))
    prelim={'started_utc':started,'repository':'TrillionniumFoundation/theta-theory','all_branch_count':len(allrefs),'scoped_branch_count':len(scoped),'scoped_unique_head_count':len(set(r['sha'] for r in scoped)),'selected_branch_count_including_main':len(selected),'selected_unique_head_count_including_main':len(heads),'ancestor_commit_count':len(commits),'scoped_change_commit_count':len(selected_commits),'scoped_change_or_selected_head_commit_count':len(set(selected_commits)|set(heads)),'unique_scoped_path_count':len(allpaths),'eligible_unique_text_blob_count':len(versions),'missing_blobs_before_read':len(missing),'eligible_present_uncompressed_bytes':sum(sizes.values()),'inventory_only':a.inventory_only,'path_scope':'General Theta/GTF-I named paths and shared repository-level pipeline/audit/governance records; unrelated paper/review/revision folders excluded unless explicitly imported within a General Theta source edition'}
    jwrite(a.out/'HISTORY_INVENTORY_RECEIPT.json',prelim)
    if a.inventory_only:print(json.dumps(prelim));return
    if missing:raise RuntimeError(f'{len(missing)} blobs require explicit materialization before full scan')
    reader=subprocess.Popen(['git','-C',str(a.repo),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'})
    index=[];issues={};catcounts=collections.Counter();decodefails=[];bytecount=0;legacy_logs=[]
    tar=tarfile.open(a.out/'HISTORICAL_TEXT_CORPUS.tar.gz','w:gz') if a.corpus else None
    for sha in sorted(versions):
        reader.stdin.write((sha+'\n').encode());reader.stdin.flush();header=reader.stdout.readline().decode().split()
        if len(header)!=3 or header[0]!=sha or header[1]!='blob':raise RuntimeError(str(header))
        size=int(header[2]);content=reader.stdout.read(size);terminator=reader.stdout.read(1)
        if len(content)!=size or terminator!=b'\n':raise RuntimeError('truncated blob '+sha)
        actual=hashlib.sha1(f'blob {len(content)}\0'.encode()+content).hexdigest()
        if actual!=sha:raise RuntimeError('Git hash mismatch '+sha)
        encoding='utf-8'
        try:body=content.decode(encoding)
        except UnicodeDecodeError as e:
            if all(pathlib.Path(v['path']).suffix.lower()=='.log' for v in versions[sha]):
                encoding='latin-1';body=content.decode(encoding);legacy_logs.append({'blob':sha,'encoding':encoding,'reason':'8-bit LaTeX transcript, decoded byte-for-byte; original bytes remain the hash authority'})
            else:decodefails.append({'blob':sha,'error':str(e),'versions':versions[sha]});continue
        bytecount+=size;cats=sorted(set(c for v in versions[sha] for c in categories(v['path'],body)));catcounts.update(cats)
        lines=body.splitlines();matches=[{'line':i,'text':line[:1200]} for i,line in enumerate(lines,1) if ISSUE.search(line)]
        if matches:issues[sha]=matches
        index.append({'git_blob':sha,'sha256':hashlib.sha256(content).hexdigest(),'bytes':size,'lines':len(lines),'encoding':encoding,'categories':cats,'versions':versions[sha]})
        if tar:
            info=tarfile.TarInfo('blobs/'+sha+'.txt');info.size=size;info.mtime=0;info.mode=0o644;tar.addfile(info,io.BytesIO(content))
    reader.stdin.close();reader.wait()
    if tar:tar.close()
    jwrite(a.out/'HISTORICAL_TEXT_INDEX.json.gz',index);jwrite(a.out/'HISTORICAL_ISSUE_LINES.json.gz',issues);jwrite(a.out/'DECODE_FAILURES.json',decodefails);jwrite(a.out/'LEGACY_LOG_ENCODINGS.json',legacy_logs)
    receipt={**prelim,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inventory_only':False,'decoded_and_hash_verified_unique_text_blobs':len(index),'utf8_text_blobs':len(index)-len(legacy_logs),'legacy_8bit_latex_logs':len(legacy_logs),'decoded_bytes':bytecount,'decode_failures':len(decodefails),'overlapping_category_counts':dict(catcounts),'scope_limitation':'Complete text decoding, hashing and lexical issue indexing of eligible versioned paths; not a line-by-line reproof, formal proof check, human expert assessment or scan of binary source archives.'}
    jwrite(a.out/'HISTORY_SCAN_RECEIPT.json',receipt);print(json.dumps(receipt))

if __name__=='__main__':main()
