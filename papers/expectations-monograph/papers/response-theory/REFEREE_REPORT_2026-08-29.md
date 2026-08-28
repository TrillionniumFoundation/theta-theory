# Referee Report

**Manuscript:** *Conormal Source Modules, Recovery, and Obstructions for Finite-Horizon Dispersing Billiards with Moving Singularities*  
**Source reviewed:** `main.tex` and the associated theorem inventory / risk register / proof audit  
**Repository state reviewed:** `main` at commit `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`  
**Standard applied:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Recommendation:** **Reject**

## 1. Summary

The paper develops a large formalism for derivatives of transfer operators when billiard singularity sets move. It introduces decorated conormal source modules, one-face currents, point/jet atoms, label-resolved quotients, strong-recovery criteria, scalar assembly resets, and several obstruction results.

The unconditional positive content is much narrower than the title suggests:

- smoothness of static collision averages obtained from the explicit collision-flux measure;
- first- and second-order recovery for the complete invariant source of one radial-inflation family;
- fixed-length, post-assembly scalar reset estimates for those radial blocks;
- exact-coboundary and exact-current benchmark classes;
- split-surjectivity and periodic-orbit obstructions showing that generic independently prescribed sources fail the required gluing identities.

The general finite-order moving-singularity susceptibility theorem is conditional on the response-scale and triangular recovery certificates (S1)–(S3). The manuscript expressly states that those certificates are not proved by the preceding construction and are not used in the radial theorem. Continuous-time moving-family response is not proved.

This is a serious and intellectually honest diagnosis of the problem. It is not, however, the general response theorem advertised by the title and by the downstream papers.

## 2. Main reasons for rejection

### 2.1 The hard theorem is assumed as (S1)–(S3)

The general finite-order results assume a “collision response-scale and triangular recovery certificate.” These assumptions require precisely the properties that make moving-singularity response difficult:

- transfer invariance on the higher response scale;
- controlled conormal insertions across all branches and refinements;
- recovery of every assembled derivative tree to a strong primitive;
- uniform bounds sufficient to sum the infinite observable-side words.

The manuscript itself says that these certificates are not inferred from the fixed-atlas calculation and are not proved for the nonconjugate general family. Consequently, the theorem “finite-order moving-singularity response” is an implication theorem of the form

\[
\text{assume the complete response/recovery mechanism}
\quad\Longrightarrow\quad
\text{the response formula is valid}.
\]

That implication may be useful bookkeeping, but it does not solve the mathematical problem.

### 2.2 The unconditional theorem is a source-specific order-two identity

For radial inflation, the complete invariant source is shown to recover through order two after all insertion positions and density-jet terms are assembled. This is not an eventwise derivative theorem and not an all-seed response theorem.

The key identity is ultimately obtained by differentiating invariance and identifying the assembled current with
\[
(I-\mathscr L_0)\rho_j
\quad\text{or}\quad
(I-\mathscr L_0^N)\rho_j.
\]
This does prove cancellation for that complete invariant assembly if every differentiation and realization step is justified. But it does not provide a reusable response theory for a prescribed observable/correlation source. The paper's own gluing theorem says that such a prescribed source generically fails an infinite-codimension family of conditions.

The gap between “the invariant density differentiates because its explicit flux density differentiates” and “correlations admit moving-singularity linear response” is the central issue. The paper does not bridge it.

### 2.3 Static average differentiability is not dynamical linear response

For a billiard collision map, the invariant collision measure is explicit. Smoothness of
\[
\int f_s\,d\nu_s
\]
under a smooth transport of the collision section can therefore be proved directly by differentiating the flux density. The manuscript repeatedly uses the transfer formula as a consistency representation of this already known derivative.

This is not evidence that singular susceptibility series converge for nontrivial dynamical observables. The main theorem should not place direct static differentiation and moving-singularity dynamical response on the same rhetorical level.

### 2.4 Exact-current and exact-coboundary classes are tautological benchmarks

If
\[
g_s=(I-\mathscr L_s)h_s,
\]
then the susceptibility telescopes. Differentiating this identity also forces the represented conormal terms to cancel in the complete assembly. This is a valid consistency check, but it is true by construction.

Likewise, a rigid translation treated in the exact conjugacy trivialization has vanishing operator variation in that trivialization. It is not a nonconjugate moving-face example.

These examples should be labelled as tests of the formalism, not as positive evidence for the missing theorem.

### 2.5 The assembly reset is scalar, not a closed dynamical source theory

The paper correctly emphasizes that raw historical terminal labels can grow linearly and that the post-assembly reset is not equality in the label-resolved module. This admission exposes a limitation:

- the reset is certified only after pairing complete truncations with future tests;
- it discards the label information needed inside a later singular event;
- it is not a bounded projection on the full source module;
- it does not prove that a reset source can be reinserted into another moving singularity without a new certificate.

Thus the reset can justify selected scalar telescoping calculations, but it cannot support the downstream claim of a general differentiated resolvent calculus unless (S3) is separately verified.

### 2.6 The higher-order radial obstruction defeats the advertised finite-order scope

The paper computes that the isolated second radial letter has
\[
\partial_s^2\alpha\asymp u^{-6},
\]
leaving a nonintegrable \(u^{-3}\) flux coefficient. It also identifies a fourth-order endpoint atom. These are valuable warnings. They mean that a general finite-order radial response theorem is not available.

