#!/usr/bin/env python3
"""Finite algebra and norm regressions, not billiard proof certification."""
from fractions import Fraction as F
from itertools import product
import math
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def local_norm(v, h):
    return max(sum(abs(v[(i+j) % len(v)]) for j in range(h)) for i in range(len(v)))


def finite_checks():
    R, a, phi, dx, dy = sp.symbols('R a phi dx dy', real=True)
    foot = dx*sp.cos(a-phi)+dy*sp.sin(a-phi)-R*sp.cos(phi)
    distance = -dx*sp.sin(a-phi)+dy*sp.cos(a-phi)-R*sp.sin(phi)
    require(sp.simplify(sp.diff(distance, a)/R+sp.cos(phi)+foot/R)==0,
            'arclength derivative')
    require(sp.simplify(sp.diff(distance, phi)-foot)==0, 'angle derivative')
    require(sp.simplify(foot**2+distance**2-(dx-R*sp.cos(a))**2-(dy-R*sp.sin(a))**2)==0,
            'orthogonal foot identity')
    gap_squared=F(53,100)**2-F(48,100)**2
    require(gap_squared>F(22,100)**2, 'uniform positive foot')
    require(F(1,4)*F(1,16)==F(1,64), 'depth exponent')
    require(F(1,12)*F(1,16)==F(1,192), 'ordered bandwidth exponent')
    marked=0
    for radius in (.45,.46,.47):
        for cx,cy in ((1.,0.),(.5,math.sqrt(3)/2),(-.5,math.sqrt(3)/2)):
            for ia in range(80):
                aa=2*math.pi*ia/80
                for ip in range(81):
                    pp=-math.pi/2+math.pi*ip/80
                    ll=cx*math.cos(aa-pp)+cy*math.sin(aa-pp)-radius*math.cos(pp)
                    zz=-cx*math.sin(aa-pp)+cy*math.cos(aa-pp)-radius*math.sin(pp)
                    if ll>0 and radius<=abs(zz)<=radius+.009:
                        require(ll>=math.sqrt(float(gap_squared))-1e-12, 'sample foot lower bound')
                        for slope in (-3.,-8.):
                            deriv=-math.cos(pp)-ll/radius+ll*slope
                            require(deriv<=-math.sqrt(float(gap_squared))/.47+1e-10,
                                    'sample stable transversality')
                        marked+=1
    require(marked>0, 'empty geometry regression')
    x=F(9,10); depth_cases=0
    for m in range(2,81):
        contacts=[min(j,m-j) for j in range(m+1)]
        flights=[min(j,m-1-j) for j in range(m)]
        require(len(contacts)+len(flights)==2*m+1, 'physical mark count')
        require((2*m+1)*m*m<=3*m**3, 'summed spectral error')
        require(sum(x**d for d in contacts+flights)<=4/(1-x), 'full depth sum')
        for J in (0,m//4,m//2):
            require(sum(x**d for d in contacts+flights if d>J)<=4*x**(J+1)/(1-x),
                    'physical depth tail')
            depth_cases+=1
    # The previous-flight variable must be placed at j+1, not j.
    marker_cases=0
    for bits in product((0,1),repeat=7):
        shifted=(0,)+bits
        for j in range(7):
            require(shifted[j+1]==bits[j], 'previous-flight chronological mark')
            marker_cases+=1
    kernels=((F(-1,4),F(3,2),F(-1,4)),(F(1,3),F(1,3),F(1,3)))
    vectors=((F(1),F(-2),F(3),F(0),F(-1)),(F(0),F(0),F(9),F(0),F(0)))
    convolution_cases=0
    for k,v in product(kernels,vectors):
        require(sum(k)==1,'kernel mass')
        conv=[sum(k[j]*v[(i-j)%len(v)] for j in range(len(k))) for i in range(len(v))]
        for h in range(1,len(v)+1):
            require(local_norm(conv,h)<=sum(abs(z) for z in k)*local_norm(v,h),
                    'local convolution inequality')
            convolution_cases+=1
    conditional_cases=0
    for f in ((F(1),F(2),F(3)),(F(0),F(1),F(4))):
        for raw in ((F(-1),F(1),F(3)),(F(2),F(2),F(1))):
            g=tuple(max(F(0),z) for z in raw); ff=sum(f); gg=sum(g)
            E=sum(abs(u-v) for u,v in zip(f,g))
            require(E<=sum(abs(u-v) for u,v in zip(f,raw)), 'positive part domination')
            tv=sum(abs(u/ff-v/gg) for u,v in zip(f,g))/2
            require(tv<=E/ff, 'conditional normalization')
            conditional_cases+=1
    # Negative controls reject inferences not made by the article.
    n=64
    spike_mass=F(1,n); spike_height=n
    require(spike_mass<1 and spike_height>1, 'small mass does not imply small height')
    require(any((0,)+bits != bits+(0,) for bits in product((0,1),repeat=3)),
            'wrong-side mark must be distinguishable')
    require(sum(abs(z) for z in kernels[0])>sum(kernels[0]),
            'signed kernel norm must not be replaced by its mass')
    return {'symbolic_geometric_identities':3,'clearance_grid_points':marked,
            'depth_cases':depth_cases,'chronological_mark_cases':marker_cases,
            'signed_convolution_cases':convolution_cases,'conditional_normalization_cases':conditional_cases,
            'weak_gain':'1/8','local_amplitude_gain':'1/16','depth_gain':'1/64',
            'ordered_correction_gain':'1/192','summed_remainder':'m^3 rho^(m/2)',
            'negative_controls':3,'continuum_proof_certified':False}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
