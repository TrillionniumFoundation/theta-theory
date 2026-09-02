# External Referee Report on the Round-Twenty-Seven Revision

## Recommendation: **Reject all eleven manuscripts; do not invite another major revision of the dossier**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round27-referee-positive-closure-11paper-2026-09-02`  
**Pre-review head:** `31d955aad5cff5c8edba00bfb9e500a87fd3ba72`  
**Review branch:** `review/round28-gpt56-pro-harsh-11paper-2026-09-02`  
**Review date:** 2 September 2026  
**Scope:** the eleven active `ROUND27_POSITIVE_CLOSURE.tex` files and wrappers, `AUTHOR_RESPONSE_ROUND26.md`, the Round-Twenty-Seven review index and dependency ledger, and the committed verification record.

This report applies the standard of correctness, self-containedness, significance, and presentation expected at *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, or *Acta Mathematica*.

Round Twenty Seven is a genuine source revision. Unlike the nominal Round-Twenty-Five branch, it contains new active mathematical files, switches all eleven wrappers, supplies an author response, and records clean builds. The source-of-truth problem identified in the preceding report has therefore been addressed at the repository level.

The mathematical conclusion is nevertheless negative. Several replacement statements are false as written, several displayed constructions are not well typed, and several arguments solve an earlier objection only by quotienting away the physical variable that the paper still claims to study. The most serious defects can be checked directly from the submitted definitions and do not depend on specialist disagreement about the literature.

The principal direct contradictions are:

1. A1 sends distributional parameter derivatives in the wrong direction on its Sobolev-dual scale, and its alleged polygonal process is a step process that is not a random element of `C([0,1];J)`.
2. A2's certificate estimate is impossible at derivative order zero because it contains an unweighted sum of inverse-branch `C^2` norms bounded by `Ce^{-cn}`. Its continuous-character argument is also false for the explicitly allowed case `d_c=2`.
3. A3's history-balance identity fails even for a test depending only on the chronological coordinate. Its collision-stopped path is evaluated on the wrong physical-time interval, and its stopped return sum cannot have the claimed nondegenerate square-root Gaussian scale.
4. A4's capped distance makes its weighted Lipschitz space incompatible with the unbounded weights and Feynman--Kac sources used immediately afterward. Its power drift does not follow from the A3 moment bound, and its renewal/compression/sectorial claims remain unproved or ill defined.
5. B1's exceptional high-frequency argument assumes a reserved good block precisely on the event on which there may be no good block. Its final coefficient formula also contains an undefined index.
6. B2's fibre-product operation is not defined for arbitrary measures in the stated Banach space; the automorphism normalization is misstated; and the proposed subtree shear generally leaves the tree-contact constraint manifold rather than providing a coordinate on it.
7. B3 removes `ker C` by quotienting, but nonzero contact defects in `ker C` have positive entropy cost and are visible in the joint contact current. The quotient therefore changes the Hessian and the claimed joint fluctuation theory. Its localization proof also has the wrong commutator scaling.
8. B4 defines a path cost that includes the initial entropy and then calls the resulting value operators a semigroup. Already at time zero the identity axiom fails, and concatenation double-counts preparation. Its asserted exponential superquadratic moment is infinite under the Gaussian velocity tails assumed upstream.
9. C1's translated-noise density is not a density with respect to its claimed fixed probability envelope. It also differentiates deterministic push-forwards of Dirac measures in a signed-measure norm in which they are not even continuous.
10. C2 assumes a continuous weight with compact sublevels on state spaces advertised as genuinely non-locally compact; that assumption itself supplies relatively compact neighborhoods and therefore excludes the stated platforms. Its Brownian innovation theorem does not match C1's general discrete/surface/noisy observation model.
11. D1 invokes a joint local theorem not proved by A2 or B1, defines component rates circularly, ignores phases with zero prior weight in its leading maximum, and proposes Morse--Bott integration over a policy manifold in a problem containing a supremum rather than an integral over policies.

Each of these points is developed below.

---

## 1. Confidential recommendation to the editor

I recommend **rejection of the entire eleven-paper submission, without another major-revision invitation for this dossier**.

The revision is more responsive and better organized than the earlier versions. In particular, it correctly abandons several disproved mechanisms: exact-tail Doeblin minorization, the old regular-point residue, the old unnormalised exact-number pressure, the old collision Hessian, noiseless smooth observation kernels, and the claim that a scalar max-plus leading order preserves shared control.

Those improvements do not bring the manuscripts near the top-journal threshold. New direct contradictions appear in the active source. Some are elementary type or scaling errors; others concern precisely the root estimates on which all downstream papers depend. The active source files are only five to seven pages each while claiming theorem packages that would ordinarily require substantial independent papers. At crucial points the text still replaces the hard theorem by a sentence saying that a certificate, compactness argument, cut algebra, pressure theorem, or standard multiplier supplies the desired conclusion.

This is not a finite list of polishing requests. A valid future submission would need to isolate one root theorem, give complete definitions and proofs, and survive specialist review before any downstream synthesis is considered.

---

## 2. Source identity, build status, and what the revision genuinely fixes

### 2.1 Source identity

The reviewed revision is one commit ahead of the Round-Twenty-Six review branch. It adds eleven active `ROUND27_POSITIVE_CLOSURE.tex` files, eleven standalone wrappers, a common preamble, a response, a dependency ledger, a verifier, and a CI workflow. The active `main.tex` files point to the Round-Twenty-Seven wrappers.

The review baseline is therefore unambiguous:

```text
revision/round27-referee-positive-closure-11paper-2026-09-02
31d955aad5cff5c8edba00bfb9e500a87fd3ba72
```

### 2.2 Build status

The committed verification record reports successful source checks, eleven individual builds, and a 49-page combined dossier. I do not dispute those repository facts.

Compilation establishes only that TeX accepts the files. It does not establish that:

