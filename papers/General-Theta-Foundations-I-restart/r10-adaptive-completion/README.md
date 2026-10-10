# General Theta Foundations I — restart R10

**Acquired Geometry and Causal Resource Transfer**

This is the new ordinary manuscript source. Its main theorem is adaptive causal acquired-geometry completion, with the entire autonomous acquisition controller counted in the persistent alphabet. It is a foundations revision, not a renamed realization. The preceding R4–R9 subtrees remain unchanged alongside it.

Read `main.tex`, then Theorem `thm:autonomous` and Lemmas `lem:frontiercomparison`, `lem:causalpruning`; the new raw-kernel theorem is `thm:markovadaptive` and the attained joint-resource consequence is `cor:adaptivejoint`. The complete serial continuation, noisy rank, singular terminal expansion, progressive acquisition and filtering proofs are retained as ordinary inputs. Supplement S contains the complete retained technical text and is part of the same submission.

## Reproduction

From an ordinary source checkout, with Python 3, pypdf, pdfLaTeX, Latin Modern, scalable Computer Modern and Poppler installed:

```sh
python3 papers/General-Theta-Foundations-I-restart/r10-adaptive-completion/verify.py
python3 papers/General-Theta-Foundations-I-restart/r10-adaptive-completion/regression.py
python3 -O papers/General-Theta-Foundations-I-restart/r10-adaptive-completion/regression.py
python3 papers/General-Theta-Foundations-I-restart/r10-adaptive-completion/build.py \
  --source-sha SOURCE_COMMIT --expected-tree NATIVE_SOURCE_TREE \
  --output /tmp/theta-r10-artifacts --receipt /tmp/theta-r10-build.json
```

Replace the two uppercase values by the immutable source bindings in the publication receipt. Do not run `refresh_manifest.py` during verification; it is an authoring-only manifest tool. Builds use ordinary committed source and do not generate mathematical text. The build copies source into isolated temporary directories, performs two three-pass native builds and two three-pass retained-text builds, and twice builds the supplement cover. Evidence and artifacts are separate from the manifest.

The native mathematical article and integral supplement are the submission. Audit documents explain proof dependencies, assumptions, literature and scope but are not mathematical proof substitutes. Exact finite checks are not continuum proofs. Source, artifact and final evidence-only commits are separately bound in `evidence/` after publication.
