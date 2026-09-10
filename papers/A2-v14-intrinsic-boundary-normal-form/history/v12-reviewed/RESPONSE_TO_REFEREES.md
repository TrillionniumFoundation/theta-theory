# Response to the independent A2 v11 report

**Revision:** A2 v12, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.  
**Author:** Qian Qi.  
**Report answered:** `bcde40b514e4dc00a3252f2d0710002a2caeac7b`, branch `review/a2-v11-abel-stability-harsh-independent-2026-09-10`.  
**Reviewed author source:** `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`, native manuscript tree `35a9fad03d7f1ee41f2c8661ee3c7aa58047bbad`.  
**New manuscript directory:** `papers/A2-v12-two-contact-rigidity`.

We thank the referee for distinguishing the correctness questions already resolved by v11 from the remaining quantitative and geometric-significance questions. We agree with the two-derivative gain in Section 5 of the report. We have checked the proposed regularizer and its full physical preparation charge, proved the improved bound under the unchanged profile and calibration hypotheses, and credited the report explicitly. We have also developed a separate geometric consequence: the two even laws determine two independent even analytic contacts, without requiring the graphs to coincide or their curvatures to be separated. This result is accompanied by independent physical realizations and a fixed-window observation theorem with physical alternatives.

The 192 theorem, lemma, proposition, corollary and proof environments active in the reviewed manuscript remain active and byte-identical. The article now contains 212 such environments. Their narrative order has deliberately changed: the relative law, geometric inverse and complete-profile observation form the main argument; all auxiliary results and earlier acquisition proofs remain in the appendices. The main article compiles to 117 pages, and the unchanged two-collision companion to 7 pages. These are reproducibility facts, not evidence by themselves of mathematical significance.

## 1. The report's closed findings remain closed

The report did not find a fatal error in the Abel inverse, the positive-node acquisition, the rare-event accounting or the smooth-class pilot. We do not describe the present revision as repairing such an error. The linear Abel discrepancy and its triangle inequality are retained. The estimator still observes only selected-event bits, not derivatives or values at zero. It charges failures and uses a finite ordered dictionary with a measurable tie rule. The calibration still estimates the actual gap, area and multiplier inside a model with unknown smooth finite-flight remainders, rather than importing an exact-family inverse.

The old sufficient exponents remain valid results for the old procedures. They are no longer highlighted as the strongest consequences of the integrated-flux identity. The previously established physical relative law, full smooth energy-profile uniqueness and odd-law compatibility are unchanged. In particular, the odd law is predicted from the two even laws; separately measured odd records validate that prediction and are not presented as a third independent coordinate.

## 2. Section 5 and R2: two additional derivatives and the revised observation bound

**Location:** `article/28_regularized_observation.tex`, Lemmas 13.1–13.2, Theorem 13.3, Corollary 13.4 and Theorem 13.5; the labels are respectively `lem:v12-gain`, `lem:v12-reconstruction`, `thm:v12-acquisition`, `cor:v12-modulus` and `thm:v12-self-calibrated`.

We accept the referee's mathematical point, not just the observation that our old rate was not claimed minimax. Keep the identical sum-norm class

\[
\mathcal K_m=\{V\in C^{m-1,1}([0,D]):V(0)=1,\ V\ge\beta,
\ \sum_{a=0}^{m-1}\|V^{(a)}\|_\infty+\operatorname{Lip}(V^{(m-1)})\le B\}.
\]

For the integrated flux, the exact physical identity gives

\[
H(V,W)''(d)=\frac2\pi\int_0^1
\frac{V(ds)W(d(1-s))}{\sqrt{s(1-s)}}\,ds.
\]

Differentiation through order `m-1`, the integrable beta weight, and the Lipschitz last derivatives give a uniform `C^{m-1,1}` bound for this second derivative. The identities `H(0)=H'(0)=0` then yield a uniform `C^{m+1,1}` bound for `H`. The proof is valid at zero and requires no extension across it.

We use `q=m+2` positive nodes in each globally smooth stencil, reproducing degree `m+1`. The same physical profile class is used in the dictionary: it is not replaced by a smoother class. The three estimates now read

\[
|JH_V-H_V|_{\mathscr A}\le Ch^{m-1/2},\qquad
|Jf|_{\mathscr A}\le C\|f\|_{C^3},\qquad
|Jz|_{\mathscr A}\le Ch^{-5/2}\max_k|z_k|.
\]

The second inequality is crucial: the finite-flight error and the structured calibration error still need only the original `C^3` bounds. The two-derivative gain is applied to limiting candidate fluxes, not to those errors. Thus the improvement has no hidden stronger bridge hypothesis.

The compact nodal-image dictionary, first-index minimization, Bernoulli concentration and charged allocations give

\[
\max_b\|\widehat V_b-\mathcal V_b\|_\infty
\le C(h^{m-1/2}+\tau^j+t h^{-5/2}+\delta).
\]

