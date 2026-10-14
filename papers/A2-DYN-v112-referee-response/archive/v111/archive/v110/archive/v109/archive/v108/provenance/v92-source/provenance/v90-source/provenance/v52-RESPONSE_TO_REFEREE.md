# Response to the external referee: A2-DYN revision 52

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v51-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `f3c14d327837289fd44d3824d0447c010565aba2` / `a46a201ebef4fcc56e4b80df5494d7358389e42a`.  
**Reviewed author commit:** `39ee9d88831a574a519785407732b3872ccbca3b`.  
**Frozen complete author paper tree:** `39ddc1f7c3be0c3010dc1388a5aeddd7789a4075`.  
**New article:** `papers/A2-DYN-v52-referee-response/main.tex`.

We thank the referee for distinguishing the one-sided density theorem from the missing upper height and for requiring a numerator at the same roof coordinate in the bridge problem. We preserve the original four-coordinate actual-return target and its arithmetic main term. This revision supplies a path-valued raw numerator on the complete source. Its unconditional conclusion is a roof-integrated path-dual local law and a same-roof bridge in conditional mean. Its pointwise conclusion shows that the existing scalar positive-height condition suffices for the uniform bridge; it does not assert that condition.

## R1--R3. Incidence height, clearance height and the two-sided scalar endpoint

The report's objection is correct: positive narrow spikes are compatible with the existing local-variation theorem and the one-sided lower law. We do not turn a small mass into an essential-height estimate. The positive first-physical-defect split, including all later decision defects, remains unchanged. Neither physical seam is crossed in the new proof.

There is a new simultaneous numerator result. Theorem `thm:v52-path-remainder` proves, at each fixed reconstruction band, that the **whole path-density measure** minus the arithmetic reference bridge measure is approximated in essential supremum of bounded-Lipschitz dual norm by the original positive physical path measure. Its mass is exactly the v51 scalar physical remainder. The source is the same for every path test; it is not selected after the test or after the roof. This is a measure-valued strengthening of the v51 representation, not an extra height hypothesis.

The normalized ordered error is `O(B^(-1/192))`, with `epsilon(B)=A_0 B^(-1/12)` fixed before the collision limit. It follows that the scalar height condition is sufficient for all bounded-Lipschitz pointwise path numerators as well. The two scalar positive component heights themselves remain unclosed. The complete raw-return, upper pointwise, full correction and forward-likelihood flags stay false.

## R4. A numerator and conditional path law at the same roof value

This is the principal new theorem-bearing response. The proof does not differentiate a fixed-window bridge theorem by its interval length.

**Endpoint admissibility.** On a protected endpoint chart, every prefix roof satisfies `d S_j = -p_0 d a + p_j d y_j`. The inherited contact response bounds its derivative independently of the word length. All displacement and occupation prefixes are constant on that chart. Consequently the map from the two endpoint contacts to the *entire* pinned collision path has Lipschitz constant `C epsilon^(-1) m^(-1/2)` in the path supremum metric. Composition with every unit bounded-Lipschitz path test is eventually admissible with the same protected derivative budget. This includes nonsmooth Lipschitz functionals of the full path; it excludes arbitrary measurable path selectors.

**Uniform path factorization at fixed band.** Lemma `lem:v52-fixed-band-path` strengthens the inherited cylindrical calculation to the whole bounded-Lipschitz unit ball. A fixed positive band-limited function dominates the absolute value of the reconstruction kernel. The chronological fourth-derivative argument gives tightness of the resulting positive finite path measures. Cylindrical factorization and tightness then identify every signed-measure subsequential limit as its scalar mass times the Gaussian bridge. Equicontinuity on compact path sets yields the uniform path norm. This is the step which a mere finite-dimensional statement would not supply.

**Raw path-valued local variation.** The protected correction, the complete decision estimate and the physical local-variation bound apply to that common class. They prove convergence of the integral, over each translated fixed roof window, of the bounded-Lipschitz dual norm of the raw path-density error. The path test may now be chosen measurably after the roof value. The proof first obtains a common pointwise norm using a countable norming class; it never differentiates a roof-dependent selection.

