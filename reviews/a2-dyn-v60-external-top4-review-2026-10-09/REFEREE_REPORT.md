# External top-four referee report on A2-DYN revision 60

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v60-referee-response-2026-10-09`, `revision/a2-dyn-v60-referee-copy-2026-10-09`  
**Reviewed commit:** `5559cde546c7e3925dfa8706ee499eef93f813f1`  
**Reviewed repository tree:** `be6027a9d69154cf48863a49d1a1f0e85ffd9165`  
**Ordinary source payload tree:** `5f4d746ee936b176184e0921befaeb35c48db3b8`  
**Active manuscript directory:** `papers/A2-DYN-v60-referee-response`  
**Active mathematical source:** one hundred thirty numbered core modules; revision 60 retains all one hundred twenty-seven revision-59 modules and adds modules 128--130  
**Frozen revision-59 author baseline:** `69ab2afcceff0a8a2892910b335ac180678b5f4b`  
**Frozen revision-59 complete paper tree:** `7ca1775bcf25516a93fea04e834da38652f75687`  
**Controlling external report:** `reviews/a2-dyn-v59-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `546a82be685897355e4918598f2d06847aa9f69c` / `72cc0cbaeafba69f070740ea5311c34148a12e59`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 60 is a genuine theorem-bearing advance over revision 59. The preceding report accepted the correlated Markov baker realization, its continuous deterministic roof, its unperturbed pointwise density theorem, and its direct positive boundary-height estimates. It nevertheless emphasized a precise separation: the moving damped spectral peak was proved for a nonzero perturbation family, whereas pointwise inversion and positive heights were proved only at the unperturbed parameter.

Revision 60 closes that separation in the model.

The new source keeps the two integer Markov counts before scalar projection, proves a joint exact-state lattice local limit and a positive tilted Gaussian coefficient bound, obtains labelled stable-cylinder estimates, and evaluates the exact coarea density uniformly for every fixed compact perturbation interval

```text
|epsilon| <= epsilon_0 < 1/4.
```

It proves

```text
ess sup_t |sqrt(m) p_{m,epsilon}(t)
             - g_{sigma_epsilon^2}((t-m bar_tau_epsilon)/sqrt(m))|
    <= C log(2+m)^(3/2) / sqrt(m),
```

with the correct mean and variance, and it retains an explicit arithmetic profile for weighted endpoints. It also proves the three original positive boundary-source height bounds uniformly on this same perturbed family. Finally, at the critical scale `epsilon=c_m/sqrt(m)`, it evaluates a fixed physical witness density whose damping is

```text
exp(-12 pi^2 c_m^2 / 119),
```

matching the independently computed pressure-peak damping.

The manuscript additionally isolates a positive exact-label coarea criterion. This criterion correctly states that small source mass is not enough: one needs a wordwise nondegenerate derivative and a positive local bound after the relevant exact labels or cylinders have been fixed.

I audited the new modules

- `core/128_positive_coarea_criterion.tex`;
- `core/129_perturbed_markov_density.tex`;
- `core/130_perturbed_heights_and_contact.tex`;

and their use in the revised front matter. I also checked the relevant inherited definitions of the correlated Markov baker, its invariant measure, the stable endpoint recurrence, the pressure branch, the unperturbed coarea theorem, and the source-height sets.

I found no decisive counterexample, missing coarea Jacobian, wrong stationary factor, false lattice-span assumption, covariance error, conditional-Gaussian error, endpoint-indexing error, invalid summation of a signed local-limit error, or mismatch between the critical density damping and the pressure damping in the new chain.

In particular, the following points are internally coherent.

1. The two count means are `(3/7,2/7)` and the asymptotic covariance is

   ```text
   (1/343) [[204,192],[192,198]].
   ```

2. The full two-dimensional lattice is aperiodic even with specified endpoint states.
3. The positive exact-count envelope comes from a real tilt of a positive matrix and not from subtracting a signed Gaussian approximation.
4. The scalar strip bound is obtained only after the full two-count envelope is proved; no rationality or Diophantine condition on `epsilon` is used.
5. Stable-cylinder errors are summed with transition weights rather than with the exponentially large number of words.
6. The coarea derivative is exactly `1-a_w` and is bounded away from zero uniformly in the word and perturbation.
7. Gaussian tails in the second count are removed before the local-limit errors are summed.
8. The unweighted scalar projection is evaluated by a mesh Riemann sum and gives variance

   ```text
   sigma_epsilon^2=(204+384 epsilon+198 epsilon^2)/343.
   ```

