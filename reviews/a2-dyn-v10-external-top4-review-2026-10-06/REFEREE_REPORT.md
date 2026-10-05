# External top-four referee report on A2-DYN revision 10

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v10-referee-response-2026-10-05`, `revision/a2-dyn-v10-referee-copy-2026-10-05`  
**Reviewed commit:** `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`  
**Reviewed repository tree:** `c9893bd1d53e8c3f978a9e3e8e4388934735792d`  
**Active manuscript directory:** `papers/A2-DYN-v10-referee-response`  
**Active core tree:** `66cf9b07589443f8b7380199275ac801e738dba5`  
**Substantive revision commit:** `133c0e05d9a7d41034e688bcbbced7674d7dd335`  
**Controlling earlier report:** `reviews/a2-dyn-v9-external-top4-review-2026-10-05/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `8448e718a22658c94dcb654b52c69b44f9889fe1` / `14539536556fc1d041cc30917296708084146259`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 10 is a genuine and technically substantial revision. It does not merely repackage the Gaussian and functional limit theory proved in revision 9. The new main result establishes, for the actual deterministic first-return record and uniformly in the disk radius, an integrated Gaussian comparison on a polynomially expanding ball of rescaled Fourier frequencies:

\[
 \sup_R\int_{|v|\le 2n^{1/200}}
 \left|C_{n,R}(v)-e^{-v^{\mathsf T}D_Rv/2}\right|\,dv
 \le Cn^{-3/280}\sqrt{\log(2+n)}.
\]

The theorem also treats complex initial insertions with uniformly bounded supremum and initial-coordinate BV norms. The proof retains the physical stopping time, tracks the frequency dependence of every smoothing, covariance, spectral-amplitude and stopping error, and does not assume a spectral expansion for the unbounded induced operator. The revision additionally supplies detailed proofs of the one-collision BV estimate, the local collision-space density embedding, chronological products of differently twisted collision operators, short-block treatment, complex fourth-derivative bounds and coarse polygonal interpolation.

On the new arguments I audited, I found no decisive counterexample. The four-dimensional frequency-volume bookkeeping is coherent, the explicit exponent range is nonempty, and the final clarification of the initial-density class removes an ambiguity in the finite-dimensional product corollary. The exact raw-inversion corollary also states its remaining hypotheses rather than presenting the growing central band as a complete local limit theorem.

The negative recommendation is therefore not based on the absence of mathematical progress or on a detected fatal flaw in Theorem B. It is based on the continued gap between the paper's organizing endpoint and the unconditional theorem presently proved. The parameter-uniform raw mixed-density LLT, its weighted forms, and the exact-event conditioned physical-time consequences still require three major ingredients:

1. uniform positive definiteness of the four-dimensional covariance, including a regularity theorem that makes the zero-variance transfer function evaluable on the selected periodic orbits;
2. an integrated estimate on the entire complementary frequency region, including the annulus between the new central cutoff and the previously contemplated outer regime;
3. a complete critical/singular branch decomposition with quantitative, return-count-dependent residual derivative sums and local edge bounds.

These are not routine clean-up items. They are the remaining mechanisms that turn a growing central Gaussian integral into the raw density theorem advertised by the title and final synthesis. At the requested benchmark, proving one central part of the Fourier inversion while leaving nondegeneracy and the full complementary-frequency/residual analysis conditional is not sufficient for acceptance.

The compensation-and-stopping method is elegant and potentially useful beyond this particular paper. In its present form, however, it is developed for one specially constructed four-coordinate record in one triangular Lorentz family, and the manuscript does not yet extract a general theorem with several substantial applications that could independently support a top-four claim. A carefully reorganized paper centered on the unconditional Gaussian, functional and growing-major-arc results could be a strong specialist contribution after independent expert verification, but that is a different editorial standard from the one requested here.

## 2. Frozen source, chronology and version identity

Both named revision-10 branches resolve to the same commit:

`3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`.

The substantive revision is its parent

`133c0e05d9a7d41034e688bcbbced7674d7dd335`,

which is based directly on the revision-9 review commit. The final reviewed commit makes a narrow but useful correction: it states that the finite-dimensional smoothing passage is uniform for initial probability densities with uniformly bounded supremum and variation norms, while only the deterministic short-increment estimate uses the supremum bound alone. It updates the corresponding source hash.

Revision 10 preserves all twenty-four mathematical core files of revision 9 byte for byte and adds three new mathematical files:

