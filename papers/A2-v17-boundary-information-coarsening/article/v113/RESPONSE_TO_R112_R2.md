# Response to the second independent referee report on A2 v112

Controlling report: `reviews/a2-v112-independent-harsh-top4-r2-2026-09-22/REFEREE_REPORT.md` at `66220b85960a5a50db15342ccfacfbf1395bca88`.

The revision is offered for renewed independent mathematical review at the same intended level. The response does not infer publication suitability from the absence of a counterexample, a successful build, or finite diagnostics. All substantive new claims have theorem statements and written proofs in the manuscript.

## 1. Provenance and actual revision material

The report correctly distinguished the previous report-only v113 branch names from an actual v113 manuscript. This branch begins from the controlling second-review commit and adds a principal `article/v113/paper.tex`, complete sources, a point-by-point response and source-bound verification. No earlier manuscript, review branch or main branch is changed. The additions-only verifier checks the entire baseline diff, not just selected manuscripts.

## 2. A structural layer rather than another rank count — report §§4, 6, 9

Theorem `thm:residual-tangent` gives an exact tangent sequence at every annihilator rank. Its compatibility space is the annihilator of the radical product span `sum W_nu^2`; the individual plane derivatives are solved by explicit dual frames. This is the invariant mechanism behind the rank-two residual wall, and it is not restricted to generic points or stable dimensions.

Proposition `prop:all-corank-schur` gives an exact scheme presentation at every multiplication corank. It explicitly does not identify a tangent cone merely with minors of a linearized matrix.

Theorem `thm:higher-phase` goes beyond quadratic products: for every symmetric power it classifies the two-point annihilator sectors. Their number is `(m^(L-1)+gcd(m,2)^(L-1))/2`, because support interchange acts by inversion after cyclic phase normalization. Theorem `thm:higher-residual` gives the corresponding residual conormal formula. This is a higher-product sector theorem, not an unsupported global higher-product component theorem.

## 3. Removal of the stable restriction — report §§4, 6.6, 9.4

Theorem `thm:all-dimension` covers the complete original domain `4 <= c < k`, with sufficient product capacity. Lemma `lem:all-ties` proves an exhaustive analytic equality classification, not a conclusion drawn from a finite search.

The five exceptional triples `(c,k,L)` are `(5,7,1)`, `(5,8,1)`, `(6,10,1)`, `(6,11,1)`, `(7,13,1)`. Their generic annihilator ranks are respectively `4,6,8,10,12`. In each case the plane contains the whole radical and becomes maximal isotropic in the nondegenerate quotient. Orientation monodromy joins the two geometric orthogonal families. The even full-rank case `(7,14,1)` is treated separately and is not silently declared geometrically connected.

The expected-codimension assertions now concern the entire scheme in this full range. The excess assertion lists every maximal-dimensional component, including the additional `(5,7,1)` component. Its existence and corank one are proved by the explicit subspace `span(1,t,g,tg,t^2 g)` and twelve products of distinct degrees. The boundary case `k=c+1` is handled by multiplication of the full residual binary space, not by applying a strict-subseries theorem outside its domain.

## 4. Wall geometry — report §§5.1, 9.8, 12A

Proposition `prop:residual-dominance` constructs the residual morphism and proves that its fibres are affine spaces of dimension `L(k-c-1)`. Thus independence of the residual planes is established, rather than assumed.

Corollary `cor:residual-singularity` identifies singularity on the split rank-two, multiplication-corank-one open stratum exactly with failure of the residual map. The tangent excess equals its residual cokernel dimension.

Theorem `thm:wall-node` proves that, in the stated stable wall range, the pullback residual determinant is an irreducible reduced divisor with a nonempty dense ordinary-double-crossing open set. The proof establishes original multiplication corank one by varying the lifts, identifies the normal derivative determinant with the residual determinant, and eliminates equations analytically. The resulting completed local ring is `C[[t_1,...,t_(d-1),u,v]]/(uv)`; the analytic equation is `uv=0`. The two branches are the signed component and the nondegenerate component. Their intersection has codimension one in each branch. Tangent cone, normalization, conductor and seminormality are computed from this ring.

This is not a claim that every higher-corank or colliding-support intersection is a node. Those boundary strata are not replaced by the dense open normal form.

## 5. Signed incidence intersections and excess scheme structure — report §§5.1–5.2, 6.4

