#!/usr/bin/env python3
"""Auxiliary exact/symbolic checks for native337; not a billiard/LLT proof."""
from pathlib import Path
from fractions import Fraction as F
import argparse, json, math
import mpmath as mp
import sympy as sp
p=argparse.ArgumentParser()
p.add_argument("--output",type=Path,required=True)
args=p.parse_args()
mp.mp.dps=50
rows=[]
def record(name,passed,details):
    rows.append({"name":name,"passed":bool(passed),"details":details})
    if not passed:raise AssertionError(name)
def close(a,b,tol=mp.mpf("1e-35")):return abs(a-b)<=tol*(1+abs(b))
def sinc(x):return mp.sin(x)/x if x else mp.mpf(1)
def mpc(x):
    if isinstance(x,tuple):return mp.mpc(str(x[0]),str(x[1]))
    return mp.mpc(str(x))
# A component is a finite sum of exact interval indicators, hence actual
# compactly supported BV test functions with no arbitrary derivative atoms.
intervals=[
 [(F(0),F(1),mp.mpc(1)),(F(1),F(2),mp.mpc(2)),(F(0),F(1),mp.mpc(-1))],
 [(F(1,3),F(5,3),mp.mpc(0,1)),(F(5,3),F(7,3),mp.mpc(1,-1))],
 [(F(-1),F(1,2),mp.mpc(F(1,2).numerator/F(1,2).denominator))]
]
labels=[(0,0,1),(1,-1,2),(-1,1,1)]
def atoms_of(component):
    out={}
    for l,r,c in component:
        out[l]=out.get(l,0)+c;out[r]=out.get(r,0)-c
    return {u:c for u,c in out.items() if c}
atoms=[atoms_of(x) for x in intervals]
def atom_transform(j,s):
    return sum(c*mp.exp(1j*s*mp.mpf(u.numerator)/u.denominator) for u,c in atoms[j].items())
def roof_transform(j,s):
    if not s:return sum(c*mp.mpf((r-l).numerator)/(r-l).denominator for l,r,c in intervals[j])
    return sum(c*(mp.exp(1j*s*mp.mpf(r.numerator)/r.denominator)-mp.exp(1j*s*mp.mpf(l.numerator)/l.denominator))/(1j*s) for l,r,c in intervals[j])
for s in [mp.mpf("0.125"),mp.mpf("1"),mp.mpf("-2.25"),mp.mpf("11")]:
    for j in range(len(labels)):
        record("positive-exponent Fourier derivative sign",close(-1j*s*roof_transform(j,s),atom_transform(j,s)),{"component":j,"s":str(s)})
# Coincident sources must combine before squaring, even at identical labels.
record("coincident opposite sources cancel before square",atoms[0]=={F(1):mp.mpc(2),F(2):mp.mpc(-2)},{"combined":{str(k):str(v) for k,v in atoms[0].items()}})
naive=sum(abs(c)**2*2 for l,r,c in intervals[0])
actual=sum(abs(c)**2 for c in atoms[0].values())
record("negative control: separate-source energy is rejected",naive!=actual,{"incorrect":str(naive),"correct":str(actual)})
energy=sum(abs(c)**2 for a in atoms for c in a.values())
for S in [mp.mpf(1),mp.mpf(4),mp.mpf(13)]:
    finite=sum(sum(c*mp.conj(d)*sinc(S*mp.mpf((u-v).numerator)/(u-v).denominator) for u,c in a.items() for v,d in a.items()) for a in atoms)
    numeric=mp.quad(lambda s:sum(abs(atom_transform(j,s))**2 for j in range(len(atoms))),[-S,0,S])/(2*S)
    cross=sum(sum(abs(c*d)*min(1,1/(S*abs(mp.mpf((u-v).numerator)/(u-v).denominator))) for u,c in a.items() for v,d in a.items() if u!=v) for a in atoms)
    record("finite-S sinc identity by independent quadrature",close(numeric,finite,mp.mpf("1e-30")),{"S":str(S),"error":str(abs(numeric-finite))})
    record("finite-S cross bound",abs(finite-energy)<=cross+mp.mpf("1e-35"),{"S":str(S),"left":str(abs(finite-energy)),"bound":str(cross)})
# Orthogonality of the full three-torus: 7 roots suffice for these degree gaps.
s=mp.mpf("2.3");N=7
vals=[atom_transform(j,s) for j in range(len(labels))]
torus=mp.mpf(0)
for i in range(N):
 for j in range(N):
  for k in range(N):
   torus+=abs(sum(v*mp.exp(2j*mp.pi*(i*l[0]+j*l[1]+k*l[2])/N) for l,v in zip(labels,vals)))**2
