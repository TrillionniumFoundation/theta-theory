# CM2 Round231–232 cold replay

Date: 2026-07-27

Using `.venv-cm2` with `python-flint 0.9.0`:

- Round231 `--no-write` reproduced result
  `83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a`
  and certificate
  `7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374`.
- Round232 `--no-write` reproduced result
  `7cbaaba7964555eee3018927688d8c6aa2cdabbf354125ec2b389e92301cb313`
  and certificate
  `a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0`.
- Independent verifier `--no-write` reproduced
  `PASS_INDEPENDENT_ROUND232` and verification result
  `e172ebc533eb18a7f4076fee4c3620801455013698cd4eb29037e6536522ebb8`.

All `6,804` promoted descendant interval classifications were independently
recomputed during verifier replay.
