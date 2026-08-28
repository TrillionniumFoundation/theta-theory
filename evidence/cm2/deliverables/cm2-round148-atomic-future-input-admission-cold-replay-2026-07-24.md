# CM2 Round148 cold replay

Date: 2026-07-24

```text
producer PYTHONHASHSEED=0    byte-identical PASS
producer PYTHONHASHSEED=91   byte-identical PASS
verifier PYTHONHASHSEED=0    byte-identical PASS
verifier PYTHONHASHSEED=91   byte-identical PASS
semantic mutations           8/8 rejected
strict JSON attacks          4/4 rejected
```

The verifier reconstructs both atomic future-input slots and the complete
14-node superseding DAG without importing or executing the producer.
