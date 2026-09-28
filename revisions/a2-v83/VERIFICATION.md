# Executed verification for A2 v83

## Source identity

Scientific commit: `c4867fc79d04db38ea887b66a9fba0965b008f62`.
Review parent: `b7075ecdeacb42befd55d4c732cbff4706fb4aca`.
The complete principal dependency graph is recorded with SHA-256 and Git blob hashes in `LOCAL_BUILD_REPORT.json`. Remote read-back of the six `article/v83/` files matches the locally built source. Later handoff-only commits do not change these mathematical files.

## Results actually executed

The command `python scripts/build_a2_v83.py --main-only` ran the normal and optimized regression suites and natively compiled the **complete self-contained principal article**, including its bibliography. It produced a 16-page PDF.

| Check | Executed result |
|---|---|
| Normal Python regressions | 22 run; 0 failures; 0 errors |
| Optimized Python regressions | 22 run; 0 failures; 0 errors |
| Undefined references or citations | 0 |
| Multiply-defined labels | 0 |
| Overfull boxes | 0 |
| Underfull boxes | 4 nonfatal spacing diagnostics |
| Visual inspection | All 16 final pages rendered and inspected; no clipping observed |

The principal PDF is 422016 bytes, SHA-256 `ed576833e9094d3f8c4ddefa1979dd128bc3e6b0687afbdb2d0a1528b47fee0c`.
The local environment was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 and pdfTeX 1.40.26. The tests exercise symbolic identities and specified numerical cases. They are not a formal proof certificate or an independent referee report.

## Expanded edition and CI — distinct status

`rigidity_v83_full.tex` retains the old integrated mathematical input sequence. Its native build was **not executed in the local partial historical-source checkout**; the principal result above must not be counted as an expanded-edition pass. The local copy recovered selected historical files from the v78 native source artifact and exact later blob reads, but not the entire post-v78 dependency graph.

The default command `python scripts/build_a2_v83.py` requires both editions, audits the retained direct inputs, and records their recursive hashes and separate native diagnostics. The GitHub workflow supplies the full checkout and runs that command. At the recorded check, run `35328468756` on scientific commit `c4867fc79d04db38ea887b66a9fba0965b008f62` was **queued**, with no conclusion. No remote-CI or expanded-native-build success is claimed here. The workflow separately archives the exact source checkout before the native build.

## Reproduction

From a full checkout, install Python dependencies from `scripts/requirements_a2_v83.txt`, install `latexmk`, the standard AMS/LaTeX packages, Latin Modern and Poppler, then run:

```sh
python scripts/test_a2_v83.py --output checks.json
python -O scripts/test_a2_v83.py --output checks-optimized.json
python scripts/build_a2_v83.py
```

Use `--main-only` only when intentionally reproducing the self-contained principal target. Its report records that the expanded target was omitted. Build logs and source graphs are generated in `papers/A2-v17-boundary-information-coarsening/build-v83/`; the accompanying review bundle includes the actual local native and regression logs. PDFs can differ bytewise across TeX environments; the source graph identifies the mathematical input independently of PDF metadata.
