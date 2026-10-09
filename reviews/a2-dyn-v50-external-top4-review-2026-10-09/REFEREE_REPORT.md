# External top-four submission-status referee report on A2-DYN revision 50

**Manuscript program:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Nominal author response branch:** `revision/a2-dyn-v50-referee-response-2026-10-09`  
**Nominal referee-copy branch:** `revision/a2-dyn-v50-referee-copy-2026-10-09`  
**Response-branch head reviewed:** `bdbba17ce1692b21e296dacade86df9f838dfacf`  
**Response-branch repository tree:** `32d327154eab9defb146bbf91c8c8b1839ed62b2`  
**Referee-copy head observed at the time of review:** `11520f4876ca9033c0a0abfbdb0041e1f85c260e`  
**Controlling completed author manuscript:** revision 49, commit `f3174ed1e7e339aa9c4bb5bd716a24653080c7dd`  
**Controlling completed external report:** `reviews/a2-dyn-v49-external-top4-review-2026-10-09/REFEREE_REPORT.md`, commit `11520f4876ca9033c0a0abfbdb0041e1f85c260e`, blob `cad56babdd60f941c0e554dc88c99e90c20335b4`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation: return without substantive mathematical review because revision 50 is not yet a manuscript.**

If the editorial workflow requires a binary recommendation at the requested four-journal benchmark, the appropriate entry is:

**reject in the present form as an incomplete submission.**

This recommendation is procedural and source-based, not a negative mathematical judgment on a new theorem. The repository does not presently contain a revision-50 article to referee.

The response-branch commit explicitly describes itself as a bootstrap source freeze before a later substantive revision. The new revision-50 paper directory contains only `REVISION_CHARTER.md`. It does not contain `main.tex`, mathematical core modules, a bibliography, a build script, a source manifest, a proof ledger, a response-to-referee document, a specialist audit map, a publication-status record, or a compiled-manuscript qualification receipt.

The charter itself states:

- revision 49 is the author baseline;
- the revision-49 external report is the controlling report;
- the title, actual-return record, arithmetic transition kernel, pointwise target, inherited mathematics, and provenance are to be retained;
- the review is to be answered by explicit proofs rather than by relabelling local `L^1` convergence as uniform density convergence;
- the present commit merely freezes the review bytes and baseline;
- it is not a completed manuscript or proof certificate.

I therefore do not treat the bootstrap as a theorem-bearing author revision, and I do not manufacture a mathematical referee assessment from the revision-49 manuscript under a revision-50 label.

## 2. Exact source state

The nominal response branch resolves to

`bdbba17ce1692b21e296dacade86df9f838dfacf`.

That commit has the completed revision-49 external-report commit

`11520f4876ca9033c0a0abfbdb0041e1f85c260e`

as its parent.

The commit message is:

> A2-DYN v50: freeze latest v49 referee source before the substantive revision

and expressly states that the commit freezes source bytes only and makes no manuscript-qualification or mathematical-completion claim.

The commit adds exactly two relevant items:

1. `.github/workflows/a2-dyn-v50-qualification.yml`;
2. `papers/A2-DYN-v50-referee-response/REVISION_CHARTER.md`.

The revision-50 paper directory contains no other file.

Consequently there is no revision-50 manuscript tree, no ordinary source payload tree for an article, and no mathematical source list to audit.

## 3. Author-branch inconsistency

At the time of this review, the two nominal author branches did not resolve to the same source.

- `revision/a2-dyn-v50-referee-response-2026-10-09` points to the bootstrap commit `bdbba17...`.
- `revision/a2-dyn-v50-referee-copy-2026-10-09` points to `11520f48...`, the revision-49 external-report commit.

Thus the copy branch does not contain even the revision-50 charter and workflow.

This mismatch does not create a mathematical ambiguity because neither branch contains a completed revision-50 article. It does, however, prevent the usual exact-source statement that two author refs identify one manuscript SHA.

A future substantive revision should synchronize the author response and referee-copy branches before external review begins.

## 4. Meaning of the workflow result

The response-branch workflow run completed successfully:

- workflow: `A2-DYN v50 exact-source qualification`;
- run: `37861340498`;
- event SHA: `bdbba17ce1692b21e296dacade86df9f838dfacf`;
- conclusion: success.

This workflow is intentionally a freeze-only workflow. Its job is named `freeze-source`, and it checks the controlling revision-49 report blob, archives the review, the revision-50 charter directory, and the workflow, and records the event SHA.

It does not:

- compile a revision-50 article;
- verify TeX inclusions;
- verify mathematical labels;
- compare inherited core modules;
- run mathematical diagnostics;
- render theorem pages;
- produce an ordinary manuscript Merkle tree;
- certify a manuscript PDF;
- or claim mathematical qualification.

No workflow run was present for the nominal referee-copy branch at the time of review.

The successful response-branch run is therefore valid evidence that the bootstrap freeze executed as designed. It is not evidence that a new paper has been built or qualified.

## 5. What can and cannot be reviewed

### 5.1 What is reviewable

