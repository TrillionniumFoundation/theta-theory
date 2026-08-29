# Atomic main-tree migration

This staging branch contains the SHA-256-pinned clean eleven-paper source tree as ordered base64 parts. The workflow reconstructs and builds the source, checks its exact folder contract, checks out `main` separately, replaces its tracked tree atomically, and pushes one cleanup commit.

Archives created before migration:

- `archive/main-pre-11paper-cleanup-2026-08-30`
- `archive/v11-five-paper-synthesis-2026-08-30`

Expected archive checksum:

```text
566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2
```
