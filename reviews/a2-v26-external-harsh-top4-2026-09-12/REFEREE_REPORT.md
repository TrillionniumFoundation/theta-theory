# External referee-style report on A2 v26

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Reviewed revision:** `revision/a2-v26-single-offset-law-inverse-top4-2026-09-12`  
**Immutable manuscript commit:** `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`  
**Manuscript tree:** `53d4ad26fcc4a84f427ef75ddb92b59c99c08d83`  
**Active entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Entry-point blob:** `a71285b0c1363c6aa950cde8fc498019a9478064`  
**Previous report:** v25, at `47057587d104074f0e1dde54c1d5d6abb629378f`  
**Review branch:** `review/a2-v26-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026  
**Requested standard:** Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, or Acta Mathematica.

This is an author-requested, AI-assisted independent referee-style assessment, not a commissioned journal report or an editorial decision. Its judgments concern the pinned A2 revision, not statistical A1 v36 or the entire theta-theory programme. The coverage and verification limits are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md).

## Recommendation

**Major revision. Do not accept the present submission at the requested top-four level.**

The main new single-offset inverse is a genuine improvement of the declared observation map. I found no contradiction in its four-density identity, fixed-anchor stability argument, or the inspected passage from the recovered actions to finite contact jets. The previous objections about common domination, the same-experiment graph-sampling benchmark, and cumulative-versus-restarted budgets have substantially been answered. It would be unjustified to repeat them unchanged or to demand another unrelated flagship merely because those objections were repaired.

There is, however, a new proposition that is **false as written**: the position-versus-scalar comparison does not require the even-flight design to start on the obstacle being deformed. When it starts on the fixed obstacle, both recorded endpoints lie on that fixed boundary. The alleged mutually singular position laws then have a common dominating measure and a common positive-density region. At the endpoint-only record level the scalar and position experiments are actually equivalent for this subfamily. Section 3 gives the explicit construction and the exact missing hypothesis.

A second correction concerns the use of an infinite Taylor-series equality in a theorem stated for arbitrary smooth contacts. This is locally repairable by finite Taylor remainders and a flat-variation argument; it is not a counterexample to the intended finite-jet theorem. The submission package also remains insufficiently integrated: its navigation still identifies v25, the v26 delta does not supply an updated response/active-source manifest, and the exact-head native workflow failed without executing any steps. These are actual presentation and verification deficiencies, but they must not be misrepresented as a demonstrated LaTeX error or as a refutation of the main inverse.

This recommendation is not a judgment that the programme should be abandoned or reduced. It is a judgment that a theorem-level observation error and the current submission-verification gap prevent acceptance now. Whether the corrected and fully assembled article clears the significance threshold of a particular top-four journal remains a separate editorial assessment. I do not certify that threshold merely from the number of revisions, formal statements, or finite diagnostic cases.

## 1. What was reviewed

The latest located revision branch was rechecked and still pointed to the commit above. Relative to the preceding v25 review tip it is two commits ahead with no divergence. The delta consists of seven new mathematical TeX modules, the modified native entry point, a new diagnostic script and two diagnostic records, and a v26 workflow. The root and manuscript-directory README files still advertise v25.

I examined the seven v26 mathematical modules, their statements and proofs, the active abstract and introduction, the previous report, and selected inherited dependencies. These include the weighted half-line inverse and envelope/jet-isolation proof through source line 450, the common-observation calibration and test implementation, the finite-signature and compact-inverse arguments, and the first part of the scalar boundary-information proof. This is a revision-focused mathematical audit, not a claim that every historical auxiliary theorem or every recursively included TeX file has been independently recertified.

No complete native checkout, whole-graph reference scan, manuscript compilation, PDF-page inspection, or execution of the author's 3343-case suite was performed in this review. An independently written standard-library diagnostic was executed in ordinary and optimized Python. Its 347 cases, recorded separately, check finite identities and a local two-flight witness; they are not substitutes for the proofs below.

Throughout, `P` means `papers/A2-v17-boundary-information-coarsening`. Source identifiers [S1]–[S12] at the end refer to the immutable manuscript commit, not a moving branch. Stable theorem labels are used instead of invented PDF page numbers.

## 2. Disposition of the v25 objections

| Previous issue | Assessment of v26 | Qualification |
|---|---|---|
| Exact planar positions permit direct graph acquisition in the same long-even experiment | Substantially closed | [S4] now proves the charged interpolation benchmark and the introduction explicitly accepts it. |
| The principal inverse must have a clearly different observation map from noiseless graph sampling | Substantially closed | [S2] uses only the two signed transverse endpoint laws at one fixed offset, plus the separately supplied gap and chart conventions. No graph ordinates occur in that intrinsic datum. |
| Common domination confused with domination by the reference member | Closed in the inspected revised statements | [S5] gives the Lebesgue/atomic reference measures and the Poisson envelope explicitly; [S6–S7] use the corrected distinction. This is not a certification of uninspected historical prose. |
| Prescribed-budget implementation might retain earlier, shorter flights | Closed | [S3] runs the selected stage afresh and expressly disclaims a diverging minimum for a cumulative archive. |
| Exact-position and scalar information need a rigorous comparison | Correct mechanism, incorrect statement scope | [S5] needs the endpoint-type hypothesis identified in Section 3. Under that hypothesis an even stronger comparison is available. |
| Exact-head complete native build | Not closed | The v26 run failed before any steps; the recursive source graph is expressly not checked by the committed changed-source audit. |
| Current response and active-source identification | Not closed in the v26 delivery | The two README entry points remain v25 and the v26 delta has no updated response or authoritative active-source manifest. |

The older v24 objections should not be resurrected merely because their repaired proofs are inherited. The inspected calibration does use a common physical record space, the moment map includes gaps, the final flight number is selected before the pilot, concentration is applied to an uncapped success sequence with cap failure added separately, and finite-signature uniqueness uses both local immersion and global separation. Those are substantive repairs.

## 3. Required correction R1: the position-singularity proposition omits the observed obstacle type

**Location:** [S5], `prop:v26-position-deficiency`, particularly source lines 84–150 and `eq:v26-position-deficiency`; also its invocation in [S1].  
**Classification:** a false-as-written auxiliary proposition, caused by a missing design hypothesis. The intended corrected proposition is valid. This does not refute the single-offset inverse or the global consistency theorem.

### 3.1 The missing quantifier is mathematically consequential

The proposition lets one obstacle vary by anchored homotheties and then permits “a fixed admissible even-flight design.” It concludes that distinct members' raw position laws are mutually singular. Its proof then assumes that the first recorded position lies on the varying obstacle. That fact is not in the statement.

An even bridge starts and ends at the same contact type. A design starting at the other, fixed obstacle observes two positions on the fixed obstacle; the intermediate visits to the varying obstacle are not part of the retained endpoint-position record. The complete growing collision array is explicitly a different experiment elsewhere in the manuscript. It cannot be inserted here to rescue the claim.

### 3.2 A persistent anchored geometric counterexample

Take two disks in a local facing channel, with

\[
 K_0=\{(x,y):(x+1)^2+y^2\le1\},\qquad
 K_{1,\lambda}=\{(x,y):(x-1-\lambda)^2+y^2\le\lambda^2\},
 \quad \lambda\in[1-\epsilon,1+\epsilon].
\]

The closest points are always \(p_0=(0,0)\), \(p_1=(1,0)\); the gap is one and both contact tangents are fixed. The second disk is a homothetic copy of \(K_{1,1}\) about \(p_1\). For small positive \(\epsilon\), this is a compact persistent strictly convex analytic channel. The proposition is local and does not impose the global signature-rigid cycle hypotheses; using disks here violates none of its printed hypotheses. The same fixed-versus-varied endpoint distinction also works for sufficiently small homothetic deformations of nonsymmetric analytic ovals.

Choose the admissible even design \(J=2\) starting at type zero, with physical time \(2+d\), where \(d>0\) is small. Its retained word is

\[
                    K_0\longrightarrow K_{1,\lambda}\longrightarrow K_0.
\]

Both recorded positions lie on the fixed contact arc

\[
                  X_0(u)=(-1+\sqrt{1-u^2},u).
\]

The finite successful endpoint density, in the manuscript's transverse coordinates, has the form

\[
 f_\lambda(u,v)=Z_\lambda^{-1}A_\lambda(u,v)
                      (d-E_{2,\lambda}(u,v))_+,
 \qquad A_\lambda>0.
\]

Here \(E_{2,\lambda}(0,0)=0\), and the finite action and flux are smooth in \(\lambda,u,v\) on a common contact box. There is therefore a common small square on which \(E_{2,\lambda}<d/4\) for every parameter. All these densities are positive on that square. If residual time is also retained, the analogous density is positive on the common set consisting of that square and \(d/4<r<d/2\).

The parameter-independent embedding

\[
              F_0(u,v)=(X_0(u),X_0(v))
\]

pushes the scalar endpoint laws to the raw position laws. Consequently the latter have a common dominating measure, namely the pushforward of Lebesgue measure on the fixed endpoint box, and a common region on which their densities are positive. They are **not mutually singular**. With residual time retained, take the product embedding with the identity in \(r\); the same conclusion holds.

At matching endpoint-only record levels, \(F_0\) and the transverse projection are parameter-independent inverse kernels on the supported contact arcs. Thus, on this subfamily,

\[
          \Delta(\mathsf E^{(k)}_{\rm sc},\mathsf E^{(k)}_{\rm pos})=0
          \qquad\text{for every finite }k\ge1,
\]

contrary to the printed lower bound \(1/2\). The inverse kernel may use the fixed obstacle: it is a known constant of the specified statistical family, not an unknown parameter-dependent transformation.

If the author instead intends the two experiments in this proposition to retain different residual-time components, those components must be defined explicitly. The singularity claim remains false for the displayed example. Moreover the raw position–time laws vary continuously in total variation on the common embedding. For any fixed finite \(k\), restricting \(\lambda\) to a sufficiently short nontrivial interval and using the constant kernel that outputs the central raw law makes the deficiency smaller than \(1/2\). Thus an unspecified residual-time convention does not save the printed universal conclusion.

This is an analytic counterargument, not a conclusion inferred from a simulation. The accompanying numerical check solves the two-flight stationarity equation at 27 finite parameter/endpoint choices, verifies positive mixed flux and a common interior residual-time region, and illustrates the same fixed embedding. It does not establish the continuum claim; smoothness and the common positive core do.

### 3.3 Required repair and impact

State that the fixed even-flight design **starts at the obstacle undergoing the homothety**, and that its first and last recorded positions belong to that obstacle. Define exactly which components are retained in \(\mathsf E_{\rm sc}\) and \(\mathsf E_{\rm pos}\). Then propagate this restriction to the introductory reference to the proposition.

With that addition the proof by disjoint homothetic boundary curves is valid: strict convexity makes distinct copies meet only at the anchor, and an arclength-density endpoint hits the anchor with probability zero. The omission is small in wording but reverses the statistical conclusion for a permitted design. A top-level statement about information loss must not leave this dependence implicit.

The two-type intrinsic inverse in [S2] and the two-type acquisition in [S3] do not assert singularity for an arbitrary single design. They are not contradicted by this example. No deletion of those theorems is called for.

## 4. Required clarification R2: smooth jets are not convergent analytic expansions

**Location:** [S8], `eq:v22-general-contact-jets`, `lem:v22-homogeneous-isolation`, and their use in [S2].  
**Classification:** a mathematical formulation and finite-jet bookkeeping correction; not a demonstrated failure of the intended smooth finite-jet conclusion.

The all-order signed-rigidity theorem assumes \(C^\infty\) contacts, but writes

\[
             \psi_b(y)=\frac{\kappa_b}{2}y^2+
                         \sum_{n\ge3}\frac{q_{b,n}}{n!}y^n
\]

as an equality of functions. For a general smooth contact, this equality is false. For example, on a sufficiently small patch,

\[
 \psi_\varepsilon(y)=\frac{\kappa}{2}y^2+
 \begin{cases}\varepsilon e^{-1/y^2},&y\ne0,\\0,&y=0\end{cases}
\]

is strictly convex for small \(\varepsilon\), has the same complete Taylor jet at zero as the quadratic graph, and is not the quadratic function. A smooth cutoff can be used away from the patch. This does not contradict the manuscript's actual smooth conclusion, which is recovery of every finite jet rather than equality of smooth boundary images. It does show why the displayed equality cannot silently bridge the smooth and analytic assertions.

Use a formal-jet symbol, or write for each finite \(M\)

\[
 \psi_b(y)=\sum_{n=2}^{M}\frac{q_{b,n}}{n!}y^n+R_{b,M}(y),
 \qquad R_{b,M}(y)=O(|y|^{M+1})
\]

under the corresponding finite differentiability bound. The proof should explicitly state that equal graph jets through order \(M\) give equal action jets through order \(M\), even when the remaining smooth graphs differ by flat terms. Differentiating finitely many polynomial jet coordinates alone is not an explicit treatment of all smooth remainders.

The existing envelope method supplies the repair. Along a sufficiently small interpolation between two graph pairs with equal \(M\)-jets, the direct length variation is \(O(|y|^{M+1}+|z|^{M+1})\). The weighted orbit bound and the finite-truncation envelope identity then give

\[
 |S_b^{(1)}(u)-S_b^{(0)}(u)|
 \le C_M|u|^{M+1}\sum_{i\ge0}\rho^{(M+1)i}
 =O_M(|u|^{M+1}).
\]

The already established finite-order smoothness makes the action jets through \(M\) identical. For a flat perturbation the argument applies for every \(M\), without implying equality of the action functions. Uniform versions require the compact smooth bounds used in the half-line argument, not merely a bound on a list of formal coefficients. After this clarification, the analytic continuation step can legitimately be reserved for real-analytic contacts.

If the infinite display was intended only as conventional formal-jet notation, say so explicitly and include the remainder argument. I do not count this as a fatal error in the determinant-one mechanism.

## 5. The mathematical progress that should survive the next revision

### 5.1 The single-offset law inverse is correct in the inspected model

For an interior square and known \(d>0\), write

\[
 f(u,v)=Z^{-1}B(u)B(v)(d-S(u)-S(v)),\qquad
 t(u)=\frac{S(u)}{d-S(u)}.
\]

Then

\[
 R_f(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)},\qquad
                       1-R_f(u,v)=t(u)t(v).
\]

Strict convexity makes \(t(a)>0\) at any fixed nonzero anchor in the interior. Hence

\[
 t(u)=\frac{1-R_f(u,a)}{\sqrt{1-R_f(a,a)}},\qquad
 S(u)=\frac{dt(u)}{1+t(u)}.
\]

The normalized amplitude follows from the remaining slice ratio. These identities keep the signs of the transverse coordinates and retain odd derivatives. No reflection symmetry or known amplitude is used.

The stability proof is appropriately fixed-order. Evaluation on fixed slices is bounded in \(C^M\); the density denominators, anchor defect and final reciprocal denominator stay away from zero on the stated compact sets. Products, reciprocals and one scalar square root are locally Lipschitz there. This is not differentiation of a pointwise square root through the minimum at \(u=0\).

The finite-flight corollary also has the right scope. Relative \(C^M\) convergence controls the interior density; the positive-part Lipschitz bound controls normalization over the common box; the fixed-order curvature and jet recursions are smooth near compact positive geometry. An assumed density-estimation error in \(C^M\) is not silently replaced by total variation or a finite sample. The author explicitly states this distinction, and it should remain.

The observation is one **complete two-variable conditional law** of each type at one known offset, plus gap and signed chart conventions. It is not a finite list of numerical measurements or recovery from one successful bridge. The manuscript's explicit distinction between law determination and observations is correct.

### 5.2 The all-order signed inverse carries the main geometric burden

The four-density cancellation supplies the action input; it does not itself prove the geometric inverse. In the inspected inherited proof, the weighted Green estimate gives a bounded half-line inverse, the nonlinear perturbation is controlled by a Neumann series, and finite-truncation differentiation removes internal orbit variations. The residual endpoint term decays with the fixed number of derivatives used.

At order \(n\), the pure graph-jet variation is evaluated on the linear orbit. The endpoint is counted once and interior sites twice, producing

\[
 1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),\qquad
 2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
                 =\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

Since \(\mathfrak r_0\mathfrak r_1=1\), the two-by-two block has determinant one. The fixed-order lower-triangular inverse is meaningful; determinant one alone would not imply uniform conditioning of an infinite jet map, and that stronger assertion is not made. R2 clarifies the smooth remainder step without invalidating these calculations.

This review does not elevate the selected checks into a fresh certificate of every upstream relative-law theorem. A complete source-pinned proof dependency map is still needed to make that wider assessment tractable.

### 5.3 The global estimator has a coherent existential proof

The compact pair-separation argument in [S3] correctly includes the gaps. If gaps agree and all the paired endpoint laws at the fixed offset agree, [S2] forces equality of the action jets. Bounded Lipschitz tests separate the remaining laws; compactness supplies a finite list and a positive separation margin. A finite template net and a deterministic tie rule avoid an unspecified measurable selection.

The acquisition order is also correct: choose tests and sample targets, choose the final even flight number, then choose pilot precision at that same flight number. The pilot supplies \(J|\widehat g-g|\le h\) and frame error \(O(\sqrt h)\). Fixed post-pilot times have small bias for the selected tests. Hoeffding's bound concerns the uncapped iid success sequence; cap exhaustion is added as a separate event. The recorded failures are not made costless.

The increasing-order argument uses a compact inverse modulus with a summable product-metric tail, not an asserted analytic-continuation rate. The budget rule explicitly restarts the selected stage. Non-effective constants and a nonconstructively selected finite library are not contradictions in this stated existence theorem. They do limit its quantitative algorithmic interpretation.

### 5.4 The statistical classification repair should not be undone

The scalar family is dominated by Lebesgue measure with the appropriate failure and censoring atoms. A zero-shift member need not dominate it. On each bounded Poisson strip, the envelope law dominates every truncated intensity law; the displayed exponential compensator and forbidden-point indicator give the correct Radon–Nikodym derivative.

The vector proof removes a collar of width \(\delta(\log(1/\delta))^{1/4}\), whose total product mass is negligible at the logarithmic scale. The truncated score's logarithmic second moment and controlled higher moments support the stated LAN representative. Finite-subexperiment convergence is explicitly not identified with an unproved uncountable-parameter deficiency assertion. The reference-model estimator is not advertised as a globally adaptive one.

The endpoint–time proof uses a different scale: a positive density at the moving ceiling produces an order-one rare boundary layer, while corner events have vanishing total probability. Waiting counts become ancillary at that scale under the printed \(j=o(\sqrt k)\) restriction. The full two-sided kernel theorem is an inherited dependency; its complete source was not freshly re-audited here. The conclusions in this paragraph are correspondingly limited to the revised argument and its explicit hypotheses.

## 6. Two useful sharpenings, not additional acceptance conditions

### 6.1 Under the corrected observed-type hypothesis, the deficiency is actually one

The lower bound \(1/2\) in [S5] is valid after R1 is repaired, but need not be the endpoint of the comparison. Suppose both experiments retain matching endpoint components, the first endpoint belongs to the varying homothetic obstacle, and the parameter interval is uncountable. Let \(P_\lambda\) denote the scalar \(k\)-record law and \(Q_\lambda\) the raw position law, for any fixed \(k\ge1\).

The scalar family has a common dominating probability \(\mu\), obtained by normalizing Lebesgue measure on a sufficiently large finite product box. For any proposed reconstruction kernel \(K\), every \(KP_\lambda\) is dominated by the probability \(K\mu\). Let \(A_\lambda\) be the set of raw records whose first position is on \(\partial K_\lambda\setminus\{p\}\). The sets \(A_\lambda\) are pairwise disjoint and \(Q_\lambda(A_\lambda)=1\). A finite measure gives positive mass to at most countably many disjoint measurable sets. There is therefore a parameter with \((K\mu)(A_\lambda)=0\), and then

\[
             (KP_\lambda)(A_\lambda)=0,\qquad
             \|KP_\lambda-Q_\lambda\|_{\rm TV}=1.
\]

This works for every kernel. With the manuscript's total-variation convention,

\[
            \delta(\mathsf E^{(k)}_{\rm sc},\mathsf E^{(k)}_{\rm pos})=1.
\]

The reverse deficiency is zero by fixed transverse projection. This proof explains why exact noiseless positions are exceptionally informative in this special subfamily. It is a general dominated-input/disjoint-support argument, not a new billiard-specific rigidity principle. It does not say one point reconstructs an arbitrary analytic obstacle, and it does not apply to the fixed-obstacle design of Section 3.

The existing weaker bound is not wrong merely because it is nonsharp. This strengthening is offered to clarify the information distinction and the role of the missing hypothesis, not to create another mandatory research target.

### 6.2 A support-preserving gauge clarifies what the density adds

At the level of the functional model in [S2], let \(d=1\), \(S(u)=u^2\) on \([-1,1]\), and

\[
 \phi_\varepsilon(s)=s+\varepsilon s(1-s)(s-1/2),
 \qquad 0<\varepsilon\le1/10,
 \qquad \widetilde S=\phi_\varepsilon\circ S.
\]

On \([0,1]\), \(\phi_\varepsilon\) is increasing and satisfies
\(\phi_\varepsilon(1-s)=1-\phi_\varepsilon(s)\). Thus

\[
 S(u)+S(v)<1\quad\Longleftrightarrow\quad
                  \widetilde S(u)+\widetilde S(v)<1.
\]

Both actions are strictly convex. Indeed

\[
 \phi_\varepsilon'(s)\ge1-\varepsilon/2,
 \qquad
 \phi_\varepsilon'(s)+2s\phi_\varepsilon''(s)
 =1+\varepsilon(-15s^2+9s-1/2)\ge1-13\varepsilon/2>0.
\]

Consequently \(\widetilde S''(u)>0\), but \(\widetilde S\ne S\). One support at one offset does not distinguish these functional-model actions. The four-density invariant does distinguish their associated separable-amplitude densities.

This is a witness in the abstract density/action class, not a claim that both displayed actions have been realized by a pair of physical billiard tables with all the global hypotheses. No such realization is needed to check the algebraic role of retaining density rather than support. Adding this kind of carefully scoped comparison would improve the exposition; it is not an objection to the already correct density inverse.

## 7. Significance at the requested journal level

The revised observation hierarchy is appreciably clearer. The principal intrinsic chain is now

\[
 \text{one-offset transverse laws and gap}
 \ \longrightarrow\ (S_0,S_1)
 \ \longrightarrow\ \text{labelled contact jets}
 \ \longrightarrow\ \text{analytic curves and marked gluing}.
\]

Its first arrow uses an elementary but useful density invariant; the difficult geometric content is in the physical relative-law construction and the second arrow. The last global steps use analytic continuation, unique signature matching, and marked holonomies under substantial stated hypotheses. The recovery formula \(L=VM^{-1}\) is not, by itself, the hard part of metric recovery. The author already says this, correctly.

The full-position global consistency theorem remains available by direct graph sampling as well. V26 acknowledges that fact and proves the benchmark instead of treating long flight numbers as an exclusion argument. Accordingly, the old objection that the paper fails to identify any contribution beyond direct interpolation is no longer an accurate description of this revision. The intrinsic transverse-law theorem is a genuinely different claim.

That does not automatically establish top-four significance. One-offset means a complete function-valued law, supplied signed origins and axes, and a separately retained onset gap. The global physical construction still obtains those axes through the richer position pilot. Fixed-order density-norm stability and compactness-based consistency do not constitute a sharp finite-budget statistical recovery theorem. None of those limitations refutes the results, and the manuscript explicitly acknowledges several of them. A referee should evaluate the actual theorem rather than infer a broader scalar-only, unregistered, quantitatively optimal experiment.

The related-work paragraph already distinguishes the relevant data maps. Primary records checked for this review confirm the limited comparisons below:

* De Simoi–Kaloshin–Leguil [L1] study marked-length determination for analytic open dispersing billiards with non-eclipse and additional symmetry/genericity hypotheses.
* Finamore–Leguil [L2] use an enriched marked length spectrum for finite-horizon Sinai billiards; equality of that enriched datum yields isometry.
* Osterman [L3] relates marked-length data for three analytic scatterers to analytic conjugacy near a homoclinic orbit and proves determination of the third scatterer from the other two and the marked length spectrum.
* Meister–Reiß [L4] establish Poisson-experiment equivalence for a nonregular regression model with endpoint discontinuities. A Gaussian/Poisson contrast is therefore not, in isolation, a new principle.

These records do not prove that A2 is subsumed by existing work, nor that it generalizes their theorems. No reduction between the observation maps has been established here. I have not performed an exhaustive novelty search or re-proved the cited literature. The most defensible significance case is the billiard-specific relative profile and signed all-order inverse, with the new one-offset law extraction as a clear strengthening. It is not the accumulation of compactness corollaries or repeatedly revised submission labels.

A new sharp budget bound, a scalar-only calibration theorem, or a relation to spectral data could add further significance, but **none is imposed here as a new mandatory condition for correcting v26**. The required next response is to repair the actual defect, clarify the smooth proof, and deliver an auditable complete manuscript; not to append another uncontrolled layer of claims.

## 8. Required correction R3: deliver a coherent, source-pinned submission

**Locations:** root `README.md`; `P/README.md`; `P/main.tex`; `P/diagnostics/v26-changed-source-audit.json`; exact-head native workflow.  
**Classification:** submission integration and verification, not a proof counterexample.

Both entry README files identify v25 as current and direct readers to its response, active-source manifest and verification record. The mathematical entry point is already v26. The twelve-file delta from the preceding review contains no updated v26 response or active-source manifest. The expected directory response path `P/RESPONSE_TO_REFEREE_V26.md` was not found. The committed changed-source audit expressly records `native_recursive_graph: not_checked_in_this_mode`.

The exact-head GitHub Actions run is [34666361925](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34666361925). Its `native-build` job, ID `103478925267`, has conclusion `failure`, an empty `steps` array, and runner ID zero. It completed on September 12, 2026 at 01:58:35 UTC; the workflow update was at 01:58:36 UTC. These facts establish that no build step was executed in that job. They do **not** establish that the TeX fails to compile, identify an infrastructure cause, or justify inventing unresolved-reference counts.

For the next submission, update the current navigation and provide a point-by-point v26-review response, a manifest of the actual active source graph, and an executed complete build at a fixed source commit for both declared native entry points and their retained auxiliary material. Record engine versions, logs and source/output hashes, together with actual reference/label/glyph diagnostics. A successful build is a typesetting and integration check, not a proof certificate. The existing mathematical sources and historical reports should be preserved; there is no request to delete the compendium to make the build easier.

The provenance defects matter because the article has a layered source graph and its strongest conclusion depends on older analytic estimates. They are not evidence that the density algebra is wrong. Likewise, a source audit of seven changed modules is useful but cannot certify the complete active article.

## 9. Executed independent diagnostics and their limits

The [independent program](diagnostics/check_v26_referee.py) was executed with Python 3.13.5 in ordinary and optimized mode. Outputs were byte-identical. It uses explicit exceptions rather than removable Python `assert` statements.

| Category | Finite cases |
|---|---:|
| Exact rational density inversion, including odd action terms | 75 |
| Exact determinant-one last-jet blocks | 72 |
| Exact support-gauge comparisons on a rational grid | 121 |
| Numerical fixed-obstacle two-flight witness | 27 |
| Exact polynomial interpolation-error scaling | 12 |
| Restarted-budget indexing | 40 |
| **Total** | **347** |

The script SHA-256 is `21833d91c202b91bf8d9f45d8964d562858ae4926ed0ab080f612d6ed71cc025`; its Git blob is `93ad02adfe8f9aa914e36ac6fb29f64c1833c547`. The local executed bytes and uploaded blob hash were compared. [The recorded result](diagnostics/results.json) includes the numerical residuals and the exact reviewed commit.

For the two-flight examples, the largest computed excess was approximately `0.00079992005`, the smallest positive value of `-W_uv` approximately `0.2363888665`, and the largest stationarity residual approximately `3.47e-18`. These illustrate a nonempty common interior for a fixed positive offset; they do not establish a continuum theorem by a finite grid. The continuum arguments in Sections 3, 4 and 6 are separate mathematical arguments.

The author's reported 3343 finite cases were inspected as a committed diagnostic record, not re-executed or independently certified here. Neither that count nor the new 347-case count verifies analytic continuation, an infinite-dimensional contraction, the full Poisson reverse kernel, or a complete native build.

## 10. Concrete requirements for the next revision

**R1 — Necessary mathematical correction.** Restrict the singular-position comparison to a design whose observed endpoint lies on the varying obstacle, define the compared record components, and acknowledge the opposite-type counterexample. Check the introductory invocation. The strengthened deficiency calculation in Section 6.1 is available but optional.

**R2 — Necessary proof clarification.** Replace the smooth infinite-series equality by formal-jet or finite-remainder notation, and explicitly handle smooth remainders/flat perturbations through the envelope estimate. Do not promote smooth jet determination to smooth boundary-image determination.

**R3 — Necessary submission repair.** Synchronize navigation and response/manifest files with the actual revision, and supply executed, source-pinned complete native-build evidence. Preserve all substantive mathematics and history. Do not mark the whole source graph verified based on changed-module diagnostics alone.

The point-by-point response should distinguish these requirements from optional strengthening suggestions. Passing the previous round's tests is not the same as proving every active assertion; conversely, a harsh review is not a license to ignore repairs that have actually been made. With R1–R3 unresolved, I withhold acceptance. With them resolved, the single-offset signed inverse deserves a fresh substantive assessment on its mathematical content, rather than an automatic repetition of the v25 rejection.

## Source index

All [S] references are pinned to `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`. Source URL prefix: `https://github.com/TrillionniumFoundation/theta-theory/blob/cefd89084682cc2e31d730eab1a4b8d8eaac0bbe/`.

