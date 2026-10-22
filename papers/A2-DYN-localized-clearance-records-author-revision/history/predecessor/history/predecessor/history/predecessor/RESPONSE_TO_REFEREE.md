# RESPONSE TO REFEREE — A2-DYN author revision

## 1. Complete article, actual source succession, and review scope

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

**Current revision:** Marked boundary source, 19 October 2026. This is an author revision of the complete English native manuscript [main.tex](main.tex). The new proof bodies are [316](core/316_marked_clearance_momentum_and_trace.tex), [317](core/317_physical_boundary_flux_and_uniform_cancellation.tex), and [318](core/318_full_word_cross_curve_distortion.tex). All fifty-six complete inherited bodies 260–315 remain byte-identical and active. The preceding response, including all its mathematical arguments, is preserved at [history/full-physical-source-predecessor-files/RESPONSE_TO_REFEREE.md](history/full-physical-source-predecessor-files/RESPONSE_TO_REFEREE.md).

The complete scientific parent is **0933e9b44f5b0fd1d1a624d37ffd881d352496f8**, repository tree **dba7d9a6e14d2509291f03cbf269b4ceb78b9549**, article tree **ff4daf7f42d868bd9b41b0b9fe4033489f99bd21**, at `papers/A2-DYN-full-physical-source-author-revision`. Its 2,765 published files, all 66 active TeX inputs and all 56 numbered bodies were checked. A fresh isolated three-pass build produced its 174-page native article without changing any predecessor file. The fourth literal history anchor reconstructs this entire article tree, while retaining the three earlier immutable anchors. Buildability identifies a complete source; it does not certify a dynamical theorem.

The controlling report remains commit **f01482035a0b945b50f1f9c30f30ef35077558dc**, report blob **9c68b0e8b31cd196c732514a29ebd44d95964243**, SHA256 **4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06**. Its exact original body is retained at [history/reviews/v115-controlling-report.md](history/reviews/v115-controlling-report.md). It expressly examined author commit **31792379408c5ace2c09284c2eb22d2331023433**, repository tree **008dba443ce2ca29b3e276b1bf05bcf7021011c1**, and native modules **260–276**. It did not directly review 277–315 or the present 316–318. Its substantive unresolved requirements remain applicable. The report is an author-requested AI-assisted assessment; it is not represented as a journal decision or an independent human reconstruction.

The fresh exhausted census contains 1,293 repository branches and 429 A2-DYN branches. The author source catalog covers 130 distinct author heads, 118 article trees, 114 core trees and 367 numbered source variants. All existing branch identities are unchanged from the preceding final census. The 178 review branches resolve to **91 distinct actual report bodies**, including a newly recovered original v73 referee-copy report that differs from the later canonical v73 report. The original 90-report index is preserved, with a separate exact supplement and historical-objection crosswalk. This recovery does not change the controlling report. Favorable reviews of the separate A2 geometry paper remain outside the A2-DYN review record.

The corresponding source, review, publication and CI evidence is indexed in [BASELINE_AND_HISTORY_AUDIT.md](BASELINE_AND_HISTORY_AUDIT.md). Unsupported connector endpoints, unavailable historical objects, workflow-only sources and unfinished qualifications are recorded with those actual limitations. The new manuscript is not claimed complete merely because an unavailable historical wrapper advertised a higher number.

## 2. Unchanged observations and the proved increment

The physical system remains the unit-speed triangular circular Lorentz gas,
\[
 R\in[9/20,47/100],\qquad d\nu=\frac{d\alpha\,dp}{4\pi},\qquad
 d\nu_R^*=\frac{\mathbf1_{Y_R^*}}{c_*}\,d\nu,\qquad
 c_*=\frac{91}{10000\pi}.
\]
The original five section rectangles, occupation convention, terminal test, lattice basis, actual collisions and physical roof are unchanged in [model.tex](model.tex). Occupation counts indices 0 through \(m-1\); the terminal index \(m\) is tested separately. Every new source may retain the full exact event \(\Pi_{n,k,m,R}\) and a specified interval of the original roof \(L_{m,R}\), whose support is contained in \([m\tau_-,m\tau_+]\). No probability is conditioned again on a clearance mark, an endpoint cap or a selected critical neighborhood.

