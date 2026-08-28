# K2R231 cold replay record

Command shape (offline frozen cache):

```text
PYTHONHASHSEED=<seed> uv run --offline --with 'python-flint==0.9.0' \
  python -I -B \
  deliverables/cm2_round306b1af4k2r231_source_g_outgoing_seam_authority_independent_verifier.py \
  --verify-no-write
```

Successful publish replay:

- exit code: 0;
- wall time: 122.10 seconds;
- peak RSS: 1,084,188 KiB;
- result SHA-256: `672bd85e4313b5cbfea0173eeb2676bfbb2011e39a8833cbd8b539a1c8717d00`;
- selected rows: 95,640.

Final no-write replay, `PYTHONHASHSEED=17`:

- exit code: 0;
- wall time: 121.42 seconds;
- peak RSS: 1,085,340 KiB;
- result SHA-256: `672bd85e4313b5cbfea0173eeb2676bfbb2011e39a8833cbd8b539a1c8717d00`;
- pre/post package byte and dev/inode/size/mtime/ctime/SHA snapshot: identical.

Final no-write replay, `PYTHONHASHSEED=93`:

- exit code: 0;
- wall time: 121.59 seconds;
- peak RSS: 1,083,760 KiB;
- result SHA-256: `672bd85e4313b5cbfea0173eeb2676bfbb2011e39a8833cbd8b539a1c8717d00`;
- pre/post package byte and dev/inode/size/mtime/ctime/SHA snapshot: identical.

The first attempted invocation under the system Python failed before verification with `ModuleNotFoundError: flint`; it wrote no package artifact.  A later complete replay also correctly fail-closed on a directory timestamp model that was too strict for concurrent authorized package publication.  That model was narrowed to stable directory identity (device/inode/mode), while every selected file retained the full inode/size/mtime/ctime/path/SHA checks shown above.

Canonical receipts contain no elapsed time, RSS, temporary path, timestamp, random seed, or other live-run field.
