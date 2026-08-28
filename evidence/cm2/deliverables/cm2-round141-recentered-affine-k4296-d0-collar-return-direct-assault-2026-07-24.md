# Round141 K4296 direct assault

Status: **PASS**

The frozen Round141 producer, centered engine, certificate, and independent
verifier were attacked without changing any Round139 or Round140 artifact.

## In-verifier attacks

- Semantic mutations: **20/20 rejected**
  - status/width/factor
  - model row count, model digest, and maximum-radius bound
  - owner, official-word, and compact-path digests
  - candidate count and collision-three anchor count
  - homogeneity and incidence histograms
  - terminal owner and terminal `p` enclosure
  - false historical component, Round35 restriction, image-recut, Gate5, and
    CM2 promotions
- Strict JSON attacks: **9/9 rejected**
  - duplicate keys
  - `NaN`, positive infinity, and negative infinity
  - top-level array and string
  - trailing JSON data
  - symlink and hardlink inputs
- Output-path safety attacks: **9/9 rejected**
  - producer, certificate, engine, and verifier aliases
  - directory output
  - missing parent
  - symlink parent/output
  - hardlink output

Each semantic mutation was checked with closure checking disabled for that
attack only, so rejection came from the affected semantic invariant rather
than trivially from the frozen result hash.

## Separate process/I/O attacks

Twenty-one separate subprocess probes all exited nonzero as required:

- **17/17** direct atomic-write probes rejected protected source/certificate/
  engine/verifier/Round139 aliases, directories, missing parents, output
  symlinks, and output hardlinks.
- **4/4** CLI probes rejected precision below 8192, malformed precision,
  unknown producer arguments, and a non-frozen verifier certificate path.

The hardlink fixture was removed immediately after the test and the frozen
certificate's link count was confirmed to be one.

## Mathematical scope held fixed

The assault does not enlarge the theorem.  Round141 certifies one exact
fixed-leaf local collar of intrinsic width `2^-4296`; it does not certify a
historical maximal component ID, a Round35 restriction, a natural short-cell
rank, or an image-recut rank.  Gate5 remains `10/18` and CM2 remains
`NO-GO_FOR_CLAIM`.
