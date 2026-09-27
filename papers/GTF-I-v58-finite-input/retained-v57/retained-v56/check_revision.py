"""Exact finite regressions for v56, not a verifier of universal theorems.

The checks exercise chronological matrix products, the Ramsey decoder shortcut,
normal-kernel averaging, noncommutative phase gauges, rational spherical rows,
existential-formula generation and dyadic rounding. No spectral gap, Ramsey
number optimum, infinite-group closure, or universal theorem is numerically
certified here. Explicit exceptions keep every check active under python -O.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json
import re
from finite_group_formula import compile_formula, validate
from finite_precision import round_row, sample_integer

count=0
negative=[]

def check(ok, message):
    global count
    count+=1
    if not ok:raise RuntimeError(message)

def control(name, fails):
    check(fails,'Negative control escaped: '+name);negative.append(name)

def rejected(fn):
    try:fn()
    except (ValueError,KeyError,TypeError):return True
    return False

def matrix(rows):return tuple(tuple(F(x) for x in row) for row in rows)
def eye(n):return matrix([[int(i==j) for j in range(n)] for i in range(n)])
def mul(a,b):return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)
def shift(n,t):return matrix([[int(j==(i+t)%n) for j in range(n)] for i in range(n)])
def tv(p,q):return sum(abs(x-y) for x,y in zip(p,q))/2
def rnorm(a,b):return max(sum(abs(x-y) for x,y in zip(r,s)) for r,s in zip(a,b))
def fold(rows,n):
    a=eye(n)
    for b in rows:a=mul(a,b)
    return a

def test_extraction():
    n=8;k=2;cuts=[1,3,5,7];letters=['a','b']
    def kernel(t,c):
        q=F(t+1,1000);r=F(t+3,1200)
        if c=='a':q+=F(1,10)
        if c=='b':r+=F(1,8)
        return matrix([[1-q,q],[r,1-r]])
    def composite(i,j,c):
        word=['e']*(cuts[j]-cuts[i])
        if c!='e':word[0]=c
        return fold([kernel(cuts[i]+t+1,a) for t,a in enumerate(word)],k)
    table={(i,j,c):composite(i,j,c) for i in range(4) for j in range(i+1,4) for c in ['e']+letters}
    rep={c:table[0,1,c] for c in ['e']+letters}
    delta=max(rnorm(table[i,j,c],rep[c]) for i,j,c in table)
    D=matrix([[F(1,7)],[F(6,7)]])
    alpha=mul(matrix([[F(2,5),F(3,5)]]),kernel(1,'e'))
    decoder=mul(kernel(8,'e'),D)
    for length in range(3):
        for word in product(letters,repeat=length):
            path=[]
            for t,c in enumerate(word):path.append(table[t,t+1,c])
            path.append(table[length,3,'e'])
            actual=mul(mul(alpha,fold(path,k)),decoder)[0][0]
            candidate=mul(mul(mul(alpha,fold([rep[c] for c in word],k)),rep['e']),decoder)[0][0]
            check(abs(actual-candidate)<=F(5,7)*(length+1)*delta,'Ramsey telescoping error')
            expanded=['e']
            for t,c in enumerate(word):expanded += [c]+['e']*(cuts[t+1]-cuts[t]-1)
            expanded += ['e']*(cuts[3]-cuts[length])+['e']
            check(len(expanded)==n,'Shortcut omitted a real command')
            direct=mul(mul(matrix([[F(2,5),F(3,5)]]),fold([kernel(t+1,c) for t,c in enumerate(expanded)],k)),D)[0][0]
            check(direct==actual,'Composite boundary chronology')
    control('filler_need_not_be_idempotent',mul(rep['e'],rep['e'])!=rep['e'])
    control('empty_word_requires_filler_decoder',mul(alpha,decoder)!=mul(mul(alpha,rep['e']),decoder))
    control('return_row_not_identity',rep['e']!=eye(2))


def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(a):return tuple(a.index(i) for i in range(len(a)))
def power(a,n):
    if n<0:return power(inverse(a),-n)
    z=tuple(range(len(a)))
    for _ in range(n):z=compose(a,z)
    return z

def even(a):return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2==0

def test_gauge():
    e=(0,1,2);a=(1,0,2);alphabet=[a,(0,2,1),(2,1,0)]
    control('noncommutative_execution_order',compose(a,alphabet[1])!=compose(alphabet[1],a))
    for n in range(8):
        r=n%2
        for word in product(alphabet,repeat=n):
            g=e;z=power(a,n-r)
            check(even(z),'Initial phase gauge outside J')
            for t,b in enumerate(word,1):
                c=compose(compose(power(a,n-t),b),power(a,-(n-t+1)))
                check(even(c),'Command phase gauge outside J')
                z=compose(c,z);g=compose(b,g)
                direct=compose(compose(power(a,n-t),g),power(a,-r))
                check(z==direct,'Noncommutative gauge identity')
            check(compose(z,power(a,r))==g,'Final frame did not return correct physical product')
    for r,ell in product(range(2),repeat=2):
        b=(r-ell)%2
        for h in permutations(range(3)):
            if even(h):
                left=compose(compose(power(a,b),h),power(a,ell))
                transformed=compose(compose(power(a,b),h),power(a,-b))
                transformed=compose(transformed,power(a,ell+b-r))
                check(left==compose(transformed,power(a,r)),'Residue target equivalence')
    control('one_letter_exact_return_cannot_be_assumed',power((1,2,0),1)!=e)


def test_kernel():
    n=6;Q=matrix([[F(1,3) if i%2==j%2 else 0 for j in range(n)] for i in range(n)])
    V=matrix([[F(1,3) if j%2==i else 0 for j in range(n)] for i in range(2)])
    beta=matrix([[F(i+1,21) for i in range(n)]]);D=matrix([[F(i,5),1-F(i,5)] for i in range(n)])
    alpha=matrix([[sum(beta[0][j] for j in range(n) if j%2==i) for i in range(2)]])
    check(mul(Q,Q)==Q,'Kernel average idempotent')
    check(mul(alpha,V)==mul(beta,Q),'Orbit initialization')
    for t in range(6):
        P=shift(6,t);R=shift(2,t%2)
        check(mul(V,P)==mul(R,V),'Orbit intertwining')
        check(mul(Q,P)==mul(P,Q),'Normal kernel averaging commutation')
        check(mul(mul(mul(beta,Q),P),D)==mul(mul(alpha,R),mul(V,D)),'Purified output')
    control('physical_fiber_outputs_can_differ',mul(beta,D)!=mul(mul(beta,shift(6,2)),D))
    control('initialization_not_forced_pure',all(x>0 for x in alpha[0]))


def test_sphere():
    Rx=matrix([[1,0,0],[0,F(3,5),-F(4,5)],[0,F(4,5),F(3,5)]])
    Rz=matrix([[F(3,5),-F(4,5),0],[F(4,5),F(3,5),0],[0,0,1]])
    transpose=lambda a:tuple(zip(*a))
    for R in [Rx,Rz]:check(mul(transpose(R),R)==eye(3),'Rational orthogonality')
    control('SO3_alphabet_not_abelian',mul(Rx,Rz)!=mul(Rz,Rx))
    vertices=matrix([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
    rotations=[eye(3),Rx,transpose(Rx),Rz,transpose(Rz)];r=F(1,3)
    def row(x):
        values=[F(0)]*6
        for j,v in enumerate(x):values[2*j+int(v<0)]+=abs(v)
        left=1-sum(values);check(left>=0,'Octahedron enclosure')
        values[0]+=left/2;values[1]+=left/2
        return tuple(values)
    tables=[]
    for R in rotations:
        points=mul(vertices,transpose(R));T=tuple(row(tuple(r*x for x in v)) for v in points)
        check(all(sum(v)==1 and min(v)>=0 for v in T),'Legal spherical stochastic rows')
        check(mul(T,vertices)==tuple(tuple(r*x for x in v) for v in points),'Spherical row means')
        tables.append(T)
    alpha=matrix([[0,0,0,0,1,0]]);rho=r**3
    for word in product(range(5),repeat=3):
        output=mul(mul(alpha,fold([tables[i] for i in word],6)),vertices)[0]
        physical=(F(0),F(0),F(1))
        for i in word:physical=tuple(sum(x*y for x,y in zip(rr,physical)) for rr in rotations[i])
        check(output==tuple(rho*x for x in physical),'Exact noncommuting spherical example')
    for k in range(1,65):
        t=F(2,k);integral=t-F(k,4)*t*t
        check(integral==F(1,k),'Exact spherical cap quantization')
        delta=F(1,4*k);lam_power_bound=F(1,64*k*k)
        check(delta+4*lam_power_bound/delta==F(1,2*k),'Spherical smoothing budget')
    control('unit_amplitude_decoder_requires_slack',F(1)/r**3>1)
    control('sphere_vector_radius_not_binary_half',F(3,4)!=F(3,8))


def parse(tokens):
    stack=[];root=None
    for token in tokens:
        if token=='(':
            node=[]
            if stack:stack[-1].append(node)
            elif root is not None:raise ValueError('Multiple expressions')
            else:root=node
            stack.append(node)
        elif token==')':
            if not stack:raise ValueError('Unmatched close parenthesis')
            stack.pop()
        else:
            if not stack:raise ValueError('Atom outside expression')
            stack[-1].append(token)
    if stack or root is None:raise ValueError('Incomplete expression')
    return root

def evaluate(ast,env):
    if isinstance(ast,str):
        if ast in env:return env[ast]
        if ast=='true':return True
        return F(ast)
    op,*args=ast;v=[evaluate(x,env) for x in args]
    if op=='+':return sum(v)
    if op=='*':
        q=F(1)
        for x in v:q*=x
        return q
    if op=='/':return v[0]/v[1]
    if op=='-':return -v[0] if len(v)==1 else v[0]-v[1]
    if op=='=':return v[0]==v[1]
    if op=='>=':return v[0]>=v[1]
    if op=='<=':return v[0]<=v[1]
    raise ValueError(op)

def test_complexity():
    U=matrix([[1,2],[3,1],[2,4]]);V=matrix([[2,1,3],[0,4,1]])
    A=mul(U,V);norms=[sum(row) for row in A];P=tuple(tuple(x/t for x in row) for row,t in zip(A,norms))
    masses=[sum(row) for row in V];D=tuple(tuple(x/t for x in row) for row,t in zip(V,masses))
    E=tuple(tuple(U[s][i]*masses[i]/norms[s] for i in range(2)) for s in range(3))
    check(mul(E,D)==P,'NMF stochastic normalization')
    check(all(sum(row)==1 and min(row)>=0 for row in E+D),'NMF normalized rows')
    control('raw_NMF_factors_need_normalization',any(sum(row)!=1 for row in V))
    data={'multiplication':[[0,1],[1,0]],'identity':0,'k':2,'epsilon':'0',
          'targets':[[[['1','0'],['0','1']]],[[['1/3','2/3'],['2/3','1/3']]]]}
    formula,stats=compile_formula(data);env={}
    for g,i,j in product(range(2),repeat=3):env[f'P_{g}_{i}_{j}']=F(int(j==(i+g)%2))
    starts=[[F(1),F(0)],[F(1,3),F(2,3)]]
    for s,i in product(range(2),repeat=2):env[f'E_{s}_{i}']=starts[s][i]
    for i,c in product(range(2),repeat=2):env[f'D_0_{i}_{c}']=F(int(i==c))
    for s,g,c in product(range(2),repeat=3):env[f'Z_{s}_0_{g}_{c}']=F(0)
    claims=[]
    for line in formula.splitlines():
        if line.startswith('(assert '):claims.append(parse(iter(re.findall(r'\(|\)|[^\s()]+',line)))[1])
    check(len(claims)==stats['constraints'],'Generated constraint count')
    for claim in claims:check(evaluate(claim,env),'Generated finite group formula rejected exact witness')
    broken=dict(env);broken['P_0_0_0']=F(0)
    control('group_identity_constraint_enforced',not all(evaluate(c,broken) for c in claims))
    bad=dict(data);bad['epsilon']='-1'
    control('negative_error_rejected',rejected(lambda:validate(bad)))
    bad=dict(data);bad['multiplication']=[[0,1],[1,1]]
    control('nongroup_input_rejected',rejected(lambda:validate(bad)))
    bad=dict(data);bad['epsilon']=0.1
    control('inexact_float_input_rejected',rejected(lambda:validate(bad)))
    Path('evidence').mkdir(exist_ok=True)
    Path('evidence/FINITE_GROUP_EXAMPLE.json').write_text(json.dumps(data,indent=2)+'\n')
    Path('evidence/FINITE_GROUP_EXAMPLE.smt2').write_text(formula)
    return stats


def test_rounding():
    rows=[]
    for m in range(1,5):
        for offset in range(1,7):
            raw=[F((i+1)*offset+i*i+1) for i in range(m)];total=sum(raw)
            rows.append(tuple(x/total for x in raw))
    for row in rows:
        for b in range(7):
            masses=round_row(row,b);q=1<<b;rounded=tuple(F(x,q) for x in masses)
            check(sum(masses)==q and min(masses)>=0,'Rounded probability legal')
            check(tv(row,rounded)<=F(len(row)-1,q),'Rounding error budget')
            samples=Counter(sample_integer(masses,u) for u in range(q))
            check(all(samples[i]==mass for i,mass in enumerate(masses)),'Exact integer sampling law')
    control('invalid_row_rejected',rejected(lambda:round_row([F(2),F(-1)],4)))
    control('invalid_random_integer_rejected',rejected(lambda:sample_integer([1,3],4)))
    control('non_dyadic_denominator_rejected',rejected(lambda:sample_integer([1,2],0)))
    def rounded(M,b):return tuple(tuple(F(v,1<<b) for v in round_row(row,b)) for row in M)
    alpha=matrix([[F(1,3),F(2,3)]]);D=matrix([[F(1,7),F(6,7)],[F(4,7),F(3,7)]])
    T=[matrix([[F(6,7),F(1,7)],[F(2,5),F(3,5)]]),matrix([[F(1,6),F(5,6)],[F(3,8),F(5,8)]])]
    for b in [3,6,9]:
        for n in range(6):
            for word in product(range(2),repeat=n):
                x=mul(mul(alpha,fold([T[c] for c in word],2)),D)[0]
                y=mul(mul(rounded(alpha,b),fold([rounded(T[c],b) for c in word],2)),rounded(D,b))[0]
                check(tv(x,y)<=F(n+2,1<<b),'Accumulated clocked rounding error')
        for n in range(129):
            P=shift(2,n)
            x=mul(mul(alpha,P),D)[0];y=mul(mul(rounded(alpha,b),P),rounded(D,b))[0]
            check(tv(x,y)<=F(2,1<<b),'Stationary permutation error independent of horizon')
    control('stochastic_rounding_can_accumulate',abs(F(7,8)**8-F(6,7)**8)>F(1,56))
    control('binary_TV_has_half_factor',tv([F(1),F(0)],[F(0),F(1)])==1 and tv([F(1),F(0)],[F(0),F(1)])!=2)


def main():
    test_extraction();test_gauge();test_kernel();test_sphere();stats=test_complexity();test_rounding()
    print(json.dumps({'status':'success','exact_finite_assertions':count,'negative_controls_detected':negative,
                      'finite_group_formula':stats,'scope':'Finite rational/algebraic identities and negative controls only; not universal theorem verification or numerical certification of a spectral gap.'},sort_keys=True))

if __name__=='__main__':main()
