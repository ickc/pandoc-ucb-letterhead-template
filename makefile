SHELL = /usr/bin/env bash

SRC = $(wildcard *.md)
TEX = $(patsubst %.md,%.tex,$(SRC))
PDF = $(patsubst %.md,%.pdf,$(SRC))

TEMPLATE = ucb-letterhead.latex
LATEX = lualatex

pdf: $(PDF) $(TEX)

%.tex: %.md $(TEMPLATE)
	pandoc -s -o $@ $< --template=$(TEMPLATE)

%.pdf: %.tex
	latexmk -$(LATEX) $<

clean:
	find -name '*.tex' -exec latexmk -c {} \;
	rm -f $(TEX) $(PDF)

print-%:
	$(info $* = $($*))
