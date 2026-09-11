# Response to the A2 v14 referee report

**Revision:** A2 v15, 11 September 2026.  
**Article:** *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.  
**Frozen report:** `0c523413ef7ffa2dedd1ab471ce58b3275896a93`, `reviews/a2-v14-independent-harsh-intrinsic-density-2026-09-11/REFEREE_REPORT.md`, together with `SCALAR_LINEARIZATION_AND_WIDTH_BENCHMARK.md`.  
**Reviewed author source:** `e136929b120912586266fb78e0ae7b3c9d43bfd6`, native manuscript tree `d516d2bc9230ea4a333f3d41ba2718485a307b27`.

We thank the referee for distinguishing the mathematical questions closed in v14 from the remaining attribution, notation and significance questions. This revision preserves the general smooth physical theorem, the independent-contact geometric inverse and its physical image, and the complete-profile observation theorem. It adds the requested scalar comparison with a full uniform proof and identifies its product with the physical Fredholm determinant, rather than treating classical scalar linearization as a separate new mechanism. No geometric or observation hypothesis is silently strengthened to replace a proof, and no existing mathematical section is removed.

## C14-1. Classical smooth scalar linearization

**Comment.** A smooth scalar contraction already has a uniquely normalized smooth linearizer. Its density admits an elementary infinite-product construction and its normalized iterates converge. These conclusions do not require analytic two-dimensional normal forms and should not be credited to the determinant construction as new scalar linearization results.

**Response.** We agree with the comparison and have incorporated it at the level of both statements and proofs. The introduction's hyperbolic comparison now distinguishes the classical scalar construction from the physical amplitude identification. In Section 8, the new Lemma `lem:v15-scalar-product` proves the following for a jointly smooth family of contractions on a common interval:

