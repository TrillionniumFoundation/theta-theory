# Independent referee report on A2, revision 67

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. Correctness, originality, exceptional significance, and reproducibility are separate questions. The author's response is a statement of claims to examine, not evidence that those claims have been proved.

## 1. Recommendation and frozen submission

**Recommendation: do not accept at the requested highest general-journal level on the present exceptional-significance case. The quantitative correction R66-m1 is satisfactorily implemented, and no new mandatory core proof repair or fatal counterexample is established within this round's coverage.** The revised proposition now controls the error of the complete finite-jet reconstruction, rather than treating a curvature error as a complete-jet error with coefficient one. The residual stopping criterion and its certified inexact-evaluation variant are also valid.

Revision 67 is a quantitative correction and a mechanism-led restatement, not a new global identification theorem. The stronger exact result already present in v66 remains: marked positive-curvature candidates need not be close for exact contact identification. That conclusion must not be confused with uniform global analytic-norm stability or reconstruction of an unknown polygon. The new opening respects this distinction.

The negative placement recommendation is consequently not an allegation that the correction failed. Section 6 assesses the combined relative physical law and actual contact-response mechanism, including the nonlinear-information example emphasized by the author. Neither another version number nor the absence of a new error settles that assessment.

| Object | Immutable identity |
|---|---|
| Actual compiled mathematical source | `97b0c5bf15d6581c42b0f503bbe902c9d89b42db` |
| Reconstructed manuscript subtree | `5ba7cc8f87aaadd2e3f734c41bb030668e15cff7` |
| Source branch | `revision/a2-v67-relative-law-mechanism-2026-09-16` |
| Referee-ready branch | `revision/a2-v67-referee-ready-2026-09-16` |
| Referee-ready head used as review parent | `c5633d2e4d4f2d7c2b34d4b05f9440fdc5a18591` |
| Native workflow / attempt / artifact | `35074257415` / `1` / `10437417575` |
| Preceding v66 report | `3d49684cc6c9bad36d80c99dc46af276f53fae18` |
| Source reviewed in that report | `38f798a9b28237420f070a032d3601f0bee72cde` |

The manuscript directory is `papers/A2-v17-boundary-information-coarsening/`; its historical name does not identify the revision. The principal article has **151 pages**, the full technical manuscript **326 pages**, and the companion **seven pages**. Page references below are to the principal article. The source-to-referee-ready comparison contains six later commits but no changed compiled mathematical input. The corrected module was also fetched directly at the compiled commit; its Git blob is `4a581b2181257d152b56167f60fff4f65454fa3b`, matching the frozen source. [D1]

### Coverage and exclusions

The complete current 431-line global-curvature module was read, including the residual argument and the full finite-jet propagation proof. The revised synthesis and abstract, response, cover letter, historical audit, and dependency declaration were checked. This round also directly revisits the periodic relative determinant and physical-time interface; the graph-coordinate, two-offset, and actual-smooth envelope interfaces; the integrated-amplitude stable-return argument; and the area-preserving leading-data comparison. These are the mathematical ingredients singled out by the new significance argument. [S1–S6, R1–R2]

This is **not** a fresh line-by-line proof audit of all 484 pages. The complete earlier finite-chain/full-phase prerequisites, every detail of the retained analytic Banach inverse and conditional-continuation theorem, all unregistered global matching/lattice and moving-family proofs, the full calibration/statistical catalogue, and the companion are not freshly certified. Inherited source identity establishes retention, not fresh proof certification. Mechanical comparison of all delivered pages has a different scope.

## 2. Disposition of the preceding report

