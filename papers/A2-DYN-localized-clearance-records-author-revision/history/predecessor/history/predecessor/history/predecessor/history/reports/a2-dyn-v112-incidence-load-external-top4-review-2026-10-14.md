# External top-four referee report on A2-DYN revision 112

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v112-referee-response-2026-10-14`, `revision/a2-dyn-v112-referee-copy-2026-10-14`  
**Reviewed author commit:** `45015de51c652bcdaca13123bf65627bf199b2ab`  
**Reviewed repository tree:** `f377dc19c5df4be7c620e0bbed2caabf3b28042d`  
**Active manuscript directory:** `papers/A2-DYN-v112-referee-response`  
**Active mathematical source:** 269 numbered core modules; revision 112 adds modules 268--269 and supplies completion/indexing additions in the active copies of modules 265--266  
**Immediate author baseline:** revision 111, commit `8c617cafa5e5493e26817401e866b2415522f7c0`  
**Frozen revision-111 packet tree:** `790e627efe3a89a4549123d7e9acacf24089c287`  
**Controlling report:** `reviews/a2-dyn-v111-guard-witness-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling review commit / report blob:** `ddd59615ed6e7073f9cc85bf76ab269cf0b3889a` / `a9173eb21f73bedd968ccfadfb3ee87215db7a20`  
**Exact-SHA qualification at review freeze:** response run `38561460974`, queued; referee-copy run `38561508199`, queued  
**Date:** 14 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 112 is a genuine theorem-bearing response to the revision-111 report. It does not merely relabel the localized residual, replace the original exact event by an averaged event, or multiply a per-itinerary estimate by the number of physical words.

The revision adds two substantive mechanisms.

First, it retains both the collision-end depth and the additional logarithmic severity of every original incidence witness. For

\[
J_\varepsilon(x)
 =\{1\le i<m:c_i(x)<2\varepsilon r^{d_i}\},
 \qquad r=q_0^{1/4},
\]

it defines

\[
\mathscr L_\varepsilon(x)
 =\sum_{i\in J_\varepsilon(x)}
       \log\frac{2\varepsilon}{c_i(x)}.
\]

Relative to the retained target-roof marked-pressure theorem, it proves the exponential-moment estimate

\[
\left\|D[e^{\lambda\mathscr L_\varepsilon}]\right\|_\infty
 \le C_\star
 \exp\!\left\{
  \frac{4K_\star\varepsilon}
       {e^{\alpha(1-\lambda)}-1}
 \right\},
 \qquad 0<\lambda<1,
\]

where \(\alpha=|\log q_0|/4\). Chernoff optimization gives

\[
\left\|D[\mathbf1_{\{\mathscr L_\varepsilon\ge u\}}]\right\|_\infty
 \le C_\star
 \min\{1,e^{-u+2\sqrt{b_\varepsilon u}}\},
 \qquad
 b_\varepsilon=4K_\star\varepsilon/\alpha.
\]

At \(u=(2+\eta)\log(m+1)\), this produces an actual \(m^2\)-normalized positive payment. In particular, a single sufficiently severe shallow incidence can now be paid without being deep and without belonging to a large witness set.

Second, the revision preserves the actual two-ended depth multiset rather than replacing it by its total threshold mass. It proves matching quadratic exponents for the elementary symmetric polynomial

\[
E_{m,s}(r)=e_s((r^{d_i})_{1\le i<m}),
\]

namely

\[
r^{\lfloor(s+1)^2/4\rfloor}
 \le E_{m,s}(r)
 \le
 \frac{(s+1)r^{\lfloor(s+1)^2/4\rfloor}}
      {(r;r)_\infty^2}
\]

when the lower bound is applicable. This yields a target-roof witness-count tail whose normalized payment threshold is of order \(\sqrt{\log m}\), improving the preceding \(\log m/\log\log m\) schedule.

The revision also supplies two requested presentation/completion steps in the active copies of the inherited argument: a monotone exhaustion for unbounded marked weights in the roof--angle change of variables, and explicit marked-step indexing that includes adjacent marks, a final mark, and zero-length blocks.

I audited

