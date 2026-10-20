# External top-four referee report on A2-DYN revision 89

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v89-referee-response-2026-10-12`, `revision/a2-dyn-v89-referee-copy-2026-10-12`  
**Reviewed author commit:** `48e372ed14472bb307c88b25c88ec9febd67900c`  
**Reviewed repository tree:** `fd9283755e918241bfec9c23d99b342634e045df`  
**Active manuscript directory:** `papers/A2-DYN-v89-referee-response`  
**Canonical revision identity:** `a2-dyn-v89-critical-distribution-2026-10-12`  
**Active source:** 210 core modules; revision 89 adds modules 208--210  
**Immediate mathematical baseline:** weak-Lp revision 88 at `24eaaab3b0564c1b8eecbb2217959e3be4320032`  
**Frozen weak-Lp v88 paper tree:** `af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6`  
**Controlling weak-Lp report:** `reviews/a2-dyn-v88-weaklp-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `c615c2e8a9ac955634fceb5c6f7ab0da8263af6e` / `90affffc4882c6312707aea59b0d2c51d6f4be28`  
**Parallel main-v88 report commit / blob:** `3b1fb458831d4a1a2e51d01ab4682b30ae1a6cb7` / `874290c1568d86c93d7e93606b05fc8439d6662f`  
**Parallel main-v88 source:** `e0d462e7b04c35fa3547435ede29adafe1968d8f`, preserved paper tree `1c3e7c85c15f7265f66f8ee96ce6617d2f65488d`  
**Qualification runs at review freeze:** response `38229077381`; referee-copy `38229086853`; both queued, with no conclusion  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 89 is a genuine theorem-bearing revision and a substantive advance over both revision-88 alternatives. It should not be described as a metadata-only merge of the two histories. The new source continues the weak-Lp alternative, preserves the complete parallel main-v88 source under a distinct directory, and adds three new mathematical modules:

- `core/208_critical_surface_distribution.tex`;
- `core/209_logarithmic_endpoint_and_exceptional_source.tex`;
- `core/210_diffusive_window_and_exact_limit_order.tex`.

The new argument reaches the previously excluded critical distribution exponent

```text
Q = 32/31
```

for the complete untruncated outgoing first-exit surface. It does so by retaining the measure of the tested roof set through the finite-count residence-band sum, rather than by substituting the endpoint order into a negative-residence moment theorem that is valid only below the endpoint. From this it obtains:

1. a collision-count-uniform critical weak bound for the complete first-exit surface;
2. a critical weak bound for the original exact-label raw density;
3. raw-error convergence at the critical exponent with every positive logarithmic loss;
4. a logarithmic critical estimate acting directly on the original critical-or-short-residence exceptional union; and
5. strong subcritical and logarithmically weakened critical convergence on the complete central roof window in the natural diffusive measure `dt/sqrt(m)`.

I found no decisive counterexample, sign error, exponent mismatch, illicit interchange of a collision limit with an infinite residence sum, hidden collision-dependent Fourier band, or omitted gluing factor in the three new modules. The finite-count remainder exponent, the mass-to-logarithmic interpolation, and the diffusive coordinate normalization are mutually consistent.

The negative recommendation is nevertheless forced by the manuscript's own unchanged governing assertion. The paper continues to organize itself around the pointwise exact-label raw local limit

```text
sup_{R,n,k} esssup_t |m^2 p_{n,R}(k,m,t) - L_{m,R}(k,t,n)| -> 0
```

on the full central class. Revision 89 does not prove this statement. It explicitly retains the original exceptional-source essential-height charge and explicitly states that the charge has not been proved zero.

This is not a merely quantitative gap between two versions of an otherwise completed theorem. Critical weak bounds, logarithmically weakened endpoint convergence, and finite-p convergence permit roof spikes whose supports shrink while their essential heights remain bounded away from zero or diverge. The new estimates strongly constrain the distribution of such spikes, but do not exclude them. Therefore the remaining charge is precisely the pointwise theorem, not a dispensable remainder after it.

