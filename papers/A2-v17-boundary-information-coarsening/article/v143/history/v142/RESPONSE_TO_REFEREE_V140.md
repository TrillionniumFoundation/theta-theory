# Response to the independent A2 v140 referee report

Revision 141 — 23 September 2026. Controlling report: `reviews/a2-v140-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `17e039fe55fc0d060b443d486421d937f637439a`. Reviewed v140 head: `6bac73f9ebcaadcfa135e4960de19c93323bbfd7`. Native predecessor restoration: `bf0d9be9e2624058d24a57c48b19ec4c38105c1f`, successful run `35866863687`.

The revision preserves the previous mathematics and its hypotheses. It adds a universal family theorem, scheme-theoretic spectral readout, and a separate constructive theorem proving the all-real reciprocal likelihood assertion formulated by Fevola–Mandelshtam–Sturmfels. It does not equate a successful build with formal proof, historical priority, or a journal's editorial decision.

## B140.1 — Native manuscript and source-bound build

The index-dependent restoration check has been replaced by verification of the authentic v138 archive and every entry of its assembled-source manifest. The complete v138–v140 native manuscript trees are now committed on the new revision branch, without changing the reviewed branch. Revision 141 has native LaTeX sources, executable checks, and a self-contained build entry point. The active source manifest, nondeletion map, and final build receipt identify exactly which source was compiled. The publishing workflow commits sources before building, and the final verification is read-only on a commit already containing the native submission object. Historical transports remain history, not the referee's reading route.

The predecessor's native source hashes are checked before assembling v141. A missing or altered predecessor file is an error; the assembler neither silently replaces conflicts nor treats Git-index membership as byte provenance. Existing review reports and other paper branches are not modified.

## B140.2 — Ballico 1993

**Not represented as closed.** The publisher record was checked again. The complete article was not obtained through the available lawful routes. `LITERATURE_AUDIT_V141.md` records all six requested axes and distinguishes our proved statements from unknown contents of that paper. Neither the new likelihood theorem nor the successful native build supplies the missing historical comparison. No unperformed interlibrary request, author contact, purchase, or expert certification is claimed.

The manuscript retains its reconstruction theorems without adding genericity assumptions. It also retains the explicit documentary qualification rather than replacing it with an unsupported nonanticipation statement.

## B140.3 — Exact contraction operator

The operator-level comparison now records the source, target, normalization, stabilizer, singular-rank kernel, and even-dimensional exceptional line of the specific map `iota_q j_n`. The full-rank harmonic decomposition, binary transvectant, unrestricted exterior-contraction kernel, Piola cancellation, and skew-flattening support bound are assigned to their appropriate classical roles. The manuscript now also writes the exact intersection problem with `wedge^n ker(q)`, explaining why knowing the ambient exterior-contraction kernel is not the desired restricted calculation.

This is a map-specific comparison with the inspected sources, not an exhaustive expert priority clearance. That broader documentary judgment remains unverified. The all-ranks theorem and all its proof cases are retained in full and are not relabelled as consequences of the unrelated Laplacian kernel formula.

## B140.4 — An external theorem, not only an interpreted invariant

`thm:totally-real-reciprocal-likelihood` addresses the assertion stated as Conjecture 4.5 in *Pencils of quadrics: old and new*, arXiv:2009.04334v2, p. 10, equation (14). For **every** definite real symmetric pencil, with **arbitrary** eigenvalue multiplicities and `r` distinct eigenvalues, it gives an explicit nonempty Euclidean open set of real data for which all `2r-3` complex reciprocal-likelihood critical points are real and nondegenerate.

Write the distinct eigenvalues as `alpha_1 < ... < alpha_r`, put `D(t)=prod(t-alpha_i)`, and choose a degree `r-1` polynomial `Q` whose roots all lie to the right of `alpha_r`. The data are the residues `sigma_i=Q(alpha_i)/D'(alpha_i)`. If `m_i` are the multiplicities and `n=sum(m_i)`, elimination gives

