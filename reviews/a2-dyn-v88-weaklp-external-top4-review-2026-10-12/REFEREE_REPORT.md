# External top-four referee report on A2-DYN revision 88 — weak-Lp alternative

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v88-weaklp-referee-response-2026-10-12`, `revision/a2-dyn-v88-weaklp-referee-copy-2026-10-12`  
**Reviewed author commit:** `24eaaab3b0564c1b8eecbb2217959e3be4320032`  
**Reviewed repository tree:** `a91219a03b468ed239e1ffa97600a3ca8a6a21e3`  
**Active manuscript directory:** `papers/A2-DYN-v88-referee-response`  
**Active mathematical source:** 207 numbered core modules; this alternative revision adds modules 205--207  
**Immediate author baseline:** revision 87 at `44785327cc0331d994d5d1de371710615cfd6b93`  
**Frozen revision-87 paper tree:** `086086bf42a833b241422b0b8a145fa5771a6f2d`  
**Controlling external report:** `reviews/a2-dyn-v85-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `af90a4e75bb4262cf16e64ff5e62a688bc21c007` / `86ecdfdf87d9ad7f6ecbe20c97f10cc75967eec5`  
**Parallel main-v88 author commit:** `e0d462e7b04c35fa3547435ede29adafe1968d8f`; the present branch is an independent alternative descended from v87, not a descendant or replacement of that commit  
**Exact-SHA qualification runs at report freeze:** response `38220442356`; referee-copy `38220448221`; both were queued  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

This is not a cosmetic revision. The weak-`L^p` alternative proves a genuine new local-norm theorem for the original unaveraged exact-label roof density. In particular, it does not merely restate the critical/zero-residence charge isolated in revision 87. Its three new modules establish:

1. a collision-count-uniform physical cap for short total residence and actual negative total-residence moments below the ordered exponent `1/32`, without a positive lower residence cutoff;
2. a complete nongrazing first-exit surface estimate in a finite weak `L^q` roof norm, with no lower residence or initial-gradient cutoff, for every `1<q<32/31`; and
3. local weak-`L^q` and strong-`L^p` convergence of the original exact-label raw density error on every fixed-length roof interval, uniformly in interval location, radius, return count, displacement label, and occupation label, for `q<32/31` and `p<32/31`.

These are mathematically substantive conclusions. I found no decisive counterexample, no sign reversal in the roof flow, no error in the printed exponent arithmetic, no illicit replacement of an exact-label source by a larger relabelled source, no hidden collision-dependent Fourier band, and no claim that a finite local norm controls the essential supremum.

The negative recommendation is nevertheless unavoidable under the requested benchmark and the manuscript's own governing objective. The paper continues to present the unrestricted exact-label pointwise raw local limit theorem as the organizing endpoint. That theorem remains unproved. The new finite local norms control the distribution of roof-density heights on bounded intervals, but they permit increasingly narrow high spikes. They therefore do not imply vanishing of the collision-normalized essential supremum and do not prove the original microscopic concentration charge to be zero.

The present alternative should consequently be judged in one of two ways:

- as a revision of the pointwise A2-DYN program, it remains incomplete at its central theorem and cannot be accepted at the requested level;
- as a separate paper centered on the local weak/strong `L^p` theorem, it would require a new title, abstract, theorem hierarchy, comparison with the existing local-limit literature, and a substantially shorter self-contained proof architecture before its independent significance could be assessed.

The present report evaluates the manuscript as submitted, with its unchanged pointwise target. On that basis the recommendation is rejection in the present form.

## 2. Frozen source and chronology

The two reviewed author branches resolve to the same commit:

`24eaaab3b0564c1b8eecbb2217959e3be4320032`.

That commit has parent

`44785327cc0331d994d5d1de371710615cfd6b93`,

the exact revision-87 author baseline. The branch therefore contains one author commit beyond v87. It preserves the 204 inherited core modules and adds:

