# Round173 cold replay

Date: 2026-07-26

The producer was run under `PYTHONHASHSEED=17301` and `17303`.  Both outputs
were byte-identical to the frozen certificate.

The independent verifier was run against those two certificates under
`PYTHONHASHSEED=17307` and `17309`.  Both outputs were byte-identical to the
frozen verification.

```text
certificate sha256
5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a

verification sha256
e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99
```

The replay used the system Python 3 standard library only.  No earlier
artifact was modified.
