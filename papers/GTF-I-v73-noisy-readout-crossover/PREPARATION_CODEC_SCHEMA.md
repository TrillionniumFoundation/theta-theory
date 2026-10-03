# Exact preparation codec — v68

## Mathematical input

Use the inherited `Instrument` JSON format: positive integer input/output dimensions d,n, a positive integer denominator, and m Gaussian-integer Hermitian matrices of order dn. The convention is `input-first-unnormalized`. The validator requires PSD and the exact joint output partial trace. This codec further requires each block to be `I_d tensor sigma_y`. It rejects a general non-preparation channel even when that channel is CP and TP.

The rank bounds are a public list of m integers in [0,n], not all zero. If omitted they all equal n. The exact validator checks the actual block ranks do not exceed the bounds. Singular pivots and zero outcomes are accepted.

## Encoded core

Schema `gtf68.preparation-code/1` records public d,n,m, rank bounds and grid B, a pivot-set header, actual real-factor coordinate count h, family dimension v, and `body_hex`. Pivot positions are zero-based and strictly increasing within each outcome. There are at most mn header bits. Given this header the body index is

    (2*anchor + negative_sign_bit)*(2B+1)^(h-1)
        + mixed_radix_index(nonanchor_digits),

where every digit is in [-B,B] and the anchor is exactly +/-B. The hexadecimal string is canonical lowercase with no leading zeros, except `0`. Its mathematical fixed-length binary alphabet is padded to the worst-case bound

    mn + ceil(log2(2(v+1)(2B+1)^v)).

Dimensions, public rank bounds, B and requested horizon/error are common parameters and not target-specific payload. The singleton family has a unique predetermined code and zero payload. JSON keys, decimal headers and certificate prose are interchange overhead, not compressed-bit claims.

## Exact construction

At a positive rational Schur pivot u, the diagonal factor coordinate has square u. A lower real/imaginary coordinate has square component^2/u, and its sign is known. Comparing these rational squares selects a largest coordinate. A ratio with squared value b_i/b_anchor yields the exact integer digit magnitude

    isqrt(floor(B^2 b_i/b_anchor)).

No irrational square root is stored. Decoding forms the triangular Gaussian-integer matrices Z_y, computes T=sum ||Z_y||_F^2, and returns blocks Z_y Z_y*/T, with I_d tensored in to produce Choi data. B^2<=T<=h B^2. The result is CP and TP by construction. Empty pivot sets remain zero outcomes; ranks can decrease under rounding but cannot increase.

## Adaptive certificate

Schema `gtf68.adaptive-preparation-code/1` wraps a core code, positive integer N, canonical rational unhalved tolerance delta in (0,2), and the squared error bound. The implementation chooses

    B >= 4 ceil(sqrt(N*v))/delta

using exact integer arithmetic. Its computed certificate is

    N * 16(h-1)/B^2 <= delta^2.

This bounds all common quantum testers with at most N uses of the same memoryless preparation instrument, including references and public stopping. Transcript TV is half an unhalved classical block norm. No all-rare-posterior guarantee is added.

`decode` proves codeword legality and checks internally recomputable metadata; it cannot certify proximity to an unspecified target. `verify` re-runs the exact deterministic encoder against the provided target and compares the full certificate. Changing the target, payload, parameters or bound invalidates target-bound verification. A mathematical total decoder may map malformed codewords to a fixed legal instrument; the executable CLI rejects them with exit code 2.

## Resources and boundaries

The codec is deterministic and makes no random-bit claim. Rational input PSD/Schur preprocessing and integer arithmetic have polynomial bit complexity in explicit data and output length. Full decoded matrices and preprocessing workspace are not bounded by the optimal payload. The returned object is a mathematical quantum instrument, not a finite-classical-message physical simulator of unknown entangled input. Rank bounds and the input-erasure promise are essential to the stated boundary family.