- `core/265_global_roof_angle_uniqueness.tex`;
- `core/266_target_roof_marked_pressure.tex`;
- `core/267_uniform_incidence_witness_summation.tex`;
- `core/268_joint_incidence_load_concentration.tex`;
- `core/269_positive_low_load_source_reduction.tex`;
- `main.tex` and `inputs.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `PROOF_LEDGER.md`;
- `SOURCE_MANIFEST.json` and `PUBLICATION_STATUS.json`;
- the validation record; and
- the revision-111 report which posed the remaining localized-shortage problem.

Within the inherited hypotheses actually stated in those files, I found no decisive sign error in the new product majorization, no incorrect Chernoff optimizer, no missing factor in the two-ended depth polynomial, no off-by-one error in the new marked-step display, no invalid positive-source subtraction, no hidden independence assumption, no uncontrolled physical-word multiplier, and no illegal insertion of a collision-dependent spectral or roof window into a fixed-window estimate.

The negative recommendation is nevertheless forced by the exact endpoint of the revision. The new scalar theorem is

\[
\mathcal E_M
 \le
 \mathcal H_M(\mathsf R_B^{\rm low})
 +C_MB^{-1/384},
\]

where

\[
\mathsf R_B^{\rm low}
 =
 (\mathsf U_B^{\rm low}-K_BP_{r_B}^{\rm ng})_+.
\]

The manuscript proves that the unchanged exact-label raw pointwise assertion is equivalent to

\[
\mathcal H_M(\mathsf R_B^{\rm low})\longrightarrow0
 \qquad\text{for every fixed }M.
\]

**No theorem establishes this limit.**

The surviving source still allows:

- shallow incidence witnesses with total load below \((2+\eta)\log(m+1)\);
- a bounded or slowly growing number of incidences whose individual severities are not enough to supply the required \(m^{-2}\) gain;
- clearance witnesses at arbitrary collision depth, including tangencies to unvisited disks;
- positive source with no incidence witness at all and only a clearance witness;
- capacity deficiency of the full nongrazing comparison pool;
- positive critical-entrance and section-cut contributions not paid by the incidence theorem; and
- singular endpoint or pairing configurations outside the inherited regular physical-source hypotheses.

The source manifest and publication-status file correctly keep the remaining low-load shortage, the localized-shortage limit, the full raw-return LLT, and closure of the primary referee request false.

Thus revision 112 removes another nontrivial positive part of the exact obstruction in the correct pointwise topology, but the remaining positive source is still the upper half of the organizing theorem. It is not a secondary error after a completed local limit theorem.

At the requested four-journal benchmark, the present state does not support acceptance. A positive recommendation would require a proof of the complete remaining shortage, or a reformulation around a complete theorem of independent top-four breadth and significance. Revision 112 supplies neither yet.

## 2. Frozen source and chronology

The two reviewed author branches both resolve to

`45015de51c652bcdaca13123bf65627bf199b2ab`.

The repository tree at that commit is

`f377dc19c5df4be7c620e0bbed2caabf3b28042d`.

The active article is

`papers/A2-DYN-v112-referee-response/main.tex`.

The complete revision-111 packet is preserved under

`papers/A2-DYN-v112-referee-response/archive/v111`,

with exact tree

`790e627efe3a89a4549123d7e9acacf24089c287`.

Revision 112 starts from the controlling revision-111 review commit

`ddd59615ed6e7073f9cc85bf76ab269cf0b3889a`,

whose reviewed author source was

`8c617cafa5e5493e26817401e866b2415522f7c0`.

The controlling report had accepted the mathematical coherence of the target-roof incidence-pressure chain relative to its inherited inputs, but emphasized that its unscaled \(O(\varepsilon(B))\) all-incidence bound cannot be multiplied by \(m^2\) at a fixed outer stage. It identified shallow incidence, clearance, capacity deficiency, critical entrances, section cuts, and singular configurations as remaining classes.

Revision 112 responds to the incidence part of that criticism. It adds modules

- `core/268_joint_incidence_load_concentration.tex`;
- `core/269_positive_low_load_source_reduction.tex`.

It also extends the active copies of modules 265--266 with the monotone unbounded-weight completion and explicit marked-step indexing requested by the preceding report. The preceding versions remain frozen in `archive/v111`; the current packet does not rewrite its historical source.

The present review branch starts directly from the exact revision-112 author commit and adds only this report under

`reviews/a2-dyn-v112-incidence-load-external-top4-review-2026-10-14/`.

No author manuscript, author branch, workflow, previous report, archived source tree, or unrelated paper is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v112-source-and-manuscript.yml`.