9. The three positive source heights are proved from positive coefficient estimates, not from source mass, weak integrability, or deletion of an exceptional roof set.
10. The conditional constants `16/17` and `6/119` and the damping `12 pi^2/119` agree.

These are meaningful achievements. Revision 60 is substantially stronger than revision 59 and directly answers the most important model-level criticism in the controlling report.

The negative top-four recommendation is nevertheless still forced by the manuscript's principal mathematical object. Revision 60 explicitly does **not** prove either of the two missing Lorentz essential-height estimates. It therefore does not prove the unrestricted two-sided pointwise arithmetic raw-density theorem for the original four-coordinate actual-return record.

The new coarea criterion identifies sufficient inputs, but the hard Lorentz work is precisely to verify those inputs while retaining

- the exact return index;
- exact displacement and collision labels;
- the first physical incidence defect;
- the next-collision competing-hit clearance convention;
- grazing and singularity geometry;
- and the complete positive first-defect source.

None of those verifications is supplied by the Markov calculation. The manuscript is transparent about this distinction, but it remains decisive for the requested venue.

The breadth route also remains incomplete. The criterion is verified in one explicitly coded correlated Markov baker family. It is not verified in multiple genuinely different non-Markov singular-hyperbolic systems, and its assumptions already encode the principal density-level difficulty. The finite-state Markov additive local limit and compact-family variants are classical; the new exact coarea and height calculation is useful, but not by itself a top-four general theorem.

At the requested benchmark, the article would need either

1. completion of the Lorentz incidence and clearance height estimates and hence of the unrestricted pointwise theorem which governs the title and much of the one-hundred-thirty-module architecture; or
2. a substantially broader source-height theorem whose hypotheses are independently verifiable in several genuinely different singular systems and whose significance does not depend on the unfinished Lorentz endpoint.

Revision 60 supplies neither endpoint yet. No independent human specialist audit has been obtained.

My mathematical assessment is therefore positive about the new modules and the direction of the program, but negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`5559cde546c7e3925dfa8706ee499eef93f813f1`.

The repository tree is

`be6027a9d69154cf48863a49d1a1f0e85ffd9165`.

The active article is

`papers/A2-DYN-v60-referee-response`.

The ordinary source payload tree recorded in the manifest is

`5f4d746ee936b176184e0921befaeb35c48db3b8`.

The author commit has the revision-59 external-report commit

`546a82be685897355e4918598f2d06847aa9f69c`

as its parent. The chronology is correct: revision 60 begins from the frozen external assessment and preserves the reviewed revision-59 source.

The source manifest records:

- all one hundred twenty-seven inherited core files retained byte-for-byte;
- all one hundred seventy-one inherited Python files retained byte-for-byte;
- all inherited compiled appendices retained;
- all one thousand seven hundred thirteen inherited mathematical labels retained;
- an append-only bibliography change;
- three new modules, 128--130;
- `positive_labelled_coarea_criterion_proved: true`;
- `uniform_perturbed_markov_density_proved: true`;
- `uniform_perturbed_markov_height_proved: true`;
- `critical_density_pressure_contact_proved: true`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false` for the Lorentz record;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `arithmetic_factor_identically_one_proved: false`;
- `multiple_nonmarkov_height_realizations_proved: false`;
- and `independent_human_review: false`.

These flags accurately describe the scope. The pointwise and height theorems in revision 60 concern the original correlated Markov roof family, not the Lorentz incidence or clearance densities.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v60-external-top4-review-2026-10-09/`.

No author manuscript source, prior review, workflow, historical manuscript or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA qualification workflows completed successfully on both reviewed author refs:

- response branch run `37944743670`;
- referee-copy branch run `37944762589`.

The runs bind the source archive, finite diagnostics, native build and theorem-page renders to the reviewed SHA.

According to the validation record, the verifier checks

- the frozen revision-59 complete paper tree;
- the controlling revision-59 report blob;
- one hundred twenty-seven unchanged inherited core files;
- one hundred seventy-one unchanged inherited Python files;
- all one hundred thirty core inclusions;
- all inherited compiled appendices and mathematical labels;
- thirteen provenance copies;
- the append-only bibliography;
- the ordinary Git payload identity;
- the read-only workflow hash;
- agreement of ordinary and optimized finite diagnostics;
- native TeX compilation; and
- theorem-label-based rendering.

