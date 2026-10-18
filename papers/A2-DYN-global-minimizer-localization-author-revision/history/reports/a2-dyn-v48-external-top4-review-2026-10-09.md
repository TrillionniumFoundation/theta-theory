# External top-four referee report on A2-DYN revision 48

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v48-referee-response-2026-10-08`, `revision/a2-dyn-v48-referee-copy-2026-10-08`  
**Reviewed commit:** `418000c216e9efa7c259a9bee9dac4fcf288ee1d`  
**Reviewed repository tree:** `713cfea3f615023cce5a755f5b432ee0b12171cd`  
**Ordinary paper tree recorded by the exact-SHA build receipt:** `8918ca0a31f4966750326217f15b79ad71ba6df7`  
**Ordinary source payload tree:** `ad0a05b34c189b93feba5586b85516057bbbf88d`  
**Active manuscript directory:** `papers/A2-DYN-v48-referee-response`  
**Active mathematical source:** one hundred four numbered core modules; revision 48 adds modules 102--104  
**Frozen revision-47 author baseline:** `ec4e7cca65ee3cbdc441c8264b39aca3ead112ac`  
**Controlling report:** `reviews/a2-dyn-v47-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `c7401a143332921b42cd532ea1f23617ad59e1bc` / `1d45f2c8bbf9664a4a1e188c80004d44ed4f9cfc`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 48 is a genuine theorem-bearing advance over revision 47. The preceding report isolated three unresolved positive sources in the raw correction: first bad incidence, first bad clearance, and first bad interior section decision. The new revision does not infer pointwise smallness of the third source from its small mass, and it does not interchange an uncontrolled family of fixed-depth limsups with an infinite depth sum. Instead, it proves a width- and mark-uniform local upper bound, constructs a positive telescope through every section-decision depth, retains one bad marked strip in both the high-gradient roof flow and the low-gradient critical collar, and sums the finite-count errors before taking the collision limit.

The resulting theorem is substantial. For the entire section-decision source with all physical incidence and clearance margins protected, it proves

```text
limsup_m sup_{R,n,k, |w|<=M}
  m^2 ||d^{eta,epsilon,w}_{n,k,m,R}||_infinity
  <= C M epsilon^(1/16),
```

and an explicit depth-tail estimate

```text
m^2 ||d_{>J}||_infinity
 <= C M epsilon^(1/16) (J+2) (47/53)^((J+1)/64)
    + C_{eta,epsilon} M m^4 rho_{eta,epsilon}^{m/2}.
```

The estimate is for the original exact return index, displacement, collision count, and roof variable. The occupation enlargement occurs only on the positive upper-comparison side. It remains valid for arbitrary bounded measurable source insertions by Radon--Nikodym domination. The complete signed convolution correction of this source is controlled uniformly over every reconstruction band.

Revision 48 then gives the exact positive split

```text
p = f^epsilon + d^{epsilon,epsilon} + b^epsilon,
```

where `f` is the inherited smoothly protected source, `d` is the newly controlled all-depth decision source, and `b` contains precisely the physical incidence and clearance defects. With `epsilon(B)=A B^(-1/12)`, the paid part of the normalized correction is `O(B^(-1/192))`. Thus the full arithmetic pointwise law is reduced to the signed correction of the two physical sources.

I audited the new modules

- `core/102_thin_strip_marked_local.tex`;
- `core/103_all_depth_decision_deconcentration.tex`;
- `core/104_physical_boundary_remainder.tex`;

and their use in the new leading theorem, together with the response, proof ledger, specialist audit map, source manifest, publication status, exact-SHA workflow runs, build receipt, finite-check output, and rendered theorem pages.

Within the scope of that audit, I found no decisive counterexample, Fourier-sign error, collision/return endpoint mismatch, missing factor of the section mass, incorrect occupation convention, illicit packet averaging on the target side, or hidden use of a reconstruction band growing with the collision count inside a fixed-band spectral theorem.

The negative recommendation is nevertheless unavoidable. The theorem which continues to govern the title and raw-inversion architecture is not proved. The remaining incidence and clearance sources have only the positive mass estimates

```text
sum_{n,k} ||b_inc||_1 <= C epsilon^2,
sum_{n,k} ||b_clr||_1 <= C epsilon,
```

and no `m^{-2}`-scale pointwise or Fourier-norm estimate for

```text
b^epsilon - K_B * b^epsilon.
```

A grazing incidence is a genuine singular regime of the collision map. A competing-hit clearance boundary changes the selected physical collision word. The roof-translation argument for a section-membership cut cannot simply be transported across either boundary. Small total mass does not control density height, and positivity before applying `I-K_B*` does not imply a signed cancellation afterwards.