| Previous point | Present disposition |
|---|---|
| R66-m1 / R66-D2: propagate curvature stopping error through the higher-jet inverse | **Closed.** Proposition 10.4 supplies an explicit off-fixed-point recursion and the factor $L_M E_m$. |
| First-increment bound described as a posteriori | **Corrected.** Theorem 10.2 distinguishes the a priori estimate from the residual estimate and proves the latter. |
| Global exact identification without candidate closeness | Retained. It is not weakened to selection of a local curvature branch. |
| Supplied polygon, physical gauges, two-offset factors, fixed placement and visitation | Retained beside the relevant conclusions. |
| Mechanism-led presentation rather than a list of strongest consequences | Improved. Theorem 1.1 now displays the relative physical input and the geometric inverse together. |
| Exceptional significance | Reconsidered in Section 6; not a correctness issue that a small stopping amendment automatically closes. |

All **837 inherited source paths** remain: **829 byte-identical**, eight changed with byte-exact originals archived, and no inherited Git-mode change. All **134 inherited active inputs** remain, with no new active path. The complete periodic-forward, periodic-inverse, finite-experiment, and position-pilot modules are unchanged. These are independent byte/input-graph findings, not a count of distinct mathematical theorems. [D1]

## 3. The corrected stopping and propagation argument

### R67-M1. The residual certificate has the right domain and interpretation

Theorem 10.2, pp. 46–48, retains the projected map

$$
(\Phi_s z)_i=\left[s_i-k_i+\frac{k_i^2}{k_i+s_{i+1}+z_{i+1}}\right]_+,
\qquad q(s)=\max_i\left(\frac{k_i}{k_i+s_{i+1}}\right)^2<1.
$$

Here $s>0$ is the specified action-Hessian datum, and $z\ge0$. The map sends the complete closed orthant into $\prod_i[0,s_i]$. Positive part is one-Lipschitz, and the magnitude of the derivative in the next coordinate is at most $q(s)$. Thus its unique fixed point is defined without an initial-closeness requirement. The first-increment estimate remains an a priori bound. [S1]

For any nonnegative trial vector $v$, not only an exact iterate, the triangle inequality gives

$$
\|v-z(s)\|_\infty
\le\|v-\Phi_s v\|_\infty+q(s)\|v-z(s)\|_\infty.
$$

Consequently the new equation (10.4) is the valid a posteriori certificate

$$E(v;s)=\frac{\|\Phi_s v-v\|_\infty}{1-q(s)}.$$

If a computed map value $w$ satisfies a **certified** error bound $\|w-\Phi_s v\|_\infty\le\eta$, replacing the numerator by $\|w-v\|_\infty+\eta$ is correct. This assumes the evaluation-error bound; it does not itself implement interval arithmetic or certify arbitrary floating-point evaluations. It also concerns the fixed datum $s$, not uncertainty in the extracted Hessians. The latter is charged separately in Proposition 10.4.

The test $\min_i v_i>E(v;s)$ is sufficient for the exact fixed point to be strictly positive. This certifies membership in the positive **quadratic contact image**, not realization by an arbitrary globally closed obstacle collection. For a strictly positive fixed point, convergent iterates eventually pass the test. The manuscript does not assert finite-time certification of nonmembership when a fixed-point component is zero. These are appropriate limits of the criterion.

### R67-M2. The approximate-curvature reconstruction is now actually specified

Proposition 10.4, pp. 49–51, first obtains extracted action jets $t=(t_2,\ldots,t_M)$ from the finite-flight densities. The limiting densities are realizable; the finite densities are compared with them before the two-offset factorization is used. The exact fixed point $z(t_2)$ remains the curvature reconstruction. On the stipulated compact positive class and at fixed $M$, the exact-fixed-point jet error remains $C_M(\tau^N+\varepsilon)$. [S1, S3]

The finite-iteration extension needs more information than a bound for $z^{(m)}-z$. Keeping $t$ fixed, the revised proof specifies

$$
\widehat\sigma_i(v;t_2)=\frac{\epsilon_i k_i}{k_i+t_{2,i+1}+v_{i+1}},
\qquad (\widehat T_n w)_i=\widehat\sigma_i^n w_{i+1},
$$

