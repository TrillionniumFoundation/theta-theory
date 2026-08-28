# CM2 Round145 finite connected leaf-corridor atlas — cold replay

Date: 2026-07-24

## Frozen producer replay

The formal producer was executed at 8,192-bit precision from the frozen
Round139, Round141 and Round143 inputs:

```bash
env PYTHONHASHSEED=145001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round145_finite_connected_leaf_corridor_atlas.py \
  --precision-bits 8192
```

It returned exit code 0 in `13:58.64` wall time, used `6,748.13` user
seconds and `7.89` system seconds, and reached `57,896 KiB` maximum RSS.
The 13-way atlas replay produced:

```text
producer SHA256:
6deed0506b0105eee9ee9a89dd4c28ee9bed81aa4922586eb8b8005a433ba4c7

certificate SHA256:
5edac93e1425c72992ab671f3b3f7db269d236819ea3ad689b612505426ccec6

certificate result SHA256:
16cec30f7af9d3f0d278d0bae85f8dca4a9a3041186021fc7ebd1b9c43a7fc0b
```

## Materialized cross-precision replay

The frozen producer was separately run at 12,288 bits and a different hash
seed:

```bash
env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round145_finite_connected_leaf_corridor_atlas.py \
  --precision-bits 12288 \
  --output deliverables/cm2-round145-finite-connected-leaf-corridor-atlas-secondary-12288-2026-07-24.json
```

It returned exit code 0 in `25:08.12`, used `11,880.23` user seconds and
`13.71` system seconds, and reached `57,832 KiB` maximum RSS.

The 8,192- and 12,288-bit results are exactly equal after removing only the
explicit generation precision and 13 generation-precision-specific
model-radius ledger hashes.  All topology, faces, frozen paths, radius
exponents/witnesses, worst margins, derivative signs/depths, fixed endpoint
outers, ranks, counts and promoted IDs are byte-exact.  All 13 ledger hashes
change, as expected, and are retained as separate proof evidence rather than
used in the versioned branch identity.

```text
secondary certificate SHA256:
c96dd56c7070e6f35d3302245c2e132bbb061388c54ebc96880f232626af2192

secondary result SHA256:
b62020c00b861e1634ab7a4c77ce280aa48b29117d7fc096c39dfe39d4826108
```

## Independent verifier and same-precision replay

The verifier does not import the producer.  It independently checks the
closed dependency envelope, exact atlas adjacency, corrected Round137-v1
rank arithmetic, source short-cell and image-recut arithmetic, and every
historical null/nonpromotion.  It validates the pinned 12,288-bit artifact
under the exact cross-precision contract, then launches the frozen producer
again at 8,192 bits with `PYTHONHASHSEED=987654321` and requires a
byte-identical primary certificate.

```bash
env PYTHONHASHSEED=145145 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=deliverables /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round145_finite_connected_leaf_corridor_atlas_verifier.py
```

The command returned exit code 0 in `11:44.05`, used `6,810.21` user
seconds and `7.56` system seconds, and reached `57,712 KiB` maximum RSS.
Its internal
same-precision producer replay returned exit code 0, had empty stderr, and
was byte-identical to the frozen primary certificate.

```text
verifier SHA256:
47f283b48bba7c28a94ca01fcaec0389728c1aebd90d31a1f8c36fca0ee4f255

formal verification SHA256:
6101a4bdd7e1bea160a6d1bf36f0b4be281d340f217eb87d38b47f9961fd24a8

verification result SHA256:
c94ebce061403c7c99f09f8db26391e0470fe66217ba922b58aec80061e655b0
```

## Hostile replay

The formal verifier rejected all:

```text
re-signed semantic mutations:       48/48
cross-precision mutations:            7/7
strict-JSON payload attacks:          9/9
verifier output-path attacks:         7/7
```

A separate in-process harness exercised every producer-protected path plus a
symlink, hardlink and missing parent; all `18/18` were rejected.  A second
strict-input harness combined the nine malformed JSON payloads with a
symlink, hardlink, directory and FIFO; all `13/13` were rejected without
blocking.  Canonical source, dependency, certificate and verifier hashes
remained unchanged.

## Replayed mathematical envelope

The replay repeats 21,424 cell/collision stages and 3,449,264 complete
radius-four candidate tests.  It proves:

- 13 cells joined by 12 exact shared faces;
- one fixed 1,648-owner/official-word path throughout;
- 21,411 strict preterminal nonreturn cell/stages;
- a unique terminal `G:S, p=-1/50` face root;
- strict negative terminal `p` and image-observable derivatives on every
  cell;
- a complete connected physical branch for the frozen leaf itinerary.

The corrected Round137-v1 ranks, `k=0` source short cell and image-recut
registry are versioned coordinate-explicit objects.  All historical
Round27/Round35 identifiers remain null.  Gate5 remains `10/18`,
`NOT_CERTIFIED`; CM2 remains `NO-GO_FOR_CLAIM`.
