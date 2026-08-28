# Round294-B registry-builder admission closure

## Verdict

PASS as a zero-credit evidence-admission closure.

Round294 remains immutable. Round294-B repairs one dependency-boundary
omission: the Round294 producer pinned the Round292-A result, ledger,
verification, and manifest, but did not directly hash the actual Round292-A
independent-verifier source. Round294-B now directly validates:

- the inert Round292 registry builder:
  `2c0b7e864839880f47cca2989b3f8d48fcec0399c0644c92f8aabab225402004`;
- the actual Round292-A verifier:
  `9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010`;
- the Round292-A manifest:
  `4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870`;
- the Round294 manifest:
  `90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131`.

The producer and independent verifier require the exact seven-member
Round292-A manifest and exact nine-member Round294 manifest. Every one of the
16 actual members is a HERE-only regular, non-symlink, single-link file with
the exact committed SHA-256. Extra, missing, renamed, path-escaped, or
substituted members fail closed.

## Registry census retained

Round294-B rechecks, but does not change, the sealed Round294 census:

| field | value |
|---|---:|
| formal registry rows | 431,208 |
| preserved Round266 occurrences | 126,468 |
| new Round288 atom occurrences | 295,336 |
| new refined Round287 occurrences | 9,404 |
| total formal new occurrences | 304,740 |
| representation bindings | 46,288 |
| binding rows issuing occurrence IDs | 0 |

The exact deterministic GZIP streams expand to 1,495,443,148 registry-ledger
bytes and 136,099,588 representation-binding-ledger bytes.

## Explicit rejection boundary

The closure independently preserves all three required rejections:

- direct issuance of all 10,020 Round287 unions is rejected;
- the superseded 431,824 registry census is rejected;
- the legacy pre-Round294 value 63,224 is rejected as a current quotient.

The nonadmissible Round292-B witness-binding artifact is absent from the
dependency graph.

## Independent verifier and attacks

The verifier does not import or execute the Round294-B producer or any
Round292/Round294 producer. It reconstructs the complete expected admission
object before opening the candidate result.

All 38 attacks are rejected. They include direct-verifier/manifest pin
substitution, exact-set omission, fully re-signed census and credit forgeries,
revival of 10,020 / 431,824 / 63,224, attempted Round292-B consumption,
duplicate/trailing/non-integral/non-finite/non-UTF8 JSON, malformed
manifests, symlink/hardlink/FIFO/directory/missing/path-escape substitutions,
and truncated/concatenated/trailing/non-deterministic GZIP.

## Strict nonpromotion

Round294-B grants no mathematical credit. Registry delta, binding delta, new
occurrence, alias, component, DSU rank, seam, `Jx/Jy`, maximality, fibre, and
global-disposition credits are all zero. The expanded-registry DSU remains
`NOT_REBUILT`, its quotient count remains null, Gate5 remains `10/18`, D02
remains blocked, and CM2 remains no-go for claim.

All new downstream consumers of the Round294 registry package must directly
pin the Round294-B manifest and verification. Existing sealed Round294 and
Round295+ artifacts remain unchanged historical packages.

## Commitments

- producer:
  `ed8346b550c461cea28a4a01393c4c5d1be802f9e6145537a0ae7fe5c2e13192`;
- result file:
  `656676d6f5dd4accc7b9aa473a14d9c1326b83eff2fe8974e7b43694adb44ccc`;
- result object:
  `c7737386ce2db72315d71a05cfedf474c0b1ff4a00306851a5294f6a6e58e221`;
- verifier:
  `f6aa9278de7a8c478b6c4d8b49bbf8517f54ba1fb2a2b15fda5ce8afae41cc92`;
- verification file:
  `b1440432a082b392de744bc6f4ca20e893122cb923a3236899357ccfb4fd6581`;
- verification object:
  `1746adb7b71607909eae031da879671885deee8602fdb5685dc561ba9afa4179`;
- attack-suite file:
  `4d4f99615078062b0fbc544ff04245f6bd9055beb3ca8807480e0aff4aacdcff`;
- attack-suite object:
  `113f8d6b6b636b1f6116f5cec32438a33e16d2fdcf6c2b9bcf13bf9c6bb68499`.
