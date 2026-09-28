# Response to the A2 v18 independent referee — v19 revision

We thank the referee for the detailed report on `review/a2-v18-independent-harsh-top4-2026-09-11`. We have treated the report as a request for a stronger theorem chain rather than for a cosmetic rewrite. The v18 boundary-information and endpoint-critical arguments are retained. The v19 revision adds two new main theorems, reorganizes the active source around the theorem chain, expands the novelty audit, and fixes the notation/provenance items identified in the report.

Revision branch: `revision/a2-v19-signed-endpoint-rigidity-2026-09-11`.

## C18-E1 — general smooth rigidity was weaker than the even-contact inverse

**Referee concern.** The general smooth result recovered a symmetrized boundary-energy profile, while the explicit independent-contact jet inverse required individually even contacts and supplied leading geometry.

**Revision.** We now use a strictly richer part of the same physical record: the signed endpoint positions. After residual time is integrated out, the same-type limiting endpoint density is positive precisely on

`S_b(u)+S_b(v)<d`.

Therefore the support threshold `T_b(u,v)` is `S_b(u)+S_b(v)`, and the slice `T_b(u,0)` recovers the *unsymmetrized* half-line action `S_b(u)`. This is information that is deliberately lost by the scalar energy-profile observation.

The new theorem is `article/23a_signed_endpoint_rigidity_v19.tex`, Theorem `thm:v19-signed-rigidity`. It removes individual evenness, reflection symmetry, equality of the two contacts and supplied contact curvatures. The physical onset gives the gap `g`; from `a_b=S_b''(0)` one obtains

`gamma=asinh(g sqrt(a_0 a_1))`,  
`c_b=cosh(gamma) sqrt(a_b/a_{1-b})`,  
`kappa_b=(c_b-1)/g`.

For every degree `n>=3`, after lower jets have been recovered, the next pair of labelled graph jets enters the next action jets through

```
[[coth(n gamma), frak_r_0^n csch(n gamma)],
 [frak_r_1^n csch(n gamma), coth(n gamma)]].
```

Because `frak_r_0 frak_r_1=1`, this block has determinant exactly one. Thus odd and even labelled jets are recovered recursively at every fixed order. The proof is the nonsymmetric extension of the already reviewed v12 envelope calculation, evaluated on the historical linear half-line orbit. In the analytic class, equality of the signed endpoint-law germs and onset determines both participating analytic contact germs. The finite long-bridge support reconstructs finite jets with `O_M(tau^j)` error by the existing relative action estimate.

The earlier even-contact theorem is not deleted. It remains as a more strongly coarsened special inverse and an independent consistency benchmark.

## C18-E2 — endpoint experiment was a fixed-table simple experiment

**Referee concern.** The v18 critical experiment compared the finite endpoint law with the boundary endpoint law on a fixed table; geometry was not the statistical parameter.

**Revision.** `article/18a_vector_boundary_information_v19.tex` introduces a vector moving-support family

`f_theta=a_theta(w_theta)_+`, `theta in R^r`,

with normal support velocity `V=D_theta w_theta|_0` and intrinsic matrix

`J_Sigma = integral_Sigma a_0 V V^T / |grad w_0| d sigma`.

At the boundary rate

`n p_n delta_n^2 log(1/delta_n) -> 1`,

the retained-failure triangular array is locally asymptotically normal with information matrix `J_Sigma`. The theorem also gives the efficient local score estimator, the exact Gaussian testing profile and the sharp local quadratic asymptotic minimax value `tr(W J_Sigma^{-1})` when the matrix is positive definite.

For a finite-dimensional family of unknown billiard geometries, the endpoint support is

`w_{eta,d}(u,v)=d-S_{0,eta}(u)-S_{p,eta}(v)`.

Hence the matrix is an explicit boundary integral of the geometric support velocity. The signed-endpoint rigidity theorem implies that the collection of the two same-type endpoint experiments over a positive offset interval has trivial common information kernel on every fixed finite labelled contact-jet model. Compactness of the unit sphere then gives a *finite* set of positive endpoint windows with positive-definite summed information. Independent batches allocated to those windows add their information matrices. The relative law transfers the experiment to actual long finite bridges when the accumulated finite-to-boundary error vanishes; in raw preparations the effective sample size includes the success probability, so failed preparations remain charged.

