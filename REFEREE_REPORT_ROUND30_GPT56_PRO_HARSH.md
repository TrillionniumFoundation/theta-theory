# External Referee Report on the Round-Twenty-Nine Revision

## Recommendation: **Reject all eleven manuscripts; do not invite another dossier-wide major revision**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round29-referee-positive-closure-11paper-2026-09-02`  
**Pre-review head:** `0fb10c3bca5ac401c032a87407a192c155a2d548`  
**Mathematical-source commit:** `76f7ae36d7f894673383ceccda41c86b1cb6ac5c`  
**Review branch:** `review/round30-gpt56-pro-harsh-11paper-2026-09-02`  
**Review date:** 2 September 2026  
**Scope:** all eleven active `ROUND29_POSITIVE_CLOSURE.tex` files and wrappers, `AUTHOR_RESPONSE_ROUND28.md`, the Round-Twenty-Nine review index, dependency ledger, mathematical regression ledger, source manifest, and committed verification record.

This report applies the standard of correctness, self-containedness, significance, and presentation expected at *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, or *Acta Mathematica*.

Round Twenty Nine is a genuine source revision. It changes all eleven active theorem files, switches the wrappers, provides an author response, and records successful local builds of an eleven-paper, 51-page dossier. Several elementary contradictions from Round Twenty Eight have indeed been removed.

The mathematical conclusion remains negative. The new sources contain fresh direct contradictions, incorrect normalizations, invalid compactness claims, and proof steps that do not follow from the hypotheses stated immediately before them. A number of the new “repair mechanisms” work only by assuming the difficult conclusion as a certificate. The defects below occur in root papers and therefore invalidate every downstream synthesis paper.

The most decisive findings are:

1. A1 loses Sobolev regularity under differentiation but nevertheless claims trace-norm differentiability of a covariance operator on the original, more regular Hilbert space.
2. A2 claims that an exact arithmetic annihilator condition is stable under small perturbations, which is false; its all-frequency bounds also do not provide the integrable noncentral estimate required for the LLT and, when combined at zero frequency as the proof does, conflict with `L_0^n 1 = 1`.
3. A3 charges transition relative entropy against holding occupation rather than transition count. Even for deterministic return length `R=r`, its proposed rate differs from the exact chain entropy by the factor `r`.
4. A4's vertical-line memory expansion does not follow from a graph-bounded observation operator: the final resolvent remainder is at best controlled one power more weakly than claimed. Its compression proof also invokes a bounded perturbation theorem for a perturbation only bounded from the graph domain.
5. B1's “universal coarea anchor” cannot have a uniformly nonzero momentum-energy Jacobian on its whole support: at configurations with all anchor velocities equal, the energy differential is a linear combination of the momentum differentials.
6. B2's radius-loss estimate is not implied by its one-step Cauchy bound. The standard analytic-translation counterexample shows that a `1/(a-a')` creation estimate permits evolution only for time comparable with the lost radius, not the asserted arbitrary-time exponential bound.
7. B3's root-revealment argument does not prove an Aldous stopping-time estimate. Resampling one root may move the stopping time itself and thereby move the entire observation interval; predictability in the temporal filtration does not localize Efron--Stein influence in the root-revealment filtration.
8. B4's entropy-energy shells are not compact in `W_2`. A vanishing mass placed at velocity `R` can retain order-one kinetic energy while keeping both relative entropy and total second moment uniformly bounded. The claimed global strong continuity also fails on the unbounded-energy state space.
9. C1's stratified observation density is not normalized: the factor `2^{|s|}` cancels the envelope weight on each stratum, so every active stratum contributes mass one. Its asserted strict Hilbert-projective contraction is also false for deterministic hidden dynamics.
10. C2 writes the hidden-model likelihood with one common filter in numerator and denominator; the correct product uses the parameter-specific filter under each parameter. The displayed formula is generally false already at the second observation.
11. D1 has the sign of the lattice-summation power wrong for an ordinary phase cell, assumes a higher-order local expansion not exported by A2 or B1, and later rescales the raw lattice variable inconsistently.

Any one of items 2, 3, 5, 7, 8, or 9 is sufficient to reject its paper. Together they break both root chains and all synthesis nodes.

---

## 1. Confidential recommendation to the editor

I recommend **rejection of the entire eleven-paper submission, without another major-revision invitation for this dossier**.

This recommendation is not based on the ambition or breadth of the programme. If correct, several of the claimed results would be substantial. The problem is that the active proofs do not establish the active statements. Some failures are elementary and admit explicit counterexamples; others are exactly the deep analytic steps for which the manuscripts provide only a sentence or a certificate label.

The repository verification is useful for source identity and reproducibility. It is not mathematical validation. The active papers are four to six pages each, yet they claim complete theorem packages in singular hyperbolic dynamics, raw local limit theory, stopped path-space large deviations, hard-sphere cluster expansions, kinetic process limits, nonlinear semigroups, filtering, adaptive Bernstein--von Mises theory, strict-topology duality, optional projections, and phase coexistence. At this level, every root estimate must be fully proved on the exact space exported downstream.

The current dossier is not close to that threshold. A future submission should isolate one root theorem and present a complete specialist paper before any downstream synthesis is resubmitted.

---

## 2. Source identity and repository status

### 2.1 The revision is real

The comparison with `review/round28-gpt56-pro-harsh-11paper-2026-09-02` shows a genuine two-commit Round-Twenty-Nine revision. The mathematical commit adds eleven active `ROUND29_POSITIVE_CLOSURE.tex` files, eleven standalone wrappers, the response and ledgers, and a verifier. The head then makes a CI-isolation adjustment.

All eleven `main.tex` files point to Round Twenty Nine. I therefore reviewed the Round-Twenty-Nine sources, not the older files or the prose in the response alone.

### 2.2 Build status

The committed verification record reports:

```text
active_sources: 11
standalone_pdfs: 11
dossier_pages: 51
local_latex_builds: pass
local_regression_tokens: pass
local_source_identity: pass
```

I do not dispute those repository facts. They establish that the selected source files compile and contain the requested labels and regression tokens.

They do not establish that:

- a loss-indexed derivative remains trace-norm differentiable on the original Hilbert space;
- an exact nonarithmeticity condition is open;
- a piecewise Fourier bound has a negligible integral;
- a stopped-chain action uses the correct entropy clock;
- a graph-domain resolvent remainder has the advertised power of `|z|`;
- a global coarea minor is nonzero;
- an analytic-radius loss can be spent indefinitely;
- a random stopping time is stable under root replacement;
- entropy and energy bounds imply `W_2` compactness;
- a countable-stratum likelihood integrates to one;
- or a hidden-model likelihood can use the same filter under two parameters.

### 2.3 Genuine improvements

The revision does make several sensible corrections:

- A1 now sends distributional derivatives toward larger negative-Sobolev spaces and uses a genuine polygonal interpolation.
- A3 separates the return overshoot from the Gaussian renewal coordinates.
- A4 no longer uses exact-tail Doeblin minorization and types the elementary suspension renewal maps.
- B3 retains contact-cycle directions instead of quotienting them away.
- B4 separates initial preparation entropy from the running action.
- C1 includes the missing envelope Radon--Nikodym factor on each individual stratum.
- C2 separates discrete, point-process, and Brownian likelihood formulas.
- D1 excludes zero-prior phases from its finite log-sum and no longer integrates over a policy manifold.

These corrections remove earlier counterexamples. They do not prove the replacement theorems, and in several cases the replacement introduces a new contradiction.

---

## 3. Direct mathematical contradictions

### 3.1 A1: trace-norm covariance response is incompatible with the declared derivative loss

The paper correctly defines the inclusions

```text
J^s -> J^{s+2},
```

where the larger index is the larger, more singular current space. It then proves only

```text
partial_a D_0 in J^{m+2},
```

for an increment `D_0` originally lying in `J^m`.

Nevertheless Theorem A1.16 states that

```text
Q_a h = E[<D_0,h>D_0]
```

is `C^{r-1}` **in trace norm on `J^m`**.

This does not follow and is generally false. Differentiating a rank-one term formally gives

```text
D_0' tensor D_0 + D_0 tensor D_0'.
```

But `D_0'` is only known to belong to `J^{m+2}`, not to `J^m`. Such a tensor is not a trace-class operator on `J^m` unless additional regularity is imposed.

