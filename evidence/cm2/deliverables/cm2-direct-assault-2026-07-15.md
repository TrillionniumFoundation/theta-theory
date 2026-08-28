# CM2 direct assault: theorem audit and route correction

Date: 2026-07-15 (Asia/Shanghai)  
Status: direct local research; no cron or detached scheduler was used  
Frozen baseline: v51/v52 are inputs only and were not edited

## Executive verdict

Unconditional CM2 is **not proved**.  The correct claim status remains
`NO-GO FOR CLAIM`.

This round nevertheless closes or materially sharpens five subproblems:

1. Lima--Obata--Poletti Lemma 5.1 supplies an existential clean common
   homoclinic magnet for the two regular physical periodic orbits on the
   standard finite-horizon collision section.  This closes the *topological*
   common-homoclinic-class issue, but not the transported derivative wedges,
   explicit full-strip certificate, or physical endpoint identity.
2. Stenlund's enlarged section `M* = M sqcup W` is a genuine common
   refinement of the fixed section `M` and the standard solid section
   `N = G sqcup W`.  Both return depths are uniformly bounded and have a
   finite Borel word registry.  Thus the geometric/measurable part of `SF1`
   can be discharged.
3. Because the circle radii and the abstract arclength--angle gauges are
   fixed, all three collision-flux probabilities are parameter independent.
   Differentiated Kac centering therefore has an explicit quotient derivative;
   the scalar derivative in v52 is not an independent unknown.  This closes
   the algebraic part of `SF3`, while typing of its boundary currents remains
   part of `SF2/SF5`.
4. Demers--Zhang plus a short Cauchy argument replace the circular form of
   `RW1`: a simple invariant pole, an annular inverse, and a spectral gap imply
   the exponentially weighted Wiener remainder.  The cited theorem supplies
   this for a mixing standard collision operator, not for the moving
   partition current or the common-refinement phase matrix.
5. A corrected 400-bit Arb two-stage atlas covers all 65536 tiles of the
   translated connector branch on `|b-h/2|<=2e-11`.  It certifies the complete
   28-collision word and proves `B_2<0` on the whole branch, strictly excluding
   this local stable-translation repair.  It does not construct the missing
   common magnet.

Gates 2--4 remain open.  In particular, no cited theorem supplies a uniform
finite-time Frostman estimate on every stopped physical parent, and the two
local tags `i_ent` and `i_exit` are different occurrences, not the two views
of one occurrence required by face time.

## Gate status after this round

| Gate | Status | Exact boundary |
|---|---|---|
| 1. connector/QNL common magnet | **topological layer proved; one larger local repair falsified; physical common-vertex certificate open** | Clean homoclinic relation/common standard magnet follows abstractly.  The corrected two-stage atlas excludes the declared translated quartic branch, but transported loop derivatives, full-strip margins and common-vertex twisting are not identified with the certified point matrices. |
| 2. actual SRB/Gibbs, stopped-parent PPE, endpoint identity | **open** | Common invariant law and a local finite-type seed are proved.  Every-parent finite-time Frostman, normalized `A/Z_A` moments, actual kernel weights and pointwise endpoint/projective identity are not. |
| 3. global one-return event inventory, DQ, matching | **open** | Single regular radical faces and a local positive core are proved.  No fail-closed chart/word/lift manifest, critical/common-factor audit, or complete occurrence/source matching exists. |
| 4. same-occurrence face-time and exact `q` | **open** | The abstract implication is correct.  Existing entry and exit atoms have different provenance; no one-mass bidirectional factorization exists. |
| 5. fixed section to full boundary | **SF1, SF3 algebra and the standard-`N` spectral layer closed; SF2/return-phase/SF5 open** | Common refinement and Kac identities are explicit, and the target collision resolvent is uniformly Wiener.  The full block current, any separately used return-phase matrix, and norm/test intertwiners are not. |

Here “exact `q`” must not silently strengthen v52's general bridge.  The
general statement there is

\[
  m_{\rm src}=K_*m_{\rm phys},\qquad
  q_{\rm src}\le C K_*q_{\rm phys},
\]

