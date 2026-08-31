# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — Microcanonical Preparation  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `f9c8b97e6362e211e2df5e1ef55d135c0a191714`

## Executive assessment

The manuscript has finally adopted the correct source-dependent finite saddle, distinguishes normalized from extensive shell variables, acknowledges the one-particle momentum–energy paraboloid, and retains the low-particle/empty Poisson sectors. These are substantive improvements.

The new smoothing theorem still does not follow. A full-rank coarea patch gives only an absolutely continuous component of a convolution, not a globally smooth convolution law. The remaining singular component has non-negligible mass and destroys the claimed high-frequency bound. The rank assumptions on the additional constraints are unstated, and the covariance proof incorrectly extracts an order-one lower bound from an exponentially rare fixed-particle sector.

## Major mathematical objections

### 1. A local full-rank patch does not make the whole convolution smooth

Lemma r7-b1-rank finds one open product patch on which the differential of the mark-sum map has full rank. Coarea then gives an absolutely continuous component of the pushforward of the restricted measure. It does not imply that the complete convolution \(
u_1^{*n_0}\) is absolutely continuous, much less \(C^4\).

The complement of the patch has positive probability independent of \(\mu_arepsilon\). Its pushforward may retain singular components or critical-value singularities. The proof itself shifts language from “has a density” in the theorem to “has an absolutely continuous component” in the proof. These are not equivalent.

The high-frequency argument then groups the first \(n_*\) marks and applies integration by parts as though their entire convolution possessed a smooth density. The singular remainder need not decay in Fourier space. Unlike the low Poisson sectors, it is not exponentially small. Thus Theorem r7-b1-characteristic does not follow.

### 2. The rank theorem is false for the stated general constraint family

The continuous mark includes arbitrary functions

\[
\chi_1,\ldots,\chi_d.
\]

No independence or transversality hypothesis is stated. If, for example, \(\chi_1\equiv0\), or \(\chi_1\) is a linear combination of momentum and energy, the differential of the summed mark can never have rank \(4+d\), for any particle number. The phrase “assumed activity patches” refers to an assumption that is absent from the theorem.

Even for the momentum–energy block, the proof says that radial variations near \(\pm ae_1,\pm be_2\) span three momentum directions and energy. Radial directions in that configuration span at most the \(e_1,e_2\) momentum plane plus energy; no \(e_3\) direction is produced. A correct full-rank argument is possible with general velocity variations, but it is not the argument written.

### 3. Further convolution does not automatically raise regularity to arbitrary order

Once a measure has one absolutely continuous component, convolving with additional copies does not eliminate a singular component that persists from the complement of the full-rank patch. Nor does a single nonzero Jacobian minor provide the uniform global derivative bounds claimed on the saddle chart. To obtain arbitrary Fourier decay, the authors need either:

- a convolution power whose entire law has a globally controlled Sobolev density; or
- a decomposition in which every nonsmooth sector has exponentially small total mass.

Neither is proved.

### 4. The covariance proof uses an exponentially rare sector

The proof of the Hessian lower bound conditions on an \(n_0\)-particle product patch and says its “Poisson probability per unit activity is bounded below.” Under a compound Poisson law with mean of order \(\mu_arepsilon\), the event of exactly \(n_0\) particles has probability

\[
e^{-c\mu_arepsilon}\mu_arepsilon^{n_0}/n_0!,
\]

which is exponentially small. It cannot yield an order-one lower bound for

\[
D_{\lambda\lambda}^2Q_arepsilon
=\mu_arepsilon^{-1}\operatorname{Cov}(C_{m tot}).
\]

A covariance lower bound should instead be derived from the typical \(O(\mu_arepsilon)\)-particle compound process and the affine span of the one-particle mark. The current proof does not do so.

### 5. The shell coefficient depends on the unproved characteristic theorem

The central Gaussian calculation at the exact saddle is plausible, and the extensive shell scaling is now correctly typed. But the minor-arc and large-frequency error estimates rely precisely on the invalid global smoothing assertion above. The coefficient theorem, uniform ensemble transfer, and prepared LDP therefore remain unproved.

### 6. The hard-sphere dynamic source input is still conditional on B2

All uniform source derivatives and the connected remainder estimates are imported from B2-GC. Since B2's marked deterministic expansion remains open, B1 cannot use it as a completed analytic pressure theorem.

## Required reconstruction

State explicit linear-independence/transversality hypotheses for every added constraint. Prove a global mixed lattice/nonlattice local limit theorem for the actual compound law, with a rigorous decomposition of all singular sectors and uniform Sobolev bounds for the smooth part. Derive covariance from typical compound activity rather than a fixed rare sector, and only then perform the exact-saddle coefficient extraction.

## Recommendation

**Reject.** The finite-saddle architecture is now correct, but the smoothing and high-frequency theorem—the central new ingredient—confuses a local absolutely continuous component with a globally smooth convolution law.
