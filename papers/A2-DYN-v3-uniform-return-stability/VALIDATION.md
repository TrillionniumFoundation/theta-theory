# Reproducing the A2-DYN v3 source and finite checks

From this directory:

```sh
mkdir -p evidence
python3 tools/audit_v3.py > evidence/audit-v3.json
python3 -O tools/audit_v3.py > evidence/audit-v3-optimized.json
cmp evidence/audit-v3.json evidence/audit-v3-optimized.json
python3 tools/certify_winding.py > evidence/certify_winding.py.json
python3 tools/verify.py > evidence/verify.py.json
python3 tools/certify_excursion.py > evidence/certify_excursion.py.json
python3 tools/verify_v2.py > evidence/verify_v2.py.json
bash build.sh
```

The winding and excursion scripts provide finite rational enclosures. The two retained verification scripts check finite algebra and explicitly floating physical examples. The new audit checks literal TeX inputs, byte-preserved proof blocks and labels, and finite normalization/conditioning inequalities. It is not a proof assistant or a substitute for the continuous arguments in Sections 4 and 10.

In the local validation, all five scripts also ran under `python3 -O` with byte-identical output. The actual TeX recorder closure agreed with the thirteen declared manuscript files. The 23-page PDF compiled with no final warning, undefined-reference, overfull or underfull findings and was rendered for visual inspection. Details and output hashes are in `evidence/local-validation.json`; that file makes no remote-CI claim.

The repository workflow `.github/workflows/a2-dyn-v3.yml` builds the exact event commit, compares source audits before and after compilation, and uploads the PDF and generated evidence. Its two external actions are pinned to the commit objects returned for the official v7 tags on 5 October 2026. A workflow's eventual result must be read from its actual run; merely adding this workflow is not a successful CI execution.
