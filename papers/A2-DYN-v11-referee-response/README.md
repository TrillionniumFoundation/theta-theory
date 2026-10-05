# A2-DYN — revision 11

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Qian Qi — 6 October 2026

This directory contains the complete revised article. Compile `main.tex` through `bash build.sh`; the output is `build/main.pdf`. The title, triangular physical family, actual displacement/count/flight-time record and raw mixed-density endpoint are unchanged. All **27** mathematical core files and **14** Python diagnostics of the reviewed revision 10 are preserved byte for byte. The complete article includes all inherited results and the two new core files.

## Frozen review and mathematical baseline

- Controlling review: `reviews/a2-dyn-v10-external-top4-review-2026-10-06/REFEREE_REPORT.md`.
- Review commit: `a42dc1401007f9f8025c916106884e09d7d864f0`; report blob: `e6732df7a22bc7e161ac4650e74e9fdce80d52b3`.
- Reviewed author commit: `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`.
- Reviewed mathematical core tree: `66cf9b07589443f8b7380199275ac801e738dba5`.

This response addresses the revision-10 report, not the earlier reports on revisions 8 or 9. The intended revision parent is the controlling review commit. `PUBLICATION_STATUS.json` records the actual delivery state separately from the mathematical source.

## New theorem

Theorem C and Theorem 22.5 prove an integrated central estimate with a mark at **any actual return**, uniformly for `0 <= k <= n`. For an insertion `a` supported in the section, set `M_a=||a||_infinity`, `V_a=||a||_BV`, and `alpha_a=integral a dnu`. Here `nu` is the full collision probability and the BV norm includes the section boundary. The marked complex measure weights the true record by `a((F_R^*)^k x)`. Its centered transform satisfies

`integral_{|v|<=2 n^(1/200)} |C^[k],a_n,R(v)-alpha_a exp(-v^T D_R v/2)| dv`

`<= C [M_a n^(-3/280) sqrt(log(2+n)) + V_a n^(-9/175)]`.

The cases `k=0` and `k=n` are the initial and terminal insertions. Every intermediate sequence `k=k_n` is covered without a separation assumption. The BV norm may grow as `O(n^kappa)` for `kappa<9/175` when the supremum norm is bounded. The insertion mass may be complex; this is not then a probability law. The original section probability is recovered with `a=s_R`, not with the bare section indicator.

The proof changes the orbit origin to the marked return and compensates the backward and forward collision sums exactly. It uses a multiplier between two **forward collision** spectral powers. It does not smooth a long induced composition, replace a random mark by a deterministic-time state, or assume induced mixing. Short and zero collision blocks are handled separately, making the result uniform up to the endpoints.

Corollary 22.6 gives the central estimate under an unchanged marked-return-state event, with the denominator and BV-growth cost explicit. This does not identify a final lattice-record event with a return-state event.

## Reading path and supporting files

`core/28_marked_return_band.tex` contains the new theorem and full proof chain. `core/29_norm_source_map.tex` is Appendix C, mapping the collision norm estimates to their source definitions. Theorem C is placed in the introduction alongside the retained Theorems A and B.

`RESPONSE_TO_REFEREE.md` answers all seven essential requests and twelve presentation comments. `PROOF_LEDGER.md` records dependencies and remaining hypotheses. `HISTORICAL_DERIVATION_AUDIT.md` explains the use of earlier derivations. `SOURCE_MANIFEST.json` freezes the baseline and new core hashes. `VALIDATION.md` distinguishes source tests, finite algebra, native compilation and continuum proof review.

## Validation and publication state

Local native compilation produces **75 pages**, with **29** unique core inclusions, **98** proof environments and **289** labels. Normal and optimized Python diagnostics agree. The new finite checks include **26,880** marked compensation cases and **243** chronological operator pairings, with **165** negative controls detecting the wrong insertion time.

The workflow `.github/workflows/a2-dyn-v11-qualification.yml` is part of the published revision source and qualifies the exact pushed SHA on the response/copy revision branches. Live branch refs and the corresponding GitHub Actions run are authoritative for remote publication and qualification status.

## Mathematical boundary

The new result is an integrated **central-frequency** theorem, not a weighted raw local limit theorem. It keeps the physical band radius `n^(-99/200)`. Uniform covariance positive definiteness, the whole complementary-frequency integral, the complete critical/singular residual sum and the multiple-time weighted raw estimates remain unproved here. The exact raw inversion conclusion remains conditional on these explicitly stated inputs. No independent human specialist approval or journal decision is claimed.