This theorem is separate from, and does not replace, the v18 fixed-table coarsening result. The manuscript now states the distinction explicitly in the introduction and `article/01b_observation_hierarchy.tex`.

## C18-E3 — archive-like architecture obscured the theorem chain

**Revision.** `main.tex` now exposes two main parts only:

- relative laws and geometric determination, ending in the signed-endpoint rigidity theorem and the physical two-flight benchmark;
- boundary information and local experiments, beginning with scalar boundary information and the new vector LAN theorem, followed by the fixed-table endpoint hierarchy and stable profile inverse.

The old appendix modules are still compiled, but their long flat input list is collected behind the single entry point `article/99_auxiliary_compendium_v19.tex`. No mathematical module was deleted to shorten the paper. `ACTIVE_SOURCE_MANIFEST_V19.md` is the authoritative v19 source map; `PROOF_LEDGER_V19.md` records the active theorem dependencies.

## C18-E4 — novelty audit was explicitly non-exhaustive

**Revision.** `LITERATURE_VERIFICATION_V19.md` expands the audit by mechanism: classical nonregular endpoint models, parameter-dependent support and limits of experiments, recent optimal testing, multidimensional support-dependent covariance bounds, nonparametric support-boundary recovery, and billiard/spectral rigidity.

The manuscript now expressly concedes the established general phenomena. In particular, Smith's 1985 linearly vanishing endpoint regime, Hirano--Porter's parameter-dependent-support limit-experiment/minimax framework, and recent Shimizu--Otsu optimal testing work are not claimed as new. The retained claim is narrower: the regular-hypersurface logarithmic coefficient and its matrix form in the present linearly vanishing model, the retained-failure thinning law, the explicit billiard support velocity and determinant normalization, and the coupling with signed-endpoint rigidity that proves nonsingularity for finite contact-jet families and transfers the local experiment to actual long bridges.

## C18-M1 — `lambda` was overloaded

**Closed.** In `article/01c_geometric_setup_v18.tex`, the lattice translation in the channel index is now `ell`: `e=(a,b,ell)`. The symbol `lambda=varrho^2=e^{-2 gamma}` is reserved for the scalar return multiplier.

## C18-M2 — centered geometric derivative convention was not explicit enough

**Closed.** The formal setup now states

`t = j g_e(xi) + d`

and declares that all geometric derivatives in the relative law, the half-line actions/amplitudes and the limiting profiles are taken with `d` fixed. They are not derivatives at fixed physical time unless a statement explicitly says otherwise.

## C18-R2 / C18-R3 — stale README and confusing v17/v18 provenance

**Closed at the source-map level.** Both the root README and manuscript README now identify v19 as the active A2 revision. The large manuscript directory keeps the historical v17 filesystem name so that the reviewed source graph is not duplicated, but `ACTIVE_SOURCE_MANIFEST_V19.md`, the branch name and `main.tex` are explicitly authoritative. Historical v17/v18 ledgers and verification files are preserved as historical records rather than silently reused as v19 status documents.

## C18-R1 — no successful native full build was evidenced

We added `.github/workflows/a2-v19-native-build.yml` and triggered it on the v19 revision branch. GitHub Actions created run `34577476783` at commit `1f3bc3fec0cee52ffb3a3665aae171925b0027f7`. The job failed before the runner executed any step: the job record has an empty step list (`steps=[]`). This reproduces the infrastructure-level symptom noted by the referee for v18 and is **not** evidence of a TeX/compiler failure. We therefore do not label this item closed and do not claim a successful native build from that run.

The build driver itself still recursively traverses every `input/include`, compiles the original companion and `main.tex`, rejects unresolved references/citations, duplicate labels and missing glyphs, and records source/PDF hashes. The v19 source refactor is compatible with that recursive graph traversal. The revision metadata distinguishes this source-level audit from an actually executed native compile.

## Summary of the mathematical revision

The two conceptual objections are answered by strengthening the mathematics rather than reducing scope. The new geometric theorem uses signed endpoint support to recover general labelled contact jets, and the new statistical theorem treats the unknown geometry as the local parameter with a positive-definite finite endpoint design, an efficient information matrix and a sharp local minimax bound. The v18 core results and all earlier auxiliary developments remain present for independent re-review.
