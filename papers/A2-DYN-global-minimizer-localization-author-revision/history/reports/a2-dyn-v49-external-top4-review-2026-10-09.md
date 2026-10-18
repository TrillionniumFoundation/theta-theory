# External top-four referee report on A2-DYN revision 49

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v49-referee-response-2026-10-09`, `revision/a2-dyn-v49-referee-copy-2026-10-09`  
**Reviewed commit:** `f3174ed1e7e339aa9c4bb5bd716a24653080c7dd`  
**Reviewed repository tree:** `aef11215031a8fe99cea3e4e07d38841871a837f`  
**Ordinary source payload tree:** `cfe61ff963dc68ac0fd8fda9399deb15f53e3be2`  
**Active manuscript directory:** `papers/A2-DYN-v49-referee-response`  
**Active mathematical source:** one hundred seven numbered core modules; revision 49 adds modules 105--107  
**Frozen revision-48 author baseline:** `418000c216e9efa7c259a9bee9dac4fcf288ee1d`  
**Frozen revision-48 ordinary paper tree:** `8918ca0a31f4966750326217f15b79ad71ba6df7`  
**Controlling report:** `reviews/a2-dyn-v48-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `3c8a41dd89f8491ac85c1ba40d85c68dc040e6dc` / `931f8f23563434275fb6d02b7077bfccda740954`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 49 is a substantial theorem-bearing advance. The preceding external report reduced the still-uncontrolled positive source to the physical incidence and clearance layers. The present manuscript addresses exactly those two sources, without transporting an orbit across a grazing or competing-hit seam and without replacing the original exact return coefficient by an averaged packet.

The new result is stronger than a fixed-interval probability local limit. For the complete original mixed density, the manuscript proves, for every fixed roof-window length \(h>0\),

\[
 \sup_{R,\,1\le n\le m,\,k,t}
 \frac1h\int_t^{t+h}
 \left|m^2p_{n,R}(k,m,u)
       -\mathcal L_{m,R}(k_1,k_2,u,n)\right|\,du
 \longrightarrow0.
\]

The absolute value is taken before integration. Equivalently, the conclusion is uniform over every measurable roof selector of modulus at most one supported in the translated interval, even when the selector is chosen after the collision count. The source is the unmodified original first-return source, every exact discrete label is retained, and the finite transition kernel keeps all arithmetic branches. The paper also derives total-variation convergence of the central mixed measure and of the exact-window conditional roof law.

This is a real closing of the revision-48 **local-variation** blocker. I found no decisive counterexample, missing section normalization, erroneous mark shift, Fourier-sign error, illicit packet averaging, or substitution of a count-dependent frequency band into a fixed-band spectral theorem in the new modules.

The negative recommendation nevertheless remains appropriate at the requested benchmark for three independent reasons.

First, the theorem which continues to govern the title and the retained raw-inversion architecture is the pointwise density theorem. Revision 49 expressly does not prove it. Translation-bounded local \(L^1\) convergence allows density spikes of arbitrarily small width and large height. Hence it does not imply the essential-supremum physical-boundary criterion, a pointwise roof-density local limit, or a bridge conditioned at one prescribed roof value.

Second, the new continuum proof is load-bearing and highly specialized. Its validity depends on a uniform physical thin-layer multiplier theorem through grazing homogeneity strips, a moving-peak weak-to-strong interpolation, the full occupation-torus spectral theory, and an all-depth summation in which the finite-count errors must remain uniform in the mark and strip width. These arguments require independent checking by specialists in dispersing billiards and anisotropic transfer operators. The exact-source workflows and finite diagnostics do not provide such verification.

Third, the article remains an exceptionally large, model-specific proof system. The local-variation theorem is mathematically interesting and plausibly publishable as the centerpiece of a focused dynamics/probability paper, but the present manuscript does not yet establish either the complete pointwise arithmetic raw theorem or a general principle of sufficient breadth to meet the requested four-journal standard.

