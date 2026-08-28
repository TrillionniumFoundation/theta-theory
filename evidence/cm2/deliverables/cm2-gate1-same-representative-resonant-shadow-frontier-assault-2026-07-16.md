# CM2 Gate 1: same-representative and resonant-shadow frontier

Date: 2026-07-16 (Asia/Shanghai)  
Frozen baseline: fourteenth-round finite faithful clean coding, diagonal
class-`H` representative, and compact-gauge four-wedge loop  
Strict verdict: **formal Hölder cohomology cannot merge the two frozen
representatives; moreover, the existing compact logarithmic gauge has a
strictly divergent stable canonical tail at the frozen 96-collision periodic
shadow.  This refutes class `H` for that gauge on every clean horseshoe that
contains the shadow and a nontrivial local-stable tail accumulating on it,
but does not exclude a third gauge and does not certify
that the predecessor's existential horseshoe contains the shadow.  Gate 1
remains `NOT_CERTIFIED`.**

## 1. Result

The fourteenth round left a precise fork:

```text
invariant Eu/Es frame:  faithful and class H, same-axis twisting = 0;
compact QNL log gauge:  one physical loop with four nonzero wedges,
                        all-plaque class H not certified.
```

This pass closes two ways of accidentally erasing that fork.

1. It writes the exact cohomology-defect identity for canonical holonomies.
   Outside fiber bunching, a Hölder transfer does not transport canonical
   holonomies unless an amplified tail defect tends to the identity.  The
   frozen wedge mismatch proves that at least one selected defect is not the
   identity.
2. It replays the complete frozen periodic-shadow word to order two at 5000
   Arb bits.  In the eigenbasis of the compact-gauged return, the derivative
   of the lower-left fiber entry in the physical stable direction is

   ```text
   -3.89445593740627418819...e-13 +/- 2.91e-94.
   ```

   It strictly excludes zero.  The stable canonical comparison increments
   therefore grow exponentially, so the existing compact gauge is not in
   class `H` on any clean horseshoe containing this periodic shadow and a
   nontrivial local-stable tail accumulating on it.

The new decision table is

```text
exact non-fiber-bunched cohomology defect identity:       CERTIFIED
formal transport of compact wedges from diagonal H:       REFUTED
compact-gauge stable limit at the 96-collision shadow:     DIVERGENT
compact gauge class H on a nontrivial shadow horseshoe:     REFUTED
shadow in predecessor's particular existential horseshoe: NOT CERTIFIED
every possible third resonant gauge obstructed:            NO
one representative with both H and twisting:               NOT CERTIFIED
Gate 1:                                                     NOT CERTIFIED
```

## 2. Exact cohomology-defect identity

Use the convention

```text
B(x)=D(fx)^(-1) A(x) D(x).
```

For a local stable pair `x,y`, finite cocycle algebra gives

```text
H_B^s(x,y;n)
 =D(y)^(-1) A^n(y)^(-1)
  [D(f^n y)D(f^n x)^(-1)] A^n(x)D(x).
```

Writing `H_A^s(x,y;n)=A^n(y)^(-1)A^n(x)`, the extra right factor is

```text
L_D^s(x,y;n)
 =A^n(x)^(-1)[D(f^n y)D(f^n x)^(-1)]A^n(x).
```

Thus canonical transport is valid only when `L_D^s -> I`; the unstable
formula is the backward analogue.  Hölder continuity merely makes the
unconjugated bracket tend to `I`.  In this QNL regime the condition number of
`A^n` amplifies that bracket, and the frozen periodic spectrum is not
fiber-bunched on either natural coding.

This is not only a warning.  If every stable and unstable defect were the
identity, the compact loop would be the base-fiber conjugate of the diagonal
loop.  Its periodic eigenaxes would be conjugated by the same base matrix, so
both same-axis wedges would remain zero.  The frozen compact loop instead has
all four wedges strictly nonzero.  Hence at least one selected stable or
unstable defect is genuinely nontrivial.  The compact twisting cannot be
imported from the diagonal class-`H` family by a formal cohomology statement.

## 3. The physical periodic shadow used for the jet test

The frozen reversible shooting root is refined at 5000 bits, using the same
shooting equation and no changed orbit data, to an interval of radius
`1e-800`.  The half and full words are

```text
Q^10 B^2,                 Q^10 B^4 Q^10,
```

with respectively 48 and 96 solid collisions.  This is the same excursion
word used by the selected QNL homoclinic, now closed at its separate periodic
shadow base point.

In the canonical QNL resonance coordinates, the base point is

```text
x_* = -8.2937621943296019634...e-15,
y_* =  1.1245565789608028843...e-13.
```

