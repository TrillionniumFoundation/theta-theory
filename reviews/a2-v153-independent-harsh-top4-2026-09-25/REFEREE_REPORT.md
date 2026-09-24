# Independent harsh referee report — A2 revision 153

## Manuscript and review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Purported revision:** A2 revision 153  
**Revision branch reviewed:** `revision/a2-v153-global-incidence-fibre-structure-2026-09-25`  
**Revision-branch tip:** `2580b6397fd9a8c25db74b9913a6360955ffd1e6`  
**Parent / controlling review commit:** `60f1a3c5f8078c31019dfab249d334d0e717e225`  
**Only v153 file on the controlling branch:** `papers/A2-v17-boundary-information-coarsening/article/v153/REVISION_SOURCE_LOCK.md`  
**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and presentation standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I inspected the latest A2 revision branch, its tip commit and parentage, the complete branch comparison against the controlling v152 review commit, the contents of the v153 article directory, the repository's current review entry, and the separate v153 staging branch. The decisive issue is not subtle mathematical judgment. The repository does not contain a completed v153 manuscript on the branch designated as the latest revision.

## Recommendation

**Return without external review; equivalently, reject the purported revision in its present form as an incomplete submission.**

No mathematical recommendation concerning the advertised v153 theorems can responsibly be made, because no complete v153 theorem-and-proof object has been supplied on the controlling revision branch. This is not a negative correctness judgment on a finished manuscript. It is a finding that the finished manuscript does not exist in the submitted revision tree.

For a top-four journal this is an absolute threshold failure. A source-lock promise, an incomplete transport stream, or a description of mathematics that will later be supplied is not a paper. The branch must contain a stable, complete, source-bound review object before a referee can assess correctness, novelty, or significance.

---

## 1. Decisive repository finding

The branch `revision/a2-v153-global-incidence-fibre-structure-2026-09-25` is exactly one commit ahead of the controlling v152 review commit. The comparison contains one added file and no manuscript changes:

`papers/A2-v17-boundary-information-coarsening/article/v153/REVISION_SOURCE_LOCK.md`.

That file has eleven lines. It records ancestry and says that new mathematics and a revised reading order will be supplied in the v153 directory. It expressly states that the initial source-lock commit is not a claim that the revision or its verification is complete.

The v153 directory contains no other file. In particular, the branch contains no v153 version of any of the following:

- principal LaTeX source;
- principal PDF;
- focused reconstruction article;
- focused divisor-geometry article;
- abstract or front matter;
- new theorem sections;
- bibliography for the new claims;
- response to the v152 referee report;
- issue matrix;
- proof-scope audit;
- literature audit;
- build script;
- exact-check script;
- theorem locator;
- source-lock manifest binding actual v153 source files;
- provenance or nondeletion manifest;
- build receipt;
- PDF hashes;
- compilation logs.

The repository's `CURRENT_REVIEW_ENTRY.md` still declares revision 152 as the current referee object, points to the v152 branch, and identifies the v152 source commit and v152 PDFs. Nothing in the controlling v153 branch supersedes that entry with a materialized revision.

This is not a matter of an inconvenient folder layout. The new mathematical source is absent.

---

## 2. The separate staging branch does not cure the defect

A sibling branch exists:

`revision/a2-v153-squarefree-conductor-stratification-2026-09-24`.

Its tip is `a72ba0b883b7c22ec6ce792da56730aa086ef2f1`, whose commit message identifies it as source transport **3 of 4**. Relative to v152, that branch adds three Base64 payload fragments and the already-existing v152 referee report. It does not contain a materialized v153 article tree.

The three payload files form the beginning of one Base64-encoded XZ stream. A nonexecuting decode audit confirms that the stream is incomplete: it has no XZ end-of-stream marker and terminates in the middle of a LaTeX equation in the proposed squarefree-stratification section. The absent fourth transport fragment cannot be reconstructed from the first three. The resulting partial data cannot be treated as a complete source package, cannot be compiled, and cannot establish the final statements or proofs.

Even a complete staging transport would not automatically replace the explicitly designated latest revision branch. Here the problem is stronger: the transport itself is incomplete.

A referee must not silently fill missing bytes, infer omitted proof endings, or promote an unmaterialized staging payload into an authoritative submission. Doing so would destroy version control precisely where the manuscript claims unusual strength in provenance and auditability.

---

