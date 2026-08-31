# Independent Referee Report — Round Eleven

**Manuscript:** A2 — Sinai Homological Pressure  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/A2_EVEN_BIRTH_CERTIFIED_FOURIER_LLT.tex` (Git blob `a73417bb66470bb7fa509b92dfb3bd172d1ef736`)

## Executive assessment

The paper now separates arithmetic aperiodicity, geometric UNI, moderate frequency, very high frequency, and the different roof-window regimes. It also abandons the impossible period-one winding orbits used in round ten. These are substantive improvements.

The replacement theorem is nevertheless not established. The birth coordinate is internally inconsistent, the claimed evenness does not follow from branch exchange, the “certificate” contains only asserted output numbers rather than interval boxes or reflection equations, and the four-range Fourier argument leaves a large frequency interval uncovered. The local limit theorem therefore has no proved analytic input.

## Major mathematical objections

### 1. The signed square-root coordinate is algebraically inconsistent

The manuscript defines

\[
s=\operatorname{sgn}(R-R_0)|R-R_0|^{1/2}
\]

and then writes \(R=R_0+s^2\). For \(R<R_0\), the first formula gives \(s<0\), but the second gives \(R>R_0\). The correct relation would be \(R-R_0=s|s|\), not \(s^2\).

This is not notation only: the proof treats \(s\mapsto-s\) both as crossing the birth and as exchanging two newborn branches. Those are different operations.

### 2. Physical evenness at a branch birth is not implied by branch exchange

A pair of newborn branches exists only on the birth side. Exchanging the two branches on that side may make their sum even in a local square-root coordinate, but it does not analytically continue the physical operator through the no-branch side. A contribution of the form

\[
1_{R>R_0}\bigl(T_{+,R}+T_{-,R}\bigr)
\]

is not made \(R\)-differentiable by the fact that the two summands exchange. The theorem needs a genuine fold pushforward calculation showing cancellation of the turn-on singularity in the physical norm. No such calculation is provided.

Consequently the formula

\[
\partial_R\mathcal L_R|_{R_0}
=\tfrac12\partial_s^2\mathcal L_s|_0
\]

has not been justified.

### 3. The periodic-orbit “certificate” is not a certificate

The repository JSON lists orbit names, homologies, collision counts, narrow roof intervals, incidence bounds, clearances, and one determinant lower bound. It does not contain:

- impact-coordinate interval boxes;
- the scatterer lifts visited by each segment;
- interval enclosures for the reflection equations;
- the implicit-function matrices;
- neighboring-scatterer distance calculations; or
- chart-by-chart continuation data over \(R\in[0.45,0.47]\).

The proof repeatedly says that these objects are in the certificate, but they are absent. A list of claimed outputs cannot verify existence of the five regular periodic orbits or the determinant theorem.

The nearly constant roof intervals across a nontrivial radius interval are especially in need of the missing geometric data.

### 4. The Fourier ranges do not cover the Fourier line

Range (iii) is announced for

\[
n^K<|b|\le e^{\delta n},
\]

but the Dolgopyat estimate is used only on the subrange where

\[
|b|^A e^{-cn/\log|b|}
\le e^{-c'n/\log n}.
\]

For large \(|b|\), the left side grows; the condition fails well before \(e^{\delta n}\). Range (iv) begins only at \(|b|>e^{\delta n}\). Hence an entire intermediate band is untreated. Calling the theorem “four-range” does not fill that gap.

### 5. The very-high-frequency integration by parts is not global

One returned UNI pair supplies a nonstationary direction on a selected branch pair. It does not provide an integration coordinate with a uniform derivative on every homogeneous inverse branch occurring in the full transfer sum. Singular cutoffs, branch endpoints, and amplitude derivatives must be controlled under repeated integration by parts. The proof merely states the desired factorial bound.

### 6. The density LLT depends on unproved error estimates

The final proof says that all three nonsmall ranges are integrable \(o(n^{-3/2})\) errors. No bound establishing this appears. In particular, the uncovered intermediate band already prevents the conclusion. Uniformity with a cylinder insertion also requires trace estimates through the moving singularity bundle, not the assertion that the insertion is a bounded multiplier.

### 7. The moving-billiard spectral theorem remains compressed into a paragraph

Uniform Riesz contours, graph Lasota–Yorke estimates, material derivatives, birth charts, and cylinder traces are still the model-specific main theorem. The manuscript names these inputs but supplies no quantitative construction sufficient for external verification.

## Status of earlier objections

The false one-collision orbit packet and the previously incorrect roof-window normalization are removed. Arithmetic and UNI are now conceptually separated. The replacement arithmetic, birth, and high-frequency theorems remain unproved or internally inconsistent.

## Minimum reconstruction

The authors should first produce a standalone computer-assisted periodic/UNI appendix with complete interval data and an independently checkable verifier. They must then formulate a correct one-sided fold theorem, prove the parameter-uniform transfer bundle, and give a frequency partition whose estimates cover every \(b\in\mathbb R\) with integrable constants.

## Recommendation

**Reject.** The paper advertises a verified billiard packet, but the geometric certificate is only a summary of assertions and the Fourier proof has an explicit uncovered frequency range.