- a dual Sobolev derivative has the displayed direction;
- a stochastic process actually belongs to the asserted path space;
- a branch certificate is nonempty;
- a fibre product of arbitrary measures is defined;
- an exceptional Fourier contribution remains integrable;
- a quotient preserves a physical rate function;
- an initial-cost value family has the semigroup identity;
- a translated probability density is normalized against a fixed envelope;
- or a supremum over controls can be treated by Laplace integration over the control set.

### 2.3 Genuine corrections

The following changes are mathematically sensible in intent:

- A3 uses conditional-reference cell recovery rather than singular representative atoms.
- A4 retains the generic `z^{-1}` memory coefficient and no longer uses a residue at a holomorphic point.
- B1 separates probability normalization from absolute free energy.
- B3 recognizes the existence of a large collision-to-density kernel.
- C1 adds independent measurement noise.
- D1 acknowledges the phase-blind nature of the scalar leading max-plus value.

The problem is that several proposed replacements are themselves incorrect.

---

## 3. Decisive direct counterexamples and type failures

### 3.1 A1: the current derivative runs in the wrong Sobolev direction

A1 defines

```text
Phi^s  = positive tests of Sobolev order s + codimension + 2,
J^s    = (Phi^s)'.
```

As `s` increases, `Phi^s` becomes smaller and its dual `J^s` becomes larger, allowing more singular distributions. A distributional derivative therefore moves from `J^s` toward a space such as `J^{s+1}` or `J^{s+2}`, not toward the smaller and more regular dual `J^{s-2}`.

The submitted lemma instead states

```text
nabla_a : J^{m+2r} -> J^{m+2r-2}.
```

This reverses the standard duality. The elementary model is a delta current on a line: differentiating it gives a derivative of delta, which requires more negative Sobolev regularity, not less. Transposing a test operator that consumes derivatives has the same direction.

The coherent jets then place the `j`th derivative in `J^{m+2r-2j}`, repeating the same reversed scale throughout the response theorem. Thus the central typed repair of A1 is itself mistyped.

### 3.2 A1: the asserted `C([0,1])` process is not continuous

A1 calls

```text
W_n(t)=n^{-1/2} sum_{k<nt} Y_k
```

a polygonal process and asserts convergence in

```text
C([0,1];J^m).
```

The displayed process is a step function with jumps at multiples of `1/n`. Unless every increment vanishes, it is not an element of `C([0,1];J^m)`. A fractional interpolation term is missing. One may prove convergence in `D`, or add a genuine polygonal interpolation and then prove that the interpolation error is negligible, but the theorem as written is not a statement in the claimed space.

### 3.3 A2: the branch certificate is empty as written

Certificate (C1) requires, for `0 <= j <= r_*+2`,

```text
sum_{h:R(h)=n} [
  ||J_h||_{C^j}
  + ||J_h||_{C^j} ||tau_h||_{C^{j+2}}
  + ||partial_a^j h||_{C^2}
] <= C e^{-cn}.
```

At `j=0`, the last term is the unweighted `C^2` norm of the inverse branch itself. A usual `C^2` norm includes the zero-order norm. Whenever a return layer contains a branch, that norm is not forced to tend to zero like `e^{-cn}`; indeed it is coordinate dependent and generally of order one. Even if one silently replaced the norm by a derivative seminorm, no Jacobian weight controls the countable branch sum.

The proposition claiming a nonempty certificate class does not address this term. It describes a few periodic corridors and blocking scatterers, but it does not prove the countable high-order branch estimate or the terminal nonstationarity requirement for every bad branch. Hence the root class used by the entire A-chain has not been shown to contain a single billiard.

### 3.4 A2: two roof vectors do not kill all characters in `R^2`

The source explicitly permits `1 <= d_c <= 2`. It then uses two roof differences `beta_1,beta_2` to conclude that the generated closed subgroup contains all of `R^{d_c}` and that every continuous character vanishes.

For `d_c=2`, the integer span of two vectors is at most a lattice in `R^2` when the vectors are independent. Its annihilator is the nonzero dual lattice. If they are dependent, the generated subgroup is even smaller. A Diophantine lower bound on integer combinations of the two vectors does not change this fact.

Thus the exact annihilator theorem is false in an explicitly included case. To obtain a dense subgroup of `R^2`, additional incommensurate generators and a correctly formulated character theorem are required.

### 3.5 A3: the submitted history-balance equation is false

A3 imposes

```text
int [phi(U(h,m))-phi(h)] dQ
  = int partial_s phi_s(h) d ell(s,h).
```

Take a test depending only on the chronological coordinate, `phi_s(h)=psi(s)`. Then the left side is identically zero, while the right side is

```text
int psi'(s) d ell(s,h),
```

which is not generally zero. This already contradicts the equation.

The exact finite-word telescoping identity must include the chronological increment `R(m)/N`, the appropriate occupation measure, and boundary terms. The current formula omits that structure. Since the rate function is defined on states satisfying this false balance identity, the path LDP is not correctly formulated.

### 3.6 A3: the collision-stopped path uses the wrong time interval

Each completed excursion graph has physical duration `tau(m)`. Their concatenation is therefore defined on

```text
[0, sum_{k<=nu_N} tau(m_k)].
```

For collision stopping, the source defines

```text
Gamma_N(t)=Cat(G_{m_1},...,G_{m_nu})(N t), 0<=t<=1.
```

There is no assumption that the total physical duration is at least `N`. Time units can be chosen so that the mean free-flight duration is below one; then `N t` leaves the domain of the concatenated path for large `t`. The correct collision-clock graph parametrization must use collision index or normalize by the actual physical clock. The displayed state is not defined on all legal words.

### 3.7 A3: the stopped return sum is not a nondegenerate Gaussian coordinate

The stopping time is

```text
nu_N = inf{k:S_k R >= N}.
```

Consequently

```text
S_{nu_N}R - N
```