At the freeze of this report, the exact-SHA runs were

- response branch run `38561460974`: `queued`, conclusion `null`;
- referee-copy branch run `38561508199`: `queued`, conclusion `null`.

I therefore do not describe revision 112 as remotely qualified at the review freeze.

The author records a successful local build of a 31-page article, three stabilized LaTeX passes, no unresolved references, no multiply defined labels, and no overfull boxes. The local finite checks include 36,372 new load/depth/source cases, the inherited optical and marked-pressure checks, and rendered-page inspection. The normal and optimized Python outputs are reported to agree byte-for-byte.

These are useful source, assembly, and finite-algebra checks. A later successful remote run would strengthen the reproducibility record. It would not certify

1. the original incident-component pairing-sheet construction;
2. one-copy physical multiplicity after all sheet and seam identifications;
3. the historical uniform geometric pressure theorem;
4. the stable optical comparison on the complete claimed regular family;
5. the full-area two-sided regular-set passage under the roof--angle map;
6. every endpoint/coarea convention at singular extensions;
7. collision-uniform clearance-witness summation;
8. abundance of nongrazing comparison capacity;
9. decay of \(\mathsf R_B^{\rm low}\); or
10. the full exact-label raw pointwise local limit theorem.

The packet correctly distinguishes finite diagnostics and source qualification from proof certification.

## 4. Scope of this review

The substantive audit concentrates on

1. the monotone completion of the target-roof change of variables for unbounded positive weights;
2. the explicit geometric-pressure and stable-optical input statement;
3. marked-step indexing and block reconstruction;
4. the product majorization for the incidence load;
5. the geometric sum over collision-end depths;
6. Chernoff optimization and its quantifiers;
7. the two-ended depth-polynomial coefficient bounds;
8. the square-root-logarithmic count schedule;
9. the exact positive source partition;
10. the positive-part residual comparison;
11. the collision-normalized payment at the original target roof;
12. the distinction between incidence and clearance; and
13. the exact classes retained in the final shortage.

The first 264 historical modules, and the wider spectral, arithmetic, Gaussian, coarea, optical, pressure, and pairing-space pipeline, are treated as source-pinned inputs except where their interfaces are directly needed for the new argument. This report does not independently reconstruct that entire historical chain.

## 5. The inherited obstruction from revision 111

Revision 111 had reduced the original pointwise error to

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
 (\mathsf U_B^{\rm loc}-K_BP_{r_B}^{\rm ng})_+.
\]

It paid two source classes in the required target-roof topology:

- incidence witnesses beyond a logarithmic collision-end layer; and
- trajectories carrying at least \(s_m\asymp\log m/\log\log m\) incidence witnesses.

The target-roof marked-pressure theorem used to obtain those payments is unscaled. Its basic all-incidence consequence is of order \(\varepsilon(B)\), with no \(m^{-2}\) factor. The revision-111 report therefore correctly rejected any inference that all remaining incidence source is small.

Revision 112 keeps the same original source, comparison pool, exact labels, and order of limits. It seeks additional collision-dependent gain from the *amount* of incidence degeneracy, rather than merely from the existence of an incidence witness.

This is the correct direction of attack.

## 6. Monotone completion for unbounded marked weights

Proposition `prop:v112-exhaustion` in module 265 fills an important measure-theoretic gap in the presentation of the target-roof formula.

At fixed \(m,R,n,k\), the proof covers the noncritical regular endpoint domain by countably many relatively compact local charts on which

\[
Q\mapsto(F(Q),\arg g(Q))
\]

is a \(C^1\) diffeomorphism. It disjointizes those charts by Borel source pieces, fixes an angular seam, and defines

\[
h_N=\min\{h,N\}\mathbf1_{\cup_{j\le N}B_j}.
\]

