# Literature audit — A2 v41

**Search and inspection date: 4 October 2026.** This audit addresses §11.1 of the [v40 referee report](../../reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md). The corresponding manuscript discussion is [Related inverse problems](core/28_theorem_comparison.tex). The comparison records the observation, assumptions, complete ambiguity where established, and conclusion of the closest inspected primary results. It also preserves attribution for the analytic, transportation and variation tools used in the retained programme. It makes no exhaustive priority assertion.

## 1. The theorem being compared

The exact A2 datum is the ordered pair of spatial fields \((F_{te},F_{-te})\), with one fixed positive length and one fixed direction. Starts remain hidden. Each field averages the same forward collision bit against one unknown stationary probability \(\mu\). The obstacle configuration is nonempty and locally finite, with compact strictly convex planar bodies, bounded diameters and gap \(d>0\). The support \(A\) of \(\mu\) is compact and convex, and \(t+\operatorname{diam}A<d\). The law may be atomic or singular; \(A\) may be a point or segment. No coordinate independence or boundary smoothness is assumed in the exact theorem.

The finite prefix formula first recovers occupation. A matched occupation support \(P=C-A\) and two collision supports then satisfy

\[
2h_P-h_{K_+}-h_{K_-}+t|u\cdot e|=h_C-h_{L_C}.
\]

The negative atoms of the associated signed measure identify the transverse chord \(L_C\); the remaining nonatomic measure identifies the strictly convex body. Support cancellation recovers the footprint, and the isolated occupation convolution recovers the whole probability. The full equivalence class is common translation of obstacles, footprint and launch law. The same reconstruction determines all bounded-length forward responses and the full period group. These are the inputs and outputs against which the following results are compared.

## 2. Geometric factorization: covariograms and an unknown probe

The direct convex-geometric predecessor is the **cross covariogram**, not only morphological dilation. For convex bodies,

\[
g_{C,A}(x)=|C\cap(A+x)|=\mathbf1_C*\mathbf1_{-A}(x).
\]

