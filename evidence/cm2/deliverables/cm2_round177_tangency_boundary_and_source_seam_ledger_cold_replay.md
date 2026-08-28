# Round177 cold replay

Date: 2026-07-26

The producer and independent verifier were run in separate clean Python
processes with bytecode disabled.

```text
PYTHONHASHSEED=1
certificate result  9352f036325bc6e884fc6d31da2e1e2a04532d45fb11de90b3e5051103f56a9f
verification result 6968d5b50037457e546c06fbe2f7f620fbbfbb73f354f78b7035afb23426934e

PYTHONHASHSEED=987654321
certificate result  9352f036325bc6e884fc6d31da2e1e2a04532d45fb11de90b3e5051103f56a9f
verification result 6968d5b50037457e546c06fbe2f7f620fbbfbb73f354f78b7035afb23426934e
```

`cmp -s` passed for both the certificate and verification files.

```text
certificate file SHA256
8e0a7d3d093026932d847657d737f7f1dfc5aaea3727ff4d3e202728aa64c7cc

verification file SHA256
2b56c96af9d6d284ee39d71636bf43425431183da8ae19df63eaa6b90a6df4b3
```
