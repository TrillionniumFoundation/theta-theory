# Response to the independent A2 v117 report

**Revision:** A2 v118, *Conductor strata and nonreduced multiplication failure schemes*.  
**Report:** `reviews/a2-v117-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md` at `2c6f180fa0baf23386e0a46a64abe7503ea65b00`.  
**Predecessor:** v117 product head `fb999b3a43fe4331becb42646bc2faeadfa5492a`.

We thank the referee for separating mathematical correctness, proof architecture, and significance. The response is a mathematical extension rather than a reduction of the preceding claims. Every inherited theorem label is retained. The principal additions address the two structural requests: higher-defect quotient mechanisms and a nonreduced multigenerator family with complete primary structure. A new global conductor argument connects the latter to section multiplication in arbitrary projective dimension.

This document responds to the owner-requested independent report. Neither that report nor this response is a journal-issued editorial decision.

## E117.1 — Ballico 1993 theorem-level comparison

**Status: OPEN; not represented as closed.**

The DOI and Wiley PDF routes did not deliver the complete theorem pages through the available access in this revision. The inherited bibliographic reference and the explicit source-access qualification remain. No theorem hypotheses have been invented, and no claim of non-anticipation is deduced from missing full text. The required comparison against the conductor transports, fixed and moving failure schemes, and quotient incidence still requires those pages. New mathematics does not substitute for this bibliographic obligation.

## E117.2 — Broader audit of the universal hyperplane theorem

**Status: addressed by a theorem-level, explicitly bounded comparison; no exhaustive-priority certificate.**

The expanded literature section compares the inspected statements of Iovanov–Sistko, Sistko, Grönkvist–Leffler–Torstensson–Ufnarovski, and Arpin–Bozlee–Herr–Smith. The audit separates five logically different assertions:

| Assertion | Treatment in v118 |
|---|---|
| Geometric hyperplane/maximal-subalgebra types | Attributed to existing finite-algebra classifications, not claimed as a new closed-point classification. |
| Relative quotient/subalgebra equivalence | Proved on test schemes, including nilpotent bases; distinguished from agreement of reduced varieties. |
| Equality of higher multiplication Fitting ideals | Proved by unit-normalized residual presentations; all stable Fitting ideals are also handled in the higher-defect theorem. |
| Base-change compatibility | Proved for the hyperplane incidence and for exact-rank conductor flags; explicitly not claimed across arbitrary conductor-rank jumps. |
| Global-section transport | Kept as a separate theorem, now also proved for fat points in projective spaces of arbitrary dimension. |

The standard Hilbert functor, nested-divisor construction, and faithful-representation viewpoint are not relabelled as new constructions. See `LITERATURE_AUDIT.md` for the inspected theorem numbers and the remaining priority boundary.

## E117.3 — The reduced three-plane result and Haiman

**Status: addressed.**

The three-plane section now opens by identifying the all-powers diagonal identity as Haiman's input. The total-degree truncation lemma is moved, verbatim, to the finite-algebra preliminaries because it is also needed for the new higher-defect theorem. The proof explicitly maps Haiman's number-of-points index to our contact length and his power index to our independently varying power. The contribution is stated as the exact multiplication presentation and global cokernel transport, not a new proof of Haiman's theorem.

The nonreduced theorem added in the next section uses a filtered substitution matrix instead. It produces a determinant power with growing multiplicity and does not appeal to the diagonal-ideal result.

## E117.4 — A multigenerator theorem beyond reduced contacts

**Status: addressed by a full noncurvilinear class, with a global application.**

`thm:fat-primary` treats

\[
B_{e,h}=\mathbb C[z_1,\ldots,z_e]/(z_1,\ldots,z_e)^h,
\qquad e\ge2,\ h\ge3,
\]

on the **entire** generating `(e+1)`-plane Grassmannian. Its stable multiplication cokernel has a square substitution presentation. Filtration by powers of the maximal ideal gives

\[
\det T=\prod_{j=1}^{h-1}\det(\operatorname{Sym}^jM)
      =(\det M)^{\binom{e+h-1}{e+1}}.
\]

Consequently the full failure ideal, not just its radical, is the indicated power of an integral determinant divisor. Every ordinary power is primary, the nilradical index and generic transverse length are exact, and there are no embedded associated points on the universal parameter space. For `e=2` this is a three-plane theorem for every `C[x,y]/(x,y)^h`, not one small algebra or one local slice. Its stable threshold `m=h-1` is exact by the source-rank obstruction below that degree.