## 3. Why the missing review object is mathematically fatal

The absence of a complete source is not merely an editorial nuisance. It prevents every core act of mathematical refereeing.

### 3.1 The theorem statements are not fixed

A title such as “global incidence fibre structure” or “squarefree conductor stratification” is not a theorem. Without the completed source, I cannot determine the final hypotheses, quantifiers, exceptional cases, conventions, or relation among the advertised assertions.

For this project, small changes in hypotheses are mathematically decisive. Earlier revisions repeatedly distinguished:

- binary from multivariate forms;
- squarefree gcds from repeated-root collisions;
- reduced support from scheme-theoretic image;
- normalization fibres from image local rings;
- tangent dimensions from lengths;
- `GL(E)` first-relation orbits from `PGL(V)` pencil congruence;
- fibrewise statements from assertions over nonreduced bases.

A referee cannot verify that the final v153 text respects these distinctions when the final text is absent.

### 3.2 The proofs are not reviewable

The proposed advance appears intended to include global conductor and branch formulas, resultant-Fitting identifications, homological invariants, arbitrary-rank singular ideals, and reciprocal-fibre consequences. Each of these requires a complete proof, not an issue-matrix declaration.

Among the proof obligations that would require close inspection are:

- whether the simultaneous root coordinates give the entire completed ambient ring rather than a slice;
- whether the completed incidence functor is identified over arbitrary local Artin bases;
- whether the image ideal equals the stated Fitting ideal as an ideal, not merely on points or after completion without descent;
- whether all branch intersections are represented by sums of the asserted ideals;
- whether the conductor calculation is internal to the image ring and globalizes on the stated open;
- whether seminormality descends from the completed local calculation under the precise finite-normalization hypotheses;
- whether the Betti formula follows from the correct simplicial complex and coloring convention;
- whether the depth, type, and Gorenstein criteria include every boundary case;
- whether the arbitrary-rank pinch Fitting ideal is proved in the nonnormal image ring rather than only after pullback;
- whether reciprocal-fibre lengths and socles are exact or merely lower bounds.

The incomplete transport stops before even the proposed homological theorem is fully stated. None of these obligations can be certified from a source-lock stub.

### 3.3 The response to the previous report is not part of the submission

Revision 152 received a detailed report identifying both technical corrections and global structural conditions for another top-four evaluation. The latest branch contains no response document and no issue matrix. A partial response embedded in an incomplete staging stream is not a stable response on the controlling branch.

Therefore I cannot determine which objections the authors formally claim to have closed, which remain open, and which claims have been narrowed.

### 3.4 The literature position cannot be checked

The v152 report emphasized the unresolved Ballico 1993 comparison and the need for a serious comparison with factorization, resultant, coincident-root, and compactification literature. The controlling v153 branch contains no v153 bibliography or literature audit.

A top-four novelty assessment cannot be based on promised citations. It requires the actual article text, exact attribution, and final theorem statements.

### 3.5 Reproducibility claims cannot be tested

The repository has previously used source locks, theorem locators, build receipts, exact scripts, hashes, and preservation manifests. Those are useful when they bind an actual manuscript. Here there is no v153 receipt, no source manifest, no PDF hash, and no completed source to reproduce.

The project cannot simultaneously make auditability part of its presentation and ask a referee to overlook the absence of the audited object.

---

## 4. What has and has not been reviewed

The v152 manuscript was reviewed in the report committed at `60f1a3c5f8078c31019dfab249d334d0e717e225`. That report should not be relabeled as a v153 review.

I have **not** treated the partial staging stream as a completed manuscript. Its recoverable prefix indicates the direction of the intended revision, including a squarefree binary conductor theorem and related homological claims. Those claims may be substantial. But the stream ends mid-source, and the controlling branch expressly says the mathematics remains to be supplied. Consequently:

- I make no finding that the proposed v153 theorems are false;
- I make no finding that their proofs are correct;
- I make no finding that the v152 objections have been closed;
- I make no finding that the new material reaches top-four significance;
- I make no priority or literature judgment concerning the absent final text.

This limitation is not referee timidity. It is the minimum discipline required to avoid reviewing an imagined manuscript.

---

## 5. The repository state is itself inconsistent with “revision landed”

The latest branch name presents a revision and the source-lock title presents “revision 153,” but the branch content presents only an intention to create that revision. The current review entry still presents v152. The separate staging branch presents three quarters of a transport. These three signals do not define one reviewable object.

