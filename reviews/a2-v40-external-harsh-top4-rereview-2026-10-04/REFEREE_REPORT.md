# External top-four referee report on A2 v40

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v40-joint-response-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v40-referee-copy-2026-10-04`  
**Reviewed commit:** `c5593b05546889f436ce858c327670d080aae204`  
**Reviewed repository tree:** `1e794c5161114d34a4d46e6e5b5cb50567dfc731`  
**Controlling preceding review:** `790654161f2f069fb4d1d1ee18bfe86ea5290d74`  
**Manuscript directory:** `papers/A2-v40-joint-response`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation: major revision, with reconsideration at the requested benchmark.**

This is a materially more favorable assessment than my report on v39. Version 40 answers the central information-model objection rather than merely changing notation. Its principal exact theorem uses only two fixed opposite forward commands, at one fixed positive length and under one unknown stationary launch law. The data are the resulting two spatial mean fields on the plane. There is no angular sweep, no limit of command lengths to zero, no second launch setting, no homothety relation, and no separately supplied reciprocal experiment.

From these two fields the manuscript recovers, up to one unavoidable common translation, an arbitrary locally finite separated configuration of strictly convex planar obstacles and an arbitrary compactly supported launch probability with convex support. The law may be atomic, singular, or supported on a lower-dimensional convex set. Exact recovery requires only

\[
        t+\operatorname{diam}A<d,
\]

where `d` is the obstacle separation. Boundary smoothness, positive curvature, periodicity, a lower obstacle-width bound, and density regularity are absent from the exact theorem.

The proof has a clean collision-specific core. A finite prefix identity recovers the occupation. The supports of that occupation and the two collision fields give three observable support functions in which the unknown footprint cancels. The remaining function is the support difference between the obstacle and a transverse contact chord. Strict convexity makes the obstacle surface-area measure nonatomic, whereas the chord contributes two negative atoms. The Jordan decomposition recovers the chord and then the obstacle. One compact occupation component then recovers the complete launch law by exact convolution factorization. The common-translation fiber, the full period group, and every finite-length forward response follow.

I found no fatal counterexample in this exact chain. The finite geometric theorem, finite probability recovery in `W_1`, and response-prediction corollaries are also coherent at the level audited. The exact-SHA workflow qualifies both the focused primary article and the retained technical companion.

The manuscript has therefore crossed the threshold at which a top-four submission deserves substantive reconsideration rather than an editorial rejection based on the old angular-continuum or multi-setting data. I am not yet recommending acceptance. Several load-bearing continuum arguments require a fresh human proof review, the closest blind-factorization literature needs a stronger theorem-level comparison, and the relationship between the 23-page primary and the 85-page companion should be made journal-ready. These are major-revision issues, not a demand for another unrelated theorem.

## 2. Frozen source and revision chronology

Both v40 revision names resolve to the same author commit

`c5593b05546889f436ce858c327670d080aae204`

with repository tree

`1e794c5161114d34a4d46e6e5b5cb50567dfc731`.

The parent is the completed v39 review commit

`790654161f2f069fb4d1d1ee18bfe86ea5290d74`,

which reviewed v39 author source

`f815a7acdb5c03e03b9996fc7052b405db66936d`.

No A2 revision branch later than v40 existed when this report was frozen. The review branch starts directly from the v40 author head and adds files only under

`reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author branch, workflow, prior report, retained paper, or unrelated path is modified.

The submission now consists of two separately compiled documents:

1. `main.tex`, a focused primary containing the new two-field exact inverse, finite geometry, finite law recovery, and prediction;
2. `companion.tex`, retaining the complete earlier A2 programme and all reviewed v39 proof bodies.

The genuinely new mathematical inputs are principally:

- `core/00j_two_field_introduction.tex`;
- `core/21_two_field_rigidity.tex`;
- `core/22_two_field_finite.tex`;
- `core/23_two_field_law.tex`.

## 3. Data and theorem package

Fix one vector `a=te`, with `t>0`, and one unknown stationary probability `mu`. The only two commanded displacements are `a` and `-a`. At nominal center `x`, the hidden start is `x+Z`, and the observed means are

\[
 F_+(x)=\int B_a(x+z)\,d\mu(z),
 \qquad
 F_-(x)=\int B_{-a}(x+z)\,d\mu(z).
\]

A bit is one exactly when a free start has a first collision on the prescribed unreflected segment. Solid starts and free misses both return zero and remain in the denominator. The exact datum is the ordered pair of whole-plane spatial fields `(F_+,F_-)`; it is not two scalar numbers.

