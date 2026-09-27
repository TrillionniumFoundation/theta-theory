"""Finite exact regression for v58; not a proof of universal claims or gap."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sympy as s
import qubit_compiler as qc

COUNT=0
NEG=[]
def check(ok,message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)
def negative(name,predicate):
    check(not predicate,'negative control escaped: '+name);NEG.append(name)
def exception(name,fn):
    try:fn()
    except (ValueError,RuntimeError):NEG.append(name);check(True,name);return
    raise RuntimeError('invalid input accepted: '+name)
def qmul(a,b):
    t,x,y,z=a;u,v,w,r=b
    return (t*u-x*v-y*w-z*r,t*v+x*u+y*r-z*w,t*w-x*r+y*u+z*v,t*r+x*w-y*v+z*u)
def conj(a):return (a[0],-a[1],-a[2],-a[3])
def qnorm(a):return sum(x*x for x in a)
def matmul(a,b,p=5):return tuple(tuple(sum(a[i][t]*b[t][j] for t in range(2))%p for j in range(2)) for i in range(2))
def imatrix(q):
    t,x,y,z=q
    return (( (t+2*x)%5,(y+2*z)%5),((-y+2*z)%5,(t+3*x)%5))
def bloch(q,n):
    v=qmul(qmul(q,(0,0,0,1)),conj(q));den=25**n
    check(v[0]==0,'conjugate pure quaternion')
    return (F(v[3],den),F(v[2],den),F(v[1],den))
def output(data,word,rounded=False):
    prob=[F(0)]*data['labels'];prob[data['initial_label']]=1
    for a in word:
        new=[F(0)]*len(prob)
        for i,p in enumerate(prob):
            if p:
                for j,t in data['rows'][a][i]:new[j]+=p*t
        prob=new
    return tuple(sum((p*z[d] for p,z in zip(prob,data['decoder_bloch'])),F(0)) for d in range(3))
def tv(row,other):
    a=dict(row);b=dict(other)
    return sum((abs(a.get(i,F(0))-b.get(i,F(0))) for i in a.keys()|b.keys()),F(0))/2

def main():
    # Exact complex input, unitary and Bloch-convention identities.
    ii=s.I
    U=s.Matrix([[-3+4*ii,0],[0,-3-4*ii]])/5
    V=s.Matrix([[-3,4],[-4,-3]])/5
    P=s.ones(2)/2
    sx=s.Matrix([[0,1],[1,0]]);sy=s.Matrix([[0,-ii],[ii,0]]);sz=s.diag(1,-1)
    sigmas=[sx,sy,sz]
    for name,a in [('U',U),('V',V)]:
        check(s.simplify(a*a.conjugate().T)==s.eye(2) and s.simplify(a.det())==1,'SU2 input')
        for j in range(3):
            for i in range(3):
                entry=s.simplify(s.trace(sigmas[i]*a*sigmas[j]*a.conjugate().T)/2)
                check(entry==s.Rational(qc.COMMANDS[name][i][j].numerator,qc.COMMANDS[name][i][j].denominator),'Bloch rotation convention')
    check(P*P==P and s.trace(P)==1,'pure rational seed')
    negative('commuting-generators-substitution',U*V==V*U)
    # All six finite-field matrices and their exact zero-product relation.
    gen=[(1,2,0,0),(1,-2,0,0),(1,0,2,0),(1,0,-2,0),(1,0,0,2),(1,0,0,-2)]
    matrices=[imatrix(q) for q in gen]
    check(len(set(matrices))==6,'six distinct residues')
    for i,a in enumerate(matrices):
        check(s.Matrix(a).det()%5==0 and a!=((0,0),(0,0)),'rank one residue')
        for j,b in enumerate(matrices):
            check((matmul(a,b)==((0,0),(0,0)))==(j==(i^1)),'inverse-pair zero product')
    negative('allow-adjacent-cancellation',matmul(matrices[0],matrices[1])!=((0,0),(0,0)))
    negative('reduce-modulo-two-instead-of-five',len({tuple(x%2 for x in q) for q in gen})==6)
    layer=[((1,0,0,0),-1)]
    for n in range(1,6):
        layer=[(qmul(g,q),i) for q,last in layer for i,g in enumerate(gen) if last<0 or i!=(last^1)]
        check(len(layer)==6*5**(n-1),'free triple finite enumeration')
        for q,last in layer:
            check(qnorm(q)==5**n,'norm numerator')
            check(imatrix(q)!=((0,0),(0,0)),'reduced word nonzero residue')
            check(any(q[i] for i in [1,2,3]),'finite scalar exclusion')
    # All reduced two-generator orbits through radius seven; full group proof is in prose.
    ab=[(-3,4,0,0),(-3,-4,0,0),(-3,0,4,0),(-3,0,-4,0)]
    seen={qc.E1};profile=[1];layer=[((1,0,0,0),-1)]
    for n in range(1,8):
        layer=[(qmul(g,q),i) for q,last in layer for i,g in enumerate(ab) if last<0 or i!=(last^1)]
        for q,last in layer:
            x=bloch(q,n)
            check(qc.dot(x,x)==1,'pure reachable point')
            check(all((z*25**n).denominator==1 for z in x),'rational denominator lattice')
            check(x not in seen,'orbit stabilizer collision')
            seen.add(x)
        check(len(seen)==2*3**n-1,'exact finite orbit profile')
        profile.append(len(seen))
    z=(F(0),F(0),F(1))
    negative('axis-seed-has-trivial-stabilizer',qc.apply(qc.U,z)!=z)
    negative('remove-identity-but-count-ball',len(layer)==profile[-1])
    # Rank witnesses: the all-direction exponent need not be the generic orbit dimension.
    for d in range(2,7):
        pstar=2*(d-1)
        check(d*d-((d-1)**2+1)==pstar,'rank-one multiplicity formula')
        for m in range(1,d):check(2*m*(d-m)>=pstar,'Grassmannian minimum rank')
    negative('use-regular-orbit-exponent-for-all-centroids',4*4-(3*3+1)>=4*4-4)
    negative('permit-trivial-summand-with-positive-minimum-rank',s.zeros(3,1).rank()>=1)
    # Rational nets, exact row certificates, and all 25 words at horizon two.
    for m in range(2,8):
        verts=qc.net(m)
        check(len(verts)<=13*m*m and verts[0]==qc.ZERO and qc.E1 in verts,'net size and seed')
        for v in verts[1:]:check(qc.dot(v,v)==1,'rational unit vertex')
    data=qc.compile_exact(2,F(1,2),max_labels=100)
    for a,rows in data['rows'].items():
        for v,row in zip(data['vertices'],rows):
            check(qc.valid_row(data['vertices'],row,qc.scale(data['contraction'],qc.apply(qc.COMMANDS[a],v))),'certified common row')
    check(data['max_row_support']<=4,'sparse row support')
    for word in product(qc.COMMANDS,repeat=2):
        x=qc.E1
        for a in word:x=qc.apply(qc.COMMANDS[a],x)
        check(output(data,word)==qc.scale(F(1,2),x),'exact wordwise realization')
    row=data['rows']['U'][data['initial_label']];target=qc.scale(data['contraction'],qc.apply(qc.U,qc.E1))
    negative('negative-row-mass',qc.valid_row(data['vertices'],[(0,F(-1)),(1,F(2))],target))
    negative('row-mass-not-one',qc.valid_row(data['vertices'],[(0,F(1,2))],target))
    negative('identity-row-for-nonidentity-command',qc.valid_row(data['vertices'],[(data['initial_label'],F(1))],target))
    negative('row-target-without-contraction',qc.valid_row(data['vertices'],row,qc.apply(qc.U,qc.E1)))
    negative('wrong-contraction-rescaling',output(data,('U','V'))==qc.scale(F(1,2)*data['contraction'],qc.apply(qc.V,qc.apply(qc.U,qc.E1))))
    negative('reverse-noncommuting-word',output(data,('U','V'))==output(data,('V','U')))
    negative('overscaled-decoder-legal',qc.dot(qc.scale(F(2),qc.E1),qc.scale(F(2),qc.E1))<=1)
    for b in range(2,9):
        for rows in data['rows'].values():
            for row in rows:
                rounded=qc.dyadic(row,b)
                check(sum(p for _,p in rounded)==1 and all(p>=0 for _,p in rounded),'dyadic stochasticity')
                check(set(i for i,_ in rounded)<=set(i for i,_ in row),'no support expansion')
                check(tv(row,rounded)<=3*F(1,2**b),'sparse rounding budget')
    noisy=qc.compile_noisy(2,F(1,2),max_labels=100)
    for word in product(qc.COMMANDS,repeat=2):
        x=qc.E1
        for a in word:x=qc.apply(qc.COMMANDS[a],x)
        y=output(noisy,word);dif=tuple(a-b for a,b in zip(x,y))
        check(qc.dot(dif,dif)/2<=F(1,4),'rounded full density output error')
    negative('claim-quantum-sampling',noisy.get('quantum_output_sampled',False))
    negative('claim-gap-from-tests',data['spectral_gap_certified'])
    exception('unit-amplitude-exact-compiler',lambda:qc.compile_exact(2,F(1),max_labels=100))
    exception('negative-horizon',lambda:qc.compile_exact(-1,F(1,2),max_labels=100))
    exception('invalid-net-size',lambda:qc.net(1))
    exception('zero-noisy-error',lambda:qc.compile_noisy(2,F(0),max_labels=100))
    exception('preallocation-label-limit',lambda:qc.compile_exact(100,F(99,100),max_labels=100))
    # Integer safe endpoint inequality: (diameter of decoder cap)^2 <= (sqrt(2)/2)*625^-N.
    for n in range(0,21):
        e=F(1,16*625**n)
        check((8*e)**2*2 < F(1,625**(2*n)),'strict separated cap diameter')
    result={'status':'success','exact_finite_assertions':COUNT,'negative_controls_detected':NEG,
            'finite_free_triple_max_length':5,'finite_free_pair_orbit_profile':profile,
            'compiler_labels':data['labels'],'compiler_rows':sum(len(x) for x in data['rows'].values()),
            'max_row_support':data['max_row_support'],'rational_word_checks':25,
            'spectral_gap_certified':False,'universal_small_ball_certified_by_tests':False,
            'scope':'Exact finite regression, not universal proof, infinite freeness verification, spectral-gap computation, or priority clearance.'}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
