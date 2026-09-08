#!/usr/bin/env python3
"""Exact original-model enclosure. No sampling or floating-point optimizer."""
from __future__ import annotations
from fractions import Fraction as F
from math import comb
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
import json
import hashlib
from pathlib import Path


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def moment(n: int) -> F:
    if n < 0:
        raise ValueError("negative power")
    return F(0) if n % 2 else F(1, 20**n * (n + 1))


def term(k: int) -> F:
    # (X-Z)^2 (X+Z)^(2k), independent symmetric uniform X,Z.
    return sum((F(comb(2*k, j)) * (
        moment(j+2)*moment(2*k-j)
        - 2*moment(j+1)*moment(2*k-j+1)
        + moment(j)*moment(2*k-j+2)
    ) for j in range(2*k+1)), F(0))


def rational(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def outward(x: F, rounding: str) -> str:
    with localcontext() as ctx:
        ctx.prec = 100
        return str((Decimal(x.numerator)/Decimal(x.denominator)).quantize(
            Decimal('1e-30'), rounding=rounding))


def integrate(poly: list[F]) -> F:
    return sum((c/F(i+1) for i, c in enumerate(poly)), F(0))


def multiply(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def main() -> None:
    a, K = F(1,240), 5
    k1, k2 = [F(1,4),F(1,2)], [F(3,4),-F(1,2)]
    H2 = [F(19,40),F(1,20)]
    check(integrate(k1)==integrate(k2)==F(1,2), "cell means")
    check(integrate(multiply(k1,[F(0),F(1)]))/integrate(k1)==F(7,12), "posterior cell 1")
    check(integrate(multiply(k2,[F(0),F(1)]))/integrate(k2)==F(5,12), "posterior cell 2")
    check(integrate(H2)==F(1,2), "unconditional target")
    check(F(9,20)*F(1,4)==F(9,80), "likelihood floor")
    # The exact implementing controller: accepted 1 -> label 1; otherwise 0.
    # Its one-step raw-cell rows are (probability label 0, label 1).
    A = [[F(1,2),F(1,2)],[F(1),F(0)]]
    q1 = [c/F(2) for c in k1]
    q0 = [F(1)-q1[0],-q1[1]]
    w1, w0 = integrate(q1), integrate(q0)
    b1, b0 = integrate(multiply(q1,H2)), integrate(multiply(q0,H2))
    check(w1==F(1,4) and w0==F(3,4), "label probabilities")
    check(b1/w1==F(121,240) and b0/w0==F(359,720), "centroid decoder")
    check(b1/w1-F(1,2)==a and b0/w0-F(1,2)==-a/3, "centered targets")
    eps=F(1,10)
    margin=F(1,2)-3*eps/2-(1+3*eps**2)/4
    check(margin==F(37,400) and margin>0, "all-encoder coverage margin")
    terms=[term(k) for k in range(K+1)]
    check(terms[0]==F(1,600), "second moment of X-Z")
    check(all(x>0 for x in terms), "positive geometric-series terms")
    JK=sum(terms,F(0))
    remainder=F(1,600)*F(1,10**(2*K+2))/(1-F(1,100))
    lo=a*a*(F(1,12)+JK/4)
    hi=lo+a*a*remainder/4
    check(lo>0 and hi>lo, "strict positive enclosure")
    check(hi-lo==a*a*F(1,2400)*F(1,10**(2*K+2))/(1-F(1,100)), "enclosure width")
    # A diagnostic of moment convergence, not the global coverage argument.
    next_lo=a*a*(F(1,12)+(JK+term(K+1))/4)
    check(lo<next_lo<hi, "nested partial sums")
    result={
        "schema":"theta-theory-v33-exact-continuous-instance-v1",
        "base_manuscript_commit":"e712437fe13cf29978715d3f16d825eadb450fea",
        "controlling_review_commit":"60c5b116a2c002dfd8056a351a87d7014d8c78e1",
        "arithmetic":"fractions.Fraction; no assert-based checks",
        "model":{"latent_prior":"uniform [0,1]","exponents":[0,1],
                 "commands":"independent uniform [9/20,11/20]^2",
                 "horizon":2,"memory_labels":2,"memory_charged_after_every_report":True,
                 "query_commands":[["1/2","1/2"],["9/20","11/20"]],
                 "query_weights":["1/2","1/2"],"likelihood_floor":"9/80"},
        "implementing_controller":{"initial_label":0,"update":{"accepted_1":1,"accepted_2":0,"failure":0},
            "depends_on_command":False,"persistent_public_seed":False,
            "raw_cell_rows_label_order_0_1":[list(map(rational,row)) for row in A],
            "decoder_H1":["1/2","1/2"],"decoder_H2":[rational(b0/w0),rational(b1/w1)]},
        "certificate":{"K":K,"J_partial_terms":list(map(rational,terms)),
            "J_partial_sum":rational(JK),"J_tail_upper":rational(remainder),
            "lower":rational(lo),"upper":rational(hi),"width":rational(hi-lo),
            "decimal_lower_outward":outward(lo,ROUND_FLOOR),
            "decimal_upper_outward":outward(hi,ROUND_CEILING),
            "coverage":"All Borel stochastic two-label encoders on the continuous cube, by Theorem thm:v33-exact-example and Corollary cor:v33-enclosure.",
            "coverage_margin":"37/400","general_controller_net_enumerated":False},
        "limits":"The executed arithmetic evaluates the proved certificate; it is not a formal proof assistant check of the continuum theorem.",
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
