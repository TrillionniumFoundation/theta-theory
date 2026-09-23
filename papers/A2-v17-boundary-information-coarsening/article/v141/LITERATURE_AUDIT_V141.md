# Primary-source and map-specific comparison — A2 v141

Date: 23 September 2026. This file distinguishes inspected mathematical statements, our additional proofs, and documentary comparisons not yet verified. It is not an exhaustive priority certificate.

## 1. Exact external question answered

C. Fevola, Y. Mandelshtam and B. Sturmfels, *Pencils of quadrics: old and new*, Le Matematiche 76 (2021), 319–335, DOI 10.4418/2021.76.2.2. The version used for numbering is **arXiv:2009.04334v2, 19 May 2021**: https://arxiv.org/pdf/2009.04334.

The primary text was inspected, particularly §4, pp. 8–11, equation (14), Corollary 4.4, Conjecture 4.5, and Example 4.6. The conjectural assertion is the existence of unrestricted real data giving `2r-3` distinct real reciprocal likelihood critical points for every definite pencil with `r` distinct eigenvalues. The requirement is not that the data be positive definite or that all critical points be positive definite. Example 4.6 uses mixed-sign data. Our `thm:totally-real-reciprocal-likelihood` proves that precise assertion by explicit residues and two separated strings of sign changes; it additionally proves nondegeneracy and a nonempty open set of such data. The proof does not invoke the generic complex ML degree as an upper bound.

The same primary source supplies the classical Weierstrass–Segre classification (Theorem 1.1), spectral elementary divisors (Corollary 2.1 and equation (5)), reciprocal curves (§3), and Segre closure order (Theorem 5.1). None of those is claimed as a new classification. Scheme-theoretic transport under a closed immersion is formal. The new relative input is the actual multiplication-failure neighbourhood family and its base-change-compatible spectral Fitting readout.

PDF screenshot requests for the relevant page returned a tool error; no figure, diagram, or table transcription is used. The readable theorem text supplies the comparison. Searches for a later resolution did not supply a verified priority determination, so the paper says that it proves the assertion formulated in that source, not that an exhaustive historical search has established a first solution.

## 2. Exact restricted contraction and its classical neighbors

The object to compare is not an unspecified contraction. With `W=Sym^2 V`, `dim V=n`, fix the polarized map

`j_n: det(V) tensor Sym^n(V) -> wedge^n W`,

whose pure-power value is the wedge of the `n` products `ell*x_i`. The Jacobian map `C_n` is normalized by `C_n j_n=2 id`. For `q in W*` the map in the theorem is

`kappa_(n,q)=iota_q j_n: det(V) tensor Sym^n(V) -> wedge^(n-1) W`.

Its rank-dependent kernel is `det(V) tensor Sym^n(rad q)` at rank `<n`; at full rank it is zero for odd `n`, and the line `det(V) tensor C(q^{-1})^(n/2)` for even `n`. This is the exact formula requiring priority comparison, not harmonic decomposition alone.

