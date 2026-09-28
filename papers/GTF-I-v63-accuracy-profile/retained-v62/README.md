# General Theta Foundations I — Revision 62

## Independent articles

**Quantitative:** *Spectral Entropy, Return-Free Stochastic Widths, and Vanishing Error* (`quantitative.tex`, `paper.pdf`).

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* (`structural.tex`, `STRUCTURAL_PAPER.pdf`).

Each focused article includes every proof it uses. The complete research edition (`main.tex`, `COMPLETE_REVISION.pdf`) preserves all preceding active statements and adds the new proofs. It is archival, not a third submission. All 344 native v61 files are retained byte-for-byte under `retained-v61/`, including their nested histories; these archives are not hidden prerequisites of either focused paper.

The new quantitative proof allows arbitrary deterministic physical drift between independent spectral steps. It retains a full Koopman action gap, but needs no identity command or return words. Keeping the centroid-loss budget gives a joint amplitude/accuracy inequality and a matched law when the inverse slack is subexponential in the horizon. The explicit six-command rational LPS experiment has exact profile `5^t` even without an idle instruction, and width `Theta(N/epsilon_N)` for subexponentially vanishing positive tolerance. The complete exponentially small crossover and optimal leading constants are not claimed.

The structural paper derives an all-error strong converse from the classical finite-state tail-event principle, finite-product compactness, and one common diagnostic cycle. In the repeatable fresh-probe model, the future-response cardinality is the eventual minimum at every fixed whole-transcript TV error below one. The intermediate tail lemma also applies to nonhomogeneous irreversible hidden emission processes; the full classification still requires repeatable nondisturbing classical probes.

## Review identities

- Base v61 final head: `2c215579336a253585499328f19a647446445dc4`.
- External r40: `4a99da0aab823418d95631d5dbbd8e9b8178994d`.
- Proof/pipeline r40: `02c642d3c08774d2dbaee939ffb2eee57b545f92`.
- Work branch: `revision/general-theta-foundations-i-v62-referee-response-2026-09-28`.
- Referee branch: `revision/general-theta-foundations-i-v62-referee-ready-2026-09-28`.

## Reproduction and compact submission package

`python build.py --check-isolated` verifies frozen source and reports, executes the new and inherited finite tests in normal and optimized Python, runs rational compiler examples, typesets the complete document set, and rebuilds the native archive in isolation. The frozen reports must be present for publication qualification. `--local-missing-evidence` is a local-only preflight and cannot qualify publication.

`evidence/JOURNAL_PACKAGE.zip` contains only the two focused PDFs, their active TeX sources, a minimal build script, the response, and a compact manifest. It excludes all retained histories, predecessor PDFs, and the full native archive. Its own TeX sources are independently rebuilt and compared page by page. `evidence/REFEREE_PACKAGE.zip` supplies the full preservation/reproduction package for deeper audit.

The final source and publication identities are recorded in the root review entry. A separate `contents: read` workflow verifies the exact connector-authored final request commit and writes its attestation outside the reviewed tree. Build success is source/artifact evidence, not formal proof verification, independent priority clearance, signature, or journal acceptance. No A/B/C/D analytic closure is assigned.
