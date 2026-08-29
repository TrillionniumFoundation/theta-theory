#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, math, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors=[]

def req(cond,msg):
    if not cond: errors.append(msg)

paper_dirs=sorted([p for p in (ROOT/'papers').iterdir() if p.is_dir()])
req(len(paper_dirs)==5, f'exactly five papers required, found {len(paper_dirs)}')
for p in paper_dirs:
    names={x.name for x in p.iterdir() if x.is_file()}
    req('main.tex' in names, f'{p.name}: missing main.tex')
    req('references.bib' in names, f'{p.name}: missing references.bib')
    req(not any(re.search(r'(main-(v|final|round|submission)|references-)',n,re.I) for n in names), f'{p.name}: historical filename present')

for a in (-0.9,-0.4,0.0,0.4,0.9):
    w=[(1-a)/6,(1-a)/3,3*(1+a)/14,2*(1+a)/7]
    req(all(x>0 for x in w), f'weights not positive at {a}')
    req(abs(sum(w)-1)<1e-12, f'weights do not sum to one at {a}')
    d=[(2,0),(-1,0),(0,4),(0,-3)]
    mean=[sum(w[i]*d[i][j] for i in range(4)) for j in range(2)]
    req(max(abs(x) for x in mean)<1e-12, f'impulses not centered at {a}')
    C=[[sum(w[i]*d[i][r]*d[i][c] for i in range(4)) for c in range(2)] for r in range(2)]
    target=[[1-a,0],[0,6*(1+a)]]
    req(max(abs(C[r][c]-target[r][c]) for r in range(2) for c in range(2))<1e-12, f'covariance mismatch at {a}')
    tau=sum(w[i]*(2 if i<2 else 1) for i in range(4))
    req(abs(tau-(3-a)/2)<1e-12, f'roof mismatch at {a}')

# Base preparation and theta/rate derivative.
a0=0.4
w0=[(1-a0)/6,(1-a0)/3,3*(1+a0)/14,2*(1+a0)/7]
req(max(abs(w0[i]-[.1,.2,.3,.4][i]) for i in range(4))<1e-12,'base weights mismatch')
for a in (-0.8,-0.2,0.2,0.7):
    theta=.5*math.log(3*(1+a)/(7*(1-a)))
    Z=.3*math.exp(-theta)+.7*math.exp(theta)
    mean=(.7*math.exp(theta)-.3*math.exp(-theta))/Z
    req(abs(mean-a)<1e-12,f'theta inversion mismatch at {a}')
    h=1e-7
    def rate(x):
        q=(1+x)/2
        return q*math.log(q/.7)+(1-q)*math.log((1-q)/.3)
    deriv=(rate(a+h)-rate(a-h))/(2*h)
    req(abs(deriv-theta)<2e-7,f'rate derivative mismatch at {a}')

# Canonical branch weights equal driven weights.
for a in (-0.7,0.1,0.8):
    theta=.5*math.log(3*(1+a)/(7*(1-a)))
    base=[.1,.2,.3,.4]
    c=[-1,-1,1,1]
    z=sum(base[i]*math.exp(theta*c[i]) for i in range(4))
    tilt=[base[i]*math.exp(theta*c[i])/z for i in range(4)]
    driven=[(1-a)/6,(1-a)/3,3*(1+a)/14,2*(1+a)/7]
    req(max(abs(tilt[i]-driven[i]) for i in range(4))<1e-12,f'driven tilt mismatch at {a}')

result={
 'status':'PASS' if not errors else 'FAIL',
 'paper_count':len(paper_dirs),
 'checks':{
   'active_tree_hygiene': not any('historical filename' in e for e in errors),
   'weights': not any('weights' in e for e in errors),
   'centering_and_covariance': not any(('centered' in e or 'covariance' in e) for e in errors),
   'roof': not any('roof' in e for e in errors),
   'theta_rate_duality': not any(('theta' in e or 'rate derivative' in e) for e in errors),
   'canonical_driven_identity': not any('driven tilt' in e for e in errors),
 },
 'errors':errors,
 'scope':'Finite-dimensional formulas and repository structure only; does not certify analytical proofs or peer review.'
}
(ROOT/'status'/'VERIFICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(1 if errors else 0)
