#!/usr/bin/env python3
"""Reject TeX defects, recording one exact byte-preserved legacy advisory."""
from pathlib import Path
import json
import re
import sys
from check_v107 import require

P = Path(__file__).resolve().parents[1]
KNOWN = (
    'Package amsmath Warning: Foreign command \\over;\n'
    '(amsmath)                \\frac or \\genfrac should be used instead\n'
    '(amsmath)                 on input line 21.'
)
PATTERN = re.compile(r'LaTeX Warning|Package [^\n]* Warning|Overfull|undefined|Missing character')


def audit(name):
    require(name in ('main', 'supplement'), 'unexpected document')
    log = (P/'build'/f'{name}.log').read_text()
    recorded = []
    for match in PATTERN.finditer(log):
        start = match.start()
        inherited = (name == 'main' and log.startswith(KNOWN, start)
                     and 'core/253_uniform_positive_residence_persistence.tex'
                     in log[max(0, start-300):start])
        require(inherited, 'unexpected TeX diagnostic: '+log[start:start+300])
        recorded.append({'kind': 'retained_plain_TeX_fraction_advisory',
                         'source': 'core/253_uniform_positive_residence_persistence.tex',
                         'line': 21, 'message': KNOWN,
                         'source_is_byte_preserved': True})
    require(len(recorded) <= 1, 'duplicate inherited advisory')
    return {'document': name, 'unexpected_diagnostics': 0,
            'recorded_inherited_advisories': recorded,
            'formal_proof_certificate': False}


if __name__ == '__main__':
    require(len(sys.argv) == 2, 'usage: audit_v107_texlog.py main|supplement')
    print(json.dumps(audit(sys.argv[1]), indent=2, sort_keys=True))
