# Response to the controlling A2-DYN referee report

**Manuscript:** *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

**Document type:** author response accompanying a new native revision. This is not a new referee report, an independent specialist certification, or a statement of journal acceptance.

## Source identity, scope of the report, and scope of this response

The controlling report is the original `REFEREE_REPORT.md` at commit `f01482035a0b945b50f1f9c30f30ef35077558dc`, report blob `9c68b0e8b31cd196c732514a29ebd44d95964243`, in `reviews/a2-dyn-v115-double-clearance-external-top4-review-2026-10-15/`. It explicitly examined author commit `31792379408c5ace2c09284c2eb22d2331023433`, repository tree `008dba443ce2ca29b3e276b1bf05bcf7021011c1`, article tree `1cbc4d65c0b512292bd93535a2648ecdfc51415f`. Its substantive new-proof scope was native modules 270–276 relative to the inherited chain. Its comments do not constitute an examination of later modules 277–332, or of the present modules 333–335. The report describes itself as an author-requested AI-assisted assessment; we preserve that qualification.

This revision starts from the latest complete localized-clearance author manuscript, mathematical source commit `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761` and evidence-carrier commit `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd`, at `papers/A2-DYN-localized-clearance-records-author-revision`. The former has article tree `1fb3b20b29e3fe447bdae42f0faca0baf4f6b9cc`; the latter has article tree `7d1a65637fd0178727d574494bf2963172aa9881`. All native proof bodies 260–332 are retained byte for byte. The older native source, original reports, failed approaches, conditional statements and execution evidence remain traceable through the source manifest and history-preservation audit.

The response addresses each major request in §18, each proposed closing route in §20, and each minor/source request in §21 separately. “New” identifies a result proved in modules 333–335. “Inherited” identifies a retained author theorem with its actual proof and assumptions. “Open” identifies a mathematical conclusion not established here. None of these labels implies independent human reconstruction of a dynamical input.

The A2 geometry paper and any favorable assessment of it are separate objects. No such assessment is used as an A2-DYN review. A branch with a higher version number, a workflow-only artifact, a finite diagnostic or an incomplete source tree is not used to select the mathematical baseline.

## What this revision adds

### Quantitative reconstruction of the original section interface: module 333

Module 333, Section `sec:sm-section`, adds explicit constants and a precise norm qualification to the already proved section-multiplier interface. Lemma `lem:sm-grid` derives, for the actual defining polynomial of the physical moving section,
\[
 0<q'_R<3,\qquad |\theta'_R|<6,
 \qquad\text{moving side displacement in }(\alpha,\varphi)
       \le 11|R-S|.
\]
It gives a partition with at most 121 cells, an explicit lower transverse angle, a uniform nongrazing section cap, and a fixed common test-curve construction. Theorems `thm:sm-multipliers` and `thm:sm-moving` reconstruct the exact strong multiplier and weak parameter estimate under the stated Demers–Zhang norm hypotheses. Corollary `cor:sm-transfer` identifies the source-side occupation and separate terminal test with the unchanged physical record.

This is explicitly a quantitative proof-completeness addition. Historical module 77, `lem:v37-section-multiplier`, already proved the finite rectangular partition, transverse boundary control and entire occupation phase. Historical module 84, `thm:v40-polynomial-LY`, already proved the weak estimate in terms of the section-motion width, as well as the full occupation-torus argument at a fixed roof band. We do not claim to discover those results again. The fixed common test construction is not silently identified with different radius-dependent dynamical spaces, and invariance of the enlarged curve family remains a separate spectral requirement.

### Exact unsmoothed interval inversion: module 334

The historical inversion architecture is retained explicitly. Native 93 already gives exact singular-germ-subtracted labelwise inversion and a finite remainder certificate (`thm:v43-labelwise-inversion`, `cor:v43-finite-remainder-certificate`). Native 331 already gives exact finite-band likelihood reconstruction and actual-denominator certificates (`thm:av-likelihood`, `cor:av-exact-fourier`, `cor:av-denominator`). Neither the first exact inversion nor the first denominator certificate is claimed here. The additional formula below directly inverts the unchanged interval indicator with an absolute, label-summed tail and the specified smooth endpoint/phase observations.

