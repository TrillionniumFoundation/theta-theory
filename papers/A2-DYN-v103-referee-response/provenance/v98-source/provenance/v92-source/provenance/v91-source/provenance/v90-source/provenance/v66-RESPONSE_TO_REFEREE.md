# Response to the revision-65 external referee report

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revision:** 66, 10 October 2026  
**Reviewed author source:** `04f38424177533db60dfd13c3052381dc0adb481`  
**Complete reviewed paper tree:** `897816d34b3d012fb93feaf532dcf64740723d83`  
**Controlling report:** `reviews/a2-dyn-v65-external-top4-review-2026-10-10/REFEREE_REPORT.md`, commit `8f5b4dd2b2b12b7454b3ebdfa0e41546ba7f6908`, blob `2b2f7798f7c6eefa23c9c0a27368fd53df907442`.

We thank the referee for distinguishing the valid local geometry from the unproved ordered pointwise conclusion. We retain the original Lorentz record, arithmetic modulation, positive source decomposition and pointwise target. We do not replace the problem by a model system, an averaged return index, a growing Fourier band, or a smaller journal claim.

The principal change is a count-uniform coordinate and source theorem, not another finite-word affine expansion. The selected contact equations can be continued across clearance and section boundaries without claiming that the continued points are physical. The actual nonlinear physical and section decisions then remain in the density integral. This separates the deterioration of physical angular sets from the regularity of the contact coordinates.

## 1. New mathematical results

### 1.1 An incidence-normalized contact inverse

Module 140, `lem:v66-weighted-inverse`, strengthens the inherited contact estimate to

\[
 |(A^{-1})_{ij}|\le C\min(c_i,c_j)q^{|i-j|},\qquad q=47/53.
\]

The final diagonal factor in the Neumann series retains one incidence, and symmetry supplies the other choice. The normalized Hessian `N=A D_c` therefore has a uniformly bounded inverse in the norm with weights `sigma^{min(j,m-j)}`, `sigma=sqrt(q)`. No product of inverse incidences remains in this inverse bound.

We then divide the stationary equation at contact `j` by its **frozen base incidence**, not by a variable whose derivatives would have to be estimated. The stationary equations depend only on three neighboring contacts. On the tapered class `c_j >= chi q^{min(j,m-j)/4}`, their weighted nonlinear derivatives have bounds independent of the collision count. A quantitative contraction argument gives contact derivatives of orders one, two and three, bounded respectively by `C sigma^{d_j}`, `C chi^{-1} sigma^{d_j}`, and `C chi^{-2} sigma^{d_j}`.

The theorem no longer assumes positive clearance or section margins. It is a theorem about the selected-contact continuation. Every point failing an original physical decision has zero source weight later.

### 1.2 Uniform Morse coordinates and an exact physical angular profile

Theorem `thm:v66-uniform-morse` gives a common Morse radius `r_chi=r_0 chi^3`, roof radius `h_chi=r_chi^2/2` and relative density budget `K_chi=C chi^{-2}`. These are uniform in the collision count within the stated tapered incidence class. The determinant formula gives a relative source estimate without a lower bound for the individual coefficient `J_z`.

Module 141 keeps the **nonlinear** physical first-hit and exact-label indicators. Its angular integral `A_{z,n,k}^epsilon(h)` is not the v65 affine integral and is not asserted to have a uniformly computed angular shape. Positive polar coarea gives

\[
 e^{-K_\chi\sqrt{2h}}\frac{J_z}{2\pi}A_{z,n,k}^{\varepsilon}(h)
 \le b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+h)
 \le e^{K_\chi\sqrt{2h}}\frac{J_z}{2\pi}A_{z,n,k}^{\varepsilon}(h).
\]

Thus a small boundary gradient does not appear in the error constant. The error is relative to the actual retained physical angular weight, rather than to the sum of unrestricted full-word weights. The entire exact-label vector is controlled with no label-count multiplier.

For `epsilon <= chi/4`, all selected incidence guards equal one on the common chart. Endpoint influence also gives a count-uniform Lipschitz bound for the original clearance multiplier. At a zero-clearance seam the multiplier equals one on a disk of radius `min(r_chi,epsilon/C_g)`, including simultaneous seams and section coincidences. This statement preserves the first-defect telescoping order and the image mark `j+1`.

### 1.3 A physical trace with a proved ordered bound

Module 142 constructs a trace from the actual physical collar mass:

\[
 \mathcal Q_{m,s;n,k,R}
 =\sum_z\left(s^{-1}\int_0^s b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+u)\,du\right)\delta_{t_z}.
\]

It is not a spectral trace previously constructed in the article, nor the full reversible trace of v65. The physical chart pieces are disjoint. Their endpoints lie in two normal strips of width `C sqrt(s)` and their actual roofs lie in an interval of length `2h+s`. The inherited exact-label two-strip local theorem therefore gives

\[
 \limsup_{m\to\infty}\sup_{R,n,k,t}m^2\mathcal Q_{m,s;n,k,R}([t-h,t+h])
 \le C(2h+s).
\]

Both widths are fixed before the collision limit. In particular the expression with `h=s` vanishes as `s` decreases to zero **after** that limit. This proves an exact geometric-to-dynamical bridge for a specified positive physical trace; it uses no mean-square annular estimate, word-count bound, cancellation, or assumed separation of critical values.

At fixed finite count the zero-width coefficient is `beta_{z,n,k}=J_z theta_{z,n,k}`, with the physical exact-label angular fraction. The full coefficient `J_z` is not generally this observable coefficient. The positive comparison

