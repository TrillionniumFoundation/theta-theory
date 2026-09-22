# A2 revision 123 — referee reading packet

**Polarized ramification and higher-corank structure in multiplication failure**  
Qian Qi · 23 September 2026

The principal manuscript is **[geometry.pdf](geometry.pdf)** (16 pages). The **[complete companion](paper.pdf)** (147 pages) contains the new manuscript, a preservation leaf, and every page of the preceding 130-page complete manuscript. The preceding editable mathematical sources remain unchanged in `../v122/`. The source-provenance ZIP supplied with the release contains them as well.

The controlling report is `reviews/a2-v122-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md` at repository commit `14dcc67aced0a92d178ba7fd688b0c8b54111aad`. It reviews the v122 published product at `37480f3872b5c9f4ae18731e60a799986114c427`, built from mathematical source `790fff70e40ccdbe97d2569792535d6fe6cb6b2a`.

## Reading order

Read the three statements in §1, then §§3–6. Theorem 1.1 reconstructs the quartic polarization from the intrinsic nilradical line and the canonical bundle of its annihilator scheme. Theorem 1.2 proves a nine-dimensional image in actual polarized K3 moduli and generic finite ambiguity for the algebra. Theorem 1.3 describes a new embedded component on an explicitly nonempty open part of projection corank two. Appendix A gives the classical determinantal comparison; Appendix B contains explicit finite certificates.

The detailed [response](RESPONSE_TO_REFEREE_V122.md), [dependency map](DEPENDENCY_MAP.md), [literature audit](LITERATURE_AUDIT.md), and [issue matrix](ISSUE_MATRIX.json) distinguish the new proofs, their scope, and the documentary issue that is still outstanding. `evidence/` contains exact computations, page counts, source hashes, preservation checks, and build logs.

## Scope that must not be lost in review

The polarized reconstruction holds for every member of the stated smooth ramification class and for abstract isomorphisms of the whole Grassmannian failure scheme. The explicit primary classification at corank two holds on the open of admissible pairs, not on its exceptional complement and not at projection corank three or four. Generic finite ambiguity is not unique reconstruction of the quadratic map or the algebra. Ordinary powers remain powers of an ideal, not different multiplication degrees.

Ballico 1993 has not been obtained in full. The theorem-text priority comparison remains outstanding. The weighted formula is explicitly credited as a coefficientwise consequence of the classical symbolic-order profile. The classical web/incidence K3 construction is credited rather than presented as a new class of K3 surfaces.

## Reproduction

From this directory, run `bash build.sh`. This executes both new finite certificates and all three inherited regression entry points, builds both PDFs, rejects unresolved references and overfull boxes, and verifies historical page preservation. Dependencies are Python 3, SymPy, NumPy, PyMuPDF, and a LaTeX installation providing `pdflatex`, AMS packages, `lmodern`, `geometry`, `hyperref`, and `pdfpages`.

`SOURCE_LOCK.json` is the delivered source lock. `evidence/BUILD_RECEIPT.json` records the delivered build. Reproduction creates `evidence/REBUILD_RECEIPT.json`; it does not rewrite the delivered receipt. PDF byte hashes can differ across TeX installations even when text and mathematical inputs agree.

## Repository publication status

The target ref is `revision/a2-v123-polarized-k3-corank-two-2026-09-23`. The last connector read found that ref at the controlling review commit, with no revision-123 source commit on it. **This packet has not been pushed from the execution environment.** The available repository operations were read-only and the container could not connect to GitHub. No remote source commit is invented in the receipt.

The release includes an additive binary Git patch and `apply_revision.sh`. That script checks the exact review baseline, refuses a moved target branch, creates or uses only the target revision branch at that baseline, applies the addition-only patch, and commits. With `--push` it requests an ordinary fast-forward push; it never force-pushes, merges into `main`, deletes a branch, or rewrites an old revision.