$$
D_n=(I-\widehat T_n)(I+\widehat T_n)^{-1},\quad
\mathcal J_2(v;t)=v,\quad
\mathcal J_n(v;t)=D_n\{t_n-\mathcal R_n(\mathcal J_2,\ldots,\mathcal J_{n-1})\}.
$$

At $v=z(t_2)$ the Schur relation makes these the actual one-step factors and the actual inverse. Away from that point this is an explicitly chosen smooth algebraic extension. Recomputing physical tail factors from $v$ alone would give a different off-point rule; the proof no longer leaves that choice ambiguous. It correctly makes no assertion that the off-point tuple solves a physical stationary problem.

The remainders $\mathcal R_n$ are not freely assigned formal functions. Their smooth finite-jet dependence comes from the retained stationary-envelope factorization for actual reflecting graphs. On compact positive curvature sets, finite-order local representatives and their higher-jet perturbations give the needed smooth domains. The slightly enlarged common jet boxes can therefore be chosen before estimating the stopping error. There is no need for every such local jet tuple to extend to a globally prescribed table.

### R67-M3. The matrix derivative and complete-jet induction are correct

On the chosen positive boxes, let $\alpha<1$ bound $|\widehat\sigma_i|$ and let $d_*$ bound $k_i/(k_i+t_{2,i+1}+v_{i+1})^2$. Then

$$
\|D_n\|_\infty\le b_n=\frac{1+\alpha^n}{1-\alpha^n},\qquad
\|D_vD_n\|\le\beta_n=\frac{2n\alpha^{n-1}d_*}{(1-\alpha^n)^2}.
$$

The identity $D_n=2(I+\widehat T_n)^{-1}-I$ gives

$$
\mathrm dD_n=-2(I+\widehat T_n)^{-1}
             (\mathrm d\widehat T_n)(I+\widehat T_n)^{-1}.
$$

The perturbation is sandwiched between two resolvents. It is not commuted through a signed cyclic shift. Each row of $\mathrm d\widehat T_n$ has one relevant entry, so its maximum row-sum norm is bounded by $n\alpha^{n-1}d_*\|\mathrm dv\|_\infty$. No unaccounted factor equal to the cycle length is needed in this estimate. Independent exact controls detect the incorrect commuted derivative in all 60 tested nonconstant signed configurations. [S1, D2]

Let $U_n$ bound the residual action coefficient and $r_n$ bound the derivative of $\mathcal R_n$ in the **joint maximum norm** of all lower jets. Subtracting the two recursions at fixed $t$ yields the claimed sufficient constants

$$
L_2=1,\qquad
L_n=\max\{L_{n-1},\ \beta_nU_n+b_nr_nL_{n-1}\}.
$$

The joint norm convention matters: $r_n$ already measures simultaneous changes in all lower coefficients. Induction proves

$$\|\mathcal J_{\le M}(v;t)-\mathcal J_{\le M}(z(t_2);t)\|_\infty
\le L_M\|v-z(t_2)\|_\infty.$$

Adding the exact-fixed-point error gives

$$
\|\widehat q_{\le M}^{(m)}-q_{\le M}\|_\infty
\le C_M(\tau^N+\varepsilon)+L_M E_m(t_2).
$$

This is the requested correction, with an actual proof rather than the insertion of an unspecified constant. Sufficiently small combined error keeps the trial curvature positive and all intermediate reconstructions in the common boxes. The constants are class-dependent and fixed-order; they are not inferred from a noisy law alone or claimed uniform in the maximum norm of unweighted derivatives as $M\to\infty$.

### R67-M4. The previous cubic control is now covered

The v66 report used a normal two-contact local example with

$$k_0=k_1=1,\quad F_i(x)=x^2/8+10x^3/6,\quad c_i=1/4,\quad s_i=3/4.$$

These graphs are strictly convex on a sufficiently small real collar. The symmetric cubic action coefficient is $90/7$, and the cubic lower-order remainder is zero. Starting the curvature iteration at zero gives $v_i=9/28$. The old first-increment bound is $12/77$, whereas the observed-Schur prescription gives the factor $14/29$ and cubic error

