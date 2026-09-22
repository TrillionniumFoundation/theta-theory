#!/usr/bin/env python3
"""Finite regressions for the structural revision; not a theorem verifier."""
from __future__ import annotations
import argparse, itertools, json, math
from fractions import Fraction as F

MUTANTS = ['uncharged_vertices','broken_prepend','erased_noise_floor',
           'closed_mean_only','constant_histogram','wrong_budget_power']
COUNT=0

def check(ok: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not ok:
        raise RuntimeError('FAILED: '+message)

def children(v:tuple[int,...], markov:bool):
    return [v+(i,) for i in (0,1) if not(markov and v and v[-1]==i==1)]

def mass(v,markov):
    if not v:return F(1)
    if not markov:
        return math.prod((F(1,3),F(2,3))[i] for i in v)
    out=(F(2,3),F(1,3))[v[0]]
    for i,j in zip(v,v[1:]):out*=((F(1,2),F(1,2)),(F(1),F(0)))[i][j]
    return out

def energy(v,markov):return mass(v,markov)*F(1,4)**len(v)

def tree_at(budget,markov):
    vertices={()};internal=set();leaves={()}
    while True:
        v=min(leaves,key=lambda x:(-energy(x,markov),x))
        cs=children(v,markov)
        if len(leaves)+len(cs)-1>budget:break
        internal.add(v);leaves.remove(v);leaves.update(cs);vertices.update(cs)
    return vertices,internal,leaves

def parse(word,internal,leaves):
    for k in range(len(word)+1):
        v=word[:k]
        if v in leaves:return v
        if v not in internal:raise RuntimeError('invalid parse')
    return word

def tree_checks(mutant):
    profiles={}
    for markov in (False,True):
        rows=[]
        for budget in (1,2,3,4,7,12,25,51,100):
            verts,ints,leaves=tree_at(budget,markov)
            counted=len(leaves) if mutant=='uncharged_vertices' else len(verts)
            check(counted==1+sum(len(children(v,markov)) for v in ints),'exact whole-tree state count')
            check(len(verts)<=(2 if markov else 1)*(2*len(leaves)-1),'unary state bound')
            theta=max(energy(v,markov) for v in leaves)
            for v in leaves:check(energy(v,markov)>=F(1,12)*theta,'balanced energies')
            for v in verts:
                for k in range(len(v)+1):check(v[k:] in verts,'full suffix closure')
                if v in ints:
                    for k in range(1,len(v)+1):check(v[k:] in ints,'internal suffix closure')
                if v:
                    check(energy(v,markov)<energy(v[1:],markov),'strict prefix energy drop')
            if budget>=3:
                for hist in itertools.product((0,1),repeat=9):
                    if markov and any(hist[k]==hist[k+1]==1 for k in range(8)):continue
                    state=()
                    for t,new in enumerate(hist):
                        candidate=(new,)+state
                        state=parse(candidate,ints,leaves)
                        if mutant=='broken_prepend' and state:state=state[:-1]
                        expected=parse(tuple(reversed(hist[:t+1])),ints,leaves)
                        check(state==expected,'prepend update equals direct past encoding')
            rows.append({'leaves':len(leaves),'states':len(verts),'profile':float(sum(energy(v,markov) for v in leaves))})
        profiles['golden_mean' if markov else 'bernoulli']=rows
    # The tilted cut identity is exact at s=1/2 for p0=p1=1/2, r^2=1/2.
    for depth in range(1,12):check(F(2)**depth*F(1,2)**depth==1,'tilted full-cut mass')
    return profiles

def w1_discrete(a,b):
    points=sorted({x for x,w in a+b});aa={};bb={}
    for x,w in a:aa[x]=aa.get(x,F(0))+w
    for x,w in b:bb[x]=bb.get(x,F(0))+w
    ca=cb=F(0);out=F(0)
    for j,x in enumerate(points[:-1]):
        ca+=aa.get(x,F(0));cb+=bb.get(x,F(0));out+=abs(ca-cb)*(points[j+1]-x)
    return out

def qmeasure(atoms,n):
    atoms=sorted(atoms);out=[]
    for j in range(n):
        target=F(2*j+1,2*n);s=F(0)
        for x,w in atoms:
            s+=w
            if s>=target:break
        scaled=x*n;lo=scaled.numerator//scaled.denominator
        k=lo+int(scaled-lo>F(1,2));out.append((F(k,n),F(1,n)))
    return out

def update(atoms,y):
    return [(F(3*b,5)+x/5+x*x/50,w*(F(3,4) if b==y else F(1,4)))
            for x,w in atoms for b in (0,1)]

def posterior_checks(mutant):
    for eps in (F(0),F(1,10),F(1,4),F(1,2)):
        floor=F(0) if mutant=='erased_noise_floor' else eps*(1-eps)
        direct=sum(F(1,2)*a*(1-a) for a in (eps,1-eps))
        check(floor==direct,'noise floor from actual conditional law')
    for n in range(1,12):
        check(math.comb(2*n,n)<=4**n,'finite measure codebook count')
        exact=[(F(0),F(1,2)),(F(1),F(1,2))];approx=qmeasure(exact,n)
        for y in (0,1,1,0,1):
            before=w1_discrete(exact,approx)
            e=update(exact,y);a=update(approx,y)
            check(w1_discrete(e,a)<=F(6,25)*before,'same-report measure contraction')
            approx=qmeasure(a,n);exact=e
            check(w1_discrete(a,approx)<=F(3,2*n),'charged quantile projection radius')
            check(w1_discrete(exact,approx)<=F(6,25)*before+F(3,2*n),'recursive approximation bound')
    # Same first moment, different second moment: next mean differs in the nonlinear model.
    a=[(F(0),F(1,2)),(F(1),F(1,2))];b=[(F(1,2),F(1))]
    check(sum(x*w for x,w in a)==sum(x*w for x,w in b),'equal old means')
    ma=sum(x*w for x,w in update(a,0));mb=sum(x*w for x,w in update(b,0))
    if mutant=='closed_mean_only':mb=ma
    check(ma!=mb and ma-mb==F(1,200),'mean closure is false, measure closure is real')

def normal_cdf(x):return (1+math.erf(x/math.sqrt(2)))/2

def density(u,mean):
    x=math.tan(math.pi*(u-.5))
    return math.exp(-(x-mean)**2/2)/math.sqrt(2*math.pi)*math.pi*(1+x*x)

def histogram_errors(J,mean):
    edges=[-math.inf]+[math.tan(math.pi*(i/J-.5)) for i in range(1,J)]+[math.inf]
    masses=[normal_cdf(edges[i+1]-mean)-normal_cdf(edges[i]-mean) for i in range(J)]
    check(abs(sum(masses)-1)<1e-12,'Gaussian cell masses normalize')
    tent=constant=0.;steps=32768
    for k in range(steps):
        u=(k+.5)/steps;x=J*u-.5;lo=math.floor(x);s=x-lo
        g=J*((1-s)*masses[lo%J]+s*masses[(lo+1)%J])
        h=J*masses[min(int(u*J),J-1)];p=density(u,mean)
        tent+=abs(g-p);constant+=abs(h-p)
    return tent/(2*steps),constant/(2*steps)

def gaussian_checks(mutant):
    rows=[]
    for mean in (0.,.7):
        errors=[histogram_errors(J,mean) for J in (32,64,128)]
        chosen=[e[1] if mutant=='constant_histogram' else e[0] for e in errors]
        check(chosen[0]/chosen[1]>3.5 and chosen[1]/chosen[2]>3.5,'positive reconstruction is second order, not first order')
        rows.append({'mean':mean,'tent_tv':[round(e[0],10) for e in errors],
                     'constant_tv':[round(e[1],10) for e in errors]})
    for J in (2,3,7,21):
        for k in range(100):
            u=F(2*k+1,200);x=J*u-F(1,2);lo=x.numerator//x.denominator;s=x-lo
            check((1-s)+s==1,'positive interpolation unity')
            check((1-s)*F(2*lo+1,2*J)+s*F(2*(lo+1)+1,2*J)==u,'affine reproduction including periodic lifts')
    for r in range(1,7):
        budget_exp=F(r,4) if mutant=='wrong_budget_power' else F(r,10)
        check(budget_exp*F(2,r)==F(1,5),'matched N^(-1/5) label exponent')
        check(F(r,6)*F(3,r)==F(1,2),'joint-window balance')
    return rows

def poisson_checks():
    rows=[]
    for mu in (64.,256.,1024.,4096.):
        lo=max(0,int(mu-10*math.sqrt(mu)-2));hi=int(mu+10*math.sqrt(mu)+2)
        total=0.;sub=16
        for k in range(lo,hi+1):
            mass=math.exp(-mu+k*math.log(mu)-math.lgamma(k+1))
            for j in range(sub):
                x=k-.5+(j+.5)/sub
                normal=math.exp(-(x-mu)**2/(2*mu))/math.sqrt(2*math.pi*mu)
                total+=abs(mass-normal)/sub
        tv=total/2
        check(tv*math.sqrt(mu)<1.,'jittered Poisson local-normal finite diagnostic')
        rows.append({'mean':mu,'tv_quadrature':round(tv,10),'scaled_tv':round(tv*math.sqrt(mu),10)})
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=MUTANTS);args=parser.parse_args()
    try:
        profiles=tree_checks(args.mutant);posterior_checks(args.mutant)
        gaussian=gaussian_checks(args.mutant);poisson=poisson_checks()
        check(args.mutant is None,'mutant unexpectedly survived all designated controls')
        print(json.dumps({'status':'passed','finite_checks':COUNT,'tree_profiles':profiles,
            'positive_reconstruction':gaussian,'poisson_quadrature':poisson,
            'scope':'Finite identities and deterministic regression diagnostics, not formal or independent proof validation.'},sort_keys=True,indent=2))
    except RuntimeError as exc:
        print(str(exc));raise SystemExit(1)
if __name__=='__main__':main()
