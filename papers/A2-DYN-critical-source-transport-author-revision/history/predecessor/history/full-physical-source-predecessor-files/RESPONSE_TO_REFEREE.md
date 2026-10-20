# RESPONSE TO REFEREE — A2-DYN author revision

## 1. Article, source identity, and scope of this response

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

**Current author revision:** Full physical source, 19 October 2026. The complete English native entry point is [main.tex](main.tex). This revision adds [module 314](core/314_full_physical_source_roof_regularity.tex) and [module 315](core/315_full_physical_singular_multiplier.tex). All fifty-four inherited native proof bodies 260–313, the model and analytic interfaces, and the complete historical source assembly are retained. The immediate predecessor's response is preserved without alteration at [history/physical-tube-predecessor-files/RESPONSE_TO_REFEREE.md](history/physical-tube-predecessor-files/RESPONSE_TO_REFEREE.md).

The actual complete source parent is commit **fdf2603c8bf422314f199fa431086485a0d1ebb5**, repository tree **d90e88848644a25b2d9f2e3a28383f4908d2a646**, article tree **f5c90ecd279dd116330c5d90fa31cae2b0d6f61e**, at papers/A2-DYN-physical-tube-source-height-author-revision. Its 2,088 actual files, native inputs, and historical anchors were checked, and the selected native article was rebuilt in three actual compiler passes to 164 pages. This identifies the complete readable scientific baseline independently of its branch name. The source and build evidence is recorded in [BASELINE_AND_HISTORY_AUDIT.md](BASELINE_AND_HISTORY_AUDIT.md) and its linked fresh census and rebuild receipt.

The controlling report is the complete report at commit **f01482035a0b945b50f1f9c30f30ef35077558dc**, Git blob **9c68b0e8b31cd196c732514a29ebd44d95964243**, SHA-256 **4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06**, originally at reviews/a2-dyn-v115-double-clearance-external-top4-review-2026-10-15/REFEREE_REPORT.md. The unchanged local body is [history/reviews/v115-controlling-report.md](history/reviews/v115-controlling-report.md). It expressly examined author commit **31792379408c5ace2c09284c2eb22d2331023433**, repository tree **008dba443ce2ca29b3e276b1bf05bcf7021011c1**, through modules **260–276**. It did not review 277–313 or the present 314–315.

The fresh census exhausts 1,290 repository refs, including 426 A2-DYN refs; the author-related sources identify 129 distinct author heads, and the merged native catalog records 365 numbered variants. Ninety retrieved historical A2-DYN report bodies and their applicability records remain available. The census found no newly controlling substantive report. The favorable assessment of the separate A2 geometry article is excluded. Workflow-only exports, absent higher-numbered source, incomplete jobs, skipped qualification steps, and auxiliary model calculations retain those limitations in the source record.

This is an **author response**, not another referee report or a new recommendation. The controlling report was an author-requested, AI-assisted assessment; it is not represented as a commissioned journal decision or an independent human reconstruction of the entire billiards and transfer-operator chain.

**Scientific status.** The new proofs establish full-source roof regularity, uniform integrability of the actual mixed singular multiplier, and complete normalized deep-source bulk and regular-interior variation budgets. The original raw pointwise local limit theorem and four-coordinate local inversion remain the scientific objective. Their complete shallow positive-source, paired-endpoint, unrestricted pressure, and final analytic closure are not claimed proved. In particular no additional pressure theorem numbered 316 is invoked or claimed.

## 2. Unchanged physical conventions and the new results

The system remains the original unit-speed triangular Lorentz gas with
\[
 R\in[9/20,47/100],\qquad
 d\nu=\frac{d\alpha\,dp}{4\pi},\qquad
 d\nu_R^*=\frac{\mathbf1_{Y_R^*}}{c_*}\,d\nu,\qquad
 c_*=\frac{91}{10000\pi}.
\]
All new pushforwards use the complete physical roof \(L_{m,R}\), including both actual end portions, on its original support \([m\tau_-,m\tau_+]\). The original return count, displacement in the original lattice basis, collision count, section events, terminal tests, roof intervals, and microscopic conditioning are retained.

For statements about roof densities, \(\mathcal C_{m,R}\) denotes regular physical records with \(|p_0|,|p_m|\le5/6\). The entire original exact event lies in this endpoint cap. No probability is renormalized on the cap. Given any Borel source \(E\) and Borel \(0\le H\le1\), the new measures are
\[
 \mu_{E,H}=(L_{m,R})_*
   (\mathbf1_E\mathbf1_{\mathcal C_{m,R}}H\,\nu_R^*),\qquad
 \mu^I_{E,H}=(L_{m,R})_*
   (I_m\mathbf1_E\mathbf1_{\mathcal C_{m,R}}H\,\nu_R^*).
\]
Taking \(H=\mathbf1_{\Pi_{n,k,m,R}}h\) retains all original exact labels and every bounded selector. Taking \(H=1\) is an upper bound on the source, not a new conditioning event. The actual physical factors are
\[
 q_0=\frac{47}{53},\qquad
 I_m=1+\sum_{i=1}^{m-1}\frac{q_0^{d_i}}{c_i},\qquad
 Z_m=\frac{I_m}{|\nabla_qF|}
     =\frac{I_m}{R|(p_0,p_m)|}.
\]
The new phase-space theorem for \(Z_m\) itself holds on the full regular collision space without this endpoint cap; the cap enters the subsequent roof atlas only.