$$\left|\frac{1-(14/29)^3}{1+(14/29)^3}\frac{90}{7}-10\right|
=\frac{48740}{189931}>\frac{12}{77}.$$

That remains a correct negative control of the **superseded coefficient-one interpretation**, not a counterexample to the revised proposition. The new residual bound at the same iterate is $42/319$. On the segment from $1/4$ to $9/28$, one may take $\alpha=1/2$, $d_*=1/4$, $U_3=90/7$, and $r_3=0$, giving $L_3=2160/343$. Hence

$$\frac{48740}{189931}<\frac{1080}{2401}
=L_3\left|\frac9{28}-\frac14\right|\le L_3\frac{42}{319}.$$

The author both attributes the antecedent and remedies it. No further change of the exact theorem or statistical exponent follows from this example. These are local smooth/algebraic controls, not a claim that arbitrary test tuples have been realized as complete periodic tables. [R1, S1, D2]

## 4. Reassessment of the combined relative/contact mechanism

### R67-C1. Relative normalization, not the Schur recurrence alone, carries the forward claim

The revised Theorem 1.1 places the exact reference twist and the physical law before the inverse. This is mathematically appropriate. For $N=nP$ returning oriented flights, the retained periodic construction has

$$D_{N,b}=\frac{\sinh\chi}{(\mathcal M_b)_{12}\sinh(n\chi)}.$$

The chronological monodromy entry, signed coordinates, and endpoint half-mass convention fix this exact quantity. An unspecified exponential equivalent would not fix the relative physical normalization. The smallness of $D_{N,b}$ prevents an ordinary absolute action estimate from being substituted for a relative mixed-derivative theorem. [S2, S4]

The actual proof starts with the corner cofactor, normalizes it, and writes the logarithm as an edge sum minus $\log\det(I+G_N\Delta H_N)$. The sign-conjugated Jacobi operator has a strictly positive diagonal surplus. Its nearest-neighbor resolvent expansion gives exponentially decaying Green entries. Nonlinear half-lines and finite bridges are constructed in weighted spaces; their two-ended gluing error has a summable bound with a polynomial-in-$N$ factor.

The determinant passage needs trace-norm control, not merely a uniform operator bound. The perturbation is localized at the ends with summable entrywise tails. Truncating at a fixed fraction of the bridge length leaves exponentially small tails; the retained end blocks are compared with the respective half-line compressions. Reflected and opposite-end Green terms are exponentially small. The trace-series estimate

$$|\operatorname{tr}(T^h-\widetilde T^h)|
\le hq_1^{h-1}\|T-\widetilde T\|_1,\qquad q_1<1,$$

then supports the product of two end amplitudes. The proof does not compare entire reference resolvents in a trace norm they need not possess. Separately fixed differentiations introduce fixed polynomial losses, absorbed by a strict exponential margin. I found no new fatal error in this examined relative interface. That is a proof assessment, not a deduction from finite matrix tests. [S4]

The physical-time factor is also essential. If $E=W-nL+p_bu-p_bv$, the remaining physical interval is $d-E+p_bu-p_bv$, not $d-E$. The unconditioned law carries $D_{N,b}/(2\pi A)$ before conditioning. A sufficiently small positive window and lower bounds on adjacent flights justify the first/last collision interpretation. A gauge change of the variational action is not a change of the clock. These conventions remain explicit in the new opening. [S2, S4]

### R67-C2. The actual boundary response supports exact identification without candidate closeness

The graph sensor is the scaled tangent projection, not the unknown normal graph value. The retained envelope proof cancels variations of internal stationary coordinates, keeps and bounds the terminal contribution, and only then passes to the infinite half-line. The initial graph variation is counted once and later contacts twice. Interpolation of actual smooth representatives establishes finite-jet factorization before the signed cyclic block is used. This is the part distinguishing a geometric inverse from inversion of freely assigned formal generating functions. [S3]

