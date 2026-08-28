# θ-Theory research archive

This private repository is a curated, reproducible archive of the θ-Theory
program as of **2026-08-28**.  It keeps the latest-wins canonical volumes,
the three-paper source stack, the CM2 bridge history, and the readable CM2
source/evidence needed to continue the work in a fresh environment.

## Start here

1. `canonical/theta_theory_navier_stokes_initial_md_all_chat_canonical_latest_nonrecursive_through_v16320_2026-08-28.md` — current non-recursive θ-Theory/NSE canonical volume (`v16320-DRAFT`).
2. `canonical/theta_theory_recursive.md` — recursive/type-checked θ-Theory architecture (`v164`).
3. `canonical/CM2_无条件攻坚_Canonical_Latest-Wins_非递归单一总卷_through_r63bd_2026-08-26.md` — CM2 origin, audit history, and controlling `r63bd` state.
4. `canonical/CM2_LATEST_STATUS.md` — compact CM2 status snapshot.

The canonical volumes are editorial consolidations.  They preserve
provenance and latest-wins control, but do not create a new theorem or
authority certificate.  Their explicit fail-closed/NO-GO boundaries remain
the controlling interpretation.

## Layout

| Path | Contents |
| --- | --- |
| `canonical/` | Latest θ-Theory, recursive, and CM2 control volumes. |
| `papers/expectations-monograph/` | Source snapshot of `A_Theory_of__Expectations`: monograph, Paper 1 response theory, Paper 2 theta-expectation/HJB, Paper 3 representation calculus, CM2 bridge, plans, inventories, and referee material. LaTeX build by-products are omitted. |
| `evidence/cm2/bridge-notes/` | CM2 bridge-note source/PDF version history (plus the retained v15 source/PDF). |
| `evidence/cm2/deliverables/` | Readable CM2 reports, source programs, TeX, PDFs, checksums, and small machine-readable manifests/certificates. |
| `evidence/cm2/artifacts/` | Additional retained CM2/response PDFs. |
| `tools/cm2-scripts/` | CM2/C79g launchers, builders, reviewers, and canonical-volume helpers. |
| `provenance/` | Inclusion manifest, source inventory, and exclusion policy. |

## Reuse and verification

The exact per-file SHA-256 manifest is
`provenance/inclusion-manifest.tsv`.  Paths in the manifest are archive
relative and the source labels identify the local corpus without copying
private workspace memory.  To verify the archive after checkout:

```sh
awk -F '\t' 'NR > 1 { print $5 "  " $1 }' provenance/inclusion-manifest.tsv \
  | sha256sum -c -
```

For the three LaTeX papers, use the source files and the retained PDFs under
`papers/expectations-monograph/papers/`.  Their `compile-status.md` files
record the last successful local build and its scope; generated `.aux`,
`.log`, `.fls`, `.fdb_latexmk`, `.out`, `.toc`, and `.blg` files are not part
of this archive.  The small `.bbl` bibliography snapshots are retained where
present to make the recorded paper builds easier to reproduce.

## Scope and exclusions

This is a research-source archive, not a raw disk image.  Raw agent memory,
chat/session logs, credentials, cookies, virtual environments, Python bytecode,
large generated ledgers, and unrelated projects are intentionally excluded.
The exclusion inventory and rationale are recorded in
`provenance/excluded-local-corpus.md`; no excluded item is silently treated as
part of the canonical theory.  Large generated evidence can be regenerated or
located from its original local provenance when a future release explicitly
needs it.

Inherited copyright and license notices remain with their respective source
files.  See `NOTICE.md`; this repository does not grant a blanket public
license over the research manuscripts.