**[S1]** `P/main.tex`; `P/article/01_introduction_v26.tex`. Current abstract, flagship statements and observation/literature comparisons.

**[S2]** `P/article/23f_single_offset_law_inverse_v26.tex`: `thm:v26-density-inverse`, `prop:v26-density-stability`, `cor:v26-finite-flight-inverse`, `thm:v26-single-offset-global`.

**[S3]** `P/article/25b_augmented_global_reconstruction_v26.tex`: `lem:v26-single-offset-separators`, `thm:v26-fixed-order-physical`, `thm:v26-global-physical-reconstruction` and restarted budget construction.

**[S4]** `P/article/29b_direct_position_benchmark_v26.tex`: `prop:v26-position-jets` and the comparison to the law-valued inverse.

**[S5]** `P/article/18f_domination_and_position_comparison_v26.tex`: `prop:v26-common-domination`, `prop:v26-position-deficiency`, `eq:v26-position-deficiency`. The design omission is in the latter proposition, not in the common-domination proposition.

**[S6]** `P/article/18a_vector_boundary_information_v26.tex`: full section, including common-collar equivalence, LAN, quotient experiment, testing and minimax statements.

**[S7]** `P/article/18c_full_endpoint_time_information_v26.tex`: full section, including the Poisson limit and complete stopped endpoint–time experiment. Its separately referenced inherited two-sided-deficiency theorem was not fully reread in this review.

