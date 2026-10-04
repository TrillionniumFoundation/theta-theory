#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
export TEXINPUTS="$(pwd)/build:${TEXINPUTS:-}:"
for pass in 1 2 3; do
  for document in companion main; do
    latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
      -latexoption=-no-shell-escape -outdir=build "$document.tex"
  done
done
cp build/main.pdf A2-v43-primary.pdf
cp build/companion.pdf A2-v43-companion.pdf
