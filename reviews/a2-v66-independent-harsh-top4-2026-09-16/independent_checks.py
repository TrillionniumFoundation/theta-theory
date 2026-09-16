#!/usr/bin/env python3
"""Independent finite controls for the v66 global curvature inverse.
No author code is imported. Exact rational identities and high-precision finite
chains do not certify the infinite-dimensional, geometric or statistical proofs.
Requires Python 3 and mpmath. All checks remain active under python -O.
"""
from fractions import Fraction as F
import json, math, random
import mpmath as mp

def require(ok, message):
    if not ok: raise RuntimeError(message)

def norm(v): return max(abs(x) for x in v)
def phi(k,s,z):
    r=len(k)
    return [max(0,s[i]-k[i]+k[i]**2/(k[i]+s[(i+1)%r]+z[(i+1)%r])) for i in range(r)]
def qbound(k,s):return max((k[i]/(k[i]+s[(i+1)%len(k)]))**2 for i in range(len(k)))
def mpv(v):return [mp.mpf(x.numerator)/x.denominator if isinstance(x,F) else mp.mpf(x) for x in v]

def exact_data(k,a):
    r=len(k)
    c=[(k[(i-1)%r]*(1/a[(i-1)%r]-1)-k[i]*(1-a[i]))/2 for i in range(r)]
    s=[k[i]+c[i]-k[i]*a[i] for i in range(r)]
    return c,s

