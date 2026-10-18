#!/usr/bin/env python3
"""Create an ordinary-source inventory before the source commit; not a verifier."""
from pathlib import Path
import hashlib,json
from verify import ROOT,ordinary_files
files=ordinary_files()
(ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps({'format':1,'scope':'all ordinary native files, excluding this manifest, artifacts and final evidence','files':{n:hashlib.sha256(d).hexdigest() for n,d in files.items()}},sort_keys=True,indent=2)+'\n')