The concrete section residues are also still not proved trivial. At fixed radius the exact-index main term naturally retains the arithmetic factor `mathfrak a_R(k,n,m)`; uniformly through changes of arithmetic type the correct object remains the transition kernel `mathcal L_{m,R}`. Revision 48 preserves this correctly, but it does not prove the unmodulated radius-uniform singleton theorem.

Accordingly, revision 48 closes a real blocker, but it does not close the decisive physical-boundary correction. At the requested venue level, the article would need either

- a complete arithmetic pointwise raw-density theorem, including incidence and clearance transitions or a proved signed cancellation mechanism, with the correct arithmetic main term; or
- a substantially broader conceptual theorem whose significance does not depend on the unfinished raw endpoint.

Revision 48 supplies neither yet.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`418000c216e9efa7c259a9bee9dac4fcf288ee1d`.

The repository tree is

`713cfea3f615023cce5a755f5b432ee0b12171cd`.

The active manuscript is

`papers/A2-DYN-v48-referee-response`.

The source manifest records the ordinary source payload tree

`ad0a05b34c189b93feba5586b85516057bbbf88d`.

The exact-SHA build receipt records the ordinary paper tree

`8918ca0a31f4966750326217f15b79ad71ba6df7`.

The reviewed author commit has the controlling revision-47 report commit as its parent. The chronology is therefore correct: the author revision descends from the frozen external report rather than rewriting the previously reviewed author source.

The source records state that all one hundred one inherited core modules and all one hundred twenty-seven inherited Python scripts are retained byte-for-byte. The bibliography, compiled A--X synopsis, provenance records, and inherited mathematical labels are preserved. Revision 48 adds modules 102--104, revised front matter and proof maps, finite diagnostics, and its exact-source qualification workflow.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v48-external-top4-review-2026-10-09/`.

No author source, prior review, workflow, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully at the reviewed SHA:

- response branch run `37808567408`;
- referee-copy branch run `37808581744`.

The response artifact is `11563633552`, named

`a2-dyn-v48-418000c216e9efa7c259a9bee9dac4fcf288ee1d`,

with archive digest

`sha256:eab8f4c8d96436bdb77e4c570e3072d54689ac4be05bea19caebdf0ca4f88f01`.

The downloaded build receipt binds the execution to the reviewed SHA and records

- `native_build_passed: true`;
- `dirty_scoped_source: false`;
- verification of the controlling report;
- PDF SHA-256 `e2a2db1d8a2731af40fe0792986331a534537b2d0c8176dd0f57a5300a056094`;
- `continuum_proof_certified: false`;
- `full_raw_LLT_certified: false`;
- `independent_human_review: false`.

The verifier checks, among other things,

- the frozen revision-47 full paper tree and controlling report blob;
- all one hundred four core inclusions;
- byte identity of inherited core files and scripts;
- retention of inherited labels, bibliography, and the A--X synopsis;
- the ordinary-source Merkle identity and workflow hash;
- normal/optimized finite-check agreement;
- native TeX compilation and stabilized references;
- theorem-label-based page rendering.

The new finite diagnostics cover affine strip-intersection models, interpolation exponents, both chronological long-block cases, occupation allowances, positive depth telescopes, geometric tail sums, exponential-error summation, and the ordered exponent `1/192`. Negative controls reject both a weak-mass-only height inference and an interchange of separate layer limsups with an uncontrolled depth sum.

These are meaningful source, algebra, and bookkeeping checks. They do not establish

- the uniform multiplier theorem on the actual anisotropic completion;
- the moving-peak spectral interpolation in the continuum spaces;
- the global glued-domain injectivity of the roof flow;
- preservation of a marked strip throughout every completed critical collar;
- disjointness and single charging of all physical collars;
- or the missing incidence/clearance correction.

The manuscript and its validation records state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove the complete one-hundred-four-module article. The substantive audit concentrates on the new chain which could alter the revision-47 assessment:

1. uniform strong multiplication by collapsing transverse strips;
2. the `s^(1/8)` strong-to-weak gain;
3. interpolation from weak smallness to moving spectral projection amplitudes;
4. marked chronological pairings at arbitrary collision time;
5. the four-frequency peak integral and the nonresonant long-block estimate;
6. positivity and exactness of the depth telescope;
7. a common continuation independent of decision depth and collision count;
8. the occupation allowance with terminal membership excluded;
9. retention of one bad marked strip under high-gradient roof transport;
10. retention of that strip throughout a completed critical collar;
11. collar disjointness and single charging;
12. summation of finite-count errors before the collision limit;
13. extension to arbitrary bounded source insertions;
14. the all-band convolution consequence;
15. exact reassignment of every history with a physical defect to the physical remainder;
16. the ordered `B^(-1/192)` correction ledger;
17. and the equivalence between the full raw law and the remaining physical correction.

Inherited load-bearing inputs include the full occupation-torus fixed-band spectrum, strong-space faithfulness, moving spectral maxima, physical projection formula, endpoint continuation and response, relative source distortion, physical critical collars, arithmetic transition formula, protected correction theorem, and the coefficient-first arithmetic raw criterion.

## 5. The thin-strip multiplier

Let `b_{R,s}` be the union of the finitely many coordinate strips of width comparable to `s` around the sides of the actual section. Revision 48 proves

```text
||M_{b_{R,s}} h||_B <= C ||h||_B,
|M_{b_{R,s}} h|_w <= C s^(1/8) ||h||_B.
```

The first assertion is uniform as the two parallel sides of a strip coalesce. The proof does not obtain this by differentiating the indicator or by paying an inverse strip width. It partitions a homogeneous stable curve at a uniformly bounded number of vertical and horizontal cut lines. On retained matched pieces the indicator is constant; pieces lost when boundaries fail to match have length controlled by the graph distance, or by the strip width when the entire strip is thinner than that distance.

The weak estimate uses the fact that each admissible stable graph crosses the fixed family of strips in a uniformly bounded number of intervals of length `O(s)`. The strong stable length normalization then pays `s^(varsigma)` with `varsigma=1/8`.

I found this mechanism internally consistent. It is exactly the type of statement needed to avoid a long pullback of a section indicator. The following points remain specialist obligations:

- the supporting-line cuts must satisfy the precise fixed-complexity multiplier hypotheses on every homogeneity strip;
- stable slopes must remain uniformly transverse to both coordinate directions used by the section sides;
- the strong-completion extension must preserve the physical multiplication operation;
- the unmatched-piece estimate must remain uniform when the strip width is below the matching distance;
- no hidden constant may depend on the separation of the parallel strip boundaries.

The manuscript addresses each point at the level of a proof sketch and cites the appropriate multiplier framework. I found no immediate contradiction, but this lemma is foundational for the entire new result.

## 6. Spectral interpolation from weak smallness

On a moving peak chart the manuscript writes

```text
Q^a = lambda^a Pi + N^a,
||N^a|| <= C rho^a,
```

and combines power boundedness with the full-occupation Doeblin--Fortet estimate

```text
||Q^a h|| <= C sigma^a ||h|| + C(1+a)|h|_w.
```

After shrinking the peak chart so that `|lambda|>=r>sigma^(1/4)`, it chooses a logarithmic time `L` from the weak norm `t=|h|_w/||h||` and obtains

```text
||Pi h|| + sup_a |ell(Q^a h)|
 <= C ||h||^(1/2) |h|_w^(1/2).