`F=n D Q' - Q sum_i (n-m_i) D/(t-alpha_i)`.

Its leading terms cancel. Sign changes between consecutive `alpha_i` and between consecutive roots of `Q` produce `2r-3` distinct real roots, exhausting its degree. The proof explicitly establishes coprimality with denominators, excludes the omitted axis `x=0`, computes the Hessian Schur complement, and obtains openness by the residue-interpolation isomorphism. It does **not** assume the complex ML-degree count. Thus it is not a composition of the internal Torelli theorem with classical pencil classification.

The source's assertion permits unrestricted real data, and its Example 4.6 itself uses mixed signs. The revision does not claim positivity of the data matrix, that all critical points lie in the positive definite cone, or that they are all statistical maxima. The complex unmarked reconstruction theorem is not claimed to reconstruct a real structure. The assertion is proved here; first historical priority and the current journal-level significance judgment are not certified.

The geometric extension is also uniform: `thm:universal-finite-neighbourhood` realizes the entire pencil Grassmannian by actual flat projective neighbourhood families. `thm:relative-spectral-readout` recovers spectral Fitting incidence schemes, including nonreduced base changes. All classical Segre-stratum closures and their intersections are transported through the relation-space immersion. The manuscript explicitly credits the classical closure order and identifies transport of closed subschemes as formal, instead of calling that transport a new classification.

## Requests 5 and 6 — Relative gluing and the two spectral lemmas

`thm:universal-finite-neighbourhood` constructs the global coefficient morphism

`det(V*) tensor det(U) tensor det(S*) tensor wedge^p Sym^2(U) -> Sym^d Hom(U,V)*`.

Its image is a split rank-`binom(N,2)` subbundle in every frame chart. Right frame changes transform the determinant and exterior factors equivariantly, so the ideals glue inside the actual graph neighbourhood. Quotienting by the `(d+1)`-st power of the zero-section ideal gives the actual ideal-adic family. This explicitly completes the relative step used in the v140 specialization.

`lem:spectral-sheaf-similarity` identifies the affine torsion sheaf with the finite `C[z]`-module on which `z` acts as `A^{-1}B`, with a fixed sign convention. `lem:artinian-polynomial-square-root` writes the truncated binomial square root in every local Artinian factor of the minimal polynomial and joins them by the Chinese remainder theorem. Nonsemisimple invertible matrices are included.

## Requests 7–9 — Scope and hierarchy

The qualifier **reduced rank loci** is retained throughout. Full spectral Fitting data change in the specialization; the reciprocal curves are not asserted to form a flat family. Sharpness at `d=n^2+2n-4` is uniform sharpness for all pencils, not a pointwise minimality assertion for every pair. No equivalence of unmarked moduli stacks, automorphism groups, or all infinitesimal deformations is asserted.

The introduction and abstract now have one main inverse-problem chain: intrinsic coefficient extraction, sharp finite reconstruction, and spectral geometry. The all-real likelihood theorem supplies a separately stated external consequence. The web/K3, contraction, hyperelliptic, boundary and polar results remain in their complete source and proof locations. Every inherited mathematical label remains reachable from the complete compilation. Changed predecessor files are preserved byte-for-byte under `history/v140/`; unchanged files are hash-checked.

## Evidence and next scrutiny

The two new exact scripts supplement, rather than replace, the fifteen inherited scripts. They check Artinian roots, nonsemisimple congruence, truncated spectral presentations, Fitting ideals over dual numbers, Jordan partitions, and 54 exact rational likelihood configurations (24 with independent Sturm interval counts). These are finite audits of written proofs. The controlling verification counts inherited/current labels, checks source hashes and archives, and inspects the three compiled PDFs for unresolved references, errors, and layout overflow. Exact counts and commit identifiers are in `evidence/BUILD_RECEIPT_V141.json`.

A fresh referee should scrutinize the new universal gluing and likelihood proofs directly and separately assess their significance. The Ballico full-text comparison and exhaustive contraction-priority clearance remain honestly distinguished from mathematical and build completion.
