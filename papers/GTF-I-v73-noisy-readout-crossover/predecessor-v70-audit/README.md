# General Theta Foundations I — Revision 70

## Current manuscripts

**Quantitative:** Coherent and Preparation Directions in Rational Instrument Coding (`quantitative.tex`, `paper.pdf`).

**Structural:** Finite Physical Actions and a Strong Converse for Repeatable Observations (`structural.tex`, `STRUCTURAL_PAPER.pdf`).

**Complete research edition:** `main.tex`, `COMPLETE_REVISION.pdf`, retaining every v68 active mathematical label.

## Main addition

For F_(U,sigma),y(X)=U X U* tensor sigma_y, fixed d,n,m and rank bounds, set u=d^2-1 and v=sum r_y(2n-r_y)-1. Against common adaptive quantum testers with references, feedback and stopping at N, the optimal reusable description length in unhalved trace distance is

    (u+v/2) log2 N + (u+v) log2(1/delta) + O(1),
    N>=1, 0<delta<=1/32.

This boundary family is not input erasing: it transmits the data system unitarily and appends a possibly singular, support-changing preparation. Its outcome probabilities are nevertheless input independent. The theorem is not a classification of all disturbing instruments, a learning theorem or a physical classical simulation. The lower bound allows all legal memoryless centres; the rational upper centres preserve target zero outcomes and never increase a preparation block rank. Encoder workspace and expanded matrices are separate from the compressed payload.

Section 42 also proves an exact preparation-centre retraction at every positive radius. It may increase centre rank and does not prove a full-error extension of the joint coding law.

## Executable example

    python coherent_codec.py encode --input inputs/preparation-boundary.json --quaternion '["1/2","1/2","1/2","1/2"]' --horizon 100 --error 1/1000 --ranks '[2,1,0]' > code.json
    python coherent_codec.py decode --input code.json > instrument.json
    python coherent_codec.py verify --input inputs/preparation-boundary.json --quaternion '["1/2","1/2","1/2","1/2"]' --certificate code.json
    python coherent_codec.py retract --input instrument.json

The general-d rational Givens decoder and finite exhaustive encoder are library functions in the same module. The optional search cap reports an inconclusive search, never a mathematical obstruction. The qubit CLI is direct, not an exhaustive search.

## Reproduction

    python check_coherent.py
    python build_revision.py --isolated

Python, PyMuPDF, SymPy and a standard AMS/Latin Modern LaTeX installation are required. The build executes seven test suites in ordinary and optimized modes, checks preserved labels, compiles three manuscripts, and repeats the native reconstruction in an empty directory. `evidence/JOURNAL_PACKAGE.zip` has only the two focused proof graphs, PDFs, response and verifier. `evidence/RESEARCH_PACKAGE.zip` also contains the full article and executable sources.

Actual page counts and test results are authoritative in the build receipt, not inferred from this README. Exact-head verification is read-only and its attestation is external to the tree it verifies.

## Ancestry and review

Controlling v68/r45 report `e862e5c963ef36b9caa3b1b814b495ae4428a088`; audit `a3fd5b80549a855c46151fd7183b3fc7139abac7`; completed v68 base `d9d8c464282157485813041d181e909e648b1f4f`. The v69 anchor supplies no proof premise. No predecessor branch, file or theorem is replaced.

Work: `revision/general-theta-foundations-i-v70-coherent-boundary-coding-2026-10-03`.
Referee alias after exact-head verification: `revision/general-theta-foundations-i-v70-referee-ready-2026-10-03`.

The 14 required and 24 detailed r45 comments are addressed in `RESPONSE_TO_REFEREE.md`. Primary CMW/unitary-discrimination antecedents are credited. No independent priority clearance, author signature, acceptance, formal proof-assistant verification or A/B/C/D aggregate closure is asserted.
