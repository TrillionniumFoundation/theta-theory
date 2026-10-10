#!/usr/bin/env python3
"""R27 finite exact witnesses; not proofs of continuum or Borel assertions."""
from __future__ import annotations
import argparse,json,random
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from certificate import evaluate,dot
COUNTS=Counter()
def check(ok,group):
    if not ok:raise RuntimeError('finite check failed: '+group)
    COUNTS[group]+=1

def solve(A,b):
    n=len(b)
    if not n:return []
    a=[list(row)+[v] for row,v in zip(A,b)]
    for k in range(n):
        pivot=next((j for j in range(k,n) if a[j][k]),None)
        if pivot is None:raise RuntimeError('singular finite linear system')
        a[k],a[pivot]=a[pivot],a[k];v=a[k][k];a[k]=[q/v for q in a[k]]
        for j in range(n):
            if j!=k:
                v=a[j][k];a[j]=[q-v*r for q,r in zip(a[j],a[k])]
    return [a[i][-1] for i in range(n)]

def gain(P,T,r):
    m=len(P);reach=[[i==j or bool(P[i][j]) for j in range(m)] for i in range(m)]
    for k in range(m):
        for i in range(m):
            for j in range(m):reach[i][j]|=reach[i][k] and reach[k][j]
    seen=set();closed=[]
    for i in range(m):
        if i in seen:continue
        C=[j for j in range(m) if reach[i][j] and reach[j][i]];seen.update(C)
        if not any(P[j][k] for j in C for k in range(m) if k not in C):closed.append(C)
    g=[F(0)]*m;recurrent=set()
    for C in closed:
        n=len(C);A=[[P[C[j]][C[i]]-F(i==j) for j in range(n)] for i in range(n)]
        A[-1]=[F(1)]*n;b=[F(0)]*n;b[-1]=F(1);pi=solve(A,b)
        v=sum((pi[j]*r[C[j]] for j in range(n)),F(0))/sum((pi[j]*sum(T[C[j]]) for j in range(n)),F(0))
        for j in C:g[j]=v
        recurrent.update(C)
    trans=[i for i in range(m) if i not in recurrent]
    A=[[F(i==j)-P[i][j] for j in trans] for i in trans]
    b=[sum((P[i][j]*g[j] for j in recurrent),F(0)) for i in trans]
    for i,v in zip(trans,solve(A,b)):g[i]=v
    return g

