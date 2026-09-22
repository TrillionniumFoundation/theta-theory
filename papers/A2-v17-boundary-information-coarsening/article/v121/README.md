# A2 v121 — Determinantal flags and primary boundaries in multiplication failure

Author: Qian Qi. Revision date: 2026-09-22.

## Reading objects

**The journal manuscript is `geometry.tex` / `geometry.pdf`.** It begins with the universal primary flag and the elliptic embedded boundary, and contains the full finite-algebra/conductor core. The class and open conditions of each theorem are stated explicitly. This is the principal object for the next mathematical referee.

`paper.tex` / `paper.pdf` is the complete companion/archival edition. It contains the entire primary article together with all previously retained complementary geometry and statistical proofs. `applications.tex` / `applications.pdf` remains the applications reading edition. They are not presented as additional premises needed for the primary theorem. No historical manuscript is deleted or overwritten.

Read `RESPONSE_TO_R120.md` for the point-by-point reply, `LITERATURE_AUDIT.md` for precise source status, and `DEPENDENCY_MAP.md` for the theorem chain. `evidence/BUILD_RECEIPT.json` binds source hashes and generated products; diagnostics are regression evidence, not proof certification.

## Controlling review and branch

Repository: `TrillionniumFoundation/theta-theory`.

Review: `reviews/a2-v120-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md` at commit `b20eafa006fd3abe650ad7478542d637327b1094`.

New revision branch: `revision/a2-v121-determinantal-flags-elliptic-boundary-2026-09-22`, created directly from that review commit. The previous v120 source and all other papers stay unchanged.

## Mathematical additions

The weighted determinantal lemma computes an irredundant symbolic-primary intersection for `t * sum(t^(q-i) I_i(A))`. Its proof is coefficientwise and supplies explicit irredundancy witnesses.

For universal surjective quadratic multiplication tensors with `q <= e(e-1)/2`, the primary classification applies on the projection-corank-at-most-one open with `gamma(HV)=S` along the divisor. Every embedded support is a restriction-rank locus; the theorem gives all associated points on that open, exact nilpotency indices, normal supports, and projective incidence resolutions. It does not claim to classify the omitted higher projection-corank strata, and it does not specialize primary components without proof.

The rank-seven `(1,3,3)` family has a smooth embedded support which is a rank-four vector bundle over a varying elliptic curve times a projective plane. The full ideal is `I_Delta * I_E = I_Delta intersect I_E^2`. The nilradical is the square-zero line module `O_E(-Delta)`. This family is flat over the stated parameter open; its conductor has constant rank one. Distinct elliptic j-invariants give nonisomorphic finite algebras.

A named frame-primary descent lemma and its application make all global ideals and associated points in the retained `(1,2,2)` classification explicit.

## Source status

**E120.1 is not closed:** the complete Ballico 1993 article was not obtained. Its publisher record was checked; it is not a substitute for theorem text. The manuscript and response make no positive or negative priority certification against the unread article. The new mathematical results do not waive this documentary requirement.

## Rebuild

From the repository checkout:

```sh
bash papers/A2-v17-boundary-information-coarsening/article/v121/build.sh
```

Requirements: Python 3 with SymPy, pdfLaTeX with AMS/Latin Modern/microtype/hyperref and related packages, and `pdfinfo`. The build reads the preserved sibling `../v120` for the prior regression suites and preservation baseline; it does not write there. It first checks the algebraic regressions and content preservation, builds the complete edition, exports the cross-reference labels, and builds the two reading editions. There is no authoring script inside the build.

The publication workflow materializes the versioned source overlay before the source commit and then builds from that committed source. It pushes source and products only to this exact revision branch, with ordinary fast-forward pushes.
