# Validation protocol and evidence: revision 13

## Frozen baseline evidence

Revision-12 exact source: `13b088e47bfbe8d46313b00bb97bc92a235a2376`. Successful baseline run: `37399143352`. Artifact: `11384359352`; archive SHA-256: `064604c3ed2aab67292133b5d52aa8abe98c5970f0a4f0b3dd24f2e62d063714`. These identify the baseline, not the new execution.

## New source qualification

`tools/verify_v13.py` checks all 30 core inclusions, retention of inherited mathematical labels, 28 byte-identical inherited core files, the exact one-character repair in file 15, unchanged inherited diagnostic scripts and bibliography, declared source hashes, references, citations, and balanced proof environments. It runs the entire inherited v11 finite-check chain, exact rational stopping/frequency balances, 64 exact Rademacher fourth-moment cases, ordered-gap summation checks, finite dyadic prefix checks, and two negative controls. The normal and optimized outputs must agree byte-for-byte. The six inherited geometry/return/inversion diagnostics run separately.

The native build runs without shell escape until references stabilize and rejects undefined references, LaTeX/package warnings, and overfull boxes. `evidence/build-receipt.json` is generated only after those checks; it records the checked-out SHA, event SHA, run ID and attempt, clean scoped-source state, PDF and TeX-log hashes, and verified source hashes. The artifact also contains the exact source archive and build log. The workflow upload has its own GitHub artifact digest.

No future run is predeclared successful in this static file. The dynamic receipt and the corresponding GitHub run are the authoritative execution records. Local rendering is a typesetting inspection, not proof certification. The source checks and finite diagnostics do not verify continuum billiard regularity, covariance positivity, a high-frequency resolvent, the full raw coarea sum, or independent human review.
