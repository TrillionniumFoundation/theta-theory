# General Theta Foundations I — Revision 53

## Referee reading order

1. `paper.pdf` / `main.tex`: the independently complete main article, **Sharp Noise Thresholds for Stochastic Realizations of Compact Group Experiments**.
2. `RESPONSE_TO_REFEREE.md`: responses to the major r34 requests and all thirty local comments.
3. `COMPANION_NOTES.pdf` / `supplement-notes.tex`: local proof refinements, support-cone geometry, and intrinsic reachable-basis conditioning.
4. `COMPLETE_SUPPLEMENT.pdf` / `retained-v52/main.tex`: the complete preceding mathematical theory, not a selected excerpt.
5. `evidence/BUILD_RECEIPT.json`, `evidence/SOURCE_HASHES.json`, and `evidence/REFEREE_PACKAGE.zip`: actual qualification, source identity, and the portable referee package.

## Central result

For finite continuous binary-mean interfaces on a compact matrix-group closure H with an executable identity command, the critical total-variation error is

`epsilon_c = (1/4) max_{seed,query,component} (maximum mean - minimum mean)`.

Uniformly bounded horizon-specific clocked stochastic width exists **if and only if epsilon >= epsilon_c**, including equality. A single stationary permutation machine attains the boundary. Below it every fixed width has a horizon-independent occupation budget. No spanning, reachability-rank, positive-mass, or conditioning assumption is imposed.

Consequences include the intrinsic observable-quotient exact criterion, the sharp planar threshold rho/2, continuous nonlinear and measure-once unitary readouts, compact similarity, and explicit algebraic-circle width bounds for the whole interval epsilon<rho/2. The rational example rho=1/10, epsilon=1/25 has r=5, Delta=1/150, and A=23364.

## Frozen sources and preservation

Parent publication: `7641901c2ef957542aa50d9918f272ac7a72ca1c` (v52).  
Controlling r34: `4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c`.  
Working branch: `revision/general-theta-foundations-i-v53-component-oscillation-2026-09-27`.  
Publication branch: `revision/general-theta-foundations-i-v53-referee-ready-2026-09-27` (created only after actual qualification).

The complete 59-file validated predecessor source inventory is retained byte-for-byte under `retained-v52/`. Its 33 active LaTeX inputs and all 242 loaded labels are rebuilt. The original v52 paths and all previous revision/review branches remain unchanged. Historical introductions and secondary estimates remain in the complete supplement rather than being silently removed from the deliverable.

## Reproduce

With Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7, and TeX Live with AMS, Latin Modern, microtype, and TikZ installed, run `python build.py --check-isolated` from this directory. The portable native source archive requires no GitHub access to rebuild. `prepare_sources.py` is only the repository-side materializer for frozen predecessor and report bytes; it is not needed in the already materialized archive.

The proof is written in the manuscript. Exact finite tests and PDF reproducibility do not replace independent mathematical review. The detailed resource and analytic-dependency boundaries are in the article, response, and audit; neither practical six-state noise-search execution nor a general SOS discovery engine is claimed.
