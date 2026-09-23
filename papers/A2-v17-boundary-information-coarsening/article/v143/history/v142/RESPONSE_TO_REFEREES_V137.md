# Response to the report on A2 revision 137

**Intrinsic reconstruction from nonreduced failure schemes** — Qian Qi  
Revision 138 · 23 September 2026

Controlling report: `reviews/a2-v137-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `ba24a0b2d062897ee2d7a6b02add81c504fe0e71`. Reviewed native manuscript head: `d4f45624e91456ff135434a1236d8de2549ff0b9`. The report is owner-requested and AI-assisted, not represented as a journal-issued decision.

## The mathematical change

The central smooth-web theorem is unchanged in strength: it holds for **every** basepoint-free four-dimensional web with smooth Jacobian quartic. The polar-system theorem, all-dimensional support theorems, boundary results, and full technical supplement are retained. The new result is not a restriction of that theorem, a change of journal target, or an auxiliary coefficient-encoding replacement.

The original multiplication-failure construction is now treated for quadratic relation spaces

`R in Gr(r, Sym^2 V), dim V=n>=3, N=n(n+1)/2, 1<=r<N-n`.

The new automatic coefficient theorem derives the complete intrinsic normal-cone and Cauchy-coefficient structure from the actual multiplication matrix for every relation space in this Grassmannian. Its pencil specialization (`r=2`) reconstructs **every** quadratic pencil in every dimension `n>=3`, with no regularity, base-locus, or discriminant hypothesis. The abstract scheme comes with no supplied embedding, zero section, or tensor marking. This provides a second natural family from the same construction and an explicit application to classical discriminant fibres.

## B137.1 — Ballico 1993

The full article has still **not** been obtained. The requested six-axis theorem-level comparison is therefore not marked complete. The present session checked publisher full-text routes, title/DOI searches, and the user's Library. The Library results were prior A2 patches and responses, not the nine-page article; title-specific searches supplied no copy. An integration search did not provide an already connected institutional full-text route. None of these outcomes implies that the article cannot be obtained elsewhere.

`LITERATURE_AUDIT_V138.md` separates bibliographic identification, inherited first-page notes, and actual theorem text. Each of the six requested axes remains explicitly unverified against the complete 1993 source. The 1996 paper is not substituted for it. No invented theorem number, nonanticipation assertion, or negative novelty conclusion fills that gap. The mathematics has been strengthened independently; this is not presented as a substitute for the missing reading.

## B137.2 — A natural second family

Section `sec:natural-pencils` proves `thm:natural-pencil-reconstruction` for the **same** zeroth Fitting ideal of multiplication in `C + V + (Sym^2 V/R)`. No determinant block is appended to an unrelated evaluation map. Quadratic pencils, including singular pencils and their discriminant degenerations, are standard objects of projective geometry.

The proof first obtains the normal-cone ideal

`I = (det T) I_(N-r)(gamma Sym^2 T)`.

The degree-one ambient bundle, deepest base, determinant ideal line and residual ideal are intrinsic. The maximal-minor coefficient map is proved to have the exact Cauchy realization, not only the correct representation dimension. For two relations, `wedge^2 Sym^2 V = S_(3,1) V` is irreducible. Exterior duality then turns the recovered coefficient line into the whole Pluecker line of `R`. This is the decisive reason that **all pencils**, including the nonregular boundary, are recovered.

The original polar construction remains proved, but is no longer asked to carry the natural-geometric significance argument. Its heading and discussion describe coefficient reconstruction, without implying that its auxiliary invariant was previously a standard Torelli object.

## B137.3 — Deriving the criterion's hypotheses

The new `thm:automatic-quadratic-coefficients` proves the criterion's hypotheses for an entire Grassmannian family, rather than assuming them in a second example. The proof supplies, in order:

1. The actual scalar/linear/quadratic multiplication matrix and every maximal-minor factor.
2. The fixed Schubert reduction, its intrinsic deepest stratum `Gr(n,S)`, and the complete homogeneous normal-cone ideal.
3. The two relative rank-one ruling schemes; the nontriviality of the tautological ruling is proved by restriction to a Schubert line.
4. Determinant-line cancellation, with no chosen generator in the recovered data.
5. The universal multiplicity-free matrix-coefficient inclusion, nonzero on every diagonal Cauchy summand, and the resulting left lines under one common projective transformation.

Thus the structural theorem remains a useful criterion, now accompanied by a general geometric theorem showing when it applies automatically. For relation spaces with several Schur components, we do not silently assume that their separately projectivized lines recover relative scalars. The existing web recombination theorem addresses that issue; for pencils there is only one component.

## B137.4 — The external consequence

The paper now centers its external illustration on a precise classical loss of information: the determinant of a regular quadratic pencil retains the discriminant roots and their total multiplicities but can lose the partitions of their elementary divisors. This is the Weierstrass–Segre classification recalled by Fevola–Mandelshtam–Sturmfels, Theorem 1.1 and Corollary 2.1.

`cor:intrinsic-segre-data` shows that the abstract failure scheme recovers all root-labelled elementary divisors. The proof includes a self-contained simultaneous-congruence argument, including nonsemisimple self-adjoint matrices, while attributing the classification as classical.

`ex:same-discriminant-distinct-failure` supplies explicit symmetric pairs in every `n>=3`. Their determinant forms are, up to scalar,

`s^2 product_(i=3)^n (s+mu_i t)`.

At the unique double root their ranks are `n-2` and `n-1`, corresponding to partitions `(1,1)` and `(2)`. They are therefore inequivalent pencils, but have the same full discriminant and the same reduced failure scheme. The new theorem proves their **nonreduced** failure schemes are nonisomorphic. The example exhibits an actual ambiguity, not an unproved generic degree.

For `n=2g+2`, `g>=2`, `cor:hyperelliptic-failure-invariant` turns the classical simple-discriminant pencil correspondence into an injective invariant of smooth hyperelliptic curve classes with a fixed reduced scheme. The family has dimension `2g-1`. At the displayed boundary the discriminant double cover alone no longer distinguishes the pencils, whereas the failure scheme does.

This does not claim that classical pencil classification or hyperelliptic Torelli was an unsolved problem. The new conclusion concerns the abstract multiplication-failure invariant. For webs, the nine-dimensional generically finite K3 map is retained, but its generic degree is not asserted to exceed one. The manuscript no longer uses a hypothetical nontrivial K3 packet as its external significance evidence. Whether these theorems meet a particular journal's significance threshold remains an independent editorial judgment, not a property verified by computation.

## B137.5 — Exact operator comparison and attribution

Section `sec:operator-signatures` and the new literature audit add actual-map comparisons with Howe's classical invariant theory (Theorem 9 and Section 4(a)), Olive's transvectant and polarization conventions (Definition 2.6 and Remark 2.7), and the already cited plethysm, harmonic, Piola and exterior-support sources.

The revision explicitly identifies the binary Jacobian with the first transvectant and acknowledges the `n=2` contraction kernel as elementary exterior algebra. It does not claim that case or the orthogonal harmonic decomposition as new. It compares the source, target and nondegenerate kernels of quadratic apolar differentiation and the restricted exterior contraction: they are different maps with different kernels. The singular-radical shear calculation and the nonzero coefficients on positive harmonic summands are identified as the additional arguments relative to the inspected classical statements.

These are positive theorem-level comparisons, not a certificate that no equivalent result exists anywhere in the literature. The unanswered Ballico comparison is kept separate.

## Section 7 — Local clarifications

In `lem:rank-one-fano-scheme`, the identity `u wedge A(u)=0` is explicitly polarized to `u wedge A(v)+v wedge A(u)=0`; the text identifies it with the full bilinear linearization in characteristic zero. In `lem:full-orthogonal-harmonics`, the compact-real-to-full-complex implication is stated explicitly. The polar construction displays the literal two-row matrix, whose maximal minors are `delta f_i`. Reduced support identities are not strengthened into scheme-theoretic identities.

## Sections 8–10 — Presentation, preservation and evidence

The principal article presents the results and proofs without a revision-round banner; version information is kept in PDF metadata and the companion response. The supplement and complete manuscript remain available. No inherited mathematical label is removed. Every modified predecessor source is archived verbatim; the immutable v137 directory and all review records remain untouched.

The new exact script checks the exterior-square highest-weight orbit in five dimensions, every maximal minor in two actual multiplication charts, the same-discriminant pairs in six dimensions, and a nonsemisimple congruence correction. It runs alongside all twelve inherited scripts. The source-bound receipt distinguishes these finite identities and compilation checks from general structural proofs and historical priority. The branch publication receipt records execution only after it occurs.

The revision therefore supplies a natural all-pencil theorem, an automatic-family theorem, an explicit classical discriminant-fibre consequence, and the requested proof clarifications, while retaining the entire earlier mathematics. The full-text Ballico comparison remains the specific documentary item not completed by this revision.
