# Response to the revision-67 external report

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Revision:** 68, 10 October 2026.  
**Reviewed author source:** `add4d884ec0902fd5c70c68e1a82065442eab58f`.  
**Complete reviewed paper tree:** `266c432351a184e230b7e4df4f970c9d9f87208c`.  
**Controlling review:** `reviews/a2-dyn-v67-external-top4-review-2026-10-10/REFEREE_REPORT.md`, commit `d3321f707ba556bd25bb586178eed89038133cc8`, blob `b6e34eb10fa505a97a800a5ef7bc0e99cc222609`.

We thank the referee for distinguishing the fixed-stratum zero-width theorem from the complete positive-source endpoint. We retain the original problem and every inherited mathematical source. The response below identifies the new proved statements and the estimates which those statements do not supply. In particular, no small-mass assertion is relabelled as an essential-height theorem.

## 1. The new mathematical step

The previous source partition left every zero-tangent-fraction nonlinear sector in the positive complement. Such a sector has no nonzero physical zero-width atom, so even control of the old atomic tail cannot estimate its nonlinear height. Revision 68 treats this part directly.

Theorem `thm:v68-angular-germ-classification` proves that, at each fixed selected circular-billiard word, the exact unguarded angular fraction is either zero as a germ or has the form

\[
 \ell_{z,\lambda}(r)=\eta_{z,\lambda}r^{d_{z,\lambda}}+O_z(r^{d_{z,\lambda}+1}),
 \quad \eta_{z,\lambda}>0,\quad d_{z,\lambda}\in\mathbb N_0.
\]

The proof uses the analytic selected-contact graph and the specific analytic Morse coordinates already constructed in the paper. Dividing an active margin by the radius gives a function whose two angular zeros are simple. Their analytic root germs have a fixed cyclic order on a sufficiently small one-sided interval. Exact labels are assigned to the intervening arcs by the complete original visit rule. No generic transversality between different margins is assumed. Identical root germs require an analytic identity, not a finite list of vanishing jets.

For a nonzero germ, a recorded derivative remainder gives a relative error with respect to its first nonzero coefficient. If the actual first-clearance guard has positive center value `g_z`, its inherited Lipschitz bound gives a relative guard error as well. These two errors and the certified radius define a persistence number `mathfrak p`. On `mathfrak p <= K`, Theorem `thm:v68-relative-radial-profile` proves

\[
 e^{-K_\chi r}(1-Kr)\gamma_{z,\lambda}r^d
 \le b_{z,\lambda}^{\varepsilon,\mathrm{clr}}(t_z+r^2/2)
 \le e^{K_\chi r}(1+Kr)\gamma_{z,\lambda}r^d,
 \qquad \gamma=J_zg_z\eta.
\]

For a seam and order zero, `gamma = J_z theta`. For positive order, `gamma` is a radial coefficient, not a nonzero zero-width atom. At a non-seam center a positive guard value is sufficient; guard saturation is no longer required for this comparison.

The decisive comparison is with the **outer roof annulus** `H < u < 2H`. Every monomial `r^d`, including arbitrarily large finite orders, is no smaller there than on the inner collar. Proposition `prop:v68-annular-comparison` therefore has no constant depending on `d`. It compares the original nonlinear density with the actual positive source average, rather than replacing the physical mask by a tangent mask.

Applying the inherited collar theorem to that one common width gives Theorem `thm:v68-all-order-height`:

\[
 \limsup_m\sup_{R,\lambda}m^2\|b^{\mathrm p,K,H}_{m;\lambda,R}\|_\infty
 \le 6CH F_{\chi,K}(H),
 \qquad
 F_{\chi,K}(H)=e^{(2+\sqrt2)K_\chi\sqrt H}
       \frac{1+\sqrt2K\sqrt H}{1-2K\sqrt H}.
\]

Here `2H < h_chi` and `2K sqrt(H) < 1`, and all parameters are fixed before the collision limsup. At fixed `K,chi,epsilon`, the right side tends to zero with `H`. There is no cutoff on birth order, no word-count or label-count multiplier, and no interchange of an infinite dyadic sum with the collision limsup. This is an ordered essential-height theorem for original-source restrictions with zero tangent fraction as well as positive tangent fraction.

## 2. Response to the required changes in Section 24

### 24.1. Physical weighted tightness of the angular condition number

The old functional `E(K)` and its physical weights `J_z theta` are retained unchanged in module 145. Analytic finite-order classification does not prove its collision-limsup tightness. The new persistence number is not identified with the old angular condition number. Neither finite-count exhaustion nor a constant independent of a cutoff is used to infer uniformity in the cutoff. The old moment criterion remains explicitly conditional. Thus the requested unrestricted tail estimate is not marked proved.

The substantive advance here is different and necessary: source with zero tangent fraction is controlled on finite persistence strata even though it is invisible to `E(K)`. Its finite birth order is allowed to grow without limit. The proof pays for the genuine relative remainder and radius, not the birth order itself.

### 24.2. The positive complement

Theorem `thm:v68-all-order-height` removes the blanket exclusion of zero-tangent-fraction nonlinear sectors from the controlled family. It also includes non-seam critical centers whose actual center guard is positive. All of their finite birth orders are summed before the collision limit. The exact partition in `eq:v68-complete-source-partition` keeps everything else positive.

Specifically, failed incidence taper, selected grazing, noncritical components, uncovered physical states, large persistence numbers, source outside the certified germ disk, and outer chart annuli remain in the complement. A zero-center-value smooth guard may create an infinitely flat positive source and is not assigned an analytic birth order. An identically zero angular germ gives zero source only inside its certified zero disk; possible source elsewhere remains. No height estimate is inferred for these residual classes from their mass or from the new classification.

