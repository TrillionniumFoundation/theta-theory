# A2 v39 proof ledger

This ledger describes the active article in [main.tex](main.tex).
The preservation baseline is the v38 author source at
`a346669928e5147cf2c0ef86c3bc2a455b512d14`; the controlling report is
the v38 review at `5dd7a7e346a9d31d7541efe791335d4e965cadb0`.
The ledger records proof content and its hypotheses, not an independent
formal certification of the article.

## 1. New exact chain

| Result | Input and conclusion | Proof mechanism |
|---|---|---|
| Lemma 2.1, `lem:single-boundary-flux` | One unknown stationary density and deterministic short forward flights give an \(L^1_{\rm loc}\) boundary-flux germ. | Exact strip disintegration, translation continuity in \(L^1\), local finiteness and a weak error bounded by \(t\|\nabla\psi\|_\infty/2\) times the relevant widths. |
| Lemma 2.2, `lem:single-angular-resolution` | Angular filtering of the germ gives a positive sum of weighted reflected translates of the density. | The unit-mass identity \(k''+k=\delta_{\pi/2}+\delta_{-\pi/2}\), followed by continuity of translations in \(L^1\). |
| Theorem 2.3, `thm:single-law-rigidity` | A uniform angular-copy gap identifies the centered footprint, the entire centered density and all centered obstacles. | Separate the supports; read each mass and Steiner point; normalize one density copy; take the union of the boundary contact centers over angles and its connected components. |
| Corollary 2.4, `cor:single-law-fiber` | The common translation is exactly the full observational ambiguity. | Equality of the canonical triples gives one direction; translating the launch law and table together couples every forward bit for the converse. |
| Corollary 2.5, `cor:single-germ-periods` | The germ determines all finite-length responses and has exactly the obstacle translation-period group. | Reconstruct the table and law; use translation equivariance and discreteness of the separated obstacle stabilizer. Rank two is equivalent to a finite-orbit crystal. |
| Theorem 2.6, `thm:single-resolved-obstacle` | Exact recovery needs only \(\operatorname{diam}A\le\Delta<d\) and one obstacle of diameter greater than \(\Delta\). | A minimum-area angular support component is a single density copy; the odd germ gives \(\nabla v\); the unique bounded continuous potential with infimum zero recovers occupation; support subtraction recovers every obstacle. |

The new exact sources are
`core/19_single_law_rigidity.tex` and
`core/19a_one_resolved_component.tex`. Their six proof environments
are self-contained apart from the experiment's definitions and basic
convex-geometric facts stated in the proofs.

### Normalizations and measure-theoretic points

The forward flux uses \((-n\cdot n_\theta)_+\), with the negative
normal sign appropriate to entering an obstacle. There is no extra
factor of two or \(2\pi\) in the density-copy identity. The density
copy supported on \(K=c-A\) has mass equal to the curvature radius
at \(c\). With \(k=s(K)\),

\[
A_0=-(K-k),\qquad
j_0(z)=\frac{S_{\theta,K}(k-z)}{\int_K S_\theta(x)\,dx},
\qquad j_0(z)=j(z+s(A)).
\]

Supports are supports of positive measures. Positivity almost
everywhere in the footprint interior identifies its support even
when a representative of the density vanishes on a dense null set.
Density equality is almost-everywhere equality. Germ equality and
germ periods are defined in \(L^1_{\mathrm{loc}}\) for each angle.

Theorem 2.6 uses a minimum which is attained by at least one isolated
copy, not compactness of an infinite set of obstacle labels. A union
of two distinct translates of a convex body with nonempty interior
has strictly larger area than one copy. A diameter pair of the
resolved smooth obstacle has antipodal normals and gives the
required separated copies. The relation
\(q_\theta-q_{\theta+\pi}=\partial_{n_\theta}v\) is distributional;
the proof does not restrict an arbitrary \(L^1\) function to a
prescribed line. Separation of the expanded components guarantees
\(\inf v=0\), fixing the additive constant.

## 2. New finite chain

All four results are in `core/20_single_law_finite.tex`. They use
the quantitative uniform-copy-gap hypotheses stated there, including
the boundary-mass lower bound
\(j\ge b_0\operatorname{dist}(\cdot,\partial A)^\gamma\) almost
everywhere, and quantitative \(C^s\) support and curvature bounds.
They do not assume a density upper bound or modulus of continuity.