- `core/205_capped_negative_residence_moments.tex`;
- `core/206_uncut_surface_lorentz_control.tex`;
- `core/207_exact_label_raw_density_local_norm.tex`.

The branch is later in repository chronology than the separately developed main-v88 pair at `e0d462e7b04c35fa3547435ede29adafe1968d8f`, but it is not a descendant of that pair. The two v88 objects use different modules 205--207 and prove different theorems. I have therefore treated the present weak-`L^p` pair as an independent alternative manuscript, not as a superseding revision of the already reviewed main-v88 source.

The active README, response, proof ledger, publication status, referee status, and source manifest consistently state that the pointwise theorem is still open and that the local-norm result is not a pointwise closure. This is an important and correct limitation of scope.

## 3. Mathematical contribution in revision 88 weak-`L^p`

### 3.1. Short total residence is controlled by a physical cap

Let

\[
 \ell=\tau^-+\tau^+
\]

be the total residence length of the original maximal regular exact-event segment. It is not the collision return time. Module 205 proves, uniformly in collision count, radius, and exact labels,

\[
 \bar\nu\{\ell\le s\}
 \le \bar\nu\{\tau^+\le s\}
 \le C s^{1/2}.
\]

The proof uses the actual first-exit layer decomposition. Incidence layers have invariant collision mass of quadratic order in their incidence width, while section-edge and flight-clearance layers have linear order in their geometric width. Since the physical layer widths are proportional to `q_0^d sqrt(s)` and at most two marks occur at each depth on each side, the geometric depth sum is finite and gives the displayed square-root cap.

This is the correct type of estimate for the later layer cake. It is a bound on the full positive physical probability. The manuscript does not incorrectly assert that an unsigned spectral remainder itself inherits the physical cap.

### 3.2. The finite-count spectral remainder remains capped before layer cake

Combining the retained fixed-band short-exit estimate with the physical cap gives

\[
\begin{split}
 m^2\bar\nu\{F\in J,\ell\le s\}
 \le{}& C s^{\gamma_0}(|J|+B_*^{-1}) \\
 &+C_{B_*}(1+B_*|J|)m^3
       \min\{\rho_{B_*}^{m/2},s^{1/2}\},
\end{split}
\]

where

\[
 \gamma_0=\frac1{32}.
\]

The minimum is essential. An error term independent of the residence threshold would be nonintegrable against the negative-moment layer cake. The manuscript keeps the cap until the layer cake has been evaluated at finite collision count.

### 3.3. Actual negative residence moments

For

\[
 0<\upsilon<\gamma_0
\]

module 205 defines the actual positive source

\[
 q_{\upsilon,s}(t)\,dt
 =F_\#\bigl(\ell^{-\upsilon}
       \mathbf 1_{\{0<\ell\le s\}}\bar\nu\bigr).
\]

The source identity

\[
 \ell^{-\upsilon}\mathbf 1_{\{\ell\le s\}}
 =s^{-\upsilon}\mathbf 1_{\{\ell\le s\}}
 +\upsilon\int_0^s v^{-\upsilon-1}
            \mathbf 1_{\{\ell\le v\}}\,dv
\]

is applied with positive lower truncations, followed by monotone convergence. For the capped remainder the printed identity

\[
\begin{split}
&s^{-\upsilon}\min(D,s^{1/2})
 +\upsilon\int_0^s v^{-\upsilon-1}
                 \min(D,v^{1/2})\,dv \\
&\qquad =\frac1{1-2\upsilon}
 \min\{s^{1/2-\upsilon},D^{1-2\upsilon}\}
\end{split}
\]

is correct. Splitting at `v=D^2` produces cancellation of the boundary terms. Substitution of `D=\rho_{B_*}^{m/2}` gives an exponentially summable finite-count remainder.

After fixing interval length, residence width, and auxiliary band before the collision limsup, one obtains

\[
 \limsup_m\sup_{R,n,k}\sup_{|J|=L}
 m^2\int_J q_{\upsilon,s}(t)\,dt
 \le C_\upsilon L s^{1/32-\upsilon}.
\]