The moving-Dirac model invoked by the authors illustrates the obstruction. Choose the base Sobolev index so that `delta_a` belongs to the base dual but its derivative belongs only to the next larger dual. Then `a -> delta_a` is differentiable in the larger distribution space but not in the base Hilbert norm. Consequently `delta_a tensor delta_a` need not be differentiable in the trace norm of the base Hilbert space.

Normal convergence in the loss-indexed spaces does not repair this type mismatch. The correct conclusion would have to be a covariance derivative in a weaker operator topology between different levels of the scale, or it would require two additional derivatives of the current observable so that every derivative returns to the base space.

A second unresolved point is that condition (A1.12), required for the maximal martingale approximation, is simply imposed after the projective current domain is constructed. The manuscript does not prove that the motivating seam current satisfies the two-sided projection condition with the extra `(1+|q|)^{1/2}` weight. Thus even the nondifferentiated FCLT is not closed for the advertised geometric observable.

**Disposition for A1: reject.** The direction of distributional loss is now correct, but the covariance-response theorem ignores that very loss.

---

### 3.2 A2: exact arithmetic is not perturbatively stable

Proposition A2.5 claims that the entire certificate, including the exact annihilator property

```text
{b: b.beta_j in 2 pi Z for all j} = {0},
```

is stable under sufficiently small smooth perturbations.

That is false. In one dimension the property for the pair `(1,sqrt(2))` is irrationality of the ratio. Every neighbourhood of `sqrt(2)` contains a rational `p/q`. Replacing `sqrt(2)` by `p/q` creates the nonzero character

```text
b = 2 pi q,
```

which pairs integrally with both generators.

The same defect occurs in two dimensions. The vector `(sqrt(2),sqrt(3))` can be approximated arbitrarily closely by a rational vector relative to `(1,0)` and `(0,1)`, producing a nonzero dual-lattice character. Exact nonarithmeticity of a finitely generated subgroup is not an open finite collection of strict inequalities.

The proof sentence “all inequalities are strict and hence survive a small perturbation” does not apply to (A2.4). If the family theorem needs uniform arithmetic, the parameter family must be defined by an exact symbolic or Diophantine constraint and cannot be declared open in the ordinary `C^r` topology.

### 3.3 A2: the good/bad estimates conflict with the untwisted eigenvalue

The finite grammar says that every word either contains the required returned blocks or belongs to the terminal bad language. Lemma A2.9 gives an exponentially decaying bound for the first class; Lemma A2.10 gives an exponentially decaying bound for the second class.

Set `b=0`. Then `(1+|b|)^{-M}=1`. If these two estimates are combined exactly as the proof of Theorem A2.12 says, they cover the whole `n`-iterate and imply an exponentially decaying untwisted operator norm. But the untwisted transfer operator satisfies

