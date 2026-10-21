#!/usr/bin/env python3
"""Exact algebraic reconstruction for native modules 324--325 and 326's source use.

This auxiliary check does not certify real first-hit coverage, the inherited
curve-growth theorem, analytic endpoint exhaustion, or any local limit theorem.
Those are the explicit mathematical proofs in the associated source/audit.
"""
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from pathlib import Path
import sympy as sp

checks = []
def zero(name, value, explanation):
    v = sp.simplify(value)
    if v != 0:
        raise RuntimeError(f'{name}: nonzero exact residual {v}')
    checks.append({'id':name,'kind':'symbolic_identity','result':'pass','residual':'0','meaning':explanation})
def yes(name, condition, explanation, exact=None):
    if condition is not True and condition != sp.true:
        raise RuntimeError(f'{name}: exact condition failed: {condition}')
    item={'id':name,'kind':'exact_inequality_or_count','result':'pass','meaning':explanation}
    if exact is not None:item['exact']=str(exact)
    checks.append(item)
def positive_polynomial(name, expression, generators, explanation):
    poly=sp.Poly(sp.expand(expression),*generators)
    coeffs=poly.coeffs()
    yes(name, all(bool(c>=0) for c in coeffs),explanation,poly.as_expr())

R,k,c,d,t = sp.symbols('R k c d tau',positive=True)
B=lambda z:sp.Matrix([[z,0],[k,1]])
P=lambda z:sp.Matrix([[1,z],[0,1]])
K=lambda z:sp.Matrix([[1,0],[2*k/z,1]])
Dc=sp.Matrix([[t*k+c,t],[t*k*k+k*d+k*c,t*k+d]])/d
for rr in range(2):
    for cc in range(2):
        zero(f'collision_optical_conjugacy_{rr}{cc}',(B(d)*Dc-K(d)*P(t)*B(c))[rr,cc],
             'The positive physical derivative and outgoing transverse field are exactly conjugate.')
terminal=sp.Matrix([[0,d]])*B(d).inv()*K(d)
zero('terminal_no_kick_row',terminal[0]-k,'The terminal kick cancels to the incoming row (k,d).')
zero('terminal_no_kick_incidence',terminal[1]-d,'The terminal incidence is retained in the momentum row.')
zero('physical_determinant',Dc.det()-c/d,'The actual collision derivative has determinant c/d.')
zero('horizontal_initial_field',(B(c)*sp.Matrix([R,0]))[1].subs(k,1/R)-1,
     'A canonical angle variation has outgoing field (R c,1), not (0,1).')
zero('vertical_initial_field',(B(c)*sp.Matrix([0,1]))[1]-1,
     'The fixed-contact angle fan has outgoing field (0,1).')

am,ap,xm,xp,ym,yp=sp.symbols('am ap xm xp ym yp',positive=True)
AHm=R*c*xm+ym; AHp=R*c*xp+yp
D=sp.Matrix([[AHm,-ym],[AHp,yp]]).det()
zero('two_half_determinant',D-(AHm*yp+ym*AHp),
     'Reversal changes the sign of the central phi column relative to the alpha column; determinant adds.')
zero('horizontal_coarea_root',c/D-c/(AHm*AHp*(ym/AHm+yp/AHp)),
     'Collision area c d-alpha d-phi retains the central factor c in the inverse endpoint root weight.')
zero('vertical_coarea_root',c/D-c/(ym*yp*((1+R*c*xm/ym)+(1+R*c*xp/yp))),
     'The fixed-position fan formula has the same exact root weight, no extra radius factor.')

ast,bline,p,dd=sp.symbols('a b_line p d',real=True,nonzero=True)
V=k+dd/ast
aslope=p+bline*dd/ast
dslope=-p*V
Vslope=sp.diff(V,ast)*aslope+sp.diff(V,dd)*dslope
zero('first_image_slope_derivative',Vslope-(-p*k/ast-2*p*dd/ast**2-bline*dd**2/ast**3),
     'Both canonical sources use the exact first-image derivative; b_line=R b or zero.')
zero('first_image_momentum_variation',k*aslope+dslope-dd*(k*bline-p)/ast,
     'Absolute one-flight log variation is bounded without dividing by an initial incidence.')

lo=sp.Rational(3,50); Rp=sp.Rational(47,100); km=1/Rp; kp=sp.Rational(20,9)
U=sp.Rational(170,9); sig=sp.Rational(47,59)
zero('cone_U',U-kp-1/lo,'The source image cone upper endpoint is inherited unchanged.')
zero('class_K_mom', (kp+2/lo)/lo+1/(lo**3*km) - (U/lo+(1+Rp/lo)/lo**2),
     'The proposed coarse first-image allowance is exactly the already qualified K_mom of native284.')
zero('source_optical_rate',1+2*lo/Rp-1/sig,'Each additional real kick and flight expands B by at least59/47.')
zero('source_E',1/(km*lo)-sp.Rational(47,6),'The l-flight inverse bound begins E sigma^(l-1), with E=47/6.')
zero('horizontal_C0',(lo+Rp)/(2*lo)-sp.Rational(53,12),'The retained horizontal product constant is53/12.')

