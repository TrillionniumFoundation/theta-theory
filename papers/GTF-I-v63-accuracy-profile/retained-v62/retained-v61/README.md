# General Theta Foundations I — Revision 61

**Spectral Entropy and Sharp Stochastic Widths of Compact Group Experiments**

The quantitative article is `quantitative.tex` / `paper.pdf`. The independent structural article is `structural.tex` / `STRUCTURAL_PAPER.pdf`. The complete research edition is `main.tex` / `COMPLETE_REVISION.pdf`; it retains the full mathematical development rather than serving as a third submission object.

The predecessor is v59 final head `310dabfa4020a7c4da2d7999c59ea692dede7850`. The two controlling r39 reports reviewed v58 and are frozen in this directory. The existing v60 preparation branch is untouched. This revision does not alter other manuscript branches.

## New mathematical content

The sharp occupation theorem replaces a repeated logarithmic mixing-block cost by a single entropy budget along narrow cuts. Its full proof treats zero centroids, arbitrarily small label masses, nontransitive actions, compactly supported densities with zeros, and unrestricted intervening widths. It assumes a full action L2 spectral gap, not contraction of only the original finite-dimensional matrices.

For matching least-orbit and target-orbit dimensions it gives sharp polynomial width, including `Theta(N^(d-1))` for legal d-dimensional density matrices. A second rational Bloch experiment has numerical noisy bounds using the classical LPS norm `sqrt(5)/3` and exact profile `5^t`, stable for error at most `25^(-N)/16`. The original rational-unitary pair and its robust exponential profile remain intact, now with a matching linear noisy law but no newly computed Bourgain–Gamburd constant.

The v59 causal classification, adaptive instruments, generic compiler and structural results are preserved as inherited mathematics. The interpretation of classical repeatable probes is not quantum measurement. No optimal leading constants, full joint error/horizon crossover, arbitrary irreversible-system classification, independent priority clearance or A/B/C/D analytic closure is asserted.

## Reconstruction

From this directory run:

```sh
python check_revision.py
python -O check_revision.py
python build.py --check-isolated
python qubit_compiler.py --input RAMANUJAN_INPUT.json --horizon 2 --amplitude 1/2 --max-labels 100 --output lps-example.json
```

The builder requires Python, SymPy, PyMuPDF and TeX. Optional SciPy proposes candidate facets only; every accepted row is verified with exact rational arithmetic and exhaustive triples are the fallback. Dependency versions of the actual qualification are in `evidence/BUILD_RECEIPT.json`.

`PRESERVATION_MANIFEST.json` freezes all 285 predecessor native files. `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `RESPONSE_TO_REFEREE.md` and `LITERATURE_AUDIT.md` distinguish written proofs, finite tests and imported inputs. `evidence/THEOREM_LOCATIONS.json` gives actual compiled numbers and pages. The native-only archive is `evidence/CORE_SOURCES.zip`; both focused and full review archives are supplied.

Publication qualification is followed by a separate read-only Actions run on the exact final review head. That verifier emits an external `FINAL_HEAD_ATTESTATION.json`, not a self-referential in-tree success claim. Source identity and reproducible rendering are not a formal proof certificate, a cryptographic author signature, or journal acceptance.