```text
L_0^n 1 = 1.
```

Its norm cannot decay exponentially.

This shows that at least one of the following is being conflated:

- return-time layer estimates;
- branchwise oscillatory differences;
- the full `n`-iterate;
- or cancellation that is present only when `|b|` is bounded away from zero.

The stated lemmas cannot simultaneously be the all-word operator estimates used in Theorem A2.12.

### 3.4 A2: the intermediate-frequency estimate does not close Fourier inversion

The intermediate line of (A2.12) is

```text
exp[-c n/(1+log|b|)^q],
B < |b| <= exp(kappa n).
```

Near the upper end of that interval this is only

```text
exp[-C n^(1-q)],
```

and for the usual `q >= 1` it is bounded away from zero or even tends to one. More generally, for every fixed `q>0`, the volume of the interval grows like `exp(kappa d_c n)`, which dominates the displayed sublinear exponent. The integral of the **stated majorant** over the intermediate region is not `o(n^{-(3+d_c)/2})`.

The high-frequency polynomial line begins only after `exp(kappa n)`. The proof of the LLT nevertheless calls the intermediate contribution “exponentially or superpolynomially small.” That conclusion does not follow from the theorem just stated.

One could attempt to take the minimum with a direct coarea estimate valid throughout the intermediate region, but no such combined bound is stated or proved. Indeed, the zero-frequency contradiction above shows that the direct branch estimate cannot hold uniformly in the form claimed.

**Disposition for A2: reject.** The exact arithmetic family, the word decomposition, and the Fourier budget are not coherent. Consequently the mixed LLT exported to A3, A4, and D1 is unavailable.

---

### 3.5 A3: the entropy action uses the wrong clock

The exact relative-entropy representation for a controlled Markov chain stopped after `nu_N` transitions is

```text
(1/N) E sum_{k <= nu_N} H(q_k | K(h_{k-1},.)) .
```

It charges once per selected mark. With the paper's transition flow `Q_N`, the continuum cost must be integrated against the transition-count marginal of `Q`, not against the holding occupation `L`.

Instead (A3.16) defines

```text
A(q,L) = integral [q log q - q + 1] K(h,dm) L(ds,dh).
```

The measure `L_N` gives the `k`th state mass `R(m_k)/N`, so this weights the entropy of choosing mark `k` by its return length.

A one-line counterexample makes the discrepancy explicit. Suppose every mark has deterministic return length `R=r>1` and use the same controlled mark density at every transition, with one-step entropy `H`.

The stopping index is asymptotically `nu_N=N/r`. The exact normalized entropy is therefore

```text
(nu_N/N) H -> H/r.
```

But `L_N` has total mass

```text
sum_k R/N -> 1,
```

so (A3.16) assigns cost `H`.

The proposed rate is wrong by the factor `r` even in this elementary renewal chain. No topology or recession compactification can repair a wrong Radon measure in the action.

The same mismatch leaves the phrase “predictable kernels producing the state” undefined: `q` governs the transition law at the atoms of `Q`, while the action integrates it over the holding occupation `L`. A relation between the transition intensity, `Q`, and `L` is not supplied.

### 3.6 A3: the telescoping identity does not provide the advertised time-dependent balance

After division by `N`, equation (A3.8) has a time-derivative term multiplied by `1/N`, whereas the transition term is integrated against `Q_N`. In the limit the displayed identity imposes only the leading fast-chain stationarity relation

```text
integral Delta_m phi dQ = 0,
```

while the chronological derivative and endpoint terms vanish. It does not yield a first-order continuity equation in the scaled coordinate `s` for a general `s`-dependent controlled kernel.

That may be acceptable for a stationary empirical-flow LDP, but it is not the closed chronological balance claimed for the state in Theorem A3.18. A two-scale formulation or a windowed transition-flow identity is needed.

### 3.7 A3: the stopped local theorem assumes an overshoot factorization not derived from A2

A2 is a fixed-iterate local theorem. A3.22 asserts a random-time Markov-renewal local theorem with a factor

```text
Gaussian(x) * rho_H(o)
```

uniformly under source derivatives. In a lattice Markov renewal process, the terminal state and overshoot can retain arithmetic dependence on the lattice reward and on the central coordinate. A scalar overshoot law independent of `x_N` requires a separate terminal-state renewal theorem and aperiodicity statement.

The proof gives only a sentence about a simple renewal root. It does not construct the enlarged transfer operator, identify all peripheral renewal poles, or prove the claimed uniform asymptotic independence.

**Disposition for A3: reject.** The proposed LDP rate is already wrong in a deterministic-return example, and the random-stop local theorem is not supplied by A2.

---

### 3.8 A4: the graph-bounded observation loses one power in the vertical resolvent expansion

The memory theorem assumes

```text
B_Q : R -> D(L_Q^3),
C_Q : D(L_Q) -> R.
```

For `y=B_Q r`, the paper writes

```text
(z-L_Q)^(-1)y
 = z^(-1)y + z^(-2)L_Q y + z^(-3)L_Q^2 y
   + z^(-3)(z-L_Q)^(-1)L_Q^3 y.
```

This identity is fine in the Hilbert space. The problem appears after applying `C_Q`, which is bounded only in the graph norm.

On a vertical half-plane, exponential semigroup stability gives a uniform `H -> H` resolvent bound. It does **not** give a uniform `H -> D(L_Q)` graph-norm bound. Indeed

```text
L_Q(z-L_Q)^(-1)x = z(z-L_Q)^(-1)x - x,
```

so the graph norm can grow like `|z|`.

Consequently the final term is controlled only by

