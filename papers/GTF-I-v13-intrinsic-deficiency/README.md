# General Theta Foundations I — v13 intrinsic-deficiency revision

**English theorem–proof article, 23 September 2026.** The controlling report is the independent v12 report at `a03a574936230aedbe1a8d3f4cb5b1fbd9c8ceb3`; the reviewed v12 head is `a9f8e05640e8bb100178a3216fa6165482ca4676`.

The canonical manuscript is `main.tex` / `paper.pdf`. Its five sections develop the intrinsic deficiency theorem, endogenous common decisions, nonsummable regenerative average risks, and active hard-sphere realization. The companion `development.tex` / `complete-development.pdf` includes that article followed by the entire preserved v12 mathematical development, including all earlier bodies. The source files of every predecessor remain unchanged.

Start with `RESPONSE_TO_REFEREE.md`, then the canonical article. `PROOF_LEDGER.md` identifies assumptions and proof locations. `PRESERVATION_DIFF.md` records the exact local annotations to two preserved bodies. `HISTORY_AUDIT.md` and `PIPELINE_GRAPH.json` give the frozen mathematical dependency structure; `REPOSITORY_SNAPSHOT.json` is a separate branch-freshness observation, not a proof of a dependency. `LITERATURE_COMPARISON.md` identifies original texts inspected and the two outstanding original-source comparisons.

## Principal results

- `thm:v13-main`: attained private polynomial deficiency; complete hidden-mixture testing dual with priced finite selector; visible-seed zero-set theorem; optimized cost composition and risk transport.
- `prop:v13-rank`: nonnegative-rank zero set, exact private/hidden identity-channel resource laws, and a strict hidden/visible separation.
- `thm:v13-endogenous`: exact Bellman-optimal common compression on policy-generated supports, with a positive finite-table regret certificate.
- `thm:v13-average` and `thm:v13-cycle`: nonsummable stationary finite-register average risks with synchronous physical/register resets and width-uniform cycle transport.
- `thm:v13-active` and `cor:v13-active-average`: actual velocity interventions in microscopic hard-sphere trajectories; two-sided marked approximation before optimization, at fixed horizons and under regeneration.

These are statements in their stated categories. A hidden selector is not a free private register, a physically repeated reset is not an inferred ergodicity property, and finite-dimensional observable matrices are not finite-cardinality consumer memory. No claim of journal approval or independent proof certification is made.

## Reproduce

From a checkout containing the pinned source closure:

```sh
python -m pip install -r papers/GTF-I-v13-intrinsic-deficiency/requirements.txt
# Debian/Ubuntu: texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v13-intrinsic-deficiency/build.py
```

The build rejects changed input digests, unresolved references, duplicate labels, and overfull boxes. It checks every predecessor companion label and equal numbering of the shared canonical labels. It executes finite diagnostics in ordinary and optimized Python, designated negative controls, and the twelve predecessor suites. The resulting `evidence/BUILD_RECEIPT.json` records the actual checkout, compiler, files, pages, and executed checks; the receipt is reproducibility evidence, not an analytic proof checker. `evidence/COMPILED_SOURCES.zip` contains all pinned inputs, without font files.

The two original-source audits still open are Norberg's full filtered-experiment proof and the original Paull–Unger partial-machine proof. Publisher retrievals did not yield these full texts. Their absence is not filled with invented theorem numbers or priority claims.
