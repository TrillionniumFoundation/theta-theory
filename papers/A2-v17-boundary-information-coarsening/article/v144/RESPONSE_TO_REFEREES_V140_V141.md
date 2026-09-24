# Response to the v140 and v141 referee reports — revision 142

We thank the referee for distinguishing reviewability, correctness, historical comparison, and significance. Revision 142 adds an exact operator factorization, treats the whole fixed-discriminant/fixed-reduced-rank locus, and identifies the first relation with a standard graded Betti space. Every mathematical part of the latest native predecessor is retained. New mathematics is not used to erase unresolved documentary requests.

## Source chronology

The controlling review is `reviews/a2-v141-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `a10f8f1ea938e0ef8ce5a4aca4ee8e4a662ee84c`, assessing restoration head `bf0d9be9e2624058d24a57c48b19ec4c38105c1f`. Its statement that that head had no native v141 manuscript is correct for the reviewed state.

After the report, the revision branch acquired substantive native manuscript `8cd389f4048a1047be9aa8e8e4f642595175a555`. We inspected that source, its relative spectral section, totally real reciprocal likelihood theorem, response and literature audit. Revision 142 inherits this later state, not merely v140. The universal actual-neighbourhood theorem, scheme-theoretic spectral readout and proof of the assertion formulated as FMS Conjecture 4.5 are retained, not relabelled as new v142 contributions. Both the controlling review and later mathematical predecessor are in the new commit ancestry. Original branches are not rewritten.

## B141.1 and B140.1 — native reading objects

`article/v142/` has its own principal, supplement and complete LaTeX entry points, mathematical additions, response, issue matrix, bibliography extension, tests and build entry point. All inherited parts are native. No payload decoding or previous Actions artifact is needed to read or compile them. Version metadata identifies revision 142. Changed wrappers are archived under `history/v141/`; every inherited mathematical part remains byte-for-byte unchanged. The executed nondeletion receipt records the actual hashes and label counts. We do not retroactively claim that restoration-only v141 contained these additions.

## B140.2 — Ballico 1993

The complete 1993 article has not been obtained. The six axes in `LITERATURE_AUDIT_V142.md` give precise locations for the present results and explicitly unverified Ballico entries. Publisher PDF/epdf and institutional routes did not supply the theorem text. No theorem numbers or hypotheses are invented; neither anticipation nor nonanticipation is certified. This documentary item remains open. The hypotheses and conclusions of the paper are preserved rather than weakened because a source is inaccessible.

## B140.3 — an exact identification with classical operators

The new mixed identity, on `det(V) tensor Sym^n V`, is

`C_n (h wedge -) kappa_(n,q) = (4/n) D_(hq) - 2/[n(n-1)] h Delta_q`.

Its proof is a row-replacement determinant calculation on pure powers followed by polarization. It holds for every pair h,q and every rank. The domain, codomain, group actions, off-diagonal convention and constants are explicit in `parts/24-jacobian-casimir.tex`.

For singular q, a radical square first forces `Delta_q f=0`; varying h then forces `D_(hq)f=0`. Coordinate squares eliminate all nonradical variables. This independently proves the full singular-kernel formula without harmonic branching or shear descent. The old proof is retained.

At full rank, h=q^{-1} gives `2/[n(n-1)]` times the angular Casimir. The independently proved adjoint formula `j_n*=2^(-n) C_n`, in the specified degree-normalized Fischer/Hermitian products, yields

`kappa* kappa = 2^(1-n)/[n(n-1)] Casimir`.

The complete squared singular-value spectrum is `2^(1-n)m(m+n-2)/[n(n-1)]` on harmonic degree m=n,n-2,..., with exact multiplicities. It gives the odd/even kernel distinction, sharp condition number and explicit Moore–Penrose inverse. The comparison therefore identifies a precise composite under classical differential packaging, rather than arguing from different codomains.

The audit separates classical harmonic decomposition, binary transvectants, unrestricted exterior contraction, Fischer adjoints and exterior support, and distinguishes fresh source inspection from inherited access records. The exact composite and consequences are proved. Exhaustive priority across every equivalent historical formulation remains uncertified; computations do not replace that qualification.

## B140.4 — all fixed-data transitions and a standard Betti interpretation

Fix a nonsingular symmetric form A, a characteristic polynomial with root multiplicities m_i, and coranks c_i. The full orthogonal orbits are tuples of partitions of m_i into c_i parts; dimensions are explicit. Unmarked neighbourhood classes are tuples modulo the actual permutation image of the projective stabilizer of decorated roots. The possibly infinite stabilizer itself is not incorrectly called finite.

Every componentwise dominance transition, and only such a transition, occurs over a smooth pointed algebraic curve with A, the full determinant and every reduced rank locus fixed. The proof uses the classical self-adjoint nilpotent orbit closure criterion, orthogonal primary decomposition and curve selection. The inspected Trevisiol formulation and FMS Segre comparison are credited; dominance itself is not claimed new.

The universal-family theorem then realizes every allowed transition by a flat projective family of actual order-d multiplication-failure neighbourhoods. All lower truncations are locally constant families. Every strict transition is separated at d=n^2+2n-4 even without markings: the conjugate-partition square sum changes strictly and is invariant under root permutations. This treats the whole fixed-data locus, not only the earlier (3,1)->(2,2) model. Intermediate spectral length inequalities, the exact number of labelled classes, and the criterion for uniqueness of the coarse data are included.

The first relation is also `Tor_1^S(Q_R,C)_d`. The graded quotient Hilbert functor is a Grassmannian and the pencil locus is a closed copy of the original parameter scheme, including nonreduced parameters. This is the first Betti space of the quotient, not relations among ideal generators. It is a marked Hilbert statement, not an unmarked stack equivalence.

The independent real likelihood theorem from post-review v141 is retained in full, with its real-structure and unrestricted-data qualifications. The manuscript supplies substantive material for a new significance assessment; it does not self-certify top-four acceptance.

## Architecture, qualifiers and executed evidence

The principal article includes a compact dependency map: foundational Fitting geometry, web recombination, pencil/finite-order reconstruction, classical spectral input, the independent real theorem, and supplementary boundary results. Historical responses remain in the repository rather than replacing the mathematical narrative.

The distinctions remain explicit: reduced rank loci versus full determinantal ideals; finite-neighbourhood versus unrestricted failure-scheme flatness; uniform detection versus arbitrary pairwise minimality; complex square roots versus arbitrary fields; specified positive real norms versus arbitrary complex coordinates; relative socle versus absolute nilradical over nonreduced bases; marked quotients versus unmarked groupoids.

The new exact suite checks all monomials for n=2,...,6 in the Gram/Casimir identity, every quadratic rank for n=2,...,5, 84 mixed-identity evaluations, and 14,832 fixed-length partition comparisons through size 16. These finite tests do not replace the written proofs. All seventeen inherited scripts remain in the build sequence.

Only the executed source-bound receipt reports what actually passed: exact source commit, PDF hashes and page counts, source preservation, references and layout. A local preflight is labelled as such, not as a remote green run. Ballico access, exhaustive priority and editorial acceptance are outside what a build can certify.