At degree two, the actual Schur identity is

$$s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}}.$$

Its converse is not an arbitrary choice of Riccati root: the resulting ratios construct a decaying solution of the positive Jacobi problem, and coercivity identifies it with the physical linearized tail. Strict positivity of the fixed point is therefore the correct quadratic-image criterion. Equal data also imply

$$c_i-\widetilde c_i=-a_i\widetilde a_i(c_{i+1}-\widetilde c_{i+1}),$$

whose product around the cycle has absolute value below one. This proves global curvature uniqueness, rather than inferring it from nonsingularity of a Jacobian everywhere. [S1]

With curvature fixed, the actual factors determine all later signed blocks $(I+T_n)(I-T_n)^{-1}$. Successive comparison of lower jets gives all exact contact jets without candidate closeness. Analyticity then identifies germs on a common smaller neighborhood; smooth flat differences are not identified as zero germs. Whole-obstacle identity additionally requires actual connected closed analytic boundaries, fixed placement/lattice, and visitation of every labelled obstacle. The revised main statement retains these qualifications next to the conclusion. Global coefficient uniqueness is not used in place of the separately proved local analytic operator inverse. [S1–S3]

### R67-C3. The leading-information example is a realized distinction, at its stated level

The revised significance discussion emphasizes Theorem A.4.2, pp. 149–150. This round re-examined its support-function argument rather than merely accepting the citation. For

$$h_{s,z}(\theta)=1+s\sin^4\theta+z\sin^6\theta,$$

the exact area polynomial is

$$\mathcal A=\pi+\frac{3\pi}4s+\frac{5\pi}8z
-\frac{45\pi}{128}s^2-\frac{105\pi}{128}sz-\frac{525\pi}{1024}z^2.$$

Thus an analytic choice $z(s)$ preserves area exactly, with $z'(0)=-6/5$. At the horizontal contacts the support value, its first derivative, and curvature radius remain fixed. The fourth graph derivative is $3-24s$. For a sufficiently small parameter interval, strict convexity, disjointness, and the horizontal clearance margin persist in the stated periodic arrangement. The contact variation is an actual analytic obstacle family, not a tuple of formal coefficients. [S5]

The retained quartic response calculation gives, at $g=\kappa=1$, $\gamma=\operatorname{arcosh}2$, and $a=\sqrt3$,

$$\left.\frac{\mathrm d}{\mathrm ds}\mathcal R_\infty^{(s)}(0)\right|_{s=0}=\frac{\sqrt3}{2}.$$

The endpoint multiplicities and the integrated quartic terms give this nonzero coefficient. The leading gap, area, Hessian, count-amplitude and endpoint-covariance data specified by the theorem stay fixed, while the sufficiently small positive-offset law changes. This supports a real nonlinear-information claim. It is not a pair with identical complete marked length spectra or identical positive-offset probabilities, and the manuscript expressly does not make either claim. [S5, D2]

### R67-C4. The amplitude also carries nonlinear dynamical information

The retained Corollary 8.4, p. 34, defines $\zeta_b^\pm(u)=\int_0^u B_b^\pm(t)\,dt$. Double integration of the relative mixed derivative controls the connected action divided by $D_{N,b}$, with an $O(\tau^N|uv|)$ remainder. For the future stable return and the reversed unstable return, respectively,

$$B(T(u))T'(u)=e^{-\chi}B(u),\qquad
\zeta(T(u))=e^{-\chi}\zeta(u).$$

The normalization $B(0)=1$ fixes the scalar linearizing coordinate. Uniqueness follows by iterating the scalar contraction and using the derivative at zero. Thus recovery of the actual amplitudes supplies the corresponding nonlinear return germ in its declared endpoint chart, not just its multiplier. [S3–S4]

This is a consequence of the same relative amplitude, not a separate linearization theory. Its observational interpretation uses the amplitudes of the stipulated physical law; arbitrary changes of detector efficiency between offsets cannot be inserted into the cancellation formula. The introductory claim is accurate with the printed observation conventions.

