"""Generate permutations and test real LuaLaTeX output, without PDF text heuristics."""
from itertools import product
from pathlib import Path
import os
import subprocess
import sys

from paths import tests, work, environment
build = work
env = environment()
commands = [(1, 'mathbf'), (2, 'mathsf'), (4, 'mathup'), (4, 'mathrm'), (8, 'mathtt')]
sample = r'aA\alpha\Gamma\partial\nabla1'
lines = [r'\documentclass{article}', r'\usepackage[oldstyle]{hep-font}', r'\usepackage{hep-math-font}',
         r'\begin{document}', r'\directlua{checks = dofile("' + (tests / 'check.lua').as_posix() + '")}',
         r'\newcommand{\sample}{' + sample + '}']

def wrap(seq, body):
    for _, command in reversed(seq):
        body = '\\' + command + '{' + body + '}'
    return body

# All subsets, all orders, and repeated modifiers (idempotence).
for length in range(5):
    for seq in product(commands, repeat=length):
        state = 0
        for bit, _ in seq:
            if bit in (2, 8):
                state &= ~10  # The innermost family selector wins.
            state |= bit
        for style in [r'\displaystyle', r'\scriptstyle', r'\scriptscriptstyle']:
            lines.append(r'\setbox0=\hbox{$' + style + wrap(seq, r'\sample') + '$}')
            lines.append(r'\directlua{checks.check(' + str(state) + ')}')

for state, command in [(3, 'mathbfsf'), (5, 'mathbfup'), (6, 'mathsfup'), (7, 'mathbfsfup'),
                       (9, 'mathbftt'), (12, 'mathttup'), (13, 'mathbfttup')]:
    lines += [r'\setbox0=\hbox{$' + chr(92) + command + r'{\sample}$}',
              r'\directlua{checks.check(' + str(state) + ')}']

pairs = [
    (r'\mathbf{a+\mathsf{b+\mathup{c}}+d}+e',
     r'\mathbf{a}+\mathbfsf{b}+\mathbfsfup{c}+\mathbf{d}+e'),
    (r'\mathbf{\mathsf{\mathup{\frac{\partial f}{\partial x}+\hat{x}_{\alpha}^{\beta}+\sqrt{\gamma}+\sin x}}}',
     r'\mathbfsfup{\frac{\partial f}{\partial x}+\hat{x}_{\alpha}^{\beta}+\sqrt{\gamma}+\sin x}'),
    (r'\mathsf\sample', r'\mathsf{\sample}'),
    (r'\mathbf{a+\mathtt{b+\mathrm{c}}+d}+e',
     r'\mathbf{a}+\mathbftt{b}+\mathbfttup{c}+\mathbf{d}+e'),
    (r'\mathtt{\mathbf{\mathrm{\frac{\partial f}{\partial x}+\hat{x}_{\alpha}^{\beta}+\sqrt{\gamma}+\sin x}}}',
     r'\mathbfttup{\frac{\partial f}{\partial x}+\hat{x}_{\alpha}^{\beta}+\sqrt{\gamma}+\sin x}'),
]
# The blackboard flag commutes with the other modifiers and is idempotent.
pairs += [(r'\mathbb{\mathsf{\mathbf{Rx1}}}', r'\mathbfsf{\mathbb{Rx1}}'),
          (r'\mathbf{\mathbb{Rx1}}', r'\mathbb{\mathbf{Rx1}}'),
          (r'\mathbb{\mathbb{R}}', r'\mathbb{R}'),
          (r'\mathbb{\mathup{R}}', r'\mathbb{\mathit{R}}'),
          (r'\mathbb{\mathnormal{R}}', r'R')]
# The calligraphic flag likewise; it excludes blackboard, innermost wins.
pairs += [(r'\mathcal{\mathsf{\mathbf{AB}}}', r'\mathbfsf{\mathcal{AB}}'),
          (r'\mathbf{\mathcal{L}}', r'\mathcal{\mathbf{L}}'),
          (r'\mathcal{\mathcal{L}}', r'\mathcal{L}'),
          (r'\mathcal{\mathtt{L}}', r'\mathcal{\mathsf{L}}'),
          (r'\mathcal{xA1}', r'x\mathcal{A}1'),
          (r'\mathcal{\mathbb{R}}', r'\mathbb{R}'),
          (r'\mathbb{\mathcal{R}}', r'\mathcal{R}'),
          (r'\mathcal{\mathnormal{L}}', r'L')]
# The script flag likewise; the three flags exclude each other.
pairs += [(r'\mathscr{\mathsf{\mathbf{AB}}}', r'\mathbfsf{\mathscr{AB}}'),
          (r'\mathbf{\mathscr{L}}', r'\mathscr{\mathbf{L}}'),
          (r'\mathscr{\mathscr{L}}', r'\mathscr{L}'),
          (r'\mathscr{\mathtt{L}}', r'\mathscr{\mathsf{L}}'),
          (r'\mathscr{xA1}', r'x\mathscr{A}1'),
          (r'\mathscr{\mathcal{L}}', r'\mathcal{L}'),
          (r'\mathcal{\mathscr{L}}', r'\mathscr{L}'),
          (r'\mathscr{\mathbb{R}}', r'\mathbb{R}'),
          (r'\mathbb{\mathscr{R}}', r'\mathscr{R}'),
          (r'\mathscr{\mathnormal{L}}', r'L')]
