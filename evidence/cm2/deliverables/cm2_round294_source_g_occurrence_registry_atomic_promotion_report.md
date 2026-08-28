# Round294 Source-G occurrence-registry atomic promotion

## Outcome

Round294 passes as an atomic promotion of the current formal Stage-A
open-3D plus Round287-refined occurrence-registry frontier.

The promoted census is exact:

| class | rows |
|---|---:|
| preserved Round266 occurrence IDs | 126,468 |
| formal new Round288 canonical-atom occurrence IDs | 295,336 |
| formal new overlap-refined Round287 occurrence IDs | 9,404 |
| formal registry rows | 431,208 |
| formal new occurrences | 304,740 |
| formal representation bindings | 46,288 |

Binding rows issue no occurrence ID and collapse no pair of distinct occurrence
IDs. Their exact partition is 36,680 Round288 exact-existing bindings, 2,476
Round287 region subcovers, 5,532 Round287 signed-cell subcovers, and 1,600
Round292 refined existing-occurrence subcovers.

## Frozen input contract

The producer byte-pins the sealed Round292 overlap quartet:

| artifact | SHA-256 |
|---|---|
| overlap result | `f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508` |
| overlap ledger | `8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab` |
| overlap verification | `7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd` |
| overlap manifest | `4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870` |

That sealed package proves 1,564 exact positive-volume overlap relations,
1,600 occupied representation-subcover cells, 10,252 uncovered refinement
cells, 9,404 connected strictly new supports, and zero unresolved positive
overlaps. Round294 also consumes the byte-pinned and independently verified
Round266, Round287, Round288, and Round290 packages.

## Why 431,824 and direct issuance of 10,020 are rejected

The old 431,824 census assumed that all 10,020 Round287 source unions could be
issued directly. That is false: 920 source unions have positive-volume overlap
with the preserved registry. Exact refinement yields only 9,404 new connected
supports; 1,600 occupied refinement cells are representation bindings, not new
occurrences.

The independent verifier and attack suite explicitly reject:

* a fully reclosed result with registry count 431,824;
* a fully reclosed result issuing all 10,020 Round287 unions;
* a reclosed direct-union registry row; and
* binding rows forged to issue IDs or collapse identities.

## Independent verification

The cacheless verifier does not import or execute the Round294 producer or the
Round292 candidate builder, and does not use a candidate output as an
expected-row oracle. It directly opens the frozen source ledgers and:

1. verifies every input/output byte pin and selected manifest binding;
2. reconstructs all 126,468 Round266 preserved rows;
3. reconstructs the 295,336 Round288 new-atom rows and their Round279/Round290
   inner-support provenance;
4. reconstructs all 9,404 refined-component IDs and the complete 10,252-cell
   uncovered partition;
5. reconstructs all 46,288 representation bindings;
6. reverses and verifies each complete Round292 candidate-row closure;
7. checks both Round294 ledger envelopes, row content IDs, row hashes, table
   commitments, occurrence-ID injectivity, and exact credit sums; and
8. exhausts the output source-identity sets with independently derived source
   sets.

The final verifier status is:

```text
PASS_INDEPENDENT_CACHELESS_ROUND294_STAGE_A_REGISTRY__431208_ROWS__
126468_PRESERVED__304740_FORMAL_NEW__46288_REPRESENTATION_BINDINGS__
POST_REGISTRY_DSU_NOT_REBUILT
```

## Strict document, gzip, path, and file-object boundary

The verifier enforces duplicate-free, finite, integral, single-document JSON;
canonical JSON bytes for the result; single-member, no-trailing GZIP; a
2,000,000,000-byte uncompressed GZIP cap; and a 1,100,000,000-byte file cap.
Every consumed artifact must be a HERE-only regular, non-symlink,
single-hardlink file.

All 41 attacks are rejected:

* 11 fully reclosed semantic attacks;
* duplicate-key, NaN, Infinity, float, oversized-integer, and trailing-document
  JSON attacks;
* multi-member, trailing-byte, and uncompressed-size-cap GZIP attacks; and
* symlink, hardlink, FIFO, directory, missing, path-escape, and oversize
  substitutions against each actual result, registry-ledger, and
  binding-ledger path.

## Scope and nonpromotion boundary

The 431,208 registry rows are not claimed to be a final exhaustive all-stratum
registry. The final registry count is undetermined. The known Round291
576-entry lower-stratum gap frontier and Round289 396-entry
incidence-refinement frontier may require append-only occurrence extensions;
they may not rewrite this closed Stage-A identity frontier.

Only occurrence identity and representation-binding credits move in Round294:

| credit/state | Round294 value |
|---|---:|
| formal new expanded occurrence credit | 304,740 |
| formal occurrence alias/binding credit | 46,288 |
| component-union credit | 0 |
| DSU rank-reduction credit | 0 |
| seam-edge credit | 0 |
| Jx/Jy same-point glue credit | 0 |
| maximality credit | 0 |
| fibre credit | 0 |
| global-disposition credit | 0 |

The number 63,224 is only the legacy pre-Round294 preserved-registry quotient
baseline. It is explicitly rejected as a current quotient count. The
post-Round294 expanded-registry component/DSU has not been rebuilt; its
quotient-component count is null, and maximality, fibres, and dispositions all
wait on that rebuild. Gate5 remains 10/18, D02 remains blocked, and CM2 remains
no-go for claim.

## Replay

Two producer seeds and two verifier `PYTHONHASHSEED` values reproduce identical
registry, binding, result, verification, and attack-suite commitments. See the
separate cold-replay record for commands, hashes, and observed runtimes.
