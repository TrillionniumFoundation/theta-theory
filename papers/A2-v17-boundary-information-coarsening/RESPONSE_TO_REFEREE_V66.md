# Response to the referee on A2, revision 65

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 66, September 16, 2026  
**Report answered:** `review/a2-v65-independent-harsh-top4-2026-09-16`, immutable head `7f4603531f7b97a23ce627fec47b7ddc5f4f9912`, report blob `44a677ec4f967f90b5a89851ea794fdb8e19666d`.  
**Reviewed mathematical source:** `06a197e4d11bc3d4193e9f0b7904105df35875fa`, manuscript tree `469aba06035399f96f07417b172653228df36114`.

## 1. What the report establishes, and what this revision changes

We thank the referee for distinguishing the correctness of the marked periodic inverse from its exceptional-significance case. The report establishes no new fatal error or mandatory core repair in its stated coverage. We do not relabel the preceding extension as a correction of a false theorem, and we do not describe the present extension as closing a technical defect that the report did not find. The report's restricted mathematical coverage is not a certificate of every inherited result.

There are two changes. First, we replace the catalogue-led opening with a common account of the relative physical law, the actual boundary response, and the distinct observation models. Second, we strengthen exact marked identification: the curvature map has a global inverse on its positive-curvature image, and hence equal marked laws identify analytic contact germs and, with fixed lattice and full visitation, entire obstacle images **without requiring the candidates to be close**. The complete local analytic norm theorem and its conditional real-law stability are retained as separate, quantitatively different conclusions.

The new quadratic argument is suggested by the Riccati comparison in R65-M5. It uses that identity in a nonlinear inverse direction not asserted in the report. We attribute the comparison in both bibliographies and acknowledgments. The new global theorem, its algorithm, and the subsequent consequences are proved in `article/10c_global_curvature_inverse_v66.tex`. They are not supported by an appeal to the report's recommendation or by numerical evidence alone.

## 2. New mathematical argument

For the same fixed marked polygon and measured graph coordinates, put

\[
k_i=L_i^{-1},\qquad c_i=F_i''(0)>0,\qquad s_i=(S_i^-)''(0).
\]

The first edge followed by the actual stationary half-line gives the boundary Schur complement

\[
s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}},\qquad
 a_i=\frac{k_i}{k_i+c_{i+1}+s_{i+1}}\in(0,1).
\]

Lemma `lem:v66-riccati` proves this directly and proves the converse by constructing the decaying Jacobi solution. It does not select an arbitrary algebraic Riccati solution as a physical action.

For positive observed quadratic data define

\[
(\Phi_s z)_i=\left[s_i-k_i+\frac{k_i^2}{k_i+s_{i+1}+z_{i+1}}\right]_+,
\quad z\ge0,\quad
q(s)=\max_i\left(\frac{k_i}{k_i+s_{i+1}}\right)^2<1.
\]

This map takes the closed positive orthant into the box with upper corner `s`, and is a strict contraction there. Its unique fixed point is the curvature vector whenever the data are realizable. Conversely, strict positivity of that fixed point characterizes the positive-curvature image. Theorem `thm:v66-curvature` proves the image characterization, global real-analytic inversion, an a posteriori iteration bound, and a two-point Lipschitz bound whose constant is determined by the action data. The positive-part extension handles positive nonrealizable data without silently admitting zero-curvature tables. An explicit positive vector outside the geometric image is included.

Once curvature is identified globally, the existing actual-smooth signed recursion identifies all higher jets. Its signs are still those of the physical contact cycle; no orientation doubling removes odd contact information. Theorem `thm:v66-global-rigidity` therefore proves exact finite-jet and analytic-germ identification for arbitrary candidate contacts in the stated positive class, with no local branch choice. The fixed-lattice/full-visitation conclusion follows by the same analytic continuation argument as before, now without a closeness condition on the tables.

This exact result does **not** turn analytic coefficient uniqueness into a global same-disc norm estimate. The full Banach-space inverse from v65 remains necessary for its norm bounds, including the lower-degree couplings. Its real-observation estimate still has a local bounded analytic prior and a smaller output disc. Proposition `prop:v66-finite-flight` separately proves a fixed-order finite-flight reconstruction bound on compact positive classes, using the global quadratic inverse before the signed recursion. Density error is the input to that proposition, not a number of preparations.

The normal two-contact specialization is printed explicitly and agrees with the retained alternating curvature formulas. This relates the geometry of the two inverses; it is not an equivalence of their observations.

## 3. Point-by-point disposition

