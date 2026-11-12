"""Two-pass TOCs, including class entry macros that forward implicit arguments."""
from pathlib import Path
import os
import subprocess

from paths import work, environment
build = work / 'hep-toc'
build.mkdir(parents=True, exist_ok=True)
env = environment()

for engine in ['pdflatex', 'lualatex']:
    for cls in ['article', 'book', 'report']:
        for math in [False, True]:
            name = f'{engine}-{cls}-math{int(math)}'
            # The plain book case reproduces test.tex with default lining text;
            # other cases exercise oldstyle figures and nested font hooks too.
            options = '' if cls == 'book' and not math else '[oldstyle]'
            source = '\\documentclass{'+cls+'}\n\\usepackage'+options+'{hep-font}\n'
            if math:
                source += '\\usepackage{hep-math-font}\n'
            source += r'''
\begin{document}
\makeatletter
\let\beforetocnormalfont\normalfont
\edef\beforetocfont{\fontname\font}
\tableofcontents
\edef\aftertocfont{\fontname\font}
\ifx\beforetocnormalfont\normalfont\else\errmessage{TOC changed normalfont}\fi
\ifx\beforetocfont\aftertocfont\else\errmessage{TOC leaked numeral style}\fi
\makeatother
\section{test}
\part{Part 123}
'''
            if cls != 'article':
                source += '\\chapter{Chapter 123}\n'
            source += r'''
\section{Section 123}
\subsection{Subsection 123}
Ordinary text 0123456789.
\end{document}
'''
            (build/(name+'.tex')).write_text(source)
            # Ensure the test checks both a genuinely empty and a populated TOC.
            for suffix in ['.aux', '.toc']:
                (build/(name+suffix)).unlink(missing_ok=True)
            for turn in [1, 2]:
                p = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', name+'.tex'],
                                   cwd=build, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                (build/(name+f'-pass{turn}.stdout')).write_bytes(p.stdout)
                assert p.returncode == 0, f'{name}: pass {turn} failed; see {build}'
                log = (build/(name+'.log')).read_text(errors='replace')
                warnings = [s for s in log.splitlines() if ('Warning:' in s or 'Missing character:' in s)
                            and not s.startswith("Package nfssext-cfr Warning: Overwriting the format's definition of \\DeclareEnc")]
                assert not warnings, (name, turn, warnings)
            assert r'\contentsline {section}' in (build/(name+'.toc')).read_text()
            print('PASS', name, '(two passes; font state preserved)', flush=True)
