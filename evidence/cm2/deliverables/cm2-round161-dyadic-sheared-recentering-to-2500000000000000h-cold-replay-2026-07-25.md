# CM2 Round161 dyadic sheared recentering cold replay

Date: 2026-07-25

## Result

PASS.  Producer and independent verifier both reproduced their sealed JSON
documents byte-for-byte under different Python hash seeds.

## Producer replay

- Sealed run: `PYTHONHASHSEED=161`
- Cold run: `PYTHONHASHSEED=1161`
- Sealed and cold certificate file SHA256:
  `317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd`
- Certificate result SHA256:
  `842ef791a414e85b5f2eeb458f876d837d269a284f26ae8317059bd4e0fb2f12`
- Byte comparison: PASS

## Verifier replay

- Sealed run: `PYTHONHASHSEED=611`
- Cold run: `PYTHONHASHSEED=1611`
- Sealed and cold verification file SHA256:
  `01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db`
- Verification result SHA256:
  `5c1a78555644f4fb424e8e164e3088fd24a1d393252a6214d4b8829815571e07`
- Byte comparison: PASS

Each verifier run independently reconstructed the C24, strict-return bridge
and D3 boxes, including the collision-three correlated anchor proof, all
531,139 radius-four candidate tests, the exact slope-change seam and the
75/225/0 combined atlas.
