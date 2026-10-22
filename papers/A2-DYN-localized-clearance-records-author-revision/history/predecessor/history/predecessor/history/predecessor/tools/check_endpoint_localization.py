#!/usr/bin/env python3
"""Supplementary exact algebra and actual triangular-billiard diagnostics.
No finite test proves a continuum theorem, complete root sum, or raw LLT.
All failures use explicit exceptions and remain active under python -O.
"""
from __future__ import annotations
import argparse, json, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp

SIG=F(47,59); Q0=F(47,53); RP=F(47,100); TM=F(3,50)
J=RP/(2*TM)*(SIG+1/SIG)
CC=J*(1+RP/TM*(1+1/SIG)); CD=RP*J*(1+SIG)
C3=RP+3*RP**2/TM+3*RP**3/TM**2
CF=8*C3*J**3*(1+SIG)**3/(1-SIG**3)

def require(x, msg):
    if not x: raise RuntimeError(msg)

def tri_solve(diag, off, rhs):
    """Positive tridiagonal solve; supports exact rational or float scalars."""
    if not diag:return []
    d=list(diag);b=list(rhs);u=list(off)
    for i in range(1,len(d)):
        a=u[i-1]/d[i-1];d[i]-=a*u[i-1];b[i]-=a*b[i-1]
    x=[b[-1]/d[-1]]
    for i in range(len(d)-2,-1,-1):x.append((b[i]-u[i]*x[-1])/d[i])
    return x[::-1]

def exact():
    require(2/RP-(1/SIG-1)/TM==0,'exact supersolution cancellation')
    require(SIG<Q0<1 and SIG**4<Q0,'depth summability and fourth-root comparison')
    require(J==F(2845,354),'Jacobi constant')
    counts=0;smallest=F(1)
    for m in range(1,18):
        for v in range(6):
            R=[F(9,20),F(23,50),RP][v%3]
            cs=[F(4,5)]+[ [F(1,10**12),F(1,2),F(3,4)][(i+v)%3] for i in range(1,m)]+[F(9,10)]
            ts=[TM+F((i+3*v)%11,17) for i in range(m)]
            eta=[(F(1),F(0)),(F(0),F(-1)),(F(2,3),F(-4,5))][v%3]
            ys=[cs[0]*eta[0],(-1)**m*cs[-1]*eta[1]]
            if m>1:
                w=[1/t for t in ts];k=[2/(R*cs[i]) for i in range(1,m)]
                diag=[k[i-1]+w[i-1]+w[i] for i in range(1,m)]
                off=[-w[i] for i in range(1,m-1)]
                rhs=[F(0)]*(m-1);rhs[0]+=w[0]*ys[0];rhs[-1]+=w[-1]*ys[-1]
                ys=[ys[0]]+tri_solve(diag,off,rhs)+[ys[-1]]
            for i,y in enumerate(ys):
                s=SIG**i+SIG**(m-i)
                require(abs(y)<=SIG**i*cs[0]*abs(eta[0])+SIG**(m-i)*cs[-1]*abs(eta[1]),'rational weighted localization')
                require(abs(y/cs[i])<=J*s*max(map(abs,eta)),'rational unweighted localization')
            counts+=1;smallest=min(smallest,*cs)
    polys=0;variables=0
    for m in range(1,6):
        ts=sp.symbols('t0:'+str(m),positive=True);ks=sp.symbols('k1:'+str(m),positive=True)
        M=sp.Matrix([[1,ts[0]],[0,1]])
        for i in range(1,m):M=sp.Matrix([[1,ts[i]],[0,1]])*sp.Matrix([[1,0],[ks[i-1],1]])*M
        b=sp.expand(M[0,1]);allv=ts+ks;p=sp.Poly(b,*allv)
        require(all(c>0 for c in p.coeffs()),'optical coefficient positivity')
        require(all(max(mon)<=1 for mon in p.monoms()),'separate optical multiaffinity')
        for x in allv:
            q=sp.Poly(sp.expand(b-x*sp.diff(b,x)),*allv)
            require(all(c>=0 for c in q.coeffs()),'nonnegative log-sensitivity complement');variables+=1
        polys+=1
    # Exact two-dimensional Gauss determinant including the physical factor.
    a,b,d,z,R,c=sp.symbols('a b d z R c',positive=True)
    # Rotate at the point to e=(1,0): D(F,arg grad) rows are (z,0),(b/z,d/z).
    require(sp.Matrix([[z,0],[b/z,d/z]]).det()==d,'Gauss determinant chi')
    require(sp.simplify((R/(4*sp.pi*R*c))*(1/d)-1/(4*sp.pi*c*d))==0,'original section normalization')
    return dict(exact_rational_chains=counts,smallest_test_incidence=str(smallest),
        optical_polynomials=polys,optical_variable_checks=variables,
        exact_constants={'sigma':str(SIG),'J_star':str(J),'C_c':str(CC),'C_clearance':str(CD),'C_F':str(CF)},
        scope='finite exact algebra only; rational chains are not asserted to be physically realizable')