- `core/25_uniform_bv_details.tex`;
- `core/26_functional_details.tex`;
- `core/27_growing_major_arc.tex`.

The complete article includes each of the twenty-seven core files once. Earlier manuscripts, earlier reviews and unrelated repository paths remain present. The source manifest identifies the reviewed revision-9 commit, the controlling report commit and blob, the inherited core tree, the new core hashes, and the fact that neither the full raw LLT nor uniform positive definiteness is claimed.

The exact-source workflow completed successfully on both reviewed revision branches at the reviewed SHA. The local and remote records report a 69-page native article, 27 unique core inclusions, 91 proof environments and 266 labels, with the twenty-four inherited core files unchanged. These facts establish source identity and reproducibility of the build. They do not establish the continuum billiard arguments.

The present review branch starts from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v10-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, previous review or unrelated repository path is modified.

## 3. What revision 10 actually proves

The revision builds on the revision-9 collision compensation

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

and the exact stopping identity

\[
 J_{n,R}-n\bar G_R=S_{N_{n,R},R}h_R.
\]

The previous revision used these identities to prove a continuous positive-semidefinite covariance, a quantitative compact-frequency characteristic estimate, Gaussian weak convergence, a zero-variance coboundary characterization and functional limits.

Revision 10 makes the compact-frequency estimate quantitative in the frequency radius. Its principal unconditional additions are:

- a uniform BV proof for the one-collision record and section indicator in initial collision coordinates;
- explicit embeddings of smooth relative densities and multiplier/test pairings into the local Demers--Zhang collision spaces;
- an explicit collision characteristic estimate in which all powers of the real rescaled frequency are retained;
- a stopped finite-ball estimate for the actual first-return record;
- an integrated comparison on the ball `|v| <= 2 n^(1/200)` with a decaying four-dimensional L1 error;
- the same central estimate for complex initial insertions supported in the section with uniform `L-infinity + BV` bounds;
- a conditional exact raw-inversion corollary that replaces an assumed small-frequency induced spectral expansion by the proved central band.

The theorem is stronger than a pointwise CLT. It gives precisely the type of integrated central estimate needed to control the central inverse Fourier integral uniformly in the observation variable. It is nevertheless only the central term of the exact decomposition.

## 4. Audit of the uniform one-collision BV argument

The first new appendix expands a load-bearing step that was compressed in revision 9.

The finite-center lemma uses the uniform free-flight bound to place every possible next lattice center in a fixed Euclidean ball. Since the triangular lattice is discrete, this gives a finite candidate set independent of the initial state and radius.

In rational angular charts, the outgoing velocity, candidate entry roots, admissibility inequalities and comparisons of finitely many candidate roots form bounded semialgebraic families in the radius and initial coordinates. Parameterized cell decomposition and one-dimensional monotonicity then give a uniform bound on the number of monotone fiber pieces. Because each fiber is bounded, its variation is uniformly bounded. Applying this separately in both coordinate directions and using Fubini/integration by parts yields finite distributional derivatives in the rectangle. The treatment of zero extensions accounts for boundary jumps.

The chart-gluing argument is also logically appropriate. A fixed partition of unity prevents artificial jumps at chart boundaries, bounded coordinate changes preserve BV up to a uniform constant, and the argument remains in the flat `(alpha,p)` collision coordinates. The moving section contributes only the perimeter of finitely many rectangles. Values assigned on singular or tie sets are lower-dimensional and do not affect the almost-everywhere function or its distributional derivatives.

I found this argument coherent. Two points remain appropriate for specialist checking:

1. the precise semialgebraic description of all competing-root and first-entry conditions near grazing and tangency;
2. the passage from the rectangular two-scatterer cover to the original triangular quotient in the imported collision-space framework.

These are verification requests, not detected contradictions. The manuscript correctly does not infer from this initial-coordinate first variation any second-derivative estimate for a many-return pushed-forward density.

## 5. Audit of the collision-space embeddings

Lemma A.4 makes explicit the convention that a smooth function `a` represents the density `a dnu` relative to the invariant reference probability, rather than an unweighted area density with an additional cosine factor. This convention is essential near grazing.

The weak and strong stable estimates follow from bounded stable-curve lengths and the admissible test normalization. The unstable comparison uses matched graph curves, `C1` control of the density and the source exponent `beta<1`. The multiplier estimate separates the old matched-test difference from the difference between the two restrictions of a `C2` multiplier and uses the exponent inequality `beta<1-q`. The resulting bounds give

