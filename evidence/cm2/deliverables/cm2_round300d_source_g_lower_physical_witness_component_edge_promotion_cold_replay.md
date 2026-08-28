# Round300-D cold replay

Run from the repository `deliverables` directory with Python 3.12 or newer.
No network access, producer cache, persisted expected ledger, or producer
import is required by the independent verifier.

```bash
set -euo pipefail
P=cm2_round300d_source_g_lower_physical_witness_component_edge_promotion

sha256sum -c "${P}_manifest.sha256"

PYTHONHASHSEED=101 python "${P}.py" \
  --seed 300401 \
  --ledger "${P}_replay_alpha_ledger.json.gz" \
  --result "${P}_replay_alpha_result.json"

PYTHONHASHSEED=909 python "${P}.py" \
  --seed 987654321 \
  --ledger "${P}_replay_beta_ledger.json.gz" \
  --result "${P}_replay_beta_result.json"

cmp "${P}_ledger.json.gz" "${P}_replay_alpha_ledger.json.gz"
cmp "${P}_ledger.json.gz" "${P}_replay_beta_ledger.json.gz"
cmp "${P}_result.json" "${P}_replay_alpha_result.json"
cmp "${P}_result.json" "${P}_replay_beta_result.json"

PYTHONHASHSEED=313 python "${P}_verifier.py" \
  --seed 300411 \
  --attacks "${P}_replay_alpha_attack_suite.json" \
  --verification "${P}_replay_alpha_verification.json"

PYTHONHASHSEED=733 python "${P}_verifier.py" \
  --seed 300499 \
  --attacks "${P}_replay_beta_attack_suite.json" \
  --verification "${P}_replay_beta_verification.json"

cmp "${P}_attack_suite.json" "${P}_replay_alpha_attack_suite.json"
cmp "${P}_attack_suite.json" "${P}_replay_beta_attack_suite.json"
cmp "${P}_verification.json" "${P}_replay_alpha_verification.json"
cmp "${P}_verification.json" "${P}_replay_beta_verification.json"
```

Expected stable byte pins:

```text
56e414eba093fb0ceb9a78895b94b63ccff3beaf590b05d4e969d43d767ac333  cm2_round300d_source_g_lower_physical_witness_component_edge_promotion.py
287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7  cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_ledger.json.gz
59b7e788ed217ceb590a3e2125cc13aefbf447af236315ea607f4f631cb29c84  cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_result.json
d7fbbeeb3f0959de54e55f20928f276a36df75100907b1af16bb2e46317ddc26  cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_verifier.py
b0b201a2c3f7255bd9d386bead2ab1e7b66711581d1cf09033cb4edfe267fbcf  cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_attack_suite.json
a5bd12b10103b4785574bd4633e608c7fd5107369ba8f2343ebffe7e08eba1c7  cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_verification.json
```

Validate strict single-member deterministic gzip, JSON self-closures, and
single-link regular files:

```bash
python - <<'PY'
import hashlib
import json
import os
from pathlib import Path
import stat
import zlib

p = "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion"

def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()

raw = Path(p + "_ledger.json.gz").read_bytes()
assert raw[:3] == b"\x1f\x8b\x08"
assert raw[4:8] == b"\x00\x00\x00\x00"
decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
for offset in range(0, len(raw), 1 << 16):
    decoder.decompress(raw[offset:offset + (1 << 16)])
decoder.flush()
assert decoder.eof and decoder.unused_data == b""

for suffix, field in (
    ("_result.json", "result_sha256"),
    ("_verification.json", "verification_sha256"),
):
    document = json.loads(Path(p + suffix).read_bytes())
    claimed = document.pop(field)
    assert hashlib.sha256(canonical(document)).hexdigest() == claimed

for path in Path(".").glob(p + "*"):
    info = os.lstat(path)
    assert stat.S_ISREG(info.st_mode)
    assert info.st_nlink == 1
    assert not path.is_symlink()
PY

test "$(wc -l < "${P}_manifest.sha256")" -eq 8
sha256sum -c "${P}_manifest.sha256"
```

After replay, the temporary files may be removed:

```bash
rm -f "${P}"_replay_alpha_* "${P}"_replay_beta_*
```

The accepted result must retain:

- 111,524 incidence edges and 1,600 assignment exclusions;
- 86,308 same-key and 25,216 cross-key edges;
- `eligible_for_component_DSU_application=false`;
- zero identity/key-merge/component-edge/union/quotient/DSU/maximality/fibre/
  disposition credit;
- historical 29,984 status diagnostic-only, with no issued quotient count.
