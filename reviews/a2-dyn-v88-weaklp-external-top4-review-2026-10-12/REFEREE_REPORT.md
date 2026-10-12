# External top-four referee report on A2-DYN revision 88 — weak-Lp alternative

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v88-weaklp-referee-response-2026-10-12`, `revision/a2-dyn-v88-weaklp-referee-copy-2026-10-12`  
**Reviewed author commit:** `24eaaab3b0564c1b8eecbb2217959e3be4320032`  
**Reviewed repository tree:** `a91219a03b468ed239e1ffa97600a3ca8a6a21e3`  
**Active manuscript directory:** `papers/A2-DYN-v88-referee-response`  
**Active source:** 207 core modules; this alternative adds modules 205–207  
**Immediate baseline:** revision 87 at `44785327cc0331d994d5d1de371710615cfd6b93`  
**Frozen v87 paper tree:** `086086bf42a833b241422b0b8a145fa5771a6f2d`  
**Controlling report:** `reviews/a2-dyn-v85-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `af90a4e75bb4262cf16e64ff5e62a688bc21c007` / `86ecdfdf87d9ad7f6ecbe20c97f10cc75967eec5`  
**Parallel main-v88 commit:** `e0d462e7b04c35fa3547435ede29adafe1968d8f`; the present source is an independent alternative descended from v87  
**Qualification runs at report freeze:** response `38220442356`; copy `38220448221`; both queued  
**Date:** 12 October 2026  
**Benchmark:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, editorial decision, formal proof certificate, or independent human specialist audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

The weak-Lp alternative is a genuine theorem-bearing revision. It proves new finite local-norm results for the original unaveraged exact-label roof density, rather than merely restating the critical/zero-residence charge isolated in revision 87. In particular, it establishes:

1. a collision-count-uniform physical cap for short total residence and actual negative residence moments without a positive lower cutoff;
2. a complete nongrazing first-exit surface estimate in weak `L^q`, without a residence or initial-gradient cutoff, for every `1<q<32/31`; and
3. local weak-`L^q` and strong-`L^p` convergence of the original exact-label raw density error on every fixed-length roof interval, uniformly in interval location and all physical and arithmetic labels, for `q<32/31` and `p<32/31`.

I found no decisive counterexample, sign reversal, exponent error, hidden collision-dependent Fourier band, word-count loss, or illicit claim that finite local norms imply essential-height control.

The negative recommendation is nevertheless forced by the manuscript's own governing objective. The unrestricted exact-label pointwise raw local limit theorem remains open. Finite weak and strong `L^p` norms allow increasingly narrow high roof spikes and therefore do not imply vanishing of the collision-normalized essential supremum or of the original microscopic concentration charge.

At the requested benchmark, a manuscript organized around the pointwise theorem must prove that theorem. The new local-norm result is substantial, but it is not a substitute for pointwise closure.

## 2. Frozen source and variant identity

Both reviewed author branches resolve to

`24eaaab3b0564c1b8eecbb2217959e3be4320032`.

This commit has parent

`44785327cc0331d994d5d1de371710615cfd6b93`,

the exact v87 baseline. It preserves 204 inherited core modules and adds:

- `core/205_capped_negative_residence_moments.tex`;
- `core/206_uncut_surface_lorentz_control.tex`;
- `core/207_exact_label_raw_density_local_norm.tex`.

The repository also contains a separate main-v88 source at `e0d462e7b04c35fa3547435ede29adafe1968d8f`. The two v88 objects have different modules 205–207 and prove different theorems. The present report therefore treats the weak-Lp pair as an independent alternative manuscript, not as a descendant or replacement of main v88.

The active README, response, proof ledger, publication status, referee status, and source manifest correctly state that the pointwise theorem remains open and that the local-norm result is not pointwise closure.

## 3. Audit of module 205: physical cap and negative residence moments

Let

\[
\ell=\tau^-+\tau^+
\]

be the total residence of the original maximal regular exact-event segment. It is not the collision return time.

### 3.1. Count-independent short-residence cap

The module proves, uniformly in collision count, radius, and exact labels,

\[
\bar\nu\{\ell\le s\}\le \bar\nu\{\tau^+\le s\}\le C s^{1/2}.
\]

The proof uses the actual first-exit layer classification. Incidence layers have quadratic mass in incidence width, while section-edge and flight-clearance layers have linear mass in geometric width. Physical layer widths are proportional to `q_0^d sqrt(s)`, and only boundedly many marks occur at each depth, so the geometric depth sum gives the square-root cap.

The cap is applied to the full positive probability. The manuscript does not incorrectly attribute it to an unsigned spectral remainder in isolation.

### 3.2. Capped finite-count remainder

Combining the physical cap with the retained fixed-band short-exit estimate gives