\[
 \|a\nu\|_{\mathcal B_j}\le C\|a\|_{C^1},
 \qquad
 \|M_gV\|_{\mathcal B_j}\le C\|g\|_{C^2}\|V\|_{\mathcal B_j},
\]

and, after smoothing,

\[
 \| (\mathsf S_\delta a)\nu\|_{\mathcal B_j}
 \le C\delta^{-2}\|a\|_\infty.
\]

This is the correct kind of estimate needed for the spectral amplitude and complementary-power terms. It is also the most source-dependent part of the new proof. A specialist should compare the claimed density embedding, matched-curve metric, exponent inequalities and mass functional directly with the precise local spaces being used. The source map supplied by the authors is useful, but it is not a substitute for this independent check.

Importantly, the appendix does not claim that the hard section projection is a bounded multiplier on the anisotropic space and does not construct the unbounded induced twist there.

## 6. Audit of the chronological product and functional details

The second appendix satisfactorily addresses several proof-presentation concerns from the previous report.

For a fixed number of consecutive blocks, the product

\[
 L_q^{m_q}\cdots L_1^{m_1}
\]

is expanded into principal and complementary terms in physical chronological order. A complementary term pays one initial-vector factor `delta^-2` and one exponential factor `rho^(m_j)`; the remaining fixed number of projectors and powers are uniformly bounded. The all-principal product is telescoped around the rank-one unperturbed projection. Combining the projector displacement `O(delta^-2 |z_j|)` with the smoothed initial-vector norm produces the stated `delta^-4 sum |z_j|` amplitude loss. No spurious `delta^(-2q)` factor is introduced.

The treatment of zero and short blocks is also correct in form. A zero block is the identity and is omitted before the spectral expansion. A deterministic short block is removed directly by its collision-space second moment, without pretending that it has a long complementary spectral power or shifting the other blocks in time. The final reviewed commit now states the correct initial-density class for the smoothing part of this argument.

The complex fourth-derivative lemma records a uniform complementary bound on a complex disk before using Cauchy's estimate. The coarse interpolation proposition uses a first fractional block, a complete-block middle interval and a last fractional block. The `L4` triangle inequality keeps the constants independent of the number of coarse blocks. The deterministic fine/coarse difference is of order `L/sqrt(n)`.

I found no fatal defect in these additions. They materially improve the reviewability of the revision-9 functional proof.

## 7. Audit of the frequency-explicit collision estimate

Lemma `lem:explicit-frequency-error` is the analytical core of revision 10. It proves, under the explicit analytic-radius and cubic-remainder restrictions,

\[
\begin{aligned}
 &\left|\int a\,e^{it\cdot S_mh_R/\sqrt m}\,d\nu
 -\left(\int a\,d\nu\right)e^{-t^{\mathsf T}\Gamma_Rt/2}\right| \\
 &\quad\le C\bigg[
 \delta+|t|\sqrt{\delta\ell_\delta}
 +|t|^2\delta\ell_\delta
 +\frac{|t|\delta^{-4}+|t|^3\delta^{-6}}{\sqrt m}
 +\delta^{-2}\rho^m\bigg].
\end{aligned}
\]

The individual terms have identifiable sources:

- `delta` from smoothing the initial insertion in `L1`;
- `|t| sqrt(delta ell_delta)` from removing smoothing of the observable using the small-residual variance estimate;
- `|t|^2 delta ell_delta` from replacing the smoothed covariance by the physical covariance;
- `|t| delta^-4 / sqrt(m)` from the perturbed spectral amplitude and smoothed initial-vector norm;
- `|t|^3 delta^-6 / sqrt(m)` from the cubic eigenvalue remainder;
- `delta^-2 rho^m` from the complementary power.

The proof correctly uses the positive-semidefinite covariance only to keep the real quadratic principal factor bounded. It therefore remains valid when the limiting covariance is singular. Signed and complex insertions are handled through absolute values and a uniform supremum bound.

The stated analytic restrictions are consistent with the later power-law choices. I found no missing four-dimensional volume factor at this stage; those losses are introduced only after integration.

## 8. Audit of stopping at the actual return time

The stopped estimate retains the exact physical return clock rather than replacing it by an independent or deterministic number of excursions.

With

\[
 m_n=\lfloor n/c_*\rfloor,
 \qquad b_n=\lceil n^{3/5}\rceil,
\]

