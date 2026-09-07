# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** A2 — Sinai Homological Pressure  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `49e756efced03e7d36ef63228122f42900999ae76fb82d8340ab9a3426b63be7`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

The revision correctly separates four logically distinct tasks: moving-geometry regularity, compact-frequency arithmetic, geometric UNI, and very-high-frequency control. It also repairs the missing factor in the vector–roof window scaling and no longer extrapolates a central Gaussian formula to fixed average windows.

The new packet still fails at its geometric and Fourier foundations. Two of the five periodic orbits used in the arithmetic determinant cannot be regular one-collision winding orbits; the birth construction is smooth only in a square-root coordinate while the theorem later differentiates in the original radius; and the moderate-frequency estimate becomes exponentially large at the top of its own range. The very-high-frequency argument contains an additional circular choice of derivative order. Consequently neither the compact-frequency certificate nor the uniform density LLT is established.

## Major mathematical objections

### 1. The claimed primitive one-collision winding orbits are not regular billiard periodic orbits

The certificate lists `w1` and `w2` as one-collision periodic orbits with homologies \(e_1\) and \(e_2\). Consider a period-one collision orbit with lattice displacement \(e_1\). Period one means that, after translating the terminal scatterer back to the fundamental cell, the boundary point and outgoing direction agree with the initial collision state. Hence the free-flight endpoints are corresponding points on two translated copies of the same circle, and the flight direction is parallel to \(e_1\). The normal at the terminal point is the same as the initial normal.

For specular reflection to leave that flight direction unchanged one must have

\[
v-2(v\cdot n)n=v,
\]

so \(v\cdot n=0\). The collision is grazing. The same argument applies to \(e_2\). Thus a regular, non-grazing one-collision winding orbit of the asserted type does not exist.

The first two homology rows of the four-coordinate determinant are therefore built from nonexistent periodic states. The numerical lower bound on a formal determinant does not certify billiard aperiodicity.

### 2. The birth bundle is differentiable in the blown-up coordinate, not in the physical radius

At a branch birth the manuscript writes

\[
T_{r,\pm}=T_0\pm r^{1/2}T_1+O(r)
\]

and obtains regularity in

\[
s=\operatorname{sgn}(r)|r|^{1/2}.
\]

But \(s(R)\) is not differentiable at \(R=R_0\). The physical realization of the odd coordinate contains \(r^{1/2}U^{\rm od}\), whose \(R\)-derivative is of order \(r^{-1/2}\) unless an exact even cancellation is proved for the complete operator and every insertion.

The later spectral theorem nevertheless asserts material derivatives in \(R\), including branch-sensitive cylinder insertions. Smoothness in the blow-up parameter does not imply smoothness in the original radius. The manuscript must either formulate response in \(s\), restrict to even physical combinations, or prove the missing cancellation theorem.

### 3. The moderate-frequency estimate is useless at the top of its declared range

The paper claims, for \(2\le |b|\le e^{\delta n}\),

\[
\|\mathcal L_{R,iu,ib}^n\|
\le C|b|^A\exp\{-cn/\log(2+|b|)\}.
\]

Set \(|b|=e^{\delta n}\). The right-hand side is approximately

\[
C\exp(A\delta n)\exp(-c/\delta),
\]

which grows exponentially in \(n\). It gives neither contraction nor an integrable Fourier bound. Therefore the compact/moderate contribution cannot be declared negligible on the basis of this estimate.

A valid Dolgopyat range must relate the iterate length to \(\log |b|\) so that the polynomial prefactor is dominated. The stated range extends far beyond that regime.

### 4. The very-high-frequency argument is circular

The claimed bound is

\[
C_M e^{C_Mn}|b|^{-M},
\qquad |b|>e^{\delta n},
\]

and the proof says to choose \(M>C_M/\delta+3\). The constant \(C_M\) itself depends on \(M\), through derivatives of inverse branches, amplitudes, singularity partitions, and roof denominators. No growth estimate for \(C_M\) is given, so there is no reason an integer satisfying \(M>C_M/\delta+3\) exists.

Moreover, the UNI theorem supplies a nonstationary phase only for one selected pair of returned branches. It does not give a uniform derivative lower bound on every inverse branch appearing in the full operator. Repeated integration by parts over the entire branch decomposition therefore requires an additional pairing/cancellation construction that is absent.

### 5. The asserted UNI proof is not a verified model-specific theorem

At the symmetric orbit the difference of two momenta may indeed be nonzero. The manuscript then subtracts two unproved global error bounds, each stated as \(1/8\), to obtain \(3/4\). The certificate contains only final numerical values; it does not specify the interval endpoints, branch words, Hessian enclosures, common suffix, singularity distances, or interval-arithmetic proof needed to reproduce those inequalities.

More fundamentally, the existence of a local derivative separation for one pair does not by itself establish the operator-level nonconcentration and branch comparability used in a Dolgopyat estimate on the moving anisotropic trace bundle.

### 6. The density LLT is not proved once the Fourier estimates fail

The corrected scaling of the central Gaussian density is plausible. But the proof relies entirely on the four-range theorem. Since the moderate and very-high ranges are not controlled, the relative density error \(O(n^{-\eta})\), the insertion version, and all three subcentral/saturated window regimes are unsupported.

The theorem also depends on a uniform nonsingular covariance and a target-dependent real saddle over the whole radius interval. These require the very arithmetic/non-coboundary theorem whose periodic certificate is invalidated above.

## Dependency and editorial assessment

A2 is the main upstream gate for A3, A4, C2, and the Sinai part of D1. Until a genuine parameter-uniform moving-billiard spectral/UNI/density theorem is supplied, those papers may not cite this packet as established.

The manuscript should be reduced to one focused result. A viable paper would construct the moving anisotropic bundle and prove a complete vector–roof local limit theorem with explicit, correct periodic orbits and quantitative Fourier ranges. The current omnibus assertion is not close to top-four publication.

## Recommendation

**Reject.** The arithmetic certificate uses nonexistent regular period-one winding orbits, and the key Fourier bound grows exponentially on part of its claimed range. These are fatal mathematical defects, not presentation issues.
