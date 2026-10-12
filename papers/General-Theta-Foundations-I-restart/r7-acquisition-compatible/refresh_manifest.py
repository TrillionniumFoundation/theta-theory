#!/usr/bin/env python3
"""Explicit authoring operation; verification/build never refreshes the manifest."""
import json
from verify import ROOT, sources, sha256, git_hash

files = {}
for name in sources():
    data = (ROOT / name).read_bytes()
    files[name] = {'sha256': sha256(data), 'git_blob_sha': git_hash('blob', data)}
(ROOT / 'SOURCE_MANIFEST.json').write_text(json.dumps({
    'schema': 1,
    'scope': 'R7 native sources, excluding artifacts/evidence and this self-excluded manifest',
    'files': files,
}, sort_keys=True, indent=2) + '\n')