whereas equality of `q` requires an additional diagonal/single-copy
construction.

## 1. What the new homoclinic theorem does and does not close

Let `T` be the standard collision map of the centered finite-horizon
two-disk pilot.  Both the exact gray--white QNL orbit and the certified
period-eight fixed-section connector are regular hyperbolic physical periodic
orbits; after inserting the white collisions, the latter is a regular
periodic orbit of `T` as well.

Lima--Obata--Poletti, Lemma 5.1 in arXiv:2405.04676v2, proves that for any
`x,y in NUH^#_chi` there is `k>0` such that

\[
 T^k(W^u(x))\pitchfork W^s(y)\ne\varnothing
\]

at a point outside every iterate of the singularity set.  Its proof uses one
positive-measure magnet `R*`: an iterate of a subrectangle through `x`
u-crosses `R*`, while a backward iterate of a subrectangle through `y`
s-crosses the same `R*`.  Applying the construction to both orderings of the
two periodic points supplies clean heteroclinic connections in both
directions.  Shrinking around the finitely many clean orbit segments yields
regular full-cross branches, and the usual lambda-lemma/Markov construction
places the two orbits in one hyperbolic homoclinic class.

Source:

- Lima--Obata--Poletti, *Measures of maximal entropy for non-uniformly
  hyperbolic maps*, arXiv:2405.04676v2, Section 5, Lemma 5.1:
  <https://arxiv.org/abs/2405.04676v2>.

This is an existential topological result.  It does **not** identify the
derivative of either return loop after transport to a selected common base
rectangle.  In particular, the four Arb wedges for the untransported matrix
`J_B` cannot be copied to a loop of the form

\[
 D H_{\rm out}\,J_B^n\,D H_{\rm in}.
\]

The v52 connector countermodel shows why arbitrary connector derivatives can
align projective eigenlines.  Consequently the following still need one
common-strip certificate:

- the two concrete full return words and uniform physical margins;
- the transported pinching/twisting wedges on the same vertex;
- a positive conditional mass bound for the chosen strips;
- the pointwise identity between the transported projective slope and the
  actual endpoint derivative ratio.

Thus `TOPOLOGICAL_COMMON_HOMOCLINIC_CLASS` is discharged, while
`PHYSICAL_COMMON_VERTEX` is not.

## 2. Gate 2: exact audit of the actual-PPE chain

The true object chain is:

\[
 \mu_{\rm coll}
 \longrightarrow {\rm NST}_{\rm phys}
 \longrightarrow {\rm ACTUAL\_SLOPE\_BRIDGE}
 \longrightarrow {\rm SS}(d_Z=1)
 \longrightarrow {\rm PPE}_{1\text{--}4}.
\]

The common law

\[
 d\mu=\mathcal N_M^{-1}\cos\varphi\,dr\,d\varphi
\]

is exact and independent of the center displacement.  The pilot also has an
actual local order-two finite-type seed, a physical period-eight connector,
and an artificial Bernoulli projective Frostman benchmark.  None of these
changes the following quantified requirements.

On **every** stopped physical parent, uniformly in history, parameter and
depth, one still needs

\[
 \nu_{N,y}(I)\le C\bigl(|I|^\kappa+\rho^N\bigr),
\]

together with an exponentially small endpoint exception, the same retained
descendants for all amplitudes, and

\[
 \mathbb E\!\left[\left.(A/Z_A)^p\right|\mathcal F_{\rm parent}\right]\le C.
\]

Raw `L^p(A)` is insufficient: `A=1_E` on a small event is the elementary
counterexample after normalization.  A stationary i.i.d. Furstenberg
Frostman theorem is also insufficient because it has neither arbitrary
stopped parents nor place-dependent/countable Gibbs weights.

Finally, on the same immutable carrier one must construct actual endpoints
`X,Y` and prove pointwise

\[
 S=\log\left|\frac{\partial_uY}{\partial_uX}\right|,
 \qquad
 \frac{dY(1,z)}{dX(1,z)}
   =\frac{a+bz}{c+dz},
\]

with uniform denominator and wedge margins.  An auxiliary Möbius formula or
equality in distribution is not this identity.

