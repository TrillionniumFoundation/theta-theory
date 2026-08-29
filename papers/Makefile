PAPERS := paper-I-path-ensembles paper-II-physical-homogenization paper-III-endogenous-theta paper-IV-saddle-information paper-V-rigidity-tangent

.PHONY: all clean $(PAPERS)
all: $(PAPERS)
$(PAPERS):
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error -e '$$bibtex="/usr/bin/bibtex.original %O %B"' main.tex
clean:
	@for p in $(PAPERS); do cd $$p && latexmk -C main.tex; cd ..; done
