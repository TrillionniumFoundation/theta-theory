# Round 53 primary-source audit

Accessed 5 September 2026. This is a targeted comparison, not an exhaustive priority search.

## Sarkar–Rakhlin–Dahleh

Sources: the authors' preprint [arXiv:1902.01848v6](https://arxiv.org/html/1902.01848v6), dated 8 April 2020; and the [JMLR journal record](https://jmlr.org/papers/v22/19-725.html), *Finite Time LTI System Identification*, JMLR 22(26), 1–61 (2021), with its journal PDF. The journal Assumption 1 page was inspected as a rendered PDF as well as text. The input-Gram and error analysis in preprint Sections 10–11 were read. Section numbers below refer to the preprint.

Assumption 1 allows isotropic sub-Gaussian excitation. Section 11 analyzes sub-Gaussian inputs. Algorithm 1's Gaussian pseudocode is therefore not a theoretical bounded-input obstruction. A scalar Rademacher input meets the required centering, variance and sub-Gaussian conditions. This corrects the incomplete Round 51 comparison.

Our derived experiment map is stated in `ROUND53_REVISION.tex`, Section 7.1: at regular-duration readout endpoints, the sampled state obeys `z_(i+1)=U z_i+a H B S_(i+1)`. The finite-section stability and response-sum bounds are proved in the manuscript. Zero process noise removes its error terms while input excitation remains; this is a proof-level specialization, not a claim that zero covariance satisfies a printed isotropy normalization. Nonzero initial state adds a separate decaying response. Neither special case is presented as an intrinsic obstacle to FIR estimation.

Actual residual comparisons are irregular duration choices, history-dependent block baselines, the tail-uniform inverse to labeled physical coefficients, and complete nonlinear working-posterior contraction. A response estimator is reusable after checking its hypotheses and charging finite-section bias. No theorem from this comparator is silently asserted to supply the full posterior statement.

## Posterior robustness context

[Fanny Seizilles and Maximilian Siebel, arXiv:2603.28177v1](https://arxiv.org/abs/2603.28177v1), submitted 30 March 2026: the primary abstract describes heteroscedastic nonlinear Gaussian regression using surrogate likelihoods, proxy variances and approximate forward maps. Only that scope and bibliography are used here. Its full theorem-level applicability was not audited, and no uniqueness or priority inference is drawn from a difference in wording.

Our energy-transfer proof is self-contained. Its assumptions are a compact continuous predictable contrast family, deterministic entropy and prior thickness, conditional grouped information, fresh Gaussian noise, and a uniformly summable working-nuisance envelope. The true predictable discrepancy only needs a finite-horizon squared-energy budget relative to information. These are the specific quantities a further comparison should match.

## Historical derivation sources

`round51/model_inverse.tex` is byte-identical to the inspected `round49/model_inverse.tex` (Git blob `a61a885f02fbbe9ffa3f3e5524c1cb7e3076360e`). It supplies the moment/Gram secants and `Q^(25(J+1))` physical inverse. `round51/likelihood.tex` supplies the earlier complete-likelihood, entropy and grouped-square arguments. Both are explicit source dependencies of the new root, not paraphrased publication receipts. Their classical inverse-spectral references remain in the article. The Round 50 response and Round 52 report were read to distinguish inherited work from new claims.
