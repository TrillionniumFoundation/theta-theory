# Submission and referee navigation — A2 v37

The controlling report is the v36 external top-four rereview at
`3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`. This package is an additive revision
of its author source `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`.
The primary entry point is [main.tex](main.tex); every mathematical dependency
is included from this directory. The native primary has 65 pages.

## 1. Main reading order

| Primary location | Pages | Source | Content |
| --- | --- | --- | --- |
| Abstract and §1 | 1–4 | main.tex, core/00_setting.tex, core/00f_global_overview.tex | Experiment, leading results, exact/finite distinction, stronger step condition and resource definitions |
| §2 | 5–7 | core/14_global_response.tex | Unknown-positive-set inverse, finite-field locality and complete translation-period rigidity |
| §3 | 7–12 | core/15_unregistered_footprints.tex | Unknown origins and scales, matching-free support inversion, full geometric fiber and finite reconstruction |
| §4 | 12–19 | core/16_sharp_stationary.tex, core/16a_shrinking_upper.tex | Effective boundary geometry, Hellinger contraction, stopped lower bound, shrinking-layer upper bound and matched stationary power |
| §5 | 19–25 | core/09_stationary_jitter.tex | Retained density-independent stationary inverse and finite boundary reconstruction |
| §6 | 25–29 | core/10_unknown_footprint.tex | Retained unknown footprint at known homothetic scales |
| §7 | 29–33 | core/12_rare_stationary.tex | Retained local rare-collision query and improved stationary reconstruction |
| §8 | 33–39 | core/13_unknown_scale.tex | Retained width and independent area normalization for unknown scale |
| §9 | 39–42 | core/11_stationary_information.tex | Retained range contraction and earlier stationary converse, with the old bracket related to §4 |
| §10 | 42–45 | core/05_comparison.tex | Observation categories, classical ingredients and literature comparison |
| Appendices A–H | 45–65 | retained core inputs | Complete localized, finite-control, period, packing, stopped-information and calibration proofs |
| References | 65 | references.tex | Complete bibliography |

Page numbers describe the qualified native layout. TeX labels in the proof
ledger remain the stable reference if another TeX distribution changes breaks.

## 2. New principal statements

| Result | Stable label | What a referee can check first |
| --- | --- | --- |
| Theorem 2.2 | thm:global-occupation | Stopped payoff over an unknown positive set; uniqueness, stability and exponential truncation |
| Theorem 2.4 | thm:global-response-rigidity | Translation covariance, permutation of separated positive components and support cancellation |
| Theorem 3.2 | thm:registration-rigidity | Independent width deficits and cancellation of a possibly infinite centered-support envelope |
| Corollary 3.3 | cor:registration-fiber | Necessity and sufficiency of common translation and footprint period offsets |
| Theorem 3.5 | thm:registration-finite | Coarse offset bound, orbit averages, transferred patch margin and charged scalar samples |
| Corollary 3.6 | cor:registration-finite-cloud | Finite nonperiodic component averages and relative centroid registration |
| Lemmas 4.1–4.2 | lem:effective-collision-boundary, lem:all-short-hellinger | Uniform geometry down to zero command length and treatment of both Bernoulli endpoints |
| Theorem 4.4 | thm:sharp-stationary-lower | Common-index packing reduction and information bound for stopped adaptive experiments |
| Proposition 4.5 | prop:shrinking-rare | Safeguarded bracket invariant, geometric confidence allocation and single-logarithm cost |
| Corollary 4.6 | cor:stationary-minimax | Identical physical class, law, loss and expected-cost criteria in the minimax chain |

## 3. Information and hypothesis map

| Statement family | Supplied structure | Recovered quantities | Additional finite conditions |
| --- | --- | --- | --- |
| Global scalar inverse | Convex components with common diameter and separation bounds; stationary positive footprint density; fixed compass | Occupation and complete expanded-component field | Finite iteration has an explicit reachable-field region and truncation error |
| Full period rigidity | Same global exact experiment | The entire translation group and rank-two crystallinity | Uniform finite period decisions are a separate theorem |
| Unregistered exact homothety | Labelled exactly homothetic supports at at least two distinct scales; independent unknown setting translations allowed | Ratios, centered footprint, each translated obstacle union and relative offsets modulo periods | No periodicity, scale-gap lower bound or smoothness needed for exact distinct-scale recovery |
| Unregistered periodic finite inverse | Bounded smooth periodic class, uniform footprint and boundary-mass bounds | Finite geometry, primitive data, free area and registrations to stated accuracy | Positive scale gap, patch margin and a coarse bound on setting translations |
| Finite nonperiodic inverse | Finite component count bounded in advance | The component union in a common frame and relative translations | Complete protected aperture; no periodicity or patch margin |
| Sharp stationary minimax power | One common known positive-scale uniform-disk experiment and one nondegenerate bounded smooth physical class | Necessary and sufficient polynomial attempted-bit power | Fixed confidence; the chosen pooled step satisfies the stronger rare-query separation |

Raw `F_i,R_i` are distinguished from `g_i=F_i-R_i`. The global inverse and
retained area normalization use differences. Direct-width calibration uses
the raw forward means. No global rare-event membership assertion is made:
the rare query operates inside protected boundary brackets.

## 4. Retained source and preservation

The v36 paper, v36 review, v35 paper and review, and v34 paper retain their
native tree identities. The new manuscript keeps all 162 reviewed labels and
all 43 reviewed proof bodies active. The source-preservation gate compares
those proof bodies byte for byte against the pinned v36 source.

The revision has 24 core TeX inputs, plus main.tex and references.tex. Its
233 labels, 59 proof bodies and 62 formal statements include sixteen new
proved results. Old theorem proofs have not been replaced by cross-references
to an earlier repository version. Introductory and comparison prose outside
those proofs is updated to reflect the new main theorems.

## 5. Reproducibility package

The committed source consists of the active TeX, six reading/audit documents,
three validation programs, one workflow and SOURCE_PINS.json. The manifest
hashes every source except itself; the qualified source archives and artifact
binding include the manifest itself. Generated evidence is kept outside the
source manifest under verification/current/.

The journal archive carries the manuscript at its normal internal layout.
The repository archive also carries qualification and navigation materials.
The receipt records the exact expected and actual commit, source hashes,
preservation checks, diagnostic and contract outputs, primary build status,
page count and artifact hashes. The binding associates the receipt, PDF and
source archives. A dirty development run cannot be reported as qualification
of a Git commit.

The two v37 revision branch names are source aliases, not separate manuscript
variants. The next review should pin their common SHA and the artifact from
the hosted workflow for that SHA. The controlling report remains unchanged.
