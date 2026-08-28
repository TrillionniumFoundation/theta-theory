# CM2 Gate 4: physical-incidence type, retained-fraction shell and repeated-core frontier

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: the fifteenth-round Gate-4 weak-Borel and 24-inner-core
strong/product stacks, the fourteenth-round same-occurrence product stack,
the 64-row maximal occurrence registry and v52 were read only  
Strict verdict: **a same-occurrence Borel mass shell, a finite one-cut
mass-weighted corner charge and arbitrary-time unnormalised propagation for
the fixed 24-core open operator are certified; the transported physical
core-to-occurrence incidence, native repeated recovery, complete
`C_fw,C_rev,q` and Gate 4 remain `NOT_CERTIFIED`**

## 1. Executive result

This pass separates three objects that the preceding scalar bridge could not
distinguish.

1. The 24 rational cores are regular two-dimensional strict-first-hit
   interiors.  The 64 occurrence bases are singular moving-face rows.
   Therefore their direct set-theoretic intersection is empty on all
   `24*64=1,536` pairs.  The needed bridge is a **transported recovery-carrier
   incidence**, not a direct intersection.
2. On one positive occurrence law, any pre-registered restriction `A` has
   retained fraction

   ```text
   p=m_e(A)/m_e(row),
   D(A)=ceil(log_2(1/p)).
   ```

   The two nonadditive views use the same `m_e`, restriction, `p` and `D`.
   This gives a genuine query-independent Borel shell ledger on all 64 rows.
3. A one-interval core corner clip still has infinite conditional shape-cost
   supremum.  Nevertheless, after weighting by its retained mass, its
   two-orientation recovery-clock factor is uniformly finite:

   ```text
   p exp[(R_fw+R_rev)/12060] < 15/8.
   ```

   Thus the correct alternative to charging `sup 1/p` is a mass-weighted
   retained-fraction shell.  It is certified for one cut, but it cannot be
   installed physically until the transported incidence and the one-interval
   strong typing of both views are supplied.

Independently, the fixed physical open operator obtained by repeatedly
restricting to the union of the 24 cores has a complete unnormalised
arbitrary-time Growth resolvent.  This bypasses corner normalization for that
one fixed operator.  It is not a native stopping antichain and does not
control arbitrary query-selected indicators or the discarded cemetery
piece.

## 2. The 24-to-64 incidence audit

The frozen core stack certifies every inner rectangle against the complete
retained candidate list and records no branch-internal singularity cut.  The
64-row stack, by contrast, consists exactly of state-changing singular
moving-face rows.  Hence

```text
direct regular-core / singular-base pair universe:  1,536
direct intersections:                                   0.
```

This zero does not solve the desired bridge.  It proves that the desired
incidence must have the richer immutable type

```text
(occurrence_id, view, recovery carrier/branch record,
 transport time, core component id, identical pulled-back restriction).
```

Label matching cannot substitute for this record.  Matching only the source
obstacle creates 768 candidates: each of the twelve `G` cores sees 44 rows
and each of the twelve `W` cores sees 20.  Matching source and target lift
reduces this to 112 candidates, with exact per-core histogram

```text
0 candidates: 8 cores,
5 candidates: 8 cores,
9 candidates: 8 cores.
```

It is still many-to-many and leaves eight cores unmatched.  It has no
recovery carrier, transport time or pulled-back restriction, so it is not a
physical incidence.  The certified transported incidence count remains
zero.

## 3. Same-occurrence retained-fraction shell

For `0<p<=1`, define

```text
D=ceil(log_2(1/p)).
```

Then

```text
2^-D <= p,
p < 2^(1-D)  for D>=1,
1/p <= 2^D.
```

The frozen product record already makes the forward and reverse views
alternative views of the same positive occurrence law and carries the same
restriction before any later test is chosen.  Consequently they have exactly
the same `p` and `D`.  This proves, on all 64 rows,

```text
SAME-OCCURRENCE BOREL RETAINED-FRACTION SHELL: CERTIFIED.
```

No strong conclusion follows for an arbitrary Borel `A`: it need not be one
interval on either recovery carrier.  In particular, this shell does not by
itself identify any of the 24 core restrictions on an occurrence.

## 4. Finite mass-weighted replacement for the corner supremum

Let a recovered input family satisfy `Z_*/M<=C_p^*`, and suppose a sole
retained interval `I` has mass fraction `p`.  The frozen core characteristic
estimate gives

```text
Z_*(I) <= (2000/1999) Z_*(W).
```

Since `2000/1999<2`, the depth shell gives

```text
Z_*(I)/M_I < 2^(D+1) C_p^*.
```

The physical Growth coefficient satisfies

```text
vartheta_p^1005 <= 1/2.
```

The inherited term is therefore below `C_p^*/2` after

