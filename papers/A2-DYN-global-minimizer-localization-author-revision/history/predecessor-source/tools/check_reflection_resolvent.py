#!/usr/bin/env python3
"""Exact matrix checks and finite physical diagnostics for native proofs 290--291.
No finite computation certifies the continuum theorem or the original raw LLT.
"""
from __future__ import annotations
import argparse, json, math
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import check_endpoint_localization as old

RP=Q(47,100); TM=Q(3,50); A=RP/TM; LAM=Q(50,47); Q0=Q(47,53)
T2=A+A*A; T3=A+3*A*A+2*A**3; C1=2+A; C2=2*T2*C1*C1
C3=2*T3*C1**3+6*T2*C1*C2
D3=RP+3*RP**2/TM+3*RP**3/TM**2
D4=RP+7*RP**2/TM+18*RP**3/TM**2+15*RP**4/TM**3
F4=2*D4*C1**4+6*D3*C2*C1*C1

def need(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def solve_tri(d, lo, up, b):
    if not d: return []
    d=list(d); b=list(b)
    for i in range(1,len(d)):
        h=lo[i-1]/d[i-1]; d[i]-=h*up[i-1]; b[i]-=h*b[i-1]
    x=[b[-1]/d[-1]]
    for i in range(len(d)-2,-1,-1): x.append((b[i]-up[i]*x[-1])/d[i])
    return x[::-1]

def exact():
    need(A==Q(47,6) and A/(1+A)==Q0,'matrix contraction constant')
    need(2-2*A*(LAM-1)==1,'weighted column margin')
    need(C1==Q(59,6) and 2+2*LAM*A==Q(56,3),'endpoint forcing constants')
    records=[]; columns=0; non_row_dominant=0
    for m in [2,3,4,7,12,16]:
      for case in range(8):
        R=[Q(9,20),Q(23,50),RP][case%3]
        cs=[Q(4,5)]+[[Q(0),Q(1),Q(1,10**30),Q(2,3)][(i+case)%4]
                     for i in range(1,m)]+[Q(9,10)]
        if case==0:cs=[Q(1)]*(m+1)
        ts=[TM+Q((i+case)%7,13) for i in range(m)]
        w=[1/t for t in ts]; n=m-1
        d=[2+R*cs[i]*(w[i-1]+w[i]) for i in range(1,m)]
        lo=[-R*w[i]*cs[i] for i in range(1,m-1)]
        up=[-R*w[i]*cs[i+1] for i in range(1,m-1)]
        max_col=Q(0); max_weighted=Q(0)
        for j in range(n):
            b=[Q(0)]*n;b[j]=Q(1);x=solve_tri(d,lo,up,b)
            need(all(y>=0 for y in x),'positive inverse entries including simultaneous zeros')
            need(sum(x)<=Q(1,2),'exact unweighted inverse norm')
            weighted=sum(LAM**abs(i-j)*x[i] for i in range(n))
            need(weighted<=1,'exact weighted Green column')
            for i in range(n):
                val=d[i]*x[i]
                if i:val+=lo[i-1]*x[i-1]
                if i+1<n:val+=up[i]*x[i+1]
                need(val==b[i],'exact nonsymmetric inverse identity')
            max_col=max(max_col,sum(x));max_weighted=max(max_weighted,weighted);columns+=1
        for i in range(n):
            row_off=(abs(lo[i-1]) if i else 0)+(abs(up[i]) if i+1<n else 0)
            if row_off>d[i]:non_row_dominant+=1
        records.append({'m':m,'case':case,'R':str(R),'incidences':list(map(str,cs)),
                        'flights':list(map(str,ts)),'max_inverse_column_sum':str(max_col),
                        'max_weighted_Green_sum':str(max_weighted),
                        'scope':'exact algebraic coefficient array, not a claim of physical realizability'})
    need(non_row_dominant>0,'negative control: row-dominance cannot replace column proof')
    # Independent set-partition enumeration verifies low-order recursion coefficients.
    def parts(items):
        if not items:yield ();return
        x,*rest=items
        for p in parts(rest):
            yield ((x,),)+p
            for j in range(len(p)):yield p[:j]+((x,)+p[j],)+p[j+1:]
    cr={1:C1};tr={}
    for r in range(1,7):
        pp=list(parts(list(range(r))))
        tr[r]=sum(Q(math.factorial(len(p)-1))*A**len(p) for p in pp)
        if r>1:cr[r]=2*sum(tr[len(p)]*math.prod(cr[len(b)] for b in p)
                          for p in pp if len(p)>=2)
    need(tr[2]==T2 and tr[3]==T3,'all angle-composition partitions')
    need(cr[2]==C2 and cr[3]==C3,'all second and third stationary-lift partitions')
    constants={k:str(v) for k,v in {'a_star':A,'lambda':LAM,'q0':Q0,'C1':C1,
               'C2':C2,'C3':C3,'D3':D3,'D4':D4,'F4':F4}.items()}
    return {'exact_chains':len(records),'exact_inverse_columns':columns,
            'non_row_dominant_rows_retained':non_row_dominant,
            'simultaneous_zero_incidence_cases':sum('0' in r['incidences'] for r in records),
            'jet_recursion_orders_checked':6,'constants':constants},records

def reflection(o,angles):
    """Full angle-equation Jacobian; does not assume stationarity to differentiate."""
    R=o['R'];z=o['centers'][:,0]+1j*o['centers'][:,1];n=np.exp(1j*angles)
    X=np.diff(z+R*n);m=len(X);D=np.zeros((m,m+1))
    for i in range(m):
        D[i,i]=(-1j*R*n[i]/X[i]).imag
        D[i,i+1]=(1j*R*n[i+1]/X[i]).imag
    B=-(D[:-1]+D[1:])
    for i in range(1,m):B[i-1,i]+=2
    return B,X,n

def etensor(o,angles,vecs):
    """Second or third tensor of E using all mixed complex-log terms."""
    R=o['R'];_,X,n=reflection(o,angles);m=len(X)
    def dx(vs):
        power=len(vs);v=np.prod(np.array(vs),axis=0)
        return (1j**power)*R*(n[1:]*v[1:]-n[:-1]*v[:-1])
    if len(vecs)==2:
        a,b=vecs;edge=(dx([a,b])/X-dx([a])*dx([b])/X**2).imag
    elif len(vecs)==3:
        a,b,c=vecs
        edge=(dx([a,b,c])/X-(dx([a,b])*dx([c])+dx([a,c])*dx([b])+dx([b,c])*dx([a]))/X**2
              +2*dx([a])*dx([b])*dx([c])/X**3).imag
    else:raise ValueError('only second and third tensors are needed')
    return -(edge[:-1]+edge[1:])

def lifts(o,angles,eta):
    m=o['m'];B,_,_=reflection(o,angles);J=np.zeros(m+1);J[0],J[-1]=eta
    K=np.zeros_like(J);Z=np.zeros_like(J)
    if m>1:
        J[1:-1]=np.linalg.solve(B[:,1:-1],-B[:,[0,m]]@eta)
        K[1:-1]=np.linalg.solve(B[:,1:-1],-etensor(o,angles,[J,J]))
        Z[1:-1]=np.linalg.solve(B[:,1:-1],-etensor(o,angles,[J,J,J])-3*etensor(o,angles,[K,J]))
    return J,K,Z

def conv(a,b,N=4):return np.convolve(a,b)[:N+1]

def action_jet(o,angles,J,K=None,Z=None):
    """Independent fourth-order Taylor arithmetic; coefficients contain 1/r!."""
    m=o['m'];K=np.zeros(m+1) if K is None else K;Z=np.zeros(m+1) if Z is None else Z
    xs=[]
    for i in range(m+1):
        h=np.array([1j*angles[i],1j*J[i],1j*K[i]/2,1j*Z[i]/6,0j]);e=np.zeros(5,complex)
        e[0]=np.exp(h[0])
        for r in range(1,5):e[r]=sum(k*h[k]*e[r-k] for k in range(1,r+1))/r
        x=o['R']*e;x[0]+=complex(*o['centers'][i]);xs.append(x)
    total=np.zeros(5)
    for i in range(m):
        X=xs[i+1]-xs[i];u=conv(X,np.conjugate(X)).real;y=np.zeros(5);y[0]=math.sqrt(u[0])
        for r in range(1,5):y[r]=(u[r]-sum(y[k]*y[r-k] for k in range(1,r)))/(2*y[0])
        total+=y
    return total

def physical():
    rng=np.random.default_rng(2026290291);eta=np.array([.7,-.9]);rows=[];fds=[];counter=0
    for run in range(72):
        R=[.45,.46,.47][run%3];m=[1,2,3,5,8,12,20,32][run%8]
        alpha=float(rng.uniform(-math.pi,math.pi));p=float(rng.uniform(-.94,.94))
        if run%12==0:alpha=0.;p=0.;m=8
        elif run%12==1:p=1-1e-12
        o=old.trace(alpha,p,R,m);ang=o['angles'];Hdata=old.action(R,o['centers'],ang)
        B,X,n=reflection(o,ang);J,K,Z=lifts(o,ang,eta)
        if m>1:
            cs=np.array(o['incidences']);factor=R*np.diag(cs[1:-1])@B[:,1:-1]
            ferr=float(np.max(abs(Hdata[2][1:-1,1:-1]-factor)))
            need(ferr<2e-8,'full physical Hessian/reflection row-factor identity')
            need(max(abs(J-Hdata[4]@eta))<3e-7,'independent action and reflection first lift')
        else:ferr=0.
        need(sum(abs(J))<=float(C1)*max(abs(eta))+1e-8,'physical first l1 bound')
        need(sum(abs(K))<=float(C2)*max(abs(eta))**2+1e-8,'physical second l1 bound')
        need(sum(abs(Z))<=float(C3)*max(abs(eta))**3+1e-8,'physical third l1 bound')
        weights=float(LAM)**np.minimum(np.arange(m+1),np.arange(m,-1,-1))
        need(sum(weights*abs(J))<=float(2+2*LAM*A)*max(abs(eta))+1e-8,'physical weighted first lift')
        M1=2+2*LAM*A;M2=2*(1+LAM)*T2*M1**2
        need(sum(weights*abs(K))<=float(M2)*max(abs(eta))**2+1e-8,'physical weighted second lift')
        tensor4=24*action_jet(o,ang,J)[4]
        mixed=3*old.third(R,o['centers'],ang,[K,J,J])
        exact4=tensor4+mixed
        direct4=24*action_jet(o,ang,J,K,Z)[4]
        err=abs(exact4-direct4)/max(1.,abs(exact4),abs(direct4))
        need(err<2e-6,'complete fourth-order stationary-chain identity')
        need(abs(exact4)<=float(F4)*max(abs(eta))**4,'physical fourth derivative bound')
        if abs(mixed)>1e-5:counter+=1
        row={'R':R,'m':m,'alpha0':alpha,'p0':p,'word':o['word'],'incidences':o['incidences'],
             'flights':o['flights'],'clearances':o['clearances'],'physical_roof':o['physical_roof'],
             'exact_displacement_label':o['displacement_label'],'return_count':o['return_count'],
             'initial_section':o['initial_section'],'terminal_section':o['terminal_section'],
             'J':J.tolist(),'K':K.tolist(),'third_lift':Z.tolist(),
             'Hessian_factor_error':ferr,'fourth_action_tensor':tensor4,'mixed_terms_sum':mixed,
             'fourth_reduced_action':exact4,'full_Taylor_chain_fourth':direct4,'chain_relative_error':err}
        if m<=12 and min(o['incidences'])>.06:
            h=2e-6;ap,dp=old.solve_endpoint(o,h*eta);am,dm=old.solve_endpoint(o,-h*eta)
            if old.physical_valid(R,o['centers'],ap) and old.physical_valid(R,o['centers'],am):
                jp,_,_=lifts(o,ap,eta);jm,_,_=lifts(o,am,eta)
                kerr=float(np.max(abs((jp-jm)/(2*h)-K))/max(1.,float(np.max(abs(K)))))
                thirdp=old.third(R,o['centers'],ap,[jp,jp,jp]);thirdm=old.third(R,o['centers'],am,[jm,jm,jm])
                fourerr=abs((thirdp-thirdm)/(2*h)-exact4)/max(1.,abs(exact4))
                need(kerr<5e-4,'same-physical-word second lift finite difference')
                need(fourerr<2e-3,'same-physical-word fourth reduced variation finite difference')
                row['finite_difference']={'step':h,'second_lift_error':kerr,'fourth_variation_error':fourerr}
                fds.append(row['finite_difference'])
            else:row['finite_difference_status']='physical perturbation left domain; not counted as pass'
        else:row['finite_difference_status']='not selected: length/incidence diagnostic conditioning'
        rows.append(row)
    need(counter>0,'negative control: deleting the three mixed terms must change a genuine physical result')
    return {'actual_physical_records':len(rows),'actual_flights':sum(r['m'] for r in rows),
            'section_to_section_records':sum(r['initial_section'] and r['terminal_section'] for r in rows),
            'smallest_sampled_incidence':min(min(r['incidences']) for r in rows),
            'maximum_full_chain_identity_relative_error':max(r['chain_relative_error'] for r in rows),
            'nonzero_mixed_term_negative_controls':counter,'same_physical_word_finite_differences':len(fds),
            'maximum_second_lift_fd_error':max((r['second_lift_error'] for r in fds),default=None),
            'maximum_fourth_variation_fd_error':max((r['fourth_variation_error'] for r in fds),default=None),
            'scope':'finite floating actual-billiard diagnostics, not continuum proof, probability estimation, or interval certification'},rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path);args=ap.parse_args()
    ex,er=exact();ph,pr=physical()
    if args.details:
        args.details.parent.mkdir(parents=True,exist_ok=True)
        args.details.write_text(json.dumps({'exact':er,'physical':pr},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','exact_algebra':ex,'physical':ph,
          'continuum_theorem_certified_by_script':False,'raw_pointwise_LLT_proved':False,
          'four_coordinate_inversion_completed':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
