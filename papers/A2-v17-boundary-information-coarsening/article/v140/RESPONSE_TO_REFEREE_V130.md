# Response to the A2 revision-130 referee report

Revision 131 — 23 September 2026

Controlling report: `reviews/a2-v130-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, review commit `57c70a882150cc6e44d85ad6f68043b7327d8a10`.
Reviewed manuscript: `472200a5373ce2adc6dacf8d211f02d765ff62f2`, source `article/v129`.
New branch: `revision/a2-v131-relative-primary-filtrations-2026-09-23`.
New self-contained manuscript: `papers/A2-v17-boundary-information-coarsening/article/v131/geometry.tex`.

The report is an owner-requested AI-assisted external-referee-style assessment, not a journal-issued report. This response records mathematical changes supplied for renewed scrutiny. A successful compilation or an exact finite computation does not certify a structural theorem or predict a journal decision.

## E130.1 — exact exhaustion of geometric associated points

The old proof based on an undefined adapted affine cover and the fixed-open containment statement of Stacks 05KR is replaced, not merely supplemented with another citation.

`parts/09d-relative-primary-filtrations.tex`, Proposition `prop:relative-primary-models`, starts with an actual primary decomposition on the geometric generic fibre. For each primary quotient Q with prime p it uses the annihilator filtration F_j=(0:Q p^j). Its graded quotients are p-annihilated torsion-free modules over A/p, and therefore embed in finite free modules over A/p. These embeddings, the filtration sequences, the diagonal injection M into the sum of the primary quotients, the quotient maps, and an associated-element injection A/p into M for every prime form a finite diagram. All cokernels needed for preservation of injections are flattened.

On each geometric fibre the diagonal injection proves Ass(M) is contained in the listed primes, including exclusion of additional embedded points. The associated-element injections prove the reverse inclusion. Noncontainment witnesses keep the primes distinct and their containment poset fixed. Thus actual irredundant primary decompositions, not only supports, persist on finite splitting covers. The packet lemma then handles affine-chart closures, field extensions, descent of conjugate packets, and Noetherian induction. Chosen primary components are not claimed to be canonical or individually descended.

## E130.2 — a coherent relative torsion module

Proposition `prop:no-new-packet-torsion` chooses T=(0:M p^n)=H^0_p(M) on the split generic fibre. The quotient Q=M/T has no p-power torsion. Prime avoidance gives h in p acting injectively on Q. The proof spreads p^nT=0, the exact sequence defining Q, and multiplication by h; flattening Q and coker(h) makes both injections universal. On any subsequent fibre an additional p-power torsion element would give an h-power torsion element in Q, which is impossible. This proves equality with the full fibrewise torsion, not just inclusion of a spread-out submodule.

The finite p-power filtration of T is then made compatible with base change. Explicit local free presentations of its graded quotients, together with nonvanishing witnesses on packet fibres, identify their generic ranks with the summands of the required local length. The collision example x^2=x(y^2-t)=0 illustrates why the refinement is necessary.

## M130.1 — the grading and multiplication maps

The universal target vector space is E, leaving the base notation unambiguous. The revised corollary uses A=O_U[t_ij] with coefficient degree zero and matrix-entry degree one. It defines M_q and L_j=M_{j-1}(-ej), and names the finite family of balanced A-linear maps L_i tensor_A L_j -> L_{i+j}, i+j<=N. They are the canonical quotient maps. Every degree component of a finite graded flat module is finite locally free, so the already obtained whole-module flatness fixes all Hilbert-function values without infinitely many refinements. Further prescribed coefficient-degree maps are explicitly a finite additional family.

The ungraded theorem no longer asserts an unspecified Hilbert polynomial or numerical rank. The graded conclusion is derived separately. Colons are re-formed on each stratum, and arbitrary base change means base change within that final stratum, not across different strata.

## Section 10 — the decisive Pieri coefficient

The old coefficient-one straightening assertion is replaced by an exact Fischer projection. For p=[123|123]^4 x_44^4 and D=(det X)^4, the determinant monomials using only that block and x_44 are exactly p. Thus <p,D>=<p,p>>0. The exact values are 24,883,200 and 870,912,000, giving projection p -> D/35. Right-GL ideal stability, semisimplicity, and the nondegenerate multiplicity-one pairing with the specific nonzero Jacobian component are retained. The new script checks these integer polynomial pairings; the structural representation argument remains a written proof.

## S130 — a sharper nonformal global consequence

Theorem `thm:sharp-global-jacobian-depth` observes that the corank-four identity is a polynomial identity on the entire 4x4 matrix space. Restricting it to X=I_H direct-sum T gives d^4 in J on every Schur chart. Hence Nhat^5=0 globally on G_4^circ, and the inherited d^3 exclusion gives exact index five at both coranks three and four. The previous five-or-six alternative on the smooth Jacobian open is eliminated, not restated as a finiteness assertion.

Some ambient coefficient-space rows have index six. They are preserved. Proposition `prop:smooth-web-rank-admissibility` explains the apparent conflict: smoothness forces a>=2 and basepoint freeness forces a+b>=5 at corank two. The full ambient tables and their exact computations are not all strata of G_4^circ.

For proper quotient-induced symmetric powers the manuscript also gives J=P^a, (J:d^q)=P^max(a-q,0), dJ=(d) intersection P^(a+1), a sharp exponent and closed local-length formulas. The maximal-minor equality is explicitly attributed to Bruns--Vasconcelos (2003), Theorem 1(2). This is an explicit application and primary calculation, not a claim to have discovered that classical identity.

## Higher-corank geometry and cross-corank specialization

Theorem `thm:global-minimal-supports` identifies the unique minimal supports of the first two layers on the full matrix space: the Jacobian incidence image Z_R and the rank-two determinantal variety D_2. Their generic lengths are one (for the second, on the inherited dense simple-contact open). A smooth proper birational incidence resolution has fibre Y_R intersected with the projective space of hyperplanes containing the matrix image. Its generic rank-two, rank-one and zero fibres are four contact points, a genus-three plane quartic and the K3 surface.

Theorem `thm:cross-corank-incidence` constructs a Grassmannian graph family with M(u,v)=diag(u,v,0,0). The pulled-back incidence family has equations u alpha_1=v alpha_2=0, with the exact reduced intersection (u,v) intersection (u,alpha_2) intersection (alpha_1,v) intersection (alpha_1,alpha_2). The last factor splits into four contact sections, giving seven components and no embedded component. Its fibre Hilbert polynomials are 4, 4n-2 and 2n^2+2. This is an actual nonflat cross-stratum family, not an invocation of within-stratum base change.

The intrinsic graded residue-field algebras along the same family are k[epsilon]/epsilon^3 on the corank-two torus and k[epsilon]/epsilon^5 on the corank-three axes and corank-four origin. The paper explicitly distinguishes pullback of this already formed graded algebra from formation of a nilradical after pullback, which would lose transverse data.

These results materially advance higher-corank geometry and meet the requested direction of a global specialization theorem. They do NOT supply a complete generic list of all embedded transverse primes and multiplicities of W_3 and W_4. The issue matrix retains that remaining distinction. The seven-component decomposition is of the incidence family, not of the entire transverse failure scheme.

## S130 inverse question

The polarized K3 reconstruction and all its proofs are preserved. No generic injectivity or recovery of the original relation web is claimed. This revision advances the report's alternative global-boundary direction. The unresolved finite web/Torelli ambiguity is not relabelled as solved by the incidence construction.

## M130.2 — primary terminology

The revised definition distinguishes the intrinsic primary signature, actual noncanonical primary decompositions on splitting covers, the explicit corank-two tables, the quotient-induced primary law, and the incidence-family decomposition. The full universal stratification is not advertised as an effective classification of all primary components.

## M130.3 — literature boundary

The publisher metadata for Ballico (1993), Math. Nachr. 163, 5-13, DOI 10.1002/mana.19931630102, was checked. Attempts to obtain the publisher's full article/PDF did not yield readable full text. A theorem-by-theorem full-text comparison has therefore NOT been completed, and no nonanticipation claim is made. The existing historical discussion is retained. Bruns--Vasconcelos and the Cayley identity are now explicitly credited where used. The classical Reye moduli count remains distinguished from the manuscript's inverse theorem.

## Architecture, preservation, and evidence

The final source path, title-page version and receipt are all v131. The assembly script reads the reviewed v130 source by immutable commit, copies all inherited mathematical sections and checks, and changes only explicitly identified proof, statement and presentation passages. New technical arguments are included in the article, not left solely in this response. The provenance manifest records old blob hashes and the hashes of every assembled source file. The old v129 source tree and every review file remain unchanged.

The build executes the five inherited exact scripts and a new independent script for the Fischer pairing, a symmetric-square maximal-minor identity, the squarefree incidence intersection, and length formulas. It compiles the entire article three times and records source hashes and actual results. Structural proofs are explicitly listed as source-level mathematics requiring referee verification. No automatic issue closure or top-four acceptance claim is inferred from a green build.
