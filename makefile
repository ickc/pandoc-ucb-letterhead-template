.DEFAULT_GOAL = help

TEMPLATE = ucb-letterhead.latex
LATEX = lualatex
DIFF = difft
pandocArg = -V linkcolorblue -V citecolor=blue -V urlcolor=blue

SRC = $(wildcard *.md)
PDF = $(patsubst %.md,%.pdf,$(SRC))

.PHONY: pdf
pdf: $(PDF)  ## generate PDFs from markdown files
%.pdf: %.md $(TEMPLATE)
	pandoc -s -o $@ $< --template=$(TEMPLATE) --pdf-engine=$(LATEX) $(pandocArg)

.PHONY: template
template: $(TEMPLATE)  ## generate the pandoc UCB letterhead template
$(TEMPLATE): util/generate_pandoc_template.py
	$< > $@

.PHONY: diff
diff: $(TEMPLATE)  ## show differences between the default template and the generated template
	$(DIFF) <(pandoc --print-default-template=latex) $<

.PHONY: clean
clean:  ## remove generated files
	rm -f *.pdf

# modified from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:  ## print this help message
	@awk 'BEGIN{w=0;n=0}{while(match($$0,/\\$$/)){sub(/\\$$/,"");getline nextLine;$$0=$$0 nextLine}if(/^[[:alnum:]_-]+:.*##.*$$/){n++;split($$0,cols[n],":.*##");l=length(cols[n][1]);if(w<l)w=l}}END{for(i=1;i<=n;i++)printf"\033[1m\033[93m%-*s\033[0m%s\n",w+1,cols[i][1]":",cols[i][2]}' $(MAKEFILE_LIST)
print-%:
	$(info $* = $($*))
