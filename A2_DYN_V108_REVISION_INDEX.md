# A2-DYN revision 108: canonical roofwise comparison capacity

**Active article:** `papers/A2-DYN-v108-referee-response/main.tex`  
**Full historical supplement:** `papers/A2-DYN-v108-referee-response/supplement.tex`  
**Response to the controlling referee report:** `papers/A2-DYN-v108-referee-response/RESPONSE_TO_REFEREE.md`  
**Proof ledger:** `papers/A2-DYN-v108-referee-response/PROOF_LEDGER.md`

The controlling report is `reviews/a2-dyn-v107-positive-source-external-top4-review-2026-10-14/REFEREE_REPORT.md`, frozen at commit `6811140ec51276247d75057980692d4a4d5e77b6` and blob `82cff2e2fc14e6a1eaa12b75fb41012dd155bdae`. The inherited author head is `7f660346afea9500138920ca87fef46026a7e507`, with paper tree `7f6fcd70afa7a54f6891d4d399bf370c302eb526`.

The new author branches are:

- `revision/a2-dyn-v108-microscopic-referee-response-2026-10-14`
- `revision/a2-dyn-v108-microscopic-referee-copy-2026-10-14`

## Mathematical revision

Modules 258--259 construct the complete admissible one-sided comparison pool at each original target roof. The weights are explicit and Borel, the physical overlap is one, and the endpoint-envelope capacity is bounded by the inherited paired average and uncut optical variation. The resulting source allocation is an attained pointwise maximum within an explicitly specified fixed-window envelope-certificate class. It pointwise dominates every compatible v107 fixed-family allocation at the same total cost.

The original microscopic source has the exact positive residual

`R_B_can(t) = (U_B_micro(t) - K_B P_rB(t))_+`.

The unchanged raw pointwise error satisfies

`E_M <= H_M(R_B_can) + C_M B^(-1/384)`.

The collision-uniform decay of this residual is not proved here. Neither a full raw LLT, a collision-uniform logarithmic insertion, all singular endpoint extensions, independent human review nor formal proof certification is claimed. Finite-count exhaustion is proved and explicitly distinguished from the prescribed collision-limit order. The organizing topic and target have not been replaced by a standalone comparison problem.

## Preservation and provenance

The new packet retains all 257 inherited core modules byte-for-byte and adds two, for 259 active modules. The previous article is typeset from an exact source snapshot, with new sections inserted before its appendices. All old paper directories and review reports are unchanged; no unrelated paper is modified.

The versioned `provenance/v106-metadata-supersession.json` explicitly corrects the stale v106 local identity without rewriting the frozen historical tree. `provenance/v107-final-qualification.json` records the final successful paired v107 author runs and distinguishes the theorem-bearing commit from its qualification-only successor.

## Exact-checkout qualification

Run:

```sh
bash papers/A2-DYN-v108-referee-response/build.sh
```

The dedicated workflow is `.github/workflows/a2-dyn-v108-canonical-capacity-qualification.yml`. It verifies source preservation and claim flags, runs exact rational diagnostics in normal and optimized Python, compiles both documents until references stabilize, retains the precise inherited TeX-advisory exception, checks recorder coverage of all 259 modules, and uploads PDFs, rendered pages, raw logs and exact-SHA evidence. Qualification status must be read from the actual run at the corresponding head; this index does not predeclare workflow success.