\[
 \mathcal B_m(I)\le e^{K_\chi\sqrt{2s}}\mathcal Q_{m,s}(I)+\mathcal D_{m,s}(I)
\]

isolates the angular loss `D` between the exact nonlinear set and its tangent fraction. Its uniform normalized smallness is stated as an additional, unproved input. This is not an interchange of the two limits.

## 2. Responses to the requested changes

### Report 31.1: uniform source coverage

**Substantially advanced for a precisely specified class, not closed for the entire source.** Modules 140–141 give common coordinates, contact jets, guard admissibility and relative density for every normal critical physical-side word satisfying the tapered incidence envelope. Unlike the old protected-collar theorem, they permit zero clearance and section margins. They avoid individual boundary-gradient lower bounds by retaining the exact nonlinear angular sets. They do not establish such lower bounds, selected-grazing coverage, or coverage of every noncritical roof-rank component.

### Report 31.2: reversible-weight concentration

**The full v65 atomic concentration estimate remains unproved.** The new proved estimate concerns the finite-width physical trace `Q`, not the full reversible measure `T`. The zero-width physical trace `B` also retains an unproved angular-loss input. The three measures are defined separately in the manuscript and in the status manifest. Individual exponential decay is not used to bound their sum.

### Report 31.3: the positive complement

**The complement is preserved, not declared negligible.** Equation `eq:v66-complete-positive-partition` retains all source outside the verified chart pieces, including selected-grazing neighborhoods, violations of the tapered envelope, noncritical rank components and annuli removed when a chart is shortened. No mass or support estimate is promoted to a pointwise height estimate. No probability is assigned to a nonphysical continuation.

### Report 31.4: complete incidence height

**Not closed in this revision.** The inherited inverse-incidence density theorem remains unchanged, with its exponential finite-count factor. The new normalized inverse is used for contact continuation and relative distortion; it is not asserted to bound the full exact-label incidence density. The corresponding status remains false.

### Report 31.5: complete clearance height

**The uniform chart contribution is resolved into an exact angular integral; the complete ordered height is not closed.** Both the nonlinear angular height and the positive outside source still require control. The physical width is fixed before the collision limit. The v63 threshold is explicitly noted to fail eventually at every fixed positive width, and is not used in the new proof.

### Report 31.6: unrestricted pointwise theorem and consequences

**The target is unchanged, and no unsupported endpoint conclusion is added.** The complete integrated arithmetic record theorem and coupled path results remain compiled. The unrestricted two-sided pointwise arithmetic local limit, unrestricted same-roof bridges, forward essential likelihood and pointwise roof-conditioned paths remain separate from those integrated conclusions. The corresponding status flags are not changed to true.

### Report 31.7: connect geometry and dynamics

**Closed for the newly specified finite-width physical trace.** The exact positive comparison `eq:v66-positive-trace-comparison` links the original physical collar to the inherited two-normal-endpoint local law at the same exact return index, displacement and collision count. The construction allows label changes inside a chart rather than assigning every chart the label of its singular center. The additional atomic-to-collar comparison states the remaining angular loss explicitly. This is not presented as the still-missing theorem for the full reversible trace.

### Report 31.8: qualification metadata

Both new author branches are created before the final source update, so that the same final source can receive two distinct push-triggered qualification runs. The new workflow records the exact checkout SHA, preserves the reviewed paper tree, checks every inherited source file and label, runs finite diagnostics in normal and optimized Python, compiles the full TeX manuscript and renders the new theorem pages. Each run's identity and actual conclusion must be read from GitHub Actions; this response does not predeclare success. Finite diagnostics and a successful build are not continuum proof certificates.

### Report 31.9: independent expert review

**Not obtained.** No independent human specialist audit is claimed. The source and report are frozen for such an audit. Particular new points are the frozen-incidence row normalization, the weighted implicit-function estimates, the interpretation of the continued contact graph, the exact guard on that graph, the physical chart disjointness and the use of the inherited endpoint local theorem. The earlier operator, collision-graph and semialgebraic dependencies remain in the audit map.

### Report 31.10: reduce the journal proof burden

The front of the article now states two principal theorems and the short dependency route through modules 140–142. The old abstract and introduction are compiled in `appendices/v65_frontmatter.tex`; the full old main file is additionally preserved verbatim in provenance. All 139 inherited core modules, all 191 inherited Python files, all prior appendices and the bibliography are byte-identical. The history is not deleted, and a local coordinate theorem is not represented as completion of the original pointwise target.

## 3. Technical conventions retained

The manuscript distinguishes reconstruction band, physical guard width, tapered incidence parameter, Morse radius and collar roof width. It retains the square root in the reversible determinant, the original half-word labels, the absence of primitive-period division, and the physical-side meaning of a derivative at a seam. It uses common coarea representatives almost everywhere in the roof. Coincident critical values add positively. Initial membership, occupation and terminal membership remain separate. The new relative vector estimate has no output-label factor.

The original finite arithmetic kernel and its zero classes remain. No conditional law or likelihood is assigned to a zero reference class. Probability total variation, variation mass and path bounded-Lipschitz norms remain distinct. All first-defect pieces, including later incidences after a first clearance outside the incidence-controlled charts, remain on the original source.

## 4. Scope of the present revision

The new results remove collision-count dependence from the selected-contact chart and its relative density under the stated tapered incidence envelope, and prove an ordered estimate for an actual positive physical collar trace. They do not complete the full source height theorem. The next unresolved mathematical quantities are now explicitly the physical angular loss, pointwise angular concentration, and the incidence/outside-source heights. This revision makes no claim of journal acceptance, formal proof certification, or independent specialist verification.
