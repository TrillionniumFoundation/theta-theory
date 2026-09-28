# General Theta Foundations I — Revision 54

## Referee reading order

1. `paper.pdf` / `main.tex`: **Sharp Noise Thresholds and Width Laws for Stochastic Realizations of Compact Group Experiments**. The main article is independently complete.
2. `RESPONSE_TO_REFEREE.md`: the response to r35, with all nine required-revision items and all thirty local comments.
3. `LITERATURE_AUDIT.md`, `HISTORY_AND_PIPELINE_AUDIT.md`, and `PROOF_STATUS.json`: theorem-level comparisons, precise inheritance, and hypothesis boundaries.
4. `SCALAR_PREDECESSOR.pdf`, `COMPANION_NOTES.pdf`, and `COMPLETE_SUPPLEMENT.pdf`: the full preceding article, companion, and earlier theory, rebuilt from unchanged native sources under `retained-v53/`. They are optional background, not missing steps in the main proof.
5. `evidence/BUILD_RECEIPT.json`, `evidence/SOURCE_HASHES.json`, and `evidence/REFEREE_PACKAGE.zip`: actual source-bound qualification and portable referee material. A scope commit or queued workflow is not a qualified publication.

## Principal advances over v53

The scalar oscillation threshold is replaced by the constrained Chebyshev radius of an entire output image on each connected component. The output may be a single categorical or joint law, or any compact-convex finite-dimensional numerical output. Bounded nonuniform clocked width exists exactly at and above that radius. One stationary component-permutation machine attains it. Below it the occupation of every fixed width is bounded independently of the horizon, including machines with unrestricted intervening registers.

The intrinsic theorem uses compact Hausdorff groups with **finitely many connected components**, not just matrix groups. Executable identity returns of every sufficiently large length replace the identity-letter hypothesis. This is a sufficient synchronization condition, not a purported classification of all compact semigroups or all padding languages.

For an alphabet of s planar rotations satisfying the dual badly approximable condition, optionally with the standard reflection, and signed coordinate interfaces of amplitude **0 < rho < 1**, the minimum command width is **Theta(N^(s/(2s+1))) at every fixed 0 <= epsilon < rho/2**. The upper realization is exact. This extends the historical small-noise matching law to the whole subcritical interval; it does not claim discovery of a new exponent or apply the exact upper construction at rho=1.

For rational orthogonal matrices with an identity letter and rational polynomial categorical readouts, the compact real components, exact algebraic threshold, boundary machine, subcritical occupation constants, and each finite-horizon minimum width are computable. The proof uses established terminating group-closure and real-algebraic algorithms. The repository checks are not an implementation of that general solver.

The finite quotient-minimum theorem characterizes precisely **deterministic component-quotient machines**. It is not an unrestricted stochastic minimum theorem.

## Frozen provenance and preservation

Predecessor publication: `825d1d302cfca6c6b5abe8497bddb4df8680d810`.
Controlling r35: `ea6d8b71653ec4aa6084b4faf63fe7d702505a26`.
Controlling report blob: `a4f024689b9470c0f311fe0b1f744abc14ea54ac`.

Working branch: `revision/general-theta-foundations-i-v54-chebyshev-radius-2026-09-27`.
Referee-ready branch: `revision/general-theta-foundations-i-v54-referee-ready-2026-09-27`, created only after successful qualification and inspection.

The 72-file native v53 source inventory is retained byte-for-byte, including all 59 v52 source files, 33 active inputs, and 242 loaded labels of its complete supplement. Earlier original paths and review branches remain unchanged. No part of the unrelated A/B/C/D analytic dependency graph is declared complete by this finite-dimensional realization result.

## Reproduction

Use Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7, and TeX Live with AMS, Latin Modern, microtype and TikZ. From this directory run:

```sh
python build.py --check-isolated
```

The native source archive rebuilds without GitHub or repository access. The build reruns the new and inherited checks in normal and optimized Python, compiles four PDFs, checks every loaded label and every page, and compares text and raster hashes in an isolated native-source rebuild. The proofs remain mathematical arguments requiring independent review; finite regression counts and successful typesetting do not certify them or establish exhaustive priority.
