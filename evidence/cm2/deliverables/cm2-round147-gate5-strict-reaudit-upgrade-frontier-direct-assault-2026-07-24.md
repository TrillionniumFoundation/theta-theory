# Round147 direct hostile assault

Independent verification status: PASS.

- semantic checks: 205
- re-signed semantic mutations rejected: 16/16
- hostile process/I/O cases rejected: 10/10

Semantic mutations covered illicit F5 promotion, maturity/block-count
promotion, invented historical parent-W and Round35 restriction, invented
Round50 owner, invented Round54 t54, invented Round67 Omega_j and q_j,
partial future-slot binding, field deletion/reordering, deletion of the D02
frontier, Gate5/CM2 promotion, and strict-nonclaim deletion.

Process/I/O attacks covered invalid UTF-8, appended JSON, double newline,
noncanonical pretty JSON, missing newline, UTF-8 BOM, directory, FIFO,
symlink, and oversized sparse input.

- certificate SHA256:
  `db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee`
- verification SHA256:
  `8302642619f66a4a47ec79d8fefb0230378331b578a363f12ad1b64dffebbd3d`
- verification result SHA256:
  `340a899a53e3124d2e3210a627eb29bb87725cc88c56040257d58ef2b5e2e7da`
