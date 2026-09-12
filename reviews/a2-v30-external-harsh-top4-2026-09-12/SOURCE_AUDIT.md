# A2 v30 review: source and execution audit

## Identity and access

Repository: `TrillionniumFoundation/theta-theory`. All manuscript readings used the authenticated GitHub connector and the immutable ref `46f4b1dc2f9609963cae6a80b3a0f458d88250e1`, not a public-web copy or the default branch. Its tree is `3f0e5d977e7fd85a71b246d72e893c1959e4cc09`. The source branch is `revision/a2-v30-complete-native-submission-top4-2026-09-12`. The previous-review parent is `8582aa1839dad65ae370e0920e94d7cfe5b1dfa4`.

Initial revision-branch discovery identified A2 v30 as the latest numbered A2 revision returned. A subsequent `a2-v3` branch search returned only that revision. During report preparation, the branch head was re-read and still matched the pinned commit. These are discovery observations, not a claim that every historical branch was ordered by commit date.

The authenticated comparison establishes one commit ahead of the previous review, no divergence, and exactly four changed paths. Three files are added and `main.tex` replaces one input line. No file is deleted. The separate previous main is preserved as `main_v29_preserved_before_v30.tex`; its addition was established by comparison metadata, not an independent local byte comparison in this review.

## Direct manuscript reading inventory

Paths below are relative to `papers/A2-v17-boundary-information-coarsening`. “Full” means the complete text of that module was read in the connector output, including continuation ranges where an initial response was truncated. It does not mean all references from the module were independently rederived or all files were locally materialized.

