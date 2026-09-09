# A2 v9: nonlinear boundary compatibility

Revision branch: `revision/a2-v9-nonlinear-boundary-compatibility-2026-09-09`.

Frozen referee baseline: `79ff2f96fc2e41899666065355238915f21273b0`.

Manuscript: **Relative boundary laws and inverse experiments in dispersing billiards**, Qian Qi, September 9, 2026.

## Complete source packet

The complete original text packet is committed under `.publication/a2-v9/`: 82 inherited source files in `reuse/`, and 35 new text files in the eight hash-pinned compressed-payload chunks. This includes the full English manuscript, the two-collision companion source, the response to referees, the proof ledger, historical derivation records, and the original reproducibility files. It is not a shortened manuscript. The transport representation is lossless; the restoration command checks every original text file against its SHA-256 before writing it.

Restore the 117 original text files into the native manuscript directory from the repository root:

```bash
python3 papers/A2-v9-nonlinear-boundary-compatibility/restore_sources.py
```

The resulting entry points are:

- `papers/A2-v9-nonlinear-boundary-compatibility/main.tex`
- `papers/A2-v9-nonlinear-boundary-compatibility/two_collision.tex`
- `papers/A2-v9-nonlinear-boundary-compatibility/RESPONSE_TO_REFEREES.md`
- `papers/A2-v9-nonlinear-boundary-compatibility/PROOF_LEDGER.md`

To run the original finite diagnostics and rebuild the PDFs, with Python/SymPy/mpmath and the LaTeX dependencies installed:

```bash
python3 papers/A2-v9-nonlinear-boundary-compatibility/restore_sources.py --verify --build
```

The delivered PDFs are reproducible build products. The restoration script additionally checks their original SHA-256 and Git blob identities. PDF binaries are not represented as already committed native files in this source-packet publication.

## Integrity and validation boundaries

Compressed payload SHA-256: `ef947b9ee98acd7348d4e6d3b76a8d9f0384e63a9ea062afd30f30d48fff9a91`.

Decoded payload SHA-256: `eeba93cc4d5e0bc4f03d7dd2604bcdc13e62fd885b6cb8fe8195f3b367e687d0`.

The original delivery records describe the state at packet generation and remain unchanged. The published transport and restoration entry constitute a later source-packet publication. A historical statement that the packet had not yet been pushed should not be silently rewritten into a retrospective receipt.

The local build reproduced the delivered 91-page main manuscript and 7-page companion. The original finite suites comprise 407 new and 249 inherited diagnostics. These are reproducibility checks, not formal proof certification. The attempted GitHub Actions publication jobs failed before executing their steps; remote CI success is not claimed.

Existing author manuscripts and referee reports are retained. This revision branch is not a merge into `main`.
