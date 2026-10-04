# A2 v41 — two-field referee revision

**Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.**

This revision responds to the completed [v40 referee report](../../reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md), frozen at commit `24baf07cf2952668d61881c727cc6417e952c76e`. The reviewed author source is v40, commit `c5593b05546889f436ce858c327670d080aae204`. The new revision is based directly on the completed review, with all additions confined to this manuscript directory and its new workflow.

Author branch: `revision/a2-v41-referee-response-2026-10-04`.

Equivalent delivery alias: `revision/a2-v41-referee-copy-2026-10-04`.

## Manuscript and reading order

The submission is one primary article with a technical supplement. The article is [main.tex](main.tex); its supplement is [companion.tex](companion.tex). They compile to `A2-v41-primary.pdf` and `A2-v41-companion.pdf`. Put the two PDFs in the same directory to retain their cross-document links.

The primary proceeds through the observation model and theorem-level literature comparison, exact joint rigidity, finite geometry, and finite probability recovery and prediction. Its two appendices supply complete geometric acquisition estimates and the estimated-factor moment construction. The finite section contains an explicit table and stated hypotheses and conclusions for every auxiliary supplement dependency. The supplement's theorem statements and complete proofs stand under their own observation models.

## Mathematical revision

The principal experiment remains the ordered pair of whole-plane forward mean fields for the two fixed vectors `te` and `-te`, under the same unknown stationary law. The exact theorem retains nonsmooth strictly convex obstacles, arbitrary compact probabilities with convex support, the gap `t + diam(A) < d`, common-translation uniqueness, exact response completion, and recovery of the full period group.

The new proofs isolate positive-measure convolution supports, the physical/open-strip boundary conventions, singular-law component matching and almost-everywhere periods. They derive the support-arc identity without boundary differentiability and prove the precise exposed-face interpretation of each surface-area atom. The signed measure and its Jordan decomposition retain singular continuous curvature.

The finite geometry appendix makes the tangential collar, grazing strip area, cap mass, finite-grid conditioning, complete-component cutoff, numerical assignment reserve and signed plateau explicit. The finite law appendix uses the exact moments of an actual rational polygon factor, a protected rational cutoff and a padded positive linear programme. A rational weight-reduction argument returns at most `binom(4m+2,2)` nonzero atoms while preserving all fitted moments, the objective and the transportation guarantee. It requires no new observations.

The finite hypotheses, sufficient rates and prediction norms remain those of the reviewed theorem. Exact Fourier uniqueness is distinguished from the finite moment estimate in the abstract, roadmap and theorem discussion. The resource exclusions and finite output representation appear beside the main finite theorems.

## Preservation and review materials

The full active v40 article/supplement union is the preservation baseline. All **402 labels and 92 proof bodies** remain; every baseline proof body is byte-identical. The current union has **46 TeX files, 456 labels, 113 formal result blocks and 110 complete proof bodies**. The primary has 13 literal TeX inputs and the supplement 35; their only shared inputs are the label-free preamble and bibliography. Eleven historical paper/review directory trees are fixed by Git identities.

- [RESPONSE_TO_REFEREES.md](RESPONSE_TO_REFEREES.md): response to all seven requested revisions.
- [PROOF_LEDGER.md](PROOF_LEDGER.md): new results and proof dependencies.
- [SUBMISSION_MAP.md](SUBMISSION_MAP.md): journal package and reading contract.
- [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md): primary-source theorem comparisons and inspected versions.
- [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md): exact historical inputs and mathematical inheritance.
- [INDEPENDENT_SOURCE_AUDIT.md](INDEPENDENT_SOURCE_AUDIT.md): AI-assisted internal mathematical and source audit, with its limits stated.
- [SPECIALIST_REVIEW_BRIEF.md](SPECIALIST_REVIEW_BRIEF.md): concrete questions for the requested subsequent human proof review.

## Build and evidence

The new workflow is [a2-v41-verify.yml](../../.github/workflows/a2-v41-verify.yml). Its checkout, source archives, diagnostics, article, supplement and receipt are bound to the triggering commit. It captures source before installing the TeX environment and preserves failure evidence. The upload name includes the complete commit SHA and run attempt.

For a committed checkout, from this directory:

```bash
python3 tools/validate_v41.py --expected-head <full-commit-sha>
```

For deliberate source editing, regenerate the manifest and make a development qualification:

```bash
python3 tools/validate_v41.py --freeze-manifest
python3 tools/validate_v41.py --allow-dirty
```

A development qualification does not attest an exact committed source. Final delivery requires the first command at the actual remote SHA and a successful workflow at that same SHA. Generated evidence is written under `verification/current/`; it includes the source manifest, both final logs and recorders, stable auxiliary states, normal/optimized diagnostics, source archives, PDFs and a receipt. The artifact binding records the hashes of these files.

The mathematical diagnostics are finite models and algebraic checks. The manuscript supplies the continuum proofs. The requested human specialist review is a subsequent review activity; no human report or journal acceptance is represented as having been obtained in this revision.
