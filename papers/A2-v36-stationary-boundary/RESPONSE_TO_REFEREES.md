# Response to the A2 v35 referee report

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*, A2 v36, 4 October 2026.

**Controlling report:** review/a2-v35-external-harsh-top4-rereview-2026-10-04, commit **985d798e172d38c0a9df2a068fe414b2fd13bcbc**.

**Reviewed source:** revision/a2-v35-self-calibrated-stationary-2026-10-04, commit **70c055e1ff090d58ecd61a5644e0fa62a7766f13**.

The report accepts the mathematical chains of the two-scale support inverse and common-stationary-noise lower bound, and identifies the rate gap, scale calibration, control accounting, exposition and source delivery as the principal issues. The revision addresses these issues by new proofs in the same collision experiment. The original theorem package and all its proofs remain active. Report section numbers below refer to the controlling report; TeX labels give stable manuscript locations.

## 1. Narrow the stationary exponent gap (report §§7.3, 9, 10.1)

**Revision:** Section 4; Lemma 4.1, Proposition 4.2 and Theorem 4.3 (lem:rare-coarse-normals, prop:rare-query, thm:rare-stationary).

The earlier query estimates two pooled means and subtracts them. A small occupation does not make either raw mean rare. The new proof constructs a rare event geometrically.

Fixed coarse reconstruction supplies a normal approximation throughout a tubular neighborhood of each radial bracket. The controller selects at most two near-maximizing outward compass vertices, including every true maximizer and all ties. At each shifted nominal center \(y+tv\), direction is still drawn from the original unobserved uniform compass law. A candidate is positive when a fixed finite batch contains a collision; the query takes the conjunction of these marks.

At an exterior point, one true maximizer forces every segment beyond the supporting line, giving exactly zero pooled probability. At inner depth at least \(e\), all selected candidates start free and have collision probability at least one quarter of the occupation mass. The local cost is
\[
C e^{-(\gamma+3/2)}\log(C/\varepsilon).
\]
The theorem explicitly requires the fixed design margin \(2t+D_*<d_0\). A dyadic step is chosen once from the strict footprint gap. Earlier statements under their weaker margin remain active; no direction-resolved observation is introduced.

For \(\gamma=0\), the bracket becomes
\[
c\nu^{-(s+1)/(s-2)}
\le N^*_{\rm stat}(\nu)
\le C\nu^{-(3s/2+1)/(s-2)}\log^2(C/\nu).
\]
The difference between the powers decreases from \(2s/(s-2)\) to \(s/(2(s-2))\), a factor of four. At \(s=7\), the old upper, new upper and retained lower powers are 4.4, 2.3 and 1.6. The lower-bound proof is unchanged. The new upper rate is not described as minimax.

## 2. Remove the supplied scale ratio (report §§7.1, 9, 10.2)

**Revision:** Section 5; Lemma 5.1 and Theorems 5.2 and 5.4 (lem:unk-scale-flux, thm:unk-scale-flux, thm:unk-scale-finite).

The two labelled settings have footprints \(A\) and \(rA\), with only known bounds \(1+g_*\le r\le R_*\). The ratio is an unknown. The physical first footprint is the dilation reference, so no unobservable latent unit is assigned to a parameter footprint.

For an isolated complete component,
\[
\Phi_C=\int_E F_1(x)\,dx=\frac t2\mathcal W(C),
\quad \mathcal W(C)=w_C(e_1)+w_C(e_2).
\]
Each collision strip has area equal to flight length times transverse width. Integration removes the unknown normalized density. Coarse data determine a domain containing the complete response support and excluding all other components. An obstacle width or area is not supplied.

For \(P_1=C+Q,\ P_2=C+rQ,\ D=(r-1)Q,\ a=(r-1)^{-1}\),
\[
a=\frac{\mathcal W(P_1)-2\Phi_C/t}{\mathcal W(D)},\qquad
r=1+a^{-1},\qquad p_Q=a p_D,\qquad p_C=p_{P_1}-a p_D.
\]
The denominator is at least \(4g_*r_K\), giving uniform stability. The argument uses the observed mean pairs, equivalently \((g_1,g_2,F_1)\). It does not identify \(F_1\) with a reciprocal difference.

An independent normalization is proved in Theorem 5.5 and Propositions 5.6–5.7 (thm:unk-scale-exact, prop:unk-scale-stability, prop:unk-scale-mass). The differences \((g_1,g_2)\) alone determine the ratio under the weaker separation: occupation mass equals \(|C|\), and the mixed-area quadratic has a unique physical smaller root with discriminant \(V(C,D)^2\) bounded away from zero. A finite killed-walk adjoint measures this mass from reciprocal bits.