| Result | Conclusion | Principal estimates |
|---|---|---|
| Lemma 3.1, `lem:single-weak-sampling` | A finite rational forward experiment estimates each smoothed angular response. | Positive spatial-kernel importance sampling, signed angular weights, four deterministic biases and a Bernstein variance bound. |
| Lemma 3.2, `lem:single-finite-copies` | A finite threshold field yields all complete separated footprint copies to Hausdorff error \(O(e)\). | Positive regularization, inner mass of order \(e^\gamma\), a support collar of order \(e\), and a graph at a fixed fraction of the copy gap. |
| Theorem 3.3, `thm:single-law-finite` | Finite forward-only recovery of centered footprint and periodic table in \(C^2\), with correct primitive data and explicit resources. | Complete-copy aperture rule, Steiner centers, a second component graph, quadratic angular support error, signed high-order support smoothing and the retained period-locking construction. |
| Corollary 3.4, `cor:single-finite-cloud` | The same finite geometric recovery for a complete bounded nonperiodic cloud. | The protected aperture makes all components complete; no period decision is performed. |

### Bias, variance and the exponent

For spatial scale \(r\), angular smoothing scale \(b\), command
length \(t\), spatial mesh \(\ell\), angular quadrature mesh
\(d_\theta\), and command rounding \(\zeta\), the four bias terms
are bounded by a constant times

\[
t r^{-3}b^{-2}
+\frac{\ell r^{-2}b^{-2}}{t}
+d_\theta r^{-2}b^{-3}
+\frac{\zeta r^{-2}b^{-2}}{t}.
\]

The estimator has absolute bound \(Ct^{-1}b^{-2}\) and variance
at most \(Ct^{-1}r^{-2}b^{-4}\). The latter uses a spatially
averaged collision probability bounded by \(Ctr^{-2}\); it does
not assume the generally unavailable pointwise bound \(F_t\le Ct\).
Spatial and displacement quadrature errors are proved after
conditioning on the hidden launch displacement and estimating the
area of cells meeting the collision-strip boundary. Integration
against the density then uses its unit mass only.

For geometric support error \(e\), choose

\[
r,b\asymp e,\quad t\asymp e^{\gamma+5},\quad
\ell,\zeta\asymp e^{2\gamma+9},\quad
d_\theta\asymp e^{\gamma+5}.
\]

The estimation threshold is of order \(e^\gamma\). Each target
costs \(O(e^{-(3\gamma+11)}\log(C/\varepsilon))\) attempted
bits. There are \(O(e^{-2})\) spatial targets and
\(O(e^{-1/2})\) target angles. The angular count follows from

\[
0\le h_C(\phi)-c_C(\psi)\cdot n_\phi
\le r_C^+(1-\cos|\phi-\psi|),
\]

so angular spacing \(\sqrt e\) gives support error \(O(e)\).
With \(e\asymp\nu^{s/(s-2)}\), the total bound is

\[
N_\nu\le C\nu^{-(3\gamma+27/2)s/(s-2)}
\log\frac{C}{\nu\delta}.
\]

Every sampled center-and-vector pair is counted as an occurrence,
giving \(S_\nu\le J_\nu\le N_\nu\). The aperture paragraph
distinguishes nominal centers from actual displaced launches. The
finite smooth representation uses support smoothing followed by
finite smooth interpolation; the curvature reserve ensures a valid
strictly convex output. The period-margin argument is applied to
the reconstructed canonical table.

This is a sufficient rate for joint unknown-law geometric recovery.
The finite theorem does not claim a uniform strong-norm estimate of
an arbitrary \(L^1\) density, or an optimal exponent for this
unknown-law class.

## 3. Retained proof packages and dependencies