The wider native-source novelty audit also identifies module 64's sharp full-law interval formula after its geometric residual extraction, module 66's label-dependent windows and arbitrary-selector positive likelihood, and module 67's absolute stationary flight-age inversion using interval amplitudes. `audit/EXACT_INTERVAL_NOVELTY_AUDIT.md` gives their exact objects and labels. The new result is the explicit direct consequence of the complete first-order BV budget for this original fixed-collision four-record law; it is not a new general Fourier inversion method, and its smooth observation class does not supersede the older Borel-selector result.

Theorem `thm:ui-inversion` proves an absolutely convergent joint Fourier formula for the **unchanged** exact-label event whose original roof lies in a specified union \(I\) of at most \(J\) bounded intervals. The extra decay comes from the exact interval transform, not from squaring a weak operator bound:
\[
 |\widehat{\mathbf1_I}(s)|\le\min\{|I|,2J/|s|\},
 \qquad
 |\mathcal F_{m,R}^{w,V}(\vartheta,s)|
          \le\min\{A_V,D_V/|s|\}.
\]
Here \(D_V\) is the actual inherited complete physical variation budget for the stated \(C^1\) endpoint and trajectory-phase tests. The original source is unweighted or has its original fixed guard \(W^\varepsilon\).

For \(d=|I|>0\) and sharp frequency cutoff \(S>0\), the full tail is
\[
 \left|\int_I f_{\mathbf j}-\mathfrak I_S(\mathbf j,I;V)\right|
 \le \frac{D_V}{\pi}\mathfrak t_J(d,S)
 \le\frac{2JD_V}{\pi S},
\]
where
\[
 \mathfrak t_J(d,S)=
 \begin{cases}
 d[1+\log(2J/(dS))],&dS\le2J,\\
 2J/S,&dS\ge2J.
 \end{cases}
\]
Corollary `cor:ui-all-labels` sums different original windows at every exact label using the already summed variation norm, without a number-of-labels factor. Corollary `cor:ui-normalization` states the cost \(2JD_Vm^2/(\pi dS)\) after the actual density normalization. The sharp truncation is not asserted positive.

Proposition `prop:ui-conditional` gives a finite denominator certificate for the actual event. If the calculated denominator \(D_S\) satisfies \(D_S>E_0\), then the true mass is positive and
\[
 \left|\frac Np-\frac{N_S}{D_S}\right|
       \le\frac{E_V+A_VE_0}{D_S}.
\]
The statement applies to precisely the displayed test class. It does not transfer the \(C^1\) variation bound to arbitrary additional Borel information.

Proposition `prop:ui-raw-bridge` first separates the complete local derivative charge, the arithmetic-reference modulus, the scalar frequency comparison and the explicit truncation term. The subsequent Lemma `lem:ui-reference-modulus` and Proposition `prop:ui-inherited-bridge` then use the **already proved** native 87 fixed-window theorem, `thm:v41-uniform-transition`, with its original finite-peak data. For each positive analysis width fixed before the collision limit, the scalar comparison and reference modulus tend to zero. They are not additional open premises on this route. The no-roof-resonance property is used only at unit peaks; moving nonunit peaks remain in the reference and their roof derivative is controlled by damping and compactness.

The resulting sufficient remaining physical condition is
\[
 \lim_{B\to\infty}\limsup_{m\to\infty}\Omega^p_{m,B}=0,
 \qquad
 \Omega^p_{m,B}=\sup_{R,n,k}m^2\operatorname*{ess\,sup}_{t\in\mathcal C(M)}
 |Dp_{n,R}(k,m,\cdot)|([t-h_B,t+h_B]),
\]
with every finite \(h_B>0\) fixed before \(m\to\infty\). Equation `eq:ui-local-charge-suffices` proves the implication at the original order of limits. This local physical charge is not proved to vanish and is not claimed necessary. A growing-band strong-operator theorem is an optional alternative route, not a missing premise of this scalar bridge. The analytic spike diagnostic explains why small interval mass, finite global BV norm and polynomial-band control alone do not imply raw essential-height convergence; it is not substituted for the physical billiard system.

### All-flight endpoint clearance kernels and positive-width critical coefficients: module 335

