# v9 homological pressure review bundle

This directory contains the complete UTF-8 source tree for the v9 candidate as a reproducible `tar.gz` bundle.

Controlling branch: `series/v9-homological-pressure-2026-08-29`.
Base mathematical platform: the v8 compact periodic finite-horizon Sinai/Liouville family, upgraded to the coordinate-free platform `TL2-HOM-v1`.

The source bundle contains five manuscripts, build tools, theorem manifests, status files, and hostile-audit records. Extract with:

```bash
tar -xzf theta_v9_source_only.tar.gz
make -C papers all
python tools/verify_v9.py
python tools/verify_v9_deep.py
```

The locally built circulation package, including PDFs, is retained separately as the external-review artifact. This GitHub bundle records source and provenance; successful build or machine checks do not constitute mathematical certification or peer review.
