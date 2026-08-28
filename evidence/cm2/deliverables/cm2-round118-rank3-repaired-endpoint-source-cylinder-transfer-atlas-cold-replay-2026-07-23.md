# Round118 double cold-replay record

Date: 2026-07-23

Two fresh temporary directories were created independently.  In each directory the producer
generated a new certificate and the independent verifier generated a new verification file.
All four commands exited zero; each verifier reported `PASS` and rejected 42 hostile tests.

| artifact | cold A SHA256 | cold B SHA256 | canonical SHA256 | byte comparison |
|---|---|---|---|---|
| certificate | `91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f` | `91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f` | `91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f` | `PASS` |
| verification | `240b9f0dc15257b5dd9309acdc2129910f5a2a8231cc9afc45f0739b258fd85b` | `240b9f0dc15257b5dd9309acdc2129910f5a2a8231cc9afc45f0739b258fd85b` | `240b9f0dc15257b5dd9309acdc2129910f5a2a8231cc9afc45f0739b258fd85b` | `PASS` |

Replay command template:

```bash
python3 deliverables/cm2_round118_rank3_repaired_endpoint_source_cylinder_transfer_atlas.py \
  --output "$COLD_DIR/certificate.json"
python3 deliverables/cm2_round118_rank3_repaired_endpoint_source_cylinder_transfer_atlas_verifier.py \
  --certificate "$COLD_DIR/certificate.json" \
  --output "$COLD_DIR/verification.json"
```

Four `cmp -s` checks passed: cold A versus cold B for each artifact, and cold A versus the
canonical artifact for each artifact.  The cold outputs were generated outside the workspace;
no frozen upstream or gate file was modified.