| New result | Native locator | Exact scope |
|---|---|---|
| Both-direction momentum kernel of a clearance source | 316, **thm:nm-kernel**, **eq:nm-roots** | All actual positive collision counts from the marked foot; all regular physical words; uniform radius and positive clearance; complete root sums at every regular value. |
| Joint mark/incidence domination and singular moments | 316, **cor:nm-joint**, **cor:nm-moments** | The same physical marked counting measure, arbitrary collision index, exact labels and roof tests; unchanged interior \(I_m\), moments \(1\le\gamma<2\). |
| Exact one-sided finite-record trace | 316, **thm:nm-trace** | Original section and roof-interval conventions, including equalities at limiting endpoints; the tangency mark is not counted as a collision at the marked foot, and later actual hits of that disk remain ordinary collisions. |
| Physical boundary density and two-half optical determinant | 317, **thm:bf-flux**, **thm:bf-foot-determinant**, **cor:bf-wronskian** | Exact \(R\), \(c_*\), two-sign and incident-side factors; true physical normal speed and signed endpoint cancellation. |
| Uniform cancellation in a common formal gradient disk | 317, **lem:zf-formal**, **thm:zf-flux** | All actual pieces covered by a true critical zero-offset configuration, including arbitrarily short or disconnected pieces; no positive momentum cutoff or collision-word factor. |
| Radius-uniform comparison across real word components | 318, **thm:xd-cross-distortion**, **cor:xd-normalized-cocycles** | Any two real realizations of one lifted word and any two cone directions, with precisely stated homogeneity indices and exact endpoint incidence factors. |

Modules 314–315 already prove full-source weak roof bounds, integrability of the actual mixed singular multiplier and normalized deep-source estimates in their displayed norms. Those are inherited results here. The new boundary arguments concern a different positive measure and do not reuse volume integrability as a trace theorem.

The complete raw pointwise local limit and four-coordinate inversion remain unproved. This statement concerns their actual current proof status; their original assertions, microscopic windows, normalization and order of limits remain in the manuscript.

## 3. Responses to the six mathematical requirements in Section 18

### 18.1. The global clearance-to-roof sum

**Response and retained results.** The original local clearance-to-endpoint and roof/Gauss determinants, the full Hessian chain rule, finite-type and fold estimates, and the critical coarea statements of 274–275 remain unchanged. The complete fixed-margin atlas in 311 and full positive-margin exhaustion in 314 are inherited, as are 315's complete volume and regular-interior variation budgets. These conclusions are not recast as newly supplied hypotheses.

**New source mechanism.** Module 316 starts from the exact angular source of 279. Its first true collision has
\[
 \frac{dp_1}{d\vartheta}=-(\kappa a+c),\qquad
 a\ge a_\circ=\frac{\sqrt{1827}}{200}.
\]
For later collisions the proof propagates the exact first-image density through \(l-2\) actual steps, and uses the final physical collision to perform momentum coarea. Its terminal incidence cancels before taking a bound. With the existing physical growth constant, the resulting two-sign kernel is
\[
 H_{\rm nm}=\max\left\{\frac{2M_*}{k_-a_\circ},
                         \frac{A_*C_gJ_f}{k_-\tau_-}\right\}.
\]
No additional collision or terminal homogeneous-strip sum is introduced. The proof sums the true labelled source before taking the radius and time-count bounds. It covers angular-almost every source point and separately extends the complete positive inverse-root bound to every regular root value.

**New boundary conversion.** The source at zero clearance is not assigned zero merely because its underlying collision-area set is null. Theorem **thm:nm-trace** constructs the actual one-sided finite record. The original roof/Gauss boundary coefficient then has the exact conversion
\[
 f^\varepsilon|\partial_\vartheta\theta|\,d\vartheta
 =\frac{W^\varepsilon}{4\pi Rc_*}
          |\partial_tu|_\theta\,d\vartheta,
 \qquad f^\varepsilon=\frac{\omega W^\varepsilon}{4\pi c_*\chi}.
\]
This identity retains the physical normal speed and the complete positive marked multiplicity. Section sides have the corresponding collision-coordinate formula with prefactor \(1/(4\pi c_*)\). The distinction between these two densities is explicitly proved.

**What is now closed and what remains.** The actual angular source, its finite-record trace and the complete marked boundary conversion are established at their stated scopes. The covered critical boundary class receives the uniform cancellation described under 18.3. The unrestricted offset term, original section/pairing boundary sum and final \(m^2L^\infty\) source estimate are not consequences of these results alone. The response does not promote an angular kernel into an original-roof density or remove a higher-degeneracy component by a volume-null argument.

