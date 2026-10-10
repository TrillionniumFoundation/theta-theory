# A2-DYN — revision 73

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Qian Qi · 11 October 2026

This revision responds to the v72 external report at `fad5823b36f2c68595c6b17bebf62c70032d30a9`. The manuscript's exact-return arithmetic pointwise target, original source, normalization and zero classes are unchanged.

Start with [main.tex](main.tex), [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md), [PROOF_LEDGER.md](PROOF_LEDGER.md), and [JOURNAL_ROUTE.md](JOURNAL_ROUTE.md). The active status is [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). Unchanged versioned notes and scripts are inherited history, not new endpoint declarations.

## Mathematical changes

Modules 160–163 give a common source kernel and interface ledger; finite BV of the **complete original scalar source** at every fixed collision count by an exact signed threshold representation; a paired incoming/outgoing flux bound with reserve two; and equality of the ordered scalar and bounded-Lipschitz path-numerator errors. The finite-measure theorem is no longer merely an extra hypothesis. Its bound is not uniform in collision count. The unrestricted scalar pointwise endpoint and uniform paired-flux decay are not declared proved.

## Complete manuscript build

From a clean checkout of either revision-73 branch:

```sh
bash papers/A2-DYN-v73-referee-response/build.sh
```

The native TeX master is `main.tex`. The first verification step deterministically extracts `build/v72-body.tex` and `build/v72-frontmatter.tex` from the byte-pinned `provenance/v72-main.tex`. This retains the complete old input order, every old proof and the preceding opening without maintaining a second handwritten copy. The new master compiles all **163 core modules**, not only an abridged front paper. Generated TeX, the full PDF, logs, recorder, rational-fixture results, page previews and exact-source archive are attached to the exact-SHA qualification run.

The read-only workflow is `.github/workflows/a2-dyn-v73-qualification.yml`. Both `revision/a2-dyn-v73-referee-response-2026-10-11` and `revision/a2-dyn-v73-referee-copy-2026-10-11` are intended to identify the same final commit. Consult the actual run result rather than treating this README as a passing-build certificate.

All 159 inherited cores, all inherited Python sources and appendices, and the bibliography are preserved byte-for-byte. The v72 sibling and controlling review remain unchanged. The first mathematical checkpoint is retained in `REVISION_73_CHECKPOINT.md`; this README and the manifest describe the assembled revision.
