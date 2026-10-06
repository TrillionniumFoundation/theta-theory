# A2-DYN revision 17

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The author baseline is v16 at `2054310e587e576ce593112c30cdfabac6742105`; the controlling report is the v16 review at `b0b7ddfcd90f493e02254742b33174e9108fc5a7`. The topic, physical table, actual section and raw mixed-density target are unchanged.

## New proofs

`core/38_peripheral_return_phases.tex` improves endpoint deletion from a supremum estimate to a centered second-moment estimate. It treats the collision frequency and constant phase jointly, including the cancellation line, and lifts an arbitrary per-return phase exactly. Theorem H proves a joint local physical/spectral defect bound under the quadratic budget `rho^2 K(H,rho)<=a`, replacing the earlier linear-frequency budget at spectral parameter one. On the original annulus it permits explicitly quantified peripheral arcs and subexponential BV budgets.

`core/39_compressed_return_resolvents.tex` constructs finite-rank compressions of the genuine unbounded return operator. A normalized grid vector has supremum plus zero-extension BV norm at most `C/h`. An exact orthogonal residual identity converts physical function defects into local peripheral resolvent bounds, including non-normal matrices and approximate vectors. A separate projection-telescoping estimate compares finite powers with the unmodified characteristic function.

All 37 inherited core files, all inherited diagnostic scripts and the bibliography are byte-identical. The exact six inherited edits are confined to `main.tex` and replayed by `tools/verify_v17.py`. The article includes all old theorem labels and the two new sections.

## Verification

Run `bash papers/A2-DYN-v17-referee-response/build.sh` in a checkout. The build checks source identities and exact edits, normal/optimized finite algebra, the inherited diagnostics and full native TeX. The exact-SHA workflow stores the PDF, logs, source archive and dynamic receipt in its artifact. Successful execution is not continuum proof certification.

`RESPONSE_TO_REFEREE.md` answers the latest report item by item. `PROOF_LEDGER.md` and `PERIPHERAL_OPERATOR_INPUT_MAP.md` record dependencies and scope. The quantitative spectral-phase theorem is local, and the operator theorem is for the stated compression. A full-circle estimate, mesh-uniform uncompressed power decay, the complete complementary integral and raw second-derivative sum are not claimed proved.