| Primary result and inspected location | Input and hypotheses | Equivalence class and conclusion |
| --- | --- | --- |
| G. Averkov and G. Bianchi, *Confirmation of Matheron's conjecture on the covariogram of a planar convex body*, JEMS **11** (2009), 1187–1202. [Official article](https://ems.press/journals/jems/articles/1922); [full text](https://ems.press/content/serial-article-files/31689?nt=1). Theorem 1.1, journal p. 1188. DOI **10.4171/JEMS/179**. | Whole covariogram \(g_{C,C}\); any planar convex body. | Determines the body up to translation and reflection. |
| G. Bianchi, *The cross covariogram of a pair of polygons determines both polygons, with a few exceptions*, Adv. Appl. Math. **42** (2009), 519–544. [Primary manuscript](https://arxiv.org/pdf/0805.1805), Theorem 1.1, PDF p. 3, and Examples 4.1, 5.2. DOI **10.1016/j.aam.2008.10.002**. | Whole \(g_{C,A}\), with both factors planar convex polygons; competitors are planar closed convex sets. | Common translation and reflected interchange are trivial associates. Further ambiguities occur in the specified affine parallelogram families. The exceptions are part of the theorem. |
| G. Bianchi, *The covariogram and Fourier–Laplace transform in* \(\mathbb C^n\), Proc. Lond. Math. Soc. **113** (2016), 1–23. [Primary manuscript](https://arxiv.org/pdf/1312.7816), Theorem 6.3, PDF p. 17. DOI **10.1112/plms/pdw020**. | Whole cross covariogram; both factors and both competitors are planar \(C^8_+\) bodies. | Unique up to common translation and reflected interchange. The proof uses Fourier–Laplace transforms and their zeros; it already treats two unknown geometric factors. |
| G. Bianchi, R. J. Gardner and M. Kiderlen, *Phase retrieval for characteristic functions of convex bodies and reconstruction from covariograms*, JAMS **24** (2011), 293–343. [Primary manuscript](https://arxiv.org/pdf/1003.4486), Theorem 4.10, PDF p. 22, and Theorem 6.4. DOI **10.1090/S0894-0347-2010-00683-2**. | Noisy covariogram grids; centered convex body in a known cube, determined by its covariogram. NoisyCovLSQ requires rowwise independent centered errors with bounded third absolute moments and independent consistent Blaschke- or difference-body approximations. Theorem 6.4 supplies the latter from grids under fourth-moment and smoothing assumptions. | Algorithmic strong Hausdorff consistency up to reflection. This is a finite geometric reconstruction precedent, with a different observation model. |
| J. S. Villarrubia, *Algorithms for scanned probe microscope image simulation, surface reconstruction, and tip estimation*, J. Res. NIST **102** (1997), 425–454. [Official full text](https://nvlpubs.nist.gov/nistpubs/jres/102/4/j24vil.pdf). §5.1, equations (14)–(15), journal pp. 433–434; §7.3.3, p. 445. DOI **10.6028/jres.102.030**. | Morphological dilation images and an initial containing bound for the unknown tip. Further images supply additional intersections of constraints. | The decreasing iterates contain the actual tip and yield the largest consistent tip in the initial bound. Actual-tip equality depends on the contacts encoded by the data. The conclusion is a maximal consistent reconstruction. |

**Comparison.** Uniform launch on a full-dimensional \(A\) gives the A2 occupation field \(|A|^{-1}g_{C,A}\). This is a normalized cross covariogram; the area factor must be retained when comparing the observations. The two ordered collision fields contain additional support information. They yield a full factor separation for a general compact probability, allow a nonsmooth strictly convex obstacle and an arbitrary convex footprint, and extend componentwise to the separated configuration. The orientation and ordering are fixed experimental information, and the A2 fiber has no additional reflected interchange. The finite collision theorem accounts for the bits needed to acquire its support information; a noisy-covariogram sample is not supplied to that procedure.

### Follow-ups checked

G. Jóźwiak and coauthors, *The regularized blind tip reconstruction algorithm as a scanning probe microscopy tip metrology method*, [arXiv:1105.1472v1](https://arxiv.org/pdf/1105.1472), §2.2, equations (2)–(4), develops threshold regularization of blind tip reconstruction and tests it numerically and experimentally. Its reconstruction constraints preserve the morphological antecedent above; it supplies no replacement theorem identifying an arbitrary probability kernel.

Y. Matsunaga, S. Fuchigami, T. Ogane and S. Takada, *End-to-end differentiable blind tip reconstruction for noisy atomic force microscopy images*, Scientific Reports **13** (2023), 129, DOI [10.1038/s41598-022-27057-2](https://www.nature.com/articles/s41598-022-27057-2), was screened through the primary abstract and [author implementation](https://github.com/matsunagalab/differentiable_BTR). Full article retrieval was blocked during this audit; no theorem-level conclusion is attributed to that screening.

G. Bianchi, A. Burchard and Y. Lin, *Strict concavity properties of cross covariograms*, [arXiv:2508.03887v1](https://arxiv.org/html/2508.03887v1), Theorems 1–3, concerns strict concavity and affine behavior of cross covariograms. These results concern the shape of the observed function and do not replace a factor-identification theorem.

## 3. Unknown-noise identification and joint support inference

| Primary result and inspected location | Data and identifying assumptions | Equivalence class or quantitative conclusion |
| --- | --- | --- |
| É. Gassiat, S. Le Corff and L. Lehéricy, *Deconvolution with unknown noise distribution is possible for multivariate signals*, Ann. Statist. **50** (2022), 303–323. [Journal-layout author PDF](https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/deconvolNP_aos.pdf), Theorem 2.1, PDF p. 4. DOI **10.1214/21-AOS2106**. | Law of \(Y=X+\epsilon\); independence of signal and noise and between two specified noise-coordinate blocks; signal transform growth order \(\rho<2\) and condition (H2). | Identifies both summands up to opposite translations. (H2) is the absence of identically zero complex coordinate slices of the signal transform, not merely ordinary dependence. |
| J. Capitao-Miniconi, É. Gassiat and L. Lehéricy, *Support and Distribution Inference from Noisy Data*, Bernoulli, forthcoming. [Accepted manuscript](https://www.e-publications.org/ims/submission/BEJ/user/submissionFile/68730?confirm=a078ae36), Corollary 2.5, p. 6; Theorem 5.1, p. 17. [Author version](https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/support.pdf). | Product-noise observations; singleton support slices, including strictly convex supports; quantitative standardness, transform, contrast (Amin), and noise bounds. | Uniform compact-signal \(W_p\) risk at most \(C\log\log n/\log n\). Exact identification is recalled in Theorem 2.2. |

**Comparison, including the overlapping submodel.** If \(U_C\) is uniform on a component and independent of \(Z\), then \(v_C/|C|\) is the density of \(U_C-Z\). For a product launch law, the cited strict-convex-support criterion applies to \(U_C\). Thus additive unknown-noise identifiability already covers this submodel after the occupation reduction. The A2 geometric separation handles general dependent planar launch laws by using the matched collision supports. Its finite controls and observations are nominal sites and collision bits, rather than samples of the vector \(U_C-Z\). This distinction concerns the source of identification and acquisition of information; it does not imply that singular-law inference or joint support inference first occurs in A2.

**Version and proof-status pins.** Status: [official forthcoming list](https://www.bernoullisociety.org/publications/bernoulli-journal/bernoulli-journal-papers), [author bibliography](https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/liste-publi.html). Accepted/author numbering: Theorem 2.2/Theorem 1; Corollary 2.5/Corollary 2; Theorem 5.1/Theorem 6. The PDFs have 30/51 pages. The [Gassiat–Le Corff–Lehéricy author erratum](https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/erratum.pdf) concerns the quantitative contrast argument in Proposition A.2. No statistical bound from that argument is imported into A2; its moment conditioning is proved directly.

## 4. Signed support measures, compact transforms and moment inversion

| Source and precise location | Classical conclusion and hypotheses | Role in A2 |
| --- | --- | --- |
| Y. Martinez-Maure, *Geometric study of Minkowski differences of plane convex bodies*, Canad. J. Math. **58** (2006), 600–624. [Official full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C13B5680AAEA98ABA76F1FB9956A968A/S0008414X00021969a.pdf/geometric-study-of-minkowski-differences-of-plane-convex-bodies.pdf), Definition 4.4 and Theorem 4.6, p. 612. DOI **10.4153/CJM-2006-025-x**. | A finite signed circle measure with zero first moment determines its generalized support difference up to translation. This does not select its ordered convex summands. | Attribution for signed length measures. The obstacle-minus-chord identity and mutual singularity of its nonatomic and atomic contributions supply the additional factor separation. |
| A. Meister, *Deconvolving compactly supported densities*, Math. Methods Statist. **16** (2007), 63–76. [Institutional preprint](https://www.f08.uni-stuttgart.de/.content/media/downloads/Mathematik/mathematische_berichte/2005/2005-007.pdf), §2 and Theorem 1. DOI **10.3103/S106653070701005X**. | Univariate compact target density; the error transform is known and bounded away from zero only on a neighborhood of the origin. Polynomial continuation gives consistency and Sobolev risk bounds, including logarithmic rates for fixed support. | A direct analytic-continuation antecedent. Compactness can make local frequency information sufficient; this exact principle does not itself bound the conditioning cost. |
| A. Delaigle and A. Meister, *Nonparametric function estimation under Fourier-oscillating noise*, Statistica Sinica **21** (2011), 1065–1092. [Official full text](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A21n34.pdf), Theorem 4.1, p. 1076. DOI **10.5705/ss.2009.082**. | A univariate known error transform satisfying the specified oscillating lower bound; one-sided support and Sobolev regularity of the signal. Gives finite integrated squared-risk bounds on bounded intervals. | Relevant zero-aware statistical deconvolution, with its own support and spectral hypotheses. It is not used as a theorem for arbitrary planar zero sets or an unknown error factor. |
| P. Rigollet and J. Weed, *Uncoupled isotonic regression via minimum Wasserstein deconvolution*, Inform. Inference **8** (2019), 691–717. [Primary full text](https://arxiv.org/html/1806.10648v2), §2.3, Theorem 4 and Corollary 1. DOI **10.1093/imaiai/iaz006**. | Quantitative moment-to-\(W_p\) comparison for univariate laws; the bounded-support corollary relates finite moment accuracy and degree to transport error. | Classical transportation principle. A2 proves the required bivariate mixed-moment estimate, its sensitivity to body-factor error and its acquisition from Bernoulli fields. |

R. Schneider, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Cambridge University Press, 2014, [publisher DOI](https://doi.org/10.1017/CBO9781139003858), supplies the support-function, surface-area-measure and Steiner-point framework. The v41 exact proof includes its needed planar measure statements and applies them to nonsmooth strictly convex bodies.

**The multivariable Fourier point.** After geometry has been recovered, A2 knows the compact nonzero factor \(\mathbf1_C\). Its transform is entire on \(\mathbb C^2\), and its real zero set has empty interior. The unknown finite measure transform is determined on the dense complement and then everywhere by continuity. This reasoning allows zero curves and uses no coordinate product structure. It is distinct from the two-unknown-factor Fourier–Laplace analysis in Bianchi's theorem and from the one-dimensional statistical assumptions in the last table. Finite stability is supplied separately by the explicit estimate

\[
W_1(\mathcal L(Z),\mathcal L(\widetilde Z))
\le C/m+a(Cm)^{Cm},
\]

for the bounded bivariate moment problem through degree \(4m\), including error in the recovered body factor. These steps, together with positive nominal-record hulls and finite occupation acquisition, yield A2's sufficient law cost

\[
\exp[C\varepsilon^{-1}\log(C/\varepsilon)]\log^2(C/\delta).
\]

This cost is not a transferred passive-deconvolution rate or a minimax-optimality assertion. The geometric acquisition uses the stated stronger separation \(2t+\Delta<d_0\), smoothness \(s=6+\beta\), boundary mass exponent \(\gamma\), and power \(Q_{\rm pair}=(\gamma+9/2)s/(s-2)\).

## 5. Retained transportation, prediction and angular attribution

The following sources remain relevant to the full retained programme. Their role is an identified analytic ingredient, with the collision-specific reduction proved in the manuscript.

| Ingredient | Primary reference and inspected scope | Use and attribution boundary |
| --- | --- | --- |
| Transportation duality | G. Peyré and M. Cuturi, *Computational Optimal Transport*, Found. Trends Mach. Learn. **11** (2019), 355–607, [§6.1, equation (6.1)](https://arxiv.org/html/1803.00567v4); C. Villani, *Optimal Transport: Old and New*, Springer, 2009, [publisher](https://link.springer.com/book/10.1007/978-3-540-71050-9). | Couplings, duality and finite grid measures are standard. A2's probability output is meaningful for singular laws, with density recovery under its separately stated BV prior. |
| Known-error geometric deconvolution | C. Caillerie, F. Chazal, J. Dedecker and B. Michel, *Deconvolution for the Wasserstein metric and geometric inference*, EJS **5** (2011), 1394–1423, [journal text](https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-5/issue-none/Deconvolution-for-the-Wasserstein-metric-and-geometric-inference/10.1214/11-EJS646.pdf). | Direct precedent for transportation loss in geometric inference with a known error law. |
| Transportation inversion inequalities | J. Rousseau and C. Scricciolo, *Wasserstein convergence in Bayesian and frequentist deconvolution models*, Ann. Statist. **52** (2024), 1691–1715, DOI [10.1214/24-AOS2413](https://doi.org/10.1214/24-AOS2413); [author manuscript](https://arxiv.org/abs/2309.15300). | Known-error additive observations; no statistical rate is assigned to the collision experiment from this source. |
| Variation of translates | B. Galerne, *Computation of the perimeter of measurable sets via their covariogram. Applications to random sets*, Image Anal. Stereol. **30** (2011), 39–51, [Proposition 11, p. 45](https://www.ias-iss.org/ojs/IAS/article/download/22/10/45). | The bound \(\|f(\cdot+ru)-f\|_1\le|r|V_u(f)\) controls collision-indicator translation under a coupling. |
| BV smoothing and embedding | L. Ambrosio, N. Fusco and D. Pallara, *Functions of Bounded Variation and Free Discontinuity Problems*, Oxford, 2000, [Chapter 3](https://academic.oup.com/book/53762). | Translation, coarea and planar BV-to-\(L^2\) estimates. A2 gives the embedding argument used for its density and uniform-prediction conclusion. |
| Nominal positive-record hulls | V.-E. Brunel, *Uniform behaviors of random polytopes under the Hausdorff metric*, Bernoulli **25** (2019), 1770–1793, DOI [10.3150/18-BEJ1035](https://doi.org/10.3150/18-BEJ1035). | Attribution for cap-mass support estimation. The collision procedure observes nominal centers with positive bits, not hidden points sampled from an obstacle. |
| Retained angular inversion | A. K. Louis, M. Riplinger, M. Spiess and E. Spodarev, *Inversion algorithms for the spherical Radon and cosine transform*, Inverse Problems **27** (2011), 035015, [§4, Proposition 1](https://www.uni-ulm.de/fileadmin/website_uni_ulm/mawi.inst.110/mitarbeiter/spiess/publications/inv-cos-rad.pdf). | Classical planar angular operator in the retained collision-germ proof. A2's fixed-pair inverse differentiates a reconstructed support function and acquires no angular command sweep. |

The probability theorem yields local spatial \(L^1\) prediction uniformly over commands of bounded length. Under the additional BV density prior, smoothing at scale \(\varepsilon\) after acquiring \(W_1\) error of order \(\varepsilon^2\) gives density \(L^1\) error and uniform raw-mean error of order \(\varepsilon\), at sufficient cost \(\exp[C\varepsilon^{-2}\log(C/\varepsilon)]\log^2(C/\delta)\). These losses and hypotheses remain distinct in the statements.

The repository's finite-chain minimum, reversal balance, mean-exit and finite-polytope inverses are traced in [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md). They document derivation history and are not counted as independently published literature.

## 6. Search record and scope of the audit

The search used broad primary-source discovery, then exact-title and theorem searches, followed by inspection of the full texts identified above. Representative queries were:

- `blind geometric deconvolution convex bodies unknown probe identifiability theorem`; `Villarrubia blind tip reconstruction largest consistent tip`; `blind tip reconstruction uniqueness theorem followup`.
- `cross covariogram pair convex bodies determines both bodies`; `Bianchi cross covariogram C8 Theorem 6.3`; `cross covariogram identifiability 2025 2026`; `noisy covariogram reconstruction convex bodies theorem Gardner Kiderlen`.
- `Gassiat Le Corff Lehericy unknown noise multivariate Theorem 2.1`; `Support and Distribution Inference from Noisy Data theorem strictly convex`; `Support and Distribution Inference from Noisy Data Bernoulli`; `Gassiat deconvolution erratum Proposition A.2`.
- `Martinez Maure Minkowski differences signed length measure Theorem 4.6`; `Delaigle Meister Fourier oscillating noise Theorem 4.1`; `Meister deconvolving compactly supported densities`; `multivariate deconvolution compactly supported zeros characteristic function theorem`.
- `Rigollet Weed moment Wasserstein Theorem 4`; `Adaptive minimax-optimal Wasserstein deconvolution with unknown error distributions`.

The last query also located C. Scricciolo's 2026 Statistics & Probability Letters article, [publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0167715225002342), DOI **10.1016/j.spl.2025.110589**. The full text was unavailable in this audit, so it is recorded as bibliographic screening and supplies no theorem-level comparison or priority inference. Search results and blocked pages were not treated as inspected proofs.

The substantive expansion over v40 is the explicit cross-covariogram comparison, the complete unknown-noise identification hypotheses, the product-launch submodel overlap, the distinction between signed-difference reconstruction and factor separation, and the separation of exact multivariable Fourier uniqueness from statistical zero-handling assumptions. These comparisons preserve the full collision theorem and identify the experiment-specific assertions to be assessed on their proofs.