```text
|z|^(-3) * O(|z|) = O(|z|^(-2)),
```

under the stated hypotheses. The claimed operator remainder `O(|z|^{-3})` in (A4.20) requires an additional admissibility/smoothing estimate, or `C_Q` bounded on the Hilbert space itself. Neither is assumed.

### 3.9 A4: the compression perturbation is not a bounded perturbation on the semigroup space

Equation (A4.14) produces a perturbation `K` bounded from `D(L)` with graph norm into `H`. The proof then invokes “the bounded perturbation theorem” to obtain an exponentially stable semigroup.

The standard bounded perturbation theorem requires a bounded operator on the underlying Banach/Hilbert space. A graph-bounded perturbation is merely relatively bounded. Preservation of generation and the quantitative spectral bound requires a genuine relative-bound theorem and its hypotheses; it is not automatic from small graph norm.

Thus the orthogonal-dynamics decay used by the memory equation is not established by the displayed argument.

### 3.10 A4: arbitrary bounded base potentials are not covered by local perturbation at zero

The Feynman--Kac theorem first proves a small source ball around zero, then asserts that every bounded Holder potential has its own simple leading eigenvalue after changing to an equivalent Lyapunov weight. Bounded multiplication does not by itself preserve simplicity and isolation of the leading eigenvalue on a noncompact countable-state system. Large bounded potentials may create competing almost-invariant regions or close the spectral gap.

This unsupported global chart assertion is the sole input for C2's exposing-ray rigidity argument.

**Disposition for A4: reject.** The elementary renewal types are improved, but the compressed semigroup and the vertical memory asymptotics do not follow from the stated graph hypotheses.

---

### 3.11 B1: the universal momentum-energy anchor is impossible

The universal anchor certificate requires a finite family of minors with

```text
chi_l != 0  =>  |M_l| >= c_A > 0
```

at **every** anchor configuration in the support, uniformly over the exterior.

Consider the standard continuous conservation map carried by any exact momentum-energy preparation:

```text
P(v_1,...,v_m) = sum_i v_i,
E(v_1,...,v_m) = (1/2) sum_i |v_i|^2.
```

At an anchor configuration with

```text
v_1 = ... = v_m = v,
```

the differential satisfies

```text
dE = v . dP.
```

The energy row is a linear combination of the three momentum rows. The momentum-energy derivative has rank at most three rather than four. No maximal minor in these four constraint directions can be bounded below.

These equal-velocity configurations are interior points of the Maxwellian velocity support. Hard-core boundary charts concern positions and do not restore the missing velocity rank. A finite compact subcover cannot create rank at a point where the derivative is singular.

The rank-deficient set may have measure zero, but the paper claims a configurationwise uniform lower bound and a uniform zero-extended `W^{s,1}` density. Handling a neighbourhood of the rank-deficient set requires a separate quantitative singular-coarea estimate; it cannot be assigned to one of the same full-rank anchors.

Therefore Lemma B1.8 and the exceptional-component smoothing theorem do not follow. The nonintegrable exceptional Fourier problem remains unresolved.

### 3.12 B1: conditioning on an event can destroy anchor smoothness

The proof of B1.10 says that the anchor density is applied “after the event has been resolved.” Unless the good-block event is measurable with respect to the non-anchor variables alone, multiplying the anchor density by the event indicator introduces discontinuous anchor-dependent boundaries and destroys the `W^{s,1}` estimate.

The source does not exclude anchor variables from every good-block test or prove boundary-flat approximation with uniform derivatives. This is a second independent gap in the exceptional-event argument.

**Disposition for B1: reject.** The new anchor mechanism is false on the momentum-energy rank-degenerate set.

---

### 3.13 B2: the radius-loss Duhamel estimate does not follow from the creation bound

The only analytic-scale input is

```text
||C_t K||_{a'} <= C/(a-a') ||K||_a.
```

The paper claims that iteration yields

```text
||T_t K - T_t K~||_{a'}
 <= exp(Ct/(a-a')) ||K-K~||_a
```

for arbitrary `t`.

This is not a valid consequence of a Cauchy radius-loss estimate. Divide the total radius loss `a-a'` among `n` insertions. Each insertion costs order `n/(a-a')`, so the `n`th term is bounded by

```text
(C n/(a-a'))^n * t^n/n!.
```

Since `n^n/n!` is exponentially large, the resulting series has a finite time radius comparable with `a-a'`; it does not sum to the asserted entire exponential.

The standard counterexample is the derivative operator on analytic functions. On sup-norm spaces of functions analytic in a disk,

```text
||partial_z f||_{a'} <= C/(a-a') ||f||_a,
```

but its evolution is translation,

```text
e^{t partial_z} f(z) = f(z+t),
```

which is not bounded from radius `a` to radius `a'` once `t >= a-a'`.

Thus B2.17 requires a special structural estimate beyond B2.15. None is proved. The finite-time propagation, connected logarithm, pressure, B3 revealment bounds, and B4 core all depend on this invalid step.

### 3.14 B2: the pivot certificate assumes the hard rank theorem

The source introduces a “pivot certificate” containing:

- a causal right inverse of the full tree-contact derivative;
- tangent vector fields preserving every tree contact;
- exact triangular vanishing for later pivots;
- and a diagonal lower bound for every surplus closure.

Those are precisely the difficult geometric conclusions. Unlike the A2 section, B2 gives no nonemptiness or construction theorem showing that every hard-sphere genealogy entering the expansion admits such a certificate. The proof of the rank lemma simply restates the certificate.

