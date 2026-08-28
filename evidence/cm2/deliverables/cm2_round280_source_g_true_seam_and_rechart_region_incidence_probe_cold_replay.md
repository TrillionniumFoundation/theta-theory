# Round280 true-seam/rechart incidence probe — cold replay

The zero-credit producer was run twice from the pinned frozen inputs with
external replay labels `280071` and `280929`.  The label is intentionally not
consumed by the deterministic producer.

Both runs produced byte-identical stdout, result JSON, region attachment, and
patch attachment.

- producer SHA256:
  `6aae0b7b1cf8d4c59bcbba58fb9072006eff5f62ad45676674278bf6d6ecaca7`
- result JSON SHA256:
  `3a71b06526d089ff470bce71953eb2f89b02d373ff224fe549120b18942a87d6`
- result object SHA256:
  `a86842c7ee7fd71727c7d49e869d042adbb0273e94356e588484122c3363a76d`
- 13,788-row region attachment SHA256:
  `8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b`
- 152-row patch attachment SHA256:
  `074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814`

This replay freezes a probe result only.  It does not substitute for the
missing seam-normal corridor certificate and awards no occurrence or DSU
credit.

