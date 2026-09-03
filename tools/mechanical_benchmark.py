#!/usr/bin/env python3
"""Finite-chain regression model; not a substitute for the infinite-state proof."""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm, expm_frechet


def generator(theta: tuple[float, float], sites: int = 12,
              epsilon: float = 0.1, cb: float = 1.5, kb: float = 1.0):
    c, k = theta
    if sites < 2 or min(c, k, cb, kb) <= 0 or epsilon < 0:
        raise ValueError('positive mechanical constants and at least two sites required')
    lap = 2*np.eye(sites)-np.eye(sites,k=1)-np.eye(sites,k=-1)
    lap[0,0] = 1
    C = cb*np.eye(sites); C[0,0] = c
    K = kb*np.eye(sites); K[0,0] = k
    K += epsilon*lap
    A = np.block([[np.zeros_like(C), np.eye(sites)],[-K,-C]])
    B = np.zeros(2*sites); B[sites] = 1
    return A, B, C, K


def transition(theta, duration, sites=12, epsilon=0.1, derivatives=False):
    if duration <= 0:
        raise ValueError('duration must be positive')
    A, B, _, _ = generator(theta, sites, epsilon)
    dim = len(B)
    aug = np.zeros((dim+1,dim+1)); aug[:dim,:dim]=A; aug[:dim,-1]=B
    E = expm(duration*aug)
    result = (E[:dim,:dim], E[:dim,-1])
    if not derivatives:
        return result
    ds=[]
    for col in (sites,0):
        dA = np.zeros_like(aug); dA[sites,col]=-1
        dE=expm_frechet(duration*aug,duration*dA,compute_expm=False)
        ds.append((dE[:dim,:dim],dE[:dim,-1]))
    return (*result,ds)


def prediction(theta, actions, sites=12, initial=None, gradients=False):
    x=np.zeros(2*sites) if initial is None else np.array(initial,dtype=float).copy()
    if x.shape != (2*sites,):
        raise ValueError('initial state dimension mismatch')
    grad=np.zeros((2*sites,2)); means=[]; gs=[]; cache={}
    for duration, force in actions:
        key=float(duration)
        if key not in cache:
            cache[key]=transition(theta,key,sites,derivatives=gradients)
        T,b,*rest=cache[key]
        if gradients:
            old=x.copy()
            grad=T@grad+np.column_stack([dT@old+db*force for dT,db in rest[0]])
        x=T@x+b*force
        means.append(x[0]); gs.append(grad[0].copy())
    return np.array(means),np.array(gs),x,grad


def policy_probs(previous_y, rho):
    if not 0 < rho <= 1:
        raise ValueError('rho outside (0,1]')
    p=np.full(4,rho/4)
    # Feedback selects both duration and sign using only the observed past.
    exploit=(2 if abs(previous_y)>0.1 else 0)+(1 if previous_y>0 else 0)
    p[exploit]+=1-rho
    return p


def simulate(n=512,theta=(1.4,1.6),sites=12,tau=1/32,a=2.0,
             rho=0.5,sigma=0.05,seed=35):
    if n < 1 or sigma <= 0:
        raise ValueError('positive sample size and noise required')
    rng=np.random.default_rng(seed)
    atoms=[(tau,a),(tau,-a),(2*tau,a),(2*tau,-a)]
    cache={d:transition(theta,d,sites) for d in (tau,2*tau)}
    x=np.zeros(2*sites); x[1]=0.5; x[sites+2]=-0.4
    initial=x.copy(); y=[]; noise=[]; actions=[]; probs=[]; previous=0.0
    for _ in range(n):
        p=policy_probs(previous,rho)
        choice=int(rng.choice(4,p=p))
        duration,force=atoms[choice]
        T,b=cache[duration]
        x=T@x+b*force
        xi=float(rng.normal(scale=sigma))
        previous=float(x[0]+xi)
        actions.append((duration,force));y.append(previous);noise.append(xi);probs.append(p)
    return dict(actions=actions,y=np.array(y),noise=np.array(noise),
                probabilities=np.array(probs),initial=initial,final=x)
