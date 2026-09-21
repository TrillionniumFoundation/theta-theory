# A2 revision 111

**Recovery of information metrics: contact multiplication and global degeneracy**

The principal manuscript is `paper.tex`; its inputs are `parts/*.tex` and `references.tex`. It is a self-contained 20-page amsart article. Read `RESPONSE_TO_R110.md` for the response to the controlling report and `PRESERVATION_AND_DEPENDENCIES.md` for attribution, historical interfaces and assumptions.

Controlling review: `review/a2-v110-independent-harsh-top4-2026-09-21`, exact commit `043495e949f535554c5540c24b679b4aafa6a31d`.

Isolated revision branch: `revision/a2-v111-global-degeneracy-boundary-experiment-2026-09-21`.

## Main additions

Theorem 1.1 computes the exact global codimension of failure of the sum of within-contact multiplication maps: `min{L*c*(c+1)/2 - 2*k + 2, L*c - 3}`, for `4 <= c < k` and `L*c*(c+1)/2 >= 2*k-1`. It identifies a common-secant component in the secant-dominant regime and gives the sharp number of independently designed contacts. Theorem 5.1 classifies positive fixed-space realization with global fibre separation. Section 8 identifies the physical cone experiment; Section 9 constructs randomized contact-score statistics directly from counts and proves their local Le Cam comparison and exact information loss.

The original sharp threshold, finite-sample estimators, stability results, monomial constructions, complete-contact ambiguity, budget fibres, and endpoint representation results remain in the principal text or appendices. All inherited repository files remain unchanged.

## Build and replay

From this directory, with Python 3, SymPy, latexmk, pdfLaTeX and pdfinfo installed:

```sh
python3 build_review.py --local
```

This builds the principal paper, runs finite exact diagnostics, and writes `evidence/local-receipt.json`. It explicitly does not claim an inherited-source check or companion build.

From a full repository checkout containing the controlling review commit:

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v111/build_review.py
```

This checks that all changes from the review baseline are new v111 files, builds v111 plus unchanged v110/v109/v108, and writes `evidence/ci-receipt.json`. The new branch-only GitHub Actions workflow runs this command and commits the principal PDF and exact-source receipt back to this branch after checking that its head has not moved.

A workflow definition or queued run is not evidence of successful execution. Inspect the receipt's `status`, `source_bound`, `source_commit`, `run_url`, hashes and companion records. Its source commit intentionally precedes the generated-evidence commit.

Finite exact diagnostics check 9,920 dimension triples, 2,106,240 feasible rank strata, ten product witnesses, three globally separated native witnesses, a corank-one secant witness and rational matrix identities. These checks are stress tests, not a proof of the universal theorems or a certification of journal-level significance.
