# One-article submission and repository archive

## Journal route

Submit `main.tex` and its generated PDF. Its only source dependencies are `references.tex` and twelve `core/*.tex` files. Sections 1–8 retain the full active scalar reconstruction, period, bit, dyadic and adversarial-calibration proofs. Section 9 adds stationary fixed-footprint reconstruction and its quantitative lemmas. Section 10 compares information categories. No external historical manuscript is required to prove an active theorem.

`SOURCE_PINS.json` declares exactly one journal document. The validator produces `verification/current/A2-v34-journal-source.zip` with only the active TeX sources, excluding `archive/`, validation outputs and nested supplementary names. The response letter is editorial correspondence, not another proof volume.

## Repository provenance route

`archive/v33/main.tex` is the complete reviewed v33 manuscript. Its original `retained/v32/` contains the complete v32 manuscript; successive original retained paths continue through the earlier scalar, marked-law, moment and relative-law developments. Their original `SUBMISSION_MAP.md` files remain historical records, not current submission instructions. The entire archive has native tree `213cecf77265c5ebea98791a99126b9def5d25f0`.

Validation hashes this full tree and reruns the v33/v32 diagnostic and contract suites. It does not rebuild the sixteen historical documents or claim that their historical names define the current journal package. The v33 hosted sixteen-document pass remains its own recorded result. Current read-only CI builds the one current article at the exact triggering SHA.