## 5. Observation scope and primary-literature comparison

The revised opening distinguishes four assertions that must remain distinct: exact marked identification, local analytic-norm inversion, weaker-data alternating-channel reconstruction, and charged preparation results. The stopping correction changes none of their observation models. The present fixed-order density input is an interior $C^M$ error. It is not a derivative bound inferred from total variation alone, and no general-period sampling budget is proved by the residual test. Nor does the finite-dimensional curvature iteration give a running-time bound for the inherited countable realizable-law selector. [S1–S2, S6]

The targeted primary-source check was refreshed. Bálint–De Simoi–Kaloshin–Leguil's Theorem D and Corollary E concern length asymptotics and marked Lyapunov recovery for general periodic words in their open-billiard setting. Remark 2.3 distinguishes that information from individual contact-parameter separation by their asymptotic relations. The present supplied polygon and phase-resolved endpoint laws are different data; the contact inverse is not a solution of that separation question using the marked length spectrum. This comparison does not establish an impossibility theorem for all alternative uses of marked lengths. Printed pp. 9–10 were inspected. [L1]

Bolotin–Treschev's discrete Hill formula and orientation discussion, printed p. 12, provide classical cyclic-Hessian/monodromy context. Their formula is not the Dirichlet corner cofactor or the nonlinear two-ended conditional law. The current manuscript appropriately identifies the determinant algebra as a tool rather than claiming a new universal Hill formula. [L2]

The primary records also preserve the distinctions between De Simoi–Kaloshin–Leguil's analytic open-billiard symmetry/genericity setting and Finamore–Leguil's enriched marked-length datum for Sinai billiards. Florio–Leguil's version-5 notice removes the affected geometric spectral-rigidity assertion; that removed statement is not an available competing theorem. [L3–L5]

This is not an exhaustive priority investigation or a full proof audit of those works. I make no allegation that the manuscript's central theorem is already known. Neither standard ingredients nor a short final recurrence establishes prior art for their geometric combination.

## 6. Exceptional significance and article-level assessment

### R67-E1. The combined mechanism is the right subject of evaluation

The revision successfully changes the emphasis. Its strongest case is now visible: exact relative normalization retains nonlinear endpoint information at an exponentially small physical scale; an actual boundary response then converts that information into geometry, with global exact contact uniqueness. The realized leading-data example and the recovered nonlinear stable coordinates explain what information survives. They are not cosmetic examples, and I have not dismissed them as mere changes of notation.

My recommendation nevertheless remains adverse at the requested highest general-journal level. The issue is not that a proof uses familiar tools, that the data are function-valued, or that the argument is localized near selected orbits. None is inherently disqualifying. The issue is the demonstrated depth and reach of this particular theorem relative to the claimed placement.

On the forward side, the geometric reduction produces a uniformly controlled scalar nearest-neighbor variational problem. Weighted contraction and summable end perturbations then make the two-end normalization accessible by a resolvent expansion and trace-series continuity. This is a substantive and carefully assembled relative estimate. The manuscript has not persuaded me, however, that the resulting physical law exhibits a sufficiently broad new phenomenon or resolves a sufficiently consequential obstacle outside that controlled setting to support the proposed exceptional placement.

On the inverse side, once the actions are extracted in the supplied signed polygon coordinates, the boundary response has an invertible initial contribution and contracted later visits. The signed cyclic algebra and global curvature comparison then remove the local ambiguity. This is a clean geometric mechanism. Its exact whole-image consequence uses analyticity in fixed placement; it does not reconstruct that placement from the same general-period data. The nonlinear-information example separates the positive-offset law from its specified leading hierarchy, but not from an established full inverse datum in the comparison literature. These distinctions limit the importance that can be inferred from the example and global clause; they are not errors in either result.