Ordinary change of variables is applied only to bounded weights on finitely many charts. The proof then passes to the unbounded nonnegative weight by monotone convergence and Tonelli, before using the pressure estimate to establish finiteness.

This is the right logical order. It does not assume integrability of \(\prod_{i\in S}c_i^{-1}\) in order to prove the roof-fiber estimate which supplies that integrability.

The argument also states the relevant null-set boundary: the complement of the two-sided regular set has zero collision area, local Lipschitz coordinate maps send the relevant chart pieces to target-null sets, and the fixed-radius roof identity is recovered by Fubini. No radius-independent exceptional set is claimed.

I do not find a decisive flaw in this completion. It remains load-bearing and should be reconstructed by a billiards/coarea specialist, especially at singular seams and in the precise convention for the extended positive weight on the discarded zero-area set.

## 7. Explicit pressure input and marked-step indexing

Module 266 now states the inherited geometric input as an explicit input statement. In particular it distinguishes

- Euclidean arclength on the true stable line in collision coordinates \((s,\varphi)\);
- the stable Jacobian cocycle used consistently on every block;
- the endpoint derivative \(\omega\) in the original \((\alpha,p)\) variables;
- the full-area two-sided regular set;
- the physical-word pressure bound; and
- the stable optical inequalities.

The declared inputs are

\[
\sup_{R,l}P_l(R)\le Q_*,
\qquad
\omega\le C_0c_mJ^sT^m,
\qquad
J^sT/c\le C_1.
\]

The revision correctly describes them as retained unconditioned geometric inputs rather than as a new exact-label or twisted pressure theorem.

The marked-step display also resolves the indexing ambiguity noted in the preceding report. For marks

\[
S=\{i_1<\cdots<i_s\}\subset\{1,\ldots,m-1\},
\]

the surviving block lengths are

\[
i_1,
\quad i_2-i_1-1,
\quad\ldots,\quad
m-i_s-1.
\]

The example \(m=7\), \(S=\{1,2,6\}\) gives \((1,0,3,0)\). Thus adjacent marks, a final interior mark, and the convention \(P_0=1\) are all explicit.

Within the stated physical alphabet assumption, the reconstruction by the unmarked blocks and at most \(D^s\) deleted step symbols yields the claimed product of pressure sums. I found no off-by-one defect in this revised display.

## 8. The incidence-load exponential moment

The key pointwise inequality in module 268 is sound.

Put

\[
y_i=2\varepsilon/c_i.
\]

On the witness event \(i\in J_\varepsilon\), one has

\[
y_i>r^{-d_i}.
\]

For \(0<\lambda<1\),

\[
y_i^\lambda
 =y_i y_i^{-(1-\lambda)}
 \le y_i r^{(1-\lambda)d_i}.
\]

Therefore

\[
e^{\lambda\mathscr L_\varepsilon}
 =\prod_i
   \left[1+(y_i^\lambda-1)
              \mathbf1_{\{i\in J_\varepsilon\}}\right]
 \le
 \prod_i\left(
  1+\frac{2\varepsilon r^{(1-\lambda)d_i}}{c_i}
 \right).
\]

This is a deterministic positive inequality on each trajectory. No collision independence is used.

The inherited product-insertion theorem applies with

\[
a_i=2\varepsilon r^{(1-\lambda)d_i}.
\]

Since at most two indices have each positive depth,

\[
\sum_i a_i
 \le
 4\varepsilon\sum_{d\ge1}r^{(1-\lambda)d}
 =
 \frac{4\varepsilon}
      {e^{\alpha(1-\lambda)}-1}.
\]

This gives the displayed moment estimate after the complete physical sum. I found no missing factor in this passage.

The theorem is explicitly relative to the marked-pressure input. It is not an independent re-proof of the uniform pressure and optical chain.

## 9. Chernoff optimization and normalized payment

Positivity gives

\[
\mathbf1_{\{\mathscr L_\varepsilon\ge u\}}
 \le e^{-\lambda u}e^{\lambda\mathscr L_\varepsilon}.
\]

Writing \(v=1-\lambda\) and using

\[
e^{\alpha v}-1\ge\alpha v,
\]

the exponent is bounded by

\[
-u+vu+b_\varepsilon/v.
\]

