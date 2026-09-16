#!/usr/bin/env python3
"""Independent finite controls for A2 v65. Requires sympy and numpy.
No manuscript checker is imported. These are not infinite-dimensional proofs.
Run normally or with python -O; no removable assert statements are used.
"""
import json, math
from fractions import Fraction as F
import numpy as np
import sympy as sp

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def maxnorm(M):
    return max(sum(abs(x) for x in M.row(i)) for i in range(M.rows))

def cyclic_blocks():
    cases=0;sign_controls=0;riccati_cases=0
    for r in range(2,8):
        aa=[sp.Rational(1,3)+sp.Rational(i,20*r) for i in range(r)]
        kk=[sp.Rational(1)+sp.Rational(i,10*r) for i in range(r)]
        cc=[(kk[(i-1)%r]*(1/aa[(i-1)%r]-1)-kk[i]*(1-aa[i]))/2 for i in range(r)]
        require(all(x>0 for x in cc),'Nonpositive constructed Jacobi mass')
        Ja=sp.zeros(r);Jc=sp.zeros(r)
        for i in range(r):
            j=(i+1)%r;den=kk[i]+kk[j]+2*cc[j]-kk[j]*aa[j]
            require(aa[i]*den==kk[i],'Riccati reference identity')
            Ja[i,i]=den;Ja[i,j]=-aa[i]*kk[j];Jc[i,j]=2*aa[i]
        da=-Ja.inv()*Jc
        Ds=sp.eye(r)-sp.diag(*kk)*da
        T2=sp.zeros(r)
        for i in range(r): T2[i,(i+1)%r]=aa[i]**2
        require(Ds==(sp.eye(r)+T2)*(sp.eye(r)-T2).inv(),'Curvature Jacobian from implicit Riccati differentiation')
        riccati_cases+=1
        patterns=[[1]*r,[-1]*r,[(-1)**i for i in range(r)],[-1]+[1]*(r-1)]
        for signs in patterns:
            ss=[a*s for a,s in zip(aa,signs)];lam=sp.prod(ss)
            for n in range(2,12):
                T=sp.zeros(r)
                for i in range(r): T[i,(i+1)%r]=ss[i]**n
                I=sp.eye(r);C=(I+T)*(I-T).inv();Ci=(I-T)*(I+T).inv()
                require(T**r==lam**n*I,'Cyclic monodromy')
                require(C*Ci==I,'Cayley inverse')
                det=(1-(-1)**r*lam**n)/(1-lam**n)
                require(C.det()==det and det>0,'Cyclic determinant')
                bound=(1+max(aa)**n)/(1-max(aa)**n)
                require(maxnorm(C)<=bound and maxnorm(Ci)<=bound,'Homogeneous row-sum bound')
                require(C==2*sum((T**j for j in range(r)),sp.zeros(r))/(1-lam**n)-I,'Periodic visit sum')
                if r%2 and n%2 and signs==[-1]*r:
                    absT=-T;wrong=(I+absT)*(I-absT).inv()
                    require(C!=wrong,'Odd sign-erasure control');sign_controls+=1
                cases+=1
    return {'exact_blocks':cases,'exact_riccati_curvature_jacobians':riccati_cases,'odd_cycle_sign_erasure_controls':sign_controls,'three_sites_sigma_minus_one_half_order_three_det':'511/513','scope':'Constructed positive scalar Jacobi parameters; no arbitrary rational tuple is asserted globally realized.'}

def density_ratios():
    u,v=sp.symbols('u v');xs=[sp.Rational(i,30) for i in range(-3,4)]
    cases=0;axes=0;offset_bad=0
    for phase in range(3):
        p=sp.Rational(phase-1,5)
        A=-p*u+(phase+2)*u**2/2+u**3/3
        C=p*v+(phase+3)*v**2/2-v**3/4
        B=1+u/3+u**2/5;D=1-v/7+v**2/9
        for d1,d2 in [(sp.Rational(1,4),sp.Rational(1,2)),(sp.Rational(1,3),sp.Rational(3,4))]:
            def density(d):
                numerator=sp.expand(B*D*(d-A-C))
                Z=sp.integrate(numerator,(u,-sp.Rational(1,10),sp.Rational(1,10)),(v,-sp.Rational(1,10),sp.Rational(1,10)))
                return numerator/Z
            f,g=density(d1),density(d2)
            f0=f.subs({u:0,v:0});g0=g.subs({u:0,v:0})
            for x in xs:
                for y in xs:
                    av=A.subs(u,x);cv=C.subs(v,y)
                    fv=f.subs({u:x,v:y});gv=g.subs({u:x,v:y})
                    require(fv>0 and gv>0,'Density positivity')
                    Q=fv*g0/(gv*f0);H=d1*d2*(1-Q)/(d2-d1*Q)
                    require(H==av+cv,'Two-offset action separation');cases+=1
                    if y==0:
                        amp=fv/f0*d1/(d1-av)
                        require(amp==B.subs(u,x),'Axis amplitude extraction');axes+=1
                    if x:
                        # A changed second-offset efficiency. Its normalization cancels from Q.
                        Qbad=Q/(1+x/20);Hbad=d1*d2*(1-Qbad)/(d2-d1*Qbad)
                        require(Hbad!=av+cv,'Offset-dependent nuisance control');offset_bad+=1
    return {'exact_normalized_density_identities':cases,'exact_axis_amplitudes':axes,'offset_dependent_efficiency_negative_controls':offset_bad,'scope':'Polynomial positive normalized laws; changed-efficiency examples lie outside the printed common-amplitude model.'}

