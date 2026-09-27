# GTF-I revision 52 source-transfer provenance

This directory is a transport scaffold, not the referee-facing manuscript. The four binary parts concatenate to one bzip2-compressed JSON source recipe. `bootstrap.py` verifies its SHA-256 and reconstructs exactly 59 readable native files under `papers/GTF-I-v52-quantitative-lifts/`, using the frozen v51 publication inherited by the controlling r33 review. It never modifies v51 or any other paper.

Recipe SHA-256: `1ab06ab91906c7b594f80f48d340c059417d80783445b98d8ae328e838c37737`.

Base v51 publication: `6363748923a5623801a53cfdb507a776aad414c3`.

Controlling r33: `9d2f516b4113016f57fc8193c24ba192f8f782d5`.

A separately hashed bibliographic metadata correction replaces an incorrectly transcribed title in LITERATURE_AUDIT.md with Lei Huang's verified arXiv 2406.13980v2 title, *On the complexity of matrix Putinar's Positivstellensatz*. The correction occurs before committing native source and before qualification; it does not alter the mathematical manuscript or its bibliography. Both its preimage and final digest are checked in the readable bootstrap.

The publication workflow first commits the readable native source, then runs all exact suites in ordinary and optimized Python, compiles the full article and reading excerpt, checks all original labels, and rebuilds the complete source-only archive in isolation. Only a source-bound successful receipt permits a separate derived-artifact commit and non-force atomic publication to the v52 work and referee-ready branches. The ready entry point is GENERAL_THETA_FOUNDATIONS_I_V52_REVIEW_READY.md.