When \(u>b_\varepsilon\), the choice

\[
v=\sqrt{b_\varepsilon/u}
\]

lies in \((0,1)\) and yields

\[
-u+2\sqrt{b_\varepsilon u}.
\]

This optimization is correct. It is performed inside a finite-count inequality valid for every \(0<\lambda<1\); it is not a collision-dependent choice inserted into a theorem available only at one fixed spectral width.

For

\[
u_m=(2+\eta)\log(m+1),
\]

multiplication by \(m^2\le(m+1)^2\) gives exponent

\[
-\eta\log(m+1)
 +2\sqrt{b_{\varepsilon(B)}(2+\eta)\log(m+1)}.
\]

At fixed outer \(B\), the square-root term is \(o(\log m)\). Hence the load source has zero ordered \(m^2\)-normalized height.

This is a genuine pointwise gain which was absent in revision 111.

## 10. The two-ended depth polynomial

The deterministic coefficient estimate in Lemma `lem:v112-depth-poly` is also coherent.

The collision-depth multiset is contained in two copies of

\[
1,2,3,\ldots.
\]

Coefficientwise positivity therefore bounds its generating polynomial by

\[
\prod_{d\ge1}(1+zr^d)^2.
\]

For one copy, the coefficient of \(z^a\) is

\[
\frac{r^{a(a+1)/2}}{(r;r)_a}.
\]

Splitting \(s\) marks as \(a\) from one end and \(s-a\) from the other gives the middle sum in the stated bound. Its smallest exponent is

\[
f(s)=\left\lfloor\frac{(s+1)^2}{4}\right\rfloor.
\]

The denominator estimate using \((r;r)_\infty>0\) is in the correct direction.

For the lower bound, the \(s\) smallest available depths have total \(f(s)\) whenever \(m\ge s+1\). That product is one term of the finite elementary symmetric polynomial. The manuscript correctly warns that this is a lower bound for a deterministic depth polynomial, not a lower bound for a physical roof density.

The resulting logarithmic rate

\[
\log E_{m,s}(r)
 =-\frac{\alpha}{4}s^2
  +O_r(s+\log(s+1))
\]

is justified by the two-sided coefficient bounds.

## 11. Quadratic witness-count tail

The count event satisfies the usual positive elementary-symmetric bound. Applying the unrelaxed marked-pressure estimate with thresholds

\[
2\varepsilon r^{d_i}
\]

gives

\[
\|D[\mathbf1_{\{N^\varepsilon\ge s\}}]\|_\infty
 \le
 \frac{C_\star(s+1)(2K_\star\varepsilon)^s}
      {(r;r)_\infty^2}
 r^{f(s)}.
\]

At

\[
\sigma_m=
 \left\lceil
 2\sqrt{\frac{(2+\eta)\log(m+1)}{\alpha}}
 \right\rceil,
\]

the quadratic exponent pays \((m+1)^{-(2+\eta)}\). The remaining terms grow only like \(O_B(\sqrt{\log m}+\log\log m)\) at fixed \(B\). Thus the normalized height tends to zero.

This calculation is correct as an upper bound. It does not prove that the threshold is sharp for physically realized trajectories, and the manuscript does not claim such sharpness.

In the final source description, the load inequality already implies

\[
\alpha f(N)<u_m
\]

on the retained source. The separate count theorem is therefore best viewed as an explicit quantitative consequence and an independent finite-count comparison with the older factorial schedule, not as a second missing payment needed for the final partition.

## 12. Exact positive source preservation

The source partition in module 269 is exact.

Let \(\mathcal Z_{B,m}\) denote the previously paid deep/many incidence set and let

\[
\mathcal Q_{B,m}
 =\{\mathscr L_{\varepsilon(B)}\ge u_m\}.
\]

Then

\[
\mathsf U_B^{\rm per}
 =
 \mathsf U_B^{\rm exc}
 +\mathsf U_B^{\rm load}
 +\mathsf U_B^{\rm low}
\]

is a disjoint positive identity before the roof pushforward and remains exact afterwards.

The same full nongrazing capacity \(K_BP_{r_B}^{\rm ng}\) is used in both residuals. Since the positive-part map is monotone and one-Lipschitz,