The new finite regressions include exact joint reward recursions, Fourier matrix pairings, complete-word coarea checks, boundary-source mass checks, fixed-witness pressure pairings and independent Gaussian-profile quadratures. Negative controls retain a lost second count, an omitted coarea Jacobian and erased endpoint arithmetic as failures.

These are useful source, algebra and bookkeeping checks. They do not certify

- the inherited Lorentz occupation operator on anisotropic spaces;
- physical peripheral representations and branch visibility;
- resonant Hessian contact through arithmetic transitions;
- the Lorentz first-physical-defect decomposition;
- incidence and clearance multiplier geometry;
- the complete local raw variation theorem;
- the graph-coupled return clock;
- the continuum Markov coarea asymptotics uniformly in every word;
- or either missing Lorentz essential-height estimate.

The manuscript and its validation files state these limitations correctly.

## 4. Scope of this review

I did not attempt to re-prove all one hundred thirty core modules. The substantive audit concentrates on the new modules and the inherited inputs immediately used by them:

1. the exact-label positive coarea proposition;
2. the two sufficient height mechanisms and their quantifiers;
3. preservation of the correlated Markov baker measure;
4. the two-count mean and covariance;
5. full two-torus aperiodicity, including specified endpoint states;
6. the joint exact-state local limit;
7. the positive tilted coefficient envelope;
8. strip anti-concentration after scalar projection;
9. suffix rewards and stable-cylinder lengths;
10. the use of detailed balance at the joining state;
11. the exact perturbed coarea identity;
12. the Gaussian-tail truncation before summing local errors;
13. the weighted arithmetic profile;
14. the unweighted triangle periodization and Riemann sum;
15. the vertical, terminal-stable and initial-age positive heights;
16. the same-roof conditional source estimate;
17. the critical-scale profile;
18. the comparison with the pressure damping;
19. source preservation and qualification evidence;
20. the relation of the model mechanism to the missing Lorentz heights; and
21. top-four significance and architecture.

The inherited revision-59 and earlier Lorentz continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 5. The positive exact-label coarea criterion

Module 128 starts from a disintegration into words `w`, with positive masses `c_w`, a scalar coordinate `y`, bounded conditional densities, and a monotone observation

```text
T_w(y)=ell_lambda(q_w)+u_w(y),
|u_w|<=H,
|u_w'|>=eta>0.
```

For almost every target roof, the word contributes

```text
c_w r_w(y_w(t)) / |u_w'(y_w(t))|.
```

This is the correct one-dimensional coarea formula. Positivity and Tonelli permit the word contributions to be summed without cancellation. The conclusion keeps every further exact label `q_w` and the auxiliary label `iota`.

The first sufficient mechanism uses a cylinder cover. It correctly requires not only small total cylinder mass, but also a residual local constraint after each cylinder has been fixed:

```text
sum_{w subset C, |ell(q_w)-t|<=H} c_w
       <= K a_m c(C).
```

Summing over an overlapping cover is legitimate because the proof uses it only as a positive upper cover and assumes the sum of the cylinder masses is already bounded.

The second mechanism uses an endpoint statistic `b_w`. Its hypotheses correctly combine

- an exact-label interval envelope at each `q`; and
- a summable projected envelope over labels capable of meeting the same roof.

The conclusion for a union of at most `K` intervals pays both their total length and the finite number of interval errors. Bounded source insertions are controlled by domination before pushforward.

I find this proposition correct as stated.

Its limitation is equally important. It is a sufficient bookkeeping/coarea theorem. It does not produce the wordwise derivative, cylinder-conditioned local estimate, endpoint interval estimate or projected summability. In the Lorentz application those are the hard geometric and dynamical statements. The proposition should therefore not be presented as closing the physical source-height problem by abstraction alone.

## 6. The two-count Markov record

The new record is

```text
A_m=sum_{r=1}^m I_r,
B_m=sum_{r=1}^m I_{r-1} I_r.
```

For the transition matrix

```text
P=[[3/4,1/4],[1/3,2/3]],
pi=(4/7,3/7),
```

stationarity gives

```text
E A_m/m = 3/7,
E B_m/m = 2/7.
```

Differentiating the Perron root gives

```text
Sigma_*=(1/343)[[204,192],[192,198]].
```

The determinant is positive. The projected variance for `A+epsilon B` is therefore