is an overshoot, typically tight or at the return-tail scale, not a variable with variance of order `N`. A3 nevertheless places `S_{nu_N}R` together with `nu_N`, homology, and roof in a vector said to have one joint Gaussian square-root scale and a nondegenerate stopped saddle.

That cannot be correct. The stopped return coordinate is pinned to `N` up to overshoot and is asymptotically degenerate at square-root scale. A valid renewal local theorem must separate the renewal count, the pinned clock, and the overshoot law.

### 3.8 A4: the power drift does not follow from the imported moment estimate

A4 sets

```text
V(h)=1+sum rho^j chi(m_{-j}),
W(h)=exp(epsilon V(h)).
```

After one append/shift step,

```text
V(U(h,m)) = constant + rho V(h) + rho chi(m).
```

A3 supplies only a conditional exponential-mark bound of the form

```text
int exp(eta chi(m)) K(h,dm) <= C W(h).
```

Using that estimate yields at best a factor comparable to `W(h)^{rho+1}`, not `W(h)^alpha` with `alpha<1`. A4 simply states the power drift `PW <= C W^alpha` without supplying the stronger conditional exponent needed for it.

Since the weak-Harris and Feynman--Kac arguments both use this power drift, the gap is structural.

### 3.9 A4: the capped distance is incompatible with its weighted function space

A4 defines `d_* <= 1` and the seminorm

```text
sup_{h != h'} |f(h)-f(h')| / d_*(h,h').
```

Because the denominator is globally at most one, finite seminorm implies globally bounded oscillation:

```text
|f(h)-f(h_0)| <= Lip(f)
```

for every `h`. Thus functions in the space are bounded up to an additive constant. The first weighted supremum term allowing growth like `W^gamma` is therefore incompatible with the second term.

The problem becomes immediate in the Feynman--Kac section. Sources may grow like `delta log W`, so even `P_g 1` can grow with `W`. The pointwise weighted estimate does not prove that `P_g1` has bounded global oscillation, and hence does not prove that it belongs to the declared Banach space.

A standard weak-Harris cost may be capped for Wasserstein contraction, but the corresponding weighted Lipschitz norm must be designed consistently; the submitted combination is not.

### 3.10 B1: the exceptional Fourier contribution has no smoothing variable

B1 proves that linearly many good blocks exist with exponentially high probability. It then reserves one good block for coarea smoothing and says that the same reserved block is integrated on the exceptional event.

But the exceptional event is precisely the event on which there are too few good blocks, and it may contain configurations with no good block at all. The probability bound alone gives

```text
|exceptional characteristic contribution| <= e^{-cN},
```

which is independent of the unbounded continuous frequency and therefore not integrable over that Fourier space.

A reserved block can repair this only if it is guaranteed to possess a uniform smooth conditional density on every configuration, not merely with positive conditional probability. No such theorem is proved. The monotone approximation of the exceptional indicator does not manufacture a good block.

### 3.11 B2: the history product is undefined on the stated Banach space

The elements `H_G` of `mathfrak H_a` are arbitrary signed measures on parameter manifolds. The product `H^- star H^+` is defined as a fibre product over matching cut variables, “integrating the common cut state once.”

For arbitrary measures, a fibre product over a diagonal is not defined without disintegrations with respect to a common base measure and compatible absolute-continuity hypotheses. Two singular measures may not possess a canonical product on the matching set. Fubini cannot be invoked before the measure has been defined.

Therefore `star` is not a bilinear operation on all of `mathfrak H_a`, and the asserted Banach-algebra estimate and associativity do not follow.

The normalization sentence is also wrong as written: a fully labelled graph normally has trivial automorphism group, not automorphism group of order `|V|!`. The `1/k!` exponential-generating factor and the automorphism factor are distinct combinatorial objects.

### 3.12 B2: the subtree shear need not remain on the tree-contact manifold

For a surplus edge, the source cuts the tree edge immediately preceding the later endpoint and translates the descendant subtree. That translation generally breaks the already imposed contact represented by the cut tree edge. Applying the translation only after that contact would create a discontinuity unless one introduces and verifies a legitimate post-contact coordinate.

Thus the proposed shear is not shown to be a tangent coordinate on `Omega_G`, the manifold on which all tree contacts are imposed. The claim that earlier tree contacts remain unchanged omits exactly the tree edge connecting the translated subtree to its complement.

Moreover, after excluding a small neighborhood of singularities, the proof asserts a remainder `||R_e|| <= C delta_sing`. Being away from a singular set does not make derivative transport close to the identity with an error tending to zero as the excluded neighborhood shrinks. No such small parameter has been identified.

Hence the block-triangular Jacobian and the multiplicative loop gain are not established.

### 3.13 B3: quotienting `ker C` changes the physical action

A nonzero contact defect `h` in `ker C` leaves the density balance unchanged, but it changes the contact current. The quadratic expansion of the relative entropy assigns it the positive cost

```text
(1/2) int h^2/A_f.
```

B3 instead identifies every such defect with zero in `H_c/ker C` and defines the collision cost as the minimal quotient norm. Thus a physically nonzero contact perturbation can receive zero cost.

That quotient may be appropriate after contracting the joint theory to density alone. It is not appropriate for a paper that still claims a joint density/contact fluctuation process and imports the joint B2 contact-current LDP. Contact tests can detect directions in `ker C`; the collision noise contains them even when their gain-minus-loss marginal is zero.

The new quotient therefore does not repair the old graph kernel. It changes the theorem and makes the Hessian and covariance inconsistent with the advertised joint observable.

### 3.14 B3: the localization commutators have the wrong scale

The observability proof covers space-time by boxes of side `ell`, chooses a partition `chi_alpha`, and claims

```text
[chi_alpha, v.grad_x] = O(ell)
```

in the graph norm. In fact

```text
[chi_alpha, v.grad_x]p = -(v.grad_x chi_alpha)p,
```

and a partition subordinate to boxes of side `ell` has `|grad chi_alpha|` of order `1/ell`, not `ell`. Pseudodifferential commutators with the localized Kawashima multiplier have the same derivative-of-cutoff difficulty.

