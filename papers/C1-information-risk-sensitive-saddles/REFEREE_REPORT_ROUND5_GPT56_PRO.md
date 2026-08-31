# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — *Information States, Risk-Sensitive Saddles, and Controlled Kinetic Values*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `a811922180e67e29581d1806fadb4ca80c0b73e5`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/C1_POSTERIOR_STATE_BLOCK_GAME_LAN.tex`, blob `97789ba9d9f4b55325d7649e3ff90578c27536ff`

## Source-control verdict

The active C1 manuscript is unchanged from round four. It therefore retains the unresolved construction of the random conditional hierarchy state, overclaims posterior asymptotics, and depends on the unproved B2–B4 kinetic interfaces.

The round-five packet is not part of the manuscript. It makes a useful conceptual correction by declaring the exact finite information state to be a posterior law rather than a density alone. The proposed posterior update, expected contraction exponent, and LAN theorem nevertheless contain direct errors.

## Audit of the proposed round-five replacement

### 1. The displayed Bayes update omits conditioning on the new observations

The candidate defines the posterior at time `t` as

\[
\Pi_t^\varepsilon=\operatorname{Law}(Z_t^\varepsilon\mid
\mathcal F_t^{\rm res})
\]

and then gives the next posterior as the normalized pushforward of the current posterior under a tilted deterministic block. This formula describes the predictive tilted law at `t_{k+1}` before conditioning on the newly observed resolved history over the block. In general the actual posterior must also include the observation likelihood or disintegration with respect to

\[
\mathcal F_{t_{k+1}}^{\rm res}.
\]

Unless the entire block observation is already a deterministic function retained in the state and explicitly conditioned upon, the displayed update is not Bayes’ formula for the declared information filtration. It therefore does not prove a Markov transition on posterior states or a dynamic programming principle for the observed game.

### 2. The likelihood normalization is written with the wrong recursively controlled posterior

The first block may be normalized using the base posterior. After one control-dependent change of measure, the next conditional normalizer must use the posterior under that controlled law and under the actual observations. The theorem begins with an uncontrolled `Pi_t` and only later adds superscripts in the update. The consistency of these regular conditional probabilities across nonanticipative strategies is not constructed.

Mean-one normalization of one isolated increment is elementary. It does not establish a globally measurable controlled posterior kernel on the strategy space.

### 3. Expected posterior error is assigned the wrong exponent

The candidate claims

\[
\limsup \mu_\varepsilon^{-1}
\log \mathbb E_{\theta_0}
\int_{O^c}r_T^\varepsilon(\theta)d\theta
\le-\inf_{\theta\notin O}
\mathcal K_T(\theta_0\Vert\theta),
\]

where `K` is relative entropy.

This is false in general. Typical log posterior odds have a Kullback–Leibler rate, but the expectation of posterior error is controlled by testing/Chernoff information because rare likelihood-ratio events dominate the expectation. Even for two simple iid hypotheses, the Bayes error exponent is Chernoff information, generally strictly smaller than either directed KL divergence.

The round-four source had correctly distinguished KL odds from Chernoff expected error. The round-five candidate reintroduces the rejected formula.

### 4. The LAN score is centered at the limiting rather than finite-volume mean

The candidate defines

\[
\Delta_\varepsilon=\sqrt{\mu_\varepsilon}
(X_\varepsilon-DQ(\theta_0)).
\]

The exact exponential-family likelihood expansion is centered at

\[
DQ_\varepsilon(\theta_0),
\]

not at its limit. Local analytic convergence gives `DQ_epsilon -> DQ`, but no rate implying

\[
\sqrt{\mu_\varepsilon}
(DQ_\varepsilon-DQ)\to0.
\]

Thus the asserted LAN expansion can contain an uncontrolled deterministic linear term. This is exactly the finite-centering error corrected in the round-four D1 packet and then reintroduced here.

### 5. The Bernstein–von Mises theorem is far stronger than the supplied inputs

Finite-dimensional LAN on compact `h`-sets, even if corrected, does not alone yield total-variation posterior convergence. One needs uniformly consistent tests outside local neighborhoods, prior thickness, local asymptotic quadraticity on expanding balls, and control of nuisance/nonidentifiable quotient directions.

The candidate’s global tail input is the false KL expected-posterior theorem. Therefore the BvM conclusion is unsupported.

### 6. Posterior stability is not proved on the declared class

The set of posterior laws with bounded hierarchy norm and relative entropy is called a compact posterior class, but no topology or compactness theorem is stated. The Bayes denominator can be exponentially small for some realized histories; Jensen’s inequality does not give the uniform lower bound needed to control posterior hierarchy norms over all strategies and histories.

Uniform source derivatives of unconditional B2 pressures do not imply strategy-uniform derivatives of random conditional pressures.

### 7. The posterior-to-density contraction is assumed

The adaptive-game proof says that the exact state is `(history, posterior)` but the posterior coordinate contracts to the resolved density in the kinetic limit. This is a nontrivial nonlinear filtering/propagation-of-chaos theorem under controlled exponential tilts. It is not proved by half-relaxed viscosity limits or by ordinary B2 compactness.

### 8. All controlled kinetic conclusions remain downstream of invalid inputs

The proposed game uses B2 source sewing, B3 pressure Hessians, and B4 comparison. None of those model-specific theorems is established. The generic separation of one-time preparation, reward-only control, and adaptive law control is correct bookkeeping but not an independent top-four result.

## Genuine improvement

The candidate correctly identifies a posterior probability law as the exact information state and uses conditional normalization rather than a fictitious Poisson compensator. It also keeps the three game timings distinct. Those improvements should be retained.

## Required reconstruction

The authors must construct the controlled posterior transition including new observations, prove measurable strategy-uniform conditional kernels, restore the Chernoff/testing exponent for expected posterior error, and center LAN at the exact finite-volume mean. Any BvM theorem must be limited to a precisely verified canonical experiment with uniform tests and tail control.

## Recommendation

**Reject.** The active paper is unchanged. The unmaterialized candidate improves information-state typing but gives an incomplete Bayes update, assigns KL rather than Chernoff information to expected posterior error, and repeats the finite-volume centering error in its LAN theorem.