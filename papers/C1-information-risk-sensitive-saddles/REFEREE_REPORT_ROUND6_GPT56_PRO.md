# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — *Information States, Risk-Sensitive Saddles, and Controlled Kinetic Values*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `3c7e75e0df7a29988d2bba841cb4a73dd2cf8761`

## Editorial summary

The revised finite-volume score is now centered correctly, and the distinction between typical KL odds and expected Chernoff/testing error is conceptually right. The posterior update also explicitly conditions on the newly observed block, repairing the previous predictive-only Bayes formula.

The exact-observation model, however, is incompatible with the B2 trace hierarchy used to restart every controlled block. Conditioning a deterministic continuous observation normally produces a posterior supported on a level set and singular with respect to Liouville volume. It need not have `L1` correlation densities, incoming boundary traces, or the B2 analytic source chart. The claimed conditional Laplace principle and kinetic contraction therefore have no foundation. The continuous-parameter posterior-error proof and game selector theorem also omit essential denominator and continuity arguments.

## Major mathematical objections

### 1. Exact noiseless observations destroy the B2 trace-regular density class

The observation `Y_k` is a Borel function of the deterministic hard-sphere block path. Given an exact value `Y_k=y`, the posterior on the initial or terminal microstate is supported on the level set

\[
\{z:O_k(\Phi_{[0,\Delta]}z)=y\}.
\]

For a nontrivial finite-dimensional continuous observation this set typically has positive codimension. The regular conditional probability is then singular with respect to the ambient Liouville measure. A simple model already shows the issue: if an absolutely continuous random vector `Z` is observed through `Y=Z_1`, the conditional law of `Z` given `Y=y` is supported on the hyperplane `Z_1=y` and has no full-dimensional density.

B2's state, by contrast, is a complete hierarchy of `L1` correlation densities with integrated incoming-flux traces and tangential derivatives. A singular posterior level-set measure is not an element of that Banach space. Its factorial “moments” may be measures or distributions, not the densities `g_k` required by B2.

Thus the definition

\[
\|\pi\|_{\rm tr}=\|G(\pi)\|_{\alpha,\beta}^{\rm tr}
\]

is not finite for the post-observation posterior in general. Exact Bayes disintegration does not preserve trace regularity. The entire block-restart mechanism of `lem:r6-c1-source` and `thm:r6-c1-contraction` fails unless observation noise, positive-width bins, or a new singular conditional-measure theory is introduced.

### 2. Conditional expectation does not give the asserted trace-norm estimate

The manuscript writes

\[
\mathbb E\|\Pi_k^\varepsilon\|_{\rm tr}
\le C_k\|\Pi_0^\varepsilon\|_{\rm tr}e^{Ck\Delta e^{CR}}.
\]

There is no Jensen argument for this statement because `Pi_k` is a random probability measure obtained by disintegration, while the trace norm is defined only for absolutely continuous hierarchy densities. Even if one chooses conditional densities with respect to a reference measure where possible, conditioning can increase `L1`-Sobolev or boundary-trace norms without any bound; exact observations create delta-like concentration.

The average posterior measure equals the predictive measure, but

\[
\mathbb E\|\Pi_k\|
\]

is not controlled by the norm of the average. Norm convexity gives the opposite Jensen direction when the objects lie in a common linear space. The claimed “average trace norm preservation” is therefore both undefined in the singular case and unsupported in the regular case.

### 3. No strategy-uniform conditional pressure follows from the unconditional B2 theorem

B2 concerns a specific grand-canonical/tilted class of smooth initial hierarchy laws. The paper says its connected expansion is linear in the initial hierarchy and therefore applies to every posterior on a trace ball. This overlooks two issues:

- posterior laws depend on exact observations and strategies and may be singular, as above;
- even for regular initial densities, a uniform conditional large-deviation theorem requires lower and upper bounds with constants stable under the random posterior, not only an operator-norm estimate.

An annealed source expansion from the original law does not imply a quenched conditional Laplace principle after observing the same microscopic path. Rare observations can select precisely the configurations on which cluster estimates deteriorate.

### 4. The posterior-to-kinetic contraction assumes the desired Gibbs conditioning theorem

`thm:r6-c1-contraction` asserts that, conditionally on the resolved density/contact history, finite posterior marginals satisfy a uniform conditional Laplace principle with one regular minimizer. Its proof says: apply the B2 normalized tilt, use pressure derivatives and strict covariance, and obtain concentration.

This is not a proof of a conditional LDP. One needs the conditional normalizing probability of the observed history, a ratio theorem uniform in that history, and exponential control of exceptional observations. Strict Hessian positivity at one phase gives local uniqueness; it does not exclude remote phases or prove a conditional lower bound.

Moreover, the “strict quotient covariance” invoked here is the unproved B3 theorem, downstream of B2. The declared dependency order is therefore violated.

### 5. Compact relaxed controls do not by themselves give the measurable selectors claimed

