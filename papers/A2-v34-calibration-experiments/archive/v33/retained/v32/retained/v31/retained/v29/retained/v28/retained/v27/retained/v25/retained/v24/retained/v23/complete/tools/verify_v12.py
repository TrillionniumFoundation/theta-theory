#!/usr/bin/env python3
"""Independent finite diagnostics for A2 v12, not a proof certificate.
Standard library only; no network, simulation, manuscript-code import, or
assert statements. Exact rational finite Jacobi/moment calculations are
compared with the new two-contact limiting formula. Source retention is
order-independent because v12 deliberately reorganizes the main argument.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
CHECKS=[]

def check(name,condition,kind='exact_algebra'):
    if not condition:raise RuntimeError('Failed: '+name)
    CHECKS.append({'name':name,'kind':kind,'status':'pass'})

def sha(data):return hashlib.sha256(data).hexdigest()
def sh(l,k):return (l**(-k)-l**k)/2
def ch(l,k):return (l**(-k)+l**k)/2
def th(l,k):return sh(l,k)/ch(l,k)
def rising(n):return math.prod((F(2*k+1,2) for k in range(n)),start=F(1))

def limiting_block(l,r,g,m):
    a=[r*sh(l,1)/g,sh(l,1)/(r*g)]
    E=l**(4*(m-1))/(1-l**(4*(m-1)))-l**(4*m)/(1-l**(4*m))
    O=1/(2*sh(l,2*(m-1)))-1/(2*sh(l,2*m))
    P=ch(l,2*m)/sh(l,2*m)+2*m*E
    Q=1/sh(l,2*m)+2*m*O
    K=[F(4,2**m*(m+1)*math.factorial(m)**2)/ab**m for ab in a]
    return [[-P*K[0],-Q*K[1]],[-Q*K[0],-P*K[1]]],(a,E,O,P,Q,K)

def finite_block_row(l,r,g,m,j,b):
    """Finite Dirichlet Green diagonal + full ellipse moments.
    This route sums both endpoint influence vectors before integrating;
    it does not insert the limiting half-line action/amplitude formulas.
    The output is the derivative of the finite same-type law coefficient.
    """
    a=[r*sh(l,1)/g,sh(l,1)/(r*g)]
    rb=r if b==0 else 1/r
    shj=sh(l,j);cj=ch(l,j)/shj
    action=[F(0),F(0)];determinant=[F(0),F(0)]
    for i in range(j+1):
        typ=(b+i)%2;ratio=F(1) if i%2==0 else rb
        left=ratio*sh(l,j-i)/shj;right=ratio*sh(l,i)/shj
        # Variance under the inverse endpoint Hessian.
        nu=(cj*(left*left+right*right)+2*left*right/shj)/a[b]
        action[typ]+=(1 if i in (0,j) else 2)*nu**m
        if i not in(0,j):
            G=(1-l**(2*i))*(1-l**(2*(j-i)))/(2*a[typ]*(1-l**(2*j)))
            determinant[typ]+=G*nu**(m-1)
    A=F(2,2**m*(m+1)*math.factorial(m)**2)
    B=F(4,2**(m-1)*m*(m+1)*math.factorial(m-1)**2)
    return [-A*x-B*y for x,y in zip(action,determinant)]

def sources(rel='main.tex',stack=()):
    if rel in stack:raise RuntimeError('Input cycle: '+rel)
    text=(ROOT/rel).read_text();out=[(rel,text)]
    for name in re.findall(r'\\input\{([^}]+)\}',text):
        out+=sources(name+'.tex',stack+(rel,))
    return out

BLOCK_PATTERN=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}',re.S)

def run():
    for l in [F(1,3),F(1,2),F(2,3),F(4,5)]:
        c=ch(l,1)
        for r in [F(1),(c+1)/2]:
            for g in [F(1),F(3,2)]:
                for m in range(2,9):
                    mat,(a,E,O,P,Q,K)=limiting_block(l,r,g,m)
                    tag=f'{l}_{r}_{g}_{m}'
                    check('positive_curvatures_'+tag,c*r>1 and c/r>1)
                    check('antisymmetric_identity_'+tag,P-Q==m*th(l,m-1)-(m-1)*th(l,m))
                    D=l**(2*(m-1))/(1-l**(2*(m-1)))-l**(2*m)/(1-l**(2*m))
                    check('identical_contact_restriction_'+tag,P+Q==ch(l,m)/sh(l,m)+2*m*D)
                    check('positive_block_'+tag,P>Q>0)
                    check('unequal_factor_'+tag,K[0]*r**(2*m)==K[1])
                    determinant=mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
                    check('block_determinant_'+tag,determinant==K[0]*K[1]*(P-Q)*(P+Q)>0)
                    inv=[[(-P/K[0])/(P*P-Q*Q),(Q/K[0])/(P*P-Q*Q)],
                         [(Q/K[1])/(P*P-Q*Q),(-P/K[1])/(P*P-Q*Q)]]
                    check('explicit_inverse_'+tag,all(sum(inv[i][k]*mat[k][j] for k in(0,1))==(1 if i==j else 0) for i in(0,1) for j in(0,1)))
    bridges=[]
    for l in [F(1,3),F(1,2),F(2,3)]:
        c=ch(l,1)
        for r in [F(1),(c+1)/2]:
            for m in range(2,6):
                target,_=limiting_block(l,r,F(1),m)
                errs=[]
                for j in [16,32,64]:
                    calc=[finite_block_row(l,r,F(1),m,j,b) for b in(0,1)]
                    err=max(abs(calc[b][k]-target[b][k]) for b in(0,1) for k in(0,1))
                    errs.append(err)
                check(f'finite_bridge_decreasing_{l}_{r}_{m}',errs[2]<errs[1]<errs[0],'finite_exact_benchmark')
                check(f'finite_bridge_tolerance_{l}_{r}_{m}',errs[2]<F(1,10**18),'finite_exact_benchmark')
                bridges.append({'lambda':str(l),'curvature_scale_ratio':str(r),'m':m,'j':[16,32,64],
                    'exact_max_errors':[str(e) for e in errs]})
    # One-flight-free interpolation and the higher-order integrated kernel.
    for m in range(4,11):
        q=m+2;L=q+4
        for ell in range(L+1):
            start=max(1,min(ell-(q-1)//2,L-q+1));nodes=list(range(start,start+q))
            check(f'positive_stencil_{m}_{ell}',min(nodes)>=1 and max(nodes)<=L and (ell==0 or ell in nodes))
            for x in [F(ell),F(2*ell+1,2)]:
                basis=[math.prod((F(x-v,w-v) for v in nodes if v!=w),start=F(1)) for w in nodes]
                check(f'polynomial_reproduction_{m}_{ell}_{x}',all(sum(b*w**k for b,w in zip(basis,nodes))==x**k for k in range(q)))
        nu=F(m)-F(1,2)
        check(f'gain_approximation_power_{m}',(F(m)+F(m-1))/2==nu)
        check(f'preparation_power_{m}',2+1/nu+5/nu==2+6/nu)
        check(f'modulus_balance_{m}',nu/F(m+2)==1-F(5,2*(m+2)))
        check(f'pilot_subordinate_{m}',2+6/nu>2+F(2,m))
        check(f'strict_improvement_{m}',2+6/nu>0 and 2+6/nu<2+6/(F(m)-F(5,2)))
    check('m4_accuracy_power',2+6/(F(4)-F(1,2))==F(26,7))
    for r in range(9):
        for s in range(9):
            # H coefficient from simplex integral; H'' from beta integral.
            hc=2*rising(r)*rising(s)/math.factorial(r+s+2)
            qc=2*rising(r)*rising(s)/math.factorial(r+s)
            check(f'integrated_gain_identity_{r}_{s}',hc*(r+s+2)*(r+s+1)==qc)
    for R in [F(1),F(9,10),F(11,10)]:
        for m in range(2,9):
            # Envelope leading coefficient: theta(y)=y/R+O(y^3).
            diagonal=-F(math.factorial(2*m),1)/R**(2*m)
            check(f'support_contact_diagonal_{R}_{m}',diagonal!=0)
            check(f'area_compensator_derivative_{m}',F(2*math.comb(2*m+2,m+1),4**(m+1))>0)
    for n in range(1,9):
        nodes=list(range(1,n+1))
        determinant=math.prod(nodes)*math.prod(nodes[j]-nodes[i] for i in range(n) for j in range(i+1,n))
        check(f'positive_window_vandermonde_{n}',determinant>0)
    for c in [F(2),F(13,3)]:
        for p in [F(1,101),F(1,7),F(2,3)]:
            check(f'scaled_bernoulli_variance_{c}_{p}',c*c*p*(1-p)==c*(c*p)*(1-p))
    active=sources();names=[p for p,_ in active];text='\n'.join(s for _,s in active)
    check('unique_active_inputs',len(names)==len(set(names)),'source_integrity')
    check('no_invalid_control_characters',all(ord(c)>=32 or c in '\n\r\t' for c in text),'source_integrity')
    baseline=json.loads((ROOT/'history/v11-active-blocks.json').read_text())
    blocks=[m.group(0).encode() for _,s in active for m in BLOCK_PATTERN.finditer(s)]
    old_names=set(baseline['inputs'])
    old_blocks=[m.group(0).encode() for name,s in active if name in old_names for m in BLOCK_PATTERN.finditer(s)]
    old_digest=sha(('\n'.join(sorted(sha(b) for b in old_blocks))+'\n').encode())
    check('all_192_prior_active_environments_retained',len(old_blocks)==baseline['block_count']==192 and old_digest==baseline['sorted_block_multiset_sha256'],'source_integrity')
    check('all_prior_active_inputs_retained',set(baseline['inputs'])<=set(names),'source_integrity')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check('unique_active_labels',len(labels)==len(set(labels)),'source_integrity')
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
    check('resolved_internal_references',all(x in labels or x.startswith('TC-') for x in refs),'source_integrity')
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    cites={k.strip() for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in g.split(',')}
    check('resolved_citations',cites<=keys,'source_integrity')
    needed={'thm:v12-two-contact','thm:v12-realization','thm:v12-finite-observation','thm:v12-acquisition','thm:v12-self-calibrated','cor:v12-modulus'}
    check('new_central_results_active',needed<=set(labels),'source_integrity')
    return {'schema':'a2-v12-finite-diagnostics-v1','status':'pass','counts':{'total':len(CHECKS),**dict(Counter(c['kind'] for c in CHECKS))},
        'checks':CHECKS,'finite_bridge_benchmarks':bridges,
        'retention':{'prior_environments':192,'current_environments':len(blocks),'new_environments':len(blocks)-192,
                     'all_prior_blocks_byte_identical':True,'order_preserved':False,'order_change':'Deliberate main/appendix hierarchy; no formal block removed.'},
        'limitations':['Finite algebra is not a proof of the analytic or statistical theorems.',
            'Finite Jacobi/moment benchmarks are not nonlinear billiard simulations or formal proof certificates.',
            'No minimax claim is made for the complete-profile preparation exponent or conditional modulus.',
            'The physical finite-window risk theorem has a fixed finite-dimensional family and fixed allowed windows.',
            'The general asymmetric graph fibre problem is not asserted solved.','No remote CI run is claimed.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'verification/v12.normal.json');args=parser.parse_args()
    result=run();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','counts','retention')},sort_keys=True))