Lemma `lem:ce-first` adds the missing selected-length budget through the first actual image of a horizontal momentum source:
\[
 \sum_C\|\rho_C\|_\infty\le S_{\rm first},
 \qquad
 \sum_C\|\rho_C\|_\infty |C|
                \le M_{\rm first}\delta.
\]
It uses the exact first-image density from native 284, a uniform ratio inside each individual homogeneous piece, and the true first-hit map. The comparison makes no assertion across separate grazing strips and inserts no collision at a clearance foot.

Theorem `thm:ce-kernel` proves, for every physical flight \(0\le j<m\),
\[
 D_{m,R;j,\delta}(a,v)
 \le C_{\rm end}\{\delta+
             \theta_{\rm r}^{\max(j,m-1-j)}\}.
\]
It includes both endpoint flights. The reversed estimate is proved on the same actual orbit: \(j\) becomes \(m-1-j\), the endpoint momenta become \((-v,-a)\), and the determinant-one collision derivative preserves the inverse root weight. Taking the smaller of two valid estimates gives the exponent \(\max(j,m-1-j)\). No independence is introduced.

Theorem `thm:ce-critical` transfers this estimate to the complete one-copy leading critical coefficients on the specified physical-side sectors with positive visited incidences, including positive-width unvisited-clearance witnesses. For the original depth-weighted guard it yields
\[
 C_{\rm crit}\left\{
   \frac{4\varepsilon(B)}{1-q_0^{1/4}}
       +m\theta_{\rm r}^{(m-1)/2}\right\},
 \qquad q_0=47/53.
\]
This is a uniform small-source estimate in the endpoint-momentum kernel and the **unscaled leading critical-coefficient norm**. It does not contain an \(m^{-2}\) factor. It does not bound a collision-uniform nonleading coarea remainder or prove the remaining roofwise shortage zero. Native 322 `pc:fan` already proves the longer-side exponential bound at zero clearance and, in `pc:all-marks`, its complete all-flight sum tends to zero even after multiplication by \(m^2\), including shallow indices. That stronger zero-level result is inherited; the new critical conclusion is its explicitly width-sensitive positive-clearance extension.

## Fixed physical and probabilistic scope

All statements retain the triangular lattice \(\mathbb Z(1,0)+\mathbb Z(1/2,\sqrt3/2)\), the original circular radii
\[
 R\in[9/20,47/100],
\]
genuine first-hit collisions, specular reflection and unit physical speed. The collision probability is \(d\nu=d\alpha\,dp/(4\pi)\), and the entrance law is
\[
 d\nu_R^*=\mathbf1_{Y_R^*}\,d\nu/c_*,
 \qquad c_*=\frac{91}{10000\pi}.
\]
No selected positive source is renormalized.

At fixed true collision count \(m\), the original event records displacement \(k\), the exact number \(n\) of section visits at times \(0,\ldots,m-1\), and separate terminal membership at time \(m\). The joint Fourier ordering \((k_1,k_2,n,t)\) is bookkeeping for those same records. The original physical roof, return interpretation, lattice labels, guard factors and arithmetic classes are unchanged.

The new endpoint-kernel estimate permits original Borel restrictions by positive domination. The new tested Fourier and conditional estimates have the narrower, explicitly stated smooth endpoint/trajectory-phase observation class. These two observation scopes are not conflated.

The raw target remains the radius-uniform, exact-label, four-coordinate pointwise density and local inversion problem with its full finite-peak arithmetic reference. Complete physical sums and the required suprema are taken before collision \(\limsup\); every original outer geometric/comparison width is fixed at that stage; \(B\to\infty\) is last. The auxiliary frequency cutoff in an exact finite-count formula does not change that order or widen any microscopic conditioning event.

## Replies to the major requests in §18

### §18.1 — Complete clearance chart sum

**Request.** Control the full finite-type, fold, degenerate, critical, one-sided unvisited, section and pairing-seam contributions with collision-uniform constants in the original \(m^2L^\infty\) topology.

**Inherited results.** Native 274 retains its finite-type and integrated-fold theorems (`thm:cr-finite-type`, `thm:cr-fold`) with their chart hypotheses. Native 275 retains its local critical density (`thm:cr-critical-density`). Later native 310 already pays a normalized source inside its guarded critical-tube union (`thm:cv-positive-roof`, `cor:cv-ec-normalized`); native 311 already gives a full physical-roof estimate on its guard-margin class (`thm:at-height`). Those are completed results on their stated domains, not work repeated here.

