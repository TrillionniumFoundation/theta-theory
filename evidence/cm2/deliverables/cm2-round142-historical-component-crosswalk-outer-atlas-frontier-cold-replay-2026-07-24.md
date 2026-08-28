# Round142 cold replay

Date: 2026-07-24

## Frozen artifact hashes

```text
97477687d0013f5a8b426250b930e845858c624685c1f45f6528c336963b7d4c  producer
816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0  certificate
e734b4008ab822710c8b4c5aec5cc1a871f16d7bcea2230ba80eb2f493f0a37e  certificate result
ef2d2297aec42ef39a2b0ca352f05659a2fbb72435283333713f393193dbbad5  verifier
3e7abbe91af042cea229b998fba9c3829fe94120227102f98ecea620005db170  verification
6b5d015ecc67626a6c30ab8d7b837d44aea6c280b42655415ef4fa371895f8eb  verification result
```

## Replay

The producer was run independently with:

```text
PYTHONHASHSEED=1
PYTHONHASHSEED=777
```

Both outputs were byte-identical to each other and to the canonical
certificate:

```text
816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0
```

The verifier was run independently with the same two hash seeds.  Both
outputs were byte-identical to each other and to the canonical verification:

```text
3e7abbe91af042cea229b998fba9c3829fe94120227102f98ecea620005db170
```

Typical local replay times were below three seconds per invocation.  No
producer or verifier output depends on hash-table iteration order.

## Fail-closed process assault

Seventeen hostile process/path cases returned nonzero and created no regular
result output:

```text
missing certificate
tampered certificate
directory as certificate
symlink certificate
FIFO certificate
producer as verifier output
certificate as verifier output
directory as producer output
symlink verifier output
FIFO verifier output
hardlinked verifier output
producer source as producer output
pinned Round139 certificate as producer output
symlink producer output
FIFO producer output
hardlinked producer output
symlinked parent directory
```

The canonical certificate is an intentional legal producer output target;
replaying to it was accepted and reproduced the frozen bytes.

## Verified boundary

```text
two-model enumeration ambiguity: CERTIFIED
historical numeric rank:         NOT IDENTIFIED
historical c24-component ID:     NOT IDENTIFIED
complete 2D outer atlas:         NOT MATERIALIZED
Gate5:                           NOT_CERTIFIED
CM2:                             NO-GO_FOR_CLAIM
```
