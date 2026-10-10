#!/usr/bin/env python3
"""Exact rational primal/dual verification for an already supplied marked response.

This verifies a finite certificate, not raw-kernel hypotheses, gain correctness,
program implementability, or a global synthesis optimum. JSON rationals are
integers or strings such as "2/7". Floating-point input is deliberately rejected.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Any

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def rational(x: Any) -> F:
    require(isinstance(x, (int, str)) and not isinstance(x, bool),
            "Use integer or rational-string input, not floating point")
    return F(x)

def dot(a: list[F], b: list[F]) -> F:
    return sum((x*y for x,y in zip(a,b)), F(0))

def evaluate(P: list[list[F]], b: list[F], N: int,
             u: list[F], z: list[F]) -> dict[str, Any]:
    m=len(P)
    require(m>=1 and isinstance(N,int) and not isinstance(N,bool) and N>=1,
            "Positive state count and integer horizon required")
    require(all(len(row)==m for row in P) and len(b)==len(u)==len(z)==m,
            "Dimension mismatch")
    require(all(all(p>=0 for p in row) and sum(row)==1 for row in P),
            "P must be row-stochastic")
    residual=[b[i]-u[i]+dot(P[i],u) for i in range(m)]
    flux=[z[j]-sum((P[i][j]*z[i] for i in range(m)),F(0)) for j in range(m)]
    require(sum(abs(x) for x in z)<=1,"Dual l1 constraint violated")
    require(sum(abs(x) for x in flux)/2<=F(1,N),"Dual balance constraint violated")
    upper=max(abs(x) for x in residual)+F(max(u)-min(u),N)
    lower=max(F(0),dot(z,b))
    require(lower<=upper,"Exact weak duality failed")
    return {"status":"PASS","states":m,"N":N,"lower":str(lower),
            "upper":str(upper),"gap":str(upper-lower),
            "residual_inf":str(max(abs(x) for x in residual)),
            "oscillation":str(max(u)-min(u)),
            "dual_l1":str(sum(abs(x) for x in z)),
            "dual_balance_half_l1":str(sum(abs(x) for x in flux)/2),
            "scope":"exact supplied finite response only; not raw-kernel or continuum verification"}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    obj=json.loads(args.input.read_text())
    result=evaluate([[rational(v) for v in row] for row in obj["P"]],
                    [rational(v) for v in obj["b"]],obj["N"],
                    [rational(v) for v in obj["u"]],[rational(v) for v in obj["z"]])
    text=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end="")
if __name__=="__main__":
    main()
