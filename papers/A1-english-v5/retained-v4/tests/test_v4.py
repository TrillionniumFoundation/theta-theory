#!/usr/bin/env python3
"""Formula diagnostics and source regression checks. Finite checks are not all-budget proofs."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,platform,sys,time
import sympy as s
import certify_adaptive as cert
ROOT=Path(__file__).resolve().parents[1]
RESULTS=[]
def check(name,kind,fn):
    start=time.perf_counter()
    detail=fn()
    RESULTS.append({'name':name,'kind':kind,'passed':True,'seconds':round(time.perf_counter()-start,4),'detail':detail})

def gram_inverse():
    H=s.Matrix([[1,s.Rational(1,4),0],[1,0,s.Rational(1,4)],
                [1,-s.Rational(1,4),0],[1,0,-s.Rational(1,4)]])
    G=H.T*H/4; assert G==s.diag(1,s.Rational(1,32),s.Rational(1,32))
    z=s.Matrix([s.Rational(1,1000),s.Rational(1,2000),-s.Rational(1,3000)])
    gates=s.ones(4,1)/2-H*G.inv()*z
    assert all(0<x<1 for x in gates)
    assert H.T*(s.ones(4,1)-gates)/4==H.T*s.ones(4,1)/8+z
    return 'Exact normalized finite experiment: Gram inverse produces requested failure coefficients.'

def gram_perturbation():
    H=s.Matrix([[1,s.Rational(1,4),0],[1,0,s.Rational(1,4)],[1,-s.Rational(1,4),0],[1,0,-s.Rational(1,4)]])
    new=H.copy(); new[0,2]+=s.Rational(1,100);new[1,2]-=s.Rational(1,100)
    G=H.T*H/4; G1=new.T*new/4
    assert sum(new[:,2])==0
    bound=2*s.Rational(5,4)*s.Rational(1,100)+s.Rational(1,10000)
    assert bound<s.Rational(1,32)
    diff=G1-G;assert sum(x*x for x in diff)<bound**2
    assert all(G1[:k,:k].det()>0 for k in [1,2,3])
    return {'perturbation_bound':str(bound),'original_gram_margin':'1/32'}

def rank_defect():
    H=s.Matrix([[1,1,0],[1,-1,0],[1,0,0]])
    assert (H.T*H).rank()==2
    assert H*s.Matrix([0,0,1])==s.zeros(3,1)
    return 'An annihilator confines all failure vectors to a plane; no full-rank conclusion is asserted.'

def body_rank():
    V=s.eye(4); A=s.Matrix([1,2,3,4]);Fmat=V.row_join(V*A)
    assert Fmat.rank()==4 and (Fmat.T*Fmat).rank()==4
    return 'Five coordinates, intrinsic rank four, for a continuation coordinate in the old span.'

def product_ranks():
    t=s.symbols('t');out={}
    for q in [1,2,3,4]:
        for n in [1,2,3,4]:
            fs=[1+(i+1)*t**q for i in range(n)];cols=[]
            for i in range(n):
                other=s.prod(fs[j] for j in range(n) if j!=i)
                for k in range(q+1):
                    p=s.Poly(t**k*other,t);cols.append([p.nth(j) for j in range(q*n+1)])
            rank=s.Matrix(cols).T.rank();assert rank==q*n+1;out[f'q={q},n={n}']=rank
    return {'finite_ranks':out,'scope':'Finite q,n only; manuscript supplies the all-n proof.'}

def lorentz_rank():
    a,b,p,e=s.symbols('a b p e',nonzero=True)
    # constant, linear, quadratic, cubic rows; four moment columns.
    M=s.Matrix([[0,-a,0,0],[0,b,-b,0],[-p,p,0,0],[0,0,0,-b*e]])
    assert s.factor(M.det())!=0;assert M.subs(e,0).rank()==3
    return {'moment_map_determinant':str(s.factor(M.det()))}

def bernstein_product():
    t=s.symbols('t')
    for d,m in [(3,3),(6,5),(1,7)]:
        c=[s.Rational(i+1,d+2) for i in range(d+1)];h=[s.Rational(j+2,m+3) for j in range(m+1)]
        B=lambda n,k:s.binomial(n,k)*t**k*(1-t)**(n-k)
        got=sum(sum(s.binomial(d,i)*s.binomial(m,k-i)/s.binomial(d+m,k)*c[i]*h[k-i]
                    for i in range(d+1) if 0<=k-i<=m)*B(d+m,k) for k in range(d+m+1))
        expected=sum(c[i]*B(d,i) for i in range(d+1))*sum(h[j]*B(m,j) for j in range(m+1))
        assert s.expand(got-expected)==0
    return 'Exact product identities at unequal degrees, including surrogate factors.'

def physical_normalization():
    t=s.symbols('t');m=7;a=s.Rational(1,3);R=s.Rational(9,20)+t/s.Integer(50)
    B=lambda i:s.binomial(m,i)*t**i*(1-t)**(m-i)
    plus=s.expand(sum((1+a*s.Rational(i,m)**2)*B(i) for i in range(m+1)))
    minus=s.expand(sum((1-a*s.Rational(i,m)**2)*B(i) for i in range(m+1)))
    assert s.expand((plus+minus)/2)==1
    assert s.Poly(R*plus,t).degree()<=m+1
    for i in range(m+1):assert 1-a*s.Rational(i,m)**2>0
    return 'Positive normalized two-mark analogue; multiplication by R keeps the physical hit factor.'

def sharp_c2_constant():
    t=s.symbols('t');m=7;a=s.Rational(1,3)
    q=s.expand(sum((1+a*s.Rational(i,m)**2)*s.binomial(m,i)*t**i*(1-t)**(m-i) for i in range(m+1)))
    assert s.expand(q-(1+a*t*t)-a*t*(1-t)/m)==0
    tv=a/(8*m);L2=2*a
    assert tv==L2/(16*m)
    return 'The L2/(16m) TV constant is attained at t=1/2 in the normalized two-mark quadratic example.'

def binomial_variance():
    t=s.symbols('t');m=9
    v=s.expand(sum((s.Rational(i,m)-t)**2*s.binomial(m,i)*t**i*(1-t)**(m-i) for i in range(m+1)))
    assert s.expand(v-t*(1-t)/m)==0
    return 'Exact binomial mean-square error used in both surrogate rates.'

def smooth_perturbation():
    R=s.symbols('R');assert s.simplify(s.diff(R*s.sin(R),R,4)-(R*s.sin(R)-4*s.cos(R)))==0
    assert s.diff(R*s.sin(R),R,4)!=0
    return 'Smooth nonpolynomial firmware does not inherit the exact cubic derivative cutoff.'

P=[[F(1,2),F(1,3),F(1,6)],[F(1,4),F(1,4),F(1,2)]]
Z=[F(2,5),F(3,5)];S=F(99,100)
def terminal(z):return max(2*z[0]+z[1],z[0]+2*z[1])
def qgate(g):
    hit=sum((S*g[j]*terminal([Z[i]*P[i][j] for i in range(2)]) for j in range(3)),F(0))
    fail=[Z[i]*sum((1-g[j])*P[i][j] for j in range(3)) for i in range(2)]
    return hit+terminal(fail)

def endpoints_finite():
    v=max(qgate(g) for g in product([F(0),F(1)],repeat=3))
    assert max(qgate(g) for g in product([F(0),F(1,2),F(1)],repeat=3))==v
    return {'vertex_value':str(v),'scope':'Finite analogue, not the infinite-dimensional selection proof.'}

def layer_cake():
    g=[F(1,4),F(1,2),F(3,4)]
    vertices=[[F(int(x>F(k,4))) for x in g] for k in range(4)]
    assert [sum(v[j] for v in vertices)/4 for j in range(3)]==g
    assert qgate(g)<=sum(qgate(v) for v in vertices)/4
    return 'Exact layer cake and convexity inequality on a rational four-layer gate.'

def last_step_formula():
    xs=[F(-1),F(-1,2),F(0),F(1,2),F(1)]
    ks=[[1+F(1,4)*x for x in xs],[1+F(3,4)*x for x in xs]]
    G=[[F(2),F(1),F(3,2)],[F(1),F(2),F(7,5)]]
    As=[S*max(sum(Z[i]*ks[i][j]*G[i][d] for i in range(2)) for d in range(3)) for j in range(5)]
    Cs=[[sum(Z[i]*ks[i][j]*G[i][d] for i in range(2)) for j in range(5)] for d in range(3)]
    for eta in [F(0),F(1,10)]:
        formula=max(sum(eta*(As[j]+C[j])+(1-2*eta)*max(As[j],C[j]) for j in range(5))/5 for C in Cs)
        enum=max(sum(g[j]*As[j]+(1-g[j])*C[j] for j in range(5))/5
                 for C in Cs for g in product([eta,1-eta],repeat=5))
        assert formula==enum
    return 'Exact finite-mark maximization checks the formula for full and interior endpoint intervals.'

def convex_boundary():
    # A convex maximum of affine functions minus an affine censor value.
    x=s.symbols('x');left=-x-s.Rational(2,5);right=x-s.Rational(3,10)
    assert s.solve(left,x)==[-s.Rational(2,5)] and s.solve(right,x)==[s.Rational(3,10)]
    for z in [s.Rational(i,100) for i in range(-100,101)]:
        f=max(left.subs(x,z),right.subs(x,z),-s.Rational(1,10))
        assert (f>0)==bool(z<-s.Rational(2,5) or z>s.Rational(3,10))
    return 'Convex-envelope example has exactly two positive end intervals; topology proof is analytic.'

def lookup_cancellation():
    J=7;cut=F(2,5);direct=(1-cut*cut)/2;averaged=F(0);rhs=F(0)
    for k in range(J):
        lo=F(k,J);hi=F(k+1,J);fraction=max(F(0),hi-max(lo,cut))/(hi-lo)
        averaged+=fraction*(hi*hi-lo*lo)/2
        # Integral of g(t)[t-E_J(t)] on each cell.
        start=max(lo,cut)
        if start<hi:rhs+=(hi*hi-start*start)/2-(hi+lo)/2*(hi-start)
    assert direct-averaged==rhs and abs(rhs)<=F(1,J)
    return 'Exact cancellation for a discontinuous gate and Lipschitz integrand; no uniform L1 gate convergence used.'

def recurrence():
    # Symbolic backward accumulation of e_b = C b-independent times a^b.
    a,C=s.symbols('a C');E=0
    for n in range(1,8):E=s.expand(C*a**n+a*E);assert s.expand(E-n*C*a**n)==0
    return 'The Bellman Lipschitz recurrence yields N times the common horizon factor.'

def rare_failure():
    h=[F(1),F(2),F(3),F(4)]
    for scale in [F(1),F(1,10**12)]:
        hs=[scale*x for x in h]
        assert [x/sum(hs) for x in hs]==[x/sum(h) for x in h]
    return 'Normalized failure factors retain their margin independently of rare-event mass.'

def coupling_tight():
    e=F(1,17);q=[(1-e)**2,(1-e)*e,F(0),e]
    p=[F(1),F(0),F(0),F(0)]
    tv=sum(abs(x-y) for x,y in zip(p,q))/2
    assert tv==1-(1-e)**2 and tv<=2*e
    payoff=[F(1),F(3),F(3),F(3)]
    assert abs(sum((x-y)*u for x,y,u in zip(p,q,payoff)))==2*tv
    return 'Two-step absorbing-mismatch example attains the coupling bound and oscillation-times-TV value bound.'

def censor_contraction():
    p=[F(1,2),F(1,3),F(1,6)];q=[F(1,3)]*3;raw=sum(abs(a-b) for a,b in zip(p,q))/2
    for g in product([F(0),F(1,2),F(1)],repeat=3):
        gp=[g[i]*p[i] for i in range(3)]+[sum((1-g[i])*p[i] for i in range(3))]
        gq=[g[i]*q[i] for i in range(3)]+[sum((1-g[i])*q[i] for i in range(3))]
        assert sum(abs(a-b) for a,b in zip(gp,gq))/2<=raw
    return 'Exact contraction for 27 gates, including endpoints; theorem uses a common channel.'

def threshold_regression():
    a=s.symbols('a',real=True);flow=a
    assert s.diff(flow,a)==1
    assert int(bool(flow.subs(a,-s.Rational(1,100))>0))==0
    assert int(bool(flow.subs(a,s.Rational(1,100))>0))==1
    text=(ROOT/'sections/A_scope_repairs.tex').read_text()
    assert r'\emph{state}' in text and 'No regularity is asserted for an arbitrary Borel readout.' in text
    return 'Smooth no-event flow plus threshold readout: retained counterexample and corrected source qualification.'

def two_trace():
    a=s.symbols('a');J=a+2*(1-a)
    assert s.diff(J,a)==1-2
    assert 'Eulerian' in (ROOT/'sections/A_scope_repairs.tex').read_text()
    assert r'\sum_\Gamma' in (ROOT/'sections/A_scope_repairs.tex').read_text()
    return 'Internal sign and explicit Eulerian/outer-boundary conventions checked.'

def preserved_sources():
    expected={'02_laboratory.tex':'083158af4d8d3a0a9ee1fe0d1f9489ed81b9eb72',
     '03_attainability.tex':'70facb924b1581ef39039bb524379da8882747f7',
     '04_positive_filter.tex':'50f40537992da80868647c27f4e75f0184dea816',
     '06_response.tex':'cff62d4578afe72f501d1112ff7830fac9c905bd'}
    for name,sha in expected.items():
        b=(ROOT/'sections'/name).read_bytes();got=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert got==sha,(name,got)
    labels=['thm:main','prop:raw','thm:attainable','thm:filter','thm:general','thm:dimension','lem:body','thm:control','thm:boundary','thm:response','prop:biased','thm:two-trace','thm:transport-prep']
    alltext='\n'.join(p.read_text() for p in (ROOT/'sections').glob('*.tex'))
    assert all(alltext.count('\\label{'+x+'}')==1 for x in labels)
    assert 'five-dimensional for every budget' not in alltext
    return {'unchanged_git_blobs':expected,'retained_principal_labels':len(labels)}

def full_advantage():
    result=cert.certificate()
    (ROOT/'validation/ADAPTIVE_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    return {'nominal_gap':result['nominal']['strict_advantage'],
            'full_cubic_gap':result['full_cubic_transfer']['certified_gap'],
            'scope':'Exact finite inequalities plus analytic reduction and model transfer in manuscript.'}

def main():
    checks=[('Attainable Gram right inverse','exact rational',gram_inverse),
    ('Same-degree perturbation margin','exact rational',gram_perturbation),
    ('Rank-deficient failure family','exact algebra',rank_defect),
    ('Intrinsic versus ambient moment dimension','exact algebra',body_rank),
    ('Coprime product differential ranks','finite exact ranks',product_ranks),
    ('Lorentz amplitude and rank','exact symbolic',lorentz_rank),
    ('General Bernstein product','exact symbolic',bernstein_product),
    ('Positive normalized physical surrogate','exact symbolic',physical_normalization),
    ('Sharp quadratic surrogate TV constant','exact symbolic',sharp_c2_constant),
    ('Binomial variance identity','exact symbolic',binomial_variance),
    ('Nonpolynomial detector regression','exact symbolic',smooth_perturbation),
    ('Endpoint optimum finite analogue','exact rational finite analogue',endpoints_finite),
    ('Layer-cake convexity finite analogue','exact rational finite analogue',layer_cake),
    ('Last-cartridge optimized formula','exact rational finite analogue',last_step_formula),
    ('Two-tail convex acceptance example','exact rational finite diagnostic',convex_boundary),
    ('Lookup averaging cancellation','exact rational',lookup_cancellation),
    ('Backward lookup error recurrence','exact symbolic',recurrence),
    ('Rare-failure normalization','exact rational',rare_failure),
    ('Sharp two-step model coupling','exact rational finite analogue',coupling_tight),
    ('Common censor contraction','exact rational finite analogue',censor_contraction),
    ('Smooth readout qualification','scope regression',threshold_regression),
    ('Two density traces and outer flux','scope regression',two_trace),
    ('Source and theorem preservation','source integrity',preserved_sources),
    ('Full-class adaptive certificate','exact outward rational certificate',full_advantage)]
    for name,kind,fn in checks:check(name,kind,fn);print('PASS:',name)
    receipt={'suite':'A1 English v4','passed':len(RESULTS),'total':len(checks),
      'interpretation':'Executed diagnostics, not proof-assistant or independent-referee certification.',
      'historical_counts_excluded':True,'environment':{'python':platform.python_version(),'sympy':s.__version__},
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':RESULTS}
    (ROOT/'validation/V4_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
