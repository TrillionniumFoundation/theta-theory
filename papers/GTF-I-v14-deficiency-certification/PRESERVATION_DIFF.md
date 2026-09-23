# Exact preservation map — v14

The parent is the published v13 commit `e8a5354659a65c3c909cd927c2f4f628ea1b1a6c`. Its exact compiled source closure contains 319 files. `INHERITED_INPUTS.json` records all their SHA-256 values; the build checks every value before and after compilation. No v1–v13 source is edited in place.

The canonical v14 `core.tex` imports the four v13 mathematical sections directly: intrinsic deficiency, endogenous tasks, regenerative risks, and active hard-sphere dynamics. Two new files append subsections to the intrinsic and physical sections. The full v13 theorem statements and proofs remain in the canonical manuscript. The new introduction replaces only the current article's framing; the unchanged v13 introduction is included in the historical part of `development.tex`.

The local `preserved-core.tex` differs from v13's file only in these two input paths:

- `infinite-horizon-annotated` becomes `../GTF-I-v13-intrinsic-deficiency/infinite-horizon-annotated`;
- `operator-memory-annotated` becomes `../GTF-I-v13-intrinsic-deficiency/operator-memory-annotated`.

Their target files are unchanged. All other old-body inputs and the historical supporting bodies are retained. The predecessor companion auxiliary file has 717 labels, including the previous article's introduction. The new build requires all of them in the new complete development and checks identical numbering for every label shared by the new canonical and complete views.

New front matter changes the revision number and summary, not the mathematical assumptions. The bibliography copies preserve all original entries and add the inspected Weisshaupt and Basu sources and the Paull–Unger bibliographic record. The latter's full proof was not retrieved, as the audit states.

The new source directory, its dedicated workflow, and the later referee entry are the only intended repository additions. No default, review, A2 or pre-existing GTF revision reference is updated by this delivery. A frozen referee branch will identify the published v14 without changing its source-bound PDF receipt.