# Complete enclosing disk set, not a stochastic substitute.  Norm <=9 includes
# every nearest hit and every clearance minimizer by the native horizon <28/5.
LAB=np.array([(a,b) for a in range(-11,12) for b in range(-11,12) if a*a+a*b+b*b<=81],dtype=int)
CEN=np.column_stack((LAB[:,0]+LAB[:,1]/2,np.sqrt(3)*LAB[:,1]/2))
ZERO=np.flatnonzero(np.all(LAB==0,axis=1))[0]

def normang(a):return (a+math.pi)%(2*math.pi)-math.pi

def section(a,p,R):
    lo,hi=.49,.53
    def f(q):return 8*R*q*(1+q*q)-4*q*(1-q*q)+math.sqrt(3)*(1-6*q*q+q**4)
    require(f(lo)*f(hi)<0,'section polynomial bracket')
    for _ in range(60):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<=0:hi=mid
        else:lo=mid
    th=2*math.atan((lo+hi)/2)
    squares=[(0.,0.),(math.pi/6,-.5),(-th,math.sin(th)),(math.pi/3-th,math.sin(th))]
    return any(abs(normang(a-u))<1/200 and abs(p-v)<1/200 for u,v in squares) or (abs(normang(a-math.pi/6))<3/50 and abs(p)<3/20)

def trace(alpha,p,R,m):
    n=np.array([math.cos(alpha),math.sin(alpha)]);v=math.sqrt(1-p*p)*n+p*np.array([-n[1],n[0]])
    q=R*n;center=np.zeros(2);label=np.zeros(2,dtype=int)
    centers=[center.copy()];angles=[alpha];ps=[p];cs=[math.sqrt(1-p*p)];ts=[];cls=[];word=[];contact=[]
    for _ in range(m):
        rel=q-CEN;bv=rel@v;dis=bv*bv-np.sum(rel*rel,axis=1)+R*R
        roots=np.full(len(LAB),np.inf);ok=dis>0;roots[ok]=-bv[ok]-np.sqrt(dis[ok]);roots[roots<=1e-9]=np.inf;roots[ZERO]=np.inf
        j=int(np.argmin(roots));tau=float(roots[j]);require(math.isfinite(tau) and tau<=5.6+1e-8,'complete physical first-hit search')
        hit=q+tau*v;nn=(hit-CEN[j])/R;contact.append(abs(float(np.linalg.norm(nn))-1))
        foot=np.clip((CEN-q)@v,0,tau);dist=np.linalg.norm(CEN-(q+np.outer(foot,v)),axis=1)-R
        dist[[ZERO,j]]=np.inf;cl=float(dist.min());require(cl>=-1e-8,'unvisited collision hidden by declared itinerary')
        nn/=np.linalg.norm(nn);inc=-float(v@nn);require(inc>0,'strict physical incidence')
        vv=v-2*float(v@nn)*nn;pp=float(vv@np.array([-nn[1],nn[0]]))
        center=center+CEN[j];label=label+LAB[j]
        centers.append(center.copy());angles.append(math.atan2(nn[1],nn[0]));word.append(LAB[j].tolist());ps.append(pp);cs.append(inc);ts.append(tau);cls.append(cl)
        q=R*nn;v=vv/np.linalg.norm(vv)
    return {'R':R,'m':m,'angles':np.array(angles),'centers':np.array(centers),'incidences':cs,'flights':ts,'clearances':cls,'momenta':ps,'word':word,
       'return_count':sum(section(a,pp,R) for a,pp in zip(angles[:-1],ps[:-1])),
       'initial_section':section(angles[0],ps[0],R),'terminal_section':section(angles[-1],ps[-1],R),
       'displacement_label':label.tolist(),'physical_roof':sum(ts),'contact_error':max(contact)}

