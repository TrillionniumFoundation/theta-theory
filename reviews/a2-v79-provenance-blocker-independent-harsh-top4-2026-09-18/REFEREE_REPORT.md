# Independent harsh referee report on nominal A2 revision 79

**Manuscript family:** A2, currently represented by *Marked clocked laws and reconstruction of generating actions*  
**Author:** Qian Qi  
**Date:** September 18, 2026  
**Nominal revision branch submitted for review:** `revision/a2-v79-universal-records-stable-quotient-2026-09-17`  
**Nominal reviewed head:** `f9de5e1e471df61f5ac02718d0c7b18b2e7d955e`  
**Last substantive manuscript branch:** `revision/a2-v78-observation-quotient-root-free-2026-09-17`  
**Last substantive manuscript head:** `9b0b6c25a3194cb99ba719d118c00a23dfb8febe`  
**Existing v78 referee branch:** `review/a2-v78-observation-quotient-independent-harsh-top4-2026-09-17`  
**Existing v78 referee head:** `f9de5e1e471df61f5ac02718d0c7b18b2e7d955e`  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested external-referee-style assessment, not a commissioned journal report or editorial decision. I apply a deliberately severe top-general-journal standard. The central finding of this round is not a new mathematical objection. It is a provenance fact that prevents a legitimate mathematical rereview.

## 1. Recommendation

**The nominal v79 submission is not reviewable as a new paper revision. I would return it to the author without a new substantive editorial assessment.**

The reason is exact and repository-verifiable:

1. the branch named `revision/a2-v79-universal-records-stable-quotient-2026-09-17` points to commit `f9de5e1...`;
2. that commit is itself the existing referee commit whose message is  
   `review: add independent harsh top-four report for A2 v78`;
3. the nominal v79 branch is **identical** to  
   `review/a2-v78-observation-quotient-independent-harsh-top4-2026-09-17`;
4. relative to the substantive v78 manuscript head `9b0b6c25...`, the nominal v79 head is exactly one commit ahead;
5. that one-commit delta adds only  
   `reviews/a2-v78-observation-quotient-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`;
6. there is no v79 manuscript source delta.

Thus the object presented under a v79 revision branch is not a mathematical revision of the paper. It is the previous referee report commit relabelled by a revision branch name.

At the requested journal level, this is a fatal procedural blocker. A referee cannot certify that objections were answered when no revised mathematical source exists.

The previous v78 mathematical report therefore remains controlling in full. Its negative top-four recommendation is neither superseded nor weakened by this nominal v79 branch.

## 2. Immutable provenance audit

### P79-1. The nominal v79 branch and the existing v78 review branch are the same Git object

A direct branch comparison gives status `identical`, with zero commits ahead and zero commits behind, between

- `review/a2-v78-observation-quotient-independent-harsh-top4-2026-09-17`, and
- `revision/a2-v79-universal-records-stable-quotient-2026-09-17`.

Both resolve to

`f9de5e1e471df61f5ac02718d0c7b18b2e7d955e`.

There is therefore no independent v79 source head to review.

### P79-2. The only delta from substantive v78 is the old v78 referee report

Comparing

`revision/a2-v78-observation-quotient-root-free-2026-09-17`

against the nominal v79 branch gives:

- status: ahead;
- ahead by: 1;
- behind by: 0;
- total commits: 1;
- changed files: exactly one.

The only changed path is

`reviews/a2-v78-observation-quotient-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`.

No `.tex`, bibliography, theorem, proof, response, build entry point, data-model file, or mathematical note changes in this delta.

### P79-3. The nominal v79 head is explicitly a referee commit

The head commit message is:

> review: add independent harsh top-four report for A2 v78

This is not ambiguous metadata. The commit itself declares its purpose to be addition of the v78 review.

A branch called `revision/a2-v79-...` should not silently point to a commit whose sole function is to add the previous referee report.

### P79-4. No v79 manuscript entry point exists

At the nominal v79 head, the following expected revision artifacts are absent:

- `papers/A2-v17-boundary-information-coarsening/rigidity_v79.tex`;
- `papers/A2-v17-boundary-information-coarsening/main_v79.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v79/01_introduction.tex`;
- `A2_REVISION_V79_REVIEW_READY.md`;
- `papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V78.md`.

The absence of any one of these would not by itself prove that no revision exists. Their simultaneous absence, together with the exact Git comparison above, does.