`thm:fat-conductor` proves the new global comparison on `P^e` for an order-`h` fat point and `n>=2h-1`. A triangular monomial argument works over the coefficient ring itself. It proves the coherent cokernel isomorphism and every Fitting equality after arbitrary base change. The bound is sharp uniformly over all generating ranks; no fixed-rank sharpness is asserted. `cor:global-fat-primary` gives the resulting global noncurvilinear primary schemes.

We do not extrapolate these results to every finite algebra or to every nonreduced curvilinear multiplicity partition. The class treated here has arbitrary embedding dimension and arbitrary nilpotence order, with explicit global consequences.

## E117.5 — Higher-defect mechanism and its obstruction

**Status: addressed by a relative structure theorem and the complete next-codimension mechanism.**

`thm:higher-defect-strata` first constructs the canonical stable generated algebra `E`, independent of the chosen unit. On an exact-rank stratum of its action on `B/E`, the conductor quotient is the flag

\[
 C=E/J\subset Q=B/J,\qquad
 \operatorname{rank}(Q/C)=r,\quad \operatorname{rank}C=t,
\]

with a universally injective, locally split action `C -> End(Q/C)`. The inverse construction is the preimage of `C` in `B`. These are mutually inverse functors, not a classification on geometric points only.

`prop:extreme-corank` identifies the unital-subalgebra scheme with the `(r-1)`st Fitting locus of multiplication, in every degree at least two. The text carefully distinguishes this extreme-corank locus from the zeroth-Fitting nonsurjectivity scheme for `r>1`.

`thm:codimension-two` proves `I_3(theta)=0` **scheme-theoretically**, using the bracket isomorphism on trace-zero two-by-two matrices. The two strata are rank-three quotients with scalar subalgebra, and rank-four quotients quadratic over a rank-two algebra. The proof supplies the cyclic-vector argument over the relative base.

The family `E=<1,sz^2+z^3,z^4> subset C[s][z]/z^5` demonstrates why a single fixed-rank quotient cannot replace the stratification. Its rank-one action locus is `s^2=0`, not merely the reduced point `s=0`; the conductor rank jumps there. The theorem includes the replacement functor before presenting this obstruction.

## E117.6 — Remaining relative constructions

**Status: addressed.**

The hyperplane theorem now writes the canonical line explicitly:

\[
 \mathcal C_m=i_*(Q/\ell^{(m)}).
\]

It also gives the version for an invertible `B`-module. The relative generating-open lemma states the ideal-generation, residue-evaluation, and smooth-surjective unit-cover characterizations and proves their equivalence. The curve theorem names every direct image `f_*L^j(-bD)` for `j>=1`, `b=0,1,2`, its vanishing and base-change hypotheses, and the precise vector-bundle surjections used. The moving hyperplane proof identifies the projectivization of the universal rank-two quotient and its tautological generating-line open.

## E117.7 — Primary-article architecture and preservation

**Status: addressed.**

The primary edition remains a single geometric argument: conductor comparison, finite-algebra structure, exact failure schemes, and their global applications. Its length increases only to accommodate the new proofs and explicit relative statements. The independent quadratic, polar, unrestricted, and statistical developments remain in the complete manuscript and separate application appendices; none is imported into the new proof spine.

`evidence/PRESERVATION.json` records all **273 inherited labels**, none missing, and **25 unchanged active source files**. The truncation lemma is relocated verbatim. The preceding `v117` sources and its archived `v116` derivations remain untouched on the branch.

## Verification and the next referee reading

The article contains the proofs. The exact regression program separately checks a fully symbolic length-six nonlinear substitution matrix; eighteen finite substitution specializations; triangular conductor columns; the nonreduced rank-jump ideal; and the trace-zero bracket identity. The build rejects unresolved references, duplicate labels, and overfull boxes. Actual page counts, source commit, and hashes are in `evidence/BUILD_RECEIPT.json`.

These checks are reproducibility evidence, not proof or priority certification. The mathematical and significance assessment remains for independent review. In particular, **E117.1 is still open** and must not be conflated with the substantive progress on E117.4–E117.6.
