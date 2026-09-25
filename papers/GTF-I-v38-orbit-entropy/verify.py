#!/usr/bin/env python3
"""Finite exact witnesses for v38. No finite spectral truncation is a gap proof."""
from __future__ import annotations
import argparse
import itertools
import json
import math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import sympy as s
from scipy.optimize import linprog


def require(ok: bool, text: str) -> None:
    if not ok:
        raise RuntimeError('CHECK_REJECTED: '+text)


def rational_matrix(M):
    return [[str(x) for x in M.row(i)] for i in range(M.rows)]


def calculate(negative: str | None=None):
    counts={}; witnesses={}
    I=s.I
    pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
    c=s.Rational(-3,5);v=s.Rational(4,5)
    rotations=[s.Matrix([[1,0,0],[0,c,-v],[0,v,c]]),
               s.Matrix([[c,0,v],[0,1,0],[-v,0,c]]),
               s.Matrix([[c,-v,0],[v,c,0],[0,0,1]])]
    if negative=='wrong-bloch-sign': rotations[0][1,2]=-rotations[0][1,2]
    six=[];bloch=0
    for j,R in enumerate(rotations):
        U=(s.eye(2)-2*I*pauli[j])/s.sqrt(5)
        require(s.simplify(U.H*U)==s.eye(2),'Unitary gate fails')
        require(R.T*R==s.eye(3) and R.det()==1,'Orthogonality fails')
        for a,b in itertools.product(range(3),repeat=2):
            require(s.simplify(s.trace(pauli[a]*U*pauli[b]*U.H)/2)==R[a,b],
                    'Adjoint and Bloch rotation disagree')
            bloch+=1
        six.extend([R,R.T])
    counts['exact_bloch_entries']=bloch
    witnesses['six_rational_rotations']=[rational_matrix(R) for R in six]

    # The norm certificate is a cited arithmetic theorem, not the output of these tests.
    lam_squared=F(5,9); gap=1-lam_squared
    B=2048*3*16
    require(B==98304 and gap==F(4,9),'Gap normalization arithmetic')
    denominator=F(B,1)/gap
    if negative=='wrong-gap-normalization': denominator=F(B,1)/(1-F(1,3))
    require(denominator==221184,'Use the squared norm gap in the occupation bound')
    require(denominator*90000==19906560000,'Exact calibration constant')
    require(4*19906560000+1==79626240001,'Crossover arithmetic')
    require(s.simplify(150-(82+48*s.sqrt(2)))>0,'Rational net count constant')
    witnesses['gap_certificate']={'external_theorem':'LPS spherical Hecke bound, p=5',
       'normalized_norm_upper':'sqrt(5)/3','squared_gap_lower':'4/9',
       'mean_zero_space':'full L2_0(S^2)','finite_harmonic_test_used':False,
       'old_five_gate_gap_evaluated':False,
       'sources':['LPS 1986/1987','Parzanchevski-Sarnak, section 3.2',
                  'Pisier, Theorem 3(ii)']}
    if negative=='finite-gap-substitution':
        witnesses['gap_certificate']['mean_zero_space']='defining representation only'
    require(witnesses['gap_certificate']['mean_zero_space']=='full L2_0(S^2)',
            'A finite-dimensional gap cannot certify the required full gap')

    # Exact stochastic realization for all rows of a finite sphere-net example.
    N=1;M=math.ceil(2*math.sqrt(2*N));eta=s.Rational(8*N-1,8*N)
    points=[]
    for sign in [-1,1]:
        for a,b in itertools.product(range(-M,M+1),repeat=2):
            x=s.Rational(a,M);y=s.Rational(b,M);den=1+x*x+y*y
            p=s.Matrix([2*x/den,2*y/den,sign*(1-x*x-y*y)/den])
            if p not in points: points.append(p)
    require(all((p.T*p)[0]==1 for p in points),'Stereographic unit norm')
    A=s.Matrix.vstack(s.ones(1,len(points)),s.Matrix.hstack(*points))
    Af=np.array(A,float); row_samples=[];rows=0
    for gi,R in enumerate(six):
        for idx,p in enumerate(points):
            target=s.Matrix([1,*list(eta*R*p)])
            fit=linprog(np.zeros(len(points)),A_eq=Af,b_eq=np.array(target,float).ravel(),
                        bounds=(0,None),method='highs')
            require(fit.success,'Finite rational sphere enclosure is infeasible')
            active=np.flatnonzero(fit.x>1e-8).tolist()
            require(len(active)<=4,'Finite LP returned more than four successors')
            weights=A[:,active].gauss_jordan_solve(target)[0]
            require(all(w.is_Rational for w in weights),'Exact rational row required')
            if negative=='unnormalized-row' and rows==0: weights[0]+=s.Rational(1,100)
            require(sum(weights)==1 and all(w>=0 for w in weights),'Stochastic row normalization')
            require(A[:,active]*weights==target,'Exact row reconstruction')
            if idx==0: row_samples.append({'gate':gi,'label':idx,'successors':active,
                                            'weights':[str(w) for w in weights]})
            rows+=1
    counts['exact_rational_command_rows']=rows
    counts['sphere_net_labels']=len(points)
    witnesses['sphere_N1']={'labels':[list(map(str,p)) for p in points],
                          'eta':str(eta),'sample_rows':row_samples,
                          'all_command_rows_checked':rows}

    # All-spectra constants and a repeated-eigenvalue centroid witness.
    orbital={}
    for q in range(2,9):
        records=[]
        for k in range(1,q):
            m=k*(q-k)
            b=s.prod(s.factorial(q-k+j-1)/s.factorial(j-1) for j in range(1,k+1))/s.factorial(m)
            require(m>=q-1,'Uniform minimum orbit exponent')
            val=max(s.Integer(1),b)*s.Integer(9*q*(q-1)**2)**m
            records.append((k,str(b),str(val)))
        Aq=max(s.Rational(a[2]) for a in records)
        require(Aq>=s.Integer(9*q*(q-1)**2)**(q-1),'Large-radius bound')
        orbital[str(q)]={'s':2*(q-1),'A_q':str(Aq),'grassmann':records}
    counts['all_spectra_constant_dimensions']=len(orbital)
    witnesses['orbital_constants']=orbital
    # A normalized mixture of two pure projectors is not pure for q=3.
    P=s.diag(s.Rational(1,2),s.Rational(1,2),0)
    if negative=='pure-centroid-assumption': require(s.trace(P*P)==1,'Hidden centroids can be mixed')
    require(s.trace(P)==1 and s.trace(P*P)==s.Rational(1,2),'Mixed centroid witness')
    # An isospectral repeated-eigenvalue projector calculation, with exact conjugation.
    A0=s.diag(2,-1,-1)/s.sqrt(6);P0=s.diag(1,0,0)
    projector_cases=0
    for z in [s.Rational(1,3),s.Rational(2,5),s.Rational(3,4),s.Rational(4,5)]:
        cc=(1-z*z)/(1+z*z);ss=2*z/(1+z*z)
        U=s.Matrix([[cc,-ss,0],[ss,cc,0],[0,0,1]])
        C=U*A0*U.T;Q=U*P0*U.T;delta=s.Rational(3)/s.sqrt(6)
        left=s.trace((Q-P0)**2);right=2*s.trace((C-A0)**2)/delta**2
        require(s.simplify(right-left)>=0,'Projector stability inequality')
        projector_cases+=1
    counts['exact_projector_stability_cases']=projector_cases

    # Exact conjugation, seed-span and quantum-readout identities in several dimensions.
    query_checks=0; gate_checks=0
    for q in [2,3,4]:
        eye=s.eye(q);basis=[];seeds=[]
        for i in range(q):
            e=eye[:,i];seeds.append(e*e.H)
        for i in range(q):
            for j in range(i+1,q):
                e=eye[:,i];f=eye[:,j]
                seeds.extend([(e+f)*(e+f).H/2,(e+I*f)*(e+I*f).H/2])
                E=eye[:,i]*eye[:,j].H
                basis.extend([(E+E.H)/s.sqrt(2),I*(E-E.H)/s.sqrt(2)])
        for j in range(1,q):
            basis.append(s.diag(*([1]*j+[-j]+[0]*(q-j-1)))/s.sqrt(j*(j+1)))
        require(len(basis)==q*q-1 and len(seeds)==q*q,'Seed and query alphabets')
        centered=[P-eye/q for P in seeds]
        columns=s.Matrix.hstack(*[s.Matrix(C).reshape(q*q,1) for C in centered])
        require(columns.rank()==q*q-1,'Full predictive seed span')
        rq=s.sqrt(s.Rational(q-1,q));rho=s.Rational(1,10)
        gates=[]
        for j in range(q-1):
            R=eye.copy();R[j:j+2,j:j+2]=s.Matrix([[3,-4],[4,3]])/5
            D=eye.copy();D[j,j]=(3+4*I)/5;D[j+1,j+1]=(3-4*I)/5
            gates.extend([R,R.H,D,D.H])
        require(s.Rational(1,2)+len(gates)*s.Rational(1,8*(q-1))==1,'Lazy alphabet law')
        for G in gates:
            require(s.simplify(G.H*G)==eye and s.simplify(G.det())==1,'SU(q) gate identity')
            gate_checks+=1
        for i,P in enumerate(seeds):
            G=gates[i%len(gates)]*gates[(i+1)%len(gates)]
            sigma=eye/q+rho*(P-eye/q)/rq
            if negative=='wrong-reset-trace' and q==2 and i==0: sigma+=eye/100
            require(s.simplify(s.trace(sigma))==1,'Reset density must have trace one')
            for Fq in basis:
                lhs=s.trace(Fq*G*sigma*G.H)
                rhs=rho*s.trace(Fq*(G*P*G.H-eye/q))/rq
                require(s.simplify(lhs-rhs)==0,'Quantum and classical means disagree')
                query_checks+=1
    counts['exact_SU_gate_checks']=gate_checks
    counts['exact_quantum_coordinate_identities']=query_checks

    # Posterior Hessian identity for a two-point Gaussian mixture.
    x,a,t=s.symbols('x a t',real=True,positive=True)
    logf=-(x*x+a*a)/(2*t*t)+s.log(s.cosh(a*x/t**2))
    hessian=s.diff(logf,x,2)
    require(s.simplify(hessian+1/t**2-a*a/(t**4*s.cosh(a*x/t**2)**2))==0,
            'Gaussian posterior Hessian identity')
    if negative=='wrong-hessian-sign':
        require(s.simplify(hessian-1/t**2-a*a/(t**4*s.cosh(a*x/t**2)**2))==0,
                'Gaussian Hessian negative curvature sign')
    mean_error=F(1,7);tv=mean_error/2
    if negative=='wrong-binary-tv':tv=mean_error
    require(tv==F(1,14),'Binary TV is half the mean error')
    counts['gaussian_hessian_identities']=1
    output={'schema':'gtf38.checks/1','exact_checks':counts,
      'analytic_results':{'projective_width':'Theta(N^(q-1)), fixed q, full group gap and calibrated error',
                         'orbit_bound':'uniform over all traceless Hermitian unit spectra',
                         'effective_six_gate_squared_gap':'4/9, external LPS theorem',
                         'effective_exact_lower_denominator':19906560000,
                         'effective_exact_upper':'<150 N',
                         'old_five_gate_gap_evaluated':False},
      'scope':'Finite exact identities and rational row witnesses. The full gap is an external arithmetic theorem, not certified by these tests. Universal entropy and orbit estimates are proved analytically; no independent priority or proof certification.'}
    return output,witnesses


