# General Theta Foundations I — Revision 67

**Quantitative:** *Intrinsic Instrument Entropy, Adaptive Precision, and Positive Streaming* (`quantitative.tex`, `paper.pdf`).

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* (`structural.tex`, `STRUCTURAL_PAPER.pdf`).

**Complete research edition:** `main.tex`, `COMPLETE_REVISION.pdf`. All 368 previously active complete-edition labels are retained. All 100 predecessor native files remain immutable in the base repository tree; the new source contains their active proofs and the new sections, rather than substituting summaries for proofs.

## New mathematical conclusions

For m-outcome completely positive, jointly trace-preserving instruments M_d -> M_n, the intrinsic affine dimension is

    s = d^2 (m n^2 - 1).

At fixed dimensions, the minimum fixed-length legal-description code at diamond error eta has length

    s log_2(1/eta) + O_(d,n,m)(1).

An exact rational coordinate codec achieves this coefficient, retaining exactly s independent real digits and solving the d^2 marginal coordinates algebraically. It validates CP/TP exactly and uses no floating-point decision or Kraus factorization. See Section 38, Theorems `thm:entropy67` and `thm:intrinsiccodec67`.

For a fixed Choi eigenvalue margin 0<a<1/(mn), fixed unhalved joint-state error 0<delta<1, and arbitrary common causal quantum testers with at most N calls to the **same memoryless instrument**, the minimum reusable description length is

    (s/2) log_2 N + O_(d,n,m,a,delta)(1).

The decoded object is reused at every call; testers may have entangled references, quantum memory, feedback and bounded public stopping. The proof uses a two-point classical-programme representation and repeated Choi tests. The programme principle is credited to Demkowicz-Dobrzanski, Kolodynski and Guta; volumetric coding and binary concentration are elementary ingredients, not claimed new. Theorem `thm:adaptiveentropy67` gives explicit finite upper/lower bounds. A unitary boundary example shows why a uniform square-root continuity bound needs a strict margin.

These are description-length results. They neither prove a general mutable streaming-workspace lower bound nor supply a physical classical simulator accepting an unknown entangled input. No spectral gap is used in the new description theorems. The inherited fixed-program streaming lower bounds still require their expanding subsystem, full action gap/cap hypotheses and legal numerical matrix output. Variable-description trajectory simulation remains a separately charged upper theorem, with validation space distinct from post-validation streaming space.

## Exact code

    python instrument_codec.py encode --input inputs/rectangular-choi.json --grid 4096 > code.json
    python instrument_codec.py decode --input code.json
    python instrument_codec.py verify --input inputs/rectangular-choi.json --certificate code.json
    python instrument_codec.py adaptive --input inputs/interior-codec.json --horizon 100 --margin 1/8 --error 1/4
    python check_codec.py

The hexadecimal payload is an encoding of one mixed-radix integer, not a claim that the JSON file size equals the optimal payload length. Headers and the full decoded matrix cost extra. Strict decoding rejects illegal Choi words; a mathematical total decoder may send them to the canonical instrument. A valid decoded matrix alone does not verify closeness to an unspecified target. `verify` recomputes the target-bound encoder result. `CODEC_SCHEMA.md` specifies coordinates, error conditions and resources.

## Reproduction

    python build_revision.py --isolated
    python build_revision.py --verify-published

Requirements: Python, PyMuPDF, SymPy, pdflatex, AMS and Latin Modern packages. The build runs all new and inherited exact suites in normal/optimized modes, typesets three manuscripts, checks all previous labels, reconstructs an empty-directory native archive and compares every PDF page's text and raster. The minimal journal package rebuilds independently without historical PDFs or executable test modules. Actual receipts are generated under `evidence/`; this README is not a build receipt.

## Sources and publication

Base v66 exact head: `58490231d19fd5c5e557e353593251f1202105fa`. Controlling v66/r43 report: `0a3d74582eeeda315237ee73fdd2ac0021862184`; audit: `6c2aee0e242668ff960f3bf4835c87923b8e730f`. Work branch `revision/general-theta-foundations-i-v67-intrinsic-instrument-entropy-2026-10-03` was anchored remotely before substantive editing. Referee branch `revision/general-theta-foundations-i-v67-referee-ready-2026-10-03` is created only after completed publication and exact-head verification.

Read `RESPONSE_TO_REFEREE.md` for all 15 required and 24 detailed r43 items. The general-journal research objective is unchanged. The literature audit now includes Naik–Zartab–Gisin–Banik and 2026 channel-learning comparisons, with the operational differences stated explicitly. It is author-side, not an independently commissioned priority review. Cryptographic authorship, formal proof-assistant verification, journal acceptance and A/B/C/D analytic closure are not asserted by this package.