| Location | Complete retained content | Relationship to the new principal inverse |
|---|---|---|
| Section 4 | Effective collision-boundary estimate, adaptive information bound, shrinking-layer upper construction and matched known-disk polynomial minimax power | An unchanged quantitative benchmark for its fixed-law experiment |
| Appendix A | Global stopped-Poisson occupation inverse and exact period identity | An alternative pooled-data inverse; not used by the direct Theorem 2.3 |
| Appendix B | Killed stopping polytope, arbitrary-data stability, primal-dual certificates and pointwise finite occupation | A pointwise computational theorem; not a finite germ oracle |
| Appendix C | Stationary boundary and component queries with calibrated support | Retained auxiliary geometric and statistical tools |
| Appendix D | Joint table and homothetic footprint recovery with fixed origin | Retained alternative apparatus model |
| Appendix E | Rare pooled collisions and stationary boundary recovery | Supplies the retained fixed-law upper construction |
| Appendix F | Area/width calibration of an unknown homothety ratio | Retains its own raw/difference data distinctions |
| Appendix G | Unregistered homothetic launch supports and complete registration fiber | Retained multiple-setting inverse with unknown origins and ratios |
| Appendix H | General centered displacement laws and isotropic perimeter normalization | Retained exact response and scale results |
| Appendix I | Earlier fixed-common-density information lower bound | Preserved within its original comparator |
| Appendix J | Complete earlier theorem and resource summaries | Consolidates the inherited statements under their stated models |
| Appendices K–M | Localized occupation queries, adaptive boundary reconstruction and finite binary controls | Retained finite geometric constructions and control accounting |
| Appendix N | Period recognition from a reconstructed patch | Used by the new periodic finite theorem under the same positive margin |
| Appendices O–P | Physical packing, quotient gauge and sequential information | Retained lower-bound foundations |
| Appendix Q | Resolution converse for table-dependent bounded errors | Retained control-error model, distinct from one stationary density |

The exact direct chain is Lemma 2.1 → Lemma 2.2 → Theorem 2.3 →
Corollaries 2.4–2.5. Theorem 2.6 uses the same angular formula and
adds minimum-area selection and the odd occupation gradient. The
finite chain is Lemma 3.1 → Lemma 3.2 → Theorem 3.3, with support
smoothing and Appendix N for period locking. Corollary 3.4 uses
the geometric part without period locking.

## 4. Preservation contract

| Quantity | Reviewed v38 | Active v39 |
|---|---:|---:|
| TeX inputs, including primary and references | 29 | 34 |
| Core TeX inputs | 27 | 32 |
| Labels | 265 | 322 |
| Proof environments | 66 | 76 |
| Theorem, lemma, proposition and corollary blocks | 69 | 79 |

The validator reads the reviewed primary's actual recursive input
closure from the preserved v38 tree. It compares label multisets and
complete proof bodies with the current active closure. Every reviewed
proof body is retained byte-for-byte, and every reviewed label remains
active. Introductory prose, titles and navigation have been adjusted
to the new main-body/appendix organization. The historical manuscript
and review directories themselves are unchanged Git trees.

## 5. Finite diagnostics and source qualification

`tools/verify_v39.py` is self-contained and uses only the Python
standard library. It retains 606,502 v37 checks and all 1,796 v38
checks, including the 512 finite stopping policies. The 14,678 new
checks are divided as follows:

| New diagnostic group | Count | Finite content |
|---|---:|---|
| Angular kernel | 1,737 | Unit masses, angular shifts, Fourier identities and odd-flux sign |
| Density-copy geometry | 12,154 | Nonconstant-curvature supports, normalization, asymmetric densities, canonical centers and common translations |
| Flux and weak error | 616 | Exact rectangular strip models, gradient signs and the weak \(t/2\) coefficient |
| Regularization | 103 | Polynomial kernels, endpoint derivatives, integration by parts and signed Bernoulli estimators |
| Resource algebra | 68 | Bias scales, Bernstein powers, target counts, precision and angular support order |

The total is 622,976. The normal and optimized Python outputs must
be byte-identical. The frozen diagnostic source SHA-256 is
`ad344718100d4afea9d76e1b447898e1a8c20e79a7d4d26ffeb57120c0028751`;
its common JSON output SHA-256 is
`44990bf0956c28f8a0721c49d09c5d1911dc99ca2c61484e7d6643b3e67b78fb`.
The independent qualification-contract suite contains 66 tests.

Finite diagnostics exercise finite identities and models. They do
not prove the continuum support, regularity, identifiability or
statistical theorems. Those arguments are written in the article.
The exact-source validator additionally verifies committed bytes,
historical tree identities, active inputs, labels and citations,
ordinary/optimized agreement, the native primary build and the
binding of the PDF and source archives to the execution receipt.
