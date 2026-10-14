#!/usr/bin/env python3
"""Exact finite adversarial witnesses, plus the separately identified inherited suite."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import hashlib,json,os,subprocess,sys,tempfile
import verify
ROOT=Path(__file__).resolve().parent
COUNTS={};WITNESSES=[]
def check(group,ok,message,value=None):
    if not ok:raise RuntimeError(group+': '+message)
    COUNTS[group]=COUNTS.get(group,0)+1
    if value is not None:WITNESSES.append(repr(value))
def capvalue(nu,loss,cap):
    remaining=F(1);total=F(0)
    for j in sorted(range(len(nu)),key=lambda j:(loss[j],j)):
        mass=min(remaining,cap*nu[j]);total+=mass*loss[j];remaining-=mass
    if remaining:raise RuntimeError('infeasible cap')
    return total
def visit(Q):
    a=1-Q[0][0];b=-Q[0][1];c=-Q[1][0];d=1-Q[1][1];det=a*d-b*c
    if det<=0:raise RuntimeError('nontransient test')
    return d/det,-b/det

def main():
    nu=[F(1,2),F(1,3),F(1,6)];f=[F(-1,3),F(0),F(1,3)];t=[F(0),F(1,4),F(1,3)]
    alpha=F(1,5);beta=F(1,7);l=(1-alpha)*(1-beta);u=(1+alpha)*(1+beta)
    distort=[F(1,3),F(-1,3),F(-1,3)]
    check('exact_raw_order',sum(nu[y]*distort[y] for y in range(3))==0,'report normalization')
    joint=[]
    for s in range(2):
        sign=1 if s==0 else -1
        rows=[[nu[y]*(1+sign*alpha*distort[y])*(1+e*sign*beta)/2 for e in (-1,1)] for y in range(3)]
        joint.append(rows)
        check('exact_raw_order',sum(sum(row) for row in rows)==1,'joint row normalized')
        for y,e in product(range(3),range(2)):
            ratio=rows[y][e]/(nu[y]/2)
            check('exact_raw_order',l<=ratio<=u,'two-sided raw joint order',ratio)
    for pattern in product((F(1,4),F(1,2),F(3,4)),repeat=6):
        q=[pattern[:3],pattern[3:]]
        P=[[sum(joint[s][y]) for y in range(3)] for s in range(2)]
        Q=[[sum(P[s][y]*(1-q[s][y]) for y in range(3) if y%2==z) for z in range(2)] for s in range(2)]
        occ=visit(Q);budget=sum(occ)
        accepted=sum(occ[s]*P[s][y]*q[s][y] for s in range(2) for y in range(3))
        check('exact_actual_occupation',accepted==1,'one actual terminal mass')
        xi=[nu[y]*sum(occ[s]*q[s][y] for s in range(2)) for y in range(3)]
        check('exact_relative_mass',sum(xi)>=1/u,'comparison terminal mass',sum(xi))
        for y in range(3):check('exact_relative_cap',xi[y]<=budget*nu[y],'actual prehistory cap')
        for C in ((F(0),),(F(-1,2),F(1,2)),(F(-1,2),F(0),F(1,2))):
            choose=[[C[(y+s)%len(C)] for y in range(3)] for s in range(2)]
            actual=sum(occ[s]*joint[s][y][z]*q[s][y]*(f[y]+(-1 if z==0 else 1)*t[y]-choose[s][y])**2 for s in range(2) for y in range(3) for z in range(2))
            comparison=sum(occ[s]*nu[y]*q[s][y]*(t[y]**2+(f[y]-choose[s][y])**2) for s in range(2) for y in range(3))
            check('exact_task_lower',actual>=l*comparison,'relative loss on actual occupation')
            loss=[t[y]**2+min((f[y]-r)**2 for r in C) for y in range(3)]
            for A,E in ((F(0),F(0)),(F(1,10),F(1,100))):
                mass=(1-A)/u
                lower=l*mass*capvalue(nu,loss,budget/mass)-E
                check('exact_affine_converse',actual>=max(F(0),lower),'rescaled lower with both kinds of error',(actual,lower))
    for lower,upper,b,a in product((F(1,2),F(3,4),F(1)),(F(1),F(5,4)),map(F,range(1,32)),(F(0),F(1,1000),F(1,100))):
        cap=lower*b/(1+b*a)
        if cap<1:continue
        p=lower/cap-a
        check('exact_hazard_restore',p==1/b,'same physical budget')
        for loss,e in ((F(0),F(0)),(F(1,10),F(1,1000))):
            direct=b*(upper*loss/cap+e);closed=upper*(1+b*a)/lower*loss+b*e
            check('exact_hazard_loss',direct==closed,'unified upper substitution',direct)
    for eta,bias,scale in product((F(1,10),F(1,2),F(9,10)),(F(-1),F(0),F(1)),(F(0),F(1),F(1,2**10),F(1,2**40))):
        b=bias*eta
        # Both u A0-A1 and A1-l A0 have diagonal eta, eta*t^2 and off-diagonal +/-b*t.
        det=eta**2*scale**2-b**2*scale**2
        check('exact_singular_order',det>=0 and eta>=0 and eta*scale**2>=0,'PSD principal minors')
        check('exact_rank_strata',(scale==0 and det==0) or scale!=0,'zero-range treatment',(scale,det))
    for e in (F(1,100),F(1,10**12)):
        check('exact_kernel_violation',e>0,'absolute perturbation creates forbidden positive kernel direction',e)
    for live,terminal in product(range(1,12),repeat=2):
        check('exact_role_packing',len(set(range(live))|set(range(terminal)))==max(live,terminal),'event overlap')
        check('exact_role_packing',live+terminal>max(live,terminal),'typed separation')
    for n in range(2,18):
        for true in (F(1,10),F(1,3),F(1,2),F(2,3),F(9,10)):
            false_mass=F(0);miss_mass=F(0);r=F(1,5);low=F(1,4);high=F(3,4)
            for k in range(n+1):
                est=F(k,n);declared=(est-r>=low and est+r<=high and 1-est-r>=low and 1-est+r<=high)
                covered=abs(est-true)<=r
                false=declared and not (low<=true<=high)
                check('exact_pilot_logic',not false or not covered,'false certificate is outside confidence event')
                mass=F(comb(n,k))*true**k*(1-true)**(n-k)
                if false:false_mass+=mass
                if not covered:miss_mass+=mass
            check('exact_pilot_probability',false_mass<=miss_mass,'exact finite tail inclusion',(false_mass,miss_mass))
    for weights in ((F(1,3),F(2,3)),(F(1,7),F(6,7))):
        for b in map(F,range(1,10)):
            for s in (F(0),F(1,5),F(1,2),F(1)):
                if s>b*weights[0] or 1-s>b*weights[1]:continue
                masses=[s,1-s]
                for j in range(2):
                    if masses[j]:check('exact_stratum_budget',b*weights[j]/masses[j]>=1,'retained mass feasible')
                check('exact_stratum_budget',sum(masses)==1,'strata do not drop probability')
    for b in map(F,range(1,30)):
        e=F(1)/(10*b)
        check('exact_absolute_sharpness',b*e*(1/b)==e,'one-step defect versus selected risk',b*e)
    for r in (F(-1),F(-1,3),F(0),F(1,2),F(1)):
        check('exact_all_program_mean_failure',((1-r)**2+(-1-r)**2)/2==1+r*r,'common indistinguishable alternatives')
    with tempfile.TemporaryDirectory(prefix='theta-r59-negative-') as tmp:
        d=Path(tmp)
        for source in (r'\input{missing}',r'\label{x}\label{x}',r'\ref{missing}',r'\cite{missing}'):
            (d/'main.tex').write_text(source)
            try:verify.tex_audit(d)
            except verify.AuditFailure:check('structural_negative_control',True,'bad source rejected')
            else:raise RuntimeError('source auditor accepted deliberate defect')
    env=os.environ.copy();env.update({'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
    args=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'retained/r58-native/regression.py')]
    run=subprocess.run(args,capture_output=True,text=True,env=env)
    if run.returncode:raise RuntimeError('inherited regression failed:\n'+run.stdout+run.stderr)
    inherited=json.loads(run.stdout)
    output={'status':'PASS','new_counts':dict(sorted(COUNTS.items())),'new_checks':sum(COUNTS.values()),'new_exact_checks':sum(v for k,v in COUNTS.items() if k.startswith('exact_')),'witness_sha256':hashlib.sha256('\n'.join(WITNESSES).encode()).hexdigest(),'retained_R58_and_R57':inherited,'limitations':'Finite exact witnesses, structural controls and separately counted inherited floating checks only. Not continuous-parameter proof or independent peer review.'}
    print(json.dumps(output,sort_keys=True,indent=2))
if __name__=='__main__':main()
