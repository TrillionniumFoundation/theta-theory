# A2 revision 136: response to the two reports on revision 135

Manuscript: *Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes*  
Author: Qian Qi  
Revision branch: `revision/a2-v136-functorial-support-reconstruction-2026-09-23`  
Reviewed manuscript: `003fb13458c8ed11e2973963493a662f31c700c0`  
Controlling R2 review: `9fb3a5b9b27d4f6c6df2f3e557b4fc709c3a546d`, `reviews/a2-v135-independent-harsh-top4-r2-2026-09-23/REFEREE_REPORT.md`  
Companion R1 review: `9f246bef692ee715851c4b200041c5cfe76da7d9`, `reviews/a2-v135-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`.

These are owner-requested, AI-assisted referee-style reports, not decisions issued by a journal. The response addresses their mathematics and documentary requirements directly. The smooth-Jacobian inverse theorem retains exactly its full v135 scope. No additional exceptional open is imposed, and no inherited mathematical theorem is removed.

## 1. R2-B135.3: a proved extension, not only a significance paragraph

The new principal section `sec:uniform-support` proves a family of contraction and inverse theorems in every dimension. For `dim V=n`, the map

`j_n: det(V) tensor Sym^n(V) -> wedge^n Sym^2(V)`

is normalized on pure powers by `j_n(epsilon tensor l^n)=wedge_i(l x_i)`. The kernel of `i_q j_n` is now determined for **every n>=2 and every nonzero bilinear form q**:

- for singular q it is `det(V) tensor Sym^n(rad q)`;
- for nondegenerate q and odd n it is zero;
- for nondegenerate q and even n it is the line `det(V) tensor C(q^{-1})^(n/2)`.

The singular proof uses the inherited arbitrary-degree shear lemma, moved intact into its natural general setting. It includes the full disconnected rank-two orthogonal group. The even-dimensional line is handled by an algebraic cofactor-divergence identity and the monomial Wick recurrence, without a decomposition of the exterior-power target. A direct coefficient calculation gives `m(n+m-2)/(n(n-1))` on every positive-degree harmonic summand. This recovers the old coefficients 2 and 2/3 when n=4, but is not restricted to that dimension. The accepted SO4 proof remains compiled as an independent specialized proof.

The resulting exact exterior-support formula is `N-binomial(n-d+1,2)` for `d<n` essential variables, where `N=n(n+1)/2`. Full-variable forms have support N, except for the nondegenerate quadratic-power exception in even dimension, which has support N-1. Thus for **every n>=4**, at least three essential variables give support strictly greater than 2n.

Theorem `thm:uniform-recombination` applies this gap to canonical complementary projections `Q_n=(j_n C_n)/2` and `P_n=1-Q_n`. The Jacobian identity `C_n j_n=2 id` makes the construction independent of a chosen irreducible decomposition of the complement. On a nonempty open of `Gr(n,Sym^2 V)`, the component pair reconstructs the relation space; the relative pencil intersection is exactly the tautological section after arbitrary, including nonreduced, base change. The diagonal web supplies a concrete point of this open in every dimension.

This answers the extension option in the report with an actual theorem. It does **not** assert a higher-dimensional abstract failure-scheme readout that has not been proved. The latter geometric input is established here in dimension four, and the distinction is stated in `rem:uniform-versus-intrinsic`.

## 2. R2-S135.1 / R1-S135.1: regular oriented Segre descent

New Lemma `lem:oriented-segre-descent` is in the principal proof, before the universal readout. It constructs the two ruling parameter spaces as relative parameter **schemes** of maximal linear subspaces. Their scheme structures are checked in bundle frames, including the linearized minors. Preservation of the oriented ruling therefore produces a regular projective-bundle isomorphism.

The proof then compares relative O(1), pushes forward, and obtains local invertible matrices differing by line-bundle transition scalars. Their projective classes glue to a regular PGL-valued morphism. Only after this descent is established does projectivity of the Grassmannian and affineness of PGL imply constancy. A constant projective lift and right bundle maps recover the tensor formula. Homogeneity of both degree-twelve left coefficient factors and the common exterior-duality determinant twist show why local line-bundle ambiguities do not split the two projective transformations.

The original common-g lemma is strengthened to invoke this construction explicitly. Its conclusion and its universal coefficient square remain unchanged. The old source is also retained verbatim in the history directory.

