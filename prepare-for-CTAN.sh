#!/bin/bash

runlatex () {
#   latexmk -pdflatex -bibtex $1
  latexmk --pdf $1
}

generate () {
  mv README-hep-$1.md README.md
  yes | pdflatex hep-$1.ins
  runlatex hep-$1-implementation.dtx
  runlatex hep-$1-documentation.tex
  ctanify -nos --noauto hep-$1.ins hep-$1-implementation.dtx hep-$1-documentation.pdf hep-$1-implementation.pdf bibliography.bib license.md README.md ${@:2}
  mv README.md README-hep-$1.md
}

if [ ! -f README-temp.md ]; then
  mv README.md README-temp.md
fi

generate "acronym"
generate "bibliography"
generate "float"
generate "font"
generate "graphic"
generate "math"
generate "math-font"
generate "paper"
generate "reference"
generate "text"
generate "title"

mv README-temp.md README.md