\[
\begin{aligned}
 m^2\bar\nu\{F\in J,\ell\le s\}
 \le{}& C s^{\gamma_0}(|J|+B_*^{-1})\\
 &+C_{B_*}(1+B_*|J|)m^3
 \min\{\rho_{B_*}^{m/2},s^{1/2}\},
\end{aligned}
\]

where `gamma_0=1/32`. The minimum is essential: an error independent of the residence threshold would be nonintegrable in the subsequent negative-moment layer cake.

### 3.3. Layer cake

For `0<upsilon<gamma_0`, the actual source is

\[
q_{\upsilon,s}(t)\,dt
=F_\#\bigl(\ell^{-\upsilon}
\mathbf 1_{\{0<\ell\le s\}}\bar\nu\bigr).
\]

The proof uses

\[
\ell^{-\upsilon}\mathbf 1_{\{\ell\le s\}}
=s^{-\upsilon}\mathbf 1_{\{\ell\le s\}}
+\upsilon\int_0^s v^{-\upsilon-1}
\mathbf 1_{\{\ell\le v\}}\,dv
\]

with positive lower truncations and monotone convergence. The exact identity

\[
\begin{aligned}
&s^{-\upsilon}\min(D,s^{1/2})
+\upsilon\int_0^s v^{-\upsilon-1}\min(D,v^{1/2})\,dv\\
&\qquad=\frac{1}{1-2\upsilon}
\min\{s^{1/2-\upsilon},D^{1-2\upsilon}\}
\end{aligned}
\]

is correct. Splitting at `v=D^2` cancels the boundary terms.

Consequently, after fixing interval length, residence width, and auxiliary band before the collision limsup,

\[
\limsup_m\sup_{R,n,k}\sup_{|J|=L}
 m^2\int_J q_{\upsilon,s}(t)\,dt
\le C_\upsilon L s^{1/32-\upsilon}.
\]

The physical cap gives fixed-count finiteness for negative orders below `1/2`; ordered decay uses the stricter range below `1/32`. The manuscript distinguishes these scopes correctly.

## 4. Audit of module 206: complete uncut surface weak norm

### 4.1. Weak norm and pulse lemma

For `q>1`, the manuscript defines

\[
\mathcal N_q(f;J)=
\sup_{E\subset J,\ 0<|E|<\infty}
|E|^{-1+1/q}\int_E|f(t)|\,dt.
\]

This is a norm equivalent to the standard weak-`L^q` Lorentz quasi-norm and is subadditive.

For weighted interval pulses, Tonelli gives a contribution bounded by `T min(v,ell)` on a measurable set of measure `v`. With `upsilon=1-1/q`,

\[
v^{-\upsilon}\min(v,\ell)\le \ell^{1-\upsilon},
\]

so arbitrary overlap of physical roof intervals is allowed. No disjointness assumption is hidden in the proof.

### 4.2. Whole-segment trace

On one maximal segment the exact angular density is

\[
A=\frac{\omega}{4\pi c_*\chi},
\]

and the retained derivative bound is

\[
|A'|\le C A I_m/z.
\]

For `a<t<b`, integrating

\[
A(b-)\le A(t)+C\int_t^b A(u)I_m(u)/z(u)\,du
\]

over the whole segment produces the load-bearing triangular factor:

\[
\begin{aligned}
A(b-)\ell^{1-\upsilon}
\le{}&\int_a^b A(t)\ell^{-\upsilon}\,dt\\
&+C\ell^{-\upsilon}
\int_a^b (u-a)A(u)I_m(u)/z(u)\,du.
\end{aligned}
\]

Forward radial growth gives `z(u)^2 >= 2 lambda_0 (u-a)`. With `kappa=(1-eta)/2`,

\[
(u-a)z(u)^{-1}
\le C_\eta (u-a)^{1-\kappa}z(u)^{-\eta}.
\]

The exponent arithmetic is correct. The variation term is therefore bounded by

\[
C_\eta s^{1-\kappa-\upsilon}
\int_a^b A I_m z^{-\eta}.
\]

Both `omega` and `chi` are differentiated through the complete density. No inverse Jacobian is set equal to one.

### 4.3. Multiplicity-one complete sum

The Borel maximal-segment parametrization counts each physical interior point once, with incident components kept distinct. The outgoing nongrazing selector is retained on the trace side and dropped only on positive upper sources. No physical-word multiplier is introduced.

### 4.4. Exponent range

Writing

\[
\upsilon=1-\frac1q,
\]

the short-surface rate is `s^(1/32-upsilon)`. Hence the precise admissible range is

\[
1<q<\frac{32}{31}.
\]

For the complete first-exit surface, long residences are paid by the inherited positive-residence height theorem and short residences by the finite-count negative moment. The final rate is

\[
\nu_q=\frac1q-\frac{31}{32}>0,
\]

with

