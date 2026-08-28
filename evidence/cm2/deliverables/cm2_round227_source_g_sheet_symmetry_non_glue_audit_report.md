# Round227 source-G sheet symmetry non-glue audit — frozen report

## Verdict

`PASS_PARTIAL_FORMAL_ROUND227`.

All `17,716` Round211 event sheets have one exact Jx partner and one exact Jy
partner.  The `35,432` directed partner rows form exactly `4,429` disjoint
Klein-four orbits, each of size four, with full sheet coverage.  Jx and Jy
commute on every sheet, and every generator edge remains inside its reported
orbit.  The canonical
orbit-member hash is
`1daabf6231863b9ed9225a647b8813b6820d9db316d00e79c38b596959ad185d`.

Round173 pins Jx and Jy as the nonidentity physical reflections
`(x,y,s,p)->(-x,y,-s,-p)` and `(x,y,s,p)->(x,-y,s,-p)`.  Their exact sheet
partners prove equivariance; they do not give two atlas coordinate names for
one physical point.  Consequently every symmetry row and orbit has zero
physical-glue and component-union credit.

## Hostile audit

The independent verifier reconstructed all partner rows and orbits without
importing or executing the Round227 producer.  It rejected `10/10` freshly
re-signed semantic attacks, `16/16` strict-JSON attacks, and `8/8` path/file
object attacks.  The attack suite
explicitly includes attempts to turn a symmetry partner/orbit into an atlas
glue or physical component.

Cold replays under `PYTHONHASHSEED=227041` and `227919` both exited zero and
produced identical stdout and verification hashes.

## Frozen hashes

- producer: `71ecc4f3bfbd0740656cdf4f11efa52451e22ff4cb95d5960d4f897fb6c8603f`;
- certificate: `fa8d518239d2f2d4eb993ac58c66ffe2b7d222fa8efd4d916689cebd05201461`;
- certificate result: `fe134a35a2bb601f79ed4b712eba0cdb9a01db696bf854a24678a006ab2036ba`;
- verifier: `0007c88a7e7d63985ca1ac13fc81338d644487b01cdcf6336edfd6584aaddf6e`;
- verification: `a0446082bb4f7c9b2f35885ce085237dfd2eec4789aa8447c0b0e85864d500e6`;
- verification result: `1e5c854ea9adbf4ee2d0e4959b2a043d135136e90cd4babb4639661759fa15d9`.

## Strict boundary

No union-find edge is added.  The `7,404` known-connectivity blocks remain a
lower-bound quotient, not maximal physical components.  D02 remains
`BLOCKED`, Gate5 remains `10/18`, and CM2 remains `NO-GO_FOR_CLAIM`.
