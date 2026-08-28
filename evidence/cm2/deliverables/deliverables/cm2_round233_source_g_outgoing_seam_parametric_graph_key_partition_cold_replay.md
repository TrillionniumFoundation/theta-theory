# CM2 Round233 cold replay

Environment: `.venv-cm2`, Python 3.12, `python-flint 0.9.0`.

`PYTHONHASHSEED=233071` and `PYTHONHASHSEED=233929` both reproduced:

- producer result `6be5b81be350a7d575fb34dd80fce53046fb017096d497070a218c04f92a88fc`;
- certificate `cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41`;
- verification result `d01cafb426600dadbba6e874be609f55666273a510a7a1f267d5399eb5d54669`.

Both producer and verifier exited zero.  The verifier independently reran the
interval geometry on all `3,148` candidate roots.
