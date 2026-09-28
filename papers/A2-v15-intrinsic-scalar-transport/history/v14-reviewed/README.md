# A2 v14 — nonlinear boundary laws and two-contact rigidity

Complete English author revision, 10 September 2026. Start with `main.tex`
and `RESPONSE_TO_REFEREES.md`. The locally compiled main manuscript has
129 pages; its unchanged two-collision companion has 7 pages. The native
repository deliverable is the complete reproducible TeX source.

This revision responds to the latest same-v13 report at
`b3f0ad5843782c221651c9189fc156d20865cab1`, reviewing author commit
`0e54099f079232df233316ae6fe7986fc51b7ea1`. The earlier same-v13 report at
`f29d8f96e87bf46db2ffbe8217caa09563c5e536` is also addressed. This is a
new author revision for independent review, not an acceptance decision.

## Reading map

Theorem 1.1: complete smooth relative physical law on a nonshrinking collar.

Section 8 is new: Proposition 8.1 gives the attributed analytic normal-form
comparison in physical endpoint coordinates; Theorem 8.2 identifies the
smooth determinant amplitude as the normalized stable-branch linearizing
density, with its exact first-flight cocycle and mixed derivative limits;
Corollary 8.3 identifies the complete normalized stable-action width.

Theorems 9.1, 10.1 and 11.1 retain the full smooth Volterra inverse,
independent-contact limiting-jet inverse and physical analytic open image.
Theorem 12.1 and Corollary 12.2 retain the two-flight geometric inverse and
finite-jet coordinate equivalence. Theorem 12.3 gives the two-flight window
experiment in each constructed locally full-rank finite-jet family.

Theorems 13.1, 15.3 and 15.5 retain Abel stability, regularized full-profile
preparation and the separately charged smooth-class pilot. All auxiliary
endpoint, count-only, coalescence, smooth-remainder and collision-record
proofs remain active in the appendix. The long-bridge finite-family design
also remains available; it is not deleted in favor of the two-flight design.

## Build and reproduce

From this directory, with TeX Live and Python 3:

```sh
pdflatex -interaction=nonstopmode -halt-on-error two_collision.tex
pdflatex -interaction=nonstopmode -halt-on-error two_collision.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
python3 tools/verify_v13.py --output verification/v13.normal.json
python3 -O tools/verify_v13.py --output verification/v13.optimized.json
cmp verification/v13.normal.json verification/v13.optimized.json
python3 tools/verify_v14.py --output verification/v14.normal.json
python3 -O tools/verify_v14.py --output verification/v14.optimized.json
cmp verification/v14.normal.json verification/v14.optimized.json
```

The companion is built first to resolve external cross-references. The
latest referee's independent diagnostic is retained at
`../../reviews/a2-v13-independent-harsh-normal-form-2026-09-10/verify_review.py`;
run it with `--output` to an explicitly chosen JSON path, ordinarily and
with `python3 -O`, to reproduce the separate referee benchmark.

`VERIFICATION.json` records the build, three paired suites and artifact
hashes. The v14 suite checks exact rational identities on a stated
synthetic generating-action model, not simulated physical billiards.
Algebraic tests and successful compilation are not formal proof
certification, remote CI or an optimal full-profile sampling theorem.

## Preservation and source identity

All 52 prior active inputs and all 218 reviewed formal statement/proof
blocks remain active; the new totals are 53 inputs and 224 formal blocks.
The retention check uses a frozen hash of the complete sorted block
multiset, together with unchanged-file and archived-file Git hashes.
Replaced front matter and metadata are preserved under
`history/v13-reviewed/`. The native manuscript tree is based on the full
v13 tree and therefore preserves its inactive historical material too.

`SOURCE_PINS.json`, `HISTORICAL_DERIVATION_AUDIT.md`, `PROOF_LEDGER.md` and
`LITERATURE_VERIFICATION.md` give the source chain and proof dependencies.
The old manuscript and review branches are unchanged. No merge,
force-push, branch-protection change or deletion is part of this revision.