Native 328, `thm:lc-selected-roof-height`, treats the full actual endpoint cap and a specified selected clearance flight with
\[
 \|\text{selected roof density}\|_\infty
 \le C(\delta^{1/4}+\theta_{\rm r}^j+
                     \theta_{\rm r}^{m-1-j}).
\]
Native 329, `thm:lc-deep-payment`, already converts this to an \(m^2\)-vanishing payment for all sufficiently deep witnesses. Its logarithmic endpoint layer and same-pool remainder are retained.

**New response.** Native 335 `thm:ce-kernel` now controls a selected positive-width clearance source at every index, including the first and last flight, in the complete endpoint-momentum kernel. Native 335 `thm:ce-critical` pays its complete leading physical-side critical coefficient with an explicit width-sensitive bound. These statements sum actual roots/germs with multiplicity one; they do not require a new count of symbolic words. Native 334 `thm:ui-inversion` provides exact interval inversion for the complete inherited physical densities, with all already included boundaries and labels.

**Disposition: partial progress; the requested final topology remains open.** The endpoint-kernel and critical-coefficient bounds are not roof \(m^2L^\infty\) bounds. We have not supplied a common collision-uniform estimate for all nonleading critical/fold remainders at the same roof, nor proved vanishing of the original remaining source. A separate shrinking chart radius at each count is not used to claim that conclusion.

### §18.2 — Single-mark and cross-flight clearance

**Request.** Pay the first-order one-witness source and handle witnesses across genuine flights at the required normalized target-roof scale; same-flight duplicate control is insufficient.

**Inherited results.** Native 276 remains an exact **same-flight ordered** two-mark theorem (`thm:dc-exact`, `thm:dc-factorial`, `cor:dc-schedule`). Its second-factorial and weak duplicate payment do not bound the full first-order witness source. Native 327 already supplies the physical clearance cover and length-sensitive transport (`lem:lc-cover`, `thm:lc-renewal`, `thm:lc-local-half`). Native 329 pays the union of deep selected flights by the pointwise indicator inequality, without independence.

**New response.** Native 335 retains the small source length through the first actual image rather than retaining only a uniform density-supremum budget. For \(j\ge1\), it uses native 327 with the exact count identity \(h=j-1\), \(n=m-j-1\), \(h+n+2=m\). For \(j=0\), it uses one first collision, \(m-2\) intervening collisions and one last collision; the last-collision momentum cancellation is applied once. Genuine reversal treats the opposite endpoint.

The resulting \(O(\delta)+O(\theta_{\rm r}^{\max(j,m-1-j)})\) kernel bound is first order in the actual witness width. Summing the selected coefficients for the original union is justified by positivity on each trajectory, even if several flights or several disks witness the event. The two-at-each-depth count gives the explicit geometric series in `eq:ce-guard-critical`. Neither an independence hypothesis nor a mixed factorial identity is inserted.

**Disposition: a new complete all-flight estimate in the stated kernel/coefficient norms; target-roof closure remains open.** This is not an exponential-moment or clearance-load theorem at \(m^{-2}\) roof height. The original cross-flight and endpoint source is not declared paid in that stronger topology.

### §18.3 — Critical and boundary budgets

**Request.** Sum actual critical coefficients and local errors; retain the physical-side pairing, unvisited, section, singular and critical traces.

**Inherited results.** Native 284 gives the physical endpoint kernel and exact first/last collision formulas. Native 285 gives complete critical sectors and the angular comparison (`thm:mc-critical-sectors`, `eq:mc-sector-comparison`). Native 322 `pc:representatives` supplies finite analytic physical-side sector representatives. Its `pc:fan` already bounds the zero-clearance fan by the longer-side exponential, and `pc:all-marks` pays the complete sum over all flight indices, including shallow ones, at \(m^2\) normalization. Native 323–325 and 330–332 retain the complete physical roof-variation, canonical boundary, exact-record and tested variation proof bodies.

