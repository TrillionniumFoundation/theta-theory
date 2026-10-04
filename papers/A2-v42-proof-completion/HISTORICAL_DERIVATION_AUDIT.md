# Historical derivation audit — A2 v41

This revision is based on the completed v40 referee branch, not on an earlier author or review snapshot. The historical papers remain unchanged and supply a derivation record; they are not treated as independently published literature.

## 1. Frozen controlling objects

| Object | Git identity |
| --- | --- |
| Controlling review commit | `24baf07cf2952668d61881c727cc6417e952c76e` |
| Review repository tree | `f92ed0a753b6e21ef2525c01111a6a0e0711783b` |
| Review directory tree | `75107868144f15707ef63c465ffe14ca25244d4c` |
| Report blob | `aab6da8d2ee5964d1baf5527ffc84cf790db1956` |
| Review source-audit blob | `013cca509412cdc8603434a00de972ee2c72d094` |
| Review literature-audit blob | `b5a86e65e8c959a0d99784c9df24ab1f4adf712b` |
| Reviewed v40 author commit | `c5593b05546889f436ce858c327670d080aae204` |
| Reviewed v40 repository tree | `1e794c5161114d34a4d46e6e5b5cb50567dfc731` |
| Reviewed v40 manuscript tree | `3aab67827e78db4063d8a0b6b4f137286af96171` |
| Reviewed v40 core tree | `affdee32d295d87581908a57cbe90acbf79fe9e8` |

The report is [here](../../reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md). It supports the audited exact and finite chain and requests major revision on singular-law supports, nonsmooth curvature, finite proof details, closest-prior comparison and journal architecture. Its recommendation is not a journal decision. The present response is directed to the seven items in its §11.

The v40 preservation object contains both `main.tex` and `companion.tex`: 40 active TeX files, 402 labels, 95 formal result blocks and 92 proof bodies. The validator reads the deduplicated union of both documents directly from Git. Every one of those labels and proof bodies is retained in v41, and every baseline proof body is byte-identical.

## 2. Finite reversal and occupation

The directly inspected finite-chain antecedent is [v29 `core/01_reversal.tex`](../A2-v29-scalar-collision-tomography/core/01_reversal.tex), blob `e5cc7e7c52284ecb0b773a06a6d86dc1d6dd0a20`. Its pointwise balance is

\[
B_a(y)-B_{-a}(y+a)=\mathbf1_{\mathcal O}(y+a)-\mathbf1_{\mathcal O}(y).
\]

The same physical conventions remain: a free start that reaches the closed obstacle on its unreflected segment gives one; a solid start or a free miss gives zero; all attempts are included. Integrating against one stationary law gives a translation difference of occupation. Nonnegativity and a zero along each finite chain recover occupation by the prefix maximum. In v40 the geometric gap supplies a chain length bounded by `floor((D+Delta)/t)+1` using only two fixed opposite commands. V41 preserves that proof verbatim and supplies the explicit support and a.e.-class arguments on which its geometric use depends.

The [v31 mean-exit inverse](../A2-v31-reciprocal-command-reconstruction/core/09_mean_exit_inverse.tex), blob `f6147757d0a82b2c5ff1e0debd26a4e9f33f9f74`, is a separate historical realization of occupation recovery. It uses a computational random walk, a bounded stopping identity, exit tails and a Bellman inverse under its own reciprocal preparation model. The fixed directed chain does not replace that older theorem's hypotheses; its full programme remains active in the supplement.

## 3. Directional-germ and two-field identification

The reviewed v39 author is `f815a7acdb5c03e03b9996fc7052b405db66936d`, manuscript tree `e60aaed448b772942ffd38d556babab35b3c3880`, core tree `113a60e9545374aee5ae6fd80b14f4fedf8e8ed6`. Its controlling v39 review is `790654161f2f069fb4d1d1ee18bfe86ea5290d74`, review-directory tree `99a365ce0caa40d473dd89c9e2e4bd8f869796d5`.

| Historical source | Mathematical contribution retained |
| --- | --- |
| v39 `core/19_single_law_rigidity.tex` | Short-flight flux, angular density copies, complete translation fiber, response completion and periods. |
| v39 `core/19a_one_resolved_component.tex` | One resolved obstacle, minimum-area pure-copy selection and odd-flux occupation recovery. |
| v39 `core/20_single_law_finite.tex` | Positive regularization, rational acquisition and quantitative finite geometry. |
| v40 `core/21_two_field_rigidity.tex` | Fixed positive-length prefix inverse, three-support cancellation, negative chord atoms, full compact probability recovery and single-orientation comparison. |
| v40 `core/22_two_field_finite.tex` | Same-command rare tests, positive nominal hulls, chord regularization and the sufficient geometric exponent. |
| v40 `core/23_two_field_law.tex` | Finite mixed moments, positive law reconstruction, local mean prediction and the separate BV-density conclusion. |

