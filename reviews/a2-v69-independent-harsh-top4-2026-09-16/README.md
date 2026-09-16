# A2 v69 independent referee review

Read `REFEREE_REPORT.md` first. It contains the recommendation, theorem-level discussion, primary-source comparisons, source anchors and explicit coverage limits. `AUDIT_EVIDENCE.json` contains the independently emitted evidence, not an author's proof certificate.

Reviewed source: `1a46fd69a508bccb90c6d2553892124f068f4657`.

Review parent: `17e3e881935239a0d47e9f73bd0ecf3c93dcdd22`.

Manuscript subtree: `e0c2434849fe72a715cec1fae5e6e36bf90b5669`.

Review branch: `review/a2-v69-independent-harsh-top4-2026-09-16`.

The branch adds only this review directory. It does not change manuscripts, old reviews, published deliveries, default-branch refs or permissions. The report is an author-requested AI-assisted referee-style assessment, not a commissioned journal decision.

## Reproduction

Download the native GitHub Actions artifact `10446655754` from run `35096091680`, and the previous artifact `10442234606` from run `35088239966`. Save the complete outer archives as `a2-v69-native-artifact.zip` and `a2-v68-native-baseline.zip`. The expected SHA-256 identities are in the evidence JSON.

Python 3.10 or newer is sufficient for the scripts. `verify_delivery.py` and `compare_builds.py` additionally require PyMuPDF (`fitz`). `independent_checks.py` uses the standard library only. None of these programs imports author code.

```sh
python verify_delivery.py a2-v69-native-artifact.zip \
  --baseline a2-v68-native-baseline.zip > delivery.json
python independent_checks.py > checks.json
python -O independent_checks.py > checks-optimized.json
cmp checks.json checks-optimized.json
```

The delivery verifier checks source bytes, lengths, Git blob identities, raw ZIP modes, independently reconstructed Git trees, the literal active TeX input graph used by this source, original-file retention, native PDF identities and pages, the final-log diagnostic patterns, and all native build-report evidence entries. The optional baseline is compared to the embedded old manifest and its actual source bytes; the two historical raw-mode discrepancies are reported rather than repaired. This input-graph traversal is tailored to the literal `input`/`include` forms in this source, not a general TeX interpreter.

For fresh builds, extract the final artifact, verify it, and extract its `native-source.zip` into a clean directory. Copy **only** the 895 frozen files under its `source/` prefix to the build directory; do not import published auxiliary files. ZIP extraction alone does not restore executable permissions. This review checked raw headers and did not rely on executing a script by its executable bit.

With `latexmk`, `pdflatex` and the required TeX packages installed, run in the clean source directory, in this order:

```sh
for entry in two_collision main rigidity; do
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
    -file-line-error -recorder \
    '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' "$entry.tex"
done
```

Then compare the extracted native product directory with the new build directory:

```sh
python compare_builds.py NATIVE_PRODUCT_DIRECTORY CLEAN_BUILD_DIRECTORY \
  --dpi 72 > comparison.json
```

The independently rebuilt 507 pages matched in extracted text and same-renderer 72-dpi RGB arrays. PDF bytes differed. The comparison program emits mismatching page numbers and matched error-pattern names; inspect these output fields rather than interpreting process exit alone as a pass. Exact rendering equality across unrelated renderer/TeX versions is not promised. The review inspected only the visual sample specified in the evidence JSON.

## Interpretation

The finite checks validate moment algebra, the displayed rate balances, finite first-success mark identities, two-offset cancellation and weighted thresholds. The finite moment model uses a polynomial weight, not the manuscript's smooth bump. Deliberately incorrect dimension and free-success balances are detected. No finite test certifies the geometric inverse, a concentration theorem, an infinite-dimensional limit, or minimax optimality.

The four author normal/optimized diagnostic output pairs in the downloaded artifact were compared, but those author programs were not rerun. Detailed local build logs and sampled page images are retained in the separately supplied audit archive. No all-page proof certification or exhaustive literature-priority claim is made.