**New response.** Native 335 `thm:ce-critical` treats positive-width witnesses at all flight indices. For a finite family of actual one-copy germs, a limiting witness of width at most \(\delta\) lies in the strict \(\delta+\eta\) physical source in a sufficiently small actual regular neighborhood. At fixed \(m,R,j\), the proof takes the physical-side angular limit, then \(\eta\downarrow0\), then exhausts finite germ families. The bound obtained is uniform in \(m,R,j\) and exact restrictions. This is not an assertion of a common neighborhood radius for every germ.

The coordinate kernel carries the single factor \(1/(4\pi c_*)\). The critical angular comparison supplies \(C_{\rm crit}=U_2C_{\rm end}/(2c_*)\); it does not condition a second time. A zero-clearance limiting witness is retained from its actual unvisited side, and a positive critical coefficient is not erased because a boundary is null in collision area. The new theorem assumes positive visited incidences at its limiting germs; its statement does not silently include visited-grazing sectors outside that hypothesis.

Native 334 starts from the complete label-summed BV theorem. Its all-label tail sums each component's derivative variation once, after exact torus extraction, and thus introduces no record-count or boundary-component factor.

**Disposition: new positive-width leading-coefficient tightness and exact inversion of inherited complete densities; the requested full normalized local-error budget remains open.** In particular,
\[
 m^2\,\frac{4\varepsilon(B)}{1-q_0^{1/4}}
\]
does not vanish with \(B\) fixed before \(m\). The nonleading local coarea remainder still requires its own uniform estimate. The new leading coefficient theorem is not used in its place.

### §18.4 — Low-incidence shallow source

**Request.** Control the true low-incidence-load positive source, including a shallow or incidence-only source that survives clearance estimates.

**Inherited results.** The original incidence-load bound and its valid consequences are retained. Native 329's normalized deep-clearance payment removes a genuine positive part of the source. Low load means **incidence load**; it does not imply absence of unvisited near misses.

**New response.** Native 335 supplies a positive-width clearance-kernel and critical-coefficient estimate even at shallow/end indices, where the direct two-tail expression from native 328 has a nondecaying term. The gain uses the longer actual propagation direction and the newly retained first-image length. It advances the clearance part of the endpoint problem, but in a different explicitly specified norm.

**Disposition: the remaining normalized low-incidence shallow source remains open.** An incidence-only positive source is not estimated by a clearance witness theorem. Neither a small number of indices nor the relative size of an endpoint layer implies small \(m^2\)-normalized height. No collision-dependent choice of the outer guard is used to make \(m^2\varepsilon(B)\) small.

### §18.5 — Capacity abundance

**Request.** Prove that the full original nongrazing comparison pool has sufficient roofwise capacity for the remaining positive source.

**Inherited result retained exactly.** Native 329, `thm:lc-same-pool`, keeps the original pool \(P^{\rm ng}\), coefficient \(K_B\), exact labels and roof. For the exact positive split \(U=U_{\rm deep}+U_{\rm end}\),
\[
 0\le (U-K_BP^{\rm ng})_+
       -(U_{\rm end}-K_BP^{\rm ng})_+
       \le U_{\rm deep}.
\]
The right side has the already proved normalized deep payment. This establishes equality of the two ordered shortage limits, not their value.

**New response and disposition: open.** Modules 333–335 do not change the pool or supply a new abundance theorem. In particular, the upper bound for a selected endpoint kernel is not a lower bound for comparison capacity. The historical weighted momentum capacity discharged in modules 241–243 is also a different quantity from this comparison pool. Equation `eq:lc-final-shortage` is retained as the exact unresolved target. No residual is renamed and declared zero.

### §18.6 — Inherited global inputs and independent reconstruction

**Request.** Reconstruct pressure, optical comparison, multiplicity, singular passages, spectral/arithmetic inversion and denominator consequences at their actual hypotheses and quantifiers.

**Source reconstruction.** `HISTORICAL_DEPENDENCY_STATUS.md` and the native-source audit replace metadata-only statements with exact proof-body locations and frozen identities. The audit verifies the full v108 source tree and reads the original modules underlying current `inputs.tex`: physical segment/coarea module 196, critical insertion modules 183/186/187, uniform pressure/capacity modules 241–243, paired average 245, positive-residence 253, and microscopic equivalence 255. The old separate (SC) premise is marked discharged by the actual later theorem; its proof's inherited joint spectral/geometric assumptions remain visible. Native 326 `ps:pressure` remains a complete later author pressure proof with explicit native hypotheses.

