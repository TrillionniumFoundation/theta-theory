# Excluded local corpus and rationale

The staging process intentionally selected research inputs rather than copying
the whole workstation.  The following classes remain in their original local
locations and are not represented as canonical theory content:

| Class | Local source | Reason |
| --- | --- | --- |
| Raw agent memory and session material | Resident workspace `MEMORY.md`, `memory/`, and OpenClaw session stores | Private conversation/provenance data; the canonical volumes already contain the relevant sanitized research history. |
| Credentials and client state | `auth.json`, browser/Telegram cookies, GitHub/OpenClaw config | Secrets and non-research state. |
| Build by-products | LaTeX `.aux/.log/.fls/.fdb_latexmk/.out/.toc/.blg` files and Python `__pycache__`/`.pyc` | Reproducible noise; compile summaries, source/PDF outputs, and the small retained `.bbl` bibliography snapshots are kept instead. |
| Historical package containers | `A_Theory_of__Expectations/packages/` and its `source_workspace.zip` files | Redundant nested snapshots (including large duplicate archives); the unpacked source snapshot is retained. |
| Automation output trees | `A_Theory_of__Expectations/automation-results/` | Repeated intermediate PDFs; final/retained PDFs and status records are retained. |
| Large generated CM2 ledgers/runtime | Workspace `.cm2-runtime/`, compressed ledgers, and deliverable JSON/JSONL files above the staging size threshold | Tens of GB of seed-specific/generated state; selected readable reports, source, manifests, and small certificates are retained. |
| Unrelated workspace projects | Phone/app downloads, cleanup runs, trading projects, and other non-θ-Theory trees | Outside the requested research scope. |

For auditability, `provenance/inclusion-manifest.tsv` records every included
file's source label, relative source path, destination, size, SHA-256, and
source modification time.  This document records the policy boundary; it is
not a claim that an excluded generated ledger is mathematically irrelevant.
A future release may add a specifically named, independently checked evidence
bundle without rewriting this snapshot.

## Snapshot totals

The measured exclusion totals for this release are in
`provenance/excluded-summary.tsv`:

- 1,053 deliverable files / 23,792,573,501 bytes (large/generated payloads);
- 12,266 CM2 runtime files / 30,571,336,993 bytes;
- 24 historical paper-package files / 650,252,605 bytes;
- 4 automation-result files / 5,778,733 bytes.

These totals are inventory metadata only; none of those payloads is required
to interpret the canonical control volumes in this snapshot.
