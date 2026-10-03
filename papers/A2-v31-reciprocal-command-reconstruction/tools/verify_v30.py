#!/usr/bin/env python3
"""Exact finite algebra, independent numerical geometry, and source checks.

No physical apparatus is executed. The numerical tests are not interval
certification, proof certification, or a uniform error theorem.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import numpy as np
from scipy.integrate import quad
from reconstruct_scalar import (bellman_inverse, chain_inverse, convex_hull,
                                threshold_hulls, support, lock_rational)
ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()
NUMERIC = {}


def check(condition, group: str, detail='') -> None:
    if not condition:
        raise RuntimeError(group+': '+str(detail))
    COUNTS[group] += 1


def exact_algebra() -> None:
    for pattern in itertools.product([0, 1], repeat=7):
        for i, j in itertools.combinations(range(7), 2):
            hit = int(any(pattern[i:j+1]))
            fwd = (1-pattern[i])*hit; rev = (1-pattern[j])*hit
            check(fwd-rev == pattern[j]-pattern[i], 'reversal_and_capacity')
            check(fwd == hit-pattern[i], 'endpoint_exclusion')
    for n in range(2, 10):
        for seed in range(9):
            u = [F((i*7+seed*3)%11+1, 12) for i in range(n)] + [F(0)]
            T = [[F(0) for _ in u] for _ in u]
            for i in range(n):
                T[i][min(i+1,n)] += F(1,3)
                T[i][min(i+2,n)] += F(2,3)
            T[n][n] = F(1)
            g = [sum(row[j]*u[j] for j in range(n+1))-u[i] for i,row in enumerate(T)]
            check(bellman_inverse(T,g,n) == u, 'acyclic_stopped_inverse')
            for depth in range(n+1):
                exact = bellman_inverse(T,g,depth)
                noisy = bellman_inverse(T,[x+F((-1)**i,1000) for i,x in enumerate(g)],depth)
                check(all(0 <= x <= y for x,y in zip(exact,u)), 'stopped_order_bound')
                check(max(abs(x-y) for x,y in zip(exact,noisy)) <= F(depth,1000),
                      'stopped_noise_bound')
    n = 24
    u = [F((i%4)+1,4) if i%12 < 4 else F(0) for i in range(n)]
    T = [[F(0) for _ in u] for _ in u]
    for i in range(n):
        T[i][(i+1)%n] = F(2,5); T[i][(i+2)%n] = F(3,5)
    g = [sum(row[j]*u[j] for j in range(n))-u[i] for i,row in enumerate(T)]
    check(bellman_inverse(T,g,5) == u, 'periodic_cone_zero_witness')
    T = [[F(0),F(1,2),F(1,2)], [F(1,2),F(0),F(1,2)], [F(0),F(0),F(1)]]
    g = [F(-1,2),F(-1,2),F(0)]
    for n in range(1,15):
        check(bellman_inverse(T,g,n) == [1-F(1,2)**n,1-F(1,2)**n,F(0)],
              'finite_hitting_hypothesis_necessary')
    for n in range(2,9):
        for zero in range(n+1):
            u = np.array([((j*3+2)%11+1)/12 for j in range(n+1)])
            u[zero] = 0
            rec = chain_inverse(np.diff(u)[None,:])[0]
            check(abs(rec-u[0]) < 2e-15, 'deterministic_chain_specialization')
    for q in range(1,15):
        for p in range(-q,q+1):
            value = F(p,q); eta = .1/(15**2)
            check(lock_rational(float(value)+eta/3,15,eta) == value,
                  'bounded_denominator_lock')
    for exponent in [F(1,6)]:
        check(1-2*exponent == 4*exponent == F(2,3), 'support_smoothing_balance')
        check(F(3,2)*2 == 3 and F(3,2)*4 == 6, 'attempt_and_operation_exponents')
        check(2-4*exponent == F(4,3), 'finite_quadrature_exponent')


def capsule_distance(q, center, a):
    # Distance to the segment center + [-a,0], allowing one a per point.
    w = q-center
    aa = np.sum(a*a,axis=-1)
    lam = np.clip(-np.sum(w*a,axis=-1)/aa,0,1)
    return np.linalg.norm(w+lam[...,None]*a,axis=-1)


def calibration_geometry() -> None:
    rng = np.random.default_rng(29030)
    max_ratio = 0.0
    for sigma in [.08,.16,.32]:
        for alpha in [.001,.003,.006]:
            t=.7; ell=.002*sigma; tau=.003*sigma
            r=ell+tau+t*alpha
            q=rng.uniform([-1.2,-.9],[.3,.9],size=(12000,2))
            center=np.array([0.,0.]); radius=.55
            a=np.array([t,0.])
            angle=alpha*np.sin(19*q[:,0]+7*q[:,1])
            tp=t+tau*np.cos(11*q[:,0])
            ap=np.stack((tp*np.cos(angle),tp*np.sin(angle)),axis=1)
            shift=ell*np.stack((np.cos(5*q[:,1]),np.sin(5*q[:,1])),axis=1)
            qp=q+shift
            hit=capsule_distance(q,center,a)<=radius
            solid=np.linalg.norm(q,axis=1)<=radius
            hitp=capsule_distance(qp,center,ap)<=radius
            solidp=np.linalg.norm(qp,axis=1)<=radius
            changed=(hit & ~solid)!=(hitp & ~solidp)
            tube=np.minimum(abs(capsule_distance(q,center,a)-radius),
                            abs(np.linalg.norm(q,axis=1)-radius))
            check(np.all(tube[changed] <= r+1e-12), 'coupled_capsule_tube_containment')
            max_ratio=max(max_ratio,float(changed.mean())/(r/sigma))
    NUMERIC['capsule_trials'] = 108000
    NUMERIC['capsule_max_empirical_change_over_r_by_sigma'] = round(max_ratio,10)


def disk_average(dist, radius, sigma):
    d=np.asarray(dist)
    out=np.zeros_like(d)
    out[d <= radius-sigma]=1
    mask=(d > abs(radius-sigma)) & (d < radius+sigma)
    x=d[mask]
    if len(x):
        a=np.arccos(np.clip((x*x+radius*radius-sigma*sigma)/(2*x*radius),-1,1))
        b=np.arccos(np.clip((x*x+sigma*sigma-radius*radius)/(2*x*sigma),-1,1))
        rad=(-x+radius+sigma)*(x+radius-sigma)*(x-radius+sigma)*(x+radius+sigma)
        out[mask]=(radius*radius*a+sigma*sigma*b-.5*np.sqrt(np.maximum(rad,0)))/(np.pi*sigma*sigma)
    return out


def hull_geometry() -> None:
    # Uniform-disk averaging is used only for this geometric diagnostic. The
    # threshold lemma requires support/positivity, not a smooth kernel derivative.
    worst=0.0
    for sigma in [.16,.12]:
        step=sigma/6
        xs=np.arange(-2.8,2.8+step/2,step)
        ys=np.arange(-1.4,1.4+step/2,step)
        xx,yy=np.meshgrid(xs,ys)
        points=np.stack((xx.ravel(),yy.ravel()),axis=1)
        centers=[np.array([-1.15,0.]),np.array([1.15,.13])]
        radii=[.62,.51]
        u=sum(disk_average(np.linalg.norm(points-c,axis=1),r,sigma)
              for c,r in zip(centers,radii))
        noisy=np.clip(u+.124*np.sin(101*points[:,0]+83*points[:,1]),0,1)
        hulls=threshold_hulls(points,noisy,sigma)
        check(len(hulls)==2,'adversarial_grid_component_count')
        angles=np.linspace(0,2*np.pi,4096,endpoint=False)
        for h,c,r in zip(hulls,centers,radii):
            true=c[0]*np.cos(angles)+c[1]*np.sin(angles)+r
            error=float(np.max(abs(support(h,angles)-true)))
            worst=max(worst,error/sigma)
            check(error < 3*sigma,'threshold_hull_support_error')
    NUMERIC['grid_hull_max_sampled_Hausdorff_over_sigma']=round(worst,10)
    normalizer=quad(lambda z:np.exp(-1/(1-z*z)) if abs(z)<1 else 0,-1,1)[0]
    def phi(z):
        result=np.zeros_like(z); m=abs(z)<1
        result[m]=np.exp(-1/(1-z[m]**2))/normalizer
        return result
    angles=np.linspace(0,2*np.pi,4096,endpoint=False); spacing=2*np.pi/len(angles)
    true=1+.02*np.cos(2*angles)+.01*np.sin(3*angles)
    true1=-.04*np.sin(2*angles)+.03*np.cos(3*angles)
    true2=-.08*np.cos(2*angles)-.09*np.sin(3*angles)
    records=[]
    for n in [32,64,128]:
        theta=np.arange(n)*2*np.pi/n
        p=1+.02*np.cos(2*theta)+.01*np.sin(3*theta)
        dp=-.04*np.sin(2*theta)+.03*np.cos(3*theta)
        vertices=np.stack((p*np.cos(theta)-dp*np.sin(theta),
                           p*np.sin(theta)+dp*np.cos(theta)),axis=1)
        H=convex_hull(vertices); values=support(H,angles)
        e=float(np.max(abs(values-true))); h=e**(1/6)
        z=(angles+np.pi)%(2*np.pi)-np.pi
        weights=(4*phi(z/h)/h-phi(z/(2*h))/(2*h))/3*spacing
        spectrum=np.fft.fft(values)*np.fft.fft(weights)
        modes=np.fft.fftfreq(len(angles),d=1/len(angles))
        sm=np.fft.ifft(spectrum).real
        sm1=np.fft.ifft(1j*modes*spectrum).real
        sm2=np.fft.ifft(-modes*modes*spectrum).real
        error=max(float(np.max(abs(sm-true))),float(np.max(abs(sm1-true1))),float(np.max(abs(sm2-true2))))
        check(error < 3*e**(2/3),'polygon_C2_smoothing_diagnostic')
        check(np.min(sm+sm2)>0,'reconstructed_positive_curvature')
        records.append({'vertices':n,'sampled_e':round(e,10),'sampled_C2_error':round(error,10)})
    NUMERIC['smooth_support_diagnostics']=records


def source_integrity() -> None:
    pinned={'01_reversal.tex':'e5cc7e7c52284ecb0b773a06a6d86dc1d6dd0a20',
            '02_local_acquisition.tex':'a947f0fae1d7bc5867decc7025b3c3c9cc426f31',
            '03_periods.tex':'ddb7e05792ea6c42e5d6735ea5f1ac0ebe7176aa',
            '04_finite_experiment.tex':'643b36d28189428225b38c47e0201150e7b28299',
            '05_comparison.tex':'9c04be666b86d5a45c5cb04faf2f48a2fdf9570c'}
    main=(ROOT/'main.tex').read_text(); text=main
    inputs=re.findall(r'\\input\{([^}]+)\}',main)
    for name,expected in pinned.items():
        data=(ROOT/'core'/name).read_bytes()
        actual=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        check(actual==expected,'unchanged_reviewed_core_blob',name)
        check('core/'+name[:-4] in inputs,'old_core_remains_active',name)
    for name in inputs:
        path=ROOT/(name+'.tex')
        check(path.is_file(),'active_input_exists',name)
        text+='\n'+path.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'unique_labels')
    for ref in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        check(ref in labels,'resolved_cross_reference',ref)
    bibs=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    for group in re.findall(r'\\cite\{([^}]+)\}',text):
        for key in group.split(','):
            check(key in bibs,'resolved_bibliography',key)


def main() -> None:
    exact_algebra(); calibration_geometry(); hull_geometry(); source_integrity()
    print(json.dumps({'schema':'a2-v30-finite-diagnostics-1','status':'passed',
        'total_checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
        'numerical_diagnostics':NUMERIC,'physical_sensor_executed':False,
        'interval_certified':False,'formal_proof_certificate':False},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