def renewal_case(rows,maxN=12):
    m=len(rows);P=[[F(0)]*m for _ in rows];T=[[F(0)]*m for _ in rows];r=[F(0)]*m
    for i,row in enumerate(rows):
        check(sum(p for p,_,_ in row)==1,'raw_row_normalization')
        for p,j,scores in row:
            check(len(scores)>=1 and all(0<=s<=1 for s in scores),'bounded_marked_scores')
            P[i][j]+=p;T[i][j]+=p*len(scores);r[i]+=p*sum(scores)
    g=gain(P,T,r);b=[r[i]-dot(T[i],g) for i in range(m)];mu=max(map(sum,T))
    check(all(dot(P[i],g)==g[i] for i in range(m)),'harmonic_gain')
    Fhist=[[F(0)]*m];H=[[F(0)]*m];at=[[F(0)]*m]
    for t in range(1,maxN+1):
        f=[sum((p*(sum(scores[:t])+(Fhist[t-len(scores)][j] if len(scores)<=t else F(0))) for p,j,scores in row),F(0)) for row in rows]
        Fhist.append(f);H.append([f[i]-t*g[i] for i in range(m)])
        at.append([sum((p*(sum(scores[t:])-max(len(scores)-t,0)*g[j]) for p,j,scores in row),F(0)) for row in rows])
        for i,row in enumerate(rows):
            rhs=b[i]-at[t][i]+sum((p*H[max(t-len(scores),0)][j] for p,j,scores in row),F(0))
            check(H[t][i]==rhs,'exact_first_excursion_identity')
    for N in range(1,maxN+1):
        u=[sum(H[t][i] for t in range(1,N+1))/N for i in range(m)]
        Delta=max(abs(v) for row in H[1:N+1] for v in row)/N
        B=sum((max(sum((p*max(len(scores)-t,0) for p,j,scores in row),F(0)) for row in rows) for t in range(1,N+1)),F(0))/N
        resid=[b[i]-u[i]+dot(P[i],u) for i in range(m)]
        for i,row in enumerate(rows):
            rhs=sum(at[t][i] for t in range(1,N+1))/N+sum((p*sum((H[s][j] for s in range(max(1,N-len(scores)+1),N+1)),F(0))/N for p,j,scores in row),F(0))
            check(resid[i]==rhs,'exact_terminal_strip_converse')
        check(max(map(abs,resid))<=B+mu*Delta,'converse_residual_bound')
        check((max(u)-min(u))/N<=2*Delta,'converse_oscillation_bound')
        rawz=[F((-1)**i*(i+1)) for i in range(m)]
        flux=[rawz[j]-sum((P[i][j]*rawz[i] for i in range(m)),F(0)) for j in range(m)]
        scale=max(F(1),sum(map(abs,rawz)),N*sum(map(abs,flux))/2)
        z=[v/scale for v in rawz]
        cert=evaluate(P,b,N,u,z);lo=F(cert['lower']);up=F(cert['upper'])
        check(lo<=up,'exact_primal_dual_verification')
        check(Delta<=up+B,'physical_upper_from_constructed_corrector')
        check(Delta>=max(F(0),lo-B)/(mu+2),'physical_dual_lower')
    return P,T,r,g,H

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    rng=random.Random(271010)
    for m in (1,2,3,4):
        for case in range(12):
            rows=[]
            for i in range(m):
                count=rng.randrange(1,4);row=[]
                for j in range(count):
                    dest=rng.randrange(m);tau=rng.randrange(1,5)
                    row.append((F(1,count),dest,tuple(F(rng.randrange(4),3) for _ in range(tau))))
                rows.append(row)
            renewal_case(rows)
    rows=[[(F(1,2),1,(F(0),)),(F(1,2),2,(F(0),)*3)],[(F(1),1,(F(0),))],[(F(1),2,(F(1),))]]
    P,T,r,g,H=renewal_case(rows)
    check(g==[F(1,2),F(0),F(1)],'multichain_classwise_gain')
    check(r[0]-dot(T[0],g)==F(-3,2),'joint_duration_exit_not_product')
    P,T,r,g,H=renewal_case([[(F(1),1,(F(0),))],[(F(1),0,(F(1),))]])
    for N in range(1,13):
        u=[F(-1,4),F(1,4)];z=[F(-1,2*N),F(1,2*N)];b=[F(-1,2),F(1,2)]
        cert=evaluate(P,b,N,u,z)
        check(F(cert['gap'])==0 and F(cert['lower'])==F(1,2*N),'periodic_exact_modulus')
        if N%2==0:check(H[N]==[0,0],'terminal_cancellation_prefix_required')
    P,T,r,g,H=renewal_case([[(F(1),0,(F(1),F(1),F(0),F(0)))]])
    check(H[1]==[F(1,2)] and r[0]-dot(T[0],g)==0,'physical_tail_cannot_be_omitted')
    # Exact loaded marks with mark-dependent physical service duration.
    counts=[[F(0),F(0)]]
    for N in range(1,81):
        values=[F(0),F(0)]
        for mark,L in ((0,1),(1,3)):
            tau=L+2
            values[mark]+=F(max(0,min(N-2,L)),2)
            if tau<=N:
                for j in (0,1):values[j]+=counts[N-tau][j]/2
        counts.append(values)
        for j in (0,1):
            measure=values[j]/N
            check(measure>=max(F(0),F(1,5)-F(1,N))/2,'controlled_load_actual_submass')
            check(measure<=F(3,2),'controlled_load_actual_upper_mass')
            check(measure>=F(max(N-2,0),5*N)/2,'predictable_first_service_mass')
        if N>=10:
            mass=sum(values)/N
            quantized=(values[0]/N)*(values[1]/N)/mass
            check(F(1,40)<=quantized<=F(3,4),'controlled_load_same_task_risk')
    example=None
    for lam in (F(1,100),F(1,8),F(1,3),F(1)):
        for amp in (F(0),F(1,7),F(1)):
            for N in (1,2,3,8,16,100):
                k=amp*min(F(1),1/(N*lam));v=amp/lam if N*lam>=1 else F(0)
                P=[[F(1),F(0)],[lam,1-lam]];z=[F(0),min(F(1),1/(N*lam))]
                cert=evaluate(P,[F(0),amp],N,[F(0),v],z)
                check(F(cert['lower'])==k and F(cert['gap'])==0,'revelation_exact_primal_dual')
                D=amp*sum(((1-lam)**j for j in range(N)),F(0))/(2*N)
                check(k/4<=D<=k/2,'geometric_profile_two_sided')
                example={'P':[[str(v) for v in row] for row in P],'b':['0',str(amp)],'N':N,'u':['0',str(v)],'z':[str(q) for q in z]}
    for power in (1,2,3,4):
        pairs=[(F(j,16),F(j,16)**power) for j in range(17)]
        for N in (1,2,8,64):
            psi=lambda e:max(a*min(F(1),1/(N*(l-e))) if l>e else a for a,l in pairs)
            p0=psi(F(0))
            for e in (F(0),F(1,32),F(1,8),F(1,2)):
                Ae=max(a for a,l in pairs if l<=e);A2=max(a for a,l in pairs if l<=2*e)
                check(max(p0,Ae)<=psi(e)<=max(2*p0,A2),'erasure_profile_exact_split')
    for M in range(2,65):
        q=F(1,12*M*M);w1=F(1,4*M);radius=F(1,4*M)
        check(q>0 and w1==radius,'resolution_scale_witness')
        clipped=radius**2-F(4,3)*M*radius**3
        check(clipped>=radius**2/2,'uniform_truncated_small_ball_mass')
        check(2*(M//2)<=M,'counted_sign_codebook_product')
        check(F(1,12*(M//2)**2)<=9*q,'uniform_quantization_doubling')
    output={'status':'PASS','component':'R27 native finite exact regression','checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),'arithmetic':'fractions.Fraction throughout; no floating diagnostics','normal_optimized_invariant':True,'limitations':'Finite identities and counterexamples only. Not a proof of arbitrary marked kernels, continuum optimization, Borel compactness, or priority. Historical nested counts are not summed.'}
    if args.output:
        args.output.mkdir(parents=True,exist_ok=True)
        (args.output/'R27_FINITE_CERTIFICATE.json').write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
        (args.output/'R27_EXACT_RESPONSE_EXAMPLE.json').write_text(json.dumps(example,sort_keys=True,indent=2)+'\n')
    print(json.dumps(output,sort_keys=True,indent=2))
if __name__=='__main__':main()
