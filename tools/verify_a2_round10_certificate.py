#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cert=json.loads((ROOT/'revision/round10-referee-final/A2_ROUND10_CERTIFICATE.json').read_text())
lo,hi=cert['radius_interval']; step=cert['subdivision_width']
def determinant(r: float) -> float:
    return 4+4*r-6*math.sqrt(3)*r-4*math.sqrt(1-(1+math.sqrt(3))*r+2*r*r)
def derivative(r: float) -> float:
    h=1e-7
    return (determinant(r+h)-determinant(r-h))/(2*h)
n=math.ceil((hi-lo)/step); minimum=1e100; maxder=0.0
for j in range(n+1):
    r=min(hi,lo+j*step)
    minimum=min(minimum,abs(determinant(r)))
    maxder=max(maxder,abs(derivative(r)))
certified=minimum-maxder*step
assert certified>cert['verified_bounds']['arithmetic_determinant_abs_lower'], (certified,minimum,maxder)
assert 1.0-2*hi>0 and 1.0-math.sqrt(3)*hi>0
assert 1-(1+math.sqrt(3))*hi+2*hi*hi>0
print(f'A2_ROUND10_CERTIFICATE_PASS determinant_lower={certified:.6f}')
