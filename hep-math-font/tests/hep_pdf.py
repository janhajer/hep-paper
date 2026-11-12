"""Inspect pdfTeX box lists: actual fonts/slots, spacing, sizes and scoping."""
from itertools import product
from pathlib import Path
import os
import re
import subprocess

from paths import work, environment
build=work/'hep-pdf'
build.mkdir(parents=True,exist_ok=True)
env=environment()
commands=[(1,'mathbf'),(2,'mathsf'),(4,'mathup'),(4,'mathrm'),(8,'mathtt')]
lines=[r'\documentclass{article}',r'\usepackage[oldstyle]{hep-font}',r'\usepackage{hep-math-font}',
       r'\begin{document}\showboxbreadth=10000\showboxdepth=1000']
sample=r'aA\alpha\Gamma\partial\nabla1'
pairs=[]

def pair(a,b):
    pairs.append((a,b))
    lines.extend([r'\setbox0=\hbox{'+a+r'}\showbox0',r'\setbox0=\hbox{'+b+r'}\showbox0'])

for length in range(5):
    for seq in product(commands,repeat=length):
        state=0
        for bit,_ in seq:
            if bit in (2,8): state &= ~10
            state |= bit
        body=sample
        for _,command in reversed(seq): body='\\'+command+'{'+body+'}'
        bank=(4 if state&8 else 2 if state&2 else 0)+(state&1)
        offset=128 if state&4 else 0
        # Independently specified packed slots: a,A,alpha,Gamma,partial,nabla,1.
        expected=''.join(r'\mathchar\numexpr"7000+256*\csname symhepalpha'+str(bank)+r'\endcsname+'
                         +str(offset+i)+r'\relax ' for i in [26,0,86,64,118,119,53])
        for style in [r'\displaystyle',r'\scriptstyle',r'\scriptscriptstyle']:
            pair('$'+style+' '+body+'$','$'+style+expected+'$')
for a,b in [
    (r'\mathbf{a+\mathsf{b+\mathup{c}}+d}+e',r'\mathbf{a}+\mathbfsf{b}+\mathbfsfup{c}+\mathbf{d}+e'),
    (r'\mathbf{\mathsf{\mathup{\frac{\partial f}{\partial x}+\hat{x}_\alpha^\beta+\sqrt\gamma+\sin x}}}',
     r'\mathbfsfup{\frac{\partial f}{\partial x}+\hat{x}_\alpha^\beta+\sqrt\gamma+\sin x}'),
    (r'\mathtt{\mathbf{\mathrm{a\alpha}}}',r'\mathbfttup{a\alpha}'),
    (r'\mathup{\mathit{a\alpha}}',r'a\alpha'),
    (r'\mathbf{\mathsf{\mathnormal{a\alpha123}}}',r'a\alpha123')]:
    pair('$'+a+'$','$'+b+'$')
for family,command in [('rmfamily','mathserif'),('sffamily','mathsf'),('ttfamily','mathtt')]:
    pair('{\\'+family+' $'+sample+'$}', '$\\'+command+'{'+sample+'}$')
    pair('{\\'+family+r'\bfseries $'+sample+'$}', r'{\boldmath $\mathbf{'+'\\'+command+'{'+sample+'}}$}')
pair(r'{\sffamily $a$}$a$',r'$\mathsf{a}$$a$')

# Native operator names must use ASCII slots, not the packed alphabet indices.
for name, command in [('sin', r'\sin'), ('rank123', r'\operatorname{rank123}')]:
    roman = ''.join(r'\mathchar\numexpr"7000+256*\csname symoperators\endcsname+'
                    +str(ord(c))+r'\relax ' for c in name)
    for modifier in ['',r'\mathsf',r'\mathbf',r'\mathbfttup']:
        body = modifier+'{'+command+' x}' if modifier else command+' x'
        pair('$'+body+'$',
             r'$\mathop{\kern0pt '+roman+r'}\nolimits '+(modifier+'{x}' if modifier else 'x')+'$')
# The sans-serif calligraphic capitals must come from a distinct design.
lines.append(r'$\mathcal{L}\mathbf{\mathcal{L}}\mathsf{\mathcal{L}}\mathbfsf{\mathcal{L}}$')
# Script and upright calligraphic capitals come from the hepscript alphabets
# 0-5: script, bold script, upright script, bold upright script, upright
# calligraphic, bold upright calligraphic. L is the 12th capital.
def script(alphabet):
    return (r'\mathchar\numexpr"7000+256*\symhepscript+'
            + str(26 * alphabet + 11) + r'\relax ')
for body, alphabet in [(r'\mathscr{L}', 0), (r'\mathbf{\mathscr{L}}', 1),
                       (r'\mathsf{\mathscr{L}}', 0), (r'\mathtt{\mathscr{L}}', 0),
                       (r'\mathup{\mathscr{L}}', 2), (r'\mathscr{\mathbfrm{L}}', 3),
                       (r'\mathup{\mathcal{L}}', 4), (r'\mathsfup{\mathcal{L}}', 4),
                       (r'\mathbfsfup{\mathcal{L}}', 5), (r'\mathcal{\mathscr{L}}', 0),
                       (r'\mathscr{\mathcal{\mathup{L}}}', 4)]:
    pair('$' + body + '$', '$' + script(alphabet) + '$')
pair(r'$\mathscr{xL1}$', r'$x\mathscr{L}1$')
pair(r'$\mathscr{\mathbb{R}}$', r'$\mathbb{R}$')
pair(r'$\mathscr{\mathnormal{L}}$', r'$L$')
lines.append(r'$\mathscr{L}\mathup{\mathcal{L}}\mathbfup{\mathcal{L}}$')
lines.append(r'\end{document}')
(build/'boxes.tex').write_text('\n'.join(lines)+'\n')
# \showbox deliberately emits ! OK, so a nonzero TeX exit status is expected.
p=subprocess.run(['pdflatex','-interaction=nonstopmode','boxes.tex'],cwd=build,env=env,stdout=subprocess.DEVNULL)
log=(build/'boxes.log').read_bytes().decode('latin1')
errors=re.findall(r'^! (.*)$',log,re.M)
assert errors and all(e=='OK.' for e in errors), errors[:10]
assert 'Missing character:' not in log and 'LaTeX Font Warning:' not in log
boxes=re.findall(r'> \\box0=\n(.*?)\n+! OK\.',log,re.S)
assert len(boxes)==2*len(pairs),(len(boxes),len(pairs))
for i,(a,b) in enumerate(pairs):
    assert boxes[2*i]==boxes[2*i+1], f'Pair {i}: {a} != {b}\n{boxes[2*i]}\n{boxes[2*i+1]}'
fonts=subprocess.run(['pdffonts','boxes.pdf'],cwd=build,env=env,text=True,stdout=subprocess.PIPE).stdout
for face in ['URWChanceryL-MediItal','LMMathSymbols10-Regular','LMMathSymbols10-Bold',
             'rsfs10','EUSM10','EUSB10']:
    assert face in fonts, face
print(f'PASS: {len(pairs)} pdfTeX font/slot/structure comparisons')
