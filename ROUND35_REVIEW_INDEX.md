# Round 35 review index

## Immutable input and publication unit

Controlling report: `REFEREE_REPORT_ROUND34_GPT56_PRO_HARSH.md`.
Report commit: `9f5276233b63218a0d89df6611381975dc873232`.
Report Git blob: `9aae7570d710c5804f703c21fab212bc11e21aa1`.
Reviewed Round 33 commit: `7bb555662a572bd400fbfb0d6011a812ad578593`.
Revision branch: `revision/round35-mechanical-identification-2026-09-03`.

The focused new publication unit is `ROUND35_REVISION.tex`, with proofs in
`round35/mechanical.tex`. The C1 canonical paper entry selects the same
material. This is a new mechanical-model theorem for independent review, not
an assertion that every original paper has regained its old unconditional
headline theorem.

## Theorem-level reading order

| Result | Active locator | Premises verified in this manuscript |
|---|---|---|
| Uniform infinite-lattice stability | `lem:r35-energy` | Positive damping/pinning, bounded half-line spring operator; energy identity on the whole Hilbert space |
| Global two-duration identification | `lem:r35-embedding`, `prop:r35-certificate` | Actual step-response coefficients, explicit remainder, whole-rectangle rational certificate |
| Policy-uniform excitation | `lem:r35-excitation` | Four nonoverlapping force-duration atoms; signs cancel existing-state cross terms |
| Infinite initial-state nuisance | `prop:r35-nuisance` | Bounded support, exponentially decaying physical transients, exact chronological likelihood |
| Global posterior localization | `lem:r35-score`, `thm:r35-lan` | Finite-net martingale concentration and a smooth martingale-field bound |
| Parameter posterior/evidence | `thm:r35-bvm` | Actual localization and local quadratic remainder; no assumed information limit |
| Filter jets and state posterior | `thm:r35-filter`, `cor:r35-state` | Dissipation and normalized likelihood derivatives, not Fisher-to-Riccati inference |
| Infinite bath memory | `thm:r35-memory` | Bounded physical block operators and an explicitly solved Jacobi resolvent |
| Finite-preparation amplitudes | `thm:r35-labels` | Derived nuisance evidence limits under one common policy |

The parameter is local **damping and stiffness**, not a sensor offset. The
hidden bath is coupled when epsilon is positive. Initial states are not reset
between diagnostic words. There is no finite-dimensional density assigned to
the infinite state and no replacement of the infinite proof by simulation.

## Active supporting corrections

B1, B3 and C2 canonical `main.tex` entries now select new Round 35 wrappers and
materialized files under `round35/supporting/`. Their repaired Round 33
arguments are retained, with the singleton atom, bounded zero-evidence versions,
Minkowski range, and stochastic measurability specifications corrected in the
actual source. Old `round33/chapters/` files remain archival, not inputs of these
four changed canonical entries. Other canonical paper entries are unchanged.

`round35/errata.tex` gives self-contained corrected statements in the focused
manuscript as well. `round35/HISTORICAL_REUSE.md` records the source identities.

## Reproduction and evidence

Run `python3 tools/verify_round35.py`. The verifier checks the source manifest,
runs the finite tests and exact rational certificate, builds the focused dossier
and four canonical entries in two fresh directories, and checks the source
hashes again. The certificate covers an entire parameter rectangle and the
uncomputed infinite-operator tail; it does not certify all statistical theorems.

`ROUND35_LOCAL_VERIFICATION.json` records the actual local execution. Remote
commit identity is established by GitHub's returned commit/ref and read-back,
not by embedding a future self-referential commit hash in the source manifest.
Remote CI is a separate observation, never inferred from the workflow file.

## Remaining original programme

See `round35/PROOF_LEDGER.json`. The new verified model interfaces are not
substitutes for the original unweighted seam, singular Sinai Fourier theorem,
chronological recovery, extensive hard-sphere path tilt, all-genealogy LDP,
microscopic contact-process theorem, spatial kinetic comparison, singular
pressure rigidity or adaptive thermodynamic phase expansions. None is deleted
from the programme or declared closed because this manuscript compiles.
