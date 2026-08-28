# Round277 true-support candidate-universe audit (zero credit)

## Scope

This audit independently rebuilds the Round276/277 same-signature
positive-common-face candidate universe after replacing each canonical
`(Round182 leaf, complete signature)` node's whole-leaf box by the union of its
frozen rectangular supports.

The only source rows with a support box stricter than the Round182 leaf are the
twelve Round271 `OUTGOING-W` rows carrying `t_child_box`.  Side orientation is
derived geometrically:

- the endpoint whose support box has its **upper** face at the shared
  coordinate is the negative-side endpoint;
- the endpoint whose support box has its **lower** face there is the
  positive-side endpoint.

Lexical tuple order is never used to infer side orientation.

## Exact result

- Frozen source rows: **332,020**
- Canonical atoms after explicit alias grouping: **332,016**
- Explicit Round271 artificial split alias contractions: **4**
- Atoms whose normalized support union is the full Round182 leaf:
  **332,012**
- Atoms with a strictly smaller frozen rectangular support: **4**

The candidate universe is byte-for-byte unchanged:

- old Round276 candidate edges: **330,724**
- true-support candidate edges: **330,724**
- unchanged records: **330,724**
- changed-overlap records: **0**
- removed endpoint edges: **0**
- added endpoint edges: **0**
- old records removed: **0**
- new records added: **0**
- old edges incident to one of the four smaller-support atoms: **4**
- new edges incident to one of the four smaller-support atoms: **4**

Both unordered universes have SHA256
`8e6a26f93f954a89b37db293bd46c16ca087762e19758fafb6b0fc95864aebbb`.

Each of the four smaller-support atoms has old degree **1** and new degree
**1**.  The independently oriented old and true-support universes are also
byte-for-byte equal and have SHA256
`b49164162644e16d4de141908831fca6b340cba5f8f24fdebcbe9e7cc34a7ee9`.

Empty change sets all have canonical-empty-list SHA256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

## Alias treatment

For each of the four duplicated negative-signature W-tail atoms, its two
`t_child_box` values:

1. have identical tangential spans,
2. meet exactly on the artificial middle `t` face, and
3. merge without enlargement to the complete Round182 parent leaf.

The four middle faces therefore remain explicit alias witnesses.  They are not
frontier adjacency edges and are not counted among the 330,724 candidates.

The four other W-tail signature atoms occupy only one child box.  Respecting
those smaller supports changes no candidate record: it removes no endpoint,
adds no endpoint, and changes no overlap rectangle in the frozen
same-signature common-face universe.

## Interpretation

This validates the Round276 candidate count and digest against the frozen
rectangular atom supports.  It does **not** turn candidate faces into physical
component edges.  Each retained candidate still needs a positive-area exact
`MATCH` patch and strict inward corridors on both geometrically oriented sides.

No expanded-occurrence, component-edge, maximality, fibre, disposition, or
CM2 credit is issued by this audit.