Theorem `thm:signed-normalization` gives the normalization over the split rank-two base using its natural double cover. Pairwise and higher intersections with a common labelled annihilator are exactly products of Grassmannians in the radical at disagreeing contacts and in a hyperplane at the remaining contacts. Their dimension is `M-b-c|J|`.

Proposition `prop:rank-two-fibre` computes the full fixed-annihilator isotropy fibre at a plane in the radical. Its nilradical is a square-zero copy of `wedge^2 C^c`, annihilated by the origin ideal. The two minimal primes and the embedded origin prime are explicitly identified. This is genuine nonreduced fibre information, but it is not misreported as an embedded prime of the global reduced expected-codimension scheme.

The general global excess scheme's smaller components and all associated primes have not been classified by this revision. The exact Schur presentation and the full rank-two fibre calculation are the proved statements, rather than an unsupported blanket assertion. The corresponding scope boundary is stated alongside the main theorem.

## 6. The previously compressed proof transitions — report §§6.1–6.5, 9.2, 9.5–9.9

`prop:incidence-components` isolates the finite-stratification and projection argument. Its zero-dimensional-fibre step uses that a nonempty open subset of a positive-dimensional projective annihilator space cannot be zero-dimensional. The exceptional rank is the largest feasible isotropic rank, making the necessary rank condition open.

`prop:residual-dominance` supplies the missing residual-map dominance and fibre calculation. The proof of `thm:residual-tangent` solves mixed and square equations independently for every contact.

`prop:expected-grade` and `prop:generic-reducedness` separately establish expected height/grade, Eagon–Northcott perfection, Cohen–Macaulayness, absence of embedded primes, and reducedness from generic reducedness. The dual-map convention is explicit in `eq:all-dimension-cycle`.

The exact square-to-rectangular Hankel ideal identification is displayed in `01b-structural-overview.tex` with its common polynomial ring and indexed matrices. The retained proof of `lem:hankel-strata` supplies dimensions and the exact-rank open stratum. Orthogonal-fibre irreducibility and orientation monodromy are treated in `lem:orientation-incidences` rather than assuming every maximal orthogonal fibre is connected.

## 7. Conditioning and the statistical connection — report §§5.3, 8, 10

The new double-crossing calculation yields `cor:node-tail`: the least multiplication singular value is locally comparable to `sqrt(|z|^2+u^2 v^2)`, and a bounded positive density gives the local law `epsilon^a log(1/epsilon)`. This uses the newly proved singularity rather than merely applying a smooth tube formula.

The result is local and conditional on a real split crossing and a specified design density. It is not promoted to a global random-loading law. The manuscript also avoids identifying an unwhitened multiplication singular value with Fisher information in the exact compressed-score experiment, whose covariance changes with the compression.

The complete statistical arguments are retained in the appendices. Proposition `prop:poisson-constants` supplies an explicit uniform `N_0` and an explicit `L^1` constant for the jittered Poisson comparison. Definition `def:nuisance-invariant` makes the Gaussian nuisance-translation invariant precise. No finite-precision result, cone restriction, root-scale result, or estimation complement has been removed.

## 8. Literature and priority — report §§7, 12F

The bibliography now includes Ballico 1993 with its verified publisher metadata and DOI. Accessible primary sources and exact dependencies are recorded in `LITERATURE_AUDIT.md`. Full-text requests for Ballico 1993 did not provide its theorem text in this environment. Accordingly we do not claim to have completed that theorem-by-theorem comparison or certified exhaustive priority. This portion of the referee's request remains unverified, not fictitiously closed.

The new theorems specify their objects and scope: varying proper binary subseries, independent within-contact products, exceptional isotropic incidences, residual local equations and dihedral sectors. Classical secant obstruction, Hankel determinantal facts, determinantal resolutions and cycle formulas remain attributed to their sources.

## 9. Organization, retention and review status

The principal mathematical sequence is now: exact contact setup; full-range codimension; residual tangent calculus; all-dimension components; signed and wall geometry; higher products; native realization. The earlier stable theorem and the full statistical development remain available as appendices. All six inherited mathematical part files are preserved byte-for-byte, and inherited labels and bibliography keys are checked for retention.

The source-bound receipt reports compilation and diagnostic results only after actual execution. New proofs, especially orientation descent and the wall normal-form argument, are specifically identified for independent referee scrutiny. The revision is not automatically merged, submitted to a journal, or labelled accepted.
