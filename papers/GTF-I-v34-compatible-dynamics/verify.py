#!/usr/bin/env python3
"""Finite algebra and 80-digit diagnostics for the v34 analytic proofs.

No finite test verifies the all-horizon converse or establishes novelty.
Checks use explicit exceptions, and therefore also run under Python -O.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import random
import mpmath as mp
import sympy as sp

CONTROLS=['angular-linear','omit-moment-loss','signed-fejer','deficiency-factor',
          'terminal-factor','golden-constant','resonance-sign','time-independent-test']


def require(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError('CHECK_REJECTED: '+why)


def exact_matrix(rows):
    return sp.Matrix([[sp.Rational(v.numerator,v.denominator) if isinstance(v,F) else v for v in row] for row in rows])


def mf(v: F):
    return mp.mpf(v.numerator)/v.denominator


def angular(z,l):
    r=abs(z)
    return mp.mpc(0) if r==0 else r*(z/r)**l


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--negative-control');ap.add_argument('--export',type=Path)
    args=ap.parse_args();mutant=args.negative_control
    require(mutant is None or mutant in CONTROLS,'unknown negative control')
    mp.mp.dps=80;tol=mp.mpf('1e-65')
    out={'schema':'gtf34.checks/1',
         'scope':'Exact finite identities and explicitly labelled 80-digit diagnostics; not proof of universal optimization, independent proof certification or priority clearance.'}
    x=sp.symbols('x')
    for l in range(1,33):
        require(sp.expand(x**l-1-l*(x-1)-(x-1)*sum(x**j-1 for j in range(l)))==0,'angular polynomial identity')
    for k in range(1,81):
        M=2*k
        v=sum(F(M+1-l,M+1)*l*l for l in range(1,M+1))
        require(v==F(M*(M+1)*(M+2),12) and v<=2*k**3,'weighted harmonic square sum')
        require(F(M,2)+4*v<=9*k**3,'occupation constant')
    out['exact_angular_identities']=32;out['exact_harmonic_sums']=80

    # Symmetric small-angle mixtures witness the quadratic, not linear, loss cost.
    th=mp.mpf('0.01');l=20;zs=[mp.e**(1j*th),mp.e**(-1j*th)]
    lhs=abs((angular(zs[0],l)+angular(zs[1],l))/2-angular(sum(zs)/2,l))
    factor=(l+1) if mutant=='angular-linear' else (l*l+1)
    require(lhs<=factor*(1-abs(sum(zs)/2))+tol,'angular averaging needs harmonic-square cost')
    rng=random.Random(340925);angular_cases=0
    for _ in range(100):
        m=rng.randint(2,6);w=[rng.randint(1,10) for _ in range(m)];den=sum(w)
        z=[mp.mpc(rng.randint(-20,20),rng.randint(-20,20))/20 for _ in range(m)]
        if _%10==0:z=[mp.mpc(0),mp.mpc(1),mp.mpc(-1)];w=[2,1,1];den=4;m=3
        ez=sum(wi*zi for wi,zi in zip(w,z))/den
        loss=sum(wi*abs(zi) for wi,zi in zip(w,z))/den-abs(ez)
        for l in [1,2,3,5,8,13,21]:
            err=abs(sum(wi*angular(zi,l) for wi,zi in zip(w,z))/den-angular(ez,l))
            require(err<=(l*l+1)*loss+tol,'homogeneous angular Jensen diagnostic')
            angular_cases+=1

    # Exact Fejer expansion on rational-weight measures at fourth roots of unity.
    roots=[sp.Integer(1),sp.I,sp.Integer(-1),-sp.I];fejer_cases=0
    for k in range(1,5):
        weights=[sp.Rational(i+1,k*(k+1)//2) for i in range(k)]
        for M in range(1,13):
            mus=[sum(weights[i]*roots[i]**l for i in range(k)) for l in range(M+1)]
            phi=sum(sp.Rational(M+1-l,M+1)*sp.expand(mus[l]*sp.conjugate(mus[l])) for l in range(1,M+1))
            integral=0
            for i in range(k):
                for j in range(k):
                    val=sum((roots[i]/roots[j])**a for a in range(M+1))
                    kernel=sp.expand(val*sp.conjugate(val))/(M+1)
                    require(kernel>=0,'Fejer kernel nonnegative')
                    integral+=weights[i]*weights[j]*kernel
            require(sp.simplify(1+2*phi-integral)==0,'Fejer integral identity')
            require(1+2*phi>=sp.Rational(M+1,k),'Fejer finite atom lower')
            fejer_cases+=1
    if mutant=='signed-fejer':
        M=4;theta=mp.mpf('0.001');v=[1,mp.e**(1j*theta)]
        lhs=sum(2*(1-mp.mpf(l)/(M+1))*abs(v[0]**l-v[1]**l)**2 for l in range(1,M+1))
        require(lhs>=2*(M+1),'dropping cross terms fails for signed measures')
    out['exact_fejer_cases']=fejer_cases

    # Time-varying finite machines with no statewise observable interpretation.
    # p is rational and u=E[Y 1_S] is propagated using 80-digit complex arithmetic.
    moment_checks=0;trajectories=[];zeta=mp.mpc(3,4)/5
    for widths in [[2,5,3,7,1,4,2],[1,2,4,2,6,3,5],[3,3,3,3,3,3,3]]:
        p=[F(1,widths[0])]*widths[0];u=[mp.mpc(mf(v)) for v in p]
        previous_q=mp.mpf(1);history=[];total_loss=mp.mpf(0)
        for t in range(len(widths)-1):
            K,J=widths[t:t+2];z=[u[i]/mf(p[i]) if p[i] else 0 for i in range(K)]
            q=sum(mf(p[i])*abs(z[i]) for i in range(K))
            rows=[]
            for c in range(2):
                rr=[]
                for s in range(K):
                    a=[rng.randint(0,9) for _ in range(J)]
                    if sum(a)==0:a[0]=1
                    rr.append([F(v,sum(a)) for v in a])
                rows.append(rr)
            if mutant=='time-independent-test' and K!=J:
                require(K==J,'the tested transition profile is genuinely time dependent')
            pn=[sum(p[s]*rows[c][s][j]/2 for s in range(K) for c in range(2)) for j in range(J)]
            un=[sum(u[s]*mf(rows[c][s][j])*zeta**(-c)/2 for s in range(K) for c in range(2)) for j in range(J)]
            zn=[un[j]/mf(pn[j]) if pn[j] else mp.mpc(0) for j in range(J)]
            qn=sum(mf(pn[j])*abs(zn[j]) for j in range(J));loss=q-qn
            require(loss>=-tol and abs(q-previous_q)<tol,'conditional amplitude telescopes')
            for l in range(1,13):
                a=(1+zeta**(-l))/2
                mt=sum(mf(p[i])*angular(z[i],l) for i in range(K))
                mn=sum(mf(pn[j])*angular(zn[j],l) for j in range(J))
                budget=0 if mutant=='omit-moment-loss' else (l*l+1)*loss
                require(abs(mn-a*mt)<=budget+tol,'moment recursion must retain barycentric error')
                require(abs(mn)**2<=abs(a)**2*abs(mt)**2+4*l*l*loss+tol,'squared harmonic budget')
                moment_checks+=1
            history.append({'cut':t+1,'states':J,'amplitude':mp.nstr(qn,40)})
            total_loss+=loss;previous_q=qn;p,u=pn,un
        require(abs(total_loss+previous_q-1)<tol,'one common total amplitude loss')
        trajectories.append(history)
    out['floating_diagnostics']={'decimal_precision':80,'angular_mixtures':angular_cases,'moment_recursions':moment_checks}

    # The finite deficiency example has exact, matching primal and dual witnesses.
    E=exact_matrix([[F(1,2),0,F(1,2),0],[F(1,2),0,0,F(1,2)],
                    [0,F(1,2),F(1,2),0],[0,F(1,2),0,F(1,2)]])
    Fmat=exact_matrix([[1,0],[1,0],[0,1],[0,1]])
    T=exact_matrix([[1,0],[0,1],[F(1,2),F(1,2)],[F(1,2),F(1,2)]])
    Z=exact_matrix([[F(1,2),0],[0,0],[0,F(1,2)],[0,0]])
    row_errors=[sum(abs(v) for v in (E*T-Fmat).row(h))/2 for h in range(4)]
    support=sum(max((E.T*Z).row(i)) for i in range(4))
    dual=sum(Z.multiply_elementwise(Fmat))-support
    require(max(row_errors)==dual==sp.Rational(1,4),'matched one-sided deficiency witnesses')
    expected=sp.Rational(1,2) if mutant=='deficiency-factor' else sp.Rational(1,4)
    require(dual==expected,'TV deficiency has its declared factor of one half')
    require(sum(max(Z.row(h))-min(Z.row(h)) for h in range(4))==1,'oscillation budget normalization')
    out['exact_deficiency']='1/4 with normalized primal/dual witnesses'

    # Constants used to transfer terminal TV error and Diophantine separation.
    e=F(1,100);kappa=F(1,10)-(e if mutant=='terminal-factor' else 2*e)
    require(kappa==F(2,25),'binary row TV changes each mean by twice the error')
    golden=F(1,9)*F(1,100)/18
    expected=F(1,1620) if mutant=='golden-constant' else F(1,16200)
    require(golden==expected,'golden fifth-root coefficient')
    require(F(18)*100*4==7200 and 8*25**2==5000,'rational width constants')
    alpha=(sp.sqrt(5)-1)/2;alphap=-(sp.sqrt(5)+1)/2
    n,pv=sp.symbols('n pv',integer=True)
    require(sp.expand((n*alpha-pv)*(n*alphap-pv)-(pv**2+n*pv-n*n))==0,'golden norm identity')
    zz=sp.Rational(3,5)+4*sp.I/5
    for j in range(1,33):
        a,b=sp.expand((3+4*sp.I)**j-5**j).as_real_imag()
        require(a*a+b*b>=1,'Gaussian integer arithmetic separation')
    out['arithmetic_constants']={'golden':'1/16200','rational':'N <= 7200 K^3 25^(2K)','gaussian_integer_checks':32}

    # Fully rational terminal identities of a counter realization, for every word.
    tr=[(sp.Rational(1,2),0),(-sp.Rational(1,2),sp.Rational(1,2)),(-sp.Rational(1,2),-sp.Rational(1,2))]
    powers=[sp.expand(zz**i) for i in range(9)];word_cases=0
    for n in range(7):
        for word in itertools.product([0,1],repeat=n):
            r=powers[sum(word)]
            for sx,sy in itertools.product([-1,1],repeat=2):
                x,y=sp.Rational(sx,10),sp.Rational(sy,10)
                weights=[x+sp.Rational(1,2),(sp.Rational(1,2)-x)/2+y,(sp.Rational(1,2)-x)/2-y]
                val=sp.expand(sum(weights[i]*r*(tr[i][0]+sp.I*tr[i][1]) for i in range(3)))
                require(sp.expand(val-r*(x+sp.I*y))==0,'complete rational rotation word')
                word_cases+=1
    out['exact_rational_rotation_words']=word_cases

    # Recheck the inherited resonance rows; labels denote vertices, not stored reals.
    fib=[0,1]
    for _ in range(20):fib.append(sum(fib[-2:]))
    ga=(mp.sqrt(5)-1)/2;row_cases=0;polygons=[]
    for n in [1,3,8,21,55]:
        i=next(i for i in range(5,len(fib)) if fib[i]>=max(5,mp.root(40*n,3)))
        p,q=fib[i-1],fib[i];a=mp.pi/q;delta=2*mp.pi*(ga-mp.mpf(p)/q)
        lam=mp.cos(a-abs(delta))/mp.cos(a);w=mp.sin(abs(delta))/(lam*mp.sin(2*a))
        sign=1 if delta>0 else -1
        if mutant=='resonance-sign':sign=-sign
        require(lam>=1 and 0<=w<=1 and mp.log(lam)<mp.mpf(40)/q**3,'resonant range')
        require(lam**n/4<1,'final bounded decoder')
        v=[mp.e**(2j*mp.pi*s/q) for s in range(q)]
        for s in range(q):
            val=lam*((1-w)*v[(s+p)%q]+w*v[(s+p+sign)%q])
            require(abs(val-mp.e**(2j*mp.pi*ga)*v[s])<tol,'resonant active orientation')
            idle=lam*(v[s]/lam+(1-1/lam)*sum(v)/q)
            require(abs(idle-v[s])<tol,'resonant idle normalization')
            row_cases+=2
        polygons.append({'N':n,'p':p,'q':q,'lambda_80digit':mp.nstr(lam,80),'weight_80digit':mp.nstr(w,80)})
    out['floating_diagnostics']['resonance_rows']=row_cases
    out['proved_claims']={'all_hidden_bounded_type':'Omega(N^(1/5)) <= W_N <= O(N^(1/3))',
      'occupation':'count(K_t<=k)*beta_(2k) <= 18*k^3/kappa^2',
      'robust_range':'uniform row-TV epsilon < 1/20',
      'diagram':'D >= [1/10 - sqrt(18*K^3/(N*beta_(2K)))]_+/2',
      'sharp_hidden_exponent_claimed':False}
    if args.export:
        args.export.write_text(json.dumps({'conditional_phase_diagnostics':trajectories,
          'resonant_polygon_diagnostics':polygons,'deficiency_primal':[list(map(str,T.row(i))) for i in range(T.rows)],
          'scope':'Finite witnesses and high-precision diagnostics, not exact real row encodings or universal proof certification.'},indent=2)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