The historical fixed-band joint spectral and arithmetic arguments in modules 72, 77 and 84–87 are retained as actual theorems with their proof bodies. They are not labeled wholly absent because the final raw theorem is open. Their fixed-band constants are not extended to growing bands by assertion. A one-step weak \(C^1\to(C^1)^*\) bound from native 332 is not an iterable strong anisotropic estimate.

**New quantitative qualification.** Module 333 reconstructs the section interface with the actual moving root, explicit transverse geometry and a fixed common weak test construction. It checks the cited multiplier theorem's partition and exponent hypotheses. It states separately that full twisted collision realization, enlarged-cone invariance, compact embedding and map-perturbation hypotheses require their own arguments. It does not import a spectral corollary merely from a multiplier lemma.

**New inversion/conditioning interface.** Module 334 proves exact interval inversion and a finite certificate for a positive **actual** microscopic denominator. It does not prove that this certificate succeeds uniformly for every admissible asymptotic target. Zero arithmetic classes remain zero, and no conditional law is assigned there.

The existing native 87 fixed-window law is also used positively: `prop:ui-inherited-bridge` discharges the scalar interval comparison in the new raw bridge. `lem:ui-reference-modulus` retains moving nonunit peaks and proves the reference modulus tends to zero from their actual compact scalar data and no-roof-resonance property. The full normalized local derivative charge remains the sole new sufficient closing premise on that route. No new growing-band strong estimate is inferred.

**Disposition: author reconstruction and quantitative proof-completeness additions; no independent human specialist audit claimed.** Internal author derivations, exact algebra, code, PDF builds and CI do not satisfy the separate request for independent billiards/transfer-operator reconstruction. Full raw height closure, conditional microscopic normalization and the required inverse consequences remain open at their precise scope.

## Replies to the proposed closing routes in §20

These are alternative sufficient ways to close the governing theorem. They are not four independent mandatory proofs, and a partial estimate in another norm is not counted as completion of one.

### §20.1 — Complete normalized clearance theorem

**Inherited:** native 328's selected-flight roof estimate and native 329's complete normalized deep-clearance payment. **New:** native 335's all-flight endpoint kernel and positive-width critical-coefficient tightness, including both shallow endpoint sides. **Still required:** an \(m^{-2}\) roof-density estimate paying the remaining complete exact-label source and all required local remainders. This route is not completed.

### §20.2 — Target-roof clearance insertion/load theorem

**Inherited:** genuine selected-source transport and deep union control without independence. **New:** the first-image weighted-length estimate `eq:ce-first-budgets`, the longer-side complete root bound `eq:ce-kernel`, and the original all-flight guard coefficient bound `eq:ce-guard-critical`. **Still required:** a full original-roof and exact-record insertion theorem of sufficient normalized strength, including the unchanged mark torus, physical cuts and arithmetic classes. The endpoint-momentum estimate is not that missing theorem.

### §20.3 — Capacity-abundance theorem

**Inherited:** the exact original pool and the quantitative same-pool shortage comparison. **New:** no abundance assertion is made. **Still required:** a roofwise lower comparison capable of paying the remaining original source under the required suprema and ordered limits. This route remains open.

### §20.4 — Direct original shortage limit

**Inherited:** native 329's identity and paid deep component, and native 87's complete radius-uniform fixed-window arithmetic law. **New:** module 334 `prop:ui-raw-bridge` is evaluated by `prop:ui-inherited-bridge`: the scalar frequency comparison and reference modulus are paid using that retained law, the compact peak properties and the explicit interval tail. The only new sufficient physical premise on this route is the ordered vanishing of the complete normalized local derivative charge in `eq:ui-local-charge-suffices`. It is not substituted for the existing shortage or asserted necessary. **Still required:** a real mechanism proving the exact remaining shortage tends to zero, or proving this sufficient local-charge condition on the full original density. No equivalent reformulation or inherited fixed-window theorem is reported as new closure.

The report's additional request for independent specialist reconstruction remains separate. This author revision does not represent the complete result as journal-ready or claim that the report's recommendation has been reversed.

