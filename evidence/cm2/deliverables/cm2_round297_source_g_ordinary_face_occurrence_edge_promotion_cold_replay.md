# Round297 cold replay

Run from the `deliverables` parent directory with the seven upstream manifests
and all 62 byte-pinned members present.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=297001 \
  python3 -B deliverables/cm2_round297_source_g_ordinary_face_occurrence_edge_promotion.py \
  --seed 297001
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=297997 \
  python3 -B deliverables/cm2_round297_source_g_ordinary_face_occurrence_edge_promotion.py \
  --seed 297997
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=297101 \
  python3 -B deliverables/cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_verifier.py \
  --seed 297101 --output /tmp/cm2_round297_verification_seed1.json
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=297929 \
  python3 -B deliverables/cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_verifier.py \
  --seed 297929 --output /tmp/cm2_round297_verification_seed2.json
cmp /tmp/cm2_round297_verification_seed1.json \
  /tmp/cm2_round297_verification_seed2.json
```

Both producer invocations must report:

- 330,724 formal ordinary component-edge witnesses;
- zero current quotient;
- edge-ledger file SHA-256
  `18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371`;
- result self-digest
  `4cc22f9bb0130475908e71d2102182ed8a6a182efffeedfb5e5367acce57a2d8`;
- result file SHA-256
  `e95f7139548f6f2fe9d96c52d50ebd116fff938b990c7b31b2f76c0d17bc8d56`.

Both verifier invocations must report:

- independent cacheless reconstruction of all 330,724 edge rows before
  candidate read;
- 62 of 62 attacks rejected;
- verification self-digest
  `04831605599719882f14ffa240a1439f6056c9525a6aa245b3fa09e97106ebbb`;
- verification file SHA-256
  `74ef0c5cb3fe52cce8295fffc1a8b1af0c2f9e38e7bf02cbd5db923b6d6dcdb5`.

The two verification files must be byte-identical.  No producer or verifier
invocation may promote an occurrence identity collapse, component-union or
DSU-rank credit, or a current quotient-component count.