```text
R_I(D)<=1005(D+2),
```

while the additive equilibrium contributes at most the other `C_p^*/2`.
For the two views,

```text
R_fw+R_rev <=2010(D+2).
```

At `gamma=1/12060`, use

```text
exp(1/6)<5/4,
exp(1/3)<3/2.
```

For `D>=1`, `p<2^(1-D)` now yields

```text
p exp(gamma(R_fw+R_rev))
 <2 exp(1/3) [exp(1/6)/2]^D
 <3(5/8)^D
 <=15/8.
```

The no-cut case `p=1,D=0` has factor one.  Thus

```text
normalized shape supremum:                  infinity,
one-cut mass-weighted two-view clock factor: <15/8.
```

This is the requested alternative charging mechanism.  For a pre-fixed
finite history of length `H`, its current bound is `(15/8)^H`.  There is no
query-independent tail on `H`, so this statement does not imply unbounded
repeated-indicator recovery.

## 5. Genuine repeated control without normalization

The fixed physical open operator

```text
O=T_* o M_core
```

first restricts to the union of the 24 cores and then applies one physical
step.  Its unnormalised adapted boundary recurrence is

```text
Z_*(O F)
 <= b_core Z_*(F)+2*10^90 mass(F),

b_core=720269600000/720626832337<1,
1-b_core=357232337/720626832337.
```

Because the open mass is nonincreasing, iteration gives for every `n>=0`

```text
Z_*(O^n F)
 <=b_core^n Z_*(F)
   +2*10^90 (1-b_core^n)/(1-b_core) mass(F).
```

The exact inherited-boundary resolvent and stationary mass coefficient are

```text
1/(1-b_core)
 =720626832337/357232337,

2*10^90/(1-b_core)
 =1441253664674*10^90/357232337.
```

Also `b_core^2018<1/2`.  Therefore

```text
FIXED 24-CORE UNNORMALISED ARBITRARY-n PROPAGATION: CERTIFIED.
```

This result never divides by the retained mass and therefore does not see
the divergent corner shape supremum.  Its exact boundary is equally
important: the fixed core union is not a native antichain; the discarded
complement has no strong cemetery payload; and an arbitrary later indicator
is outside the operator.

## 6. Conditional product arithmetic and nonpromotion

If a future certificate supplies the transported incidence and proves that
the identical restriction is one interval on both recovery carriers, the
frozen controlled product envelope can be multiplied by the core strong
factor and the new one-cut shell factor.  The resulting conditional
arithmetic is

```text
(2000/1999)*(15/8)*
1087598065258783059015245434544676138185728521412801591795461
----------------------------------------------------------------
                         6710886400000

=3262794195776349177045736303634028414557185564238404775386383
 ----------------------------------------------------------------
                         10732049530880.
```

This is only a checked implication.  Its physical hypotheses are not
certified in the current evidence stack, so the number is not promoted to `C_fw` or
`C_rev`, and no numerical `q=max(C_fw,C_rev,2)m` is assigned.

## 7. Exact remaining boundary

```text
direct regular-core / singular-base intersection audit: CERTIFIED ZERO
same-occurrence Borel retained-fraction shell:           CERTIFIED
one-cut mass-weighted corner recovery charge:            CERTIFIED
fixed-core unnormalised arbitrary-n propagation:         CERTIFIED

transported 24-core ->64-occurrence incidence:           NOT CERTIFIED
same core restriction one interval in both views:        NOT CERTIFIED
strong complement/cemetery payload:                      NOT CERTIFIED
Gate-3 branch-record MT_DQ/current identification:        NOT CERTIFIED
unbounded repeated-cut count tail:                       NOT CERTIFIED
native full reweighted recovery:                         NOT CERTIFIED
complete C_fw,C_rev,q:                                   NOT CERTIFIED
Gate 4:                                                  NOT CERTIFIED
```

The next executable Gate-4 object is not another label table.  It is a
transported incidence table on actual forward/reverse recovery carriers,
including time, branch owner and the common pulled-back restriction.  Once
that table exists, the `15/8` shell can be installed rowwise; after that, the
strong cemetery payload and an actual tail or contraction on the number of
registered cuts decide native repeated recovery.

## 8. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate4_incidence_shell_repeated_frontier_cert.py \
  deliverables/cm2_gate4_incidence_shell_repeated_frontier_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate4_incidence_shell_repeated_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate4_incidence_shell_repeated_frontier_verifier.py \
  --self-test

# Expected exit 2: transported incidence, native repeated recovery,
# complete C_fw,C_rev,q and Gate 4 remain open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate4_incidence_shell_repeated_frontier_verifier.py
```

Replay/integrity and pycompile exit `0`; the semantic suite rejects `21/21`
mutations; live mode exits `2`.