# Upright calligraphic (Euler) and script (slanted back) capitals.
pairs += [(r'\mathup{\mathcal{L}}', r'\mathcal{\mathrm{L}}'),
          (r'\mathup{\mathcal{L}}', r'\mathsfup{\mathcal{L}}'),
          (r'\mathbfup{\mathcal{L}}', r'\mathcal{\mathbf{\mathup{L}}}'),
          (r'\mathup{\mathscr{L}}', r'\mathscr{\mathrm{L}}'),
          (r'\mathbfsfup{\mathscr{L}}', r'\mathsf{\mathscr{\mathbfup{L}}}'),
          (r'\mathup{\mathit{\mathscr{L}}}', r'\mathscr{L}')]
differ = [(r'\mathcal{L}', r'L'), (r'\mathcal{L}', r'\mathsf{\mathcal{L}}'),
          (r'\mathcal{L}', r'\mathbf{\mathcal{L}}'),
          (r'\mathsf{\mathcal{L}}', r'\mathbfsf{\mathcal{L}}'),
          (r'\mathcal{L}', r'\mathup{\mathcal{L}}'),
          (r'\mathup{\mathcal{L}}', r'\mathbfup{\mathcal{L}}'),
          (r'\mathscr{L}', r'\mathsf{\mathscr{L}}'),
          (r'\mathscr{L}', r'\mathbf{\mathscr{L}}'),
          (r'\mathscr{L}', r'\mathup{\mathscr{L}}'),
          (r'\mathsf{\mathscr{L}}', r'\mathsfup{\mathscr{L}}'),
          (r'\mathup{\mathscr{L}}', r'\mathup{\mathcal{L}}')]
# The stylistic set replaces the calligraphic by the script glyphs.
for a, b in [(r'\mathcal{AL}', r'\mathscr{AL}'),
             (r'\mathsf{\mathcal{AL}}', r'\mathsf{\mathscr{AL}}'),
             (r'\mathbf{\mathcal{AL}}', r'\mathbf{\mathscr{AL}}'),
             (r'\mathcal{AL}', r'\mathup{\mathscr{AL}}')]:
    lines += [r'\setbox0=\hbox{$' + a + '$}', r'\setbox1=\hbox{$' + b + '$}',
              r'\directlua{checks.glyphdiffer()}']
for a, b in differ:
    lines += [r'\setbox0=\hbox{$' + a + '$}', r'\setbox1=\hbox{$' + b + '$}',
              r'\directlua{checks.differ()}']
for command in ['mathup', 'mathbf', 'mathsf', 'mathtt', 'mathbfttup']:
    pairs.append(('\\' + command + r'{\epsilon\phi\varepsilon\varphi\partial\nabla}',
                  '\\' + command + '{ϵϕεφ∂∇}'))
for a, b in pairs:
    lines += [r'\setbox0=\hbox{$' + a + '$}', r'\setbox1=\hbox{$' + b + '$}',
              r'\directlua{checks.equal()}']

lower = 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma varsigma tau upsilon phi chi psi omega'
upper = 'Alpha Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu Nu Xi Omicron Pi Rho Sigma Tau Upsilon Phi Chi Psi Omega'
greek_commands = ''.join('\\' + name + '{}' for name in (lower + ' ' + upper).split())
greek_literal = 'αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
math_greek = greek_literal.replace('ε', 'ϵ').replace('φ', 'ϕ')
for command, face in [('mathtt', 'Italic'), ('mathbftt', 'BoldOblique'),
                      ('mathttup', 'Regular'), ('mathbfttup', 'Bold')]:
    for style in [r'\displaystyle', r'\scriptstyle', r'\scriptscriptstyle']:
        lines += [r'\setbox0=\hbox{$' + style + '\\' + command + '{' + greek_commands + '}$}',
                  r'\directlua{checks.monogreek("' + math_greek + '", "' + face + '")}']
for family in [r'\rmfamily', r'\sffamily', r'\ttfamily']:
    for shape in ['', r'\itshape', r'\bfseries', r'\bfseries\itshape']:
        face = family + shape + ' '
        lines += [r'\setbox0=\hbox{' + face + '0123456789}',
                  r'\setbox1=\hbox{' + face + r'\addfontfeatures{Numbers=Lining}0123456789}',
                  r'\directlua{checks.oldstyle()}',
                  r'\setbox0=\hbox{' + face + greek_commands + '}',
                  r'\setbox1=\hbox{' + face + greek_literal + '}',
                  r'\directlua{checks.textgreek()}']
lines += [r'\directlua{texio.write_nl("PASS: "..checks.count.." glyph/structure checks")}',
          r'\end{document}']
# Check inherited text defaults independently of explicit modifiers.
for family, command in [('rmfamily','mathserif'),('sffamily','mathsf'),('ttfamily','mathtt')]:
    for textbold, mathbold in [('', ''), (r'\bfseries', r'\boldmath')]:
        lines[-2:-2] = [r'\setbox0=\hbox{' + '\\' + family + textbold + ' $' + sample + '$}',
                        r'\setbox1=\hbox{' + mathbold + r'\relax $' + '\\' + command + '{' + sample + '}$}',
                        r'\directlua{checks.equal()}']
lines[-2:-2] = [r'\setbox0=\hbox{$\mathbf{\mathsf{\mathnormal{\sample}}}$}',
                r'\setbox1=\hbox{$\sample$}', r'\directlua{checks.equal()}']
name = 'hep-regression'
(build / (name + '.tex')).write_text('\n'.join(lines) + '\n')
subprocess.run(['lualatex', '-interaction=nonstopmode', '-halt-on-error',
                '-output-directory=' + str(build), str(build / (name + '.tex'))], env=env, check=True, stdout=subprocess.DEVNULL)
log = (build / (name + '.log')).read_text(errors='replace')
assert 'Missing character:' not in log and 'LaTeX Font Warning:' not in log, name + ': font warning'
print(next(line for line in log.splitlines() if 'PASS:' in line))