At the requested benchmark, a paper whose title, introduction, source architecture, and principal endpoint are the unrestricted pointwise raw local limit theorem must prove that theorem. Revision 89 materially sharpens the last obstruction but does not close it.

## 2. Frozen source, chronology, and variant identity

Both reviewed revision-89 branches resolve to

`48e372ed14472bb307c88b25c88ec9febd67900c`.

The repository tree is

`fd9283755e918241bfec9c23d99b342634e045df`.

The active article is

`papers/A2-DYN-v89-referee-response`.

The source manifest identifies the weak-Lp revision-88 manuscript as the immediate mathematical baseline:

`24eaaab3b0564c1b8eecbb2217959e3be4320032`,

with frozen paper tree

`af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6`.

All 207 inherited weak-Lp core modules are retained, and the three modules listed above raise the active count to 210. The complete preceding weak-Lp article is compiled in `supplement.tex`.

The repository also preserves the different main-v88 author source at

`e0d462e7b04c35fa3547435ede29adafe1968d8f`

under `papers/A2-DYN-v88-main-preserved`, with its source tree separately pinned. This is the correct treatment: the two revision-88 variants had incompatible modules 205--207 and proved different theorems, so silently combining their module numbering would have destroyed source identity.

The present report treats revision 89 as a descendant of the weak-Lp alternative which also responds to the mathematical objections in the parallel main-v88 report. It does not treat the parallel source as an alternative baseline for the new theorem.

