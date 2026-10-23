# General Theta Foundations I — complete R78 source

Begin with [START_HERE.md](START_HERE.md). This source continues R77 source `18b76a739898d2734c4f5bfcb609db0786cd4c11`, published at `300807bad3eb00ad8e1975ae9ff1ea1971a333db`. The new source and its sibling publication directory are the only added paper paths. Every earlier paper directory and branch remains unchanged.

## Native reproduction

Use Python 3.11 or later with the packages in `requirements.txt`, native `pdflatex`, `pdftotext` and `pdfinfo`, and the AMS/Latin Modern/microtype packages in the retained preamble. A separate environment can be prepared with:

```bash
python3 -m venv /tmp/theta-r78-env
/tmp/theta-r78-env/bin/python -m pip install -r requirements.txt
```

Check out the exact **source commit** recorded in the sibling `PUBLICATION_RECEIPT.json`. From this source directory run:

```bash
/tmp/theta-r78-env/bin/python -B seal_source.py --check
/tmp/theta-r78-env/bin/python -B build_theorem_map.py --check
/tmp/theta-r78-env/bin/python -B verify.py --source-commit "$(git rev-parse HEAD)" --out /tmp/theta-r78-strict-reproduction
```

The output directory must be fresh and outside the source tree. Strict verification checks actual Git HEAD equality, the computed current paper tree, the unchanged R77 predecessor tree, all 622 preserved predecessor files, all old theorem bodies, all 235 inherited statement labels, all 240 current compiled locators, and the complete inherited R58 companion. It rejects changes outside the new source directory relative to the pinned R77 publication.

The verifier runs all **26 inherited diagnostic suites plus the new R78 suite**, each ordinarily and with `python -O`. It rejects assert-based diagnostics, unequal normal/optimized output, missing suites, count inconsistencies, undefined references/citations, duplicate labels and overfull boxes. It runs three native passes for each of the paired current documents and the companion, with no shell escape. The actual receipt records interpreter and library versions; a dependency specification is not evidence of an installed environment.

For an edited working copy or standalone source bundle, run:

```bash
python -B verify.py --draft --out /tmp/theta-r78-draft-reproduction
```

Draft mode emits `DRAFT_COMPILE_COMPLETE`, never a strict source-commit PASS. `--skip-diagnostics` is allowed only in draft mode and is explicitly recorded. If layout changes, copy the newly generated native index from the output directory, regenerate the author map, regenerate the complete preservation map as needed, and reseal before making the immutable source commit.

## Historical source authentication

The unchanged R77 archive parts/deltas retain the earlier 7,024 historical text blobs. The R78 census records the actual refreshed 7,137-blob scope and its precise source identities; its portable reconstruction checker and minimal additional delta are in `provenance/r78-audit/`. It reads archive members without extracting paths and checks Git blob identities, SHA-256, lengths, unique inventories and the current index. This source authentication is separate from mathematical proof checking.

## Evidence interpretation

Written proofs carry the quantified mathematical claims. Finite diagnostics test exact rational examples, boundary counterexamples and floating probes at stated tolerances. They are not formal verification. The new suite independently evaluates stochastic controller product chains and checks the smaller palette realization and exact cover formulas on finite cases. General real-algebraic elimination is a proved procedure, not an experiment claimed to have been executed for all inputs. A local strict PASS is not hosted CI, remote delivery, independent human endorsement or a journal decision.

Future author revisions should start from these complete native sources on a new branch, preserve this source and all reports, update the actual theorem/dependency map, and separate the new source commit from its later execution/publication receipt.
