# CM2 Round155 — cold replay record

Date: 2026-07-25

The producer replay under `PYTHONHASHSEED=155` is byte-identical to the sealed
certificate and retains result SHA256
`b182a2223c5d8b9560acdb4eee8031b93b0a79bed84bb24ef8697248d6e8bf13`.

The verifier replay under `PYTHONHASHSEED=551` is byte-identical to the sealed
verification and retains result SHA256
`dd7afee6829d04a37757e94113ccd3dd8bcabc40ba7b7b7e611e85b5fbcb8cdd`.

Final result: producer and verifier cold replays are byte-identical.
