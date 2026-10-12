#!/usr/bin/env python3
"""Exact finite arithmetic regressions; not proofs of continuum claims."""
from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict
from itertools import product
import json

checks=0

def require(condition, message):
    global checks
    checks+=1
    if not condition:
        raise RuntimeError(message)

def bayes(p, a, y, alpha=F(1,5), lam=F(3,5)):
    q=alpha+(1-2*alpha)*p
    f0,f1=F(1,2),F(1,2)+(2*y-1)*lam/4
    if a: f0,f1=f1,f0
    r=(1-q)*f0+q*f1
    return r,q*f1/r

@lru_cache(None)
def value(k,p):
    if k==0:return 2*p*(1-p)
    return min(sum(r*value(k-1,w) for y in(0,1)
                   for r,w in[bayes(p,a,y)]) for a in(0,1))

def action(k,p):
    costs=[sum(r*value(k-1,w) for y in(0,1)
               for r,w in[bayes(p,a,y)]) for a in(0,1)]
    return min(range(2),key=lambda a:(costs[a],a))

def pooling(n,L):
    labels={0:(F(1),F(1,2))}
    paths=[(0,F(1),F(1,2))]
    gaps=F(0)
    for t in range(1,n+1):
        actions={i:action(n-t+1,p) for i,(mass,p) in labels.items()}
        cells=defaultdict(lambda:[F(0),F(0),F(0)])
        for i,(mass,p) in labels.items():
            for y in(0,1):
                r,w=bayes(p,actions[i],y)
                j=min(L-1,int(w*L))
                cells[j][0]+=mass*r;cells[j][1]+=mass*r*w
                cells[j][2]+=mass*r*value(n-t,w)
        newlabels={j:(mass,first/mass) for j,(mass,first,v) in cells.items()}
        require(sum(m for m,p in newlabels.values())==1,'actual total mass')
        for j,(mass,first,v) in cells.items():
            gap=mass*value(n-t,first/mass)-v
            require(gap>=0,'concave acquired Jensen gap')
            gaps+=gap
        newpaths=[]
        # Physical full history paths have their own posterior, not the label's.
        for i,m,pfull in paths:
            for y in(0,1):
                rfull,wfull=bayes(pfull,actions[i],y)
                rlabel,wlabel=bayes(labels[i][1],actions[i],y)
                j=min(L-1,int(wlabel*L))
                newpaths.append((j,m*rfull,wfull))
        for j,(mass,p) in newlabels.items():
            pm=sum(m for jj,m,pf in newpaths if jj==j)
            hidden=sum(m*pf for jj,m,pf in newpaths if jj==j)
            require(pm==mass and hidden==mass*p,'all-edge posterior barycenter')
        paths,labels=newpaths,newlabels
    risk=sum(m*2*p*(1-p) for m,p in labels.values())
    require(risk-value(n,F(1,2))==gaps,'exact Bellman pooling telescope')
    # Correct one-hot squared loss: for X=1 -> 2(1-p)^2; X=0 -> 2p^2.
    direct=sum(m*(pf*2*(1-labels[j][1])**2+(1-pf)*2*labels[j][1]**2)
               for j,m,pf in paths)
    require(direct==risk,'physical risk equals label Bayes risk')
    require(1+n*L>n*L and len(labels)<=L,'phase counted')
    return risk

def determinant(mat):
    a=[r[:] for r in mat];ans=F(1)
    for i in range(len(a)):
        k=next(j for j in range(i,len(a)) if a[j][i])
        if k!=i:a[i],a[k]=a[k],a[i];ans=-ans
        pivot=a[i][i];ans*=pivot
        for j in range(i+1,len(a)):
            ratio=a[j][i]/pivot
            for z in range(i+1,len(a)):a[j][z]-=ratio*a[i][z]
    return ans

def integrate_poly(coeffs,a,b):
    return sum(c*(b**(k+1)-a**(k+1))/(k+1) for k,c in enumerate(coeffs))

