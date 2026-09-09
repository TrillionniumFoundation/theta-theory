# Response to the independent A2 v5 referee report

Author: Qian Qi. Date: 9 September 2026.

## Source basis and status

The controlling report is `reviews/a2-v5-statistical-contact-rigidity-harsh-independent-2026-09-09/REFEREE_REPORT.md` at commit `9975aa037d5d9eb1f339b9220f9cd21fb54c0876`. Its reviewed manuscript is `papers/A2-v5-statistical-contact-rigidity/` at `1e57d9c024f90f0304e5572c0e320707bab88074`. The parallel variable-chain derivation is `papers/A2-v5-boundary-factorization/v5/10_twist_chains.tex` at `ee879236d0fae1f84c685bef4ff27326403d4b2d`. The corresponding parallel report tip is `0e7270aadc41019109f72565b557ddcd79ce132f`. Earlier derivations and reports are retained by branching from the controlling review; no deletion or modification of an earlier manuscript is requested.

The present mathematical sections are in `v6_revision.tex`. They contain the proposed additions and detailed proofs. They are not a substitute for an assembled and compiled complete revision. In this execution the tool did not return usable write, branch-tip, or build receipts. Accordingly this response does not claim a verified commit, successful compilation, a rendered PDF, a clean cross-reference audit, successful automated diagnostics, or completion of the requested repository delivery. Inherited equation labels in the new section source still require reconciliation against the full native source before compilation. Neither this response nor the independent report is a journal editorial decision or a formal correctness certificate.

## SCR-R1 — State what the observations identify

We retain the general forward threshold theorem for unequal facing curvatures. In that setting a scalar channel amplitude identifies the effective number `c=sqrt((1+g*kappa_0)(1+g*kappa_1))`, not its two curvature factors separately. The actual unordered curvature-triple theorem applies to the equal-facing physical support family. The eventual revised abstract and headline theorem must state this assumption immediately, rather than leave it to a later model definition. This is a correction of the observation statement, not a reduction of the forward theorem. The realized fixed-gap and fixed-area fibers, endpoint tomography, and the distinction between labelled and unlabelled observations are retained.

## SCR-R2 — Exact germs, finite jets, and coefficient sensitivity

The all-order triangular contact inverse, its fixed finite-order local inverse, and its analytic rigidity consequence are retained. The new Proposition `prop:v6-sensitivity` proves the exact ratio of the limiting and one-flight top-jet diagonals:

`D_m(infinity)/D_m(1) = tanh(gamma)^m [coth(m gamma)+2m D_m]`,

where `D_m=(exp(2(m-1)gamma)-1)^(-1)-(exp(2m gamma)-1)^(-1)`.

For fixed positive gamma the bracket is `1+O_gamma(m exp(-2(m-1)gamma))`. The independent referee identified this comparison, and that contribution is explicitly credited. Its meaning is coefficient sensitivity with lower jets held fixed. It is not a full triangular condition-number estimate, a minimax experiment comparison, or stable analytic continuation. The revised discussion distinguishes exact probability germs, finite coefficient data, and finite noisy preparations. The long-chain factorization supplies a uniform relative physical limit; it does not reveal even contact jets absent from the nonlinear one-flight germ.

## SCR-R3 — Physical three-dimensional inverse versus independent-area four-dimensional inverse

The existing four-amplitude theorem is retained for the enlarged model in which area is an independent nuisance parameter. The physical support family has constrained area

`A_R(e)=A_0-pi R e_1/54+41 pi e_1^2/7776-5 pi e_2/432`,

with `A_0=sqrt(3)/2-pi R^2`. Theorem `thm:v6-three` proves that for every fixed reference radius some three of the first four amplitudes form a local coordinate system on that physical coefficient family. The argument restricts the invertible four-dimensional ambient differential to the rank-three graph of the area function and selects a nonzero three-row minor. It gives a finite collection of observation charts on compact reference-radius intervals; it does not assert the first three work at every radius.