the return-clock window gives an exceptional probability of order `n/b_n^2 = n^-1/5`. On its complement, the forward and backward deterministic-window maximal estimate yields a characteristic error

\[
 C\left[n^{-1/5}+|v|n^{-1/5}\log(2+n)\right].
\]

The proof does not attempt to control an unbounded stopped sum on the exceptional event. The bounded insertion reduces the exceptional contribution directly to the unweighted return-clock probability. This is the correct strategy.

At deterministic time `m_n`, the collision estimate is used with the rescaled frequency `t=v sqrt(m_n/n)`. The covariance `(m_n/n) Gamma_R` differs from `D_R=c_*^{-1}Gamma_R` by order `1/n`, producing an integrated `n^-1 U^6` contribution. Integration over a four-dimensional ball correctly changes a factor `|v|^j` into `U^(4+j)`.

The resulting finite-ball estimate lists all polynomial contributions separately. This transparency is a strength of the revision.

## 9. Audit of the growing-band exponent balance

The proof chooses

\[
 U=n^\varepsilon,
 \qquad \delta=\tfrac14n^{-\theta},
\]

with

\[
 0<\varepsilon<1/134,
 \qquad
 10\varepsilon<\theta<\frac{1/2-7\varepsilon}{6}.
\]

The analytic-radius conditions reduce to strict linear inequalities that follow from the displayed range. After integration, the three slow margins are

\[
 \frac\theta2-5\varepsilon,
 \qquad
 \frac12-6\theta-7\varepsilon,
 \qquad
 \frac15-5\varepsilon.
\]

The interval for `theta` is nonempty exactly when `67 epsilon < 1/2`. At

\[
 \varepsilon=1/200,
 \qquad \theta=1/14,
\]

the margins are

\[
 3/280,
 \qquad 51/1400,
 \qquad 7/40.
\]

The first is the minimum and carries the square-root logarithm. The remaining logarithmic terms have a strictly better polynomial margin and can be absorbed. I independently checked the algebra of these exponents and found it consistent with the nine terms in the stopped finite-ball estimate.

Thus Theorem B is, in my assessment, a real theorem-level advance over revision 9 rather than a restatement of compact-frequency weak convergence.

## 10. Audit of the insertion into exact raw inversion

The new corollary uses the inherited exact decomposition

\[
 p_{n,R}=K_n*\mu_{n,R}
 +(e_{n,R}-K_n*E_{n,R})
 +\mathcal F^{-1}[(1-\chi_n)H_{n,R}].
\]

With `a_n=n^(1/200)`, the support of the cutoff corresponds after `v=sqrt(n) omega` to the frequency ball covered by Theorem B. Multiplying by the physical Jacobian `n^2` cancels the four-dimensional Fourier rescaling. The integrated major-arc estimate therefore controls the central convolution uniformly in the observation variable. Assuming `D_R >= d_0 I`, the omitted Gaussian tail is uniformly negligible.

The argument correctly retains two further terms:

- the complementary transform integral of the residual;
- the local density and convolution errors of the extracted edge measure.

It also first uses `H in L1` to obtain an actual mixed density, so the conclusion is not merely a theorem about a smoothed observation.

The corollary is mathematically useful, but it is conditional. In particular, the physical radius of the proved central band is

\[
 n^{-1/2+1/200}=n^{-99/200}.
\]

The earlier outer-tail discussion began at `n^-2/5`. Since

\[
 n^{-99/200}<n^{-2/5},
\]

there is a genuine intervening annulus. The revision explicitly acknowledges this point. Consequently the new theorem does not close the complementary-frequency problem by combining automatically with the old outer estimate.

## 11. Uniform positive definiteness remains open

Revision 9 proved that the kernel of `D_R` is exactly the set of directions for which the centered induced observable is an `L2` coboundary. Revision 10 does not strengthen the regularity of the transfer function.

The selected periodic orbits form a zero-measure set. An `L2` equivalence class cannot be evaluated on those orbits without an additional regularity theorem. The periodic rank and phase-separation calculations therefore still do not imply that `D_R` is positive definite. The new growing-band theorem deliberately allows singular covariance; the raw inversion corollary separately assumes `D_R >= d_0 I`.

For the full raw four-dimensional LLT, this is a major unresolved issue. The authors need either:

- a Livšic-type regularity theorem applicable to the actual discontinuous induced observable and its billiard singularities;
- a direct periodic approximation argument producing a representative on the selected periodic points;
- or a different proof of nondegeneracy that avoids pointwise evaluation of the measurable transfer function.

