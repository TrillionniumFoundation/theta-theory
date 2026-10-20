#!/usr/bin/env python3
"""Verify the scoped Git object DAG; optionally recover all original proof variants.
Content-addressed recovery avoids expanding recursive archive copies. This is
source identity validation, not independent mathematical certification.
"""
from __future__ import annotations
import argparse,hashlib,io,json,re,tarfile
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ARCH=P/'provenance/remote-ci-38919903130/a2-dyn-historical-source.tar.gz'
EXPECTED='17b8a00ca97ba3979c8cdd063aaac659d0da84c0c0bfd2daa1c79c1e8ca88da7'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def oid(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--recover',type=Path);ap.add_argument('--details',type=Path);a=ap.parse_args()
    data=ARCH.read_bytes();require(hashlib.sha256(data).hexdigest()==EXPECTED,'frozen census archive mismatch')
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tar:
        members={m.name:m for m in tar.getmembers() if m.isfile()}
        require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in members),'unsafe archive member')
        def read(name):return tar.extractfile(members[name]).read()
        d=json.loads(read('history/INDEX.json'))
        blobs={n.rsplit('/',1)[-1]:read(n) for n in members if n.startswith('history/blobs/')}
    for sha,data in blobs.items():require(oid('blob',data)==sha,'blob object mismatch '+sha)
    for sha,es in d['trees'].items():
        raw=b''.join(e['mode'].lstrip('0').encode()+b' '+e['name'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in es)
        require(oid('tree',raw)==sha,'tree object mismatch '+sha)
        for e in es:require(e['sha'] in (d['trees'] if e['type']=='tree' else blobs),'unretained scoped object')
    for sha,raw in d['commits'].items():require(oid('commit',raw.encode())==sha,'commit object mismatch')
    proofs={};reports={}
    for sha,es in d['trees'].items():
        for e in es:
            match=re.match(r'(\d+)_.*\.tex$',e['name'])
            if match:
                key=e['sha'];item=proofs.setdefault(key,{'module':int(match[1]),'blob':key,'names':[],'scoped_parent_trees':[]})
                if e['name'] not in item['names']:item['names'].append(e['name'])
                item['scoped_parent_trees'].append(sha)
            if e['name']=='REFEREE_REPORT.md':reports.setdefault(e['sha'],[]).append(sha)
    require(set(v['module'] for v in proofs.values())==set(range(1,292)),'numbered historical coverage')
    if a.recover:
        dest=a.recover;dest.mkdir(parents=True,exist_ok=True)
        for sha,entry in proofs.items():
            name=f"{entry['module']:03d}/{sha}-{entry['names'][0]}";f=dest/'proofs'/name;f.parent.mkdir(parents=True,exist_ok=True)
            if f.exists():require(f.read_bytes()==blobs[sha],'refusing to overwrite different recovered proof')
            else:f.write_bytes(blobs[sha])
        for sha in reports:
            f=dest/'reports'/(sha+'.md');f.parent.mkdir(parents=True,exist_ok=True)
            if f.exists():require(f.read_bytes()==blobs[sha],'refusing to overwrite different report')
            else:f.write_bytes(blobs[sha])
        (dest/'RECOVERY_INDEX.json').write_text(json.dumps({'proofs':list(proofs.values()),'reports':reports},sort_keys=True,indent=2)+'\n')
    details={'archive_sha256':EXPECTED,'refs':[{'ref':r['ref'],'commit':r['commit'],'tree':r['tree']} for r in d['refs']],
        'proofs':list(proofs.values()),'report_objects':reports,'scope':d['scope']}
    if a.details:a.details.parent.mkdir(parents=True,exist_ok=True);a.details.write_text(json.dumps(details,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'passed','named_A2_DYN_heads':len(d['refs']),'commit_objects':len(d['commits']),
        'scoped_tree_objects':len(d['trees']),'scoped_blob_objects':len(blobs),'distinct_proof_blobs':len(proofs),
        'numbered_proof_ids':list(range(1,292)),'distinct_referee_report_blobs':len(reports),
        'all_intermediate_commits_examined':False,'all_historical_proofs_independently_reconstructed':False,
        'mathematical_proof_certificate':False,'archive_sha256':EXPECTED},sort_keys=True,indent=2))
if __name__=='__main__':main()
