#!/usr/bin/env python3
"""Finite R70 diagnostics. Exact rational/algebraic identities and numerical probes
are separate. No sampled statement is used as a continuum proof certificate.
"""
from __future__ import annotations
import itertools,json,math
import numpy as np
import scipy
import sympy as sp
R=sp.Rational
COUNTS={};DETAILS={}
def check(ok,group,detail):
    if not bool(ok):raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def equal(A,B):
    if hasattr(A,'shape'):return (A-B).applyfunc(sp.simplify)==sp.zeros(*A.shape)
    return sp.simplify(A-B)==0

def square(alpha):
    # Rational regular-square realization, not a minimality claim.
    c,s=R(3,5),R(4,5);h=(1-alpha*(c+s))/4
    row=[h+alpha*c,h+alpha*s,h,h]
    return sp.Matrix(4,4,lambda i,j:row[(j-i)%4])

def circulant3(alpha):
    c,s=R(3,5),R(4,5)
    row=[(1+2*alpha*c)/3,(1-alpha*c+sp.sqrt(3)*alpha*s)/3,
         (1-alpha*c-sp.sqrt(3)*alpha*s)/3]
    return sp.Matrix(3,3,lambda i,j:row[(j-i)%3])

def killed(Q,lam):
    n=Q.rows;P=sp.zeros(n+1);P[:n,:n]=lam*Q
    for j in range(n):P[j,n]=1-lam
    P[n,n]=1
    return P

def rational_cosines(n):
    a,b=sp.Integer(1),sp.Integer(0);out=[]
    for _ in range(n):out.append((a,b));a,b=(3*a-4*b)/5,(4*a+3*b)/5
    return out

def exact_realization():
    vertices=sp.Matrix([[1,0],[0,1],[-1,0],[0,-1]])
    cosines=rational_cosines(12)
    for alpha,lam,gamma,(cp,ss) in itertools.product(
            (R(1,5),R(1,2)),(R(1,4),R(1,2),R(4,5)),
            (R(1),R(2,3)),((R(1),R(0)),(R(3,5),R(4,5)),(R(-1),R(0)))):
        Q=square(alpha);K=killed(Q,lam)
        d=sp.Matrix([(1+gamma*(cp*x-ss*y))/2 for x,y in vertices.tolist()]+[0])
        check(K*sp.ones(5,1)==sp.ones(5,1) and min(K)>=0,'exact_cemetery_rows',(alpha,lam))
        check(min(d)>=0 and max(d)<=1,'exact_bounded_decoder',(gamma,cp,ss))
        row=sp.Matrix([[1,0,0,0,0]])
        for n,(cn,sn) in enumerate(cosines):
            target=lam**n*(1+gamma*alpha**n*(cp*cn-ss*sn))/2
            check((row*d)[0]==target,'exact_killed_response',(alpha,lam,gamma,n))
            row=row*K
    V=sp.Matrix([[1,1,0],[1,-R(1,2),sp.sqrt(3)/2],[1,-R(1,2),-sp.sqrt(3)/2]])
    alpha=R(1,2);Q=circulant3(alpha)
    T=sp.Matrix([[1,0,0],[0,alpha*R(3,5),alpha*R(4,5)],[0,-alpha*R(4,5),alpha*R(3,5)]])
    check(equal(Q*V,V*T),'exact_minimal_four_intertwining','nonreal three-state block')
    check(min(Q)>=0,'exact_minimal_four_intertwining','three-state feasibility')
    for lam in (R(1,10),R(1,2),R(9,10)):
        K=killed(Q,lam);d=sp.Matrix([1,R(1,4),R(1,4),0])
        check(equal(K[:3,:3],lam*Q) and K[3,3]==1 and d[3]==0,
              'exact_minimal_four_construction',lam)
    # Relative spectral normalization has no global positive Perron vector here.
    h1,h2=sp.symbols('h1 h2',positive=True)
    S=sp.Matrix([[R(1,2),R(1,4)],[0,R(1,4)]])
    check((S*sp.Matrix([h1,h2])-sp.Matrix([h1,h2])/2)[0]==h2/4,
          'exact_reducible_scaling_negative','strictly positive residual')
    # A recurrent output-inactive state is retained, not counted as physical halt.
    S=sp.Matrix([[R(1,3),R(1,4)],[0,R(1,2)]]);K=killed(S,1)
    K[0,2]=1-sum(S.row(0));K[1,2]=1-sum(S.row(1))
    check(K*sp.ones(3,1)==sp.ones(3,1),'exact_transient_core','completion')
    check(max(S.eigenvals())<1 and 1 in K.eigenvals(),'exact_transient_core','different spectra')
    d=sp.Matrix([R(2,3),R(1,4),0])
    for n in range(8):
        check((K**n*d)[0]==(S**n*d[:2,0])[0],'exact_transient_core','active response')
    # Degeneracies need their own counts; verify explicit realizing matrices.
    for initial in (R(0),R(1,4),R(1,2),R(1)):
        lam=R(2,3);K=sp.Matrix([[0,1,0],[0,lam,1-lam],[0,0,1]])
        d=sp.Matrix([initial,lam/2,0])
        for n in range(7):
            check((K**n*d)[0]==(initial if n==0 else lam**n/2),'exact_degenerate_prefix',(initial,n))
    values=[R(1,2)**n*(1+cn)/2 for n,(cn,_) in enumerate(rational_cosines(10))]
    scalar=sp.Matrix([[values[i+j] for j in range(4)] for i in range(4)])
    full=sp.Matrix([[1]+[values[i+j] for j in range(3)] for i in range(4)])
    check(scalar.rank()==3 and full.det()!=0,'exact_rank_four_not_memory','leaking irrational phase')