The physical cap alone gives fixed-count finiteness for every negative exponent below `1/2`; the ordered decay needed later uses the stricter range below `1/32`. The manuscript distinguishes these two scopes correctly.

## 4. Audit of the complete surface estimate

### 4.1. The weak roof norm

For `q>1` the manuscript uses

\[
 \mathcal N_q(f;J)
 =\sup_{E\subset J,\ 0<|E|<\infty}
 |E|^{-1+1/q}\int_E |f(t)|\,dt.
\]

This is a norm equivalent to the usual weak `L^q` Lorentz quasi-norm. It is subadditive, monotone under restriction, and directly adapted to positive sums of interval pulses.

### 4.2. The pulse lemma is valid with arbitrary overlap

For a family of intervals `(a_\sigma,b_\sigma)` of lengths `\ell_\sigma` and weights `T_\sigma`, the roof pulse

\[
 f(t)=\int T_\sigma
 \mathbf 1_{(a_\sigma,b_\sigma)}(t)\,d\sigma
\]

satisfies, with `\upsilon=1-1/q`,

\[
 \mathcal N_q(f;J)
 \le \int_{(a_\sigma,b_\sigma)\cap J\ne\varnothing}
 T_\sigma\ell_\sigma^{1-\upsilon}\,d\sigma.
\]

Indeed a measurable set of measure `v` intersects each interval in at most `min(v,\ell_\sigma)`, and

\[
 v^{-\upsilon}\min(v,\ell)
 \le \ell^{1-\upsilon}.
\]

No disjointness assumption is used. This is important because physical roof intervals from different exact words may overlap.

### 4.3. Whole-segment integration supplies the missing residence factor

On one maximal segment the physical angular density is

\[
 A=\frac{\omega}{4\pi c_*\chi},
\]

and the retained derivative estimate is

\[
 |A'|\le C A I_m/z.
\]

For `a<t<b`, the outgoing trace obeys

\[
 A(b-)\le A(t)+C\int_t^b A(u)I_m(u)/z(u)\,du.
\]

Integrating over the whole segment gives the exact triangular factor

\[
 A(b-)\ell^{1-\upsilon}
 \le \int_a^b A(t)\ell^{-\upsilon}\,dt
 +C\ell^{-\upsilon}
   \int_a^b (u-a)A(u)I_m(u)/z(u)\,du.
\]

The factor `(u-a)` is load-bearing. Forward radial growth gives

\[
 z(u)^2\ge 2\lambda_\circ(u-a).
\]

With

\[
 \kappa=\frac{1-\eta}{2},
\]

one obtains

\[
 (u-a)z(u)^{-1}
 \le C_\eta (u-a)^{1-\kappa}z(u)^{-\eta}.
\]

The exponent calculation is correct: after using the lower bound on `z`, the remaining power of `(u-a)` is zero. Consequently the variation term is bounded by

\[
 C_\eta s^{1-\kappa-\upsilon}
 \int_a^b A I_m z^{-\eta}.
\]

The proof differentiates the complete angular density, including both `\omega` and `\chi`; it does not set the physical Jacobian equal to one.

### 4.4. Multiplicity-one summation

The complete Borel maximal-segment parametrization is used to sum the segment energies. Its incident-component convention prevents geometric endpoints belonging to distinct physical components from being identified. Each interior point is counted once. The outgoing nongrazing selector is retained on the trace side; it is dropped only on positive upper comparison sources.

No word-count multiplier appears. At the level of this audit, the summation is consistent with the inherited Borel parametrization.

### 4.5. Endpoint of the weak exponent

Combining the negative residence moment and the fractional optical source yields, for

\[
 \upsilon=1-\frac1q,
\]

short-surface decay of order

\[
 s^{1/32-\upsilon}.
\]

Thus the admissible range is precisely

\[
 1<q<\frac{32}{31}.
\]

For the complete first-exit surface the long-residence contribution is paid by the inherited positive-residence essential-height theorem, while the short part is paid by the finite-count negative moment. The resulting rate is