def geometry(vertices,curvature,cubic,quartic):
    points=np.array(vertices,float);edges=np.roll(points,-1,axis=0)-points
    lengths=np.linalg.norm(edges,axis=1);e=edges/lengths[:,None]
    normals=e-np.roll(e,1,axis=0);normals/=np.linalg.norm(normals,axis=1)[:,None]
    tangents=np.c_[-normals[:,1],normals[:,0]]
    nu=np.sum(e*normals,axis=1);p=np.sum(e*tangents,axis=1)/nu
    eps=[]
    for i in range(3):
        j=(i+1)%3;tr=tangents[i]@tangents[j]-(e[i]@tangents[i])*(e[i]@tangents[j])
        eps.append(int(np.sign(tr)))
        require(abs(abs(tr)-nu[i]*nu[j])<2e-14,'Transverse product magnitude')
    require(np.prod(eps)==-1,'Odd physical orientation product')
    return points,lengths,normals,tangents,nu,p,np.array(eps),np.array(curvature)/nu,np.array(cubic),np.array(quartic)

def stable_ratios(k,c):
    a=np.zeros(3)
    for _ in range(1000):
        b=np.array([k[i]/(k[i]+k[(i+1)%3]+2*c[(i+1)%3]-k[(i+1)%3]*a[(i+1)%3]) for i in range(3)])
        if np.max(abs(b-a))<2e-15: return b
        a=b
    raise RuntimeError('Riccati iteration did not converge')

