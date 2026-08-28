PAPERS := \
	paper-I-bilateral-response \
	paper-II-pressure-diffusion \
	paper-III-rough-theta \
	paper-IV-filtering-games \
	paper-V-representations

APPENDICES := \
	paper-I-bilateral-response/technical-appendix-v4.tex \
	paper-II-pressure-diffusion/technical-appendix-v4.tex \
	paper-III-rough-theta/technical-appendix-v4.tex \
	paper-III-rough-theta/physical-clock-appendix-v4.tex \
	paper-IV-filtering-games/technical-appendix-v4.tex \
	paper-V-representations/technical-appendix-v4.tex

.PHONY: all manuscripts appendices verify clean $(PAPERS)

all: manuscripts appendices

manuscripts: $(PAPERS)

$(PAPERS):
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

appendices:
	@for a in $(APPENDICES); do \
		d=$$(dirname $$a); f=$$(basename $$a); \
		cd $$d && latexmk -pdf -interaction=nonstopmode -halt-on-error $$f && cd - >/dev/null; \
	done

verify:
	python3 ../../tools/verify_referee_revision_v4.py --write-receipt
	python3 ../../tools/verify_referee_appendices_v4.py

clean:
	@for p in $(PAPERS); do \
		cd $$p && latexmk -C && cd ..; \
	done
