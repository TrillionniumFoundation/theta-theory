# Literature audit — A2 v40

This audit records primary sources consulted on 4 October 2026 and separates classical machinery from the collision-specific inverse. It addresses the new two-field identification and finite law-and-prediction results, while retaining the scope distinctions of the reviewed angular-germ programme. The cited comparisons support attribution and the formulation of the result; they do not constitute an exhaustive priority claim.

## 1. Support functions and signed curvature measures

**Y. Martinez-Maure**, *Geometric study of Minkowski differences of plane convex bodies*, Canadian Journal of Mathematics **58** (2006), 600–624. DOI: [10.4153/CJM-2006-025-x](https://doi.org/10.4153/CJM-2006-025-x). Consulted: [official full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C13B5680AAEA98ABA76F1FB9956A968A/S0008414X00021969a.pdf/geometric-study-of-minkowski-differences-of-plane-convex-bodies.pdf), Section 4, especially Definition 4.4, Theorem 4.6, and the measure decompositions on pp. 614–616.

This source develops signed length measures for differences of support functions and uniqueness up to translation. Its discussion distinguishes discrete, absolutely continuous, and singular continuous parts. These are direct classical antecedents for treating \(h_C-h_L\) through \((\partial_\varphi^2+1)(h_C-h_L)\). **R. Schneider**, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Cambridge University Press, 2014, supplies the general support-function, surface-area-measure and Steiner-point framework; [publisher DOI](https://doi.org/10.1017/CBO9781139003858).

The collision-specific identity proved in v40 is

\[
2h_{C-A}-h_{K_+}-h_{K_-}+t|u\cdot e|=h_C-h_L.
\]

Its proof includes the identification and matching of the observed support components. For strictly convex \(C\), the measure \(S_C\) is nonatomic, while the chord contributes two negative atoms. The Jordan decomposition therefore separates them without boundary smoothness. Singular continuous obstacle curvature is allowed. This is more precise than identifying the positive part with a smooth curvature-radius density.

Classical signed-measure calculus begins after the experimental support identity has been established. The support-normal variable ranges over an already reconstructed spatial set; it does not increase the experimental alphabet beyond the two fixed vectors \(\pm te\).

## 2. Morphological observation and an unknown probe

**J. S. Villarrubia**, *Algorithms for scanned probe microscope image simulation, surface reconstruction, and tip estimation*, Journal of Research of the National Institute of Standards and Technology **102** (1997), 425–454. DOI: [10.6028/jres.102.030](https://doi.org/10.6028/jres.102.030). Consulted: [official NIST record](https://www.nist.gov/publications/algorithms-scanned-probe-microscope-image-simulation-surface-reconstruction-and-tip) and [full article](https://pmc.ncbi.nlm.nih.gov/articles/PMC4882144/).

Its dilation, erosion and blind tip-estimation setting is a useful antecedent for geometric observation with an unknown probe. In A2, the occupation support \(C-A\) alone leaves the unknown summands entangled. The two associated collision supports supply additional geometric information that cancels the footprint and leaves a body-minus-chord support function. Once this identifies the obstacle, support cancellation recovers the footprint and the occupation convolution identifies its probability law. The result concerns this structured geometric experiment, not unrestricted blind factorization.

## 3. Compact convolution, Fourier zeros, and exact uniqueness

**A. Delaigle and A. Meister**, *Nonparametric function estimation under Fourier-oscillating noise*, Statistica Sinica **21** (2011), 1065–1092. DOI: [10.5705/ss.2009.082](https://doi.org/10.5705/ss.2009.082). Consulted: [primary journal record and article links](https://www3.stat.sinica.edu.tw/sstest/j21n3/j21n34/j21n34.html).

This paper treats deconvolution in the presence of zeros of the error characteristic function, including compactly supported examples. Its statistical rates use additional assumptions. It is a relevant warning against treating nonvanishing Fourier division as automatic for an obstacle indicator.

The exact A2 argument is elementary and stated separately from statistical stability. For the recovered compact body \(C\), \(\widehat{\mathbf 1_C}\) is entire and nonzero at zero, so its nonzero set is dense in real frequency space. The component convolution determines \(\widehat\mu\) there, and continuity determines it everywhere. Fourier uniqueness identifies the finite measure. No launch density is required, and the proof does not claim stable division through the zero set. The finite theorem instead uses a quantitative moment argument.

## 4. Moment comparison and finite probability recovery

**P. Rigollet and J. Weed**, *Uncoupled isotonic regression via minimum Wasserstein deconvolution*, Information and Inference: A Journal of the IMA **8** (2019), 691–717. DOI: [10.1093/imaiai/iaz006](https://doi.org/10.1093/imaiai/iaz006). Consulted: [primary full text, arXiv:1806.10648v2](https://arxiv.org/html/1806.10648v2), Section 2.3, Theorem 4 and Corollary 1.

Section 2.3 relates moment comparison to Wasserstein distances and explicitly discusses the classical bounded-support route through polynomial approximation of Lipschitz functions and the dual formula for \(W_1\). Its broader one-dimensional moment bounds and uncoupled-regression minimax results are not asserted as new in A2 or imported as rates for collision observations.

The v40 finite proof supplies its own bivariate estimate, including perturbation of the recovered obstacle factor. For bounded independent pairs \((U,Z)\), \((\widetilde U,\widetilde Z)\), moment errors of size \(a\) in \(U\) and \(U-Z\), through degree \(4m\), give

\[
W_1(\mathcal L(Z),\mathcal L(\widetilde Z))
\le C/m+a(Cm)^{Cm}.
\]

The proof uses triangular convolution moments, an explicit factorial conditioning bound, tensor polynomial approximation and positivity of a finite grid measure. The sensor-specific steps preceding it are recovery of occupation from the two fixed fields, isolation of a complete component, finite-bit moment acquisition, and control of the reconstructed body moments. Hidden launch displacements are never treated as observed independent samples.

The preceding geometric theorem uses \(s=6+\beta\), the boundary-mass exponent \(\gamma\), and the stronger finite separation \(2t+\Delta<d_0\). Its sufficient bit bound is

\[
N_{\rm geom}(\nu,\delta)
\le C\nu^{-Q_{\rm pair}}\log(C/\nu)\log(C/(\nu\delta)),
\qquad Q_{\rm pair}=\frac{(\gamma+9/2)s}{s-2}.
\]

This rate comes from the proof's acquisition of positive nominal-record hulls and stable chord extraction, with the same two fixed commands. It is separate from classical moment-comparison estimates and from the weaker separation condition in exact identification.

The resulting sufficient bit bound is

\[
\exp\!\left[C\varepsilon^{-1}\log(C/\varepsilon)\right]
\log^2(C/\delta)
\]

for \(W_1\) error \(C\varepsilon\), under the quantitative geometric class. This records the conditioning cost of the proof and is not a joint minimax claim.

## 5. Transportation loss and weak reconstruction

**G. Peyré and M. Cuturi**, *Computational Optimal Transport*, Foundations and Trends in Machine Learning **11** (2019), 355–607. DOI: [10.1561/2200000073](https://doi.org/10.1561/2200000073). Consulted: [author project](https://optimaltransport.github.io/book/) and [full text](https://arxiv.org/html/1803.00567v4), Section 6.1, equation (6.1), and the discussion of weak metrics in Section 8. **C. Villani**, *Optimal Transport: Old and New*, Grundlehren der mathematischen Wissenschaften **338**, Springer, 2009, is a further standard reference; [publisher record](https://link.springer.com/book/10.1007/978-3-540-71050-9).

Kantorovich–Rubinstein duality, coupling, translation bounds and grid quantization are standard ingredients. The finite output in A2 is a probability measure with a finite atomic description. Its \(W_1\) approximation is meaningful for singular and absolutely continuous laws alike, but does not imply total-variation or \(L^1\)-density approximation. The separate bounded-variation density corollary states the additional hypothesis and finer acquisition accuracy needed for strong density recovery and uniform raw-mean prediction.

**C. Caillerie, F. Chazal, J. Dedecker and B. Michel**, *Deconvolution for the Wasserstein metric and geometric inference*, Electronic Journal of Statistics **5** (2011), 1394–1423. DOI: [10.1214/11-EJS646](https://doi.org/10.1214/11-EJS646). Consulted: [primary journal text](https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-5/issue-none/Deconvolution-for-the-Wasserstein-metric-and-geometric-inference/10.1214/11-EJS646.pdf) and [author bibliography](https://geometrica.saclay.inria.fr/team/Fred.Chazal/publis.html). This is a direct precedent for distribution deconvolution in a transportation metric motivated by geometric inference. Its page range begins at 1394.

**J. Rousseau and C. Scricciolo**, *Wasserstein convergence in Bayesian and frequentist deconvolution models*, Annals of Statistics **52** (2024), 1691–1715. DOI: [10.1214/24-AOS2413](https://doi.org/10.1214/24-AOS2413). Consulted: [author preprint](https://arxiv.org/abs/2309.15300) and [institutional publication record](https://www.dse.univr.it/?ent=pubbdip&id=1110507&lang=en). Its known-error additive observation model supplies a useful comparison for transportation inversion inequalities. The two unknown factors and Bernoulli active observations in A2 require a different acquisition proof.

## 6. Joint support and distribution inference with unknown noise

**J. Capitao-Miniconi, É. Gassiat and L. Lehéricy**, *Support and distribution inference from noisy data*, [arXiv:2304.09452](https://arxiv.org/abs/2304.09452). Consulted: the [author-hosted full text](https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/support.pdf), Sections 2.1–2.3 and 5.

This is a closer blind geometric-probabilistic comparison than known-kernel deconvolution alone. It studies additive observations without known noise or auxiliary noise samples, using independence between two noise-coordinate blocks and analytic and geometric signal conditions; its compact-support results include Wasserstein recovery. A2 obtains identification from two active collision fields, separated obstacle components and the signed support identity. Its arbitrary planar launch law need not have independent coordinate blocks. The comparison concerns the joint inverse problem and the source of identification; neither paper's statistical rate is transferred to the other experiment.

## 7. Bounded variation and the predictive conclusion

**B. Galerne**, *Computation of the perimeter of measurable sets via their covariogram. Applications to random sets*, Image Analysis and Stereology **30** (2011), 39–51. DOI: [10.5566/ias.v30.p39-51](https://doi.org/10.5566/ias.v30.p39-51). Consulted: [official full text](https://www.ias-iss.org/ojs/IAS/article/download/22/10/45), Proposition 11 on journal page 45.

The proposition gives the translation inequality

\[
\int|f(x+ru)-f(x)|\,dx\le |r|V_u(f)
\]

and its infinitesimal limit. The relationship between covariogram derivatives, variation and perimeter is classical. In the v40 prediction proof, the relevant function is a collision-start indicator on a protected bounded region. Sweeping a convex obstacle along a segment of length at most \(T\) increases its perimeter by at most \(2T\). Coupling the estimated and true launch measures then controls the spatially integrated error, while convex symmetric-difference bounds control the geometric perturbation.

The theorem concludes

\[
\sup_{|b|\le T}\|\widehat F_b-F_b\|_{L^1(U)}
\le C_{U,T}\bigl(\hbox{geometric error}+W_1(\widehat\mu_0,\mu_0)\bigr).
\]

It does not replace this norm by pointwise control for arbitrary singular laws. The same variation principle gives the separate density estimate

\[
\|\rho_h*\widehat\mu_0-j_0\|_1
\le CVh+Ch^{-1}W_1(\widehat\mu_0,\mu_0)
\]

when the zero extension of \(j_0\) has variation at most \(V\).

**L. Ambrosio, N. Fusco and D. Pallara**, *Functions of Bounded Variation and Free Discontinuity Problems*, Oxford Mathematical Monographs, Clarendon Press, Oxford, 2000. The [official Oxford University Press record](https://academic.oup.com/book/53762) identifies Chapter 3, *Functions of Bounded Variation*, as the standard reference for the BV facts used here, including translation bounds, coarea and the planar embedding in \(L^2\). The manuscript also gives the embedding argument explicitly: layer cake and Minkowski's inequality, followed by planar isoperimetry and coarea, yield \(\|j_0\|_2\le C|Dj_0|(\mathbb R^2)\le CV\).

For geometric tolerance \(\xi\), the swept-body symmetric difference has area \(O(\xi)\). Cauchy–Schwarz therefore bounds the true-density geometric contribution to any raw mean by \(C_{U,T}V\sqrt\xi\), uniformly for \(x\in U\) and \(|b|\le T\). Substituting the estimated density adds at most its \(L^1\) error. Acquiring \(W_1\) accuracy \(c\varepsilon^2\), using smoothing scale \(\varepsilon\), and retaining the finer geometric estimate in the construction consequently gives

\[
\sup_{x\in U,\,|b|\le T}
|\widehat F_b^{\rm dens}(x)-F_b(x)|
\le C_{U,T,V}\varepsilon
\]

at the same sufficient cost \(\exp[C\varepsilon^{-2}\log(C/\varepsilon)]\log^2(C/\delta)\) as the strong density output. The BV hypothesis belongs to both conclusions; it is absent from the probability and local spatial-mean conclusions. These are applications of classical variation bounds to the recovered collision geometry and probability law.

## 8. Retained angular inversion and attribution boundaries

**A. K. Louis, M. Riplinger, M. Spiess and E. Spodarev**, *Inversion algorithms for the spherical Radon and cosine transform*, Inverse Problems **27** (2011), 035015. DOI: [10.1088/0266-5611/27/3/035015](https://doi.org/10.1088/0266-5611/27/3/035015). Consulted: [author-hosted full text](https://www.uni-ulm.de/fileadmin/website_uni_ulm/mawi.inst.110/mitarbeiter/spiess/publications/inv-cos-rad.pdf), Section 4, Proposition 1.

The planar angular operator is classical. In the retained v39 collision-germ argument it gives an antipodal sum, and the additional spatial separation and normalization identify translated density copies. The companion preserves that proof and its hypotheses. The new main theorem instead differentiates a geometric support identity after recovering its spatial support components; it acquires no angular command sweep and no length tending to zero.

The finite-chain minimum and reversal balance have explicit repository antecedents in v29; the mean-exit and finite-polytope inverses have later repository antecedents. Their source identities and distinctions are recorded in [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md). These manuscripts document derivation history. They are not counted as independently published literature.

The claimed contribution is the complete identification chain from two fixed positive-length forward fields, together with a finite experiment that yields a probability law and bounded-length response predictions. The support calculus, moment-to-transport principle, variation inequalities, exact Fourier uniqueness, and existing deconvolution rates retain their classical attribution. Full spatial fields remain continuum data in the exact theorem; a finite-bit theorem has its own quantitative priors and resource accounting.
