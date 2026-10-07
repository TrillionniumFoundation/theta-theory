# Historical derivation audit — revision 27

The controlling v26 report was read in full at commit `20337e845157a833fe770687ea98f337788fa586`, blob `f75e48fa7276be7be654c61afe3cc276ba44d514`. The exact v26 baseline artifact was downloaded from run `37537199282`, artifact `11446932702`, and extracted with all archived A2-DYN sources. The reviewed source is `6a790b65b48f57d264dbc7871bd1ae46571c2662`, ordinary paper tree `6101fe93f514d9586658d748e08a0ffd6c610044`.

The modules checked for the new proof are the covariance/nondegeneracy and actual-moment chain; exact finite-count extraction; count-localized inversion; multiscale stopping and all fixed moments; high-order damped unsmoothing; retained isotropic, anisotropic and measurable-shape estimates; and the coherent raw cutoff identity. The main text and dependency guide were checked for integration points. This audit does not claim an independent proof-by-proof reconstruction of every inherited singularity or collision-space estimate.

The decisive distinction from v26 is that order comparison controls an actual unsmoothed box probability. Combining that probability with the known low-frequency convolution gives a bound for a single signed correction averaged over the box. The added physical result also compares distinct events relative to a denominator proved in the same revision. Neither addition is re-labeled as the stronger unresolved microscopic theorem.

All inherited core files and Python files are byte-identical. Six introduction/bibliography edits are explicitly replayable. Every old label and bibliography item remains; the replaced v26 abstract is retained separately. The complete manuscript remains an ordinary-source revision of the same paper, not a separate topic or a specialist-target rewrite.
