# External top-four referee report on A2-DYN revision 55

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v55-referee-response-2026-10-09`, `revision/a2-dyn-v55-referee-copy-2026-10-09`  
**Reviewed commit:** `32866de446dd83c3036c04544ce4da66b019a990`  
**Reviewed repository tree:** `13fb49d00e2bc5888fc7d2828b73fda781b8668a`  
**Ordinary source payload tree:** `e3e3d73a2be912424f339fdef250404077ff1785`  
**Active manuscript directory:** `papers/A2-DYN-v55-referee-response`  
**Active mathematical source:** one hundred eighteen numbered core modules; revision 55 retains all one hundred sixteen revision-54 modules and adds modules 117--118  
**Frozen revision-54 author baseline:** `63135318e1eadd80341d4d0656a17e8caba60c90`  
**Frozen revision-54 complete paper tree:** `f5374f17d39e11b8ee489a2ced0818aad12d5a10`  
**Controlling external report:** `reviews/a2-dyn-v54-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `7d4e3f6cafebf96da91d2d3a81147841418d9e61` / `a5fc63527861cda25889357bbdd395b2c1efa57e`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 55 is a genuine theorem-bearing advance over revision 54. It does not merely restate the previously obtained higher-integrability result with a more favorable notation. The new argument removes the dependence of the proved integrability interval on the ratio between a fixed-band spectral decay exponent and the complete exponential density-height exponent. It does so by combining two finite-count estimates for the **same positive source**:

1. a local thin-layer mass bound of the form
   \[
   C(1+h)\bigl(\varepsilon^{1/16}+e^{-\kappa m}\bigr),
   \]
   obtained at one fixed auxiliary roof band; and
2. an exact global source-mass bound of the form
   \[
   C m^2\varepsilon.
   \]

A two-regime argument then removes the exponentially small finite-count term uniformly in both the collision count and the protection scale. Combining the resulting error-free local mass bound with the inherited protected-source height estimate

\[
\|F_\varepsilon\|_\infty\le C\varepsilon^{-9}
\]

gives the explicit density-weighted tail

\[
\int_{\{P>L\}}P\le C L^{-1/144},
\]

and hence the uniform weak endpoint

\[
P=m^2p_{n,R}(k,m,\cdot)\in L^{145/144,\infty}_{\mathrm{loc}}.
\]

The manuscript further derives:

- strong local `L^q` bounds and raw local laws for every
  \[
  1<q<145/144;
  \]
- finite-count `L^q` estimates for the positive incidence and clearance remainders separately;
- logarithmically weakened endpoint Orlicz laws;
- the corresponding bounded-Lipschitz-dual path-valued raw laws;
- forward likelihood convergence in the same explicit power range;
- forward relative-entropy convergence;
- and forward Renyi convergence for every order in the same open interval, under the unchanged pointwise arithmetic reference floor.

I audited the new modules

- `core/117_cap_free_boundary_layers.tex`;
- `core/118_endpoint_raw_laws.tex`;

and their use in the revised front matter. I also checked the precise inherited inputs invoked from modules 115--116, the positive source decomposition, the exact-label disjointness argument, the source normalization, the exponent arithmetic, the endpoint modular, the likelihood normalization, and the qualification records.

I found no decisive counterexample, Fourier-sign error, normalization error, collision/return endpoint mismatch, false arithmetic cancellation, invalid use of a collision-count-dependent frequency band, or illicit inference from a weak endpoint to an essential-supremum theorem in the new text.

The following parts of the new chain are particularly sound.

- The local and global estimates concern the same finite-count positive source and the same protection scale.
- The two-regime lemma is a finite inequality, not a diagonal subsequence argument.
- The global normalized mass factor `m^2` is paid explicitly and is compatible with the disjoint exact labels at fixed collision count.
- The endpoint exponent is correctly computed as
  \[
  \frac{1/16}{9}=\frac1{144}.
  \]
- Weak `L^(145/144)` is kept distinct from strong `L^(145/144)` and from essential boundedness.
- The finite-count physical-remainder estimate has the correct exponent
  \[
  9\left(\frac{145}{144}-q\right).
  \]
