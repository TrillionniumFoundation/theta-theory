#!/usr/bin/env python3
"""Independent finite algebra checks for the v56 referee report.
Requires SymPy. Does not import manuscript checking code or certify limits.
"""
import json, sys
import sympy as s

def require(cond, msg):
    if not cond: raise ValueError(msg)
def zero(expr): return s.cancel(s.expand(expr))==0

def main():
    y,p,th=s.symbols('y p theta');k=s.symbols('kappa',positive=True)
    q={n:s.symbols(f'q{n}') for n in range(3,7)}
    psi=k*y*y/2+sum(q[n]*y**n/s.factorial(n) for n in q)
    a={1:1/k}
    for j in range(2,6):
        aj=s.symbols(f'a{j}')
        yy=sum(a[i]*p**i for i in a)+aj*p**j
        coeff=s.diff(psi,y).subs(y,yy).series(p,0,j+1).removeO().expand().coeff(p,j)
        a[j]=s.factor(s.solve(coeff,aj)[0])
    H=sum(a[j]*p**(j+1)/s.Integer(j+1) for j in a)
    h=(s.cos(th)*H.subs(p,s.tan(th))).series(th,0,7).removeO().expand()
    jets={j:s.factor(h.coeff(th,j)*s.factorial(j)) for j in range(2,7)}
    for j,expr in jets.items():
        require(not any(expr.has(q[n]) for n in q if n>j),f'higher graph jet in order {j}')
    require(zero(jets[2]-1/k),'h2 mismatch')
    require(zero(jets[3]+q[3]/k**3),'h3 mismatch')
    require(zero(jets[4]-(2/k-q[4]/k**4+3*q[3]**2/k**5)),'h4 mismatch')
    blocks=0
    for z in [s.Rational(1,5),s.Rational(1,3),s.Rational(1,2)]:
        for r in [s.Rational(2,3),s.Rational(1),s.Rational(3,2)]:
            for n in range(3,13):
                ct=(1+z**(2*n))/(1-z**(2*n));cs=2*z**n/(1-z**(2*n))
                M=s.Matrix([[ct,r**n*cs],[r**(-n)*cs,ct]])
                require(M.det()==1,'last-jet determinant mismatch')
                Minv=s.Matrix([[ct,-r**n*cs],[-r**(-n)*cs,ct]])
                require(M*Minv==s.eye(2),'last-jet inverse mismatch')
                require(1+2*z**(2*n)/(1-z**(2*n))==ct,'own-end weight mismatch')
                require(2*r**n*z**n/(1-z**(2*n))==r**n*cs,'opposite-end weight mismatch')
                blocks+=1
    u,v=s.symbols('u v');d=s.Integer(2)
    S=lambda x:x*x+s.Rational(1,7)*x**3+s.Rational(1,11)*x**4
    A=lambda x:1+s.Rational(1,5)*x
    C=lambda x:1+s.Rational(1,3)*x*x
    f=lambda x,y:A(x)*C(y)*(d-S(x)-S(y))
    R=f(u,v)*f(0,0)/(f(u,0)*f(0,v))
    t=lambda x:S(x)/(d-S(x))
    require(zero((1-R)-t(u)*t(v)),'four-density ratio mismatch')
    anchor=s.Rational(1,4)
    recovered_t=s.cancel((1-R.subs(v,anchor))/t(anchor))
    recovered=s.cancel(d*recovered_t/(1+recovered_t))
    require(zero(recovered-S(u)),'signed action recovery mismatch')
    require(s.diff(recovered,u,3).subs(u,0)==s.Rational(6,7),'odd jet lost')
    log_mixed=s.diff(s.diff(f(u,v),u)/f(u,v),v)
    require(zero(log_mixed+s.diff(S(u),u)*s.diff(S(v),v)/(d-S(u)-S(v))**2),'mixed log derivative mismatch')
    L=s.Matrix([[s.Rational(3,2),s.Rational(1,5)],[s.Rational(1,7),s.Rational(5,4)]])
    M=s.Matrix([[2,1],[0,3]]);V=L*M
    require(V*M.inv()==L and V!=L,'nonunimodular gain control failed')
    out={'purpose':'Finite symbolic and exact rational stress controls only; not a proof of smooth limiting or global billiard theorems.',
      'sympy_version':s.__version__,'graph_to_support_jets':{str(j):str(v) for j,v in jets.items()},
      'graph_order_tested_through':6,'rational_last_jet_blocks_checked':blocks,
      'density_fixture':'S(x)=x^2+x^3/7+x^4/11; d=2; separate factors A(x)=1+x/5,C(y)=1+y^2/3',
      'ratio_identity_verified':True,'nonzero_anchor':str(anchor),'recovered_third_action_derivative':'6/7',
      'mixed_log_identity_verified':True,'lattice_gain_matrix':str(M),'gain_determinant':str(M.det()),
      'nonunimodular_lattice_recovery_verified':True,
      'limitations':['Polynomial density fixture is not claimed to be a realized billiard law.',
                    'No trace-class convergence, finite smooth remainder, analytic continuation or global classification is numerically certified.',
                    'No author checker was imported.']}
    text=json.dumps(out,indent=2)+'\n'
    if len(sys.argv)>1:open(sys.argv[1],'w').write(text)
    print(text)
if __name__=='__main__':main()