Thus shrinking the boxes does not make these errors absorbable; it makes the naive commutators larger. A genuine localization argument needs an IMS-type balance, a different scale, or a global variable-coefficient hypocoercive estimate. The submitted proof has the scaling sign reversed.

### 3.15 B4: the representation theorem contradicts the definition of the rate

B4 defines `I_T(f)` as an infimum over all regular control sequences producing the density path `f`. It then claims that for every approximable controlled pair `(f,q)`,

```text
I_T(f)=A_T(f,q).
```

The equality cannot hold for every `q`. Different contact controls can have the same gain-minus-loss term and hence the same density path while carrying different entropy costs. The existence of `ker C`, emphasized by B3 itself, gives exactly this situation.

At most one can claim

```text
I_T(f)=inf_{q producing f} A_T(f,q),
```

or keep the contact current as part of the state. The submitted representation theorem is false.

### 3.16 B4: the initial entropy destroys the semigroup property

The action used in `I_t` contains

```text
H(f_0|f_0^ref).
```

The value operator is then

```text
V_t phi(f)=sup [phi(f_t)-I_t(f_path)].
```

At time zero this gives

```text
V_0 phi(f)=phi(f)-H(f|f^ref),
```

not `phi(f)`. Thus `V_0` is not the identity. Concatenating two paths also charges preparation entropy at the intermediate state a second time, so `V_{t+s}=V_t V_s` fails.

Initial preparation cost can appear in a one-shot variational problem, but a dynamic semigroup must use a running action conditional on the fixed initial state. The Hamiltonian displayed later corresponds to the latter, not to the action actually placed in `V_t`.

### 3.17 B4: the superquadratic exponential moment is infinite under Gaussian tails

The chosen containment function satisfies

```text
Psi(v) ~ |v|^2 log |v|.
```

The upstream regular preparation assumes Gaussian velocity tails. For a Maxwellian random velocity `V`,

```text
E exp(lambda Psi(V)) = infinity
```

for every `lambda>0`, because `lambda |v|^2 log|v|` dominates the negative quadratic Maxwellian exponent.

B4 nevertheless asserts a uniform positive exponential moment of

```text
mu_epsilon sup_t <f_t^epsilon,Psi_R>
```

with constants independent of the truncation `R`, and then sends `R` to infinity. The bound is already impossible at time zero in the Maxwellian reference ensemble. A quadratic exponential moment cannot be upgraded uniformly to an exponential moment of `|v|^2 log|v|`.

The claimed “microscopic exponential martingale” is also unexplained in a deterministic collision flow whose only randomness is the initial state.

### 3.18 C1: the fixed probability envelope and translation formula are incompatible

C1 says that `xi_s` has density `rho_s` with respect to a probability measure `nu_s`, and that the translated observation has density

```text
rho_s(y-O(x))
```

with respect to the same `nu_s`.

That formula is correct for a translation-invariant reference such as Lebesgue measure. There is no finite translation-invariant probability measure on a noncompact Euclidean stratum. For a general probability envelope, the translated law has an additional Radon--Nikodym factor involving the translated reference measure, and it may fail to be equivalent at all.

Consequently the claimed identity

```text
int g(x,y) nu(dy)=1
```

does not follow. The finite-envelope repair is therefore not correctly implemented.

### 3.19 C1: deterministic push-forwards are not differentiable in signed-measure norm

The unnormalised update contains

```text
(Phi_theta)_# mu.
```

The proof claims that its first three parameter derivatives are bounded between weighted signed-measure spaces. This is false in the natural total-variation or finite-measure graph norm. For the elementary family

```text
Phi_theta(x)=x+theta,
```

the measures `delta_{x+theta}` and `delta_x` have total-variation distance two for every nonzero `theta`. The map is not even continuous in that norm, let alone differentiable.

Smooth measurement noise can make the predictive observation density differentiable after integration. It does not make the hidden posterior measure differentiable as a finite signed measure. One needs a distributional/Sobolev dual state space and a complete derivative-filter theorem in that topology.

### 3.20 C2: its weight assumption reintroduces local compactness

C2 begins with a Polish space and assumes a continuous weight `W` with compact sublevels. For any point `x`, choose `n>W(x)`. The open neighborhood `{W<n}` has closure contained in the compact set `{W<=n}`. Hence the space is locally compact.

Thus the assumption contradicts the stated purpose of treating genuinely non-locally-compact Polish path, probability, and belief spaces. The additional requirement of a compact exhaustion `K_n` also forces sigma-compactness and is unavailable on many infinite-dimensional Polish spaces.

The isolated weighted-duality calculation may be valid on an appropriate locally compact or weighted sigma-compact state space, but it does not establish the exported theorem for the actual A3/B4/C1 platforms.

### 3.21 C2: the Brownian innovation theorem does not match C1

C1 permits Euclidean, surface, countable, and confusion-matrix observation strata. C2 then writes

```text
dL_t=L_t H_t dI_t
```

and invokes Brownian martingale representation and Novikov.

Independent measurement noise does not imply that the observation filtration is Brownian or that every likelihood martingale is continuous. Discrete observations give product likelihoods and jump martingales; countable and surface channels need different stochastic calculus. No theorem in C1 identifies a continuous Brownian innovation filtration.

Accordingly the claimed stable innovation exponential is not a consequence of the submitted observation model.

### 3.22 D1: zero prior weights invalidate the leading maximum

D1 expressly allows arbitrary prior phase weights `w_j` with `w_j>=0` and `sum w_j=1`. Its leading theorem nevertheless maximizes over all phases:

```text
lim N^{-1} V_N = sup_alpha max_j G_j(alpha).
```

If `w_j=0`, phase `j` is absent from the finite-`N` log-sum and cannot contribute at any order. Choose two phases with `w_1=1`, `w_2=0`, and `sup G_2 > sup G_1`. The displayed limit selects phase two, while the exact value contains only phase one.

