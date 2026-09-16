#!/usr/bin/env python3
"""Independent finite controls for the v68 review; NOT a theorem certificate.
No manuscript checker is imported. Requires mpmath and sympy.
Outputs exact rational checks and high-precision finite Euclidean chord tests.
"""
from fractions import Fraction as Q
import json
import mpmath as mp
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def weighted_controls():
    thresholds = []
    for a in map(Q, ['1/3','1/2','3/4','9/10','19/20']):
        m = 3
        while 6*a**m/(1-a**m) >= 1:
            m += 1
        theta = 6*a**m/(1-a**m)
        thresholds.append({'a':str(a),'m':m,'theta':str(theta),
                           'inverse_bound':str(2/(1-theta))})
        require(theta < 1, 'Incorrect weighted threshold')
    samples = 0
    # Convex averages, not a numerical quadrature assertion about a continuum.
    # These are generic nonlinear composition models, NOT realized billiards.
    R=Q(1,4); J=4
    for a in [Q(1,2),Q(3,4),Q(9,10)]:
        m=3
        while 6*a**m/(1-a**m)>=1: m+=1
        theta=6*a**m/(1-a**m)
        for r in [2,3]:
            z=[Q(1),Q(-2,3),Q(1,2)][:r]
            M=Q(1)+R/10
            values=[]
            for u in [R,-R,R/2,-R/2]:
                for b in range(r):
                    total=Q(0)
                    for t in [Q(0),Q(1,2),Q(1)]:
                        x=u; g=(1+u/5)*z[b]*u**m*(1+u/10)
                        for j in range(1,J+1):
                            i=(b+j-1)%r
                            sig=(-1 if i%2 else 1)*a*Q(3+i,5+r)
                            old=x; x=sig*(x+t*x*x/8)
                            require(abs(x)<=a*abs(old),'One-step contraction failed')
                            v=2+(old+x)/10
                            require(1<=v<=3,'Weight floor failed')
                            h=z[(b+j)%r]*x**m*(1+x/10)
                            require(abs(h)<=M*a**(j*m)*abs(u)**m,'Weighted evaluation bound failed')
                            g+=v*h; samples+=1
                        total+=g/3
                    values.append(abs(total)/abs(u)**m)
            omitted=3*M*a**((J+1)*m)/(1-a**m)
            # The full output norm is at least the sampled norm minus this tail bound.
            require(max(values)-omitted >= (1-theta)*M/2,
                    'Finite model plus rigorous tail majorant violates separation')
    # Mere C rho^j does not yield high-order smallness when C rho>1.
    require((Q(2)*Q(3,4))**20 > 1000,'Constant-one negative control failed')
    return {'thresholds':thresholds,'exact_nonlinear_evaluation_bounds':samples,
            'averaged_models':6,'constant_one_negative_control':True,
            'scope':'Finite rational contraction models with an infinite tail majorant; not billiard realization.'}


def algebra_controls():
    A,C,d,e,Z,Y,U,V=sp.symbols('A C d e Z Y U V',nonzero=True)
    h=A+C
    f=U*V*(d-h)/Z; ft=U*V*(e-h)/Y
    quotient=sp.cancel(f*(e/Y)/(ft*(d/Z)))
    recovered=sp.cancel(d*e*(1-quotient)/(e-d*quotient))
    require(sp.cancel(recovered-h)==0,'Two-offset cancellation')
    cases=0
    for aa in [Q(-1,8),Q(0),Q(1,7)]:
      for cc in [Q(-1,9),Q(0),Q(1,6)]:
       for dd,ee in [(Q(1),Q(2)),(Q(2,3),Q(5,4))]:
        for uu,vv in [(Q(1),Q(1)),(Q(5,3),Q(2,5)),(Q(7,4),Q(9,7))]:
         q=(uu*vv*(dd-aa-cc)/3)*(ee/5)/((uu*vv*(ee-aa-cc)/5)*(dd/3))
         got=dd*ee*(1-q)/(ee-dd*q)
         require(got==aa+cc,'Exact signed physical action extraction');cases+=1
    # Exact area-preserving shear witness for a unit disk.
    th,eps=sp.symbols('th eps',real=True); phi=sp.Function('phi')
    x=sp.cos(th)-eps*phi(sp.sin(th)); y=sp.sin(th)
    curvature_num=sp.simplify(sp.diff(x,th)*sp.diff(y,th,2)-sp.diff(y,th)*sp.diff(x,th,2))
    target=1+eps*sp.Subs(sp.diff(phi(sp.Symbol('z')),sp.Symbol('z'),2),sp.Symbol('z'),sp.sin(th))*sp.cos(th)**3
    require(sp.simplify(curvature_num-target)==0,'Sheared disk curvature identity')
    # (x,y)->(x-eps*phi(y),y) has Jacobian one for every smooth phi.
    xx,yy=sp.symbols('xx yy'); jac=sp.Matrix([xx-eps*phi(yy),yy]).jacobian([xx,yy]).det()
    require(jac==1,'Exact area preservation')
    # Derivatives of exp(-1/u^2) are Laurent polynomial times the same exponential.
    u=sp.symbols('u',positive=True); pol=sp.Integer(1)
    for n in range(12):
        nxt=sp.diff(pol,u)+2*pol/u**3
        require(sp.simplify(sp.diff(pol*sp.exp(-1/u**2),u)-nxt*sp.exp(-1/u**2))==0,'Flat derivative recurrence')
        pol=sp.expand(nxt)
    return {'symbolic_two_offset_identity':True,'exact_density_cases':cases,
            'area_preserving_shear_jacobian':str(jac),'sheared_disk_curvature_numerator':'1+eps*phi_second(sin(theta))*cos(theta)^3',
            'flat_derivative_recurrences':12,
            'scope':'Symbolic identities. Smooth flatness and geometric clearance still use the analytical arguments in the report.'}