def exact_checks():
    rng=random.Random(660916); cases=[]; iteration_checks=0; pair_checks=0
    for r in range(2,9):
        for rep in range(8):
            k=[F(rng.randint(3,9),4) for _ in range(r)]
            a=[F(rng.randint(1,4),20) for _ in range(r)]
            c,s=exact_data(k,a)
            require(min(c)>0,'Generated curvature not positive')
            require(all(c[i]<s[i]<c[i]+k[i] for i in range(r)),'Schur positivity')
            require(phi(k,s,c)==c,'Projected Schur identity')
            for i in range(r):
                require(k[i]/(k[i]+c[(i+1)%r]+s[(i+1)%r])==a[i],'One-step contraction')
            q=qbound(k,s)
            for z0 in [[F(0)]*r,[2*x for x in s],[F(3,7)]*r]:
                z1=phi(k,s,z0); first=norm([x-y for x,y in zip(z1,z0)]);z=z0
                for n in range(7):
                    error=norm([x-y for x,y in zip(z,c)])
                    require(error<=q**n/(1-q)*first,'A-priori iterate error failed')
                    if n>0:require(all(0<=z[i]<=s[i] for i in range(r)),'Orthant box invariance')
                    iteration_checks+=1;z=phi(k,s,z)
            at=[x*F(19,20) for x in a];ct,st=exact_data(k,at)
            qs=max((k[i]/(k[i]+min(s[(i+1)%r],st[(i+1)%r])))**2 for i in range(r))
            require(norm([x-y for x,y in zip(c,ct)])<=(1+qs)/(1-qs)*norm([x-y for x,y in zip(s,st)]),'Two-point inverse inequality')
            pair_checks+=1
            cases.append({'r':r,'k':k,'a':a,'c':c,'s':s})
    # Independent exact chain elimination: endpoint half mass counted once.
    terminal_checks=0;finite_chain_checks=0;wrong_half_mass=0
    for case in cases:
        k,a,c,s=[case[key] for key in ['k','a','c','s']];r=len(k)
        for N in [r,2*r,4*r]:
            # Terminal exact action continuation must return the original action.
            tail=s[N%r]
            for j in range(N-1,-1,-1):
                i=j%r;tail=k[i]+c[i]-k[i]**2/(k[i]+c[(i+1)%r]+tail)
            require(tail==s[0],'Exact terminal action elimination');terminal_checks+=1
            # Dirichlet terminal endpoint: positive surplus from finite truncation.
            tail=k[(N-1)%r]+c[(N-1)%r]
            for j in range(N-2,-1,-1):
                i=j%r;tail=k[i]+c[i]-k[i]**2/(k[i]+c[(i+1)%r]+tail)
            require(tail>s[0],'Finite Dirichlet truncation comparison');finite_chain_checks+=1
            if tail+c[0]!=tail:wrong_half_mass+=1
    # The author's positive nonimage example and a second nonimage datum.
    k=[F(1),F(1)];s=[F(1,10),F(10)];z=[F(0),F(109,11)]
    require(phi(k,s,z)==z,'Nonimage fixed point')
    raw=s[0]-1+1/(1+s[1]+z[1]);require(raw<0,'Clipping-negative control')
    st=[F(1,5),F(8)];zt=[F(0),F(47,6)]
    require(phi(k,st,zt)==zt,'Second nonimage fixed point')
    qs=max((k[i]/(k[i]+min(s[1-i],st[1-i])))**2 for i in range(2))
    require(norm([z[i]-zt[i] for i in range(2)])<=(1+qs)/(1-qs)*norm([s[i]-st[i] for i in range(2)]),'Nonimage stability');pair_checks+=1
    # A contraction is not a claim of monotone convergence. The homogeneous case
    # k=1,c=1/4,s=3/4 oscillates around its strictly positive fixed point.
    kosc=[F(1)]*2;sosc=[F(3,4)]*2;cosc=[F(1,4)]*2
    z1=phi(kosc,sosc,[F(0)]*2);z2=phi(kosc,sosc,z1)
    require(z1==[F(9,28)]*2 and z2==[F(27,116)]*2,'Oscillating iteration values')
    require(z1[0]>cosc[0]>z2[0],'False monotone-iteration negative control')
    # A curvature-only stopping certificate cannot be added with coefficient one
    # to the entire jet error. Actual smooth normal profiles with c=1/4 and
    # common third derivative 10 have action third derivative 90/7.
    cert=qbound(kosc,sosc)/(1-qbound(kosc,sosc))*F(9,28)
    require(cert==F(12,77),'Curvature certificate')
    # Recomputing the physical tail at c_tilde=9/28 yields
    # q3_hat=2754*sqrt(65)/2093. Prove q3_hat-10 > 12/77 by squaring.
    require(2754**2*65*77**2 > 782**2*2093**2,'Full jet error exceeds raw curvature certificate')
    # Using the observed s in the Schur expression instead also exceeds it.
    at=F(14,29);q3t=F(90,7)*(1-at**3)/(1+at**3)
    require(q3t-F(10)>cert,'Observed-s block also amplifies curvature error')
    amplification={'true_curvature':'1/4','true_action_Hessian':'3/4','true_graph_third_derivative':'10','true_action_third_derivative':'90/7','first_iterate':'9/28','curvature_certificate':str(cert),'physical_tail_recomputed_third_derivative':'2754*sqrt(65)/2093','observed_s_recomputed_third_derivative':str(q3t),'required_form':'C_M*(density_error + flight_error + curvature_iteration_error)','scope':'Countercontrol of unweighted error propagation, not of the exact inverse theorem.'}
    return {'iteration_error_propagation_control':amplification,'realizable_rational_data_sets':len(cases),'physical_periods':list(range(2,9)),'iterate_error_inequalities':iteration_checks,'two_point_inverse_inequalities':pair_checks,'exact_terminal_tail_eliminations':terminal_checks,'finite_Dirichlet_comparisons':finite_chain_checks,'endpoint_double_count_negative_controls':wrong_half_mass,'nonmonotone_iteration':{'true_c':'1/4','z0':'0','z1':str(z1[0]),'z2':str(z2[0])},'positive_nonimage':{'k':['1','1'],'s':['1/10','10'],'z':['0','109/11'],'unclipped_first_component':str(raw)},'scope':'These scalar data satisfy the positive periodic Jacobi identities; no global billiard realization of arbitrary rational data is asserted.'},cases

def forward(k,c):
    s=list(c);r=len(k)
    for count in range(20000):
        nxt=[k[i]+c[i]-k[i]**2/(k[i]+c[(i+1)%r]+s[(i+1)%r]) for i in range(r)]
        if norm([nxt[i]-s[i] for i in range(r)])<mp.mpf('1e-58'):return nxt
        s=nxt
    raise RuntimeError('Forward reference iteration did not converge')

