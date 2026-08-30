PAPERS := papers/A1-exact-benchmarks papers/A2-sinai-homological-pressure papers/A3-full-empirical-path-ldp papers/A4-history-memory-universal-pressure papers/B1-microcanonical-preparation papers/B2-collision-clusters-dynamic-ldp papers/B3-hamilton-boltzmann-cotangents papers/B4-nonlinear-kinetic-semigroups papers/C1-information-risk-sensitive-saddles papers/C2-cotangent-rigidity-tangent-representations papers/D1-deterministic-theta-contractions

.PHONY: all clean $(PAPERS)
all: $(PAPERS)
$(PAPERS):
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	@for p in $(PAPERS); do cd $$p && latexmk -C main.tex; cd ../..; done
