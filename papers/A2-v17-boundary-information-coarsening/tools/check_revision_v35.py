#!/usr/bin/env python3
"""Finite R1 diagnostics and source-preservation checks; not a proof or PDF build."""
from __future__ import annotations
from decimal import Decimal, localcontext, ROUND_CEILING
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CHECKS: list[str] = []


def require(condition: bool, name: str) -> None:
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def source_checks() -> dict:
    rel = 'article/18a_vector_boundary_information_v26.tex'
    before = (ROOT/'history/v34'/rel).read_bytes()
    after = (ROOT/rel).read_bytes()
    require(blob(before) == 'c036b730155d55420b92980a20abd40812ba7811',
            'Exact inherited vector source retained')
    require(blob(after) == '8ff3ce7334954d6544555e9867a12fa805ca5ea0',
            'R1 source matches the tested complete replacement')
    claims = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}', re.S)
    old_claims = [m.group(0) for m in claims.finditer(before.decode())]
    new_claims = [m.group(0) for m in claims.finditer(after.decode())]
    require(bool(old_claims) and old_claims == new_claims,
            'Every theorem and lemma statement is byte-for-byte unchanged')
    main = (ROOT/'main.tex').read_text()
    old_main = (ROOT/'history/v34/main.tex').read_text()
    inputs = re.compile(r'\\input\{([^}]+)\}')
    active = inputs.findall(main)
    require(active == inputs.findall(old_main) and len(active) == 52,
            'All 52 direct inputs remain in their inherited order')
    require('article/18a2_likelihood_tilting_moments_v34' in active,
            'The v34 likelihood-tilting and risk proof remains active')
    abstract = re.compile(r'\\begin\{abstract\}.*?\\end\{abstract\}', re.S)
    require(abstract.search(main).group(0) == abstract.search(old_main).group(0),
            'The complete abstract is preserved exactly')
    auxiliary = (ROOT/'article/99_auxiliary_compendium_v19.tex').read_bytes()
    require(blob(auxiliary) == 'a596f344cd660eeaacc8e4e3eb21a0cb39610a9e'
            and len(inputs.findall(auxiliary.decode())) == 36,
            'All 36 auxiliary inputs are retained by exact compendium blob')
    require('A2 revision 35' in main and 'A2 revision 34' not in main,
            'The active native entry identifies revision 35')
    return {'unchanged_claims': len(old_claims), 'direct_inputs': len(active),
            'auxiliary_inputs': 36, 'vector_blob': blob(after)}


def exact_checks() -> dict:
    # Centered fourth moment for independent, unequal Bernoulli variables.
    probabilities = (F(1,3), F(2,5), F(3,7))
    mean = sum(probabilities)
    actual = F(0)
    for outcome in product((0,1), repeat=3):
        mass = F(1)
        for x,p in zip(outcome,probabilities):
            mass *= p if x else 1-p
        actual += mass*(sum(outcome)-mean)**4
    variances = [p*(1-p) for p in probabilities]
    fourths = [p*(1-p)**4+(1-p)*p**4 for p in probabilities]
    formula = sum(fourths)+6*sum(variances[i]*variances[j]
                              for i in range(3) for j in range(i+1,3))
    require(actual == formula, 'Exact centered independent-sum fourth moment')
    require(actual <= 3*sum(variances)**2+sum(fourths),
            'Exact fourth-moment upper bound')
    # Algebra of the normalized moving-support scalar density.  Treat
    # log(1/q) as a scalar variable here: this checks a polynomial identity.
    for q in (F(1,8), F(1,16), F(1,32)):
        ell = F(7,3)
        a = 2*(q-q*q)
        b = 2*(ell-2+2*q)
        for theta in (F(-1,100), F(1,100)):
            exact = (a+theta*b)/(1-theta)**2
            expansion = a+theta*(b+2*a)
            remainder = theta**2*(3*a+2*b-theta*(b+2*a))/(1-theta)**2
            require(exact-expansion == remainder,
                    f'Exact alternative-mean Taylor remainder q={q}, theta={theta}')
    return {'centered_fourth_moment': str(actual),
            'centered_formula': str(formula)}


def rate_checks() -> list[dict]:
    rows = []
    with localcontext() as context:
        context.prec = 90
        d = Decimal
        previous_error = None
        for k in (64,256,1024,4096):
            delta = d(2)**(-k)
            ell = -delta.ln()
            l = ell.sqrt().sqrt()
            q = delta*l
            logq = -q.ln()
            p = d(1)/7
            n = (1/(p*delta*delta*ell)).to_integral_value(rounding=ROUND_CEILING)
            budget = n*p*delta*delta*ell
            quantities = (n*p*delta*q, n*p*delta*delta*logq,
                          n*p*delta**4/q**2)
            identities = (budget*l/ell, budget*(1-ell.ln()/(4*ell)),
                          budget/ell/ell.sqrt())
            require(all(abs(x-y) <= d('1e-80')*max(d(1),abs(x))
                        for x,y in zip(quantities,identities)),
                    f'Three collar-rate identities at delta=2^-{k}')
            means = []
            for h in (-2,-1,0,1,2):
                theta = delta*h
                one_mark_mean = 2*((q-q*q)+theta*(logq-2+2*q))/(1-theta)**2
                means.append(n*p*delta*one_mark_mean)
            error = max(abs(mu-2*h) for mu,h in zip(means,(-2,-1,0,1,2)))
            require(previous_error is None or error < previous_error,
                    f'Exact scalar-model alternative-mean diagnostic at k={k}')
            previous_error = error
            rows.append({'k':k,'max_mean_error_on_five_point_grid':str(+error),
                         'truncated_mean_budget':str(+quantities[0]),
                         'second_moment_budget':str(+quantities[1]),
                         'fourth_moment_budget':str(+quantities[2])})
    return rows


def main() -> None:
    sources = source_checks()
    exact = exact_checks()
    rates = rate_checks()
    print(json.dumps({'status':'passed','scope':__doc__, 'source_checks':sources,
                      'exact_diagnostics':exact,'rate_diagnostics':rates,
                      'check_count':len(CHECKS),'checks':CHECKS},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