For a serious submission, the following must agree:

1. the branch identified as the revision;
2. the tip commit identified as the source-bound mathematical commit;
3. the current review entry;
4. the article directory;
5. the principal PDF and LaTeX source;
6. the response to the controlling report;
7. the build receipt and source hashes.

Here they do not agree. The version identity is broken before one reaches the mathematics.

At a top-four journal, this would normally result in an immediate return by the editorial office rather than consumption of referee time.

---

## 6. Minimum conditions for a genuine v153 review

A new review round should begin only after all of the following are present on one immutable revision branch.

### 6.1 Complete manuscript objects

The branch must contain the complete v153 LaTeX source and rendered PDF for every object the authors propose as a submission or a referee comparison object. If the revision is split into a reconstruction paper and a divisor-geometry paper, both must be complete, and the authors must identify which object is submitted to which journal.

### 6.2 A single authoritative source commit

The source lock must name the commit that actually contains the mathematical source, not a predecessor or a future intended materialization. The review branch must be created from that commit.

### 6.3 Updated review entry

`CURRENT_REVIEW_ENTRY.md` must point to v153, identify the principal review object, give its source-bound commit, and link to the response, theorem locator, receipt, and source lock.

### 6.4 Complete response to v152

The point-by-point response and issue matrix must be ordinary readable files in the v153 directory. They must distinguish corrections, new theorems, narrowed claims, and still-open matters.

### 6.5 Full new proofs and references

Every new theorem must appear with its complete proof and final references. No proof may depend on a missing transport segment, an unexpanded patch description, or generated files absent from the branch.

### 6.6 Native build evidence

A source-bound build receipt should record the actual scripts, versions, return codes, PDF hashes, resolved references, and theorem locations. Finite checks must remain explicitly secondary to proof.

### 6.7 Clean branch comparison

The comparison against v152 should expose the actual mathematical changes in ordinary paths. A referee should not have to decode opaque payload fragments to discover what the revision claims.

### 6.8 Stable literature disclosure

The final article must retain the unresolved Ballico limitation unless the full theorem-level comparison is completed. Comparisons with resultant and compactification literature must appear in the submitted text, not only in repository metadata.

---

## 7. Conditions for another top-four mathematical evaluation

Materializing the source is necessary but not sufficient for a favorable mathematical decision. Once a genuine v153 exists, the next referee should still assess whether the revision meets the structural conditions stated in the v152 report.

In particular, a claimed squarefree conductor theorem would need to be evaluated for:

- genuine scheme-theoretic equality with the relevant Fitting/resultant structure;
- a conductor formula on an entire natural open, not only at selected completed points;
- complete control of all branch intersections and descent from ordered roots;
- correct closure relations for the exact-gcd strata;
- rigorous homological formulas, including all edge cases;
- a clear account of what remains unknown for repeated roots and multivariate collisions;
- a significance argument that goes beyond applying standard squarefree-monomial machinery after obtaining coordinates;
- a convincing relation, if claimed, to the motivating pencil problem rather than merely to a large ambient first-relation space.

The architecture would also need a definite editorial choice. Supplying two focused papers plus an integrated comparison manuscript may be useful for a referee, but it does not answer which paper is actually seeking publication. Each submitted paper must have a coherent independent theorem package and a significance case that does not rely on unpublished companion material.

None of these mathematical questions can be settled in the present round because the relevant paper is absent.

---

## 8. Final assessment

The repository currently contains a completed v152 manuscript and its harsh referee report. It does not contain a completed v153 manuscript on the latest v153 revision branch.

The latest branch adds only a source-lock placeholder that expressly disclaims completeness. The sibling staging branch contains only three of four transport fragments and terminates mid-source. The current review entry still points to v152. There is no v153 PDF, no complete v153 LaTeX tree, no response, no authoritative build receipt, and no source-bound mathematical commit containing the proposed revision.

A referee cannot evaluate correctness, originality, depth, or exposition under these conditions. A top-four journal should not treat this repository state as a submitted revision.

**Recommendation: return without review; reject the purported v153 revision in its present incomplete form.**

A future report should be commissioned only after a complete, stable, materialized v153 review object is committed to one revision branch. That future report must be a new mathematical review. It cannot be inferred from this delivery audit or from the v152 decision.