Continuity plus pointwise semidefiniteness is not enough.

## 12. The complementary-frequency problem remains open

The central result now covers a polynomially expanding rescaled ball. Outside that ball, the raw inversion needs an integrated estimate of order `o(n^-2)` in physical frequencies after removal of the explicit edge terms.

The missing region includes:

1. the annulus between `n^-99/200` and the beginning of any previously available minor-arc regime;
2. compact nonzero torus frequencies coupled to the continuous roof frequency;
3. growing and large roof frequencies where the periodic phase separation must be converted into an actual operator contraction or resolvent estimate;
4. the far tail where the derivative growth of the raw residual decomposition must be combined with physical-count truncation.

The exact renewal identities and one-step periodic coercivity remain valuable compatibility constraints, but they do not construct the anisotropic induced family or prove phase reconstruction from approximate spectral vectors. Revision 10 removes the induced spectral hypothesis from the central band only.

A future proof must provide actual constants and verify a strict splice. Phrases such as “take the intermediate cutoff small” and “then take the derivative order large” are not sufficient unless the competing exponential growth constants are displayed and leave a nonempty interval.

## 13. The complete critical/singular residual sum remains open

The paper retains a correct distinction among three different kinds of estimates:

- deletion of high physical collision counts in total variation;
- first variation of the one-collision record in initial coordinates;
- second distributional derivatives of the one-dimensional roof densities after many-return coarea pushforward.

Only the third type directly yields the `1/b^2` Fourier decay required for absolute roof-frequency integration of the residual. Revision 10 does not classify and sum all regular critical words, central critical branches, competing-root boundaries, grazing boundaries and other singular itinerary boundaries. It also does not prove the actual `n`-dependence of the total residual derivative norm.

The individual edge coefficients and exact subtraction of selected jumps remain useful, but a global theorem must show that every nonintegrable jump has been extracted and that the remaining second-derivative norms are absolutely summable with constants compatible with the frequency splice.

This is a principal theorem still missing from the advertised raw LLT, not a routine appendix.

## 14. Weighted limits and exact conditioning

The new insertion class is nontrivial but limited. It consists of complex functions of the initial collision state, supported in the section, with a uniform collision-coordinate `L-infinity + BV` bound. The central integral is uniform over this class, including `n`-dependent choices with the same norm bound.

This does not automatically cover:

- terminal-state insertions;
- multiple-time path insertions;
- indicators of exact final lattice values;
- insertions whose BV norm grows with `n`;
- the relative error needed to replace one shrinking exact conditioning event by another.

For such applications one still needs weighted complementary-frequency and edge estimates. The same-event conditioned unfinished-block theorem does not authorize changing the conditioning event. The manuscript states this boundary correctly.

## 15. Top-four significance assessment

The unconditional package is now stronger than in revision 9:

- continuous collision covariance;
- actual-return Gaussian and functional laws;
- measurable coboundary characterization of the kernel;
- an integrated growing major arc for the actual unbounded induced record;
- an exact conditional route from that central theorem to raw inversion.

The compensation identity and stopping method are conceptually appealing. The growing-band theorem is tailored closely enough to raw inversion that it has more significance than an ordinary CLT.

Nevertheless, at the requested benchmark, the manuscript still presents a program whose central density theorem is conditional on three major new results. The proven major arc is one component of a local limit proof, not the local limit theorem itself. The remaining nondegeneracy, complementary-frequency and singular-branch problems are precisely the hard mechanisms that prevent central Gaussian asymptotics from determining a raw density.

Nor does the current manuscript formulate and prove an abstract theorem showing that bounded collision compensation systematically transfers growing major arcs to broad classes of induced hyperbolic records. Such a general theorem, together with several substantive applications, could change the significance assessment even before every model-specific raw LLT is finished. The present paper remains highly specialized to the chosen triangular family and section.

My top-four recommendation therefore remains negative, despite the substantial advance and the absence of a fatal error in the new central proof.

## 16. Required work for a future top-four resubmission

A future resubmission at the same benchmark should, at minimum, accomplish the following.

