# CM2 Gate 1 assault: common magnet, tangent matching, and transport typing

Date: 2026-07-15 (Asia/Shanghai)  
Scope: Gate 1 only  
Frozen inputs: `cm2-bridge-note-v51.tex` and `cm2-bridge-note-v52.tex` were
read but not edited  
Claim status: **PHYSICAL COMMON-VERTEX CERTIFICATE OPEN / NO-GO**

## 1. Executive verdict

The current data do **not** close the requested physical common-vertex gate.
The correct split verdict is:

| Layer | Verdict | Reason |
|---|---|---|
| Regular QNL and connector periodic orbits | certified | Frozen exact/Arb certificates. |
| Existential clean heteroclinic cycle on the standard solid-collision map | proved, nonconstructively | Lima--Obata--Poletti, Section 5, Lemma 5.1, applied in both orderings. |
| Existential compact clean basic set/common Markov construction | proved at the topological level | The two clean transverse heteroclinic connections lie in a finite regular neighborhood; the inclination/Smale--Birkhoff construction applies there. |
| Explicit immutable transition candidate | improved | A new 400-bit Arb certificate gives a transverse match between finite images of the **linear eigentangents**, with complete physical words and strict margins. |
| Actual invariant-manifold intersection | **not certified** | No validated local stable/unstable graph or graph-remainder enclosure is available. |
| Quantitative four-face full crossing in a rectangle containing the periodic vertices | **not certified** | No invariant graph, rectangle widths, or four boundary inequalities have been proved. |
| Transported common-vertex loop derivative and four twisting wedges | **not certified** | The actual inbound/outbound strip holonomies and closed loop are not typed. |

Thus the topological existence issue is settled, but the certificate required
by physical PPE is not.  In particular, this report does not promote a
periodic matrix, a tangent-line match, or a local numerical tube to an actual
common-vertex cocycle.

## 2. Frozen baseline and model audit

The centered torus billiard has circular gray and white obstacles of radii

```text
R_G = 9/25,       R_W = 4/25,
```

at integer and half-integer centers.  The frozen geometry certificate gives
disjoint strictly convex obstacles and finite horizon.  The exact QNL orbit
is the gray--white normal two-cycle based at `G(0,0)`, and the certified
connector is the fourteen-solid-collision/eight-fixed-return orbit

```text
G0 W0 G0 W0 G0 W0 G1 G0 G1 W0 G0 W0 G0 W0 G0.
```

Both are regular hyperbolic periodic points on the standard collision map.
For a sufficiently small `chi`, a regular hyperbolic periodic point belongs
to `NUH^#_chi`: its Pesin data and recurrence scale are periodic and its
finite orbit is disjoint from all iterates of the singularity set.

The frozen manifest was checked after the new work:

```text
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

All entries, including the v51/v52 TeX/PDF hashes, returned `OK`.

## 3. What the cited homoclinic theorem proves exactly

Lima--Obata--Poletti consider a finite-horizon dispersing billiard with
pairwise disjoint `C^3`, strictly convex obstacles on the two-torus and its
standard solid-collision map `f`.  Their Section 5, Lemma 5.1 states:

> If `x,y in NUH^#_chi`, then for some `k>0`,
> `f^k(W^u(x))` meets `W^s(y)` transversely at a point outside
> `union_{n in Z} f^n(S)`.

Source:

- Yuri Lima, Davi Obata, Mauricio Poletti, *Measures of maximal entropy for
  non-uniformly hyperbolic maps*, arXiv:2405.04676v2, Section 5, Lemma 5.1,
  pp. 22--23: <https://arxiv.org/abs/2405.04676v2>.

Its proof uses Chernov--Markarian Lemmas 7.87 and 7.90: long stable/unstable
curves cross a finite family of rectangles, and suitable maximal images
u-cross (respectively s-cross) one positive-Lebesgue-measure magnet `R*`.
Mixing supplies the required forward/backward visits.

Apply Lemma 5.1 first to `(QNL,connector)` and then to
`(connector,QNL)`.  This gives a genuine clean transverse heteroclinic cycle.
Because only finitely many iterates of the two intersection orbits are used,
one can shrink to a neighborhood on which the billiard map is a smooth
diffeomorphism.  The standard inclination and Smale--Birkhoff/Markov
construction in that neighborhood gives a compact clean hyperbolic basic set
containing the two periodic orbits and transition branches.  White
collisions can be retained on the standard section or grouped into finite
words between gray returns after shrinking to constant-word strips.

