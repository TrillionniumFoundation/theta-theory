#!/usr/bin/env python3
"""Exact finite instrument identities and separate floating spectral probes.
These diagnostics do not certify a continuum theorem, priority or peer review.
"""
from __future__ import annotations
import itertools,json,math
import numpy as np
import sympy as sp
COUNTS={};DETAILS={}

def check(ok,group,detail):
    if not bool(ok):raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def same(a,b):
    return (a-b).applyfunc(sp.simplify)==sp.zeros(*a.shape)

I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
PAULI=[X,Y,Z];BASIS=[I,X,Y,Z]
H=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2)
weak=[sp.diag(sp.Rational(3,5),sp.Rational(4,5)),sp.diag(sp.Rational(4,5),sp.Rational(3,5))]
ad=[sp.diag(1,sp.Rational(3,5)),sp.Matrix([[0,sp.Rational(4,5)],[0,0]])]
OPS=[weak,[(H*k*H).applyfunc(sp.simplify) for k in weak],ad,[(H*k*H).applyfunc(sp.simplify) for k in ad]]
VERTICES=[(I+sgn*p)/2 for p in PAULI for sgn in (1,-1)]
v=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)]);VERTICES.append(v*v.T)
M=len(VERTICES);ANCHOR=M-1
COORD=sp.Matrix([[sp.trace(b*t) for t in VERTICES[:6]] for b in BASIS])

def depol(t):return t/4+3*sp.trace(t)*I/8

def branch(a,y,t):
    k=OPS[a][y]
    return depol(k*t*k.H).applyfunc(sp.simplify)

def adjoint(a,y,t):
    k=OPS[a][y]
    return (k.H*depol(t)*k).applyfunc(sp.simplify)

def weights(t):
    mass=sp.simplify(sp.trace(t));b=[sp.simplify(sp.trace(p*t)) for p in PAULI]
    rest=(mass-sum(abs(x) for x in b))/6
    w=[rest+max(s*x,0) for x in b for s in (1,-1)]
    # Exact Caratheodory reduction in trace/Bloch coordinates, without floating LP.
    while len(ids:=[i for i,x in enumerate(w) if x>0])>4:
        z=COORD[:,ids].nullspace()[0]
        pos=[j for j,x in enumerate(z) if x>0]
        if not pos:z=-z;pos=[j for j,x in enumerate(z) if x>0]
        lam=min(w[ids[j]]/z[j] for j in pos)
        for j,i in enumerate(ids):w[i]=sp.simplify(w[i]-lam*z[j])
    return w+[sp.Integer(0)]

