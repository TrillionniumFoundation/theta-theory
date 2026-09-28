# Proof and information ledger — A2 v15

| Claim | Direct proof | Dependencies and scope |
|---|---|---|
| Exact probability and signed-moment integrals | Lemma 2.1, `core/02_local_law.tex` | Stationary two-flight action; canonical section measure; actual initial residual time; fixed first-hit patches; no conditional sampling |
| Smooth extension to zero | End of Lemma 2.1 | Fixed Morse disk and parity of the integrated scaling parameter; does not assume even contacts |
| Even all-degree block with arbitrary lower odd jets | Proposition 3.1, §§3.1–3.3 | Exact homogeneous action and twist variations; weights after fixed-domain reduction; opposite-contact twist included |
| New odd block and strict separation | Proposition 3.1, §§3.2–3.3 | Mark u+v; ellipse cross-moment identity; determinant lower bound for every m>=1 and positive z |
| All-degree finite-jet inverse | §3.4, equation (3.15) | Successive nonsingular two-by-two solves; fixed order; coefficients depend only on displayed finite jets |
| Analytic participating-boundary determination | End of §3.4 | Equality of all recovered jets; real analyticity and continuation of connected embedded analytic boundaries; not a smooth or whole-table inverse |
| Independent asymmetric physical image | Proposition 4.1 | Explicit support functions; same global transverse sign at both contacts; positivity, clearance, triangular all-degree Jacobian and free-area derivative |
| Finite positive-window coordinates | Proposition 4.2 | Supplied physical family; fixed labelled leading geometry; block interpolation with controlled parameter derivative remainders; unknown area enters as a shared intercept |
| Binary confidence and risk bounds | Theorem 4.3 | Only the explicitly compressed finite channel experiment; seed and original mark not returned; independent preparations, charged failures; physical local alternatives |
| Analytic physical forward comparison | Proposition 5.1 | Supplied canonical normalizing charts; relative estimate before differentiating; fixed physical inverse box and explicit same-section conventions |
| Smooth relative law and whole symmetrized profiles | `complete/main.tex` and its retained inputs | Full historical smooth determinant, first-hit, Volterra, Abel and acquisition proofs retained; no growing-order or optimal full-profile minimax upgrade asserted |

The numbering above is a reading aid; source labels are authoritative if pagination or numbering changes. The new inverse is triangular in the order eta_1, xi_1, eta_2, xi_2, and so on. A reflection argument explicitly prevents confusing the signed and count-only information sets. Fixed-order Lipschitz constants may deteriorate with the jet order.

## What the computations check

`tools/verify_blocks.py` independently constructs homogeneous action polynomials, differentiates their mixed twist, integrates polynomial monomials by Gaussian pairings and radial factors, and compares the resulting coefficients with the displayed blocks. Exact rational grids include equal curvatures and small positive hyperbolicity parameters. The script also checks determinant signs, nodal designs and deliberately singular repeated-node controls. Its 2,747 checks do not import the manuscript's integration formula as their integration implementation.

`tools/verify_sources.py` reconstructs the frozen native Git tree, compares every inherited file, checks the actual TeX dependency closure and the exact historical input sequence, and produces a mathematical-source manifest. Only the declared companion paragraphs and front matter can differ. This is a preservation check, not a theorem prover.

`tools/run_validation.py` executes the checks twice (normal and optimized Python), forces all three full builds, audits their final logs and verifies that the mathematical sources did not change during validation. None of the tools edits source to obtain a pass. There is no formal proof certificate or claimed independent human reproof of every inherited result.