```

The exponent bookkeeping is correct. Since `r>sigma^(1/4)`, the factor `r^(-L)` costs strictly less than `t^(-1/4)`, while the Doeblin--Fortet weak payment contributes `t(1+|log t|)`. This is bounded by `Ct^(1/2)`.

Applied to the thin-strip multiplier, the result gives the amplitude gain

```text
s^(1/16).
```

The argument also controls terminal pairings uniformly over the length of the remaining block. It correctly treats the zero weak-norm case by sending the logarithmic time to infinity rather than dividing by zero.

The load-bearing assumptions are

- a common equivalent strong norm on the finite peak cover;
- a simple isolated branch with uniformly bounded projection;
- a complementary contour strictly inside the unit circle;
- uniform strong power boundedness on the chosen peak neighborhood;
- and continuity of the mass functional on the weak space.

These inputs are inherited from the revision-40/41 spectral chain. Revision 48 does not re-certify them, but it uses them in a mathematically coherent way.

## 7. The marked exact-coefficient local upper bound

For a mark at collision time `j`, the exact characteristic pairing is

```text
ell(Q^(m-j) M_b Q^j nu).
```

This ordering is correct for the physical push-forward realization: the first `j` phases are accumulated, the strip is tested at `T^j x`, and the remaining `m-j` phases are then accumulated.

At least one of the two blocks has length at least `m/2`. If the left block is long, the projection estimate is applied to `Pi M_b Q^j nu`; if the right block is long, it is applied to the terminal pairing with `M_b Pi nu`. The short block is used only through uniform strong power boundedness. Thus the peak contribution is bounded by

```text
C s^(1/16) |lambda|^(m/2) + C rho^(m/2).
```

The moving-peak Gaussian modulus integrates in the four real frequency variables to `O(s^(1/16)m^(-2))`. The nonresonant part of each fixed outer roof band has an exponentially decaying long block. A positive band-limited majorant of the roof interval then gives

```text
m^2 P(K_m^c=k, A_m=l, S_m-t in I, b_s(T^j x)=1)
 <= C s^(1/16)(h+B^(-1))
    + C_B(1+Bh)m^2 rho_B^(m/2).
