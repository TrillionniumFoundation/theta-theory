# A2 v43 — journal revision

**Qian Qi, Scalar collision laws and recognition of periodic dispersing billiards**

This is the complete author revision responding to the v42 referee report,
commit `74787c9c353b72983fe1bb43af467e31d3eb0f2a`, reviewing author commit
`fffc85d4da8c8ee6369833369d564b1cffabc63d`. The report recommends minor revision,
conditional on the listed corrections and an independent specialist check; it
is an AI-assisted referee-style report, not a journal decision.

## Reading the submission

`main.tex` is the primary article. `companion.tex` is its technical supplement.
The exact inverse is self-contained in the primary. The finite interface is
printed in `core/29_supplement_interface.tex` and pinned in
`JOURNAL_INTERFACE.json`. The two PDFs and their complete TeX closures are
supplied together in `A2-v43-journal-package.zip`.

The unprefixed `PROOF_LEDGER.md`, `LITERATURE_AUDIT.md`,
`RESPONSE_TO_REFEREES.md`, `SUBMISSION_MAP.md`, and `SOURCE_AUDIT.md` all describe
v43. Historical front matter is preserved under `provenance/v41/` and
`provenance/v42/`; it is excluded from the journal-facing archive. The earlier
paper and review directories are unchanged. No manuscript proof was removed.
The versioned older diagnostic and validator modules under `tools/` are retained
code; only `tools/qualify_v43.py` is the current qualification entry point.

## Current statements

The default finite-law controller uses shared signed two-bit records. Its
separated bound is `N_geom(c a_m,delta/2) + C a_m^(-2) log(Cm/delta)`.
The `C m^2 a_m^(-4)` acquisition is explicitly the retained deterministic
all-node design alternative, not the default current bound. Neither bound
removes fine geometry or the exponentially small moment tolerance.

Exact whole-plane fields identify an arbitrary compact launch probability with
convex support and strictly convex obstacles, up to common translation. Finite
joint recovery uses quantitative geometry and yields `W_1` error. Finite
response prediction is local spatial `L^1`; uniform response prediction is
separately stated under a known `BV` density bound. Exact periods need no
periodicity premise; finite period decisions use a positive patch margin.

## Reproduction

In the repository, run from this directory:

```sh
python3 tools/qualify_v43.py --expected-head "$(git rev-parse HEAD)"
```

Publication qualification checks committed bytes, the frozen source inventory,
the unchanged v42 exact proofs and supplement interface, all retained labels
and proof bodies, both numerical suites in normal and optimized Python,
negative contract tests, both PDF builds, and stable cross-document references.
The exact-SHA receipt and artifact manifest distinguish successful execution
from source-only capture and local development. The workflow is
`.github/workflows/a2-v43-verify.yml`.

In an extracted journal package, `sh build_journal.sh` rebuilds both documents.
No revision-time source transformation is part of either build.

## Review status

The author-side minor corrections are recorded individually in
`RESPONSE_TO_REFEREES.md`. An independent human specialist confirmation has not
been obtained by this revision. `SPECIALIST_REVIEW_BRIEF.md` gives the five
requested proof tracks without manufacturing a certificate. Source checks and
finite models are supporting evidence, not continuum proof certification.
