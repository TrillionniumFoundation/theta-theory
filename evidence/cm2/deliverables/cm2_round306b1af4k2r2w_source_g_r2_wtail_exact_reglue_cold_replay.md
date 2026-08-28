# K2R2W cold replay

- The final producer full replay explicitly bound theorem kind
  `ARTIFICIAL_FACE_REGLUE_EXACT_V2` and reconstructed result SHA-256
  `e3231a108032cac6fc0f7c686e18fccbc7b3c48c150542d5c1276578972b7ee0`
  and theorem rows SHA-256
  `378b3f6a45c7f66add5a3396e0ce63ba7ff6cdd5a00cb9d49ef8727219fe7113`.
- First independent-verifier attempt fail-closed on object insertion-order
  sensitivity in its comparison routine.  That verifier candidate was not
  accepted as a receipt.  The routine was corrected to compare exact key sets
  and recursively type-strict values, preserving bool/int separation.
- The final independent verifier was run twice with byte-identical JSON output.
  Both runs exited `0`; the measured first run took `119.40 s` with peak RSS
  `25,200 KiB`.  Seven upstream pins and four package pins passed two-pass and final
  rehash; 5 ordered tables, 4 blocked rows and 10 attacks passed.
- No producer code was imported or executed by the independent verifier.
- Final credit remains zero; no physical-equivalence or half-open-owner theorem
  is claimed.
