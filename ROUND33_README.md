# Theta Theory — Round 33 proof reconstruction

Read `AUTHOR_RESPONSE_ROUND32.md` and `ROUND33_REVIEW_INDEX.md` first. The immutable controlling review is Round 32 at `e037717914a34fe7c0636743b3f5c645969bcb20`.

## Active files

Eleven chapter sources are in `round33/chapters/`. The eleven canonical `papers/*/main.tex` entries resolve only to Round 33. The combined source is `ROUND33_REVISION_DOSSIER.tex`. Historical proofs, reports and scripts are preserved but are not active mathematical inputs.

## Reproduce

Requires Python 3.10+, latexmk, pdfLaTeX, standard LaTeX packages, Latin Modern, and Poppler tools.

```sh
python3 tools/verify_round33.py --build
```

The command checks source hashes, control bytes, input graphs, labels, local references, 42 finite mathematical examples, and all 12 PDF builds. It writes only to `build/`, rechecks hashes after building, and does not run historical finalizers. A first-page render is a mechanical rendering check, not a visual or mathematical correctness claim. Local visual inspection is recorded separately.

## What the verification means

`ROUND33_LOCAL_VERIFICATION.json` is evidence of an executed local build at the exact manifest hash. It is not a remote GitHub Actions success certificate. The read-only workflow produces its own `VERIFIED_SOURCE_COMMIT.txt` and JSON record if it actually completes. No pending job is reported as successful.

The issue ledger maps 76 objections. Several original mechanical application proofs remain open and are marked accordingly. The 42 finite tests are algebraic/numerical examples, not a formal proof assistant or a test of every infinite-dimensional assertion. The original research programme remains the target; neither a change of wording nor a certificate is substituted for its missing proof obligations.
