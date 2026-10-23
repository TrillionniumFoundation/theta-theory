#!/usr/bin/env python3
"""Regenerate the exact 386-file R75 retention map without sealing R76.

Run from any working directory after archiving every changed R75 file under
inputs/r75 at its original relative path. Existing archive copies take
precedence over an unchanged current copy. No missing predecessor bytes are
silently reconstructed or declared irrelevant by this script.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from seal_source import (BASE_COMMIT, BASE_SOURCE_COMMIT, BASE_PATH,
                         BASE_TREE, BASE_MANIFEST, BASE_MANIFEST_SHA256,
                         COMPLETE_PRESERVATION, EXPECTED_PREDECESSOR_FILES,
                         file_identity, git_object, sha256, require)

def main() -> None:
    raw=(ROOT/BASE_MANIFEST).read_bytes()
    require(sha256(raw)==BASE_MANIFEST_SHA256,'Archived R75 manifest differs')
    manifest=json.loads(raw);old={r['path']:r for r in manifest['files']}
    require(len(old)==len(manifest['files']),'Duplicate R75 manifest paths')
    old['SOURCE_MANIFEST.json']={'path':'SOURCE_MANIFEST.json','mode':'100644',
        'bytes':len(raw),'git_blob':git_object('blob',raw),'sha256':sha256(raw)}
    require(len(old)==EXPECTED_PREDECESSOR_FILES,'Wrong predecessor file count')
    rows=[]
    for name,row in sorted(old.items()):
        archive=ROOT/'inputs/r75'/name
        kept=archive if archive.is_file() else ROOT/name
        require(kept.is_file(),'Missing retained R75 file: '+name)
        got=file_identity(kept)
        require(all(got[k]==row[k] for k in ('mode','bytes','git_blob','sha256')),
                'Changed R75 file lacks its exact inputs/r75 archive: '+name)
        rows.append({'predecessor_path':name,
            'current_preserved_path':kept.relative_to(ROOT).as_posix(),
            'bytes':row['bytes'],'git_blob':row['git_blob'],'sha256':row['sha256']})
    record={'file_count':len(rows),'predecessor_commit':BASE_COMMIT,
        'predecessor_path':BASE_PATH,'predecessor_tree':BASE_TREE,
        'source_commit':BASE_SOURCE_COMMIT,'files':rows}
    (ROOT/COMPLETE_PRESERVATION).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    same=sum(r['predecessor_path']==r['current_preserved_path'] for r in rows)
    print(json.dumps({'status':'PRESERVATION_MAP_REFRESHED_NOT_SOURCE_SEALED',
        'old_files':len(rows),'same_path':same,'archived':len(rows)-same,
        'map_sha256':sha256((ROOT/COMPLETE_PRESERVATION).read_bytes())},indent=2))

if __name__=='__main__':main()