\[
\limsup_m\sup_{R,n,k}\sup_{|J|=L}
\mathcal N_q(m^2\overline{\mathcal F}_r;J)
\le C_{q,L}r^{\nu_q}.
\]

The endpoint `q=32/31` is correctly excluded, and the theorem is not relabelled as an essential-supremum estimate.

## 5. Audit of module 207: original raw density in local norms

### 5.1. Truncated potential and embedding

For

\[
P_rv(t)=\int_0^r s^{-\kappa}v(t+s)\,ds,
\]

Minkowski gives

\[
\|P_rv\|_{L^q(J)}
\le (1-\kappa q)^{-1/q}r^{1/q-\kappa}
\int_{J+(0,r)}v(u)\,du
\]

when `1/q>kappa`. With `eta=1/4`, `kappa=3/8`, so this holds throughout the stated range.

The distribution-function argument also gives, for `1<=p<q`,

\[
\|f\|_{L^p(J)}
\le \left(\frac q{q-p}\right)^{1/p}
|J|^{1/p-1/q}\mathcal N_q(f;J).
\]

The constants and exponents are correct.

### 5.2. Complete bad-source control

The retained source-shift inequality is used as

\[
b^\varepsilon
\le 2A_rb^\varepsilon
+C\overline{\mathcal F}_r
+C_\eta\mathsf P_{\eta,r}v^\eta
+C_\Theta(1+\varepsilon^{-1})\sqrt r\,A_rp.
\]

All terms are complete source terms. The proof fixes `epsilon`, `r`, and auxiliary bands before the collision limsup, enlarges bands afterwards, and finally lets `r` decrease with `epsilon` fixed. The surface, potential, and guard powers are all positive. It obtains

\[
\limsup_m\sup_{R,n,k}\sup_{|J|=L}
\mathcal N_q(m^2b^\varepsilon;J)
\le C_qL^{1/q}\varepsilon^{1/16}.
\]

The target is the original unaveraged density; averaging is only an intermediate proof operation.

### 5.3. Raw exact-label LLT

Let

\[
f_{m,R,n,k}(t)=m^2p_{n,R}(k,m,t)
-\mathcal L_{m,R}(k_1,k_2,t,n).
\]

At a fixed outer reconstruction band `B`, the positive remainder theorem and the bad-source estimate yield

\[
\begin{aligned}
\limsup_m\sup_{R,n,k}\sup_{|J|=L}
\mathcal N_q\bigl(
 f_{m,R,n,k}\mathbf 1_{\mathcal C_{m,R,n,k}(M)};J
\bigr)
\le C_{q,M,L}B^{-1/192}.
\end{aligned}
\]

The left side is independent of `B`, so `B` may be sent to infinity last. Thus, for every fixed `M,L>0` and `1<q<32/31`, the original exact-label error converges to zero locally in weak `L^q`, uniformly in all stated parameters and interval locations. Choosing `p<q<32/31` gives strong local `L^p` convergence for every `1<=p<32/31`.

I find this argument internally consistent, subject to the inherited spectral, coarea, source-shift, and Borel-segment inputs.

## 6. Exact scope of the theorem

The new conclusion is a genuine raw local-limit theorem in finite local norms. It retains:

- the original section and normalization;
- the original smooth guard;
- exact displacement and occupation labels;
- every retained arithmetic peak and zero class;
- the original unaveraged roof density.

Its uniformity is strong with respect to physical parameters and interval location, but the interval length `L` is fixed before the collision limit.

## 7. What remains unproved

### 7.1. Endpoint exponent

At `q=32/31`, the surface power `nu_q` vanishes. No endpoint Lorentz estimate or logarithmic improvement is proved.

### 7.2. Growing-window or global central-window norm

The central roof region has length of order `sqrt(m)`. Covering it by fixed-length windows introduces a growing number of intervals. The present theorem therefore does not imply a global `L^p` theorem on the full central window.

### 7.3. Pointwise essential height

Finite weak and strong norms do not control `L^infinity`. A sequence of increasingly tall pulses supported on sufficiently narrow intervals can converge in every finite norm stated here while its essential supremum stays positive or diverges.

Hence the governing pointwise objective remains open:

\[
\sup_{R,n,k}\operatorname*{ess\,sup}_{t\in\mathcal C(M)}
|m^2p_{n,R}(k,m,t)-\mathcal L_{m,R}(k_1,k_2,t,n)|
\longrightarrow0.
\]

### 7.4. Zero concentration charge

The original critical/zero-residence charge has not been proved zero. The finite-norm theorem controls distributions of heights but does not exclude spikes collapsing with collision count.

### 7.5. Downstream laws

Without scalar pointwise closure and a pointwise denominator, the manuscript cannot promote unrestricted same-roof path bridges, pointwise clock transfer, essential likelihood convergence, or unconditional ratio statements. The manifest correctly leaves these claims false.

