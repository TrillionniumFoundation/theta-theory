# Preservation and submission boundary

## Immutable starting point

Repository: `TrillionniumFoundation/theta-theory`.

The controlling review commit is `47fd795b7e4d80f9fe81e9798e73a05efc7fa8f7`, tree `c0f30d4cc3e583c3fd71de66f99538a53bba0128`. Its report blob is `5b981570c0b527d038f9e8bdb77b8f9fc76cd992`. The reviewed v88 source commit is `777a9c951d5ca94a5261a6585ab6548d267e21e4`.

The v89 manuscript commit is `3de72a935ce643ea22e522ba7a6c233331d76247`, tree `7f3cd07fab62c100c7c7d849fbaf6bfdec1098ad`, with the controlling review as its sole parent. A live GitHub compare of those commits returned `ahead_by=1`, `behind_by=0`, fourteen files, every status `added`, 2065 additions and zero deletions. This is a repository readback, not an inference from a successful TeX build. The subsequent response package adds only documentation and recorded results.

There is no main-branch merge, force push, report rewrite, archival deletion, or replacement of an inherited path. The review branch remains the PR base, not a destination silently moved by this revision.

## Exact principal-module preservation

The following v89 files use exactly the v88 Git blobs. Their contents were also reconstructed locally and their Git blob hashes checked before the full native build.

| Module | Git blob |
| --- | --- |
| `residues.tex` | `ee777186ec85289e96831e423256aae08b4cb161` |
| `algorithm.tex` | `58cb58454b62c0bec9fa662cc4e60fe1b523bdc9` |
| `statistics.tex` | `7714d619335f5c01bf4172605aef469b6b6a532c` |
| `relations.tex` | `2a908d0d2de838e20a48065c5662bfb89ece95fb` |

The polynomial module is newly written in v89 to add the requested proof details, while the entire v88 version remains untouched. The introduction is rewritten to organize the stronger general-degree theory. The bibliography retains all earlier entries and adds three realization/interpolation predecessors.

## Historical derivations consulted and retained

The v87 principal paper's arbitrary-rank action inverse and compact-fibre formulation were read against the v88 extension. Its principal-paper blob remains `45abc130f8bcebb347abbe895498b1a568bc7e7b`.

The v87 companion driver, blob `f677aa7d59263468a0ee45c0dea022677884b5c9`, retains its earlier shared-apparatus, detector, geometric and raw-acquisition sources. The v86 compact-surface detector derivation was read directly in `article/v86/04_meromorphic_structure.tex`, blob `f1ccb1a022f24d41156868b448e28775831562c7`. Its normalized differentials, divisor/period tests and sufficient genus-dependent clock budget concern a different observation law. The new polynomial sharp clock count does not reclassify that sufficient budget as optimal or subsume those detector spaces without proof.

The archive remains available in the inherited tree. This preservation statement does not claim that every page of every historical revision was reread or independently revalidated during this revision.

## Mathematical correspondence

| Retained v88 result | v89 location and extension |
| --- | --- |
| Normalization kernel and common-factor cancellation | Theorem 1.1; Lemma 2.1; general module in Theorem 5.1 |
| Positive fixed-channel local fibres | Lemma 2.2, with the finite-valued continuous-root argument |
| Arbitrary-capacity 2d-clock obstruction | Proposition 2.3; its low functional rank explicit; full-span counterpart in Proposition 2.6 |
| Diagonal root matching, including cross-component collisions | Lemma 2.4, now with explicit contour and touching-disk count |
| Channel-coordinate additive polynomial inverse | Theorem 1.1; observable strengthening in Theorem 3.1 |
| Affine pole recovery, two-clock gauge and residue condition | Lemma 6.1 and Theorem 6.2; unchanged proof module |
| Factor identification and intrinsic fibre envelope | Proposition 6.4 and the retained affine theorem |
| Explicit algebraic estimator | Theorem 7.1; general-degree observable guarantee in Theorem 3.1 |
| Compact residual inversion and whole-model honesty | Lemma 8.1, Theorem 8.2; polynomial counterpart in Theorem 9.1 |
| Positive product and complete-collapse families | Lemma 8.3 and Theorem 8.4; unchanged exact identities and singular limits |
| Degree-d positive lower bounds and real-rooted multiplicities | New Theorems 9.2 and 9.3 |
| Logarithmic action law, binary determinant and other regimes | Section 10, unchanged |

The exact local metric theorem is on its stated regular charts; the multiplicity theorem is neighbourhood minimax. Neither replaces the global one-sided inverse nor asserts a classification of all intersections with normalization cancellation and rank loss.

## Reproducible preservation check

After checking out the revision branch, run from the repository root:

```sh
git diff --name-status 47fd795b7e4d80f9fe81e9798e73a05efc7fa8f7 HEAD
git hash-object papers/A2-v17-boundary-information-coarsening/article/v89/residues.tex
git hash-object papers/A2-v17-boundary-information-coarsening/article/v88/residues.tex
```

Every diff status must be `A`; the two hash outputs must both equal the residue blob above. The same test applies to the other three copied modules. The branch workflow checks additions-only preservation. Local manuscript compilation was not misreported as a full repository checkout check.
