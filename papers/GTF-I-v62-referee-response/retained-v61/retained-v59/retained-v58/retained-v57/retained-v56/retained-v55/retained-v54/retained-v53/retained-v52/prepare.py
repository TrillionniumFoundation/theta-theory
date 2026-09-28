"""Check that the already materialized v52 native source has its required files.

Remote assembly is handled by the v52-only bootstrap outside this directory.
This command performs no file or repository mutation.
"""
from pathlib import Path
import json

def main():
    root=Path(__file__).resolve().parent
    required=['main.tex','noisy-rigidity.tex','effective-surplus.tex','global-certificates.tex',
              'uniform-resources.tex','EXPECTED_V51.json','RESPONSE_TO_REFEREE.md']
    missing=[n for n in required if not (root/n).is_file()]
    if missing:raise SystemExit('Incomplete v52 source: '+', '.join(missing))
    print(json.dumps({'status':'materialized','revision':52,'checked':len(required)}))
if __name__=='__main__':main()