This implication is existential.  Lemma 5.1 does not return:

- the collision/lift words of either heteroclinic connection;
- numerical stable/unstable graph radii or four-face margins;
- the derivative of the inbound and outbound transition holonomies;
- a uniform parameter-continuation interval;
- a numerical conditional SRB/Gibbs branch-weight lower bound.

Consequently `EXISTENTIAL_CLEAN_HETEROCLINIC_CYCLE` and
`EXISTENTIAL_COMMON_BASIC_SET` are discharged, while
`EXPLICIT_PHYSICAL_COMMON_VERTEX` is not.

## 4. New fail-closed tangent-line matching certificate

### 4.1 Discovery and immutable words

The non-rigorous search utility
`cm2_gate1_tangent_matching_search.py` found a binary64 candidate by
intersecting:

- ten forward solid collisions from the QNL **unstable eigentangent**; and
- fourteen inverse solid collisions from the connector **stable
  eigentangent**.

The search was only word discovery.  Its candidate was not accepted until an
independent 400-bit Arb calculation fixed the following relative-lift words:

```text
QNL forward:
  W0 G0 W0 G0 W0 G0 W0 G0 W0 G0

connector inverse, evaluated as I T^14 I:
  W0 G0 W0 G0 W0 G(+1,0) G(-1,0) G(+1,0)
  W(-1,0) G0 W0 G0 W0 G0.
```

The cumulative universal-cover connector lifts are

```text
(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(1,0),(0,0),
(1,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0).
```

### 4.2 Certified finite statement

In QNL eigen-coordinates use the linear unstable tangent

```text
(s,p) = t (1,k_A),
```

and in connector eigen-coordinates use the linear stable tangent

```text
(s,p) = u (1,-k_B).
```

The new script `cm2_gate1_tangent_line_matching_cert.py` first refines the
frozen connector root from radius `1e-50` to radius `1e-70` by an 8-dimensional
interval-Newton inclusion.  A two-dimensional Krawczyk calculation then
proves a unique zero of the finite tangent-line matching equations in

```text
t = -1.396101069259116746830594312272814e-9  +/- 4.92e-43,
u =  2.186137101021440040809485447235071e-12 +/- 5.57e-46.
```

The matching Jacobian determinant is strictly separated from zero:

```text
det D_(t,u) E = 6.8155727760125352319007e14 +/- 5.49e-9.
```

On the complete two legs, an exhaustive `[-3,3]^2` lift check gives

```text
minimum flight                 > 0.1871067811865475,
minimum target discriminant    > 0.0102643235474075,
minimum incoming incidence     > 0.6332062369959779,
minimum unintended clearance  > 0.2228385811397997,
transparent-wall crossings     = 0.
```

Every canonical endpoint lies in `(-3/2,3/2)^2`; any omitted lift has a
coordinate gap at least two, larger than either obstacle radius.  This makes
the finite first-hit enumeration exhaustive.

Reproduction:

```bash
python3 -m py_compile \
  deliverables/cm2_gate1_tangent_line_matching_cert.py \
  deliverables/cm2_gate1_tangent_matching_search.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_tangent_line_matching_cert.py
```

The final script deliberately prints

```text
TANGENT_LINE_MATCHING_SEED: CERTIFIED
HETEROCLINIC_INTERSECTION: NOT CERTIFIED
MICRO_FULL_CROSS_TRANSITION: NOT CERTIFIED
FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED
TRANSPORTED_TWISTING: NOT CERTIFIED
```

### 4.3 Why this is not a heteroclinic certificate

The source curves above are the affine tangent lines at the two periodic
points.  They are not validated pieces of `W^u(QNL)` and `W^s(connector)`.
At the displayed offsets the missing graph remainders are naturally of
orders

```text
t^2 approximately 1.95e-18,
u^2 approximately 4.78e-24,
```

before propagation.  No certified curvature/remainder constants currently
turn these heuristic orders into enclosures.  The Krawczyk radii of the
tangent problem therefore cannot be reused for the invariant manifolds.

