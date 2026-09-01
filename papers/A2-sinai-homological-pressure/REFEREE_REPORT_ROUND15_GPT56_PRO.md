# Independent Referee Report — Round 15

**Manuscript:** A2 — *Sinai Homological Pressure*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Recoverable registered Round-Fifteen candidate:** `A2_INDUCED_BUNDLE_FOURIER_LLT.tex` from the truncated checksum-pinned payload  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence boundary

The paper folder still loads Round Fourteen. The Round-Fifteen candidate was not materialized into the manuscript, and no Round-Fifteen certificate exists. A complete copy of the A2 candidate was recoverable from the surviving payload, so I reviewed it as a supplemental candidate—not as the controlling paper.

## Executive assessment

The candidate makes two real improvements: it fixes one induced return map carrying homology, return count, and roof on the same branches, and it retains the correct four-dimensional \(n^{-2}\) Gaussian prefactor. The central local-limit theorem is nevertheless not proved. Its only integrable very-high-frequency estimate is obtained after multiplying by the Fourier transform of an externally inserted smooth time test. That establishes a smoothed coefficient, not the raw roof density stated in the theorem.

The parent-fold bundle, lattice-span construction, and returned UNI are also asserted at the level of geometric sketches rather than a verifiable uniform billiard proof.

## Decisive objections

### 1. The high-frequency theorem proves only a smoothed statement

The candidate's unsmoothed bound is

\[
\|\mathcal L_{u,s,b}^n\|
\le C(1+|b|)^A
\exp\{-cn/\log(2+|b|)\}.
\]

As \(|b|\to\infty\), the exponential factor tends to one and the right side grows polynomially. It is not integrable on the Fourier line.

Integrability is recovered only after inserting \(g\in C_c^M\):

\[
|\widehat g(b)[z^kw^m]\mathcal L_{z,w,b}^n|
\le C_M(1+|b|)^{-M+A}
e^{-cn/\log(2+|b|)}.
\]

Fourier inversion of this expression gives convolution of the roof law with \(g\), or evaluation against a smooth time test. It does not give the pointwise density

\[
p_{n,R}(k,m,t)
\]

asserted later.

To recover a density from smooth tests, one would need an approximate identity \(g_n\) whose derivatives grow with \(n\), together with estimates uniform in those derivative norms. The theorem explicitly fixes \(g\), and its constants depend on the inserted test. The passage from the smoothed estimate to the raw density is therefore invalid.

### 2. The LLT proof cites the wrong input

The proof of the four-dimensional LLT says the moderate and very-high ranges are controlled by the Fourier theorem. The very-high part of that theorem is available only with \(\widehat g(b)\). No such \(g\) occurs in the density inversion. Hence the complementary Fourier integral is uncontrolled and the displayed local density theorem does not follow.

Every ratio-conditioning corollary that needs an unsmoothed denominator inherits this gap.

### 3. The source contains a corrupted scale statement

The UNI proof contains the text

\[
|b|^{-1}\,\texttt{egl},
\]

which is not a mathematical expression. This is not harmless in context: the precise unstable interval scale and derivative/cutoff costs determine the high-frequency estimate.

### 4. The induced Banach bundle is not constructed

The argument states that a common finite family of magnets, parent homogeneous branches, complemented fibers, compact embeddings, moving-fold traces, and \(C^2\) parameter transport all exist uniformly in \(R\). These are the principal model-specific theorems. “Finite horizon, growth lemma, compactness” does not prove compatibility of varying singularity partitions or bounded complement projections.

The paper needs full definitions of the spaces, norms, identifications, and fold operators, followed by uniform one-step expansion, distortion, complexity, trace, and Lasota–Yorke estimates.

### 5. Lattice rank and UNI are described, not verified

The four periodic return loops are obtained by an informal reachability argument. No collision coordinates, reflection equations, incidence bounds, or clearance estimates are supplied. Likewise, nonzero roof derivative at one “central orbit” is promoted to a uniform returned-branch UNI statement without a computed orbit or a parameter-uniform continuation proof.

These facts may hold for a suitable family, but they are not established by the text.

### 6. The coefficient notation is untyped

The operator is defined using angular variables \(u\in\mathbb T^2\) and \(s\in\mathbb T\), yet the high-frequency statement suddenly uses

\[
[z^kw^m]\mathcal L_{R,z,w,b}^n.
\]

No analytic variables \(z,w\), domains, or relation to the angular Fourier coefficients are defined. This matters for uniformity in \(k,m\) and for contour deformation under real tilts.

## Required reconstruction

A serious submission should first prove one theorem: an unsmoothed, integrable vector–return–roof Fourier estimate for one fully specified induced billiard operator. It must either derive actual vertical decay of the operator kernel or state only a smooth-test LLT. The common bundle, periodic loops, and UNI pair require explicit constructions with uniform constants.

## Recommendation

**Reject.** Round Fifteen is not the controlling manuscript, and even the recoverable candidate proves only a smoothed time coefficient while claiming a raw four-dimensional density LLT.