```text
(204+384 epsilon+198 epsilon^2)/343,
```

which remains uniformly positive on every fixed `|epsilon|<=epsilon_0<1/4`.

The torus phase argument is complete. A unit-modulus eigenvalue forces equality on every positive edge. The `00` loop fixes the eigenvalue, the `10` edge equates the state phases, the `01` edge fixes the first frequency and the `11` loop fixes the second. Thus there is no nonzero peripheral point on the two-torus.

This is the correct arithmetic object to retain before projecting onto `A+epsilon B`. It avoids the false requirement that all scalar projections share one lattice span.

## 7. The joint exact-state local limit

The near-zero Fourier expansion has a simple eigenvalue with Hessian `Sigma_*`, while the complementary spectrum is uniformly separated. In two dimensions the projection error and the cubic logarithmic error integrate to order `m^(-3/2)` in the unscaled probability. Multiplication by `m` gives the printed uniform `O(m^(-1/2))` exact-state error.

The argument is uniform in the lattice target because the inverse Fourier phase has modulus one. Endpoint-state normalization is `pi_j`, as required.

No Edgeworth coefficient is claimed, and no local error is used to prove a positive upper bound. I find the scaling and normalization consistent.

A specialist should nevertheless check the exact matrix convention against the coded transition orientation, because the reward is attached to the arrival state and to the ordered edge. The manuscript's physical pairing and finite recursions are consistent with that convention, but this is a load-bearing indexing point.

## 8. The positive tilted coefficient envelope

For the positive upper bound, the manuscript uses the matrix at a small real tilt and its Perron root `C(theta)`. The corresponding Doob transform keeps the same four positive edges. Hence the only unit-modulus frequency remains zero, uniformly on a sufficiently small compact tilt ball.

The Fourier integral then contributes the correct two-dimensional factor `m^(-1)`. Choosing

```text
theta=a(q-m mu_*)/m
```

is legitimate for every feasible count when `a` is fixed sufficiently small. The quadratic pressure inequality gives

```text
Pr_i(Q_m=q,I_m=j)
 <= C m^(-1) exp(-c |q-m mu_*|^2/m).
```

This is a positive coefficient estimate and does not inherit the sign or error of the local limit theorem.

The proof is concise but structurally sound. The points requiring specialist verification are uniform control of the Doob conjugating factors and the compact nonzero-frequency gap throughout the chosen tilt ball.

## 9. Projected strip anti-concentration

At a fixed second count `B_m=l`, the condition

```text
|A_m+epsilon l-t|<=H
```

allows only a bounded number of integer values of `A_m`, independently of the rationality of `epsilon`. Summing the positive joint Gaussian envelope in `l` gives a factor of order `sqrt(m)`, which combines with `m^(-1)` to give

```text
C_H m^(-1/2).
```

This is the correct one-dimensional density scale after projection. It is also exactly the residual local input required after a prefix or suffix cylinder is fixed in the height proof.

## 10. Labelled stable-cylinder estimates

The suffix argument keeps the exact two-count suffix reward. If the joining state is `i` and the terminal state is `j`, the full probability factors as

```text
Pr_pi(Q_{m-L}=q-q_w,I_{m-L}=i) P(w).
```

Detailed balance converts `pi_i P(w)` into the stationary mass of the terminal stable cylinder. The local-limit errors are multiplied by `P(w)` and summed; they are not multiplied by the number of suffix words. This is essential and is handled correctly.

The shift from the prefix center to the full-time center costs `O((1+L)/sqrt(m))` after normalization. The positive upper bound requires `L<=sqrt(m)` so that the suffix reward displacement can be absorbed into the Gaussian exponent. The manuscript retains this restriction.

Inner and outer interval covers use only finitely many boundary cylinders per terminal state, each of length at most `rho_0^L`. The endpoint conventions therefore have no effect on the estimate.

I find no missing exponential word factor in this calculation.

The exact joining-state reward convention, the orientation of the stable cylinder and the detailed-balance identity should nevertheless receive independent checking because an off-by-one reward would affect both the count and the endpoint interval.

## 11. The exact perturbed coarea identity

On a complete word,

```text
y_m=b_w+a_w y_0,
S_m tau_epsilon=3m+A_m+epsilon B_m+b_w-(1-a_w)y_0.
```

Solving for `y_0` gives the exact density factor `(1-a_w)^(-1)` and support interval

```text
[b_w+a_w-1,b_w].
```

