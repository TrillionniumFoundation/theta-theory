# CM2 Round149 cold replay

Date: 2026-07-24

All replays used `.venv-neurips/bin/python`, fixed locale/timezone, and
distinct hash seeds.

```text
producer PYTHONHASHSEED=149001   byte-identical PASS
producer PYTHONHASHSEED=149997   byte-identical PASS
verifier PYTHONHASHSEED=149101   byte-identical PASS
verifier PYTHONHASHSEED=149909   byte-identical PASS
semantic mutations              8/8 rejected
strict JSON attacks             4/4 rejected
```

Producer replay SHA256:
`4748f90bee1c8f82a79fa7aeb936d9e13d766ad456cb95bf7f792e41107c53b7`.

Verifier replay SHA256:
`c668db505c6be2c6c06e25d2610a68c68c7a38c0f6dec393b19c826969fd071a`.
