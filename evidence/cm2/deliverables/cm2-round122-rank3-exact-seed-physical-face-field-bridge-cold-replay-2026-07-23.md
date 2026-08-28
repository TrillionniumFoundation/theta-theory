# CM2 Round122 cold replay

Date: 2026-07-23

## Frozen code and logical digests

```text
producer             44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4
certificate          a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028
certificate result   e8bc4e02635b70dda7cee0485811ae68d42ee595c37a03a5b2aa94ecf170f6cb
verifier             bcf6e34398dcd2fd4cb6bb23aec649db5df75d26a80f307e58521d8ef439d31e
verification         aa0eca5e14fccbeeaad74d075cce0f10ee01f4caf8fccd0e9130ccc0e5cba82b
verification result  c4c3350801310eee7f79e27673391035994bdf348f65e5d46a3da0ff7f4dddb4
```

## Producer replays

Two clean 2048-bit producer runs used fixed locale/timezone and different
hash seeds:

```text
PYTHONHASHSEED=122731 LC_ALL=C TZ=UTC
PYTHONHASHSEED=912207 LC_ALL=C TZ=UTC
```

The canonical certificate and both temporary outputs have exactly the same
SHA256:

```text
a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028
```

Both `cmp` checks pass.  The physical audit, 25 artificial faces, 48 traces,
24 child incidences and 960 new slots are byte-stable.

## Independent verifier replays

Two complete 3072-bit verifier runs used:

```text
PYTHONHASHSEED=122307 LC_ALL=C TZ=UTC
PYTHONHASHSEED=730221 LC_ALL=C TZ=UTC
```

The canonical verification and second temporary output have exactly the same
SHA256:

```text
aa0eca5e14fccbeeaad74d075cce0f10ee01f4caf8fccd0e9130ccc0e5cba82b
```

The `cmp` check passes.  An additional root replay with
`PYTHONHASHSEED=314159`, `LC_ALL=C`, and `TZ=UTC` is also byte-identical.
Every replay reports:

```text
verdict                         PASS
verification precision         3072 bits
upstream/helper pins            59
independent candidate census    57 / 55 / 57 = 169
common actual children          24
physical face instances         0
moving artificial faces         23
stationary outer faces           2
artificial one-sided traces     48
new full-key slots              960
slots per new field             120
combined full-key slots         1680
semantic mutations rejected     120
strict-JSON mutations rejected  15
rank3 seed-child maturity       14/18
global Gate5 maturity           10/18
complete 18-field blocks        0
CM2                             NO-GO_FOR_CLAIM
```

The byte comparison includes the independently recomputed physical census,
implicit-face derivatives, complete attack labels and final status ledger.
