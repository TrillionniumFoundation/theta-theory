# Independent Referee Report — Round Sixteen

**Paper:** `B2 — Collision Clusters and Dynamic LDP`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/B2-collision-clusters-dynamic-ldp`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/B2_PRECONTACT_ENTROPIC_PROJECTION_LDP.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

This candidate contains the most important genuine repair in the hard-sphere chain. It no longer deletes a contact equation while retaining the associated reflection. Instead it defines a precontact map from the incoming trajectory, treats the contact condition as a zero set, and only constructs the specular reflection and future on that zero set. It also introduces genealogywise analytic minors, a global trajectory series, and an entropy-penalized positive projection intended to produce lower-bound recovery sequences.

The precontact reformulation should be retained. It removes the previous pseudo-orbit error. The full dynamic LDP nevertheless remains unproved because the two global steps—uniform recollision removal at logarithmic scale and positivity-preserving recovery—are not established.

## Major objections

### 1. The precontact construction is local, but the theorem is global

For each fixed regular genealogy, a nonzero transverse analytic minor can imply that a degeneracy set has small measure. The candidate then sums genealogy-dependent estimates under a factorial trajectory majorant. This can justify a qualitative dominated-convergence statement if the bad-set probability is bounded by one and the genealogy weights are summable.

The LDP needs more. The recollision cutoff, tube width, and Boltzmann–Grad parameter vary together, and the discarded set must be negligible at the logarithmic speed used in the upper and lower bounds. Pointwise convergence for every fixed genealogy does not provide a rate uniform in genealogical depth. The manuscript does not prove an estimate of the form
\[
\limsup_{\varepsilon\downarrow0}
  a_\varepsilon^{-1}\log
  \sum_G W_\varepsilon(G)
  \mathbf P_G(\mathrm{bad}_{\varepsilon,G})
  =-\infty
\]
or specify an order of limits that would make a weaker estimate sufficient.

The degrees, analytic norms, transversality constants, and sublevel exponents may deteriorate with genealogy complexity. A factorial count controls total tree mass; it does not automatically control the logarithmic error required by the LDP.

### 2. Entropic penalization cannot create feasibility in the positive collision cone

The lower recovery uses an optimization of the schematic form
\[
j_{\eta,n}
 =\arg\min_{j\ge0}
 \Bigl\|\Delta^*j-h_n\Bigr\|+\eta\,\mathrm{Ent}(j\mid A_f),
\]
and claims that strict convexity plus a positive reference intensity forces
\[
\Delta^*j_{\eta,n}\to h_n.
\]

This is false without a range theorem. As \(\eta\downarrow0\), the residual converges at best to the distance from \(h_n\) to the closure of
\[
\{\Delta^*j:j\ge0,\ j\ll A_f\}.
\]
If \(h_n\) lies outside that positive cone, no entropy penalty can make the distance vanish. Adding a positive background changes the current and its divergence; it does not represent an arbitrary signed Hodge correction by physical nonnegative collision events.

The candidate needs a positivity-preserving right inverse or a quantitative controllability theorem for the collision balance equation. That theorem is neither stated nor proved. This is the same fundamental lower-bound obstruction in a new variational notation.

### 3. Density of exposed positive pairs is therefore unsupported

The full lower bound is reduced to smooth positive balanced pairs exposed by contact sources, followed by the entropic projection. Because the projection does not establish feasibility, the candidate has not shown that exposed positive pairs are rate-dense in the finite-action domain.

Finite-dimensional exposed-point density is not enough: the balance constraint, positivity of the contact current, and absolute continuity with respect to \(A_f\) must survive the approximation simultaneously. The paper supplies no recovery sequence satisfying all three.

### 4. Finite-dimensional LDP plus tightness does not identify the full rate in one step

The candidate derives finite-coordinate log-Laplace limits from the global tree series and then invokes exponential tightness. To obtain the asserted full joint density–contact LDP, it must prove projective consistency, lower semicontinuity and goodness of the candidate rate, and a lower bound on the nonexposed boundary of the positive cone.

Those arguments are compressed into a paragraph. In particular, the Legendre transform of the limiting Hamiltonian can give only the convex dual candidate. Equality with the dynamic action requires the missing positive recovery theorem.

### 5. The microcanonical conclusion depends on the invalid B1 coefficient theorem

The source-conditioned microcanonical LDP is obtained by dividing by the exact shell coefficient supplied by B1. The recovered B1 module does not prove its positive compound-Poisson representation. Thus even a correct grand-canonical B2 theorem would not imply the stated microcanonical result.

## Genuine progress

The precontact map is a substantive correction. A physical surplus contact should indeed be treated as the zero set of an incoming map, with the reflection defined only after contact is imposed. This removes the specific inconsistency in the controlling Round-Fourteen construction.

That local correction must not be confused with closure of the global LDP. The positive-cone recovery problem remains fatal.

## Dependency and editorial significance

B2 is the mathematical root of most of the hard-sphere program:
\[
B2_{\rm GC}\to B1\to B2_{\rm MC}\to B3\to B4\to C1,C2,D1.
\]
A failure of the B2 lower bound propagates to every claimed Gaussian, nonlinear-semigroup, information, and phase result downstream.

## Minimum requirements for a new submission

A new version must include:

1. a complete atlas for precontact zero sets and postcontact continuation, including multiple/grazing exclusions;
2. logarithmic, not merely qualitative, control of the summed recollision remainder in the exact joint limit;
3. a proved positivity-preserving controllability/right-inverse theorem for \(\Delta^*\);
4. rate-dense recovery sequences preserving balance, positivity, and entropy;
5. a full projective-limit lower-bound argument;
6. a separate, valid B1 denominator theorem before asserting microcanonical conditioning.

## Verdict

**Reject.** The candidate genuinely repairs the pseudo-orbit construction, but the decisive positive lower recovery is still absent, and the genealogy summation is not shown at the LDP scale. The central joint dynamic LDP is therefore not established.
