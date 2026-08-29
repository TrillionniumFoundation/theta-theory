BIBTEX ?= bibtex

PAPERS := \
	paper-I-geometric-response \
	paper-II-physical-rough \
	paper-III-dpp-hjb \
	paper-IV-filtering-games \
	paper-V-tangent-laws

.PHONY: all clean $(PAPERS)

all: $(PAPERS)

$(PAPERS):
	cd $@ && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd $@ && $(BIBTEX) main
	cd $@ && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd $@ && pdflatex -interaction=nonstopmode -halt-on-error main.tex

clean:
	for p in $(PAPERS); do \
	  rm -f $$p/main.aux $$p/main.bbl $$p/main.blg $$p/main.fdb_latexmk \
	        $$p/main.fls $$p/main.log $$p/main.out $$p/main.toc; \
	done
