#!/usr/bin/env python3
"""Read-only whole-ref refresh and native baseline verification for GTF-I.

This verifies the native baseline and binds a separately executed fresh full
historical text scan. No repository state is mutated by this script.
"""
import collections
import datetime
import gzip
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

REPO = Path('/workspace/scratch/f856e3d63ac5/theta-revision')
OUT = Path('/workspace/scratch/f856e3d63ac5/r74-audit')
SOURCE_COMMIT = 'e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b'
PUBLICATION_COMMIT = '39980d65d6665e52c30aa340cfb0e2eb199c0f9a'
SOURCE_PATH = 'papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form'
SOURCE = REPO / SOURCE_PATH
PUBLICATION = REPO / (SOURCE_PATH + '-publication')
PROVENANCE = SOURCE / 'provenance'

def git(*args, stdin=None):
    return subprocess.check_output(['git', '-C', str(REPO), *args], input=stdin)

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + '\n')

def identity(data):
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()}

def require(test, message):
    if not test:
        raise RuntimeError(message)

def main():
    snapshot = json.loads((OUT / 'CURRENT_REFS.json').read_text())
    refs = snapshot['all']
    old_snapshot_data = (PROVENANCE / 'REFS_SNAPSHOT.json').read_bytes()
    old_snapshot = json.loads(old_snapshot_data)
    old = {r['ref']:r['sha'] for r in old_snapshot['all']}
    now = {r['ref']:r['sha'] for r in refs}
    require(all(now.get(k)==v for k,v in old.items()), 'Existing historical ref changed')

    metadata=[]
    for sha in sorted({r['sha'] for r in refs}):
        raw=git('cat-file','commit',sha)
        require(hashlib.sha1(f'commit {len(raw)}\0'.encode()+raw).hexdigest()==sha,'Commit object hash mismatch')
        headers, message=raw.decode().split('\n\n',1)
        lines=headers.splitlines()
        def date(kind):
            line=next(x for x in lines if x.startswith(kind+' '))
            timestamp,offset=line.rsplit(' ',2)[1:]
            tz=datetime.timezone(datetime.timedelta(minutes=(1 if offset[0]=='+' else -1)*(60*int(offset[1:3])+int(offset[3:]))))
            return datetime.datetime.fromtimestamp(int(timestamp),tz).isoformat()
        metadata.append({'commit':sha,'tree':lines[0].split()[1],
                         'parents':[x.split()[1] for x in lines if x.startswith('parent ')],
                         'author_date':date('author'),'committer_date':date('committer'),
                         'subject':message.splitlines()[0]})
    write('ALL_CURRENT_HEAD_METADATA.json', metadata)

    manifest_data = (SOURCE/'SOURCE_MANIFEST.json').read_bytes()
    manifest = json.loads(manifest_data)
    source_files=[]
    for item in manifest['files']:
        f=SOURCE/item['path'];data=f.read_bytes();actual=identity(data)
        require(all(actual[k]==item[k] for k in actual), 'Manifest mismatch '+item['path'])
        source_files.append({'path':item['path'],**actual})
    actual_paths={str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    expected_paths={x['path'] for x in manifest['files']} | {'SOURCE_MANIFEST.json'}
    require(actual_paths==expected_paths, 'Source inventory mismatch')
    source_tree=git('rev-parse',SOURCE_COMMIT+':'+SOURCE_PATH).decode().strip()
    pub_source_tree=git('rev-parse',PUBLICATION_COMMIT+':'+SOURCE_PATH).decode().strip()
    require(source_tree==pub_source_tree=='0507d04ad0bebd20cb0ce609ab94f7cc67d11f56','Source tree mismatch')

    closures={}
    for root in ('main.tex','supplement.tex','companion-r58/main.tex'):
        base=SOURCE/('companion-r58' if root.startswith('companion-r58') else '')
        visited=set()
        def walk(path):
            rel=str(path.relative_to(SOURCE))
            if rel in visited:return
            require(path.is_file(),'Missing input '+str(path))
            visited.add(rel)
            body=path.read_text()
            body=re.sub(r'(?<!\\)%[^\n]*','',body)
            for child in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',body):
                q=base/child
                if not q.suffix:q=q.with_suffix('.tex')
                walk(q)
        walk(SOURCE/root)
        closures[root]=sorted(visited)

    receipt=json.loads((PUBLICATION/'BUILD_RECEIPT.json').read_text())
    delivery=json.loads((PUBLICATION/'DELIVERY_RECORD.json').read_text())
    require(delivery['source_commit']==SOURCE_COMMIT,'Publication source binding mismatch')
    docs=[]
    for item in delivery['documents']:
        data=(PUBLICATION/item['file']).read_bytes();actual=identity(data)
        require(actual['sha256']==item['sha256'] and actual['bytes']==item['bytes'], 'Published PDF hash mismatch')
        info=subprocess.check_output(['pdfinfo',str(PUBLICATION/item['file'])]).decode()
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        require(pages==item['pages'],'PDF page mismatch')
        docs.append({'file':item['file'],'pages':pages,**actual})
    archive_path=PUBLICATION/delivery['source_archive']['file']
    archive_identity=identity(archive_path.read_bytes())
    require(archive_identity['sha256']==delivery['source_archive']['sha256'],'Archive hash mismatch')
    with zipfile.ZipFile(archive_path) as archive:
        zipped={name.split('/',1)[1]:name for name in archive.namelist() if '/' in name}
        require(set(zipped)==actual_paths,'Archive source inventory mismatch')
        for rel,name in zipped.items():
            require(archive.read(name)==(SOURCE/rel).read_bytes(),'Archive source bytes mismatch '+rel)

    report_data=(PROVENANCE/'R65_REFEREE_REPORT.md').read_bytes()
    require(identity(report_data)['git_blob']=='d1ff9c5662390156ee212c82b173e86a21180e84','Report identity mismatch')
    history_data=(PROVENANCE/'HISTORICAL_TEXT_INDEX.json.gz').read_bytes()
    history=json.loads(gzip.decompress(history_data))
    history_receipt=json.loads((PROVENANCE/'HISTORY_SCAN_RECEIPT.json').read_text())
    require(len(history)==history_receipt['decoded_and_hash_verified_unique_text_blobs']==6363,'Historical inventory size mismatch')
    require(sum(x['bytes'] for x in history)==history_receipt['decoded_bytes']==77994293,'Historical byte total mismatch')
    require(len({x['git_blob'] for x in history})==len(history),'Historical duplicate object')
    fresh=OUT/'current-full-scan'
    fresh_data=(fresh/'HISTORICAL_TEXT_INDEX.json.gz').read_bytes()
    fresh_index=json.loads(gzip.decompress(fresh_data))
    fresh_receipt=json.loads((fresh/'HISTORY_SCAN_RECEIPT.json').read_text())
    fresh_by_blob={x['git_blob']:x for x in fresh_index}
    for prior in history:
        require(prior['git_blob'] in fresh_by_blob,'Prior historical blob missing')
        current=fresh_by_blob[prior['git_blob']]
        require(all(current[k]==prior[k] for k in ('bytes','sha256','encoding')),'Prior historical identity changed')
    require(fresh_receipt['missing_blobs_before_read']==fresh_receipt['decode_failures']==0,'Incomplete fresh historical scan')
    require(len(fresh_index)==fresh_receipt['decoded_and_hash_verified_unique_text_blobs'],'Fresh historical index length mismatch')
    require(sum(x['bytes'] for x in fresh_index)==fresh_receipt['decoded_bytes'],'Fresh historical byte total mismatch')
    old_blobs={x['git_blob'] for x in history}
    added=[x for x in fresh_index if x['git_blob'] not in old_blobs]
    require(not any('report_candidate' in x['categories'] for x in added),'New report candidate requires inspection')
    review_classes=json.loads((PROVENANCE/'REVIEW_DIFF_CLASSIFICATION.json').read_text())
    require(all(now.get(x['ref'])==x['head'] for x in review_classes),'Historical review head changed')

    new_commits=json.loads((OUT/'NEW_COMMITS.json').read_text())
    new_gtf=[];other=[]
    for c in new_commits:
        paths=[row.split('\t')[-1] for row in c['changes']]
        if any(SOURCE_PATH in p for p in paths):
            require(c['sha'] in (PUBLICATION_COMMIT,SOURCE_COMMIT,'f3f3f4b521e866a49a567558f41ecd1a98d26363'),'Unexpected GTF source change')
            new_gtf.append({'commit':c['sha'],'subject':c['subject'],'changed_paths':len(paths)})
        else:
            require(all(p.startswith(('papers/A2-DYN','.github/workflows/')) for p in paths),'Unclassified new ancestor path')
            other.append({'commit':c['sha'],'subject':c['subject'],'changed_paths':len(paths),'classification':'A2-DYN source/publication or corresponding workflow; no General Theta path'})

    result={
      'schema':'theta.r74.baseline-refresh.v1',
      'status':'PASS',
      'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'role':'Author-team AI provenance audit; not a new external referee report or mathematical proof certificate',
      'repository':'TrillionniumFoundation/theta-theory',
      'all_head_count':len(refs),
      'unique_head_count':len(metadata),
      'all_head_metadata_read':True,
      'old_refs_unchanged':len(old),
      'new_refs':len(now)-len(old),
      'diff_from_r73_initial':snapshot['diff_from_r73_initial'],
      'new_ancestor_count':len(new_commits),
      'new_general_theta_commits':new_gtf,
      'new_other_paper_commits':other,
      'manuscript':{
        'source_commit':SOURCE_COMMIT,'publication_commit':PUBLICATION_COMMIT,
        'source_path':SOURCE_PATH,'source_tree':source_tree,
        'source_repository_tree':git('rev-parse',SOURCE_COMMIT+'^{tree}').decode().strip(),
        'publication_repository_tree':git('rev-parse',PUBLICATION_COMMIT+'^{tree}').decode().strip(),
        'source_manifest':identity(manifest_data),'source_file_count':len(actual_paths),
        'source_manifest_all_bytes_rechecked':True,
        'input_closure':closures,'documents':docs,
        'build_receipt':identity((PUBLICATION/'BUILD_RECEIPT.json').read_bytes()),
        'source_archive':{'file':archive_path.name,**archive_identity,'all_source_file_bytes_rechecked':True},
        'published_receipt_interpretation':'Actual prior source-bound execution, not relabeled as a new R74 run',
        'readability':'All three PDFs are readable by pdfinfo; full native input graph is present. Visual QA and original successful native builds are separately fixed prior evidence.',
      },
      'report':{
        'commit':'358481b21ceeeedb1205ebd30f86982e32a2cb04',
        'original_path':'GENERAL_THETA_FOUNDATIONS_I_RESTART_R65_BOUNDARY_MEMORY_EXTERNAL_REFEREE_REPORT_R65.md',
        **identity(report_data),
        'full_report_reread':True,
        'latest_response':{'commit':SOURCE_COMMIT,'path':SOURCE_PATH+'/RESPONSE_TO_REFEREE.md',**identity((SOURCE/'RESPONSE_TO_REFEREE.md').read_bytes())},
        'latest_response_fully_reread':True,
        'classification':'Latest applicable deposited substantive report; not a new unanswered report on R73. R66-R73 give substantive replies; surviving contribution and broader-scope questions continue.',
      },
      'inherited_history':{
        'containing_commit':SOURCE_COMMIT,
        'index_file':'provenance/HISTORICAL_TEXT_INDEX.json.gz',**identity(history_data),
        'indexed_text_objects':len(history),'indexed_bytes':sum(x['bytes'] for x in history),
        'original_scan_completed_utc':history_receipt['completed_utc'],
        'review_branch_classifications_revalidated':len(review_classes),
        'all_old_branch_heads_unchanged':True,
        'scope':'Pinned previous historical record, independently checked against the separately executed complete fresh text scan below.',
      },
      'fresh_complete_history_scan':{
        'receipt':fresh_receipt,
        'receipt_identity':identity((fresh/'HISTORY_SCAN_RECEIPT.json').read_bytes()),
        'index_identity':identity(fresh_data),
        'previous_6363_objects_all_reread_with_identical_hashes':True,
        'new_text_objects':len(added),
        'new_report_candidate_blobs':0,
        'corpus_identity':identity((fresh/'HISTORICAL_TEXT_CORPUS.tar.gz').read_bytes()),
        'limitation':'All scoped text objects were read, decoded, hashed and lexically indexed; this is not a fresh line-by-line reproof, proof-assistant verification, independent human referee assessment, or recompilation of every old binary edition.'
      },
      'conclusion':'R73 is the latest complete native author source because its complete source, sealed status, source-bound readable publication and exact ancestry are verified. No later valid General Theta source or deposited substantive referee report appears in the current whole-ref inventory.'
    }
    write('BASELINE_REFRESH_RECEIPT.json',result)
    write('BASELINE_SOURCE_IDENTITIES.json',source_files+[{'path':'SOURCE_MANIFEST.json',**identity(manifest_data)}])
    print(json.dumps({'status':result['status'],'heads':len(refs),'unique_heads':len(metadata),'source_files':len(actual_paths),'new_commits':len(new_commits),'baseline_source':SOURCE_COMMIT}))

if __name__=='__main__':main()