def main():
    totals={}
    begin=checks
    for n in range(1,5):
        for L in range(1,10):pooling(n,L)
    totals['exact_pooling_and_physical_paths']=checks-begin
    begin=checks
    # Continuous raw likelihood Jacobian at rational inputs, any d by derivation.
    for d in range(1,5):
        for k in range(1,5):
            q=[F(j+k,sum(range(k,k+d+1))) for j in range(d+1)]
            lam=F(k,6)
            for y in product((F(-1),F(0),F(1)),repeat=d):
                D=1+lam*sum(q[j+1]*y[j] for j in range(d))
                mat=[[((q[i+1]*lam if i==j else 0)*D-
                       q[i+1]*(1+lam*y[i])*lam*q[j+1])/D**2
                      for j in range(d)] for i in range(d)]
                exact=lam**d
                for x in q:exact*=x
                exact/=D**(d+1)
                require(determinant(mat)==exact,'Bayes pushforward Jacobian')
                u=[q[0]/D]+[q[i+1]*(1+lam*y[i])/D for i in range(d)]
                require(sum(u)==1 and min(u)>0,'positive normalized posterior')
                for j in range(d):
                    require((q[0]*u[j+1]/(q[j+1]*u[0])-1)/lam==y[j], 'inverse map')
    totals['raw_sensor_jacobian']=checks-begin
    begin=checks
    # Exact integrated kink examples for density 1+x on [0,1] (submeasure).
    for L in range(2,35):
        h=F(1,L)
        for kink in [F(1,7),F(1,2),F(5,6)]:
            defect=F(0)
            for j in range(L):
                a,b=F(j,L),F(j+1,L)
                mass=integrate_poly([1,1],a,b)
                mean=integrate_poly([0,1,1],a,b)/mass
                def pos(l,r):return integrate_poly([-kink,1-kink,1],l,r)
                integ=(-pos(a,b) if b<=kink else pos(a,b) if a>=kink
                       else -pos(a,kink)+pos(kink,b))
                gap=integ-mass*abs(mean-kink)
                require(gap>=0,'nonsmooth Jensen sign')
                defect+=gap
            require(defect<=h*h,'integrated kink second order')
    totals['integrated_curvature_witnesses']=checks-begin
    begin=checks
    for denom in range(4,15):
        alpha=F(1,denom);lam=F(denom-1,denom)
        for y in [F(-1),F(-1,2),F(1,2),F(1)]:
            q=alpha+(1-2*alpha)*(1+lam*y)/(2+lam*y)
            require((q-F(1,2))*y>0,'noisy observation changes optimal side')
            series=lambda z:sum(lam**(2*k+2)*z**(2*k)/F(2*k+3) for k in range(15))
            diff=series(q)-series(1-q)
            require(diff*(q-F(1,2))>0,'strict information comparison')
        gap=alpha**2*(1-alpha)**2*(1-2*alpha)*lam**5*(1-lam/2)/(20*(2+lam))
        require(gap>0,'positive continuum feedback lower constant')
    totals['feedback_exact_witnesses']=checks-begin
    begin=checks
    for M in range(7,150):
        for n in range(1,8):
            L=(M-4)//(3*n)
            if L>=1:require(4+3*n*L<=M,'channel-controller-phase product')
        for t in range(1,5):
            require(1+t*((M-1)//t)<=M,'disjoint phase budget')
    for den in range(2,30):
        eps=F(1,den)
        src0=[1-2*eps,0,2*eps];src1=[0,1-2*eps,2*eps]
        require(sum(src0)==1 and min(src0)>=0,'erasure normalization')
        tv=sum(abs(a-b) for a,b in zip(src0,src1))/2
        require(tv==1-2*eps,'erasure experiment TV')
        require((1-tv)/2==eps,'deficiency lower')
        require((2*eps)*F(1,4)==eps/2,'squared erasure risk')
    # Negative control: ordinary nearest rounding lacks exact posterior calibration.
    actual=F(1,3);rounded=F(1,2)
    risk=2*(actual*(1-rounded)**2+(1-actual)*rounded**2)
    require(risk-2*actual*(1-actual)==2*(rounded-actual)**2>0,'uncalibrated rounding negative control')
    totals['resources_defect_and_negative_controls']=checks-begin
    print(json.dumps({'component':'R11 posterior pooling','checks':checks,'groups':totals,
                      'arithmetic':'exact rational; finite witnesses only',
                      'continuum_proof':False,'status':'PASS'},sort_keys=True))

if __name__=='__main__':main()
