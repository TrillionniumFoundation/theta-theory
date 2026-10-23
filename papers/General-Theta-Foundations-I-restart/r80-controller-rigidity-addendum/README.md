# General Theta Foundations I: first-order controller-rigidity author addendum

This is a substantive, narrowly scoped author addition to the actual published R80, not a new independent referee report and not a renamed duplicate of R80's value asymptotic. The complete English article, current technical supplement, and retained companion are buildable from this checkout. The original title, research identity, and four-leading-mathematics-journal goal remain unchanged.

## Start here

- `main.tex`: complete current article entry, adding `sections/60-first-order-controller-rigidity.tex` after the unchanged R80 sharpness proof.
- `supplement.tex`: complete paired current technical supplement entry.
- `companion.tex`: native entry to the unchanged separately retained R58 companion. The build script compiles that source in its original directory.
- [Pinned complete R80 source](../r80-stability-and-saturation/README.md): all shared preamble, sections, bibliography, history, proofs, maps and companion remain here, unchanged. This is a required sibling dependency, not an omitted appendix or an online mathematical oracle.
- `RESPONSE_TO_REFEREE.md`, `THEOREM_DEPENDENCIES.json`, `PRESERVATION_MAP.md`, `PROOF_AUDIT.md`, `RESEARCH_STATUS.md`, `SOURCE_PROVENANCE.md`: current author records.
- `build.py`: source-bound native reproduction, all 32 inherited diagnostic suites plus the new exact algebraic checks, and paired theorem-index reconstruction.

The only additional numbered theorem is `thm:dot-first-order-controller-rigidity`. For the exact two-model/two-label/six-parameter family of R80, excess cost o(sqrt(epsilon)) is equivalent to five necessary-and-sufficient coordinate asymptotics. In particular gamma=o(epsilon), the alpha deficit is o(sqrt(epsilon)), and xi is unrestricted. Every exact optimizer satisfies these rates. This is a first-order optimizer classification, not an exact positive-epsilon formula or a general quantum-instrument theorem.

## Reproduce

Use the exact source commit recorded by the later publication receipt. A complete ordinary checkout includes the pinned sibling. In a sparse checkout, materialize both this directory and `papers/General-Theta-Foundations-I-restart/r80-stability-and-saturation`. Required ancestor objects are R80 source `c0ac246181c2f4214e3e830952386adffb7d82df` and publication `304357fcada3771a5d01a29cdd93b4f42434cb7d`; the paper tree at both is `d9d760358cc951be5dff54c4495810d4bd342185`. Do not substitute the later publication hash for a source-bound build.

Run from this directory, using Python 3 with the versions in the inherited `requirements.txt` and TeX Live with the inherited native packages:

```sh
python3 -B build.py --source-commit FULL_SOURCE_COMMIT --out /tmp/theta-controller-rigidity-reproduction
```

The output directory must be fresh and outside the source. The runner sets the TeX source search path to the exact sibling, so no manual copying of old sections or 127 MB historical payloads is required. It compiles the full main article and supplement in alternating passes, resolves cross-document labels, compiles the independent companion, and rejects overfull boxes, unresolved references/citations and inconsistent 268-entry theorem locators. `--draft` is explicitly not a committed-source PASS; inherited diagnostics may be skipped only in draft mode. No shell escape is used.

To compile the main entry manually, put `.` and the absolute pinned sibling path in TEXINPUTS, retain the system default search path, and follow the alternating reference passes in `build.py`. The script is the supported complete reproducibility entry.

## Evidence boundaries

R80's 267 declarations and 32 diagnostics are inherited, not new contributions. The source author's existing publication is `304357fcada3771a5d01a29cdd93b4f42434cb7d`. This continuation independently reproduced the exact R80 source before editing, then proved a distinct equality-case conclusion. Native compilation, algebraic identities, author proof reconstruction and separate internal mathematical checks are distinct evidence. No new external referee, human-priority certificate or editorial acceptance is claimed. The controlling R65 report remains scoped to R65; the broader unsolved research questions are not pronounced closed.
