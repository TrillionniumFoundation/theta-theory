# CM2 Round234 cold replay

Environment: `.venv-cm2`, Python 3.12, `python-flint 0.9.0`.

`PYTHONHASHSEED=234071` and `PYTHONHASHSEED=234929` both reproduced:

- producer result `d05d6bbc590157e855a577f411668d0f3b7486ccdbea8e47ed30299194b5ba08`;
- certificate `6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac`;
- verification result `417a8d97fcbba4dd48b99c488b8bb908355f35af014c283b70faf325df307598`.

Both producer and independent verifier exited zero.
