# Reassemble the inspected page images

The 26 inspected PNG images are preserved in the original ZIP as two ordered raw byte parts. No image, ZIP member, compression stream or archive metadata was changed. Concatenating the parts reproduces the original 14,459,769-byte ZIP exactly.

| Part, in required order | Bytes | SHA256 |
|---|---:|---|
| `inspected-page-images.zip.part01` | 8,388,608 | `412327f5e576f8d3e36763ae3480d6721a8d963608924e900124ddd0510a4ee3` |
| `inspected-page-images.zip.part02` | 6,071,161 | `2553fd1296bc6dcfe969fd4141496e171ca909a94b186b2dbe5f598ec8c6e0ce` |

Run these commands from this directory:

```sh
cat inspected-page-images.zip.part01 inspected-page-images.zip.part02 > inspected-page-images.zip
sha256sum inspected-page-images.zip
```

The required whole-archive SHA256 is:

```text
40d2b4a0bd42fe071c53020c4a2599f91acebe009f5b92c51d122227565aa9b6
```

For a platform-independent verification and reconstruction using Python:

```python
from pathlib import Path
import hashlib
import json

folder = Path(".")
manifest = json.loads((folder / "ARCHIVE_PARTS.json").read_text())
parts = []
for part in manifest["parts"]:
    data = (folder / part["path"]).read_bytes()
    if len(data) != part["bytes"] or hashlib.sha256(data).hexdigest() != part["sha256"]:
        raise SystemExit("Part verification failed: " + part["path"])
    parts.append(data)
archive = b"".join(parts)
if len(archive) != manifest["archive_bytes"] or hashlib.sha256(archive).hexdigest() != manifest["archive_sha256"]:
    raise SystemExit("Archive verification failed")
(folder / manifest["archive_filename"]).write_bytes(archive)
print("Verified archive:", manifest["archive_filename"])
```

The rebuilt ZIP is ignored by the article's exact-path Git rule; both parts, these instructions and their hashes remain in the release. `PDF_VISUAL_QA.json` retains the original whole-archive hash and every inspected image hash. `ARCHIVE_PARTS.json` records the successful byte and member verification and the actual transport error: the unsplit base64 request exceeded the connector's stated 16 MiB request-body limit. This was an HTTP transport-size failure, not an approval rejection. Splitting this evidence archive changes no mathematical or build source and makes no new mathematical or CI claim.