## 8. Decisive remaining mathematical task

The next theorem must prevent concentration of the original exceptional source inside

\[
\limsup_{m\to\infty}
\sup_{R,n,k}m^2\operatorname*{ess\,sup}_t.
\]

A successful route could be a collision-uniform modulus of continuity, a Carleson or maximal estimate, a BV/directed-variation estimate with acceptable collision growth, a reverse-persistence theorem for the exceptional source, or a direct finite-count essential-height envelope covering initial criticality and zero total residence.

Another fixed-window mass estimate or another finite exponent alone will not close the pointwise theorem.

## 9. Imported inputs requiring specialist verification

The new modules rely on:

- the fixed-band four-record spectral decomposition and Gaussian `m^-2` integration;
- the positive finite-count short-exit estimate;
- the physical true-exit layer classification;
- the Borel maximal-segment bijection and multiplicity-one pushforward;
- the full angular-density derivative bound;
- the source-shift inequality;
- the fixed-width fractional optical input;
- the positive-residence surface height theorem;
- common coarea versions and common null sets.

I checked the new uses against the active statements and relevant historical modules. I did not independently reconstruct the full anisotropic transfer spaces, four-record spectral theory, or every billiard-geometric layer proof. These remain appropriate targets for independent human review.

## 10. Major editorial comments

1. **Choose the organizing theorem.** If the manuscript remains a pointwise A2-DYN paper, the zero-charge theorem must be proved. If the finite local-norm theorem is intended as the final result, the title, abstract, introduction, literature comparison, and theorem hierarchy should be rewritten around that theorem.
2. **Make load-bearing interfaces self-contained.** The focused article should state the exact short-exit spectral estimate, physical cap, Borel segment map, angular-density derivative, source-shift inequality, fractional input, and long-residence surface theorem in the normalization actually used.
3. **Explain the exponent.** The endpoint `32/31` comes from the available residence exponent `1/32`; it is not claimed to be physically sharp. This should be explicit.
4. **Preserve the local/global/pointwise distinction.** Fixed `L`, finite `q`, and uniform interval location do not yield a growing-window norm or essential-supremum theorem.
5. **Maintain scalar-first normalization.** No path ratio or likelihood theorem should be promoted from the local finite-norm result alone.

## 11. Provenance and validation comments

1. `SOURCE_MANIFEST.json` contains both `new_estimate` and `new_complete_estimate`. The former still describes the inherited v87 shrinking-gradient/residence envelope; the latter describes the present weak-Lp increment. The stale field should be removed, renamed as inherited, or clearly labelled as provenance.
2. Two independent objects currently use revision number 88 and the same active directory name. Add a canonical variant identifier or assign a new revision number before formal submission.
3. Keep the finite-count capped remainder visible until after the negative-moment layer cake; this is presently done correctly.
4. Give a dependency diagram from the short-residence cap through the negative moment and surface norm to the raw local LLT.
5. State explicitly that uniformity over interval locations of fixed length does not yield a full central-window norm.
6. Keep source receipts, fixtures, TeX compilation, and PDF geometry outside the mathematical argument.
7. At report freeze, workflow runs `38220442356` and `38220448221` were queued. They are not recorded here as passing evidence.
8. Continue to state that no independent human specialist audit or formal proof certificate has been obtained.
9. Separate the technical supplement needed for the current theorem from the much larger provenance and superseded-revision archive.

## 12. Qualification evidence

The validation contract checks exact-source preservation, normal/optimized agreement of finite diagnostics, native TeX builds, the union of all 207 core modules, references, warnings, and PDF geometry. These are useful source-integrity checks. They do not prove the continuum spectral, geometric, coarea, surface, or zero-charge assertions.

Both exact-SHA runs were queued when this report was frozen, so no remote success is claimed.

## 13. Final assessment

Revision 88 weak-Lp proves or materially strengthens:

- a collision-uniform short-residence physical cap;
- actual negative total-residence moments without a positive lower cutoff;
- a complete nongrazing first-exit surface weak-`L^q` estimate without residence or gradient cutoffs;
- local weak-`L^q` convergence of the original exact-label raw error for `1<q<32/31`;
- local strong `L^p` convergence for `1<=p<32/31`;
- preservation of all exact labels, arithmetic classes, and original source normalization.

I found no decisive flaw in modules 205–207 at the level of this referee-style audit. The most delicate inherited spectral, billiard-geometric, coarea, and segment inputs still require independent human verification.

The revision does not prove:

- the endpoint `q=32/31`;
- a growing-window or global central-window norm theorem;
- zero critical/zero-residence concentration charge;
- the unrestricted exact-label pointwise raw LLT;
- the pointwise roof-density LLT;
- unconditional path, clock, ratio, or likelihood consequences.

The organizing pointwise theorem therefore remains open.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
