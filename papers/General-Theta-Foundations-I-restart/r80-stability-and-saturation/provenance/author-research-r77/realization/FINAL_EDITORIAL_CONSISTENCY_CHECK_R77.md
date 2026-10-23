# R77 final editorial and internal-consistency check

## Scope and evidence

Read the current R77 root `README.md`, `START_HERE.md`, `SOURCE_PROVENANCE.md`, `PRESERVATION_MAP.md`, `RESPONSE_TO_REFEREE.md`, `PROOF_AUDIT.md`, `RESEARCH_STATUS.md`, `LITERATURE_AND_PRIORITY.md`, and generated theorem/dependency maps. The audit and status files were byte-identical to the detailed author records already examined. This was an author-team AI editorial/consistency check, not a new referee report or a re-review of the closed inherited proof bodies. No current source file was edited.

No current source/label/link blocker was found. The pending sibling publication files and the forthcoming compact provenance delta were treated as scheduled integration work, as requested.

## Precision corrections for integration

1. **Carry the commuting qualification through the response.** The main mathematical statement, status, proof audit, and theorem map correctly say that the **cost/effect operators commute**, and do not assert commutation of the reset CP maps. Three shortened descriptions in `RESPONSE_TO_REFEREE.md` should use the same qualification:
   - R65-17.6: “its rational commuting realization”;
   - R65-17.7: “rational commuting reset data”;
   - R65-18.29: “The commuting hardness example”.

   Suggested common replacement: “the rational reset realization with commuting cost/effect operators”. This is a precision correction, not a defect in the proof or reduction.

2. **Empty dependency-category prose.** The generated addendum prints “None; the proof is given directly from the listed hypotheses and classical ingredients” for an empty inherited-mechanisms category, including rows with nonempty direct logical prerequisites. The declared JSON correctly lists those prerequisites. For an empty category the generator should print “None listed in this category” so that the prose does not appear to deny the immediately preceding dependencies.

3. **Optional version pin for the new primary source.** The literature table calls `https://arxiv.org/pdf/1505.08031` the “original v2 manuscript”, while its native bibliography names v2. Using `https://arxiv.org/pdf/1505.08031v2` would pin that description. The current DOI `10.1016/j.laa.2016.12.023`, authors, journal, volume and pages agree with the checked primary metadata. This is a reproducibility improvement, not an identified citation error.

## Completed consistency checks

- All **18 current relative Markdown links** resolved. Four links into the sibling publication directory remain deliberately pending final publication and were not classified as broken deliverables. Exact inline paths under `sections/`, `inputs/`, `provenance/`, and `companion-r58/` that were named in the inspected wrappers also resolved.
- `THEOREM_INDEX.json` and `THEOREM_DEPENDENCIES.json` had identical label sets and identical document/number/page/source locators for **235 statements**, including **15 additions**. Every referenced source file existed.
- `python build_theorem_map.py --check` completed with status **PASS**, reporting 220 inherited and 15 added records. Its scope is dependency-map/source consistency, not mathematical proof verification or native compilation.
- The response contained exactly one heading for each of the **ten R65-17 requests** and each of the **forty R65-18 comments**. Older original-paper R62/R61 obligations had their distinct crosswalk and source identities; they were not misrepresented as reviews of R77.
- No stale claim that R76 is the current revision, no use of an old PDF as the current supplement, and no prospective R77 strict/hosted PASS were identified. R76 page counts and historical receipts are explicitly marked as predecessor evidence. Current final execution is delegated to actual source-bound publication receipts.
- The unrestricted **log-log lower versus logarithmic upper** distinction is consistent across the response, status, proof audit, literature record, and generated map. The original general-`M` squared-sign risk problem remains separately open. The stronger physical-dictionary rate retains its Born/density and arithmetic hypotheses. The no-future-test-code condition is explicit in the detailed response and new proof.
- The exact reset cover retains positive exposure, tied actions, initial-row reuse, and the stated stopping interface. Its gap certificate is not presented as the full constrained frontier. The PSD counterexample is correctly classified as showing the need for exposure.
- Shared preparation keeps common transitions/decoder, counted pure initial labels, common means for exact low-contrast synthesis, and the different-means obstruction. The sharp families are not promoted to universal formulas for every preparation family.
- Literature records distinguish full-text inspection from publisher metadata/abstract access, credit classical support antichains and control theory, and avoid invented human approval or exhaustive priority clearance.

The check was performed before the final source seal and commit. Rebuilding the affected generated prose after any correction and completing the final source-bound verification remain integration steps; this report does not predict their result.
