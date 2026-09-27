"""Exact finite regressions for revision 50; not a universal-proof oracle."""
from __future__ import annotations
import itertools
import json
import math
from fractions import Fraction as F
from typing import Sequence


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def bits(i: int) -> tuple[int, int, int]:
    return ((i >> 2) & 1, (i >> 1) & 1, i & 1)


def index(z: Sequence[int]) -> int:
    return 4*z[0] + 2*z[1] + z[2]


def permutation(a: int) -> list[int]:
    require(a in (0, 1), 'invalid command')
    return [index((bits(i)[1], bits(i)[2], bits(i)[0] ^ a)) for i in range(8)] + [8]


def apply(p: Sequence[int], x: Sequence[F]) -> list[F]:
    require(sorted(p) == list(range(len(x))), 'not a permutation')
    out = [F(0)]*len(x)
    for i, j in enumerate(p):
        out[j] = x[i]
    return out


def check_embedding(x: Sequence[F], commands: Sequence[Sequence[int]]) -> None:
    require(len(x) == 9, 'seed dimension')
    require(sum(t*t for t in x) == 1, 'unit seed')
    target = [F(1,10), F(2,5), F(4,5), F(2,5)]
    for word in itertools.product((0,1), repeat=3):
        y = list(x)
        for a in word:
            y = apply(commands[a], y)
        require(y[0] == F(200,357)*target[sum(word)], 'wrong orthogonal response')


def determinant3(a: Sequence[Sequence[F]]) -> F:
    return sum((F(1) if p in ((0,1,2),(1,2,0),(2,0,1)) else F(-1)) *
               a[0][p[0]]*a[1][p[1]]*a[2][p[2]]
               for p in itertools.permutations(range(3)))


def area(poly: Sequence[tuple[F,F]]) -> F:
    return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0]
                   for i in range(len(poly))))/2


def hull(points: Sequence[tuple[F,F]]) -> list[tuple[F,F]]:
    pts=sorted(set(points))
    def cross(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lo=[]; hi=[]
    for p in pts:
        while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:
            hi.pop()
        hi.append(p)
    return lo[:-1]+hi[:-1]


def main() -> None:
    vals=[F(1,10),F(2,5),F(4,5),F(2,5)]
    x=[F(200,357)*vals[sum(bits(i))] for i in range(8)]+[F(-157,357)]
    commands=[permutation(a) for a in (0,1)]
    check_embedding(x,commands)
    require(commands[0][commands[1][0]] != commands[1][commands[0][0]], 'commands commute')
    flatten=[[F(1,10),F(2,5),F(2,5),F(4,5)], [F(2,5),F(4,5),F(4,5),F(2,5)]]
    row=[F(1,4),F(3,5),F(3,5),F(3,5)]
    err=max(abs(flatten[i][j]-row[j]) for i in range(2) for j in range(4))
    require(err==F(1,5)<F(13,50), 'flattening witness')
    def cubic(t): return 500*t**3-375*t**2+540*t-124
    require(cubic(F(260362898747,10**12))<0<cubic(F(260362898748,10**12)), 'cubic bracket')
    require((-750)**2-4*1500*540<0, 'cubic monotonicity')
    require(all((3*r**3+3*r*r+r+2)%7 for r in range(7)), 'irreducibility')
    # Every coordinate of the circuit's exponent sum cancels, with multiplicity two at 111.
    left=[(0,1,1),(1,0,1),(1,1,0)]; right=[(0,0,0),(1,1,1),(1,1,1)]
    require(all(sum(e[k]==a for e in left)==sum(e[k]==a for e in right)
                for k in range(3) for a in (0,1)), 'circuit incidence')
    for d in range(2,21):
        orthants=sum(F(math.comb(d,k), math.factorial(k)*math.factorial(d-k)) for k in range(d+1))
        require(orthants==F(math.comb(2*d,d), math.factorial(d)), 'difference body sum')
        require(F(math.comb(2*d,d),2**d)>1, 'positive volume charge')
        # Barycentric coefficients of -v_i/d in the centered regular simplex.
        require(F(1+F(1,d),d+1)-F(1,d)==0, 'simplex asymmetry')
    triangle_checks=0
    for tri in [[(F(0),F(0)),(F(1),F(0)),(F(0),F(1))],
                [(F(-2),F(1)),(F(3),F(2)),(F(1),F(-4))],
                [(F(1,3),F(2,5)),(F(7,4),F(-2,3)),(F(-3,2),F(9,5))]]:
        diff=hull([(a[0]-b[0],a[1]-b[1]) for a in tri for b in tri])
        require(area(diff)==6*area(tri), 'triangle difference area')
        triangle_checks+=1
    require(F(3,2)**13<=200<F(3,2)**14, 'sufficient horizon threshold')
    # Four-state common transition rows are actual permutations for a noncommuting alphabet.
    seeds=[(1,0),(-1,0),(0,1),(0,-1)]
    mats=[((1,0),(0,1)),((-1,0),(0,-1)),((0,1),(1,0)),((1,0),(0,-1))]
    for mat in mats:
        image=[(mat[0][0]*a+mat[0][1]*b,mat[1][0]*a+mat[1][1]*b) for a,b in seeds]
        require(sorted(image)==sorted(seeds),'four-state transition')
    # Explicit rank-three Hankel submatrix (constant, coordinate means).
    r=F(1,10)
    require(determinant3([[F(1),r,F(0)],[F(1),-r,F(0)],[F(1),F(0),r]])!=0,'rank certificate')
    negative=[]
    def reject(name, fn):
        try:
            fn()
        except ValueError:
            negative.append(name)
        else:
            raise RuntimeError('negative control accepted: '+name)
    bad=list(x); bad[8]=0
    reject('unnormalized_seed', lambda: check_embedding(bad,commands))
    badcommand=[list(commands[0]),list(commands[1])]; badcommand[1][0]=badcommand[1][1]
    reject('nonbijective_command', lambda: check_embedding(x,badcommand))
    reject('word_order_drift', lambda: check_embedding(x,[commands[0],list(range(9))]))
    reject('premature_horizon_certificate',lambda:require(F(3,2)**13>200,'false threshold'))
    reject('false_flattening_optimum',lambda:require(err>=F(13,50),'flattening not globally tight'))
    reject('rank_two_substitution',lambda:require(determinant3([[1,1,1],[1,1,1],[1,1,1]])!=0,'rank lost'))
    reject('dimension_one_growth',lambda:require(F(math.comb(2,1),2)>1,'dimension excluded'))
    print(json.dumps({'status':'success','orthogonal_words_checked':8,'ambient_dimension':9,
        'exact_scaling':'200/357','cubic_bracket':['260362898747/1000000000000','260362898748/1000000000000'],
        'flattening_mean_error':'1/5','difference_body_dimensions':19,'triangle_checks':triangle_checks,
        'rho':'1/10','four_state_sufficient_horizon':14,'negative_controls_detected':negative,
        'scope':'Finite exact algebra and regression checks; universal statements are proved in the manuscript.'},sort_keys=True))


if __name__=='__main__':
    main()
