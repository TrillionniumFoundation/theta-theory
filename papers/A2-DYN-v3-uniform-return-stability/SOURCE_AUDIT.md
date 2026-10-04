# A2-DYN v3: source and report audit

## Exact inputs

- Remote A2-DYN v1: `36f1365041de95ca478739a1e2984734c72f95aa`; repository tree `ab31ca44bd101d45f28836563c4f24ddd553b725`; paper subtree `f1feba6b26237efd5a796a5c224c845aab095b53`.
- Locally delivered v2 archive: SHA-256 `0b4be3de2b0035b268dcc39cf75d27888f8c83d3181ce2151a11509e41ff650d`. It was mounted in this conversation and extracted, not inferred from a filename. The archive did not establish a remote v2 commit.
- Frozen geometry v43: `4557df22f5c72bc80943690ecd6c2e39de3734ab`.
- Located geometry final report: `reviews/a2-v43-external-top4-final-rereview-2026-10-04/REFEREE_REPORT.md`, blob `d91833561bb85fcb1b4ac44f4de10482a1e17949`, review head `af2390e3073acf8ccd90b10d7566e30cbf18c425`.

## Report discovery boundary

The branch searches included `a2-dyn` with its continuation exhausted, `dyn`, `A2`, and the A2 entries among `review` branches. Before this revision, the only A2-DYN-named branches found were the research and referee-copy aliases of v1. The v1 paper subtree was inspected, and its `SPECIALIST_REVIEW_BRIEF.md` was read. That brief is explicitly not a completed referee report. The geometry report was read and excluded as a dynamics referee source. This records the search scope; it does not assert that a report cannot exist at some unlocated path.

## Preservation and new content

`PROOF_BASELINE.json` pins the v2 proof blocks and labels and includes the v1 baseline. The active TeX closure has 28 proof blocks and 78 labels. Every v2 proof block, including its begin/end delimiters, is preserved byte-for-byte. The unchanged physical, periodic, edge, inversion and downstream core files are hash checked. The new proofs live in `core/11_return_stability.tex`; introduction and status passages were updated without changing older proofs.

The new core subtree was uploaded as `6e77aa7666558fb71810bc02194a2da8f66e8ac2`, which agrees with the independently computed local Git tree. The first complete manuscript was published at commit `25bbbef23f253486e82fdade3656e856e4891cd0`. Subsequent support-file commits leave that mathematical core unchanged. All changes are additions under the new A2-DYN v3 paper directory, with a scoped build workflow if present; old papers, reviews and main are not edited.

## Reproduction boundary

The four retained finite diagnostic scripts are copied without alteration. They use only the Python standard library. `verify_v2.py` reads finite candidate coordinates but imports no author optical solver. `audit_v3.py` checks source closure and preservation and finite algebra for normalization and conditioning. None proves the infinite period family, L1 compactness, an LLT, or a continuum spectral bound. Those conclusions must be assessed from the analytical text.

Local PDF/build evidence is bound to manuscript hashes. Remote commit publication is verified separately. No local receipt is relabelled as remote CI or independent human review.