The current primary has three mathematical layers.

1. **Exact joint rigidity.** The two fields determine the obstacle configuration, footprint, and probability law up to common translation, as well as the full period group and all other forward responses.
2. **Finite geometry.** On quantitative smooth periodic classes, the same two fixed commands reconstruct the centered footprint and table in `C^2`, with explicit attempted-bit, site, command, and coordinate-precision bounds.
3. **Finite law and prediction.** The same experiment recovers the launch probability in transportation distance, predicts every bounded-length response in local spatial mean, and, under an additional `BV` density prior, recovers the density in `L^1` and predicts raw means uniformly on bounded windows.

These layers have different hypotheses and stability conclusions. The manuscript generally distinguishes them correctly.

## 4. Audit of the finite-prefix occupation inverse

The pointwise endpoint identity is

\[
 B_a(y)-B_{-a}(y+a)
       =\mathbf 1_{\mathcal O}(y+a)-\mathbf 1_{\mathcal O}(y).
\]

It remains valid under the manuscript's closed-solid convention, including atomic laws that charge boundary configurations. Integrating against the same stationary law gives

\[
 r(x):=F_+(x)-F_-(x+a)=v(x+a)-v(x).
\]

Put

\[
 M=\left\lfloor\frac{D+\Delta}{t}\right\rfloor+1.
\]

The occupation is recovered by

\[
 v(x)=\max_{0\le m\le M}
       \left\{-\sum_{k=0}^{m-1}r(x+ka)\right\}.
\]

Every prefix equals `v(x)-v(x+ma)` and is at most `v(x)`. If `v(x)>0`, the arithmetic progression exits the containing expanded component within `M` steps because that component has diameter at most `D+Delta`. The next point cannot lie in another component because the component gap exceeds `t`. At that point the occupation is zero, so one prefix attains equality.

The stability estimate is immediate: an error `epsilon` in each value of `r` changes every prefix by at most `M epsilon`; errors `epsilon` in both raw fields give `2M epsilon`. I found this argument correct, including the possibility that occupation is nonzero on the boundary of an expanded component: the attaining index is the first point outside the closed component, not merely a boundary point.

## 5. Audit of collision supports and footprint cancellation

For each obstacle `C`, the support of the occupation contribution is

\[
 P_C=C+(-A).
\]

The supports of the positive and negative collision fields are the incoming collision strips, thickened by the same unknown reflected footprint. Within each sign, distinct components remain separated by at least `d-Delta-t`. Each collision component meets its own `P_C` and no other occupation component. Hence the three support components can be matched from the observed fields without supplied obstacle labels.

For the matched components, the manuscript proves

\[
 h_{K_+}=h_{\Gamma_+}+h_{-A}+t(-u\cdot e)_+,
 \qquad
 h_{K_-}=h_{\Gamma_-}+h_{-A}+t(u\cdot e)_+.
\]

The two incoming arcs satisfy

\[
 h_{\Gamma_+}+h_{\Gamma_-}=h_C+h_{L_C},
\]

where `L_C` is the chord joining the two contact points with normals `e^perp` and `-e^perp`. Consequently the observable combination

\[
 H_C(u)=2h_{P_C}(u)-h_{K_+}(u)-h_{K_-}(u)+t|u\cdot e|
\]

obeys the exact cancellation

\[
                         H_C=h_C-h_{L_C}.
\]

This is the conceptual heart of v40. The unknown footprint cancels before any geometric differentiation is taken. I checked the hemisphere cases and finite models independently and found no missing support term or sign error.

## 6. Audit of the signed curvature measure

Let the chord have length `ell` and normal directions `n,-n`. In planar support coordinates,

\[
  (\partial_\phi^2+1)H_C
     =\mathsf S_C-\ell(\delta_n+\delta_{-n}).
\]

For a strictly convex planar body, the surface-area measure has no atoms: atoms correspond to exposed boundary segments. The chord contributes exactly two negative atoms of mass `ell`. Thus the positive and negative parts of this signed measure are mutually singular. The negative part determines the centered chord, and

\[
                  H_C+h_{L_C^0}
\]

is the support function of the obstacle translated by the chord midpoint. Steiner centering then gives the obstacle shape canonically.

This argument legitimately permits nonsmooth strictly convex bodies and singular-continuous curvature measure. It does not require identifying the positive part with a smooth curvature-radius density. The points deserving the most careful human verification are:

