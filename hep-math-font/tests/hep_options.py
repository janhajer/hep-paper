"""Check the HEP mathsf family option with both engines and document families."""
from pathlib import Path
import os
import subprocess

from paths import work, sources, environment
build = work / 'hep-options'
build.mkdir(parents=True, exist_ok=True)
env = environment(build, sources)
(build / 'extract.ins').write_text(
    r'\input docstrip.tex \keepsilent\askforoverwritefalse\nopreamble\nopostamble'
    r'\generate{\file{hep-math-font.sty}{\from{hep-math-font-implementation.dtx}{package}}}'
    r'\endbatchfile')
subprocess.run(['tex', '-8bit', '-interaction=batchmode', 'extract.ins'],
               cwd=build, env=env, check=True, stdout=subprocess.DEVNULL)

for engine in ['pdflatex', 'lualatex']:
    for sans in [False, True]:
        for contrast in [None, False, True]:
            name = f'{engine}-sans{int(sans)}-contrast{contrast}'
            options = 'oldstyle' + (',sans' if sans else '')
            mathsf_option = '' if contrast is None else '[mathsf=' + ('contrast' if contrast else 'sans') + ']'
            source = r'''\documentclass{article}
\usepackage[OPTIONS]{hep-font}
\usepackageMATHSF{hep-math-font}
\pagestyle{empty}
\begin{document}
$\mathsf{a\alpha123}$
$\mathbfsf{a\alpha123}$
$\mathsf{\frac{a_1}{\alpha^2}}$
$\mathserif{\mathbb{R}}\mathsf{\mathbb{R}}$
\end{document}
'''.replace('OPTIONS', options).replace('MATHSF', mathsf_option)
            (build / (name + '.tex')).write_text(source)
            result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', name + '.tex'],
                                    cwd=build, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            (build / (name + '.stdout')).write_text(result.stdout)
            assert result.returncode == 0, name + ': see ' + str(build / (name + '.stdout'))
            log = (build / (name + '.log')).read_text(errors='replace')
            assert 'Missing character:' not in log and 'LaTeX Font Warning:' not in log, name + ': font warning'
            fonts = subprocess.check_output(['pdffonts', str(build / (name + '.pdf'))], text=True)
            (build / (name + '.fonts')).write_text(fonts)
            serif_target = sans and contrast is True
            if engine == 'lualatex':
                expected = 'NewCMMath-Regular' if serif_target else 'NewCMSansMath-Regular'
                assert expected in fonts, name + ': expected ' + expected + '\n' + fonts
            else:
                # The alphabet glyph a and Greek alpha come from this OML face.
                expected = 'LMMathItalic' if serif_target else 'ComputerModernSans-Mathitalic'
                assert expected.lower() in fonts.lower(), name + ': expected ' + expected + '\n' + fonts
            # The composable blackboard uses both serif and sans-serif faces.
            # With mathsf=contrast in a sans document \mathsf selects serif.
            bb = (['NewCMMath-Regular'] if engine == 'lualatex' else ['ncmbb-regular'])
            if not serif_target:
                bb.append('NewCMSansMath-Regular' if engine == 'lualatex' else 'BBOLDX-Regular')
            for face in bb:
                assert face.lower() in fonts.lower(), name + ': expected ' + face + '\n' + fonts
            print('PASS', name, '->', 'serif' if serif_target else 'sans', flush=True)

print('PASS: 12 engine/document/option combinations')
