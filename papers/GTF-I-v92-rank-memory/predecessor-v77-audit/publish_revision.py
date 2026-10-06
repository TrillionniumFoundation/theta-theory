#!/usr/bin/env python3
"""Prepare checked v77 publication metadata from a qualified native source.

Run after build_revision.py --isolated at the native-source commit.
This command is read-only: it emits the exact generated-file inventory for
Git data publication. It does not move refs, sign releases, or reuse an older
revision's publication script. Publish the generated tree as a direct child
of source_commit, then run the v77 exact-head workflow before assigning the
referee-ready alias. The predecessor publisher is preserved in its archive.
"""
from pathlib import Path
import hashlib
import json
import subprocess
from build_revision import sources, DOCUMENTS

ROOT=Path(__file__).resolve().parent
WORK='revision/general-theta-foundations-i-v77-r50-response-2026-10-04'
READY='revision/general-theta-foundations-i-v77-referee-ready-2026-10-04'
NATIVE='revision/general-theta-foundations-i-v77-native-source-2026-10-04'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    receipt=json.loads((ROOT/'evidence/BUILD_RECEIPT.json').read_text())
    require(receipt['schema']=='gtf77.build/1' and receipt['status']=='success',
            'v77 production receipt required')
    require(receipt['isolated_rebuild'] and receipt['normal_optimized_identical'],
            'isolated or optimized-mode qualification absent')
    require(all(not x for x in receipt['latex_diagnostics'].values()),
            'unresolved typesetting diagnostics')
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    require(source==receipt['source_commit'],'prepare publication at the native-source commit')
    inv=json.loads((ROOT/'evidence/SOURCE_HASHES.json').read_text())
    require(sources(ROOT)==inv,'native source changed after qualification')
    preserve=json.loads((ROOT/'PRESERVATION_MANIFEST.json').read_text())
    repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
    for name,digest in preserve['files'].items():
        previous=repo/preserve['source_root']/name
        require(previous.is_file() and sha(previous)==digest,'predecessor changed: '+name)
    files={}
    for name in DOCUMENTS.values():
        require(sha(ROOT/name)==receipt['documents'][name]['sha256'],'PDF differs: '+name)
        files[name]=sha(ROOT/name)
    for path in sorted((ROOT/'evidence').rglob('*')):
        if path.is_file():files[str(path.relative_to(ROOT))]=sha(path)
    package=json.loads((ROOT/'evidence/PACKAGE_MANIFEST.json').read_text())
    for name,digest in package['packages'].items():
        require(sha(ROOT/'evidence'/name)==digest,'package differs: '+name)
    print(json.dumps({'schema':'gtf77.publication-plan/1','status':'success',
          'source_commit':source,'base_commit':receipt['base_commit'],
          'repository':'TrillionniumFoundation/theta-theory',
          'paper_path':str(ROOT.relative_to(repo)),
          'native_source_branch':NATIVE,'work_branch':WORK,'referee_ready_branch':READY,
          'publication_parent':source,'generated_files':files,
          'documents':receipt['documents'],'source_files':receipt['source_files'],
          'complete_active_labels':receipt['complete_active_labels'],
          'regression_suites':len(receipt['regression']),
          'postpublication_verification':'GITHUB_SHA=<publication> python build_revision.py --verify-published',
          'read_only':True,'human_signature':False},indent=2,sort_keys=True))

if __name__=='__main__':main()