\[
 \nu_q=\frac1q-\frac{31}{32}>0,
\]

and

\[
 \limsup_m\sup_{R,n,k}\sup_{|J|=L}
 \mathcal N_q(m^2\overline{\mathcal F}_r;J)
 \le C_{q,L}r^{\nu_q}.
\]

For example, `q=64/63` gives `\nu_q=1/64`. The manuscript correctly excludes the endpoint `q=32/31`, where this power vanishes.

The complete surface theorem is a finite weak-norm result. It is not an essential-height theorem, and the manuscript says so explicitly.

## 5. Audit of the raw local-norm theorem

### 5.1. Truncated fractional potential

For

\[
 P_rv(t)=\int_0^r s^{-\kappa}v(t+s)\,ds,
\]

Minkowski's inequality gives

\[
 \|P_rv\|_{L^q(J)}
 \le (1-\kappa q)^{-1/q}r^{1/q-\kappa}
       \int_{J+(0,r)}v(u)\,du,
\]

provided `1/q>\kappa`. With the manuscript's choice `\eta=1/4`, one has `\kappa=3/8`, and this condition holds throughout the much smaller range `q<32/31`.

The weak-to-strong embedding

\[
 \|f\|_{L^p(J)}
 \le \left(\frac q{q-p}\right)^{1/p}
 |J|^{1/p-1/q}\mathcal N_q(f;J),
 \qquad 1\le p<q,
\]

follows from the distribution-function estimate associated with `\mathcal N_q`. The constant and exponents are correct.

### 5.2. Complete bad-source control

The retained source-shift inequality is applied in the form

\[
 b^\varepsilon
 \le 2A_rb^\varepsilon
 +C\overline{\mathcal F}_r
 +C_\eta\mathsf P_{\eta,r}v^\eta
 +C_\Theta(1+\varepsilon^{-1})\sqrt r\,A_rp.
\]

All terms are complete source terms. The proof takes the collision limsup with `\varepsilon`, `r`, and all auxiliary bands fixed. It then enlarges the bands and only afterwards lets `r` tend to zero with `\varepsilon` fixed. The three `r`-powers are positive:

- the complete surface contributes `r^{\nu_q}`;
- the fractional potential contributes `r^{1/q-\kappa}`;
- the guard term contributes `\sqrt r`.

This yields

\[
 \limsup_m\sup_{R,n,k}\sup_{|J|=L}
 \mathcal N_q(m^2b^\varepsilon;J)
 \le C_qL^{1/q}\varepsilon^{1/16}.
\]

The left side is the original unaveraged bad density. Averaging appears only inside the proof. The source retains all initial momenta, all positive residences, collision incidences, terminal tests, exact labels, and arithmetic classes.

### 5.3. Exact-label local weak and strong laws

Let

\[
 f_{m,R,n,k}(t)
 =m^2p_{n,R}(k,m,t)
 -\mathcal L_{m,R}(k_1,k_2,t,n).
\]

The positive remainder theorem at fixed outer band `B`, combined with the bad-source estimate and

\[
 \varepsilon(B)^{1/16}=A_0^{1/16}B^{-1/192},
\]

gives

\[
\begin{split}
\limsup_m\sup_{R,n,k}\sup_{|J|=L}
\mathcal N_q\bigl(
 f_{m,R,n,k}\mathbf 1_{\mathcal C_{m,R,n,k}(M)};J
\bigr)
\le C_{q,M,L}B^{-1/192}.
\end{split}
\]

The left side is independent of `B`, so sending `B` to infinity last proves convergence to zero. For any

\[
 1\le p<\frac{32}{31}
\]

one chooses `q` strictly between `p` and `32/31` and applies the weak-to-strong embedding.

I find this argument internally consistent, subject to the inherited spectral, source-shift, coarea, and Borel-segment inputs discussed below.

## 6. What has been proved

The new theorem is best stated as follows.

For every fixed central radius `M`, every fixed roof-window length `L`, and every