- the arc-support identity at nonsmooth strict-convex boundary points;
- the statement that the observed field supports have exactly the asserted connected components for arbitrary singular launch laws;
- the Jordan-decomposition step in the chosen support-function conventions.

I found these steps consistent, but they carry the main continuum burden and should not be delegated to finite diagnostics.

## 7. Recovery of the canonical geometry and launch law

Once the centered obstacle shape has been recovered, the Steiner point of `P_C` places it in the canonical frame:

\[
 C_P^0=(C-s(C))+s(P_C)=C-s(A).
\]

Support subtraction yields the common centered footprint

\[
 h_{-A_0}=h_{P_C}-h_{C_P^0}.
\]

The reconstructed table is therefore `O-s(A)`.

For one isolated occupation component,

\[
 v_P=\mathbf 1_{C_P^0}*\check\mu_0.
\]

The Fourier transform of the recovered compact obstacle indicator is entire and nonzero at the origin. Its real zero set has empty interior. Hence on a dense set

\[
 \widehat\mu_0(-\xi)
 =\frac{\widehat v_P(\xi)}
        {\widehat{\mathbf 1_{C_P^0}}(\xi)}.
\]

Continuity determines the characteristic function at the zeros, and Fourier uniqueness determines the compact probability measure. This is an exact uniqueness argument, not a stable division theorem. The finite section correctly avoids claiming stability through the Fourier zeros and instead uses finite moments.

The complete fiber is one common translation of the table and law. The recovered canonical triple also determines every other finite-length forward response. A period of the two fields is a period of the recovered occupation components and hence of the obstacle configuration; the converse follows from translation covariance. I found these conclusions sound.

## 8. The one-orientation obstruction

The final exact proposition constructs distinct smooth strictly convex bodies with the same forward responses in one fixed orientation for every positive command length. The incoming arc is held fixed while the outgoing arc is perturbed. This is a useful and honest negative result: one orientation, even with all lengths, is not sufficient.

It should not be overstated as a universal information-theoretic minimality theorem for every conceivable single-field experiment. It establishes the necessity of additional directional information in the stated fixed-orientation family, and it explains why the pair `a,-a` is structurally natural.

## 9. Audit of finite geometric reconstruction

The finite theorem uses stronger quantitative assumptions: `C^{6,beta}` obstacle and footprint supports, positive curvature margins, a boundary-mass lower bound

\[
 j(z)\ge b_0\operatorname{dist}(z,\partial A)^\gamma,
\]

and the stronger separation `2t+Delta<d_0`. The flight length and the two directions remain fixed as accuracy increases.

The proof has three main stages.

1. The prefix inverse supplies finite occupation queries and coarse expanded components. A two-direction rare test works even when the expanded-boundary normal is nearly perpendicular to the command direction. An outer tangent disk keeps the shifted starts free; outside points force one candidate to miss, while an inner point has collision probability bounded below by the footprint cap mass.
2. Positive nominal centers are used to approximate the convex hulls of the two collision supports. Each support cap receives probability at least `c epsilon^(gamma+9/2)`: `epsilon^3` comes from the collision strip and `epsilon^(gamma+3/2)` from the footprint cap. A rational-grid quadrature argument is uniform in the hidden launch displacement and uses no density modulus.
3. The negative curvature atoms are extracted stably from an `L^infinity` approximation of `H_C`. A sine second difference locates the atom, a signed plateau with vanishing moments estimates its mass, and support smoothing yields `C^2` obstacle error.

With `s=6+beta`, the sufficient power is

\[
 Q_{\rm pair}=\frac{(\gamma+9/2)s}{s-2},
\]

and

\[
 N_\nu\le C\nu^{-Q_{\rm pair}}
       \log(C/\nu)\log(C/(\nu\delta)).
\]

At `gamma=0`, `s=7`, the power is `6.3`, one third of the v39 sufficient power `18.9`. I found the exponent balance and the support-error conversion coherent. No optimality is proved, and none should be implied.

The delicate finite points are the uniform strip-ball lower bound at tangencies, the assignment of positive records to obstacles, the complete-component cutoff, and the signed moment construction used for chord length. These merit line-by-line human checking.

## 10. Audit of finite law recovery and prediction

Normalize one isolated occupation component. It is the law of `X-Z`, where `X` is uniform on the recovered obstacle and `Z` has the unknown canonical launch law. The manuscript acquires all mixed moments through degree `4m` from shared prefix queries on a rational grid.