\[
0\le
\mathsf R_B^{\rm loc}-\mathsf R_B^{\rm low}
\le
\mathsf U_B^{\rm load}.
\]

This is the correct algebraic comparison. The new payment is not spent twice and no source coefficient is replaced by a signed surrogate.

The resulting error bound and necessity direction preserve the original order of limits and the original scalar equivalence.

## 13. What the retained low-load support actually says

On \(\mathsf U_B^{\rm low}\), the revision proves

\[
\alpha\sum_{i\in J}d_i<u_m,
\qquad
\alpha f(N)<u_m,
\qquad
\prod_{i\in J}\frac{c_i}{2\varepsilon(B)}>e^{-u_m}.
\]

Consequently

\[
N<2\sqrt{u_m/\alpha}
\]

and every incidence witness satisfies

\[
c_i>2\varepsilon(B)e^{-u_m}.
\]

These are meaningful restrictions. They prevent a large accumulated incidence load, a sufficiently severe single incidence, and a large witness count.

They do **not** imply that the remaining source is small in the required topology. For example, the restrictions are compatible with one or a few shallow incidences whose \(c_i\) are comparable to the original \(\varepsilon(B)\)-scale threshold. The target-roof pressure theorem gives an unscaled upper bound for such source; at fixed \(B\), that bound does not acquire the required \(m^{-2}\) factor merely because the witness set is small.

Thus the phrase “low load” is a classification, not a smallness theorem.

## 14. Clearance remains a separate obstruction

The revision is appropriately explicit that

\[
\mathscr L_\varepsilon
\]

contains only actual incidence witnesses. It contains no inverse clearance, third-disk distance, or unvisited tangency factor.

The persistent guard can be positive because of a clearance witness even when

\[
J_\varepsilon=\varnothing.
\]

Such a state has zero incidence load and survives every theorem in module 268. A clearance witness may occur at arbitrary depth and may concern a disk not visited by the physical itinerary. The incidence marked-pressure theorem does not automatically sum these witnesses.

Any complete proof of `eq:v112-remaining` must therefore add a genuinely new clearance mechanism, or a direct source-capacity argument which controls clearance-only states without pretending they are incidence events.

This is now the clearest unresolved geometric component of the manuscript.

## 15. Capacity shortage also remains

Even after incidence localization, the final residual is

\[
(\mathsf U_B^{\rm low}-K_BP_{r_B}^{\rm ng})_+.
\]

The load theorem estimates a positive part of the **source**. It does not prove that the full nongrazing pool has enough comparison capacity to pay the low-load source at every relevant target roof.

Accordingly, a state can satisfy all new incidence restrictions and still lie in a capacity-deficient roof fiber. The positive comparison shortage is retained with its original coefficient.

The manuscript needs either

1. a collision-uniform capacity-abundance theorem for the low-load source;
2. a direct pointwise estimate for the low-load source strong enough to bypass comparison capacity; or
3. a positive decomposition covering the remaining geometric classes, with every component paid in the same essential-height topology.

Finite-count source classification alone does not close this gap.

## 16. Critical entrances, section cuts, and singular extensions

The new theorems act on the regular incidence source relative to the inherited physical/coarea inputs. They do not establish every singular endpoint extension.

Positive critical-entrance traces, section-boundary terms, singular pairing configurations, and any source outside the verified regular comparison space remain subject to the older hypotheses and reductions. They cannot be deleted because the incidence load happens to be small or empty.

The source manifest correctly leaves independent human review and formal proof certification false. A complete journal proof will require a specialist reconstruction of these interfaces, not only additional finite algebra.

## 17. Order of limits

The revision observes the required quantifier order.

At each outer stage, the quantities

\[
\varepsilon(B),h_B,r_B,\gamma_B,K_B
\]

are fixed. The load threshold \(u_m\) classifies a trajectory at finite collision count inside a pointwise inequality valid for every threshold. The full physical sum, exact-label/radius/roof suprema, and collision limsup are then taken, with \(B\to\infty\) last.

No outer spectral width or comparison window is made collision-dependent. The Chernoff parameter is optimized only inside an inequality valid simultaneously for all \(0<\lambda<1\).

I found no limit-order violation in modules 268--269.

