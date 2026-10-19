#!/usr/bin/env python3
"""Prepare, but do not publish, an exact metadata-only successor of tested C2.

The actual GitHub object/ref calls are retained separately. This program has no
network access and never updates a Git ref. Explicit gates also run under -O.
"""
from pathlib import Path
import hashlib
import importlib.util
import json

WORK = Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019')
ROOT = WORK.parent/'theta-theory/papers/A2-DYN-physical-tube-source-height-author-revision'
PREFIX = 'delivery/publication/physical-tube-20261019/'
SOURCE_GATE = 'evidence/current-execution/physical-tube-publication-source/'
MANIFEST_SHA = 'a891751e40fd6bb41fec5bd099883f78a66e616aeb4a95496694f991d95cc069'
WORKFLOW_SHA = '3723f4b215e823e9a6353e2b29151e8194e4430f663be71600d2cde1610ee7db'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def write(name, obj):
    path = WORK/name
    path.write_text(json.dumps(obj, indent=2)+'\n')
    return path

def main():
    spec = importlib.util.spec_from_file_location('transport_revision', WORK/'transport_revision.py')
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    spec2 = importlib.util.spec_from_file_location('source_gate', ROOT/'tools/package_source_manifest.py')
    gate = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(gate)
    manifest_result = gate.verify_manifest(ROOT)
    require(hashlib.sha256((ROOT/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()==MANIFEST_SHA,
            'Frozen source manifest itself changed')
    for path in (ROOT/'ci/a2-dyn-physical-tube-source-height-20261019.yml',
                 ROOT.parents[1]/'.github/workflows/a2-dyn-physical-tube-source-height-20261019.yml'):
        require(hashlib.sha256(path.read_bytes()).hexdigest()==WORKFLOW_SHA,
                'Tested workflow changed')
    before = json.loads((WORK/'C2_FILE_IDENTITIES.json').read_text())
    old = {r['path']: r for r in before['files']}
    rows = adapter.scan()
    current = {r['path']: r for r in rows}
    require(set(old)<=set(current), 'Metadata successor removes an existing article file')
    changed = [r for r in rows if r['path'] not in old or
               any(r[k]!=old[r['path']][k] for k in ('sha','mode','bytes'))]
    require(changed, 'No metadata delta to publish')
    require(all(r['path']=='PUBLICATION_STATUS.json' or r['path'].startswith((PREFIX,SOURCE_GATE))
                for r in changed), 'Change lies outside the metadata-only publication scope')
    known = {r['sha'] for r in before['files']}
    unique = {}
    for row in changed:
        if row['sha'] not in known and (row['encoding']=='base64' or row['bytes']>120000):
            unique.setdefault(row['sha'],row)
    large = list(unique.values())
    large_shas = set(unique)
    elements = []
    for row in changed:
        entry = {'path':row['path'],'mode':row['mode'],'type':'blob'}
        if row['sha'] in known or row['sha'] in large_shas:
            entry['sha'] = row['sha']
        else:
            # read_bytes/decode retains literal CRLF; text-mode normalization would not.
            entry['content'] = (ROOT/row['path']).read_bytes().decode('utf-8')
        elements.append(entry)
    batches, batch, size = [], [], 0
    for entry in elements:
        amount = len(json.dumps(entry))
        if batch and (len(batch)>=60 or size+amount>180000):
            batches.append(batch)
            batch, size = [], 0
        batch.append(entry)
        size += amount
    if batch:
        batches.append(batch)
    cumulative = dict(old)
    plan = []
    for index, batch in enumerate(batches):
        for entry in batch:
            cumulative[entry['path']] = current[entry['path']]
        expected, _ = adapter.tree_digest(list(cumulative.values()))
        payload = {'tree_elements':batch,'expected_tree_sha':expected}
        path = write('C3_TREE_BATCH_%02d.json'%index, payload)
        plan.append({'index':index,'path':str(path),'characters':len(path.read_bytes().decode('utf-8')),
                     'elements':len(batch),'expected_tree_sha':expected})
    article_sha, subtrees = adapter.tree_digest(rows)
    require(plan[-1]['expected_tree_sha']==article_sha, 'Final plan differs from current bytes')
    write('C3_FILE_IDENTITIES.json', {'article_tree_sha':article_sha,'files':rows,'subtree_hashes':subtrees})
    write('C3_TREE_PLAN.json', plan)
    write('C3_LARGE_BLOBS.json', large)
    scope = {'tested_parent_commit':'8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2',
             'parent_article_tree':before['article_tree_sha'],'article_tree_sha':article_sha,
             'file_count':len(rows),'bytes':sum(r['bytes'] for r in rows),
             'changed_paths':[r['path'] for r in changed], 'removed_paths':[],
             'frozen_inputs_unchanged':True,'source_manifest_sha256':MANIFEST_SHA,
             'source_input_files':1408,'workflow_sha256':WORKFLOW_SHA,
             'manifest_verification':manifest_result,
             'new_blob_uploads':len(large),'new_blob_upload_bytes':sum(r['bytes'] for r in large),
             'tree_batches':len(plan)}
    write('C3_DELTA_SCOPE.json', scope)
    print(json.dumps({k:v for k,v in scope.items() if k not in ('changed_paths','manifest_verification')}))

if __name__=='__main__':
    main()
