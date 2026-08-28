# CM2 Round154 — cold replay record

Date: 2026-07-25

The producer replay under `PYTHONHASHSEED=154` is byte-identical to the sealed
certificate and retains result SHA256
`361532f74e966f26a460f3c90db59456f5d25b62947254fce3abcd3c0575289d`.

The verifier replay under `PYTHONHASHSEED=451` is byte-identical to the sealed
verification and retains result SHA256
`cd34e677323ffb659e34fd44b7b6569aec2ee394cd6e51eb2920ff9a92ca8af0`.

Final result: producer and verifier cold replays are byte-identical.
