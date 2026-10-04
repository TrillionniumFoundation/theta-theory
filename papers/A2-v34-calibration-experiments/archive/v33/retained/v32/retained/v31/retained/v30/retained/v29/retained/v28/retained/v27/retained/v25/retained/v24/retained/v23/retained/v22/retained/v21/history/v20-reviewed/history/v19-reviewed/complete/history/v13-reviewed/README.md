# A2 v13 — nonlinear boundary laws and two-contact rigidity

Complete English revision, 10 September 2026. Start with `main.tex` and
`RESPONSE_TO_REFEREES.md`. The compiled local main manuscript has 123 pages;
the repository deliverable is the complete reproducible TeX source.

This revision responds to the independent A2 v12 report at review commit
`2ae2751f61224b66f314915fd5fc22f6321b606f`, reviewing author commit
`2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`.

## Reading map

Theorem 1.1: nonlinear relative physical law on a nonshrinking collar.
Sections 8 and 12–14: complete smooth energy invariant, Abel stability,
regularized binary observation and charged self-calibration.
Theorems 9.1 and 10.1: independent limiting-jet inverse and physical open image.
Theorem 11.1: the complete independent-contact two-flight inverse.
Corollary 11.2: finite-order analytic changes between short and limiting jets.
Theorem 11.3: the finite physical observation design with j0 = 2 for every
fixed jet order. The earlier long-bridge construction in Theorem 10.3 and
all auxiliary proofs remain active, not merely in an excluded archive.

## Build and reproduce

From this directory, with a standard TeX Live installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error two_collision.tex
pdflatex -interaction=nonstopmode -halt-on-error two_collision.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
python3 tools/verify_v13.py --output verification/v13.normal.json
python3 -O tools/verify_v13.py --output verification/v13.optimized.json
cmp verification/v13.normal.json verification/v13.optimized.json
```

The companion is built first for external cross-references. Verification
uses only Python's standard library. The finite-block reference module
contains the unchanged routine extracted from the reviewed v12 source.
`VERIFICATION.json` records the local build and diagnostic scope. Finite
algebra, source retention and a successful build are not proof certification
or a remote CI run. The full-profile exponent remains a sufficient bound.

## Preservation and source pins

All 212 reviewed formal theorem/lemma/proposition/corollary/proof blocks
remain byte-identical and active; the current total is 218. All reviewed
active inputs remain included. The prior manuscript directories and review
branches are unchanged. Replaced v12 front matter and metadata are retained
under `history/v12-reviewed/` using their original Git blobs. The full prior
review remains at its original repository path. New work is on a separate
revision branch; no merge, force-push or permission change is part of this
revision.
