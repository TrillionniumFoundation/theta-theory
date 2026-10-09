#!/usr/bin/env python3
"""Finite bridge, short-block and exponent diagnostics; not a billiard proof."""
from fractions import Fraction as F
from math import comb,cos,sin,pi,sqrt
import numpy as np

def require(ok,message):
    if not ok:raise RuntimeError(message)

def mul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return {i:x for i,x in out.items() if x}

def finite_checks():
    e0=F(3,280);k=F(23,2800);eta=F(1,200);alpha=F(1,8)
    require(e0-F(1,400)==k,'projection rate')
    require(k-eta==F(9,2800),'coarse conditional union')
    require(eta*(64-1)-F(6,25)==F(3,40),'fine conditional union/denominator')
    require(eta*alpha==F(1,1600)<F(1,200),'growing probes in joint band')
    require(4*(1-2*alpha)-1==2,'dyadic Gaussian tail summation')
    require(F(2,25)-F(1,200)==F(3,40)>k,'Gaussian endpoint phase variation')
    require(F(1,2)-F(9,100)-2*F(19,100)==F(3,100),'analytic radius')
    require(28*(F(1,2)-F(9,100))-60*F(19,100)==F(2,25),'finite-jet remainder')
    powers=[F(9,25)-40+80*F(9,100)+F(81,100)*b for b in range(1,41)]
    require(max(powers)==-F(1,25) and -max(powers)-e0==F(41,1400),'all residual blocks')
    probe={0:F(1)}
    for _ in range(4):probe=mul(probe,{0:F(1),1:-F(1,2),-1:-F(1,2)})
    require(sum(probe.values())==0,'probe at zero')
    for j in range(8):require(sum(c*i**j for i,c in probe.items())==0,'probe derivative below degree eight')
    require(sum(c*i**8 for i,c in probe.items())==2520,'probe leading derivative')
    probe_error=0.
    for x in np.linspace(-9,9,401):
        y=sum(float(c)*np.exp(1j*i*x) for i,c in probe.items())
        probe_error=max(probe_error,abs(y-(1-cos(x))**4))
    require(probe_error<1e-11,'trigonometric expansion')
    # Exact iid bridge moment, including the finite-n correction.
    bridge_cases=0;errors=[]
    for n in (16,32,64,128,256):
        j=n//2;den=comb(n,n//2)
        e2=sum(F(comb(j,a)*comb(n-j,n//2-a),den)*(2*a-j)**2
               for a in range(max(0,n//2-(n-j)),min(j,n//2)+1))
        require(e2==F(j*(n-j),n-1),'exact Rademacher bridge variance')
        require(e2/n-F(1,4)==F(1,4*(n-1)),'finite bridge covariance correction')
        err=abs(sum(comb(j,a)*comb(n-j,n//2-a)/den*cos((2*a-j)/sqrt(n))
               for a in range(max(0,n//2-(n-j)),min(j,n//2)+1))-np.exp(-1/8))
        errors.append(float(err));bridge_cases+=1
    require(all(a>b for a,b in zip(errors,errors[1:])),'finite bridge characteristic convergence')
    # Distinct spectral projectors: zero and short blocks must not be discarded.
    eye=np.eye(2);max_word_error=0.;max_boundary_error=0.;mixed_nonzero=0.
    import itertools
    for lens in ((0,0,9),(0,1,8),(1,0,8),(8,1,0),(1,1,7),(3,3,3)):
        ps=[];ns=[];ls=[];lambdas=[]
        for angle,z in zip((0.13,-0.09,0.22),(0.04,0.07,-0.03)):
            v=np.array([cos(angle),sin(angle)]);p=np.outer(v,v);lam=np.exp(-z*z/2)
            ps.append(p);ns.append(eye-p);ls.append(lam*p+0.3*(eye-p));lambdas.append(lam)
        direct=np.linalg.matrix_power(ls[2],lens[2])@np.linalg.matrix_power(ls[1],lens[1])@np.linalg.matrix_power(ls[0],lens[0])
        expanded=np.zeros((2,2))
        for choices in itertools.product((0,1),repeat=3):
            word=eye.copy()
            for l,(length,choice) in enumerate(zip(lens,choices)):
                term=(lambdas[l]**length)*ps[l] if choice==0 else (0.3**length)*ns[l]
                word=term@word
            expanded+=word
        max_word_error=max(max_word_error,float(np.linalg.norm(direct-expanded)))
        for l in range(2):
            residual=(0.3**lens[l])*ns[l]
            max_boundary_error=max(max_boundary_error,float(np.linalg.norm(residual@ps[l+1]-residual@(ps[l+1]-ps[l]))))
        principal=(lambdas[2]**lens[2]*ps[2])@(lambdas[1]**lens[1]*ps[1])@(lambdas[0]**lens[0]*ps[0])
        mixed_nonzero=max(mixed_nonzero,float(np.linalg.norm(direct-principal)))
    require(max_word_error<1e-12 and max_boundary_error<1e-12,'short-block spectral algebra')
    require(mixed_nonzero>1e-3,'false pure-principal short-block claim escapes control')
    # Gaussian bridge finite-dimensional covariance, not independent partial sums.
    times=[F(1,4),F(1,2),F(3,4)]
    K=[[min(s,t)-s*t for t in times] for s in times]
    require(K[0][0]==F(3,16) and K[0][2]==F(1,16),'Gaussian bridge covariance')
    det=(K[0][0]*(K[1][1]*K[2][2]-K[1][2]*K[2][1])
         -K[0][1]*(K[1][0]*K[2][2]-K[1][2]*K[2][0])
         +K[0][2]*(K[1][0]*K[2][1]-K[1][1]*K[2][0]))
    require(det==F(1,256)>0,'interior cylinder nondegeneracy')
    require(K[0][0]*K[1][1]-K[0][1]**2>0,'bridge leading minors')
    # Same path selector, two different endpoint events: normalized TV bound.
    probs=[F(i,36) for i in range(1,9)];A={0,1,2,3,4};D={1,2,4,6};E={0,1,2,4,5}
    pA=sum(probs[i] for i in A&D);pE=sum(probs[i] for i in E&D)
    tv=sum(abs((probs[i]/pA if i in A&D else 0)-(probs[i]/pE if i in E&D else 0)) for i in range(8))/2
    diff=sum(probs[i] for i in A^E)
    require(tv<=2*diff/pA,'relative selected event comparison')
    # Replacing the chosen high moment by fourth order would not pay the denominator.
    require(eta*(2-1)-F(6,25)<0,'low-moment negative control')
    return {'joint_band':'m^(9/100)','path_frequency_budget':'m^(1/200)',
      'conditional_characteristic_rate':'23/2800','coarse_union_rate':'9/2800',
      'fine_union_rate':'3/40','probe_frequency_exponent':'1/1600',
      'fixed_residual_orders':[40,29],'all_residual_blocks_checked':len(powers),
      'probe_coefficients':{str(i):str(c) for i,c in sorted(probe.items())},
      'probe_grid_cases':401,'probe_max_error':probe_error,
      'rademacher_bridge_cases':bridge_cases,'rademacher_characteristic_errors':errors,
      'short_block_words_checked':48,'short_block_word_error':max_word_error,
      'short_block_boundary_error':max_boundary_error,'short_block_mixed_term':mixed_nonzero,
      'bridge_scalar_covariance_determinant':str(det),'negative_controls':2,
      'billiard_or_conditional_path_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
