# CM2 Round157 — cold replay record

Date: 2026-07-25

The producer replay under `PYTHONHASHSEED=7157` is byte-identical to the
certificate produced under `PYTHONHASHSEED=157`. Both retain result SHA256
`b710d5f24642219a6d66db8de8ae7b63461616bddbb1518cbe4c80f1699ee913`
and file SHA256
`3c25d0f3fc813c8e26760c54cee858a463dcafa65721129c3a58d5463af28351`.

The verifier replay under `PYTHONHASHSEED=7150` is byte-identical to the
verification produced under `PYTHONHASHSEED=751`. Both retain result SHA256
`ea620007fd4d919b05be3f211d08a69a2e8b4438c299665283784d18d9147d56`
and file SHA256
`724e35ea187096be6dee38639e1259a90c14924c7ebc9524bfdfbc6bf4150851`.

Final result: producer and verifier cold replays are byte-identical.