Since `0<a_w<=rho_0^m`, the derivative is bounded below by `1-rho_0`. The perturbation changes only the integer reward, not this derivative.

The endpoint insertions are evaluated at the actual solved values of `y_0` and `y_m`. The formula uses conditional uniformity of `y_0` on a word and introduces no independent smoothing variable.

The normalization is correct: integrating the word densities gives the original word masses and summing gives one in the unweighted case.

## 12. The weighted arithmetic profile

For fixed second count `l`, the first count is summed through the one-periodic endpoint overlap `Theta_{f,d}`. The resulting reference is

```text
R_{m,epsilon}^{f,d}(t)
 = m^(-1/2) sum_l
   g_{Sigma_*}((r-epsilon l-3m/7)/sqrt(m),
               (l-2m/7)/sqrt(m))
   Theta_{f,d}(r-epsilon l).
```

This expression retains the projected arithmetic for rational, irrational and count-dependent perturbations. It is not replaced by a product of endpoint means.

For `f=d=1`, the triangle-periodization identity makes `Theta` exactly one. For general bounded Lipschitz endpoints, the overlap has a uniform bounded-variation norm and the stable-cylinder discrepancy can be integrated against it.

This is the correct distinction between the unweighted scalar density and the weighted arithmetic profile.

## 13. Summing the local errors

A naive sum of the uniform joint local-limit error over all possible second counts would be too large. Revision 60 explicitly avoids that mistake.

It first restricts to

```text
|l-2m/7| <= K sqrt(m log(2+m)).
```

For each retained `l`, only a bounded number of first counts can meet the coarea support. The omitted positive source and omitted Gaussian reference are controlled by the positive joint envelope, with `K` chosen so that the normalized tail is negligible.

The number of retained pairs is `O(sqrt(m log m))`. Each pair has normalized error of order `log(m)/m` after conversion from the two-dimensional probability scale to the scalar density scale. Their sum is therefore

```text
O(log(m)^(3/2)/sqrt(m)).
```

The exponent and count are consistent.

The replacement of the integer first count by the real coarea center costs another `O(m^(-1/2))` after summing a Gaussian derivative. I find no missing factor of `sqrt(m)` in this step.

## 14. The unweighted Gaussian projection

With

```text
z=(t-m bar_tau_epsilon)/sqrt(m),
y_l=(l-2m/7)/sqrt(m),
```

the remaining profile is the mesh Riemann sum of

```text
F_{epsilon,z}(y)=g_{Sigma_*}(z-epsilon y,y).
```

Its integral is the one-dimensional Gaussian with variance

```text
sigma_epsilon^2=(1,epsilon) Sigma_* (1,epsilon)^T.
```

The total variation in the `y` variable is uniformly bounded after the polynomial factor is absorbed by the Gaussian. The elementary interval-by-interval Riemann estimate therefore costs `O(m^(-1/2))`, uniformly in `z` and in the compact perturbation interval.

This proves the unweighted pointwise local limit without selecting a scalar arithmetic regime.

## 15. The three positive boundary heights

The vertical source is covered by forward cylinders of depth `floor(m/2)`. Their total stationary mass is `O(s+rho_0^L)`. After a prefix is fixed, the remaining projected reward has strip probability `O(m^(-1/2))`. This verifies the cylinder version of the positive coarea criterion.

The terminal stable source is covered by suffix cylinders. The prefix exact-count estimate is conditioned on the suffix joining state, and detailed balance converts the suffix transition product into the actual stable-cylinder mass. Again the residual strip probability is `O(m^(-1/2))`.

For the initial-age source, the coarea equation gives two separate endpoint intervals. Both are retained:

```text
y_0<s     implies b_m in [delta,delta+s],
y_0>1-s   implies b_m in [delta+1-s-rho_0^m,delta+1].
```

The positive labelled stable-cylinder envelope at depth

```text
L_m=min(floor(m/2),floor(sqrt(m)))
```

supplies the endpoint version of the criterion. Summing the exact two-count Gaussian envelope gives the required `m^(-1/2)` scale.

The resulting bound

```text
sqrt(m) (||p_vert||_infty+||p_stab||_infty+||p_age||_infty)
 <= C(s+rho_0^L_m)
```

is a genuine essential-height estimate. It is not inferred from the masses of the strips.

## 16. Same-roof conditional source probabilities

