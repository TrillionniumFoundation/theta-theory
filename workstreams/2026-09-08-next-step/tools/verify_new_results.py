#!/usr/bin/env python3
"""Independent finite diagnostics for the September 8 execution.

Exact identities are separated from floating quadrature. This is not a proof
assistant, a verification of the continuum theorems, or a novelty certificate.
Requires Python 3.10+, NumPy and SymPy. Run normally and with python -O.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import unittest
import io
import numpy as np
import sympy as s


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def a2_quadrature(R: float, n: int = 160, T: float = .11) -> dict[str, float]:
    """Gauss quadrature on the actual six short-flight sectors; NOT intervals."""
    if not .45 <= R <= .47 or T != .11 or n < 8:
        raise ValueError('This diagnostic uses the stated radius interval and T=.11')
    x,w=np.polynomial.legendre.leggauss(n)
    alpha_max=np.arccos((1-2*R*T-T*T)/(2*R))
    alpha=alpha_max*x[:,None]
    nx,ny=np.cos(alpha),np.sin(alpha)
    dx,dy=1-R*nx,-R*ny
    distance=np.sqrt(dx*dx+dy*dy)
    psi=np.arctan2(dy,dx)
    beta=np.arccos(np.clip((distance**2+T*T-R*R)/(2*distance*T),-1.,1.))
    theta=psi+beta*x[None,:]
    vx,vy=np.cos(theta),np.sin(theta)
    L=dx*vx+dy*vy
    impact=dx*(-vy)+dy*vx
    root=np.sqrt(R*R-impact*impact)
    tau=L-root
    n1x=(R*nx+tau*vx-1)/R
    n1y=(R*ny+tau*vy)/R
    cosine=np.cos(theta-alpha)
    end_cos=-(n1x*vx+n1y*vy)
    tau_prime=(1-n1x*nx-n1y*ny)/(n1x*vx+n1y*vy)
    weight=6/(4*np.pi)*alpha_max*beta*cosine*w[:,None]*w[None,:]
    J=float(np.sum(weight*(T-tau)))
    Jp=float(np.sum(weight*(-tau_prime)))
    area=np.sqrt(3)/2-np.pi*R*R
    intensity=2*R/area
    intensity_p=2*(np.sqrt(3)/2+np.pi*R*R)/area**2
    p2=intensity*J; p1=intensity*T-2*p2; p0=1-p1-p2
    return dict(R=R,T=T,J=J,J_prime=Jp,p0=p0,p1=p1,p2=p2,
                p2_prime=intensity_p*J+intensity*Jp,
                min_start_cos=float(cosine.min()),min_end_cos=float(end_cos.min()),
                max_tau=float(tau.max()))


class DynamicsAudit(unittest.TestCase):
    def test_green_kubo_derivatives_exact(self):
        p=s.symbols('p');lam=2*p-1
        for n in (1,2,3,7):
            direct=1+2*sum((1-s.Rational(k,n))*lam**k for k in range(1,n))
            formula=p/(1-p)-2*lam*(1-lam**n)/(n*(1-lam)**2)
            for j in range(4):
                require(s.simplify(s.diff(direct-formula,p,j))==0,'covariance jet')

    def test_martingale_boundary_exact(self):
        lam=F(2,5)
        for N in range(1,8):
            for word in product((-1,1),repeat=N+1):
                D=sum((F(word[k])-lam*word[k-1])/(1-lam) for k in range(1,N+1))
                Y=sum(word[1:])
                remainder=lam/(1-lam)*(word[0]-word[-1])
                require(F(Y)-D==remainder,'boundary cancellation')

    def test_markov_bridge_cannot_be_deleted(self):
        p=s.symbols('p');P=s.Matrix([[p,1-p],[1-p,p]])
        eps=s.Matrix([-1,1]);pi=s.diag(s.Rational(1,2),s.Rational(1,2))
        cov=(eps.T*pi*P**3*eps)[0]
        require(s.expand(cov-(2*p-1)**3)==0,'bridge correlation')
        require(s.diff(cov,p).subs(p,s.Rational(3,4))!=0,'nonzero bridge derivative')

    def test_physical_two_time_integral(self):
        p,y=s.symbols('p y')
        terms=[p*p*y**2/2,(1-p)**2*y**2/2,
               (1-p)*y*(p+(1-p)*y)/2,p*y*(1-p+p*y)/2]
        integral=s.integrate(sum(terms),(y,0,1))
        require(s.simplify(integral-(s.Rational(1,3)-p*(1-p)/6))==0,'physical integral')
        require(s.simplify(s.diff(integral,p)-(2*p-1)/6)==0,'physical derivative')

    def test_perron_endpoint_numerical(self):
        P=np.array([[.63,.37],[.37,.63]]);q=.4
        A=P*np.exp(q*np.array([[0,1],[0,1]]))
        values,vectors=np.linalg.eig(A);ix=int(np.argmax(values.real));lam=values[ix].real
        r=vectors[:,ix].real;r=r/r.sum()
        vl,ll=np.linalg.eig(A.T);l=ll[:,np.argmin(abs(vl-lam))].real;l=l/(l@r)
        Pq=A*r[None,:]/(lam*r[:,None]);piq=l*r
        for word in product((0,1),repeat=6):
            left=.5;right=piq[word[0]]
            for i,j in zip(word,word[1:]):left*=P[i,j]*np.exp(q*j);right*=Pq[i,j]
            right*=lam**5*(.5*r[word[0]])/(piq[word[0]]*r[word[-1]])
            require(abs(left-right)<1e-13,'Perron endpoints')


class SuspensionAndLorentz(unittest.TestCase):
    def test_stationary_tail_identity_exact(self):
        roofs=[F(7,100),F(9,100),F(8,100)]
        mean=sum(roofs)/3
        for horizon in (F(1,100),F(11,100),F(22,100),F(33,100)):
            for k in range(1,8):
                actual=F(0);Aprev=F(0);Anext=F(0)
                for i in range(3):
                    total=sum(roofs[(i+j)%3] for j in range(k))
                    actual+=max(F(0),min(roofs[i],roofs[i]-(total-horizon)))
                    prev=sum(roofs[(i+j)%3] for j in range(k-1))
                    Aprev+=max(F(0),horizon-prev)
                    Anext+=max(F(0),horizon-total)
                require(actual/(3*mean)==(Aprev-Anext)/(3*mean),'stationary tail')
            count=F(0)
            for k in range(1,8):
                for i in range(3):
                    total=sum(roofs[(i+j)%3] for j in range(k))
                    count+=max(F(0),min(roofs[i],roofs[i]-(total-horizon)))/(3*mean)
            require(count==horizon/mean,'stationary intensity')

    def test_two_hit_law_exact(self):
        roofs=[F(7,100),F(9,100),F(8,100)];T=F(11,100);mean=sum(roofs)/3
        J=sum(max(F(0),T-r) for r in roofs)/3
        p2=J/mean;p1=T/mean-2*p2;p0=1-T/mean+p2
        require(p0+p1+p2==1,'normalization')
        require(p1+2*p2==T/mean,'mean count')
        require(p1+p2!=T/mean,'do not iterate one-collision hit probability')
        require(min(p0,p1,p2)>=0,'positivity')

    def test_analytic_rational_margins(self):
        R=F(47,100);T=F(11,100)
        require((1-2*R-T*T)/(2*R*T)==F(479,1034),'cosine constant')
        require(F(479,1034)>F(46,100),'strict transversality')
        require(F(3,50)<T<2*F(3,50),'two-event window')
        require(F(9,10)*F(9,1000)/4000000>F(1,10**9),'two-hit lower bound')
        require(F(43,50)-F(22,7)*R*R>F(16,100),'area lower bound')

    def test_radius_root_derivative(self):
        for R in (.451,.46,.469):
            for alpha,theta in ((0.,0.),(.03,-.02),(-.05,.04)):
                def entry(radius):
                    n=np.array([np.cos(alpha),np.sin(alpha)]);v=np.array([np.cos(theta),np.sin(theta)])
                    d=np.array([1.,0.])-radius*n
                    L=d@v;b=d@np.array([-v[1],v[0]])
                    tau=L-np.sqrt(radius*radius-b*b)
                    end=(radius*n+tau*v-np.array([1.,0.]))/radius
                    derivative=(1-end@n)/(end@v)
                    return tau,derivative
                tau,deriv=entry(R);h=1e-6
                finite=(entry(R+h)[0]-entry(R-h)[0])/(2*h)
                require(abs(finite-deriv)<1e-8,'implicit radius derivative')
                require(deriv<0 and tau<.11,'actual active test')

    def test_sector_quadrature_convergence(self):
        for R in (.45,.46,.47):
            lo=a2_quadrature(R,96);hi=a2_quadrature(R,192)
            require(abs(lo['p2']-hi['p2'])<2e-7,'quadrature stabilization')
            require(min(hi['p0'],hi['p1'],hi['p2'])>0,'count positivity')
            require(hi['p2']>1e-9 and hi['p2_prime']>0,'positive response')
            require(min(hi['min_start_cos'],hi['min_end_cos'])>479/1034,'geometric lower margin')

    def test_integrated_first_response(self):
        R=.46;h=2e-5
        mid=a2_quadrature(R,200)
        finite=(a2_quadrature(R+h,200)['J']-a2_quadrature(R-h,200)['J'])/(2*h)
        require(abs(finite-mid['J_prime'])<2e-6,'integrated first response')


class ChronologicalContacts(unittest.TestCase):
    def test_rod_elimination_and_metric_exact(self):
        A=s.Matrix([[-1,0],[1,-1]]);B=s.Matrix([[-1,1,0],[0,-1,1]])
        K=A.inv()*B;H=s.eye(3)+K.T*K;S=s.Matrix([[-1,0,1]])
        require(-K==s.Matrix([[-1,1,0],[-1,0,1]]),'rod derivatives')
        require(H.det()==8,'graph metric')
        require((S*H.inv()*S.T)[0]==s.Rational(5,8),'intrinsic Jacobian')
        D=A.row_join(B).col_join(s.Matrix([[0,1,0,0,0]]))
        require((D*D.T).det()==5,'joint Jacobian')

    def test_schur_rank_and_gram_exact(self):
        A=s.Matrix([[2,0,0],[1,-3,0],[-2,1,4]])
        B=s.Matrix([[1,2,0,1],[0,1,1,-1],[2,0,1,3]])
        Gt=s.Matrix([[1,0,2],[0,2,-1]])
        Gz=s.Matrix([[0,1,2,0],[1,0,1,2]])
        K=A.inv()*B;S=Gz-Gt*K;H=s.eye(4)+K.T*K
        D=A.row_join(B);allD=D.col_join(Gt.row_join(Gz))
        require(allD.rank()==3+S.rank(),'surplus rank')
        require(s.simplify((allD*allD.T).det()-(D*D.T).det()*(S*H.inv()*S.T).det())==0,'coarea Schur')
        require((D*D.T).det()==A.det()**2*H.det(),'event coarea')

    def test_redundant_closure_is_rejected(self):
        A=s.Matrix([[1,0],[3,2]]);B=s.Matrix([[1,2,3],[0,1,1]]);C=s.Matrix([[2,1]])
        S=C*B-C*A*A.inv()*B
        require(S==s.zeros(1,3),'redundant closure')
        require(A.det()!=0,'good time inverse does not imply surplus')

    def test_inverse_bound_exact(self):
        for m in range(1,7):
            A=s.eye(m)*2
            for i in range(m):
                for j in range(i): A[i,j]=(-1)**(i+j)*3
            actual=max(sum(abs(v) for v in row) for row in A.inv().tolist())
            bound=s.Rational(1,2)*s.Rational(5,2)**(m-1)
            require(actual<=bound,'triangular inverse bound')

    def test_forest_uniform_bound_exact(self):
        normals=[(s.Rational(1),s.Rational(0)),(s.Rational(3,5),s.Rational(4,5))]
        for edges in ([(0,1),(1,2),(2,3)],[(0,1),(0,2),(0,3)]):
            m=len(edges);R=s.zeros(m,8)
            for row,(i,j) in enumerate(edges):
                for k,n in enumerate(normals[row%2]): R[row,2*i+k]=-n;R[row,2*j+k]=n
            require(R.rank()==m,'forest independent')
            for entries in product((-1,0,1),repeat=m):
                v=s.Matrix(entries);b=R.T*v
                require((b.T*b)[0]*m*(m+1)>=(v.T*v)[0],'forest metric bound')

    def test_implicit_second_jet(self):
        a=s.symbols('a');t=s.Matrix([a**2+s.exp(a),s.sin(a)])
        # F = A(t - exact(a)); coefficient extraction must return exact jets.
        A=s.Matrix([[2,0],[a,3]]);h=s.symbols('h');a0=s.Rational(0)
        approx=t.subs(a,a0)+h*t.diff(a).subs(a,a0)
        residual=(A.subs(a,h)*(approx-t.subs(a,h)))
        coeff=s.Matrix([s.expand(s.series(v,h,0,3).removeO()).coeff(h,2) for v in residual])
        recovered=-2*A.subs(a,0).inv()*coeff
        require(recovered==t.diff(a,2).subs(a,0),'implicit jet recursion')


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();stream=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    output.with_suffix('.log').write_text(stream.getvalue())
    record={'status':'PASS' if result.wasSuccessful() else 'FAIL',
            'test_cases':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
            'skips':len(result.skipped),'quadrature':'floating Gauss-Legendre; not directed intervals',
            'samples':[a2_quadrature(R,192) for R in (.45,.46,.47)],
            'scope':'Independent finite exact and floating diagnostics; not proofs of continuum or long-time theorems.'}
    output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,indent=2))
    if not result.wasSuccessful(): raise SystemExit(1)

if __name__=='__main__':main()