```

The leading constant is independent of the outer roof band because every actual resonance has zero roof coordinate and the peak charts are chosen once in a fixed small roof neighborhood. The remainder may depend on the fixed outer band, as it should.

The theorem is uniform in the mark and strip width, so both may depend on the collision count. It is only an upper bound; the manuscript does not claim a Gaussian asymptotic for a shrinking strip.

I found no missing arithmetic factor. All moving peaks are retained, and the estimate is obtained by an absolute upper bound rather than by replacing the exact coefficient with an unmodulated origin contribution.

## 8. The positive depth telescope

With all physical margins in `H^eta` and every decision margin in `D^epsilon`, the revision defines

```text
G_a = H^eta product_{d_j>a} decision_guard_j,
G_{-1}=H^eta D^epsilon,
Z_a=G_a-G_{a-1}>=0.
```

The exact identity is

```text
sum_{a=0}^{floor(m/2)} Z_a = H^eta(1-D^epsilon).
```

If `Z_a>0`, every physical margin is protected, every decision deeper than `a` is protected, and at least one of the at most two contacts of depth `a` lies in a strip of width comparable to

```text
epsilon (47/53)^(a/4).
```

Only decisions of depth at most `a` are allowed to change. The safe occupation allowance is `|l-n|<=2a+2`. This is used only in a positive collision comparison. The density on the left remains the density of the original exact return event.

The terminal section membership at collision time `m` is correctly excluded from the occupation sum over times `0,...,m-1`.

This positive source-level telescope is the correct way to sum over depth. It avoids cancellation assumptions between separately normalized conditional laws and avoids an interchange of infinitely many qualitative limsups.

## 9. Common continuation for all decision depths

The crucial geometric claim is that, after retaining every incidence and clearance margin, one endpoint continuation of radius comparable to

```text
zeta^3,  zeta=min(eta,epsilon),
```

works for every layer `a`, including `a` of order `m`. The reduced physical action, displacement, collision count, Hessian bounds, and relative source density do not depend on section membership. The proof therefore omits precisely the section checks of depth at most `a` while retaining every physical-word check.

The response estimate is

```text
|grad s_j| <= C zeta^(-1) (47/53)^(3 d_j/4)
```

almost everywhere. Its constant is asserted independent of the number of omitted decision checks.

This is plausible because section cuts are not singularities of a fixed physical collision word. Nevertheless, it is one of the deepest geometric points in the revision. An independent audit should verify

- that the continuation remains a single physical-word chart after crossing an unbounded number of section cuts;
- that no accumulated multiplicity or topological obstruction enters when those cuts are glued;
- that the endpoint response constant truly does not sum over omitted checks;
- that the almost-everywhere derivative statement is sufficient at rectangle corners;
- and that the ambient density remains exactly `nu/c` after either endpoint leaves the section.

I did not identify an explicit counterexample in the stated geometry.

## 10. High-gradient transport with one retained bad mark

On the set `|grad F|>=delta`, the manuscript uses

```text
V = grad F / |grad F|^2
```

with one fixed roof width

```text
h = c min(zeta^3 delta^2, epsilon zeta delta).
```

The flow crosses only the freed section decisions. It does not cross an incidence boundary, clearance boundary, physical-word boundary, or retained deeper decision boundary.

If a contact of depth `a` is initially bad, the endpoint response gives

```text
change in s_j <= C h zeta^(-1) delta^(-1) q_0^(3a/4),
```

which is bounded by a constant multiple of

```text
epsilon q_0^(a/4).
```

Thus one bad marked strip survives the entire flow. The image lies in a positive event with the same displacement and collision count, a roof interval of fixed width, the same marked strip, and occupation in the finite allowance around `n`.

There are `O(a+1)` occupation coefficients and at most two possible marks. Applying the marked local upper bound and dividing by the fixed flow width yields

```text
m^2 ||z_a^+||_infinity
 <= C(a+1) epsilon^(1/16) q_0^(a/64)
    + C_{eta,epsilon}(a+1)m^2 rho^(m/2).