def action(R,centers,angles):
    n=np.column_stack((np.cos(angles),np.sin(angles)));t=np.column_stack((-np.sin(angles),np.cos(angles)))
    x=centers+R*n;X=np.diff(x,axis=0);length=np.linalg.norm(X,axis=1);vs=X/length[:,None]
    N=len(angles);g=np.zeros(N);H=np.zeros((N,N))
    for i in range(N-1):
        v=vs[i];P=np.eye(2)-np.outer(v,v);T=length[i]
        g[i]-=R*t[i]@v;g[i+1]+=R*t[i+1]@v
        H[i,i]+=R*n[i]@v+R**2/T*(t[i]@P@t[i])
        H[i+1,i+1]+=-R*n[i+1]@v+R**2/T*(t[i+1]@P@t[i+1])
        H[i,i+1]=H[i+1,i]=-R**2/T*(t[i]@P@t[i+1])
    E=[0,N-1];L=np.zeros((N,2));L[0,0]=L[-1,1]=1
    if N>2:L[1:-1]=-np.linalg.solve(H[1:-1,1:-1],H[np.ix_(list(range(1,N-1)),E)])
    G=L.T@H@L
    return float(sum(length)),g,H,G,L,n,t,vs,length

def third(R,centers,angles,lifts):
    _,_,_,_,_,n,t,vs,ts=action(R,centers,angles);result=0.
    for i,v in enumerate(vs):
        A,B,C=lifts;P=np.eye(2)-np.outer(v,v);T=ts[i]
        def d(U):return R*(t[i+1]*U[i+1]-t[i]*U[i])
        def d2(U,V):return R*(-n[i+1]*U[i+1]*V[i+1]+n[i]*U[i]*V[i])
        da,db,dc=d(A),d(B),d(C)
        cube=-((v@da)*(db@P@dc)+(v@db)*(da@P@dc)+(v@dc)*(da@P@db))/T**2
        pairs=(d2(A,B)@P@dc+d2(A,C)@P@db+d2(B,C)@P@da)/T
        d3=R*(-t[i+1]*A[i+1]*B[i+1]*C[i+1]+t[i]*A[i]*B[i]*C[i])
        result+=cube+pairs+v@d3
    return float(result)

def solve_endpoint(o,delta):
    a=o['angles'].copy();a[0]+=delta[0];a[-1]+=delta[1]
    for _ in range(16):
        data=action(o['R'],o['centers'],a);g,H=data[1:3]
        if len(a)<=2 or np.max(abs(g[1:-1]))<2e-13:break
        step=np.linalg.solve(H[1:-1,1:-1],g[1:-1]);a[1:-1]-=step
    require(len(a)<=2 or max(abs(action(o['R'],o['centers'],a)[1][1:-1]))<2e-10,'stationary branch solve residual')
    return a,action(o['R'],o['centers'],a)

def physical_valid(R,centers,angles):
    data=action(R,centers,angles);n,vs,ts=data[5],data[7],data[8]
    if min(ts)<float(TM)-1e-8:return False
    for i,v in enumerate(vs):
        if v@n[i]<=1e-9 or -v@n[i+1]<=1e-9:return False
        q=R*n[i];dest=centers[i+1]-centers[i]
        j=int(np.argmin(np.linalg.norm(CEN-dest,axis=1)))
        if np.linalg.norm(CEN[j]-dest)>1e-7:return False
        foot=np.clip((CEN-q)@v,0,ts[i]);dd=np.linalg.norm(CEN-(q+np.outer(foot,v)),axis=1)-R
        dd[[ZERO,j]]=np.inf
        if min(dd)<-1e-8:return False
    return True

def observables(R,centers,angles):
    data=action(R,centers,angles);n,vs,ts=data[5],data[7],data[8]
    cs=np.array([vs[0]@n[0]]+[-vs[i-1]@n[i] for i in range(1,len(n))])
    cls=[]
    for i,v in enumerate(vs):
        q=R*n[i];j=int(np.argmin(np.linalg.norm(CEN-(centers[i+1]-centers[i]),axis=1)))
        foot=np.clip((CEN-q)@v,0,ts[i]);dist=np.linalg.norm(CEN-(q+np.outer(foot,v)),axis=1)-R
        dist[[ZERO,j]]=np.inf;cls.append(float(min(dist)))
    M=np.array([[1.,ts[0]],[0.,1.]])
    for i in range(1,len(ts)):
        M=np.array([[1.,ts[i]],[0.,1.]])@np.array([[1.,0.],[2/(R*cs[i]),1.]])@M
    return cs,np.array(cls),ts,float(R*cs[0]*cs[-1]/M[0,1])

