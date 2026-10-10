# A2-DYN — revision 71

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The manuscript is `main.tex`. The new proof is in `core/155_pooled_physical_collar.tex` and `core/156_two_sided_current_and_raw_budget.tex`. All 154 earlier core modules remain compiled and byte-identical; the preceding opening is compiled in `appendices/v70_frontmatter.tex`.

Revision 71 starts from the v70 controlling report, not from an earlier unreviewed checkpoint. It keeps the original physical family, actual section, exact four-coordinate record, section normalization, arithmetic transition kernel and zero classes, and unrestricted pointwise endpoint.

The new theorem recovers part of the original angular loss by pooling unused receiving capacity **within one exact label and at a common roof**. The recovered controlled source has height `O(K chi^6)` and contains the old controlled source. The new loss is a subsource of the old loss and is bounded by the positive excess of a signed two-sided physical current. The complete selected-source theorem applies on an explicit receiving-reserve class, not automatically to every Lorentz record.

The unrestricted ordered net-current, original outside-source and complete first-incidence heights are not proved. Consequently the full pointwise endpoint and unrestricted same-roof consequences retain false proof flags. See `PROOF_LEDGER.md`, `RESPONSE_TO_REFEREE.md`, `SOURCE_MANIFEST.json` and the active `SPECIALIST_AUDIT_MAP.md`.

Run `bash build.sh` from a Git checkout for exact-source qualification. In an extracted source archive, `python3 tools/verify_v71.py --local` performs the explicitly local source/finite checks without claiming a frozen Git checkout. The read-only GitHub workflow produces the full PDF, exact source archive and actual proof-page renderings. Its finite checks and build are not continuum proof certification or independent human review.
