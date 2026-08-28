# CM2 Gate 1: local-jet gauge obstruction frontier

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: the fifteenth-round same-representative shadow obstruction and
the fourteenth-round finite faithful coding / connector obstruction  
Strict verdict: **all gauge repairs that keep the compact gauge's value and
first jet at the 96-collision shadow, and all gauges locally constant near
the connector, inherit a certified divergent stable canonical comparison.
This refutes the natural QNL-local and first-order-flat repair classes, but it
does not exclude a genuinely global jet-changing third gauge. Gate 1 remains
`NOT_CERTIFIED`.**

## 1. New exact layer

For a periodic return `G(z_*)=z_*` and a gauge `D`, write

```text
A_D(z)=D(Gz)^(-1) DG(z)D(z).
```

Differentiation at the periodic point gives

```text
dA_D[v]
 =-D^-1 dD[DG v]D^-1 DG D
  +D^-1 d(DG)[v]D
  +D^-1 DG dD[v].
```

Consequently `A_D(z_*)` and `dA_D(z_*)` depend on the gauge only through
`D(z_*)` and `dD(z_*)`.  Two gauges with the same value and first jet at the
periodic point have the same gauged return, the same fiber eigenbasis and the
same resonant mixed coefficient.  No second or higher gauge jet enters this
first-derivative test.

The fifteenth-round 5000-bit replay certified, in the compact-gauge
eigenbasis at the 96-collision shadow,

```text
c_* = -3.89445593740627418819...e-13 +/- 2.91e-94,
```

strictly outside zero.  Hence every alternative gauge satisfying

```text
D_alt(z_*)  =D_compact(z_*),
dD_alt(z_*) =dD_compact(z_*)
```

has exactly the same nonzero coefficient.  On any clean horseshoe containing
the shadow and a nontrivial local-stable tail, its canonical increments obey
the already certified exponential asymptotic and cannot converge.  This
includes all modifications supported away from the shadow and all
modifications flat through first order there.  It does not assert anything
negative about the isolated periodic orbit alone.

## 2. Connector-local obstruction

At the symmetric connector fixed point the physical return has the strict
mixed-jet enclosure

```text
partial_xy G_2 = -0.042403922337495...,
-1/20 < partial_xy G_2 < -1/25.
```

If a gauge is constant on a neighbourhood of that point, the return and all
finite canonical comparisons change only by constant conjugacy.  Divergence
is invariant under such a conjugacy.  Therefore every gauge supported inside
the frozen QNL chart—and more generally every gauge locally constant near
the connector—retains the connector stable-tail obstruction.

Combining the two tests rules out a large natural repair class:

```text
QNL-local cutoff / partition-of-unity repair,
unchanged near the connector,
and unchanged through first order at the periodic shadow.
```

Such a repair cannot turn the compact twisting representative into class
`H`.

## 3. Exact scope boundary

The conclusion is deliberately local-jet conditional.  A surviving third
representative must do at least both of the following:

1. change the shadow value or first jet so as to cancel its resonant mixed
   coefficient;
2. change the connector local jet, or cease to be a QNL-local gauge.

The present certificate neither solves nor proves inconsistent the global
stable and unstable resonant jet equations at every periodic word.  Jets at
two distinct periodic points can be prescribed independently before global
compatibility is imposed.  Therefore it would be an overclaim to infer a
no-go theorem for every global gauge, one same-representative class-`H` plus
twisting theorem, full-mass coding, or physical PPE.

```text
periodic gauge first-jet invariance:                    CERTIFIED
shadow first-jet equivalence-class class H:             REFUTED
connector locally-constant-gauge class H:               REFUTED
pure QNL-local cutoff repair:                            REFUTED
arbitrary global jet-changing third gauge:               NOT CERTIFIED
one representative with class H and twisting:            NOT CERTIFIED
Gate 1:                                                   NOT CERTIFIED
```

## 4. Latest-technology audit

The official arXiv `math.DS` API was checked through the 2026-07-15 update
batch (latest listed identifier `2607.14048v1`).  The new batch contains no
canonical-holonomy theorem for non-fiber-bunched cocycles and no theorem that
solves the present all-periodic-word resonant jet equations.  The potentially
nearby July papers on Markov cocycles, hyperbolic random dynamics and SRB
measures assume smooth/random hyperbolic interfaces rather than the required
singular-billiard same-representative construction.  No literature result is
used to promote this local-jet theorem beyond its explicit hypotheses.

## 5. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate1_local_jet_gauge_obstruction_frontier_cert.py \
  deliverables/cm2_gate1_local_jet_gauge_obstruction_frontier_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate1_local_jet_gauge_obstruction_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate1_local_jet_gauge_obstruction_frontier_verifier.py \
  --self-test

# Expected fail-close live verdict: exit 2.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate1_local_jet_gauge_obstruction_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-local-jet-gauge-obstruction-frontier-manifest-2026-07-16.sha256
```
