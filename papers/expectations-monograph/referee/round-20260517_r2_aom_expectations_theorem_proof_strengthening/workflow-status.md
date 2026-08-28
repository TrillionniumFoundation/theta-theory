# Referee Workflow Status - R2 Theorem/Proof Strengthening

- Round: round-20260517_r2_aom_expectations_theorem_proof_strengthening
- Updated: 2026-05-17 Asia/Shanghai
- Edited artifact: main.tex
- External upload performed: no

## R2 Scope

This round keeps the manuscript's first-principles deterministic thesis intact and integrates the repair into the body of the paper rather than adding a referee-response appendix.

The main changes strengthen the following load-bearing points:

- finite-response port is a microscopic action/read-out mechanism, not an oracle for effective coefficients;
- exact prelimit jet graph is constructed branchwise before any homogenized HJB object is introduced;
- moving-singularity response derivatives entering the cell equations are expressed as deterministic resolvent words plus weak trace functionals;
- the main homogenization theorem now cites the strengthened forward-order chain;
- the critical closure proof now routes through the new port, prelimit-jet, and response-to-cell identities;
- layout noise introduced by the new formulas was reduced.

## Local Gate

- Command: latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
- Result: passed
- PDF: main.pdf
- Pages: 245
- Page size: letter
- SHA256: 60140341ce1f98c3a36642f6a4090cd259eda628211a9aa91d23afbd5d4b5712
- Undefined references/citations: 0 / 0
- Overfull hboxes/vboxes: 3 / 0
- Underfull hboxes/vboxes: 8 / 9
- LaTeX/package/pdfTeX warnings: 1 / 1 / 0

## Deterministic Proof Boundary Check

Part I contains no occurrences of martingale, CLT, central limit, martingale approximation, response addendum, or referee-response.

