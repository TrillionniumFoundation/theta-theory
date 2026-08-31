# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/A2_BLOWUP_UNI_DENSITY_LLT.tex`  
**Reviewed source SHA-256:** `58fd8b1572bad503540f44f47fd659581aea3743962ffb0f071f1747863d2834`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The revision makes three conceptually correct distinctions: a blow-up is preferable to identifying a vanishing birth coordinate with a fixed nonzero trace space; compact-frequency arithmetic is different from high-frequency temporal nonintegrability; and a density-level local limit theorem is the right route to genuinely small roof windows.

None of the three load-bearing theorems is proved for the announced billiard family. The blow-up bundle remains a formal local normal form, the periodic and UNI packets are asserted without a verified orbit construction, and the high-frequency bound stated in the paper does not yield the Fourier integrability used in the density theorem. The sharp-window corollary also exceeds the range of its density estimate.

## Major mathematical objections

### 1. The birth construction is not defined on both sides of the geometric birth

The newborn traces \(T_{r,+}\) and \(T_{r,-}\) exist only on the side of the parameter where the two branches are present. The manuscript writes
\[
 T_r^{\rm od}=|r|^{-1/2}(T_{r,+}-T_{r,-})
\]
and claims a uniform graph through \(r=0\), but it does not define the physical traces on the no-branch side or specify an extension whose realized distribution remains physical.

The connection
\[
 \nabla_r=\partial_r-\frac{\zeta}{2r}\partial_\zeta+\mathcal C_r
\]
is singular at \(r=0\). A Taylor expansion of formal trace coordinates does not prove that this is a bounded connection on the declared anisotropic spaces, nor that its iterates have uniform graph norms. The closed graph theorem cannot create a uniformly bounded inverse without first proving bounded-below estimates and completeness for the actual material graph.

### 2. The uniform moving-billiard spectral theorem is still only a proof sketch

Theorem `r9-a2-bundle` is the principal new billiard result. Its proof must construct the strong/weak spaces and verify, uniformly through moving singularities and births:

- one-step expansion and complexity estimates;
- distortion and homogeneity-strip bounds;
- compact embedding;
- multiplier estimates for vector and roof twists;
- bounded covariant derivatives;
- invariance of the physical graph; and
- exclusion of trace-only peripheral modes.

The paragraph supplied does not establish these facts. In particular, the claim that every trace diagonal block is “a restriction of the same physical operator” is not a spectral argument, and triangular off-diagonal structure does not exclude new peripheral Jordan chains without quantitative bounds.

### 3. The advertised arithmetic determinant is not computed

The remaining determinant is
\[
 (\tau_3-\tau_0)(n_4-n_0)-(\tau_4-\tau_0)(n_3-n_0).
\]
The assertion that triangular and rhombic loops have “different mean free lengths” does not imply that this determinant is nonzero. It is an affine-slope condition relative to \(w_0\), not simply inequality of \(\tau_3/n_3\) and \(\tau_4/n_4\).

No explicit orbit coordinates or length formulas are given, and there is no proof that the proposed winding, triangular, rhombic, and replacement polygonal orbits remain regular and admissible on the stated parameter charts. The finite-cover conclusion therefore has no established local certificates to cover with.

### 4. The UNI theorem is the missing geometric theorem, not a consequence of a picture

The proof assumes a symmetric reference orbit with two outgoing angles \(\pm\theta_R\), a uniform lower bound for \(|\sin\theta_R|\), common return branches, and an exponentially small derivative contribution from the common suffix. None of these is derived for the specified Lorentz family.

Periodic aperiodicity does not imply UNI. A complete proof would need actual returned inverse branches on one quotient interval, differentiable continuations in \(R\), distortion bounds, and a calculation of the temporal-distance derivative including all moving collision endpoints.

### 5. The stated Dolgopyat estimate does not supply an integrable Fourier tail

For fixed \(n\),
\[
 |b|^A\exp\!\left(-\frac{cn}{\log(2+|b|)}\right)
\]
behaves like \(|b|^A\) as \(|b|\to\infty\). It is not integrable. The proof of the density LLT says that “one further roof derivative” supplies an integrable tail. One integration by parts gives only a \(1/|b|\) factor, which is not integrable and does not overcome the polynomial loss \(|b|^A\).

The paper needs a separate very-high-frequency estimate with sufficiently many derivatives, a quantified frequency range depending on \(n\), and uniform bounds for all derivative insertions. These are absent.

### 6. The density theorem does not justify the entire sharp-window corollary

Theorem `r9-a2-density-llt` is uniform only for
\[
 |t-n\bar\tau_R|\le C\sqrt n
\]
with fixed \(C\). The corollary is stated for every \(G_n>0\), including “saturated” windows whose \(u\)-range
\[
 \sqrt n\,G_n B
\]
escapes every fixed central compact set. Integrating a pointwise central LLT over such a growing interval is not justified. Fixed average-width windows include macroscopically off-center roof values and require a large-deviation saddle varying across the window, not one central Gaussian density.

For very small windows the density route can in principle give a relative result, but only after the density and its uniform error have actually been proved.

### 7. The paper imports arbitrary cylinder insertions without a multiplier theorem

A fixed central path cylinder is not automatically a finite-rank bounded insertion on the moving blow-up bundle. The theorem must show how its one-sided traces and parameter derivatives act on the strong/weak scale. This is not addressed.

## Dependency assessment

A2 is the first gate in the Sinai chain. A3 cannot use the vector–roof coefficient theorem, singularity control, or spectral differentiability until A2 supplies a genuine model-specific proof. A4 and C2 inherit the same obstruction.

## Minimum viable reconstruction

The strongest viable submission would isolate one theorem: a parameter-uniform vector/roof spectral and local-limit theorem for a precisely specified finite-horizon Lorentz family. It would include explicit orbit certificates, a full UNI/Dolgopyat proof, and a density LLT with rigorously separated frequency ranges. The projective and downstream superstructure should be deferred.

## Recommendation

**Reject.** The revision identifies the right interfaces but still states the entire billiard analysis in several paragraphs. The high-frequency estimate as written is insufficient for the density inversion, and the sharp-window conclusion exceeds the proved central range.
