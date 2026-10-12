# General Theta Foundations I — restart R32 referee packet

## Fixed delivery

Title: **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**.

- Ordinary source: `6a62f90eff5357d6e47b3faeba13a25e8500dee8`.
- Artifact parent: `20838ed65f7ff50cda2cb726f393929e42d37c74`.
- Ordinary-source projection: `97c35f107294a7a07308ce06813507895f4a529c`.
- Latest completed external review: R29, `204a9cc62c2c1ce48d0668f35c4bbc326118ebd7`, exact local input `../review_inputs/R29_EXTERNAL_REFEREE_REPORT.md`.
- Latest previous completed ready article: R29, `09eda58be2297ce885c7f2b4447f24fec3a0c9b4`.
- R30 and R31 were research contracts only; the R32 intake preserves them by an explicit second parent, with canonical restart as first parent.
- Hosted build: run `38098908126`, job `114350537056`, success; source artifact `11686603529`, full artifact `11687650249`.

The final evidence commit is the direct child of the artifact parent and is the intended new revision/referee-ready target. Its SHA is obtained from the branch ref, not inserted circularly into its own content.

New refs:

```
foundation/general-theta-restart-r32-bayesian-curvature-research-2026-10-11
revision/general-theta-restart-r32-bayesian-curvature-2026-10-11
referee-ready/general-theta-restart-r32-bayesian-curvature-2026-10-11
```

The ordinary-source and artifact refs stay separate:

```
foundation/general-theta-restart-r32-bayesian-curvature-source-2026-10-11
artifacts/general-theta-restart-r32-bayesian-curvature-2026-10-11
```

## Main mathematical change

The R29 review asked for genuinely informative likelihoods and nonlinear Bayes updating rather than a neutral-report reparametrization. R32 gives one general theorem with complete proofs in `../main.tex` and the ten section inputs. It treats known positive raw instruments on a finite affine carrier obtained from executable future tests. Borel realization and finite closure are explicit hypotheses, verified by the two raw realizations; they are not asserted for arbitrary kernels.

For raw numerator `U_t(y,u)=a_t(y)+A_t(y)u`, report likelihood `ell_t(y,u)` affine in `u`, and normalized update `F_t=U_t/ell_t`, define the experiment-generated perspective potential

```
Phi_t(u) = integral ||U_t(y,u)||^2 / ell_t(y,u) d lambda_t(y).
```

If `X_t` is the exact predictive-test vector, `V_t=E[X_t | S_t]` is the actual finite-state barycenter, and `r_t=E||X_t-V_t||^2`, Theorem 2.2 proves the exact three-defect law

```
r_t = E Phi_t(X_{t-1}) - E Phi_t(V_{t-1}) + D_row,t + D_pool,t.
```

All three terms are nonnegative. `D_row` is within-old-label report quantization; `D_pool` is the additional loss when incoming conditional centroids merge into a common next label. Section 3 derives the likelihood-normalized Hessian from the raw numerator and likelihood. It does not assume a Fisher or covariance geometry. The row-mass quantization lower bound applies to every legal randomized Borel observer. Rowwise equality conditions are not misrepresented as global online attainment.

The same theorem proves matching checkpoint and internally clocked online laws from actual conditional small-ball upper mass bounds, compatible global covers, report continuity, and either a block-summable perspective-curvature certificate (C) or a same-actual-report metric stability certificate (P). With a bounded postcommit test `Z`, `E[Z|H_n]=X_n`, and `B_n=E||Z-X_n||^2`,

```
R_cp(n,M) = B_n + q_M(Law(X_n)),
R_cp(n,M)-B_n  asymp  M^(-2/d),
R_aut(n,M)-B_n asymp  (M-n)^(-2/d),  M >= n+1.
```

The constants are uniform in `n,M` for the stated experiment certificates. Exactly `n` reports with no free clock requires at least `n+1` total observer labels. The core physical count is preparation plus `n` reports plus audit, `N=n+2`. Section 4 proves the clock obstruction and integer geometric allocation; all phase labels are charged. The (P) implementation stores codepoints and uses current report plus current label, not a free exact posterior. The (C) barycenters are declared read-only program constants; finite-bit compilation requires the separately stated computational certificate.

**Inheritance is explicit:** R11 conditional pooling, R15 curvature/mass clock rates, and the R15 Gaussian-density and positive-congruence tools are retained and credited. The power `2/d` and the clock shift `M-n` are not claimed as first discovered in R32. The new connection is the normalized Bayes/Jensen defect and its combination with a second implementable stability route, which admits informative examples without the old `3*kappa<1` sufficient condition. The fixed passive theorem is not a claim to subsume the older controlled theorem.

## Two raw-kernel verifications of that theorem

**Theorem 5.1, Gaussian hidden-state reports.** The primitive experiment observes from the current hidden state and then makes a positive invertible transition. Means have the stated affine independence, covariance is positive definite, and the untruncated Gaussian likelihood depends on the current predictive state. Full-tail log-odds estimates give uniform acquired density, including near the simplex boundary. Positive transition gives same-report Hilbert-metric stability for arbitrarily weak positive mixing; no `3*kappa<1` restriction, truncation or free conditioning is used. Bounded categorical audit realizes the stated task.

