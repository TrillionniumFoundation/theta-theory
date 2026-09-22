# Response to the v3 referee report — fourth revision

**Paper:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction.  
**Author:** Qian Qi. **Date:** 22 September 2026.  
**Controlling report:** `reviews/general-theta-foundations-i-v3-2026-09-22/REFEREE_REPORT.md`, review commit `d084e3cf505f3978ddaab9b954aac94b97fe7bd3`, blob `a0fdf0b8335d9b14c2fc8e66cd6b5e2dbe4c2479`.  
**New revision:** `revision/general-theta-foundations-i-v4-2026-09-22`.

We thank the referee for distinguishing mathematical errors from the demand for a stronger general theorem. This revision responds by proving additional results, not by replacing the paper with a programme statement or suppressing its earlier mathematics. All preceding source editions and reports remain unchanged. The complete new article retains the quantitative v3/v2 results and the foundational appendices with their proofs; a new independent principal chain precedes them.

The main changes are a posterior-orbit realization theorem for arbitrary Borel dynamics with noisy renewal observations; a matched finite-state law for noisy expanding torus experiments in every dimension with nongeometric renewal laws; a uniform critical-window analysis; and an actual calibrated, changing-rank moment experiment whose singular modulus and matching tests are derived. Numerical and build records below support reproducibility, not the truth of an infinite-dimensional argument.

The stable TeX labels below are authoritative locators. Their final theorem numbers and PDF pages are generated in `evidence/BUILD_RECEIPT.json` under `new_mathematical_locations`.

## Decisive objections

### E1. A general converse without a general realization theory

**New proof:** `posterior-orbits.tex`, Theorem `thm:v4-orbit`, Corollary `cor:v4-exponent`, Proposition `prop:v4-closure`.

For a fresh pair `(U,Y)` with an arbitrary standard Borel observation kernel, the relevant object is the posterior orbit `Z(Y) = (sqrt(w_k) E[f(T^k U)|Y])_k`, not the noiseless orbit of the hidden state. If `B` denotes the complete-history Bayes floor, the theorem proves

```
R_M^av = B + E_M^av,
e_M^2(Z) <= E_M^av,
E_(N n+1)^av <= e_N^2(Z^{<n}) + ||f||_infinity^2 W(n).
```

The converse includes randomized, time-dependent machines and arbitrary Hilbert-space centres. The upper bound is an explicit measurable finite-state construction: states `(codeword, age)` for `N` codewords and `n` ages, together with one exhausted state. No age register is hidden. The proof uses the actual independent renewal law, including deterministic/arithmetic cycle lengths; it assumes only finite mean for this sandwich.

Under `W(n) <= A exp(-c n^beta)`, the causal excess risk has the same finite positive quantization exponent as the posterior orbit. This is a general exponent theorem, rather than an unevaluated converse. Under a two-sided power law its upper overhead is displayed as `(log M)^(alpha/beta)`. Exact same-cardinality realization is separately characterized for autonomous deterministic ray codebooks by left-shift closure. A two-state example proves that orbit quantization alone cannot imply a same-`M` equality without that closure. This boundary sharpens the theorem's statement; it is not a replacement for achievability.

The model admits arbitrary Borel transition and observation maps. As stated, this is a measurable-state theorem, not an assertion that every Borel quantizer has a finite computable implementation. The sharp suffix constructions below are explicit finite algorithms.

### E2. One engineered example and no near-critical scaling

**New proof:** `expanding-noisy.tex`, Theorem `thm:v4-noisy`, Corollaries `cor:v4-noise-memory`, `cor:v4-critical`, Proposition `prop:v4-conjugacy`.

The sharp model now includes every integer expansion `b >= 2`, every dimension `d >= 1`, wrapped Gaussian noise at the acquisition, and every renewal law satisfying the explicitly stated bounded-mean-residual-lifetime condition `W(n) <= A w_n`. This includes bounded cycle lengths and suitable mixtures of geometric laws, not only Bernoulli resets. It does not silently include polynomial tails.

The exact posterior is `a_k Phi(b^kY)`, with `a_k = exp(-2 pi^2 sigma^2 b^(2k))`. Writing `v_k=w_k a_k^2`, the theorem bounds the optimal excess risk above and below by the same profile

```
Psi_v(n) = sum_{k<n} v_k b^(-2(n-k)) + sum_{k>=n} v_k,
1 + b^d + ... + b^(dn_M) <= M < 1 + ... + b^(d(n_M+1)).
```

The lower constant `1/(8 A b^6)` and upper constant `d pi^2/3` are explicit, independent of `M` and `sigma`. Off-image centres and all randomized nonstationary encoders are covered. The matching suffix code charges all word lengths, rather than only the longest words. Its exact risk is proved using posterior conditional means over the digit cubes.

