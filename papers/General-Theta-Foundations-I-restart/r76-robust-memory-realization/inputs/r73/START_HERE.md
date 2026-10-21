# Independent-reader entry — General Theta Foundations I, R73

This is an **author revision** of **General Theta Foundations I: Acquired
Geometry and Causal Resource Transfer**, by Qian Qi. It continues the complete
native R72 source and preserves the original research identity. The new center
is the structure and exact minimum of stochastic memory for compactly
reversible controlled responses, together with algebraic synthesis and finite
certificates. The paper retains its Annals / Acta / Inventiones / JAMS research
objective; journal suitability requires an actual independent assessment.

## 1. Fix the edition before reading

Use the [publication entry](../r73-reversible-normal-form-publication/START_HERE.md)
for the immutable **final source commit**, the three native PDFs, their hashes,
and the actual build and diagnostic receipts. Read `REVISION_STATUS.json` in
this source directory as well. If that file says
`UNSEALED_AUTHOR_WORK_IN_PROGRESS`, or the publication entry is absent, the
packet is an intermediate author checkpoint and must not be treated as a
completed, source-bound delivery.

The new branch is
`revision/general-theta-r73-reversible-memory-normal-form-20261018`.
Its preservation checkpoint
[`f3f3f4b521e866a49a567558f41ecd1a98d26363`](https://github.com/TrillionniumFoundation/theta-theory/commit/f3f3f4b521e866a49a567558f41ecd1a98d26363)
was explicitly unsealed. That hash is historical checkpoint provenance, **not
the final source SHA**. The branch name alone is also not an immutable edition.

The controlling predecessor is the complete native source at
[`5463d93f0f22a7459efba8c44af1f8b326d92c34`](https://github.com/TrillionniumFoundation/theta-theory/tree/5463d93f0f22a7459efba8c44af1f8b326d92c34/papers/General-Theta-Foundations-I-restart/r72-reversible-memory),
paper tree `5449385c491b0ef60a7744dcaa744f52d1e251fe`.
The latest applicable deposited substantive report is R65, at
[`358481b21ceeeedb1205ebd30f86982e32a2cb04`](https://github.com/TrillionniumFoundation/theta-theory/blob/358481b21ceeeedb1205ebd30f86982e32a2cb04/GENERAL_THETA_FOUNDATIONS_I_RESTART_R65_BOUNDARY_MEMORY_EXTERNAL_REFEREE_REPORT_R65.md).
That report assessed R65; it did not assess or endorse R66–R73. Many of its
technical requests were already answered before this revision. The current
response inherits those closures and identifies its remaining contribution,
generality and quantitative requests separately.

## 2. Recommended mathematical reading path

1. Read the current main article's overview and experiment definitions, then
   **the minimal response space and finite-realization criterion** in
   `sections/31-reversible-control.tex`. This fixes the observable quotient,
   compact reversibility, all-word response, pure initial label and bounded
   decoder conventions.
2. Read **the normal form and exact memory formula** in
   `sections/33-reversible-normal-form.tex`. The crucial proof constructs the
   identity-word projection on the original hidden machine, establishes only
   the sandwiched loop identity, and charges a mixed initialization to a live
   transient label. The full finite-chain convergence argument is in
   `supplement-normal-form.tex`.
3. Read **rank rigidity, the factorial two-command family, and the bounded
   decoder obstruction** in the same section. The two $S_3$ examples explain
   why the group, linear rank and permutation module do not by themselves
   determine the positive factorization minimum.
4. Read **exact algebraic synthesis** in
   `sections/34-algebraic-synthesis.tex` and **finite certificates and stable
   memory** in `sections/35-finite-certificates.tex`. The algebraic input
   promises, classical algorithmic ingredients and limited complexity claims
   are explicit. The period-four interval has a written rational certificate;
   the general quantifier-elimination algorithm is not claimed to have been
   executed by the accompanying finite diagnostics.
5. Read the main article's **original actual-history transfer theorem and
   proof**, then follow the current supplement according to the experiment,
   resource or geometric question of interest. The supplementary periodic,
   arithmetic, leakage, stopping, risk, reset, rank and geometry bodies retain
   their individual hypotheses. They are not all prerequisites for the new
   normal form and are not relabeled its corollaries.

The [theorem map](THEOREM_MAP.md) and `THEOREM_DEPENDENCIES.json` describe the
logical roles. `THEOREM_INDEX.json` supplies actual theorem numbers and pages
from the current paired build. The independent absolute-calibration companion
is compiled separately from its complete 34-file native source in
`companion-r58/`; the original ordered-measurement and reset companion sources
have their actual immutable locations in [PRESERVATION_MAP.md](PRESERVATION_MAP.md).

## 3. Read the response and the evidence at their proper scope

- [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md) responds separately to all
  ten major requests and forty technical comments in the controlling report.
  It distinguishes inherited closures, new strengthening and open questions.
- [RESEARCH_STATUS.md](RESEARCH_STATUS.md) states what the present proof chain
  establishes and what remains unresolved, including the older squared-sign
  risk frontier for general $M$ and general multi-command optimal feedback.
- [LITERATURE_AND_PRIORITY.md](LITERATURE_AND_PRIORITY.md) distinguishes
  classical stochastic-group, equivalence and real-algebraic methods from the
  manuscript's response-specific structural claims.
- `PROOF_AUDIT.md` and the source-bound publication receipts distinguish
  written proof scrutiny, finite exact diagnostics, floating diagnostics,
  native compilation, formal proof, human review and editorial assessment.
- [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md),
  `provenance/BASELINE_AUDIT.md`, and [PRESERVATION_MAP.md](PRESERVATION_MAP.md)
  explain the content-based source selection, refreshed historical inspection,
  immutable dependencies and retained proof bodies.

R65 Actions run `38861581555` succeeded at
`ee79ca9114f8009d62c056d07381b766645e3fc4`. That closes the old report's specific
terminal-run question. It is not an R73 CI result. Any R73 hosted execution
must be identified by its own actual run and matching SHA in the publication
record.

## 4. Reproduce the native build

The current source package is self-contained for the main article, current
supplement and retained absolute-calibration companion. It requires Python 3,
the versions listed in `requirements.txt`, a working `pdflatex` installation,
and the native TeX packages used by `preamble.tex`. Use an output directory
outside this source tree so generated files do not alter the input identity.

For a standalone or work-in-progress build, run from this directory:

```bash
python3 verify.py --draft --out /tmp/general-theta-r73-draft
```

Draft mode is useful for reading and checking the source; it does not provide
the immutable Git source identity required for the final delivery.

For strict source-bound verification, obtain the full final source SHA from
the publication entry and use an unchanged Git checkout of that exact commit.
From this paper directory run:

```bash
python3 verify.py \
  --source-commit FULL_FINAL_SOURCE_COMMIT_SHA \
  --out /tmp/general-theta-r73-verified
```

Replace `FULL_FINAL_SOURCE_COMMIT_SHA` with the actual forty-character source
commit. Do not substitute the unsealed checkpoint, a branch name, an
archive-local identity or the later publication commit. The verifier and its
receipt specify the actual source checks, document builds, diagnostic counts
and resulting file hashes. A successful command on an altered source tree
cannot be reported as success for the sealed source commit.

The two new exact diagnostic scripts can also be inspected and run directly:

```bash
python3 diagnostics_r73_normal_form.py
python3 -O diagnostics_r73_normal_form.py
python3 diagnostics_r73_certificates.py
python3 -O diagnostics_r73_certificates.py
```

Their finite identities and examples support the diagnostic record. The
general theorems are established by the written mathematical proofs, not by
the size of a test suite. The final receipt, rather than an expected total in
an earlier note, is the authority for which diagnostics actually ran.