An attempted direct twenty-four-step Arb thickening was discarded.  Even at
tiny dyadic source widths, dependency wrapping gave an unresolved stable
coordinate enclosure of about `+/-1.74e-6`; a subsequent parametric target
attempt gave a Krawczyk `c` image about `+/-1.94e-10` for a proposed box about
`+/-8.08e-28`.  These are failed enclosures, not dynamical falsifications,
and no micro full-cross claim is retained.

## 5. Why transported twisting is still untyped

Let `R` be an actual common Markov vertex.  A connector loop based at `R`
must have the form

```text
L_n = D H_out · J_B^n · D H_in,
```

where `H_in` and `H_out` are the derivatives along the actual two
heteroclinic/full-cross transition branches, evaluated at the closed symbolic
loop.  The four required wedges compare `L_n` with the Perron lines of the
QNL loop based at the same vertex.

The frozen matrix `J_B` is based at the connector periodic point.  The new
tangent-line script differentiates a finite word between off-center tangent
points.  It supplies neither `D H_in` nor `D H_out` on invariant strips and
does not close a return loop at a common vertex.  Its displayed long-word
tangent-coordinate Jacobian also has unresolved second-row intervals:

```text
[[1.80959e13 +/- 8.18e7,  -0.00914 +/- 6.87e-6],
 [          +/- 6.17e7,             +/- 4.39e-6]].
```

It is therefore illegal to insert this matrix into the four frozen
untransported wedges.  This is a typing failure, not just a weak numerical
margin.

Once actual `H_in,H_out` are available, the dwell search is finite.  If
`B` has eigenvalues `lambda,lambda^{-1}` with right/left eigenvectors
`v_+,v_-` and `ell_+,ell_-`, then for QNL eigenlines `e_i,e_j`,

```text
det(e_i, H_out B^n H_in e_j)
  = a_ij lambda^n + b_ij lambda^{-n},
```

where

```text
a_ij = ell_+(H_in e_j) det(e_i,H_out v_+),
b_ij = ell_-(H_in e_j) det(e_i,H_out v_-).
```

If `(a_ij,b_ij)` is not `(0,0)`, this expression vanishes for at most one
integer `n`.  Hence, after certifying non-identicality for all four pairs,
one of any five consecutive dwell values avoids all four zeros.  This reduces
the future twisting check to eight transport endpoint factors plus five
closed-loop replays; it does not remove the need to construct the transport.

## 6. Minimal next certifiable primitive

The next fail-closed Gate 1 certificate should do exactly the following:

1. Validate local invariant graphs

   ```text
   W^u_A: p = k_A s + r_A(s),
   W^s_B: p = -k_B s + r_B(s),
   ```

   on intervals containing the tangent seed, with interval bounds for
   `r_A,r_A',r_B,r_B'` and explicit graph-transform contraction.

2. Re-run the split `10+14` matching Krawczyk calculation with those graph
   enclosures.  Any loss of inclusion is a strict falsification of this
   candidate word, not of the LOP existential connection.

3. Thicken a successful invariant-manifold intersection into source/target
   rectangles and certify all four face inequalities, uniform cone margins,
   every first hit, and a parameter-continuation interval.

4. Close the two directed transition branches at one selected Markov vertex,
   calculate `D H_in,D H_out`, and run the five-dwell four-wedge test above.

Only item 4 would turn Gate 1 into the physical common-vertex input expected
by the downstream actual-SRB/PPE gate.  Until then the global claim remains
`NO-GO FOR CLAIM`.

## 7. Final status labels

```text
EXISTENTIAL_CLEAN_HETEROCLINIC_CYCLE: PROVED (LOP Lemma 5.1)
EXISTENTIAL_COMMON_BASIC_SET: PROVED (clean finite Smale--Birkhoff construction)
TANGENT_LINE_MATCHING_SEED: CERTIFIED (400-bit Arb)
ACTUAL_INVARIANT_MANIFOLD_MATCH: NOT CERTIFIED
EXPLICIT_FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED
TRANSPORTED_COMMON_VERTEX_TWISTING: NOT CERTIFIED
GATE_1_PHYSICAL: OPEN / NO-GO
```