The maximum must be restricted to phases of positive prior weight, with a separate treatment when weights depend on `N`.

### 3.23 D1: the component-rate definition is circular

The source first writes

```text
Ical(j,z)=gamma_j + I_j(z) - gamma_*,
```

and immediately defines

```text
I_j(z)=Ical(j,z)-inf_y Ical(j,y).
```

The object `I_j` is used in the definition of `Ical` and then defined from `Ical`. No upstream labelled rate resolving this circularity is actually stated in A2 or B1.

### 3.24 D1: there is no policy integral to which Morse--Bott applies

The value is a supremum over policies. If the maximizing set is a smooth manifold, asymptotics of a supremum are governed by maxima and perturbations of the objective. There is no integration measure over policies and therefore no Gaussian determinant or Morse--Bott volume factor from “integrating on the policy manifold.”

The final sentence of the subleading theorem confuses Laplace integration with optimization. A policy manifold can create nonuniqueness, but not a Laplace prefactor unless the model explicitly averages over policies.

---

## 4. Paper-by-paper assessment

## A1 — Exact symplectic benchmarks and current limits

The mapping-torus portion is the least problematic part of the dossier, but the main analytical claims remain invalid.

### Major objections

1. The dual Sobolev scale has the derivative direction reversed, as explained in Section 3.1.
2. The projective boundary jets `B_{a,N}^{(j)}` are not required to be coherent, yet the tail identity later uses a projective object `B_a^{(j)}`.
3. The norm in the response domain forces the displayed `B_{a,N}^{(j)}` to decay as `N` grows, while it was introduced as the full boundary derivative of the `N`-cylinder current. The intended shell versus cumulative meaning is not defined.
4. The geometric certificate asserts that a product of branch widths controls current norms and all material derivatives. Push-forward norms of delta-type seam currents generally involve inverse Jacobians and incidence multiplicities; the one-sentence product argument is insufficient.
5. The functional CLT is ill typed in `C([0,1])` because the displayed process is not polygonally interpolated.
6. Uniform parameter derivatives of the covariance require differentiating the projective martingale projections and the infinite `D_0` sum. This is not supplied by the response theorem for the mean alone.

### Disposition

**Reject.** A corrected suspension/current note might be viable after the dual-scale direction, coherent boundary data, and functional limit are completely rewritten.

---

## A2 — Sinai arithmetic and raw local limits

### Major objections

1. The branch certificate (A2.1) is impossible as written at `j=0`.
2. The asserted nonempty billiard construction verifies selected periodic corridors but not the global countable branch derivative budget or terminal nonstationarity on every bad word.
3. The annihilator theorem is false for the allowed two-dimensional continuous roof coordinate.
4. The norm (A2.4) is only a schematic expression; domains of unstable derivatives, homogeneity weights, completions, and compact embedding are not defined.
5. The returned-UNI lemma promotes a formal repeated integration-by-parts calculation to an anisotropic operator bound without proving stability of the matched stable-curve decomposition under all derivatives.
6. Certificate (C4) is an infinite assertion about every bad branch, not a finite certificate, and the nonempty-class proof does not establish it.
7. The quantitative Dolgopyat lemma is essentially the desired difficult theorem restated in one paragraph. Periodic Diophantine data do not by themselves imply a fixed fraction of locally cancelling branch pairs at every intermediate frequency.
8. The claimed `O(n^{-1/2})` raw local density error requires a complete uniform spectral expansion and regularity theorem beyond the norm bounds provided.

### Disposition

**Reject.** Since A2 is the root of the billiard chain, A3, A4, C1, C2, and D1 cannot import its local theorem.

---

## A3 — Chronological graph currents and path large deviations

### Major objections

1. The completed-graph quotient and legality closure are not constructed at the level needed to prove that the entire mark space is Polish.
2. The collision-stopped path parametrization is undefined when total physical time is below `N`.
3. The history-balance identity is directly false for chronological-only tests.
4. The spaces in the projective recession inverse limit are called compact without defining a uniform mass bound. The total mass of `R^{(r)}` is not bounded on the stated state space.
5. A terminal mark of size order `N` escapes every compact subset of the unscaled mark space. The same normalized entropy bound that permits one-big-excursion controls does not make the full terminal mark tight.
6. Compatibility formula (A3.6) uses an undefined recession evaluation `omega_infty` and does not show that escaping marks are not double counted between `Q` and `R`.
7. Uniform positive connector probabilities are asserted for recurrent and recession pieces, including endpoints arbitrarily near singularity, without proof.
8. The stopped local theorem gives a Gaussian scale to a clock pinned by the stopping rule.
9. The terminal threshold indicator in the renewal operator depends on the accumulated clock and `N`; it is not a fixed bounded strong-space multiplier merely because its values lie in `[0,1]`.
10. Exponential approximation of every bounded continuous path functional by finite-memory sources is asserted from tightness without constructing the required uniform approximation on the projective current state.

### Disposition

**Reject.** The proposed graph-current direction is potentially useful, but the state, balance law, stopping theorem, and conditioning theorem are not valid as submitted.

---

## A4 — Weak Harris theory, renewal, and memory

### Major objections

1. The power drift is not derived from the A3 conditional moment estimate.
2. The capped cost and the global Lipschitz seminorm force bounded oscillation, contradicting the intended weighted source class.
3. The local coupling proof assumes common regular-branch overlap and total-variation control that A3 does not establish across branch births and singular cuts.
4. The weak-Harris theorem is invoked as if Wasserstein contraction automatically yielded the full weighted operator norm (A4.8) on the inconsistent Banach space.
5. The source set `U_delta` is not supplied with a complete Banach norm, yet operator analyticity in an infinite-dimensional “small ball” is asserted.
6. `m_0(h)` in the entrance operator is not defined by the complete-past state. The exit operator produces a section-point function and contains no residual flow coordinate, so the claimed flow-to-flow resolvent factorization is not geometrically typed despite the arrows written above it.
7. `R_0(z)` is not defined.
8. The `L^2` exponential gap (A4.10) is not proved from the weighted-Lipschitz Harris gap. Pressure tangent observables are not automatically spectral modes of the continuous-time generator.
9. The finite-rank compression lemma requires a genuine graph isomorphism and bounded perturbation theorem; (A4.11) does not state equality of ranks, closeness of projections, or complete domain hypotheses.
10. Exponential semigroup stability does not supply the sectorial resolvent bound used for the expansion on sectors approaching the negative real axis. Sectoriality/analyticity of `L_Q` is never established.
11. Since `C_Q` is only graph-norm bounded, decay of the forcing term requires graph-norm estimates on `Qx`, not merely Hilbert-space decay.

