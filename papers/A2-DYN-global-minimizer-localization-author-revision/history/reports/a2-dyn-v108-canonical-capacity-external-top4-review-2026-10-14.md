# External top-four referee report on A2-DYN revision 108

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v108-microscopic-referee-response-2026-10-14`, `revision/a2-dyn-v108-microscopic-referee-copy-2026-10-14`  
**Reviewed author commit:** `2144665f89362ca80116f1999d99c80875833dcf`  
**Reviewed repository tree:** `01859d5234f0ddc6807ffa36c378a6a468667446`  
**Active manuscript directory:** `papers/A2-DYN-v108-referee-response`  
**Active mathematical source:** 259 numbered core modules; revision 108 adds modules 258--259  
**Immediate author baseline:** revision-107 qualification head `7f660346afea9500138920ca87fef46026a7e507`  
**Revision-107 theorem-bearing commit:** `2fad9446935a3c3efe6682715c8989ef66f1726d`  
**Frozen revision-107 paper tree:** `7f6fcd70afa7a54f6891d4d399bf370c302eb526`  
**Controlling report:** `reviews/a2-dyn-v107-positive-source-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling review commit / report blob:** `6811140ec51276247d75057980692d4a4d5e77b6` / `82cff2e2fc14e6a1eaa12b75fb41012dd155bdae`  
**Exact-SHA qualification at review freeze:** response run `38516993945`, queued; referee-copy run `38516999935`, queued  
**Date:** 14 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, o-minimal-geometry, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 108 is a genuine theorem-bearing response to the revision-107 report. It does not merely choose another family of angular blocks. It replaces the family-selection problem by an explicit roofwise pool containing every admissible physical segment which contains one of the two fixed windows

\[
[t,t+r],\qquad [t-r,t].
\]

The pool is Borel, a deterministic orientation convention counts each physical comparison sheet at most once, and its endpoint-envelope capacity admits a finite-count pointwise bound in terms of the inherited paired average and uncut optical variation. The revision then allocates the original microscopic source by

\[
V_{r,K}(t)=\min\{U(t),KP_r(t)\},
\qquad
R_{r,K}(t)=(U(t)-KP_r(t))_+.
\]

Within the explicitly stated fixed-window certificate class, the accepted height is an attained pointwise maximum. The construction also pointwise dominates every compatible revision-107 fixed-family allocation at the same total cost.

I audited

- `core/258_canonical_roofwise_comparison_capacity.tex`;
- `core/259_maximal_capacity_and_original_microscopic_residual.tex`;
- `appendices/v108_dependency_and_quantifier_audit.tex`;
- the active article shell;
- the response, proof ledger, source manifest and publication status;
- the controlling revision-107 report; and
- the inherited modules 255--257 needed for the new scalar and dominance statements.

Within the scope actually stated in those files, I found no decisive sign error, missing factor of the window length, reversed interval inclusion, invalid positive-source subtraction, unaccounted physical-overlap factor, exponent error, hidden differentiation of the Borel selector, or illegal interchange of the collision limit with the outer parameter. The new pool estimate and the stated attained maximality are mathematically coherent.

The negative recommendation is nevertheless forced by the exact endpoint of the argument. At the original outer schedule the manuscript proves

\[
\mathcal E_M
\le
\mathcal H_M(\mathsf R_B^{\rm can})
+C_MB^{-1/384},
\]

where

\[
\mathsf R_B^{\rm can}(t)
=
\bigl(\mathsf U_B^{\rm micro}(t)-K_BP_{r_B}(t)\bigr)_+.
\]

It also proves that the unchanged exact-label raw pointwise assertion is equivalent to

\[
\mathcal H_M(\mathsf R_B^{\rm can})\longrightarrow0
\qquad\text{for every fixed }M.
\]

No theorem establishes this limit.

