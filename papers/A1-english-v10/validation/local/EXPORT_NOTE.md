# Local receipt export
This directory exports the original local BUILD_REPORT.json and SOURCE_MANIFEST.json.
Its operation log paths describe that original execution environment; local per-test
JSON and log files are not included in this compact source transfer. The complete
fresh runner-side per-test outputs and logs are in ../ci/. A standalone rebuild
writes its own complete outputs to ../standalone/. Contexts are not interchangeable.
