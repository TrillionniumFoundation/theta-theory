# C71b v3 verification status-count rejection and supersession

The first no-producer verification output is rejected and superseded.  Its
structured `coherent_attacks` object truthfully records 28 attempted and 28
rejected hash-reclosed attacks, but its human-readable status token incorrectly
said `32_COHERENT_ATTACKS`.

- rejected file SHA-256: `9c6733e7aabc900e77e8ca0358c4658b9acc7e48873e902b70651ce6360875e9`
- rejected object SHA-256: `89de4868bde9eef79f79ff25ecbb6a73a8cb4a1973b22b4398a16c174ec3e2ca`
- rejected verifier source SHA-256: `df50057b663919ad411a0262aaced4ed8612f0c53013b65d6893ea0f42bebaa8`
- credit granted: zero

The rejected output must never be consumed as a verification authority.  A
fresh no-replace output from the corrected verifier, with an exact
`28_COHERENT_ATTACKS` status token, is the only eligible successor.
