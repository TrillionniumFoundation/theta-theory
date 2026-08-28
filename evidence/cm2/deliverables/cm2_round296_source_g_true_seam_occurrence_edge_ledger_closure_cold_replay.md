# Round296 cold replay

Run from the `deliverables` parent directory with the eight upstream
manifests and all of their sealed members present.

```bash
python deliverables/cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure.py --seed 296071 --no-write
python deliverables/cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure.py --seed 296997 --no-write
python deliverables/cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_verifier.py --seed 296173 --no-write
python deliverables/cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_verifier.py --seed 296991 --no-write
```

Both producer invocations must report:

- edge ledger SHA-256
  `1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7`
- cell ledger SHA-256
  `c664bcb76b056faac47970a1add9be7ce906dab3212a5ab954a5388d0476ecb8`
- result file SHA-256
  `d55d9d8fe13ef98c8f07cdea91a6b5397b7f6715f85ae0f8549832ba59c1498f`
- `seed_affects_output=false`

Both verifier invocations must report:

- verification file SHA-256
  `8ec51d83459f2eac3389054b0c08a7c646973d2eac4addb7447cce6210d8b4d5`
- verification self-digest
  `90516ef3e0c6bc247d124101e089c35bd72778a9e44747a2bb78b70afc8edfc3`
- attack-suite file SHA-256
  `9564e51783d6496d3eaebf725a00581c5a812a6dd6590f6fba354097659ff826`
- 46 attacks rejected and `seed_affects_output=false`

The verifier must reconstruct the frozen sources before opening the Round296
candidate artifacts.  No invocation may report a DSU rank reduction or a
quotient-component count.