The proved increment is summarized here; the detailed responses below explain its mechanism and limits.

| New statement | Exact source locator | Proved scope |
| --- | --- | --- |
| Uniform physical margin tails and full roof regularity | 314, **lem:fr-margin-tail**, **lem:fr-exhaustion**, **thm:fr-full-source** | All positive incidence and clearance margins; every actual word; full roof densities in weak \(L^{3/2}\), and actual \(I_m\)-weighted densities in weak \(L^{6/5}\). |
| Complete normalized deep-source bounds | 314, **thm:fr-deep-source**, **eq:fr-deep-norms**, **eq:fr-deep-rates** | The exact inherited observable source \(\mathcal E^{\rm obs}_{D_m,R,m}\), with no remaining guard indicator, has exponentially decaying mass and the stated weak and strong roof norms; each remains vanishing after multiplication by \(m^2\). |
| Full actual singular multiplier | 315, **lem:sm-intersection**, **lem:sm-mixed-tail**, **thm:sm-full-multiplier** | A new intersection estimate from two actual momentum kernels gives uniform phase-space weak \(L^{4/3}\) and a complete, uniformly integrable first moment of \(Z_m\). No independence or pressure premise is inserted. |
| Critical-band and full singular-roof payment | 315, **cor:sm-critical-band**, **thm:sm-roof** | The actual \(I_m/\lvert\nabla_qF\rvert\) critical-band volume is \(O(s^{1/4})\); the full singular-roof density is weak \(L^{12/11}\), and the complete deep-source singular volume and stated roof norms receive the \(m^2\)-normalized payment. |
| Actual regular-interior variation and marked comparison | 315, **cor:sm-variation**, **cor:sm-marked**; 314, **cor:fr-full-comparison** | The retained one-copy physical variation inequality now has a finite full-source right side and a normalized deep-source payment. Exact marked comparison retains the signed endpoint clock work in the proved roof spaces. |

Weak \(L^q\) here means precisely
\[
 \|f\|_{q,\infty}
   =\sup_{\lambda>0}\lambda
      |\{t\in\mathbb R:f(t)>\lambda\}|^{1/q}.
\]
It uses Lebesgue measure on the original physical roof line. It is neither a smoothed observation nor the essential supremum required by the final raw theorem.

## 3. Response to the six substantive requests in Section 18

### 18.1. Complete clearance chart sum and the normalized roof topology

**Request.** Control the entire physical sum, including folds, higher degeneracy, critical roofs, one-sided boundaries, cuts, and pairing seams, with common constants before taking the roof essential supremum.

**Inherited conclusions retained.** The local Jacobian, finite-type, fold, and critical statements in 274–275 remain at their original scopes. In particular an exponentially large determinant does not imply a lower bound on the smallest singular value or on a complete inverse-Jacobian sum. The physical endpoint continuation, support inequality, and distortion arguments in 288–293, and the complete fixed-margin atlas in 311, are inherited proved results. They are not claimed as new discoveries here.

Module 311 already performs a complete positive physical sum on \(\mathcal G_{\varepsilon,m,R}\): actual inverse-momentum tubes, global uniqueness per physical word, and overlap at most 25 replace a collision-word count. Its constant is exactly of order \(\varepsilon^{-2}\). The predecessor correctly left the complement outside that \(L^\infty\) conclusion.

**New proof beyond the fixed guard.** Module 314 controls that complement quantitatively. At most two physical flights occur at each end depth, and at most two interior contacts occur at each positive depth. The exact clearance flux and incidence marginal give
\[
 \nu(\mathcal C_{m,R}\setminus\mathcal G_{\varepsilon,m,R})
 \le B_\Delta\varepsilon+B_c\varepsilon^2
 \qquad(0<\varepsilon\le\varepsilon_\sharp=1/200),
\]
with the explicit constants in **eq:fr-constants**. This statement counts all third disks on every closed actual flight, including disks encountered at other times. It does not omit a collision or assume that different margins are independent.

Combining this physical tail with the full atlas yields, for every Borel roof set \(S\),
\[
 \mu_{E,H}(S)\le A_E\varepsilon^{-2}|S|+B_\sharp\varepsilon.
 \tag{314: eq:fr-finite-exhaustion}
\]
This inequality is proved at each finite collision count and for every allowed \(\varepsilon\). Taking \(S\) null and then \(\varepsilon\downarrow0\) proves full absolute continuity. For a density superlevel set, choosing \(\varepsilon=\sqrt{2A_E/\lambda}\) in its valid range, and using the mass bound outside that range, gives
\[
 \|f_{E,H}\|_{3/2,\infty}\le W_E,\qquad
 \mu_{E,H}(S)\le\min\{M_E,3W_E|S|^{1/3}\},
\]
where
\[
 W_E=
 \left[\sqrt{2A_E}\,
    \max\{2B_\sharp,M_E/\varepsilon_\sharp\}\right]^{2/3}.
\]
Both high and low superlevel regimes are proved in **lem:fr-exhaustion**. This is a complete positive source estimate after all physical words have been summed. No shrinking observation window is substituted into a fixed-window theorem.

The actual insertion is then treated on the same physical roof preimage. The exact marginal gives \(\int h/c_i\,d\nu\le2(\int h\,d\nu)^{1/2}\), and
\[
 \sum_{i=1}^{m-1}q_0^{d_i}\le\frac{47}{3},\qquad
 \int hI_m\,d\nu\le\frac{97}{3}\left(\int h\,d\nu\right)^{1/2}.
\]
The conditioned roof consequence has the single resulting factor \(c_*^{-1/2}\), as shown in **eq:fr-weighted-full**. It gives weak \(L^{6/5}\) for the actual insertion without replacing it by a fixed-guard upper bound.