| Referee point | Response and location |
|---|---|
| **R65-M1: legitimate graph sensor and substantial marks** | Retained without weakening. The new opening lists collision points, signed frames, phase labels, closing translation, flight geometry and measured tangent projections. Curvature and normal graph heights remain unknown. Both new exact theorems fix these marks. The original graph-sensor proof is unchanged. |
| **R65-M2: nonlinear gauge correction** | The complete graph/arclength comparison is unchanged. Physical momenta are restored before action extraction, including in the new principal theorem. No unobserved coordinate conversion is made an input to the inverse. |
| **R65-M3: shared two-offset amplitudes** | The common-amplitude hypothesis is explicit in the opening, the new global theorem and the response. The normalizers may differ. Arbitrary offset-dependent recording distortions are not cancelled by this theorem. We retain the separate alternating nuisance theory under its own assumptions. |
| **R65-M4: actual envelope and smooth-jet factorization** | The complete envelope proof remains byte-identical. The new higher-order uniqueness proof explicitly uses actual-smooth factorization before inducting on jets. It concludes equality of smooth jets, not equality of arbitrary smooth germs. |
| **R65-M5: curvature and signed cyclic blocks** | We preserve the full old calculation and add a global quadratic inverse based on the nonlinear Schur complement. The direct equal-data cyclic comparison and the contraction algorithm are both proved. Odd-cycle signs in degrees above two remain unchanged. The Riccati comparison is attributed, not claimed as newly discovered here. |
| **R65-M6: variable-curvature analytic construction** | The original degree-two Banach neighborhood, protected arguments, terminal estimates and holomorphic dependence proof are unchanged. The new exact uniqueness result does not require or replace a new complex extension of every closed obstacle. |
| **R65-M7: complete inverse rather than diagonal inversion** | The finite-low/tail inverse is retained and explicitly distinguished from global coefficient identification. Uniform induced quotient bounds continue to refer to the complete local analytic operator, not unweighted derivatives or a global operator bound. |
| **R65-G1: finite-flight and real-noise order of operations** | We keep finite law comparison before rational extraction and anchoring. The new fixed-order proposition replaces only the quadratic branch-selection step by the global contraction. Real-law Hölder estimates remain local and conditional with radius loss. No general-period confidence or total-preparation rate is asserted. |
| **R65-G2: whole-table identity has supplied placement and coverage** | Fixed lattice, common polygon, labelled connected analytic boundaries and visitation of every obstacle remain hypotheses. The new result removes only the closeness condition on the candidate tables. It is not unmarked reconstruction or unknown-lattice recovery. |
| **R65-G3: nonnormal three-contact realization** | The entire realization and its independent curvature variations are retained. The new uniqueness theorem applies to any two members satisfying the stated same-mark observation conditions; local perturbation is still how that physical family is constructed. We do not replace a geometric realization by freely chosen scalar recurrence coefficients. |
| **R65-L1: comparison concerns different data** | The opening and `LITERATURE_CHECK_V66.md` compare precise observations. No theorem is claimed about reconstructing these endpoint laws from a marked length spectrum. No priority or redundancy conclusion is inferred from the targeted search. |
| **R65-E1: exceptional significance** | We present the strengthened result and its exact observation model for a fresh assessment. The global curvature inverse removes a real local ambiguity condition, but does not remove the supplied polygon or function-valued data. We do not claim that this extension mathematically settles an editorial judgment. |
| **R65-E2: synthesis, not artificial repairs or theorem inflation** | Both entries now begin with one shared mechanism-led theorem. The old alternating lead is retained, moved under an explicit alternating-channel heading. Every old proof stays active. The four new proved statements serve a single chain: boundary elimination, global curvature inversion, exact geometric identification and finite-flight inversion. They are not counted as four independent significance claims. |
| **R65-D1–D4** | We preserve the scoped correctness assessment, credit the existing general-period inverse, state all observation distinctions, and treat the adverse placement assessment as editorial rather than as a sign error or a no-go theorem. The exact local-branch qualification is now strengthened by a proved global uniqueness result; the local stability qualification is not. |

## 4. What is retained

All 818 files in the reviewed frozen source remain at their original paths. Of these, 811 are unchanged in bytes and mode. Seven framing/entry/bibliography files are revised; their byte-exact originals and the immutable frozen manifest are retained under `history/v65-review-baseline/`. No inherited proof module is replaced. All 131 inherited active input paths remain active; the new abstract, introductory synthesis and proof module give 134 distinct active inputs. Both principal and full entries include the complete new proof.

The existing periodic forward law, local analytic inverse, all alternating inverse and unregistered multichannel results, the corrected finite-experiment module, the position-pilot module and the companion are retained. Archiving an earlier abstract does not substitute for retaining a theorem: the corresponding theorem statements and proofs remain in the active manuscript.

## 5. Verification and limits

`tools/check_revision_v66.py` checks the complete inherited byte/mode inventory and active proof graph, exact rational Schur identities, signed blocks, the contraction iteration, finite Dirichlet chains, the two-site specialization and a positive nonimage control. Normal and optimized executions are compared. The unchanged native engine builds the three complete manuscripts from an immutable source snapshot with fresh auxiliaries and shell escape disabled. Actual build results, source identities and PDF checks are recorded in the delivery index and evidence, rather than predicted here.

These controls are distinct from the mathematical proof. They do not certify all inherited arguments, prove an infinite-dimensional theorem by experiment, or certify suitability for any journal. The revision continues to present the full result for the requested general-journal assessment, with the supplied observations and quantitative limitations stated as part of the mathematics.
