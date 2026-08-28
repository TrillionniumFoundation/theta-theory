# CM2 Round144 direct assault

Date: 2026-07-24

## Target

The target is the append-only Round137-v1 superseding migration schema.  The
assault tests whether a mutation can:

- alias the prospective namespace to a historical identifier;
- mark a blocked DAG node ready;
- upgrade a positive basis upper bound to a least rank;
- mint any component, restriction, owner, token, or output;
- select an owner from the incomplete 64-row observed subset;
- promote Gate5 or CM2;
- bypass strict JSON or filesystem protections.

## Semantic mutations

The independent verifier rejected 34/34 mutations, including:

- enumeration ID and index-origin substitutions;
- historical reinterpretation and fail-open changes;
- namespace prefix, payload-field, prerequisite, and null-policy changes;
- DAG readiness, edge, and node-order changes;
- forged component, restriction, owner, t54, and q_j IDs;
- first-blocker and owner-contract changes;
- source core, return depth, path hash, and upper-bound promotions;
- future-certificate overpromotion;
- historical/versioned count, Gate5, CM2, and registry-ID changes.

## Strict JSON attacks

The verifier rejected 8/8 attacks:

- duplicate root key;
- `NaN`, `Infinity`, and `-Infinity`;
- array and scalar roots;
- trailing JSON;
- truncated JSON.

## In-process path attacks

The verifier rejected 12/12 attacks:

- certificate symlink, hardlink, and directory;
- output symlink, hardlink, directory, missing parent, and symlink parent;
- output aliasing the producer, verifier, certificate, or a pinned dependency.

## Hostile process/I/O attacks

Seventeen independent process cases all exited 1:

1. verifier certificate symlink;
2. verifier certificate hardlink;
3. verifier certificate directory;
4. verifier mutated certificate;
5. verifier output symlink;
6. verifier output hardlink;
7. verifier output directory;
8. verifier output in a missing parent;
9. verifier output through a symlink parent;
10. verifier output aliasing the certificate;
11. verifier output aliasing the producer;
12. verifier output aliasing a pinned Round142 dependency;
13. producer output symlink;
14. producer output hardlink;
15. producer output directory;
16. producer output in a missing parent;
17. producer output aliasing a pinned Round142 dependency.

No unexpected output file was created.  The symlink/hardlink target remained
byte-identical.  Producer, verifier, certificate, and Round142 dependency
hashes remained unchanged.  The temporary certificate hardlink was removed
after its rejection and the frozen certificate returned to link count one.

## Verdict

`PASS`

The assault found no route to reinterpret historical bytes, bypass a direct
prerequisite, mint a blocked identifier, corrupt a protected input, or promote
Gate5/CM2.  The exact frontier remains D02, followed by the D03 least-rank
negative oracle.