**What this completes and what remains.** Full positive-margin coverage, complete bulk absolute continuity, and the displayed collision-uniform roof spaces are now proved. It is no longer accurate to list the entire guard complement as wholly uncontrolled. However, the demanded full \(m^2L^\infty\) estimate is not a consequence of these weak norms. Arbitrarily narrow roof spikes and separately defined boundary traces remain outside that implication. The local chart hypotheses in 274 and all positive one-sided contributions remain in the manuscript; they are neither deleted nor silently declared classified by this bulk argument.

### 18.2. First-order single marks and cross-flight clearance

**Request.** Pay the actual first-order source across flights with one-copy multiplicity and exact records; duplicate control on one flight is insufficient.

**Inherited conclusions retained.** The identity
\[
 \int N_\delta\,d\nu=\delta/R
\]
in 270 and the exact ordered same-flight coarea in 276 are unchanged. The distinct first-order indicator and second-factorial duplicate bounds remain distinct. Modules 277–278 already supply actual cross-flight Jacobi/coarea and marked-pressure implications, with their stated pressure dependence; later native curve-growth and momentum-kernel results retain their separately proved scopes. These historical increments are not reassigned to this revision.

The exact-record disintegration in 273 still has precisely
\[
 \frac{1}{4\pi R c_*}\int_0^\delta
              \mathcal K_{m,R,n,k,j,u}(S)\,du.
\]
There is no additional conditioning on a near miss and no second section-normalization factor. The stronger pointwise kernel domination **eq:cf-bridge-input** remains an explicitly unproved sufficient route.

**New full-source normalized payment.** The source in **thm:fr-deep-source** is exactly the observable exceptional union of 309. Its clearance, incidence, and section-collar widths, actual time indices, and observable definitions are unchanged. In particular
\[
 q_{\rm a}=\frac{3263680}{3263681},\qquad N=94
\]
retain their inherited values; \(q_{\rm a}\) does not replace \(q_0\) in \(I_m\).

The theorem consumes the already proved six-term widened-observation budget \(V_\varepsilon(D)\) from **eq:nh-budget** in 312. It preserves the squared-incidence widening coefficient 16, the closed-flight clearance tests, both end-depth sums, and the original section collar. The finite threshold \(D_{\rm cv}\) places every used width in its strict physical flux and collar range. The expression \(V_0(D)\) is the zero-widening mass bound, not a zero-radius physical tube.

For \(D_m=\lceil\theta m\rceil\), \(0<\theta<1/2\), the full source, including every arbitrarily small positive margin, satisfies
\[
 \|f_{D_m,H}\|_1=O(e^{-\lambda_bm}),\qquad
 \|f_{D_m,H}\|_{3/2,\infty}=O(e^{-\lambda_bm/3}),
\]
\[
 \|f^I_{D_m,H}\|_1=O(e^{-\lambda_bm/2}),\qquad
 \|f^I_{D_m,H}\|_{6/5,\infty}=O(e^{-\lambda_bm/6}),
\]
where the inherited positive rate is
\[
 \lambda_b=\theta\min\{|\log q_{\rm a}|/(4N),|\log(47/59)|\}.
\]
Every displayed norm vanishes after multiplication by \(m^2\). The strong \(L^p\) rates are explicit in **eq:fr-deep-rates**. Positivity and invariant one-time marginals suffice for the observable union; no joint independence, Poisson law, or multiplication by the number of physical words appears.

**Remaining part of the request.** This is a normalized estimate for the complete original deep observable source in the stated full-roof spaces, beyond the predecessor's fixed-guard restriction. It is not a complete roofwise insertion theorem for every shallow single-clearance source. A first-order witness with no duplicate, including the clearance-only case with empty incidence witness set, remains a genuine possible contributor to the original low-load source. Its final \(m^2L^\infty\) payment or a valid same-roof capacity comparison is still required.

### 18.3. Critical roofs, physical multipliers, and boundary budgets

**Request.** Sum the relevant coefficients and errors with their actual Jacobians, preserve physical one-sided cuts, and integrate the result with the real pairing construction.

**Inherited critical geometry retained.** The criticality identity \(\nabla_qF=R(-p_0,p_m)\), the actual reversing orbit, and the monodromy coefficient in 275 remain unchanged:
\[
 \mathfrak J(x)
 =\frac{\omega}{2c_*\sqrt{\det G}}
 =\frac{1}{Rc_*\sqrt{|\det(I-DT_R^{2m})|}}.
\]
The occupation identity is \(A_{2m,R}=A_{m,R}+A_{m,R}^{\mathcal I}\); it is not replaced by \(2A_{m,R}\). The local angular selector, its possible absence of a limit, and the physical-side interpretation at an unvisited tangency or section cut are retained. Neither an unscaled critical coefficient sum nor a bulk-null critical fiber is called a complete normalized endpoint payment.

