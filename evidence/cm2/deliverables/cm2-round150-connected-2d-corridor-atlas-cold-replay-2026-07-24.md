# CM2 Round150 cold replay

Date: 2026-07-24

## Producer

The producer was rerun from cold processes under
`PYTHONHASHSEED=150001` and `PYTHONHASHSEED=150997`.

Both outputs were byte-identical to the formal certificate:

```text
6bb182760205190ad635ef34c21eca6221d2224e2dcdb585f70c157fad76321c
```

Both result payloads had SHA256:

```text
2228116225baa95c31a7b8b0f13d222b623f5973b0f8c8e12366f9b4464681e6
```

## Verifier

The independent verifier was rerun from cold processes under
`PYTHONHASHSEED=150101` and `PYTHONHASHSEED=150909`.

Both outputs were byte-identical to the formal verification:

```text
686e236dbe998c111a0307e3edfd34d0b26185b6f52ec54fa33e340725655ee5
```

Both verification result payloads had SHA256:

```text
2d67c62756c8b4811f7537e1ede92c8b77861caee58178ead7105958e2920d1f
```

## Verdict

```text
producer cold replay      BYTE_IDENTICAL
verifier cold replay      BYTE_IDENTICAL
formal verification      PASS
```
