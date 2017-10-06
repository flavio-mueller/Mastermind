# documents 
BUILD_DIR := build
RES_DIR := res

SOURCES := mastermind.tex
DOCUMENTS := $(patsubst %.tex,$(BUILD_DIR)/%.pdf,$(SOURCES))

RES_SRC := $(wildcard $(RES_DIR)/*.svg)
RES := $(patsubst %.svg,%.pdf,$(RES_SRC))

# compiler settings
TEX := texfot lualatex

# recipes
.PHONY: all dir clean
all: $(DOCUMENTS)

$(DOCUMENTS): $(BUILD_DIR)/%.pdf: %.tex $(SOURCES) $(RES) dir
	@printf "\nBuilding $< \n\n"
	$(TEX) --output-directory=$(BUILD_DIR) $<

$(RES): $(RES_DIR)/%.pdf: $(RES_DIR)/%.svg $(RES_SRC) dir
	inkscape -z -D --file=$< --export-pdf=$@

dir:
	mkdir -p $(BUILD_DIR)

clean:
	rm $(BUILD_DIR)/*
