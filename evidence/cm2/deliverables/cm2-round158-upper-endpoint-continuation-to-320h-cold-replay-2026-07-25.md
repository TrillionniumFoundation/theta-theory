# CM2 Round158 — cold replay record

Date: 2026-07-25

The producer replay under `PYTHONHASHSEED=8158` is byte-identical to the
certificate produced under `PYTHONHASHSEED=158`. Both retain result SHA256
`79c330cc92be3d00c7500f5e76a52fbf9180647a52ea508de1537e2410caa5b3`
and file SHA256
`9b7196d43f608a1a83f9eb98116fa8a3f7b4c41e3bc89fee2724f51dcecf53c6`.

The verifier replay under `PYTHONHASHSEED=8150` is byte-identical to the
verification produced under `PYTHONHASHSEED=851`. Both retain result SHA256
`50273f316effa92b3fd309ec0868872456e98a41de9f78b8c9bfb950e4c19e37`
and file SHA256
`5c814d68f68732a527fd769db773a955f3281fc733d88fd585ffac249f03fd9b`.

Final result: producer and verifier cold replays are byte-identical.
