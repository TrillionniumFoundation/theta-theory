# CM2 Round306B1AF4K2R230 — resolved/retained bulk authority hardening

Date: 2026-08-02

## Verdict

`PASS_NARROW_LOCAL_AUTHORITY_ONLY__NO_GO_FOR_FULL_SUPPORT_OR_CM2`

The replacement freezes and independently replays the exact Round230
resolved/retained local-bulk evidence.  It grants authority only to `784`
strict-positive-area local continuation patches and the `464` local
known-block incidence attachments derived from those patches.  An incidence
attachment is not a member assignment, a representation pullback, a physical
component, or a maximality result.

## Exact selected-row census

The pinned `67,327,799`-byte legacy certificate has SHA-256
`88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`
and result digest
`325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e`.
The replacement binds the exact result-relative path, row order, row ID,
canonical row digest, declared body digest, source file/schema/result digest,
ordinal, and transitive authority-context digest for every selected row:

- event-zero absence: `8,976`;
- exact face candidates: `1,512`;
- accepted local-bulk edges: `784`;
- rejected candidates: `740`;
- bridge stars: `448`;
- local incidence deltas: `464`;
- post-frontier occurrences: `53,968`;
- post-frontier keys: `116`.

Total: `8` tables and `67,008` rows.  Every upstream row retains its own
verified SHA-256 closure.  The largest final canonical row is `2,589` bytes,
against the fail-closed `8,388,608`-byte cap.

## Security replacement

The legacy construction manifest is opened first.  The full replay surface is
held as one descriptor set: the legacy package, Round179/208/211/220/225/229
inputs, Round186 factor kernel, and all local kernel dependencies.  Each pin is
a regular single-link file, opened with `O_NOFOLLOW`, hashed twice before
parsing, checked for path/FD identity, and fully rehashed after semantic replay.
No temporary file, spill, or `TMPDIR` is used by either producer or verifier.

Strict JSON rejects duplicate keys, floats, nonfinite constants, BOM, NUL,
surrogates, noncanonical wire encodings, trailing values, and missing final
newline.  Recursive type-strict equality rejects both `false == 0` and
`true == 1`, including nested contracts.  The 22-test attack suite passes.

## Legacy defects contained

- Legacy inputs were opened and closed one at a time instead of remaining in
  one manifest-first held-FD set through final replay.
- The legacy `importlib` factor-kernel load was not tied to the same held and
  finally rehashed path lifetime as all semantic sources.
- Ordinary Python equality in census/scope checks and multiple `== 0` credit
  checks allowed bool/int aliases.
- Selected rows had own-row hashes but no explicit transitive canonical input
  commitment binding file, schema, result, path, ordinal, ID, and row body.
- There was no final canonical per-row 8 MiB check.
- Stale `deliverables/deliverables` report/cold copies differ from the root
  package and are explicitly excluded from authority.

The replacement does not claim that the old package was wholly false.  It
replays the pinned old independent semantic model under the stronger input and
type boundary, thereby recovering only its narrow local theorem content.

## Exact replacement hashes

- producer: `b76cd281e2fccce73bea55295dc9eb34e4a3cffc4da508e1753e142c6537ba87`;
- ledger: `ff604cd343cca5f07cd9fc646a1e1a927bddecdef9a4ebd8f5aab4b39f85110c`;
- ledger object: `c889e348ee0b966f3f97b36ddf200b1610fc8cf0de29d6f0dbc7181c7807e26e`;
- verifier: `15188fa6a1627799a5a11ef6da0eaa224d56fd0fd9e4a1548292f9901f9a2838`;
- attack suite: `ec32df6cabefd6f3fe452df9ae8e099701104f3d812e42c0988b54ccba17d419`;
- verification: `b2e1465dfadafedab9ecae0080b4884fa833efe0c6e0aadfd11828b272de92a3`;
- verification object: `ea2652f38ba372b4a59a87e72c5261ac39809c904d91298c73e6edd4aecf0a6f`.

Seeds `17` and `93`, executed with Python `-I -B`, produced byte-identical
`84,467,079`-byte ledgers.  The full verifier also ran with `-I -B` under
Python `3.12.3` / python-flint `0.9.0`; explicit write and no-write modes
both returned rc `0` and produced byte-identical verification receipts.

## Missing bridge theorem and strict nonpromotion

Round230 proves equality/sign conditions only on selected local face patches.
To obtain member full support, a new bridge theorem must prove that these and
all remaining event/contact strata form an exhaustive, ownership-compatible
support construction for each member, and that the construction is physically
equivalent to the member rather than merely locally incident.  A separate
representation theorem must prove total and unique pullback of every required
representation handle.  Neither theorem exists here.

Therefore normalized full-support credit, representation-cover credit,
known-block membership credit, physical-component/maximality credit, fibre
credit, global disposition credit, B1A, B2, and CM2 are all `0`.  `D02` remains
`BLOCKED`; Gate5 remains `10/18` with zero complete 18-field global blocks;
CM2 remains `NO-GO_FOR_CLAIM`.
