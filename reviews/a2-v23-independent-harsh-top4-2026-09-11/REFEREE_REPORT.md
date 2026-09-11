# Independent harsh referee-style report on A2 v23

**Manuscript:** Qian Qi, *Boundary laws, intrinsic rigidity, and multiscale physical information in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the American Mathematical Society*  
**Author revision branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Revision-branch head reviewed:** `55b2d3b41acd3e0beb7e9071c13e54637137f9ad`  
**Canonical manuscript-source commit:** `8840bf01ee8a7752504d2913bf00af54656afbb5`  
**Immediate predecessor report:** `reviews/a2-v22-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Principal active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and is not an editorial decision by any journal named above. I have reviewed the active v23 theorem chain and the new modules introduced specifically to answer the v22 report. I treat the response letter and revision manifest only as navigation aids; mathematical claims are assessed from the active manuscript sources.

## 1. Recommendation to the editor

**Recommendation: reject in the present form at the requested top-four level, while encouraging one further substantial reconstruction and a fresh assessment.**

This recommendation should not be read as a repetition of the v22 report. V23 is a genuine mathematical advance over v22. The most serious registration ambiguity in the previous global theorem has been removed: distinct channel frames are no longer supplied in one common Euclidean laboratory, the periodic deck labels are used explicitly, relative placements are posed as a gluing problem, and the cycle-holonomy argument gives a real mechanism for tying the channel network to the periodic lattice. The paper also analyzes two richer statistical records that v22 had deliberately left outside the endpoint-output experiment, and it gives a compactness/diagonal bridge from finite action jets to global analytic loss.

I do **not** find a new elementary algebraic contradiction in the determinant-one signed inverse, the analytic germ-globalization lemma, the cycle identity, or the one-channel negative-binomial LAN calculation. In particular, the v22 objection that the unregistered theorem was false or undefined under the weak reading is no longer my objection.

The reason for a negative top-four recommendation is now different. Once the earlier local defects have been repaired, the burden shifts to whether the new global and statistical architecture actually closes the strongest claims suggested by the title and introduction. In my view it does not yet do so at the requested venue level.

The main remaining issues are these.

1. The paper calls the new conclusion a **fully intrinsic periodic table rigidity theorem**, but the inverse problem still starts with a marked abstract **Euclidean** lattice whose Gram form and orientation are fixed, as well as the complete lifted deck labels `(a,b,ell)`. The theorem reconstructs the obstacle/channel placement relative to that known flat lattice; it does not recover the Euclidean lattice geometry itself from billiard data. This is a legitimate inverse problem, but its scope should either be stated more narrowly or strengthened.

2. The headline classification theorem identifies table realizations with an `admissible gluing space` whose definition already requires the reconstructed periodic translates to form a valid dispersing billiard table with the declared measured channels. That bijection is useful bookkeeping, but by itself it is close to a reformulation of the realization problem. The genuinely nontrivial global content lies in the sufficient singleton criterion: a signature-rigid anchoring cycle plus a signature-rigid spanning tree. The manuscript does not yet establish that such a network arises naturally, generically, minimally, or from a small intrinsic acquisition scheme. At top-four level, this distinction between classification formalism and rigidity mechanism matters.

3. The endpoint--time Poisson boundary experiment is potentially a strong result, but the proof of **Le Cam asymptotic equivalence** is currently too compressed for the strength of the statement. The point-process approximation itself is plausible. What is not yet written at publication-level detail is the uniform reverse deficiency: the common-bulk conditional law, the parameter-independent reconstruction kernel, the two-sided endpoint corner under support expansion, and the uniform total-variation/Hellinger control needed to replace the full successful sample by the Poisson layer plus a parameter-free factor.

4. The new analytic/global statistical bridge is mathematically correct as a compactness/diagonal principle, but it is **conditional on the main global statistical input one actually needs**: for every fixed order `M`, a uniformly consistent estimator of the full finite data vector `D_M(T)` over the compact analytic class. The local Poisson/LAN theorems and positive information matrices are reference-local and use local designs/anchored charts. They do not by themselves produce a globally implementable common acquisition atlas or uniform fixed-order estimator over an unknown table class. Thus the exact/global and physical/statistical chains are closer than in v22, but they are not yet fused into an unconditional physical global-reconstruction theorem.

5. The count--endpoint theorem is a serious improvement, but its displayed fast channel is one-dimensional because it is formulated for one anchored channel and one gradient `D gamma`. A multichannel physical experiment can carry several exponent gradients whose span has rank larger than one. If the paper wants the phrase `multiscale physical information` to describe the acquisition system rather than one local channel, the vector/rank version is the natural endpoint.

6. The canonical manuscript-source workflow still has no successful native build. The exact-source Actions run is completed with conclusion `failure`, and the repository record states that both attempts had `steps=null`, so no checkout/build/reference/numerical/hash step executed. This is an infrastructure failure rather than evidence of a TeX error, but submission readiness remains unverified.

My overall assessment is therefore:

> **V23 has crossed an important threshold: the manuscript now contains a genuine intrinsic channel-network mechanism, a non-Gaussian endpoint--time experiment, a count-sensitive multirate experiment, and an explicit growing-order compactness bridge. The earlier registration objection is substantially resolved. However, the strongest global theorem still fixes the Euclidean lattice metric and relies on a strong signature-rigid network; the Le Cam equivalence proof is not yet complete at the stated level; and the global statistical conclusion remains conditional on uniform fixed-order acquisition/estimation that the paper does not derive. These are no longer cosmetic defects. They are exactly the issues that determine whether the work is a very strong specialist contribution or a four-journal paper.**

I therefore recommend another strengthening revision rather than downscaling or deleting the all-order results.

## 2. Scope of this review

I reviewed the v23 source graph with particular attention to the material added after the v22 report:

- `papers/A2-v17-boundary-information-coarsening/main.tex`;
- `article/01_introduction_v23.tex`;
- `article/01b_observation_hierarchy_v23.tex`;
- `article/23c_analytic_continuation_v23.tex`;
- `article/23b_intrinsic_multichannel_rigidity_v23.tex`;
- `article/18c_full_endpoint_time_information_v23.tex`;
- `article/18d_count_endpoint_multirate_v23.tex`;
- `article/18e_compatible_rates_v23.tex`;
- `article/25_analytic_global_bridge_v23.tex`;
- the active inherited v22 modules on the all-order inverse, common-collar endpoint experiment, anchored realization, physical fixed-window reduction and stopped transfer;
- the v23 response letter, manifest and exact-head verification record.

I also compared the significance positioning against the rigidity literature already relevant to the manuscript: De Simoi--Kaloshin--Leguil on marked-length rigidity of analytic chaotic billiards, Osterman on length-spectrum rigidity for open dispersing billiards, and the recent Finamore--Leguil enriched marked-length approach for finite-horizon Sinai billiards. The observation architectures are different, and I do **not** identify an obvious duplication of the determinant-one signed-endpoint mechanism. My significance objection is therefore not a priority objection; it concerns how much global geometry the present data reconstruct rather than assume.

I have not machine-reproved every inherited lemma. I rechecked the new theorem interfaces and the earlier results at the points where v23 uses them to make stronger global/statistical claims.

## 3. What v23 genuinely fixes

### 3.1 The v22 registration ambiguity is substantially resolved

This is the most important improvement.

The intrinsic datum for a measured edge `e=(a,b,ell)` now contains the lifted label, onset, two signed endpoint-law germs and transverse sign convention, all in the channel-adapted frame. It does **not** supply the Euclidean placement of that frame relative to the lattice or to another channel.

After the all-order inverse and analytic continuation recover complete oriented copies of the two incident obstacle lifts in each edge frame, v23 introduces unknown edge placements `A_e` and an unknown oriented realization `iota` of the marked Euclidean lattice. Incidences carrying the same quotient obstacle label are glued only after translating their recovered lifts back by the relevant deck vectors.

This is the right geometric formulation. The disconnected-component counterexample behind the v22 objection is no longer available under the new connected network plus gluing/holonomy setup.

### 3.2 The analytic germ-globalization lemma is clean and credible

The standalone lemma is useful. Equality of a registered real-analytic boundary germ gives equality of curvature germs; analytic continuation on the arclength cover gives a common positive analytic curvature function; positivity plus total turning forces equality of the arclength periods; and Frenet uniqueness gives equality of the complete boundary images.

I do not see a defect in this argument under the stated connected, embedded, strictly convex, real-analytic hypotheses.

### 3.3 The cycle-holonomy mechanism is a genuine new global ingredient

The relation

`R_e0 v_c = iota(eta_c)`

for a signature-rigid closed channel cycle is conceptually useful. With a fixed Euclidean Gram form on the marked lattice, one nonzero deck vector indeed fixes the orientation-preserving lattice realization relative to the starting channel frame. A rooted signature-rigid spanning tree can then propagate obstacle placement.

This is substantially stronger than simply assuming every measured contact frame is already registered in one laboratory.

### 3.4 The observation hierarchy is now honest and mathematically useful

The manuscript explicitly distinguishes:

1. the full growing collision history;
2. the per-preparation endpoint--time record plus failure;
3. the stopped endpoint--time transcript;
4. the count--endpoint coarsening;
5. the endpoint-output coarsening.

It also states which finite-to-boundary comparison applies to which sigma-field. This removes an important source of ambiguity from earlier versions. The paper no longer presents the endpoint-only Gaussian theorem as an efficiency theorem for the full raw history.

### 3.5 The endpoint--time and count refinements are real mathematical additions

The positive-density moving ceiling produces a natural extreme-value/Poisson scale of order `k^{-1}` for shape and `(jk)^{-1}` for gap. After residual time is removed, the negative-binomial waiting count detects the hyperbolic exponent at a different scale, while the linearly vanishing endpoint density retains the slower moving-support Gaussian channel.

This three-level hierarchy is a coherent answer to the v22 criticism that the success/waiting channel had been left outside the physical information theorem.

### 3.6 The explicit compatible rate regime is useful

The example

`delta_n=n^{-1}`, `k_n=floor(n^2/log n)`, `j_n=2 ceil(C log n)`

with sufficiently large `C` verifies simultaneously that the several asymptotic requirements are not mutually empty. This should remain in the paper.

### 3.7 The exact/global versus finite-order distinction is now treated explicitly

The compactness theorem and the diagonal theorem do address a real conceptual gap from v22. They make clear that one does not need a uniform-in-order condition number merely to obtain **consistency** along an arbitrarily slowly growing order sequence, provided fixed-order data are uniformly consistently estimable.

That is mathematically correct and worth retaining. The remaining issue is the conditional nature of the statistical premise, discussed below.

## 4. Major blocker C23-M1: `fully intrinsic` currently means intrinsic **inside a fixed marked Euclidean lattice**

The global inverse problem begins with `Lambda_abs` as a marked abstract lattice **with its fixed Euclidean Gram form and orientation**. The measured edge label also includes its exact deck element `ell` in that lattice.

This is a reasonable model if the flat torus/lattice is part of the known ambient apparatus and only the obstacles are unknown. But then the strongest correct description is something like:

> intrinsic obstacle/channel reconstruction in a fixed marked Euclidean periodic lattice.

The current phrase `complete labelled periodic table is intrinsically determined` can be read more strongly: as though the periodic geometry itself were recovered from the channel laws. It is not. The metric shape and scale of the lattice are supplied through the Gram form. The anchoring cycle determines only its orientation relative to the channel frame because the Euclidean lattice has already been fixed up to an orientation-preserving isometry.

This is not a logical error in Theorem `thm:v23-intrinsic-table-rigidity`. It is a scope/significance issue, but at the requested venue level it is substantial.

There are two clean responses.

### Route A: narrow the theorem language

State everywhere that the ambient marked Euclidean lattice, including its Gram form, is fixed. Replace `fully intrinsic periodic table rigidity` by a formulation that makes the fixed torus metric explicit. Then calibrate the significance claim accordingly.

### Route B: strengthen the theorem and recover the lattice metric

A materially stronger theorem would begin with a marked rank-two deck group but **without** a prescribed Euclidean Gram form. Two linearly independent signature-rigid cycles would yield two data-determined holonomy vectors. Their deck classes could then determine the full oriented lattice realization, including its Gram matrix, provided the corresponding deck vectors are linearly independent. One would then genuinely reconstruct the periodic Euclidean geometry together with the obstacles up to global Euclidean motion.

This extension is mathematically natural in the present framework and, in my view, would materially improve the top-four case.

## 5. Major blocker C23-M2: the classification theorem is partly definitional; the real rigidity theorem needs a stronger naturality/genericity statement

The manuscript defines an algebraic periodic gluing and then calls it `admissible` only if the resulting periodic translates are already a genuine dispersing billiard table with the prescribed measured channels. The theorem that table realizations modulo global `SE(2)` are in bijection with the admissible gluing space is therefore correct, but much of the statement is a precise parameterization of realizations rather than a rigidity theorem in the usual sense.

The serious global content begins only when the paper proves that the gluing space is a singleton under a lattice-anchoring cycle and a rooted signature-rigid spanning tree.

That singleton criterion is plausible and useful, but its hypotheses are strong:

- every transition used in the cycle/tree must be signature-rigid;
- repeated complete curvature signatures caused by obstacle symmetries create ambiguity;
- the measured network must already contain the appropriate closed deck-nontrivial cycle;
- the spanning tree must meet unique framed signatures in an order that propagates all obstacle orbits.

The paper treats circles and cyclic symmetries honestly as true ambiguities. What is missing is a theorem explaining how restrictive the required network is in the natural class of tables.

For a top-four presentation I would want at least one of the following.

1. **Genericity:** prove that for a residual/open-dense/full-measure class of analytic periodic dispersing tables, a specified finite family of lifted channels contains a signature-rigid anchoring structure.
2. **Finite acquisition theorem:** give an a priori bound, preferably depending only on the number of obstacle orbits and simple symmetry data, on how many channels are sufficient to force singleton gluing.
3. **Intrinsic selection:** show how the necessary cycle/tree can be selected from observable channel data rather than imposed as a favorable design.
4. **Symmetry-resolved theorem:** classify exactly the residual finite/continuous ambiguity when signature-rigidity fails and prove that the quotient ambiguity is the only obstruction.

Without such a result, the global theorem is stronger than v22 but still conditional on a carefully engineered channel network. That may be excellent specialist mathematics; it is not yet, by itself, the global conceptual leap suggested by the title.

## 6. Major blocker C23-M3: the endpoint--time Poisson theorem needs a full deficiency proof, not only a point-process heuristic plus likelihood bookkeeping

I find the central scaling convincing. With conditional density

`q_0(u,v,r)=rho(u,v) 1_{0<r<w(u,v)}`

and a ceiling displacement of order `k^{-1}`, a boundary layer of thickness `k^{-1}` contains order-one points, so a Poisson boundary-shift limit is natural. The codimension-two intersection with `r=0` has one-record mass of order `k^{-2}` and is negligible over `k` records. The binomial-to-Poisson estimate for the retained layer is also the right tool.

However, Theorem `thm:v23-et-poisson` asserts **asymptotic equivalence in Le Cam distance**, uniformly on compact local parameter sets. This is stronger than convergence of the extracted point process or convergence of likelihood ratios.

The present proof compresses the reverse direction into the sentence that one may generate the asymptotically parameter-free bulk from the reference conditional law and attach it to the Poissonized boundary layer. For publication at the requested level, several points need to be written explicitly.

### 6.1 The reverse Markov kernel must be parameter-independent

The deficiency from the limiting Poisson experiment back to the finite sample requires a kernel that cannot depend on the unknown local parameter `z`. The proof should define that kernel, including how many bulk observations are generated after the random boundary-layer count is realized and how design labels are handled.

### 6.2 The bulk conditional laws need a quantitative product bound

The statement that the centered bulk log-likelihood has variance `O(k^{-1})` strongly suggests parameter-freeness, but it is not itself a uniform total-variation bound for the conditional bulk experiment. A clean proof should give a one-record Hellinger/chi-square/TV estimate on the common bulk and then tensorize it, uniformly for `z` in a compact set.

### 6.3 The support-expansion side of the endpoint corner should be made explicit

The displayed coarea estimate treats `0<w<=2R/k`. Under a ceiling expansion, there can also be endpoint coordinates just outside the null endpoint domain, `w<0` but `w_z>0`. That region should be included in a two-sided collar argument. It is very likely negligible for exactly the same codimension-two reason, but the theorem should prove it rather than leave the support-extension case implicit.

### 6.4 The projective `R_K` formulation should be made into a precise experiment

For each compact parameter set the theorem chooses `R_K`. If the final limit experiment is meant to live on the whole boundary half-space, define the projective family and the comparison kernels coherently, or state the local equivalence for each finite window and then prove the passage to the increasing-window experiment.

### 6.5 Capping and stopped transfer should be composed at the experiment level

The later theorem uses cap negligibility and the stopped finite-to-boundary comparison. The final version should display the triangle inequality in Le Cam/TV distance across: uncapped boundary stopped experiment -> capped boundary experiment -> Poisson experiment -> finite-bridge stopped experiment. This will make the claimed `complete stopped endpoint--time local experiment` genuinely audit-ready.

I emphasize that I regard this as a **proof-completeness blocker, not a counterexample to the Poisson limit**. The idea looks correct. The present proof is simply shorter than the theorem it claims.

## 7. Major blocker C23-M4: the global statistical bridge assumes the missing global fixed-order estimator

Theorem `thm:v23-finite-coordinate-resolution` is a compactness consequence of injectivity of the infinite action-jet data. Theorem `thm:v23-diagonal-global-reconstruction` is then a standard but useful diagonal/sieve principle.

The crucial premise is

`sup_T P_{n,T}( ||Dhat_{n,M}-D_M(T)|| > eta ) -> 0`

for **every fixed `M`**, uniformly over the compact analytic class.

This is precisely the point at which the paper has not yet connected the local physical experiments to the global table problem.

The physical theorems establish local experiments around a reference table in anchored coordinates. The finite positive design may depend on the reference geometry and on `M`; the caps and physical windows are constructed from reference quantities; the local chart itself assumes an anchored realization. None of the current theorems proves that an experimenter who does not know `T` can choose one common finite acquisition protocol over `K` and uniformly estimate every `D_M(T)`.

The corollary acknowledges this by saying `whenever` the compact class admits such a common finite acquisition atlas. This makes the logic correct, but it means the v22 exact/statistical gap has not been fully closed; it has been converted into an explicit assumption.

At top-four level I would require the missing theorem, for example through one of these routes.

### Route A: common deterministic atlas

Construct finitely many physical windows/channel designs, independent of the unknown `T` in `K`, whose fixed-order information is uniformly nondegenerate and whose finite-to-boundary transfer constants are uniform on `K`. Then prove a global minimum-distance or testing estimator for `D_M`.

### Route B: adaptive two-stage acquisition

Use a coarse pilot experiment to localize the table/channel geometry uniformly over `K`, then choose the local positive design/caps in a second stage. Prove that the pilot cost is negligible at the final scales and that design selection is stable uniformly over the class.

### Route C: finite covering plus robust tests

Exploit compactness to build a finite cover of local charts and uniformly consistent tests between separated `D_M` values, then derive a global estimator. This would still need a physically implementable protocol whose observation space is common across the cover.

Once this fixed-order global theorem is in place, the diagonal argument in Section 25 becomes a legitimate bridge from the actual finite-bridge experiment to global analytic table loss. Without it, the abstract should not suggest that the paper itself has proved global physical table reconstruction unconditionally.

## 8. Major blocker C23-M5: the count--endpoint theorem is one-channel/rank-one, whereas the physical architecture is multichannel

Section 18d fixes **one anchored labelled channel** and decomposes the shape tangent space using the single covector

`lambda = D_vartheta gamma`.

The resulting count experiment has one fast Gaussian coordinate `b`. This is internally coherent. But the paper elsewhere uses a finite positive design across several channels/preparations, and the global inverse uses a measured channel network.

For several channels `e`, the success probabilities contain different exponents `gamma_e(T)`. Their gradients `D gamma_e` can span a subspace of dimension larger than one. The waiting counts should then yield a vector Gaussian shift on the span of these exponent gradients, with an information matrix assembled from the design proportions. The endpoint component should live on the complementary slow tangent directions, with possible overlaps handled by the joint multirate parameterization.

A natural complete theorem would therefore identify:

- the fast tangent subspace `span{D gamma_e}` visible through counts;
- its count information matrix and rank;
- the slow tangent subspace invisible to first-order count scores;
- the endpoint boundary information restricted to that slow subspace;
- and the joint product/cross-information structure under a common acquisition design.

This would make `multiscale physical information` a theorem about the actual finite design/network rather than a one-channel prototype. If the author chooses not to pursue this extension, the introduction should clearly label Section 18d as a single-channel local model rather than the complete multichannel count information theorem.

## 9. Major blocker C23-M6: exact-head native build remains uncertified

The canonical manuscript-source commit is `8840bf01ee8a7752504d2913bf00af54656afbb5`. Workflow run `34602335326` is completed with conclusion `failure`. The repository verification record states that both the first attempt and explicit rerun returned `steps=null`, so no checkout, TeX build, numerical diagnostic, unresolved-reference check, hash step or artifact upload executed.

I agree with the author's interpretation: this is **not evidence of a TeX failure**. It is nevertheless not a successful build certificate.

Before another serious submission round, the exact manuscript source should have:

- a successful clean native LaTeX build;
- no unresolved references/citations or fatal diagnostics;
- reproducible numerical diagnostic output where claimed;
- a PDF/source hash tied to the reviewed commit;
- and an archived build artifact.

This is a submission-readiness requirement, not a mathematical objection.

## 10. Secondary mathematical and expository comments

### 10.1 Separate `classification` from `rigidity` in the headline theorem hierarchy

The bijection with `G_per(D)` and the singleton criterion do different jobs. The first identifies the realization space; the second proves uniqueness under extra geometry. The abstract and introduction should make that distinction as sharply as the body does.

### 10.2 State exactly what is known about the lattice in the abstract

The phrase `marked abstract Euclidean lattice` is mathematically precise in the body but easy to miss in the abstract. If the Gram form remains input, say so at the first global-rigidity claim.

### 10.3 Quantify or characterize signature-rigidity

A reader needs to know whether repeated complete curvature signatures are exceptional, how they relate to the full orientation-preserving symmetry group, and whether a generic analytic obstacle has trivial `Sym^+(C)`. A short genericity proposition would strengthen the tree/cycle theorem substantially.

### 10.4 Clarify the role of channel labels as data versus design

The lifted labels `(a,b,ell)` contain nontrivial global/topological information. The paper should distinguish clearly between labels known because the experimenter selected the channel and labels inferred from the observed trajectory. The current theorem takes them as part of the intrinsic datum/design.

### 10.5 The endpoint--time density normalization under alternatives should be written explicitly

The proof uses smooth changes of the ceiling and amplitude. Write the alternative density and its normalizing relation before the Poisson theorem so the deterministic compensator calculation can be checked directly.

### 10.6 Give a lemma for the common-bulk product distance

A short self-contained Hellinger lemma would make the reverse deficiency argument much cleaner than prose about centered likelihood variance.

### 10.7 The non-dominated Poisson limit deserves a precise comparison statement

Because alternatives can create points where the null intensity is zero, avoid any hidden use of a reference likelihood in the final formulation. Pairwise likelihoods on common parts and direct Poisson process distances are safer.

### 10.8 The assertion `D_vartheta gamma != 0` should cite the exact derivative formula

The text says this follows because the finite jet coordinate contains the two contact curvatures and `gamma` depends nontrivially on them. This is plausible from the earlier explicit quadratic formulas, but a direct citation or one-line derivative calculation would remove ambiguity.

### 10.9 For the multichannel count extension, allow rank deficiency

Even with several channels the exponent-gradient matrix need not have full rank. The natural statement should use its range and Moore--Penrose inverse, in the same spirit as the endpoint information theorem's identifiable-subspace formulation.

### 10.10 The compact analytic class should have one explicit model

The text says a uniformly bounded holomorphic extension to a fixed complex collar is sufficient. It would help to define one concrete Banach/compact class and verify continuity/compactness of the finite action maps there, so the global bridge does not look purely axiomatic.

### 10.11 The finite-data norms should be compatible under truncation

The compactness proof implicitly uses that closeness of `D_m` controls all lower truncations. State that the norms are chosen compatibly, e.g. the Euclidean norm on a nested coordinate vector or an equivalent monotone family.

### 10.12 Distinguish consistency from quantitative stability

Section 25 proves qualitative finite-coordinate resolution and global consistency. It does not give a modulus of continuity, a global rate, an optimal `M_n`, or a sample-cost/risk theorem. The manuscript generally admits this; the abstract should preserve that restraint.

### 10.13 Keep the v22 fixed-order conditioning disclaimer

The all-order determinant-one blocks do not imply uniform conditioning of the full triangular inverse as `M -> infinity`. V23 correctly avoids this inference. Do not weaken that disclaimer in future versions.

### 10.14 Keep the observation hierarchy exactly as explicit as it is now

The distinction among full collision history, endpoint--time transcript, count--endpoint transcript and endpoint-only experiment is one of the strongest expository improvements in v23.

### 10.15 The manuscript is still very large

The theorem-first introduction is much better than the revision-era narrative it replaces. Nevertheless, the paper still contains a large number of inherited modules and auxiliary applications. For a four-journal submission, every section should be visibly subordinate to one of the headline theorem chains. This is an editorial issue only after the mathematical blockers above are resolved.

## 11. What I would require before another top-four assessment

I would not ask the author to weaken the determinant-one inverse or delete the new multiscale results. I would ask for the following stronger program.

### R23-1. Decide whether the lattice geometry is fixed or reconstructed

Either narrow the global theorem language to a fixed marked Euclidean lattice, or strengthen the intrinsic result so that two independent holonomy cycles recover an initially unknown lattice Gram/realization.

### R23-2. Turn the signature-rigid network criterion into a natural rigidity theorem

Prove genericity, finite channel sufficiency, an intrinsic channel-selection theorem, or a sharp symmetry-obstruction classification. The goal is to make singleton gluing a theorem for a meaningful class rather than an assumption engineered into the measured graph.

### R23-3. Complete the endpoint--time Le Cam proof

Give explicit forward and reverse parameter-independent kernels, a quantitative common-bulk product bound, a two-sided corner estimate, and a clean composition with capping/stopped transfer.

### R23-4. Prove uniform fixed-order physical estimability over the compact analytic class

This is the missing step needed to turn Section 25 from a conditional bridge into an actual global physical reconstruction theorem. A common atlas or adaptive pilot theorem would suffice.

### R23-5. Upgrade the waiting-count theorem to the multichannel rank formulation, or narrow its positioning

The natural fast information object is the span/information matrix generated by all channel exponent gradients, not a single scalar direction.

### R23-6. Produce a successful exact-head native build

Do not call the paper submission-ready until the configured build and diagnostics have actually executed and passed.

### R23-7. Preserve the genuine v22/v23 repairs

Do not regress on:

- the weighted all-order half-line inverse;
- finite-truncation envelope cancellation and homogeneous action filtration;
- determinant-one signed blocks;
- even-flight same-type convention;
- reference-based cap quantifiers;
- fixed laboratory coordinates for local experiments;
- the non-dominated/common-collar distinction;
- parameter-independent comparison kernels;
- identifiable-subspace treatment of singular endpoint information;
- the explicit record sigma-field hierarchy;
- the intrinsic channel-frame formulation;
- the analytic germ-globalization lemma;
- and the explicit admission that the full growing collision array is not covered by the present transfer theorem.

## 12. Bottom-line assessment of the headline claims

My present judgments are:

- **Relative boundary law and inherited nonlinear asymptotics:** no new v23 objection identified at the interfaces checked in this round.
- **All-order signed endpoint rigidity / determinant-one new-jet blocks:** remains the strongest and most distinctive theorem in the paper; I regard the v22 proof architecture as substantially credible and see no v23 regression.
- **Analytic germ globalization:** credible under the stated strict-convexity/analyticity assumptions.
- **Intrinsic gluing formulation:** a genuine improvement; the v22 registration ambiguity is substantially resolved.
- **Admissible gluing classification:** correct as a realization-space formulation, but partly definitional and not by itself a top-four rigidity result.
- **Anchoring-cycle + signature-rigid spanning-tree uniqueness:** plausible and nontrivial under its hypotheses; presently too conditional on a favorable measured network to settle the significance question.
- **Endpoint--time Poisson boundary experiment:** strong and plausible in scaling/limit form, but the proof of full Le Cam equivalence is not yet complete enough for publication at the claimed level.
- **Complete stopped endpoint--time transfer:** credible conditional on completion of the Poisson-equivalence proof and the inherited stopped coupling.
- **Count--endpoint two-speed Gaussian experiment:** internally coherent as a one-channel/rank-one local theorem; a multichannel rank formulation is still missing.
- **Endpoint-output Gaussian experiment:** the v22 common-collar/non-dominated architecture remains coherent and is correctly presented as a coarsening.
- **Uniform finite-coordinate resolution:** mathematically correct compactness consequence of injectivity on the assumed compact class.
- **Diagonal growing-order reconstruction:** mathematically correct conditional sieve principle; it does not itself prove uniform fixed-order estimability from the physical acquisition model.
- **Global physical table reconstruction:** **not yet established unconditionally** by the current manuscript.
- **Submission readiness:** not yet achieved because the exact-source native build has not executed successfully.

## 13. Final recommendation

**Reject in the present form at Annals/Acta/Inventiones/JAMS standard, with encouragement to submit a substantially strengthened version for a fresh assessment.**

This is a materially more favorable mathematical assessment than the v22 rejection. V23 solves the most obvious global-registration defect and adds serious new asymptotic-statistical content. I would no longer characterize the paper as a collection of local results searching for a global theorem. There is now a recognizable global mechanism.

The remaining question is whether that mechanism is strong and complete enough for the requested venues. In the present version, the periodic Euclidean lattice metric is still supplied; singleton gluing relies on a strong signature-rigid acquisition network without a genericity/sufficiency theorem; the richest new Poisson experiment is not yet proved in full Le Cam detail; and the global statistical bridge assumes rather than derives the uniform fixed-order acquisition theorem needed to connect physical data to a global analytic table.

Those are precisely the next problems to solve. If the author can (i) recover or explicitly delimit the lattice geometry, (ii) make the anchoring network natural/generic, and (iii) close the uniform physical-to-global statistical chain with a complete Poisson deficiency proof, the venue assessment could change materially. The current revision is strong enough to justify that next round, but not yet strong enough for acceptance at the requested top-four level.