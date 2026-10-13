#!/usr/bin/env python3
"""Finite algebra and finite orbit identities only; no continuum certification."""
from fractions import Fraction as F
from math import comb, factorial
import cmath


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def partitions(n):
    if n == 0:
        yield []
        return
    for previous in partitions(n-1):
        yield previous + [[n-1]]
        for i in range(len(previous)):
            copy = [b[:] for b in previous]
            copy[i].append(n-1)
            yield copy


def finite_checks():
    e = F(67,1400)
    margins = {
        'analytic_disk': F(1,2)-e-F(2,5),
        'degree_19_remainder': 18*(F(1,2)-e)-8,
        'quartic_pair': F(2,5)-8*e,
        'quartic_connected': 1+F(1,5)-8*e,
        'fine_replacement': 3-F(3,2)-7*e,
        'mark_variation': 3-4*e,
        'stopping': F(1,4)-5*e,
        'gaussian_tail_power': 2*e,
        'kernel_prefactor': 4*e,
        'kernel_separation': F(1,2)+e,
    }
    expected = ['73/1400','97/700','3/175','143/175','233/200',
                '983/350','3/280','67/700','67/350','767/1400']
    require([str(v) for v in margins.values()] == expected, 'frequency exponent identity')
    rate=F(3,280)
    require(margins['quartic_pair']-rate == F(9,1400), 'quartic logarithmic slack')
    require(e>F(1,21)>F(1,50)>F(1,200), 'band not wider')
    require(2+4*F(-1,2)==0, 'raw Jacobian')
    require(F(1,4)-5*(e+F(1,100000))<rate, 'rate-balance negative control')

    shell_orders = []
    shell_cases = 0
    for q in [1,2,3,4,6,8,12,16,20]:
        p=max(2,(3*q)//4+1)
        exponent=F(3*q,2)-2*p
        require(exponent<0 and F(q,2*p)<1, 'nonsummable shell order')
        require(F(p)-F(q,2)+exponent/2==F(q,4), 'fourth-root shell scaling')
        shell_orders.append({'q':q,'p':p,'shell_exponent':str(exponent)})
        if q % 2 == 0:
            ratio=F(2)**int(exponent)
            for count in range(1,41):
                partial=sum((ratio**j for j in range(1,count+1)),F(0))
                require(partial<=ratio/(1-ratio), 'geometric shell bound')
                shell_cases+=1
    require(F(3*4,2)-2*3==0, 'critical-order negative control')
    require(F(3*2,2)-2*2==-1, 'fourth moments must suffice for L2')

    # Independent finite partition check of a marked moment identity.
    probs=[F(1,10),F(2,10),F(3,10),F(4,10)]
    xs=[F(-2),F(-1),F(1),F(2)]
    aa=[F(-1),F(2),F(0),F(3)]
    mx=sum(p*x for p,x in zip(probs,xs));ma=sum(p*a for p,a in zip(probs,aa))
    xs=[x-mx for x in xs];aa=[a-ma for a in aa]
    def block_moment(block):
        marked=0 in block
        power=len(block)-int(marked)
        return sum(p*(a if marked else 1)*x**power for p,x,a in zip(probs,xs,aa))
    def cumulant(block):
        result=F(0)
        for pi in partitions(len(block)):
            term=F((-1)**(len(pi)-1)*factorial(len(pi)-1))
            for b in pi:
                term*=block_moment([block[i] for i in b])
            result+=term
        return result
    moment_cases=0
    for d in range(1,7):
        cache={}
        result=F(0)
        for pi in partitions(d+1):
            term=F(1)
            for b in pi:
                key=tuple(b)
                if key not in cache: cache[key]=cumulant(b)
                term*=cache[key]
            result+=term
            marker=next(b for b in pi if 0 in b)
            if len(marker)>1 and all(len(b)>=2 for b in pi if b is not marker):
                require(len(pi)-1 <= (d-1)//2, 'marked partition block count')
        require(result==block_moment(list(range(d+1))), 'marked moment-cumulant inversion')
        moment_cases+=1
    for d in range(2,21):
        # A nonpair partition with no singleton has at most (d-2)/2
        # blocks for even d; odd d has at most (d-1)/2 blocks.
        def sizes(total, minimum=2):
            if total==0:
                yield []
            for j in range(minimum,total+1):
                for tail in sizes(total-j,j): yield [j]+tail
        for pi in sizes(d):
            if d%2:
                require(len(pi)<=(d-1)//2,'odd moment scaling')
            elif any(b!=2 for b in pi):
                require(len(pi)<=d//2-1,'even non-Gaussian scaling')

    # Exact finite invertible cyclic words test the pathwise recentering,
    # clock endpoints, four deterministic windows and shell partition.
    # These finite rotations are NOT used as mixing billiard models.
    orbit_cases=0
    N=8
    for mask in range(1,2**N-1):
        eta=[(mask>>i)&1 for i in range(N)]
        count=sum(eta); c=F(count,N)
        h=[1-F(a)/c for a in eta]
        section=[i for i,a in enumerate(eta) if a]
        def clock(y,j,sign):
            if not j:return 0
            seen=0
            for distance in range(1,(j+1)*N+1):
                seen+=eta[(y+sign*distance)%N]
                if seen==j:return distance
            raise RuntimeError('finite cyclic return not found')
        def sum_interval(y,left,right):
            return sum((h[(y+i)%N] for i in range(left,right)),F(0))
        def max_window(y,end,L):
            return max(abs(sum_interval(y,end,end+j)) for j in range(L+1))+max(abs(sum_interval(y,end-j,end)) for j in range(L+1))
        for n in (1,2,3):
            for k in range(n+1):
                r=(F(k)/c).__floor__();s=(F(n-k)/c).__floor__()
                for y in section:
                    back=clock(y,k,-1);forward=clock(y,n-k,1)
                    z=sum_interval(y,-back,forward);w=sum_interval(y,-r,s)
                    D=abs(back-r)+abs(forward-s)
                    visits=sum(eta[(y+i)%N] for i in range(-back,forward))
                    require(visits==n and z==back+forward-F(n)/c,'exact marked compensation')
                    L=max(1,D)
                    require(abs(z-w)<=max_window(y,-r,L)+max_window(y,s,L),'deterministic shell envelope')
                    b0=1
                    while b0*b0<n:b0+=1
                    if D>b0:
                        L=b0
                        while L<D:L*=2
                        require(L//2<D<=L,'disjoint dyadic shell')
                    orbit_cases+=1
    return {'exponents':{k:str(v) for k,v in margins.items()},
            'shell_orders':shell_orders,'geometric_shell_checks':shell_cases,
            'exact_marked_partition_cases':moment_cases,'finite_cyclic_orbit_cases':orbit_cases,
            'negative_controls':2,'fourth_moments_suffice_for_L2':True,
            'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
