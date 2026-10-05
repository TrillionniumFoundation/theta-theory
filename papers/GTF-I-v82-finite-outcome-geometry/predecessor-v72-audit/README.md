# General Theta Foundations I — Revision 72

## Manuscripts

Quantitative: **Observable Readout Geometry and Reusable Instrument Descriptions**, `quantitative.tex` → `paper.pdf`.

Structural companion: **Finite Physical Actions and a Strong Converse for Repeatable Observations**, `structural.tex` → `STRUCTURAL_PAPER.pdf`.

Complete research edition: `main.tex` → `COMPLETE_REVISION.pdf`. It retains every one of the 460 previously active mathematical labels, the earlier proofs, and the new sections. Previous repository paths are not overwritten.

## Main additions

For a varying ordered rank-one readout on C^d with **observable readout label** and rank-bounded conditional preparations, put

    b = d^2-d,
    V = sum_x (sum_y r_xy (2n-r_xy)-1).

Theorem `thm:readoutentropy72` proves the reusable-description law

    (b+V/2) log2 N + (b+V) log2(1/delta) + O(1),

uniformly for N>=1 and 0<delta<=1/32, at fixed public dimensions and ranks. The lower bound permits arbitrary legal memoryless instrument centres. The upper code gives legal rational centres, preserving conditional zero blocks and never increasing their ranks. The readout coordinate is the ordered flag U(d)/T^d: column phases are removed, label permutations are charged. A corollary recovers the label from fixed orthogonal output supports. Arbitrary unlabelled overlapping rows are not assigned this exponent; equal rows erase the basis exactly.

A new **direct triangular flag codec** uses partial-pivot LU of unnormalized rational projector columns. It neither constructs algebraic normalized eigenvectors nor searches an exhaustive unitary net. Every valid chart word decodes to a legal rational flag. The proof supplies an explicit projector perturbation bound and fixed-dimensional numerator/denominator bit bounds.

Theorem `thm:seizablecover72` proves exact equality of family covering numbers under a common processor with a common one-use left inverse on the **entire ambient programme state space**. This includes arbitrary legal memoryless centres, not only two specified hypotheses. It transfers the inherited full submaximal-error rank-state law, and a Pauli/Bell corollary supplies an exact rational example. Retraction of an arbitrary centre can increase Choi rank; programme rank/zero preservation belongs to the upper encoder.

The multiple-query projective measurement theorem and common-environment/seizing principles are imported and cited. The new claims are the explicit family coverings, direct rational flag construction and centre-class consequences, not the invention of those discrimination principles.

## Exact executable interface

The supplied target comprises ordered rational projection matrices and one normalized rational instrument-state row per projection. Both qubit and qutrit inputs are included. For example:

    python readout_codec.py encode --input inputs/varying-readout-qubit.json --horizon 12 --error 1/100 --ranks '[[1,0],[0,1]]' > code.json
    python readout_codec.py decode --input code.json > instrument.json
    python readout_codec.py verify --input inputs/varying-readout-qubit.json --certificate code.json

The decoded Choi convention is input-first and unnormalized; its blocks are transpose(P_x) tensor sigma_xy. The main CLI retains the readout label. The orthogonal-output and Pauli/Bell maps are additionally exposed as exact library functions and exercised in the regression suite. JSON is a transport envelope, not the fixed-length payload. Header, body, rank, legality and canonical target replay are validated separately. Bare decoding does not identify an unknown target.

Run `python check_readout.py`. Its actual count and negative controls are recorded in `evidence/REGRESSION_RESULTS.json`; normal and optimized runs must agree. All eight earlier suites are also executed unchanged. Finite tests do not prove all adaptive testers, continuum packing, the imported measurement theorem or independent priority.

## Reproduction

Run `python build_revision.py --isolated` with Python, PyMuPDF, SymPy and pdflatex/AMS packages. The builder checks predecessor proof labels, runs the exact suites, compiles all three PDFs, and reconstructs the complete native source archive in an empty directory. Unresolved references, citations and overfull/underfull boxes fail the build. `evidence/BUILD_RECEIPT.json` records the actual outcome and exact source identity.

`evidence/JOURNAL_PACKAGE.zip` contains the two focused manuscripts and only their active TeX proof graph, response, hashes and verifier. `evidence/RESEARCH_PACKAGE.zip` adds the complete edition and exact tools. Neither focused article depends on historical PDFs. The final-head workflow checks the exact final commit with contents-read permission only and uploads its attestation outside the reviewed tree.

## Source ancestry and response

Base: completed v71 final head `8c053f4820da3abcbb04daab628aa94379fd01e3`.
Controlling v71/r46 report: `b78c1dddd41de645edf207bc415406b3fc1b5e83`.
Companion proof/pipeline audit: `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.

The pre-existing v72 work anchor was `3caaf5abf52b3b067075d7085f56a28e5b666435`; continuation was pushed at `f9d7d15469a46841c3783565eb21c705ccb2cb4b` before substantive publication. Its incomplete local transfer was consulted, not treated as a verified source release. This completed construction uses direct projector/LU coordinates in place of its proposed exhaustive flag search.

Work branch: `revision/general-theta-foundations-i-v72-varying-readout-2026-10-03`.
Referee branch after final qualification: `revision/general-theta-foundations-i-v72-referee-ready-2026-10-03`.

`RESPONSE_TO_REFEREE.md` maps all sixteen required revisions and twenty-six detailed comments. v70 and v71 theorems retain their separate attribution and error ranges. No change of journal objective or deletion of older mathematical content is used as a response. Independent priority and acceptance are not certified. Every aggregate A/B/C/D analytic completion flag remains false; the detailed obligations remain in the frozen history and ledger.