The unweighted pointwise theorem gives a uniform lower bound of order `m^(-1/2)` on every fixed central compact set. Dividing the positive boundary-source heights by this same-roof denominator gives a conditional source probability of order

```text
s+rho_0^L_m
```

for almost every central roof.

This division is legitimate because both numerator and denominator concern the unchanged original Markov roof and the same perturbation. No exceptional set of positive Lebesgue measure is removed.

The result remains an almost-everywhere statement, as regular conditional probabilities at exact continuous roof values are defined only up to null sets.

## 17. The critical moving profile

At the critical scale

```text
epsilon=c_m/sqrt(m),
```

the weighted arithmetic profile becomes a Riemann sum with the endpoint factor evaluated at `r_epsilon-c_m y`.

The conditional law of the second Gaussian coordinate given the first has

```text
mean=(16/17) z,
variance=6/119.
```

These constants follow from the displayed covariance matrix:

```text
(192/343)/(204/343)=16/17,
198/343-(192/343)^2/(204/343)=6/119.
```

For the fixed witnesses

```text
f(y)=exp(2 pi i y),
d(y)=exp(-2 pi i y),
```

the overlap is `exp(-2 pi i r)`. Its conditional Gaussian transform is therefore

```text
exp(-2 pi i(r_epsilon-(16/17)c_m z))
exp(-12 pi^2 c_m^2/119).
```

This agrees with the pressure damping because

```text
m kappa_epsilon=(12 pi^2/119)c_m^2+O(m^(-1/2))
```

for bounded `c_m`.

I find the conditional-Gaussian computation and the damping coefficient correct.

## 18. What revision 60 closes

Relative to revision 59, the new manuscript closes the following points.

- Moving pressure contact, pointwise density inversion and positive source heights now coexist on the same nonzero perturbation family.
- The scalar arithmetic transition is handled by retaining two integer counts before projection.
- The exact-state local law includes terminal-state normalization.
- A positive tilted coefficient estimate supplies Gaussian tails independently of the signed local-limit error.
- Stable-cylinder estimates retain exact two-count labels.
- The weighted endpoint theorem preserves the projected arithmetic profile.
- All three original model boundary sources have direct essential-height bounds uniformly in the perturbation.
- The critical physical witness density reproduces the pressure damping coefficient.
- A separate proposition records the exact-label coarea hypotheses needed by future source-height arguments.

These are mathematically substantive improvements.

## 19. What revision 60 does not close

The principal Lorentz endpoint remains open.

The manuscript has not proved

```text
lim_{B->infinity} limsup_{m->infinity}
 sup_{R,n,k} ess sup_{central u}
 m^2 b_{n,k,m,R}^{epsilon(B),inc,1}(u)=0,
```

or the analogous estimate for the complete next-collision clearance source.

Consequently it has not proved

- the unrestricted two-sided pointwise arithmetic raw-density theorem for the Lorentz return record;
- the unrestricted pointwise roof-density LLT;
- unrestricted same-roof collision and return bridges;
- forward essential likelihood convergence;
- a pointwise roof-conditioned path theorem at every positive-reference roof;
- a constant arithmetic factor on all classes;
- or an independent proof certificate for the inherited Lorentz continuum chain.

The source manifest and publication-status file correctly keep these claims false.

## 20. Why the Markov height theorem does not transfer to Lorentz geometry

The Markov calculation has three special structural features.

First, every full word has one globally monotone stable coordinate with derivative `1-a_w` bounded uniformly away from zero.

Second, the exact local constraints are controlled by a finite-state positive transition matrix. After a prefix or suffix is fixed, a uniform positive Gaussian coefficient estimate remains available.

Third, the endpoint geometry is represented by stable intervals whose lengths are exactly related to transition products by detailed balance.

The Lorentz incidence and clearance sources do not presently have these properties in a proved form. Their difficulties include

- grazing derivatives;
- changes of the first physical hit;
- competing collision roots;
- singularity proliferation;
- image-side marking;
- exact return labels;
- and the need to stop rather than continue through a physical seam.

The abstract criterion is useful precisely because it shows what must be proved. It does not prove those hypotheses by analogy.

## 21. Generality and novelty

The two-count projection and exact deterministic endpoint coarea are nontrivial. The uniform passage across rational, irrational and count-dependent scalar arithmetic regimes is a clean feature of the proof. The simultaneous density, height and pressure-contact theorem is stronger than the unperturbed model in revision 59.