**New mixed physical mechanism.** A main remaining multiplier was the product of inverse endpoint momentum and inverse incidence. Separate marginal estimates are not enough to prove its first moment. Module 315 uses the fully native kernel **thm:mc-kernel** of 284 on the actual blocks \(0,\ldots,m\) and \(0,\ldots,i\). With \(r=|(p_0,p_m)|\), it proves
\[
 \nu\{r<s\}\le A_0s^2,\qquad
 \nu\{r<s,\ c_i<u\}\le A_1su^2,
 \quad
 A_0=\frac{C_{\rm mom}}4,\quad
 A_1=\frac{C_{\rm mom}}\pi.
 \tag{315: eq:sm-intersection}
\]
The second bound is a joint restriction on the same trajectory, not a product of probabilities. It is proved for every \(s,u>0\), including the large-\(u\) range.

On \(r<b\), the first bound costs \(A_0b^2\). Summing the complete dyadic annuli \(2^jb\le r<2^{j+1}b\) with the second bound costs at most \(4A_1/(bt^2)\). Choosing \(b=(A_1/A_0)^{1/3}t^{-2/3}\) gives
\[
 \nu\{(rc_i)^{-1}>t\}
 \le K_\times t^{-4/3},\qquad
 K_\times=5A_0^{1/3}A_1^{2/3}.
\]
Layer cake then pays the real insertion at all depths. With
\[
 J_\times=
 \frac1{R_-}\left(2\sqrt{A_0}
            +\frac{188}{3}K_\times^{3/4}\right),
\]
**thm:sm-full-multiplier** proves
\[
 \int hZ_m\,d\nu\le J_\times
       \left(\int h\,d\nu\right)^{1/4}
 \qquad(0\le h\le1).
 \tag{315: eq:sm-full-functional}
\]
Thus the full actual multiplier has a collision- and radius-uniform first moment and uniform integrability, including arbitrarily small positive incidences and endpoint momenta. The source theorem does not assume \(Q_*\), a lower clearance margin, a tangent-sector selection, or an artificial independent model.

The conditioned restricted-mass inequality is
\[
 \int hZ_m\,d\nu_R^*
 \le J_\times c_*^{-3/4}
             \left(\int h\,d\nu_R^*\right)^{1/4}.
\]
The power \(c_*^{-3/4}\) follows from \(a=c_*\int h\,d\nu_R^*\) and a single division by \(c_*\). It is displayed explicitly in **eq:sm-conditioned-functional**.

**Critical-band consequence with the actual insertion.** The disk estimate **eq:sm-disk-Z** proves
\[
 \int_{\{r<a\}}Z_m\,d\nu
 \le\frac{2A_0a+94\sqrt{A_0A_1}\,a^{1/2}}{R_-}.
\]
For the actual one-copy critical-origin arm family of 286, its proved geometry gives \(r\le A_s=\min\{\rho,\sqrt{2U_ms}\}\). Therefore **cor:sm-critical-band** gives the complete actual \(I_m/|\nabla F|\) volume \(O(s^{1/4})\), uniformly in words, radii, labels, and allowed Borel arm selections. The proof does not extend an arm beyond its physical boundary.

**Full roof and variation consequences.** Combining the restricted-mass bound with 314 yields full weak \(L^{12/11}\) for the original singular-roof density. For the complete deep source,
\[
 \|f^Z_{D_m,H}\|_1=O(e^{-\lambda_bm/4}),\quad
 \|f^Z_{D_m,H}\|_{12/11,\infty}=O(e^{-\lambda_bm/12}),
\]
\[
 \|f^Z_{D_m,H}\|_p
 =O(e^{-\lambda_bm(2/p-7/4)}),
 \qquad 1<p<12/11.
\]
These are the full-volume and roof-norm statements in **eq:sm-roof-rates**; each has zero \(m^2\)-normalized limit. They include every original roof interval without enlarging its width or changing its location.

The connection to an existing physical budget is explicit. Applying the retained one-copy **prop:el-positive** of 289, **cor:sm-variation** proves, for every Borel roof set,
\[
 \mathcal V_{\varepsilon,E,H}(S)
 \le C_{\rm reg}(1+\varepsilon^{-1})
                     \mu^Z_{E,\mathbf1_\Pi H}(S).
\]
The derivative is the regular-interior derivative of the actual \(f^\varepsilon\), taken before multiplication by any source or section indicator. The full regular-interior variation is now finite uniformly in \(m,R\); its restriction to the full deep source has the stated normalized decay at every fixed original \(\varepsilon(B)>0\).

**Boundary limitation kept explicit.** This closes an actual bulk singular-factor and regular-interior derivative budget. It does not differentiate an exact-event selector, count jumps between separate physical segments, construct a missing pairing, or dominate an endpoint minimum by an unrelated small bulk set. A separately defined one-sided or paired endpoint charge still requires its own valid trace or capacity inequality. The full unscaled variation bound is not the vanishing whole-shallow normalized variation input. These distinctions are made in the proof of **cor:sm-variation**, not postponed to the response alone.

### 18.4. Low-incidence load and the surviving shallow source

**Request.** Prove original-source scarcity or enough genuine comparison capacity for low-load source that survives the previously paid classes.

The original positive identity and pool in 269 are retained:
\[
 \mathsf U_B^{\rm per}
 =\mathsf U_B^{\rm exc}+\mathsf U_B^{\rm load}
                          +\mathsf U_B^{\rm low},\qquad
 \mathsf R_B^{\rm low}
 =(\mathsf U_B^{\rm low}-K_BP_{r_B}^{\rm ng})_+.
\]
Their original dependence on the marked-pressure input is not concealed. The already established payments of deep, numerous, and high-load incidence source remain inherited; this revision does not repackage them as new work.

