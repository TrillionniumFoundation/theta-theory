#!/usr/bin/env python3
"""Exact auxiliary checks of the independently reconstructed boundary proof.

This program verifies finite algebra and constant bookkeeping.  Its output is
not a proof of any continuous geometric, source, spectral, or limit theorem.
The independent continuous proof reconstruction is in the accompanying report.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import sympy as sp

parser=argparse.ArgumentParser()
parser.add_argument('--details', required=True)
args=parser.parse_args()
checks=[]
def require(condition, name, details):
    if not condition:
        raise RuntimeError(name)
    checks.append({'name':name, 'passed':True, 'details':details})

Rminus=Q(9,20); Rplus=Q(47,100); tau=Q(3,50)
lam=Q(50,47); gam=1/lam; aval=Q(47,6)
K=2*(1+lam)*(4*aval+16*aval**2)
r=min(1/(8*(1+aval)),1/(8*K))
eta=r/(8*(1+lam*aval)); P=2*(1+lam*aval)
glow=Rminus/2; Lam=Q(47,6)
KF=2048*Rplus/eta**2
a=min(eta/16,glow/(2*KF)); b=glow*a/4
Lz=Q(28,5)+Rplus+Q(3,200)
LB=P*(4*Rplus+12*(Rplus/tau)*Lz)
KB1=6*LB; KB2=128*LB/eta
KBg=KB2/glow**2+KB1*KF/glow**3
require(P*eta/2 == r/8 and r<Q(1,8) and Lz==Q(1217,200),
        'inherited_domain_and_contact_localization',
        {'P_eta_over_2_equals_r_over_8':True, 'Lz':str(Lz),
         'eta':str(eta), 'r_star':str(r)})
require(Q(5,3)**2 == Q(25,9) and 1/(1-r)<2 and Q(136,27)<6,
        'complex_vector_norm_and_direction_derivative',
        {'norm_square_bound':'25/9', 'normal_upper':'1/(1-r_star) < 2',
         'direction_derivative_ratio':'136/27 < 6'})
require(2*4*8**2 == 512 and 4*512==2048 and 8<16 and 32<36
        and 2*Q(1,2)*8**2==64 and 2*64==128,
        'cauchy_factorials_and_Euclidean_conversion',
        {'gradient_second_partial_factor':512,
         'gradient_Hessian_derivative_factor':2048,
         'B_gradient_conversion':'4 sqrt(2) < 6',
         'B_Hessian_operator_factor':128})
require(KF*a<=glow/2 and a<=eta/16 and a/4<eta/8
        and Lam+glow/2<2*Lam and b/glow==a/4,
        'common_real_inverse_radius',
        {'a':str(a), 'b':str(b),
         'Hessian_increment':'<= g_under/2',
         'inverse_range':'|q(g)-q_star| < a/4'})

x,y=sp.symbols('x y', real=True)
psi=(x*x+y*y)/2+x**3/6+x*y*y/3+y**4/20
qv=sp.Matrix([sp.diff(psi,x),sp.diff(psi,y)])
u,v=sp.symbols('u v', real=True)
Bout=2*u-3*v+u*u/7+u*v/11+v*v/13
outer_grad=sp.Matrix([sp.diff(Bout,z) for z in (u,v)])
subs={u:qv[0],v:qv[1]}
Jq=qv.jacobian((x,y))
chain_one=Jq.T*sp.hessian(Bout,(u,v)).subs(subs)*Jq
chain_two=sum((outer_grad[i].subs(subs)*sp.hessian(qv[i],(x,y))
               for i in range(2)),sp.zeros(2))
direct=sp.hessian(Bout.subs(subs),(x,y))
require(all(sp.simplify(z)==0 for z in direct-chain_one-chain_two)
        and any(sp.simplify(z)!=0 for z in chain_two),
        'second_composition_term_is_necessary',
        {'exact_symbolic_chain_rule':True,
         'second_term_nonzero_in_gradient_inverse_example':True,
         'bound':'KB2/g_under^2 + KB1*KF/g_under^3'})

s=sp.symbols('s', real=True)
for degree in range(13):
    fs=s**degree
    lhs=sp.diff(fs,s).subs(s,1)
    rhs=fs.subs(s,1)-fs.subs(s,0)+sp.integrate(s*sp.diff(fs,s,2),(s,0,1))
    if sp.simplify(lhs-rhs)!=0:
        raise RuntimeError('Euler monomial identity failed')
require(True,'exact_Euler_remainder_and_nonzero_offset',
        {'degrees_verified':list(range(13)),
         'boundary_zero_offset':'D B(g).g = integral_0^1 s D2B(sg)[g,g] ds',
         'nonzero_offset_retained':'-B(0) + integral_0^1 s D2B(sg)[g,g] ds',
         'integral_s':'1/2',
         'speed_bound':'Lambda_circ * KBg * gamma^depth'})

Am,Ap,Bm,Bp,p0,pm,s0,sm,sig,RR=sp.symbols('Am Ap Bm Bp p0 pm s0 sm sig RR', nonzero=True)
M=sp.Matrix([[s0*Am,sig*s0*Bm],[sm*Ap,-sig*sm*Bp]])
require(sp.expand(M.det()+sig*s0*sm*(Am*Bp+Bm*Ap))==0,
        'two_half_ray_signed_determinant',
        {'determinant':'-sigma*s0*sm*(Am*Bp + Bm*Ap)',
         'absolute_determinant':'Am*Ap*(hm+hp)',
         'no_terminal_kick':True})
wr=(p0*sm*Ap-pm*s0*Am)/(Am*Ap)
require(sp.simplify(wr-(sm*p0/Am-s0*pm/Ap))==0,
        'Wronskian_row_cancellation',
        {'numerator':'sm*p0/Am - s0*pm/Ap',
         'root_density':'1/[R Am Ap (hm+hp)]',
         'angle_denominator':'(p0^2+pm^2)'})

opt_cases=0
for n in range(1,6):
  for ci in (Q(1),Q(1,2),Q(1,1000000)):
    for af in (Q(1,4),Q(1,2),Q(1)):
      for cend in (Q(1),Q(1,3),Q(1,1000000)):
        RRq=Rminus
        mat=sp.Matrix([[1,sp.Rational(af.numerator,af.denominator)],[0,1]])
        for i in range(1,n):
          ell=tau+Q(i,10)
          kk=2/(RRq*ci)
          PP=sp.Matrix([[1,sp.Rational(ell.numerator,ell.denominator)],[0,1]])
          KK=sp.Matrix([[1,0],[sp.Rational(kk.numerator,kk.denominator),1]])
          mat=PP*KK*mat
        kap=1/RRq
        kapS=sp.Rational(kap.numerator,kap.denominator)
        cS=sp.Rational(cend.numerator,cend.denominator)
        Apv=kapS*mat[0,1]+cS*mat[1,1]
        Bpv=kapS*mat[0,0]+cS*mat[1,0]
        hv=Q(Bpv/Apv)
        if mat.det()!=1 or Apv<=0 or Bpv<=0 or not (1/(af+Rplus)<=hv<=1/af):
          raise RuntimeError('positive half-product ratio failed')
        opt_cases+=1
require(True,'positive_half_product_finite_checks',
        {'cases':opt_cases,
         'scope':'Exact algebra on positive optical products only; physical reflection proof is in manuscript.',
         'ratio':'1/(a_foot+R_plus) <= h <= 1/a_foot',
         'arbitrarily_small_sampled_incidence':'1/1000000'})

checked=0
for m in range(1,101):
  for D in range((m+1)//2+2):
    actual=sum((gam**min(j,m-1-j) for j in range(m)
                if min(j,m-1-j)>=D),Q(0))
    if actual>2*gam**D/(1-gam):
      raise RuntimeError('depth tail bound failed')
    checked+=1
require(True,'flight_depth_and_geometric_sum',
        {'finite_count_depth_pairs':checked, 'gamma':str(gam),
         'proved_tail':'2 gamma^D/(1-gamma)',
         'asymptotic_proof':'m^2 gamma^(theta*m) tends to zero for each fixed theta>0; analytic proof, not this finite enumeration.'})

payload={'status':'PASS','check_groups':len(checks),
         'checks':checks,
         'limitations':['Finite algebra does not prove the continuous billiard source statements.',
                        'No claim of whole Q pressure, complete critical boundary, raw pointwise LLT, or four-coordinate inversion completion.']}
Path(args.details).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','groups':len(checks),'optical_cases':opt_cases,
                  'depth_pairs':checked},sort_keys=True))