def exact_realization():
    matrices={}
    for a,ks in enumerate(OPS):
        check(same(sum((k.H*k for k in ks),sp.zeros(2)),I),'exact_primitive_normalization',a)
        for y in (0,1):
            rows=[]
            for i,t in enumerate(VERTICES):
                out=branch(a,y,t);w=weights(out)
                check(all(q>=0 for q in w),'exact_nonnegative_branch',(a,y,i))
                check(sum(w)==sp.trace(out),'exact_unnormalized_branch_mass',(a,y,i))
                check(same(sum((q*tau for q,tau in zip(w,VERTICES)),sp.zeros(2)),out),
                      'exact_all_word_intertwining',(a,y,i))
                check(sum(q!=0 for q in w)<=4,'exact_sparse_successors',(a,y,i))
                rows.append(w)
            matrices[a,y]=sp.Matrix(rows)
        check(matrices[a,0]*sp.ones(M,1)+matrices[a,1]*sp.ones(M,1)==sp.ones(M,1),
              'exact_report_normalization',a)
    check(all(x==0 for x in list(matrices[2,1][4,:])), 'exact_null_branch','amplitude damping on |0>')
    # Two nonreset commands have incompatible unique invariant density matrices.
    stat_z=(I+sp.Rational(16,91)*Z)/2;stat_x=(I+sp.Rational(16,91)*X)/2
    check(same(branch(2,0,stat_z)+branch(2,1,stat_z),stat_z),'exact_distinct_fixed_states','Z')
    check(same(branch(3,0,stat_x)+branch(3,1,stat_x),stat_x),'exact_distinct_fixed_states','X')
    check(not same(branch(3,0,stat_z)+branch(3,1,stat_z),stat_z),
          'exact_no_common_stationary_state','fixed states differ')
    for a in (2,3):
        check(not same(branch(a,0,VERTICES[0])/sp.trace(branch(a,0,VERTICES[0])),
                       branch(a,0,VERTICES[1])/sp.trace(branch(a,0,VERTICES[1]))),
              'exact_nonreset_branch',a)
    # Direct independent forward word sums and terminal audit probabilities.
    effects=[(I+Z)/6,(I+X)/8];effects.append(I-sum(effects,sp.zeros(2)))
    for e in effects:check(e[0,0]>=0 and e[1,1]>=0 and e.det()>=0,'exact_audit_positivity','three outcomes')
    alphabet=list(itertools.product(range(4),(0,1)))
    for n in range(3):
        for word in itertools.product(alphabet,repeat=n):
            state=VERTICES[ANCHOR];row=sp.zeros(1,M);row[ANCHOR]=1
            for a,y in word:state=branch(a,y,state);row=row*matrices[a,y]
            check(sum(row)==sp.trace(state),'exact_finite_word_probability',str(word))
            for e in effects:
                d=sp.Matrix([sp.trace(e*t) for t in VERTICES])
                check(sp.simplify((row*d)[0]-sp.trace(e*state))==0,'exact_terminal_effect_law',str(word))
    # An adaptive observer toggles its own state after report 0; report 1 halts.
    # The physical operator solve and hidden-state solve are independent.
    gs=[sp.diag(1,sp.Rational(6,5)),sp.diag(sp.Rational(5,4),sp.Rational(29,20))]
    fs=[sum(((z-r)**2*e for z,e in zip((-1,0,1),effects)),sp.zeros(2)) for r in (-1,1)]
    coeff=lambda a:sp.Matrix([sp.simplify(sp.trace(b*a)/2) for b in BASIS])
    tp=sp.zeros(8);gc=sp.zeros(8,1);sc=sp.zeros(8,1)
    tm=sp.zeros(2*M);gm=sp.zeros(2*M,1);sm=sp.zeros(2*M,1)
    for s in range(2):
        other=1-s
        gc[4*s:4*s+4,0]=coeff(gs[s]);sc[4*s:4*s+4,0]=coeff(adjoint(s,1,fs[s]))
        for j,b in enumerate(BASIS):tp[4*s:4*s+4,4*other+j]=coeff(adjoint(s,0,b))
        tm[s*M:(s+1)*M,other*M:(other+1)*M]=matrices[s,0]
        for i,t in enumerate(VERTICES):
            gm[s*M+i]=sp.trace(gs[s]*t);sm[s*M+i]=sp.trace(fs[s]*branch(s,1,t))
            check(sum(matrices[s,0][i,j] for j in range(M))<=sp.Rational(16,25),
                  'exact_stopping_survival_margin',(s,i))
    hp=(sp.eye(8)-tp).inv()*gc;kp=(sp.eye(8)-tp).inv()*sc
    hm=(sp.eye(2*M)-tm).inv()*gm;km=(sp.eye(2*M)-tm).inv()*sm
    for s in range(2):
        hc=sum((hp[4*s+j]*b for j,b in enumerate(BASIS)),sp.zeros(2))
        kc=sum((kp[4*s+j]*b for j,b in enumerate(BASIS)),sp.zeros(2))
        for i,t in enumerate(VERTICES):
            check(sp.simplify(sp.trace(hc*t)-hm[s*M+i])==0,'exact_adaptive_stopped_cost',(s,i))
            check(sp.simplify(sp.trace(kc*t)-km[s*M+i])==0,'exact_adaptive_stopped_squared_risk',(s,i))
    DETAILS['adaptive_example']={'simulator_states':M,'observer_live_labels':2,
        'initial_expected_cost':str(hm[ANCHOR]),'initial_squared_risk':str(km[ANCHOR]),
        'row_successor_bound':4,'scope':'Exact operator and rational killed-matrix identities, not sampled paths.'}