The triangular moment identity gives an explicit conditioning bound of factorial type. Tensor polynomial approximation of Lipschitz functions then yields

\[
 W_1(\mathcal L(Z),\mathcal L(\widetilde Z))
       \le C/m+a(Cm)^{Cm}.
\]

A finite rational linear programme returns a positive atomic law. Taking `m` of order `epsilon^{-1}` and moment tolerance of order `exp[-C m log m]` gives the sufficient attempted-bit bound

\[
 \exp\!\left(C\varepsilon^{-1}
          \log(C/\varepsilon)\right)\log^2(C/\delta).
\]

This cost is enormous but explicit, and the manuscript does not claim minimax sharpness. Arithmetic complexity and output size are separated from attempted-bit cost.

The resulting `W_1` estimate and geometric estimate imply prediction of every bounded-length response in local spatial `L^1`, by convex symmetric-difference bounds and the translation inequality for finite-perimeter indicators. This is the correct weak norm for arbitrary singular launch laws.

Under the additional prior that the zero-extended density has bounded variation, smoothing a more accurate probability estimate gives `L^1` density recovery and uniform raw-response prediction on bounded windows. The stronger cost replaces `epsilon^{-1}` by `epsilon^{-2}` in the exponential. The extra `BV` hypothesis is necessary for these strong conclusions and is stated explicitly.

## 11. Major revisions required before acceptance

### 11.1 Strengthen the closest-prior-work comparison

The literature audit is thoughtful, but the exact theorem now warrants a more systematic theorem-level comparison with:

- blind geometric deconvolution and unknown-probe morphology;
- joint support-and-distribution inference with unknown noise;
- signed Minkowski differences and uniqueness from signed surface-area measures;
- compact deconvolution in the presence of Fourier zeros.

The paper should say precisely which hypotheses and conclusions are new, and which parts are classical after the observable support identity is obtained. An exhaustive priority claim is unnecessary, but the present theorem is strong enough that a broader search is required before publication at this level.

### 11.2 Make the singular-law support argument fully self-contained

The exact theorem permits atomic and lower-dimensional launch laws. The proof should isolate, as a standalone lemma, the following assertions with all measure-support conventions explicit:

- support of the occupation convolution is `C+(-A)`;
- support of each collision convolution is the collision strip plus `-A`;
- connected-component matching remains valid for singular measures;
- equality almost everywhere determines the same measure supports and period group.

The present argument appears correct, but these claims are sufficiently load-bearing to deserve a visibly self-contained statement.

### 11.3 Expand the nonsmooth strict-convex curvature argument

The primary should explicitly state the standard equivalence between atoms of the planar surface-area measure and exposed boundary segments, and explain why strict convexity excludes those atoms even when the boundary has corners or singular curvature. The support-arc identity should be written in a form that does not tacitly assume differentiability of the obstacle boundary.

### 11.4 Separate exact uniqueness from finite stability

The Fourier quotient is an exact uniqueness argument and may be arbitrarily ill-conditioned near its zeros. The finite law theorem uses a different moment mechanism with exponential conditioning. This distinction is already present, but it should be emphasized in the theorem roadmap and abstract discussion so that exact response completion is not read as a finite-cost extrapolation theorem.

### 11.5 Clarify the primary/companion dependency contract

The 23-page primary is a major editorial improvement. Nevertheless, the finite geometry proof invokes cap-mass, radial interpolation, support smoothing, and period-locking results from the 85-page companion. The final journal package should provide a concise dependency table in the primary and ensure that every cited companion result has a stable statement and hypothesis visible to a reader who does not reconstruct the revision history.

The editor may prefer either a true supplement with a frozen theorem interface or two separately citable papers. The present cross-reference mechanism is reproducible, but mathematical readability, not merely source preservation, should determine the final form.

### 11.6 State resource exclusions next to the main finite theorem

The theorem counts attempted bits, command occurrences, distinct nominal sites, coordinate-description length, and output representation. It does not price physical movement, apparatus calibration, realization of the fine grid, or linear-program arithmetic. These distinctions should remain in the theorem statement rather than only in later discussion.

### 11.7 Obtain an independent specialist proof review

The repository evidence is unusually strong, but finite diagnostics do not certify the continuum arguments. At minimum, a human expert should independently audit:

- the singular-law support decomposition;
- the arc-support cancellation and negative-atom extraction;
- the tangential rare-test geometry;
- the cap-probability and rational-grid hull acquisition;
- the moment-factor perturbation and positive finite-law reconstruction.

