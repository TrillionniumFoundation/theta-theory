# A2-DYN, revision 63

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete manuscript is `main.tex`. This revision responds to the v62 external report at `0ed5b59fdcf9e4f38e621307da4a864cc5a83c8b`, from the reviewed author SHA `45425f65832e3f1e69336c791de5fc32f8ed22bb`.

New modules 135-136 quantify buffered caustic separation and vertical tube length in both the actual collision count and incidence cap. They retain the auxiliary collision graph, use fixed-block real quantifier elimination with coefficient bounds, and apply the resulting determinant threshold on the unchanged first-clearance source. The geometric overcover carries no measure. The cap of the actual source is chi; the reference cap is chi/2.

For a fixed C0 the budgets are `E_m=ceil(2^(C0 (m+1)^16))` and `K_m=2^E_m`. They bound the separation and tube moduli, but are not count-uniform or central-scale decay estimates. The complete retained caustic source is positive and has a mass estimate, not a proved essential-height estimate. The original pointwise raw-return target and its ordered incidence/clearance requirements remain in the manuscript.

All 134 inherited core modules, 183 inherited Python files, every compiled appendix and all 1788 old mathematical labels are retained unchanged. Fifteen v62 source/editorial snapshots are under `provenance/`. The bibliography is append-only. `RESPONSE_TO_REFEREE.md` addresses report sections 30.1-30.8 and its technical comments. `PROOF_LEDGER.md`, `JOURNAL_ROUTE.md`, and `SPECIALIST_AUDIT_MAP.md` distinguish the new proof, imported inputs, and remaining endpoint requirements.

Run `bash papers/A2-DYN-v63-referee-response/build.sh` in the exact checkout. The read-only qualification workflow checks source and report identities, normal/optimized finite diagnostics, native typesetting and theorem-page rendering. Its dynamic receipt records the actual event SHA and run ID; a build is not an independent mathematical audit.
