# The `hep-paper` package

A `LaTeX` package for publications in High Energy Physics.

## Introduction

The `hep-paper` package aims to provide a single style file containing most configurations and macros necessary to write appealing publications in High Energy Physics.
Instead of reinventing the wheel by introducing newly created macros `hep-paper` preferably loads third party packages as long as they are lightweight enough.

For usual publications it is enough to load additionally to the `article` class without optional arguments only the `hep-paper` package.

    \documentclass{article}
    \usepackage{hep-paper}

## Installation

Running `pdflatex hep-paper.ins` will generate the main style file `hep-paper.sty` together with the necessary datamodel file `hep-paper.dbx`.
These two files must be moved into a folder the `tex` installation is aware of, e.g. the folder containing the document that should use the `hep-paper` package.
Additionally the documentation file `hep-paper-documentation.tex` will be generated.
Subsequently running `pdflatex hep-paper-documentation.tex` will generate the documentation `hep-paper-documentation.pdf`.
Finally running `pdflatex hep-paper-implementation.dtx` will generate the complete documentation of the implementation `hep-paper-implementation.pdf`

## Author

Jan Hajer

## License

This file may be distributed and/or modified under the conditions of the `LaTeX` Project Public License, either version 1.3c of this license or (at your option) any later version.
The latest version of this license is in `http://www.latex-project.org/lppl.txt` and version 1.3c or later is part of all distributions of LaTeX version 2005/12/01 or later.
