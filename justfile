test:
	uv run ruff format
	uv run ruff check --fix
	uv run pyright src
	uv run pytest

clean:
	rm -rf data/*

ghostty:
	mkdir -p ./data/ghostty
	uv run render-template -v light ./templates/ghostty-theme > data/ghostty/okcolors-light
	uv run render-template -v dark ./templates/ghostty-theme > data/ghostty/okcolors-dark

compile variant="smooth":
	#!/bin/sh
	set -euo pipefail
	mkdir -p ./data
	dark_json=$(uv run export-colorscheme {{variant}} -v dark -f hex | jq '.colors')
	light_json=$(uv run export-colorscheme {{variant}} -v light -f hex | jq '.colors')
	echo '{"dark": '"$dark_json"', "light": '"$light_json"'}' | jq '.' > ./data/okcolors-{{variant}}.json

swatches:
	uv run render-swatch smooth -v dark
	uv run render-swatch smooth -v light
	uv run render-swatch sharp -v dark
	uv run render-swatch sharp -v light
