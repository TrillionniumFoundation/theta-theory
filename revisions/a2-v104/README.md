# A2 revision 104 — referee entrypoint

**Intrinsic finite-sheet reduction and reconstruction of metric quotients**  
Qian Qi · September 20, 2026

Revision branch: `revision/a2-v104-intrinsic-reduction-endpoint-reconstruction-2026-09-20`  
Mathematical/build source commit: `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`  
Source tree: `35629baf76a5add33c5a0e1a0c06ee4b271a9c60`  
Controlling v103 review: `f38495b78e52496d78b44cb5d461fbec65ff530b`  
Report: `reviews/a2-v103-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`

## Read the revision

The principal is `papers/A2-v17-boundary-information-coarsening/article/v104/paper.tex`. Its seven literal input files under `article/v104/parts/` form one self-contained article. Compile the wrapper from the paper directory, not from the nested article directory:

```sh
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder rigidity_v104.tex
```

The local native build produces an **18-page** principal, with no undefined references/citations, duplicate labels, LaTeX warnings, or overfull/underfull boxes. Exact source and local PDF hashes are in `LOCAL_VALIDATION.json`; this evidence covers the principal only.

## Principal new results

Theorem 2.2 derives inverse sheets from a polynomial finite map and quantitative discriminant/derivative bounds. Corollary 2.5 covers coupled weighted initial maps; Example 2.6 approaches a ramified discriminant at unequal scales. Theorem 3.1 identifies the tensor quotient extracted by that reduction.

Theorem 4.3 reconstructs every minimal endpoint representation in the fully visible class, in arbitrary endpoint dimension. Proposition 4.4 gives a nonempty open class in each dimension; Proposition 4.5 supplies a finite deletion criterion without the visibility assumption.

Theorem 5.1 determines native dimension, normalized secants, and sharp fixed/adaptive exact-ray counts for paired-contrast polynomial observations in every dimension. Corollary 5.2 realizes a native open family at every positive definite quotient and embeds the finite-map reduction into positive probability observations. Theorem 6.1 identifies the variational costs with efficient Gaussian discrimination; query counts are not sample counts.

Lemmas A.1–A.2 and Theorem A.3 give the local-algebra, proper-pruning, and real-accessibility arguments. Lemmas B.1–B.2 repair the clock quantifier and display all retained/free polynomial score columns.

## Review and preservation records

Read `RESPONSE_TO_REFEREE.md`, `CONTENT_PRESERVATION.md`, and `QUANTIFIER_AUDIT.md` with the paper. All paths inherited from the controlling review remain unchanged. Relative to the controlling review, the source head adds 15 paths, with zero modified or deleted inherited paths, as verified by GitHub's commit comparison.

The four volume entrypoints are `rigidity_v104.tex`, `rigidity_v104_supporting.tex`, `rigidity_v104_archive.tex`, and `rigidity_v104_complete.tex`. The supporting volume inputs the entire unchanged v103 principal. The archive inputs the entire unchanged v103 complete volume, including its earlier mathematical record. Appendix B is the operative clock-pair erratum; the historical source itself is not silently rewritten.

## Validation and native runtime boundary

From the repository root:

```sh
python3 scripts/check_a2_v104.py
python3 scripts/build_a2_v104.py --dry-run
python3 scripts/build_a2_v104.py
```

The checker passed locally using exact rational/symbolic arithmetic. It tests endpoint dimensions 1–4, native retained dimensions 1–5, the four ramified inverse branches, and the clock-pair quantifier. These are finite algebraic checks, not formal verification of the universal theorems.

The full builder first compiles the new principal, then runs the exact v103 builder in a detached worktree at its actual source trigger `618b0b098654f53e61a782138272349df92d16ad`. Only a successful v103 receipt permits reuse of its four byte-verified PDFs. All four v104 targets are then compiled, recorder inputs are bound to the source commit, and a composite receipt is emitted only after every stage succeeds.

Source-bound GitHub Actions run **35509714156** was observed **pending**, with no conclusion, for source commit `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`. Full archival compilation was not executed locally. Accordingly **R103.7 / R102.8 is not marked closed**. A future successful workflow is configured to commit the PDFs, native logs, source hashes, exact v103 replay, and `native/RUNTIME_RECEIPT.json` only to this revision branch. A queued job and this configuration are not success evidence.

The all-dimensional native classification is for the explicitly defined paired-contrast class; it is not an unproved extension to every higher-degree binary-mixture pattern. The endpoint fibre theorem is complete on its stated fully visible class, not a claim to classify every nonvisible or nonminimal representation. Those scope distinctions leave the inherited theorems intact.
