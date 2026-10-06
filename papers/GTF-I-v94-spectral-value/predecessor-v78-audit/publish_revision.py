#!/usr/bin/env python3
"""Prepare checked v78 publication metadata from a qualified native source.

Run after build_revision.py --isolated at the actual native-source commit.
This read-only command emits the exact generated-file inventory for Git data
publication. Publish that tree as a direct child of source_commit, then run
the v78 exact-head workflow before moving the referee-ready alias. A further
metadata-only child requires its own exact-head run. No refs are changed here.
"""
from pathlib import Path
import hashlib
import json
from build_revision import (DOCUMENTS, FINAL_REQUEST, WORKFLOW, committed_inventory,
                            git_output, require, verify_artifacts)

ROOT=Path(__file__).resolve().parent
WORK='revision/general-theta-foundations-i-v78-r51-response-2026-10-04'
READY='revision/general-theta-foundations-i-v78-referee-ready-2026-10-04'
NATIVE='revision/general-theta-foundations-i-v78-native-source-2026-10-04'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt,inventory,_=verify_artifacts(ROOT)
    source=git_output(ROOT,'rev-parse','HEAD')
    require(source==receipt['source_commit'],'prepare publication at the qualified native-source commit')
    repo=committed_inventory(ROOT,source,inventory)
    require(not git_output(ROOT,'status','--porcelain','--untracked-files=no'),
            'tracked native source must remain clean while preparing publication')
    require((repo/WORKFLOW).is_file(),'v78 exact-head workflow is missing from the native object')
    require(not (repo/FINAL_REQUEST).exists(),'a final-head request cannot precede publication')
    preserve=json.loads((ROOT/'PRESERVATION_MANIFEST.json').read_text())
    predecessor_inventory=repo/preserve['source_root']/'evidence/SOURCE_HASHES.json'
    require(sha(predecessor_inventory)==preserve['source_inventory_sha256']
            and json.loads(predecessor_inventory.read_text())==preserve['files'],
            'preservation inventory differs from the reviewed v77 inventory')
    for name,digest in preserve['files'].items():
        previous=repo/preserve['source_root']/name
        require(previous.is_file() and sha(previous)==digest,'predecessor changed: '+name)
    files={name:sha(ROOT/name) for name in DOCUMENTS.values()}
    for path in sorted((ROOT/'evidence').rglob('*')):
        if path.is_file():files[path.relative_to(ROOT).as_posix()]=sha(path)
    print(json.dumps({'schema':'gtf78.publication-plan/1','status':'success',
          'source_commit':source,'base_commit':receipt['base_commit'],
          'repository':'TrillionniumFoundation/theta-theory',
          'paper_path':ROOT.relative_to(repo).as_posix(),
          'native_source_branch':NATIVE,'work_branch':WORK,'referee_ready_branch':READY,
          'publication_parent':source,'generated_files':files,
          'documents':receipt['documents'],'source_files':receipt['source_files'],
          'complete_active_labels':receipt['complete_active_labels'],
          'active_document_labels':receipt['active_document_labels'],
          'regression_suites':len(receipt['regression']),
          'standalone_journal_rebuild':receipt['standalone_journal_rebuild'],
          'postpublication_verification':'GITHUB_SHA=<exact-publication-or-final-child> python build_revision.py --verify-published',
          'optional_final_child_request':FINAL_REQUEST,
          'final_alias_rule':'Move the referee-ready alias only to an exact head with a successful read-only reconstruction run.',
          'read_only':True,'human_signature':False,
          'independent_human_priority_review_obtained':False},indent=2,sort_keys=True))


if __name__=='__main__':main()
