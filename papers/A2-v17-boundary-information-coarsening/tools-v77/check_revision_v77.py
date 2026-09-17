#!/usr/bin/env python3
"""Independent algebra and actual nonlinear finite-billiard checks for A2 v77.

These are reproducible diagnostics, not mathematical proof verification.
Dependencies: numpy, scipy, sympy. No network access is used.
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import root, brentq


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Obstacle:
    center: tuple[float, float]
    radius: float
    epsilon: float

    def frame(self, theta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        n = np.array([np.cos(theta), np.sin(theta)])
        t = np.array([-np.sin(theta), np.cos(theta)])
        h = self.radius + self.epsilon*np.cos(3*theta)
        hp = -3*self.epsilon*np.sin(3*theta)
        curv_radius = self.radius - 8*self.epsilon*np.cos(3*theta)
        curv_radius_p = 24*self.epsilon*np.sin(3*theta)
        return (np.array(self.center)+h*n+hp*t,
                curv_radius*t, curv_radius_p*t-curv_radius*n)


INCIDENCE_MARGINS: list[float] = []
INTERIOR_EIGENVALUES: list[float] = []

OBSTACLES = [Obstacle((0.0, 0.0), 1.0, 0.08),
             Obstacle((4.0, 0.0), 0.8, 0.025)]


def chord(i: int, x: float, j: int, y: float):
    a, ap, app = OBSTACLES[i].frame(x)
    b, bp, bpp = OBSTACLES[j].frame(y)
    z = b-a
    length = np.linalg.norm(z)
    e = z/length
    proj = np.eye(2)-np.outer(e,e)
    grad = np.array([-np.dot(e,ap), np.dot(e,bp)])
    hess = np.array([[ap@proj@ap/length-e@app, -ap@proj@bp/length],
                     [-ap@proj@bp/length, bp@proj@bp/length+e@bpp]])
    return float(length), grad, hess


def full_path(word: list[int], x: np.ndarray):
    value = 0.0
    grad = np.zeros(len(word))
    hess = np.zeros((len(word),len(word)))
    for k in range(len(word)-1):
        v,g,h = chord(word[k],x[k],word[k+1],x[k+1])
        value += v
        grad[k:k+2] += g
        hess[k:k+2,k:k+2] += h
    return value,grad,hess


def action(word: list[int], s: float, t: float):
    middle = np.array([0.0 if i == 0 else np.pi for i in word[1:-1]])
    def evaluate(z):
        return full_path(word,np.r_[s,z,t])
    if len(middle):
        sol = root(lambda z:evaluate(z)[1][1:-1],middle,
                   jac=lambda z:evaluate(z)[2][1:-1,1:-1],tol=1e-11)
        residual = np.max(np.abs(evaluate(sol.x)[1][1:-1]))
        require(residual < 2e-11, f"stationary path residual {residual}")
        value,grad,hess = evaluate(sol.x)
        hin = hess[1:-1,1:-1]
        min_eig = np.linalg.eigvalsh(hin).min()
        require(min_eig > 0, "interior Hessian not positive")
        INTERIOR_EIGENVALUES.append(float(min_eig))
        edges = [0,len(word)-1]
        reduced = hess[np.ix_(edges,edges)]-hess[np.ix_(edges,range(1,len(word)-1))]@np.linalg.solve(hin,hess[np.ix_(range(1,len(word)-1),edges)])
        path = np.r_[s,sol.x,t]
    else:
        value,grad,hess = evaluate(middle)
        reduced = hess
        min_eig = None
        path = np.r_[s,t]
    for i in range(len(word)-1):
        a0=OBSTACLES[word[i]].frame(path[i])[0]
        b0=OBSTACLES[word[i+1]].frame(path[i+1])[0]
        direction=(b0-a0)/np.linalg.norm(b0-a0)
        n0=np.array([np.cos(path[i]),np.sin(path[i])])
        n1=np.array([np.cos(path[i+1]),np.sin(path[i+1])])
        margin=float(min(direction@n0,-direction@n1))
        require(margin>0,'nongrazing support-halfplane test failed')
        INCIDENCE_MARGINS.append(margin)
    return value,grad[[0,-1]],reduced,path,min_eig


def clock_inverse(T: np.ndarray, values: np.ndarray, anchor: int, probe: int):
    g = values/values[:,anchor,None]
    c = np.array([T[1]-T[2],T[2]-T[0],T[0]-T[1]])
    denominator = c@g[:,probe]
    require(abs(denominator)>1e-10, "unusable clock anchor")
    w0 = (c*T)@g[:,probe]/denominator
    d = T-w0
    Q = g[0]/g[1]
    return w0+d[0]*d[1]*(1-Q)/(d[1]-d[0]*Q), float(abs(denominator))


def run() -> dict:
    T1,T2,T3,w0,w,a = sp.symbols('T1 T2 T3 w0 w a')
    T = [T1,T2,T3]
    c = [T2-T3,T3-T1,T1-T2]
    g = [a*(t-w)/(t-w0) for t in T]
    require(sp.factor(sum(c[j]*(T[j]-w0)*g[j] for j in range(3)))==0,
            'symbolic clock cancellation failed')
    root_action = action([0,1,0],0.0,0.0)
    clocks = root_action[0]+np.array([0.18,0.33,0.51])
    nodes = np.linspace(-0.12,0.12,9)
    pairs = np.array([(s,t) for s in nodes for t in nodes])
    lengths = np.array([action([0,1,0],s,t)[0] for s,t in pairs])
    joint = np.exp(0.4*pairs[:,0]-0.3*pairs[:,1]+0.8*pairs[:,0]*pairs[:,1])
    vals = joint[None,:]*(clocks[:,None]-lengths[None,:])
    require(np.all(vals>0), 'clock residual is not positive')
    vals /= vals.sum(axis=1,keepdims=True) # independent normalizations cancel exactly
    anchor = len(pairs)//2
    recovered, clock_margin = clock_inverse(clocks, vals, anchor, 0)
    clock_error = float(np.max(np.abs(recovered-lengths)))
    require(clock_error < 1e-9, f'finite action clock error {clock_error}')

    prefix_errors=[]; schur_errors=[]; root_derivatives=[]; path_residuals=[]
    for t in [-0.0002,0.0,0.0002]:
        for v in [np.pi-0.002,np.pi,np.pi+0.002]:
            def matching(s):
                return action([0,1,0,1],s,v)[1][0]-action([0,1,0],s,t)[1][0]
            s0=brentq(matching,-0.18,0.18,xtol=1e-12)
            U=action([0,1,0],s0,t)
            V=action([0,1,0,1],s0,v)
            ell=chord(0,t,1,v)
            prefix_errors.append(abs(V[0]-U[0]-ell[0]))
            B=U[2][1,1]+ell[2][0,0]
            exact_derivative=-(U[2][0,1]**2)/B
            found=V[2][0,0]-U[2][0,0]
            schur_errors.append(abs(found-exact_derivative))
            root_derivatives.append(found)
            path_residuals.append(float(np.max(np.abs(V[3][:-1]-U[3]))))
    require(max(prefix_errors)<1e-10,'nonlinear prefix length cancellation failed')
    require(max(schur_errors)<1e-10,'matching derivative identity failed')
    require(max(root_derivatives)<0,'matching not monotone')
    require(max(path_residuals)<1e-8,'prefix paths are not physically identical')

    sn=np.array([-0.83,-0.53,-0.19,0.07,0.37,0.76])
    tn=np.pi+np.array([-0.67,0.12,0.69])
    A=np.array([OBSTACLES[0].frame(s)[0] for s in sn])
    B=np.array([OBSTACLES[1].frame(t)[0] for t in tn])
    D=np.sum((A[:,None,:]-B[None,:,:])**2,axis=2)
    X=-0.5*(D[1:,1:]-D[1:,0,None]-D[0,None,1:]+D[0,0])
    M=np.c_[X[:,0]**2,2*X[:,0]*X[:,1],X[:,1]**2,-2*X[:,0],-2*X[:,1]]
    coeff=np.linalg.solve(M,D[1:,0]-D[0,0])
    G=np.array([[coeff[0],coeff[1]],[coeff[1],coeff[2]]]); h=coeff[3:]
    eigen,E=np.linalg.eigh(G)
    require(eigen.min()>0,'recovered metric not positive')
    P=(E*np.sqrt(eigen))@E.T
    ahat=np.r_[np.zeros((1,2)),X]@P.T
    Y=np.array([[0.,0.],[1.,0.],[0.,1.]])
    bhat=np.linalg.solve(P.T,(Y+h).T).T
    true=np.r_[A,B]; hat=np.r_[ahat,bhat]
    u,_,vt=np.linalg.svd((hat-hat.mean(axis=0)).T@(true-true.mean(axis=0)))
    O=u@vt
    shift=true.mean(axis=0)-hat.mean(axis=0)@O
    anchor_error=float(np.max(np.abs(hat@O+shift-true)))
    # Full functions, not only the nine distance anchors.
    all_s=np.linspace(-0.82,0.74,71)
    all_A=np.array([OBSTACLES[0].frame(s)[0] for s in all_s])
    dist=np.sum((all_A[:,None,:]-B[None,:,:])**2,axis=2)
    mat=2*(bhat[1:]-bhat[0])
    rhs=np.sum(bhat[1:]**2,axis=1)-np.sum(bhat[0]**2)-(dist[:,1:]-dist[:,0,None])
    fullhat=np.linalg.solve(mat,rhs.T).T
    function_error=float(np.max(np.abs(fullhat@O+shift-all_A)))
    require(max(anchor_error,function_error)<1e-6,'geometric patch reconstruction failed')
    # Curvature and inclusion margins of the explicitly proved triangular-lattice class.
    R,eps=0.465,0.002
    example_margins={'inner_disk_minus_corridor':R-eps-np.sqrt(3)/4,
                     'half_spacing_minus_outer_disk':0.5-R-eps,
                     'minimum_curvature_radius':R-8*eps}
    require(min(example_margins.values())>0,'example margins failed')
    return {'status':'passed','scope':'Algebra, actual nonlinear regular branches and Euclidean patches; not a proof certificate.',
            'symbolic_clock_identity':True,
            'minimum_tested_incidence_cosine':min(INCIDENCE_MARGINS),
            'minimum_tested_interior_hessian_eigenvalue':min(INTERIOR_EIGENVALUES),
            'actual_nonlinear_clock_error':clock_error,
            'clock_anchor_margin':clock_margin,
            'actual_nonlinear_prefix_length_error':max(prefix_errors),
            'matching_schur_identity_error':max(schur_errors),
            'maximum_matching_derivative':max(root_derivatives),
            'shared_path_coordinate_error':max(path_residuals),
            'distance_certificate_minimum_singular_value':float(np.linalg.svd(M,compute_uv=False).min()),
            'distance_anchor_error_mod_isometry':anchor_error,
            'whole_patch_function_error_mod_isometry':function_error,
            'triangular_example_strict_margins':example_margins}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=run()
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
