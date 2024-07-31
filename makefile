.DEFAULT_GOAL = help

SRC_DIR ?= src
AUX_DIR ?= aux
BUILD_DIR ?= build

# reproducible build: https://tex.stackexchange.com/a/313605
export SOURCE_DATE_EPOCH = 0

TEMPLATE = ucb-letterhead.latex
LATEX = lualatex
DIFF = difft
pandocArg = -V linkcolorblue -V citecolor=blue -V urlcolor=blue

SRC = $(wildcard $(SRC_DIR)/*.md)
TEX = $(patsubst $(SRC_DIR)/%.md,$(AUX_DIR)/%.tex,$(SRC))
PDF = $(patsubst $(SRC_DIR)/%.md,$(BUILD_DIR)/%.pdf,$(SRC))

$(BUILD_DIR)/%.pdf: $(AUX_DIR)/%.tex
	@mkdir -p $(@D)
	latexmk -lualatex $< -auxdir=$(AUX_DIR) -outdir=$(BUILD_DIR)
$(AUX_DIR)/%.tex: $(SRC_DIR)/%.md $(TEMPLATE)
	@mkdir -p $(@D)
	pandoc -s -o $@ $< --template=$(TEMPLATE) $(pandocArg)

.PHONY: pdf open serve template diff clean Clean update help
pdf: $(PDF)  ## generate PDFs from markdown files
open: $(PDF)  ## open the PDFs
	open $^ --background
serve:  ## open and watch for changes and recompile the PDFs
	echo $(SRC) $(TEMPLATE) | tr ' ' '\n' | entr $(MAKE) open

template: $(TEMPLATE)  ## generate the pandoc UCB letterhead template
$(TEMPLATE): util/generate_pandoc_template.py
	$< > $@
diff: $(TEMPLATE)  ## show differences between the default template and the generated template
	$(DIFF) <(pandoc --print-default-template=latex) $<

clean:  ## remove generated files
	rm -rf $(AUX_DIR)
Clean: clean  ## remove generated files and PDFs
	rm -rf $(BUILD_DIR) *.pdf

update:  ## update environments using nix & devbox
	devbox update --all-projects --sync-lock
# modified from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:  ## print this help message
	@awk 'BEGIN{w=0;n=0}{while(match($$0,/\\$$/)){sub(/\\$$/,"");getline nextLine;$$0=$$0 nextLine}if(/^[[:alnum:]_-]+:.*##.*$$/){n++;split($$0,cols[n],":.*##");l=length(cols[n][1]);if(w<l)w=l}}END{for(i=1;i<=n;i++)printf"\033[1m\033[93m%-*s\033[0m%s\n",w+1,cols[i][1]":",cols[i][2]}' $(MAKEFILE_LIST)
print-%:
	$(info $* = $($*))
