"""Dual-engine integration, dependency, option and font-shape regressions."""
from pathlib import Path
import os
import subprocess

from paths import work, environment
build = work / 'hep-integration'
build.mkdir(parents=True, exist_ok=True)
env = environment()
lower = 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma varsigma tau upsilon phi chi psi omega'
upper = 'Alpha Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu Nu Xi Omicron Pi Rho Sigma Tau Upsilon Phi Chi Psi Omega'
greek = ''.join('\\'+c+'{}\\allowbreak ' for c in (lower+' '+upper).split())
faces = '\n'.join('{\\'+family+' '+shape+' '+greek+r' 0123456789\par}' for family in ['rmfamily','sffamily','ttfamily']
                   for shape in ['',r'\bfseries',r'\itshape',r'\bfseries\itshape'])
formula = r'''$\mathcal{ABC}+\mathscr{ABC}+\mathbb{R}+\mathfrak{g}+\bm{\sum_i x_i}$
$\mathsf{\frac{\partial f}{\partial x}+\hat{x}_\alpha^\beta+\sqrt\gamma+\sin x}$
{\sffamily $a\alpha\Gamma\partial123$} {\ttfamily $a\alpha\Gamma\partial123$}
{\bfseries $a\alpha\Gamma\partial123$} $a\alpha\Gamma\partial123$
'''

def run(engine, name, preamble, body, error=None, passes=1):
    name = engine+'-'+name
    src = '\\documentclass[12pt]{article}\n'+preamble+'\n\\begin{document}\n'+body+'\n\\end{document}\n'
    (build/(name+'.tex')).write_text(src)
    for _ in range(passes):
        p = subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=build,env=env,
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (build/(name+'.stdout')).write_text(p.stdout)
    log = (build/(name+'.log')).read_text(errors='replace')
    if error:
        assert p.returncode and error in ' '.join(log.split()), name+': expected '+error
    else:
        assert p.returncode == 0, name+': compile failed'
        warnings = [s for s in log.splitlines() if ('Warning:' in s or 'Missing character:' in s)
                    and not s.startswith("Package nfssext-cfr Warning: Overwriting the format's definition of \\DeclareEnc")]
        assert not warnings, name+': '+repr(warnings[:5])+' (see full log)'
    print('PASS',name,flush=True)

for engine in ['pdflatex','lualatex']:
    run(engine,'text-alone',r'\usepackage[oldstyle]{hep-font}',faces)
    if engine == 'lualatex':
        run(engine,'text-with-unicode-math',r'\usepackage{hep-font}\usepackage{unicode-math}',faces)
    run(engine,'math-alone',r'\usepackage{hep-math-font}',formula)
    for symbols in ['true','false','ams','minion']:
        pre = r'\usepackage[oldstyle]{hep-font}\usepackage[symbols='+symbols+r']{hep-math-font}'
        body = faces + (formula if symbols != 'false' else r'$\mathbf{\mathsf{\alpha123}}$')
        run(engine,'symbols-'+symbols,pre,body,
            'symbols=minion is not supported' if symbols=='minion' and engine=='lualatex' else None)
    run(engine,'invalid-symbols',r'\usepackage[symbols=typo]{hep-math-font}','', 'Unknown symbols option')
    run(engine,'invalid-size',r'\usepackage[size=typo]{hep-font}','','Invalid font size')
    for size, expect in [('default','12'),('10.5pt','10.5')]:
        run(engine,'size-'+size,r'\usepackage[size='+size+r']{hep-font}',
            r'\makeatletter\ifdim\f@size pt='+expect+r'pt\else\errmessage{Wrong font size}\fi\makeatother Size.')
    run(engine,'references',r'\usepackage[oldstyle]{hep-font}\usepackage{hep-math-font}\usepackage{hyperref}',
        r'''\tableofcontents\section{A heading $a\alpha$}
\begin{equation}\label{eq:test}a=123\end{equation}
Reference \ref{eq:test}, \eqref{eq:test}.
\begin{figure}\centering 123\caption{123}\end{figure}
\makeatletter\edef\actual{\theequation}\def\expected{1}\ifx\actual\expected\else\errmessage{Nonsemantic equation counter}\fi\makeatother
'''.replace(r'\section{A heading $a\alpha$}',r'\section{A heading}'),passes=2)
    # nfssext-cfr stores its variant list globally in \set whenever an
    # oldstyle family switches numerals, for example in the equation tag
    # that align typesets while measuring; a user \set must survive.
    for numerals in ['oldstyle','lining']:
        run(engine,'set-'+numerals,r'\usepackage['+numerals+r']{hep-font}\usepackage{amsmath}'
            r'\newcommand*\set[1]{\{#1\}}\let\savedset\set',
            r'''\begin{align}\set{}\end{align}
{\tstyle 1}{\ostyle 2}{\lstyle 3}{\pstyle 4}\texttl{5}
\ifx\set\savedset\else\errmessage{nfssext-cfr overwrote set}\fi''')
    # url.sty sets its argument in math mode with the text font as family 0;
    # letters and digits must keep their native math codes there.
    url = '10.1007/JHEP11(2022)082'
    for style in ['tt','rm','sf']:
        for extra in ['',r'\usepackage{hyperref}']:
            name = 'url-'+style+('-hyperref' if extra else '')
            run(engine,name,r'\usepackage{hep-math-font}\usepackage{url}'+extra,
                r'\urlstyle{'+style+r'}\url{'+url+r'} $\mathbf{x}_1$ \url{'+url+'}',passes=2)
            text = subprocess.run(['pdftotext',engine+'-'+name+'.pdf','-'],cwd=build,
                                  stdout=subprocess.PIPE,text=True,check=True).stdout
            assert text.split()[0::2] == [url,url], engine+'-'+name+': '+repr(text)

run('xelatex','smoke',r'\usepackage[oldstyle]{hep-font}\usepackage{hep-math-font}',faces+formula)
