PAPERS := \
	paper-I-bilateral-response \
	paper-II-pressure-diffusion \
	paper-III-rough-theta \
	paper-IV-filtering-games \
	paper-V-representations

.PHONY: all verify clean $(PAPERS)

all: $(PAPERS)

$(PAPERS):
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

verify:
	python3 ../../tools/verify_referee_revision_v4.py --write-receipt

clean:
	@for p in $(PAPERS); do \
		cd $$p && latexmk -C && cd ..; \
	done
