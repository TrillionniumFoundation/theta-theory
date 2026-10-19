# External top-four referee report on the putative A2-DYN revision 11

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Putative author branch:** `revision/a2-dyn-v11-referee-response-2026-10-06`  
**Branch head inspected:** `a42dc1401007f9f8025c916106884e09d7d864f0`  
**Object at that SHA:** the preceding external review commit, `Review A2-DYN v10: external top-four assessment of the growing-major-arc revision`  
**Last complete author revision:** `revision/a2-dyn-v10-referee-response-2026-10-05` / `revision/a2-dyn-v10-referee-copy-2026-10-05`  
**Last complete author SHA:** `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`  
**Controlling completed review:** `reviews/a2-dyn-v10-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling review commit:** `a42dc1401007f9f8025c916106884e09d7d864f0`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style source and editorial assessment; not a commissioned journal report, formal proof certificate, editorial decision, or independent human billiards-specialist report.

## 1. Recommendation

**Return without a new mathematical review. The branch is not a new manuscript revision.**

The branch named as revision 11 does not currently contain a revision-11 manuscript, response package, source manifest, proof ledger, or qualification workflow. Its head is exactly the commit that added the external referee report on revision 10. In particular, the expected manuscript path

`papers/A2-DYN-v11-referee-response/`

is absent at the branch head.

There is therefore no new mathematical object to compare with revision 10 and no defensible basis for issuing a fresh top-four correctness or significance judgment. Treating the branch name alone as evidence of a mathematical revision would repeat the version-identity problem previously observed in this project: a new-looking ref would be mistaken for new mathematical content although the underlying Git object is unchanged.

The completed revision-10 report remains the controlling assessment. Its recommendation was rejection in the present form at the requested four-journal benchmark, while recognizing the genuine Gaussian, functional-limit, and growing-major-arc advances. Nothing presently on the putative revision-11 branch changes that assessment.

## 2. Frozen source audit

The inspected ref is

`refs/heads/revision/a2-dyn-v11-referee-response-2026-10-06`.

It resolves to

`a42dc1401007f9f8025c916106884e09d7d864f0`.

That SHA is not an author revision. Its commit message is

`Review A2-DYN v10: external top-four assessment of the growing-major-arc revision`.

Its unique parent is the complete author revision-10 SHA

`3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`.

The files added by `a42dc1401007f9f8025c916106884e09d7d864f0` consist of the revision-10 referee report under

`reviews/a2-dyn-v10-external-top4-review-2026-10-06/REFEREE_REPORT.md`.

The contents query for

`papers/A2-DYN-v11-referee-response/`

at the putative revision-11 ref returns `Not Found`. No second author branch such as `revision/a2-dyn-v11-referee-copy-2026-10-06` is present in the inspected branch list.

These facts establish that the current branch is an initialization or alias of a review commit, not a landed revision manuscript.

## 3. Mathematical delta relative to revision 10

There is no mathematical delta to audit.

No new theorem, lemma, proposition, corollary, proof, calculation, source file, response letter, bibliography entry, diagnostic, or workflow specific to revision 11 is present at the branch head. In particular, there is no basis to claim progress on the three principal blockers identified in the completed revision-10 report:

1. uniform positive definiteness of the four-dimensional covariance through a periodic-evaluable regularity bridge or another nondegeneracy argument;
2. the complete integrated complementary-frequency estimate, including the annulus between the proved growing central band and the contemplated outer-frequency regime;
3. the full critical/singular branch decomposition with quantitative, return-count-dependent residual derivative sums and local edge estimates.

Nor is there any new material concerning weighted exact-event conditioning, terminal or multiple-time insertions, induced high-frequency Fredholm estimates, phase reconstruction, or independent specialist verification.

It would be incorrect to infer either success or failure on any of these mathematical points from the existence of the branch name.

## 4. Editorial consequence at the top-four benchmark

A top journal must identify the exact manuscript under review. A branch label is not a manuscript identity; the commit SHA and active source tree are.

Because the putative revision-11 branch resolves to the prior referee commit, the submission is administratively incomplete as a new revision. The appropriate editorial action is to return it without further mathematical review and request a source-pinned resubmission.

This conclusion is independent of the merits of revision 10. Even if the preceding paper had received a favorable recommendation, a new report could not responsibly be issued on an unchanged review commit represented as a new author revision.

## 5. Requirements for a reviewable revision 11

A subsequent revision-11 submission should satisfy all of the following before a new referee assessment is requested.

### 5.1 Exact author source

The author branch must advance beyond `a42dc1401007f9f8025c916106884e09d7d864f0` to a new commit whose tree contains the complete manuscript. The active directory should be unambiguous, for example

`papers/A2-DYN-v11-referee-response/`.

A referee-copy branch should resolve to the same final author SHA.

### 5.2 Version identity

The article title page, revision date, README, response letter, source manifest, proof ledger, workflow paths, author branch, and referee-copy branch should all identify revision 11 consistently.

The manifest should pin:

- the revision-10 author SHA;
- the controlling revision-10 review SHA and report blob;
- the inherited mathematical core tree;
- every new or modified mathematical source file;
- whether inherited files are byte-identical or intentionally changed.

### 5.3 Mathematical delta

The response should identify theorem-level changes rather than only presentation changes. For each claimed advance it should state:

- the exact new statement;
- the proof inputs actually used;
- its relation to the raw mixed-density LLT;
- which previous blocker it closes;
- which stronger conclusions remain unproved.

### 5.4 Reproducibility

The exact-event-SHA workflow should build and audit the complete article from the final author commit. Build success and finite diagnostics must remain clearly separated from mathematical proof certification and independent specialist approval.

## 6. Controlling mathematical assessment until a genuine revision lands

Until the author branch contains a new manuscript commit, the revision-10 referee report remains controlling.

That report recognized as genuine advances:

- the bounded collision compensation and exact stopping identity;
- continuous collision Green--Kubo covariance and actual-return Gaussian laws;
- functional limits for the return and unconditioned physical-time processes;
- the polynomially growing integrated central Fourier band;
- the detailed one-collision BV, collision-space embedding, chronological-product, short-block, complex-derivative, and coarse-interpolation arguments.

It nevertheless concluded that the full raw local theorem remained conditional on covariance nondegeneracy, complementary-frequency control, and the complete critical/singular residual decomposition. No source currently attached to the putative revision-11 branch changes those conclusions.

## 7. Scope of this review branch

This review branch starts directly from `a42dc1401007f9f8025c916106884e09d7d864f0` and adds only this report under

`reviews/a2-dyn-v11-external-top4-review-2026-10-06/`.

It does not modify any manuscript source, author branch, workflow, historical report, or unrelated repository path.

## 8. Final disposition

**Disposition: return without new mathematical review because no revision-11 manuscript has been landed at the named ref.**

Once the branch advances to an actual author commit containing a complete revision-11 source tree, that exact SHA should be submitted for a fresh top-four referee assessment. The next report should be based on the mathematical delta of that commit, not on the branch name or on this source-identity notice.