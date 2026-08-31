# Independent Referee Report — Round 12

**Manuscript:** D1 — *Deterministic Theta Contractions*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `c4d0d3f684bd713be5962dec1dc58b704f70e06e8affeb20a29e498ad38b167b`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject; remove as a standalone submission**

## Executive assessment

Round 12 correctly distinguishes normalized component pressure from unnormalized restricted pressure, retains an explicit remainder label, avoids double counting phase cost, and recognizes that labels must be defined on the original microscopic sample space.

Its proposed construction of those labels is mathematically false. Positivity of an operator does not imply positivity of each Riesz spectral projection. A two-by-two positive matrix gives an immediate counterexample. Therefore the functions \(E_{n,j}1\) need not be nonnegative, the ratios \(\chi_{n,j}\) need not be probabilities, and the advertised exact positive disintegration does not exist. The claim that a spectral remainder is superexponentially small also does not follow from a uniform annular gap. The subsequent component LDP, pressure minimum, shell mixture, and phase sheaf are consequently unsupported.

## Decisive objections

### 1. Positive operators need not have positive nonleading Riesz projections

The manuscript states:

> Positivity gives band projections \(E_{n,j}\ge0\).

This is false. Consider the strictly positive matrix

\[
A=
\begin{pmatrix}
2&1\\
1&2
\end{pmatrix}.
\]

Its eigenvalues are \(3\) and \(1\). The Riesz projection onto the eigenvalue \(1\) is

\[
E_1=rac12
\begin{pmatrix}
1&-1\\
-1&1
\end{pmatrix},
\]

which is not a positive operator: it has negative entries and sends positive vectors to signed vectors.

Perron–Frobenius positivity applies to the leading eigenvector/eigenfunctional of an irreducible positive operator. It does not make every peripheral or subleading spectral band projection positive.

### 2. The proposed label probabilities may be negative or undefined

The definitions

\[
\chi_{n,j}(x)
=
\frac{E_{n,j}1(x)}{\sum_kE_{n,k}1(x)+R_n1(x)}
\]

and

\[
\chi_{n,\partial}(x)
=
\frac{R_n1(x)}{\sum_kE_{n,k}1(x)+R_n1(x)}
\]

are probabilities only if every numerator is nonnegative and the denominator is positive. Neither follows from spectral projection theory. The complementary operator

\[
R_n=I-\sum_jE_{n,j}
\]

is not generally positive either.

Thus the first theorem's “exact positive disintegration” fails before any large-deviation argument begins.

### 3. A spectral band is not a microscopic latent event

Even if one had a positive leading eigenprojection, an operator spectral component is a decomposition of propagated functions or measures. It is not automatically a pointwise random label measurable with respect to the original microstate. Constructing a latent variable requires positive kernels or a genuine measurable partition/disintegration.

The manuscript converts operator bands into pointwise functions \(E_{n,j}1(x)\) without specifying the operator's state/function orientation, normalization, or relation to the physical finite-volume law. This is a category error between spectral decomposition and probabilistic mixture decomposition.

### 4. An annular spectral gap gives exponential, not superexponential, remainder

A uniform peripheral gap typically yields a remainder of order

\[
C\rho^n=e^{-cn},
\qquad 0<\rho<1.
\]

At LDP speed \(n\), this has finite rate \(c\). It is not superexponentially small. The theorem claims the \(\partial\)-weight is superexponential solely from the peripheral gap and compact containment. That conclusion is false unless a stronger, separately proved estimate is available.

The paper retains the \(\partial\) component in formulas, which is correct in principle, but it cannot then simultaneously discard it as superexponential in the component construction.

### 5. The platform papers do not construct the assumed positive band family

A2–A4 discuss simple leading eigenvalues on regular charts; B1–B4 discuss cluster pressures and kinetic semigroups. None proves that at coexistence there is a finite family of positive, uniformly separated peripheral band operators whose sum plus a positive remainder reconstructs the microscopic law.

The opening assumption therefore imports the exact phase decomposition that D1 claims to derive.

### 6. The component LDP does not follow from restricting to a Riesz range

The proof says that A3 or B2 Laplace principles apply “with the positive band as an additional finite state” and that recoveries can be conditioned on that state. A Riesz range is a linear subspace, not a finite-state event. There is no conditional probability law until the positive label construction has been completed—which it has not.

The component LDP, boundary recovery, and local coefficients are therefore circular.

### 7. The phase pressure formula is algebraically correct only after a genuine mixture exists

The formula

\[
Q(\theta)=
\max_j\{-\alpha_j+\widetilde Q_j(\theta)\}
\]

is correct for an actual finite positive mixture with normalized component laws. Round 12 does not construct such a mixture. Correcting the normalization from Round 10 does not repair the missing positive disintegration.

### 8. The phase sheaf has no established objects to continue

Analytic continuation of Riesz contours can track spectral subspaces, including signed ones. It does not turn them into positive probabilistic phase labels. Monodromy may also permute bands around excluded degeneracies, so a globally consistent sheaf requires more than “a band cannot cross another band.”

### 9. Every downstream commutation theorem is conditional on the false first theorem

Shell conditioning, Gaussian tangent formation, and dynamic semigroup summation commute over a finite positive mixture once such a mixture and uniform component limits are proved. Here they are generic finite-sum identities placed after an invalid spectral-to-probability conversion.

The paper adds no independent theorem capable of closing A3/B2 component LDPs or their coexistence interfaces.

## Genuine improvements recognized

The following Round 12 principles are correct and should be retained elsewhere:

- component pressures must be normalized before phase costs are added;
- an overlap/remainder cannot be silently discarded;
- labels must be common to all observable projections;
- contraction of a finite labelled LDP gives a nonconvex pointwise minimum; and
- coexistence tangents depend on actual finite-volume weights.

## Required reconstruction

A viable phase theorem must begin with a genuine positive microscopic decomposition: measurable basins with controlled boundaries, metastable committor kernels, or positive reducible blocks whose kernels are proved to form a Markov partition. Spectral projections alone are insufficient. Component LDPs and local coefficients must then be proved under those actual conditional laws.

This material should be incorporated as a phase-mixture section of whichever platform paper constructs the decomposition.

## Recommendation

**Reject; remove as a standalone submission.** The canonical phase labels are built from spectral projections that need not be positive. The exact mixture, component LDP, pressure formula application, and all commutation claims therefore lack a probabilistic foundation.