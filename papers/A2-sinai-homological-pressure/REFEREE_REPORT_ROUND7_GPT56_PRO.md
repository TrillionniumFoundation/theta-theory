# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — Sinai Homological Pressure  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `1dd2f7177127c16c694717c38a16de0328ca0d32`

## Executive assessment

The paper correctly recognizes three defects from the preceding round: zero and nonzero trace spaces should not be identified by an invertible chart, four affine coefficients require at least five periodic words, and a cancellation estimate must use genuine near-opposition rather than a generic phase angle. Those are worthwhile corrections.

The replacement still does not establish the advertised spectral/local-limit theorem. The proposed physical quotient has no uniform complement through births and deaths; the five-word certificate is not actually constructed; periodic aperiodicity is confused with the nonlocal-integrability derivative required by Dolgopyat theory; and the stated local-limit normalization is inconsistent with its own window scaling.

## Major mathematical objections

### 1. A uniform right inverse cannot survive a vanishing birth current

Near a birth, the paper obtains a physical paired current

\[
\mathcal I_R=2(R-R_0)T_2+O((R-R_0)^2).
\]

Thus the realization of the corresponding nonzero ambient coordinate tends to zero in the physical distribution norm as \(R\to R_0\). Any right inverse from the physical current range back to an ambient coordinate of order one must therefore have norm at least \(c|R-R_0|^{-1}\). It cannot be uniformly bounded across the birth.

The proof tries to avoid this by choosing the least continuation label and an \(\ell^2\) tail projection. That only chooses a representative; it does not change the smallest singular value of the realization map. The claim

\[
\mathbb B_R^{(2)}=\ker E_R\oplus J_R(\operatorname{Ran}E_R)
\]

with a uniformly bounded \(J_R\) is therefore unsupported and, under the natural physical distribution norm, false at the parameter where the current vanishes. If the range is instead given the quotient norm by definition, the right-inverse statement becomes tautological and no longer proves uniform comparison with the physical billiard distribution space.

The paper must construct a continuous field/quotient topology with explicit parameter estimates; it cannot obtain it from a finite-depth triangularity slogan.

### 2. The five periodic words are not an explicit uniform certificate

No five admissible billiard words are listed and no four-by-four determinant is computed. The proof says that a “local unstable slide” of a periodic loop changes the roof while preserving homology. Periodic points of a fixed hyperbolic billiard word are isolated; an unstable slide is not another periodic orbit with the same word. One may select different words, but then their admissibility and roof derivatives must be calculated.

The passage from local certificates on a finite cover of \(K\) to one global certificate is also invalid as written. Concatenating local words with marker words does not make the determinant of one selected four-by-four difference matrix uniformly nonzero over the entire parameter interval. Determinants may vanish away from the chart for which the words were chosen. A finite family can give a frequency-dependent choice of certificate, but that is a different theorem and must be incorporated into the Fourier/Dolgopyat construction.

### 3. Periodic aperiodicity does not imply the Dolgopyat derivative estimate

The five-word determinant, even if valid, rules out an exact coboundary/peripheral eigenfunction. It does not imply that, for every large frequency, two inverse branches have a phase difference whose derivative crosses an interval containing \(\pi\). That is a uniform nonintegrability/UNI statement involving derivatives of temporal distance along a common interval.

The proof of Theorem r7-a2-dolgopyat simply asserts this implication:

> “The five-word certificate provides ... a returned branch pair whose phase difference crosses an interval containing \(\pi\).”

No such result follows from periodic sums. Aperiodicity controls compact nonzero frequencies; high-frequency Dolgopyat cancellation requires a separately constructed branch pair, distortion estimates, cone invariance, nonconcentration, and a quantified return theorem. Those are precisely the missing model-specific theorem.

### 4. The roof-window normalization is dimensionally inconsistent

The paper declares the regimes

\[
G_n=O(n^{-1/2}),\qquad n^{-1/2}\ll G_n\ll1,
\qquad G_n\ge G_0>0.
\]

These are regimes for a window in the normalized roof average \(T_n/n\). The corresponding interval for the sum \(T_n\) has length \(nG_n\). A joint two-lattice/one-continuous local density is of order \(n^{-3/2}\); integrating it over the roof-sum interval gives order

\[
nG_n\,n^{-3/2}=G_n n^{-1/2},
\]

with the two-dimensional lattice coefficient already included.

The displayed theorem instead multiplies \(n^{-3/2}\) by \(\operatorname{vol}(G_nB)\), giving \(G_n n^{-3/2}\), short by a factor \(n\). If \(G_n\) were intended as a window for the unnormalized sum, then the declared \(n^{-1/2}\), central, and fixed regimes would be the wrong regimes. The statement cannot be correct under either interpretation.

### 5. The spectral quotient theorem is largely an assertion

The proof does not establish common anisotropic spaces, bounded trace-jet multiplication, a uniform Lasota–Yorke inequality on the quotient, parameter differentiability of the quotient projection, or the claimed equality of physical and quotient spectra. In particular, a quotient can remove kernel eigenvectors, but it does not automatically remove generalized modes interacting with a nonuniform complement.

## Dependency assessment

A2 remains the first unresolved gate in the Sinai chain. A3 may not use its pressure, covariance, or high-frequency estimates as proved input; A4 and C2 consequently cannot treat the conditional path kernel or Doob data as established.

## Required reconstruction

The authors should construct one genuine physical anisotropic quotient with parameter-uniform norm equivalence, give explicit periodic/UNI branches with verified determinants and derivative separation, and state the vector–roof LLT in unambiguous sum or average variables with the correct scaling. Aperiodicity and Dolgopyat nonintegrability must be proved as separate results.

## Recommendation

**Reject.** The new architecture points in the right direction, but the quotient is not uniformly controlled, the high-frequency theorem is not derived, and the local-limit formula has a direct scaling error.
