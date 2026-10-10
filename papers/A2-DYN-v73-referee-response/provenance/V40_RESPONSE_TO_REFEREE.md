# Response to the external referee: A2-DYN revision 40

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v39-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Review commit / blob:** `a76fcf9d6ef7288ea324fed327c4f2f0ce088461` / `34fd05b1740816104f38ca84c75826b11eec1694`.  
**Reviewed author SHA:** `75eda04842b69319ae81c97ce1502129d55ee5fc`.  
**Frozen author paper tree:** `549a0879a747bf0a2506a0fb7d1fdd847d2d7577`.  
**Revised article:** `papers/A2-DYN-v40-referee-response/main.tex`.

We thank the referee for identifying exactly which fixed-coefficient statement is not supplied by the preceding Abel and source-vector estimates. This revision addresses that distinction directly. It preserves the original section, the exact return record, the physical family, the title, and the pointwise raw mixed-density endpoint. It adds three complete proof modules rather than relabeling the previous averaged estimates.

## 1. From arithmetic classification to fixed-count control

Module 84 proves the new full occupation-torus power estimates. Its geometric starting point is an already regular homogeneous inverse collision curve. Each intermediate stable image crosses a fixed number of horizontal and vertical section sides. Refining that single curve by all occupation decisions therefore creates at most `1+K m` intervals, not an exponential number of cells.

The proof checks the unstable comparison as well as the one-curve count. It removes connectors meeting a section boundary, pays the trimming cost, retains equal occupation itineraries on matched common domains, and charges all additional unmatched pieces through their terminal lengths and the original Jacobian-power sum. All three Lasota--Yorke estimates retain their explicit polynomial multiplicity. The weak powers initially have an `O(1+m)` bound; the proof does not incorrectly call this a uniform weak bound. After choosing a block length and then an equivalent-norm coefficient, a Doeblin--Fortet estimate with polynomial weak remainder gives quasi-compactness.

Bounded physical pairings exclude peripheral Jordan blocks before power boundedness is invoked. The physical Cesaro construction then represents every peripheral vector, and the measurable phase group identifies all unit-modulus eigenvalues. Local spectral stability gives uniform full-band powers and exponential decay on compact subsets of the joint nonresonant complement.

`thm:v40-uniform-resonant-reduction` inserts these splittings into the exact inverse at the specified collision count `m`. Its error is exponentially small on each fixed roof band. This resolves the request for a finite resonant decomposition plus a decaying complement. It is not a source-vector resolvent bound in disguise.

## 2. Every relevant resonance and its actual residue

Module 85 strengthens the group classification. Along stable or unstable pairs, the occupation difference is eventually zero almost everywhere: boundary-tube estimates and contraction make the mismatch probabilities summable. The occupation correction to each leaf holonomy is therefore an integer. Multiplication around almost every local product rectangle puts the roof-area phase in a countable cyclic set. The contact area has no atoms, even on positive-measure product blocks with gaps. Hence the roof frequency must vanish.

The possible group is now finite cyclic of uniformly bounded order. No nonzero roof generator remains. Triviality of this finite group is not assumed.

`prop:v40-general-residue` computes the actual spectral projection on bounded physical strong sources. The endpoint coefficient is the product of the two physical phase means. For the section-to-section pairing it is `abs(nu(eta q_gamma))^2` at every scalar eigenvalue. The general source identity retains both the nonzero displacement term and the scalar phase term. It therefore includes exactly the cases not covered by the previous pure-occupation unit-eigenvalue cancellation.

`prop:v40-resonant-curvature` differentiates the entire analytic operator family. It obtains the same centered covariance `Omega_R` at every resonance without postulating that multiplication by a merely measurable transfer function, or by the isolated forward roof, acts on the strong space.

## 3. The nonresonant full torus

The complementary powers in module 84 are actual anisotropic operator powers. Finite point spectrum alone is not used to exclude continuous near-unit spectrum: the polynomial cut bounds and compact embedding give quasi-compactness first. The finite spectral reduction covers the entire fixed band and occupation torus. Every near-unit contribution is retained in one of finitely many rank-one local branches.

The partition is made in the joint parameter-frequency space. A branch is kept throughout its chart even when its modulus becomes less than one at a nearby radius. Consequently the uniform reduction does not silently assume a continuous choice of an exact resonance generator or a uniform gap on a fiberwise complement whose distance from resonance tends to zero.

## 4. Fixed coefficients, not Abel averages

The new inverse uses `T_theta^m` at the requested integer `m`. The v39 partial sums and Abel identity remain in the article but play no role in passing to this coefficient.

At a fixed radius, the finite group has occupation generator `2 pi/d`, displacement generator `2 pi a/d`, and scalar phase `2 pi h/d`. Normalize its transfer function by `q_*^d=1`, and let `w_l` be the collision measure of the section phase class `q_*=exp(2 pi i l/d)`. The exact nonnegative factor is

`a_R(k,n,m) = (d/c^2) sum_l w_l w_(l+a.k+n+h m)`.

Theorem 5 proves, for each fixed positive roof interval `J`,