| Primary statement / operator | What is classical | Exact additional calculation in the manuscript |
|---|---|---|
| Howe, *Remarks on classical invariant theory*, Trans. AMS 313 (1989), Theorem 9 and §4(a), pp. 555–557; DOI 10.1090/S0002-9947-1989-0986027-X | Full orthogonal harmonic decomposition and commuting quadratic multiplication/Laplacian operators | Restrict `iota_q j_n` to every harmonic summand, prove the nonzero coefficients, and isolate the even scalar line. Howe's decomposition is not presented as the restricted kernel formula. |
| Olive, *About Gordan's algorithm for binary forms*, arXiv:1403.2283v5, §2.2, Definition 2.6 and Remark 2.7 | The first binary transvectant is the two-input Jacobian with its normalization | At `n=2`, the kernel is elementary because `j_2` is onto. The singular/all-rank calculation for `n>=3` is not inferred from this binary identity. |
| Unrestricted exterior contraction `iota_q: wedge^n W -> wedge^(n-1) W` | Its kernel is `wedge^n ker q` for nonzero `q` | Compute the intersection with `im j_n`, including singular quadratic ranks. This records a possible equivalent-map route explicitly. |
| Quadratic apolar operator `q(partial): Sym^n V -> Sym^(n-2) V` | Its full-rank kernel is the harmonic summand | Its source/target and kernel dimension differ from those of `iota_q j_n`; it is not an interchangeable operator. |
| Kupferman–Shachar, *A geometric perspective on the Piola identity in Riemannian settings*, J. Geom. Mech. 11 (2019), 59–76; arXiv:1805.12365v1, equation (1.1), §3.1 | Cofactor-divergence cancellation | The even scalar calculation uses such cancellation; a Piola identity does not by itself give all singular-rank kernels. |
| Landsberg–Ottaviani, arXiv:1111.4567v1, §10.1; Sheridan, arXiv:1906.05465v1, §2.4 | Exterior/skew-flattening support and secant/tangent support bounds | The manuscript computes the support on this specified Jacobian component and obtains a strict gap above `2n`. |

Howe's primary full text and the indicated operator sections were examined in this revision; the earlier detailed comparisons and their source records are retained in `LITERATURE_AUDIT_V138.md`, `LITERATURE_AUDIT_V139.md`, and `parts/19-operator-comparison.tex`. Primary routes include https://www.ams.org/tran/1989-313-02/S0002-9947-1989-0986027-X/S0002-9947-1989-0986027-X.pdf, https://arxiv.org/pdf/1403.2283, and https://arxiv.org/pdf/1805.12365. Version-specific numbering is that recorded in the bibliography; later arXiv revisions are not silently assigned old numbering.

For singular `q`, the proof uses the nondegenerate orthogonal factor **and radical shears**. This is a material difference from a full-rank orthogonal-branching comparison. The full orthogonal group, including the dimension-two reflection, remains in the proof. The scalar even-dimensional case and all singular-rank cases remain explicit.

**Status:** the comparison identifies differences from inspected statements and the exact equivalent exterior-intersection problem. It does not prove that no equivalent kernel formula exists anywhere in the invariant-theory literature. Independent expert priority clearance has not been obtained and is not represented by a passing script.

## 3. Ballico 1993 — six axes, with the evidentiary boundary retained

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13; DOI 10.1002/mana.19931630102.

The publisher table of contents was checked again: https://onlinelibrary.wiley.com/toc/15222616/1993/163/1. The full article was not obtained at the attempted publisher PDF route https://onlinelibrary.wiley.com/doi/pdf/10.1002/mana.19931630102. The inherited v139 audit records earlier library/institutional searches. Discovery of an unconnected scholarly-reading integration does not constitute access to the article. No paid access, interlibrary loan, or author request was performed.

| Requested axis | Present precise statement and location | Ballico theorem/proof text |
|---|---|---|
| Parameter spaces | `Gr(2,Sym^2 V)` and the relative socle Grassmannian; `sec:natural-pencils`, `sec:relative-spectral-strata` | Not obtained; unverified |
| Reduced versus scheme-theoretic failure | Literal maximal-minor/Fitting ideal; fixed reduced Schubert divisor | Not obtained; unverified |
| Varied map | Actual multiplication `Sym^m(O+U) -> A_R`, not an inserted coefficient block | Not obtained; unverified |
| Nilpotent/infinitesimal structure | Socle ideal filtration, normal cone, determinant colon, first homogeneous relation | Not obtained; unverified |
| Relative/base change | Closed relation-space immersion and actual universal ideal-adic neighbourhood, arbitrary complex base change | Not obtained; unverified |
| Inverse/reconstruction conclusion | Unmarked order-`d` classification of pencils, spectral sheaf, framed spectral incidence schemes | Not obtained; unverified |

A title, bibliographic record, first-page route, or later citation does not establish any entry in the last column. The manuscript makes neither an anticipation nor a nonanticipation claim about the unread proofs. This remains the specific documentary item requested in B140.2; the new external theorem does not erase it.
