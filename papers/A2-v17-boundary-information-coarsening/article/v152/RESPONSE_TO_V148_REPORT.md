# Response to the independent report on A2 revision 148

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**New revision:** 149, September 24, 2026  
**Controlling review branch:** `review/a2-v148-independent-harsh-top4-2026-09-24`  
**Controlling review commit:** `dc3a951e26de17e0e69403b1d8cfdfb5e28bc306`  
**Controlling report blob:** `b508fc349213e461d6745a2c1330245fedf4b48a`  
**Revision branch:** `revision/a2-v149-intrinsic-pencil-strata-deformations-2026-09-24`

We thank the referee for distinguishing the validity of the principal inverse chain from the further conceptual and documentary requirements. This revision does not replace the all-pencil theorem by a generic result, discard singular pencils, weaken an ungraded algebra isomorphism to a graded one, or replace actual source-bundle recovery by projective recovery. Every mathematical block from the previous principal article is retained. Three new sections develop an intrinsic relative moduli comparison and describe deformations outside the coefficient class.

The principal article remains `geometry.pdf`. The applications and historical archive remain separate. A theorem-number and label concordance is supplied in `README.md` after compilation; labels below give stable references to the proofs.

## 1. Full historical comparison: report §§11 and 16.1

**Status: documentary item unresolved, not represented as completed.**

We repeated the exact-title and DOI search and inspected the publisher's record and issue entry. The record establishes the bibliographic identity of Ballico's 1993 article, but does not provide its complete theorem/proof text in the accessible response. No newly obtained full article is available in this revision. The six requested axes on the Ballico side—objects, scheme structure, infinitesimal order, relative hypotheses, forgotten data, and inverse conclusions—therefore remain unverified.

The new mathematics does not substitute for reading that predecessor. Neither the response, the issue matrix, nor the build receipt asserts historical priority or nonanticipation. The introduction preserves the explicit distinction between the inspected material from Ballico 1996 and the incompletely inspected 1993 paper. `LITERATURE_AUDIT_V149.md` records the sources and the boundary of the comparison.

This is the one concrete documentary requirement from the report that the present package does not close. It is not used as a reason to stop the mathematical revision or to change its intended level.

## 2. Beyond full-factor invariance: report §§3, 12 and 16.2

The new section **Common-divisor strata and intrinsic families** starts with a geometric condition on an arbitrary space of homogeneous first relations. Full right-factor invariance is not assumed.

**Universal common divisor (`lem:universal-gcd`).** The locus of r-dimensional spaces of degree-D forms with exact common-divisor degree g is a reduced locally closed scheme. Multiplication identifies it with the product of the projective space of degree-g factors and the open Grassmannian of gcd-free residual subspaces. The proof checks properness, universal injectivity, and the differential: if `dot(f) J + f dot(J)` is zero modulo `fJ`, the gcd-free hypothesis forces `f | dot(f)` and then the tangent vector is zero. The resulting scheme isomorphism recovers the common-divisor line over arbitrary, including nonreduced, bases.

This is not a fibrewise radical argument. `rem:gcd-scheme-condition` gives an explicit dual-number counterexample: the span of `x² + ε y²` and `xy` has common factor x in its special fibre but does not have a deforming common factor. It does not lie in the scheme-theoretic stratum. This distinction is part of the theorem, not a qualification added after its proof.

**Determinant-divisor stratum (`thm:determinant-stratum`).** Requiring the common divisor to be a power of a determinant gives an intrinsic locally closed stratum, with quotient stack `[X/G]`, where X is the unrestricted gcd-free residual Grassmannian and G is the entire determinant-preserver group, including transposition. The proof proceeds through the universal common divisor and homogeneous-space descent. It applies to arbitrary parameter schemes and supplies the tangent complex `[Lie(G) -> Hom(J,S_h/J)]`.

**Relations leaving both symmetries (`thm:fixed-support-grassmannians`).** Through every pencil residual relation, we construct a projective Grassmannian of relations with exactly the same determinant radical. It contains a projective line through that pencil whose other points are invariant under neither full factor group. The construction fixes a small gcd-free subsystem that has no base point on the invertible locus, so preservation of the radical is proved and is not inferred from a tangent calculation. Thus the new ambient theorem actually includes relations excluded by the old recognition test.

We do not claim to classify every homogeneous ideal with a determinant radical. The larger natural object is an explicitly specified common-divisor stratum, and the revision describes its geometry, deformation theory, and the pencil locus inside it.

## 3. An independent pencil-native moduli consequence: report §§8 and 16.3

The new central consequence concerns the standard parameter space of **all quadratic pencils**, not a chosen covering-map family.

**Exact multiplicity (`lem:primitive-pencil`).** For every pencil, its first relation is

`K_R = det(T)^(n-1) · J_R^primitive`,

where the primitive residual degree is `3n-4`. The relevant Schur partition is `(3^(n-2),2,0)`. The proof derives the determinant twist from exterior duality and proves the residual gcd is one by right-group invariance and a rank-(n-1) coefficient test. This does not require a regular pencil or a general coefficient line.

**Effective pencil stack (`thm:pencil-stack-equivalence`).** The intrinsic common-divisor inverse, Cauchy projections, and Pluecker equations identify a locally closed pencil relation stratum scheme-theoretically. After the two specified inertia quotients, its stack is equivalent to

