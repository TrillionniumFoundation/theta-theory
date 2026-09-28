# Source audit for the external A2 v15 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Article: Qian Qi, *Nonlinear boundary laws and asymmetric two-contact rigidity in dispersing billiards*  
Paper directory: `papers/A2-v15-asymmetric-contact-rigidity`

The repository contains three v15 revision names:

- `revision/a2-v15-asymmetric-contact-rigidity-2026-09-28`;
- `revision/a2-v15-referee-copy-2026-09-28`;
- `revision/a2-v15-smooth-observation-equivalence-2026-09-28`.

At the review cutoff all three resolved to head commit

`0dbe3b317da4b2b14f7a99e000da808fbbf8691e`

with repository tree

`21a390f312961e6c3c7b355717ee367ff797ea0f`.

That head commit adds only `DELIVERY.json`. The delivery record identifies the immutable manuscript qualification commit as

`00f27ebd0071d75504995b61f9a15c67f896188f`,

repository tree

`f7a58687b8443ca507f5da971155a35843b17385`,

and paper tree

`db84120af7be42acd785a9bc8d87dc6c652ee8d9`.

The mathematical-source checkpoint is

`cbb48f18a2820d85d0f9ba21f77224db6d1e5420`.

This report reviews the mathematics at `00f27ebd...`, while branching from the latest delivery head `0dbe3b...` so that the author's source-binding metadata remains available.

No A2 v16 branch was present at the review cutoff.

## 2. Review branch isolation

The review was written on

`review/a2-v15-external-harsh-top4-rereview-2026-09-28`.

It was created from `0dbe3b317da4b2b14f7a99e000da808fbbf8691e`. The review adds files only under

`reviews/a2-v15-external-harsh-top4-rereview-2026-09-28/`.

No author source, revision branch, prior report, historical snapshot, workflow, or unrelated paper was edited.

## 3. Source chain and preserved material

The v15 source pins identify the frozen v14 native tree as

`5506d189c55aff9b2e67dc9bfee9602615e0909a`

and the prior v14 review commit as

`a8e432bd27c21485a4babc268006314a5c7186c5`.

The complete v14 source is retained at

`papers/A2-v15-asymmetric-contact-rigidity/history/v14-reviewed`.

The v15 package has three mathematical documents:

1. `main.tex`, the 13-page theorem-led primary article;
2. `complete/main.tex`, the 133-page retained smooth-law and auxiliary-proof volume;
3. `complete/two_collision.tex`, the 7-page retained auxiliary article.

The author's preservation record reports 312 inherited files, of which 309 are byte-identical. The three declared direct edits in the complete volume are:

- `complete/main.tex` front matter;
- `complete/article/16_normal_form_comparison.tex` chart-convention clarification;
- `complete/article/31_regular_observability.tex` probability-margin clarification.

The primary article's main mathematical source consists of `main.tex` and five files under `core/`.

## 4. Files read in detail

The review inspected:

- `main.tex`;
- `core/01_introduction.tex`;
- `core/02_local_law.tex`;
- `core/03_asymmetric_inverse.tex`;
- `core/04_physical_observation.tex`;
- `core/05_relative_laws.tex`;
- `README.md`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `PROVENANCE.md`;
- `SOURCE_PINS.json`;
- `VERIFICATION.json`;
- `DELIVERY.json` at the branch head;
- `tools/verify_blocks.py`;
- `tools/verify_sources.py`;
- `tools/run_validation.py`;
- `.github/workflows/a2-v15-verify.yml`;
- `complete/main.tex` and the directly edited complete-volume sections;
- the frozen v14 referee report and the relevant v14 source sections.

The source checkpoint and qualification commit were compared. The primary mathematical files are unchanged by the qualification layer; the latter adds the response, ledgers, build records, preservation tools, workflow, historical report copy, and the declared complete-volume presentation corrections.

## 5. Author verification evidence

`VERIFICATION.json` records an executed local source-content qualification with:

- 2,747 v15 finite exact checks in normal and optimized Python with identical outputs;
- 1,588 retained v14 finite checks in normal and optimized Python with identical outputs;
- a 13-page primary build;
- a 133-page complete-volume build;
- a 7-page auxiliary build;
- zero final TeX warnings recorded for each document;
- identical source-preservation output before and after validation;
- a mathematical-source manifest SHA-256 of `3a12de3f535afc0cf8e514b905eea801a9f65a2f07e3f042459c2144ca61aff6`.

The delivery commit binds that local receipt and the relevant Git objects to the immutable qualified manuscript commit. The record explicitly does not call the checks a formal proof certificate.

At the final review check, hosted workflow run `36385817642`, triggered by head commit `0dbe3b...`, remained `queued` with `conclusion: null`. Therefore this review records the author's commit-bound local qualification but does not claim a completed hosted v15 run.

## 6. Independent review diagnostics

The review's `verify_review.py` imports no author module. It uses exact rational arithmetic and a different implementation based on closed unweighted and residual-weighted ellipse moments. It checks:

| Group | Checks |
|---|---:|
| displayed block entries | 5,100 |
| block determinants | 1,275 |
| odd separation inequalities | 675 |
| even separation identities | 600 |
| cubic, quartic and quintic references | 3 |
| fixed-area window designs | 54 |
| free-area window designs | 54 |
| deliberately singular window controls | 108 |
| window dimensions | 18 |
| area directions | 18 |
| reflection/parity controls | 2 |
| **Total** | **7,907** |

All checks passed in the review execution. They support only the finite highest-jet algebra and nodal designs. They do not establish the nonlinear Morse-domain degree argument, physical first-hit geometry, analytic continuation, retained smooth theory, or top-journal significance.

## 7. Scope and limits

This was a targeted rereview of the new v15 theorem and its response to the v14 report. It is not an independent line-by-line formal verification of the entire 133-page companion.

The review concentrated on:

1. exact local probability and signed-moment formulas;
2. the odd and even all-degree highest-jet blocks;
3. triangular finite-jet recovery with arbitrary lower odd jets;
4. the all-parity support-function realization;
5. fixed- and free-area positive-window coordinates;
6. the stated compressed binary experiment;
7. the change in information set from count-only data to framed signed moments;
8. the significance of the result at the requested Annals/Acta/Inventiones/JAMS benchmark.

The literature check is targeted rather than exhaustive. The independent script is diagnostic evidence, not a proof certificate. The editorial recommendation belongs to the referee report, not to any verification program.
