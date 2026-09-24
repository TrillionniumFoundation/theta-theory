#!/usr/bin/env python3
"""Exact identities and explicit causal-channel witnesses, not proof certification."""
from __future__ import annotations
import argparse, itertools, json
from fractions import Fraction as F
import sympy as s

def require(ok, msg):
    if not ok: raise RuntimeError(msg)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',default='');arg=ap.parse_args();mut=arg.mutant
    g,k,r,u,z,t,p,b=s.symbols('g k r u z t p b')
    f=r**3+(13-2*g+8*k)*r**2+(3-12*g+48*k)*r-1-2*g+8*k
    if mut=='omit-leakage':f=f-8*k
    D=s.diff(f,r)
    H=(-u**3+(7-4*g-8*k)*u**2+(-3+48*k)*u+13+4*g-104*k)/32
    J=-f.subs(r,u)/64
    T=2*(-3*r**2+(14-8*g-16*k)*r-3+48*k)/D
    A=24*g**2+(3*g-10)*r**2+(6*g-20)*r*u+12*g*r+6*g*u-51*g+30-384*k**2-96*k*r-48*k*u-144*k
    poly=s.cancel(64*D*(H+T*J-H.subs(u,r)) -4*(u-r)**2*A)
    require(s.rem(s.Poly(poly,r),s.Poly(f,r)).as_expr()==0,'Full-support square factorization')
    require(s.simplify(T-64*s.diff(H,u).subs(u,r)/D)==0,'Stationarity tie identity')
    require(f.subs({r:s.Rational(33,100),g:s.Rational(6,25),k:s.Rational(1,1000)})<0,'Lower root bracket')
    require(f.subs({r:s.Rational(7,20),g:s.Rational(13,50),k:0})>0,'Upper root bracket')
    R=s.Rational;lo=R(33,100);hi=R(7,20);gm=R(6,25);gp=R(13,50);kp=R(1,1000)
    require(3*lo**2+(26-4*gp)*lo+3-12*gp>8,'Derivative lower')
    require(3*hi**2+(26-4*gm+16*kp)*hi+3-12*gm+48*kp<10,'Derivative upper')
    require(28*lo-6-16*gp*hi-32*kp*hi-6*hi**2>1,'Coin positive margin')
    require(28*hi+96*kp-6-16*gm*lo-6*lo**2<2,'Coin upper margin')
    require(30-10*hi**2-20*hi-51*gp-384*kp**2-96*kp*hi-48*kp-144*kp>8,'Global square positivity')
    require(R(5,32)-kp-R(3,256)>R(1,8),'Transverse monotonicity')
    require(hi**2+4*hi-1-2*gm*(1+lo)+8*kp*(1+hi)<-R(1,10),'Strict posterior row-one sign')
    require(hi**2-4*lo-1+2*gp*(1+hi)+8*kp*(1+hi)<0,'Third coefficient sign')
    require(hi-1+2*gp+8*kp<0,'Middle-count coefficient signs')
    require(32*lo*(1+lo)-8*gp*(hi**2+6*hi+1)>7,'Extreme-count coefficient sign')
    require(kp<(1-hi)/8,'Off-diagonal coefficients stay negative')
    # Direct reconstruction from the full binomial likelihood, independent of the displayed table.
    Q=[(1+g)/4-k,(1-g)/4-k,(1-g)/4-k,(1+g)/4-k]
    table=[]
    for S in range(5):
        row=[]
        for j,target in enumerate(Q):
            expr=s.expand(sum(s.binomial(4,S)*a**S*(1-a)**(4-S)*(target-((1-a)**2 if j<2 else a*a)/2)/2 for a in [(1+b)/2,(1-b)/2]))
            terms=s.Poly(expr,b).terms();require(all(n[0]%2==0 for n,c in terms),'Prior symmetry')
            row.append(s.expand(sum(c*r**(n[0]//2) for n,c in terms)))
        table.append(row)
    L=r*r+6*r+1
    claimed=[0,-8*g*L,32*r*(r+1)-8*g*L,32*r*(r+1)]
    for a,c in zip(table[0],claimed):require(s.rem(s.Poly(256*a-c,r),s.Poly(f,r)).as_expr()==0,'Extreme coefficient reconstruction')
    require(table[4]==list(reversed(table[0])) and table[3]==list(reversed(table[1])),'Reflected coefficient rows')
    # Microscopic exchangeable-error mixture, retaining E[e^2] rather than E[e]^2.
    m,n=s.symbols('m n');a=R(5,16)-5*m/8+n/2;bb=R(3,16)-3*m/8+n/2;kk=(m-n)/2;gg=R(1,4)-m/2
    if mut=='independent-unconditional-noise':kk=(m-m*m)/2
    require(s.expand((1+gg)/4-kk-a)==0 and s.expand((1-gg)/4-kk-bb)==0,'Physical common-signal mixture')
    # exact deterministic functions and minimal channel faces
    atoms=list(itertools.product([0,1],repeat=3));diag=[(0,0,0),(0,0,1),(1,1,0),(1,1,1)]
    masks=[dict(zip(diag,v)) for v in [(0,0,1,1),(1,0,1,1),(1,1,1,1),(1,1,0,1),(1,1,0,0)]]
    def out(e,w):return masks[e].get(w[3:],0)-masks[e].get(w[:3],0)
    def rows(a,b,ideal=False):
        order=tuple(list(range(a))+list(range(3,3+b))+list(range(a,3))+list(range(3+b,6)))
        words=[x+y for x in atoms for y in (diag if ideal else atoms)]
        pre=sorted({tuple(w[i] for i in order[:a+b]) for w in words})
        suffix=sorted({tuple(w[i] for i in order[a+b:]) for w in words})
        def row(e,prefix):
            return tuple(out(e,tuple(dict(zip(order,prefix+ss))[i] for i in range(6))) for ss in suffix)
        return pre,suffix,row
    def certify(a,b,selected,expected,ideal=False):
        pre,suffix,row=rows(a,b,ideal);V={row(e,p) for e in [1,2,3] for p in pre}
        require(len(V)==expected[0],f'{a,b}: forced vertices')
        faces=[]
        for e,prefix in selected:
            # The prefix excludes simultaneous occurrence of the free atom on both tapes.
            require(any(bit!=(0 if e==0 else 1) for bit in prefix),'Ambiguous zero-output gate coupling')
            d0=row(e,prefix);d1=row(1 if e==0 else 3,prefix)
            require(d0!=d1,'Nontrivial mixed channel')
            face=tuple(frozenset((x,y)) for x,y in zip(d0,d1))
            inside=[v for v in V if all(x in F for x,F in zip(v,face))]
            require(len(inside)==1,'Exactly one mandatory vertex in the face')
            faces.append(face)
        if mut=='face-overlap':faces[-1]=faces[0]
        require(all(any(not F&G for F,G in zip(x,y)) for i,x in enumerate(faces) for y in faces[:i]),'Pairwise face separation')
        require(len(faces)==expected[1],'Face capacity')
        return {'vertices':len(V),'additional_faces':len(faces),'lower':sum(expected)}
    certs={
       '20':certify(2,0,[(0,(0,1)),(0,(1,1)),(4,(0,0)),(4,(0,1))],(8,4)),
       '11':certify(1,1,[(0,(0,1)),(0,(1,0)),(4,(0,1)),(4,(1,0))],(10,4)),
       '21':certify(2,1,[(0,(0,1,0)),(0,(1,1,0))],(12,2)),
       '13_ideal':certify(1,3,[(0,(0,0,0,1)),(0,(0,1,1,0))],(8,2),True)}
    if mut=='free-zero-coupling':certify(1,1,[(0,(0,0))],(10,1))
    # Upper full-support residual field; same restrictions build the actual transitions.
    field=[]
    for a in range(4):
        rr=[]
        for b in range(4):
            pre,suf,row=rows(a,b);rr.append(len({row(e,p) for e in range(5) for p in pre}))
        field.append(rr)
    require(field==[[5,10,12,10],[10,15,14,10],[12,14,13,7],[10,10,7,3]],'Full-support residual field')
    profile=[5,10,12,10,10,7,3]
    schedules=[]
    for idx in itertools.combinations(range(6),3):
        a=b=0;path=[(a,b)];order=''
        for j in range(6):
            if j in idx:a+=1;order+='X'
            else:b+=1;order+='Y'
            path.append((a,b))
        upper=max(field[a][b] for a,b in path)
        lower=max([5]+[12 if (a,b) in [(2,0),(0,2)] else 14 if (a,b) in [(1,1),(2,1),(1,2)] else 0 for a,b in path])
        require(lower<=upper,'Causal schedule interval')
        schedules.append({'order':order,'lower':lower,'upper':upper})
    best=min(x['upper'] for x in schedules)
    if mut=='eleven-states':best=11
    require(best==12 and min(x['lower'] for x in schedules)==12,'Order-optimized exact peak')
    require([x['order'] for x in schedules if x['upper']==12]==['XXXYYY','YYYXXX'],'Only serial minimizers')
    require(all(x['lower']>=14 for x in schedules if x['order'] not in ['XXXYYY','YYYXXX']),'Nonserial strict cost')
    # Reverse ideal suffix counts and law-support distinction.
    rev=[]
    for a,b in [(0,2),(0,3),(1,3),(2,3),(3,3)]:
        pre,suf,row=rows(a,b,True);rev.append(len({row(e,p) for e in range(5) for p in pre}))
    if mut=='delete-support':rev[0]=12
    require(rev==[9,9,10,7,3],'Ideal support-aware reverse compiler')
    # Exact finite witnesses are independent of t within (0,1).
    print(json.dumps({'schema':'gtf28.exact/1','square_identity':True,'posterior_coefficients':20,
      'physical_common_signal_mixture':True,'root_interval':['33/100','7/20'],'tie_interval':['1/10','1/4'],
      'full_support_region':{'gamma':['6/25','13/50'],'kappa':['0','1/1000']},
      'physical_noise_range':'0 < sigma <= 1/24','decision_width':5,
      'declared_clock_minimum_peak':12,'nonserial_lower_peak':14,'ideal_reverse_peak':10,
      'certificate_capacities':certs,'residual_field':field,'schedules':schedules,
      'scope':'Exact finite identities and witnesses; continuum proofs and all resource quantifiers are in the manuscript.'},indent=2))
if __name__=='__main__':main()