\[
 h_\xi(u)=\log(R_\xi'(u)/\lambda_\xi),\qquad
 \mathfrak B_\xi(u)=\exp\sum_{i\geq0}h_\xi(R_\xi^i(u)),\qquad
 \mathfrak z_\xi(u)=\int_0^u\mathfrak B_\xi(x)\,dx.
\]

The proof includes every fixed mixed parameter and endpoint derivative. It first obtains summable polynomial-times-exponential bounds by differentiating the orbit equation. It then proves the density cocycle, integration to the linearizing coordinate, normalized uniqueness, the finite derivative-product identity, and the sharper iterate rate for every fixed strict margin above the maximum return multiplier. The positive lower multiplier bound and the common fixed point are explicit hypotheses. This is presented as a self-contained classical lemma, with Sternberg and Eynard-Bontemps–Navas cited, and with the referee memorandum acknowledged for the requested comparison and product argument.

The new Corollary `cor:v15-determinant-product` states the exact identification

\[
 \frac{\exp U_b(u)}{\det(I+G^{(b)}\Delta H_b(u))}
 =B_b(u)
 =\exp\sum_{i\geq0}\log\frac{R_b'(R_b^i(u))}{\lambda}.
\]

Its finite logarithmic remainder is exactly `log B_b(R_b^n(u))`, not an unspecified asymptotic error; it has the stated mixed-norm exponential bound. The proof identifies the physical density by the existing exact Schur-concatenation theorem and then uses uniqueness of the normalized scalar density. This makes the logical dependence explicit: the physical factorization proves which density enters the collision probability; classical scalar theory identifies that density's coordinate meaning. The scalar lemma is not used circularly to establish the finite-bridge relative theorem.

**Locations:** `article/01_introduction.tex`; `article/16a_scalar_linearization.tex`; `article/16b_determinant_transport.tex`; their active inputs in `article/16_hyperbolic_coordinates.tex`; abstract, acknowledgments and bibliography. The previous analytic proposition and complete physical cocycle proof remain active without alteration of their statement/proof blocks.

## C14-2. Flight and return multipliers

**Comment.** In the reviewed text, Section 8 uses `lambda` for the return multiplier and `r_b` for the first-hit derivative, whereas the independent-contact section uses the same symbols for the single-flight factor and curvature ratio.

**Response.** A single local convention now applies to both sections:

\[
 \varrho=e^{-\gamma},\qquad \lambda=\varrho^2=e^{-2\gamma},\qquad
 \mathfrak r_b=\sqrt{c_b/c_{1-b}},\qquad r_b=\mathfrak r_b\varrho.
\]

Thus `j` counts flights, `n` counts returns, and `j=2n` for the return comparison. The curvature ratios multiply to one; the first-hit derivatives multiply to `lambda`. The freely chosen error rate `rho` remains distinct from the exact factor `varrho`. We use `mathfrak r_b`, rather than `chi_b`, because the latter already denotes the inverse Morse coordinate in the energy-profile construction.

The entire independent-contact source differs from its frozen predecessor only by the two explicit alpha-renamings `lambda -> varrho` and `r_b -> mathfrak r_b`. Reversing these substitutions reproduces that source byte for byte. New rational tests check the return/flight conversion in the exact hyperbolic-sine reference, both concatenation parities, the curvature scaling in the last-jet block, and its inverse, including equal curvatures. A deliberately wrong return multiplier fails the corresponding identities.

**Locations:** introduction, `eq:v15-multiplier-convention`; beginning of the smooth intrinsic subsection; `article/23_two_contact_rigidity.tex`; `tools/verify_v15.py`.

## Width, energy profile and asymmetric contacts

The revision now prints both directions of the equivalence:

\[
 \mathcal W_b(E)=\int_0^E x^{-1/2}\mathcal V_b(x)\,dx,
 \qquad \mathcal V_b(E)=\sqrt E\,\mathcal W_b'(E),\quad E>0.
\]

The weighted derivative extends smoothly with value one; `W_b(E)=2 sqrt(E)+O(E^(3/2))`. The width and profile are therefore two representations of one complete invariant. The width interpretation is not counted as an additional independent rigidity theorem. The existing corollary and energy-pushforward proof remain in the article.

For asymmetric contacts the width gives the difference of the action's inverse branches, not their midpoint. The even-contact inverse retains its additional hypotheses and its separate geometric block calculation. The abstract width shear in the referee's benchmark is not asserted here to be a physically realized billiard deformation. Conversely, the actual independent-contact analytic realizations already proved in the article are retained with their full physical constraints.

## Significance and the positive mathematical content

The report's publication recommendation is principally a judgment of significance. We respond by sharpening the theorem-level contribution and preserving its scope, not by replacing it with an unsupported broader rigidity assertion or by removing the demanding parts of the argument.

The forward result concerns actual smooth periodic dispersing billiards and selected physical collision events on a nonshrinking collar. Its normalized finite cofactor, trace-norm boundary comparison, exact parity-dependent reference and residual-time integration jointly control every fixed mixed geometric and offset derivative. Classical scalar linearization does not itself supply this relative physical probability statement. The analytic comparison is retained with its physical projection and its explicit uniform-chart hypotheses.

The geometric result supplies an explicit independent two-contact inverse at fixed labelled leading geometry, including coincident curvatures, together with analytic physical realizations invisible to the selected leading hierarchy. The two-flight theorem remains the direct finite-record benchmark and observation design. We do not manufacture a need for long records in that finite-jet problem; its finite-jet coordinate equivalence does not identify the finite and limiting law functions or their noisy experiments.

The function-valued result concerns general smooth contacts, without the evenness assumption. It determines the complete symmetrized boundary invariant by Volterra uniqueness and gives a separately charged, regularized binary observation procedure with smooth-class calibration. The sufficient preparation bound, its regularity and convergence certificates, and the finite-family restrictions remain exactly those printed in the reviewed mathematical statements. The physical calibration removes the actual gap, area and multiplier; it does not supply the separate labelled curvatures used by the geometric inverse.

These are the positive results submitted for renewed assessment. Their significance should be evaluated together with their hypotheses and closest comparisons; a source-retention check or a finite numerical test does not settle that editorial judgment. The revision makes no assertion of journal acceptance or of an exhaustive priority survey.

## Earlier requests and preservation

The v14 report records the main v13 requests as closed. Their resolutions remain active: the analytic mixed-boundary comparison and canonical-to-physical projection; exact reference normalization; the finite-family restriction in the abstract; the distinction between exact two-flight germs and charged observations; full-profile regularization and its pilot; and the separate comparison with marked-length and spectral rigidity. No closed issue is reopened by deleting its proof or by narrowing the main physical theorem.

All 52 top-level TeX input commands remain in their original order. The two new scalar/transport inputs are inserted inside Section 8. All original statement/proof blocks in the edited mathematical files are retained, modulo only the reversible contact-section notation change. The new native manuscript tree is built directly on the frozen complete v14 tree, so all other active inputs, inactive historical materials, companion source and auxiliary proofs are inherited unchanged. Original versions of every overridden source or metadata file are stored under `history/v14-reviewed/`. The old manuscript and review directories are not modified.

## Executed verification and limits

The pinned referee diagnostic source was reproduced byte for byte and rerun: 3,216 checks pass in normal and optimized Python, with byte-identical JSON outputs. The new v15 suite passes 10,549 explicit checks in `--scope edited`, likewise identically under `-O`. This includes exact finite products, normalization and inverse-block identities and the six-file source pins. These are finite diagnostics, not formal proof certificates.

An isolated 18-page build of the revised sections and bibliography completed in two LaTeX passes, with no undefined control sequence and no overfull box. The multiplier, scalar lemma, its proof and the physical-product pages were rendered and visually inspected. References to inherited sections are intentionally unresolved in this isolated wrapper. The full native article and its companion were not compiled in this revision session; the recorded test is not labelled as that build. A full-checkout retention mode and complete build commands are supplied in the README. The attempted source-export Actions run returned failure before usable execution logs, and is not counted as a successful CI run. Its temporary workflow is absent from the delivered tree.
