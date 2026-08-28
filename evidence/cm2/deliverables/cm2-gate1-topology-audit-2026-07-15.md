# CM2 Gate 1 topology audit — 2026-07-15

## Verdict

The 400-bit calculation in `cm2_gate1_tangent_line_matching_cert.py` is a
rigorous calculation for **two affine eigentangent lines**, but it is not a
validated intersection of the actual invariant manifolds.  Consequently,
the calculation plus reversibility does **not**, by itself, prove a
heteroclinic cycle, a common homoclinic class, or a common locally maximal
hyperbolic magnet.

There is nevertheless an independent, non-effective theorem-level closure
of the **existential topological layer**.  The certified QNL and connector
periodic points are clean regular hyperbolic periodic points of the same
finite-horizon dispersing billiard.  Applying Lima--Obata--Poletti, Lemma
5.1, to the two orderings gives clean transverse heteroclinic intersections
in both directions.  The standard inclination-lemma/Markov construction
then places the two periodic orbits in one compact locally maximal
hyperbolic basic set and supplies existential full-cross transition strips.

This does **not** close the v52 physical `COMMON_MAGNET` gate: no selected
common vertex, explicit source rectangles, transported return derivatives,
or uniform boundary-face margins have been certified.

| assertion | audit status | reason |
|---|---:|---|
| clean finite word between the two affine eigentangents | **CERTIFIED** at the successful root layer | interval Krawczyk, nonzero matching determinant, declared physical itinerary and strict flight/incidence/clearance margins |
| true `W^u(QNL) \pitchfork W^s(connector)` from that root | **OPEN** | affine eigentangents are substituted for nonlinear invariant manifolds |
| opposite true intersection by reversibility | **OPEN from this root** | reversibility can reverse a true heteroclinic intersection, but cannot turn a tangent-line surrogate into one |
| same homoclinic class, existentially | **CERTIFIED independently** | Lima--Obata--Poletti Lemma 5.1, applied in both orders |
| common locally maximal hyperbolic basic set / existential Markov full-cross strips | **CERTIFIED independently** | clean two-way transverse cycle plus the standard inclination-lemma/basic-set construction |
| explicit common periodic vertex satisfying v52 Certificate B | **OPEN** | no common return rectangle, two return strips, transported loop matrices, or quantitative full-cross faces |

## What the Arb root actually solves

At the QNL point the script uses

\[
 (\theta,p)=\left(\frac\pi4+\frac{t}{R_G},\;s_A t\right),
\]

and at the connector point it uses

\[
 (\theta,p)=\left(\theta_B+\frac{u}{R_G},\;-s_Bu\right).
\]

These are the two **linear eigenlines**; see lines 297--318 of the audited
script.  The Krawczyk calculation at lines 389--428 proves a unique zero of
the matching equation built from those two affine lines.  At the audited
successful root it obtained

\[
 t=-1.3961010692591167\ldots\,10^{-9},\qquad
 u= 2.1861371010214400\ldots\,10^{-12},
\]

and

\[
 \det D\Phi=6.815572776012535\ldots\,10^{14}>0.
\]

The clean-word layer also proved the strict aggregate margins

\[
 \tau>0.1871,\quad \Delta>0.01026,\quad
 \cos\iota>0.6332,\quad \operatorname{clearance}>0.2228.
\]

Thus this is a strong and useful shooting seed.  It is not a heteroclinic
root because the script never constructs graphs

\[
 \gamma_A^u(t)\in W^u_{\rm loc}(A),\qquad
 \gamma_B^s(u)\in W^s_{\rm loc}(B),
\]

nor bounds their value and derivative errors relative to the two affine
eigenlines.  The tiny Krawczyk radii (`1e-43` and `1e-46`) only enclose the
zero of the affine-line problem; they do not enclose the unknown nonlinear
manifold correction.  Qualitative tangency, even together with the
nonvanishing affine matching determinant, is not a validated perturbation
argument at these fixed radii.

An earlier in-progress revision attempted a
`MICRO_FULL_CROSS_TRANSITION` between rectangles centred at the two matched
affine-line points.  Such a rectangle would not cure the invariant-manifold
gap because it excludes the two periodic centres.  That attempted layer also
failed direct interval wrapping and has been removed.  The audited final
script, SHA-256
`d58a196da59b1f31191ad67239b079e669a5629aec1deaee925fa76d9c489ed1`,
correctly prints `HETEROCLINIC_INTERSECTION: NOT CERTIFIED` and
`MICRO_FULL_CROSS_TRANSITION: NOT CERTIFIED`.

## Independent existential topology

Lima--Obata--Poletti, *Measures of maximal entropy for non-uniformly
hyperbolic maps*, arXiv:2405.04676v2, Section 5, Lemma 5.1, states that for
`x,y in NUH^#_chi` there is `k>0` such that

