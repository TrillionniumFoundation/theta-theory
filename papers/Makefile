PAPERS := paper-I-liouville-ensembles paper-II-cell-homogenization paper-III-theta-generator paper-IV-control-information paper-V-rigidity-tangent

.PHONY: all clean $(PAPERS)
all: $(PAPERS)
$(PAPERS):
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	@for p in $(PAPERS); do cd $$p && latexmk -C main.tex; cd ..; done
