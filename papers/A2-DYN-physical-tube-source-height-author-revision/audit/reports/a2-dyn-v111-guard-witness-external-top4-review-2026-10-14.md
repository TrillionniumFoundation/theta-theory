# External top-four referee report on A2-DYN revision 111

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v111-guard-witness-referee-response-2026-10-14`, `revision/a2-dyn-v111-guard-witness-referee-copy-2026-10-14`  
**Reviewed author commit:** `8c617cafa5e5493e26817401e866b2415522f7c0`  
**Reviewed repository tree:** `4bca37d3c2939e6e2cf88e3ddacb4cb29b898478`  
**Active manuscript directory:** `papers/A2-DYN-v111-referee-response`  
**Active mathematical source:** 267 numbered core modules in the complete preserved packet; revision 111 adds modules 265--267  
**Immediate mathematical baseline:** revision 110 author commit `0abce3fcfbc735ff5cc6d085279abea5f32a7a22`  
**Frozen revision-110 manuscript tree:** `89ec727b370bf21d66d7086041f75d7868671d4b`  
**Controlling report:** `reviews/a2-dyn-v110-persistent-guard-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling review commit / report blob:** `fb1240d2f8c0562a148d559df5a8d9c3bd2d5e39` / `d57761aeb65b42940a974c8009f13ee47ffd6fce`  
**Exact-SHA qualification observed before this report:** response run `38535355035`, success; referee-copy run `38535364837`, success  
**Date:** 14 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 111 contains genuine new mathematics and responds directly to one of the principal routes identified in the revision-110 report. It does not merely refine another scalar certificate, rename the persistent residual, or multiply a per-itinerary estimate by an uncontrolled number of collision words.

The revision proves three substantive results.

First, for a fixed lifted collision itinerary it proves global injectivity of the map

\[
Q\longmapsto (F(Q),\arg \nabla F(Q))
\]

on the noncritical regular physical trajectories, including trajectories lying in different connected components of the itinerary domain. The argument uses two convex support inequalities for the Cartesian broken-path length. It does not interpolate between the trajectories through a possibly forbidden physical path and does not assume that an angular word domain is convex.

Second, this roof--angle injectivity is combined with the retained stable-Jacobian pressure theorem and the optical comparison

\[
\omega\le C_0c_mJ^sT^m,
\qquad
\frac{J^sT}{c}\le C_1,
\]

to obtain a genuine target-roof physical word sum. For every prescribed set of distinct interior incidence marks \(S\), the revision proves

