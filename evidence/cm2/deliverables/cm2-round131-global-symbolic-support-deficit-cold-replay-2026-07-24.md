# CM2 Round131 cold replay

Date: 2026-07-24

```text
producer PYTHONHASHSEED=0           byte-identical PASS
producer PYTHONHASHSEED=987654321   byte-identical PASS
verifier PYTHONHASHSEED=0           byte-identical PASS
verifier PYTHONHASHSEED=987654321   byte-identical PASS
re-signed semantic mutations        4/4 rejected
strict JSON/encoding attacks        3/3 rejected
```

The verifier independently reconstructs 18 touched symbolic words and the
441,262-word complement without importing or executing the producer.
