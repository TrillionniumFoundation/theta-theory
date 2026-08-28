# CM2 Round159 — cold replay record

Date: 2026-07-25

The producer replay under `PYTHONHASHSEED=9159` is byte-identical to the
certificate produced under `PYTHONHASHSEED=159`. Both retain result SHA256
`841c237bd774d48513061a380865dd423151129c8db651baf45f4c91f3f8b6f6`
and file SHA256
`9af879463f5e300f07d3ec88642757c86a8cca214986eb8f1f908a511f39f142`.

The verifier replay under `PYTHONHASHSEED=9150` is byte-identical to the
verification produced under `PYTHONHASHSEED=951`. Both retain result SHA256
`64ac7427197b37d3da1aa3228acbf2036bdf499025e4a2fde2056b32f865805f`
and file SHA256
`d3a787d242e2cb485955553b52e1a95c9044b8075291b981f933973bfbfac059`.

Final result: producer and verifier cold replays are byte-identical.