torus/=N**3
direct=sum(abs(v)**2 for v in vals)
record("full discrete-torus Parseval without label factor",close(torus,direct,mp.mpf("1e-35")),{"torus":str(torus),"components":str(direct),"labels":len(labels)})
# Triangular density has an absolutely continuous derivative and zero atoms.
def tri_g(s):
    if not s:return mp.mpf(0)
    return ((mp.exp(1j*s)-1)-(mp.exp(2j*s)-mp.exp(1j*s)))/(1j*s)
def tri_f_integral(s):
    return mp.quad(lambda t:t*mp.exp(1j*s*t),[0,1])+mp.quad(lambda t:(2-t)*mp.exp(1j*s*t),[1,2])
for s in [mp.mpf(".4"),mp.mpf("3"),mp.mpf("-6")]:
 record("AC derivative sign with independent physical-variable integral",close(-1j*s*tri_f_integral(s),tri_g(s),mp.mpf("1e-32")),{"s":str(s)})
# Mixed derivative: first two interval components plus an independent triangle.
D=sum(sum(abs(c) for c in a.values()) for a in atoms)+2
for S in [mp.mpf(2),mp.mpf(7)]:
 Q=mp.quad(lambda s:abs(tri_g(s))**2,[-S,0,S])/(2*S)
 W=mp.quad(lambda s:sum(abs(atom_transform(j,s)+(tri_g(s) if j==0 else 0))**2 for j in range(len(atoms))),[-S,0,S])/(2*S)
 C=sum(sum(abs(c*d)*min(1,1/(S*abs(mp.mpf((u-v).numerator)/(u-v).denominator))) for u,c in a.items() for v,d in a.items() if u!=v) for a in atoms)
 bound=C+2*D*mp.sqrt(Q)+Q
 record("mixed AC-atomic finite-band inequality",abs(W-energy)<=bound,{"S":str(S),"error":str(abs(W-energy)),"bound":str(bound),"Q":str(Q)})
# The exact coalescence countercheck prohibits swapping sup_R/limit_S.
delta=mp.mpf("1e-8");S=mp.mpf(10)
small=2-2*sinc(S*delta)
record("coalescence has energy 2 but tiny finite-S energy",0<small<mp.mpf("1e-12"),{"finite":str(small),"true_fixed_delta_limit":"2"})
# Complex-vector norm identity and inherited critical coefficient.
ar,ai,br,bi=sp.symbols("ar ai br bi",real=True)
lhs=(ar**2+ai**2)-((ar-br)**2+(ai-bi)**2)
record("exact complex energy subtraction identity",sp.expand(lhs-(2*(ar*br+ai*bi)-br**2-bi**2))==0,{"symbolic":str(sp.expand(lhs))})
sigma=F(47,59)
# Finite controls include both endpoints, the center, and both parities.
# The inequality for every m is proved in the manuscript.
for m,j in [(1,0),(2,0),(2,1),(7,0),(7,3),(7,6),(8,3),(8,4),(30,0),(30,29)]:
 record("longer-side fan exponent after squaring",sigma**(2*max(j,m-1-j))<=sigma**(m-1),{"m":m,"j":j})
# Raw necessary scaling is m^2 times jump energy, not m^4.
for m in [1,2,7,31]:
 eps=F(3,7); aa=[F(1,5),F(1,7),F(1,9)]
 cap=2*eps/F(m*m)
 a=[min(x,cap) for x in aa];D0=sum(abs(x) for x in a)
 record("raw max-jump to all-label energy normalization",m*m*sum(x*x for x in a)<=2*eps*D0,{"m":m,"epsilon":str(eps)})
# This scope example is not included in the executed-check count.
scope_annotation={"family":"m^-2 phi((t-m*tau0)/exp(-m)), phi smooth compactly supported with maximum1","jumps":0,"normalized_height":1,"meaning":"Analytical necessity-versus-sufficiency example, not a billiard counterexample or executed continuum verification."}
result={"status":"PASS","checks":len(rows),"precision_decimal_digits":mp.mp.dps,"all_passed":all(r["passed"] for r in rows),"scope":"Exact rational and symbolic identities; independent finite quadratures and negative controls. No continuum billiard hypothesis, LLT, or exchanged limit is certified.","results":rows,"scope_annotation":scope_annotation}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":result["status"],"checks":len(rows),"output":str(args.output)}))

