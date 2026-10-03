#!/usr/bin/env python3
"""Exact finite regression, not proof of universal estimates or novelty."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import copy
import hashlib
import io
import json
from math import isqrt
import random
import subprocess
import sys
import instrument_streaming as m

ROOT = Path(__file__).resolve().parent
COUNT = 0
NEG = []

def require(ok, message):
    global COUNT
    COUNT += 1
    if not ok:
        raise RuntimeError(message)

def rejects(name, fn):
    try:
        fn()
    except (ValueError, KeyError, TypeError):
        NEG.append(name)
    else:
        raise RuntimeError("negative control escaped: "+name)

def sqrt_upper(x: F) -> F:
    if x == 0:
        return F(0)
    unit = 1 << 96
    num, den = x.numerator*unit*unit, x.denominator
    n = isqrt(num//den)
    if n*n*den < num:
        n += 1
    return F(n, unit)

def difference_upper(values, d):
    vals = list(values)
    entry_bound = sum(abs(x) for x in vals)
    frobenius_bound = sqrt_upper(d*sum(x*x for x in vals))
    return min(entry_bound, frobenius_bound)

def norm_upper(a, za, b, zb):
    """Rigorous trace-norm upper bound: min(entrywise L1, sqrt(d)*Frobenius)."""
    return difference_upper((F(x, za)-F(y, zb)
               for ar, br in zip(a, b) for ag, bg in zip(ar, br) for x, y in zip(ag, bg)),len(a))

def unnormalized_upper(a, wa, b, wb):
    return difference_upper((wa*x-wb*y for ar, br in zip(a, b)
               for ag, bg in zip(ar, br) for x, y in zip(ag, bg)),len(a))

def maximum_bits(p):
    return max(abs(x).bit_length() for row in p for z in row for x in z)

def outer(v):
    return [[m.mul(a, m.conj(b)) for b in v] for a in v]

def round_checks():
    rng = random.Random(6501)
    cases = 0
    for d in [2, 3, 4, 5]:
        for _ in range(45):
            vectors = [[(rng.randrange(-4, 5), rng.randrange(-4, 5))
                        for _ in range(d)] for __ in range(3)]
            p = m.identity(d)
            for v in vectors:
                p = m.plus(p, outer(v))
            if _ % 3 == 0:
                p = outer(vectors[0])
            if m.trace(p) == 0:
                p = m.identity(d)
            require(m.psd(p), "input PSD")
            for B in [1, 2, 3, 7, 16, 128, 1024]:
                a = m.round_density(p, B)
                z = B+2*d*d
                require(a == m.adjoint(a), "repair Hermiticity")
                require(m.trace(a) == z, "fixed denominator")
                require(m.psd(a), "repaired matrix PSD")
                require(norm_upper(a,z,p,m.trace(p)) <= F(6*d*d,B),
                        "trace norm certified by rational norm enclosure")
                require(maximum_bits(a) <= z.bit_length(), "legal numerator size")
                cases += 1
    p = [[(4,0),(6,0)],[(6,0),(9,0)]]
    a = m.round_density(p, 3)
    naive = [row[:] for row in a]
    for i in range(2):
        naive[i][i] = (naive[i][i][0]-4,0)
    require(not m.psd(naive) and m.psd(a), "indefinite naive rounding witness")
    NEG.append("trace-preserving-coordinate-rounding-is-not-positive")
    require(not m.psd([[(1,0),(2,0)],[(2,0),(1,0)]]),"reject indefinite")
    require(not m.psd([[(0,0),(1,0)],[(1,0),(1,0)]]),"zero pivot row test")
    for n in range(-200,201):
        for z in range(1,31):
            t=m.toward_zero(n,z)
            require(abs(t)*z <= abs(n) < (abs(t)+1)*z,"signed division identity")
    rejects("zero-divisor",lambda:m.toward_zero(1,0))
    rejects("zero-grid",lambda:m.round_density(p,0))
    rejects("zero-state-normalization",lambda:m.round_density(m.zero(2),4))
    return cases

def sampling_checks():
    trials=0
    for total in range(1,80):
        width=(total-1).bit_length()
        counts=[0]*total
        for j in range(1<<width):
            if j>=total:
                continue
            stream=iter((j>>k)&1 for k in reversed(range(width)))
            got=m.uniform_below(total,lambda:next(stream))
            require(got==j,"exact accepted binary word")
            counts[got]+=1;trials+=1
        require(all(c==1 for c in counts),"uniform accepted distribution")
    bits=iter([1,1,0,1])  # total 3: reject 3 then accept 1.
    require(m.uniform_below(3,lambda:next(bits))==1,"explicit rejection")
    for j in range(7):
        bits=iter((j>>k)&1 for k in [2,1,0])
        outcome=m.draw([0,2,0,5,0],lambda:next(bits))
        require(outcome==(1 if j<2 else 3),"zero intervals never sampled")
    require(m.draw([0,0,17],lambda: (_ for _ in ()).throw(RuntimeError()))==2,
            "single possible outcome consumes no bits")
    rejects("invalid-fair-bit",lambda:m.uniform_below(3,lambda:2))
    rejects("zero-sampling-total",lambda:m.uniform_below(0,lambda:0))
    rejects("negative-outcome-mass",lambda:m.draw([1,-1],lambda:0))
    rejects("zero-instrument-row",lambda:m.draw([0,0],lambda:0))
    return trials

def policy(h, t):
    # Includes adaptive disturbance; probabilities need not be bounded below.
    if t%4==0:
        return [('u',F(1,3)),('v',F(2,3))]
    if t%4==1:
        return [('a',F(1))]
    if t%4==2:
        return [('m',F(1))]
    return [('u' if h[-1][1] else 'd',F(1))]

def path_checks():
    blocks=0
    for d,name in [(2,'qubit'),(3,'qutrit'),(4,'ququart')]:
        spec=m.Specification.read(ROOT/'inputs'/f'{name}-instrument.json')
        for B in [128, 4096]:
            # (true integer branch matrix, true scalar, numerical integer
            # matrix, simulator public-history probability).
            ap=m.round_density(spec.initial,B)
            states={(): (spec.initial,F(1,m.trace(spec.initial)),ap,F(1))}
            for t in range(7):
                error=sum(unnormalized_upper(p,w,a,v/F(m.trace(a)))
                          for p,w,a,v in states.values())
                require(error<=F((t+1)*6*d*d,B),"whole-tree cq trace upper bound")
                tv=sum(abs(w*m.trace(p)-v) for p,w,a,v in states.values())/2
                require(tv<=error/2,"classical marginal data processing")
                require(sum(w*m.trace(p) for p,w,a,v in states.values())==1,"true mass one")
                require(sum(v for p,w,a,v in states.values())==1,"simulator mass one")
                if t==6:break
                new={}
                for h,(p,w,a,v) in states.items():
                    for command,cprob in policy(h,t):
                        true=spec.branches(p,command);approx=spec.branches(a,command)
                        for y,(sp,sa) in enumerate(zip(true,approx)):
                            st=m.trace(sa)
                            if st==0:
                                # Store a legal arbitrary normalized state on a zero simulator branch.
                                out=m.round_density(spec.initial,B)
                            else:
                                out=m.round_density(sa,B)
                            prob=v*cprob*F(st,spec.q**2*m.trace(a))
                            coeff=w*cprob/F(spec.q**2)
                            require(m.psd(out),"full-tree legality, including unreachable branches")
                            require(m.trace(out)==B+2*d*d,"full-tree common denominator")
                            if coeff*m.trace(sp)>0 or prob>0:
                                new[h+((command,y),)]=(sp,coeff,out,prob)
                            blocks+=1
                states=new
    return blocks

def recurrence_checks():
    rng=random.Random(6502)
    stats={"exact":0,"positive-grid":0}
    steps=0
    for name in ['qubit','qutrit','ququart']:
        spec=m.Specification.read(ROOT/'inputs'/f'{name}-instrument.json')
        for N in [2,8,32,80,128]:
            for L in [2,5,150]:
                sim=m.Streamer(spec,N,L);stats[sim.mode]+=1
                true=[row[:] for row in spec.initial]
                for t in range(N):
                    command=rng.choice(list(spec.commands))
                    before=[row[:] for row in sim.p]
                    branches=spec.branches(before,command)
                    y=sim.step(command,lambda:rng.randrange(2))
                    require(m.psd(sim.p),"sampled path PSD")
                    require(m.trace(sim.p)>0,"nonzero sampled path")
                    true_branches=spec.branches(true,command)
                    if m.trace(true_branches[y])>0:
                        true=true_branches[y]
                    else:
                        # A branch impossible under the true model need not be
                        # conditionally close. Reset only the unused test comparator.
                        true=[row[:] for row in spec.initial]
                    if sim.B is None:
                        require(sim.p==true_branches[y],"exact branch identity")
                        require(m.trace(sim.p)<=m.trace(spec.initial)*spec.q**(2*(t+1)),
                                "exact trace growth")
                    else:
                        B=sim.B;d=spec.d
                        require(m.trace(sim.p)==B+2*d*d,"sampled grid denominator")
                        require(norm_upper(sim.p,m.trace(sim.p),branches[y],m.trace(branches[y]))
                                <=F(6*d*d,B),"chosen successor repair")
                    s=min(N,L+(N+1).bit_length())
                    require(maximum_bits(sim.p)<=20*(s+1),"conservative finite register bound")
                    steps+=1
                result=sim.finish()
                require(result['dimension']==spec.d,"actual output dimension")
    return steps,stats

def data_checks():
    rejects("non-object-specification",lambda:m.Specification.from_dict([]))
    raw=json.loads((ROOT/'inputs/qutrit-instrument.json').read_text())
    bad=copy.deepcopy(raw);bad['commands']['u'][0][0][0][0]=-2
    rejects("incomplete-Kraus-row",lambda:m.Specification.from_dict(bad))
    bad=copy.deepcopy(raw);bad['initial_numerator'][0][0]=-1
    rejects("illegal-initial-density",lambda:m.Specification.from_dict(bad))
    bad=copy.deepcopy(raw);bad['commands']['u'][0][0][0][0]=0.5
    rejects("floating-point-physical-input",lambda:m.Specification.from_dict(bad))
    bad=copy.deepcopy(raw);bad['commands']['bad']=bad['commands'].pop('u')
    rejects("non-atomic-command",lambda:m.Specification.from_dict(bad))
    # A very small nonzero branch and an exactly zero branch, without a floor.
    q=1000000000001
    # Rational Pythagorean triple: 2000000,999999999999,1000000000001.
    rare={"dimension":2,"kraus_denominator":q,"initial_numerator":[[0,0],[0,1]],
          "commands":{"r":[[[[q,0],[0,999999999999]]],[[[0,2000000],[0,0]]],[[[0,0],[0,0]]]]}}
    spec=m.Specification.from_dict(rare)
    a=spec.branches(spec.initial,'r')
    require([m.trace(x) for x in a]==[999999999999**2,2000000**2,0],"rare and zero exact probabilities")
    for c in [b'',b'\n',b'-2\n',b'2',b'2x\n']:
        rejects("bad-header-"+repr(c),lambda c=c:m.read_decimal_line(io.BytesIO(c),12))
    require(m.read_decimal_line(io.BytesIO(b'9'*100000+b'\n'),128)==128,"saturating precision parser")
    spec=m.Specification.read(ROOT/'inputs/qutrit-instrument.json')
    rejects("horizon-below-two",lambda:m.Streamer(spec,1,2))
    rejects("precision-below-two",lambda:m.Streamer(spec,3,1))
    sim=m.Streamer(spec,2,2)
    rejects("unknown-command",lambda:sim.step('?',lambda:0))
    rejects("too-few-commands",sim.finish)
    sim.step('u',lambda:0);sim.step('u',lambda:0)
    rejects("too-many-commands",lambda:sim.step('u',lambda:0))
    # Classical attenuation is sign-preserving but not numerically faithful.
    for beta in [F(1,2),F(4,5)]:
        for lam in [F(0),F(1,3)]:
            for f in [F(0),F(1,4),F(1)]:
                for n in range(1,12):
                    out=lam+beta**n*(f-lam)
                    require((out>lam)==(f>lam),"strict-cutpoint sign")
                    require(abs(out-f)==(1-beta**n)*abs(f-lam),"attenuation metric defect")

def cli_checks():
    p=subprocess.run([sys.executable,str(ROOT/'instrument_streaming.py')],
                     input=b'32\n2\n'+b'uvdi'*8+b'\n',
                     capture_output=True,check=True,timeout=30)
    rows=[json.loads(s) for s in p.stdout.splitlines()]
    require(len(rows)==33 and all(r=={'outcome':0} for r in rows[:-1]),"one-pass CLI outcomes")
    r=rows[-1];z=int(r['denominator_hex'],16)
    a=[[tuple(int(x,16) for x in entry) for entry in row] for row in r['numerator_hex']]
    require(m.psd(a) and m.trace(a)==z,"actual CLI final density legality")
    return hashlib.sha256(p.stdout).hexdigest()

def main():
    rounded=round_checks()
    sampled=sampling_checks()
    blocks=path_checks()
    steps,modes=recurrence_checks()
    data_checks()
    cli_hash=cli_checks()
    print(json.dumps({"schema":"gtf65.instrument-regression/1","status":"success",
                      "exact_assertions":COUNT,"positive_rounding_cases":rounded,
                      "accepted_binary_words":sampled,"adaptive_tree_branches":blocks,
                      "sampled_prefixes":steps,"mode_cases":modes,
                      "negative_controls":NEG,"cli_example_sha256":cli_hash,
                      "floating_point_decisions":False,
                      "scope":"Finite exact arithmetic, legal density matrices, actual CLI, full adaptive tree error bounds, and implementation identities only. Not universal proof, formal space verification, ideality of OS randomness, or priority clearance."},
                     indent=2,sort_keys=True))
if __name__=="__main__":
    main()
