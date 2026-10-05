# Exact support certificate — v84

`support_geometry.py INPUT [--verify CERTIFICATE] [--max-system-dimension CAP]` accepts canonical Gaussian-rational Hermitian effects with exact positivity and sum I, together with a Hermitian generator. The schema is `gtf84.support-orbit/1`; see `examples/support-bb84.json`. Integers for dimension/outcome count are strict positive integers, not booleans. No floating tolerance or numerical rank decision is used.

The output reconstructs support projections, their ranks, the support-span dimension, the covariance-kernel dimension, and the Hilbert–Schmidt projection and complement of the generator. It labels a fixed known orbit stationary, square_root, or linear under the written finite-angle theorem. The certificate does not estimate an unknown device, evaluate D_N, give uniform constants over E,G, synthesize arbitrary controls, or execute a physical protocol. Replay recomputes every field exactly; extra or modified fields fail. Exceeding the resource cap returns an error, not a partial certificate.

The internal `transported_energy` routine evaluates the regularized dual form with rational public weights and tau. It returns `None` for +infinity off the range. Its coordinate system uses the inherited nonorthogonal tangent basis and the exact operator stiffness; the full Hilbert–Schmidt pairing is retained. Zero output rows and reversible label refinements are covered by tests, not omitted.

The current suite contains 280 positive checks and 18 negative controls. A symbolic BB84 logical recovery verifies a particular nonzero-angle channel identity. It neither executes the general recovery construction nor proves continuum statements by finite enumeration.
