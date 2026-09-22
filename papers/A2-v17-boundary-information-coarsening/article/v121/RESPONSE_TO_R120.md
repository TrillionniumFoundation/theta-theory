# Response to the independent v120 referee report

**Manuscript:** Determinantal flags and primary boundaries in multiplication failure  
**Revision:** v121, 2026-09-22  
**Controlling report:** `reviews/a2-v120-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md`  
**Review commit:** `b20eafa006fd3abe650ad7478542d637327b1094`

We thank the referee for distinguishing the established v120 repairs from the remaining questions of scope, priority, and global consequence. This revision does not replace a primary scheme by its support, remove the extreme-corank conclusions already proved, or present finite diagnostics as general mathematical evidence. It adds a uniform primary-flag theorem and a non-isotrivial elliptic boundary family, and formalizes descent. The actual journal object is the geometry edition; the complete edition retains the complementary material.

One documentary requirement remains unmet: we have not obtained the complete Ballico 1993 article. E120.1 is explicitly open. The statements below are a substantive response for further referee assessment, not a declaration that journal significance or exhaustive priority has been certified.

## E120.1 — Complete Ballico 1993 comparison

**Status: not closed.** We checked the publisher's bibliographic/reference page for DOI `10.1002/mana.19931630102`, attempted its full-text PDF/ePDF routes, and searched the available file library for the exact title and DOI. The library results were earlier A2 documents citing Ballico, not the article. No readable complete text was obtained.

We therefore cannot responsibly fill in Ballico's theorem hypotheses or conclusions, and do not infer them from the title, reference list, or the 1996 follow-up. `LITERATURE_AUDIT.md` records all nine requested comparison dimensions and the corresponding precise v121 theorem objects; the Ballico side is marked unverified throughout. The main article explicitly makes no anticipation or nonanticipation claim based on those metadata.

We did obtain and inspect the primary texts needed for the new argument: Bruns–Römer–Wiebe (2005), Theorem 3.5(c), for generic determinantal normality/primality, and Artebani–Dolgachev (2009), Section 2, equations (4)–(5), for the Hesse Weierstrass coefficients. The new weighted identity is proved in the manuscript; it is not used to claim a new foundational theorem about generic determinantal rings or Hesse cubics.

## E120.2 — A structural theorem with genuine moduli

**Response: a uniform primary classification in arbitrary embedding dimension on an explicit universal open, plus a fixed-tensor family with genuine elliptic moduli.**

The new main algebraic result is Theorem `thm:weighted-primary`. For a generic q-by-p matrix A, with p at least q, put

\[
 F=t\sum_{i=0}^q t^{q-i}I_i(A),\qquad P_j=(t,I_j(A)).
\]

We prove the irredundant primary decomposition

\[
 F=(t)\cap\bigcap_{j=1}^q P_j^{(q-j+2)}.
\]

The proof proceeds coefficient by coefficient in t. At coefficient t^u, the component with j=q+1-u forces membership in I_j(A), and Schur-complement symbolic orders imply all remaining conditions. To witness irredundancy of P_j's component we use

\[
 t^{q-j+1}d_{j-1}^{\,2},
\]

where d_(j-1) is a nonzero (j-1)-minor and d_0=1. A squared q-minor witnesses the determinant component. This is a proof for every matrix size, not a table of finite ideal checks.

Theorem `thm:universal-primary-flag` applies this identity to the universal surjective quadratic tensor for Hilbert function (1,e,q), for q <= binom(e,2). On the projection-corank-one divisor write H for the image hyperplane, and impose gamma(HV)=S. The quadratic matrix reduces to [A,tB,t^2 c], and the surjectivity of [A,B] proves the exact column-module equality with [A,tI_q]. Together with the linear determinant factor this identifies the **full** multiplication ideal with F.

The resulting global primary supports are

\[
 Z_j=\{\det M=0,\ \operatorname{rank}(\gamma|_{\operatorname{Sym}^2H})<j\},
 \quad \max(1,q-e+2)\le j\le q.
\]

The theorem gives every associated point on that open, the symbolic exponent q-j+2 of the specified embedded primary representative, the codimension, normality, generic divisor multiplicity one, and the exact local nilradical index q-a+1 at restricted rank a. Its maximal index is min(q,e-1)+1. Conductor kernels are computed by an explicit companion map of the same tensor in Proposition `prop:universal-conductor-flag`.

**Exact scope.** This is a universal corank-one, first-order-spanning theorem. It is not a complete primary decomposition on all projection-corank strata of every cube-zero algebra. It is also not claimed that a generic primary decomposition survives arbitrary substitution. The manuscript keeps these distinctions explicit, rather than extending a theorem beyond its proof. The old whole-Grassmannian (1,2,2) classification, including its extreme-corank point and nilradical index four, is retained without weakening.

The `(1,3,3)` family in Theorem `thm:elliptic-boundary` supplies genuine moduli after fixing the tensor: it is not an orbit-reparametrization of the two binary-quadratic algebras. Its restriction degeneracy curve has a nonconstant j-invariant, and different j-values imply nonisomorphic local algebras. Its primary decomposition is separately proved by a smooth two-parameter local calculation.

## E120.3 — A global consequence beyond transporting a fixed finite example

**Response: global resolutions for the universal embedded supports and a flat, non-isotrivial elliptic-boundary family.**

