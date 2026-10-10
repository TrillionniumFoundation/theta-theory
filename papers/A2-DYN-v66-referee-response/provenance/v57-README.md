# A2-DYN revision 57

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. Revision 57 starts from the v56 external report at `f3d5a8a6238497950ecde6c6f276e3c80624fc4a`, reviewing author SHA `4292877a5100c4c22975d9d563a1c54793139db4`. It keeps the original actual-return record, source, arithmetic and unrestricted pointwise target.

The new Part I proves a pressure--drift estimate for the existing moving spectral peaks: squared drift from the physical mean is bounded by spectral damping. It obtains a uniform Gaussian envelope for the complete arithmetic transition sum. Together with the inherited local raw-variation theorem and the actual return fourth moment, this proves total-variation convergence on the entire untruncated mixed record space at each fixed return index. The arithmetic reference is the normalized positive part of the full transition density, not a central truncation.

The second new section proves the joint collision/actual-return bridge law in observation variation and path bounded-Lipschitz dual. The two limit bridges are linearly coupled, not independent. Every record-only observation kernel contracts this mixed norm. Conditioning on its full selection event has explicit denominator-loss bounds when its reference mass dominates the approximation error.

All 120 inherited core modules, 159 inherited Python files, the bibliography and compiled appendices are byte-identical. The former three leading statements and front matter are retained verbatim in `appendices/v56_frontmatter.tex`; the former full main source and status files are archived. Both new core modules are compiled, for a total of 122. The leading journal narrative now has one theorem; no old theorem is deleted.

Run `bash papers/A2-DYN-v57-referee-response/build.sh` in a full checkout. The read-only v57 workflow checks the frozen source, report, ordinary Git tree, all inherited identities and labels, finite diagnostics in normal and optimized modes, native TeX and theorem-page rendering. Dynamic receipts, not this README, identify actual successful executions.

The global variation theorem does not close the incidence or clearance essential-height estimates. The unrestricted pointwise density theorem, unrestricted same-roof bridges, concrete unmodulated arithmetic criterion and independent specialist audit remain distinct requirements. See `RESPONSE_TO_REFEREE.md` and `PROOF_LEDGER.md` for the exact scope.