For geometric renewals the bound is uniform on compact `q`-intervals. At `q_n=b^(-2) exp(x/n)` the scaled profile converges uniformly on bounded `x`-intervals to `(1-b^(-2)) (exp(x)-1)/x`. The exact suffix risk has the corresponding coefficient `d pi^2/3`. The optimal risk is uniformly comparable to this profile; we do not turn constant-factor bounds into an unsupported exact optimal prefactor. The original scalar doubling theorem is retained, not retrospectively relabelled as a uniform result.

Smooth conjugacy provides explicit nonconstant-slope, nonuniform-density, transported-noise examples. Bi-Lipschitz changes of the embedded readout preserve raw risks within specified factors. These examples are a proved robustness class; their Lyapunov exponent is still `log b`. A pressure formula for arbitrary nonconjugate variable expansion is not asserted.

### E3. Finite-rate control and dynamical rate-distortion comparisons

**Changes:** Introduction, theorem-level comparison table, `LITERATURE_AUDIT.md`, six additional bibliography entries.

We compare directly with Tatikonda–Mitter, Propositions 3.1 and 5.3, and Lindenstrauss–Tsukamoto, Theorem 1.5 and Corollary 1.10. Nair–Evans and Matveev–Savkin are also cited. The comparison records resource, dynamics, observations, information pattern, objective, converse class, upper construction, and controlling invariant.

The distinction is mathematical: a per-time channel alphabet does not bound the total number of decoder states when an encoder retains real-valued centres or scales. Conversely, one initial persistent state with no further data is not a continuing communication channel. Our general theorem explicitly pays for making a finite orbit codebook causal, and the sharp theorem proves a closed finite-state implementation. We do not claim that expansion-based lower bounds or rate-distortion ideas originate here.

### E4. Classical invariant minimax theory

**Changes:** Introduction and `LITERATURE_AUDIT.md`; retained Theorem `thm:v3-quotient` remains unchanged.

The Gaussian quotient is now explicitly situated in invariant/minimax theory, with Bondar–Milnes as a reference for asymptotically invariant averaging. Its diffuse-nuisance method is not advertised as a new Hunt–Stein principle. Its exact conclusion is preservation of every hard label budget and the covariance of the actually observed pair, for bounded losses about the target parameter. The proof privately simulates the asymptotically uninformative residual before compression, so it does not add labels.

The new collision theorem uses this established reduction to prove a specified nonregular model law. Neither the paper nor this response identifies equality of target minimax risks with a parameter-uniform Blackwell equivalence for `(theta, eta)`.

### E5. Assumed contact geometry and hidden conditioning constants

**New proof:** `collision-moments.tex`, Theorem `thm:v4-roots`, Lemmas `lem:v4-root-modulus`, `lem:v4-root-testing`.

The observation mean is the actual power-sum map `P_j(theta)=sum_i theta_i^j` on ordered roots in `[0,1]`. Its Jacobian determinant is `d! product_{i<j}(theta_j-theta_i)`, so it loses rank at root collisions. The data are a correlated Gaussian measurement of these power sums paired with a noisy additive-calibration measurement. No global bi-Lipschitz contact law is assumed.

Newton identities first control the polynomial coefficients by the moment discrepancy. A multiplicity-preserving complex-root argument then proves the global inverse modulus with exponent `1/d` and the separated-cluster modulus with exponent `1/r_j`. For the converse, perturbing only the constant coefficient of a real-rooted polynomial gives distinct configurations matching the first `r-1` moments. Scaling those configurations yields the matching Gaussian two-point lower bound. A separate hard-label covering lower bound gives

```
R_M(global) ~ min(1, sigma^(2/d)) + M^(-2/d),
R_M(fixed separated cluster domain) ~ min(1, sigma^(2/r_*)) + M^(-2/d).
```

The cluster domains allow collisions within known separated intervals; they are not incorrectly treated as exact-multiplicity manifolds of dimension `d`. Constants may depend on dimension, covariance conditioning, interval widths, and gaps. The earlier contact theorem is retained, together with an explicit new clarification that its physical uniformity requires uniform control of `lambda` and `Lambda`.

This is an actual nonseparable changing-rank experiment. It is not claimed to be the old Sinai experiment or the unknown-weight i.i.d. mixture experiment.

### E6. Relation to the eleven-paper pipeline

**Changes:** `HISTORY_AUDIT.md`, `HISTORY_INPUT_MANIFEST.json`, main proof-dependency paragraph.

We consulted the complete exported pipeline context, the master programme, the latest fixed Round-20 reports for all eleven components, the controlling Round-17 theorem/proof inventory, and the relevant modern A1 v37/A2 v112 sources. The audit states which material was read and what was not independently re-proved. It records file hashes and immutable editions.

The positive connection is now specific. Theorem `thm:v4-orbit` supplies a general finite-state realization result at the programme's T07/T08 interface. The sharp noisy theorem gives a joint statistical/transport realization of the G1/G3 questions. The derived moment modulus and tests instantiate T10/G2 in a changing-rank calibrated model. These are proved mathematical applications rather than additional interfaces.

