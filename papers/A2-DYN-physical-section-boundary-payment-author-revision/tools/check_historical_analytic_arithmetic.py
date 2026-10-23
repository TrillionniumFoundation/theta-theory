#!/usr/bin/env python3
"""Exact scalar checks only; these do not validate the dynamical hypotheses."""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
checks = []
def check(name, value, expected=None):
    ok = value == expected if expected is not None else bool(value)
    checks.append({'name': name, 'actual': str(value), 'expected': str(expected), 'passed': ok})
    assert ok, name

alpha, beta = F(129, 128), F(17, 16)
check('long-left endpoint exponent', F(63,64)+F(7,8)*F(1,32), F(259,256))
check('long-left endpoint surplus', F(259,256)-alpha, F(1,256))
check('long-left incidence surplus', F(3,2)*F(31,32)-beta, F(25,64))
check('long-right initial coefficient', F(7,8)*F(1,32)+F(31,32), F(255,256))
check('long-right endpoint exponent', F(255,256)+F(1,32), F(263,256))
check('long-right endpoint surplus', F(263,256)-alpha, F(5,256))
check('long-right incidence exponent', F(47,32)*F(31,32)*F(3,4), F(4371,4096))
check('long-right incidence surplus', F(4371,4096)-beta, F(19,4096))
check('uncut first moment leading exponent', alpha-1, F(1,128))
check('critical height square-radius exponent', (alpha-1)/2, F(1,256))
check('outer epsilon leading rate', F(1,12)*F(1,16), F(1,192))
check('outer growing-balance rate', F(1,12)*(F(1,16)-F(1,32)), F(1,384))
check('whole-arm paid deficit exponent', F(3)-F(1,32), F(95,32))
for p in [F(1), F(257,256), F(129,128)]:
    a, b = (4-2*p)/3, (2*p-1)/3
    check('two-cap m^2 exponent sum at '+str(p), a+b, F(1))
    check('two-cap crossover E exponent at '+str(p), F(2,3)*(2-p), a)
    check('two-cap crossover H exponent at '+str(p), 1-F(2,3)*(2-p), b)
check('p=1 is below alpha', F(1)<alpha)
check('p=alpha leading layer integral is excluded', not (alpha<alpha))
for dm in range(1,21):
    for dp in range(1,21):
        h, left, right = F(1), F(dm,10), F(dp,10)
        if left+right >= h:
            assert min(h,left)+min(h,right) >= h
checks.append({'name':'persistence rational diagnostics (not a continuum proof)', 'passed':True})
out={'scope':'Exact scalar/rational identity checks. No spectral, geometric, limit-exchange or physical-source theorem certified.', 'checks':checks, 'all_passed':all(x['passed'] for x in checks)}
path=args.output
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'output':str(path),'checks':len(checks),'all_passed':out['all_passed']}))