The revision therefore replaces the previous invalid shear by an unverified finite datum that already contains the desired rank. Conditional theorems on a certified chart are legitimate, but they do not prove that the actual collision-history expansion is covered by such charts.

### 3.15 B2: the exact coarea power and LDP remain proof sketches

Even assuming local pivots, the passage from one surplus contact to a multiplicative `epsilon^{alpha_K s(G)}` bound over all nested genealogies requires:

- compatible chart changes after each contact;
- uniform control of pivot flows and their domains;
- label sums;
- simultaneous-contact strata;
- and a summable graphwise majorant.

The manuscript gives one paragraph. It does not establish these estimates at the level needed by the projective pressure and LDP.

**Disposition for B2: reject.** The analytic-scale evolution is invalid as written and the loop-rank theorem is assumed rather than proved.

---

### 3.16 B3: root revealment does not yield an arbitrary stopping-time modulus

The stopping time in Lemma B3.13 belongs to the natural empirical/history filtration. The proof then switches to a different filtration: deterministic revealment of initial roots. It applies Efron--Stein and says that changing root `j` affects the random interval only through the cluster containing that root because the interval indicator is predictable.

That is false. The stopping time itself is a function of all root variables. Resampling root `j` can move the stopping time from `tau` to `tau'`. The increment interval changes from

```text
[tau,tau+h]
```

to

```text
[tau',tau'+h].
```

Contributions from many other roots may lie in the symmetric difference of those intervals. Their influence is not confined to the cluster containing root `j`.

Predictability with respect to the temporal empirical filtration does not imply measurability with respect to the root-revealment sigma-field before root `j` is revealed. A simple discrete analogue already fails: let a stopping time equal time 1 or time `T` according to the first root. Replacing that root moves the observation window and changes all variables sampled in the window.

A valid Aldous estimate needs a conditional future-increment theorem or a martingale decomposition adapted to the temporal filtration. The revealment estimate supplied here is insufficient.

### 3.17 B3: Efron--Stein controls variance, not the full stopped increment claimed

The centered fluctuation field is not itself a martingale; it has a transport and collision drift. Efron--Stein bounds the variance of a functional of the roots. Lemma B3.13 is a bound on the full second moment of a random-time increment. The proof does not separately control its conditional mean or drift uniformly at stopping times.

The higher conditional cumulant claim is even further removed from Efron--Stein and is not proved by the single-cluster sentence.

### 3.18 B3: the process theorem imports unproved B2 pressure derivatives

The finite-dimensional cumulants and covariance in B3.17 rely on the B2 pressure and finite-time kernel propagation, both of which fail above. Consequently even a repaired stopping-time argument would lack its root input.

**Disposition for B3: reject.** The contact-cycle correction is conceptually right, but the process-tightness mechanism is invalid for random stopping times.

---

### 3.19 B4: bounded entropy and bounded energy do not imply `W_2` compactness

Lemma B4.7 and Theorem B4.8 claim that a bound on relative entropy with respect to a Gaussian, together with a bound on the second moment, makes second moments uniformly integrable.

This is false. Let `M` be a centered Gaussian on velocity space. Let `M_R` be its translate by `R e_1`, put `p_R=R^{-2}`, and define

```text
f_R = (1-p_R) M + p_R M_R.
```

By convexity of relative entropy,

```text
H(f_R | M)
 <= p_R H(M_R | M)
 = p_R R^2/2
 = 1/2.
```

The second moment is also uniformly bounded:

```text
integral |v|^2 df_R = integral |v|^2 dM + O(1).
```

But the second-moment tail does not vanish uniformly:

```text
integral_{|v|>R/2} |v|^2 df_R >= c > 0.
```

Thus the family is not uniformly square-integrable and has no `W_2`-convergent subsequence. The entropy inequality used in the proof necessarily leaves a fixed term proportional to the entropy bound; it cannot make the tail tend to zero.

This directly contradicts:

- the last sentence of Lemma B4.7;
- the compactness theorem B4.8;
- and the assertion that the shell `K_{E,H}` in B4.15 is compact.

### 3.20 B4: strong continuity fails on the full unbounded-energy state space

The semigroup is declared strongly continuous on `BUC(X_E)`, where `X_E` contains all finite-second-moment states with no common energy bound.

Take the spatial torus and the bounded Lipschitz observable

```text
phi(f) = integral cos(2 pi x_1) df.
```

For each small `t`, choose a monokinetic state concentrated at position zero and velocity `v_t=(1/(2t),0,0)`. Its collision rate is zero because all velocities coincide, so its only admissible zero-cost evolution is free transport. At time `t` the position has shifted by one half-period, and

```text
phi(f_0)=1,
phi(f_t)=-1.
```

Hence

```text
sup_{x in X_E} |V_t phi(x)-phi(x)| >= 2
```

for arbitrarily small `t`. Strong continuity in the global sup norm fails. A valid theorem must be restricted to a common energy shell or use a weighted topology.

### 3.21 B4: the comparison proof uses a noncompact shell

The doubled-variable argument explicitly relies on compactness of `K_{E,H}`. The counterexample above shows that this set is not compact in `W_2`. Therefore the maximizing pairs need not remain in a compact set, and the viscosity comparison proof does not start.

**Disposition for B4: reject.** The preparation/running-action factorization is repaired, but the compact state space and strong-continuity claims remain false.

---

### 3.22 C1: the countable-stratum density is not normalized

The paper defines

```text
nu = sum_s 2^{-|s|} nu_s,
```

and on stratum `E_s`

```text
g(x,y) = 2^{|s|} rho_s(y-O_s(x))/q_s(y).
```