The separate spectral, particle-LDP, kinetic, nonlinear-semigroup, and unbounded-operator claims are not used as premises and are not declared resolved by the new proofs. Their derivations remain in the repository. Resolving a mathematically different model is not evidence for an old hard gate; respecting that distinction is necessary to make the new positive results checkable.

### E7. Integrated architecture

**Changes:** principal theorem chain in Sections 2–4; independent dependency map; full retained quantitative and foundational development follows.

The paper now begins with a short new conceptual introduction and three connected proof sections. A referee can read the orbit theorem and the noisy expansion theorem without the historical filter/control material. The collision theorem depends on one retained result, the exact Gaussian quotient, and two local lemmas proved in its own section.

All prior mathematical statements, proofs, and examples remain available in the integrated manuscript and in their untouched earlier editions. The preceding introductory prose remains in the preceding edition. The new organization separates what carries the main argument from what supplies complementary foundations. The request to split the manuscript is an editorial preference; we address its underlying readability concern without deleting the work the author requested to preserve.

## Major objections

| Objection | Concrete response in v4 |
|---|---|
| M1: persistent states versus ordinary memory complexity | Section 2 defines all decoder/update inputs and charges every persistent register, including renewal age and a data-dependent random-seed position. The introduction and literature audit distinguish cardinality, communication, transient computation, and description length. No total-complexity theorem is claimed. |
| M2: difficulty only after perfect acquisition | The noisy torus theorem computes the actual posterior, the Bayes noise floor, and the matched memory loss in one experiment. A decoder knowing neither noise level nor renewal law is proved order-optimal for raw risk. |
| M3: robustness beyond binary exactness | Every integer base and dimension, bounded-residual-life nongeometric renewal laws, wrapped acquisition noise, explicit nonconstant-slope conjugates, and bi-Lipschitz readouts are treated. The nonconjugate pressure problem is kept distinct. |
| M4: causal realizability of an orbit codebook | General `Nn+1` realization; exponent invariance; exact autonomous shift-closure characterization; and an explicit example separating unconstrained orbit quantization from same-cardinality causal execution. |
| M5: preservation is not mathematical upgrading | The new dependency map identifies the sole retained input to the collision theorem and the independence of the orbit/expansion chain. No byte comparison is used in a mathematical proof. All retained proofs remain available for independent review. |
| M6: theorem-level literature | The in-paper comparison is complemented by the eight-field audit, with exact theorem locators and verified primary-source metadata. Classical methods are attributed, and the different experiments/resources are specified. |
| M7: title and scope | The title is retained. Its programme meaning is now supported by a general realization theorem and concrete noisy/singular realizations, not by a claim that all historical downstream models have been completed. |

## Technical comments in Section 19

**19.1.** Lemma `lem:v4-kernels` realizes every standard Borel stochastic kernel with a countable independent uniform family. Fixing this family and the pre-renewal history gives at most `M` no-renewal decoder strings. No measurability assertion is left to an informal random-tape metaphor.

**19.2.** The retained scalar checkpoint theorem uses the complete acquisition history. For clarity: that history contains the last exact acquired value and every subsequent observed reset/nonreset mode; the known deterministic map therefore determines the current state exactly. Uniform scalar quantization then gives `1/(12 M^2)`. In the new noisy theorem the analogous object is a posterior conditional mean, and the complete-history error is explicitly nonzero.

**19.3.** Proposition `prop:v4-closure` and Example `ex:v4-gap` make the causal-realization issue a formal statement rather than a caution in prose. The general sandwich pays the missing finite-age overhead.

**19.4.** Corollary `cor:v4-critical` supplies an actual uniform window. It separates exact suffix coefficients from constant-factor optimal-risk bounds and fixed-`q` asymptotics.

**19.5.** The target-minimax versus full-experiment distinction is stated in the introduction, before the collision theorem, and in the literature audit.

**19.6.** Lemmas `lem:v4-root-modulus` and `lem:v4-root-testing` derive a coupled moment geometry and matching lower configurations across actual rank-changing collisions. The application no longer consists solely of a shear of coordinatewise powers.

## Relation to the referee's proposed routes

Route A is addressed by a general noisy posterior-orbit converse/realization and exponent theorem, together with a same-cardinality closure characterization. Route B is addressed by a uniform critical profile, arbitrary dimension and base, a nongeometric renewal theorem, and a specified robustness class; not by a claim of an arbitrary-map pressure theorem. Route C is addressed by a sharp noisy-acquisition plus expanding-transport theorem and a noise-independent upper machine. Route D is addressed by the derived collision moment geometry. Route E is a separate programme obligation, not a premise or consequence silently imported into the new results.

The mathematical response is the new sequence of complete proofs. Source hashes, finite diagnostics, successful compilation, and page inspection are supplied separately. This revision is submitted for another mathematical referee pass; no independent acceptance decision is represented by its build status.