The allocations are summed, including every ceiling and every failed preparation. Their order is unchanged:

\[
2L+C A\sinh(j\gamma)h^{-1}t^{-2}\log(4L/\eta).
\]

Choosing `h` of order `epsilon^{1/(m-1/2)}`, `t` of order `epsilon h^{5/2}`, and the least adequate even flight number gives

\[
N_{\rm tot}\le
C\varepsilon^{-\left(2+6/(m-1/2)+\gamma/|\log\tau|\right)}
\log\frac{C}{\eta\varepsilon}.
\]

For `m=4` the profile-stage power is `26/7`, rather than `6`, before the common bridge contribution. This is the referee's improved sufficient benchmark, explicitly acknowledged in the article and bibliography.

The plug-in physical mean is still exactly `R H_{j,b}(d+Delta)`, with `Delta=j(ghat-g)`. On the good pilot event, its `C^3` discrepancy is bounded by `C(tau^j+alpha+j zeta+j rho)`. The smooth-input estimate above prevents an inverse mesh power from multiplying that structured error. The original smooth-class pilot at accuracy `xi=c epsilon/j` has smaller power `2+2/m` and is fully charged. Its cost is absorbed into the revised profile bound with `gamma_+`. Projections onto the supplied boxes keep the preparation charge deterministic even on bad pilot histories.

We also include the conditional uniform-data consequence

\[
\|V-W\|_\infty\le C\|H_V-H_W\|_\infty^{(m-1/2)/(m+2)}.
\]

It is a conditional estimate on a fixed regularity class of forward images, not unconditional Lipschitz stability for raw probabilities. Neither this exponent nor the preparation exponent is asserted optimal. The introduction and conclusion explicitly retain the certificate dependence of `tau`; increasing an admissible certificate can worsen the numerical bound without changing the billiard. The finite-dimensional and smooth-envelope minimax statements remain separate experiments.

## 3. R1: a geometric result beyond identical contacts and finite-jet nonconstancy

**Location:** `article/23_two_contact_rigidity.tex`, Theorem 9.1 and Corollary 9.2; `article/24_physical_image.tex`, Theorem 10.1, Corollary 10.2 and Theorem 10.3.

The existing identical-even theorem is not relabelled as new. It remains intact in the appendices, including its one-flight comparison and finite-order physical realizations. The new calculation allows the two even facing graphs to have independent jets. Their curvatures may differ or coincide. The gap and the two labelled curvatures are fixed; evenness is an additional hypothesis of the graph inverse only, not of the general relative law.

Let `q_m=(q_{0,2m},q_{1,2m})` and let `f_{m-1}` be the corresponding pair of degree-`m-1` coefficients of the two same-type laws. At arbitrary fixed lower even jets we prove the affine block derivative

\[
D_{q_m}f_{m-1}=
-\begin{pmatrix}P_m&Q_m\\Q_m&P_m\end{pmatrix}
\operatorname{diag}(K_{m,0},K_{m,1}).
\]

The proof computes the two types of half-line action contributions, the diagonal Green-kernel variation of the relative determinant, and the residual-time moments. The unequal-curvature factors cancel in the off-diagonal entries in precisely the way displayed in the theorem. The determinant is strictly positive because both `P_m+Q_m` and

\[
P_m-Q_m=m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)
\]

are positive. The latter follows from strict concavity of `tanh` and is the separating coefficient absent from a shared-graph variation. It produces an explicit block-triangular inverse at every finite order, with bounds on compact parameter boxes and no denominator involving the curvature difference. At equal curvatures the diagonal restriction recovers exactly the old identical-even coefficient; the antisymmetric direction is the additional information.

Equality of the two normalized even-law germs now determines both analytic even contact graphs. Connected analytic participating boundaries are then determined in their respective contact frames by analytic continuation of curvature and the planar Frenet equations. This is an exact determination result, not noisy global continuation. It does not determine unobserved obstacles, the lattice, or arbitrary odd contact jets.

### Independent physical image and specified fibres

For each fixed `M`, we construct a `2(M-1)`-parameter support-function family near the disk, allowing two independently prescribed curvature radii near one. The separate perturbations are

\[
\frac{1+\cos\theta}{2}\sin^{2m}\theta,
\qquad
\frac{1-\cos\theta}{2}\sin^{2m}\theta.
\]

At the selected contact each begins in order `2m`, while at the other it begins two orders later. An analytic area compensator vanishing through order `2M` preserves the area exactly. The lattice is `3Z x 4Z`; the selected gap is one, the free area is `12-pi`, and both contact curvatures remain fixed. Positive curvature, clearance and the strict gap to other translates persist.

