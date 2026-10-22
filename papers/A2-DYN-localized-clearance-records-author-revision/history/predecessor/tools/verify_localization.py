#!/usr/bin/env python3
"""Fresh recovery validation of native modules 304--309.

Reconstructed after workspace loss; this is not the old validator's byte
identity and its outputs are new executions.  Fraction checks concern exact
algebra and finite integer bookkeeping.  Optional numpy diagnostics use real
first-hit triangular Lorentz paths with analytically known comparison minima.
Neither category certifies continuous geometry or the raw pointwise LLT.
All checks use exceptions and remain active under python -O.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def mul(a, x):
    return tuple(a*b for b in x)


def unit(t):
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def fstr(x):
    return f"{x.numerator}/{x.denominator}"


def ceil_cuberoot_fraction(x):
    lo, hi = 0, 1
    while F(hi**3) < x:
        hi *= 2
    while lo+1 < hi:
        mid = (lo+hi)//2
        if F(mid**3) >= x:
            hi = mid
        else:
            lo = mid
    require(F(hi**3) >= x and (hi == 0 or F((hi-1)**3) < x), "exact cube-root ceiling")
    return hi


def log_bounds_fraction(x, terms=32):
    """Exact atanh-series enclosure, after x=2**shift*y, 1<=y<2."""
    require(x >= 1, "positive-log range")
    shift = 0
    while x >= 2:
        x /= 2
        shift += 1

    def series(y):
        z = (y-1)/(y+1)
        lo = 2*sum((z**(2*k+1)/F(2*k+1) for k in range(terms)), F(0))
        hi = lo+2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
        return lo, hi

    a, b = series(F(2))
    c, d = series(x)
    return shift*a+c, shift*b+d


def exact_checks():
    r, n, a, tau, t, c = F(47,100), 94, F(1,416640), F(3,50), F(187,25), 10**8
    rminus = F(9,20)
    require(F(28,5)+4*r == t, "comparison edge upper bound includes both endpoint movements")
    ah = 4*r*r/a+8*r*r*(1+3*n/a+12*n*n)
    af = 24*r*r*n*n*t
    ccut = 4*(r*ah+4*af)/tau
    ktail = max(2*r*c*(4*n)**3, (64*ccut)**2)
    rootk = 64*ccut
    require(rootk*rootk == ktail, "exact square root of K_tail")
    bh = 3*((1+3*n)/a+12*n*n)+8
    bf = 9*n*n*t
    bg = 3*r/a+9*n*r/a+18*n*n*t+36*n*n*r+12*r
    be = 36*n*r+4*r
    require(bg == 167591049 and be == F(39809,25), "global transverse constants")
    require((1+3*n)/a >= 12*n, "initial endpoint and anchor payments share the positive gap")
    kperp = (256*r*bh+1024*bf)*rootk/tau
    cincsq = 512*rootk/(tau*tau)
    flux, h0 = F(3,200), F(1,200)
    d0 = max(2*n+2, ceil_cuberoot_fraction(4*kperp/(flux*flux)), ceil_cuberoot_fraction(4*cincsq))
    require(F(d0**3) >= 4*kperp/(flux*flux) and F(d0**3) >= 4*cincsq, "D0 source ranges")
    require(flux/2 < tau/2, "strict strip regime at source threshold")
    kappa = r/(a*tau)
    qa = kappa/(1+kappa)
    require(kappa == 3263680 and qa == F(3263680,3263681), "exact anchor contraction")
    require(F(47,53) < qa < 1, "new contraction cannot replace narrower original guard")
    require(max(r*ah,2*af) < c, "same quartic constant after shared energy payment")
    require(max(r*bh,2*bf) < bg+be, "same transverse constant after shared energy payment")
    kclock = (32*r/rminus+64)*rootk/tau
    kphase = 8192*rootk/(tau*tau)+24*ktail/rminus**4
    kphase_exp = F(128)/tau+24*c/rminus**4
    require(kphase == F(64)/tau*(128*rootk/tau)+24*ktail/rminus**4, "terminal incoming flight multiplicity")
    agamma_sq, ac_sq, aphi_fourth = 2*r*(bg+be), 2*r/tau, 2*r*kphase_exp
    logarg = max(F(1), 4*agamma_sq/flux**2, 4*ac_sq, aphi_fourth/h0**4)
    numlo, numhi = log_bounds_fraction(logarg)
    denlo, denhi = log_bounds_fraction(1/qa, terms=4)
    ratio_lo, ratio_hi = numlo/denhi, numhi/denlo
    ceil_lo = -(-ratio_lo.numerator//ratio_lo.denominator)
    ceil_hi = -(-ratio_hi.numerator//ratio_hi.denominator)
    require(ceil_lo == ceil_hi, "exact rational logarithms isolate observation ceiling")
    jobs, dobs = 1+ceil_hi, n*(1+ceil_hi)
    require((jobs-1)*denlo >= numhi, "all three observation threshold inequalities")
    require(dobs//n-1 == jobs-1, "observation depth exponent")

    rng = random.Random(304307)
    counts = {name:0 for name in ['integration_by_parts','young_remainder','clock_decomposition','hard_interval_boundary_work','disk_support','shared_positive_gap','cutoff_layers','depth_induction','anchor_overlap','anchor_layer_contraction','geometric_depth_tail','normalized_cost','terminal_incoming_duplication','point_phase_depth_indices']}
    for size in [1,2,3,7,16,32]:
        for _ in range(20):
            vs = [unit(F(rng.randint(-4,4),rng.randint(1,5))) for _ in range(size)]
            vhs = [unit(F(rng.randint(-4,4),rng.randint(1,5))) for _ in range(size)]
            taus = [tau+F(rng.randint(0,20),10) for _ in range(size)]
            ells = [tau+F(rng.randint(0,20),10) for _ in range(size)]
            es = [sub(vh,v) for vh,v in zip(vhs,vs)]
            ds = [(F(1,7),F(-2,9))]
            for i in range(size):
                ds.append(add(ds[-1],sub(mul(ells[i],vhs[i]),mul(taus[i],vs[i]))))
            eta = [F(0)]+[F(rng.randint(0,5),5) for _ in range(size-1)]+[F(0)]
            grad = sum((eta[i]**2*dot(sub(es[i],es[i-1]),ds[i]) for i in range(1,size)),F(0))
            kinetic, work = F(0), F(0)
            for i in range(size):
                require(dot(vs[i],vs[i]) == dot(vhs[i],vhs[i]) == 1, "rational unit directions")
                edge_sum = add(mul(taus[i],vs[i]),mul(ells[i],vhs[i]))
                require((taus[i]+ells[i])**2-dot(edge_sum,edge_sum) == taus[i]*ells[i]*dot(es[i],es[i]), "strict triangle equality fixes minimizing directions")
                require(dot(es[i],sub(ds[i+1],ds[i])) == (ells[i]+taus[i])*dot(es[i],es[i])/2, "exact kinetic identity")
                av = (eta[i]**2+eta[i+1]**2)/2
                bd = eta[i+1]**2-eta[i]**2
                db = mul(F(1,2),add(ds[i],ds[i+1]))
                require(sub(mul(eta[i+1]**2,ds[i+1]),mul(eta[i]**2,ds[i])) == add(mul(av,sub(ds[i+1],ds[i])),mul(bd,db)), "cutoff product identity")
                kinetic += av*(ells[i]+taus[i])*dot(es[i],es[i])/2
                work += bd*dot(es[i],db)
                if av:
                    require(bd*bd/av <= 4*(eta[i+1]-eta[i])**2, "cutoff quotient constant")
                    require(bd*bd*dot(db,db)/(av*(ells[i]+taus[i])) <= (eta[i+1]-eta[i])**2*(dot(ds[i],ds[i])+dot(ds[i+1],ds[i+1]))/tau, "Young remainder normalization")
                    counts['young_remainder'] += 1
            require(grad+kinetic+work == 0, "finite integration by parts sign")
            boundary = dot(vs[-1],ds[-1])-dot(vs[0],ds[0])
            contact = sum((dot(sub(vs[i-1],vs[i]),ds[i]) for i in range(1,size)),F(0))
            flight = sum((ells[i]*dot(es[i],es[i])/2 for i in range(size)),F(0))
            require(sum(ells,F(0))-sum(taus,F(0)) == boundary+contact+flight, "exact clock includes endpoint work")
            counts['integration_by_parts'] += 1
            counts['clock_decomposition'] += 1
            for left,right in [(0,size),(0,1),(size-1,size)]:
                gg = sum((dot(sub(es[i],es[i-1]),ds[i]) for i in range(left+1,right)),F(0))
                kk = sum(((ells[i]+taus[i])*dot(es[i],es[i])/2 for i in range(left,right)),F(0))
                ww = dot(es[right-1],ds[right])-dot(es[left],ds[left])
                require(gg+kk == ww, "hard interval exact boundary work")
                for ei,di in [(es[left],ds[left]),(es[right-1],ds[right])]:
                    payment = tau*dot(ei,ei)/4+dot(di,di)/tau
                    require(payment >= abs(dot(ei,di)), "signed endpoint Young inequality")
                for i in range(left,right):
                    paid = (int(i==left)+int(i==right-1))*tau/4
                    require((ells[i]+taus[i])/2-paid >= ells[i]/2, "one edge may pay both endpoints")
                counts['hard_interval_boundary_work'] += 1

    for _ in range(200):
        normal = unit(F(rng.randint(-5,5),rng.randint(1,6)))
        zz = mul(r*F(rng.randint(0,10),10),unit(F(rng.randint(-5,5),rng.randint(1,6))))
        delta = sub(zz,mul(r,normal))
        require(2*r*(r-dot(normal,zz)) == dot(delta,delta)+r*r-dot(zz,zz), "exact disk support identity")
        require(dot(delta,delta) <= 2*r*(r-dot(normal,zz)), "disk support inequality")
        other = unit(F(rng.randint(-5,5),rng.randint(1,6)))
        bd = sub(mul(r,other),mul(r,normal))
        incidence = F(rng.randint(0,100),100)
        require(dot(mul(-2*incidence,normal),bd) == incidence*dot(bd,bd)/r, "on-circle clock contact equality")
        u = F(rng.randint(0,100),100)
        require((1-u*u)**2 <= 1-u*u, "incidence marginal upper bound")
        hs = [F(rng.randint(0,100),100) for _ in range(9)]
        normalized_contacts = [hh*F(rng.randint(0,100),100) for hh in hs]
        ff = [F(rng.randint(0,100),100) for _ in range(10)]
        gap = sum(hs,F(0))+sum(ff,F(0))/2
        energy = sum(normalized_contacts,F(0))+sum(ff,F(0))/2
        require(energy <= gap, "shared contact and flight energy consume G once")
        inner = F(rng.randint(0,100),100)*qa*gap
        require(inner <= kappa*(gap-inner), "removed-shell rearrangement")
        counts['disk_support'] += 1
        counts['shared_positive_gap'] += 1

    for k in range(20):
        for width in range(1,25):
            for extra in [0,1,3,2*n,2*n+3]:
                m = 2*(k+width)+extra
                eta = [min(F(1),F(max(i-k,0),width),F(max(m-k-i,0),width)) for i in range(m+1)]
                edge_indices = [i for i in range(m) if eta[i+1] != eta[i]]
                use = {}
                for i in edge_indices:
                    require(abs(eta[i+1]-eta[i]) == F(1,width), "exact cutoff slope")
                    for j in (i,i+1): use[j] = use.get(j,0)+1
                require(eta[0] == eta[-1] == 0 and len(edge_indices) == 2*width, "two complete cutoff layers")
                require(len(use) <= 4*width and max(use.values()) <= 2, "transition vertices and multiplicity")
                require(all(k <= j <= m-k for j in use), "layer lies inside S_k")
                target = k+width+n
                if 2*target <= m: require(m-target <= m-k-width-1, "local coercivity includes target")
                counts['cutoff_layers'] += 1
    for d in range(4*n,30001):
        k, width = d//2,d-d//2-n
        require(width >= 1 and 16*width*(k+1) >= (d+1)**2, "induction factor64")
        require(k < d and k+width+n == d, "induction depth identity")
        counts['depth_induction'] += 1
    for d in range(1,30001):
        k, width = d//2,d-d//2
        require(4*width*(k+1) >= d*d, "energy tail constant")
        if d >= 2*n: require(2*(d-n) >= d, "transverse depth loss")
    for theta in [F(1,10),F(1,3),F(49,100)]:
        for m in range(3,3000):
            depth = (theta.numerator*m+theta.denominator-1)//theta.denominator
            if 2*depth < m:
                require(F(m*m,depth**3) <= 1/(theta**3*m), "original m^2 normalized geometric cost")
                counts['normalized_cost'] += 1
    for m in range(3,300):
        for depth in sorted(set([1,max(1,m//4),max(1,(m-1)//2)])):
            b = m-depth
            if b <= depth: continue
            indices = [min(i,b-1) for i in range(depth,b+1)]
            use = {i:indices.count(i) for i in set(indices)}
            require(use[b-1] == 2 and all(v == (2 if i==b-1 else 1) for i,v in use.items()), "last central incoming flight is used twice")
            counts['terminal_incoming_duplication'] += 1
    for m in [1,2,93,94,95,188,193,512]:
        anchors = set(range(93,m,93))
        for u in range(min(m,110)):
            for v in [m,max(u+1,m//2)]:
                if v > m or v <= u: continue
                flights, starts = {}, {}
                for i in range(u+n,v):
                    if i in anchors: continue
                    candidates = [j for j in anchors if j < i]
                    require(bool(candidates), "preceding anchor exists")
                    j = max(candidates)
                    require(j > u and i-j < n, "local anchor remains interior")
                    starts[j] = starts.get(j,0)+1
                    for l in range(j,i): flights[l] = flights.get(l,0)+1
                require(not flights or max(flights.values()) <= n, "flight overlap")
                require(not starts or max(starts.values()) <= n, "anchor overlap")
                counts['anchor_overlap'] += 1
        for d in range(m//2+4):
            if 2*(d+n) > m: continue
            left = [j for j in anchors if d+1 <= j <= d+n-1]
            right = [j for j in anchors if m-d-n+1 <= j <= m-d-1]
            require(bool(left) and bool(right), "both physical boundary layers contain anchors")
            u,v = min(left),max(right)
            require(u < d+n <= m-d-n < v, "anchors enclose singleton as well as interval")
            outer = {i for i in range(1,m) if d <= i <= m-d}
            inner = {i for i in range(1,m) if d+n <= i <= m-d-n}
            flights = {i for i in range(m) if d+n <= i < m-d-n}
            require({u,v}.issubset(outer-inner), "anchor payment belongs to removed layer")
            require(inner.issubset(set(range(u+1,v))) and flights.issubset(set(range(u,v))), "hard interval contains inner energy")
            counts['anchor_layer_contraction'] += 1
    for z in [F(1,2),F(2,3),F(97,100)]:
        def tail(depth):
            block,offset = divmod(depth,n)
            return (n-offset)*z**(block-1)+n*z**block/(1-z)
        for depth in range(n,4*n+5):
            block = depth//n
            require(tail(depth)-tail(depth+1) == z**(block-1), "geometric depth tail one-step identity")
            require(tail(depth+n) == z*tail(depth), "geometric depth block identity")
            require(tail(depth) <= n*z**(block-1)/(1-z), "geometric tail before depth multiplicity")
            counts['geometric_depth_tail'] += 1
    for m in range(2,512):
        for i in range(1,m):
            depth = min(i,m-i)
            incoming = min(i-1,m-i)
            require(incoming >= depth-1 and incoming//n >= max(0,depth//n-1), "point phase includes incoming outer flight")
            if m == 2*i: require(incoming == depth-1, "central singleton incoming depth")
            counts['point_phase_depth_indices'] += 1
    dimensions = [(2*h0,2*h0)]*4+[(F(3,25),F(3,10))]
    require(sum((w+h for w,h in dimensions),F(0)) == F(1,2), "actual section side-length sum")
    for rho in [h0,F(1,1000),F(1,10000)]:
        area = F(0)
        for w,h in dimensions:
            require(2*rho <= min(w,h), "collar inner rectangle is nonnegative")
            piece = (w+2*rho)*(h+2*rho)-(w-2*rho)*(h-2*rho)
            require(piece == 4*rho*(w+h), "collar corners cancel including degeneracy")
            area += piece
        require(area == 2*rho and area/4 == rho/2, "actual invariant collar coefficient before pi and c_star")
    require(-r < r < 1-r < 1+r, "zero-transverse longitudinal strip example")

    constants = {'r':r,'R_minus':rminus,'tau_minus':tau,'a':a,'T':t,'A_H':ah,'A_F':af,'C_cut':ccut,'K_tail':ktail,'sqrt_K_tail':rootk,'B_H':bh,'B_F':bf,'B_G':bg,'B_E':be,'K_perp':kperp,'C_inactive_squared':cincsq,'K_clock':kclock,'K_phase':kphase,'kappa':kappa,'q_anchor':qa,'K_phase_exponential':kphase_exp,'A_clearance_exponential_squared':agamma_sq,'A_incidence_exponential_squared':ac_sq,'A_phase_exponential_fourth':aphi_fourth}
    with localcontext() as ctx:
        ctx.prec = 40
        decimal_constants = {key:str(Decimal(val.numerator)/Decimal(val.denominator)) for key,val in constants.items()}
    return {'status':'passed','scope':'Exact algebra and finite index checks; universal geometry is established by written proof bodies.','counts':counts,'fraction_constants':{key:fstr(val) for key,val in constants.items()},'decimal_constants_for_readability_only':decimal_constants,'exact_D0':d0,'exact_observation_threshold':{'J_obs':jobs,'D_obs':dobs,'maximum_log_argument':fstr(logarg),'isolated_ceiling':ceil_hi,'method':'Exact rational positive atanh-series bounds:32 numerator terms after power-of-two range reduction,4 denominator terms.'},'limits':{'source_mass':'Original full positive source in total variation only','normalized_cost':'Specified polynomial/exponential geometric costs conditional on the named inherited physical-pressure input','unproved':'Full original normalized shortage and raw pointwise LLT; unbounded optical and pairing weights; full unbounded-frequency inversion','normalization':'One original c_star inverse; unchanged full physical roof and exact event'}}


def numerical_diagnostics():
    try:
        import numpy as np
    except ImportError:
        return {'status':'not_run','reason':'numpy unavailable','proof_certificate':False}
    sqrt3 = math.sqrt(3)
    def center(pair):
        return np.array([pair[0]+pair[1]/2,sqrt3*pair[1]/2],dtype=float)
    offsets = [( (aa,bb),center((aa,bb))) for aa in range(-16,17) for bb in range(-16,17) if aa*aa+aa*bb+bb*bb <= 100]

    def actual_path(radius,alpha,momentum,m):
        norm = np.array([math.cos(alpha),math.sin(alpha)])
        tangent = np.array([-norm[1],norm[0]])
        vel = math.sqrt(1-momentum*momentum)*norm+momentum*tangent
        pos = radius*norm
        cp = (0,0)
        qs,os,cps,vs,taus = [pos.copy()],[center(cp)],[cp],[],[]
        max_projection = 0.0
        for _ in range(m):
            vs.append(vel.copy())
            best,hit = math.inf,None
            for offset,_ in offsets:
                if offset == (0,0): continue
                candidate = (cp[0]+offset[0],cp[1]+offset[1])
                cc = center(candidate)
                rel = pos-cc
                proj = float(rel@vel)
                disc = proj*proj-float(rel@rel)+radius*radius
                if disc <= 0: continue
                flight = -proj-math.sqrt(disc)
                if 1e-12 < flight < best:
                    best,hit = flight,candidate
            require(hit is not None and best <= 28/5+1e-9, "actual next hit within proved physical horizon")
            require(best >= 0.06-1e-9, "true next-hit minimum separation")
            cc = center(hit)
            raw = pos+best*vel
            radial = raw-cc
            radius_error = abs(float(np.linalg.norm(radial))-radius)
            max_projection = max(max_projection,radius_error)
            norm = radial/np.linalg.norm(radial)
            require(float(vel@norm) < 0, "true incoming collision")
            pos = cc+radius*norm
            vel = vel-2*float(vel@norm)*norm
            vel /= np.linalg.norm(vel)
            cp = hit
            qs.append(pos.copy());os.append(cc);cps.append(cp);taus.append(best)
        q,o,v,ta = np.array(qs),np.array(os),np.array(vs),np.array(taus)
        normals = (q-o)/radius
        cosines = np.empty(m+1)
        cosines[:-1] = np.einsum('ij,ij->i',v,normals[:-1])
        cosines[-1] = -float(v[-1]@normals[-1])
        require(float(cosines.min()) > 0, "all actual incidences positive")
        return q,o,v,ta,cosines,cps,max_projection

    def segdist(z,a,b):
        edge = b-a
        u = max(0.0,min(1.0,float((z-a)@edge)/float(edge@edge)))
        return float(np.linalg.norm(z-a-u*edge))

    records, strips, clocks, points = [],[],[],[]
    maximum_excess = 0.0
    for radius in [0.45,0.46,0.47]:
        x = (1-2*radius)/radius
        growth = 1+x+math.sqrt(x*(2+x))
        for m in [3,12,32,193,257]:
            q,o,v,ta,cosines,cps,projection = actual_path(radius,1e-4*growth**(-m),0.0,m)
            require(all(pair == (i%2,0) for i,pair in enumerate(cps)), "actual alternating physical word")
            y = np.array([[radius if i%2 == 0 else 1-radius,0.0] for i in range(m+1)])
            edges = y[1:]-y[:-1]
            ell = np.linalg.norm(edges,axis=1)
            vh = edges/ell[:,None]
            ds,es = y-q,vh-v
            hf = cosines[1:-1]*np.einsum('ij,ij->i',ds[1:-1],ds[1:-1])
            ff = ell*np.einsum('ij,ij->i',es,es)
            require(float(np.max(abs(ell-(1-2*radius)))) < 1e-14, "analytic global-minimum lower bound attained flightwise")
            def phase_case(j,fi):
                nn,nh = (q[j]-o[j])/radius,(y[j]-o[j])/radius
                angle = abs(math.atan2(nn[0]*nh[1]-nn[1]*nh[0],float(nn@nh)))
                tangent,th = np.array([-nn[1],nn[0]]),np.array([-nh[1],nh[0]])
                phase = max(angle,abs(float(v[fi]@tangent)-float(vh[fi]@th)))**4
                bound = 8*float(es[fi]@es[fi])**2+24*0.45**-4*float(ds[j]@ds[j])**2
                require(phase <= bound+1e-35+1e-8*bound, "physical point-phase inequality")
                return phase,bound
            for j in sorted(set([1,m-1,m//2])):
                phase,bound = phase_case(j,j-1)
                points.append({'R':radius,'m':m,'contact':j,'central_singleton':2*j==m,'phase_fourth':phase,'incoming_point_bound':bound})
            for depth in sorted(set([1,max(1,m//4),max(1,m//2)])):
                eta = np.array([min(1.0,i/depth,(m-i)/depth) for i in range(m+1)])
                av = (eta[:-1]**2+eta[1:]**2)/2
                lhs = float(np.sum(eta[1:-1]**2*hf)/radius+np.sum(av*(ell+ta)*np.einsum('ij,ij->i',es,es))/4)
                rhs = float(np.sum(np.diff(eta)**2*(np.sum(ds[:-1]**2,axis=1)+np.sum(ds[1:]**2,axis=1)))/0.06)
                maximum_excess = max(maximum_excess,lhs-rhs)
                require(lhs-rhs <= 1e-15+1e-8*max(lhs,rhs), "Caccioppoli on actual word and known minimum")
                b = m-depth
                if b <= depth: continue
                boundary = float(v[b-1]@ds[b]-v[depth]@ds[depth])
                delta_clock = float(np.sum(ell[depth:b]-ta[depth:b]))
                positive = float(np.sum(hf[depth:b-1])/radius+np.sum(ff[depth:b])/2)
                error = abs(delta_clock-boundary-positive)
                require(error <= 1e-11+1e-7*max(abs(delta_clock),abs(boundary),positive), "physical clock retains endpoint work")
                cases = [phase_case(j,min(j,b-1)) for j in range(depth,b+1)]
                clocks.append({'R':radius,'m':m,'depth':depth,'delta_actual_subrecord_clock':delta_clock,'retained_endpoint_work':boundary,'positive_bulk_cost':positive,'absolute_identity_error':error,'phase_quartic_sum':sum(x[0] for x in cases),'pointwise_bound_sum':sum(x[1] for x in cases)})
            records.append({'R':radius,'m':m,'all_next_collisions_enumerated_with_radius':10.0,'largest_roundoff_projection_to_original_circle':projection,'min_incidence':float(cosines.min()),'quartic_sum':float(np.sum(np.linalg.norm(ds,axis=1)**4)),'flight_energy_sum':float(ff.sum()),'minimum_identity':'m*(1-2R), with the disk separation attained on every edge','raw_positions':q.tolist(),'comparison_positions':y.tolist()})
    rng = np.random.default_rng(304307)
    for radius in [0.45,0.46,0.47]:
        for alpha,momentum in [(0.18,0.22),(0.67,-0.35),(1.13,0.51)]:
            q,o,v,ta,cosines,cps,projection = actual_path(radius,alpha,momentum,8)
            for i in range(8):
                transverse = np.array([-v[i,1],v[i,0]])
                for _ in range(12):
                    b0,b1 = float(rng.uniform(-0.009,0.009)),float(rng.uniform(-0.009,0.009))
                    y0 = q[i]-radius*cosines[i]*v[i]+b0*transverse
                    y1 = q[i+1]+radius*cosines[i+1]*v[i]+b1*transverse
                    if np.linalg.norm(y0-o[i]) > radius or np.linalg.norm(y1-o[i+1]) > radius: continue
                    beta = max(abs(float((y0-q[i])@transverse)),abs(float((y1-q[i+1])@transverse)))
                    require(2*beta < 0.06, "strict small-strip regime")
                    gq,gy = math.inf,math.inf
                    for pair,_ in offsets:
                        cp = (cps[i][0]+pair[0],cps[i][1]+pair[1])
                        if cp in [cps[i],cps[i+1]]: continue
                        zz = center(cp)
                        gq = min(gq,segdist(zz,q[i],q[i+1])-radius)
                        gy = min(gy,segdist(zz,y0,y1)-radius)
                    require(gy+1e-10 >= min(gq,0.06)-beta, "all-center closed-segment strip inequality")
                    strips.append({'R':radius,'flight':i,'beta':beta,'longitudinal_start':float((y0-q[i])@v[i]),'longitudinal_end':float((y1-q[i+1])@v[i]),'original_clearance':gq,'comparison_clearance':gy,'slack':gy-min(gq,0.06)+beta})
    radius,m = 0.47,5
    q = np.array([[radius if i%2 == 0 else 1-radius,0.0] for i in range(m+1)])
    yy = q.copy();yy[2,0] -= 0.1
    ds = yy-q
    eta = np.array([0,1,1,1,1,0],dtype=float)
    work = float(np.sum(np.diff(eta)**2*(np.sum(ds[:-1]**2,axis=1)+np.sum(ds[1:]**2,axis=1)))/0.06)
    contact = float(np.sum(eta[1:-1]**2*np.sum(ds[1:-1]**2,axis=1))/radius)
    require(contact > 0 and work == 0, "negative control rejects removing global minimality")
    require(any(x['retained_endpoint_work'] < 0 and abs(x['retained_endpoint_work']) > x['positive_bulk_cost'] for x in clocks), "negative control rejects deleting clock endpoint work")
    return {'status':'passed','scope':'Fresh finite floating diagnostics after recovery, not a continuum or probability proof certificate.','numpy_version':np.__version__,'exactly_identified_global_minimum_cases':len(records),'all_center_strip_cases':len(strips),'clock_phase_cases':len(clocks),'single_contact_phase_cases':len(points),'max_caccioppoli_excess':maximum_excess,'records':records,'strip_cases':strips,'clock_diagnostics':clocks,'point_phase_diagnostics':points,'negative_control':{'nonminimal_contact_work':contact,'cutoff_work':work,'correctly_rejected':True,'dropping_clock_endpoint_work_correctly_rejected':True}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--skip-numerics',action='store_true')
    parser.add_argument('--source-root',type=Path)
    args = parser.parse_args()
    result = {'schema':'A2-DYN-304-309-recovery-validation-v3','recovery_status':'Reconstructed validator; this is a fresh execution, not a retained old log.','proof_certificate':False,'raw_pointwise_llt_completed':False,'exact':exact_checks()}
    result['numerical'] = {'status':'not_run','reason':'explicit --skip-numerics'} if args.skip_numerics else numerical_diagnostics()
    candidates = [Path(__file__).parent,Path(__file__).parent.parent/'core',Path(__file__).parent/'core']
    source_root = args.source_root if args.source_root is not None else next((p for p in candidates if (p/'304_global_minimizer_boundary_localization.tex').exists()),Path(__file__).parent)
    sources = [Path(__file__)]+sorted(source_root.glob('30[4-9]_*.tex'))
    result['source_sha256'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    result['source_files_present'] = len(sources)-1
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','exact_counts':result['exact']['counts'],'numerical_status':result['numerical']['status'],'proof_certificate':False,'raw_pointwise_llt_completed':False},sort_keys=True))


if __name__ == '__main__':
    main()
