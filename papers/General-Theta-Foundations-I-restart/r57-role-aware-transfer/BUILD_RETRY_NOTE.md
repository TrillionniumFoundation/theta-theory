# Citation-audit rebuild

The initial hosted run 38514626770 failed its auxiliary-file citation audit after the native 27-page PDF compiled. Its error was `declared citation CGM97 absent from aux`. CGM97 and GG99 were already cited together in the source. This follow-up emits grouped citation keys separately. It also supplies contextual introduction citations for three inherited bibliography entries (CCGK, ACSS, DPChatter) and strengthens the source verifier to reject uncited native entries. All existing bibliography entries and mathematical statements are retained. The ordinary source is re-sealed before its immutable source commit; the complete retained build is rerun.

Citation-normalized native inputs: .
