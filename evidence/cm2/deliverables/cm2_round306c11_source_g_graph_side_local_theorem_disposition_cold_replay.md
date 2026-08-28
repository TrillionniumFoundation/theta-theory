# Round306C11 Cold Replay

- Environment: `env -i`, explicit `PATH=/usr/bin:/bin`, `PYTHONHASHSEED=311777`, `/usr/bin/python3 -I -B -S`.
- Mode: producer candidate build outside `deliverables/`, traced with `strace -ff -qq -e trace=%file`.
- Status: `PASS_10118_GRAPH_SIDE_ROUTING_DISPOSITIONS__9950_CANDIDATE_READY_ROUTING__168_STRUCTURALLY_BLOCKED__10_MISSING_LOCAL_SHARED_REROUTE_FINDINGS__ZERO_LOCAL_THEOREM_AND_DOWNSTREAM_CREDIT`.
- Exit status: `0`.
- Trace files: `1`.
- Deliverables mutation syscalls: `0`.
- Published output in `deliverables/`: `false`.

The cold candidate reproduced all five candidate files byte for byte:

- Disposition ledger: `b1af6336b83842f2c6380929977f6d3591cfb50a1b305c7eafd197931d623543`.
- Candidate-ready routing ledger: `a0ec0b8e13b51a7495fb5eda6221bb7cf1dde8cceeb4c4e4893f5a7fe6f32014`.
- Blocked ledger: `8607da23d37de93d6cdf8e04a36d2f70d7908e8b55a8595cd34693f377479bdf`.
- Reroute findings: `3e257ca914aeb2306eab4064a118d5f1e28a753a215e694b137233a3b066f5c8`.
- Result: `083103ac958dfcb01283850abcda03fcdce26a8910c42b79c570a87486925506`.

This cold replay validates deterministic routing classification and the no-write boundary only. It grants no local theorem, physical-incidence, trace, pullback, normalized-support, DSU, B1A, B2, maximality, or CM2 credit.