**Theorem 6.2, noncommuting quantum instruments.** The primitive map is `I_H(rho)=T(K_H rho K_H)` with `K_H=sqrt(I+eta H)` and depolarizing-unitary positive `T`. The report density `tr((I+eta H)rho)` genuinely depends on `rho`; this is not the neutral Haar-orbit example. Positive-congruence inversion and its Jacobian give actual acquired density, while cone-metric contraction gives certificate (P). A finite randomized bounded audit separates all matrix coordinates. The observer is classical and all its state labels are counted; no quantum workspace is free. Corollary 6.3 allows noncontracting unitary phases separated by paid contracting phases, under an explicit block condition.

**Theorem 7.2, rank-changing acquired law.** A separate channel-then-measurement primitive instrument mixes a weak full-rank outcome with rank-one projective outcomes. Actual component weights `omega` and `1-omega` remain in the law. Proposition 7.1 gives

```
Xi_w(m) = sum_j w_j m^(-2/d_j),
```

with checkpoint `Xi_w(M)` and autonomous `Xi_w(M-n)` rates. Here full-rank and projective dimensions are `D^2-1` and `2(D-1)`. The pure component contributes zero perspective curvature, and the stated weighted curvature condition yields certificate (C). This is an explicit singular proof, not an interface declaration or renormalization of a low-mass stratum.

## Same-task composition and charged retained information

Propositions 8.1-8.2 prove task-compatible parameter-independent simulator composition and finite-precision perturbation. Simulator states multiply observer labels; workspace, program bits, arithmetic precision, physical reports and time are separate. TV perturbation is applied to the same stopped/scored experiment, and continuous-to-discrete numerical rounding is treated by a coupling/boundary certificate rather than a false TV proximity assertion.

Theorem 8.3 adds one genuinely acquired independent bit, an attained early erasure probability `a`, and an unobservable fixed calibration offset `theta=+/-delta`. The protected early-report deficiency is exactly `epsilon=a/2`. With `N=n+3` physical calls and `Q=max(1,M-2n-1)`,

```
R_cp - B_n  asymp  M^(-2/d) + delta^2 + epsilon,
R_aut - B_n asymp  Q^(-2/d) + delta^2 + epsilon.
```

The autonomous legal class is nonempty exactly for `M>=n+2`. The lower bound is over all Borel observers: either some post-bit phase has only one label and loses that independent bit completely, or every such phase needs two labels, leaving at most `M-2n-1` terminal labels. A two-lane finite observer attains the upper order. These are attained calibration/erasure alternatives, not lower bounds inferred from arbitrary error tolerances. `B_n` is a dynamic same-terminal-test oracle baseline, not a claimed monotone static-parameter learning curve.

## Retained mathematics and response to the report

`REFEREE_RESPONSE.md` and `REFEREE_COMMENT_CONCORDANCE.md` address all 12 major and 28 technical R29 comments. Appendix A makes retained energy degeneracies, circle optimality, row/global attainment, modular orbit constants and Borel chart sections explicit. Companion G is the complete R29 article. Companion F carries a new correction notice before its entire corrected temporal article; it is NOT described as the originally reviewed R27 PDF. Companions A-F and S-X remain independent mathematics with their original hypotheses.

The complete delivery is 23 native pages plus 353 companion pages, not a replacement obtained by dropping old proofs. The existing R4-R31 source subtrees and four canonical control files are retained. All source/proof/notation/assumption/counterexample/resource/pipeline/literature/scope ledgers are provided. Original v1-v96, frozen archive and realization branches are not updated. `HISTORY_COVERAGE.md` distinguishes fresh reading, inherited dependencies and mere preservation; there is no claim to have freshly certified every historical proof.

## Verification and remaining mathematics

38 isolated PDF builds with three passes each were executed in each of the hosted and independent environments. The independent run used the downloaded remote ordinary-source ZIP and preserved all 725 input files. The native normal/-O regression comprises 8386 cases: 1183 rational, 6625 integer, 578 floating; historical nested suites also pass and are not double-counted. All 14 PDFs/376 pages have equal normalized text and equal MuPDF rendered pixels at 97.2 dpi across TeX Live 2023 and 2025, but different cross-environment PDF bytes. All pages were inspected in contact sheets and the native paper/corrected cover more closely. The JSON receipts record the exact comparison boundaries.

No unrestricted adaptive-control theorem, unknown-kernel learning/regret law, arbitrary non-summable continuation classification, general infinite predictive carrier, arbitrary degenerate strata, unbounded stopping/infinite-horizon theorem or optimal program/workspace/time/simulator-state frontier is asserted. Some older noncontracting orbit and temporal results remain independent rather than being forced into the new block-stable theorem. The stated conditional proofs are complete submissions for renewed external checking, not claims of journal acceptance or proof/priority certification by tests.

Primary next-review targets: Theorem 2.2 and its Section 3 Hessian/three-defect proof; Section 4 clock/allocation proof; Theorems 5.1 and 6.2 raw hypotheses; Theorem 7.2 actual-mass singular extension; Theorem 8.3 all-observer retained-bit lower bound and implementation.
