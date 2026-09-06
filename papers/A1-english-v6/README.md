# A1 English v6 — Sparse observation algebras and finite-horizon memory

**Author:** Qian Qi. **Revision date:** 6 September 2026.

**New revision branch:** `revision/a1-english-v6-sparse-sensor-streaming-2026-09-06`.
The parent is the latest source-pinned v5 review, commit
`171a7e20470d7e83a5b6b614f60a3434fd3145d7`, not an earlier v4 submission.

## Manuscripts and preservation

The revised principal manuscript is `main.tex` (16 compiled pages). Its seven
sections contain the full new proofs, not a plan or a theorem-only outline.
`RESPONSE_TO_REFEREE.md` answers E1–E4 and P1–P5 individually.
`PROOF_LEDGER.md` maps the statements to their hypotheses and proofs.

The **entire** reviewed v5 directory is also part of this delivery, verbatim,
as `legacy/`, with Git tree identity
`6e96d9e79bdc62bfb221500796400156dda59315`. It contains the full previous
manuscript, all sixteen numbered sections and appendices, the complete
foundation companion, tests, responses and historical material. Its original
location `papers/A1-english-v5/` is unchanged. No existing repository file is
removed or rewritten by this revision. The new principal text and the complete
retained proof companion can be assembled with `complete.tex`.

The split is an explicit organization of the full delivery: the new principal
argument has one central structural theorem; all prior control, positive-filter,
mechanical-response, approximation and cost-comparison proofs remain available
in full. Historical review-relative wording in `legacy/` is archival, not the
wording of the new manuscript or a current review claim.

## Central results

For a positive finite calibrated detector spanning
`W_A = span{t^a : a in A}`, with any finite nonnegative real exponent set
containing zero, a full-support prior and bounded lookup commands, the exact
continuous history-state dimension is

`d_A(n,m) = min{ n(|A|-1), |mA|-1 }`.

The proof constructs an attainable binomial product tangent and proves strict
mixed-moment transversality for every such prior. It does not merely reproduce
the review's isolated `span(1,t^2,t^5)` example. Integral sumsets give the
observation algebra's Hilbert function; a complete three-exponent formula
and asymmetric causal profiles follow.

A genuinely online filter stores one of `M` states after every report. Its
fixed-horizon prediction exponent is governed by
`D_A(N) = max_n d_A(n,N-n)`, with matching upper and lower powers
`M^(-2/D_A(N))` in the specified prediction experiment. A separate additive
control theorem gives an upper loss bound `C'_N M^(-1/D_A(N))`; that control
power is not asserted to be optimal. Persistent memory, input streams,
read-only calibration, and arithmetic workspace are distinguished explicitly.

The physical collision-bit comparison uses the same second-cartridge target
and total Bayes risk for both devices, at every state budget. Its partition
formula proves a positive four-state gain and an exact small-amplitude
resolution threshold. It is not a comparison of two separate regret baselines.

## Reproduction

Requirements for the principal manuscript: a LaTeX installation with `amsart`,
`lmodern`, `microtype`, `geometry`, `hyperref`, and `latexmk`.
Diagnostics require Python 3.10 or later and SymPy.

```sh
cd papers/A1-english-v6
python tests/test_v6.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
# Or run both:
bash build.sh
# Also compile the complete preserved v5 and assemble both manuscripts:
bash build.sh --complete
```

The local v6 run completed **101/101 checks**, including **1,057 exact positive
mixed minors**. The diagnostic streaming fixture covers 19,683 three-report
prefixes for each of five state budgets on its explicitly finite input menu.
It tests index-only updates; it is not used to infer the continuous-input
asymptotic theorem. The physical gain is enclosed using rational bounds on
pi and sqrt(3), not replacements of those constants by rational surrogates.

The principal PDF was compiled and all 16 pages rendered for layout inspection;
key proof pages were inspected at full size. There were no unresolved references,
undefined citations or overfull boxes. The complete legacy manuscript and the
combined PDF were **not freshly compiled in this run**. Their build entry is
provided, not reported as executed. See `BUILD_REPORT.json` and
`DIAGNOSTICS.json` for the exact execution boundary.

These are author-side analytic proofs and executable diagnostics supplied for
further referee examination, not formal verification or a journal acceptance
claim. No new audit of the entire eleven-paper program is represented here.
