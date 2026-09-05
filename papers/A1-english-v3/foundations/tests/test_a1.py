"""Finite independent checks for A1 English edition 2.0.

Exact checks use Fraction or SymPy. Floating checks state their tolerance and
use elementary identities or independent quadrature; they do not certify the
infinite-dimensional theorems or any long-time billiard claim.
Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations
import itertools
import math
import unittest
from fractions import Fraction as F

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import expit, logsumexp


def kl(q, p):
    q, p = np.asarray(q, float), np.asarray(p, float)
    positive = q > 0
    if np.any(p[positive] <= 0):
        return math.inf
    return float(np.sum(q[positive] * np.log(q[positive] / p[positive])))


def tilt(p, v):
    p, v = np.asarray(p, float), np.asarray(v, float)
    logz = float(logsumexp(np.log(p) + v))
    return np.exp(np.log(p) + v - logz), logz


def capped_density(p, m, cap):
    p, m = np.asarray(p, float), np.asarray(m, float)
    if cap < 1 or not np.isclose(p.sum(), 1):
        raise ValueError('A probability and cap >= 1 are required')
    if cap == 1:
        return np.ones_like(p)
    root = brentq(lambda t: np.dot(p, np.minimum(cap, np.exp(t + m))) - 1,
                  -100 - float(np.max(abs(m))), 100 + float(np.max(abs(m))),
                  xtol=1e-14)
    return np.minimum(cap, np.exp(root + m))


class SelectionChecks(unittest.TestCase):
    def setUp(self):
        self.p = np.array([.1, .2, .3, .4])
        self.v = np.array([-.7, .3, 1.1, -.2])

    def test_gibbs_identity(self):
        q = np.array([.4, .1, .2, .3])
        star, z = tilt(self.p, self.v)
        self.assertAlmostEqual(z - q @ self.v + kl(q, self.p), kl(q, star), places=13)

    def test_partition_gradient_and_hessian(self):
        p = np.array([.2, .3, .5]); c = np.array([-1., 0., 2.]); a = .4
        q, _ = tilt(p, a*c)
        x = sp.symbols('x'); Z = sp.Rational(1,5)*sp.exp(-x)+sp.Rational(3,10)+sp.Rational(1,2)*sp.exp(2*x)
        self.assertAlmostEqual(float(sp.diff(sp.log(Z), x).subs(x,a)), q@c, places=12)
        self.assertAlmostEqual(float(sp.diff(sp.log(Z), x,2).subs(x,a)), q@(c*c)-(q@c)**2, places=12)

    def test_coarse_preparation_and_projection_are_distinct(self):
        p = np.ones(4)/4; v = np.log([1.,3.,2.,2.])
        full, z = tilt(p,v); m = np.repeat([v[:2].mean(),v[2:].mean()],2)
        coarse, zc = tilt(p,m)
        projected = np.array([full[:2].sum(),full[2:].sum()])
        self.assertTrue(np.allclose(projected, [.5,.5]))
        self.assertGreater(np.linalg.norm(projected-[coarse[:2].sum(),coarse[2:].sum()]), .01)
        self.assertAlmostEqual(z-zc, kl(coarse,full), places=13)

    def test_nested_coarse_preparation(self):
        _,z=tilt(self.p,self.v)
        m=np.array([np.average(self.v[:2],weights=self.p[:2])]*2+[np.average(self.v[2:],weights=self.p[2:])]*2)
        _, z2=tilt(self.p,m)
        self.assertLessEqual(z-z2,z-self.p@self.v+1e-14)
        self.assertGreaterEqual(z-z2,-1e-14)

    def test_coarse_quadratic_deficit(self):
        p=np.ones(4)/4; f=np.array([-1.,1.,2.,4.]); m=np.repeat([0.,3.],2)
        target=.5*(p@(f*f)-p@(m*m))
        eps=1e-4
        _,a=tilt(p,eps*f);_,b=tilt(p,eps*m)
        self.assertAlmostEqual((a-b)/eps**2,target,delta=1e-5)

    def test_cap_exact_two_atom_optimizer(self):
        p=np.array([.5,.5]);m=np.log([1.,9.]);q=capped_density(p,m,1.5)
        self.assertTrue(np.allclose(q,[.5,1.5],atol=1e-12))
        value=np.dot(p,q*m-q*np.log(q))
        for x in np.linspace(.5,1.5,301):
            candidate=np.array([x,2-x])
            self.assertGreaterEqual(value+1e-12,np.dot(p,candidate*m-candidate*np.log(candidate)))

    def test_cap_uniqueness_and_gap(self):
        q=capped_density(self.p,self.v,1.4); star,z=tilt(self.p,self.v)
        self.assertAlmostEqual(self.p@q,1,places=12)
        val=np.dot(self.p,q*self.v-q*np.log(q))
        self.assertAlmostEqual(z-val,kl(self.p*q,star),places=12)
        self.assertLessEqual(max(q),1.4)

    def test_cap_response_tv_bound(self):
        for d in [.001,.05,.4]:
            other=self.v+np.array([d,-d,d/2,-d/3])
            q=capped_density(self.p,self.v,1.4)
            qt=capped_density(self.p,other,1.4)
            self.assertLessEqual(.5*np.dot(self.p,abs(q-qt)),d/2+1e-12)

    def test_cap_value_envelope_derivative(self):
        direction=np.array([.2,-.8,.3,.4]);h=1e-5
        def val(v):
            q=capped_density(self.p,v,1.4)
            return np.dot(self.p,q*v-q*np.log(q))
        derivative=(val(self.v+h*direction)-val(self.v-h*direction))/(2*h)
        self.assertAlmostEqual(derivative,np.dot(self.p,capped_density(self.p,self.v,1.4)*direction),places=8)

    def test_acceptance_exact(self):
        p=[F(1,4)]*4; weights=[F(1),F(3),F(2),F(2)]; cap=F(3)
        unnormalized=[x*w/cap for x,w in zip(p,weights)];success=sum(unnormalized)
        self.assertEqual(success,F(2,3))
        self.assertEqual([x/success for x in unnormalized],[F(1,8),F(3,8),F(1,4),F(1,4)])

    def test_bounded_trial_acceptance_law(self):
        p=[F(1,3),F(2,3)];acc=[F(1,2),F(1)];success=sum(x*y for x,y in zip(p,acc)); B=5
        weights=[sum((1-success)**k*p[j]*acc[j] for k in range(B)) for j in range(2)]
        total=sum(weights)
        self.assertEqual(total,1-(1-success)**B)
        self.assertEqual([x/total for x in weights],[p[j]*acc[j]/success for j in range(2)])


class InformationAndChronology(unittest.TestCase):
    def test_entropy_chain(self):
        p=np.array([.1,.2,.3,.4]); q=np.array([.25,.15,.2,.4]); visp=np.array([.3,.7]);visq=np.array([.4,.6])
        hidden=.4*kl(q[:2]/.4,p[:2]/.3)+.6*kl(q[2:]/.6,p[2:]/.7)
        self.assertAlmostEqual(kl(q,p),kl(visq,visp)+hidden,places=13)

    def test_tilt_projection_identity(self):
        p=np.array([.1,.2,.3,.4]);v=np.array([1.,-1.,.2,.7]);q,z=tilt(p,v)
        masses=np.array([p[:2].sum(),p[2:].sum()]);eff=np.log([np.dot(p[:2],np.exp(v[:2]))/masses[0],np.dot(p[2:],np.exp(v[2:]))/masses[1]])
        qy,_=tilt(masses,eff)
        self.assertTrue(np.allclose(qy,[q[:2].sum(),q[2:].sum()],atol=1e-14))

    def test_hidden_information_tangent(self):
        p=np.ones(4)/4;f=np.array([-1.,1.,2.,4.]);eps=1e-4;q,_=tilt(p,eps*f)
        loss=kl(q,p)-kl([q[:2].sum(),q[2:].sum()],[.5,.5])
        self.assertAlmostEqual(loss/eps**2,.5,delta=1e-5)

    def test_history_doob_includes_initial_reweighting(self):
        p0=[F(1,3),F(2,3)];K=[[F(3,4),F(1,4)],[F(1,5),F(4,5)]];g=[F(1),F(4)]
        h0=[sum(K[i][j]*g[j] for j in range(2)) for i in range(2)]
        Z=sum(p0[i]*h0[i] for i in range(2))
        for i,j in itertools.product(range(2),repeat=2):
            bridge=(p0[i]*h0[i]/Z)*(K[i][j]*g[j]/h0[i])
            self.assertEqual(bridge,p0[i]*K[i][j]*g[j]/Z)
        self.assertNotEqual(h0[0],h0[1])

    def test_terminal_tilts_not_projective(self):
        self.assertEqual(F(2,1)/(1+2),F(2,3))
        self.assertEqual(F(4,1)/(1+4),F(4,5))
        self.assertNotEqual(F(2,3),F(4,5))

    def test_fixed_phase_mixture_not_semigroup(self):
        I=np.eye(2);S=np.array([[0,1],[1,0]]);M=(I+S)/2
        self.assertTrue(np.allclose((I@I+S@S)/2,I))
        self.assertFalse(np.allclose(M@M,I))

    def test_conditional_entropic_tower(self):
        p=np.array([.1,.2,.3,.4]);g=np.array([-.5,.2,1.3,.7]);eta=.8
        direct=logsumexp(np.log(p)+eta*g)/eta
        h=[logsumexp(np.log(p[:2]/.3)+eta*g[:2])/eta,logsumexp(np.log(p[2:]/.7)+eta*g[2:])/eta]
        tower=logsumexp(np.log([.3,.7])+eta*np.array(h))/eta
        self.assertAlmostEqual(direct,tower,places=13)

    def test_dirac_log_transform_is_linear(self):
        for eta in [-2.,.3,2.]:
            self.assertAlmostEqual(math.log(math.exp(eta*.6))/eta,.6,places=13)

    def test_predictor_positive_update(self):
        # A static prepared bit, read twice through a specified binary instrument.
        prior=[F(2,5),F(3,5)];em=[[F(4,5),F(1,5)],[F(1,4),F(3,4)]]
        py=sum(prior[z]*em[z][1] for z in range(2))
        joint=sum(prior[z]*em[z][1]*em[z][0] for z in range(2))
        posterior=[prior[z]*em[z][1]/py for z in range(2)]
        self.assertEqual(joint/py,sum(posterior[z]*em[z][0] for z in range(2)))

    def test_nominal_prediction_not_response_sufficient(self):
        a=sp.symbols('a'); p1=sp.Rational(1,2)+a;p2=sp.Rational(1,2)+2*a
        self.assertEqual(p1.subs(a,0),p2.subs(a,0))
        self.assertNotEqual(sp.diff(p1,a),sp.diff(p2,a))
        self.assertEqual((sp.diff(p1,a)**2/(p1*(1-p1))).subs(a,0),4)
        self.assertEqual((sp.diff(p2,a)**2/(p2*(1-p2))).subs(a,0),16)

    def test_resource_dp_matches_policy_enumeration(self):
        eta=.7; outcomes=[0,1];prob=[F(1,2),F(1,2)]
        def reward(u,y): return u*(1+2*y)
        def dp(n,b):
            if n==2:return 0.
            return max(math.log(sum(float(prob[y])*math.exp(eta*(reward(u,y)+dp(n+1,b-u))) for y in outcomes))/eta for u in range(b+1))
        vals=[]
        for u0 in [0,1]:
            for acts in itertools.product(range(2-u0),repeat=2):
                v=sum(float(prob[y0]*prob[y1])*math.exp(eta*(reward(u0,y0)+reward(acts[y0],y1))) for y0,y1 in itertools.product(outcomes,repeat=2))
                vals.append(math.log(v)/eta)
        self.assertAlmostEqual(dp(0,1),max(vals),places=13)
        illegal=2*math.log(.5*(math.exp(eta)+math.exp(3*eta)))/eta
        self.assertGreater(illegal,dp(0,1))

    def test_continuous_pointer_density_normalizes(self):
        # A prepared circular position with a strictly positive smooth density.
        for shift in [0.,.17,.9]:
            integral=quad(lambda y:1+.3*math.cos(2*math.pi*(y-shift)),0,1,epsabs=1e-13)[0]
            self.assertAlmostEqual(integral,1,places=12)
        self.assertGreater(1-.3,0)


class MechanicalAndJetChecks(unittest.TestCase):
    def test_pointer_shear_symplectic(self):
        k=sp.symbols('k');S=sp.Matrix([[1,0,0,0],[0,1,0,-k],[k,0,1,0],[0,0,0,1]])
        J=sp.diag(sp.Matrix([[0,1],[-1,0]]),sp.Matrix([[0,1],[-1,0]]))
        self.assertEqual(sp.simplify(S.T*J*S),J)

    def test_pointer_work_identity(self):
        p,pi,k,m=sp.symbols('p pi k m',nonzero=True)
        self.assertEqual(sp.expand(((p-k*pi)**2-p**2)/(2*m)-(-k*p*pi/m+k**2*pi**2/(2*m))),0)

    def test_unequal_mass_reflection(self):
        M=sp.diag(2,3);Minv=M.inv();n=sp.Matrix([1,-1]);p=sp.Matrix([3,-2])
        out=p-2*(n.T*Minv*p)[0]/(n.T*Minv*n)[0]*n
        self.assertEqual((out.T*Minv*out)[0],(p.T*Minv*p)[0])
        self.assertEqual(sum(out),sum(p))
        back=out-2*(n.T*Minv*out)[0]/(n.T*Minv*n)[0]*n
        self.assertEqual(back,p)

    def test_wall_parameter_saltation(self):
        v=sp.symbols('v',positive=True);fm=sp.Matrix([v,0]);fp=sp.Matrix([-v,0]);J=sp.diag(1,-1)
        sensitivity=(J*fm-fp)/v
        self.assertEqual(sensitivity,sp.Matrix([2,0]))

    def test_implicit_collision_jets(self):
        a,h=sp.symbols('a h');R0=sp.Rational(3,5);b=sp.Rational(1,10);ell=sp.Rational(4,5)
        tau0=ell-sp.sqrt(R0**2-b**2);series=tau0
        Ft=2*(tau0-ell)
        for j in range(1,5):
            residual=sp.expand((series-ell)**2+b**2-(R0+h)**2)
            d=sp.expand(residual).coeff(h,j)
            cj=sp.simplify(-d/Ft);series+=cj*h**j
            exact=sp.diff(ell-sp.sqrt(a*a-b*b),a,j).subs(a,R0)/math.factorial(j)
            self.assertEqual(sp.simplify(cj-exact),0)

    def test_bell_chain_through_six(self):
        a=sp.symbols('a');b=a+a*a;f=sp.exp(b)
        for n in range(1,7):
            value=sum(sp.exp(b)*sp.bell(n,k,tuple(sp.diff(b,a,j) for j in range(1,n-k+2))) for k in range(1,n+1))
            self.assertEqual(sp.simplify(sp.diff(f,a,n)-value),0)

    def test_distributional_threshold_signs(self):
        a,x=sp.symbols('a x');b=a+a*a;f=x**4+2*x+1
        primitive=sp.integrate(f,(x,b,2))
        for n in range(1,5):
            current=-sum(sp.bell(n,k,tuple(sp.diff(b,a,j) for j in range(1,n-k+2)))*sp.diff(f,x,k-1).subs(x,b) for k in range(1,n+1))
            self.assertEqual(sp.simplify(sp.diff(primitive,a,n)-current),0)

    def test_quotient_jets_through_six(self):
        a=sp.symbols('a');N=sp.exp(a)+a*a;Z=2+a+a*a;U=N/Z;computed=[U]
        for n in range(1,7):
            value=(sp.diff(N,a,n)-sum(math.comb(n,j)*sp.diff(Z,a,j)*computed[n-j] for j in range(1,n+1)))/Z
            computed.append(sp.simplify(value))
            self.assertEqual(sp.simplify(value-sp.diff(U,a,n)),0)

    def test_log_jets_through_six(self):
        a=sp.symbols('a');Z=2+a+a*a;computed={}
        for n in range(1,7):
            value=(sp.diff(Z,a,n)-sum(math.comb(n-1,j)*sp.diff(Z,a,j)*computed[n-j] for j in range(1,n)))/Z
            computed[n]=sp.simplify(value)
            self.assertEqual(sp.simplify(value-sp.diff(sp.log(Z),a,n)),0)

    def test_moving_upper_limit_recursion(self):
        R,t=sp.symbols('R t');f=R**3*t**2+sp.exp(R)*t
        I=sp.integrate(f,(t,0,R))
        for n in range(1,6):
            rhs=sp.integrate(sp.diff(f,R,n),(t,0,R))+sum(sp.diff(sp.diff(f,R,k).subs(t,R),R,n-1-k) for k in range(n))
            self.assertEqual(sp.simplify(rhs-sp.diff(I,R,n)),0)


class LorentzChecks(unittest.TestCase):
    def test_geometric_margins_exact(self):
        self.assertGreater(F(9,20)**2,F(3,16))  # R_min > sqrt(3)/4
        self.assertEqual(1-2*F(47,100),F(3,50))
        self.assertLess(F(1,25),F(3,50))
        self.assertGreater(F(45,100)**2-F(1501,1000000)**2,F(44999,100000)**2)

    def test_local_threshold_derivatives(self):
        R,B=sp.symbols('R B',positive=True);chi=-sp.sqrt(R*R-B*B)
        self.assertEqual(sp.simplify(sp.diff(chi,R)+R/sp.sqrt(R*R-B*B)),0)
        self.assertEqual(sp.simplify(sp.diff(chi,R,2)-B*B/(R*R-B*B)**sp.Rational(3,2)),0)
        self.assertEqual(sp.simplify(sp.diff(chi,R,3)+3*B*B*R/(R*R-B*B)**sp.Rational(5,2)),0)

    def test_local_entrance_root_and_cutoff(self):
        T=.04
        for x,y,phi,R in itertools.product([.4991,.5,.5009],[-.0009,0,.0009],[-.0009,0,.0009],[.4595,.46,.4605]):
            ell=(1-x)*math.cos(phi)-y*math.sin(phi);b=(1-x)*math.sin(phi)+y*math.cos(phi)
            tau=ell-math.sqrt(R*R-b*b)
            q=np.array([x,y])+tau*np.array([math.cos(phi),math.sin(phi)])-np.array([1.,0.])
            self.assertAlmostEqual(np.dot(q,q),R*R,places=13)
            chi=1-T*math.cos(phi)-math.sqrt(R*R-(y+T*math.sin(phi))**2)
            if abs(tau-T)>1e-12:self.assertEqual(tau<=T,x>=chi)
            self.assertGreater(tau,.028);self.assertLess(tau,.053)

    def test_incoming_tube_jacobian(self):
        R,alpha,phi,s=sp.symbols('R alpha phi s',real=True)
        n=sp.Matrix([sp.cos(alpha),sp.sin(alpha)]);t=sp.Matrix([-sp.sin(alpha),sp.cos(alpha)])
        v=-sp.cos(phi)*n+sp.sin(phi)*t;q=R*n-s*v
        coordinates=sp.Matrix([q[0],q[1],alpha+sp.pi-phi])
        det=sp.trigsimp(coordinates.jacobian([alpha,phi,s]).det())
        self.assertEqual(sp.trigsimp(det**2-R**2*sp.cos(phi)**2),0)

    def test_global_hit_probability_from_flux(self):
        area=math.sqrt(3)/2;T=.04
        for R in [.45,.46,.47]:
            flux=R*T*(2*math.pi)*quad(math.cos,-math.pi/2,math.pi/2,epsabs=1e-13)[0]
            probability=flux/(2*math.pi*(area-math.pi*R*R))
            self.assertAlmostEqual(probability,2*R*T/(area-math.pi*R*R),places=14)
            self.assertTrue(0<probability<1)

    def test_global_response_jets_through_eight(self):
        R,A,T=sp.symbols('R A T',positive=True);den=A-sp.pi*R*R;p=2*R*T/den
        jets=[p,sp.diff(p,R)]
        for j in range(2,9):
            nxt=(2*j*sp.pi*R*jets[-1]+j*(j-1)*sp.pi*jets[-2])/den
            self.assertEqual(sp.simplify(nxt-sp.diff(p,R,j)),0)
            jets.append(sp.factor(nxt))

    def test_global_second_derivative(self):
        R,A,T=sp.symbols('R A T',positive=True);p=2*R*T/(A-sp.pi*R*R)
        formula=4*sp.pi*R*T*(3*A+sp.pi*R*R)/(A-sp.pi*R*R)**3
        self.assertEqual(sp.simplify(sp.diff(p,R,2)-formula),0)

    def test_direction_independent_hit_footprint(self):
        # Integrate incoming boundary at fixed laboratory direction: 2 R T.
        R=.46;T=.04
        for theta in [0.,.3,1.8,3.2]:
            integral=quad(lambda a:R*T*max(0.,-math.cos(theta-a)),theta+math.pi/2,theta+3*math.pi/2,epsabs=1e-13)[0]
            self.assertAlmostEqual(integral,2*R*T,places=12)

    def test_global_tube_generated_trajectories(self):
        # Finite geometric samples, explicitly not a proof of complete coverage.
        R=.46;T=.04
        for alpha,phi,s in itertools.product(np.linspace(0,2*math.pi,7,endpoint=False),[-1.5,-.7,0.,.7,1.5],[.001,.02,.039]):
            n=np.array([math.cos(alpha),math.sin(alpha)]);t=np.array([-math.sin(alpha),math.cos(alpha)])
            vm=-math.cos(phi)*n+math.sin(phi)*t;vp=math.cos(phi)*n+math.sin(phi)*t;q0=R*n-s*vm
            self.assertGreater(np.linalg.norm(q0),R)
            self.assertTrue(np.allclose(q0+s*vm,R*n,atol=1e-14))
            self.assertAlmostEqual(np.dot(vm,n),-math.cos(phi),places=14)
            self.assertTrue(np.allclose(vp,vm-2*np.dot(vm,n)*n))
            self.assertGreater(np.linalg.norm(R*n+(T-s)*vp),R)

    def test_binary_fisher_information(self):
        for p,dp in [(.2,1.3),(.5,2.),(.8,.4)]:
            score=np.array([-dp/(1-p),dp/p]); weights=np.array([1-p,p])
            self.assertAlmostEqual(weights@score,0,places=13)
            self.assertAlmostEqual(weights@(score*score),dp*dp/(p*(1-p)),places=13)

    def test_binary_quadratic_mean_remainder(self):
        area=math.sqrt(3)/2;T=.04;R=.46
        p=lambda x:2*x*T/(area-math.pi*x*x)
        pp=2*T*(area+math.pi*R*R)/(area-math.pi*R*R)**2
        root=np.sqrt([1-p(R),p(R)]);droot=np.array([-pp/(2*root[0]),pp/(2*root[1])])
        ratios=[]
        for h in [1e-4,5e-5,2.5e-5]:
            remainder=np.sqrt([1-p(R+h),p(R+h)])-root-h*droot
            ratios.append(float(remainder@remainder/h**4))
        self.assertLess(max(ratios)/min(ratios),1.05)

    def test_noisy_readout_information_bounds(self):
        sigma=.6;p=.2;dp=1.3
        def gauss(y,mu):return math.exp(-(y-mu)**2/(2*sigma*sigma))/(sigma*math.sqrt(2*math.pi))
        integral=quad(lambda y:(gauss(y,1)-gauss(y,0))**2/((1-p)*gauss(y,0)+p*gauss(y,1)),-12,13,epsabs=1e-11)[0]
        l1=quad(lambda y:abs(gauss(y,1)-gauss(y,0)),-12,13,points=[.5],epsabs=1e-11)[0]
        self.assertGreaterEqual(dp*dp*integral,dp*dp*l1*l1-1e-10)
        self.assertLessEqual(dp*dp*integral,dp*dp/(p*(1-p))+1e-10)

    def test_direction_preparation_gap(self):
        p=.2
        for xi in [-1.,-.1,.3,2.]:
            gap=math.log(1-p+p*math.exp(xi))-xi*p
            self.assertGreater(gap,0)
        eps=1e-4;gap=math.log(1-p+p*math.exp(eps))-eps*p
        self.assertAlmostEqual(gap/eps**2,p*(1-p)/2,delta=1e-5)

    def test_conjugate_calibration(self):
        p=.23;c=.7;xi=math.log(c/(1-c))-math.log(p/(1-p))
        selected=expit(math.log(p/(1-p))+xi)
        self.assertAlmostEqual(selected,c,places=14)
        for delta in [-.5,-.1,.03,.3]:
            other=expit(math.log(p/(1-p))+xi+delta)
            self.assertLessEqual(abs(other-selected),abs(delta)/4+1e-14)


class ApproximationChecks(unittest.TestCase):
    def test_positive_normalization_bound(self):
        a=np.array([.1,.2,.6]);b=np.array([.2,.1,.8]);lhs=np.sum(abs(a/a.sum()-b/b.sum()));rhs=2*np.sum(abs(a-b))/a.sum()
        self.assertLessEqual(lhs,rhs)

    def test_conditioning_budget(self):
        p=np.array([.1,.2,.3,.4]);q=np.array([.12,.18,.29,.41]);eps=.5*np.sum(abs(p-q));A=[0,1]
        lhs=.5*np.sum(abs(p[A]/sum(p[A])-q[A]/sum(q[A])))
        self.assertLessEqual(lhs,2*eps/min(sum(p[A]),sum(q[A])))

    def test_testwise_ratio_bound(self):
        alpha=np.array([.3,.7]);beta=np.array([.25,.65]);f=np.array([-1.,2.]);B=2;zstar=.9
        lhs=abs(alpha@f/alpha.sum()-beta@f/beta.sum())
        rhs=(abs((alpha-beta)@f)+B*abs(alpha.sum()-beta.sum()))/zstar
        self.assertLessEqual(lhs,rhs+1e-14)

    def test_dirac_tv_and_smooth_tests(self):
        h=.001
        self.assertEqual(sum(abs(x-y) for x,y in zip([F(1),F(0)],[F(0),F(1)]))/2, F(1))
        self.assertLessEqual(abs(math.sin(h)-math.sin(0)),h)

    def test_bilateral_rates(self):
        A,B,C,D=2.,3.,.4,.5;lam=(B+D)/(A+B+C+D);rho=math.exp((C*D-A*B)/(A+B+C+D))
        self.assertLess(rho,1)
        self.assertAlmostEqual(-A*lam+D*(1-lam),math.log(rho),places=14)
        self.assertAlmostEqual(C*lam-B*(1-lam),math.log(rho),places=14)
        for m,n in itertools.product(range(5),repeat=2):
            self.assertLessEqual(min(math.exp(-A*m+C*n),math.exp(D*m-B*n)),rho**(m+n)+1e-13)


if __name__ == '__main__':
    unittest.main(verbosity=2)