## 12. Significance at the requested benchmark

Version 40 materially changes the editorial balance. The command alphabet has been reduced from an angular continuum and a short-length limit to two fixed vectors of one positive length. The exact class is broader: nonsmooth strict convexity and arbitrary compact probabilities are allowed. The proof is organized around one new support identity, and the primary article has been reduced to a focused theorem chain.

The data are still two complete active fields on the plane, so the theorem is not a rigidity result from a passive marked length spectrum, scattering relation, count germ, or orbit law. Nevertheless, complete operator- or field-valued data are standard in inverse problems, and the literal two-command reduction is mathematically meaningful. The observable cancellation, negative-atom recovery, and joint law/table factorization form a coherent principle rather than an accumulation of unrelated estimates.

I therefore no longer regard the old information-model objection, by itself, as sufficient for rejection. If the exact theorem survives an independent proof audit and the literature comparison confirms the claimed novelty, the paper is plausibly competitive for at least the broad end of the requested benchmark. The finite results strengthen the package but are not what carries the top-four case; their rates are sufficient and highly nonsharp.

## 13. Source qualification and reproducibility

The exact-head GitHub Actions run is

- run ID: `37199933345`;
- workflow: `A2 v40 exact-source article and companion qualification`;
- head SHA: `c5593b05546889f436ce858c327670d080aae204`;
- status: `completed`;
- conclusion: `success`.

Exact checkout, pre-install source capture, environment installation, qualification of source and finite diagnostics, both document builds, evidence binding, and artifact upload all succeeded.

The uploaded artifact is

- artifact ID: `11302741601`;
- digest: `sha256:abfc63698ea4bbcc7c9bc175955c5a68a7ba8364ddf14f89327d84b507d29519`.

The receipt records:

- exact commit qualified: true;
- primary article: 23 pages;
- technical companion: 85 pages;
- current active labels: 402;
- current formal result blocks: 95;
- current proof bodies: 92;
- all 322 reviewed v39 labels retained;
- all 76 reviewed v39 proof bodies byte-identical;
- 656,744 author finite diagnostics;
- stable cross-document auxiliaries;
- no final TeX findings;
- primary PDF SHA-256 `6bef02a47cbea835d640832c222b728bcb62bd6fabde5be11b0c1fbf69785f3a`;
- companion PDF SHA-256 `284c9bf0dd9782e721ca2650d3c7b0aa3e9765813d5ee05337819ef027975d76`.

This is strong source evidence, not formal proof certification or physical-sensor validation.

## 14. Independent diagnostics and limits

The accompanying `verify_review.py` imports no author code and uses only the Python standard library. Ordinary and optimized executions are byte-identical at SHA-256

`24f20fd8d36e196a1b0adc7551ffbc27a2d5ea7aa4b8ffcc71f2f4434d374d00`.

It records 108,428 successful checks covering:

- the endpoint bit identity, including boundary conventions;
- the finite-prefix inverse and perturbation bound;
- incoming/outgoing support-arc identities and three-support cancellation in smooth noncircular models;
- the two negative chord signatures;
- exact Fourier-quotient recovery in compact model families;
- triangular bivariate moment inversion and the factorial stability bound;
- signed finite-command estimators;
- finite geometry and law-recovery exponent algebra.

These checks support finite algebra and explicit models only. They do not certify the continuum support theory, nonsmooth curvature measure, infinite configurations, finite hull acquisition, or journal-level priority. I did not perform an exhaustive literature search or re-prove every theorem in the companion.

## 15. Final verdict

**Response to the v39 report:** substantively successful. The principal theorem now uses two fixed positive-length forward fields under one unknown law, removes angular and length-continuum commands, broadens the exact class, and supplies finite geometry, probability, and prediction statements. The article/companion split substantially improves focus without deleting reviewed mathematics.

**Mathematical audit:** no fatal counterexample found in the new v40 core. The support cancellation and exact law factorization are compelling. The singular-law support, nonsmooth curvature, and finite acquisition arguments require independent specialist review.

**Source delivery:** successful exact-SHA qualification of both documents with archived evidence.

**Editorial assessment:** the manuscript is now plausibly competitive at the requested level, but acceptance would be premature without the major revisions and proof/literature audits above.

**Recommendation: major revision, with reconsideration at the Annals / Acta / Inventiones / JAMS benchmark.**