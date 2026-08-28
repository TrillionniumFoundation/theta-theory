# CM2 Gate 1: global coding and class-H separation frontier

Date: 2026-07-16 (Asia/Shanghai)  
Frozen baseline: the thirteenth-round immutable QNL homoclinic loop and its
four certified twisting wedges  
Strict verdict: **a finite faithful clean-horseshoe coding and a global
class-`H` diagonal representative on that horseshoe are certified, but the
diagonal representative has zero same-axis twisting while the twisting
compact-gauge representative still lacks all-plaque holonomies; no single
representative is certified to have both properties, so Gate 1 remains
`NOT_CERTIFIED`**

## 1. Executive result

This pass closes the topological/coding ambiguity without promoting the
selected local loop to a global typical cocycle.

1. The selected symmetric QNL homoclinic occurrence is now strictly
   transverse.  On the whole validated unstable-graph tube, the tangent of
   the 48-collision half image has both coordinate components nonzero.  At
   its time-reversal fixed midpoint the reflected tangent has determinant
   with absolute value greater than `3e54`.
2. The Birkhoff--Smale construction therefore gives a compact clean
   horseshoe for a return iterate and a finite Markov coding.  Pulling back
   the actual derivative gives a faithful physical cocycle on this clean
   subsystem; no periodic matrix or finite-word surrogate is substituted.
3. The stable and unstable tangent line fields on that horseshoe give a
   faithful diagonal Hölder representative.  Its canonical stable and
   unstable holonomies converge uniformly with a Hölder modulus, so this
   representative belongs to Butler--Park class `H`.
4. Every holonomy loop of the diagonal representative is diagonal and
   preserves both periodic eigenaxes.  Its two same-axis twisting wedges
   are exactly zero.  Thus it is not weakly typical.
5. Conversely, the compact logarithmic gauge used for the four nonzero
   thirteenth-round wedges is not globally certified in class `H`.  A new
   point-jet calculation gives a stronger negative result on the earlier
   common basic set containing the connector: at the connector periodic
   point its stable canonical tail diverges exponentially.

The essential separation is therefore

```text
finite faithful clean coding:                         CERTIFIED
faithful invariant-frame representative in class H:  CERTIFIED
weak typicality of that diagonal representative:     REFUTED
four wedges for the selected compact gauge:           CERTIFIED (frozen)
all-plaque class H for that twisting compact gauge:   NOT CERTIFIED
one representative with both H and twisting:          NOT CERTIFIED
full-mass physical coding / PPE:                       NOT CERTIFIED
Gate 1:                                                NOT CERTIFIED
```

## 2. The selected physical homoclinic is transverse

Let `z_h` be the frozen actual unstable-graph root and put

```text
w=T^48 z_h in Fix(I),       I(theta,p)=(theta,-p).
```

The whole graph tube is replayed through the same physical half word
`Q5^2 B^2`.  If the actual input tangent is `(1,h'(x))`, the frozen graph
theorem gives `|h'|<=1e-4`.  The new interval calculation yields

```text
d theta_48(1,h') > 9e26,
d p_48(1,h')     > 2e27.
```

More precisely, the two lower interval bounds are centred at
`9.0959803478e26` and `2.2199703455e27`.  If the first tangent is `(a,b)`,
the stable branch obtained by reversibility has tangent `(a,-b)` at `w`.
Hence

```text
det((a,b),D I(a,b))=-2ab,
|det((a,b),D I(a,b))|>3e54.
```

The actual certified lower interval is centred at `4.0385613271e54` and
strictly excludes zero.  Since the whole 48-collision tube retains the
frozen flight, discriminant, incidence and clearance margins, this is a
clean transverse physical homoclinic point.  Diffeomorphic pullback gives
the same transversality at `z_h`.

The standard Birkhoff--Smale construction may now be performed inside a
regular neighbourhood of the periodic orbit and the finite excursion.  It
produces a compact locally maximal horseshoe for a return iterate `G` and a
finite Markov coding

```text
pi: Sigma_A -> Lambda,       G o pi = pi o sigma.
```

The partition can be chosen with the QNL periodic point in the interior of
its periodic rectangles.  The selected orbit then has a symbolic
homoclinic lift with the QNL code on both tails.  This is a coding of a
compact clean subsystem, not a full-collision-SRB or full-mass singular
billiard coding.

## 3. Faithful actual derivative cocycle

Choose finite local tangent trivializations on the Markov rectangles.  The
pulled-back cocycle is

```text
A_log(x)=E(sigma x)^(-1) D_(pi x)G E(x).
```

This formula is exact.  The Markov map `pi`, the invariant bundles and the
compact logarithmic gauge are Hölder on the clean set, so `A_log` is a
Hölder `GL(2,R)` cocycle.  This closes the former finite clean-horseshoe
coding blocker.  It does not create a full-mass quotient or a stopped
physical projective law.

## 4. A global class-H representative that cannot twist

Uniform hyperbolicity supplies Hölder line fields `E^u` and `E^s` on
`Lambda`.  Their pullbacks to the zero-dimensional finite SFT admit Hölder
frames after a finite clopen trivialization.  A finite higher-block recoding
makes the two orientation signs one-step.  In those frames,

```text
A_diag(x)=C(sigma x)^(-1) A_log(x) C(x)
         =diag(a_u(x),a_s(x)).
```

