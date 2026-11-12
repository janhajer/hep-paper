# The `hep-paper` bundle

A bundle of `LaTeX` packages improving some parts of the default setup.

## Introduction

The `hep-paper` package loads most of the other packages.

## Packages

Each directory `hep-*` contains one package, released to CTAN on its own:
`hep-paper`, `hep-font`, `hep-math-font`, `hep-math`, `hep-text`, `hep-float`, `hep-reference`, `hep-title`, `hep-acronym`, `hep-bibliography`, `hep-graphic`, `hep-talk`, and `hep-cv`.
`hep-erc` and `hep-cv-private` are private: built, tested and installed, but not released.

## Building

The bundle is built with [`l3build`](https://ctan.org/pkg/l3build), which is part of TeX Live.
The pdfTeX virtual fonts of `hep-math-font` are generated with Python 3 and [fontTools](https://pypi.org/project/fonttools/).

```sh
l3build doc       # typeset all documentation
l3build check     # run the regression tests
l3build install   # install all packages into the local texmf tree
l3build ctan      # create the CTAN archives
```

Run the same commands inside a package directory to process only that package.

## Author

Jan Hajer

## License

This file may be distributed and/or modified under the conditions of the `LaTeX` Project Public License, either version 1.3c of this license or (at your option) any later version.
The latest version of this license is in `http://www.latex-project.org/lppl.txt` and version 1.3c or later is part of all distributions of LaTeX version 2005/12/01 or later.