The broader forward domain, the genuine periodic inverse, the removal of candidate closeness, and the separate finite-budget consequences deserve full credit. My reservation concerns whether their common mechanism has sufficient independent depth and likely mathematical influence for these general journals, rather than whether each later consequence is another separate breakthrough. The current case does not convince me. That is an evaluative judgment, not proof of lack of novelty or a prediction that every specialist or editor would agree.

### R67-E2. No new artificial repair cycle is prescribed

The author has answered the actual quantitative objection and has made the contribution case more coherent. It would be unfair to retain R66-m1 as an unresolved issue, to resurrect the candidate-closeness objection, or to describe the paper as lacking finite-observation consequences altogether. It would also be misleading to call the current stopping correction an independent new principal theorem.

I do not impose an unmarked theorem, ordinary marked-length rigidity, a grazing limit, period-uniform control, a general-period acquisition rate, or global same-disc stability as a missing prerequisite of the stated results. Nor do I request arbitrary deletion of the mathematical corpus. The principal and complete technical entries should remain distinct, with their different reading purposes clear.

A further editorial assessment should focus on the central relative/contact theorem itself. An alternative favorable assessment would need to explain its exceptional mathematical significance at the level of the mechanism and its consequences. Another small auxiliary result or preservation certificate cannot substitute for that explanation. This report therefore does not invite another nominal repair-only round.

## 7. Disposition codes

**R67-D1 — Quantitative correction:** R66-m1 is closed. The residual certificate, explicit off-point reconstruction, noncommutative derivative estimate, and complete-jet propagation justify the revised bound.

**R67-D2 — Exact and analytical scope:** preserve the global exact no-closeness conclusion, the positive quadratic-image distinction, and the separate local analytic/operator and observational hypotheses. No new fatal counterexample or mandatory core repair is established within the declared coverage.

**R67-D3 — Contribution and presentation:** the combined relative physical law/contact response is now foregrounded, and its leading-data and dynamical consequences are correctly scoped. This is an improved synthesis, not a new theorem count.

**R67-D4 — Placement:** do not accept at the requested level on the present exceptional-significance case. Do not reinterpret this as a remaining stopping-error defect, an established priority verdict, or a requirement to solve an unrelated inverse problem.

## 8. Independent reproduction and evidentiary limits

The downloaded artifact SHA-256 is `0be6400d1d4861df61a5a5396846cbdeca6faa18e19f17b68db85b494e847631`. Independent verification checks lengths, SHA-256 values and Git blob identities for **855 frozen files**, reconstructs the manuscript subtree using recorded modes, checks **134 distinct active inputs**, and verifies **47 native build-report evidence entries**. The per-entry active counts are 123 full, 55 principal and one companion. The separate baseline comparison verifies the retention findings in Section 2. Hash consistency is not authentication of authorship or reconstruction of the entire repository tree. [D1]

Fresh companion/full/principal builds succeeded with shell escape disabled and regenerated auxiliaries. All **484 pages** agree with the native PDFs in extracted text and same-renderer **72-dpi RGB arrays**. PDF bytes differ. Final logs have four full-manuscript and one principal underfull-box notice, none in the companion; no undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern was found. Actual visual inspection covered principal pp. **3, 46, 47, 49, 50, 51, 149 and 150**, at **108 dpi**. No clipping or unreadable formula was observed there. All-page mechanical parity is not all-page visual inspection. [D1]

The independent diagnostic imports no author checker. It checks 30 positive periodic quadratic data sets; 900 first-increment, 900 residual and 900 certified-inexact-evaluation inequalities; 840 sufficient positivity certificates; 30 two-point bounds; 60 signed block pairs with derivative and Lipschitz controls; the old cubic negative control with a valid propagation constant; and exact support-area and nonlinear-response identities. Normal and optimized Python emit identical JSON. The matrix tests do not independently evaluate every higher-order remainder $\mathcal R_n$; the general propagation induction is assessed in the printed proof. The scalar configurations are not claimed as globally realized billiards. [D2]