Exact homothety and the fixed common laboratory origin remain assumptions. An unknown common unscaled offset translates the reconstructed table; translating that offset and the table together leaves every bit unchanged. This gauge is stated directly. Inherited theorem headings now use calibrated-homothety terminology; the new result explicitly identifies which scale information is learned.

## 3. Joint sample and input-description bounds (report §§7.2, 10.3)

**Revision:** Theorem 5.4, equations eq:unk-scale-attempts, eq:unk-scale-centers and eq:unk-scale-control-description; the resource statement is adjacent to the leading rate in §1.3.

The scalar integral is estimated to error \(m=O(\nu)\) with \(O(\nu^{-2}\log(C/\delta))\) pooled bits. This suffices for the final \(C^2\) loss and need not equal the finer boundary mesh. Since the boundary power exceeds two, learning the ratio does not enlarge the leading attempted-bit power.

The added integral-measurement centers are charged:
\[
J_\nu\le C\nu^{-1/(s-2)}\log(C/\nu)+C\nu^{-2}\log(C/\delta).
\]
The complete center, setting and repetition-count list has binary length bounded by this expression times \(C\log(C/(\nu\delta))\). The finest dyadic nominal mesh is \(O(\nu^{s/(s-2)})\).

For finite-grid commands, the quadrature proof conditions on the launch displacement and bounds boundary cells of convex bodies and segment sweeps. It uses neither a density upper bound nor a pointwise density modulus. The theorem prices observations and digital command descriptions. Physical homothety certification, manufacture, travel, realization of nominal positioning and arithmetic running time remain distinct resources.

## 4. Preserve the converse and period scope (report §§7.4–7.5)

**Revision:** Section 6 and Appendices E–G, with the relevant distinctions repeated in the introduction.

The stationary converse retains its fixed nondegenerate physical subclass, common known uniform-disk law, deterministic laboratory frame, bounded short commands and worst-case expected attempts. Direction-specific commands and scale selection in a fixed positive interval are permitted. Observed launch positions, analog outputs, unbounded flights and vanishing spreads are not added to its conclusion.

Finite primitive-orbit and rational-period decisions retain the bounded periodic prior and known positive nonperiod-patch margin. Exact recognition and pointwise eventual decisions without a supplied margin remain separate statements. Euclidean period vectors remain estimates.

## 5. Give stationary results primary narrative weight (report §10.4)

**Revision:** main.tex and SUBMISSION_MAP.md.

The abstract and introduction lead with rare pooled boundary queries and identification of an unknown homothety ratio. Sections 2–6 contain the occupation inverse, footprint separation, new boundary query, integral normalization and common-noise converse. Complete localized and earlier resource results follow in Appendices A–H. The article is self-contained.

All 117 labels of the controlling v35 source remain active, and all 33 original proof bodies are retained byte for byte. Formal statements increase from 36 to 46, and proofs from 33 to 43. Earlier repository directories and the controlling review are unchanged. The title, topic and original mathematical conclusions are retained.

The comparison section credits active line search/interpolation, informative rare responses, convex support and mixed-area identities, and query-precision accounting to their predecessors. The Brunel–Klusowski–Yang reference now gives its final Bernoulli publication. No exhaustive priority claim is made.

## 6. Repair source delivery (report §§8, 10.5)

**Revision:** tools/, SOURCE_PINS.json and .github/workflows/a2-v36-verify.yml.

The native v35 failure is reproducible: the first align row in core/00_setting.tex has a single trailing backslash, causing two labels to occupy one row. The retained localized statement corrects this separator without changing the expression.

The new package contains the diagnostic and validation routes it documents. Its manifest binds active sources, documentation, tools and workflow, and pins the preserved v35/v34/review trees. The validator rejects unexpected, missing and altered sources; verifies active input closure and retained proof content; runs ordinary and optimized diagnostics; builds the actual primary; and retains source archives, logs and a receipt on success or failure. The hosted workflow checks out its triggering SHA and uploads available evidence even when qualification fails.

The local manuscript has compiled to 48 pages without final TeX warnings or unresolved references, and all pages were rendered for layout inspection. The generated receipt records actual diagnostic counts and whether a clean exact commit was qualified. Historical v34 success and the failed v35 run are not reused as v36 evidence.

## Scope of the response

The revision gives new proofs for the rate and calibration objections, makes the added control count explicit, preserves the accepted theorem package and repairs source delivery. The remaining stationary exponent gap and the external reference required by an unknown common offset are stated precisely. These revisions and finite verification tools do not imply referee or journal acceptance.