`n^2 P{K_n=k, N_n=m, T_n-t in J} = |J| a_R(k,n,m) g_D(V_n) + o_R(1)`.

The error is uniform over central target compact sets at each fixed radius. The finite Fourier calculation shows that the factor averages to one over `d` consecutive return indices. If it is zero, the unchanged exact event is null; on positive classes it gives a positive microscopic denominator. Regular endpoint weights have the corresponding cross correlation of phase-class masses.

This is an exact-index interval law, not a diverging-index window theorem. It also identifies the old signed remainder: its leading term is proportional to `a_R-1`. Without a proof that all nontrivial section residues vanish, that term must not be set to zero. The original unmodulated radius-uniform raw target remains in place rather than being quietly redefined to match this arithmetic theorem.

## 5. Pointwise roof inversion

The new proof fixes the Fourier band, takes `m` to infinity, and only then enlarges the band through positive interval envelopes. It establishes a fixed positive interval, not a pointwise roof density. No new estimate of the complete second-derivative coarea sum, every critical edge, or the far roof tail is asserted.

The common pointwise correction and full roof-frequency estimates retain their original roles in `thm:LLT`. This revision therefore does not claim full closure of the raw mixed-density theorem. It closes a different, precisely identified step requested by the report: long-power control and explicit fixed-count arithmetic inversion on each roof band, followed by a fixed-radius sharp-interval law.

## 6. Constants and parameter quantifiers

The three-norm and nonresonant power constants depend on a fixed roof band and, where relevant, a compact subset of the joint nonresonant locus. Occupation ranges over its entire real torus. Uniformity in the table parameter always uses a finite cover of local common spaces, not one unproved global norm.

The finite spectral reduction is radius-uniform. The displayed arithmetic Gaussian asymptotic is `o_R(1)` at fixed radius. A transition where a resonance appears or disappears may contain a near-resonant branch whose decay is not uniform at the collision scale. That branch is kept in the uniform formula. No polynomial local-limit rate, no growing-band spectral estimate, and no globally continuous resonance generator are claimed.

The selected theorem uses multiplier-bounded section endpoint functions. It is not a Gaussian amplitude theorem for an arbitrary path-dependent selector. Total variation retains the convention already fixed in the article.

## 7. Independent specialist verification

No independent human audit has been obtained in this author revision. `SPECIALIST_AUDIT_MAP.md` identifies the new geometric matching and holonomy steps, the spectral continuation, and the inherited continuum inputs requiring that audit. Finite tests check signs, normalization, residue arithmetic, cut-count algebra and spectral-model logic. They do not certify continuum billiard estimates.

## 8. Generality and novelty

Finite arithmetic factors and local limit theorems with endpoint residues are classical structures, and no historical priority for them is claimed. The change in this article is a full-torus realization for the true rectangular section occupation, based on polynomial refinement of actual collision curves, followed by an exact fixed-return-index law. This is not the constant collision-step cocycle or the stationary age-overlap theorem under a new name.

The physical endpoint formula also explains why the previously proved fine-index windows recover the unmodulated Gaussian: a diverging window averages a finite periodic residue factor. The earlier source cancellation is retained as an exact special case, not elevated to a general resonance cancellation assertion. The prior-art comparison with the billiard, mixing-LLT, suspension and perturbative frameworks remains in Part I; the new section states its specific additional role without claiming that the whole framework is new.

## 9. Article structure and preservation

The direct Part II route now points to Theorem 5 and its three proof modules. The full inherited geometry, Gaussian and functional laws, marked moments, local windows, source identities, raw edge extraction and raw inversion statements remain compiled. All 83 inherited core files, all 95 inherited Python files, the bibliography, and the A--X synopsis are byte-identical. The v39 main source, reply, proof ledger and manifest are archived under `provenance/`. No old branch or review is overwritten.

The paper remains a unified study of the original actual-return problem; it has not been replaced by a specialist-venue paper or a new topic. The new exact-index interval theorem is stated alongside, not in place of, the original pointwise target.

## Technical comments and exact qualification

The torus quotient metric is explicit in module 84. The proof retains the order of measurable approximation and time limits. Mixing and ergodicity have separate roles in the peripheral argument. Zero roof means the frequency coordinate `b=0`, not zero flight time. The finite group is not declared trivial. The old degenerating source denominators, the `|omega|/(1-r)` term, the initial factor `z`, and the half-open `[0,m)` convention are untouched. The new residue calculation treats nonunit scalar phases explicitly.

The baseline is the exact v39 author SHA stated above, whose response run is `37703491265`, artifact `11518588432`, and archive digest `b954a00c3f77593b17a9af621d48415b780686639b37c66f21340c5c30f7373c`. These identify the baseline, not the v40 execution. The v40 read-only workflow archives the exact author source and controlling report, verifies source identity and finite diagnostics normally and under `-O`, typesets the complete manuscript, and renders the new proof pages. Its dynamic receipt records the actual event SHA, run ID, PDF hash and source cleanliness. No future run or independent proof audit is predeclared successful.
