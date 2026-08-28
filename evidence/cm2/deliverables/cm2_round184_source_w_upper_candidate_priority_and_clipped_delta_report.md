# CM2 Round184 — source-W upper-candidate priority and clipped-Delta tranche

Date: 2026-07-26

## Verdict

`PASS_PARTIAL_BOUNDED_ROUND184`.

Round184 first publishes a deterministic registry of all 1,444 source-W
whole-exclusion upper candidates left open by Round180.  It then processes
the outcome-blind first class, the 794 origins whose entire Round180 residual
support consists of a single clipped or face-overwrapped discriminant graph.
Exactly 620 complete original physical parents receive new integer exclusion
credit.

The conservative source-W ledger is therefore

```text
74,012 excluded + 2,820 live = 76,832 refined source-W records.
```

This is a bounded ledger improvement, not a core-gate closure.  D02 remains
`BLOCKED`, D03's negative oracle remains `UNAUTHORIZED`, Gate5 remains
`10/18`, the complete global 18-field-block count remains zero, and CM2
remains `NO-GO_FOR_CLAIM`.

## Complete deterministic priority registry

Every still-open Round180 upper candidate enters the registry before any
Round184 proof outcome is inspected.  The ordering key is:

1. residual-support class rank;
2. Round180 residual-child count ascending; and
3. exact origin key ascending.

The complete partition is:

| Priority class | Origins |
|---|---:|
| pure single clipped Delta | 794 |
| pure root equality | 0 |
| Delta-H or multi, without compact-q | 596 |
| compact-q present | 54 |
| **Total** | **1,444** |

The exact registry-order digest is
`9ed48108c64c1bad5a6ec37490517adeb539c2a7cdf7e0c10334213ab7931611`.
The 1,444 registry-row digest is
`d6d247658c26c685a6df4f385902122e212dfdf5ed74ca6058ca14510591712e`.
The exact 794-key selected-prefix digest is
`fcfe248134dd13811e6d8aa58e9fb1506c7a29dc45b11a08364a750d5748d4ef`.

Four origins have no preclosed Round176 kind.  They remain in the complete
partition rather than being silently discarded; their exact-key digest is
`a5931d795fc156acf42c5582c6128f630dd8d20c650891a1fd41d4d30abc4ad4`.

## Pure clipped-Delta proof tranche

The 794 selected origins contain 83,274 Round180 residual children.  For
every child, the verifier independently reconstructs the unresolved target,
strict p-derivative sign, Delta-negative removal disposition, positive-first
test, owner, and outgoing-chart exclusion.

The proof partition is dimension safe:

| Stratum | Ambient/outer dimension | Required evidence |
|---|---:|---|
| `Delta<0` open side | 3 | target removed and remaining cell excluded |
| `Delta=0` graph | 2 | owner or independently recomputed chart mismatch |
| `Delta>0` open side | 3 | unique-first owner or outgoing-chart mismatch |
| graph/box-face outer | 1 | inherited excluded graph proof |
| graph/edge or corner outer | 0 | inherited excluded graph proof |

Graph, face, edge, and corner counts are conservative outers; nonemptiness is
not inferred from an outer count.  Split faces use a half-open owner, and
duplicate 1D and 0D split strata are deduplicated.  An origin receives integer
credit only when every residual child and every inherited 3D/2D/1D/0D
stratum is closed.

The tranche reconstructs 66,782 successful child proofs.  Exactly 620
origins are wholly closed; their exact-key digest is
`9105617c4f5d60e2bb9f2e602472cb489bad5af23edcdfb9a2e11de9efd0a8ae`.
The 794 per-origin row digest is
`76519d1d5e3c892a2b7a2d0fb3686d1633a0c01f0d4f4ea18f15d87e178cda7d`.

The remaining 174 origins have exact-key digest
`043be51484742a3370632eb28e425423959da57e090656dc8c490698fb923338`.
Their failure decomposition is:

| Failure | Child occurrences | Origins |
|---|---:|---:|
| target not uniformly strict-positive-first | 16,492 | 162 |
| source physical seam requires a separate half-open partition | origin-level | 18 |

Six origins occur in both sets, so `162 + 18 - 6 = 174`.  The number 16,492
is a child-failure count, not an origin count.

Of the 794 source parents, 776 are strict physical-chart interiors and 18 are
source-seam/guard composites.  All 620 credits come from strict interiors.
The seam parents, rational guard, child counts, child volume, and analytic
internal strata contribute zero integer credit.

## Independent verification

The independent verifier pins the Round184 producer as inert bytes and never
imports or executes it.  It uses the pinned, independently verified Round180
verifier as its geometry library, but reimplements all Round184-specific
priority, clipped-Delta, source-domain, and ledger logic.

It reconstructs:

- all 1,444 registry rows and their exact deterministic order;
- all 794 tranche rows and the complete child-proof digests;
- the exact 620 closed and 174 failed key sets;
- the 162/18/6 failure-set decomposition;
- every credited and noncredited 3D/2D/1D/0D ledger;
- the producer output-safety contract; and
- the complete expected certificate, byte for byte.

The certificate file SHA256 is
`292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f`;
its result SHA256 is
`70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe`.

The independent verifier rejects:

| Attack suite | Rejected |
|---|---:|
| re-signed semantic mutations | 37/37 |
| strict JSON, encoding, type, and canonical-form attacks | 16/16 |
| input path/type and output-authorization attacks | 15/15 |

The official seed-184061 verification completed in 18 minutes 2.85 seconds
with maximum RSS 742,164 KB.  Its result SHA256 is
`126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9`;
the verification-file SHA256 is
`7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6`.

A separate parent replay under seed 184051 completed in 16 minutes 11.99
seconds with maximum RSS 743,880 KB and was byte-identical to the official
verification.

## Output safety

The producer writes only the official certificate or an authorized hidden
Round184 certificate replay in the deliverables directory.  It uses a
same-directory temporary regular file, flushes and fsyncs that file, and
atomically replaces the requested certificate.

The verifier admits only the official verification or a hidden
`.cm2_round184_*_verification.json` replay in the same physical directory.
It rejects symlink, hardlink, directory, FIFO, nested, escaped, protected, and
unauthorized outputs.  Its successful write fsyncs both the temporary file
and the parent directory around the atomic replacement.

## Remaining core work

Exactly 824 upper candidates remain:

```text
174 current clipped-Delta failures
+ 596 Delta-H/multi origins
+  54 compact-q origins
= 824.
```

The next bounded work is to retain the frozen registry order while resolving
the 174 positive-first/source-seam failures, then continue through the 596
Delta-H/multi and 54 compact-q candidates.  The pure root-equality class is
empty in this registry.  No later tranche may change the integer ledger
without another complete whole-parent 3D/2D/1D/0D proof.