### 24.3. Complete first-incidence height

The revision reuses the incidence-normalized geometry only in its established scope. Module 131 gives finite-count inverse-incidence estimates with exponential count constants; module 140 supplies the selected-contact chart under a fixed taper. Neither is claimed to prove the complete ordered first-incidence estimate. The complete incidence term is displayed explicitly in `eq:v68-canonical-endpoint-budget`. Its status remains unproved, not replaced by a reconstruction band depending exponentially on collision count.

### 24.4. Complete clearance height

The new original-source restriction has the ordered height `6CH F`. The exact remaining budget is

\[
 \mathcal H(b^{\varepsilon,\mathrm{clr}})
 \le6CH F_{\chi,K}(H)+\mathcal H(r_{68}^{\varepsilon,\chi,K,H}).
\]

The transverse, finite-type, buffered-caustic, and earlier angular-stratum results remain compiled. Their finite-count or restricted hypotheses have not been silently upgraded. The full complementary height is still needed to turn this budget into a complete clearance theorem.

### 24.5. Unrestricted pointwise arithmetic theorem

The title, original section, exact return record and central-window pointwise target are unchanged. Equation `eq:v68-canonical-endpoint-budget` places the new height into the inherited positive raw-error identity:

\[
 \mathcal E_M\le C_MB^{-1/192}
 +\mathcal H(b^{\varepsilon(B),\mathrm{inc}})
 +6CH F_{\chi,K}(H)
 +\mathcal H(r_{68}^{\varepsilon(B),\chi,K,H}).
\]

This is a proved budget, not a claim that every right-hand term tends to zero. First fix `B` and its physical width, then admissible `chi,K,H`, then take the collision limsup. Subsequent outer choices may depend on `B`, never on `m`. The finite arithmetic transition kernel and all zero classes are retained. The unrestricted endpoint is not marked proved.

### 24.6. Unrestricted same-roof consequences

The inherited same-roof collision and actual-return bridge implications, forward essential-likelihood target and roof-conditioned path target are preserved with their full-source hypotheses. The new restricted height is not substituted for a two-sided pointwise law on the entire central window. No conditional law is assigned at a zero arithmetic denominator.

### 24.7. Independent specialist review

No independent human specialist review has been obtained in this revision. `SPECIALIST_AUDIT_MAP.md` identifies the new and inherited load-bearing checks. In particular, the analytic margin list, the root-order argument, the physical-side continuation, the original nonlinear density normalization, and the arbitrary-subfamily collar theorem need expert scrutiny. Finite fixtures and native compilation are not substitutes for that review or for continuum proofs.

### 24.8. Exact-SHA qualification on both refs

A new workflow targets both revision-68 refs and deliberately has no path filter. Each push is qualified on its actual SHA with read-only repository permission, an exact frozen revision-67 paper-tree check, and the controlling report-blob check. Both refs must have their own successful run before two-ref qualification is described as complete. The immutable workflow receipts, not this source file, record the actual run IDs, refs and SHAs. The preceding revision-67 run is not reused as revision-68 qualification.

### 24.9. Reduce the proof burden without deleting the mathematics

The active opening now gives the original problem and two leading theorems. The shortest new route is modules 146--148, with explicit references to inherited analytic geometry, the physical density profile and the finite-width collar theorem. The previous leading statements move verbatim to a compiled historical appendix; all 145 old core modules, seven old appendices, 197 old Python files, the bibliography, and all old mathematical labels remain. No other paper or earlier review is rewritten.

### 24.10. Generality after verification

We have not switched to a general singular-systems framework or introduced an unverified second realization. The analytic classification is proved for the original circular Lorentz source using its actual scalar tests. The elementary high-order local example illustrates why the annular constant should not depend on the birth order; it is explicitly not advertised as a Lorentz realization of every order. The same original unrestricted Lorentz endpoint remains the objective.

## 3. Technical comments in Section 25

The manuscript continues to distinguish the finite-width physical trace `Q`, the zero-width physical trace `B`, and the larger reversible trace. The new `C_H` is explicitly scale weighted and is not called a zero-width trace at positive birth order. The germ radius, inactive-sign radius, Morse radius, reconstruction band, collar width, taper, old angular cutoff and new persistence cutoff are kept distinct.

Every estimate specifies its finite-count or collision-limsup status and the order of limits. The density comparison uses common coarea representatives and an essential supremum. Critical centers contributing to a roof lie in the exact interval `[t-H,t]`, whose length contributes the factor `H`; the collar average has width `2H`, producing the final factor `6`. Coincident centers add positively. Exact labels are one-hot only after the entire original visit rule, with occupation through `m-1` and separate terminal membership at `m`, has been evaluated. The image mark `j+1` and normalization `c_*^{-1}` remain inherited without change.

All inherited proof-status booleans are preserved, including every false endpoint flag. New true flags describe only the stated analytic-germ, relative-radial and restricted all-order height theorems. The qualification packet includes deliberate negative controls for fixed-count exhaustion, finite-jet equality, zero-center flat guards, and mass-to-height substitution. These diagnostics test stated finite identities and invalid inferences; they are not a certification of the full billiard program.

## 4. Delivered result and remaining mathematical task

Revision 68 supplies a direct ordered nonlinear height theorem for all finite-order angular births on fixed persistence strata, including a previously uncontrolled zero-tangent source and positive-guard non-seam source. Its proof does not require a uniform birth-order bound or the full reversible trace. The complete physical angular tail, incidence height, and positive complementary clearance height remain separate mathematical tasks. Their presence in the final exact budget is explicit. No topic change, source deletion, or unsupported claim of the unrestricted theorem is used to answer the referee.
