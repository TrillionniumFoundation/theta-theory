# Supplement: frozen-to-integrated 338 comparison

Date: 2026-10-23, approximately 14:22 UTC.

## Result

The integrated file differs from the previously reconstructed frozen candidate only in the four textual hunks listed below. No formula, constant, substantive proof step, estimate, or mathematical conclusion has changed. The previous internal mathematical reconstruction therefore applies to this integrated proof body, with its original scope and limitations. This is not an external referee approval or a re-audit of the whole manuscript.

## Compared files and SHA256

Frozen source:

`/workspace/shared/paper-a2dyn-dot/derived338.tex`

SHA256: `2ef5dfa9ac8c3b586af23c3323f5b2e77a1118fadbc9db151dfb63124c95bf01`

Integrated source:

`/workspace/shared/paper-a2dyn-dot/repo/papers/A2-DYN-selected-singular-clearance-author-revision/core/338_selected_clearance_singular_multiplier.tex`

SHA256: `2a4ae1553501244196b0de9d63f648d1f6603795092da150f8355a22c5b8691e`

Existing reconstruction record, preserved byte-for-byte:

`/workspace/shared/paper-a2dyn-dot/verification-derived338-selected-source.md`

SHA256: `95472eeb4f147ff0046de8c49ba2dfa8a621848709dc2fa980a79aa8d6b11789`

## Exact difference classification

1. The initial TeX comment changes from an unintegrated working-draft description to an author-continuation description with reconstruction recorded separately.
2. The first lemma explicitly adds R in [R_-,R_+] and specifies integer m>=1. These make the previously inherited physical-radius and collision-count domains explicit.
3. After the annular minimization formula, an added sentence specifies that the displayed value is the exact minimum of that upper bound over b>0, not a claim of the best possible constant in the theorem. This correctly limits the optimality claim; the constant and its derivation are unchanged.
4. The deep-payment theorem explicitly specifies finite integer m>=1, the original outer B, and integer D>=0. This makes the previously inherited domains explicit and does not change either finite-depth condition or the ordered-limit conclusion.

## Verification method and preservation

A complete `diff -u` returned exactly those four hunks. As an additional byte-level check, applying exactly the four displayed textual substitutions once each to the frozen bytes reproduced the integrated bytes exactly. This check is a comparison of the actual files, not an assumption based on the author's description.

The frozen file, integrated file, and existing reconstruction record were read only. Their hashes were checked at the start and again after the comparison. This supplement is a new separate file; the existing report was not edited. The mathematical reconstruction was not unnecessarily rerun.

The shallow outgoing/same-roof shortage and separate raw local-limit/inverse dependencies remain unresolved, as already stated in both proof versions and the original review.
