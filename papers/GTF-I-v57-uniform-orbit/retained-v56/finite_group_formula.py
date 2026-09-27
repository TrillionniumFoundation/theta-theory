"""Emit the explicit finite-group stationary decision as QF_NRA SMT-LIB.

This is a formula compiler, not a claim to run a complete real-algebraic solver.
Input: multiplication (square table), identity (index), k, epsilon (rational),
targets[seed][query][group_element][category]. A generating alphabet is not
needed: all group elements are explicitly tabulated. Example generation is
exercised by check_revision.py.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any


def rational(value: Any) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError('Rationals must be integers or exact strings, not floats/bools')
    return Fraction(value)


def validate(data: dict) -> tuple[list[list[int]], int, int, Fraction, list, list[int]]:
    table=data['multiplication']; e=data['identity']; k=data['k']
    n=len(table)
    if not n or not isinstance(e,int) or isinstance(e,bool) or not 0<=e<n:
        raise ValueError('Invalid group identity')
    if not isinstance(k,int) or isinstance(k,bool) or k<1:raise ValueError('Invalid label bound')
    if any(len(row)!=n or any(type(x) is not int or not 0<=x<n for x in row) for row in table):
        raise ValueError('Invalid multiplication table')
    if any(table[e][x]!=x or table[x][e]!=x for x in range(n)):raise ValueError('Identity law failed')
    for a in range(n):
        if not any(table[a][b]==e==table[b][a] for b in range(n)):raise ValueError('Inverse law failed')
        for b in range(n):
            for c in range(n):
                if table[table[a][b]][c]!=table[a][table[b][c]]:raise ValueError('Associativity failed')
    eps=rational(data['epsilon'])
    if eps<0:raise ValueError('Negative error')
    source=data['targets']
    if not source or not source[0]:raise ValueError('Nonempty seed and query sets required')
    jcount=len(source[0]);dims=[];targets=[]
    for j in range(jcount):
        if len(source[0][j])!=n or not source[0][j][0]:raise ValueError('Missing target')
        dims.append(len(source[0][j][0]))
    for seed in source:
        if len(seed)!=jcount:raise ValueError('Query count mismatch')
        out=[]
        for j,query in enumerate(seed):
            if len(query)!=n:raise ValueError('Group target count mismatch')
            rows=[]
            for row in query:
                if len(row)!=dims[j]:raise ValueError('Category count mismatch')
                vals=[rational(x) for x in row]
                if any(x<0 for x in vals) or sum(vals)!=1:raise ValueError('Illegal categorical target')
                rows.append(vals)
            out.append(rows)
        targets.append(out)
    return table,e,k,eps,targets,dims


def smt_number(q: Fraction) -> str:
    if q<0:return '(- '+smt_number(-q)+')'
    return str(q.numerator) if q.denominator==1 else f'(/ {q.numerator} {q.denominator})'


def add(values) -> str:
    v=list(values)
    return '0' if not v else v[0] if len(v)==1 else '(+ '+' '.join(v)+')'


def compile_formula(data: dict) -> tuple[str,dict]:
    table,e,k,eps,targets,dims=validate(data);n=len(table);ns=len(targets)
    if k>=ns*n:
        return '; Exact seed-group construction meets the label bound.\n(set-logic QF_NRA)\n(assert true)\n(check-sat)\n', {'direct_exact_upper_bound':ns*n,'variables':0,'constraints':1}
    lines=['; Real stationary realization, not rational-factor feasibility.','(set-logic QF_NRA)'];variables=0;constraints=0
    def var(name):
        nonlocal variables
        lines.append(f'(declare-fun {name} () Real)');variables+=1
        return name
    def claim(expr):
        nonlocal constraints
        lines.append(f'(assert {expr})');constraints+=1
    P=[[[var(f'P_{g}_{i}_{j}') for j in range(k)] for i in range(k)] for g in range(n)]
    E=[[var(f'E_{s}_{i}') for i in range(k)] for s in range(ns)]
    D=[[[var(f'D_{j}_{i}_{c}') for c in range(dims[j])] for i in range(k)] for j in range(len(dims))]
    for g in range(n):
        for i in range(k):
            for j in range(k):claim(f'(= (* {P[g][i][j]} (- {P[g][i][j]} 1)) 0)')
            claim(f'(= {add(P[g][i])} 1)');claim(f'(= {add(P[g][j][i] for j in range(k))} 1)')
    for i in range(k):
        for j in range(k):claim(f'(= {P[e][i][j]} {int(i==j)})')
    for g in range(n):
        for h in range(n):
            for i in range(k):
                for j in range(k):
                    claim(f'(= {add(f"(* {P[g][i][l]} {P[h][l][j]})" for l in range(k))} {P[table[g][h]][i][j]})')
    for row in E+[row for query in D for row in query]:
        for x in row:claim(f'(>= {x} 0)')
        claim(f'(= {add(row)} 1)')
    inverse=[next(h for h in range(n) if table[g][h]==e==table[h][g]) for g in range(n)]
    for s in range(ns):
        for j,m in enumerate(dims):
            for g in range(n):
                z=[]
                for c in range(m):
                    v=var(f'Z_{s}_{j}_{g}_{c}');z.append(v);claim(f'(>= {v} 0)')
                    mean=add(f'(* {E[s][i]} {P[inverse[g]][i][l]} {D[j][l][c]})' for i in range(k) for l in range(k))
                    diff=f'(- {mean} {smt_number(targets[s][j][g][c])})'
                    claim(f'(>= {v} {diff})');claim(f'(>= {v} (- {diff}))')
                claim(f'(<= {add(z)} {smt_number(2*eps)})')
    lines.append('(check-sat)')
    return '\n'.join(lines)+'\n', {'variables':variables,'constraints':constraints,'group_order':n,'width':k,'semantics':'existential real, polynomial degree at most three'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    formula,stats=compile_formula(json.loads(args.input.read_text()))
    args.output.write_text(formula)
    print(json.dumps(stats,sort_keys=True))

if __name__=='__main__':main()