\[
 f^k(W^u(x))\pitchfork W^s(y)\ne\varnothing
\]

at a point outside every iterate of the billiard singularity set.  Its proof
uses a positive-Lebesgue-measure magnet rectangle `R_*`: an iterate of an
unstable subrectangle u-crosses `R_*`, while a backwards iterate of a stable
subrectangle s-crosses the same `R_*`.

The frozen certificates give regular hyperbolic periodic QNL/connector
orbits with clean words; the connector trace is greater than `10^8`, while
the exact QNL matrix is hyperbolic.  The companion uniform-horizon
certificate proves `tau_max<3` for the same table.  A clean hyperbolic
periodic point belongs to `NUH^#_chi` for any sufficiently small `chi` below
its Lyapunov exponent.  Hence Lemma 5.1 applies first to `(A,B)` and then to
`(B,A)`.

The two clean transverse connections have finite transition segments a
positive distance from singularities and tails converging to the two clean
periodic orbits.  Restricting the billiard map to a smooth neighbourhood of
this finite cycle permits the ordinary inclination-lemma construction.  A
finite Markov refinement gives a compact transitive locally maximal
hyperbolic basic set containing both periodic orbits.  Its Markov transition
strips are full crossings in the usual stable/unstable sense.  This is an
existence result only: neither Lemma 5.1 nor the standard construction
identifies the transition word, the rectangle width, or the transported
matrix needed by v52 Certificate B.

The source checked for this audit was `/tmp/lop2405.04676v2.pdf`, SHA-256
`776a48e4438b6be7b360de77246e7883e438150a96b6a29c392a164236ffde06`.

## Minimal validated repair of the explicit root

To upgrade the new shooting seed itself, it is enough to add the following
finite data.

1. Construct validated local invariant graphs in the same eigencharts,
   for example
   `gamma_A^u(t)=L_A^u(t)+e_A(t)` and
   `gamma_B^s(u)=L_B^s(u)+e_B(u)`, with interval enclosures of both `e` and
   `e'` on declared nondegenerate intervals.  The graphs must satisfy the
   actual QNL/connector return invariance equations, not only pointwise or
   finite-node interpolation.
2. Propagate the two graph tubes through the declared 10- and reverse
   14-collision words.  Recheck first-hit exhaustion, non-grazing,
   clearance, and singularity separation on the whole tubes.
3. Define the true matching map

   \[
   \Phi(t,u)=T^{10}\gamma_A^u(t)-T^{-14}\gamma_B^s(u).
   \]

   With a rational preconditioner `C`, certify

   \[
   x_0-C\Phi(x_0)+(I-CD\Phi(X))(X-x_0)
      \subset \operatorname{int}X
   \]

   and `0 notin det D Phi(X)`.  Equivalently, a Newton--Kantorovich audit may
   use `eta=||C Phi(x_0)||`,
   `kappa=sup ||I-C D Phi||<1`, and
   `eta/(1-kappa)<dist(x_0,partial X)`.
4. Certify the billiard involution `I(theta,p)=(theta,-p)`, the clean identity
   `I T I=T^{-1}`, and that the chosen symmetric representatives of both
   periodic orbits are fixed by `I` (up to their certified phase).  Only
   then does the first true intersection produce the opposite one by
   reversibility.

These four items would certify an explicit transverse heteroclinic cycle.
They would already imply existential nonzero full-cross rectangles by
openness and the inclination lemma.

For the stronger v52 common-vertex certificate, one must additionally choose
one actual product rectangle
`R=[-alpha,alpha]_u x [-beta,beta]_s` and two return strips.  On each whole
strip, interval arithmetic must prove one fixed clean word, stable
containment with a strict margin, and opposite unstable-face exits, e.g.

\[
 |B_j|<\beta-\varepsilon,\qquad
 A_j(\partial_-S_j)<-\alpha-\varepsilon,\qquad
 A_j(\partial_+S_j)> \alpha+\varepsilon
\]

(up to orientation), together with cone hyperbolicity.  The loop derivatives
must then be evaluated after the actual inbound/outbound transport.  The
untransported periodic matrices in the frozen certificate cannot substitute
for these common-vertex derivatives.

## Reproduction

The audit ran:

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_tangent_line_matching_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_tangent_line_matching_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_standard_section_horizon_lift_cert.py
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The tangent-root layer printed `TANGENT_LINE_MATCHING_ROOT: CERTIFIED`, then
fail-closed labels for the heteroclinic and micro-full-cross layers.  The
horizon certificate printed `STANDARD_SECTION_UNIFORM_HORIZON: CERTIFIED`
with 35,024 leaf boxes and maximum binary depth 14.  Every frozen v52
manifest entry remained `OK`.