Relevant literature shortens only separate layers:

- Baladi--Demers, Theorem 1.1, arXiv:2009.10936: the standard finite-horizon
  collision SRB is the `t=1` geometric equilibrium state and is exponentially
  mixing.
- Lima--Obata--Poletti, Lemmas 5.1--5.3, arXiv:2405.04676v2: one homoclinic
  class and a locally compact countable coding with Holder lifted potential.
- Stenlund--Young--Zhang, Corollary 32, Lemma 33 and Corollary 34,
  arXiv:1210.0011v4: a fixed coupling fraction and exponential uncoupled
  remainder after a family is already proper.
- Rush, arXiv:2601.14061: positive dimension for stationary measures of
  compactly supported i.i.d. `SL(2,R)` products under SIP.

None supplies the conjunction above.  Gate 2 therefore remains open.

## 3. Gates 3 and 4: fail-closed formulation

### 3.1 Complete one-return manifest required for Gate 3

The v52 finite-type reduction is not an instantiated event inventory.  A
machine-checkable manifest must have one row for every source chart,
direct/white-entry/white-exit word, physical target and admissible torus lift.
Each row must record

\[
 G=|q+tu-c_k(s)|^2-R_k^2,
\]

its squarefree discriminant/event function

\[
 H=(u\cdot(q-c_k))^2-(|q-c_k|^2-R_k^2),
\]

the selected root, forward/incoming/first-hit inequalities, physical traces,
coarea coefficient, polarity and immutable owner.

The checker must then certify:

1. coverage and mutual exclusivity of physical words;
2. submersion, target transversality and parameter continuation;
3. gcd/resultant and pair/triple incidence tables;
4. exact cancellation for artificial duplicates, or a joint normal form for
   every genuine common factor;
5. exact `m` and scalar-current pushforward and the declared `q` equality or
   domination on every restriction.

It must fail on either of the following decisive witnesses:

- `H = grad H = 0` with nonzero physical coefficient;
- a genuine common factor with unequal traces and nonzero coefficient,
  producing an untreated nonintegrable singularity.

The existing scripts do not implement this manifest.  In particular the
post-v52 local one-return tube is only a positive regular core, and the old
`cm2_common_rectangle_separator_cert.py` is superseded because its QNL angle
was set incorrectly.

### 3.2 The single-copy incidence registry required for Gate 4

The current local entry and exit constructions register two atoms.  This
cannot prove face time: splitting one bidirectionally recoverable order-one
current into two additive occurrences leaves one positive order-one tail in
each one-sided time cone.

The correct primitive starts with one physical incidence object `a` and one
coefficient measure `m_a`.  It stores two *alternative views*, not two
summands:

\[
 J_a
  =\langle U_a^-\nu_a^-,E_a^-\rangle
  =\langle U_a^+\nu_a^+,E_a^+\rangle.
\]

The occurrence index, coefficient, polarity and owner must be identical in
both displays.  Before any time query define only once

\[
 q_a=C_{\rm occ}(a)m_a,\qquad
 C_{\rm occ}(a)=\max\{C_a^-,C_a^+\}.
\]

Then prove that both views recover to proper standard families with uniform
cone/length/density/mark control and exponential moments for `R^-` and
`R^+`.  Only after exact record restriction and scalar-current matching may
the orientation be chosen.  If every occurrence has both views, the
orientation mismatch mass is zero by construction.

No such global incidence registry exists in v52.  This is the exact boundary
of Gate 4.

## 4. A proved common-refinement lemma (`SF1`)

Let

- `M` be Stenlund's fixed section: all gray collisions plus clean transparent
  wall crossings;
- `W` be the white collision component in its fixed arclength--angle gauge;
- `X=M*=M sqcup W`;
- `N=G sqcup W` be the standard solid-boundary collision section.

Then `X` contains both `M` and `N`.  Let `U_c` be first return to `X`.
Stenlund's free-zone construction gives

\[
 r_M(x)=\min\{j\ge1:U_c^jx\in M\}\in\{1,2\}.
\]