## 18. Top-four significance

The target-roof marked-pressure theorem and its new incidence-load consequences are technically substantial within this project. In particular, the revision achieves a real collision-normalized payment without an independence assumption and without counting physical words naively.

Nevertheless the article remains organized around an exact-label raw pointwise local limit theorem which is still unproved. The new theorems are specialized to the triangular Lorentz family and depend on a long source-pinned optical/pressure/coarea pipeline. The manuscript has not isolated a complete general theorem, applicable across a broad class of singular hyperbolic systems, whose independent significance could replace completion of the stated main result at the requested benchmark.

A chain of increasingly precise positive-source reductions is valuable research progress. It is not, by itself, a completed top-four paper while the manuscript's own governing theorem remains equivalent to an unproved positive shortage limit.

## 19. Required mathematical work for another revision

A further revision capable of changing the recommendation should prove the remaining estimate

\[
\lim_{B\to\infty}
\limsup_{m\to\infty}
\sup_{R,n,k}m^2
\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
(\mathsf U_{B,m}^{\rm low}(t)-K_BP_{r_B,m}^{\rm ng}(t))_+
=0.
\]

The proof must address, rather than rename, the following classes.

### 19.1 Clearance-only and unvisited-tangency source

Construct a target-roof summation or source estimate for the actual clearance witnesses, including witnesses involving unvisited disks. State the weight, multiplicity, geometric depth, and one-copy physical summation explicitly. Do not infer it from the incidence theorem.

### 19.2 Low-load shallow incidence

Show why a bounded-total-load, \(O(\sqrt{\log m})\)-witness source has vanishing normalized height, or show that it is paid by nongrazing capacity. A count bound alone is not enough.

### 19.3 Capacity abundance

Prove that the full nongrazing pool is quantitatively sufficient on the retained source, or replace it with a different positive mechanism whose complete shortage is controlled in the original roof topology.

### 19.4 Singular and boundary configurations

Close the positive critical, section-cut, singular-endpoint, and pairing-seam terms under the same exact event and normalization.

### 19.5 Independent reconstruction

Obtain specialist verification of the family-uniform pressure theorem, stable optical comparison, roof--angle change of variables, physical multiplicity, and null-set passage. Software qualification cannot substitute for this audit.

## 20. Presentation requests

The current presentation is substantially clearer than the previous packet. I nevertheless recommend the following refinements.

1. State near the main theorem that the new \(\sqrt{\log m}\) count restriction is already implied on the final retained source by \(\alpha f(N)<u_m\), while Theorem `thm:v112-count` gives a separate direct tail estimate.
2. Keep the phrase “low load” consistently qualified as “low incidence load.” It gives no clearance localization.
3. In the monotone-exhaustion proposition, state explicitly how the unbounded marked weight is defined on the zero-area excluded set, even if the value is irrelevant to the resulting measure.
4. Keep every statement of the geometric-pressure theorem explicitly labeled as a retained input until an independent specialist reconstruction is supplied.
5. Update the qualification paragraph only from actual completed run records; do not infer success from the existence of the workflow or from local checks.

These are secondary to the missing estimate.

## 21. Final assessment

Revision 112 makes real and mathematically coherent progress relative to its stated inputs.

It

- completes the unbounded-weight roof--angle passage by monotone exhaustion;
- clarifies marked-step reconstruction;
- proves a joint depth/severity exponential moment;
- pays high incidence load in the required \(m^2\)-normalized roof topology;
- obtains the correct quadratic exponent for the two-ended depth polynomial;
- improves the direct count threshold to order \(\sqrt{\log m}\);
- preserves the original positive source by an exact identity; and
- states its remaining boundary honestly.

I found no decisive error in the new finite-count mathematics.

But the final low-incidence-load shortage is unproved, clearance is not summed, comparison capacity may still be deficient, and the full exact-label raw pointwise local limit theorem remains open within the manuscript.

Accordingly, my recommendation at the requested benchmark is

**reject in the present form.**

The strongest next step is not another reclassification of the incidence residual. It is a complete target-roof theorem for clearance and capacity abundance, or a direct microscopic source estimate which proves `eq:v112-remaining` in the original order of limits.