### P79-5. The active paper remains v78

The active revision-specific mathematical material on the nominal v79 head remains the v78 source, including

- `rigidity_v78.tex`;
- `article/v78/01_introduction.tex`;
- `article/v78/02_information.tex`;
- `article/v78/03_root_free.tex`;
- `article/v78/04_mechanics.tex`;
- `article/v78/05_uniform_records.tex`;
- `periodic_companion_v78.tex`;
- the v78 checker and build infrastructure.

Accordingly, any mathematical rereview performed now would simply be another review of the same v78 paper.

### P79-6. The root navigation is also stale

The root `README.md` on the nominal v79 head begins with “A2 revision 76” and points readers to the v76 handoff before retaining later historical entries.

For a repository with dozens of tightly versioned referee cycles, stale root navigation is not a trivial presentation issue. It materially increases the probability that authors and referees inspect different objects while believing they are discussing the same revision.

### P79-7. The role boundary between revision and review branches has been violated

The repository has otherwise used a sensible conceptual distinction:

- `revision/...` branches contain author revisions;
- `review/...` branches contain referee assessments.

The nominal v79 branch destroys that distinction by pointing to the previous review head without a manuscript commit in between.

For a long iterative proof-development process, this is particularly dangerous. It can make a later response appear to address a review that is already part of its own parent tree while obscuring whether the mathematical source actually changed.

### P79-8. There is no point-by-point response to the controlling v78 report

The controlling v78 report contains ten major concerns and eight required corrections. The nominal v79 head contains no `RESPONSE_TO_REFEREE_V78.md` and, more importantly, no source changes that could constitute an implicit response.

I therefore cannot credit any previous objection as closed in this round.

## 3. Status of the controlling v78 mathematical objections

Because there is no v79 mathematical delta, every substantive item in the v78 report remains open unless it was already expressly recorded there as a positive finding.

For clarity, the unresolved major objections remain:

### V78-M1. The quotient theorem removes the statistical encoding as the main source of conceptual novelty

Within the exact shared-weight model, the three normalized laws modulo common positive reweighting are information-equivalent to the absolute action. The significance case must therefore come from the post-action rigidity mechanism rather than from portraying the clock laws as intrinsically weaker data.

No new theorem changes this conclusion.

### V78-M2. The billiard observation operator remains highly marked and reference-dependent

The experiment still presupposes exact scalar boundary labels, obstacle/lift information, branch identities, prefix-extension pairing, branch-specific gates, admissible clocks and branch resolution.

No v79 natural, table-independent observation operator has been added.

### V78-M3. The fixed mechanical protocol remains engineered around action-threshold retention

The event `alpha + S_n(s,t) < T` directly depends on the unknown stationary action. The previous report requested either a natural physical realization, a reframing as an abstract encoding experiment, or a genuinely natural fixed-protocol application.

No new source addresses this.

### V78-M4. The abstract generating-action theorem remains close to a repackaging of its assumptions

The current abstract theorem assumes the decisive deterministic-match and positivity structure. The previous report requested a genuinely broad class where these properties follow from intrinsic geometry and yield a rigidity theorem not already implicit in standard generating-function composition.

No v79 theorem exists.

### V78-M5. Exact cross-clock shared weighting remains structurally brittle

The inverse depends on an exact common nuisance multiplier. No misspecification theorem, overidentified multi-clock test, robust quotient, or bias analysis has been added.

### V78-M6. The literature positioning remains inadequate

The v78 principal bibliography is still far too small for claims spanning billiard rigidity, marked length/lens data, twist maps, generating functions, discrete variational mechanics, distance geometry and nonparametric inverse problems.

No v79 bibliography or related-work revision exists.

### V78-M7. Headline scope statements remain broader than the proved theorems

The previous report identified the “whole smooth potential” and “bounded billiard classes” formulations as materially broader than the corresponding theorem statements.

With no manuscript change, these scope defects remain.

### V78-M8. The finite-record cost model still hides branch-resolution burden

There is still no revised theorem separating branch preparation cost from post hoc branch classification cost.

### V78-M9. The quotient-space Lipschitz language still lacks a defined quotient topology

No v79 definition or reformulation has been added.

### V78-M10. The root-free theorem still needs the physical single-branch hypothesis stated explicitly

The existing argument depends on every zero corresponding to the same deterministic physical branch family. The controlling report asked that this be encoded in the theorem statement rather than left informal.

