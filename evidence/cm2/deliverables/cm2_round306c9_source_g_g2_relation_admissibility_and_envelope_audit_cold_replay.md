# Round306C9 Cold Replay

- Environment: `env -i`, `python3 -I -B -S`, `LC_ALL=C`, `LANG=C`, `HOME=/nonexistent`.
- Mode: independent verifier `--verify-no-write` against the first byte-identical candidate.
- Status: `PASS_INDEPENDENT_5264_GRAPH_DOMAIN_AND_15392_RELATION_ADMISSIBILITY_REPLAY__15382_CANDIDATES_10_NO_INCIDENCE__ZERO_SUPPORT_CREDIT`.
- Elapsed: `46.55s`.
- Peak RSS: `1,360,048 KiB`.
- Exit status: `0`.
- Mutating `openat` calls: `0`.
- Deliverables mutation syscalls: `0`.
- Standard-output writes: `1` receipt write.
- Producer imported or executed: `false`.

The replay independently recomputed the exact interval endpoint counterexamples for all `4,432` R235 target graphs, rebuilt both ledgers, and matched the result and both gzip ledgers byte for byte. Formal support credit remains zero.
