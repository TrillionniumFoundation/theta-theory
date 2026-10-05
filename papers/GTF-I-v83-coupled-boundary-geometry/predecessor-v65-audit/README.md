# General Theta Foundations I — Revision 65

## Manuscripts and entry points

**Quantitative:** *Positive Streaming Simulation and Spectral Space Bounds*, `quantitative.tex` -> `paper.pdf`.

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*, `structural.tex` -> `STRUCTURAL_PAPER.pdf`.

**Complete research edition:** `main.tex` -> `COMPLETE_REVISION.pdf`. It retains all prior active mathematical sections and labels. The focused articles have independent proof graphs; this complete edition is archival.

## Principal additional results

Sections 32–33 give an explicit positive fixed-denominator matrix rounding map and a one-pass simulator for any fixed finite Gaussian-rational Kraus description with a fixed rational initial state. For horizon N and accuracy 2^(-L), the simulator uses

    O_input(min(N, L + log(N+1))) writable bits.

The approximation controls the summed trace norm of the full classical–quantum history blocks at every prefix, uniformly over adaptive classical control policies. Consequently it controls transcript total variation and any common terminal measurement. State disturbance, zero-probability outcomes and arbitrarily small nonzero probabilities are allowed. Stored/returned matrices are always legal; branch probabilities are sampled with explicit integer rejection from fair bits. Exact simulation has linear space. One-outcome channels are deterministic.

Section 34 matches the upper space order for legal matrix-output tasks under a full action spectral gap and an all-direction cap law. It supplies explicit rational examples in every fixed dimension. The lower proof is still conditional on those spectral/geometric premises and uses the inherited entropy budget. It permits arbitrary randomization and unlimited time. The usual work-space interpretation is for one fixed program, with program-dependent constants and a sufficiently large horizon, not an uncharged program family changing with N,L.

This does not claim the same lower bound for every noisy channel or for a transcript-only simulator. The process theorem does not extend the finite-response-quotient classification beyond its repeatable nondisturbing-probe hypotheses. The error is not TV of binary encodings of matrices or a uniform posterior error conditional on rare histories.

Section 35 compares the exact versions of Chen–Wu's 2026 strict-cutpoint results. The April paper's August version proves n^2+1 states for n>=2, rather than only a quadratic-order assertion. An elementary attenuation proposition shows why preserving a strict cutpoint does not preserve numerical calibration.

## Executable rational instrument interface

The reference uses only the Python standard library:

    printf '8\n2\nuvdiuvdi\n' | python instrument_streaming.py

The default is `inputs/qutrit-instrument.json`. The optional fixed-input path is supplied with `--spec`. Input gives two decimal parameter lines, then one-pass command characters; output gives each sampled outcome immediately and finally a common-denominator numerical matrix using signed hexadecimal integers.

Examples for dimensions 2, 3 and 4 include rational adjacent-coordinate unitary commands, their inverses, amplitude damping, projective measurements, dephasing and an explicit zero outcome. In the qutrit input, `u,v,w,x` are adjacent unitary generators, uppercase denotes inverses, `i` is identity, `a` is amplitude damping, `m` is projective measurement and `d` is dephasing. The input description is fixed before N,L; this is not a uniform-in-dimension running-time claim. These unitary matrices are not the six LPS Bloch matrices used by the inherited qubit theorem.

`check_instruments.py` exercises positive rounding, exact completeness, actual branch sampling, adaptive history trees, rare and zero outcomes, exact/grid modes, fixed-denominator legality, parser failures, scratch estimates and the real CLI. All mathematical comparisons use exact rational/integer arithmetic. `streaming.py`, `check_streaming.py`, `inherited_check_v63.py`, `accuracy_profile.py` and `qubit_compiler.py` retain their distinct earlier tasks.

The reference executes the stated integer recurrence; Python's allocator and operating-system entropy are not certified as an optimal-space bit machine. The theorem specifies the binary arithmetic and ideal fresh fair-bit interface separately.

## Rebuild and review

Run `python build_revision.py --isolated` with pdflatex, PyMuPDF 1.26.7 and SymPy 1.14.0. It compiles all three documents, verifies prior and new proof labels, runs ordinary/optimized exact regressions, and reconstructs from a native-only source archive in an empty directory. Actual counts, pages, source identity and diagnostics are recorded in `evidence/BUILD_RECEIPT.json`.

`evidence/JOURNAL_PACKAGE.zip` contains the two focused PDFs and only their active source dependency graphs, the response and a verifier. `evidence/RESEARCH_PACKAGE.zip` also contains the complete edition, code, fixed inputs and audits. Published package hashes and the final read-only run are separate from mathematical and priority assessment.

The response maps all 14 required r41 items and all 24 detailed comments. `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, `HISTORY_AND_PIPELINE_AUDIT.md` and `PROOF_STATUS.json` distinguish new proofs, inherited results, classical inputs and open external assessment. No submission target is changed, no independent expert opinion or author signature is fabricated, and no independent analytic-pipeline flag is changed.

## Exact ancestry and branches

Base v64 final head: `abd5600b0085463ff78a1525d9588f42c8a514d5`.
Controlling r41 report: `bee28d9c8af25880c548b4650f2fdc7eacbdf8af`.
Companion r41 audit: `7284bc1e406665a8f89edf2741abdd5e71e8555d`.

All 71 v64 native files remain at their original Git paths. All 321 prior complete-edition labels and all prior focused proof labels are preserved. The new revision does not recursively duplicate historical packages or depend on their PDFs for a proof.

Work branch: `revision/general-theta-foundations-i-v65-positive-instrument-streaming-2026-09-29`.

Referee branch, created after qualification: `revision/general-theta-foundations-i-v65-referee-ready-2026-09-29`.