At radius `R=1/4`, the first-three determinant identified by the referee is included with its exact derivative table and factorization:

`-2 sqrt(2) (15804720 A_0+64253 pi)/(72930375 A_0^4)`.

The coefficient inverse is locally Lipschitz; multiplicity-preserving cubic root recovery gives curvature exponent `1/3`. The existing physical two-sided path proves its sharpness. Variable measured gap is handled by the block-triangular map `(R,e) -> (1-2R,C_J)`.

## SCR-R4 — Charge the count experiment, including onset localization

The new count-only theorem has a deterministic preparation bound, including failure outcomes. It does not borrow the conditional-position acquisition rate. A supplied initial interval has fixed width inside a common one-flight onset collar; no accuracy-dependent coarse bracket is assumed free.

1. A count-only adaptive interval procedure uses at most `C h^(-2) log(C/eta)` preparations to produce an `O(h)` gap bracket. At a midpoint, a success gives an exact upper endpoint. On no success, a conservative lower-endpoint update has conditional error bounded using the quadratic onset probability. Geometric shrinking widths bound both the summed conditional error and the total cost.
2. Fixed-size one-flight batches and square-root interpolation give gap error `O_m(h^(m+1))`. The proof is the same calibration mechanism as before but applied to the sum of the unlabelled channel probabilities.
3. Fresh fixed-size count batches at a finite set of programmed offsets and Richardson extrapolation yield amplitude error `O_m(h^m)`. The normalized variance scale is `1/(n h^2)`. The calibrated timing error contributes `O(|gap error|/h)=O_m(h^m)`.
4. The physical coefficient inverse gives area error `O_m(h^m)` and matching curvature error `O_m(h^(m/3))`. A compact discrepancy estimator handles noisy vectors not lying in the exact image.

The total deterministic preparation upper bound is `C_m h^(-(2m+2)) log(C_m/eta)`. Thus a sufficient count-only curvature-accuracy order is `epsilon^(-(6+6/m)) log(C_m/eta)`. The selected conditional-position experiment retains its separate `epsilon^(-(2+2/m))` order and its own assumptions. Neither upper bound is advertised as minimax. Trial batches, rather than unbounded event waiting, ensure that failed localization outcomes do not produce an infinite or uncontrolled cost.

## SCR-R5 — Organize around the relative mechanism

The new sections extend the relative boundary argument to uniformly convex nonperiodic scalar twist chains and derive a relative locality consequence. If two admissible chains agree on their first and last `L` edges, their actions and their individually normalized mixed twists differ by `O_k(theta^L)` on a common endpoint box, regardless of the number or size of admissible interior changes.

The proof does not divide an absolute action error by an exponentially small twist. It uses the exact cofactor ratio, trace-class localized Hessian perturbations, operator-norm Green bounds, and differentiated logarithmic determinant series. Short shared segments identify each boundary action and amplitude up to `O_k(theta^L)`; the full-chain relative factorization then proves locality. A stable two-dimensional Morse change of variables transfers this estimate to the normalized onset law through every fixed right derivative, including zero offset.

The normalized law is divided by its own quadratic onset coefficient. No comparison of the raw rare probabilities or of the two leading transmission coefficients is claimed. General abstract chains are not asserted to be billiard realizations. The physical identification requires the already established contact localization and full-phase measure. This distinguishes the general mathematical mechanism from its geometric application.

## Assembly and verification still required

The full inherited article, companion, analytic realization, endpoint inverse, scalar nonidentifiability fibers, record response, acquisition proofs, circular calculations, and appendices must remain available. The new results must be integrated into that full manuscript, with the corrected abstract and observation hierarchy. Native references must be reconciled and the primary-literature comparison independently checked. A new build, optimized and nonoptimized diagnostics, PDF inspection, and remote branch-tip verification are required before reporting delivery. Old build reports and old diagnostic counts cannot be presented as new verification.