def geometric_envelopes():
    triangles=[[(0,0),(6,0),(3,3*math.sqrt(3))],[(0,0),(7,0),(1.8,6)]]
    records=[];worst=0.;wrong_hits=0;curvature_worst=0.;block_worst=0.
    for gi,vertices in enumerate(triangles):
        geom=geometry(vertices,[1.,.85,1.2],[.23,-.17,.31],[.4,.25,.35])
        points,lens,normals,tang,nu,p,eps,c,cubic,quartic=geom;k=1/lens
        a=stable_ratios(k,c);sig=eps*a
        T=np.zeros((3,3))
        for i in range(3): T[i,(i+1)%3]=sig[i]**2
        C2=np.linalg.solve((np.eye(3)-T).T,(np.eye(3)+T).T).T
        def hess(cv): return k+cv-k*stable_ratios(k,cv)
        J=np.empty((3,3));dc=1e-5
        for i in range(3):
            v=np.eye(3)[i];J[:,i]=(hess(c+dc*v)-hess(c-dc*v))/(2*dc)
        ce=float(np.max(abs(J-C2)));curvature_worst=max(curvature_worst,ce)
        require(ce<2e-9,'Geometric curvature Jacobian')
        for b in range(3):
            for N in [12,18]:
                ids=(b+np.arange(N+1))%3;ei=ids[:-1]
                for degree in [2,3,4]:
                    z=np.array([1.,-.45,.65]);z[b]=1.;fac=math.factorial(degree)
                    def solve(u,par):
                        def evaluate(x):
                            cs=c[ids];cu=cubic[ids];qu=quartic[ids]
                            f=cs*x*x/2+cu*x**3/6+qu*x**4/24+par*z[ids]*x**degree/fac
                            fp=cs*x+cu*x*x/2+qu*x**3/6+par*z[ids]*x**(degree-1)/math.factorial(degree-1)
                            fpp=cs+cu*x+qu*x*x/2+par*z[ids]*x**(degree-2)/math.factorial(degree-2)
                            dis=(tang[ids]*x[:,None]-normals[ids]*f[:,None])/nu[ids,None]
                            vel=(tang[ids]-normals[ids]*fp[:,None])/nu[ids,None]
                            base=points[ids[1:]]-points[ids[:-1]];dd=np.diff(dis,axis=0);ch=base+dd
                            lengths=np.linalg.norm(ch,axis=1);dirs=ch/lengths[:,None]
                            # Stable chord increment instead of subtracting two nearly equal lengths.
                            inc=(2*np.sum(base*dd,axis=1)+np.sum(dd*dd,axis=1))/(lengths+lens[ei])
                            action=float(np.sum(inc+p[ids[:-1]]*x[:-1]-p[ids[1:]]*x[1:]))
                            acc=-normals[ids]*fpp[:,None]/nu[ids,None]
                            dl=np.sum(dirs*vel[:-1],axis=1);dr=np.sum(dirs*vel[1:],axis=1)
                            ll=(np.sum(vel[:-1]**2,axis=1)-dl*dl)/lengths-np.sum(dirs*acc[:-1],axis=1)
                            rr=(np.sum(vel[1:]**2,axis=1)-dr*dr)/lengths+np.sum(dirs*acc[1:],axis=1)
                            lr=-(np.sum(vel[:-1]*vel[1:],axis=1)-dl*dr)/lengths
                            H=np.diag(rr[:-1]+ll[1:])+np.diag(lr[1:-1],1)+np.diag(lr[1:-1],-1)
                            return action,dirs,vel,H
                        def grad(y):
                            x=np.r_[u,y,0.];ac,di,ve,H=evaluate(x)
                            return np.sum((di[:-1]-di[1:])*ve[1:-1],axis=1)
                        initial=[];prod=u
                        for i in range(N-1): prod*=sig[(b+i)%3];initial.append(prod)
                        y=np.array(initial)
                        for iteration in range(12):
                            g=grad(y)
                            if np.max(abs(g))<2e-14: break
                            H=evaluate(np.r_[u,y,0.])[3]
                            y-=np.linalg.solve(H,g)
                        residual=float(np.max(abs(grad(y))))
                        require(residual<3e-13,'Stationary chord residual')
                        x=np.r_[u,y,0.];action,di,ve,H=evaluate(x)
                        et=z[ids]*x**degree/fac
                        weightsleft=np.sum(di*normals[ids[:-1]],axis=1)/nu[ids[:-1]]
                        weightsright=-np.sum(di*normals[ids[1:]],axis=1)/nu[ids[1:]]
                        env=float(np.sum(weightsleft*et[:-1]+weightsright*et[1:]))
                        return action,env,weightsleft[0]*et[0],residual
                    for u in [-.06,.06]:
                        ac,env,initialterm,residual=solve(u,0.)
                        step=2e-4
                        difference=(solve(u,step)[0]-solve(u,-step)[0])/(2*step)
                        er=abs(env-difference)/max(abs(env),1e-14);worst=max(worst,er)
                        require(er<4e-6,'Actual geometric envelope shape derivative')
                        require(abs(difference-env-initialterm)>abs(initialterm)*.9,'Double initial visit negative control');wrong_hits+=1
                        records.append({'triangle':gi,'phase':b,'flights':N,'degree':degree,'u':u,'relative_error':er,'stationarity_residual':residual})
                    u0=.01
                    ep=solve(u0,0.)[1];em=solve(-u0,0.)[1]
                    homogeneous=(ep+(-1)**degree*em)/(2*u0**degree/fac)
                    Tn=np.zeros((3,3))
                    for i in range(3):Tn[i,(i+1)%3]=sig[i]**degree
                    Cn=np.linalg.solve(np.eye(3)-Tn,np.eye(3)+Tn)
                    be=abs(homogeneous-(Cn@z)[b]);block_worst=max(block_worst,be)
                    require(be<3e-4,'Finite small-endpoint cyclic response comparison')
    return {'finite_stationary_configurations':len(records),'initial_visit_negative_controls':wrong_hits,'worst_relative_envelope_error':worst,'worst_curvature_jacobian_absolute_error':curvature_worst,'worst_small_endpoint_cyclic_absolute_error':block_worst,'records':records,'scope':'Actual Euclidean chords on local polynomial graph arcs, finite stationary chains and finite differences; not a global realization or infinite-limit certificate.'}

def polar_realization():
    theta,delta,eta=sp.symbols('theta delta eta', real=True)
    R=1+delta*(1-sp.cos(theta))*(1+eta*sp.sin(theta))
    first=sp.diff(R,theta);second=sp.diff(first,theta)
    curvature0=sp.simplify(((R**2+2*first**2-R*second)/(R**2+first**2)**sp.Rational(3,2)).subs(theta,0))
    require(curvature0==1-delta,'Exact polar contact curvature')
    lower=[]
    for d,e in [(F(1,50),F(1,5)),(F(1,20),F(1,4)),(F(1,40),F(1,3))]:
        D=2*d*(1+e);floor=(1-D)**2-(1+D)*d*(1+5*e)
        require(1-D>0 and floor>0,'Uniform polar curvature numerator bound')
        lower.append({'abs_delta':str(d),'abs_eta':str(e),'curvature_numerator_floor':str(floor)})
    return {'curvature_at_contact':'1-delta','uniform_convexity_bounds':lower,'scope':'Exact contact formula and conservative analytic global convexity bounds; full lattice-clearance persistence uses the manuscript geometric margins.'}

if __name__=='__main__':
    result={'scope':'Independent finite controls, not proofs of function-space inversion, trace-class limits, or global rigidity. No manuscript checker imported.','cyclic':cyclic_blocks(),'two_offset':density_ratios(),'geometric':geometric_envelopes(),'polar':polar_realization()}
    print(json.dumps(result,indent=2,sort_keys=True))