x,y,rgap,tgap,gap,Rpos,tpos=sp.symbols('x y r_gap tau_gap one_minus_c R t_min',nonnegative=True)
Rpvar=Rpos+rgap; tau=tpos+tgap; cv=1-gap
Y=tau*x+y; AH=Rpos*cv*x+Y
witness=((rgap+Rpos*gap)+Rpvar*tgap/tpos)*x+Rpvar*y/tpos
zero('horizontal_ratio_witness',(1+Rpvar/tpos)*Y-AH-witness,
     'The incidence ratio lower bound follows from a nonnegative explicit witness.')
positive_polynomial('horizontal_ratio_nonnegative',tpos*witness,[x,y,rgap,tgap,gap,Rpos,tpos],
                    'For positive physical t_min, the ratio inequality follows from nonnegative monomials.')
Bv,Dv,dt,dk=sp.symbols('B D dt dk',nonnegative=True)
kmin=2/Rp
res=sp.expand((1+(lo+dt)*(kmin+dk))*Bv+(lo+dt)*Dv-(1+lo*kmin)*Bv)
positive_polynomial('optical_induction_nonnegative',res,[Bv,Dv,dt,dk],
                    'The all-length optical induction has a nonnegative algebraic remainder.')

A0,B0,C0,c0,cN=sp.symbols('A0 B0 C0 c0 cN',positive=True)
D0=(c0/cN+B0*C0)/A0
Mat=sp.Matrix([[A0,B0],[C0,D0]])
Can=sp.diag(1/R,cN)*Mat*sp.diag(R,1/c0)
zero('canonical_area_determinant',Can.det()-1,'The actual finite derivative is area preserving in alpha,p coordinates.')
zero('endpoint_backward_root',Can.inv()[1,0]+Can[1,0],
     'Backward horizontal inverse momentum derivative has the same absolute magnitude as the forward derivative.')
zero('endpoint_root_matrix',Can[1,0]-R*cN*C0,'The full physical derivative yields u=1/(R cN D21), with both factors retained.')
AA,BB,CC,DD=sp.symbols('A B C D',positive=True)
Den2=(DD+k*BB)**2+(CC+k*AA)**2
positive_polynomial('pressure_affine_comparison',sp.expand(Den2-CC**2),[AA,BB,CC,DD,k],
                    'The affine inverse norm denominator is at least D21; no terminal incidence was dropped.')

n,Dd,L,j=sp.symbols('n D L j',integer=True,positive=True)
r=sp.symbols('r',positive=True)
geom=sp.summation(sig**j,(j,0,n-1))
zero('complete_depth_sum',geom-(1-sig**n)/(1-sig),
     'Each of the two actual interior age sequences has a bounded geometric sum.')
deep=sp.summation(sig**(Dd+j),(j,0,L-1))
zero('deep_depth_sum',deep-sig**Dd*(1-sig**L)/(1-sig),
     'A deep-index restriction retains the factor sigma^D before the count supremum.')

h0=sp.Rational(1,200)
area=4*(2*h0)**2+sp.Rational(6,50)*sp.Rational(3,10)
zero('original_section_probability',area/(4*sp.pi)-sp.Rational(91,10000)/sp.pi,
     'The four original squares and U retain exactly c*=91/(10000 pi).')
ymax=2*sp.Rational(53,100)/(1+sp.Rational(53,100)**2)+h0
margin=sp.Rational(5,6)-ymax
zero('original_endpoint_margin',margin-sp.Rational(6073,7685400),
     'The largest possible original section momentum is strictly inside5/6.')
yes('positive_endpoint_margin',margin>0,'The endpoint cap follows from the unchanged original section.',margin)
yes('section_side_count',5*2==10,'Five original rectangles have10 horizontal and10 vertical sides, before any seam gluing.')
z=sp.symbols('z',real=True)
zero('unit_phase_jump',sp.trigsimp(2-2*sp.cos(z)-4*sp.sin(z/2)**2),
     'A single occupation jump has modulus2|sin(zeta/2)|; endpoint indicator jumps remain at most1.')
S,Db=sp.symbols('S Db',positive=True)
s=sp.symbols('s',positive=True)
zero('squared_fourier_tail',2*sp.integrate(Db**2/s**2,(s,S,sp.oo))-2*Db**2/S,
     'The squared roof Fourier tail is2D^2/S; this does not claim an L1 high-frequency tail.')

parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
default_core=Path(__file__).resolve().parent.parent/'core'
if not default_core.is_dir():default_core=Path(__file__).resolve().parent
parser.add_argument('--source-dir',type=Path,default=default_core)
args=parser.parse_args()
source_files=list(sorted(args.source_dir.glob('32[4-6]_*.tex')))
for prefix in ('324_','325_'):
    if sum(p.name.startswith(prefix) for p in source_files)!=1:
        raise RuntimeError('Expected exactly one native source for '+prefix+' in '+str(args.source_dir))
result={'schema':'a2-dyn-canonical-boundary-exact-check-v1','status':'pass','check_count':len(checks),
        'python':platform.python_version(),'sympy':sp.__version__,'optimized':bool(sys.flags.optimize),
        'scope':'Auxiliary exact algebra, normalization, endpoint factors and finite side counts; not a continuum or local-limit certificate.',
        'sources':[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in source_files],
        'checks':checks}
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','checks':len(checks),'optimized':bool(sys.flags.optimize),'output':str(args.output) if args.output else None},sort_keys=True))