**The actual return clock.** Lemma `lem:v52-return-transfer` uses the exact identity `theta_l-l/n = -(sqrt(m)/n) B_4(theta_l)` on the original event. The unnormalized microscopic fourth moment gives tightness even when an exact event mass is small. The pinned time change transfers the path-valued local law to the actual return bridge with covariance `D_R`, without modifying the roof or the return index.

**Same-roof disintegration.** Theorem `thm:v52-same-roof-mean` concerns regular conditional path kernels at their own roof coordinate `u`. Their bounded-Lipschitz distance to the Gaussian bridge tends to zero in mean under the original conditional roof law, uniformly on central targets with positive integrated arithmetic reference mass. The same holds under the reference roof law. Hence the bridge convergence is uniform outside target-dependent roof sets of conditional probability tending to zero. This is stronger than convergence of only the path mixture over a fixed interval; it is not convergence at every prescribed roof value.

**What the scalar criterion would finish.** Proposition `prop:v52-pointwise-path-charge` charges the same-roof conditional collision-path error to twice the exact posterior probability of the physical defective source, plus the ordered small error. If the v51 scalar height criterion is established, the full uniform essential-supremum bridge follows, including its actual-return-clock version, on positive-reference central sets. Thus a second independent pointwise bounded-Lipschitz numerator obstruction is no longer required. We do not claim an unconditional uniform pointwise bridge while the scalar heights remain unproved.

## R5. Arithmetic and normalization

Every uniform formula retains `mathcal L_{m,R}`. The fixed-radius specialization retains `c mathfrak a_R g_{Omega_R}`, with central restrictions and positive-residue conditions where division occurs. No section residue is assigned the value one. The integrated mean theorem uses `int_I (G)_+ >= d h`; the pointwise conditional estimate separately uses `G(u)>=d`. These are not conflated. The original section probability supplies the single factor `1/c` throughout. The kernels condition on exact n,k,m and their own roof, not on an averaged index or a substitute event.

## R6. Specialist audit

No independent human audit has been obtained. The new specialist map separates three new continuum interfaces: the endpoint-to-path Lipschitz estimate, the positive band-envelope fourth moment on finite path measures, and the uniform signed path-measure compactness passage. All depend on the pinned inherited collision/occupation spectrum, action geometry and raw source partition. Finite tests verify algebra and finite models, not these continuum inputs or the missing physical height.

## R7. Generality and theorem-level significance

The result is not advertised as a new ordinary Gaussian bridge or as historical priority for mixing local limits. Existing cell-index and suspension local-limit theories, discussed with exact references in the retained literature section, do not by themselves justify taking a measurable roof-dependent path test after conditioning on this exact four-coordinate source. This revision proves that stronger norm passage within the present physical and arithmetic framework.

The new mechanism is a uniform endpoint Lipschitz estimate for an entire path map, plus fixed-band tightness and common positive-source reconstruction. It yields a reusable path-valued extension when those hypotheses are available; we do not invent independent applications or claim a broad singular-hyperbolic theorem solely by renaming the hypotheses. The original pointwise raw endpoint is retained rather than replaced by a different topic or venue target.

## R8. Direct route, preservation and qualification

The new theorem is stated in the front matter with a four-interface route. The two new modules contain the proofs, with no new chain of historical status modules. All 109 inherited core modules, all 139 inherited Python scripts, the bibliography and the three compiled appendices are byte-identical. All inherited labels and A--X statements remain compiled. The former main source and principal records are archived verbatim under provenance.

The new revision branches start at the actual v51 review commit. The read-only workflow verifies that exact report blob and the full v51 baseline tree, reruns the inherited finite checks, compares normal/optimized outputs, builds the full article and renders the new label-selected pages. Every final receipt is tied to the actual event SHA and run. No successful remote execution is asserted by this static response in advance.

## Technical comments 1--16

All pointwise norms remain essential norms with common almost-everywhere versions. The central restrictions, arithmetic kernel, fixed-band order and separate auxiliary band remain explicit. The physical remainder is positive but is not called small in height. A regular conditional density/kernel does not assign positive probability to a singleton continuous roof event. Mean bridge convergence, fixed-window minorization and the conditional pointwise implication are stated separately. Reverse and forward likelihood directions remain unchanged. The v50 freeze remains provenance only. Source identity, finite diagnostics, native build and independent mathematical verification remain distinct.
