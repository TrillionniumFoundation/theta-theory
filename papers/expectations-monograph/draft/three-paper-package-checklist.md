# Three-Paper Package Checklist

- Last checked: 2026-07-09 16:10 CST
- Scope: consolidated package status for the extracted three-paper stack.
- Source ledger: `main.tex` at the repository root remains the long master
  manuscript and should not be submitted as one of the split papers.
- Split plan: `draft/three-paper-split-plan.md`
- Coverage audit: `draft/three-paper-content-coverage-audit.md`

## Package Inventory

| Paper | Role | Submission-facing PDFs | Pages | Latest clean check |
| --- | --- | --- | ---: | --- |
| Paper 1 response theory | singular billiard response package | `papers/response-theory/response-theory.pdf` | 72 | 2026-07-09 16:10 Asia/Shanghai |
| Paper 2 theta-expectation/HJB | deterministic HJB limit and theta-expectation semigroup | `papers/theta-expectation-hjb/theta-expectation-hjb.pdf` | 27 | 2026-07-09 16:31 Asia/Shanghai |
| Paper 3 representation calculus | downstream payoff-calibrated diffusion, BSDE, and Girsanov calculus | `papers/representation-calculus/representation-calculus.pdf` | 6 | 2026-07-09 07:39 CST |

## PDF Hashes

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `papers/response-theory/response-theory.pdf` | 808131 | `3e752cdde251c70296c9658c268fc16895c79e8b0de648dcc52ee0a911c8f88d` |
| `papers/theta-expectation-hjb/theta-expectation-hjb.pdf` | 482590 | `c8c55404f9464029fd8f3f7454f4756d0daa465fe381b0187bffa1944a8c9cf7` |
| `papers/representation-calculus/representation-calculus.pdf` | 286530 | `4cfa46f73edfce134c037b0e2963ca091d55a1ed89961638b4b9ddc03be6ade5` |

## Source Upload Sets

### Paper 1

Default PDF-only upload:

- `papers/response-theory/response-theory.pdf`

If source upload is required:

- `papers/response-theory/main.tex`
- `papers/response-theory/proof-ledger-appendix.tex`
- `papers/response-theory/main.bbl`
- common LaTeX dependencies only if the venue system lacks them.

### Paper 2

Default PDF-only upload:

- `papers/theta-expectation-hjb/theta-expectation-hjb.pdf`

If source upload is required:

- `papers/theta-expectation-hjb/main.tex`
- `papers/theta-expectation-hjb/technical-appendix.tex`
- `papers/theta-expectation-hjb/main.bbl`
- `reference.bib` only if the venue explicitly asks for BibTeX source.

### Paper 3

Default PDF-only upload:

- `papers/representation-calculus/representation-calculus.pdf`

If source upload is required:

- `papers/representation-calculus/main.tex`
- `papers/representation-calculus/main.bbl`
- `reference.bib` only if the venue explicitly asks for BibTeX source.

## Current QA Gates

All three extracted papers have current standalone build evidence in their own
`compile-status.md` files.

- Paper 1: `main.tex` now inputs `proof-ledger-appendix.tex`, so the former
  proof-ledger material is integrated into one manuscript PDF.  Three
  successful `pdflatex -interaction=nonstopmode -halt-on-error main.tex` runs
  after the merge produced stable cross-references and a 72-page
  `response-theory.pdf`.
  Final logs
  had no fatal errors, undefined references, undefined control sequences,
  emergency stops, rerun warnings, or overfull boxes.
- Paper 2: `main.tex` now inputs `technical-appendix.tex`, so the former
  technical proof details are integrated into one manuscript PDF.  Three
  successful `pdflatex -interaction=nonstopmode -halt-on-error main.tex` runs
  after the merge produced stable cross-references and a 27-page
  `theta-expectation-hjb.pdf`.  Final scans found no fatal errors, LaTeX
  errors, undefined citations, undefined references, undefined control
  sequences, overfull boxes, or rerun warnings.  Remaining warnings are
  underfull boxes.
- Paper 3: `main.bbl` was unchanged from the previous clean BibTeX build;
  `main.tex` passed two `pdflatex -interaction=nonstopmode -halt-on-error`
  runs after the sign/application pass.  Final scans found no fatal errors,
  LaTeX errors, undefined citations, undefined references, undefined control
  sequences, overfull boxes, BibTeX warnings, or rerun warnings.
- Source scans over the submission-facing TeX files are clean for workspace
  paths, local process markers, master-source line tags, `\src{...}`,
  `Proof roadmap`, `TODO`, `FIXME`, and extraction markers.

## Submission Posture

The split is dependency-clean:

1. Paper 1 exports the singular-billiard response package.
2. Paper 2 imports Paper 1 and derives the nonconvex HJB/theta-expectation
   semigroup.
3. Paper 3 imports Paper 2 and gives payoff-calibrated representation
   calculus.

Keep the boundaries strict:

- Do not add HJB proofs or BSDE/Girsanov material to Paper 1.
- Do not add singular-billiard proof details or representation calculus to
  Paper 2 except through named companion-paper interfaces.
- Do not let Paper 3 read as a primitive probabilistic derivation of the HJB
  theorem; its laws, BSDEs, and Girsanov shifts are downstream and
  payoff-calibrated.

## Honest Readiness Assessment

| Paper | Clean package? | Main remaining risk |
| --- | --- | --- |
| Paper 1 | Yes, as a single integrated PDF | 72 pages, so a hard 70-page venue needs a small trim; remaining risk is proof-depth completeness and venue posture |
| Paper 2 | Yes, as a single integrated PDF | still short relative to a 50-75 page flagship HJB proof paper; remaining risk is venue-specific proof depth or numerical/orbit illustration if requested |
| Paper 3 | Yes, as a current short article package | coherent as a short downstream note, but a stochastic-analysis venue may ask for expanded well-posedness assumptions or a richer application |

## Target-Venue Routing

- Paper 1: dynamical systems, ergodic theory, mathematical physics, or
  hyperbolic billiards venues.  Current Paper 1 posture is a single integrated
  PDF; a hard 70-page cap requires the safe trim queue recorded in
  `papers/response-theory/proof-depth-venue-audit.md`.
- Paper 2: probability/PDE/control venues that accept deterministic
  homogenization and viscosity-solution arguments; cite Paper 1 as a companion
  response theorem.
- Paper 3: probability/stochastic-analysis, control/PDE, or finance-facing
  venues after choosing whether to expand well-posedness details or the
  robust-pricing stress illustration.

## Next Package Actions

1. Decide whether the immediate target is a clean internal split package or an
   externally submitted paper.
2. If external submission starts with Paper 1, confirm whether 72 pages is
   acceptable for the target venue before adding more proof detail.
3. If Paper 1 must fit a hard 70-page cap, trim 2--4 pages from
   crosswalk/dependency prose before rebuilding.
4. If external submission starts with Paper 2, decide whether to add
   venue-specific proof polish or a true orbit/parameter numerical experiment.
5. If external submission starts with Paper 3, choose probability/control/finance
   framing and expand only the relevant introduction or example.
6. Once a target path is chosen, freeze companion-paper titles and citation
   language across all three papers.
