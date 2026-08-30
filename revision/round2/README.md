# Referee round-two bootstrap

This directory contains a SHA-256-pinned payload used once to materialize the
eleven-paper positive referee revision. The bootstrap workflow verifies the
archive, expands it, inserts every addendum into the controlling `main.tex`,
builds all eleven manuscripts, deletes this bootstrap directory, and pushes
the materialized revision to the same branch.
