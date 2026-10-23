#!/usr/bin/env python3
"""Authenticate the R80 baseline census extension using only delivered files.

Stream the exact 72-text R79-source/publication delta; authenticate its extension
from 7,201 to 7,273 historical texts; recompute all 875 frozen head identities;
check the four new ancestors, unchanged prior refs and review classification.
The inherited R78 and R79 portable checkers separately authenticate all retained
7,201 payloads. No extraction, Git, network or third-party library is used. Only
an explicitly requested receipt outside --source-root may be written.
"""
from __future__ import annotations
import argparse,base64,datetime,gzip,hashlib,json,re,tarfile
from pathlib import Path,PurePosixPath

MANIFEST_SHA256='4bd97f2c0343b9f83a5038f35704016338e2ef13a495c852d65b98ab9c055456'

def require(v,m):
    if not v:raise RuntimeError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def gh(kind,b):return hashlib.sha1(f'{kind} {len(b)}\0'.encode()+b).hexdigest()
def safe(root,relative):
    p=PurePosixPath(relative)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe input path')
    f=root.joinpath(*p.parts)
    require(f.is_file() and not f.is_symlink() and root in f.resolve().parents,
            'Missing/nonregular/escaped input '+relative)
    return f
def parse(name,raw):return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
def index(rows):
    d={}
    for r in rows:
        k=r.get('git_blob','')
        require(re.fullmatch('[0-9a-f]{40}',k) and k not in d,'Invalid/duplicate blob')
        require(type(r.get('bytes')) is int and r['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',r.get('sha256','')),'Malformed indexed identity')
        d[k]=r
    return d
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument('--receipt',type=Path)
    a=p.parse_args();source=a.source_root.resolve();bundle=Path(__file__).resolve().parent
    if a.receipt is not None:
        dest=a.receipt.resolve();require(dest!=source and source not in dest.parents,'Receipt must be outside the source')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    raw=safe(bundle,'CURRENT_HISTORY_MANIFEST.json').read_bytes()
    require(digest(raw)==MANIFEST_SHA256,'Pinned current census manifest differs')
    manifest=json.loads(raw);require(manifest['schema']=='theta.r80.portable-census-delta.v1','Wrong schema')
    data={}
    for row in manifest['files']:
        key=row['path'];require(key not in data,'Duplicate bundled path');raw=safe(bundle,key).read_bytes()
        require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Current input differs '+key);data[key]=raw
    inherited={}
    for row in manifest['inherited_files']:
        key=row['path'];require(key not in inherited,'Duplicate inherited path');raw=safe(source,key).read_bytes()
        require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Inherited input differs '+key);inherited[key]=raw
    def current(n):return parse(n,data[n])
    def old(n):return parse(n,inherited['provenance/r79-audit/'+n])
    retained=index(old('CURRENT_HISTORICAL_TEXT_INDEX.json.gz'))
    extra=index(current('NEW_TEXT_INDEX.json.gz'));alltexts=index(current('CURRENT_HISTORICAL_TEXT_INDEX.json.gz'))
    require(len(retained)==7201 and len(extra)==72 and len(alltexts)==7273,'Text inventory count differs')
    require(not set(retained)&set(extra) and set(alltexts)==set(retained)|set(extra),'Text inventory partition differs')
    for k,r in {**retained,**extra}.items():require(all(r[f]==alltexts[k][f] for f in ('bytes','sha256')),'Text identity changed')
    seen=set();bytecount=0
    with tarfile.open(safe(bundle,'HISTORICAL_TEXT_DELTA_CURRENT.tar.gz'),'r|gz') as archive:
        for member in archive:
            path=PurePosixPath(member.name)
            require(member.isfile() and len(path.parts)==2 and path.parts[0]=='blobs' and path.parts[1] in extra,'Unexpected archive member')
            key=path.parts[1];require(key not in seen,'Duplicated delta member')
            f=archive.extractfile(member);require(f is not None,'Unreadable archive member');raw=f.read();r=extra[key]
            require(len(raw)==member.size==r['bytes'] and gh('blob',raw)==key and digest(raw)==r['sha256'],'Delta content identity differs')
            raw.decode('utf-8');seen.add(key);bytecount+=len(raw)
    require(seen==set(extra) and bytecount==3786951,'Delta inventory/bytes differ')
    require(sum(x['bytes'] for x in alltexts.values())==116158319,'Total historical bytes differ')
    previous={r['ref']:r['sha'] for r in old('CURRENT_REFS.json')['all']}
    refs={r['ref']:r['sha'] for r in current('CURRENT_REFS.json')['all']}
    require(len(previous)==1307 and len(refs)==1309 and all(refs.get(k)==v for k,v in previous.items()),'Old ref changed/disappeared')
    added={k:v for k,v in refs.items() if k not in previous}
    require(set(added.values())=={'a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2','1e44e7a3360aa1ff41de4fc8f8b71fd173f6ba2a'},'Unexpected new head')
    require(current('BRANCH_PAGINATION_CHECK.json')['status']=='PASS' and current('BRANCH_PAGINATION_CHECK.json')['paginated_count']==len(refs),'Independent enumeration differs')
    payloads={}
    for row in old('HEAD_COMMIT_OBJECTS.json.gz')+current('NEW_COMMIT_PAYLOADS.json.gz'):
        k=row['sha'];raw=base64.b64decode(row['payload_base64'],validate=True)
        require(gh('commit',raw)==k,'Bad commit payload')
        require(k not in payloads or payloads[k]==raw,'Conflicting commit payload');payloads[k]=raw
    heads=set(refs.values());require(len(heads)==875 and heads<=set(payloads),'Missing current head payload')
    ancestors=set(inherited['provenance/r79-audit/ALL_ANCESTOR_COMMITS.txt'].decode().splitlines())
    current_anc=set(data['ALL_ANCESTOR_COMMITS.txt'].decode().splitlines());new=current('NEW_COMMIT_IDENTITIES.json');newids={r['sha'] for r in new}
    require(len(ancestors)==2711 and len(newids)==4 and not ancestors&newids and current_anc==ancestors|newids,'Ancestor extension differs')
    for row in new:
        raw=payloads[row['sha']];header=raw.split(b'\n\n',1)[0].decode()
        parents=re.findall(r'^parent (\w+)$',header,re.M);tree=re.search(r'^tree (\w+)$',header,re.M)
        require(tree is not None and tree.group(1)==row['tree'] and parents==row['parents'] and set(parents)<=current_anc,'Bad new ancestor metadata')
    review=current('REVIEW_REF_RECHECK.json');require(review['count']==132 and review['all_unchanged'],'Review inventory differs')
    for r in review['refs']:require(previous.get(r['ref'])==refs.get(r['ref'])==r['sha'],'Review ref changed')
    require(current('NEW_REPORT_CANDIDATES.json')==[],'Unclassified new report candidate')
    result={'schema':'theta.r80.portable-current-history-verification.v1','status':'PASS','started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_source_commit':'90cae2f5aca243b39d3a2194a4d6e0696671a101','baseline_publication_commit':'a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2','current_remote_refs':len(refs),'distinct_head_commit_payloads_authenticated':len(heads),'ancestor_commits':len(current_anc),'retained_index_blobs':len(retained),'additional_text_blobs_read_authenticated_decoded':len(seen),'additional_text_bytes_read_authenticated_decoded':bytecount,'combined_index_blobs':len(alltexts),'combined_index_bytes':sum(x['bytes'] for x in alltexts.values()),'new_independent_referee_report_candidates':0,'manifest_sha256':MANIFEST_SHA256,'verifier_sha256':digest(Path(__file__).read_bytes()),'retained_archive_requirement':'Run the unchanged provenance/r78-audit/verify_history_r78.py and provenance/r79-audit/verify_current_history.py separately to authenticate all 7201 retained payloads in the same verification run.','scope':'Portable content/commit identity verification only; no new theorem reproof, independent human review, hosted CI or editorial decision.'}
    if a.receipt is not None:a.receipt.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
