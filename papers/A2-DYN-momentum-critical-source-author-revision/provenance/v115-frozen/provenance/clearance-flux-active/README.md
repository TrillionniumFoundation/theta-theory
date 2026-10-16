# A2-DYN — clearance-flux author revision

This is a complete buildable **active** English manuscript extending the exact revision-112 active author source. It is not a referee review, not a replacement physical model, and not a claim that the complete raw pointwise LLT or four-coordinate inversion has been proved.

## New proof modules

270 proves exact near-miss flux and all-depth mass bookkeeping; 271 proves grazing-uniform transverse strip geometry with the correct time orientation; 272 proves uniform propagation in an explicitly defined stable-test seminorm, conditional on the retained curve-growth input; 273 proves exact original joint-record disintegration and states the missing pointwise bridge without claiming it.

The previous ten active proof bodies and model/input files are unchanged. The unmodified downloaded active packet is in `provenance/v112-active`. The recursive older archive remains immutable in the source repository and is pinned, but was not fully materialized here. See `HISTORY_PRESERVATION_AUDIT.md` before interpreting the packet as a full historical export.

## Build

Requirements: Python 3 with NumPy and SymPy, pdflatex, pdfinfo, pdftoppm and the LaTeX packages used by the original manuscript (`amsart`, `lmodern`, `microtype`, `hyperref`, `mathtools`).

```bash
./build.sh
```

This checks local blob identities and preservation, runs inherited and new diagnostics under normal and optimized Python and compares their outputs, runs three LaTeX passes, checks references/labels/overfull boxes, and renders every page. The result is `manuscript/A2-DYN-clearance-flux.pdf`.

`tools/check_source.py --repository` is the separate strict Git-history check after this add-only packet is committed on a real checkout descended from the pinned controlling-review commit. It is not silently passed in this standalone local delivery repository.

## Status and evidence

Read `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, `PUBLICATION_STATUS.json`, `LITERATURE_AUDIT.md`, and `VALIDATION.md`. No independent human certification, new remote CI completion or remote push is claimed. The proof of the remaining normalized low-incidence-load shortage is still missing; no clearance source was removed using a weak norm as though it were pointwise roof height.