The revision proves that the comparison pool exists, is measurable, has overlap one, and is optimal within its declared certificate class. It does not prove that the pool contains enough capacity, uniformly in collision count, to pay the original microscopic source. Finite-count exhaustion as \(r\downarrow0\) is in the wrong quantifier order for the raw local limit theorem and is correctly identified by the manuscript as insufficient.

The residual therefore remains the upper pointwise obstruction itself. It is not a harmless error left after the principal theorem. The source manifest accurately keeps canonical-residual height decay, the full raw-return local limit theorem, closure of the primary referee request, collision-uniform logarithmic insertion, complete singular-endpoint verification and independent proof certification false.

At the requested benchmark, an explicit optimal allocation for an available comparison capacity is useful but does not substitute for the missing Lorentz-specific capacity-abundance theorem. Nor is the fixed-window maximality, by itself, a theorem of independent top-four breadth: once the certificate class permits a roofwise scalar accepted height bounded only by \(U(t)\) and \(K\) times the pool capacity, the formula \(\min\{U,KP_r\}\) is necessarily the algebraic maximum. The substance lies in the pool bound; the remaining difficulty lies in proving that its shortage is small. That difficulty is not resolved in revision 108.

## 2. Frozen source and chronology

The two reviewed author branches both resolve to

`2144665f89362ca80116f1999d99c80875833dcf`.

The repository tree at that commit is

`01859d5234f0ddc6807ffa36c378a6a468667446`.

The active article is

`papers/A2-DYN-v108-referee-response/main.tex`,

and the full historical source is assembled through the accompanying `supplement.tex`.

The author commit starts from the controlling revision-107 review commit

`6811140ec51276247d75057980692d4a4d5e77b6`.

The frozen revision-107 author head is

`7f660346afea9500138920ca87fef46026a7e507`,

whose theorem-bearing parent is

`2fad9446935a3c3efe6682715c8989ef66f1726d`.

The distinction matters. The later revision-107 head is a narrow TeX-diagnostic qualification repair, not a second mathematical revision. Revision 108 records that distinction correctly and also records the later successful completion of both revision-107 author workflows without rewriting the freeze-time observation in the controlling report.

Revision 108 retains all 257 inherited numbered modules and adds

- `core/258_canonical_roofwise_comparison_capacity.tex`;
- `core/259_maximal_capacity_and_original_microscopic_residual.tex`.

The current review branch starts directly from the exact revision-108 author commit and adds only this report under

`reviews/a2-dyn-v108-canonical-capacity-external-top4-review-2026-10-14/`.