def raw_channel(X,lam,alpha):
    U=sp.Matrix([[2,-1],[1,2]])/sp.sqrt(5);A=X[:2,:2]
    F=alpha*U*A*U.T+(1-alpha)*sp.trace(A)*sp.eye(2)/2
    out=sp.zeros(3);out[:2,:2]=lam*F
    out[2,2]=X[2,2]+(1-lam)*sp.trace(A)
    return out

def exact_physical():
    U=sp.Matrix([[2,-1],[1,2]])/sp.sqrt(5)
    for lam,alpha in itertools.product((R(1,4),R(1,2),R(3,4)),(R(0),R(1,2),R(1))):
        Ks=[];A=sp.zeros(3);A[:2,:2]=sp.sqrt(lam*alpha)*U;Ks.append(A)
        for i,j in itertools.product(range(2),repeat=2):
            K=sp.zeros(3);K[i,j]=sp.sqrt(lam*(1-alpha)/2);Ks.append(K)
        for i in range(2):
            K=sp.zeros(3);K[2,i]=sp.sqrt(1-lam);Ks.append(K)
        K=sp.zeros(3);K[2,2]=1;Ks.append(K)
        check(equal(sum((K.T*K for K in Ks),sp.zeros(3)),sp.eye(3)),
              'exact_raw_kraus_normalization',(lam,alpha))
        for i,j in itertools.product(range(3),repeat=2):
            X=sp.zeros(3);X[i,j]=1
            actual=sum((K*X*K.T for K in Ks),sp.zeros(3))
            check(equal(actual,raw_channel(X,lam,alpha)), 'exact_raw_channel_identity',(lam,alpha,i,j))
        rho=sp.diag(1,0,0)
        for n,(cn,_) in enumerate(rational_cosines(12)):
            check(equal(rho[0,0],lam**n*(1+alpha**n*cn)/2),
                  'exact_qutrit_born',(lam,alpha,n))
            check(equal(sp.trace(rho),1) and rho[2,2]==1-lam**n,
                  'exact_qutrit_population',(lam,alpha,n))
            rho=raw_channel(rho,lam,alpha).applyfunc(sp.simplify)
    # Independently form actual three-outcome squared-audit effects on six dimensions.
    I=sp.eye(6);alive=sp.diag(1,0);E=sp.diag(1,0,0);F=2*E-sp.eye(3)
    h=R(3,2);eps=R(1,4)
    for sigma in (-1,1):
        v=I-sigma*eps*sp.kronecker_product(alive,F)
        m=-sigma*eps*sp.kronecker_product(alive,sp.eye(3))/2
        Bp=(v+h*m)/(2*h*h);Bm=(v-h*m)/(2*h*h);B0=I-v/(h*h)
        check(Bp+Bm+B0==I and min(Bp.diagonal())>=0 and min(Bm.diagonal())>=0 and min(B0.diagonal())>=0,
              'exact_six_dimensional_povm',sigma)
        for r in (-1,1):
            loss=(h-r)**2*Bp+(-h-r)**2*Bm+r*r*B0
            check(loss==2*I+sigma*eps*sp.kronecker_product(alive,r*sp.eye(3)-F),
                  'exact_squared_loss_moments',(sigma,r))
        rho=sp.diag(1,0,0)
        for n in range(9):
            for t,b in itertools.product((R(0),R(1,4),R(1,2)),(R(0),R(1,3),R(1))):
                state=sp.kronecker_product(sp.diag(t**n,1-t**n),rho)
                lossplus=(h-1)**2*Bp+(-h-1)**2*Bm+B0
                lossminus=(h+1)**2*Bp+(-h+1)**2*Bm+B0
                actual=sp.trace((b*lossplus+(1-b)*lossminus)*state)
                check(actual==2+2*sigma*eps*t**n*(b-rho[0,0]),
                      'exact_physical_decision_identity',(sigma,n,t,b))
            rho=raw_channel(rho,R(1,2),R(1)).applyfunc(sp.simplify)