Nevertheless, finite-state Markov additive local limits, positive tilted coefficient bounds and compact transition-family variants are established theory. The new criterion is an elementary positive coarea/disintegration statement once its hypotheses are available. Its present verification is in one explicitly coded correlated Markov baker family.

This is valuable model mathematics, but it does not yet constitute a broad theorem at the level expected for the requested four journals.

A stronger generality case would require, for example,

- a source-height theorem for a broad class of singular hyperbolic maps with verifiable geometric hypotheses;
- several genuinely different non-Markov realizations;
- or completion of the Lorentz physical heights, where the criterion's assumptions are genuinely difficult.

The manuscript currently has none of these.

## 22. Architecture and editorial significance

The article now compiles one hundred thirty mathematical modules and a very long historical pipeline. The front matter accurately states three different levels of conclusion:

1. global integrated Lorentz arithmetic laws and coupled bridges;
2. a general pressure-contact principle with model realizations; and
3. a pointwise perturbed Markov density/height theorem.

The title, however, remains centered on raw local inversion in the triangular Lorentz gas, and the unrestricted pointwise Lorentz endpoint remains unproved.

At a specialist-journal level, a focused paper on the pressure-contact principle, the two-count Markov coarea theorem and the positive height criterion could be valuable. The present combined architecture asks the editor and reader to verify an enormous inherited Lorentz chain while the title-level endpoint is still missing.

For a top-four submission, the proof route should be reorganized around one completed principal theorem of commensurate breadth. Preservation of research history in the repository is compatible with a much shorter journal manuscript.

## 23. Independent specialist verification

No independent human specialist audit has been obtained.

For modules 128--130, the highest-priority checks are:

1. the exact disintegration weights and monotone inverse in the coarea criterion;
2. the auxiliary-label quantifiers in both height mechanisms;
3. the full two-torus phase exclusion with specified endpoint states;
4. the uniform tilted Fourier integral and Doob conjugating factors;
5. the feasible-count tilt choice;
6. suffix reward subtraction at the joining state;
7. the detailed-balance stable-cylinder identity;
8. summation of transition weights rather than cylinder counts;
9. the depth restrictions in the positive envelope;
10. both coarea interval inclusions;
11. Gaussian-tail truncation before summing local errors;
12. the exact `1-a_w` denominator;
13. the periodization identity in the first count;
14. the remaining second-count Riemann sum;
15. the prefix-conditioned vertical source;
16. the terminal suffix source;
17. both initial-age intervals;
18. the conditional constants `16/17` and `6/119`; and
19. use of the same fixed physical endpoint witnesses as in the pressure theorem.

The inherited Lorentz audit remains separate and substantially harder. It includes the occupation spectrum, physical peripheral representations, first-defect source partition, grazing and competing-hit geometry, protected critical collars, complete local variation, actual-return clock transfer, and both missing Lorentz height estimates.

Source hashes, finite recursions, exact arithmetic checks and PDF rendering do not replace this audit.

## 24. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 24.1 Prove the Lorentz incidence height

Establish the essential-height estimate for the complete positive incidence source at the original exact labels. The proof must retain the actual first physical hit, grazing geometry, return index, displacement and collision count.

### 24.2 Prove the Lorentz clearance height

Establish the corresponding estimate for the next-collision competing-hit clearance source. Do not continue trajectories through a physical seam or replace the exact word by a nearby regular word.

### 24.3 Complete the unrestricted pointwise theorem

Combine those two positive heights with the already proved positive raw-error representation and canonical arithmetic reference. Keep the finite arithmetic factor unless a separate residue theorem proves it trivial.

### 24.4 Derive the unrestricted pointwise consequences

Only after the height estimates are established should the manuscript assert unrestricted same-roof bridges, forward essential likelihood, or exact-roof path laws.

### 24.5 Verify the coarea criterion in broader systems

If the generality route is pursued instead, prove that the criterion's hypotheses follow from reusable geometric/dynamical assumptions and verify them in several genuinely different non-Markov singular systems.

### 24.6 Obtain independent specialist review

The Lorentz anisotropic operator chain, physical source decomposition, Markov coarea proof and the new exact-label height mechanism all require human expert verification.

### 24.7 Resolve the arithmetic presentation

Either make the finite arithmetic transition kernel and zero classes permanent features of the principal statement, or prove the concrete residue-triviality criterion. Do not present an unmodulated Gaussian as the uniform theorem without that step.

