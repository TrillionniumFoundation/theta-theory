# Reproducible build

Run `python3 seal.py` only BEFORE the ordinary source commit. Thereafter:

```
python3 verify.py
python3 regression.py
python3 -O regression.py
python3 build.py --prepared-root /path/to/repository --output /tmp/r56-output --retained --source-sha FULL_SOURCE_SHA
```

The native builder is a hash-pinned reuse of the established isolated implementation, with only publication names/retained predecessor changed. It performs two isolated three-pass native builds, compares bytes, checks actual recorder inputs, references, labels and overfull boxes, verifies immutable source manifests, compares ordinary/-O outputs, and recursively builds the complete R54 predecessor and its retained chain. It never runs an old publisher. Native and historical regression categories remain separate; nested counts are not summed as independent tests.

`--source-sha` is an asserted binding requiring GitHub readback; an uncommitted preflight has no source SHA. Hosted artifact publication must make the artifact commit a direct child of immutable source. Final independent reconstruction downloads the ACTUAL remote artifact, snapshots all inputs, rebuilds outside the source tree and compares all delivered PDFs. Cross-environment PDF byte differences are not concealed; normalized text and rendered comparisons are recorded separately. Final evidence is a distinct child commit.

Build success is delivery consistency, not mathematical correctness, priority or acceptance. The ordinary article is native; full retained companions are optional provenance. A full retained build is not a fresh line-by-line re-certification of all historical proofs or the entire repository.

The R56 adapter verifies R54's existing pinned R53 report rather than injecting the R32 input that the base R52 builder supplies to its own predecessor. An initial local preflight caught this predecessor-inventory mismatch; only the new adapter was corrected, never a retained manuscript or its manifest.
