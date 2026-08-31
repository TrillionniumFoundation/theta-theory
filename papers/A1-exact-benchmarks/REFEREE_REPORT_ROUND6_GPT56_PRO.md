# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A1 — *Deterministic Path Ensembles, Driven Collision Maps, and Endogenous Conjugate Parameters*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `2710b04cf5dc878fef6d584f1e86933551dcb905`

## Editorial summary

Round six is a genuine materialized revision. The controlling module is loaded by the manuscript and the source builds. The new full-port work layer also repairs the previous core-cutoff defect: on the declared disjoint incoming components the integral of the work form is indeed `epsilon_i` for every regular point.

Those improvements do not close the paper. The main return map is not a bijection on the graph completion actually defined, and the physical response theorem invokes a spectral gap on an inappropriate isotropic piecewise-Hölder space. These are theorem-level failures, not requests for exposition.

## Major mathematical objections

### 1. Lemma `lem:r6-a1-section` is false on the stated graph completion

The section is

\[
\widehat\Sigma_a=\bigsqcup_i\overline{I_i(a)}^{\,g}\times[0,1].
\]

Only endpoints of the first coordinate are given oriented copies. The horizontal seams

\[
p=s_i(a),\qquad i=1,2,3,
\]

in the second coordinate are not graph-completed and do not carry the previous-port label.

This destroys injectivity. Fix a regular `Q` lying in the interior of one next-port interval `I_j(a)`. The two boundary points

\[
x=(i,s_{i-1}+p_iQ,1),
\qquad
\widetilde x=(i+1,s_i+p_{i+1}Q,0)
\]

are distinct points of the disjoint-union source, but the displayed formula gives

\[
F_a(x)=F_a(\widetilde x)=(j,Q,s_i).
\]

The target contains neither an oriented copy of the horizontal seam nor a retained old label, so these images are identical. The sentence that “oriented endpoint copies make both label assignments single valued at every seam” is therefore incorrect: the construction duplicates vertical-port endpoints only.

Consequently the claimed inverse, the mapping-torus gluing, and the first-return theorem are not defined on the full corner strata stated in the paper. The repair is straightforward in concept—complete both seam families or retain both current and previous labels—but it must be carried through in the section, symplectic atlas, and suspension.

### 2. The physical transfer operator has no proved spectral gap on `mathscr B_a^{m,r,eta}`

The map is an invertible, area-preserving baker-type transformation: it expands the first coordinate and contracts the second. The paper places its physical transfer operator on a finite direct sum of ordinary `C^{k,eta}` cell functions and trace jets, then states that “the spectral gap on the finite-branch expanding factor” supplies

\[
S_a=(I-\mathcal L_a)^{-1}Q_a.
\]

A spectral gap of the one-sided symbolic factor does not imply a spectral gap for the invertible two-dimensional physical Perron or Koopman operator on isotropic Hölder spaces. Stable-direction oscillations are not contracted in that norm, and an invertible measure-preserving operator generally carries substantial unit-circle spectrum. Trace coordinates do not cure this defect.

Thus the reduced resolvent used in `lem:r6-a1-shape` is not established, the geometric time sums in `thm:r6-a1-response` need not converge, and the claimed all-order physical response does not follow. A valid proof would require a declared anisotropic Banach scale adapted to the baker map, a Lasota–Yorke inequality, compact embedding, peripheral-spectrum analysis, and parameter/trace estimates on that scale.

### 3. The all-order trace-jet calculus is asserted beyond the regularity supplied

The paper states that each parameter derivative creates at most one higher trace jet and that retaining jets through order `m` closes arbitrary order response. This omits several effects:

- derivatives of moving cell intersections create corner distributions, not only face traces;
- repeated differentiation changes incidence maps and pullback Jacobians, producing mixed tangential/normal derivatives;
- compatibility of traces at multiply incident corners must be preserved by the triangular transfer action; and
- the parameter-dependent projectors and reduced resolvents lose regularity between strong and weak spaces.

No norm estimate is given for these corner terms or for the iterated resolvent words. Even after replacing the physical space by an anisotropic one, the stated finite direct sum is not yet an all-order shape-calculus theorem.

### 4. The autonomous impact-network realization remains a sketch

The mapping torus with Hamiltonian `H=E` is an abstract suspension once a genuine symplectic return map is available. The additional claim of a smooth autonomous impact network is stronger. The proof invokes compactly supported branch Hamiltonians, a relative extension, a recutting hub, and “standard autonomization,” but gives no global Hamiltonian, no compatible corner atlas, and no verification that the time-dependent branch isotopies glue while preserving exact return time and section flux.

In particular, autonomizing a time-dependent Hamiltonian normally replaces `E` by `E+K_tau`; it is not automatic that the resulting energy surface and section have the exact properties asserted. This part should either be constructed explicitly or removed.

### 5. The work proposition is an improvement but is tied to an unconstructed layered cobordism

On four genuinely disjoint incoming cylinders, the constant port coefficient is smooth and the integral is exactly `epsilon_i`. I accept that local computation. However the manuscript defines the mapping torus first and later replaces one flight by three layers in a separate “port cobordism.” The identification between this layered model and the mapping torus is only the unproved network conjugacy of objection 4. Therefore the work theorem cannot presently be transported to the advertised autonomous system.

### 6. The calibration statement is conditional and the remaining benchmark is below the top-four threshold

The revised theorem correctly says that `vartheta=theta` follows only after imposing equality of two normalized likelihood cocycles in common units. This is a compatibility axiom, not endogenous preference selection by mechanics. Once correctly scoped, the remaining ingredients are an explicit baker/Bernoulli benchmark, multinomial conditioning, transfer response, and a standard CARA classification. Even a corrected version would require a substantially stronger conceptual theorem to meet the editorial threshold of the four named journals.

## Required reconstruction

A mathematically viable revision must:

1. graph-complete both vertical and horizontal seam data, or retain enough labels to make `F_a` genuinely bijective;
2. rebuild the mapping torus and impact realization from that corrected map;
3. place the physical transfer operator on an anisotropic space and prove its spectral gap and parameter dependence;
4. include corner currents and mixed jets in a rigorous finite-order shape calculus; and
5. keep the valuation identification explicitly conditional.

## Recommendation

**Reject.** Round six fixes the former port-core work defect and is materially cleaner, but its foundational return-map lemma has an explicit boundary counterexample and its physical response theorem uses a nonexistent isotropic Hölder spectral gap. The main results are therefore not proved, and the corrected benchmark would still fall short of top-four novelty.