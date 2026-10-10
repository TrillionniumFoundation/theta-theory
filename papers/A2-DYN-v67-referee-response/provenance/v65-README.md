# A2-DYN — revision 65

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Author: Qian Qi. Date: 10 October 2026.

This revision responds to the frozen v62 external report and preserves the complete v63 manuscript at `ae14ecbfa39d0d9005574155de86acecd2e8a166`. The v64-named branch resolved to that same v63 source; this directory is an independently identified revision 65.

`main.tex` is the complete manuscript. It retains all 136 old core modules and adds `137_reversible_critical_weights.tex`, `138_simple_caustic_density_profile.tex` and `139_affine_caustic_label_profiles.tex`. The new leading theorem states their actual local scope. The original pointwise arithmetic target, source normalization, exact labels and positive complements are unchanged.

Read `RESPONSE_TO_REFEREE.md` for the itemized replies, `PROOF_LEDGER.md` for theorem scopes, and `SPECIALIST_AUDIT_MAP.md` for the next mathematical audit. Prior metadata is archived under `provenance/v63-*`. The bibliography is append-only.

Run `bash build.sh` from a clean repository checkout with native TeX and the documented Python dependencies. The read-only workflow `.github/workflows/a2-dyn-v65-qualification.yml` checks the exact event source, reruns inherited and new finite diagnostics in normal and optimized Python, builds the complete article without unresolved references or overfull boxes, renders the new proof pages by their actual labels, and publishes a PDF/source/evidence artifact.

The branches are `revision/a2-dyn-v65-referee-response-2026-10-10` and `revision/a2-dyn-v65-referee-copy-2026-10-10`. A successful build is not a proof of the missing ordered long-count height estimates or independent human review.