The author's preservation/mathematical checker was not rerun. The delivery verifier is reused from a prior independent audit, and the baseline comparator is adapted to the current pair of sources. Finite controls do not certify infinite-dimensional inversion, trace-class limits, all smooth differentiation orders, global continuation, or statistical risk theorems.

## Source keys

All S-keys refer to actual compiled source `97b0c5bf15d6581c42b0f503bbe902c9d89b42db`, under `papers/A2-v17-boundary-information-coarsening/`. [Immutable source root](https://github.com/TrillionniumFoundation/theta-theory/tree/97b0c5bf15d6581c42b0f503bbe902c9d89b42db/papers/A2-v17-boundary-information-coarsening).

- **S1:** `article/10c_global_curvature_inverse_v66.tex`, lines 1–431. Lemma 10.1 and Theorems 10.2–10.3; Proposition 10.4, pp. 49–51; particularly the new residual bound and lines 295–431. The filenames remain stable across revisions.
- **S2:** `article/00g_contact_synthesis_v66.tex`, lines 1–208; `article/00h_abstract_v66.tex`; current `rigidity.tex` and `main.tex`. Theorem 1.1 and adjacent observation-model discussion.
- **S3:** `article/10b_periodic_contact_inverse_v65.tex`, especially lines 1–355. Graph-coordinate transport, two-offset extraction, actual stationary envelope and signed finite-jet recursion. The full retained analytic function-space proof is not freshly certified in its entirety here.
- **S4:** `article/10a_periodic_itinerary_relative_v64.tex`, especially lines 1–475. Geometric Jacobi normalization, fixed-collar relative comparison, integrated amplitudes and physical-time law; Corollary 8.4, p. 34. The final nonnormal realization is retained, not fully re-audited in this round.
- **S5:** `v4/20_nonlinear_information.tex`, lines 1–195. Quartic response and realized area-preserving leading-data fiber; Theorem A.4.2, pp. 149–150.
- **S6:** `journal/DEPENDENCY_LEDGER_V67.md`; retained `article/23f2_finite_experiment_analytic_inverse_v62.tex` and `article/25a_common_observables_v25.tex`. Dependency declarations, observation separation and byte retention, not a fresh full statistical proof audit.
- **R1:** [v66 report](https://github.com/TrillionniumFoundation/theta-theory/blob/3d49684cc6c9bad36d80c99dc46af276f53fae18/reviews/a2-v66-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md), particularly R66-m1, E1–E2 and D1–D4.
- **R2:** `RESPONSE_TO_REFEREE_V67.md`, `COVER_LETTER_V67.md`, `HISTORICAL_DERIVATION_AUDIT_V67.md`, and `LITERATURE_CHECK_V67.md`. Author arguments and provenance, not proof substitutes.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, and `compare_baseline.py` in this review directory; artifacts 10437417575 and 10433187185; source-to-referee-ready GitHub comparison.
- **D2:** `independent_checks.py` and the full emitted JSON summarized in `AUDIT_RESULTS.json`; complete outputs and retained rebuild logs accompany the separate audit archive.
- **L1:** P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Commun. Math. Phys. 374 (2020), 1531–1575, DOI 10.1007/s00220-019-03448-x; [author-hosted paper](https://leguil.perso.math.cnrs.fr/Articles/Balint_DeSimoi_Kaloshin_Leguil.pdf), printed pp. 9–10 inspected.
- **L2:** S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257, DOI 10.1070/RM2010v065n02ABEH004671; [arXiv:1006.1532](https://arxiv.org/pdf/1006.1532), printed p. 12 inspected.
- **L3:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, DOI 10.1007/s00222-023-01191-8; [primary record](https://arxiv.org/abs/1905.00890).
- **L4:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*; [enriched-datum primary record](https://arxiv.org/abs/2510.18983).
- **L5:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*; [version-5 correction notice](https://arxiv.org/abs/2010.04120v5).

Primary records were checked September 16, 2026. This review adds only review files; manuscript sources, earlier reports, native deliveries, the default branch and repository permissions are not altered.