def chord_controls():
    mp.mp.dps=75
    def phi(x): return mp.exp(-1/(x*x)) if x else mp.mpf(0)
    def graph(x,phase,eps):
        f=1-mp.sqrt(1-x*x); p=x/mp.sqrt(1-x*x); pp=(1-x*x)**mp.mpf('-1.5')
        if phase==0 and x:
            ph=phi(x); f+=eps*ph; p+=eps*ph*2/x**3; pp+=eps*ph*(4/x**6-6/x**4)
        return f,p,pp
    def edge(x,y,i,eps):
        f,p,pp=graph(x,i%2,eps); F,P,PP=graph(y,(i+1)%2,eps)
        h=2+f+F; d=y-x; ell=mp.sqrt(h*h+d*d)
        ax=h*p-d; ay=h*P+d
        return (ell,ax/ell,ay/ell,(p*p+h*pp+1)/ell-ax*ax/ell**3,
                (p*P-1)/ell-ax*ay/ell**3,(P*P+h*PP+1)/ell-ay*ay/ell**3,h/ell)
    def solve(u,N,eps):
        a=3-2*mp.sqrt(2); xs=[u]+[u*a**i for i in range(1,N)]+[mp.mpf(0)]
        for step in range(20):
            ed=[edge(xs[i],xs[i+1],i,eps) for i in range(N)]
            grad=mp.matrix([ed[i-1][2]+ed[i][1] for i in range(1,N)])
            if max(abs(v) for v in grad)<mp.mpf('1e-65'): break
            H=mp.matrix(N-1)
            for i in range(N-1):
                H[i,i]=ed[i][5]+ed[i+1][3]
                if i+1<N-1:H[i,i+1]=H[i+1,i]=ed[i+1][4]
            delta=mp.lu_solve(H,grad)
            for i in range(1,N):xs[i]-=delta[i-1]
        else: raise RuntimeError('Finite chord Newton solver did not converge')
        ed=[edge(xs[i],xs[i+1],i,eps) for i in range(N)]
        action=sum(v[0]-2 for v in ed)
        envelope=sum(ed[i][6]*((phi(xs[i]) if i%2==0 else 0)+(phi(xs[i+1]) if (i+1)%2==0 else 0)) for i in range(N))
        residual=max(abs(ed[i-1][2]+ed[i][1]) for i in range(1,N))
        return action,envelope,xs,ed,residual
    records=[];worst=mp.mpf(0)
    for u0 in ['0.14','0.20','0.28']:
      for sign in [1,-1]:
       u=sign*mp.mpf(u0); eps=mp.mpf('.01'); ratios=[]
       for N in [8,12]:
        base=solve(u,N,mp.mpf(0)); pert=solve(u,N,eps)
        ratio=(pert[0]-base[0])/(eps*phi(u)); ratios.append(ratio)
        require(mp.mpf('.5')<ratio<mp.mpf('1.2'),'Flat finite physical action signal')
        require(all(abs(pert[2][i+1])<mp.mpf('.3')*abs(pert[2][i]) for i in range(N-1)), 'Physical visit contraction')
        step=mp.mpf('1e-5');mid=solve(u,N,eps/2)
        diff=(solve(u,N,eps/2+step)[0]-solve(u,N,eps/2-step)[0])/(2*step)
        err=abs(diff-mid[1])/phi(u);worst=max(worst,err)
        require(err<mp.mpf('1e-18'),'Finite envelope comparison')
        wrong=mid[1]+mid[3][0][6]*phi(u)
        require(abs(diff-wrong)>phi(u)/2,'Initial multiplicity negative control')
        records.append({'endpoint':str(u),'flights':N,'signal_over_eps_flat':mp.nstr(ratio,22),
                        'scaled_envelope_error':mp.nstr(err,8),'stationarity_residual':mp.nstr(pert[4],8)})
       require(abs(ratios[0]-ratios[1])<mp.mpf('1e-9'),'Finite length proxy comparison')
    return {'precision_decimal_digits':mp.mp.dps,'configurations':len(records),'worst_scaled_envelope_error':mp.nstr(worst,10),
            'doubled_initial_negative_controls':len(records),'records':records,
            'scope':'Actual Euclidean circle-graph chords, one flat perturbation, finite stationary chains only. The cutoff is one on all sampled coordinates. No infinite-limit error certificate.'}


if __name__=='__main__':
    result={'imports_author_code':False,'weighted':weighted_controls(),'algebra':algebra_controls(),'physical_flat_chords':chord_controls()}
    print(json.dumps(result,indent=2,sort_keys=True))
