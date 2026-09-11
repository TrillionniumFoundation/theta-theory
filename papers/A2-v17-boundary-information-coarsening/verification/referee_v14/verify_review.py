#!/usr/bin/env python3
"""Independent A2-v14 diagnostics; not a proof or global billiard simulation.

Exact rational checks use explicitly conjugated scalar contractions.
Floating checks use actual Euclidean local flight lengths between facing
strictly convex graph patches. They solve finite stationary boundary problems,
not trajectories in a globally completed periodic table. No author code is used.
"""
from __future__ import annotations
import argparse
import json
import math
import platform
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import solve_banded

CHECKS = 0

def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def exact_checks() -> dict:
    start = CHECKS
    cocycles = 0
    negative_controls = 0
    max_n = 8
    for c0, c1 in [(Q(1,3), Q(-1,4)), (Q(-1,5), Q(2,7)), (Q(0), Q(1,2))]:
        c = (c0, c1)
        for r0, r1 in [(Q(1,3), Q(2,5)), (Q(1,2), Q(1,2)), (Q(2,7), Q(3,8))]:
            r = (r0, r1)
            lam = r0*r1
            for b in (0,1):
                o = 1-b
                for u in [Q(-1,5), Q(-1,11), Q(0), Q(1,13), Q(1,4)]:
                    a = c[o]*r[b]-c[b]
                    phi = r[b]*u/(1+a*u)
                    dphi = r[b]/(1+a*u)**2
                    B = 1/(1-c[b]*u)**2
                    Bo = 1/(1-c[o]*phi)**2
                    zeta = u/(1-c[b]*u)
                    zetao = phi/(1-c[o]*phi)
                    require(Bo*dphi == r[b]*B, 'first-flight density cocycle')
                    require(zetao == r[b]*zeta, 'first-flight coordinate cocycle')
                    cocycles += 1
                    ret = r[o]*phi/(1+(c[b]*r[o]-c[o])*phi)
                    require(ret == lam*u/(1-c[b]*(1-lam)*u), 'two-type return')
                    require(Bo*dphi != B/r[b], 'negative control: reciprocal r')
                    negative_controls += 1
                    for n in range(1,max_n+1):
                        ln = lam**n
                        rn = ln*u/(1-c[b]*(1-ln)*u)
                        normalized = rn/ln
                        expected_difference = -c[b]*ln*u*u/((1-c[b]*u)*(1-c[b]*(1-ln)*u))
                        require(normalized-zeta == expected_difference, 'iterate remainder')
                        dn = ln/(1-c[b]*(1-ln)*u)**2
                        require(dn/ln == 1/(1-c[b]*(1-ln)*u)**2, 'normalized derivative')
    blocks = 0
    for g in (Q(1,2), Q(1), Q(3,2)):
        for c0, c1 in [(Q(2),Q(2)), (Q(3,2),Q(5,2)), (Q(7,4),Q(9,4))]:
            z = c0*c1-1
            for m in range(2,13):
                U = (1+2*z)**m
                V = 1+2*m*z
                remainder = sum(Q(math.comb(m,k))*(2*z)**k for k in range(2,m+1))
                require(U-V == remainder and remainder > 0, 'two-flight separation')
                km = Q(4,2**m*(m+1)*math.factorial(m)**2)
                L0,L1 = g/(2*c0*z),g/(2*c1*z)
                det = (U*U-V*V)*km**2*L0**m*L1**m
                require(det > 0, 'two-flight block determinant')
                # Independent elementary inverse of the endpoint quadratic Hessian.
                hb = (c0-Q(1,2)/c1)/g
                off = -1/(2*c1*g)
                determinant = hb*hb-off*off
                require(hb/determinant == L0*(1+2*z), 'endpoint variance')
                require(2*(hb-off)/(determinant*4*c1*c1) == L1, 'middle variance')
                blocks += 1
    # Quadratic well shifted in intrinsic coordinate; same width, distinct branches.
    for t in [Q(1,100),Q(1,25),Q(9,100)]:
        for eps in [Q(-1,3),Q(1,4)]:
            # Rational t keeps the energy t^2/2 and both branches exact.
            energy = t*t/2
            xp = t+eps*energy
            xm = -t+eps*energy
            require(xp-xm == 2*t, 'abstract sheared width')
            require(xp+xm == 2*eps*energy and xp+xm != 0, 'nontrivial branch midpoint')
    return {'checks':CHECKS-start, 'scalar_cocycle_cases':cocycles,
            'two_flight_block_cases':blocks, 'negative_controls':negative_controls,
            'max_iterate':max_n,
            'scope':'Exact rational identities in scalar models and printed two-flight quadratic block; abstract widths are not asserted to be billiard-realizable.'}