This is a faithful cohomologous representative of the actual derivative,
not a locally constant approximation.  For a local stable pair `x,y`, its
canonical holonomy is

```text
diag(
  product_(n>=0) a_u(sigma^n x)/a_u(sigma^n y),
  product_(n>=0) a_s(sigma^n x)/a_s(sigma^n y)
).
```

After the sign recoding, the sign ratios cancel on local plaques.  If
`phi=log|a_i|` is `beta`-Hölder and the symbolic contraction is `theta`,

```text
sum_(n>=0) |phi(sigma^n x)-phi(sigma^n y)|
 <= Hol_beta(phi) d(x,y)^beta/(1-theta^beta).
```

The unstable calculation is identical backwards.  Thus both canonical
families converge and are Hölder, exactly the two defining conditions of
Butler--Park class `H` (`arXiv:1909.11548v2`, equations (1.2) and condition
(b)).

However, every resulting holonomy is diagonal.  At the QNL periodic fiber,
every homoclinic loop preserves both coordinate eigenaxes.  Therefore

```text
det(e_u,psi_z e_u)=0,
det(e_s,psi_z e_s)=0
```

exactly.  The diagonal representative is reducible and is not weakly
typical.  This is not in conflict with the four nonzero compact-gauge
wedges: outside the fiber-bunched regime canonical holonomies are not
automatically transported by an arbitrary Hölder cohomology.  The two
canonical families must not be identified.

## 5. The compact QNL gauge fails on the connector basic set

The compact logarithmic gauge is supported in the QNL eigen-disk of radius
`1e-10`.  The connector fixed point has both QNL eigen-coordinates near
`-2.3500905801e-4`, hence a neighbourhood of it sees the identity gauge.

Let `G_B=T^14` be the connector return, written in its exact unstable/stable
eigen-coordinates with multipliers

```text
Lambda = 1.0749964438512...e8,
nu     = 9.3023563540...e-9,
Lambda*nu=1.
```

A fresh zero-radius 1000-bit point-jet replay, still carrying the frozen
`1e-70` connector root interval, proves

```text
partial_x partial_y (G_B)_2(0)
 = -0.04240392233749... +/- 4.78e-34
 in (-1/20,-1/25).
```

On the local stable graph `x=h(y)`, with `h(0)=h'(0)=0`, write

```text
b_21(y)=partial_x (G_B)_2(h(y),y)=c y+O(y^2),    c != 0.
```

For a nontrivial stable point, `y_n~d nu^n` with `d!=0`.  If
`H_n=D G_B^n(z)^(-1)D G_B^n(0)`, exact cocycle algebra gives

```text
(H_n^(-1)H_(n+1))_21
 = -Lambda (Lambda/nu)^n b_21(y_n)
 ~ -Lambda c d Lambda^n.
```

The increment is unbounded, whereas convergence of `H_n` would force it to
tend to zero.  Consequently the compact QNL gauge is not in class `H` on
the already established common clean basic set containing the connector.
This does not refute a different global gauge or prove failure on every
smaller selected horseshoe; it blocks the direct compact-support extension
that previously remained implicit.

## 6. Exact remaining boundary

The positive result is deliberately subsystem-scoped.  Gate 1 still needs
one and the same physically relevant representative with all of:

1. canonical stable and unstable holonomies on every coded plaque;
2. a uniform Hölder modulus for those holonomies;
3. the selected nonzero twisting loop in that same canonical family;
4. a bridge from the clean finite coding to the full-mass physical
   projective law and PPE.

The present stack instead proves a sharp fork:

```text
invariant-frame gauge: global class H, but twisting = 0;
compact logarithmic gauge: selected twisting != 0, but global H absent.
```

No single-cocycle Butler--Park weak-typicality or projective spectral/PPE
claim follows.

## 7. Latest official arXiv audit

The official arXiv API was queried on 2026-07-16 for canonical holonomies,
non-fiber-bunched cocycles, holonomy and typicality.

- Butler--Park `arXiv:1909.11548v2` remains the exact class-`H` reference;
  its definition requires global convergence and Hölder continuity of the
  canonical limits.
- Kalinin--Sadovskaya `arXiv:2604.13401v1` proves Hölder cohomology from
  conjugate periodic data only under narrow-spectrum, constant-target,
  measurable-cohomology or bounded-conjugacy hypotheses.  None is supplied
  for the compact twisting gauge.
- Mohammadpour--Varandas `arXiv:2508.05771v1` still assumes a
  `1`-typical fiber-bunched cocycle.  The frozen QNL periodic spectral
  obstruction excludes that route.
- The remaining 2026 query hits concern solenoidal rigidity, random or
  Schrödinger cocycles, and do not construct singular-billiard all-plaque
  canonical holonomies.

No newer theorem merges the two representatives certified here or removes
the same-representative requirement.

## 8. Replay

Use `python-flint==0.9.0`:

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate1_global_coding_class_h_frontier_cert.py \
  deliverables/cm2_gate1_global_coding_class_h_frontier_verifier.py

$PY deliverables/cm2_gate1_global_coding_class_h_frontier_verifier.py \
  --replay --integrity-only
$PY deliverables/cm2_gate1_global_coding_class_h_frontier_verifier.py \
  --self-test

# Expected fail-close live verdict: exit 2.
$PY deliverables/cm2_gate1_global_coding_class_h_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.sha256
```