For return to `N`, lift a physical free flight to `R^2`.  Uniform finite
horizon gives a length bound `tau_max`, independent of the admissible center.
A segment of length at most `tau_max` crosses at most
`ceil(tau_max)+1` vertical and the same number of horizontal integer lines.
Only a subset of these are clean transparent returns.  Including the terminal
solid collision gives, for example,

\[
 r_N\le 2\lceil\tau_{\max}\rceil+3=:K_N.
\]

This also applies when the starting point is a clean wall crossing, because
it lies partway through such a bounded solid-to-solid flight.

In the common abstract gauge, `U_c` is Borel off its usual singular set.  For
`B=M` or `N`,

\[
 \{r_B=j\}=\bigcap_{i=1}^{j-1}U_c^{-i}(X\setminus B)
                  \cap U_c^{-j}(B)
\]

is Borel.  The component alphabet is finite and word length is bounded by
`max(2,K_N)`, so the component/lift word registry is finite.  Empty words for
a particular parameter remain empty Borel fibers in the common registry.
The same bounds hold on the whole compact displacement path.

This proves the geometric and measurable content of `COMMON_REFINEMENT`
(`SF1`).  It does not prove the DQ of the moving word boundaries.

Source: Stenlund, arXiv:1210.0902v3, Sections 2.1--2.4.  In particular, the
paper defines `M`, proves the free-zone one-white-hit property, defines
`M*=M sqcup W` in fixed coordinates, and states `n_c in {1,2}`:
<https://arxiv.org/abs/1210.0902v3>.

## 5. Differentiated Kac centering without a circular scalar (`SF3` algebra)

The radii and boundary parametrizations are fixed.  Consequently the
collision-flux probabilities on `M`, `N` and `X` all have fixed density
proportional to `cos(phi) dr dphi`; their normalizing constants do not depend
on the center displacement.

For either base `B=M,N`, let

\[
 r_{B,s}:B\to\{1,\dots,K_B\},\qquad
 \mathcal S_{B,s}h
   =\sum_{j=0}^{r_{B,s}-1}h\circ U_s^j,
\]

and `bar r_s=mu_B(r_{B,s})`.  Kac gives

\[
 \mu_X(h_s)=
 \frac{\mu_B(\mathcal S_{B,s}h_s)}{\bar r_s}.
\]

All measures in this formula are parameter independent.  Therefore, whenever
the displayed current pairings exist,

\[
 \partial_s\mu_X(h_s)|_0=\mu_X(\dot h)
 =\frac{\mu_B(\dot{\mathcal S}h+\mathcal S\dot h)}{\bar r}
  -\mu_X(h)\frac{\mu_B(\dot r)}{\bar r}.
\]

In fact `bar r_s=1/mu_X(B)` is constant because `B` is a fixed subset in the
fixed flux gauge, hence `mu_B(dot r)=0` distributionally.  The centered
induced observable consequently satisfies the exact four-term identity

\[
 \partial_s\{\mathcal S_s h_s-r_s\mu_X(h_s)\}|_0
 =\dot{\mathcal S}h+\mathcal S\dot h
  -\dot r\,\mu_X(h)-r\,\mu_X(\dot h).
\]

Thus `partial_s muhat_s(h_s)` is not an extra assumption or an unknown to be
solved circularly.  The remaining issue is analytic typing: `dot S` and
`dot r` contain the moving return-partition boundary currents.  Their bounded
actions on the declared source/test pairs are precisely `SF2/SF5`, not a
consequence of this algebra.

## 6. Correct noncircular Wiener lemma and the reach of Demers--Zhang

Let on a Banach source space

\[
 R(z)=\sum_{j=1}^J z^jR_j,\qquad D(z)=I-R(z).
\]

Assume `R` is analytic on `|z|<rho` for some `rho>1`, `D(z)` is invertible on
`|z|<=rho_0` except at `z=1`, and at `1`

\[
 D(z)^{-1}=\frac{\Pi}{\bar r(1-z)}+H(z)
\]

with the displayed pole simple and correctly normalized.  Then `H` is
holomorphic on a neighborhood of the closed disk `|z|<=rho_0`.  Cauchy's
estimate gives, for every `1<rho_1<rho_0`,