def cutoff(x):
    if x<=1:return 0.
    if x>=2:return 1.
    u=x-1.;logit=1/(1-u)-1/u
    if logit>=0:return 1/(1+math.exp(-logit))
    e=math.exp(logit);return e/(1+e)

def guard(cs,cls,eps):
    m=len(cls);H=1.
    for i,c in enumerate(cs):H*=cutoff(c/(eps*float(Q0)**(min(i,m-i)/4)))
    for i,c in enumerate(cls):H*=cutoff(c/(eps*float(Q0)**(min(i,m-1-i)/4)))
    return 1-H

def observable_checks(o,eta,a,ap,am,dp,dm,h):
    R=o['R'];m=o['m'];centers=o['centers'];base=action(R,centers,a)
    cs,cl,ts,omega=observables(R,centers,a)
    cp,clp,tp,wp=observables(R,centers,ap);cm,clm,tm,wm=observables(R,centers,am)
    s=np.array([float(SIG)**i+float(SIG)**(m-i) for i in range(m+1)])
    xi=base[4]@eta;n,t,vs=base[5:8];dc=[];dt=[]
    dv=[]
    for i,v in enumerate(vs):
        dX=R*(t[i+1]*xi[i+1]-t[i]*xi[i]);dt.append(float(v@dX));dv.append((np.eye(2)-np.outer(v,v))@dX/ts[i])
    for i in range(m):dc.append(float(dv[i]@n[i]+vs[i]@t[i]*xi[i]))
    dc.append(float(-dv[-1]@n[-1]-vs[-1]@t[-1]*xi[-1]));dc=np.array(dc);dt=np.array(dt)
    incidence_error=float(max(abs((cp-cm)/(2*h)-dc)))
    require(incidence_error<2e-5,'physical incidence chain rule')
    require(max(abs(dc)-float(CC)*s*max(abs(eta)))<1e-7,'physical incidence derivative bound')
    require(max(abs(dt)-float(RP*J)*(s[:-1]+s[1:])*max(abs(eta)))<1e-7,'physical flight derivative bound')
    clearance_ratio=float(max(abs((clp-clm)/(2*h))/(float(RP*J)*np.maximum(s[:-1],s[1:])*max(abs(eta)))))
    require(clearance_ratio<1+1e-4,'true minimum-clearance derivative bound including switches')
    M=np.array([[1.,ts[0]],[0.,1.]]);dM=np.array([[0.,dt[0]],[0.,0.]])
    for i in range(1,m):
        S=np.array([[1.,ts[i]],[0.,1.]]);dS=np.array([[0.,dt[i]],[0.,0.]])
        k=2/(R*cs[i]);C=np.array([[1.,0.],[k,1.]]);dC=np.array([[0.,0.],[-k*dc[i]/cs[i],0.]])
        dM=dS@C@M+S@dC@M+S@C@dM;M=S@C@M
    dlog=dc[0]/cs[0]+dc[-1]/cs[-1]-dM[0,1]/M[0,1]
    logerr=abs((math.log(wp)-math.log(wm))/(2*h)-dlog)
    require(logerr<2e-5,'log optical denominator physical finite difference')
    depth=np.minimum(np.arange(m+1),np.arange(m,-1,-1));flightdepth=np.minimum(np.arange(m),np.arange(m-1,-1,-1))
    eps=.7*min(float(min(cs/float(Q0)**(depth/4))),float(min(cl/float(Q0)**(flightdepth/4))))
    require(eps>0,'positive original guard diagnostic scale')
    gd=abs((guard(cp,clp,eps)-guard(cm,clm,eps))/(2*h))
    # For u<=1/2, theta' <= exp(2-1/u)*(u^-2+4)<=8; use symmetry otherwise.
    # The native theorem retains the actual symbolic supremum M_Theta.
    CW=4*8*float(CC+CD)/(1-float(SIG)/float(Q0)**.25)
    require(gd<=CW/eps*max(abs(eta)),'unchanged physical guard variation')
    return {'incidence_finite_difference_error':incidence_error,'minimum_clearance_bound_ratio':clearance_ratio,
        'log_optical_finite_difference_error':logerr,'fixed_diagnostic_guard_epsilon':eps,
        'guard_directional_difference':gd,'guard_model':'one explicit admissible smooth cutoff, all original factors retained'}

