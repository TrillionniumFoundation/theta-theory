# A2-DYN: clearance-to-roof and critical-return stability author revision

This is an author revision of Qian Qi's original paper, not a new referee review. It retains the complete downloaded v112 active manuscript and the earlier local clearance-flux extension, and adds modules274–275 with full proofs. The scientific target, physical section, collision clock, displacement/return labels and limit order are unchanged.

Run `bash build.sh` in this directory. Dependencies: Python3 with NumPy and SymPy; pdfLaTeX with the listed standard AMS/Latin Modern packages; Poppler `pdfinfo` and `pdftoppm`. Each mathematical diagnostic runs normally and under `python3 -O`, and outputs must agree. The final LaTeX log must contain no unresolved references, duplicate labels, overfull boxes, errors or rerun request. `manuscript/A2-DYN-clearance-roof.pdf` is copied only after those gates pass. Execution receipts are in `evidence/current/` and build logs in `build/`.

Start with `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, and `REVISION_BASE.json`. The active article supplies the complete new proof bodies, but the original recursive historical archive is source-pinned rather than fully downloaded here. Read `HISTORY_PRESERVATION_AUDIT.md` before making any claim of exhaustive historical reconstruction or remote ancestry.

The new regular critical coefficient is an actual return-stability weight, not a conditioning on a periodic orbit. Integrated folds are controlled locally without a fixed-clearance density bound. All global all-word, collision-normalized source/capacity closure claims remain false. This is a substantive partial author revision, not a claim that the requested full journal-level mathematical completion has been achieved.
