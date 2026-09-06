#!/usr/bin/env python3
"""Independent exact-rational probes for A1 v14 (Python standard library only).

No manuscript module or author test helper is imported.  Newton functions
are constructed as the leading coefficient of a Hermite interpolation
polynomial, not by the author's divided-difference implementation.
These are finite diagnostics, not a proof verifier or a priority search.
Usage: python reproduce_review.py --source /path/to/papers/A1-english-v14 \
           --output INDEPENDENT_PROBES.json
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import time

EXPECTED_MANIFEST_BLOB = 'c7995cd0073733257d85f0520e1f889dbe034335'
SUBMISSION = 'ffb9214b0fc7e218d6183c1f81bccb3e47587421'
H = F(16)
checks = 0

def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)

class PolyLog:
    """Finite sum of c*t**a*log(t)**k; continuous at 0 in our test cases."""
    def __init__(self, terms=None):
        self.terms = {key: F(c) for key,c in (terms or {}).items() if c}
    def __add__(self, other):
        if not isinstance(other, PolyLog): other = constant(other)
        d = dict(self.terms)
        for key,c in other.terms.items(): d[key] = d.get(key,F(0)) + c
        return PolyLog(d)
    __radd__ = __add__
    def __neg__(self): return self * F(-1)
    def __sub__(self, other): return self + (-other if isinstance(other,PolyLog) else -F(other))
    def __mul__(self, other):
        if not isinstance(other, PolyLog):
            return PolyLog({k:v*F(other) for k,v in self.terms.items()})
        d = {}
        for (a,k),c in self.terms.items():
            for (b,l),e in other.terms.items():
                key = (a+b,k+l)
                d[key] = d.get(key,F(0)) + c*e
        return PolyLog(d)
    __rmul__ = __mul__
    def __truediv__(self, x): return self * (1/F(x))
    def bound(self):
        # e**y >= y**k/k! gives t**a*|log t|**k <= k!*(2/a)**k.
        return sum(abs(c)*(F(1) if k==0 else F(factorial(k))*(2/a)**k)
                   for (a,k),c in self.terms.items())

def monomial(a, k=0): return PolyLog({(F(a),k):F(1)})
def constant(c): return PolyLog({(F(0),0):F(c)})
ONE = constant(1)
ZERO = constant(0)

class Prior:
    def __init__(self, name, density, atom0=F(0), atom1=F(0)):
        self.name, self.density = name, density
        self.atom0, self.atom1 = F(atom0),F(atom1)
    def mean(self, f):
        p = self.density * f
        integral = sum(c*F((-1)**k*factorial(k))/(a+1)**(k+1)
                       for (a,k),c in p.terms.items())
        at0 = f.terms.get((F(0),0),F(0))
        at1 = sum(c for (a,k),c in f.terms.items() if k==0)
        return integral + self.atom0*at0 + self.atom1*at1

PRIORS = [
    Prior('uniform',ONE),
    Prior('nonuniform-density', (ONE+monomial(1))*F(2,3)),
    Prior('full-support-with-endpoint-atoms',(ONE+monomial(1))/2,F(1,8),F(1,8)),
]

def inverse(matrix):
    n=len(matrix)
    a=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        require(pivot is not None,'matrix invertibility')
        a[j],a[pivot]=a[pivot],a[j]
        scale=a[j][j]; a[j]=[v/scale for v in a[j]]
        for i in range(n):
            if i!=j:
                scale=a[i][j]
                a[i]=[u-scale*v for u,v in zip(a[i],a[j])]
    return [row[n:] for row in a]

def positive_ldl(matrix):
    a=[list(row) for row in matrix]
    for j in range(len(a)):
        require(a[j][j]>0,'positive exact covariance LDL pivot')
        for i in range(j+1,len(a)):
            for k in range(j+1,len(a)):
                a[i][k]-=a[i][j]*a[j][k]/a[j][j]

def hermite_flag(nodes):
    result=[]
    for length in range(1,len(nodes)+1):
        multiplicities=Counter(nodes[:length])
        rows=[(z,k) for z,count in sorted(multiplicities.items()) for k in range(count)]
        matrix=[[F(comb(j,k))*z**(j-k) if j>=k else F(0)
                 for j in range(length)] for z,k in rows]
        functional=inverse(matrix)[-1]
        g=sum((monomial(H*z,k)*(c*H**k/F(factorial(k)))
               for c,(z,k) in zip(functional,rows)),ZERO)
        result.append(g)
    return result

def leja(nodes):
    remaining=list(enumerate(nodes)); ordered=[]; scales=[]
    while remaining:
        scored=[(abs(prod(z-v for v in ordered)), -i, j)
                for j,(i,z) in enumerate(remaining)]
        # The first node is the least one, with label tie breaking.
        j=min(range(len(remaining)),key=lambda j:(remaining[j][1],remaining[j][0])) if not ordered else max(scored)[2]
        _,z=remaining.pop(j)
        scales.append(abs(prod(z-v for v in ordered))); ordered.append(z)
    return ordered,scales

def prod(values):
    ans=F(1)
    for x in values: ans*=x
    return ans

def raw_nodes(exponents):
    # Symmetric degree-two formal labels; exclude the all-constant label.
    return [(exponents[i]+exponents[j])/H for i in range(len(exponents))
            for j in range(i,len(exponents)) if i or j]

def covariance_probe(exponents, prior, nonconstant, use_leja):
    nodes=raw_nodes(exponents)
    ordered,d=leja(nodes)
    if not use_leja:
        # Interleave equal nodes instead of treating repeats as adjacent blocks.
        ordered=nodes[1::2]+nodes[::2]
    phi=hermite_flag(ordered); q=len(phi)
    likelihood=((ONE/2+monomial(exponents[1])/64)*
                (ONE/2-monomial(exponents[-1])/64)) if nonconstant else ONE/4
    z=prior.mean(likelihood)
    require(F(0)<z<=1,'history probability')
    def nu(f): return prior.mean(likelihood*f)/z
    means=[nu(g) for g in phi]
    centered=[g-m for g,m in zip(phi,means)]
    gamma=[[nu(f*g) for g in centered] for f in centered]
    positive_ldl(gamma)
    inv=inverse(gamma)
    # Verify the *full* matrix inverse, not merely one solved direction.
    for i in range(q):
        for j in range(q):
            require(sum(gamma[i][k]*inv[k][j] for k in range(q))==F(i==j),'inverse identity')
    c0=max(F(1),sum(abs(inv[i][j])*centered[j].bound() for i in range(q) for j in range(q)))
    epsilon=F(1,4); step=epsilon/(4*c0)
    vectors=[[F(j==i) for j in range(q)] for i in range(q)]
    vectors += [[F((-1)**i) for i in range(q)], [F(-1)]*q]
    queries=[ONE/2]+[ONE/2+monomial(a)/64 for a in exponents[1:]]
    physical=[a*b for a,b in product(queries,repeat=2)]
    raw=[monomial(H*z) for z in ordered]
    # Independent Newton interpolation identity, valid also in non-Leja order.
    for node in ordered:
        reconstructed=sum((g*prod(node-u for u in ordered[:j]) for j,g in enumerate(phi)),ZERO)
        require(reconstructed.terms==monomial(H*node).terms,'Hermite/Newton reconstruction')
    bad_normalization_detected=False
    for v in vectors:
        weights=[sum(v[i]*inv[i][j] for i in range(q)) for j in range(q)]
        f=sum((c*g for c,g in zip(weights,centered)),ZERO)
        require(nu(f)==0,'posterior centering')
        require(f.bound()<=c0,'analytic sup-norm envelope')
        for j,g in enumerate(phi): require(nu(g*f)==v[j],'simultaneous covariance direction')
        prior_den=1+step*prior.mean(f)
        ratio=(ONE+f*step)/prior_den
        require(prior.mean(ratio)==1,'pulled-back prior total mass')
        require(2*step*c0/(1-step*c0)<=epsilon,'relative prior envelope')
        require(1-step*c0>0,'positive density lower bound')
        new_z=prior.mean(ratio*likelihood)
        require(new_z==z/prior_den,'Bayes evidence normalization')
        def new_nu(g): return prior.mean(ratio*likelihood*g)/new_z
        for j,g in enumerate(phi): require(new_nu(g)-means[j]==step*v[j],'exact posterior moment shift')
        raw_shift=[new_nu(g)-nu(g) for g in raw]
        if use_leja:
            for row,node in enumerate(ordered):
                expected=step*sum(prod(node-u for u in ordered[:j])*v[j] for j in range(q))
                require(raw_shift[row]==expected,'physical L D shift including zero pivots')
            if sum(bool(x) for x in v)==1:
                j=next(i for i,x in enumerate(v) if x)
                require(all(x==0 for x in raw_shift[:j]),'exact raw-prefix advice')
                if d[j]: require(raw_shift[j]!=0,'active direction really changes a raw moment')
                else: require(all(x==0 for x in raw_shift),'inactive zero-pivot direction physically invisible')
        shifts=[new_nu(query)-nu(query) for query in physical]
        for query,shift in zip(physical,shifts):
            require(shift==step*nu(query*f),'physical product-query probability shift')
        require(any(raw_shift)==any(shifts),'spanning physical queries detect exactly raw shifts')
        if prior.mean(f):
            require(prior.mean(ONE+f*step)!=1,'negative control: omitting prior normalization fails')
            bad_normalization_detected=True
    if nonconstant: require(bad_normalization_detected,'nonconstant history exposes normalization error')
    else: require(not bad_normalization_detected,'constant-history pullback denominator equals one')
    # The upper inclusion is tested using an independent admissible prior tilt.
    tilt=(monomial(1)-prior.mean(monomial(1)))*epsilon
    require(prior.mean(tilt)==0,'outer-test prior normalized')
    for g,m in zip(phi,means):
        displacement=(nu((ONE+tilt)*g)/(1+nu(tilt)))-m
        require(displacement==nu(tilt*(g-m))/(1+nu(tilt)),'outer inclusion exact Bayes identity')
        require(abs(displacement)<=4*g.bound()*epsilon,'outer coordinate bound')
    return {'q':q,'distinct_nodes':len(set(ordered)),'prior':prior.name,
            'history':'two-nonconstant-failures' if nonconstant else 'two-constant-failures',
            'order':'Leja' if use_leja else 'interleaved',
            'exponents':[str(a) for a in exponents],
            'normalization_negative_control_detected':bad_normalization_detected}

def determinant_probe(exponents):
    nodes=raw_nodes(exponents); ordered,d=leja(nodes)
    require(all(d[i]>=d[i+1] for i in range(len(d)-1)),'decreasing Leja scales')
    for ell in range(1,len(nodes)+1):
        volume=max(prod(abs(nodes[i]-nodes[j]) for i,j in combinations(indices,2))
                   for indices in combinations(range(len(nodes)),ell))
        prefix=prod(d[:ell])
        require(prefix<=volume<=factorial(ell)*prefix,'maximal determinant-volume comparison')
        require((volume==0)==(ell>len(set(nodes))),'exact collision rank')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); start=time.monotonic()
    manifest_bytes=(args.source/'SOURCE_MANIFEST.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(manifest_bytes)).encode()+b'\0'+manifest_bytes).hexdigest()
    require(blob==EXPECTED_MANIFEST_BLOB,'source manifest anchored to submission')
    manifest=json.loads(manifest_bytes)
    for name,digest in manifest['files'].items():
        require(hashlib.sha256((args.source/name).read_bytes()).hexdigest()==digest,'source hash: '+name)
    for prior in PRIORS: require(prior.mean(ONE)==1,'base prior normalization')
    configurations=[[F(0),F(1),F(2)+theta] for theta in [F(0),F(1,16),F(-1,32),F(1,1024)]]
    configurations += [[F(0),F(1),F(2),F(3)]]
    cases=[]
    for exponents in configurations:
        determinant_probe(exponents)
        for prior,nonconstant,use_leja in product(PRIORS,[False,True],[True,False]):
            cases.append(covariance_probe(exponents,prior,nonconstant,use_leja))
    # Exact profile checks for the three-trial separation example.
    profile_checks=[]
    for theta in [F(0),F(1,16),F(-1,32),F(1,1024)]:
        exponents=[F(0),F(1),F(2)+theta]
        nodes=raw_nodes(exponents); _,d=leja(nodes)
        require((d[-1]==0)==(theta==0),'last ambiguity width vanishes exactly at collision')
        for budget in [1,2,8,64,1024,10**6]:
            # Both checkpoints have prefix length 2; their maximum volume is the two-trial diameter.
            xi=max(F(1,budget**2),(max(nodes)-min(nodes))/budget)
            require(F(1,8*budget)<=xi<=F(1,budget),'collision-uniform M^-1 profile')
        if theta: profile_checks.append({'theta':str(theta),'d5_over_abs_theta':str(d[-1]/abs(theta))})
    result={'submission_commit':SUBMISSION,'manifest_git_blob':blob,
            'source_files_verified':len(manifest['files']),'passed':True,
            'assertions':checks,'cases':len(cases),'case_details':cases,
            'profile_diagnostics':profile_checks,
            'normalization_negative_controls':sum(c['normalization_negative_control_detected'] for c in cases),
            'seconds':round(time.monotonic()-start,3),
            'scope':'Finite exact-rational diagnostics; no author helper imported. Includes nonuniform full-support priors, endpoint atoms, nonconstant histories, interleaved repeated nodes and simultaneous additive collisions. Not formal proof verification or a continuum numerical test.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('case_details',)},indent=2))

if __name__=='__main__': main()
