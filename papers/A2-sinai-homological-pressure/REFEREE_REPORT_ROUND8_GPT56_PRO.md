# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `df062b12677dc42cc2f59c50c3f6f674c5a0872b`

## Executive assessment

Round eight separates three issues that were conflated previously: geometric birth/death of trace components, compact-frequency arithmetic, and high-frequency UNI. It also corrects the missing factor in the roof-window scaling. These are substantive repairs.

The principal theorems are still not proved. The birth bundle theorem is conditional on a transverse closed-range hypothesis never established for the billiard trace realization, and its renormalized coordinates are incompatible with the claimed uniform parameter derivatives. The periodic argument assumes the desired no-coboundary statement rather than proving it for the Lorentz family. The geometric UNI proof is a sketch whose asserted cancellation of connector legs is unjustified. The Dolgopyat estimate has no quantified block length and is too weak to support Fourier inversion. Finally, the LLT theorem gives only an `o(n^{-1})` absolute remainder but the corollary claims a relative local asymptotic whose main term can be arbitrarily smaller than `n^{-1}`.

## Genuine repairs recognized

The following changes should be preserved:

- no direct isomorphism is asserted between a zero trace space and a nonzero trace space;
- periodic aperiodicity and geometric UNI are treated as distinct mechanisms;
- the joint arithmetic data have the correct four coordinates;
- roof windows are expressed first in the average variable and the missing factor of `n` is restored;
- one target-dependent saddle is used rather than multiplying incompatible Gaussian factors.

## Major mathematical objections

### 1. The uniform birth chart is a conditional lemma, not a theorem for the billiard family

Lemma `r8-a2-birth` begins with the assumption that

\[
E_{R_0}^{\rm old}
\quad\text{and}\quad
\widetilde E_{R_0}^{\rm b}
\]

have transverse closed ranges. This is precisely the difficult geometric-functional statement at a moving tangency. The manuscript does not construct these ranges, prove closedness in the declared anisotropic distribution norm, or establish a uniformly complemented sum.

The subsequent continuous-field theorem simply cites the lemma and “the usual branch estimate.” Thus the load-bearing moving-singularity theorem remains an assumption.

### 2. The renormalized coordinate is not compatible with the claimed uniform shape derivatives

Near a birth, the physical variable is

\[
z=(R-R_0)y.
\]

The fiber norm makes `y` cheap as `R -> R_0`, which can make the realization uniformly bounded. But a fixed physical perturbation `z` corresponds to

\[
y=\frac{z}{R-R_0}.
\]

Differentiating the chart or a transported operator in `R` therefore produces inverse powers of `R-R_0` unless a precise connection cancels them. No such connection, domain scale, or compatibility formula is constructed. A continuous field of normed spaces does not by itself imply that the transfer operators have `m` uniform parameter derivatives across the rank-changing point.

### 3. The periodic certificate assumes the desired aperiodicity

Lemma `r8-a2-span` assumes that no nonzero affine combination of

\[
\kappa_R^{(1)},\ \kappa_R^{(2)},\ \tau_R,\ 1
\]

is a coboundary. It then derives a finite periodic certificate. That implication is standard. What the paper needs is a proof of the hypothesis for the specified periodic Lorentz-gas family, uniformly in geometry and under nearby tilts.

No actual periodic words, collision coordinates, determinant, or geometric exclusion of a coboundary are supplied. “Enumerating words terminates” is an algorithm conditional on nonvanishing; it is not a verification that nonvanishing occurs.

### 4. The geometric UNI argument does not establish a returned branch pair

The proof selects two itineraries leaving one scatterer along different arcs and says that common return connectors contribute “identical terminal legs.” Specification gives admissible connectors, but connectors starting from two different branch endpoints are not identical geometric flights and their roof derivatives do not generally cancel.

Strict convexity also does not by itself imply that the derivative of the total temporal distance is nonzero after all later legs are included. A valid UNI theorem requires an explicit pair of inverse branches, a common quotient interval, distortion control, and a direct lower bound for the derivative of the complete returned roof difference. None is supplied.

### 5. The stated Dolgopyat estimate is not sufficient for Fourier inversion

The theorem states that for a single unspecified block length `n(b)`,

\[
\|\mathcal L_{R,\xi,b}^{n(b)}\|
\le 1-C|b|^{-\gamma}.
\]

It does not state how `n(b)` grows, how the estimate iterates, or what strong/weak norm conversion is lost. Without those data one cannot derive an integrable high-frequency estimate for arbitrary `n`, which is what the LLT Fourier inversion requires.

The proof also calls the face/corner extension “finite triangular” although the moving billiard singularity hierarchy is all-depth. Uniform summability of those off-diagonal blocks is not demonstrated.

### 6. The local-window corollary does not follow from the theorem's error bound

The theorem gives

\[
\mathbb P(\cdots)
=\frac1n\int_{\text{window}}\varphi_\Sigma(\cdots,u)\,du
+o(n^{-1}).
\]

If `G_n << n^{-1/2}`, the claimed main term is

\[
G_n n^{-1/2}=o(n^{-1}).
\]

For example, with `G_n=n^{-1}`, the main term is `n^{-3/2}`, while the allowed remainder is merely `o(n^{-1})` and may dominate it by an arbitrarily large factor. Hence the theorem supplies no relative local asymptotic in the regime asserted by Corollary `r8-a2-regimes`.

A valid local statement needs an error `o(G_n n^{-1/2})`, or a uniform local-density theorem followed by integration, with a smoothing scale tied to `G_n`.

### 7. Sharp Borel windows require a smoothing theorem absent from the text

The statement is uniform over bounded Borel sets with negligible boundary and arbitrarily small `G_n`. High-frequency control of a sharp indicator depends quantitatively on boundary smoothing. The manuscript neither introduces smooth upper/lower approximants nor tracks the Fourier tail against the window width. The one-paragraph inversion proof cannot yield the advertised uniformity.

### 8. The model-specific spectral theorem remains the missing paper

Uniform anisotropic spaces through moving singularities, a verified arithmetic packet, a true UNI estimate, and a joint vector-roof LLT would constitute a substantial theorem. Here each is compressed into a conditional lemma or proof sketch. Internal compilation and a certificate do not replace these estimates.

## Dependency assessment

A2 remains an upstream blocker for A3's finite-projection pressures, A4's conditional homogenization and resolvent continuation, and every downstream Sinai contraction in C2/D1. Those papers may not cite the Round-8 labels as closed interfaces.

## Required reconstruction

A viable submission should isolate and prove one theorem completely:

1. construct a physical quotient strong/weak bundle with an explicit connection through births;
2. verify aperiodicity with concrete periodic words;
3. prove a separate returned-branch UNI theorem;
4. derive a quantified high-frequency bound for all iterates; and
5. state the LLT with error estimates matched to each window regime.

## Recommendation

**Reject.** The scaling correction is welcome, but the local corollary is still mathematically unsupported and the moving-billiard spectral/UNI theorem remains a research program rather than a proof.