Since `nu_s=q_s m_s`, the contribution of **each** active stratum is

```text
integral_{E_s} g(x,y) nu(dy)
 = integral rho_s(z) m_s(dz)
 = 1.
```

Summing over strata gives the number of active strata, and gives infinity for a countably infinite family. The factors `2^{-|s|}` and `2^{|s|}` cancel stratum by stratum.

Proposition C1.3 proves normalization on one stratum and then incorrectly concludes normalization on the disjoint union. A valid model needs explicit stratum-selection probabilities `p_s(x,a,theta)` whose sum is one, or it must declare that exactly one stratum is active in each experiment. Neither appears in the source.

This is a direct contradiction in the probability kernel from which every filter, likelihood, LAN, and BvM statement is derived.

### 3.23 C1: deterministic prediction plus common likelihood does not contract Hilbert projective distance

The derivative-filter theorem claims that positive upper and lower likelihood bounds give a strict Hilbert-projective contraction over a fixed number of observations.

For deterministic bijective hidden dynamics this is false. Let two priors have positive densities `p` and `q` on a finite hidden state space. Under a deterministic permutation followed by multiplication by the same positive observation likelihood `l_y`, the posterior ratio is

```text
p'(x)/q'(x) = constant * p(Phi^{-1}x)/q(Phi^{-1}x).
```

The maximum-to-minimum ratio is unchanged. Therefore the Hilbert projective distance is exactly preserved, not strictly contracted. The identity hidden dynamics is the simplest example.

Strict Birkhoff contraction requires a genuinely positive integral transition kernel mixing all hidden states, or another observability mechanism over a controlled sequence. Uniform upper and lower observation densities alone do not supply it.

Thus Theorem C1.8(iii), the “contracting homogeneous part” of the derivative recursion, and the claimed summable LAN remainder are not established.

### 3.24 C1: the negative-Sobolev chart is not defined on the advertised hidden states

The text chooses `r > dim X/2+4` on every smooth hidden chart. The hidden states imported from A3 and B2 include complete histories, stopped graph currents, and projective kernel coordinates. These are generally infinite-dimensional Polish spaces, not finite-dimensional manifolds with a Sobolev dimension.

Moreover the vector field formula uses `(Phi_theta^a)^{-1}`, although no invertibility is assumed for the controlled hidden map. The push-forward derivative lemma may be valid for a smooth finite-dimensional diffeomorphism, but it is not a theorem on the actual hidden spaces advertised by the dossier.

### 3.25 C1: global signal separation does not by itself identify a hidden mixture

Condition C1.13 compares signal maps at the **same hidden point**. Under two parameters the hidden state distribution and filter are different. A parameter change can be compensated by a symmetry or relabelling of hidden states, making the observation mixture identical even when pointwise signal values differ at the same coordinate.

Uniform tests require separation of the induced observation laws over the reachable belief class, not only pointwise separation of deterministic signal maps.

**Disposition for C1: reject.** The observation kernel is not a probability kernel as written, and the key filtering contraction is false for deterministic dynamics.

---

### 3.26 C2: the discrete likelihood uses the wrong filter

For a hidden model, the predictive density under parameter `theta` is computed from the filter generated recursively under `theta`. The correct likelihood ratio is

```text
L_n = product_k
      r_theta(Pi_{k-1}^theta,A_k,Y_k)
      / r_theta0(Pi_{k-1}^{theta0},A_k,Y_k).
```

Equation C2.12 uses one common `Pi_{k-1}` in numerator and denominator. Already after the first observation, `Pi_1^theta` and `Pi_1^{theta0}` are generally different. At the second observation the displayed product is therefore not the Radon--Nikodym derivative.

This is not a notational detail: the derivative of the filter is a central term in the score and observed information. The discrete likelihood proposition is false as written.

### 3.27 C2: the optional-projection theorem assumes too little for filter convergence

Weak convergence of hidden and observation kernels on a cylinder core, path tightness, and moment bounds do not in general imply convergence of nonlinear filters or optional projections. Filtering can be unstable under weak model convergence when observation laws become nearly singular or when conditional independence structures change.

The proof says that “core convergence identifies every subsequential filter limit,” but no uniqueness theorem for the limiting filter martingale problem is stated. The continuation kernels under adaptive controls are also not defined as a compact continuous family.

Thus C2.11 remains a programme statement rather than a theorem proved from the listed assumptions.

### 3.28 C2: pressure localization imports an unavailable A4 theorem

C2 assumes A4 supplies a simple analytic leading projection around every finite bounded exposing potential. A4 establishes only a small source theorem near zero and then asserts the arbitrary-base-potential extension without proof. Therefore the equilibrium states used in C2.7 do not exist by any established upstream result.

### 3.29 C2: the Brownian statement is separated, but the BSDE corollary is still blanket

The three likelihood propositions now distinguish discrete, point-process, and Brownian channels. The final BSDE corollary nevertheless states a common stability result under broad “appropriate characteristics” without specifying the filtration, martingale representation property, jump integrand space, or comparison conditions for each channel. Terminal and driver convergence are necessary but not sufficient for the claimed joint convergence across these different stochastic bases.

**Disposition for C2: reject.** The strict-duality lemma may be separable, but the likelihood and optional-projection package is not established.

---

### 3.30 D1: the lattice summation power has the wrong sign

Equation D1.2 is a local mass/density at one lattice value. In an ordinary phase cell containing the lattice minimizer, one must **sum** over all central lattice values. There are order `N^{d_Z/2}` such values in a square-root neighbourhood.

A single central lattice probability has the local factor `N^{-d_Z/2}`. Summing the Gaussian lattice profile cancels that factor. It does not create another `N^{-d_Z/2}`.