The Bayes kernel is shown only to be jointly Borel. The one-step value is then said to be lower/upper semicontinuous in relaxed controls because the work and reward are continuous. Continuity of the payoff does not imply continuity of the posterior transition under disintegration. Conditional laws can vary discontinuously with the parameter and observed value, especially at zero-density observations.

To apply measurable minimax selection and obtain Borel upper/lower values, the paper needs a Feller or analytic-graph property of the belief-state kernel, plus the appropriate semicontinuity in each control. Standard Borel disintegration supplies measurability of some version, not these continuity properties. Elliott–Kalton strategy spaces add another noncompact functional layer not addressed by one-step relaxed-control compactness.

### 6. The continuous-prior Chernoff proof omits the posterior denominator

For two simple hypotheses, the inequality

\[
\frac{x}{1+x}\le x^s
\]

produces a Chernoff bound. For a continuous prior, however, the posterior mass outside `O` is

\[
\frac{\int_{O^c}r_0(\theta)L_\theta\,d\theta}
{\int_\Theta r_0(\vartheta)L_\vartheta\,d\vartheta}.
\]

There is no prior atom at `theta_0`, so the denominator cannot be bounded below by the single likelihood `L_{theta_0}` or by a posterior density value at one point. A local ball around `theta_0` must be integrated, and one needs a uniform local likelihood lower bound at a radius that may shrink with `mu_epsilon`, together with prior thickness and entropy control.

The proof covers `O^c` by finitely many fixed neighborhoods and integrates pairwise likelihood-ratio moments but never supplies this denominator bound. Pairwise Chernoff information is a plausible exponent under additional testing and local-prior hypotheses; it is not established by the argument given.

### 7. “Locally uniform typical odds” requires a uniform law of large numbers

The first part of `thm:r6-c1-testing` asserts local uniform convergence in `theta` away from nonidentifiable points. Pointwise pressure differentiability gives a law of large numbers for each fixed likelihood ratio. Uniformity over an uncountable compact set requires stochastic equicontinuity, a finite net with control of derivatives, and an exponential bound on the score supremum. Those are not proved. Analytic compactness of deterministic pressures does not by itself control the random likelihood process uniformly.

### 8. The LAN formula is corrected but wholly dependent on B3

Centering at `DQ_epsilon(theta_0)` removes the deterministic drift error from the prior version. The algebraic Taylor expansion is valid on a genuine finite-dimensional analytic family. The score CLT, positive information matrix, and total-variation BvM, however, are delegated to B3's unproved process/covariance theorem.

The BvM proof also needs posterior concentration on a shrinking local chart and uniform LAN under alternatives. The stated Chernoff bound only treats fixed complements, while the intermediate annulus between `M_epsilon/sqrt(mu_epsilon)` and a fixed neighborhood requires quantitative local testing. Positive Hessian alone is not a finite-volume testing theorem.

### 9. The kinetic game limit inherits unresolved B2 and B4 failures

The controlled Hamiltonian and Isaacs equation are formal consequences of an assumed controlled density/contact LDP and a valid comparison theorem. The B2 report identifies failure of the upstream cyclic estimate and lower bound; the B4 report identifies an invalid perturbed-test corrector and unbounded doubled cotangents. C1 cannot use those results as closed black boxes.

### 10. The exact finite information state is too large for the claimed density reduction

The state `(H,Pi)` retains the entire resolved observation history and a posterior over full microstates. Even with noisy observations, convergence of finitely many posterior correlations to one deterministic hierarchy does not show that the value function becomes a function of the one-particle density alone. Controls can exploit posterior higher correlations at the next block. A quantitative asymptotic sufficiency theorem is required; finite-projection concentration is not enough to pass a minimax DPP.

## What is actually improved

The prediction/observation split, Ionescu–Tulcea construction at a formal Borel level, exact finite-volume score centering, and KL-versus-Chernoff distinction are all appropriate corrections. They do not resolve the singularity of noiseless filtering or prove the controlled kinetic limit.

## Required reconstruction

A viable revision must:

1. specify noisy or positive-width observations that preserve absolute continuity, or build a new hierarchy theory for singular conditional laws;
2. prove posterior trace-class stability rather than infer it from conditional expectation;
3. establish a quenched conditional Laplace/Gibbs theorem uniform over strategy-reachable beliefs;
4. prove Feller/semicontinuity properties of the belief transition needed for selectors;
5. supply a continuous-prior denominator bound and local testing theorem for posterior error/BvM; and
6. prove asymptotic sufficiency of the reduced density state for the controlled value.

## Recommendation

**Reject.** Round six fixes the previous Bayes formula and statistical centering, but its exact noiseless observations generally produce singular posteriors outside the B2 trace hierarchy. The conditional source charts, posterior contraction, and kinetic DPP therefore do not exist on the stated state space. The statistical limit theorems also rely on unproved B3 inputs and incomplete continuous-prior testing.