`[Gr(2, Sym² V) / PGL(V)]`

over every complex parameter scheme. The consequence is not just a transport of closed-point labels: pencil deformations, stabilizers, singular specializations, and the equations of invariant rank/Fitting strata correspond over nonreduced bases. The tangent complex is `[pgl(V) -> Hom(R,Sym²V/R)]`; the effective stack is smooth of dimension `n-3`, with exactly the classical pencil stabilizer jumps.

**Natural degeneration loci (`cor:pencil-specialization-stack`).** Every invariant locally closed pencil subscheme, with its given scheme structure, has the corresponding intrinsic effective failure stratum. This includes rank-incidence and spectral Fitting conditions and their scheme-theoretic intersections. The assertion is about the equations and their deformations, not merely the presence of a boundary point in a set.

The classical smoothness and dimension of the pencil quotient are not advertised as new results about pencils in isolation. The substantive comparison is that an ungraded finite failure algebra, after its precisely identified ineffective automorphisms are removed, retains this entire relative moduli problem. The earlier moving-cover example is preserved as a different global consequence, not used as a substitute for this comparison.

## 4. Stabilizers, nonreduced bases, and the difference from an orbit set: report §§4–6 and 16.4

The two ineffective kernels are deliberately not suppressed.

First, `prop:relative-first-relation` works with finite locally free algebras on a maximal-lower-Hilbert-function stratum. The augmentation is intrinsic normalized multiplication trace and is required to be multiplicative. Its kernel replaces the absolute nilradical over a nonreduced base. Local generator lifts give a homogeneous first-relation presentation; every other lift is a finite higher-order substitution. The underlying kernel scheme is `Hom(E,N²)`, with its actual nonadditive substitution law.

Second, after taking linear parts, the pencil relation stack is `[Gr(2,Sym²V)/G°]`, with

`1 -> GL(U) -> G° -> PGL(V) -> 1`.

The full right factor is ineffective on the recovered pencil. Only after quotienting these morphisms and fppf stackifying is the effective stack the PGL quotient. We neither assert a global splitting of this extension nor identify the original algebra stack with the effective one.

The family proof uses universal gcd descent, equivariant subbundle equations, and fppf local lifts. It does **not** extend the reduced-base commutant lemma to nonreduced bases by saying that fibrewise equality implies equality of sections. The original proper-reduction moving theorem and the new parameter-base stack theorem have different bases and different morphism conventions; `rem:moduli-scope` separates them explicitly.

## 5. Transverse geometry, rather than a further list of examples

The new theorem `thm:transverse-pencil-directions` computes the normal space of the pencil locus inside the residual Grassmannian as three equivariant parts:

1. `Hom(∧²R, ∧²(W/R))`, the normal space to the Pluecker locus;
2. `Hom(L,A/L) ⊗ sl(F)`, which breaks the full right multiplicity factor while staying in the same Cauchy summand;
3. `Hom(L⊗F,H_other)`, which moves into other Cauchy summands.

The group-orbit tangent is already inside the pencil tangent, so this normal quotient survives the effective first-relation comparison. The proof does not claim a canonical splitting of the Pluecker tangent sequence. Every ambient first-order direction integrates locally in the smooth common-divisor stratum; the separate fixed-support theorem supplies complete families for which the whole radical stays the determinant ideal. Keeping those two claims distinct prevents an unjustified passage from tangent directions to fixed-radical deformations.

## 6. Preservation and presentation: report §§10, 14 and 16.5

All previous principal mathematical blocks and labels remain in the principal article. All previous part files are byte-for-byte unchanged; the old root source files are also preserved in `history/v148-root`. The inherited applications are not abbreviated, and the historical archive is retained. `NONDELETION_V149.json` records the exact file hashes and block comparison.

The abstract now states the general determinant-divisor stratum separately from the recognized coefficient and pencil loci, and explicitly calls the stack comparison effective. The introduction states the new theorem architecture without a chronology of repair rounds. The number `d=n²+2n-4` remains the sharp uniform order of this construction, but orbit rigidity and family reconstruction carry the main conceptual emphasis. Internal version suffixes in labels are invisible in the compiled article. The separate applications PDF metadata now correctly says revision 149.

## 7. Verification and evidentiary scope

The revision adds exact checks for the primitive Schur degree and dimension, the common determinant multiplicity of all fifteen maximal minors of a singular 3-dimensional pencil, a dual-number failure of fibrewise gcd recovery, a small exact differential calculation, pencil tangent ranks in dimensions 3–5, and the three normal-space dimension identities. The inherited twenty-five regression scripts are retained and rerun by the isolated build, together with the new script. The receipt records actual outcomes, not anticipated ones.

All three manuscripts are compiled natively. Source hashes, predecessor hashes, report identity, executed-script logs, reference resolution, and nondeletion are bound to the published mathematical source commit. These checks are finite consistency and reproducibility evidence. They do not certify the universal proofs, the unresolved Ballico comparison, or a journal decision.

We submit the new intrinsic-stratum, effective-moduli, and transverse-deformation proofs for renewed mathematical scrutiny. Whether their scope reaches a particular general journal's significance threshold remains a referee judgment; it is not declared settled by the revision itself.
