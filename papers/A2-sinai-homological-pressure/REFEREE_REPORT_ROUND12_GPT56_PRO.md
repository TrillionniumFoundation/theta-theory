# Independent Referee Report — Round 12

**Manuscript:** A2 — *Sinai Homological Pressure*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `57e16a01bb276cdd499d65aa7fc1c6933520519761e5adbefcd42c1faa2ff11b`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 makes several correct strategic changes: the physical parent branch is distinguished from its symbolic cut representation; the impossible period-one winding certificate is removed; arithmetic obstruction and geometric UNI are separated; and the roof-window theorem is stated using the exact conditional Gaussian interval mass.

The Fourier theorem still contains two direct contradictions. First, its purported compact-frequency spectral gap includes frequencies tending to zero, where the leading eigenvalue necessarily tends to one. Second, its very-high-frequency estimate contains a positive constant term on an infinite frequency interval, so the asserted Fourier integrability is impossible. These are failures of the displayed theorem, not missing cosmetic estimates. The moving-billiard bundle and UNI arguments also remain compressed sketches of the main model-specific work.

## Decisive objections

### 1. Range (ii) cannot have a uniform spectral gap

The frequency partition contains

\[
n^{-2/5}<|b|\le b_0.
\]

The manuscript calls this a “uniform compact-frequency spectral gap.” But for the leading twisted eigenvalue,

\[
\lambda_R(ib)
=1-\frac12\sigma_R^2 b^2+O(|b|^3)
\]

near \(b=0\). Hence

\[
|\lambda_R(i n^{-2/5})|
=1-O(n^{-4/5})\longrightarrow1.
\]

There is no fixed \(c>0\) for which the spectral radius is at most \(1-c\) throughout that range. The required estimate is a covariance damping bound of the form

\[
|\lambda_R(ib)|^n\le e^{-cnb^2},
\]

not a compact nonzero-frequency gap. The proof invokes arithmetic obstruction and compactness, neither of which is uniform as the lower endpoint approaches zero.

### 2. The very-high-frequency estimate is not Fourier integrable

Lemma 4.1 states, for every \(|b|>L_n\),

\[
\|\mathcal L_{R,iu,ib}^n\|
\le Ce^{-cn}+C\left(\frac C{|b|}\right)^{\eta n}.
\]

The first term is independent of \(b\). Therefore

\[
\int_{L_n}^{\infty}Ce^{-cn}\,db=\infty.
\]

The manuscript nevertheless concludes that all nonsmall frequency ranges are integrable \(o(n^{-3/2})\) errors. This conclusion does not follow from the displayed estimate and is, as written, false.

If the \(Ce^{-cn}\) term represents a bad standard-family sector, that sector still needs its own frequency decay before Fourier inversion. Exponentially small mass alone is not an integrable bound over an unbounded Fourier line.

### 3. The multi-block integration-by-parts product is not established

The proof claims that an itinerary contains \(\eta n\) disjoint returned UNI blocks and that one integration by parts on each block produces

\[
(C/|b|)^{\eta n}.
\]

This requires much more than a returned-branch UNI derivative:

- a global product coordinate in which all selected phases can be integrated independently;
- uniform control of derivatives created when earlier integrations hit later amplitudes and holonomies;
- cancellation of every branch endpoint and homogeneity-strip boundary term;
- a distortion bound that remains multiplicative through \(O(n)\) integrations; and
- uniformity with central-cylinder insertions and material derivatives.

The proof simply assigns all homogeneity endpoints to an exponentially small bad family. Partition endpoints are present in every standard-family decomposition; their total boundary contribution is not automatically exponentially small. No theorem proves the stated product estimate.

### 4. The periodic obstruction theorem is still asserted rather than constructed

The manuscript now avoids period-one winding orbits, which is correct. It replaces them with “regular periodic orbits with homologies \(e_1,e_2\)” obtained from topological mixing and a finite connector family. Topological mixing supplies symbolic connections, not a parameter-uniform geometric continuation with explicit grazing clearance, singularity avoidance, roof regularity, and common homogeneous charts over the entire radius interval.

Likewise, a nonconstant temporal-distance function on two inverse branches does not by itself produce the four-coordinate periodic rank theorem without closing those branches into regular periodic points and controlling the resulting roof sums. These are the central billiard estimates and cannot be compressed into one paragraph.

### 5. The parent-fold identity does not establish the full material bundle theorem

Writing a parent integral as the sum of its two cut pieces is algebraically valid. It does not by itself prove that the anisotropic norms, stable-curve traces, holonomies, strong-to-weak compactness, and all material derivatives are uniform when the singularity partition changes. In billiard spaces, the difficulty is not equality of two scalar integrals; it is uniform control of the moving discontinuity geometry on the operator scale.

The proof of Theorem 2.2 names the growth lemma, compactness, and a common resolvent contour but does not verify the branch-complexity and trace estimates required for this radius family.

### 6. The density formula is not fully typed

The displayed LLT uses

\[
e^{-\frac12z^T\Sigma_R^{-1}z}
\]

without defining \(z\). If \(z=(k-na,t-n\bar\tau)\) is the raw deviation, the exponent is missing a factor \(1/n\). If \(z\) is normalized by \(\sqrt n\), that normalization must be stated, especially because the theorem then integrates over windows expressed in unnormalized roof units.

This ambiguity is load-bearing for every local, central, and saddle-varying window formula.

### 7. The claimed LLT therefore remains unavailable downstream

A3 and A4 use A2 for clock coefficients, inserted spectral data, and high-frequency resolvent control. The two direct Fourier defects above prevent those interfaces from being treated as proved inputs.

## Genuine improvements recognized

The following Round 12 changes should be retained:

- use of the signed fold coordinate \(r=s|s|\);
- separation of the parent physical branch from symbolic cut pieces;
- deletion of period-one winding orbits;
- separation of arithmetic obstruction from UNI;
- the threshold \(L_n=e^{\kappa\sqrt n}\), rather than extrapolating a Dolgopyat estimate to all frequencies; and
- exact Gaussian interval masses for subcentral, central, and saturated roof windows.

These improvements do not close the actual Fourier theorem.

## Required reconstruction

A publishable paper would need to prove, in a single fully specified anisotropic bundle:

1. the moving-cut Lasota–Yorke and material trace estimates;
2. an explicit regular periodic rank certificate throughout the radius interval;
3. a returned-branch UNI theorem with all branch domains and derivatives;
4. a frequency decomposition whose bounds are genuinely integrable on every region; and
5. a correctly normalized density LLT with relative errors strong enough for inserted conditioning.

## Recommendation

**Reject.** The Round 12 theorem still fails at the level of elementary Fourier integration and small-frequency perturbation. The model-specific moving-billiard and multi-block estimates are also asserted rather than proved. This paper cannot serve as the spectral/local-limit gate for the series.