def reject_control(name: str) -> None:
    """Execute one small, deliberately corrupted witness without rerunning all LPs."""
    if name=='wrong-bloch-sign':
        R=s.Matrix([[1,0,0],[0,s.Rational(-3,5),s.Rational(4,5)],
                    [0,s.Rational(4,5),s.Rational(-3,5)]])
        require(R.T*R==s.eye(3),'Altered Bloch sign breaks orthogonality')
    elif name=='wrong-gap-normalization':
        wrong=F(98304,1)/(1-F(1,3))
        require(wrong==221184,'Unsquared norm produces wrong constant')
    elif name=='finite-gap-substitution':
        certificate={'space':'defining representation only','bound':F(1,2)}
        require(certificate['space']=='full L2_0(S^2)','Finite representation cannot certify full gap')
    elif name=='unnormalized-row':
        row=[F(1,4),F(1,4),F(1,2)+F(1,100)]
        require(sum(row)==1,'Mutated row exceeds unit mass')
    elif name=='pure-centroid-assumption':
        P=s.diag(s.Rational(1,2),s.Rational(1,2),0)
        require(s.trace(P*P)==1,'Mixed hidden centroid is not pure')
    elif name=='wrong-reset-trace':
        reset=s.eye(2)/2+s.eye(2)/100
        require(s.trace(reset)==1,'Perturbed reset has wrong trace')
    elif name=='wrong-hessian-sign':
        x=s.symbols('x',real=True)
        logf=-x*x/2+s.log(s.cosh(x))
        require(s.simplify(s.diff(logf,x,2)-1-1/s.cosh(x)**2)==0,
                'Gaussian Hessian curvature has negative base sign')
    elif name=='wrong-binary-tv':
        a,b=F(1,3),F(2,3)
        wrong=abs((2*a-1)-(2*b-1))
        require(wrong==abs(a-b),'Binary mean error is twice TV')
    else:
        raise RuntimeError('CHECK_REJECTED: unknown negative control')
    raise RuntimeError('Negative witness unexpectedly accepted')

def main():
    p=argparse.ArgumentParser();p.add_argument('--negative-control');p.add_argument('--export',type=Path)
    args=p.parse_args();valid={'wrong-bloch-sign','wrong-gap-normalization','finite-gap-substitution',
          'unnormalized-row','pure-centroid-assumption','wrong-reset-trace','wrong-hessian-sign','wrong-binary-tv'}
    require(args.negative_control is None or args.negative_control in valid,'Unknown control')
    if args.negative_control: reject_control(args.negative_control)
    data,witness=calculate()
    if args.export:
        args.export.parent.mkdir(parents=True,exist_ok=True)
        args.export.write_text(json.dumps(witness,indent=2,sort_keys=True)+'\n')
    print(json.dumps(data,sort_keys=True))
if __name__=='__main__':main()
