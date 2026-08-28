# Round169 cold replay

Date: 2026-07-26

The producer was run under `PYTHONHASHSEED=16901` and `16903`.  Both outputs
were byte-identical to the frozen certificate.

The independent verifier was run against those two certificates under
`PYTHONHASHSEED=16907` and `16909`.  Both outputs were byte-identical to the
frozen verification.

```text
certificate sha256
87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb

verification sha256
90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f
```

The replay used `.venv-neurips/bin/python`.  No Round164--Round167 artifact
was modified.
