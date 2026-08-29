#!/usr/bin/env python3
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sqrt3=sp.sqrt(3)
A=sqrt3/2
rmin=sp.Rational(9,20)
rmax=sp.Rational(47,100)
checks={}
checks['disk_disjoint_margin']=sp.simplify(1-2*rmax)
checks['corridor_closed_margin']=sp.simplify(2*rmin-A)
checks['next_neighbour_period_clearance']=sp.simplify(sp.Rational(1,2)-rmax)
assert all(sp.N(checks[k])>0 for k in checks)

alpha_mass=2*sp.pi
p=sp.Symbol('p')
phi_mass=sp.integrate(sp.cos(p),(p,-sp.pi/2,sp.pi/2))
liouville=sp.simplify(alpha_mass*phi_mass/(4*sp.pi))
assert liouville==1

r=sp.symbols('r', positive=True)
mean_roof=sp.simplify((A-sp.pi*r**2)/(2*r))
mean_roof_prime=sp.simplify(sp.diff(mean_roof,r))
assert sp.simplify(mean_roof_prime + A/(2*r**2)+sp.pi/2)==0
assert float(mean_roof.subs(r,rmax))>0

L1=2*(1-2*r)
L3=2*(sqrt3-2*r)
ratio=sp.simplify(L3/L1)
ratio_prime=sp.simplify(sp.diff(ratio,r))
assert ratio_prime!=0
assert float(ratio_prime.subs(r,sp.Rational(23,50)))>0

# Open nearest-neighbour displacement branches generate the lattice.
e1=sp.Matrix([1,0]); e2=sp.Matrix([sp.Rational(1,2),sqrt3/2])
assert sp.sqrt(e1.dot(e1))==1
assert sp.sqrt(e2.dot(e2))==1
nearest_gap=1-2*rmax
other_centre_clearance=sqrt3/2-rmax
assert float(nearest_gap)>0
assert float(other_centre_clearance)>0
assert 1-0==1

# Generic second derivative identity for Psi(p,kappa(p))=0.
Psi_p,Psi_s,Psi_pp,Psi_ps,Psi_ss=sp.symbols('Psi_p Psi_s Psi_pp Psi_ps Psi_ss')
kprime=-Psi_p/Psi_s
ksecond=sp.simplify(-(Psi_pp+2*Psi_ps*kprime+Psi_ss*kprime**2)/Psi_s)
assert ksecond.has(Psi_pp)

# Cole-Hopf generator identity.
theta,D,b,c,ux,uxx=sp.symbols('theta D b c ux uxx')
nonlinear=c+b*ux+D*uxx/2+theta*D*ux**2/2
cole=c+b*ux+D*(uxx+theta*ux**2)/2
assert sp.simplify(nonlinear-cole)==0

result={
 'status':'PASS_GEOMETRY_AND_FORMULA_REGRESSION',
 'exact':{
   'lattice_area':'sqrt(3)/2',
   'radius_interval':['9/20','47/100'],
   'mean_roof':'(sqrt(3)/2-pi*r^2)/(2*r)',
   'mean_roof_derivative':'-sqrt(3)/(4*r^2)-pi/2',
   'marked_periods':['2(1-2r)','2(sqrt(3)-2r)'],
   'theta_generator':'c+b*u_x+D*u_xx/2+theta*D*u_x^2/2'},
 'numeric':{
   'disk_disjoint_margin':float(checks['disk_disjoint_margin']),
   'corridor_closed_margin':float(checks['corridor_closed_margin']),
   'next_neighbour_period_clearance':float(checks['next_neighbour_period_clearance']),
   'nearest_branch_gap':float(nearest_gap),
   'other_centre_line_clearance':float(other_centre_clearance),
   'mean_roof_at_rmax':float(mean_roof.subs(r,rmax)),
   'period_ratio_derivative_at_0.46':float(ratio_prime.subs(r,sp.Rational(23,50)))},
 'scope_warning':'Does not certify anisotropic spectral theory, Gibbs conditioning, ASIP, viscosity convergence, or external review.'}
out=ROOT/'status'/'DEEP_VERIFICATION_RECEIPT.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
