# CM2 round306c55c no-producer global strict decider report

Date: 2026-08-12 (CST)

## Verdict

The independent no-producer boundary is implemented and the exact C55-A/C55-B
inputs have been cold-replayed.  The only lawful real-input result is:

```text
FAIL_CLOSED_GLOBAL_STRICT_DECIDER_NOT_ENABLED
positive_terminal_enabled  false
terminal_class             null
formal_credit              0
D02_credit                 0
CM2                        NO-GO_FOR_CLAIM
```

The real row census independently reconstructs to 75,388
`EARLIEST_PREFIX_EXCLUDED` + 296 `TYPED_EVENT_GRAPH` + 0
`CONNECTED_TO_KNOWN` + 0 `SOURCE_GRAZING_OR_CEMETERY` + 1,148
`UNRESOLVED_R1648_CONTINUATION` = 76,832.  C55-C does not replace those
1,148 rows with labels, and it does not trust the A/B eligibility booleans.

## Independence and exact bindings

The verifier imports and executes neither the C55-A nor C55-B producer.  It
consumes their files as inert data through held `O_NOFOLLOW` descriptors,
requires regular single-link owner-controlled files, and rechecks file and
parent-directory identities after the complete bundle read.

The exact installed C53 global head is bound by file/object
`f62483c8...eeb3 / cb90ab91...cbfb`, and the effective checkpoint is
`b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab`.
The frozen C55p0 contract file is `0e2a7b71...2333b`.

The exact A inputs are:

```text
leaf ledger file/object  e80c012e...d8db6 / 7dd4c19c...59d90
glue ledger file/object  d91dbc92...ae00b / b9a9a3fd...45cef
```

The exact B inputs are:

```text
result file/object       6bf9cae7...32a93 / 1ce396e9...7cc56
cell ledger file         123a742e...a2ce       (1,724 rows)
edge/glue ledger file    23ea0b44...29a0       (5,358 rows)
component ledger file    bebc49f6...8a04       (26 rows)
```

## Independent reconstruction performed

C55-C verifies all 76,832 A leaf row self-hashes and the terminal-null iff
explicit-unresolved rule.  It recomputes the four-class census, verifies every
leaf glue ordinal against 161,586 intra faces, 888 source seams, 1,024 source
grazing faces, and 8 grazing corners, and checks the frozen exact input hashes.

On the B side it validates one-member gzip integrity, canonical duplicate-free
JSONL, every row self-hash and row-sequence commitment.  It reconstructs the
1,724-cell reflection pairing, all 5,358 edge/component incidences, the exact
26-component partition and graph connectivity, member/edge hashes, the
576/1,148 ordinary-cell census, two reflected strict-subset anchor cells, and
the 1,124 + 24 unresolved partition.  The A/B crosswalk covers all 1,724
ordinary cells with exact physical boxes and component bindings; their full
censuses agree.

The remaining exact blockers are:

- A has 574 nonempty blocker rows and 1,148 unresolved leaves.
- B proves neither global closure nor unresolved-zero and correctly marks the
  strict decider ineligible.
- The frozen B data has no inert 76,832-row second projection ledger, so a
  second full per-row reconstruction cannot be inferred from a summary
  boolean.
- The two anchored components cover 1,124 unresolved cells but have only
  strict-subset collars, not whole-component common refinements; 24 singleton
  components still lack complete event/exterior closure.

## Hostile tests

The self-test is 31/31 PASS.  It includes an exact-76,832 synthetic eligible
gate exercise (explicitly non-authoritative), 18 coherently re-signed semantic
attacks, duplicate-key/BOM/NaN/noncanonical JSON, closed-object mutation,
symlink, hardlink, same-name file swap, and parent-directory TOCTOU attacks.
Every attack fails closed.  The synthetic path grants no terminal, formal, or
D02 credit and is never consumed as real evidence.

## Cryptographic bindings

```text
verifier source file  b66ab9ca935925806acd35fb736ee20b79d905c855973eec4059df7cacc3c135
contract file/object  9b6497bc7e91e002f0d89a4a3575211aa7b11c541ef1fd3e585b8787d0311092
                      6a8f7773a69b43fc084c2a0213ddb0c601a56e3a6a63689ce8444ce3e25556fc
self-test file/object  8c0430fa2ac012ffe528f6cab6ccec1de16ff4148e66d12196803d193e7c4aff
                      82282add3a77c3d515852843f9ae68491612c97fc811fafc9b98b343bf60da63
verification file/obj  9c6c8377d8e8183bc602475dbe1efc05a8a9d51aeece5abca5f15a939bc65be0
                      4cf91683fbd857343335969b8ef10f9044a78be8620cc5c5b062e7a4e7de3ca3
```

No C55-C command writes runtime state, canonical status, a pointer, claim,
receipt, authority, or seal.
