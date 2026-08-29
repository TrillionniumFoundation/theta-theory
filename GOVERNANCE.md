# Repository governance

## Source authority

The only active manuscript source for each paper is its `main.tex`, and the
only active bibliography is `references.bib`.

Historical filenames such as `main-v2.tex`, `main-final.tex`,
`main-round4.tex`, and competing `FINAL_STATUS` pages are forbidden on the
default branch.

## Platform typing

Every load-bearing theorem must carry a platform identifier from
`platforms/platform-registry.yaml`.

A same-platform theorem may use only imports with the same platform identifier,
unless a separate bridge theorem is stated and proved.

## Status dimensions

The following statuses are independent:

- mathematical manuscript status;
- actual-system/platform status;
- build/verification status;
- independent external review status.

A build receipt may not upgrade mathematical or review status.

## Archive

Historical assets are immutable on
`archive/full-v4-pre-governance-2026-08-29`.  They may be consulted for
provenance and regression testing, but they are not controlling sources.

## Changes

A mathematical change must update:

1. the relevant `main.tex`;
2. `papers/SERIES_MANIFEST.yaml`;
3. `status/ACTIVE_STATUS.yaml`;
4. the paper's `REFEREE_GUIDE.md` when the review surface changes.
