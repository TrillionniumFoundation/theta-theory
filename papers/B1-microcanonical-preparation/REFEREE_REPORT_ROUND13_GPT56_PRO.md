# Independent Referee Report — Round 13

**Manuscript:** B1 — *Microcanonical Preparation*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `7fc4061b3dfd8564feafe72507a4e209b6d12e3d045b8ce4e24054f9339f94c4`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Extracting the exact particle-number coefficient before performing continuous Fourier inversion is the correct response to the empty grand-canonical sector. Round 13 also retains separate source-dependent saddles and a declared regular shell class. These are genuine improvements.

The replacement Fourier theorem is still internally inconsistent. Its displayed high-frequency bound contains a term with only a fixed exponent `s+cN_0`, yet the theorem claims that the integral of that term is `o(N^{-1/2})`. With fixed `R`, `s`, and `N_0`, the integral is a positive constant independent of `N`. The proof informally replaces the exponent by `s+cN` on a “good-label sector,” but the graph dichotomy needed to do so is neither stated precisely nor true for the general canonical polymer monomials described. The exact-number coefficient expansion and the full-rank smoothing mechanism remain unproved.

## Decisive objections

### 1. The stated Fourier tail cannot have an `o(N^{-1/2})` integral

Part (iii) states

\[
 |\phi_{\varepsilon,N,H}(u)|
 \le C_s(1+|u|)^{-s-cN_0}
      +C_se^{-cN}(1+|u|)^{-s},
 \qquad |u|>R,
\]

where `N_0` is fixed. In continuous dimension `d_c`,

\[
 \int_{|u|>R}(1+|u|)^{-s-cN_0}\,du
\]

is a strictly positive finite number depending on `(R,s,N_0)` but not on `N`. It does not tend to zero, much less satisfy

\[
 o(N^{-1/2}).
\]

The second term is exponentially small, but the first is not. The sentence saying that its exponent “may be replaced by `s+cN` on the good-label sector” is not part of the displayed global bound. A sector decomposition must yield a global estimate of the form

\[
 C(1+|u|)^{-s-cN}+Ce^{-cN}(1+|u|)^{-s}
\]

before the asserted integral follows.

As written, the high-frequency region can dominate the claimed `N^{-1/2}` number coefficient, so the sharp shell theorem is not proved.

### 2. The dependency-graph dichotomy is not established

The proof asserts that every exact-`N` polymer monomial has either a linear number of conditionally independent smooth leaves or a linear number of “extra” bonds with exponentially small activity.

A long tree or chain can have only two graph-theoretic leaves and only the baseline number of bonds. More generally, conditioning on the rest of a trajectory polymer need not leave any single particle mark with a uniformly smooth full-rank density: path/contact sources and collision constraints couple its initial coordinates to the entire chronology.

One might instead extract a large independent set, a block matching, or a regeneration structure, but each requires a precise combinatorial lemma and a uniform conditional coarea estimate. None is stated. The proof cannot simply promote “exactly `N` labels” into `cN` independent integrations by parts.

### 3. Canonical coefficient extraction from the connected grand partition is a missing theorem

Cauchy's coefficient formula applied to

\[
 \exp\{\text{connected polymer series}\}
\]

with `N` proportional to `mu_epsilon` requires a uniform complex activity annulus, a unique saddle, nonvanishing of the partition function, tail control on the contour, and canonical cluster estimates uniform in density. Termwise coefficient extraction of a normally convergent grand-canonical series does not by itself yield a normally convergent canonical polymer expansion for extensive `N`.

The proof states these conclusions rather than deriving them. This is the principal bridge between B2's grand-canonical expansion and the claimed primitive shell.

### 4. The number coordinate is inconsistently typed after exact-number extraction

The constraint mark `C` includes the constant coordinate `1`, and the Hessian theorem claims a positive lower bound in the full constraint space. Under the exact-number canonical law, however, the number coordinate is deterministic and its covariance and all Hessian entries in that direction are zero.

The theorem can be true only for the pre-extraction grand-canonical pressure, while the Fourier theorem is stated under the post-extraction canonical law. The manuscript moves between these two pressures without giving distinct notation or proving the Schur relation between their Hessians. The activity saddle, the number multiplier, and the exact coefficient are therefore double-counted or left ambiguous.

### 5. The shell class is defined relative to an unspecified remainder

The assumption

\[
 \gamma_{H,a}(W_\varepsilon)\gg\mu_\varepsilon^{-K}
\]

is said to hold “after comparison with the explicit Fourier remainder,” but neither `K` nor a uniform remainder bound is stated. This makes the admissible shell class partly circular: a shell is admissible when it is larger than the error of the theorem that is being proved.

A sharp coefficient theorem must give explicit central, annular, and tail errors first, then state a checkable geometric/mass condition on `W_epsilon`.

### 6. The exact-number coefficient does not remove all singular high-frequency components automatically

Removing the zero-particle atom eliminates one obstruction. Fixed-`N` hard-sphere laws can still have singular or lower-dimensional sectors in the continuous constraint map, especially when the added macro observables are not transverse on every canonical polymer component. A full affine span on selected one-particle patches does not show that every non-exponentially-small canonical sector contains enough such patches.

The claimed high-frequency integration by parts requires exactly this typical-sector theorem, which is not supplied.

### 7. The microcanonical transfer remains dependent on B2

Even a corrected coefficient theorem applies to the full path/contact source only if B2 supplies a source-uniform complex grand-canonical pressure and canonical coefficient control. B2 does not prove its fixed-genealogy transversality or full LDP. Therefore the final transfer theorem cannot presently be used downstream.

## Genuine improvements recognized

The number-first strategy, separate numerator/denominator saddles, removal of the empty-sector bound, and the requirement of a regular shell with nonnegligible Gaussian mass are all correct architectural choices.

## Required reconstruction

The authors must prove a standalone canonical cluster/coefficient theorem. It should distinguish grand-canonical and exact-number Hessians, establish a rigorous typical smoothing-block lemma under the full dynamic source, and provide a global integrable Fourier bound whose integral is quantitatively smaller than the local main term.

## Recommendation

**Reject.** The old empty-sector contradiction is removed, but the replacement high-frequency theorem contains an immediate asymptotic contradiction and rests on an unproved canonical smoothing dichotomy. The primitive-shell coefficient and every downstream microcanonical claim remain open.