class FlightModel:
    def __init__(self, name, gap, coefficients):
        self.name = name
        self.g = float(gap)
        self.coeff = np.asarray(coefficients,dtype=float)
        self.kappa = self.coeff[:,0]
        self.c = 1+self.g*self.kappa
        self.gamma = float(np.arccosh(np.sqrt(np.prod(self.c))))
        self.lam = float(np.exp(-2*self.gamma))
        self.a = np.sqrt(np.prod(self.c))*np.sinh(self.gamma)/(self.g*self.c[::-1])
        self.r = np.sqrt(self.c/self.c[::-1])*np.exp(-self.gamma)

    def graph(self,b,x):
        k,p,q = self.coeff[b]
        return (k*x*x/2+p*x**3/6+q*x**4/24,
                k*x+p*x*x/2+q*x**3/6,
                k+p*x+q*x*x/2)

    def edge(self,b,u,v):
        f,fu,fuu = self.graph(b,u)
        h,hv,hvv = self.graph(1-b,v)
        D = self.g+f+h
        L = np.sqrt(D*D+(v-u)**2)
        p = (D*fu+u-v)/L
        q = (D*hv+v-u)/L
        H11 = (fu*fu+D*fuu+1-p*p)/L
        H22 = (hv*hv+D*hvv+1-q*q)/L
        H12 = (fu*hv-1-p*q)/L
        excess = ((D-self.g)*(D+self.g)+(v-u)**2)/(L+self.g)
        return p,q,H11,H22,H12,excess

    def bridge(self,b,j,u,v):
        i = np.arange(j+1)
        types = (b+i)%2
        sig = np.sqrt(self.c[1-types])
        y = (sig/sig[0]*np.sinh((j-i)*self.gamma)/np.sinh(j*self.gamma)*u
             +sig/sig[-1]*np.sinh(i*self.gamma)/np.sinh(j*self.gamma)*v)
        y[0],y[-1] = u,v
        iterations = 0
        for iterations in range(24):
            arr = np.asarray([self.edge((b+k)%2,y[k],y[k+1]) for k in range(j)])
            diag = arr[:-1,3]+arr[1:,2]
            off = arr[1:-1,4]
            grad = arr[:-1,1]+arr[1:,0]
            band = np.zeros((3,j-1))
            band[1,:]=diag
            band[0,1:]=off
            band[2,:-1]=off
            delta = solve_banded((1,1),band,-grad,check_finite=True)
            y[1:-1]+=delta
            if np.max(np.abs(delta))<2e-16:
                break
        else:
            raise RuntimeError('Newton failed: '+self.name)
        arr = np.asarray([self.edge((b+k)%2,y[k],y[k+1]) for k in range(j)])
        diag = arr[:-1,3]+arr[1:,2]
        off = arr[1:-1,4]
        grad = arr[:-1,1]+arr[1:,0]
        band = np.zeros((3,j-1))
        band[1,:]=diag; band[0,1:]=off; band[2,:-1]=off
        rhs = np.zeros(j-1); rhs[0]=-arr[0,4]
        deriv = np.r_[1,solve_banded((1,1),band,rhs),0]
        pivots = diag.copy()
        for k in range(1,j-1):
            pivots[k] -= off[k-1]**2/pivots[k-1]
        require(bool(np.all(pivots>0) and np.all(arr[:,4]<0)), 'positive twist/Hessian')
        require(float(np.max(np.abs(grad)))<2e-13, 'stationarity residual')
        logflux = np.log(-arr[:,4]).sum()-np.log(pivots).sum()
        cend = (b+j)%2
        logref = .5*math.log(self.a[b]*self.a[cend])-math.log(math.sinh(j*self.gamma))
        return {'x':y,'dx':deriv,'B':float(np.exp(logflux-logref)),
                'action':float(arr[:,5].sum()),'residual':float(np.max(np.abs(grad))),
                'iterations':iterations+1}


