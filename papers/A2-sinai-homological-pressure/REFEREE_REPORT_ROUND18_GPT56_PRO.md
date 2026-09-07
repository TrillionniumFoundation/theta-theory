# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`A2_MATRIX_COEFFICIENT_RAW_LLT.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The unsmoothed four-dimensional local limit theorem is not proved.

## 1. Overall assessment

This revision correctly abandons the earlier attempt to repair a non-trace-class operator by a trace-class correction and no longer conflates flat trace, nuclear trace, and ordinary matrix coefficients. That is a material conceptual improvement. Formulating the characteristic function as

\[
\Phi_{n,R}^{\ell}(u,s,b)=\ell_R(\mathcal L_{R,u,s,b}^n h_R)
\]

is the right type of object for Fourier inversion.

The replacement proof, however, does not construct the claimed uniform induced Banach bundle or establish the high-frequency bounds needed for raw Fourier inversion. Several statements are internally impossible or lack the quantitative content required by their own later use. The central LLT and all downstream conditioning conclusions therefore remain unavailable.

## 2. Decisive mathematical objections

### 2.1. [FATAL] The branch-complexity hypothesis in `thm:r17-a2-bundle` cannot hold as written

Item (iii) asserts

\[
\sum_h e^{\eta r_h}\bigl(\|J_h\|_{C^2}+\|\tau_{R,h}\|_{C^4}+\|\partial_R^4\tau_{R,h}\|_{C^0}\bigr)<C.
\]

The induced map has countably many return branches. The roof on every nonempty branch is positive, and in a finite-horizon billiard it is bounded below in terms of the return count. Thus an **unweighted** sum of positive `C^4` roof norms, multiplied by `e^{\eta r_h}`, cannot be finite over infinitely many branches. The same problem affects an unweighted sum of Jacobian norms unless `J_h` means a small inverse-Jacobian weight, which is not defined here.

What one normally needs is a probability/Jacobian-weighted summability estimate, or an operator norm estimate in which expansion and branch measure compensate complexity. No such weight appears in the theorem. Because item (iii) is used to sum all differentiated amplitudes and boundary pieces, this is a fatal defect rather than a typographical inconvenience.

### 2.2. [FATAL] The “uniform parent-fold Banach bundle” is asserted, not constructed

The proof of `thm:r17-a2-bundle` invokes a standard family of Young magnets, parent labels, stable-curve trace theorems, the growth lemma, exponential return tails, and Keller–Liverani perturbation. None of these ingredients is formulated with the uniformity actually claimed over `R\in[0.45,0.47]`.

In particular, the manuscript does not provide:

1. a common symbolic/branch index set or an explicit rule for branch births and deaths;
2. transport maps between the anisotropic spaces, including their action at folds and homogeneity cuts;
3. uniform one-step and iterated Lasota–Yorke inequalities for all twisted operators;
4. compact embeddings for the transported strong/weak pairs;
5. differentiability of the operator family in `R` on a fixed pair of spaces;
6. compatibility of local spectral projectors on chart overlaps.

Keeping two one-sided traces at a fold is a useful bookkeeping idea, but it does not prove bounded perturbation theory. The claimed analytic twist and `C^2` radius dependence of the leading projector are among the deepest points of the paper and cannot be obtained from a paragraph of references to standard tools.

### 2.3. [MAJOR] The arithmetic/UNI certificate is not converted into a mathematical proof

The periodic-loop and branch boxes are referred to through a JSON certificate. A computer-assisted certificate can be part of a proof, but the paper must state the exact interval equations, rounding model, covering argument, and implication from the certified boxes to the global cohomological obstruction.

The proof of `lem:r17-a2-arithmetic` also says that a coboundary has “equal returned derivatives” on the two selected branches. This is not true without a precise common-endpoint or common-suffix cancellation identity. For

\[
e^{i\phi}=e^{ic}g/(g\circ F),
\]

the derivative of the coboundary term depends on both inverse branches and their endpoints. One must write the branch compositions and show exactly which `g`-terms cancel. The manuscript does not do this, and the constant phase `c` and return periods are not tracked in the periodic-loop argument.

### 2.4. [FATAL] Lemma `lem:r17-a2-ibp` does not establish branchwise high-frequency decay

The “raw branchwise integration by parts” lemma is the decisive new ingredient. Its proof is only a program. It does not specify:

- the branchwise integration variables and their domains;
- the smooth partition and uniform derivative bounds of its cutoffs;
- how boundary terms created at homogeneity and singularity cuts cancel or are controlled;
- the Jacobian of the proposed phase-difference coordinate;
- the distortion cost after repeated differentiation;
- a quantitative large-deviation estimate for the number of disjoint UNI blocks in a branch word;
- uniformity in `(u,s)` and in the central insertion `\ell`.

