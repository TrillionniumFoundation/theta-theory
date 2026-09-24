# A2 v135 primary-source comparison

Date: 23 September 2026. Controlling review commit: `a08b157800c27c0f73f0c5c9a52155265ef4f395`.

## Exact primary statements inspected

**Grassmannian tangents.** A. Boralevi, *A note on secants of Grassmannians*, Rend. Istit. Mat. Univ. Trieste 45 (2013), 67–72, https://rendiconti.dmi.units.it/volumi/45/011.pdf . Lemma 2.1, printed p.68, gives the affine tangent formula `Λ^(k−1)R ∧ W`. Its elementary support bound is treated as classical. The additional assertion here is the position of the specified quartic Schur submodule, not a new result about general secant dimensions.

**Essential variables.** E. Carlini, *Reducing the number of variables of a polynomial*, https://arxiv.org/pdf/math/0507531 . Proposition 1 and its proof, pp.5–6, give the first-catalecticant rank and derivative-span characterizations. Page 6 was also inspected as a rendered image. This is the classical criterion used for the binary boundary. Publication metadata were checked at the author's institutional record, https://iris.polito.it/handle/11583/1500789 (2006, pp.237–247).

**Subspace varieties.** J. M. Landsberg and J. Weyman, *On the ideals and singularities of secant varieties of Segre varieties*, author manuscript January 2007, https://people.tamu.edu/~jml//1-07LWsecseg.pdf . Definition 1 and Theorem 3.1 (printed p.5) describe tensor-product subspace varieties, flattening generators and singularities. This is a methodological comparison, not a theorem about the contraction of our determinant-twisted quartic summand. A2 proves its exterior-support identity directly and does not import radicality or singularity assertions for alternating tensors.

**Unramified morphisms.** Stacks Project, Section 29.36, Tag 02G3, Lemma 29.36.14, https://stacks.math.columbia.edu/tag/02G3 . Only the relative-differential criterion is used to explain the Fitting non-unramified locus; no global finite-flat double cover is asserted.

## Claim-level boundary

| Item | What is and is not asserted |
|---|---|
| Multiplicity-one embedding; Cauchy and SL₂ operations | Classical representation theory, with the needed small character calculations displayed. No new plethysm method. |
| Exterior support and support-eight secant/tangent bound | Elementary/classical linear algebra; proved directly. |
| Essential variables | Carlini Proposition 1; no novelty claim. |
| Exact kernel of `iota_q j` for every bilinear rank | Specialized calculation proved by shear descent and the full SO₄ decomposition. The inspected statements above do not state this kernel result. This is a bounded comparison, not exhaustive novelty clearance. |
| Reduced support-locus pullbacks | Exact consequence of the support table. No ideal-radicality assertion. |
| Closed second-secant exclusion | Uses support-eight closedness; no full tensor-rank or orbit classification. |
| Smooth-web reconstruction | Combines intrinsic readout, common projective coordinates, and support separation; not merely the classical Jacobian K3 construction. |
| Ambient binary-Jacobian boundary | Containment of support, not equality or an irreducible-component classification. |

Inherited representation references remain, including Fulton–Harris and De Concini–Eisenbud–Procesi. This revision does not claim a fresh complete reading of those works. Its new target decomposition is derived in the manuscript from explicit character identities.

## M134.1: missing complete Ballico 1993 text

Target: E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

Current-session attempts included https://onlinelibrary.wiley.com/doi/10.1002/mana.19931630102 , https://onlinelibrary.wiley.com/doi/pdf/10.1002/mana.19931630102 , https://iris.unitn.it/simple-search?query=10.1002%2Fmana.19931630102 , exact-title/DOI web searches, and exact-title/DOI search in the user's Library. No complete readable lawful copy was obtained. The Library returned earlier A2 patches and responses, not Ballico's article. These failures do not establish that no accessible copy exists elsewhere.

| Required axis | A2 object | Ballico comparison |
|---|---|---|
| Parameter spaces | Gr(4,Sym²V), then Gr(4,V⊕S_R) | Unverified |
| Scheme structure | Full zeroth-Fitting failure scheme | Unverified |
| Varied multiplication | Sym^m(O⊕K) → B_R⊗O, m≥2 | Unverified |
| Nilpotent/colon data | Intrinsic layers, deepest cone, residual ideals | Unverified |
| Base change | Relative Fitting/flat-flag and primary-module results | Unverified |
| Inverse reconstruction | Entire smooth Jacobian locus | Unverified |

The accessible **1996** paper, *On the failure cycles for the quadratic normality of a projective variety*, Pacific J. Math. 172 (1996), 307–313, https://msp.org/pjm/1996/172-2/pjm-v172-n2-p01-s.pdf , is distinct. Its Definition 0.1 measures failure by a multiplication-cokernel dimension, and Theorem 0.2 gives a linear-section conclusion under its stated cohomological and codimension hypotheses. The page containing that theorem was inspected. This does not resolve any of the six 1993 comparisons.

`Ballico_1993_full_text_obtained=false`; `priority_certified=false`. No anticipation or nonanticipation conclusion is inferred from metadata or a different paper.
