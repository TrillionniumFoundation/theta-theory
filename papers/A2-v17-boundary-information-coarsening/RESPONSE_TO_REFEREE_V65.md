# Response to the independent v64 report

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 65, September 16, 2026

This responds to `reviews/a2-v64-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md` at `838e62dd0435f350ca9f398df09374e189a6e44c`. The mathematical baseline is `ee2380ceb76808dd2969d6b5faaa180737020eff`, not an inferred or unbuilt revision. The report is an author-requested AI-assisted external-referee-style assessment, not a commissioned journal report.

## The substantive change

The report establishes no new mandatory core correction within its stated coverage. In particular, it accepts the broader periodic forward mechanism while reserving judgment on exceptional significance. We do not recast that reservation as a missing arithmetic lemma. We respond with a geometric inverse for the newly available periodic laws.

New Section 9, `article/10b_periodic_contact_inverse_v65.tex`, contains nine statements and their proofs. It starts from a **fixed marked collision polygon**, including contact points, tangent choices, phase labels and closing translation, and phase-resolved laws of scaled tangent projections at **two fixed positive offsets**. Curvatures, normal graph values and flux amplitudes are not supplied. The new inverse is local. These are different data from the retained gap-only alternating experiment; the latter's stronger calibration, unmarked-lattice and preparation-budget conclusions are not transferred without proof.

Two density ratios first recover the unequal physical endpoint actions, with both unknown normalizers and both amplitudes cancelled. For normalized graphs

\[
R_i(x)=q_i+\nu_i^{-1}(t_i x-n_i F_i(x)),
\]

the derivative of the actual future action counts the initial graph variation once and internal visits twice. At order \(n\) its block is

\[
\mathcal C_n=(I+T_n)(I-T_n)^{-1},\qquad (T_nz)_i=\sigma_i^n z_{i+1},
\]

where the **signed** one-step derivatives satisfy \(|\sigma_i|<1\). This includes an invertible curvature Jacobian. It also includes odd contact cycles and odd jet orders, for which discarding the signs is incorrect. The determinant is \((1-(-1)^r\Lambda^n)/(1-\Lambda^n)>0\), with \(\Lambda=\prod\sigma_i\); it is not asserted to equal one for every cycle.

The complete analytic inverse is proved in a space of bounded holomorphic anchored graphs, not inferred from the diagonal blocks. The derivative consists of an invertible multiplier plus contracted evaluations. One finite low-degree inverse and a norm-convergent tail inverse control the full operator, including all lower-degree couplings. The proof permits curvature variations and handles protected interior derivatives without treating boundary differentiation as bounded on \(H^\infty\).

Consequences include all finite smooth jets, complete analytic contact germs, conditional stability from real density error with an analytic prior and radius loss, and exact fixed-lattice analytic table rigidity when every labelled obstacle is visited. A nonnormal three-obstacle analytic family has a fixed collision polygon and independently varying contact curvatures. This is an actual geometric realization, not a prescribed Jacobi sequence.

## Point-by-point disposition

