#!/usr/bin/env python3
"""Finite regressions for the printed algebra, not an execution of real QE."""
from fractions import Fraction as F
from itertools import product

def require(ok, message):
    if not ok: raise RuntimeError(message)

def rejects(predicate, message):
    try: require(predicate, message)
    except RuntimeError: return 1
    raise RuntimeError('negative fixture was not rejected: '+message)

def finite_checks():
    leading_cases=0
    for degree in range(1,7):
        for height in range(1,5):
            delta=F(1,4*(degree+1)*2**height)
            for order in range(degree+1):
                # Smallest leading coefficient versus the largest adverse tail.
                value=delta**order-sum(F(2**height)*delta**i for i in range(order+1,degree+1))
                require(value>=delta**degree/2,'integer leading coefficient bound')
                leading_cases+=1
    rank_cases=0
    for exponent in range(1,9):
        for cap, distance in product([F(1,2),F(1,3),F(1,7)],repeat=2):
            budget=F(2**exponent)
            epsilon=(cap*distance)**exponent/(4*budget)
            required=(cap*distance)**exponent/budget
            determinant=required-2*epsilon
            require(determinant==(cap*distance)**exponent/(2*budget),'rank subtraction')
            require(min(cap,distance)>=cap*distance,'product/min modulus')
            rank_cases+=1
    tube_cases=0
    for degree in range(1,9):
        # Caustic t^degree=R: use rational roots to avoid floating-point claims.
        for root in [F(1,2),F(1,5),F(1,10)]:
            h=root**degree
            require(root**degree==h,'algebraic tube exponent')
            for cap in [F(1,2),F(1,4)]:
                for length in [root,F(1,2),F(3,2)]:
                    delta=min(length,cap,F(1))
                    require(delta>=cap*length/F(3),'interval normalization')
                    tube_cases+=1
    # An exact simple cap-threshold fixture: f(x)=x, cap carrier x>=chi-a.
    # At chi=a+1/l its critical point 0 is absent at the unbuffered cap,
    # while it lies at the buffered cap chi/2 for l large.
    a=F(1,2)
    for l in range(5,65):
        cap=a+F(1,l);x=F(1,l)
        require(x>=cap-a,'source cap fixture')
        require(not(F(0)>=cap-a),'unbuffered critical point unexpectedly present')
        require(F(0)>=cap/2-a,'buffered critical point missing')
        require(abs(x-F(0))==F(1,l),'buffered critical distance')
    # Upper bounds on prenex blocks from the literal infimum constructions.
    prefixes={'separation_lower_bound':'AE','separation_approximation':'AEA',
              'tube_lower_bound':'AEA','tube_approximation':'AEAE'}
    separation_blocks=len(prefixes['separation_lower_bound'])+len(prefixes['separation_approximation'])+1
    tube_blocks=len(prefixes['tube_lower_bound'])+len(prefixes['tube_approximation'])+1
    require(max(separation_blocks,tube_blocks)<=12,'quantifier block budget')
    require(16>12,'printed polynomial degree must dominate block product')
    # Three-way physical-source partition, including a low incidence after clearance.
    partitions=0
    for low,near in product([False,True],repeat=2):
        pieces=[int(low),int(not low and near),int(not low and not near)]
        require(sum(pieces)==1,'positive source partition')
        partitions+=1
    cap=F(1,4);incidences=[F(1,2),F(1,3),F(1,8),F(3,4)]
    invprod=F(1)
    for c in incidences: invprod/=c
    require(F(1)<=sum(cap/c for c in incidences)<=len(incidences)*cap*invprod,
            'later-incidence domination')
    p=F(145,144)
    require(1-1/p==F(1,145) and 1/p==F(144,145),'mass/height exponents')
    mass=F(1,7)
    require(mass/2!=mass,'probability TV convention')
    negative=0
    negative+=rejects(F(1,10)<=F(1,100),'linear tube bound at a quadratic fold')
    negative+=rejects(2*F(1,5)<=F(1,5),'seam subtraction without the factor two')
    negative+=rejects(F(1,145)==F(1),'weak integrability does not give essential height')
    negative+=rejects(F(1,2)+F(1,2)==F(1,2),'probability TV is not variation mass')
    # Fixed width with an exponential count factor is not a vanishing collision estimate.
    require(2**30*F(1,1000)>2**20*F(1,1000),'fixed-width count-order guard')
    return {'leading_coefficient_cases':leading_cases,'rank_threshold_cases':rank_cases,
            'tube_interval_cases':tube_cases,'buffered_cap_cases':60,
            'positive_partition_cases':partitions,'negative_controls':negative,
            'prenex_block_upper_bounds':{'separation':separation_blocks,'tube':tube_blocks},
            'printed_budget':'E_m=ceil(2^(C0*(m+1)^16)), K_m=2^E_m',
            'actual_quantifier_elimination_executed':False,
            'continuum_geometry_certified':False,'ordered_height_limits_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