### 18.2. First-order marks across physical flights

The one-copy flux of 270, same-flight ordered factorial law of 276, genuine cross-flight Jacobi/coarea of 277 and completed angular-source growth of 279–283 remain at their established scopes. In particular first moments, second factorial moments and witness indicators still have different meanings.

For every Borel selector \(0\le h\le1\), the new joint estimate in **cor:nm-joint** applies to any original collision index \(i\), not only an endpoint or a neighboring collision:
\[
 \int h\mathbf1_\Pi N_E(T_R^jx)\mathbf1_{\{p_i\in I\}}\,d\nu_R^*
 \le\frac{H_{\rm nm}}{4\pi Rc_*}|E|\,|I|.
\]
If \(i\le j\), the backward kernel has exactly \(j-i+1\) true collisions; if \(i\ge j+1\), the forward kernel has \(i-j\). This includes \(j=0\), \(j=m-1\), \(i=0\) and \(i=m\). The original time-reversal selector is carried through the bijection rather than replaced by a reversed section. The two events in this inequality concern the same trajectory and are never assigned an independent law.

For the unchanged load
\[
 I_m=1+\sum_{i=1}^{m-1}\frac{q_0^{\min(i,m-i)}}{c_i},\qquad q_0=47/53,
\]
weighted convexity and the angular momentum density prove, for \(1\le\gamma<2\),
\[
 \int h\mathbf1_\Pi N_\delta(T_R^jx)I_m^\gamma\,d\nu_R^*
 \le\frac{\delta W_0^{\gamma-1}B_\gamma}{4\pi Rc_*},
\]
where \(W_0=1+2/(1-q_0)\), \(B_\gamma=4\pi+2H_{\rm nm}J_\gamma/(1-q_0)\), and \(J_\gamma=\int_{-1}^1(1-v^2)^{-\gamma/2}\,dv<\infty\). An arbitrary nonnegative depth sum is paid by the corresponding sum of its actual widths. The intersection with \(c_i<\eta\) has the additional exact momentum-length payment bounded by \(2\eta^2\).

These results give first-order marked-source control with the actual singular incidence insertion, uniformly at shallow as well as deep marked flights. The roof interval remains inside the measure. They do not produce a factor equal to its length, and hence do not establish the pointwise roof bridge of 273 or the report's full target-roof exponential-moment theorem. The original single-clearance source remains first order. No duplicate estimate is used to turn it into a second-order error.

### 18.3. Critical and singular endpoint payment

The reversing-orbit interpretation, return-stability coefficient, occupation identity and critical-fan coarea in 275 and 285 are retained. The new result is a direct bound on the true positive boundary density, using a common analytic domain rather than a word-dependent shrinking physical interval.

First, the two half-ray optical products in **thm:bf-foot-determinant** give positive endpoint derivatives \(A_-^p,A_+^p\) and ratios \(h_-,h_+\) with
\[
 \frac1{\tau_++R_+}\le h_\pm\le\frac1{a_\circ},\qquad
 |\det D_{(\vartheta,u)}(p_0,p_m)|
       =A_-^pA_+^p(h_-+h_+).
\]
Time reversal fixes the two clearance-column signs; the positive sum cannot cancel. The original endpoint kernel weight is exactly
\[
 u_x=\frac1{R A_-^pA_+^p(h_-+h_+)}.
\]
The signed Wronskian in **cor:bf-wronskian** preserves the difference of the two endpoint contributions before bounding it. No condition number of a long optical product replaces this exact identity.

