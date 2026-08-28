# Round147 cold replay

`PYTHONHASHSEED=0` and `PYTHONHASHSEED=91` were used to regenerate the
certificate into two fresh temporary paths.

- seed-0 regenerated certificate SHA256:
  `db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee`
- seed-91 regenerated certificate SHA256:
  `db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee`
- sealed certificate SHA256:
  `db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee`
- certificate result SHA256:
  `00649a259ff69590eed6a9f4e828b6a622c0c03deb3ca07a70526446b827e922`
- seed-0 versus sealed bytes: PASS
- seed-91 versus sealed bytes: PASS
- seed-0 versus seed-91 bytes: PASS

The replay excluded Round145 and Round146 from its dependency snapshot and
did not pin or admit either round.
