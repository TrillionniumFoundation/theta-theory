# Audit, sources, and reproduction — A2 v39

## 1. Frozen scope

This ledger accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). The review date is September 13, 2026. The repository is private; its links require authorized access.

- Submission: `revision/a2-v39-native-complete-article-2026-09-13` at `dd0e5aefd49d200652afc3fc3f29f7a6f38ae326`.
- Tree: `e936d5f6f463ea51f7f4cccb862de9216d4c258d`.
- Previous referee: `ac0c9d136d5a14f5f5d60388253d3f197f478902`.
- Previous v38 submission: `7b506becac7fc51dc1ea4f5ab407389d1208b07a`.
- v39 increment commits: `eb6edfb72567ad23ff97adfcea254cfba6ee42c2`, then the reviewed head.

The revision head was re-read before publication of this review and still pointed to the frozen submission. A search for `refs/heads/review/a2-v39` returned no branch before creation. The new review is an additive descendant of the submission; it is not a manuscript revision or a merge into the default branch.

## 2. Primary repository source key and read coverage

All source links below use the immutable submission, except the explicitly identified comparison, historical referee commit, and hosted execution endpoints. “Read” means direct inspection of the fetched source, not a typeset page or a formally verified proof. The ledger does not claim that every transitive dependency was read.

