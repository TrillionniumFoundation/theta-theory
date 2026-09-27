"""Executed exact regressions for v49. Not independent universal proof certification."""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys
from dual_certificate import threshold, bracket, verify_conclusion, verify_primal, LogValue, ResourceLimit

HOME=Path(__file__).resolve().parent

def require(condition, message):
    if not condition: raise RuntimeError(message)

def interval_product(a,b):
    v=[x*y for x in a for y in b]
    return min(v),max(v)

def matrix_reference(values, delta):
    intervals=[(max(F(-1),f-delta),min(F(1),f+delta)) for f in values]
    a=interval_product(intervals[0],intervals[3]);b=interval_product(intervals[1],intervals[2])
    return max(a[0],b[0])<=min(a[1],b[1])

def cubic(t): return 500*t**3-375*t**2+540*t-124

def cube_floor(value,bits=100):
    scale=1<<bits;lo=0;hi=scale
    while lo<hi:
        mid=(lo+hi+1)//2
        if F(mid,scale)**3<=value:lo=mid
        else:hi=mid-1
    require(F(lo,scale)**3<=value<F(lo+1,scale)**3,'Invalid cube-root isolator')
    return F(lo,scale)

def main():
    matrix_count=0
    for entries in product([F(-1),F(-1,2),F(0),F(1,2),F(1)],repeat=4):
        for delta in [F(0),F(1,4),F(1,2),F(1)]:
            c=threshold((2,2),entries,delta)
            require(c['feasible']==matrix_reference(entries,delta),'Independent determinant interval mismatch')
            require(verify_conclusion((2,2),entries,delta,c),'Unbound or invalid conclusion')
            matrix_count+=1
    rng=random.Random(490927);tensor_count=0;constructed=0
    for dims in [(2,2,2),(2,2,2,2),(1,2,3)]:
        for _ in range(12):
            factors=[[F(rng.randint(-4,4),4) for i in range(d)] for d in dims]
            values=[]
            for key in product(*(range(d) for d in dims)):
                g=F(1)
                for t,i in enumerate(key):g*=factors[t][i]
                values.append(g)
            c=threshold(dims,values,F(0))
            require(c['feasible'] and verify_conclusion(dims,values,0,c),'Lost exact product')
            constructed+=1
    for _ in range(60):
        dims=(2,2,2);values=[F(rng.randint(-8,8),10) for i in range(8)]
        delta=F(rng.choice([0,1,2,3,4,5,8]),10)
        c=threshold(dims,values,delta)
        require(verify_conclusion(dims,values,delta,c),'Invalid random tensor certificate')
        tensor_count+=1
    values=[F(1,10),F(2,5),F(2,5),F(4,5),F(2,5),F(4,5),F(4,5),F(2,5)]
    low=F(260362898747,10**12);high=F(260362898748,10**12)
    require(cubic(low)<0<cubic(high),'Cubic interval does not isolate the root')
    require(750**2-4*1500*540<0,'Derivative positivity failed')
    residues=[(3*x**3+3*x*x+x+2)%7 for x in range(7)]
    require(all(residues),'Cubic irreducibility witness failed')
    lo=threshold((2,2,2),values,low);hi=threshold((2,2,2),values,high)
    require(not lo['feasible'] and hi['feasible'],'Cubic threshold bracket failed')
    require(verify_conclusion((2,2,2),values,low,lo) and verify_conclusion((2,2,2),values,high,hi),'Invalid cubic certificates')
    u0=cube_floor(F(1,10)+high);u1=cube_floor(F(2,5)+high)
    f=(u0,u1);realized=[]
    for key in product(range(2),repeat=3):
        realized.append(f[key[0]]*f[key[1]]*f[key[2]])
    residual=[x-y for x,y in zip(realized,values)]
    error=max(map(abs,residual))/2
    require(error<=high/2,'Dyadic stochastic upper witness failed')
    require(error>low/2,'Inconsistent lower/upper certificates')
    init=[[(1+u)/2,(1-u)/2] for u in [u0,-u0,u1,-u1]]
    rows=[[[ (1+u)/2,(1-u)/2],[(1-u)/2,(1+u)/2]] for u in [u0,u1]]
    decoder=[[u0,-u0],[u1,-u1]]
    for row in init+[r for T in rows for r in T]:
        require(sum(row)==1 and min(row)>=0,'Invalid witness stochastic row')
    # Independent Gram recurrence using exact SymPy and the categorical target
    # represented explicitly by its complete residual list in this finite example.
    S2=2*sum(r*r for r in residual);S4=2*sum(r**4 for r in residual)
    require(S2>0 and S4>0,'Candidate tests must not certify exactness')
    orthogonal_words=0
    for N in range(1,8):
        for w in product(range(2),repeat=N):
            for i in range(2):
                for j in range(2):
                    actual=F(4 if (i+j+sum(w))%2==0 else 3,5)
                    require(abs(actual-F(7,10))/2==F(1,20),'Orthogonal magnitude frontier failed')
                    orthogonal_words+=1
    controls=[]
    broken=deepcopy(lo);broken['certificates'][0]['multipliers']=[0]*len(broken['certificates'][0]['multipliers'])
    require(not verify_conclusion((2,2,2),values,low,broken),'Zero dual accepted');controls.append('zero_dual')
    broken=deepcopy(lo);broken['certificates'][0]['bases'][0]='2'
    require(not verify_conclusion((2,2,2),values,low,broken),'Unbound base accepted');controls.append('altered_base')
    broken=deepcopy(lo);broken['certificates']=[]
    require(not verify_conclusion((2,2,2),values,low,broken),'Uncovered sign chambers accepted');controls.append('missing_chamber')
    broken=deepcopy(hi);broken['log_magnitudes'][0]=LogValue.base(F(2)).scale(-1).dump()
    require(not verify_primal((2,2,2),values,high,broken),'Factor above one accepted');controls.append('factor_out_of_range')
    negative=[F(1),F(1),F(1),F(-1)];cert=threshold((2,2),negative,F(1,4))
    require(cert['kind']=='sign','Expected sign contradiction')
    broken=deepcopy(cert);broken['balanced_entries']*=2
    require(not verify_conclusion((2,2),negative,F(1,4),broken),'Duplicate sign cycle accepted');controls.append('duplicate_sign_cycle')
    try: threshold((2,2),[0,1,2,3],0)
    except ValueError: controls.append('target_out_of_range')
    else: raise RuntimeError('Illegal mean accepted')
    try: threshold((2,2),[0,0,0],0)
    except ValueError: controls.append('incomplete_table')
    else: raise RuntimeError('Incomplete table accepted')
    try: threshold((2,2,2),values,low,max_rows=1)
    except ResourceLimit: controls.append('resource_limit_is_not_infeasibility')
    else: raise RuntimeError('Resource limit not exercised')
    # Exact noncommuting orthogonal Gram identity at horizon three.
    from sympy import Matrix,eye,zeros
    U=[Matrix([[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]),Matrix([[1,0],[0,-1]])]
    T=[Matrix([[F(2,3),F(1,3)],[F(1,4),F(3,4)]]),Matrix([[F(1,5),F(4,5)],[F(3,5),F(2,5)]])]
    E=[Matrix([[1,0]]),Matrix([[0,1]])];x=[Matrix([[1,0]]),Matrix([[0,1]])];rho=F(1,10)
    us=[e.row_join(-rho*xx) for e,xx in zip(E,x)]
    vs=[Matrix([F(1,5),F(-1,3),1,0]),Matrix([F(-1,7),F(2,5),0,1])]
    As=[t.row_join(zeros(2)).col_join(zeros(2).row_join(u.T)) for t,u in zip(T,U)]
    G=sum((u.T*u for u in us),zeros(4))
    for _ in range(3):G=sum((A.T*G*A for A in As),zeros(4))
    gram=sum((v.T*G*v)[0] for v in vs);direct=F(0);wrong=F(0)
    for i in range(2):
        for w in product(range(2),repeat=3):
            ap=eye(4);tp=eye(2);up=eye(2)
            for a in w:ap=ap*As[a];tp=tp*T[a];up=U[a]*up
            for j,v in enumerate(vs):
                R=(us[i]*ap*v)[0]
                target=(up*x[i].T)[j]
                expected=(E[i]*tp*v[:2,0])[0]-rho*target
                require(R==expected,'Target transpose/order mistake')
                direct+=R**2
    require(gram==direct,'Gram sum is not all-word square sum')
    evidence=HOME/'evidence';evidence.mkdir(exist_ok=True)
    evidence_data={'schema':'gtf49.cubic/1','mean_root_polynomial':[500,-375,540,-124],
        'root_interval':[str(low),str(high)],'binary_tv_interval':[str(low/2),str(high/2)],
        'mod7_values':residues,'initialization':[[str(v) for v in row] for row in init],
        'commands':[[[str(v) for v in row] for row in R] for R in rows],
        'decoder_columns':[[str(v) for v in row] for row in decoder],
        'dyadic_upper_actual_error':str(error),'dyadic_S2':str(S2),'dyadic_S4':str(S4),
        'lower_certificate':lo,'upper_log_certificate':hi,
        'scope':'Exact rational bracket and dyadic witness, not an execution of general symbolic optimum isolation.'}
    (evidence/'CUBIC_CERTIFICATE.json').write_text(json.dumps(evidence_data,indent=2,sort_keys=True)+'\n')
    result={'schema':'gtf49.exact/1','independent_2x2_interval_cases':matrix_count,
        'constructed_exact_tensors':constructed,'random_rational_tensor_thresholds':tensor_count,
        'orthogonal_word_coordinate_checks':orthogonal_words,'noncommuting_gram_words':8,
        'cubic_irreducible_modulus':7,'cubic_mean_bracket':[str(low),str(high)],
        'negative_controls_detected':controls,'floating_optimization_used':False,
        'scope':'Finite exact tests and input-bound certificates; universal claims are analytic proofs, not independent peer review.'}
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
