# Independent Referee Report — Round 15

**Manuscript:** B1 — *Microcanonical Preparation*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence and submission integrity

The submitted folder remains Round Fourteen. No Round-Fifteen B1 module or certificate is present, and no complete B1 candidate was recoverable from the truncated payload. The branch is therefore not a self-contained Round-Fifteen submission.

## Executive assessment

Extracting exact particle number before continuous Fourier inversion is the correct response to the grand-canonical empty-sector atom, and source-dependent finite saddles are necessary. The controlling proof still fails to establish a positive exact-\(N\) coefficient law with the claimed smoothing, and its formal high-frequency theorem contains a nonintegrable constant term. Consequently the sharp shell coefficient and microcanonical transfer are not proved.

## Decisive objections

### 1. The formal high-frequency bound is not integrable

The theorem states, for \(|u|>R\),

\[
|\varphi_{\varepsilon,N,H}(u)|
\le e^{-cN}+C_s(1+|u|)^{-s-c_0N}.
\]

The first term is constant in \(u\), hence

\[
\int_{|u|>R}e^{-cN}\,du=\infty.
\]

The claimed \(o(N^{-d/2})\) Fourier tail cannot follow.

The proof later substitutes a different estimate,

\[
e^{-cN}(1+|u|)^{-s}+(1+|u|)^{-s-c_0N},
\]

but this is not the stated theorem and is not implied by the preceding “fewer than \(c_0N\) regular components” alternative. The exceptional class may contain no smoothing component at all.

### 2. The Chernoff argument has no positive probability measure

Connected polymer activities in a hard-core/log-partition expansion are generally signed, and under complex sources they are complex. The proof marks selected polymers by an auxiliary variable and treats the derivative of a coefficient pressure as the mean number of regular components under a positive law, then applies Chernoff's inequality.

No positive measure on polymer partitions with those weights is constructed. Absolute-value cluster bounds do not turn signed Ursell activities into probabilities, and positivity of the total canonical coefficient does not imply positivity term by term.

### 3. A local smooth component does not smooth the complete coefficient law

The proof identifies finitely many regular polymer types whose mark map is a submersion on a positive-activity patch. This gives an absolutely continuous component of their pushforward. It does not show that every configuration in the claimed good sector contains independent copies of those components, nor that the conditional distribution after fixing the rest factorizes sufficiently to multiply Fourier decays.

The matching/dependency lemma and its uniformity under source-decorated hard-sphere trajectories are not proved.

### 4. The exact-\(N\) saddle theorem assumes the coefficient expansion it needs

Normal convergence of a grand-canonical cluster expansion on an activity annulus does not by itself yield a uniform canonical coefficient asymptotic with three derivatives. One needs a zero-free annulus, a unique complex saddle, a quantitative off-central angular gap, and uniform control of the coefficient after the dynamical source is inserted.

The proof cites “span-one particle count and polymer aperiodicity” without proving the relevant modulus gap for the signed coefficient generating function.

### 5. The shell class partly defines the desired conclusion

A shell is called regular when smooth approximations have Fourier error

\[
r_\varepsilon=o(g_\varepsilon\mu_\varepsilon^{-d/2}).
\]

This is essentially the error comparison needed for the local theorem. No geometric criteria are supplied that verify it beyond expanding central boxes. As a result, the theorem is not a derived uniform shell result but a conditional restatement.

### 6. The full Hessian lower bound is not obtained from component occurrence alone

Even if linearly many regular components existed under a positive canonical law, correlations imposed by exact particle number, hard-core exclusion, and dynamical source tilts can create cancellations or degeneracies in aggregate constraint directions. A uniform covariance lower bound requires a conditional tensorization or block-decoupling theorem, not merely positive activity of several local types.

### 7. The entire hard-sphere input remains conditional on B2

The source \(H\), connected trajectory polymers, all-contact majorant, and source derivatives are imported from B2. B2's fixed-horizon actual-contact expansion and lower recovery remain unproved. Thus B1 cannot serve as an independent bridge from physical preparation to the rest of the hard-sphere series.

## Required reconstruction

Construct a genuinely positive canonical representation or use analytic coefficient estimates without probabilistic Chernoff language. State one correct global Fourier majorant and prove it for every sector. Then derive, rather than encode into the definition, a quantitative shell class and source-uniform coefficient theorem.

## Recommendation

**Reject.** The purported Round-Fifteen revision is absent, and the controlling exact-number proof still lacks both positivity and a valid integrable high-frequency estimate.
