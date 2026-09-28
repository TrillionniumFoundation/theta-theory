# Response to the referee report on A2 revision 59

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Revision 60 — September 16, 2026 — Qian Qi**

The addressed report is `reviews/a2-v59-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`, frozen at `f480cf1d099128c0c84df1ed149cff9b75e6ba2d`. It reviewed mathematical source `b56282439324435668ae80be90207fe7f5eebbf2`, not the preparation commit or the review-ready navigation layer. The complete report and its `AUDIT_LEDGER.md` were read. This exchange is author-requested and AI-assisted, not commissioned journal refereeing.

## 1. The mathematical status and the response chosen

We thank the referee for recognizing that Theorem 12.12 in revision 59 is an inverse for the complete analytic action map, including its lower-degree couplings. We retain its proof in full. We do not treat the earlier diagonal estimate as the strongest current result, nor describe the new revision as repairing a theorem found false: the report establishes no mandatory new core repair within its stated coverage.

Revision 60 follows the suggestion in R59-E2 to isolate the functional-analytic structure, and then addresses the observational distinction in R59-S1 constructively. The new shared subsection contains three proved statements. Proposition 12.13 gives a precise contracted-evaluation criterion. Lemma 12.14 proves an explicit conditional restriction estimate by interpolation. Theorem 12.15 combines that estimate with the complete analytic inverse to control whole contact germs on an inner disc from real conditional laws. It also gives conditional total-variation and histogram bounds when one additional real Lipschitz bound is imposed. These results are inside the contact-inversion section of both complete entries, not a new detached statistical section.

The new theorem is not an unconditional upgrade of the old analytic norm. The analytic neighborhood is fixed before the errors; the output disc is strictly smaller; density and anchor margins are retained. The proof does not infer outer-disc smallness from real data. This distinction is the reason the new conclusion is valid rather than a contradiction of the report's monomial example.

## 2. R59-M1–M3 and R59-D2: preserve the complete analytic advance

Lemmas 12.10–12.11 and Theorem 12.12 remain verbatim. In particular the uncontracted initial graph is used only through its value in the interior stationarity equation. All differentiated graphs are evaluated on protected smaller discs. The finite terminal term is still estimated before taking the infinite limit, and the initial visit is counted once while internal visits are counted twice. The compact approximation is on the same function space; no holomorphic-radius gain is attributed to the full operator.

Proposition 12.13 formulates the additional structure separately. A bounded holomorphic invertible multiplier plus a summable family of strictly contracted evaluations has a small high-vanishing tail. After one tail order is fixed, invertibility is equivalent to nonsingularity of the finitely many remaining graded blocks. The proof includes both implications and the inverse bound. It is not an inference from a diagonal estimate for an arbitrary triangular matrix. The compactness proof also includes an explicit finite-rank approximation.

The qualitative Fredholm check and the suggestion to isolate this structure are attributed to the v59 memorandum in the text and bibliography. The criterion and the inverse-function step are elementary functional analysis, not claimed as a new general Fredholm theory. The billiard-specific input remains the protected holomorphic construction and the actual stationary envelope. This distinguishes reusable reasoning from the geometric hypotheses that make it applicable.

## 3. R59-S1 and R59-E1: a conditional real-observation consequence

Theorem 12.15 fixes a local neighborhood of a real analytic positive-curvature contact pair in a bounded-holomorphic space on an outer disc. Both gap and curvatures may vary. Two candidates in this neighborhood have actions bounded on that outer disc; their restrictions lie in one local inverse ball on an inner disc. This is a geometric regularity prior, not a conclusion from accurate data.

For signed, contact-centered densities at the same known positive offset, separate positive recording factors cancel in the four-density ratio. No analyticity of those nuisance factors is needed. Uniform real density error `epsilon` gives uniform real action error `C epsilon` using only density and scalar-anchor margins. The elementary interpolation lemma then gives inner-disc action error `C epsilon^theta`, where

`theta = log(1/b_0) / log(A_0/b_0)`,