```

The exact labels remain on the left. The finite occupation enlargement is not averaged into the target coefficient.

The principal specialist issue is global injectivity of the level-to-window map after gluing all freed section cells of one physical word. The roof value determines the flow time and ODE uniqueness determines the initial point, which is the correct formal mechanism. A billiard-geometric audit should still verify that no hidden chart overlap or multiple physical representation survives the gluing.

## 11. Low-gradient critical collars retain the bad strip

The fixed-depth argument of revision 47 used normal endpoint strips and produced a constant that could not be summed over an unbounded depth. Revision 48 introduces the necessary additional ingredient: the bad depth-`a` section strip is retained throughout the completed critical collar.

A low-gradient source point is completed to its unique physical normal-to-normal center. The center is within `O(delta)` in endpoint coordinates and within `O(delta^2)` in roof value. On the completed square,

```text
s_j <= 2 epsilon q_0^(a/4)
       + C delta zeta^(-1) q_0^(3a/4)
     <= C' epsilon q_0^(a/4).
```

The collar therefore lies in a marked-strip event of the same width used in the high-gradient estimate.

Each physical collar is charged once, even if free section decisions split the return-index pieces. Distinct physical words have disjoint collars by endpoint injectivity. The collar retains its middle occupation; the free decisions introduce only the same `2a+2` allowance, not a second enlargement.

A positive marked collision upper bound on the union of the collars controls the sum of intrinsic critical coefficients. Dividing by the collar mass and applying the collar-density upper estimate gives the same summable factor

```text
C(a+1) epsilon^(1/16) q_0^(a/64).
```

I found the scaling coherent. The load-bearing assertions requiring specialist verification are

- uniqueness of the physical critical completion;
- persistence of all half-margins on the completed square;
- preservation of the bad marked strip on the entire collar, not merely at its center;
- disjointness of collars from distinct physical words;
- single charging when decision cells split one collar;
- and exact reuse of the occupation allowance.

## 12. Summing the depth layers before the collision limit

The leading layer estimates sum by

```text
sum_{a>J}(a+1) x^a
 = x^(J+1) ((J+2)/(1-x) + x/(1-x)^2),
 x=(47/53)^(1/64)<1.
```

The finite-count error in each layer is

```text
C_{eta,epsilon}(a+1)m^2 rho^(m/2).
```

Since there are at most `floor(m/2)+1` layers and

```text
sum_{a<=m/2}(a+1)=O(m^2),
```

the total error is

```text
C_{eta,epsilon} m^4 rho^(m/2),
```

which tends to zero.

This is the decisive quantifier improvement over revision 47. The source telescope is finite at every collision count, the uniform error is summed first, and only then is the collision limit taken. No unproved exchange of an infinite sum with separate limsups is used.

The resulting tail tends to zero for every `J=J(m)->infinity` at fixed physical and decision margins. This does not create a count-dependent protection theorem for the physical margins, and the manuscript does not claim one.

## 13. Bounded insertions and the all-band consequence

For a measurable source insertion `w` with `|w|<=M`, the total variation of the signed source is dominated by `M` times the positive unweighted source. This gives the same density estimate without differentiating `w` or treating a long pullback of a selector as a strong multiplier.

Once the source density itself is pointwise small, the complete signed smoothing correction follows from

```text
||f-K_B*f||_infinity
 <= (1+||K_1||_1)||f||_infinity.
```

The supremum over reconstruction bands is therefore a convolution consequence. It is not a spectral estimate at a band growing with the collision count. The auxiliary spectral band used in the proof of the density theorem remains fixed for each pair of margin parameters.

This distinction is stated correctly.

## 14. Exact reduction to the physical remainder

At equal physical and decision margins, the source identity is

```text
1-H D = H(1-D) + (1-H).
```

Thus

```text
p = f^epsilon + d^{epsilon,epsilon} + b^epsilon.
```

This ordering is important. An old first-bad-middle-decision history may contain a later physical defect. Revision 48 does not rename that entire old source as controlled. Every history with at least one incidence or clearance defect is assigned to `b^epsilon` before any physical first-defect ordering.

The physical remainder is then partitioned positively and disjointly into

- a first bad incidence source;
- a first bad clearance source.

Their variation masses are `O(epsilon^2)` and `O(epsilon)`, respectively. These are mass estimates only.

Combining the inherited protected correction with the all-depth decision theorem gives

```text
limsup_m sup_{R,n,k} m^2
 || D_B - (b^epsilon-K_B*b^epsilon) ||_infinity
 <= C B^(-1/192),