Nevertheless D1.4 sets

```text
kappa_j = lambda_j + (d_R-r_j)/2 + d_Z/2,
```

and the proof says that the “Gaussian sum supplies ... `N^{-d_Z/2}`.” This is backwards for a summed phase cell.

The elementary symmetric random-walk example is decisive. For a one-dimensional centered walk,

```text
P(S_N=k) ~ N^{-1/2} phi(k/sqrt N).
```

Summing over all central `k` gives probability tending to one, not `N^{-1/2}`. If the intended event pins an exact lattice value, the theorem must state exact lattice conditioning rather than a phase cell and must not perform a lattice sum.

### 3.31 D1: the assumed local expansion is not an upstream export

D1.2 assumes a `C^6` labelled expansion through order `N^{-1}` with four uniform derivatives. The active A2 and B1 theorems provide only a leading Gaussian factor with relative error `O(N^{-1/2})` and two source derivatives. They do not provide:

- a labelled phase local density;
- an `N^{-1}` Edgeworth coefficient;
- four source derivatives;
- a full off-central rate `I_j(k/N,y)`;
- or uniformity over strategic measures.

D1 therefore begins by assuming a theorem strictly stronger than the declared upstream interfaces. The dependency ledger is inaccurate at this node.

### 3.32 D1: the final Gaussian variable is scaled inconsistently

The source defines

```text
xi_N=(K_N,Y_N),  K_N in Z^{d_Z},
```

and uses the rate at `K_N/N`. The final coexistence statement writes

```text
sqrt N (xi_N - m_{J_N}).
```

If `K_N` is the raw additive lattice variable, the correct central scaling is

```text
(K_N-Nm_j)/sqrt N
```

or equivalently `sqrt N(K_N/N-m_j)`, not `sqrt N(K_N-m_j)`. The current formula is dimensionally inconsistent unless `xi_N` is silently redefined as normalized, contrary to D1.1 and D1.2.

### 3.33 D1: the policy expansion is assumed rather than derived

The “uniform controlled finite-dimensional expansion” is justified by saying that a compact strategic-measure space maps into a compact parameter set of the upstream local theorem. Adaptive policies do not merely choose a static source parameter: they change the path law recursively and correlate actions with observations. Compactness of policy laws does not automatically turn A2/B1's deterministic-source LLT into a uniform adaptive-policy Edgeworth expansion.

The epi-development (E1)--(E3) then assumes precisely the uniform near-maximizer control needed for the subleading theorem. The result is a conditional lexicographic lemma, not a mechanical phase-control theorem.

**Disposition for D1: reject.** The phase coefficient has a direct lattice-power error and relies on local inputs not proved upstream.

---

## 4. Paper-by-paper editorial assessment

| Paper | Recommendation | Principal reason |
|---|---|---|
| A1 | Reject | Covariance derivatives leave the base current Hilbert space, so trace-norm response on that space is not typed. |
| A2 | Reject | Nonarithmeticity is falsely declared open; the all-frequency estimate does not provide the LLT Fourier budget and conflicts with the untwisted operator when used at `b=0`. |
| A3 | Reject | Relative entropy is integrated against holding occupation rather than transition count; the rate is wrong even for constant return length. |
| A4 | Reject | Compression generation and the `O(|z|^{-3})` memory remainder do not follow from graph-bounded coupling assumptions. |
| B1 | Reject | A uniform full-rank momentum-energy anchor cannot exist on equal-velocity configurations. |
| B2 | Reject | The radius-loss Duhamel estimate is invalid from the stated Cauchy bound, and the pivot rank is assumed as a certificate. |
| B3 | Reject | Root revealment does not control arbitrary temporal stopping times; the process CLT lacks tightness. |
| B4 | Reject | Entropy-energy shells are not `W_2` compact; strong continuity fails globally. |
| C1 | Reject | The countable-stratum observation kernel has total mass equal to the number of strata, and deterministic Bayes updates do not strictly contract projective distance. |
| C2 | Reject | The discrete likelihood uses a common rather than parameter-specific filter; optional projection convergence is unsupported. |
| D1 | Reject | The lattice Laplace power is wrong and the required higher-order local theorem is not exported upstream. |

No paper is ready for publication in its present form. A1's loss-indexed current idea and C2's weighted strict-duality lemma may contain material that could be developed separately, but neither is presently embedded in a correct full theorem package.

---

## 5. Dependency-level consequences

The repository's directed graph is formally acyclic. The mathematical exports are not available.

### 5.1 Billiard chain

- A2 does not establish the claimed uniform family or the noncentral Fourier integral.
- A3 therefore lacks the stopped local theorem; independently, its path LDP has the wrong entropy action.
- A4 imports A3's unproved drift/state and contains independent compression and resolvent errors.

Consequently the Sinai pressure, conditioning, memory, observation, and phase interfaces used by C1, C2, and D1 do not exist at the claimed level.

### 5.2 Hard-sphere chain

- B2 lacks a valid analytic-radius evolution and a proved all-graph pivot theorem.
- B1 therefore lacks its grand-canonical conditional input and independently fails at the universal anchor.
- B3 has no valid stopped-process tightness mechanism.
- B4's action shells are not compact and its global semigroup is not strongly continuous.

Consequently the hard-sphere LDP, process covariance, nonlinear semigroup, filtering, and phase inputs are unavailable.

### 5.3 Synthesis chain

- C1's observation kernel is not normalized, so there is no probability experiment to filter.
- C2's likelihood is not the Radon--Nikodym derivative of the two hidden models.
- D1 assumes an unproved local expansion and applies an incorrect lattice summation.