The new contribution here is the removal of the positive-margin restriction from the full deep-source bulk and stated roof norms, and the complete actual multiplier estimate above. Where the native positive domination \(0\le c_{\rm per}\le f^\varepsilon\le A\) of **lem:v111-domination** applies, a restriction of that original source inherits the corresponding established source-side bound. The derivative consequence uses precisely the measure inequality of **cor:sm-variation**.

The observable union \(\mathcal E^{\rm obs}_{D_m,R,m}\) is used as defined in 309. It has not been renamed to be the entire low-load source. The exact central comparison off that union does not delete shallow end portions, clearances, incidence witnesses, or section tests. A clearance-only witness may have zero incidence load. Low load therefore does not establish small original mass, small normalized roof height, or available same-roof capacity.

The completed uniform first moment of \(Z_m\) is also not a source-scarcity theorem: multiplication of a merely uniform full-source mass by \(m^2\) need not vanish. The still-open shallow part requires a bound on its actual source or actual endpoint charge in the original topology. This is the precise unresolved obligation, rather than a newly named residual or an additional conditioning hypothesis.

### 18.5. Capacity abundance of the full nongrazing pool

**Request.** Show that the original full pool has enough roofwise capacity after the complete physical source sum.

The existing full pool \(P_{r_B,m}^{\rm ng}\) remains unchanged. The inherited contraction to every global minimum, the retained physical center comparisons, and the new full-source bounds make the source costs more explicit. They do not by themselves give a lower bound for a pool at the same original roof and exact labels.

The current full marked comparisons, **cor:fr-full-comparison** and **cor:sm-marked**, retain the central integer record, the two separate endpoint tests, and the original complete roof pushforward. In particular the compensating phase is \(e^{-isW_d}\), with the sign dictated by
\[
 L_d(Y)-L_d(Q)=W_d+T_{\rm clock},\qquad
 0\le T_{\rm clock}\le2R_+q_{\rm a}^{\lfloor d/N\rfloor}.
\]
The finite-count hypotheses include \(d\ge1\) and \(2d<m\). With \(d=\lceil\theta m\rceil\), fixed \(0<\theta<1/2\), the normalized comparison holds uniformly in all lattice and return twists and
\[
 |s|\le e^{\lambda m},\qquad
 0<\lambda<\lambda_c=\theta|\log q_{\rm a}|/N.
\]
Its strong roof-norm ranges are \(1\le p<3/2\) without insertion, \(1\le p<6/5\) with \(I_m\), and \(1\le p<12/11\) with \(Z_m\); \(p=1\) denotes total variation of the corresponding density. The finitely many counts before \(2d<m\) hold do not affect the limit. These estimates do not authorize an unbounded Fourier inversion.

A physical comparison preserving a central word can still have nonzero endpoint work. Source-side upper volume is not same-roof lower capacity. A complete abundance proof must attach the real shallow portions, meet the original return/displacement/collision/roof tests, and include the map's actual Jacobian and multiplicity. No such full-pool abundance theorem is asserted in 314–315. Direct control of the unchanged shortage remains an alternative, but its required topology is the original one.

### 18.6. Inherited global dynamical, optical, pairing, and analytic inputs

**Request.** Reconstruct pressure, optical comparison, physical multiplicity and singular passage, and the spectral/arithmetic/conditional inverse consequences under their actual uniform quantifiers.

The proof ledger now distinguishes the following interfaces.