def physical():
    rng=np.random.default_rng(1608289);rows=[];fd_errors=[];third_errors=[];mininc=1.;ratiomax=0.;skips=0
    for run in range(120):
        R=[.45,.46,.47][run%3];m=[1,2,3,4,7,12,20,32][run%8]
        alpha=float(rng.uniform(-math.pi,math.pi));p=float(rng.uniform(-.92,.92))
        if run%10==0:alpha=0.;p=0.;m=[2,8,20,32][(run//10)%4]
        elif run%10==1:p=1-1e-8
        o=trace(alpha,p,R,m);a=o['angles'];data=action(R,o['centers'],a);_,g,H,G,L,*_=data
        require(m<2 or np.max(abs(g[1:-1]))<2e-9,'actual specular stationarity')
        cs=np.array(o['incidences']);ts=np.array(o['flights']);s=np.array([float(SIG)**i+float(SIG)**(m-i) for i in range(m+1)])
        require(np.max(abs(L)-float(J)*s[:,None])<1e-7,'actual unweighted Jacobi bound')
        for k in range(2):
            weighted=(float(SIG)**np.arange(m+1)*cs[0] if k==0 else float(SIG)**np.arange(m,-1,-1)*cs[-1])
            require(np.max(abs(L[:,k])*cs-weighted)<2e-7,'actual weighted Jacobi bound')
        ratio=float(np.max(abs(L)/(float(J)*s[:,None])));ratiomax=max(ratiomax,ratio);mininc=min(mininc,float(min(cs)))
        eta=np.array([.7,-.9]);dq=L@eta
        A=np.array([[third(R,o['centers'],a,[L[:,i],L[:,j],dq]) for j in range(2)]for i in range(2)])
        require(np.max(abs(A))<=float(CF)*np.max(abs(eta)),'actual third-variation bound')
        one={'R':R,'m':m,'alpha0':alpha,'p0':p,'word':o['word'],'incidences':o['incidences'],'flights':o['flights'],
          'clearances':o['clearances'],'roof':o['physical_roof'],'return_count':o['return_count'],
          'displacement_label':o['displacement_label'],'initial_section':o['initial_section'],'terminal_section':o['terminal_section'],
          'max_contact_error':o['contact_error'],'jacobi_bound_ratio':ratio,'third_tensor_directional':A.tolist()}
        if m<=12 and min(cs)>.025:
            h=2e-6;ap,dp=solve_endpoint(o,h*eta);am,dm=solve_endpoint(o,-h*eta)
            if physical_valid(R,o['centers'],ap) and physical_valid(R,o['centers'],am):
                diff=(ap-am)/(2*h);err=float(np.max(abs(diff-dq))/max(1.,float(np.max(abs(dq)))))
                err3=float(np.linalg.norm((dp[3]-dm[3])/(2*h)-A)/max(1.,float(np.linalg.norm(A))))
                require(err<3e-5,'actual stationary Jacobi finite difference')
                require(err3<3e-4,'actual third-Schur finite difference')
                fd_errors.append(err);third_errors.append(err3);one['finite_difference']={'step':h,'Jacobi_error':err,'third_Schur_error':err3};one['physical_observable_checks']=observable_checks(o,eta,a,ap,am,dp,dm,h)
            else:skips+=1;one['finite_difference_status']='perturbed physical domain failed; not counted as pass'
        else:one['finite_difference_status']='not selected: length or conditioning safeguard'
        rows.append(one)
    return dict(actual_physical_records=len(rows),actual_flights=sum(r['m'] for r in rows),
        actual_original_section_to_section_records=sum(r['initial_section'] and r['terminal_section'] for r in rows),
        smallest_sampled_incidence=mininc,max_jacobi_bound_ratio=ratiomax,
        actual_same_physical_word_finite_differences=len(fd_errors),
        incidence_clearance_optical_guard_checks=sum('physical_observable_checks' in r for r in rows),
        maximum_Jacobi_finite_difference_error=max(fd_errors,default=0.),
        maximum_third_Schur_finite_difference_error=max(third_errors,default=0.),
        rejected_perturbed_physical_domains=skips,
        enclosure='all lattice centers norm<=9; horizon<28/5 and radius<=47/100 pay excluded centers',
        scope='floating physical diagnostics, not rigorous interval integration or a continuum proof'),rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path);a=ap.parse_args()
    ex=exact();ph,rows=physical()
    result={'status':'passed','exact_algebra':ex,'physical':ph,'continuum_proof_certified_by_script':False,
        'full_raw_pointwise_LLT_proved':False,'full_four_coordinate_inversion_completed':False}
    if a.details:a.details.parent.mkdir(parents=True,exist_ok=True);a.details.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