## 3. R2-S135.2 / R1-S135.2: the residual ideal is intrinsic

New Lemma `lem:intrinsic-residual-ideal` defines the residual data within the recovered symmetric algebra A, not by choosing a scalar determinant equation. If I is the homogeneous cone ideal and D the ideal of its reduction, set `J=(I:D)`. The determinant coefficient line is

`L=D_4=(det V)^* tensor det K_0`,

and multiplication canonically identifies `L tensor J_12` with `I_16`. Thus `J_12=L^* tensor I_16`, with its embedding into A_12 supplied by the colon construction.

The proof establishes local `(dJ:d)=J`, independence of generator, and transport under every graded cone isomorphism. It also explains the exact base-change scope: the generic determinant remains a nonzerodivisor over every coefficient ring, but on a nonreduced new base the determinant ideal is **transported**, rather than recomputed as an absolute reduction. The readout and common-g proofs now use this lemma in place of informal determinant division.

## 4. R2-B135.1 / R1-B135.2 / R1-S135.3: the direct exterior literature

The principal introduction and literature section now cite the exact exterior antecedents requested by both reports. Landsberg--Ottaviani's first skew-flattening/subspace discussion is identified in arXiv:1010.1825v1, Section 6.1, and in the merged paper arXiv:1111.4567v1, Section 10.1. Sheridan's enclosing-space formulation is identified in arXiv:1906.05465v1, Section 2.4, Definitions 2.10--2.11. The version transition is documented rather than silently citing the withdrawn replacement record as if it were the original text.

The comparison assigns the general contraction-rank support notion and secant containment to that literature. It identifies the added calculation as the restriction to j_n: the all-ranks kernel, parity exception, exact support values, and subsequent inverse use. The polarization map and the occurrence of the Schur module are not claimed as inventions. The support-based secant exclusion is explicitly presented as an immediate consequence of the new restricted calculation and the classical containment. A six-question comparison is recorded in `LITERATURE_AUDIT_V136.md`; it is a comparison with inspected statements, not an exhaustive novelty clearance.

## 5. R2-B135.2 / R1-B135.1: Ballico 1993 remains documentary-open

The publisher's actual first-page image, printed p.5, was obtained and inspected. It defines higher-order spanning/very-ampleness conditions through restrictions of section spaces to finite subschemes, including general-point variants. This is more information than title metadata, but it is not the nine-page article.

The accessible publisher PDF route did not supply the complete text. A renewed Library search returned earlier A2 revision files and audits, not a verified complete copy of Ballico's paper. The six comparison axes are recorded individually, with first-page information separated from later theorem statements that remain unverified. No invented theorem numbers, nonanticipation conclusion, or claim of complete closure fills this gap.

Accordingly, **the full Ballico 1993 comparison is not marked closed**. The stronger mathematics above is not offered as a substitute for completing that scholarly comparison. Neither anticipation nor nonanticipation is certified.

## 6. Boundaries and preservation

The reduced support-pullback proposition is unchanged as a reduced statement; no radicality or scheme-theoretic equality of the pulled-back flattening ideals is added. The binary-boundary containment is not upgraded to a component classification. The rank-one residual Cartier section and the Fitting-ramification scope established in v135 remain intact.

All mathematical labels compiled by the complete v135 manuscript are required to appear in the complete v136 build. The previous universal-readout source is byte-identical. The specialized SO4 proof, primary-boundary theory, all ten old exact scripts, and the technical supplement are retained. Modified predecessor source files are additionally archived byte-for-byte. The new general support theorem is part of the focused principal article; the primary-boundary archive is not moved back into it.

## 7. Reproducibility and what the receipts do not certify

An eleventh script adds exact polarization-matrix checks in dimensions 2 through 7 at every bilinear rank, rational evaluation of even-dimensional scalar kernels, harmonic coefficients, and support examples including the diagonal web in each tested dimension. Modular elimination supplies exact lower-rank certificates; the exhibited zero columns or rational kernel vectors supply the finite upper bounds. No floating-point tolerance is used.

`evidence/BUILD_RECEIPT.json` records the actually executed run, source and PDF hashes, page counts, references/citations/labels checks, retained labels, and dependency versions. Local preflight is distinguished from a GitHub Actions run. Its successful checks do not certify the dimension-uniform proof, bundle descent, arbitrary base-change arguments, historical novelty, or a journal decision. Those arguments are given as written proofs for independent review.
