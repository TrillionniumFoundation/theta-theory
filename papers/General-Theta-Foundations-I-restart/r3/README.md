# General Theta Foundations I — restart r3

**Acquired Geometry and Causal Resource Transfer** — Qian Qi, 7 October 2026.

The entry point is `main.tex`; the rendered article is `paper.pdf`. This is a new native restart revision, not a continuation of v96 numbering and not a replacement of the general problem by a realization. The exact r2 tree is retained beside it. All nineteen inherited formal results remain in the article.

The principal addition is Theorem `thm:bridge`, with the raw-flow verification `prop:recharge-flow`. It derives terminal acquired-mass error control for a nonstationary recurrent partition class and combines it with countable multiscale geometry. The additional singular, noisy-state and one-probe theorems answer specific outstanding questions of the latest r2 report. The full scope and remaining responsibilities are explicit in `SCOPE_AUDIT.md`.

## Rebuild

From a clean committed checkout, run:

```sh
cd papers/General-Theta-Foundations-I-restart/r3
python3 build.py --source-sha "$(git rev-parse HEAD)"
```

Requirements: Python 3 standard library, pdfLaTeX with amsart/lmodern/microtype/hyperref and standard LaTeX packages, and `pdfinfo`. The build checks every native source hash, labels, citations, includes and retained statements; runs old and new regressions in ordinary and `-O` modes; and builds in two independent clean directories. Only after byte-identical rebuild does it write the paper and receipts. These checks do not prove the continuum theorems.

The build receipt names the exact source commit. The artifact commit is its immediate child and changes only `paper.pdf` and `evidence/`. Final read-only verification binds both SHAs without a self-referential commit field. That final receipt is carried by the workflow artifact and the separate verification record, not used as a mathematical premise.

## Provenance and reading

Canonical restart: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
R1 report: `4454ad669ebdbccb93d10d828484600dce58845d`.
R2 report: `32350573ac91d4fbf2f79343622e43e4555dce2e`.
R2 artifact reviewed: `593c3f3077ef9565bcc4b71fdeed9c99287d23c2`.

This author-requested revision is offered for a fresh external mathematical review. Neither successful compilation nor an internal proof audit is a journal endorsement or an independent correctness certificate.
