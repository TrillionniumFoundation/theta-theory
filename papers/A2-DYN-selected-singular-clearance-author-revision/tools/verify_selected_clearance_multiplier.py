#!/usr/bin/env python3
"""Auxiliary exact algebra/index checks. Not a physical-dynamics proof."""
import json, math, argparse
from fractions import Fraction as Q
from pathlib import Path
import sympy as s
b,A,B,t=s.symbols('b A B t', positive=True)
f=A*b*b+4*B/(t*t*b)
bstar=(2*B/A)**s.Rational(1,3)*t**s.Rational(-2,3)
assert s.simplify(s.diff(f,b).subs(b,bstar))==0
assert s.simplify(f.subs(b,bstar)-3*2**s.Rational(2,3)*A**s.Rational(1,3)*B**s.Rational(2,3)*t**s.Rational(-4,3))==0
C,alpha,beta=s.symbols('C alpha beta',positive=True)
k=3*2**s.Rational(2,3)*(C*alpha/4)**s.Rational(1,3)*(C*beta/s.pi)**s.Rational(2,3)
assert s.simplify(k-3*C*s.pi**(-s.Rational(2,3))*alpha**s.Rational(1,3)*beta**s.Rational(2,3))==0
q=Q(47,53); theta_max=Q(53,59)
assert theta_max**4<q
assert 2*q/(1-q)==Q(47,3)
indices=0
for m in range(1,101):
 for j in range(m):
  d=min(j,m-1-j)
  for i in range(1,m):
   if j<i: length=i; local=j
   else: length=m-i;local=j-i
   assert length>=1 and 0<=local<length
   exp=max(local,length-1-local)
   assert exp>=d
   indices+=1
# Quarter powers retained as exact monomials. Coefficients in the linear regime.
d=s.symbols('d',positive=True)
assert s.simplify((d*(2*d))**s.Rational(1,2)-s.sqrt(2)*d)==0
assert s.simplify(d**s.Rational(1,4)*(2*d)**s.Rational(1,4)*(2*d)**s.Rational(1,2)-2**s.Rational(3,4)*d)==0
# Exact geometric series and positive conditioning powers.
c,p=s.symbols('c p',positive=True)
for exponent in [s.Rational(1,2),s.Rational(1,4)]:
 assert s.simplify((c*p)**exponent/c-c**(exponent-1)*p**exponent)==0
out={'status':'passed','actual_block_index_cases':indices,'collision_counts_checked':'1..100','exact_checks':['tail cutoff optimizer and constant','two selected-block factors','theta_max^4 < q0','incidence depth-weight sum 47/3','linear-regime exponents','single-conditioning powers'],'scope':'Finite symbolic arithmetic and index regression only. Full continuous source and limit statements require the written proof and inherited dynamical theorems.'}
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
if args.output: args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