## Replies to the presentation and source-record requests in §21

### §21.1 — Paired response/copy refs at one SHA

The native manuscript, full new proofs, this response, dependency ledger and source manifest belong to one new revision source tree. Its exact source commit and later evidence-carrier identity are recorded separately by the publication manifest. The user's instruction confines this iteration to a new revision branch and preserves all historical author/review/copy branches. We therefore meet the single-source identity requirement by co-locating the reviewable manuscript and response; we do not claim to create additional paired aliases or move old refs. The report's preferred alias naming is not represented as an action already performed.

### §21.2 — Preparation-time versus post-push metadata

The source manifest and `PUBLICATION_STATUS.json` distinguish mathematical source, local preparation, completed source publication, later evidence carrier and actual workflow head. A preparation-time null is preserved only as historical metadata, not used as a current remote status. Current push and CI facts must be supported by actual receipts; no anticipated success is stated here. The frozen predecessor identities above are immutable facts independent of the new publication record.

### §21.3 — Provenance and novelty of successive modules

The manuscript preserves the distinctions requested:

- 270–273: the earlier one-mark flux, transverse geometry, transfer tests and exact-record disintegration;
- 274–275: the local clearance-to-roof/fold and critical-roof arguments;
- 276: the same-flight two-mark theorem;
- 277–332: later retained author proofs, including the already completed normalized deep-clearance payment;
- 333: explicit quantitative reconstruction and external-hypothesis qualification of an existing section interface;
- 334: exact unsmoothed interval inversion, explicit tail/denominator bounds and a conditional raw bridge;
- 335: selected first-image length, the all-flight endpoint kernel and positive-width critical-coefficient tightness.

Historical modules 77 and 84 are cited at the beginning of 333 so their multiplier and moving-width mechanisms cannot be mistaken for new discoveries. Native 93's exact germ-subtracted inversion and native 331's likelihood/denominator certificates are credited in 334. Native 87 supplies the fixed-window input actually used in the scalar bridge. Native 322's zero-clearance longer-side exponential and all-flight normalized fan payment are credited in 335; only the positive-width extension is new there.

### §21.4 — Explicit finite horizon and lattice counts

This request was already answered in retained native 287. Theorem `thm:eh-horizon` gives
\[
 \tau_+\le\sqrt{3847/124}<28/5,
\]
and Corollary `cor:eh-counts` gives \(N_f,N_*\le150\), \(N_{\rm pair}\le162\), \(J_f\le301\). The lower physical flight bound remains \(3/50\). The new constants use these actual enclosing bounds; they are not fitted from sampled flights. The finite candidate count is not a bound on long collision words or a replacement for one-copy pairing. These results are cited as inherited, not counted again as new.

### §21.5 — Ordered marks, unordered marks and witness indicators

The original conventions of 276 are unchanged. The selector in 335 is the event \(N_{\delta,R}(T_R^jx)\ge1\), not the mark count or its factorial moment. A root or critical germ with several witnesses is counted once in the relevant selected family. The union over flights is bounded by a sum of indicators solely by positivity, with no independence claim. The interval inversion in 334 extracts the original exact discrete coefficient.

### §21.6 — Total variation versus roof essential height

The distinction is stated in the new theorem bodies and this response. Native 335 proves an unscaled endpoint-kernel/coefficient estimate, not an \(m^2\) roof-height estimate. Native 334 proves exact interval inversion, not a raw pointwise LLT. Its normalized tail explicitly divides by the original interval length. Proposition `prop:ui-raw-bridge` retains the full local derivative charge; the spike diagnostic shows that a global BV or small-mass assertion cannot replace it. The already normalized deep payment of 329 remains a separate inherited theorem with its real decay rate.

### §21.7 — Reversal set-image convention

The equality
\[
 E_\delta^-=\mathcal I E_\delta^+=T_RE_\delta^+
\]
is retained as an equality of **set images on the regular collision space**, as in native 271 `eq:cf-reversal`. The new finite-record reversal in 335 separately sends the selected index to \(m-1-j\) and endpoint momenta to \((-v,-a)\). Original observations are transported by that real reversal or restored as positive restrictions; the conditioning section is not replaced.

### §21.8 — Scope of the local critical component

