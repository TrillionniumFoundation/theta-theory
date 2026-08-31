# Independent Referee Report — Round 12

**Manuscript:** B1 — *Microcanonical Preparation*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `dada73a7333ec4a9ecebbaddb0b2f0e09a17f6ad6bcd87adff03e43284e23b41`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject without invitation to revise in the present architecture**

## Executive assessment

Round 12 retains the correct source-dependent finite saddle, restricts targets to a relative-interior chart, and imposes a regular shell class with a relative Gaussian mass lower bound. Those changes repair important earlier defects.

The new full-frequency theorem is nevertheless directly false even for the singleton compound-Poisson model on which its proof is based. A compound-Poisson law has a zero-particle atom. Its characteristic function approaches a nonzero constant of order \(e^{-c\mu_\varepsilon}\) as the continuous frequency tends to infinity. It cannot be bounded by

\[
e^{-c\mu_\varepsilon}(1+|u|)^{-s\mu_\varepsilon},
\]

which tends to zero. Equivalently, the scaled pressure gap tends to a finite negative constant; it cannot acquire an additional \(-C\log|u|\) term. The Fourier-tail argument for the sharp shell coefficient therefore collapses.

## Decisive objections

### 1. The claimed speed-dependent power tail contradicts the compound-Poisson formula

Let the singleton mark law have activity \(a>0\) and characteristic function \(\widehat\nu(u)\). For the compound-Poisson sector,

\[
\mathbb E e^{iuY}
=
\exp\{\mu_\varepsilon a(\widehat\nu(u)-1)\}.
\]

If the mark has a smooth integrable density, then by Riemann–Lebesgue,

\[
\widehat\nu(u)\longrightarrow0
\qquad(|u|\to\infty).
\]

Hence

\[
\left|\mathbb E e^{iuY}\right|
\longrightarrow e^{-a\mu_\varepsilon}>0.
\]

This is exactly the mass of the empty configuration. The Round 12 bound

\[
|\varphi_\varepsilon(t,u)|
\le e^{-c\mu_\varepsilon}(1+|u|)^{-s\mu_\varepsilon}
\]

converges to zero as \(|u|\to\infty\), contradicting the explicit singleton law.

### 2. The pressure inequality has the same contradiction

For the singleton pressure,

\[
\Phi^{(1)}(u)=a(\widehat\nu(u)-1),
\]

so

\[
\Re\Phi^{(1)}(u)\longrightarrow-a.
\]

It cannot satisfy

\[
\Re\Phi^{(1)}(u)
\le -c-C_s\log(1+|u|),
\]

whose right-hand side tends to \(-\infty\).

The proof incorrectly turns polynomial decay of the *single-mark Fourier transform* into a logarithmic decay of the *compound-Poisson pressure*. The Fourier transform appears additively inside \(a(\widehat\nu-1)\); it is not exponentiated once for each of \(\mu_\varepsilon\) independent deterministic blocks.

### 3. The connected polymer remainder cannot repair the empty-sector atom

The remainder is bounded by \(CT_*\) on the complex chart. A bounded analytic correction cannot create the missing \(-\log|u|\) divergence. The full grand-canonical law still contains the exact empty configuration with positive probability, and more generally low-particle sectors remain exponentially small but nonzero.

One may isolate those sectors and exploit cancellation after exact number-coefficient extraction. The manuscript instead asserts a false pointwise absolute bound on the unreduced joint characteristic function.

### 4. The high-frequency Fourier inversion is therefore invalid

The proof of the shell theorem requires an integrable tail that is

\[
o\bigl(\mu_\varepsilon^{-1/2}\gamma(W_\varepsilon)\bigr).
\]

A frequency-independent tail of size \(e^{-c\mu_\varepsilon}\) is not integrable over \(u\in\mathbb R^{d-1}\). Exact integration over the number angle may cancel sectors with the wrong particle number, but that cancellation is not captured by the absolute bound used in the proof. The order of lattice coefficient extraction and continuous Fourier inversion must be reorganized.

### 5. The singleton covariance proof also suppresses the Poisson number direction

For a compound-Poisson pressure, the multiplier Hessian is the activity second moment

\[
\int C C^T\,d\nu,
\]

not simply the covariance of a normalized one-particle mark after subtracting one global mean. The number coordinate and its cross terms must be retained in the exact Hessian. Positivity may still hold under the affine-span hypothesis, but the displayed proof does not compute the finite-volume object it later inverts.

### 6. The complex aperiodicity argument is not uniform for the full dynamical source

The compact-annulus proof uses equality in the triangle inequality for the singleton integral. The actual pressure includes a path/contact tilt that correlates particles through their future collision histories. Bounding its connected part by \(CT_*\) can preserve a fixed singleton gap only on a quantitatively small time/source chart. The theorem states one uniform chart but supplies no constants showing that all annuli, multiplier boundaries, and source derivatives fit inside it.

### 7. The shell theorem depends on a false frequency theorem

The regular shell hypotheses are sensible, and the exact finite saddle is the correct center. But the claimed relative coefficient follows only after the false high-frequency estimate. Compilation and the internal hostile check merely confirm that the phrase “speed-dependent power” is present; they do not validate it.

### 8. The microcanonical transfer and all downstream uses remain blocked

The variational formula

\[
Q^{\rm mc,a}(H)=
Q(H,\lambda_{H,a})-\lambda_{H,a}\cdot a
-Q(0,\lambda_{0,a})+\lambda_{0,a}\cdot a
\]

is the correct candidate. It has not been derived from the primitive shell without a valid coefficient theorem. B2-MC, B3's prepared covariance, B4's initial contraction, C1's observation coefficient, and D1's shell mixture therefore cannot treat B1 as a closed interface.

## Genuine improvements recognized

The following Round 12 features should be retained:

- separate exact saddles for numerator and denominator;
- relative-interior target conditions;
- uniform finite-volume Hessian control as the right existence mechanism;
- a shell class with controlled boundary and non-superexponentially small Gaussian mass; and
- the source-dependent constrained pressure formula.

## Required reconstruction

A correct proof must perform exact-number coefficient extraction while explicitly isolating the finite low-particle sectors. It may then prove continuous-frequency decay for the coefficient of the target particle number rather than for the full compound-Poisson characteristic function. The full hard-sphere connected remainder must be controlled in that coefficient theorem, not merely bounded on a local pressure chart.

## Recommendation

**Reject without invitation to revise in the present architecture.** The main frequency theorem is contradicted by the empty-configuration atom of its own singleton model. The sharp shell coefficient and the microcanonical bridge are consequently unproved.