The paper has therefore advanced materially, but the top-four recommendation does not change.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`f3174ed1e7e339aa9c4bb5bd716a24653080c7dd`.

The repository tree is

`aef11215031a8fe99cea3e4e07d38841871a837f`.

The active article is

`papers/A2-DYN-v49-referee-response`.

The ordinary source payload tree recorded in the source manifest is

`cfe61ff963dc68ac0fd8fda9399deb15f53e3be2`.

The reviewed author commit has the controlling revision-48 report commit as its parent. The chronology is therefore correct: the new author revision begins from the frozen external report rather than modifying the previously reviewed author source in place.

The source manifest records that all one hundred four inherited core modules and all one hundred thirty-one inherited Python scripts are byte-identical. The earlier leading statements remain compiled in an appendix, and the bibliography, mathematical labels, A--X synopsis, and prior source records are retained. Revision 49 adds

- `core/105_physical_thin_layers.tex`;
- `core/106_physical_residual_local_variation.tex`;
- `core/107_raw_local_total_variation.tex`;

with revised front matter and source-control records.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v49-external-top4-review-2026-10-09/`.

No author manuscript source, prior report, workflow, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully at the reviewed SHA:

- response branch run `37825377112`;
- referee-copy branch run `37825400351`.

The runs bind the build and finite diagnostics to the exact reviewed event SHA. The verifier checks, among other things,

- the frozen revision-48 tree and controlling-report blob;
- all one hundred seven core inclusions;
- byte identity of the one hundred four inherited cores and one hundred thirty-one inherited scripts;
- retention of inherited labels, bibliography, former leading statements, and the A--X synopsis;
- the ordinary-source Merkle identity and workflow hash;
- agreement of normal and optimized finite diagnostics;
- native TeX compilation with stabilized references;
- theorem-label-based rendering of the new proof pages.

The new finite diagnostics check the signed line-distance derivatives, selected transversality samples, the shift of a clearance mark from flight \(j\) to collision \(j+1\), geometric depth sums, finite-count exponential-error summation, the local convolution inequality, and conditional normalization.

These are useful source, algebra, and bookkeeping checks. They do not certify

- the continuum transversality of every physical envelope on all homogeneous stable curves;
- the fixed-complexity multiplier hypotheses on the anisotropic completion;
- the uniform no-inverse-width strong bound;
- the moving spectral projection interpolation;
- the full occupation-torus spectral theorem inherited from revisions 40--41;
- the all-depth physical remainder estimate on the actual spaces;
- or any pointwise raw-density conclusion.

The manuscript's validation and publication-status files state this boundary accurately. In particular, they continue to mark independent human review and the full pointwise raw LLT as absent.

## 4. Scope of this review

I did not attempt to re-prove all one hundred seven modules. The substantive audit concentrates on the chain that changes the revision-48 assessment:

1. the image-side geometric envelope for a true small-clearance flight;
2. the grazing incidence envelope in the physical collision angle;
3. finite partition complexity and stable transversality uniformly in the layer width;
4. strong multiplication and the \(s^{1/8}\) strong-to-weak gain;
5. moving-peak interpolation to a marked \(s^{1/16}\) local upper bound;
6. exact placement of the clearance mark at collision \(j+1\);
7. preservation of the original occupation convention \(0,\ldots,m-1\);
8. summation over every physical depth before the collision limit;
9. extension to arbitrary bounded measurable source insertions by domination;
10. the local-\(L^1\) convolution inequality for a signed reconstruction kernel;
11. combination with the inherited protected and section-decision corrections;
12. the ordered \(B^{-1/192}\) full-source correction ledger;
13. the passage from the fixed-band arithmetic kernel to the full-source local-variation theorem;
14. the central mixed-measure counting argument;
15. and the normalization of the exact-window conditional roof law.

The inherited load-bearing inputs include the full occupation-torus fixed-band operator theory, strong-space faithfulness, physical peripheral representations, moving spectral peaks, arithmetic transition kernel, complete-source absolute continuity, the protected correction theorem, and the all-depth section-decision theorem.

## 5. The image-side physical envelopes

### 5.1 Clearance is read from the preceding flight

The manuscript correctly avoids representing the clearance of flight \(j\) by a forward observable at its initial collision. It instead reads the same physical segment at the image collision \(j+1\), using the backward incoming velocity

\[
 v^-=\cos\varphi\,n_\alpha-\sin\varphi\,t_\alpha.
\]

For a candidate disk center \(d\), the quantities

\[
 L_d=(d-q_R)\cdot v^- ,
 \qquad
 Z_d=(d-q_R)\cdot (v^-)^\perp
\]

are respectively the longitudinal position of the perpendicular foot and the signed distance of the supporting line. If the actual flight has clearance less than \(s\), the nearest point to the offending nonincident disk lies in the interior of the flight because all endpoint gaps exceed the chosen \(s_0\). Hence the corresponding image state lies in the positive upper envelope

\[
 L_d>0,\qquad R\le |Z_d|\le R+s.
\]

This is only an upper comparison. It does not identify trajectories on opposite sides of a competing-hit seam and does not change a collision label. That distinction is essential and is maintained throughout the proof.

The finite candidate set is justified by finite horizon and the uniform radius range. Keeping the previous incident disk in the candidate list does not enlarge the envelope to a full two-dimensional set: for an actual incident disk the supporting line meets the disk, so its signed distance is at most \(R\), with equality only in the tangential boundary case.

### 5.2 The derivative calculation

In arclength-angle coordinates the manuscript obtains

\[
 \partial_r Z_d=-\cos\varphi-L_d/R,
 \qquad
 \partial_\varphi Z_d=L_d.
\]

On the relevant strips, lattice separation and the upper bound on \(|Z_d|\) give a uniform positive lower bound for \(L_d\). The level curves therefore have positive slope

\[
 \frac{d\varphi}{dr}=R^{-1}+rac{\cosarphi}{L_d},
\]

whereas admissible stable curves have negative slope. Along a stable curve the derivative of \(Z_d\) is bounded away from zero. Consequently a band of \(Z_d\)-width \(s\) cuts a stable curve in intervals of total componentwise length \(O(s)\).

The formula is internally consistent, including the arclength factor \(R^{-1}\). I found no sign error in the backward-flight convention.

### 5.3 Grazing incidence

The incidence layer is written as \(\{\cosarphi<s\}\), i.e. as two angular bands near the grazing endpoints. The proof stays in the collision angle and does not invert \(p=\sinarphi\) where the coordinate derivative degenerates. Within each homogeneity strip only the two threshold cuts are added, and the intersection length with a stable graph is \(O(s)\).

This is the appropriate geometry for the desired weak smallness. It still requires specialist verification that the stable-cone bounds used in the cited multiplier theorem remain uniform in the chosen angle charts through the complete homogeneity decomposition.

### 5.4 Remaining geometric verification obligations

The following details are not contradicted by the text, but are sufficiently load-bearing that they should be checked independently:

- the candidate-center list must be common to the entire radius interval and every allowed finite-horizon flight;
- the level-set partition must have uniformly bounded connected complexity on every homogeneity strip;
- all supporting-line chart cuts must satisfy the precise piecewise-multiplier hypotheses of the cited anisotropic framework;
- the constants must remain uniform when the two parallel layer boundaries coalesce as \(s\downarrow0\);
- matched stable graphs must lose only \(O(\delta)\) length when a transverse boundary moves, including the regime \(s<\delta\);
- the physical multiplication operation on the strong completion must agree with the limiting multiplication of smooth densities.

The manuscript addresses each point in a plausible way, but these are continuum assertions rather than finite symbolic identities.

## 6. The physical thin-layer multiplier

The new proposition states

\[
 \|M_{a_{R,s}}h\|_{\mathcal B}\le C\|h\|_{\mathcal B},
 \qquad
 |M_{a_{R,s}}h|_w\le Cs^{1/8}\|h\|_{\mathcal B},
\]

for both grazing and clearance envelopes.

The proof separates the two assertions correctly. The strong norm is bounded uniformly but is not claimed small. Smallness occurs only in the weak norm through the stable-length normalization. No derivative of an indicator and no inverse layer width is paid. On matched pieces the two indicators agree; unmatched pieces are charged by the graph distance, with the whole strip charged when its width is smaller than that distance.

This is exactly the structural input required for the later interpolation. The argument is not a consequence of the layer's small measure alone. It uses finite boundary complexity, cone transversality, and the specific anisotropic norm.

I found no immediate contradiction in this multiplier proof. However, because the entire revision-49 theorem rests on it, the final version should provide a completely explicit citation-to-hypothesis table for the relevant multiplier lemma, including the treatment of horizontal grazing thresholds and the parameter dependence of the clearance arcs.

## 7. The marked physical-defect local upper bound

For a mark at collision time \(j\), the exact pairing is

\[
 \ell\!\left(\mathscr T_{R,\theta}^{m-j}
       M_{a_{R,s}}
       \mathscr T_{R,\theta}^{j}\nu\right).
\]

At least one chronological block has length at least \(m/2\). On a moving peak chart, the uniform strong multiplier bound and weak \(s^{1/8}\) gain are interpolated to obtain an \(s^{1/16}\) bound on the relevant spectral amplitudes. Expanding the long block gives a principal part of size \(s^{1/16}|\lambda|^{m/2}\) plus an exponentially decaying complementary term. Integration of the four-dimensional Gaussian peak then gives the natural \(m^{-2}\) coefficient scale.

The resulting bound is

\[
\begin{aligned}
 m^2\nu\{&K^{\rm c}_{m,R}=k,A_{m,R}=l,
       S_{m,R}\in J,
       a_{R,s}(T_R^j x)=1\} \\
 &\le Cs^{1/16}(|J|+B_*^{-1})
 +C_{B_*}(1+B_*|J|)m^2\rho_{B_*}^{m/2}.
\end{aligned}
\]

The leading constant is independent of the fixed auxiliary roof band \(B_*\). This independence is essential because \(B_*\) is enlarged only after the collision limit.

The proof retains every occupation resonance and the exact discrete coefficient. The positive Fourier majorant is used only to bound a positive source. There is no cancellation between differently labelled physical words.

The clearance of flight \(j\) is marked at collision \(j+1\), including the terminal mark for flight \(m-1\). The occupation variable remains

\[
 A_m=\sum_{a=0}^{m-1}\eta_R\circ T_R^a;
\]

no terminal section visit is inserted. I found the indexing consistent.

The principal specialist issue is the inherited interpolation lemma: one must verify that its constants are uniform simultaneously in the radius, moving peak chart, mark location, and layer width, including zero-length chronological blocks at the endpoints.

## 8. Summing all physical depths

The physical guard has graded contact and flight margins. If a factor is below one, then the corresponding incidence or clearance width is bounded by

\[
 2\varepsilon q_0^{d/4},
 \qquad q_0=47/53,
\]

with at most two contacts and two flights at each depth. The positive inequality

\[
 1-\prod_i a_i\le\sum_i\mathbf1_{\{a_i<1\}}
\]

therefore gives an upper union of marked physical layers.

Applying the marked local theorem term by term, the leading contributions form the convergent geometric series

\[
 \sum_{a\ge0}
 (2\varepsilon q_0^{a/4})^{1/16}
 <\infty.
\]

There are only \(O(m)\) physical marks. Thus the finite-count errors are summed before taking the collision limit and become

\[
 C_{B_*}(1+B_*h)m^3\rho_{B_*}^{m/2}.
\]

This order is mathematically important. The proof does not take an uncontrolled family of fixed-depth limsups and then sum them. It gives one finite-\(m\) estimate and only afterward lets \(m\to\infty\).

The theorem obtains

\[
\begin{aligned}
 \sup_{R,n,k}m^2
 \|b^{\varepsilon,w}_{n,k,m,R}\|_{1,h}^{\rm loc}
 \le{}& CM\varepsilon^{1/16}(h+B_*^{-1})\\
 &+C_{B_*}M(1+B_*h)m^3\rho_{B_*}^{m/2},
\end{aligned}
\]

for every measurable insertion \(|w|\le M\). The weighted extension uses the pointwise domination of total variation by the unweighted positive source and does not differentiate \(w\).

The first-defect tail receives the expected additional factor \(q_0^{(J+1)/64}\). The proof does not normalize first-defect pieces as separate probability laws.

I found this finite-count summation coherent. Its validity remains contingent on the uniformity of the marked local theorem in the mark and width and on the exact positive source decomposition inherited from module 104.

## 9. The local convolution inequality

For

\[
 \|f\|_{1,h}^{\rm loc}
 =\sup_t\int_t^{t+h}|f(u)|\,du,
\]

Tonelli's theorem gives

\[
 \|K*f\|_{1,h}^{\rm loc}
 \le\|K\|_1\|f\|_{1,h}^{\rm loc}.
\]

No positivity of \(K\) is needed. Since the reconstruction kernels have a scale-invariant \(L^1\) norm, the estimate is uniform in the reconstruction band \(B\).

Consequently the physical source satisfies an all-band signed-correction estimate in local variation. The auxiliary spectral band \(B_*\) and reconstruction band \(B\) remain distinct. The proof first fixes the margin and \(B_*\), takes the collision limsup, and then enlarges \(B_*\). This is not a growing-band spectral argument.

The convolution step is elementary and correct.

## 10. The full-source correction ledger

The exact source identity is

\[
 p^w=f^{\varepsilon,w}
     +d^{\varepsilon,\varepsilon,w}
     +b^{\varepsilon,w},
\]

where

- \(f\) is the smoothly protected source;
- \(d\) is the complete all-depth section-decision source with physical margins protected;
- \(b\) contains every physical incidence or clearance defect, whether or not a later section-decision defect is also present.

For a fixed reconstruction band \(B\), the manuscript chooses

\[
 \varepsilon(B)=A B^{-1/12}.
\]

The inherited protected correction contributes \(O(B^{-1/2})\) after normalization. The all-depth decision correction contributes \(O(\varepsilon^{1/16})\). The new physical theorem contributes the same order in local variation. Hence

\[
 \limsup_{m\to\infty}
 \sup_{R,n,k,w}
 \frac{m^2}{h}
 \|p^w-K_B*p^w\|_{1,h}^{\rm loc}
 \le C(M+L)B^{-1/192}.
\]

The exponent arithmetic is correct:

\[
 (B^{-1/12})^{1/16}=B^{-1/192}.
\]

The order of limits is also correct:

1. fix \(B\) and therefore \(arepsilon(B)\);
2. take the collision limit;
3. enlarge the auxiliary spectral band used only in the physical upper bound;
4. then let the reconstruction band \(B\to\infty\).

No operator estimate is evaluated at a band depending on \(m\).

This theorem is the central achievement of revision 49.

## 11. The full-source local-variation law

At every fixed reconstruction band, the inherited arithmetic fixed-band theorem gives

\[
 \sup_{R,n,k,u}
 \left|m^2(K_B*p_{n,R}(k,m,\cdot))(u)
       -\mathcal L_{m,R}(k_1,k_2,u,n)\right|
 \longrightarrow0.
\]

Integrating this uniform error over a translated interval and adding the full-source correction yields a limsup bounded by \(CB^{-1/192}\). Letting \(B\to\infty\) proves

\[
 \lim_{m\to\infty}\sup_{R,n,k,t}
 \frac1h\int_t^{t+h}
 \left|m^2p_{n,R}(k,m,u)
       -\mathcal L_{m,R}(k_1,k_2,u,n)\right|du=0.
\]

This argument is logically sound provided the inherited fixed-band theorem and the new correction estimate hold. It does not select a pointwise representative of the density.

The theorem is genuinely stronger than convergence against one fixed interval indicator. By \(L^1\)-\(L^\infty\) duality, it is uniform over all measurable selectors supported in the interval. These selectors may depend on the parameters and on \(m\).

At fixed radius and on central compact sets, the finite transition kernel reduces to the arithmetic Gaussian

\[
 c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z(u)),
\]

with the equivalent \(D_R\) return normalization. The arithmetic coefficient is retained rather than assumed equal to one.

## 12. Central mixed-measure total variation

For a fixed return count \(n\) and a bounded central region,

- the collision count has \(O(\sqrt n)\) admissible values;
- the two-dimensional displacement has \(O(n)\) admissible lattice values;
- each roof range has length \(O(\sqrt n)\) and hence requires \(O(\sqrt n)\) unit intervals.

The total number of local unit cells is therefore \(O(n^2)\). On each cell the local-variation theorem gives an error \(m^{-2}e_m\), with \(e_m\to0\) uniformly and \(m\asymp n\). Summing produces \(O(e_m)	o0\).

The positive part of the finite transition kernel is legitimate because, for \(p\ge0\) and real \(L\),

\[
 |m^2p-L_+|\le |m^2p-L|.
\]

The resulting central mixed-measure approximation is therefore in total variation, not merely weak convergence. The counting argument is correct.

## 13. Exact-window conditional roof total variation

On target families for which the positive transition mass on \(I_t=[t,t+h]\) satisfies

\[
 G_{m,R}^{n,k}(I_t)\ge dh,
\]

let

\[
 f=m^2p\mathbf1_{I_t},
 \qquad
 g=(\mathcal L_{m,R})_+\mathbf1_{I_t}.
\]

The local theorem gives \(E=\|f-g\|_1=o(h)\). Since \(|\int f-\int g|\le E\), the true denominator is eventually at least \(dh/2\). The standard normalization estimate then yields

\[
 d_{\rm TV}(f/F,g/G)\le 2E/(dh)\longrightarrow0.
\]

The conditioning event remains exactly

\[
 K_{n,R}=k,\qquad N_{n,R}=m,\qquad T_{n,R}\in[t,t+h].
\]

No substitute section or return-index packet is introduced. The conclusion is a roof-variable conditional law, not a path bridge conditioned at \(T_{n,R}=t\).

## 14. Arithmetic modulation remains intrinsic

Revision 49 does not prove that the concrete section phase masses are uniform. Accordingly, the exact-index main term at fixed radius continues to contain

\[
 \mathfrak a_R(k,n,m),
\]

and the uniform parameter statement continues to use the finite transition kernel

\[
 \mathcal L_{m,R}.
\]

This is mathematically honest. The local-variation theorem is not an unmodulated radius-uniform singleton theorem.

A final theorem may proceed in either of two ways:

1. prove the zero-residue criterion for the concrete section and obtain the unmodulated specialization; or
2. state the arithmetic factor and transition kernel as intrinsic parts of the answer.

Revision 49 follows the second route for the theorem it actually proves. It should preserve that formulation.

## 15. Why local variation is not the pointwise raw theorem

The manuscript draws the correct distinction. A sequence of nonnegative densities can converge in every fixed translated local \(L^1\) window while retaining spikes whose heights diverge and widths vanish. The theorem therefore does not imply

\[
 \sup_{R,n,k,t}
 \left|m^2p_{n,R}(k,m,t)
       -\mathcal L_{m,R}(k_1,k_2,t,n)\right|\to0.
\]

Nor does it prove a uniform essential-supremum estimate for the physical source or its signed reconstruction correction.

The following remain open in the manuscript's own ledger:

- the full pointwise roof-density LLT;
- central-scale essential-height smallness of every physical boundary source;
- pointwise control of narrow grazing and clearance spikes;
- the original full signed pointwise correction;
- a path bridge conditioned at a single roof value;
- and the zero-residue specialization for the concrete section.

The new theorem does imply that the set of roof values on which a fixed-size pointwise error occurs has asymptotically negligible relative Lebesgue measure in every fixed window. This exceptional-set conclusion is useful, but it is not uniform convergence.

## 16. Relation to existing local-limit theory

Classical local-limit results already cover the periodic Lorentz cell process, mixing local limits with endpoint observables in dispersing billiards, and local central limit theorems for broad classes of suspension flows including finite-horizon Sinai billiards. The manuscript itself acknowledges these routes and does not claim that a Gaussian cell local limit, endpoint factor, or suspension step is new in isolation.

Revision 49's more distinctive contribution is the conjunction of

- the actual four-coordinate first-return record;
- exact return and collision indices;
- physical arithmetic residues;
- image-side treatment of grazing and competing-hit layers;
- the all-depth unsmoothed source decomposition;
- and full-source convergence in a translation-bounded local density norm.

This is a meaningful specialist contribution. The paper should sharpen the comparison further by stating theorem by theorem which parts are not consequences of the existing mixing-LLT and suspension frameworks after verification of their hypotheses.

At present the novelty is substantial within the program but still concentrated in one triangular finite-horizon Lorentz family and a very elaborate source-extraction architecture. That level of specialization weighs against the requested four-journal placement unless the pointwise endpoint is completed or the physical-layer method is elevated to a reusable general theorem.

## 17. Presentation and submission architecture

Revision 49 improves the front matter considerably. It presents one new leading theorem and a short proof route, while compiling the eleven previous leading statements in an appendix. This is preferable to placing every historical milestone in the introduction.

The manuscript is nevertheless still extremely large and dependency-heavy. A reader must trust a chain spanning one hundred seven modules, several revisions of raw inversion, two distinct local records, multiple sections, arithmetic resonance analysis, conditional bridges, and a large validation apparatus.

For journal submission, the authors should consider one of two coherent architectures.

### Architecture A: a focused local-variation paper

Make the revision-49 theorem the principal endpoint. State clearly that the topology is the translation-bounded local \(L^1\) norm, include the arithmetic transition kernel in the theorem, and move the unfinished pointwise program and historical derivation ledger to a companion work or technical appendix.

### Architecture B: the complete raw-inversion paper

Retain the current title and architecture only after proving the essential-supremum physical-boundary criterion and the pointwise arithmetic raw-density theorem.

The present manuscript occupies an unstable middle position: it contains a complete and interesting norm theorem but continues to organize a large part of the article around a stronger pointwise endpoint which remains open.

## 18. Independent specialist verification

The new modules require detailed human checking of at least the following points:

1. backward incoming-velocity and arclength conventions;
2. completeness of the finite candidate-center set;
3. the positive lower bound for the perpendicular-foot coordinate;
4. uniform component count of the clearance arcs on every homogeneity strip;
5. stable transversality through grazing;
6. exact hypotheses of the piecewise multiplier theorem;
7. strong-completion multiplication with no inverse-width loss;
8. uniform weak-to-strong interpolation on moving peak charts;
9. treatment of zero-length chronological blocks;
10. all occupation resonances in the marked local estimate;
11. the source domination factor \(1/c\);
12. the collision-\(j+1\) clearance mark and unchanged occupation count;
13. the finite-\(m\) physical-depth sum and its \(m^3\rho^{m/2}\) error;
14. inherited all-depth decision and protected correction estimates;
15. local convolution contraction for the actual reconstruction kernel;
16. order of the collision, auxiliary-band, and reconstruction-band limits;
17. the full-source band-limited arithmetic theorem;
18. and the central mixed-measure counting argument.

The source manifest, finite checks, native build, and rendered theorem pages are not substitutes for this audit.

## 19. Required mathematical revisions for the same benchmark

A future revision seeking the same four-journal benchmark should address the following.

1. **Close the pointwise physical-boundary estimate.**  
   Prove an essential-height or sufficiently strong Fourier-norm bound excluding narrow incidence and clearance spikes at the \(m^{-2}\) scale.

2. **Complete the pointwise arithmetic raw theorem.**  
   Combine the physical estimate with the transition kernel, retaining the arithmetic residue unless it is separately proved trivial.

3. **Resolve the concrete section arithmetic.**  
   Either prove uniform phase masses for the actual section or make the arithmetic modulation part of the final principal theorem.

4. **Obtain independent specialist review.**  
   The thin-layer multiplier, inherited full occupation spectrum, moving spectral peaks, and all-depth source decompositions need expert verification.

5. **Extract a reusable general principle.**  
   Formulate assumptions under which physical singular layers transverse on the image side imply full-source local-variation LLTs for parameterized singular hyperbolic systems.

6. **Clarify the final topology.**  
   Decide whether the paper's endpoint is local \(L^1\), essential supremum, or both, and make the title, abstract, and theorem hierarchy reflect that choice.

7. **Reduce the proof burden.**  
   Separate historical pipeline material from the shortest complete route to the main result.

8. **Strengthen the literature comparison.**  
   Explain precisely which joint-record, parameter-uniform, arithmetic, and unsmoothed-source conclusions are unavailable from the existing billiard and suspension local-limit theorems.

## 20. Technical comments

1. Keep the symbols \(B\) and \(B_*\) visibly distinct in every statement and proof.
2. State explicitly whenever \(B_*\) is enlarged only after the collision limit.
3. Preserve the convention that clearance of flight \(j\) is observed at collision \(j+1\).
4. Keep the occupation sum \(0,\ldots,m-1\) explicit near terminal marks.
5. Record the factor \(1/c\) whenever the initial-section or terminal-section restrictions are dropped on an upper-comparison side.
6. Do not describe the local-variation theorem as a pointwise density theorem.
7. Do not infer an essential-height estimate from the exceptional-roof-set corollary.
8. Keep the positive part in the finite transition reference density at finite count.
9. State the central compact restriction whenever replacing the uniform transition kernel by the fixed-radius arithmetic Gaussian.
10. Preserve the distinction between arbitrary roof selectors and arbitrary trajectory selectors.
11. Keep the exact-window denominator assumption explicit in the conditional roof theorem.
12. Do not assign a conditional law to an arithmetic class with zero transition mass.
13. Explain in one place why the actual previous disk does not make the clearance upper envelope thick.
14. Include a hypothesis table for the cited piecewise multiplier lemma.
15. State how horizontal grazing thresholds interact with the homogeneity partition.
16. Keep the finite-count \(m^3\rho^{m/2}\) physical error distinct from the inherited \(m^4\rho^{m/2}\) section-decision error.
17. Preserve the source-manifest distinction between local-variation closure and pointwise closure.
18. Continue to separate source qualification from continuum proof certification.

## 21. Final assessment

Revision 49 is a serious and constructive response to the revision-48 report.

It provides a credible image-side geometry for actual grazing and clearance layers, proves a width- and mark-uniform local upper bound, sums all physical depths before taking the collision limit, and combines this with the protected and all-depth decision estimates to obtain a full-source \(B^{-1/192}\) correction in local variation.

It then proves a genuine exact-index density theorem for the unmodified original source:

- the finite arithmetic transition kernel is evaluated;
- all exact discrete labels are retained;
- every translated fixed roof window is controlled in absolute density variation;
- every bounded measurable roof selector is allowed;
- the central mixed measure converges in total variation;
- and exact-window conditional roof laws converge in total variation.

I found no decisive error in the new three-module chain within the scope of this review.

The paper nevertheless remains short of the pointwise theorem that still governs its title and retained raw-inversion program. Local \(L^1\) convergence does not exclude narrow physical-boundary spikes, does not prove the essential-supremum correction, and does not yield a path bridge conditioned at one roof value. The concrete arithmetic residues also remain nontrivial unless the section phase masses are separately shown to be uniform.

Subject to independent specialist verification and substantial reorganization, the revision-49 local-variation theorem could anchor a strong specialist paper. It does not yet constitute a complete top-four pointwise raw local inversion theorem, nor has the manuscript established a sufficiently broad general replacement theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**