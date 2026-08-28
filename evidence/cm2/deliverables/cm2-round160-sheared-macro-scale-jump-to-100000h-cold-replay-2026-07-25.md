# CM2 Round160 sheared macro scale-jump cold replay

Date: 2026-07-25

## Result

PASS. Producer and independent verifier both reproduced their sealed JSON
documents byte-for-byte under different Python hash seeds.

## Producer replay

- Sealed run: `PYTHONHASHSEED=160`
- Cold run: `PYTHONHASHSEED=1060`
- Sealed and cold certificate file SHA256:
  `f2243caf5d14e5876388f48f468927b5846284c5997879e23d70d1456a6bca5f`
- Certificate result SHA256:
  `984855ea7a08fa5aea8728b7f51f5b5e3ed8a57ca840e7d2448c39adf0d7a4a0`
- Byte comparison: PASS

## Verifier replay

- Sealed run: `PYTHONHASHSEED=601`
- Cold run: `PYTHONHASHSEED=1601`
- Sealed and cold verification file SHA256:
  `7495730c2be0df01470169469c4a91af659b1f926e6fb1748aaec220d072c731`
- Verification result SHA256:
  `a07050a832d7d0971c6e0dce43c14b2a958fdc48116444ef5ca7b1dd4b5f0279`
- Byte comparison: PASS

The verifier did not import or execute the producer. Each verifier run
independently reconstructed the C24, strict-return bridge, and D3 macro boxes,
including all 531,139 radius-four candidate tests.