def exact_boundaries():
    # Projective cap integral and mixed-vertex threshold algebra.
    x,r,s,a=sp.symbols('x r s a',real=True)
    for d in range(2,9):
        val=sp.integrate((d-1)*(1-x)**(d-2),(x,1-r*r,1))
        check(sp.simplify(val-r**(2*d-2))==0,'exact_projective_cap_integral',d)
    check(sp.expand((a-s)-(1-s)*(2*a-1)-(1-a)*(1-2*s))==0,
          'exact_mixed_vertex_cap_algebra','nonnegative on stated domain')
    # One call can fail strict interiority although two calls have a uniform floor.
    A=sp.Matrix([[0,-sp.Rational(1,2),sp.Rational(1,2)],
                 [sp.Rational(1,2),-sp.Rational(1,2),0],
                 [sp.Rational(1,2),0,sp.Rational(1,2)]])
    check((sp.eye(3)-A.T*A).det()==0,'exact_block_first_call_boundary','singular value one')
    B=A*A
    check(sp.trace(B.T*B)==sp.Rational(5,8),'exact_block_second_call_margin','Frobenius norm')
    check(sp.Rational(5,8)<sp.Rational(7,8)**2,'exact_block_second_call_margin','eta=1/8')
    # An average floor cannot substitute for conditioning on the recorded branch.
    U=sp.Matrix([[2,-1],[1,2]])/sp.sqrt(5);rho=sp.diag(1,0);states=[]
    for n in range(18):
        check(rho.det()==0 and sp.trace(rho)==1,'exact_recorded_unitary_branch_pure',n)
        check(all(rho!=old for old in states),'exact_distinct_pure_orbit_prefix',n)
        avg=sum((p*rho*p.H for p in BASIS),sp.zeros(2))/8+U*rho*U.H/2
        check(same(avg-I/4,U*rho*U.H/2),'exact_average_floor_negative_control',n)
        states.append(rho);rho=(U*rho*U.H).applyfunc(sp.simplify)
    # Gaussian-integer separation and the explicit rational exclusion constants.
    z=sp.Integer(1)
    for M in range(1,31):
        z=sp.expand(z*(3+4*sp.I));delta=z-5**M
        check(sp.re(delta)**2+sp.im(delta)**2>=1,'exact_fixed_angle_separation',M)
        bound=sp.Rational(1,49*M*(25*M)**M)
        check(0<bound<sp.Rational(1,2*M),'exact_rational_spectral_margin',M)
    DETAILS['spectral_exclusion']={str(M):str(sp.Rational(1,49*M*(25*M)**M)) for M in (2,3,4,8)}

def floating_spectral():
    rng=np.random.default_rng(68016);max_ratio=0.
    for M in range(2,11):
        shift=np.roll(np.eye(M),1,axis=1)
        for noise in (1e-8,1e-5,.001,.02,.2):
            random=rng.dirichlet(np.ones(M),size=M)
            Q=(1-noise)*shift+noise*random
            for z in np.linalg.eigvals(Q):
                alpha=min(1.,abs(z));eps=1-alpha
                if abs(z)<1e-10 or abs(z.imag)<1e-10:continue
                if eps<=1/(2*M):
                    distance=min(abs(1-np.exp(1j*k*np.angle(z))) for k in range(1,M+1))
                    bound=(4*math.sqrt(2*M**(M+1))+M)*math.sqrt(max(0.,eps))
                    check(distance<=bound+1e-9,'float_near_peripheral_cycle_bound',(M,noise))
                    if bound:max_ratio=max(max_ratio,distance/bound)
    DETAILS['float_maximum_cycle_ratio']=max_ratio

if __name__=='__main__':
    exact_realization();exact_boundaries();floating_spectral()
    print(json.dumps({'schema':'theta.r68.finite-diagnostics.v1','status':'PASS',
        'checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),'details':DETAILS,
        'numpy':np.__version__,'sympy':sp.__version__,
        'limits':'Finite rational operator identities and separate floating spectral probes. Not continuum proof, formal proof, expert approval, priority certification or journal acceptance.'},sort_keys=True,indent=2))
