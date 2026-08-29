PAPERS := paper-I-specular-ensembles paper-II-specular-homogenization paper-III-specular-theta paper-IV-specular-control paper-V-specular-rigidity

all:
	@set -e; for p in $(PAPERS); do \
	  cd $$p; pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null; \
	  bibtex main >/dev/null; \
	  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null; \
	  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null; cd ..; \
	done

clean:
	@find . -name '*.aux' -o -name '*.bbl' -o -name '*.blg' -o -name '*.log' -o -name '*.out' -o -name '*.toc' | xargs -r rm -f