```

for `epsilon(B)=A B^(-1/12)` and sufficiently large fixed `B`.

The exponent ledger is correct:

```text
(epsilon(B))^(1/16)=A^(1/16)B^(-1/192).
```

The inherited protected payment is `O(B^(-1/2))`, so the decision term governs the displayed paid modulus.

## 15. What revision 48 has genuinely closed

Subject to specialist verification of the continuum arguments, revision 48 closes the following obstruction from the controlling report.

Every section-decision layer on the physically protected source, including a layer whose depth grows with the collision count, has normalized exact-index density bounded by a summable geometric factor. The entire section-decision source satisfies

```text
limsup m^2 ||d||_infinity <= C epsilon^(1/16).
```

Its complete signed smoothing correction is controlled for every reconstruction band and for arbitrary bounded measurable source insertions.

This is materially stronger than

- a small total-mass estimate;
- a fixed-depth endpoint theorem;
- a finite trace-jump estimate;
- or a qualitative diagonal in the endpoint depth.

The exact return index is not replaced by a packet. The discrete occupation allowance occurs only in a positive upper bound. The arithmetic moving peaks are retained.

The revision also removes a bookkeeping ambiguity in the old residual: middle-decision histories followed by a physical defect are assigned to the physical remainder, not silently absorbed into the new decision theorem.

## 16. The decisive remaining incidence obstruction

The incidence source consists of trajectories for which a graded incidence margin is small. Near grazing, the collision map loses the regularity used by the physical-word endpoint continuation. Crossing the boundary can change the collision branch and may alter the collision count in the exact return record.

The new roof flow deliberately keeps every incidence factor protected. The marked-strip theorem concerns section sides, not grazing geometry. Consequently none of the new pointwise estimates applies to the incidence source.

The mass estimate

```text
sum_{n,k} ||b_inc||_1 <= C epsilon^2
```

is favorable but insufficient. A nonnegative density of mass `epsilon^2` may concentrate on a roof set much thinner than `epsilon^2 m^2` and have height far above the local scale `m^(-2)`.

A complete proof needs a new physical grazing normal form, a pointwise coarea/Fourier estimate, or a signed cancellation theorem which is compatible with the original exact labels and arithmetic modulation.

## 17. The decisive remaining clearance obstruction

The clearance source lies near a competing-hit boundary. Crossing it changes which obstacle is selected as the next collision and therefore changes the physical center word. The reduced action and its derivative data do not glue across this boundary in the same way they glue across a section-membership cut.

Again, the revision protects every clearance margin throughout the new continuation. The mass estimate

```text
sum_{n,k} ||b_clr||_1 <= C epsilon
```

does not imply a pointwise bound or a Fourier-norm estimate.

A complete proof must control the pair or finite cluster of competing physical branches, including their exact collision labels, endpoint Jacobians, critical values, and arithmetic phases. No such transition theorem is present.

## 18. Small mass does not prove the signed correction

The remaining criterion is

```text
lim_{B->infinity} limsup_{m->infinity} sup_{R,n,k}
  m^2 esssup_{central t}
  |b^{epsilon(B)}(t)-K_B*b^{epsilon(B)}(t)| = 0.
