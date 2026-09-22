# A2 v117 — finite quotients and primary structures

**Primary article:** *Finite quotients and primary structures of multiplication failure schemes*, Qian Qi.

**Unique revision branch:** `revision/a2-v117-finite-quotient-primary-structure-2026-09-22`.

The controlling R116 report is frozen at `a65e0e92b24fe6882e60ebcf678bb2f9f5048312`, reviewing the primary-contact v116 head `fadcfaa11a1939625177eb12e97569b63b7a1a9d`. This revision does not merge the divergent higher-product v116 line. Both historical branches remain unchanged.

## Reading entry

[Geometry article](geometry.pdf) ([source](geometry.tex)) is the principal coherent finite-contact paper. [Complete archival manuscript](paper.pdf) ([source](paper.tex)) also includes every inherited quadratic, polar, residual, wall, unrestricted hyperplane and application development. [Application appendices](applications.pdf) remain available separately, with cross-references into the complete manuscript.

[Response to R116](RESPONSE_TO_R116.md), [proof and literature audit](AUDIT.md), [identity](IDENTITY.json), [preservation manifest](evidence/V116_SOURCE_MANIFEST.json), [finite diagnostics](evidence/DIAGNOSTICS.json), [source receipt](evidence/SOURCE_RECEIPT.json), and [actual PDF build receipt](evidence/BUILD_RECEIPT.json).

## Mathematical changes

The uniform binary conductor range is improved to **n >= 2d-k**, with an exact evaluation-kernel criterion and boundary examples proving uniform sharpness. The comparison extends to curves under structural cohomology/normal-generation hypotheses, in particular when deg L >= 2d+2g-1. It remains an isomorphism of coherent cokernels after arbitrary base change.

For **any finite locally free commutative algebra**, generating hyperplanes have a single failure scheme in all degrees m >= 2. It is isomorphic to the space of rank-two quotient algebras with a generating line. This identifies the closed scheme on nonreduced bases, not just the generator open or its radical.

For **every multiplicity partition of a fixed divisor**, the generating contact-hyperplane failure scheme is a disjoint union of primary curves with transverse rings G_r = C[u,v]/(F_r,F_{r+1}) and C[x,y]/(x^r,y^s). Their exact lengths are binomial(r,2) and r*s; their nilpotency indices are 2r-3 and r+s-1. The moving total scheme is smooth. For the noncurvilinear algebra C[x,y]/(x^2,y^2), an exact chart instead has ideal (ab,b^2) = (b) intersect (a,b)^2, displaying an embedded component.

The stable **three-generator reduced-contact** ideal and every power are determined using Haiman's diagonal-ideal theorem, explicitly attributed. The pencil theorem, its exact weights and normalization are preserved with the sharper n >= 2d-2 bound. A standalone etale descent lemma proves the powered-prime identities at all branch intersections.

## Preservation, scope and review status

All 28 immediately reviewed TeX files are archived byte-for-byte under `history/v116_source/`; original source files and historical branches are not edited. All old part labels remain in the complete manuscript. Independent earlier results are separated by reading architecture, not removed or represented as premises of the new theorem.

The paper does **not** assert a classification on the unrestricted ambient Grassmannian. It does not relabel the old unrestricted evaluation-curve primary bound as an exact ideal. Classical index forms, Grassmannian cohomology and Haiman's theorem are identified as inputs, not claimed as new.

**The Ballico 1993 full-theorem comparison remains uncompleted.** The complete theorem pages were not obtained; no originality conclusion is inferred from this. All other response items have explicit revised locations. Mathematical proofs, finite diagnostics, source provenance and editorial novelty are separate assessments. This is an AI-assisted author revision, not journal-issued referee certification or acceptance.

## Rebuild and immutable identity

Run `python3 prepare_revision.py` once from a checkout containing the pinned sibling v116, then `bash build.sh`. The build reruns v116/v115 diagnostics in a disposable directory, runs new exact regressions, compiles all three copies, exports cross-references and hashes actual products. Final logs must have no undefined references, duplicate labels, overfull or underfull boxes.

The publishing workflow commits materialized mathematical sources before building; `evidence/SOURCE_RECEIPT.json` identifies that immutable source commit. A subsequent commit adds actual PDFs, logs and receipts. The source receipt is the source identity; the GitHub commit containing the PDFs is the product identity. Neither is a mathematical correctness certificate.