\[
\left\|
\frac{dF_\#\!\left(\prod_{i\in S}c_i^{-1}\mathbf1_\Pi\nu_R^*\right)}{dt}
\right\|_{L^\infty(dt)}
\le C_\star K_\star^{|S|},
\]

uniformly in the collision count, radius, original exact labels, roof, and marked indices. The proof reconstructs a full word from its unmarked blocks and at most \(|S|\) deleted physical step symbols, so adjacent marks and zero-length blocks are included. This is a weighted pressure sum, not a raw word count.

Third, the revision applies the marked theorem to the actual positive persistent source. It proves that persistent states carrying an incidence witness deeper than an explicit \(O(\log m)\) collision-end layer have zero \(m^2\)-normalized essential height, and that states carrying at least

\[
s_m\asymp \frac{\log m}{\log\log m}
\]

incidence witnesses also have zero normalized height. The witness may depend on the target roof and angle; no single witness is selected for a whole physical segment.

I audited the new modules

- `core/265_global_roof_angle_uniqueness.tex`;
- `core/266_target_roof_marked_pressure.tex`;
- `core/267_uniform_incidence_witness_summation.tex`;

as well as the active article, the revised local explanations in modules 262--263, the response, proof ledger, source manifest, publication-status flags, validation record, the controlling revision-110 report, and the source-pinned historical inputs needed by the new pressure argument.

Within the assumptions actually stated in those files, I found no decisive sign error in the support inequalities, no missing marked stable factor, no evident off-by-one error in the block decomposition, no uncontrolled physical-word multiplier, no invalid positive-source subtraction, no exponent error in the depth or factorial schedules, and no illegal substitution of a collision-dependent width into a theorem stated only at fixed width. The new target-roof summation chain is mathematically coherent relative to its inherited inputs.

The negative recommendation is nevertheless forced by the exact endpoint of the argument. The revised scalar theorem is

\[
\mathcal E_M
\le
\mathcal H_M(\mathsf R_B^{\rm loc})
+C_MB^{-1/384},
\]

where

\[
\mathsf R_B^{\rm loc}
=
\bigl(\mathsf U_B^{\rm loc}-K_BP_{r_B}^{\rm ng}\bigr)_+.
\]

The manuscript proves that the unchanged exact-label raw pointwise assertion is equivalent to

\[
\mathcal H_M(\mathsf R_B^{\rm loc})\longrightarrow0
\qquad\text{for every fixed }M.
\]

**No theorem establishes this limit.**

The remaining source still permits:

- shallow incidence witnesses in the two logarithmic collision-end layers;
- fewer than \(s_m\) incidence witnesses, with no pointwise smallness obtained merely from that number bound;
- clearance witnesses at arbitrary depth, including tangencies to unvisited disks;
- critical entrances and section cuts not paid by the new incidence insertion;
- source on which the full nongrazing comparison pool remains capacity-deficient; and
- any singular endpoint or pairing configuration outside the inherited regular physical-source hypotheses.

The new marked-pressure bound is deliberately unscaled. Its all-incidence consequence is \(O(\varepsilon(B))\), not \(O(m^{-2})\). At fixed outer \(B\), multiplying that bound by \(m^2\) does not make it small. Only the additional depth and factorial factors pay the two classes isolated in revision 111.

Thus revision 111 proves a real target-roof weighted summation theorem and removes nontrivial portions of the persistent source in the correct topology, but the residual in equation `eq:v111-remaining` is still the upper pointwise obstruction itself. It is not a harmless remainder after the organizing local limit theorem.

At the requested benchmark, this is not sufficient for acceptance. A positive recommendation would require closure of the complete localized-shortage estimate, or a reformulation around a complete theorem of independent breadth and significance. Revision 111 supplies neither yet.

## 2. Frozen source and chronology

The two reviewed author branches both resolve to

`8c617cafa5e5493e26817401e866b2415522f7c0`.

The repository tree at that commit is

`4bca37d3c2939e6e2cf88e3ddacb4cb29b898478`.

The active article is

`papers/A2-DYN-v111-referee-response/main.tex`.

The complete revision-110 packet is preserved under

`papers/A2-DYN-v111-referee-response/archive/v110`,

with exact tree

`89ec727b370bf21d66d7086041f75d7868671d4b`.

Revision 111 starts from the revision-110 review commit

`fb1240d2f8c0562a148d559df5a8d9c3bd2d5e39`,

whose parent is the reviewed revision-110 author commit

`0abce3fcfbc735ff5cc6d085279abea5f32a7a22`.

The controlling report identified the persistent guarded shortage as the unresolved positive source and proposed, among other possibilities, a uniform guard-witness summation theorem. Revision 111 establishes the incidence part of that route by a new target-roof pressure theorem. It does not establish the corresponding clearance theorem or the full residual decay.

The active source retains all 264 earlier numbered modules in its historical packet and adds

- `core/265_global_roof_angle_uniqueness.tex`;
- `core/266_target_roof_marked_pressure.tex`;
- `core/267_uniform_incidence_witness_summation.tex`.

Modules 262--263 also contain the presentation clarifications requested in the preceding report: explicit Borel endpoint completion, the positive optical denominator at critical endpoints, the actual surviving coefficient, and the distinction between a changing pointwise witness and a segmentwise witness.

The present review branch starts directly from the exact revision-111 author commit and adds only this report under

`reviews/a2-dyn-v111-guard-witness-external-top4-review-2026-10-14/`.

No author manuscript, author branch, workflow, historical report, archived source tree, or unrelated paper is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v111-source-and-manuscript.yml`.

Both exact-SHA runs completed successfully at the reviewed author commit:

- response branch run `38535355035`;
- referee-copy branch run `38535364837`.

The workflow checks the exact checkout, the original and archived trees, the frozen controlling report, the pinned historical pressure/optical anchors, normal and optimized source diagnostics, active manuscript compilation, reference stabilization, TeX diagnostics, source immutability during the build, and artifact upload.

The author additionally records a 25-page successful local build, rendered-page inspection, exact rational marked-word and witness tests, geometric depth-tail tests, and floating-point physical trajectory diagnostics for the support inequalities.

These are meaningful source, assembly, and reproducibility checks. They do not certify:

1. the original incident-component pairing-sheet construction;
2. the one-copy physical multiplicity convention;
3. the common coarea versions at fixed \(m,R,n,k\);
4. the historical stable-Jacobian pressure theorem and its family-uniform constants;
5. the stable optical comparison on every relevant singularity-free orbit;
6. global validity of the endpoint change of variables on every physical component;
7. the null-set passage for the two-sided regular set under the roof--angle map;
8. collision-uniform summation of clearance witnesses;
9. decay of the localized residual; or
10. the full exact-label raw local limit theorem.

The manuscript correctly distinguishes software qualification from mathematical certification.

## 4. Scope of this review

The substantive audit concentrates on:

1. the two convex support inequalities in module 265;
2. the strict ordering of physical lengths along one endpoint-gradient ray;
3. global roof--angle injectivity across disconnected components;
4. the target-roof change-of-variables formula;
5. removal of several marked stable factors;
6. reconstruction of a physical word from unmarked blocks and deleted symbols;
7. transfer of the uniform pressure bound to a roof fiber;
8. the product and factorial incidence insertions;
9. domination of the persistent coefficient by the original uncut density;
10. the deep-incidence and high-multiplicity schedules;
11. the exact positive source and residual identities;
12. the order of limits; and
13. the exact source classes which remain unproved.

The first 264 historical modules are treated as source-pinned inputs except where they are directly needed to check the new argument. This report does not independently reconstruct the complete spectral, arithmetic, Gaussian, coarea, optical, pressure, and pairing-sheet history of the project.

## 5. The inherited obstruction from revision 110

Revision 110 split the original microscopic paired coefficient into

\[
c^\varepsilon
=
\min\{c^\varepsilon,\gamma_B\mathcal V^\varepsilon\}
+
(c^\varepsilon-\gamma_B\mathcal V^\varepsilon)_+.
\]

The first positive submeasure was paid by the original uncut optical volume. The surviving coefficient

\[
c_{\rm per}^{\varepsilon,\gamma_B}
=
(c^\varepsilon-\gamma_B\mathcal V^\varepsilon)_+
\]

has nearly constant positive density on its entire short physical segment, and the original guard remains active at every roof point.

The remaining shortage was

\[
\mathsf R_B^{\rm per}
=
(\mathsf U_B^{\rm per}-K_BP_{r_B}^{\rm ng})_+.
\]

The revision-110 report emphasized that pointwise existence of an incidence or clearance witness does not itself supply a collision-uniform physical sum. The witness can change with the roof, and multiplying a per-itinerary optical estimate by the number of words would be invalid.

Revision 111 addresses this exact issue for incidence witnesses. The key new ingredient is a multiplicity theorem on the target roof.

## 6. The two-trajectory support inequalities

Fix a lifted itinerary \(w=(O_0,\ldots,O_m)\) and write

\[
S(Q)=\sum_{j=0}^{m-1}|Q_{j+1}-Q_j|.
\]

As a function of the independent Cartesian contacts, \(S\) is convex. At a regular specular trajectory its gradients are

\[
\nabla_0S=-c_0n_0-p_0t_0,
\qquad
\nabla_jS=-2c_jn_j\quad(0<j<m),
\qquad
\nabla_mS=-c_mn_m+p_mt_m.
\]

For two physical trajectories \(Q,\widehat Q\) of the same word, the manuscript sets

\[
b_j=1-n_j\cdot\widehat n_j,
\qquad
s_j=t_j\cdot\widehat n_j,
\qquad
s_E=(s_0,s_m).
\]

Applying the convex support inequality in both directions gives

\[
S(\widehat Q)-S(Q)
\ge
R\sum_{j=0}^m\beta_jc_jb_j+g\cdot s_E,
\]

and

\[
S(Q)-S(\widehat Q)
\ge
R\sum_{j=0}^m\beta_j\widehat c_jb_j-\widehat g\cdot s_E.
\]

The signs of the endpoint tangential terms are consistent with

\[
g=R(-p_0,p_m).
\]

Adding the inequalities gives

\[
(\widehat g-g)\cdot s_E
\ge
R\sum_{j=0}^m\beta_j(c_j+\widehat c_j)b_j.
\]

I find this calculation correct. In particular, no path of physical trajectories between \(Q\) and \(\widehat Q\) is used. The convex function is evaluated at two actual configurations in the ambient Cartesian product, so disconnectedness of the physical word domain is not an obstruction.

This point is a genuine improvement over an argument based only on local implicit continuation.

## 7. Global roof--angle uniqueness

If \(\widehat g=g\), the last inequality forces every \(b_j=0\), since all regular incidences are positive. Hence all normals, contacts, and flight directions agree.

If

\[
\widehat g=\widehat z e,
\qquad
g=ze,
\qquad
\widehat z>z>0,
\]

then the configurations cannot coincide, so at least one \(b_j>0\). The support-sum inequality gives

\[
e\cdot s_E>0.
\]

Substitution into the forward support inequality yields

\[
S(\widehat Q)>S(Q).
\]

Thus, along a fixed endpoint-gradient ray, physical length is strictly increasing in the gradient magnitude. Equal roof and equal Gauss angle therefore imply equal gradient magnitude and then equality of trajectories.

This proves global injectivity of

\[
Q\mapsto(F(Q),\arg g(Q))
\]

on the noncritical regular trajectories of one lifted itinerary, including disconnected physical components and all restrictions imposed by the original exact event.

The proof is concise but sound. The critical case \(g=0\) is not placed inside the angle chart. Instead, equal-gradient uniqueness gives at most one regular critical point per word; because the finite-horizon alphabet gives finitely many words at each finite count, the critical set is collision-area null. This is the correct measure-theoretic role of the critical points.

A specialist should nevertheless verify the endpoint first-variation convention against the collision-coordinate convention used in the historical optical modules. I found no internal mismatch in the active manuscript.

## 8. The bounded roof range

The manuscript also proves

\[
|S(Q)-S(\widehat Q)|
\le |Q_0-\widehat Q_0|+|Q_m-\widehat Q_m|
\le4R
\]

for two regular trajectories of one itinerary.

The argument uses the convex support inequality to show that, with the endpoint contacts fixed, a specular trajectory minimizes the broken-path length over the product of the closed interior scatterer disks. The interior contacts of the second trajectory are then legal competitors, and the endpoint change is paid by the triangle inequality.

This argument does not require the competitor broken path itself to satisfy the original collision event. It is only used in the ambient convex minimization, which is legitimate. The manuscript also correctly states that this range estimate does not control occupation-label variation and is not used to drop the exact occupation test.

## 9. Target-roof change of variables

On each regular component, the map

\[
q\mapsto(F(q),\arg\nabla F(q))
\]

is a local diffeomorphism because the coarea determinant satisfies

\[
\chi\ge\lambda_\circ>0
\]

under the original endpoint section cap. Global injectivity shows that different regular components of one word have disjoint images.

Consequently, for a nonnegative Borel trajectory weight \(a\), the revision obtains

\[
\frac{dF_\#(a\mathbf1_\Pi\nu_R^*)}{dt}(t)
=
\int_0^{2\pi}
\sum_{w\in\mathcal W_m(R)}
\mathbf1_{\{x_w(t,\vartheta)\text{ exists}\}}
\frac{\omega(x_w)a(x_w)}{4\pi c_*\chi(x_w)}
\,d\vartheta.
\]

This is the necessary bridge from a pressure theorem stated over physical words to a pointwise target-roof density.

The passage is plausible and internally consistent. It uses:

- disjoint local charts;
- the new global one-point-per-word theorem;
- the inherited incident-component convention;
- Borel local inverses;
- positivity and Tonelli; and
- null-set passage from the two-sided regular set.

For a final publication version, the exhaustion used for unbounded marked weights should be written more explicitly. In particular, one should first truncate the products of \(c_i^{-1}\), perform the chartwise change of variables, and then use monotone convergence. The current proof states this in compressed form. I do not regard the compression as a demonstrated error, but it is a load-bearing measure-theoretic passage.

## 10. Removal of several stable factors

The new pressure argument uses the inherited estimates

\[
\sup_{R,l}P_l(R)\le Q_*,
\qquad
\omega(x)\le C_0c_m(x)j_m(x),
\qquad
\frac{j(x)}{c(x)}\le C_1.
\]

For a marked set

\[
S=\{i_1<\cdots<i_s\}\subset\{1,\ldots,m-1\},
\]

one obtains

\[
\frac{\omega(x)}{\prod_{i\in S}c_i(x)}
\le
C_0C_1^s
\prod_{v\in\{0,\ldots,m-1\}\setminus S}j(T_R^vx).
\]

The indexing is consistent: a mark at \(i\) removes the stable factor associated with the physical step at that index and pays it by \(j(T_R^ix)/c_i(x)\le C_1\).

Deleting the marked steps breaks the word into \(s+1\) blocks of lengths

\[
i_1,
\quad i_2-i_1-1,
\quad\ldots,
\quad i_s-i_{s-1}-1,
\quad m-i_s-1.
\]

Zero-length blocks are allowed. Together with the \(s\) deleted physical step symbols, the translated block words determine the full lifted word. Since the one-flight physical alphabet has at most \(D\) symbols, this gives at most \(D^s\) choices for the deleted symbols.

Summing the suprema blockwise gives

\[
\sum_w
\frac{\omega(x_w)}{\prod_{i\in S}c_i(x_w)}
\le
C_0C_1^sD^sQ_*^{s+1}.
\]

This is the right type of argument. It handles adjacent marks and does not count homogeneity strips at the removed incidences.

The conclusion remains relative to the inherited uniform pressure theorem. That theorem is one of the most load-bearing historical inputs in the project and has not been independently re-proved in this report.

## 11. Target-roof marked pressure

Using one point per word at an almost-everywhere target \((t,\vartheta)\), the manuscript combines the selected-word sum with

\[
\chi\ge\lambda_\circ
\]

and integrates over an angular interval of length \(2\pi\). With

\[
C_\star=\frac{C_0Q_*}{2c_*\lambda_\circ},
\qquad
K_\star=C_1DQ_*,
\]

this yields

\[
\|d_S\|_\infty
\le C_\star K_\star^{|S|}.
\]

The constants and the factor \(2\pi/(4\pi c_*\lambda_\circ)\) are consistent.

Expanding the positive product

\[
\prod_{i=1}^{m-1}(1+a_i/c_i)
\]

over distinct marked sets gives

\[
\|d_{\boldsymbol a}\|_\infty
\le
C_\star\prod_{i=1}^{m-1}(1+K_\star a_i)
\le
C_\star\exp\!\left(K_\star\sum_i a_i\right).
\]

The inherited linear insertion

\[
I_m=1+\sum_{i=1}^{m-1}q_0^{d_i}/c_i
\]

then has a collision-uniform unscaled roof-density bound because

\[
\sum_iq_0^{d_i}\le\frac{2q_0}{1-q_0}.
\]

The manuscript is correct not to attach an \(m^{-2}\) gain to this theorem. The exact occupation and displacement labels remain on the source side; dropping their tests in the positive upper sum does not create a local-limit factor.

## 12. Changing incidence witnesses

Let

\[
N_J=\sum_{i\in J}\mathbf1_{\{c_i<\eta_i\}}.
\]

The elementary inequality

\[
\mathbf1_{\{N_J\ge s\}}
\le
{N_J\choose s}
\le
\sum_{\substack{S\subset J\\|S|=s}}
\prod_{i\in S}\frac{\eta_i}{c_i}
\]

is valid pointwise. Pushing it through the original roof measure and applying the marked theorem gives

\[
\left\|
\frac{dF_\#(\mathbf1_{\{N_J\ge s\}}\mathbf1_\Pi\nu_R^*)}{dt}
\right\|_\infty
\le
C_\star K_\star^s e_s((\eta_i)_{i\in J})
\le
C_\star\frac{(K_\star A_J)^s}{s!}.
\]

This correctly handles a witness which changes with the target roof and angle. It avoids a measurable selection of one witness on an entire segment and introduces no factor equal to the number of possible witness indices.

## 13. Domination of the persistent source

The surviving coefficient is

\[
c_{\rm per}^{\varepsilon,\gamma}
=(c^\varepsilon-\gamma\mathcal V^\varepsilon)_+.
\]

At every point of its closed segment, total variation gives

\[
f^\varepsilon(u,\theta)
\ge c^\varepsilon-\mathcal V^\varepsilon.
\]

For \(\gamma\ge1\), this implies

\[
0\le c_{\rm per}^{\varepsilon,\gamma}
\le f^\varepsilon(u,\theta)
\le A(u,\theta).
\]

Thus a target-dependent Borel restriction of the persistent paired source is bounded by the corresponding restriction of the original uncut roof measure. This is the correct bridge to the target-roof marked theorem. The proof uses the actual surviving coefficient, not the original endpoint minimum.

## 14. Deep incidence witnesses

The original guard supplies incidence thresholds

\[
\eta_i^\varepsilon
=2\varepsilon q_0^{d_i/4},
\qquad
d_i=\min(i,m-i).
\]

There are at most two indices at each depth, so

\[
\sum_{d_i\ge L}\eta_i^\varepsilon
\le
\frac{4\varepsilon q_0^{L/4}}{1-q_0^{1/4}}.
\]

Applying the witness theorem with \(s=1\) gives

\[
\|\mathsf U_B^{\rm per}[\cup_{d_i\ge L}E_i]\|_\infty
\le
C\varepsilon(B)q_0^{L/4}.
\]

The choice

\[
L_m=
\left\lceil
\frac{4(2+\eta)}{|\log q_0|}\log(m+1)
\right\rceil
\]

then yields

\[
m^2
\|\mathsf U_B^{\rm per}[\mathcal D_{B,m}]\|_\infty
\le
C\varepsilon(B)(m+1)^{-\eta}.
\]

This calculation is correct. The depth threshold is substituted into an inequality already proved for every finite \(m\) and every \(L\). It is not an outer Fourier, roof, or residence width and therefore does not violate the prescribed limit order.

## 15. Numerous incidence witnesses

The total threshold sum satisfies

\[
A_\varepsilon
\le
\frac{4\varepsilon q_0^{1/4}}{1-q_0^{1/4}}.
\]

For fixed outer \(B\), the quantity

\[
a=K_\star A_{\varepsilon(B)}
\]

is finite. Taking

\[
s_m=
\left\lceil
\frac{4\log(m+e)}{\log\log(m+e^e)}
\right\rceil
\]

and using \(s!\ge(s/e)^s\) gives

\[
m^2\frac{a^{s_m}}{s_m!}
=
\exp\{2\log m+s_m(1+\log a-\log s_m)\}
=
m^{-2+o(1)}\to0.
\]

The asymptotics

\[
s_m\log s_m=(4+o(1))\log m,
\qquad
s_m=o(\log m)
\]

are consistent. If \(s_m>m-1\), the event is empty.

Thus the high-multiplicity payment is valid for every fixed outer \(B\). Again, it does not claim uniformity after interchanging \(B\) with the collision limit.

## 16. Exact source preservation and residual comparison

Revision 111 defines

\[
\mathsf U_B^{\rm exc}
=
\mathsf U_B^{\rm per}[\mathcal Z_{B,m}],
\qquad
\mathsf U_B^{\rm loc}
=
\mathsf U_B^{\rm per}[\mathcal Z_{B,m}^c].
\]

At finite count,

\[
\mathsf U_B^{\rm per}
=
\mathsf U_B^{\rm exc}
+
\mathsf U_B^{\rm loc}
\]

is an identity of nonnegative original submeasures. No coefficient is discarded.

With the unchanged full nongrazing pool,

\[
\mathsf R_B^{\rm loc}
=
(\mathsf U_B^{\rm loc}-K_BP_{r_B}^{\rm ng})_+.
\]

Since the positive-part map is increasing and one-Lipschitz,

\[
0\le
\mathsf R_B^{\rm per}-\mathsf R_B^{\rm loc}
\le
\mathsf U_B^{\rm exc}.
\]

The excluded source has zero collision-normalized height for every fixed \(B\), so

\[
\mathcal H_M(
\mathsf R_B^{\rm per}-\mathsf R_B^{\rm loc})=0.
\]

Combining this with the revision-110 scalar theorem gives

\[
\mathcal E_M
\le
\mathcal H_M(\mathsf R_B^{\rm loc})
+C_MB^{-1/384}.
\]

The necessity direction is also correctly retained because

\[
0\le\mathsf R_B^{\rm loc}
\le\mathsf U_B^{\rm micro}.
\]

## 17. The decisive remaining obstruction

The exact remaining estimate is

\[
\lim_{B\to\infty}
\limsup_{m\to\infty}
\sup_{R,n,k}m^2
\esssup_{t\in\mathcal C_{m,R,n,k}(M)}
(\mathsf U_{B,m}^{\rm loc}(t)-K_BP_{r_B,m}^{\rm ng}(t))_+
=0.
\]

Revision 111 does not prove this statement.

The retained incidence information is limited to:

1. every incidence witness lies at depth \(<L_m=O(\log m)\);
2. fewer than \(s_m=O(\log m/\log\log m)\) incidence witnesses occur; and
3. the original persistent density is nearly constant on its short physical segment.

None of these facts supplies an \(m^{-2}\) pointwise gain for the retained source.

The clearance alternative remains even less controlled. A clearance witness can occur at any flight and can arise from tangency to an unvisited disk. It is not represented by an inverse visited-incidence factor \(c_i^{-1}\), so the marked stable-factor theorem cannot be applied to it by a change of notation.

The full nongrazing pool may still have insufficient capacity at the prescribed outer width. The new pressure theorem controls an unconditioned target-roof sum; it does not prove that this capacity dominates the persistent source on the central exact-label roof set.

The remaining source also retains any critical entrance, section cut, singular endpoint extension, or physical pairing configuration which is not covered by the inherited regular source and the proved payments.

This is the exact point at which the manuscript's organizing theorem remains incomplete.

## 18. Why the unscaled incidence theorem is not enough

The target-roof theorem with one incidence mark gives an upper bound of order

\[
C\eta_i.
\]

Summing all original incidence thresholds gives \(C\varepsilon(B)\), uniformly in \(m\). This is a useful finite-count pointwise bound, but at fixed \(B\)

\[
m^2C\varepsilon(B)
\]

does not tend to zero.

The deep and numerous classes vanish only because they carry, respectively,

- an additional factor \(q_0^{L_m/4}\lesssim m^{-2-\eta}\); or
- a factorial factor \(1/s_m!\) strong enough to beat \(m^2\).

The retained shallow, low-multiplicity incidence class has neither factor. Any future argument must obtain a new geometric, probabilistic, or capacity gain; the present pressure theorem alone cannot close it.

## 19. What a decisive next revision must prove

A revision capable of changing the recommendation must establish the complete remaining localized-shortage limit. Several routes appear logically possible.

### Route A: clearance-witness pressure

Construct a positive marked expansion for third-disk clearance witnesses, including unvisited tangencies, and prove a target-roof weighted sum with constants compatible with the collision normalization. This requires a genuine geometric mark; a clearance cannot simply be renamed as a visited incidence.

### Route B: shallow-incidence scarcity

Prove that the persistent source with fewer than \(s_m\) incidence witnesses, all confined to the two \(L_m\)-deep end layers, has vanishing ordered height. Such a theorem may require a boundary-layer pressure improvement, a packing theorem, or a coupling to the fixed-window nongrazing capacity.

### Route C: capacity abundance

Show directly that the full nongrazing pool pays the localized persistent source at the prescribed collision-independent window, up to a positive remainder of vanishing ordered height.

### Route D: direct microscopic insertion

Establish an inverse-residence, logarithmic, or another source insertion on the remaining original positive measure, with constants uniform in collision count, radius, labels, and the outer stage.

### Route E: a hybrid decomposition

Separate shallow incidence, clearance, critical, section-boundary, and capacity-deficient mechanisms into positive original submeasures and prove a normalized estimate for every part.

Every valid route must preserve the existing order of limits:

1. fix \(B\) and all outer widths and costs;
2. prove the finite-count positive identities;
3. complete the physical sum;
4. take the exact-label, radius, and essential-roof suprema;
5. take the collision limsup; and
6. send \(B\to\infty\) last.

## 20. Specialist audit obligations

Even apart from the unproved final limit, the following passages require independent specialist reconstruction before publication:

1. the original incident-component pairing-sheet construction;
2. one-copy physical multiplicity after all seams and endpoint mechanisms;
3. the endpoint action and first-variation sign conventions;
4. global roof--angle injectivity on every claimed physical word domain;
5. the local change of variables and null-set passage for the two-sided regular set;
6. the historical uniform pressure theorem \(\sup_{R,l}P_l(R)\le Q_*\);
7. the stable optical comparison \(\omega\le C_0c_mj_m\);
8. the one-step factor removal \(j/c\le C_1\);
9. reconstruction of words from translated blocks and deleted symbols;
10. the endpoint trace and total-variation completion used to dominate the persistent coefficient;
11. the fixed-window paired and uncut-volume inputs; and
12. the inherited scalar equivalence linking microscopic-source decay to the raw pointwise theorem.

The exact and floating-point diagnostics do not certify these continuum statements.

## 21. Presentation and technical requests

The 25-page active article is considerably more readable than the historical archive. The following changes would improve a later submission.

1. State the complete main theorem status at the beginning of the introduction: the global uniqueness theorem, target-roof marked pressure theorem, and two normalized incidence payments are proved; the raw pointwise LLT and equation `eq:v111-remaining` are not.

2. Promote the source-pinned pressure theorem and stable optical comparison to an explicit input theorem in the active article, with their exact hypotheses and conventions. At present they are stated in module 266, but their historical proof boundary remains easy to miss.

3. Expand the truncation and monotone-exhaustion argument for the unbounded weights \(\prod c_i^{-1}\) in the target-roof change of variables.

4. Add a short indexing diagram for the block decomposition in Lemma 10.1, especially for adjacent marks and marks at \(1\) and \(m-1\).

5. Keep the distinction between an unscaled \(O(1)\) roof-density theorem and an \(m^{-2}\)-normalized local-limit estimate in every summary statement.

6. Keep incidence and clearance witnesses in separate notation throughout. The current revision does this correctly; it should not be weakened in a later version.

7. Record the successful v111 paired workflow runs in a versioned provenance file without rewriting the source packet's pre-run statement.

8. Do not describe the remaining source merely as localized without immediately stating that only incidence witnesses are localized; clearance witnesses remain at arbitrary depth.

These requests are secondary to the missing localized-shortage theorem.

## 22. Significance at the requested benchmark

The new results are mathematically meaningful.

The global roof--angle uniqueness theorem is a clean geometric statement that resolves a real multiplicity problem. The target-roof marked pressure theorem is substantially stronger than the preceding per-itinerary optical polynomial. It supplies a complete physical sum and may be useful in other local inversion questions for finite-horizon dispersing billiards.

The incidence-witness application also demonstrates that the theorem is not merely formal: it removes collision-deep and high-multiplicity positive source classes in exactly the \(m^2\)-normalized essential-height topology required by the paper.

Nevertheless, the present manuscript remains organized around a raw four-record pointwise local limit theorem which is not proved. The new theorems are specialized components inside that unfinished program and depend on a long source-pinned chain of billiard-specific optical, pressure, coarea, and spectral inputs.

For a top-four mathematics journal, either the organizing theorem must be completed, or the new roof--angle/marked-pressure mechanism must be extracted as a broader theorem with independently significant applications. In its present form, neither condition is met.

The work may already contain the core of a strong specialist paper after independent verification and substantial reorganization, but that is a different editorial judgment from the requested top-four benchmark.

## 23. Final recommendation

**Reject in the present form at the requested top-four benchmark.**

This recommendation is not based on a finding that revision 111 is empty or internally inconsistent. The new global uniqueness and target-roof summation arguments are genuine advances, and I found no decisive contradiction in the newly audited finite-count chain relative to its inherited inputs.

The recommendation follows because the manuscript itself proves that its organizing exact-label raw pointwise theorem is equivalent to a localized positive-shortage estimate which remains unproved. Until shallow incidence, clearance, critical/section mechanisms, and capacity deficiencies are all paid in the collision-normalized essential-height topology, the principal result has not been established.

---

### Status boundary

This document is an author-requested, AI-assisted referee-style assessment of the identified Git objects. It is not a commissioned report from *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or the *Journal of the American Mathematical Society*; it is not an editorial decision; it is not an independent human specialist audit; and it is not a formal proof certificate.