**[S8]** `P/article/23a_signed_endpoint_rigidity_v22.tex`, source lines 1–450: support inverse, leading geometry, weighted inverse, envelope limit, homogeneous isolation and last-jet blocks.

**[S9]** `P/article/25a_common_observables_v25.tex`, inspected material through the test-implementation proof near line 270: common records, localization, pilot, normalization and finite-test bias.

**[S10]** `P/article/23e_signature_stability_v25.tex`, inspected material through the compact-inverse proof near line 280: finite embedding, noisy matching, gluing persistence and product-metric modulus.

**[S11]** `P/article/18_boundary_information_v18.tex`, source lines 1–230: scalar density assumptions, support-exclusive mass and critical information proof. The rest of that inherited section was not separately recertified.

**[S12]** root `README.md`; `P/README.md`; `P/diagnostics/v26-changed-source-audit.json`; v26 commit metadata and twelve-file delta; workflow run `34666361925` and job `103478925267`.

**Previous report:** `reviews/a2-v25-independent-harsh-top4-2026-09-12/REFEREE_REPORT.md` at `47057587d104074f0e1dde54c1d5d6abb629378f`. Its judgments were re-evaluated rather than adopted as proof certificates.

### Primary literature records checked on September 12, 2026

**[L1]** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), last revised August 17, 2022; related DOI `10.1007/s00222-023-01191-8`.

**[L2]** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), submitted October 21, 2025; the accessed record displayed version 1.

**[L3]** O. V. Osterman, *On length spectrum rigidity of dispersing billiard systems*, Journal of Modern Dynamics 19 (2023), 847–878, [publisher record](https://www.aimsciences.org/article/doi/10.3934/jmd.2023025), DOI `10.3934/jmd.2023025`.

**[L4]** A. Meister and M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248](https://arxiv.org/abs/1101.5248), submitted January 27, 2011.

Only the primary records and their stated observation/hypothesis comparisons are used here. This is not an exhaustive literature review or a claim of complete proof-level verification of these external papers.