The statement that boundary pieces are “reexpressed by the two trace components” is insufficient. A trace component records a boundary distribution; it does not make the corresponding term vanish, nor does it automatically give the same `b^{-M}` decay.

The treatment of exceptional words is especially unsupported. The manuscript says that every such word still contains “two ordinary non-grazing flight coordinates,” so two coarea integrations yield `(1+|b|)^{-2}`. No theorem proves the existence of those two independent coordinates uniformly for every exceptional branch, nor that the conditional amplitude has the required two derivatives up to the relevant boundaries.

### 2.5. [FATAL] The constants in the repeated integration-by-parts argument are not compatible with the selected frequency split

The lemma gives a term

\[
C_M e^{c_M n}(1+|b|)^{-M}.
\]

The proof of `thm:r17-a2-fourier` then chooses `M` so that

\[
(M-1)\kappa>c_M+2\kappa.
\]

There is no estimate at all on the growth of `c_M` with `M`. Repeated differentiation of billiard inverse branches and partitions can make `c_M` grow at least linearly and often much faster. It may therefore be impossible to find an `M` satisfying the displayed inequality for the previously fixed `\kappa`. The statement “choose `M`” is circular unless a quantitative relation such as `c_M\le c_0+c_1M` with `\kappa>c_1` is proved, or a different frequency/block optimization is supplied.

Similarly, the medium-frequency Dolgopyat estimate

\[
|\Phi_n|\le C(1+|b|)^A e^{-cn},\qquad 1\le |b|\le e^{\kappa n},
\]

is merely attributed to the one UNI pair. A Dolgopyat theorem for this anisotropic, countable-branch, parameter-dependent operator family requires cone/phase cancellation, norm estimates, and nonconcentration arguments that are absent.

### 2.6. [MAJOR] Nondegeneracy of the full covariance is not proved

The paper says that arithmetic obstruction and returned UNI imply

\[
cI_4\le\Sigma_R\le CI_4.
\]

Aperiodicity of the lattice coordinates and nonintegrability of the roof exclude certain exact coboundaries, but a uniform positive lower bound for the entire tilted `4\times4` covariance requires a quantitative argument ruling out every real linear combination of homology, return count, and roof as a coboundary, uniformly over `R` and over the real tilt chart. The five certified loops and one temporal pair might furnish such an argument, but the relevant determinant/variance estimate is not written.

### 2.7. [FATAL] The raw LLT has no established integrable majorant

Theorem `thm:r17-a2-llt` depends completely on `thm:r17-a2-fourier`. Because the compact-minor-arc spectral estimate, medium-frequency Dolgopyat estimate, and very-high-frequency IBP estimate have not been proved, the claimed `o(n^{-2})` complement is unavailable. The Gaussian calculation near zero is standard only after a genuine uniform cubic pressure expansion and covariance theorem are supplied.

The statement that the joint law has a density in the roof coordinate also needs proof. Absolute continuity of each branch roof push-forward, including critical points and singular branch boundaries, is not automatic from the formal Fourier representation.

### 2.8. [MAJOR] The conditioning corollary exceeds the range of the LLT even as stated

Corollary `cor:r17-a2-conditioning` applies the density theorem to “any roof interval” and claims local, central, and saturated regimes. The LLT itself is stated only for points in an `O(\sqrt n)` central window. It does not control arbitrary shrinking intervals, intervals outside the central range, exponentially small windows, or saturated/far-tail regimes. Nor is the denominator uniformly positive for an arbitrary interval. Separate moderate/large-deviation estimates and a precise admissible window class are necessary.

## 3. Dependency consequences

A2 is the first gate in the Sinai chain. Without its raw Fourier theorem and density LLT, the uses of A2 in A3 conditioning, A4 renewal continuation, C1 regular observation charts, C2 optional-projection/statistical interfaces, and D1 phase charts are not licensed. This is not a minor local defect: the principal downstream analytic input is absent.

## 4. Requirements before reconsideration

A future submission would need:

1. a correct, Jacobian-weighted countable-branch summability theorem;
2. a fully specified uniform anisotropic Banach bundle over the radius family;
3. a reproducible computer-assisted arithmetic/UNI proof embedded in the mathematics;
4. a complete Dolgopyat theorem with explicit norm and parameter estimates;
5. a branchwise IBP theorem including cutoffs, boundary traces, block-frequency estimates, and growth of constants with derivative order;
6. a quantitative full-covariance nondegeneracy argument;
7. a Fourier inversion theorem with a rigorously integrable global majorant and precisely delimited conditioning windows.

## 5. Recommendation

**Reject.** The revision fixes the category error involving traces, but replaces it with an unproved high-frequency program. One of the bundle hypotheses is impossible as written, and the decisive medium- and high-frequency bounds are not derived. The claimed raw four-dimensional LLT is therefore not established.