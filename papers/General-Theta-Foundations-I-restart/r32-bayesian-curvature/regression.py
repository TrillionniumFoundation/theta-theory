#!/usr/bin/env python3
"""Finite exact algebra and floating sanity; not proofs of the continuum theorems."""
from __future__ import annotations
import argparse,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
COUNTS={'exact_rational_cases':0,'finite_integer_cases':0,'floating_sanity_cases':0}
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def done(kind):COUNTS[kind]+=1

def bayes_cases():
    configurations=[[(F(-3,4),F(1,4),0),(F(-1,4),F(1,4),0),(F(1,4),F(1,4),1),(F(3,4),F(1,4),1)],
        [(F(-1),F(1,3),0),(F(0),F(1,3),0),(F(1),F(1,3),0)],
        [(F(-4,5),F(1,5),0),(F(1,5),F(1,5),1),(F(3,5),F(3,5),1)],
        [(F(-1,2),F(1,2),0),(F(1,2),F(1,2),1)]]
    rules=list(itertools.product((F(0),F(1)),repeat=4))+list(itertools.product((F(1,3),F(2,3)),repeat=4))
    for beta,eta in itertools.product((F(1,5),F(3,5),F(9,10)),(F(1,4),F(1,2),F(3,4))):
        ell=lambda y,x:(1+eta*y*x)/2
        post=lambda y,x:beta*(x+eta*y)/(1+eta*y*x)
        phi=lambda x:sum(ell(y,x)*post(y,x)**2 for y in (-1,1))
        for conf in configurations:
            mass={s:sum(p for x,p,ss in conf if ss==s) for s in (0,1)}
            means={s:sum(p*x for x,p,ss in conf if ss==s)/v for s,v in mass.items() if v}
            for rule in rules:
                atoms=[]
                for x,p,s in conf:
                    for yi,y in enumerate((-1,1)):
                        z=post(y,x);w=post(y,means[s]);prob=rule[2*s+yi]
                        for j,kprob in ((0,1-prob),(1,prob)):
                            q=p*ell(y,x)*kprob
                            if q:atoms.append((q,s,j,z,w))
                pair={};out={}
                for q,s,j,z,w in atoms:
                    pq,pw=pair.get((s,j),(F(0),F(0)));pair[s,j]=(pq+q,pw+q*w)
                    oq,ow=out.get(j,(F(0),F(0)));out[j]=(oq+q,ow+q*w)
                c={k:w/q for k,(q,w) in pair.items()};v={k:w/q for k,(q,w) in out.items()}
                row=sum(q*(w-c[s,j])**2 for q,s,j,z,w in atoms)
                pool=sum(q*(c[s,j]-v[j])**2 for q,s,j,z,w in atoms)
                residual=sum(q*(z-v[j])**2 for q,s,j,z,w in atoms)
                old=sum(p*phi(x) for x,p,s in conf)-sum(mass[s]*phi(u) for s,u in means.items())
                require(old>=0 and row>=0 and pool>=0,'nonnegative defects')
                require(residual==old+row+pool,'normalized Bayes row/pooling identity')
                for j in out:
                    actual=sum(q*z for q,s,jj,z,w in atoms if jj==j)/out[j][0]
                    require(actual==v[j],'likelihood-reweighted barycenter')
                done('exact_rational_cases')
    for eta in (F(1,10),F(1,3),F(4,5)):
        require(eta*eta>0,'informative report creates energy')
        # Exact endpoint/center potential, including a boundary posterior.
        phi=lambda x:sum((x+eta*y)**2/(2*(1+eta*y*x)) for y in (-1,1))
        require(phi(0)==eta*eta and phi(1)==1 and phi(-1)==1,'binary potential')
        done('exact_rational_cases')

def budget_cases():
    z=F(1,2)
    for n in range(1,41):
        for M in range(n+1,n+122):
            B=M-n-1
            widths=[1+(B*(1-z)*z**(n-t)).numerator//(B*(1-z)*z**(n-t)).denominator for t in range(1,n+1)]
            require(min(widths)>=1 and 1+sum(widths)<=M,'count every phase')
            require(widths[-1]<=M-n,'terminal capacity')
            # d=1, rho=1/8: a uniform geometric upper has an explicit constant.
            err=sum(F(1,8)**(n-t)/widths[t-1]**2 for t in range(1,n+1))
            require(err<=F(32)/(M-n)**2,'integer geometric budget inequality')
            done('finite_integer_cases')
    for n in range(1,31):
        for M in range(n+2,4*n+15):
            Q=max(1,M-2*n-1)
            if M>=2*n+3:
                core=1+(M-3)//2
                require(core>=n+1 and 1+2+2*(core-1)<=M,'bit tag plus all phases')
                require(F(Q,4)<=core-n<=Q,'effective core budget comparison')
            else:require(Q==1,'single-tag bottleneck regime')
            done('finite_integer_cases')
    for a in (F(0),F(1,10),F(1,3),F(1,2)):
        for theta in (F(0),F(1,7),F(1,2)):
            bitrisk=F(0)
            for u in (-1,1):
                for b in (-1,1):
                    p=F(1,2)*((1-a)*(b==u)+a/2)
                    bitrisk+=p*(u-(1-a)*b)**2
            require(bitrisk==2*a-a*a and bitrisk<=2*a,'two-tag imputation risk')
            for g in (F(-1),F(0),F(1,3)):
                require(((g-theta)**2+(g+theta)**2)/2==g*g+theta*theta,'calibration average')
            done('exact_rational_cases')
        for p in (F(0),F(1,7),F(1,2),F(1)):
            tv=F(0)
            for u in (-1,1):
                for b in (-1,1):
                    ideal=F(1,2)*(b==u)
                    sim=F(1,2)*((1-a)*(b==u)+a*(p if b==1 else 1-p))
                    tv+=abs(ideal-sim)/2
            require(tv==a/2,'audit-protected deficiency for any erased guess')
            done('exact_rational_cases')
    for D in range(2,12):
        for w in (F(0),F(1,1000),F(1,4),F(1,2),F(1)):
            for M in (1,2,4,16,100):
                df,dp=D*D-1,2*(D-1)
                profile=float(w)*M**(-2/df)+float(1-w)*M**(-2/dp)
                require(0<profile<=1+1e-14,'weighted mass profile range')
                done('floating_sanity_cases')

def root(a):
    ev,U=np.linalg.eigh(a);require(np.min(ev)>0,'positive matrix root')
    return (U*np.sqrt(ev))@U.conj().T

def state(rng,D,floor=0.03):
    a=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));a=a@a.conj().T;a/=np.trace(a)
    return (1-floor)*a+floor*np.eye(D)/D