The manuscript therefore contains a contradiction of emphasis: a long abstract finite-order calculus is presented as the central framework, while the actual nonconjugate example stops at order two and the paper proves structural reasons that naive extension fails.

### 2.7 No moving-family continuous-time theorem is proved

The continuous-time section retains the fixed-table Baladi–Demers–Liverani input and then lists obstructions:

- transverse generator derivatives;
- a \(u^{-2}\) grazing multiplier;
- noncomparability of the collision weights at successive impacts;
- absence of a moving-family graph domain and symbol estimate.

This is not a suspension response theorem. Downstream papers cannot import it as one.

The distinction is especially important because the HJB paper relies on continuous-time reduced resolvents, moving trace insertions, and uniform response words. Those are not unconditional outputs of the present manuscript.

### 2.8 The new Banach modules are not yet shown to be canonical enough for the claimed use

The label-resolved quotient and weighted primitive domains are elaborate. For a top-tier functional-analytic theorem, the paper must prove, not merely design:

- independence or controlled equivalence under admissible atlases and refinements;
- completeness and closability of every realization/trace map;
- compatibility of physical regrouping with transfer;
- coordinate invariance of the conormal coefficients;
- a bounded operator theorem for the full countable branch family;
- uniform constants under the actual moving family.

The paper explicitly withdraws several of these claims for the fixed-atlas block-flux seminorm. That is appropriate, but it leaves the construction as a source-specific bookkeeping device rather than a canonical response space.

### 2.9 The obstruction results are more convincing than the positive theorem, but they are not organized as the paper's main contribution

The split-surjectivity of the moving-face defect, the infinite-codimension kernel, the periodic-orbit Ward conditions, and the failure of eventwise all-seed recovery may form the basis of an interesting negative paper. At present they are embedded in a very long manuscript whose title promises a positive response framework.

A top journal paper should have one theorem-level spine. Here the most credible spine is:

> generic prescribed sources fail; only complete source-specific assemblies can recover.

If that is the intended main theorem, the paper should be rewritten around a precise no-go statement, with the radial example as a sharp exceptional class.

## 3. Position relative to the literature

Demers–Zhang established spectral stability for broad Lorentz-gas perturbations, including moving and deforming scatterers. That result does not give differentiability when discontinuity boundaries move.

Stenlund–Young–Zhang established uniform loss of memory for sequential moving-scatterer billiards. That does not supply the two-time trace-current estimates needed for susceptibility differentiation.

Baladi–Demers–Liverani established exponential mixing and a spectral theory for a fixed finite-horizon Sinai billiard flow. It is not a parameter-uniform moving-flow response theorem.

Recent work on conditional mixing and discontinuous perturbations makes clear that the missing convergence of singular profiles is itself a serious theorem. Canestrari's small-hole result is a model-specific positive theorem with a different source geometry. The manuscript correctly notes these distinctions, but then has no comparable positive theorem for a genuinely moving scatterer beyond the radial invariant assembly.

## 4. Specific issues that must not be exported downstream

The following are not unconditional theorem outputs of this paper:

1. a general \(C^J\) moving-singularity response theorem for prescribed sources;
2. eventwise reinsertion of recovered currents;
3. all-seed (S1) or (S3);
4. a moving-family continuous-time graph domain;
5. a parameter-uniform suspension symbol theorem;
6. a general finite regularity-loss budget for the HJB coefficient hierarchy;
7. convergence of raw historical terminal states.

Any companion paper that treats these as established inputs is mathematically unsupported.

## 5. Presentation

The abstract is far too long and reads as an internal risk register. The manuscript repeatedly states what it does not prove; this is commendably honest, but it also demonstrates that the paper has not converged to a publishable theorem.

The reader must navigate:

- several strong/weak/positive spaces;
- multiple quotient realizations;
- conditional and unconditional theorem lines;
- exact-current examples;
- no-go appendices;
- radial blocks;
- continuous-time obstructions;
- theorem inventories and risk registers outside the article.

A top-journal submission cannot require the referee to reconstruct the actual claim from side documents.

## 6. A viable revision strategy

The current paper should not be revised incrementally. It should be split.

### Paper A: a no-go theorem

Prove cleanly that, for a genuinely moving physical face, the Poisson gluing defect is split surjective on a natural, coordinate-invariant source/observable domain, and derive the infinite-codimension and periodic-orbit obstructions. This could be significant if the function spaces and geometric hypotheses are canonical.

### Paper B: one actual positive theorem

Choose one nonconjugate deformation and prove a complete response result that is not an exact coboundary and not merely a static invariant-density identity. The theorem should include:

- a specified observable/source class;
- convergence of the susceptibility;
- parameter differentiability;
- all singular trace cancellations;
- a reusable reinsertion or block-reset theorem;
- a continuous-time statement if it is to be used for homogenization.

Until such a theorem is proved, the general S1–S3 calculus should be presented as a conjectural program, not as the principal response package.

## 7. Recommendation

The manuscript contains serious ideas and useful negative diagnostics, but the central positive theorem is conditional and the actual example is too narrow for the advertised scope. The work is not suitable for a top-four general mathematics journal in its current form.

**Recommendation: reject.**