The review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v89-external-top4-review-2026-10-12/`.

No author manuscript, revision branch, workflow, prior report, preserved variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-89 exact-SHA workflow runs are:

- response branch run `38229077381`;
- referee-copy branch run `38229086853`.

At the time this report was frozen, both runs were queued and had no conclusion. I therefore do not describe revision 89 as having completed remote qualification.

The declared validation protocol is meaningful. A completed run is designed to check:

- the weak-Lp v88 baseline tree;
- the parallel main-v88 preserved tree;
- both controlling report blobs;
- byte preservation of all inherited sources and top-level snapshots;
- inclusion and recorder coverage of all 210 active modules;
- ordinary and optimized finite-fixture agreement;
- native builds of the focused article and the complete supplement;
- stable references and warning gates; and
- PDF geometry.

These checks would establish source identity, finite algebraic consistency, and typesetting reproducibility. They would not certify the continuum coarea identities, Borel disintegration, optical derivative estimates, inherited four-record spectral theorem, critical source comparison, or the pointwise concentration charge. The manuscript correctly states this limitation.

## 4. Scope of this audit

The complete source contains a focused journal article and a very large technical supplement carrying 207 inherited modules. I have not independently re-proved the entire historical pipeline.

The substantive review concentrates on:

1. both revision-88 external reports and the exact objections carried into revision 89;
2. the capped dyadic pulse sum and critical measurable-set estimate in module 208;
3. the passage from the complete surface to the original raw density;
4. the endpoint interpolation lemma and logarithmic critical convergence in module 209;
5. the estimate on the original exceptional union itself;
6. the interval gluing and diffusive coordinate change in module 210;
7. the relation of these finite-norm conclusions to the unchanged pointwise target;
8. limit order, exact labels, physical source, guard, and arithmetic classes;
9. source-variant preservation; and
10. the top-four significance and completeness standard.

The inherited local source estimates, physical flow identities, scalar positive remainder, maximal-segment parametrization, long-residence height estimate, and subcritical weak-Lp theorem are treated as source-pinned inputs. Their interfaces with the new proof are audited here; this report does not convert them into independently certified theorems.

## 5. The governing pointwise assertion

The event remains the original exact four-coordinate actual-return event. The initial section visit is counted, the terminal section visit is tested separately, and no displacement or occupation class is pooled. The density is `p_{n,R}(k,m,t)`, and the reference is the complete finite-peak expression `L_{m,R}` with all active arithmetic charts retained.

The governing assertion is the essential-supremum limit

```text
sup_{R,1<=n<=m,k} esssup_{t in C(M)}
|m^2 p_{n,R}(k,m,t) - L_{m,R}(k,t,n)| -> 0.
```

The retained positive scalar decomposition has the form

```text
m^2 p - L = m^2 b^{epsilon(B)} + e_B,
```

where `b^{epsilon(B)}` is nonnegative and the remainder `e_B` is pointwise small after the outer reconstruction band is enlarged. The unresolved task is therefore to prove that the original weighted source `b^{epsilon(B)}` has zero collision-normalized essential-height charge in the cofinal source limit.

Revision 89 proves new distributional restrictions on this source. It does not prove the required essential-height statement.

The distinction can be seen without any billiard-specific subtlety. On a fixed interval, the functions

```text
f_j = 1_[0,delta_j]
```

satisfy `||f_j||_infinity = 1` while their weak-`L^(32/31)` measurable-set norm tends to zero as `delta_j -> 0`. Adding a logarithmic denominator only weakens that topology further. Positivity does not prevent this phenomenon. Consequently, even unweakened critical weak convergence would not by itself imply the pointwise theorem; a source-specific anti-concentration or oscillation mechanism is still indispensable.

## 6. Module 208: capped dyadic pulse sums

### 6.1. The elementary sums

The first new lemma proves

```text
sum_j min(1,2v/s_j) s_j^theta <= C_theta min(v^theta,s^theta)
```

for the dyadic scales `s_j=2^(-j)s`.

The split at the first `s_j <= v` is correct. Earlier scales contribute

```text
2v s_j^(theta-1),
```

whose geometric sum is of order `v^theta`; later scales contribute a geometric tail of the same order.

The capped inequality

```text
min(D,x^a) <= D^(1-gamma/a) x^gamma
```

for `0<gamma<a<1` is also correct. With `a=1/2`, `gamma=1/32`, and `D=rho^(m/2)`, it gives the exponent

```text
D^(1-2gamma) = rho^(15m/32).
```

I find no error in this exponent arithmetic.

### 6.2. Retaining the tested-set measure

The key conceptual improvement is that a segment of residence length `ell` contributes

```text
T_sigma min(|E|,ell)
```

to a tested roof set `E`. Revision 89 retains this minimum through the complete residence-band sum. This is what permits the endpoint exponent `gamma=1/32` without integrating an unavailable negative residence moment of order exactly `1/32`.

The whole-segment trace inequality

```text
T_sigma ell_sigma <= U_sigma + C ell_sigma^(5/8) V_sigma
```

uses the complete angular density and the triangular factor obtained by integrating over starting roofs. The proof does not set an inverse physical Jacobian to one and does not impose a positive residence, gradient, or incidence cutoff.

### 6.3. Complete finite-count sum

The Borel segment parametrization counts physical interiors once. Summing the `U_sigma` terms in one residence band is bounded by the actual collision volume with residence at most the upper edge of that band. The capped finite-count short-residence input is inserted before the infinite dyadic sum and before the collision limit.

The resulting remainder

```text
C_B (1+B|J|) m^3 rho_B^(15m/32)
```

is summable at fixed auxiliary band and vanishes in the required collision limsup. No sum of already-taken limsups is used.

The variation term has exponent

```text
5/8 - 1/32 = 19/32,
```

which is also correct.

### 6.4. Exact conclusion

The theorem yields a critical weak bound on a fixed interval. It does not yield fixed-interval convergence of the short surface as the outer width tends to zero. The printed bound retains a term proportional to the fixed interval length.

The corollary becomes `O(r)` only when the tested interval length is also chosen as `L=r`. That is a useful scale-compatible statement, but it is not a fixed-window endpoint limit and not an essential-height estimate. The manuscript states this accurately.

## 7. Module 209: critical raw-density bound

The proposition bounding the raw density at the critical exponent uses the original source comparison at auxiliary guard parameter one. Since the initial incidence cosine is at most one, the first guard factor vanishes and `W^1=1`; therefore `b^1=p` is the original density rather than a selected subsource.

The three positive terms on the comparison's right-hand side are treated in three distinct topologies:

- the average `A_r p` by the retained fixed-width essential-height input;
- the complete surface by the new critical measurable-set estimate; and
- the fractional potential by an actual `L^Q` Minkowski bound, valid because `kappa Q<1`.

This gives boundedness of the original raw density in the critical weak norm. The analogous error bound uses one fixed outer reconstruction band and the positive scalar remainder. No division by an arithmetic Gaussian reference is used.

I find this step internally coherent, subject to the inherited positive remainder and source-shift inputs.

## 8. Endpoint interpolation and logarithmic convergence

The interpolation lemma starts from

```text
N_Q(f;J) <= A
```

and the normalized mass ratio

```text
t = ||f||_1 / (A L^gamma).
```

Testing the critical norm on the whole interval gives `0<=t<=1`. Splitting measurable test sets at

```text
delta = L t^(1/(2gamma))
```

produces the two terms

```text
A t^(1/2)
```

and

```text
A (1 + log(1/t)/(2gamma))^(-sigma).
```

The calculation is correct and is applied to each finite-count error before any parameter supremum or collision limit. Uniform local `L^1` convergence then gives convergence in the logarithmically weakened critical norm for every `sigma>0`.

This is a genuine endpoint result. It is, however, endpoint convergence in the explicitly weaker norm

```text
sup_E |E|^(-gamma) integral_E |f|
      / (1+log(L/|E|))^sigma.
