# A2 v82 proof and source ledger

Mathematical source: `80133d376cc28cc8f2555f58324a3285f9dcfb67`.
Base: v81 head `8315577eeb8dcc711c4c1c89fc804d132be2e52e`.
Controlling report: v80 review head `2edd50e3f97228432ab3c7a1e1f11618f8f45a09`.

## Principal dependency diagram

```text
Five projective endpoint/readout matrices
  [independent retained readings; clock-invariant full-rank channels]
       |
       +-- rank(P1) ------------------> visible component count
       |
       +-- joint K2,K3 projectors ----> channels and component probabilities
       |   [(W,kappa) distinct; no pairwise action gap required]
       |
       +-- component log ratios -----> observable unequal-action anchor
       |
       +-- five-value rigidity ------> absolute anchor actions and relative rates
       |   [fixed log-affine detector family; not all actions equal]
       |
       +-- three-value anchor inverse -> remaining actions, including coincidences
       |
       +-- gauge classification -----> only common weight/exponential ambiguity
       |
       +-- regular generating sheets -> covered exact return lift
           [canonical coordinates; mixed derivative margins; phase-domain cover]
```

The polynomial detector theorem replaces the affine nuisance by a fixed degree-q family and gives q+5 sufficient global clocks. The exact common-detector inverse from v81, the calibrated v80 inverse, and the conditional-law companions use different observation assumptions; they are not steps secretly required by the new principal proof.

## New mathematical assertions

| Source label | Proof mechanism | What the numerical checks do not establish |
|---|---|---|
| `thm:v82-main` | Rank, joint spectral recovery, five-value lemma, anchor recovery and exact gauge classification | General global uniqueness rests on the written proof, not example fitting. |
| `lem:v82-separation` | Strict sign of the second derivative of a log ratio; finite separating combination | A single simple reduced operator is not assumed. |
| `lem:v82-components` | Exact rank-one projector identity and column normalization | Generic tensor uniqueness is not newly claimed. |
| `lem:v82-five` | Four derivative zeros; quartic root sum lies below all observation clocks; pole cancellation | Five-clock global minimality is not claimed. |
| `lem:v82-anchor` | Observable nonzero second divided difference; three-value strict-convexity argument | No externally labelled unequal pair is supplied. |
| `prop:v82-stable` | Explicit four-clock Jacobian, finite spectral/minor cover, smooth local extensions | Arbitrary noisy outputs need not be exact latent models. |
| `prop:v82-three` | Rank-three map on four scalar parameters; action-changing level set | This is not a geometric sampling minimax lower bound. |
| `prop:v82-equal` | Common action factor cancels under projectivization | This does not invalidate the unequal-anchor positive theorem. |
| `thm:v82-polynomial` | Repeated Rolle, polynomial degree count, rational pole cancellation | Unknown unbounded detector degree is not covered. |
| `cor:v82-return` | Recovered sheets give actual canonical graphs; a covered finite Bezout word | Neither a global section nor missing phase coverage is discovered. |
| `prop:v82-physical` | Uniform independent release delay with class-wide bound and one source | It is not the older adjacent-flight apparatus. |
| `prop:v82-shear` | Explicit exact shear, three regular sheets, fixed-source survival detector and independent Vandermonde readings | Action coincidences are included; caustic/fold points are not. |
| `cor:v82-error` | Normalize a joint density with a marginal floor, then use the local inverse | No unproved geometric sampling-optimality claim. |

## Historical derivations consulted and retained

The v80 report was read in full, including M1–M20, T1–T15 and the suggested conceptual directions. The v81 blind-pencil proof, projective scale recovery, unpaired-return argument, common-clock construction, fixed-source lower bound, finite-observation theorem and scope table were inspected. The v80 intrinsic-action/Reeb and physical-compensation proofs were separately checked against the new claims. The older conditional, distance-registration, coverage and convex proofs remain active historical companions; this delivery does not claim a fresh line-by-line independent certification of every older appendix.

All paths below are relative to `papers/A2-v17-boundary-information-coarsening/`. The full v82 entry retains these v81 top-level mathematical inputs unchanged:

```text
article/v81/01_blind_pencils
article/v81/03_multisheet_example
article/v81/02_geometry_and_experiments
article/v80/01_introduction
article/v80/02_framework
article/v77/02_physical_clocks
article/v80/03_raw_records
article/v80/04_intrinsic_actions
article/v79/02_information
article/v79/03_robust_quotient
article/v79/04_statistics
article/v79/05_prefix_cancellation
article/v79/05_root_free
article/v77/04_distance_registration
article/v77/05_finite_coverage
article/v80/07_convex_suspensions
article/v80/08_regularity
article/v78/04_mechanics
article/v78/05_uniform_records
article/v79/09_robust_geometry
article/v80/09_physical_nuisance
article/v80/10_calibrated_statistics
article/v81/references
```

The old frontmatter is superseded only by the new title, abstract and principal theorem; its preamble is reused unchanged. The full bibliography wrapper preserves all inherited entries and adds the direct joint-diagonalization reference. Old article and review files are neither edited nor deleted. The old root README is preserved as `revisions/a2-v82/README_before_v82.md` using its original Git blob.

## Literature positioning

Allman–Matias–Rhodes, Anandkumar–Hsu–Kakade, and Bonhomme–Jochmans–Robin are primary predecessors for latent/spectral identification. The new scalar deadline-rigidity statement is not attributed to them. Generating-function calculus, the Reeb return primitive and the Bezout identity are classical components and are not presented as new standalone contributions. The directly added source is Bonhomme–Jochmans–Robin, Annals of Statistics 44 (2016), 540–563, DOI 10.1214/15-AOS1376; its title and journal details were checked against the authors' arXiv record 1603.09141.

## Verification boundary

Fifteen deterministic algebra/regression checks and the core native build are recorded in `VERIFICATION.md`. They detect implementation/algebra regressions, not every possible mathematical error. The main proof is written in the manuscript; independent mathematical review and author approval are separate from compilation and examples. The core reading edition is not the entire integrated manuscript.