No author manuscript, author branch, workflow, prior review, historical paper tree or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v108-canonical-capacity-qualification.yml`.

At the freeze of this report, the two exact-SHA runs were

- response branch run `38516993945`: `queued`, conclusion `null`;
- referee-copy branch run `38516999935`: `queued`, conclusion `null`.

I therefore do not describe revision 108 as remotely qualified at the review freeze.

The encoded workflow is designed to check

1. the exact author SHA;
2. the frozen revision-107 paper tree;
3. the controlling report blob;
4. preservation of inherited blobs and executable modes;
5. the active claim flags and metadata supersession;
6. normal and optimized finite diagnostics;
7. native article and supplement compilation;
8. reference stabilization and the narrow inherited TeX-advisory exception;
9. recorder coverage of all 259 modules; and
10. upload of exact-SHA sources, PDFs and diagnostic evidence.

Those are meaningful source and reproducibility checks. A later successful run would not certify

1. the inherited physical pairing-sheet construction;
2. existence and finiteness of all one-sided endpoint traces on the comparison space;
3. the endpoint variation inequality on every relevant physical segment;
4. one-copy identification of the uncut optical source after the physical sum;
5. collision-uniform abundance of fixed-window comparison capacity;
6. singular endpoint extensions outside the inherited regular-segment hypotheses;
7. a collision-uniform inverse-residence or logarithmic insertion;
8. decay of the canonical residual; or
9. the full exact-label raw local limit theorem.

The manuscript itself generally observes this distinction.

## 4. Scope of the mathematical audit

The substantive audit concentrates on

1. the Borel roofwise pool and its deterministic disjointization;
2. the decomposition \(P_r=D_r+E_r\);
3. the finite-count estimate for \(D_r\);
4. payment of \(E_r\) by the inherited uncut optical variation;
5. physical multiplicity one;
6. the exact allocation of the original microscopic source;
7. the fixed-window certificate class;
8. attained maximality in that class;
9. domination of compatible revision-107 allocations;
10. the strictness diagnostic;
11. the outer schedule and exponent arithmetic;
12. the scalar equivalence;
13. finite-count exhaustion and its order of quantifiers; and
14. the exact remaining physical estimate.

The first 254 modules and the broader inherited spectral, arithmetic, Gaussian, coarea, pressure, optical and raw-inversion chain are treated as source-pinned inputs. This report does not independently re-prove that historical pipeline.

## 5. The obstruction inherited from revision 107

Revision 107 had reached an exact positive decomposition of the original microscopic source using a chosen countable family of source blocks and comparison weights. For each block it used the endpoint envelope

\[
p_\vee=\max\{f_-,f_+\}
=c^arepsilon+|f_--f_+|
\]

as comparison capacity. The paired minimum \(c^arepsilon\) was the source measure, while the difference between the maximum and minimum was paid by the uncut endpoint variation.

The revision-107 report accepted the finite-count comparison within its stated hypotheses but identified two unresolved tasks:

1. construct a complete comparison family with controlled physical overlap and outer cost; and
2. prove that the capacity-deficient residual has vanishing ordered essential height.

Revision 108 addresses the first task in a strong and clean way. It removes the need to enumerate or optimize angular source blocks. It does not address the second task quantitatively.

## 6. The complete roofwise pool

At a fixed collision count, radius, exact labels and \(arepsilon\), module 258 defines

\[
q_+(t,\theta)
=\mathbf1_{\{0<\ell<\Delta,\ a<t,\ t+r<b\}},
\]

and

\[
q_-(t,\theta)
=(1-q_+)
\mathbf1_{\{0<\ell<\Delta,\ a<t-r,\ t<b\}}.
\]

Thus

\[
Q_r=q_++q_-
\]

is the indicator of the union of the two admissible one-sided window conditions, with positive orientation preferred when both are available.

This construction has three useful properties.

First, it is Borel because it is expressed by Borel inequalities in the endpoint maps and the target roof.

Second,

\[
0\le Q_r\le1,
\]

so the comparison space has physical overlap one by construction. There is no separate combinatorial overlap theorem and no word-count factor.

Third, every admitted segment has length less than \(\Delta\), contains the relevant one-sided roof window, and lies entirely in

\[
(t-\Delta,t+\Delta).
\]

These statements are correct on the inherited admissible physical comparison space. They do not extend the endpoint-trace and variation inputs to singular sheets on which those inputs have not been verified.

## 7. The finite-count capacity bound

The pool capacities are

\[
P_r(t)=\int Q_rp_\vee\,d\theta,
\qquad
D_r(t)=\int Q_rc^arepsilon\,d\theta,
\qquad
E_r(t)=\int Q_re_\partial\,d\theta,
\]

with

\[
P_r=D_r+E_r.
\]

For the paired-minimum part, every positively oriented admitted segment contains \([t,t+r]\), and every negatively oriented admitted segment contains \([t-r,t]\). Therefore

\[
D_r(t)
\le
{1\over r}
\int_{t-r}^{t+r}
\mathsf T_\Delta^arepsilon(u)\,du.
\]

The factor is correct. Each orientation contributes one interval of length \(r\); after the deterministic disjointization the two contributions combine into the single two-sided integral displayed above.

For the endpoint-difference part, the inherited endpoint passage gives

\[
e_\partial(\theta)
\le
C(1+\varepsilon^{-1})
\int_{a(\theta)}^{b(\theta)}
A(u,\theta)I_m(u,\theta)/z(u,\theta)\,du.
\]

Since every admitted segment lies in \((t-\Delta,t+\Delta)\) and \(Q_r\le1\), one-copy physical summation gives

\[
E_r(t)
\le
C(1+\varepsilon^{-1})
\int_{t-\Delta}^{t+\Delta}v^0(u)\,du.
\]

I found no hidden block multiplicity in this step. The comparison weight is a single physical-sheet indicator, not a sum over source blocks.

Combining the two estimates yields the asserted finite-count bound

\[
P_r(t)
\le
{1\over r}
\int_{t-r}^{t+r}
\mathsf T_\Delta^arepsilon(u)\,du
+
C(1+\varepsilon^{-1})
\int_{t-\Delta}^{t+\Delta}v^0(u)\,du.
\]

Using the inherited fixed-window average inputs gives

\[
\mathcal H_M(KP_r)
\le
CK\{\varepsilon^{1/16}+(1+\varepsilon^{-1})\Delta\}.
\]

The independence of the leading constant from the previously fixed positive window is load-bearing. It is inherited rather than newly proved in revision 108.

## 8. Exact allocation of the original source

For the original selected source

\[
U(t)=
\int c^arepsilon(\theta)
\mathbf1_{\{a(\theta)<t<b(\theta)\}}
H(\Psi(\theta,t))\,d\theta,
\]

the manuscript defines

\[
V_{r,K}(t)=\min\{U(t),KP_r(t)\},
\]

and

\[
R_{r,K}(t)=(U(t)-KP_r(t))_+.
\]

The measurable source multiplier

\[
\beta_{r,K}(t)=
\min\{1,KP_r(t)/U(t)\}
\]

when \(U(t)>0\) gives the exact finite-count identity

\[
U=V_{r,K}+R_{r,K}.
\]

This is a valid positive decomposition. The source measure remains the original paired minimum with its original selector at the original roof. The endpoint maximum appears only in the comparison capacity.

A conceptual boundary should nevertheless be stated with particular care. The multiplier \(eta_{r,K}(t)\) is a scalar depending on the roof, not on the source sheet. It therefore allocates the same fraction of the entire source at roof \(t\), including source carried by sheets outside the admissible comparison subspace. This is legitimate for the scalar pointwise inequality because the accepted height is bounded by \(KP_r(t)\). It is not a sheetwise physical matching theorem and does not show that each accepted source trajectory has a comparison trajectory associated to it.

Accordingly, statements that source outside the verified comparison subspace is “retained” should be read as follows: it remains in the original positive source before the roofwise allocation, and every unallocated fraction remains in the residual. It is not retained with coefficient one whenever \(eta_{r,K}(t)>0\). The manuscript's certificate definition makes the global roofwise nature of the argument explicit, so this is principally a matter of interpretation and presentation rather than a counterexample to the displayed inequalities.

## 9. Attained maximality

Definition `def:v108-certificate` fixes \(r,\Delta,K\), the same comparison space, one-sided window support and the one-copy constraint

\[
w_++w_-\le1.
\]

A certificate accepts a scalar height \(Z(t)\) satisfying

\[
0\le Z(t)\le U(t),
\qquad
Z(t)\le
K\int(w_++w_-)p_\vee\,d\theta.
\]

Any admissible weights satisfy

\[
w_++w_-\le Q_r,
\]

hence

\[
Z(t)\le\min\{U(t),KP_r(t)\}=V_{r,K}(t).
\]

The choice

\[
w_+=\gamma q_+,
\qquad
w_-=\gamma q_-,
\qquad
\gamma={V_{r,K}\over KP_r}
\]

on \(P_r>0\) attains equality. Measurability and the bound \(0\le\gamma\le1\) are immediate. The zero-capacity case is handled correctly.

Thus the maximality theorem is correct in its stated class.

Its scope is narrow and should not be inflated. The class deliberately decouples the scalar accepted source height from a source-sheet matching and permits roof-dependent comparison weights. It fixes the window, cost and admissible comparison space. The theorem is not an optimality result over transport mechanisms, variable scales, singular extensions or Lorentz comparison geometries. The manuscript says this, and the top-four assessment depends on preserving that limitation.

## 10. Domination of revision-107 allocations

For a compatible revision-107 family with comparison width at least \(r\), comparison length below \(\Delta\), overlap at most \(N\) and block budget \(\kappa\), every active comparison support contains one of the canonical \(r\)-windows. It is therefore contained in the canonical pool.

The old blockwise allocation satisfies

\[
\beta_jT_j(t)\le\beta_jC_j\le\kappa P_j.
\]

Summing the active blocks and using the full physical overlap gives

\[
V^{\rm old}(t)\le N\kappa P_r(t).
\]

Since source blocks are disjoint and their scalar fractions lie in \([0,1]\), also

\[
V^{\rm old}(t)\le U(t).
\]

Consequently

\[
V^{\rm old}(t)\le V_{r,N\kappa}(t),
\qquad
R_{r,N\kappa}(t)\le U(t)-V^{\rm old}(t).
\]

This is a genuine pointwise dominance statement, not merely a comparison of integrated capacities. I found the use of the inherited common-window lemma and the overlap factor \(N\) correct.

## 11. Strictness of the certificate class

The two-interval diagnostic in `prop:v108-strict` is internally consistent. The selected source interval has length \(s\), the comparison interval has length \(r+s/2\), and for a positive interval of target roofs the comparison interval contains \([t,t+r]\). Thus the canonical certificate has positive capacity and accepts the selected source.

At the same time, no interval of length less than \(r+s\) can contain a translate of the entire source interval by \([0,r]\) or \([-r,0]\), so the old whole-source-window block criterion is unavailable.

This proves strict inclusion of the declared certificate classes. It is not a physical Lorentz realization and does not show that the newly added capacity is collision-uniformly abundant in the actual model. The manuscript correctly labels it as a diagnostic.

## 12. Outer schedule and rate

Revision 108 sets

\[
\Delta_B=8\delta(B),
\qquad
0<r_B<\Delta_B,
\qquad
1\le K_B\le C\varepsilon(B)^{-1/32},
\]

with all parameters fixed at the outer stage before the collision limit.

Since

\[
\delta(B)=O(\varepsilon(B)^4),
\]

the pool estimate gives

\[
\mathcal H_M(V_{r_B,K_B})
\le
C\varepsilon^{-1/32}
\{\varepsilon^{1/16}+O(\varepsilon^3)\}
=O(\varepsilon^{1/32}).
\]

With

\[
\varepsilon(B)=A_0B^{-1/12},
\]

this is

\[
O(B^{-1/384}).
\]

The exponent arithmetic is correct. No dependence on \(r_B\) appears in the final bound because the inherited paired-average estimate is stated uniformly in each previously fixed positive averaging width.

## 13. The canonical residual and scalar equivalence

For the original unmatched microscopic source, the manuscript defines

\[
\mathsf R_B^{\rm can}(t)
=
\bigl(
\mathsf U_B^{\rm micro}(t)-K_BP_{r_B}(t)
\bigr)_+.
\]

The accepted part has height \(O(B^{-1/384})\), so the inherited scalar reduction gives

\[
\mathcal E_M
\le
\mathcal H_M(\mathsf R_B^{\rm can})
+C_MB^{-1/384}.
\]

Sufficiency of canonical-residual decay is immediate.

For necessity, the inherited revision-105 theorem states that the original pointwise assertion implies

\[
\mathcal H_M(\mathsf U_B^{\rm micro})\to0.
\]

Since

\[
0\le\mathsf R_B^{\rm can}\le\mathsf U_B^{\rm micro},
\]

canonical-residual decay follows. Thus the asserted equivalence is correct, conditional on the inherited scalar chain.

This equivalence also identifies the exact mathematical status of revision 108: the original theorem is still unproved unless the canonical shortage is shown to vanish.

## 14. Finite-count exhaustion

At fixed collision count, radius, labels and \(\Delta\), every interior point of a positive-length admissible segment contains a sufficiently small one-sided window. Hence

\[
Q_r(t,\theta)theta)\uparrow
\mathbf1_{\{0<\ell<\Delta,\ a<t<b\}}
\qquad(r\downarrow0).
\]

Monotone convergence and

\[
p_\vee\ge c^arepsilon
\]

show that, for source supported on the admissible comparison space and \(K\ge1\),

\[
R_{r,K}(t)\downarrow0
\]

for almost every \(t\) as \(r\downarrow0\).

This proposition is correct.

It does not imply the needed theorem. The proposition first fixes collision count and then sends \(r\) to zero. The raw pointwise theorem requires \(r_B\) to be fixed from the outer parameter before the complete physical sum, essential suprema and collision limsup. No uniform modulus in collision count is proved. A diagonal choice \(r=r(m)\) is not permitted by the declared order of limits.

This is not a technicality. Microscopic source can move to smaller and smaller segment lengths as collision count grows. For every fixed \(r_B>0\), the capacity pool may remain deficient on precisely the collision-dependent scales carrying the upper spike. Finite-count exhaustion supplies no estimate against that possibility.

## 15. The remaining positive source

The canonical residual can retain positive height for several distinct reasons.

1. The source may concentrate on segments whose residence is smaller than the fixed \(r_B\) at increasing collision counts.

2. The admissible comparison space may exclude singular endpoint extensions for which finite traces, absolute continuity or the weighted variation estimate have not been verified.

3. Even when source and comparison spaces coincide, the pool capacity at the same target roof may be smaller than \(U/K_B\) at the collision-uniform scale.

4. The endpoint envelope may be finite but spatially arranged so that few segments contain a complete one-sided \(r_B\)-window.

5. Flat, short-reach, nonstationary and capacity-deficient microscopic sheets can remain whenever other same-event sheets do not provide enough roofwise capacity.

6. The inherited logarithmic and inverse-residence criteria remain unverified on the full Lorentz source.

The canonical construction removes selection and overlap as independent construction problems. It does not remove physical scarcity.

## 16. What a decisive next revision must prove

A revision capable of changing the recommendation must prove, for an explicit outer schedule \(r_B,\Delta_B,K_B\) fixed before collision limsup,

\[
\lim_{B\to\infty}
\limsup_{m\to\infty}
\sup_{R,n,k}
m^2
\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
\bigl(
\mathsf U_{B,m}^{\rm micro}(t)
-K_BP_{r_B,m}(t)
\bigr)_+
=0
\]

for every fixed \(M\).

There are several logically acceptable routes, but one of them must be completed on the original source.

### Route A: a collision-uniform capacity-abundance theorem

Prove that the canonical pool contains enough same-event endpoint-envelope capacity at a schedule-compatible fixed window, after the complete physical sum and uniformly over radius and exact labels.

This requires more than finite-count coverage. It requires a quantitative lower comparison between the original microscopic source and the pool capacity, with every singular or excluded class either admitted under proved trace hypotheses or estimated separately.

### Route B: a direct microscopic insertion

Prove the inverse-residence estimate proposed in revision 105 or the logarithmic insertion proposed in revision 106, with constants uniform in collision count, radius, exact labels and the outer parameter in exactly the order required by the raw pointwise theorem.

### Route C: a hybrid scarcity decomposition

Partition the canonical residual into physically defined classes and prove a summable height estimate for each class: shrinking regular segments, singular extensions, short-reach sheets, flat pulses and any endpoint-trace exception. The partition must be performed before the collision limsup and must retain all original positive weights.

Adding another certificate class without such a uniform scarcity theorem would not close the organizing result.

## 17. Specialist audit obligations

Even after the residual estimate is supplied, the following load-bearing continuum inputs still merit independent specialist reconstruction:

1. the incident-component pairing-sheet model and multiplicity-one convention;
2. endpoint trace existence and one-sided passage;
3. local absolute continuity of the weighted density on every admitted segment;
4. the weighted endpoint-variation inequality;
5. the identification of the summed variation integral with the original uncut optical source;
6. common coarea versions for roof-dependent Borel restrictions;
7. uniformity of the fixed-window paired and uncut average estimates;
8. the complete order of the radius, label, collision and outer limits; and
9. the inherited spectral and pressure inputs supporting those averages.

The current source and CI checks cannot certify these matters.

## 18. Metadata and presentation

Revision 108 correctly supersedes the stale local revision-106 identity through a versioned provenance record rather than rewriting the historical tree. It also distinguishes the revision-107 theorem-bearing commit from its later qualification-only head.

The active README, source manifest, publication status, proof ledger and response are mutually consistent about the main incompleteness flags.

The packet nevertheless retains inherited files such as `LOCAL_FULL_BUILD_RECORD.md` and `VALIDATION.md` whose headings describe revision 105. The active README explicitly declares such files historical, so I do not treat this as source fraud or a mathematical defect. For a genuine journal submission, however, the active packet should present one unambiguous current validation summary and move stale status files into a clearly marked provenance directory. The present archive architecture is useful for repository history but burdens the readable article and referee trail.

The main article is assembled by inserting modules 258--259 and the quantifier appendix into an exact snapshot of the preceding article. This preserves history, but the journal-facing exposition continues to accumulate successive reductions around an unproved endpoint. A future submission should provide a coherent theorem hierarchy in which the completed results are stated independently and the single remaining hypothesis is visible without reconstructing more than two hundred historical modules.

## 19. Minor mathematical and expository requests

1. In the statement following the restriction to a verified comparison subspace, clarify that the source outside that subspace is retained in the original source but may receive the global roofwise multiplier \(eta_{r,K}(t)\); it is not retained sheetwise with coefficient one.

2. State directly in the maximality theorem that the source allocation is global in the roof variable and is not a coupling between individual source and comparison sheets.

3. In the dominance theorem, include the condition \(r\le r_{m old}\) in the theorem's displayed hypotheses rather than only in prose as “window width at least \(r\).”

4. In the strictness diagnostic, emphasize in the proposition statement, not only the proof, that the old class has roof-independent source blocks and requires inclusion of the translated entire source interval.

5. Place the exact definition of the admissible comparison subspace in the active article near Definition `def:v108-pool`, rather than referring generally to wherever the inherited regular-segment hypotheses were verified.

6. Record the final v108 workflow states in a later provenance-only commit if they complete, without changing the freeze-time statements in this report.

7. Consolidate current validation metadata so that stale revision-105 headings cannot be mistaken for the active qualification record.

These requests do not alter the principal recommendation.

## 20. Decision

Revision 108 makes a real and useful advance. It supplies an explicit Borel comparison pool, eliminates a separate angular-family selection problem, proves physical overlap one, obtains a clean finite-count endpoint-envelope bound, and identifies the pointwise optimal allocation within a precisely stated fixed-window certificate class. It also proves a correct domination theorem over compatible revision-107 allocations.

The manuscript remains incomplete at its governing theorem. Its final scalar statement is equivalent to decay of the canonical capacity shortage, and no collision-uniform theorem proves that decay. Finite-count exhaustion cannot be substituted because its limit order is different. The full exact-label raw pointwise local limit theorem and its unrestricted downstream consequences therefore remain unproved.

**Recommendation: reject in the present form at the Annals / Acta / Inventiones / JAMS benchmark.**

A materially different recommendation would require closure of the canonical residual on the complete Lorentz family, or a standalone completed theorem of independent top-four breadth whose statement no longer depends on that missing endpoint. Revision 108 does not yet provide either.
