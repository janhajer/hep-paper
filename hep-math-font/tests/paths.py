"""Locations used by the hep-font/hep-math-font regression tests.

The tests use the packages and pdfTeX fonts that l3build writes to
build/local, so run `l3build unpack` in hep-math-font first (any l3build
doc or check run also does this). Results are written to build/python-tests.
"""
from pathlib import Path
import os

tests = Path(__file__).resolve().parent
repo = tests.parents[1]
sources = repo / 'hep-math-font'
local = repo / 'build' / 'local'
work = repo / 'build' / 'python-tests'
work.mkdir(parents=True, exist_ok=True)
texmfvar = work / 'texmf-var'


def environment(*inputs):
    """Environment for TeX runs: extra input directories, then build/local."""
    path = os.pathsep.join([str(p) for p in inputs] + [str(local), ''])
    fonts = str(local) + os.pathsep
    return dict(os.environ, TEXMFVAR=str(texmfvar), TEXMFCACHE=str(texmfvar),
                TEXINPUTS=path, TEXFONTS=fonts, TFMFONTS=fonts, VFFONTS=fonts,
                ENCFONTS=fonts, TEXFONTMAPS=fonts)