The support-to-graph diagonal is `-(2m)! kappa_b^{2m}`, with zero same-order cross entry. Composing its triangular inverse with the new law block shows that both sets of statistical jets are independent local coordinates. Thus the physical image contains an open set in the full `2(M-1)`-dimensional jet space while the selected leading hierarchy is constant. Within a larger fixed `2(N-1)`-dimensional family, the fibres of the truncated `2(M-1)`-coordinate observation have dimension `2(N-M)`. This is a stated finite-family fibre theorem, not a claim to classify every asymmetric smooth fibre.

### A genuine finite physical observation theorem

Theorem 10.3 moves from coefficient germs to finitely many actual binary means. At fixed jet order, choose positive offsets `h,2h,...,(M-1)h` in both orientations. The derivative of the limiting nodal law is an invertible block Vandermonde matrix plus a controlled higher-order remainder. Then choose one sufficiently large, fixed even flight number; differentiated relative convergence preserves its invertibility. The leading normalizations are constant throughout the physical family. Consequently the actual positive-window probability vector is a local bi-Lipschitz coordinate.

The fixed windows and record length are chosen independently of requested accuracy. All preparations are charged. Finite-net fitting and Bernoulli concentration give uniform high-confidence error with `C epsilon^{-2} log(C/eta)` preparations. For squared risk, the upper order is `N^{-1}`. Pairs of nearby physical tables in this same family, with exactly unchanged leading hierarchy, give the matching lower bound by conditional Bernoulli entropy and the chain rule, even for adaptive choices among those windows.

The allowed experiment is deliberately specified: a known finite-dimensional physical family, supplied leading geometry and labels, and the fixed finite window set. Its conditioning constants can worsen with jet order. Its lower bound is not imported into the infinite-dimensional profile problem. The new significance claim rests on the independent-contact inverse and its physical image and observation consequences, not on the rate correction alone. We submit these results for mathematical reassessment without treating a venue recommendation as already resolved by the author.

## 4. R3: information sets and symmetrization remain explicit

The introduction, the graph theorem and both observation sections now separate three information sets. The geometric inverse fixes the gap and both labelled contact curvatures and assumes two individually even graphs. The finite-window physical theorem supplies an exact finite-dimensional family and fixed leading data. The full-profile theorem permits general contacts and unknown smooth finite-flight remainders; its pilot removes the actual `g,A,gamma`, but not labels, boxes, a coarse gap bracket, collars or regularity/convergence certificates.

The single multiplier is not said to recover two curvatures separately. The symmetrized energy profiles are not called unsymmetrized contact branches. The new additional evenness assumption is not imposed retroactively on the general forward theorem, profile compatibility, Abel inverse or full-profile acquisition. The distinction between exact analytic continuation and noise-stable continuation is preserved.

## 5. R4: hierarchy without loss of content

The article now gives precedence to the relative physical law, the two-contact graph inverse, physical realization and finite observation. The second main part gives the Abel coordinate and the strongest complete-profile acquisition. The 192 inherited formal environments are all still typeset, with identical contents. Earlier acquisitions, identical-contact inverses, endpoint experiments, exact-family curvature recovery, smooth-envelope theory and record-response formulas remain fully available in the appendices, not merely as uncompiled archival files. The original v11 introduction and input order are also archived for comparison.

No generality has been removed from the relative law. No old theorem has been silently replaced by a stronger-looking statement with extra assumptions. The new theorem statements and their hypotheses are separate and explicitly cross-referenced. The source-retention check is order-independent precisely because this revision changes the hierarchy rather than reproducing the earlier order as an end in itself.

## 6. Reproduction and remaining verification limits

The native v11 source packet was independently checked against all 110 Git blob hashes and reconstructed to the reviewed manuscript tree. The latest report blob was checked as `75f604f50085fc2e2824f46288892a2ed1a80089`. The historical derivation chain used here is listed in `HISTORICAL_DERIVATION_AUDIT.md`; this was a targeted audit, not an exhaustive re-refereeing of the eleven-paper program.

The inherited diagnostic suites and the new suite were executed in normal and optimized Python modes, with identical paired outputs. The new standard-library suite includes 1,307 finite diagnostics: exact block identities and inverses; independent finite Dirichlet-Green/ellipse-moment calculations compared with the limiting block; positive-node interpolation; integrated beta-kernel identities; rate algebra; and active-source retention. These checks overlap. They are not 1,307 independent proof obligations, nonlinear billiard simulations or a formal proof certificate.

Both PDFs were rebuilt from a clean auxiliary state with shell escape disabled. The final logs contain no unresolved cross-references, unresolved citations, duplicate labels or overfull boxes. Page contact sheets were inspected across the article, with enlarged checks of the new result pages and transitions. Full logs and raw test outputs accompany the delivery packet; `VERIFICATION.json` records hashes and actual limits. No remote CI execution or external journal acceptance is claimed.

The full proofs, not the test count or the page count, are the basis for the revised mathematical claims.