Both coordinates are nonzero and have magnitude below the `chi=1` core
radius.  Consequently the compact gauge is the exact analytic formula near
this point; neither the logarithmic axes nor a cutoff derivative enters the
calculation.

The order-two collision replay differentiates every physical collision and
composes the Hessians through the complete closed word.  In the same
canonical coordinates it gives

```text
det DG contains 1,
tr DG > 1e53,
Lambda = 1.0722583849647160265...e53,
nu     = 9.3261103295816728256...e-54.
```

## 4. Compact-gauge mixed coefficient

Let

```text
t(r)=k r^2 log|r|,
k=-325/(144 log(mu_QNL)),
B(x,y)=(I+t(x)E_12)(I+t(y)E_21).
```

At `(x_*,y_*)`, `B` is smooth.  If `v_s` is the stable eigenvector of the
physical 96-collision return `G`, the gauged return cocycle is

```text
A_hat(z)=B(Gz)^(-1) DG(z) B(z).
```

The certificate uses the exact three-term product rule

```text
d A_hat[v_s]
 =-B^(-1)dB[DG v_s]B^(-1)DG B
  +B^(-1)d(DG)[v_s]B
  +B^(-1)DG dB[v_s].
```

The fiber eigenbasis is `B(z_*)^(-1)(v_u,v_s)`.  In that basis, the
lower-left entry of the displayed derivative is

```text
c_* in
[-3.894455937406274188191812505690847732052761536129335093463194...
 +/- 2.91e-94].
```

In particular `c_* != 0`.

For a nontrivial point on the local stable tail, write its stable coordinate
as `y_n=d nu^n+O(nu^(2n))`, with `d != 0`.  The same exact increment algebra
used in the connector obstruction gives

```text
(K_n)_21 ~ -Lambda c_* d Lambda^n.
```

The increments are unbounded.  Convergence of the canonical comparison
would force them to tend to zero.  Therefore the compact-gauge stable
canonical limit diverges at this periodic shadow.

## 5. Scope discipline

The shadow word is the periodic closure of the same certified physical
excursion and is itself clean and hyperbolic.  The result therefore refutes
class `H` for the existing compact gauge on **any** clean horseshoe that
contains it together with a nontrivial local-stable tail accumulating on the
shadow.  It does not make a claim about the isolated periodic orbit viewed as
a zero-entropy invariant set.

It does not silently add the shadow to the particular horseshoe whose
existence was asserted in the fourteenth-round Birkhoff--Smale step.  That
partition was not materialized, so membership of this finite shadow remains
`NOT_CERTIFIED`.  More importantly, the calculation is not a no-go theorem
for every transfer: a third, globally solved resonant gauge could have
different jets at every periodic word while retaining the selected loop.

The exact remaining Gate-1 interface is therefore:

1. construct one faithful representative on one materialized clean coding;
2. solve its stable and unstable resonant tail equations on every plaque with
   uniform Hölder constants;
3. retain a nonzero twisting loop in that same canonical family;
4. bridge that subsystem statement to the full-mass physical projective law
   and PPE.

None of items 1--4 is inferred from the present obstruction.

## 6. Latest official arXiv audit

The official arXiv API was queried again on 2026-07-16 for canonical
holonomies, fiber-bunched cocycles, cocycle cohomology and holonomy.

- Butler--Park `arXiv:1909.11548v2` remains the exact class-`H` reference and
  assumes the global convergence and Hölder canonical families needed here.
- Mohammadpour--Varandas `arXiv:2508.05771v1` assumes a `1`-typical
  fiber-bunched cocycle, so it cannot create the missing representative.
- Kalinin--Sadovskaya `arXiv:2604.13401v1` concerns narrow-spectrum rigidity
  for hyperbolic automorphisms and supplies no singular-billiard resonant
  gauge or same-representative twisting transport.
- The newest 2026 query hits concern unrelated foliation measures,
  representations, random systems or algebraic holonomy.

No official result found in this audit makes canonical holonomies invariant
under the present non-fiber-bunched Hölder cohomology or solves the missing
all-periodic-word resonant jets.

## 7. Replay

Use `python-flint==0.9.0`:

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate1_same_representative_resonant_shadow_frontier_cert.py \
  deliverables/cm2_gate1_same_representative_resonant_shadow_frontier_verifier.py

$PY deliverables/cm2_gate1_same_representative_resonant_shadow_frontier_verifier.py \
  --replay --integrity-only
$PY deliverables/cm2_gate1_same_representative_resonant_shadow_frontier_verifier.py \
  --self-test

# Expected fail-close live verdict: exit 2.
$PY deliverables/cm2_gate1_same_representative_resonant_shadow_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-same-representative-resonant-shadow-frontier-manifest-2026-07-16.sha256
```
