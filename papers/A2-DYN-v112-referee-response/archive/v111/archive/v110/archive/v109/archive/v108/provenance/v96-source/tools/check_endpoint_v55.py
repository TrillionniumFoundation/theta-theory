#!/usr/bin/env python3
"""Finite algebra and abstract examples, not continuum proof certification."""
from fractions import Fraction as F
import math


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    alpha, beta, K = F(1,16), F(1), F(9)
    a, pc = alpha/K, 1+alpha/K
    require(a == F(1,144) and pc == F(145,144), 'endpoint algebra')
    regimes = 0
    for j in range(1,49):
        eps = F(1,2**(16*j)); leading=F(1,2**j)
        for m in range(2,161):
            local=leading+F(1,2**m); global_mass=m*m*eps
            require(min(local,global_mass) <= 2*leading, 'two-regime finite estimate')
            if m < j:
                require(global_mass <= leading, 'small-count branch')
            regimes += 1
    powers=[]
    for fraction in [F(1,8),F(1,4),F(1,2),F(3,4),F(7,8)]:
        q=1+a*fraction
        power=alpha*(pc-q)/(pc-1)
        require(power==9*(pc-q)>0,'physical remainder exponent')
        require(q<pc and q<2,'likelihood exponent')
        powers.append({'q':str(q),'width_power':str(power)})
    # Capped power tails on (0,1) have a uniform weak endpoint,
    # bounded subcritical moments and a divergent strong endpoint.
    for H in [2.,10.,1e3,1e8,1e20]:
        p=float(pc)
        for fraction in [.125,.5,.875]:
            q=1+(p-1)*fraction
            moment=H**(q-p)+p/(p-q)*(1-H**(q-p))
            require(moment<=p/(p-q)+1e-9,'capped subcritical moment')
        for L in [1.,math.sqrt(H),H]:
            tail=p/(p-1)*L**(1-p)-1/(p-1)*H**(1-p)
            require(tail<=p/(p-1)*L**(1-p)+1e-9,'weighted-tail identity')
    require(1+float(pc)*math.log(1e20)>40,'endpoint negative control')
    # beta>alpha is necessary for the asserted abstract two-regime lemma.
    for m in [16,32,64]:
        leading=F(1,2**(2*m))
        bad=min(leading+F(1,2**m),m*m*leading)
        require(bad/leading==m*m,'equal-width-exponent negative control')
    convexity=0
    for b in [1.01,1.5,2.,4.]:
        for x in [1e-6,.01,1.,10.,1e6]:
            second=x**(float(pc)-2)/math.log(math.e+x)**b
            require(second>0 and math.isfinite(second),'Young-function convexity')
            convexity+=1
        # Exact logarithmic model integral from T to infinity.
        T=math.e**4
        tail=(math.log(T)**(1-b))/(b-1)
        require(tail>0 and math.isfinite(tail),'endpoint modular tail')
    return {'two_regime_cases':regimes,'endpoint':str(pc),'physical_powers':powers,
            'convexity_samples':convexity,'negative_controls':2,
            'uses_complete_exponential_height_cap':False,
            'continuum_proof_certified':False}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