### Disposition

**Reject.** The algebraic form of the Schur--Feshbach identity is now correct, but its actual history/flow realization and stable compressed generator are not proved.

---

## B1 — Exact-number preparation and mixed local coefficients

### Major objections

1. Conditioning successively on deterministic blocks is not reconciled with the repeated phrase “condition on the exterior configuration.” Conditioning each block on its full complement produces non-nested sigma-fields; the tower-product argument requires a precise integration order.
2. A hard-core conditional block can have very small or empty allowed region under an adverse exterior. The claimed uniform lower comparison with a Maxwellian product is not a consequence of B2's averaged cluster expansion.
3. The statement that only a fixed number of hard-core boundary components meet a relevant box is unsupported at Boltzmann--Grad particle number and depends critically on the box scale.
4. The good-block covariance and aperiodicity are assumed uniformly over all preceding conditionings rather than proved.
5. The reserved-block argument fails on the exceptional event, as shown in Section 3.10.
6. Source differentiation of an extensive path source does not merely “mark at most two factors” without combinatorial powers of `N` and recentering estimates.
7. The Edgeworth-size relative error is not derived from the displayed characteristic bound alone.
8. `ind H` and `ind 0` in (B1.10) are undefined. For fixed-dimensional nondegenerate saddles the Gaussian dimension does not change merely because a source is present.
9. Strict convexity on the real axis does not exclude all competing complex activity saddles; the invoked zero-free tube is not a theorem in B2.

### Disposition

**Reject.** The normalization correction is valid, but the global Fourier estimate and exact coefficient ratio are not established.

---

## B2 — Collision-history algebra and hard-sphere LDP

### Major objections

1. The fibre-product algebra is undefined for arbitrary signed measures.
2. The automorphism normalization is misstated for labelled graphs.
3. The subtree shear generally breaks the cut tree contact and is not shown to be a legal coordinate on the constrained history manifold.
4. The `O(delta_sing)` derivative remainder has no geometric basis.
5. A contact equation with a free impact direction does not automatically yield the scalar tube factor asserted after cross-section cancellation; the coarea dimensions and powers of `epsilon` are not computed.
6. Nested or overlapping descendant subtrees need not give independent shear variables merely because surplus edges are chronologically ordered.
7. The Duhamel map is never defined as an operator on the measure-valued history space. Differentiating a generating series in the radius does not prove the exact nonlinear estimate (B2.11).
8. Finite-time propagation of chaos and collision histories does not follow from the tail estimate plus termwise removal of fixed recollision graphs. Initial correlation control, cut compatibility, and limit uniqueness are absent.
9. A logarithm in the generally noncommutative and not-yet-defined history algebra is not constructed.
10. The finite collision simplex cannot correct an arbitrary space-time-velocity balance defect using one fixed finite family of collisions without a refining local construction and uniform constants.
11. A second source derivative gives a variance scale, not exponential concentration of a deterministic tilt. A Chernoff/Laplace theorem on the full complement is needed.
12. The claimed LDP is for `(f,Gamma,H)` but the displayed rate constrains only `(f,Gamma)` and does not identify the retained history coordinate.
13. Local analyticity of the pressure near zero does not by itself give a full good LDP on the infinite-dimensional topology.

### Disposition

**Reject.** B2 remains the decisive failed root of the hard-sphere chain.

---

## B3 — Quotient defects and kinetic fluctuations

### Major objections

1. The quotient erases positive-cost, observable contact-current directions.
2. The resulting Hessian cannot be the inverse covariance of the joint density/contact process.
3. The space `L^2(A_f^{-1})` and the closed map `C` are not completely defined when defects are signed measures rather than densities.
4. The localized commutator estimate has the wrong dependence on the box size.
5. The closed-range theorem identifies the adjoint estimate with the full primal graph norm without controlling the contact representative needed by the nonlinear recovery.
6. The conditional cut-density lemma assumes a uniformly bounded denominator. Applying radius-loss estimates to numerator and denominator does not yield a uniform `L^p` bound for their ratio when the conditioning history has very small probability.
7. The cut sigma-field and the “unresolved future roots” are not constructed as a conditional factorization of the deterministic initial ensemble.
8. Summing scalar cumulant estimates over an orthonormal basis requires explicit Hilbert--Schmidt singular values and uniform constants; the one-sentence argument is insufficient.
9. The Gaussian martingale problem and its uniqueness are not stated on a complete path/test space.
10. The Mosco recovery uses the quotient right inverse to correct a concrete positive contact multiplier, but a quotient class does not select the physical representative required for positivity.

### Disposition

**Reject.** The quotient is not a permissible repair for a joint contact-current theorem.

---

## B4 — Attainable actions and nonlinear semigroups

### Major objections