| Report point | Revision and location |
|---|---|
| **R64-M1:** signed/scaled geometry and coercivity | The complete v64 proof is unchanged. Lemma 9.1 derives the graph Hessian with signed mixed entries and positive mass \(2F_i''(0)\). It proves strictly contracting one-step tails and relates graph sensors to signed arclength with the correct action gauge and endpoint Jacobians. |
| **R64-M2:** chronological transfer, Dirichlet cofactor and half masses | All existing formulas and proofs are unchanged. The new contact response is a boundary-variation operator, not a replacement of the Dirichlet determinant by Hill's cyclic determinant. Its initial multiplicity is one, internal multiplicity two. |
| **R64-M3:** weighted estimates and differentiation scope | Retained unchanged. Lemmas 9.3 and 9.5 use the weighted construction and distinguish separately fixed smooth derivatives from analytic norm estimates. The analytic construction allows quadratic variations, contributing an explicit \(O(\delta R)\) term. |
| **R64-M4:** relative trace-class comparison | Retained unchanged and used as a prerequisite. The new inverse begins after the physical relative law; it does not attempt to obtain a relative law by dividing an absolute action error. |
| **R64-M5:** connected action and scalar linearizer | Retained unchanged. Neither scalar linearization nor the Cayley-transform algebra is advertised as a new general theorem independent of its geometric realization. |
| **R64-M6:** physical clock, window and charged normalization | Proposition 9.2 extracts \(A=S^- -pu\) and \(C=S^+ +pv\), not the incorrectly gauged residual. Positive offsets and denominator floors are explicit. Conditional reconstruction is not an acquisition-cost theorem. The original success mass and all charged alternating experiments remain intact. |
| **R64-M7:** genuine nonnormal realization | The original three-disk/scalene realization remains unchanged. Proposition 9.9 perturbs actual analytic closed obstacles while fixing the same polygon and independently varying its curvatures. The physical period is three; six oriented steps do not create six independent germs. |
| **R64-E1:** general forward versus alternating-only inverse; significance | Theorems 9.4 and 9.6 and Corollary 9.7 now give a general-period marked contact inverse. The new theorem's additional marks, two-offset observations and local scope are stated in the abstract, shared introductory Theorem 1.1 and Section 9. Its relation to the existing weaker-data alternating inverse is explicit. This changes the mathematical contribution; exceptional journal placement remains a judgment for the next referee. |
| **R64-E2:** no artificial repair condition | We do not claim that the report required this extension, that another certificate resolves significance, or that grazing/unbounded-period/unmarked-spectrum theorems are missing hypotheses of the printed statements. No inherited content was removed to narrow the claims. |
| **R64-D1–D4** | Preserve the report's scoped finding of no mandatory core repair; preserve the broader forward domain and its physical conventions; add the marked periodic inverse with its own observation model; do not transform a placement reservation into an alleged arithmetic error or an established priority verdict. |

## Proof map for the next examination

The shared principal/full Section 9 is organized by mathematical dependency:

- Lemma 9.1 and Proposition 9.2: physical graph coordinates and law-to-action extraction.
- Lemma 9.3 and Theorem 9.4: actual smooth envelope, finite-jet factorization, curvature and all higher cyclic blocks.
- Lemma 9.5 and Theorem 9.6: Banach-valued half-lines and the full analytic inverse.
- Corollary 9.7, Theorem 9.8 and Proposition 9.9: density-error inversion, conditional analytic stability and physical nonnormal rigidity.

These labels refer to the principal article; the full manuscript has its own numbering, with the same proof bodies. The introductory theorem is a roadmap to these statements, not an additional theorem count.

## Retention, literature and verification

All **800** frozen baseline files remain. **793** are byte-identical in place. The seven changed entry/framing/bibliography files have byte-exact originals under `history/v64-review-baseline/`; the complete v64 manifest records their original Git blobs and SHA-256 values. Every inherited mathematical proof module is unchanged, including the complete periodic-itinerary module and the corrected finite-experiment and position-pilot modules. All **129** distinct inherited active TeX paths remain active; the two new shared inputs make **131**. This is a retention census, not a theorem census or a fresh certification of all inherited proofs.

`HISTORICAL_DERIVATION_AUDIT_V65.md` identifies the derivations reused. `LITERATURE_CHECK_V65.md` records the primary-source comparison and its limits. In particular the supplied marked-polygon/function-law data are not identified with an ordinary or enriched marked length spectrum. No claim of exhaustive priority is made.

`tools/check_revision_v65.py` independently checks the new finite cyclic algebra, curvature response, actual Euclidean chord envelope and two-offset extraction, alongside unchanged v64 transfer/geometric checks. Normal and optimized runs must agree. The native build uses the retained provenance engine with fresh auxiliary files and shell escape disabled; exact source identities and final PDFs are recorded in the versioned delivery. Finite diagnostics, source integrity, visual inspection, mathematical proof and exceptional significance remain distinct forms of evidence.
