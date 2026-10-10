#!/usr/bin/env python3
"""Intentional source-manifest refresh, never called by verification/build."""
import json
from verify import ROOT,sources,sha256,git_hash
files={}
for name in sources():
    data=(ROOT/name).read_bytes()
    files[name]={'bytes':len(data),'sha256':sha256(data),'git_blob_sha':git_hash('blob',data)}
(ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps({'version':1,'scope':'native r6 sources, excluding evidence and build artifacts','files':files},sort_keys=True,indent=2)+'\n')
