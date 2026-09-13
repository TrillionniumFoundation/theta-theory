# Independent referee-style report on A2 v35

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/a2-v35-referee-integration-native-verification-2026-09-13`  
**Immutable reviewed submission:** `1c50ef04fc2863b4744b5312b539cb68265054f3`  
**Submission tree:** `adb6e3539ded98487636a0fe2e8f961c17383e01`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**New review branch:** `review/a2-v35-external-harsh-top4-2026-09-13`  
**Date:** September 13, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the requested standards of Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a claim of affiliation with those journals. It does not represent an additional human referee. Source keys and the exact coverage of this examination are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). References below use source filenames and theorem labels, not page numbers of an uninspected PDF.

## Recommendation

**Major revision of the assembled submission; no acceptance recommendation in its present delivery state. The focused mathematical response is satisfactory at the points re-examined.**

V35 closes the previous R1 request. The local-alternative mean is now expanded in the existing vector Gaussian proof, and the fourth-moment estimate is applied to centered summands before restoring that mean. The retained v34 likelihood-tilting argument also survives examination. Both current README entries now identify v35 correctly. The finite-experiment normalization, compact-parameter upgrade, and declared transverse count record should not be reopened merely to manufacture another round of objections. [S2–S6]

The outstanding concrete issue is **C2: a complete, immutable, actually verified native submission**. The hosted v35 build failed before any job step ran and produced no artifacts. The author's own execution record certifies neither the complete main nor its inspected PDF. A companion build and an isolated chapter build are not the requested assembled article. This is an unresolved delivery and verification requirement, **not evidence that the TeX source fails to compile, and not a counterexample to a theorem**. GitHub Actions is not itself a journal requirement; a reproducible successful local native build with retained products would also address C2. [S4, C1]

**No fatal mathematical counterexample to a stated theorem was established in this review.** That sentence is deliberately weaker than a correctness certificate for the whole article. This round examines the statistical revisions, the half-line and relative-factorization arguments, the signed contact inverse, the single-offset density inverse, and the principal calibration/estimation constructions. It does not freshly rederive every active appendix, the entire intrinsic gluing and orientation classification, every flux-integration step, the two-sided Poisson construction, or the native companion. Nor was a complete main PDF compiled or inspected in this review. Earlier favorable module reports do not add up automatically to comprehensive independent validation.

| Issue | V35 disposition | Basis |
|---|---|---|
| R1: alternative mean and quadratic-risk integrability | **Closed** | Correct in-place mean expansion, centered fourth moment, and original-law risk control |
| I1: current version and navigation | **Closed** | Both actual README entries now point to v35 and distinguish the v33 review from the unreviewed v34 predecessor |
| M1: finite versus compact experiment wording | **Remains closed in the inspected scope** | Finite likelihood comparison and the separate compact modulus/net argument are distinguished |
| M2: retained count–endpoint observation | **Remains closed** | The theorem retains laboratory transverse pairs and waiting information, not normal coordinates or residual time |
| M3: finite likelihood-experiment theorem | **Remains closed** | Normalization supplies uniform integrability; one coupling gives both parameter-independent kernels |
| E1: compact local Gaussian convergence | **Remains closed under the printed hypotheses** | The necessary uniform moving-boundary modulus is present |
| C2: complete native submission verification | **Open** | No successful complete-main execution and inspected product were verified; current hosted job has zero executed steps and no artifacts |

The next response should finish this submission rather than enlarge its theorem list. No arbitrary deletion, reduction to finite parameter sets, or weakening of the established observation-level conclusions is requested. Closing C2 would settle the outstanding delivery request; it would not by itself establish publication-level originality or verify every proof.

## 1. Submission identity and the actual mathematical increment

The pinned commit is dated **September 12, 2026, 23:37:08 UTC**, namely **September 13, 2026, 01:37:08 Europe/Amsterdam**. This is distinct from the manuscript's printed date. The latest addressed referee report is at `d51c06689ba540711b2f890beb35eb235dba13e4`, and it reviewed the assembled v33 source `b577cffcb3ca5597cb4905269bea9de3bd4ead38`. V35 also preserves author v34 at `127f9334f15c5fb12307bd691973d1eb44e499e8`. There is no intervening v34 referee approval to assume. [S1, S4]

The authenticated v34-to-v35 comparison is two commits ahead, zero behind, and lists eighteen changed paths. Only two active TeX files change: `main.tex` and `article/18a_vector_boundary_information_v26.tex`. The latter has 68 added and 10 removed lines. The other changes concern navigation, response/evidence machinery, historical copies, and importation of the preceding referee records. No path is deleted. The v34 tilting module remains an active input. This is a focused repair, not an independently new proof of all inherited geometry. [S1, S3–S5]

The active source advertises 52 direct inputs and retains the 36-module auxiliary compendium. The compendium's list was inspected; its existence is not a claim that all thirty-six proofs were audited in this round. The historical `A2-v17-...` directory name is not a version-identity defect: the current native entry and both active README files now consistently identify v35. The absence of complete build evidence belongs under C2, not a renewed I1 objection. [S2, S3]

## 2. R1 is genuinely closed, including the unbounded-loss issue

### 2.1 Expansion under the alternatives

Write the successful density as

\[
 f_\theta=a_\theta(w_\theta)_+,\qquad
 \mathsf S=D_\theta\log a_\theta|_0+V/w_0,\qquad
 J=\int_\Sigma \frac{a_0VV^t}{|\nabla w_0|}\,d\sigma.
\]

Let \(\ell_n=\log(1/\delta_n)\), \(q_n=\delta_n\ell_n^{1/4}\), and \(C_n=\{w_0\ge q_n\}\). The hypothesis is \(B_n=np_n\delta_n^2\ell_n\to1\). On the common collar, the moving defining function stays positive uniformly on a compact local parameter set. Taylor expansion of the *smooth product* \(a_\theta w_\theta\) before division by \(a_0w_0\) gives precisely

\[
 \frac{f_{\delta_nh}}{f_0}
 =1+\delta_n h^t\mathsf S
   +O_K\bigl(\delta_n^2(1+w_0^{-1})\bigr).
\]

This is `eq:v35-one-mark-expansion`, and the stated joint smoothness suffices. In normal coordinates \(s=w_0\), the score is \(O(1+s^{-1})\) and the reference density times volume element is \(O(s)\,ds\,d\sigma\). Integrating the remainder against the score therefore costs a logarithm, not an uncontrolled inverse power. [S5]

Consequently `eq:v35-alternative-mean` is correct:

\[
 \begin{aligned}
 \mathbb E_{n,h}\Delta_n
 ={}&np_n\delta_n\mathbb E_0[\mathsf S\mathbf1_{C_n}]\!+
 np_n\delta_n^2\mathbb E_0[\mathsf S\mathsf S^t\mathbf1_{C_n}]h\\
 &+O_K\bigl(np_n\delta_n^3\log(1/q_n)\bigr)
 =Jh+o_K(1).
 \end{aligned}
\]

The centering and information budgets are explicit:

\[
 np_n\delta_nq_n=B_n\ell_n^{-3/4},\qquad
 np_n\delta_n^2\log(1/q_n)
 =B_n\left(1-\frac{\log\ell_n}{4\ell_n}\right).
\]

The remainder equals \(O_K(B_n\delta_n[1-\log\ell_n/(4\ell_n)])\) and vanishes. This proves a uniformly bounded alternative mean before the independent-sum fourth-moment estimate is used. It is not a circular appeal to the desired quadratic-risk conclusion.

### 2.2 Center the summands, then restore the mean

For \(\xi_{n,i}=\delta_nY_i\mathsf S(X_i)\mathbf1_{C_n}(X_i)\), the one-success density ratio is uniformly bounded on \(C_n\). The reference collar moments therefore give uniform alternative bounds for \(\sum_i\mathbb E\|\xi_{n,i}\|^2\) and \(\sum_i\mathbb E\|\xi_{n,i}\|^4\). Expanding centered scalar fourth powers coordinatewise, in fixed dimension, yields

\[
 \mathbb E_{n,h}\|\Delta_n-\mathbb E_{n,h}\Delta_n\|^4
 \le C_K\left\{[np_n\delta_n^2\log(1/q_n)]^2
                 +np_n\delta_n^4q_n^{-2}\right\}.
\]

The last term is \(B_n\ell_n^{-3/2}\). Restoring the already controlled mean proves compact-uniform fourth moments. The wording now also specifies the actual statistic correctly: **each** excluded observation contributes zero; one excluded observation does not erase the other observations in the sample. [S5]

This matters for more than presentation. Total-variation closeness of the original and censored experiments controls bounded risks, but does not alone transfer an unbounded quadratic loss. The new calculation is directly under the original alternatives, and hence supplies the missing integrability rather than assuming it from experimental equivalence. Applying the fixed Moore–Penrose inverse on \(\operatorname{Ran}J\) preserves that control; no risk for an unidentifiable coordinate is asserted.

### 2.3 The retained v34 tilting proof is also valid

In `prop:v34-tilting-moments`, joint convergence of \((\Delta_n,L_n)\) and unit expectations of both prelimit and limiting likelihoods imply uniform integrability through

\[
 \mathbb E(L_n-A)_+=1-\mathbb E(L_n\wedge A).
\]

Truncated likelihood tilting can then be passed to the limit. Positivity of the limiting Gaussian likelihood supplies reverse contiguity by

\[
 P_n(A_n)\le P_n\{L_n\le c\}+c^{-1}Q_n(A_n).
\]

The shift is \(N(Jh,J)\), including singular information. Fourth-moment control plus subsequence compactness gives uniform quadratic-risk convergence to \(\operatorname{tr}(WJ^+)\). No product-likelihood bound tending to one, and no additional high likelihood moment, is smuggled into this proof. [S5]

An independent explicit model check is included in the accompanying diagnostics. For

\[
 f_\theta(x)=\frac{2}{\pi(1+\theta)^2}
                  (1+\theta-|x|^2)_+,\qquad |x|<2,
\]

with small \(\theta\), the null radial variable \(s=1-|x|^2\) has density \(2s\) on \((0,1)\), score \(s^{-1}-2\), and boundary information \(J=2\). Its exact truncated alternative mean is

\[
 \int_{s\ge q}\mathsf S f_\theta\,dx
 =\frac{2\{q^2-q+\theta[\log(1/q)-2+2q]\}}{(1+\theta)^2}.
\]

This reproduces the centering and logarithmic budgets. It is a diagnostic of the local statistical calculation, not a claim that this density family is itself realized by a billiard channel. The proof, not the finite numerical sample, closes R1.

## 3. The finite-to-compact statistical argument should not be weakened

`lem:v33-finite-likelihood` contains the normalization hypothesis actually needed. Coordinatewise unit means and weak convergence give uniform integrability of the nonnegative likelihood vector. Coupling its laws with vanishing expected \(\ell^1\) discrepancy, and then disintegrating the same coupling in the two directions, gives common kernels with

\[
 \|K_n(x_i\mu_n)-y_i\mu\|_{\rm TV}
 \le \tfrac12\int|x_i-y_i|\,d\pi_n.
\]

The likelihood vector is sufficient for the finite dominated experiment by conditional reconstruction under the reference measure. Standard Borelness is the appropriate assumption. Neither direction receives the unknown parameter as an input. This is a valid standard result, properly identified as such, rather than a new discovery or an unsupported appeal to likelihood convergence. [S5]

The compact conclusion uses additional work. `lem:v32-finite-net` selects one comparison kernel on a finite net and estimates its error away from the net by the two continuity moduli. The nearby net point is used in the bound, not fed to the kernel. The moving-boundary estimate supplies

\[
 H^2(P_{n,h}^{\otimes n},P_{n,h'}^{\otimes n})
 \le C_Ks^2(1+\log(1/s)),\qquad s=\|h-h'\|\le1,
\]

and the Gaussian modulus is evaluated on the identifiable range. Taking the sample-size limit at a fixed net and subsequently shrinking its mesh proves compact Le Cam convergence. The singular and zero-information cases do not require inverting \(J\) on its kernel. E1 remains closed under the printed regularity and rate hypotheses. [S6]

For the count–endpoint product, the slow and fast coordinates are separated before comparison. With \(\eta_n=(j_n\sqrt{k_n})^{-1}\), the success log-ratio remainder after \(-b/\sqrt{k_n}\) is bounded by

\[
 C_K(\delta_n+\eta_n+j_n\delta_n^2
                     +j_n\delta_n\eta_n+j_n\eta_n^2).
\]

Multiplication by \(\sqrt{k_n}\) makes every term vanish under the printed conditions. The endpoint cost of removing the fast coordinate is

\[
 k_n\eta_n^2\log(e/\eta_n)
       =\frac{1+\log(j_n\sqrt{k_n})}{j_n^2}\longrightarrow0.
\]

The proof removes the caps before using independence of waiting times and successful marks, combines kernels on compact projections, restricts to the actual compact parameter set, and only then restores cap and finite-bridge errors. It does not assert iid successful marks after conditioning on cap completion. The negative-binomial score and its derivative formulas are consistent with the exact geometric waiting law. As an additional finite check, the affinity for a wait stopped at \(k\) successes is

\[
 \left(\frac{\sqrt{pq}}{1-\sqrt{(1-p)(1-q)}}\right)^k.
\]

The provided diagnostic reproduces this formula without a Poisson approximation. [S6]

Crucially, `thm:v23-count-endpoint-joint` excludes normal coordinates, residual time, and intermediate collisions. Singular information in the richer noiseless planar-position experiment is not a counterexample to this coarser theorem. The conclusions are local, reference-based, and compact-parameter conclusions; they do not assert global Gaussian equivalence over the analytic table class.

## 4. Geometric scrutiny beyond the revised statistical pages

### 4.1 Jacobi normalization and the relative determinant

I checked the alternating quadratic normalization rather than taking the displayed hyperbolic formulas on trust. For the local flight length

\[
 \ell_b(u,v)=\sqrt{(g+\psi_b(u)+\psi_{1-b}(v))^2+(v-u)^2},
\]

the interior Hessian has diagonal \(2c_{b+i}/g\) and adjacent entries \(-1/g\). The period-two scaling used in the manuscript gives the stated half-line Green kernel and endpoint Schur complement. In particular the one-flight Hessian is exactly \(g^{-1}\begin{pmatrix}c_0&-1\\-1&c_1\end{pmatrix}\). The diagnostic verifies twelve finite Schur complements and 162 entries of the half-line recurrence using exact rational arithmetic, including unequal curvatures and both starting types. [S7, D1]

The nonlinear relative-factorization proof has the right mechanism. Weighted localization makes the perturbation of the interior Hessian trace class, with entrywise summability rather than a dimension-dependent norm estimate. The finite cofactor formula is normalized before taking logarithms. Truncating to the two endpoint blocks, comparing the compressed Green kernels with the half-line kernels, and controlling logarithmic determinants in trace norm avoids dividing an absolute action error by an exponentially small reference twist. Fixed derivative-order polynomial losses can be absorbed by a strictly slower exponential rate. [S7]

These are substantial analytical arguments and not consequences of the numerical checks. The inspected construction provides a coherent route to the relative law. My examination here does not independently certify every subsequent physical flux integration and boundary-coordinate transfer used elsewhere in the manuscript.

### 4.2 All-order jet inversion: multiplicities and smooth remainders

The weighted nonlinear half-line inverse, finite-truncation envelope identity, and smooth-remainder factorization were examined. The envelope proof retains the right-boundary variation term until its decay has been established. Interpolating two smooth graph pairs with equal finite jets gives an action difference of order \(O(|u|^{M+1})\); this justifies factorization through finite jets without identifying a smooth graph with its formal Taylor series. Analyticity is invoked later for equality of boundary germs, not for this finite-order argument. [S8]

The last-jet block has the correct site multiplicities. The boundary site is counted once, and every interior site twice. Therefore the own-contact coefficient is

\[
 1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),
\]

while the opposite-contact coefficient is

\[
 2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
        =\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

Because \(\mathfrak r_0\mathfrak r_1=1\), the determinant is one. The coefficient of the new graph jet is independent of that jet, since only the linear orbit contributes at its first homogeneous degree. The finite-order lower-triangular inverse is consequently justified. Exact rational checks at orders three through sixteen agree with the formulas. [S8, D1]

The qualifications in the manuscript must be retained: fixed-order compact stability is not uniform infinite-order conditioning; smooth flat perturbations are not excluded by equality of all formal jets; and analytic continuation is an exact identification argument, not a stable high-resolution extrapolation theorem. I found no new defect in the inspected local jet recursion.

### 4.3 The four-density identity really removes the amplitude

For \(f(u,v)=Z^{-1}B(u)B(v)[d-S(u)-S(v)]\) on an interior square,

\[
 1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
 =\frac{S(u)}{d-S(u)}\frac{S(v)}{d-S(v)}.
\]

A fixed nonzero anchor has strictly positive action. Taking a scalar square root only at that anchor and using a mixed slice recovers the signed action values on both sides of zero. This avoids the false step of differentiating a degenerate pointwise square root at the contact. The unknown amplitude and normalization cancel exactly. An asymmetric rational example in the diagnostics checks both the action and the normalized-amplitude reconstructions. [S8, D1]

The inverse is appropriately stated in an interior \(C^M\) density norm. It does not turn total variation into control of arbitrary derivatives, and it does not treat density values as individual finite-sample observations. Both contact types and the separately supplied onset gap remain part of the data. The last lattice identity \(L=VM^{-1}\) is elementary; the demanding inputs are the all-order contact inverse and the uniqueness of the required analytic incidence matching. The latter entire global classification was not rederived in this round and is not certified by the density identity.

## 5. Physical calibration and global estimation: what is and is not observed

The common record space and calibration rule were scrutinized because they are natural places for hidden geometric oracles. The acquisition uses labelled alternating words, programmed physical times, and planar endpoint positions in a common frame for the two types of each channel. Different channel frames are not supplied as registered. Marked labels are assumed available; the theorem is not a discovery procedure for unlabelled channels. Independent normalized phase-volume preparations are part of the model. [S9]

The onset scan uses a known compact-class bracket. A grid point lies between one and two resolution widths beyond the true onset; the uniform lower mass \(c h^2e^{-j\gamma_+}\) gives a finite deterministic cap for each scan. Earlier successes cannot occur before onset. Taking the two observed contact positions from these near-onset successes controls their errors by \(O(\sqrt h)\). Most importantly, the pilot is run at the already selected final flight number \(J\), so it controls \(J|\widehat g-g|\), not an error at an earlier smaller flight number. All failed preparations remain charged. [S9]

The post-pilot test bias is bounded by \(C(\sqrt h+h+\tau^J)\). The estimated transverse projection is a common statistic of the transcript; the unknown exact contact projection appears only in the error analysis. The centered scalar laws have the asserted continuity by integration over their fibers. No continuity in total variation between noiseless planar laws on different boundary curves is asserted. The measurable physical coupling lemma likewise compares two laws embedded in the same fixed table, not different unknown tables through a parameter-dependent simulator. Its explicit diagonal-plus-residual coupling has the required jointly measurable dependence. [S9]

The global estimator includes the gaps in its minimum-distance criterion, rather than merely using them to program observation times. Compactness and separation by bounded tests give a finite library; the proof correctly admits that this library and its inverse moduli can be non-effective. Concentration is applied to uncapped successful sequences, then the cap event is charged. The diagonal construction runs the chosen budget stage afresh, so its whole acquired transcript genuinely has a diverging minimum flight number. It does not mistakenly make that assertion for a cumulative archive containing earlier short flights. [S9]

These points support the stated existence and consistency mechanism. They do not supply an effective design complexity or a sharp analytic minimax rate. Nor does the global planar-position consistency result prove that the half-line inverse is necessary: the manuscript itself describes a direct graph-interpolation benchmark in that richer observation model. The intrinsic transverse-law theorem, rather than a prohibition on short flights, is where the distinct inverse content must be assessed. [S10]

## 6. C2 remains open: the evidence does not show a native build

The actual v35 hosted run is `34725901237`, on the exact reviewed SHA. Its only job, `103639833518`, is recorded as failed with **`steps: []`**, **`runner_id: 0`**, and an empty runner name. The job lasted from 23:37:24 to 23:37:28 UTC on September 12. The dedicated artifacts query returned an empty list. These are direct authenticated API observations. [C1]

This supports only the conclusion that no executed build or resulting artifact was evidenced by that run. It does not identify a LaTeX error, prove a workflow-script defect, or establish the cause of the runner failure. No billing or permission diagnosis is justified by these fields alone.

`VERIFICATION_V35.md` reports an exact native companion build, its seven-page PDF hash, an isolated vector-chapter syntax check, and ordinary/optimized author diagnostics. These are transparently distinguished from full-main evidence in the document. In this review, those reported companion products were not independently retrieved and rerun. The finite mathematical diagnostics accompanying this report are separate newly executed checks; they must not be relabelled as reproductions of the author's native build. [S4, D1]

The current branch does not contain the promised complete-main execution certificate in the inspected record. Its source-first workflow is useful engineering, but a configured archive step that never ran is not an archived submission. Preserve the source-first approach, but supply the actual products.

**C2 acceptance criterion:** identify the immutable assembled source used for the test; compile the unabridged `main.tex` and native `two_collision.tex` with all active inputs and bibliography; retain commands, tool versions, exit status, full final logs, and source/product hashes; inspect the actual compiled article for unresolved references/citations, missing content, and unreadable formula/layout defects; and record that inspection's coverage. A successful ordinary local build is sufficient evidence of execution—hosted CI is not mandatory. When a different assembled SHA is used, compare it with the reviewed SHA so that a changed mathematical source is not silently substituted.

Do not respond with another isolated fixture, a theorem-presence counter, a hash without its product, or an assertion that unchanged inputs make compilation unnecessary. Conversely, do not represent a clean PDF as mathematical proof validation.

## 7. Assessment against the requested journal level

The potentially substantial contribution is the combination of a nonlinear relative long-bridge law with an unsymmetrized, two-contact, all-order inverse obtained from one positive-offset transverse density per type. Neither the four-density algebra alone, the final two-by-two lattice calculation alone, nor a standard finite-likelihood lemma would establish the level of contribution sought. The manuscript's case must rest on the analytical construction, its inverse content under genuinely coarsened observations, and the exact scope of the global geometric conclusion. This is an assessment of significance, not a priority certification.

The introduction now makes a defensible distinction from related spectral problems. De Simoi–Kaloshin–Leguil study marked-length determination for analytic open dispersing billiards with symmetry and genericity assumptions. Finamore–Leguil formulate finite-horizon Sinai rigidity using an enriched marked length spectrum. The present signed channel-law data, onset gaps, and marked incidence structure are different data. Without a theorem relating these observation maps, removing a symmetry assumption in one problem does not make it a generalization of the other. V35 does not claim such a subsumption. [S10, L1, L2]

The general appearance of Poisson boundary experiments is also not a new principle: Meister–Reiß establish Le Cam equivalence with Poisson boundary observations in a nonregular regression setting. The relevant question here is the billiard-specific construction and the exact kernels between the retained observation levels. The external comparison in this review checks these stated scopes and primary-source metadata; it is not an exhaustive literature or priority audit. [S10, L3]

For editorial presentation, the v34 tilting proposition and the v35 in-place calculation now overlap. This is a nonblocking clarity issue, not a mathematical contradiction. A final proof-dependency guide could identify which passage supplies the density Taylor expansion, which supplies likelihood tilting, and which supplies risk integrability, while preserving the mathematics and historical source. Similarly, retained auxiliary results should have visibly separate hypotheses and roles. No wholesale deletion or arbitrary contraction of the programme is requested.

The present review does not support unconditional submission-readiness language or an acceptance recommendation at any of the four requested venues. It also does not support a categorical rejection of the mathematical core as false or trivial. A verified assembled manuscript and a complete significance/correctness assessment remain different requirements; one must not be used as a substitute for the other.

## 8. Required response and final disposition

The mandatory author response is to close C2 with actual native products and an accurate tested-source ledger while preserving the mathematical repairs now in place. Keep R1 and the v34 alternative-law argument intact. Keep the finite/compact distinction, the singular identifiable quotient, the transverse-only count record, and all charged preparation conventions intact. The navigation repair is accepted.

The accompanying `diagnostics.py` was executed in ordinary and optimized Python; both executions succeeded with byte-identical JSON. It checks exact finite algebra and explicit model calculations, not the entire theorem network. Its scope, commands, and hashes are in the audit. No full native main or companion was compiled or PDF-inspected by this referee round.

**Final disposition: R1 and I1 closed; M1–M3 and E1 not reopened at their stated scope; C2 open; major revision of the assembled delivery; no acceptance recommendation and no newly established fatal mathematical counterexample.**
