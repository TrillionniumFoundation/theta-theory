# Complete R75 archives

These are the complete archives, stored in ordered raw byte parts of at most 6 MiB for GitHub connector transport. Each part and each reassembled archive has an exact SHA-256. The filenames, contents and roles are fixed by [ARCHIVE_PARTS.json](ARCHIVE_PARTS.json).

| Complete archive | Bytes | SHA-256 |
|---|---:|---|
| `General_Theta_Foundations_I_R75_Source.zip` | 21,875,209 | `0eda004670c3baa56cfccf398611407e74601cc4b9655d5b12b06d43dc58961e` |
| `General_Theta_Foundations_I_R75_Validation.zip` | 28,390,060 | `a4dc9ee29e7a48f9b76b479fea25e24a41d975c86adf1a3923a879ae23ae75d7` |
| `General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz` | 24,147,671 | `d9722229622f615401c7df4df83f6062ef04202923f0ec460569591c22164dae` |

The source ZIP is the exact 386-file final source tree, including the complete inherited proofs, diagnostic programs, referee response, provenance and correction history. The validation ZIP includes the final strict execution, both failed attempts, the preceding successful run, full native logs/auxiliaries and the rendered-page inspection evidence. The historical corpus is the unchanged 6,432-blob archive authenticated by the source indexes.

From the complete publication directory:

```bash
python3 verify_received.py
python3 restore_archives.py --out /tmp/general-theta-r75-archives
```

Both commands verify the full delivery, each part, each complete archive and its exact member inventory. The restoration command refuses to overwrite a different existing output. The source ZIP contains `General_Theta_Foundations_I_R75_Source/`; the validation ZIP contains `General_Theta_Foundations_I_R75_Validation/` and its internal `ARCHIVE_MANIFEST.json`.

## Ordered part links

### General_Theta_Foundations_I_R75_Source.zip

- [General_Theta_Foundations_I_R75_Source.zip.part001](General_Theta_Foundations_I_R75_Source.zip.part001) — 6,291,456 bytes; SHA-256 `214c51bf3e113a4f66bdd18152e727218777f7428244a61725ccef81250c467b`
- [General_Theta_Foundations_I_R75_Source.zip.part002](General_Theta_Foundations_I_R75_Source.zip.part002) — 6,291,456 bytes; SHA-256 `dcb41d377c2ecb9ac3167012a10596cba699774fa460e9abd6729d702cb466ac`
- [General_Theta_Foundations_I_R75_Source.zip.part003](General_Theta_Foundations_I_R75_Source.zip.part003) — 6,291,456 bytes; SHA-256 `4bcadc844d7c5b6214f8612cc476dc42867c927d9675c3affc1fe57b54b400a4`
- [General_Theta_Foundations_I_R75_Source.zip.part004](General_Theta_Foundations_I_R75_Source.zip.part004) — 3,000,841 bytes; SHA-256 `e6b00384436ea3fb63f6f798cb33409a4cde7c5370539ccbad20177428dbc7fc`

### General_Theta_Foundations_I_R75_Validation.zip

- [General_Theta_Foundations_I_R75_Validation.zip.part001](General_Theta_Foundations_I_R75_Validation.zip.part001) — 6,291,456 bytes; SHA-256 `92d39c1e05cbf85609540c7facc67b9ad545f7c5e615f4fd22d29ff5ba694aa0`
- [General_Theta_Foundations_I_R75_Validation.zip.part002](General_Theta_Foundations_I_R75_Validation.zip.part002) — 6,291,456 bytes; SHA-256 `b1ddf6f50a24e9209fd051eb83681717f393d7e8f55d0f7368f7e0e447d9a0f4`
- [General_Theta_Foundations_I_R75_Validation.zip.part003](General_Theta_Foundations_I_R75_Validation.zip.part003) — 6,291,456 bytes; SHA-256 `45d40314e2c682a7ae2a5233266e8e7d3a5edbec7fdde0964d65c897fe291b04`
- [General_Theta_Foundations_I_R75_Validation.zip.part004](General_Theta_Foundations_I_R75_Validation.zip.part004) — 6,291,456 bytes; SHA-256 `263c4486c675d11955f73d60f3ed448d07cb8815a3dfb55d6e64994b6c65444b`
- [General_Theta_Foundations_I_R75_Validation.zip.part005](General_Theta_Foundations_I_R75_Validation.zip.part005) — 3,224,236 bytes; SHA-256 `fd38fa0cf1837f2701e21604b80ec907ac484e6ca2f4fda6f49e321e7d2bc213`

### General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz

- [General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part001](General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part001) — 6,291,456 bytes; SHA-256 `abf021642873a7c25417acbf170930f4d7ac1a7384a9e385816015c9d49b9ac2`
- [General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part002](General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part002) — 6,291,456 bytes; SHA-256 `3a7658ba99c8dad1aa77bd036578777ea9d876574e903e9850750bd8ab7367d9`
- [General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part003](General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part003) — 6,291,456 bytes; SHA-256 `169cc9b2981149eec7b853de82446c9b2dfb9cd77766cb89a4b02926c5eafd2e`
- [General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part004](General_Theta_Foundations_I_R75_Historical_Text_Corpus.tar.gz.part004) — 5,273,303 bytes; SHA-256 `77ad0a827d5c3277526073a6bff627ac72ee8d59f49ccdfd2a7c52ce116a8c83`
