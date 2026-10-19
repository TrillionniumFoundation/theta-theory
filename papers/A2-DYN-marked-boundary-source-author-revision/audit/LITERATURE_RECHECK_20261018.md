# Primary theorem recheck and native hypothesis map

## Status and provenance

This document restores the substantive author-side literature checks made in this iteration. After workspace maintenance its wording was reconstructed from the retained source-specific verification notes; the former document SHA-256 was 5f892ff1874b5df2d556cf77a7da609b18f4f3ab86c3681449c564d6a9a07650. Byte identity with that former serialization is not claimed. This is not a new referee report and does not certify every historical imported theorem.

The primary PDFs actually inspected were:

- Demers--Zhang, A functional analytic approach to perturbations of the Lorentz gas: https://arxiv.org/pdf/1210.1261
- Baladi--Demers, Thermodynamic formalism for dispersing billiards: https://arxiv.org/pdf/2009.10936
- Dolgopyat--Nandori, On mixing and the local central limit theorem for hyperbolic flows: https://arxiv.org/pdf/1710.08568

The bibliography census separately enumerates all 25 external works in the recovered source. Three direct primary-paper checks do not independently recertify the other 22 works or every use of these three papers.

## Demers--Zhang: actual source curves and perturbation spaces

The checked short-curve result is Lemma 3.2(b), with its H2--H4 geometric/expansion/distortion hypotheses. In the inspected PDF the relevant proof is on printed page 12 (PDF page index 11); historical page-14 locators belong to another pagination and must not be treated as a theorem identity.

The local unstable/stable curve-growth lemma concerns actual curves in the specified class and their singularity/homogeneity decomposition. It requires controlled curvature, the appropriate one-step expansion/summability, and distortion. It is not a theorem for arbitrary angular images solely because they are curves.

Native modules 281--283 supply the actual angular-source parametrization and its curvature, short-curve growth and distortion comparisons needed for this specific application. This is a substantive hypothesis match already achieved in the native chain; it should be inherited rather than repackaged as a new result in 304--309.

The anisotropic strong/weak spaces and perturbation statements in Theorems 2.2--2.6 are distinct objects. In particular a changing-radius family needs the coordinate identification indicated by Remark 2.7(b), the actual operator discrepancy bounds, and the specified Banach-space norms. The short-curve match alone does not prove uniform physical-cylinder pressure with all optical multipliers and pairing coefficients.

Status: the specified actual-curve import is matched by the retained native proof. The full physical-word pressure input, all radius-uniform operator norms, and every historical spectral use are not independently reconstructed by checking this lemma.

## Baladi--Demers: strong finite horizon is satisfied, pressure adaptation is separate

The finite-horizon convention in Section 1.1 excludes a straight trajectory that avoids all disk interiors while making only tangencies. This is stronger than merely assigning a uniform roof to almost every regular collision state. It is relevant to the singularity geometry used in Proposition 5.2 and cannot be silently ignored.

For the original triangular radius family this geometric issue is genuinely resolved by the native proofs. Module 287 proves the deterministic horizon

tau_max <= sqrt(3847/124) < 28/5.

The entire ratio 3847/124 lies under the square root. The alternative expression sqrt(3847)/124 is a transcription error and is not used.

More directly, the buffer lemma in module 294 proves that every point and direction, on an actual straight segment of length 28/5, has a lattice center at transverse distance strictly less than 179/400<R_-. Thus an infinite straight line avoiding all open disks, including an all-tangent line, is impossible. The statement covers every point and every direction and is not inferred from finitely many sampled trajectories.

This discharges the strong horizon geometry for the relevant theorem family. It does not discharge all remaining pressure hypotheses. The geometric potential, its pressure interval, and the strict gap Lambda^{-t}<exp(P(t)) must be matched to the particular imported theorem. Uniformity on a compact parameter interval in the potential is not automatically uniformity over the scatterer radius. The actual weighted partition/cylinder object and its relation to the native physical stable-arclength and optical weights also require a separate comparison.

Status: no-all-tangent geometry is verified natively. Complete partition-object adaptation, the pressure gap on the exact required parameter range, and radius-uniform constants are separate retained analytic obligations. Saying only that finite horizon is unverified would incorrectly reopen a solved native lemma; saying that finite horizon proves all pressure input would be equally incorrect.

## Dolgopyat--Nandori: tested local limits and arithmetic object

Definition 2.2 uses the actual measurable observable/cohomological decomposition, its closed subgroup and translation, regularity and integrability requirements, and a positive-definite covariance condition. The checked statement has tested observables/endpoints and a compact scaled fluctuation range. Its arithmetic cases depend on the minimal cohomological group of the actual observable.

Remark 2.5 permits suitable null-boundary indicator tests within the stated tested formulation. It does not supply raw essential roof height, nor a collision-dependent microscopic conditioning event of arbitrary width. Proposition 6.3 treats the finite-horizon Sinai billiard specialization and the corresponding arithmetic cases; one must match the actual roof/observable group and minimality hypothesis rather than transfer a scalar nonarithmetic conclusion to a four-mark observable without proof.

The source's marked return, displacement and collision observables have an inherited exact arithmetic chain. Its occupation convention, lattice labels, section conditioning and covariance calculations remain part of that chain. None is supplied merely by citing a flow local-limit theorem.

Status: the primary theorem object's test class, probability topology and arithmetic hypotheses were checked. It cannot be used to exchange unproved limits, insert changing microscopic windows into a fixed-window theorem, remove exact endpoint conditioning, or replace the full raw four-coordinate inversion estimate.

## Application to the current new proofs

The complete elementary variational, strip, common-minimum, clock, collar and positive-source proofs in 304--309 use no new external theorem. Their deterministic estimates and original-source mass bounds are native arguments. The normalized roof-height statements in 306 and 309 explicitly invoke native Input v112-geometric-pressure and its original one-copy optical/roof domination; the literature checks above do not convert that input into an unconditional result.

The exact stable-curve growth lemma and strong horizon condition already proved in the native chain should be retained as solved. The complete physical-word pressure, singular-interface and pairing reconstruction still needs its own proof at the actual norms and quantifiers. A successful finite script or manuscript compilation is not an external theorem-hypothesis verification.

