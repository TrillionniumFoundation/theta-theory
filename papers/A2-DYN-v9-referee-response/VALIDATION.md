# Validation record — A2-DYN revision 9

The local native build completed on 5 October 2026 using `bash build.sh`. The complete article is **60 pages**. The final LaTeX log has no unresolved references, warnings, overfull boxes, or underfull boxes. References stabilized under repeated native `pdflatex` runs with shell escape disabled.

## Source and finite checks actually run

`tools/verify_v9.py` passed in both normal Python and `python3 -O`; their JSON outputs are byte-identical. The script verified all 24 unique core inclusions, 234 labels, 77 proof environments, and preservation of 124 inherited mathematical environments. Of the 21 inherited core files, 17 are byte-identical; four have the documented exposition changes. All ten inherited Python scripts are byte-identical to the pinned v8 source. The complementary-projection rename is normalized explicitly during the mathematical-environment comparison.

The new finite suite performed 863 exact checks of deterministic stopped compensation, visit counting, physical-clock cancellation, dyadic decompositions, and the rational scale exponents. The inherited renewal/counting suite performed 13,217 checks. These test finite models and algebra only, not continuum billiard theorems.

The six retained finite diagnostics were also run successfully: `certify_winding.py`, `certify_excursion.py`, `verify.py`, `verify_v2.py`, `check_v5.py`, and `check_v6.py`.

## PDF inspection

Representative pages covering the introduction, compatibility diagram, new covariance and Gaussian arguments, functional proof, and references were rendered for visual inspection. A text-block extent check over all 60 pages found no block outside a five-point page safety inset. This check is not a substitute for reading the mathematical arguments.

## Reproduction and remote evidence

The build produces `evidence/v9-source-and-finite-checks.json`, the optimized-mode counterpart, six retained diagnostic outputs, and `evidence/build-receipt.json`, which hashes the TeX sources and PDF. Local compilation occurred before the remote commit, so its receipt does not claim an exact remote event SHA. The scoped GitHub workflow independently checks and builds `github.sha`, archives the source snapshot, and records the resulting SHA in its receipt. Its run status must be read from GitHub rather than inferred from the local success.

This validation does **not** certify a full raw LLT, covariance nondegeneracy, a complete singular-branch sum, or independent human specialist acceptance. The scope and remaining estimates are stated in `PROOF_LEDGER.md` and `RESPONSE_TO_REFEREE.md`.