1. **Prove uniform covariance nondegeneracy.** Establish a periodic-evaluable regularity theorem for the zero-variance coboundary or provide another uniform proof that `D_R >= d_0 I`.
2. **Close the entire complementary-frequency integral.** Cover the intervening annulus, compact minor arcs, growing roof frequencies and far tails with compatible uniform constants.
3. **Construct the actual high-frequency operator mechanism.** Either realize the unbounded induced twists on suitable anisotropic spaces and prove Fredholm/phase-reconstruction estimates, or replace that route by another theorem with equivalent quantitative conclusions.
4. **Complete the global raw branch decomposition.** Classify all relevant critical and singular branches, extract every nonintegrable edge, and prove the true `n`-dependent derivative sums.
5. **Verify the strict frequency splice.** Display numerical or symbolic inequalities among the actual spectral, branch-growth and derivative-growth constants.
6. **Extend the weighted theory needed for conditioning.** Prove complementary tails and edge estimates for the terminal or multiple-time insertions used in the intended exact-event applications.
7. **Obtain an independent specialist proof review.** In particular, the Demers--Zhang local-space identification, semialgebraic BV argument, singular boundaries, smoothing embeddings and growing-major-arc proof should be checked by an expert in dispersing billiards and anisotropic transfer operators.

If the authors instead submit the unconditional Gaussian/functional/major-arc package as a self-contained specialist paper, the introduction, title and theorem hierarchy should be reorganized around that accomplished result, with the raw LLT clearly separated as a future application. That editorial alternative does not weaken the mathematics; it changes the theorem by which the paper is judged.

## 17. Presentation and technical comments

1. Keep the distinction between the unnormalized collision measure `nu` and the normalized section probability `nu_R^*` visible whenever initial insertions are stated. The original probability corresponds to the density `s_R`, not to the bare indicator.
2. State near Theorem B that the insertion amplitude `alpha_R` may be complex and that the resulting object is a finite complex measure, not a probability law.
3. Preserve the explicit distinction between rescaled frequency `v` and physical frequency `omega=v/sqrt(n)` in every cutoff statement and diagram.
4. Retain the final-commit correction that finite-dimensional smoothing requires a uniform BV bound on the initial density. Do not revert to the broader phrase “bounded initial densities.”
5. In any future summary, do not describe the central band as reaching the old `n^-2/5` threshold; the physical exponent is `-99/200`.
6. Keep the positive-semidefinite and positive-definite covariance statements separate. Theorem B needs only the former; raw Gaussian density inversion needs the latter.
7. The conditional raw-inversion corollary should always be quoted together with its `H in L1`, complementary-tail and local-edge hypotheses.
8. The phrase “weighted local limit” should be reserved for cases where the complementary and edge estimates have been proved for the weighted measure, not merely the central integral.
9. The source-dependent density embedding in Lemma A.4 would benefit from a short table matching each manuscript norm estimate to the exact definition or equation in the cited collision-space source.
10. The semialgebraic argument should continue to state explicitly that its BV norm is in initial collision coordinates and does not concern the pushed-forward density.
11. If a future revision introduces another cutoff sequence, avoid overloading symbols already used for initial insertions.
12. Keep version chronology and build evidence in supporting files rather than interrupting the mathematical proof flow.

## 18. Reproducibility and verification limits

The native source builds successfully, references stabilize, and the exact-source workflow succeeds at the reviewed SHA. The finite diagnostics check the rational exponent inequalities, analytic-radius restrictions, central-versus-outer cutoff comparison, stopping identities, chronological products and interpolation algebra. The inherited geometry and clock diagnostics also pass.

These checks are valuable for detecting source drift and algebraic mistakes. They do not verify:

- the imported collision-space theorem at the precise stated norms;
- the continuum semialgebraic collision partition at every singular boundary;
- covariance nondegeneracy;
- an anisotropic induced high-frequency realization;
- the complete critical/singular residual decomposition;
- the weighted complementary tails;
- or the full raw mixed-density LLT.

No independent human specialist endorsement is represented by the workflow, the finite checks or this AI-assisted report.

## 19. Final assessment

Revision 10 responds seriously to the previous report. It proves a new integrated growing-major-arc theorem for the true physical return record, exposes previously compressed proof details, preserves the full earlier mathematics, and states the boundary of the new result accurately. I found no decisive contradiction in the new proof chain.

The paper is therefore materially stronger than revision 9. It is not, however, complete at the theorem level by which it asks to be judged. The raw mixed-density LLT still depends on uniform nondegeneracy, complementary-frequency control and a complete singular-branch residual theorem. Until those are supplied, I cannot recommend publication in *Annals*, *Acta*, *Inventiones* or *JAMS*.

**Recommendation: reject in the present form at the requested top-four benchmark.**