No new theorem statement exists.

## 4. Why I am not manufacturing a second mathematical report on unchanged source

A referee can always reread the same manuscript and potentially notice something new. That is not what a revision cycle is for.

The relevant question in a revision round is whether the author has changed the source in response to the previous report and whether those changes close, weaken, or expose new objections. Here the answer is mechanically determined: there are no manuscript changes.

Writing another long mathematical report against the same v78 source and calling it a “v79 review” would create false version history. It would suggest that a new v79 theorem package had been examined when no such package exists.

A harsh referee should be especially unwilling to create that fiction.

The mathematically responsible disposition is therefore:

- preserve the existing v78 report as the controlling substantive assessment;
- record the provenance failure separately;
- require a genuine new source revision before the next mathematical rereview.

## 5. Required resubmission package

Before another referee cycle, I would require the following minimum repository state.

### R79-REQ1. A genuine new revision branch

Create a new `revision/...` branch whose head differs from the substantive v78 source head by actual manuscript commits.

It may be called v79 or a later number, but the version identifier must correspond to a real source delta.

### R79-REQ2. A pinned review-ready entry

Add a concise entry such as `A2_REVISION_V79_REVIEW_READY.md` that records:

- exact reviewed baseline branch and SHA;
- exact new revision head SHA;
- active principal source;
- active companion/full source if any;
- exact response-to-referee path;
- build products and their provenance, if supplied;
- a statement that diagnostics are not proof certification.

### R79-REQ3. A point-by-point response to v78

Add `RESPONSE_TO_REFEREE_V78.md` or an equivalently unambiguous file.

For each major concern, state one of:

- closed by theorem-level change;
- partially addressed;
- intentionally not addressed, with a precise reason;
- corrected as a scope/presentation issue.

Do not treat a new validation script as a response to a conceptual objection.

### R79-REQ4. New source entry points

If the new paper is genuinely v79, provide explicit revision entry points such as

- `rigidity_v79.tex`;
- revision-specific new modules or clearly documented reuse of v78 modules.

A new version need not copy every unchanged source file, but the active dependency graph must make it impossible to confuse v78 and v79.

### R79-REQ5. Do not use a referee commit as the revision head

A revision branch may contain historical review files in its ancestry, but its head should represent the author revision, not merely the preceding review commit.

The source/review/source alternation must remain auditable from Git history.

### R79-REQ6. Repair top-level navigation

Update the root navigation so that the first visible “current referee entry” points to the actual current revision. Historical entries can remain preserved below it.

For a repository this large, provenance is part of mathematical auditability.

### R79-REQ7. Demonstrate the actual response delta

The next review-ready entry should summarize which source paths changed relative to `9b0b6c25...` and why each changed path matters mathematically.

A top-four referee should be able to locate the new theorem-level content without reverse-engineering dozens of branch names.

## 6. Top-four editorial position

Nothing in this report changes the mathematical credit already recorded for v78:

- the exact three-clock quotient is coherent under its model assumptions;
- the root-selection-free downward-zero argument is a real improvement over v77;
- the strongly convex discrete-mechanical inverse is mathematically coherent;
- the finite-record exponents inspected in v78 were not found internally inconsistent;
- the principal/companion split improved the paper architecture.

Equally, nothing in the nominal v79 branch changes the negative top-four assessment.

At the requested journal level, the current state is weaker than an unsuccessful mathematical revision: it is **no mathematical revision at all**.

Accordingly, my recommendation is:

**Return without substantive rereview. The v78 referee report remains controlling. Require a genuine new manuscript delta before any further top-four assessment.**

## 7. Final referee statement

The repository currently labels the v78 referee head as a v79 revision branch. That label is not supported by the Git tree.

I therefore do not recognize `revision/a2-v79-universal-records-stable-quotient-2026-09-17` as a new paper revision. It contains no v79 manuscript, no v79 review-ready entry, no response to the v78 report, and no mathematical source change after the substantive v78 head.

This conclusion is not a judgment that a future v79 theorem cannot answer the previous objections. It is the narrower and more rigorous conclusion that **no such theorem has yet been committed on the branch submitted for review**.

The next useful step is not another referee report on unchanged mathematics. It is a clean author revision that produces a real, pinned, auditable manuscript delta. Only then is a fresh harsh mathematical review meaningful.