\[
 \|[z^n]H\|\le
 \sup_{|z|=\rho_1}\|H(z)\|\,\rho_1^{-n}.
\]

Hence the remainder belongs to every weaker exponentially weighted operator
Wiener algebra.  The same proof applies on the test side.  This is the
conclusion that v52's `RW1` currently assumes.

Demers--Zhang, arXiv:1210.1261, proves uniform Lasota--Yorke inequalities and
quasi-compactness for Lorentz-gas perturbations.  Theorem 2.2 states that the
peripheral spectrum is a finite union of roots of unity, without Jordan
blocks; if every power is ergodic, `1` is the only unit-modulus eigenvalue and
the collision map has exponential decay.  Theorems 2.5--2.6 put movements of
fixed-arclength scatterers on the same Banach pairs and control their spectral
data; Theorem 2.11 gives a uniform gap along a compact continuous path inside
the uniform billiard class.

Source: Demers--Zhang, *A functional analytic approach to perturbations of
the Lorentz gas*, arXiv:1210.1261, Section 2:
<https://arxiv.org/abs/1210.1261>.

For the standard full-boundary map this supplies a uniform decomposition
`L_s=Pi_s+Q_s` with `||Q_s^n||<=C rho^n` on the fixed source pair.  Choosing
`delta>0` with `exp(delta)rho<1` gives directly

\[
 \sup_s\sum_{n\ge0}e^{\delta n}\|Q_s^n\|<\infty,
 \qquad
 \sup_s\sum_{n\ge0}e^{\delta n}\|(Q_s^*)^n\|<\infty.
\]

Thus the standard target's centered source/test resolvents and absence of a
nontrivial unit-circle mode are closed.  The theorem does not supply

- a derivative of the transfer operator across moving singularity curves;
- the Kac return-partition boundary current;
- absence of a phase resonance for a separately chosen common-refinement
  tower;
- bounded intertwiners for the particular CM2 source/test/current pairs.

Thus it closes the standard-`N` spectral/Wiener layer of `SF4`, but not `SF2`,
the phase-matrix part of `SF4`, or `SF5`.  Its perturbation estimate is only
Holder from the strong to the weak space (of order at best a positive power
strictly below one here); dividing it by `s` does not produce the missing
first-difference current.

## 7. Route correction: direct standard-section formulation

There is a cleaner route to the target theorem than proving a large transfer
theorem after all fixed-section gates are closed.

The standard section `N=G sqcup W` already has a fixed abstract phase space:
both circle perimeters are fixed and the moving white boundary is identified
by its arclength--angle gauge.  Its invariant probability is fixed, and the
Demers--Zhang spaces/spectral theorem are formulated precisely for this
collision section.  The physical QNL two-cycle and connector word can be
recoded on `N` by retaining every white collision.

Moreover a one-step standard collision has no transparent-wall cut and no
nested white-entry/white-exit radical.  For a source point `q`, outgoing unit
vector `u`, and a candidate target circle `(a,R)`, put

\[
 w=u^\perp\cdot(a-q),\qquad
 \Delta=R^2-w^2.
\]

At a forward tangency, with flight length `ell=u dot (a-q)>0`,

\[
 |\partial_\varphi\Delta|=2R\ell
 \ge2R_{\min}\tau_{\min}>0.
\]

For the exact pilot, `R_min=4/25` and the already certified no-overlap
margin gives

\[
 \tau_{\min}\ge 2^{-1/2}-\frac{21}{40}>0.18210,
 \qquad
 |\partial_\varphi\Delta|>0.058272.
\]

The rational part of this margin is reproduced by
`cm2_standard_section_tangency_submersion_cert.py`; it deliberately prints
`GLOBAL_EVENT_DQ_AND_MATCHING: NOT CERTIFIED` to prevent promotion of this
one-step lemma into Gate 3.

Thus every physical one-step target-tangency face is a regular analytic
hypersurface; the feared single-event critical germ cannot occur there.
Distinct target circles cannot share an event hypersurface, because two
distinct circles have only finitely many common tangent lines.  A first-hit
target ordering cannot switch while both roots remain transverse: equality
of two positive hit times would put the same physical point on two disjoint
obstacle boundaries.  It can switch only through a tangency face.

