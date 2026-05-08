# Shortcuts for the bbo-vault ingestion pipeline, powered by uv.
#
# Setup:
#   curl -LsSf https://astral.sh/uv/install.sh | sh   # install uv
#   make sync                                          # install deps
#
# Use:
#   make all       # download + convert
#   make download  # fetch raw PDFs and HTML
#   make convert   # convert raw/ to markdown
#   make clean     # delete raw/ and raw-md/ (keeps your vault notes)
#   make help      # show all targets

UV     ?= uv
RAW    := scripts/raw
RAW_MD := scripts/raw-md

.PHONY: help all download convert clean sync lock check-uv

help:
	@echo "Targets:"
	@echo "  make sync         create venv and install deps from pyproject.toml"
	@echo "  make all          download all sources and convert to markdown"
	@echo "  make download     fetch raw PDFs and HTML into $(RAW)/"
	@echo "  make convert      convert $(RAW)/ to markdown in $(RAW_MD)/"
	@echo "  make lock         refresh uv.lock"
	@echo "  make clean        remove $(RAW) and $(RAW_MD) (keeps vault notes)"
	@echo ""
	@echo "Variables:"
	@echo "  TIER=1|2|3   limit downloads to a tier (default: 3 = all)"
	@echo "  UV=...       override uv binary (default: uv)"

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || { \
	  echo "ERROR: 'uv' not found. Install it with:"; \
	  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	  exit 1; \
	}

sync: check-uv
	$(UV) sync

lock: check-uv
	$(UV) lock

all: download convert

download: check-uv
	cd scripts && $(UV) run download_raw.py $(if $(TIER),--tier $(TIER),)

convert: check-uv
	cd scripts && $(UV) run convert_to_md.py

clean:
	rm -rf $(RAW) $(RAW_MD)
	@echo "Removed $(RAW) and $(RAW_MD). Vault notes are untouched."
