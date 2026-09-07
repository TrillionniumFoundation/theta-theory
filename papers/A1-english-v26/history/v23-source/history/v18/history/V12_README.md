# A1 — English revision 12

**Sparse observation algebras and certified memory across exponent collisions**  
Author: Qian Qi. Date: 6 September 2026.

This is a complete English manuscript, not a replacement abstract, addendum-only
submission, or plan. `main.tex` builds the full principal chain and all retained
appendices. The new section is `sections/construction_stability.tex`.

## Submission identity

The controlling report is `reviews/a1-english-v11-certified-memory-2026-09-06/`
at commit `7492bf0d74236e866048ef9e5e5b28e4ea9a7f56`. Its reviewed v11 submission
is `f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0`. The revision branch is
`revision/a1-english-v12-referee-response-2026-09-06`.

The exact source identity is `SOURCE_MANIFEST.json`. The executed build writes
`validation/REVISION_VALIDATION.json`, `BUILD_REPORT.json`,
`PRESERVATION_REPORT.json`, and `main.pdf`. A source hash is an identity check,
not a proof certificate. The original review and v11 submission remain intact.

## Reading order

Read the manuscript first, then `RESPONSE_TO_REFEREE.md`. The latter maps every
P11/E11 request to a source label and executable evidence. `PROOF_LEDGER.md`
records the new dependencies and uniformity hypotheses.
`HISTORICAL_DERIVATION_MAP.md` identifies consulted historical arguments.
`NUMERICAL_EVIDENCE.md` explains the tested domains and their limitations.
`LITERATURE_VERIFICATION.md` pins the corrected external theorem reference.

## What changes mathematically

The full collision profile, arbitrary fixed full-support-prior theorem,
unconditional acquired-history lower bound, attainable dimension, global cover,
causal converse, and profile-adaptive exact M-label realization are retained.
The new construction theorem uses a reference allowance fixed independently of
any supplied transition targets. Paired-history stability gives Hausdorff and
covering-radius stability in finite moment data. One common imperfect numerical
name then constructs one program with regret `O(Xi_N + delta^2)` simultaneously
for all compatible experiments in a **specified dominated prior family**. A
positive rank-two experiment has the matching `M^-2 + delta^2` law for this
common-advice problem. No uniformity over all full-support priors is asserted;
the original fixed-prior result is not restricted to that new family.

The new prior-family and imperfect-advice statements are additional results,
not replacements for the original full profile or a weaker separated floor.
Classical greedy covering, Lipschitz propagation, and the elementary two-point
lower-bound method are not advertised as new principles. No assertion of
journal acceptance or exhaustive priority clearance is made.

## Preservation

The 10 pinned inherited core files are unchanged. All 62 v11 named results are
retained. Of its 59 complete proofs, 58 are byte-identical; the remaining proof
has only the P11.3 exact-arithmetic prose correction, pinned in
`PROOF_CORRECTIONS.json`. Nine additional proved results bring the full source
to 68 proof blocks and 71 theorem/lemma/proposition/corollary labels. Existing
v10 and v11 tests remain byte-identical. The legacy full v11 response and audit
maps are retained in `history/` as well as in their original directory.

## Reproduction

From this directory, using Python's standard library and a LaTeX installation
with AMS, Latin Modern, microtype, geometry, booktabs and hyperref:

```sh
python3 validate.py
```

For a source-only preparation check:

```sh
python3 build.py --prepare-only
```

The adjacent `../A1-english-v11/` is required only for reproducing the **old**
transition mutation, with its three source hashes checked before and after.
The new checker rejects a collapsed adaptive compiler call site before returning
a program. Its contract enumerates the fixed numerical lists independently of
the compiler's rounding, distance, greedy and transition helpers.

The physical adaptive diagnostics cover exact collision, gap `10^-12`, and gap
`1/7`, with successively perturbed coefficient/moment data. They cover a complete
finite two-command subexperiment and a continuous common-command line with an
exact posterior quotient; they do **not** test the whole command cube or the
four-cell five-trial resource phases. Exact finite covering radii for these
fixtures are computed independently by exhaustive graph colouring. Full details,
negative controls, tolerances, all stopping brackets, entries and payload sizes
are in `validation/V12_DIAGNOSTICS.json` after execution.
