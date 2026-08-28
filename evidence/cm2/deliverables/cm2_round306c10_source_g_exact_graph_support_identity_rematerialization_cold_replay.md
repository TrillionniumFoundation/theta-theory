# Round306C10 Cold Replay

- Environment: `env -i`, explicit `PATH=/usr/bin:/bin`, `PYTHONHASHSEED=314159`, `/usr/bin/python3 -I -B -S`.
- Mode: producer candidate build outside `deliverables/`, traced with `strace -ff -qq -e trace=%file`.
- Status: `PASS_5264_EXACT_G2_FEATURE_SUPPORT_ASTS__5264_NATURAL_KEY_IDENTITIES_PRESERVED__ZERO_PHYSICAL_PULLBACK_TRACE_GLOBAL_SUPPORT_CREDIT`.
- Exit status: `0`.
- Trace files: `1`.
- Deliverables mutation syscalls: `0`.
- Published output in `deliverables/`: `false`.

The cold candidate reproduced all three candidate files byte for byte:

- Exact graph support ledger: `b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c`.
- Member identity disposition ledger: `5041df1ab4b5bf9e79984859f828c9fb69718f53bd62d2920d51ebea8b7ec9df`.
- Result: `b188eaa6c4dee77e0fff13b4a48cec9f8b46d324e48e7927265807a0f2865b55`.

This cold replay validates deterministic reconstruction and the no-write boundary only. It does not grant physical-incidence, pullback, trace, normalized-support, B1A, B2, maximality, or CM2 credit.
