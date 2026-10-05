# A2-DYN v4: proof and dependency ledger

Base: `55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191`. Mathematical core: `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`.

## New results in the primary article

| Result | Label | Analytical inputs | New conclusion |
|---|---|---|---|
| Lemma 5.1 | `lem:uniform-half-hessian` | Exact optical action and interior minimizers of Section 4; norm Hessian formula | Uniform tridiagonal Hessian and two-sided coordinate decay via an averaged Hessian |
| Theorem 5.2 | `thm:quantitative-excess` | Lemma 5.1; exact append/truncate variational comparisons | Uniform two-sided excess increments and continuous uniform limit |
| Theorem 5.3 | `thm:log-period-separation` | Theorem 5.2; actual counts from Lemma 4.1 | Explicit polynomial discrepancy at large roof frequency; logarithmic physical-word budget |
| Corollary 5.4 | `cor:approximate-phase-bound` | Continuous circle-valued phase near the three regular cycles; exact telescoping | Quantitative essential-supremum phase error lower bound |
| Lemma 12.1 | `lem:compact-subadditive` | Compact parameter set, continuity, nonnegative subadditivity, pointwise vanishing normalized infimum | Uniform normalized convergence and finite-cover block budget |
| Theorem 12.2 | `thm:uniform-return-fluid` | Ergodicity, exact means, Theorem 11.2, cocycle invariance, Lemma 12.1 | Uniform mean and functional first-order law of actual return records |
| Lemma 12.3 | `lem:uniform-maximal-block` | Uniform integrability of return count/roof and finite horizon | Sublinear maximum return block; transfer to stationary length-biased base law |
| Theorem 12.4 | `thm:uniform-physical-clock` | Theorem 12.2, Lemma 12.3, exact marked suspension, monotone inverse | Uniform first-order physical visits/collisions/displacement; all-window unfinished-return control |
| Corollary 12.5 | `cor:physical-rate-error` | Theorem 12.4, exact mean derivative | Radius-error propagation for the physical rate, without independence |

Each entry has a proof in the active primary TeX closure. The two new core files contain nine proofs. The previous 28 proof bodies and all 78 labels are preserved; `PROOF_BASELINE.json` and `tools/audit_v4.py` check this mechanically. Nine old proof-bearing core files are byte-identical to v3. Only introductory and status prose changes in the other old core files.

## Retained dependency tracks

The actual marked suspension, winding periodic orbits and effective zero-roof lattice remain in Sections 2-3. The true excursion family, strict excess monotonicity, complete periodic annihilator, real rank and compact-frequency separation remain in Section 4. Section 6 retains the original-section raw critical-edge calculation; its normalization is not transferred to the enlarged section. Sections 7-8 retain the exact residual and localized inversion arguments. Sections 9-10 retain conditioning, Gaussian-clock and geometry interfaces, exact means and the full suspension. Section 11 retains fixed-record raw density and first-moment continuity, weighted denominators and uniform stationary finite endpoints.

## Dependencies not silently supplied

Theorem 5.3 is a periodic estimate, not a resolvent estimate. Corollary 5.4 explicitly assumes continuity at the selected periodic states; it does not prove measurable-coboundary regularity. Theorem 12.4 is at scale t, not sqrt(t). Neither result supplies the variance criterion, a continuous positive covariance, an all-central-branch residual sum, or weighted shrinking-interval local limits. Section 13 keeps these exact requirements for the original raw LLT.

No general-method novelty is claimed for Fourier inversion, the Morse lemma, ergodic theory, the elementary subadditive lemma, or renewal inversion. The new work is their detailed application to the specified actual return family and its quantitative period geometry. Finite sample checks certify only the printed finite statements they evaluate.