Theorem `thm:flag-resolution` constructs a smooth incidence space over each Z_j by adjoining a (j-1)-dimensional subspace T of the quadratic layer containing gamma(Sym^2 H). The incidence is a nonempty open in a vector bundle over a product of Grassmannians and a projective space. Its map to Z_j is projective and birational. Over restriction rank r its scheme-theoretic fibre is

\[
 \operatorname{Gr}(j-1-r,q-r).
\]

This is a theorem about the global geometry of the actual embedded supports over the tensor parameter space, not merely a Fitting-ideal pullback to high-degree sections.

Theorem `thm:elliptic-boundary` studies

\[
 B_\lambda=\mathbb C[x,y,z]/((x,y,z)^3,
 xy-\lambda z^2,yz-\lambda x^2,zx-\lambda y^2).
\]

On the explicitly stated nonempty parameter open and on the **entire** projection-corank-at-most-one open U in Gr(3,6), the full failure scheme has

\[
 \mathcal I_{D_\lambda}=\mathcal I_\Delta\cap\mathcal I_{E_\lambda}^{2}
 =\mathcal I_\Delta\mathcal I_{E_\lambda}.
\]

The reduced divisor Delta is fixed. The smooth embedded support E_lambda is a rank-four vector bundle over C_lambda times P^2, where

\[
 C_\lambda:\quad \lambda(a^3+b^3+c^3)+(1-4\lambda^3)abc=0.
\]

It follows that the nilradical is exactly the nonzero square-zero module O_(E_lambda)(-Delta), and that a natural smooth projective compactification of E_lambda has Albanese C_lambda. This gives a global invariant of the embedded geometry which is lost by retaining only the fixed reduced divisor.

The conductor is the same rank-one kernel Lambda throughout this corank-one boundary. Thus the new structural description does not falsely identify numerical conductor rank with all primary data; it records the additional quadratic restriction flag which carries the moduli.

Corollary `cor:elliptic-family` proves flatness of the family of full failure schemes by the exact nilradical sequence and flatness of both outer terms. This is a proved property of this family, not an extrapolation from base change of Fitting ideals.

## E120.4 — Formal frame-to-Grassmannian descent

**Response: Lemma `lem:frame-primary-descent` and Corollary `cor:loewy-primary-descent`.**

The proof works on the actual Zariski trivializations of the GL-frame torsor: A -> A[z_ij,det(z)^(-1)]. Faithful flatness contracts ideal equalities, flatness preserves finite intersections, and contraction of a primary ideal establishes primarity downstairs. Irredundancy is equivalent upstairs and downstairs. The associated-point assertion is then obtained from the irredundant decomposition on each affine chart, not from the blanket phrase that regular fibres introduce no new associated primes.

For the (1,2,2) theorem the factor surface ideals are defined as zero loci of K -> V/L. Their sum is the point ideal of K -> V. The determinant ideal is intrinsic, the residual J is the ideal quotient by its square, and Q_0 and Q_* are specified sums and products of these global ideals. Each associated stratum meets the full-frame open by taking the lower frame block to be the identity. This proves the global intersection, irredundancy, and exactly the claimed associated points.

The application has no circular dependency: it uses only the affine equalities already proved in `thm:loewy-primary`; that theorem then invokes the descent corollary for its global conclusion.

## E120.5 — Titles and scope

**Response: the retained theorem is now titled “Complete primary decomposition for Hilbert function (1,2,2).”** Its equations, power formula, associated primes, and nilradical index are unchanged.

The new abstract and opening roadmap distinguish general finite locally free algebras, split cube-zero algebras, the universal first-order-spanning corank-one open, and the full (1,2,2) class. The `(1,3,3)` theorem states its parameter open and its Grassmannian open in the theorem. Neither the title nor the abstract calls the new open-stratum theorem a classification of all cube-zero primary geometry.

## E120.6 — The actual journal manuscript

**Response: `geometry.tex` / `geometry.pdf` is explicitly the principal journal object.** It begins with the structural primary theorem and the elliptic consequence. It also retains the finite-algebra and global-conductor framework and every original core section. The prior introduction is retained, with its heading changed to “Finite-algebra and global conductor framework.”

`paper.tex` / `paper.pdf` remains the complete archival/companion object and includes all complementary geometry and statistical proofs. The applications edition remains available. Historical v120 and prior versions remain unchanged in the new branch. A preservation check confirms every prior theorem label and every old core input is still present; the only edited old mathematical part is the explicit descent/title repair, in addition to the introduction's heading.

## E120.7 — The program label

**Response: the journal paper is presented on its own mathematical merits.** A2 is repository lineage. No unchecked A1 input or downstream dependency is offered as evidence of significance. `DEPENDENCY_MAP.md` lists the actual theorem interfaces and source inputs. The new global consequence is proved inside this paper.

## Verification and handoff

All inherited v118–v120 algebraic regressions are rerun. New finite checks independently verify the q=p=2 weighted-primary intersection, the elliptic restriction determinant, the Hesse j normalization, nonconstancy, a parameter in the admissible open, and the local ideal intersection `(t) intersect (t,f)^2 = (t^2,tf)`. These tests guard against transcription errors. The general results depend on the written proofs, not the tests.

The source-bound build creates the geometry, complete, and applications PDFs with resolved references and source/product hashes. The build itself does not run an authoring script. Source publication and product publication are separate commits on the new revision branch; no default-branch or other-paper mutation is intended.

The next referee should assess the structural theorem and the global elliptic consequence at their exact scope. The documentary Ballico comparison remains to be completed from readable full text; neither a successful build nor this new mathematics is presented as a substitute for that requirement.
