# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `9eb3794fe0cb6a929d581ec38ef11d3019068d1f`

## Editorial summary

The revision makes two genuine advances over the preceding candidate. It no longer identifies a nonzero trace space with the zero space at a component birth, and it separates sharp local, central, and saturated roof-window regimes. Those are the correct repair directions.

The new ambient field, however, is not proved to represent the physical current bundle without spurious kernel spectrum. More decisively, the stated arithmetic certificate has a dimension/counting error and cannot establish joint aperiodicity. The Dolgopyat cancellation proof also uses a false elementary inequality. Hence the spectral packet and the master local-limit theorem remain unsupported.

## Major mathematical objections

### 1. The ambient realization is noninjective and its range is not proved closed

The map

\[
E_R:\mathbb B^{(2)}\to\mathscr D'(M_R)
\]

annihilates every coordinate whose geometric component is absent. It may also identify different continuation labels representing the same physical one-sided current. Thus `E_R` has a large parameter-dependent kernel.

The proof of `lem:r6-a2-ambient` says that closedness of the physical range follows from completeness of the ambient direct sum, continuity of finite-depth projections, and a vanishing tail. A continuous image of a Banach space need not be closed. The listed facts do not provide a lower bound on `E_R`, a complemented kernel, or a closed-range theorem.

This matters spectrally. An operator on the ambient space can possess eigenvalues and Jordan chains entirely in `ker E_R`. The intertwining identity

\[
E_R\mathbb L_R=L_RE_R
\]

only sends ambient physical classes to physical distributions; it does not imply that the leading spectrum of the lift equals the spectrum of the physical operator. One must pass to a Hausdorff quotient by the kernel, prove the quotient norm is well behaved and parameter coherent, or construct a complemented physical subbundle. None is done.

### 2. The claimed second-order birth/death amplitude is not a free choice

At a tangency or birth, the actual current carried by a new singular arc has the geometric Jacobian dictated by that arc. The manuscript says that one may multiply the fixed reference current by an incidence amplitude that vanishes to second order in `R` and thereby make the realization `C^2`.

That amplitude cannot be selected independently of the physical current. Typical saddle-node geometry has signed displacement of order `sqrt(R-R_0)` and arc length or current mass with the corresponding fractional scaling. Using the signed square-root as a coordinate regularizes dependence in the square-root parameter, not automatically in `R`. Multiplying by an extra square changes the represented distribution unless the ambient coefficient is simultaneously renormalized, in which case the coordinate norm becomes singular.

A valid construction must compute the exact current Jacobian through the birth and prove boundedness of the renormalized coordinate maps. The present proof merely declares the desired order of vanishing.

### 3. The arithmetic certificate is dimensionally inconsistent

The manuscript defines

\[
\mathbf c_R(v)=\bigl(S\kappa_R(v),S\tau_R(v),|v|\bigr).
\]

Since `kappa_R` takes values in `Z^2`, this is a vector in four real dimensions, not three. The text then says that the three differences obtained from four periodic words “form a matrix whose determinant is bounded away from zero.” Three four-dimensional vectors do not have a determinant.

The underlying periodic-orbit equations also show the missing degree of freedom. If

\[
u\cdot\kappa_R-t\tau_R=c+U-U\circ T,
\]

then a periodic word of length `n` satisfies

\[
u\cdot S_n\kappa_R-tS_n\tau_R=nc.
\]

The unknown coefficients are `(u_1,u_2,t,c)`, four scalars. Four words provide only three independent difference equations. Unless all selected words have the same length, or a fifth independent word is supplied, those equations cannot force `(u,t)=0`. No equal-length condition or explicit word computation appears.

Therefore `lem:r6-a2-arithmetic` is unproved. Its conclusions—aperiodicity on compact minor arcs and positive joint covariance—cannot be used in the Dolgopyat or local-limit arguments.

### 4. The cancellation inequality in `lem:r6-a2-cancel` is false as stated

The proof invokes

\[
|z_1+z_2|^2\le(1-c)|z_1|^2+(1-c)|z_2|^2
\]

whenever the phase separation is merely bounded away from zero. Take `z_1=1` and `z_2=i`. Their phase separation is `pi/2`, but the left side equals `2` and the right side is `2(1-c)<2`.

A standard Dolgopyat argument needs a subinterval on which the phase is near opposition, control of the amplitude ratio, and a majorant inequality with a carefully reduced branch. None of those quantitative hypotheses is stated. The claim that alternating cutoffs and a returned mass automatically yield a fixed `L^2` loss is not a proof, especially on the added trace-jet sector.

### 5. The trace-jet Lasota–Yorke estimate is only schematic

The countable trace block includes births, tangencies, intersections, and derivatives through order two. The proof accounts for descendants by one geometric factor, but does not establish:

- the norm of incidence maps at multiple intersections;
- compatibility of normal jets under branch composition;
- compactness of finite-depth trace coordinates in the declared fractional spaces;
- absence of peripheral spectrum in the trace-only kernel; or
- uniform `C^2` parameter bounds through combinatorial changes.

The chosen weighted `ell^1` convention is also not checked against both the realization norm and child multiplicity. A condition such as `C_1 theta zeta<1` is not by itself the boundedness condition for a realization from a norm weighted by `zeta^d`; one needs the exact ratio between the physical current norm and the coordinate weight.

### 6. The master local-limit formula has an unresolved tilt convention

The formula is written under a fixed real tilted chart with mean `(a,b)`, but the probability under the original law is multiplied by

\[
e^{-nI(k_n/n,t_n/n)}
\]

and also by a Gaussian factor in `(k_n-na)/sqrt n`. If the tilt is fixed at `(a,b)`, the exact change-of-measure factor is the linear tilt exponent, not the full target-dependent rate. If the tilt is chosen at the target, the additional Gaussian displacement factor must be recomputed. As written, the theorem risks counting the same quadratic deviation twice.

The proof does not state which saddle is used, how `I` is normalized for a window rather than a point, or how the sharp-interval smoothing error is controlled without invoking the local estimate being proved.

## Dependency consequences

A3 uses the A2 ambient transfer estimate, singularity shield, survivor spectral inputs, and cylinder insertions. A4 uses the A2 spectral gap, high-frequency resolvent, and conditional finite-block estimates. C2 and D1 then inherit those statements. Until the quotient/aperiodicity/Dolgopyat issues above are repaired, no downstream theorem may cite A2 as a closed interface.

## Required reconstruction

A viable proof must:

1. construct a quotient or complemented physical trace bundle and eliminate spurious ambient spectrum;
2. compute actual birth/death current scaling rather than assigning an arbitrary amplitude;
3. give explicit periodic words with enough independent equations to remove the coboundary constant;
4. supply a correct Dolgopyat branch-pairing inequality and full cone estimates; and
5. state one unambiguous saddle convention for the Fourier/local-limit theorem, with absolute and relative errors proved separately.

## Recommendation

**Reject.** The revision correctly recognizes the previous bundle and wide-window errors, but its replacement spectral theorem is not established. The arithmetic certificate is dimensionally invalid, the cancellation lemma contains a false inequality, and the ambient lift is not shown to have the physical spectrum. The advertised vector–roof pressure packet therefore remains unproved.