- The endpoint modular uses a genuine convex Young-type function with a logarithmically integrable weak-endpoint tail.
- The path-valued extension uses one common roof version and scalar domination, not a null set or source chosen separately for each path test.
- The forward likelihood theorem keeps the pointwise reference floor `G >= d`; it does not replace that condition by positivity of an integrated denominator.
- The arithmetic transition kernel is retained uniformly, and its fixed-radius residue is not silently set equal to one.

The negative recommendation is nevertheless forced by the same principal endpoint that governed the revision-54 report. Revision 55 still does **not** prove

\[
\sup_{R,n,k}\operatorname*{ess\,sup}_{u\,\mathrm{central}}
\left|m^2p_{n,R}(k,m,u)
      -\mathcal L_{m,R}(k_1,k_2,u,n)\right|\longrightarrow0.
\]

The positive incidence and clearance sources may still form arbitrarily narrow upward spikes. A uniform weak `L^(145/144)` bound, every strong `L^q` bound below that endpoint, endpoint Orlicz convergence, and both forward and reverse relative-entropy convergence are all compatible with unbounded essential heights on sets of vanishing width.

Thus revision 55 gives a clean explicit endpoint in the scale of finite integral norms, but it does not close the two positive essential-height estimates which the manuscript itself identifies as equivalent to the full two-sided pointwise raw-density theorem.

At the requested benchmark, a manuscript of this length and model specificity, entitled and organized around raw local inversion, should either complete that pointwise endpoint or extract a substantially broader theorem whose independent significance is not governed by the remaining positive-height obstruction. Revision 55 does neither yet.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`32866de446dd83c3036c04544ce4da66b019a990`.

The repository tree at that commit is

`13fb49d00e2bc5888fc7d2828b73fda781b8668a`.

The active article is

`papers/A2-DYN-v55-referee-response`.

The ordinary source payload tree recorded in the manifest is

`e3e3d73a2be912424f339fdef250404077ff1785`.

The author commit has the revision-54 external-report commit

`7d4e3f6cafebf96da91d2d3a81147841418d9e61`

as its parent. The chronology is therefore correct: the new author revision begins from the frozen external assessment rather than altering the reviewed revision-54 source in place.

The source manifest records:

- all one hundred sixteen inherited core modules retained byte-for-byte;
- all one hundred fifty-one inherited Python files retained byte-for-byte;
- the bibliography and compiled appendices retained;
- all one thousand five hundred forty-nine inherited mathematical labels retained;
- two new modules, 117 and 118;
- `cap_free_weak_density_endpoint_proved: true`;
- `strong_density_exponent_range: 1<q<145/144`;
- `endpoint_modular_raw_laws_proved: true`;
- `forward_likelihood_convergence_proved: true`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `pointwise_roof_conditioned_bridge_proved: false`;
- `arithmetic_factor_identically_one_proved: false`;
- and `independent_human_review: false`.

The exact-source qualification workflows completed successfully on both reviewed refs:

- response branch run `37893598233`;
- referee-copy branch run `37893616764`.