def exact_finite_tests():
    z=sp.symbols('z');lam=R(1,2);c=R(3,5)
    U=sp.cancel(1/(2*(1-lam*z))+(1-lam*c*z)/(2*(1-2*lam*c*z+lam**2*z*z)))
    P,D=sp.fraction(U)
    check(sp.degree(P,z)<=2 and sp.degree(D,z)==3,'exact_target_order','three scalar modes')
    for M in range(1,6):
        Q=sp.zeros(M)
        for i in range(M-1):Q[i,i]=R(i+1,M+1);Q[i,i+1]=1-Q[i,i]
        Q[M-1,M-1]=1;d=sp.Matrix([R(i+1,M+2) for i in range(M)])
        B=sp.cancel(((sp.eye(M)-z*Q).inv()*d)[0]);PB,DB=sp.fraction(B)
        cross=sp.Poly(sp.expand(PB*D-P*DB),z)
        check(cross.degree()<=M+2,'exact_resolvent_degree',M)
        nodes=[R(j,4*(M+2)) for j in range(M+3)]
        vals=[sp.cancel(B.subs(z,x)-U.subs(z,x)) for x in nodes]
        check(any(v!=0 for v in vals),'exact_finite_model_detection',M)
        # Recover the entire cross-polynomial from its degree-bounded node values.
        interp=sp.interpolate([(x,cross.eval(x)) for x in nodes],z)
        check(sp.expand(interp-cross.as_expr())==0,'exact_interpolation_identity',M)
    # Exact one-label optimum on the four-model-pair witness, not local optimization.
    nodes=[R(j,12) for j in range(4)]
    lines=[]
    for x in nodes:
        a=1/(1-x);b=-U.subs(z,x)
        lines.extend([(a,b),(-a,-b)])
    candidates={R(0),R(1)}
    for (a,b),(aa,bb) in itertools.combinations(lines,2):
        if a!=aa:
            v=sp.cancel((bb-b)/(a-aa))
            if 0<=v<=1:candidates.add(v)
    radius,decoder=min((max(a*v+b for a,b in lines),v) for v in candidates)
    check(radius>0 and 0<=decoder<=1,'exact_one_label_minimax','finite convex piecewise-linear optimum')
    DETAILS['finite_one_label_witness']={'decoder':str(decoder),'risk_gap':str(radius/4),'radius':str(radius),'physical_models':8}
    # Without the dimension bound, a different legal full-history response can fit all nodes.
    H=sp.Poly(sp.prod(z-x for x in nodes),z)
    coefs=[H.nth(n) for n in range(H.degree()+1)]
    us=[lam**n*(1+cn)/2 for n,(cn,_) in enumerate(rational_cosines(len(coefs)))]
    margins=[min(us[n],1-us[n])/abs(a) for n,a in enumerate(coefs) if a!=0]
    eta=min(margins)/2
    modified=[u+eta*a for u,a in zip(us,coefs)]
    check(eta>0 and all(0<=v<=1 for v in modified) and modified!=us,
          'exact_finite_tests_need_dimension_bound','legal different coefficient list')
    check(all(H.eval(x)==0 for x in nodes),'exact_finite_tests_need_dimension_bound','all test responses agree')
    DETAILS['rational_target_generating_function']=str(U)

