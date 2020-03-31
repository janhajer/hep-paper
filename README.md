# The `hep-paper` package

A `LaTeX` package for publications in High Energy Physics.

## Introduction

The `hep-paper` package aims to provide a single style file containing most configurations and macros necessary to write appealing publications in High Energy Physics.
Instead of reinventing the wheel by introducing newly created macros `hep-paper` preferably loads third party packages as long as they are lightweight enough.

For usual publications it is enough to load additionally to the `article` class without optional arguments only the `hep-paper` package.

    \documentclass{article}
    \usepackage{hep-paper}

## Author

Jan Hajer

## License

This file may be distributed and/or modified under the conditions of the `LaTeX` Project Public License, either version 1.3c of this license or (at your option) any later version.
The latest version of this license is in `http://www.latex-project.org/lppl.txt` and version 1.3c or later is part of all distributions of LaTeX version 2005/12/01 or later.
