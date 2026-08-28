# Round306C6 corrected G2 invalidation and fresh DSU freeze

Status: `PASS_INDEPENDENT_66688_INVALIDATIONS__476118_EDGES__61928_FRESH_COMPONENTS_REPLAY`.

- The sealed C5 empty-graph dispositions invalidate exactly `33,344` sheet members and `33,344` side members from the sealed C0 universe. All `66,688` identities join uniquely to C0 member rows.
- The invalidations affect `42,196` old base roots: `33,344` are deleted, `8,852` are rekeyed from retained membership, and `325,752` remain unchanged. The fresh universe contains `497,772` members and `334,604` base roots.
- All `478,718` C0 edge applications were replayed. Exactly `2,600` `R300E_HALF_OPEN_OWNER` rows hit deleted roots and are dropped; `476,118` rows remain. No invalid member occurs as a canonical occurrence endpoint.
- Forward and reverse application from separate empty DSUs both reduce rank by `272,676` and produce the same `61,928`-component partition. Its SHA256 is `989fa50c0915cbea0c5cf13e20c0c01c858580a47d366ad05f179d7392f75bbb`.
- The fresh cross-component pair denominator is `123,410,984,634`; the component member-size vector SHA256 is `b814f69e61d8f9c38db99aa8e138b13f0686b0edbd154bd5c28b4389952d80b0`.
- Six full ledgers contain `1,807,658` rows. Two hash seeds produced byte-identical eight-file candidates. The independent verifier does not import, execute, or parse the producer and rejected all `16` coherent attacks.
- After complete package sealing, fresh member-universe and fresh-DSU credit may be recorded. Normalized support, B1A, B2, maximality, and CM2 remain zero.

Artifact SHA256 values:

- Producer: `f44e2f77f000ae34e3b0a4355d1a10c77c69c2fbef5746374d81b03e0460d7d1`
- Member invalidation ledger: `7f4c361b5039b9adac60cdb08405f384dc4a05bbe66b4ae2eac49ac02204e3db`
- Base-root disposition ledger: `42873309e86486edb03a45bb365735d4c9d94b7f6af49f09cf003a8663b6a9e0`
- Edge application ledger: `9d0421e5e01a14b67a005894ce6b73b3abe2443d95a9194ca52b55d6314554cb`
- Member-component ledger: `730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2`
- Base-root-component ledger: `6ba4dcaf45c125c7afbfd5cdf9ad60ef5fa16f26ba123d443cbc3d2f2d905165`
- Component census ledger: `a5aea01409ae3678fdc6b86fc3f1edfdfa41da013809dbadd217dda7e2eaf389`
- Cross denominator: `24b05554613dff1b4615a927d26fb5b15859b2ce59355421fde844243d60d2de`
- Result file: `3f4e3e666dfe0b5b3a163c866057031b42dac09000175f4bc0b32ec353c5e4c5`
- Result object: `e926547acb5032a33d8194ecdfac51ba0761c26f936366bdde5fd79a3e16da76`
- Independent verifier: `255bf25f290cba755359da657b054107375517bc2627e31633bcf6ba0d49c2a4`
- Attack file: `797c8fdc45c43a292105ba4078413452d5c5b52d67ea97d04e6962a357529fa3`
- Verification file: `5e6aa16e04140f046b350e70f205ef76c58ca5c9676888c942407061072e6039`

Global status remains `NO-GO_FOR_CLAIM`.