V39's angular and length-continuum observation model remains attached to its own theorems. V40's fixed-pair theorem uses a different geometric separation: match `P=C-A` to the two collision supports, cancel `h_-A`, and recover `h_C-h_L`. The positive nonatomic obstacle measure and the negative segment atoms identify the chord. A compact occupation component then identifies the complete launch probability. The same reconstruction determines every finite-length response and the period group.

V41 does not replace this theorem. It supplies a full positive-measure support lemma, explicit graph strips for singular laws, a derivative-free arc proof, exposed-face formulas for surface-area atoms and an exact Jordan proof. These are the requested mathematical expansions of the two-field chain. The dense atomic example confirms the meaning of convex topological support for a purely atomic law.

## 4. Finite geometric inheritance and new detail

The supplement's `core/02_adaptive_boundary.tex` proves complete coarse clustering, interior centers, relaxed bisection and radial interpolation. Its label premise is now supplied by fixed-prefix occupation estimates and the two-command rare test. The original localized or randomized observation protocols are not additional inputs to the current experiment.

The cap mass proof in `core/09_stationary_jitter.tex` uses rolling-radius overlap and the boundary density lower bound. Its constants are uniform over the present footprint class. That file also contains the signed smoothing coefficients. `core/12_rare_stationary.tex` gives the fixed-accuracy normal construction; its geometric proof permits any specified fixed normal tolerance. The current two-direction test proves the free-start reserve at tangency by an outer tangent disk.

The period proofs in `core/03_period_recognition.tex` operate on complete recovered component geometry and a known positive whole-patch nonperiod margin. `core/15_unregistered_footprints.tex` proves the orbitwise invariance of that defect under a common summand and translation. The primary's interface states these exact dependencies and their conditions; the finite-cloud alternative omits the period stage.

The new Appendix A gives all constants and set comparisons needed to inspect the finite geometry argument: the `11t^2/16` free-start reserve, the grazing parameter rectangle, the `epsilon^(gamma+9/2)` positive cap mass, grid approximation uniform in the hidden displacement, numerical component assignment, complete-component cutoff and the signed plateau's Vandermonde determinant. These leave the sufficient exponent

\[
Q_{\rm pair}=\frac{(\gamma+9/2)s}{s-2}
\]

unchanged. It is still one third of the retained single-law sufficient exponent at the same `s` and `gamma`; the separate known-uniform-disk minimax benchmark remains a different experiment.

## 5. Finite law, factor consistency and sparse output

V40 already proved the moment mechanism with perturbation of the estimated geometric factor. V41 makes its numerical realization an actual positive factor: a rational convex polygon has an exactly computable area and exactly computable rational mixed moments. Variation distance between its uniform law and the true obstacle's uniform law controls both the factor moments and bounded convolution test moments.

A rational cutoff selects the entire protected occupation component pointwise, including boundary atoms. Finite-grid quadrature is proved conditional on every hidden displacement before averaging, so it uses no continuity of the launch law. The padded grid contains a quantized comparison law. That law may have irrational weights, while the minimizing rational linear programme has a rational optimizer. These are different roles and are stated explicitly.

The explicit factorial amplification and complete error budget give the existing finite transportation rate. A further rational column-elimination argument compresses the probability to at most `binom(4m+2,2)` atoms while preserving every fitted convolution moment. This is an elementary finite convex-combination reduction within the same experiment. The original candidate-grid upper bound remains valid; the final positive output is smaller. Neither the observation model nor its error guarantee changes.

The local spatial `L^1` prediction theorem and the stronger density and uniform-response result under a known zero-extended BV bound retain their original proofs and hypotheses. Exact Fourier completion is kept separate from these finite estimates.

## 6. Historical preservation and evidence

`SOURCE_PINS.json` records eleven fixed paper/review directory trees. The unchanged historical chain includes v40 and its review, v39 and its review, v38 and its review, v37, v36, v35, v34 and the retained v35 review. The workflow checks all of these actual Git tree objects. New work is confined to `papers/A2-v41-referee-response/` and `.github/workflows/a2-v41-verify.yml`.

The journal-source archive contains the complete current TeX union. The repository-source archive includes the response, proof ledger, audits, specialist brief and verification tools. The exact triggering commit, source-byte preservation, normal/optimized diagnostic parity, both PDF builds and cross-document stability are recorded in the qualification receipt. These records establish what was reviewed and built; they do not assert an external human or formal proof certificate.
