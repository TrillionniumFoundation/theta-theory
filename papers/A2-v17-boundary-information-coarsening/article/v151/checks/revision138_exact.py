#!/usr/bin/env python3
"""Exact finite regressions for v138; the general intrinsic proofs are not certified."""
from pathlib import Path
import itertools,json,math
import sympy as s
ROOT=Path(__file__).resolve().parents[1]

# Independent highest-weight orbit computation for wedge^2 Sym^2, in ranks 2--6.
def wedge_rep(n):
    mon=list(itertools.combinations_with_replacement(range(n),2))
    mi={p:i for i,p in enumerate(mon)};N=len(mon)
    wp=list(itertools.combinations(range(N),2));wi={p:i for i,p in enumerate(wp)}
    def root(a,b):
        cols=[{} for _ in mon]
        for j,p in enumerate(mon):
            for k in range(2):
                if p[k]==b:
                    q=list(p);q[k]=a;i=mi[tuple(sorted(q))]
                    cols[j][i]=cols[j].get(i,0)+1
        out=s.zeros(len(wp))
        for j,(i,k) in enumerate(wp):
            for t,c in cols[i].items():
                if t!=k:out[wi[tuple(sorted((t,k)))],j]+=c*(1 if t<k else -1)
            for t,c in cols[k].items():
                if i!=t:out[wi[tuple(sorted((i,t)))],j]+=c*(1 if i<t else -1)
        return out
    w=s.zeros(len(wp),1);w[wi[(mi[(0,0)],mi[(0,1)])]]=1
    assert all(root(a,a+1)*w==s.zeros(len(wp),1) for a in range(n-1))
    # Sparse integer vectors with rational echelon reduction, no numerical rank.
    lowers=[root(a+1,a) for a in range(n-1)]
    basis={};queue=[]
    def insert(v):
        v={i:s.Rational(c) for i,c in enumerate(v) if c}
        for piv,b in sorted(basis.items()):
            c=v.get(piv,0)
            if c:
                for i,x in b.items():
                    y=v.get(i,0)-c*x
                    if y:v[i]=y
                    else:v.pop(i,None)
        if not v:return False
        p=min(v);c=v[p];v={i:x/c for i,x in v.items()};basis[p]=v;queue.append(v);return True
    insert(w);head=0
    while head<len(queue):
        d=queue[head];head+=1;v=s.zeros(len(wp),1)
        for i,c in d.items():v[i]=c
        for L in lowers:insert(L*v)
    dim=n*(n-1)*(n+1)*(n+2)//8
    assert len(basis)==len(wp)==dim
    return {'n':n,'quadratic_dimension':N,'highest_weight_orbit_rank':len(basis),'hook_dimension':dim}
reps=[wedge_rep(n) for n in range(2,7)]

# All maximal minors of the actual multiplication block, two rational n=3 charts.
# The bottom-left block is varied independently and does not enter the factor.
fit=[]
for M in [s.Matrix([[1,2,0],[0,1,1],[1,0,1]]),s.Matrix([[1,2,0],[0,0,0],[1,0,1]])]:
    n=3;mon=list(itertools.combinations_with_replacement(range(n),2));N=len(mon);p=N-2
    ix={q:i for i,q in enumerate(mon)};B=s.zeros(N)
    for j,(a,b) in enumerate(mon):
        for i in range(n):
            for k in range(n):B[ix[tuple(sorted((i,k)))],j]+=M[i,a]*M[k,b]
    gam=s.Matrix([[1,0,0,1,0,0],[0,1,0,0,1,0],[0,0,1,0,0,1],[0,0,0,1,1,1]])
    assert gam.rank()==p;Q=gam*B
    A0=s.Matrix(p,n,lambda i,j:(i+1)*(j+2)+int(i==j))
    full=s.zeros(1+n+p,1+n+N);full[0,0]=1;full[1:1+n,1:1+n]=M
    full[1+n:,1:1+n]=A0;full[1+n:,1+n:]=Q
    count=0
    for cols in itertools.combinations(range(1+n+N),1+n+p):
        actual=full[:,list(cols)].det();fixed=list(range(1+n))
        expected=M.det()*Q[:,[c-(1+n) for c in cols if c>=1+n]].det() if all(c in cols for c in fixed) else 0
        assert actual==expected;count+=1
    fit.append({'rank_M':M.rank(),'maximal_minors_checked':count})

# Explicit same-discriminant pairs, including the hyperelliptic dimensions.
u,v=s.symbols('u v');pairs=[]
for n in range(3,9):
    vals=list(range(1,n-1));S=s.Matrix([[0,1],[1,0]]);J=s.Matrix([[0,1],[0,0]])
    As=s.eye(n);Bs=s.diag(0,0,*vals);Aj=s.diag(S,s.eye(n-2));Bj=s.diag(S*J,*vals)
    fs=(u*As+v*Bs).det();fj=(u*Aj+v*Bj).det()
    assert s.expand(fs+fj)==0
    assert Bs.rank()==n-2 and Bj.rank()==n-1
    assert (As.inv()*Bs)[:2,:2]==s.zeros(2)
    assert (Aj.inv()*Bj)[:2,:2]==J
    pairs.append({'n':n,'same_determinant_up_to_scalar':True,'double_root_ranks':[n-2,n-1]})

# Polynomial square-root correction in a nonsemisimple self-adjoint example.
A=s.Matrix([[0,1],[1,0]]);C=s.Matrix([[2,1],[0,2]])
H=s.eye(2)+C/2;K=s.sqrt(2)*(s.eye(2)+(C-2*s.eye(2))/8)
assert s.simplify(K*K-H)==s.zeros(2)
assert K.T*A==A*K and K*C==C*K
Ap=A*H;Bp=Ap*C;h=K.inv()
assert Ap==Ap.T and Bp==Bp.T
assert s.simplify(h.T*Ap*h-A)==s.zeros(2)
assert s.simplify(h.T*Bp*h-A*C)==s.zeros(2)

# Hyperelliptic moduli count after fixing three branch points.
mods=[{'genus':g,'n':2*g+2,'dimension':2*g-1} for g in range(2,9)]
checks={'highest_weight_generation_five_ranks':len(reps)==5,'multiplication_block_all_maximal_minors':True,
'same_discriminant_different_partitions_six_dimensions':len(pairs)==6,'nonsemisimple_congruence_correction':True}
out={'revision':138,'ok':all(checks.values()),'checks':checks,'wedge_square':reps,'multiplication_blocks':fit,
'discriminant_pairs':pairs,'moduli_dimension_examples':mods,
'structural_proofs_not_machine_certified':['intrinsic recovery of deepest stratum and oriented ruling',
'automatic coefficient extraction for every quadratic relation space in the stated range',
'abstract reconstruction of all pencils in arbitrary dimension','hyperelliptic isomorphism-class reconstruction',
'full historical novelty and the unread Ballico 1993 theorem comparison']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION138_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
