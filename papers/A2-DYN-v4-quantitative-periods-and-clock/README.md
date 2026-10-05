# A2-DYN v4: quantitative periods and the uniform mechanical clock

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`, with its thirteen active core files and `references.tex`. Build it from this directory with `sh build.sh`; the native PDF is `build/main.pdf`. The validated local article has 29 pages. The author branch is `revision/a2-dyn-v4-referee-response-2026-10-05`; the referee-copy branch is `revision/a2-dyn-v4-referee-copy-2026-10-05`.

## New mathematics

Section 5 proves uniform Hessian and endpoint bounds for the exact nonlinear half action, two-sided exponential excess increments, an explicit polynomial periodic-phase separation using logarithmic-length physical words, and a lower bound for continuous unit-modulus approximate phases. In particular, for every radius and every positive integer m,

    400^(-m)/10000 <= E_(m+1)-E_m <= (49/100)^(m-1)/300.

Section 12 proves a parameter-uniform first-order functional law for the actual induced records and physical clock. Its proof includes the stationary length bias, the initial prefix, and the maximum incomplete return over the entire growing observation interval. A geometric collision-rate error bound requires no independence between the radius estimate and the observed orbit.

All 28 v3 proof bodies and 78 v3 labels remain active. Nine proved results are added; the complete article has 37 proof bodies and 107 labels. The nine older core files containing proofs are byte-identical to the v3 base. Existing paper and review paths are unchanged.

## Review entry and scope

Read `RESPONSE_TO_REVIEW_ITEMS.md`, `PROOF_LEDGER.md`, and `SOURCE_AUDIT.md` with the article. No A2-DYN-specific referee report was located in the documented searches. The response addresses the verified specialist handoff and the v3 analytical requirements; it does not invent a referee report or transfer the A2-GEOM acceptance recommendation.

The target remains the original geometrically uniform raw mixed-density local limit. Period discrepancy is not an operator resolvent or an integrable characteristic-function tail. The first-order functional clock is not the Gaussian-scale clock. The common operator/measurable-cohomology realization, covariance and all-central-branch residual estimates remain explicitly identified in Section 13. The full A3 shrinking-conditioning input is not declared complete.

The core tree is `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`, descended from v3 commit `55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191`. `VALIDATION.md` separates source/build evidence from mathematical proof and independent review.