The following source-management facts can be checked:

- the controlling revision-49 external report is identified by commit and blob;
- the revision-49 author manuscript is identified as the baseline;
- the revision-50 response branch descends from the controlling report commit;
- the charter preserves the model, record, arithmetic main term, pointwise target, inherited mathematics, and provenance;
- the charter correctly distinguishes local-variation convergence from pointwise density convergence;
- the freeze workflow does not overstate its evidentiary meaning.

These are sound revision-governance choices.

### 5.2 What is not reviewable

There is no new mathematical text from which to assess:

- a new theorem statement;
- a new proof;
- closure of the physical-boundary essential-supremum criterion;
- suppression or retention of arithmetic residues;
- a pointwise raw-density local limit;
- a single-roof conditional bridge;
- generality beyond the triangular Lorentz family;
- novelty relative to the billiard and suspension local-limit literature;
- correctness of any new continuum anisotropic-space argument;
- or readiness for a top-four journal.

Any such assessment would be invented.

## 6. Relation to revision 49

Revision 49 remains the latest complete manuscript presently available in the repository.

Its external report recognized a substantial theorem-bearing advance: the complete original exact-index density was controlled in uniformly translated fixed roof windows in local variation, all physical incidence and clearance sources were included, arbitrary measurable roof selectors were allowed, and central mixed-measure and exact-window conditional roof laws were obtained in total variation.

That report nevertheless recommended rejection at the requested benchmark because, among other reasons:

- local `L^1` variation does not exclude narrow high density spikes;
- the essential-supremum physical-boundary correction remained open;
- the pointwise roof-density local limit remained open;
- a path bridge conditioned at one prescribed roof value remained open;
- concrete section residues were not proved trivial;
- independent specialist verification was absent;
- and the submission remained exceptionally large and model-specific.

Revision 50 contains no mathematical change to any of those conclusions.

The revision-49 recommendation therefore remains the last substantive mathematical assessment. It should not be copied into revision 50 as though a new manuscript had been examined; it remains attached to revision 49 and its exact SHA.

## 7. Standard required for a new top-four review

A revision seeking a new external top-four assessment should contain, on two synchronized author refs, at minimum:

1. a complete `main.tex` or equivalent article source;
2. all new mathematical modules and all retained inherited modules;
3. a precise source manifest identifying inherited and changed files;
4. a response to the controlling revision-49 referee report;
5. a proof ledger describing the new logical chain;
6. a specialist audit map identifying continuum obligations;
7. a publication-status file that distinguishes proved, conditional, and open endpoints;
8. a build and validation protocol tied to the exact manuscript SHA;
9. a successful manuscript qualification run on each author ref, or a documented reason why one identical-SHA run is the sole execution evidence;
10. a source tree containing an actual paper rather than a charter alone.

For the mathematics, a revision intending to change the revision-49 recommendation should directly address the controlling substantive issues rather than only reorganize them.

The most important possible routes are:

- prove the physical-boundary essential-supremum correction at the microscopic `m^{-2}` scale;
- prove a genuine pointwise arithmetic raw-density theorem with the correct transition or residue factor;
- prove the corresponding single-roof conditional result;
- or replace the model-specific endpoint by a broader theorem whose independent significance justifies the requested venue.

A completed revision may instead choose a focused local-variation paper. In that case its title, abstract, introduction, theorem hierarchy, and novelty comparison should be organized around the theorem actually proved, without allowing an unproved pointwise endpoint to dominate the editorial claim.

## 8. Source and branch recommendations

Before requesting another referee report, the author should:

1. land the complete revision-50 article on the response branch;
2. move the referee-copy branch to the identical completed manuscript SHA;
3. ensure the completed manuscript descends from the controlling report in a transparent chronology;
4. replace or extend the freeze-only workflow with manuscript compilation and exact-source verification;
5. retain the current charter as provenance, rather than treating it as the manuscript;
6. record all theorem-status flags honestly;
7. avoid predeclaring successful execution in static source files;
8. preserve the distinction between source qualification and proof certification.

## 9. Editorial and mathematical assessment

The current repository state is well described as **revision preparation**, not **revision submission**.

The charter is useful. It fixes the correct controlling report, preserves the original topic and main objects, and explicitly forbids a false upgrade from local variation to uniform pointwise density convergence. The workflow also correctly limits itself to freezing source provenance.

Those are positive process signals, but they are not a mathematical article.

A top-four referee cannot evaluate novelty, correctness, depth, generality, or presentation without theorem statements and proofs. Nor should an editor treat a successful provenance-freeze job as a manuscript-qualification event.

## 10. Final recommendation

Revision 50, as presently landed, consists of a source-freeze workflow and a nine-line revision charter. The charter explicitly says that the substantive revision has not yet been completed.

There is therefore no revision-50 mathematical manuscript to review.

**Final recommendation: return without substantive review; if a binary journal decision is required, reject the present incomplete submission.**

A fresh external mathematical report should be requested only after a complete revision-50 manuscript is landed and the two author branches are synchronized at the same exact SHA.