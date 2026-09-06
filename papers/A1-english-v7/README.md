# A1 English v7

**Sparse observation algebras, confluent directions, and finite-state memory**  
Qian Qi — 6 September 2026

This is the substantive revision of the latest source-pinned A1 v6 referee report, not a revision of an earlier similarly named A1 branch. It retains all 15 v6 principal results and adds 10 result labels with proofs. The 28-page principal text uses `amsart`; referee correspondence and execution bookkeeping are separate from its theorem/proof narrative.

## Reading and building

Read [`main.pdf`](main.pdf) or build [`main.tex`](main.tex). The source includes ten sections and a bibliography. Run from the repository root:

```sh
bash papers/A1-english-v7/build.sh
```

Requirements: Python 3.10 or later, NumPy, SymPy, and a TeX installation with `pdflatex`, AMS, Latin Modern, geometry, microtype, booktabs and hyperref. The build uses no shell escape, runs the 97-check v7 diagnostic suite, compiles three passes, and fails on undefined references/citations or overfull boxes. It does not claim efficient finite-precision synthesis of the abstract optimal filters.

The controlling report is [`../../reviews/a1-english-v6-2026-09-06/REFEREE_REPORT.md`](../../reviews/a1-english-v6-2026-09-06/REFEREE_REPORT.md), at immutable commit `414f8c43a6236586362c1532c00aa9b9da01fe64`. Its reviewed manuscript is commit `750a65ef62422e81307b4a61fd891ee42fa2639e`, [`../A1-english-v6/`](../A1-english-v6/).

## Main additions

Theorem 5.1 proves a uniform resolved checkpoint law for affine exponent families: the multiplicities of additive collisions give confluent orders, and those orders determine the entire anisotropic distortion profile in the full-future regime. The limiting logarithmic tests are analytical coordinates; the proof recovers their physical weights in executable query probabilities.

Theorem 7.1 proves the uniform streaming law

```
R_(M,5)^theta ~ max{M^(-1/2), theta^(2/5) M^(-2/5)}
```

for `A_theta={0,1,2+theta}`, every integer `M>=1` and `0<=theta<=1/2`, with constants independent of both variables. It uses a fixed positive detector, fixed labels and five trials. The crossover is order `theta^(-4)` states. Every lossy update is included; the shrinking Bayes formula has no division by `theta`.

Theorem 8.2 gives a same-payoff decision consequence. Dropping the weak coordinate from a particular four-moment history statistic loses order `theta^2`; an actual `M`-state streaming policy recovers a fixed fraction of that value for `M>=K theta^(-4)`. The erased comparator is allowed its four coordinates uncompressed. This is history postprocessing, not a raw detector erasure or a lower bound against every four-dimensional encoding.

## Review and provenance documents

[`RESPONSE_TO_REFEREE.md`](RESPONSE_TO_REFEREE.md) answers E1–E3 and P1–P5 individually. [`PROOF_LEDGER.md`](PROOF_LEDGER.md) identifies the new proof dependencies and preserves the previous result inventory. [`HISTORICAL_DERIVATION_MAP.md`](HISTORICAL_DERIVATION_MAP.md) identifies the actual historical text consulted. [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json) pins source hashes and the review base. [`REFERENCE_AUDIT.md`](REFERENCE_AUDIT.md) records the primary literature checks.

`validation/local/` contains the fresh v7 console receipt (97/97) and full unchanged-script v6 author (101/101) and referee (108/108) rerun receipts. They are not aggregated into a proof count. `LOCAL_BUILD_REPORT.json` describes the local 28-page build. Repository CI produces its own `DIAGNOSTICS.json` and `BUILD_REPORT.json`, whose runtime versions and PDF metadata need not equal the local ones.

## Preservation and source transport

The new branch starts from the exact latest review commit. All existing repository files, the complete v6 directory, its full `legacy/` subtree and earlier foundations remain unchanged. The original main results remain in the v7 principal manuscript; preservation does not rely only on leaving a discarded theorem in an archive.

The expanded UTF-8 sources are committed directly as Git objects, with
reused original blobs for the three verbatim sections. The branch-scoped
CI job verifies the source manifest, builds and tests the principal text,
and publishes its PDF and fresh execution evidence only to this revision
branch. It never force-pushes or merges. Its token is restricted to the
repository and the job checks the exact revision branch before publication.

The general checkpoint theorem assumes the stated full-future inequality. The matched uniform online and binary-decision laws concern the specified five-trial family, not arbitrary optimized acquisition problems. Constants may depend on the fixed prior and protocol. This is an author revision submitted for further scrutiny, not formal verification or journal approval.