1. The effective-domain representation is false because `I_T(f)` contracts over controls while the theorem equates it to every control cost.
2. The positive superquadratic exponential moment is impossible under the Gaussian reference tail.
3. The deterministic hard-sphere process has no stated collision-counting martingale with the compensator used in the proof.
4. The Povzner estimate for the truncated function `Psi_R=Psi wedge R`, uniform in `R`, is asserted without proof; truncation destroys the simple convexity structure.
5. The dynamic action includes initial entropy and therefore does not generate a semigroup.
6. The state space `X_Psi` is not defined independently of path/action sublevels, while the viscosity theorem is said to hold “on every I_T sublevel.”
7. The entropy topology (B4.8) is largely redundant with the separately assumed weak convergence and does not create strong convergence of collision densities.
8. The comparison proof for the exponential collision Hamiltonian is reduced to a slogan about synchronous coupling; the doubled-variable derivatives and unbounded velocity tails are not controlled.
9. The realization map for a general density is defined by choosing a recovery and taking a graph closure. No canonical selection or independence of the recovery is proved, so the map is not well defined.
10. The final uniform supremum uses `f` both as a state and as a full path constrained by `I_T(f)`, producing a type ambiguity.

### Disposition

**Reject.** Both the variational semigroup and its microscopic limit fail before the Trotter--Kato argument begins.

---

## C1 — Noisy filtering and adaptive inference

### Major objections

1. The translated-noise density is not normalized against the claimed finite probability envelope.
2. The signal map is initially assumed continuous, while the channel-regularity proof uses three parameter derivatives without stating them as hypotheses.
3. Deterministic push-forward of beliefs is not differentiable in the claimed signed-measure norm.
4. Feller continuity is not a contraction estimate for derivative errors; the recursive-QMD proof uses it as one.
5. A lower noise-density bound only on compact diagnostic regions does not give a uniform bound for all observations when the noise has unbounded support.
6. The closed convex hull of a reachable belief set is not automatically a shell on which all model-specific regularity estimates remain valid.
7. The information Gramian condition at one belief does not combine with global action frequencies when an adaptive policy correlates its action choice with the current belief. One can choose the least informative action at each belief while satisfying aggregate frequencies.
8. An ergodic law of large numbers is invoked for an arbitrary adaptive, nonstationary policy without an invariant controlled chain theorem.
9. Local Fisher positivity does not give the fixed-distance Hellinger identifiability needed for the asserted global tests.
10. The growing-annulus covering calculation is only a proof sketch and does not establish strategy-uniform total-variation Bernstein--von Mises convergence.

### Disposition

**Reject.** Adding independent noise repairs the old conceptual contradiction, but the actual reference measure, derivative filter, information theorem, and BvM argument are not correct.

---

## C2 — Strict duality, rigidity, and path prediction

### Major objections

1. The compact-sublevel weight assumption forces local compactness and therefore does not match the advertised platforms.
2. The compact exhaustion used to define the topology may not exist on the intended infinite-dimensional Polish spaces.
3. The annihilator theorem imports B3's invalid quotient graph and therefore cannot represent the full contact cotangent.
4. A4 supplies pressure analyticity only on a small source ball, not along the complete unbounded exposing rays required here.
5. Equilibrium existence, uniqueness, tail tightness, and zero-temperature localization on the countable history shift are each asserted rather than proved.
6. The stopped-path prediction state lives in a time-dependent space `D([0,t])`; no fixed Polish state space for the process `bar Pi_t` is constructed.
7. Conditional expectation of a full future path functional requires a continuation kernel not included in the stated prediction process or assumptions.
8. Predictable covariation convergence is assumed in (P4) and then returned as a conclusion; the upstream papers do not verify it.
9. The Brownian innovation theorem is incompatible with the general C1 observation channels.
10. The C1 score envelope and action-frequency condition do not prove the exponential bracket moment (C2.9).
11. Joint BSDE convergence requires convergence of terminal conditions and drivers in addition to UT and bracket convergence.

### Disposition

**Reject.** The weighted dual may be salvageable in a correctly delimited functional-analytic note, but the rigidity and stochastic-convergence package is not proved.

---

## D1 — Phase coefficients and shared-policy asymptotics

### Major objections

1. A2 and B1 do not prove the joint local expansion (D1.1) for “all remaining path coordinates.” They prove selected finite-dimensional additive local theorems at best.
2. The mixed lattice/continuous reference cannot be treated by one ordinary tubular Morse--Bott integral without a separate lattice summation theorem.
3. The assumed `C^3` normal form and two derivative bounds do not justify an explicit `N^{-1/2}` coefficient with `O(N^{-1})` remainder; higher derivatives are required.
4. The symbol `d_j` is used both for ambient dimension and for a correction coefficient.
5. The component-rate definition is circular.
6. The leading theorem ignores zero prior phase weights.
7. Sequential compactness of all relaxed feedback policies is not a consequence of the Feller property alone; adaptedness and stable-topology closure must be proved.
8. Uniform A2/B1 source estimates over a finite-dimensional source ball do not imply a uniform controlled Laplace principle over an infinite-dimensional policy space.
9. Near-optimal policies outside the exact maximizer set can alter polynomial and constant orders. The quadratic-drop assumption is not developed into a valid optimization expansion.
10. The Morse--Bott policy-manifold sentence incorrectly integrates a supremum problem.
11. Positivity of each analytic amplitude at zero plus compactness does not yield one uniform zero-free chart unless continuity and a positive uniform lower bound are established.
12. Every mechanical component imported by D1 is already unavailable because its root chain fails.

### Disposition

**Reject.** D1 is a formal synthesis conditional on local and control theorems that the dossier does not contain.

---

## 5. Dependency-level consequence

The Round-Twenty-Seven dependency ledger is acyclic as a graph, but the mathematical contracts at its root nodes fail.

### Billiard chain

- A1 has an incorrectly directed current scale and an ill-typed functional limit.
- A2's certified class is not shown nonempty and its arithmetic theorem is false for an allowed dimension.
- A3 uses a false balance equation and a degenerate stopped coordinate as Gaussian.
- A4 imports the failed A3 moment/state, and its own weighted space, renewal, and compression arguments fail.

Therefore none of the billiard pressure, local conditioning, memory, filtering, rigidity, or phase exports is established.

### Hard-sphere chain

