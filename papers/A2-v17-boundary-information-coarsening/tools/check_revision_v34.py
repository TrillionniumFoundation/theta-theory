#!/usr/bin/env python3
"""Finite algebra and source-preservation checks; not a proof or full-main build."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import re


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def dot(a, b):
    return sum((x*y for x,y in zip(a,b)), F(0))


def matmul(a, b):
    return [[dot(row,col) for col in zip(*b)] for row in a]


def check() -> dict:
    out = {'scope': 'Finite exact identities, numerical rate illustrations, and direct-input preservation only; no automated proof certification and no native-main build.'}
    # A single reference coupling generates both kernels for every parameter.
    pi = [[F(2,5),F(0)],[F(1,10),F(1,2)]]
    mx = [sum(row) for row in pi]
    my = [sum(col) for col in zip(*pi)]
    kxy = [[pi[i][j]/mx[i] for j in range(2)] for i in range(2)]
    kyx = [[pi[i][j]/my[j] for i in range(2)] for j in range(2)]
    records=[]
    for x,y in [([F(1),F(1)],[F(1),F(1)]),
                ([F(1,4),F(3,2)],[F(1,2),F(3,2)]),
                ([F(7,4),F(1,2)],[F(3,2),F(1,2)])]:
        require(dot(x,mx)==dot(y,my)==1,'likelihood normalization')
        fx=[sum(mx[i]*x[i]*kxy[i][j] for i in range(2)) for j in range(2)]
        fy=[sum(my[j]*y[j]*kyx[j][i] for j in range(2)) for i in range(2)]
        forward=sum(abs(fx[j]-my[j]*y[j]) for j in range(2))/2
        reverse=sum(abs(fy[i]-mx[i]*x[i]) for i in range(2))/2
        bound=sum(pi[i][j]*abs(x[i]-y[j]) for i in range(2) for j in range(2))/2
        require(forward<=bound and reverse<=bound,'coupling total-variation bound')
        records.append({'forward_tv':str(forward),'reverse_tv':str(reverse),'bound':str(bound)})
    out['parameter_independent_coupling']=records
    # Unit prelimit means alone are insufficient if the limiting mean is lost.
    out['normalization_necessity']=[{'n':n,'prelimit_mean':1,'tv':str(1-F(1,n)),
                                  'limiting_mean':0} for n in [2,10,100]]
    v=[F(1),F(2)]; norm=dot(v,v)
    j=[[a*b for b in v] for a in v]
    jp=[[x/(norm*norm) for x in row] for row in j]
    projection=[[x/norm for x in row] for row in j]
    require(matmul(jp,j)==projection,'identifiable projection')
    require(matmul(matmul(jp,j),jp)==jp,'singular Gaussian covariance')
    out['singular_information']={'rank':1,'projection_verified':True,'covariance_verified':True}
    out['collar_budgets']=[]
    for m in [2,4,8,16]:
        t=m**4
        out['collar_budgets'].append({'log_inverse_delta':t,'mean_term':str(F(1,m**3)),
           'fourth_term':str(F(1,m**6)),'second_term':1-math.log(m)/t})
    nb=[]
    r=F(12,25)
    for k in [1,2,3,4]:
        affinity=F(12,13)**k
        partial=sum((F(math.comb(t-1,k-1))*r**t for t in range(k,201)),F(0))
        require(0<=affinity-partial<F(1,10**40),'negative-binomial affinity tail')
        nb.append({'k':k,'affinity':str(affinity),'tail_less_than':'1e-40'})
    for p in [F(1,10),F(9,25),F(16,25)]:
        for k in [1,7]:
            mean_t=F(k)/p; var_t=F(k)*(1-p)/(p*p)
            require((k-p*mean_t)/(1-p)==0,'NB centered score')
            require(p*p*var_t/(1-p)**2==F(k)/(1-p),'NB score information')
            require(-(mean_t-k)*p/(1-p)**2==-F(k)/(1-p),'NB expected Hessian')
    out['negative_binomial']=nb
    for n in range(3,21):
        z=F(n+1); c=(z*z+1)/(z*z-1); s=2*z/(z*z-1); r=F(3,2)**n
        require(c*c-(r*s)*(s/r)==1,'last-jet determinant')
    out['last_jet_determinants']={'orders':list(range(3,21)),'all_exactly_one':True,
        'limitation':'Does not prove nonlinear jet filtration; that is a manuscript argument.'}
    def action(u): return u*u/4+u**3/10+u**4/20
    def amplitude(u): return 1+u/5+u*u/9
    def density(u,v): return amplitude(u)*amplitude(v)*(1-action(u)-action(v))
    def ratio(u,v): return density(u,v)*density(F(0),F(0))/(density(u,F(0))*density(F(0),v))
    anchor=F(1,4); ta=action(anchor)/(1-action(anchor))
    require(1-ratio(anchor,anchor)==ta*ta and ta>0,'positive fixed anchor')
    for u in [F(-1,4),F(-1,8),F(0),F(1,8),F(1,4)]:
        tu=(1-ratio(u,anchor))/ta
        require(tu/(1+tu)==action(u),'asymmetric action inverse')
        require(density(u,F(0))/density(F(0),F(0))*(1+tu)==amplitude(u),'amplitude inverse')
    out['four_density_inverse']={'signed_points':5,'exact':True,'limitation':'Algebraic density example; no billiard realization is inferred.'}
    R=F(47,100); T=F(11,100); gap=F(3,50)
    require(T<2*gap,'three-collision exclusion budget')
    require((1-2*R-T*T)/(2*R*T)==F(479,1034),'complete short-flight transversality')
    require(F(9,10)*F(9,1000)*F(1,4000000)>F(1,10**9),'two-collision witness')
    area_lower=F(43,50)-F(22,7)*R*R
    require(area_lower>F(4,25) and 2*R*T/F(4,25)<F(13,20),'zero-collision positivity budget')
    out['native_companion_rational_checks']='passed'
    source=Path(__file__).resolve().parents[1]
    base=source/'history/v33/main.tex'
    current=source/'main.tex'
    if base.is_file() and current.is_file():
        old=base.read_text(); new=current.read_text()
        inp=re.compile(r'\\input\{([^}]+)\}')
        a=inp.findall(old); b=inp.findall(new)
        require([x for x in b if x in a]==a,'inherited direct inputs removed or reordered')
        require([x for x in b if x not in a]==['article/18a2_likelihood_tilting_moments_v34'],'unexpected active input change')
        abstract=re.compile(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',re.S)
        require(abstract.search(old).group(1)==abstract.search(new).group(1),'abstract altered')
        out['direct_source_preservation']={'old_inputs':len(a),'new_inputs':len(b),
              'inherited_sequence_unchanged':True,'abstract_byte_identical':True,
              'recursive_graph_execution':'not performed by this check'}
    else:
        raise RuntimeError('Preserved v33 main and current main are required')
    return out


if __name__=='__main__':
    print(json.dumps(check(),indent=2,sort_keys=True))