### 24.8 Reduce the journal proof burden

Present the shortest complete route to one principal theorem. Move provenance, validation ledgers, superseded front matter and unfinished alternative endpoints out of the main journal narrative without deleting them from the repository.

### 24.9 Sharpen the literature comparison

State theorem by theorem what is new beyond finite-state Markov additive density theory, classical Lorentz-process local limits, endpoint mixing local limits and suspension-flow local central limit theory.

## 25. Technical and presentation comments

1. Keep the two integer counts visible until after the coarea projection.
2. State explicitly whenever a constant is uniform in a count-dependent `epsilon_m`.
3. Retain `pi_j` in every endpoint-state local limit.
4. Keep the positive tilted coefficient bound separate from the signed local-limit expansion.
5. Do not sum a uniform exact-state error over all second-count labels without first truncating by the positive Gaussian envelope.
6. Keep the restriction `L<=sqrt(m)` in every use of the positive stable-cylinder bound.
7. Distinguish the full-word endpoint `b_m` from the endpoint of a suffix cylinder.
8. Keep the exact suffix reward and joining state in the cylinder factorization.
9. State the coarea denominator `1-a_w` in every density and source formula.
10. Preserve both lower and upper interval inclusions for the coarea support.
11. Keep the weighted arithmetic profile distinct from a product of endpoint means.
12. State that the unweighted triangle-periodization identity is special to `f=d=1`.
13. Preserve the almost-everywhere qualifier for exact-roof conditional probabilities.
14. Do not infer source-height control from source mass or local variation.
15. Keep the Markov height theorem separate from the Lorentz incidence and clearance claims.
16. State that the abstract coarea proposition is sufficient, not necessary, and does not verify its own dynamical inputs.
17. Preserve the dependence of the critical profile on the fractional arithmetic phase `r_epsilon`.
18. Keep the conditional mean coefficient `16/17` and variance `6/119` visible in the pressure comparison.
19. Do not identify the fixed-witness damping with the unweighted endpoint factor.
20. Keep the compact perturbation restriction `epsilon_0<1/4`, which guarantees positivity of the roof.
21. State when `epsilon` is fixed and when it may depend on `m`.
22. Keep probability total variation as one half of variation mass in inherited global statements.
23. Preserve arithmetic zero classes and avoid assigning conditional laws to zero denominators.
24. Do not promote model finite diagnostics to continuum proof evidence.
25. Keep source qualification and independent mathematical verification separate.
26. Make clear that the new rate is for the Markov density, not the Lorentz raw density.
27. Retain the false status of the two Lorentz height flags until the actual physical sources are controlled.
28. Avoid describing one Markov baker family as multiple independent non-Markov realizations.
29. Keep the original exact-return source and next-collision clearance convention visible in every future Lorentz height claim.
30. Consider a separate focused manuscript for the model pressure/coarea theorem if the Lorentz endpoint is not yet ready.

## 26. Final assessment

Revision 60 is a serious and mathematically coherent response to the revision-59 report.

It proves an exact-label positive coarea criterion, retains both integer Markov counts through the arithmetic transition, establishes a joint exact-state local law and a positive Gaussian envelope, derives a uniform pointwise continuous-roof local limit throughout a nonzero perturbation interval, proves three direct positive source-height estimates on that same family, and evaluates a critical fixed-witness density whose damping matches the pressure peak.

The central constants and normalizations are consistent:

```text
mu_*=(3/7,2/7),
Sigma_*=(1/343)[[204,192],[192,198]],
beta_*=16/17,
v_*=6/119,
2 pi^2 v_*=12 pi^2/119.
```

The error summation correctly truncates the second count before adding local errors, and the source-height proof uses positive conditional estimates rather than signed asymptotics. I found no decisive error in modules 128--130.

The advance nevertheless remains a model theorem and an abstract sufficient criterion. It does not prove the two Lorentz physical essential-height estimates. The unrestricted pointwise arithmetic raw-density theorem, unrestricted same-roof consequences and forward essential likelihood therefore remain open for the manuscript's title object.

The article also remains highly model-specific, extraordinarily large and dependent on a continuum Lorentz chain which has not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper built around the pressure-contact principle, the perturbed Markov coarea theorem and the positive exact-label height criterion could be significant if the proof survives expert audit. A future top-four submission should return only after closing the Lorentz incidence and clearance heights or after proving and independently validating a substantially broader source-height theorem.