The downstream papers therefore cannot be rescued by accepting the ledgers as interfaces.

---

## 6. Significance, novelty, and presentation

The dossier remains written as a collection of compressed research programmes. New named mechanisms—“Jacobian-weighted finite grammar,” “two-clock telescoping current complex,” “universal coarea anchor,” “disintegrated kernel category,” “orthogonal cycle-normal splitting,” and “positive-support epi-argmax”—are potentially useful organizational ideas. A name and a one-paragraph proof do not establish the hard theorem.

At the top-journal level, the following steps require full papers or substantial sections:

- construction of a concrete billiard family satisfying the exact arithmetic and all-frequency operator conditions;
- anisotropic stable-curve estimates through the claimed derivative order;
- a Markov-renewal local theorem at random stopping with terminal overshoot;
- a complete Polish state and correctly normalized entropy-control LDP;
- all-graph hard-sphere loop rank and radius-loss propagation;
- conditional stopping-time cumulants for deterministic hard spheres;
- compactness and viscosity comparison on the actual kinetic state space;
- recursive differentiability and testing for adaptive hidden models;
- and uniform controlled Edgeworth/Morse--Bott expansions.

The current sources repeatedly state one of these as a certificate, an assumption, or a sentence invoking a standard theorem. Several such sentences contain the direct errors above.

The literature interfaces also remain inadequate. A precise submission must state exactly which known anisotropic, Dolgopyat, hard-sphere cluster, hypocoercive, filtering, nonlinear-semigroup, or Bernstein--von Mises theorem is imported and verify every hypothesis on the actual spaces used here.

---

## 7. Minimum requirements for a scientifically meaningful future submission

A further simultaneous eleven-paper rewrite is not the appropriate next step.

1. **Choose one root theorem.** Submit either A2 or B2 as a self-contained specialist paper.
2. **For A1, keep all response derivatives on a declared scale.** Do not claim trace-norm differentiability on the base space unless the derivative remains in that space.
3. **For A2, remove the false openness claim.** Define a fixed exact arithmetic class, and prove a Fourier estimate whose integrated noncentral bound is explicitly `o(n^{-d/2})`.
4. **Resolve the `b=0` contradiction.** Separate return-time layer estimates from iterate estimates and state precisely where oscillatory cancellation begins.
5. **For A3, derive the entropy representation before defining the rate.** Charge KL against transition count, not holding time, and provide the exact relation among `Q`, `L`, and the controlled kernel.
6. **For A4, prove the compressed generator theorem with a valid relative-perturbation result.** Add the admissibility estimate needed to apply a graph-bounded observation to the vertical resolvent.
7. **For B1, replace the universal full-rank anchor.** Stratify or quantitatively control the rank-degenerate momentum-energy set; a uniform minor on the entire support is impossible.
8. **For B2, prove the analytic-radius evolution with correct time loss.** Construct the pivot fields for every graph rather than including their rank in a certificate.
9. **For B3, work in the temporal filtration.** A valid Aldous estimate must account for movement of the stopping time under changes of the initial roots.
10. **For B4, add genuine de la Vallee--Poussin control beyond quadratic energy.** Entropy relative to a Gaussian plus a second-moment bound does not imply `W_2` compactness. Restrict strong continuity to common energy shells.
11. **For C1, define stratum-selection probabilities.** Verify that the full observation kernel integrates to one. Do not claim projective contraction from deterministic dynamics plus diagonal likelihood multiplication.
12. **For C2, use parameter-specific filters in every likelihood.** State a separate, complete filter-stability theorem before optional projections or BSDE limits.
13. **For D1, distinguish exact lattice conditioning from summation over a phase cell.** Correct the polynomial exponent and the normalization of the Gaussian variable.
14. **Do not import an Edgeworth theorem that upstream papers do not prove.** Either prove the full higher-order local expansion or reduce the phase conclusion.
15. **Obtain independent specialist review of each root area.** Billiards, hard-sphere dynamics, kinetic process limits, filtering/statistics, and nonlinear semigroups require distinct expertise.

These are reconstruction requirements, not a finite major-revision checklist.

---

## 8. Final verdict

Round Twenty Nine is a real and responsive source revision. It fixes several earlier formulas and improves repository source discipline.

It is not a mathematical closure. The active sources contain direct counterexamples to central statements:

- A1's trace-norm covariance response is incompatible with its own derivative loss;
- A2's exact arithmetic condition is not open, its word estimates conflict with the untwisted operator when combined as written, and its intermediate-frequency majorant does not close Fourier inversion;
- A3's entropy action is integrated against the wrong clock;
- A4's graph-domain resolvent does not yield the claimed remainder;
- B1's universal momentum-energy anchor loses rank at equal velocities;
- B2's radius-loss evolution is false from the stated bound;
- B3's revealment argument does not control a stopping time that moves when a root is replaced;
- B4's entropy-energy shell is not `W_2` compact and its global semigroup is not strongly continuous;
- C1's countable-stratum observation density is not normalized and its deterministic filter does not strictly contract Hilbert distance;
- C2's discrete likelihood uses the wrong filter;
- and D1's lattice phase power is reversed and its local input is not proved upstream.

These defects occur at the root nodes and propagate through the declared dependency graph. Compilation, source hashes, theorem labels, and regression tokens do not change that conclusion.

**Recommendation to the editor: reject all eleven manuscripts and do not invite another dossier-wide major revision. Any future submission should be a substantially reconstructed, self-contained root paper with complete proofs and an independently verified model class.**