This observation does not by itself prove the full DQ/current theorem, but it
removes the transparent-wall and nested-secondary strata from the global
one-step inventory.  A direct `N`-based v53 route would therefore:

1. keep the physical periodic/QNL certificates, recoded by solid collisions;
2. use the LOP homoclinic theorem directly on the target section;
3. instantiate the one-step circle-tangency manifest above;
4. build one incidence occurrence with forward/backward views by time
   reversal;
5. use the standard collision spectral gap directly, eliminating the final
   section-transfer gate.

This is a route reduction, not a CM2 proof.  Gates 2--4 still have to be
closed on the new common occurrence tree.

## 8. Immediate falsifiable work products

The next certificates should be fail-closed in this order:

1. **Transported common-vertex strip.**  Use the clean heteroclinic words
   supplied existentially above, then interval-certify both complete return
   strips and the transported wedges.  Stop on any lost word/cone margin or
   zero wedge.
2. **Standard-section event manifest.**  Enumerate the uniformly finite target
   lifts and certify every tangency submersion, first-hit region and pair/triple
   incidence.  Stop on an unclassified common factor or a nonzero critical
   coefficient.
3. **Single-copy incidence registry.**  Make the forward and time-reversed
   parameterizations views of one coefficient measure and verify exact record
   restriction before any orientation query.
4. **Actual stopped-parent kernel.**  Prove a uniform physical strip hazard,
   then a bespoke finite-time conditional Frostman bound and normalized
   amplitude moment on that same kernel.
5. **Typed full-boundary current.**  Pair the resulting current with the
   Demers--Zhang source/test resolvents and verify the exact CM2 norms directly
   on `N`.

Until these certificates exist, no local numerical connector exclusion,
stationary projective theorem, global mixing theorem, or bounded return roof
may be reported as unconditional CM2.

## 9. Corrected full two-stage connector atlas

The pre-audit draft of `cm2_connector_quartic_two_stage_atlas_cert.py` was not
a valid certificate: the rectangular extension of the final gray angle used
the numerator of the `atan2` derivative but omitted the denominator
`n_x^2+n_y^2`, and several diagnostic minima selected overlapping Arb balls
with an ordinary strict comparison.  All runs made before this was found were
stopped and discarded.

The repaired dependency chain now:

- differentiates `atan2(n_y,n_x)` with the full positive denominator on both
  stage charts;
- propagates the centered affine remainder by a mean-value enclosure;
- uses Arb `min`/`max` for every clearance and reported extremum;
- checks at every one of the 28 collisions the forward root, discriminant,
  incoming incidence, all unintended lattice-obstacle clearances, and the
  absence of a transparent-wall crossing;
- covers the closed source interval with 65536 adjacent closed tile boxes.

The fixed hashes are recorded in
`cm2-two-stage-atlas-manifest-2026-07-15.sha256`.  With
`python-flint==0.9.0` and 400-bit Arb, the following four half-open index
ranges were run after the final patch:

```text
[0,16384)      exit 0
[16384,32768)  exit 0
[32768,49152)  exit 0
[49152,65536)  exit 0
```

They are disjoint as index sets and jointly cover every atlas tile.  The
closed tile boxes overlap at their geometric endpoints, so there is no gap in

```text
|b-h/2| <= 2e-11,       a = g(b)-6e-20.
```

The aggregate physical minima are conservatively

```text
flight                 > 0.1871087142206
target discriminant    > 0.01026437292622
incoming incidence     > 0.6332077600841
unintended clearance   > 0.2228387554787
```

and the complete two-return stable coordinate satisfies

```text
-3.037598028e-9 < B_2(b) < -3.037597839e-9 < 0.
```

Thus this specific translated quartic branch has no two-return stable root on
the doubled window.  This is a rigorous falsification of a proposed repair,
not a proof that all curved magnets fail.  The wrapped derivative still
crosses zero, so `monotone_stable_coordinate_inverse=NOT_CERTIFIED`, and the
script correctly ends with `COMMON_MAGNET: NOT CERTIFIED`.