| Key | Source | Direct coverage in this review |
|---|---|---|
| S01 | [Comparison from preceding referee to submission](https://github.com/TrillionniumFoundation/theta-theory/compare/ac0c9d136d5a14f5f5d60388253d3f197f478902...dd0e5aefd49d200652afc3fc3f29f7a6f38ae326) | Two-commit identity and nine-path delta; first increment patch read, second increment's changed source and checker inspected. |
| S02 | [Native main](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/main.tex) | Complete entry, abstract, input order, acknowledgments, appendix entry. Not the full recursively assembled article. |
| S03 | [Proof architecture](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/01d_proof_architecture_v39.tex) | Complete new 74-line roadmap. |
| S04 | [Operator comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/15_operator_comparison.tex) | Cofactor, trace transport, normalized sublevel integration, and corrected forward reference. |
| S05 | [Envelope minimax](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/65_envelope_minimax.tex) | Complete chapter read; changed opening compared with archived opening and commit patch. Its cited upper-bound dependency was not independently rederived. |
| S06 | [Two nonlinear boundary layers](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex) | Half-line construction, trace-class amplitude, full two-boundary factorization proof. Later physical-law material and all underlying finite-geometry/flux dependencies were not comprehensively re-audited. |
| S07 | [Signed endpoint rigidity](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex) | Lines 1–530: theorem, leading recovery, weighted inverse, finite envelope, functional smooth remainders, homogeneous isolation, last-jet block and recursion. Later applications are not claimed as a complete fresh audit. |
| S08 | [Single-offset inverse](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v26.tex) | Lines 1–220: density identity, interior stability, finite-flight corollary, periodic theorem and beginning of its composition proof. Separate gluing/lattice/signature chapters were not freshly re-proved. |
| S09 | [Vector information](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v26.tex) | Hypotheses, collar bounds, support decomposition, censoring, LAN, contiguity, finite likelihood lemma, identifiable quotient, original-law mean/centered fourth moment, hypersurface stability. Targeted tail reads resolved truncated initial responses. The separate likelihood-tilting supplement was not exhaustively re-audited. |
| S10 | [Compact local experiments](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/18a1_compact_experiments_v32.tex) | Complete finite-net lemma, compact vector theorem, fixed-window corollary, and scope remark. Separate multirate chapters and every transfer dependency were not freshly rederived. |
| S11 | [Common physical observables](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/25a_common_observables_v25.tex) and [global estimator](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/25b_augmented_global_reconstruction_v26.tex) | Record space, near-onset localization/mass argument, grid/cap pilot, estimated coordinate map and law continuity; separator proof, finite templates, sample/cap conditioning, increasing order and fresh-stage budget implementation. No claim to reconstruct all cited physical and analytic inverse dependencies. |
| S12 | [v39 source checker](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/tools/check_revision_v39.py) | Complete code read; not executed by this referee. Its default source scope and opt-in full-graph scope are distinct from a build. |
| S13 | [v39 native workflow](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/.github/workflows/a2-v39-native-submission.yml) | Complete configuration read; no workflow execution was dispatched by this referee. |
| S14 | [Run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34748124986), [job API](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34748124986/jobs), [artifact API](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34748124986/artifacts) | Independently fetched run/job/artifact metadata. The observed fields are preserved in EXECUTION.json, explicitly as extracted metadata rather than a raw full API archive. |
| S15 | [Root entry](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/README.md), [paper entry](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/README.md), and [introduction](https://github.com/TrillionniumFoundation/theta-theory/blob/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v27.tex) | Both entries read in full; principal introductory statements, data distinctions, related work and organization inspected. A guessed conventional v39 response filename returned 404; that alone is not treated as proof that no response exists anywhere. The narrower finding is that the current entries are stale and the nine-path delta adds no response/evidence index. |
| S16 | [Previous referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/ac0c9d136d5a14f5f5d60388253d3f197f478902/reviews/a2-v38-external-harsh-top4-2026-09-13/REFEREE_REPORT.md) | Dispositions, mathematical discussion, execution limits, R38-P1, and C2 read. Historical judgments and tests are not represented as new executions. |

### Selected directly returned Git blob identities

These identify retrieved source objects, not a complete local checkout or a compiler input manifest.

| Path relative to the native article directory | Git blob |
|---|---|
| `main.tex` | `f75f887804e494df63cf3fa12591cc9ccbd66409` |
| `article/01d_proof_architecture_v39.tex` | `907ec8811c103f4ba1c16d6e7295a13d5eee5547` |
| `article/15_operator_comparison.tex` | `f5b656ed89bb8813f48e0e192d8222d7196a334a` |
| `article/65_envelope_minimax.tex` | `298e83b3428d595f12cc62265deb6bf61b37c892` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/23f_single_offset_law_inverse_v26.tex` | `63ed36efd417cd23e6f869952627719de00e6ef7` |
| `article/18a_vector_boundary_information_v26.tex` | `6db9136e31c0e94bc09eddc5f261eab1b25be3ba` |
| `article/18a1_compact_experiments_v32.tex` | `176e2588344ce0646ed47c09c64f371d6d16a045` |
| `tools/check_revision_v39.py` | `ee137c3b2ff3e3503b168fd853fb728f673f1af4` |

## 3. Independently executed finite controls

The standalone program imports no repository code and creates no source snapshot. It uses Python 3.13.5 and mpmath 1.3.0 at 100 decimal digits. It uses explicit exceptions, not optimization-disabled assertions. No claim of an interval-arithmetic certificate is made.

Run from this review directory:

```sh
python -B independent_checks.py > normal.json
python -B -O independent_checks.py > optimized.json
cmp normal.json optimized.json
```

Both final executions returned zero with empty stderr and byte-identical stdout. The exact interpreter path and commands are recorded in EXECUTION.json. The committed RESULTS.json is that stdout.

- Script SHA-256: `bdcef7df447aa1c49632882adcab52abdf3b89a99767dbca541472659deba130`.
- Output SHA-256: `8d26f0a3ee9ab3b688f11da08ecaa91f0b4689104e2f47fbeecc08ef970277e1`.

**Moving-support model.** For `r=1+theta`, use `f_theta(x)=3(r^2-x^2)_+/(4r^3)`. The two support boundary points give information `J=3`. Root-density integration on the common support and an exact support-exclusive mass formula test `H^2/(theta^2 log(1/|theta|)) -> 3/4` for both signs, at four absolute shifts. This is a model satisfying the regular moving-support structure, not a claim that it is a realized billiard law.

**Original-alternative moments.** The null score is `S(x)=-3+2/(1-x^2)`. Put `ell=log(1/delta)`, `q=delta ell^(1/4)`, `c=sqrt(1-q)`, and the effective intensity `k=1/(delta^2 ell)`. Under the original alternative `theta=delta h`, exact antiderivatives give the truncated first and second score moments. Four values of ell and three h values are evaluated. The intensity is not rounded to an integer and no sample is drawn; these are moment/scaling diagnostics, not finite-sample simulations. At ell=16, separate quadrature checks the antiderivatives, with maximum discrepancy approximately `2.95e-95`. At ell=128, the mean and variance retain nonzero asymptotic corrections, exposed in the result file rather than hidden by a “pass” label.

**Pilot grid.** Exact rational arithmetic checks 216 centering cases with even flight numbers 2, 4, 100 and 10000. It checks grid coverage and the factor-j centering bound. It does not check a billiard's flux lower bound, phase-volume acquisition, or unknown-frame geometry.

**Finite/compact negative control.** On K=[0,1], let P_(n,t) be the point mass at one only when t=1/(n+1), and the point mass at zero otherwise; let every Q_t be the point mass at zero. Every fixed finite restriction eventually agrees, but the full two-sided distance is 1/2 and every small-radius TV modulus is one. The reverse-kernel minimax calculation is exact: max(q,1-q) is at least 1/2 and attains it at q=1/2. The code additionally enumerates a rational grid. This illustrates the necessity of the uniform modulus; the manuscript proves one and is not refuted by this example.

**Diagnostic-development correction.** An initial draft program incorrectly demanded that the shifted collar masses decrease monotonically at all displayed ell values. This failed for the negative shift. Finite shifted masses need not have that monotonicity; the final program checks the appropriate uniform inverse-square-root-log bound. The correction is recorded in EXECUTION.json. It is not a manuscript counterexample and is not concealed as a passing first attempt.

## 4. Literature records consulted

Only primary research records are used for the comparisons below. The review uses their declared settings and data, not an alleged complete verification of their proofs or an exhaustive priority search.

- **L1.** J. De Simoi, V. Kaloshin and M. Leguil, [Marked Length Spectral determination of analytic chaotic billiards with axial symmetries](https://arxiv.org/abs/1905.00890). Analytic open billiards with stated symmetry/genericity assumptions. Consulted to distinguish observation maps, not to assert subsumption.
- **L2.** D. Finamore and M. Leguil, [A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards](https://arxiv.org/abs/2510.18983). Finite-horizon Sinai billiards and enriched marked-length data. No reduction from these data to the manuscript's signed channel laws was established here.
- **L3.** A. Meister and M. Reiss, [Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors](https://arxiv.org/abs/1101.5248). Consulted for the pre-existing nonregular-regression/Poisson-boundary comparison, not as a proof of this manuscript's billiard-specific kernels.

## 5. What was not done

No complete repository checkout, full recursive source graph, native-main build, native-companion build, or manuscript PDF inspection was performed. The author's v39 checker and the preceding referee's regression program were read or discussed as source/history, not run anew. This review's finite controls are distinct programs with explicit scope.

A full fresh audit of the entire 36-input auxiliary compendium, all count–endpoint and other multirate applications, the full orientation quotient, and every periodic gluing/signature dependency is not claimed. No proof of global physical realizability of arbitrary nuisance splices is claimed. The report's positive findings are restricted to its directly inspected arguments and the stated dependency boundaries.

The review files preserve these limits so that a later referee can reproduce the actual controls without mistaking them for an acceptance certificate or a complete mathematical proof check.