def inverse(k,s):
    z=[mp.mpf(0)]*len(k);q=qbound(k,s)
    for count in range(20000):
        nxt=phi(k,s,z);gap=norm([nxt[i]-z[i] for i in range(len(k))])
        if gap/(1-q)<mp.mpf('1e-50'):return nxt,count+1
        z=nxt
    raise RuntimeError('Inverse did not converge')

def numerical_checks(cases):
    mp.mp.dps=70;worst=mp.mpf(0);jac_worst=mp.mpf(0); iterations=[];chain_worst=mp.mpf(0);records=[]
    chosen=[cases[i] for i in range(0,len(cases),7)]
    for case in chosen:
        k,c,s0=[mpv(case[key]) for key in ['k','c','s']];r=len(k)
        s=forward(k,c);z,it=inverse(k,s);iterations.append(it)
        err=norm([z[i]-c[i] for i in range(r)]);worst=max(worst,err)
        require(err<mp.mpf('1e-48'),'Reconstruction error')
        require(norm([s[i]-s0[i] for i in range(r)])<mp.mpf('1e-54'),'Exact versus iterative forward')
        a=[k[i]/(k[i]+c[(i+1)%r]+s[(i+1)%r]) for i in range(r)]
        T=mp.matrix(r,r)
        for i in range(r):T[i,(i+1)%r]=a[i]**2
        J=mp.inverse(mp.eye(r)-T)*(mp.eye(r)+T)
        h=mp.mpf('1e-20')
        for j in range(r):
            cp=list(c);cm=list(c);cp[j]+=h;cm[j]-=h
            sp=forward(k,cp);sm=forward(k,cm)
            for i in range(r):jac_worst=max(jac_worst,abs((sp[i]-sm[i])/(2*h)-J[i,j]))
        for phase in range(r):
            N=16*r;idx=(phase+N-1)%r;tail=k[idx]+c[idx]
            for j in range(N-2,-1,-1):
                i=(phase+j)%r;tail=k[i]+c[i]-k[i]**2/(k[i]+c[(i+1)%r]+tail)
            chain_worst=max(chain_worst,abs(tail-s[phase]))
        records.append({'period':r,'inverse_steps':it,'max_inverse_error':mp.nstr(err,10)})
    require(jac_worst<mp.mpf('1e-34'),'Curvature differential');require(chain_worst<mp.mpf('1e-30'),'Finite chain precision')
    # Smoothly invertible on the strict image, but clipping gives a kink on its boundary.
    k=[mp.mpf(1)]*2;s=[1/mp.sqrt(2),mp.sqrt(2)];z,_=inverse(k,s)
    require(abs(z[0])<mp.mpf('1e-48') and abs(z[1]-1)<mp.mpf('1e-48'),'Nonnegative-curvature boundary')
    # Equal k and curvature specialization, including small curvature and near-flat loss.
    normal=[]
    for g,c0,c1 in [(1,.05,.1),(2,.3,1.2),(.25,4,.2)]:
        k=[1/mp.mpf(g)]*2;c=mpv([c0,c1]);s=forward(k,c)
        H=mp.sqrt(1+g*g*s[0]*s[1]);special=[(H*mp.sqrt(s[i]/s[1-i])-1)/g for i in range(2)]
        require(norm([special[i]-c[i] for i in range(2)])<mp.mpf('1e-52'),'Normal specialization')
        normal.append({'gap':g,'curvatures':[c0,c1]})
    return {'high_precision_data_sets':len(chosen),'precision_decimal_digits':mp.mp.dps,'max_inverse_error':mp.nstr(worst,12),'max_curvature_Jacobian_error':mp.nstr(jac_worst,12),'finite_Dirichlet_max_error':mp.nstr(chain_worst,12),'records':records,'nonnegative_boundary_control':{'s':['1/sqrt(2)','sqrt(2)'],'z':['0','1'],'strictly_positive_curvature_image':False},'normal_two_site_specializations':normal}

def main():
    exact,cases=exact_checks();numerical=numerical_checks(cases)
    result={'scope':'Independent algebra/finite-chain controls of Section 10. Not certification of infinite orbit convergence, smooth factorization, analytic continuation, global table realization, or sampling theorems.','imports_author_code':False,'exact':exact,'numerical':numerical}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
