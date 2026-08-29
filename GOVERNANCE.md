# Repository governance

## 1. One active source per paper

Each current paper has exactly one `main.tex` and one `references.bib`. Versions are
represented by commits and tags, not filenames such as `main-final.tex`, `main-v3.tex`
or `main-round4.tex`.

## 2. Archive separation

Historical manuscripts, cumulative chat/canonical volumes, CM2 evidence and legacy
verification programs live only on the archive branch identified in
`ARCHIVE_POINTER.md`.

## 3. Authority separation

The following are distinct and must never be collapsed into one status:

```text
proved in manuscript
actual model supplied
build or formula check passed
independent mathematical review completed
```

## 4. Platform binding

Every load-bearing theorem must carry a `platform_id`. Theorems from different
platforms cannot be composed into a `SAME_PLATFORM` conclusion without an explicit
bridge theorem.

## 5. No unscoped finality labels

The active tree must not introduce competing `FINAL`, `LATEST_WINS`, `RemainingGaps: 0`
or global `CLOSED` status pages. One machine-readable registry will generate human
status summaries.

## 6. Review preservation

Referee reports and hostile audits remain active review records when they apply to the
current theorem lineage. Historical reports must state the reviewed commit and are
retained on the archive branch or in a scoped review folder.
