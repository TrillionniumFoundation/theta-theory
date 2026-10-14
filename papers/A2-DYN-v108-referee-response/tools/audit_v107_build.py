#!/usr/bin/env python3
"""Check recorder coverage; render every main page for inspection."""
from pathlib import Path
import json
import subprocess
from check_v107 import require
P = Path(__file__).resolve().parents[1]
seen = set()
for document in ('main', 'supplement'):
    for line in (P/'build'/f'{document}.fls').read_text().splitlines():
        if line.startswith('INPUT '):
            seen.add((P/line[6:]).resolve())
core = set(p.resolve() for p in (P/'core').glob('*.tex'))
require(len(core) == 257, 'active core count')
require(core <= seen, 'core modules not read: '+str(sorted(str(p) for p in core-seen)))
subprocess.run(['pdftoppm', '-scale-to', '1200', '-png', str(P/'build/main.pdf'),
                str(P/'evidence/main')], check=True)
subprocess.run(['pdftotext', '-layout', str(P/'build/main.pdf'), str(P/'evidence/main.txt')], check=True)
text = (P/'evidence/main.txt').read_text()
require('??' not in text, 'unresolved PDF references')
require('Two-ended comparison' in text and 'Unallocated capacity' in text, 'new sections missing')
print(json.dumps({'recorded_core_modules': len(core), 'main_pages_rendered':
                  len(list((P/'evidence').glob('main-*.png'))),
                  'formal_proof_certificate': False}, sort_keys=True, indent=2))
