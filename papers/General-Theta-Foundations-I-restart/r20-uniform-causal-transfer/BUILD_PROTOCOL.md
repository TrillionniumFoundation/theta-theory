# Immutable-source build protocol

The native mathematical source is the manifested UTF-8 file set in this directory. Building never regenerates it from a patch script. The one-shot GitHub publication transport is separate and removed before the ordinary source commit; its hash remains in the bootstrap ancestor. The R19 generators remain unchanged in the predecessor directory but are not duplicated as a second source of the new article.

Run, with output outside a read-only checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python papers/General-Theta-Foundations-I-restart/r20-uniform-causal-transfer/build.py \
  --source-sha <ordinary-source-commit> --expected-tree <native-directory-tree> \
  --output /tmp/r20-build/artifacts --receipt /tmp/r20-build/BUILD_RECEIPT.json
```

`verify.py` checks the source manifest, hashes, native Git tree, all active TeX inputs, labels/references, bibliography use and statement environments. `regression.py` performs the declared new exact finite checks and records the complete inherited regression chain separately. `native_build.py` compares ordinary and optimized outputs and makes two isolated three-pass TeX builds from copied manifested source, with deterministic metadata, no shell escape, recorder-input checks, no undefined references and no overfull boxes. The full build rebuilds R19 and its whole preserved chain from their pinned source-tree identities.

Hosted and independent builds must name the same immutable ordinary source and artifact parent. Different TeX environments are compared by normalized text and rendered pages; cross-engine PDF byte identity is not assumed. Source, artifact and final evidence-only commits remain separate. Final verification records what actually ran, not predicted counts. A build is not a proof, and rebuilding companions is not a theorem-by-theorem recertification of the archive.
