#!/usr/bin/env python3
"""Independent exact arithmetic for author drafts 338--339, not an orbit proof."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def frac(x):
    return {'numerator':x.numerator,'denominator':x.denominator,'decimal_for_navigation':float(x)}


def verify(physical, analytic):
    # Reconstruct each constant from the inherited geometric formula rather
    # than using the proposed large rational numerator as an input.
    rmin,rmax,tmin = F(9,20),F(47,100),F(3,50)
    sigma = 1/(1+2*tmin/rmax)
    kmin,kmax = 1/rmax,1/rmin
    E = 1/(kmin*tmin)
    C0 = (tmin+rmax)/(2*tmin)
    critical_U = kmax+1/tmin
    h0=F(1,200)
    section_area = 4*(2*h0)**2 + (2*F(3,50))*(2*F(3,20))
    cstar_times_pi = section_area/4
    endpoint_horizontal_minimum_lower = 2*F(49,100)/(1+F(49,100)**2)-h0
    assert sigma == F(47,59) and 0 < sigma < 1
    assert E == F(47,6) and C0 == F(53,12)
    assert critical_U == F(170,9)
    assert cstar_times_pi == F(91,10000)
    assert endpoint_horizontal_minimum_lower > h0 > 0
    # 338: the two possible product estimates give the smaller power of
    # sigma, i.e. sigma**max, since sigma<1. The complete counts are the
    # five original rectangles, not an enlarged or truncated section.
    side_counts = {'interior_horizontal':5*2,'interior_vertical':5*2,
                   'endpoint_vertical':2*5*2,'endpoint_horizontal':2*5*2}
    assert side_counts == {'interior_horizontal':10,'interior_vertical':10,
                           'endpoint_vertical':20,'endpoint_horizontal':20}

    # 339: lower bounds for the actual radical constants, proved by
    # squaring positive quantities, are sufficient for exact arithmetic.
    clow,llow,L = F(2,5),F(9,50),F(47,6)
    assert clow**2 < F(19,100)
    assert llow**2 < F(81*19,40000)
    jstar = max(F(1),rmax/(2*tmin)*(sigma+1/sigma))
    C3 = rmax+3*rmax**2/tmin+3*rmax**3/tmin**2
    CF = 8*C3*jstar**3*(1+sigma)**3/(1-sigma**3)
    Cc = jstar*(1+rmax/tmin*(1+1/sigma))
    Comega_bar = 2*rmax*jstar*(1+sigma)/(tmin*(1-sigma))+4*Cc/clow+2*Cc
    E0 = rmax**2/tmin
    E1_bar = 500*rmax*Comega_bar
    Q_bar = L/llow
    Kbar = F(9,10)*rmax*Q_bar*(E1_bar/llow+E0*CF/llow**2)
    assert jstar == F(2845,354)
    assert CF == F(16132182255644462065,3378910095288)
    assert Comega_bar == F(18557935,6372)
    assert Kbar == F(396358110646634302372735325,39411607351439232)
    threshold = llow/2
    assert Kbar*sigma**112 < threshold
    assert Kbar*sigma**111 >= threshold
    # Nontrivial exact-positive numerator of the long-time certificate.
    gap = threshold-Kbar*sigma**112
    assert gap.numerator > 0
    # The integral over |v|<=kappa*|b|*sigma**(m-1) is 2 arctan,
    # the trace kernel costs two orientations, and the label jump costs1.
    atom_multiplier = 2*2*1*side_counts['endpoint_horizontal']
    assert atom_multiplier == 80
    source_files = []
    for p in [physical,analytic]:
        data=p.read_bytes()
        source_files.append({'path':p.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    return {
        'status':'PASS','purpose':'Internal author reconstruction arithmetic only; not a mathematical theorem, sampled physical verification, external report, or independent human review.',
        'draft_identities':source_files,
        'section_normalization':{'area':frac(section_area),'cstar_times_pi':frac(cstar_times_pi),
            'critical_CJ_times_cstar':frac(critical_U/2),
            'Fcs':frac(L/(4*cstar_times_pi*rmin**2))},
        'section_fan_constants':{'sigma':frac(sigma),'E':frac(E),'C0':frac(C0),
            'critical_U':frac(critical_U),'side_counts':side_counts,
            'nonzero_endpoint_momentum_lower_bound':frac(endpoint_horizontal_minimum_lower)},
        'endpoint_constants':{k:frac(v) for k,v in {'Jstar':jstar,'C3':C3,'CF':CF,'Cc':Cc,
            'Comega_bar':Comega_bar,'E0':E0,'E1_bar':E1_bar,'Q_bar':Q_bar,'Kbar':Kbar}.items()},
        'threshold_certificate':{'sufficient_collision_count':114,'threshold':frac(threshold),
            'Kbar_sigma112':frac(Kbar*sigma**112),'Kbar_sigma111':frac(Kbar*sigma**111),
            'positive_exact_gap':frac(gap),'m113_certified_by_same_bound':False,
            'all_m_ge114_reason':'0<sigma<1, so the bound decreases after the exact m=114 integer comparison.'},
        'endpoint_atom_multiplier_without_AV_Fcs_Cmom_arctan':atom_multiplier,
        'not_certified_by_this_script':['canonical source growth theorem','trace collar existence',
            'all-word kernel bound','finite physical side decomposition','source representative argument',
            'full raw pointwise local limit theorem','four-coordinate raw inverse'],
    }


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--physical',type=Path,required=True)
    ap.add_argument('--analytic',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    result=verify(args.physical,args.analytic)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'sufficient_collision_count':114,
                      'm113_certified_by_same_bound':False,'normalization_verified':True}))