\[
 1<q<\frac{32}{31},
\]

one has

\[
 \sup_{R,n,k}\sup_{|J|=L}
 \mathcal N_q\bigl(
 (m^2p_{n,R}-\mathcal L_{m,R})
 \mathbf 1_{\mathcal C_{m,R,n,k}(M)};J
 \bigr)
 \longrightarrow0.
\]

For every

\[
 1\le p<\frac{32}{31},
\]

the corresponding strong `L^p` norm on `J\cap\mathcal C(M)` also tends to zero, uniformly in the same parameters and all interval locations of length `L`.

The theorem concerns the original raw density, not a smoothed density and not a roof average. It retains every exact label and all arithmetic peak classes. It is therefore a genuine exact-label raw local-limit result in finite local norms.

## 7. What has not been proved

The revision does not prove any of the following.

### 7.1. No endpoint weak exponent

The argument requires

\[
 1-\frac1q<\frac1{32}.
\]

At `q=32/31` the surface power `\nu_q` is zero. No endpoint Lorentz estimate, logarithmic improvement, or endpoint compactness theorem is supplied.

### 7.2. No growing-window or global central-window norm

The window length `L` is fixed before the collision limit. The central roof range has length of order `\sqrt m`. Covering it by fixed windows introduces a growing number of intervals, and the present theorem gives no summable global estimate. Thus the result is not a global `L^p` LLT on the full central window.

### 7.3. No pointwise essential-height theorem

Finite weak `L^q` and strong `L^p` norms do not control `L^\infty`. A model sequence

\[
 f_j=H_j\mathbf 1_{I_j},
\]

with `H_j\to\infty` and `|I_j|` shrinking sufficiently rapidly can converge to zero in every stated finite norm while its essential supremum diverges. This is exactly the concentration phenomenon isolated by revision 87.

The original pointwise objective

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_{t\in\mathcal C(M)}
 |m^2p_{n,R}(k,m,t)-\mathcal L_{m,R}(k_1,k_2,t,n)|
 \longrightarrow0
\]

therefore remains open.

### 7.4. No zero-charge theorem

The original critical/zero-residence concentration charge remains unproved zero. The local weak-norm theorem controls its distribution at every finite exponent in the stated range, but it does not rule out roof spikes that become taller and narrower with collision count.

### 7.5. No unconditional downstream ratios

Without scalar pointwise closure and a uniform pointwise denominator, the manuscript cannot promote:

- unrestricted same-roof conditional path bridges;
- actual-return clock transfer at the pointwise level;
- forward essential arithmetic likelihood convergence;
- unconditional ratio or posterior statements on all positive arithmetic classes.

The source manifest correctly leaves these flags false.

## 8. The decisive remaining mathematical problem

The remaining task is no longer to prove another fixed-window mass estimate or another finite `L^p` estimate. The manuscript now needs a source-specific mechanism preventing concentration of the original critical/zero-residence source in roof space.

Any successful route must operate uniformly inside

\[
 \limsup_{m\to\infty}
 \sup_{R,n,k}m^2\operatorname*{ess\,sup}_t.
\]

Examples of estimates that would suffice include:

1. a collision-uniform modulus of continuity for the exceptional source density;
2. a Carleson or maximal-function estimate converting the negative residence moment into pointwise height;
3. a collision-uniform BV or directed-variation estimate with acceptable growth in collision count;
4. a reverse-persistence theorem for the exceptional source itself;
5. an endpoint Lorentz improvement strong enough, together with additional regularity, to exclude shrinking spikes;
6. a direct finite-count essential-height envelope covering the union of initial criticality and zero total residence.

A further sequence of finite exponents approaching infinity would not by itself be enough unless the constants are controlled quantitatively in the exponent and uniformly in collision count.

## 9. Dependence on inherited inputs

The new modules are short relative to the full archive but rely on several load-bearing inherited assertions:

- the fixed-band four-record spectral decomposition and Gaussian `m^{-2}` integration;
- the positive short-exit localization estimate with its finite-count remainder;
- the exact physical layer classification for true exits;
- the common Borel maximal-segment parametrization and multiplicity-one pushforward identity;
- the complete angular density and its derivative bound;
- the full source-shift inequality;
- the fixed-width fractional optical source estimate;
- the positive-residence surface essential-height theorem;
- common coarea versions and common null sets for the relevant kernels.

I checked the new uses of these inputs against the active statements and the indicated historical modules. I did not independently reconstruct the anisotropic transfer spaces, the entire four-record spectral theory, or all billiard-geometric layer proofs from first principles. Those imported components remain appropriate targets for an independent human specialist audit.

For a top-four submission, the focused article must make the dependency chain substantially easier to verify. A reader should not have to recover the current theorem by traversing hundreds of historical modules.

## 10. Relation to the parallel main-v88 branch

The repository presently contains two distinct objects called revision 88:

- the main-v88 branch at `e0d462e7b04c35fa3547435ede29adafe1968d8f`, proving higher unconditioned optical moments, a larger shrinking-family envelope, and common-survivor total-variation stability;
- this weak-`L^p` alternative at `24eaaab3b0564c1b8eecbb2217959e3be4320032`, proving negative residence moments, uncut surface weak norms, and local raw-density finite-norm convergence.

Neither branch contains the other's new modules. They share the same revision number and active directory name. This is acceptable for isolated research branches but is not acceptable publication provenance if the branches are later merged or cited without a variant coordinate.

The authors should assign an unambiguous variant identifier or a new revision number before any formal submission. A canonical theorem ledger should state which alternative is being submitted and whether the two advances have been combined on one exact source tree.

## 11. Major comments to the authors

### 11.1. Decide which theorem is the paper's organizing theorem

The present abstract and main theorem prominently advertise the new local weak/strong `L^p` result, while the pointwise objective remains declared as governing. This creates a structural ambiguity.

If the paper remains a pointwise A2-DYN paper, the zero-charge theorem must be proved. If the local finite-norm theorem is intended as the final result of this manuscript, the title, abstract, introduction, literature comparison, and theorem hierarchy should be rewritten around that result, and the pointwise program should be clearly identified as future work rather than the governing assertion.

At the requested benchmark, merely keeping the stronger target in view does not compensate for not proving it.

### 11.2. Make the new proof self-contained at its load-bearing interfaces

The focused article should include, rather than only point to the archive for:

- the precise short-exit spectral estimate used in module 205;
- the physical cap and the finite candidate-disk clearance geometry;
- the Borel maximal-segment map and exact density formula;
- the derivative formula for the complete angular density;
- the source-shift inequality in the exact normalization used here;
- the long-residence surface theorem and fixed-width fractional input.

A concise but complete theorem-input section is preferable to a long historical supplement whose current and superseded claims must be reconstructed by the reader.

### 11.3. Clarify sharpness and the role of `32/31`

The exponent `32/31` is inherited from the currently available residence exponent `1/32`, not presented as a physical sharp threshold. The article should say this explicitly near the main theorem and discuss which input would improve it. In particular, an improved short-residence exponent `\gamma` would formally lead to `q<1/(1-\gamma)` through the present pulse argument.

### 11.4. Do not infer global or pointwise results from local norms

The manuscript itself respects this distinction. It should remain explicit in every abstract, status file, and downstream theorem. Fixed `L`, finite `q`, and collision-uniform interval location do not imply a growing-window norm or an essential-supremum theorem.

### 11.5. Preserve scalar-first normalization

No same-roof ratio or likelihood theorem should be promoted until the scalar pointwise denominator is controlled. The local strong `L^p` theorem is not enough to divide pointwise by the reference density, especially on arithmetic zero classes.

## 12. Expository, provenance, and validation comments

