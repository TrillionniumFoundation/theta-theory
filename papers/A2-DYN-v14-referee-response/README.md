# A2-DYN, revision 14

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision responds to the external v13 report at `014dbfa28501551a30388b44c0509fb7fbfbc444`, on the reviewed author source `47d2430dc14c4d98a9e80db6fd573b049be8808c`. The new branch starts from the review commit so that the controlling report and the entire reviewed manuscript remain in its history.

## New mathematical result

Theorem E proves uniform positive definiteness of the full four-dimensional covariance of the same actual return record. Its full proofs are in `core/32_measurable_phase_rigidity.tex` and `core/33_joint_nondegeneracy.tex`.

The exact collision action identity `d tau = T*theta-theta`, with `theta=R p d alpha`, gives a symplectic-area obstruction to nonzero roof frequency for a merely measurable physical phase. Conditional-pair probabilities have bounded marginals, so smooth approximation justifies the stable and unstable holonomy identities without assigning values at selected periodic points. Products over two and three rotations exclude a nonintegral constant collision phase. Finally a hypothetical real spatial coboundary, rotated through sixty degrees, would make both lattice coordinates coboundaries and create a nonconstant invariant function on an ergodic finite physical cover.

Exponentiation removes the integer-valued section indicator before these arguments are used. All joint zero-variance directions are excluded. Continuity of the established covariance on the compact radius interval then gives a uniform positive lower eigenvalue. The earlier scalar count argument is retained and clarified, rather than used as a substitute for this joint proof.

## Preservation and scope

All 31 inherited core modules, all inherited theorem labels, all inherited Python diagnostics, and the bibliography are retained. Twenty-three core files remain byte-identical. Eight receive precisely replayable scope/cross-reference or proof-clarification edits; `INHERITED_EDITS.json` records every replacement. No inherited theorem is deleted, and no paper topic, return section, record or target measure is changed.

The full raw mixed-density theorem still requires its complementary-frequency integral, complete critical/singular branch extraction and residual sum, and weighted exact-event estimates. The new Gaussian tail estimate is not misidentified as a physical-transform tail. Qualitative exclusion of exact phases is not a quantitative resolvent bound.

## Build and review

Run `bash papers/A2-DYN-v14-referee-response/build.sh` from a checkout. The verifier checks all source hashes, replays every inherited edit, retains all old labels, runs the inherited diagnostic chain and new exact/finite physical checks normally and with `-O`, and builds the full article without shell escape. The workflow `.github/workflows/a2-dyn-v14-qualification.yml` archives the exact event source and produces a receipt with its SHA, run ID and PDF hash.

`RESPONSE_TO_REFEREE.md` is the point-by-point response. `GEOMETRIC_INPUT_MAP.md` identifies the qualitative billiard input and its checked hypotheses. `PROOF_LEDGER.md` separates the new proofs, imported theorems and remaining raw-density requirements. Successful execution is not a formal proof certificate or an independent human review.