Native 275 `thm:cr-critical-density` remains a component theorem restricted to its coordinate ball. Later complete coefficient and cap theorems have their own proofs and domains. Native 335 does not upgrade the old local component into the entire roof density. Its finite-germ angular limit proves a bound on the complete leading coefficient sum, with no inferred uniform chart radius or estimate of the full nonleading density remainder.

### §21.9 — Actual exact-SHA CI and the boundary of computation

The predecessor source run `39712256295` at `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761` and carrier run `39714539054` at `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd` were separately reread through the GitHub API and both report completed/success. Their jobs and artifacts have distinct identities. The audit records artifact metadata and inspected job logs; an API digest alone is not described as independent reconstruction of artifact bytes.

The new revision's compilation, exact-arithmetic execution and any remote workflow are reported in its own validation/publication records, only after the actual operation. No result is transferred from a tested source SHA to a different untested SHA. Finite diagnostics verify identities, exponents and transcription in stated cases; they do not prove continuous geometry, all-word spectral estimates, a limiting shortage or expert acceptance.

## Earlier unresolved comments and the current dependency status

The complete v112 report at `d7fd0b24314d7341f9a611130bb650371d2d5ef2` and v73 rereview at `e31a74560d86082da1c2f2ef55c513343cfd41a0` remain preserved. `HISTORICAL_DEPENDENCY_STATUS.md` records their live mathematical content without treating every old conditional premise as permanently unresolved.

For v112 §§19.1–19.4, the unvisited-clearance source, shallow incidence-only source, actual pool abundance and physical boundary integration are distinguished. Later 327–329 paid the specified deep source; new 335 advances all-flight endpoint/critical control; the full normalized shortage and its incidence-only part are not thereby eliminated. The requested external specialist reconstruction in §19.5 remains absent. The v112 minor count restriction is an inherited consequence of its load bound, not a new theorem in this revision.

For the v73 rereview, collision-uniform pointwise concentration, full arithmetic, actual conditional denominators and the original clock remain decisive. New 334's exact interval formula does not replace the raw target by an averaged theorem. Conditional smooth tests are not total-variation convergence of a rescaled path to a Gaussian law, and the historical bounded-Lipschitz path conclusions keep their stated topology. Historical fixed-count tame geometry and common null-set conventions are retained with their actual proof sources.

The source audit also prevents an opposite error: the original fixed-band spectral and arithmetic theorems have actual proof bodies, and weighted momentum capacity (SC) was later discharged. We retain those results rather than repeatedly packaging their proof as a new contribution.

## Final mathematical status and the next necessary closure

The revision makes a new all-flight geometric estimate for the actual clearance-selected endpoint kernel, including the first physical image and both shallow sides; proves positive-width critical-coefficient tightness; supplies an exact unsmoothed microscopic-interval inverse with a full tail; and makes the inherited section multiplier's quantitative and external hypotheses explicit.

The unrestricted raw pointwise local limit theorem and four-coordinate local inversion are **not claimed completed**. The remaining requirements must be distinguished by route:

1. For original raw-height closure, prove a genuine physical estimate paying the retained same-roof endpoint/shallow shortage, including any incidence-only source, with the original pool and normalization; alternatively, prove the sufficient complete local-charge condition in `eq:ui-local-charge-suffices`. These are alternative routes, not a demand to prove both.
2. If the proof proceeds through critical/coarea geometry, control the full physical nonleading local remainder strongly enough to obtain that raw estimate. A leading critical coefficient bound alone is insufficient.
3. For conditional and inverse consequences, establish the required actual microscopic event-mass bound or successful certified denominator on the original admissible targets, with its exact observation class, relative error, physical clock and long-time Jacobian. Arithmetic zero classes cannot be normalized.
4. Independent specialist reconstruction remains a separate evidence qualification before asserting the requested complete journal-level result.

The scalar bridge already uses the native 87 fixed-window law to pay its comparison and reference terms. A direct strong spectral theorem on a growing roof band remains unproved, but is an optional alternative method rather than an independent missing condition for that bridge.

These are concrete proof obligations on the unchanged physical system. The new results do not lower the target, delete difficult collisions, change the clock or section, enlarge the conditioning window, or assert that the remaining positive mass disappears automatically.