Second, **lem:zf-formal** constructs one common formal inverse-gradient disk from the already proved analytic reflection domain of 292. Cauchy's estimate is applied to the bounded endpoint gradient \(R(-p_0,p_m)\), not to the total roof, which grows with \(m\). For a designated nonincident disk at flight \(j\), the signed clearance function in these coordinates satisfies
\[
 \|D_g^2\mathcal B(g)\|\le K_{B,g}(47/50)^{d'_j}.
\]
The proof includes both terms of the second-order chain rule through the inverse gradient. Its constants are explicit in **eq:zf-constants** and **eq:zf-final-constant**. The uniform domain also admits closed physical reference configurations with limiting interior grazing. It is a formal domain; physical admissibility is required independently at every source point being integrated.

For a true critical zero-offset configuration, \(\mathcal B(0)=0\). At an actual boundary point \(\mathcal B(g)=0\) as well. Therefore
\[
 D_g\mathcal B(g)\cdot g
       =\int_0^1sD_g^2\mathcal B(sg)[g,g]\,ds,
\qquad
 \partial_tu|_\theta
       =\frac{D_g\mathcal B(g)\cdot g}{g^{\mathsf T}G^{-1}g}.
\]
The numerator and denominator both contain a quadratic gradient factor. Their cancellation gives a true normal-speed bound with no \(1/|g|\) loss. Every actual piece represented by this designated inverse is included, even if its physical domain is very short or disconnected. Intermediate points of the formal segment are not treated as trajectories.

Finally **thm:zf-flux** integrates this uniform pointwise bound over the complete two-sign angular source of mass \(4\pi\). Unique physical records and a disjoint Borel chart assignment give
\[
 \mathfrak B^{\rm crit}_{j,u_0}\le C_{\rm zf}(47/50)^{d'_j},
 \qquad
 \sum_{j:d'_j\ge D}\mathfrak B^{\rm crit}_{j,u_j}
       \le\frac{2C_{\rm zf}}{1-47/50}(47/50)^D.
\]
This is a complete sum on the stated geometric class, not a bound per word multiplied by an unproved word count. At \(D=\lceil\vartheta_*m\rceil\), fixed \(0<\vartheta_*<1/2\), the positive charge still vanishes after multiplication by \(m^2\). The actual zero-clearance physical side is \(u>0\); a positive level is treated on one specified incident side, with any second side charged separately.

The theorem concerns regular boundary points with arbitrarily small positive \(|g|\). The incoming critical fan at \(g=0\) remains the distinct original source. If \(\mathcal B(0)=a_w\ne0\), the exact numerator is instead
\[
 -a_w+\int_0^1sD_g^2\mathcal B(sg)[g,g]\,ds.
\]
This physical/formal-word offset is retained. A complete weighted sum of this offset term, uncovered critical pieces and the original section and pairing endpoints remains necessary. The truncated estimate **thm:bf-truncated** is explicitly limited to its noncritical region and cannot pay that remainder by itself. Neither the smallness of \(a_w\) nor a separate finite local coefficient proves uniform disappearance after the ordered collision limit.

### 18.4. Shallow sources with small incidence load

The original high-load concentration and positive low-load reduction in 267–269 remain unchanged. The low-load class still contains a clearance-only witness with no incidence witness, as well as an incidence-only source. The new joint clearance/incidence estimate and moment bound control real shallow marked sources, but they do not imply that every low-load source is rare on its microscopic return event.

The original physical comparison factor \(I_m\), full roof and section membership are retained throughout. In particular \(I_m\) has not been replaced by an endpoint-augmented quantity or by a fixed-margin bound. Full volume uniform integrability of 315 is inherited. An \(m^{-2}\) same-roof scarcity estimate or a valid capacity payment for the remaining shallow positive source is still required. No new condition has been inserted into the original event to exclude this class.

### 18.5. Capacity of the actual comparison pool

The revision does not infer abundance from local invertibility or from a nonempty nongrazing pool. The fixed-margin physical tubes, their overlap bound and the original capacity construction remain available, with all their physical clock and label restrictions.

Module 318 completes a concrete geometric comparison needed by a proposed full-cell route. Two arbitrary actual realizations of the same lifted word are compared to one common disk-product minimum. The inherited anchor theorem applies to that same minimum from both real references. It gives exponentially small phase differences toward the middle even if the real word domain is disconnected. The proof does not interpolate between the two physical records.

On matching interior \(q=2\) homogeneity strips, a one-third Hölder bound for \(\log c_i\) makes their entire incidence-log difference summable. The exact physical slope map has contraction at most \(47/48\), so arbitrary initial cone directions also have a summable discrepancy. Telescoping the Euclidean length factors then yields the uniform cross-curve Jacobian comparison of **thm:xd-cross-distortion**. A terminal incidence is explicitly retained unless its actual strip is also matched.

This theorem removes the previously conditional transverse distortion step. It does not prove that all physical cell suprema can be assigned to a sufficiently large collection of comparison curves, or that very short cells have enough original same-roof capacity. The full geometric cell/refinement and abundance assertion remains open. No small-area cell is assumed paid by volume integrability.

### 18.6. Global analytic, optical, and arithmetic dependencies

The physical optical comparison itself was already proved in 313 with the explicit factor 30000. Module 318 adds the complete same-word comparisons
\[
 \frac{j_m(x)}{c_0(x)}\asymp_{C_\times}
 \frac{j_m(\widehat x)}{c_0(\widehat x)},\qquad
 \frac{\omega(x)}{c_0(x)c_m(x)}
       \asymp_{30000^2C_\times}
 \frac{\omega(\widehat x)}{c_0(\widehat x)c_m(\widehat x)}.
\]
The squared optical constant is used once for a comparison of two points, not once per collision. Tangent norms are the actual \((s,\varphi)\) Euclidean norms, with \(s=R\alpha\); no probability or radius normalization is hidden in them. Reflection of artificial strip boundaries is treated using the closure-valid incidence estimate, without changing the original partition convention.

The complete physical word-pressure sum is still not obtained from this pairwise comparison. Nor does the finite-curve growth theorem establish all hypotheses of a radius-uniform twisted transfer-operator theorem. The current [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) records the actual curve class, partition, function-space, pressure, minimality and arithmetic scopes of the retained external results. No tested or averaged flow limit is substituted for the raw four-record density. All spectral peaks, exact lattice labels, arithmetic zero classes, original return denominator and long-time inverse Jacobian remain in the retained manuscript and dependency ledger. A full independent specialist reconstruction of that analytic chain has not occurred in this author revision.

## 4. The four requested closing routes in Section 20

| Request | Current mathematical response | Remaining smallest interface on this route |
|---|---|---|
| 20.1: Uniform normalized global clearance density | 316 supplies the exact all-time angular/marked kernels and finite-record trace; 317 supplies the true positive boundary conversion and a common-domain zero-offset cancellation. The 311–315 full-source roof estimates are inherited. | The entire unrestricted marked and pairing sum must still be paid in the original \(m^2L^\infty\) topology; covered-boundary total charge is not that density theorem. |
| 20.2: Insertion on the original target roof | The complete joint clearance/any-collision kernel and unchanged \(I_m^\gamma\) insertion are proved without independence or word-count multiplication. | Obtain the requisite original-roof density or marked operator bound with all exact labels and prescribed microscopic intervals; retaining an interval in a selector alone does not supply its length factor. |
| 20.3: Abundance at the same roof and labels | 318 closes the native transverse distortion comparison; inherited physical tubes and optical constants remain available. | Prove actual full-cell assignment/refinement and enough nongrazing comparison capacity, including arbitrarily short and disconnected cells. |
| 20.4: Direct ordered shortage payment | The new exact boundary identity identifies the nonzero-offset term, while the original positive-source expression is unchanged. | Prove that original positive part vanishes after the full physical sum, radius/label supremum, roof essential supremum and collision limsup, with \(B\to\infty\) last. |

These are responses to all four proposed routes, not claims that the report's requested endpoint theorem has been completed. The new mechanisms have full proofs on their stated physical classes; their unclosed interfaces remain explicit mathematical obligations rather than unnamed residuals.

## 5. Responses to all nine presentation requests in Section 21

1. **21.1 — Paired source, copy and response references.** The dedicated new revision, referee-copy and referee-response refs are recorded together in [PUBLICATION_STATUS.json](PUBLICATION_STATUS.json). Actual remote verification requires that they resolve to the same final commit; the old author and review refs are preserved. No new referee recommendation is issued.

2. **21.2 — Preparation versus actual publication.** Fixed parent/report identities are in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json). Current publication facts are maintained separately after actual commits and execution. The tested CI commit, the source carrier and the later evidence carrier have distinct roles. A post-CI evidence commit is not represented as a separately tested checkout merely because its mathematical source is identical.

3. **21.3 — Attribution of earlier modules.** The whole 260–315 chain is retained. The provenance of 270–273, 274–275 and 276 remains distinct. The completed growth theorem, optical theorem and full-source 314–315 increment are explicitly inherited. Only 316–318 are new proof bodies in this revision; an unavailable historical pressure wrapper is not counted as one of them.

4. **21.4 — Auditable horizon and lattice geometry.** Module 287 retains the uniform original-flight proof, \(\tau_+\le\sqrt{3847/124}<28/5\), and its finite lattice budgets; in particular **cor:eh-counts** proves \(N_{\rm pair}\le162\). The new foot standoff is the already proved \(\sqrt{1827}/200\), not a sampled distance. The new constants \(H_{\rm nm}\), \(K_{B,g}\), \(C_{\rm zf}\) and \(C_\times\) are explicit formulas in those fixed physical bounds.

5. **21.5 — Mark multiplicity conventions.** The ordered two-mark law and its factorial diagonal subtraction remain in 276. The new \(N_E\) counts distinct unvisited disks on one actual flight. It neither increments collision count nor replaces a witness indicator. Every physical marked copy is transported once; coincident representations are disjointized before any bound.

6. **21.6 — Probability topology.** The new angular kernels, collision-volume moments, boundary charges and their physical-roof pushforwards have different explicitly stated measures. Total variation, weak \(L^p\), finite strong \(L^p\) and raw roof essential height are not interchanged. The actual \(m^2\)-normalized deep-boundary statement is limited to its positive-charge topology.

7. **21.7 — Reversal conventions.** The retained set-image convention in 275 is unchanged. Module 316 additionally writes the exact line-parameter reversal \((\vartheta,\sigma,u)\mapsto(\vartheta+\pi,-\sigma,u)\) and momentum reversal \(p\mapsto-p\). The original section indicator is transported, not replaced by a different event. Module 317 checks the signs of both transverse columns explicitly.

8. **21.8 — Critical component versus complete density.** The original coordinate-ball critical coarea and fan remain local components at their stated scopes. The common formal chart theorem requires agreement of the entire designated physical contact record with its inverse, not merely proximity of endpoint angles. It excludes the \(g=0\) incoming fan from the regular boundary integration and does not assert coverage of all small-gradient branches or all nonzero offsets.

9. **21.9 — Execution evidence.** [VALIDATION.md](VALIDATION.md) and the current publication packet distinguish actual local runs, final mathematical-source identity, native compilation, historical rebuilds and the exact remote workflow checkout. Finite symbolic and ray computations supplement the mathematical proof. CI success certifies the described source and executions, not a continuum theorem or a journal qualification.

## 6. Crosswalk of the report's earlier technical sections and recovered history

The discussions in report Sections 6–17 are all retained in this response's scope. Sections 6–8 map to the unchanged 270–273 flux/disintegration and new 316; Sections 9–10 to unchanged 274 and new 317's exact conversion; Sections 11–13 to unchanged 275 and 285–286, inherited 290–295, and new 317's specified critical-boundary mechanism; Sections 14–16 to unchanged 276 and later cross-flight 277–283; Section 17's first-order, shallow and capacity distinctions remain explicit under responses 18.2, 18.4 and 18.5. No previously proved finite determinant or factorial estimate is weakened or discarded.

The recovered original v73 report at **5e9877a6677300615f909b47661775451f543817** directly concerns author **39575228f055862103edbebdd984bd6764fa0ad9** and the then complete 1–163 source. Its literal root typo is preserved in the original text and corrected only in the applicability record using the actual commit object. Its four remaining themes—quantitative paired-flux decay, a literal scalar endpoint, exact positive-class normalization and limit order, and collision-uniform constants—are crosswalked in the historical supplement. Fixed-count finiteness and later completed optical and volume results are inherited; those old objections are not all mechanically declared open or all mechanically declared resolved.

## 7. Exact continuing theorem obligation

The manuscript still asks for
\[
 \lim_{B\to\infty}\limsup_{m\to\infty}\sup_{R,n,k}
 m^2\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
 \bigl(\mathsf U^{\rm low}_{B,m}(t)-K_BP^{\rm ng}_{r_B,m}(t)\bigr)_+=0.
\]
Every outer width is fixed before the collision limsup. The full physical positive sum precedes the suprema. The same event, original clock, collision and lattice labels, arithmetic reference, return denominator and four-coordinate inverse target are retained. The new proofs do not change any of those quantifiers. [PROOF_LEDGER.md](PROOF_LEDGER.md) identifies the exact dependencies and the remaining geometric and analytic closure conditions. This revision supplies complete new author proof bodies and current execution/provenance evidence. The recovery audit identifies the interrupted candidate records that were not recoverable; missing original receipts are not fabricated. The final theorem remains open at the scope stated above.
