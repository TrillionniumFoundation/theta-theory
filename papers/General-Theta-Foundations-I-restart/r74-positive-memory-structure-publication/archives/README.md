# Complete archives and lossless reconstruction

The full native source is already present as ordinary files in the sibling R74 source directory. These additional archives preserve the complete exact source snapshot, actual validation evidence, and historical text corpus.

Large single-blob requests failed at the GitHub plugin transport. Each archive is therefore stored as ordered ordinary Git blob parts of at most 6 MiB. The parts concatenate byte-for-byte to the original archive; they are not individually valid ZIP files. `ARCHIVE_PARTS.json` fixes both each part and each complete archive by size and SHA-256.

From the publication directory, run:

```bash
python3 verify_received.py
python3 restore_archives.py --out /tmp/general-theta-r74-archives
```

The first command checks publication bytes, complete reconstructed archive hashes, and every validation payload hash without modifying the directory. The second writes the three complete archives to the chosen output directory, using only the Python standard library. It refuses to overwrite an existing file with different bytes. The full individual archives are also supplied as downloadable author-delivery files.

## General_Theta_Foundations_I_R74_Source.zip

Complete size: **20,503,674 bytes**. SHA-256: `ff37f29830ffcf9f1a9b375a0d572ff4042ba90f743238ee1a284ea4363d557f`.

| Part | Bytes | SHA-256 |
|---|---:|---|
| [General_Theta_Foundations_I_R74_Source.zip.part001](General_Theta_Foundations_I_R74_Source.zip.part001) | 6291456 | `811004c65a5454a894febeaddffc6637b9a27714a3709a39df533008276aaf47` |
| [General_Theta_Foundations_I_R74_Source.zip.part002](General_Theta_Foundations_I_R74_Source.zip.part002) | 6291456 | `b33e3bc8de78e3ba1d8c2549fa0083befbe6d5047499580d46b2519c601acc51` |
| [General_Theta_Foundations_I_R74_Source.zip.part003](General_Theta_Foundations_I_R74_Source.zip.part003) | 6291456 | `124b1286ba7bd294fc86ac9125ad401d4b13a24ecef5585170167233928b6af4` |
| [General_Theta_Foundations_I_R74_Source.zip.part004](General_Theta_Foundations_I_R74_Source.zip.part004) | 1629306 | `9c0460b7b8641b0d6c80d756a12e383639dcd373176cde7b432fa6b93a1aa6b7` |

## General_Theta_Foundations_I_R74_Validation.zip

Complete size: **18,864,318 bytes**. SHA-256: `1b74d67ae07e8abcc41a4347c455afbd720384c5392df5096414f205fbde0475`.

| Part | Bytes | SHA-256 |
|---|---:|---|
| [General_Theta_Foundations_I_R74_Validation.zip.part001](General_Theta_Foundations_I_R74_Validation.zip.part001) | 6291456 | `edfbe0e778ecb8b339e0e35e444ee1450925a4da73f6b9883543a94f70c58346` |
| [General_Theta_Foundations_I_R74_Validation.zip.part002](General_Theta_Foundations_I_R74_Validation.zip.part002) | 6291456 | `d02a71a52c9f9bf96a9eb9563deeb98840eff05745c0acad11a1805b2a1d7856` |
| [General_Theta_Foundations_I_R74_Validation.zip.part003](General_Theta_Foundations_I_R74_Validation.zip.part003) | 6281406 | `6350af64d7182311eca99236a1fe26524f086066d7b66c1c0e56c0616156c6d8` |

## General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz

Complete size: **24,147,671 bytes**. SHA-256: `d9722229622f615401c7df4df83f6062ef04202923f0ec460569591c22164dae`.

| Part | Bytes | SHA-256 |
|---|---:|---|
| [General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part001](General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part001) | 6291456 | `abf021642873a7c25417acbf170930f4d7ac1a7384a9e385816015c9d49b9ac2` |
| [General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part002](General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part002) | 6291456 | `3a7658ba99c8dad1aa77bd036578777ea9d876574e903e9850750bd8ab7367d9` |
| [General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part003](General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part003) | 6291456 | `169cc9b2981149eec7b853de82446c9b2dfb9cd77766cb89a4b02926c5eafd2e` |
| [General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part004](General_Theta_Foundations_I_R74_Historical_Text_Corpus.tar.gz.part004) | 5273303 | `77ad0a827d5c3277526073a6bff627ac72ee8d59f49ccdfd2a7c52ce116a8c83` |

