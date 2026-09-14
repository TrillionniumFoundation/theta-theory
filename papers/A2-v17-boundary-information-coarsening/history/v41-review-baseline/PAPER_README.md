# A2 v38 — source-pinned native revision and referee response

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 13, 2026

This stable directory contains the complete unabridged native source. Its `A2-v17` directory name is not the current revision number. The current branch is `revision/a2-v38-source-pinned-native-referee-response-2026-09-13`.

[Native main](main.tex) · [Native companion](two_collision.tex) · [Response to the v37 referee](RESPONSE_TO_REFEREE_V38.md) · [Actual verification](VERIFICATION_V38.md) · [Preservation](PRESERVATION_V38.md) · [Historical dependency audit](HISTORICAL_DERIVATION_AUDIT_V38.md) · [Complete build protocol](NATIVE_BUILD_PROTOCOL_V38.md).

## Revision identity and changes

The addressed [v37 report](../../reviews/a2-v37-external-harsh-top4-2026-09-13/REFEREE_REPORT.md) is at review commit `377efa79597776e75e3cc1d399c1986edd097aaf`, reviewing submission `6c311aa389e3af833f06f14ae98de7bfc28c1327`. The new branch descends from that review commit. Mathematical changes are at `c206a27ba01f20f1a21b780e6d71c77a837ef11d`; the complete inherited source and repaired tools are at `7d34d96a7c2dd974ab3725e009bbb584d3228114`.

The abstract and introductory rigidity theorem now specify a rank-two anchoring pair based at one channel frame and rooted signature-rigid propagation to every obstacle orbit. The short contiguity proof directly invokes the existing noncircular normalized-likelihood argument. The detailed periodic theorem, signed inverse, original-alternative moments, compact-experiment conclusions, physical acquisition and complete appendices are retained. All 52 direct main inputs and the unchanged 36-input auxiliary wrapper remain in place.

The builder now reads immutable Git-object snapshots and verifies the actual compilation inputs against them. Recorder, native entry and recursive-input coverage are mandatory. Generated companion auxiliary data have explicit producer/consumer provenance. The old mathematical files and builder are preserved under [history/v37](history/v37); the prior directory entry is [README_PRE_V38.md](README_PRE_V38.md).

## Actual verification and remaining delivery

Forty-one software-provenance regressions and six retained mathematical diagnostic families were actually executed in normal and optimized Python; each pair of outputs is byte-identical. A genuine miniature TeX integration run validates the complete new CLI and companion-auxiliary path, but its one-page entries are not A2 manuscripts. The exact native companion was separately compiled into seven pages, source-verified and inspected on all rendered pages. Its PDF and full raw local evidence accompany the revision conversation; identities and scope are in the ledger.

**C2 remains open.** The complete native main has not been built or PDF-inspected in this revision session. The hosted full-build attempt failed without executed steps or artifacts. Neither diagnostics, the companion, a fixture nor workflow configuration is presented as complete-main delivery. The full mathematical source remains available here for further independent review; no submission-readiness or journal-acceptance claim is made.