1. `SOURCE_MANIFEST.json` contains both `new_estimate` and `new_complete_estimate`. The former still describes the revision-87 shrinking-gradient/residence envelope, whereas the latter describes the actual weak-`L^p` increment. This stale field should be removed, renamed as an inherited estimate, or clearly labelled as provenance.
2. Add a unique variant identifier to the manifest, revision index, PDF metadata, and artifact names. Two unrelated v88 commits using the same active directory name create unnecessary audit risk.
3. The focused article should state the weak norm definition before the abstract's first use of “weak `L^q`,” and should call it a norm equivalent to the Lorentz weak norm rather than silently identifying all normalizations.
4. The proof should retain the finite-count capped remainder visibly until after the negative-moment layer cake. This is currently done correctly and should not be compressed away.
5. The whole-segment trace identity and the origin of the `(u-a)` factor deserve a displayed explanatory paragraph in the journal article.
6. State at first use that the outgoing trace is nongrazing and that grazing exits are paid through the inherited two-sided optical/source budget.
7. Give one diagram showing the flow from short-residence cap to negative moment, then to surface weak norm, bad-source weak norm, and raw local LLT.
8. Explain explicitly that uniformity over all interval locations of fixed length does not give a norm on the full `O(\sqrt m)` central range.
9. Keep all qualification language separate from mathematical proof. Finite fixtures, source preservation, TeX compilation, and PDF geometry do not certify the continuum spectral or coarea arguments.
10. At the time this report was frozen, exact-SHA workflow runs `38220442356` and `38220448221` were queued. They must not be described as successful evidence unless their final conclusions are actually checked.
11. The complete supplement remains extremely large. Provenance and superseded revision history should be separated from the technical supplement required to verify the current theorem.
12. Continue to state that no independent human specialist audit or formal proof certificate has been obtained.

## 13. Qualification evidence

The active validation contract checks preservation of the inherited source, normal/optimized agreement of finite diagnostics, native TeX builds, the recorder union of all 207 core modules, references, warnings, and PDF geometry.

These checks are useful for source identity and regression control. They do not verify:

- the four-record spectral assumptions;
- the physical clearance geometry;
- the complete coarea disintegration;
- the Borel segment bijection;
- the zero-charge theorem;
- any continuum essential-height statement.

At report freeze, both new exact-SHA runs were queued. I therefore record no remote qualification success in this report.

## 14. Editorial assessment at the requested benchmark

The local weak/strong `L^p` theorem is a real advance. It shows that the raw exact-label density error is not merely small after averaging: it converges in a family of finite local norms, uniformly across physical parameters and exact labels. The route through a physical short-residence cap, a finite-count negative moment, and complete segment traces is conceptually coherent and may be reusable.

Nevertheless, the current exponent range is close to `L^1`, the result is local on fixed roof windows, and the paper's organizing pointwise theorem remains open. The manuscript also depends on a very large inherited architecture whose load-bearing analytic and geometric inputs have not received independent specialist verification.

For a top-four journal, the combination of an unproved governing theorem, the absence of pointwise closure, and the current presentation burden is decisive. The paper should not be accepted in its present form.

## 15. Final assessment

Revision 88 weak-`L^p` proves or materially strengthens:

- a collision-uniform physical cap for short total residence;
- actual negative total-residence moments with no positive lower cutoff;
- a complete nongrazing first-exit surface weak-`L^q` estimate without a residence or gradient cutoff;
- weak-`L^q` convergence of the original exact-label raw density error on every fixed-length local roof interval for `1<q<32/31`;
- strong local `L^p` convergence for every `1\le p<32/31`;
- preservation of every exact label, arithmetic peak, source normalization, and zero class.

I found no decisive flaw in modules 205--207 at the level of this referee-style audit. The most delicate inherited spectral, geometric, coarea, and segment inputs still require independent human verification.

The revision does not prove:

- the endpoint `q=32/31`;
- a growing-window or global central-window `L^p` theorem;
- zero critical/zero-residence concentration charge;
- the unrestricted exact-label pointwise raw LLT;
- the pointwise roof-density LLT;
- unconditional path, clock, ratio, or likelihood consequences.

The organizing pointwise theorem therefore remains open within the submitted manuscript.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
