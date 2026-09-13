# A2 v38 — complete native build and delivery protocol

This protocol describes the complete source-pinned execution required for C2. It is not evidence that the complete native main was built in the present session. Actual execution status is in [VERIFICATION_V38.md](VERIFICATION_V38.md).

## Pinned source and command

The complete inherited native source and new verifier are committed at `7d34d96a7c2dd974ab3725e009bbb584d3228114`. From a clean checkout of that commit, with Git, Python 3, NumPy, SciPy, SymPy, `latexmk`, a complete PDFLaTeX installation including the stated packages, and Poppler installed, run:

```sh
python -B papers/A2-v17-boundary-information-coarsening/tools/build_submission.py \
  --output-dir /absolute/path/outside/the/manuscript/a2-v38-native-evidence
```

The output directory must be absent or empty. The driver reads the declared Git objects and requires a clean manuscript working-tree scope. It does not accept an abridged substitute entry. It builds `two_collision.tex` first, then the complete `main.tex`, retaining every recursive native input. The main's companion auxiliary file must come from the verified first build.

The same execution is configured in [.github/workflows/a2-v38-native-submission.yml](../../.github/workflows/a2-v38-native-submission.yml). The workflow checks out its exact triggering commit with read-only contents permissions and retains the output directory even on failure. A configured or triggered workflow does not establish a successful build.

## Evidence emitted by the driver

The output includes `build-report.json`, the frozen Git-source manifest, the active recursive-input manifest, a retrievable `native-source.zip`, versions of the executed tools, normal and optimized diagnostic outputs, the actual build commands and outputs, final native logs, recorders and actual-input manifests, PDF identities and page counts, and explicit producer/consumer evidence for `two_collision.aux`.

The source archive contains the frozen source and a manifest with commit/tree and blob identities. Existing root products are excluded and listed rather than silently reused. Installed TeX packages and fonts are separately identified and hashed; their standalone font files are not distributed in the source archive. A build-product digest identifies the actual produced file, not a promise that another TeX distribution will generate byte-identical PDF output.

## Fail-closed checks and interpretation

Missing or empty recorders, missing native entry or recursive inputs, changed compilation bytes, unexplained local inputs, symbolic links and inputs outside the declared TeX installation roots are fatal. Generated input files are separately accounted for, and imported companion output must match its recorded producer. An unresolved reference or citation, duplicate label or PDF destination, missing glyph, failed TeX exit or invalid PDF is fatal. Available outputs and logs are retained after failure without issuing a successful product certificate.

Overfull/underfull reports are collected for layout inspection. A programmatic pass does not establish that the layout is suitable for submission. Both PDFs must be rendered and inspected, with the inspected source commit, PDF hashes, renderer, page coverage and findings recorded separately. C2 requires the complete-main and companion products plus that inspection evidence; a seven-page companion or one-page integration fixture is not a substitute.

The trust boundary is Git and the installed toolchain. The verifier does not attest a hostile compiler or protect against every adversarial transient filesystem mutation. A clean source scope and the immutable Git-object snapshot do prevent the concrete source-versus-compilation-copy mismatch reproduced in R37-V1 from being accepted.
