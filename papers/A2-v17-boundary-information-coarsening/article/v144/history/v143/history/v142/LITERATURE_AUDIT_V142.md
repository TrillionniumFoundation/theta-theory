# Source and exact-operator audit — A2 revision 142

Date: 24 September 2026. This is an inspected-source comparison, not exhaustive historical priority certification. The substantive post-review v141 source at `8cd389f4048a1047be9aa8e8e4f642595175a555`, its audit and real-likelihood theorem are preserved.

## Primary spectral sources inspected

Marco Trevisiol, *Normality of closure of orthogonal nilpotent symmetric orbits*, arXiv:2105.08680v3, 10 May 2022, https://arxiv.org/pdf/2105.08680. Section 1, page 3, equation (2) and the following paragraphs give the full-orthogonal self-adjoint nilpotent classification, orbit dimensions and dominance closure. The page image and the following page were inspected. These are self-adjoint operators, not skew-adjoint orthogonal Lie algebra elements. Full orthogonal orbits need not be connected; no general normality claim is used.

Fevola–Mandelshtam–Sturmfels, *Pencils of quadrics: old and new*, Le Matematiche 76 (2021), 319–335, DOI 10.4418/2021.76.2.2, arXiv:2009.04334v2, https://arxiv.org/pdf/2009.04334. Theorem 1.1, Corollary 2.1 and Theorem 5.1 supply classical pencil classes and Segre/Jordan closure order. The new theorem credits that input; its further assertions concern actual finite failure neighbourhoods, sharp intrinsic detection and a marked first-Betti/Hilbert locus. The retained v141 proof of the assertion formulated as Conjecture 4.5 is neither a new v142 result nor an exhaustively certified first solution.

## Exact map, groups and irreducible summands

Set D=det V, W=Sym^2 V and dim V=n. The GL(V)-equivariant polarization `j_n(epsilon tensor ell^n)=wedge_i(ell*x_i)` has domain `D tensor Sym^n V`, highest weight `(n+1,1,...,1)`, and codomain `wedge^n W`. The family `kappa_(n,q)=iota_q j_n` is GL(V)-covariant as q varies contragrediently. For fixed nondegenerate q the group is the full O(q). The Jacobian covariant C_n is normalized by `C_n j_n=2 id`.

| Classical map | Signature and decomposition | Exact comparison |
|---|---|---|
| Apolar Laplacian Delta_q | Sym^n V -> Sym^(n-2) V; full-rank kernel H_n, dimension binom(2n-1,n)-binom(2n-3,n-2) | Not kappa. The new mixed formula specifies a composite through derivations and h Delta_q. |
| Angular Casimir E(E+n-2)-rho Delta_q | End(Sym^n V), O(q); summands rho^t H_m, m+2t=n, eigenvalues m(m+n-2) | Exactly n(n-1)/2 times C_n (rho wedge -) kappa, and a scalar multiple of kappa* kappa in the specified norms. |
| Unrestricted iota_q | wedge^n W -> wedge^(n-1) W; kernel wedge^n ker(q:W->C) | Restricted kernel is its intersection with im j_n, not the unrestricted exterior kernel. |
| Binary Jacobian / first transvectant | wedge^2 Sym^2 V -> det V tensor Sym^2 V, n=2 | j_2 is onto and its nonzero contraction kernel is an elementary line; the new identity covers all n and ranks. |
| Fischer adjoints | Multiplication and differentiation on symmetric powers; normalized monomial norm alpha!/k! | We prove j_n*=2^(-n) C_n and iota_q*=rho wedge -, fixing the exact Gram scale. |
| Exterior support / skew flattening | W* -> wedge^(n-1) W, q maps to iota_q z | The classical enclosing space is applied to z=j_n f; the inherited support-gap calculation is retained. |

For singular rank r<n the stabilizer includes an orthogonal nondegenerate factor, GL(rad q) and radical shears. The kernel is `D tensor Sym^n(rad q)`, dimension binom(2n-r-1,n). The new radical-square proof does not require branching for this nonreductive group. At full rank the kernel is zero for odd n and `D tensor C rho^(n/2)` for even n. The old proof retains full O(q), including the n=2 reflection.

The exact identity `kappa* kappa = 2^(1-n)/[n(n-1)] [E(E+n-2)-rho Delta_q]` gives the positive harmonic eigenvalues, multiplicities, sharp condition number and Moore–Penrose inverse. Norm statements assume q=I in a specified real orthonormal frame and complexification. They are not O(n,C)-invariant bounds under arbitrary coordinate changes. Constants are proved by differentiation and adjoints, not inferred from a shared representation.

### Fresh versus inherited source verification

De Bie–Eelbode–Roels, *The harmonic transvector algebra in two vector variables*, J. Algebra 473 (2017), 247–282, arXiv:1510.06566v3, https://arxiv.org/pdf/1510.06566: Definition 6.1/Lemma 6.2 on Fischer products and adjoints, and the two-variable harmonic decomposition, were consulted. They do not themselves identify this exterior composite. Our normalization is checked directly on powers and wedges.

The exact Howe Theorem 9/section 4(a), Olive Definition 2.6/Remark 2.7, Piola and skew-flattening source records are preserved in `LITERATURE_AUDIT_V141.md`, `LITERATURE_AUDIT_V138.md`, and `parts/19-operator-comparison.tex`. This revision does not label every inherited access record a fresh full-text reading. The mixed identity and direct calculation supply the claimed constants without an unverified attribution of that identity to those sources.

This comparison identifies equations, groups, ranks and source summands. It does not establish that no equivalent formula has appeared elsewhere; exhaustive expert priority clearance remains uncertified.

## Ballico 1993 — six axes still requiring complete text

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102. Publisher contents: https://onlinelibrary.wiley.com/toc/15222616/1993/163/1. Publisher PDF/epdf and institutional attempts did not supply complete text. A bibliographic or first-page record is not a theorem-level comparison. No purchase, author contact or interlibrary request was made.

| Requested axis | Present exact object | Ballico comparison |
|---|---|---|
| Parameter space | Pencil and relative socle Grassmannians | Complete text not obtained; unverified |
| Scheme versus reduction | Literal Fitting/minor ideal, fixed reduced Schubert support | Unverified |
| Varied map | Actual multiplication in the cube-zero algebra | Unverified |
| Infinitesimal structure | Ideal-adic neighbourhood, first relation, normal cone, determinant colon | Unverified |
| Families/base change | Closed immersion and actual universal family under arbitrary complex base change | Unverified |
| Inverse conclusion | Unmarked finite-pencil classification, spectral sheaf, marked incidence and Betti readout | Unverified |

No theorem numbers or hypotheses are assigned to unread text. Neither anticipation nor nonanticipation is claimed. B140.2 is explicitly open, not a weakening of the mathematical theorems or a global stop decision.