These runs establish source identity, byte preservation, native TeX compilation, agreement of normal and optimized finite diagnostics, and theorem-label-based rendering at the reviewed SHA. They do not certify the continuum singular geometry, the anisotropic-space estimates, the moving spectral decomposition, or the positive-height endpoint.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v55-external-top4-review-2026-10-09/`.

No author manuscript source, prior review, workflow, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Scope of this review

I did not attempt to re-prove all one hundred eighteen core modules. The substantive audit concerns the changes capable of altering the revision-54 assessment:

1. the exact global mass of all guard failures;
2. the normalization and disjointness of exact labels in that mass estimate;
3. the two-regime removal of the finite-count spectral error;
4. simultaneous local thin-layer mass at arbitrary finite protection scales;
5. the abstract positive-source endpoint principle;
6. the explicit weak endpoint `145/144`;
7. strong local powers below the endpoint;
8. finite-count powers of the incidence and clearance remainders;
9. all-band convolution estimates in those powers;
10. the endpoint Orlicz function and its tail integral;
11. the endpoint-modular scalar raw law;
12. the bounded-Lipschitz-dual path-valued extension;
13. the forward likelihood normalization;
14. forward relative entropy and Renyi convergence;
15. the distinction between these integral results and the remaining essential-height criterion;
16. arithmetic modulation;
17. source identity and qualification evidence.

The inherited revision-54 continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 4. The exact global all-margin mass

The new global estimate is

\[
\sup_R\sum_{n=1}^m\sum_{k\in\mathbb Z^2}
\int_{\mathbb R}R_{\varepsilon,n,k,m,R}(u)\,du
\le C m^2\varepsilon,
\]

where

\[
P=m^2p_{n,R}(k,m,\cdot),\qquad
F_\varepsilon=m^2f^{\varepsilon,1}_{n,k,m,R},\qquad
R_\varepsilon=P-F_\varepsilon\ge0.
\]

The proof uses invariant one-flight estimates for the individual guard failures:

- incidence mass `O(a^2)` at width `a`;
- section-decision mass `O(a)`;
- clearance mass `O(a)`, with the clearance of flight `j` read at collision `j+1`.

The graded widths are geometric in the distance to the endpoints. Since at most two indices have a given depth, the sum over all depths is `O(epsilon)` rather than `O(m epsilon)`.

At fixed collision count `m`, the events with exact labels `(n,k)` are disjoint. Summing their pushforward masses therefore costs no overlap factor. The initial-section normalization contributes `1/c` once. Multiplication by the local-limit normalization `m^2` produces the displayed global bound.

This is the correct normalization. The estimate is intentionally global in `(n,k,u)` and is not itself a local limit.

The main specialist obligations are inherited geometric ones:

- the complete list of guard factors must be exactly the one used in the protected source;
- each strip-mass estimate must be uniform in the radius;
- clearance must remain an image-side, next-collision event;
- the graded union must not introduce an uncounted endpoint term;
- the terminal section visit must not be added to the half-open occupation count.

I found no contradiction in the written bookkeeping.

## 5. The two-regime lemma

The abstract statement is elementary but load-bearing. If

\[
U_m(\varepsilon)
\le C_1(\varepsilon^\alpha+e^{-\kappa m})
\]

and simultaneously

\[
U_m(\varepsilon)\le C_2m^r\varepsilon^\beta,
\qquad \beta>\alpha,
\]

then the manuscript splits into two cases.

If

\[
\kappa m\ge\alpha\log(1/\varepsilon),
\]

then the exponential term is at most `epsilon^alpha`.

Otherwise

\[
m\le (\alpha/\kappa)\log(1/\varepsilon),
\]

and the global estimate gives

\[
U_m(\varepsilon)
\le C[\log(1/\varepsilon)]^r\varepsilon^\beta
\le C\varepsilon^\alpha.
\]

The last inequality follows because a polynomial in the logarithm is dominated by

\[
\varepsilon^{-(\beta-\alpha)}
\]

as `epsilon` tends to zero.

This is a finite-count argument. It neither chooses a subsequence nor interchanges a collision limit with a protection-scale limit. The constant is allowed to depend on the fixed auxiliary spectral estimate, but not on `m` or `epsilon`.

The deduction is correct.

## 6. Error-free simultaneous local thin mass

The inherited revision-54 estimate has the form

\[
\int_I R_\varepsilon
\le C(1+h)\bigl(\varepsilon^{1/16}+m^3\rho^{m/2}\bigr)
\]

for every interval `I` of length `h`, every collision count and every protection scale.

The polynomial factor is absorbed into a weaker exponential:

\[
m^3\rho^{m/2}\le Ce^{-\kappa m}.
\]

The global estimate supplies

\[
\int_I R_\varepsilon
\le C m^2\varepsilon.
\]

After division by `1+h`, the two-regime lemma applies with

\[
(\alpha,\beta,r)=(1/16,1,2).
\]

The result is the finite inequality

\[
\sup_{R,n,k}\int_I R_\varepsilon(u)\,du
\le C(1+h)\varepsilon^{1/16}
\]

for all `m >= 2` and all admissible `epsilon`, including scales depending on `m`.

The same estimate holds separately for the positive incidence and clearance sources because each is dominated by the full positive remainder. Bounded insertions are handled by variation domination.

This theorem is a real advance over the revision-54 statement. It removes the finite-count error before any density-level integration and is the reason the new endpoint no longer depends on `kappa/Gamma`.

It remains a mass theorem. It does not estimate the essential height of either positive remainder.

## 7. The abstract positive-source endpoint principle

The new principle assumes an exact positive decomposition

\[
P_m=A_{m,\varepsilon}+B_{m,\varepsilon},
\qquad A_{m,\varepsilon},B_{m,\varepsilon}\ge0,
\]

with

\[
\|A_{m,\varepsilon}\|_\infty
\le C_A\varepsilon^{-K}
\]

and the two mass estimates required by the preceding section.

After using the two-regime lemma to obtain

\[
\int B_{m,\varepsilon}\le C\varepsilon^\alpha,
\]

the proof chooses

\[
\varepsilon=(2C_A/L)^{1/K}.
\]

On the set `{P_m > L}` one has `A <= L/2 < P_m/2`, and hence

\[
B_{m,\varepsilon}\ge P_m/2.
\]

Therefore

\[
\int_{\{P_m>L\}}P_m
\le C L^{-\alpha/K}.
\]

Dividing by `L` gives the distribution tail

\[
|\{P_m>L\}|
\le C L^{-(1+\alpha/K)}.
\]

The uniform first moment controls bounded density levels. Layer-cake integration yields strong `L^q` for every

\[
1<q<1+\alpha/K.
\]

No complete-source height cap is used. The proof is correct.

This abstract theorem is reusable as a measure-theoretic device. Its dynamical content, however, lies entirely in the model-specific verification of the positive decomposition, protected height and two simultaneous mass estimates.

## 8. The explicit weak endpoint

For the actual billiard source,

\[
K=9,\qquad \alpha=1/16.
\]

Thus

\[
a_c=\frac{\alpha}{K}=\frac1{144},
\qquad p_c=1+a_c=\frac{145}{144}.
\]

On every translated roof interval of fixed length `h`, the manuscript proves

\[
\int_{I\cap\{P>L\}}P\le C(1+h)L^{-1/144},
\]

and

\[
\sup_{L>0}L^{145/144}|\{u\in I:P(u)>L\}|
\le C(1+h).
\]

Consequently

\[
\int_I P^q\le C_q(1+h)
\qquad(1<q<145/144).
\]

The interval length is fixed in every raw-limit conclusion, although the finite-count tail estimate itself is uniform in translated intervals. The constant may depend on the fixed local norm parameters and, for strong powers, on `q`.

The endpoint is weak. The manuscript does not claim strong `L^(145/144)` and should continue to resist formulations such as “the density is in `L^(145/144)`” without the word “weak.”

The calculation is correct.

## 9. Finite-count norms of the physical remainders

For each positive physical component

\[
B_{\varepsilon,j}=m^2b_{n,k,m,R}^{\varepsilon,j,1},
\qquad j\in\{\mathrm{inc},\mathrm{clr},\mathrm{phys}\},
\]

one has

\[
0\le B_{\varepsilon,j}\le P.
\]

The local first moment is

\[
\int_I B_{\varepsilon,j}
\le C(1+h)\varepsilon^{1/16}.
\]

The weak endpoint of `P`, together with the elementary interpolation between the Markov tail and the weak-endpoint tail, gives

\[
\int_I |B_{\varepsilon,j}^w|^q
\le C_qM^q(1+h)
\varepsilon^{9(145/144-q)}
\]

for every bounded insertion `|w| <= M` and every

\[
1<q<145/144.
\]

The exponent is correctly computed:

\[
\frac1{16}
\frac{p_c-q}{p_c-1}
=9(p_c-q).
\]

Minkowski's integral inequality and the scale-invariant `L^1` norm of the reconstruction kernel yield the same order for

\[
B_{\varepsilon,j}^w-K_B*B_{\varepsilon,j}^w
\]

uniformly in every reconstruction bandwidth. This last step is an analytic convolution estimate; it does not invoke a spectral theorem at a growing band.

The result is correctly stated for each finite count and each protection scale. It is still an integral norm, not an essential-height estimate.

## 10. The logarithmically weakened endpoint modular

For `beta > 1`, the manuscript defines

\[
\Phi_\beta(x)
=
\int_0^x
\frac{(x-t)t^{p_c-2}}
     {[\log(e+t)]^\beta}\,dt.
\]

One has

\[
\Phi_\beta''(x)
=
\frac{x^{p_c-2}}{[\log(e+x)]^\beta}>0.
\]

Since

\[
p_c-2=-143/144>-1,
\]

the integral is finite at zero. The function is convex, increasing, behaves like `x^(p_c)` near zero, and is comparable at infinity to

\[
\frac{x^{p_c}}{[\log(e+x)]^\beta}.
\]

If a family has a uniform weak `L^(p_c)` bound, then

\[
\int_{\{f>T\}}\Phi_\beta(f)
\le C_\beta[\log(e+T)]^{1-\beta}.
\]

The integral converges precisely because `beta > 1`.

If in addition `int f <= delta`, splitting at a power of `delta^(-1)` gives

\[
\int\Phi_\beta(f)
\le C_\beta\left(
\delta^{1/2}+[1+\log(1/\delta)]^{1-\beta}
\right).
\]

This proves modular convergence from local `L^1` convergence plus the uniform weak endpoint.

The endpoint modular is a genuine strengthening of every fixed subcritical power, but it remains weaker than strong `L^(p_c)` and much weaker than essential supremum.

I found the convexity, tail integration and small-mass argument correct.

## 11. Scalar raw laws below and at the modular endpoint

The arithmetic transition kernel `G` is uniformly bounded. Therefore

\[
|P-G|\le P+C
\]

inherits a uniform weak `L^(p_c)` bound on translated fixed windows.

The revision-49 theorem supplies

\[
\int_I|P-G|\longrightarrow0
\]

uniformly after the prescribed normalization. Interpolation gives

\[
\int_I|P-G|^q\longrightarrow0
\qquad(1<q<p_c).
\]

The endpoint modular lemma gives

\[
\int_I\Phi_\beta(|P-G|)\longrightarrow0
\qquad(\beta>1).
\]

The arithmetic main term is the full transition kernel

\[
G(u)=\mathcal L_{m,R}(k_1,k_2,u,n).
\]

At fixed radius and on central compact sets it specializes to

\[
c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z(u)).
\]

The factor `mathfrak a_R` is intrinsic to the theorem currently proved. No section-residue triviality is assumed.

The scalar endpoint law is internally coherent.

## 12. Path-valued endpoint laws

Let `mathbf P(u)` be the path-valued raw measure and let `W_R` be the Gaussian bridge reference. The manuscript considers

\[
E^{\mathrm{path}}(u)
=
\|\mathbf P(u)-G(u)\mathsf W_R\|_{\mathrm{BL}^*}.
\]

Since the path source is positive and `W_R` is a probability,

\[
E^{\mathrm{path}}(u)
\le P(u)+|G(u)|.
\]

Thus the path error inherits the scalar weak endpoint. Its local first moment tends to zero by the inherited common-numerator theorem. The same interpolation and modular arguments yield the path-dual local `L^q` and endpoint-modular laws.

For the actual return path, the theorem is restricted to the inherited central target classes and uses the previously proved roof-integrated return-clock transfer.

The norm is bounded-Lipschitz dual in the path variable. It is not path-space total variation. The convergence is integrated in the roof variable and does not by itself give a bridge at every roof value.

These distinctions are accurately maintained.

## 13. Forward likelihood and endpoint divergences

Fix a roof window `I` of positive length and assume

\[
G(u)\ge d>0
\]

almost everywhere on that window. Let

\[
F=\int_I P,\qquad H=\int_I G,
\]

and define the true and reference conditional roof laws by

\[
d\pi=P\,du/F,
\qquad
dQ=G\,du/H.
\]

Their likelihood ratio is

\[
r=\frac{d\pi}{dQ}=rac{HP}{FG}.
\]

The exact identity

\[
r-1
=
\frac{H(P-G)}{FG}
+
\frac{H-F}{F}
\]

is correct. The pointwise floor on `G`, the uniform upper bound on `G`, and local `L^1` convergence give positive and bounded normalizing constants for sufficiently large counts.

The raw local `L^q` theorem therefore yields

\[
\int|r-1|^q\,dQ\longrightarrow0
\qquad(1<q<p_c).
\]

The endpoint modular passes through bounded scalar multiplication and the constant normalization error by convexity and the fixed-factor doubling inequality.

For relative entropy, the inequality

\[
0\le x\log x-x+1
\le C_q|x-1|^q,
\qquad 1<q<2,
\]

is applicable because `p_c < 2`. Since `int(r-1)dQ=0`, this proves

\[
D(\pi\Vert Q)\longrightarrow0.
\]

For every fixed Renyi order `q` in the same range, `L^q(Q)` convergence implies

\[
\int r^q\,dQ\longrightarrow1
\]

and hence convergence of the Renyi divergence.

The function

\[
f(x)=\Phi_\beta(|x-1|)
\]

is convex because `Phi_beta` is convex and nondecreasing and absolute value is convex. It therefore defines a genuine nonnegative convex `f`-divergence.

The proof is correct in its stated scope.

The pointwise floor is indispensable. A positive integrated reference mass alone would not bound the factor `1/G`, and the manuscript does not make that mistake.

## 14. What revision 55 closes

Relative to revision 54, the new manuscript closes several real issues.

1. It removes the dependence of the proved integrability interval on the complete exponential height cap.
2. It converts the former nonexplicit exponent
   \[
   1+s_*,
   \qquad
   s_*<\min\{1/144,\kappa/\Gamma\},
   \]
   into the explicit weak endpoint
   \[
   145/144
   \]
   and the full open strong range below it.
3. It proves an error-free local positive-source mass bound at every finite count and protection scale.
4. It gives explicit finite-count `L^q` powers for each physical remainder separately.
5. It gives endpoint-modular scalar and path-valued raw laws.
6. It gives endpoint-modular forward likelihood convergence.
7. It keeps all exact labels, the unchanged source, and the arithmetic transition kernel.

These are substantive improvements.

## 15. What revision 55 does not close

The following remain unproved.

### 15.1 Positive incidence essential height

The manuscript does not prove

\[
\lim_{B\to\infty}\limsup_{m\to\infty}
\|m^2b_{\mathrm{inc}}^{\varepsilon(B),1}\|_{\infty,M}=0.
\]

### 15.2 Positive clearance essential height

It does not prove

\[
\lim_{B\to\infty}\limsup_{m\to\infty}
\|m^2b_{\mathrm{clr}}^{\varepsilon(B),1}\|_{\infty,M}=0.
\]

### 15.3 The two-sided pointwise raw-density theorem

The positive-remainder identity shows that these two bounds are equivalent to the remaining upper side of the original pointwise theorem. They are not optional refinements.

### 15.4 Uniform same-roof bridges

The inherited theorem shows that scalar pointwise height would imply the corresponding uniform same-roof path statement. Since scalar height is still open, the unconditional uniform bridge remains open.

### 15.5 Forward essential likelihood

Finite powers, endpoint Orlicz convergence and relative entropy do not imply

\[
\|r-1\|_\infty\longrightarrow0.
\]

### 15.6 Strong critical-endpoint integrability

The manuscript proves weak `L^(145/144)` and logarithmically weakened endpoint modulars, not strong `L^(145/144)`.

### 15.7 Unmodulated arithmetic specialization

The concrete section residues are not proved trivial. The fixed-radius arithmetic factor and the parameter-uniform transition kernel must remain in the theorem.

## 16. Why the weak endpoint does not settle essential height

A family may satisfy

\[
\sup_m\|P_m\|_{L^{p,\infty}}<\infty
\]

for some `p > 1` while

\[
\|P_m\|_\infty\longrightarrow\infty.
\]

For example, a spike of height `H` and width `H^(-p)` has a bounded weak `L^p` quasi-norm. Its contribution to every `L^q`, `q < p`, tends to zero as `H` tends to infinity, but its essential height diverges.

Logarithmically weakened endpoint modular convergence allows the same phenomenon with a suitable reduction in width. Relative entropy is also insensitive to sufficiently narrow spikes.

Thus the new results make positive physical spikes quantitatively rare, but they do not bound their height. The principal pointwise obstruction is unchanged in topology, even though it is much more sharply localized.

## 17. Arithmetic modulation

The manuscript now presents the finite transition kernel as a permanent part of the main theorem. This is mathematically appropriate.

At fixed radius, the exact-index central main term is

\[
c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z).
\]

Uniformly through changes of arithmetic type, it is

\[
\mathcal L_{m,R}.
\]

Revision 55 proves neither that the resonance group is trivial nor that the actual section phase masses are uniform. The arithmetic factor therefore cannot be replaced by one.

A future pointwise theorem should retain the arithmetic transition kernel unless the zero-residue criterion is separately proved for the concrete section.

## 18. Generality and top-four significance

The cap-free endpoint principle is a clean and reusable measure-theoretic observation. It identifies a useful mechanism:

- polynomial protected height;
- local thin-source mass with a finite-count exponential error;
- exact global thin-source mass with a better width exponent;
- a two-regime removal of the error;
- and an explicit weak endpoint.

However, the difficult hypotheses are verified here through a highly specialized and very long chain involving:

- one triangular finite-horizon Lorentz family;
- the particular moving section;
- the image-side physical incidence and clearance geometry;
- protected flow boxes and critical collars;
- local collision anisotropic spaces;
- full occupation-torus peripheral analysis;
- finite arithmetic resonance groups;
- exact-label disintegration;
- all-depth decision and physical-source decompositions;
- moving spectral peaks;
- and path-valued roof disintegration.

The abstract endpoint principle itself is comparatively elementary once those inputs are granted. Revision 55 does not verify a second genuinely different singular-hyperbolic application and does not yet extract a broad theorem whose importance is independent of the unfinished pointwise endpoint.

Subject to specialist verification, the explicit weak-endpoint density law, endpoint Orlicz theorem, path-valued raw laws and forward likelihood results could support a strong specialized dynamics/probability paper. They do not, in my judgment, support the requested top-four placement in the present architecture.

## 19. Independent specialist verification

No independent human specialist audit has been obtained. At minimum, the following inherited and new interfaces require line-by-line expert checking.

1. The complete list and exact normalization of the full guard factors.
2. Uniform invariant mass of the section strips.
3. The image-side incidence and clearance strip geometry.
4. The next-collision convention for flight clearance.
5. The geometric depth sums at both endpoints.
6. Disjointness of exact `(n,k)` events at fixed collision count.
7. The fixed-band marked local upper estimate.
8. Uniformity of the local estimate in the mark and strip width.
9. The full occupation-torus anisotropic power bounds.
10. Strong-space faithfulness and physical peripheral representatives.
11. Moving spectral peak charts and common complex neighborhoods.
12. The protected flow-box height estimate of order `epsilon^(-9)`.
13. Near-critical completion and one-time charging of critical collars.
14. Exact preservation of the source normalization `1/c`.
15. The half-open occupation convention `0,...,m-1`.
16. The common roof versions of the path-valued measures.
17. The actual return-clock transfer on central target classes.
18. The uniform pointwise arithmetic floor through parameter transitions.

The new two-regime, interpolation and Orlicz arguments are largely self-contained. Their application nevertheless depends on these continuum inputs.

The exact-source workflows and finite diagnostics are valuable reproducibility evidence but are not mathematical proof certification.

## 20. Architecture and editorial presentation

The front matter is more honest than in early revisions. It states the explicit weak endpoint, the arithmetic main term, the path topology, and the unproved positive-height endpoint separately.

The manuscript nevertheless remains extremely large and combines several papers' worth of mathematics:

1. stationary physical local limits;
2. compact-family action and spectral theory;
3. exact return-index arithmetic;
4. path-valued raw inversion and same-roof transport;
5. protected and unprotected physical-boundary reconstruction;
6. endpoint density integrability and likelihood theory;
7. an unfinished pointwise raw-density program.

For a journal submission, the authors should choose a single principal endpoint.

### Option A: focused endpoint-integrability paper

Center the paper on the explicit weak `L^(145/144)` endpoint, the subcritical raw laws, endpoint Orlicz convergence and the path/likelihood consequences. State the arithmetic transition kernel as intrinsic. Move the unfinished essential-height program and much of the historical pipeline to a companion work.

### Option B: complete pointwise raw-inversion paper

Retain the present title and full architecture only after proving the two positive physical essential-height estimates and the resulting uniform same-roof bridge.

The present manuscript remains between these two architectures.

## 21. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

1. **Control the positive incidence height.**  
   Prove central-scale essential-supremum smallness of the complete first-incidence remainder, uniformly in the exact labels and radius.

2. **Control the positive clearance height.**  
   Prove the analogous estimate for the first-clearance remainder without continuing an orbit through a competing-hit seam.

3. **Complete the two-sided arithmetic raw theorem.**  
   Combine the two positive-height estimates with the existing transition kernel and positive-remainder representation.

4. **Deduce the unconditional uniform same-roof bridge.**  
   Apply the already isolated path-measure implication after scalar height has been established.

5. **Resolve the arithmetic endpoint editorially.**  
   Either prove the concrete zero-residue criterion or retain the arithmetic factor and transition kernel permanently in the principal theorem and title-level description.

6. **Obtain independent specialist review.**  
   The physical multipliers, protected critical geometry, full occupation spectrum, moving peaks, exact source partition and path transfer require external human verification.

7. **Extract and verify a broader theorem.**  
   Formulate a singular-hyperbolic endpoint theorem with checkable assumptions and verify it in more than one genuinely different system if top-four breadth is sought.

8. **Reduce the submission burden.**  
   Present the shortest complete proof route to one principal result. Historical derivations, duplicated theorem hierarchies and validation ledgers should not dominate the article.

9. **Sharpen the prior-art comparison.**  
   Explain theorem by theorem which exact-label, arithmetic, unprotected-source, endpoint-norm and same-roof conclusions are not consequences of existing Lorentz-process, billiard mixing-local-limit and suspension local-limit theorems.

## 22. Technical and presentation comments

1. Keep the auxiliary spectral band, reconstruction band, protection width, density level, collision count and roof-window length visibly distinct.
2. State explicitly whenever an estimate is finite in `m`, rather than a limsup for each fixed scale.
3. Keep the global normalized mass `C m^2 epsilon` separate from the local normalized mass `C(1+h) epsilon^(1/16)`.
4. Preserve the exact-label disjointness argument when summing over `(n,k)`.
5. Record the source factor `1/c` exactly once.
6. Keep clearance of flight `j` at collision `j+1`.
7. Keep the half-open occupation interval `0,...,m-1` explicit near terminal marks.
8. Do not state strong `L^(145/144)`; the proved endpoint is weak.
9. Keep the condition `beta > 1` visible in every endpoint-modular theorem.
10. Do not infer essential height from endpoint modular convergence.
11. Keep fixed-window local laws distinct from shrinking-window or pointwise laws.
12. State the dependence of strong `L^q` constants on `q` as `q` approaches the endpoint.
13. Keep bounded-Lipschitz path dual norm distinct from path-space total variation.
14. Keep roof-integrated path convergence distinct from pointwise same-roof convergence.
15. Retain the pointwise arithmetic floor `G >= d` in forward likelihood statements.
16. Do not assign a reference likelihood to zero arithmetic classes.
17. Keep forward finite-order likelihood distinct from forward essential likelihood.
18. Retain the arithmetic transition kernel through parameter transitions.
19. Continue to distinguish source qualification and finite diagnostics from continuum proof certification.
20. State in one place that the abstract endpoint principle is measure-theoretic and that its difficult hypotheses remain model-specific.

## 23. Final assessment

Revision 55 is a serious and mathematically constructive response to the revision-54 report.

It proves a finite-count, protection-scale-uniform local mass estimate for the full guard complement; removes the finite-count spectral error by combining local and exact global bounds; obtains the explicit weak endpoint `145/144` without using the complete exponential density cap; gives the full open strong range below that endpoint; derives finite-count subcritical norms for the incidence and clearance remainders; establishes logarithmically weakened endpoint scalar and path-valued raw laws; and proves forward likelihood, relative entropy and Renyi convergence in the corresponding range.

The new deductions are internally coherent in their stated topology. I found no decisive mathematical error in modules 117--118.

The principal theorem advertised by the title is nevertheless still incomplete. Positive incidence and clearance sources may retain arbitrarily narrow upward spikes, and neither their essential heights nor the full two-sided pointwise arithmetic raw-density theorem are proved. Uniform pointwise same-roof bridges and forward essential likelihood remain conditional on that missing scalar estimate.

The manuscript is also exceptionally large, highly model-specific, and not independently audited by specialists in dispersing billiards and anisotropic transfer operators.

Subject to such verification, the explicit weak-endpoint and endpoint-modular results could form a strong specialized paper in a focused architecture. At the requested four-journal benchmark, however, the unresolved pointwise endpoint and limited generality remain decisive.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