- B2 lacks a well-defined history algebra and a valid loop-rank coordinate.
- B1 therefore has no valid grand-canonical input and independently lacks an integrable exceptional Fourier estimate.
- B3 changes the contact-current action by quotienting it.
- B4 uses a false rate representation, an impossible exponential moment, and a non-semigroup action.

Therefore none of the exact-number LDP, fluctuation, kinetic semigroup, filtering, or phase exports is established.

### Synthesis chain

- C1's noisy channel is not normalized as written and its derivative filter is mistyped.
- C2 does not apply to the claimed non-locally-compact states and does not match C1's observation filtration.
- D1 assumes a stronger local theorem than any upstream node provides and contains independent control asymptotic errors.

Passing the repository's acyclicity and token checks cannot repair failed theorem contracts.

---

## 6. Significance and presentation

The advertised programme is highly ambitious. A correct proof of even one of the root theorems could be important. That ambition raises, rather than lowers, the required level of detail.

The active dossier is 49 pages for eleven papers. Individual sources are five to seven pages while claiming, among other things:

- a new all-frequency anisotropic local theorem for Sinai billiards;
- a projective stopped path-space LDP;
- a weak-Harris/Feynman--Kac/renewal/memory platform;
- a new finite-time hard-sphere collision-history expansion and full dynamic LDP;
- a nuclear process CLT and Mosco Hessian;
- nonlinear kinetic semigroup convergence;
- adaptive filtering, LAN, and Bernstein--von Mises;
- optional-projection and BSDE stability;
- and Morse--Bott shared-policy phase asymptotics.

These cannot be established by naming the difficult mechanism and giving one paragraph. In several places the paragraph contains a direct algebraic or type error. The manuscripts still read as research programmes or proposed proof blueprints, not completed proofs.

---

## 7. Minimum requirements for a scientifically meaningful future submission

A further all-at-once eleven-paper revision is not the appropriate next step. A credible submission should proceed as follows.

1. **Choose one root paper.** Submit either a complete A2 theorem for a precisely specified billiard class or a complete B2 theorem for a precisely specified hard-sphere ensemble.
2. **Remove conditional theorem inflation.** A “certificate” must be explicitly constructed and verified; it cannot contain the desired global operator estimate as one of its unchecked fields.
3. **For A1, repair the dual scale and path space.** State the correct distributional derivative direction, define coherent boundary jets, and use a genuinely continuous interpolation or the Skorokhod space.
4. **For A2, correct the branch norm and continuous arithmetic.** Weight all countable branch derivatives correctly, prove a nonempty class including bad-word estimates, and formulate the closed subgroup theorem in the actual continuous dimension.
5. **For A3, derive the exact discrete balance identity first.** Construct the projective recession and terminal spaces with explicit mass bounds, normalize collision and physical clocks correctly, and separate Gaussian renewal variables from overshoots.
6. **For A4, use a consistent weak-Harris function space.** Prove the power drift, define all renewal entry/exit maps including the flow coordinate, and establish the compressed generator and sectorial estimates independently.
7. **For B1, prove smoothing on every exceptional component.** A high-probability good-block theorem alone is insufficient for an integrable Fourier tail.
8. **For B2, restrict the algebra to measures admitting compatible disintegrations.** Define the cut product rigorously, correct the combinatorial normalization, and construct a genuine tangent coordinate preserving every tree contact.
9. **For B3, do not quotient away observed contact currents.** Contract to density explicitly if that is the intended theorem, or retain the full positive contact Hessian and control its kernel correctly.
10. **For B4, separate preparation from dynamics.** Initial entropy belongs outside the semigroup running cost. Prove containment at a moment scale actually supported by the reference ensemble.
11. **For C1, select a valid fixed observation envelope.** Write the exact Radon--Nikodym density of translated noise and differentiate only in a topology in which deterministic push-forwards are differentiable.
12. **For C2, delimit the state class honestly.** Do not claim non-locally-compact Polish generality under assumptions that force local compactness. Separate discrete/jump and Brownian observation theorems.
13. **For D1, prove a finite-dimensional local input before phase synthesis.** Restrict leading maxima to phases present in the prior, define rates noncircularly, and treat policy optimization as optimization rather than integration.
14. **Provide full literature interfaces.** Every imported theorem must be stated precisely, with each hypothesis verified on the exact source and topology used downstream.
15. **Obtain independent specialist reports.** Billiard dynamics, hard-sphere expansions, kinetic hypocoercivity, filtering/statistics, and nonlinear semigroup theory require distinct referees.

These are reconstruction requirements, not a major-revision checklist for the present dossier.

---

## 8. Final verdict

Round Twenty Seven is a real revision and fixes the prior branch-integrity failure. It also removes several previously disproved formulas. Those are meaningful improvements in process and presentation.

The active mathematical sources nevertheless remain invalid. The suite contains direct counterexamples to central statements, including:

- the reversed A1 distributional scale;
- an A1 process not belonging to its claimed path space;
- an impossible A2 branch certificate and a false two-dimensional character argument;
- a false A3 balance identity and degenerate stopped Gaussian coordinate;
- an A4 Banach space incompatible with its own unbounded sources;
- a B1 exceptional Fourier term without smoothing;
- an undefined B2 measure fibre product and an invalid shear coordinate;
- a B3 quotient that erases positive contact entropy;
- a B4 value family that fails `V_0=Id` and a superquadratic exponential moment that diverges under Gaussian tails;
- a C1 observation density not normalized against its envelope and a nondifferentiable Dirac push-forward;
- a C2 state assumption that forces local compactness and a stochastic representation inconsistent with the observation model;
- and D1 phase/control formulas with zero-weight, circular-definition, and supremum-versus-integration errors.

Because these failures occur at the root nodes and propagate through the declared dependency graph, none of the eleven manuscripts is ready for publication.

**Recommendation to the editor: reject all eleven manuscripts and do not invite another major revision of this dossier. Any future submission should be a substantially reconstructed, self-contained root paper with complete proofs and an independently verified model class.**