| Module | Reading scope | Authenticated Git blob |
|---|---|---|
| `main.tex` | Full native entry; exact local byte check; literal direct inputs counted | `a64ec22354c7411f8eeb9964b6146ed49264e5dc` |
| `article/17_adaptive_experiments_v30.tex` | Full; stopped coupling, physical budget and pilot proofs | `32501ed008f29b03a1f8d9054a954c70f5055bcd` |
| `article/17a_measurable_physical_coupling_v30.tex` | Full; exact local byte check | `b02d1de6b6f5e7392e409d47aefab0de1835b6ea` |
| `v6/10_experiment_transfer.tex` | Full; normalized/raw laws, failure atom, physical embeddings and scope | `c7c68620e16fda23fd1942cbfb6e5fdeddeb0077` |
| `v4/10_boundary_layers.tex` | Full, including continuation; half-line construction, relative determinant, physical law and corollaries | `892a88e37a24e591fa525013c41910c791e28e73` |
| `article/15_operator_comparison.tex` | Full; cofactor, trace transport and normalized sublevel stability | `886adb2d68e105723f41f6554eeec59391cab44c` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Full in three ranges; weighted inverse, envelope limit, smooth remainders, jet blocks and finite inverse | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/23f1_equivariant_density_extension_v29.tex` | Full; formula domain, equivariance, pairwise stability, quotient and witness | `f90531eae71f43486029a7dd042c249627aa22b8` |
| `article/01b_observation_hierarchy_v29.tex` | Full; common stopped space and retained-design qualification | `9ff3141c19ec00b669667c0a9226138a2698d234` |
| `article/23h_global_orientation_quotient_v29.tex` | Full quotient subsection; underlying global gluing theorem not independently reread | `ac9938ee655b8b63f069a0c79c467d227eca5ab1` |
| `article/01_introduction_v27.tex` | Introductory relative-law, intrinsic-inverse and physical-acquisition discussion, and beginning of local-information discussion; initial fetch truncated later | Pinned path; no local byte certificate |
| `VERIFICATION_V29.md` | Full author execution record; reported builds not rerun | `e73b1d950b1e647328c9a233b25aec182d0beb6d` |
| `README.md` | Full; still labels v29 | `b5e5e81b8e7ad9e11f9c86427c7d9b363a96fbe6` |

Repository-root `README.md` was also read in full, blob `eda66be0234cc6c5677c60e8e9878887dc13f103`. The preceding report at `reviews/a2-v29-external-harsh-top4-2026-09-12/REFEREE_REPORT.md` was read through its mathematical dispositions, build discussion, limitations and source key, with a continuation request. It was used to identify what was previously closed, not as a substitute for current direct verification. A truncated recursive-tree response was not treated as a successful full source audit.

## Exactly what was executed locally

Two source texts were materialized from the authenticated outputs and checked by the Git blob formula `SHA1("blob " + decimal_length + NUL + bytes)`. Both identities matched the connector metadata:

- `main.tex`: 6,430 bytes, 125 lines; SHA-256 `ae3e6e6800dad229dff4d41bb571aac680e1f197b249dd6fa78f7e0cd37c4661`.
- New coupling lemma: 3,762 bytes, 75 lines; SHA-256 `6800cb8fc20ba4efd21fe4e65475f839f65649b788964fa3a343bab0eb73a878`.

The main contains 50 literal direct `input` commands, including its preamble and bibliography. The complete list is retained in `source_identity_checks.json`. This is not a recursive closure check, a label/citation resolution audit, or a TeX build.

The independent diagnostic uses only the Python standard library. The following commands were executed, with zero exit status and byte-identical output:

```sh
python3 independent_checks.py > independent_checks.json
python3 -O independent_checks.py > independent_checks.optimized.json
cmp independent_checks.json independent_checks.optimized.json
```

Python version: 3.13.5. Checks remain active under optimization because failures raise explicit exceptions. The script covers 1,225 pairs of finite probability vectors, 36 finite stopped-policy cases, an exact retained pilot, noninjective observation and cross-parameter embedding guards, retained adaptive-design information, 20 anchor-transport slice checks, and the old fixed-anchor witness. The counts describe test cases, not formal theorem certificates.

Script SHA-256: `666919cb7714032ab584531f0826c3dce0c3e7c48ee53ef41a8cc4ce199aea25`. JSON SHA-256: `5a7690187c1697f992c91b325d3807030b37383561b585c5e2136dc2e40452bf`. The optimized JSON is identical and need not be stored twice in Git. Its copy is included in the local evidence package.

No independent rerun of the author's v29 diagnostic was performed. No symbolic proof assistant, billiard simulator or continuum numerical solver was used. All new finite diagnostics are expressly separated from the analytical arguments in the report.

## Repository and native-build observations

The authenticated v30 Actions-run query returned an empty run list and total count zero, including the final recheck. `REPOSITORY_OBSERVATIONS.json` records the extracted response and commit/comparison facts. It is not represented as an unedited dump of all API responses.

The inherited verification record reports a successful native companion and a selected-module fixture, while expressly leaving complete native-main execution open. This review read that record but did not rebuild the companion, decode its complete logs, inspect its PDF, or rerun previous hosted jobs. The old empty-step job observations in the previous report are inherited, not newly fetched job evidence in this round. No workflow, repository setting or permission was changed for this review.

## External literature scope

Primary sources were consulted through web search. Levin–Peres–Wilmer's author-hosted second-edition PDF was opened and printed pages 50–51 were inspected using screenshots (zero-based PDF pages 65–66). They contain the total-variation coupling characterization and overlap construction. No manuscript PDF was analyzed.

Bolotin–Treschev, arXiv:1006.1532, was checked at abstract level. De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4, was checked at abstract/version-metadata level. Finamore–Leguil, arXiv:2510.18983v1, was checked through its abstract, introductory enriched-marking description and Theorem A in the HTML text. No comprehensive priority or complete-proof comparison was performed. Bibliographic identifiers and qualifications are in the report.

## Not independently verified in this round

This review did not execute the native main build, inspect a complete main or companion PDF, audit the full recursive source closure, or check all source labels and citations. The finite-geometric foundation and differentiated-operator sources cited by the inspected forward modules were not all independently reread. The full Part II LAN/Poisson arguments, Part III global acquisition proofs, underlying intrinsic gluing and finite-signature theorems, companion mathematics, and every auxiliary chapter were not checked line by line.

The report therefore accepts the specific v30 technical addition and preserves the dispositions of specifically resolved objections without certifying the entire manuscript. Its C2 finding is an evidence/package finding, not a theorem-level counterexample. Completing C2 is necessary to answer the existing request; it would not itself establish correctness of all inherited mathematics or top-four significance.
