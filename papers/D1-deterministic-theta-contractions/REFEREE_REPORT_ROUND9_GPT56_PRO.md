# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/D1_EXACT_PHASE_LABEL_MIXTURE.tex`  
**Reviewed source SHA-256:** `bc82650fecde44acaa42a070764410d0e5ba4ed54be76ea24feb1ef4eed9110c`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

Round nine correctly recognizes that phase coexistence must be represented by an actual label before taking a physical contraction, that exponentially small remainders can affect a full LDP, and that local likelihoods should be centered at the exact finite-volume mean.

The paper does not construct such an exact labelled decomposition for either physical platform. It assumes phase laws, conditional LDPs, face recovery, uniform thin-shell coefficients, topology upgrades, and Gaussian limits—the entire content of the preceding series—and then applies standard disintegration and contraction identities. For hard-sphere “exposed phases,” the proposed labels are tilted measures, not latent components of the original physical law, so mixing them generally defines a new law.

## Major objections

### 1. The exact labelled physical law is not supplied by the platform papers

The theorem begins with genuine normalized laws \(\mathbb P_{\varepsilon,\alpha}\) and defines
\[
 \overline{\mathbb P}_\varepsilon(d\alpha,dx)
 =\rho_\varepsilon(d\alpha)\mathbb P_{\varepsilon,\alpha}(dx),
\]
declaring the physical law to be its projection.

This is an assumption, not a decomposition proved in A3 or B1/B2. A family of exponential tilts or exposed kinetic phases is not a partition/disintegration of one original law. Mixing those tilted laws with an arbitrary prior changes the physical measure.

For metastable boundary conditions, different \(\alpha\) may even correspond to different finite-volume models. An exact common-space mixture requires explicit latent events or phase projectors and a proof that their weighted sum equals the original law.

### 2. The joint LDP theorem assumes all difficult lower bounds

The hypotheses require, uniformly in the label:

- a good conditional LDP;
- boundary-face recovery;
- exponential tightness;
- local lower bounds; and
- regularity of \(I_\alpha(x)\).

These are precisely the unresolved A3 and B2 theorems. The proof by finite covering is standard once they are assumed; it is not a closure theorem for the series.

### 3. The prior hypothesis is ambiguous and insufficient

The prior is said to satisfy an LDP with rate \(J\) and also to have neighborhood masses “bounded below by \(e^{-o(\mu)}\)” on compact label sets. At labels with \(J(\alpha)>0\), an LDP gives mass of order \(e^{-\mu J(\alpha)}\), not subexponential mass. The intended lower bound must include the \(J\)-cost and be uniform in neighborhood size.

For a continuous label space, Laplace lower bounds also require continuity/exponential regularity of the conditional laws in \(\alpha\), not merely pointwise conditional LDPs.

### 4. The fixed-phase analytic chart is an imported assumption

The existence of a normalized positive phase law with a zero-free complex transfer/cluster chart is not proved for the phase labels introduced here. At coexistence, defining a restricted partition function requires actual boundary conditions or spectral projectors with positivity. D1 cannot create these objects by labelling them.

### 5. The topology-upgrade theorem assumes the desired recovery property

The strong-topology lower bound is obtained by assuming every finite-rate point has a recovery law exponentially concentrated in one compact weighted sublevel. This is the difficult exponential-goodness theorem. Projective Dawson–Gärtner alone does not supply it.

### 6. The thin-shell formula is conditional on unproved uniform coefficients

The exact integral over labels is algebraically correct if every labelled phase has a uniform A2/B1 coefficient. Those coefficients are not established. The formula also requires uniform control near phase-boundary labels, where saddles and Hessians may degenerate.

### 7. The “commutation principle” is tautological after all inputs are assumed

Disintegration, contraction of a label, and conditional application of a local Gaussian likelihood are standard identities. The final theorem adds no new mathematical mechanism capable of repairing an upstream gap.

### 8. The manuscript title and scope remain misleading

The paper is presented as a rigidity/universal-contraction theorem for hard-sphere cotangents. Its actual result is an abstract conditional statement about an exact mixture model. It neither proves rigidity nor constructs the phase decomposition for hard spheres.

## Dependency assessment

D1 sits at the end of every unresolved chain. It cannot be used as evidence that the series is closed. Its valid identities belong as a short labelled-mixture appendix to a future principal platform paper after the component laws have been constructed.

## Required reconstruction

To justify a standalone theorem, the authors would need a genuinely new phase-decomposition result: positive finite-volume component measures on a common space, exact reconstruction of the physical law, uniform component LDPs, and a nontrivial commutation theorem not reducible to ordinary contraction. Nothing of that scale is proved here.

## Recommendation

**Reject; remove as a standalone submission.** The manuscript assumes the complete platform theory and then applies standard mixture and contraction formulas. The exact label decomposition on which it rests is not constructed for the physical models.