```

The source `b` is positive before applying `I-K_B*`, but the correction is signed. Positivity therefore supplies neither monotonicity nor cancellation after convolution subtraction.

The complete finite-count exponential height bound inherited from revision 44 does not close this criterion. Combining

```text
mass <= C epsilon
```

with

```text
height <= C A^m
```

still permits concentration far above `m^(-2)`.

The manuscript states this limitation correctly. The source-manifest flags for central-scale physical-boundary smallness, full signed correction, pointwise roof-density LLT, and full raw return LLT remain false.

## 19. Arithmetic form of the main term

Revision 48 preserves the correct arithmetic formulation.

At each fixed radius the exact-index interval main term is

```text
c mathfrak a_R(k,n,m) g_{Omega_R}(Z),
```

or equivalently

```text
mathfrak a_R(k,n,m) g_{D_R}(V_n)
```

in the original return normalization.

Uniformly through changes of arithmetic type, the evaluated finite transition kernel is

```text
mathcal L_{m,R}.
```

The marked local upper bound retains all surviving resonance branches. The positive occupation allowance is not averaged into the target coefficient. A zero arithmetic class is not assigned a positive conditional denominator.

No proof is given that the actual section phase masses are uniform or that every nontrivial endpoint residue vanishes. Therefore an unmodulated radius-uniform singleton theorem remains unproved.

Any eventual pointwise roof-density theorem should state its arithmetic main term explicitly unless the concrete zero-residue criterion is established.

## 20. Fixed intervals, pointwise density, and conditioning

The article now contains several strong but distinct conclusions:

- a stationary microscopic singleton local law;
- fixed-radius exact-index arithmetic local laws for fixed roof intervals;
- a radius-uniform transition formula for those interval laws;
- an exact-event Gaussian return bridge under a microscopic denominator;
- arithmetic endpoint posteriors;
- finite-packet consequences;
- full-source labelwise reconstruction certificates;
- protected-source pointwise correction estimates;
- fixed-depth endpoint-decision deconcentration;
- and the new all-depth physically protected decision theorem.

None proves the pointwise roof-density LLT for the complete original source because the physical remainder is uncontrolled at the local scale.

A fixed positive roof interval is not a density value. An existential slowly shrinking interval is not a prescribed differentiation scale. A componentwise reconstruction certificate is not a common long-time asymptotic. A small physical-defect mass is not pointwise density smallness.

The pointwise roof-conditioned bridge remains open for the same reason: its numerator and denominator would need the missing density theorem at the same roof value and with the same physical remainder.

## 21. Weighted statements

The new all-depth decision theorem permits arbitrary bounded measurable source insertions by domination. This is a real strengthening over regular endpoint theorems which require gradient budgets.

It should not be conflated with a complete weighted raw LLT. The inherited protected weighted estimate still has its own endpoint-derivative hypotheses, and the incidence/clearance remainder is not controlled for the same insertion at the same roof value.

Nor does domination provide Gaussian amplitudes for arbitrary path selectors. A complete pointwise conditioned-path theorem would require a common physical-boundary estimate for both numerator and denominator.

## 22. Novelty and top-four significance

The new argument is technically interesting. It combines

- a collapsing-strip multiplier with no inverse-width loss;
- weak-to-strong spectral interpolation on moving arithmetic peak charts;
- an exact marked chronological pairing at arbitrary collision time;
- a finite-count local upper bound uniform in strip width and mark;
- a positive decision-depth telescope;
- roof transport retaining one bad marked strip;
- a critical-collar comparison retaining the same strip;
- and a finite error sum completed before the collision limit.

This is not merely formal bookkeeping, and it directly answers the principal interior-decision objection in the controlling report.

The article, however, is now a 323-page compilation with one hundred four core modules and many interacting theorem programs. It contains substantial completed results, but the theorem emphasized by the title and raw-inversion architecture remains incomplete. The editorial and verification burden is therefore too high relative to the completed principal claim at the requested benchmark.

Subject to independent specialist verification and substantial reorganization, the completed stationary, compact-family, interval, transition, bridge, posterior, protected-inverse, critical-cluster, endpoint-decision, and all-depth decision results could support a strong focused dynamics/probability paper. They do not yet constitute a complete top-four raw local inversion theorem.

A broader general theorem could change this assessment, but revision 48 remains specialized to the same triangular finite-horizon Lorentz family, its moving section, and the inherited anisotropic-space architecture.

## 23. Independent specialist verification

No independent human specialist audit has been obtained.

The new load-bearing items requiring expert review include

1. uniform multiplier constants as parallel strip boundaries coalesce;
2. the `s^(1/8)` weak gain in the actual strong completion;
3. the common equivalent norms and branch separation on moving peak charts;
4. the logarithmic interpolation for both projections and terminal pairings;
5. exact marked chronological pairings at `j=0` and `j=m` as well as interior marks;
6. the four-dimensional peak integral and finite-band complement;
7. continuation after freeing an unbounded number of section decisions;
8. global injectivity on the glued physical-word domain;
9. the common flow width and forbidden-boundary list;
10. retention of the bad strip through every completed critical collar;
11. physical collar disjointness and single charging;
12. reuse, rather than duplication, of the occupation allowance;
13. the uniform finite-count error before the depth sum;
14. and exact reassignment of every later physical defect to the physical remainder.

Inherited items which remain load-bearing include the collision-space anisotropic norms, physical action identity, full occupation-torus spectral theorem, strong-space faithfulness, physical projection formula, integer holonomy, moving spectral peaks, arithmetic transition expansion, endpoint response, relative distortion, critical collar estimates, protected correction theorem, and bridge tightness.

Source hashes, finite models, compilation, rendering, and exact-SHA workflow receipts do not certify these continuum arguments.

## 24. Required mathematical work for another revision at the same benchmark

A subsequent revision seeking the same benchmark should address the following.

1. **Prove the physical residual criterion.**  
   Establish the `m^{-2}`-scale signed correction estimate for the sum of the incidence and clearance sources at the original exact labels.

2. **Develop grazing transition control.**  
   Provide a physical normal form, coarea estimate, Fourier estimate, or cancellation theorem valid when the collision map approaches a grazing singularity and the collision count may change.

3. **Develop competing-hit transition control.**  
   Treat both physical branches at a clearance boundary, including their endpoint Jacobians, actions, critical data, and arithmetic phases.

4. **Close the ordered parameter ledger.**  
   Give the exact argument showing that the chosen physical protection, reconstruction band, and any new transition scale make the complete correction vanish in the ordered limit.

5. **Keep the arithmetic main term.**  
   Either prove the concrete zero-residue condition or formulate the final density theorem with `mathfrak a_R` at fixed radius and `mathcal L_{m,R}` uniformly.

6. **Complete a weighted pointwise theorem.**  
   If the pointwise conditioned bridge remains a target, prove numerator and denominator estimates for the same physical remainder and the same roof value.

7. **Obtain independent expert verification.**  
   The anisotropic spectral, singular geometry, and critical-collar chains are too load-bearing to rely only on source qualification and finite diagnostics.

8. **Strengthen the novelty comparison.**  
   State theorem by theorem which completed conclusions are not consequences of existing billiard local-limit, mixing-LLT, and suspension-flow frameworks.

9. **Reduce the central route.**  
   Present one completed principal theorem. Move unresolved companion programs out of the main route unless they are closed.

## 25. Technical comments

1. Keep collision count `m`, return index `n`, reconstruction band `B`, auxiliary spectral band `B_*`, physical margin `eta`, decision margin `epsilon`, layer `a`, tail cutoff `J`, and gradient cutoff `delta` visually distinct.
2. State the source normalization `nu/c` whenever the continuation leaves the initial section.
3. Retain the convention that occupation counts times `0,...,m-1`; terminal membership at `m` is not another summand.
4. Keep every occupation enlargement on the positive upper-comparison side only.
5. Do not describe the continuation as preserving the return index after a section decision crosses.
6. Preserve the almost-everywhere qualification for section-distance derivatives at rectangle corners.
7. State all physical and retained decision boundaries which the high-gradient flow is forbidden to cross.
8. Keep the auxiliary spectral band fixed before the collision limit and before summing depth layers.
9. Do not infer a growing-band spectral theorem from the all-band convolution consequence.
10. Preserve the distinction between the strip multiplier's uniform strong bound and its small strong-to-weak bound.
11. The square-root interpolation depends on a peak neighborhood with `|lambda|>sigma^(1/4)`; keep this local restriction explicit.
12. The marked theorem is an upper bound, not a shrinking-selector Gaussian asymptotic.
13. State that the mark and strip width may depend on `m` only because the finite-count remainder is uniform in them.
14. Keep the positive depth telescope at source level; do not replace it by a sum of separately normalized conditional laws.
15. In the low-gradient argument, state again that the same bad strip is retained throughout the whole collar.
16. Charge each physical collar once even when free decisions split its return-index pieces.
17. Do not enlarge the occupation allowance a second time after critical completion.
18. Keep the `m^4 rho^(m/2)` finite-count error visible when stating a quantitative depth tail.
19. The all-depth theorem applies to `H^eta(1-D^epsilon)`; it does not apply to histories carrying a later physical defect.
20. Preserve the exact positive identity `1-HD=H(1-D)+(1-H)` before any first-defect partition.
21. Variation-mass estimates for incidence and clearance must not be described as pointwise bounds.
22. Do not infer cancellation of physical corrections from positivity of their pre-convolution sources.
23. Keep `epsilon(B)=A B^(-1/12)` fixed before the collision limsup.
24. Preserve the arithmetic factors `mathfrak a_R` and `mathcal L_{m,R}` in every candidate raw main term.
25. A fixed interval theorem should not be cited as a pointwise roof-density theorem.
26. A bounded-insertion domination estimate should not be cited as a Gaussian-amplitude theorem for arbitrary selectors.
27. Source qualification and finite models should remain separated from continuum proof certification.

## 26. Final assessment

Revision 48 is a serious and mathematically constructive response to the revision-47 report.

It proves a width- and mark-uniform thin-strip local upper bound, converts weak strip smallness into moving-peak amplitude smallness, retains a bad marked decision through both roof transport and critical collars, and sums every decision depth before taking the collision limit. It thereby proves pointwise `m^{-2}` deconcentration for the entire physically protected section-decision source, uniformly for arbitrary bounded insertions. It also gives the exact physical-only remainder and the paid `B^(-1/192)` correction modulus.

I found no decisive error in modules 102--104 within the scope of this review.

The paper nevertheless remains short of the theorem which governs its title and raw-inversion architecture. The incidence and clearance corrections are not controlled pointwise; their small masses do not close the signed residual criterion. The full arithmetic pointwise roof-density LLT and pointwise roof-conditioned bridge remain open, and the concrete arithmetic residues are not proved trivial.

Subject to independent specialist verification, the completed stationary, interval, transition, bridge, posterior, protected-inverse, critical-cluster, endpoint-decision, and all-depth decision results could form a strong focused paper. They do not yet constitute a complete top-four raw local inversion theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**