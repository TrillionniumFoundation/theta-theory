# General Theta Foundations I — Revision 74

**Quantitative:** *Coupled Boundary Geometry and Reusable Measurement Descriptions* (`quantitative.tex`, `paper.pdf`).

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* (`structural.tex`, `STRUCTURAL_PAPER.pdf`).

**Complete research edition:** `main.tex`, `COMPLETE_REVISION.pdf`. Every v73 complete-edition mathematical label remains typeset; the structural companion is inherited, not credited as new work.

## New mathematics

Section `50-coupled-boundary-geometry.tex` treats the entire unbiased binary-qubit measurement ball, E_x^±=(I±x·sigma)/2. For s=min(|x|,|y|), define D=sqrt(N/(1-s²+1/N)) |x-y|. At every N>=1, including unequal visibilities and both boundaries,

    (1/256) min(1,D) <= d_N(M_x,M_y) <= min(2,6D).

The metric is the unhalved final-state trace norm maximized over all common reference-assisted adaptive testers with feedback and bounded stopping. The one-use distance is exactly |x-y|.

A compact k-Ahlfors-regular identifiable subset X has, uniformly at sufficiently small error,

    covering number ~ delta^(-k) integral_X [N/(1-|x|²+1/N)]^(k/2) dmu.

The lower cover permits arbitrary legal memoryless centres; the upper centres belong to X. A depth distribution mu{1-|x|²<=t}~t^alpha gives N^(k/2), N^(k/2)log(N+2), or N^(k-alpha), according as alpha is greater than, equal to, or less than k/2. Positive mass on the projective boundary gives N^k.

The joint measurement disk therefore has cover order N log(N+2) / delta²; the full ball has order N²/delta³. Unlike v73, visibility is encoded, not supplied as a free parameter. These are not claims for arbitrary biased POVMs or general disturbing instruments.

## Exact code

`coupled_codec.py` takes a rational Cartesian Bloch vector. Its norm may be irrational. Rational stereographic layers and exact sign-before-square comparisons produce one fixed-length index charging both visibility and direction. Every index decodes to a legal rational instrument. The payload is index capacity; JSON, public N/delta/dimension, encoder workspace and expanded matrices are separate resources.

    python coupled_codec.py encode --input inputs/coupled-ball-3.json --horizon 7 --error 1/128
    python check_coupled_geometry.py

All calculations deciding grids, charts, digits and legality are exact. The algorithm enumerates radial layers only; it is not claimed polynomial in encoded horizon/accuracy or optimal in mutable workspace. It receives a description and neither learns an unknown device nor physically simulates unknown quantum inputs using finite classical hardware.

## Reproduction

    python build_revision.py --isolated

Dependencies: Python, SymPy, PyMuPDF, pdflatex, AMS and Latin Modern packages. The build runs all eleven exact regression suites in normal and optimized modes, typesets three manuscripts, checks every prior proof label, and independently rebuilds the native ZIP. It rejects unresolved references/citations and overfull/underfull boxes. `evidence/BUILD_RECEIPT.json` records actual results, not predictions from this README.

`evidence/JOURNAL_PACKAGE.zip` contains both independently complete focused proof graphs, PDFs, response, manifest and a journal verifier. `evidence/RESEARCH_PACKAGE.zip` additionally preserves the combined edition and tools. Historical source files remain at their existing repository paths; the current package does not require historical PDFs to compile.

## Controlling reports and branches

The controlling reports are v73/r47: external `fa857238020a0b5f2befd936b39820a9b426390a`, proof/pipeline audit `62ffc56f0911b939f3e6b79ae0a5e38563e5a988`. The base is the completed v73 final head `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`. The already-created v74 anchor is continued, not replaced by a parallel revision.

Work: `revision/general-theta-foundations-i-v74-coupled-boundary-geometry-2026-10-04`.

Referee alias after exact-head verification: `revision/general-theta-foundations-i-v74-referee-ready-2026-10-04`.

The response maps all 17 required and 30 detailed comments. Direct comparisons with Sedlak–Ziman (2014) and Puchala et al. (2018) are added. Independent human priority review and cryptographic author signing are not supplied or claimed. The journal target is unchanged. All separate A/B/C/D analytic completion flags remain false.