def exact_background():
    lam=R(1,2);alpha=R(1);Q=circulant3(lam*alpha)
    vertices=sp.Matrix([[1,0],[-R(1,2),sp.sqrt(3)/2],[-R(1,2),-sp.sqrt(3)/2]])
    table=[]
    for eta in (R(1,2),R(1,8),R(1,64)):
        T=1
        while (1-eta)*lam**T>eta/2:T+=1
        a=(1-eta)*lam**T/2;cp,ss=rational_cosines(T+1)[T]
        G=sp.Matrix([eta/2+2*a*(cp*x-ss*y) for x,y in vertices.tolist()])
        F=sp.Matrix([eta/2+2*a,eta/2])
        suffix=sp.diag(sp.Matrix([[lam,1-lam],[0,1]]),Q)
        K=sp.zeros(T+5)
        for i in range(T-1):K[i,i+1]=1
        K[T-1,T]=R(1,2);K[T-1,T+2]=R(1,2);K[T:,T:]=suffix
        prefix=[eta/2+(1-eta)*lam**n*(1+cn)/2 for n,(cn,_) in enumerate(rational_cosines(T))]
        d=sp.Matrix(prefix+list(F)+list(G))
        check(equal(K*sp.ones(K.rows,1),sp.ones(K.rows,1)) and min(K)>=0,
              'exact_background_stochastic',(eta,T))
        check(all(sp.simplify(x)>=0 and sp.simplify(1-x)>=0 for x in d),
              'exact_background_bounded_decoder',eta)
        row=sp.zeros(1,T+5);row[0]=1
        for n,(cn,_) in enumerate(rational_cosines(T+8)):
            target=eta/2+(1-eta)*lam**n*(1+cn)/2
            check(equal((row*d)[0],target),'exact_background_complete_response',(eta,n))
            row=(row*K).applyfunc(sp.simplify)
        check(K.rows==T+2+3,'exact_background_anchor_count','no free start mixture')
        table.append({'eta':str(eta),'prefix':T,'labels':K.rows})
    DETAILS['exact_background_controllers']=table

def numeric_channel():
    rng=np.random.default_rng(701016)
    U=np.array([[2.,-1.],[1.,2.]])/math.sqrt(5)
    def channel(X,lam,alpha):
        A=X[:2,:2];out=np.zeros((3,3),dtype=complex)
        out[:2,:2]=lam*(alpha*U@A@U.T+(1-alpha)*np.trace(A)*np.eye(2)/2)
        out[2,2]=X[2,2]+(1-lam)*np.trace(A);return out
    def tn(A):return float(np.sum(np.abs(np.linalg.eigvalsh((A+A.conj().T)/2))))
    maximum=0.
    for lam,alpha in itertools.product((.01,.3,.7,.97),(0.,.4,1.)):
        for j in range(16):
            A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));rho=A@A.conj().T;rho/=np.trace(rho)
            A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));sigma=A@A.conj().T;sigma/=np.trace(sigma)
            a=channel(rho,lam,alpha);b=channel(sigma,lam,alpha)
            check(tn(a-b)<=lam*tn(rho-sigma)+1e-11,'float_trace_contraction',(lam,alpha,j))
            check(abs(np.trace(a)-1)<1e-12 and np.linalg.eigvalsh(a).min()>-1e-12,
                  'float_qutrit_output_states',(lam,alpha,j))
        rho=np.diag([1.,0.,0.]);omega=np.diag([0.,0.,1.])
        angle=math.atan2(4,3)
        for n in range(40):
            target=lam**n*(1+alpha**n*math.cos(n*angle))/2
            err=abs(rho[0,0]-target);maximum=max(maximum,float(err))
            check(err<1e-11 and tn(rho-omega)<=2*lam**n+1e-11,
                  'float_mixing_and_response',(lam,alpha,n))
            rho=channel(rho,lam,alpha)
    DETAILS['maximum_raw_born_error']=maximum
    DETAILS['seed']=701016

if __name__=='__main__':
    exact_realization();exact_physical();exact_finite_tests();exact_background();numeric_channel()
    print(json.dumps({'schema':'theta.r70.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,
        'total_checks':sum(COUNTS.values()),'details':DETAILS,'numpy':np.__version__,
        'scipy':scipy.__version__,'sympy':sp.__version__,
        'limits':'Finite exact identities and floating probes, not proofs by sampling, a general-size executed elimination, independent expert review, priority certification or editorial acceptance.'},sort_keys=True,indent=2))