**Optical comparison is completed inherited work.** Module 313 proves, in true Euclidean stable arclength in the actual \((s,\varphi)\) collision coordinates,
\[
 \frac{c_mj_m}{30000}\le\omega\le30000c_mj_m,\qquad
 j_1/c_0\le6400.
\]
It holds on the full-collision-area set \(M_R'\) regular in both infinite directions, with arbitrarily small positive incidence. The signs, arclength conversion, empty cocycle block, and original \((\alpha,p)\) optical convention are explicit. These complete the two optical components of **input:v112-geometric-pressure**. They are inherited here, not new 314–315 claims. Equality of finite-record bulk measures on that full-area domain does not erase a separately defined singular trace.

**The physical momentum kernel is also inherited.** The kernel **thm:mc-kernel** of 284 already includes the actual first-image construction, homogeneous component summation, and endpoint incidence cancellation. Modules 281–283 supply its native admissible-curve geometry and matched growth scope. Module 315 makes a new use of two instances of that kernel to prove the mixed intersection estimate; it does not claim a newly established kernel.

**Restricted pressure is proved; unrestricted pressure remains separate.** The inherited **cor:nh-guarded-pressure** of 312 proves
\[
 \sum_w\sup_{[w]_R\cap M_R'\cap\mathcal G_\varepsilon}j_m
 \le
 \frac{1500000R_+^2U^2C_{\rm dist}^2}
      {(\rho_\varepsilon^{\rm at})^2},\qquad
 \rho_\varepsilon^{\rm at}
     =\frac{g\delta_*\varepsilon}{128R_+}.
\]
This is the atlas radius of 311, with its endpoint cap and fixed guard. It is not a whole-cylinder bound. The all-margin mass and weak-norm estimates in 314–315 do not control
\[
 \sup_{R,l}\sum_{w\in\mathcal W_l(R)}
                    \sup_{[w]_R\cap M_R'}j_l
 \le Q_*.
\]
Taking a supremum within each word is different from integrating a small margin set. No exhaustion argument in this response promotes guarded pressure to \(Q_*\). The stronger historical 239/241 passage still needs uniform physical test-curve realization, whole-partition domination, and bounded multiplicity at its actual singularity cuts.

**Pairing and singular passage retain their own scope.** The new variation consequence explicitly consumes the inherited countable one-copy coarea; it is not an independent reconstruction of every incident-component pairing. It covers a concrete derivative measure and the actual \(I_m/|\nabla F|\) bulk factor. Boundary traces, their matching conventions, simultaneous endpoint configurations, and any positive minimum on a short actual segment must still be paid by their genuine physical trace/capacity construction.

**Spectral, arithmetic, conditional, and inverse conclusions are not inferred from bulk regularity.** The original geometry, periodic orbits, exact arithmetic obstructions, induced return, spectral interfaces, and four-coordinate inverse formulas are retained. Their family-uniform function spaces, twisting estimates, small and large roof frequencies, error integration, and conditional microscopic denominator require their actual hypotheses. An arithmetic-forbidden class is never assigned a positive conditional denominator. Full phase-space \(L^p\) integrability of a multiplier does not establish a pointwise exact-record probability or control the long-time inverse Jacobian.

The literature audit keeps the primary theorem passages and historical use scopes separate. In particular the specified-curve homogeneous growth estimate of Demers–Zhang is not a whole-word supremum estimate; the relevant long-cell and distortion results of Baladi–Demers do not acquire radius-family uniformity merely from uniformity in a potential parameter; and the flow LLT of Dolgopyat–Nándori retains its actual cohomology, subgroup, covariance, and endpoint-test assumptions. None is cited as a substitute for the original four-variable conditioned raw conclusion. The new central steps in 314–315 are proved directly from named native inputs by positive measure estimates, exact area bounds, and layer cake. No unchecked external theorem supplies a missing closure.

The current proof reconstruction and code checks are author-side validation. No independent human specialist certification of the entire pressure, pairing, spectral, or inverse chain is claimed.

## 4. Response to each completion route in Section 20

### 20.1. A complete normalized clearance theorem

The requested route requires the complete exact-label one-copy source, including physical boundaries and degeneracies, to have the required \(m^{-2}\) roof-density bound on the central target. The retained atlas supplies an \(L^\infty\) theorem at fixed physical margins, and 314–315 now prove all-margin bulk and weak/strong roof bounds with normalized decay for the complete deep source. These are substantial new parts of that route. They do not provide the demanded full shallow-source essential-height bound or a complete singular endpoint sum. This route is **advanced but not closed**.

A sufficient next bridge must convert the remaining original positive contributions to the actual central \(m^2L^\infty\) payment after their full sum, with common constants. It cannot consist only of per-chart shrinking neighborhoods or a bound on the Lebesgue measure of exceptional roofs.

### 20.2. Target-roof clearance insertion across physical flights

The exact one-mark kernel, actual cross-flight geometry, and conditional marked-pressure implications remain preserved. The new proof handles a full many-flight observable union without independence and without a word-count factor; the new mixed kernel also controls the real singular insertion on that complete source. It does not establish the unrestricted roofwise marked-pressure or exponential-moment theorem for all shallow clearance witnesses. This route is **advanced but not closed**.

The original sufficient condition **eq:cf-bridge-input** remains explicitly unproved. A suitably summed positive kernel bound can replace that stronger per-mark condition, but it must have the same exact-label normalization and original ordered-limit consequence.

### 20.3. Capacity abundance

The new source norms, central record comparison, and full singular-volume payment are upper source estimates. They are not a lower bound on the full nongrazing pool at the same roof. The prescribed capacity route is **not closed**. A valid completion must preserve all original labels and end portions and verify the actual comparison Jacobian, available target measure, and bounded physical multiplicity. No conveniently selected subpool or Markov surrogate is introduced.

### 20.4. Direct proof of the remaining shortage limit

The original positive-part quantity is retained and is displayed in Section 7 below. New theorems pay genuine components but do not prove its full roof essential-height limit. This route is **not closed**. The same conclusion applies to the organizing raw pointwise LLT and full four-coordinate inversion. Their theorem statements and dependencies are retained with an accurate status, rather than replaced by the new auxiliary weak-norm theorems.

The request for an independent billiards and transfer-operator reconstruction remains outstanding at its full scope. This author response does not present internal proof validation or CI as that independent review.

## 5. Response to all nine presentation and source-record requests in Section 21

### 21.1. Paired author, response, and referee-copy refs

The intended publication consists of one complete author-source commit and the author, referee-response, and referee-copy refs resolving to that same source. These are publication labels, not independent referee endorsements. Their actual names, commit identities, and readbacks belong in [PUBLICATION_STATUS.json](PUBLICATION_STATUS.json) and the current publication receipts. At the preparation of this response, publication of the new iteration is not asserted complete. The already published predecessor triple and its source identities remain historical evidence.

### 21.2. Preparation metadata and post-push facts

[SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) fixes the baseline and controlling report. It does not invent the containing commit's future identity. Preparation-time metadata, local mathematical executions, actual remote source verification, and subsequent exact-head CI are separately scoped. A frozen null remote field remains an earlier observation, not a current denial of a later verified push. Conversely a planned ref or job is never called completed. Later publication receipts must state their actual observation time and tested source rather than silently rewriting an earlier record.

### 21.3. Separate the mathematical provenance

The distinct reviewed contributions remain visible: 270–273 contain the flux, transverse test, transfer, and exact-record interface; 274–275 contain the long-record and local critical/fold geometry; 276 contains the same-flight ordered two-mark theorem. Modules 277–309, and the physical-tube and explicit optical results 310–313, are now inherited. Only **314–315** are the present theorem increment. The actual kernel of 284 and the explicit optical proof of 313 are named as inputs rather than new achievements. [PROOF_LEDGER.md](PROOF_LEDGER.md), [PROOF_INDEX.json](PROOF_INDEX.json), and the preserved prior source establish this separation.

### 21.4. Explicit horizon and finite lattice counts

The retained auditable location is [module 287](core/287_explicit_physical_horizon_and_lattice_budgets.tex), **thm:eh-horizon** and **cor:eh-counts**:
\[
 \tau_-\ge3/50,\qquad
 \tau_+\le\sqrt{3847/124}<28/5,
\]
\[
 N_f,N_\circ\le150,\qquad N_{\rm pair}\le162,\qquad
 J_f\le301,
\]
with at most 1201 angular first-hit intervals. These are enclosing geometric candidate bounds, not finite-sample estimates. The overlap 25 in the atlas is a separate momentum-grid multiplicity, not a count of collision words or marked disk pairs.

### 21.5. Ordered pairs, factorial counts, and witness indicators

The ordered identity **eq:dc-exact** and factorial bound **eq:dc-factorial** in 276 remain unchanged; opposite relative vectors represent the two orders. The difference between \(N_\delta\), \(\mathbf1_{\{N_\delta\ge1\}}\), and \(N_\delta(N_\delta-1)\) is maintained. The new margin and observable-union bounds use only positive domination \(\mathbf1_{\{N\ge1\}}\le N\), invariant actual marginals, and the explicit at-most-two depth count. They do not turn an \(O(\delta^2)\) duplicate estimate into an \(O(\delta^2)\) first-order source bound.

### 21.6. Total variation and roof essential height

The distinctions are strengthened. The inherited fixed-guard height theorems, the new full-source weak \(L^{3/2}\), weak \(L^{6/5}\), and weak \(L^{12/11}\) theorems, and the actual singular-volume/regular-interior variation bounds each state their own topology. The strong endpoints are not claimed. Quantitative superlevel control in **eq:fr-spikes** is not roof essential-height control.

For example, as an analytical illustration only, \(f_m=m^{-2}\mathbf1_{[0,e^{-m}]}\) has \(m^2\|f_m\|_{q,\infty}\to0\) for every finite \(q\), while \(m^2\|f_m\|_\infty=1\). This is not asserted to be a billiard density; it records exactly why the proved weak-norm limits cannot certify the final raw theorem.

### 21.7. Image and preimage conventions

The retained reversible identity in 271, **eq:cf-reversal**, uses \(IE\) and \(T_RE\) as set images on the regular invertible domain. \(T_R^{-1}E\) denotes a preimage. The new fixed-time probability estimates use invariant preimages of the actual events. The tube saturation in 311–312 is an auxiliary physical union for positive domination; it is not an altered conditioning event. These conventions prevent reversal, time shifting, or saturation from changing the exact source.

### 21.8. A local critical component and the complete density

The density in 275, **thm:cr-critical-density**, remains the contribution restricted to its specified coordinate ball, with its Borel angular fraction. The inherited critical-tube theorem and complete fixed-guard atlas state separately what they sum. The new **cor:sm-critical-band** covers exactly the one-copy physical arm family of 286, not all roots at an arbitrary nearby roof. Full roof regularity in 314–315 comes from the complete source/atlas argument, not by treating one local critical component as the global density.

### 21.9. Exact-head workflow completion and its mathematical boundary

The actual successful predecessor run is **39187286448**, at scientific head **8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2**. The preserved receipt records its completed success, 44 mathematical commands, 35 normal/optimized output pairs, the three-pass 164-page native build, and the actual historical rebuild. The selected final carrier **fdf2603c8bf422314f199fa431086485a0d1ebb5** is a later publication-evidence successor; its skipped metadata CI is not a separately executed scientific run.

At the preparation of this response, the new iteration's current CI is **not started** in [PUBLICATION_STATUS.json](PUBLICATION_STATUS.json). This statement is temporally scoped. A later completed new run may be claimed only after its exact head, job steps, artifacts, and source inputs are read back and recorded in the current receipt. Neither the real prior CI nor this iteration's local proof checks are represented as execution of the new whole article. A successful build makes the source reproducible; it is not a certificate of the continuous mathematical argument.

## 6. Earlier detailed objections retained at their exact scope

The following crosswalk records the material technical points in Sections 6–17 of the controlling report, in addition to the responses above.

| Report passage | Native locator and author response |
| --- | --- |
| Section 6: exact one-mark flux, endpoint foot, multiplicity, and measure factor | 270, **lem:cf-foot**, **eq:cf-jacobian**, **thm:cf-flux**, **eq:cf-exact-mean** remain intact. The new margin proof uses the exact first-order flux in its strict range; no unvisited mark is inserted as a reflection. |
| Section 7: grazing-uniform transverse tests and curve-growth topology | 271–272 remain unchanged; the completed native curve-growth match in 281–283 and the kernel in 284 are inherited separately. Bounded dependence on roof frequency is not decay permitting arbitrary Fourier inversion. |
| Section 8: exact record kernel and missing pointwise bridge | 273, **thm:cf-record**, **eq:cf-record-disintegration**, **eq:cf-bridge-input** retain one \(c_*^{-1}\), all exact labels, and the explicit unproved sufficient bridge. The new full-source theorem does not promote a conditional angular kernel to a uniformly bounded density. |
| Section 9: long-time determinant versus conditioning of the Jacobian | 274, **eq:cr-area**, **eq:cr-gauss**, **eq:cr-chain-hessian** retain the full Hessian chain term. New full-source estimates use actual physical tubes and source distributions; they do not infer a smallest singular value or global inverse bound from determinant growth alone. |
| Section 10: finite-type bands and integrated folds | 274, **thm:cr-finite-type** and **thm:cr-fold**, keep their derivative, radius, and monotonicity hypotheses. Their local constants are not declared uniform on every degenerate or boundary chart. |
| Sections 11–13: reversing orbit, occupation, monodromy, and local critical coarea | 275, **thm:cr-periodic**, **eq:cr-occupation**, **thm:cr-monodromy**, **thm:cr-critical-density**, and **cor:cr-one-sided** are unchanged. New 315 proves the actual singular insertion on the precise physical critical bands, without a fictitious orbit on a boundary or an automatic angular-selector limit. |
| Sections 14–17: two-mark transversality, ordered roots, factorial law, and its limits | 276 retains the exact constant \(\sqrt{591}/100\), physical mask, ordered branches, and the distinction between first-order source and second-order duplicates. Later cross-flight results retain their stated premises; 314–315 do not replace a many-flight law by independent sampling. |

The historical v112 obstruction and v113 submission-state objection remain traceable through the complete preserved reports. A workflow-only branch is still not a mathematical source, and finite tests of a coarea identity still do not prove the uniform normalized sum.

## 7. Minimum remaining closure and original order of limits

For each fixed central-window bound \(M\), the unresolved organizing quantity remains exactly
\[
 \lim_{B\to\infty}\limsup_{m\to\infty}\sup_{R,n,k}
 m^2\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
 \bigl(\mathsf U^{\rm low}_{B,m}(t)
                    -K_BP^{\rm ng}_{r_B,m}(t)\bigr)_+=0.
\]
It is the same positive source and full comparison pool as in the inherited scalar reduction. Neither \(\mathcal E^{\rm obs}_{D_m,R,m}\) nor a guard complement is substituted for the complete residual.

All physical sums are taken before the required essential supremum. The original outer parameters \(\varepsilon(B),h_B,r_B,\gamma_B,K_B\) are fixed before the collision limsup, and \(B\) tends to infinity last. The finite-\(m\) optimization in 314 proves a new function-space inequality valid at that finite \(m\); it does not exchange these original limits. Substitution of \(D_m=\lceil\theta m\rceil\) occurs only after a theorem valid at each finite \(D,m\), and changes neither a microscopic window nor a conditioning event. In the actual variation corollary, \(C_{\rm reg}(1+\varepsilon(B)^{-1})\) is fixed before taking \(m\to\infty\).

The minimal outstanding mathematical obligations are now more specific:

1. **Original shallow positive height or real pool capacity.** Prove the above \(m^2L^\infty\) shortage limit for the surviving original low-load/shallow source, by a direct positive estimate or a same-roof capacity construction. The new full-source weak norms and deep-source decay cannot replace this condition.
2. **Actual endpoint and pairing charges.** Connect every remaining positive one-sided, cut, seam, or short-segment endpoint contribution to a proved physical trace/variation/capacity bound with its own Jacobian and multiplier. The full bulk integrability of \(Z_m\) and its regular-interior derivative payment are completed; a separate endpoint minimum does not follow from them automatically.
3. **Unrestricted global and analytic interfaces where used.** Establish the required whole-word \(Q_*\) bound or a valid direct replacement at every place it is invoked, and reconstruct the uniform spectral/arithmetic inversion, microscopic conditional denominator, and long-time four-coordinate inverse estimates under the original spaces and quantifiers. The completed optical comparison and momentum kernel remain available inputs and are not left as repeatedly renewed tasks.

These are closure conditions on the original mathematical problem, not new assumptions added to an unconditional theorem. The present revision does not remove proved results, weaken the microscopic target, change the physical clock, or use a different stochastic system.

## 8. Preservation, proof validation, and execution records

The historical preservation audit retains the full parent packet, all earlier proof bodies, reports, responses, failures, counterexamples, and actual execution evidence. The new article keeps the earlier native bodies 260–313 byte-identical; modified author documents and derived delivery material have their exact predecessor bytes preserved. Earlier article directories, review branches, companion papers, and unrelated papers are outside this author revision's modification scope.

For the two new modules, the author proof validation reconstructs the all-Borel exhaustion, high/low superlevel split, mixed two-kernel intersection, complete annular sum, all normalization powers, exact \(q_0\)-depth factors, critical-disk constants, strong-norm exponents, actual variation transfer, and signed physical clock comparison. The mathematical diagnostic program uses explicit failing checks under ordinary and optimized Python; it does not rely on removable assertions. Its normal and optimized preliminary executions both completed successfully with identical deterministic output. These are checks of the displayed algebra, finite index conventions, and logical negative controls, not synthetic physical evidence or a proof of the continuum theorem.

The independent reconstruction within the author team read both new complete proof bodies and their specified inherited inputs. That record is separate from a commissioned external specialist audit. Current native compilation, source-freeze, publication, and CI facts must be read from their actual current receipts and [PUBLICATION_STATUS.json](PUBLICATION_STATUS.json); no pending execution is claimed complete in this response.

The new full-source singular-factor and deep-source theorems are submitted with complete native proofs and an explicit dependency record. The original raw pointwise theorem remains the unchanged goal, with the precise remaining closure stated above.