def euclidean_checks() -> dict:
    start = CHECKS
    models = [
        FlightModel('equal_curvature_even',1.0,[(1.0,0.0,0.8),(1.0,0.0,-0.3)]),
        FlightModel('unequal_curvature_even',0.8,[(0.7,0.0,1.1),(1.6,0.0,0.4)]),
        FlightModel('unequal_curvature_asymmetric',0.9,[(1.2,0.7,0.9),(0.9,-0.5,0.6)]),
    ]
    rows=[]; max_cocycle=0.; max_scalar=0.; max_stationarity=0.
    flux_errors={str(j):[] for j in [4,5,8,9,12,13,20,21]}
    action_errors={str(j):[] for j in [4,5,8,9,12,13,20,21]}
    for model in models:
        for b in (0,1):
            for u in [-0.12,-0.06,0.05,0.11]:
                half=model.bridge(b,64,u,0.)
                phi,dp=half['x'][1],half['dx'][1]
                other=model.bridge(1-b,64,phi,0.)
                err=abs(other['B']*dp/(model.r[b]*half['B'])-1)
                scalar=half['dx'][16]/(model.lam**8)
                scalarerr=abs(scalar/half['B']-1)
                require(err<2e-10,'Euclidean first-flight cocycle')
                require(scalarerr<2e-8,'Euclidean normalized return derivative')
                max_cocycle=max(max_cocycle,err)
                max_scalar=max(max_scalar,scalarerr)
                max_stationarity=max(max_stationarity,half['residual'],other['residual'])
                rows.append({'model':model.name,'start_type':b,'u':u,
                             'B_reference_64':half['B'],'cocycle_relative_error':err,
                             'scalar_density_relative_error_n8':scalarerr})
                for j in [4,5,8,9,12,13,20,21]:
                    v=-0.075 if u>0 else 0.085
                    right=model.bridge((b+j)%2,64,v,0.)
                    finite=model.bridge(b,j,u,v)
                    ferr=abs(finite['B']/(half['B']*right['B'])-1)
                    aerr=abs(finite['action']-half['action']-right['action'])
                    flux_errors[str(j)].append(ferr)
                    action_errors[str(j)].append(aerr)
                    if j>=20:
                        require(ferr<2e-9,'finite relative factorization at long length')
                        require(aerr<2e-9,'finite action factorization at long length')
    return {'checks':CHECKS-start,'models':[
        {'name':x.name,'gap':x.g,'graph_coefficients_kappa_cubic_quartic':x.coeff.tolist(),
         'gamma':x.gamma,'two_flight_multiplier':x.lam} for x in models],
        'halfline_truncation':64,'cocycle_cases':len(rows),
        'max_cocycle_relative_error':max_cocycle,
        'max_normalized_scalar_derivative_relative_error_n8':max_scalar,
        'max_halfline_stationarity_residual':max_stationarity,
        'max_flux_factorization_errors':{j:max(v) for j,v in flux_errors.items()},
        'max_action_factorization_errors':{j:max(v) for j,v in action_errors.items()},
        'details':rows,
        'scope':'Double precision local Euclidean stationary actions; finite truncation and roundoff, no certified enclosure, no global periodic table or physical trajectory simulation.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    exact=exact_checks()
    euclidean=euclidean_checks()
    result={'reviewed_commit':'e136929b120912586266fb78e0ae7b3c9d43bfd6',
            'status':'pass','checks':CHECKS,'python':platform.python_version(),
            'numpy':np.__version__,'scipy':scipy.__version__,
            'exact':exact,'euclidean':euclidean,
            'not_proof_certification':True,'author_suites_rerun':False,
            'tex_build_rerun':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'pass','checks':CHECKS,'output':str(args.output),
                      'max_cocycle_relative_error':euclidean['max_cocycle_relative_error'],
                      'max_scalar_relative_error':euclidean['max_normalized_scalar_derivative_relative_error_n8']},sort_keys=True))
if __name__=='__main__':
    main()