```

The logarithmic denominator is mathematically significant. It cannot be omitted from theorem statements or summaries.

## 9. The original exceptional union

Revision 89 estimates the actual weighted source

```text
R_h^epsilon
 = integral W^epsilon 1_{z<h^(1/8) or ell<h^(1/4)} dmu_t.
```

This is the original union, not a common-survivor source, a boundary collar, a protected word, or a sum in which the intersection is counted twice.

The critical-initial part is dominated by the inherited fractional source, and the short-residence part by the complete residence cap. The resulting interval mass is

```text
O(h^(1/128)).
```

Since `R_h^epsilon <= p`, the uniform critical weak bound for `p` supplies the endpoint bound needed by the interpolation lemma. The theorem therefore gives

```text
N_{Q,sigma}(m^2 R_h^epsilon;J)
 <= C (1+|log h|)^(-sigma)
```

in the ordered collision limsup.

This directly answers an important part of the parallel main-v88 report: the new mechanism acts on the original exceptional source itself, not only on its regular complement.

It still does not prove that source's essential height tends to zero. The cofinal essential-height charge is unchanged and remains the missing scalar endpoint.

## 10. Module 210: the complete diffusive window

The central roof interval has length of order `sqrt(m)`. Revision 89 correctly does not infer an unnormalized growing-window theorem from a fixed-length local theorem.

Partitioning the roof interval into `N=O(sqrt(m))` pieces gives

```text
integral_K |f|^p <= N d_m^p
```

and

```text
N_Q(f;K) <= A_m N^(31/32).
```

Under the coordinate change

```text
t = m bar(tau_R) + sqrt(m) u,
```

the `p`th-power integral acquires the factor `m^(-1/2)`, while the critical norm acquires the factor

```text
m^(-31/64).
```

These factors exactly cancel the growth of the number of local intervals at their respective exponents. The stated theorem on the fixed diffusive interval `u in [-M,M]` follows.

The result is naturally expressed with the roof measure `dt/sqrt(m)`. It is not an unnormalized `dt` theorem. The article, response, and proof ledger all preserve this distinction.

## 11. Relation to the two revision-88 reports

The controlling weak-Lp report identified three immediate issues:

1. the excluded endpoint `q=32/31`;
2. the absence of a full central-window theorem; and
3. the continuing difference between finite local norms and pointwise essential height.

Revision 89 resolves the first at the level of boundedness, proves convergence with every positive logarithmic loss, and resolves the second in the correctly normalized diffusive roof measure. It does not resolve the third.

The parallel main-v88 report requested a mechanism acting on the original exceptional source and ultimately proving its essential-height charge zero. Revision 89 supplies the former: the logarithmic critical estimate is genuinely on the original exceptional union. It does not supply the latter.

The response also corrects two factual points in the main-v88 report concerning the revision-87 tree and the ordering of powers of `h`. These corrections improve source accuracy but do not change the mathematical recommendation, because neither correction proves the residual charge zero.

## 12. Why the critical endpoint is not the pointwise endpoint

The phrase "critical endpoint" is used in two different senses in this project and they must not be conflated.

The distributional endpoint is the exponent `Q=32/31` dictated by the available short-residence power `1/32`. Revision 89 reaches boundedness at that exponent and logarithmically weakened convergence.

The governing pointwise endpoint is `L^infinity` in the roof variable after collision normalization. It is represented by the zero essential-height charge of the original source.

There is no interpolation from a finite `Q` bound and small mass to `L^infinity` without additional regularity. Even convergence in every finite `L^p`, or in unweakened weak `L^Q`, does not exclude narrow spikes. Therefore removing the logarithmic loss would be worthwhile but would still not, by itself, prove the principal theorem.

A successful closure must add a genuinely source-specific anti-concentration mechanism. Plausible forms include a collision-uniform oscillation estimate, a variation or Sobolev control at the correct microscopic scale, a reverse-Hölder/self-improvement statement, a maximal-function estimate with scale gain, or a geometric persistence theorem showing that a high roof value forces a quantitatively large roof interval of comparable height. The present distributional statements do not contain such a conclusion.

## 13. Inherited proof burden

The focused article is short, but its proof depends on a 720-page supplement and 207 inherited modules. The new source helpfully restates the principal inherited inputs in the journal article, including:

- the stopped physical coarea flow;
- exact source comparison;
- marked section and guard estimates;
- actual fractional source bounds;
- the positive scalar remainder;
- maximal-segment density and angular variation;
- finite-count exit mass;
- long-residence essential-height decay; and
- the Borel kernel convention.

This is much better than referring only to opaque historical module numbers. Nevertheless, source preservation and repeated internal reviews do not substitute for independent verification of those continuum inputs.

The load-bearing points for a specialist audit remain:

1. the exact coarea Jacobian and stopping convention;
2. the one-to-one maximal-segment parametrization with incident components;
3. the angular density derivative bound through all exact labels;
4. the finite-count physical short-residence cap;
5. the four-record spectral and positive-remainder theorem;
6. the common-kernel disintegrations and parameter-dependent null sets; and
7. the source-shift inequality on the original guard.

I found no new contradiction at the revision-89 interfaces, but I do not regard the complete inherited chain as independently certified.

## 14. Significance and architecture

The new endpoint distribution theorem is mathematically nontrivial. The combination of a complete physical residence distribution, a whole-segment trace, an endpoint measurable-set estimate, and an exact-label raw-density consequence is likely of interest in singular hyperbolic dynamics and geometric local-limit theory.

The current submission, however, continues to present the unrestricted pointwise raw local limit as its organizing theorem. That theorem remains open after 210 modules. The strongest unconditional new conclusions are finite-norm and logarithmically weakened distribution statements.

At a strong specialist journal, a focused paper centered on the critical surface distribution theorem, exact-label finite-norm local limits, and the normalized diffusive-window result could merit serious consideration after independent proof audit and substantial compression. That editorial route would require the title, abstract, introduction, theorem hierarchy, and claims to be aligned with the proved topology.

At the requested four-journal benchmark, retaining the pointwise theorem as the principal claim while leaving its exact essential-height obstruction open is not acceptable.

## 15. Required mathematical changes before another top-four review

A further top-four revision should address the following points.

### 15.1. Prove the original essential-height charge zero

The primary requirement is

```text
lim_{B->infinity} R_{epsilon(B),M} = 0
```

for the original weighted exceptional source in the exact order of limits used by the scalar decomposition. A finite `L^p`, Lorentz, logarithmic, or mass estimate is not enough.

### 15.2. Supply an anti-concentration mechanism

The proof must show that a high value of the original roof density cannot be supported on an arbitrarily small roof set. The mechanism must act before the collision limsup and remain uniform in radius, exact labels, arithmetic peak class, and the outer reconstruction parameters.

### 15.3. Keep the original source and exact event

A successful estimate must apply to the original source `R_h^epsilon` or an exactly equivalent source-level object. It must not replace the event by pooled labels, a common-survivor subsource, a protected symbolic word, an averaged density, or a fixed-cutoff theorem whose constants deteriorate before the cutoff is removed.

### 15.4. Distinguish the remaining two endpoints

The paper should continue to distinguish:

- unweakened convergence in the finite critical weak norm; and
- essential-supremum convergence.

The first does not imply the second. A future response should not identify removal of the logarithmic loss with completion of the pointwise LLT unless an additional regularity theorem is also proved.

### 15.5. Complete exact-SHA qualification

Before relying on execution evidence, both revision-89 workflows should complete successfully at the reviewed SHA. Any later source change requires new runs and a new source freeze.

### 15.6. Obtain independent specialist review

The coarea, Borel-segment, optical trace, finite-count cap, and spectral remainder chain should be reviewed by experts in dispersing billiards, geometric measure theory, and anisotropic transfer operators. The current AI-assisted report and repository diagnostics are not substitutes for that audit.

### 15.7. Rationalize the submission architecture

If the pointwise theorem is completed, the journal article should provide a navigable dependency map from that theorem to a reasonably bounded set of principal propositions, with the historical development separated from the proof actually required for publication.

If the pointwise theorem is not completed, the unconditional finite-norm theorem should be submitted as a clearly focused result rather than embedded in a manuscript whose governing claim remains false as a status assertion.

## 16. Editorial comments

1. The abstract is accurate in stating that the residual essential-height charge is not inferred to vanish. This sentence must remain.
2. Every statement of the full-window theorem should display `dt/sqrt(m)` or its equivalent rescaled-coordinate formulation.
3. Every endpoint convergence statement should display the positive logarithmic loss.
4. The critical exponent `32/31` should continue to be described as arising from the available residence exponent, not as a proved optimal physical exponent.
5. The two revision-88 variants should remain separately identified in all manifests and provenance records.
6. Workflow status should be reported as queued until GitHub records a completed conclusion.
7. The focused article should state prominently that only six core files are loaded directly and that the complete preceding proof is imported through the supplement.
8. The theorem names should distinguish "critical weak boundedness" from "critical convergence" and from "pointwise closure."
9. No downstream denominator, same-roof ratio, bridge, or likelihood theorem should be promoted without the scalar pointwise denominator and the retained positive-arithmetic hypotheses.
10. The example of shrinking spikes, or an equivalent warning, would help readers understand why the final concentration problem is genuinely different from the new finite-norm theorems.

## 17. Final assessment

Revision 89 is a serious mathematical response to the two revision-88 reports. It reaches the critical weak exponent by a new finite-count capped distribution argument, establishes logarithmically weakened endpoint convergence, acts directly on the original exceptional union, and supplies correctly normalized full diffusive-window limits. I found no decisive error in those three new modules.

The manuscript is also commendably explicit about what remains open. Its proof ledger, publication status, source manifest, abstract, and final section all state that:

- unweakened critical weak convergence is not proved;
- the original pointwise raw return LLT is not proved;
- the exceptional-source essential-height charge is not proved zero;
- unnormalized growing-window convergence is not proved; and
- unconditional point-conditioned downstream laws are not promoted.

Those limitations are decisive at the requested venue level. The pointwise theorem is the governing assertion of the paper, and its exact concentration charge remains unresolved.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

This recommendation does not deny the value of the new critical distribution theorem. Subject to independent verification, that theorem and the associated exact-label finite-norm local limits may support a strong focused paper. They do not yet support acceptance of the present manuscript as a completed pointwise raw local-limit theorem.