`A_0 = 2(r+s)/s`, and `b_0 = (r+s)/(varrho-s) < 1`.

The full analytic inverse on that inner disc yields

`||psi-psi_tilde||_r <= C (|g-g_tilde| + epsilon^theta)`.

All contact coefficients are controlled simultaneously in the explicitly weighted analytic norm. There is no order-dependent cascade of real derivative estimates. The leading Hessians are bounded coefficient functionals of the recovered inner-disc actions, so they need not be separately supplied as measurements.

Under a common Lipschitz bound for the real densities on a larger positive square, a direct two-dimensional smoothing argument gives exponent `theta/3` from local L1 error, hence from total variation. Cell-average approximation gives the corresponding bound from cell-mass error plus the stated mesh bias. The proof of this interpolation step is printed in the principal article; it imports no full-manuscript acquisition theorem.

This differs from the existing quantified full-table histogram theorem. That theorem controls finitely many real derivatives and contact jets before a separately quantified global continuation and registration step. The new theorem uses the complete function-space inverse to obtain a fixed power for an entire local germ, on one already selected analytic neighborhood. It does not replace the global theorem or its hypotheses. The conditional continuation argument itself belongs to standard analytic background, as discussed by Trefethen; its short proof is included so that the constants and the radius loss are explicit.

## 4. R59-G1–G4 and R59-D3: boundaries and closed corrections retained

The relative determinant proof, actual-smooth remainder estimate, signed density extraction, origin-visible interior-window theorem, finite reconstruction fibers, unknown-lattice cochain and common-strip differential theorem remain unchanged. The contact frames, signs, units and offset are supplied in the new stability theorem; it is not a new noisy centering theorem for unknown origins. Finite matching alternatives remain, and a local germ need not extend to an entire periodic obstacle.

The new estimate concerns pairs of locally admissible candidates. It does not assert that arbitrary corrupted densities lie in the exact analytic inverse's image, or supply a globally defined estimator. Its exponent is not claimed optimal. Uniform constants over arbitrary analytic tables, vanishing anchor margins or coalescing analytic radii are not asserted. The recorded density prior is separate from an efficiency lower bound: rescaling efficiencies can leave the conditional law unchanged and make preparations arbitrarily rare.

Corollary 19.9 remains explicitly dependent on full Theorem F.47.3 and its sensor, analytic-family, calibration and charged-preparation assumptions. The new proof does not use that acquisition theorem. The dependency ledger retains the established eight comparison/background targets and one substantive theorem input. A syntax scan is still not described as a semantic proof certificate.

## 5. R59-E1/E2 and R59-D1/D4: article-level assessment

The principal article continues to lead with the relative law and actual-smooth inverse. The constructive analytic theorem remains in its proof path, followed by the structural criterion and the conditional observation estimate. The latter is a direct consequence of the stronger core inverse under explicitly different inputs, not another routine stopped-record consequence.

We do not claim that adding these statements mechanically resolves the journal-placement judgment. The mathematical case is that the relative boundary law yields a full local action coordinate system and, under analytic regularization, an all-order local contact estimate from real law data. The scope and analytical cost of each arrow are stated. A specialist can assess the significance of that mechanism without treating the finite matching or standard inverse-function argument as independent breakthroughs.

No earlier theorem is weakened or removed. All 122 inherited active source paths remain. The author preservation checker verifies all 580 inherited statement/proof blocks verbatim, including 274 proof blocks; shared display copies are not counted as distinct mathematical results. Eight edited source files have exact archived originals, and 114 inherited inputs remain byte-identical in place. The new common subsection adds one proposition, one lemma, one theorem and their three proofs. The full technical corpus and companion remain compiled.

The final review-ready record identifies the actual committed source, all three native PDFs, verification results and actual visual coverage. Builds, finite controls and block preservation are not mathematical or journal-significance certificates. The next review should examine the conditional norm transfer and its stated prior, alongside the retained relative/action mechanism.
