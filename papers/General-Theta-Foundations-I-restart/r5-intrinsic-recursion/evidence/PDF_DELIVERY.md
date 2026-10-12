# PDF delivery and execution boundary

The compiled new manuscript has 20 pages and 451573 bytes. SHA-256:
`e06a2bdeae6b85ce0dcf1e551e643c90b9cb12f5eadf50092f93fb9921c4493a`.

It is supplied as a conversation PDF and inside the referee package. The binary `r5-intrinsic-recursion/paper.pdf` has NOT been published as a Git blob in this delivery. The remote branch contains the complete native manuscript, audits, deterministic build scripts, source manifest, and actual local build/verification receipts. The build-evidence child is not a binary-PDF publication commit.

The proposed new GitHub Actions workflow was blocked before writing; no workflow was changed. There is no hosted-CI run for the source SHA. The successful builds and regressions reported here actually ran in the local container, bound to the exact remote native paper subtree. Neither a full-repository checkout nor a hosted-CI success is claimed.

Reproduce the new PDF in the paper directory:

```sh
python3 build.py --source-sha e78b9b54f3f6c7fe8bc7fb23bb9575f7763ea545 --source-tree 0c82472de3707069e03726d700351184838eb865
```

The new paper and the preserved supplement each rebuilt identically in two isolated directories in the current TeX environment. The supplement's current-environment rebuild is not byte-identical to the historical PDF produced by an earlier TeX version; its historical source and published PDF remain unchanged. The relevant two hashes and compiler distinction are recorded in the receipts.

Normal and optimized runs agree: 11510 new checks plus 42162 inherited checks, with 8 new and 861 inherited negative controls rejected per mode. These are finite regression/integrity checks, not proofs of continuum mathematics or independent referee endorsement.