def effect(rng,D):
    a=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));h=(a+a.conj().T)/2;h-=np.trace(h)*np.eye(D)/D;h/=max(1,np.linalg.norm(h))
    return np.eye(D)+0.3*h

def metric(a,b):
    rb=root(b);ib=np.linalg.inv(rb);e=np.linalg.eigvalsh(ib@a@ib)
    return math.log(e[-1]/e[0])

def analytic_checks():
    rng=np.random.default_rng(321011)
    for D in range(2,6):
        for _ in range(40):
            P=rng.uniform(.01,1,size=(D,D));P/=P.sum(axis=0,keepdims=True);alpha=float(P.min())
            x=rng.uniform(.001,1,size=D);x/=x.sum();z=rng.uniform(.001,1,size=D);z/=z.sum()
            likelihood=np.exp(rng.normal(0,3,size=D));u=x*likelihood;u/=u.sum();v=z*likelihood;v/=v.sum()
            hil=lambda a,b:float(np.ptp(np.log(a/b)))
            require(hil(P@u,P@v)<=(1-alpha)*hil(x,z)+1e-11,'positive-matrix Hilbert contraction')
            done('floating_sanity_cases')
    for D in range(2,6):
        for lam in (.05,.5,.95):
            for _ in range(14):
                rho=lam*state(rng,D)+(1-lam)*np.eye(D)/D;sigma=lam*state(rng,D)+(1-lam)*np.eye(D)/D
                A=effect(rng,D);K=root(A);f=lambda r:K@r@K/np.trace(A@r)
                out=f(rho);rs=root(rho);irs=np.linalg.inv(rs)
                B=irs@root(rs@out@rs)@irs;back=D*(B@B)/np.trace(B@B)
                require(np.linalg.norm(back-A)<1e-9,'positive congruence inverse')
                c=(1-lam)/(D*(lam+(1-lam)/D));H0=2*math.log((lam+(1-lam)/D)/((1-lam)/D))
                contraction=(1-c)*math.exp(H0)/((1-c)*math.exp(H0)+c)
                T=lambda r:lam*r+(1-lam)*np.eye(D)/D
                require(metric(T(f(rho)),T(f(sigma)))<=contraction*metric(rho,sigma)+1e-9,'quantum Hilbert contraction')
                # Directional likelihood perspective Hessian at a genuinely informative effect.
                vv=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));vv=(vv+vv.conj().T)/2;vv-=np.trace(vv)*np.eye(D)/D;vv/=np.linalg.norm(vv)
                ell=float(np.trace(A@rho).real);un=K@rho@K;du=K@vv@K;dl=float(np.trace(A@vv).real)
                target=2*np.linalg.norm(du-un/ell*dl)**2/ell
                potential=lambda t:float(np.linalg.norm(K@(rho+t*vv)@K)**2/np.trace(A@(rho+t*vv)).real)
                h=1e-4;fd=(potential(h)-2*potential(0)+potential(-h))/h**2
                require(abs(fd-target)<2e-6,'perspective Hessian factor and normalization')
                done('floating_sanity_cases')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    bayes_cases();budget_cases();analytic_checks()
    result={'status':'PASS','cases':COUNTS,'total_cases':sum(COUNTS.values()),'seed':321011,
      'suites':['exact likelihood reweighting and three-defect identity','integer total-clock and retained-bit allocations','attained erasure and calibration algebra','actual weighted strata','positive-matrix and quantum cone contraction','positive-congruence inverse and Hessian sanity'],
      'scope':'Each case may contain several checks. Exact arithmetic is separated from floating sanity. No finite test certifies the continuous theorem, global optimality, priority, or journal significance.'}
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        p=Path(args.output);p.mkdir(parents=True,exist_ok=True);(p/'FINITE_REGRESSION.json').write_text(text)
    print(text,end='')
if __name__=='__main__':main()
